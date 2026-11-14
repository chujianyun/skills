# Time travel

> Inspect, navigate, and resume from any checkpoint in the conversation history

A [checkpoint](https://docs.langchain.com/oss/python/langgraph/persistence.md#checkpoints) is a saved snapshot of a
LangGraph agent's state. Time travel lets you inspect a checkpoint and continue
execution from that saved state to explore alternative paths.

> [!NOTE]
>
> This feature requires the [LangGraph Agent Server](https://docs.langchain.com/oss/python/langgraph/local-server.md). Run your agent locally with `langgraph dev` or [deploy it to LangSmith](https://docs.langchain.com/langsmith/deployment.md) to use this pattern.

## How checkpoints work

LangGraph persists agent state at super-step boundaries. Nodes that run in
parallel in the same super-step share a checkpoint boundary. Each persisted state
is a [ThreadState](https://reference.langchain.com/javascript/langchain-langgraph-sdk/index/ThreadState) object that captures:

* **checkpoint**: The checkpoint identifier, including its ID and namespace.
* **created\_at**: The snapshot creation time.
* **parent\_checkpoint**: The previous checkpoint in this path.
* **values**: The full agent state at this point (messages, custom keys).
* **tasks**: The graph nodes that were scheduled to run next.
* **next**: The names of upcoming nodes in the execution plan.

History can contain multiple execution paths, not one linear conversation.
`getHistory()` returns checkpoints newest first, with a default limit of 10.
Use `parent_checkpoint` to follow ancestry rather than treating adjacent entries
as parent and child. The examples below display the returned page of history.

## Setting up `useStream`

Create the stream for your agent, then fetch checkpoint history explicitly from
the LangGraph client for the active thread. Resuming from a checkpoint uses
`forkFrom: checkpointId`.

> [!NOTE]
>
> The code examples use `useStream<typeof myAgent>` for type-safe stream state. See Type inference for [Python](../Overview.md#type-inference) or [JavaScript](https://docs.langchain.com/oss/javascript/langchain/frontend/overview.md#type-inference) backends.

```tsx React
import { useStream } from "@langchain/react";
import { useEffect, useState } from "react";

const AGENT_URL = "http://localhost:2024";

export function TimeTravelChat() {
  const [threadId, setThreadId] = useState<string | null>(null);
  const [history, setHistory] = useState<ThreadState[]>([]);
  const stream = useStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "time_travel",
    threadId,
    onThreadId: setThreadId,
  });

  useEffect(() => {
    if (!threadId || stream.isLoading) return;
    stream.client.threads.getHistory(threadId).then(setHistory);
  }, [stream.client, threadId, stream.isLoading]);

  function resumeFrom(cp: ThreadState) {
    if (!cp.checkpoint.checkpoint_id) return;
    stream.submit(undefined, {
      forkFrom: cp.checkpoint.checkpoint_id,
    });
  }

  return (
    <div className="flex h-screen">
      <ChatPanel messages={stream.messages} />
      <TimelineSidebar history={history} onSelect={resumeFrom} />
    </div>
  );
}
```

```vue Vue
<script setup lang="ts">
import { useStream } from "@langchain/vue";
import { ref, watch } from "vue";

const AGENT_URL = "http://localhost:2024";
const threadId = ref<string | null>(null);
const history = ref<ThreadState[]>([]);

const stream = useStream<typeof myAgent>({
  apiUrl: AGENT_URL,
  assistantId: "time_travel",
  threadId,
  onThreadId: (id) => (threadId.value = id),
});

watch(
  [threadId, stream.isLoading],
  async ([id, isLoading]) => {
    if (isLoading) return;
    history.value = id
      ? ((await stream.client.threads.getHistory(id)) as ThreadState[])
      : [];
  },
  { immediate: true },
);

function resumeFrom(cp: ThreadState) {
  if (!cp.checkpoint.checkpoint_id) return;
  stream.submit(undefined, {
    forkFrom: cp.checkpoint.checkpoint_id,
  });
}
</script>

<template>
  <div class="flex h-screen">
    <ChatPanel :messages="stream.messages.value" />
    <TimelineSidebar :history="history" @select="resumeFrom" />
  </div>
</template>
```

```svelte Svelte
<script lang="ts">
  import { useStream } from "@langchain/svelte";

  const AGENT_URL = "http://localhost:2024";
  let threadId = $state<string | null>(null);
  let history = $state<ThreadState[]>([]);

  const stream = useStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "time_travel",
    threadId: () => threadId,
    onThreadId: (id) => (threadId = id),
  });

  $effect(() => {
    if (!threadId) {
      history = [];
      return;
    }
    if (stream.isLoading) return;
    stream.client.threads.getHistory(threadId).then((states) => {
      history = states as ThreadState[];
    });
  });

  function resumeFrom(cp: ThreadState) {
    if (!cp.checkpoint.checkpoint_id) return;
    stream.submit(undefined, {
      forkFrom: cp.checkpoint.checkpoint_id,
    });
  }
</script>

<div class="flex h-screen">
  <ChatPanel messages={stream.messages} />
  <TimelineSidebar {history} onSelect={resumeFrom} />
</div>
```

```ts Angular
import { Component, effect, signal } from "@angular/core";
import { injectStream } from "@langchain/angular";

const AGENT_URL = "http://localhost:2024";

@Component({
  selector: "app-time-travel-chat",
  template: `
    <div class="flex h-screen">
      <app-chat-panel [messages]="stream.messages()" />
      <app-timeline-sidebar
        [history]="history()"
        (select)="resumeFrom($event)"
      />
    </div>
  `,
})
export class TimeTravelChatComponent {
  threadId = signal<string | null>(null);
  history = signal<ThreadState[]>([]);

  stream = injectStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "time_travel",
    threadId: this.threadId,
    onThreadId: (id) => this.threadId.set(id),
  });

  constructor() {
    effect(() => {
      if (this.stream.isLoading()) return;
      void this.refreshHistory(this.threadId());
    });
  }

  async refreshHistory(id: string | null) {
    this.history.set(id
      ? ((await this.stream.client.threads.getHistory(id)) as ThreadState[])
      : []);
  }

  resumeFrom(cp: ThreadState) {
    if (!cp.checkpoint.checkpoint_id) return;
    this.stream.submit(undefined, {
      forkFrom: cp.checkpoint.checkpoint_id,
    });
  }
}
```

## Building a checkpoint timeline

The timeline sidebar shows every checkpoint as a clickable entry. Each entry
displays the scheduled nodes and how many messages existed at that point.
`tasks` describes work for the next step, not the nodes that produced the
checkpoint. Use `next` to label all scheduled nodes, including parallel work:

```tsx
function TimelineSidebar({
  history,
  onSelect,
}: {
  history: ThreadState[];
  onSelect: (cp: ThreadState) => void;
}) {
  return (
    <aside className="w-80 overflow-y-auto border-l bg-gray-50 p-4">
      <h2 className="mb-4 text-sm font-semibold uppercase text-gray-500">
        Checkpoint Timeline
      </h2>
      <div className="space-y-2">
        {history.map((cp, i) => {
          const nextNodes = cp.next?.join(", ") || "Complete";
          const msgCount = (cp.values?.messages as unknown[])?.length ?? 0;

          return (
            <button
              key={cp.checkpoint.checkpoint_id}
              onClick={() => onSelect(cp)}
              className="w-full rounded-lg border bg-white p-3 text-left
                         hover:border-blue-400 hover:shadow-sm transition-all"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-400">#{i + 1}</span>
                <NodeBadge name={nextNodes} />
              </div>
              <p className="mt-1 text-sm font-medium">Next: {nextNodes}</p>
              <p className="text-xs text-gray-500">
                {msgCount} message{msgCount !== 1 ? "s" : ""}
              </p>
            </button>
          );
        })}
      </div>
    </aside>
  );
}
```

## Inspecting checkpoint state

Clicking a checkpoint should show the full state at that point. A JSON viewer
gives developers complete visibility into what the agent knew and decided:

```tsx
function CheckpointInspector({ checkpoint }: { checkpoint: ThreadState }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="rounded-lg border bg-white p-4">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold">
          Checkpoint {checkpoint.checkpoint.checkpoint_id?.slice(0, 8)}...
        </h3>
        <button
          onClick={() => setExpanded(!expanded)}
          className="text-sm text-blue-600 hover:underline"
        >
          {expanded ? "Collapse" : "Expand"} state
        </button>
      </div>

      <div className="mt-2 space-y-1 text-sm">
        <p>
          <strong>Next:</strong>{" "}
          {checkpoint.next?.join(", ") || "—"}
        </p>
        <p>
          <strong>Messages:</strong>{" "}
          {(checkpoint.values?.messages as unknown[])?.length ?? 0}
        </p>
      </div>

      {expanded && (
        <div className="mt-3 max-h-96 overflow-auto rounded bg-gray-900 p-3">
          <pre className="text-xs text-gray-200">
            {JSON.stringify(checkpoint.values, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
```

> [!TIP]
>
> For production UIs, consider using a proper JSON viewer component with
> collapsible nodes instead of raw `JSON.stringify`. Libraries like
> `react-json-view` or `react-json-tree` give users a much better exploration
> experience.

## Resuming from a checkpoint

The core of time travel is the ability to **resume execution from any prior
checkpoint**. When a user selects a checkpoint, call `submit` with `undefined`
input and pass the checkpoint ID as `forkFrom`:

```ts
const checkpointId = selectedCheckpoint.checkpoint.checkpoint_id;
if (checkpointId) {
  stream.submit(undefined, { forkFrom: checkpointId });
}
```

The SDK sends `undefined` or `null` input as `null`, which continues from the
selected checkpoint without supplying new input. An empty object (`{}`) is new
input, not the same continuation signal. If the checkpoint has no next nodes,
there is no pending work to replay.

The new run creates another path in the same thread. The UI displays that path;
the original checkpoints remain available in history.

> [!WARNING]
>
> Replaying a checkpoint can execute downstream tools and API calls again.
> It does not reverse earlier external effects, such as sent messages or database
> writes. Check those effects before replaying a run.

## The SplitView layout

Time travel works best with a split layout, with the main chat on the left and the
timeline on the right:

```tsx
function TimeTravelLayout() {
  const [threadId, setThreadId] = useState<string | null>(null);
  const [history, setHistory] = useState<ThreadState[]>([]);
  const stream = useStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "time_travel",
    threadId,
    onThreadId: setThreadId,
  });

  const [selectedCheckpoint, setSelectedCheckpoint] =
    useState<ThreadState | null>(null);

  useEffect(() => {
    if (!threadId || stream.isLoading) return;
    stream.client.threads.getHistory(threadId).then(setHistory);
  }, [stream.client, threadId, stream.isLoading]);

  return (
    <div className="flex h-screen">
      {/* Main chat area */}
      <main className="flex-1 overflow-y-auto p-6">
        <div className="mx-auto max-w-2xl space-y-4">
          {stream.messages.map((msg) => (
            <Message key={msg.id} message={msg} />
          ))}
        </div>
        <ChatInput
          onSubmit={(text) =>
            stream.submit({ messages: [{ type: "human", content: text }] })
          }
          isLoading={stream.isLoading}
        />
      </main>

      {/* Timeline sidebar */}
      <aside className="w-96 overflow-y-auto border-l bg-gray-50">
        <TimelineSidebar
          history={history}
          selected={selectedCheckpoint}
          onSelect={setSelectedCheckpoint}
          onResume={(cp) => {
            if (!cp.checkpoint.checkpoint_id) return;
            stream.submit(undefined, {
              forkFrom: cp.checkpoint.checkpoint_id,
            });
          }}
        />
        {selectedCheckpoint && (
          <CheckpointInspector checkpoint={selectedCheckpoint} />
        )}
      </aside>
    </div>
  );
}
```

## Extracting checkpoint metadata

Transform raw checkpoint data into display-friendly entries for your timeline:

```ts
function formatCheckpoints(history: ThreadState[]) {
  return history.map((cp, index) => ({
    index,
    id: cp.checkpoint?.checkpoint_id,
    nextLabel: cp.next?.join(", ") || "Complete",
    messageCount: (cp.values?.messages as unknown[])?.length ?? 0,
    hasInterrupts: cp.tasks?.some((t) => t.interrupts?.length) ?? false,
    nextNodes: cp.next ?? [],
  }));
}
```

This makes it easy to render timeline entries with meaningful labels instead of
raw IDs.

## Use cases

Time travel is invaluable across many scenarios:

* **Debugging agent behavior**: step through the agent's decisions to
  understand why it chose a particular path
* **Trying another path**: continue from an earlier saved state without
  deleting the original checkpoints
* **Exploring alternatives**: fork from a mid-conversation checkpoint to see
  how different inputs change the outcome
* **Auditing**: review the complete history of an agent's actions for
  compliance, quality assurance, or post-incident analysis
* **Teaching**: walk through an agent's execution step by step to explain how
  multi-step reasoning works

> [!NOTE]
>
> Time travel is especially powerful when combined with
> [human-in-the-loop](Human-in-the-Loop.md) patterns. If a human reviewer
> rejects an agent's action at an interrupt, they can resume from the checkpoint
> before the action was taken and provide corrective input.

## Handling interrupts in the timeline

Checkpoints that contain interrupts (human-in-the-loop pauses) deserve special
visual treatment. They represent moments where the agent stopped and waited for
human input:

```tsx
function TimelineEntry({
  checkpoint,
  index,
}: {
  checkpoint: ThreadState;
  index: number;
}) {
  const hasInterrupt = checkpoint.tasks?.some(
    (t) => t.interrupts && t.interrupts.length > 0
  );

  return (
    <div
      className={`rounded-lg border p-3 ${
        hasInterrupt
          ? "border-amber-300 bg-amber-50"
          : "border-gray-200 bg-white"
      }`}
    >
      <div className="flex items-center gap-2">
        <span className="text-xs text-gray-400">#{index + 1}</span>
        {hasInterrupt && (
          <span className="rounded bg-amber-200 px-1.5 py-0.5 text-xs font-medium text-amber-800">
            Interrupt
          </span>
        )}
      </div>
      <p className="mt-1 text-sm font-medium">
        Next: {checkpoint.next?.join(", ") || "Complete"}
      </p>
    </div>
  );
}
```

## Best practices

* **Load history lazily**: for threads with hundreds of checkpoints, paginate
  or load only the most recent N entries to keep the UI responsive.
* **Show meaningful labels**: display scheduled next nodes and message counts
  instead of raw checkpoint IDs. Users need context, not UUIDs.
* **Confirm before resuming**: show a confirmation dialog before starting
  another path, especially when downstream nodes have external effects.
* **Highlight the current checkpoint**: make it visually obvious which
  checkpoint corresponds to the current state of the conversation.
* **Support keyboard navigation**: power users will want to step through
  checkpoints with arrow keys. Add keyboard handlers to the timeline for a
  smooth debugging experience.
* **Diff state between checkpoints**: for advanced users, showing what changed
  between two consecutive checkpoints can reveal exactly how the agent's state
  evolved at each step.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/frontend/time-travel.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
