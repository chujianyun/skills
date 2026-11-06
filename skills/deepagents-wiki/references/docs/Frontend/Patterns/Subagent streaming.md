# Subagent streaming

> Display specialist subagents with streaming content, progress tracking, and collapsible cards

When a coordinator agent spawns specialist subagents (a researcher, an
analyst, a writer), you need to render the orchestrator's messages separately
from each subagent's streaming output. The v1 SDK keeps coordinator messages on
the root stream and exposes subagents as discovery snapshots. Pass a snapshot to
selector hooks or composables such as `useMessages(stream, subagent)` to render
the specialist's scoped stream.

This is where the LangChain frontend SDKs go beyond a flat chat transcript:
subagents are first-class stream entities with their own status, messages,
tool-call metadata, and results. Your UI can show delegation, progress, errors,
and final synthesis without asking users to read interleaved tokens from every
worker.

## Why selector-based subagent streams

The root stream stays focused on the coordinator conversation:

* `stream.messages` contains only the coordinator's messages
* `stream.subagents` contains discovery snapshots with identity, namespace, and status
* Each subagent's messages, tool calls, and values are read with selector helpers
* The UI stays clean: the coordinator's reasoning is separate from the
  specialists' work

This separation lets you render the orchestrator's messages in one place and
mount subagent cards only when the user needs to see specialist work.

For large tasks, this also keeps the UI scalable. Users can skim the
coordinator's high-level plan, expand only the specialist work they care about,
and still retain the full subagent trace for debugging, audit, or replay.

## Setting up `useStream`

No extra stream options are required. Point the stream at your deep agent,
render coordinator messages from `stream.messages`, and use `stream.subagents`
to mount cards for active specialists. In chat layouts, index subagents by the
tool-call ID that spawned them so each card appears under the coordinator turn
Point the stream at your deep agent, render coordinator messages from `stream.messages`, and use `stream.subagents` to mount cards for active specialists. In chat layouts, index subagents by the
tool-call ID that spawned them so each card appears under the coordinator turn that delegated the work.

> [!NOTE]
>
> The code examples use `useStream<typeof myAgent>` for type-safe stream state. See Type inference for [Python](https://docs.langchain.com/oss/python/langchain/frontend/overview.md#type-inference) or [JavaScript](https://docs.langchain.com/oss/javascript/langchain/frontend/overview.md#type-inference) backends.

```tsx React theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import { useStream } from "@langchain/react";
import { AIMessage, HumanMessage } from "langchain";

const AGENT_URL = "http://localhost:2024";

export function DeepAgentChat() {
  const stream = useStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "deep_agent_subagent_cards",
  });
  const subagents = [...stream.subagents.values()];
  const subagentsByCallId = new Map(subagents.map((s) => [s.id, s]));

  return (
    <div>
      {stream.messages.map((msg) => {
        const turnSubagents = AIMessage.isInstance(msg)
          ? (msg.tool_calls ?? [])
              .map((tc) => subagentsByCallId.get(tc.id ?? ""))
              .filter((s): s is NonNullable<typeof s> => !!s)
          : [];

        return (
          <div key={msg.id}>
            {HumanMessage.isInstance(msg) && <HumanBubble>{msg.text}</HumanBubble>}
            {AIMessage.isInstance(msg) && msg.text.trim() && (
              <AIBubble>{msg.text}</AIBubble>
            )}
            {turnSubagents.map((subagent) => (
              <SubagentCard key={subagent.id} stream={stream} subagent={subagent} />
            ))}
          </div>
        );
      })}
    </div>
  );
}
```

```vue Vue theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
<script setup lang="ts">
import { computed } from "vue";
import { useStream } from "@langchain/vue";
import { AIMessage, HumanMessage } from "langchain";

const AGENT_URL = "http://localhost:2024";

const stream = useStream<typeof myAgent>({
  apiUrl: AGENT_URL,
  assistantId: "deep_agent_subagent_cards",
});

const subagentsByCallId = computed(
  () => new Map([...stream.subagents.value.values()].map((s) => [s.id, s]))
);

function subagentsForMessage(msg: unknown) {
  if (!AIMessage.isInstance(msg)) return [];
  return (msg.tool_calls ?? [])
    .map((tc) => subagentsByCallId.value.get(tc.id ?? ""))
    .filter(Boolean);
}
</script>

<template>
  <div>
    <div
      v-for="msg in stream.messages.value"
      :key="msg.id"
    >
      <HumanBubble v-if="HumanMessage.isInstance(msg)">
        {{ msg.text }}
      </HumanBubble>
      <AIBubble v-else-if="AIMessage.isInstance(msg) && msg.text.trim()">
        {{ msg.text }}
      </AIBubble>
      <SubagentCard
        v-for="subagent in subagentsForMessage(msg)"
        :key="subagent.id"
        :stream="stream"
        :subagent="subagent"
      />
    </div>
  </div>
</template>
```

```svelte Svelte theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
<script lang="ts">
  import { useStream } from "@langchain/svelte";

  const AGENT_URL = "http://localhost:2024";

  const stream = useStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "deep_agent_subagent_cards",
  });
</script>

<div>
  {#each stream.messages as msg (msg.id)}
    <Message {msg} />
  {/each}
  {#each [...stream.subagents.values()] as subagent (subagent.id)}
    <SubagentCard {stream} {subagent} />
  {/each}
</div>
```

```ts Angular theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import { Component, computed } from "@angular/core";
import { injectStream } from "@langchain/angular";

const AGENT_URL = "http://localhost:2024";

@Component({
  selector: "app-deep-agent-chat",
  template: `
    @for (msg of stream.messages(); track msg.id) {
      <app-message [message]="msg" />
    }
    @for (subagent of subagents(); track subagent.id) {
      <app-subagent-card [stream]="stream" [subagent]="subagent" />
    }
  `,
})
export class DeepAgentChatComponent {
  stream = injectStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "deep_agent_subagent_cards",
  });

  subagents = computed(() => [...this.stream.subagents().values()]);
}
```

## Submitting messages

Submit messages through the root stream. Deep agent workflows often involve
multiple layers of nested subgraphs, so set an appropriate recursion limit if
your agent can delegate deeply:

```ts theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
stream.submit(
  { messages: [{ type: "human", content: text }] },
  { config: { recursion_limit: 100 } }
);
```

> [!NOTE]
>
> Deep Agents sets a default recursion limit of 10,000, which is sufficient for
> most multi-expert setups. You can override this via `config.recursion_limit` if
> needed.

## The SubagentDiscoverySnapshot

Each [SubagentDiscoverySnapshot](https://reference.langchain.com/javascript/langchain-react/SubagentDiscoverySnapshot) is a lightweight discovery record for a
subagent running inside the thread. It tells your UI that a subagent exists,
where it sits in the subagent tree, and what lifecycle state it is in.

The snapshot does **not** include the subagent's streamed messages or tool calls.
Instead, pass the snapshot to selector hooks such as
`useMessages(stream, subagent)` or `useToolCalls(stream, subagent)`. These hooks
use the snapshot namespace to subscribe to the subagent's stream primitives only
when the corresponding card or panel is mounted.

## Building the SubagentCard

Each subagent card shows the specialist's name, status, streaming content, and
tool calls. Use selector hooks to subscribe to the subagent namespace:

```tsx theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import { useState } from "react";
import { AIMessage } from "langchain";
import {
  useMessages,
  useToolCalls,
  type AnyStream,
  type SubagentDiscoverySnapshot,
} from "@langchain/react";

function SubagentCard({
  stream,
  subagent,
}: {
  stream: AnyStream;
  subagent: SubagentDiscoverySnapshot;
}) {
  const [expanded, setExpanded] = useState(true);
  const messages = useMessages(stream, subagent);
  const toolCalls = useToolCalls(stream, subagent);

  const lastAIMessage = messages
    .filter(AIMessage.isInstance)
    .at(-1);

  const displayContent =
    lastAIMessage?.text ?? subagent.output ?? "";

  return (
    <div className="rounded-lg border bg-white shadow-sm">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex w-full items-center justify-between p-4"
      >
        <div className="flex items-center gap-3">
          <StatusIcon status={subagent.status} />
          <div>
            <h4 className="font-semibold capitalize">{subagent.name}</h4>
            <p className="text-xs text-gray-500">
              {toolCalls.length} tool call{toolCalls.length === 1 ? "" : "s"}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <StatusBadge status={subagent.status} />
        </div>
      </button>

      {expanded && displayContent && (
        <div className="border-t px-4 py-3">
          <div className="prose prose-sm max-w-none line-clamp-6">
            {displayContent}
            {subagent.status === "running" && (
              <span className="inline-block h-4 w-1 animate-pulse bg-blue-500" />
            )}
          </div>
        </div>
      )}
    </div>
  );
}
```

## Progress tracking

Show a progress bar and counter so users know how many subagents have finished:

```tsx theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
function SubagentProgress({
  subagents,
}: {
  subagents: SubagentDiscoverySnapshot[];
}) {
  const completed = subagents.filter((s) => s.status === "complete").length;
  const total = subagents.length;
  const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;

  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-xs text-gray-500">
        <span>Subagent progress</span>
        <span>
          {completed}/{total} complete
        </span>
      </div>
      <div className="h-2 overflow-hidden rounded-full bg-gray-200">
        <div
          className="h-full rounded-full bg-blue-500 transition-all duration-300"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
```

## Rendering messages with subagent cards

The key layout pattern is to render coordinator messages from the root stream
and attach subagent cards to the AI message whose tool call spawned them:

```tsx theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
function DeepAgentLayout({ stream }: { stream: AnyStream }) {
  const subagents = [...stream.subagents.values()];
  const subagentsByCallId = new Map(subagents.map((s) => [s.id, s]));

  return (
    <div className="space-y-3">
      {stream.messages.map((message) => {
        const turnSubagents = AIMessage.isInstance(message)
          ? (message.tool_calls ?? [])
              .map((tc) => subagentsByCallId.get(tc.id ?? ""))
              .filter((s): s is SubagentDiscoverySnapshot => !!s)
          : [];

        return (
          <div key={message.id}>
            <Message message={message} />
            {turnSubagents.length > 0 && (
              <div className="ml-4 space-y-3 border-l-2 border-blue-200 pl-4">
                <SubagentProgress subagents={subagents} />
                {turnSubagents.map((subagent) => (
                  <SubagentCard key={subagent.id} stream={stream} subagent={subagent} />
                ))}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
```

You can combine inline cards with a global subagent view: index subagents by
the coordinator tool call that spawned them for transcript cards, and use
`stream.subagents` for a persistent sidebar that summarizes all active workers.
That gives users both local context and a bird's-eye view of the whole run.

## Best practices

* **Mount selectors only where needed**. Scoped messages and tool calls stream
  when a card calls `useMessages(stream, subagent)` or `useToolCalls(stream, subagent)`.
* **Show specialist names**. `subagent.name` tells users which worker is active.
* **Use collapsible cards**. In workflows with 5+ subagents, auto-collapse
  completed cards so users can focus on active work.
* **Override recursion only when needed**. Deep Agents sets a high default
  recursion limit; pass `config.recursion_limit` only for unusually deep custom
  workflows.
* **Handle errors per subagent**. One subagent failing shouldn't crash the
  entire UI. Show the error in that subagent's card while others continue
  running.

## Related LangChain guides

These LangChain frontend patterns work with subagent cards the same way they
work with single-agent streams. Deep Agents are built on the same `useStream`
API, so these guides apply directly:

> [card] [Tool calling](https://docs.langchain.com/oss/python/langchain/frontend/tool-calling.md)
>
> Render each subagent's tool calls as rich, type-safe UI cards with pending, completed, and failed states.

> [card] [Markdown messages](https://docs.langchain.com/oss/python/langchain/frontend/markdown-messages.md)
>
> Display coordinator and subagent messages as formatted markdown with proper streaming support.

> [card] [Human-in-the-Loop](https://docs.langchain.com/oss/python/langchain/frontend/human-in-the-loop.md)
>
> Pause a delegated subagent for user approval or input using the same interrupt API.

> [card] [Reasoning tokens](https://docs.langchain.com/oss/python/langchain/frontend/reasoning-tokens.md)
>
> Surface model thinking inside subagent cards using collapsible reasoning blocks.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/deepagents/frontend/subagent-streaming.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
