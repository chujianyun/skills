# Trace Visual Studio Code Copilot Chat sessions

> Capture VS Code Copilot Chat agent interactions, LLM calls, tool executions, and token usage in LangSmith via OpenTelemetry.

[Visual Studio Code Copilot Chat](https://code.visualstudio.com/docs/copilot/overview) can export traces over [OpenTelemetry](https://opentelemetry.io/) (OTel). LangSmith ingests OTLP directly, so you can point Copilot Chat at LangSmith and inspect agent turns, model metadata, tool calls, and token usage alongside the rest of your LLM traces.

This guide is based on Copilot's [Monitor agent usage with OpenTelemetry](https://code.visualstudio.com/docs/copilot/guides/monitoring-agents) reference.

> [!NOTE]
>
> In an [agent-based workspace](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

## Prerequisites

Before setting up tracing, ensure you have:

* A recent version of [Visual Studio Code](https://code.visualstudio.com/) with GitHub Copilot Chat installed and signed in.
* A [LangSmith API key](../../../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md).

## Choose your harness

Since [VS Code 1.143](https://code.visualstudio.com/updates/v1_143), Copilot runs on the new Copilot harness by default and you can still switch back to the older Local harness from the harness picker. Each one takes its own endpoint and settings. Only the Local harness sends [Git information](#trace-metadata) so use it if you want your traces tagged with the repo and branch.

## Configure tracing

Copilot Chat enables OTel emission when any of `COPILOT_OTEL_ENABLED`, `OTEL_EXPORTER_OTLP_ENDPOINT`, or the `github.copilot.chat.otel.enabled` setting (Local harness) is set. The simplest way to send Copilot Chat traces to LangSmith is to export the following environment variables before launching VS Code:

```bash
export COPILOT_OTEL_ENABLED=true
export COPILOT_OTEL_PROTOCOL=http
export COPILOT_OTEL_ENDPOINT=https://api.smith.langchain.com/otel/v1/traces
export COPILOT_OTEL_CAPTURE_CONTENT=true
export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true
export OTEL_EXPORTER_OTLP_HEADERS="x-api-key=<your_langsmith_api_key>,Langsmith-Agent-Id=<your-agent-id>,Langsmith-Agent-Environment=local"
```

| Variable | Description |
| - | - |
| `COPILOT_OTEL_ENABLED` | Set to `true` to enable Copilot Chat OTel export. |
| `COPILOT_OTEL_PROTOCOL` | OTLP protocol. Use `http` to target LangSmith's HTTP OTLP ingestion endpoint. |
| `COPILOT_OTEL_ENDPOINT` | LangSmith OTLP endpoint. On the Local harness it takes precedence over `OTEL_EXPORTER_OTLP_ENDPOINT`, and on the Copilot harness it's used only when that variable is unset. |
| `COPILOT_OTEL_CAPTURE_CONTENT` | Capture full prompts, responses, tool arguments, and tool results on spans on the Local harness. Off by default. |
| `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` | The same content capture on the Copilot harness. Off by default. |
| `OTEL_EXPORTER_OTLP_HEADERS` | Authentication headers for the OTLP exporter. Use `x-api-key=<your_langsmith_api_key>` and `Langsmith-Agent-Id=<your-agent-id>,Langsmith-Agent-Environment=local` to route traces to the registered [agent and environment](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md). |

This endpoint is for the Copilot harness, which sends to the URL exactly as written. The Local harness adds `/v1/traces` on its own so use `https://api.smith.langchain.com/otel` there instead.

VS Code must inherit these environment variables, so export them in the shell session that launches VS Code (for example, by adding them to `~/.zshrc`, `~/.bashrc`, or a shell profile) before starting the editor.

Set the endpoint to your LangSmith API URL (`LANGSMITH_ENDPOINT`) plus `/otel` on the Local harness, or plus `/otel/v1/traces` on the Copilot harness. For the URL on each deployment type, see [Find your OTLP endpoint](../Agent%20frameworks/Trace%20with%20OpenTelemetry.md#find-your-otlp-endpoint).

> [!WARNING]
>
> Content capture records full prompt and response content, system prompts, tool schemas, tool arguments, and tool results. Only enable it in trusted environments where capturing source code, file contents, and user prompts is acceptable.

### Alternative: VS Code settings

If you prefer not to set environment variables, you can enable OTel from VS Code settings instead. Open **Settings** (`⌘,` / `Ctrl+,`), search for `copilot otel`, and configure these for the Local harness:

```json
{
  "github.copilot.chat.otel.enabled": true,
  "github.copilot.chat.otel.exporterType": "otlp-http",
  "github.copilot.chat.otel.otlpEndpoint": "https://api.smith.langchain.com/otel",
  "github.copilot.chat.otel.captureContent": true
}
```

The Copilot harness reads its own settings instead: `chat.agentHost.otel.enabled`, `chat.agentHost.otel.otlpEndpoint` (set to `https://api.smith.langchain.com/otel/v1/traces`), and `chat.agentHost.otel.captureContent`, as listed in VS Code's [Agent Host OTel reference](https://github.com/microsoft/vscode/blob/main/src/vs/platform/agentHost/OTEL.md).

Authentication headers must still be provided through the `OTEL_EXPORTER_OTLP_HEADERS` environment variable—VS Code settings do not expose a header field. On the Local harness, environment variables also take precedence over VS Code settings when both are set.

## View traces in LangSmith

Start a Copilot Chat session and send a request. In [LangSmith](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-trace-with-vscode-copilot), select your agent and environment, then open **Tracing**. Each agent interaction produces a hierarchical span tree following the [OTel GenAI Semantic Conventions](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/):

* `invoke_agent` spans wrap the full agent orchestration, including agent name, conversation ID, turn count, and total token usage.
* `chat` spans capture individual LLM API calls with model, token counts, response time, and finish reason.
* `execute_tool` spans capture tool invocations with tool name, type, duration, and success status.

When an agent invokes a subagent, Copilot Chat propagates trace context automatically, so the subagent's `invoke_agent` span appears as a child of the parent's `execute_tool` span in LangSmith.

### Trace metadata

LangSmith adds the same [coding agent metadata](Coding%20agent%20metadata%20contract.md) that the Claude Code, Codex, and Cursor plugins send, so Copilot traces work with the same filters and charts. Each conversation is grouped into one thread, and `ls_integration` is set to `copilot`.

On the Local harness, the top-level run includes the branch and commit of the open folder, plus the repo details when it has a remote. You don't need to turn anything on for this. The Copilot harness doesn't send Git information so those fields won't appear on its traces.

## Troubleshooting

* **No traces appear in LangSmith.** Confirm `COPILOT_OTEL_ENABLED=true` and that VS Code was launched from the shell where the variables are exported. Verify `OTEL_EXPORTER_OTLP_HEADERS` includes `x-api-key=<your_langsmith_api_key>` and that the API key belongs to the workspace you want to trace into. Restart VS Code after changing environment variables.
* **Traces land in the wrong environment.** Set `Langsmith-Agent-Id=<your-agent-id>,Langsmith-Agent-Environment=local` in `OTEL_EXPORTER_OTLP_HEADERS`. Use the registered agent ID and the intended environment. Remove `Langsmith-Project` when using agent headers.
* **No traces from the Copilot harness.** Its endpoint must end in `/otel/v1/traces`, since it doesn't add the path itself.
* **Prompts and responses are missing.** Content capture is opt-in. On the Local harness, set `COPILOT_OTEL_CAPTURE_CONTENT=true` (or enable `github.copilot.chat.otel.captureContent`), and on the Copilot harness set `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true` (or enable `chat.agentHost.otel.captureContent`).

## Related resources

* [VS Code Copilot: Monitor agent usage with OpenTelemetry](https://code.visualstudio.com/docs/copilot/guides/monitoring-agents)
* [Trace with OpenTelemetry](../Agent%20frameworks/Trace%20with%20OpenTelemetry.md)
* [Configure legacy integrations](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project)
