# Trace JS functions in serverless environments

> [!NOTE]
>
> This section is relevant for those using the LangSmith JS SDK version 0.2.0 and higher. If you are tracing using LangChain.js or LangGraph.js in serverless environments, see [this guide](../../Tracing%20setup/Integrations/Agent%20frameworks/Trace%20LangChain%20agents%20%28Python%20and%20JS-TS%29.md#ensure-all-traces-are-submitted-before-exiting).

When tracing JavaScript functions, LangSmith will trace runs in the background by default to avoid adding latency. In serverless environments where the execution context may be terminated abruptly, it's important to ensure that all tracing data is properly flushed before the function completes.

To make sure this occurs, you can either:

* Set an environment variable named `LANGSMITH_TRACING_BACKGROUND` to `"false"`. This will cause your traced functions to wait for tracing to complete before returning.
  * Note that this is named differently from the [environment variable](../../Tracing%20setup/Integrations/Agent%20frameworks/Trace%20LangChain%20agents%20%28Python%20and%20JS-TS%29.md#ensure-all-traces-are-submitted-before-exiting) in LangChain.js because LangSmith can be used without LangChain.
* Pass a custom client into your traced runs and `await` the `client.awaitPendingTraceBatches();` method.

Here's an example of using `awaitPendingTraceBatches` alongside the [`traceable`](../../Tracing%20setup/Manual%20instrumentation/Custom%20instrumentation.md) method:

```typescript
import { Client } from "langsmith";
import { traceable } from "langsmith/traceable";
const langsmithClient = new Client({});
const tracedFn = traceable(
  async () => {
    return "Some return value";
  },
  {
    client: langsmithClient,
  }
);
const res = await tracedFn();
await langsmithClient.awaitPendingTraceBatches();
```

## Rate limits at high concurrency[ ](#rate-limits-at-high-concurrency "Direct link to rate limits at high concurrency")

By default, the LangSmith client will batch operations as your traced run executions, sending a new batch every few milliseconds.

This works well in most situations, but if your traced function is long-running and you have very high concurrency, you may also hit rate limits related to overall request count.

If you are seeing rate limit errors related to this, you can try setting `manualFlushMode: true` in your client like this:

```typescript
import { Client } from "langsmith";
const langsmithClient = new Client({  manualFlushMode: true,});
const myTracedFunc = traceable(
  async () => {
    // Your logic here...
  },
  { client: langsmithClient }
);
```

And then manually calling `client.flush()` like this before your serverless function closes:

```typescript
try {
  await myTracedFunc();
} finally {
  await langsmithClient.flush();
}
```

Note that this will prevent runs from appearing in the LangSmith UI until you call `.flush()`.
