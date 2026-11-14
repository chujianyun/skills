# Message queues

> Queue multiple messages and manage them while the agent processes sequentially

Message queuing lets users send multiple messages in rapid succession without waiting for the agent to finish processing the current one. Each message is accepted immediately, queued for the active thread, and processed sequentially, giving you full visibility and control over the pending work.

> [!NOTE]
>
> This feature requires the [LangGraph Agent Server](https://docs.langchain.com/oss/python/langgraph/local-server.md). Run your agent locally with `langgraph dev` or [deploy it to LangSmith](https://docs.langchain.com/langsmith/deployment.md) to use this pattern.

## Why message queues?

In a typical chat interface, users must wait for the agent to finish responding before sending another message. This creates friction in several scenarios:

* **Batch questions**: a user wants to ask five related questions at once rather than waiting for each answer
* **Follow-up chains**: submitting clarifications or additional context while the agent is still working
* **Automated testing sequences**: programmatically sending a series of prompts to validate agent behavior
* **Data entry workflows**: feeding structured inputs one after another for processing

Message queuing solves this by accepting all submissions immediately and processing them in order.

This is an agent UX primitive rather than a cosmetic chat feature. The SDK keeps
track of the queue as part of the stream controller, so your UI can show pending
work, cancel stale requests, and keep the composer active while the current run
continues.

## How it works

Pass `multitaskStrategy: "enqueue"` when you want a submission to wait behind
the currently running request. While the agent is processing, queued submissions
are added to the active thread's queue. Once the current run completes, the
next queued message is dispatched automatically.

Read queue state with the companion queue helper for your framework:

| Property | Type | Description |
| - | - | - |
| `queue.entries` | `SubmissionQueueEntry[]` | Array of all pending queue entries |
| `queue.size` | `number` | Number of entries currently in the queue |
| `queue.cancel(id)` | `(id: string) => Promise<void>` | Cancel a specific queued entry by ID |
| `queue.clear()` | `() => Promise<void>` | Cancel all queued entries |

Each [SubmissionQueueEntry](https://reference.langchain.com/javascript/langchain-react/SubmissionQueueEntry) object contains:

| Field | Type | Description |
| - | - | - |
| `id` | `string` | Unique identifier for this queue entry |
| `values` | `object` | The input values (including messages) that were submitted |
| `options` | `object` | Any additional options passed with the submission |
| `createdAt` | `string` | ISO timestamp of when the entry was created |

## Setting up `useStream`

Connect [`useStream`](https://reference.langchain.com/javascript/langchain-react/index/useStream) to your agent, then pair it with the submission queue
helper for your framework. Call `stream.submit()` to send messages while a run
is in progress; pass `multitaskStrategy: "enqueue"` on submissions that should
wait behind the active request. Read `queue.entries` and `queue.size` to render
pending work, and use `queue.cancel()` or `queue.clear()` to remove items before
they start processing.

> [!NOTE]
>
> The code examples use `useStream<typeof myAgent>` for type-safe stream state. See Type inference for [Python](../Overview.md#type-inference) or [JavaScript](https://docs.langchain.com/oss/javascript/langchain/frontend/overview.md#type-inference) backends.

```tsx React
import { useStream, useSubmissionQueue } from "@langchain/react";

function Chat() {
  const stream = useStream<typeof myAgent>({
    apiUrl: "http://localhost:2024",
    assistantId: "simple_agent",
  });
  const queue = useSubmissionQueue(stream);

  const handleSubmit = (text: string) => {
    stream.submit({
      messages: [{ type: "human", content: text }],
    });
  };

  const pendingCount = queue.size;
  const entries = queue.entries;

  return (
    <div>
      <MessageList messages={stream.messages} />
      {pendingCount > 0 && <QueueList entries={entries} queue={queue} />}
      <ChatInput onSubmit={handleSubmit} />
    </div>
  );
}
```

```vue Vue
<script setup lang="ts">
import { useStream, useSubmissionQueue } from "@langchain/vue";
import { computed } from "vue";

const stream = useStream<typeof myAgent>({
  apiUrl: "http://localhost:2024",
  assistantId: "simple_agent",
});
const queue = useSubmissionQueue(stream);

function handleSubmit(text: string) {
  stream.submit({
    messages: [{ type: "human", content: text }],
  });
}

const pendingCount = computed(() => queue.size.value);
const entries = computed(() => queue.entries.value);
</script>

<template>
  <div>
    <MessageList :messages="stream.messages" />
    <QueueList v-if="pendingCount > 0" :entries="entries" :queue="queue" />
    <ChatInput @submit="handleSubmit" />
  </div>
</template>
```

```svelte Svelte
<script lang="ts">
  import { useStream, useSubmissionQueue } from "@langchain/svelte";

  const stream = useStream<typeof myAgent>({
    apiUrl: "http://localhost:2024",
    assistantId: "simple_agent",
  });
  const queue = useSubmissionQueue(stream);

  function handleSubmit(text: string) {
    stream.submit({
      messages: [{ type: "human", content: text }],
    });
  }
</script>

<div>
  <MessageList messages={stream.messages} />
  {#if queue.size > 0}
    <QueueList entries={queue.entries} {queue} />
  {/if}
  <ChatInput on:submit={(e) => handleSubmit(e.detail)} />
</div>
```

```ts Angular
import { Component } from "@angular/core";
import { injectStream, injectSubmissionQueue } from "@langchain/angular";

@Component({
  selector: "app-chat",
  template: `
    <message-list [messages]="stream.messages()" />
    @if (queue.size() > 0) {
      <queue-list [entries]="queue.entries()" [queue]="queue" />
    }
    <chat-input (onSubmit)="handleSubmit($event)" />
  `,
})
export class ChatComponent {
  stream = injectStream<typeof myAgent>({
    apiUrl: "http://localhost:2024",
    assistantId: "simple_agent",
  });
  queue = injectSubmissionQueue(this.stream);

  handleSubmit(text: string) {
    this.stream.submit({
      messages: [{ type: "human", content: text }],
    });
  }
}
```

## Displaying the queue

Build a `QueueList` component that shows each pending message with a cancel button. This gives users visibility into what's waiting and the ability to remove items they no longer need.

```tsx
function QueueList({ entries, queue }) {
  return (
    <div className="queue-panel">
      <div className="queue-header">
        <span>Queued messages ({entries.length})</span>
        <button onClick={() => queue.clear()}>Clear all</button>
      </div>
      <ul className="queue-entries">
        {entries.map((entry) => {
          const text = entry.values?.messages?.at(-1)?.content ?? "Pending...";
          return (
            <li key={entry.id} className="queue-entry">
              <span className="queue-text">{text}</span>
              <span className="queue-time">
                {new Date(entry.createdAt).toLocaleTimeString()}
              </span>
              <button
                className="queue-cancel"
                onClick={() => queue.cancel(entry.id)}
              >
                Cancel
              </button>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
```

> [!TIP]
>
> Display the first few characters of each queued message as a preview so users can quickly identify which items to cancel without reading full messages.

## Cancelling queued messages

You have two levels of cancellation:

### Cancel a single entry

Remove a specific message from the queue by its ID. The agent will skip it and move to the next entry.

```ts
await queue.cancel(entryId);
```

### Clear the entire queue

Remove all pending messages at once. Useful when the user changes context or wants to start over.

```ts
await queue.clear();
```

> [!NOTE]
>
> Cancelling a queue entry only affects messages that have **not yet started
> processing**. If the agent is already working on a message, cancelling it from
> the queue has no effect. Use `stream.stop()` to interrupt the current run.

## Chaining follow-up submissions with `onCreated`

The `onCreated` callback fires when a new run is created, giving you a hook to submit follow-up messages programmatically. This is useful for building multi-step workflows where the next question depends on the previous submission being accepted.

```ts
stream.submit(
  { messages: [{ type: "human", content: "What is quantum computing?" }] },
  {
    onCreated(run) {
      console.log("Run created:", run.runId);
      // Chain a follow-up
      stream.submit({
        messages: [{ type: "human", content: "Give me a simple analogy." }],
      });
    },
  }
);
```

This pattern naturally fills the queue. The first message starts processing
immediately, and the follow-up is queued behind it.

## Starting a new thread

When a user wants to begin a fresh conversation, update the reactive `threadId`
that you pass into the stream. Passing `null` clears the current thread binding;
the next submission creates a new thread.

```tsx React
function NewThreadButton() {
  const [threadId, setThreadId] = useState<string | null>(null);
  const stream = useStream<typeof myAgent>({ threadId, onThreadId: setThreadId });

  return (
    <button onClick={() => setThreadId(null)}>
      New conversation
    </button>
  );
}
```

```vue Vue
<script setup lang="ts">
const threadId = ref<string | null>(null);
const stream = useStream<typeof myAgent>({
  threadId,
  onThreadId: (id) => (threadId.value = id),
});
</script>

<template>
  <button @click="threadId = null">New conversation</button>
</template>
```

```svelte Svelte
<script lang="ts">
  let threadId = $state<string | null>(null);
  const stream = useStream<typeof myAgent>({
    threadId: () => threadId,
    onThreadId: (id) => (threadId = id),
  });
</script>

<button onclick={() => (threadId = null)}>New conversation</button>
```

```ts Angular
threadId = signal<string | null>(null);
stream = injectStream<typeof myAgent>({
  threadId: this.threadId,
  onThreadId: (id) => this.threadId.set(id),
});

// In template:
// <button (click)="threadId.set(null)">New conversation</button>
```

## Best practices

* **Limit queue size**: While there is no hard client-side limit on queue size,
  be mindful that very large queues can degrade user experience. Consider
  showing a warning when the queue exceeds a reasonable threshold (e.g., 10
  items).
* **Show queue position**: Number each queued item so users know the processing order.
* **Preserve input focus**: Keep the input field focused after submission so users can type the next message immediately.
* **Animate transitions**: Smoothly move items from the queue panel into the message list as they start processing.
* **Handle errors gracefully**: If a queued message fails, surface the error without blocking subsequent queue entries.
* **Debounce rapid submissions**: For automated or programmatic submissions, add a small delay between messages to avoid overwhelming the server.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/frontend/message-queues.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
