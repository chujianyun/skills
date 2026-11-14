# Metadata parameters reference

When you trace LLM calls with LangSmith, you often want to [track costs](../../Configuration%20%26%20troubleshooting/Cost%20tracking.md), compare model configurations, and analyze performance across different providers. LangSmith's native integrations (like [LangChain](../Integrations/Agent%20frameworks/Trace%20LangChain%20agents%20%28Python%20and%20JS-TS%29.md) or the [OpenAI](../Integrations/LLM%20providers/Trace%20with%20OpenAI.md)/[Anthropic](../Integrations/LLM%20providers/Trace%20with%20Anthropic.md) wrappers) handle this automatically, but custom model wrappers and self-hosted models require a standardized way to provide this information. LangSmith uses `ls_` metadata parameters for this purpose.

These metadata parameters (all prefixed with `ls_`) let you pass model configuration and identification information through the standard `metadata` field. Once set, LangSmith can automatically calculate costs, display model information in the UI, and enable [filtering](../../../Debug/Viewing%20%26%20managing%20traces/Filter%20traces.md) and analytics across your traces.

Use `ls_` metadata parameters to:

* **Enable automatic cost tracking** for custom or self-hosted models by identifying the provider and model name.
* **Track model configuration** like temperature, max tokens, and other parameters for experiment comparison.
* **Filter and analyze traces** by provider or configuration settings
* **Customize Trajectory view rendering** for custom agent instrumentation.
* **Mark interrupted errors** so LangSmith can render interrupted runs separately from other errors.
* **Improve debugging** by recording exactly which model settings were used for each run.

## Basic usage example

The most common use case is enabling cost tracking for custom model wrappers. To do this, you need to provide two key pieces of information: the provider name (`ls_provider`) and the model name (`ls_model_name`). These work together to match against LangSmith's pricing database.

```python Python
from langsmith import traceable

@traceable(
    run_type="llm",
    metadata={
        "ls_provider": "my_provider",
        "ls_model_name": "my_custom_model"
    }
)
def my_custom_llm(prompt: str):
    return call_custom_api(prompt)
```

```typescript TypeScript
import { traceable } from "langsmith/traceable";

const myCustomLlm = traceable(
  async (prompt: string) => {
    return callCustomApi(prompt);
  },
  {
    run_type: "llm",
    metadata: {
      ls_provider: "my_provider",
      ls_model_name: "my_custom_model"
    }
  }
);
```

```java Java
import com.langchain.smith.tracing.RunType;
import com.langchain.smith.tracing.TraceConfig;
import com.langchain.smith.tracing.Tracing;
import java.util.HashMap;
import java.util.Map;
import java.util.function.Function;

Map<String, Object> metadata = new HashMap<>();
metadata.put("ls_provider", "my_provider");
metadata.put("ls_model_name", "my_custom_model");

Function<String, String> myCustomLlm =
    Tracing.traceFunction(
        prompt -> callCustomApi(prompt),
        TraceConfig.builder()
            .runType(RunType.LLM)
            .metadata(metadata)
            .build());
```

```kotlin Kotlin
import com.langchain.smith.tracing.RunType
import com.langchain.smith.tracing.TraceConfig
import com.langchain.smith.tracing.traceable

val myCustomLlm =
    traceable(
        { prompt: String -> callCustomApi(prompt) },
        TraceConfig.builder()
            .runType(RunType.LLM)
            .metadata(
                mapOf(
                    "ls_provider" to "my_provider",
                    "ls_model_name" to "my_custom_model",
                ),
            )
            .build(),
    )
```

This minimal setup tells LangSmith what model you're using, enabling automatic cost calculation if the model exists in the pricing database or if you've [configured custom pricing](../../Configuration%20%26%20troubleshooting/Cost%20tracking.md#llm-calls-automatically-track-costs-based-on-token-counts).

For more comprehensive tracking, you can include additional configuration parameters. This is especially useful when [running experiments](../../../../Test/Get%20started/Evaluation%20quickstart.md) or comparing different model settings:

```python Python
@traceable(
    run_type="llm",
    metadata={
        "ls_provider": "openai",
        "ls_model_name": "gpt-6.1-sol",
        "ls_temperature": 0.7,
        "ls_max_tokens": 4096,
        "ls_stop": ["END"],
        "ls_invocation_params": {
            "top_p": 0.9,
            "frequency_penalty": 0.5
        }
    }
)
def my_configured_llm(messages: list):
    return call_llm(messages)
```

```typescript TypeScript
const myConfiguredLlm = traceable(
  async (messages: Array<any>) => {
    return callLlm(messages);
  },
  {
    run_type: "llm",
    metadata: {
      ls_provider: "openai",
      ls_model_name: "gpt-6.1-sol",
      ls_temperature: 0.7,
      ls_max_tokens: 4096,
      ls_stop: ["END"],
      ls_invocation_params: {
        top_p: 0.9,
        frequency_penalty: 0.5
      }
    }
  }
);
```

```java Java
import com.langchain.smith.tracing.RunType;
import com.langchain.smith.tracing.TraceConfig;
import com.langchain.smith.tracing.Tracing;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;

Map<String, Object> metadata = new HashMap<>();
metadata.put("ls_provider", "openai");
metadata.put("ls_model_name", "gpt-6.1-sol");
metadata.put("ls_temperature", 0.7);
metadata.put("ls_max_tokens", 4096);
metadata.put("ls_stop", Collections.singletonList("END"));

Map<String, Object> invocationParams = new HashMap<>();
invocationParams.put("top_p", 0.9);
invocationParams.put("frequency_penalty", 0.5);
metadata.put("ls_invocation_params", invocationParams);

Function<List<Map<String, String>>, String> myConfiguredLlm =
    Tracing.traceFunction(
        messages -> callLlm(messages),
        TraceConfig.builder()
            .runType(RunType.LLM)
            .metadata(metadata)
            .build());
```

```kotlin Kotlin
val myConfiguredLlm =
    traceable(
        { messages: List<Map<String, String>> -> callLlm(messages) },
        TraceConfig.builder()
            .runType(RunType.LLM)
            .metadata(
                mapOf(
                    "ls_provider" to "openai",
                    "ls_model_name" to "gpt-6.1-sol",
                    "ls_temperature" to 0.7,
                    "ls_max_tokens" to 4096,
                    "ls_stop" to listOf("END"),
                    "ls_invocation_params" to
                        mapOf(
                            "top_p" to 0.9,
                            "frequency_penalty" to 0.5,
                        ),
                ),
            )
            .build(),
    )
```

With this setup, you can later filter traces by temperature, compare runs with different max token settings, or analyze which configuration parameters produce the best results. All these parameters are optional except for the `ls_provider` and `ls_model_name` pair needed for cost tracking.

## All parameters

### User-configurable parameters

| Parameter | Type | Required | Description |
| - | - | - | - |
| [`ls_provider`](#ls_provider) | `string` | Yes\* | LLM provider name for cost tracking |
| [`ls_model_name`](#ls_model_name) | `string` | Yes\* | Model identifier for cost tracking |
| [`ls_temperature`](#ls_temperature) | `number` | No | Temperature parameter used |
| [`ls_max_tokens`](#ls_max_tokens) | `number` | No | Maximum tokens parameter used |
| [`ls_stop`](#ls_stop) | `string[]` | No | Stop sequences used |
| [`ls_invocation_params`](#ls_invocation_params) | `object` | No | Additional invocation parameters |
| [`ls_agent_type`](#ls_agent_type) | `string` | No | Controls how agent runs appear in the Trajectory view: `"root"`, `"subagent"`, or `"middleware"` |
| [`ls_message_view_exclude`](#ls_message_view_exclude) | `boolean` | No | Hides the run from the Trajectory view |
| [`ls_is_error_interrupt`](#ls_is_error_interrupt) | `boolean` | No | Marks an errored run as interrupted when set to `true` |

\* `ls_provider` and `ls_model_name` must be provided together for cost tracking

### System-generated parameters

| Parameter | Type | Description |
| - | - | - |
| [`ls_run_depth`](#ls_run_depth) | `integer` | Depth in trace tree (0=root, 1=child, etc.) - automatically calculated |
| [`ls_method`](#ls_method) | `string` | Tracing method used (e.g., "traceable") - set by SDK |

### Experiment parameters

| Parameter | Type | Description |
| - | - | - |
| [`ls_example_*`](#ls_example_) | `any` | Example metadata prefixed with `ls_example_` - added during experiments |
| [`ls_experiment_id`](#ls_experiment_id) | `string` (UUID) | Unique experiment identifier - added during experiments |

## Parameter details

### `ls_provider`

* **Type:** `string`
* **Required:** Yes (with [`ls_model_name`](#ls_model_name))

**What it does:**
Identifies the LLM provider. Combined with `ls_model_name`, enables automatic cost calculation by matching against [LangSmith's model pricing database](https://smith.langchain.com/settings/workspaces/models).

**Common values:**

* `"openai"`
* `"anthropic"`
* `"azure"`
* `"bedrock"`
* `"google_vertexai"`
* `"google_genai"`
* `"fireworks"`
* `"mistral"`
* `"groq"`
* Or, any custom string

**When to use:**
When you want [automatic cost tracking](../../Configuration%20%26%20troubleshooting/Cost%20tracking.md) for custom model wrappers or self-hosted models.

**Example:**

```python
@traceable(
    run_type="llm",
    metadata={
        "ls_provider": "openai",
        "ls_model_name": "gpt-6.1-sol"
    }
)
def my_llm_call(prompt: str):
    return call_api(prompt)
```

**Relationships:**

* **Requires** [`ls_model_name`](#ls_model_name) for cost tracking to work.
* Works with token usage data to calculate costs.

### `ls_model_name`

* **Type:** `string`
* **Required:** Yes (with `ls_provider`)

**What it does:**
Identifies the specific model. Combined with `ls_provider`, matches against pricing database for automatic cost calculation.

**Common values:**

* OpenAI: `"gpt-6.1-sol"`, `"gpt-5.4-mini"`
* Anthropic: `"claude-sonnet-5-5"`, `"claude-opus-4-8"`
* Custom: Any model identifier

**When to use:**
When you want automatic [cost tracking](../../Configuration%20%26%20troubleshooting/Cost%20tracking.md) and model identification in the [UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-ls-metadata-parameters).

**Example:**

```python
@traceable(
    run_type="llm",
    metadata={
        "ls_provider": "anthropic",
        "ls_model_name": "claude-sonnet-5-5"
    }
)
def my_claude_call(messages: list):
    return call_claude(messages)
```

**Relationships:**

* **Requires** [`ls_provider`](#ls_provider) for cost tracking to work.
* Works with token usage data to calculate costs.

### `ls_temperature`

* **Type:** `number` (nullable)
* **Required:** No

**What it does:**
Records the temperature setting used. This is for tracking only—does not affect LangSmith behavior.

**When to use:**
When you want to track model configuration for experiments or debugging.

**Example:**

```python
metadata={
    "ls_provider": "openai",
    "ls_model_name": "gpt-6.1-sol",
    "ls_temperature": 0.7
}
```

**Relationships:**

* Independent; just for tracking.
* Useful alongside other config parameters for experiment comparison.

### `ls_max_tokens`

* **Type:** `number` (nullable)
* **Required:** No

**What it does:**
Records the maximum tokens setting used. This is for tracking only—does not affect LangSmith behavior.

**When to use:**
When you want to track model configuration for experiments or debugging.

**Example:**

```python
metadata={
    "ls_provider": "openai",
    "ls_model_name": "gpt-6.1-sol",
    "ls_max_tokens": 4096
}
```

**Relationships:**

* Independent; just for tracking.
* Useful for cost analysis when combined with actual token usage.

### `ls_stop`

* **Type:** `string[]` (nullable)
* **Required:** No

**What it does:**
Records stop sequences used. This is for tracking only—does not affect LangSmith behavior.

**When to use:**
When you want to track model configuration for experiments or debugging.

**Example:**

```python
metadata={
    "ls_provider": "openai",
    "ls_model_name": "gpt-6.1-sol",
    "ls_stop": ["END", "STOP", "\n\n"]
}
```

**Relationships:**

* Independent; just for tracking.

### `ls_invocation_params`

* **Type:** `object` (any key-value pairs)
* **Required:** No

**What it does:**
Stores additional model parameters that don't fit the specific `ls_` parameters. Can include provider-specific settings.

**Common parameters:**
`top_p`, `frequency_penalty`, `presence_penalty`, `top_k`, `seed`, or any custom parameters

**When to use:**
When you need to track additional configuration beyond the standard parameters.

**Example:**

```python
metadata={
    "ls_provider": "openai",
    "ls_model_name": "gpt-6.1-sol",
    "ls_invocation_params": {
        "top_p": 0.9,
        "frequency_penalty": 0.5,
        "presence_penalty": 0.3,
        "seed": 12345
    }
}
```

**Relationships:**

* Independent; stores arbitrary configuration.

### `ls_agent_type`

* **Type:** `"root" | "subagent" | "middleware"`
* **Required:** No

**What it does:**
Controls how messages from custom agent-like runs appear in the [Trajectory view](../../../Debug/Viewing%20%26%20managing%20traces/View%20traces.md#trajectory-view).

Tracing wrapper integrations from the latest versions of the LangSmith SDK set this metadata automatically when needed. For custom instrumentation, set this key on the run that represents the agent or middleware step.

**Values:**

* `"root"`: Messages from this run appear in the main Trajectory view.
* `"subagent"`: Messages from this run appear in a side thread, separate from the main conversation.
* `"middleware"`: Messages from this run are hidden from the Trajectory view.

**When to use:**
When you are building custom agent instrumentation and want the Trajectory view to distinguish root agents, subagents, and middleware.

For more details, see [Customize the Trajectory view](../../../Debug/Viewing%20%26%20managing%20traces/View%20traces.md#customize-the-trajectory-view).

**Relationships:**

* Independent of model identification and cost tracking metadata.
* Complements the trace parent-child structure by identifying the role a run plays in an agent trace.

### `ls_message_view_exclude`

* **Type:** `boolean` (presence-based)
* **Required:** No

**What it does:**
Hides the run from the [Trajectory view](../../../Debug/Viewing%20%26%20managing%20traces/View%20traces.md#trajectory-view). Excluded runs still appear in the regular trace view, runs explorer, and metrics.

The filter checks for the **presence of the key**, not truthiness. `{LS_MESSAGE_VIEW_EXCLUDE: False}` still excludes the run. Omit the key entirely to include the run.

**Import the constant:**
The key is exported as the `LS_MESSAGE_VIEW_EXCLUDE` constant from `langsmith` (Python and JS), whose value is the string `"ls_message_view_exclude"`. Prefer the constant to avoid typos; the literal string still works.

**When to use:**
For LLM subspans that are not conversational turns, such as classification calls, embedding lookups, safety filters, or routing/guardrail decisions, that you still want visible elsewhere in LangSmith but do not want cluttering the conversation transcript.

**Example:**

```python
from langsmith import LS_MESSAGE_VIEW_EXCLUDE, traceable

@traceable(run_type="llm", metadata={LS_MESSAGE_VIEW_EXCLUDE: True})
def classify_intent(query: str) -> str:
    return llm.predict(f"Classify: {query}")
```

For additional code examples across Python and JS contexts (`@traceable`, `trace`, `wrap_openai`, `RunnableConfig`, `wrapAISDK`, `RunTree.createChild`), see [Exclude runs from the Trajectory view](../../../Debug/Trajectory%20view/Trajectory%20view%20integrations.md#exclude-runs-from-the-trajectory-view).

**Relationships:**

* Independent of model identification and cost tracking metadata.
* Complements [`ls_agent_type`](#ls_agent_type), which routes messages by role rather than hiding the run entirely.

### `ls_is_error_interrupt`

* **Type:** `boolean`
* **Required:** No

**What it does:**
When set to `true` on a run with an error, marks the run status as interrupted instead of error.

**When to use:**
When your instrumentation can identify that an error represents an interrupted run, such as a user interruption or human-in-the-loop interruption, and you want LangSmith to render it separately from other errors.

**Example:**

```python
metadata={
    "ls_is_error_interrupt": True
}
```

**Relationships:**

* Only affects runs that include an error.
* Independent of model identification and cost tracking metadata.

### `ls_run_depth`

* **Type:** `integer`
* **Set by:** LangSmith backend (automatic)
* **Cannot be overridden**

**What it does:**
Indicates depth in the trace tree:

* `0` = Root run (top-level)
* `1` = Direct child
* `2` = Grandchild
* etc.

**When it's used:**
Automatically calculated during trace ingestion. Used for filtering (e.g., "show only root runs") and UI visualization.

**Example query:**

```
metadata_key = 'ls_run_depth' AND metadata_value = 0
```

**Relationships:**

* Determined by trace parent-child structure.
* Cannot be set manually.

### `ls_method`

* **Type:** `string`
* **Set by:** SDK (automatic)

**What it does:**
Indicates which SDK method created the trace (commonly `"traceable"` for `@traceable` decorator).

**When it's used:**
Automatically set by the tracing SDK. Used for debugging and analytics.

**Relationships:**

* Set by SDK based on how trace was created.
* Cannot be set manually.

### `ls_example_*`

* **Type:** Any (depends on example metadata)
* **Pattern:** `ls_example_{original_key}`
* **Set by:** LangSmith experiments system (automatic)

**What it does:**
When running [experiments on datasets](../../../../Test/Get%20started/Evaluation%20quickstart.md), metadata from the example is automatically prefixed with `ls_example_` and added to the trace.

**Special parameter:**

* `ls_example_dataset_split`: Dataset split (e.g., "train", "test", "validation")

**When it's used:**
During dataset experiments. Allows filtering/grouping by example characteristics.

**Example:**
If example has metadata `{"category": "technical", "difficulty": "hard"}`, trace gets:

```json
{
  "metadata": {
    "ls_example_category": "technical",
    "ls_example_difficulty": "hard",
    "ls_example_dataset_split": "test"
  }
}
```

**Relationships:**

* Automatically derived from example metadata.
* Cannot be set manually on traces.

### `ls_experiment_id`

* **Type:** `string` (UUID)
* **Set by:** LangSmith experiments system (automatic)

**What it does:**
Unique identifier for an experiment run.

**When it's used:**
Automatically added when running [experiments/evaluations on datasets](../../../../Test/Get%20started/Evaluation%20quickstart.md). Used to group all runs from the same experiment.

**Relationships:**

* Links runs to specific experiments.
* Cannot be set manually.

## Parameter relationships

### Cost tracking dependencies

For LangSmith to automatically calculate costs, several parameters must work together. Here's what's required:

**Primary requirement:** [`ls_provider`](#ls_provider) + [`ls_model_name`](#ls_model_name)

* Both should be present for automatic cost calculation.
* If [`ls_model_name`](#ls_model_name) is missing, system will fall back to checking [`ls_invocation_params`](#ls_invocation_params) for model name.
* [`ls_provider`](#ls_provider) must match a provider in the [pricing database](https://smith.langchain.com/settings/workspaces/models) (or use custom pricing).

**Additional requirements:**

* Run must have `run_type="llm"` (or [arbitrary cost tracking](../../Configuration%20%26%20troubleshooting/Cost%20tracking.md#other-runs-send-costs) must be enabled).
* [Token usage data](Log%20LLM%20calls.md#provide-token-and-cost-information) must be present in the trace (prompt\_tokens, completion\_tokens).
* Model must exist in pricing database or have [custom pricing configured](../../Configuration%20%26%20troubleshooting/Cost%20tracking.md#llm-calls-automatically-track-costs-based-on-token-counts).

**Fallback behavior:**
If [`ls_model_name`](#ls_model_name) is not in metadata, the system checks [`ls_invocation_params`](#ls_invocation_params) for model identifiers like `"model"` before giving up on cost tracking.

### Configuration tracking group

These parameters help you track model settings but don't affect LangSmith's core functionality:

**Optional, work independently:** [`ls_temperature`](#ls_temperature), [`ls_max_tokens`](#ls_max_tokens), [`ls_stop`](#ls_stop)

* These are for tracking/display.
* Do not affect LangSmith behavior or cost calculation.
* Useful for experiment comparison and debugging.

### Interrupt rendering

Set [`ls_is_error_interrupt`](#ls_is_error_interrupt) to `true` when a run error should be rendered as interrupted instead of error. This parameter only affects runs that include an error.

### Invocation params special case

The `ls_invocation_params` parameter has a dual role as both a tracking field and a fallback mechanism:

**[`ls_invocation_params`](#ls_invocation_params)**; partially independent with fallback role:

* Primarily stores arbitrary configuration for tracking.
* **Can serve as fallback** for cost tracking if [`ls_model_name`](#ls_model_name) is missing.
* Does not directly affect cost calculation when [`ls_model_name`](#ls_model_name) is present.

### System parameters

These parameters are automatically generated by LangSmith and cannot be manually set:

**Cannot be user-set:** [`ls_run_depth`](#ls_run_depth), [`ls_method`](#ls_method), [`ls_example_*`](#ls_example_), [`ls_experiment_id`](#ls_experiment_id)

* Automatically set by system.
* Used for filtering, analytics, and system tracking.

## Filter traces by metadata parameters

Once you've added `ls_` metadata parameters to your traces, you can use them to filter and search traces programmatically via the [API](../../../Reference/LangSmith%20REST%20API/Tracing/Query%20runs.md) or interactively in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-ls-metadata-parameters). This lets you narrow down traces by model, provider, configuration settings, or trace depth.

### Use the API

In an agent-based workspace, replace `my-app` below with the [environment's `tracer_session_name`](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project).

Use the [`Client`](https://reference.langchain.com/python/langsmith/client/Client) class with the `client.runs.query()` method to query traces based on metadata values. It takes a project ID and looks back 1 day unless you pass `min_start_time`. The [filter syntax](../../../Debug/Viewing%20%26%20managing%20traces/Trace%20query%20syntax.md) supports equality checks, comparisons, and logical operators. For more examples, see [Query traces using the SDK](../../../Debug/Viewing%20%26%20managing%20traces/Query%20traces%20using%20the%20SDK.md).

```python Python
import asyncio
from datetime import datetime, timedelta, timezone

from langsmith import Client


async def main():
    client = Client()
    project_id = str(client.read_project(project_name="my-app").id)
    since = datetime.now(timezone.utc) - timedelta(days=7)

    async def query(filter: str):
        return [
            run
            async for run in client.runs.query(
                project_ids=[project_id], min_start_time=since, filter=filter
            )
        ]

    # Filter runs by provider
    runs = await query('and(eq(metadata_key, "ls_provider"), eq(metadata_value, "openai"))')

    # Filter by specific model
    runs = await query('and(eq(metadata_key, "ls_model_name"), eq(metadata_value, "gpt-6.1-sol"))')

    # Filter root runs only (top-level traces)
    runs = await query('and(eq(metadata_key, "ls_run_depth"), eq(metadata_value, 0))')

    # Filter by temperature threshold
    runs = await query('and(eq(metadata_key, "ls_temperature"), gt(metadata_value, 0.5))')


asyncio.run(main())
```

```typescript TypeScript
import { Client } from "langsmith";

const client = new Client();
const projectId = (await client.readProject({ projectName: "my-app" })).id;
const since = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString();

async function query(filter: string) {
  const runs = [];
  for await (const run of client.runs.query({
    project_ids: [projectId],
    min_start_time: since,
    filter,
  })) {
    runs.push(run);
  }
  return runs;
}

// Filter runs by provider
const runsByProvider = await query('and(eq(metadata_key, "ls_provider"), eq(metadata_value, "openai"))');

// Filter by specific model
const runsByModel = await query('and(eq(metadata_key, "ls_model_name"), eq(metadata_value, "gpt-6.1-sol"))');

// Filter root runs only (top-level traces)
const rootRuns = await query('and(eq(metadata_key, "ls_run_depth"), eq(metadata_value, 0))');

// Filter by temperature threshold
const highTempRuns = await query('and(eq(metadata_key, "ls_temperature"), gt(metadata_value, 0.5))');
```

These examples show common filtering patterns:

* **Filter by provider or model** to analyze usage patterns or costs for specific models
* **Filter by run depth** to get only root traces (depth 0) or child runs at specific nesting levels
* **Filter by configuration** to compare experiments with different temperature, max tokens, or other settings

### Use the UI

In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-ls-metadata-parameters), use the filter/search bar with the [filter syntax](../../../Debug/Viewing%20%26%20managing%20traces/Trace%20query%20syntax.md):

```
metadata_key = 'ls_provider' AND metadata_value = 'openai'
metadata_key = 'ls_model_name' AND metadata_value = 'gpt-6.1-sol'
metadata_key = 'ls_run_depth' AND metadata_value = 0
```

## Related

* [Cost tracking guide](../../Configuration%20%26%20troubleshooting/Cost%20tracking.md): Learn how to track and analyze LLM costs in LangSmith.
* [Log LLM traces](Log%20LLM%20calls.md): Format requirements for logging LLM calls with proper token tracking.
* [Trace query syntax](../../../Debug/Viewing%20%26%20managing%20traces/Trace%20query%20syntax.md): Complete reference for filtering and searching traces.
* [Evaluation quickstart](../../../../Test/Get%20started/Evaluation%20quickstart.md): Run experiments on datasets to compare model configurations.
* [Add metadata and tags](../../Configuration%20%26%20troubleshooting/Data%20%26%20privacy/Add%20metadata%20and%20tags%20to%20traces.md): General guide to adding metadata to traces.
* [Filter traces (ClickHouse)](../../../Debug/Viewing%20%26%20managing%20traces/Filter%20traces%20%28ClickHouse%29.md): Programmatically filter traces in your code.
