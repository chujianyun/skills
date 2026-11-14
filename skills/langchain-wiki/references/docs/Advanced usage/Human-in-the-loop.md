# Human-in-the-loop

The Human-in-the-Loop (HITL) [middleware](../Middleware/Prebuilt%20middleware.md#human-in-the-loop) lets you add human oversight to agent tool calls.
When a model proposes an action that might require review—for example, writing to a file or executing SQL—the middleware can pause execution and wait for a decision.

It does this by checking each tool call against a configurable policy. If intervention is needed, the middleware issues an [interrupt](https://reference.langchain.com/python/langgraph/types/interrupt) that halts execution. The graph state is saved using LangGraph's [persistence layer](https://docs.langchain.com/oss/python/langgraph/persistence.md), so execution can pause safely and resume later.

A human decision then determines what happens next: the action can be approved as-is (`approve`), modified before running (`edit`), rejected with feedback (`reject`), or responded to directly (`respond`) for "ask user" style tools.

## Interrupt decision types

The [middleware](../Middleware/Prebuilt%20middleware.md#human-in-the-loop) defines four built-in ways a human can respond to an interrupt:

| Decision Type | Description | Example Use Case |
| - | - | - |
| ✅ `approve` | Execute the tool with the original arguments as proposed by the agent. | Send an email draft exactly as written |
| ✏️ `edit` | Modify the tool arguments before execution. | Change the recipient before sending an email |
| ❌ `reject` | Skip executing this tool call entirely and return rejection feedback to the agent. | Deny file deletion and explain why |
| 💬 `respond` | Return the human's message directly as a synthetic tool result, skipping execution, for "ask user" style tools. | Answer an `"ask_user"` prompt with a direct reply |

The available decision types for each tool depend on the policy you configure in `interrupt_on`.

When multiple tool calls are paused at the same time, each action requires a separate decision.

In the default batched mode, provide decisions in the same order as the actions appear in the interrupt request. In [per-call mode](#pause-once-per-tool-call), each tool call has its own interrupt and takes one decision.

Use `reject` when the human is denying the requested action. Use `respond` only when the human is acting as the tool, such as answering an `ask_user` prompt. Do not use `respond` to deny side-effecting tools, because its message is treated as a successful tool result.

> [!TIP]
>
> When **editing** tool arguments, make changes conservatively. Significant modifications to the original arguments may cause the model to re-evaluate its approach and potentially execute the tool multiple times or take unexpected actions.

## Configuring interrupts

To use HITL, add the [middleware](../Middleware/Prebuilt%20middleware.md#human-in-the-loop) to the agent's `middleware` list when creating the agent.

You configure it with a mapping of tool actions to the decision types that are allowed for each action. The middleware will interrupt execution when a tool call matches an action in the mapping.

This example uses the default batched mode. To pause once per tool call, see [Set the interrupt mode](#set-the-interrupt-mode).

```python
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware # [!code highlight]
from langgraph.checkpoint.memory import InMemorySaver # [!code highlight]


agent = create_agent(
    model="gpt-6.1-sol",
    tools=[write_file, execute_sql, read_data],
    middleware=[
        HumanInTheLoopMiddleware( # [!code highlight]
            interrupt_on={
                "write_file": True,  # All decisions (approve, edit, reject, respond) allowed
                "execute_sql": {"allowed_decisions": ["approve", "reject"]},  # No editing allowed
                "read_data": False, # Safe operation, no approval needed
            },
            # Prefix for interrupt messages - combined with tool name and args to form the full message
            # e.g., "Tool execution pending approval: execute_sql with query='DELETE FROM...'"
            # Individual tools can override this by specifying a "description" in their interrupt config
            description_prefix="Tool execution pending approval",
        ),
    ],
    # Human-in-the-loop requires checkpointing to handle interrupts.
    # In production, use a persistent checkpointer like AsyncPostgresSaver or MongoDBSaver.
    checkpointer=InMemorySaver(),  # [!code highlight]
)
```

> [!NOTE]
>
> You must configure a checkpointer to persist the graph state across interrupts.
> In production, use a persistent checkpointer like [`AsyncPostgresSaver`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.postgres.aio.AsyncPostgresSaver) or [`MongoDBSaver`](https://pypi.org/project/langgraph-checkpoint-mongodb/). For testing or prototyping, use [`InMemorySaver`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.memory.InMemorySaver).
>
> When invoking the agent, pass a `config` that includes the **thread ID** to associate execution with a conversation thread.
> See the [LangGraph interrupts documentation](https://docs.langchain.com/oss/python/langgraph/interrupts.md) for details.

> [accordion] Configuration options
>
> **interrupt\_on** `dict` *required*
>
> Mapping of tool names to approval configs. Values can be `True` (interrupt with default config), `False` (auto-approve), or an `InterruptOnConfig` object.
>
> **description\_prefix** `string` (default: Tool execution requires approval)
>
> Prefix for action request descriptions
>
> **interrupt\_mode** `string` (default: batched)
>
> How the agent pauses for review. `"batched"` raises one interrupt per model turn, answered with an ordered list. `"per_call"` raises one interrupt per gated call, answered by interrupt ID. `"per_call"` requires `langchain>=1.4.6`. See [Set the interrupt mode](#set-the-interrupt-mode).
>
> **edit\_notice** `string | None`
>
> Text added before the result of a call that a reviewer replaced with an `edit` decision, so the model knows the call changed. Defaults to a note that a human reviewer replaced the call. Pass `None` to add nothing.
>
> **`InterruptOnConfig` options:**
>
> **allowed\_decisions** `list[string]`
>
> List of allowed decisions: `'approve'`, `'edit'`, `'reject'`, or `'respond'`
>
> **description** `string | callable`
>
> Static string or callable function for custom description
>
> **when** `callable`
>
> Optional predicate that receives a [ToolCallRequest](https://reference.langchain.com/python/langgraph.prebuilt/tool_node/ToolCallRequest) and returns `True` to interrupt or `False` to auto-approve. Use it to gate interrupts on a call's arguments. Requires `langchain>=1.3.3`.

## Conditional interrupts

By default, every tool call listed in `interrupt_on` pauses for review. To pause only some calls, add a `when` predicate to a tool's `InterruptOnConfig`. The predicate receives a `ToolCallRequest` and returns `True` to interrupt or `False` to auto-approve, so you can gate on the tool's arguments.

> [!NOTE]
>
> Conditional interrupts require `langchain>=1.3.3`.

```python
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware, ToolCallRequest
from langgraph.checkpoint.memory import InMemorySaver


def writes_outside_workspace(request: ToolCallRequest) -> bool:
    """Pause writes to paths outside the workspace directory."""
    path = request.tool_call["args"].get("path", "")
    return not path.startswith("/workspace/")


def is_write_query(request: ToolCallRequest) -> bool:
    """Pause SQL that isn't a read-only SELECT."""
    query = request.tool_call["args"].get("query", "")
    return not query.lstrip().upper().startswith("SELECT")


agent = create_agent(
    model="gpt-6.1-sol",
    tools=[write_file, execute_sql, read_data],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "write_file": {
                    "allowed_decisions": ["approve", "edit", "reject"],
                    "when": writes_outside_workspace,
                },
                "execute_sql": {
                    "allowed_decisions": ["approve", "reject"],
                    "when": is_write_query,
                },
            },
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

When the `when` predicate returns `False`, the call runs without interrupting. When it returns `True`, or when you omit `when`, the call pauses as usual. Calls that evaluate to `False` never pause, so a reviewer only sees the actions that need a decision.

The predicate runs again when the agent resumes, so it must return the same result for the same call. If it returns `False` on resume, the tool runs and the reviewer's answer is ignored, even a `reject`. In batched mode, if the result changes for only some of the calls, the middleware raises a `ValueError`.

## Set the interrupt mode

The middleware pauses in one of two modes, set with `interrupt_mode`:

* **`"per_call"`**: Each tool call that needs review raises its own interrupt as it starts. Each interrupt carries a [`response_schema`](https://docs.langchain.com/oss/python/langgraph/interrupts#define-an-interrupt-response-schema) of the answers it accepts. You answer it with one decision, keyed by the interrupt ID.
* **`"batched"`** (default): One interrupt per model turn lists every call that needs review. You answer with a list of decisions in the same order.

Use per-call mode for new agents. LangChain plans to make it the default in the next major release. For a side-by-side comparison and the problems per-call mode solves, see the [human-in-the-loop overview](https://docs.langchain.com/oss/python/concepts/human-in-the-loop.md).

## Pause once per tool call

> [!NOTE]
>
> Per-call interrupts require `langchain>=1.4.6`.

Set `interrupt_mode="per_call"` to review each tool call separately. This agent gates `write_file` and `execute_sql`, and lets `read_data` run without review:

```python Google
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver


@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file."""
    return f"Wrote {len(content)} characters to {path}"


@tool
def execute_sql(query: str) -> str:
    """Run a SQL query."""
    return "Deleted 42 rows"


@tool
def read_data(table: str) -> str:
    """Read rows from a table."""
    return f"3 rows from {table}"


agent = create_agent(
    model="google_genai:gemini-4-hydrogen",
    tools=[write_file, execute_sql, read_data],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "write_file": True,
                "execute_sql": {"allowed_decisions": ["approve", "reject"]},
                "read_data": False,
            },
            interrupt_mode="per_call",  # [!code highlight]
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

```python OpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver


@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file."""
    return f"Wrote {len(content)} characters to {path}"


@tool
def execute_sql(query: str) -> str:
    """Run a SQL query."""
    return "Deleted 42 rows"


@tool
def read_data(table: str) -> str:
    """Read rows from a table."""
    return f"3 rows from {table}"


agent = create_agent(
    model="openai:gpt-6.1-sol",
    tools=[write_file, execute_sql, read_data],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "write_file": True,
                "execute_sql": {"allowed_decisions": ["approve", "reject"]},
                "read_data": False,
            },
            interrupt_mode="per_call",  # [!code highlight]
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

```python Anthropic
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver


@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file."""
    return f"Wrote {len(content)} characters to {path}"


@tool
def execute_sql(query: str) -> str:
    """Run a SQL query."""
    return "Deleted 42 rows"


@tool
def read_data(table: str) -> str:
    """Read rows from a table."""
    return f"3 rows from {table}"


agent = create_agent(
    model="anthropic:claude-sonnet-5",
    tools=[write_file, execute_sql, read_data],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "write_file": True,
                "execute_sql": {"allowed_decisions": ["approve", "reject"]},
                "read_data": False,
            },
            interrupt_mode="per_call",  # [!code highlight]
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

```python OpenRouter
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver


@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file."""
    return f"Wrote {len(content)} characters to {path}"


@tool
def execute_sql(query: str) -> str:
    """Run a SQL query."""
    return "Deleted 42 rows"


@tool
def read_data(table: str) -> str:
    """Read rows from a table."""
    return f"3 rows from {table}"


agent = create_agent(
    model="openrouter:z-ai/glm-5.2",
    tools=[write_file, execute_sql, read_data],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "write_file": True,
                "execute_sql": {"allowed_decisions": ["approve", "reject"]},
                "read_data": False,
            },
            interrupt_mode="per_call",  # [!code highlight]
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

```python Fireworks
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver


@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file."""
    return f"Wrote {len(content)} characters to {path}"


@tool
def execute_sql(query: str) -> str:
    """Run a SQL query."""
    return "Deleted 42 rows"


@tool
def read_data(table: str) -> str:
    """Read rows from a table."""
    return f"3 rows from {table}"


agent = create_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    tools=[write_file, execute_sql, read_data],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "write_file": True,
                "execute_sql": {"allowed_decisions": ["approve", "reject"]},
                "read_data": False,
            },
            interrupt_mode="per_call",  # [!code highlight]
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

```python Baseten
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver


@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file."""
    return f"Wrote {len(content)} characters to {path}"


@tool
def execute_sql(query: str) -> str:
    """Run a SQL query."""
    return "Deleted 42 rows"


@tool
def read_data(table: str) -> str:
    """Read rows from a table."""
    return f"3 rows from {table}"


agent = create_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[write_file, execute_sql, read_data],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "write_file": True,
                "execute_sql": {"allowed_decisions": ["approve", "reject"]},
                "read_data": False,
            },
            interrupt_mode="per_call",  # [!code highlight]
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

```python Ollama
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver


@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file."""
    return f"Wrote {len(content)} characters to {path}"


@tool
def execute_sql(query: str) -> str:
    """Run a SQL query."""
    return "Deleted 42 rows"


@tool
def read_data(table: str) -> str:
    """Read rows from a table."""
    return f"3 rows from {table}"


agent = create_agent(
    model="ollama:north-mini-code-1.0",
    tools=[write_file, execute_sql, read_data],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "write_file": True,
                "execute_sql": {"allowed_decisions": ["approve", "reject"]},
                "read_data": False,
            },
            interrupt_mode="per_call",  # [!code highlight]
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

### Read the interrupts

When the model calls all three tools in one turn, `read_data` runs right away. The two gated calls each raise an interrupt:

```python
config = {"configurable": {"thread_id": "1"}}
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Archive old orders, then delete them."}]},
    config=config,
    version="v2",
)

# One interrupt per gated tool call, in no fixed order
for interrupt in result.interrupts:
    print(interrupt.value)
# > {'type': 'tool_approval', 'tool_call_id': 'call_write', 'name': 'write_file', 'args': {'path': 'orders_archive.csv', 'content': 'id,total\n1,20\n'}, 'description': "Tool execution requires approval\n\nTool: write_file\nArgs: {'path': 'orders_archive.csv', 'content': 'id,total\\n1,20\\n'}"}
# > {'type': 'tool_approval', 'tool_call_id': 'call_sql', 'name': 'execute_sql', 'args': {'query': "DELETE FROM orders WHERE created_at < '2025-01-01'"}, 'description': 'Tool execution requires approval\n\nTool: execute_sql\nArgs: {\'query\': "DELETE FROM orders WHERE created_at < \'2025-01-01\'"}'}
```

Each interrupt value has `type: "tool_approval"`, so a client can tell it apart from other interrupts. The `tool_call_id`, `name`, and `args` fields identify the call under review.

### Read the response schema

Each interrupt also carries a `response_schema`: a JSON schema with one branch per decision the tool allows, matched on the decision's `type`. The `execute_sql` schema has `approve` and `reject` branches. The `write_file` schema has all four. For a tool that allows one decision, `response_schema` is that decision's schema alone, with no `oneOf`.

Each tab shows one `write_file` branch, an answer that matches it, and the [ToolMessage](https://reference.langchain.com/python/langchain-core/messages/tool/ToolMessage) the model receives. For readability, the branches below expand `$ref` definitions in place and omit the `title` and `description` fields.

> [tab] approve
>
> Run the call as proposed.
>
> ```json Schema branch
> {"properties": {"type": {"const": "approve", "type": "string"}}, "required": ["type"], "type": "object"}
> ```
>
> ```python Answer
> {"type": "approve"}
> ```
>
> ```text Model receives
> Wrote 14 characters to orders_archive.csv
> ```

> [tab] edit
>
> Run the call with new arguments. `edited_action.name` must stay `write_file`, and `edited_action.args` must match `write_file`'s argument schema. Arguments the tool does not declare are ignored, as they are when the model sends them.
>
> ```json Schema branch
> {
>   "properties": {
>     "type": {"const": "edit", "type": "string"},
>     "edited_action": {
>       "properties": {
>         "name": {"const": "write_file", "type": "string"},
>         "args": {
>           "properties": {
>             "path": {"type": "string"},
>             "content": {"type": "string"}
>           },
>           "required": ["path", "content"],
>           "type": "object"
>         }
>       },
>       "required": ["name", "args"],
>       "type": "object"
>     }
>   },
>   "required": ["type", "edited_action"],
>   "type": "object"
> }
> ```
>
> ```python Answer
> {
>     "type": "edit",
>     "edited_action": {
>         "name": "write_file",
>         "args": {"path": "archive/orders_2024.csv", "content": "id,total\n1,20\n"},
>     },
> }
> ```
>
> The model receives the tool's result after a note that a reviewer replaced the call. Set `edit_notice` on the middleware to change the note, or pass `None` to remove it.
>
> ```text Model receives
> Note: a human reviewer replaced this tool call before it ran. The call recorded in your message is the one you produced, not the one that executed. This was intentional and authorized. Do not re-issue your original call. Executed instead: write_file with arguments {"path": "archive/orders_2024.csv", "content": "id,total\n1,20\n"}.
>
> Tool response:
> Wrote 14 characters to archive/orders_2024.csv
> ```

> [tab] reject
>
> Skip the call. The `message` is optional and tells the model why.
>
> ```json Schema branch
> {"properties": {"type": {"const": "reject", "type": "string"}, "message": {"type": "string"}}, "required": ["type"], "type": "object"}
> ```
>
> ```python Answer
> {"type": "reject", "message": "Write to the archive/ folder instead."}
> ```
>
> ```text Model receives (error status)
> User rejected the tool call for `write_file` with reason: Write to the archive/ folder instead.
> ```

> [tab] respond
>
> Skip the call and answer in place of the tool. The `message` is required. The model receives it as a successful tool result, so use `reject` to deny a call.
>
> ```json Schema branch
> {"properties": {"type": {"const": "respond", "type": "string"}, "message": {"type": "string"}}, "required": ["type", "message"], "type": "object"}
> ```
>
> ```python Answer
> {"type": "respond", "message": "Saved orders_archive.csv to the shared drive myself."}
> ```
>
> ```text Model receives
> Saved orders_archive.csv to the shared drive myself.
> ```

### Resume each call by ID

Answer each interrupt with one decision, keyed by its ID:

```python
from langgraph.types import Command

decisions = {}
for interrupt in result.interrupts:
    if interrupt.value["name"] == "execute_sql":
        decisions[interrupt.id] = {
            "type": "reject",
            "message": "Archive the rows before deleting them.",
        }
    else:
        decisions[interrupt.id] = {"type": "approve"}

result = agent.invoke(Command(resume=decisions), config=config, version="v2")
```

You can also answer interrupts one at a time. An interrupt you do not answer stays pending, and its tool runs once it gets an answer.

> [!WARNING]
>
> If one of several answers sent together is invalid, the tools for the others can run while their interrupts still show as pending. Answering them again runs those tools twice. Check answers against `response_schema` before you send them together, or send one at a time.

### Correct an invalid answer

LangGraph checks each answer against the interrupt's `response_schema` before it saves the answer. An invalid answer raises a `ValidationError` and nothing is saved, so you can send a corrected answer to the same interrupt ID. Here, the edit leaves out `content`:

```python
from pydantic import ValidationError

write_file_interrupt = next(
    interrupt for interrupt in result.interrupts if interrupt.value["name"] == "write_file"
)
edit = {
    "type": "edit",
    "edited_action": {"name": "write_file", "args": {"path": "archive/orders_2024.csv"}},
}

try:
    agent.invoke(Command(resume={write_file_interrupt.id: edit}), config=config, version="v2")
except ValidationError as error:
    for problem in error.errors():
        print(".".join(str(part) for part in problem["loc"]), problem["msg"])
# > edit.edited_action.args.content Field required

# Nothing was saved, so answer the same interrupt again
edit["edited_action"]["args"]["content"] = "id,total\n1,20\n"
result = agent.invoke(
    Command(resume={write_file_interrupt.id: edit}), config=config, version="v2"
)
```

Each error names the field that failed, so you can show it to the reviewer. For a tool whose arguments are a raw JSON schema instead of a Pydantic model, `response_schema` shows the arguments, but LangGraph does not check edits against them.

### Order middleware for per-call review

In per-call mode, the review happens as the tool call starts, inside the tool-call middleware chain:

* List `HumanInTheLoopMiddleware` before tool retry or error-handling middleware, such as [ToolRetryMiddleware](https://reference.langchain.com/python/langchain/agents/middleware/tool_retry/ToolRetryMiddleware) and [ToolErrorMiddleware](https://reference.langchain.com/python/langchain/agents/middleware/tool_error/ToolErrorMiddleware), so it wraps them. Otherwise a retried call asks the reviewer again, and an invalid answer is retried or returned to the model as a tool error.
* When the agent resumes, middleware listed before `HumanInTheLoopMiddleware` runs again up to the pause, so it must not have side effects before it calls its handler. The tool runs only after the answer.
* A [`when` predicate](#conditional-interrupts) runs as each call starts, so the [ToolCallRequest](https://reference.langchain.com/python/langgraph.prebuilt/tool_node/ToolCallRequest) it receives includes the tool.

## Responding to interrupts

When you invoke the agent, it runs until it either completes or an interrupt is raised. An interrupt is triggered when a tool call matches the policy you configured in `interrupt_on`. With `version="v2"`, the result is a `GraphOutput` with an `interrupts` attribute containing the actions that require review. You can then present those actions to a reviewer and resume execution once decisions are provided.

The examples in this section and the decision types below use the default batched mode. For per-call mode, see [Pause once per tool call](#pause-once-per-tool-call).

```python
from langgraph.types import Command

# Human-in-the-loop leverages LangGraph's persistence layer.
# You must provide a thread ID to associate the execution with a conversation thread,
# so the conversation can be paused and resumed (as is needed for human review).
config = {"configurable": {"thread_id": "some_id"}} # [!code highlight]
# Run the graph until the interrupt is hit.
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Delete old records from the database",
            }
        ]
    },
    config=config, # [!code highlight]
    version="v2", # [!code highlight]
)

# result is a GraphOutput with .value and .interrupts
print(result.interrupts)  # [!code highlight]
# > (
# >    Interrupt(
# >       value={
# >          'action_requests': [
# >             {
# >                'name': 'execute_sql',
# >                'args': {'query': 'DELETE FROM records WHERE created_at < NOW() - INTERVAL \'30 days\';'},
# >                'description': 'Tool execution pending approval\n\nTool: execute_sql\nArgs: {...}'
# >             }
# >          ],
# >          'review_configs': [
# >             {
# >                'action_name': 'execute_sql',
# >                'allowed_decisions': ['approve', 'reject']
# >             }
# >          ]
# >       }
# >    ),
# > )


# Resume with approval decision
agent.invoke(
    Command( # [!code highlight]
        resume={"decisions": [{"type": "approve"}]}  # or "reject" [!code highlight]
    ), # [!code highlight]
    config=config, # Same thread ID to resume the paused conversation
    version="v2",
)
```

### Decision types

> [tab] approve
>
> Use `approve` to approve the tool call as-is and execute it without changes.
>
> ```python
> agent.invoke(
>     Command(
>         # Decisions are provided as a list, one per action under review.
>         # The order of decisions must match the order of actions
>         # in the interrupt request.
>         resume={
>             "decisions": [
>                 {
>                     "type": "approve",
>                 }
>             ]
>         }
>     ),
>     config=config,  # Same thread ID to resume the paused conversation
>     version="v2",
> )
> ```

> [tab] edit
>
> Use `edit` to modify the tool call before execution.
> Provide the edited action with the new tool name and arguments.
>
> ```python
> agent.invoke(
>     Command(
>         # Decisions are provided as a list, one per action under review.
>         # The order of decisions must match the order of actions
>         # in the interrupt request.
>         resume={
>             "decisions": [
>                 {
>                     "type": "edit",
>                     # Edited action with tool name and args
>                     "edited_action": {
>                         # Tool name to call.
>                         # Will usually be the same as the original action.
>                         "name": "new_tool_name",
>                         # Arguments to pass to the tool.
>                         "args": {"key1": "new_value", "key2": "original_value"},
>                     }
>                 }
>             ]
>         }
>     ),
>     config=config,  # Same thread ID to resume the paused conversation
>     version="v2",
> )
> ```
>
> > [!TIP]
> >
> > When **editing** tool arguments, make changes conservatively. Significant modifications to the original arguments may cause the model to re-evaluate its approach and potentially execute the tool multiple times or take unexpected actions.

> [tab] reject
>
> Use `reject` to deny the tool call and provide feedback instead of execution. The tool is not executed.
>
> ```python
> agent.invoke(
>     Command(
>         # Decisions are provided as a list, one per action under review.
>         # The order of decisions must match the order of actions
>         # in the interrupt request.
>         resume={
>             "decisions": [
>                 {
>                     "type": "reject",
>                     # Optional: explain why the action was rejected
>                     # and whether the agent should retry a different approach.
>                     "message": "User rejected this action. Do not retry this tool call.",
>                 }
>             ]
>         }
>     ),
>     config=config,  # Same thread ID to resume the paused conversation
>     version="v2",
> )
> ```
>
> The `message` is added to the conversation as feedback to help the agent understand why the action was rejected and what it should do instead. When you omit `message`, the middleware uses a default rejection message that tells the model the tool was not executed and not to retry the same tool call unless the user asks. For side-effecting tools, provide a domain-specific message that is explicit about whether the agent should abandon the action, ask a follow-up question, or try a safer alternative.

> [tab] respond
>
> Use `respond` for "ask user" style tools where the tool's real implementation is the human's reply. The `message` content is returned directly as the tool result; the tool itself is not executed.
>
> ```python
> agent.invoke(
>     Command(
>         # Decisions are provided as a list, one per action under review.
>         # The order of decisions must match the order of actions
>         # in the interrupt request.
>         resume={
>             "decisions": [
>                 {
>                     "type": "respond",
>                     # The human's reply, returned directly as the tool result
>                     "message": "Blue.",
>                 }
>             ]
>         }
>     ),
>     config=config,  # Same thread ID to resume the paused conversation
>     version="v2",
> )
> ```
>
> The `message` is returned to the agent as a successful `ToolMessage`. Use `respond` when the tool is intentionally a placeholder for human input, for example, an `ask_user` tool that prompts for clarification. Do not use `respond` to deny a proposed action, because it tells the model that the tool completed successfully.

***

### Multiple decisions

When multiple actions are under review, provide a decision for each action in the same order as they appear in the interrupt:

```python
{
    "decisions": [
        {"type": "approve"},
        {
            "type": "edit",
            "edited_action": {
                "name": "tool_name",
                "args": {"param": "new_value"}
            }
        },
        {
            "type": "reject",
            "message": "This action is not allowed"
        }
    ]
}
```

## Streaming with human-in-the-loop

You can stream real-time updates while the agent runs and handles interrupts using `stream_events()`. Use `stream.messages` to stream LLM tokens and `stream.values` to check agent state snapshots for interrupts.

```python
from langgraph.types import Command

config = {"configurable": {"thread_id": "some_id"}}

# Stream agent progress and LLM tokens until interrupt
stream = agent.stream_events(
    {"messages": [{"role": "user", "content": "Delete old records from the database"}]},
    config=config,
    version="v3",  # [!code highlight]
)
for message in stream.messages:  # [!code highlight]
    for token in message.text:  # [!code highlight]
        print(token, end="", flush=True)

# Check whether the run paused for human input
if stream.interrupted:  # [!code highlight]
    print(f"\n\nInterrupt: {stream.interrupts}")  # [!code highlight]

# Resume with streaming after human decision
stream = agent.stream_events(
    Command(resume={"decisions": [{"type": "approve"}]}),
    config=config,
    version="v3",  # [!code highlight]
)
for message in stream.messages:  # [!code highlight]
    for token in message.text:
        print(token, end="", flush=True)
```

In [per-call mode](#pause-once-per-tool-call), `stream.interrupts` holds one interrupt per gated tool call. Resume with a dict keyed by interrupt ID:

```python
decisions = {interrupt.id: {"type": "approve"} for interrupt in stream.interrupts}
stream = agent.stream_events(Command(resume=decisions), config=config, version="v3")
for message in stream.messages:
    for token in message.text:
        print(token, end="", flush=True)
```

See the [Streaming](../Core%20components/Streaming.md) guide for more details on stream modes.

## Execution lifecycle

The middleware defines an `after_model` hook that runs after the model generates a response but before any tool calls are executed:

1. The agent invokes the model to generate a response.
2. The middleware inspects the response for tool calls.
3. If any calls require human input, the middleware builds a [HITLRequest](https://reference.langchain.com/python/langchain/agents/middleware/human_in_the_loop/HITLRequest) with `action_requests` and `review_configs` and calls [interrupt](https://reference.langchain.com/python/langgraph/types/interrupt).
4. The agent waits for human decisions.
5. Based on the `HITLResponse` decisions, the middleware executes approved or edited calls, synthesizes [ToolMessage](https://reference.langchain.com/python/langchain-core/messages/tool/ToolMessage)'s for rejected calls, returns human replies directly as [ToolMessage](https://reference.langchain.com/python/langchain-core/messages/tool/ToolMessage)'s for `respond` decisions, and resumes execution.

In [per-call mode](#pause-once-per-tool-call), the `after_model` hook does nothing. The middleware instead pauses each gated call as it runs, with one [interrupt](https://reference.langchain.com/python/langgraph/types/interrupt) per call, and runs the tool once that call's decision arrives.

## Custom HITL logic

For more specialized workflows, you can build custom HITL logic directly using the [interrupt](https://reference.langchain.com/python/langgraph/types/interrupt) primitive and [middleware](https://docs.langchain.com/oss/python/langchain/middleware.md) abstraction.

Review the [execution lifecycle](#execution-lifecycle) above to understand how to integrate interrupts into the agent's operation.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/human-in-the-loop.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
