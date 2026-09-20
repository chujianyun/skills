# Autoresearch feature discovery

> Runs an autoresearch loop that proposes TypeSafe questions, converts free text into numeric features, and uses model errors to improve a supervised CatBoost regressor.

*TypeSafe questions turn free text into numeric features for a supervised CatBoost model;
use an autoresearch loop to discover them.*

CatBoost needs a table of numbers, and a tasting note is not one. This cookbook builds the
table out of questions about the note, and none of them are written by hand. An LLM
proposes the questions, TypeSafe answers them for every row, and CatBoost trains on the
answers. The autoresearch part is what comes next: CatBoost reports which questions it used
and which rows it still gets wrong, the following proposal call reads that report, and the
loop runs again.

By the end you have a loop you can point at your own labelled text, a curve of held-out
error per round, and a table of which questions the final model used most.

```
tasting note
    |
    v
38 TypeSafe answers
    |-- 29 score questions x 2 columns = 58
    |     expected rubric level + answer uncertainty
    `--  9 noul questions  x 1 column  =  9
          probability true
    |
    v
67 numeric columns --> CatBoost --> predicted critic score
                                     held-out RMSE: 1.77 points
```

A score answer becomes two columns: the average level the answer points at, and how spread
out it is around that average. A noul answer is one probability, so it is one column.

The data is 2,000 wine reviews: a tasting note in, the critic's score on an 80-100 scale
out. RMSE measures prediction error in critic-score points, with larger misses counting for
more, and lower is better. Every number in the table below comes from the 800 reviews that
neither the model nor the loop ever saw.

| how the note becomes a score                            | RMSE     |
| ------------------------------------------------------- | -------- |
| predict the average score of the training rows          | 3.09     |
| the same CatBoost, reading the note as word counts      | 2.47     |
| ask TypeSafe for the score itself, rescaled and shifted | 2.15     |
| 18 questions from one proposal call, no loop            | 1.87     |
| **38 questions after five rounds of the loop**          | **1.77** |

The last two rows are the loop. One proposal call, with nothing to go on yet, gets to 1.87.
Four more rounds of reading its own worst predictions get to 1.77. Most of the gain is in
that first call, and how much the four rounds after it add is measured further down.

  Want to take this notebook further or apply it to another problem? See
  [Next steps](#next-steps).

```python
from __future__ import annotations

import json
import os
import random
import textwrap
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from time import perf_counter
from typing import NamedTuple

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from catboost import CatBoostRegressor
from cooksafe import JsonCache, make_playground_link
from IPython.display import Markdown, display
from typesafe_sdk import Noul, NoulCriteria, Score, TypeSafeClient

matplotlib.use("Agg")  # headless render

TYPESAFE_MODEL = "jev-1.12"
FOLDS, REPEATS = 5, 3  # repeats steady the error at this sample size
CATBOOST = dict(
    iterations=400,
    depth=4,
    learning_rate=0.05,
    loss_function="RMSE",
    verbose=0,
    random_seed=0,
    thread_count=1,
    allow_writing_files=False,
)

client = TypeSafeClient(
    # keyless kernels replay the cache
    api_key=os.environ.get("TYPESAFE_API_KEY", "cache-only"),
    base_url=os.environ.get("TYPESAFE_ENDPOINT"),
    timeout=120.0,
)
json_cache = JsonCache(Path("json_cache.json"))

# ----------------------------------------------------------------- the specification

INTENSITY_LEVELS = [
    "Not present in this note at all",
    "Barely present - mentioned once, in passing",
    "Present at a moderate level",
    "Present strongly - the note dwells on it",
    "Dominant - the note is largely about this",
]
PRESENCE_CRITERIA = NoulCriteria(
    true="The note states this or clearly implies it",
    false="The note gives no indication of this",
)

# Asking for the score outright: ten quality bands, rescaled onto the 80-100 critic scale.
SCORE_LEVELS = [
    "Faulty or unpleasant - the note is mostly criticism",
    "Barely acceptable - drinkable, with nothing to recommend it",
    "Simple and sound - correct, plain, forgettable",
    "Pleasant everyday wine - some appeal, little depth",
    "Good - clear varietal character, well made",
    "Very good - balanced, with something to say",
    "Excellent - complex and structured",
    "Outstanding - depth and length, built to age",
    "Superb - among the best of its type",
    "Profound - the note treats it as exceptional",
]

# Structured output requires every property in `required`, so unused fields come back empty.
PROPOSAL_SCHEMA = {
    "type": "object",
    "properties": {
        "actions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "op": {"type": "string", "enum": ["add", "revise", "drop"]},
                    "target": {"type": "string"},
                    "name": {"type": "string"},
                    "kind": {"type": "string", "enum": ["intensity", "presence"]},
                    "question": {"type": "string"},
                },
                "required": ["op", "target", "name", "kind", "question"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["actions"],
    "additionalProperties": False,
}

PROPOSALS = 18  # actions the proposer may return per round

# The one string that knows this is about wine. Point it at your own label and text.
PROPOSER_TASK = f"""You are designing numeric features for a gradient-boosting model that
predicts the score a wine critic gave (an integer from 80 to 100) from the tasting note alone.
The model sees nothing but the features you design.

Return up to {PROPOSALS} actions. Each action is one of:

- {{"op": "add", "target": "", "name": ..., "kind": ..., "question": ...}}
  A new feature.
- {{"op": "revise", "target": <name of an existing feature>, "name": ..., "kind": ...,
  "question": ...}}
  Replace that feature's question with better wording. Use this when a feature measures the
  right thing badly: too narrow, too vague, or worded so nearly every note answers the same.
- {{"op": "drop", "target": <name of an existing feature>, "name": "", "kind": "intensity",
  "question": ""}}
  Remove a feature that is not earning its place.

`kind` is "intensity" for something with a degree, or "presence" for a yes/no fact.
`question` is what gets asked about one tasting note.

An "intensity" question is graded against this fixed five-level rubric, so word it so that the
levels make sense:
{chr(10).join(f"  {i}. {level}" for i, level in enumerate(INTENSITY_LEVELS))}

A "presence" question is answered as the probability that it is true of the note.

Good features can be judged from the note's own words, vary from note to note, and carry
information about quality that the other features do not. Reviewers describe structure, fruit,
oak, length, complexity, and drinkability, and they also signal quality through word choice."""

class Split(NamedTuple):
    """The rows, their labels, and which half the loop is allowed to read."""

    notes: list[str]
    scores: np.ndarray
    dev: np.ndarray
    test: np.ndarray

# ----------------------------------------------------------------- the data

WINEMAG_CSV = (
    "https://huggingface.co/datasets/GroNLP/ik-nlp-22_winemag/resolve/"
    "90eb39f35fc64e556fc17f06d4137a4a69ec3297/train.csv"
)

@json_cache
def load_slice(n_dev: int, n_test: int, seed: int) -> dict:
    """Fetch the pinned CSV and take a seeded sample of note + score, one row per note."""
    import csv
    import io

    request = urllib.request.Request(
        WINEMAG_CSV, headers={"User-Agent": "typesafe-cookbook/1.0"}
    )
    with urllib.request.urlopen(request, timeout=300) as response:
        text = response.read().decode()
    rows, seen = [], set()
    for row in csv.DictReader(io.StringIO(text)):  # a few notes repeat verbatim
        if not row["description"] or not row["points"] or row["description"] in seen:
            continue
        seen.add(row["description"])
        rows.append((row["description"], float(row["points"])))
    random.Random(seed).shuffle(rows)
    picked = rows[: n_dev + n_test]
    return {"notes": [r[0] for r in picked], "points": [r[1] for r in picked]}

def example_rows(split: Split, out_of_fold: np.ndarray | None, n: int) -> list[int]:
    """Select representative dev rows for a proposer round."""
    dev = split.dev
    if out_of_fold is None:
        ranked = dev[np.argsort(split.scores[dev], kind="stable")]
        return [int(ranked[round(q * (len(ranked) - 1))]) for q in np.linspace(0, 1, n)]
    error = np.abs(split.scores[dev] - out_of_fold)
    order = np.argsort(-error, kind="stable")
    worst = [int(dev[i]) for i in order[: n // 2]]
    best = [int(dev[i]) for i in order[len(order) - (n - n // 2) :]]
    return worst + best

def example_block(
    rows: list[int],
    split: Split,
    out_of_fold: np.ndarray | None,
    previous: np.ndarray | None = None,
) -> str:
    """Format selected rows for the proposer."""
    if out_of_fold is None:
        head = "Example notes, with the score each one was given:"
        body = [f"- scored {split.scores[r]:.0f}: {split.notes[r]}" for r in rows]
        return head + "\n" + "\n".join(body)

    head = (
        "Dev notes, worst-predicted first. The first half is where your current questions "
        "miss by the most and the second half is where they are already right, so what "
        "separates the halves is what the questions have not captured."
    )
    if previous is not None:
        head += (
            " Each line also carries what the previous round predicted, so you can see which "
            "notes your last batch of questions moved."
        )
    body = []
    for r in rows:
        line = f"- scored {split.scores[r]:.0f}, predicted {out_of_fold[r]:.1f}"
        if previous is not None:
            line += f" (last round {previous[r]:.1f})"
        body.append(f"{line}: {split.notes[r]}")
    return head + "\n" + "\n".join(body)

def load_split(n_dev: int, n_test: int, seed: int = 0) -> Split:
    # keyword, because the cache key is the function name plus how each argument was spelled
    data = load_slice(n_dev, n_test, seed=seed)
    return Split(
        notes=data["notes"],
        scores=np.array(data["points"]),
        dev=np.arange(n_dev),
        test=np.arange(n_dev, n_dev + n_test),
    )

# ----------------------------------------------------------------- step 1: propose

def proposal_prompt(examples: str, feedback: str, accepted: list[dict]) -> str:
    parts = [PROPOSER_TASK, "\n" + examples]
    if accepted:
        parts.append(
            "\nThe features you have now. `add` must not duplicate one of these; `revise` and "
            "`drop` refer to one by name:\n"
            + "\n".join(
                f"- {f['name']} ({f['kind']}): {f['question']}" for f in accepted
            )
        )
    if feedback:
        parts.append("\nHow the model did with those features:\n" + feedback)
    return "\n".join(parts)

@json_cache
def propose(model: str, round_index: int, prompt: str) -> dict:
    """One proposal call. Every number in `prompt` is rounded so a replay hits the cache."""
    if model.startswith("claude"):
        import anthropic

        response = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY", "cache-only")
        ).messages.create(
            model=model,
            max_tokens=16000,
            output_config={
                "effort": "medium",
                "format": {"type": "json_schema", "schema": PROPOSAL_SCHEMA},
            },
            messages=[{"role": "user", "content": prompt}],
        )
        body = next(block.text for block in response.content if block.type == "text")
        usage = [response.usage.input_tokens or 0, response.usage.output_tokens or 0]
    else:
        from openai import OpenAI

        response = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY", "cache-only")
        ).chat.completions.create(
            model=model,
            reasoning_effort="high",
            max_completion_tokens=16000,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "user",
                    "content": prompt
                    + "\n\nReply with JSON matching this schema:\n"
                    + json.dumps(PROPOSAL_SCHEMA),
                }
            ],
        )
        body = response.choices[0].message.content
        usage = [response.usage.prompt_tokens, response.usage.completion_tokens]
    return {"actions": json.loads(body)["actions"][:PROPOSALS], "usage": usage}

def slug(name: str, taken: set[str]) -> str:
    """Names become question ids and column labels, so keep them plain and unique."""
    base = (
        "".join(c if c.isalnum() else "_" for c in name.lower()).strip("_") or "feature"
    )
    candidate, n = base, 2
    while candidate in taken:
        candidate, n = f"{base}_{n}", n + 1
    return candidate

def to_candidates(actions: list[dict], accepted: list[dict], round_index: int) -> tuple:
    """Split a round's actions into screenable candidates and a list of names to drop."""
    live = {f["name"] for f in accepted}
    drops = [a["target"] for a in actions if a["op"] == "drop" and a["target"] in live]
    replacing = {
        a["target"] for a in actions if a["op"] == "revise" and a["target"] in live
    }
    # a revision may keep the name it replaces, since that feature is on its way out
    taken, candidates = live - replacing, []
    for action in actions:
        if action["op"] == "drop":
            continue
        if action["op"] == "revise" and action["target"] not in live:
            continue  # a revision of something that is not there
        name = slug(action["name"], taken)
        taken.add(name)
        candidates.append(
            {
                "id": f"{name}@{round_index}",  # unique, so earlier rounds keep their columns
                "name": name,
                "kind": action["kind"],
                "question": action["question"],
                "replaces": action["target"] if action["op"] == "revise" else "",
            }
        )
    return candidates, drops

# ----------------------------------------------------------------- step 2: answer

def feature_questions(features: list[dict]) -> dict:
    questions = {}
    for feature in features:
        if feature["kind"] == "intensity":
            questions[feature["name"]] = Score(
                instructions=feature["question"], criteria=INTENSITY_LEVELS
            )
        else:
            questions[feature["name"]] = Noul(
                instructions=feature["question"], criteria=PRESENCE_CRITERIA
            )
    return questions

@json_cache
def answer(model: str, note: str, features_json: str) -> dict:
    """One request per note; every question of the round rides it. Keeps every probability."""
    features = json.loads(features_json)
    started = perf_counter()
    response = client.system_one(
        state=note, questions=feature_questions(features), model=model
    )
    raw = {}
    for feature in features:
        got = response.answers[feature["name"]]
        if feature["kind"] == "intensity":
            raw[feature["name"]] = [
                got.probabilities.get(i, 0.0) for i in range(len(INTENSITY_LEVELS))
            ]
        else:
            raw[feature["name"]] = [got.noul]
    return {
        "raw": raw,
        "seconds": round(perf_counter() - started, 2),
        "input_tokens": response.usage.input_tokens or 0,
        "output_tokens": response.usage.output_tokens or 0,
    }

def featurize(notes: list[str], features: list[dict]) -> dict:
    """Answer one question set for many notes: one request each, eight in flight."""
    payload = json.dumps(features, sort_keys=True)
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(
            pool.map(lambda note: answer(TYPESAFE_MODEL, note, payload), notes)
        )
    return {
        f["name"]: np.array([r["raw"][f["name"]] for r in results], dtype=float)
        for f in features
    }

def encode(feature: dict, probabilities: np.ndarray, mode: str) -> list[tuple]:
    """Turn one question's probabilities into named columns."""
    name = feature["name"]
    if feature["kind"] == "presence":
        return [(name, probabilities[:, 0])]  # one number is all there is
    levels = np.arange(probabilities.shape[1])
    mean = probabilities @ levels
    if mode == "mean":
        return [(name, mean)]
    if mode == "mean_spread":
        variance = probabilities @ (levels**2) - mean**2
        return [(name, mean), (f"{name}_sd", np.sqrt(np.clip(variance, 0, None)))]
    return [(f"{name}_p{i}", probabilities[:, i]) for i in levels]

def design(features: list[dict], answers_for: dict, mode: str) -> tuple:
    """Stack every feature's columns into one matrix, plus a label per column."""
    columns, labels = [], []
    for feature in features:
        for label, column in encode(feature, answers_for[feature["id"]], mode):
            columns.append(column)
            labels.append(label)
    return np.column_stack(columns), labels

def plain(features: list[dict]) -> list[dict]:
    """What goes on the wire and into the cache key: no id, no bookkeeping."""
    return [
        {"name": f["name"], "kind": f["kind"], "question": f["question"]}
        for f in features
    ]

# ----------------------------------------------------------------- step 3: fit

def rmse(y: np.ndarray, p: np.ndarray) -> float:
    return float(np.sqrt(np.mean((y - p) ** 2)))

def spearman(a: np.ndarray, b: np.ndarray) -> float:
    """Rank correlation: does the model order the wines the way the critic did?"""
    ranks = (
        np.argsort(np.argsort(a)).astype(float),
        np.argsort(np.argsort(b)).astype(float),
    )
    return float(np.corrcoef(*ranks)[0, 1])

def folds(y: np.ndarray, k: int, seed: int) -> list[np.ndarray]:
    """Label-stratified k-fold: sort by the label with a seeded tiebreak, then deal off the top."""
    rng = np.random.default_rng(seed)
    order = np.lexsort((rng.random(len(y)), y))
    return [np.sort(order[i::k]) for i in range(k)]

def cross_validate(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, float]:
    out_of_fold = np.zeros((REPEATS, len(y)))
    for repeat in range(REPEATS):
        for fold in folds(y, FOLDS, seed=repeat):
            train = np.setdiff1d(np.arange(len(y)), fold)
            model = CatBoostRegressor(**CATBOOST).fit(X[train], y[train])
            out_of_fold[repeat, fold] = model.predict(X[fold])
    scores = [rmse(y, out_of_fold[repeat]) for repeat in range(REPEATS)]
    return out_of_fold.mean(axis=0), float(np.mean(scores))

def importances(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    return CatBoostRegressor(**CATBOOST).fit(X, y).get_feature_importance()

def paired_gain(y: np.ndarray, before: np.ndarray, after: np.ndarray) -> tuple:
    """Bootstrap the paired held-out RMSE change."""
    squared = ((y - before) ** 2, (y - after) ** 2)
    rng = np.random.default_rng(0)
    drawn = []
    for _ in range(2000):
        rows = rng.integers(0, len(y), len(y))
        drawn.append(
            np.sqrt(squared[1][rows].mean()) - np.sqrt(squared[0][rows].mean())
        )
    drawn = np.array(drawn)
    return (
        rmse(y, after) - rmse(y, before),
        float(np.percentile(drawn, 2.5)),
        float(np.percentile(drawn, 97.5)),
    )

def fit_predict(X: np.ndarray, split: Split) -> np.ndarray:
    model = CatBoostRegressor(**CATBOOST).fit(X[split.dev], split.scores[split.dev])
    return model.predict(X[split.test])

def fit_predict_text(split: Split) -> np.ndarray:
    """The reference arm: the same model, handed the note instead of the columns."""
    from catboost import Pool

    raw = np.array([[note] for note in split.notes], dtype=object)
    model = CatBoostRegressor(**CATBOOST).fit(
        Pool(raw[split.dev], split.scores[split.dev], text_features=[0])
    )
    return model.predict(Pool(raw[split.test], text_features=[0]))

def evaluate(
    features: list[dict], answers_for: dict, split: Split, mode: str
) -> tuple[np.ndarray, float]:
    """Cross-validated error on the dev rows for one candidate question set."""
    X, _ = design(features, answers_for, mode)
    return cross_validate(X[split.dev], split.scores[split.dev])

def swap_in(accepted: list[dict], feature: dict) -> list[dict] | None:
    """The accepted set with `feature` in place of the one it revises, or None if it is gone."""
    at = next(
        (i for i, f in enumerate(accepted) if f["name"] == feature["replaces"]), None
    )
    if at is None:
        return None
    trial = list(accepted)
    trial[at] = {k: feature[k] for k in ("id", "name", "kind", "question")}
    return trial

def try_change(
    trial: list[dict],
    accepted: list[dict],
    cv: float,
    answers_for: dict,
    split: Split,
    mode: str,
    tolerance: float,
) -> tuple[list[dict], float, str, bool]:
    """Refit with the change and keep it only if the dev error improves. No API calls."""
    _, cv_trial = evaluate(trial, answers_for, split, mode)
    if cv_trial <= cv + tolerance:
        return trial, cv_trial, f"CV {cv:.3f} -> {cv_trial:.3f}", True
    return accepted, cv, f"would cost {cv_trial - cv:+.3f}", False

def owner_of(label: str, features: list[dict]) -> dict:
    """Which feature a column label belongs to - encodings suffix the name."""
    exact = next((f for f in features if f["name"] == label), None)
    if exact:
        return exact
    return next(f for f in features if label.startswith(f["name"] + "_"))

def importance_per_feature(
    features: list[dict], labels: list[str], column_importances: np.ndarray
) -> dict:
    """Sum each question's CatBoost column importances.

    Intensity questions can produce multiple model columns. Combining their normalized
    importances gives one percentage share per question.
    """
    total = {f["name"]: 0.0 for f in features}
    for label, column_importance in zip(labels, column_importances):
        total[owner_of(label, features)["name"]] += float(column_importance)
    return total

def feedback_for(
    history: list[float],
    accepted: list[dict],
    answers_for: dict,
    split: Split,
    mode: str,
    out_of_fold: np.ndarray,
    previous: np.ndarray | None,
) -> str:
    """The scoreboard the next proposal call reads. The notes themselves arrive separately,
    through `example_block`. Numbers are rounded before they enter the prompt."""
    X, labels = design(accepted, answers_for, mode)
    dev, scores = split.dev, split.scores
    by_name = importance_per_feature(accepted, labels, importances(X[dev], scores[dev]))

    lines = ["Cross-validated RMSE in points so far, lower is better:"]
    lines += [f"  round {i + 1}: {v:.2f}" for i, v in enumerate(history)]
    if previous is not None:
        now, before = np.abs(scores[dev] - out_of_fold), np.abs(scores[dev] - previous)
        better, worse = int((now < before - 0.1).sum()), int((now > before + 0.1).sum())
        lines.append(
            f"\nAgainst the previous round, {better} of the {len(dev)} dev notes are now "
            f"predicted better by more than 0.1 points and {worse} are predicted worse."
        )
    lines.append(
        "\nYour features, with importance as a percentage of the total and the spread of the "
        "column across the dev rows. Low importance or low spread means the question is not "
        "doing much; revise or drop it."
    )
    for feature in sorted(accepted, key=lambda f: -by_name.get(f["name"], 0.0)):
        column = encode(feature, answers_for[feature["id"]], mode)[0][1]
        lines.append(
            f"  {feature['name']} ({feature['kind']}): "
            f"{by_name.get(feature['name'], 0.0):.1f}% importance, "
            f"spread {column[dev].std():.2f}"
        )
    return "\n".join(lines)

# ----------------------------------------------------------------- the loop itself

class Discovery(NamedTuple):
    """Artifacts returned by the discovery loop."""

    accepted: list[dict]  # the question set it ended with
    answers_for: dict  # feature id -> (rows x levels) probabilities
    snapshots: list[list[dict]]  # the set as it stood at the end of each round
    history: list[float]  # dev CV error after each round
    batches: list[tuple]  # what each round sent, for the request table
    journal: list[tuple]  # every action and what became of it

def run_loop(
    split: Split,
    proposer: str,
    rounds: int,
    examples: int,
    mode: str,
    min_spread: float,
    tolerance: float,
) -> Discovery:
    """Run the propose, answer, fit, and feedback loop."""
    shown = example_rows(split, None, examples)  # round 1 has nothing predicted yet
    out_of_fold = previous = None
    got_from = Discovery([], {}, [], [], [], [])
    accepted, answers_for = got_from.accepted, got_from.answers_for
    snapshots, history = got_from.snapshots, got_from.history
    batches, journal = got_from.batches, got_from.journal
    feedback = ""

    for round_index in range(1, rounds + 1):
        block = example_block(shown, split, out_of_fold, previous)
        actions = propose(
            proposer, round_index, proposal_prompt(block, feedback, accepted)
        )["actions"]
        keep, drops = to_candidates(actions, accepted, round_index)

        if keep:  # one request per row, carrying every question this round proposed
            batches.append((round_index, plain(keep)))
            answers = featurize(split.notes, plain(keep))
            for feature in keep:
                answers_for[feature["id"]] = answers[feature["name"]]

        for (
            feature
        ) in keep:  # an add goes in; importance says later whether it earned it
            if feature["replaces"]:
                continue
            column = encode(feature, answers_for[feature["id"]], mode)[0][1]
            flat = float(column[split.dev].std()) < min_spread
            journal.append(
                (round_index, "flat" if flat else "add", feature["name"], "")
            )
            if not flat:
                accepted.append(
                    {k: feature[k] for k in ("id", "name", "kind", "question")}
                )

        _, cv = evaluate(accepted, answers_for, split, mode)
        trial_args = (answers_for, split, mode, tolerance)

        for feature in [f for f in keep if f["replaces"]]:  # every revision is tried
            trial = swap_in(accepted, feature)
            if trial is None:  # it revises something an earlier round already dropped
                journal.append(
                    (round_index, "stale", feature["name"], "target is gone")
                )
                continue
            accepted[:], cv, note, took = try_change(trial, accepted, cv, *trial_args)
            what = "revise" if took else "reject"
            journal.append(
                (
                    round_index,
                    what,
                    feature["name"],
                    f"was {feature['replaces']}, {note}",
                )
            )

        for name in drops:  # and so is every drop
            trial = [f for f in accepted if f["name"] != name]
            if not trial:
                continue
            accepted[:], cv, note, took = try_change(trial, accepted, cv, *trial_args)
            journal.append((round_index, "drop" if took else "keep", name, note))

        previous, (out_of_fold, cv) = (
            out_of_fold,
            evaluate(accepted, answers_for, split, mode),
        )
        history.append(cv)
        snapshots.append(list(accepted))
        feedback = feedback_for(
            history, accepted, answers_for, split, mode, out_of_fold, previous
        )
        # next round reads the rows these questions get most wrong, and as many they get right
        shown = example_rows(split, out_of_fold, examples)
        report(round_index, keep, drops, journal, accepted, cv)

    return got_from

def report(
    round_index: int,
    keep: list[dict],
    drops: list[str],
    journal: list[tuple],
    accepted: list[dict],
    cv: float,
) -> None:
    """One block per round: the counts, the names it added, then everything with a number."""
    revised = sum(1 for f in keep if f["replaces"])
    print(
        f"round {round_index}: {len(keep) - revised} add, {revised} revise, "
        f"{len(drops)} drop"
    )
    this_round = [j for j in journal if j[0] == round_index]
    added = [name for _, what, name, _ in this_round if what == "add"]
    if added:
        print(
            textwrap.fill(
                ", ".join(added),
                88,
                initial_indent="  added  ",
                subsequent_indent=" " * 10,
            )
        )
    for _, what, name, note in this_round:  # everything carrying a number of its own
        if what != "add":
            print(f"  {what:<7}{name:<34}{note}")
    print(f"  -> {len(accepted)} features, dev CV RMSE {cv:.3f}\n")

# ----------------------------------------------------------------- asking for the score

@json_cache
def ask_score(model: str, note: str) -> dict:
    """One `Score` over ten quality bands, read as a level and rescaled to 80-100."""
    response = client.system_one(
        state=note,
        questions={
            "quality": Score(
                instructions=(
                    "Judging only by what this tasting note says, how good is the wine?"
                ),
                criteria=SCORE_LEVELS,
            )
        },
        model=model,
    )
    got = response.answers["quality"]
    top = len(SCORE_LEVELS) - 1
    expected = sum(k * v for k, v in got.probabilities.items())
    return {
        # level 0 is the bottom of the critic's scale, level 9 the top
        "expected": 80.0 + 20.0 * expected / top,
        "picked": 80.0 + 20.0 * got.score / top,
        "input_tokens": response.usage.input_tokens or 0,
        "output_tokens": response.usage.output_tokens or 0,
    }

# ----------------------------------------------------------------- charts

SURFACE, INK, INK2, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
GRID, AXIS, BLUE, ORANGE = "#e1e0d9", "#c3c2b7", "#2a78d6", "#eb6834"

def style(ax) -> None:
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(AXIS)
    ax.tick_params(colors=MUTED, labelcolor=INK2, labelsize=9)
    ax.set_axisbelow(True)

def polarity(feature: dict, answers_for: dict, split: Split) -> float:
    """Rank correlation between a question's answer and the critic score, on the dev rows.

    Positive means a higher answer goes with a better review, negative the opposite. It is
    what orders the rows of the feature map, so the map reads as a gradient that flips.
    """
    column = encode(feature, answers_for[feature["id"]], "mean")[0][1]
    return spearman(column[split.dev], split.scores[split.dev])

def reviews_heatmap(
    plt,
    questions: list[dict],
    answers_for: dict,
    split: Split,
    rows: tuple,
):
    """Compare held-out reviews across the discovered questions, best-signal first.

    Rows arrive sorted from the questions that rise with the score to the ones that fall with
    it, so a row above the divider shades left to right and a row below it shades right to
    left.
    """

    def value_of(feature: dict, row: int) -> float:
        return float(encode(feature, answers_for[feature["id"]], "mean")[0][1][row])

    signs = [polarity(question, answers_for, split) for question in questions]
    flip = next((i for i, s in enumerate(signs) if s < 0), len(questions))

    raw = np.array(
        [[value_of(question, row) for row in rows] for question in questions]
    )
    normalized = np.array(
        [
            values / (4 if question["kind"] == "intensity" else 1)
            for question, values in zip(questions, raw)
        ]
    )
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        "typesafe_heat", [SURFACE, "#f7c7ad", ORANGE]
    )
    fig, ax = plt.subplots(
        figsize=(9.5, 1.8 + 0.58 * len(questions)), facecolor=SURFACE
    )
    image = ax.imshow(normalized, aspect="auto", cmap=cmap, vmin=0, vmax=1)
    row_labels = []
    for question, sign in zip(questions, signs):
        kind = "score" if question["kind"] == "intensity" else "noul"
        prefix = f"{sign:+.2f} ({kind}) "
        lines = textwrap.wrap(
            " ".join(question["question"].split()),
            width=52,
            max_lines=2,
            placeholder="...",
            break_long_words=False,
            break_on_hyphens=False,
        )
        row_labels.append(prefix + (f"\n{' ' * len(prefix)}").join(lines))
    column_labels = [
        f"#{i}\n{split.scores[row]:.0f} points\n{' '.join(split.notes[row].split())[:15]}..."
        for i, row in enumerate(rows, 1)
    ]
    ax.set_yticks(np.arange(len(questions)), row_labels)
    ax.set_xticks(np.arange(len(rows)), column_labels)
    ax.tick_params(
        axis="x", top=True, labeltop=True, bottom=False, labelbottom=False, pad=8
    )
    ax.tick_params(axis="y", labelsize=8.5)
    for side in ax.spines.values():
        side.set_visible(False)
    ax.set_xticks(np.arange(-0.5, len(rows), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(questions), 1), minor=True)
    ax.grid(which="minor", color=SURFACE, linewidth=2)
    ax.tick_params(which="minor", bottom=False, left=False)
    for i, question in enumerate(questions):
        for j, value in enumerate(raw[i]):
            label = (
                f"{value:.1f}" if question["kind"] == "intensity" else f"{value:.2f}"
            )
            color = SURFACE if normalized[i, j] > 0.58 else INK2
            ax.text(j, i, label, ha="center", va="center", color=color, fontsize=8)
    # the line where the questions stop rising with the score and start falling with it
    if 0 < flip < len(questions):
        ax.axhline(flip - 0.5, color=INK, linewidth=1.2)
        ax.annotate(
            "a higher answer means a worse review, below this line",
            (len(rows) - 0.5, flip - 0.5),
            xytext=(-4, 5),
            textcoords="offset points",
            va="bottom",
            ha="right",
            color=INK2,
            fontsize=8.5,
        )
    colorbar = fig.colorbar(image, ax=ax, fraction=0.025, pad=0.025)
    colorbar.set_ticks([0, 0.5, 1])
    colorbar.set_label("normalized answer", color=INK2, fontsize=8.5)
    colorbar.ax.tick_params(labelsize=8, colors=INK2)
    fig.suptitle(
        "Every question, on five held-out reviews from worst to best",
        x=0.01,
        y=0.995,
        ha="left",
        color=INK,
        fontsize=11,
    )
    fig.text(
        0.01,
        0.972,
        "sorted by how the answer moves with the score, so each row above the line shades "
        "left to right and each row below it shades the other way",
        color=MUTED,
        fontsize=9,
    )
    fig.text(
        0.01,
        0.005,
        "Row labels lead with the rank correlation between that question's answer and the "
        "critic score. Cell text is each question's native scale: score 0-4, noul 0-1.",
        color=MUTED,
        fontsize=8.5,
    )
    return fig

def rounds_chart(
    plt, curve: list[tuple], history: list[float], n_test: int, gain: tuple
):
    """Dev error and held-out error per round. The trend is the point, not the gap."""
    rounds = list(range(1, len(curve) + 1))
    values = [v for _, v in curve]

    fig, ax = plt.subplots(figsize=(7, 3.9), facecolor=SURFACE)
    style(ax)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    # each dev fold trains on four fifths of the rows, so the dev line sits the higher of the two
    ax.fill_between(rounds, history, values, color=GRID, alpha=0.75, linewidth=0)
    ax.plot(
        rounds,
        history,
        marker="o",
        color=BLUE,
        linewidth=2,
        linestyle="--",
        label="dev, cross-validated - what the loop optimises",
    )
    ax.plot(
        rounds,
        values,
        marker="o",
        color=ORANGE,
        linewidth=2,
        label="held out - what that actually buys",
    )
    # label each point on the outside of the pair, so neither line crowds its own numbers
    for x, dev_value, test_value in zip(rounds, history, values):
        for value, other in ((dev_value, test_value), (test_value, dev_value)):
            ax.annotate(
                f"{value:.2f}",
                (x, value),
                textcoords="offset points",
                xytext=(0, 8 if value >= other else -16),
                ha="center",
                color=INK2,
                fontsize=8.5,
            )
    ax.set_xticks(
        rounds, [f"round {x}\n{n} features" for x, (n, _) in zip(rounds, curve)]
    )
    ax.set_ylabel("RMSE in points (lower is better)", color=INK2, fontsize=9)
    # tight around the two lines: the whole finding lives inside 0.15 of a point
    low, high = min(values + history), max(values + history)
    ax.set_ylim(low - 0.10, high + 0.05)
    difference, low_ci, high_ci = gain
    ax.set_title(
        f"{len(rounds)} rounds of the loop, scored on {n_test} held-out reviews",
        loc="left",
        color=INK,
        fontsize=11,
        pad=20,
    )
    # the number the chart is really about: is the held-out move bigger than the noise?
    ax.text(
        0,
        1.015,
        f"round 1 to round {len(rounds)}, held out: {difference:+.3f} points, "
        f"95% CI [{low_ci:+.3f}, {high_ci:+.3f}]",
        transform=ax.transAxes,
        color=MUTED,
        fontsize=9,
    )
    ax.legend(frameon=False, labelcolor=INK2, fontsize=9, loc="lower left")
    return fig
```

## Setup

```bash
pip install anthropic openai catboost numpy matplotlib ipython "typesafe-sdk>=0.5.7" cooksafe --extra-index-url https://pypi.typesafe.ai/
```

then set `TYPESAFE_API_KEY` and `ANTHROPIC_API_KEY`. Every API call is cached to
`json_cache.json`, which ships with the cookbook, so a re-render replays these numbers
without calling anything. Delete it to re-run live. The numbers came from TypeSafe
`jev-1.12` and `claude-sonnet-5` on 2026-08-03. `propose()` has a second branch for
`gpt-5.6-luna`, which was not run.

The first code cell is the whole implementation: API calls, encodings, metrics, chart
style. It is there so this file runs on its own, and the docs site folds it away. Skip it
on a first read - the recipe starts under it.

```python
N_DEV, N_TEST = 1200, 800  # the loop reads dev labels only; test is scored once
ROUNDS = 5  # a round answers questions for all 2,000 rows: 2,000 requests
PROPOSER = "claude-sonnet-5"  # or "gpt-5.6-luna"; the cache holds the Anthropic run
EXAMPLES = 60  # dev notes the proposer reads per round, half of them its worst misses
MIN_SPREAD = 0.05  # a column this flat cannot separate anything, so it is not kept
CHANGE_TOLERANCE = 0.0  # a revision or drop has to improve dev error, not just not hurt
ENCODING = "mean_spread"  # a score answer becomes two columns: its mean and spread

split = load_split(N_DEV, N_TEST, seed=0)
NOTES, SCORES, DEV, TEST = split.notes, split.scores, split.dev, split.test

print(
    f"{len(DEV)} dev rows, {len(TEST)} held out; scores run "
    f"{SCORES.min():.0f}-{SCORES.max():.0f}, mean {SCORES.mean():.2f}, sd {SCORES.std():.2f}"
)
print(f"\none of the notes:\n{NOTES[0]}")
```

```
1200 dev rows, 800 held out; scores run 80-98, mean 88.73, sd 3.17

one of the notes:
A Champagne that is very much wine. The structure and the richness are just right for a food wine, showing ripe acidity, flavors of plums and apricots, and balancing these primary fruits with a dense, complex structure that takes in yeast, maturity and a tight apple skin finish.
```

The loop reads the same 1,200 of the 2,000 rows (the dev rows) over and over, and keeps a
question when it helps predict those 1,200 scores. Scoring on the same rows would mostly
measure how well the loop fitted itself to them, so the other 800 are held out and scored
once, at the end.

## Two question types

A proposed question is one of two kinds, and the kind decides what number comes back.

* **`intensity`** becomes a `Score`, for anything that comes in degrees. Its five
  levels are printed below, and the column is the average level, so a note that sits
  between "moderate" and "strongly" comes out between the two.
* **`presence`** becomes a `Noul`, for a yes/no fact like whether a fault is named.
  The column is that one probability.

## The method

```
questions <- {}
repeat for each round:
    notes  <- round 1 ? 60 dev notes across the score range
                      : the 30 worst-predicted dev notes + the 30 best,
                        each with its score, this prediction and the last
    actions <- LLM(brief, questions, notes, importance and error so far)
    answers[q] <- TypeSafe(note, all new questions of this round) for every row
    for each added q:      keep it unless its column is flat
    for each revised q:    refit; keep the change only if dev error drops
    for each dropped q:    refit; drop it only if dev error drops
    out_of_fold <- k-fold CatBoost on the columns   # judges, and picks next round's notes
```

No question is filtered out before it is answered. All of a round's questions go out in the
same request, so one more question costs no extra request. A question that applies to one
row in ten will look useless in the 60 notes the proposer reads, and still be the most
useful column in the set.

k-fold means splitting the dev rows into k parts and predicting each part with a model
trained on the other parts. Those predictions do three jobs: they judge every revision and
drop, they pick the notes the next round reads, and they tell the proposer which of its
questions helped, by how far they have moved since the round before.

```python
print("every intensity question is graded on these five levels:\n")
for i, level in enumerate(INTENSITY_LEVELS):
    print(f"  {i}. {level}")
print("\nevery presence question is judged true or false against these:\n")
print(f"  true:  {PRESENCE_CRITERIA['true']}")
print(f"  false: {PRESENCE_CRITERIA['false']}")
print("\nthe brief the proposer works from:\n")
print("\n".join(PROPOSER_TASK.splitlines()[:6]) + "\n  ...")
```

```
every intensity question is graded on these five levels:

  0. Not present in this note at all
  1. Barely present - mentioned once, in passing
  2. Present at a moderate level
  3. Present strongly - the note dwells on it
  4. Dominant - the note is largely about this

every presence question is judged true or false against these:

  true:  The note states this or clearly implies it
  false: The note gives no indication of this

the brief the proposer works from:

You are designing numeric features for a gradient-boosting model that
predicts the score a wine critic gave (an integer from 80 to 100) from the tasting note alone.
The model sees nothing but the features you design.

Return up to 18 actions. Each action is one of:

  ...
```

## The autoresearch loop

`run_loop` runs all five rounds and prints a block per round. An added question goes
straight in: its answers have already been fetched, and its importance will show later
whether it was worth asking. A revision or a drop takes away a column the model is already
using, so each one is tried first: refit with the change, and keep it only if the dev
error goes down. A refit costs no API calls, so trying a change and rejecting it is free.

```python
run = run_loop(
    split, PROPOSER, ROUNDS, EXAMPLES, ENCODING, MIN_SPREAD, CHANGE_TOLERANCE
)
accepted, answers_for = run.accepted, run.answers_for
snapshots, history = run.snapshots, run.history
```

```text
round 1: 18 add, 0 revise, 0 drop
  added  complexity, fruit_intensity, tannin_structure, acidity_intensity,
          oak_intensity, finish_length, balance_harmony, aging_potential,
          positive_superlative_language, negative_critical_language,
          drinkability_easiness, body_richness, sweetness_level, texture_descriptors,
          earthy_savory_notes, flaw_or_defect_mentioned,
          single_vineyard_or_prestige_signal, varietal_blend_detail
  -> 18 features, dev CV RMSE 1.903

round 2: 5 add, 3 revise, 3 drop
  added  power_concentration_language, flavor_distinctiveness, generic_fruit_language,
          candied_artificial_flavor, rustic_authentic_character
  reject oak_dominance                     was oak_intensity, would cost +0.005
  revise negative_critical_language        was negative_critical_language, CV 1.897 -> 1.894
  revise single_vineyard_or_prestige_signalwas single_vineyard_or_prestige_signal, CV 1.894 -> 1.881
  keep   finish_length                     would cost +0.009
  keep   texture_descriptors               would cost +0.001
  keep   varietal_blend_detail             would cost +0.023
  -> 23 features, dev CV RMSE 1.881

round 3: 7 add, 2 revise, 1 drop
  added  elegance_finesse_language, minerality_precision_language,
          hedged_qualified_praise, underripe_green_character,
          reviewer_overall_verdict_strength, unusual_or_funky_descriptor_valence,
          botrytis_or_special_winemaking_signal
  revise negative_critical_language        was negative_critical_language, CV 1.868 -> 1.864
  revise finish_quality                    was finish_length, CV 1.864 -> 1.861
  keep   candied_artificial_flavor         would cost +0.014
  -> 30 features, dev CV RMSE 1.861

round 4: 5 add, 2 revise, 3 drop
  added  excess_or_imbalance_signal, descriptive_detail_density,
          critic_enthusiasm_confidence, savory_food_wine_seriousness,
          note_overall_tone_positivity
  revise rustic_authentic_character        was rustic_authentic_character, CV 1.843 -> 1.838
  reject hedged_qualified_praise           was hedged_qualified_praise, would cost +0.014
  keep   botrytis_or_special_winemaking_signalwould cost +0.011
  keep   candied_artificial_flavor         would cost +0.009
  keep   unusual_or_funky_descriptor_valencewould cost +0.010
  -> 35 features, dev CV RMSE 1.838

round 5: 4 add, 2 revise, 8 drop
  added  structural_seriousness, youthful_tension_signal, surface_prettiness_vs_depth,
          price_value_signal
  reject unconventional_character_as_virtuewas rustic_authentic_character, would cost +0.010
  revise flavor_distinctiveness            was flavor_distinctiveness, CV 1.849 -> 1.843
  keep   candied_artificial_flavor         would cost +0.002
  keep   botrytis_or_special_winemaking_signalwould cost +0.003
  keep   hedged_qualified_praise           would cost +0.006
  keep   excess_or_imbalance_signal        would cost +0.005
  drop   underripe_green_character         CV 1.843 -> 1.840
  keep   unusual_or_funky_descriptor_valencewould cost +0.002
  keep   texture_descriptors               would cost +0.001
  keep   generic_fruit_language            would cost +0.000
  -> 38 features, dev CV RMSE 1.840
```

## Pointing it at your own data

`PROPOSER_TASK` is the only string that mentions wine, and `featurize()` takes any list of
strings. Editing that brief changes the proposal prompt, and the prompt is part of the
cache key, so the next run calls the API again for every round.

The request count grows with rows, not with questions: one request per row per round, so
100,000 rows is 100,000 requests a round. A revision counts as a new question, so it costs
another pass over every row. Raise the worker pool slowly. Eight is already enough to hit
a rate limit on a shared key.

## What the questions see

Five held-out reviews, one at each quarter of the score range, against fifteen of the 38
questions: the top eight score questions by importance, plus the top seven nouls.

Those fifteen rows are then sorted by which way the answer moves with the critic score.
Questions whose answer rises with the score come first, questions whose answer falls with
it come after the divider. So going left to right, from the worst review to the best, the
answers above the divider should climb and the answers below it should drop off.

```python
X, labels = design(accepted, answers_for, ENCODING)
column_importances = importances(X[DEV], SCORES[DEV])
# an encoding gives a feature more than one column, so add a feature's columns back up
feature_importances = importance_per_feature(accepted, labels, column_importances)
ranked = sorted(accepted, key=lambda f: -feature_importances[f["name"]])
score_questions = [f for f in ranked if f["kind"] == "intensity"][:8]
noul_questions = [f for f in ranked if f["kind"] == "presence"][:7]
# ordered by which way the answer moves with the score, so the map flips halfway down
heatmap_questions = sorted(
    score_questions + noul_questions,
    key=lambda f: -polarity(f, answers_for, split),
)
ordered_test = TEST[np.argsort(SCORES[TEST], kind="stable")]
positions = np.linspace(0, len(ordered_test) - 1, 5).round().astype(int)
review_rows = tuple(ordered_test[positions])

print("the five held-out heatmap columns:\n")
for i, row in enumerate(review_rows, 1):
    excerpt = " ".join(NOTES[row].split())
    print(f"  {i}. {SCORES[row]:.0f} points: {excerpt[:100]}...")

fig = reviews_heatmap(plt, heatmap_questions, answers_for, split, review_rows)
display(fig)
plt.close(fig)
```

```
the five held-out heatmap columns:

  1. 80 points: Raw cherry and plum aromas are resiny and suggest wet cement. This is shearing and so jacked up with...
  2. 86 points: A slight spritz brightens the mouthfeel of this lemony wine. Aromas are a bit musky, but flavors of ...
  3. 89 points: This is a European-style Syrah, cofermented with 2% Viognier. It's soft and round, medium in body, a...
  4. 91 points: From the producer's dry-farmed estate vineyard, and supported by small amounts of Merlot and Caberne...
  5. 97 points: A thoroughly elegant, serious and yet immensely enjoyable wine that stays lively many days after ope...
```

<img src="https://mintcdn.com/ts-docs/2NirYCl-v96cw05F/cookbooks/autoresearch_feature_discovery/autoresearch_feature_discovery.executed.1.png?fit=max&auto=format&n=2NirYCl-v96cw05F&q=85&s=9a9c9e88ad39b5cc6ae00db22d38b9d5" alt="output" width="1882" height="1593" data-path="cookbooks/autoresearch_feature_discovery/autoresearch_feature_discovery.executed.1.png" />

The table from the top of the page, computed. All five arms are scored once on the same 800
held-out rows, and the first three skip feature discovery. One predicts the mean of the dev
scores and reads nothing from the note at all. One hands the note to the same CatBoost
through its `text_features` handling, which turns it into word counts. One asks TypeSafe
for the score itself.

That third one is a single `Score` per row over ten quality bands, from "faulty or
unpleasant" up to "profound". Ten because ten levels is the most a `Score` question
takes -
eleven comes back as a server error. Level 0 maps to 80 points and level 9 to 100.
Spreading the bands over the scale that way is not enough on its own, because nothing in
the question says where this publication's scores actually sit on it. So every answer is
then moved by a single offset, measured on the dev scores. That offset is printed in the
row label, and it is the only thing this shortcut learns from the scores.

Spearman is rank correlation, where 1.0 would put the held-out wines in exactly the
critic's order. The word-count row is CatBoost's own text handling, not a tuned
text-regression pipeline. All of this is one dataset and one run of the loop.

```python
predicted = fit_predict(X, split)
text_predicted = fit_predict_text(split)

# ask TypeSafe for the score itself, one request per row
with ThreadPoolExecutor(max_workers=8) as pool:
    direct = list(pool.map(lambda note: ask_score(TYPESAFE_MODEL, note), NOTES))
asked = np.array([d["expected"] for d in direct])
shift = float(SCORES[DEV].mean() - asked[DEV].mean())  # one number, from the dev labels

# what one proposal call gets you, before any feedback: the set round 1 ended with
first_round, _ = design(snapshots[0], answers_for, ENCODING)

print(f"{'arm':<46}{'RMSE':>7}{'spearman':>10}")
for label, p in (
    ("predict the mean of the dev rows", np.full(len(TEST), SCORES[DEV].mean())),
    ("the note as word counts, same CatBoost", text_predicted),
    (f"ask for the score itself, shifted {shift:+.2f}", asked[TEST] + shift),
    (
        f"{len(snapshots[0])} questions from round 1, no loop",
        fit_predict(first_round, split),
    ),
    (f"{len(accepted)} questions after all {ROUNDS} rounds", predicted),
):
    print(f"{label:<46}{rmse(SCORES[TEST], p):>7.3f}{spearman(SCORES[TEST], p):>10.3f}")
```

```
arm                                              RMSE  spearman
predict the mean of the dev rows                3.088    -0.014
the note as word counts, same CatBoost          2.466     0.605
ask for the score itself, shifted -1.71         2.145     0.761
18 questions from round 1, no loop              1.869     0.778
38 questions after all 5 rounds                 1.772     0.799
```

## Did the autoresearch rounds help?

Both lines plot the error of the question set at the end of each round, starting from
the first proposal. The dashed line is the cross-validated dev error, the number every
accept and reject decision is made on. The solid line scores the same question set on
the held-out rows, which the loop never reads. Each point is the set as it stood when
the round closed, so a round that only revised or dropped a question still moves both
lines. The feature map says what the questions measure; the error is what tells you
whether the rounds after the first proposal made the predictions any better.

The axis is tight: everything on it happens inside a fifth of a point, and every shortcut
from the table above sits far off the top of it. The dev line runs above the held-out line
the whole way, and that is a training-size effect. Each dev fold trains on four fifths of
the dev rows, while the held-out number comes from a model that got all 1,200. The two
lines move together, so the dev number the loop steers by tracks the held-out number it
never sees. The interval under the title comes from resampling the held-out rows, so it
says whether the move from round 1 to round 5 is bigger than the noise in 800 rows.

```python
curve, per_round = [], []
for features in snapshots:
    X_round, _ = design(features, answers_for, ENCODING)
    per_round.append(fit_predict(X_round, split))
    curve.append((len(features), rmse(SCORES[TEST], per_round[-1])))

# the same held-out rows resampled 2,000 times, both arms scored on each resample
gain = paired_gain(SCORES[TEST], per_round[0], per_round[-1])
print(
    f"round 1 -> round {ROUNDS} on the held-out rows: {gain[0]:+.3f} points, "
    f"95% CI [{gain[1]:+.3f}, {gain[2]:+.3f}]"
)

fig = rounds_chart(plt, curve, history, len(TEST), gain)
display(fig)
plt.close(fig)
```

```
round 1 -> round 5 on the held-out rows: -0.097 points, 95% CI [-0.147, -0.050]
```

<img src="https://mintcdn.com/ts-docs/2NirYCl-v96cw05F/cookbooks/autoresearch_feature_discovery/autoresearch_feature_discovery.executed.2.png?fit=max&auto=format&n=2NirYCl-v96cw05F&q=85&s=8e122e0435a22f9f18f4a3d780f06e69" alt="output" width="945" height="599" data-path="cookbooks/autoresearch_feature_discovery/autoresearch_feature_discovery.executed.2.png" />

The held-out line falls further than the dev line does. Round 1 wrote its questions with no
feedback to work from, and the four rounds after it are worth 0.10 points on the held-out
rows, 95% CI \[-0.147, -0.050].

Round 5 proposed four adds, two rewordings and eight drops, and gave the first dev number
that did not improve. There is only so much to ask about a 245-character note, and by round
5 the proposals had tipped from adding questions to dropping them.

```python
kinds = {f["name"]: f["kind"] for f in accepted}
print("feature importance share: % of total CatBoost importance across all questions")
print(f"{'feature':<38}{'asked as':<10}{'importance share':>16}")
for name, importance_share in sorted(feature_importances.items(), key=lambda p: -p[1])[
    :12
]:
    kind = "score" if kinds[name] == "intensity" else "noul"
    print(
        f"{name[:36]:<38}{kind:<10}{importance_share:>8.1f}%  "
        f"{'#' * round(importance_share)}"
    )
counts = f"{sum(1 for k in kinds.values() if k == 'intensity')} score"
counts += f", {sum(1 for k in kinds.values() if k == 'presence')} noul"
print(f"\nthe {len(accepted)} questions the loop kept: {counts}")
top = max(feature_importances, key=feature_importances.get)
print(
    f'the question behind the top row:\n  {top}: "{owner_of(top, accepted)["question"]}"'
)
```

```
feature importance share: % of total CatBoost importance across all questions
feature                               asked as  importance share
note_overall_tone_positivity          score         17.4%  #################
savory_food_wine_seriousness          score          8.7%  #########
positive_superlative_language         score          8.4%  ########
single_vineyard_or_prestige_signal    noul           7.2%  #######
descriptive_detail_density            score          5.7%  ######
elegance_finesse_language             score          5.0%  #####
complexity                            score          5.0%  #####
aging_potential                       score          5.0%  #####
balance_harmony                       score          2.9%  ###
drinkability_easiness                 score          2.9%  ###
critic_enthusiasm_confidence          score          2.7%  ###
flavor_distinctiveness                score          2.6%  ###

the 38 questions the loop kept: 29 score, 9 noul
the question behind the top row:
  note_overall_tone_positivity: "Setting aside specific descriptors, how positive is the overall emotional tone and word choice of the note taken as a whole (warm, admiring language throughout vs. flat, neutral, or lukewarm phrasing)?"
```

`importance share` is CatBoost feature importance, normalized so all 38 questions sum to
100%. It is not a share of rows, of questions, or of prediction accuracy. A score question
owns two columns, a mean and a spread, so its two column importances are added back
together before the percentage is printed. `note_overall_tone_positivity` accounts for
17.4% of the total. The fourth row is a noul: whether the note names a single vineyard or
some other prestige signal is a yes/no fact, so it was asked as one.

## Next steps

This run keeps the loop small. Direct extensions:

* Screen a candidate before paying to answer it. Treat the proposed question itself as the
  state and ask nouls about it: can it be answered from the source text, does it mean
  one thing under its criteria, does it apply to most rows, will it vary across rows. Send
  only the questions that clear all four with enough confidence.
* Prune correlated features. Measure correlation between encoded columns on the dev rows,
  cluster the near-duplicates, and keep the clearest or most important question from each
  cluster.
* Add simple baselines. Compare TF-IDF, character counts, and other structural features on
  their own, then append them to the discovered columns to measure what each contributes.
* Mix proposer families. Generate candidate batches with Anthropic, OpenAI, Google Gemini,
  and open-source models, then merge and deduplicate them before any of them reach
  TypeSafe. Different families should widen the search more than repeated calls to one
  proposer.
* Compare predictive models and methods. Try linear or elastic-net regression, a support
  vector regressor, random forests, and recalibration where the downstream output is
  probabilistic. Check whether the discovered features help outside CatBoost.
* Add an embedding baseline. An embedding turns a note into a few hundred numbers with no
  question attached: `sentence-transformers/all-MiniLM-L6-v2` runs locally, OpenAI's
  `text-embedding-3-small` is a hosted call. Append one to the discovered columns and
  measure whether it carries anything they do not.
* Match validation to deployment. Use chronological splits when predicting the future,
  grouped splits when related rows must stay together, and keep a final test set untouched
  by both feature discovery and model selection.
* Stop on a plateau. End the loop when cross-validated RMSE stops improving for a fixed
  number of rounds, or when it reaches a question or request budget.
* Run a longer search in an agent's Goal mode. Give it an explicit metric, budget, and
  stopping rule, then let it propose, evaluate, and refine more rounds.
* Check stability. Repeat discovery across seeds or data slices and keep the questions that
  stay useful, rather than the ones whose importance rests on one split.

## Open it in the playground

This share link holds one tasting note plus every question the loop ended up with.

```python
playground_link = make_playground_link(
    NOTES[0], feature_questions(accepted), models=[TYPESAFE_MODEL]
)
display(
    Markdown(
        f"🔗 [Open the note + questions in the TypeSafe playground]({playground_link})"
    )
)
```

[Open the note + questions in the TypeSafe playground →](https://console.typesafe.ai/playground#share/N4IgJg9gxgrgtgUwHYBcAqCAeKQC4AEIAgvgMIAWAhnAA6UDmSC+KVK+AlgM74BuCAJwCe+ODCjl8Adw5MAdPjTlmXFAPEoYA5pSRgWy-AI4SmXHpW34AVjFVGO9cuwBmEAfkr43EfTKYANPhc5BD+9A40OlAcYBwoQkEuADaUvO48EC74NMnwFnqeNMZQEChcQbr6AEaUqUgxSBGsCFzMxRxwliIu6vE8Mqye+GDIbUGltMlYwWoaWsyslOwolADWrZxI+EIIlKpBXZrGCZ6FXiiOzkW5Kmuy3rLc5HIgQSDFELTlGNh4hMAADogSa3TDxITAghAkAJKJQ-DArilbTAoLAqAnQQcSgIgDawIAcmUcto2qgtgZuPgkGUdOw6sk0YiQAAhSwIZIiYqtZDsAC0oj5HAgTH0oqgCCCDzo5lk9GZwIACmS+Z4GaJfIJlsxpvwmW8WSreRTVAJRfQufhBS0aXSRlJOclMtt4oqQAARL6yXQCgzMWkoZjU1ICeickSUaoQGArcjcYEAXXRIFkZo0IqQXARwIAEmFZuamlbIJtbYHmAhaFQuBwAF6LQz+BAAch4oOm4ISQVSu20+hSaQyQXcohgyUutxG3EuDQZ5q6XAA9IP0gIBu57k0WBBwy0BAB+YEAXxTvRg8QA+rIg1mIQiYXCEDmQMj3M-DRiscZcf8CSBiXYHlyXYB5WGpCt1U8ZIDRTdltCtYC1UFRBUEzBBxQaKVKVlWsmndY0QKgrw4C1AQdXwPVOQI1VTTUC0rRtQxILAR0YJdTgUHdL04B9CkmIDe0Q0scMrSjGM4wTEBkxZNM5igS5RWzf48wLM0GMjQpeA4bSwBLCAy2Y+1RmRYxqmYc94nwCRLEoBTBHwAAKBA5HoOQgmMKIzAqYIohiFwTG8Pp2BMzEOBoFBhwcUxWkybJLNcVI1wASiPEBTxZVYkCQWRL3TBSFgfYEnxfN9UU-EFvxxfEiRJJCKTA+MeEg5ZoNgll4IjUkTT9VDFLFfAJWwmV9jwhUKsItVWpIsiKKo9rlVo9h1OLEQBLtIMHSdDi3Qqni+L9cshJ4UNRMjaNYypZSZOBOT1AUzNlIIVSpELDSRgMngjs2uJkTsL7dBy7Z8uOZhRwgfhyJgwt5ihx4BDgbyl1qKA1mjJg0oy4E7NiCFr1QMZ73+R8hHhFTXxRD8UzCoMfxqgC6qWylwOa+1ppg91OsQpmUOFUUMMGrDpW2XD5RonriM1UZyM2+bxaIlbLTW-0NuYVjtsFzjuO9JBfWtFXIOEsMuvEy6WaTFM7ozJSX3zV7Ff0wzBJ+7hYHMTwYjibtrOMLgaG8kcPFWAQUG8zGUwgdZ8dvWsEiK2FSY-Z6Kffd0aexX8CH-QDuqIxqILZhkOYqrnuR5oU0P5zDJWFnJRrFiamemqXtVlhB9XltUHeV761bY51Nd2lN9t1-iDeOyiRJNi7JOuy2s3k-qnpZO23tWj6ndViv+sG9YgikCBfE8eh5SCWoBAQoJIv2FBA74XQOBgyglz9kxnbLUmTEZHoF13tZw5ZAFHKIRLwAEcYB1CJtCYqidSqUzTlVTO+Bs6MwlvnVmm12YLTZBybmEteaVwGkNWuot8KNwls3Ui0s5rt2ouQhW9F17rRYv3HaXE9o6z1swiep1p4SSuhbWSC97pL1tmpRhSsN5fSMptYolBuCNmYOAyBpwsgqyAc8TibRkguCCIGGwdhQLlEosgegQxnKuXcvgFsyR5SCB4OZSgsYOAuHHFyFsQQWyWliK0Dx1jShYVQDLAWGiQh+JsRaDyCAgEhKeGE5KfB7F2HwCfbS25bShMkLSDaUZpg5AgLHHSixtDLD6gA4EtR6iSkvFQBGopITExgWTZOZUqYsnTnTP8tUgJM3QVvLBnNcFl3wdvdC1dhoi3rmQlMk0KSUNmm3Du9Cu4SMYuPH6rDB7sOHpwsevdOAnSnmJGeAjpLzxBo9MR9tVkiFLNI9+pJ5FtBVs2Ns+BKm6BrvgWppEkCJEGh4G8CB6Ay0zINbI-RrJfBoPzVAXBykgAYPKS8MLbyXDqPHEq5NWkIPiBnemOd6qgW2CzfpRdsGl1zshUZVdBZfJGnKaZRom4aioa3XUtDsGzOWjc-W+z1bsS2drXio9DoyODIc42xz+HmzOUIi5Ntyar27lI9ZKgYD0HDPYUlzZvn7GPvKfJaKcTJABdIR+prOifH4EuUY+oIA0G8Fofc5qhiXEQMzQwkon6HhPCmGFhT+B5RgFEAQqRLhBvqPQCB4ZMWwOxfAiqHTqpdIZj0tBJKmpkraoMhCwyiIEP6gLYhOEpnjRmSy4YbLgkmKWRWiWKruEbI1qKLWHCRVcLVQcyeUrzoyqaoI26wjrZZiuWvSRdyu12HVaG8NRSzXxicIhAp8R53tzqBAiNupdDRoYMwCxblPH0HcOGGMXBwnUEoHWeU4SQV7GWuISU5hwltGoNMZ9njHHONcckFsCTIqPIUS82QYNIaMgRUwegywimXhpl-ZIl4o0xqTvgEmzSWQ4qTYgglqC86ZoLpg8luaupEv1n1MZdKJl10ZeW5lFDWULI5XWujDCiySKbX3FtrptkshHp2-ZRszqeBObKm6qZh0PUVcnZVvLJ29zeRDbU0NIpMGCBqrV7BwxIAvKp36lAaAwpvH1M1XhIZxAUgYVqtpdUuEZDwEI7h2AHqsS2R06xWgoHCXp1Qghwn6J-VaAJaTGj0D-ZUTIBmCkCwA14MaeTeLJH0FANI96aUDQZWNV18Zti6EGvuGQzyA2rv4EYduHAEBSARWAYwSA1hRkfnjPYeFYpxvQ0iRN1NsOpsJb0-DGD6Q5pLkMqlY9yO0pLRlhu9aiLzOoYsuh02VlsbWfyzZrah68d2WKh5gm+FmwHXKodCrR1KvEct25n0u29GoIo81qn9VNaEPyarsgtz0CCLWKY2EYANGhbY5LQYwB3xKWAEQAGXu1btK9QYoRLquJDsoDwdrOQOrKX6lk0ZQeXhKOQbyrWUPtdTlhvFnSs7dJG8Sq62bGTEbwQWtLxahalpo53OZDG5tMYWyxpb70ONbUFetnjwI+N7PFd23h0r9tSTE1bSTJ3pNnfenJsXoUzK3deQ43w-zHRXFvtFXHsU74BMlEE6DrbnOeIC-yTH5WwDhJx15sYrZPHG75MEu3qV0dIkdAgUOsVEOcvx3AonnWScprJ2minnqCMDZp0NvNUfC0UYm5Mlnyy2dVsY7Wrni0G28r5wKgegvhUHT5WL3bkvZ6DvE8d5eL1x2O3uVvVXHBzLBB93792o4uAau6NZWpdlaaeuYM2BFQZsALEvC3iKGQg8JpD+0rrEeesZqpy1Ij8eSPlzG0Qpnk2mW55m+z9l2euVM0bV2wvbCS+irLztyVQnTZV8OzXxelzTvXPO6q-lrQwpt9WA9HkuPqDGaqRLGOQC4AgJyE5C5IetYlwKRGUOQOEvqPwAkC+o-GsEIOEpiHsHANgZ4jClINLNgZ7ulCmHsAjkIHlEOMIJeBWMvGhgTinOVKHrTOHsguTqRn0uvoNnBMNqRknuNnvqnmNKzgyMfjWnLOnjyl-gXmttxjfvxuXg-nts-jLhJqIh-g3hdpvCxL-mrvgJQawP8lwLQf8qOLSEgPyAlP3rZPZB4D3hIJ4CdPeojlfBACjKUEED9tLNUOoCEIcCBlDHfIjtUKrPCl7iAIOFIJeO4FPtEggApJeDvhhHPsnLSOOO6LLlocnF6HofaDvsMDEWaqMJARZo1CPiBh9uIJIPquZIav2OIBhEkD9lgYcLGC0XquuOQB9jGAIHfEgYIAVmDC4C4PyDQLGLOPQGlGwfio0rCOoMwUoA8qoDqNItSKOFANMJYFaFarYpsBtsCLZs6MsWLqkpsNkrIOZmbtsGorKseFjK+PKNMJeGkggEIJYGAHEQICimSJcOGHlI4LrAaNAgnG1iAJkdgjke-nkZdvsrWIwHUL5EkSarnACWDB4FEHEHeo2OaBqpIEUWorFn5C4oFO8Z8QIEDkYWsZtNoJMasP1D2J0HivoJ8GACOiOIlnwCBj5LZmAQMCBl0BsAMWaoGLkswORCcEIEuHZNsfInALMYvmHkgo+EsS+CsVvLSYZJsR4NsZQXsVMOVjwEcdEXUG0BqecUUqzFsDcTvPcQdo8SmLwJYOVqsAhtUNMHoAkasI-OkSyFCdkZobCZtgUZtH7KiS4GDoYCCvpswC6cYL7iIKOJ6cgGyYICbqsFqpSKML6ckEqV+CqZiuqeTJqZBNqRsZkHqTsWGiIPscaW2meOaWcQ8hcTadcV-PadkA8U8UQYILBkNKbv1Ihjushv6YTqwcqewUgigumnhmvoXHwR1AIdvnzLvvSqIVNtzhnjNBzqfuIToXfs3goY2Zth2qLvfj2o-iJgdhobXmOiqsrg8tOpPE0MhuCiMITN7H2aKa7kOZmHfECneKcBbtYqMFmM7tYuQBqpBS2H+WoDqHbp4mme+uep4m0FWC8SIChbFOEtUI4H+juJ+aZK3uriBgpmBtDFaoPgiquPEb9LOA9PwHjgsVii0h1lOfMcvrhmqDwYuXHvwQnoIQzuMiQmWgebNiftIYtnRHIZfieaaSLttlvBXn2lLnPPKm-lJivAWD9nYBAskEEFgGUCYHfBGf5IFNSLaIplDKanRQILKQuKZtAFGOOH3tOvoHxZtKBUQF0OaGfGUMIJcD5LGTQPGEGB9pQGMUWEEKijCloMYAkqCByPoDFlvHmoaq2pML8kZZDEIGAJQD-BeCgEuJHGsMRWFDPuuPrDWgAAycDZDCgJ5abYhQBBAAAsDVKs6QyW1QblwgWinIEK9magHAb2Zw+gelPeyJrA+JTgEkCKLVJQl4CUI5b5e645kJMY0JwZ2lwu8JYuCeXQsgVoraS1plUKcAvyuQdkFkwUFVnkkU1VjktiGw-eggwgZ8H1-yuQ8AlQBm0wCSMO-CugtyM4sgTFmJ+AU1Bldh5EDhERBZlURZrFJZycZZ9oFZVOWxNZhpuQDZppJxFppZVp-A7ZegnZYKDpUkTp7SVQtul4lglwAUMQdQK1SU7gm1gZFUMJe1noB1DyLebeyWFNXRTNZJrNhlwQQgqAyglwbVZqXAvglA-Ir1FkHNz1sBViAAyh0BFdZLoOqlBqKbZjAJgEFMVRMFUEIAkj3pqh5oal4KkKjB+brMcMiaOE4i0GhFAHDYPoIEjcmqqcVGjSyBjeGYyTqVWdZLjXWUaYcULmaacZaa2daXaLaZTa2tTcpLTcCAEfLYzeAcKFALBgPg4ZtZhnMaTpwZHtwX1tTsXIJVviMqkaJczmITIZLNWjQsxofjzkwvJVxqefteecpYbKoZXqcneVpfLjpZ-krgLVvNdh6vnRda4rVv8ufH8l8YMYlvyAfL4EuK5o-Hbn7Qjfql4AxRDVupUEXT7TySHDAKMcBqpo5DLIjpZjlhYN4KkK9EsMSnMCZKUb7vDeUMlFEsbXpLFB+VIHLR-f-WfUPtSOaRAD7KujEA2PoJyG0LA4IMGJmu-AipyMCp8ggCtbyW0GtburGqxfGuxQvoWdOThnObxfXbwQJcuUJauYQozhudRh3TJRIZnnudJdubIbzoPQLooe2qXnzqpcJv2tLucjPXXiADJl-k+VvC+Uhnuh+cQ1BkzjEuYNhNoDEn1FEmaPIqgLFRALYoEWajyDELWOblrchdMAY55p4qYyBkhdYjCnY8oL4y2P8eRDeBgckFgd1E45mIRQBjZKA9iA2C-QgAiiKkpnjI49wJmFQ2ObQxCZXZxdXbOVHl5bHo3Zw83fTq3ZRmJWnoI13VnqI33bJRI6tkPYpVtkeePVeWoVPcoyIiGfXo+YvZBFWGFfsPWMwGk1DBCB9iphQ3fE7SBpYCuNAB5bFdoE4yoE7h+SDAsDAZYp4tM3UM9sYMxS+ghbrpRORZ4rYkwJYOEgCc4FaG4G7BhGFtOKoNfUFF8EYUzeQMmR4FvZSUlmXbTAioE+GN8corYgFBhH8U8ihkwS+Nzf0yOqo-kU3pBHQBwFiaE88g6VUapjDmcEYZgPjTEOwDCy4kIIaslvwK1KBS2H1Z41BWELQgII87Dk4OErsJ5v+mwCwGM-YmarYrxMYrlkMQICMfkoGjoMY+YGjsTkw6jU-SnVqZHZWWavqbsXHfjQne6ETS2VvG2enR2QDlTd2Y6U8doNpBVv2TZYyG8YIOZigHlGoKYqwBXRxYw1xTXSvvOaSuw+U8CJSsJdUynvw1uc00I7uVJYHp3Rfm01I8PfzaPV0zwkcmpeoWi3Lqo+owvWGZWOS2SAUGSxS-EBMKKAFOBewI69DGZiYAyDeUS62DwNSyBa49YlgJKBFJmHUBeqSJ0MW9QFOFkBc-zPyKUNybuuRATLBfzB+baOZKoIRe-Q5EsMDPsbcgYa3oauSErQNcsKNSy5sMDZdLFvAH5SILYGAPQEq08TDWzfEevVgQkSRVVW8XUMgJKN6ww8jSq9xSww1Gw-xSGzglwy3Wubw1RqQrRjGw0yIwm-U0myrgpYnUpRm5tPI0-n05pQM3zQAOrKAENaNtA8BPtS2vsWFAuWDb1Un8hPgPXhRPU8CgXAs73fIZAID8hrGpmtG1ZBCsjaAoAoDgNcfz3ryTpWTL2NjUjxP+0eAX2yvFbYRX1vnPCGqXN1tWuttGDLDwNUBf3FG-2K1fC+7ZbNCCuQAdpBgFD6C5mgORHkEY6BVCDBU-F5Skls3NjCnIqIkglc3bVBn3nkyYtdpFEkmonIm+frBadJG44cDgJQ0BJexgqjTQA4iA5ZbfJXD4AdumG1EuHvJufBU9gUS1Jk167nwITeCCB9S3FGXYBpkCzTCbBIpNB3yUeJLGOmodcRCgWTENDKCihVsNAicIBkFV0cFqlqsk2rGavY3VkGl6sHEmmJ1GvquQSmtXEU0WtZ1Ws01PE9v+7xGdAfJYRAlImgmoZNLMGov4fosvjhcInqYebJPdo2WQCBDfJ7C8BPZGejDUmjg-YXeSieXAzmdGHTDGagUndyglZlVLjXwHDQSlChCmrKDLBXyAwPA2XJCRzUnbEQC0vbhcAd4BxQVWRCAxjD7eC3XhI3jqAmSPNQG0wcTE+k+ha21FcINeCgiwp1uQy4PJBwA8DrtBxGdbBBixl2c5fWYgaB1L63eLFzfo1i5Y2ko40recDx3reGvNlbf2g7eoPmu3FLvWspjT5bo+nyIIbgWxwNJglsUYY+sAd+vFN10LmEZLmhsrlQc8Nt377wcgDcqIfxu92h-n756SNF7SM7LptyMT3Zt4dHYqNjpdB-KfOMV67mUS2eBOUrga0vyLxaDInW8ZDf5i50Au0PCORO2RKTx9gCwA51C7i7Okks1cAJL6oOoBrRaoO2D2CLujgoAHwpLICtXMdVU+TaCQOoUwNwMbuGC0xi8F-tArpbpikkNboIpwYl18jQW1j7BwADlIA1s-tIt3fB6Tm+tFNcG9be9lMUr+9VPQdB+bkH5R-0bCMR857f+sZWmaHdphh06ZJ8emk9UTLm1yJz0xwzhTRpBBBzFdcsYzNgBdQCQX8KQWAUNOwDTLcdjMhLO7G20GiUVTUBXJyIrE-LylQUJWORAoiCCjBomJWRtgpB74RZ++qVVBl4EHB65JiCea3vOlHCQtHaUAUoD9hQAIozCa4agj4G+LNg8o2IM9CxWd50NXe-7IOswxKagcfeHDP3pBzf6B8am7daNgAKmiSEe6--MPqh0FroclCF5FSsnwUbqVq8vNWekM1kwjN7QsnD7vqjaDGAz0SQQ+GAH3qOYAWZlUvrZREAtgrUjmX0C2AOZwFqsphCIV0T6qPxXAo-FfhKTPgXgJwRFXRiS1jLaRVg3ffTi6k3bIDgg+xbCMlmmqmpawBmAOlEQrBxFSBl4FTGQyKwRooEKvF3hOTaR38OCnvR-kGzA4v99B1KCNiISjZf8w+klKQshzEaHl5CIAuwWPUza9onBObR7nmxfDa1fc0xFwj4hRIWVfaFfdcEEFCCvQuh86KyoYHramoqwJlUUDNUXZVBpA7gUFhADfgW8HkqwDYMZy8CwNbG+6KQJYDgCVAwAvEGrBEB0bhgDAc1WHOwF4BcAFAPAvRAgFjAhFRWMADYGCIRg5ByA5EMaGQSeJ7MoYCg-wXYGUG9DVB-Q3FIB39Y8UQOT-YiOBzDbcMi0H-GYSHzmHmD5sZ+PPHJWTZx9U2mHcARLhT5QCdhMA9wRo08GbQ3Ac-fEoUHJHIliGfUNjllCBiVBPYszUQMERUQ21iutoMok8E64fR02CnBGoQObAeQDOy-XLB62gzbhbCo4ToIgDiAURbg+wfZvqltDHURY3w1AAihp7gEf07QwmKKCu6Bc8mzBApoMJnIP9V8ownQeyNf6TD3+Rg4PhJX5Gc5BRgAgeiKOvwyNb8EorNlsNT6v4CObgtRorik4Ki1Yu7f-E2BAzFcwxFop5igCtAHxfCOPEOHfG1GWUcs0gQqpZlcDkREAWrGOOl2-oBddmig5JKimFDIkJen9KoVME0jQ0kAIOHoL-UkFaBbM1SHkKJwoZvEuACRCKOQD-a393e9-WuiMKzTBtxhlTTMYYMjZwdcxv-BYZHysEx9ixQqUscoUvKSjKx0otPjWPzb1iJ0jY0rKdUh4uBeBInb2KMH+w6gkgBPbEaOEeynNXshqOEVUVYAg1nQqDALpAm3CjArxczERAsDMqLiuA3kGqhRE6ouIu01IGzj6Gy7VARAn2KcCeNnDQMSWtiUTnkmwbYR6qrEhElcPbA1lPyV4kvjRKsBt8mgtYUYGajkh7BxQ2QfiRQwRQdBqkLpPIGQzIk3dkW5MB7hBKe5hdYJ2A-7PECtCmM8GWEIdl8kMlP0q2qPFMggEdopIghyMSgA5z2B2VMhUzfmEICV4o1neodYEOHRUCLctey3XVrr31b68Kom3ebiazTq7c7SlrU5I8WPCGhEUNADgAADV7EmYf4CAF4AABGQqdoiSKA4AAslqGdB-gQA1gduPyGqlyBqpAAJmkjHggAA)
