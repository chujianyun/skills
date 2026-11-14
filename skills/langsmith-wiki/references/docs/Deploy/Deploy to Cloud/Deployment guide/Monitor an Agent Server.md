# Monitor an Agent Server

> View build logs, server logs, and metrics for an Agent Server on LangSmith Cloud.

Monitor an Agent Server on LangSmith Cloud with build logs, Agent Server logs, and runtime metrics. Use logs to investigate a specific revision and metrics to track Agent Server performance over time.

## View Agent Server logs

Each revision includes build logs and server logs.

> [tab] LangSmith UI
>
> From the **Agent Servers** view:
>
> 1. Select an Agent Server.
> 2. In the **Revisions** table, select a revision. The details panel opens with the **Build** tab selected.
> 3. Review the build logs.
> 4. Select the **Server** tab to view server logs. Server logs become available after LangSmith deploys the revision.
> 5. Adjust the date and time range as needed. The default range is **Last 7 days**.

> [tab] LangGraph CLI
>
> To view server logs, run:
>
> ```shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> langgraph deploy logs
> ```
>
> To view build logs, run:
>
> ```shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> langgraph deploy logs --type build
> ```
>
> To stream new logs, run:
>
> ```shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> langgraph deploy logs --follow
> ```
>
> Filter logs by time range, log level, or search string:
>
> ```shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> langgraph deploy logs --start-time 2026-03-01T00:00:00Z --level ERROR
> ```
>
> To select an Agent Server, pass its name or ID:
>
> ```shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> langgraph deploy logs --name my-agent
> langgraph deploy logs --agent-server-id <AGENT_SERVER_ID>
> ```
>
> For all options, see the [`deploy logs` CLI reference](../../Get%20started/Reference/LangGraph%20CLI.md#deploy-logs).

## Forward server logs to Datadog

To forward Agent Server logs to Datadog, configure these environment variables or secrets on the Agent Server:

* **`DD_API_KEY`**: Your [Datadog API key](https://docs.datadoghq.com/account_management/api-app-keys/).
* **`DD_LOGS_ENABLED=true`**: Enables log forwarding.

To correlate logs with traces, also set `DD_LOGS_INJECTION=true`. For all supported Datadog variables, see [Supported Datadog environment variables](../Reference/Cloud%20Agent%20Server%20environment%20variables.md#dd_api_key).

## View Agent Server metrics

To view Agent Server metrics:

1. From the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-monitor-deployment), select **Agent Servers**.
2. Select an Agent Server.
3. Select the **Monitoring** tab. For metric definitions, see [Control plane monitoring](../../Get%20started/Deployment%20components/LangSmith%20control%20plane.md#monitoring).
4. Adjust the date and time range as needed. The default range is **Last 15 minutes**.

## See also

* [Revisions](Revisions.md)
* [Manage an Agent Server](Manage%20an%20Agent%20Server.md)
