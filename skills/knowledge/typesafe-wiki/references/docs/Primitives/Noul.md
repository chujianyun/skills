# Noul

> A Noul question asks the TypeSafe model to evaluate a yes/no question and return the probability that the answer is yes.

export function TypesafeExample({example, display, title}) {
  const keyStrUriSafe = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-$";
  function compressToEncodedURIComponent(input) {
    if (input == null) return "";
    return _compress(input, 6, function (a) {
      return keyStrUriSafe.charAt(a);
    });
  }
  function _compress(uncompressed, bitsPerChar, getCharFromInt) {
    if (uncompressed == null) return "";
    var i, value, context_dictionary = {}, context_dictionaryToCreate = {}, context_c = "", context_wc = "", context_w = "", context_enlargeIn = 2, context_dictSize = 3, context_numBits = 2, context_data = [], context_data_val = 0, context_data_position = 0, ii;
    for (ii = 0; ii < uncompressed.length; ii += 1) {
      context_c = uncompressed.charAt(ii);
      if (!Object.prototype.hasOwnProperty.call(context_dictionary, context_c)) {
        context_dictionary[context_c] = context_dictSize++;
        context_dictionaryToCreate[context_c] = true;
      }
      context_wc = context_w + context_c;
      if (Object.prototype.hasOwnProperty.call(context_dictionary, context_wc)) {
        context_w = context_wc;
      } else {
        if (Object.prototype.hasOwnProperty.call(context_dictionaryToCreate, context_w)) {
          if (context_w.charCodeAt(0) < 256) {
            for (i = 0; i < context_numBits; i++) {
              context_data_val = context_data_val << 1;
              if (context_data_position == bitsPerChar - 1) {
                context_data_position = 0;
                context_data.push(getCharFromInt(context_data_val));
                context_data_val = 0;
              } else {
                context_data_position++;
              }
            }
            value = context_w.charCodeAt(0);
            for (i = 0; i < 8; i++) {
              context_data_val = context_data_val << 1 | value & 1;
              if (context_data_position == bitsPerChar - 1) {
                context_data_position = 0;
                context_data.push(getCharFromInt(context_data_val));
                context_data_val = 0;
              } else {
                context_data_position++;
              }
              value = value >> 1;
            }
          } else {
            value = 1;
            for (i = 0; i < context_numBits; i++) {
              context_data_val = context_data_val << 1 | value;
              if (context_data_position == bitsPerChar - 1) {
                context_data_position = 0;
                context_data.push(getCharFromInt(context_data_val));
                context_data_val = 0;
              } else {
                context_data_position++;
              }
              value = 0;
            }
            value = context_w.charCodeAt(0);
            for (i = 0; i < 16; i++) {
              context_data_val = context_data_val << 1 | value & 1;
              if (context_data_position == bitsPerChar - 1) {
                context_data_position = 0;
                context_data.push(getCharFromInt(context_data_val));
                context_data_val = 0;
              } else {
                context_data_position++;
              }
              value = value >> 1;
            }
          }
          context_enlargeIn--;
          if (context_enlargeIn == 0) {
            context_enlargeIn = Math.pow(2, context_numBits);
            context_numBits++;
          }
          delete context_dictionaryToCreate[context_w];
        } else {
          value = context_dictionary[context_w];
          for (i = 0; i < context_numBits; i++) {
            context_data_val = context_data_val << 1 | value & 1;
            if (context_data_position == bitsPerChar - 1) {
              context_data_position = 0;
              context_data.push(getCharFromInt(context_data_val));
              context_data_val = 0;
            } else {
              context_data_position++;
            }
            value = value >> 1;
          }
        }
        context_enlargeIn--;
        if (context_enlargeIn == 0) {
          context_enlargeIn = Math.pow(2, context_numBits);
          context_numBits++;
        }
        context_dictionary[context_wc] = context_dictSize++;
        context_w = String(context_c);
      }
    }
    if (context_w !== "") {
      if (Object.prototype.hasOwnProperty.call(context_dictionaryToCreate, context_w)) {
        if (context_w.charCodeAt(0) < 256) {
          for (i = 0; i < context_numBits; i++) {
            context_data_val = context_data_val << 1;
            if (context_data_position == bitsPerChar - 1) {
              context_data_position = 0;
              context_data.push(getCharFromInt(context_data_val));
              context_data_val = 0;
            } else {
              context_data_position++;
            }
          }
          value = context_w.charCodeAt(0);
          for (i = 0; i < 8; i++) {
            context_data_val = context_data_val << 1 | value & 1;
            if (context_data_position == bitsPerChar - 1) {
              context_data_position = 0;
              context_data.push(getCharFromInt(context_data_val));
              context_data_val = 0;
            } else {
              context_data_position++;
            }
            value = value >> 1;
          }
        } else {
          value = 1;
          for (i = 0; i < context_numBits; i++) {
            context_data_val = context_data_val << 1 | value;
            if (context_data_position == bitsPerChar - 1) {
              context_data_position = 0;
              context_data.push(getCharFromInt(context_data_val));
              context_data_val = 0;
            } else {
              context_data_position++;
            }
            value = 0;
          }
          value = context_w.charCodeAt(0);
          for (i = 0; i < 16; i++) {
            context_data_val = context_data_val << 1 | value & 1;
            if (context_data_position == bitsPerChar - 1) {
              context_data_position = 0;
              context_data.push(getCharFromInt(context_data_val));
              context_data_val = 0;
            } else {
              context_data_position++;
            }
            value = value >> 1;
          }
        }
        context_enlargeIn--;
        if (context_enlargeIn == 0) {
          context_enlargeIn = Math.pow(2, context_numBits);
          context_numBits++;
        }
        delete context_dictionaryToCreate[context_w];
      } else {
        value = context_dictionary[context_w];
        for (i = 0; i < context_numBits; i++) {
          context_data_val = context_data_val << 1 | value & 1;
          if (context_data_position == bitsPerChar - 1) {
            context_data_position = 0;
            context_data.push(getCharFromInt(context_data_val));
            context_data_val = 0;
          } else {
            context_data_position++;
          }
          value = value >> 1;
        }
      }
      context_enlargeIn--;
      if (context_enlargeIn == 0) {
        context_enlargeIn = Math.pow(2, context_numBits);
        context_numBits++;
      }
    }
    value = 2;
    for (i = 0; i < context_numBits; i++) {
      context_data_val = context_data_val << 1 | value & 1;
      if (context_data_position == bitsPerChar - 1) {
        context_data_position = 0;
        context_data.push(getCharFromInt(context_data_val));
        context_data_val = 0;
      } else {
        context_data_position++;
      }
      value = value >> 1;
    }
    while (true) {
      context_data_val = context_data_val << 1;
      if (context_data_position == bitsPerChar - 1) {
        context_data.push(getCharFromInt(context_data_val));
        break;
      } else context_data_position++;
    }
    return context_data.join("");
  }
  function buildHref(ex) {
    const documentText = ex.state === undefined ? "" : typeof ex.state === "string" ? ex.state : JSON.stringify(ex.state, null, 2);
    return "https://console.typesafe.ai/decode#share/" + compressToEncodedURIComponent(JSON.stringify({
      apiVersion: "v1",
      documentText,
      promptsText: JSON.stringify(ex.questions, null, 2),
      selectedModels: ex.selectedModels
    }));
  }
  const displayedExample = display === "questions" ? example.questions : example.state === undefined ? {
    questions: example.questions
  } : {
    state: example.state,
    questions: example.questions
  };
  const code = JSON.stringify(displayedExample, null, 2);
  const href = buildHref(example);
  return

```json
{code}
```


        <a href={href} target="_blank" rel="noreferrer" className="text-primary">
          Try it in the Playground →
        </a>

    ;
}

Use a Noul when the answer is yes or no. For example, does this message ask for a refund, does this resume mention distributed systems, does this comment contain personal data. If the answer is one of several options, use a [Choice](Choice.md). If it's a position on a spectrum, use a [Score](Score.md). [Choose a question type](Primitives (Questions).md#choose-a-question-type) compares all three.

A Noul answer is a single number representing the probability that the answer is yes where 0 means no and 1 means yes.

## Request structure

The POST request body to the [TypeSafe API](../API reference.md) has the same three top-level fields as any other question type: `state`, which is the content to evaluate; `model`; and `questions`. Each Noul question has the following fields:

* `type`: Always `"noul"`.
* `instructions`: The yes/no question the model answers, or a statement for it to judge.
* `criteria`: Optional. An object with `true` and `false` descriptions of what a yes and a no mean.

Below is a request where the state is a support message and the two questions are whether the customer wants a person and whether they have contacted support before:

```jsx

```jsx

```jsx

```jsx
<TypesafeExample
  display="request"
  example={{
state: 'I have asked three times now. Can I please just talk to a real person?',
selectedModels: ['jev-latest'],
questions: {
  is_human_escalation: {
    type: 'noul',
    instructions: 'Is the customer asking for a human agent?',
  },
  is_repeat_contact: {
    type: 'noul',
    instructions: 'Has the customer contacted support about this before?',
    criteria: {
      true: 'Mentions a prior attempt, ticket, or that they have asked before',
      false: 'No sign of any previous contact',
    },
  },
},
}}
/>
```

```

```

```

You choose the question ids, `is_human_escalation` and `is_repeat_contact` here. The ids are not sent to the model. Each answer is returned under the same id. The first question relies on `instructions` alone. The second adds `criteria` to say what counts as a yes and what counts as a no.

With the [Python SDK](../SDKs/Python/TypeSafe Python SDK.md), the same questions are `Noul` objects:

```python
from typesafe_sdk import Noul, NoulCriteria, TypeSafeClient

with TypeSafeClient() as client:
    response = client.system_one(
        model="jev-latest",
        state="I have asked three times now. Can I please just talk to a real person?",
        questions={
            "is_human_escalation": Noul(
                instructions="Is the customer asking for a human agent?",
            ),
            "is_repeat_contact": Noul(
                instructions="Has the customer contacted support about this before?",
                criteria=NoulCriteria(
                    true="Mentions a prior attempt, ticket, or that they have asked before",
                    false="No sign of any previous contact",
                ),
            ),
        },
    )

    print(response.answers["is_human_escalation"].noul)
    print(response.answers["is_repeat_contact"].noul)
```

The `system_one` method and the `https://api.typesafe.ai/v1/systemone` endpoint are both named after [System One](../Concepts/System One.md), TypeSafe's AI model. [How to build with TypeSafe](../Concepts/How to build with TypeSafe.md) covers where to use it in your code.

If you're using a coding agent, install the [TypeSafe agent skill](../Agent skill.md#installation) first so it knows the request and response shapes.

**Note:**

`instructions` can be a string, an object, or an array. Start with a string. Use an object when the question needs data alongside it, such as a record to compare the state against, or when part of the question is built by your code. [Use structure in the questions](../Concepts/How to build with TypeSafe.md#use-structure-in-the-questions) explains when structure helps, and [the example below](#structured-instructions) shows it with questions built in code.

## Response structure

The response has one entry in `answers` per question, under the ids from the request:

```json
{
  "model": "jev-1.13.0",
  "answers": {
    "is_human_escalation": {
      "type": "noul",
      "noul": 0.99
    },
    "is_repeat_contact": {
      "type": "noul",
      "noul": 0.93
    }
  },
  "usage": {
    "input_tokens": 360,
    "output_tokens": 39
  }
}
```

Both answers here are close to 1. The customer says "talk to a real person", so `is_human_escalation` is 0.99. "I have asked three times now" matches the `true` description of `is_repeat_contact`, so it is 0.93.

## Reading a Noul

The number is the answer and the certainty in one. A value near 1 is a strong yes. A value near 0 is a strong no. A value near 0.5 means the model gives yes and no similar probability.

The table below shows recorded `jev-1.13.0` answers to the `is_human_escalation` question for different customer messages:

| State                                                                  | `noul` |
| ---------------------------------------------------------------------- | ------ |
| Thanks, that fixed it!                                                 | 0.02   |
| How do I reset my password?                                            | 0.07   |
| I need this sorted today, whatever it takes.                           | 0.26   |
| Are you a bot?                                                         | 0.40   |
| Is there any way to speak to someone about my invoice?                 | 0.84   |
| I have asked three times now. Can I please just talk to a real person? | 0.99   |

The first two and the last two are clear. "I need this sorted today" is urgent but never asks for a person, and gets 0.26. "Are you a bot?" hints at wanting a human without asking for one, and the model splits almost evenly at 0.40. Both are the kind of message where a decision needs to be made based on a threshold in your code.

There is no separate `confidence` value for a Noul, unlike a [Choice](Choice.md) or a [Score](Score.md). A Noul's probability distribution has only two outcomes, yes and no, so the single `noul` value describes it completely. A Choice or Score spreads probability over several options or levels, and `confidence` summarizes that spread.

Most often your code thresholds `noul` into a boolean:

```python
wants_human = response.answers["is_human_escalation"].noul > 0.9

if wants_human:
    route_to_agent(ticket)
else:
    route_to_bot(ticket)
```

Where to set the threshold depends on the cost of being wrong. Use 0.5 when yes and no are equally easy to act on. Raise it when acting on a false yes is expensive, such as paging someone or issuing a refund. Lower it when missing a true yes is expensive, such as failing to flag a safety issue. Values in the middle can go to a person rather than either code path. That is the same three-way split the [Confidence](../Concepts/Confidence.md#three-paths-for-using-confidence-in-your-code) page describes for Choice and Score answers.

A Noul value runs from 0 to 1, but it's not a scale of the thing you asked about. It is the probability that the answer is yes. If the question is really about degree, the value does not measure the degree. Below, "Is the candidate strong in Python?" is asked about four candidates, next to a [Score](Score.md) with four levels: no experience, some familiarity, regular use in a job, deep expertise.

| Candidate                                                                                   | Noul: "Is the candidate strong in Python?" | Score: "How much Python experience does the candidate have?" |
| ------------------------------------------------------------------------------------------- | ------------------------------------------ | ------------------------------------------------------------ |
| My experience is in Java and Go. I have not used Python.                                    | 0.03                                       | 0.0 (No experience)                                          |
| I have used Python occasionally for small scripts alongside my main Java work.              | 0.14                                       | 1.0 (Some familiarity)                                       |
| I used Python every day for two years in my last job, mostly data pipelines.                | 0.81                                       | 2.05 (Regular use in a job)                                  |
| I have written Python daily for eight years, including maintaining a large Django codebase. | 0.92                                       | 2.89 (Deep expertise)                                        |

The Noul judges one proposition, "strong", and the values are how likely it is. You could create levels in the 0 to 1 range in your code, such as 0.3 to 0.7 for "some experience", but the model will not see them, so nothing in the answer was judged against them. A middle value can mean medium experience or an unclear case, and the spacing between candidates is not something you chose. The Score judges each level description on its own, so every candidate landed on or near a level you wrote, and the returned probabilities show how the model divided its judgment between levels. If you disagree, reword a level and run it again. [Choose a question type](Primitives (Questions).md#choose-a-question-type) explains the distinction.

## Writing a Noul question

Ask one yes/no question per Noul. If a question has two conditions, such as "Is the customer angry and asking for a refund?", the model has to judge both at once and the value means less. Ask two Nouls and combine them in code.

Phrase the question so that a high value means yes. "Does the message contain personal data?" is clear. "Is the message free of personal data?" inverts the meaning, and code that reads it later will get it backwards.

A statement works as well as a question. For "The customer is requesting a refund", a value near 1 means the statement is true. Try both phrasings with your own data to see which works better.

Make the boundary between yes and no unambiguous. "Does this candidate have any Python experience?" works well because "any" leaves no middle ground. When the boundary is subtle, add `criteria` with `true` and `false` descriptions, as the `is_repeat_contact` question above does. The instruction is enough for most Nouls, so try your questions with and without `criteria` and keep whichever gives better answers on your documents.

## Good practice: ask more than one question per call

For a checklist of conditions, ask many Noul questions in one request: one question per condition, and the code decides what the combination means. Questions are evaluated in parallel, so adding Nouls barely changes the response time. [Ask multiple questions together](Primitives (Questions).md#ask-multiple-questions-together) explains this in more detail.

## Handling multiple Noul answers in code

The two-question request above gives the code enough to route the message. The example below escalates to a person when the customer asks for one, and raises the priority when they have been in touch before. A value in the middle on either question goes to a reviewer instead of a code path:

```python
from typesafe_sdk import Noul, NoulCriteria, TypeSafeClient

SUPPORT_QUESTIONS = {
    "is_human_escalation": Noul(
        instructions="Is the customer asking for a human agent?",
    ),
    "is_repeat_contact": Noul(
        instructions="Has the customer contacted support about this before?",
        criteria=NoulCriteria(
            true="Mentions a prior attempt, ticket, or that they have asked before",
            false="No sign of any previous contact",
        ),
    ),
}

YES = 0.8
NO = 0.2

def route(message: str) -> None:
    with TypeSafeClient() as client:
        response = client.system_one(
            model="jev-latest",
            state=message,
            questions=SUPPORT_QUESTIONS,
        )
    answers = response.answers

    wants_human = answers["is_human_escalation"].noul
    repeat = answers["is_repeat_contact"].noul

    if NO < wants_human < YES or NO < repeat < YES:
        # The model isn't sure either way. Let a person decide.
        send_to_review(message)
        return

    priority = "high" if repeat > YES else "normal"
    if wants_human > YES:
        route_to_agent(message, priority=priority)
    else:
        route_to_bot(message, priority=priority)
```

For the message above, the noul answer value for `is_human_escalation` is 0.99 and `is_repeat_contact` is 0.93, so the code routes it to an agent at high priority. The message "How do I reset my password?" is 0.07 on both questions and is routed to the bot.

The thresholds live in your code. If reviewers see too many messages, narrow the gap between `NO` and `YES`. If too many wrong routes get through, widen it. If you later need to know whether the message mentions a payment, or whether it contains personal data, add another Noul to `SUPPORT_QUESTIONS`. The request count stays at one.

## Structured instructions

Instructions can be an object instead of a string, with the question in one field and supplementary data in the others. [Use structure in the questions](../Concepts/How to build with TypeSafe.md#use-structure-in-the-questions) covers when that helps. Here it's used for a question built using code: a resume that has just arrived is compared against records in a candidate database that might be the same person. Each record goes into a `potential_duplicate` field as it is, the `question` is the same for every record, and all the records are checked in one request. The code-generated question keys contain each record's database ID:

```jsx

```jsx

```jsx

```jsx
<TypesafeExample
  display="request"
  example={{
state: {
  resume: {
    name: 'John Smith',
    location: 'Oakland, CA',
    summary: 'Backend engineer with eight years of Python and Go experience.',
    experience: [
      { employer: 'Google', title: 'Senior Backend Engineer', years: '2021-2025' },
      { employer: 'Microsoft', title: 'Software Engineer', years: '2017-2021' },
    ],
  },
},
selectedModels: ['jev-latest'],
questions: {
  same_as_record_18: {
    type: 'noul',
    instructions: {
      potential_duplicate: { name: 'Jon Smith', location: 'Oakland, CA', last_employer: 'Google' },
      question: 'Is the resume for the same person as `potential_duplicate`?',
    },
  },
  same_as_record_42: {
    type: 'noul',
    instructions: {
      potential_duplicate: { name: 'John Smith', location: 'Austin, TX', last_employer: 'Lone Star Freight' },
      question: 'Is the resume for the same person as `potential_duplicate`?',
    },
  },
  same_as_record_77: {
    type: 'noul',
    instructions: {
      potential_duplicate: { name: 'John Smithers', location: 'Oakland, CA', last_employer: 'Bay Health Clinic' },
      question: 'Is the resume for the same person as `potential_duplicate`?',
    },
  },
},
}}
/>
```

```

```

```

The response:

```json
{
  "model": "jev-1.13.0",
  "answers": {
    "same_as_record_18": {
      "type": "noul",
      "noul": 0.74
    },
    "same_as_record_42": {
      "type": "noul",
      "noul": 0.09
    },
    "same_as_record_77": {
      "type": "noul",
      "noul": 0.08
    }
  },
  "usage": {
    "input_tokens": 535,
    "output_tokens": 58
  }
}
```

Each answer is the probability that the resume is for the person in that record. Record 18 spells the name differently but matches on location and employer, and gets 0.74. Record 42 has the same name in a different city with a different employer, and gets 0.09. Record 77 is a similar name at the same location with a different employer, and gets 0.08. Threshold each value in your code, as in [Handling multiple Noul answers in code](#handling-multiple-noul-answers-in-code), and send the middle values to a person.

With the Python SDK, the questions are built from the candidate records. The question text is fixed and the record changes:

```python
from typesafe_sdk import Noul, TypeSafeClient

SAME_PERSON = "Is the resume for the same person as `potential_duplicate`?"

def duplicate_questions(candidates: list[dict]) -> dict[str, Noul]:
    """One Noul per candidate record, all asking the same question."""
    return {
        f"same_as_record_{candidate['id']}": Noul(
            instructions={
                "potential_duplicate": {
                    "name": candidate["name"],
                    "location": candidate["location"],
                    "last_employer": candidate["last_employer"],
                },
                "question": SAME_PERSON,
            },
        )
        for candidate in candidates
    }

def find_duplicates(resume: dict, candidates: list[dict]) -> list[str]:
    with TypeSafeClient() as client:
        response = client.system_one(
            model="jev-latest",
            state={"resume": resume},
            questions=duplicate_questions(candidates),
        )
    return [
        question_id
        for question_id, answer in response.answers.items()
        if answer.noul > 0.7
    ]
```

The [structured-data-extraction cascade cookbook](../Cookbooks/SDE cascade.md) uses structured instructions to verify an extracted record. Every field gets the same set of questions. Each question's `instructions` object has the question text in the `main_question` property. There are also `field_spec` and `extracted_field` properties that change for each field.

## Noul in the cookbooks

Take a look at our cookbooks to see apps using Noul questions:

* [Parallel questions](../Cookbooks/Parallel questions.md) runs a 13-question regulatory checklist over one article in a single request.
* [Self-consistency: nouls](../Cookbooks/Self-consistency nouls.md) scores an insurance claim against a 15-question rubric and measures how stable the values are across runs.
* [Re-ranking](../Cookbooks/Re-ranking.md) uses the probability itself, not a threshold: one Noul per query-candidate pair, then sorts candidates by the value.
* [Line-by-line search](../Cookbooks/Line-by-line search.md) pairs a Choice that finds the matching line with a Noul that checks whether the document contains an answer at all.
* [Structure recovery](../Cookbooks/Structure recovery.md) asks one Noul per pair of lines, whether a line break split a sentence, to rebuild paragraphs from plain text.
