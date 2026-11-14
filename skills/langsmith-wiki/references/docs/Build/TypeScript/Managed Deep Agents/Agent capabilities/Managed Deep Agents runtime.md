# Managed Deep Agents runtime

> Read run context, the verified caller, the thread, and the sandbox from the native runtime types that agent factories, tools, and middleware receive.

Agent factories, tools, and middleware hooks each receive a runtime. It is the native LangChain or LangGraph runtime with three managed fields added. Context, state, and the store work as they do in [LangChain](https://docs.langchain.com/oss/javascript/langchain/runtime.md), and your type checker sees your own context type.

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

## Understand the runtime types

Managed Deep Agents extends one native type for each place your code runs:

| Code | Type | Extends |
| - | - | - |
| Agent factory | `ManagedServerRuntime<Context>` | `ServerRuntime` from `@langchain/langgraph-sdk` |
| Tool | `ManagedToolRuntime<State, Context>` | `ToolRuntime` from `@langchain/core/tools` |
| Middleware hook | `ManagedRuntime<Context>` | `Runtime` from `langchain` |

Type parameters follow the native order, so `ManagedToolRuntime` takes state first, then context. Both parameters are optional. `ManagedDeepAgentRuntime` is an alias for `ManagedToolRuntime`.

Each type keeps every native field and method, such as `context`, `state`, `store`, `writer`, and `toolCallId`. Managed Deep Agents adds three fields:

* **`serverInfo`**: Native server metadata plus the verified caller. Tools and middleware receive it.
* **`thread`**: The run's thread and the channel conversation it came from. See [Thread](#thread).
* **`backend`**: The thread's [sandbox](Add%20a%20sandbox%20to%20Managed%20Deep%20Agents.md) filesystem. `undefined` when the project declares no sandbox.

## Separate context, caller, and delivery

Context, the caller, and the channel delivery come from different sources and have different trust levels. The runtime keeps them in separate fields:

* **Context** comes from the `context` parameter of an API call. LangGraph validates it against your context schema. Use it to select behavior, not to grant access.
* **Server info** comes from [identity](Add%20identity%20to%20Managed%20Deep%20Agents.md), which resolves the caller from a verified token. Managed Deep Agents strips identity keys that a client sends through `configurable`, so use this field for authorization.
* **Channel** comes from managed [channel](Channels/Connect%20Managed%20Deep%20Agents%20to%20channels.md) ingress, which verifies the delivery before the run starts. A `channel` key in a direct API call's context does not create `runtime.thread.origin`.

API callers pass context next to the input:

```ts
await client.runs.create(threadId, "support", {
  input: { messages: [{ role: "user", content: "Where is my order?" }] },
  context: { tier: "fast" },
});
```

### Handle channel runs without context

A channel delivery carries no application context. Managed Deep Agents removes delivery data before LangGraph validates context, so required context fields do not reject channel runs. Direct API runs keep native validation.

On channel runs, context is `undefined` in the agent factory and tools, and an empty object in native middleware.

To tell a channel run from a direct run, check `runtime.thread.origin`.

## Read the runtime in the agent factory

An agent factory receives a `ManagedServerRuntime`: the native [`ServerRuntime`](../../../../Deploy/Agent%20Server/Server%20customization/Rebuild%20graph%20at%20runtime.md) plus `thread` and `backend`. To write a factory, see [Select configuration per run](Define%20a%20Managed%20Deep%20Agent.md#select-configuration-per-run).

Agent Server also calls the factory to read schemas and state. `accessContext` names the operation. [`executionRuntime`](../../../../Deploy/Agent%20Server/Server%20customization/Rebuild%20graph%20at%20runtime.md#access-contexts) is `null` outside `threads.create_run`, so read run context from `executionRuntime.context`. Return the same graph structure and schemas from every call.

`thread` is available, so a factory can choose configuration per channel. `backend` is always `undefined`, because the factory selects the sandbox.

## Read the runtime in tools

Annotate the runtime parameter with `ManagedToolRuntime`:

```ts tools/check-order.ts
import { tool } from "langchain";
import type { ManagedToolRuntime } from "managed-deepagents";
import { z } from "zod";

type AppContext = { region?: string };

export const checkOrder = tool(
  async ({ orderId }, runtime: ManagedToolRuntime<unknown, AppContext>) => {
    const principal = runtime.serverInfo?.principal;
    if (!principal) return "Sign in to check orders.";
    await runtime.thread?.origin?.channel.post?.({
      type: "content",
      content: "Checking that order now.",
    });
    const region = runtime.context?.region ?? "us";
    return `Order ${orderId} for ${principal.id} ships from ${region}.`;
  },
  {
    name: "check_order",
    description: "Check the status of an order.",
    schema: z.object({ orderId: z.string() }),
  }
);
```

`principal` is absent when no caller resolved, because identity is opt-in. `post` sends an additional message, and the agent's final reply still posts automatically. For more on writing tools, see [Custom tools](Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md).

## Read the runtime in middleware

Cast the hook's runtime to `ManagedRuntime` to read the managed fields:

```ts middleware/log-caller.ts
import { createMiddleware } from "langchain";
import type { ManagedRuntime } from "managed-deepagents";

type AppContext = { region?: string };

export const logCaller = createMiddleware({
  name: "LogCaller",
  beforeModel: (_state, runtime) => {
    const { serverInfo, thread } = runtime as ManagedRuntime<AppContext>;
    const caller = serverInfo?.principal?.id ?? "anonymous";
    console.log(`${caller} via ${thread?.origin?.channel.provider ?? "api"}`);
    return undefined;
  },
});
```

Tool-call hooks receive a `ManagedToolRuntime`. Declarative subagents receive the same managed fields. Neither requires an identity or sandbox declaration. For more on writing middleware, see [Custom middleware](Add%20custom%20middleware%20to%20Managed%20Deep%20Agents.md).

## Reference the managed fields

### Server info

`runtime.serverInfo` is a `ManagedServerInfo`. It keeps the native `assistantId`, `graphId`, and `user` fields and adds the caller:

* **`principal`**: The verified caller. `id` is the caller ID, `kind` is `"person"`, `"service"`, or `"channel"`, and `claims` holds the token claims. `claims.groups` is always a string array, and `claims.email` is always a string.
* **`subject`**: The authority the run acts with. `authority` is `"agent"` or `"user"`, with `agent_id` and `user_id`.
* **`link`**: The account link. `status` currently reports `"not_required"`.
* **`source`**: Where the run entered. `provider` is a value such as `"http"`, `"schedule"`, `"studio"`, or `"slack"`, with an optional `threadId`.

Read the caller from `principal`, not from the native `user`. For identity providers and claim mapping, see [Identity](Add%20identity%20to%20Managed%20Deep%20Agents.md).

### Thread

`runtime.thread` is a `ManagedThread`:

* **`id`**: The LangGraph thread ID.
* **`origin`**: The channel conversation the thread came from, with its `channel` and the `sender` of the latest message. Not set on a thread that no channel message reached.
* **`participants`**: The people on the thread. Each has an `id` and a `role`, `"owner"` or `"member"`.

> [!WARNING]
>
> `runtime.channel` is deprecated and will be removed in `managed-deepagents` 0.11. Read `runtime.thread.origin.channel` instead.

### Channel

`runtime.thread.origin.channel` is a `RuntimeChannel`:

* **`name`**: The configured channel name.
* **`provider`**: The provider label, such as `"slack"`.
* **`event`**: The typed delivery. `null` in a run that no channel event started, such as a Studio resume. See the event types below.
* **`rawEvent`**: The original provider payload, when the channel supplies one. For Slack, this is the inner Slack event without HTTP headers or the Trigger envelope. A resume can omit it.
* **`post`**: An async function that sends a message to the conversation that started the run. `undefined` when the channel cannot send.

`event.type` is one of:

* **`message`**: A new message. `messages` holds the incoming messages.
* **`user_prompt_response`**: A reply to an interactive prompt. Carries `action`, an optional `value`, and an optional `correlation_id`. See [Agent-owned interrupts](Channels/Prompt%20Slack%20users%20with%20agent-owned%20interrupts.md).
* **`interrupt_resume`**: A resume for a pending interrupt. `resume` holds the resume value.

`post` accepts a content message, `{"type": "content", "content": ...}`, or a native message, `{"type": "native", "native": ...}`. The built-in Slack channel sends text content only. The reply target stays private: `post` has no address or destination override, and code cannot read or replace the target.

### Backend

`runtime.backend` reads and writes files in the thread's sandbox. See [Read and write sandbox files from code](Add%20a%20sandbox%20to%20Managed%20Deep%20Agents.md#read-and-write-sandbox-files-from-code).

## See also

* [Runtime](https://docs.langchain.com/oss/javascript/langchain/runtime.md)
* [Rebuild graph at runtime](../../../../Deploy/Agent%20Server/Server%20customization/Rebuild%20graph%20at%20runtime.md)
* [Agent definition](Define%20a%20Managed%20Deep%20Agent.md)
* [Custom tools](Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md)
* [Custom middleware](Add%20custom%20middleware%20to%20Managed%20Deep%20Agents.md)
* [Channels](Channels/Connect%20Managed%20Deep%20Agents%20to%20channels.md)
* [Identity](Add%20identity%20to%20Managed%20Deep%20Agents.md)
