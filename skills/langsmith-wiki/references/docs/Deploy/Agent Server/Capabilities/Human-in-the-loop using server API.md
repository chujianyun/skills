# Human-in-the-loop using server API

To review, edit, and approve tool calls in an agent or workflow, use LangGraph's [human-in-the-loop](https://docs.langchain.com/oss/python/langgraph/interrupts.md) features.

## Dynamic interrupts

> [tab] Python
>
> ```python {highlight={2,34}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph_sdk import get_client
> from langgraph_sdk.schema import Command
> client = get_client(url=<DEPLOYMENT_URL>)
>
> # Using the graph deployed with the name "agent"
> assistant_id = "agent"
>
> # create a thread
> thread = await client.threads.create()
> thread_id = thread["thread_id"]
>
> # Run the graph until the interrupt is hit.
> result = await client.runs.wait(
>     thread_id,
>     assistant_id,
>     input={"some_text": "original text"}   # (1)!
> )
>
> print(result['__interrupt__']) # (2)!
> # > [
> # >     {
> # >         'value': {'text_to_revise': 'original text'},
> # >         'resumable': True,
> # >         'ns': ['human_node:fc722478-2f21-0578-c572-d9fc4dd07c3b'],
> # >         'when': 'during'
> # >     }
> # > ]
>
>
> # Resume the graph
> print(await client.runs.wait(
>     thread_id,
>     assistant_id,
>     command=Command(resume="Edited text")   # (3)!
> ))
> # > {'some_text': 'Edited text'}
> ```
>
> 1. The graph is invoked with some initial state.
> 2. When the graph hits the interrupt, it returns an interrupt object with the payload and metadata.
>    3\. The graph is resumed with a `Command(resume=...)`, injecting the human's input and continuing execution.

> [tab] JavaScript
>
> ```javascript {highlight={32}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
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
> // Run the graph until the interrupt is hit.
> const result = await client.runs.wait(
>   threadID,
>   assistantID,
>   { input: { "some_text": "original text" } }   # (1)!
> );
>
> console.log(result['__interrupt__']); # (2)!
> // > [
> # >     {
> # >         'value': {'text_to_revise': 'original text'},
> # >         'resumable': True,
> # >         'ns': ['human_node:fc722478-2f21-0578-c572-d9fc4dd07c3b'],
> # >         'when': 'during'
> # >     }
> # > ]
>
> // Resume the graph
> console.log(await client.runs.wait(
>     threadID,
>     assistantID,
>     { command: { resume: "Edited text" }}   # (3)!
> ));
> # > {'some_text': 'Edited text'}
> ```
>
> 1. The graph is invoked with some initial state.
> 2. When the graph hits the interrupt, it returns an interrupt object with the payload and metadata.
> 3. The graph is resumed with a `{ resume: ... }` command object, injecting the human's input and continuing execution.

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
> Run the graph until the interrupt is hit.:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
> --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/wait \
> --header 'Content-Type: application/json' \
> --data "{
>   \"assistant_id\": \"agent\",
>   \"input\": {\"some_text\": \"original text\"}
> }"
> ```
>
> Resume the graph:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
>  --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/wait \
>  --header 'Content-Type: application/json' \
>  --data "{
>    \"assistant_id\": \"agent\",
>    \"command\": {
>      \"resume\": \"Edited text\"
>    }
>  }"
> ```

> [accordion] Extended example: using `interrupt`
>
> This is an example graph you can run in the Agent Server.
> See [LangSmith quickstart](../../Get%20started/Deploy%20your%20app%20to%20cloud.md) for more details.
>
> ```python {highlight={7,13}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from typing import TypedDict
>
> from langgraph.checkpoint.memory import InMemorySaver
> from langgraph.constants import START
> from langgraph.graph import StateGraph
> from langgraph.types import interrupt, Command
>
> class State(TypedDict):
>     some_text: str
>
> def human_node(state: State):
>     value = interrupt( # (1)!
>         {
>             "text_to_revise": state["some_text"] # (2)!
>         }
>     )
>     return {
>         "some_text": value # (3)!
>     }
>
>
> # Build the graph
> graph_builder = StateGraph(State)
> graph_builder.add_node("human_node", human_node)
> graph_builder.add_edge(START, "human_node")
>
> graph = graph_builder.compile()
> ```
>
> 1. `interrupt(...)` pauses execution at `human_node`, surfacing the given payload to a human.
> 2. Any JSON serializable value can be passed to the [`interrupt`](https://reference.langchain.com/python/langgraph/types/interrupt) function. Here, a dict containing the text to revise.
> 3. Once resumed, the return value of `interrupt(...)` is the human-provided input, which is used to update the state.
>
> Once you have a running Agent Server, you can interact with it using
> [LangGraph SDK](../../Get%20started/Reference/Related/langgraph_sdk.md)
>
> > [tab] Python
> >
> > ```python {highlight={2,34}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langgraph_sdk import get_client
> > from langgraph_sdk.schema import Command
> > client = get_client(url=<DEPLOYMENT_URL>)
> >
> > # Using the graph deployed with the name "agent"
> > assistant_id = "agent"
> >
> > # create a thread
> > thread = await client.threads.create()
> > thread_id = thread["thread_id"]
> >
> > # Run the graph until the interrupt is hit.
> > result = await client.runs.wait(
> >     thread_id,
> >     assistant_id,
> >     input={"some_text": "original text"}   # (1)!
> > )
> >
> > print(result['__interrupt__']) # (2)!
> > # > [
> > # >     {
> > # >         'value': {'text_to_revise': 'original text'},
> > # >         'resumable': True,
> > # >         'ns': ['human_node:fc722478-2f21-0578-c572-d9fc4dd07c3b'],
> > # >         'when': 'during'
> > # >     }
> > # > ]
> >
> >
> > # Resume the graph
> > print(await client.runs.wait(
> >     thread_id,
> >     assistant_id,
> >     command=Command(resume="Edited text")   # (3)!
> > ))
> > # > {'some_text': 'Edited text'}
> > ```
> >
> > 1. The graph is invoked with some initial state.
> > 2. When the graph hits the interrupt, it returns an interrupt object with the payload and metadata.
> >    3\. The graph is resumed with a `Command(resume=...)`, injecting the human's input and continuing execution.
>
> > [tab] JavaScript
> >
> > ```javascript {highlight={32}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
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
> > // Run the graph until the interrupt is hit.
> > const result = await client.runs.wait(
> >   threadID,
> >   assistantID,
> >   { input: { "some_text": "original text" } }   # (1)!
> > );
> >
> > console.log(result['__interrupt__']); # (2)!
> > # > [
> > # >     {
> > # >         'value': {'text_to_revise': 'original text'},
> > # >         'resumable': True,
> > # >         'ns': ['human_node:fc722478-2f21-0578-c572-d9fc4dd07c3b'],
> > # >         'when': 'during'
> > # >     }
> > # > ]
> >
> > // Resume the graph
> > console.log(await client.runs.wait(
> >     threadID,
> >     assistantID,
> >     { command: { resume: "Edited text" }}   # (3)!
> > ));
> > # > {'some_text': 'Edited text'}
> > ```
> >
> > 1. The graph is invoked with some initial state.
> > 2. When the graph hits the interrupt, it returns an interrupt object with the payload and metadata.
> > 3. The graph is resumed with a `{ resume: ... }` command object, injecting the human's input and continuing execution.
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
> > Run the graph until the interrupt is hit:
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > curl --request POST \
> > --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/wait \
> > --header 'Content-Type: application/json' \
> > --data "{
> >   \"assistant_id\": \"agent\",
> >   \"input\": {\"some_text\": \"original text\"}
> > }"
> > ```
> >
> > Resume the graph:
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > curl --request POST \
> > --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/wait \
> > --header 'Content-Type: application/json' \
> > --data "{
> >   \"assistant_id\": \"agent\",
> >   \"command\": {
> >     \"resume\": \"Edited text\"
> >   }
> > }"
> > ```

## Static interrupts

Static interrupts (also known as static breakpoints) are triggered either before or after a node executes.

> [!WARNING]
>
> Static interrupts are **not** recommended for human-in-the-loop workflows. They are best used for debugging and testing.

You can set static interrupts by specifying `interrupt_before` and `interrupt_after` at compile time:

```python {highlight={1,2,3}}
graph = graph_builder.compile( # (1)!
    interrupt_before=["node_a"], # (2)!
    interrupt_after=["node_b", "node_c"], # (3)!
)
```

1. The breakpoints are set during `compile` time.
2. `interrupt_before` specifies the nodes where execution should pause before the node is executed.
3. `interrupt_after` specifies the nodes where execution should pause after the node is executed.

Alternatively, you can set static interrupts at run time:

> [tab] Python
>
> ```python {highlight={1,5,6}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> await client.runs.wait( # (1)!
>     thread_id,
>     assistant_id,
>     inputs=inputs,
>     interrupt_before=["node_a"], # (2)!
>     interrupt_after=["node_b", "node_c"] # (3)!
> )
> ```
>
> 1. `client.runs.wait` is called with the `interrupt_before` and `interrupt_after` parameters. This is a run-time configuration and can be changed for every invocation.
> 2. `interrupt_before` specifies the nodes where execution should pause before the node is executed.
> 3. `interrupt_after` specifies the nodes where execution should pause after the node is executed.

> [tab] JavaScript
>
> ```javascript {highlight={1,6,7}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> await client.runs.wait( // (1)!
>     threadID,
>     assistantID,
>     {
>     input: input,
>     interruptBefore: ["node_a"], // (2)!
>     interruptAfter: ["node_b", "node_c"] // (3)!
>     }
> )
> ```
>
> 1. `client.runs.wait` is called with the `interruptBefore` and `interruptAfter` parameters. This is a run-time configuration and can be changed for every invocation.
> 2. `interruptBefore` specifies the nodes where execution should pause before the node is executed.
> 3. `interruptAfter` specifies the nodes where execution should pause after the node is executed.

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
> --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/wait \
> --header 'Content-Type: application/json' \
> --data "{
>     \"assistant_id\": \"agent\",
>     \"interrupt_before\": [\"node_a\"],
>     \"interrupt_after\": [\"node_b\", \"node_c\"],
>     \"input\": <INPUT>
> }"
> ```

The following example shows how to add static interrupts:

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
> # Run the graph until the breakpoint
> result = await client.runs.wait(
>     thread_id,
>     assistant_id,
>     input=inputs   # (1)!
> )
>
> # Resume the graph
> await client.runs.wait(
>     thread_id,
>     assistant_id,
>     input=None   # (2)!
> )
> ```
>
> 1. The graph is run until the first breakpoint is hit.
> 2. The graph is resumed by passing in `None` for the input. This will run the graph until the next breakpoint is hit.

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
> // Run the graph until the breakpoint
> const result = await client.runs.wait(
>   threadID,
>   assistantID,
>   { input: input }   # (1)!
> );
>
> // Resume the graph
> await client.runs.wait(
>   threadID,
>   assistantID,
>   { input: null }   # (2)!
> );
> ```
>
> 1. The graph is run until the first breakpoint is hit.
> 2. The graph is resumed by passing in `null` for the input. This will run the graph until the next breakpoint is hit.

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
> Run the graph until the breakpoint:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
> --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/wait \
> --header 'Content-Type: application/json' \
> --data "{
>   \"assistant_id\": \"agent\",
>   \"input\": <INPUT>
> }"
> ```
>
> Resume the graph:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
> --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/wait \
> --header 'Content-Type: application/json' \
> --data "{
>   \"assistant_id\": \"agent\"
> }"
> ```

## Learn more

* [Human-in-the-loop conceptual guide](https://docs.langchain.com/oss/python/langgraph/interrupts.md): learn more about LangGraph human-in-the-loop features.
* [Common patterns](https://docs.langchain.com/oss/python/langgraph/interrupts.md#common-patterns): learn how to implement patterns like approving/rejecting actions, requesting user input, tool call review, and validating human input.
* [Human-in-the-loop over MCP](Human-in-the-loop%20over%20MCP.md): answer interrupts from an MCP client.
