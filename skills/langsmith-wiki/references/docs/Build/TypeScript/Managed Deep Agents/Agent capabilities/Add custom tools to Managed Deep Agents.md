# Add custom tools to Managed Deep Agents

> Define authored tools for managed deep agents projects.

Custom tools are application code the agent can call for fetching real-time data, querying databases, executing code, and taking actions. Unlike [instructions](Add%20instructions%20to%20Managed%20Deep%20Agents.md) and [skills](Add%20skills%20to%20Managed%20Deep%20Agents.md), MDA does not discover them automatically.

To load tools from a remote MCP server, see [Connect to MCP servers](Connect%20to%20MCP%20servers.md).

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

Put authored tools under `tools/`, import them into the agent entry, and pass them to the agent definition:

```text
my-agent/
  agent.ts
  tools/
    customer.ts
```

For the full project layout, see [Project structure](../Get%20started/Managed%20Deep%20Agents%20project%20structure.md).

To load tools from a remote MCP server without importing them into the agent entry, use an [MCP connector](Connect%20to%20MCP%20servers.md) instead.

MCP connectors are declared under `tools/` as well, so the `tools/mcp.ts` file name is reserved for that declaration.

## Add a tool

Use authored tools for business logic, private APIs, database access, and other code that belongs in your agent project.

**1. Define a tool module**

```ts tools/customer.ts
import { tool } from "langchain";
import { z } from "zod";

export const lookupCustomer = tool(
  async ({ customerId }) => `Customer ${customerId} is on the enterprise plan.`,
  {
    name: "lookup_customer",
    description: "Look up a customer record by ID.",
    schema: z.object({
      customerId: z.string().describe("Customer ID from the CRM."),
    }),
  },
);
```

Use clear, unique tool names to avoid collisions. For more about LangChain tool definitions, see [Tools](https://docs.langchain.com/oss/javascript/langchain/tools.md).

**2. Attach the tool to the agent**

Import the tool into the project-root agent entry and pass it in the `tools` list:

```ts agent.ts
import { defineDeepAgent } from "managed-deepagents";

import { lookupCustomer } from "./tools/customer";

export const agent = defineDeepAgent({
  name: "support-agent",
  model: "openai:gpt-6.1-sol",
  tools: [lookupCustomer],
});
```

Your imports should work the same way they do in a normal local TypeScript project.

**3. Add human-in-the-loop (Optional)**

Pause the agent before sensitive tool calls so a person can approve, edit, or reject them.

Set `interruptOn` in the agent definition, and optionally set `permissions` to gate tool and filesystem access:

```ts agent.ts
import { defineDeepAgent } from "managed-deepagents";

import { lookupCustomer } from "./tools/customer";

export const agent = defineDeepAgent({
  name: "support-agent",
  model: "openai:gpt-6.1-sol",
  tools: [lookupCustomer],
  interruptOn: {
    lookup_customer: true,
  },
});
```

The `interruptOn` field applies the same interrupt behavior as LangChain's [human-in-the-loop middleware](https://docs.langchain.com/oss/javascript/langchain/guardrails.md#human-in-the-loop).

For decision types (approve, edit, reject), conditional interrupts, and permission rules, see the Deep Agents [Human-in-the-loop](https://docs.langchain.com/oss/javascript/deepagents/human-in-the-loop.md) and [Permissions](https://docs.langchain.com/oss/javascript/deepagents/permissions.md) guides.

To resume a paused run, see [Respond to an interrupt](#respond-to-an-interrupt).

To pause on a form your own tool posts in Slack instead, see [Agent-owned interrupts](Channels/Prompt%20Slack%20users%20with%20agent-owned%20interrupts.md).

For a full project that pauses campaign changes for Slack approval, see the [paid media agent template](../Templates/Deploy%20the%20open-source%20paid%20media%20agent.md).

## Use secrets and context

A tool reads fixed configuration, such as a region or an endpoint URL, from an environment variable. Put local values in `.env` for `mda dev`. `mda deploy` forwards non-reserved `.env` values as hosted deployment secrets.

Credentials belong in a [connection](Manage%20connections.md) instead. A connection keeps the value in your LangSmith workspace rather than the project. It can also resolve a different credential for each caller. See [Use tools that require authentication](#use-tools-that-require-authentication).

For per-run values such as request metadata or feature flags, see [Access runtime context](#access-runtime-context).

## Deployment

`mda dev` and `mda deploy` copy project files into the compiled build, including modules under `tools/`. Tools are not synced to Context Hub; they ship with the agent code.

## When to use tools

| Concept | Kind | How it reaches the agent |
| - | - | - |
| **Tools** | Application code | Import and pass in the agent definition |
| **[MCP connectors](Connect%20to%20MCP%20servers.md)** | Managed configuration | Declared in the MCP module under `tools/`; no import into the agent entry |
| **[Skills](Add%20skills%20to%20Managed%20Deep%20Agents.md)** | Managed context | Procedures the agent loads when relevant |
| **[Instructions](Add%20instructions%20to%20Managed%20Deep%20Agents.md)** | Managed context | Always-on system prompt |

For more information, see [Project structure](../Get%20started/Managed%20Deep%20Agents%20project%20structure.md).

## Respond to an interrupt

When a run hits an interrupt, it pauses and waits for a human response before continuing.

* **During local development**, `mda dev` runs the agent in LangSmith Studio, which surfaces the interrupt so you can inspect the pending tool call and resume the run.

* **On a deployed agent**, resume the paused run through the Agent Server API with a resume payload. See [Human-in-the-loop using server API](../../../../Deploy/Agent%20Server/Capabilities/Human-in-the-loop%20using%20server%20API.md).

Human-in-the-loop needs durable thread state to pause and resume. The managed runtime owns the checkpointer, so no extra setup is required.

## Use tools that require authentication

If a tool requires an API key or an OAuth token, resolve it at runtime with a [connection](Manage%20connections.md). `connections.get(...)` takes the connection slug and the credential owner, and returns the credential as a string.

The second argument selects the owner. Pass `{"type": "agent"}` for one credential that the whole deployment shares, such as a team search key. Pass `{"type": "user"}` for the calling person's own credential, so the agent acts as them. For more information, see [Choose a credential owner](Manage%20connections.md#choose-a-credential-owner).

This tool resolves the caller's own GitHub credential:

```ts tools/get-github-user.ts
import { tool } from "langchain";
import { connections } from "managed-deepagents";
import { z } from "zod";

export const getGitHubUser = tool(
  async () => {
    // Replace `frontend-github` with the name of your connection.
    const accessToken = await connections.get("frontend-github", { type: "user" });
    const response = await fetch("https://api.github.com/user", {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });
    if (!response.ok) {
      throw new Error(`GitHub request failed with status ${response.status}`);
    }
    const user = (await response.json()) as { login: string };
    return user.login;
  },
  {
    name: "get_github_user",
    description: "Get the authenticated caller's GitHub login.",
    schema: z.object({}),
  },
);
```

A user-owned connection needs a grant from each caller. The first run for someone who has not authorized the service pauses on a [`credential_authorization_required` interrupt](Manage%20connections.md#handle-the-authorization-interrupt). Slack and LangSmith Studio complete that interrupt for the caller.

Create the connection itself with `mda connections create`. For create modes, local development, and the authorization interrupt, see [Manage connections](Manage%20connections.md).

## Access runtime context

For per-run values such as request metadata or feature flags, use the normal LangChain runtime context patterns for tools. See [how to access context from within your tools](https://docs.langchain.com/oss/javascript/langchain/tools.md#access-context).

For the caller, channel, and sandbox fields that Managed Deep Agents adds, see [Runtime](Managed%20Deep%20Agents%20runtime.md).

To read or write files in the thread's sandbox from a tool, use `runtime.backend`. See [Read and write sandbox files from code](Add%20a%20sandbox%20to%20Managed%20Deep%20Agents.md#read-and-write-sandbox-files-from-code).
