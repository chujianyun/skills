# Streaming API

The [LangGraph SDK](../../Get%20started/Reference/Related/langgraph_sdk.md) lets you stream outputs from the [LangSmith Agent Server API](../../Get%20started/Reference/Agent%20Server%20API/Agent%20Server%20API%20reference.md) in multiple modes, from full state snapshots after each step to token-by-token LLM output. Thread streaming also supports resumability: if a connection drops, reconnect with the last event ID to pick up where you left off.

> [!NOTE]
>
> LangGraph SDK and Agent Server are a part of [LangSmith](../../../Monitor/Overview/LangSmith%20Observability.md).

## Basic usage

Basic usage example:

> [tab] Python
>
> ```python {highlight={12}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph_sdk import get_client
> client = get_client(url=<DEPLOYMENT_URL>, api_key=<API_KEY>)
>
> # Using the graph deployed with the name "agent"
> assistant_id = "agent"
>
> # create a thread
> thread = await client.threads.create()
> thread_id = thread["thread_id"]
>
> # create a streaming run
> async for chunk in client.runs.stream(
>     thread_id,
>     assistant_id,
>     input=inputs,
>     stream_mode="updates"
> ):
>     print(chunk.data)
> ```

> [tab] JavaScript
>
> ```javascript {highlight={12}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { Client } from "@langchain/langgraph-sdk";
> const client = new Client({ apiUrl: <DEPLOYMENT_URL>, apiKey: <API_KEY> });
>
> // Using the graph deployed with the name "agent"
> const assistantID = "agent";
>
> // create a thread
> const thread = await client.threads.create();
> const threadID = thread["thread_id"];
>
> // create a streaming run
> const streamResponse = client.runs.stream(
>   threadID,
>   assistantID,
>   {
>     input,
>     streamMode: "updates"
>   }
> );
> for await (const chunk of streamResponse) {
>   console.log(chunk.data);
> }
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
> Create a streaming run:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
> --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/stream \
> --header 'Content-Type: application/json' \
> --header 'x-api-key: <API_KEY>'
> --data "{
>   \"assistant_id\": \"agent\",
>   \"input\": <inputs>,
>   \"stream_mode\": \"updates\"
> }"
> ```

> [accordion] Extended example: streaming updates
>
> This is an example graph you can run in the Agent Server.
> See [LangSmith quickstart](../../Get%20started/Deploy%20your%20app%20to%20cloud.md) for more details.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # graph.py
> from typing import TypedDict
> from langgraph.graph import StateGraph, START, END
>
> class State(TypedDict):
>     topic: str
>     joke: str
>
> def refine_topic(state: State):
>     return {"topic": state["topic"] + " and cats"}
>
> def generate_joke(state: State):
>     return {"joke": f"This is a joke about {state['topic']}"}
>
> graph = (
>     StateGraph(State)
>     .add_node(refine_topic)
>     .add_node(generate_joke)
>     .add_edge(START, "refine_topic")
>     .add_edge("refine_topic", "generate_joke")
>     .add_edge("generate_joke", END)
>     .compile()
> )
> ```
>
> Once you have a running Agent Server, you can interact with it using
> [LangGraph SDK](../../Get%20started/Reference/Related/langgraph_sdk.md)
>
> > [tab] Python
> >
> > ```python {highlight={12,16}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langgraph_sdk import get_client
> > client = get_client(url=<DEPLOYMENT_URL>)
> >
> > # Using the graph deployed with the name "agent"
> > assistant_id = "agent"
> >
> > # create a thread
> > thread = await client.threads.create()
> > thread_id = thread["thread_id"]
> >
> > # create a streaming run
> > async for chunk in client.runs.stream(  # (1)!
> >     thread_id,
> >     assistant_id,
> >     input={"topic": "ice cream"},
> >     stream_mode="updates"  # (2)!
> > ):
> >     print(chunk.data)
> > ```
> >
> > 1. The `client.runs.stream()` method returns an iterator that yields streamed outputs.
> >    2\. Set `stream_mode="updates"` to stream only the updates to the graph state after each node. Other stream modes are also available. See [supported stream modes](#supported-stream-modes) for details.
>
> > [tab] JavaScript
> >
> > ```javascript {highlight={12,17}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "@langchain/langgraph-sdk";
> > const client = new Client({ apiUrl: <DEPLOYMENT_URL> });
> >
> > // Using the graph deployed with the name "agent"
> > const assistantID = "agent";
> >
> > // create a thread
> > const thread = await client.threads.create();
> > const threadID = thread["thread_id"];
> >
> > // create a streaming run
> > const streamResponse = client.runs.stream(  // (1)!
> >   threadID,
> >   assistantID,
> >   {
> >     input: { topic: "ice cream" },
> >     streamMode: "updates"  // (2)!
> >   }
> > );
> > for await (const chunk of streamResponse) {
> >   console.log(chunk.data);
> > }
> > ```
> >
> > 1. The `client.runs.stream()` method returns an iterator that yields streamed outputs.
> > 2. Set `streamMode: "updates"` to stream only the updates to the graph state after each node. Other stream modes are also available. See [supported stream modes](#supported-stream-modes) for details.
>
> > [tab] cURL
> >
> > Create a thread:
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > curl --request POST \
> > --url <DEPLOYMENT_URL>/threads \
> > --header 'Content-Type: application/json' \
> > --data '{}'
> > ```
> >
> > Create a streaming run:
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > curl --request POST \
> > --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/stream \
> > --header 'Content-Type: application/json' \
> > --data "{
> >   \"assistant_id\": \"agent\",
> >   \"input\": {\"topic\": \"ice cream\"},
> >   \"stream_mode\": \"updates\"
> > }"
> > ```
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {'run_id': '1f02c2b3-3cef-68de-b720-eec2a4a8e920', 'attempt': 1}
> {'refine_topic': {'topic': 'ice cream and cats'}}
> {'generate_joke': {'joke': 'This is a joke about ice cream and cats'}}
> ```

### Supported stream modes

| Mode | Description | LangGraph Library Method |
| - | - | - |
| [`values`](#stream-graph-state) | Stream the full graph state after each [super-step](../Server%20customization/Rebuild%20graph%20at%20runtime.md#define-graphs). | `.stream()` / `.astream()` with [`stream_mode="values"`](https://docs.langchain.com/oss/python/langgraph/streaming#graph-state) |
| [`updates`](#stream-graph-state) | Streams the updates to the state after each step of the graph. If multiple updates are made in the same step (e.g., multiple nodes are run), those updates are streamed separately. | `.stream()` / `.astream()` with [`stream_mode="updates"`](https://docs.langchain.com/oss/python/langgraph/streaming#graph-state) |
| [`messages-tuple`](#messages) | Streams LLM tokens and metadata for the graph node where the LLM is invoked (useful for chat apps). | `.stream()` / `.astream()` with [`stream_mode="messages"`](https://docs.langchain.com/oss/python/langgraph/streaming#messages) |
| [`debug`](#debug) | Streams as much information as possible throughout the execution of the graph. | `.stream()` / `.astream()` with [`stream_mode="debug"`](https://docs.langchain.com/oss/python/langgraph/streaming#graph-state) |
| [`custom`](#stream-custom-data) | Streams custom data from inside your graph | `.stream()` / `.astream()` with [`stream_mode="custom"`](https://docs.langchain.com/oss/python/langgraph/streaming#custom-data) |
| [`events`](#stream-events) | Stream all events (including the state of the graph); mainly useful when migrating large LCEL apps. | `.astream_events()` |

### Stream multiple modes

You can pass a list as the `stream_mode` parameter to stream multiple modes at once.

The streamed outputs will be tuples of `(mode, chunk)` where `mode` is the name of the stream mode and `chunk` is the data streamed by that mode.

> [tab] Python
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> async for chunk in client.runs.stream(
>     thread_id,
>     assistant_id,
>     input=inputs,
>     stream_mode=["updates", "custom"]
> ):
>     print(chunk)
> ```

> [tab] JavaScript
>
> ```js theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> const streamResponse = client.runs.stream(
>   threadID,
>   assistantID,
>   {
>     input,
>     streamMode: ["updates", "custom"]
>   }
> );
> for await (const chunk of streamResponse) {
>   console.log(chunk);
> }
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
>  --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/stream \
>  --header 'Content-Type: application/json' \
>  --data "{
>    \"assistant_id\": \"agent\",
>    \"input\": <inputs>,
>    \"stream_mode\": [
>      \"updates\"
>      \"custom\"
>    ]
>  }"
> ```

## Stream graph state

Use the stream modes `updates` and `values` to stream the state of the graph as it executes.

* `updates` streams the **updates** to the state after each step of the graph.
* `values` streams the **full value** of the state after each step of the graph.

> [accordion] Example graph
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from typing import TypedDict
> from langgraph.graph import StateGraph, START, END
>
> class State(TypedDict):
>   topic: str
>   joke: str
>
> def refine_topic(state: State):
>     return {"topic": state["topic"] + " and cats"}
>
> def generate_joke(state: State):
>     return {"joke": f"This is a joke about {state['topic']}"}
>
> graph = (
>   StateGraph(State)
>   .add_node(refine_topic)
>   .add_node(generate_joke)
>   .add_edge(START, "refine_topic")
>   .add_edge("refine_topic", "generate_joke")
>   .add_edge("generate_joke", END)
>   .compile()
> )
> ```

> [!NOTE]
>
> **Stateful runs**
> Examples below assume that you want to **persist the outputs** of a streaming run in the [checkpointer](https://docs.langchain.com/oss/python/langgraph/persistence.md) DB and have created a thread. To create a thread:
>
> > [tab] Python
> >
> > ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langgraph_sdk import get_client
> > client = get_client(url=<DEPLOYMENT_URL>)
> >
> > # Using the graph deployed with the name "agent"
> > assistant_id = "agent"
> > # create a thread
> > thread = await client.threads.create()
> > thread_id = thread["thread_id"]
> > ```
>
> > [tab] JavaScript
> >
> > ```js theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "@langchain/langgraph-sdk";
> > const client = new Client({ apiUrl: <DEPLOYMENT_URL> });
> >
> > // Using the graph deployed with the name "agent"
> > const assistantID = "agent";
> > // create a thread
> > const thread = await client.threads.create();
> > const threadID = thread["thread_id"]
> > ```
>
> > [tab] cURL
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > curl --request POST \
> > --url <DEPLOYMENT_URL>/threads \
> > --header 'Content-Type: application/json' \
> > --data '{}'
> > ```
>
> If you don't need to persist the outputs of a run, you can pass `None` instead of `thread_id` when streaming.

### Stream mode: `updates`

Use this to stream only the **state updates** returned by the nodes after each step. The streamed outputs include the name of the node as well as the update.

> [tab] Python
>
> ```python {highlight={5}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> async for chunk in client.runs.stream(
>     thread_id,
>     assistant_id,
>     input={"topic": "ice cream"},
>     stream_mode="updates"
> ):
>     print(chunk.data)
> ```

> [tab] JavaScript
>
> ```javascript {highlight={6}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> const streamResponse = client.runs.stream(
>   threadID,
>   assistantID,
>   {
>     input: { topic: "ice cream" },
>     streamMode: "updates"
>   }
> );
> for await (const chunk of streamResponse) {
>   console.log(chunk.data);
> }
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
> --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/stream \
> --header 'Content-Type: application/json' \
> --data "{
>   \"assistant_id\": \"agent\",
>   \"input\": {\"topic\": \"ice cream\"},
>   \"stream_mode\": \"updates\"
> }"
> ```

### Stream mode: `values`

Use this to stream the **full state** of the graph after each step.

> [tab] Python
>
> ```python {highlight={5}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> async for chunk in client.runs.stream(
>     thread_id,
>     assistant_id,
>     input={"topic": "ice cream"},
>     stream_mode="values"
> ):
>     print(chunk.data)
> ```

> [tab] JavaScript
>
> ```javascript {highlight={6}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> const streamResponse = client.runs.stream(
>   threadID,
>   assistantID,
>   {
>     input: { topic: "ice cream" },
>     streamMode: "values"
>   }
> );
> for await (const chunk of streamResponse) {
>   console.log(chunk.data);
> }
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
> --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/stream \
> --header 'Content-Type: application/json' \
> --data "{
>   \"assistant_id\": \"agent\",
>   \"input\": {\"topic\": \"ice cream\"},
>   \"stream_mode\": \"values\"
> }"
> ```

## Subgraphs

To include outputs from [subgraphs](https://docs.langchain.com/oss/python/langgraph/use-subgraphs.md) in the streamed outputs, you can set `subgraphs=True` in the `.stream()` method of the parent graph. This will stream outputs from both the parent graph and any subgraphs.

```python {highlight={5}}
async for chunk in client.runs.stream(
    thread_id,
    assistant_id,
    input={"foo": "foo"},
    stream_subgraphs=True, # (1)!
    stream_mode="updates",
):
    print(chunk)
```

1. Set `stream_subgraphs=True` to stream outputs from subgraphs.

> [accordion] Extended example: streaming from subgraphs
>
> This is an example graph you can run in the Agent Server.
> See [LangSmith quickstart](../../Get%20started/Deploy%20your%20app%20to%20cloud.md) for more details.
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # graph.py
> from langgraph.graph import START, StateGraph
> from typing import TypedDict
>
> # Define subgraph
> class SubgraphState(TypedDict):
>     foo: str  # note that this key is shared with the parent graph state
>     bar: str
>
> def subgraph_node_1(state: SubgraphState):
>     return {"bar": "bar"}
>
> def subgraph_node_2(state: SubgraphState):
>     return {"foo": state["foo"] + state["bar"]}
>
> subgraph_builder = StateGraph(SubgraphState)
> subgraph_builder.add_node(subgraph_node_1)
> subgraph_builder.add_node(subgraph_node_2)
> subgraph_builder.add_edge(START, "subgraph_node_1")
> subgraph_builder.add_edge("subgraph_node_1", "subgraph_node_2")
> subgraph = subgraph_builder.compile()
>
> # Define parent graph
> class ParentState(TypedDict):
>     foo: str
>
> def node_1(state: ParentState):
>     return {"foo": "hi! " + state["foo"]}
>
> builder = StateGraph(ParentState)
> builder.add_node("node_1", node_1)
> builder.add_node("node_2", subgraph)
> builder.add_edge(START, "node_1")
> builder.add_edge("node_1", "node_2")
> graph = builder.compile()
> ```
>
> Once you have a running Agent Server, you can interact with it using
> [LangGraph SDK](../../Get%20started/Reference/Related/langgraph_sdk.md)
>
> > [tab] Python
> >
> > ```python {highlight={15}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langgraph_sdk import get_client
> > client = get_client(url=<DEPLOYMENT_URL>)
> >
> > # Using the graph deployed with the name "agent"
> > assistant_id = "agent"
> >
> > # create a thread
> > thread = await client.threads.create()
> > thread_id = thread["thread_id"]
> >
> > async for chunk in client.runs.stream(
> >     thread_id,
> >     assistant_id,
> >     input={"foo": "foo"},
> >     stream_subgraphs=True, # (1)!
> >     stream_mode="updates",
> > ):
> >     print(chunk)
> > ```
> >
> > 1. Set `stream_subgraphs=True` to stream outputs from subgraphs.
>
> > [tab] JavaScript
> >
> > ```javascript {highlight={17}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > import { Client } from "@langchain/langgraph-sdk";
> > const client = new Client({ apiUrl: <DEPLOYMENT_URL> });
> >
> > // Using the graph deployed with the name "agent"
> > const assistantID = "agent";
> >
> > // create a thread
> > const thread = await client.threads.create();
> > const threadID = thread["thread_id"];
> >
> > // create a streaming run
> > const streamResponse = client.runs.stream(
> >   threadID,
> >   assistantID,
> >   {
> >     input: { foo: "foo" },
> >     streamSubgraphs: true,  // (1)!
> >     streamMode: "updates"
> >   }
> > );
> > for await (const chunk of streamResponse) {
> >   console.log(chunk);
> > }
> > ```
> >
> > 1. Set `streamSubgraphs: true` to stream outputs from subgraphs.
>
> > [tab] cURL
> >
> > Create a thread:
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > curl --request POST \
> > --url <DEPLOYMENT_URL>/threads \
> > --header 'Content-Type: application/json' \
> > --data '{}'
> > ```
> >
> > Create a streaming run:
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > curl --request POST \
> > --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/stream \
> > --header 'Content-Type: application/json' \
> > --data "{
> >   \"assistant_id\": \"agent\",
> >   \"input\": {\"foo\": \"foo\"},
> >   \"stream_subgraphs\": true,
> >   \"stream_mode\": [
> >     \"updates\"
> >   ]
> > }"
> > ```
>
> **Note** that we are receiving not just the node updates, but we also the namespaces which tell us what graph (or subgraph) we are streaming from.

## Debugging

Use the `debug` streaming mode to stream as much information as possible throughout the execution of the graph. The streamed outputs include the name of the node as well as the full state.

> [tab] Python
>
> ```python {highlight={5}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> async for chunk in client.runs.stream(
>     thread_id,
>     assistant_id,
>     input={"topic": "ice cream"},
>     stream_mode="debug"
> ):
>     print(chunk.data)
> ```

> [tab] JavaScript
>
> ```javascript {highlight={6}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> const streamResponse = client.runs.stream(
>   threadID,
>   assistantID,
>   {
>     input: { topic: "ice cream" },
>     streamMode: "debug"
>   }
> );
> for await (const chunk of streamResponse) {
>   console.log(chunk.data);
> }
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
> --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/stream \
> --header 'Content-Type: application/json' \
> --data "{
>   \"assistant_id\": \"agent\",
>   \"input\": {\"topic\": \"ice cream\"},
>   \"stream_mode\": \"debug\"
> }"
> ```

## LLM tokens

Use the `messages-tuple` streaming mode to stream Large Language Model (LLM) outputs **token by token** from any part of your graph, including nodes, tools, subgraphs, or tasks.

The streamed output from [`messages-tuple` mode](#supported-stream-modes) is a tuple `(message_chunk, metadata)` where:

* `message_chunk`: the token or message segment from the LLM.
* `metadata`: a dictionary containing details about the graph node and LLM invocation.

> [accordion] Example graph
>
> ```python {highlight={15}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from dataclasses import dataclass
>
> from langchain.chat_models import init_chat_model
> from langgraph.graph import StateGraph, START
>
> @dataclass
> class MyState:
>     topic: str
>     joke: str = ""
>
> model = init_chat_model(model="gpt-5.4-mini")
>
> def call_model(state: MyState):
>     """Call the LLM to generate a joke about a topic"""
>     model_response = model.invoke( # (1)!
>         [
>             {"role": "user", "content": f"Generate a joke about {state.topic}"}
>         ]
>     )
>     return {"joke": model_response.content}
>
> graph = (
>     StateGraph(MyState)
>     .add_node(call_model)
>     .add_edge(START, "call_model")
>     .compile()
> )
> ```
>
> 1. Note that the message events are emitted even when the LLM is run using `invoke` rather than `stream`.

> [tab] Python
>
> ```python {highlight={5}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> async for chunk in client.runs.stream(
>     thread_id,
>     assistant_id,
>     input={"topic": "ice cream"},
>     stream_mode="messages-tuple",
> ):
>     if chunk.event != "messages":
>         continue
>
>     message_chunk, metadata = chunk.data  # (1)!
>     if message_chunk["content"]:
>         print(message_chunk["content"], end="|", flush=True)
> ```
>
> 1. The "messages-tuple" stream mode returns an iterator of tuples `(message_chunk, metadata)` where `message_chunk` is the token streamed by the LLM and `metadata` is a dictionary with information about the graph node where the LLM was called and other information.

> [tab] JavaScript
>
> ```javascript {highlight={6}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> const streamResponse = client.runs.stream(
>   threadID,
>   assistantID,
>   {
>     input: { topic: "ice cream" },
>     streamMode: "messages-tuple"
>   }
> );
> for await (const chunk of streamResponse) {
>   if (chunk.event !== "messages") {
>     continue;
>   }
>   console.log(chunk.data[0]["content"]);  // (1)!
> }
> ```
>
> 1. The "messages-tuple" stream mode returns an iterator of tuples `(message_chunk, metadata)` where `message_chunk` is the token streamed by the LLM and `metadata` is a dictionary with information about the graph node where the LLM was called and other information.

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
> --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/stream \
> --header 'Content-Type: application/json' \
> --data "{
>   \"assistant_id\": \"agent\",
>   \"input\": {\"topic\": \"ice cream\"},
>   \"stream_mode\": \"messages-tuple\"
> }"
> ```

### Filter LLM tokens

* To filter the streamed tokens by LLM invocation, you can [associate `tags` with LLM invocations](https://docs.langchain.com/oss/python/langgraph/streaming#filter-by-llm-invocation).
* To stream tokens only from specific nodes, use `stream_mode="messages"` and [filter the outputs by the `langgraph_node` field](https://docs.langchain.com/oss/python/langgraph/streaming#filter-by-node) in the streamed metadata.

## Stream custom data

To send **custom user-defined data**:

> [tab] Python
>
> ```python {highlight={5}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> async for chunk in client.runs.stream(
>     thread_id,
>     assistant_id,
>     input={"query": "example"},
>     stream_mode="custom"
> ):
>     print(chunk.data)
> ```

> [tab] JavaScript
>
> ```javascript {highlight={6}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> const streamResponse = client.runs.stream(
>   threadID,
>   assistantID,
>   {
>     input: { query: "example" },
>     streamMode: "custom"
>   }
> );
> for await (const chunk of streamResponse) {
>   console.log(chunk.data);
> }
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
> --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/stream \
> --header 'Content-Type: application/json' \
> --data "{
>   \"assistant_id\": \"agent\",
>   \"input\": {\"query\": \"example\"},
>   \"stream_mode\": \"custom\"
> }"
> ```

## Stream events

To stream all events, including the state of the graph:

> [tab] Python
>
> ```python {highlight={5}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> async for chunk in client.runs.stream(
>     thread_id,
>     assistant_id,
>     input={"topic": "ice cream"},
>     stream_mode="events"
> ):
>     print(chunk.data)
> ```

> [tab] JavaScript
>
> ```javascript {highlight={6}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> const streamResponse = client.runs.stream(
>   threadID,
>   assistantID,
>   {
>     input: { topic: "ice cream" },
>     streamMode: "events"
>   }
> );
> for await (const chunk of streamResponse) {
>   console.log(chunk.data);
> }
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
> --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/stream \
> --header 'Content-Type: application/json' \
> --data "{
>   \"assistant_id\": \"agent\",
>   \"input\": {\"topic\": \"ice cream\"},
>   \"stream_mode\": \"events\"
> }"
> ```

## Stateless runs

If you don't want to **persist the outputs** of a streaming run in the [checkpointer](https://docs.langchain.com/oss/python/langgraph/persistence.md) DB, you can create a stateless run without creating a thread:

> [tab] Python
>
> ```python {highlight={5}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph_sdk import get_client
> client = get_client(url=<DEPLOYMENT_URL>, api_key=<API_KEY>)
>
> async for chunk in client.runs.stream(
>     None,  # (1)!
>     assistant_id,
>     input=inputs,
>     stream_mode="updates"
> ):
>     print(chunk.data)
> ```
>
> 1. We are passing `None` instead of a `thread_id` UUID.

> [tab] JavaScript
>
> ```javascript {highlight={5,6}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { Client } from "@langchain/langgraph-sdk";
> const client = new Client({ apiUrl: <DEPLOYMENT_URL>, apiKey: <API_KEY> });
>
> // create a streaming run
> const streamResponse = client.runs.stream(
>   null,  // (1)!
>   assistantID,
>   {
>     input,
>     streamMode: "updates"
>   }
> );
> for await (const chunk of streamResponse) {
>   console.log(chunk.data);
> }
> ```
>
> 1. We are passing `None` instead of a `thread_id` UUID.

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
> --url <DEPLOYMENT_URL>/runs/stream \
> --header 'Content-Type: application/json' \
> --header 'x-api-key: <API_KEY>'
> --data "{
>   \"assistant_id\": \"agent\",
>   \"input\": <inputs>,
>   \"stream_mode\": \"updates\"
> }"
> ```

## Join and stream

LangSmith allows you to join an active [background run](Runs/How%20to%20kick%20off%20background%20runs.md) and stream outputs from it. To do so, you can use [LangGraph SDK's](../../Get%20started/Reference/Related/langgraph_sdk.md) `client.runs.join_stream` method:

> [tab] Python
>
> ```python {highlight={4,6}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph_sdk import get_client
> client = get_client(url=<DEPLOYMENT_URL>, api_key=<API_KEY>)
>
> async for chunk in client.runs.join_stream(
>     thread_id,
>     run_id,  # (1)!
> ):
>     print(chunk)
> ```
>
> 1. This is the `run_id` of an existing run you want to join.

> [tab] JavaScript
>
> ```javascript {highlight={4,6}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { Client } from "@langchain/langgraph-sdk";
> const client = new Client({ apiUrl: <DEPLOYMENT_URL>, apiKey: <API_KEY> });
>
> const streamResponse = client.runs.joinStream(
>   threadID,
>   runId  // (1)!
> );
> for await (const chunk of streamResponse) {
>   console.log(chunk);
> }
> ```
>
> 1. This is the `run_id` of an existing run you want to join.

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request GET \
> --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/<RUN_ID>/stream \
> --header 'Content-Type: application/json' \
> --header 'x-api-key: <API_KEY>'
> ```

> [!WARNING]
>
> **Outputs not buffered**
> When you use `.join_stream`, output is not buffered, so any output produced before joining will not be received.

## Stream a thread

Thread streaming opens a long-lived connection for a thread and streams output from **every run** executed on that thread. This lets you monitor all activity on a thread from a single connection, for example, in a chat UI where multiple runs may be triggered over time through follow-up messages, [human-in-the-loop](Human-in-the-loop%20using%20server%20API.md) resumptions, or [background runs](Runs/How%20to%20kick%20off%20background%20runs.md). To join a specific existing run by ID, see [Join and stream](#join-and-stream).

### Compare thread and run streaming

| | Thread streaming | Run streaming |
| - | - | - |
| **SDK method** | `client.threads.join_stream()` | `client.runs.stream()` |
| **REST endpoint** | `GET /threads/{thread_id}/stream` | `POST /threads/{thread_id}/runs/stream` |
| **Scope** | All runs on a thread | A single run |
| **Connection lifetime** | Open indefinitely | Closes when the run completes |
| **Creates a run** | No | Yes |
| **Use case** | Monitor ongoing thread activity | Execute and stream a single interaction |

### Basic usage

> [tab] Python
>
> ```python {highlight={7}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph_sdk import get_client
> client = get_client(url=<DEPLOYMENT_URL>, api_key=<API_KEY>)
>
> thread = await client.threads.create()
> thread_id = thread["thread_id"]
>
> async for chunk in client.threads.join_stream(thread_id):
>     print(chunk)
> ```

> [tab] JavaScript
>
> ```javascript {highlight={7}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { Client } from "@langchain/langgraph-sdk";
> const client = new Client({ apiUrl: <DEPLOYMENT_URL>, apiKey: <API_KEY> });
>
> const thread = await client.threads.create();
> const threadID = thread["thread_id"];
>
> for await (const chunk of client.threads.joinStream(threadID)) {
>   console.log(chunk);
> }
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request GET \
> --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/stream \
> --header 'x-api-key: <API_KEY>'
> ```

### Thread stream modes

Thread streaming supports three stream modes that control which events are returned. Pass one or more modes via the `stream_mode` parameter.

| Mode | Description |
| - | - |
| `run_modes` (default) | Streams all run events, equivalent to `client.runs.stream()` output. |
| `lifecycle` | Streams only run start and end events. Use this for lightweight monitoring of run status without the full output. |
| `state_update` | Streams only state update events, providing the thread state after each run completes. |

> [tab] Python
>
> ```python {highlight={3}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> async for chunk in client.threads.join_stream(
>     thread_id,
>     stream_mode=["lifecycle", "state_update"],
> ):
>     print(chunk.event, chunk.data)
> ```

> [tab] JavaScript
>
> ```javascript {highlight={2}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> for await (const chunk of client.threads.joinStream(threadID, {
>   streamMode: ["lifecycle", "state_update"],
> })) {
>   console.log(chunk.event, chunk.data);
> }
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request GET \
> --url '<DEPLOYMENT_URL>/threads/<THREAD_ID>/stream?stream_modes=lifecycle&stream_modes=state_update' \
> --header 'x-api-key: <API_KEY>'
> ```

### Resume from last event

Thread streams support resumability via the `Last-Event-ID` header. If the connection drops, pass the ID of the last event you received to resume without missing events. Pass `"-"` to replay from the beginning.

> [tab] Python
>
> ```python {highlight={3}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> async for chunk in client.threads.join_stream(
>     thread_id,
>     last_event_id="<LAST_EVENT_ID>",
> ):
>     print(chunk)
> ```

> [tab] JavaScript
>
> ```javascript {highlight={2}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> for await (const chunk of client.threads.joinStream(threadID, {
>   lastEventId: "<LAST_EVENT_ID>",
> })) {
>   console.log(chunk);
> }
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request GET \
> --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/stream \
> --header 'x-api-key: <API_KEY>' \
> --header 'Last-Event-ID: <LAST_EVENT_ID>'
> ```

## API reference

For API usage and implementation, refer to the [API reference](../../Get%20started/Reference/Agent%20Server%20API/Agent%20Server%20API%20reference.md).
