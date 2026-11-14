# Set a sampling rate for traces

When working with high-volume applications, you may not want to log every trace to LangSmith. Sampling rates allow you to control what percentage of traces are logged, helping you balance observability needs with cost considerations.

This guide shows you how to set a global sampling rate with the `LANGSMITH_TRACING_SAMPLING_RATE` environment variable, and how to apply different sampling rates per `Client` instance for finer-grained control over which operations are traced.

> [!TIP]
>
> To enable or disable tracing for specific requests based on runtime conditions (such as data sensitivity, tenant, or feature flag), refer to [Conditional tracing](Conditional%20tracing.md).

## Set a global sampling rate

> [!NOTE]
>
> This section is relevant for those using the [LangSmith SDK](../../../Reference/LangSmith%20reference.md) or [LangChain](https://docs.langchain.com/oss/python/langchain/overview.md), not for those logging directly with the LangSmith API.

By default, all traces are logged to LangSmith. To down-sample the number of traces logged to LangSmith, set the `LANGSMITH_TRACING_SAMPLING_RATE` environment variable to any float between `0` (no traces) and `1` (all traces). For instance, setting the following environment variable will log 75% of the traces.

```bash
export LANGSMITH_TRACING_SAMPLING_RATE=0.75
```

This works for the `traceable` decorator and `RunTree` objects.

## Set different sampling rates per client

You can also set sampling rates on specific `Client` instances and use the [`tracing_context`](../../Tracing%20setup/Manual%20instrumentation/Custom%20instrumentation.md#use-the-trace-context-manager-python-only) context manager:

```python
from langsmith import Client, tracing_context

# Create clients with different sampling rates
client_1 = Client(tracing_sampling_rate=0.5)  # 50% sampling
client_2 = Client(tracing_sampling_rate=0.25)  # 25% sampling
client_no_trace = Client(tracing_sampling_rate=0.0)  # No tracing

# Use different sampling rates for different operations
with tracing_context(client=client_1):
    # Your code here - will be traced with 50% sampling rate
    agent_1.invoke(...)

with tracing_context(client=client_2):
    # Your code here - will be traced with 25% sampling rate
    agent_1.invoke(...)

with tracing_context(client=client_no_trace):
    # Your code here - will not be traced
    agent_1.invoke(...)
```

This allows you to control sampling rates at the operation level.

## Sampling or conditional tracing

Sampling provides **probabilistic** control over trace volume, while [conditional tracing](Conditional%20tracing.md) provides **deterministic** control based on business logic.

Use **sampling** when you want to reduce overall trace volume while maintaining statistical representation of your application's behavior.

Use [conditional tracing](Conditional%20tracing.md) when you need guaranteed tracing behavior for specific requests, such as:

* Disabling tracing for clients with zero-retention policies.
* Routing traces to different projects based on tenant.
* Handling sensitive data that should never be traced.

You can combine both approaches for fine-grained control over your observability strategy.
