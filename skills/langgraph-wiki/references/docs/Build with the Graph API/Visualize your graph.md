# Visualize your graph

> Render LangGraph graphs as Mermaid diagrams or PNG images for debugging and documentation.

Render a compiled graph as Mermaid text or a PNG image to inspect topology and debug routing. For an interactive UI, use [LangSmith Studio](../LangSmith%20Studio.md) with a [local server](../Deployment/Run%20a%20local%20server.md).

You can visualize any compiled graph that exposes `get_graph()`, including [`StateGraph`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph). See the [Graph](https://reference.langchain.com/python/langgraph/graphs/) reference.

The examples below use the same small graph in both languages: two nodes, a conditional edge from `node1`, and a loop back from `node2`.

```python
from typing import Literal

from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    value: int


def node1(state: State):
    return {"value": state["value"] + 1}


def node2(state: State):
    return {"value": state["value"] * 2}


def router(state: State) -> Literal["node2", "__end__"]:
    if state["value"] < 10:
        return "node2"
    return END


app = (
    StateGraph(State)
    .add_node("node1", node1)
    .add_node("node2", node2)
    .add_edge(START, "node1")
    .add_conditional_edges("node1", router)
    .add_edge("node2", "node1")
    .compile()
)
```

## Mermaid

Call `draw_mermaid()` on the drawable graph to get Mermaid syntax. Paste the string into any Mermaid renderer, or keep it in docs and PRs.

```python
print(app.get_graph().draw_mermaid())
```

```
---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	node1(node1)
	node2(node2)
	__end__([<p>__end__</p>]):::last
	__start__ --> node1;
	node1 -.-> __end__;
	node1 -.-> node2;
	node2 --> node1;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc
```

## PNG

Render the same graph as a `.png` with one of three approaches:

* Mermaid.ink API (default; no extra packages)
* Mermaid + Pyppeteer (`pip install pyppeteer`)
* Graphviz (`pip install pygraphviz`, plus the system [Graphviz](https://graphviz.org/download/) binary)

**Using Mermaid.ink**

By default, `draw_mermaid_png()` uses the Mermaid.ink API to generate the diagram.

```python
from IPython.display import Image, display

display(Image(app.get_graph().draw_mermaid_png()))
```

![Simple graph visualization](../../assets/images/26bcd9ccaec3-graph_api_image_10.png)

**Using Mermaid + Pyppeteer**

```python
import nest_asyncio
from IPython.display import Image, display
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles

nest_asyncio.apply()  # Required for Jupyter Notebook to run async functions

display(
    Image(
        app.get_graph().draw_mermaid_png(
            curve_style=CurveStyle.LINEAR,
            node_colors=NodeStyles(first="#ffdfba", last="#baffc9", default="#fad7de"),
            wrap_label_n_words=9,
            output_file_path=None,
            draw_method=MermaidDrawMethod.PYPPETEER,
            background_color="white",
            padding=10,
        )
    )
)
```

**Using Graphviz**

```python
from IPython.display import Image, display

try:
    display(Image(app.get_graph().draw_png()))
except ImportError:
    print(
        "Install pygraphviz to draw graphs with Graphviz: `pip install pygraphviz`. "
        "You also need the Graphviz system binary: https://graphviz.org/download/"
    )
```

## See also

* [Graph API overview](Graph%20API%20overview.md)
* [Use the Graph API](Build%20checklist%20for%20the%20Graph%20API.md)
* [LangSmith Studio](../LangSmith%20Studio.md)
* [Run a local server](../Deployment/Run%20a%20local%20server.md)
