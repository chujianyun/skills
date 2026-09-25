# Structure recovery

> Reconstructs Markdown from plain text that lost its formatting in two requests: one stitches hard-wrapped lines back together, one classifies every block (heading, list, code, callout) with companion questions read only when relevant.

This cookbook takes plain text whose markup has been stripped (lines hard-wrapped
mid-sentence, no heading markers, no list bullets) and reconstructs the structure as
Markdown: headings, paragraphs, lists, quotes, code, callouts. The input is a team memo
in exactly that state.

A text-generation model could rewrite the text into Markdown, but a rewrite can also
change the words. Here the model never generates text: it answers narrow questions about
the document (*does this line pick up mid-sentence? what kind of content is this
block?*), and code does the rendering, so every character of the output comes from the
input, and every judgment carries a probability.

The whole pipeline is two API requests per document, run in sequence:

* **Pass 1, stitch:** one `Noul` question (a yes/no question whose answer is the
  probability that yes is correct) per adjacent pair of lines, asking whether the line
  break split a sentence across the two. All the pairs go in a single request, and lines
  that continue a split sentence get merged back into blocks.
* **Pass 2, classify:** one `Choice` question (pick one option from a list, with a
  probability for every option) per merged block, choosing among heading, paragraph, list
  item, quote, code, or callout (a note, tip, or warning set apart from the main text).
  The blocks only exist once pass 1 has answered, so this is a second request; it also
  carries companion questions for every block (heading level, step order, callout kind)
  whose answers are read only when the block's type makes them relevant.
* **Direct evidence stays in code.** Blank lines and explicit markers (`- `, `1.`, `#`)
  are read in code, never sent to the model to reconsider; this memo kept its blank lines
  but lost every marker. The model gets only the questions code cannot answer from the
  text.

All of the behavior is specified in the pass-2 question criteria: three dicts of
one-line descriptions, plus the step question's true/false criteria inside
`classify_questions`. The rest of the code is plumbing around them. The cost and latency
numbers are in the appendix: two round trips, 10,211 tokens, 0.8s, \$0.0015 for this
memo.

## Setup

```bash
pip install ipython "typesafe-sdk>=0.5.7" cooksafe --extra-index-url https://pypi.typesafe.ai/
```

then set `TYPESAFE_API_KEY`. Every API call is cached in `json_cache.json`, which ships
with the cookbook, so re-rendering replays the published numbers without calling the API.
Delete that file to re-run everything live.

```python
import os
import re
import urllib.request
from pathlib import Path
from time import perf_counter

from cooksafe import JsonCache, make_playground_link
from IPython.display import Markdown, display
from typesafe_sdk import Choice, Noul, NoulCriteria, TypeSafeClient

TYPESAFE_MODEL = "jev-1.12"
PRICE = (0.042, 0.00)  # $ per 1M tokens (input, output); TypeSafe jev-1.12 as of 2026-09
client = TypeSafeClient(api_key=os.environ["TYPESAFE_API_KEY"], timeout=120.0)
json_cache = JsonCache(Path("json_cache.json"))
```

## The document: a team memo that lost its formatting

The test document is a memo about a build-system migration, in the state it arrives in a
plain-text inbox: paragraphs hard-wrapped mid-sentence, a shell command sitting on a bare
line, two lists with no bullets or numbers, a warning with nothing marking it as one. The
text is fetched from a pinned gist so the cookbook's numbers stay reproducible.

```python
GIST = (
    "https://gist.githubusercontent.com/eugene-shvarts/6df7daf97233bf92bcdd6b386a0fa561"
    "/raw/5da03690611fb6ddcbaabdb91fb9f91d9751b113/build-memo.txt"
)

@json_cache
def fetch_document(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "typesafe-cookbook/1.0"})
    with urllib.request.urlopen(request) as response:
        return response.read().decode()

RAW = fetch_document(GIST)
print(RAW[:560])
```

```
Migration to the new build system

Hi everyone, quick heads up about the build system migration that is
happening next week. We have been running the new pipeline in shadow
mode for three weeks and the results look solid, so it is time to
make the switch for real.

What changes for you

The old make targets keep working until the end of the month. The new
entrypoint is a single command that wraps everything, including the
docs build that used to be separate.

bun run build

Generated artifacts no longer need to be committed. The new pipeline
uploads them
```

Line splitting, blank-line tracking, and id tagging all happen in code; no model is
involved.
Each line gets a short id (`L014| `); the ids are ordinary text the model reads as part of
the state, and questions and answers refer to lines by these ids (the same scheme as the
[semantic search cookbook](Line-by-line search.md)).

```python
def to_lines(text: str) -> list[dict]:
    lines, gap = [], False
    for raw in text.split("\n"):
        stripped = re.sub(r"[\t ]+", " ", raw).strip()
        if not stripped:
            gap = bool(lines)  # a leading blank is not a break
            continue
        lines.append({"text": stripped, "gap": gap})
        gap = False
    return lines

def tag(items: list[dict], prefix: str) -> str:
    return "\n".join(
        f"{chr(10) if item['gap'] else ''}{prefix}{i:03d}| {item['text']}"
        for i, item in enumerate(items)
    )

def line_id(i: int) -> str:
    return f"L{i:03d}"

def block_id(i: int) -> str:
    return f"B{i:03d}"

LINES = to_lines(RAW)
print(f"{len(LINES)} non-blank lines. The model sees, e.g.:")
print("\n".join(tag(LINES, "L").splitlines()[19:24]))
```

```
28 non-blank lines. The model sees, e.g.:
L013| The cutover touches three teams, so check whether you are on this
L014| list before you plan anything for Monday:
L015| The platform team
L016| The web client team
L017| Whoever still owns the release tooling
```

## Pass 1: stitching split sentences

One Noul question per adjacent pair of lines, all in one request; pairs separated by a
blank line are skipped. The question is deliberately narrow ("does this line pick up
mid-sentence?"), which is close to an objective fact about the text. The appendix covers
both the wording choice and how the merge thresholds were derived.

```python
def join_question(i: int) -> Noul:
    return Noul(
        instructions=f"Does line {line_id(i)} pick up mid-sentence, continuing a sentence left unfinished at the end of line {line_id(i - 1)}?",
        criteria=NoulCriteria(
            true="The line starts in the middle of a sentence that began on the previous line - the line break tore the sentence apart",
            false="The line begins a new sentence, item, heading, or thought of its own",
        ),
    )

@json_cache
def stitch(wording: str = "mid-sentence") -> dict:
    make = join_question if wording == "mid-sentence" else naive_join_question
    questions = {line_id(i): make(i) for i in range(1, len(LINES)) if not LINES[i]["gap"]}
    started = perf_counter()
    response = client.system_one(
        state=tag(LINES, "L"), questions=questions, model=TYPESAFE_MODEL
    )
    return {
        "joins": [
            response.answers[line_id(i)].noul if line_id(i) in response.answers else 0.0
            for i in range(len(LINES))
        ],
        "seconds": round(perf_counter() - started, 2),
        "usage": [response.usage.input_tokens, response.usage.output_tokens],
    }

result = stitch()
print(f"{sum(1 for l in LINES if not l['gap']) - 1} pair questions, one request, "
      f"{result['seconds']}s")
```

```
16 pair questions, one request, 0.32s
```

The cutoff for merging depends on how the previous line ends. After a dangling line (one
with no sentence-ending punctuation), a join probability of 0.2 or above merges the
pair; after terminal punctuation (`.` `!` `?` `:` `;`), the cutoff rises to 0.5. The
appendix walks through the probabilities behind the two numbers.

```python
JOIN_AFTER_DANGLING, JOIN_AFTER_TERMINAL = 0.2, 0.5

def ends_terminal(text: str) -> bool:
    return re.search(r'[.!?:;…]["\')\]]*$', text) is not None

def merge(joins: list[float]) -> list[dict]:
    blocks = []
    for i, line in enumerate(LINES):
        bar = (
            JOIN_AFTER_TERMINAL
            if i and ends_terminal(LINES[i - 1]["text"])
            else JOIN_AFTER_DANGLING
        )
        if blocks and not line["gap"] and joins[i] >= bar:
            blocks[-1]["text"] += " " + line["text"]
            blocks[-1]["lines"].append(i)
        else:
            blocks.append({"text": line["text"], "lines": [i], "gap": line["gap"]})
    return blocks

blocks = merge(result["joins"])
healed = len(LINES) - len(blocks)
print(f"{len(LINES)} lines -> {len(blocks)} blocks ({healed} line breaks healed)")
for i, block in enumerate(blocks):
    n = len(block["lines"])
    print(f"{block_id(i)}  {n} line{'s' if n > 1 else ' '}  {block['text'][:62]}")
```

```
28 lines -> 17 blocks (11 line breaks healed)
B000  1 line   Migration to the new build system
B001  4 lines  Hi everyone, quick heads up about the build system migration t
B002  1 line   What changes for you
B003  3 lines  The old make targets keep working until the end of the month.
B004  1 line   bun run build
B005  3 lines  Generated artifacts no longer need to be committed. The new pi
B006  2 lines  The cutover touches three teams, so check whether you are on t
B007  1 line   The platform team
B008  1 line   The web client team
B009  1 line   Whoever still owns the release tooling
B010  1 line   Things to do before Monday
B011  1 line   Update your local toolchain to version 2.4 or later
B012  1 line   Delete the old build cache directory
B013  1 line   Run the doctor script and fix anything it flags
B014  3 lines  If the doctor script reports a red result on the toolchain che
B015  2 lines  As Dana put it in the kickoff, "a migration nobody notices is
B016  1 line   Thanks, and shout if anything looks off.
```

## Pass 2: classifying blocks

Each stitched block gets a `Choice` question: *what kind of content is this?* These
three
dicts, plus the step question's true/false criteria inside `classify_questions` below,
are the entire specification of the classifier. There is no other logic. To adapt the
pipeline to your own documents, edit these descriptions.

```python
TYPE_CRITERIA = {
    "heading": "A short label or title that names the document or the section that follows it - not a full sentence of content",
    "paragraph": "Running prose: one or more complete sentences of explanatory or narrative text",
    "list_item": "One entry in a list of parallel items - an ingredient, a feature, a task, an attendee; reads as one of several sibling entries",
    "quote": "Words attributed to a person or source - quoted speech, a citation, an excerpt someone else wrote",
    "code": "Computer code, a shell command, terminal output, or a config snippet meant to be read verbatim",
    "callout": "A warning, tip, or important note that interrupts the flow to flag something the reader must not miss",
}
HLEVEL_CRITERIA = {
    "title": "The title of the whole document",
    "section": "A major section heading within the document",
    "subsection": "A minor heading nested under a section",
}
CALLOUT_CRITERIA = {
    "note": "Neutral extra information the reader should be aware of",
    "tip": "A helpful suggestion or shortcut that makes things easier",
    "warning": "A caution about something that can go wrong or cause harm",
}
```

Everything below is plumbing: build the questions, send one request, read the answers back.
If the type comes back `heading`, the renderer needs a heading level; if `list_item`,
whether order matters; if `callout`, which kind. The types are not known yet, and waiting
for them would mean a third round trip, so the companion questions are asked up front in
the same request. Most of these answers are never read: the step probability of a paragraph
means nothing and is simply ignored. An extra question adds little, since the state is
most of the tokens and is sent once either way, while an extra round trip adds a full
request of latency.

```python
HEADING_MAX_CHARS = 90  # longer blocks can't render as headings, so don't ask

def classify_questions(texts: list[str]) -> dict:
    questions = {}
    for i, text in enumerate(texts):
        bid = block_id(i)
        questions[f"type_{bid}"] = Choice(
            instructions=f"What kind of content is block {bid}?", criteria=TYPE_CRITERIA
        )
        if len(text) <= HEADING_MAX_CHARS:
            questions[f"hlevel_{bid}"] = Choice(
                instructions=f"As a heading, what level would block {bid} occupy in this document's structure?",
                criteria=HLEVEL_CRITERIA,
            )
        questions[f"step_{bid}"] = Noul(
            instructions=f"Is block {bid} an instruction in a sequence where the order of the items matters?",
            criteria=NoulCriteria(
                true="It is one step of a procedure - the items around it must happen in order",
                false="Order is irrelevant - it is a loose collection, or not a list item at all",
            ),
        )
        questions[f"callout_{bid}"] = Choice(
            instructions=f"What kind of aside is block {bid}?", criteria=CALLOUT_CRITERIA
        )
    return questions

@json_cache
def classify(texts: list[str], gaps: list[bool]) -> dict:
    tagged = tag([{"text": t, "gap": g} for t, g in zip(texts, gaps)], "B")
    questions = classify_questions(texts)
    started = perf_counter()
    response = client.system_one(state=tagged, questions=questions, model=TYPESAFE_MODEL)
    judgments = []
    for i in range(len(texts)):
        bid = block_id(i)
        type_answer = response.answers[f"type_{bid}"]
        hlevel = response.answers.get(f"hlevel_{bid}")
        judgments.append(
            {
                "type": type_answer.choice,
                "confidence": type_answer.confidence,
                "probabilities": type_answer.probabilities,
                "hlevel": hlevel.choice if hlevel else "section",
                "step": response.answers[f"step_{bid}"].noul,
                "callout": response.answers[f"callout_{bid}"].choice,
            }
        )
    return {
        "judgments": judgments,
        "n_questions": len(questions),
        "seconds": round(perf_counter() - started, 2),
        "usage": [response.usage.input_tokens, response.usage.output_tokens],
    }

classified = classify([b["text"] for b in blocks], [b["gap"] for b in blocks])
for block, judgment in zip(blocks, classified["judgments"]):
    block.update(judgment)
print(f"{classified['n_questions']} questions about {len(blocks)} blocks, one request, "
      f"{classified['seconds']}s\n")
print(f"{'block':<6}{'type':<11}{'conf':<6}{'companion used':<18}text")
for i, b in enumerate(blocks):
    companion = {
        "heading": f"level={b['hlevel']}",
        "list_item": f"step={b['step']:.2f}",
        "callout": f"kind={b['callout']}",
    }.get(b["type"], "-")
    print(f"{block_id(i):<6}{b['type']:<11}{b['confidence']:.2f}  {companion:<18}"
          f"{b['text'][:46]}")
```

```
62 questions about 17 blocks, one request, 0.51s

block type       conf  companion used    text
B000  heading    0.99  level=title       Migration to the new build system
B001  paragraph  0.98  -                 Hi everyone, quick heads up about the build sy
B002  heading    0.75  level=section     What changes for you
B003  paragraph  0.89  -                 The old make targets keep working until the en
B004  code       1.00  -                 bun run build
B005  paragraph  0.90  -                 Generated artifacts no longer need to be commi
B006  paragraph  0.43  -                 The cutover touches three teams, so check whet
B007  list_item  0.99  step=0.15         The platform team
B008  list_item  1.00  step=0.16         The web client team
B009  list_item  0.99  step=0.12         Whoever still owns the release tooling
B010  heading    0.96  level=section     Things to do before Monday
B011  list_item  0.98  step=0.86         Update your local toolchain to version 2.4 or
B012  list_item  0.99  step=0.87         Delete the old build cache directory
B013  list_item  0.92  step=0.90         Run the doctor script and fix anything it flag
B014  callout    0.65  kind=warning      If the doctor script reports a red result on t
B015  quote      0.99  -                 As Dana put it in the kickoff, "a migration no
B016  paragraph  0.92  -                 Thanks, and shout if anything looks off.
```

Every block's judgment is in that table, and the companion column shows the up-front
answers being put to use: the three "Things to do before Monday" lines carry step
probabilities near 0.9 (they will render as a numbered list), the three team lines sit
near 0.1 (bulleted), and the unmarked warning about the doctor script was classified as
a callout of kind `warning`. The appendix looks at the one block the model was unsure
about.

## Rendering

Code assembles the page from the judgments. Consecutive list items become one list,
numbered when the mean of the items' step probabilities is at least 0.5. That threshold
is a
group-level decision no single question asked directly.

````python expandable theme={null}
STEP_THRESHOLD = 0.5
HEADING_MARK = {"title": "#", "section": "##", "subsection": "###"}
CALLOUT_MARK = {"note": "NOTE", "tip": "TIP", "warning": "WARNING"}

def to_markdown(blocks: list[dict]) -> str:
    groups = []
    for b in blocks:
        if b["type"] in ("list_item", "code") and groups and groups[-1][0] == b["type"]:
            groups[-1][1].append(b)
        else:
            groups.append((b["type"], [b]))
    parts = []
    for kind, items in groups:
        if kind == "list_item":
            ordered = sum(b["step"] for b in items) / len(items) >= STEP_THRESHOLD
            parts.append("\n".join(
                f"{n + 1}. {b['text']}" if ordered else f"- {b['text']}"
                for n, b in enumerate(items)
            ))
        elif kind == "code":
            parts.append("```\n" + "\n".join(b["text"] for b in items) + "\n```")
        elif kind == "heading":
            parts.append(f"{HEADING_MARK[items[0]['hlevel']]} {items[0]['text']}")
        elif kind == "quote":
            parts.append(f"> {items[0]['text']}")
        elif kind == "callout":
            parts.append(f"> [!{CALLOUT_MARK[items[0]['callout']]}]\n> {items[0]['text']}")
        else:
            parts.append(items[0]["text"])
    return "\n\n".join(parts) + "\n"

markdown = to_markdown(blocks)
print(markdown)
````

````text expandable theme={null}
# Migration to the new build system

Hi everyone, quick heads up about the build system migration that is happening next week. We have been running the new pipeline in shadow mode for three weeks and the results look solid, so it is time to make the switch for real.

## What changes for you

The old make targets keep working until the end of the month. The new entrypoint is a single command that wraps everything, including the docs build that used to be separate.

```
bun run build
```

Generated artifacts no longer need to be committed. The new pipeline uploads them to the registry automatically, and checking them in just creates merge conflicts.

The cutover touches three teams, so check whether you are on this list before you plan anything for Monday:

- The platform team
- The web client team
- Whoever still owns the release tooling

## Things to do before Monday

1. Update your local toolchain to version 2.4 or later
2. Delete the old build cache directory
3. Run the doctor script and fix anything it flags

> [!WARNING]
> If the doctor script reports a red result on the toolchain check, do not proceed with the migration. Ping the infra channel first and we will sort it out together.

> As Dana put it in the kickoff, "a migration nobody notices is the only kind worth shipping."

Thanks, and shout if anything looks off.
````

Every word above is from the input. The pipeline only chose boundaries, types, and
markup.

## Open it in the playground

This share link holds the stitched blocks and the full pass-2 question set. Open it to
re-run the classification live.

```python
playground_link = make_playground_link(
    tag(blocks, "B"),
    classify_questions([b["text"] for b in blocks]),
    models=[TYPESAFE_MODEL],
)
display(Markdown(f"🔗 [Open the stitched memo + questions in the TypeSafe playground]({playground_link})"))
```

[Open the stitched memo + questions in the TypeSafe playground →](https://console.typesafe.ai/playground#share/N4IgJg9gxgrgtgUwHYBcAqCAeKQC4AEIAQgAxkA++AsgJYDmATgIYo0RL4oScAWC+SBAHd8AIxg0ANmHwBnAJ6yUCOAB0k60iQCMlABI18CAG4IG89ggA0+AI4SoAa3x8mYWfhgAHfE1EQYFF5+cSkZBSUVfDh6ZlZ2XhZ8Gg8eJi8vZBokOgEsIKEEBEcAOnwAdX400zEijgYYJCRs3JQ+PJEvGkzJbP5suTTIETgIMH4AMwgGXgYi-ELijyYkGTb+OdkYSRQPSQgIZ1kIXrAbY+SglM4aRE5uOCZHfnW5IRoUKB58KZm5pkkJXUmjIACZKOU0kEvis6AgPL98BYYMCkFoAMyUNDtE4yR7PThMBhw3b4Z4IHxCaaOFqeVBSYJGVb4CATRmjVA8MrY-iCETIFDmLwQbJXZZyFqSfhQCBwR7MtpJITMLweExmeRtFo2bJQSQwMC016QKAeULSRJBGCyBBrbiifg2rxElgIIEaNFkAAslHE9UaYgk0lRWgArJQAOLIMyumRE1gTJhQUlIbj7HJmPK2+61fAyuUfZRgbntPn4Lo9PqeLz7NwedZwHOvOZ0FKC+S+QKylg0KAAyTyGwrGRfBBOI18RsDABW1uh-2UHkQxOl7AmvWTsndIJIADYse1YFxTDMuDBR-WeHMXggmHBZOduKOnAs+OsZsjfHMWRwtXs27Uvz8J+NYrL4SCajwtKIlQ7BgEw8i4DuADsB78KBKC-I2yh3juAAcaELAgoh5r0AqcLeaieiQACcEI8BA6ozEoUiSCyQhIJeGwIFKTA2vcJwtCGOgkAeLT1twkCAdM-CwasCHCdouj4AAql48HKEiAQzPsfZsVwJwwgMXD4CeshsBwoIlF6LI6a6DAgto4L4AAIjxCCaa8uKBmEeZJu0hpzMm0zyI5mL4AASgGxrQFwzFQAw3RBMOPw0Jg4GQbSHw-JITB0LIik+vgACSbIxcF8WJV4QRzMKDCkkw+BzDImzbEECSvAZkhGRwz6ODYUmpkEXgMNARQyO8bTsrEPbsGUAAKE79EgEzMHmaRNDxqUMEo4ETfw7ySGxxz1ZcLKBPcJJ8Aw26eto4b4AAgh4LkrI1XgXdlxntDSTishMNiqCAjUxIws0cKm-hgB2Q29vCyRcT+A5ktkE3TFNshQRkLRAiAin7vg2IrI4D57YMARXGyKyZTk+D7IcHj-SUIA2CAI2ytVsgYNgeCEMAQMoPImQAPpaCQQMEPzICC5kEv4EDXwilACBA4DIAJR8Zg0EwctS64ho5HLQOPeTp25Q6bHTDcKBSpaAh3vD5XwORVuvDayYWXbUxHRAQgeNlAC0AgQMlPzbMdArIMrLJsjKqACqr8tsy6YNeDwRsgFFTS0uzNoEJYtnRDJeYc1Kmk2vHSDK4zbJYKBSAsCFhcNwwcQ0DUyjYInQO9Eowua2ovNAwA8oITLtskHCNb37Vss6zBHVtA8eEHYEtM1NACkOPy3igMBzNvKB8f14G+CgyirEUADcTW3u4viM2PrJyExAISqIvS0wKiXwt3ID2CHFWQ8QDlGmPfFggoaDiCLDmd6ZhjgcCtscfe0cg4AJgbITIY4eDbygB8cGQ4OBYGVgwaqchZQIALjxfiypAF-xlOMDOABhDmgRMwMOsL4QYPE2L5nlGcCiDAYgN0toED6KAbBW0anHCY9A5DNAyB5aIt5UA5gdLfNwpkzCiB7IPNWel9iBAzibIQRJmg5BsKwLwkiZi3DqkfVRQ0XhQknsoVu3hSSvHXL7HM648rkMQFqWmzY76ZjgHOYOQQYiyAKiAAAvmrbISgGge3YLEggQNIRJBpMyZ+ccL5ijELpZwYsAD8QMElJx4FKUwkhRZkHFrzKWMsgEZPVgxOG9DEpuO1rrAWHwpQZx5NbW2z9XhCAYrbE0ztUB-3dvEDQwCTaPGnEgscCyXB31pJNKCv4ArQBmSgOZMBRDzIssY6I2Qrb61pIISIMhGjjBmI1M57AKmJM4oKc8Cz0lJ2elwm5FjXxJBqVtKk2wZAf2gCUhpLIoCwC8B2b61xpmIFQAAcg8Mk75+8EDlPiWrSIXh6lkD6dLIWrSk6pm2H-JJXzUmcQzsVM0xT8Bi1PnSlJGyBgvIQPYKOB1rrOP4GAzMYz2jL2iBA+B+L9HdK1jrJpAsGiUqBsVQpBciUxy4ezZWYBcX4CDq8SVRIAjMmyuE3aaRFEcAGKKhyLMk6JkkDaDOw8GBPIRskVu7ljArCCEHL64p6b8RlIvBlNjIlcJnpcKISR+wVMqQrfsFMSWNMlgLClGdFadMdQreViVFUZpAE4jOAA5BAgQF5GGwGtbIWFwaMn+J6zGAQLTqKYKY78rI-5WIuXwSQXgJjbDkDAOgcIWIJCQQxeqR47b4kdrs-KRg+KbwdWrLt5i6AXL7IET2fgKYBI8kuu2fYOB0G4LQ2mVtd38TSEI95SdOXfIsr8zJLickyGfqu8YXqoUvjKY+zNIstDaDJS07NHTlZdM1oWslgLt1LNNkEc2W1XYDOcUkBuiBEaopdqedory9lJG9vsP2Z0g5DS4cOo6L9K7RzyewApf9555RVOnYBWct3llGnnH8IqZijG-PmGsHlHSRyrvDZ+ddcoNzih2K2Lc24d3yH-Ge-dlCDzaaPfg38kVTzpgBZ+rHF5sUlavW1OQN5b2o7vXFh9j6ELPhfcYCAb7NuWI-EVbIbQnjfuZD+tJv6b1iWrdBqqQFgOWOfRK0DswmTgTtKdzFtKoLsDAQB4QsFfFwfghZTniFmDIccRAVCXUHVGsoehYwIssLgOI9hNXt6Yx4SXOUw5LFmGEW-Cm4jI3SLXHI2QCjMhRJUUEEy6jm1aIYDo1geik4GIphczd2objWMLnY9G-rImYauPHdxnNGTeJECZPxuQSvHqWhoz1lqghUeibEpNIBn0MrfSAj9qNtX5PItcf9MKdD4ue0SklYGlXktlsA6lkhaWfK5a+plLLoVsrINoDlcOX0JB5S-flknXxmGFbZT14r+iaaXNKnasrFsFt6eDr5EX1Ves1coHw36eNjX1d+I1EqydfjNTIC1ETrWZEs0Tswf9nWuuAe6z11waA+pqTtwNhTp4HFDScKUEbm4h2jQBAeZ9fBHUTfolNgRQfgazcAnN0G83qxp0W-AUtS3AIrVWt++Q60rWmI8DZIS3CZlbRC3MnaiTed7d0ftPEh0jq2OO+EGzp3oznYqKJTxF3iRXeZcXtvVuGyQ7ujZB6LqXaCa0FxZ78AXoWKNa9Mxb1VCJIPZ7r2fkZyyUET92qf39CRwB1HQO1YtJJaCC3kO2nW6AXK2DtPi0IYua2s2fg0Ongw3bbDi7+B4dUa7Qj6zPYp5+Br32-sA1RsajRiO9HvMl0rkc23rHU4cbaVxnOvGED5yfoJ4uImy7iavzXGteuRucwZuIkZTG8LuW3dTAeN1MePTSeXXXaYzF0UzWNe8Q1dHRgW0TeVAbeCYOzA+LhI+WQE+MCaVS+NzG7TzfjbVXzGMY6KBT+XIYLX+W3cLNvKLZzWLNhO0HVeBZLchFBfgNBDLDBbLHBLhPBI+fLU+QrUhIIS7MrGhSrSfRbGrZhVhNxEucYZrAdXhWUfhTrIRbIHrMRQIfrG-WRC7EbJRRAHbSbbiTRE8ObW4ehU3O-NpExMxNbKxSNLbeqHbJxO2UUMwBoI7LxMjXxXKC7ChUvJtUJQTCJB7FIJ7D5bFN7NvT7XJWOJjX7XvAHUEAfKpUFOpLQEfOnS3cfKDVQ-NafB3ZpDDIZdoVgG2a-cZSZTfA5NFO-QlPfN5JDFZNZBlTZNwbZD4XZRkLfHopOLYU5PoxZTwy5VMGYBDPIe5OkT1XlBlIDF7DHDIpZcUBDGwCZEFdUNicFdtVlMouFBFfTXgFFLogUTFOQelPeOYIooGEHMo0fCLaHWHdI1vYBZlIpZHa4tePY7lAzG0XHaOCZAnRke1bVY1XnH3NxWQKnWonpeo5VGABnDVMeLVNnXVW0A1bnUnFQZYUaR5M6O7FwdIEXBA+1CXAEKXbTD1TMOXBXEwJXM6a4VXCAdXcNGQxTHXaePXTTA3BNeJZ7JbM3b4iosfRbaomDLEslZ3NpV3QUd3WtRqetb3RtP3FtBiIPDtLtMPW3PtJDAdaPY6MdCdBPZiGdT4C6A-BdS8DPW8LPddJOXPRDRYgvfdfwYvWIk9A-CvKvK9XIG9Jga0BvB9AlJ9CEhHYBdvFGbIh+GgX9P7K4sED4iHBAEldEH4yDJWGou3Oo+DLZPPRYhfFDJfS2FfVotfB2XDR47fAjcTYYg-UjY-CjM-MOWjCuC+BjHI2-FjFOdjDOF-WmXOd-Ggq2ITVcerX-OjYcqTWuTAIA+TUA1uHsFTSAtWaAzTWA3TVAEA7HGNZAheKUMzXnCzSeLAw0Gzc-AgzhRqYg0gqec+ZAVzdzO+agguZ+Og6tALJg8eH+ULJOdglMzgiBbgmBBLcsfgxBFLIQjA8LLLIoHLSQvLCyArTAEhYrChJQirOhW3DhDQ+rNhOvJrLhFrWjPhDrQRbrURFAPrQuAbFaIbGwsbew+0RwmQZw3RNwn2IxJDX0yxboPw+rbbRxQBYIg7MIzxdoE7KI-xEvUM9oZtMJJInXR7HYlvZMtpVMzvRjW-P9HMkgdEPMr4sgIshU34ttf414oypOYE-7FHKy9HAEz2bHaE3EvHOE78LydkmYEnNA8nb8ynFUhVcDFVJlfEx0FnLvdnPVUkxkE1Kk81KJIXek5ARk0K5k8rN1UKr1eXOYRXVRZXL1fkwUzXYUmYKjMU3afXeNI3aUk3USlAQs4sq3ZU8i+3NUsijUytLUtiD3XUr3IRA0rShI8mE0-gEPbtCYcPLwSPQdGjUdOPSdFC5DZPFxN0+4nINUVdbPDdbw6sv5PyPdBIIvBQkMicJIcMy9GvKMuvGMu9RvAypMtJTI7JL7b9cyLM-Izy6ynYofLQL0Xqqo0smKuDcHOfJDWsumeswuFo22A-dfVs2AbotG3fLslxHs8jQOfsi-VcgVb7XI2Ze-Cc9IJ-JOac3IWcj-ATIuYTUuMTcmyTAAmTN6bcxTMAvciA6YnuNsDTFQE88Cu45q2ecsFAm8iKjA8Ex8nAiRWzFgezIgxzU+cg38qgh+ecnzV+BgwLL+M8kLP+aC4y2CmLKBHg2BJCpLXa5BBgNLDCuQcQ3LaQvC2Qgiore60rOA8ravMi-RdQ4BOrBrGinQuivQtrQw5ikw1i9iqRSw7i7oUbZRPi3MabIS+bESwxDwq6iS9baS+xQI+Sg-EIw7ZSyYSIs7aIo9OIw0nS3aZImJb6ny36lMrIr9UcgpCy0E70PM6pM4klKGhyks3NKfVUunRo4BYZdGto9oCZE4TonGhOW3IjC5QY5ieYkYg2XIHZb6dew5Y5OY7YgYq5FYqs3IO5GBR5TMLYhZTuly7uzww42+44lxEohYNtSFSymyaAW4hAv8fAKY54gE3FGylnce6GqlJy23Qy9+tykGyG7yt+0XXlGEwVeEkK4nMqHnCkqVKK9EuGmfR3HEvEpnAk5Kok0aNKrnDK3nU1akwXK1PK0XJk23SXCLGXDk-2Lkv1Kq3k4NNXVcIUn2kU0OGNVq5KdquJGU9wuByevq2Ggais8HdUpOTU6tCayeBtX3Wa-3R0-+4PM0mOVa9am0ra+0z2RPWdF0g6tPd046zPNdP+X0ndGMwvIMgOq7YJcvMCCM16wuevOk+M5vH6xlHu-69M7vQevvEgL0PMiGsgUMeBhWfqme2KhG2++fJ0lGi2NG1fTGlsyYts9qDsl+AmkjI-Ym0-Jqgcy-Ncymscmm5gR-KcxobjZm+cr-dm5czmocgVHmzc2TYAhTRqwW1gfckWkAI8iW6XOAs86WwzJAueeWpeO8zA6zXA9Wt4t8wkEgpzXW6+fWviQ2l+PzE2sClgyCoGK2pOUBD1aLSBOLXgxLBBQuF2t20Q7MTBLCiQ6RXC9gfCwi-xkikOqrci8OtpSO6i7Qo5+i-Q9rVYIwli86Ni8wjitO6wjO2w8bNRASmbFwhbZNLqlbC6ugSSjbK2fwhxe7SulxaupSxGVShu9Sh6wJgS1uplqJFI1++HFB99OJvum-Ae7MoekgUMGBikElDJ1RtpP4pB6J97dyyy0MDB4VrBnHAK2EoVBE0q8KyVVEmVch7E6WeKoExKl4ikFK4kznYQ5h4h1h7K6IXKm1Aqp5Iq1kpOfh2xQRiq7kkRoNaNcRkuSRsF7XGR8UuNeRmHDqxbZRsMTJ9pdRnJ+G4tbRoGXR7UrUgx-Uox3l0xha3wCxntC0iPK0qPTa2POxgQ2s-apIQ60vE6r0zx6l7xm6qePxpuzSp64Jl69gN666z6yJtIzB97EygGqmIGnvEEpJ2V8GilElXcNNifC1ys0Yy642ZDIp5fEZPbe2HDCpje9sxkIjL2epk-DAppsmkZvHMy5jDptjOm7p7OGct-FmwuRctrUTcuCTaubVXmuTJuAW3c2Z4WtTMWmA5Z08ieC8ozTZ687Z4h+89ebA58neDWwg987Wsg78igv8usA2wCo2m59+O5821gsLf5jg15rgu2hC7gL5xt1LZ192wF7BL2ghX2iFo9KF2hGFsOxhCOzQxrGOl5OOxi9FxOkRLFlO55PF+RAl3i1RBwm7Ul4S8i9wqlhgLdWlsu2S-l491ljxdl+u7gc7ft67bSxItuvSwVhMoGZBmJ4y3utpyVtBsgXcOV4lLQddpVhBmlVVru9z1BxdgHXcbVzHXV-yimoKwnREk1lEinMhjR2e4tenBKmhpK+1+hjndK5E11rKgXHKjhr1u1Qqnhlkvh0qzk4N4R0-MN2qiR+qqRxq0U9Zq4CUtqxNxRzqwutdjd7J6nTR7N4anR0avRnUwt6a4tm7APY09tRaitlaqttamtjamPO0+Pex0xxxibZx54Vx5dT0jxnPLt-PHxwMw9DSx66EIdkO2vMduMpvSdnV6dzzwGzMhdjywL1J1drQZCUbjN8brLyhkARGmswp1DBso95s09p2XGnfTsoxupn2Bpu97rh9oD6-H7amtWB-SczjHp1-AUucwCgZpcgDv-NcsZrc8D6ZyD9uaDqA2D48+DqWhAmW7VEzBW8zXZrD-Zl83Do5j805ojvWjzMjp+Cj+gqjoLGjh5-+ejmCxjuC5j+LVjx275pBDj9C-5zCnjnC726NsCOQoiwO3TYO4Tssii8TqirQjhXQ1rWTgRNxTF3rHF1OmRdOxRdTibfirTvO1w3Tyl8S6lozzbGSgIuSzyFlxSiz47KznKLlwJTSktj1xzgVjulz3Y8L77sVrzvIqLzy5CEekoklUH4LrJ8HzE3J7L+etpRe1fcK1eqZSpuZeYnepgVZPe4Y1Y4+vZU+7o8+7eq+5Yg+25ePbMR+5TyfqJov4xT+ndml4FFDM4v+k0yy5CG47wO4sBiBrFV46BnY2ykgWv7LyokLxNz7uL9Vnzq-2L4YvyvlfV3B4KnEY1wh8k9As1tFUy5N8oeOXG1nlztas4qYqVEkkwxK7oE3W5XHPkEGFz5VquPrWrsVWlwNcg2vqHkq1zpgRsw0HXaNtI0QK9d42huAbkoy6o18we09CHiAKdxTdc2M3fNp7kMb75jGRpMxqaVDyWNNu1jOtntx2o-MnSzbVPKdyOrndTq3pIGF4xu49tfAfbB7oE0Hbnph2r3cJveg+6JkV+sTDvLOwzLA1y+IPIHiBjIB4R6BNuTNhQz1j5MkacPVGuhibJlNke+yc9lU0vb71uyN7Psve3Dhc0RyErTesT1pppwP2vTb9v0zZq08Vyj7YDtJnGZ81me9sVnnMxg59w4O2mFZohwMyXkUO-YNDugQw5WYReatMXocwcwnMda0vc5rL0ubkdrmivUCsr0gS0coK6va2pr1tofMHamQJ2j80N4iFMsHtIFrxxkKW8-a8hQTkHWUKh01CYneFhJ2jrIsZOBhJil7yTqKdfeynf3vi0D5Z0NOIfXOtoh05DdlsUfAzj4Skqx9y6CfMzsn3CIqU0+NnVQWXmz60l26qRPQVOz+qGD0yhPQpAD0sFV8x6WgKwXX3TYMDG+WbUAS3yTht8myHfDouA275b1e+AxfvkMQ2TD9xiJ9NEZ4In6YjFiwia5LfTWIP1L4i-TEcvz+EHEAUX9TfnTG34XEAG0rPCAf0RSgMoIHgE-i8S5Tn8C+l-SETf0VJAwVWD-fYm0g1YcjX+kJOih-0S6Gt8GYqP-orUAEZdbBlrMATKNtaEloBjrYrkQwQFlcaSnrBkugLOpOo6uJVWXLgMqotcVchAynpGxIFIBI0TTWRn1wTbG5k2tAiEdYId6DUtGLAkAHm3Gpzc9SC3Lgdn0Dyrdy2-AytoPmraLFrSwg7ag6T2pOMW2LjaQe20u7nVrhu7EACbADK3UVB3LMvOoMryaDR22gr6gXzc7F8AR4rBJlKySZ4RzBBZLQDRCDFbs8m6-ApujAPYI8l6SPDfISMOR410eXAzHmRlvaUZcegQhIQTyprzMSe77Mnp+yZrRDqesQ-9vEPx6M8Jm-NFnuAQogHkk4izLTP61yHnl8hyHOWqh1vLodheT5UXjhyqFa0ahhHFzPUP-Jy9r8wFfzIwTaEQVLaXQ55jbXeb21EKAw-XqhVdqcdjeYw03iC3N4ej+O-tWYbb3mEidFhtWFYUizd4MUNhcnLYQpx95q0-eg2A4ZnTsLHCc6d8bTvnQj6F19OhnUuncJM67YFKbiNlqnx8ScsYimfOznNS+FOd8+dIr7v8LTLisgRiTAHDRDBG1ISUfYqEZu2AFwiGirRJoi8Hb7qjO+Y-UITMRJFXVd6NTXERSJH5nsz6W9E5JP1JHX0Z+tMe+vP2pGKjL6Mkx-qv0ZHr9v6pxWpDv0uLSsaIXIo-ryKnHdFIGZ-d4hf1ga9i02ko34bJKBLP9wp4JcLrzz1bKi8GP-Ahi6wAHpcMS5ZSHs0mtZ6iIBBonVAw1gHOt4BlJfnOaMq6WiUKGAtWLwztECNvUTXfAc6JDTtd5ino7rt6MoFSlBu-o4bklM0ljdYRdgiUWGIjE1oC20Yn3LGKW6lsExS1c0imK25pja2u3TMQd2zHHdcxUgttu42tHyDru-pW7hWPu5VjT0z3SMmEw+rvchWvkgwfJK7zzslJnlFSSuwsHaB00oA2-vXxhFlSmBQMGHldWRrw8SmrglxFjTsmo9qmV7XwVj0XGk0Vx+PUvkTyTibiIh24qIZTx-YLlv8HNQDv-hA7JCwOIBCDheM7jzMbxkteAkhw2bPiihr4koe+NVp4FXy1Qz8s5h-IATSOjQ+Xs0JApgSza7Q1Xk80yQwT4KOvPgoMIN5oURhYhcYWbz45TCBOihOYaRQIkKw4WScBFi71orSd3e5Ez3l1m2HUSLC+w1TocMYnB9mJThM4WxIuFiVFiJdXwjxPj6md+JoRFPhEWEnWdG67w+IiY2QFRp9KTYtVnJNMr90y+IIkGapJ4j1IQZ-Y7SQtOlgIigYSI0ZEZNRFTEe+l9UkdiMH7WT1+CwfEaP2immTPijk8yXuzJE31a57kh5J5OfrnIE5+gj+v5MPqBSt+wUtkaYJEgRSeRDxTwbFMFHxThRiUkSMlMQZSjASMonziDPlG+UoSSowKiqIKlqiipkVNEqVI1jlSqGuXa4MzgK6Gi6pTrDAo1L5xsMKuKAzht62ukgAup2A+0b1LwGhsBpRAjXMNJjbkC0CkpBRjQOmnLzZpDfKGTpMWkwsRqbuSMatKmrrSOo3A5brwLW5JiNue0oQUdIbbO1xBOYyQenjcYXdP5Cgu6UoLuq2c1BT3DQS93rHvSImug1zonO+nJzjB-3HMunKBk9idAYOMURFi0najt2h9YcYvmKYuCMayM8pij3wzeDamQQImtjICGDk8Zz7JucnE6ak9n85PL9mTJiF-sf8wzY8bTKZ4MzzxQtS8SzM55LMchCHB8WAqvLczFapQlWth3wLi8hZUvf8ZQQaFeZaCxtJXrLIglsEoJisnobBJY6qzEJghZCUb1GHcdsKGE3WUQmmHW9KEhs6Fg71NlAxzZknNYdbLRa2zjCVEswjRL2F0TnZDEolpp1OGzZzhU0y4b7Oj7cT6WcfRlnxKrpPDa6OUcOen1EkBMPhm02Od8M+nSjnmP3FOaog7EwolIGc0osIpzkSK56ekhes0UMmMhjJjcgmZ8VbmlipUA-KyZ7DxFBJUZui2Yk5IskuTViXcjYk-XOX9EfJMy42Gv2HnMjf648tOWjmAaH9p5fIypnPJxQLzgcS8pSCvNC5rzXKaqTeWjiymYMcpCXfeflIEyFSn5mos+SGOy6VS3K+ouhnfKK5wCTRTUl+bHNQFcMaunU20T-J6nlV-5Tomqi6LqogKyBfPORlQL9EUtoF0K2BZDPPnQyS0S0tgago4FFsNp9neattPW5WNtuNjetvt0bakKzp5Cs7gWOoW3Srq5Y3to9LEmMK-IzC16dGVjLsLpl682ZSX1+4mD-l3YrOeUVEVT0bBjAhBdDwcGw8RxCMuRcexRlKKL2bsHwYTT8Ek1NFLTCmjosOV6K32xMwxTuPZx8Z9xZiqmfT1GZWLTxqQpTHYuZmZDuq2Qu8S4rWYFCuZqBIXsrT2YVCvxmtfDr+K-KBKSO4CEJUBTCWtCIlFtKJWGJebgJehcE3XghPY4az0sqSz2jrMmFZL9ZxFPJfb2qxLCzZxE13rHTKUJ1KJphbFjUskJ1LhsanI4W7KmwsSw+5LdWHpyuFcT-Z3S+4UHP6UCTQ5Lw4ZW8Kekt0HO-LS5NJLhUisPsNq+ZcCP4WFEdio9NSaQCcjrK3VecpevpMR4oi16By+ZncrblVzXlHAS5RMQDWwaW5Fc+5dP0eVz9u5mxRDZavhWlivla2E4qPLBS8Df1U85FCCtnmn955eKBKfKyA1OqwZ4o0VbCtSlfSN5E8pyNvKxy7ycG+Ob-piqPnYqSpA4-FbiSvkhKap70e+caP-4Ur3WtJalR-LkFfz6VbJX+UysdEYECBg0t0Ryq66xsWqPonlUmz5WppmNIG+aZaxzbhjxVK0yVTGMwVxiVukKXBctQVUHSdutpY6aqqTxkKpUF0pdFqvU00LdV90-VcGUNXVimFtYlhW9PNU6CCNH6mdvEz+mLKUcTkB1UBvsrOq1GQqvFVD1hl7t4ZzgxsvIqwyKKPB04tHohuvZYz-By4rRVfnxkbjwh9NIGIzUTVU9P8B48xdTIZ4ZqUhNitIUzNUwc8shXPZxTzw5my0BexQleHzJ8WCyfxwss5kEsAkSzgJramWcwRV6QSu1Ss7Xp8z16DrklmsgFqOoyXjqa0k6m3kYDt4qFZ1RE53iUtImosV1dsqpeusdlbqeKu64lqH09nh9vZRdPdn7NuEXreJQRa9SHOeF1171kcx9VgufVxznO7yq1aK1bHtb-peWlZVnPy2saxFc0+BWBoLkgAi5y9QVNBrLkYiMN8Gs5Ve2Q0Ej6dhKdDS-Sn7kjO5OG55TSO8nvqIunyoeSRp-qsiKNQ9bQOiCo17IZ5hyMFcmCFGQqmNOgYnc0nBnsb7+nGj5SAFlF95pdfG+LnvINYYqxcYVdUaa3E25ydRBKtVEStvm1TSVDU8lc-OU0Wi0B7Uz+d-K02MqhG-U1lQZuIFGb+yY0xsP115XHqAxaumzeTrs1iqUFTmyapwNc0TL4xHmxMV5sEGKqMxxCsQYFvVXBaKFMgjtld2LF+lItdCysbFuekmrQmZq8dhwsL70iPOX63hfjrV25adAE9ArTDSK0TcStnquGU4NkWVa-VNWkyYGvxoY81Foaxpi1ojVPtv145fRVuPjWkyk1-WlNUMyG3pqkh1iqZuNpzWTbDyji28SPHvHFqnxi2nmctorXlCBZfi9bQEtFlbbxZzahXtLNNoHa5ZR2pBdBNiXKyztA652sMOHVaz0JeYUFlhL1k4SDZeEo2QUrnVFKF1ls7hGRPKUYt7Z1S-7VxXomEts6+6j2S0q9ltKfZxdTpeetsQ9KK6ifJIOZ0R1DLTsEcjPmMujm3ZdKefH4ZwoHnWrcdUan9VLpSaMaAu3emFdrp4Mt7IuacmyMip1aoqTdX-ZLr-2PkkNT5Em0AXbr10O6oBTuxhi7sU1u6kBKm9+VaPU0+7-WOAv+bpuqp8k2VQ0rXJyp67gKI9FmqPfyp70k6XVwYgfcwP-2sDE9+jNaTNTc04LM9u0pOJaR81KqRBWYptkFtbaharp4WnVXuz1XKCDVbBsMi9Pr3vVktjYrHYRvS1tjMtm84QwXzSb3RY9wq91aVpOXlbR9iPNwZOKmIziGtmMhcc1tDh482tAhlfbGq62ZwjFu4kxcmspk76013NEbfTMP3ZqoO9ivNeLXP0gAdMc2x8ZzJv2eKVtn43xd+NrUba6hb+ptVcxAm3NwJHaujsdsAOnb+hyFIYUOq443aoDmE8FnAanUIH8lr2yilHRIlLqMD32ypWuqU6bq8D9Sgg0xKIOCVQdR62UhDpOVQ66W1By9X0qT43rGDHLFg6Mubpo7JlUk7g83rSmt7+D36jvfdH85ZzFWveu-s5UJPSH+FWrOQ3FwUOCakuRrLFa7pxUaGKpUm8AdfNoaO65Nzux+a7sQEtS35VXL3eYc02WHtN-ugBYHqAVRssJThsPRAuoHg6KT1R4rX4YizLSgj6CkI2nvc3mM8F3mq6umKIUqqSFBe+dHmMulUKUj5e7tr40yPYmaxITEdklsb2pbhdn64k+3qy1Abl2FR4HjoCC5UmIZrq2zZIqEiODvVFWpowovcGT6vBQa1RYfia1hqF9QQtce0zCGr641DNYY71vJk09DxFimmfvszVja5jbPBY1NvzUzbC1axtxYULLU7N79H4qtbsZrXHMDjDai5h-qlmgTv94FC450KuM9q4lKstjqAYeOoS0lwLZ45kvu1vHHt1CRA18ad4-HF1Vs-45sJ+1AndhIJqwmCaD7A7mlZLAuu0ooPl6Y+MOwOSifoMDLLOyO1g9ic+GcHX1+J5sUnKMGKTAzYZwnUBvDNeHCtUZuPeBkp3U6kSK9UueiN6KM6TllklnTZPrnXLo1ty45csgeUUinlC-LyVzsKMfr-kjUI4j8ol278pdMXQFdyOo0wbFdhzckyBfEM0muNdJ6i0buZOf8hNyh9k4Yc5M264qPJqqXyfy66HBT+h4U4YdFPsNxTbU83b63q6ym+p8puw0HuAWOHjNYC7lRNKgVWawzWp3w4gt1OOb9TKehuTKvT0mms9BCnPZadEEONnShexIx6VkGdsnTigl0zFqyNBM69nphvR9P7lSGcdP021XwuotA44kjqYGF0AABq8CCyLzBADGBtAMVm0PVVtCwRxgLqXmAAG0QA04EwAHG0AlAnIIAAALpxIgAA)

***

# Appendix

## Cost and latency

```python
tokens = [result["usage"], classified["usage"]]
total_in, total_out = sum(t[0] for t in tokens), sum(t[1] for t in tokens)
cost = total_in / 1e6 * PRICE[0] + total_out / 1e6 * PRICE[1]
n_joins = sum(1 for l in LINES if not l["gap"]) - 1
print(f"pass 1  {n_joins} questions  {result['seconds']}s")
print(f"pass 2  {classified['n_questions']} questions  {classified['seconds']}s")
print(f"total   {total_in + total_out:,} tokens  "
      f"{result['seconds'] + classified['seconds']:.1f}s  ${cost:.4f}")
```

```
pass 1  16 questions  0.32s
pass 2  62 questions  0.51s
total   10,211 tokens  0.8s  $0.0003
```

Two round trips, 10,211 tokens, 0.8s, \$0.0015.

## Where the join thresholds come from

The per-line join probabilities from pass 1:

```python
print("join  line")
for i, line in enumerate(LINES[:18]):
    join = "    " if i == 0 or line["gap"] else f"{result['joins'][i]:.2f}"
    print(f"{join}  {line_id(i)}| {line['text'][:66]}")
```

```
join  line
      L000| Migration to the new build system
      L001| Hi everyone, quick heads up about the build system migration that
0.77  L002| happening next week. We have been running the new pipeline in shad
0.62  L003| mode for three weeks and the results look solid, so it is time to
0.39  L004| make the switch for real.
      L005| What changes for you
      L006| The old make targets keep working until the end of the month. The
0.42  L007| entrypoint is a single command that wraps everything, including th
0.59  L008| docs build that used to be separate.
      L009| bun run build
      L010| Generated artifacts no longer need to be committed. The new pipeli
0.48  L011| uploads them to the registry automatically, and checking them in
0.40  L012| just creates merge conflicts.
      L013| The cutover touches three teams, so check whether you are on this
0.50  L014| list before you plan anything for Monday:
0.22  L015| The platform team
0.11  L016| The web client team
0.12  L017| Whoever still owns the release tooling
```

The probabilities land in two separate bands: line breaks that split a sentence score
0.39 and up, breaks the author meant score close to zero. But where to put the cutoff
between the bands depends on **how the previous line ends**, a fact code can read
directly:

* After a *dangling* line (one with no sentence-ending punctuation), anything at 0.2 or
  above counts as a continuation. True continuations score as low as 0.39 here (`L004|
  make the switch for real.`), so a single cautious cutoff at 0.5 would break up healthy
  paragraphs.
* After *terminal* punctuation (a character that ends a sentence or clause: `.` `!` `?`
  `:` `;`), the cutoff rises to 0.5. The memo's team list shows why: `L015| The platform
  team` follows a colon and scores 0.22. That is a low but nonzero "this continues the
  sentence" signal, and it would clear the 0.2 cutoff and merge the list into the
  sentence
  introducing it. No single threshold works for both cases; once code checks the
  punctuation first, the two bands separate.

## Why the question is "mid-sentence" and not "same paragraph"

The first version of this pipeline asked the obvious question: "are these two lines part
of the same paragraph?" It failed in a specific way. A run of short lines under a
heading (a list typed without bullets) *is* a paragraph in the loose sense: the lines sit
together and share a topic. Asked about paragraphs, the model says yes to every pair, and
the stitch pass merges the whole list into one long block.

Same document, same request shape, only the wording changed:

```python
def naive_join_question(i: int) -> Noul:
    return Noul(
        instructions=f"Are lines {line_id(i - 1)} and {line_id(i)} part of the same paragraph?",
        criteria=NoulCriteria(
            true="The two lines belong to the same paragraph of running text",
            false="The two lines belong to different paragraphs or different pieces of content",
        ),
    )

naive = stitch("same-paragraph")
print(f"{'':14}{'mid-sentence':>13}{'same paragraph':>16}")
for i in (15, 16, 17, 20, 21):
    print(f"{line_id(i)}{'':2}{LINES[i]['text'][:36]:<38}"
          f"{result['joins'][i]:>7.2f}{naive['joins'][i]:>13.2f}")
print(f"\nblocks after merge: {len(blocks)} (mid-sentence) vs "
      f"{len(merge(naive['joins']))} (same paragraph)")
```

```
               mid-sentence  same paragraph
L015  The platform team                        0.22         0.77
L016  The web client team                      0.11         0.81
L017  Whoever still owns the release tooli     0.12         0.78
L020  Delete the old build cache directory     0.08         0.88
L021  Run the doctor script and fix anythi     0.05         0.91

blocks after merge: 17 (mid-sentence) vs 12 (same paragraph)
```

With the paragraph wording, every unmarked list item scores above 0.75 and both lists
collapse. The memo merges into a few run-on blocks. "Same paragraph" asks the model to
judge whether the topic carries over, and between list items it does. "Picks up
mid-sentence" asks about the text itself. When a judgment call feeds a threshold, the
question should name the narrowest fact that decides it. Here the wording is the
difference between 17 blocks and 12.

## The lowest-confidence block

```python
uncertain = min(blocks, key=lambda b: b["confidence"])
print(f'"{uncertain["text"]}"')
print(f"confidence {uncertain['confidence']:.2f}: ", end="")
print(", ".join(f"{k} {v:.2f}" for k, v in
                sorted(uncertain["probabilities"].items(), key=lambda kv: -kv[1])[:3]))
```

```
"The cutover touches three teams, so check whether you are on this list before you plan anything for Monday:"
confidence 0.43: paragraph 0.53, list_item 0.24, callout 0.19
```

The sentence introducing the team list is genuinely ambiguous - it names what follows
(heading-like), is a complete sentence (paragraph-like), and sits where a callout would
go. The probabilities spread accordingly (paragraph 0.53, list\_item 0.24, callout 0.19),
and a UI can surface that - for example, underline for review any block whose type
confidence (the probability behind the winning choice) is under 0.55.
