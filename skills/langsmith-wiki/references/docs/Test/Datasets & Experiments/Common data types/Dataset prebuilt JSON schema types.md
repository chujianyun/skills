# Dataset prebuilt JSON schema types

LangSmith recommends that you set a schema on the inputs and outputs of your dataset schemas to ensure data consistency and that your examples are in the right format for downstream processing, like running evals.

In order to better support LLM workflows, LangSmith has support for a few different predefined prebuilt types. These schemas are hosted publicly by the LangSmith API, and can be defined in your dataset schemas using [JSON Schema references](https://json-schema.org/understanding-json-schema/structuring#dollarref). The table of available schemas can be seen below

| Type | JSON Schema Reference Link | Usage |
| - | - | - |
| Message | [https://api.smith.langchain.com/public/schemas/v1/message.json](https://api.smith.langchain.com/public/schemas/v1/message.json) | Represents messages sent to a chat model, following the OpenAI standard format. |
| Tool | [https://api.smith.langchain.com/public/schemas/v1/tooldef.json](https://api.smith.langchain.com/public/schemas/v1/tooldef.json) | Tool definitions available to chat models for function calling, defined in OpenAI's JSON Schema inspired function format. |

LangSmith lets you define a series of transformations that collect the above prebuilt types from your traces and add them to your dataset. For more info on available transformations, see our [reference](Dataset%20transformations.md)
