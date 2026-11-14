# Unit testing

> Test agent logic without API calls using fake chat models and in-memory persistence.

Unit tests exercise small, deterministic pieces of your agent in isolation. By replacing the real LLM with an in-memory fake (AKA fixture), you can script exact responses (text, tool calls, and errors) so tests are fast, free, and repeatable without API keys.

## Mock chat model

LangChain provides [`GenericFakeChatModel`](https://reference.langchain.com/python/langchain-core/language_models/fake_chat_models/GenericFakeChatModel) for mocking text responses. It accepts an iterator of responses ([`AIMessage`](https://reference.langchain.com/python/langchain-core/messages/ai/AIMessage) objects or strings) and returns one per invocation. It supports both regular and streaming usage.

```python
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain.messages import AIMessage, ToolCall

model = GenericFakeChatModel(messages=iter([
    AIMessage(content="", tool_calls=[ToolCall(name="foo", args={"bar": "baz"}, id="call_1")]),
    "bar"
]))

model.invoke("hello")
# AIMessage(content='', ..., tool_calls=[{'name': 'foo', 'args': {'bar': 'baz'}, 'id': 'call_1', 'type': 'tool_call'}])
```

If we invoke the model again, it will return the next item in the iterator:

```python
model.invoke("hello, again!")
# AIMessage(content='bar', ...)
```

## Return plain text with `FakeListChatModel`

For tests that only need text responses, use `FakeListChatModel`. It takes a list of strings, so you do not construct `AIMessage` objects:

```python
from langchain_core.language_models import FakeListChatModel

model = FakeListChatModel(responses=["Paris", "The Eiffel Tower"])

model.invoke("What is the capital of France?")
# AIMessage(content='Paris', ...)

model.invoke("What is a famous landmark there?")
# AIMessage(content='The Eiffel Tower', ...)
```

`FakeListChatModel` cycles through its responses. When invoked more times than the list has entries, it starts again from the first response. Use `GenericFakeChatModel` when you need exact control of each turn, such as tool calls.

## Test a tool-calling loop

An agent typically calls a tool, then uses the result to answer. To script this loop, give the fake model two responses: a tool call, then a final answer.

`GenericFakeChatModel` does not implement `bind_tools`, which [`create_agent`](https://reference.langchain.com/python/langchain/agents/factory/create_agent) calls when you pass tools. Subclass it so that `bind_tools` returns the model unchanged:

```python
from langchain.agents import create_agent
from langchain.messages import AIMessage, HumanMessage, ToolCall
from langchain.tools import tool
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel


class FakeToolCallingModel(GenericFakeChatModel):
    def bind_tools(self, tools, **kwargs):
        return self


@tool
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    return f"72°F and sunny in {city}"


def test_agent_calls_tool_then_answers():
    model = FakeToolCallingModel(messages=iter([
        # Turn 1: the model calls the tool
        AIMessage(
            content="",
            tool_calls=[ToolCall(name="get_weather", args={"city": "Tokyo"}, id="call_1")],
        ),
        # Turn 2: the model answers using the tool result
        AIMessage(content="It is 72°F and sunny in Tokyo."),
    ]))
    agent = create_agent(model, tools=[get_weather])

    result = agent.invoke({"messages": [HumanMessage(content="Weather in Tokyo?")]})

    tool_call_messages = [
        m for m in result["messages"] if isinstance(m, AIMessage) and m.tool_calls
    ]
    assert len(tool_call_messages) == 1
    assert tool_call_messages[0].tool_calls[0]["name"] == "get_weather"
    assert "Tokyo" in result["messages"][-1].text
```

## Share fake models with pytest fixtures

To reuse a fake model across tests, return it from a `pytest` fixture. This example uses `FakeToolCallingModel` and `get_weather` from the previous section:

```python
import pytest
from langchain.agents import create_agent
from langchain.messages import AIMessage, HumanMessage, ToolCall


@pytest.fixture
def weather_model():
    return FakeToolCallingModel(messages=iter([
        AIMessage(
            content="",
            tool_calls=[ToolCall(name="get_weather", args={"city": "Tokyo"}, id="call_1")],
        ),
        AIMessage(content="It is 72°F and sunny in Tokyo."),
    ]))


def test_tool_is_called(weather_model):
    agent = create_agent(weather_model, tools=[get_weather])
    result = agent.invoke({"messages": [HumanMessage(content="Weather in Tokyo?")]})
    tool_call_messages = [
        m for m in result["messages"] if isinstance(m, AIMessage) and m.tool_calls
    ]
    assert tool_call_messages[0].tool_calls[0]["name"] == "get_weather"


def test_final_response(weather_model):
    agent = create_agent(weather_model, tools=[get_weather])
    result = agent.invoke({"messages": [HumanMessage(content="Weather in Tokyo?")]})
    assert "Tokyo" in result["messages"][-1].text
```

> [!NOTE]
>
> `GenericFakeChatModel` reads responses from an iterator, and an exhausted iterator cannot be reused. Keep the fixture at the default `function` scope, which builds a fresh model for each test. A `module` or `session` scope shares one iterator, so later tests fail once it runs out.

## InMemorySaver checkpointer

To enable persistence during testing, you can use the [`InMemorySaver`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.memory.InMemorySaver) checkpointer. This allows you to simulate multiple turns to test state-dependent behavior:

```python
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from langchain.messages import HumanMessage

agent = create_agent(
    model,
    tools=[],
    checkpointer=InMemorySaver()
)

# First invocation
agent.invoke(
    {"messages": [HumanMessage(content="I live in Sydney, Australia")]},
    config={"configurable": {"thread_id": "session-1"}}
)

# Second invocation: the first message is persisted (Sydney location), so the model returns GMT+10 time
agent.invoke(
    {"messages": [HumanMessage(content="What's my local time?")]},
    config={"configurable": {"thread_id": "session-1"}}
)
```

## Next steps

Learn how to test your agent with real model provider APIs in [Integration testing](Integration%20testing.md).

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/test/unit-testing.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
