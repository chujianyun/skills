# Trace OpenCode sessions

> Capture OpenCode sessions, assistant turns, tool calls, and subagent activity in LangSmith.

The `@langchain/langsmith-opencode` plugin sends [OpenCode](https://opencode.ai/) session traces to LangSmith. Use it to inspect agent turns, model metadata, token usage, tool calls, tool errors, attachments, and subagent activity from your OpenCode workflows.

> [!NOTE]
>
> This integration uses a legacy destination setting such as `project_name` or `LANGSMITH_PROJECT`. [Create an agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md), choose its environment, and [retrieve that environment's `tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project). Use that returned value in the destination setting and any overrides. For integrations that support agent addressing, use the [agent identifier and environment](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) directly.

## Prerequisites

Before setting up tracing, ensure you have:

* [OpenCode](https://opencode.ai/) installed and configured.
* A [LangSmith API key](../../../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md).
* Access to configure the OpenCode `plugin` key in `opencode.json` or `~/.config/opencode/opencode.json`.

## Install and enable the plugin

Add the plugin to your OpenCode configuration file. You can configure it locally in `opencode.json` or globally in `~/.config/opencode/opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["@langchain/langsmith-opencode"]
}
```

Enable tracing and provide your LangSmith API key before starting OpenCode:

```bash
export TRACE_TO_LANGSMITH="true"
export LANGSMITH_API_KEY="<API_KEY>"
export LANGSMITH_PROJECT="<environment-tracer-session-name>"
```

Run OpenCode as usual. The plugin sends completed user turns to the configured agent environment.

## Configure tracing

Tracing is disabled by default. With `TRACE_TO_LANGSMITH=true` set, the plugin sends traces to LangSmith. You can also enable tracing with a LangSmith config file.

### Environment variables

The plugin reads OpenCode-specific variables first, then falls back to the generic LangSmith SDK variables when available.

| Variable | Required | Default | Description |
| - | - | - | - |
| `TRACE_TO_LANGSMITH` | Yes | `false` | Set to `"true"` to enable tracing. |
| `LANGSMITH_OPENCODE_API_KEY` | Conditional | - | LangSmith API key. Falls back to `LANGSMITH_API_KEY`. Required unless every replica provides its own API key. |
| `LANGSMITH_OPENCODE_ENDPOINT` | No | LangSmith SDK default | LangSmith API URL. Falls back to `LANGSMITH_ENDPOINT`. |
| `LANGSMITH_OPENCODE_PROJECT` | No | `opencode` | Selected agent environment's `tracer_session_name`. Falls back to `LANGSMITH_PROJECT`. |
| `LANGSMITH_OPENCODE_METADATA` | No | - | JSON object merged into root trace metadata. |
| `LANGSMITH_OPENCODE_RUNS_ENDPOINTS` | No | - | JSON array of replica destinations. |

For example:

```bash
export TRACE_TO_LANGSMITH="true"
export LANGSMITH_API_KEY="<API_KEY>"
export LANGSMITH_PROJECT="<environment-tracer-session-name>"
export LANGSMITH_OPENCODE_METADATA='{"team":"agents","environment":"dev"}'
```

### Config files

Use `.opencode/langsmith.json` for project-level settings or `~/.config/opencode/langsmith.json` for global defaults.

```json
{
  "enabled": true,
  "api_key": "<your-langsmith-api-key>",
  "api_url": "https://api.smith.langchain.com",
  "project": "<environment-tracer-session-name>",
  "metadata": {
    "team": "agents",
    "environment": "dev"
  }
}
```

| Field | Required | Default | Description |
| - | - | - | - |
| `enabled` | Yes | `false` | Set to `true` to enable tracing from the config file. |
| `api_key` | Conditional | - | LangSmith API key. Required unless provided by environment variable or replicas. |
| `api_url` | No | LangSmith SDK default | LangSmith API URL, usually `https://api.smith.langchain.com`. |
| `project` | No | `opencode` | Selected agent environment's `tracer_session_name`. |
| `metadata` | No | - | Object merged into root trace metadata. |
| `replicas` | No | - | Additional LangSmith destinations to replicate traces to. |

Keep config files that include API keys out of version control.

## Trace to multiple destinations

Set `replicas` in `langsmith.json` or `LANGSMITH_OPENCODE_RUNS_ENDPOINTS` to send the same trace data to additional agent environments or workspaces.

```json
{
  "enabled": true,
  "api_key": "<your-langsmith-api-key>",
  "project": "<environment-tracer-session-name>",
  "replicas": [
    {
      "api_url": "https://api.smith.langchain.com",
      "api_key": "<your-replica-langsmith-api-key>",
      "project": "<replica-tracer-session-name>",
      "updates": {
        "metadata": {
          "replica": true
        }
      }
    }
  ]
}
```

Replica objects support both snake\_case and LangSmith SDK-style camelCase field names. snake\_case is recommended in config files.

| Field | Description |
| - | - |
| `api_url` / `apiUrl` | LangSmith API URL for the replica destination. |
| `api_key` / `apiKey` | API key for the destination workspace. |
| `project` / `projectName` | Destination agent environment's `tracer_session_name`. |
| `updates` | Optional run fields to override on replicated runs, such as extra metadata. |

## What gets traced

The plugin listens to OpenCode chat and event hooks, aggregates each completed user turn, and submits it to LangSmith as a run tree.

* `opencode.session` root runs for completed user turns.
* `opencode.assistant.turn` child runs for assistant and model responses.
* Nested tool runs for tool calls, including inputs, outputs, errors, timing, and attachments when available.
* Subagent sessions nested under the parent tool call.
* Model name, provider, invocation parameters, token usage, and thread or session ID metadata.
* User messages, assistant messages, reasoning blocks, file parts, and system prompts associated with assistant turns.

Trace completion is based on OpenCode `step-finish` events. The plugin also flushes pending trace batches when the OpenCode server shuts down.

## View traces in LangSmith

Select the configured agent and environment in LangSmith, open **Tracing**, and look for root runs named `opencode.session`. Each trace contains the user turn as the root input and assistant responses, tool calls, and subagent traces as child runs. The plugin stores the OpenCode session ID as `thread_id` metadata, so you can filter or group related OpenCode turns in LangSmith.

## Troubleshooting

If traces do not appear in LangSmith:

* Confirm tracing is enabled with `TRACE_TO_LANGSMITH=true` or `"enabled": true` in config.
* Confirm the LangSmith API key is set in the same shell, project config, or global config used by OpenCode.
* Confirm the plugin package is installed where OpenCode can resolve it.
* Check that `LANGSMITH_OPENCODE_PROJECT` selects the intended environment's `tracer_session_name`.
* Restart OpenCode after changing `opencode.json`, `langsmith.json`, or environment variables.
* Make sure a user turn completes. The plugin does not send incomplete turns.
