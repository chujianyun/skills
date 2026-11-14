# How to cancel a run

> Cancel a single run or multiple runs via the API, and choose between interrupt and rollback actions.

This guide covers how to cancel runs for your agent via the [LangSmith Agent Server API](../../../Get%20started/Reference/Agent%20Server%20API/Agent%20Server%20API%20reference.md). You can cancel a single run by ID or cancel multiple runs by thread or status. Cancellation is useful for stopping long-running or stuck runs, or when a user abandons a request.

## Setup

Create a client and thread:

> [tab] Python
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph_sdk import get_client
>
> client = get_client(url=<DEPLOYMENT_URL>)
> assistant_id = "agent"
> thread = await client.threads.create()
> ```

> [tab] Javascript
>
> ```js theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { Client } from "@langchain/langgraph-sdk";
>
> const client = new Client({ apiUrl: <DEPLOYMENT_URL> });
> const assistantID = "agent";
> const thread = await client.threads.create();
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
>   --url <DEPLOYMENT_URL>/threads \
>   --header 'Content-Type: application/json' \
>   --data '{}'
> ```

## Cancel a single run

The following examples create a run, cancel it with different options, and print the run to show what you get in each case. You can cancel runs in `pending` or `running` status. Trying to cancel a run that is not in `pending` or `running` status will result in an error.

### Cancel with interrupt (default)

**Interrupt** stops the worker executing the run and marks the run as `interrupted`. Nothing is deleted:

* The run record remains (with status `interrupted`). You can fetch it, inspect inputs/outputs, and see the execution history.
* All checkpoints for that run remain stored. The thread state at the last completed step is preserved.
* You can later resume from a checkpoint (for example, with [time travel](../Time%20travel%20using%20the%20server%20API.md)) or inspect the partial state.

Use **interrupt** when you want to stop a run but keep it for debugging, auditing, or resuming from a checkpoint.

> [tab] Python
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> run = await client.runs.create(
>     thread["thread_id"],
>     assistant_id,
>     input={"messages": [{"role": "user", "content": "Long task"}]},
> )
> await client.runs.cancel(thread["thread_id"], run["run_id"])
>
> run_after = await client.runs.get(thread["thread_id"], run["run_id"], wait=True)
> print(run_after["status"])   # "interrupted"
> ```

> [tab] Javascript
>
> ```js theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> const run = await client.runs.create(
>     thread["thread_id"],
>     assistantID,
>     { input: { messages: [{ role: "user", content: "Long task" }] } }
> );
> await client.runs.cancel(thread["thread_id"], run["run_id"], wait=true);
>
> const runAfter = await client.runs.get(thread["thread_id"], run["run_id"]);
> console.log(runAfter["status"]);   // "interrupted"
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Create a run (use the run_id and thread_id from the response)
> curl --request POST \
>   --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs \
>   --header 'Content-Type: application/json' \
>   --data '{"assistant_id": "agent", "input": {"messages": [{"role": "user", "content": "Summarize the docs"}]}}'
>
> # Cancel with default action (interrupt)
> curl --request POST \
>   --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/<RUN_ID>/cancel?wait=true
>
> # Get the run to see status "interrupted" and that the run still exists
> curl --request GET \
>   --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/<RUN_ID>
> ```

### Cancel with rollback

**rollback** stops the run and then removes it and its checkpoints from storage:

* The run record is deleted. The run no longer appears in run lists or history for that thread.
* All checkpoints created by that run are deleted. The thread’s state is reverted to what it was before the run started (as if the run had never been executed).
* You cannot resume or inspect the run after a rollback.

Use **rollback** when you want to fully discard a run and its effects (for example, after a user abandons a request and you do not need to keep partial work).

> [tab] Python
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> run = await client.runs.create(
>     thread["thread_id"],
>     assistant_id,
>     input={"messages": [{"role": "user", "content": "Long task"}]},
> )
> await client.runs.cancel(thread["thread_id"], run["run_id"], action="rollback", wait=True)
>
> # Throws an error because the run is deleted
> try:
>     await client.runs.get(thread["thread_id"], run["run_id"])
> except Exception:
>     print("Run was correctly deleted")
> ```

> [tab] Javascript
>
> ```js theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> const run = await client.runs.create(
>     thread["thread_id"],
>     assistantID,
>     { input: { messages: [{ role: "user", content: "Long task" }] } }
> );
> await client.runs.cancel(thread["thread_id"], run["run_id"], wait=true, action="rollback");
>
> // Throws an error because the run is deleted
> try {
>     await client.runs.get(thread["thread_id"], run["run_id"]);
> } catch (e) {
>     console.log("Run was correctly deleted");
> }
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Create a run, then cancel with rollback
> curl --request POST \
>   --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs \
>   --header 'Content-Type: application/json' \
>   --data '{"assistant_id": "agent", "input": {"messages": [{"role": "user", "content": "Summarize the docs"}]}}'
>
> curl --request POST \
>   --url "<DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/<RUN_ID>/cancel?action=rollback"
>
> # Throws an error because the run is deleted
> curl --request GET \
>   --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/<RUN_ID>
> ```

### Cancel with wait

By default, the cancel request returns after the cancellation is requested and the run is cancelled asynchronously. `wait=True` makes the cancel request block until the run has been fully cancelled. This is useful when you want to know the final state of the run after it has been cancelled (e.g., what checkpoints were created, what the final output was).

> [tab] Python
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> run = await client.runs.create(
>     thread["thread_id"],
>     assistant_id,
>     input={"messages": [{"role": "user", "content": "Long task"}]},
> )
> # Cancel the run asynchronously
> await client.runs.cancel(thread["thread_id"], run["run_id"])
> # Get the status of the run
> run_after = await client.runs.get(thread["thread_id"], run["run_id"])
> print(run_after["status"])  # "pending" or "running"
>
> # Wait for the run to be properly cancelled
> await client.runs.join(thread["thread_id"], run["run_id"])
> run_after = await client.runs.get(thread["thread_id"], run["run_id"])
> print(run_after["status"])  # "interrupted"
> ```

> [tab] Javascript
>
> ```js theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> const run = await client.runs.create(
>     thread["thread_id"],
>     assistantID,
>     { input: { messages: [{ role: "user", content: "Long task" }] } }
> );
> // Cancel the run asynchronously
> await client.runs.cancel(thread["thread_id"], run["run_id"]);
> // Get the status of the run
> const runRunning = await client.runs.get(thread["thread_id"], run["run_id"])
> console.log(runRunning["status"])  // "pending" or "running"
>
> // Wait for the run to be properly cancelled
> await client.runs.join(thread["thread_id"], run["run_id"])
> const runInterrupted = await client.runs.get(thread["thread_id"], run["run_id"])
> console.log(runInterrupted["status"])  // "interrupted"
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Create a run
> curl --request POST \
>   --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs \
>   --header 'Content-Type: application/json' \
>   --data '{"assistant_id": "agent", "input": {"messages": [{"role": "user", "content": "Summarize the docs"}]}}'
>
> # Cancel the run asynchronously
> curl --request POST \
>   --url "<DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/<RUN_ID>/cancel"
>
> # Get the status of the run, should be "pending" or "running" until cancellation completes, then "interrupted"
> curl --request GET \
>   --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/<RUN_ID>
> ```

## Cancel multiple runs

Use the bulk cancel endpoint to cancel multiple runs in one request. Both the interrupt and rollback actions are supported.

### Cancel by thread ID and run IDs

Cancel specific runs by passing their IDs.

> [tab] Python
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> run1 = await client.runs.create(
>     thread["thread_id"],
>     assistant_id,
>     input={"messages": [{"role": "user", "content": "First request"}]},
> )
> run2 = await client.runs.create(
>     thread["thread_id"],
>     assistant_id,
>     input={"messages": [{"role": "user", "content": "Second request"}]},
>     multitask_strategy="enqueue",
> )
>
> await client.runs.cancel_many(
>     thread_id=thread["thread_id"],
>     run_ids=[run1["run_id"], run2["run_id"]]
> )
>
> # Wait for the runs to be cancelled
> await client.runs.join(thread["thread_id"], run2["run_id"])
> runs_after = await client.runs.list(thread["thread_id"])
> for run in runs_after:
>     if run["run_id"] in (run1["run_id"], run2["run_id"]):
>         print(run["run_id"], run["status"])  # "interrupted"
> ```

> [tab] Javascript
>
> ```js theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // Bulk delete by run IDs is not supported in the Javascript SDK
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Create two runs (capture run_id from each response)
> curl --request POST \
>   --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs \
>   --header 'Content-Type: application/json' \
>   --data '{"assistant_id": "agent", "input": {"messages": [{"role": "user", "content": "First request"}]}}'
>
> curl --request POST \
>   --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs \
>   --header 'Content-Type: application/json' \
>   --data '{"assistant_id": "agent", "input": {"messages": [{"role": "user", "content": "Second request"}]}}'
>
> # Cancel both by run IDs
> curl --request POST \
>   --url "<DEPLOYMENT_URL>/runs/cancel?action=interrupt" \
>   --header 'Content-Type: application/json' \
>   --data '{"thread_id": "<THREAD_ID>", "run_ids": ["<RUN_ID_1>", "<RUN_ID_2>"]}'
>
> # List runs to confirm
> curl --request GET \
>   --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs
> ```

### Cancel by status

Cancel all runs that match a status across all threads in a deployment. Valid status options are `pending`, `running`, or `all`.

> [tab] Python
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> run1 = await client.runs.create(
>     thread["thread_id"],
>     assistant_id,
>     input={"messages": [{"role": "user", "content": "First request"}]},
> )
> thread2 = await client.threads.create()
> run2 = await client.runs.create(
>     thread2["thread_id"],
>     assistant_id,
>     input={"messages": [{"role": "user", "content": "Second request"}]},
> )
>
> await client.runs.cancel_many(
>     status="running",
> )
>
> # Wait for the runs to be cancelled
> await client.runs.join(thread2["thread_id"], run2["run_id"])
> run_after = await client.runs.get(thread["thread_id"], run1["run_id"])
> print(run_after["status"])  # running run is now "interrupted"
> run_after2 = await client.runs.get(thread2["thread_id"], run2["run_id"])
> print(run_after2["status"])  # runs are cancelled across all threads
> ```

> [tab] Javascript
>
> ```js theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // Bulk delete by status is not supported in the Javascript SDK
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Create a run
> curl --request POST \
>   --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs \
>   --header 'Content-Type: application/json' \
>   --data '{"assistant_id": "agent", "input": {"messages": [{"role": "user", "content": "First request"}]}}'
>
> # Create a second thread
> curl --request POST \
>   --url <DEPLOYMENT_URL>/threads \
>   --header 'Content-Type: application/json' \
>   --data '{}'
>
> # Create a run in the second thread
> curl --request POST \
>   --url <DEPLOYMENT_URL>/threads/<THREAD_ID_2>/runs \
>   --header 'Content-Type: application/json' \
>   --data '{"assistant_id": "agent", "input": {"messages": [{"role": "user", "content": "Second request"}]}}'
>
> # Cancel all running runs
> curl --request POST \
>   --url "<DEPLOYMENT_URL>/runs/cancel?action=interrupt" \
>   --header 'Content-Type: application/json' \
>   --data '{"status": "running"}'
>
> # Get the status of the runs to confirm
> curl --request GET \
>   --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/<RUN_ID_1>
> curl --request GET \
>   --url <DEPLOYMENT_URL>/threads/<THREAD_ID_2>/runs/<RUN_ID_2>
> ```

## Cancel on disconnect

When starting a run with streaming or when waiting on a run, you can set `on_disconnect="cancel"` so that the run is cancelled if the client disconnects. This avoids leaving runs in progress when a user closes the app or loses connection.

> [tab] Python
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # With runs.wait: run is cancelled if the client disconnects
> result = await client.runs.wait(
>     thread["thread_id"],
>     assistant_id,
>     input={"messages": [{"role": "user", "content": "Long task"}]},
>     on_disconnect="cancel",
> )
>
> # With runs.stream: run is cancelled if the client disconnects
> async for chunk in client.runs.stream(
>     thread["thread_id"],
>     assistant_id,
>     input={"messages": [{"role": "user", "content": "Long task"}]},
>     on_disconnect="cancel",
> ):
>     print(chunk)
>
> # With runs.join: wait for an existing run; cancel if client disconnects
> run = await client.runs.create(
>     thread["thread_id"],
>     assistant_id,
>     input={"messages": [{"role": "user", "content": "Long task"}]},
> )
> await client.runs.join(
>     thread["thread_id"],
>     run["run_id"],
>     on_disconnect="cancel",
> )
>
> # With runs.join_stream: join an existing run and stream; cancel if client disconnects
> async for chunk in client.runs.join_stream(
>     thread["thread_id"],
>     run["run_id"],
>     on_disconnect="cancel",
> ):
>     print(chunk)
> ```

> [tab] Javascript
>
> ```js theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // With runs.wait: run is cancelled if the client disconnects
> const result = await client.runs.wait(
>     thread["thread_id"],
>     assistantID,
>     { input: { messages: [{ role: "user", content: "Long task" }] }, onDisconnect: "cancel" }
> );
>
> // With runs.stream: run is cancelled if the client disconnects
> const streamResponse = client.runs.stream(
>     thread["thread_id"],
>     assistantID,
>     { input: { messages: [{ role: "user", content: "Long task" }] }, onDisconnect: "cancel" }
> );
> for await (const chunk of streamResponse) {
>     console.log(chunk);
> }
>
> // With runs.join does not support cancel on disconnect in the Javascript SDK
>
> // With runs.joinStream: join an existing run and stream; cancel if client disconnects
> const joinStreamResponse = client.runs.joinStream(
>     thread["thread_id"],
>     run["run_id"],
>     { cancelOnDisconnect: true }
> );
> for await (const chunk of joinStreamResponse) {
>     console.log(chunk);
> }
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # runs.wait: create run and wait for output; cancel if client disconnects
> curl --request POST \
>   --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/wait \
>   --header 'Content-Type: application/json' \
>   --data '{"assistant_id": "agent", "input": {"messages": [{"role": "user", "content": "Long task"}]}, "on_disconnect": "cancel"}'
>
> # Create and stream a run; cancel if client disconnects
> curl --request POST \
>   --url "<DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/stream?on_disconnect=cancel" \
>   --header 'Content-Type: application/json' \
>   --data '{"assistant_id": "agent", "input": {"messages": [{"role": "user", "content": "Long task"}]}}'
>
> # runs.join: wait on an existing run; cancel if client disconnects
> curl --request GET \
>   --url "<DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/<RUN_ID>/join?cancel_on_disconnect=cancel"
>
> # runs.join_stream: join an existing run and stream; cancel if client disconnects
> curl --request GET \
>   --url "<DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/<RUN_ID>/stream?cancel_on_disconnect=cancel"
> ```

## Common scenarios

* **Human-in-the-loop and interrupts**: Agents can pause at [interrupts](../Human-in-the-loop%20using%20server%20API.md) for human input. Cancelling a run stops execution; it is different from an interrupt, where the run is paused and can be resumed with new input.
* **Time travel**: After cancelling with action `interrupt`, the run and checkpoints are still available. You can [resume from a checkpoint](../Time%20travel%20using%20the%20server%20API.md) (time travel) to replay or branch execution.
* **Double-texting**: When a user sends new input while a run is in progress, the [multitask strategy](../Double-texting/Double%20texting.md) (enqueue, reject, interrupt, rollback) determines whether the existing run is interrupted or rolled back and how the new run is handled. To cancel runs explicitly from your application, use the cancel API described on this page.
* **Studio**: In [Studio](../../../../Test/Test%20from%20Studio/How%20to%20use%20Studio.md), use the **Cancel** button in the run UI to cancel the current run.
