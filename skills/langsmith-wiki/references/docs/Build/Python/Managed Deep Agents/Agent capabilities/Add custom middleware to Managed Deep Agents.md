# Add custom middleware to Managed Deep Agents

> Add built-in or custom middleware to a managed deep agent.

Middleware adds behavior around model calls, tool calls, and the agent lifecycle. Like [custom tools](Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md), MDA does not discover middleware automatically. Import it and pass it to the agent definition.

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

Put custom middleware under `middleware/`, import it into the agent entry, and pass it to the agent definition:

```text
my-agent/
  agent.py
  middleware/
    audit.py
```

For the full project layout, see [Project structure](../Get%20started/Managed%20Deep%20Agents%20project%20structure.md).

The managed runtime still owns `backend`, `store`, `checkpointer`, `memory`, `skills`, and the system prompt. Middleware should focus on agent behavior around model calls, tool calls, and lifecycle hooks.

## Add middleware

Use middleware to redact PII, enforce call limits, retry failures, fall back between models, select models dynamically, or log and inspect tool calls.

**1. Use prebuilt middleware**

You can use LangChain [prebuilt middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in.md) directly in the agent definition:

```python agent.py
from langchain.agents.middleware import ModelCallLimitMiddleware, PIIMiddleware
from managed_deepagents import define_deep_agent

agent = define_deep_agent(
    name="support-agent",
    model="openai:gpt-6.1-sol",
    middleware=[
        PIIMiddleware("email", strategy="redact", apply_to_input=True),
        ModelCallLimitMiddleware(run_limit=50),
    ],
)
```

**2. Define custom middleware (Optional)**

For a more advanced option, define [custom middleware](https://docs.langchain.com/oss/python/langchain/middleware/custom.md) in a local module.

> [!NOTE]
>
> Middleware is a shared LangChain primitive. Managed Deep Agents always invoke the agent with `ainvoke` and `astream`, so custom middleware must use async hooks. Synchronous hooks remain available when you call [Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview.md) with `invoke` or `stream`.

```python middleware/audit.py
from collections.abc import Awaitable, Callable

from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest
from langgraph.types import Command


@wrap_tool_call
async def log_tool_calls(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], Awaitable[ToolMessage | Command]],
) -> ToolMessage | Command:
    print(f"Calling tool: {request.tool_call['name']}")
    result = await handler(request)
    print(f"Finished tool: {request.tool_call['name']}")
    return result
```

Import the middleware into the project-root agent entry and pass it in the `middleware` list:

```python agent.py
from managed_deepagents import define_deep_agent

from middleware.audit import log_tool_calls

agent = define_deep_agent(
    name="support-agent",
    model="openai:gpt-6.1-sol",
    middleware=[log_tool_calls],
)
```

Your middleware imports should work the same way they do in a normal local Python project.

## Use runtime context

Middleware can read per-run context through the normal LangChain runtime APIs. Use context for user IDs, organization IDs, feature flags, request metadata, or credentials that should not be part of the model prompt by default.

For examples, see [Custom middleware](https://docs.langchain.com/oss/python/langchain/middleware/custom.md).

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
