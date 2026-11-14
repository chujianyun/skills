# Managed Deep Agents quickstart

> Create and deploy your first Managed Deep Agent with the mda CLI.

Create and deploy your first Managed Deep Agent: scaffold a project, configure the model and instructions, add search, test in [LangSmith Studio](../../../../Test/Test%20from%20Studio/LangSmith%20Studio.md), and deploy with the [`mda` CLI](../Build%20and%20deploy/Managed%20Deep%20Agents%20CLI%20reference.md). Managed Deep Agents supplies the [Deep Agents harness](https://docs.langchain.com/oss/python/deepagents/overview.md) and hosted runtime.

After this quickstart, the [tutorial](../Build%20and%20deploy/Add%20a%20custom%20search%20tool%2C%20memory%2C%20and%20a%20schedule.md) adds durable memory and a daily schedule on the same project.

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

## Prerequisites

To follow along, you need:

* Python and `uv`.

* An API key for your model provider of choice.

## Add the `managed-deep-agents` skill

The [`managed-deep-agents` skill](https://github.com/langchain-ai/langchain-skills/blob/main/config/skills/managed-deep-agents/SKILL.md) walks a coding agent through building, testing, and deploying a Managed Deep Agent with the `mda` CLI. To add it to the current project, run:

```bash
npx skills add langchain-ai/langchain-skills --skill managed-deep-agents --yes
```

Or paste this prompt into your coding agent:

Build a Managed Deep Agent with the quickstart

Create and deploy a Managed Deep Agent in this working directory by following the Managed Deep Agents quickstart.

## Step 1: Read the guide

Fetch and follow [https://docs.langchain.com/langsmith/managed-deep-agents-quickstart.md](Managed%20Deep%20Agents%20quickstart.md) as the source of truth for CLI commands, project layout, and deployment steps. Prefer the Python or TypeScript path that matches this project.

## Step 2: Install the skill

If the `managed-deep-agents` skill is not already available, install it:

```bash
npx skills add langchain-ai/langchain-skills --skill managed-deep-agents --yes
```

Use that skill for the rest of the workflow when it is available.

## Step 3: Prerequisites and secrets

Confirm the user has LangSmith access and any required model or search credentials. If a required API key is missing, ask them to set it in the shell or a `.env` file, then wait. Do not invent, hardcode, or commit secrets.

## Step 4: Scaffold, configure, test, and deploy

Follow the quickstart steps in order: initialize the project with `mda`, configure the model and instructions, add search as shown on the page, test in LangSmith Studio, and deploy with the `mda` CLI. Stop and ask when a dashboard action or credential can only be completed by the user in the LangSmith UI.

## Rules

* Stay scoped to the quickstart. Do not add unrelated products or rewrite the generated project layout unless the guide requires it.
* Prefer the `mda` CLI and the `managed-deep-agents` skill over inventing a custom deployment path.
* Ask rather than guess when a secret, plan-tier limit, or UI-only step is unclear.

## Create and deploy an agent

**1. Set up the project**

Create a project and open its directory:

```bash
uvx --from managed-deepagents mda init research-assistant
cd research-assistant
```

You now have all the scaffolding for your agent.

**2. Add your keys**

Add your model provider API key to `.env`:

```text .env
OPENAI_API_KEY=<OPENAI_API_KEY>
# ANTHROPIC_API_KEY=<ANTHROPIC_API_KEY>
# GOOGLE_API_KEY=<GOOGLE_API_KEY>
# AZURE_AI_OPENAI_ENDPOINT=https://<resource>.services.ai.azure.com/openai/v1
# AZURE_OPENAI_API_KEY=<AZURE_OPENAI_API_KEY>
# AZURE_OPENAI_DEPLOYMENT_NAME=<AZURE_OPENAI_DEPLOYMENT_NAME>
```

This quickstart uses OpenAI by default. For Google, Anthropic, or Microsoft Foundry, set the matching values instead. `mda deploy` adds the provider key to the deployment. You can also use any [other chat provider](https://docs.langchain.com/oss/python/integrations/chat.md).

> [!WARNING]
>
> Do not commit the `.env` file into version control. It contains secrets.

**3. Set up LangSmith**

Managed Deep Agents runs on LangSmith. Your LangSmith API key authenticates local development with `mda dev`, deploys the agent with `mda deploy`, and opens the agent in [LangSmith Studio](../../../../Test/Test%20from%20Studio/LangSmith%20Studio.md) so you can chat with it and inspect traces.

[Sign up for LangSmith](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-managed-deep-agents-quickstart) if you do not already have an account.

To create a LangSmith API key, open [Settings](https://smith.langchain.com/settings), go to **API Keys**, and click **Create API Key**. For more details, see [Create an account and API key](../../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md).

On [BYOC](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md), sign in to your own data plane and create the key there. Set `LANGSMITH_ENDPOINT` to the data plane's API URL as well. See [Select a BYOC data plane](../Build%20and%20deploy/Deploy%20a%20Managed%20Deep%20Agent.md#select-a-byoc-data-plane).

Add your LangSmith API key to `.env`:

```text .env
LANGSMITH_API_KEY=<LANGSMITH_API_KEY>
```

**4. Edit the instructions**

Open `instructions.md` and describe how the agent should behave:

```markdown instructions.md
# Research assistant

You are a careful research assistant. Use internet search to find sources,
keep notes, and return concise answers with citations.
```

When you deploy, Managed Deep Agents syncs these instructions to [LangSmith Context Hub](../Build%20and%20deploy/Manage%20Context%20Hub%20for%20Managed%20Deep%20Agents.md), where you can update them without redeploying the agent.

**5. Configure your model and search**

Now set the model and a built-in web search tool. Google, OpenAI, Anthropic, and Microsoft Foundry offer server-side search without a separate search package or search API key. Pass the provider tool dict that matches your model:

Open `agent.py`:

```python OpenAI
from managed_deepagents import define_deep_agent

# OpenAI's built-in web search — no extra install or API key needed
agent = define_deep_agent(
    name="research-assistant",
    model="openai:gpt-6.1-sol",
    tools=[{"type": "web_search"}],
)
```

```python Google
from managed_deepagents import define_deep_agent

# Google's built-in search — no extra install or API key needed
agent = define_deep_agent(
    name="research-assistant",
    model="google_genai:gemini-4-hydrogen",
    tools=[{"google_search": {}}],
)
```

```python Anthropic
from managed_deepagents import define_deep_agent

# Anthropic's built-in web search — no extra install or API key needed
agent = define_deep_agent(
    name="research-assistant",
    model="anthropic:claude-sonnet-4-6",
    tools=[{"type": "web_search_20260209", "name": "web_search"}],
)
```

```python Microsoft Foundry
# Install the required dependency: uv add langchain-azure-ai
import os

from langchain_azure_ai.chat_models import AzureAIOpenAIApiChatModel
from managed_deepagents import define_deep_agent

model = AzureAIOpenAIApiChatModel(
    endpoint=os.environ["AZURE_AI_OPENAI_ENDPOINT"],
    credential=os.environ["AZURE_OPENAI_API_KEY"],
    model=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)

agent = define_deep_agent(
    name="research-assistant",
    model=model,
    tools=[{"type": "web_search"}],
)
```

The agent name is also the default deployment name. For model concepts and provider options, see [Models](https://docs.langchain.com/oss/python/langchain/models.md).

> [accordion] Using another provider?
>
> You can use a Tavily search tool instead. Store the key in a [connection](../Agent%20capabilities/Manage%20connections.md) so it lives in your LangSmith workspace rather than the project.
>
> This accordion uses the connection slug `research-tavily`. For `mda dev`, an agent-owned connection reads its value from `MDA_DEV_<SLUG>`. Add a [Tavily API key](https://app.tavily.com) to `.env` as `MDA_DEV_RESEARCH_TAVILY`:
>
> ```text .env theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> MDA_DEV_RESEARCH_TAVILY=<TAVILY_API_KEY>
> ```
>
> Install the Tavily client:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> uv add tavily-python
> ```
>
> Create a custom `internet_search` tool. `connections.get(...)` resolves the key at runtime, so the tool code is the same locally and on the deployment:
>
> ```python tools/search.py theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from typing import Literal
>
> from langchain.tools import tool
> from managed_deepagents import connections
> from tavily import AsyncTavilyClient
>
>
> @tool
> async def internet_search(
>     query: str,
>     max_results: int = 5,
>     topic: Literal["general", "news", "finance"] = "general",
> ) -> dict:
>     """Search the internet for relevant sources."""
>     api_key = await connections.get("research-tavily", {"type": "agent"})
>     tavily_client = AsyncTavilyClient(api_key=api_key)
>     return await tavily_client.search(
>         query,
>         max_results=max_results,
>         topic=topic,
>     )
> ```
>
> Import the tool and add it to the agent:
>
> ```python agent.py theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from managed_deepagents import define_deep_agent
>
> from tools.search import internet_search
>
> agent = define_deep_agent(
>     name="research-assistant",
>     model="openai:gpt-6.1-sol",
>     tools=[internet_search],
> )
> ```
>
> After you deploy in the agent in the next step, create the agent-owned connection. Agent-owned credentials belong to the deployment, so this command comes after the first successful deploy:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> uv run mda connections create research-tavily --secret-from-env MDA_DEV_RESEARCH_TAVILY
> ```
>
> Rotating this value later takes effect on the next run, with no redeploy. For more authored tools, see [Custom tools](../Agent%20capabilities/Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md). For other create modes and per-caller credentials, see [Manage connections](../Agent%20capabilities/Manage%20connections.md).

**6. Run locally**

Install the project dependencies and start the agent:

```bash
uv sync
uv run mda dev
```

`mda dev` loads the API keys from `.env`, starts a local Agent Server, and opens the agent in LangSmith Studio.

In Studio, send:

```txt wrap
What were the main announcements from the latest LangChain release?
```

You should see the agent call the web search tool, then return a concise answer that cites sources. If search never appears in the trace, confirm the provider tool dict matches the model you set in `agent.py` or `agent.ts`.

In an [agent-based workspace](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), tracing will result in errors until you register the agent. For details, see [Trace local runs](../Build%20and%20deploy/Develop%20locally%20with%20LangSmith%20Studio.md#trace-local-runs).

**7. Deploy the agent**

On [BYOC](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md), add `--push-to <image-repository>` to every command in this step. A BYOC data plane deploys from an image in a registry you manage.

Deploy the project by running:

```bash
uv run mda deploy
```

Managed Deep Agents packages the project and runs it as a hosted deployment on [LangSmith Agent Server](../../../../Deploy/Agent%20Server/Capabilities/Agent%20Server.md). When deployment finishes, the CLI prints the deployment dashboard URL.

Open that URL. You should see the deployment in a ready state. Send the same research question from the previous step and confirm the hosted agent returns an answer with a search tool call. For deployment options and secrets handling, see [Deploy a Managed Deep Agent](../Build%20and%20deploy/Deploy%20a%20Managed%20Deep%20Agent.md). To inspect the agent's execution after it runs, use [LangSmith observability](../../../../Monitor/Trace/Tracing%20quickstart.md).

## Next steps

> [card] [Tutorial](../Build%20and%20deploy/Add%20a%20custom%20search%20tool%2C%20memory%2C%20and%20a%20schedule.md)
>
> Add a custom Tavily search tool, durable memory, and a daily schedule.

> [card] [Design agent template](../Templates/Deploy%20the%20open-source%20design%20agent.md)
>
> Deploy LangChain's open-source design agent instead of scaffolding from scratch.

> [card] [Paid media agent template](../Templates/Deploy%20the%20open-source%20paid%20media%20agent.md)
>
> Deploy LangChain's open-source paid media agent for Slack campaign analysis.

> [card] [Custom tools](../Agent%20capabilities/Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md)
>
> Add authored LangChain tools from your project.

> [card] [Connections](../Agent%20capabilities/Manage%20connections.md)
>
> Authenticate with external services, as the agent or as the caller.
