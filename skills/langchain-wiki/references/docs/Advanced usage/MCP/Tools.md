# Tools

> Load MCP tools into LangChain agents, control their execution, and handle server results and requests.

> [!NOTE]
>
> The `langchain.mcp` namespace requires `langchain[mcp]>=1.4.0` and is in beta. The API may change.

[`MCPAdapter`](https://reference.langchain.com/python/langchain/mcp/adapter/MCPAdapter) bridges MCP servers and LangChain agents: it discovers the tools a server advertises and adapts them into standard LangChain tools. Pass the tools from `list_tools()` to [`create_agent`](https://reference.langchain.com/python/langchain/agents/factory/create_agent) as you would any other LangChain tool.

This page covers what is specific to that bridge: identifying MCP tools, controlling their execution, handling their outputs, and responding when a server needs input during a call. For the runnable discovery-and-agent example, see the [MCP quickstart](Model%20Context%20Protocol%20%28MCP%29.md).

## Use MCP tools in an agent

Discover the server's catalog with [`MCPAdapter.list_tools`](https://reference.langchain.com/python/langchain/mcp/adapter/MCPAdapter/list_tools), then give the returned tools to [`create_agent`](https://reference.langchain.com/python/langchain/agents/factory/create_agent). From the agent's perspective, they behave like LangChain tools: the model chooses a tool, LangChain invokes it, and the resulting [`ToolMessage`](https://reference.langchain.com/python/langchain-core/messages/tool/ToolMessage) returns to the model.

```python
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter


async def run_agent(server) -> dict:
    # Discover the server's tools, then hand them to the agent like any other
    # LangChain tools. The tools hold the client, so the agent stays usable
    # for the life of the adapter context.
    async with MCPAdapter(server) as adapter:
        tools = await adapter.list_tools()
        agent = create_agent("claude-sonnet-5", tools)
        return await agent.ainvoke(
            {
                "messages": [
                    {"role": "user", "content": "What is the forecast for Oslo?"}
                ]
            }
        )
```

> [card] [View example trace](https://smith.langchain.com/public/d1f0e6b6-32e7-430e-a167-919f6427d4e2/r)
>
> Open a public LangSmith run for this example.

For general guidance on defining, binding, and using LangChain tools, see [Tools](../../Core%20components/Tools.md). For several MCP servers and their namespaced tool catalogs, see [Connections](Connections.md#multiple-servers).

## Handle tool outputs

MCP tool results become [`ToolMessage`](https://reference.langchain.com/python/langchain-core/messages/tool/ToolMessage) objects with content the model can read, an artifact for application data, and a status indicating success or failure.

### Multimodal content

The adapter converts model-visible MCP content into LangChain [content blocks](../../Core%20components/Messages.md#standard-content-blocks). For example, a tool that returns an MCP image block with a screenshot reaches the model as an `image` block.

```python
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
from langchain.messages import ToolMessage


async def access_multimodal_tool_content(server) -> dict:
    async with MCPAdapter(server) as adapter:
        tools = await adapter.list_tools()
        agent = create_agent("claude-sonnet-5", tools)
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "Take a screenshot."}]}
        )

    # An MCP result arrives as LangChain content blocks. Image and file content
    # convert into standardized `image`/`file` blocks alongside `text`.
    for message in result["messages"]:
        if not isinstance(message, ToolMessage):
            continue
        for block in message.content_blocks:  # [!code highlight]
            if block["type"] == "text":  # [!code highlight]
                print(f"Text: {block['text']}")  # [!code highlight]
            elif block["type"] == "image":  # [!code highlight]
                preview = block.get("base64", "")[:20]  # [!code highlight]
                print(f"Image mime type: {block.get('mime_type')}")  # [!code highlight]
                print(f"Image base64: {preview}...")  # [!code highlight]

    return result
```

> [card] [View example trace](https://smith.langchain.com/public/e5bd94b5-4592-41c4-816b-265630c4af6d/r)
>
> Open a public LangSmith run for this example.

### Structured content

When a tool returns structured content, the adapter attaches it to the [`ToolMessage`](https://reference.langchain.com/python/langchain-core/messages/tool/ToolMessage) as an artifact rather than folding it into the model-visible text. Run the agent, then read the `artifact` from the [`ToolMessage`](https://reference.langchain.com/python/langchain-core/messages/tool/ToolMessage) instances in the result:

```python
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
from langchain.messages import ToolMessage


async def run_agent_structured(server) -> dict:
    async with MCPAdapter(server) as adapter:
        tools = await adapter.list_tools()
        agent = create_agent("claude-sonnet-5", tools)
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "Look up user 42."}]}
        )

    # The adapter sets `artifact` only when the tool returned structured
    # content, so a non-None artifact always carries `structured_content`.
    for message in result["messages"]:
        if isinstance(message, ToolMessage) and message.artifact is not None:
            structured = message.artifact["structured_content"]  # [!code highlight]
            print(f"Structured content: {structured}")  # [!code highlight]

    return result
```

> [card] [View example trace](https://smith.langchain.com/public/bc364aff-d6df-4849-99b2-c943fd21cf75/r)
>
> Open a public LangSmith run for this example.

The artifact is an `MCPToolArtifact`, whose `structured_content` field holds the tool result's `structuredContent`. A tool that returns no structured content leaves `artifact` as `None`.

### Errors

An MCP tool result carries an `isError` flag. When a server reports `isError=True`, the adapter converts it into a [`ToolMessage`](https://reference.langchain.com/python/langchain-core/messages/tool/ToolMessage) with `status="error"` carrying the server's own message, so the agent can read it and correct itself:

```python
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
from langchain.messages import ToolMessage


async def divide_by_zero(server) -> dict:
    async with MCPAdapter(server) as adapter:
        tools = await adapter.list_tools()
        agent = create_agent("claude-sonnet-5", tools)
        result = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "Use the divide tool to calculate 10 divided by 0.",
                    }
                ]
            }
        )

    # A server error (isError=True) reaches the model as a failed ToolMessage,
    # so the agent can read the server's own message and recover. Transport
    # failures still raise, because a model cannot act on those.
    for message in result["messages"]:
        if isinstance(message, ToolMessage) and message.status == "error":
            print(f"Tool reported: {message.text}")  # [!code highlight]

    return result
```

A server-reported error reaches the model as a failed tool message, but a transport or session failure raises instead.

## Tool metadata

Each adapted tool may carry its MCP provenance under an `mcp` namespace on the LangChain tool's metadata:

```python
tool.metadata
# {
#     "mcp": {
#         "tool": {
#             "annotations": {
#                 "destructive_hint": True,
#                 "read_only_hint": False,
#             },
#             "_meta": {"origin": "crm"},
#         },
#         "server": {
#             "name": "crm",
#             "version": "2.1.0",
#         },
#     },
# }
```

Every nested field is optional: a server may provide tool annotations, `_meta`, server identity, any combination of those, or none. `annotations` contains MCP hints such as `read_only_hint` and `destructive_hint`; `_meta` is opaque metadata supplied by the server; and `server` identifies the MCP implementation that advertised the tool.

Read optional metadata defensively, so a missing field returns a default rather than failing:

```python
from langchain.tools import BaseTool


def is_destructive(tool: BaseTool) -> bool:
    """Read the MCP destructive hint off the adapter's tool metadata."""
    # Chain `.get` with defaults so a tool missing any nested field returns
    # False rather than raising.
    annotations = (
        (tool.metadata or {}).get("mcp", {}).get("tool", {}).get("annotations", {})
    )
    return annotations.get("destructive_hint", False)
```

## Human-in-the-loop

Reading annotations lets you gate a tool based on what the server declares about it, rather than hardcoding tool names. The MCP annotation classifies the tool and LangChain's human-in-the-loop middleware enforces the approval policy.

Read the destructive hint from metadata once during tool discovery. Then give the human-in-the-loop configuration a `when` predicate that receives each pending tool call and returns whether the call needs approval:

```python
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.agents.middleware.human_in_the_loop import InterruptOnConfig
from langchain.tools import BaseTool
from langchain.tools.tool_node import ToolCallRequest


def is_destructive(tool: BaseTool) -> bool:
    """Read the MCP destructive hint off the adapter's tool metadata."""
    annotations = (
        (tool.metadata or {}).get("mcp", {}).get("tool", {}).get("annotations", {})
    )
    return annotations.get("destructive_hint", False)


async def gate_destructive_tools(server):
    async with MCPAdapter(server) as adapter:
        tools = await adapter.list_tools()

        # Read the destructive hint from metadata once, then let a callable
        # decide per call. One config covers whatever destructive tools a
        # server exposes, without hardcoding tool names.
        destructive = {tool.name for tool in tools if is_destructive(tool)}

        def needs_approval(request: ToolCallRequest) -> bool:
            return request.tool_call["name"] in destructive

        gate = InterruptOnConfig(
            allowed_decisions=["approve", "reject"], when=needs_approval
        )
        interrupt_on: dict[str, bool | InterruptOnConfig] = {
            tool.name: gate for tool in tools
        }
        return create_agent(
            "claude-sonnet-5",
            tools,
            middleware=[HumanInTheLoopMiddleware(interrupt_on=interrupt_on)],
            checkpointer=InMemorySaver(),
        )
```

When the agent calls a tool that the predicate gates, the run pauses. Approve the call to run it, or reject it to skip the tool and tell the model:

```python
from langgraph.types import Command

# Approve the pending destructive call and resume.
resumed = await agent.ainvoke(
    Command(resume={"decisions": [{"type": "approve"}]}), config
)
```

The predicate can also inspect the call's arguments. This lets a tool run freely for safe inputs and pause only for risky ones, such as a `delete_file` call targeting a protected path.

Access the arguments through `request.tool_call["args"]`.

Combine the metadata classification and argument check to gate a tool only when its type and inputs warrant approval. For the full approval workflow, see [Human-in-the-loop](../Human-in-the-loop.md).

## Server requests during tool execution

Most tools finish without asking the client for anything mid-call. When a server needs input, [`MCPAdapter`](https://reference.langchain.com/python/langchain/mcp/adapter/MCPAdapter) surfaces [elicitation](https://modelcontextprotocol.io/specification/draft/client/elicitation) as a LangGraph [`interrupt`](https://reference.langchain.com/python/langgraph/types/interrupt).

### Elicitation

[Elicitation](https://modelcontextprotocol.io/specification/draft/client/elicitation) lets an MCP server request input during a tool call. The adapter pauses the run with a LangGraph interrupt. Your application presents the request to the user and resumes the run with their answer. Agent Server asks for input this way when an agent exposed through its MCP endpoint pauses. For more information, see [Human-in-the-loop over MCP](https://docs.langchain.com/langsmith/server-mcp-elicitation.md).

Attach a [checkpointer](../../Core%20components/Short-term%20memory.md) to the agent and use the same `thread_id` when invoking and resuming it.

This example assumes the booking tool asks for one date and pauses once. Replace the sample date with the user's answer.

```python
from typing import Any

from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command


async def book_with_elicitation(server) -> dict:
    # Elicitation is handled automatically: when a server needs input mid-call,
    # the adapter surfaces the question as a LangGraph `interrupt()`, so the
    # person already reviewing the agent's work answers it and the run resumes.
    async with MCPAdapter(server) as adapter:
        tools = await adapter.list_tools()

        # Resuming a paused run needs persistence, so the interrupted run has
        # somewhere to wait.
        agent = create_agent("claude-sonnet-5", tools, checkpointer=InMemorySaver())
        config: Any = {"configurable": {"thread_id": "booking-1"}}

        paused = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "Book a table for 4."}]}, config
        )
        [interrupt] = paused["__interrupt__"]
        [question] = interrupt.value["requests"]

        # Answers are keyed by the server's own request key, so nothing has to
        # be tracked across the pause. `decline` or `cancel` would refuse.
        answer = {"action": "accept", "content": {"date": "2026-09-14"}}
        return await agent.ainvoke(
            Command(resume={"responses": {question["key"]: answer}}), config
        )
```

Elicitation is on by default. The adapter advertises the capability and drives the interrupt loop. A prebuilt client that already carries its own elicitation handler is honored instead of overridden.

Resume with `Command(resume={"responses": {key: answer}})`. The interrupt payload and answer types live in `langchain.mcp.elicitation`.

> [!NOTE]
>
> Resuming reruns the tool from the beginning. Any work performed before the server asks for input can repeat. Make that work safe to repeat without duplicating side effects.

Each answer uses one of these actions:

* **`accept`**: Provide form `content` matching the request's schema, or confirm completion of a URL interaction without `content`.
* **`decline`**: Refuse to provide the requested information.
* **`cancel`**: Indicate that the user canceled the interaction.

The adapter forwards the answer to the server, which decides how the tool call finishes.

Only elicitation is answered this way. A server that instead asks for [sampling](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling) or [roots](https://modelcontextprotocol.io/specification/2025-06-18/client/roots) raises an error, because the modern, sessionless protocol has no live back-channel for those requests. See [Sampling and roots](https://docs.langchain.com/oss/python/migrate/langchain-mcp-adapters.md#sampling-and-roots).

> [!NOTE]
>
> Interrupt-driven elicitation answers a server that returns its request as an `InputRequiredResult`. A server that only pushes elicitation over a legacy handshake session cannot be answered this way.

## See also

* [Content blocks](../../Core%20components/Messages.md#standard-content-blocks)

* [Tools](../../Core%20components/Tools.md)

* [Human-in-the-loop](../Human-in-the-loop.md)

* [FastMCP calling tools](https://gofastmcp.com/clients/tools)

* [FastMCP client elicitation](https://gofastmcp.com/clients/elicitation)

* [FastMCP server elicitation](https://gofastmcp.com/servers/elicitation)

* [MCP elicitation specification](https://modelcontextprotocol.io/specification/draft/client/elicitation)

* [MCP tool annotations](https://modelcontextprotocol.io/specification/draft/server/tools)

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/mcp/tools.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
