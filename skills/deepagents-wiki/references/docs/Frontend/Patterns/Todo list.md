# Todo list

> Track agent progress with a real-time todo list synced from agent state

Not every agent interaction is a chat. Sometimes the agent is executing a
multi-step plan, and the best way to show progress is a **todo list** that
updates in real time. The deep agent todo list pattern reads a `todos` array
directly from the agent's state, rendering each item with its current status as
the agent works through its plan. It's a progress dashboard built on the same
`useStream` hook you use for chat. It shows that agent state can power any UI,
not just message bubbles.

## How it works

Deep agents can expose a **`todos` state** channel when you opt into [`TodoListMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/todo/TodoListMiddleware). That middleware adds the `write_todos` tool and persists task progress as the agent works through its plan. As the agent executes, it updates each
todo's status from `"pending"` to `"in_progress"` to `"completed"`. The
[`useStream`](https://reference.langchain.com/javascript/langchain-react/index/useStream) hook exposes this state via `stream.values.todos`, and your UI
renders it reactively.

> [!NOTE]
>
> Task planning is opt-in. Without [`TodoListMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/todo/TodoListMiddleware), `stream.values.todos` is not present. See [Task planning](../../Deep%20Agents%20overview.md#task-planning).

The flow looks like this:

1. User submits a request
2. Agent creates a plan and populates `todos` in its state
3. Agent begins executing each todo transitions through `pending` →
   `in_progress` → `completed`
4. `stream.values.todos` updates in real time as the agent progresses
5. Your UI re-renders the todo list with current statuses

## Setting up `useStream`

Enable [`TodoListMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/todo/TodoListMiddleware) on the agent.

```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain.agents.middleware import TodoListMiddleware

agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    middleware=[TodoListMiddleware()],
)
```

```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain.agents.middleware import TodoListMiddleware

agent = create_deep_agent(
    model="openai:gpt-5.5",
    middleware=[TodoListMiddleware()],
)
```

```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain.agents.middleware import TodoListMiddleware

agent = create_deep_agent(
    model="anthropic:claude-sonnet-5",
    middleware=[TodoListMiddleware()],
)
```

```python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain.agents.middleware import TodoListMiddleware

agent = create_deep_agent(
    model="openrouter:z-ai/glm-5.2",
    middleware=[TodoListMiddleware()],
)
```

```python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain.agents.middleware import TodoListMiddleware

agent = create_deep_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    middleware=[TodoListMiddleware()],
)
```

```python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain.agents.middleware import TodoListMiddleware

agent = create_deep_agent(
    model="baseten:zai-org/GLM-5.2",
    middleware=[TodoListMiddleware()],
)
```

```python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain.agents.middleware import TodoListMiddleware

agent = create_deep_agent(
    model="ollama:north-mini-code-1.0",
    middleware=[TodoListMiddleware()],
)
```

Then point [`useStream`](https://reference.langchain.com/javascript/langchain-react/index/useStream) at that agent and
read the `todos` from `stream.values`.

> [!NOTE]
>
> The code examples use `useStream<typeof myAgent>` for type-safe stream state. See Type inference for [Python](https://docs.langchain.com/oss/python/langchain/frontend/overview.md#type-inference) or [JavaScript](https://docs.langchain.com/oss/javascript/langchain/frontend/overview.md#type-inference) backends.

```tsx React theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import { useStream } from "@langchain/react";

const AGENT_URL = "http://localhost:2024";

export function TodoAgent() {
  const stream = useStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "deep_agent_todo_list",
  });

  const todos = stream.values?.todos ?? [];

  return (
    <div>
      <TodoList todos={todos} />
      {stream.messages.map((msg) => (
        <Message key={msg.id} message={msg} />
      ))}
    </div>
  );
}
```

```vue Vue theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
<script setup lang="ts">
import { useStream } from "@langchain/vue";
import { computed } from "vue";

const AGENT_URL = "http://localhost:2024";

const stream = useStream<typeof myAgent>({
  apiUrl: AGENT_URL,
  assistantId: "deep_agent_todo_list",
});

const todos = computed(() => stream.values.value?.todos ?? []);
</script>

<template>
  <div>
    <TodoList :todos="todos" />
    <Message
      v-for="msg in stream.messages.value"
      :key="msg.id"
      :message="msg"
    />
  </div>
</template>
```

```svelte Svelte theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
<script lang="ts">
  import { useStream } from "@langchain/svelte";

  const AGENT_URL = "http://localhost:2024";

  const stream = useStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "deep_agent_todo_list",
  });

  const todos = $derived(stream.values?.todos ?? []);
</script>

<div>
  <TodoList {todos} />
  {#each stream.messages as msg (msg.id)}
    <Message message={msg} />
  {/each}
</div>
```

```ts Angular theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import { Component, computed } from "@angular/core";
import { injectStream } from "@langchain/angular";

const AGENT_URL = "http://localhost:2024";

@Component({
  selector: "app-todo-agent",
  template: `
    <div>
      <app-todo-list [todos]="todos()" />
      @for (msg of stream.messages(); track msg.id) {
        <app-message [message]="msg" />
      }
    </div>
  `,
})
export class TodoAgentComponent {
  stream = injectStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "deep_agent_todo_list",
  });

  todos = computed(() => this.stream.values()?.todos ?? []);
}
```

## Building the TodoList component

The todo list renders each item with a status icon, color coding, and visual
styling that reflects the current state:

```tsx theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
function TodoList({ todos }: { todos: Todo[] }) {
  const completed = todos.filter((t) => t.status === "completed").length;
  const percentage = todos.length
    ? Math.round((completed / todos.length) * 100)
    : 0;

  return (
    <div className="rounded-lg border bg-white p-4 shadow-sm">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold">Agent Progress</h2>
        <span className="text-sm text-gray-500">
          {completed}/{todos.length} tasks
        </span>
      </div>

      <ProgressBar percentage={percentage} />

      <ul className="mt-4 space-y-2">
        {todos.map((todo, i) => (
          <TodoItem key={i} todo={todo} />
        ))}
      </ul>
    </div>
  );
}
```

## Progress bar

A visual progress bar gives users an at-a-glance summary of overall completion:

```tsx theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
function ProgressBar({ percentage }: { percentage: number }) {
  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-xs text-gray-500">
        <span>Progress</span>
        <span>{percentage}%</span>
      </div>
      <div className="h-2 overflow-hidden rounded-full bg-gray-200">
        <div
          className="h-full rounded-full bg-green-500 transition-all duration-500"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
```

## Individual todo items

Each item gets a status icon, color-coded text, and strikethrough styling for
completed tasks:

```tsx theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
function TodoItem({ todo }: { todo: Todo }) {
  const config = {
    pending: {
      icon: "○",
      textClass: "text-gray-600",
      bgClass: "bg-gray-50",
      iconClass: "text-gray-400",
    },
    in_progress: {
      icon: "◉",
      textClass: "text-amber-800",
      bgClass: "bg-amber-50 border-amber-200",
      iconClass: "text-amber-500 animate-pulse",
    },
    completed: {
      icon: "✓",
      textClass: "text-green-800 line-through",
      bgClass: "bg-green-50 border-green-200",
      iconClass: "text-green-500",
    },
  };

  const style = config[todo.status];

  return (
    <li
      className={`flex items-start gap-3 rounded-md border px-3 py-2 ${style.bgClass}`}
    >
      <span className={`mt-0.5 text-lg leading-none ${style.iconClass}`}>
        {style.icon}
      </span>
      <span className={`text-sm ${style.textClass}`}>{todo.content}</span>
    </li>
  );
}
```

The `in_progress` icon uses `animate-pulse` to draw attention to the currently
active task.

## Calculating progress

Derive progress metrics directly from the todos array:

```ts theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
const todos = stream.values?.todos ?? [];

const completed = todos.filter((t) => t.status === "completed").length;
const inProgress = todos.filter((t) => t.status === "in_progress").length;
const pending = todos.filter((t) => t.status === "pending").length;
const percentage = todos.length
  ? Math.round((completed / todos.length) * 100)
  : 0;
```

These values update reactively as the agent modifies its state, keeping the
progress bar and counters in sync.

## Combining with chat messages

The todo list works alongside the regular chat interface. A practical layout
shows the todo list as a persistent sidebar or header panel, with chat messages
below:

```tsx theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
function TodoAgentLayout() {
  const stream = useStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "deep_agent_todo_list",
  });

  const todos = stream.values?.todos ?? [];

  return (
    <div className="flex h-screen flex-col">
      {todos.length > 0 && (
        <div className="border-b bg-gray-50 p-4">
          <TodoList todos={todos} />
        </div>
      )}

      <main className="flex-1 overflow-y-auto p-6">
        <div className="mx-auto max-w-2xl space-y-4">
          {stream.messages.map((msg) => (
            <Message key={msg.id} message={msg} />
          ))}
        </div>
      </main>

      <ChatInput
        onSubmit={(text) =>
          stream.submit({ messages: [{ type: "human", content: text }] })
        }
        isLoading={stream.isLoading}
      />
    </div>
  );
}
```

> [!TIP]
>
> Show the todo list only when `todos.length > 0`. Before the agent creates its
> plan, there's nothing to display. Showing an empty component wastes space.

## Use cases

The todo list pattern fits any scenario where an agent executes a structured
plan:

* **Project planning**: agent breaks a project into tasks and works through
  them sequentially
* **Research workflows**: each research question becomes a todo that the agent
  investigates and completes
* **Data processing**: steps like ingestion, validation, transformation, and
  export each get their own todo
* **Onboarding flows**: agent walks through setup steps, checking off each one
  as it configures services
* **Report generation**: sections of a report become todos: gather data,
  analyze trends, write summary, format output

## Handling empty and loading states

Handle the initial state before the agent has created its plan:

```tsx theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
function TodoList({ todos, isLoading }: { todos: Todo[]; isLoading: boolean }) {
  if (todos.length === 0 && !isLoading) {
    return null;
  }

  if (todos.length === 0 && isLoading) {
    return (
      <div className="rounded-lg border bg-white p-4 shadow-sm">
        <div className="flex items-center gap-2 text-sm text-gray-500">
          <span className="animate-spin">⟳</span>
          Agent is creating a plan...
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-lg border bg-white p-4 shadow-sm">
      {/* ... full todo list rendering */}
    </div>
  );
}
```

## Best practices

* **Show the todo list prominently**. It's the primary progress indicator for
  plan-based agents. Don't bury it below the fold.
* **Animate status transitions**. Smooth transitions make the agent feel more
  responsive. Use CSS transitions on background color, text decoration, and
  opacity.
* **Only highlight one `in_progress` item**. Agents typically work on one task
  at a time. If multiple items show as `in_progress`, the UI gets noisy.
  Consider only pulsing the first one.
* **Collapse or dim completed items**. As the list grows, completed items
  become less relevant. Reduce their visual weight so users focus on what's
  still happening.
* **Show the progress percentage**. A single number like "67% complete" is
  immediately understandable, even from across the room.
* **Keep the todo list in sync**. Because `stream.values` updates reactively,
  the todo list stays current automatically. Don't add manual polling or
  refresh logic.

## Related LangChain guides

The todo list pattern is a specialization of the broader LangChain approach to
rendering structured agent state. These guides cover related techniques that
pair well with plan-based agents:

> [card] [Structured output](https://docs.langchain.com/oss/python/langchain/frontend/structured-output.md)
>
> Render any structured agent state—not just todos—with custom UI components instead of plain text.

> [card] [Join & rejoin streams](https://docs.langchain.com/oss/python/langchain/frontend/join-rejoin.md)
>
> Reconnect to a running plan after a page reload or tab switch without losing progress.

> [card] [Message queues](https://docs.langchain.com/oss/python/langchain/frontend/message-queues.md)
>
> Queue follow-up tasks while the agent is still working through its current plan.

> [card] [Human-in-the-Loop](https://docs.langchain.com/oss/python/langchain/frontend/human-in-the-loop.md)
>
> Pause and resume plan execution when the agent needs user approval or input.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/deepagents/frontend/todo-list.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
