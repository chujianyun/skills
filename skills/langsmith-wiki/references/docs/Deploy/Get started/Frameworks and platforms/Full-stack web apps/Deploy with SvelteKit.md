# Deploy with SvelteKit

> Deploy a LangChain deep agent in a SvelteKit project on Cloudflare Workers with streaming chat and thread history.

The following page details an example app that deploys a LangChain **deep agent** inside a [SvelteKit](https://svelte.dev/docs/kit/introduction) project, built for [Cloudflare Workers](https://svelte.dev/docs/kit/adapter-cloudflare) with [`@sveltejs/adapter-cloudflare`](https://www.npmjs.com/package/@sveltejs/adapter-cloudflare): streaming chat UI, subagent detail views, thread history, and the [Agent Streaming Protocol](https://github.com/langchain-ai/agent-protocol/tree/main/streaming) exposed under `/api/threads/...`. No separate backend process is required.

Source: [`js-sveltekit`](https://github.com/langchain-ai/deployment-cookbook/tree/main/js-sveltekit) in the deployment cookbook.

## Deploy to Cloudflare

**1. Install and build**

```bash
cd js-sveltekit
cp .env.example .env   # set OPENAI_API_KEY for local dev
pnpm install
pnpm build
```

**2. Configure secrets**

```bash
npx wrangler login
npx wrangler secret put OPENAI_API_KEY
```

**3. Deploy**

```bash
pnpm run deploy
```

`svelte.config.js` uses `adapter-cloudflare()`. `wrangler.jsonc` points Wrangler at `.svelte-kit/cloudflare/_worker.js` and serves assets from `.svelte-kit/cloudflare`, matching the SvelteKit Cloudflare adapter docs. The build script appends the `ThreadSession` Durable Object export to that generated Worker entry because Durable Object classes must be exported by the Worker module.

`nodejs_compat` and `nodejs_compat_populate_process_env` are enabled because the LangChain runtime and tracing integrations expect Node-compatible APIs and environment access.

Optionally enable LangSmith tracing by adding the variables from [`.env.example`](https://github.com/langchain-ai/deployment-cookbook/blob/main/js-sveltekit/.env.example) as Worker secrets or vars.

## Required API endpoints

The app exposes the Agent Streaming Protocol under `/api/threads/...`. SvelteKit route handlers live in `src/routes/api/threads/`.

### Minimum (streaming chat)

| Method | Path | Purpose |
| - | - | - |
| `POST` | `/api/threads/:threadId/commands` | Accept protocol commands (`run.start`, …) and start agent runs |
| `POST` | `/api/threads/:threadId/stream` | SSE stream of protocol events for a run |
| `GET` / `POST` | `/api/threads/:threadId/state` | Read and bootstrap checkpointed thread state |

### Optional (sidebar)

| Method | Path | Purpose |
| - | - | - |
| `GET` | `/api/threads` | List threads known to the checkpointer |
| `DELETE` | `/api/threads/:threadId` | Delete a thread's session and checkpoints |
| `POST` | `/api/threads/:threadId/history` | Paginated checkpoint history |

## Cloudflare backend design

| Concern | Implementation |
| - | - |
| Frontend | SvelteKit client routes and components |
| API layer | SvelteKit server endpoints in `src/routes/api/threads/` |
| Runtime | Workers V8 + `nodejs_compat` |
| SSE replay | Per-thread Durable Object (`ThreadSession`) |
| Agent runs | Worker isolate; protocol events POSTed to the DO |
| Static assets | Workers Static Assets via `adapter-cloudflare` |
| Secrets | `wrangler secret` / local `.env` |

## Production persistence

Out of the box, the agent uses an in-memory `MemorySaver` checkpointer (`src/lib/server/agent/index.ts`). The per-thread SSE replay/session log lives in a [Durable Object](https://developers.cloudflare.com/durable-objects/) so streaming clients reconnect to one coordination point instead of a process-local map.

The checkpointer is still isolate-local demo state. Cloudflare isolates are ephemeral and may scale horizontally, so checkpointed conversation state is **not durable** across deploys, cold starts, or isolates.

For production:

1. Swap in a durable checkpointer (for example [Postgres via Hyperdrive](https://developers.cloudflare.com/hyperdrive/examples/connect-to-postgres/), or a [custom Durable Object-backed store](https://developers.cloudflare.com/agents/model-context-protocol/apis/client-api/#custom-storage-backend)).
2. Persist long-lived replay/history if clients need to reconnect after the Durable Object has been evicted from memory.

## Local development

```bash
cp .env.example .env   # set OPENAI_API_KEY
pnpm install
pnpm dev
```

Open [http://localhost:5173](http://localhost:5173).

```bash
pnpm build      # production build for Cloudflare
pnpm preview    # preview the production build locally
pnpm typecheck  # svelte-check over the project
```

For Cloudflare-style local testing after a build, run:

```bash
npx wrangler dev .svelte-kit/cloudflare/_worker.js
```

## Project layout

> [accordion] Project structure
>
> * `src/lib/server/agent/` — deep agent (`createDeepAgent`) with `researcher` and `math-whiz` subagents and mock tools.
> * `src/lib/server/durable-objects/thread-session.ts` — per-thread Durable Object event log for SSE replay.
> * `src/lib/server/protocol/` — Agent Streaming Protocol helpers: checkpointer-backed state/history, run publishing, serialization, and registry.
> * `src/routes/api/threads/` — SvelteKit route handlers for the protocol endpoints.
> * `src/lib/chat/threads-client.ts` — browser thread bootstrap and sidebar helpers.
> * `src/lib/components/` — Svelte chat UI using `@langchain/svelte`.
> * `svelte.config.js` — SvelteKit configured with `@sveltejs/adapter-cloudflare`.
> * `scripts/export-durable-objects.mjs` — postbuild patch that re-exports the Durable Object class from the generated Worker entry.
> * `wrangler.jsonc` — Cloudflare Workers Static Assets and Durable Object config.

## See also

* [Frameworks and platforms overview](Deploy%20full-stack%20web%20apps.md)
* [SvelteKit Cloudflare adapter](https://svelte.dev/docs/kit/adapter-cloudflare)
* [Agent Streaming Protocol](https://github.com/langchain-ai/agent-protocol/tree/main/streaming)
* [`@langchain/svelte`](https://reference.langchain.com/javascript/langchain-svelte/getting-started)
