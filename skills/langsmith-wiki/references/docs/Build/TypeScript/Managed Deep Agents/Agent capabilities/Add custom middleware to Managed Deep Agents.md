# Add custom middleware to Managed Deep Agents

> Add built-in or custom middleware to a managed deep agent.

Middleware adds behavior around model calls, tool calls, and the agent lifecycle. Like [custom tools](Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md), MDA does not discover middleware automatically. Import it and pass it to the agent definition.

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

Put custom middleware under `middleware/`, import it into the agent entry, and pass it to the agent definition:

```text
my-agent/
  agent.ts
  middleware/
    audit.ts
```

For the full project layout, see [Project structure](../Get%20started/Managed%20Deep%20Agents%20project%20structure.md).

The managed runtime still owns `backend`, `store`, `checkpointer`, `memory`, `skills`, and the system prompt. Middleware should focus on agent behavior around model calls, tool calls, and lifecycle hooks.

## Add middleware

Use middleware to redact PII, enforce call limits, retry failures, fall back between models, select models dynamically, or log and inspect tool calls.

**1. Use prebuilt middleware**

You can use LangChain [prebuilt middleware](https://docs.langchain.com/oss/javascript/langchain/middleware/built-in.md) directly in the agent definition:

```ts agent.ts
import { defineDeepAgent } from "managed-deepagents";
import { modelCallLimitMiddleware, piiMiddleware } from "langchain";

export const agent = defineDeepAgent({
  name: "support-agent",
  model: "openai:gpt-6.1-sol",
  middleware: [
    piiMiddleware("email", { strategy: "redact", applyToInput: true }),
    modelCallLimitMiddleware({ runLimit: 50 }),
  ],
});
```

**2. Define custom middleware (Optional)**

For a more advanced option, define [custom middleware](https://docs.langchain.com/oss/javascript/langchain/middleware/custom.md) in a local module.

```ts middleware/audit.ts
import { createMiddleware } from "langchain";

export const logToolCalls = createMiddleware({
  name: "LogToolCalls",
  wrapToolCall: async (request, handler) => {
    console.log(`Calling tool: ${request.toolCall.name}`);
    const result = await handler(request);
    console.log(`Finished tool: ${request.toolCall.name}`);
    return result;
  },
});
```

Import the middleware into the project-root agent entry and pass it in the `middleware` list:

```ts agent.ts
import { defineDeepAgent } from "managed-deepagents";

import { logToolCalls } from "./middleware/audit";

export const agent = defineDeepAgent({
  name: "support-agent",
  model: "openai:gpt-6.1-sol",
  middleware: [logToolCalls],
});
```

Your middleware imports should work the same way they do in a normal local TypeScript project.

## Use runtime context

Middleware can read per-run context through the normal LangChain runtime APIs. Use context for user IDs, organization IDs, feature flags, request metadata, or credentials that should not be part of the model prompt by default.

For examples, see [Custom middleware](https://docs.langchain.com/oss/javascript/langchain/middleware/custom.md).

For the caller, channel, and sandbox fields that Managed Deep Agents adds, see [Runtime](Managed%20Deep%20Agents%20runtime.md).

To read or write files in the thread's sandbox from a middleware hook, use `runtime.backend`. See [Read and write sandbox files from code](Add%20a%20sandbox%20to%20Managed%20Deep%20Agents.md#read-and-write-sandbox-files-from-code).

## Deployment

`mda dev` and `mda deploy` copy project files into the compiled build, including modules under `middleware/`. Middleware is not synced to Context Hub; it ships with the agent code.

## When to use middleware

| Concept | Kind | How it reaches the agent |
| - | - | - |
| **Middleware** | Application code | Import and pass in the agent definition |
| **[Custom tools](Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md)** | Application code | Import and pass in the agent definition |
| **[Instructions](Add%20instructions%20to%20Managed%20Deep%20Agents.md)** | Managed context | Always-on system prompt |

For more information, see [Project structure](../Get%20started/Managed%20Deep%20Agents%20project%20structure.md).
