# How to build with TypeSafe

> Design AI-powered software by keeping code in control and giving System One narrow, structured decisions.

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

System One is TypeSafe's model for building AI-powered software, not agents. It does not generate code or choose its own next action. It provides AI primitives that embed into software, so code remains in control while the model handles common-sense judgments over unstructured data.

**Info:**

**Summary:** build a normal software workflow and insert System One only where AI is needed.

  * Keep control flow, deterministic rules, and side effects in code.
  * Break broad judgments into narrow, typed questions with explicit instructions and criteria.
  * Give each question only the context it needs.
  * Use probabilities and confidence to act, ask for review, or escalate.
  * Ask independent questions together, then compose their answers in code.

## Three software architectures

TypeSafe is designed for building **AI-powered software**, where code owns the workflow and AI handles narrow, structured decisions.


**Traditional software**

    Traditional code is a complex decision tree made from simple software primitives. Because each primitive is reliable, developers can compose them into higher-level abstractions.



**LLM agents**

    An agent processes instructions and chooses its next step. This works well when a person is monitoring the process, but every loop introduces another opportunity to go off the rails.



**AI-powered software**

    Code handles deterministic work and owns the control flow. The model appears only where the system needs programmable common sense or needs to interpret unstructured data. Each AI task is kept atomic and constrained.


  ![Traditional software, agents, and AI-powered software shown as three different system architectures.](../../assets/software-architectures-light.webp)

  <!-- Traditional software, agents, and AI-powered software shown as three different system architectures. -->

## What makes System One composable

  - **Structured**: System One is type-safe by construction. Decisions and probabilities conform to the structured software types and JSON schema your code expects, so it never has to recover a value from generated prose.

  - **Parallel**: Questions are evaluated independently and in parallel. One primitive's result does not become hidden context that changes another primitive's result.

  - **Comparable**: Outputs are sortable and can drive smart `if` statements, thresholds, and comparisons.

  - **Fast**: Most queries complete in about 100 ms. System One is fast enough for real-time request paths and user interfaces.

  - **Calibrated confidence**: [RLCD](../Getting Started/AI primer.md) communicates uncertainty through calibrated probabilities instead of tending toward overconfidence.

  - **Self-consistent**: System One is designed to return stable answers across repeated evaluations. See the [self-consistency cookbook](../Cookbooks/Self-consistency nouls.md).

Because every output is constrained to the supplied options, the model returns a full probability distribution over those options rather than inventing a value outside the schema. TypeSafe's target is a greater than 100× intelligence-to-speed-and-cost ratio; the underlying bet is that cheaper intelligence will create much more demand.

## Design a System One workflow


1. **Use code when you can**

   Keep deterministic work in code. It is reliable and cheap. Avoid agent `while` loops when a software workflow can express the same behavior.


   #### Example: keep deterministic rules in code

         ```python
      days_overdue = (today - invoice.due_date).days

      if days_overdue > 30:
          route_to_collections(invoice)
      ```


       Browse the [System One patterns](../Patterns/Patterns.md) for bounded ways to compose model decisions with code.


1. **request**

   Include only the context relevant to the current questions. This helps the model avoid distractions and context rot. Do not rely on knowledge stored in model weights when current information can come from your own knowledge base.


   #### Example: send only relevant context


   ```jsx

```jsx

```jsx

```jsx
<TypesafeExample
           title="request"
           display="request"
           example={{
         state: {
           ticket_message: 'My flight was cancelled. Can I get a refund?',
           refund_policy: 'Cancelled flights are eligible for a full refund.',
         },
         selectedModels: ['jev-latest'],
         questions: {
           policy_supports_refund: {
             type: 'noul',
             instructions:
               'Does the refund policy support the refund requested in the ticket?',
           },
         },
       }}
         />
```

```

```

   ```


1. **request**

   Use nested JSON for the `state` and `questions` fields. Point questions at specific values when that removes ambiguity, and include the backtick characters around each path inside the question.


   #### Example: reference a nested value

         Use a backticked dot-and-index path to point a question at a specific nested value, such as `support.tickets[0].message`.


   ```jsx

```jsx

```jsx

```jsx
<TypesafeExample
           title="request"
           display="request"
           example={{
         state: {
           support: {
             tickets: [
               { message: 'I was charged twice for order A-104.' },
               { message: 'How do I reset my password?' },
             ],
           },
           commerce: {
             orders: [
               {
                 id: 'A-104',
                 charges: [
                   { amount_usd: 49, status: 'captured' },
                   { amount_usd: 49, status: 'captured' },
                 ],
               },
             ],
           },
           account: {
             security: {
               password_reset:
                 'Email a reset link to the address on file.',
             },
           },
         },
         selectedModels: ['jev-latest'],
         questions: {
           duplicate_charge: {
             type: 'noul',
             instructions:
               'Do `support.tickets[0].message` and `commerce.orders[0].charges` indicate a duplicate charge?',
           },
           password_reset_supported: {
             type: 'noul',
             instructions:
               'Can `account.security.password_reset` resolve the request in `support.tickets[1].message`?',
           },
         },
       }}
         />
```

```

```

   ```


1. **Decomposed questions (good)**

   Ask the most explicit, narrow, specific, atomic questions you can. Break down complex or ill-defined questions into separate questions that each evaluate one property.


   **Info:**

   This is probably the most important concept in this guide. Broad questions hide several judgments behind one answer. Atomic questions expose those judgments so you can inspect, tune, and combine them in code.


   #### Example: decompose spam detection


   ```jsx

```jsx

```jsx

```jsx
<TypesafeExample
           title="One broad question (bad)"
           display="questions"
           example={{
         state: {
           message: {
             sender: {
               display_name: 'Acme Payroll',
               email: 'rewards@claim-bonus.example',
             },
             subject: 'Urgent: claim your employee bonus',
             body:
               'You have been selected for a $1,000 bonus. Confirm your payroll password today to receive it.',
             links: [
               {
                 text: 'Claim bonus',
                 url: 'http://claim-bonus.example/acme',
               },
             ],
           },
         },
         selectedModels: ['jev-latest'],
         questions: {
           is_spam: {
             type: 'noul',
             instructions: 'Is `message` spam?',
           },
         },
       }}
         />
```

```

```

   ```


   ```jsx

```jsx

```jsx

```jsx
<TypesafeExample
           title="Decomposed questions (good)"
           display="questions"
           example={{
         state: {
           message: {
             sender: {
               display_name: 'Acme Payroll',
               email: 'rewards@claim-bonus.example',
             },
             subject: 'Urgent: claim your employee bonus',
             body:
               'You have been selected for a $1,000 bonus. Confirm your payroll password today to receive it.',
             links: [
               {
                 text: 'Claim bonus',
                 url: 'http://claim-bonus.example/acme',
               },
             ],
           },
         },
         selectedModels: ['jev-latest'],
         questions: {
           requests_credentials: {
             type: 'noul',
             instructions:
               'Does `message.body` ask the recipient to provide a password or other login credential?',
           },
           offers_unexpected_reward: {
             type: 'noul',
             instructions:
               'Does `message.body` claim the recipient received an unexpected prize, payment, or reward?',
           },
           creates_time_pressure: {
             type: 'noul',
             instructions:
               'Does `message.subject` or `message.body` pressure the recipient to act quickly?',
           },
           sender_identity_mismatch: {
             type: 'noul',
             instructions:
               'Does the organization named in `message.sender.display_name` conflict with the domain in `message.sender.email`?',
           },
           link_domain_mismatch: {
             type: 'noul',
             instructions:
               'Does the domain in `message.links[0].url` conflict with the organization named in `message.sender.display_name`?',
           },
           disguises_link_destination: {
             type: 'noul',
             instructions:
               'Does `message.links[0].text` conceal or misrepresent the destination in `message.links[0].url`?',
           },
         },
       }}
         />
```

```

```

   ```




   #### Example: verify a tool-call trace


   ```jsx

```jsx

```jsx

```jsx
<TypesafeExample
           title="One broad question (bad)"
           display="questions"
           example={{
         state: {
           request: {
             text: "What's the weather in Seattle tomorrow in Fahrenheit?",
             location: 'Seattle, WA',
             date: '2026-09-03',
             unit: 'fahrenheit',
           },
           available_tools: {
             geocode_city: {
               description: 'Resolve a city to latitude and longitude.',
               parameters: { city: 'string' },
             },
             get_weather: {
               description: 'Get the forecast for coordinates and a date.',
               parameters: {
                 latitude: 'number',
                 longitude: 'number',
                 date: 'YYYY-MM-DD',
                 unit: ['fahrenheit', 'celsius'],
               },
             },
           },
           trace: {
             tool_calls: [
               {
                 id: 'call_1',
                 name: 'geocode_city',
                 arguments: { city: 'Seattle, WA' },
               },
               {
                 id: 'call_2',
                 name: 'get_weather',
                 arguments: {
                   latitude: 47.6062,
                   longitude: -122.3321,
                   date: '2026-09-03',
                   unit: 'celsius',
                 },
               },
             ],
             tool_results: [
               {
                 tool_call_id: 'call_1',
                 output: { latitude: 47.6062, longitude: -122.3321 },
               },
             ],
           },
         },
         selectedModels: ['jev-latest'],
         questions: {
           tool_calls_are_correct: {
             type: 'noul',
             instructions:
               'Is `trace.tool_calls` correct for `request` and `available_tools`?',
           },
         },
       }}
         />
```

```

```

   ```


   ```jsx

```jsx

```jsx

```jsx
<TypesafeExample
           title="Decomposed questions (good)"
           display="questions"
           example={{
         state: {
           request: {
             text: "What's the weather in Seattle tomorrow in Fahrenheit?",
             location: 'Seattle, WA',
             date: '2026-09-03',
             unit: 'fahrenheit',
           },
           available_tools: {
             geocode_city: {
               description: 'Resolve a city to latitude and longitude.',
               parameters: { city: 'string' },
             },
             get_weather: {
               description: 'Get the forecast for coordinates and a date.',
               parameters: {
                 latitude: 'number',
                 longitude: 'number',
                 date: 'YYYY-MM-DD',
                 unit: ['fahrenheit', 'celsius'],
               },
             },
           },
           trace: {
             tool_calls: [
               {
                 id: 'call_1',
                 name: 'geocode_city',
                 arguments: { city: 'Seattle, WA' },
               },
               {
                 id: 'call_2',
                 name: 'get_weather',
                 arguments: {
                   latitude: 47.6062,
                   longitude: -122.3321,
                   date: '2026-09-03',
                   unit: 'celsius',
                 },
               },
             ],
             tool_results: [
               {
                 tool_call_id: 'call_1',
                 output: { latitude: 47.6062, longitude: -122.3321 },
               },
             ],
           },
         },
         selectedModels: ['jev-latest'],
         questions: {
           geocode_tool_is_relevant: {
             type: 'noul',
             instructions:
               'Is `trace.tool_calls[0].name` an appropriate tool for resolving `request.location`?',
           },
           geocode_location_matches: {
             type: 'noul',
             instructions:
               'Does `trace.tool_calls[0].arguments.city` match `request.location`?',
           },
           geocode_arguments_match_schema: {
             type: 'noul',
             instructions:
               'Does `trace.tool_calls[0].arguments` conform to `available_tools.geocode_city.parameters`?',
           },
           geocode_result_matches_call: {
             type: 'noul',
             instructions:
               'Does `trace.tool_results[0].tool_call_id` match `trace.tool_calls[0].id`?',
           },
           weather_tool_is_relevant: {
             type: 'noul',
             instructions:
               'Is `trace.tool_calls[1].name` an appropriate tool for answering `request.text`?',
           },
           weather_arguments_match_schema: {
             type: 'noul',
             instructions:
               'Does `trace.tool_calls[1].arguments` conform to `available_tools.get_weather.parameters`?',
           },
           weather_uses_geocoded_coordinates: {
             type: 'noul',
             instructions:
               'Do the coordinates in `trace.tool_calls[1].arguments` match those in `trace.tool_results[0].output`?',
           },
           weather_date_matches: {
             type: 'noul',
             instructions:
               'Does `trace.tool_calls[1].arguments.date` match `request.date`?',
           },
           weather_unit_matches: {
             type: 'noul',
             instructions:
               'Does `trace.tool_calls[1].arguments.unit` match `request.unit`?',
           },
         },
       }}
         />
```

```

```

   ```


1. **questions**

   Keep questions short. `instructions` and `criteria` are usually strings, and for a short, unambiguous question a string is all you need. They can also be objects or arrays. Put the question in one field and the data that guides the question in the others.

       Structure helps in these situations:

       * The question needs context or examples. A long sentence of background information or a list of example inputs belongs in named fields next to the question, where your code can add to them or swap them without rewriting the question.
       * Part of the question comes from your code. When a value comes from a database, put it in its own field instead of splicing it into a string template.
       * Several questions have similar instructions. A request takes one state and can include multiple questions. Adding supplementary data can help make questions distinct.


   #### Example: reference a record from your code

         This Noul compares a resume in the state against a record from a candidate database. The record goes into `potential_duplicate` as it is, and the question refers to it by name.


   ```jsx

```jsx

```jsx

```jsx
<TypesafeExample
           title="questions"
           display="questions"
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
               potential_duplicate: { name: 'John Smith', location: 'Oakland, California', last_employer: 'Google' },
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



       The "potential\_duplicate" data sourced from code can change over time. The "question" references it using backticks.

       The descriptions inside `criteria` can be objects too. For a Choice, each option's description can be an object that says what the option covers, what belongs to a different option, and a few examples. Use the same field names across options so the model can compare them directly.


   #### Example: define contrastive Choice criteria


   ```jsx

```jsx

```jsx

```jsx
<TypesafeExample
           title="questions"
           display="questions"
           example={{
         state: 'How many disposable virtual cards can I make per day?',
         selectedModels: ['jev-latest'],
         questions: {
           card_help_topic: {
             type: 'choice',
             instructions: {
               question:
                 'Which disposable virtual card topic is the user asking about?',
               focus: 'Classify the information the user wants.',
             },
             criteria: {
               get_disposable_virtual_card: {
                 what: 'Purpose, eligibility, or setup',
                 not_for: 'Quantity, transaction, or merchant restrictions',
                 examples: [
                   'How can I get a disposable virtual card?',
                   'What are disposable cards for?',
                 ],
               },
               disposable_card_limits: {
                 what: 'Quantity, transaction, or merchant restrictions',
                 not_for: 'Purpose, eligibility, or setup',
                 examples: [
                   'How many disposable cards can I make per day?',
                   'Where can I use a disposable card?',
                 ],
               },
             },
           },
         },
       }}
         />
```

```

```

   ```



       Each question type's page has a worked example:

       * [Noul](../Primitives/Noul.md#structured-instructions) compares one resume against several candidate records, one question per record, with the questions built in code.
       * [Choice](../Primitives/Choice.md#structured-instructions-and-criteria) describes two easily confused options with what each covers, what it's not for, and examples.
       * [Score](../Primitives/Score.md#structured-level-descriptions) gives each level a description and example situations.

       The [structured-data-extraction cascade cookbook](../Cookbooks/SDE cascade.md) shows the shared-wording case, asking the same battery of questions about every field of an extracted record.

       A short, unambiguous question or criterion can remain a string. Add structure when it separates guidance that would otherwise blur together. For the full set of places structure is accepted, see [Advanced: structure](../Primitives/Advanced structure.md).


1. **Ask a lot of questions**

   Ask many narrow, independent questions about the same state in one request. This is how you maximize effectiveness and intelligence per dollar with the API: questions run in parallel, and code can combine their signals without adding serial model round trips.

       See the [Speculative Fan-Out pattern](../Patterns/Speculative fan-out.md) and [Parallel questions cookbook](../Cookbooks/Parallel questions.md).


1. **Combine question outputs in code (or feed into a classical ML model)**

   Combine independent answers with deterministic rules or weighted sums. For learned composition, use the probabilities as features in a downstream classical machine-learning model.


   #### Example: combine signals with a weighted score

         ```python
      answers = response.answers

      # Combine independent signals into one application-specific score.
      quality = (
          0.4 * answers["answers_request"].noul
          + 0.4 * answers["citations_are_supported"].noul
          + 0.2 * (1 - answers["contradicts_context"].noul)
      )
      ```


       [Composite Scoring](../Patterns/Composite scoring.md) shows how to preserve individual judgments while combining them. If you do not have labels for a downstream model, use an ensemble of expensive reasoning models to generate them; the [AutoResearch cookbook](../Cookbooks/Autoresearch feature discovery.md) shows how to train a classical model on System One outputs.


1. **Route on uncertainty**

   Make code take different actions for confident and unconfident answers. Escalate uncertain cases to a person or a more expensive reasoning model. Test thresholds by plotting confidence against accuracy on your data.


   #### Example: route by confidence

         ```python
      answer = response.answers["card_help_topic"]

      if answer.confidence < 0.8:
          route_to_human_review(ticket)
      else:
          route_to_handler(answer.choice, ticket)
      ```


       See [Confidence](Confidence.md) and [Confidence-Gated Routing](../Patterns/Confidence-gated routing.md) for choosing thresholds and matching them to the risk of each action.

**Tip:**

Decomposition does not require more round trips. Questions over the same state run in parallel.

## Putting it all together

This support-ticket workflow keeps deterministic work in code, sends only relevant structured context, evaluates many atomic questions in one request, and composes the answers with explicit confidence gates.

```python
from typesafe_sdk import Choice, Noul, NoulCriteria, Score, TypeSafeClient

def triage_ticket(ticket, customer):
    # Handle deterministic states without calling a model.
    if ticket["status"] == "closed":
        return "no_action"

    open_orders = [
        order for order in customer["orders"] if order["status"] != "delivered"
    ]

    # Include only the structured context needed by the questions below.
    state = {
        "ticket": {
            "message": ticket["message"],
            "sender": ticket["sender"],
            "links": ticket["links"],
        },
        "customer": {
            "plan": customer["plan"],
            "open_orders": open_orders,
        },
        "policy": {
            "sensitive_credentials": ["password", "security code", "API key"],
        },
    }

    # Ask structured, atomic questions together so they run in parallel.
    questions = {
        "topic": Choice(
            instructions={
                "question": "Which team should handle `ticket.message`?",
                "focus": "Classify the customer's primary request.",
            },
            criteria={
                "billing": {
                    "what": "Charges, invoices, refunds, or subscriptions",
                    "not_for": "Order tracking or account access",
                    "examples": ["I was charged twice", "Where is my refund?"],
                },
                "orders": {
                    "what": "Order status, delivery, cancellation, or returns",
                    "not_for": "Charges or account access",
                    "examples": ["Where is my order?", "Cancel my shipment"],
                },
                "account": {
                    "what": "Login, profile, permissions, or security",
                    "not_for": "Charges or order tracking",
                    "examples": ["Reset my password", "I cannot sign in"],
                },
            },
        ),
        "requests_credentials": Noul(
            instructions={
                "question": "Does the message request a sensitive credential?",
                "compare": [
                    "`ticket.message`",
                    "`policy.sensitive_credentials`",
                ],
                "focus": "Look for a request to disclose the credential itself.",
            },
            criteria=NoulCriteria(
                true={
                    "what": "Asks the recipient to disclose a listed credential",
                    "examples": [
                        "Reply with your password",
                        "Send us your API key",
                    ],
                },
                false={
                    "what": "Does not ask the recipient to disclose a credential",
                    "not_for": "A legitimate instruction to reset a credential",
                    "examples": ["Use this link to reset your password"],
                },
            ),
        ),
        "sender_identity_mismatch": Noul(
            instructions={
                "question": "Does the claimed sender identity conflict with its domain?",
                "compare": [
                    "`ticket.sender.display_name`",
                    "`ticket.sender.email`",
                ],
                "focus": "Compare the named organization with the email domain.",
            },
            criteria=NoulCriteria(
                true={
                    "what": "Claims an organization unrelated to the email domain",
                    "examples": ["Acme Payroll sent from claim-bonus.example"],
                },
                false={
                    "what": "The identity and domain agree or make no conflicting claim",
                    "examples": ["Acme Payroll sent from acme.example"],
                },
            ),
        ),
        "unexpected_reward": Noul(
            instructions={
                "question": "Does the message announce an unexpected reward?",
                "inspect": "`ticket.message`",
                "focus": "Look for an unsolicited prize, payment, or reward claim.",
            },
            criteria=NoulCriteria(
                true={
                    "what": "Announces an unrequested prize, payment, or reward",
                    "examples": ["You were selected for a $1,000 bonus"],
                },
                false={
                    "what": "Contains no reward claim or discusses an expected payment",
                    "not_for": "A customer asking about a known refund or payroll deposit",
                    "examples": ["When will my approved refund arrive?"],
                },
            ),
        ),
        "refund_requested": Noul(
            instructions={
                "question": "Does the customer explicitly request a refund or credit?",
                "inspect": "`ticket.message`",
                "focus": "Require a requested remedy, not a billing complaint alone.",
            },
            criteria=NoulCriteria(
                true={
                    "what": "Directly asks for money back or an account credit",
                    "examples": ["Please refund the duplicate charge"],
                },
                false={
                    "what": "Does not ask for a refund or credit",
                    "not_for": "A complaint or billing question without a requested remedy",
                    "examples": ["Why was I charged twice?"],
                },
            ),
        ),
        "mentions_open_order": Noul(
            instructions={
                "question": "Does the message refer to a supplied open order?",
                "compare": [
                    "`ticket.message`",
                    "`customer.open_orders`",
                ],
                "focus": "Match an order id or other identifying details.",
            },
            criteria=NoulCriteria(
                true={
                    "what": "Refers to an open order by id or identifying details",
                    "examples": ["Where is order A-104?"],
                },
                false={
                    "what": "Does not identify any supplied open order",
                    "not_for": "A generic order question with no matching details",
                    "examples": ["How long does shipping usually take?"],
                },
            ),
        ),
        "frustration": Score(
            instructions={
                "question": "How frustrated does the customer appear?",
                "inspect": "`ticket.message`",
                "focus": "Judge expressed frustration, not issue severity.",
            },
            criteria=[
                {
                    "what": "Calm and matter-of-fact",
                    "signals": ["Neutral wording", "No complaint about the experience"],
                },
                {
                    "what": "Frustrated but civil",
                    "signals": ["Expresses annoyance", "Remains constructive"],
                },
                {
                    "what": "Very angry or threatening to leave",
                    "signals": ["Hostile language", "Threatens cancellation or churn"],
                },
            ],
        ),
    }

    with TypeSafeClient() as client:
        response = client.system_one(
            state=state,
            questions=questions,
        )

    # Compose independent spam signals with weights controlled by code.
    answers = response.answers
    spam_risk = (
        0.45 * answers["requests_credentials"].noul
        + 0.30 * answers["sender_identity_mismatch"].noul
        + 0.25 * answers["unexpected_reward"].noul
    )

    # Escalate uncertain judgments instead of guessing.
    spam_is_uncertain = 0.4 < spam_risk < 0.6
    if spam_is_uncertain or answers["topic"].confidence < 0.75:
        return route_to_human_review(ticket)
    if spam_risk >= 0.6:
        return quarantine_as_spam(ticket)

    # Let code decide which speculative answers matter on this path.
    if answers["topic"].choice == "billing":
        return route_to_billing(
            ticket,
            refund_requested=answers["refund_requested"].noul >= 0.7,
        )
    if answers["topic"].choice == "orders":
        return route_to_orders(
            ticket,
            mentions_open_order=answers["mentions_open_order"].noul >= 0.7,
        )

    priority = (
        "high"
        if answers["frustration"].confidence >= 0.7
        and answers["frustration"].score >= 1.5
        else "normal"
    )
    return route_to_account_support(ticket, priority=priority)
```
