# Configure threads

Many LLM applications have a chatbot-like interface in which the user and the LLM application engage in a multi-turn conversation. In order to track these conversations, you can use [*threads*](../Trace/Observability%20concepts.md#threads) in LangSmith.

## Group traces into threads

To associate traces together into a thread, you need to pass in a special `metadata` key where the value is the unique identifier for that thread. The key name should be one of:

* `session_id`
* `thread_id`

The value can be any string you want, but we recommend using **UUID v7** thread IDs.

The [LangSmith SDK](../Reference/LangSmith%20reference.md) exports a `uuid7` helper (Python v0.4.43+, JS v0.3.80+):

* **Python**: `from langsmith import uuid7`
* **JS/TS**: `import { uuid7 } from 'langsmith'`

For instructions, refer to [Add metadata and tags to traces](../Trace/Configuration%20%26%20troubleshooting/Data%20%26%20privacy/Add%20metadata%20and%20tags%20to%20traces.md).

> [!WARNING]
>
> **Important:** To ensure filtering and token counting work correctly across your entire thread, you must set the thread metadata (`session_id` or `thread_id`) on **all runs**, including child runs within a trace.
>
> If child runs don't have the thread\_id metadata, they won't be included when:
>
> * Filtering runs by thread.
> * Calculating token usage for a thread.
> * Aggregating costs across a thread.
>
> When creating child runs (e.g., using `@traceable` for nested functions or creating child spans), ensure you propagate the thread metadata to all child runs.

### Example

This example demonstrates how to log and retrieve conversation history using a structured message format to maintain long-running chats.

The example sets a `THREAD_ID` and passes it via `metadata` to the tracing wrapper, linking every run from that session into the same thread in LangSmith. Conversation history is persisted locally between turns—replace the file-based or in-memory store with a database or cache in production. The `get_chat_history` flag controls whether the pipeline continues an existing thread or starts a fresh one:

```python Python expandable wrap
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import openai
from langsmith import traceable, Client, uuid7
from langsmith.wrappers import wrap_openai

# Initialize clients
langsmith_client = Client()
client = wrap_openai(openai.Client())

# Configuration
THREAD_ID = str(uuid7())

# Using a local directory to store thread history. For production use, use a persistent storage solution.
THREADS_DIR = os.path.join(os.path.dirname(__file__), "threads")

# gets a history of all LLM calls in the thread to construct conversation history
def get_thread_history(thread_id: str) -> list:
    path = os.path.join(THREADS_DIR, f"{thread_id}.json")
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

def save_thread_history(thread_id: str, messages: list):
    os.makedirs(THREADS_DIR, exist_ok=True)
    with open(os.path.join(THREADS_DIR, f"{thread_id}.json"), "w") as f:
        json.dump(messages, f, indent=2, default=str)


@traceable(name="Chat Bot", metadata={"thread_id": THREAD_ID})
def chat_pipeline(messages: list, get_chat_history: bool = False):
    # Whether to continue an existing thread or start a new one
    if get_chat_history:
        history_messages = get_thread_history(THREAD_ID)
        # Get existing conversation history and append new messages
        all_messages = history_messages + messages
    else:
        all_messages = messages

    # Invoke the model
    chat_completion = client.chat.completions.create(
        model="gpt-5.4-mini", messages=all_messages
    )

    response_message = chat_completion.choices[0].message
    print("Response from model:", response_message)

    full_conversation = all_messages + [{"role": response_message.role, "content": response_message.content}]
    save_thread_history(THREAD_ID, full_conversation)

    return {"messages": full_conversation}


# Format message
messages = [
    {
        "content": "Hi, my name is Sally",
        "role": "user"
    }
]

# Call the chat pipeline
result = chat_pipeline(messages, get_chat_history=False)
```

```typescript TypeScript expandable wrap
import * as fs from "fs";
import * as path from "path";
import { fileURLToPath } from "url";
import * as dotenv from "dotenv";
import OpenAI from "openai";
import { traceable } from "langsmith/traceable";
import { wrapOpenAI } from "langsmith/wrappers";
import { uuid7 } from "langsmith";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Load environment variables from .env file
dotenv.config();

// Initialize client
const client = wrapOpenAI(new OpenAI());

// Configuration
const THREAD_ID = uuid7();

// Using a local directory to store thread history. For production use, use a persistent storage solution.
const THREADS_DIR = path.join(__dirname, "threads");

type Message = { role: string; content: string };

// Gets a history of all LLM calls in the thread to construct conversation history
function getThreadHistory(threadId: string): Message[] {
  const filePath = path.join(THREADS_DIR, `${threadId}.json`);
  if (!fs.existsSync(filePath)) return [];
  return JSON.parse(fs.readFileSync(filePath, "utf-8"));
}

function saveThreadHistory(threadId: string, messages: Message[]): void {
  fs.mkdirSync(THREADS_DIR, { recursive: true });
  fs.writeFileSync(
    path.join(THREADS_DIR, `${threadId}.json`),
    JSON.stringify(messages, null, 2)
  );
}

const chatPipeline = traceable(
  async function chatPipeline({ messages, get_chat_history = false }: { messages: Message[]; get_chat_history?: boolean }) {
    // Whether to continue an existing thread or start a new one
    if (get_chat_history) {
      const historyMessages = getThreadHistory(THREAD_ID);
      // Get existing conversation history and append new messages
      messages = [...historyMessages, ...messages];
    }

    // Invoke the model
    const chatCompletion = await client.chat.completions.create({
      model: "gpt-5.4-mini",
      messages,
    });

    const responseMessage = chatCompletion.choices[0].message;
    console.log("Response from model:", responseMessage);

    const fullConversation: Message[] = [
      ...messages,
      { role: responseMessage.role, content: responseMessage.content ?? "" },
    ];
    saveThreadHistory(THREAD_ID, fullConversation);

    return { messages: fullConversation };
  },
  { name: "Chat Bot", metadata: { thread_id: THREAD_ID } }
);

// Format message
const messages: Message[] = [{ role: "user", content: "Hi! My name is Sally" }];

// Call the chat pipeline
await chatPipeline({ messages, get_chat_history: false });
```

```java Java expandable wrap
import com.langchain.smith.client.LangsmithClient;
import com.langchain.smith.client.okhttp.LangsmithOkHttpClient;
import com.langchain.smith.tracing.TraceConfig;
import com.langchain.smith.tracing.Tracing;
import com.langchain.smith.wrappers.openai.OpenAITracing;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.ChatModel;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionAssistantMessageParam;
import com.openai.models.chat.completions.ChatCompletionCreateParams;
import com.openai.models.chat.completions.ChatCompletionMessageParam;
import com.openai.models.chat.completions.ChatCompletionUserMessageParam;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.function.Function;

class ThreadsChatPipeline {
  private static final String THREAD_ID = "01990f3e-7f97-74c5-a9b6-8d3f7e8e2f11";

  private static final class OpenAiResources {
    private static final LangsmithClient langsmith = LangsmithOkHttpClient.fromEnv();
    private static final ExecutorService executor = Executors.newSingleThreadExecutor();
    private static final Map<String, Object> threadMetadata = new HashMap<>();

    static {
      threadMetadata.put("thread_id", THREAD_ID);
    }

    private static final OpenAIClient openai =
        OpenAITracing.wrapOpenAI(
            OpenAIOkHttpClient.fromEnv(),
            TraceConfig.builder()
                .client(langsmith)
                .executor(executor)
                .metadata(threadMetadata)
                .build());

    private static final List<ChatCompletionMessageParam> threadHistory = new ArrayList<>();

    static final Function<ChatRequest, Map<String, List<ChatCompletionMessageParam>>> CHAT_PIPELINE =
        Tracing.traceFunction(
            request -> {
              List<ChatCompletionMessageParam> allMessages = new ArrayList<>();
              if (request.getChatHistory()) {
                allMessages.addAll(threadHistory);
              }
              allMessages.addAll(request.getMessages());

              ChatCompletion chatCompletion =
                  openai
                      .chat()
                      .completions()
                      .create(
                          ChatCompletionCreateParams.builder()
                              .model(ChatModel.GPT_5_5)
                              .messages(allMessages)
                              .build());

              String content = chatCompletion.choices().get(0).message().content().orElse("");
              List<ChatCompletionMessageParam> fullConversation = new ArrayList<>(allMessages);
              fullConversation.add(
                  ChatCompletionMessageParam.ofAssistant(
                      ChatCompletionAssistantMessageParam.builder().content(content).build()));
              threadHistory.clear();
              threadHistory.addAll(fullConversation);

              return Collections.singletonMap("messages", fullConversation);
            },
            TraceConfig.builder()
                .name("Chat Bot")
                .client(langsmith)
                .executor(executor)
                .metadata(threadMetadata)
                .build());

    private OpenAiResources() {}

    static ExecutorService executor() {
      return executor;
    }
  }

  static Function<ChatRequest, Map<String, List<ChatCompletionMessageParam>>> chatPipeline() {
    return OpenAiResources.CHAT_PIPELINE;
  }

  public static void main(String[] args) throws InterruptedException {
    try {
      List<ChatCompletionMessageParam> messages =
          Collections.singletonList(
              ChatCompletionMessageParam.ofUser(
                  ChatCompletionUserMessageParam.builder()
                      .content("Hi, my name is Sally")
                      .build()));
      chatPipeline().apply(new ChatRequest(messages, false));
    } finally {
      OpenAiResources.executor().shutdown();
      if (!OpenAiResources.executor().awaitTermination(10, TimeUnit.SECONDS)) {
        throw new IllegalStateException("Timed out waiting for LangSmith traces to submit");
      }
    }
  }

  static class ChatRequest {
    private final List<ChatCompletionMessageParam> messages;
    private final boolean getChatHistory;

    ChatRequest(List<ChatCompletionMessageParam> messages, boolean getChatHistory) {
      this.messages = messages;
      this.getChatHistory = getChatHistory;
    }

    List<ChatCompletionMessageParam> getMessages() {
      return messages;
    }

    boolean getChatHistory() {
      return getChatHistory;
    }
  }
}
```

```kotlin Kotlin expandable wrap
import com.langchain.smith.client.okhttp.LangsmithOkHttpClient
import com.langchain.smith.tracing.TraceConfig
import com.langchain.smith.tracing.traceable
import com.langchain.smith.wrappers.openai.wrapOpenAI
import com.openai.client.okhttp.OpenAIOkHttpClient
import com.openai.models.ChatModel
import com.openai.models.chat.completions.ChatCompletionAssistantMessageParam
import com.openai.models.chat.completions.ChatCompletionCreateParams
import com.openai.models.chat.completions.ChatCompletionMessageParam
import com.openai.models.chat.completions.ChatCompletionUserMessageParam
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit

val threadId = "01990f3e-7f97-74c5-a9b6-8d3f7e8e2f11"
val langsmith by lazy { LangsmithOkHttpClient.fromEnv() }
val executor by lazy { Executors.newSingleThreadExecutor() }
val threadMetadata by lazy { mapOf("thread_id" to threadId) }
val openai by lazy {
    wrapOpenAI(
        OpenAIOkHttpClient.fromEnv(),
        TraceConfig.builder()
            .client(langsmith)
            .executor(executor)
            .metadata(threadMetadata)
            .build(),
    )
}
val threadHistory = mutableListOf<ChatCompletionMessageParam>()

data class ChatRequest(
    val messages: List<ChatCompletionMessageParam>,
    val getChatHistory: Boolean = false,
)

val chatPipeline by lazy {
    traceable(
        { request: ChatRequest ->
            val allMessages =
                if (request.getChatHistory) {
                    threadHistory + request.messages
                } else {
                    request.messages
                }

            val chatCompletion =
                openai.chat().completions().create(
                    ChatCompletionCreateParams.builder()
                        .model(ChatModel.GPT_5_5)
                        .messages(allMessages)
                        .build(),
                )

            val content = chatCompletion.choices()[0].message().content().orElse("")
            val fullConversation =
                allMessages +
                    ChatCompletionMessageParam.ofAssistant(
                        ChatCompletionAssistantMessageParam.builder().content(content).build(),
                    )
            threadHistory.clear()
            threadHistory.addAll(fullConversation)

            mapOf("messages" to fullConversation)
        },
        TraceConfig.builder()
            .name("Chat Bot")
            .client(langsmith)
            .executor(executor)
            .metadata(threadMetadata)
            .build(),
    )
}

fun main() {
    try {
        val messages =
            listOf(
                ChatCompletionMessageParam.ofUser(
                    ChatCompletionUserMessageParam.builder()
                        .content("Hi, my name is Sally")
                        .build(),
                ),
            )
        chatPipeline(ChatRequest(messages))
    } finally {
        executor.shutdown()
        check(executor.awaitTermination(10, TimeUnit.SECONDS)) {
            "Timed out waiting for LangSmith traces to submit"
        }
    }
}
```

The Java and Kotlin examples use a dedicated executor. Shutting down the executor and awaiting termination ensures background trace submissions complete before the process exits.

Make the following calls to continue the conversation. By passing `get_chat_history=True` / `get_chat_history: true` / `getChatHistory = true`, you can continue the conversation from where it left off. This means that the LLM receives the entire message history and responds to it, instead of just responding to the latest message:

```python Python
# Format message
messages = [
    {
        "content": "What is my name",
        "role": "user"
    }
]

# Call the chat pipeline
result = chat_pipeline(messages, get_chat_history=True)
```

```typescript TypeScript
// Continue the conversation.
const messages: Message[] = [{ role: "user", content: "What is my name" }];

await chatPipeline({ messages, get_chat_history: true });
```

```java Java
List<ChatCompletionMessageParam> messages =
    Collections.singletonList(
        ChatCompletionMessageParam.ofUser(
            ChatCompletionUserMessageParam.builder()
                .content("What is my name")
                .build()));

ThreadsChatPipeline.chatPipeline().apply(new ThreadsChatPipeline.ChatRequest(messages, true));
```

```kotlin Kotlin
val messages =
    listOf(
        ChatCompletionMessageParam.ofUser(
            ChatCompletionUserMessageParam.builder()
                .content("What is my name")
                .build(),
        ),
    )

chatPipeline(ChatRequest(messages, getChatHistory = true))
```

Keep the conversation going. Since past messages are included, the LLM will remember the conversation:

```python Python
# Continue the conversation.
messages = [
    {
        "content": "What was the first message I sent you?",
        "role": "user"
    }
]

chat_pipeline(messages, get_chat_history=True)
```

```typescript TypeScript
// Continue the conversation.
const messages: Message[] = [{ role: "user", content: "What was the first message I sent you?" }];

await chatPipeline({ messages, get_chat_history: true });
```

```java Java
List<ChatCompletionMessageParam> messages =
    Collections.singletonList(
        ChatCompletionMessageParam.ofUser(
            ChatCompletionUserMessageParam.builder()
                .content("What was the first message I sent you?")
                .build()));

ThreadsChatPipeline.chatPipeline().apply(new ThreadsChatPipeline.ChatRequest(messages, true));
```

```kotlin Kotlin
val messages =
    listOf(
        ChatCompletionMessageParam.ofUser(
            ChatCompletionUserMessageParam.builder()
                .content("What was the first message I sent you?")
                .build(),
        ),
    )

chatPipeline(ChatRequest(messages, getChatHistory = true))
```

## View threads

You can view threads in the [UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-threads) by clicking on the **Threads** tab in any [project details](https://smith.langchain.com/tracing) page. The table shows each thread's first input, last output, start times, turn count, latency (P50/P99), token usage, cost, and feedback score.

The right panel displays aggregate stats for the project, including thread and trace counts, total and median token usage, error rate, and P50/P99 latency.

Use the **[Chat](../../Test/Datasets%20%26%20Experiments/Analyze%20experiment%20results/LangSmith%20Chat.md)** in thread views to analyze conversation threads, understand user sentiment, identify pain points, and track whether issues were resolved.

You can then click into a particular thread. You can view the thread in three different ways:

* **Trajectory** view: the conversation layer. Scan each turn as a chat-style thread showing user and assistant messages, tool calls, and subagent activity.
* **Turns** view: the per-turn summary. View each turn as a card showing its inputs and outputs, with expand/collapse and customizable input/output fields.
* **Details** view: the debugging layer. Drill into a specific run to inspect inputs, outputs, metadata, timing, errors, and child runs. The surrounding thread context stays visible so you can see where the run fits in the broader conversation.

Switch between views using the buttons at the top of the page or keyboard shortcuts `T` (Trajectory) and `D` (Details). The thread side panel defaults to the Details view. The right panel shows stats for the thread, including turn count, first and last start times, P50/P99 latency, and a cost breakdown by input and output tokens. For a full description of each view, see [View traces](Viewing%20%26%20managing%20traces/View%20traces.md).

### View feedback

Feedback scores are visible in the **Feedback** column of the threads table on the project's **Threads** tab.

Within a thread, open the Trajectory view and click the **LLM call** link in a turn's metadata row to go to the Details view for that run, where you can review feedback for the run. You can also see [thread-level feedback](../Observe/Online%20evaluators/Set%20up%20multi-turn%20online%20evaluators.md) there.

### Save thread-level filter

> [!NOTE]
>
> Thread filters look through all runs and surface a thread if at least 1 run matches the filter.

On the **Threads** tab of a project, you can [save commonly used filters](Viewing%20%26%20managing%20traces/Filter%20traces.md#save-a-filter).

## Related

* [Observability concepts](../Trace/Observability%20concepts.md#threads): background on threads and how they relate to runs and traces.
* [Add metadata and tags to traces](../Trace/Configuration%20%26%20troubleshooting/Data%20%26%20privacy/Add%20metadata%20and%20tags%20to%20traces.md): how to pass `thread_id` and other metadata keys.
* [Filter traces](Viewing%20%26%20managing%20traces/Filter%20traces.md): filter by thread metadata in the tracing UI.
* [Set up multi-turn online evaluators](../Observe/Online%20evaluators/Set%20up%20multi-turn%20online%20evaluators.md): evaluate threads rather than individual runs.
* [Log user feedback using the SDK](../../Test/Annotation%20Queues/Feedback/Log%20user%20feedback%20using%20the%20SDK.md): attach feedback to runs within a thread.
* [Create and manage datasets in the UI](../../Test/Datasets%20%26%20Experiments/Datasets/Create%20a%20dataset/Create%20and%20manage%20datasets%20in%20the%20UI.md#manually-from-a-tracing-project): add threads to a dataset.
