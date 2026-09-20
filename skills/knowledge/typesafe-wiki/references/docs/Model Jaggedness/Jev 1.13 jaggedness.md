# Jev 1.13 jaggedness

> Jev isn't perfect. Here are some jagged edges we are aware of with jev-1.13. Many of these will be fixed in later versions.

**Note:**

**Applies to `jev-1.13`.** Last reviewed 2026-09-17.

`jev-1.13` is fast, calibrated, and good at common-sense judgment but it is not perfect. `jev-1.13` does the best on [System One](../Concepts/System One.md) tasks. It may struggle with tasks that require additional levels of indirection. It can be quite literal in its understanding. It struggles with tasks that require numeric precision.

## The failure modes in detail

| # | Failure mode                                                                        | Do this instead                                                |
| - | ----------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| 1 | [Literal reading](#literal-reading)                                                 | Write the exact condition, criteria for each available options |
| 2 | [Math and Numbers](#math-and-numbers)                                               | Keep the arithmetic in code                                    |
| 3 | [Date and time comparison](#date-and-time-comparison)                               | Extract components; compare in code                            |
| 4 | [Indirection](#indirection)                                                         | Reduce hops; point to the relevant state                       |
| 5 | [Large state full of irrelevant detail](#large-state-full-of-irrelevant-detail)     | Filter first; send only what the question needs                |
| 6 | [Adversarial content](#adversarial-content)                                         | Write precise prompts, and test edge cases before deploying    |
| 7 | [Contradictory instructions and criteria](#contradictory-instructions-and-criteria) | Align the criteria and instruction                             |
| 8 | [Common-sense structural invariants](#common-sense-structural-invariants)           | Ask each decision one way; enforce identities in code          |
| 9 | [Generation](#generation)                                                           | Use a generative model                                         |

## Literal reading

`jev-1.13` answers the question you wrote, not the one you meant. Scoping words, negations, and implied conditions are read at face value. A question will be answered based on the words written in the instruction, whereas a person might have read the intent behind the instructions.

**Instead:** state the exact condition in the `instructions`. Be specific. Put boundary cases in the criteria. When you look at a wrong answer and find yourself explaining what you really meant, that explanation is the missing half of the instruction. Where interpretation is unavoidable, split it into two literal questions and combine them in code.

## Math and Numbers

Jev is not a calculator. We strongly recommend implementing any mathematical logic in code. Jev will perform better on semantic questions than mathematical ones.

### Counting

`jev-1.13` does not count reliably. This covers characters in a word, occurrences of a term in a passage, and items in a long list. The model recognizes the shape of an answer rather than tallying, and the error grows with the size of the thing being counted.

Before asking a counting question, ask why the count needs a model at all. If the unit is something a regular expression or a parser can find, the count belongs in code and the model has nothing to add.

**Instead:** count in code. When you want to count items matching some criteria, iterate in code over the candidates and ask one question for each, then add up the answers yourself.

```python
from typesafe_sdk import Noul, TypeSafeClient

client = TypeSafeClient(model="jev-1.13")
YES = 0.5  # up to you on what you want the threshold to be, depends on your usecase.

items = ["typesafe", "apple", "california", "banana", "likes", "calibration", "orange", "vertex"]

result = client.system_one(
    {"items": items},
    {
        f"item_{i}": Noul(instructions=f"Is `items[{i}]` the name of a fruit?")
        for i in range(len(items))
    },
)

count = sum(result.nouls[f"item_{i}"].noul > YES for i in range(len(items)))
```

### Numeric representations

`jev-1.13` will perform better on semantic representations than numeric. For example, questions about colors using hex values will underperform compared to those using the English names. Given RGB triples or hex values it cannot reliably judge whether two values are near each other.

Similarly, questions about high-level programming languages will perform better than questions about low level assembly, or binary encoded instructions.

**Instead:** do the conversion in code and pass in either the computed number or a named bucket. Keep the model for the part that is genuinely a judgment, such as whether a color reads as a warning.

### Math using score

Please do not use score outputs (e.g., expectations and probability) to compute the exact magnitude of a number between two levels of a criterion. You can use the expectation to check if it passes a particular threshold, but `jev-1.13`'s score levels are weak in numerical calibration. It will not be able to help you reconstruct the exact number by interpolating between the nearest two levels.

## Date and time comparison

`jev-1.13` reads dates as text, not as ordered quantities. Asking which of two dates comes first, how far apart they are, or whether one falls inside a window is unreliable. It gets worse with mixed formats, relative references and domain boundaries such as quarters, settlement windows, and accrual periods.

**Instead:** split the work. Extraction is a judgment, so give it to the model. Arithmetic is not, so keep it in code.

Every part of a date is a small closed set: twelve months, thirty-one possible days, a bounded range of years. That turns extraction into a [Choice](../Primitives/Choice.md) over enumerated options rather than free-form parsing, and it gives you somewhere to put an explicit "not stated" option so a missing part is reported rather than guessed. Code assembles the parts into a real date and owns everything after that, including ordering, duration, offset, and weekday.

The [date extraction cookbook](../Cookbooks/Date extraction.md) has the worked version, including relative dates and confidence gating.

## Indirection

Instructions carrying double negatives or complex indirection are answered less reliably. A question about a property of a property or something that requires multiple hops of reasoning costs accuracy.

**Instead:** write your instructions as directly as possible. When possible, identify the relevant parts of state by name.

## Large state full of irrelevant detail

Accuracy falls as the state grows with content unrelated to the decision. Unrelated detail acts as a distractor, and a large state makes it harder to tell which part of the input produced a wrong answer.

**Instead:** retrieve and filter in code first, and send only the fields the question needs. When it's not possible to filter in state, you can use a [Noul](../Primitives/Noul.md) to filter for relevance. The [classifying RAG passages cookbook](../Cookbooks/Classifying RAG passages.md) has a worked example.

**Note:**

**Context length limit.** `jev-1.13` has a bounded context window. See the [Models](../Models.md) page for the exact token limits.

## Adversarial content

State is data, and `jev-1.13` does not treat it as hostile by default. Content written to adversarially steer the model, whether that is an injected instruction, a deliberately misleading framing, or text that argues for its own classification, can move the answer. We expect to improve on this in the future.

**Instead:** be explicit in the criteria. Test your integration thoroughly before deploying it to many users.

## Contradictory instructions and criteria

When the `instructions` and the `criteria` ask for different things, `jev-1.13` might get confused. The best performance comes from clear phrasing. For example, a Noul where `true` maps to no and `false` maps to yes will perform worse. Aim for instructions which are easy for the average person to read and understand.

**Instead:** treat the criteria as an extension of the instruction. Align the two using clear and precise language.

## Common-sense structural invariants

`jev-1.13` is extremely consistent, meaning you should expect quantitatively similar outputs for semantically similar inputs.
However there are many structural invariants one might imagine to hold that simply aren't guaranteed by the model.

For example, "Is the customer asking for a refund?", asked as a [Noul](../Primitives/Noul.md) and as a yes/no [Choice](../Primitives/Choice.md) on the ticket "I'm not happy with the fit. What are my options here?":

| Noul `noul` | Choice `yes` | Choice `no` | Choice `confidence` |
| ----------- | ------------ | ----------- | ------------------- |
| 0.22        | 0.01         | 0.99        | 0.97                |

The comparable numbers are `noul` and `probabilities["yes"]`, and it is not obvious how to interpret either the Choice output and confidence for the Noul question or vice versa.

The same question and its negation, "Is the customer asking for something other than a refund?", as two Nouls on the ticket "I was charged twice for the same order. Can someone look into this?":

| `refund` | `not_refund` | Sum  |
| -------- | ------------ | ---- |
| 0.72     | 0.47         | 1.19 |

There are many reasons that `P(noul)` and `1 - P(not noul)` may not be directly comparable.

**Instead:** don't rely on expected structural invariance, and word questions to mean directly what you want. Don't carry a threshold tuned on a Noul over to a Choice, and don't hold the model to arithmetic identities between separate questions. A Choice over options and one Noul per option answer different questions: the Choice is relative, settling *which* option, while each Noul is absolute and can be low for all of them. The [skill suggestion cookbook](../Cookbooks/Skill suggestion.md) uses both on the same shortlist, the Choice to pick a skill and the Nouls to decide whether to suggest one at all.

## Generation

`jev-1.13` is not trained to generate text. While you can force it to by chaining choices, this will not work well and will be very slow. For data extraction, it is better to extract possible options using regex or a generative model and let `jev-1.13` pick the correct extraction.

**Instead:** when the answer space is bounded, turn extraction into a [Choice](../Primitives/Choice.md) over the options rather than asking for the value itself. If you really need to generate text... there are other models for that.

**Info:**

**As a reminder, avoid the following:**

  * Asking the model something code can compute exactly.
  * Hiding several judgments inside one question.
  * System Two tasks: more layers of indirections
  * Giving it more context in `state` than the question needs. Jev suffers from context rot, so unrelated material in the `state` costs you accuracy.

**Tip:**

Found a failure mode that belongs on this list? We want to hear about it. Reach us on [Discord](https://discord.com/invite/WUujKYBp8s).
