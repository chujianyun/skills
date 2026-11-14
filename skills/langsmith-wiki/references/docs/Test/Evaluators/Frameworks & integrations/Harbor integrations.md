# Harbor integrations

> Run evaluations, Deep Agents, and sandboxes on LangSmith with Harbor.

Use LangSmith to run, trace, compare, and cost agent evaluations from one place, with [Harbor](https://harborframework.com/docs) as the execution layer. Harbor is a framework for evaluating and optimizing agents and language models in sandboxed environments, from the creators of [Terminal-Bench](https://www.tbench.ai). It runs each trial in an isolated container, so you can parallelize evaluations and rollouts across many environments at once.

LangSmith integrates with Harbor at three points:

* **LangSmith evaluations**: Record every Harbor job to LangSmith as an experiment with `--plugin langsmith`.
* **Deep Agents**: Run an agent built with LangGraph or Deep Agents in Harbor with `--agent langgraph`.
* **Sandboxes**: Run each Harbor trial on a LangSmith sandbox with `--env langsmith`.

This page covers the LangSmith-specific Harbor flags. For the complete CLI, run `harbor run --help` or see the [Harbor documentation](https://harborframework.com/docs).

## Prerequisites

* A [LangSmith account](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-harbor-integrations) and an [API key](../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md).
* Python 3.12 or later with `pip`.
* A provider API key for the model your agent calls, such as `ANTHROPIC_API_KEY`.

### Install

Install Harbor with the `langsmith` extra. The extra includes the `harbor-langsmith` package used by the LangSmith plugin, environment, and agent:

```bash
pip install "harbor[langsmith]"
```

### Authenticate

Harbor authenticates with your LangSmith credentials. Set an API key and the endpoint that key belongs to:

```bash
export LANGSMITH_API_KEY="<SECRET>"
export LANGSMITH_ENDPOINT="<LANGSMITH_ENDPOINT>"
```

`LANGSMITH_ENDPOINT` defaults to `https://api.smith.langchain.com` (GCP US). Set it to your data plane URL on [BYOC](../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md), your instance URL on [self-hosted](../../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md), or the [API URL for your region](../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md#configure-the-sdk) on other Cloud regions.

Alternatively, select a [LangSmith SDK profile](../../../LangSmith%20setup/Account/Profile%20configuration.md) instead of exporting a key:

```bash
export LANGSMITH_PROFILE=prod
```

## Quickstart

Record a Harbor job to LangSmith as an experiment:

```bash
harbor run -d "terminal-bench@2.0" \
  --agent <agent> \
  --model <provider:model> \
  --plugin langsmith
```

Replace `<agent>` with a Harbor agent, and `<provider:model>` with a model in `provider:model` format that an installed `langchain-*` provider can resolve, for example `anthropic:claude-opus-4-8`. Run `harbor run --help` to list the available agents, or see [Deep Agents](#deep-agents) for a complete `langgraph` run.

Open [Datasets & Experiments](../../Datasets%20%26%20Experiments/Datasets/Manage%20datasets.md), select the dataset Harbor synced, such as `terminal-bench@2.0`, then open the Experiments tab to view the run.

## LangSmith evaluations

The LangSmith plugin records every Harbor job to LangSmith, so you can view and compare results under Datasets & Experiments. The plugin works with any Harbor agent, not only Deep Agents. Enable it with `--plugin langsmith`. The [Quickstart](#quickstart) shows the basic invocation, and this section covers what the plugin records and how to configure it.

Choose an agent that traces to LangSmith to capture full agent traces alongside the experiment. If the agent does not trace to LangSmith, the plugin still creates the dataset and the experiment with results and feedback, without the agent trace.

Pass the full import path instead of the short plugin name when you need to disambiguate it:

```bash
harbor run ... --plugin harbor_langsmith:LangSmithPlugin
```

The plugin requires `LANGSMITH_API_KEY`.

### See what the plugin records

As the job runs, the plugin writes to LangSmith over the API:

* **Dataset**: Syncs a reference dataset from the job. The default name comes from the dataset or task, for example `terminal-bench@2.0`. Each task becomes an example whose inputs are the task name, the instruction, and the task ID.
* **Experiment**: Creates one experiment per job, named `<name>-<job-id-prefix>`, linked to the reference dataset.
* **Runs**: Creates a root run per trial with inputs for the task name, instruction, agent, and model, plus child runs for the environment, agent, and verification phases.
* **Feedback**: Attaches one feedback score per verifier reward key, such as `reward`, and a `harbor_error` feedback when a trial raises an exception.
* **Outputs**: Records token counts under `tokens` (`input`, `cache`, `output`) and the run cost under `cost_usd` for each trial run.

### View results in LangSmith

Open [Datasets & Experiments](../../Datasets%20%26%20Experiments/Datasets/Manage%20datasets.md) in LangSmith, select the dataset the plugin synced, such as `terminal-bench@2.0`, then open the Experiments tab. Each Harbor job appears as an experiment, and you can [compare experiments](../../Datasets%20%26%20Experiments/Analyze%20experiment%20results/Analyze%20an%20experiment.md) by the `reward` and `harbor_error` feedback, the token counts and cost recorded on each run, and latency.

### Configure the plugin inputs

The plugin reads each input from a constructor keyword argument first, then falls back to an environment variable. Set the inputs with environment variables:

* **`HARBOR_LANGSMITH_DATASET`**: The dataset name. Defaults to a name derived from the job.
* **`HARBOR_LANGSMITH_EXPERIMENT`**: The experiment base name. Defaults to the job name.
* **`LANGSMITH_ENDPOINT`**: The LangSmith API endpoint. Defaults to `https://api.smith.langchain.com`.
* **`LANGSMITH_WORKSPACE_ID`**: The target workspace.
* **`HARBOR_LANGSMITH_SYNC_DATASET`**: Set to `false` to disable dataset and example syncing.
* **`HARBOR_LANGSMITH_FAIL_FAST`**: Set to `true` to raise on a LangSmith API error instead of continuing the job.

Or set the same inputs as plugin kwargs with `--pk` on the command line, or under `kwargs:` in a job config file. The kwargs mirror the constructor options: `dataset_name`, `experiment_name`, `endpoint`, `api_key`, `workspace_id`, `sync_dataset`, and `fail_fast`.

## Deep Agents

For standalone agent traces in an agent-based workspace, [register the agent](../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) and set the integration's `LANGSMITH_PROJECT` setting to the selected environment's `tracer_session_name`. Dataset-linked experiments use the evaluation flow above.

The `langgraph` integration runs your LangGraph or Deep Agents code in Harbor. Select it with `--agent langgraph`. Harbor stages your project into the sandbox, installs its dependencies, and runs the graph inside the container for each trial.

Set your LangSmith and model credentials, then run Harbor. `harbor run` is an alias for `harbor job start`, which builds a job, spins up the environment, and runs the LangGraph agent:

```bash
export LANGSMITH_PROFILE=prod
export LANGSMITH_TRACING=true
export LANGSMITH_PROJECT=harbor-deepagents
export FIREWORKS_API_KEY="<SECRET>"

harbor run \
  -t hello-world/hello-world \
  --agent langgraph \
  --model fireworks:accounts/fireworks/models/glm-5p2 \
  --ak project_path=./deep-agent \
  --ak graph=deep_agent
```

### Choose what to evaluate against

A task is one directory with a fixed layout: `task.toml` for configuration, `instruction.md` for the prompt, `environment/` for the Dockerfile the sandbox is built from, and `tests/` for the verifier that writes the reward. A dataset is many such task directories.

A task or dataset can be local or remote: point Harbor at your own folder of task directories, or pull one from Harbor's registry.

Three inputs select the tasks a job runs against:

* **`-t org/name[@ref]`**: A single task from the registry. Remote tasks are fetched with a registry lookup, then cloned at the pinned commit into `~/.cache/harbor/tasks`.
* **`-d name@version`**: A whole benchmark dataset, which is many tasks. Each task is resolved from the registry and cloned into the cache.
* **`-p <dir>`**: A local path to one task or a root folder of many tasks. Local paths are read in place, with no download and no cache copy.

Filter the selected tasks with `-i` and `-x` (glob include and exclude) and cap the count with `-l`.

A task directory has this layout:

```text
hello-world/
├── task.toml         # timeouts, CPU, and memory
├── instruction.md    # the prompt given to the agent
├── environment/
│   └── Dockerfile    # image the sandbox is built from
├── tests/
│   ├── test.sh       # writes the reward to /logs/verifier/reward.txt
│   └── test_state.py # the assertions
└── solution/         # optional, used only by the oracle agent
```

A dataset is a directory of task directories:

```text
terminal-bench/
├── hello-world/      # each subdirectory is a full task
├── fix-bug/          # (task.toml + instruction.md + environment/ + tests/)
└── parse-csv/
```

### Configure the agent

Pass agent kwargs with `--ak`:

* **`--agent langgraph`**: Selects the LangGraph agent.
* **`--model <provider:model>`**: The model to run. There is no default, so this value is required. The agent resolves it with [init\_chat\_model](https://reference.langchain.com/python/langchain/chat_models/base/init_chat_model), so it must be resolvable by an installed `langchain-*` provider in `provider:model` format, for example `anthropic:claude-opus-4-8`. A `provider/model` value is normalized to `provider:model`. The model comes from `configurable['model']` or the `HARBOR_MODEL` environment variable, and an unresolvable or missing value raises a `ValueError`.
* **`--ak project_path=<dir>`**: The local directory that contains `langgraph.json`.
* **`--ak graph=<name>`**: Which graph in `langgraph.json` to run.
* **`--ak config=<file>`**: The config filename inside `project_path` that declares the graphs. Defaults to `langgraph.json`.
* **`--ak configurable='{...}'`**: LangGraph per-run config passed to `config["configurable"]` and read by the graph at invoke time. Common keys are `model`, `model_kwargs`, and `cwd`.
* **`--ak model_kwargs='{...}'`**: Shorthand for the nested `model_kwargs` key in `configurable`, for example `{"temperature": 0, "max_tokens": 8000}`.
* **`--ak dependency_overrides='[...]'`**: Pip packages for the agent virtual environment. This list replaces the dependencies declared in `langgraph.json`, which lets you pin or swap versions without editing the project, for example `'["deepagents==0.6.10"]'`.

### Point langgraph.json at the agent and dependencies

The agent loads graphs from the `langgraph.json` file in `project_path`. The file declares the graph entry points and the pip dependencies Harbor installs in the sandbox virtual environment:

```json
{
  "dependencies": [
    "deepagents>=0.6.10,<0.7.0",
    "langchain-anthropic>=1.4.6,<1.5.0",
    "langchain-openai>=1.3.0,<1.4.0"
  ],
  "graphs": {
    "deep_agent": "./agent.py:make_graph",
    "research_agent": "./agent.py:make_research_graph"
  }
}
```

The project exposes two graphs, selected with `--ak graph`. Both build a Deep Agent with [create\_deep\_agent](https://reference.langchain.com/python/deepagents/graph/create_deep_agent) and differ only in their inputs:

* **`deep_agent`** resolves to `make_graph`, a Deep Agent created with only the model.
* **`research_agent`** resolves to `make_research_graph`, the same Deep Agent with a research system prompt.

Each graph passes the model from `--model` (read from `configurable.model`) to `create_deep_agent`, which resolves it with `init_chat_model()`:

```python
from deepagents import create_deep_agent


def make_graph(config):
    return create_deep_agent(model=config["configurable"]["model"])


def make_research_graph(config):
    return create_deep_agent(
        model=config["configurable"]["model"],
        system_prompt="You are a research assistant.",
    )
```

A factory function that reads `configurable.model` keeps the graph model-agnostic, but you can also hardcode the model in the graph when it should always run the same one. For a fixed model, point `langgraph.json` at a compiled graph instead of a factory:

```python
from deepagents import create_deep_agent

graph = create_deep_agent(model="fireworks:accounts/fireworks/models/glm-5p2")
```

### Run the agent inside the sandbox

Harbor runs the entire agent inside the trial container.

> [accordion] Single-trial lifecycle
>
> 1. **Parse and prepare**: `harbor run` parses the flags into a job config. The job factory resolves and caches the tasks, validates the environment resource limits, and resolves the metrics before any trial runs. Caching applies to remote tasks only, so a `-p` local task is read in place.
> 2. **Fan out**: Harbor builds the trial list from `n_attempts × tasks × agents`, then runs trials concurrently up to the `-n` limit, with `-r` retries. Parallelism is per trial, so different tasks, agents, and attempts run together, each in its own sandbox.
> 3. **Create the trial**: The trial loads the cached task, builds the LangGraph agent from `project_path`, `graph`, and `model`, and constructs the environment without starting it.
> 4. **Start the environment**: The environment starts and brings up the container. For the Docker environment, this builds or reuses the image and runs the container.
> 5. **Install the agent**: Harbor creates a virtual environment in the container, uploads `project_path`, and pip installs the `langgraph.json` dependencies inside the container.
> 6. **Run and verify**: Harbor runs the graph inside the container through the LangGraph runner, then runs `tests/test.sh`, which writes the reward to `/logs/verifier/reward.txt`.
> 7. **Finalize**: Harbor stops and deletes the container and writes the trial result. The job aggregates all trial results into one job result.

For more information on building Deep Agents, see the [Deep Agents documentation](https://docs.langchain.com/oss/python/deepagents/overview.md).

## Sandboxes

The `langsmith` Harbor environment runs each trial on a LangSmith sandbox. Select it with `--env langsmith` to execute Harbor jobs on LangSmith infrastructure, alongside other sandbox providers. Each trial gets its own sandbox, which Harbor deletes when the trial finishes.

### Run an evaluation

Run a Harbor job and select the LangSmith environment with `--env langsmith`:

```bash
harbor run -d "<org/name>" \
  --model "<model>" \
  --agent "<agent>" \
  --env langsmith \
  -n "<n-parallel-trials>"
```

Harbor creates one LangSmith sandbox per trial and runs the agent and verifier inside it.

### Configure the sandbox environment

The LangSmith environment boots each sandbox from a filesystem snapshot. Provide one of the following in your Harbor task:

* **Prebuilt image**: Set `[environment].docker_image` in `task.toml`. Harbor reuses or creates a snapshot from that image.
* **Existing snapshot**: Pass `environment.kwargs.snapshot_name` to boot from a [snapshot](../../../Deploy/Sandboxes/Sandbox%20snapshots.md) you already created.
* **Dockerfile**: Include an `environment/Dockerfile`. Harbor builds a snapshot from it with the [build-from-Dockerfile flow](../../../Deploy/Sandboxes/Sandbox%20snapshots.md#build-a-snapshot-from-a-dockerfile), using the task `environment/` directory as the build context.

Tune the sandbox lifecycle with environment kwargs, passed on the command line with `--ek`:

```bash
harbor run -d "<org/name>" \
  --model "<model>" \
  --agent "<agent>" \
  --env langsmith \
  -n "<n-parallel-trials>" \
  --ek idle_ttl_seconds=0 \
  --ek delete_after_stop_seconds=7200
```

* **`idle_ttl_seconds`**: Stops an idle sandbox after this many seconds. Set `0` to disable the idle timeout.
* **`delete_after_stop_seconds`**: Deletes a stopped sandbox after this many seconds.

## Troubleshooting

* **The job fails to start with an authentication error**: Confirm `LANGSMITH_API_KEY` is set, or that `LANGSMITH_PROFILE` points to a configured profile.
* **The agent raises a `ValueError` for the model**: Pass `--model` in `provider:model` format, and install the matching `langchain-*` provider package so `init_chat_model()` can resolve it.

## See also

* [Evaluate Managed Deep Agents](../../../Build/Python/Managed%20Deep%20Agents/Agent%20capabilities/Evaluate%20Managed%20Deep%20Agents.md)
* [Deep Agents documentation](https://docs.langchain.com/oss/python/deepagents/overview.md)
* [Datasets & Experiments](../../Datasets%20%26%20Experiments/Datasets/Manage%20datasets.md)
* [Analyze an experiment](../../Datasets%20%26%20Experiments/Analyze%20experiment%20results/Analyze%20an%20experiment.md)
* [Sandbox snapshots](../../../Deploy/Sandboxes/Sandbox%20snapshots.md)
* [Harbor documentation](https://harborframework.com/docs)
