# Date extraction

> Extracts absolute and relative dates by asking TypeSafe for the parts named in a document, then resolving and validating them in code with confidence-based review.

*Read a date's parts off the text with TypeSafe, then resolve them to a `date` in code.*

The function you build here, `extract_date(document, role)`, takes a document and a
phrase naming the date you want, such as "the deadline to return the form", and hands
back a `date` with a confidence. It flags a low-confidence read, and one whose parts do
not add up to a date at all, including a date the document never states. The date can be
spelled out ("August 14, 2027") or written relative to today ("tomorrow", "next
Thursday").

TypeSafe answers `Choice` questions about the date in one call: what kind of date it is,
and
which month, day, year, or weekday the text names. Code turns those answers into a `date`.
The model reads what the text says and never does the calendar math.

The cells below run that function over four short documents, print each date with its
confidence, and split the results into the ones code accepts and the ones a person should
look at.

![Overview diagram](../../assets/overview.png)

*TypeSafe reads how the date is written and which parts the text names. Code turns those
answers into a `date`, counting from today when the date is relative, and either accepts
it or sends it to review.*

## Setup

```bash
pip install ipython "typesafe-sdk>=0.5.7" cooksafe --extra-index-url https://pypi.typesafe.ai/
```

then set `TYPESAFE_API_KEY`.

```python
import os
from datetime import date, timedelta
from pathlib import Path

from cooksafe import JsonCache, make_playground_link
from IPython.display import Markdown, display
from typesafe_sdk import Choice, TypeSafeClient

TYPESAFE_MODEL = "jev-1.12"
TODAY = date(
    2026, 7, 30
)  # fixed reference "today" so relative dates resolve reproducibly
REVIEW_BELOW = 0.60  # gate: a date below this confidence is flagged for a human

MONTHS = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12,
}
WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
YEAR_WINDOW = list(range(1900, 2051))  # 1900..2050

# Cached to json_cache.json (shipped with the cookbook, so re-rendering replays the published
# results with no API spend); delete it to re-run live.
json_cache = JsonCache(Path("json_cache.json"))
```

```python
# The demo cells below run when this file is executed as the cookbook; the constants and the pure
# resolve/assemble code stay importable, so the calendar math can be unit-tested on its own.
if __name__ == "__cookbook__":
    client = TypeSafeClient(
        api_key=os.environ.get(
            "TYPESAFE_API_KEY", "cache-only"
        ),  # cached re-renders need no key
        base_url=os.environ.get("TYPESAFE_BASE_URL"),
        timeout=30.0,
    )
```

## The questions

Seven `Choice` questions go out in one call. `mode` says how the date is written:
`absolute`
for a date that names a month, `relative` for one written relative to today, and `none`
when the document does not state the date at all.

The other six read the pieces. An absolute date needs `month`, `day`, and `year`. A
relative one needs `day_anchor`: today, tomorrow, the day after, or a named weekday. When
it names a weekday, `weekday` and `week_offset` say which one and which week. Code reads
only the pieces `mode` calls for.

`year` lists one option per year from 1900 to 2050, plus two escapes. `none` means the text
states no year and code fills one in. `out_of_range` means the text states a year outside
the list, and code flags that instead of guessing. If a list that long bothers you, pull
the year-like numbers out of the text first and offer the model only those.

```python
def date_questions(role: str) -> dict[str, Choice]:
    """Seven typed choices that read a date's shape and parts off the text -- no math."""
    absent = "The document does not state this, or it is not this kind of date."
    return {
        "mode": Choice(
            instructions=(
                f"How is {role} written? 'absolute' = a calendar date naming a month (e.g. "
                "'August 14', 'the 3rd of March'); 'relative' = given relative to today (today, "
                "tomorrow, the day after tomorrow, or a named weekday such as 'next Thursday'); "
                "'none' = the document does not state this date."
            ),
            criteria={"absolute": None, "relative": None, "none": None},
        ),
        "month": Choice(
            instructions=f"If {role} is an absolute calendar date, which month is it in?",
            criteria={m: None for m in MONTHS} | {"none": absent},
        ),
        "day": Choice(
            instructions=f"If {role} is an absolute calendar date, which day of the month (1-31)?",
            criteria={str(d): None for d in range(1, 32)} | {"none": absent},
        ),
        "year": Choice(
            instructions=(
                f"If {role} is an absolute calendar date, which year? Pick 'none' if the document "
                "states no year (code infers it), or 'out_of_range' if a year is stated but not "
                "in the list."
            ),
            criteria={str(y): None for y in YEAR_WINDOW}
            | {
                "out_of_range": "A year is stated for this date but is outside the listed range.",
                "none": "No year is stated for this date.",
            },
        ),
        "day_anchor": Choice(
            instructions=(
                f"If {role} is relative to today, which day is it? 'today', 'tomorrow', "
                "'day_after' (the day after tomorrow), or 'weekday' (a named day of the week)."
            ),
            criteria={
                "today": None,
                "tomorrow": None,
                "day_after": None,
                "weekday": None,
                "none": absent,
            },
        ),
        "weekday": Choice(
            instructions=f"If {role} names a day of the week, which one?",
            criteria={w: None for w in WEEKDAYS} | {"none": absent},
        ),
        "week_offset": Choice(
            instructions=(
                f"If {role} names a weekday, which week is it in? 'next' for 'next Thursday' or "
                "'Thursday next week'; 'current' for 'this Thursday'; 'none' for a bare weekday "
                "with no qualifier (just 'Thursday' / 'on Thursday')."
            ),
            criteria={"current": None, "next": None, "none": absent},
        ),
    }
```

## Resolve it in code

`read_parts` makes the call. `assemble` turns the answers into a `date`: it fills in the
year when the text states none, and it works out which day a named weekday points at. Both
of those count from `TODAY`, which is pinned so relative dates come out the same on every
run. `assemble` also reports the lowest confidence among the parts it used, so a weak
answer on any one part can send the whole date to review.

"next Thursday" can mean two different days, so code decides which. A weekday with no
qualifier means the next one on or after today. `next` means the following calendar week,
and `current` means this week.

```python
@json_cache
def read_parts(document: str, role: str) -> dict:
    """One TypeSafe call -> {part: {choice, confidence}} for the seven questions."""
    answers = client.system_one(
        state=document, questions=date_questions(role), model=TYPESAFE_MODEL
    ).answers
    return {
        part: {"choice": ans.choice, "confidence": ans.confidence}
        for part, ans in answers.items()
    }

def resolve_weekday(today: date, weekday: str, week_offset: str) -> date:
    """Which date a named weekday points to, by our stated convention: a bare weekday is the next
    occurrence on or after today; 'next' is the following calendar week; 'current' is this week."""
    w = WEEKDAYS.index(weekday)
    this_monday = today - timedelta(days=today.weekday())
    if week_offset == "next":
        return this_monday + timedelta(days=7 + w)
    if week_offset == "current":
        return this_monday + timedelta(days=w)
    return today + timedelta(days=(w - today.weekday()) % 7)

def assemble(parts: dict, today: date = TODAY) -> dict:
    """Resolve the parts TypeSafe read into a concrete date, in code. Confidence is the weakest of
    the parts the shape actually used."""
    mode = parts["mode"]["choice"]
    confs = [parts["mode"]["confidence"]]

    def result(resolved: date | None, note: str) -> dict:
        usable = [c for c in confs if c is not None]
        confidence = min(usable) if usable else None
        needs_review = (
            resolved is None or confidence is None or confidence < REVIEW_BELOW
        )
        return {
            "date": resolved,
            "confidence": confidence,
            "needs_review": needs_review,
            "note": note,
        }

    if mode == "none":
        return result(None, "no such date stated")

    if mode == "absolute":
        month, day, year = (
            parts["month"]["choice"],
            parts["day"]["choice"],
            parts["year"]["choice"],
        )
        confs += [
            parts["month"]["confidence"],
            parts["day"]["confidence"],
            parts["year"]["confidence"],
        ]
        if "none" in (month, day) or not day.isdigit() or month not in MONTHS:
            return result(None, "absolute date incomplete")
        if (
            year == "out_of_range"
        ):  # a year is stated but off the list -> flag, don't guess
            return result(None, f"year outside {YEAR_WINDOW[0]}-{YEAR_WINDOW[-1]}")
        if (
            year == "none"
        ):  # no year stated -> infer this year, bumped to next if well past
            try:
                resolved = date(today.year, MONTHS[month], int(day))
            except (
                ValueError
            ):  # e.g. February 30 -- an inconsistent read, not a real date
                return result(None, f"impossible date: {month} {day}")
            if resolved < today - timedelta(days=31):
                resolved = date(today.year + 1, MONTHS[month], int(day))
            return result(resolved, "")
        try:  # a stated, in-range year
            return result(date(int(year), MONTHS[month], int(day)), "")
        except ValueError:
            return result(None, f"impossible date: {year}-{month}-{day}")

    if mode == "relative":
        anchor = parts["day_anchor"]["choice"]
        confs.append(parts["day_anchor"]["confidence"])
        if anchor == "today":
            return result(today, "")
        if anchor == "tomorrow":
            return result(today + timedelta(days=1), "")
        if anchor == "day_after":
            return result(today + timedelta(days=2), "")
        if anchor == "weekday":
            weekday, offset = parts["weekday"]["choice"], parts["week_offset"]["choice"]
            confs += [
                parts["weekday"]["confidence"],
                parts["week_offset"]["confidence"],
            ]
            if weekday not in WEEKDAYS:
                return result(None, "relative weekday not read")
            return result(resolve_weekday(today, weekday, offset), "")
        return result(None, "relative day not read")

    return result(None, f"unrecognized mode: {mode}")

def extract_date(document: str, role: str) -> dict:
    return assemble(read_parts(document, role))
```

## Run it

Six questions across four short documents: two dates from a contract that states its years,
a form deadline written without a year, a survey that closes "today", a review set for
"next Thursday", and a date the form never mentions. All of them resolve against `TODAY` =
2026-07-30, a Thursday.

```python
CONTRACT = "This agreement is effective January 1, 2025 and expires December 31, 2027."
FORM = "Please return the signed form by August 14."
SURVEY = "Heads up - the customer survey closes today at 5pm."
REVIEW = "Let's schedule the design review for next Thursday."

# (document, question phrase, expected date) -- the expected value is only for the scorecard.
EXAMPLES = [
    (CONTRACT, "the date the agreement takes effect", date(2025, 1, 1)),
    (CONTRACT, "the date the agreement expires", date(2027, 12, 31)),
    (FORM, "the deadline to return the form", date(2026, 8, 14)),
    (FORM, "the date of the kickoff call", None),
    (SURVEY, "the date the survey closes", date(2026, 7, 30)),
    (REVIEW, "the date of the design review", date(2026, 8, 6)),
]

if __name__ == "__cookbook__":
    print(f"{'':3}{'question':<38}{'expected':<12}{'got':<12}{'conf':>6}  flags")
    print("-" * 84)
    for document, role, expected in EXAMPLES:
        r = extract_date(document, role)
        got = r["date"].isoformat() if r["date"] else "none"
        exp = expected.isoformat() if expected else "none"
        mark = "OK" if r["date"] == expected else "XX"
        conf = f"{r['confidence']:.2f}" if r["confidence"] is not None else " n/a"
        flags = "  <== review" if r["needs_review"] else ""
        if r["note"]:
            flags += f"  ({r['note']})"
        print(f"{mark:<3}{role:<38}{exp:<12}{got:<12}{conf:>6}{flags}")
```

```
   question                              expected    got           conf  flags
------------------------------------------------------------------------------------
OK the date the agreement takes effect   2025-01-01  2025-01-01    0.97
OK the date the agreement expires        2027-12-31  2027-12-31    0.91
OK the deadline to return the form       2026-08-14  2026-08-14    0.95
OK the date of the kickoff call          none        none          0.46  <== review  (absolute date incomplete)
OK the date the survey closes            2026-07-30  2026-07-30    0.94
OK the date of the design review         2026-08-06  2026-08-06    0.92
```

The contract states both of its years, so those came off the text. The form states no year,
so code filled in 2026: it takes the current year and moves to the next one only when the
date is already more than a month past. "today" and "next Thursday" went through the same
function as the spelled-out dates.

The kickoff call is the one the form never mentions. There is a date in that form, just not
this one, and the note `absolute date incomplete` means `mode` came back `absolute` with no
month to go with it. The date came back empty, the confidence reads 0.46, and the row is
flagged for a person.

## Confidence to route on

Every answer comes back with a calibrated confidence, and a date's confidence is the lowest
one among the parts that went into it. A date under `REVIEW_BELOW` = 0.60 goes to a person,
and so does a date code could not assemble at all. The rest go straight through.

```python
if __name__ == "__cookbook__":
    confident = [
        (doc, role)
        for doc, role, _ in EXAMPLES
        if not extract_date(doc, role)["needs_review"]
    ]
    review = [
        (doc, role)
        for doc, role, _ in EXAMPLES
        if extract_date(doc, role)["needs_review"]
    ]
    print(f"auto-accept ({len(confident)}):")
    for _doc, role in confident:
        print(f"  - {role}")
    print(f"\nsend to review ({len(review)}):")
    for _doc, role in review:
        r = extract_date(_doc, role)
        print(
            f"  - {role}  (conf {r['confidence']:.2f} / {r['note'] or 'low confidence'})"
        )
```

```
auto-accept (5):
  - the date the agreement takes effect
  - the date the agreement expires
  - the deadline to return the form
  - the date the survey closes
  - the date of the design review

send to review (1):
  - the date of the kickoff call  (conf 0.46 / absolute date incomplete)
```

## Open it in the TypeSafe playground

The link below carries the "next Thursday" message and the same questions the code sends.
Open it to see the answers and their confidences, and to change the wording without writing
any code.

```python
if __name__ == "__cookbook__":
    playground_link = make_playground_link(
        REVIEW, date_questions("the date of the design review"), models=[TYPESAFE_MODEL]
    )
    display(
        Markdown(
            f"🔗 [Open this document + questions in the TypeSafe playground]({playground_link})"
        )
    )
```

[Open this document + questions in the TypeSafe playground →](https://console.typesafe.ai/playground#share/N4IgJg9gxgrgtgUwHYBcAqCAeKQC4AEIAMgigOQDO+FUAFgmDADYL4r35gIUCWA5knwAnBADceCAO74AZhCH4kWFPjS0YQimACGATwB0IADSEADkIhxTKChmx5CwADog4ELi4LOQKXaYSe+C50EDxQAcZBIFBCPCgIsdqB3toARhQQTDDxgUjMTCYuIkzaKDyiEQR5TAVRSBBKufkAvoUgPEgUKEIwUGUNFIEuABIQ0jxU7Kw68fgQMmwcXLwCwmIS0pKxKPFIAPz4ZGkZWfFk+AC8+Nr4UNosSDoKM6xI2nAdfNf4bqi0+AAKBD6Pj6Q4AQRgfBgXXwAEYACxkExkKb4ADMQjAcwWAFltEI6GQAJQAbkOxVK5QQ5yufGpgkpZQqbAgrJ0ukBKHcehM3LcQgskj5Sz01xk8QU-PkQpM8m+b0Q2MkCAQAGsOdRev9tFQyEpsKp1JoOSTyfqGjTLotptB4MgVJBuIoICouqVWOwJpwPfoXK0or92MkXL5-ENorRQuEXG0YnEEjwkg5vAApbR5Am6Jo1NoAMQQqR6WZztRc+MJtFLbXB5h4TGrUXx2Yc1TLIFTMEarfybU7TBbVV7UUh0K6jZcAGUENYEHBUgkJyAAPJ9CALoRLgByEAq88XPdzUQAIghwvvN4f2-VuwQXGpbbBEKhOBBnfU3SgPYsJnKFHF8G9D8fyoNUOmxeYfXiP0QADFwOi6Ho+h4AYIwASQWNEXhxG1OG4fhGXWKRAKoDNrnSTJslYO4HieKCEBMSRaDCf4g3+b0AI6PZ-TaDkQx8PxKiiEIwgiONtkTZMvBcOElwAJiXdElwRJcAFYlwANiXAB2JcAA4lwATiXOEAAYTNkq82jhBSrKiOElLsmSVKckA4XU1y4S0zzdM8gzPOM1y5PMoLLKHI8XDk2zwvbOTHJito5JchKojkjyUsi7yMpAOTfOyuT-PywLsvREKSrCxRhxcG8hPvJY7WfR03yoYD3VmL0KD-QCVCA10QPwMDHhwl4YLg9pOm6Xp+k6dDMNFWZIKw-DVhEcRiO9Mjjko2YaOQOiXkY5i6B9TlFo4NjAThABadE4WJbjYLaXQEAJfiw1qyNozE4SJMSfi4UM0yysqiK3MBiq22swHopB9sAdM+LYah0zkqR+zAfStGZMBrKsbB0y8rx+HCqJwHitJsyTMMuEIaqsGbKphzGdRyH0fcxncdZ7G4UJrn6ZJvmAYBqngpF2nQYBqKRcRwXDKSkXMdluTObpyXedVuWBY1uTydl0qqdug2Yb1mWNfRFmzcVs2VYlwz0XV230S1x3dY1hFgdlhFxbhwyEWNt3TdthELaDq2g5tn2EQdyPncj13bdUj2NdU72odU-2E8Dn3VJD7Ow+ziO0+jtPY7T+OfY0pPbY01P0Y0jOK6zqGNNz5v8+bwu6+LuvS7r8uoe0qufe02vse0huB6b9HtNb6f2+nzux+7sfe7H-v0b0oeob00ewb0ieN6n7G9Nn4-5+Pxe9+XvfV739fscBqnqafg+H6PsHfaf8+P8vgHDOvv+t8-73xykDLeqUga72CqZV+oCEbySBqfOB39oGX2gdfaBt9oEgOCpTIKpkaYIIZvgpmJCkG4JQQQtBBCMEEKwQQnBMDwGRRgVAmBsDgpxQQfLfBaVuHUNytw+hOsEH63wYbcRHCEbv2CubURlD0TUPtqI+h6JGHuwQV7TRUiEQyJRuQlGlCETUKjpo+hCJGGJyXBAbIAB9eYtihAZj4B9cE+BnoEhItQL88RsRyClMxKg2FUjZC8TYmwPAuC4SYBMXxwhnHAljHUS0EYdzuJev+KgbUGCyHlB1eio02gIUmshVCDgXAYVwthM60xlqETWuMUiggtqnGovcPaniDr4CYixdJBIDgAAUwhqkODVc4PA5qPntC+bJLU2QeIUACKA7hWAdBkAkKgcRiRdTIOE+xMhHEJPGQsG4CyvHZOxCElQwEOjRNiYUqIHJbEZhCJeaSAlwzlM+qJJJwRfpJjejyQceNpSCjGEuJ52gJQHmyiqdUfFXI1QjA+V8T4HSvnfH1bJIEuqcTmSofJg0IILBGjxKIxSkLTUGF8ypWFvw1LwisepGwvFMmpKydkvJulHX+JqDiKADioiBciQ4oKhQirIJC6FQhzgAjpZyKFkpWQCiFNsuYCgyBwo1HoWVNxFQ5M1AyrVxIHkuC1Qi9570IwiRjJEP5CY-opnLA0C1eM0AwG4K6vmAB1BgSgtB6CXGoDQAbgV8zzLEL1dNJylA0FG0Gk4uzxuvCkr5KLIBopfE6fF3jvwdVxT1HNhLwLDV9GS+CE1KUoRmjSyZ9EcJLSZWsBpih3jOhuIautWrDq9MtA9MaWr9kyAoKQN6glrVRh+Xa6I-ypL4G8LAQUDolwGhQCu1Nd4QDpoaui7NLpPx5sCQWrxwFi1DUgqSx65LK1TWrdSzdtL5qsAZcsAizaWX6tIt01U2rdA9uOlqrxnF9ijOUOcfxoHDTBpNDq9VhxoOhsUMob96oyDmkXSIVA4H5SokCUaENppzRjNyQoG4qQCSsHNWKSQcR-j1HwAARxgPcCZEhFkACsYQqDIAh00+AAD0hwGj4Zg7oEko1miRBANoUwPAABqGzq0OBAKIOEUmR0sD6AwXEKymAUAcAAbRAOxsQV04T6BsiAAAus0IAA)
