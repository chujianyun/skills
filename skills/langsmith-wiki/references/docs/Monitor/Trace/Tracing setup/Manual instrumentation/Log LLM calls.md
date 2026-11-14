# Log LLM calls

When you call an LLM directly, outside of [LangChain](https://docs.langchain.com/oss/python/langchain/overview.md) or a LangSmith [supported integration](../Integrations/Integrations.md), you need to provide specific metadata so that LangSmith can display token counts, calculate costs, and let you open the [run](../../Observability%20concepts.md#runs) in the [Playground](../../../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Prompt%20engineering%20concepts.md#playground) with the correct provider and model.

There are four requirements for a fully functional LLM trace:

| Requirement | What to do | Enables |
| - | - | - |
| 1. Set [`run_type="llm"`](../../../Debug/Data%20type%20reference/Run%20%28span%29%20data%20format.md#run-types) | Pass `run_type="llm"` to `@traceable` | LLM-specific rendering, token/cost display |
| 2. Format inputs/outputs | Use OpenAI, Anthropic, or LangChain message format | Structured message rendering, Playground support |
| 3. Set `ls_provider` and `ls_model_name` | Pass both in `metadata` | Cost tracking, Playground model selection |
| 4. Provide token counts | Set `usage_metadata` on the run | Token counts and cost calculation |

> [!NOTE]
>
> If you are using LangChain OSS, the [OpenAI wrapper](../Integrations/LLM%20providers/Trace%20with%20OpenAI.md), or the [Anthropic wrapper](../Integrations/LLM%20providers/Trace%20with%20Anthropic.md), these details are handled automatically.
>
> The examples on this page use the `traceable` decorator/wrapper (the recommended approach for Python and JS/TS). The same requirements apply if you use the [RunTree](Custom%20instrumentation.md#use-the-runtree-api) or [API](../../../Reference/LangSmith%20REST%20API/LangSmith%20API%20reference.md) directly.

## Messages format

When tracing a custom model or a custom input/output format, it must either follow the LangChain format, OpenAI completions format or Anthropic messages format. For more details,  refer to the [OpenAI Chat Completions](https://platform.openai.com/docs/api-reference/chat/create) or [Anthropic Messages](https://platform.claude.com/docs/en/api/messages) documentation. The LangChain format is:

**LangChain format**

**messages** `array` *required*

A list of messages containing the content of the conversation.

**role** `string` *required*

Identifies the message type. One of: `system` | `reasoning` | `user` | `assistant` | `tool`

**content** `array` *required*

Content of the message. List of typed dictionaries.

**Content options**

**type** `string` *required*

One of: `text` | `image` | `file` | `audio` | `video` | `tool_call` | `server_tool_call` | `server_tool_result`.

**text**

**type** `literal('text')` *required*

**text** `string` *required*

Text content.

**annotations** `object[]`

List of annotations for the text

**extras** `object`

Additional provider-specific data.

**reasoning**

**type** `literal('reasoning')` *required*

**text** `string` *required*

Text content.

**extras** `object`

Additional provider-specific data.

**image**

**type** `literal('image')` *required*

**url** `string`

URL pointing to the image location.

**base64** `string` *required*

Base64-encoded image data.

**id** `string`

Reference ID to an externally stored image (e.g., in a provider’s file system or in a bucket).

**mime\_type** `string`

Image [MIME type](https://www.iana.org/assignments/media-types/media-types.xhtml#image) (e.g., `image/jpeg`, `image/png`).

**file (e.g., PDFs)**

**type** `literal('file')` *required*

**url** `string`

URL pointing to the file.

**base64** `string` *required*

Base64-encoded file data.

**id** `string`

Reference ID to an externally stored file (e.g., in a provider’s file system or in a bucket).

**mime\_type** `string`

File [MIME type](https://www.iana.org/assignments/media-types/media-types.xhtml#image) (e.g., `application/pdf`).

**audio**

**type** `literal('audio')` *required*

**url** `string`

URL pointing to the audio file.

**base64** `string` *required*

Base64-encoded audio data.

**id** `string`

Reference ID to an externally stored audio file (e.g., in a provider’s file system or in a bucket).

**mime\_type** `string`

Audio [MIME type](https://www.iana.org/assignments/media-types/media-types.xhtml#image) (e.g., `audio/mpeg`, `audio/wav`).

**video**

**type** `literal('video')` *required*

**url** `string`

URL pointing to the video file.

**base64** `string` *required*

Base64-encoded video data.

**id** `string`

Reference ID to an externally stored video file (e.g., in a provider’s file system or in a bucket).

**mime\_type** `string`

Video [MIME type](https://www.iana.org/assignments/media-types/media-types.xhtml#image) (e.g., `video/mp4`, `video/webm`).

**tool\_call**

**type** `literal('tool_call')` *required*

**name** `string`

**args** `object` *required*

Arguments to pass to the tool.

**id** `string`

Unique identifier for this tool call.

**server\_tool\_call**

**type** `literal('server_tool_call')` *required*

**id** `string` *required*

Unique identifier for this tool call.

**name** `string` *required*

The name of the tool to be called.

**args** `object` *required*

Arguments to pass to the tool.

**server\_tool\_result**

**type** `literal('server_tool_result')` *required*

**tool\_call\_id** `string` *required*

Identifier of the corresponding server tool call.

**id** `string`

Unique identifier for this tool call.

**status** `string` *required*

Execution status of the server-side tool. One of: `success` | `error`.

**output**

Output of the executed tool.

**tool\_call\_id** `string`

Must match the `id` of a prior `assistant` message’s `tool_calls[i]` entry. Only valid when `role` is `tool`.

**usage\_metadata** `object`

Use this field to send token counts and/or costs with your model's output. See [Provide token and cost information](Log%20LLM%20calls.md#provide-token-and-cost-information) for more details.

```python Text and reasoning
 inputs = {
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Hi, can you tell me the capital of France?"
        }
      ]
    }
  ]
}

outputs = {
  "messages": [
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "The capital of France is Paris."
        },
        {
          "type": "reasoning",
          "text": "The user is asking about..."
        }
      ]
    }
  ]
}

```

```python Tool calls
input = {
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What's the weather in San Francisco?"
        }
      ]
    }
  ]
}

outputs = {
  "messages": [
    {
      "role": "assistant",
      "content": [{"type": "tool_call", "name": "get_weather", "args": {"city": "San Francisco"}, "id": "call_1"}],
    },
    {
      "role": "tool",
      "tool_call_id": "call_1",
      "content": [
        {
          "type": "text",
          "text": "{\"temperature\": \"18°C\", \"condition\": \"Sunny\"}"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "The weather in San Francisco is 18°C and sunny."
        }
      ]
    }
  ]
}
```

```python Multimodal
inputs = {
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What breed is this dog?"
        },
        {
          "type": "image",
          "url": "https://fastly.picsum.photos/id/237/200/300.jpg?hmac=TmmQSbShHz9CdQm0NkEjx1Dyh_Y984R9LpNrpvH2D_U",
          # alternative to a url, you can provide a base64 encoded image
          # "base64": "<base64 encoded image>",
          "mime_type": "image/jpeg",
        }
      ]
    }
  ]
}

outputs = {
  "messages": [
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "This looks like a Black Labrador."
        }
      ]
    }
  ]
}
```

```python Server-side tool calls
input = {
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What is the price of AAPL?"
        }
      ]
    }
  ]
}

output = {
  "messages": [
    {
      "role": "assistant",
      "content": [
        {
          "type": "server_tool_call",
          "name": "web_search",
          "args": {
            "query": "price of AAPL",
            "type": "search"
          },
          "id": "call_1"
        },
        {
          "type": "server_tool_result",
          "tool_call_id": "call_1",
          "status": "success"
        },
        {
          "type": "text",
          "text": "The price of AAPL is $150.00"
        }
      ]
    }
  ]
}
```

## Convert custom I/O formats into LangSmith compatible formats

If you're using a custom input or output format, you can convert it to a LangSmith compatible format using `process_inputs`/`processInputs` and `process_outputs`/`processOutputs` functions on the [`@traceable` decorator](https://reference.langchain.com/python/langsmith/run_helpers/traceable) (Python) or [`traceable` function](https://reference.langchain.com/javascript/langsmith/traceable/traceable) (TS).

`process_inputs`/`processInputs` and `process_outputs`/`processOutputs` accept functions that allow you to transform the inputs and outputs of a specific trace before they are logged to LangSmith. They have access to the trace's inputs and outputs, and can return a new dictionary with the processed data.

Here's a boilerplate example of how to use `process_inputs` and `process_outputs` to convert a custom I/O format into a LangSmith compatible format:

```python expandable
class OriginalInputs(BaseModel):
    """Your app's custom request shape"""

class OriginalOutputs(BaseModel):
    """Your app's custom response shape."""

class LangSmithInputs(BaseModel):
    """The input format LangSmith expects."""

class LangSmithOutputs(BaseModel):
    """The output format LangSmith expects."""

def process_inputs(inputs: dict) -> dict:
    """Dict -> OriginalInputs -> LangSmithInputs -> dict"""

def process_outputs(output: Any) -> dict:
    """OriginalOutputs -> LangSmithOutputs -> dict"""


@traceable(run_type="llm", process_inputs=process_inputs, process_outputs=process_outputs)
def chat_model(inputs: dict) -> dict:
    """
    Your app's model call. Keeps your custom I/O shape.
    The decorators call process_* to log LangSmith-compatible format.
    """

```

## Identify a custom model in traces

When using a custom model, it is recommended to also provide the following `metadata` fields to identify the model when viewing traces and when [filtering](../../../Debug/Viewing%20%26%20managing%20traces/Filter%20traces.md).

* `ls_provider`: The provider of the model, e.g., `"openai"`, `"anthropic"`.
* `ls_model_name`: The name of the model, e.g., `"gpt-5.4-mini"`, `"claude-opus-4-8"`.

```python Python wrap
from langsmith import traceable

inputs = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "I'd like to book a table for two."},
]
output = {
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "Sure, what time would you like to book the table for?"
            }
        }
    ]
}

@traceable(
    run_type="llm",
    metadata={"ls_provider": "my_provider", "ls_model_name": "my_model"}
)
def chat_model(messages: list):
    return output

chat_model(inputs)
```

```typescript TypeScript wrap
import { traceable } from "langsmith/traceable";

const messages = [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "I'd like to book a table for two." }
];
const output = {
    choices: [
        {
            message: {
                role: "assistant",
                content: "Sure, what time would you like to book the table for?",
            },
        },
    ],
    usage_metadata: {
        input_tokens: 27,
        output_tokens: 13,
        total_tokens: 40,
    },
};

// Can also use one of:
// const output = {
//     message: {
//         role: "assistant",
//         content: "Sure, what time would you like to book the table for?"
//     }
// };
//
// const output = {
//     role: "assistant",
//     content: "Sure, what time would you like to book the table for?"
// };
//
// const output = ["assistant", "Sure, what time would you like to book the table for?"];

const chatModel = traceable(
    async ({ messages }: { messages: { role: string; content: string }[] }) => {
        return output;
    },
    {
        run_type: "llm",
        name: "chat_model",
        metadata: {
            ls_provider: "my_provider",
            ls_model_name: "my_model"
        }
    }
);

await chatModel({ messages });
```

If you implement a custom streaming `chat_model`, you can "reduce" the outputs into the same format as the non-streaming version. This is only supported in Python:

```python expandable wrap
def _reduce_chunks(chunks: list):
    all_text = "".join([chunk["choices"][0]["message"]["content"] for chunk in chunks])
    return {"choices": [{"message": {"content": all_text, "role": "assistant"}}]}

@traceable(
    run_type="llm",
    reduce_fn=_reduce_chunks,
    metadata={"ls_provider": "my_provider", "ls_model_name": "my_model"}
)
def my_streaming_chat_model(messages: list):
    for chunk in ["Hello, " + messages[1]["content"]]:
        yield {
            "choices": [
                {
                    "message": {
                        "content": chunk,
                        "role": "assistant",
                    }
                }
            ]
        }

list(
    my_streaming_chat_model(
        [
            {"role": "system", "content": "You are a helpful assistant. Please greet the user."},
            {"role": "user", "content": "assistant"},
        ],
    )
)
```

> [!TIP]
>
> Setting `ls_model_name` in your `metadata` is required for LangSmith to identify the model and calculate costs for custom LLM traces. Without it, token counts may still be recorded but costs won't be estimated.

To learn more about how to use the `metadata` fields, refer to the [Add metadata and tags](../../Configuration%20%26%20troubleshooting/Data%20%26%20privacy/Add%20metadata%20and%20tags%20to%20traces.md) guide. To customize how custom agent runs appear in the Trajectory view, see [Customize the Trajectory view](../../../Debug/Viewing%20%26%20managing%20traces/View%20traces.md#customize-the-trajectory-view).

## Provide token and cost information

Token counts enable cost calculation, which LangSmith displays in the [Tracing Projects UI](https://smith.langchain.com/projects). There are two ways to provide them:

* **Set `usage_metadata` on the run tree**: call [`get_current_run_tree()` / `getCurrentRunTree()`](../../Configuration%20%26%20troubleshooting/Advanced%20tracing%20techniques/Access%20the%20current%20run%20%28span%29%20within%20a%20traced%20function.md) inside your [`@traceable`](Custom%20instrumentation.md#use-%40traceable-%2F-traceable) function and set the `usage_metadata` field. This does not change your function's return value.
* **Return `usage_metadata` in the output**: include `usage_metadata` as a top-level key in the dictionary your function returns.

### Supported `usage_metadata` fields

| Field | Type | Description |
| - | - | - |
| `input_tokens` | `int` | Total input/prompt tokens |
| `output_tokens` | `int` | Total output/completion tokens |
| `total_tokens` | `int` | Sum of input + output (optional, can be inferred) |
| `input_token_details` | `object` | Breakdown: `cache_read`, `cache_creation`, `cache_read_over_200k`, `ephemeral_5m_input_tokens`, `ephemeral_1h_input_tokens`, `audio`, `text`, `image` |
| `output_token_details` | `object` | Breakdown: `reasoning`, `audio`, `text`, `image` |

To send costs directly (for non-linear pricing), you can also include `input_cost`, `output_cost`, and `total_cost` fields. For details on configuring model pricing and viewing costs in the UI, refer to the [Cost tracking](../../Configuration%20%26%20troubleshooting/Cost%20tracking.md) page.

## Time-to-first-token

If you are using `traceable` or one of the SDK wrappers, LangSmith will automatically populate time-to-first-token for streaming LLM runs. However, if you are using the [`RunTree` API](Custom%20instrumentation.md#use-the-runtree-api) directly, you will need to add a `new_token` event to the run tree in order to properly populate time-to-first-token.

Here's an example:

```python Python
from langsmith.run_trees import RunTree
run_tree = RunTree(
    name="CustomChatModel",
    run_type="llm",
    inputs={ ... }
)
run_tree.post()
llm_stream = ...
first_token = None
for token in llm_stream:
    if first_token is None:
      first_token = token
      run_tree.add_event({
        "name": "new_token"
      })
run_tree.end(outputs={ ... })
run_tree.patch()
```

```typescript TypeScript
import { RunTree } from "langsmith";
const runTree = new RunTree({
    name: "CustomChatModel",
    run_type: "llm",
    inputs: { ... },
});
await runTree.postRun();
const llmStream = ...;
let firstToken;
for (const token of llmStream) {
    if (firstToken == null) {
        firstToken = token;
        runTree.addEvent({ name: "new_token" });
    }
}
await runTree.end({
    outputs: { ... },
});
await runTree.patchRun();
```

## Related

* [Custom instrumentation](Custom%20instrumentation.md): core `@traceable` and `RunTree` patterns.
* [Access the current run (span) within a traced function](../../Configuration%20%26%20troubleshooting/Advanced%20tracing%20techniques/Access%20the%20current%20run%20%28span%29%20within%20a%20traced%20function.md): using `get_current_run_tree()` to set `usage_metadata` and other fields at runtime.
* [Trace OpenAI applications](../Integrations/LLM%20providers/Trace%20with%20OpenAI.md): automatic token and cost tracking when using the OpenAI wrapper.
* [Trace Anthropic applications](../Integrations/LLM%20providers/Trace%20with%20Anthropic.md): automatic token and cost tracking when using the Anthropic wrapper.
* [Integrations overview](../Integrations/Integrations.md): full list of providers and frameworks with built-in LangSmith support.
