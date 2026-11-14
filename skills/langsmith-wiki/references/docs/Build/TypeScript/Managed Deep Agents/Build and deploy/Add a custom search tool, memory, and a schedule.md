# Add a custom search tool, memory, and a schedule

> Replace provider search with a Tavily tool, then add durable memory and a daily schedule to the research assistant from the quickstart.

This tutorial continues from the [quickstart](../Get%20started/Managed%20Deep%20Agents%20quickstart.md). Use the `research-assistant` project you created there, with your model, instructions, and a working `mda dev` setup.

`mda init` may also scaffold files such as `identity` and `sandbox/`. Leave those as they are; this tutorial does not change them.

This guide replaces the quickstart's built-in provider search with an authored [Tavily](https://tavily.com) search tool, enables durable memory, adds a daily schedule, then deploys.

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

## Extend the agent

**1. Add a custom search tool**

Built-in provider search is convenient for a first run. Authored tools give you more control: choose the search API, tune parameters, and keep the tool code in your project.

> [!NOTE]
>
> If you already added the Tavily tool with a [connection](../Agent%20capabilities/Manage%20connections.md) in the [quickstart](../Get%20started/Managed%20Deep%20Agents%20quickstart.md), skip to the next step.

This tutorial uses the connection slug `research-tavily`. For `mda dev`, an agent-owned connection reads its value from `MDA_DEV_<SLUG>`. Add a [Tavily API key](https://app.tavily.com) to `.env` as `MDA_DEV_RESEARCH_TAVILY`:

```text .env
MDA_DEV_RESEARCH_TAVILY=<TAVILY_API_KEY>
```

Install the Tavily client:

```bash npm
npm install @langchain/tavily
```

```bash pnpm
pnpm add @langchain/tavily
```

```bash bun
bun add @langchain/tavily
```

Create a custom `internet_search` tool. `connections.get(...)` resolves the key at runtime, so the tool code is the same locally and on the deployment:

```ts tools/search.ts
import { TavilySearch } from "@langchain/tavily";
import { tool } from "langchain";
import { connections } from "managed-deepagents";
import { z } from "zod";

export const internetSearch = tool(
  async ({ query, maxResults = 5, topic = "general" }) => {
    const tavilyApiKey = await connections.get("research-tavily", { type: "agent" });
    const tavilySearch = new TavilySearch({
      maxResults,
      tavilyApiKey,
      topic,
    });
    return tavilySearch._call({ query });
  },
  {
    name: "internet_search",
    description: "Search the internet for relevant sources.",
    schema: z.object({
      query: z.string().describe("The search query."),
      maxResults: z.number().optional().default(5),
      topic: z.enum(["general", "news", "finance"]).optional().default("general"),
    }),
  },
);
```

Replace the provider search tool dict with your authored tool. Keep the `model` value from the quickstart:

```ts agent.ts
import { defineDeepAgent } from "managed-deepagents";

import { internetSearch } from "./tools/search";

export const agent = defineDeepAgent({
  name: "research-assistant",
  model: "openai:gpt-6.1-sol",
  tools: [internetSearch],
});
```

Restart `mda dev` if it is already running. In Studio, ask:

```txt wrap
What were the main announcements from the latest LangChain release?
```

Confirm the agent calls `internet_search` and returns an answer with citations. For more authored tools, see [Custom tools](../Agent%20capabilities/Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md).

**2. Update the instructions for memory**

Extend `instructions.md` so the agent knows what shared knowledge to keep. Keep the research behavior and add a memory policy:

```markdown instructions.md
# Research assistant

You are a careful research assistant. Use internet search to find sources,
keep notes, and return concise answers with citations.

## Memory

- Record reusable research procedures and project knowledge that can improve future work.
- For release research, check the project's official changelog before secondary sources.
- Never store personal data or secrets in memory.
```

**3. Enable and use durable memory**

Durable memory is opt-in. Before asking the agent to remember anything, add a memory declaration at the project root:

```ts memory.ts
import { defineMemory, memoryLayer } from "managed-deepagents";

export const memory = defineMemory({ agent: memoryLayer() });
```

Memory is shared across the deployment and visible to all callers, so do not store personal data or secrets.

Restart `mda dev` so it discovers the new file. In one thread, ask the agent to research a release and to record a reusable project rule, such as "For release research, check the official changelog before secondary sources." Then create a **new thread** in Studio and ask how it will research the next release. Confirm that it applies the shared rule even though the new thread has no conversation history.

See [Memory](../Agent%20capabilities/Add%20memory%20to%20Managed%20Deep%20Agents.md) for details.

**4. Schedule a daily digest**

Add a `schedules/` module so the agent runs on a cron cadence without a user message. This schedule runs every weekday at 8am Pacific:

```ts schedules/daily-digest.ts
import { defineSchedule } from "managed-deepagents";

export const schedule = defineSchedule({
  cron: "0 8 * * 1-5",
  timezone: "America/Los_Angeles",
  prompt:
    "Review durable memory for reusable research rules. " +
    "Summarize anything useful, then list open questions for today.",
});
```

If memory is empty on the first fire, the agent still returns open questions.

`mda deploy` reconciles this schedule into a LangSmith cron job after the deployment is live. After you deploy in the next step, you should see:

* `mda deploy` finish without schedule errors (do not pass `--no-wait`, or schedules are not reconciled).
* A managed cron for this file on the deployment. The schedule name matches the module stem: `daily_digest` (Python) or `daily-digest` (TypeScript).
* No immediate digest run from this cron. The first fire waits until 8:00 America/Los\_Angeles on a weekday.

For thread behavior and constraints, see [Schedules](../Agent%20capabilities/Add%20schedules%20to%20Managed%20Deep%20Agents.md).

**5. Deploy and inspect**

Deploy the project to LangSmith:

```bash npm
npx mda deploy
```

```bash pnpm
pnpm exec mda deploy
```

```bash bun
bunx mda deploy
```

On success, the CLI prints the deployment dashboard URL. The deploy syncs the instructions to Context Hub, uploads the compiled project, and reconciles the daily schedule.

Create the Tavily connection for this deployment. Agent-owned credentials belong to the deployment. Run this command after the first successful deploy:

```bash npm
npx mda connections create research-tavily --secret-from-env MDA_DEV_RESEARCH_TAVILY
```

```bash pnpm
pnpm exec mda connections create research-tavily --secret-from-env MDA_DEV_RESEARCH_TAVILY
```

```bash bun
bunx mda connections create research-tavily --secret-from-env MDA_DEV_RESEARCH_TAVILY
```

Rotating this value later takes effect on the next run, with no redeploy. For other create modes and per-caller credentials, see [Manage connections](../Agent%20capabilities/Manage%20connections.md).

Open that URL and confirm:

* The deployment is ready.
* The `daily_digest` or `daily-digest` cron exists.
* A test chat run shows model calls, `internet_search` tool calls, and memory reads or writes in the traces.

For deploy flags and troubleshooting, see [Deploy an agent](Deploy%20a%20Managed%20Deep%20Agent.md) and the [CLI reference](Managed%20Deep%20Agents%20CLI%20reference.md#deploy-projects).

## Next steps

> [card] [Custom middleware](../Agent%20capabilities/Add%20custom%20middleware%20to%20Managed%20Deep%20Agents.md)
>
> Add logging, retries, limits, and guardrails around model and tool calls.

> [card] [Identity](../Agent%20capabilities/Add%20identity%20to%20Managed%20Deep%20Agents.md)
>
> Authenticate callers and use verified identity in tools and middleware.

> [card] [Evals](../Agent%20capabilities/Evaluate%20Managed%20Deep%20Agents.md)
>
> Develop Harbor evals with a coding agent and the eval-engineering skill.
