# Use cron jobs

There are many situations in which it is useful to run an assistant on a schedule.

For example, say that you're building an assistant that runs daily and sends an email summary
of the day's news. You could use a cron job to run the assistant every day at 8:00 PM.

LangSmith Agent Server supports cron jobs, which run on a user-defined schedule. The user specifies a schedule, an assistant, and some input. After that, on the specified schedule, the server will:

* Create a new thread with the specified assistant
* Send the specified input to that thread

Note that this sends the same input to the thread every time.

The LangSmith Agent Server API provides several endpoints for creating and managing cron jobs. See the [API reference](../../Get%20started/Reference/Agent%20Server%20API/Agent%20Server%20API%20reference.md) for more details.

Sometimes you don't want to run your graph based on user interaction, but rather you would like to schedule your graph to run on a schedule - for example if you wish for your graph to compose and send out a weekly email of to-dos for your team. LangSmith Agent Server allows you to do this without having to write your own script by using the `Crons` client. To schedule a graph job, you need to pass a [cron expression](https://crontab.cronhub.io/) to inform the client when you want to run the graph. `Cron` jobs are run in the background and do not interfere with normal invocations of the graph.

> [!NOTE]
>
> All cron schedules are interpreted in **UTC**. Make sure to convert your desired execution time to UTC when specifying the schedule.

## Setup

First, let's set up our SDK client, assistant, and thread:

> [tab] Python
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph_sdk import get_client
>
> client = get_client(url=<DEPLOYMENT_URL>)
> # Using the graph deployed with the name "agent"
> assistant_id = "agent"
> # create thread
> thread = await client.threads.create()
> print(thread)
> ```

> [tab] Javascript
>
> ```js theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { Client } from "@langchain/langgraph-sdk";
>
> const client = new Client({ apiUrl: <DEPLOYMENT_URL> });
> // Using the graph deployed with the name "agent"
> const assistantId = "agent";
> // create thread
> const thread = await client.threads.create();
> console.log(thread);
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
>     --url <DEPLOYMENT_URL>/assistants/search \
>     --header 'Content-Type: application/json' \
>     --data '{
>         "limit": 10,
>         "offset": 0
>     }' | jq -c 'map(select(.config == null or .config == {})) | .[0].graph_id' && \
> curl --request POST \
>     --url <DEPLOYMENT_URL>/threads \
>     --header 'Content-Type: application/json' \
>     --data '{}'
> ```

Output:

```
{
'thread_id': '9dde5490-2b67-47c8-aa14-4bfec88af217',
'created_at': '2024-08-30T23:07:38.242730+00:00',
'updated_at': '2024-08-30T23:07:38.242730+00:00',
'metadata': {},
'status': 'idle',
'config': {},
'values': None
}
```

## Cron job on a thread

To create a cron job associated with a specific thread, you can write:

> [tab] Python
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # This schedules a job to run at 15:27 (3:27PM) UTC every day
> cron_job = await client.crons.create_for_thread(
>     thread["thread_id"],
>     assistant_id,
>     schedule="27 15 * * *",
>     input={"messages": [{"role": "user", "content": "What time is it?"}]},
> )
> ```

> [tab] Javascript
>
> ```js theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // This schedules a job to run at 15:27 (3:27PM) UTC every day
> const cronJob = await client.crons.create_for_thread(
>   thread["thread_id"],
>   assistantId,
>   {
>     schedule: "27 15 * * *",
>     input: { messages: [{ role: "user", content: "What time is it?" }] }
>   }
> );
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
>     --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/crons \
>     --header 'Content-Type: application/json' \
>     --data '{
>         "assistant_id": <ASSISTANT_ID>,
>     }'
> ```

Note that it is **very** important to delete `Cron` jobs that are no longer useful. Otherwise you could rack up unwanted API charges to the LLM! You can delete a `Cron` job using the following code:

> [tab] Python
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> await client.crons.delete(cron_job["cron_id"])
> ```

> [tab] Javascript
>
> ```js theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> await client.crons.delete(cronJob["cron_id"]);
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request DELETE \
>     --url <DEPLOYMENT_URL>/runs/crons/<CRON_ID>
> ```

## Cron job stateless

You can also create stateless cron jobs by using the following code. Stateless cron jobs create a new thread for each execution:

> [tab] Python
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # This schedules a job to run at 15:27 (3:27PM) UTC every day
> cron_job_stateless = await client.crons.create(
>     assistant_id,
>     schedule="27 15 * * *",
>     input={"messages": [{"role": "user", "content": "What time is it?"}]},
> )
> ```

> [tab] Javascript
>
> ```js theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // This schedules a job to run at 15:27 (3:27PM) UTC every day
> const cronJobStateless = await client.crons.create(
>   assistantId,
>   {
>     schedule: "27 15 * * *",
>     input: { messages: [{ role: "user", content: "What time is it?" }] }
>   }
> );
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
>     --url <DEPLOYMENT_URL>/runs/crons \
>     --header 'Content-Type: application/json' \
>     --data '{
>         "assistant_id": <ASSISTANT_ID>,
>     }'
> ```

Again, remember to delete your job once you are done with it!

> [tab] Python
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> await client.crons.delete(cron_job_stateless["cron_id"])
> ```

> [tab] Javascript
>
> ```js theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> await client.crons.delete(cronJobStateless["cron_id"]);
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request DELETE \
>     --url <DEPLOYMENT_URL>/runs/crons/<CRON_ID>
> ```

## Thread cleanup for stateless crons

> [!NOTE]
>
> This feature requires LangGraph API version **0.5.18** or later and Python SDK **0.3.2** or later, or JavaScript SDK **1.4.0** or later.

Every time a stateless cron is triggered, a new thread is created. Control what happens to that thread after the run completes using the `on_run_completed` parameter:

* **`"delete"`** (default): Automatically deletes the thread after the run completes.
* **`"keep"`**: Preserves the thread for later retrieval. You are responsible for cleaning up these threads. See [how to add TTLs to your application](../Develop%20your%20application/Persistence/How%20to%20add%20TTLs%20to%20your%20application.md) for the recommended approach.

### Example: Keeping threads for later retrieval

> [tab] Python
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Create a stateless cron that keeps threads after execution.
> # Configure checkpointer.ttl in langgraph.json to auto-delete old threads.
> # See: https://docs.langchain.com/langsmith/configure-ttl
> cron_job = await client.crons.create(
>     assistant_id,
>     schedule="27 15 * * *",
>     input={"messages": [{"role": "user", "content": "Daily report"}]},
>     on_run_completed="keep"
> )
>
> # You can later retrieve the runs and their results
> runs = await client.runs.search(
>     metadata={"cron_id": cron_job["cron_id"]}
> )
> ```

> [tab] Javascript
>
> ```js theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // Create a stateless cron that keeps threads after execution.
> // Configure checkpointer.ttl in langgraph.json to auto-delete old threads.
> // See: https://docs.langchain.com/langsmith/configure-ttl
> const cronJob = await client.crons.create(
>   assistantId,
>   {
>     schedule: "27 15 * * *",
>     input: { messages: [{ role: "user", content: "Daily report" }] },
>     onRunCompleted: "keep"
>   }
> );
>
> // You can later retrieve the runs and their results
> const runs = await client.runs.search({
>   metadata: { cron_id: cronJob["cron_id"] }
> });
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Create a stateless cron that keeps threads after execution.
> # Configure checkpointer.ttl in langgraph.json to auto-delete old threads.
> # See: https://docs.langchain.com/langsmith/configure-ttl
> curl --request POST \
>     --url <DEPLOYMENT_URL>/runs/crons \
>     --header 'Content-Type: application/json' \
>     --data '{
>         "assistant_id": "<ASSISTANT_ID>",
>         "schedule": "27 15 * * *",
>         "input": {"messages": [{"role": "user", "content": "Daily report"}]},
>         "on_run_completed": "keep"
>     }'
> ```
