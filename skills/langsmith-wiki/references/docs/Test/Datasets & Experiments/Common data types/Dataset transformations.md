# Dataset transformations

LangSmith allows you to attach transformations to fields in your dataset's schema that apply to your data before it is added to your dataset, whether that be from UI, API, or run rules.

Coupled with [LangSmith's prebuilt JSON schema types](Dataset%20prebuilt%20JSON%20schema%20types.md), these allow you to do easy preprocessing of your data before saving it into your datasets.

## Transformation types

| Transformation Type | Target Types | Functionality |
| - | - | - |
| `remove_system_messages` | `Array[Message]` | Filters a list of messages to remove any system messages. |
| `convert_to_openai_message` | Message `Array[Message]` | Converts any incoming data from LangChain's internal serialization format to OpenAI's standard message format using langchain's [`convert_to_openai_messages`](https://reference.langchain.com/python/langchain-core/utils). If the target field is marked as required, and no matching message is found upon entry, it will attempt to extract a message (or list of messages) from several well-known LangSmith tracing formats (e.g., any traced LangChain [`BaseChatModel`](https://reference.langchain.com/python/langchain-core/language_models/chat_models/BaseChatModel) run or traced run from the [LangSmith OpenAI wrapper](../../../Monitor/Trace/Tracing%20setup/Manual%20instrumentation/Custom%20instrumentation.md#use-%40traceable-%2F-traceable)), and remove the original key containing the message. |
| `convert_to_openai_tool` | `Array[Tool]` Only available on top level fields in the inputs dictionary. | Converts any incoming data into OpenAI standard tool formats here using langchain's [`convert_to_openai_tool`](https://reference.langchain.com/python/langchain-core/utils/function_calling/convert_to_openai_tool) Will extract tool definitions from a run's invocation parameters if present / no tools are found at the specified key. This is useful because LangChain chat models trace tool definitions to the `extra.invocation_params` field of the run rather than inputs. |
| `remove_extra_fields` | `Object` | Removes any field not defined in the schema for this target object. |

## Chat model prebuilt schema

The main use case for transformations is to simplify collecting production traces into datasets in a format that can be standardized across model providers for usage in evaluations / few shot prompting / etc downstream.

To simplify setup of transformations for our end users, LangSmith offers a pre-defined schema that will do the following:

* Extract messages from your collected runs and transform them into the OpenAI standard format, which makes them compatible all LangChain ChatModels and most model providers' SDK for downstream evaluation and experimentation
* Extract any tools used by your LLM and add them to your example's input to be used for reproducibility in downstream evaluation

> [!TIP]
>
> Users who want to iterate on their system prompts often also add the Remove System Messages transformation on their input messages when using our Chat Model schema, which will prevent you from saving the system prompt to your dataset.

### Compatibility

The LLM run collection schema is built to collect data from LangChain [`BaseChatModel`](https://reference.langchain.com/python/langchain-core/language_models/chat_models/BaseChatModel) runs or traced runs from the [LangSmith OpenAI wrapper](../../../Monitor/Trace/Tracing%20setup/Manual%20instrumentation/Custom%20instrumentation.md#use-%40traceable-%2F-traceable).

Please contact support via [support.langchain.com](https://support.langchain.com) if you have an LLM run you are tracing that is not compatible and we can extend support.

If you want to apply transformations to other sorts of runs (for example, representing LangGraph state with message history), please define your schema directly and manually add the relevant transformations.

### Enablement

When adding a run from a tracing project or annotation queue to a dataset, if it has the LLM run type, we will apply the Chat Model schema by default.

For enablement on new datasets, see our [dataset management how-to guide](../Datasets/Create%20a%20dataset/Create%20and%20manage%20datasets%20in%20the%20UI.md).

### Specs

For the full API specs of the prebuilt schema, see the below sections:

#### Input schema

```json
{
  "type": "object",
  "properties": {
    "messages": {
      "type": "array",
      "items": {
        "$ref": "https://api.smith.langchain.com/public/schemas/v1/message.json"
      }
    },
    "tools": {
      "type": "array",
      "items": {
        "$ref": "https://api.smith.langchain.com/public/schemas/v1/tooldef.json"
      }
    }
  },
  "required": ["messages"]
}
```

#### Output schema

```json
{
  "type": "object",
  "properties": {
    "message": {
      "$ref": "https://api.smith.langchain.com/public/schemas/v1/message.json"
    }
  },
  "required": ["message"]
}
```

#### Transformations

And the transformations look as follows:

```json
[
  {
    "path": ["inputs"],
    "transformation_type": "remove_extra_fields"
  },
  {
    "path": ["inputs", "messages"],
    "transformation_type": "convert_to_openai_message"
  },
  {
    "path": ["inputs", "tools"],
    "transformation_type": "convert_to_openai_tool"
  },
  {
    "path": ["outputs"],
    "transformation_type": "remove_extra_fields"
  },
  {
    "path": ["outputs", "message"],
    "transformation_type": "convert_to_openai_message"
  }
]
```
