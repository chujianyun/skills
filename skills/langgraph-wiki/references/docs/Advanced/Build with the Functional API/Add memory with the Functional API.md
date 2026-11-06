# Add memory with the Functional API

> Use short-term checkpoints and long-term store memory in Functional API workflows.

Add memory to a Functional API [entrypoint](Functional%20API%20overview.md#entrypoint) with a [checkpointer](../../Capabilities/Persistence.md) and, optionally, a [store](../../Capabilities/Stores.md). Checkpoints persist state across invocations of the same `thread_id`. A store persists facts across thread IDs.

For concepts, see the [Functional API overview](Functional%20API%20overview.md). For Graph API memory recipes, see [Memory](../../Capabilities/Memory.md).

## Save state on a thread

Pass a checkpointer when you create the entrypoint. Identify each run with `thread_id`.

Add a keyword-only `previous` parameter. LangGraph sets it to the last value saved on this thread. On the first run it is `None`.

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint

checkpointer = InMemorySaver()


@entrypoint(checkpointer=checkpointer)
def accumulate(n: int, *, previous: int | None = None) -> int:
    previous = previous or 0
    return previous + n


config = {"configurable": {"thread_id": "1"}}
print(accumulate.invoke(1, config))  # 1
print(accumulate.invoke(2, config))  # 3
print(accumulate.invoke(3, config))  # 6
```

## Return a different saved value

Use [`entrypoint.final`](https://reference.langchain.com/python/langgraph/func/entrypoint/final) when the caller should receive one value and the next run should read another. `value` is returned to the caller.

`save` is what the next `previous` read sees.

For example, return a status or summary, and save the full internal state.

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint

checkpointer = InMemorySaver()


@entrypoint(checkpointer=checkpointer)
def accumulate(n: int, *, previous: int | None = None) -> entrypoint.final[int, int]:
    previous = previous or 0
    total = previous + n
    # Return the *previous* value to the caller but save the *new* total.
    return entrypoint.final(value=previous, save=total)


config = {"configurable": {"thread_id": "my-thread"}}

print(accumulate.invoke(1, config=config))  # 0
print(accumulate.invoke(2, config=config))  # 1
print(accumulate.invoke(3, config=config))  # 3
```

## Inspect checkpoints

View or delete checkpoints on the `accumulate` workflow from [Return a different saved value](#return-a-different-saved-value). `values` is the saved checkpoint (`save`), not the value returned to the caller.

### View thread state

```python
config = {
    "configurable": {
        "thread_id": "my-thread",  # [!code highlight]
        # optionally provide an ID for a specific checkpoint,
        # otherwise the latest checkpoint is shown
        # "checkpoint_id": "1f1c1826-2179-626c-8004-96dc43069e17"  # [!code highlight]
    }
}
print(accumulate.get_state(config))  # [!code highlight]
```

```
StateSnapshot(
    values=3,
    next=(),
    config={'configurable': {'thread_id': 'my-thread', 'checkpoint_ns': '', 'checkpoint_id': '1f1c1826-2179-626c-8004-96dc43069e17'}},
    metadata={'source': 'loop', 'step': 4, 'parents': {}},
    created_at='2026-10-06T12:35:16.081724+00:00',
    parent_config={'configurable': {'thread_id': 'my-thread', 'checkpoint_ns': '', 'checkpoint_id': '1f1c1826-2178-6682-8003-feda9f2ec8db'}},
    tasks=(),
    interrupts=()
)
```

### View thread history

```python
config = {"configurable": {"thread_id": "my-thread"}}  # [!code highlight]
history = list(accumulate.get_state_history(config))  # [!code highlight]
print(history[0])
```

```
StateSnapshot(
    values=3,
    next=(),
    config={'configurable': {'thread_id': 'my-thread', 'checkpoint_ns': '', 'checkpoint_id': '1f1c1826-2179-626c-8004-96dc43069e17'}},
    metadata={'source': 'loop', 'step': 4, 'parents': {}},
    created_at='2026-10-06T12:35:16.081724+00:00',
    parent_config={'configurable': {'thread_id': 'my-thread', 'checkpoint_ns': '', 'checkpoint_id': '1f1c1826-2178-6682-8003-feda9f2ec8db'}},
    tasks=(),
    interrupts=()
)
# ... earlier snapshots, including values=1, values=0, and values=None
```

### Delete checkpoints for a thread

```python
checkpointer.delete_thread("my-thread")
print(accumulate.get_state(config))
# StateSnapshot(values={}, next=(), config={'configurable': {'thread_id': 'my-thread'}}, ...)
```

## Build a chatbot with checkpoints

Keep the conversation on the thread. Return the model message to the caller, and save the full list for the next turn with `entrypoint.final`.

```python Google
from langchain_core.messages import BaseMessage
from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint, task
from langgraph.graph import add_messages

model = ChatAnthropic(model="google_genai:gemini-3.6-flash")


@task
def call_model(messages: list[BaseMessage]):
    response = model.invoke(messages)
    return response


checkpointer = InMemorySaver()


@entrypoint(checkpointer=checkpointer)
def workflow(inputs: list[BaseMessage], *, previous: list[BaseMessage] | None = None):
    if previous:
        inputs = add_messages(previous, inputs)

    response = call_model(inputs).result()
    return entrypoint.final(value=response, save=add_messages(inputs, response))


config = {"configurable": {"thread_id": "1"}}
input_message = {"role": "user", "content": "hi! I'm bob"}
print(workflow.invoke([input_message], config))
# -> AIMessage with a greeting that uses the name Bob

input_message = {"role": "user", "content": "what's my name?"}
print(workflow.invoke([input_message], config))
# -> AIMessage that answers "Bob"
```

```python OpenAI
from langchain_core.messages import BaseMessage
from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint, task
from langgraph.graph import add_messages

model = ChatAnthropic(model="openai:gpt-5.5")


@task
def call_model(messages: list[BaseMessage]):
    response = model.invoke(messages)
    return response


checkpointer = InMemorySaver()


@entrypoint(checkpointer=checkpointer)
def workflow(inputs: list[BaseMessage], *, previous: list[BaseMessage] | None = None):
    if previous:
        inputs = add_messages(previous, inputs)

    response = call_model(inputs).result()
    return entrypoint.final(value=response, save=add_messages(inputs, response))


config = {"configurable": {"thread_id": "1"}}
input_message = {"role": "user", "content": "hi! I'm bob"}
print(workflow.invoke([input_message], config))
# -> AIMessage with a greeting that uses the name Bob

input_message = {"role": "user", "content": "what's my name?"}
print(workflow.invoke([input_message], config))
# -> AIMessage that answers "Bob"
```

```python Anthropic
from langchain_core.messages import BaseMessage
from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint, task
from langgraph.graph import add_messages

model = ChatAnthropic(model="anthropic:claude-sonnet-4-6")


@task
def call_model(messages: list[BaseMessage]):
    response = model.invoke(messages)
    return response


checkpointer = InMemorySaver()


@entrypoint(checkpointer=checkpointer)
def workflow(inputs: list[BaseMessage], *, previous: list[BaseMessage] | None = None):
    if previous:
        inputs = add_messages(previous, inputs)

    response = call_model(inputs).result()
    return entrypoint.final(value=response, save=add_messages(inputs, response))


config = {"configurable": {"thread_id": "1"}}
input_message = {"role": "user", "content": "hi! I'm bob"}
print(workflow.invoke([input_message], config))
# -> AIMessage with a greeting that uses the name Bob

input_message = {"role": "user", "content": "what's my name?"}
print(workflow.invoke([input_message], config))
# -> AIMessage that answers "Bob"
```

```python OpenRouter
from langchain_core.messages import BaseMessage
from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint, task
from langgraph.graph import add_messages

model = ChatAnthropic(model="openrouter:z-ai/glm-5.2")


@task
def call_model(messages: list[BaseMessage]):
    response = model.invoke(messages)
    return response


checkpointer = InMemorySaver()


@entrypoint(checkpointer=checkpointer)
def workflow(inputs: list[BaseMessage], *, previous: list[BaseMessage] | None = None):
    if previous:
        inputs = add_messages(previous, inputs)

    response = call_model(inputs).result()
    return entrypoint.final(value=response, save=add_messages(inputs, response))


config = {"configurable": {"thread_id": "1"}}
input_message = {"role": "user", "content": "hi! I'm bob"}
print(workflow.invoke([input_message], config))
# -> AIMessage with a greeting that uses the name Bob

input_message = {"role": "user", "content": "what's my name?"}
print(workflow.invoke([input_message], config))
# -> AIMessage that answers "Bob"
```

```python Fireworks
from langchain_core.messages import BaseMessage
from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint, task
from langgraph.graph import add_messages

model = ChatAnthropic(model="fireworks:accounts/fireworks/models/glm-5p2")


@task
def call_model(messages: list[BaseMessage]):
    response = model.invoke(messages)
    return response


checkpointer = InMemorySaver()


@entrypoint(checkpointer=checkpointer)
def workflow(inputs: list[BaseMessage], *, previous: list[BaseMessage] | None = None):
    if previous:
        inputs = add_messages(previous, inputs)

    response = call_model(inputs).result()
    return entrypoint.final(value=response, save=add_messages(inputs, response))


config = {"configurable": {"thread_id": "1"}}
input_message = {"role": "user", "content": "hi! I'm bob"}
print(workflow.invoke([input_message], config))
# -> AIMessage with a greeting that uses the name Bob

input_message = {"role": "user", "content": "what's my name?"}
print(workflow.invoke([input_message], config))
# -> AIMessage that answers "Bob"
```

```python Baseten
from langchain_core.messages import BaseMessage
from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint, task
from langgraph.graph import add_messages

model = ChatAnthropic(model="baseten:zai-org/GLM-5.2")


@task
def call_model(messages: list[BaseMessage]):
    response = model.invoke(messages)
    return response


checkpointer = InMemorySaver()


@entrypoint(checkpointer=checkpointer)
def workflow(inputs: list[BaseMessage], *, previous: list[BaseMessage] | None = None):
    if previous:
        inputs = add_messages(previous, inputs)

    response = call_model(inputs).result()
    return entrypoint.final(value=response, save=add_messages(inputs, response))


config = {"configurable": {"thread_id": "1"}}
input_message = {"role": "user", "content": "hi! I'm bob"}
print(workflow.invoke([input_message], config))
# -> AIMessage with a greeting that uses the name Bob

input_message = {"role": "user", "content": "what's my name?"}
print(workflow.invoke([input_message], config))
# -> AIMessage that answers "Bob"
```

```python Ollama
from langchain_core.messages import BaseMessage
from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint, task
from langgraph.graph import add_messages

model = ChatAnthropic(model="ollama:north-mini-code-1.0")


@task
def call_model(messages: list[BaseMessage]):
    response = model.invoke(messages)
    return response


checkpointer = InMemorySaver()


@entrypoint(checkpointer=checkpointer)
def workflow(inputs: list[BaseMessage], *, previous: list[BaseMessage] | None = None):
    if previous:
        inputs = add_messages(previous, inputs)

    response = call_model(inputs).result()
    return entrypoint.final(value=response, save=add_messages(inputs, response))


config = {"configurable": {"thread_id": "1"}}
input_message = {"role": "user", "content": "hi! I'm bob"}
print(workflow.invoke([input_message], config))
# -> AIMessage with a greeting that uses the name Bob

input_message = {"role": "user", "content": "what's my name?"}
print(workflow.invoke([input_message], config))
# -> AIMessage that answers "Bob"
```

## Save facts across threads

[Long-term memory](https://docs.langchain.com/oss/python/concepts/memory.md#long-term-memory) lives in a [store](../../Capabilities/Stores.md), not in the checkpointer. Save a fact on one `thread_id` and read it on another.

Pass an [`InMemoryStore`](https://reference.langchain.com/python/langchain-core/stores/InMemoryStore) when you decorate the entrypoint. Read it from `runtime.store`.

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint
from langgraph.runtime import Runtime
from langgraph.store.memory import InMemoryStore

checkpointer = InMemorySaver()
store = InMemoryStore()


@entrypoint(checkpointer=checkpointer, store=store)
def remember(inputs: dict, *, runtime: Runtime):
    memory_store = runtime.store
    namespace = (inputs["user_id"], "memories")
    fact = inputs.get("fact")
    if fact:
        memory_store.put(namespace, "profile", {"fact": fact})
    items = memory_store.search(namespace)
    return [item.value for item in items]


config_a = {"configurable": {"thread_id": "thread-a"}}
config_b = {"configurable": {"thread_id": "thread-b"}}

remember.invoke(
    {"user_id": "user-1", "fact": "Prefers dark mode"},
    config_a,
)
print(remember.invoke({"user_id": "user-1"}, config_b))
# -> [{'fact': 'Prefers dark mode'}]
```

## See also

* [Functional API overview](Functional%20API%20overview.md)
* [Build checklist for the Functional API](Build%20checklist%20for%20the%20Functional%20API.md)
* [Memory](../../Capabilities/Memory.md)
* [Persistence](../../Capabilities/Persistence.md)
* [Stores](../../Capabilities/Stores.md)
* [Add human-in-the-loop with the Functional API](Add%20human-in-the-loop%20with%20the%20Functional%20API.md)
