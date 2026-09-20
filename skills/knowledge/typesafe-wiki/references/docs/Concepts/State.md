# State

> What state is, how to structure it, and how to give a System One model the context it needs.

**State** is the content you ask a System One model to evaluate. It could be a support message, a passage of text, or the current state of your application. You pass it in the `state` field of an API request, alongside the questions you want answered.

Each request evaluates one state against one or more questions. All questions see the same state and are evaluated independently. You can mix [Choice](../Primitives/Choice.md), [Score](../Primitives/Score.md), and [Noul](../Primitives/Noul.md) questions in one request.

## State can be a simple string or a structured JSON value

The simplest state is a plain string:

```python
state = "My card was charged twice."
```

State can also be a JSON object or array containing related context, examples, and other information that helps the model answer the associated questions. Think of state as the material you would present to a panel of experts before asking them to make a judgment. In Python, pass the corresponding string, dictionary, or list directly to `client.system_one(state=...)`.

| Format | Useful for                                          | Example                                                                 |
| ------ | --------------------------------------------------- | ----------------------------------------------------------------------- |
| String | A message, article, or passage                      | `"My card was charged twice."`                                          |
| Object | Named fields, related records, or application state | `{"message": "My card was charged twice.", "order_id": "A-104"}`        |
| Array  | A sequence of messages or records                   | `["Hi", "My customer number is TS1337.", "My card was charged twice."]` |

Use an object for most requests so each part of the state has a descriptive name and its relationships remain clear. A string is suitable when the use case is simple and requires only one piece of text.

**Note:**

Jev accepts text only. State must be a string, JSON object, or array of text values. Images, audio, and video are not supported (yet). Jev's primary training language is English; other languages, including CJK scripts, are accepted but currently have lower accuracy — see [Models](../Models.md#language-support).

```json
{
  "ticket": {
    "subject": "Duplicate charge",
    "messages": [
      {"from": "customer", "text": "I was charged twice for order A-104. Please refund the duplicate."},
      {"from": "support", "text": "We are checking the charges."}
    ]
  },
  "order": {
    "id": "A-104",
    "charges": [
      {"amount_usd": 49, "status": "captured"},
      {"amount_usd": 49, "status": "captured"}
    ]
  },
  "refund_policy": "Duplicate charges are eligible for a refund."
}
```

This object is one state, even though it contains a conversation, an order, and a policy. Put related information together when the decision requires comparing those parts.

## Separate content from questions

The state contains the content and supporting facts. [Questions](../Primitives/Primitives (Questions).md) define the judgments the model should make about that material. For example, keep the refund request and policy in the state, then ask whether the customer requested a refund and whether the policy supports it.

See [Primitives (Questions)](../Primitives/Primitives (Questions).md) for guidance on instructions, criteria, question types, and asking several questions about one state.

See the [API reference](../API reference.md) for the request schema and [client SDKs](../SDKs/Client SDKs.md) for installation, typed inputs, and response handling.
