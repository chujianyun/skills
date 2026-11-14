# Integration testing

> Test agents with real LLM APIs by organizing tests, managing keys, handling flakiness, and controlling costs.

Integration tests verify that your agent works correctly with model APIs and external services. Unlike [unit tests](Unit%20testing.md) that use fakes and mocks, integration tests make actual network calls to confirm that components work together, credentials are valid, and latency is acceptable.

Because LLM responses are nondeterministic, integration tests require different strategies than traditional software tests. This guide covers how to organize, write, and run integration tests for your agents. For general test infrastructure when contributing to LangChain itself, see [Contributing to code](https://docs.langchain.com/oss/python/contributing/code.md#running-tests).

## Separate unit and integration tests

Integration tests are slower and require API credentials, so keep them separate from unit tests. This lets you run fast unit tests on every change and reserve integration tests for CI or pre-deploy checks.

Use pytest markers to tag integration tests:

```python
import pytest
from langchain.agents import create_agent
from langchain.messages import HumanMessage

@pytest.mark.integration
def test_agent_with_real_model():
    agent = create_agent("claude-sonnet-4-6", tools=[get_weather])
    result = agent.invoke({
        "messages": [HumanMessage(content="What's the weather in SF?")]
    })
    assert len(result["messages"]) > 1
```

Configure pytest to recognize the marker and exclude integration tests from default runs:

```ini pytest.ini
[pytest]
markers =
    integration: tests that call real LLM APIs
addopts = -m "not integration"
```

```toml pyproject.toml
[tool.pytest.ini_options]
markers = [
  "integration: tests that call real LLM APIs"
]
addopts = "-m 'not integration'"
```

Run integration tests explicitly:

```bash
pytest -m integration
```

## Manage API keys

Integration tests require real API credentials. Load them from environment variables so keys stay out of source control.

Use a `conftest.py` fixture to validate that required keys are available:

```python
import os
import pytest

@pytest.fixture(autouse=True)
def check_api_keys():
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set")
```

For local development, store keys in a `.env` file and load them with [`python-dotenv`](https://pypi.org/project/python-dotenv/):

```bash .env
OPENAI_API_KEY=sk-...
```

```python conftest.py
from dotenv import load_dotenv

load_dotenv()
```

> [!WARNING]
>
> Add `.env` to your `.gitignore` to avoid committing credentials. In CI, inject secrets through your provider's secrets management (e.g., GitHub Actions secrets).

## Assert on structure, not content

LLM responses vary between runs. Instead of asserting on exact output strings, verify the structural properties of the response: message types, tool call names, argument shapes, and message count.

```python
from langchain.agents import create_agent
from langchain.messages import AIMessage, HumanMessage

def test_agent_calls_weather_tool():
    agent = create_agent("claude-sonnet-4-6", tools=[get_weather])
    result = agent.invoke({
        "messages": [HumanMessage(content="What's the weather in SF?")]
    })

    messages = result["messages"]
    tool_calls = [
        tc
        for msg in messages
        if hasattr(msg, "tool_calls")
        for tc in (msg.tool_calls or [])
    ]

    assert any(tc["name"] == "get_weather" for tc in tool_calls)
    assert isinstance(messages[-1], AIMessage)
    assert len(messages[-1].content) > 0
```

> [!TIP]
>
> For more rigorous trajectory assertions, use the [AgentEvals](Agent%20Evals.md) evaluators which support fuzzy matching modes like `unordered` and `superset`.

## Reduce cost and latency

Integration tests that call LLM APIs incur real costs. A few practices help keep test suites fast and affordable:

* **Use smaller models**: `gemini-3.1-flash-lite` or equivalent for tests that only need to verify tool calling and response structure.
* **Cap output tokens**: Limit response length on the chat model to avoid long, expensive completions.
* **Limit test scope**: Test one behavior per test. Avoid end-to-end scenarios that chain many LLM calls when a single-turn test suffices.
* **Run selectively**: Use the test separation from [above](#separate-unit-and-integration-tests) to run integration tests only in CI or before deploy, not on every file save.

```python
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

model = init_chat_model("google_genai:gemini-3.1-flash-lite", max_tokens=256)

agent = create_agent(model, tools=[get_weather])
```

## Record and replay HTTP calls

For tests that run frequently in CI, you can record HTTP interactions on the first run and replay them on subsequent runs without making real API calls. This eliminates cost and latency after the initial recording.

[`vcrpy`](https://pypi.org/project/vcrpy/1.5.2/) records HTTP request/response pairs into YAML "cassette" files. The [`pytest-recording`](https://pypi.org/project/pytest-recording/) plugin integrates this with pytest.

Set up your `conftest.py` to filter sensitive information from cassettes:

```py conftest.py
import pytest

@pytest.fixture(scope="session")
def vcr_config():
    return {
        "filter_headers": [
            ("authorization", "XXXX"),
            ("x-api-key", "XXXX"),
        ],
        "filter_query_parameters": [
            ("api_key", "XXXX"),
            ("key", "XXXX"),
        ],
    }
```

Configure your project to recognize the `vcr` marker:

```ini pytest.ini
[pytest]
markers =
    vcr: record/replay HTTP via VCR
addopts = --record-mode=once
```

```toml pyproject.toml
[tool.pytest.ini_options]
markers = [
  "vcr: record/replay HTTP via VCR"
]
addopts = "--record-mode=once"
```

> [!NOTE]
>
> The `--record-mode=once` option records HTTP interactions on the first run and replays them on subsequent runs.

Decorate your tests with the `vcr` marker:

```python
import pytest
from langchain.agents import create_agent
from langchain.messages import HumanMessage

@pytest.mark.vcr()
def test_agent_trajectory():
    agent = create_agent("claude-sonnet-4-6", tools=[get_weather])
    result = agent.invoke({
        "messages": [HumanMessage(content="What's the weather in SF?")]
    })
    assert any(
        tc["name"] == "get_weather"
        for msg in result["messages"]
        if hasattr(msg, "tool_calls")
        for tc in (msg.tool_calls or [])
    )
```

The first run makes real network calls and generates a cassette file in `tests/cassettes/`. Subsequent runs replay the recorded responses.

> [!WARNING]
>
> When you modify prompts, add new tools, or change expected trajectories, your saved cassettes will become outdated and your existing tests **will fail**. Delete the corresponding cassette files and rerun the tests to record fresh interactions.

## Next steps

Learn how to evaluate agent trajectories with deterministic matching or LLM-as-judge evaluators in [Evals](Agent%20Evals.md).

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/test/integration-testing.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
