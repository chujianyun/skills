# Tools

> Define tools that let LangChain agents fetch real-time data, execute code, query external databases, and take actions.

Tools extend what [agents](Agents.md) can do—letting them fetch real-time data, execute code, query external databases, and take actions in the world.

Under the hood, tools are callable functions with well-defined inputs and outputs that get passed to a [chat model](Models.md). The model decides when to invoke a tool based on the conversation context, and what input arguments to provide.

> [!TIP]
>
> For details on how models handle tool calls, see [Tool calling](Models.md#tool-calling). Trace tool calls and debug errors with [LangSmith](https://smith.langchain.com?utm_source=docs\&utm_medium=cta\&utm_campaign=langsmith-signup\&utm_content=oss-langchain-tools). Follow the [tracing quickstart](https://docs.langchain.com/langsmith/trace-with-langchain.md) to get set up.
>
> We recommend you also set up [LangSmith Engine](https://docs.langchain.com/langsmith/engine.md) which monitors your traces, detects issues, and proposes fixes.

## Create tools

### Basic tool definition

The simplest way to create a tool is with the [`@tool`](https://reference.langchain.com/python/langchain-core/tools/convert/tool) decorator. By default, the function's docstring becomes the tool's description that helps the model understand when to use it:

```python
from langchain.tools import tool

@tool
def search_database(query: str, limit: int = 10) -> str:
    """Search the customer database for records matching the query.

    Args:
        query: Search terms to look for
        limit: Maximum number of results to return
    """
    return f"Found {limit} results for '{query}'"
```

Type hints are **required** as they define the tool's input schema. The docstring should be informative and concise to help the model understand the tool's purpose.

> [!NOTE]
>
> **Server-side tool use:** Some chat models feature built-in tools (web search, code interpreters) that are executed server-side. See [Server-side tool use](#server-side-tool-use) for details.

> [!WARNING]
>
> Prefer `snake_case` for tool names (e.g., `web_search` instead of `Web Search`). Some model providers have issues with or reject names containing spaces or special characters with errors. Sticking to alphanumeric characters, underscores, and hyphens helps to improve compatibility across providers.

### Customize tool properties

#### Custom tool name

By default, the tool name comes from the function name. Override it when you need something more descriptive:

```python
@tool("web_search")  # Custom name
def search(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"

print(search.name)  # web_search
```

#### Custom tool description

Override the auto-generated tool description for clearer model guidance:

```python
@tool("calculator", description="Performs arithmetic calculations. Use this for any math problems.")
def calc(expression: str) -> str:
    """Evaluate mathematical expressions."""
    return str(eval(expression))
```

### Advanced schema definition

Define complex inputs with Pydantic models or JSON schemas:

```python Pydantic model
from pydantic import BaseModel, Field
from typing import Literal

class WeatherInput(BaseModel):
    """Input for weather queries."""
    location: str = Field(description="City name or coordinates")
    units: Literal["celsius", "fahrenheit"] = Field(
        default="celsius",
        description="Temperature unit preference"
    )
    include_forecast: bool = Field(
        default=False,
        description="Include 5-day forecast"
    )

@tool(args_schema=WeatherInput)
def get_weather(location: str, units: str = "celsius", include_forecast: bool = False) -> str:
    """Get current weather and optional forecast."""
    temp = 22 if units == "celsius" else 72
    result = f"Current weather in {location}: {temp} degrees {units[0].upper()}"
    if include_forecast:
        result += "\nNext 5 days: Sunny"
    return result
```

```python JSON Schema
weather_schema = {
    "type": "object",
    "properties": {
        "location": {"type": "string"},
        "units": {"type": "string"},
        "include_forecast": {"type": "boolean"}
    },
    "required": ["location", "units", "include_forecast"]
}

@tool(args_schema=weather_schema)
def get_weather(location: str, units: str = "celsius", include_forecast: bool = False) -> str:
    """Get current weather and optional forecast."""
    temp = 22 if units == "celsius" else 72
    result = f"Current weather in {location}: {temp} degrees {units[0].upper()}"
    if include_forecast:
        result += "\nNext 5 days: Sunny"
    return result
```

### Reserved argument names

The following parameter names are reserved and cannot be used as tool arguments. Using these names will cause runtime errors.

| Parameter name | Purpose |
| - | - |
| `config` | Reserved for passing `RunnableConfig` to tools internally |
| `runtime` | Reserved for `ToolRuntime` parameter (accessing state, context, store) |

To access runtime information, use the [`ToolRuntime`](https://reference.langchain.com/python/langchain/tools/#langchain.tools.ToolRuntime) parameter instead of naming your own arguments `config` or `runtime`.

If you use `InjectedState`, `InjectedStore`, `get_runtime()`, or `InjectedToolCallId`, see [Migrate from older injection patterns](#migrate-from-older-injection-patterns).

## Access context

Tools are most powerful when they can access runtime information like conversation history, user data, and persistent memory. This section covers how to access and update this information from within your tools.

Tools can access runtime information through the [`ToolRuntime`](https://reference.langchain.com/python/langchain/tools/#langchain.tools.ToolRuntime) parameter, which provides:

| Component | Description | Use case |
| - | - | - |
| **State** | Short-term memory - mutable data that exists for the current conversation (messages, counters, custom fields) | Access conversation history, track tool call counts |
| **Context** | Immutable configuration passed at invocation time (user IDs, session info) | Personalize responses based on user identity |
| **Store** | Long-term memory - persistent data that survives across conversations | Save user preferences, maintain knowledge base |
| **Stream Writer** | Emit real-time updates during tool execution | Show progress for long-running operations |
| **Execution Info** | Identity and retry information for the current execution (thread ID, run ID, attempt number) | Access thread/run IDs, adjust behavior based on retry state |
| **Server Info** | Server-specific metadata when running on LangSmith Agent Server (assistant ID, graph ID, authenticated user) | Access assistant ID, graph ID, or authenticated user info |
| **Config** | [`RunnableConfig`](https://reference.langchain.com/python/langchain-core/runnables/config/RunnableConfig) for the execution | Access callbacks, tags, and metadata |
| **Tool Call ID** | Unique identifier for the current tool invocation | Correlate tool calls for logs and model invocations |

```mermaid
graph LR
    %% Runtime Context
    subgraph "🔧 Tool Runtime Context"
        A[Tool Call] --> B[ToolRuntime]
        B --> C[State Access]
        B --> D[Context Access]
        B --> E[Store Access]
        B --> F[Stream Writer]
    end

    %% Available Resources
    subgraph "📊 Available Resources"
        C --> G[Messages]
        C --> H[Custom State]
        D --> I[User ID]
        D --> J[Session Info]
        E --> K[Long-term Memory]
        E --> L[User Preferences]
    end

    %% Tool Capabilities
    subgraph "⚡ Enhanced Tool Capabilities"
        M[Context-Aware Tools]
        N[Stateful Tools]
        O[Memory-Enabled Tools]
        P[Streaming Tools]
    end

    %% Connections
    G --> M
    H --> N
    I --> M
    J --> M
    K --> O
    L --> O
    F --> P

    classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
    classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
    classDef output fill:#EBD0F0,stroke:#885270,stroke-width:2px,color:#441E33
    classDef neutral fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#2F4B68

    class A trigger
    class B,C,D,E,F process
    class G,H,I,J,K,L neutral
    class M,N,O,P output
```

### Short-term memory (State)

State represents short-term memory that exists for the duration of a conversation. It includes the message history and any custom fields you define in your [graph state](https://docs.langchain.com/oss/python/langgraph/graph-api.md#state).

#### Access state

Add `runtime: ToolRuntime` to your tool signature to access state. At call time, [`ToolNode`](https://reference.langchain.com/python/langgraph/agents/#langgraph.prebuilt.tool_node.ToolNode) injects the value automatically; the parameter is not included in the tool schema sent to the model. Use `runtime.state` to read the current conversation state:

```python
from langchain.tools import tool, ToolRuntime
from langchain.messages import HumanMessage

@tool
def get_last_user_message(runtime: ToolRuntime) -> str:
    """Get the most recent message from the user."""
    messages = runtime.state["messages"]

    # Find the last human message
    for message in reversed(messages):
        if isinstance(message, HumanMessage):
            return message.content

    return "No user messages found"

# Access custom state fields
@tool
def get_user_preference(
    pref_name: str,
    runtime: ToolRuntime
) -> str:
    """Get a user preference value."""
    preferences = runtime.state.get("user_preferences", {})
    return preferences.get(pref_name, "Not set")
```

> [!WARNING]
>
> The `runtime` parameter is hidden from the model. For the example above, the model only sees `pref_name` in the tool schema.

#### Update state

Use [`Command`](https://reference.langchain.com/python/langgraph/types/Command) to update the agent's state. This is useful for tools that need to update custom state fields.
Include a `ToolMessage` in the update so the model can see the result of the tool call:

```python
from langchain.agents import AgentState
from langchain.messages import ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.types import Command


class CustomState(AgentState):
    user_name: str


@tool
def set_user_name(new_name: str, runtime: ToolRuntime[None, CustomState]) -> Command:
    """Set the user's name in the conversation state."""
    return Command(
        update={
            "user_name": new_name,
            "messages": [
                ToolMessage(
                    content=f"User name set to {new_name}.",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
        }
    )
```

> [card] [View example trace](https://smith.langchain.com/public/d29da0cb-a0f6-4a14-b976-9f4154e46c4c/r)
>
> Open a public LangSmith run for this example.

> [!TIP]
>
> When tools update state variables, consider defining a [reducer](https://docs.langchain.com/oss/python/langgraph/graph-api.md#reducers) for those fields. Since LLMs can call multiple tools in parallel, a reducer determines how to resolve conflicts when the same state field is updated by concurrent tool calls.

### Context

Context provides immutable configuration data that is passed at invocation time. Use it for user IDs, session details, or application-specific settings that shouldn't change during a conversation.

> [!NOTE]
>
> While `thread_id` (passed via `config={"configurable": {"thread_id": ...}}`) scopes the *conversation*: message history and checkpoints, `context` carries *per-run* data your tools and middleware read at invocation time. Persistence requires a [checkpointer](Short-term%20memory.md). In production you typically pass both a stable `thread_id` per conversation and a `context` object on every invoke.

Access context through `runtime.context`. Configure a [checkpointer](Short-term%20memory.md) and pass `context` with a stable `thread_id` so the conversation persists across invocations:

```python
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain_core.utils.uuid import uuid7
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver


USER_DATABASE = {
    "user123": {
        "name": "Alice Johnson",
        "account_type": "Premium",
        "balance": 5000,
        "email": "alice@example.com",
    },
    "user456": {
        "name": "Bob Smith",
        "account_type": "Standard",
        "balance": 1200,
        "email": "bob@example.com",
    },
}


@dataclass
class UserContext:
    user_id: str


@tool
def get_account_info(runtime: ToolRuntime[UserContext]) -> str:
    """Get the current user's account information."""
    user_id = runtime.context.user_id

    if user_id in USER_DATABASE:
        user = USER_DATABASE[user_id]
        return (
            f"Account holder: {user['name']}\n"
            f"Type: {user['account_type']}\n"
            f"Balance: ${user['balance']}"
        )
    return "User not found"


model = ChatOpenAI(model="gpt-6.1-sol")
agent = create_agent(
    model,
    tools=[get_account_info],
    context_schema=UserContext,
    checkpointer=InMemorySaver(),
    system_prompt="You are a financial assistant.",
)

thread_id = str(uuid7())
config = {"configurable": {"thread_id": thread_id}}
context = UserContext(user_id="user123")

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's my current balance?"}]},
    config=config,
    context=context,
)
print(result["messages"][-1].content_blocks)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What was my balance again?"}]},
    config=config,
    context=context,
)
print(result["messages"][-1].content_blocks)
```

> [card] [View example trace](https://smith.langchain.com/public/71fda0a0-84cc-4eb8-83a1-611ebbd675a5/r)
>
> Open a public LangSmith run for this example.

### Long-term memory (Store)

The [`BaseStore`](https://reference.langchain.com/python/langchain-core/stores/BaseStore) provides persistent storage that survives across conversations. Unlike state (short-term memory), data saved to the store remains available in future sessions.

Access the store through `runtime.store`. The store uses a namespace/key pattern to organize data:

> [!TIP]
>
> For production deployments, use a persistent store implementation like [`PostgresStore`](https://reference.langchain.com/python/langgraph/store/#langgraph.store.postgres.PostgresStore), `MongoDBStore`, or `RedisStore` instead of `InMemoryStore`. See the [memory documentation](https://docs.langchain.com/oss/python/langgraph/add-memory.md) for setup details.

```python expandable
from langgraph.store.memory import InMemoryStore
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain_openai import ChatOpenAI

# Access memory
@tool
def get_user_info(user_id: str, runtime: ToolRuntime) -> str:
    """Look up user info."""
    store = runtime.store
    user_info = store.get(("users",), user_id)
    return str(user_info.value) if user_info else "Unknown user"

# Update memory
@tool
def save_user_info(user_id: str, name: str, age: int, email: str, runtime: ToolRuntime) -> str:
    """Save user info."""
    store = runtime.store
    store.put(("users",), user_id, {"name": name, "age": age, "email": email})
    return "Successfully saved user info."

model = ChatOpenAI(model="gpt-6.1-sol")

store = InMemoryStore()
agent = create_agent(
    model,
    tools=[get_user_info, save_user_info],
    store=store
)

# First session: save user info
agent.invoke({
    "messages": [{"role": "user", "content": "Save the following user: userid: abc123, name: Foo, age: 25, email: foo@langchain.dev"}]
})

# Second session: get user info
agent.invoke({
    "messages": [{"role": "user", "content": "Get user info for user with id 'abc123'"}]
})
# Here is the user info for user with ID "abc123":
# - Name: Foo
# - Age: 25
# - Email: foo@langchain.dev
```

### Stream writer

Stream real-time updates from tools during execution. This is useful for providing progress feedback to users during long-running operations.

Use `runtime.stream_writer` to emit custom updates:

```python
from langchain.tools import tool, ToolRuntime

@tool
def get_weather(city: str, runtime: ToolRuntime) -> str:
    """Get weather for a given city."""
    writer = runtime.stream_writer

    # Stream custom updates as the tool executes
    writer(f"Looking up data for city: {city}")
    writer(f"Acquired data for city: {city}")

    return f"It's always sunny in {city}!"
```

> [!NOTE]
>
> If you use `runtime.stream_writer` inside your tool, the tool must be invoked within a LangGraph execution context. See [Streaming](Streaming.md) for more details.

### Execution info

Access thread ID, run ID, and retry state from within a tool via `runtime.execution_info`:

```python
from langchain.tools import tool, ToolRuntime

@tool
def log_execution_context(runtime: ToolRuntime) -> str:
    """Log execution identity information."""
    info = runtime.execution_info
    print(f"Thread: {info.thread_id}, Run: {info.run_id}")  # [!code highlight]
    print(f"Attempt: {info.node_attempt}")
    return "done"
```

> [!NOTE]
>
> Requires `deepagents>=0.5.0` (or `langgraph>=1.1.5`).

### Server info

When your tool runs on Agent Server, access the assistant ID, graph ID, and authenticated user via `runtime.server_info`:

```python
from langchain.tools import tool, ToolRuntime

@tool
def get_assistant_scoped_data(runtime: ToolRuntime) -> str:
    """Fetch data scoped to the current assistant."""
    server = runtime.server_info
    if server is not None:
        print(f"Assistant: {server.assistant_id}, Graph: {server.graph_id}")  # [!code highlight]
        if server.user is not None:
            print(f"User: {server.user.identity}")  # [!code highlight]
    return "done"
```

`server_info` is `None` when the tool is not running on Agent Server (e.g., during local development or testing).

> [!NOTE]
>
> Requires `deepagents>=0.5.0` (or `langgraph>=1.1.5`).

> [accordion] Migrate from older injection patterns
>
> Older examples used `InjectedState`, `InjectedStore`, `get_runtime()`, or `InjectedToolCallId`. Use [`ToolRuntime`](https://reference.langchain.com/python/langchain/tools/#langchain.tools.ToolRuntime) instead for one explicit interface to state, context, store, and execution metadata.
>
> #### Previous pattern
>
> ```python
> from langchain.tools import tool, InjectedState
>
> @tool
> def summarize(state: InjectedState) -> str:
>     """Summarize the conversation."""
>     messages = state["messages"]
>     return f"Conversation length: {len(messages)} messages."
> ```
>
> #### Recommended pattern
>
> ```python
> from langchain.tools import tool, ToolRuntime
>
> @tool
> def summarize(runtime: ToolRuntime) -> str:
>     """Summarize the conversation."""
>     messages = runtime.state["messages"]
>     return f"Conversation length: {len(messages)} messages."
> ```
>
> For agent-level migrations (for example `create_react_agent` and custom state), see the [LangChain v1 migration guide](https://docs.langchain.com/oss/python/migrate/langchain-v1.md).

## Tool execution

In LangChain, tools are used by agents (for example via [`create_agent`](https://reference.langchain.com/python/langchain/agents/factory/create_agent)) and tool error handling is configured through [middleware](https://docs.langchain.com/oss/python/langchain/middleware.md).

For LangGraph workflows, tool execution is handled by [`ToolNode`](https://reference.langchain.com/python/langgraph/agents/#langgraph.prebuilt.tool_node.ToolNode). See [ToolNode](https://docs.langchain.com/oss/python/langgraph/workflows-agents.md#toolnode) for Graph API usage, including how tools can access the current graph state and run-scoped context.

### Tool return values

You can choose different return values for your tools:

* Return a `string` for human-readable results.
* Return an `object` for structured results the model should parse.
* Return a `Command` with optional message when you need to write to state.

#### Return a string

Return a string when the tool should provide plain text for the model to read and use in its next response.

```python
from langchain.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"It is currently sunny in {city}."
```

> [card] [View example trace](https://smith.langchain.com/public/9c20937f-20e4-4ed2-adfa-eeda6fd63997/r)
>
> Open a public LangSmith run for this example.

Behavior:

* The return value is converted to a `ToolMessage`.
* The model sees that text and decides what to do next.
* No agent state fields are changed unless the model or another tool does so later.

Use this when the result is naturally human-readable text.

#### Return an object

Return an object (for example, a `dict`) when your tool produces structured data that the model should inspect.

```python
from langchain.tools import tool


@tool
def get_weather_data(city: str) -> dict:
    """Get structured weather data for a city."""
    return {
        "city": city,
        "temperature_c": 22,
        "conditions": "sunny",
    }
```

> [card] [View example trace](https://smith.langchain.com/public/2f82d8ae-bcf6-4b6d-94ee-0d724c30fa98/r)
>
> Open a public LangSmith run for this example.

Behavior:

* The object is serialized and sent back as tool output.
* The model can read specific fields and reason over them.
* Like string returns, this does not directly update graph state.

Use this when downstream reasoning benefits from explicit fields instead of free-form text.

#### Return multimodal content

Tools are not limited to plain text. When the model supports multimodal tool results, the tool can return [standard content blocks](Messages.md#standard-content-blocks) so the model receives text, images, and other media in one tool result.

```python
from langchain.tools import tool


@tool
def capture_screenshot() -> list[dict]:
    """Capture a screenshot of the current page."""
    return [
        {"type": "text", "text": "Screenshot of the current page:"},
        {"type": "image", "url": "https://example.com/page.png"},
    ]
```

Behavior:

* The return value is converted to a `ToolMessage` with multimodal `content`.
* Use `message.content_blocks` to read the normalized block list after the tool runs.
* The model must support the modalities you return. Check your [model's capabilities](https://docs.langchain.com/oss/python/integrations/chat.md) before returning images, audio, or video.

For block types and provider-specific requirements, see [Multimodal messages](Messages.md#multimodal).

MCP tools that return images or mixed content are converted the same way. See [Multimodal content](../Advanced%20usage/MCP/Tools.md#multimodal-content).

#### Return a Command

Return a [`Command`](https://reference.langchain.com/python/langgraph/types/Command) when the tool needs to update graph state (for example, setting user preferences or app state).
When the `Command` targets the current graph, include a `ToolMessage` in the update whose tool call ID matches the current tool call.
Every tool call in the message history must have a corresponding `ToolMessage`.

Use `runtime.tool_call_id` for the `tool_call_id` parameter. `ToolNode` enforces this requirement: if the update has no `ToolMessage` matching the tool call, it raises a `ValueError`.

```python
from langchain.messages import ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.types import Command


@tool
def set_language(language: str, runtime: ToolRuntime) -> Command:
    """Set the preferred response language."""
    return Command(
        update={
            "preferred_language": language,
            "messages": [
                ToolMessage(
                    content=f"Language set to {language}.",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
        }
    )
```

Behavior:

* The command updates state using `update`.
* Updated state is available to subsequent steps in the same run.
* Use reducers for fields that may be updated by parallel tool calls.

Use this when the tool is not just returning data, but also mutating agent state.

#### Return directly from a tool

Set return direct on a tool to short-circuit the agent loop: the agent returns the tool's output to the caller immediately, without sending it back through the model for further processing.

```python
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI


@tool(return_direct=True)
def fetch_order_status(order_id: str) -> str:
    """Fetch the current status of a customer order."""
    # In production, query your order management system here
    return f"Order {order_id} is shipped and will arrive in 2 days."


agent = create_agent(
    ChatOpenAI(model="gpt-5.4-mini"),
    tools=[fetch_order_status],
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "What is the status of order #12345?"}]
})
# The agent returns the tool output directly without another LLM call:
# "Order 12345 is shipped and will arrive in 2 days."
```

> [card] [View example trace](https://smith.langchain.com/public/0a2f53f6-eaea-4092-b86b-c4e0a41998bc/r)
>
> Open a public LangSmith run for this example.

Behavior:

* The tool executes normally and its output is wrapped in a `ToolMessage`.
* The agent stops looping and returns the tool's output as the final response, bypassing any additional model call.
* **Multiple parallel tool calls:** When the model calls several tools in one step, all of them execute first. After all tools finish, the agent routes to `END` only if **every** tool in that batch has `return_direct=True`. The final response includes the `ToolMessage` outputs of every tool that was called in that step.

Use this when:

* The tool's output is the complete, user-ready answer (for example, a lookup that returns a ready-to-display result).
* You want to avoid an extra model call when no additional reasoning is needed.
* You need deterministic, unmodified output: the model cannot rephrase, summarize, or act on the tool result.

> [!WARNING]
>
> Because the model does not process the tool's output, `return_direct=True` is not suitable for tools whose results require further reasoning, summarization, or chaining with other tool calls.

> [!WARNING]
>
> **Mixed parallel calls:** If the model calls a `return_direct=True` tool alongside tools that do not have `return_direct=True`, the agent does **not** exit after that step. It routes back to the model with every `ToolMessage` from the batch, so the model can reason over all results. `return_direct` only short-circuits the loop when every tool call in the step has `return_direct=True`.

#### Return a Command with return\_direct

A tool with `return_direct=True` can also return a [`Command`](https://reference.langchain.com/python/langgraph/types/Command) to update graph state before the agent exits. Unlike a plain return value, a `Command` is not automatically converted into a `ToolMessage`. When the `Command` targets the current graph (`graph` is not set or is `None`), include a `ToolMessage` in `Command.update` matching the tool call's `tool_call_id`. Omitting it causes `ToolNode` to raise a `ValueError`, because every `AIMessage` tool call must have a corresponding `ToolMessage` in the message history.

```python
from langchain.messages import ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.types import Command


@tool(return_direct=True)
def fetch_and_store_order(order_id: str, runtime: ToolRuntime) -> Command:
    """Fetch order status and store it in state."""
    status = f"Order {order_id} is shipped and will arrive in 2 days."
    return Command(
        update={
            "last_order_status": status,
            # Must include a ToolMessage so the message history stays valid
            "messages": [
                ToolMessage(
                    content=status,
                    tool_call_id=runtime.tool_call_id,
                )
            ],
        }
    )
```

To write to a parent graph instead, set `graph=Command.PARENT`. In that case the `ToolMessage` requirement is lifted because execution leaves the current graph entirely.

### Error handling

Handle tool errors using LangChain agent [middleware](https://docs.langchain.com/oss/python/langchain/middleware.md) to retry failed tool calls or return custom error messages:

```python Google
from collections.abc import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest


@wrap_tool_call
def handle_tool_errors(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage],
) -> ToolMessage:
    """Convert tool exceptions into ToolMessages the model can handle."""
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({e})",
            tool_call_id=request.tool_call["id"],
        )


agent = create_agent(
    model="google_genai:gemini-4-hydrogen",
    tools=[],
    middleware=[handle_tool_errors],
)
```

```python OpenAI
from collections.abc import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest


@wrap_tool_call
def handle_tool_errors(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage],
) -> ToolMessage:
    """Convert tool exceptions into ToolMessages the model can handle."""
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({e})",
            tool_call_id=request.tool_call["id"],
        )


agent = create_agent(
    model="openai:gpt-6.1-sol",
    tools=[],
    middleware=[handle_tool_errors],
)
```

```python Anthropic
from collections.abc import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest


@wrap_tool_call
def handle_tool_errors(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage],
) -> ToolMessage:
    """Convert tool exceptions into ToolMessages the model can handle."""
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({e})",
            tool_call_id=request.tool_call["id"],
        )


agent = create_agent(
    model="anthropic:claude-sonnet-5",
    tools=[],
    middleware=[handle_tool_errors],
)
```

```python OpenRouter
from collections.abc import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest


@wrap_tool_call
def handle_tool_errors(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage],
) -> ToolMessage:
    """Convert tool exceptions into ToolMessages the model can handle."""
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({e})",
            tool_call_id=request.tool_call["id"],
        )


agent = create_agent(
    model="openrouter:z-ai/glm-5.2",
    tools=[],
    middleware=[handle_tool_errors],
)
```

```python Fireworks
from collections.abc import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest


@wrap_tool_call
def handle_tool_errors(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage],
) -> ToolMessage:
    """Convert tool exceptions into ToolMessages the model can handle."""
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({e})",
            tool_call_id=request.tool_call["id"],
        )


agent = create_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    tools=[],
    middleware=[handle_tool_errors],
)
```

```python Baseten
from collections.abc import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest


@wrap_tool_call
def handle_tool_errors(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage],
) -> ToolMessage:
    """Convert tool exceptions into ToolMessages the model can handle."""
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({e})",
            tool_call_id=request.tool_call["id"],
        )


agent = create_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[],
    middleware=[handle_tool_errors],
)
```

```python Ollama
from collections.abc import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest


@wrap_tool_call
def handle_tool_errors(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage],
) -> ToolMessage:
    """Convert tool exceptions into ToolMessages the model can handle."""
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({e})",
            tool_call_id=request.tool_call["id"],
        )


agent = create_agent(
    model="ollama:north-mini-code-1.0",
    tools=[],
    middleware=[handle_tool_errors],
)
```

### State injection

Tools access graph state through [`ToolRuntime`](https://reference.langchain.com/python/langchain/tools/#langchain.tools.ToolRuntime). See [Access context](#access-context) for state, context, store, and streaming APIs.

```python
from langchain.tools import tool, ToolRuntime

@tool
def get_message_count(runtime: ToolRuntime) -> str:
    """Get the number of messages in the conversation."""
    messages = runtime.state["messages"]
    return f"There are {len(messages)} messages."
```

For more details on accessing state, context, and long-term memory from tools, see [Access context](#access-context).

## Dynamic tool selection

With dynamic tools, the set of tools available to the agent is modified at runtime rather than defined all upfront. Not every tool is appropriate for every situation. Too many tools may overwhelm the model (overload context) and increase errors; too few limit capabilities. Dynamic tool selection enables adapting the available toolset based on authentication state, user permissions, feature flags, or conversation stage.

There are two approaches depending on whether tools are known ahead of time:

> [tab] Filtering pre-registered tools
>
> When all possible tools are known at agent creation time, you can pre-register them and dynamically filter which ones are exposed to the model based on state, permissions, or context.
>
> > [tab] State
> >
> > Enable advanced tools only after certain conversation milestones:
> >
> > ```python
> > from langchain.agents import create_agent
> > from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
> > from typing import Callable
> >
> > @wrap_model_call
> > def state_based_tools(
> >     request: ModelRequest,
> >     handler: Callable[[ModelRequest], ModelResponse]
> > ) -> ModelResponse:
> >     """Filter tools based on conversation State."""
> >     # Read from State: check if user has authenticated
> >     state = request.state
> >     is_authenticated = state.get("authenticated", False)
> >     message_count = len(state["messages"])
> >
> >     # Only enable sensitive tools after authentication
> >     if not is_authenticated:
> >         tools = [t for t in request.tools if t.name.startswith("public_")]
> >         request = request.override(tools=tools)
> >     elif message_count < 5:
> >         # Limit tools early in conversation
> >         tools = [t for t in request.tools if t.name != "advanced_search"]
> >         request = request.override(tools=tools)
> >
> >     return handler(request)
> >
> > agent = create_agent(
> >     model="gpt-6.1-sol",
> >     tools=[public_search, private_search, advanced_search],
> >     middleware=[state_based_tools]
> > )
> > ```
>
> > [tab] Store
> >
> > Filter tools based on user preferences or feature flags in Store:
> >
> > ```python
> > from dataclasses import dataclass
> > from langchain.agents import create_agent
> > from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
> > from typing import Callable
> > from langgraph.store.memory import InMemoryStore
> >
> > @dataclass
> > class Context:
> >     user_id: str
> >
> > @wrap_model_call
> > def store_based_tools(
> >     request: ModelRequest,
> >     handler: Callable[[ModelRequest], ModelResponse]
> > ) -> ModelResponse:
> >     """Filter tools based on Store preferences."""
> >     user_id = request.runtime.context.user_id
> >
> >     # Read from Store: get user's enabled features
> >     store = request.runtime.store
> >     feature_flags = store.get(("features",), user_id)
> >
> >     if feature_flags:
> >         enabled_features = feature_flags.value.get("enabled_tools", [])
> >         # Only include tools that are enabled for this user
> >         tools = [t for t in request.tools if t.name in enabled_features]
> >         request = request.override(tools=tools)
> >
> >     return handler(request)
> >
> > agent = create_agent(
> >     model="gpt-6.1-sol",
> >     tools=[search_tool, analysis_tool, export_tool],
> >     middleware=[store_based_tools],
> >     context_schema=Context,
> >     store=InMemoryStore()
> > )
> > ```
>
> > [tab] Runtime Context
> >
> > Filter tools based on user permissions from Runtime Context:
> >
> > ```python
> > from dataclasses import dataclass
> > from langchain.agents import create_agent
> > from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
> > from typing import Callable
> >
> > @dataclass
> > class Context:
> >     user_role: str
> >
> > @wrap_model_call
> > def context_based_tools(
> >     request: ModelRequest,
> >     handler: Callable[[ModelRequest], ModelResponse]
> > ) -> ModelResponse:
> >     """Filter tools based on Runtime Context permissions."""
> >     # Read from Runtime Context: get user role
> >     if request.runtime is None or request.runtime.context is None:
> >         # If no context provided, default to viewer (most restrictive)
> >         user_role = "viewer"
> >     else:
> >         user_role = request.runtime.context.user_role
> >
> >     if user_role == "admin":
> >         # Admins get all tools
> >         pass
> >     elif user_role == "editor":
> >         # Editors can't delete
> >         tools = [t for t in request.tools if t.name != "delete_data"]
> >         request = request.override(tools=tools)
> >     else:
> >         # Viewers get read-only tools
> >         tools = [t for t in request.tools if t.name.startswith("read_")]
> >         request = request.override(tools=tools)
> >
> >     return handler(request)
> >
> > agent = create_agent(
> >     model="gpt-6.1-sol",
> >     tools=[read_data, write_data, delete_data],
> >     middleware=[context_based_tools],
> >     context_schema=Context
> > )
> > ```
>
> This approach is best when:
>
> * All possible tools are known at compile/startup time
> * You want to filter based on permissions, feature flags, or conversation state
> * Tools are static but their availability is dynamic
>
> See [Dynamically selecting tools](../Middleware/Custom%20middleware.md#dynamically-selecting-tools) for more examples.

> [tab] Runtime tool registration
>
> When tools are discovered or created at runtime (e.g., loaded from an MCP server, generated based on user data, or fetched from a remote registry), you need to both register the tools and handle their execution dynamically.
>
> This requires two middleware hooks:
>
> 1. `wrap_model_call` - Add the dynamic tools to the request
> 2. `wrap_tool_call` - Handle execution of the dynamically added tools
>
> ```python
> from langchain.tools import tool
> from langchain.agents import create_agent
> from langchain.agents.middleware import AgentMiddleware, ModelRequest, ToolCallRequest
>
> # A tool that will be added dynamically at runtime
> @tool
> def calculate_tip(bill_amount: float, tip_percentage: float = 20.0) -> str:
>     """Calculate the tip amount for a bill."""
>     tip = bill_amount * (tip_percentage / 100)
>     return f"Tip: ${tip:.2f}, Total: ${bill_amount + tip:.2f}"
>
> class DynamicToolMiddleware(AgentMiddleware):
>     """Middleware that registers and handles dynamic tools."""
>
>     def wrap_model_call(self, request: ModelRequest, handler):
>         # Add dynamic tool to the request
>         # This could be loaded from an MCP server, database, etc.
>         updated = request.override(tools=[*request.tools, calculate_tip])
>         return handler(updated)
>
>     def wrap_tool_call(self, request: ToolCallRequest, handler):
>         # Handle execution of the dynamic tool
>         if request.tool_call["name"] == "calculate_tip":
>             return handler(request.override(tool=calculate_tip))
>         return handler(request)
>
> agent = create_agent(
>     model="gpt-6.1-sol",
>     tools=[get_weather],  # Only static tools registered here
>     middleware=[DynamicToolMiddleware()],
> )
>
> # The agent can now use both get_weather AND calculate_tip
> result = agent.invoke({
>     "messages": [{"role": "user", "content": "Calculate a 20% tip on $85"}]
> })
> ```
>
> This approach is best when:
>
> * Tools are discovered at runtime (e.g., from an MCP server)
>
> * Tools are generated dynamically based on user data or configuration
>
> * You're integrating with external tool registries
>
> > [!NOTE]
> >
> > The `wrap_tool_call` hook is required for runtime-registered tools because the agent needs to know how to execute tools that weren't in the original tool list. Without it, the agent won't know how to invoke the dynamically added tool.

## Headless tools

Some tools should run **where your user's app runs** (typically the browser), not inside the process. **Headless tools** are tool definitions, which include the name, description, and argument schema, that you register on the **server** with your agent. The **implementation** is registered only on the **client** and executed after a short interrupt/resume handshake.

This is different from ordinary tools whose function body runs on the server, and from [server-side tool use](#server-side-tool-use) where the model provider executes built-in tools remotely.

### When to use headless tools

Use them when the work depends on the **environment, device, or UI** that only exists on the client. For example:

* **Browser APIs:** Geolocation, IndexedDB, Clipboard, Canvas 2D, file pickers, Battery API, etc.
* **Privacy and locality:** Data stays on the device (for example, local “memory” in IndexedDB).
* **Latency:** No extra server round trip for purely local operations.
* **Structured, safe effects:** Prefer many small, typed tools (for example one tool per canvas primitive) instead of sending arbitrary code to `eval`.

### How the pattern works

In both runtimes, the model sees a normal tool it can call, but the actual execution happens outside the server process.

1. **Define** a headless tool with `tool(name=..., description=..., args_schema=...)` from `langchain.tools`. A headless tool is schema-only, with no in-process implementation.
2. **Register** that tool with `create_agent` or your LangGraph graph so the model can call it normally.
3. **Handle** the interrupt payload when the tool is invoked. Instead of running locally, the graph pauses with a payload shaped like `{"type": "tool", "tool_call": {"id", "name", "args"}}`.
4. **Resume** the graph after your app, another service, or a human step performs the action. For browser-based flows, you can mirror the schema in the frontend and attach `.implement(...)` there.

> [!NOTE]
>
> If you call `tool(...)` in Python with only `name`, `description`, and `args_schema`, LangChain returns a `HeadlessTool`. There is no `.implement()` API on the Python side.

When the model issues a tool call for one of these tools, the run **interrupts** instead of executing the tool locally. Your app can inspect the payload, perform the action in the right environment (for example a browser, another service, or a human review step), then **resume** the graph with the tool result. When you use the supported JS SDK hooks, they can detect headless-tool interrupts, run the matching client implementation, and submit the resume command for you.

Use the optional **`onTool`** callback to observe lifecycle events (`start`, `success`, `error`) for UI feedback such as spinners or toasts.

> [card] [Headless tools frontend pattern](../Frontend/Patterns/Headless%20tools.md)
>
> See an end-to-end example of schema-only tools executed in the client with `useStream`.

## Prebuilt tools

LangChain provides a large collection of prebuilt tools and toolkits for common tasks like web search, code interpretation, database access, and more. These ready-to-use tools can be directly integrated into your agents without writing custom code.

See the [tools and toolkits](https://docs.langchain.com/oss/python/integrations/tools.md) integration page for a complete list of available tools organized by category.

## Tools from MCP servers

[Model Context Protocol (MCP)](https://modelcontextprotocol.io) is an open protocol that standardizes how applications expose tools to language models. Rather than hand-authoring a tool, you connect to an MCP server and adapt the tools it advertises into LangChain tools, ready to pass to an agent like any other tool.

[`MCPAdapter`](https://reference.langchain.com/python/langchain/mcp/adapter/MCPAdapter) discovers a server's tools and converts them into LangChain tools. Open the adapter, call `list_tools()`, and hand the result to [`create_agent`](https://reference.langchain.com/python/langchain/agents/factory/create_agent):

```python
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter

async with MCPAdapter("https://example.com/mcp") as adapter:
    tools = await adapter.list_tools()
    agent = create_agent("claude-sonnet-4-6", tools)
```

> [!NOTE]
>
> The `langchain.mcp` namespace requires `langchain[mcp]>=1.4.0` and is in beta. The API may change.

For transports, authentication, multiple servers, and handling tool results, see [Model Context Protocol (MCP)](../Advanced%20usage/MCP/Model%20Context%20Protocol%20%28MCP%29.md).

## Server-side tool use

Some chat models feature built-in tools that are executed server-side by the model provider. These include capabilities like web search and code interpreters that don't require you to define or host the tool logic.

Refer to the individual [chat model integration pages](https://docs.langchain.com/oss/python/integrations/providers) and the [tool calling documentation](Models.md#server-side-tool-use) for details on enabling and using these built-in tools.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/tools.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
