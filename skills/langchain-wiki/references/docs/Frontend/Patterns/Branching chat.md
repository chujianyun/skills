# Branching chat

> Edit messages and regenerate responses by forking from checkpoints

Conversations with AI agents are rarely linear. You may want to rephrase a
question, regenerate a response you didn't like, or explore a different
conversational path without losing the checkpoint history. Branching chat uses
LangGraph checkpoints as fork points: every edit or regeneration submits a new
run from the selected message's parent checkpoint.

> [!NOTE]
>
> This feature requires the [LangGraph Agent Server](https://docs.langchain.com/oss/python/langgraph/local-server.md). Run your agent locally with `langgraph dev` or [deploy it to LangSmith](https://docs.langchain.com/langsmith/deployment.md) to use this pattern.

## What is branching chat?

Branching chat treats a conversation as a checkpointed timeline rather than a
flat list. Each message has metadata that points to the checkpoint before that
message was created. Editing a message or regenerating a response submits a new
run from that checkpoint.

Key capabilities:

* **Edit any user message:** rewrite a previous prompt and re-run the agent from that point
* **Regenerate any AI response:** ask the agent to produce a different answer for the same input
* **Inspect history:** use the LangGraph client to load checkpoints when you need a branch timeline

## Set up stream metadata

Use the root stream for messages, then read per-message checkpoint metadata in
the component that renders each message. The metadata includes the parent
checkpoint ID to fork from.

> [!NOTE]
>
> The code examples use `useStream<typeof myAgent>` for type-safe stream state. See Type inference for [Python](../Overview.md#type-inference) or [JavaScript](https://docs.langchain.com/oss/javascript/langchain/frontend/overview.md#type-inference) backends.

```tsx React
import { useStream } from "@langchain/react";

const AGENT_URL = "http://localhost:2024";

export function Chat() {
  const stream = useStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "simple_agent",
  });

  return (
    <div>
      {stream.messages.map((msg) => (
        <MessageWithForkControls key={msg.id} stream={stream} message={msg} />
      ))}
    </div>
  );
}
```

```vue Vue
<script setup lang="ts">
import { useStream } from "@langchain/vue";

const AGENT_URL = "http://localhost:2024";

const stream = useStream<typeof myAgent>({
  apiUrl: AGENT_URL,
  assistantId: "simple_agent",
});
</script>

<template>
  <div>
    <MessageWithForkControls
      v-for="msg in stream.messages.value"
      :key="msg.id"
      :stream="stream"
      :message="msg"
    />
  </div>
</template>
```

```svelte Svelte
<script lang="ts">
  import { useStream } from "@langchain/svelte";

  const AGENT_URL = "http://localhost:2024";

  const stream = useStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "simple_agent",
  });
</script>

<div>
  {#each stream.messages as msg (msg.id)}
    <Message
      message={msg}
      {stream}
    />
  {/each}
</div>
```

```ts Angular
import { Component } from "@angular/core";
import { injectStream } from "@langchain/angular";

const AGENT_URL = "http://localhost:2024";

@Component({
  selector: "app-chat",
  template: `
    @for (msg of stream.messages(); track msg.id) {
      <app-message
        [message]="msg"
        [stream]="stream"
      />
    }
  `,
})
export class ChatComponent {
  stream = injectStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "simple_agent",
  });
}
```

## Understand message metadata

The `useMessageMetadata(stream, messageId)` helper returns [MessageMetadata](https://reference.langchain.com/javascript/langchain-react/MessageMetadata)
for one message. Use it in the component that renders each message so the
metadata stays scoped to that message ID:

```tsx
import type { BaseMessage } from "langchain";
import { useState } from "react";
import { useMessageMetadata, useStream } from "@langchain/react";

function Chat() {
  const stream = useStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "simple_agent",
  });

  return stream.messages.map((message) => (
    <MessageWithForkControls
      key={message.id}
      stream={stream}
      message={message}
    />
  ));
}

function MessageWithForkControls({
  stream,
  message,
}: {
  stream: ReturnType<typeof useStream>;
  message: BaseMessage;
}) {
  const metadata = useMessageMetadata(stream, message.id);
  const checkpointId = metadata?.parentCheckpointId;
  const [editedText, setEditedText] = useState(message.text);

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        if (!checkpointId) return;

        stream.submit(
          { messages: [{ type: "human", content: editedText }] },
          { forkFrom: checkpointId }
        );
      }}
    >
      <textarea
        value={editedText}
        onChange={(event) => setEditedText(event.target.value)}
      />
      <button disabled={!checkpointId || editedText === message.text}>
        Submit edited branch
      </button>
    </form>
  );
}
```

`parentCheckpointId` is the checkpoint just before the message. Use it as the
fork point for edits and regenerations.

## Edit a message

To edit a user message and fork the conversation:

1. Get `parentCheckpointId` from the message's metadata
2. Submit the edited message with `forkFrom: checkpointId`
3. The agent re-runs from that point

```ts
function handleEdit(
  stream: ReturnType<typeof useStream>,
  originalMsg: HumanMessage,
  metadata: MessageMetadata | undefined,
  newText: string
) {
  if (!metadata?.parentCheckpointId) return;

  stream.submit(
    {
      messages: [{ type: "human", content: newText }],
    },
    { forkFrom: metadata.parentCheckpointId }
  );
}
```

After the edit:

* The agent re-runs from the fork point with the updated message
* The original path remains available in the thread history

## Regenerate a response

To regenerate an AI response without changing the input:

1. Get `parentCheckpointId` from the AI message's metadata
2. Submit with `undefined` input and `forkFrom: checkpointId`
3. The agent produces a fresh response from that point

```ts
function handleRegenerate(
  stream: ReturnType<typeof useStream>,
  metadata: MessageMetadata | undefined
) {
  if (!metadata?.parentCheckpointId) return;

  stream.submit(undefined, {
    forkFrom: metadata.parentCheckpointId,
  });
}
```

The SDK converts `undefined` input to `null` to continue from the checkpoint
without supplying new input. An empty object (`{}`) supplies new input instead.
Each regeneration creates a new path in the same thread.

> [!WARNING]
>
> Regeneration can re-execute downstream tools and API calls. It does not reverse
> external effects from the original run. Check those effects before regenerating.

> [!TIP]
>
> Regeneration is useful for non-deterministic agents. Since LLM outputs vary
> with temperature, regenerating the same prompt often produces meaningfully
> different responses.

## How branching works under the hood

LangGraph persists state at super-step boundaries as **checkpoints**. Nodes
that run in parallel in one super-step share a checkpoint boundary. When you submit
with `forkFrom`, the backend starts a new execution path from that point instead
of appending to the current conversation. The result is a tree structure:

```
User: "What is React?"
  └─ AI: "React is a JavaScript library..." (branch A)
  └─ AI: "React is a UI framework..." (branch B, regenerated)

User: "Tell me about hooks" (branch A)
  └─ AI: "Hooks are functions..."

User: "Tell me about JSX" (edited from branch A)
  └─ AI: "JSX is a syntax extension..."
```

Each path is persisted in the checkpoint store. Use
`stream.client.threads.getHistory(threadId)` when you want to build a separate
timeline view across checkpoints. History is newest first and defaults to 10
entries. Use each state's `parent_checkpoint` to reconstruct ancestry; list
position alone does not identify a branch.

## Best practices

* **Read metadata near the message**: call `useMessageMetadata` in the component
  that renders the message controls.
* **Show fork controls on hover**: edit and regenerate buttons should appear on
  hover to keep the UI clean.
* **Refresh history on demand**: call `client.threads.getHistory()` only when
  rendering a timeline or after a fork settles.
* **Disable controls while streaming**: don't allow edits or regeneration
  while the agent is actively streaming a response. Check `stream.isLoading`
  before enabling these actions.
* **Preserve edit text on cancel**: if the user starts editing, then cancels,
  reset the textarea to the original message content.
* **Test with deep checkpoint trees**: users who edit and regenerate frequently
  can create many paths. Ensure timeline rendering remains performant.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/frontend/branching-chat.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
