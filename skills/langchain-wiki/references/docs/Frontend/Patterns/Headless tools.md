# Headless tools

> Run browser and device APIs on the client with headless tool implementations

Headless tools let your agent call tools whose real execution must happen in the
user's app instead of on the server. The agent still sees a normal tool schema,
but the implementation lives in the frontend, where it can access browser APIs
like IndexedDB, geolocation, clipboard, canvas, or file pickers.

This pattern is especially useful when data should stay local to the device.
The playground example on this page uses a small browser-memory toolkit backed
by IndexedDB plus a geolocation tool that runs entirely on the client.

## How headless tools work

At a high level, headless tools split the tool schema from the browser-only implementation.

1. Register a tool on the agent that immediately calls `interrupt()` to defer execution to the frontend.
2. Mirror the same tool names and argument fields in frontend definitions.
3. Implement the matching tools in the frontend with `.implement(...)` and pass
   them to `useStream({ tools: [...] })`.
4. When the agent invokes a matching tool, the client handles the action and
   resumes the interrupted run with the tool result.

## Register the tool on the agent

The playground defines a small set of client-side tools that follow the same
pattern: the agent exposes a tool schema, and the frontend handles the actual
execution.

Define normal tools on the server that immediately call `interrupt()`, then
mirror the same tool names and argument fields in a
frontend `tools.ts` file.

```python agent.py
from typing import Any

from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt
from pydantic import BaseModel


class MemoryPutInput(BaseModel):
    key: str
    value: Any


class MemoryGetInput(BaseModel):
    key: str


class GeolocationGetInput(BaseModel):
    save: bool = True


def _interrupt_for_client(
    tool_name: str,
    args: dict[str, Any],
    runtime: ToolRuntime,
) -> Any:
    return interrupt({
        "type": "tool",
        "tool_call": {
            "id": runtime.tool_call_id,
            "name": tool_name,
            "args": args,
        },
    })


@tool(
    "memory_put",
    description="Store a memory in the user's browser.",
    args_schema=MemoryPutInput,
)
def memory_put(key: str, value: Any, runtime: ToolRuntime) -> Any:
    return _interrupt_for_client(
        "memory_put",
        {"key": key, "value": value},
        runtime,
    )


@tool(
    "memory_get",
    description="Look up a memory stored in the user's browser.",
    args_schema=MemoryGetInput,
)
def memory_get(key: str, runtime: ToolRuntime) -> Any:
    return _interrupt_for_client("memory_get", {"key": key}, runtime)


@tool(
    "geolocation_get",
    description="Get the user's current location from the browser.",
    args_schema=GeolocationGetInput,
)
def geolocation_get(runtime: ToolRuntime, save: bool = True) -> Any:
    return _interrupt_for_client(
        "geolocation_get",
        {"save": save},
        runtime,
    )

agent = create_agent(
    model="openai:gpt-6.1-sol",
    tools=[memory_put, memory_get, geolocation_get],
    checkpointer=MemorySaver(),
)
```

Each tool interrupts with a structured payload the frontend can handle, then
returns the value provided when the run resumes. Mirror the same tool names and
schemas on the client so the frontend can attach implementations.

```ts tools.ts
import * as z from "zod";
import { tool } from "langchain";

// Mirror the Python tool names and schemas on the client.
export const memoryPut = tool({
  name: "memory_put",
  description: "Store a memory in the user's browser.",
  schema: z.object({
    key: z.string(),
    value: z.unknown(),
  }),
});

export const memoryGet = tool({
  name: "memory_get",
  description: "Look up a memory stored in the user's browser.",
  schema: z.object({
    key: z.string(),
  }),
});

export const geolocationGet = tool({
  name: "geolocation_get",
  description: "Get the user's current location from the browser.",
  schema: z.object({
    save: z.boolean().optional(),
  }),
});
```

## Implement the browser behavior

Put the client-only behavior in a separate module and attach it with
`.implement(...)`. The real playground includes a fuller IndexedDB store with
search, listing, expiration, and delete operations. The following example shows
the same shape at a higher level:

```ts impl.ts
import {
  geolocationGet as geolocationGetDefinition,
  memoryGet as memoryGetDefinition,
  memoryPut as memoryPutDefinition,
} from "./tools";

async function saveMemory(key: string, value: unknown) {
  localStorage.setItem(`agent-memory:${key}`, JSON.stringify(value));
}

async function getMemory(key: string) {
  const value = localStorage.getItem(`agent-memory:${key}`);
  return value ? JSON.parse(value) : null;
}

export const memoryPut = memoryPutDefinition.implement(async ({ key, value }) => {
  await saveMemory(key, value);
  return { success: true, key };
});

export const memoryGet = memoryGetDefinition.implement(async ({ key }) => {
  const value = await getMemory(key);
  return value === null ? { found: false, key } : { found: true, key, value };
});

export const geolocationGet = geolocationGetDefinition.implement(
  async ({ save = true }) => {
    const position = await new Promise<GeolocationPosition>((resolve, reject) =>
      navigator.geolocation.getCurrentPosition(resolve, reject),
    );

    const location = {
      latitude: position.coords.latitude,
      longitude: position.coords.longitude,
      accuracy: position.coords.accuracy,
    };

    if (save) {
      await saveMemory("user_location", location);
    }

    return location;
  },
);
```

## Wire the implementations into `useStream`

Pass the implemented tools to `useStream`. When the agent emits a matching tool
call, the hook runs the client implementation and resumes the run for you.

Define a TypeScript interface matching your agent's state schema and pass it as
a type parameter to `useStream` for type-safe access to state values:

```ts types.ts
export interface AgentState {
  messages: BaseMessage[];
}
```

```tsx React
import { useStream } from "@langchain/react";

import { geolocationGet, memoryGet, memoryPut } from "./impl";
import type { AgentState } from "./types";

const AGENT_URL = "http://localhost:2024";

export function Chat() {
  const stream = useStream<AgentState>({
    apiUrl: AGENT_URL,
    assistantId: "headless_tools",
    tools: [memoryPut, memoryGet, geolocationGet],
  });

  return <ChatView messages={stream.messages} toolCalls={stream.toolCalls} />;
}
```

```vue Vue
<script setup lang="ts">
import { useStream } from "@langchain/vue";

import { geolocationGet, memoryGet, memoryPut } from "./impl";
import type { AgentState } from "./types";

const AGENT_URL = "http://localhost:2024";

const stream = useStream<AgentState>({
  apiUrl: AGENT_URL,
  assistantId: "headless_tools",
  tools: [memoryPut, memoryGet, geolocationGet],
});
</script>

<template>
  <ChatView
    :messages="stream.messages.value"
    :tool-calls="stream.toolCalls.value"
  />
</template>
```

```svelte Svelte
<script lang="ts">
  import { useStream } from "@langchain/svelte";

  import { geolocationGet, memoryGet, memoryPut } from "./impl";
  import type { AgentState } from "./types";

  const AGENT_URL = "http://localhost:2024";

  const { messages, toolCalls } = useStream<AgentState>({
    apiUrl: AGENT_URL,
    assistantId: "headless_tools",
    tools: [memoryPut, memoryGet, geolocationGet],
  });
</script>

<ChatView messages={$messages} toolCalls={$toolCalls} />
```

```ts Angular
import { Component } from "@angular/core";
import { useStream } from "@langchain/angular";

import { geolocationGet, memoryGet, memoryPut } from "./impl";
import type { AgentState } from "./types";

const AGENT_URL = "http://localhost:2024";

@Component({
  selector: "app-chat",
  template: `
    <app-chat-view
      [messages]="stream.messages()"
      [toolCalls]="stream.toolCalls()"
    />
  `,
})
export class ChatComponent {
  stream = useStream<AgentState>({
    apiUrl: AGENT_URL,
    assistantId: "headless_tools",
    tools: [memoryPut, memoryGet, geolocationGet],
  });
}
```

## Render tool activity inline

The playground renders each memory or geolocation operation as its own card and
keeps a small memory stats panel near the input. The key step is matching each
entry in `stream.toolCalls` back to the AI message that triggered it:

```tsx
import type { ToolCallWithResult, DefaultToolCall } from "@langchain/react";

function Message({ message, toolCalls }: {
  message: AIMessage,
  toolCalls: ToolCallWithResult[]
}) {
  const messageToolCalls = toolCalls.filter((tc) =>
    message.tool_calls?.some((call) => call.id === tc.call.id),
  );

  return (
    <div>
      {message.text && <p>{message.text}</p>}
      {messageToolCalls.map((tc) => (
        <HeadlessToolCard key={tc.call.id} toolCall={tc} />
      ))}
    </div>
  );
}
```

This works especially well with the richer UI patterns from
[Tool calling](Tool%20calling.md), where each tool result can
render as a specialized card instead of raw JSON.

## Use cases

Use headless tools when the work depends on APIs or data that only exist in the
client:

* Local memory in IndexedDB or `localStorage`
* Device APIs like geolocation, clipboard, camera, or file pickers
* Canvas, audio, or other browser-only rendering primitives
* Privacy-sensitive data that should stay on the user's device
* UI actions that need direct access to in-memory frontend state

## Best practices

* Keep tools small and typed. Prefer many narrow tools over one generic
  "run arbitrary browser code" tool.
* Return JSON-serializable results. Do not try to return DOM nodes, file
  handles, or other non-serializable browser objects.
* Share definitions, separate implementations. The agent and client should agree
  on tool names and schemas, but only the client should load browser APIs.
* Surface tool state in the UI. Use `stream.toolCalls` and `onTool` to show
  pending, success, and error states.
* Add review when needed. For sensitive client-side actions, pair this pattern
  with [Human-in-the-loop](Human-in-the-Loop.md).

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/frontend/headless-tools.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
