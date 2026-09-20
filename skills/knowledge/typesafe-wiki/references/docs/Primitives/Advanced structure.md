# Advanced: structure

> Instructions, Choice options, Score levels, and Noul criteria all accept JSON structure.

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

System One models are trained to understand structure.

## Where structure is allowed

Every one of these fields is an [`EntryType`](../SDKs/JavaScript/API/Type Aliases/Type Alias EntryType.md).

| Field                                   | Applies to          | Accepted shape                         |
| --------------------------------------- | ------------------- | -------------------------------------- |
| `instructions`                          | Choice, Score, Noul | `string`, `object`, `array`, or `null` |
| `criteria` values (option descriptions) | Choice              | `string`, `object`, `array`, or `null` |
| `criteria` entries (level descriptions) | Score               | `string`, `object`, `array`, or `null` |
| `criteria.true` and `criteria.false`    | Noul                | `string`, `object`, `array`, or `null` |

## When to structure a question

* **When it helps with clarity.** When a question has multiple parts, putting them in the form of JSON helps with clarity because the keys are labeled.
* **When question needs supporting data.** A schema, a taxonomy, or a database row is already JSON. Use the JSON entirely or pass in the relevant subfields instead of serializing them into a string template.

## Structured instructions

One `field` object describes the field being checked, and each question refers to it by key. The same shape drives a Noul that verifies a value, a Choice that picks one from candidates, and two Scores that place a value on a scale.

```jsx

```jsx

```jsx

```jsx
<TypesafeExample
  display="request"
  example={{
state: {
  source_text:
    'Invoice #4471 issued March 3, 2026 to Beaver Dam Logistics for $12,840.00, net 30.',
},
selectedModels: ['jev-latest'],
questions: {
  invoice_number_is_correct: {
    type: 'noul',
    instructions: {
      field: {
        name: 'invoice_number',
        type: 'string',
        description: 'The identifier printed on the invoice.',
      },
      extracted_value: '4471',
      question: 'Does `extracted_value` match the `field` as it appears in `source_text`?',
    },
  },
  customer_name: {
    type: 'choice',
    instructions: {
      field: {
        name: 'customer_name',
        type: 'string',
        description: 'The organization the invoice was issued to.',
      },
      question: 'Which option is the value of `field` in `source_text`?',
    },
    criteria: {
      'Beaver Logistics': null,
      'Dam Logistics': null,
      'Beaver Dam Logistics': null,
      'Beaver': null,
      'Dam': null,
    },
  },
  amount_due: {
    type: 'score',
    instructions: {
      field: {
        name: 'amount_due',
        type: 'number',
        unit: 'USD',
        description: 'The total the invoice asks to be paid.',
      },
      question: 'How large is the `field` value in `source_text`?',
    },
    criteria: [
      'Under $1,000',
      '$1,000 to $10,000',
      '$10,000 to $100,000',
      '$100,000 to $1,000,000',
      'Over $1,000,000',
    ],
  },
  payment_terms: {
    type: 'score',
    instructions: {
      field: {
        name: 'payment_terms',
        type: 'integer',
        unit: 'days',
        description: 'Days allowed for payment, from terms such as "net 30".',
      },
      question: 'How many days does the `field` in `source_text` allow for payment?',
    },
    criteria: [
      'Due on receipt',
      'Net 10',
      'Net 30',
      'Net 60',
      'Net 90',
    ],
  },
},
}}
/>
```

```

```

```

In code, you could loop over the potential records and build one of these questions per field, all sent in a single call. The [SDE cascade cookbook](../Cookbooks/SDE cascade.md) does something similar to this.

Arrays work too. Use one when the instruction is a list of things to check or to compare:

```json
"instructions": {
  "question": "Does the claimed sender identity conflict with the sending domain?",
  "compare": ["ticket.sender.display_name", "ticket.sender.email"],
  "focus": "Compare the named organization with the email domain."
}
```

## Structured Choice options

A Choice option description can be a structured object as well.

### JSON rubric for boundary clarification

```jsx

```jsx

```jsx

```jsx
<TypesafeExample
  display="request"
  example={{
state:
  'I ordered the standing desk two weeks ago and tracking still says label created. Was I even charged?',
selectedModels: ['jev-latest'],
questions: {
  department: {
    type: 'choice',
    instructions: {
      question: 'Which team should handle this message?',
      focus: "Classify the customer's primary request, not every topic mentioned.",
    },
    criteria: {
      billing: {
        what: 'Charges, invoices, refunds, or subscriptions',
        not_for: 'Order tracking or account access',
        examples: ['I was charged twice', 'Where is my refund?'],
      },
      orders: {
        what: 'Order status, delivery, cancellation, or returns',
        not_for: 'Charges or account access',
        examples: ['Where is my package?', 'Cancel my order'],
      },
      account: {
        what: 'Login, password, profile, or security',
        not_for: 'Charges or delivery',
        examples: ["I can't log in", 'Change my email'],
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

The example tells the model what each option does and does *not* cover. It sharpens the boundary between options.

### Walking a taxonomy

To classify into a deep taxonomy, ask one Choice per level and walk the tree in code. At each step the options are the children of the current node, and each option's value is the child's tree. Doing so lets the model see what lives under a branch before committing to it, which matters when the item belongs to a leaf whose name is not obvious from the branch name alone.

Here the state is a product listing and the first question picks a top-level department.

```jsx

```jsx

```jsx

```jsx
<TypesafeExample
  display="request"
  example={{
state:
  "32oz plastic bottle with a flip straw lid. Fits most bike cages.",
selectedModels: ['jev-latest'],
questions: {
  department: {
    type: 'choice',
    instructions: 'Which top-level department does this product belong to?',
    criteria: {
      'Sporting Goods': {
        Cycling: ['Bike Bottles & Cages', 'Bike Lights', 'Helmets'],
        Fitness: ['Yoga Mats', 'Resistance Bands'],
        Outdoor: ['Tents', 'Sleeping Bags', 'Hydration Packs'],
      },
      'Home & Kitchen': {
        Drinkware: ['Water Bottles', 'Travel Mugs', 'Tumblers'],
        Cookware: ['Pots & Pans', 'Bakeware'],
      },
      'Baby & Toddler': ['Sippy Cups', 'Bottle Warmers', 'Bibs'],
    },
  },
},
}}
/>
```

```

```

```

The bottle plausibly fits under two departments. Showing the subtrees lets the model see that both `Sporting Goods > Cycling > Bike Bottles & Cages` and `Home & Kitchen > Drinkware > Water Bottles` exist, and weigh the listing's emphasis on bike cages against everyday drinkware. The `probabilities` on this answer tell you whether the split is close enough to explore both branches.

Once a department is chosen, ask the next Choice with that department's children as the options and their subtrees as the values, and repeat until you reach a leaf. In code this could be a loop over a nested dict, where each question's `criteria` is simply the current node. The [Hierarchical Classification cookbook](../Cookbooks/Hierarchical classification.md) shows an example of a similar walk of the tree, including a beam search that keeps several candidate paths alive when the probabilities are close.

**Note:**

Subtrees can get large. If a branch is too large, trim the value to its direct children and a sample of leaves.

## Structured Score levels

Each entry in a Score `criteria` array can be an object.

```jsx

```jsx

```jsx

```jsx
<TypesafeExample
  display="request"
  example={{
state:
  'Fixed the null check in the payment handler. Also refactored the retry loop while I was in there, and bumped the SDK version since the old one had that timeout bug.',
selectedModels: ['jev-latest'],
questions: {
  pr_scope: {
    type: 'score',
    instructions: {
      question: 'How focused is this pull request description on a single change?',
      note: 'Judge the number of independent changes, not the size of any one change.',
    },
    criteria: [
      {
        summary: 'One change, clearly stated',
        signals: ['A single fix or feature', 'Nothing described as "also" or "while I was in there"'],
      },
      {
        summary: 'One main change plus a small related tweak',
        signals: ['A primary change and one minor adjacent edit', 'The tweak supports the main change'],
      },
      {
        summary: 'Several independent changes bundled together',
        signals: ['Two or more unrelated fixes or features', 'Changes that could each be their own PR'],
      },
    ],
  },
},
}}
/>
```

```

```

```

## Structured Noul criteria

Noul `criteria` is optional, and when the yes/no boundary is subtle, structured `true` and `false` descriptions let you pin it down with a definition and examples on each side.

```jsx

```jsx

```jsx

```jsx
<TypesafeExample
  display="request"
  example={{
state: {
  sender: { display_name: 'Beaver Dam Builders Ltd.', email: 'donotreply@payroll.example' },
  message:
    'Your Q3 bonus is ready. Reply with your login password so we can verify your identity and release the funds.',
},
selectedModels: ['jev-latest'],
questions: {
  requests_credentials: {
    type: 'noul',
    instructions: {
      question: 'Does the `message` ask the recipient to disclose a sensitive credential?',
      inspect: 'message',
      focus: 'Look for a request to send the credential itself, not a request to change or reset it.',
    },
    criteria: {
      true: {
        what: 'Asks the recipient to reply with, type, or send a password, PIN, one-time code, or other security sensitive answer',
        examples: ['Reply with your password', 'Send us the 6-digit code you just received'],
      },
      false: {
        what: 'No sensitive credential is requested',
        examples: ['Reset your password from the settings page', 'Your statement is ready'],
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
