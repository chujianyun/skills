# Join & rejoin streams

> Disconnect from and reconnect to running agent streams

Join and rejoin lets you disconnect from a running agent stream without stopping the agent, then reconnect to it later. The agent continues executing server-side while the client is away, and you pick up the stream exactly where you left off.

> [!NOTE]
>
> This feature requires the [LangGraph Agent Server](https://docs.langchain.com/oss/python/langgraph/local-server.md). Run your agent locally with `langgraph dev` or [deploy it to LangSmith](https://docs.langchain.com/langsmith/deployment.md) to use this pattern.

## Why join & rejoin?

Traditional streaming APIs tightly couple the client and server: if the client disconnects, the stream is lost. Join and rejoin breaks this coupling, enabling several important patterns:

* **Network interruptions**: mobile users moving between cell towers or Wi-Fi networks can seamlessly resume
* **Page navigation**: users navigating away from a chat page and returning later without losing progress
* **Mobile backgrounding**: apps suspended by the OS can rejoin the stream when foregrounded
* **Long-running tasks**: agents performing multi-minute operations (research, code generation, data analysis) where users don't need to keep the page open
* **Multi-device handoff**: start a conversation on your phone, rejoin on your desktop

## Core concepts

The join/rejoin pattern involves three key mechanisms:

| Method / Option | Purpose |
| - | - |
| `threadId` | Bind the stream to the LangGraph thread you want to observe |
| `onThreadId` | Persist newly-created thread IDs so a remount can reconnect |
| `stream.disconnect()` | Leave the stream client-side while the agent keeps running server-side |
| Remount with the same `threadId` | Reattach to in-flight work for that thread |

> [!NOTE]
>
> **Join/rejoin uses `stream.disconnect()`, not `stream.stop()`.** By default, `stream.stop()` **cancels the active run**: it disconnects the client *and* cancels the run on the server. For join/rejoin, call `stream.disconnect()` (alias for `stop({ cancel: false })`) so the agent continues processing while you are away.
>
> To cancel execution explicitly from app code, use `stream.stop()` or [`client.runs.cancel`](https://reference.langchain.com/python/langgraph-sdk/_async/runs/RunsClient/cancel).

## Setting up `useStream`

The key setup step is persisting `threadId`. When the component remounts with
the same thread ID, the stream attaches to the thread's current state and any
in-flight run.

> [!NOTE]
>
> The code examples use `useStream<typeof myAgent>` for type-safe stream state. See Type inference for [Python](../Overview.md#type-inference) or [JavaScript](https://docs.langchain.com/oss/javascript/langchain/frontend/overview.md#type-inference) backends.

```tsx React
import { useStream } from "@langchain/react";
import { useCallback, useState } from "react";

function Chat() {
  const [connected, setConnected] = useState(true);
  const [mountKey, setMountKey] = useState(0);
  const [threadId, setThreadId] = useState<string | null>(
    () => sessionStorage.getItem("activeThreadId"),
  );

  const stream = useStream<typeof myAgent>({
    apiUrl: "http://localhost:2024",
    assistantId: "join_rejoin",
    threadId,
    onThreadId(id) {
      setThreadId(id);
      if (id) sessionStorage.setItem("activeThreadId", id);
    },
  });

  const disconnect = useCallback(() => {
    void stream.disconnect();
    setConnected(false);
  }, [stream]);

  const rejoin = useCallback(() => {
    setMountKey((key) => key + 1);
    setConnected(true);
  }, []);

  return (
    <div key={mountKey}>
      <ConnectionStatus connected={connected} />
      <MessageList messages={stream.messages} />
      <ChatControls
        stream={stream}
        threadId={threadId}
        connected={connected}
        onDisconnect={disconnect}
        onRejoin={rejoin}
      />
    </div>
  );
}
```

```vue Vue
<script setup lang="ts">
import { useStream } from "@langchain/vue";
import { ref } from "vue";

const connected = ref(true);
const mountKey = ref(0);
const threadId = ref<string | null>(sessionStorage.getItem("activeThreadId"));

const stream = useStream<typeof myAgent>({
  apiUrl: "http://localhost:2024",
  assistantId: "join_rejoin",
  threadId,
  onThreadId(id) {
    threadId.value = id;
    if (id) sessionStorage.setItem("activeThreadId", id);
  },
});

function disconnect() {
  void stream.disconnect();
  connected.value = false;
}

function rejoin() {
  mountKey.value += 1;
  connected.value = true;
}
</script>

<template>
  <div :key="mountKey">
    <ConnectionStatus :connected="connected" />
    <MessageList :messages="stream.messages" />
    <ChatControls
      :stream="stream"
      :threadId="threadId"
      :connected="connected"
      @disconnect="disconnect"
      @rejoin="rejoin"
    />
  </div>
</template>
```

```svelte Svelte
<script lang="ts">
  import { useStream } from "@langchain/svelte";

  let connected = $state(true);
  let mountKey = $state(0);
  let threadId = $state<string | null>(sessionStorage.getItem("activeThreadId"));

  const stream = useStream<typeof myAgent>({
    apiUrl: "http://localhost:2024",
    assistantId: "join_rejoin",
    threadId: () => threadId,
    onThreadId(id) {
      threadId = id;
      if (id) sessionStorage.setItem("activeThreadId", id);
    },
  });

  function disconnect() {
    void stream.disconnect();
    connected = false;
  }

  function rejoin() {
    mountKey += 1;
    connected = true;
  }
</script>

<div key={mountKey}>
  <ConnectionStatus {connected} />
  <MessageList messages={stream.messages} />
  <ChatControls
    {threadId}
    {connected}
    onDisconnect={disconnect}
    onRejoin={rejoin}
  />
</div>
```

```ts Angular
import { Component, signal } from "@angular/core";
import { injectStream } from "@langchain/angular";

@Component({
  selector: "app-chat",
  template: `
    <connection-status [connected]="connected()" />
    <message-list [messages]="stream.messages()" />
    <chat-controls
      [stream]="stream"
      [threadId]="threadId()"
      [connected]="connected()"
      (disconnect)="disconnect()"
      (rejoin)="rejoin()"
    />
  `,
})
export class ChatComponent {
  threadId = signal<string | null>(sessionStorage.getItem("activeThreadId"));
  connected = signal(true);
  mountKey = signal(0);

  stream = injectStream<typeof myAgent>({
    apiUrl: "http://localhost:2024",
    assistantId: "join_rejoin",
    threadId: this.threadId,
    onThreadId: (id) => {
      this.threadId.set(id);
      if (id) sessionStorage.setItem("activeThreadId", id);
    },
  });

  disconnect() {
    void this.stream.disconnect();
    this.connected.set(false);
  }

  rejoin() {
    this.mountKey.update((key) => key + 1);
    this.connected.set(true);
  }
}
```

## Submitting messages

Submit messages normally. The thread ID binding is what allows a later remount
to reconnect to the same conversation:

```ts
stream.submit({ messages: [{ type: "human", content: text }] });
```

## Disconnecting from a stream

Call `stream.disconnect()` to leave the stream without cancelling the run. The agent continues processing server-side.

```ts
await stream.disconnect();
// equivalent to: await stream.stop({ cancel: false })
```

Do **not** use `stream.stop()` here — by default it cancels the run on the server.

After calling `disconnect()`:

* `stream.isLoading` becomes `false`
* Your own `connected` flag should also become `false`
* The message list retains all messages received up to the disconnect point
* The agent continues running on the server
* No new messages are received until you rejoin

## Rejoining a stream

Remount the stream consumer with the saved thread ID to reconnect. In React, the
demo bumps a `mountKey`; in other frameworks, use the equivalent remount or
conditional-render pattern:

```ts
setMountKey((key) => key + 1);
setConnected(true);
```

After rejoining:

* `connected` becomes `true`
* Any messages generated while disconnected are delivered
* New streaming messages resume in real-time
* If the agent is still running, `stream.isLoading` becomes `true`; if it has
  already finished, you receive the final state immediately

## Best practices

* **Use `disconnect()` for join/rejoin, `stop()` to cancel**: navigating away or backgrounding the app should call `stream.disconnect()`. A user-facing "Stop" or "Cancel" button should call `stream.stop()` (or [`client.runs.cancel`](https://reference.langchain.com/python/langgraph-sdk/_async/runs/RunsClient/cancel)).
* **Always save the thread ID**: without it, rejoining is impossible. Use both component state and persistent storage for resilience.
* **Show clear connection state**: users should always know whether they are receiving live updates or viewing a snapshot.
* **Auto-rejoin on visibility change**: use the Page Visibility API to automatically rejoin when the user returns to the tab.
* **Set reasonable timeouts**: if a rejoin attempt takes too long, fall back to fetching the thread history instead.
* **Clean up stale threads**: remove persisted thread IDs when the user starts over or the backend reports that the thread is unavailable.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/frontend/join-rejoin.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
