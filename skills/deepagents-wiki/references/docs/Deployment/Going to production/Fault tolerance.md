# Fault tolerance

> Make your deep agent resilient with rate limiting, retries, fallbacks, and error handling

Fault tolerance middleware keeps your deep agent running when things go wrong. Not all errors should be handled the same way: transient failures (network timeouts, rate limits) should be retried automatically, errors the LLM can recover from (bad tool output, parsing failures) should be fed back to the model, and errors that need human input should pause the agent.

## Error handling strategies

Different errors need different handling strategies:

| Error type | Who fixes it | Strategy | Middleware or feature |
| - | - | - | - |
| Transient errors (network issues, rate limits) | System (automatic) | Retry with exponential backoff | [ModelRetryMiddleware](https://reference.langchain.com/python/langchain/agents/middleware/model_retry/ModelRetryMiddleware), [ToolRetryMiddleware](https://reference.langchain.com/python/langchain/agents/middleware/tool_retry/ToolRetryMiddleware) |
| LLM-recoverable errors (tool failures, parsing issues) | LLM | Convert to error `ToolMessage` and let the model adjust | [ToolErrorMiddleware](https://reference.langchain.com/python/langchain/agents/middleware/tool_error/ToolErrorMiddleware) |
| Model refusals | System or developer | Fall back to another model, then catch the error | [ModelFallbackMiddleware](https://reference.langchain.com/python/langchain/agents/middleware/model_fallback/ModelFallbackMiddleware), [ModelRefusalMiddleware](https://reference.langchain.com/python/langchain/agents/middleware/model_refusal/ModelRefusalMiddleware) |
| User-fixable errors (missing information, unclear instructions) | Human | Pause with `interrupt()` | [Human-in-the-loop](../../Steering/Human-in-the-loop.md) |
| Provider outage | System (automatic) | Fall back to an alternative model | [ModelFallbackMiddleware](https://reference.langchain.com/python/langchain/agents/middleware/model_fallback/ModelFallbackMiddleware) |
| Excessive calls (runaway loops) | System (automatic) | Cap model and tool calls per run | [ModelCallLimitMiddleware](https://reference.langchain.com/python/langchain/agents/middleware/model_call_limit/ModelCallLimitMiddleware), [ToolCallLimitMiddleware](https://reference.langchain.com/python/langchain/agents/middleware/tool_call_limit/ToolCallLimitMiddleware) |
| Unexpected errors | Developer | Let them bubble up | No middleware; let the exception propagate |

The sections below cover each strategy with code examples.

> [tab] Transient errors
>
> Add retry middleware to automatically retry network issues and rate limits. Model calls and tool calls each have their own retry middleware with exponential backoff:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langchain.agents import create_agent
> from langchain.agents.middleware import ModelRetryMiddleware, ToolRetryMiddleware
>
> agent = create_agent(
>     model="google_genai:gemini-3.6-flash",
>     tools=[search_tool, fetch_url_tool],
>     middleware=[
>         ModelRetryMiddleware(max_retries=3, backoff_factor=2.0, initial_delay=1.0),
>         ToolRetryMiddleware(
>             max_retries=2,
>             tools=["search", "fetch_url"],
>             retry_on=(TimeoutError, ConnectionError),
>         ),
>     ],
> )
> ```

> [tab] LLM-recoverable
>
> Use [ToolErrorMiddleware](https://reference.langchain.com/python/langchain/agents/middleware/tool_error/ToolErrorMiddleware) to catch tool exceptions and convert them into error `ToolMessage`s so the LLM can see what went wrong and try again:
>
> > [!NOTE]
> >
> > `ToolErrorMiddleware` requires `langchain>=1.3.14`.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langchain.agents import create_agent
> from langchain.agents.middleware import ToolErrorMiddleware
>
>
> def on_error(exc: Exception, request: ToolCallRequest) -> str | None:
>     if isinstance(exc, ValueError):
>         return f"Tool `{request.tool_call['name']}` failed: {type(exc).__name__}. Fix the input and retry."
>     # propagate everything else
>
>
> agent = create_agent(
>     model="google_genai:gemini-3.6-flash",
>     tools=[search_tool],
>     middleware=[ToolErrorMiddleware(on_error)],
> )
> ```

> [tab] User-fixable
>
> Pause and collect information from the user when needed (like account IDs, order numbers, or clarifications). Use `interrupt_on` to pause the agent before specific tool calls:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
>
> agent = create_deep_agent(
>     model="google_genai:gemini-3.6-flash",
>     tools=[send_email_tool, delete_record_tool],
>     interrupt_on={
>         "send_email": True,
>         "delete_record": True,
>     },
> )
> ```
>
> For the full human-in-the-loop guide, see [Human-in-the-loop](../../Steering/Human-in-the-loop.md).

> [tab] Provider outage
>
> If your primary model provider goes down entirely, use [ModelFallbackMiddleware](https://reference.langchain.com/python/langchain/agents/middleware/model_fallback/ModelFallbackMiddleware) to switch to an alternative model:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langchain.agents import create_agent
> from langchain.agents.middleware import ModelFallbackMiddleware
>
> agent = create_agent(
>     model="google_genai:gemini-3.6-flash",
>     tools=[search_tool],
>     middleware=[
>         ModelFallbackMiddleware("gpt-5.5"),
>     ],
> )
> ```

> [tab] Excessive calls
>
> Without limits, a confused agent can burn through your LLM API budget in minutes by looping on the same tool call or making hundreds of model calls. Set caps on both model calls and tool executions per run:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langchain.agents import create_agent
> from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware
>
> agent = create_agent(
>     model="google_genai:gemini-3.6-flash",
>     tools=[search_tool],
>     middleware=[
>         ModelCallLimitMiddleware(run_limit=50),
>         ToolCallLimitMiddleware(run_limit=200),
>     ],
> )
> ```

> [tab] Unexpected
>
> Let them bubble up for debugging. Do not catch what you cannot handle. [ToolErrorMiddleware](https://reference.langchain.com/python/langchain/agents/middleware/tool_error/ToolErrorMiddleware) only surfaces exceptions you explicitly return content for; everything else propagates unchanged:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> def on_error(exc: Exception, request: ToolCallRequest) -> str | None:
>     if isinstance(exc, (ValueError, KeyError)):
>         # Surface known, recoverable errors to the model
>         return f"Tool `{request.tool_call['name']}` failed: {type(exc).__name__}."
>     # Everything else (unexpected errors) propagates and halts the run
> ```

## Rate limiting

There are two complementary ways to limit resource usage: controlling the request rate to your model provider, and capping the total number of calls per run.

### Provider rate limiting

Chat model providers impose a limit on the number of invocations that can be made in a given time period. To control the rate at which requests are made, initialize your model with a `rate_limiter`:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.rate_limiters import InMemoryRateLimiter
from langchain.chat_models import init_chat_model

rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.1,  # 1 request every 10s
    check_every_n_seconds=0.1,  # Check every 100ms whether allowed to make a request
    max_bucket_size=10,  # Controls the maximum burst size
)

model = init_chat_model(
    model="google_genai:gemini-3.6-flash",
    rate_limiter=rate_limiter,  # [!code highlight]
)

agent = create_deep_agent(model=model, tools=[search_tool])
```

For the full configuration, see [Rate limiting](https://docs.langchain.com/oss/python/langchain/models.md#rate-limiting).

### Call limits

Without limits, a confused agent can burn through your LLM API budget in minutes by looping on the same tool call or making hundreds of model calls. Set caps on both model calls and tool executions per run:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware

agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    middleware=[
        ModelCallLimitMiddleware(run_limit=50),
        ToolCallLimitMiddleware(run_limit=200),
    ],
)
```

Use `run_limit` to cap calls within a single invocation (resets each turn). Use `thread_limit` to cap calls across an entire conversation (requires a checkpointer). See [ModelCallLimitMiddleware](https://reference.langchain.com/python/langchain/agents/middleware/model_call_limit/ModelCallLimitMiddleware) and [ToolCallLimitMiddleware](https://reference.langchain.com/python/langchain/agents/middleware/tool_call_limit/ToolCallLimitMiddleware) for the full configuration.

## Retries

Transient failures (network timeouts, rate limits) should be retried automatically. Model calls and tool calls each have their own retry middleware with exponential backoff:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain.agents.middleware import ModelRetryMiddleware, ToolRetryMiddleware

agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    middleware=[
        # Retry model calls on rate limits, timeouts, and 5xx errors
        ModelRetryMiddleware(max_retries=3, backoff_factor=2.0, initial_delay=1.0),
        # Retry specific tools that hit external APIs (not all tools)
        ToolRetryMiddleware(
            max_retries=2,
            tools=["search", "fetch_url"],
            retry_on=(TimeoutError, ConnectionError),
        ),
    ],
)
```

Scope [ToolRetryMiddleware](https://reference.langchain.com/python/langchain/agents/middleware/tool_retry/ToolRetryMiddleware) to specific tools rather than retrying everything. A filesystem `read_file` that fails will not benefit from a retry, but a web search that times out probably will. See [ModelRetryMiddleware](https://reference.langchain.com/python/langchain/agents/middleware/model_retry/ModelRetryMiddleware) for the full configuration.

> [!NOTE]
>
> Major integration packages raise standard exception types ([ModelAuthenticationError](https://reference.langchain.com/python/langchain-core/exceptions/ModelAuthenticationError), [ModelRateLimitError](https://reference.langchain.com/python/langchain-core/exceptions/ModelRateLimitError), [ModelTimeoutError](https://reference.langchain.com/python/langchain-core/exceptions/ModelTimeoutError), and others) that carry an `is_retryable` flag the retry middleware respects by default. See [Model exceptions](https://docs.langchain.com/oss/python/langchain/models.md#model-exceptions) for the full list.

## Fallbacks

If your primary model provider goes down entirely, the fallback middleware switches to an alternative model:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain.agents.middleware import ModelFallbackMiddleware

agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    middleware=[
        # If the primary model is fully down, fall back to an alternative
        ModelFallbackMiddleware("gpt-5.5"),
    ],
)
```

See [ModelFallbackMiddleware](https://reference.langchain.com/python/langchain/agents/middleware/model_fallback/ModelFallbackMiddleware) for the full configuration.

### Model refusals

A provider can refuse a request, for example under a safety policy, and still return a successful response. Deep Agents raise [`ModelRefusalError`](https://reference.langchain.com/python/langchain-core/exceptions/ModelRefusalError) when the model refuses, so the run does not end as if it succeeded. [`ModelRefusalMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/model_refusal/ModelRefusalMiddleware) runs after your middleware, so a [`ModelFallbackMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/model_fallback/ModelFallbackMiddleware) you pass retries the refused request on the next model first, and the run raises only when no fallback is left. The fallback model can be from the same provider or a different one, and it can still refuse the same request.

Model-level `with_fallbacks` does not catch refusals, because the middleware detects them after the model call returns. Use [`ModelFallbackMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/model_fallback/ModelFallbackMiddleware) instead.

When every model refuses, catch `ModelRefusalError` where you invoke the agent. The refused reply is not saved to the thread, so you can tell the user and continue the conversation. For this and other options, see [Handle a refusal](../../Middleware/Prebuilt%20middleware.md#handle-a-refusal). For how subagent refusals reach the parent agent, see [Model refusals](../../Delegation/Subagents.md#model-refusals).

## Error handling

When a tool raises an exception during execution, the agent run halts by default. Use [ToolErrorMiddleware](https://reference.langchain.com/python/langchain/agents/middleware/tool_error/ToolErrorMiddleware) to catch specific exceptions and convert them into error ToolMessages that the model can see and recover from, instead of crashing the run.

> [!NOTE]
>
> `ToolErrorMiddleware` requires `langchain>=1.3.14`.

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain.agents.middleware import ToolErrorMiddleware


def on_error(exc: Exception, request: ToolCallRequest) -> str | None:
    if isinstance(exc, ValueError):
        return f"`{request.tool_call['name']}` failed with {type(exc).__name__}."
    # propagate everything else


agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    middleware=[ToolErrorMiddleware(on_error)],
)
```

For the full configuration options and usage patterns, including async handlers and composing with retry middleware, see [Prebuilt middleware](../../Middleware/Prebuilt%20middleware.md#tool-error).

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/deepagents/fault-tolerance.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
