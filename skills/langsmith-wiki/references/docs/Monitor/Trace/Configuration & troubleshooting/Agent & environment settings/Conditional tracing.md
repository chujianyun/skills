# Conditional tracing

When you have the environment variable `LANGSMITH_TRACING=true` set globally, traces are automatically sent to LangSmith. This guide shows you how to disable or customize tracing selectively for specific requests.

Use conditional tracing when you need to:

* **Comply with data retention policies**: Some clients may require zero data retention for compliance or privacy reasons.
* **Handle sensitive operations**: Disable tracing for operations involving PII, credentials, or confidential data.
* **Implement per-tenant configurations**: Route traces to different agent environments or apply different settings based on the customer.
* **Control costs**: Disable tracing for low-value requests while maintaining visibility into critical operations.
* **Support feature flags**: Enable tracing only when specific features or experimental code paths are active.

> [!TIP]
>
> To reduce trace volume by logging only a percentage of all runs, refer to [Set a sampling rate for traces](Set%20a%20sampling%20rate%20for%20traces.md).

The [`tracing_context`](https://reference.langchain.com/python/langsmith/run_helpers/tracing_context) context manager (Python) and [`tracingEnabled`](https://reference.langchain.com/javascript/langsmith/index/RunTree/tracingEnabled) option (TypeScript) allow you to override global tracing settings at runtime, without restructuring your code or changing environment variables.

> [!NOTE]
>
> The following sections provide language-specific examples that you can adapt to your agent logic and business requirements.

> [!NOTE]
>
> In an [agent-based workspace](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

Register each agent before enabling dynamic routing. Replica configurations require each destination environment's `tracer_session_name`. Retrieve those values before enabling replication.

> [tab] Python
>
> ## How tracing context works
>
> When you use the [`tracing_context`](https://reference.langchain.com/python/langsmith/run_helpers/tracing_context) context manager, it overrides the global tracing configuration for code executed within its scope. This means you can keep automatic tracing enabled globally while selectively controlling tracing behavior for specific function calls.
>
> There are three priority levels of control:
>
> 1. **`tracing_context(enabled=...)`**: highest priority (context manager for scoped tracing control).
> 2. **`ls.configure(enabled=...)`**: global configuration (sets global tracing behavior).
> 3. **Environment variables**: lowest priority (`LANGSMITH_TRACING`).
>
> ## Disable tracing for specific invocations
>
> To disable tracing for a specific operation, wrap it in a `tracing_context` with `enabled=False`:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import langsmith as ls
> from langsmith import traceable
>
> # LANGSMITH_TRACING=true is set globally
>
> @traceable
> def my_function(input_text: str):
>     return process(input_text)
>
> # Default invocation - is traced
> result = my_function("regular data")
>
> # Disable tracing for sensitive data
> with ls.tracing_context(enabled=False):
>     result = my_function("sensitive data")  # not traced
> ```
>
> This pattern is useful for one-off cases where you know specific data should not be logged.
>
> ## Enable conditional tracing based on business logic
>
> You can dynamically enable or disable tracing based on runtime conditions, such as client settings or request properties.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import langsmith as ls
> from langsmith import traceable
>
> @traceable
> def my_function(input_text: str):
>     return process(input_text)
>
> def client_requires_zero_retention(client_id: str) -> bool:
>     """
>     Check if a client has a zero-retention policy.
>
>     In production, this would query a database, configuration service,
>     or feature flag system. Consider caching results for performance.
>     """
>     # Example: Query from database or config
>     zero_retention_clients = get_zero_retention_clients()  # Your implementation
>     return client_id in zero_retention_clients
>
> def handle_request(client_id: str, user_input: str):
>     """
>     Process a request with conditional tracing based on client requirements.
>     """
>     should_disable = client_requires_zero_retention(client_id)
>
>     with ls.tracing_context(enabled=not should_disable):
>         return my_function(user_input)
>
> # Example usage
> handle_request("client-a", "some input")  # Traced or not based on client settings
> ```
>
> ## Customize tracing configuration per request
>
> You can also customize tracing settings dynamically, such as routing traces to different agents or adding request-specific metadata.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import langsmith as ls
> from langsmith import traceable
>
> @traceable
> def my_function(input_text: str):
>     return process(input_text)
>
> def handle_request(client_id: str, user_input: str, region: str):
>     """
>     Route traces to registered client-specific agents with custom metadata.
>     """
>     client_tier = get_client_tier(client_id)  # e.g., "enterprise", "standard"
>
>     with ls.tracing_context(
>         enabled=True,
>         address=ls.agent_address(f"client-{client_id}", "production"),
>         tags=["production", f"tier-{client_tier}", f"region-{region}"],
>         metadata={
>             "client_id": client_id,
>             "region": region,
>             "tier": client_tier
>         }
>     ):
>         return my_function(user_input)
>
> # Register client-abc first; traces go to its Production environment
> handle_request("abc", "some input", "us-west")
> ```
>
> This pattern is useful for:
>
> * **Multi-tenant services**: Isolate customer traces under separate agents
> * **Regional deployments**: Track performance and behavior by geographic region
> * **Feature branches**: Route experimental feature traces to the agent's Development environment
> * **User segmentation**: Analyze behavior by user tier, cohort, or A/B test group
>
> ## Work with automatic tracing
>
> The [`tracing_context`](https://reference.langchain.com/python/langsmith/run_helpers/tracing_context) context manager works with automatic tracing. You can keep `LANGSMITH_TRACING=true` set globally and use `tracing_context` to override settings for specific requests:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import os
> import langsmith as ls
>
> # Global environment variable set
> os.environ["LANGSMITH_TRACING"] = "true"
>
> @ls.traceable
> def process_data(data: str):
>     return data.upper()
>
> # Automatically traced (respects LANGSMITH_TRACING)
> process_data("hello")
>
> # Override global setting - disable for this call
> with ls.tracing_context(enabled=False):
>     process_data("sensitive")  # not traced
>
> # Override global setting - enable with custom config
> with ls.tracing_context(
>     enabled=True,
>     address=ls.agent_address("<your-agent-id>", "staging")
> ):
>     process_data("important")  # Traced to the registered agent's Staging environment
> ```
>
> ## Nest tracing contexts
>
> When you nest `tracing_context` blocks, the innermost context takes precedence.
>
> ```python Python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import langsmith as ls
>
> @ls.traceable
> def inner_function(data: str):
>     return data
>
> @ls.traceable
> def outer_function(data: str):
>     # This call respects the inner context
>     return inner_function(data)
>
> # Outer context disables tracing
> with ls.tracing_context(enabled=False):
>     # But inner context re-enables it
>     with ls.tracing_context(enabled=True):
>         outer_function("data")  # is traced
> ```
>
> This can be useful when you want to temporarily enable tracing for debugging within a normally non-traced section.
>
> ## Conditionally redact inputs and outputs
>
> Sometimes you want the trace to be recorded—so you keep run timing, structure, errors, and metadata—but the inputs and outputs should be hidden for specific requests (for example, traces from tenants with strict privacy requirements). This is different from [disabling tracing](#disable-tracing-for-specific-invocations) entirely and from [`Client(hide_inputs=...)`](../Data%20%26%20privacy/Prevent%20logging%20of%20sensitive%20data%20in%20traces.md#hide-inputs-and-outputs), which applies the same redaction to every trace the client sends.
>
> To redact per-request, use [`tracing_context`](https://reference.langchain.com/python/langsmith/run_helpers/tracing_context) with the `replicas` parameter and pass an `updates` dict that overrides `inputs` and `outputs` on the recorded run. Because `tracing_context` is scoped to the current execution context, concurrent requests with different redaction policies do not race.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import langsmith as ls
> from langsmith import traceable
>
> @traceable
> def my_agent(user_input: str) -> str:
>     return process(user_input)
>
> def should_redact(tenant_id: str) -> bool:
>     """Return True if traces for this tenant should have inputs/outputs masked."""
>     return tenant_id in get_redacted_tenants()
>
> def handle_request(tenant_id: str, user_input: str) -> str:
>     replica: dict = {"project_name": "my-project"}
>     if should_redact(tenant_id):
>         # Recorded run will have empty inputs/outputs but full structure,
>         # timing, metadata, and any errors.
>         replica["updates"] = {"inputs": {}, "outputs": {}}
>
>     with ls.tracing_context(replicas=[replica]):
>         return my_agent(user_input)
> ```
>
> You can use any subset of run fields in `updates` (for example, `{"inputs": {"redacted": True}}` to keep a marker, or `{"outputs": {}}` to redact only outputs). The same pattern works for routing different redaction policies to different destinations: each replica can specify its own `project_name`, `api_key`, and `updates`. See [Write traces to multiple destinations with replicas](Write%20traces%20to%20multiple%20destinations%20with%20replicas.md) for the full replica reference.
>
> > [!NOTE]
> >
> > Always set `project_name` on the replica when using `updates` to redact inputs or outputs. If the replica's `project_name` matches the active trace's destination, the `updates` may be dropped and the unredacted inputs/outputs will be sent.
>
> ## Customize tracing in deployed agents
>
> Tracing is enabled by default within [Agent Server](../../../../Deploy/Agent%20Server/Capabilities/Agent%20Server.md). When using a [factory function](../../../../Deploy/Agent%20Server/Server%20customization/Rebuild%20graph%20at%20runtime.md), you can wrap the yielded graph with `tracing_context` to control tracing per-execution. This is useful for adding custom metadata, disabling tracing entirely, or customizing tracing based on the authenticated user.
>
> ### Disable tracing for a graph
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import contextlib
> import langsmith as ls
> from langgraph_sdk.runtime import ServerRuntime
>
>
> @contextlib.asynccontextmanager
> async def make_graph(runtime: ServerRuntime):
>     graph = build_my_graph()
>
>     # You can use tracing_context to dynamically enable/disable tracing,
>     # set metadata or tags, select an agent environment, etc.
>     with ls.tracing_context(enabled=False, metadata={"foo": "bar"}):
>         yield graph
> ```
>
> ### Per-user tracing
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import contextlib
> import langsmith as ls
> from langgraph_sdk.runtime import ServerRuntime
>
> def get_agent_for_user(user_id: str) -> str | None:
>     ...
>     return "<your-agent-id>"
>
> graph = build_my_graph()
>
> @contextlib.asynccontextmanager
> async def make_graph(runtime: ServerRuntime):
>     user = runtime.user
>     # Select a registered agent for the user or disable tracing
>     agent_id = get_agent_for_user(user.identity)
>
>     if agent_id is None:
>         with ls.tracing_context(enabled=False):
>             yield graph
>     else:
>         with ls.tracing_context(
>             enabled=True,
>             address=ls.agent_address(agent_id, "production"),
>             metadata={"user_id": user.identity, "foo": "bar"},
>         ):
>             yield graph
> ```
>
> ## Reusable tracing wrapper
>
> Create a decorator to automatically apply conditional tracing logic.
>
> ```python Python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import functools
> import langsmith as ls
> from langsmith import traceable
>
> def conditional_trace(check_function):
>     """
>     Decorator that conditionally traces based on a check function.
>
>     Args:
>         check_function: Function that returns True if tracing should be enabled
>     """
>     def decorator(func):
>         traced_func = traceable(func)
>
>         @functools.wraps(func)
>         def wrapper(*args, **kwargs):
>             should_trace = check_function(*args, **kwargs)
>             with ls.tracing_context(enabled=should_trace):
>                 return traced_func(*args, **kwargs)
>         return wrapper
>     return decorator
>
> # Usage
> def should_trace_client(client_id: str, *args, **kwargs) -> bool:
>     return not client_requires_zero_retention(client_id)
>
> @conditional_trace(should_trace_client)
> def process_request(client_id: str, data: str):
>     return data.upper()
>
> # Automatically applies conditional tracing based on client_id
> process_request("client-a", "some data")
> ```

> [tab] TypeScript
>
> ## How tracing enabled works
>
> In TypeScript, you control tracing per-function using the [`tracingEnabled`](https://reference.langchain.com/javascript/langsmith/index/RunTree/tracingEnabled) parameter when calling [`traceable()`](https://reference.langchain.com/python/langsmith/run_helpers/traceable). This allows you to selectively enable or disable tracing at the function level.
>
> A two-level system where tracing is controlled per-function:
>
> 1. **`tracingEnabled` parameter**: highest priority (pass to [`traceable()`](https://reference.langchain.com/python/langsmith/run_helpers/traceable) config).
> 2. **Environment variables**: lowest priority (`LANGSMITH_TRACING`).
>
> ## Disable tracing for specific invocations
>
> To disable tracing for a specific operation, create a version of your traceable function with `tracingEnabled: false`:
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { traceable } from "langsmith/traceable";
>
> const myFunction = traceable(
>     (inputText: string) => {
>         return process(inputText);
>     },
>     { name: "my_function" }
> );
>
> // Default invocation - is traced
> await myFunction("regular data");
>
> // Disable tracing for sensitive data
> const myFunctionNoTrace = traceable(
>     (inputText: string) => {
>         return process(inputText);
>     },
>     { name: "my_function", tracingEnabled: false }
> );
>
> await myFunctionNoTrace("sensitive data");  // not traced
> ```
>
> This pattern is useful for one-off cases where you know specific data should not be logged.
>
> ## Enable conditional tracing based on business logic
>
> You may need to control tracing dynamically based on runtime conditions—such as client privacy requirements, regulatory compliance, or feature flags.
>
> In TypeScript, the most efficient approach is to create both traced and non-traced variants of your function upfront, then select between them at runtime based on your business logic. This avoids the performance overhead of creating new traced wrappers on every request while still providing fine-grained control over when tracing occurs. For example:
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { traceable } from "langsmith/traceable";
>
> // Define the core logic once
> function processText(inputText: string): string {
>     // Your actual processing logic
>     return inputText.toUpperCase();
> }
>
> // Create traced and non-traced variants upfront
> const myFunction = traceable(processText, { name: "my_function" });
> const myFunctionNoTrace = traceable(processText, {
>     name: "my_function",
>     tracingEnabled: false
> });
>
> function clientRequiresZeroRetention(clientId: string): boolean {
>     /**
>      * Check if a client has a zero-retention policy.
>      *
>      * In production, this would query a database, configuration service,
>      * or feature flag system. Consider caching results for performance.
>      */
>     const zeroRetentionClients = getZeroRetentionClients();  // Your implementation
>     return zeroRetentionClients.includes(clientId);
> }
>
> async function handleRequest(clientId: string, userInput: string) {
>     /**
>      * Process a request with conditional tracing based on client requirements.
>      * Efficiently selects pre-created traced or non-traced variant.
>      */
>     const shouldDisable = clientRequiresZeroRetention(clientId);
>
>     // Select the appropriate pre-created variant
>     const fn = shouldDisable ? myFunctionNoTrace : myFunction;
>     return await fn(userInput);
> }
>
> // Example usage
> await handleRequest("client-a", "some input");  // Traced or not based on client settings
> ```
>
> ## Work with automatic tracing
>
> The [`tracingEnabled`](https://reference.langchain.com/javascript/langsmith/index/RunTree/tracingEnabled) option works seamlessly with automatic tracing. You can keep `LANGSMITH_TRACING=true` set globally and use `tracingEnabled` to override settings for specific functions.
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { AgentAddress } from "langsmith";
> import { traceable } from "langsmith/traceable";
>
> // Global tracing enabled via environment
> process.env.LANGSMITH_TRACING = "true";
>
> const processData = traceable(
>     (data: string) => {
>         return data.toUpperCase();
>     },
>     { name: "process_data" }
> );
>
> // Automatically traced (respects LANGSMITH_TRACING)
> await processData("hello");
>
> // Override global setting - disable for this call
> const processDataNoTrace = traceable(
>     (data: string) => {
>         return data.toUpperCase();
>     },
>     { name: "process_data", tracingEnabled: false }
> );
>
> await processDataNoTrace("sensitive");  // not traced
>
> // Override global setting - enable with custom config
> const processDataCustom = traceable(
>     (data: string) => {
>         return data.toUpperCase();
>     },
>     {
>         name: "process_data",
>         address: new AgentAddress("<your-agent-id>", "staging"),
>         tracingEnabled: true
>     }
> );
>
> await processDataCustom("important");  // Traced to the registered agent's Staging environment
> ```

## Comparison with sampling

Conditional tracing and [sampling](Set%20a%20sampling%20rate%20for%20traces.md) serve different purposes:

| Feature | Conditional tracing | Sampling |
| - | - | - |
| **Control** | Deterministic (explicit enable/disable) | Probabilistic (random sampling) |
| **Use case** | Business logic, compliance, per-request decisions | Cost optimization, high-volume observability |
| **Predictability** | Guaranteed behavior for specific requests | Statistical representation of traffic |
| **Configuration** | Runtime code logic | Environment variable or client config |

You can combine both approaches for fine-grained control.

## Related

* [Trace without environment variables](Trace%20without%20setting%20environment%20variables.md): Configure tracing programmatically instead of using environment variables.
* [Set a sampling rate for traces](Set%20a%20sampling%20rate%20for%20traces.md): Probabilistically sample traces to reduce volume
* [Mask inputs and outputs](../Data%20%26%20privacy/Prevent%20logging%20of%20sensitive%20data%20in%20traces.md): Hide sensitive data in traces instead of disabling tracing entirely.
* [Add metadata and tags to traces](../Data%20%26%20privacy/Add%20metadata%20and%20tags%20to%20traces.md): Categorize and filter traces with custom attributes.
