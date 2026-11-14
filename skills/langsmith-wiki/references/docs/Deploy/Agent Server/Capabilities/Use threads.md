# Use threads

This guide shows you how to create, view, and inspect *threads*. Threads work with [assistants](Assistants/Assistants.md) to enable [stateful](https://docs.langchain.com/oss/python/langgraph/persistence.md) execution of your [deployed graphs](../../Get%20started/LangSmith%20Agent%20Server.md).

## Understand threads

A thread is a persistent conversation container that maintains state across multiple runs. Each time you execute a run on a thread, the graph processes the input with the thread's current state and updates that state with new information.

Threads enable stateful interactions by preserving conversation history and context between runs. Without threads, each run would be stateless, with no memory of previous interactions. Threads are particularly useful for:

* Multi-turn conversations where the assistant needs to remember what was discussed.
* Long-running tasks that require maintaining context across multiple steps.
* User-specific state management where each user has their own conversation history.

The diagram illustrates how a thread maintains state across two runs. The second run has access to the messages from the first run, allowing the assistant to understand that the context of "What about tomorrow?" refers to the weather query from the first run:

```mermaid actions={false}
sequenceDiagram
    participant User
    participant Thread
    participant Assistant
    participant Graph

    Note over Thread: Thread ID: abc-123<br/>Persistent conversation

    User->>Thread: Run 1: "What's the weather?"
    Thread->>Assistant: Use Assistant Config
    Assistant->>Graph: Execute with context
    Graph-->>Thread: Update State<br/>{messages: [user_msg, ai_response]}
    Thread-->>User: Response

    Note over Thread: State persisted ✓

    User->>Thread: Run 2: "What about tomorrow?"
    Note over Thread: Previous messages<br/>still in state
    Thread->>Assistant: Use Assistant Config
    Assistant->>Graph: Execute with full history
    Graph-->>Thread: Update State<br/>{messages: [...prev, new_msgs]}
    Thread-->>User: Response with context
```

* A thread maintains a persistent conversation with a unique thread ID.
* Each run applies the assistant's configuration to the graph execution.
* State is updated after each run and persists for subsequent runs.
* Later runs have access to the full conversation history.

> [!NOTE]
>
> * **[Assistants](Assistants/Assistants.md)** define the configuration (model, prompts, tools) for how your graph executes. When creating a run, you can specify either a **graph ID** (e.g., `"agent"`) to use the default assistant, or an **assistant ID** (UUID) to use a specific configuration.
> * **Threads** maintain the state and conversation history.
> * **Runs** combine an assistant and thread to execute your graph with a specific configuration and state.

> [!TIP]
>
> Best practice: When tracing runs in a thread (conversation), ensure that `thread_id` is set on all runs—both parent and child runs. This is required for thread filtering, token counting, and thread-level evaluations to work correctly.

## Create a thread

To run your graph with state persistence, you must first create a thread:

> [tab] SDK
>
> ### Empty thread
>
> To create a new thread, use one of:
>
> ```python Python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph_sdk import get_client
>
> # Initialize the client with your deployment URL
> client = get_client(url=<DEPLOYMENT_URL>)
>
> # Create an empty thread
> # This creates a new thread with no initial state
> thread = await client.threads.create()
>
> print(thread)
> ```
>
> ```javascript JavaScript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { Client } from "@langchain/langgraph-sdk";
>
> // Initialize the client with your deployment URL
> const client = new Client({ apiUrl: <DEPLOYMENT_URL> });
>
> // Create an empty thread
> // This creates a new thread with no initial state
> const thread = await client.threads.create();
>
> console.log(thread);
> ```
>
> ```bash cURL theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
>     --url <DEPLOYMENT_URL>/threads \
>     --header 'Content-Type: application/json' \
>     --data '{}'
> ```
>
> For more information, refer to the [Python](https://reference.langchain.com/python/langgraph-sdk/_async/threads/ThreadsClient/create) and [JS](https://reference.langchain.com/python/langgraph-sdk/_async/threads/ThreadsClient/create) SDK docs, or the [REST API](../../Get%20started/Reference/Agent%20Server%20API/Threads/Create%20Thread.md) reference.
>
> Output:
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "thread_id": "123e4567-e89b-12d3-a456-426614174000",
>   "created_at": "2025-05-12T14:04:08.268Z",
>   "updated_at": "2025-05-12T14:04:08.268Z",
>   "metadata": {},
>   "status": "idle",
>   "values": {}
> }
> ```
>
> ### Copy thread
>
> Alternatively, if you already have a thread in your application whose state you wish to copy, you can use the `copy` method. This will create an independent thread whose history is identical to the original thread at the time of the operation:
>
> ```python Python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Copy an existing thread
> # The new thread will have the same state as the original at the time of copying
> copied_thread = await client.threads.copy(thread["thread_id"])
> ```
>
> ```javascript JavaScript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // Copy an existing thread
> // The new thread will have the same state as the original at the time of copying
> const copiedThread = await client.threads.copy(thread["thread_id"]);
> ```
>
> ```bash cURL theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST --url <DEPLOYMENT_URL>/threads/thread["thread_id"]/copy \
> --header 'Content-Type: application/json'
> ```
>
> For more information, refer to the [Python](https://reference.langchain.com/python/langgraph-sdk/_async/threads/ThreadsClient/copy) and [JS](https://reference.langchain.com/python/langgraph-sdk/_async/threads/ThreadsClient/copy) SDK docs, or the [REST API](../../Get%20started/Reference/Agent%20Server%20API/Threads/Copy%20Thread.md) reference.
>
> ### Prepopulated state
>
> You can create a thread with an arbitrary pre-defined state by providing a list of `supersteps` into the `create` method. The `supersteps` describe a sequence of state updates that establish the initial state of the thread. This is useful when you want to:
>
> * Create a thread with existing conversation history.
> * Migrate conversations from another system.
> * Set up test scenarios with specific initial states.
> * Resume conversations from a previous session.
>
> For more information on checkpoints and state management, refer to the [LangGraph persistence documentation](https://docs.langchain.com/oss/python/langgraph/persistence.md).
>
> ```python Python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph_sdk import get_client
>
> # Initialize the client
> client = get_client(url=<DEPLOYMENT_URL>)
>
> # Create a thread with pre-populated conversation history
> # The supersteps define a sequence of state updates that build up the initial state
> thread = await client.threads.create(
>   graph_id="agent",  # Specify which graph this thread is for
>   supersteps=[
>     {
>       updates: [
>         {
>           values: {},
>           as_node: '__input__',  # Initial input node
>         },
>       ],
>     },
>     {
>       updates: [
>         {
>           values: {
>             messages: [
>               {
>                 type: 'human',
>                 content: 'hello',
>               },
>             ],
>           },
>           as_node: '__start__',  # User's first message
>         },
>       ],
>     },
>     {
>       updates: [
>         {
>           values: {
>             messages: [
>               {
>                 content: 'Hello! How can I assist you today?',
>                 type: 'ai',
>               },
>             ],
>           },
>           as_node: 'call_model',  # Assistant's response
>         },
>       ],
>     },
>   ])
>
> print(thread)
> ```
>
> ```javascript JavaScript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { Client } from "@langchain/langgraph-sdk";
>
> // Initialize the client
> const client = new Client({ apiUrl: <DEPLOYMENT_URL> });
>
> // Create a thread with pre-populated conversation history
> // The supersteps define a sequence of state updates that build up the initial state
> const thread = await client.threads.create({
>     graphId: 'agent',  // Specify which graph this thread is for
>     supersteps: [
>     {
>       updates: [
>         {
>           values: {},
>           asNode: '__input__',  // Initial input node
>         },
>       ],
>     },
>     {
>       updates: [
>         {
>           values: {
>             messages: [
>               {
>                 type: 'human',
>                 content: 'hello',
>               },
>             ],
>           },
>           asNode: '__start__',  // User's first message
>         },
>       ],
>     },
>     {
>       updates: [
>         {
>           values: {
>             messages: [
>               {
>                 content: 'Hello! How can I assist you today?',
>                 type: 'ai',
>               },
>             ],
>           },
>           asNode: 'call_model',  // Assistant's response
>         },
>       ],
>     },
>   ],
> });
>
> console.log(thread);
> ```
>
> ```bash cURL theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
>     --url <DEPLOYMENT_URL>/threads \
>     --header 'Content-Type: application/json' \
>     --data '{"metadata":{"graph_id":"agent"},"supersteps":[{"updates":[{"values":{},"as_node":"__input__"}]},{"updates":[{"values":{"messages":[{"type":"human","content":"hello"}]},"as_node":"__start__"}]},{"updates":[{"values":{"messages":[{"content":"Hello\u0021 How can I assist you today?","type":"ai"}]},"as_node":"call_model"}]}]}'
> ```
>
> Output:
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "thread_id": "f15d70a1-27d4-4793-a897-de5609920b7d",
>   "created_at": "2025-05-12T15:37:08.935038+00:00",
>   "updated_at": "2025-05-12T15:37:08.935046+00:00",
>   "metadata": {
>     "graph_id": "agent"
>   },
>   "status": "idle",
>   "config": {},
>   "values": {
>     "messages": [
>       {
>         "content": "hello",
>         "additional_kwargs": {},
>         "response_metadata": {},
>         "type": "human",
>         "name": null,
>         "id": "8701f3be-959c-4b7c-852f-c2160699b4ab",
>         "example": false
>       },
>       {
>         "content": "Hello! How can I assist you today?",
>         "additional_kwargs": {},
>         "response_metadata": {},
>         "type": "ai",
>         "name": null,
>         "id": "4d8ea561-7ca1-409a-99f7-6b67af3e1aa3",
>         "example": false,
>         "tool_calls": [],
>         "invalid_tool_calls": [],
>         "usage_metadata": null
>       }
>     ]
>   }
> }
> ```

> [tab] UI
>
> You can also create threads directly from the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-use-threads):
>
> 1. Navigate to your [deployment](../../Get%20started/LangSmith%20Agent%20Server.md).
> 2. Select the **Threads** tab.
> 3. Click **+ New thread**.
> 4. Optionally provide metadata or initial state for the thread.
> 5. Click **Create thread**.
>
> The newly created thread will appear in the threads table and can be used for runs immediately.

## List threads

> [tab] SDK
>
> To list threads, use the `search` method. This will list the threads in the application that match the provided filters:
>
> ### Filter by thread status
>
> Use the `status` field to filter threads based on their status. Supported values are `idle`, `busy`, `interrupted`, and `error`. For example, to view `idle` threads:
>
> ```python Python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Search for idle threads
> # The status filter accepts: idle, busy, interrupted, error
> print(await client.threads.search(status="idle", limit=1))
> ```
>
> ```javascript JavaScript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // Search for idle threads
> // The status filter accepts: idle, busy, interrupted, error
> console.log(await client.threads.search({ status: "idle", limit: 1 }));
> ```
>
> ```bash cURL theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
> --url <DEPLOYMENT_URL>/threads/search \
> --header 'Content-Type: application/json' \
> --data '{"status": "idle", "limit": 1}'
> ```
>
> For more information, refer to the [Python](https://reference.langchain.com/python/langgraph-sdk/_async/threads/ThreadsClient/search) and [JS](https://reference.langchain.com/python/langgraph-sdk/_async/threads/ThreadsClient/search) SDK docs, or the [REST API](../../Get%20started/Reference/Agent%20Server%20API/Threads/Search%20Threads.md) reference.
>
> Output:
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> [
>   {
>     "thread_id": "cacf79bb-4248-4d01-aabc-938dbd60ed2c",
>     "created_at": "2024-08-14T17:36:38.921660+00:00",
>     "updated_at": "2024-08-14T17:36:38.921660+00:00",
>     "metadata": {
>       "graph_id": "agent"
>     },
>     "status": "idle",
>     "config": {
>       "configurable": {}
>     }
>   }
> ]
> ```
>
> ### Filter by metadata
>
> The `search` method allows you to filter on metadata. This is useful for finding threads associated with specific graphs, users, or custom metadata you've added to threads.
>
> Common metadata fields you can filter on include:
>
> | Metadata key | Description |
> | - | - |
> | `graph_id` | The graph (deployment) the thread belongs to. |
> | `assistant_id` | The [assistant](Assistants/Assistants.md) used to create runs on the thread. |
> | `langgraph_auth_user_id` | The authenticated user who owns the thread (set automatically when using [custom auth](../Auth%20%26%20access%20control/Add%20custom%20authentication.md)). |
> | `cron_id` | The [cron job](Use%20cron%20jobs.md) that created runs on the thread. |
>
> You can also filter on any custom metadata you attach when creating or updating threads.
>
> #### Filter by graph
>
> ```python Python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> print(await client.threads.search(metadata={"graph_id": "agent"}, limit=1))
> ```
>
> ```javascript JavaScript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> console.log(await client.threads.search({ metadata: { "graph_id": "agent" }, limit: 1 }));
> ```
>
> ```bash cURL theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
> --url <DEPLOYMENT_URL>/threads/search \
> --header 'Content-Type: application/json' \
> --data '{"metadata": {"graph_id": "agent"}, "limit": 1}'
> ```
>
> Output:
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> [
>   {
>     "thread_id": "cacf79bb-4248-4d01-aabc-938dbd60ed2c",
>     "created_at": "2024-08-14T17:36:38.921660+00:00",
>     "updated_at": "2024-08-14T17:36:38.921660+00:00",
>     "metadata": {
>       "graph_id": "agent"
>     },
>     "status": "idle",
>     "config": {
>       "configurable": {}
>     }
>   }
> ]
> ```
>
> #### Filter by assistant
>
> ```python Python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> print(await client.threads.search(
>     metadata={"assistant_id": "fe096781-5601-53d2-b2f6-0d3403f7e9ca"},
>     limit=1,
> ))
> ```
>
> ```javascript JavaScript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> console.log(await client.threads.search({
>   metadata: { "assistant_id": "fe096781-5601-53d2-b2f6-0d3403f7e9ca" },
>   limit: 1,
> }));
> ```
>
> ```bash cURL theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
> --url <DEPLOYMENT_URL>/threads/search \
> --header 'Content-Type: application/json' \
> --data '{"metadata": {"assistant_id": "fe096781-5601-53d2-b2f6-0d3403f7e9ca"}, "limit": 1}'
> ```
>
> #### Filter by cron job
>
> ```python Python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> print(await client.threads.search(
>     metadata={"cron_id": "8b98a268-e49a-4228-a0d3-1a354e3a54d0"},
>     limit=10,
> ))
> ```
>
> ```javascript JavaScript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> console.log(await client.threads.search({
>   metadata: { "cron_id": "8b98a268-e49a-4228-a0d3-1a354e3a54d0" },
>   limit: 10,
> }));
> ```
>
> ```bash cURL theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
> --url <DEPLOYMENT_URL>/threads/search \
> --header 'Content-Type: application/json' \
> --data '{"metadata": {"cron_id": "8b98a268-e49a-4228-a0d3-1a354e3a54d0"}, "limit": 10}'
> ```
>
> ### Sorting
>
> The SDK also supports sorting threads by `thread_id`, `status`, `created_at`, and `updated_at` using the `sort_by` and `sort_order` parameters.

> [tab] UI
>
> You can also view and manage threads in a deployment via the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-use-threads):
>
> 1. Navigate to your [deployment](../../Get%20started/LangSmith%20Agent%20Server.md).
> 2. Select the **Threads** tab.
>
> This will load a table of all threads in your deployment.
>
> **Filter by thread status:** Select a status in the top bar to filter threads by `idle`, `busy`, `interrupted`, or `error`.
>
> **Sort threads:** Click on the arrow icon for any column header to sort by that property (`thread_id`, `status`, `created_at`, or `updated_at`).

## Inspect threads

> [tab] SDK
>
> ### Get thread
>
> To view a specific thread given its `thread_id`, use the [`get`](https://reference.langchain.com/python/langgraph-sdk/_async/threads/ThreadsClient#member-get-0) method:
>
> ```python Python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Retrieve a specific thread by its ID
> # Returns the thread metadata including status, creation time, and metadata
> print((await client.threads.get(thread["thread_id"])))
> ```
>
> ```javascript JavaScript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // Retrieve a specific thread by its ID
> // Returns the thread metadata including status, creation time, and metadata
> console.log((await client.threads.get(thread["thread_id"])));
> ```
>
> ```bash cURL theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request GET \
> --url <DEPLOYMENT_URL>/threads/thread["thread_id"] \
> --header 'Content-Type: application/json'
> ```
>
> Output:
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "thread_id": "cacf79bb-4248-4d01-aabc-938dbd60ed2c",
>   "created_at": "2024-08-14T17:36:38.921660+00:00",
>   "updated_at": "2024-08-14T17:36:38.921660+00:00",
>   "metadata": {
>     "graph_id": "agent"
>   },
>   "status": "idle",
>   "config": {
>     "configurable": {}
>   }
> }
> ```
>
> For more information, refer to the [Python](https://reference.langchain.com/python/langgraph-sdk/_async/threads/ThreadsClient#member-get-0) and [JS](https://reference.langchain.com/python/langgraph-sdk/_async/threads/ThreadsClient#member-get-0) SDK docs, or the [REST API](../../Get%20started/Reference/Agent%20Server%20API/Threads/Get%20Thread.md) reference.
>
> ### Inspect thread state
>
> To view the current state of a given thread, use the [`get_state`](https://reference.langchain.com/python/langgraph-sdk/_async/threads/ThreadsClient/get_state) method. This returns the current values, next nodes to execute, and checkpoint information:
>
> ```python Python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Get the current state of a thread
> # Returns values, next nodes, tasks, checkpoint info, and metadata
> print((await client.threads.get_state(thread["thread_id"])))
> ```
>
> ```javascript JavaScript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // Get the current state of a thread
> // Returns values, next nodes, tasks, checkpoint info, and metadata
> console.log((await client.threads.getState(thread["thread_id"])));
> ```
>
> ```bash cURL theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request GET \
> --url <DEPLOYMENT_URL>/threads/thread["thread_id"]/state \
> --header 'Content-Type: application/json'
> ```
>
> Output:
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "values": {
>     "messages": [
>       {
>         "content": "hello",
>         "additional_kwargs": {},
>         "response_metadata": {},
>         "type": "human",
>         "name": null,
>         "id": "8701f3be-959c-4b7c-852f-c2160699b4ab",
>         "example": false
>       },
>       {
>         "content": "Hello! How can I assist you today?",
>         "additional_kwargs": {},
>         "response_metadata": {},
>         "type": "ai",
>         "name": null,
>         "id": "4d8ea561-7ca1-409a-99f7-6b67af3e1aa3",
>         "example": false,
>         "tool_calls": [],
>         "invalid_tool_calls": [],
>         "usage_metadata": null
>       }
>     ]
>   },
>   "next": [],
>   "tasks": [],
>   "metadata": {
>     "thread_id": "f15d70a1-27d4-4793-a897-de5609920b7d",
>     "checkpoint_id": "1f02f46f-7308-616c-8000-1b158a9a6955",
>     "graph_id": "agent_with_quite_a_long_name",
>     "source": "update",
>     "step": 1,
>     "writes": {
>       "call_model": {
>         "messages": [
>           {
>             "content": "Hello! How can I assist you today?",
>             "type": "ai"
>           }
>         ]
>       }
>     },
>     "parents": {}
>   },
>   "created_at": "2025-05-12T15:37:09.008055+00:00",
>   "checkpoint": {
>     "checkpoint_id": "1f02f46f-733f-6b58-8001-ea90dcabb1bd",
>     "thread_id": "f15d70a1-27d4-4793-a897-de5609920b7d",
>     "checkpoint_ns": ""
>   },
>   "parent_checkpoint": {
>     "checkpoint_id": "1f02f46f-7308-616c-8000-1b158a9a6955",
>     "thread_id": "f15d70a1-27d4-4793-a897-de5609920b7d",
>     "checkpoint_ns": ""
>   },
>   "checkpoint_id": "1f02f46f-733f-6b58-8001-ea90dcabb1bd",
>   "parent_checkpoint_id": "1f02f46f-7308-616c-8000-1b158a9a6955"
> }
> ```
>
> For more information, refer to the [Python](https://reference.langchain.com/python/langgraph-sdk/_async/threads/ThreadsClient/get_state) and [JS](https://reference.langchain.com/python/langgraph-sdk/_async/threads/ThreadsClient/get_state) SDK docs, or the [REST API](../../Get%20started/Reference/Agent%20Server%20API/Threads/Get%20Thread%20State.md) reference.
>
> Optionally, to view the state of a thread at a given checkpoint, pass in the checkpoint ID. This is useful for inspecting the thread state at a specific point in its execution history.
>
> First, get the checkpoint ID from the thread's history:
>
> ```python Python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Get the thread history to find checkpoint IDs
> history = await client.threads.get_history(thread_id=thread["thread_id"])
> checkpoint_id = history[0]["checkpoint_id"]  # Get the most recent checkpoint
> ```
>
> ```javascript JavaScript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // Get the thread history to find checkpoint IDs
> const history = await client.threads.getHistory(thread["thread_id"]);
> const checkpointId = history[0].checkpoint_id;  // Get the most recent checkpoint
> ```
>
> ```bash cURL theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Get the thread history to find checkpoint IDs
> curl --request POST \
> --url <DEPLOYMENT_URL>/threads/thread["thread_id"]/history \
> --header 'Content-Type: application/json' \
> --data '{"limit": 1}'
> ```
>
> Then use the checkpoint ID to get the state at that specific point:
>
> ```python Python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Get thread state at a specific checkpoint
> # Useful for inspecting historical state or debugging
> thread_state = await client.threads.get_state(
>   thread_id=thread["thread_id"],
>   checkpoint_id=checkpoint_id
> )
> ```
>
> ```javascript JavaScript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // Get thread state at a specific checkpoint
> // Useful for inspecting historical state or debugging
> const threadState = await client.threads.getState(thread["thread_id"], checkpointId);
> ```
>
> ```bash cURL theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request GET \
> --url <DEPLOYMENT_URL>/threads/thread["thread_id"]/state/<CHECKPOINT_ID> \
> --header 'Content-Type: application/json'
> ```
>
> ### Inspect full thread history
>
> To view a thread's history, use the [`get_history`](https://reference.langchain.com/python/langgraph-sdk/_async/threads/ThreadsClient/get_history) method. This returns a list of every state the thread experienced, allowing you to trace the full execution path:
>
> ```python Python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Get the full history of a thread
> # Returns a list of all state snapshots from the thread's execution
> history = await client.threads.get_history(
>   thread_id=thread["thread_id"],
>   limit=10  # Optional: limit the number of states returned
> )
>
> for state in history:
>     print(f"Checkpoint: {state['checkpoint_id']}")
>     print(f"Step: {state['metadata']['step']}")
> ```
>
> ```javascript JavaScript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // Get the full history of a thread
> // Returns a list of all state snapshots from the thread's execution
> const history = await client.threads.getHistory(
>   thread["thread_id"],
>   {
>     limit: 10  // Optional: limit the number of states returned
>   }
> );
>
> for (const state of history) {
>   console.log(`Checkpoint: ${state.checkpoint_id}`);
>   console.log(`Step: ${state.metadata.step}`);
> }
> ```
>
> ```bash cURL theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
> --url <DEPLOYMENT_URL>/threads/thread["thread_id"]/history \
> --header 'Content-Type: application/json' \
> --data '{"limit": 10}'
> ```
>
> This method is particularly useful for:
>
> * Debugging execution flow by seeing how state evolved.
> * Understanding decision points in your graph's execution.
> * Auditing conversation history and state changes.
> * Replaying or analyzing past interactions.
>
> For more information, refer to the [Python](https://reference.langchain.com/python/langgraph-sdk/_async/threads/ThreadsClient/get_history) and [JS](https://reference.langchain.com/python/langgraph-sdk/_async/threads/ThreadsClient/get_history) SDK docs, or the [REST API](../../Get%20started/Reference/Agent%20Server%20API/Threads/Get%20Thread%20History.md) reference.

> [tab] UI
>
> You can also view and inspect threads in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-use-threads):
>
> 1. Navigate to your [deployment](../../Get%20started/LangSmith%20Agent%20Server.md).
> 2. Select the **Threads** tab to view all threads.
> 3. Click on a thread to inspect its current state.
>
> To view the full thread history and perform detailed debugging, click **Open in Studio** to open the thread in [Studio](../../../Test/Test%20from%20Studio/LangSmith%20Studio.md). Studio provides a visual interface for exploring the thread's execution history, state changes, and checkpoint details.
