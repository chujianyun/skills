# Stream with the Functional API

> Emit custom progress from Functional API entrypoints, or read state snapshots from the values stream.

Stream from a Functional API [entrypoint](Functional%20API%20overview.md#entrypoint) in two ways. Custom data is a side channel: you push progress with a writer, then read `custom` chunks. Values are state snapshots the runtime records, including the entrypoint return value. You do not call a writer for values.

For concepts, see the [Functional API overview](Functional%20API%20overview.md). For messages and other typed projections, see [event streaming](../../Capabilities/Event%20streaming.md).

## Emit custom data

The Functional API uses the same stream as the [Graph API](../../Build%20with%20the%20Graph%20API/Graph%20API%20overview.md). Emit with a writer, then consume `custom` chunks. For stream modes, see [Streaming](../../Capabilities/Streaming.md).

```python
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.config import get_stream_writer
from langgraph.func import entrypoint

checkpointer = InMemorySaver()


@entrypoint(checkpointer=checkpointer)
def main(inputs: dict) -> int:
    writer = get_stream_writer()
    writer("Started processing")
    result = inputs["x"] * 2
    writer(f"Result is {result}")
    return result


config = {"configurable": {"thread_id": str(uuid7())}}

for chunk in main.stream({"x": 5}, config, stream_mode="custom"):
    print(chunk)
# Started processing
# Result is 10
```

> [card] [View example trace](https://smith.langchain.com/public/39b6ad85-7072-4290-8ae4-3f0f76c9c28a/r)
>
> Open a public LangSmith run for this example.

1. Import [`get_stream_writer`](https://reference.langchain.com/python/langgraph/config/get_stream_writer) from `langgraph.config`.
2. Call it inside the entrypoint to get a writer.
3. Emit custom data before and after the computation.
4. Call `stream(..., stream_mode="custom")` and iterate the chunks.

> [!WARNING]
>
> **Async with Python \< 3.11**
> In async code on Python \< 3.11, [`get_stream_writer`](https://reference.langchain.com/python/langgraph/config/get_stream_writer) does not work. Use the injectable `StreamWriter` parameter instead. See [Async with Python \< 3.11](../../Capabilities/Streaming.md#async).
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph.checkpoint.memory import InMemorySaver
> from langgraph.func import entrypoint
> from langgraph.types import StreamWriter
>
> checkpointer = InMemorySaver()
>
> @entrypoint(checkpointer=checkpointer)
> async def main(inputs: dict, writer: StreamWriter) -> int:  # [!code highlight]
>     writer("Started processing")
>     return inputs["x"] * 2
> ```

## Stream values

Reuse the `main` entrypoint from [Emit custom data](#emit-custom-data). Iterate `stream.values` for state snapshots. For messages and other projections, see [event streaming](../../Capabilities/Event%20streaming.md).

```python
values_config = {"configurable": {"thread_id": str(uuid7())}}
stream = main.stream_events({"x": 5}, config=values_config, version="v3")
for snapshot in stream.values:
    print(snapshot)
# 10
```

## See also

* [Functional API overview](Functional%20API%20overview.md)
* [Build checklist for the Functional API](Build%20checklist%20for%20the%20Functional%20API.md)
* [Event streaming](../../Capabilities/Event%20streaming.md)
* [Streaming](../../Capabilities/Streaming.md)
* [Add human-in-the-loop with the Functional API](Add%20human-in-the-loop%20with%20the%20Functional%20API.md)
