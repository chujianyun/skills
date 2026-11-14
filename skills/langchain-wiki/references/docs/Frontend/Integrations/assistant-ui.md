# assistant-ui

> Headless React AI chat framework with a full runtime layer, bridged to useStream

[assistant-ui](https://www.assistant-ui.com/) is a headless React UI framework for AI chat. It provides a full runtime layer—thread management, message branching, attachment handling—that connects to [`useStream`](https://reference.langchain.com/javascript/langchain-react/index/useStream) via the `useExternalStoreRuntime` adapter.

> [!TIP]
>
> Clone and run the [full assistant-ui example](https://github.com/langchain-ai/langgraphjs/tree/main/examples/assistant-ui-claude) to see a Claude-style chat interface wired to a LangChain agent with `useExternalStoreRuntime`.

## How it works

1. **Stream with [`useStream`](https://reference.langchain.com/javascript/langchain-react/index/useStream)**: connect to your agent and get reactive messages, loading state, and submit/cancel callbacks
2. **Adapt with `useExternalStoreRuntime`**: bridge `stream.messages` into assistant-ui's runtime format by converting `BaseMessage[]` to `ThreadMessageLike[]`
3. **Provide the runtime**: wrap your UI in `AssistantRuntimeProvider` and render any assistant-ui thread component

## Installation

```bash
bun add @assistant-ui/react @assistant-ui/react-markdown
```

## Wiring `useStream`

The `useExternalStoreRuntime` adapter bridges `stream.messages` into the assistant-ui runtime. Pass it to `AssistantRuntimeProvider` and render any thread component:

```tsx
import { useCallback, useMemo } from "react";
import {
  AssistantRuntimeProvider,
  useExternalStoreRuntime,
  type AppendMessage,
  type ThreadMessageLike,
} from "@assistant-ui/react";
import { useStream } from "@langchain/react";
import { Thread } from "@assistant-ui/react";

export function Chat() {
  const stream = useStream({
    apiUrl: "http://localhost:2024",
    assistantId: "claude",
  });

  const onNew = useCallback(
    async (message: AppendMessage) => {
      const text = message.content
        .filter((c) => c.type === "text")
        .map((c) => c.text)
        .join("");
      await stream.submit({ messages: [{ type: "human", content: text }] });
    },
    [stream],
  );

  // Convert LangChain messages to assistant-ui's ThreadMessageLike format
  const messages = useMemo(
    () => toThreadMessages(stream.messages),
    [stream.messages],
  );

  const runtime = useExternalStoreRuntime<ThreadMessageLike>({
    messages,
    onNew,
    onCancel: () => stream.stop(),
    convertMessage: (m) => m,
  });

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <Thread />
    </AssistantRuntimeProvider>
  );
}
```

### Converting messages

`toThreadMessages` maps LangChain `BaseMessage[]` to the `ThreadMessageLike[]` format assistant-ui expects. Handle each message type — human, AI, and tool — and convert content blocks, tool calls, and reasoning tokens:

```tsx expandable
import { AIMessage, HumanMessage, ToolMessage, type BaseMessage } from "langchain";
import type { ThreadMessageLike } from "@assistant-ui/react";

export function toThreadMessages(messages: BaseMessage[]): ThreadMessageLike[] {
  const result: ThreadMessageLike[] = [];

  for (const msg of messages) {
    if (HumanMessage.isInstance(msg)) {
      result.push({
        role: "user",
        content: [{ type: "text", text: msg.text }],
      });
    } else if (AIMessage.isInstance(msg)) {
      const parts: ThreadMessageLike["content"] = [];

      // Reasoning tokens
      const reasoning = msg.contentBlocks.find((block) => block.type === "reasoning")?.reasoning;
      if (reasoning) parts.push({ type: "reasoning", text: reasoning });

      // Tool calls
      for (const tc of msg.tool_calls ?? []) {
        parts.push({
          type: "tool-call",
          toolCallId: tc.id ?? "",
          toolName: tc.name,
          args: tc.args,
        });
      }

      // Text response
      const text = msg.text;
      if (text) parts.push({ type: "text", text });

      result.push({ role: "assistant", content: parts });
    } else if (ToolMessage.isInstance(msg)) {
      // Attach tool results to the preceding assistant message
      const last = result[result.length - 1];
      if (last?.role === "assistant") {
        for (const part of last.content) {
          if (
            part.type === "tool-call" &&
            part.toolCallId === msg.tool_call_id
          ) {
            (part as { result?: string }).result = msg.text;
          }
        }
      }
    }
  }

  return result;
}
```

## Customizing the thread UI

`<Thread />` ships a complete default thread UI including message list, composer, and scroll management. Customize individual parts by overriding component slots:

```tsx
import { Thread, ThreadMessages, Composer } from "@assistant-ui/react";

function CustomThread() {
  return (
    <Thread.Root>
      <ThreadMessages
        components={{
          UserMessage: MyUserMessage,
          AssistantMessage: MyAssistantMessage,
          ToolFallback: MyToolCard,
        }}
      />
      <Composer />
    </Thread.Root>
  );
}
```

## Best practices

* **Memoise message conversion:** wrap `toThreadMessages(stream.messages)` in `useMemo` to avoid re-running the conversion on every render
* **Handle attachments:** use `CompositeAttachmentAdapter` with `SimpleImageAttachmentAdapter` for image uploads; extend with custom adapters for files
* **Use branching:** assistant-ui has built-in message branching support via `MessageBranch`; pair edits with `useMessageMetadata` and `forkFrom` when you need LangGraph checkpoint forks
* **Thread persistence:** persist `threadId` with `onThreadId` and pass it back into [`useStream`](https://reference.langchain.com/javascript/langchain-react/index/useStream) on page load so assistant-ui reconnects to the same thread

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/frontend/integrations/assistant-ui.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
