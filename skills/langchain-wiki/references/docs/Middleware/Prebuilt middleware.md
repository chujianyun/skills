# Prebuilt middleware

> Prebuilt middleware for common agent use cases

LangChain provides prebuilt middleware for common use cases. Each middleware is production-ready and configurable for your specific needs.

> [!NOTE]
>
> Using [Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview.md) (`create_deep_agent` / `createDeepAgent`)? Middleware is added through the [customization](https://docs.langchain.com/oss/python/deepagents/customization.md#middleware) API instead.

## Provider-agnostic middleware

The following middleware work with any LLM provider:

| Middleware | Description |
| - | - |
| [Tool error](#tool-error) | Catch tool execution exceptions and convert them to error messages for the model. |
| [Tool retry](#tool-retry) | Automatically retry failed tool calls with exponential backoff. |
| [Model retry](#model-retry) | Automatically retry failed model calls with exponential backoff. |
| [Model fallback](#model-fallback) | Automatically fallback to alternative models when primary fails. |
| [Model refusal](#model-refusal) | Raise an error when the model refuses, instead of treating the refusal as a final answer. |
| [Summarization](#summarization) | Automatically summarize conversation history when approaching token limits. |
| [Human-in-the-loop](#human-in-the-loop) | Pause execution for human approval of tool calls. |
| [Model call limit](#model-call-limit) | Limit the number of model calls to prevent excessive costs. |
| [Tool call limit](#tool-call-limit) | Control tool execution by limiting call counts. |
| [PII detection](#pii-detection) | Detect and handle Personally Identifiable Information (PII). |
| [To-do list](#to-do-list) | Equip agents with task planning and tracking capabilities. |
| [LLM tool selector](#llm-tool-selector) | Use an LLM to select relevant tools before calling main model. |
| [Model router](#model-router) | Use a decision model to choose the model for each agent run. |
| [Auto mode](#auto-mode) | Use a decision model to block risky tool calls before they run. |
| [Provider tool search](#provider-tool-search) | Defer tools behind providers' server-side tool search, surfacing them on demand. |
| [Shell tool](#shell-tool) | Expose a persistent shell session to agents for command execution. |
| [Filesystem](#filesystem-middleware) | Provide agents with a filesystem for storing context and long-term memories. |
| [Subagent](#subagent) | Add the ability to spawn subagents. |
| [Rubric grading](#rubric-grading) | Apply LLM-as-a-judge grading so agents self-evaluate and iterate until a rubric is satisfied. |
| [File search](#file-search) | Provide Glob and Grep search tools over filesystem files. |
| [Context editing](#context-editing) | Manage conversation context by trimming or clearing tool uses. |
| [LLM tool emulator](#llm-tool-emulator) | Emulate tool execution using an LLM for testing purposes. |

### Tool error

Catch exceptions raised during tool execution and convert them into error `ToolMessage`s that the model can see and recover from, instead of halting the agent run. Tool error is useful for the following:

* Letting the model retry a failed tool call with corrected arguments.
* Surfacing controlled, sanitized error messages instead of raw exception details.
* Preventing unexpected tool exceptions from crashing the agent.

> [!NOTE]
>
> Tool error middleware does not automatically retry failed calls. For retries, compose with [Tool retry](#tool-retry) middleware placed *inner* (later in the `middleware` list) and configured with `on_failure="error"` so that exceptions reach the tool error middleware. See the [full example](#tool-error-full-example) below.

**API reference:** [`ToolErrorMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/tool_error/ToolErrorMiddleware)

> [!NOTE]
>
> `ToolErrorMiddleware` requires `langchain>=1.3.14`.

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ToolErrorMiddleware


def on_error(exc: Exception, request: ToolCallRequest) -> str | None:
    if isinstance(exc, ValueError):
        return f"`{request.tool_call['name']}` failed with {type(exc).__name__}."
    # propagate everything else


agent = create_agent(
    model="gpt-6.1-sol",
    tools=[your_tools],
    middleware=[ToolErrorMiddleware(on_error)],
)
```

> [accordion] Configuration options
>
> **on\_error** `Callable[[Exception, ToolCallRequest], str | list[ContentBlock] | None]`
>
> Sync handler called for each exception raised by tool execution. Return content (a `str` or list of content blocks) to convert the exception into a `ToolMessage(status="error")`. Return `None` or omit a return statement to let the exception propagate. Used on the sync path and, unless `aon_error` is given, on the async path.
>
> **aon\_error** `Callable[[Exception, ToolCallRequest], Awaitable[str | list[ContentBlock] | None]]`
>
> Optional async handler, used on the async execution path. Falls back to `on_error` when not provided.
>
> **tools** `list[BaseTool | str]`
>
> Optional list of tools or tool names to apply error handling to. If `None`, applies to all tools.

> [accordion] Tool error full example
>
> The `on_error` handler receives the exception and the `ToolCallRequest` (which includes the tool call dict with name, args, and call ID). Return `None` for exceptions you do not want to handle, and they will propagate normally.
>
> ```python
> from langchain.agents import create_agent
> from langchain.agents.middleware import ToolErrorMiddleware, ToolRetryMiddleware
>
>
> def on_error(exc: Exception, request: ToolCallRequest) -> str | None:
>     # Surface ValueError to the model so it can correct the input
>     if isinstance(exc, ValueError):
>         return f"`{request.tool_call['name']}` failed: {type(exc).__name__}. Fix the input and retry."
>     # Let all other exceptions propagate (halts the run)
>     return None
>
>
> # Async-only usage
> async def aon_error(exc: Exception, request: ToolCallRequest) -> str | None:
>     if isinstance(exc, ConnectionError):
>         return f"Tool `{request.tool_call['name']}` encountered a connection error."
>     return None
>
>
> agent = create_agent(
>     model="gpt-6.1-sol",
>     tools=[search_tool, database_tool],
>     middleware=[
>         # Place retry inner so exceptions reach ToolErrorMiddleware after retries are exhausted
>         ToolErrorMiddleware(on_error=on_error, tools=["search_tool"]),
>         ToolRetryMiddleware(max_retries=3, on_failure="error"),
>     ],
> )
>
> # Async-only: pass aon_error alone (do not pass on_error)
> async_agent = create_agent(
>     model="gpt-6.1-sol",
>     tools=[api_tool],
>     middleware=[ToolErrorMiddleware(aon_error=aon_error)],
> )
> ```
>
> > [!NOTE]
> >
> > Prefer returning content that names the exception type over the raw exception message, which may carry sensitive or internal detail. The `on_error` handler controls disclosure: the raw exception message is never sent to the model unless you choose to include it.

### Tool retry

Automatically retry failed tool calls with configurable exponential backoff. Tool retry is useful for the following:

* Handling transient failures in external API calls.
* Improving reliability of network-dependent tools.
* Building resilient agents that gracefully handle temporary errors.

**API reference:** [`ToolRetryMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/tool_retry/ToolRetryMiddleware)

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ToolRetryMiddleware

agent = create_agent(
    model="gpt-6.1-sol",
    tools=[search_tool, database_tool],
    middleware=[
        ToolRetryMiddleware(
            max_retries=3,
            backoff_factor=2.0,
            initial_delay=1.0,
        ),
    ],
)
```

> [accordion] Configuration options
>
> **max\_retries** `number` (default: 2)
>
> Maximum number of retry attempts after the initial call (3 total attempts with default)
>
> **tools** `list[BaseTool | str]`
>
> Optional list of tools or tool names to apply retry logic to. If `None`, applies to all tools.
>
> **retry\_on** `tuple[type[Exception], ...] | callable` (default: default\_retry\_on)
>
> Either a tuple of exception types to retry on, or a callable that takes an exception and returns `True` if it should be retried. With `langchain>=1.3.16`, the default retries retryable [model errors](../Core%20components/Models.md#model-exceptions) and all unclassified exceptions, and no longer retries model errors marked non-retryable.
>
> **on\_failure** `string | callable` (default: continue)
>
> Behavior when all retries are exhausted. Options:
>
> * `'continue'` (default) - Return a `ToolMessage` with error details, allowing the LLM to handle the failure
> * `'error'` - Re-raise the exception, stopping agent execution
> * Custom callable - Function that takes the exception and returns a string for the `ToolMessage` content
>
> **Deprecated values:** `'return_message'` (use `'continue'` instead) and `'raise'` (use `'error'` instead).
>
> **backoff\_factor** `number` (default: 2.0)
>
> Multiplier for exponential backoff. Each retry waits `initial_delay * (backoff_factor ** retry_number)` seconds. Set to `0.0` for constant delay.
>
> **initial\_delay** `number` (default: 1.0)
>
> Initial delay in seconds before first retry
>
> **max\_delay** `number` (default: 60.0)
>
> Maximum delay in seconds between retries (caps exponential backoff growth)
>
> **jitter** `boolean` (default: true)
>
> Whether to add random jitter (`±25%`) to delay to avoid thundering herd

> [accordion] Full example
>
> The middleware automatically retries failed tool calls with exponential backoff.
>
> **Key configuration:**
>
> * `max_retries` - Number of retry attempts (default: 2)
> * `backoff_factor` - Multiplier for exponential backoff (default: 2.0)
> * `initial_delay` - Starting delay in seconds (default: 1.0)
> * `max_delay` - Cap on delay growth (default: 60.0)
> * `jitter` - Add random variation (default: True)
>
> **Failure handling:**
>
> * `on_failure='continue'` (default) - Return error message
> * `on_failure='error'` - Re-raise exception
> * Custom function - Function returning error message
>
> ```python
> from langchain.agents import create_agent
> from langchain.agents.middleware import ToolRetryMiddleware
>
>
> agent = create_agent(
>     model="gpt-6.1-sol",
>     tools=[search_tool, database_tool, api_tool],
>     middleware=[
>         ToolRetryMiddleware(
>             max_retries=3,
>             backoff_factor=2.0,
>             initial_delay=1.0,
>             max_delay=60.0,
>             jitter=True,
>             tools=["api_tool"],
>             retry_on=(ConnectionError, TimeoutError),
>             on_failure="continue",
>         ),
>     ],
> )
> ```

### Model retry

Automatically retry failed model calls with configurable exponential backoff. Model retry is useful for the following:

* Handling transient failures in model API calls.
* Improving reliability of network-dependent model requests.
* Building resilient agents that gracefully handle temporary model errors.

**API reference:** [`ModelRetryMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/model_retry/ModelRetryMiddleware)

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRetryMiddleware

agent = create_agent(
    model="gpt-6.1-sol",
    tools=[search_tool, database_tool],
    middleware=[
        ModelRetryMiddleware(
            max_retries=3,
            backoff_factor=2.0,
            initial_delay=1.0,
        ),
    ],
)
```

> [accordion] Configuration options
>
> **max\_retries** `number` (default: 2)
>
> Maximum number of retry attempts after the initial call (3 total attempts with default)
>
> **retry\_on** `tuple[type[Exception], ...] | callable` (default: default\_retry\_on)
>
> Either a tuple of exception types to retry on, or a callable that takes an exception and returns `True` if it should be retried. With `langchain>=1.3.16`, the default retries retryable [model errors](../Core%20components/Models.md#model-exceptions) and all unclassified exceptions, and no longer retries model errors marked non-retryable.
>
> **on\_failure** `string | callable` (default: continue)
>
> Behavior when all retries are exhausted. Options:
>
> * `'continue'` (default) - Return an `AIMessage` with error details, allowing the agent to potentially handle the failure gracefully
> * `'error'` - Re-raise the exception (stops agent execution)
> * Custom callable - Function that takes the exception and returns a string for the `AIMessage` content
>
> **backoff\_factor** `number` (default: 2.0)
>
> Multiplier for exponential backoff. Each retry waits `initial_delay * (backoff_factor ** retry_number)` seconds. Set to `0.0` for constant delay.
>
> **initial\_delay** `number` (default: 1.0)
>
> Initial delay in seconds before first retry
>
> **max\_delay** `number` (default: 60.0)
>
> Maximum delay in seconds between retries (caps exponential backoff growth)
>
> **jitter** `boolean` (default: true)
>
> Whether to add random jitter (`±25%`) to delay to avoid thundering herd

> [accordion] Full example
>
> The middleware automatically retries failed model calls with exponential backoff.
>
> ```python
> from langchain.agents import create_agent
> from langchain.agents.middleware import ModelRetryMiddleware
>
>
> # Basic usage with default settings (2 retries, exponential backoff)
> agent = create_agent(
>     model="gpt-6.1-sol",
>     tools=[search_tool],
>     middleware=[ModelRetryMiddleware()],
> )
>
> # Custom exception filtering
> class TimeoutError(Exception):
>     """Custom exception for timeout errors."""
>     pass
>
> class ConnectionError(Exception):
>     """Custom exception for connection errors."""
>     pass
>
> # Retry specific exceptions only
> retry = ModelRetryMiddleware(
>     max_retries=4,
>     retry_on=(TimeoutError, ConnectionError),
>     backoff_factor=1.5,
> )
>
>
> def should_retry(error: Exception) -> bool:
>     # Only retry on rate limit errors
>     if isinstance(error, TimeoutError):
>         return True
>     # Or check for specific HTTP status codes
>     if hasattr(error, "status_code"):
>         return error.status_code in (429, 503)
>     return False
>
> retry_with_filter = ModelRetryMiddleware(
>     max_retries=3,
>     retry_on=should_retry,
> )
>
> # Return error message instead of raising
> retry_continue = ModelRetryMiddleware(
>     max_retries=4,
>     on_failure="continue",  # Return AIMessage with error instead of raising
> )
>
> # Custom error message formatting
> def format_error(error: Exception) -> str:
>     return f"Model call failed: {error}. Please try again later."
>
> retry_with_formatter = ModelRetryMiddleware(
>     max_retries=4,
>     on_failure=format_error,
> )
>
> # Constant backoff (no exponential growth)
> constant_backoff = ModelRetryMiddleware(
>     max_retries=5,
>     backoff_factor=0.0,  # No exponential growth
>     initial_delay=2.0,  # Always wait 2 seconds
> )
>
> # Raise exception on failure
> strict_retry = ModelRetryMiddleware(
>     max_retries=2,
>     on_failure="error",  # Re-raise exception instead of returning message
> )
> ```

### Model fallback

Automatically fallback to alternative models when the primary model fails. Model fallback is useful for the following:

* Building resilient agents that handle model outages.
* Cost optimization by falling back to cheaper models.
* Provider redundancy across OpenAI, Anthropic, etc.

**API reference:** [`ModelFallbackMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/model_fallback/ModelFallbackMiddleware)

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ModelFallbackMiddleware

agent = create_agent(
    model="gpt-6.1-sol",
    tools=[],
    middleware=[
        ModelFallbackMiddleware(
            "gpt-5.4-mini",
            "claude-sonnet-4-6",
        ),
    ],
)
```

Watch this [video guide](https://www.youtube.com/watch?v=8rCRO0DUeIM) demonstrating Model Fallback middleware behavior.

> [accordion] Configuration options
>
> **first\_model** `string | BaseChatModel` *required*
>
> First fallback model to try when the primary model fails. Can be a model identifier string (e.g., `'openai:gpt-5.4-mini'`) or a `BaseChatModel` instance.
>
> \***additional\_models** `string | BaseChatModel`
>
> Additional fallback models to try in order if previous models fail

### Model refusal

> [!NOTE]
>
> `ModelRefusalMiddleware` requires `langchain>=1.4.9`.

Raise [`ModelRefusalError`](https://reference.langchain.com/python/langchain-core/exceptions/ModelRefusalError) when the model refuses, instead of returning the refusal as the agent's final answer. Providers report a refusal, such as a safety-policy refusal, as a successful response, so without this middleware the agent run ends as if it succeeded. Model refusal is useful for the following:

* Failing a run clearly when the model refuses.
* Retrying a refused request on another model with [Model fallback](#model-fallback).

The middleware checks each model response for a [`refusal` content block](../Core%20components/Messages.md#content-block-reference), which OpenAI, Anthropic, and Gemini models produce. It also catches refusals that fail to parse under a structured `response_format`. It does not detect refusals the model writes as ordinary text.

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ModelFallbackMiddleware, ModelRefusalMiddleware

agent = create_agent(
    model="claude-sonnet-5-5",
    tools=[],
    middleware=[
        ModelFallbackMiddleware("gpt-6.1-sol"),
        ModelRefusalMiddleware(),
    ],
)
```

List [`ModelRefusalMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/model_refusal/ModelRefusalMiddleware) after [`ModelFallbackMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/model_fallback/ModelFallbackMiddleware) so the fallback catches the error and retries on the next model. `ModelRetryMiddleware` does not retry refusals. When streaming, text the model sends before refusing can reach the client before the middleware raises.

#### Handle a refusal

Choose how your application responds when the model refuses:

> [accordion] Catch the error and continue
>
> Catch [`ModelRefusalError`](https://reference.langchain.com/python/langchain-core/exceptions/ModelRefusalError) where you invoke the agent. The refused reply is not saved to the thread, so the next message continues the conversation normally, on the same model or a different one:
>
> ```python
> from langchain.agents import create_agent
> from langchain.agents.middleware import ModelRefusalMiddleware
> from langchain_core.exceptions import ModelRefusalError
> from langgraph.checkpoint.memory import InMemorySaver
>
> agent = create_agent(
>     model="claude-sonnet-5-5",
>     tools=[],
>     middleware=[ModelRefusalMiddleware()],
>     checkpointer=InMemorySaver(),
> )
> config = {"configurable": {"thread_id": "1"}}
>
> try:
>     agent.invoke({"messages": [{"role": "user", "content": "..."}]}, config)
> except ModelRefusalError as error:
>     print(error)  # Tell the user the request was refused
>
> # The thread is still usable
> agent.invoke({"messages": [{"role": "user", "content": "Try something else"}]}, config)
> ```

> [accordion] Fall back to another model
>
> List [`ModelFallbackMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/model_fallback/ModelFallbackMiddleware) before `ModelRefusalMiddleware`, as in the example above. When the model refuses, the request is retried on the next model, which can be from the same provider or a different one. A fallback model can still refuse the same request, so combine this with one of the other options for when every model refuses.

> [accordion] Reply to the user after fallback
>
> To reply to the user instead of failing the run when every model refuses, add a middleware before `ModelFallbackMiddleware` that catches the error:
>
> ```python
> from typing import Callable
>
> from langchain.agents import create_agent
> from langchain.agents.middleware import (
>     ModelFallbackMiddleware,
>     ModelRefusalMiddleware,
>     ModelRequest,
>     ModelResponse,
>     wrap_model_call,
> )
> from langchain.messages import AIMessage
> from langchain_core.exceptions import ModelRefusalError
>
>
> @wrap_model_call
> def reply_on_refusal(
>     request: ModelRequest,
>     handler: Callable[[ModelRequest], ModelResponse],
> ) -> ModelResponse:
>     try:
>         return handler(request)
>     except ModelRefusalError:
>         # Every model refused: reply to the user instead of failing the run
>         return ModelResponse(result=[AIMessage("I cannot help with that request.")])
>
>
> agent = create_agent(
>     model="claude-sonnet-5-5",
>     tools=[],
>     middleware=[
>         reply_on_refusal,
>         ModelFallbackMiddleware("gpt-6.1-sol"),
>         ModelRefusalMiddleware(),
>     ],
> )
> ```
>
> When `claude-sonnet-5-5` refuses, the request falls back to `gpt-6.1-sol`. If that model also refuses, `reply_on_refusal` returns the message.

> [accordion] Write custom handling
>
> For other handling, such as recording the refusal in state or calling `interrupt()` to ask a human how to continue, skip `ModelRefusalMiddleware` and check each response for a [`refusal` content block](../Core%20components/Messages.md#content-block-reference) in your own middleware. See [Custom middleware](Custom%20middleware.md).

### Summarization

Automatically summarize conversation history when approaching token limits, preserving recent messages while compressing older context. Summarization is useful for the following:

* Long-running conversations that exceed context windows.
* Multi-turn dialogues with extensive history.
* Applications where preserving full conversation context matters.

> [!NOTE]
>
> Summarization is text-oriented context compression. It does not resize, downsample, or otherwise compress image/audio/video payloads. Recent messages retained by `keep` still include their original multimodal blocks, while older multimodal messages that are summarized are represented only by the generated text summary. For image-heavy applications, store media in a filesystem or object store and pass URLs or file references through message history.

**API reference:** [`SummarizationMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/summarization/SummarizationMiddleware)

```python
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware

agent = create_agent(
    model="gpt-6.1-sol",
    tools=[your_weather_tool, your_calculator_tool],
    middleware=[
        SummarizationMiddleware(
            model="gpt-5.4-mini",
            trigger=("tokens", 4000),
            keep=("messages", 20),
        ),
    ],
)
```

> [accordion] Configuration options
>
> > [!TIP]
> >
> > The `fraction` conditions for `trigger` and `keep` (shown below) rely on a chat model's [profile data](../Core%20components/Models.md#model-profiles) if using `langchain>=1.1`. If data are not available, use another condition or specify manually:
> >
> > ```python
> > from langchain.chat_models import init_chat_model
> >
> > custom_profile = {
> >     "max_input_tokens": 100_000,
> >     # ...
> > }
> > model = init_chat_model("gpt-6.1-sol", profile=custom_profile)
> > ```
>
> **model** `string | BaseChatModel` *required*
>
> Model for generating summaries. Can be a model identifier string (e.g., `'openai:gpt-5.4-mini'`) or a `BaseChatModel` instance. See [`init_chat_model`](https://reference.langchain.com/python/langchain/chat_models/base/init_chat_model) for more information.
>
> **trigger** `ContextSize | TriggerClause | list[ContextSize | TriggerClause] | None`
>
> Condition(s) for triggering summarization. Can be:
>
> * A single [`ContextSize`](https://reference.langchain.com/python/langchain/agents/middleware/summarization/ContextSize) tuple (the specified threshold must be met)
> * A single [`TriggerClause`](https://reference.langchain.com/python/langchain/agents/middleware/summarization/TriggerClause) dict (all specified thresholds must be met - AND logic)
> * A list mixing either form (any item must be met - OR logic)
>
> Supported thresholds are:
>
> * `fraction` (float): Fraction of model's context size (0-1)
> * `tokens` (int): Absolute token count
> * `messages` (int): Message count
>
> A [`ContextSize`](https://reference.langchain.com/python/langchain/agents/middleware/summarization/ContextSize) tuple expresses exactly one threshold. A [`TriggerClause`](https://reference.langchain.com/python/langchain/agents/middleware/summarization/TriggerClause) dict can include one or more thresholds, e.g. `{"tokens": 4000, "messages": 10}`, and all thresholds in the dict must be met (AND).
>
> Each [`TriggerClause`](https://reference.langchain.com/python/langchain/agents/middleware/summarization/TriggerClause) dict must specify at least one threshold. If `trigger` is not provided, summarization will not trigger automatically.
>
> See the API reference for [`ContextSize`](https://reference.langchain.com/python/langchain/agents/middleware/summarization/ContextSize) and [`TriggerClause`](https://reference.langchain.com/python/langchain/agents/middleware/summarization/TriggerClause) for more information.
>
> **keep** `ContextSize` (default: ('messages', 20))
>
> How much context to preserve after summarization. Specify exactly one of:
>
> * `fraction` (float): Fraction of model's context size to keep (0-1)
> * `tokens` (int): Absolute token count to keep
> * `messages` (int): Number of recent messages to keep
>
> See the API reference for [`ContextSize`](https://reference.langchain.com/python/langchain/agents/middleware/summarization/ContextSize) for more information.
>
> **token\_counter** `function`
>
> Custom token counting function. Defaults to character-based counting.
>
> **summary\_prompt** `string`
>
> Custom prompt template for summarization. Uses built-in template if not specified. The template should include `{messages}` placeholder where conversation history will be inserted.
>
> **trim\_tokens\_to\_summarize** `number` (default: 4000)
>
> Maximum number of tokens to include when generating the summary. Messages will be trimmed to fit this limit before summarization.
>
> **summary\_prefix** `string` *deprecated*
>
> **Deprecated:** Use `summary_prompt` to provide the full prompt instead.
>
> **max\_tokens\_before\_summary** `number` *deprecated*
>
> **Deprecated:** Use `trigger: ("tokens", value)` instead. Token threshold for triggering summarization.
>
> **messages\_to\_keep** `number` *deprecated*
>
> **Deprecated:** Use `keep: ("messages", value)` instead. Recent messages to preserve.

> [accordion] Full example
>
> The summarization middleware monitors message token counts and automatically summarizes older messages when thresholds are reached.
>
> **Trigger conditions** control when summarization runs:
>
> * A single threshold triggers when that threshold is met
> * A trigger clause with multiple thresholds triggers only when all thresholds are met (AND logic)
> * A list of trigger conditions triggers when any item is met (OR logic)
> * Each threshold can use `fraction` (of model's context size), `tokens` (absolute count), or `messages` (message count)
>
> **Keep condition** control how much context to preserve (specify exactly one):
>
> * `fraction` - Fraction of model's context size to keep
> * `tokens` - Absolute token count to keep
> * `messages` - Number of recent messages to keep
>
> ```python
> from langchain.agents import create_agent
> from langchain.agents.middleware import SummarizationMiddleware
>
>
> # Single condition: trigger if tokens >= 4000
> agent = create_agent(
>     model="gpt-6.1-sol",
>     tools=[your_weather_tool, your_calculator_tool],
>     middleware=[
>         SummarizationMiddleware(
>             model="gpt-5.4-mini",
>             trigger=("tokens", 4000),
>             keep=("messages", 20),
>         ),
>     ],
> )
>
> # Multiple conditions: trigger if number of tokens >= 3000 OR messages >= 6
> agent2 = create_agent(
>     model="gpt-6.1-sol",
>     tools=[your_weather_tool, your_calculator_tool],
>     middleware=[
>         SummarizationMiddleware(
>             model="gpt-5.4-mini",
>             trigger=[
>                 ("tokens", 3000),
>                 ("messages", 6),
>             ],
>             keep=("messages", 20),
>         ),
>     ],
> )
>
> # AND logic: trigger only when tokens >= 4000 AND messages >= 10
> agent3 = create_agent(
>     model="gpt-6.1-sol",
>     tools=[your_weather_tool, your_calculator_tool],
>     middleware=[
>         SummarizationMiddleware(
>             model="gpt-5.4-mini",
>             trigger={"tokens": 4000, "messages": 10},
>             keep=("messages", 20),
>         ),
>     ],
> )
>
> # Combine AND and OR: trigger if (tokens >= 5000 AND messages >= 3)
> # OR (tokens >= 3000 AND messages >= 6)
> agent4 = create_agent(
>     model="gpt-6.1-sol",
>     tools=[your_weather_tool, your_calculator_tool],
>     middleware=[
>         SummarizationMiddleware(
>             model="gpt-5.4-mini",
>             trigger=[
>                 {"tokens": 5000, "messages": 3},
>                 {"tokens": 3000, "messages": 6},
>             ],
>             keep=("messages", 20),
>         ),
>     ],
> )
>
> # Using fractional limits
> agent5 = create_agent(
>     model="gpt-6.1-sol",
>     tools=[your_weather_tool, your_calculator_tool],
>     middleware=[
>         SummarizationMiddleware(
>             model="gpt-5.4-mini",
>             trigger=("fraction", 0.8),
>             keep=("fraction", 0.3),
>         ),
>     ],
> )
> ```

### Human-in-the-loop

Pause agent execution for human approval, editing, or rejection of tool calls before they execute. [Human-in-the-loop](../Advanced%20usage/Human-in-the-loop.md) is useful for the following:

* High-stakes operations requiring human approval (e.g. database writes, financial transactions).
* Compliance workflows where human oversight is mandatory.
* Long-running conversations where human feedback guides the agent.

**API reference:** [`HumanInTheLoopMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/human_in_the_loop/HumanInTheLoopMiddleware)

The middleware pauses once per model turn by default. Set `interrupt_mode="per_call"` to pause once per tool call, with each interrupt answered by its ID. See [Set the interrupt mode](../Advanced%20usage/Human-in-the-loop.md#set-the-interrupt-mode).

> [!WARNING]
>
> Human-in-the-loop middleware requires a [checkpointer](https://docs.langchain.com/oss/python/langgraph/checkpointers.md#checkpoints) to maintain state across interruptions.

```python
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver


def your_read_email_tool(email_id: str) -> str:
    """Mock function to read an email by its ID."""
    return f"Email content for ID: {email_id}"

def your_send_email_tool(recipient: str, subject: str, body: str) -> str:
    """Mock function to send an email."""
    return f"Email sent to {recipient} with subject '{subject}'"

agent = create_agent(
    model="gpt-6.1-sol",
    tools=[your_read_email_tool, your_send_email_tool],
    checkpointer=InMemorySaver(),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "your_send_email_tool": {
                    "allowed_decisions": ["approve", "edit", "reject"],
                },
                "your_read_email_tool": False,
            }
        ),
    ],
)
```

> [!TIP]
>
> For complete examples, configuration options, and integration patterns, see the [Human-in-the-loop documentation](../Advanced%20usage/Human-in-the-loop.md).

Watch this [video guide](https://www.youtube.com/watch?v=SpfT6-YAVPk) demonstrating Human-in-the-loop middleware behavior.

### Model call limit

Limit the number of model calls to prevent infinite loops or excessive costs. Model call limit is useful for the following:

* Preventing runaway agents from making too many API calls.
* Enforcing cost controls on production deployments.
* Testing agent behavior within specific call budgets.

**API reference:** [`ModelCallLimitMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/model_call_limit/ModelCallLimitMiddleware)

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model="gpt-6.1-sol",
    checkpointer=InMemorySaver(),  # Required for thread limiting
    tools=[],
    middleware=[
        ModelCallLimitMiddleware(
            thread_limit=10,
            run_limit=5,
            exit_behavior="end",
        ),
    ],
)
```

Watch this [video guide](https://www.youtube.com/watch?v=nJEER0uaNkE) demonstrating Model Call Limit middleware behavior.

> [accordion] Configuration options
>
> **thread\_limit** `number`
>
> Maximum model calls across all runs in a thread. Defaults to no limit.
>
> **run\_limit** `number`
>
> Maximum model calls per single invocation. Defaults to no limit.
>
> **exit\_behavior** `string` (default: end)
>
> Behavior when limit is reached. Options: `'end'` (graceful termination) or `'error'` (raise exception)

### Tool call limit

Control agent execution by limiting the number of tool calls, either globally across all tools or for specific tools. Tool call limits are useful for the following:

* Preventing excessive calls to expensive external APIs.
* Limiting web searches or database queries.
* Enforcing rate limits on specific tool usage.
* Protecting against runaway agent loops.

**API reference:** [`ToolCallLimitMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/tool_call_limit/ToolCallLimitMiddleware)

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ToolCallLimitMiddleware

agent = create_agent(
    model="gpt-6.1-sol",
    tools=[search_tool, database_tool],
    middleware=[
        # Global limit
        ToolCallLimitMiddleware(thread_limit=20, run_limit=10),
        # Tool-specific limit
        ToolCallLimitMiddleware(
            tool_name="search",
            thread_limit=5,
            run_limit=3,
        ),
    ],
)
```

Watch this [video guide](https://www.youtube.com/watch?v=6gYlaJJ8t0w) demonstrating Tool Call Limit middleware behavior.

> [accordion] Configuration options
>
> **tool\_name** `string`
>
> Name of specific tool to limit. If not provided, limits apply to **all tools globally**.
>
> **thread\_limit** `number`
>
> Maximum tool calls across all runs in a thread (conversation). Persists across multiple invocations with the same thread ID. Requires a checkpointer to maintain state. `None` means no thread limit.
>
> **run\_limit** `number`
>
> Maximum tool calls per single invocation (one user message → response cycle). Resets with each new user message. `None` means no run limit.
>
> **Note:** At least one of `thread_limit` or `run_limit` must be specified.
>
> **exit\_behavior** `string` (default: continue)
>
> Behavior when limit is reached:
>
> * `'continue'` (default) - Block exceeded tool calls with error messages, let other tools and the model continue. The model decides when to end based on the error messages.
> * `'error'` - Raise a `ToolCallLimitExceededError` exception, stopping execution immediately
> * `'end'` - Stop execution immediately with a `ToolMessage` and AI message for the exceeded tool call. Only works when limiting a single tool; raises `NotImplementedError` if other tools have pending calls.

> [accordion] Full example
>
> Specify limits with:
>
> * **Thread limit** - Max calls across all runs in a conversation (requires checkpointer)
> * **Run limit** - Max calls per single invocation (resets each turn)
>
> Exit behaviors:
>
> * `'continue'` (default) - Block exceeded calls with error messages, agent continues
> * `'error'` - Raise exception immediately
> * `'end'` - Stop with ToolMessage + AI message (single-tool scenarios only)
>
> ```python
> from langchain.agents import create_agent
> from langchain.agents.middleware import ToolCallLimitMiddleware
>
>
> global_limiter = ToolCallLimitMiddleware(thread_limit=20, run_limit=10)
> search_limiter = ToolCallLimitMiddleware(tool_name="search", thread_limit=5, run_limit=3)
> database_limiter = ToolCallLimitMiddleware(tool_name="query_database", thread_limit=10)
> strict_limiter = ToolCallLimitMiddleware(tool_name="scrape_webpage", run_limit=2, exit_behavior="error")
>
> agent = create_agent(
>     model="gpt-6.1-sol",
>     tools=[search_tool, database_tool, scraper_tool],
>     middleware=[global_limiter, search_limiter, database_limiter, strict_limiter],
> )
> ```

### PII detection

Detect and handle Personally Identifiable Information (PII) in conversations using configurable strategies. PII detection is useful for the following:

* Healthcare and financial applications with compliance requirements.
* Customer service agents that need to sanitize logs.
* Any application handling sensitive user data.

> [!NOTE]
>
> With `apply_to_output=True`, `PIIMiddleware` also redacts streamed wire output—text deltas, tool-call args, tool outputs, and state snapshots—via a registered stream transformer. Requires `langchain>=1.3.2`. See [Register transformers on middleware](../Core%20components/Event%20streaming.md#register-transformers-on-middleware).
>
> The stream transformer holds back the last 128 characters of each text block, tool-call argument, and tool output until more text arrives or the block finishes, and runs the detector on the held text plus the new delta. A match that is split across deltas is detected before any part of it is sent, as long as the whole match fits in 128 characters. Keep custom detector matches to 128 characters or fewer: the start of a longer match can be sent before the rest of it arrives. For background, see [OWASP AI Exchange: sensitive output handling](https://owaspai.org/go/sensitiveoutputhandling) and [Split-Boundary Leaks in Streaming Guardrails](https://doi.org/10.5281/zenodo.22909585).

**API reference:** [`PIIMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/pii/PIIMiddleware)

```python
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware

agent = create_agent(
    model="gpt-6.1-sol",
    tools=[],
    middleware=[
        PIIMiddleware("email", strategy="redact", apply_to_input=True),
        PIIMiddleware("credit_card", strategy="mask", apply_to_input=True),
    ],
)
```

#### Custom PII types

You can create custom PII types by providing a `detector` parameter. This allows you to detect patterns specific to your use case beyond the built-in types.

**Three ways to create custom detectors:**

1. **Regex pattern string** - Simple pattern matching

2. **Custom function** - Complex detection logic with validation

```python
import re

from langchain.agents import create_agent
from langchain.agents.middleware import PIIMatch, PIIMiddleware


# Method 1: Regex pattern string
agent1 = create_agent(
    model="gpt-6.1-sol",
    tools=[],
    middleware=[
        PIIMiddleware(
            "api_key",
            detector=r"sk-[a-zA-Z0-9]{32}",
            strategy="block",
        ),
    ],
)

# Method 2: Compiled regex pattern
agent2 = create_agent(
    model="gpt-6.1-sol",
    tools=[],
    middleware=[
        PIIMiddleware(
            "phone_number",
            detector=re.compile(r"\+?\d{1,3}[\s.-]?\d{3,4}[\s.-]?\d{4}"),
            strategy="mask",
        ),
    ],
)

# Method 3: Custom detector function
def detect_ssn(content: str) -> list[PIIMatch]:
    """Detect SSNs with validation."""
    matches: list[PIIMatch] = []
    pattern = r"\d{3}-\d{2}-\d{4}"
    for match in re.finditer(pattern, content):
        ssn = match.group(0)
        # Validate: first 3 digits shouldn't be 000, 666, or 900-999
        first_three = int(ssn[:3])
        if first_three not in [0, 666] and not (900 <= first_three <= 999):
            matches.append({
                "type": "ssn",
                "value": ssn,
                "start": match.start(),
                "end": match.end(),
            })
    return matches

agent3 = create_agent(
    model="gpt-6.1-sol",
    tools=[],
    middleware=[
        PIIMiddleware(
            "ssn",
            detector=detect_ssn,
            strategy="hash",
        ),
    ],
)
```

**Custom detector function signature:**

The detector function must accept a string (content) and return matches:

Returns a list of `PIIMatch` objects:

```python
from langchain.agents.middleware import PIIMatch


def detector(content: str) -> list[PIIMatch]:
    return [
        {
            "type": "custom_type",
            "value": "matched_text",
            "start": 0,
            "end": 12,
        },
        # ... more matches
    ]
```

> [!TIP]
>
> For custom detectors:
>
> * Use regex strings for simple patterns
> * Use RegExp objects when you need flags (e.g., case-insensitive matching)
> * Use custom functions when you need validation logic beyond pattern matching
> * Custom functions give you full control over detection logic and can implement complex validation rules

> [accordion] Configuration options
>
> **pii\_type** `string` *required*
>
> Type of PII to detect. Can be a built-in type (`email`, `credit_card`, `ip`, `mac_address`, `url`) or a custom type name.
>
> **strategy** `string` (default: redact)
>
> How to handle detected PII. Options:
>
> * `'block'` - Raise exception when detected
> * `'redact'` - Replace with `[REDACTED_{PII_TYPE}]`
> * `'mask'` - Partially mask (e.g., `****-****-****-1234`)
> * `'hash'` - Replace with deterministic hash
>
> **detector** `function | regex`
>
> Custom detector function or regex pattern. If not provided, uses built-in detector for the PII type.
>
> **apply\_to\_input** `boolean` (default: True)
>
> Check user messages before model call
>
> **apply\_to\_output** `boolean` (default: False)
>
> Check AI messages after model call. With `langchain>=1.3.2`, also redacts streamed wire output (text deltas, tool-call args, tool outputs, state snapshots) via a registered stream transformer. See [event streaming](../Core%20components/Event%20streaming.md#register-transformers-on-middleware).
>
> **apply\_to\_tool\_results** `boolean` (default: False)
>
> Check tool result messages after execution

### To-do list

Equip agents with task planning and tracking capabilities for complex multi-step tasks. To-do lists are useful for the following:

* Complex multi-step tasks requiring coordination across multiple tools.
* Long-running operations where progress visibility is important.

> [!NOTE]
>
> This middleware automatically provides agents with a `write_todos` tool and system prompts to guide effective task planning.

**API reference:** [`TodoListMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/todo/TodoListMiddleware)

```python
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware

agent = create_agent(
    model="gpt-6.1-sol",
    tools=[read_file, write_file, run_tests],
    middleware=[TodoListMiddleware()],
)
```

Watch this [video guide](https://www.youtube.com/watch?v=yTWocbVKQxw) demonstrating To-do List middleware behavior.

> [accordion] Configuration options
>
> **system\_prompt** `string`
>
> Custom system prompt for guiding todo usage. Uses built-in prompt if not specified.
>
> **tool\_description** `string`
>
> Custom description for the `write_todos` tool. Uses built-in description if not specified.

### LLM tool selector

Use an LLM to intelligently select relevant tools before calling the main model. LLM tool selectors are useful for the following:

* Agents with many tools (10+) where most aren't relevant per query.
* Reducing token usage by filtering irrelevant tools.
* Improving model focus and accuracy.

This middleware uses structured output to ask an LLM which tools are most relevant for the current query. The structured output schema defines the available tool names and descriptions. Model providers often add this structured output information to the system prompt behind the scenes.

**API reference:** [`LLMToolSelectorMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/tool_selection/LLMToolSelectorMiddleware)

```python
from langchain.agents import create_agent
from langchain.agents.middleware import LLMToolSelectorMiddleware

agent = create_agent(
    model="gpt-6.1-sol",
    tools=[tool1, tool2, tool3, tool4, tool5, ...],
    middleware=[
        LLMToolSelectorMiddleware(
            model="gpt-5.4-mini",
            max_tools=3,
            always_include=["search"],
        ),
    ],
)
```

> [accordion] Configuration options
>
> **model** `string | BaseChatModel`
>
> Model for tool selection. Can be a model identifier string (e.g., `'openai:gpt-5.4-mini'`) or a `BaseChatModel` instance. See [`init_chat_model`](https://reference.langchain.com/python/langchain/chat_models/base/init_chat_model) for more information.
>
> Defaults to the agent's main model.
>
> **system\_prompt** `string`
>
> Instructions for the selection model. Uses built-in prompt if not specified.
>
> **max\_tools** `number`
>
> Maximum number of tools to select. If the model selects more, only the first max\_tools will be used. No limit if not specified.
>
> **always\_include** `list[string]`
>
> Tool names to always include regardless of selection. These do not count against the max\_tools limit.

### Model router

> [!NOTE]
>
> `ModelRouterMiddleware` is in beta and requires `langchain>=1.5.0`. Its API may change without notice.

Choose the model for each agent run with a decision model. Before the run starts, the middleware asks the decision model to pick one of your named `ModelChoice` entries based on the latest human message, then uses that model for every model call in the run. The answer is stored in agent state as `model_route`.

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ModelChoice, ModelRouterMiddleware
from langchain_typesafe import TypeSafeClassifier

router = ModelRouterMiddleware(
    classifier=TypeSafeClassifier(),
    choices={
        "fast": ModelChoice(
            model="openai:gpt-6-luna",
            criteria="Direct lookups, extraction, and localized changes with explicit targets.",
        ),
        "powerful": ModelChoice(
            model="openai:gpt-6.1-sol",
            criteria="Architecture, novel root-cause reasoning, and high-stakes decisions.",
        ),
    },
    instructions="Choose the least costly model that can complete the task safely.",
)

agent = create_agent("openai:gpt-6-luna", middleware=[router])
```

### Auto mode

> [!NOTE]
>
> `AutoModeMiddleware` is in beta and requires `langchain>=1.5.0`. Its API may change without notice.

Block risky tool calls with a decision model. Before each call to a tool you list, the middleware asks the decision model for the probability that the call is risky or not authorized by the user. Calls with a probability of `0.5` or higher return an error `ToolMessage` instead of running. Tools you do not list run without classification. Auto mode blocks calls; to have a person approve them, use [Human-in-the-loop](#human-in-the-loop).

```python
from langchain.agents import create_agent
from langchain.agents.middleware import AutoModeMiddleware
from langchain.tools import tool
from langchain_typesafe import TypeSafeClassifier


@tool
def delete_all_backups() -> str:
    """Delete every backup. This action cannot be undone."""
    return "Backups deleted."


agent = create_agent(
    "openai:gpt-6.1-sol",
    tools=[delete_all_backups],
    middleware=[
        AutoModeMiddleware(
            tools=[delete_all_backups],
            classifier=TypeSafeClassifier(),
        )
    ],
)
```

### Provider tool search

Defer selected tools behind model providers' server-side tool search, so the model discovers them on demand instead of receiving every tool schema up front. Provider tool search is useful for:

* Reducing context bloat when using many tools.
* Improving tool selection accuracy by surfacing only relevant tools.

> [!NOTE]
>
> Requires a model with server-side tool search support: Anthropic (Claude Sonnet 4+/Opus 4+/Haiku 4.5+) or OpenAI (gpt-5.5+). Other providers raise a `ValueError`.

**API reference:** [`ProviderToolSearchMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/provider_tool_search/ProviderToolSearchMiddleware)

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ProviderToolSearchMiddleware

agent = create_agent(
    model="anthropic:claude-opus-4-8",
    tools=[get_weather, lookup_order],
    middleware=[
        ProviderToolSearchMiddleware(searchable_tools=["lookup_order"]),
    ],
)
```

> [accordion] Configuration options
>
> **searchable\_tools** `list[str | BaseTool]`
>
> Tools to defer behind the provider's tool search, given by name or instance. Deferred tools are withheld from the model until its search surfaces them. Tools constructed with `extras={"defer_loading": True}` are deferred regardless of this option; if `searchable_tools` is omitted, only those pre-marked tools are deferred.

> [accordion] Full example
>
> The middleware opts-in all tools included in `searchable_tools` for deferral and search. A tool can also opt into deferral at construction time by setting `extras={"defer_loading": True}`.
>
> ```python
> from langchain.agents import create_agent
> from langchain.agents.middleware import ProviderToolSearchMiddleware
> from langchain.tools import tool
>
>
> # Marked `defer_loading` at construction, so it's deferred on its own —
> # no need to list it in `searchable_tools`.
> @tool(extras={"defer_loading": True})
> def send_email(to: str) -> str:
>     """Send an email."""
>     return "sent"
>
>
> agent = create_agent(
>     model="anthropic:claude-opus-4-8",
>     tools=[send_email],
>     middleware=[ProviderToolSearchMiddleware()],
> )
> ```

### Shell tool

Expose a persistent shell session to agents for command execution. Shell tool middleware is useful for the following:

* Agents that need to execute system commands
* Development and deployment automation tasks
* Testing and validation workflows
* File system operations and script execution

> [!WARNING]
>
> **Security consideration**: Use appropriate execution policies (`HostExecutionPolicy`, `DockerExecutionPolicy`, or `CodexSandboxExecutionPolicy`) to match your deployment's security requirements.

> [!NOTE]
>
> **Limitation**: Persistent shell sessions do not currently work with interrupts (human-in-the-loop). We anticipate adding support for this in the future.

**API reference:** [`ShellToolMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/shell_tool/ShellToolMiddleware)

```python
from langchain.agents import create_agent
from langchain.agents.middleware import (
    ShellToolMiddleware,
    HostExecutionPolicy,
)

agent = create_agent(
    model="gpt-6.1-sol",
    tools=[search_tool],
    middleware=[
        ShellToolMiddleware(
            workspace_root="/workspace",
            execution_policy=HostExecutionPolicy(),
        ),
    ],
)
```

> [accordion] Configuration options
>
> **workspace\_root** `str | Path | None`
>
> Base directory for the shell session. If omitted, a temporary directory is created when the agent starts and removed when it ends.
>
> **startup\_commands** `tuple[str, ...] | list[str] | str | None`
>
> Optional commands executed sequentially after the session starts
>
> **shutdown\_commands** `tuple[str, ...] | list[str] | str | None`
>
> Optional commands executed before the session shuts down
>
> **execution\_policy** `BaseExecutionPolicy | None`
>
> Execution policy controlling timeouts, output limits, and resource configuration. Options:
>
> * `HostExecutionPolicy` - Full host access (default); best for trusted environments where the agent already runs inside a container or VM
> * `DockerExecutionPolicy` - Launches a separate Docker container for each agent run, providing harder isolation
> * `CodexSandboxExecutionPolicy` - Reuses the Codex CLI sandbox for additional syscall/filesystem restrictions
>
> **redaction\_rules** `tuple[RedactionRule, ...] | list[RedactionRule] | None`
>
> Optional redaction rules to sanitize command output before returning it to the model.
>
> > [!WARNING]
> >
> > Redaction rules are applied post execution and do not prevent exfiltration of secrets or sensitive data when using `HostExecutionPolicy`.
>
> **tool\_description** `str | None`
>
> Optional override for the registered shell tool description
>
> **shell\_command** `Sequence[str] | str | None`
>
> Optional shell executable (string) or argument sequence used to launch the persistent session. Defaults to `/bin/bash`.
>
> **env** `Mapping[str, Any] | None`
>
> Optional environment variables to supply to the shell session. Values are coerced to strings before command execution.

> [accordion] Full example
>
> The middleware provides a single persistent shell session that agents can use to execute commands sequentially.
>
> **Execution policies:**
>
> * `HostExecutionPolicy` (default) - Native execution with full host access
> * `DockerExecutionPolicy` - Isolated Docker container execution
> * `CodexSandboxExecutionPolicy` - Sandboxed execution via Codex CLI
>
> ```python
> from langchain.agents import create_agent
> from langchain.agents.middleware import (
>     ShellToolMiddleware,
>     HostExecutionPolicy,
>     DockerExecutionPolicy,
>     RedactionRule,
> )
>
>
> # Basic shell tool with host execution
> agent = create_agent(
>     model="gpt-6.1-sol",
>     tools=[search_tool],
>     middleware=[
>         ShellToolMiddleware(
>             workspace_root="/workspace",
>             execution_policy=HostExecutionPolicy(),
>         ),
>     ],
> )
>
> # Docker isolation with startup commands
> agent_docker = create_agent(
>     model="gpt-6.1-sol",
>     tools=[],
>     middleware=[
>         ShellToolMiddleware(
>             workspace_root="/workspace",
>             startup_commands=["pip install requests", "export PYTHONPATH=/workspace"],
>             execution_policy=DockerExecutionPolicy(
>                 image="python:3.11-slim",
>                 command_timeout=60.0,
>             ),
>         ),
>     ],
> )
>
> # With output redaction (applied post execution)
> agent_redacted = create_agent(
>     model="gpt-6.1-sol",
>     tools=[],
>     middleware=[
>         ShellToolMiddleware(
>             workspace_root="/workspace",
>             redaction_rules=[
>                 RedactionRule(pii_type="api_key", detector=r"sk-[a-zA-Z0-9]{32}"),
>             ],
>         ),
>     ],
> )
> ```

### Filesystem middleware

Context engineering is a main challenge in building effective agents. This is particularly difficult when using tools that return variable-length results (for example, `web_search` and RAG), as long tool results can quickly fill your context window.

`FilesystemMiddleware` from [Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview.md) provides four tools for interacting with both short-term and long-term memory:

* `ls`: List the files in the filesystem
* `read_file`: Read an entire file or a certain number of lines from a file
* `write_file`: Write a new file to the filesystem
* `edit_file`: Edit an existing file in the filesystem

```python
from langchain.agents import create_agent
from deepagents.middleware.filesystem import FilesystemMiddleware

# FilesystemMiddleware is included by default in create_deep_agent
# You can customize it if building a custom agent
agent = create_agent(
    model="claude-sonnet-4-6",
    middleware=[
        FilesystemMiddleware(
            backend=None,  # Optional: custom backend (defaults to StateBackend)
            system_prompt="Write to the filesystem when...",  # Optional custom addition to the system prompt
            custom_tool_descriptions={
                "ls": "Use the ls tool when...",
                "read_file": "Use the read_file tool to..."
            },  # Optional: Custom descriptions for filesystem tools
            tools=["read_file", "ls", "glob", "grep"],  # Optional: Allowlist restricting which filesystem tools are exposed
        ),
    ],
)
```

#### Short-term vs. long-term filesystem

By default, these tools write to a local "filesystem" in your graph state. To enable persistent storage across threads, configure a `CompositeBackend` that routes specific paths (like `/memories/`) to a `StoreBackend`.

```python
from langchain.agents import create_agent
from deepagents.middleware import FilesystemMiddleware
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from langgraph.store.memory import InMemoryStore

store = InMemoryStore()

agent = create_agent(
    model="claude-sonnet-4-6",
    store=store,
    middleware=[
        FilesystemMiddleware(
            backend=CompositeBackend(
                default=StateBackend(),
                routes={"/memories/": StoreBackend()}
            ),
            custom_tool_descriptions={
                "ls": "Use the ls tool when...",
                "read_file": "Use the read_file tool to..."
            }  # Optional: Custom descriptions for filesystem tools
        ),
    ],
)
```

When you configure a `CompositeBackend` with a `StoreBackend` for `/memories/`, any files prefixed with **/memories/** are saved to persistent storage and survive across different threads. Files without this prefix remain in ephemeral state storage.

### Subagent

Handing off tasks to subagents isolates context, keeping the main (supervisor) agent's context window clean while still going deep on a task.

The subagents middleware from [Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview.md) allows you to supply subagents through a `task` tool.

```python Google
from deepagents.backends import StateBackend
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get the weather in a city."""
    return f"The weather in {city} is sunny."


agent = create_agent(
    model="google_genai:gemini-4-hydrogen",
    middleware=[
        SubAgentMiddleware(
            backend=StateBackend(),
            subagents=[
                {
                    "name": "weather",
                    "description": "This subagent can get weather in cities.",
                    "system_prompt": (
                        "Use the get_weather tool to get the weather in a city."
                    ),
                    "tools": [get_weather],
                    "model": "gpt-6.1-sol",
                    "middleware": [],
                }
            ],
        )
    ],
)
```

```python OpenAI
from deepagents.backends import StateBackend
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get the weather in a city."""
    return f"The weather in {city} is sunny."


agent = create_agent(
    model="openai:gpt-6.1-sol",
    middleware=[
        SubAgentMiddleware(
            backend=StateBackend(),
            subagents=[
                {
                    "name": "weather",
                    "description": "This subagent can get weather in cities.",
                    "system_prompt": (
                        "Use the get_weather tool to get the weather in a city."
                    ),
                    "tools": [get_weather],
                    "model": "gpt-6.1-sol",
                    "middleware": [],
                }
            ],
        )
    ],
)
```

```python Anthropic
from deepagents.backends import StateBackend
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get the weather in a city."""
    return f"The weather in {city} is sunny."


agent = create_agent(
    model="anthropic:claude-sonnet-5",
    middleware=[
        SubAgentMiddleware(
            backend=StateBackend(),
            subagents=[
                {
                    "name": "weather",
                    "description": "This subagent can get weather in cities.",
                    "system_prompt": (
                        "Use the get_weather tool to get the weather in a city."
                    ),
                    "tools": [get_weather],
                    "model": "gpt-6.1-sol",
                    "middleware": [],
                }
            ],
        )
    ],
)
```

```python OpenRouter
from deepagents.backends import StateBackend
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get the weather in a city."""
    return f"The weather in {city} is sunny."


agent = create_agent(
    model="openrouter:z-ai/glm-5.2",
    middleware=[
        SubAgentMiddleware(
            backend=StateBackend(),
            subagents=[
                {
                    "name": "weather",
                    "description": "This subagent can get weather in cities.",
                    "system_prompt": (
                        "Use the get_weather tool to get the weather in a city."
                    ),
                    "tools": [get_weather],
                    "model": "gpt-6.1-sol",
                    "middleware": [],
                }
            ],
        )
    ],
)
```

```python Fireworks
from deepagents.backends import StateBackend
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get the weather in a city."""
    return f"The weather in {city} is sunny."


agent = create_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    middleware=[
        SubAgentMiddleware(
            backend=StateBackend(),
            subagents=[
                {
                    "name": "weather",
                    "description": "This subagent can get weather in cities.",
                    "system_prompt": (
                        "Use the get_weather tool to get the weather in a city."
                    ),
                    "tools": [get_weather],
                    "model": "gpt-6.1-sol",
                    "middleware": [],
                }
            ],
        )
    ],
)
```

```python Baseten
from deepagents.backends import StateBackend
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get the weather in a city."""
    return f"The weather in {city} is sunny."


agent = create_agent(
    model="baseten:zai-org/GLM-5.2",
    middleware=[
        SubAgentMiddleware(
            backend=StateBackend(),
            subagents=[
                {
                    "name": "weather",
                    "description": "This subagent can get weather in cities.",
                    "system_prompt": (
                        "Use the get_weather tool to get the weather in a city."
                    ),
                    "tools": [get_weather],
                    "model": "gpt-6.1-sol",
                    "middleware": [],
                }
            ],
        )
    ],
)
```

```python Ollama
from deepagents.backends import StateBackend
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get the weather in a city."""
    return f"The weather in {city} is sunny."


agent = create_agent(
    model="ollama:north-mini-code-1.0",
    middleware=[
        SubAgentMiddleware(
            backend=StateBackend(),
            subagents=[
                {
                    "name": "weather",
                    "description": "This subagent can get weather in cities.",
                    "system_prompt": (
                        "Use the get_weather tool to get the weather in a city."
                    ),
                    "tools": [get_weather],
                    "model": "gpt-6.1-sol",
                    "middleware": [],
                }
            ],
        )
    ],
)
```

A declarative subagent requires a **name**, **description**, **model**, and **tools**. You can also set a **system prompt** and additional **middleware**. This can be particularly useful when you want to give the subagent an additional state key to share with the main agent.

For more complex use cases, you can also provide your own prebuilt LangGraph graph as a subagent.

```python Google
from deepagents import CompiledSubAgent
from deepagents.backends import StateBackend
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.messages import AIMessage
from langgraph.graph import END, START, MessagesState, StateGraph


# Create a custom LangGraph graph
def create_weather_graph():
    workflow = StateGraph(MessagesState)

    def respond(_state: MessagesState):
        return {"messages": [AIMessage(content="The weather is sunny.")]}

    workflow.add_node("respond", respond)
    workflow.add_edge(START, "respond")
    workflow.add_edge("respond", END)
    return workflow.compile()


weather_graph = create_weather_graph()

# Wrap it in a CompiledSubAgent
weather_subagent = CompiledSubAgent(
    name="weather",
    description="This subagent can get weather in cities.",
    runnable=weather_graph,
)

agent = create_agent(
    model="google_genai:gemini-4-hydrogen",
    middleware=[
        SubAgentMiddleware(
            backend=StateBackend(),
            subagents=[weather_subagent],
        )
    ],
)
```

```python OpenAI
from deepagents import CompiledSubAgent
from deepagents.backends import StateBackend
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.messages import AIMessage
from langgraph.graph import END, START, MessagesState, StateGraph


# Create a custom LangGraph graph
def create_weather_graph():
    workflow = StateGraph(MessagesState)

    def respond(_state: MessagesState):
        return {"messages": [AIMessage(content="The weather is sunny.")]}

    workflow.add_node("respond", respond)
    workflow.add_edge(START, "respond")
    workflow.add_edge("respond", END)
    return workflow.compile()


weather_graph = create_weather_graph()

# Wrap it in a CompiledSubAgent
weather_subagent = CompiledSubAgent(
    name="weather",
    description="This subagent can get weather in cities.",
    runnable=weather_graph,
)

agent = create_agent(
    model="openai:gpt-6.1-sol",
    middleware=[
        SubAgentMiddleware(
            backend=StateBackend(),
            subagents=[weather_subagent],
        )
    ],
)
```

```python Anthropic
from deepagents import CompiledSubAgent
from deepagents.backends import StateBackend
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.messages import AIMessage
from langgraph.graph import END, START, MessagesState, StateGraph


# Create a custom LangGraph graph
def create_weather_graph():
    workflow = StateGraph(MessagesState)

    def respond(_state: MessagesState):
        return {"messages": [AIMessage(content="The weather is sunny.")]}

    workflow.add_node("respond", respond)
    workflow.add_edge(START, "respond")
    workflow.add_edge("respond", END)
    return workflow.compile()


weather_graph = create_weather_graph()

# Wrap it in a CompiledSubAgent
weather_subagent = CompiledSubAgent(
    name="weather",
    description="This subagent can get weather in cities.",
    runnable=weather_graph,
)

agent = create_agent(
    model="anthropic:claude-sonnet-5",
    middleware=[
        SubAgentMiddleware(
            backend=StateBackend(),
            subagents=[weather_subagent],
        )
    ],
)
```

```python OpenRouter
from deepagents import CompiledSubAgent
from deepagents.backends import StateBackend
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.messages import AIMessage
from langgraph.graph import END, START, MessagesState, StateGraph


# Create a custom LangGraph graph
def create_weather_graph():
    workflow = StateGraph(MessagesState)

    def respond(_state: MessagesState):
        return {"messages": [AIMessage(content="The weather is sunny.")]}

    workflow.add_node("respond", respond)
    workflow.add_edge(START, "respond")
    workflow.add_edge("respond", END)
    return workflow.compile()


weather_graph = create_weather_graph()

# Wrap it in a CompiledSubAgent
weather_subagent = CompiledSubAgent(
    name="weather",
    description="This subagent can get weather in cities.",
    runnable=weather_graph,
)

agent = create_agent(
    model="openrouter:z-ai/glm-5.2",
    middleware=[
        SubAgentMiddleware(
            backend=StateBackend(),
            subagents=[weather_subagent],
        )
    ],
)
```

```python Fireworks
from deepagents import CompiledSubAgent
from deepagents.backends import StateBackend
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.messages import AIMessage
from langgraph.graph import END, START, MessagesState, StateGraph


# Create a custom LangGraph graph
def create_weather_graph():
    workflow = StateGraph(MessagesState)

    def respond(_state: MessagesState):
        return {"messages": [AIMessage(content="The weather is sunny.")]}

    workflow.add_node("respond", respond)
    workflow.add_edge(START, "respond")
    workflow.add_edge("respond", END)
    return workflow.compile()


weather_graph = create_weather_graph()

# Wrap it in a CompiledSubAgent
weather_subagent = CompiledSubAgent(
    name="weather",
    description="This subagent can get weather in cities.",
    runnable=weather_graph,
)

agent = create_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    middleware=[
        SubAgentMiddleware(
            backend=StateBackend(),
            subagents=[weather_subagent],
        )
    ],
)
```

```python Baseten
from deepagents import CompiledSubAgent
from deepagents.backends import StateBackend
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.messages import AIMessage
from langgraph.graph import END, START, MessagesState, StateGraph


# Create a custom LangGraph graph
def create_weather_graph():
    workflow = StateGraph(MessagesState)

    def respond(_state: MessagesState):
        return {"messages": [AIMessage(content="The weather is sunny.")]}

    workflow.add_node("respond", respond)
    workflow.add_edge(START, "respond")
    workflow.add_edge("respond", END)
    return workflow.compile()


weather_graph = create_weather_graph()

# Wrap it in a CompiledSubAgent
weather_subagent = CompiledSubAgent(
    name="weather",
    description="This subagent can get weather in cities.",
    runnable=weather_graph,
)

agent = create_agent(
    model="baseten:zai-org/GLM-5.2",
    middleware=[
        SubAgentMiddleware(
            backend=StateBackend(),
            subagents=[weather_subagent],
        )
    ],
)
```

```python Ollama
from deepagents import CompiledSubAgent
from deepagents.backends import StateBackend
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.messages import AIMessage
from langgraph.graph import END, START, MessagesState, StateGraph


# Create a custom LangGraph graph
def create_weather_graph():
    workflow = StateGraph(MessagesState)

    def respond(_state: MessagesState):
        return {"messages": [AIMessage(content="The weather is sunny.")]}

    workflow.add_node("respond", respond)
    workflow.add_edge(START, "respond")
    workflow.add_edge("respond", END)
    return workflow.compile()


weather_graph = create_weather_graph()

# Wrap it in a CompiledSubAgent
weather_subagent = CompiledSubAgent(
    name="weather",
    description="This subagent can get weather in cities.",
    runnable=weather_graph,
)

agent = create_agent(
    model="ollama:north-mini-code-1.0",
    middleware=[
        SubAgentMiddleware(
            backend=StateBackend(),
            subagents=[weather_subagent],
        )
    ],
)
```

`SubAgentMiddleware` exposes only the subagents you provide. Configure each subagent's model and tools in its specification. Use `create_deep_agent` to include the default `general-purpose` subagent and the default Deep Agents middleware stack.

### Rubric grading

> [!NOTE]
>
> `RubricMiddleware` requires `deepagents>=0.6.5`.

Some tasks have a clear definition of "done" that an agent cannot reliably hit on the first try. `RubricMiddleware` lets you declare *what done looks like* as a rubric and have the agent self-evaluate and iterate until the rubric is satisfied or a maximum iteration cap is hit.

**API reference:** [`RubricMiddleware`](https://reference.langchain.com/python/deepagents/middleware/rubric/RubricMiddleware)

```python Google
from deepagents import RubricMiddleware, create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver

agent = create_deep_agent(
    model="google_genai:gemini-4-hydrogen",
    middleware=[
        RubricMiddleware(
            model="anthropic:claude-haiku-4-5",
            max_iterations=3,
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

```python OpenAI
from deepagents import RubricMiddleware, create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver

agent = create_deep_agent(
    model="openai:gpt-6.1-sol",
    middleware=[
        RubricMiddleware(
            model="anthropic:claude-haiku-4-5",
            max_iterations=3,
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

```python Anthropic
from deepagents import RubricMiddleware, create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver

agent = create_deep_agent(
    model="anthropic:claude-sonnet-5",
    middleware=[
        RubricMiddleware(
            model="anthropic:claude-haiku-4-5",
            max_iterations=3,
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

```python OpenRouter
from deepagents import RubricMiddleware, create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver

agent = create_deep_agent(
    model="openrouter:z-ai/glm-5.2",
    middleware=[
        RubricMiddleware(
            model="anthropic:claude-haiku-4-5",
            max_iterations=3,
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

```python Fireworks
from deepagents import RubricMiddleware, create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver

agent = create_deep_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    middleware=[
        RubricMiddleware(
            model="anthropic:claude-haiku-4-5",
            max_iterations=3,
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

```python Baseten
from deepagents import RubricMiddleware, create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver

agent = create_deep_agent(
    model="baseten:zai-org/GLM-5.2",
    middleware=[
        RubricMiddleware(
            model="anthropic:claude-haiku-4-5",
            max_iterations=3,
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

```python Ollama
from deepagents import RubricMiddleware, create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver

agent = create_deep_agent(
    model="ollama:north-mini-code-1.0",
    middleware=[
        RubricMiddleware(
            model="anthropic:claude-haiku-4-5",
            max_iterations=3,
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

For full configuration options, streaming events, and a complete code generation example, see [Grading rubrics](https://docs.langchain.com/oss/python/deepagents/rubric.md).

### File search

Provide Glob and Grep search tools over a filesystem. File search middleware is useful for the following:

* Code exploration and analysis
* Finding files by name patterns
* Searching code content with regex
* Large codebases where file discovery is needed

**API reference:** [`FilesystemFileSearchMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/file_search/FilesystemFileSearchMiddleware)

```python
from langchain.agents import create_agent
from langchain.agents.middleware import FilesystemFileSearchMiddleware

agent = create_agent(
    model="gpt-6.1-sol",
    tools=[],
    middleware=[
        FilesystemFileSearchMiddleware(
            root_path="/workspace",
            use_ripgrep=True,
        ),
    ],
)
```

> [accordion] Configuration options
>
> **root\_path** `str` *required*
>
> Root directory to search. All file operations are relative to this path.
>
> **use\_ripgrep** `bool` (default: True)
>
> Whether to use ripgrep for search. Falls back to Python regex if ripgrep is unavailable.
>
> **max\_file\_size\_mb** `int` (default: 10)
>
> Maximum file size to search in MB. Files larger than this are skipped.

> [accordion] Full example
>
> The middleware adds two search tools to agents:
>
> **Glob tool** - Fast file pattern matching:
>
> * Supports patterns like `**/*.py`, `src/**/*.ts`
> * Returns matching file paths sorted by modification time
>
> **Grep tool** - Content search with regex:
>
> * Full regex syntax support
> * Filter by file patterns with `include` parameter
> * Three output modes: `files_with_matches`, `content`, `count`
>
> ```python
> from langchain.agents import create_agent
> from langchain.agents.middleware import FilesystemFileSearchMiddleware
> from langchain.messages import HumanMessage
>
>
> agent = create_agent(
>     model="gpt-6.1-sol",
>     tools=[],
>     middleware=[
>         FilesystemFileSearchMiddleware(
>             root_path="/workspace",
>             use_ripgrep=True,
>             max_file_size_mb=10,
>         ),
>     ],
> )
>
> # Agent can now use glob_search and grep_search tools
> result = agent.invoke({
>     "messages": [HumanMessage("Find all Python files containing 'async def'")]
> })
>
> # The agent will use:
> # 1. glob_search(pattern="**/*.py") to find Python files
> # 2. grep_search(pattern="async def", include="*.py") to find async functions
> ```

### Context editing

Manage conversation context by clearing older tool call outputs when token limits are reached, while preserving recent results. This helps keep context windows manageable in long conversations with many tool calls. Context editing is useful for the following:

* Long conversations with many tool calls that exceed token limits
* Reducing token costs by removing older tool outputs that are no longer relevant
* Maintaining only the most recent N tool results in context

**API reference:** [`ContextEditingMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/context_editing/ContextEditingMiddleware), [`ClearToolUsesEdit`](https://reference.langchain.com/python/langchain/agents/middleware/context_editing/ClearToolUsesEdit)

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ContextEditingMiddleware, ClearToolUsesEdit

agent = create_agent(
    model="gpt-6.1-sol",
    tools=[],
    middleware=[
        ContextEditingMiddleware(
            edits=[
                ClearToolUsesEdit(
                    trigger=100000,
                    keep=3,
                ),
            ],
        ),
    ],
)
```

> [accordion] Configuration options
>
> **edits** `list[ContextEdit]` (default: \[ClearToolUsesEdit()])
>
> List of [`ContextEdit`](https://reference.langchain.com/python/langchain/agents/middleware/context_editing/ContextEdit) strategies to apply
>
> **token\_count\_method** `string` (default: approximate)
>
> Token counting method. Options: `'approximate'` or `'model'`
>
> **[`ClearToolUsesEdit`](https://reference.langchain.com/python/langchain/agents/middleware/context_editing/ClearToolUsesEdit) options:**
>
> **trigger** `number` (default: 100000)
>
> Token count that triggers the edit. When the conversation exceeds this token count, older tool outputs will be cleared.
>
> **clear\_at\_least** `number` (default: 0)
>
> Minimum number of tokens to reclaim when the edit runs. If set to 0, clears as much as needed.
>
> **keep** `number` (default: 3)
>
> Number of most recent tool results that must be preserved. These will never be cleared.
>
> **clear\_tool\_inputs** `boolean` (default: False)
>
> Whether to clear the originating tool call parameters on the AI message. When `True`, tool call arguments are replaced with empty objects.
>
> **exclude\_tools** `list[string]` (default: ())
>
> List of tool names to exclude from clearing. These tools will never have their outputs cleared.
>
> **placeholder** `string` (default: \[cleared])
>
> Placeholder text inserted for cleared tool outputs. This replaces the original tool message content.

> [accordion] Full example
>
> The middleware applies context editing strategies when token limits are reached. The most common strategy is `ClearToolUsesEdit`, which clears older tool results while preserving recent ones.
>
> **How it works:**
>
> 1. Monitor token count in conversation
> 2. When threshold is reached, clear older tool outputs
> 3. Keep most recent N tool results
> 4. Optionally preserve tool call arguments for context
>
> ```python
> from langchain.agents import create_agent
> from langchain.agents.middleware import ContextEditingMiddleware, ClearToolUsesEdit
>
>
> agent = create_agent(
>     model="gpt-6.1-sol",
>     tools=[search_tool, your_calculator_tool, database_tool],
>     middleware=[
>         ContextEditingMiddleware(
>             edits=[
>                 ClearToolUsesEdit(
>                     trigger=2000,
>                     keep=3,
>                     clear_tool_inputs=False,
>                     exclude_tools=[],
>                     placeholder="[cleared]",
>                 ),
>             ],
>         ),
>     ],
> )
> ```

### LLM tool emulator

Emulate tool execution using an LLM for testing purposes, replacing actual tool calls with AI-generated responses. LLM tool emulators are useful for the following:

* Testing agent behavior without executing real tools.
* Developing agents when external tools are unavailable or expensive.
* Prototyping agent workflows before implementing actual tools.

**API reference:** [`LLMToolEmulator`](https://reference.langchain.com/python/langchain/agents/middleware/tool_emulator/LLMToolEmulator)

```python
from langchain.agents import create_agent
from langchain.agents.middleware import LLMToolEmulator

agent = create_agent(
    model="gpt-6.1-sol",
    tools=[get_weather, search_database, send_email],
    middleware=[
        LLMToolEmulator(),  # Emulate all tools
    ],
)
```

> [accordion] Configuration options
>
> **tools** `list[str | BaseTool]`
>
> List of tool names (str) or BaseTool instances to emulate. If `None` (default), ALL tools will be emulated. If empty list `[]`, no tools will be emulated. If array with tool names/instances, only those tools will be emulated.
>
> **model** `string | BaseChatModel`
>
> Model to use for generating emulated tool responses. Can be a model identifier string (e.g., `'google_genai:gemini-4-hydrogen'`) or a `BaseChatModel` instance. Defaults to the agent's model if not specified. See [`init_chat_model`](https://reference.langchain.com/python/langchain/chat_models/base/init_chat_model) for more information.

> [accordion] Full example
>
> The middleware uses an LLM to generate plausible responses for tool calls instead of executing the actual tools.
>
> ```python
> from langchain.agents import create_agent
> from langchain.agents.middleware import LLMToolEmulator
> from langchain.tools import tool
>
>
> @tool
> def get_weather(location: str) -> str:
>     """Get the current weather for a location."""
>     return f"Weather in {location}"
>
> @tool
> def send_email(to: str, subject: str, body: str) -> str:
>     """Send an email."""
>     return "Email sent"
>
>
> # Emulate all tools (default behavior)
> agent = create_agent(
>     model="gpt-6.1-sol",
>     tools=[get_weather, send_email],
>     middleware=[LLMToolEmulator()],
> )
>
> # Emulate specific tools only
> agent2 = create_agent(
>     model="gpt-6.1-sol",
>     tools=[get_weather, send_email],
>     middleware=[LLMToolEmulator(tools=["get_weather"])],
> )
>
> # Use custom model for emulation
> agent4 = create_agent(
>     model="gpt-6.1-sol",
>     tools=[get_weather, send_email],
>     middleware=[LLMToolEmulator(model="claude-sonnet-4-6")],
> )
> ```

## Provider-specific middleware

These middleware are optimized for specific LLM providers. See each provider's documentation for full details and examples.

> [card] [Anthropic](https://docs.langchain.com/oss/python/integrations/middleware/anthropic)
>
> Prompt caching, bash tool, text editor, memory, and file search middleware for Claude models.

> [card] [AWS](https://docs.langchain.com/oss/python/integrations/middleware/aws)
>
> Prompt caching middleware for Amazon Bedrock models.

> [card] [OpenAI](https://docs.langchain.com/oss/python/integrations/middleware/openai)
>
> Content moderation middleware for OpenAI models.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/middleware/built-in.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
