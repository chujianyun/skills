# Custom instrumentation

> Instrument your code directly to control which functions are traced and how they appear in LangSmith.

Adding [instrumentation](../../Observability%20concepts.md#manual-instrumentation) directly to your code gives you precise control over which functions your agent traces, what inputs and outputs are logged, and how your [trace](../../Observability%20concepts.md#traces) hierarchy is structured. The three core instrumentation approaches are:

* [`@traceable` decorator](#use-%40traceable-%2F-traceable): recommended for most cases
* [`trace` context manager](#use-the-trace-context-manager-python-only): Python only
* [`RunTree` API](#use-the-runtree-api): explicit, low-level control

This page also covers:

* [Specifying a custom run ID](#specify-a-custom-run-id), which is useful for attaching feedback immediately after a run or correlating with external systems.
* [Ensuring all traces are submitted](#ensure-all-traces-are-submitted-before-exiting) before your process exits.

For LangChain (Python or JS/TS), refer to the [LangChain-specific instructions](../Integrations/Agent%20frameworks/Trace%20LangChain%20agents%20%28Python%20and%20JS-TS%29.md).

If you're using an LLM provider or agent framework with a built-in LangSmith integration, refer to the [integrations overview](../Integrations/Integrations.md) instead

## Prerequisites

Before tracing, set the following environment variables:

* `LANGSMITH_TRACING=true`: enables tracing. Set this to toggle tracing on and off without changing your code.

  > [!NOTE]
  >
  > `LANGSMITH_TRACING` controls the `@traceable` decorator and the `trace` context manager. To override this at runtime for `@traceable` without changing environment variables, use [`tracing_context(enabled=True/False)`](#use-the-trace-context-manager-python-only) (Python) or pass `tracingEnabled` directly to `traceable` (JS/TS). [`RunTree` objects](#use-the-runtree-api) are not affected by any of these controls; they always send data to LangSmith when posted.

* `LANGSMITH_API_KEY`: your [LangSmith API key](../../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md).

* Before tracing in an [agent-based workspace](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md). Use [agent addressing](../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md): set `LANGSMITH_AGENT_ID` and `LANGSMITH_AGENT_ENVIRONMENT`. Remove legacy destination variables and overrides when using agent addressing.

## Use `@traceable` / `traceable`

Apply [`@traceable`](https://reference.langchain.com/python/langsmith/run_helpers/traceable) (Python), [`traceable`](https://reference.langchain.com/javascript/langsmith/traceable) (TypeScript), `traceable` (Kotlin) or `Tracing.traceFunction` (Java) to any function to make it a traced run. LangSmith handles context propagation across nested calls automatically.

The following example traces a simple pipeline: `run_pipeline` calls `format_prompt` to build the messages, `invoke_llm` to call the model, and `parse_output` to extract the result.

Each function is individually traced, and because they're called from within `run_pipeline` (also traced), LangSmith automatically nests them as child runs. `invoke_llm` uses `run_type="llm"` to mark it as an LLM call so LangSmith can render token counts and latency correctly:

```python Python
from langsmith import traceable
from openai import Client

openai = Client()

@traceable
def format_prompt(subject):
  return [
      {
          "role": "system",
          "content": "You are a helpful assistant.",
      },
      {
          "role": "user",
          "content": f"What's a good name for a store that sells {subject}?"
      }
  ]

@traceable(run_type="llm")
def invoke_llm(messages):
  return openai.chat.completions.create(
      messages=messages, model="gpt-5.4-mini", temperature=0
  )

@traceable
def parse_output(response):
  return response.choices[0].message.content

@traceable
def run_pipeline():
  messages = format_prompt("colorful socks")
  response = invoke_llm(messages)
  return parse_output(response)

run_pipeline()
```

```typescript TypeScript
import { traceable } from "langsmith/traceable";
import OpenAI from "openai";

const openai = new OpenAI();

const formatPrompt = traceable((subject: string) => {
  return [
    {
      role: "system" as const,
      content: "You are a helpful assistant.",
    },
    {
      role: "user" as const,
      content: `What's a good name for a store that sells ${subject}?`,
    },
  ];
},{ name: "formatPrompt" });

const invokeLLM = traceable(
  async ({ messages }: { messages: { role: string; content: string }[] }) => {
      return openai.chat.completions.create({
          model: "gpt-5.4-mini",
          messages: messages,
          temperature: 0,
      });
  },
  { run_type: "llm", name: "invokeLLM" }
);

const parseOutput = traceable(
  (response: any) => {
      return response.choices[0].message.content;
  },
  { name: "parseOutput" }
);

const runPipeline = traceable(
  async () => {
      const messages = await formatPrompt("colorful socks");
      const response = await invokeLLM({ messages });
      return parseOutput(response);
  },
  { name: "runPipeline" }
);

await runPipeline();
```

```java Java
import com.langchain.smith.tracing.RunType;
import com.langchain.smith.tracing.TraceConfig;
import com.langchain.smith.tracing.Tracing;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.ChatModel;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;
import com.openai.models.chat.completions.ChatCompletionMessageParam;
import com.openai.models.chat.completions.ChatCompletionSystemMessageParam;
import com.openai.models.chat.completions.ChatCompletionUserMessageParam;
import java.util.Arrays;
import java.util.List;
import java.util.function.Function;

public class TraceablePipeline {
  public static void main(String[] args) {
    new TraceablePipelineRunner().run();
  }

  private static final class TraceablePipelineRunner {
    private final OpenAIClient openai = OpenAIOkHttpClient.fromEnv();

    private final Function<String, List<ChatCompletionMessageParam>> formatPrompt =
        Tracing.traceFunction(
            subject ->
                Arrays.asList(
                    ChatCompletionMessageParam.ofSystem(
                        ChatCompletionSystemMessageParam.builder()
                            .content("You are a helpful assistant.")
                            .build()),
                    ChatCompletionMessageParam.ofUser(
                        ChatCompletionUserMessageParam.builder()
                            .content("What's a good name for a store that sells " + subject + "?")
                            .build())),
            TraceConfig.builder().name("format_prompt").build());

    private final Function<List<ChatCompletionMessageParam>, ChatCompletion> invokeLlm =
        Tracing.traceFunction(
            messages ->
                openai.chat()
                    .completions()
                    .create(
                        ChatCompletionCreateParams.builder()
                            .model(ChatModel.GPT_5_5)
                            .messages(messages)
                            .build()),
            TraceConfig.builder().name("invoke_llm").runType(RunType.LLM).build());

    private final Function<ChatCompletion, String> parseOutput =
        Tracing.traceFunction(
            response -> response.choices().get(0).message().content().orElse(""),
            TraceConfig.builder().name("parse_output").build());

    private final Function<String, String> runPipeline =
        Tracing.traceFunction(
            subject -> parseOutput.apply(invokeLlm.apply(formatPrompt.apply(subject))),
            TraceConfig.builder().name("run_pipeline").build());

    void run() {
      runPipeline.apply("colorful socks");
    }
  }
}
```

```kotlin Kotlin
import com.langchain.smith.tracing.RunType
import com.langchain.smith.tracing.TraceConfig
import com.langchain.smith.tracing.traceable
import com.openai.client.okhttp.OpenAIOkHttpClient
import com.openai.models.ChatModel
import com.openai.models.chat.completions.ChatCompletion
import com.openai.models.chat.completions.ChatCompletionCreateParams
import com.openai.models.chat.completions.ChatCompletionMessageParam
import com.openai.models.chat.completions.ChatCompletionSystemMessageParam
import com.openai.models.chat.completions.ChatCompletionUserMessageParam
import kotlin.jvm.optionals.getOrNull

val openai = OpenAIOkHttpClient.fromEnv()

val formatPrompt =
    traceable(
        { subject: String ->
            listOf(
                ChatCompletionMessageParam.ofSystem(
                    ChatCompletionSystemMessageParam.builder()
                        .content("You are a helpful assistant.")
                        .build(),
                ),
                ChatCompletionMessageParam.ofUser(
                    ChatCompletionUserMessageParam.builder()
                        .content("What's a good name for a store that sells $subject?")
                        .build(),
                ),
            )
        },
        TraceConfig.builder().name("format_prompt").build(),
    )

val invokeLlm =
    traceable(
        { messages: List<ChatCompletionMessageParam> ->
            openai.chat().completions().create(
                ChatCompletionCreateParams.builder()
                    .model(ChatModel.GPT_5_5)
                    .messages(messages)
                    .build(),
            )
        },
        TraceConfig.builder().name("invoke_llm").runType(RunType.LLM).build(),
    )

val parseOutput =
    traceable(
        { response: ChatCompletion ->
            response.choices()[0].message().content().getOrNull().orEmpty()
        },
        TraceConfig.builder().name("parse_output").build(),
    )

val runPipeline =
    traceable(
        { subject: String -> parseOutput(invokeLlm(formatPrompt(subject))) },
        TraceConfig.builder().name("run_pipeline").build(),
    )

println(runPipeline("colorful socks"))
```

In the [UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-annotate-code), you'll find a `run_pipeline` trace with `format_prompt`, `invoke_llm`, and `parse_output` as nested child runs.

> [!NOTE]
>
> When you wrap a sync function with `traceable` (e.g., `formatPrompt` in the previous example), use the `await` keyword when calling it to ensure the trace is logged correctly.

## Use the `trace` context manager (Python only)

In Python, you can use the `trace` context manager to log traces to LangSmith. This is useful in situations where:

1. You want to log traces for a specific block of code.
2. You want control over the inputs, outputs, and other attributes of the trace.
3. It is not feasible to use a decorator or wrapper.
4. Any or all of the above.

The context manager integrates seamlessly with the `traceable` decorator and `wrap_openai` wrapper, so you can use them together in the same agent.

The following example shows all three used together. `wrap_openai` wraps the OpenAI client so its calls are traced automatically. `my_tool` uses `@traceable` with `run_type="tool"` and a custom `name` to appear correctly in the trace. `chat_pipeline` itself is not decorated; instead, `ls.trace` wraps the call, letting you pass the agent address and inputs explicitly and set outputs manually via `rt.end()`:

```python
import openai
import langsmith as ls
from langsmith.wrappers import wrap_openai

client = wrap_openai(openai.Client())

@ls.traceable(run_type="tool", name="Retrieve Context")
def my_tool(question: str) -> str:
    return "During this morning's meeting, we solved all world conflict."

def chat_pipeline(question: str):
    context = my_tool(question)
    messages = [
        { "role": "system", "content": "You are a helpful assistant. Please respond to the user's request only based on the given context." },
        { "role": "user", "content": f"Question: {question}\nContext: {context}"}
    ]
    chat_completion = client.chat.completions.create(
        model="gpt-5.4-mini", messages=messages
    )
    return chat_completion.choices[0].message.content

app_inputs = {"input": "Can you summarize this morning's meetings?"}

with ls.trace("Chat Pipeline", "chain", address=ls.agent_address("<your-agent-id>", "production"), inputs=app_inputs) as rt:
    output = chat_pipeline("Can you summarize this morning's meetings?")
    rt.end(outputs={"output": output})
```

## Use the `RunTree` API

Another, more explicit way to log traces to LangSmith is via the `RunTree` API. This API allows you more control over your tracing. You can manually create runs and children runs to assemble your trace. You still need to set your `LANGSMITH_API_KEY`, but `LANGSMITH_TRACING` is not necessary for this method.

This method is not recommended for most use cases; manually managing trace context is error-prone compared to `@traceable`, which handles context propagation automatically.

```python Python
import openai
from langsmith.run_trees import RunTree

# This can be a user input to your app
question = "Can you summarize this morning's meetings?"

# Create a top-level run
pipeline = RunTree(
  name="Chat Pipeline",
  run_type="chain",
  inputs={"question": question}
)
pipeline.post()

# This can be retrieved in a retrieval step
context = "During this morning's meeting, we solved all world conflict."
messages = [
  { "role": "system", "content": "You are a helpful assistant. Please respond to the user's request only based on the given context." },
  { "role": "user", "content": f"Question: {question}\nContext: {context}"}
]

# Create a child run
child_llm_run = pipeline.create_child(
  name="OpenAI Call",
  run_type="llm",
  inputs={"messages": messages},
)
child_llm_run.post()

# Generate a completion
client = openai.Client()
chat_completion = client.chat.completions.create(
  model="gpt-5.4-mini", messages=messages
)

# End the runs and log them
child_llm_run.end(outputs=chat_completion)
child_llm_run.patch()
pipeline.end(outputs={"answer": chat_completion.choices[0].message.content})
pipeline.patch()
```

```typescript TypeScript
import OpenAI from "openai";
import { RunTree } from "langsmith";

// This can be a user input to your app
const question = "Can you summarize this morning's meetings?";

const pipeline = new RunTree({
  name: "Chat Pipeline",
  run_type: "chain",
  inputs: { question }
});
await pipeline.postRun();

// This can be retrieved in a retrieval step
const context = "During this morning's meeting, we solved all world conflict.";
const messages = [
  { role: "system", content: "You are a helpful assistant. Please respond to the user's request only based on the given context." },
  { role: "user", content: `Question: ${question}Context: ${context}` }
];

// Create a child run
const childRun = await pipeline.createChild({
  name: "OpenAI Call",
  run_type: "llm",
  inputs: { messages },
});
await childRun.postRun();

// Generate a completion
const client = new OpenAI();
const chatCompletion = await client.chat.completions.create({
  model: "gpt-5.4-mini",
  messages: messages,
});

// End the runs and log them
childRun.end(chatCompletion);
await childRun.patchRun();
pipeline.end({ outputs: { answer: chatCompletion.choices[0].message.content } });
await pipeline.patchRun();
```

```java Java
import com.langchain.smith.client.LangsmithClient;
import com.langchain.smith.client.okhttp.LangsmithOkHttpClient;
import com.langchain.smith.tracing.RunTree;
import com.langchain.smith.tracing.RunType;
import com.langchain.smith.tracing.TraceConfig;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.ChatModel;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;
import com.openai.models.chat.completions.ChatCompletionMessageParam;
import com.openai.models.chat.completions.ChatCompletionSystemMessageParam;
import com.openai.models.chat.completions.ChatCompletionUserMessageParam;
import java.time.Instant;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class RunTreeExample {
    public static void main(String[] args) throws InterruptedException {
        LangsmithClient langsmith = LangsmithOkHttpClient.fromEnv();
        OpenAIClient openai = OpenAIOkHttpClient.fromEnv();
        ExecutorService executor = Executors.newSingleThreadExecutor();

        try {
            String question = "Can you summarize this morning's meetings?";
            String runId = "01990f3e-7f97-74c5-a9b6-8d3f7e8e2f11";

            RunTree pipeline = RunTree.builder()
                .id(runId)
                .name("Chat Pipeline")
                .runType(RunType.CHAIN)
                .inputs(Collections.singletonMap("question", question))
                .client(langsmith)
                .executor(executor)
                .build();
            pipeline.postRun();

            String context = "During this morning's meeting, we solved all world conflict.";
            List<ChatCompletionMessageParam> messages = Arrays.asList(
                ChatCompletionMessageParam.ofSystem(
                    ChatCompletionSystemMessageParam.builder()
                        .content(
                            "You are a helpful assistant. Please respond to the user's " +
                                "request only based on the given context.")
                        .build()),
                ChatCompletionMessageParam.ofUser(
                    ChatCompletionUserMessageParam.builder()
                        .content("Question: " + question + "\nContext: " + context)
                        .build()));

            RunTree childRun = pipeline.createChild(
                TraceConfig.builder().name("OpenAI Call").runType(RunType.LLM).build());
            childRun.setInputs(Collections.singletonMap("messages", messages));
            childRun.postRun();

            ChatCompletion chatCompletion = openai.chat().completions().create(
                ChatCompletionCreateParams.builder()
                    .model(ChatModel.GPT_5_5)
                    .messages(messages)
                    .build());

            String answer = chatCompletion.choices().get(0).message().content().orElse("");
            System.out.println(answer);

            childRun.setOutputs(Collections.singletonMap("response", chatCompletion.toString()));
            childRun.setEndTime(Instant.now().toString());
            childRun.patchRun();

            pipeline.setOutputs(Collections.singletonMap(
                "answer", answer));
            pipeline.setEndTime(Instant.now().toString());
            pipeline.patchRun();
        } finally {
            executor.shutdown();
            if (!executor.awaitTermination(10, TimeUnit.SECONDS)) {
                throw new IllegalStateException(
                    "Timed out waiting for LangSmith traces to submit");
            }
        }
    }
}
```

```kotlin Kotlin
import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
import com.langchain.smith.tracing.RunTree
import com.langchain.smith.tracing.RunType
import com.langchain.smith.tracing.TraceConfig
import com.openai.client.okhttp.OpenAIOkHttpClient
import com.openai.models.ChatModel
import com.openai.models.chat.completions.ChatCompletionCreateParams
import com.openai.models.chat.completions.ChatCompletionMessageParam
import com.openai.models.chat.completions.ChatCompletionSystemMessageParam
import com.openai.models.chat.completions.ChatCompletionUserMessageParam
import java.time.Instant
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit

val langsmith = LangsmithOkHttpClient.fromEnv()
val openai = OpenAIOkHttpClient.fromEnv()
val executor = Executors.newSingleThreadExecutor()

try {
    val question = "Can you summarize this morning's meetings?"
    val runId = "01990f3e-7f97-74c5-a9b6-8d3f7e8e2f11"

    val pipeline =
        RunTree.builder()
            .id(runId)
            .name("Chat Pipeline")
            .runType(RunType.CHAIN)
            .inputs(mapOf("question" to question))
            .client(langsmith)
            .executor(executor)
            .build()
    println("[run-tree-example] Posting parent run to LangSmith…")
    pipeline.postRun()

    val context = "During this morning's meeting, we solved all world conflict."
    val messages =
        listOf(
            ChatCompletionMessageParam.ofSystem(
                ChatCompletionSystemMessageParam.builder()
                    .content(
                        "You are a helpful assistant. Please respond to the user's " +
                            "request only based on the given context.",
                    )
                    .build(),
            ),
            ChatCompletionMessageParam.ofUser(
                ChatCompletionUserMessageParam.builder()
                    .content("Question: $question\nContext: $context")
                    .build(),
            ),
        )

    val childRun =
        pipeline.createChild(
            TraceConfig.builder().name("OpenAI Call").runType(RunType.LLM).build(),
        )
    childRun.inputs = mapOf("messages" to messages)
    println("[run-tree-example] Posting child run to LangSmith…")
    childRun.postRun()

    val chatCompletion =
        openai.chat().completions().create(
            ChatCompletionCreateParams.builder()
                .model(ChatModel.GPT_5_5)
                .messages(messages)
                .build(),
        )

    val answer = chatCompletion.choices()[0].message().content().orElse("")
    println("[run-tree-example] Answer:")
    println(answer)

    childRun.outputs = mapOf("response" to chatCompletion.toString())
    childRun.endTime = Instant.now().toString()
    childRun.patchRun()

    pipeline.outputs =
        mapOf(
            "answer" to answer,
        )
    pipeline.endTime = Instant.now().toString()
    pipeline.patchRun()
} finally {
    executor.shutdown()
    check(executor.awaitTermination(10, TimeUnit.SECONDS)) {
        "Timed out waiting for LangSmith traces to submit"
    }
}
```

The Java and Kotlin examples use a custom root run ID and a dedicated executor. Shutting down the executor and awaiting termination ensures the background run submissions complete before the process exits.

## Example usage

You can extend the utilities explained in the previous section to trace any code. The following code shows some example extensions.

Trace any public method in a class:

```python expandable
from typing import Any, Callable, Type, TypeVar

T = TypeVar("T")

def traceable_cls(cls: Type[T]) -> Type[T]:
    """Instrument all public methods in a class."""
    def wrap_method(name: str, method: Any) -> Any:
        if callable(method) and not name.startswith("__"):
            return traceable(name=f"{cls.__name__}.{name}")(method)
        return method

    # Handle __dict__ case
    for name in dir(cls):
        if not name.startswith("_"):
            try:
                method = getattr(cls, name)
                setattr(cls, name, wrap_method(name, method))
            except AttributeError:
                # Skip attributes that can't be set (e.g., some descriptors)
                pass

    # Handle __slots__ case
    if hasattr(cls, "__slots__"):
        for slot in cls.__slots__:  # type: ignore[attr-defined]
            if not slot.startswith("__"):
                try:
                    method = getattr(cls, slot)
                    setattr(cls, slot, wrap_method(slot, method))
                except AttributeError:
                    # Skip slots that don't have a value yet
                    pass

    return cls

@traceable_cls
class MyClass:
    def __init__(self, some_val: int):
        self.some_val = some_val

    def combine(self, other_val: int):
        return self.some_val + other_val

# See trace: https://smith.langchain.com/public/882f9ecf-5057-426a-ae98-0edf84fdcaf9/r
MyClass(13).combine(29)
```

## Specify a custom run ID

By default, LangSmith assigns a random ID to each run. You can override this when you need to know the run ID ahead of time (for example, to attach [feedback](../../../../Test/Annotation%20Queues/Feedback/Log%20user%20feedback%20using%20the%20SDK.md) immediately after a run), correlate LangSmith runs with IDs from an external system, or make runs idempotent using a deterministic ID.

> [!NOTE]
>
> Use **UUID v7** for custom run IDs. UUIDv7 embeds a timestamp, which preserves correct time-ordering of runs in a trace. The LangSmith SDK exports a `uuid7` helper (Python v0.4.43+, JS v0.3.80+):
>
> * **Python**: `from langsmith import uuid7`
> * **JS/TS**: `import { uuid7 } from 'langsmith'`
>
> Any UUID v7 string is accepted — you can use the SDK helper or your own if your system already uses UUID v7 identifiers.

Use one of the following:

* `@traceable`: pass `run_id` inside `langsmith_extra` when calling a `@traceable` function (Python), or pass `id` in the config object passed to `traceable` (TypeScript):

  ```python Python
  from langsmith import traceable, uuid7

  @traceable
  def my_pipeline(question: str) -> str:
      return "answer"

  run_id = uuid7()
  my_pipeline("What is the capital of France?", langsmith_extra={"run_id": run_id})

  # run_id can now be used to attach feedback, query the run, etc.
  ```

  ```typescript TypeScript
  import { traceable } from "langsmith/traceable";
  import { uuid7 } from "langsmith";

  const runId = uuid7();

  const myPipeline = traceable(
  async (question: string) => {
      return "answer";
  },
  { name: "my-pipeline", id: runId }
  );

  await myPipeline("What is the capital of France?");

  // runId can now be used to attach feedback, query the run, etc.
  ```

* `trace` context manager (Python only): Pass `run_id` directly to the [trace](https://reference.langchain.com/python/langsmith/run_helpers/trace) context manager constructor:

  ```python Python
  from langsmith import trace, uuid7

  run_id = uuid7()

  with trace("my-pipeline", run_id=run_id) as run:
      result = "answer"
      run.end(outputs={"result": result})

  # run_id can now be used to attach feedback, query the run, etc.
  ```

## Ensure all traces are submitted before exiting

LangSmith performs tracing in a background thread to avoid obstructing your production agent. This means that your process may end before all traces are successfully posted to LangSmith. Refer to the following options:

* If you are using LangChain, refer to the [LangChain tracing guide](../Integrations/Agent%20frameworks/Trace%20LangChain%20agents%20%28Python%20and%20JS-TS%29.md#ensure-all-traces-are-submitted-before-exiting).
* If you are using the [LangSmith SDK](../../../Reference/LangSmith%20reference.md) standalone, you can use the `flush` method before exit:

  ```python Python
  from langsmith import Client

  client = Client()

  @traceable(client=client)
  async def my_traced_func():
  # Your code here...
  pass

  try:
  await my_traced_func()
  finally:
  await client.flush()
  ```

  ```typescript TypeScript
  import { Client } from "langsmith";

  const langsmithClient = new Client({});

  const myTracedFunc = traceable(async () => {
  // Your code here...
  },{ client: langsmithClient });

  try {
  await myTracedFunc();
  } finally {
  await langsmithClient.flush();
  }
  ```

## Related

* [Observability concepts](../../Observability%20concepts.md): background on runs, traces, and the LangSmith data model
* [Run (span) data format](../../../Debug/Data%20type%20reference/Run%20%28span%29%20data%20format.md): schema reference for run fields including `dotted_order`, `trace_id`, and `parent_run_id`
* [Log user feedback using the SDK](../../../../Test/Annotation%20Queues/Feedback/Log%20user%20feedback%20using%20the%20SDK.md): common use case for pre-specifying a run ID
* [Access the current run (span) within a traced function](../../Configuration%20%26%20troubleshooting/Advanced%20tracing%20techniques/Access%20the%20current%20run%20%28span%29%20within%20a%20traced%20function.md): read or modify the active run from inside a trace
* [Configure legacy integrations](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project): configure an integration that requires `project_name`
* [Trace with API](Trace%20with%20API.md): low-level REST API alternative to the SDK
* [Tracing Basics video](https://academy.langchain.com/pages/intro-to-langsmith-preview) from the Introduction to LangSmith Course
