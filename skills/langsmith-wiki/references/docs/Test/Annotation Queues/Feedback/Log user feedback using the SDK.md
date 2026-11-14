# Log user feedback using the SDK

LangSmith makes it easy to attach [feedback](../../../Monitor/Trace/Observability%20concepts.md#feedback) to [traces](../../../Monitor/Trace/Observability%20concepts.md#traces). This feedback can come from users, annotators, automated evaluators, and so on, which is crucial for monitoring and evaluating agents.

This page details how to log feedback using the [SDK](../../../Monitor/Reference/LangSmith%20reference.md). For the structure of feedback objects, refer to [Feedback data format](../../../Monitor/Debug/Data%20type%20reference/Feedback%20data%20format.md).

> [!NOTE]
>
> In an [agent-based workspace](../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

## Use `create_feedback()` / `createFeedback`

> [!NOTE]
>
> **Child runs**
> You can attach user feedback to **any** child run of a trace, not just the trace (root run) itself.
> This is useful for critiquing specific steps of the agent, such as the retrieval step or generation step of a RAG pipeline.

> [!TIP]
>
> **Non-blocking creation (Python only)**
> The Python client will automatically background feedback creation if you pass `trace_id=` to [`create_feedback()`](https://reference.langchain.com/python/langsmith/client/Client/create_feedback).
> This is essential for low-latency environments, where you want to make sure your agent isn't blocked on feedback creation.

The following example creates a trace with two child runs, then logs feedback against the root run and against one of the child runs. The TypeScript snippet shows the equivalent `createFeedback` call shape, assuming a `runId` is already available from your agent.

```python Python
import asyncio

from langsmith import Client, trace, traceable

@traceable
def foo(x):
    return {"y": x * 2}

@traceable
def bar(y):
    return {"z": y - 1}

client = Client()

inputs = {"x": 1}
with trace(name="foobar", inputs=inputs) as root_run:
    result = foo(**inputs)
    result = bar(**result)
    root_run.outputs = result
    trace_id = root_run.id
    child_runs = root_run.child_runs

# Resolve the session_id for the agent environment
if root_run.address is not None:
    resolved = asyncio.run(client.sessions.resolve(**root_run.address))
    session_id = resolved.session_id
else:
    session_id = client.read_project(project_name=root_run.session_name).id

# Provide feedback for a trace (a.k.a. a root run)
client.create_feedback(
    key="user_feedback",
    score=1,
    trace_id=trace_id,
    session_id=session_id,
    comment="the user said that ..."
)

# Provide feedback for a child run
foo_run_id = [run for run in child_runs if run.name == "foo"][0].id
client.create_feedback(
    key="correctness",
    score=0,
    run_id=foo_run_id,
    # trace_id= is optional but recommended to enable batched and backgrounded
    # feedback ingestion.
    trace_id=trace_id,
    session_id=session_id,
)
```

```typescript TypeScript
import { AgentAddress, Client } from "langsmith";
const client = new Client();

    // ... Run your agent and get the run_id...
    // This information can be the result of a user-facing feedback form

// Resolve the session_id for the agent environment
const address = new AgentAddress("<your-agent-id>", "production");
const { session_id: sessionId } = await client.sessions.resolve(address);

await client.createFeedback({
    runId,
    sessionId,
    key: "feedback-key",
    score: 1.0,
    comment: "comment",
});
```

For project-based traces, use `readProject` with the existing project name to get its ID instead of resolving an agent address. For resolution requirements, see [Resolve an agent environment](../../../Monitor/Debug/Viewing%20%26%20managing%20traces/Resolve%20an%20agent%20environment.md).

You can even log feedback for in-progress runs using [`create_feedback()`](https://reference.langchain.com/python/langsmith/client/Client/create_feedback) / [`createFeedback`](https://reference.langchain.com/javascript/langsmith/client/Client). See [Access the current run (span) within a traced function](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Advanced%20tracing%20techniques/Access%20the%20current%20run%20%28span%29%20within%20a%20traced%20function.md) for how to get the run ID of an in-progress run.

## Collect feedback from a user interface

If you need to collect feedback from a browser or other client-side environment without exposing your API key, use **presigned feedback tokens**. These generate a URL scoped to a specific run and feedback key that clients can call directly.

See [Collect feedback with presigned URLs](Collect%20feedback%20with%20presigned%20URLs.md) for the full guide.

To learn more about how to filter traces based on various attributes, including user feedback, see [Filter traces](../../../Monitor/Debug/Viewing%20%26%20managing%20traces/Filter%20traces.md).
