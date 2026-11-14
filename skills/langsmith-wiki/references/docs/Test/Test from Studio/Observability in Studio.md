# Observability in Studio

LangSmith [Studio](LangSmith%20Studio.md) provides tools to inspect, debug, and improve your app beyond execution. By working with traces, datasets, and prompts, you can see how your application behaves in detail, measure its performance, and refine its outputs:

* [Iterate on prompts](#iterate-on-prompts): Modify prompts inside graph nodes directly or with the Playground.
* [Run experiments over a dataset](#run-experiments-over-a-dataset): Execute your assistant over a LangSmith dataset to score and compare results.
* [Debug LangSmith traces](#debug-langsmith-traces): Import traced runs into Studio and optionally clone them into your local agent.
* [Add a node to a dataset](#add-node-to-dataset): Turn parts of thread history into dataset examples for evaluation or further analysis.

## Iterate on prompts

Studio supports the following methods for modifying prompts in your graph:

* [Direct node editing](#direct-node-editing)
* [Playground interface](#playground)

### Direct node editing

Studio allows you to edit prompts used inside individual nodes, directly from the graph interface.

### Graph configuration

Define your [configuration](https://docs.langchain.com/oss/python/langgraph/graph-api-nodes.md#add-runtime-configuration) to specify prompt fields and their associated nodes using `langgraph_nodes` and `langgraph_type` keys.

#### `langgraph_nodes`

* **Description**: Specifies which nodes of the graph a configuration field is associated with.
* **Value Type**: Array of strings, where each string is the name of a node in your graph.
* **Usage Context**: Include in the `json_schema_extra` dictionary for Pydantic models or the `metadata["json_schema_extra"]` dictionary for dataclasses.
* **Example**:
  ```python
  system_prompt: str = Field(
      default="You are a helpful AI assistant.",
      json_schema_extra={"langgraph_nodes": ["call_model", "other_node"]},
  )
  ```

#### `langgraph_type`

* **Description**: Specifies the type of configuration field, which determines how it's handled in the UI.
* **Value Type**: String
* **Supported Values**:
  * `"prompt"`: Indicates the field contains prompt text that should be treated specially in the UI.
* **Usage Context**: Include in the `json_schema_extra` dictionary for Pydantic models or the `metadata["json_schema_extra"]` dictionary for dataclasses.
* **Example**:
  ```python
  system_prompt: str = Field(
      default="You are a helpful AI assistant.",
      json_schema_extra={
          "langgraph_nodes": ["call_model"],
          "langgraph_type": "prompt",
      },
  )
  ```

> [accordion] Full example configuration
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> ## Using Pydantic
> from pydantic import BaseModel, Field
> from typing import Annotated, Literal
>
> class Configuration(BaseModel):
>     """The configuration for the agent."""
>
>     system_prompt: str = Field(
>         default="You are a helpful AI assistant.",
>         description="The system prompt to use for the agent's interactions. "
>         "This prompt sets the context and behavior for the agent.",
>         json_schema_extra={
>             "langgraph_nodes": ["call_model"],
>             "langgraph_type": "prompt",
>         },
>     )
>
>     model: Annotated[
>         Literal[
>             "anthropic/claude-sonnet-4-6",
>             "anthropic/claude-haiku-4-5-20251001",
>             "openai/gpt-6.1-sol",
>             "openai/gpt-5.4-mini",
>         ],
>         {"__template_metadata__": {"kind": "llm"}},
>     ] = Field(
>         default="openai/gpt-5.4-mini",
>         description="The name of the language model to use for the agent's main interactions. "
>         "Should be in the form: provider/model-name.",
>         json_schema_extra={"langgraph_nodes": ["call_model"]},
>     )
>
> ## Using Dataclasses
> from dataclasses import dataclass, field
>
> @dataclass(kw_only=True)
> class Configuration:
>     """The configuration for the agent."""
>
>     system_prompt: str = field(
>         default="You are a helpful AI assistant.",
>         metadata={
>             "description": "The system prompt to use for the agent's interactions. "
>             "This prompt sets the context and behavior for the agent.",
>             "json_schema_extra": {"langgraph_nodes": ["call_model"]},
>         },
>     )
>
>     model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
>         default="anthropic/claude-sonnet-4-6",
>         metadata={
>             "description": "The name of the language model to use for the agent's main interactions. "
>             "Should be in the form: provider/model-name.",
>             "json_schema_extra": {"langgraph_nodes": ["call_model"]},
>         },
>     )
>
> ```

#### Editing prompts in the UI

1. Locate the gear icon on nodes with associated configuration fields.
2. Click to open the configuration modal.
3. Edit the values.
4. Save to update the current assistant version or create a new one.

### Playground

The [Playground](../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Create%20and%20manage%20prompts/Create%20a%20prompt.md) interface allows testing individual LLM calls without running the full graph:

1. Select a thread.
2. Click **View LLM Runs** on a node. This lists all the LLM calls (if any) made inside the node.
3. Select an LLM run to open in the Playground.
4. Modify prompts and test different model and tool settings.
5. Copy updated prompts back to your graph.

## Run experiments over a dataset

Studio lets you run [evaluations](../Get%20started/Evaluation%20concepts.md) by executing your assistant against a predefined LangSmith [dataset](../Get%20started/Evaluation%20concepts.md#datasets). This allows you to test performance across a variety of inputs, compare outputs to reference answers, and score results with configured [evaluators](../Get%20started/Evaluation%20concepts.md#evaluators).

This guide shows you how to run a full end-to-end experiment directly from Studio.

### Prerequisites

Before running an experiment, ensure you have the following:

* **A LangSmith dataset**: Your dataset should contain the inputs you want to test and optionally, reference outputs for comparison. The schema for the inputs must match the required input schema for the assistant. For more information on schemas, see the [graph API schema documentation](https://docs.langchain.com/oss/python/langgraph/graph-api.md#schema). For more on creating datasets, refer to [How to Manage Datasets](../Datasets%20%26%20Experiments/Datasets/Create%20a%20dataset/Create%20and%20manage%20datasets%20in%20the%20UI.md#create-a-dataset-and-add-examples).
* **(Optional) Evaluators**: You can attach evaluators (e.g., LLM-as-a-Judge, heuristics, or custom functions) to your dataset in LangSmith. These will run automatically after the graph has processed all inputs.
* **A running application**: The experiment can be run against:
  * An application deployed on [LangSmith](../../Deploy/Get%20started/LangSmith%20Agent%20Server.md).
  * A locally running application started via the [langgraph-cli](../../Deploy/Get%20started/Develop%20%26%20test/Local%20development%20%26%20testing.md).

> [!NOTE]
>
> Studio experiments follow the same [data retention](../../Monitor/Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#data-retention) rules as other experiments. By default, traces have base tier retention (14 days). However, traces will automatically upgrade to extended tier retention (180 days as of September 14, 2026) if feedback is added to them. Feedback can be added in one of two ways:
>
> * The [dataset has evaluators configured](../Evaluators/Automatically%20run%20evaluators%20on%20experiments.md).
> * [Feedback](../../Monitor/Trace/Observability%20concepts.md#feedback) is manually added to a trace.
>
> This auto-upgrade increases both the retention period and the cost of the trace. For more details, refer to [Data retention auto-upgrades](../../Monitor/Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#how-it-works).

### Experiment setup

1. Launch the experiment. Click the **Run experiment** button in the top right corner of the Studio page.
2. Select your dataset. In the modal that appears, select the dataset (or a specific dataset split) to use for the experiment and click **Start**.
3. Monitor the progress. All of the inputs in the dataset will now be run against the active assistant. Monitor the experiment's progress via the badge in the top right corner.
4. You can continue to work in Studio while the experiment runs in the background. Click the arrow icon button at any time to navigate to LangSmith and view the detailed experiment results.

## Debug LangSmith traces

This guide explains how to open LangSmith traces in Studio for interactive investigation and debugging.

### Open deployed threads

1. Open the LangSmith trace, selecting the root run.
2. Click **Run in Studio**.

This will open Studio connected to the associated deployment with the trace's parent thread selected.

### Testing local agents with remote traces

This section explains how to test a local agent against remote traces from LangSmith. This enables you to use production traces as input for local testing, allowing you to debug and verify agent modifications in your development environment.

#### Prerequisites

* A LangSmith traced thread
* A [locally running agent](../../Deploy/Get%20started/Develop%20%26%20test/Local%20development%20%26%20testing.md).

> [!NOTE]
>
> **Local agent requirements**
>
> * langgraph>=0.3.18
> * langgraph-api>=0.0.32
> * Contains the same set of nodes present in the remote trace

#### Clone thread

1. Open the LangSmith trace, selecting the root run.
2. Click the dropdown next to **Run in Studio**.
3. Enter your local agent's URL.
4. Select **Clone thread locally**.
5. If multiple graphs exist, select the target graph.

A new thread will be created in your local agent with the thread history inferred and copied from the remote thread, and you will be navigated to Studio for your locally running application.

## Add node to dataset

Add [examples](../Get%20started/Evaluation%20concepts.md#examples) to [LangSmith datasets](../Datasets%20%26%20Experiments/Datasets/Manage%20datasets.md) from nodes in the thread log. This is useful to evaluate individual steps of the agent.

1. Select a thread.
2. Click **Add to Dataset**.
3. Select nodes whose input/output you want to add to a dataset.
4. For each selected node, select the target dataset to create the example in. By default a dataset for the specific assistant and node will be selected. If this dataset does not yet exist, it will be created.
5. Edit the example's input/output as needed before adding it to the dataset.
6. Select **Add to dataset** at the bottom of the page to add all selected nodes to their respective datasets.

For more details, refer to [How to evaluate an application's intermediate steps](../Datasets%20%26%20Experiments/Evaluation%20techniques/Define%20evaluation%20target/How%20to%20evaluate%20an%20application%27s%20intermediate%20steps.md).
