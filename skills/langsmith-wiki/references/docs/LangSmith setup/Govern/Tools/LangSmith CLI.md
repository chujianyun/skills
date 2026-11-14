# LangSmith CLI

> Query and manage agent traces, runs, datasets, evaluators, experiments, insights, and threads from the terminal

The LangSmith CLI is a command-line tool for querying and managing your LangSmith data. It's designed for both developers and AI coding agents and outputs human-readable tables by default, with a `--format json` option for scripting. Use it when you need scriptable access to your LangSmith data, such as bulk exports, automation, or giving a coding agent direct access to your [traces, runs, and datasets](../../../Monitor/Trace/Observability%20concepts.md).

## Install

```bash macOS / Linux (recommended)
curl -fsSL https://cli.langsmith.com/install.sh | sh
```

```powershell Windows
irm https://cli.langsmith.com/install.ps1 | iex
```

```bash Homebrew
brew install langchain-ai/tap/langsmith-cli
```

```powershell Scoop
scoop install langsmith-cli
```

```bash GitHub Releases
# Download the latest binary for your platform:
# https://github.com/langchain-ai/langsmith-cli/releases
```

```bash Go install
go install github.com/langchain-ai/langsmith-cli/cmd/langsmith@latest
```

To upgrade at any time:

```bash
langsmith self-update
```

Use the `--dry-run` flag to preview the update without installing.

> [!NOTE]
>
> Querying a [SmithDB](../../../Monitor/Reference/SmithDB%20API%20migration/Migrate%20to%20SmithDB-backed%20APIs.md)-backed deployment requires LangSmith CLI `v0.2.44` or later.

## Authenticate

The CLI selects an agent environment through `--project` or `LANGSMITH_PROJECT`. [Retrieve that environment's `tracer_session_name`](../../Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) and use it for these options. Commands named `project` operate on the [backing trace storage](../../../Monitor/Trace/Observability%20concepts.md#agents-and-environments).

`langsmith auth login` requires LangSmith CLI `v0.2.30` or later. `langsmith profile` commands require LangSmith CLI `v0.2.26` or later.

The recommended local setup is to authenticate with OAuth:

> [!NOTE]
>
> `langsmith auth login` also works against self-hosted instances from LangSmith CLI `v0.2.46` and newer, provided the deployment is on LangSmith `0.16` or later with the OAuth authorization server enabled (requires a signing JWKS to be configured). See [Self-hosted instances](#self-hosted-instances). On earlier deployments, or without a signing JWKS, authenticate with an API key or create an API-key profile.

```bash
langsmith auth login
```

This opens a browser-based authorization flow and stores OAuth tokens in `~/.langsmith/config.json` under the selected [profile](../../Account/Profile%20configuration.md). Select a profile with `--profile` or `LANGSMITH_PROFILE`:

```bash
langsmith auth login --profile dev
langsmith --profile dev project list
```

In headless environments, pass `--no-browser` and open the printed URL manually:

```bash
langsmith auth login --no-browser --workspace-id <workspace-id>
```

To manage saved profiles:

```bash
langsmith profile list
langsmith profile create dev --workspace-id <workspace-id> --set-current
langsmith profile use dev
langsmith profile set-workspace <workspace-id>
```

For the full profile configuration reference, see [Profile configuration](../../Account/Profile%20configuration.md).

You can also authenticate with an API key directly.

Set your [API key](../../Account/Create%20an%20account%20and%20API%20key.md) as an environment variable:

```bash
export LANGSMITH_API_KEY="lsv2_..."
```

Optionally, set the agent environment to query by default using its `tracer_session_name`:

```bash
export LANGSMITH_PROJECT="<environment-tracer-session-name>"
```

If you're using LangSmith [self-hosted](../../Self-hosted/Self-hosted%20LangSmith.md), also set the endpoint:

```bash
export LANGSMITH_ENDPOINT="https://your-langsmith-instance.com"
```

Or, pass them as flags per command:

```bash
langsmith --api-key lsv2_... trace list --project "<environment-tracer-session-name>"
```

### Self-hosted instances

Point the CLI at your instance with `--api-url`, or with `LANGSMITH_ENDPOINT`. Both the browser-based login and API keys are supported.

> [tab] OAuth
>
> Requires LangSmith CLI `v0.2.46` or later and a deployment on LangSmith `0.16` or later, with the OAuth authorization server enabled. The chart exposes the OAuth authorization server under `/api`, but those endpoints stay inert until you [configure a signing JWKS](../../Self-hosted/Install%20an%20instance/Self-host%20LangSmith%20on%20Kubernetes.md#configure-a-signing-jwks).
>
> The OAuth authorization server is enabled automatically when `config.hostname` is set in your Helm chart **and** a signing JWKS is configured (via `config.signingJwks`, or the key `langsmith_signing_jwks` in `config.existingSecretName`). Without the signing JWKS, the OAuth endpoints are inactive and the CLI will receive a `404` — use the API key tab instead.
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> langsmith auth login --api-url https://langsmith.example.com --profile self-hosted
> ```
>
> Pass your instance's base URL. The CLI reads the deployment's authorization server metadata to find the OAuth endpoints, so `https://langsmith.example.com` and `https://langsmith.example.com/api` both work.
>
> Tokens are stored under the named profile, so later commands only need `--profile`:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> langsmith --profile self-hosted project list
> ```

> [tab] API key
>
> Works on every LangSmith version.
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> export LANGSMITH_ENDPOINT="https://langsmith.example.com"
> export LANGSMITH_API_KEY="lsv2_..."
>
> langsmith project list
> ```
>
> To save the endpoint and key as a reusable profile instead:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> LANGSMITH_API_KEY="lsv2_..." langsmith profile create self-hosted \
>   --api-url https://langsmith.example.com --set-current
> ```

> [!WARNING]
>
> `LANGSMITH_ENDPOINT` takes precedence over a profile's `api_url`. If it is set in your shell, every profile you select resolves to that endpoint — a common cause of commands unexpectedly reaching LangSmith Cloud while a self-hosted profile is active. Unset it when working with profiles, or pass `--api-url` explicitly.

## Quickstart

The following commands cover the core resource types:

```bash
# List tracing projects
langsmith project list

# List recent traces in a project
langsmith trace list --project "<environment-tracer-session-name>" --limit 5

# Get a specific trace with full detail
langsmith trace get <trace-id> --project "<environment-tracer-session-name>" --full

# List LLM runs with token counts
langsmith run list --project "<environment-tracer-session-name>" --run-type llm --include-metadata

# Datasets and experiments
langsmith dataset list
langsmith experiment list --dataset my-eval-set

# Conversation threads
langsmith thread list --project "<environment-tracer-session-name>"

# Sandboxes
langsmith sandbox list
langsmith sandbox tunnel my-vm --remote-port 5432
```

## Search with AI

[AI search](../../../Monitor/Debug/Viewing%20%26%20managing%20traces/Filter%20traces.md#search-with-ai) finds runs, traces, and threads by a natural-language description of their conversations. Use `--ai-search` on the streaming query commands to search from the terminal.

> [!NOTE]
>
> These commands require LangSmith CLI v0.3.9 or later and an organization admin to [enable AI search](../../../Monitor/Debug/Viewing%20%26%20managing%20traces/Filter%20traces.md#enable-ai-search). The same data-handling and PHI restrictions apply as in the UI. For release stage and availability, see [Search with AI](../../../Monitor/Debug/Viewing%20%26%20managing%20traces/Filter%20traces.md#search-with-ai). The commands require `--project-id` and do not resolve `--project` names.

```bash
langsmith threads streaming query --project-id <project-id> --ai-search "user asks for a refund"
langsmith traces streaming query --project-id <project-id> --ai-search "tool call failed"
langsmith runs streaming query-v2 --project-id <project-id> --ai-search "tool call failed" --max-items 20
```

Each server-sent event prints as a JSON patch, and `--max-items` counts events, not matched runs, traces, or threads.

Pass a nonempty description of at most 2,000 UTF-8 bytes. To combine the description with structured conditions using `AND`, add `--filter` for runs and threads, or `--trace-filter` and `--tree-filter` for traces.

The non-streaming `traces query` and `threads query` commands also accept `--ai-search`, but the server rejects those requests with HTTP `406` because AI search requires streaming. Ordinary list commands do not support AI search.

## Output formats

**Default**

Human-readable tables:

```bash
langsmith trace list --project "<environment-tracer-session-name>"
```

**JSON**

`--format json` to pipe, script, or feed output to an agent:

```bash
langsmith --format json trace list --project "<environment-tracer-session-name>"
```

**Write to file**

`-o <path>`:

```bash
langsmith trace list --project "<environment-tracer-session-name>" -o traces.json
```

## Commands

Each command group targets a specific LangSmith resource. Most commands support `--limit`, `--offset`, and a shared set of [filter flags](#filter-flags).

### List trace-storage destinations

The legacy `project list` command lists the backing trace-storage destinations, including those associated with agent environments. It returns up to 20 by default, sorted by most recent activity. Use [`experiment list`](#view-experiments) to list evaluation experiments.

```bash
langsmith project list
langsmith project list --limit 50 --name-contains chatbot
langsmith --format json project list
```

### Query traces

Defaults to the last 7 days, newest first. Use `--since` or `--last-n-minutes` to change the time window.

```bash
langsmith trace list --project "<environment-tracer-session-name>" --limit 50 --last-n-minutes 60
langsmith trace list --project "<environment-tracer-session-name>" --error                     # errors only
langsmith trace list --project "<environment-tracer-session-name>" --min-latency 5             # slow traces (>5s)
langsmith trace list --project "<environment-tracer-session-name>" --tags production           # filter by tag
langsmith trace list --project "<environment-tracer-session-name>" --full                      # all fields
langsmith trace list --project "<environment-tracer-session-name>" --show-hierarchy --limit 3  # include full run tree
langsmith trace get <trace-id> --project "<environment-tracer-session-name>" --full
langsmith trace export ./traces --project "<environment-tracer-session-name>" --limit 20 --full
```

### Query runs

Defaults to 50 results (most other commands default to 20). The same 7-day time window applies. Use `--since` or `--last-n-minutes` to override.

```bash
langsmith run list --project "<environment-tracer-session-name>" --run-type llm
langsmith run list --project "<environment-tracer-session-name>" --run-type tool --name search
langsmith run list --project "<environment-tracer-session-name>" --min-tokens 1000 --include-metadata
langsmith run get <run-id> --full
langsmith run export llm_calls.jsonl --project "<environment-tracer-session-name>" --run-type llm --full
```

### Query threads

`--project` is required for all thread commands.

```bash
langsmith thread list --project "<environment-tracer-session-name>" --last-n-minutes 120
langsmith thread get <thread-id> --project "<environment-tracer-session-name>" --full
```

### Manage datasets

`dataset export` exports the examples (rows) within a dataset, not the dataset metadata itself.

```bash
langsmith dataset list
langsmith dataset list --name-contains eval
langsmith dataset get my-dataset
langsmith dataset create --name my-eval-set --description "QA pairs for v2"
langsmith dataset delete my-old-dataset --yes
langsmith dataset export my-dataset ./data.json --limit 500
langsmith dataset upload data.json --name new-dataset
```

### Manage examples

Use `--split` to assign examples to named splits (such as `test` or `train`) when creating or listing.

```bash
langsmith example list --dataset my-dataset --limit 50
langsmith example list --dataset my-dataset --split test
langsmith example create --dataset my-dataset \
  --inputs '{"question": "What is LangSmith?"}' \
  --outputs '{"answer": "A platform for LLM observability"}' \
  --split test
langsmith example delete <example-id> --yes
```

### Manage evaluators

Evaluators can be offline (run against a dataset during experiments) or online (run against an agent environment). Use `--sampling-rate` to evaluate only a fraction of production runs, and `--replace` to overwrite an existing evaluator by name.

```bash
langsmith evaluator list
langsmith evaluator upload evals.py --name accuracy \
  --function check_accuracy --dataset my-eval-set
langsmith evaluator upload evals.py --name latency-check \
  --function check_latency --project "<environment-tracer-session-name>" --sampling-rate 0.5
langsmith evaluator upload evals.py --name accuracy \
  --function check_accuracy_v2 --dataset my-eval-set --replace --yes
langsmith evaluator delete accuracy --yes
```

### View experiments

`experiment list` shows evaluation experiments. Use [`project list`](#list-projects) for the trace-storage destinations associated with agent environments.

```bash
langsmith experiment list
langsmith experiment list --dataset my-eval-set
langsmith experiment get my-experiment-2024-01-15
```

### Manage insights

`insights` commands create, run, and read [Insights](../../../Monitor/Observe/Monitoring%20%26%20alerting/Discover%20errors%20and%20usage%20patterns%20with%20Insights.md) reports, which group an agent environment's traces into categories to surface usage patterns and failure modes. Every `insights` command needs `--project`, `--project-id`, or the `LANGSMITH_PROJECT` environment variable.

> [!NOTE]
>
> `insights create`, `insights run`, and `insights config` require LangSmith CLI v0.2.60 or later.

To create a report, define it in a JSON file:

```json
{
  "name": "Weekly reliability review",
  "summary_prompt": "Identify the request and outcome: {{run.inputs}} {{run.outputs}}",
  "last_n_hours": 168,
  "filter": "eq(is_root, true)",
  "model": "openai",
  "schedule_cron": "0 9 * * 1"
}
```

* **`name`** and **`summary_prompt`**: Required. The [summary prompt](../../../Monitor/Observe/Monitoring%20%26%20alerting/Discover%20errors%20and%20usage%20patterns%20with%20Insights.md#summary-prompt) is a Mustache template and must reference at least one of `{{run.inputs}}`, `{{run.outputs}}`, `{{run.error}}`, `{{run.feedback}}`, or `{{all_thread_messages}}`. The CLI does not support auto mode, so state what the report should look for in this prompt.
* **`last_n_hours`**, or **`start_time`** and **`end_time`**: The time range to sample traces from. Use one form, not both.
* **`model`**: `openai` (default) or `anthropic`. To pick specific models, set **`cluster_model`** and **`summary_model`** together, each to `openai`, `anthropic`, or a [model configuration](../Organization/Workspace%20setup/Manage%20model%20configurations.md) UUID. Display names are not accepted.
* **`schedule_cron`**: A cron expression for a recurring report. The first job starts immediately, and later jobs follow the schedule. Omit it for a one-time report.

The file also accepts `filter`, `sample`, `hierarchy`, `partitions`, `attribute_schemas`, and `description`. Unknown fields cause an error.

`insights create` saves the file as a job configuration and starts the first report. Reports run asynchronously and incur model costs. The workspace needs secrets for the selected models. Pass `--wait` to poll until the report succeeds or fails, for up to 30 minutes. Pass `--config -` to read the file from stdin.

```bash
langsmith insights create --project "<environment-tracer-session-name>" --config insights.json
langsmith insights create --project "<environment-tracer-session-name>" --config insights.json --wait
```

`insights run` starts a new report from a saved configuration without changing the configuration or its schedule:

```bash
langsmith insights config list --project "<environment-tracer-session-name>"
langsmith insights config list --project "<environment-tracer-session-name>" --include-prebuilt
langsmith insights run <config-id> --project "<environment-tracer-session-name>" --wait
```

`insights list` returns reports with their status and category counts. `insights get` adds the executive summary, highlighted traces, and per-category statistics:

```bash
langsmith insights list --project "<environment-tracer-session-name>" --limit 5
langsmith insights get <insight-id> --project "<environment-tracer-session-name>"
```

`insights config update` replaces a configuration's name and analysis settings from a JSON file in the same format. It does not start a report. Omit `description` or `schedule_cron` to keep the current value, or set `schedule_cron` to `null` to stop the schedule. `insights config delete` removes the configuration and every report it produced.

```bash
langsmith insights config update <config-id> --project "<environment-tracer-session-name>" --config insights.json
langsmith insights config delete <config-id> --project "<environment-tracer-session-name>" --yes
```

### Manage sandboxes

Sandbox commands let you build snapshots, create sandboxes, execute commands, open interactive consoles, and tunnel TCP ports to services running inside sandboxes.

See [Sandbox CLI](../../../Deploy/Sandboxes/Sandbox%20CLI.md) for the full sandbox command reference.

### Manage custom apps

`langsmith apps` commands scaffold, run locally, and publish [custom apps](../../../Monitor/Observe/Monitoring%20%26%20alerting/Custom%20Apps.md), UIs that run inside LangSmith and call the LangSmith API.

See [CLI reference](../../../Monitor/Observe/Monitoring%20%26%20alerting/Custom%20Apps.md#cli-reference) for the full command list.

### Call the LangSmith API directly

The `api` command is an authenticated, scriptable wrapper around the raw LangSmith REST API — useful for endpoints the typed commands above don't cover, or for piping JSON into and out of shell scripts. It's modeled after `gh api` and `curl`: pass the path as the only positional argument, and use `-X` to set the HTTP method (defaults to `GET`). Auth headers (`x-api-key`, `x-tenant-id`) are injected automatically.

```bash
# GET (default method) — query string supported in the path
langsmith api sessions?limit=5

# Discover endpoints from the OpenAPI spec
langsmith api ls --tag datasets
langsmith api info GET sessions

# Typed JSON fields with -F (numbers, booleans, null, objects, arrays parsed as JSON)
# Method auto-promotes to POST when -F/-f/--input/--body is supplied
langsmith api runs/query -F session_id=abc -F limit=10

# String-typed fields with -f (always sent as a JSON string, even if numeric)
langsmith api datasets -f name=my-dataset -f description="QA pairs"

# Other HTTP methods via -X
langsmith api sessions/abc-123 -X DELETE

# Send a request body from a file or stdin
langsmith api datasets --input create-dataset.json
echo '{"name":"test"}' | langsmith api sessions --input -

# Force GET with fields — fields go to the query string instead of a body
langsmith api runs -X GET -F limit=5 -F session=abc

# Inspect response status + headers
langsmith api sessions --include

# Add custom headers
langsmith api sessions -H "Accept: text/csv"
```

Key flags:

| Flag | Short | Default | Description |
| - | - | - | - |
| `--method` | `-X` | `GET` | HTTP method |
| `--field` | `-F` | — | Typed JSON field as `key=value`. Repeatable. Use `@<path>` or `@-` for file/stdin values. |
| `--raw-field` | `-f` | — | String JSON field as `key=value`. Repeatable. |
| `--input` | — | — | File to use as the request body (`-` for stdin) |
| `--body` | — | — | Raw request body (JSON string, `@file`, or `@-` for stdin) |
| `--header` | `-H` | — | Additional headers as `Key:Value`. Repeatable. |
| `--include` | `-i` | `false` | Print response status line and headers before body |

`--input` and `--body` are mutually exclusive. Subcommands `langsmith api ls` and `langsmith api info` browse and describe endpoints from the cached OpenAPI spec — pass `--refresh` to re-fetch.

## Filter flags

Most `trace` and `run` commands share these filters:

| Flag | Description | Example |
| - | - | - |
| `--project` | Agent environment's `tracer_session_name` | `--project "<environment-tracer-session-name>"` |
| `--limit, -n` | Max results | `-n 10` |
| `--offset` | Pagination offset | `--offset 20` |
| `--last-n-minutes` | Override the 7-day default | `--last-n-minutes 60` |
| `--since` | After ISO timestamp | `--since 2024-01-15T00:00:00Z` |
| `--error` / `--no-error` | Filter by error status | `--error` |
| `--name` | Name search (case-insensitive) | `--name ChatOpenAI` |
| `--run-type` | Run type (`llm` or `tool`) | `--run-type llm` |
| `--min-latency` / `--max-latency` | Latency range in seconds | `--min-latency 2.5` |
| `--min-tokens` | Minimum total tokens | `--min-tokens 1000` |
| `--tags` | Tags, comma-separated (OR logic) | `--tags prod,v2` |
| `--filter` | Raw LangSmith filter DSL | `--filter 'eq(status, "error")'` |
| `--trace-ids` | Specific trace IDs | `--trace-ids abc123,def456` |

**Detail flags** — control which fields are included in the response:

| Flag | Adds |
| - | - |
| `--include-metadata` | Status, duration, tokens, costs |
| `--include-io` | Inputs, outputs, error |
| `--include-feedback` | Feedback stats |
| `--full` | All of the above |
| `--show-hierarchy` | Full run tree (traces only) |
