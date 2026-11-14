# Log traces to an agent

> Configure an agent identifier and environment to send traces from your code to LangSmith.

Each trace belongs to an [agent](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md#agent) and one of its [environments](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20environments.md) within a workspace. Configure the agent identifier and environment in your code or environment variables. LangSmith uses them to route each trace to the selected environment.

> [!NOTE]
>
> Sending traces to an agent applies only to agent-based workspaces. It is supported in:
>
> * The Python SDK from `langsmith>=0.14.9`
> * The TypeScript SDK from `langsmith>=0.11.0`
> * The Go SDK from `github.com/langchain-ai/langsmith-go@v0.28.0`
> * The Java SDK from `com.langchain.smith:langsmith-java:0.1.0-beta.26`
>
> For integrations that require `project_name`, use the environment's [`tracer_session_name`](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value. For project-based workspaces, including self-hosted LangSmith, follow the [tracing quickstart](../../Tracing%20quickstart.md).

## Prerequisites

* **An agent-based workspace.** [Agent-based workspaces](../../../../LangSmith%20setup/Govern/Organization/Workspace%20setup/How%20agent-based%20workspaces%20differ.md) are available on [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md). They are not available on [self-hosted](../../../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) LangSmith. In an agent-based workspace, sending traces to an agent is already on, and you have no setting to change. To check which kind of workspace you have, look at the control at the top left. In an agent-based workspace, it names your workspace. In a project-based workspace, it shows the LangSmith logo, and sending traces to an agent is off.
* **An existing agent.** [Create the agent](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once in the target workspace before running the tracing examples. The examples use the identifier `checkout`. Replace it with your own.
* **An API key** from that workspace. See [create an API key](../../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md).
* **The SDK.** Sending traces to an agent needs `langsmith>=0.14.9` in Python, `langsmith@>=0.11.0` in TypeScript, v0.28.0 or later of `github.com/langchain-ai/langsmith-go` in Go, or 0.1.0-beta.26 or later of `com.langchain.smith:langsmith-java` in Java:

  ```bash uv
  uv add "langsmith>=0.14.9"
  ```

  ```bash pip
  pip install -U "langsmith>=0.14.9"
  ```

  ```bash npm
  npm install "langsmith@>=0.11.0"
  ```

  ```bash go
  go get github.com/langchain-ai/langsmith-go@v0.28.0
  ```

  ```kotlin Java/Kotlin (Gradle)
  implementation("com.langchain.smith:langsmith-java:0.1.0-beta.26")
  ```

## Send traces to an agent

Name the agent and the environment together, in code or as environment variables. An agent in code takes precedence over the variables. The SDK reads the variables only when nothing in code names a destination, and then it needs both.

* **Agent ID**: The agent's identifier, which the browser address bar carries and the **ID** field on the agent's Overview copies. It is not the display name. A [display name is a separate, editable value](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md#identifiers-and-display-names) that does not have to match the identifier, so read the identifier from the agent rather than deriving it from what the agent is called. For the rules an identifier must follow, see [Identifier rules](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#identifier-rules). Create the agent before using its identifier. An archived agent still holds its identifier, and LangSmith rejects a run sent to it with a `409`.
* **Environment**: The environment the run belongs to, and one of `local`, `development`, `staging`, or `production`. Environment names are not case-sensitive, and they map to the Local, Development, Staging, and Production labels in the UI. There is no default, because neither the agent nor the environment names a destination alone.

### Using environment variables

Set both variables:

```bash
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=<your-api-key>
export LANGSMITH_AGENT_ID=checkout
export LANGSMITH_AGENT_ENVIRONMENT=local
```

The first two are the usual tracing prerequisites rather than part of naming the agent. If only one of the two agent variables is set, the SDK logs a warning. Instead of picking an environment for you, it leaves untraced every call that names no destination in code, so nothing from those calls reaches LangSmith.

### Using code

Pass an agent address.

> [tab] Python
>
> Pass `ls.agent_address("checkout", "local")` as the `address` argument of [`@traceable`](https://reference.langchain.com/python/langsmith/run_helpers/traceable), or of [`tracing_context`](https://reference.langchain.com/python/langsmith/run_helpers/tracing_context) for everything traced inside a block:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import langsmith as ls
> from langsmith import traceable
>
>
> @traceable(address=ls.agent_address("checkout", "local"))
> def handle_order(order_id: str) -> dict:
>     return {"order_id": order_id, "status": "charged"}
> ```
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import langsmith as ls
> from langsmith import traceable, tracing_context
>
>
> @traceable
> def handle_order(order_id: str) -> dict:
>     return {"order_id": order_id, "status": "charged"}
>
>
> with tracing_context(address=ls.agent_address("checkout", "local")):
>     handle_order("A-1")
> ```

> [tab] TypeScript
>
> Pass `new AgentAddress("checkout", "local")` as `address` in the config of [`traceable`](https://reference.langchain.com/javascript/langsmith/traceable):
>
> ```ts theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { AgentAddress } from "langsmith";
> import { traceable } from "langsmith/traceable";
>
> const handleOrder = traceable(
>   async (orderId: string) => ({ orderId, status: "charged" }),
>   { name: "handle_order", address: new AgentAddress("checkout", "local") },
> );
> ```

> [tab] Java
>
> Pass `new AgentAddress("checkout", "local")` as `address` in the `TraceConfig` or `RunTree` builder:
>
> ```java Java theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import com.langchain.smith.address.AgentAddress;
> import com.langchain.smith.tracing.TraceConfig;
> import com.langchain.smith.tracing.Tracing;
> import java.util.Map;
> import java.util.function.Function;
>
> public class TraceAgentExample {
>   public static void main(String[] args) {
>     Function<String, Map<String, String>> handleOrder =
>         Tracing.traceFunction(
>             orderId -> Map.of("order_id", orderId, "status", "charged"),
>             TraceConfig.builder()
>                 .name("handle_order")
>                 .address(new AgentAddress("checkout", "local"))
>                 .build());
>
>     handleOrder.apply("A-1");
>   }
> }
> ```

> [tab] Go
>
> Create the address with `langsmith.NewAgentAddress("checkout", "local")`, which returns an error for an invalid value, and set it as `Address` on a `RunCreate`. `WithTracingAddress` sets it for every run of a standalone tracing client:
>
> ```go theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> package main
>
> import (
> 	"fmt"
> 	"time"
>
> 	"github.com/google/uuid"
> 	"github.com/langchain-ai/langsmith-go"
> )
>
> func main() {
> 	agent, err := langsmith.NewAgentAddress("checkout", "local")
> 	if err != nil {
> 		panic(err.Error())
> 	}
> 	client := langsmith.NewClient()
>
> 	id := uuid.New()
> 	start := time.Now().UTC()
> 	order := fmt.Sprintf("%s%06dZ%s", start.Format("20060102T150405"), start.Nanosecond()/1000, id)
>
> 	if err := client.CreateRun(&langsmith.RunCreate{
> 		ID:          id,
> 		TraceID:     id,
> 		Name:        "handle_order",
> 		RunType:     "chain",
> 		StartTime:   start,
> 		DottedOrder: order,
> 		Address:     agent,
> 		Inputs:      map[string]any{"order_id": "A-1"},
> 	}); err != nil {
> 		panic(err.Error())
> 	}
> 	if err := client.UpdateRun(&langsmith.RunUpdate{
> 		ID:          id,
> 		TraceID:     id,
> 		DottedOrder: order,
> 		EndTime:     time.Now().UTC(),
> 		Outputs:     map[string]any{"status": "charged"},
> 	}); err != nil {
> 		panic(err.Error())
> 	}
> 	client.Close()
> }
> ```

### Using OpenTelemetry

To send OTLP traces to an agent, set the `Langsmith-Agent-Id` and `Langsmith-Agent-Environment` headers instead of `Langsmith-Project`. With `langsmith>=0.14.9`, the Python SDK's OpenTelemetry exporter sets both headers from the agent variables when `OTEL_EXPORTER_OTLP_HEADERS` is unset. For the header rules and the errors LangSmith returns, see [Trace with OpenTelemetry](../../Tracing%20setup/Integrations/Agent%20frameworks/Trace%20with%20OpenTelemetry.md#trace-a-non-langchain-application).

## Send your first trace

Run your agent so it sends at least one trace. In LangSmith, select the agent in the top bar, go to **Tracing**, and set the environment control to the one you sent the trace to. The trace appears there.

## Query an agent environment

To query traces, [resolve the agent identifier and environment](../../../Debug/Viewing%20%26%20managing%20traces/Resolve%20an%20agent%20environment.md) to a `session_id`. Pass that value to query APIs that require `project_id` or `project_ids`.

## Remove conflicting destination settings

Do not combine agent addressing with legacy destination settings. The SDK handles conflicting settings as follows:

* **Agent variables and legacy variables together**: Not allowed. If you set the agent variables and also `LANGSMITH_PROJECT`, `LANGCHAIN_PROJECT`, or `LANGCHAIN_SESSION`, the trace has two destinations, and the SDK does not pick one. It logs a warning when the client starts, and it does not trace a call unless code names the destination. If you pass both `address` and `project_name` in one call, the SDK raises an error and sends nothing: `LangSmithUserError` from `@traceable` or `tracing_context()` in Python, or an `Error` from `traceable` in TypeScript. LangSmith also rejects an ingestion request that supplies both address types.
* **A `project_name` override in code**: Overrides the agent variables. Passing `project_name` to `@traceable` or `tracing_context()` in Python, or in the `traceable` config in TypeScript, traces the run to the override destination and ignores the agent variables, without an error. This is what lets an [evaluation](../../../../Test/Get%20started/LangSmith%20Evaluation.md) use its own experiment destination while the agent variables stay set for the rest of the process.

## Troubleshooting

If tracing reports that the agent does not exist, check the workspace and identifier. [Register the agent](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) with the UI or a setup credential, then retry.

On self-hosted LangSmith, where agent-based workspaces are not available, LangSmith rejects runs sent to an agent with a `403` and the message `agent addressing is not enabled for this workspace`. It rejects the whole request that carries them, so it records none of the runs in that request. See [Prerequisites](#prerequisites).

## See also

* [Agent Registry](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md)
* [Agent environments](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20environments.md)
* [Configure legacy integrations](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project)
* [Resolve an agent environment](../../../Debug/Viewing%20%26%20managing%20traces/Resolve%20an%20agent%20environment.md)
* [Trace with OpenTelemetry](../../Tracing%20setup/Integrations/Agent%20frameworks/Trace%20with%20OpenTelemetry.md)
* [Observability concepts](../../Observability%20concepts.md)
