# Define a Managed Deep Agent

> Configure the model and core capabilities of a managed deep agent.

The agent definition selects the model and core capabilities of a managed deep agent.

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

The agent entry lives at the project root:

```text
my-agent/
  agent.py
```

For the full project layout, see [Project structure](../Get%20started/Managed%20Deep%20Agents%20project%20structure.md).

To define the agent, use `define_deep_agent`:

```python OpenAI
from managed_deepagents import define_deep_agent

agent = define_deep_agent(
    name="research-assistant",
    model="openai:gpt-6.1-sol",
)
```

```python Anthropic
from managed_deepagents import define_deep_agent

agent = define_deep_agent(
    name="research-assistant",
    model="anthropic:claude-sonnet-4-6",
)
```

```python Google Gemini
from managed_deepagents import define_deep_agent

agent = define_deep_agent(
    name="research-assistant",
    model="google_genai:gemini-4-hydrogen",
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
)
```

Configure the system prompt, skills, memory, sandbox, identity, channels, and schedules through their project files rather than the agent definition. See [Project structure](../Get%20started/Managed%20Deep%20Agents%20project%20structure.md). To select the system prompt, skills, MCP servers, memory, or sandbox for each run, see [Select configuration per run](#select-configuration-per-run).

`define_deep_agent` does not compile an agent. It returns a definition, and the managed runtime compiles it with [create\_deep\_agent](https://reference.langchain.com/python/deepagents/graph/create_deep_agent) at deploy time. The parameters below are the [create\_deep\_agent](https://reference.langchain.com/python/deepagents/graph/create_deep_agent) surface without the ones the runtime owns. See [Relationship to Deep Agents](../../Deep%20Agents/Deployment/Managed%20Deep%20Agents.md#relationship-to-deep-agents).

## Parameters

| Parameter | What it does |
| - | - |
| `name=` | Required. Pass a static string that starts with a letter and contains only letters, numbers, underscores, or hyphens, such as `"research-assistant"`.  Managed Deep Agents uses the name as the agent's graph ID and the default LangSmith deployment name, and clients pass it as `assistant_id` when they call the deployment. You can override the deployment name with `mda deploy --name` without changing the agent definition. |
| `model=` | Set the chat model the agent uses. The simplest option is a `provider:model` string. Add the provider's API key to `.env` so the model works locally and in the deployment.  Pass a LangChain chat model instance instead when you need to configure model parameters in code. For model options and supported providers, see [Models](https://docs.langchain.com/oss/python/deepagents/models.md).  To connect to LLM Gateway, see [Use LLM Gateway](#use-llm-gateway). |
| `tools=` | Adds tools the agent can call. Pass tools in the `tools` list so the agent can call application logic or external services.  Define tools in local modules, import them into the agent entry, and add them to the definition. See [Custom tools](Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md). To add tools from remote MCP servers without importing them into the agent entry, use [MCP connectors](Connect%20to%20MCP%20servers.md). |
| `middleware=` | Adds behavior around model calls, tool calls, and the agent lifecycle. Pass middleware in the `middleware` list. Middleware runs in list order. See [Custom middleware](Add%20custom%20middleware%20to%20Managed%20Deep%20Agents.md). |
| `subagents=` | Defines specialized agents for delegated tasks. Pass subagent definitions when the agent should delegate specialized or context-heavy work. Each subagent can have its own prompt, model, and tools. See [Subagents](Subagents.md), including how to run a subagent in the background. |
| `permissions=` | Controls path-level access for filesystem tools. Pass filesystem permission rules to control which paths the agent's built-in filesystem tools can read or write. Cleared when the project declares a [sandbox](Add%20a%20sandbox%20to%20Managed%20Deep%20Agents.md), because a permission rule disables the sandbox `execute` tool. See [Permissions](https://docs.langchain.com/oss/python/deepagents/permissions.md). |
| `interrupt_on=` | Pauses before selected tool calls for human approval. Set `interrupt_on` to pause before selected tool calls, so a person can approve, edit, or reject the call before it runs. See [Human-in-the-loop](Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md#human-in-the-loop). |
| `response_format=` | Set when the agent must return data that matches a schema instead of an unconstrained text response. See [Structured output](https://docs.langchain.com/oss/python/langchain/structured-output.md). |
| `routes=` | Mounts Deep Agents backends at path prefixes. See [Mount your own backends](#mount-your-own-backends). |

## Mount your own backends

`routes` mounts Deep Agents [backends](https://docs.langchain.com/oss/python/deepagents/backends.md) at path prefixes, the same way [`CompositeBackend`](https://docs.langchain.com/oss/python/deepagents/backends#compositebackend-router) routes do. A path under a prefix goes to that backend with the prefix removed. Every other path stays on the managed backend.

> [!NOTE]
>
> `routes` requires `managed-deepagents` 0.10.3 or later.

```python agent.py
from deepagents.backends import StoreBackend
from managed_deepagents import define_deep_agent

agent = define_deep_agent(
    name="research-assistant",
    routes={
        "/documents/": StoreBackend(namespace=lambda _rt: ("documents",)),
    },
)
```

With this route, the agent's file tools read and write `/documents/a.md` as `/a.md` in the store backend.

* Each prefix must be an absolute directory that starts and ends with `/`, such as `"/documents/"`.
* A prefix cannot overlap the paths Managed Deep Agents mounts itself: `/instructions.md`, `/skills/`, and `/memories/`.
* Routes apply to the file tools only. Shell commands in a [sandbox](Add%20a%20sandbox%20to%20Managed%20Deep%20Agents.md) do not see them.

## Select configuration per run

To select the agent's configuration for each run, export a function as `agent` instead of a definition. One deployment can then adapt to different users, tasks, or repositories. The function is a graph factory, the same pattern LangGraph uses to [rebuild a graph at runtime](../../../../Deploy/Agent%20Server/Server%20customization/Rebuild%20graph%20at%20runtime.md): it receives the runtime and returns a definition.

This example selects instructions and skills for the repository a run works on. It assumes the project has `skills/python-service/` and `skills/typescript-web/`, each with a [`SKILL.md`](Add%20skills%20to%20Managed%20Deep%20Agents.md).

```python agent.py
from typing import TypedDict

from managed_deepagents import ManagedServerRuntime, define_deep_agent


class AppContext(TypedDict, total=False):
    repository: str


def agent(runtime: ManagedServerRuntime[AppContext]):
    execution = runtime.execution_runtime
    context = execution.context if execution is not None else None
    python_service = context is not None and context.get("repository") == "payments-service"
    return define_deep_agent(
        name="open-swe",
        model="openai:gpt-6.1-sol",
        instructions=(
            "Follow the payments service's API and reliability conventions."
            if python_service
            else "Follow the storefront's frontend and accessibility conventions."
        ),
        skills=["./skills/python-service" if python_service else "./skills/typescript-web"],
        context_schema=AppContext,
    )
```

The factory can be sync or async. It receives a `ManagedServerRuntime`, which extends the native LangGraph `ServerRuntime`. Read run context from `execution_runtime.context`. It is `None` on channel runs, and `execution_runtime` is `None` when Agent Server loads the agent for inspection.

Callers choose the configuration through the run's `context`:

```python
await client.runs.create(
    thread_id,
    "open-swe",
    input={"messages": [{"role": "user", "content": "Run the service test suite."}]},
    context={"repository": "payments-service"},
)
```

Run context is application data, not verified identity. Check authorization in [tools](Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md) against the verified caller on the runtime.

### Select managed resources

A factory can also select the resources that a static agent reads from project files. Omitting a field keeps the project's configuration. Providing a value replaces it for that run:

| Field | Omitted | Selected | Cleared |
| - | - | - | - |
| `instructions` | Uses `instructions.md`. | Uses the supplied prompt. | `""` removes authored instructions. |
| `skills` | Exposes all project skills. | Exposes only the selected skills. | `[]` exposes no skills. |
| `mcp` | Uses the `mcp` declaration. | Uses only the selected MCP definitions. | `[]` exposes no MCP tools. |
| `sandbox` | Uses the `sandbox` declaration. | Uses the supplied sandbox. | `None` disables the sandbox. |
| `memory` | Uses the `memory` declaration. | Uses the selected layers. | `None` disables durable memory. |
| `browser` | Uses root `browser.py`. | Uses the supplied browser definition. | `None` disables browser tools. |

> [!NOTE]
>
> Browser declarations and per-run selection were added in SDK 0.10. Keep a root `browser.py` even when the factory selects a browser. See [Choose a browser per run](Browser%20use.md#choose-a-browser-per-run) for scope, overrides, and disabling browser tools.

Static definitions cannot set these fields. A skill path must end in `skills/<name>` and point to a skill in the project. A factory can also return generated skill definitions, whose names must not duplicate project skill names.

This example enables the docs MCP server on request and gives one repository a longer sandbox timeout. It imports the declarations from [`tools/mcp`](Connect%20to%20MCP%20servers.md) and [`sandbox/`](Add%20a%20sandbox%20to%20Managed%20Deep%20Agents.md):

```python agent.py
from typing import TypedDict

from managed_deepagents import ManagedServerRuntime, define_deep_agent, define_sandbox

from sandbox import sandbox
from tools.mcp import mcp


class AppContext(TypedDict, total=False):
    repository: str
    needs_docs: bool


def agent(runtime: ManagedServerRuntime[AppContext]):
    execution = runtime.execution_runtime
    context = execution.context if execution is not None else None
    python_service = context is not None and context.get("repository") == "payments-service"
    needs_docs = context is not None and context.get("needs_docs", False)
    return define_deep_agent(
        name="open-swe",
        model="openai:gpt-6.1-sol",
        mcp=[mcp] if needs_docs else [],
        sandbox=define_sandbox(default_timeout=600) if python_service else sandbox,
        context_schema=AppContext,
    )
```

A memory selection overrides the project's memory declaration for that run. User memory still mounts only for an authenticated person. See [Select layers for each run](Add%20memory%20to%20Managed%20Deep%20Agents.md#select-layers-for-each-run).

### Keep the factory repeatable

Managed Deep Agents calls the factory at the start of each run, and again when a run resumes or retries. Agent Server also calls it to read schemas and state. Follow these rules:

* **No side effects**: Return the same definition for the same context. Do not create records, call external APIs, or change shared state in the factory.
* **Stable interrupts**: Keep middleware that can interrupt a run in every configuration. When a run resumes, the middleware that raised the interrupt must still be present.
* **Inline name**: Set `name` as an inline string. `mda build` reads it without calling the factory and uses it as the graph ID and default deployment name.
* **Model dependencies**: Install the integration package for every model the factory can return. The build does not detect them.

To change behavior between model calls within a run, use [custom middleware](Add%20custom%20middleware%20to%20Managed%20Deep%20Agents.md).

### Cache compiled graphs

`cached_agent` keeps the graph that a factory compiles and reuses it on later runs with the same parameters. Without it, a factory compiles a new graph on every run, and each run waits for that compile.

`keyed_by` returns the parameters the graph depends on, as a JSON-serializable value. Managed Deep Agents compiles one graph for each distinct value. The factory gets only these parameters, so read per-run data, such as credentials, in tools or middleware.

> [!NOTE]
>
> `cached_agent` requires `managed-deepagents>=0.10.2`.

```python agent.py
from managed_deepagents import ManagedServerRuntime, cached_agent, define_deep_agent

PROMPTS = {"support": "Answer support questions.", "sales": "Answer sales questions."}


def agent_params(runtime: ManagedServerRuntime) -> dict:
    execution = runtime.execution_runtime
    context = (execution.context if execution is not None else None) or {}
    return {"mode": context.get("mode", "support")}


@cached_agent(keyed_by=agent_params)
def agent(params: dict):
    return define_deep_agent(
        name="assistant",
        model="openai:gpt-5.5",
        instructions=PROMPTS[params["mode"]],
    )
```

## Use LLM Gateway

You can use [LLM Gateway](../../../../LLM%20Gateway/Get%20started/LLM%20Gateway.md) to apply rate limits, fallbacks, and other policies to model calls.

Prefix the gateway model ID with `langsmith:`:

```python
from managed_deepagents import define_deep_agent

agent = define_deep_agent(
    name="my-agent",
    model="langsmith:moonshotai/kimi-k3",
)
```

> [!NOTE]
>
> Gateway model IDs use a slash between provider and model (`langsmith:provider/model-name`). Model strings that call a provider directly use a colon (`provider:model-name`).

The gateway routes each request by model ID. `moonshotai/kimi-k3` is a LangChain-hosted model, so it requires no provider secret and draws on [Gateway Credits](../../../../LLM%20Gateway/Models%20and%20reliability/Gateway%20Credits.md). A model ID that starts with a provider your workspace has configured, such as `anthropic/claude-opus-5`, uses that [provider secret](../../../../LLM%20Gateway/Authentication/Provider%20authentication.md#add-a-provider-key) and bills to your own provider account.

For more information, see [LLM Gateway](../../../../LLM%20Gateway/Get%20started/LLM%20Gateway.md).

To scaffold a project that uses Gateway from the start, pass `--gateway` when initializing:

```bash
mda init my-agent --gateway
```
