# Deploy with Next.js

> Deploy a LangChain deep agent in a Next.js App Router project with streaming chat, subagents, and thread history.

The following page details an example app that deploys a LangChain **deep agent** entirely inside a [Next.js App](https://nextjs.org/) Router project: streaming chat UI, subagents, and thread history, all backed by the [Agent Streaming Protocol](https://github.com/langchain-ai/agent-protocol/tree/main/streaming) implemented as Next.js Route Handlers (HTTP + SSE). No separate backend process.

Source: [`js-next`](https://github.com/langchain-ai/deployment-cookbook/tree/main/js-next) in the deployment cookbook.

## Deploy to Vercel

**1. Import the repository**

Click **Deploy with Vercel** below, or import [`langchain-ai/deployment-cookbook`](https://github.com/langchain-ai/deployment-cookbook) manually.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Flangchain-ai%2Fdeployment-cookbook\&root-directory=js-next\&env=OPENAI_API_KEY\&envDescription=OpenAI%20API%20key%20for%20the%20agent%20and%20its%20subagents)

**2. Configure the project**

Set **Root Directory** to `js-next` and add `OPENAI_API_KEY` in project settings.

**3. Deploy**

Deploy the project. Route handlers already set `runtime = "nodejs"` and the SSE route sets `dynamic = "force-dynamic"`, which Vercel needs for streaming.

Optionally enable LangSmith tracing by adding the variables from [`.env.example`](https://github.com/langchain-ai/deployment-cookbook/blob/main/js-next/.env.example).

## Required API endpoints

The app exposes the Agent Streaming Protocol under `/api/threads/...`. Route handlers live in `app/api/threads/`.

### Minimum (streaming chat)

These three endpoints are enough to run a single-threaded streaming chat with `@langchain/react`'s `HttpAgentServerAdapter`:

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
  subgraph browser["Browser"]
    SP["StreamProvider"]
    Adapter["HttpAgentServerAdapter"]
    SP --- Adapter
  end

  subgraph routes["Next.js Route Handlers (Node runtime)"]
    CMD["POST /api/threads/:id/commands"]
    STR["POST /api/threads/:id/stream (SSE)"]
    STA["GET|POST /api/threads/:id/state"]
  end

  subgraph server["lib/server"]
    SRV["session · threads · registry"]
  end

  subgraph agent["lib/agent"]
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
  class browser,routes process
  class server trigger
  class agent output
```

1. Bootstrap thread state (`GET`/`POST /state`).
2. On submit, the SDK sends `run.start` to `/commands` and receives a `run_id`.
3. The SDK subscribes to `/stream` (SSE) for replay + live protocol events.
4. Subagent (`task`) runs emit namespaced events surfaced as `stream.subagents`.

## Production persistence

Out of the box, the agent uses an in-memory `MemorySaver` checkpointer (`lib/agent/index.ts`) and a process-local session map (`lib/server/registry.ts`). That works for local dev and single-instance servers, but on Vercel (serverless, multiple replicas) conversation state is **not durable** across cold starts or instances.

For production, swap in a [durable checkpointer](https://docs.langchain.com/oss/python/langgraph/checkpointers.md#checkpointer-libraries):

| Package | Backend |
| - | - |
| [`@langchain/langgraph-checkpoint-redis`](https://www.npmjs.com/package/@langchain/langgraph-checkpoint-redis) | Redis (`RedisSaver`) |
| [`@langchain/langgraph-checkpoint-postgres`](https://www.npmjs.com/package/@langchain/langgraph-checkpoint-postgres) | Postgres (`PostgresSaver`) |
| [`@langchain/langgraph-checkpoint-sqlite`](https://www.npmjs.com/package/@langchain/langgraph-checkpoint-sqlite) | SQLite (`SqliteSaver`) |

Replace `MemorySaver` in `lib/agent/index.ts` and pass the new checkpointer to `createDeepAgent`. The route handlers and `lib/server/threads.ts` helpers stay the same.

### Redis on Vercel

A common choice for Vercel is Redis via the [Marketplace](https://vercel.com/docs/redis) (for example [Upstash Redis](https://vercel.com/marketplace/upstash)). Install the integration on your Vercel project; credentials are injected as environment variables automatically.

Then wire `@langchain/langgraph-checkpoint-redis`:

```ts
import { RedisSaver } from "@langchain/langgraph-checkpoint-redis";

const checkpointer = await RedisSaver.fromUrl(process.env.REDIS_URL!);
```

Use the connection string your Redis provider exposes (Upstash provides both REST and Redis-protocol URLs; the checkpointer needs the Redis URL).

You will also want a shared session/replay store in `lib/server/registry.ts` so SSE reconnection works across serverless invocations. The checkpointer swap is the main step for durable thread history; the session store is a separate concern for live-run replay.

For more information, see [checkpointer libraries](https://docs.langchain.com/oss/python/langgraph/checkpointers.md#checkpointer-libraries) and [add memory / persistence](https://docs.langchain.com/oss/python/langgraph/add-memory.md).

## Local development

```bash
cp .env.example .env.local   # set OPENAI_API_KEY
pnpm install
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000).

```bash
pnpm build   # production build
pnpm start   # serve the production build
pnpm lint    # eslint
```

## Project layout

* `lib/agent/`: deep agent (`createDeepAgent`) with `researcher` and `math-whiz` subagents and mock tools. Marked `server-only`.
* `lib/server/`: protocol server logic: `session.ts` (SSE runs), `threads.ts` (checkpointer-backed state), `serialize.ts`, `registry.ts`.
* `app/api/threads/`: Route Handlers for the protocol endpoints above.
* `lib/chat/threads-client.ts`: browser thread bootstrap and sidebar helpers.
* `components/`: chat UI (`ChatApp`, `Chat`, `MessageList`, `Subagents`, `ThreadHistory`, …).

## See also

* [Frameworks and platforms overview](Deploy%20full-stack%20web%20apps.md)
* [Agent Streaming Protocol](https://github.com/langchain-ai/agent-protocol/tree/main/streaming)
* [`react-custom-backend`](https://github.com/langchain-ai/streaming-cookbook) — original Vite + Hono reference for a custom protocol server
* [Next.js Route Handlers](https://nextjs.org/docs/app/building-your-application/routing/route-handlers)
