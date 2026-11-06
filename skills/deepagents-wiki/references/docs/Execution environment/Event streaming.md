# Event streaming

> Stream subagents, messages, tool calls, and final output from Deep Agents.

This page covers streaming concerns specific to Deep Agents—most importantly, streaming from delegated subagents via `stream.subagents`. For general agent streaming (`stream.messages`, `stream.values`, tool calls, custom updates), see [LangChain Event Streaming](https://docs.langchain.com/oss/python/langchain/event-streaming.md).

## Stream subagents

Deep Agents add a subagent projection on top of LangGraph streaming. Use `stream.subagents` when you want one stream handle per delegated `task` call. The projection is lightweight: it discovers subagent tasks first, and message, tool-call, and value streams are opened only when you access them on a subagent handle.

Each handle's `name` is the sub-agent's configured name: the `subagent_type` the coordinator passes when it calls the `task` tool. Deep Agents binds that name to the delegated run, so the same label you defined in your subagent specs is what you filter and route on in the stream.

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
stream = agent.stream_events(
    {
        "messages": [{"role": "user", "content": "Write me a haiku about the sea"}],
    },
    version="v3",
)

subagent_names: list[str] = []
for subagent in stream.subagents:
    print(subagent.name, subagent.path, subagent.status)

    for message in subagent.messages:
        print(message.text)

    subagent_names.append(subagent.name)
```

> [card] [View example trace](https://smith.langchain.com/public/cb99e8da-078c-4f7f-935f-cfee3499714d/r)
>
> Open a public LangSmith run for this example.

## Subagent stream fields

Each subagent stream exposes the same kinds of projections as the parent run, such as messages, tool calls, nested subagents, and final output. For the general parent-run streaming model, see [LangChain Event Streaming](https://docs.langchain.com/oss/python/langchain/event-streaming.md).

Python uses snake\_case projection names such as `tool_calls`. Each subagent stream can expose `.messages`, `.tool_calls`, `.values`, `.subagents`, and `.output`.

| Field | Description |
| - | - |
| `name` | Sub-agent name, taken from the `subagent_type` the coordinator selects in its `task` call. |
| `messages` | Messages emitted by the subagent. |
| `subagents` | Nested subagent invocations. |
| `output` | Final subagent state, or completion signal for the delegated task. |
| `path` | Namespace path for the subagent stream. |
| `status` | Lifecycle status such as `started`, `completed`, `failed`, or `interrupted`. |
| `tool_calls` | Tool calls scoped to the subagent. |

## Track subagent lifecycle

Use `stream.subagents` when you only need to show which subagents started and finished. You do not need to subscribe to message or value streams unless you access those projections on an individual subagent.

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
stream = agent.stream_events(input, version="v3")

running = 0
completed = 0
failed = 0

for subagent in stream.subagents:
    running += 1
    print(f"{subagent.name}: started")

    try:
        _ = subagent.output
        running -= 1
        completed += 1
        print(f"{subagent.name}: completed")
    except Exception:
        running -= 1
        failed += 1
        print(f"{subagent.name}: failed")
```

> [card] [View example trace](https://smith.langchain.com/public/932aef21-4019-4767-9632-246873501b39/r)
>
> Open a public LangSmith run for this example.

## Stream messages

Deep Agents can emit messages from the coordinator agent and from delegated subagents. Use `stream.messages` for top-level messages and `subagent.messages` for each delegated subagent.

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
stream = agent.stream_events(input, version="v3")

coordinator_messages: list[str] = []
for message in stream.messages:
    print("[coordinator]", message.text)
    coordinator_messages.append(message.text)

for subagent in stream.subagents:
    for message in subagent.messages:
        print(f"[{subagent.name}]", message.text)
```

> [card] [View example trace](https://smith.langchain.com/public/64198e44-f030-46ae-9cfc-a469b038ac89/r)
>
> Open a public LangSmith run for this example.

## Stream tool calls

Deep Agents expose tool calls at each level of the agent tree. Use the top-level `stream.tool_calls` for coordinator tools and each `subagent.tool_calls` for delegated work.

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
stream = agent.stream_events(input, version="v3")

coordinator_tool_names: list[str] = []
for call in stream.tool_calls:
    print("[coordinator tool]", call.tool_name, call.input)
    print(call.completed, call.error)
    coordinator_tool_names.append(call.tool_name)

for subagent in stream.subagents:
    for call in subagent.tool_calls:
        print(f"[{subagent.name} tool]", call.tool_name, call.input)
        for delta in call.output_deltas:
            print(delta, end="", flush=True)

        if call.completed and call.error is None:
            print(call.output)
        elif call.error is not None:
            print(call.error)
```

> [card] [View example trace](https://smith.langchain.com/public/09b3ae28-a609-4281-af99-c66f8b27a579/r)
>
> Open a public LangSmith run for this example.

## Stream nested work

You can recurse into a subagent stream to observe nested subagents, messages, and tool calls.

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
stream = agent.stream_events(input, version="v3")

subagent_names: list[str] = []
for subagent in stream.subagents:
    print(f"subagent {subagent.name}: {subagent.status}")

    for tool_call in subagent.tool_calls:
        print(f"{tool_call.tool_name}({tool_call.input})")
        for delta in tool_call.output_deltas:
            print(delta, end="", flush=True)

    for nested in subagent.subagents:
        print(f"nested subagent {nested.name}: {nested.status}")

    subagent_names.append(subagent.name)
```

> [card] [View example trace](https://smith.langchain.com/public/126270dd-d295-4081-87a5-6a73d795f3d7/r)
>
> Open a public LangSmith run for this example.

## Consume concurrently

Coordinator and subagent output often interleave. Consume projections concurrently when you need live UI updates.

For concurrent consumption in async code, use `astream_events` with `asyncio.gather`:

```py theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import asyncio

stream = await agent.astream_events(input, version="v3")

async def consume_coordinator():
    async for message in stream.messages:
        print("[coordinator]", await message.text)

async def consume_subagents():
    async for subagent in stream.subagents:
        async for message in subagent.messages:
            print(f"[{subagent.name}]", await message.text)

await asyncio.gather(consume_coordinator(), consume_subagents())
```

For synchronous code, use `stream.interleave(...)` instead:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
stream = agent.stream_events(input, version="v3")

for name, item in stream.interleave("messages", "subagents"):
    if name == "messages":
        print("[coordinator]", item.text)
    else:
        for message in item.messages:
            print(f"[{item.name}]", message.text)
```

> [card] [View example trace](https://smith.langchain.com/public/c640cc12-1348-4743-84f7-987613a000dc/r)
>
> Open a public LangSmith run for this example.

When you need exact arrival order across the coordinator and all subagents, iterate raw protocol events and use `namespace` to identify the source:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
stream = agent.stream_events(input, version="v3")

text_deltas: list[str] = []
for event in stream:
    if event.get("method") != "messages":
        continue

    payload = event["params"]["data"][0]
    if not isinstance(payload, dict):
        continue
    if payload.get("event") != "content-block-delta":
        continue

    block = payload.get("delta") or {}
    if block.get("type") == "text-delta":
        source = "subagent" if event["params"]["namespace"] else "coordinator"
        print(f"[{source}] {block['text']}")
        text_deltas.append(block["text"])
```

> [card] [View example trace](https://smith.langchain.com/public/6613bc7a-0726-4fd7-bf4a-67c7ebe8664d/r)
>
> Open a public LangSmith run for this example.

## Subagents versus subgraphs

`stream.subgraphs` shows graph execution structure. `stream.subagents` shows product-level Deep Agents task delegations. Use `stream.subagents` for user-facing UI because it hides internal graph nodes and exposes the subagent concept directly.

## Related

* [LangChain Event Streaming](https://docs.langchain.com/oss/python/langchain/event-streaming.md) covers general agent message and tool-call streaming concepts.
* [Subagent frontend streaming](../Frontend/Patterns/Subagent%20streaming.md) shows UI patterns that separate coordinator messages from subagent cards.
* [LangGraph Event Streaming](https://docs.langchain.com/oss/python/langgraph/event-streaming.md) covers the underlying graph streaming model.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/deepagents/event-streaming.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
