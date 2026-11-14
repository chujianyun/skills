# Add metadata and tags to traces

LangSmith supports sending arbitrary metadata and tags along with traces.

Tags are strings that can be used to categorize or label a trace. Metadata is a dictionary of key-value pairs that can be used to store additional information about a trace.

Both are useful for associating additional information with a trace, such as the environment in which it was executed, the user who initiated it, or an internal correlation ID. For more information on tags and metadata, see the [Concepts](../../Observability%20concepts.md#tags) page. For information on how to query traces and runs by metadata and tags, see the [Filter traces](../../../Debug/Viewing%20%26%20managing%20traces/Filter%20traces.md) page.

```python Python
import openai
import langsmith as ls
from langsmith.wrappers import wrap_openai

client = openai.Client()
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
]

    # You can set metadata & tags **statically** when decorating a function
    # Use the @traceable decorator with tags and metadata
    # Ensure that the LANGSMITH_TRACING environment variables are set for @traceable to work
    @ls.traceable(
        run_type="llm",
        name="OpenAI Call Decorator",
        tags=["my-tag"],
        metadata={"my-key": "my-value"}
    )
    def call_openai(
        messages: list[dict], model: str = "gpt-5.4-mini"
    ) -> str:
        # You can also dynamically set metadata on the parent run:
        rt = ls.get_current_run_tree()
        rt.metadata["some-conditional-key"] = "some-val"
        rt.tags.extend(["another-tag"])
        return client.chat.completions.create(
            model=model,
            messages=messages,
        ).choices[0].message.content

    call_openai(
        messages,
        # To add at **invocation time**, when calling the function.
        # via the langsmith_extra parameter
        langsmith_extra={"tags": ["my-other-tag"], "metadata": {"my-other-key": "my-value"}}
    )

    # or you can dynamically set default metadata for runs in the given scope
    # tracing_context doesn't create a span itself, but it does initialize the
    # context for child spans that are created.
    with ls.tracing_context(metadata={"default-key": "default-value"}):
        call_openai(messages)

    # Alternatively, you can use the trace context manager
    # This creates a new span with the given metadata and tags
    with ls.trace(
        name="OpenAI Call Trace",
        run_type="llm",
        inputs={"messages": messages},
        tags=["my-tag"],
        metadata={"my-key": "my-value"},
    ) as rt:
        chat_completion = client.chat.completions.create(
            model="gpt-5.4-mini",
            messages=messages,
        )
        rt.metadata["some-conditional-key"] = "some-val"
        rt.end(outputs={"output": chat_completion})

# You can use the same techniques with the wrapped client
patched_client = wrap_openai(
    client, tracing_extra={"metadata": {"my-key": "my-value"}, "tags": ["a-tag"]}
)
chat_completion = patched_client.chat.completions.create(
    model="gpt-5.4-mini",
    messages=messages,
    langsmith_extra={
        "tags": ["my-other-tag"],
        "metadata": {"my-other-key": "my-value"},
    },
)
```

```typescript TypeScript
import OpenAI from "openai";
import { traceable, getCurrentRunTree } from "langsmith/traceable";
import { wrapOpenAI } from "langsmith/wrappers";

    const client = wrapOpenAI(new OpenAI());
    const messages: OpenAI.Chat.ChatCompletionMessageParam[] = [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: "Hello!" },
    ];

    const traceableCallOpenAI = traceable(
        async (messages: OpenAI.Chat.ChatCompletionMessageParam[]) => {
            const completion = await client.chat.completions.create({
                model: "gpt-5.4-mini",
                messages,
            });
            const runTree = getCurrentRunTree();
            runTree.extra.metadata = {
                ...runTree.extra.metadata,
                someKey: "someValue",
            };
            runTree.tags = [...(runTree.tags ?? []), "runtime-tag"];
            return completion.choices[0].message.content;
        },
        {
            run_type: "llm",
            name: "OpenAI Call Traceable",
            tags: ["my-tag"],
            metadata: { "my-key": "my-value" },
        }
    );

// Call the traceable function
await traceableCallOpenAI(messages);
```

> [!TIP]
>
> **LangSmith Agent Server**: To add metadata dynamically per invocation in Agent Server deployments, we recommend using `tracing_context` in a [factory function](../../../../Deploy/Agent%20Server/Server%20customization/Rebuild%20graph%20at%20runtime.md). See [Customize tracing in deployed agents](../Agent%20%26%20environment%20settings/Conditional%20tracing.md#customize-tracing-in-deployed-agents) for examples.

## Record the code version on traces

The LangSmith SDKs can record the commit that produced a trace as a `revision_id` key in the metadata of every run.

The SDK reads `revision_id` from the `LANGSMITH_REVISION_ID` environment variable. When that is unset, it reads `LANGCHAIN_REVISION_ID`, the legacy name. A `revision_id` set explicitly in run metadata takes precedence over both.

Set the environment variable when you build or deploy your application. For example, in a Dockerfile:

```dockerfile
ARG GIT_SHA
ENV LANGSMITH_REVISION_ID=$GIT_SHA
```

Then pass the commit when building the image:

```bash
docker build --build-arg GIT_SHA=$(git rev-parse HEAD) .
```

To find the traces from a given commit, filter on the `revision_id` metadata key. See [Filter traces](../../../Debug/Viewing%20%26%20managing%20traces/Filter%20traces.md).
