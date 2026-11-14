# Trace Pi coding agent sessions

> Trace Pi coding agent invocations to LangSmith to observe turns, debug tool calls, track token usage, and inspect individual LLM invocations.

This guide shows you how to trace [Pi coding agent](https://pi.dev) sessions to LangSmith using the `@langchain/langsmith-pi-extension` extension.

Once configured, each Pi session sends traces to LangSmith. Each trace includes user messages, assistant responses, tool calls, and individual LLM invocations, which gives you full observability into your Pi coding agent runs.

> [!NOTE]
>
> This integration uses a legacy destination setting such as `project_name` or `LANGSMITH_PROJECT`. [Create an agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md), choose its environment, and [retrieve that environment's `tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project). Use that returned value in the destination setting and any overrides. For integrations that support agent addressing, use the [agent identifier and environment](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) directly.

## Prerequisites

Before setting up tracing, ensure you have:

* [**Pi**](https://pi.dev) installed.
* A [**LangSmith API key**](../../../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md).

## Installation

Install the extension via Pi:

```sh
pi install npm:@langchain/langsmith-pi-extension
```

## Quick start

Tracing is disabled by default. Set the following environment variables to enable tracing and connect to your LangSmith account:

```sh
export TRACE_TO_LANGSMITH=true
export LANGSMITH_PI_API_KEY="<API_KEY>"
```

[Run Pi](https://pi.dev/docs/latest/quickstart) as usual. When a session starts, the extension reports whether LangSmith tracing is enabled. You can also check the current tracing state at any time from within Pi:

```text
/langsmith-tracing
```

Set `LANGSMITH_PI_PROJECT` to the selected agent environment's `tracer_session_name` before sending traces.

## Configuration

Configuration can come from environment variables or JSON config files. Values are merged in the following order, with later sources taking precedence:

1. Defaults
2. `~/.pi/langsmith.json` (global config)
3. `<current-working-directory>/.pi/langsmith.json` (project config)
4. Environment variables

### Environment variables

| Variable | Description |
| - | - |
| `TRACE_TO_LANGSMITH` | Enables tracing when set to `true`, `1`, `yes`, or `on`. Disables tracing when set to `false`, `0`, `no`, or `off`. |
| `LANGSMITH_PI_API_KEY` | LangSmith API key. Falls back to `LANGSMITH_API_KEY`. |
| `LANGSMITH_PI_ENDPOINT` | LangSmith API URL for self-hosted or custom deployments. Falls back to `LANGSMITH_ENDPOINT`. |
| `LANGSMITH_PI_PROJECT` | Selected agent environment's `tracer_session_name`. Falls back to `LANGSMITH_PROJECT`. Defaults to `pi-coding-agent`. |
| `LANGSMITH_PI_METADATA` | JSON object added to the root run metadata. Falls back to `LANGSMITH_METADATA`. |
| `LANGSMITH_PI_RUNS_ENDPOINTS` | JSON array of replica run destinations. Falls back to `LANGSMITH_RUNS_ENDPOINTS`. |

Example:

```sh
export TRACE_TO_LANGSMITH=true
export LANGSMITH_PI_API_KEY="<API_KEY>"
export LANGSMITH_PI_PROJECT="<environment-tracer-session-name>"
export LANGSMITH_PI_METADATA='{"team":"infra","environment":"local"}'
```

### Config file

Create `~/.pi/langsmith.json` for global settings or `.pi/langsmith.json` in a project directory for local overrides:

```json
{
  "enabled": true,
  "api_key": "<your-langsmith-api-key>",
  "api_url": "https://api.smith.langchain.com",
  "project": "<environment-tracer-session-name>",
  "metadata": { "environment": "local" }
}
```

Config file fields:

| Field | Required | Default | Description |
| - | - | - | - |
| `enabled` | Yes | `false` | Set to `true` to enable tracing from the config file. |
| `api_key` | No\* | — | LangSmith API key. Required unless provided by environment variable or replicas. |
| `api_url` | No | LangSmith SDK default | LangSmith API URL, usually `https://api.smith.langchain.com`. |
| `project` | No | `pi-coding-agent` | Selected agent environment's `tracer_session_name`. |
| `metadata` | No | — | Object merged into root trace metadata. |
| `replicas` | No | — | Array of additional LangSmith destinations to replicate traces to. |

## Replicas

Use `replicas` to send traces to multiple LangSmith destinations simultaneously. This is useful for forwarding traces to both a personal workspace and a shared team workspace, or to a [self-hosted LangSmith](../../../../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) instance alongside the [cloud](../../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md).

```json
{
  "enabled": true,
  "api_key": "<primary-api-key>",
  "project": "<environment-tracer-session-name>",
  "replicas": [
    {
      "api_key": "<replica-api-key>",
      "api_url": "https://replica-langsmith.example.com",
      "project": "<replica-tracer-session-name>",
      "updates": {
        "tags": ["replica"]
      }
    }
  ]
}
```

Each replica entry can include an `updates` object to override metadata or tags on the replicated runs.
