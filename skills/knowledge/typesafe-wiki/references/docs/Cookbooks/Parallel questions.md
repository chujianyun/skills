# Parallel questions

> Runs a 13-question regulatory briefing over the GDPR Wikipedia article, showing that batching every question into one TypeSafe call is 12.2x cheaper and 10.0x faster with no change in answers.

You have one document and N questions about it. You can send one request with all N
questions, or N requests with one question each. With TypeSafe the answers come out the
same either way: each question is scored on its own against the document, so its answer
doesn't depend on what else is in the request.

To check that, the cookbook asks each question several times both ways - all N in one
request, and one question per request - and compares the run-to-run std dev: how far an
answer moves from one repeat to the next. Whatever noise a question has, it has under
both batching strategies. Batching adds none. Most answers came back identical across all
5 repeats either way, the same value on every call, std dev exactly 0.0.

Cost and speed do change. The document dominates every request. N single-question calls
pay for it N times, in N round trips; the batched call pays once. The bigger the document,
the nearer that saving comes to a full Nx.

The case here is a regulatory briefing. The document is the Wikipedia article on the GDPR
(\~54,000 characters, a document-dominated workload where the document is most of every
request), and a compliance team wants 13 things checked: 8 `Noul` questions, 2 `Choice`
questions, and 3 `Score` questions.

## Setup

```bash
pip install ipython "typesafe-sdk>=0.5.7" cooksafe --extra-index-url https://pypi.typesafe.ai/
```

then set `TYPESAFE_API_KEY`.

```python
import json
import os
import urllib.request
from pathlib import Path
from statistics import mean, stdev
from time import perf_counter

from cooksafe import JsonCache, make_playground_link
from IPython.display import Markdown, display
from typesafe_sdk import Choice, ChoiceAnswer, Noul, NoulAnswer, Score, TypeSafeClient

TYPESAFE_MODEL = "jev-1.12"
PRICE = (
    0.042,
    0.00,
)  # $ per 1M tokens (input, output); TypeSafe jev-1.12 as of 2026-09, see README
RUNS = 5  # repeats per batching strategy, to estimate each answer's run-to-run std dev
client = TypeSafeClient(api_key=os.environ["TYPESAFE_API_KEY"], timeout=120.0)
json_cache = JsonCache(Path("json_cache.json"))
```

## The document: the Wikipedia article on the GDPR

Fetched as plain text from a pinned revision of the article and cached in `json_cache.json`
next to the API calls, so the document and its numbers stay fixed even as the live
article gets edited.

```python
WIKIPEDIA_REVISION = 1363040264  # "General Data Protection Regulation", as of 2026-07

@json_cache
def fetch_article(revision_id: int) -> str:
    url = (
        "https://en.wikipedia.org/w/api.php?action=query&format=json"
        f"&prop=extracts&explaintext=1&revids={revision_id}"
    )
    request = urllib.request.Request(
        url, headers={"User-Agent": "typesafe-cookbook/1.0"}
    )
    with urllib.request.urlopen(request) as response:
        pages = json.loads(response.read())["query"]["pages"]
    return next(iter(pages.values()))["extract"]

DOCUMENT = {
    "source": f"https://en.wikipedia.org/?oldid={WIKIPEDIA_REVISION}",
    "text": fetch_article(WIKIPEDIA_REVISION),
}
print(f"{len(DOCUMENT['text']):,} characters")
display(Markdown(f"📄 [Read the pinned Wikipedia revision]({DOCUMENT['source']})"))
```

```
53,777 characters
```

📄 [Read the pinned Wikipedia revision](https://en.wikipedia.org/?oldid=1363040264)

## The questions: 8 nouls + 2 choices + 3 scores

One number tracked per answer, by type:

* `Noul`: the probability of "yes".
* `Choice`: the max prob, the probability on the picked label. `criteria` maps each
  label to its meaning.
* `Score`: the score normalized to 0-1, the score divided by the top level.
  `criteria` lists the level descriptions, from level 0 up.

```python
QUESTIONS = {
    "breach_72h": Noul(
        instructions="Must a personal data breach be reported to the supervisory authority within 72 hours?"
    ),
    "applies_non_eu": Noul(
        instructions="Does the regulation apply to organisations established outside the EU that offer goods or services to people in the EU?"
    ),
    "dpo_all_orgs": Noul(
        instructions="Must every organisation appoint a Data Protection Officer, regardless of what data it processes?"
    ),
    "pre_ticked_consent": Noul(
        instructions="Can valid consent be obtained through pre-ticked boxes or inactivity?"
    ),
    "right_erasure": Noul(
        instructions="Does the regulation grant individuals a right to erasure of their personal data?"
    ),
    "data_portability": Noul(
        instructions="Does the regulation include a right to data portability?"
    ),
    "us_federal_law": Noul(instructions="Is the GDPR a United States federal law?"),
    "criminal_penalties": Noul(
        instructions="Does the GDPR itself impose criminal penalties such as imprisonment?"
    ),
    "instrument_type": Choice(
        instructions="What kind of EU legal instrument is the GDPR?",
        criteria={
            "Regulation": "Directly binding law in all member states, no national implementation needed.",
            "Directive": "Sets goals that member states implement through national law.",
            "Treaty": "An international treaty between states.",
            "Recommendation": "Non-binding guidance.",
        },
    ),
    "max_fine": Choice(
        instructions="What is the maximum administrative fine for the most serious infringements?",
        criteria={
            "TwentyM_or_4pct": "Up to EUR 20 million or 4% of annual worldwide turnover, whichever is greater.",
            "TenM_or_2pct": "Up to EUR 10 million or 2% of annual worldwide turnover, whichever is greater.",
            "FixedCap": "A fixed amount not tied to turnover.",
            "NoFines": "The GDPR provides no administrative fines.",
        },
    ),
    "individual_rights": Score(
        instructions="How strong are the rights the GDPR grants to individuals over their data?",
        criteria=[
            "None: individuals get no rights over their data.",
            "Weak: a right to be informed, but little control.",
            "Moderate: access and correction rights, but limited means to act on them.",
            "Strong: access, erasure, portability, and objection rights, with enforcement behind them.",
        ],
    ),
    "penalty_severity": Score(
        instructions="How severe are the penalties the GDPR provides for non-compliance?",
        criteria=[
            "None: no penalties of any kind.",
            "Symbolic: small fixed fines unlikely to change behavior.",
            "Substantial: fines large enough to matter to most companies.",
            "Severe: fines scaled to global revenue, material even to the largest companies.",
        ],
    ),
    "compliance_burden": Score(
        instructions="How heavy is the compliance burden the GDPR places on organisations?",
        criteria=[
            "Negligible: no meaningful obligations.",
            "Light: a few notices and disclosures.",
            "Moderate: documented processes and some dedicated roles for larger processors.",
            "Heavy: records, impact assessments, officers, and breach procedures for many organisations.",
            "Extreme: obligations so demanding that ordinary organisations cannot fully comply.",
        ],
    ),
}
N = len(QUESTIONS)
METRIC = {  # question type -> the one number we track per answer
    Noul: "p(yes)",
    Choice: "max prob",
    Score: "normalized score",
}
```

## Ask two ways, 5 times each

`ask()` sends any subset of the questions with the document and reduces each answer to its
one tracked number. The document is byte-identical in every call.

Both batching strategies run `RUNS` = 5 times, giving each question 5 answers per strategy,
enough to compare the mean (do the two agree?) and the std dev (does batching add noise?).
Calls are cached to `json_cache.json`, which ships with the cookbook, so re-rendering is
free; delete it to re-run live.

```python
@json_cache
def ask(keys: tuple[str, ...], run: int):
    """One TypeSafe call -> ({key: tracked metric}, input_tokens, output_tokens, latency_s);
    ``run`` only forces a distinct live call per repeat."""
    started = perf_counter()
    response = client.system_one(
        state={"article": DOCUMENT},
        questions={key: QUESTIONS[key] for key in keys},
        model=TYPESAFE_MODEL,
    )
    values = {}
    for key in keys:
        answer = response.answers[key]
        if isinstance(answer, NoulAnswer):
            values[key] = answer.noul
        elif isinstance(answer, ChoiceAnswer):
            values[key] = max(answer.probabilities.values())
        else:
            values[key] = answer.score / (len(QUESTIONS[key].criteria) - 1)
    return (
        values,
        response.usage.input_tokens,
        response.usage.output_tokens,
        perf_counter() - started,
    )

def priced(result):
    """({key: metric}, in_tokens, out_tokens, latency) -> ({key: metric}, cost_usd, latency)."""
    values, input_tokens, output_tokens, latency = result
    return values, input_tokens / 1e6 * PRICE[0] + output_tokens / 1e6 * PRICE[1], latency

# Price after cache retrieval, so a price change needs no new calls.
batched = [
    priced(ask(tuple(QUESTIONS), run)) for run in range(RUNS)
]  # all N in one call, x RUNS
singles = [
    {key: priced(ask((key,), run)) for key in QUESTIONS} for run in range(RUNS)
]  # N x 1, x RUNS
```

## Batching doesn't change the answers

Per question: the mean and std dev of its tracked number over the 5 runs, under each
batching strategy. If batching changed the answers, the batched columns would differ from
the single columns. A shifted mean is bias. A larger std dev is noise.

```python
print(
    f"{'question':<22}{'metric':<18}{'batched mean':>13}{'single mean':>12}"
    f"{'batched std':>13}{'single std':>12}"
)
for key, question in QUESTIONS.items():
    batched_values = [values[key] for values, _cost, _latency in batched]
    single_values = [singles[run][key][0][key] for run in range(RUNS)]
    print(
        f"{key:<22}{METRIC[type(question)]:<18}{mean(batched_values):>13.3f}"
        f"{mean(single_values):>12.3f}{stdev(batched_values):>13.4f}{stdev(single_values):>12.4f}"
    )
```

```
question              metric             batched mean single mean  batched std  single std
breach_72h            p(yes)                    0.804       0.814       0.0055      0.0055
applies_non_eu        p(yes)                    0.990       0.990       0.0000      0.0000
dpo_all_orgs          p(yes)                    0.030       0.030       0.0000      0.0000
pre_ticked_consent    p(yes)                    0.040       0.040       0.0000      0.0000
right_erasure         p(yes)                    0.990       0.990       0.0000      0.0000
data_portability      p(yes)                    0.990       0.990       0.0000      0.0000
us_federal_law        p(yes)                    0.010       0.010       0.0000      0.0000
criminal_penalties    p(yes)                    0.108       0.108       0.0045      0.0084
instrument_type       max prob                  1.000       1.000       0.0000      0.0000
max_fine              max prob                  1.000       1.000       0.0000      0.0000
individual_rights     normalized score          1.000       1.000       0.0000      0.0000
penalty_severity      normalized score          1.000       1.000       0.0000      0.0000
compliance_burden     normalized score          0.750       0.750       0.0000      0.0000
```

Reading the table by question type:

* Choices, scores, and six of the eight nouls come back identical across the 5 repeats:
  std dev exactly 0.0 under both batching strategies, every batched and single call
  returning the same number. One call with N questions gives the same answers as N calls
  with one question each.
* `breach_72h` and `criminal_penalties` carry a little run-to-run sampling noise, and it's
  the same size under both batching strategies, with the means agreeing to within that
  noise. The noise is a property of the question, not of how you batch: batching neither
  shifts the answer nor adds variance.

Either way, there is no batching effect: no question's answer depends on the 12 other
questions sharing its request.

## The only difference: cost and speed

Same answers, different bill. The \~54,000-character article dominates every request, so:

* Cost: the 13 single-question calls re-send the article 13 times; the batched call sends
  it
  once. This saving holds however you fire the calls.
* Speed: the figure sums the 13 single-call latencies, so it assumes they run one after
  another. Fire them concurrently and the gap shrinks, but the 13x token cost stays.

Token counts and latencies are cached alongside the answers; cost is applied after, and
both are averaged over the 5 runs.

```python
batched_cost = mean(cost for _values, cost, _latency in batched)
batched_latency = mean(latency for _values, _cost, latency in batched)
singles_cost = mean(
    sum(singles[run][key][1] for key in QUESTIONS) for run in range(RUNS)
)
singles_latency = mean(
    sum(singles[run][key][2] for key in QUESTIONS) for run in range(RUNS)
)
print(f"{'batching':<24}{'calls':>6}{'cost':>12}{'total time':>12}")
print(
    f"{f'one call, all {N}':<24}{1:>6}{'$' + format(batched_cost, '.6f'):>12}{format(batched_latency, '.2f') + 's':>12}"
)
print(
    f"{f'{N} calls, one each':<24}{N:>6}{'$' + format(singles_cost, '.6f'):>12}{format(singles_latency, '.2f') + 's':>12}"
)
print(
    f"\nbatching: {singles_cost / batched_cost:.1f}x cheaper, {singles_latency / batched_latency:.1f}x faster"
)
```

```
batching                 calls        cost  total time
one call, all 13             1   $0.000497       0.27s
13 calls, one each          13   $0.006090       2.71s

batching: 12.2x cheaper, 10.0x faster
```

## Open it in the TypeSafe playground

The same article and the same 13 questions, packed into a share link. Open it to re-run
the briefing live; the same numbers come back.

```python
playground_link = make_playground_link(
    {"article": DOCUMENT}, QUESTIONS, models=[TYPESAFE_MODEL]
)
display(
    Markdown(
        f"🔗 [Open this article + questions in the TypeSafe playground]({playground_link})"
    )
)
```

[Open this article + questions in the TypeSafe playground →](https://console.typesafe.ai/playground#share/N4IgJg9gxgrgtgUwHYBcAqCAeKQC4AEIwAOiAIYBOKAllADYKkEkgDOEMFUje+pAFihQAHVrgD045ADoA7tQDW1YQjDUy0iBQDm4gPwQ6asAF4AjAGYAbBYAMAFlsAmK-dIAaPiBRYUTL2j8CPgA4sgIFGR0+AAiZChk+AAKFBA+UDQQSPgASgjaMHTx1Fn4ABR5BUWZ2WUAogCqAJT4TrZmVuJWAOwAnE2eZABGQxQIAG7qPmChMUk5ntSs+Il1nBAqZNkNSCXZY1XFpaXUSABmWnBH2cIU1ONkUACe+Kf4KEH4a6mb27ul9WaKyQMw+wW+GwQWy+UCyEDgtHwAEExol6nUkU1pPhAsEQnMcq9ltDqHBhFoEqh8LCyVlkCh8BAzl8GvhbvdHi8irJgTN+PBoXdtIJltzFjdKDRYEUKMiqLQGPgABxlMwtJnvT4AYX4koijOZADEYCCyIhUFFctRhShlhqwV91r98Ds9tiAJIMqLsfDaCDjCJIZYOlCRINnfUalQUdhIS1geKJDi26hgYIOxq8r4Y7G42bzADkyz93pWY3eEHwyF1SG4rxB91TMG9BepWVDhizQpFjIDsrB1Fl0djltOFwoVxqWZQldYpOEdGoZxeDoOhWuy3H9Z8FDjNUtQxgc6QCFYrA9DNYMGHqlPmuCcQSyVS6SnMUHCAy92CvQArOJ7E6OotV5QY4CybRGTBft+FObRWE8OcyUXM5qDvEMIgRJBDAgbQnmkYhiCQPMIWdJJKEXM16SzLUOFrahontT5SKhP49hWSBhGme980JUozHsZF2WiNoOk8Gd8CGT94WCBAzgjL8A0ZbInF-fAAFkyBeUSlWxJFiWyTM12qdiylOVgfDIGYNUSNQxkUhABh4-F5nwXVljsz8GQYbRLTkhSvRBfBIDvbCGTGABHGAP3eMNWHJOcp1OCS9z2S1uWxAAJCBZAmCJFi9OgfVuf1UzvM4GEwaghgY6gUBeLdTjUSYwGbaJEDgKTZQs+J0MrcC1GXco01SXyfHwM5UjgFp2EQA1XltNlUkmOcsnPQikH04Eq0wM0F2CJjggAIQoI9WAQIqq3krzxM+Yzrkkz8qJWfABouiatFerYXjSIJZW5YlUhNUFPlkLQjHFegYDUJBILeE6yAALwYzwACkyGELZPAAZTgjGtAQHHk34ZFJtoMgiZgD58AAaQJin8Gxu58AAGS2BQGa2GZAjIBiub0s4d3wBgyEmWGeJY6FXSyW7gldbiabgyA4CrOMMlUBblkI0gGhp3jtZARY01Qcnogkh0XJyXNtSiJctF2RJaKDeB9RSDlnmRDJyi1LUkkxQZOO40onCVfBUZNYIdM8dyvqQF4kL5u4aDveRqYtgkCKIjaNpMEx8CdnxUGWXONrzS3WnaKw3LIZYLry7IoF1LiIgQtta0DODfXCSJohKla9lb9l6P21vu0Ww7gsTfAryGAArG7gqptC7WZBMn1hVBUjoBgY0ZIdUm4M8tFb0MtlYCNd6jFusnjKfzdgigwAAWkxqgXlhE1Q2XxDrwiFatBeGQKm-AtB1W-m2SEkQpxmggq9BAnV9Q9R8KPeBqhwGURqoueqe82TICiMnTcn1RhQkbvNMeg9lpLAHvgMY1QNYSXip+JciISqH2PJBRKzYaity5q9JY3Bt5bAQBwTcpxLR9yoWta2eICQrCKpWDeCRzL4DMN0CwNCmEJEusITgCV6EKJlEueOsIVBdmuFEYIW5Vz5HXDOCgLwJGrSDIMZYuVt4rGWHVUU+QlgmSUslekyxADIBLkTRlp7CeEakGSk3BPBSW0MooY8ctKdw+PEHirDTzsPmsOG+0Q16JFYCAwoMwpJ8EIuAU81oTyglnH-YIVwkBKBBAbTOSBs5EVznnMIJ4e5LVKk44uJciJ5nutA4QC5l6vGZA6ApbcOzb3yjgzJR8KCeE+rMqeM955ezKLkpALQliSRrhrN4GYGjSI0YcaB8iVgTMXH1PevldisA3Mc861kqZzjTBLVkS57zv0MAwL2n0VnLH2bfJ8GomqNlaqWOg0BeozHMmVX5lyxnsRCssMKdyFwrkrA6MFncNRzKSUtDk419ngsoWmEG6TCW6IgOdau2KFFZBPF+UoElEglQjGeNKjFZQ0kQFwdQ0RHg0EmPVTOpByh5CgHVS0ZglRYg2kiKAsJH6pIJcxJ0rF87wgRPymW5TSBJGvnGfJU8jljkuA9NJ4ULq9WDJWEkxsaCoQ1p9MqJtULDEVDClqbUPTMieBwakWwcWeQyHQF4PqPWAOyIGpslpJrwk1Ok21E5riy2yGGmA+ATz6Lbt8-UsggjQR4smuF0QjkWQYrW91zD-UIGxAATXDUUjgRh3hkAUMEZKrqNV0QZA6LNk52L5rLMEIl4sZzaAQJW1OJMohm0+IgM+Gia43yGLG4WigLr4sevgI8GsyUIDqn9fAU7PrfSgle-ZFZXhNqGg6+szUU10BlSAHEnxbhMOZWmVCuxuHzR3HAZYV5SE11NSACFVqEgG08AbWd2gkOwbmdsry6GDaKK3jvdDvCUMHyyVoA207p4JG4m8FEUpFT2DaaMmxJlShYsLWkNkjKqBPoxnip9hKSP8vFlfGMeTJ5Pi3KlMT51YBJ0AYpMBd5PrclVuObg5oGQT0aAAbjcjlPKaz31HlDC8bQQNRBt24LuDWwxkwTUeJ3HlaR6RirbhVWgmnmQA2rkpKKp4aga3LYuq9tGFTBHsKHD+PaymnHGBAfttTp4IAQAoJ9-6AxUlslPPDQLEEwDnl5HjmpBwzA-pvJ4RZhZkFkJuKabZkJPE7sul6PlLRaBGhNOrb6ysmcqyp5AanUGoE8LPaGtAxXrNlFJy1SXZN1UAcA0BBCn1qFYPQJl6ZZwwGg4tpOUzCUWshUmZk0JMz7M8AcSgYAGBnnmkFytmynxjFLZ47In07NaYuXKOj4XQ5IPQrqQKLxRtgAXRp+aiQP7cY2XcQ8M3eF3rTAqpxEPshWSwksU+krghAI+Etn6J3iuPzbJ-exGioqDkc-M-DkZ97QFI-2AlcUL44NW+t5l8HxOJCuC8HFZT7K4ReV62UA2tDcBbfWYELxGm9JPUgG7ywhgnOsmjpNqBAzmPFWZ5LGnPCLn7S9OAVM2rC3yJaGuc4ert1ilCbBbxBuPRQLlZAPFIowH86kh+MwyjYSQE-RoLQetk94ecnB3P4FdUo71S5cySqvnYmMccKtMZQA5guuRPpThQzTMSJLr9eqxCnikZznLsjvnstjj6MEZ2GFoDjoKUA7hYUtKN+tdYZN2IzQyCROeaGFCUzcQ7CHEhYEblsBdxIGTYyo8EBgAY6CeGltkOfF1BhBQCbuTXpv5-rSIkiaecFFTnU833m7uKHkurkdETMHVI--fPF8R4JNb+IJn1WHqu6lhBAMu+hAKgQTURXjRj-zB67bzblDYyYhPpBCUBZixYe5jTBA0gLi8xFyIRbCl4cQY4WRQLfgGgRjtytyLpQDYiQGvZVhP5wIILdRv6whPyQIF7Na-T6hkGeA96dxG4oAm4W6Y4YH17WQ6BbBULiyzwQDJSMjRgbghovSHjHhZIsqvSFA0D7Tv4JCf5FIabkHnIFSKEWQ+Y44H6wyKiQEeKaywYiwzC44gJyboZK4fLKQ8QIpQAPTQqLQGxXBvD+b+pf4abkZBblgOgeE3CCbZISqNjLYJAG4oHcCXIWErBgHYIfBHgrAZDEi54Gx0hPwWQbDTwgLCDkYMK-wUArQ47uICb05CaQRhFSpTJMTpKyGnDyEfBAzCh2bnJ6SOg-D6qPiJDF7x6lBHQQBXblB1BzBHSB4QD0Fap7gA7BBkHYijFJBHSajJFjDRGzHfZhatC9CF5Ph9FeTsQADqWgzSkE5Eb80i5YlAskmA3AXE1CW4seIRpyquVYyEEATw4OiivgOCbw02loMmnA4Bb69a7iCINox6WGXsEk1aJuQeLwGKUiHS7SnSucz4WeygZ+vC3IZwhQnGFAeiQyJgyJoW9AwQakx+doVMB+mA5Kw8Z+tCxQc6Oqs+1WuJdAJ4t2UYIRncnOBSlyqEMYJ+YIzKjCCqnqwYgOXOuhDIZSYKGsOJhQsakSvMFAe6vCbwiQp8QYr81EMuEQek8oZJ+AVcaY8+GwkpRyQ8CqKhZKYpRinu6SfJU8PO7GspM6zxMwJoCu945YRy6SIsehdIpuvk0QdhRyjxYh4s7AlyzB+8GJI8GiLOEksGOiBJG2+6CIVGewOGFScyGORq1wuZpAjwsmnIxZbAdiZA6ei4WZRZFSa+MwBsASZm4BvCG8qETats9UrSaqRpioVc9+XejhbJeJaZhJ06uAyJZQZALQ7oMynwmG+WOyDIMcCSGWJa1E98HpFR2SGosEdosoD6Q+XO2mG0ZQQwLQaAlY7JqE7ieGEqJuEAn+Y01CzWWWT4UJKAk2VevarACgk+ruCAfmQZhOS5BWXs5alYNq2Q5RbC809IEQncg6L0D5GQZ5REZQUAV5bKDW+A750pOWiyFAfWZujEL5G4GFSAZQYAOF-Sr4PEUqo46uz248YFWyy5hWt6YUV6sJUQVFZQjkOIlY0YSeL0CQ-5kuDKn+UA24EQ-mvxb28k425uCRTwAlZwLQhoGynwPkYCk4A6LF-mK8L0cyRFO8YeROMwr89Ung3pTR3+hlO4xlFG-oEQdwYAxskkcaRlFkJlj2hSnFIKR5tObkRy5CKRmqMMkE25+cuoVAkYRowMVEFo0QOQ1oPYgl9pq6PlPEzhzKGojcDEYAYwBybS859YSeGsG850VIRyp6lhkprJsg7J7yEZoKPJsMngNVepxm+hj0LuWAkyCqDIjx2WuW6slhQUJCJM45GZcy9V9h442ITstVDIRuehZShSKg4ptAkSYwh6vo34SAbBRQpwe6YMj8qgjZcuZoNUBQIiKwyl2aU465LuZKAV08QVKAum0IWQi4J4VeKs5atAJMMcPVVIGwoGOB22XBYwjV20UN9B1J50wK3EZKQGQCdADI-p+AkwhgLhC5Mi8wLieVa01ERyOKJod11oMAIi6pz1iApSK4nwp6FAHoaOnlYCJqRu2NmJ6YTwKgJlqGX0vOHGZSBscO12qgBRuEwW+oKFhSh+OOjND0JUZI35phHwNqrKl4O1zCslEkM1J6BVq8iYN1Y6DYQa4imESwgyFGOKk0yWe6b1SA2IFQYS0QFgTgqqREPRX1EFi0G17pV++miWy6JV1WxWywENXoQO7wpIhM04f6IR80kAncPowdbpx68VHWaSSaDIsgMGEkUN9YHRZl7YNOsorpOKiep6SWxRdeT6bNriICwUn4ANSB5NVIEkItb6lNHGOBHme6HKWSlAuV7W+oEk9dDo50jdMRBqQY1EW4RVRgpVngQGjRyKsFd0zGD0MGUkncPp+dKiVcTwUIl8PaM52NxSwo+Fl6PEUN7EW4L+NBzqT6fF280ufaA6XoooOUphlg16F9doRgTkWdZSrt3leVsERglWupkNQqxmEAagWMWYfYzau6raG0FVsdaWnVkERdxIdAqIYADiNKGswMU9nw-t+xmB5eBxAYgwhFlduWsobGOKuoSkEkYw9BQwSiDc3dONRN-SbCyFHk0ALs6uU11k-DqBLx9WkyfB99acnwlslWbuH4mhcqntKi3QaobSyJXSVoNo-li5HFgd+AXSyJOcxjaAcUCDHsvCA03ZUyXSxJe+-ZwQZgTg5O0Uz2PEFdm8bD+DpUPy469qLJGGFjK5kukOWQyOSd2p8U1xw2cl281o1UiovCUIc46pGqWSWTlilwdl2SZJsBvCKBbwRQsMzYC64obIkotA64soW4d6ET0Cnlz29h9pqEzhX9RWq9YA36NjqJaJ7o5wdq0CQUpZ8h7jpcd0GVJ+szt2ZQpJioZgv4hyue4FsTY8F4R1AY4KwiKhq4SzPGBTt2A4Q4J5cyGpkzL17Etm1JICPI2txzomM2C1iuF64s8pwzyILDwTxFMp-SLUSd14pQbu-ma+vYf8aEPIE8zhPgfodwSmZtT4b61xj0vJnpphbi4queJiBOPEj5R2umuJVAf04EYwssQLCyFlMcMJDzKsn1X5DhaYSil0zzo6Kdu5cEP80GTV+JE5E8qGngzWUFrL5jT4da8V11WYrzC0KRFO8NgTiYbS++uzhWEDOOWD-GzO+ozpEmdWwZdcGQqQuwslItrATwFk8CPG6+qArqPFSyy6dmh9fzYwGW3EaaKs6d0ZlYH1Mr8TwLO82I-tb6McUkLuV4ylCq9I6pvunxSwpytctxdA0MCrh4DIcyUbB9yWb28uLwaYT88azCZ61JYwQR4KTKc4+rEkANqWsVn9kuIFNQgrK6iu5DYTnuwQtCEwWwONL6aEhmA9KAHNS0YRsSemuUfYbBNKGd22JM5bnqu8zh2QZSY+iysMArX1QrUlnw+VB0zISI9yCAlWuMdwErf0wQcWTdIecUjeygub1qkGdigWD9PKJ5q7o7w5gRWwMAZwj5YwsorFdwqRkVTREAP5bw-1jRj0XDJQnAloCQOgi6e7INpCtCUyMBkwe6rGEwTdwGC6BJdwRcw5G7x627DAu7zJEaXEnASdtVYAN1GDy4bSgx1MpKvzkEBYPeqgrYwbwQ2rXsvCPHncBYz5c9AYYABYnbphPLiHosyHhm2LWembtKk7VkagHb6rT4urYLZUzNZNYbCtaOlGp0GQTHMj9W4ExbJtGsVuCYxO5rHYVrQN8Q6K5zEkseFIwwtUdu1KYTZ6Lw6zkctghjWcYzec8qHq5M0zMwEQNcTHVj1je+NCPnQbxTOgaQhc+FMGaxRQ3AJn3OBMmZdUGsY8CFkQV4fpO9d7Lc7EE85cb6RDHEUNoXEseq0I5xlE4ObwmkXAJMokDGmxxpqiRnveb6bL31ChZzEJPDwF7uehyXdXJ7uCnzR2GidCiWYIKspQd6wZNkha8AkeGoZmdEYArcGnY24svuyBlE1uzW4XJpqoLQZQipHJWSLQ-dtYmnd4kOJy5Qml0yjhPiNABlclrFZjXdZnso2LblFAHlXlwn0PLln0uJpoGmloEVvCTtqg8IsP0pX5N7oNfjMUceBxxwzIxraI50pRPoIQEAuExhmMbw2MLMngzPrPwQEzJBeNyIC69EqwKTAAjwTe3c+CXgqgAM-ZA-KPhMqeBDclAGr2uzyJDM9ICIwACHDAiMvtKJxv7jJjggT6z5sTCOVM8ISK7dyO1C8znjP2rQZgYGajsiq6OUP+rbJdljvdBDm3I4taLLD0L9lA-aNAwmU2WQWR8LdYjJ3Ec150D+gQRyG6QY+nobDL+oWdXvPIJIVtn6ruWXlGORHV9cDI5l+ofrojhTc6QQg4QfYm-JCz8lFGs0hlVuh8+Ft70djIgdmKEAoUHGvGsa2I2lIuu0yESdS4U50XSALMZFOCTIfTrmVh+ORIOL4szhyPaEnyfg0XpAS-CSkPBeG+-m6G-h6YnwWgzySwD0Ra13oT8FC1b2V1jOU3N-InMThWBFMnTdMEPHGqSUNhAVeNVH+VSyetIIu-NFgf1-I6IZK6PCyG0nLj+lbk5TGCPShDbU4QmWdcdO+lhRtRYeTfarn71ia18HQgpPQsKhNAJd2IDoavkeRgzNZ9u1sOVt2lKRIERYCPIKOdHzzjRa+R3StB0wYFHtWGILK0ou3Fi8I3q94aVhellBP01ov5JVlJD0LkDCssVEWodCb6t8RkffdTtEj4LCsmBEafYHJHrqJBoWFkBpowMHCwAIMMSAHNgIOiD8oWy3BSkcncJCE+UKAPdCaAuBUMwA5GT6AbFHyFMAw6GH0MbWPbzRLe1PbIIZwRTxYbMONIvjWnH74AAA8pWiDxTIoMXbfOFsCsiJBsW3oGDh9G3g5Q+2vEbqmtDKjkdIIelVgCxlgqVgxkOOG3gZRmBI5JESQvtJ3CobxkHgHsAGJ4HriagOAd9aCDjnLDkhFwHsdttQmLqVh7sV6d5lvwdDqDC6WkJ9J0ORDugouJvYxulUW64V-8ryKcE702heNlQvjFrrInrQ6I6EkpdJHekfRQUFCcbC+BrAMp3A2sMfP3P8NcwJgrg6eGDNYNPBKFUclVJoUNmFIe9XITLRZucI0TcA8CyBZAFcOfpdZxB8PZZCEUx46Uf+4I4ID8PkrDMcGDXfACDm0Dg4AAa-a2R4Xoiqa2T4EkCZQMgygWoJ+HYFsDiAnAaoHiLRE4An5w4beDbhmB65sRSgvkJSIXx3D-psyNPEvmiKxFBhrg2IcboqCVBOB3uvECngEysSfBqswxElGaGrJ3gzILQQvmTFhgIj3exNBYOUGoDUAPuZLOgC0DBFWivq10NVrwjMhujbREaI8OlFOBQDF0zuGkWOHhHg4Q85jMkX6N+EAtPQW-HFKPTPDj1-2iY30RSLVaohG4gPakBEAEbt1tcG3Oesh1YCclU+ffAep0UhDQhN6NSSzH-hPw+iF0K1eEJcIehHJOWttVsf8QGaalh0j8ZRs1mHFVZZAlya0vzRMrLcOQtHOsDk2ugORaxoLMpJERdyK1h0n8AgHmGIwJlFQGoRcQ8GXGMAKkwUDzO-Rm58sSuqXLcJmGPbLBDOZ4ixD3SiaZJWo5YNpsFBkht4I050C2p8CPH0kNu-kRhuEDPDkZNGATO8TuQfHlgN2tdZAHnV0pR0sepeHKvWEgkOQ2k-tMFMfFcoOcMEioMakmOcINVoGItN4MQkoIahnyi4V8ioN6amw9084DbCrjr6rJu2zkAkD+Qom+iqJ9hMlCLSw4rsqSKYNMD+QfJk4ZwdLL7vWBhql5ieQTHPuzVGZIBjGBcKulmCImyh0uxvf2kwNfF9VMBe6NnAimZSI5xqiyUvBvQ7rYsHQSk8MgZGsqMpmUY1J8OKyzD-ZZ2wsWBN8236QQxgAjGzOvmZB1Qt+0A3ItcRmDvk44VlRpvKCUxKCvkqKLTDmHwCGhBwEGfqg6CYnWhIm9FQrHMlPHvFz6gPBvGtBdi7xYqaYCsb33b7-UWawQTMa8jJzBTfAkQSaio2fynBSQ8AaHr8Oe4P0ni7sBqHVngQLgPiyWVuDVTqmtwdKJWFKQQgn55TIMxSHtFwycoa5ogRFdyVclsQPFPoDwO4I9TTA2VtGhQxTmNk1ob4Zsh0m6gwW4QRtf+kHXaWqPN5Ld22L0ckFQAlzEsnRLDeyejUAS4DJBFnYVKUCTzxBSaBLLWqiJ+mVgvp1zaUmt0oYAEhUpY1AtSAcHwBu+p4bEEkHyyLD4ieOPbKeBuoNFaxKcEBMyk1Q44FMy2GqpjjIR70lB3UO1j4AnTWtA+ImYPlzkGDlg4JxaGaQighlPES8U4VfnXllBlA5g2QpyF8PCqnhyQQYIpr+UaTVlO4j3dQGNNUbOj3p68CQTvDMl6E1iFIaUvRKLGX4pxQBeFuwFAKUzFMriS9G8G6C+Niku8f5EAP6rQgrIfYZlHhM0zZA2a5KUYfhHwATNp4MkICdTLxolBqgxEx4a5FdJlJgMoAp9IABqCNoHwgybHBZQ14J9PYAACkIMyNCbkupGB5APyOGthD7Agz-0JXTuMBgwKuZz6sBN4HEJsjZBEKZHVNmTyLFNyjk2uXqJpJGTZcVgDbSsGmHs44EC8+sicQ-XTgk0s+kMiyvgJn7g4N063N4etWSy8sPSx49FtKSp6YEMaVSbQKrhM6Y0lChpF3qpCNF3hpZ-RJIbkyY6X4ykOeEAdvQal5QEUwgcHBqFpnyF5ShCOnK1Eg68IABh8UgsuzgQpcAmt3H5KIAQDQwsgKbbJHTziRtTN5SyGDOwEO61t+U+rD2iNUtDdAVUBzI5NYnigNDMEbZIKC5PUBMLsEE8dSXpJhI7zqIocvAnvK-lZgtqs89ugvKxzf9FGT3OsNyX5YyCWZUySYX7PvH184YMdSgHAMZDUkyUH5HlESKUGbsEAuoOgMyCRZmz9QFCxVNEG6D2AsQ+AQ4kEAV5vs2wYMhVqJyDp9Ut2PAjiSyxsxDA2inwXwNRAtGmywZewRScvzcm-k4KqinJLc3NoBSEU4sYKWFPkascwewU2KckwvhqtuUVlF+JKETRgBxA72DKfXOYgNAbqd6XHLb24h9CnET8K4KcWHLp8rIB0CzuwAYDqk6AqLS9AiFkpuSTZgVQOhbJDrjovURNJvuyCjmZdTGcudCc6M8D1hs8fbUgaX29apDNyn48+YH3eFJTIeSTRvmB1L6TAEAbzI5c3y+ZTwEclzH-Ej1OWItmQSraKUclin-NZYaytEc+TLFOZAZ+rYGRPGyJqsCkHy45WiLW6pddB7DKeMMJLGAye5BMpwSYNBWzKUZ8yBStUu6F296lewRpYMIb7pJ2uVwH5IdzjldLAEPSpbPwH6VtUeELCi5WQJvIMQu6yEVAotAIq0MXwiQ5EGpT0iQZl2dLdxaCwqHHoBOCUh+ooglTt0uWkCjeWYITGKD26c4G+diqngXzZZ8bN1oYPuTkwsGBEtVVyswLzgpVFuLJNozWZ3CLAWzAqdPI3jQLuIQWbIGxNkp3B-ydoDVJwH4zIzFo+PA6srBMruKH86VSSqarPDxigoWZYqUlGWBizbO7IW9BMmWhtYRGb87lRvypmeIY1i4tVluFgh31XVAFTVncOfliyPIBqmWQwOnm-yb5LxABeaWAXBLmQYC27BAoQGpB7VR0uBcTPRIzLj8UfeCKC1mHjhggZSY-CsC9BhU76K+MMiWzkhY1NaIeT8PwCtbm4go34lDu1E-kBMikq6Y9NuM3b4KzBEkJpeSNS4ISeJ7CW6C0WKTHze+hgRCbEpQifgngZJeochCmSsDd61yN0IvQ0lbTd1Iq+cAwF3lLqhCrAfKUbWdgBEpSdPdMRxn+Zy4fSHU7MVuGNrOqRWG2bUWn0zX4AFA2EWQGjjLUGdBphZGoJqw0QAzZS+CyWLKOyBIhheHsLcAADkoxJxLMBMzhlThsYn4IEtgidT+KoEA+Xvukif7fyROwZblEVTyiRzOQWYVNZfNnXAcH5McvWkwglLDlkAjeQWol3t72J7ixwSQqBkM6wD9+Wi7yIii-qeA+cCJeBM5gbqTAZ2UkESSOt+i4aEAdrOTS6T6rVs8ZZyP9PpiUEpqp4OUWXP8g+F3AZldC6eU-jQiyd0Uf+a2WxJcGaYvkHALgBrEwxVl08Hg8CONHWzQwcNtwadqupmCJ9vwe6V5BGDB6tSN5IWpZDikYEIpoY9muvNHEMDP9Zkn4PTVOH7R2tjhtjNEkkHOiYK44pG9iDcPVRRVtU-E9eegpG3YK+xueWNRet-JAqMtd8KUtksuAfMhZb-fdiugK4s1XBGiK8HzWSXZZI04tHHEIFhxUxi021NTYiCFXutqSDoeujZC5r7gQ+nG0yJCLRzY0NcleWKnGQkIaqpFi6H-k+C2BYKxtWQOxUiH7nT8VCRyTTd1vCW99yepVEaMK1AQJIrlT4OgergyYJJ9WmpFbd1ku0h1vWLcT9njmpIrNL8jArQBXl03ab2IvWy5OXFLXRLTRn2gVJVSmamRbpxdRcl1rZ2lBetv3aef2i4h55KAvUPdJQL-TDbIAo21Nr0I1ZqpXWU-PaCeNp4q6YdD-aNRWH7QvIc0GO0hLjV9x4r9uxQfprilSCUEA+Fa87VDsdQaCpSRXR4HeFqqJQ8CcyScbH191gIlIM8etFwWQQXY5I7le7S6lN0P4HFzKniDOHj39VsIO0L+JrNkqfQhqCKRVPqwz7EpZQ5493LLApUIoeQW4dDXm2nnskCOQ4JpjhP7j6stwItBHJaieBShW6Se4PZXlEEnBlgMu1cqmGNi5hUhZuqcBw1H4A7q87wQWgdH+jIBtA1MEJQzAklILM+0UqjnKTxZkpWsHsW1va3ynC6iNwwE5AfNFqQlsRIezbNKVo7L6V0LC+fewOIY+hudRuUhBGFyhCoexVMLfM9jS099nd8FbEvISBV5iU8hlLnHYRcGwVIgunAVHulR3ab1tCQNpENowWq6FtxuvRZNKfjVgO5c6JddhARR4Q4CWa4VGhOLTw1tskigtYzvxFWZWxgarMCKokhBA6AYA0yfpP0WX5EAi6e8HoPLXvyB+zEt5JYq0StAaFWk03vKnazC1dlCiu8BNrHHRUn0r3OwOiPkM5JFDkqN2TauPRBFwpJnY2nfzA0PRJwRVYTIDQ1AXBqh8gHfknCQpkB5+xvCWR8Q4LlcT6qkWwLgg2AMAqKMSyosqxM1KZqSRyfXIdSW6nb0hL0AtV6v7ZLMjpBPf1WnQ+m2hAjKi4I+O0ZAaoa4AqKirRP+5ZtIM+tS0Mi3yCgIz5dzLNTkuLQ0Y7hvQA0aCniVPYnU-ap9M+2bwHSsgDm0DLwlX6aa7wieGPYlgaMu8zAkXDaNjEQViztGGchpCgwrYmHKCz4kdPYni1RV-17iGLP3LRqWtEQYlBVQQq5kZJ9FoEZqVcR1XOEsGdLJgZVhJEXqtAGjP-M9npDFAmGcUsEj-SApRUVgDwPmKItnpFEQCC2V2RwosHts2kchx+CZTME7r7y7YPGbuonh2GK9yFUPjUFcMbQHQcYOaO2SRNexOWvMS6GYoJFcwb27fMfrqoYB0tRC4hJgXcfMUkUs1-6Nah8f4Ibz1VzXTVRQEyMzpPJZ8oI+wioq2RTwz7fTUpTyq9Rel1R9I0dKRYymqjwtVo2QH5MRoUWypjmTaTQgUcJIUrDJKqf6oxt3+99HYyJ34TWSXiKy8WPZGUC6nFofm1afkLSnQ8pxZhifQPCorX9z8NJpJoa0vi08jTeS7WsTnhJh41cO4d04IU9MmpUFtQ39six5M5jnT6xn6LKEelb4PTRup5iCDsFHtge9oAM7UdGMf0aRMmLIDMBnj54zMGMEmBqFe72AmjaoQVZIxx5g6rw+eo-GQAjAFArsrAb033wSj1taTPEZACtCtGghE6FXRaKhtq6QqU1S4UaVXyVNosA1iYQc+32HNFNmGwvZLvknFN3BJTIM9IMutNhZhszOI6TDxrkxIL95SZUs8yx1HBBva73aE9JFhM6Hdyn0BEz0YtCal3EqJoFDUPFj96kA2JoiLieegEmLQRJxdCSeJ4GTCR353eAMeZCxDmTDhKSMYtMXMh19wp71MSC-BdULjPp6kzcdHNkmNJDx2fQZJeNsn3j2OECZDr0UVqaefTCIOqYqOymFDcimARotM0fZDFOFhCpQSYGbmrjw1FtOJGLNxKtuw+IrKGdKxpmIzbprMzGZzNxnijahsdCOyTOqi7xqZ0nOmbUtfank5hxLvmaQKFmZkslkYyyLGPlnpIfA-LDWciDCB6zp7O4U2fe6ywNokARwYxeTOdm1C3Z3s82FhMSWa8ZC0c4kD3N9Ic8EpsHRhEbgrrxUQUS81vkBK3nBFATey7kugp0bLV+ogxjIeMbca5sHCoM-JelI3DdJbDI6QZJVM1X8yfVHRLEfWIO6NgAI8aKebSsXmNLiMLfLlceRAbHRn1bk6UDnEjxsQR0I8I0RbXPEL9NYaWpcu26Gdq1rY3hIeAYiF0JVDQkaITTOOnzGrFDaeD2ZsT9nQmDFOZGUFQ1I7Rz81v5gbrV1DXZZrTJUsCEN1vX2IZFxNd1amCOQhlJx0ZUquqQC7HmpQQ-bzPdnUxplsmt4FhABaT9lJzg0prULzXf4UAL8OtlrPhsH7F0-aviffOxqIQdUx2gpJSQdrwayZCoQBACaKD6sr5Sm7GlmBQlXbHOYxl9BDK-LYgmNIlI0wsYvVYzj6B5C9eI3-GA1YVx3ERnOFpKuTz908fWp6hM7WJv1AIWOvUM3gSo2CtNw2jXAUCeAmKIfZyrYJDL6Vz+vlTTIvtDIvyNMdihxS7mFMS2YD3EvBrN0sYojEjaIjZQbmil7KVwidItS7wsDqIhyn1MwfVWxktZl+RUlie0LdJGIeIjsxus7LBPWFwCL2hkMDHdzt0igLweylc0+C2zJJiGg9HumiMwiyd8R2KnjyCgpGieIMz+nWPb640rgVUI3Ad2ZBey9MnAYkILH1BOb4QjmIuuWE4VTwS7T6E9UBUo0c0P0NaZYGjOnlhRljYPRIJjcy6SU+5HEYOQOjJBSr+xEOicFvW0586TUE184-IHcRL3E7r6fERpP6l2Yc7InJ1IAgHuygh7WEKoqPY27fsWrE9wsfwCyj6Z52PEFe3WF87ym4NjqVVqciC2myCRMcMaxphsz-X2QBePq+eYGMaWrzM2Sax-OQXJaNE0dg7P-YJ27AidzErWdyiSmfC26OR9NeroubwU6oCnGDMgclP9aYuuxViyIbllWY0uwyY3hoe6AvziQEyKMigBAXsUfJhqjVRxfZoxzaegfI5KEfgE6LOMSAxh9gkEq3F2xv5KHOPAzMAF-87qWkWNgVSqVwTH6xxSkQ6N+bFVIOFSgdIxgOZ6oTkb1Mo74sSFkuoGWLIYCUj3ReBVZnmfAjt2vQsgdUUBMJgxbDKVydoCzjKHTxrYLEsHLx2I2sMtZKAyT-ppWLKMuPNTa5tI1DrXVGmyt9HLo2Ij-N9GVhGV66IQXKDhdlgOxXhK90mMhj5N8j+WeUCVlNBAAKAR-3Yw-UnaNGAZB4acoDAUHBt06fsQVMlTXqVKFPB9ONr18mYolh4Ie64eD9jqihclz2conTQwQ8Y6jPlGex0i4IJ+uCCVATpWQcjZtbt5KzzBx6SHJwFKqHzqC80HqPJAhwnHkLbCLQD+VXD3qnnZSZMOwE4AldHWGe-aZcrDwMaWa16l6F2upwSptOSU49nSxFr+KyGoLae+txzGt3WUbmRYSfgv56E4OlaLeK6bJeLQsWsQJINkMv0gIjAlySVXBZlU86HwDLzcQKfUJBBVbWRvcjg4eh3Wc9D12fhZ3xti1FntooKAcExyUjhnwJ4AksAAQUyM70qNvvS8Zd1pSQicQZmc4NkyLeT5BjPJWCGpeRi0O+pkONmojpIdZeOyCO6DQDC3W4mGG8+ATMjaXO4aYW2OLGazPAuo8QBIKnlYCyvrIeQvbPbubUx12wpwaKEFyvCA8j4ljh1avM+DMu1D8z7x4LLEywLr9lefkr+nJFKB3EY65bTgWILf5HoYaIKMMOc5H1l+y8w2STBmelBvMvCREkGEuSPOs6Rh5E-ujFiQQ3+PrNVzZHcQV1XFtnNbdxOwtRBcLj9Qa1qI0jldiTDEBJzxCwk6agXeunZWxaUoKP8K7fKBvxHUQxBPwEefUKJCrhlBvWTDtSGezuAiR2g3QQ5BZwKBlRO6-4wK6gDaTZDhXoGV22ZtLS-JhVtyXjJI+2iNAn4QHx9JCIo1vGLQleSppB8KqEnRqJIpvuXDjtSFf0OtUypjizzhRgXQg7V4MBvrTCSYswrfkjyKBgC3gz2DWfW0C77YpSV4bQBPl5bYDwqwLqjiKrKQcGBXL95VWs+1dcPtJaJcuFqFLEG0HoRkvsi73sC+NeE9gdRGnMJBjqXJkS-I7KrhnRBy4VmeLvpe7fFv44Ah7YTp+iVgwNTlRop4VRk99MNwEFpAExq3yGfZPU4dkaglbhQUbJ1xxbTOfu2GFtAioRoOIDqAYgSc5WKijRp4fS8RD3G70MPJXSizpIN86gIjC667rMwvCCL-vlGyuq1AqkzVqoem20ZsQSnuoRkkFPu9VHDn+gQPpWy2bokgm-AIABwCZt3WEueGjZFGTyCK9OoRkpuD2b-5zGEAC4BJcTmEHQm53QXw-ZaGOX53PjnpKDSMtgTDawPYnguLHOnVjRDUa6hCfuc9Ig0wUUWTRPEwf27sH9-H62JhGsDmNo-tHdYc+azSzRv93v2sIe5VXyRPwixTfOqooTMTnZlvNsWcYxIjCQS3hr-9p9B4Zqod2y-DQYge6Vl++PMRCL2iD0GIc-ntAviwuiEtin2fKussCeswD6vqB1i315a3wKtXVkZQVKelFdFoQnK-d4zChCXQo7Cyk7Ux+qiBcSWDPpsWXiLxyP2IgxYYvUDGLhut+AudL5l8sKN462V+FkFmDy8aRL3soafM6nKrZBshGQZ8le+cBOA6WpECLbJsh-GfqQThgEUe7HvxsxUe6aX7sFl-QN+fzoZnyIdF-E5xfSxKXfZpxzLBYvbv7lYl6-SNipXBXDyIAshBCfQ-+qN45QFIQlRazcAfE+vlfElCF00f2L9J83g5d849X837wjdgzL6gPsJIG+9ZgwBMAEeNLdoHE+nDUEagRORgl5-6S8EfNZQ0I42hHQqk03UXcBm5qZ94PlTmbIMetyll2s02qcSpjRMgXIIr3JUOola6fAZ-DhjhBgVAzb697eiMAM58SCj2KHcMbILID2ygWG4it2w4OD0K8JrdASE2GJge6Gu+CG0IJ5txKBFe93IhoBLp1YAbREgWck9GAISQOcpMYFyi4EXIABT6E4AVyE8FXKWgNcmAB1y6YJwCNyiVGcYXuahu3Lo+wDN3Jn+ptNtADy7IMBIW6QQKPLFgqIDuCLARNOWDRshbNtCxicEI6JAW9hriwDI1CBaou8C-p4DnE1ZO5Ykwtiq4aFSFFKBhUWekscZIWaZFeBDs6hl4zLASoJ4BmAZgJ4DPyEkBYC9AN1JV4qeFgDia38QgdQhIs+fg9DYuDiH3bNg2yk074AGgUFCqe2gW4JiGwgSIz7OdiJ3BGB+JJIFmB3lmYBlAtir-4TQCHCXJAB+cgiCFyppv4GVg5cpXJIASANXLgwCAaigNySPM3L2QaCOLCYBljtEBdyxjgnKwiBAa6pJ0EkgZhb848hQFg81HjQEu4donGKNqm7sBar+RnPbTsBWxJwHJA8urWYeW+AGpAAAZCaRNAAgcXb5G-MidZtqfFpDCacespWYD+sqprauBpgaOiVg5gb+CeAVgJ4DdAN1L0A2BJPN9SsArYBFQSBMwdIE-YywD4yQBTgOsHZKLcHJa7ad8K6joi9phTQWcSllF4mYqlpmZmWmVlOC7BUgRJDmB9gIJASQTZr-5JSOHqBgfB2yq-RR440HM6BwWMh1g6gGMELDugAABobQD-u+ory1MH9Qf8llLzIAy2Yp9AtiN+jOYuEwRDm6z6V4IwiayqonMgVQ3vM76fAKdqCbqum-CCGzBz5u0EqgPtDgjAcDEGeoiUZ1gzqS4+NG0LzQr3L+AqgaoGVZfAVfhrSO8HjMRCOUHfPHIvixAdTZegXTFkgKMa8hp7K27Ek8C3QyRM5LkBNmOmwzSb0siTmoNVp9DFI50Jm52O4RMvAbQbMDyCi46Wr4REQrnmZbZW82BtBOwu9sqT4BJsBwrV05XC3KpsSbLBg5BqbORhMs08kvqTmkuOEIbww9rJTVEXoVeISQW7EjxdcmoQsSJhNKimFBc7dFnKlIjutdgF20drF5L4ijBhxTgGUBKFnsUluwo-QZSlKK6ojPrRppcWruXAiq1Jo8hcKDVjwYoWUkiB5aYMojCBwgNKiiBQgIxBiCHIRNIAjlgsYRn6HswQBkT+ixKMyB+gKDIeRU+p4ORi3uZuI-A+kGoOsL6gPKFpADcWarA60UK2FA7LoDjtmBIgP5NiyOB0TjFTF2RiipxpaBPgHTxO-UveEq+DQcaQWAZQD7R2KTGOrZo4OqsMYHh0tFyR4WffM7ZzoP9OCjFcraHh6L2BbDuIsUyokaFyUd-pagu0jYOLDlwPUhPJJwoCC3hAkrAEV5TgkmLHyZgXhHy7aMyiu5oUYAbJBAxuwzioD+Gs+IijUYNIo0C0KywMsI7oioCeGz6mYN6hB0avuCEpwDaJLhFaX4HWAiKioJBoO4XYb5DmQ1tvfy4O3eqQhfS6eoxGLgGhHcFooZVnnCZgeQAxZIeeBEZI7AHWK9xOAKwexh+4DER-jGR1KoEg-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-4bSqd4ewOKscDlmCbrUngEGoCdBgIRSB-7cqLQkKE8iTcELA4J8OuCiSgIMhHRSp5uBWK643XG2EGo2iSul2cdUNxC90EQEcac0y3LJqhq4GvSDYg2QipChw4cIDTrJigSKLLpKOB2R5S9CLzrAZHsBPBVprkFuBBCsoBkEDm6EeH5JYLIUNQxQwcKI4wZEXKpBxI1JO1xBKABFfE-m1ALST2cHwJfhyCDoFolGoKOAco8Y-yUXZb+UqhPD+0ZQA0A2SQUJNo-csqRXCqQEGdkBmAOxOe7qYkeOslqQnGYhkJ44QLlBIpMmW7ybpzYNukAY7EJ-AMQrQKI5KZMkW0BLJWvkJBPuFcApl0seqRxqC6pQFxk6JdICyY5CmquUDugWoMrLOJ7uJYTUgsDFMlIAdUSgwbcikYs6ra0AK5gngTuCcQZ08fPTIu41EmShYQx8Ot6DYEuLCrHJ6+oBraW0EUPSqSDhAbCRG5GERgVIlbn2jkYiAGPgvI+UnByYhvnPwhpaeYrFmWgTNOoAcQNEbmbcSb2ngGbCVIQkmxKNLrvhIAsckNykIcGTjBda8FmTgagGvoIKfQ74KfxRAngFqBKEH8ar6oMWYNjCUaOQouBNyMQDlBeU-2HSi3qeqXRmYAs0oc7NQEQAxqWIeIuCCsgDSXvB50lYAbAAA2hcCwArAAAC6ETmPY0iyYDSBEOuUAVzbKQUUFBHhNIoeBXUmfIzH94niPOncSrbDG67hFSMgkaQrWe3CSmQyNMaKhhqKUBGoG8HcT9G-itSQNJ2eAgBHe7iDoLVWlwW0awOsbkvSQ08DnE7YYRELHLJxmtGZTQg1rmwi06N6lsrCMykC2EHQlaKhBKQCtinxDBlPj2F0qsjAIxjBbOetR7CTIPly7GvGD8A9W2DNzlLRpYNDkzynSndqoqLIWjIXKcyGmAMA3ELe6l8mcnfx5cyAE0AbQiekVDHyfpBulDApuaYml8pdB9irwH4F7BXAFAJHx7s-KecFUciiPG636YKGtYKWPpv7JBR04q1RRKvnLOCVCMGD6lIyLFhohBEfqWwgoajxv-G-k6+tFLtcuOlU57osIFO7vmrqRibz2xAq2D5xtWOmgC4n5tuJNUB3NSQaga2JCDzQ6aUfwgAGBvNrgQR4ORgB6hgmrhN5o4J4gjsWXqdwfOVHKCRhkM6EaYsR9LHpKqOrjvqz2gjWJ2k2yjwM2wusQMcXyak2uodqoCnvFBGX430MGQi0sGhqDPiYCJl6D+ccD6b3h8AdSL2YGQDoSK5ecSAnpxfLsLjXebyDVpJ5QQPOEPqwRuVL9xX5P-QVG29KB5mQLImil4EUKvjI0Ab+RGnCAkvmCBFsF1LY5AEeKJ3Cbhz-D+bJZDBvAg-kL4Yc7oyc7vjScA2OfKjti42rKFbQ0YEi5cEOLnaqw0XXOe556QgFAZRw+AL0DyxaHvva7Ad4FJAPI3DFAUUYEuMWl4UzWG9kMFT1uAoLOdeFoS6UsCKdBu03oZt7SFdoIZrEozYSDKZgX0vAT2sfIFCD4cR6LbA3yRzpJAaFi1tOylpJMLNHVJqIIPmyIeDDHCJAUQR87Qo76sZ6yqGOa3QdCH5qViroaRIbjBuqAVFl14HRPVDCA55lZK8wIqNA7UxyiVWZAca-ACm+gyJrdFM0oufsLRFEaNvAP4x3ggZ5IfoY6paG0xJBDg0hqEMbpKXaCUjSmILE+lR06MlMEEFpLMLyOoGIkO5dF7UJ4p6sqkbOAzgYAnopEc9NPHBoc3EB3lZuYSfi7WIU2skrD8utF3CXgH7FSLc5LrryiFMeSOmw7UXHlXyP+LbjNqEgDsS-I9ZA-sxRHMUjsEp9gq6AQAJBSoL4bRg3AOzlTCopJwABg59Elw3ZlrjMCWwT8InxOcpjtNpbU3kLkwMgDQNjAAAJJMa2A7gLYCYlrLgkyBgriO3xLqw-MgVQiB2cKjuZrYmjzT+eUp0k-0soF0HqQUADTDIAyMDfzpIQQvSrpIBsJQBXc+ALN6bcvxSfiMelZl5GyFsWiyXaRQhDd6Z8dxbnHMszxQ8VmWh4FM4oAUgPJDWyyhXxjdeUwfmS8YjmA3ipAZ4DB6T00KpiwBmdtl5GtpxsuRh5gM4JIawgehE+KsgyBEIR3gKOvWg9C46uLFtAvhpgjSxGOuRKfQSJaDHGFY5m6Xn8sqsiX2AZgNICiOPpT+ppiZQWjg6AgWcOTgaq6IPauFcubApLFJck6XBl4JObycMosJIqpBrmAAYQujyPpkK6gKCoXpuyKd6QHoI5OhzHOgOvzp9WOEGQaCk+UmUAn6OUt7r+K8WFmA88IXkJTnqTMUchci1+rujS4rECyFocC6KNSX+gUIxnVsXIh0TFcqWBqAUpkzhCJ1u2Mg24xOGKQVEYRr+tlzlBbYruBRpFhE-BixXiB1ycOgLD1gRAT8Nk5SMs5WLYJllHEYUfq7fMSo44P9k6KMyNYBPjvA1nvhnkoGyCyQqwNIBiZG07SX5LbSfIEWXVwSXNhD9JVHtOYB8f+NcRg+-bHvTcIIwYcnNSlaNCARhzKFnQp5Tifw5LIX0iaYW+YCAqhO+res5gmw5uGADYEWOHgTw5XlLwgmgmAlIpGuuFbA6aEvSXTp30+ZCRqaWSaEtrZqCIhKwP0c2lgaw6hisSg2GIjNuYF6rECfBfqBUV-xEuH7gmDW4pQEqyfQ5aOkjRxdUPD74B7Sf7pTwpbImYPQXnogByV6Ib6BjA0BUmBH+UpGDCdFGYZrK5FphGIiqJBeApWG6uDjslPoFVlOBqQzoeph2uxXsW5e5ZrueUyJV2AmblJKovT7g+kuLujQACgGPhvA0NvAg8IwrFqmpMS5b4FV+pWhUWgKThHlW6gZyHFBhEKgg+Q0RwrH2C8478Tb43F2IJpBJSXWUmBUwtuRhFuprRd8lconwMlDtqsNMmaJABsIyojONTPWSyo47r0ofANKjunOILhfCW227IgTS7wX0seAriSZahnHa3SfayGVXcYgrWC5zEciY2AQv9wX0j9tSROOOscgg+qqfoF6WE7pCgKdhsiGuSUAvSE5zXgB2bXwRFd6lcjDE-tncoSOVAHQKJE0FGSDLQ3-EIYGc6fgiI9VEfPgAAAWttj9oFAF1DNFkIhgJplyKBOoGw7VWyBMoBIfaxgCJonzwsU8WYRhBQ4NCTW-kEJRZBPAioN5jphOOFCHIFwadjDdizsFkURUl3NeD8qB7CRCaJtUlkX-uOkfvRXEWSTxDgQehHFj26PCXSAUcE8BenLuuQlegkFFIOcFBRN2nD7UYi0JjBZi6eLFQg0FkAwA5V3+l8AIBwxNjD4ao+jlIHUccoLD-lQcnxFXOoNM7VaIdAI0gKERWkw6d8HiOcXE85cDmyVFkzr+Q6cjxdED8JM6R1q8hlfO8DEG7ZdWWYwwZbXw+CUQbzlAkRiWrm9kC-LYwxy+9l7Cd+e+M4TzyiIBa5UAkRWtLjYmMPxHVBE4DpXqe+FFyoEu+qc2TCsKtZcVL0fmCxUY+eFWq5mkF0BsADcauD9pTWteB7Bk68Vsu5lwsiKMBwQO2i3zWozrKhRnOWAAOHx4gTuPVk48rogAjMftOrKVcPmJ3C6gX1abg1wo6KBUgM+DFhVXEvUZnmeAjSNnXOlR0rlA+5lXDHRAVqGYqph+Cwra7JGtuEIrwBKsdGj+C5DCUCf86jCjn7Q7ZujrtkyDKHkMQPbOCxJcHhOlYRuV6CvbLe1CGzhnQfbIBXj43athpEZz7FKBMOW4CfFnah-i9DAcNAB+73cZ3KgG0CK6vhV+lNxKM660J1ZeDxy1bE1D6gYTuu7LKzOl5Dqk-yQlQXZfqTyB4M3khT6xKt9U+igu9Ka2JbgDRQLEzgA5aHLlA4WvMVHgdKcYZlFwBqNnLA54nDHZ5sCDBjRSiALepduLxkJWBIdikkAHksENGTOE+UiKqoI6HF6TZIwHEVCr2wcnoHjxBIJCXtGGsBI1FQN1BXlE1PoC+VCNccnNDlw4DrJB4Nafi8BBRtiQMy0VvKW8B8xYOkOzUAWRJjAqwAMJOxTZI3O0BqB-0hQxkJk0Z7VO42LGyUKNX9Ue7-1yCD46CaJnEOkfO-kn6B9gSANoySq2yZe6eU9CL1LNKQgqCCZ1pBtg2NC42XmA25-SRtwQlUJTMCZNJ5cpJpFarB1CJy8Zg3wZkdXEDANgXrJNKU1iwtK7aFIUnnbfgarDoqpF55hnzLA3ZVdW542QtFCa8kkEMTE4n0Br6yghxJQAmFyAHrJSpXoj-AceHuIfnYwQ7I7D2JWwSmmkAcYGhWBhhaHXjkYxkbsK8xycuboI4jRWoaniejgSSzmz2cdJChGjlVSygR0EdAgQOQFZBq8gkNjCwQEyJ3CT8T0Ff6RBdEFZgdEOVdoDc8siJlAomzIGy1UQErEk0LxtuMWhdosgHEImgR4Cbg25TzfUmyIuzVUrCFGtIBQtN3WEiaTN2uAkiPUJTRE2HlbQq43+MCIg-iegxILtj55EfKk3xpD0AbABFgUifggY2CK2RCAuofWBPwYIE-DO4z-Gu7xNW1dnSJACKKS6YmTzJTmrkADOqWxothPTrgeqePhrblqTWDXqNCWbrGLeZzr61NKGdPHKuEWagwpL0B8a3jxcSCRtB5A50PH4rsDYBUYX6OuRAAd2VZa0C-g0AV3Ga5-5eMCFAvSAenLYX0mgKhFuHrjDW4GhuogzS7kBl4yFgDonJ84-Sa3CehfGqCWN1O9qmxBl+2IVZylbwK2rtku+Sx6jW3NnjR9tyXOwpTIUkMOoAoILvw1CFCrCc0wCLPNMR28vbd9yRAjYdeJrY1kqlwQKekGrjPF+3qqII6JVGISWEEyFsEyaHsGA0Jsbrtcq3KDHAO3gI4nHB3wUjBapzfCrzDvQiadUo9S8YHkEsB7RSLjJCmV3eCb7PAT8GTBoSDyB-YfhTBd1BZ4kipakON6VQqz4It9FR4KFq+Rohlig9U6Io1ZQvB3TKzKsBUOOTfLCBpgf7fWAAd8diDL82FALlAJI0IKtR1SBqLxWmZKFIShciT8OXBCqCYEUj+KV1lDYdZm6rtkoEKAOunlAPZUOWKgenfwAGdj8C0AtFhWQo1JO5IsZ1wIu2Z2UR+s0rOrk5eBCG5d6kuEaUrYrWShxW1Fyn9kzgIqG3kqwT3v-irKIwrJp9qG9X+40i-CkpBrwzHPHJ-1iUDIVm4CdjlWp4ScolDEStfGsak4iiibC0ILwF642mTrsYKYw0YIvhIA+GNIBOVOIPljUAWYPYxw+gNKTJ8ucEPQQEaGsCeA1YjXS3BsOFUbBDOEfoDiC3agNMcYswTKMiAOiZ+GgCJ0YbjghfRLOvtxJRX8BMiqAT8JAAEaeNE1wqCmBV2ofN94frH4ATGq5C8ISJfvjXkCYE8AtAzWLWSVcV8bxVfazCsUqfQ6ekHIye2SD6AISLwNKUc2ZEmhHYwROVIXgIPZTTBNaC6nwIGYbWIfGA04LJWC+QiAAtK5MXqKYUqCLmNV2dGUZAqg-IzWLeXIOQViagjUtQl2G54XFS7jjViqjHlRBePb44DwEwt3GWSudrFScRb0IxAiMtLZchxYmbEEmmKaPSOq0dqnKxV9gNADgqoRzEYZB6oE0Hj7ttQSI4DQBKkGpBQp9mbpA-5zyeJBP1YLU9RCwAsfEgkgjpulXm6cyUp0aZJCinz2Eb6C3QpE+pcKyWFVkMsqogjvRcpblqgBCKxtzheQgWJTJG+EclFSFYC9AnbRkgbAOlbZjyFccRtwdAUae71KQMBMThKcAsbwj6MUfdxEqEafZYQB96MlOJOJ2jvhBWl4gl+ko4Iqh03DkYfjQFg5u9WSDVheBHAngEK9F+X0y5PItLRdFGJEQwVQ6K-Gid7DEZlZABbV6y7keSWXVjMXwOEmOi9zGzLnVHsPJ5EQhoH2Us8qWLAr5Y3yOoBFODivECsA9YexrGCSfgjKq9MGNZ3BALMCzAgQZQHOUYc4sMB2pAqYCrKt2yfmghttLidAyaQtJNjCNw1bCi0uRL8KkCoQDIExrZCbaMsQVtvdqhbv2fCGAC7AEJMHDa9ewqIV01TfO9rMgBsINjWJa1Bmm-9-AP-0eIc9LS5Sk-itTC5lUyCU0awr3N0BeBLQGSg4ox0cShcQZbJnwqN4tsXW8ph3DPlECtsE75uSN1HBJDCc9Lm1q5PGBO7lqCuUoZXd3rqc3MoOKMVlwNheWPT2IK0fhScCx6IQkj6LuLXwk+ydlQVyZrvGHCAc2YqJANNF-URlFh4sb+CSxDaOxBo8hoKVSkIcwPvhV6rzBiY-CtrlSBEUWtmtQW0DjKkwYZTchgMJ50pFuBodbWeKhgAsvcIS1+MctkD82AYE8nypVQuiYyCtImlqWohHrJTWFbDX2I71LMI2AFoMQJEA1qDMA6A5AtvA7Bl4fsI05Ma2MEkAxAvsC0DUSWvLIg2CLIfPL3Mc9UWw8QOQO6DYwdQNLwrklWOC7pa42bHLhwe6GYN0sx6XL0kwzmZDbZAbmSukRAlWNkLeZdtMmWKiLmFyjCxx0HtinpSIIOBF0HmlCJ-GAAMXKo6iFLGmQUZR21gYasX2AtATFZQWVW84WGA+xeplKR4IWDEFlgpf9dPBKA2iTIJCAx+U9QBQjmBc0zAFgF8UYlmJbFBnwTVSZ5zDX+MiAnDWkK4gwYShKSBttVg1CLQKNmOPl-FFw20BwAzlRx188fmYnaH5yeR724YB1oq5kDJMGsRQxoGLXxHQ++McbOWSYWUkp4J+H5k4J7oDEBPwCmQ4TqFchLdiXt5XMl3pD7cr3Bt+PZFjk-5FmckMOZyQLXhSgURZRqpN7oIyQzMQUCzCV+1fpwCQQISNm2plILOV2bwrHukhfS6jcSV-60CLngJAtJLtLv53uOrJMIOEtd02WMcvqPXh8HjAa-ksXmHqpgO-X3Eug0gILWSQ1oBnWkIFA3eAhI3+pYgOY0ZNUiyeVIErip4pBjoWKquQ4B2I5zIFcCiErTATDg2iYwfEdYeWQ-R6jTqA3joxb4Syr7QVUFVbmt+9Lni85WgCtRRur2DuAPKXXJyJYItAK6jgex1Qo0xVjolam3IsUrqBN9zzS8DnSB+c-ERAyom8hSQTuLQFgh9+Ji4XShw0db6VDMU3KTj4OHaTxyECYnJEt65fNCwgA3qUAbj0YlQR34M+BMMJDblMkNCingHqNojoovRDRAW4FqCNg0QIUNdQy2AihTOQWXp5SKbKiDIrDPGVKQvK5BJPbFte3jJ2wqmYI6GdG1xHXrS4kTp3hKsdYzUxgdkyBsReFOwKcnGDqydCkQpdLHBPsQYCV-g2YijT+kvFWY8rjijFfVUx-FvmVqAsw2IO7nNjP9dTY8g7LI2yx27MZtXUe2LFx07ej1FngNCi-VMj3hSRZd4sKxBueaU9FSVKZeFW0CRXiugwKV70cmoRoyl8DOkyaw9MCbYHWgxaAJwbBIykq44C-smNBXoGfUEBwAwDnWljsHSjwU-Qy+L8nY078FdZvAYQNmhxwb6jnVTIxgNnS2THtr+HdeOSV7BgWzchC7uQNmDIFyZDSOcwpNKZYgqVj-4tnS15aNFWjRtJqQKbDc7E00xkkPntN2tu2xQVNZAYlJc5N8fPRFlFQk3sOob0UDoXCJYDPFim545cKa23OyINJUxGFiWNh3gB1f0mceGsH+IbjQsERSagiLhePVFhk-PE3F63s-At0rYHgwdF0WHey2w6SgTyERGWIhDahUAOKBVUtnNURoRtaQZiKS4I6eKz9A7TZq+QTRQPwq54sEpKx0x5QNTQyxivfpoRuk4jq5JzDM8mUY0ML63ytTrZ8BHQcYxgCNwiwNIBoRF-Z4BIgVwIjAmoq-dwD9lhtkJD7QN1OpC0A+pZrnlAIQEiCGgSIOpBOQ9dC5ypYrdVGZ5jYnUIzvTqBBwSgaDWdVOY6vMHLmQA+WItCXYb0y5Kjk33HBGksUAFeGi5NTXW26ZngIM3Pj79HHVkojgxOLt8VsvI0aN12tiEdGx6ksZ32gmSChqVZHS9M6VbwCxDQMCCdKH3cWVh67YIVovRDdqSILANclwMKfS2DwQY2LkEBCQtbW+W-lxKS4BvZu6005YNOOkMP0E3LBksZaUAQg5BHBk2Z6yYJA5MFENRMLBhoieNxVfjuriayKtpcjfjp6UClTgdEwCBzAWoIcio5L0DnIWA9gGpC3DsMghylA63QoDXkqWFuCDTmfNs2dGIWaVRSJBqtc33MngwmxUgydRFbP8W4PmjiwLdJOwrJEVsnMq88FpYPbJwAdIC+Mkc9kBbg3pMLPSkpCT8ybjTtm2nHGSJZ-UR8KlRLlVY6HHoRezIsZA4+Ahg0cGGgCAKMDTzMmSnM29yw3b1o4SuCCB0g1lD8B+zXbhu5tlSzY0yFwtoKjPug+6M9M3UYfi-Rj0jrrigeQPPdMWWszQs+RJIupUFnXjaHmzlkhKwErXqpsgCeoxgFI19Clj8YyTBedEhAlC1C9WRPjIJecBxqZsQxg4TDq4Nt5hGSmkLdi0+x5odDyD0yZ1GWJV1ulk4jU4nlMflI1LhF6TuSSDIGwJ0GdAXQtcO0mEYbII4oyQvuJca-M7UcvjVYR0n-MUYrQ7njvIF0AhyBpCRk3y1mTFKs2DJ0Y9iD+SGoFqC2w44A7CNM-yTpl2LKEPbDdZynVkVF+smiCngp0GRHC69j8c0qGN-EJROPzzybpjRSXyfzNJGBrGfCOMRSpDJwss+oVPcqhad9ouZB6pu0ulHSnq4ygG+pfheFWoL2MBy44zlOkI3mDKXTymk9xDHaEYIdbRA06hrNXQkI58ZD+E1B2Yz4T8E0veY3lTtJIVS4xnT8LneV5UaD+shUb8VfBLmDWeIOhcgxjQ5AdUMdqsB7FVmeS7AQ61WJvgA4Jg4HjrdZFtd73BAni-qCcq1zb4vBwGkNLMzZNEDhDwG5rmrB-p2oDcu0+Paj4sgo2QP4vTDzgFGVauVkXrbzQaAJwC9azDBuzGABeE+Kip7EOGnstAcJ1w6ZmE-XMciwvqqLmhQsv7TBwgkLU32ZVcD3JXFXXrWVK+jwBTgP4OoGIiVYcGckAnkiwxOilAdDFOCYTdCuILGWeMYuWKMYwI4pzgMuVHRTWZTrEsakr4q1Nx1sacKm8QpBKnCZeapLwh3F3YYHAvQo3WemYEKmG+iudiujUH++DQJVheFEqUbLylyZkjy1tWasa1Fj76QL4FJ7EPSYH+gAyM2BgOPIKjPIuDmtFMaIQP5nYuSkzSJ2LsOFJCCgPiFDZfNIopQDVQnq6-PJ+cNYkty1FlsmZ1AD9YGDFCHq-qhLZicgLFmJE00hWf27Uhe5Zi8kmyh+V5nCORFdfcu-CvO1EBsvP03JfeHyuhqTiW7guLNc2XxX0MlCszRiaiEXVI5DVju8GZMmD6g5ayZ55gvE9kINAMQLKnreKy-7MpDdaLQFo8AfkL4s+Mxiq7OyIxHMDYwtorngqYu7bjaRJ5wCS4OTlpVP0SeecIcT3zuXUnJnK2i-XC52Rkvvjxz4Mzi419b6FzqqAtBqUiuamYBHI5dV9ZjDp4Dyr-UHrV9dTqs90DD4xly2Oet2IAX7kI7PyU86YPtATgAeJ8sCUKmiPGTHcNG49BxUgBCiOQrr4qZ7QBYAwbIqR+l9c6gODhuZwhe0r5wQE6zDVQMnonISi0WbwjZQc0I7Nchu8GUAsw7oEdB1AjnR723lVRlpN40zmG0ibMDycpn6+mzAQAsafoDQDrjUYrQEvzzQWqQEb9IBtl8tpmbwiFztQJPwKJc3QxC4Qudvwb9qLQIw1t1iQOaukdGwEyhRA-G+ZmPJmGyJtFRsXvhspUKAJVgsbbG5+lZkPgHezOYy5WA6VGEm4B5Sbu8zfwe1NlMvBtIocI+6mZ17gQDHedPrSGHLSmwL3GrzoEvixkDnNuNv4cWP9GaR0SERlIgxmACKcxKTQo1ae8+N+H4OkuOHWMeXkJuCxFuRNbJOlBVjxAKZf4NeIV434PxuCQ4W8+4dAUW4HD2DGiXhsUQ8m7+4bQTgBisoDlcDhtUtD0APK1qN5GLhJ0+ci9392QsLeUMT5vveEbDa-JaCowmQ8mqJb8yWKltIVcDr06QBAPnPsQDDA5CcuNzQ+xBQFbU3Qd4xEihRT+PiK0L70-ni3p4i-YlpBtIz8idswpBALa11Bg3k9BzQsDeqQfbAaP9qbqQzS+OG9lYGBVCrs+josDyOqVXgxEI274ZTD0KcqgEAZvaDv7Ti4PzXMQkXuwllA7oAIgUm5G0uqFw9rKcA3UcnacNOQJvcKsq+O2+IREb7m8nSBboUewk8B-qU+gr+7Y2RoShmYKtlWKjMMrQXLYeQIZCOJEKyDi7khmO3Dl0u5HyWcMpjZqvCT6AbBqAa2dEA8jcAE8AVZ0gztx286YRmXVS1lCcxQ7aKMNNrSIMovIosvrZn30qwQExoDDsQMHnIe7iGPxTS6aH9vjbyqLOI-z9hAgDeLHsNc5Ch048VA1MrYjzW+mFFk9n+7yAzjuwpMdXcU-yr9jNOUFbxe1Dtg-AC3ZVgwo0iDYwoSJinoCxUA+mAqEinhA2ZhfGAh-JDvW+kybv4wqjRAMcOdm915cLtNcCORYq6clS0PJRErV9XTXt09atI4TQxuOWC67Eu9B0+UDe9jg-+yozutok3GozyVgQjrjBBBsBGH7eYFLlHElpYgBtA9I+5hSs1W526UCYTzGyECNDH3AjDIwXot6H2L7i47Ay1rsEbPSZPIr7CYg3oZ3PIA6wxL0vLHsLSvsQvizyLZCSQL4nlAj3a7lEQKK2JhUrD0CAeX7UdGUBJA7oEkAswH3CStxgsB0gDwHM2Bft0aXsKJC+MaBy4Mfcyu-jBjAeB8gdSmBB5aCIHU4GAeci6B1ARlA0PcAikwEHLOQbQDB9EBEHg67d0QA2IDsQag6yWQeNDUBxwfMwbME0i8HREHkC7cSvl27OesIQyCVR3oU8CR4FVrxqJLNbbVCMLsM+4ghIeqRrX2Exa8HDOADGA95TwIKR3HapeCzMkqwEh7YdPgzPKM3KM9h-0iOHrINP51YzyQ96ZMkhkNyR8ywCClBHeu6z7z0d4BEdEQjQEEiBl4ey8BstaEEYAbQk63sRIr2QB77e4ixOMQZHo4ZlBs+1MP7T7Z3unwcf7uXvsaROslFxl0CYRZ7utbSkF6VkHYex-uXbTFlWC371bQ7k5c4m-lzcgpcAENODiS3f0dGUYJqNYO0Q0D1wQ1bTE3WJ5OUfsL8c1gmBC0Gh70a7DvQ1qDaHEQF0aXiSAIRL+cjYQ96Vg-NgyD2M4I5YduGyR2XsFRlR9c3ugldQyD6QTe-SCGFTaxA7TsfEu6k4rFk8sfG8q1MEoN6Ruyvt5w5xx34SheQKNI981dScKShJzo0sRiBOQvwn7fSIIeR7D0DVS14mXQs3YAx+93CWgGJ3hXsQg0hJuNLKPhkBuHvDokKyz0tZX05kcByRg-iEXD4ziAmJQoHiAfmQOvuJ967+Il5Ie1VxEcFh8vyTQVEJdSpYZQGidEnU6yIaYnW0RtCitIIDjMOEsXk4n7JFYWKlC8mmg1CfQxoNjzvGaVEkaFHuudc2bbzjvYrfrPgBkel++ACEhZ+9IPyeyg0nvKDEN3AzMDJHx+7IgunRnkWQgAAAL7+nhsIQDq0XEKwAYA2ALwBEApACXYAA+l7L8A-gCwCpFPAAQBot3aB4BeAjqdNVrQ-gKQDqQfVIM5b1T4JPb84CWurOxUXUWnaMht5neHZAPdj7KsAegKQD+nyGOQC35sZ77ixnGCkmekAKZ3mcgAqFXQCZnpANmeqSA5ydkbETMb7sW8AHtQhGRjEwfwgeoeG+iDGsoOQXbhl3WljW7UBucjNnAZ22dgA5ILGerosZ3fw-+vAMmfz6A50OcjnIAGOfcIA5wWercFNW8FPMEjuISJAgh+adWYUeq9OwRJlCR3Sk0UhAr7nrZ14D-osZ1KAJYsZ7HS9n3gNee8A6Z4UB3nD5wPADndi9kA2NOA9RCaN5jc0SUeg+-620ACWP81V+24WIgsyTwGBdtnY8N2fzmYwPBf9nSF4OcZnwZ6OcteOZ0GATndU862vUYYOkKz53LOblPoEKl1XoydPDRdeABSLGeUaz00xeIXaZ6xcoX7F-eecX45yxeTnwrGOWFZcRqXx+cfyrz5SXpAEeCxn9S-uaxnQx5ed9nil14C3nql2he5nLF+6DCsXYaavcQ8a5uC3gfSNyDGXIAMSl0Asl4qP2h1lwhcqAN52xdtnjl9xeaXvF1lVeI3MXyMZkAV7giWoy2D2XzgrqqP30gfl9mcaYUF7ZdXn4VyxeNwYhNwB3ntDc4bwX8pzmSaXXu3ug1Qlzc0JR0AFjDvyzkeuxiFoW+DUuP8-qVW2qXnR9+ADn3GotAlgl0G+hpb79DUuLThFwSkzid5-Yy24RuyxcI6plq2XkBLwA+O0B9+ARCqXchm-2mgNQAOf82fuI1dqGh4+3C7X4FxxcqSj5yxd79Yzk1DzQeycvx5XFNK5cEgfl+3ZmXjRApfFXSl6VfYtql5VcAi8F2gC5QqAE8DqQZ5xQCxn9gMIBUnLFw0CyxLIISCBBdg+AHhBfcorHRA0DXEFPDWqqDSmxZAbK2aSqlxgBIA0N1oCxnTgAjd+ASNyjeNAhICAE1zpphIUGxON+oNqksQfXIE3hmPkGkBrlaTe7XbZ7lKVVdi-kQrXFVUSMjo2dMnB7cfNyLdeA-NrlKckA56vWuQAnES7o4g0o7t4EWcutAHnWZ+pd3XSlw9dbC66GQAd2w0jrcvIHFUpD-+o+7x1Vick+cCVBRcLleG5gV+Qh-XqZ14D95jF8DeW+6gP4BfZpACde05Z+Qva7FnVxFQJB6Mq3yqX+632gEA11WiK7Gl0zRneQv6YqBEUSt-mcRZgmqnfwdBJiyKYEQfWG0fd3EO80XMYcvIL53IANPhILxd2wgTCDF0nRyXjYS9LuC+wEkZELac1mNGKT12wKkA-2VFcm36Fyxe1plnPY3Qa3tj2ACx0S5fjN2yS84UFIfl--j4ITwLGfnQGDD2ShXzF0pcB3PAG2cg3Id7wBh3IABHcEA6epvft+JlHejNIVIqpfYwnxP4qLCBAJaP-jzGTNPez9Zf2gV2CiEA3Kc+NGTdtnMxj7mUg5JwQAG3p8+njIAhF8eoJFn-Lx2VjDd9xp9gkd7A8pOcdRJAhez5LjynrSdCCJ+QG5LFSudNAh32G3Y98be3Xk90pfT3u91SZz3qV-gisezorpW-k1upNF+Xk0bGcM97SAfe2XpAMfcVXwd2QCh34d7bGZMWDDff9QrEHBCtUOUUiSqXhQzaCp3KvTyC7NcmpaZMoX8g3fqQhd71AEAAVq+Uawe7XwLxytKAlxVc96rKqudk8QziG3bZ8UeiwTwAQArFN3M8dEDZqoEjrIvJkrmSQgDnXwsnsql01vnKj22d1A2ANWyR3yj5nw+gXQ01fDkE-nGALZc581WU6k+4ol5tu1zQ83XoYFxcXnDDwAx4ccaKYK4rI6pwBeUAsesQbuET0GBgXQZ54Dtn1ADglndSAFGfjAZgMGdsAbnKoCGPNuawAX3IAPPDjAoo9IA+MIAP9n+nQAA)
