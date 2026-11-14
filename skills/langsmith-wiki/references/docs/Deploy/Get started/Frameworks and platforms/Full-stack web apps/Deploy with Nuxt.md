# Deploy with Nuxt

> Deploy a LangChain deep agent in a Nuxt 4 app with Nitro server routes, Vue composables, and subagent-aware chat UI.

The following page details an example app that deploys a LangChain **deep agent** inside a [Nuxt 4](https://nuxt.com) project: streaming chat UI, subagent detail views, thread history, and reasoning-token streaming, all backed by the [Agent Streaming Protocol](https://github.com/langchain-ai/agent-protocol/tree/main/streaming) implemented as Nitro route handlers (HTTP + SSE). No separate backend process.

Source: [`js-nuxt`](https://github.com/langchain-ai/deployment-cookbook/tree/main/js-nuxt) in the deployment cookbook.

## Deploy

> [tab] Vercel
>
> **1. Import the repository**
>
> Click **Deploy with Vercel** below, or import [`langchain-ai/deployment-cookbook`](https://github.com/langchain-ai/deployment-cookbook) manually.
>
> [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Flangchain-ai%2Fdeployment-cookbook\&root-directory=js-nuxt\&env=OPENAI_API_KEY\&envDescription=OpenAI%20API%20key%20for%20the%20agent%20and%20its%20subagents)
>
> **2. Configure the project**
>
> Set **Root Directory** to `js-nuxt` and add `OPENAI_API_KEY` in project settings.
>
> **3. Deploy**
>
> Deploy the project. Nuxt detects Vercel automatically and builds Nitro server routes for the Agent Streaming Protocol API.

> [tab] Netlify
>
> **1. Import the repository**
>
> Click **Deploy to Netlify** below, or import [`langchain-ai/deployment-cookbook`](https://github.com/langchain-ai/deployment-cookbook) manually.
>
> [![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/langchain-ai/deployment-cookbook\&base=js-nuxt)
>
> **2. Configure the project**
>
> Set **Base directory** to `js-nuxt`. Netlify runs the Nuxt build from that subdirectory.
>
> **3. Set environment variables**
>
> Add `OPENAI_API_KEY` in the Netlify deploy settings before the first build completes.

> [tab] Node
>
> **1. Build for production**
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> cd js-nuxt
> cp .env.example .env   # set OPENAI_API_KEY for local dev
> pnpm install
> pnpm build
> ```
>
> **2. Set environment variables**
>
> Export `OPENAI_API_KEY` on the host. Nitro reads it at runtime from the environment.
>
> Optionally enable LangSmith tracing by adding the variables from [`.env.example`](https://github.com/langchain-ai/deployment-cookbook/blob/main/js-nuxt/.env.example).
>
> **3. Start the Nitro server**
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> node .output/server/index.mjs
> ```
>
> Run behind any process manager or container orchestrator that keeps a Node.js process alive.

> [!TIP]
>
> `@langchain/vue` discovers subagents from the stream and renders a clickable chip per subagent. Selecting one opens a scoped chat view bound to that subagent's namespaced `messages` and `tools` channels via `useMessages`. Reasoning summaries stream into a collapsible "Thinking" block that auto-expands while streaming.

## Required API endpoints

The app exposes the Agent Streaming Protocol under `/api/threads/...`. Nitro route handlers live in `server/api/threads/`.

### Minimum (streaming chat)

These three endpoints are enough to run a single-threaded streaming chat with `@langchain/vue`'s `HttpAgentServerAdapter`:

| Method | Path | Purpose |
| - | - | - |
| `POST` | `/api/threads/:threadId/commands` | Accept protocol commands (`run.start`, …) and start agent runs |
| `POST` | `/api/threads/:threadId/stream` | SSE stream of protocol events for a run |
| `GET` / `POST` | `/api/threads/:threadId/state` | Read and bootstrap checkpointed thread state |

The client bootstraps a thread with `GET /state` (and `POST /state` on 404) so hydration does not 404 before the first message is sent.

### Optional (thread sidebar)

This example also implements endpoints for the thread-history sidebar. Omit them if your UI does not need multi-thread management:

| Method | Path | Purpose |
| - | - | - |
| `GET` | `/api/threads` | List threads known to the checkpointer |
| `DELETE` | `/api/threads/:threadId` | Delete a thread's session and checkpoints |
| `POST` | `/api/threads/:threadId/history` | Paginated checkpoint history (Agent Protocol) |

### Request flow

```mermaid
%%{init: {"themeVariables": {"lineColor": "#40668D", "primaryColor": "#E5F4FF", "primaryTextColor": "#030710", "primaryBorderColor": "#006DDD"}}}%%
flowchart TB
  subgraph browser["Browser (Vue)"]
    SP["StreamProvider"]
    Adapter["HttpAgentServerAdapter"]
    SP --- Adapter
  end

  subgraph nitro["Nitro route handlers"]
    CMD["POST /api/threads/:id/commands"]
    STR["POST /api/threads/:id/stream (SSE)"]
    STA["GET|POST /api/threads/:id/state"]
  end

  subgraph server["server/utils"]
    SRV["session · threads · runtime"]
  end

  subgraph agent["server/agent"]
    AGT["createDeepAgent + checkpointer"]
  end

  Adapter -->|POST| CMD
  Adapter -->|POST| STR
  Adapter -->|GET / POST| STA
  CMD --> SRV
  STR --> SRV
  STA --> SRV
  SRV --> AGT

  classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
  classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
  classDef output fill:#EBD0F0,stroke:#885270,stroke-width:2px,color:#441E33
  class browser,nitro process
  class server trigger
  class agent output
```

1. Bootstrap thread state (`GET`/`POST /state`).
2. On submit, the SDK sends `run.start` to `/commands` and receives a `run_id`.
3. The SDK subscribes to `/stream` (SSE) for replay + live protocol events.
4. Subagent (`task`) runs emit namespaced events surfaced as `stream.subagents`.

## Nitro backend design

| Concern | Implementation |
| - | - |
| Frontend | Vue components in `app/` (wrapped in `<ClientOnly>` for SSE) |
| API layer | Nitro route handlers in `server/api/threads/` |
| Runtime | Node.js (Nitro preset depends on deploy target) |
| SSE replay | Process-local `LocalThreadSession` (`server/utils/session.ts`) |
| Agent runs | Same Nitro process; events buffered in a LangGraph `StreamChannel` |
| Thread storage | In-memory `MemorySaver` checkpointer (`server/agent/index.ts`) |
| Secrets | `.env` locally; host environment variables in production |

The agent's checkpointer is the single source of truth for threads. There is no client-side cache: the sidebar is always fetched from the server, and restarting the server clears every thread.

## Production persistence

Out of the box, the agent uses an in-memory `MemorySaver` checkpointer (`server/agent/index.ts`) and a process-local session map (`server/utils/runtime.ts`). That works for local dev and single-instance servers, but on serverless or multi-instance hosts conversation state is **not durable** across cold starts or replicas.

For production, swap in a [durable checkpointer](https://docs.langchain.com/oss/python/langgraph/checkpointers.md#checkpointer-libraries):

| Package | Backend |
| - | - |
| [`@langchain/langgraph-checkpoint-redis`](https://www.npmjs.com/package/@langchain/langgraph-checkpoint-redis) | Redis (`RedisSaver`) |
| [`@langchain/langgraph-checkpoint-postgres`](https://www.npmjs.com/package/@langchain/langgraph-checkpoint-postgres) | Postgres (`PostgresSaver`) |
| [`@langchain/langgraph-checkpoint-sqlite`](https://www.npmjs.com/package/@langchain/langgraph-checkpoint-sqlite) | SQLite (`SqliteSaver`) |

Replace `MemorySaver` in `server/agent/index.ts` and pass the new checkpointer to `createDeepAgent`. The Nitro route handlers and `server/utils/threads.ts` helpers stay the same.

You will also want a shared session/replay store in `server/utils/runtime.ts` so SSE reconnection works across serverless invocations.

For more information, see [checkpointer libraries](https://docs.langchain.com/oss/python/langgraph/checkpointers.md#checkpointer-libraries) and [add memory / persistence](https://docs.langchain.com/oss/python/langgraph/add-memory.md).

## Local development

```bash
cp .env.example .env   # set OPENAI_API_KEY
pnpm install
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000). Send a prompt that delegates to subagents and watch their work stream into dedicated cards.

```bash
pnpm build      # production build
pnpm preview    # preview the production build
pnpm typecheck  # vue-tsc over the project
```

## Project layout

> [accordion] Project structure
>
> * `server/agent/` — deep agent (`createDeepAgent`) with `researcher` and `math-whiz` subagents, mock tools, and `stripReasoningReplay` middleware.
> * `server/utils/` — protocol server logic: `session.ts` (SSE runs), `threads.ts` (checkpointer-backed state), `serialize.ts`, `runtime.ts`.
> * `server/api/threads/` — Nitro route handlers for the protocol endpoints above.
> * `app/components/` — Vue chat UI (`ChatApp`, `Chat`, `ThreadHistory`, `SubagentList`, `MessageReasoning`, …) using `@langchain/vue`.
> * `app/utils/threads.ts` — server-driven thread helpers and LangGraph SDK bootstrap.

> [accordion] Backend details
>
> * `server/agent/index.ts` — coordinator uses a reasoning model over the Responses API; tool-using subagents use chat-completions (to avoid reasoning item replay through the checkpointer).
> * `server/agent/middleware.ts` — rebuilds prior assistant messages from `content` + `tool_calls` so stale reasoning ids are never replayed to the Responses API.
> * `server/utils/session.ts` — `LocalThreadSession` buffers protocol events and fans matching frames out over SSE via `matchesSubscription`.
> * `server/api/threads/index.get.ts` — `GET /api/threads`, the checkpointer-backed thread list.
> * `server/api/threads/[threadId]/…` — handlers for `commands`, `stream`, `state` (GET/POST), `history`, and `DELETE`.

> [accordion] Frontend details
>
> * `app/components/ChatThread.vue` — builds the `HttpAgentServerAdapter` and calls `provideStream({ transport, threadId })`.
> * `app/components/Chat.vue` — message view with composer and per-subagent detail view (with breadcrumb).
> * `app/components/SubagentList.vue` / `SubagentDetail.vue` — inline subagent cards and scoped subagent chat (`useMessages` bound to namespace).
> * `app/components/MessageReasoning.vue` — collapsible "Thinking" block for reasoning summaries.

## See also

* [Frameworks and platforms overview](Deploy%20full-stack%20web%20apps.md)
* [Agent Streaming Protocol](https://github.com/langchain-ai/agent-protocol/tree/main/streaming)
* [`react-custom-backend`](https://github.com/langchain-ai/streaming-cookbook) — original Vite + Hono reference for a custom protocol server
* [`@langchain/vue`](https://www.npmjs.com/package/@langchain/vue) — `useStream`, `provideStream`, and selector composables
* [Frontend overview](https://docs.langchain.com/oss/python/langchain/frontend/overview.md)
