# Time travel using the server API

LangGraph provides the [**time travel**](https://docs.langchain.com/oss/python/langgraph/use-time-travel.md) functionality to resume execution from a prior checkpoint, either replaying the same state or modifying it to explore alternatives. In all cases, resuming past execution produces a new fork in the history.

To time travel using the LangSmith Agent Server API (via the LangGraph SDK):

1. **Run the graph** with initial inputs using [LangGraph SDK](../../Get%20started/Reference/Related/langgraph_sdk.md)'s [client.runs.wait](https://reference.langchain.com/python/langsmith/deployment/sdk/#langgraph_sdk.client.RunsClient.wait) or [client.runs.stream](https://reference.langchain.com/python/langsmith/deployment/sdk/#langgraph_sdk.client.RunsClient.stream) APIs.
2. **Identify a checkpoint in an existing thread**: Use [client.threads.get\_history](https://reference.langchain.com/python/langgraph-sdk/_async/threads/ThreadsClient/get_history) method to retrieve the execution history for a specific `thread_id` and locate the desired `checkpoint_id`.
   Alternatively, set a [breakpoint](https://docs.langchain.com/oss/python/langgraph/interrupts.md) before the node(s) where you want execution to pause. You can then find the most recent checkpoint recorded up to that breakpoint.
3. **(Optional) modify the graph state**: Use the [client.threads.update\_state](https://reference.langchain.com/python/langgraph-sdk/_async/threads/ThreadsClient/update_state) method to modify the graph’s state at the checkpoint and resume execution from alternative state.
4. **Resume execution from the checkpoint**: Use the [client.runs.wait](https://reference.langchain.com/python/langsmith/deployment/sdk/#langgraph_sdk.client.RunsClient.wait) or [client.runs.stream](https://reference.langchain.com/python/langsmith/deployment/sdk/#langgraph_sdk.client.RunsClient.stream) APIs with an input of `None` and the appropriate `thread_id` and `checkpoint_id`.

## Use time travel in a workflow

> [accordion] Example graph
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from typing_extensions import TypedDict, NotRequired
> from langgraph.graph import StateGraph, START, END
> from langchain.chat_models import init_chat_model
> from langgraph.checkpoint.memory import InMemorySaver
>
> class State(TypedDict):
>     topic: NotRequired[str]
>     joke: NotRequired[str]
>
> model = init_chat_model(
>     "claude-sonnet-4-6",
>     temperature=0,
> )
>
> def generate_topic(state: State):
>     """LLM call to generate a topic for the joke"""
>     msg = model.invoke("Give me a funny topic for a joke")
>     return {"topic": msg.content}
>
> def write_joke(state: State):
>     """LLM call to write a joke based on the topic"""
>     msg = model.invoke(f"Write a short joke about {state['topic']}")
>     return {"joke": msg.content}
>
> # Build workflow
> builder = StateGraph(State)
>
> # Add nodes
> builder.add_node("generate_topic", generate_topic)
> builder.add_node("write_joke", write_joke)
>
> # Add edges to connect nodes
> builder.add_edge(START, "generate_topic")
> builder.add_edge("generate_topic", "write_joke")
>
> # Compile
> graph = builder.compile()
> ```

### 1. Run the graph

> [tab] Python
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph_sdk import get_client
> client = get_client(url=<DEPLOYMENT_URL>)
>
> # Using the graph deployed with the name "agent"
> assistant_id = "agent"
>
> # create a thread
> thread = await client.threads.create()
> thread_id = thread["thread_id"]
>
> # Run the graph
> result = await client.runs.wait(
>     thread_id,
>     assistant_id,
>     input={}
> )
> ```

> [tab] JavaScript
>
> ```js theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { Client } from "@langchain/langgraph-sdk";
> const client = new Client({ apiUrl: <DEPLOYMENT_URL> });
>
> // Using the graph deployed with the name "agent"
> const assistantID = "agent";
>
> // create a thread
> const thread = await client.threads.create();
> const threadID = thread["thread_id"];
>
> // Run the graph
> const result = await client.runs.wait(
>   threadID,
>   assistantID,
>   { input: {}}
> );
> ```

> [tab] cURL
>
> Create a thread:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
> --url <DEPLOYMENT_URL>/threads \
> --header 'Content-Type: application/json' \
> --data '{}'
> ```
>
> Run the graph:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
> --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/wait \
> --header 'Content-Type: application/json' \
> --data "{
>   \"assistant_id\": \"agent\",
>   \"input\": {}
> }"
> ```

### 2. Identify a checkpoint

> [tab] Python
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # The states are returned in reverse chronological order.
> states = await client.threads.get_history(thread_id)
> selected_state = states[1]
> print(selected_state)
> ```

> [tab] JavaScript
>
> ```js theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // The states are returned in reverse chronological order.
> const states = await client.threads.getHistory(threadID);
> const selectedState = states[1];
> console.log(selectedState);
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request GET \
> --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/history \
> --header 'Content-Type: application/json'
> ```

### 3. Update the state

[`update_state`](https://reference.langchain.com/python/langgraph/graphs/#langgraph.graph.state.CompiledStateGraph.update_state) will create a new checkpoint. The new checkpoint will be associated with the same thread, but a new checkpoint ID.

> [tab] Python
>
> ```python {highlight={4}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> new_config = await client.threads.update_state(
>     thread_id,
>     {"topic": "chickens"},
>     checkpoint_id=selected_state["checkpoint_id"]
> )
> print(new_config)
> ```

> [tab] JavaScript
>
> ```js theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> const newConfig = await client.threads.updateState(
>   threadID,
>   {
>     values: { "topic": "chickens" },
>     checkpointId: selectedState["checkpoint_id"]
>   }
> );
> console.log(newConfig);
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
> --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/state \
> --header 'Content-Type: application/json' \
> --data "{
>   \"assistant_id\": \"agent\",
>   \"checkpoint_id\": <CHECKPOINT_ID>,
>   \"values\": {\"topic\": \"chickens\"}
> }"
> ```

### 4. Resume execution from the checkpoint

> [tab] Python
>
> ```python {highlight={4,5}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> await client.runs.wait(
>     thread_id,
>     assistant_id,
>     input=None,
>     checkpoint_id=new_config["checkpoint_id"]
> )
> ```

> [tab] JavaScript
>
> ```javascript {highlight={5,6}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> await client.runs.wait(
>   threadID,
>   assistantID,
>   {
>     input: null,
>     checkpointId: newConfig["checkpoint_id"]
>   }
> );
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
> --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/wait \
> --header 'Content-Type: application/json' \
> --data "{
>   \"assistant_id\": \"agent\",
>   \"checkpoint_id\": <CHECKPOINT_ID>
> }"
> ```

## Learn more

* [**LangGraph time travel guide**](https://docs.langchain.com/oss/python/langgraph/use-time-travel.md): learn more about using time travel in LangGraph.
