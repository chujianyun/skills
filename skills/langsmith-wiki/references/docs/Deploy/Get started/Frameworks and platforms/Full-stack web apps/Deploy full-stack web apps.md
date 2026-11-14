# Deploy full-stack web apps

> Deploy LangChain agents as full-stack web apps on Next.js, SvelteKit, Nuxt, Cloudflare Workers, Deno Deploy, and Vite with streaming UI and thread history.

The following pages provide reference implementations for running LangChain agents in production on JavaScript frameworks and hosting platforms. Each example in the [deployment cookbook repository](https://github.com/langchain-ai/deployment-cookbook) is a full-stack chat app with streaming UI, subagents, and thread history, deployed on a different platform using the same [Agent Streaming Protocol](https://github.com/langchain-ai/agent-protocol/tree/main/streaming).

Use these guides when you need to ship an agent-backed product: copy the stack that matches your hosting environment, swap in your own tools and models, and upgrade persistence when you move beyond a single instance.

## Examples

### Pair with LangSmith Agent Server

The agent runs on LangSmith Agent Server, and a separate web app streams from the Agent Server API.

> [card] [LangSmith + Vite](Deploy%20with%20LangSmith%20and%20Vite.md)
>
> Agent graph on LangSmith Agent Server; Vite + React UI streams from the Agent Server API.

### Embed in your web framework

The agent runs inside the framework's route handlers and ships as one deployable app to the host platform.

> [card] [Next.js](Deploy%20with%20Next.js.md)
>
> App Router route handlers implement the protocol under `/api/threads/...`. Deploy to Vercel with one click.

> [card] [SvelteKit](Deploy%20with%20SvelteKit.md)
>
> SvelteKit server routes on Cloudflare Workers with `@langchain/svelte` and per-thread Durable Objects for SSE replay.

> [card] [Nuxt](Deploy%20with%20Nuxt.md)
>
> Nitro route handlers and `@langchain/vue` composables in a single deployable Nuxt 4 app.

> [card] [Cloudflare Workers](Deploy%20with%20Cloudflare%20Workers.md)
>
> Vite + React SPA and Hono API on one Worker with Workers Assets and Durable Objects.

> [card] [Deno Deploy](Deploy%20with%20Deno%20Deploy.md)
>
> Deno.serve + Hono serves the protocol API and a Vite-built React SPA from one entrypoint.

> [!TIP]
>
> Each cookbook example shares the same demo agent: a coordinator that delegates to `researcher` and `math-whiz` subagents with mock tools, so you can compare hosting choices without changing application behavior.

## What goes into an agent deployment

Every example follows the same shape. The framework and hosting change; the responsibilities do not.

### Agent runtime

The agent itself, typically a LangGraph graph or [`deepagents`](https://www.npmjs.com/package/deepagents) coordinator, with tools, optional subagents, and middleware. It is compiled with a **checkpointer** so conversation state survives across turns. Examples start with an in-memory `MemorySaver` for simplicity; production deployments swap in Redis ([`@langchain/langgraph-checkpoint-redis`](https://www.npmjs.com/package/@langchain/langgraph-checkpoint-redis)), Postgres ([`@langchain/langgraph-checkpoint-postgres`](https://www.npmjs.com/package/@langchain/langgraph-checkpoint-postgres)), SQLite ([`@langchain/langgraph-checkpoint-sqlite`](https://www.npmjs.com/package/@langchain/langgraph-checkpoint-sqlite)), or platform-specific storage.

### Protocol server

HTTP route handlers implement the [Agent Streaming Protocol](https://github.com/langchain-ai/agent-protocol/tree/main/streaming) under `/api/threads/...`.

#### Minimum (streaming chat)

These three endpoints are enough to run a single-threaded streaming chat with `HttpAgentServerAdapter`:

| Method | Path | Purpose |
| - | - | - |
| `POST` | `/api/threads/:threadId/commands` | Accept commands (`run.start`, …) and start runs |
| `POST` | `/api/threads/:threadId/stream` | SSE stream of protocol events for a run |
| `GET` / `POST` | `/api/threads/:threadId/state` | Read and bootstrap checkpointed thread state |

#### Thread sidebar (all examples)

Every example also implements endpoints for the thread-history sidebar:

| Method | Path | Purpose |
| - | - | - |
| `GET` | `/api/threads` | List threads known to the checkpointer |
| `DELETE` | `/api/threads/:threadId` | Delete a thread's session and checkpoints |
| `POST` | `/api/threads/:threadId/history` | Paginated checkpoint history |

### Session and run management

Server-side logic tracks active runs, bridges commands to the agent, and fans out live events over SSE. A registry or session store lets clients reconnect to in-flight streams. On serverless or multi-instance hosts, this layer must be shared or colocated with the checkpointer.

### Chat frontend

A browser UI wired to the protocol through `HttpAgentServerAdapter`, from [`@langchain/react`](https://www.npmjs.com/package/@langchain/react), [`@langchain/vue`](https://www.npmjs.com/package/@langchain/vue), [`@langchain/svelte`](https://www.npmjs.com/package/@langchain/svelte), or [`@langchain/angular`](https://www.npmjs.com/package/@langchain/angular). The client bootstraps thread state, submits messages, consumes the SSE stream, and renders tokens, tool calls, reasoning, and subagent activity.

These bindings ship no components of their own. Hooks like `useStream` return plain reactive state (messages, tool calls, loading flags, thread metadata) that you wire to whatever visual layer you prefer. For adapter patterns and trade-offs, see the [frontend integrations overview](https://docs.langchain.com/oss/python/langchain/frontend/integrations/overview.md).

## See also

* [LangSmith Agent Server overview](../../LangSmith%20Agent%20Server.md)
* [Agent Server](../../../Agent%20Server/Capabilities/Agent%20Server.md)
* [Configure checkpointer](../../../Agent%20Server/Develop%20your%20application/Persistence/Configure%20checkpointer%20backend.md)
* [Frontend overview](https://docs.langchain.com/oss/python/langchain/frontend/overview.md)
