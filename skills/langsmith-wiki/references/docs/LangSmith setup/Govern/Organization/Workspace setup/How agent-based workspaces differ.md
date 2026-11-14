# How agent-based workspaces differ

> What changes when a workspace moves from organizing traces by tracing project to organizing them by agent and environment.

LangSmith organizes a workspace in one of two ways. A *project-based workspace* groups traces by [tracing project](../../../../Monitor/Trace/Observability%20concepts.md#tracing-projects). An *agent-based workspace* groups them by [agent](../../../Overview/Agent-based%20workspaces/Agent%20Registry.md#agent), and divides each agent's traces across [environments](../../../Overview/Agent-based%20workspaces/Agent%20environments.md) drawn from a fixed set of four.

Agent-based organization is available on [LangSmith Cloud](../../../Cloud/Cloud%20%28SaaS%29.md). It is not available on [self-hosted](../../../Self-hosted/Self-hosted%20LangSmith.md) LangSmith. This page covers what is different in an agent-based workspace, and what changes if yours becomes one.

## Check which one you have

The control at the top left tells you. In an agent-based workspace it names your workspace and opens a list of the workspaces in your organization. In a project-based workspace it shows the LangSmith logo, and the sidebar has an **Application** section with an application picker.

## What the change is worth

Agents and environments record what a tracing project cannot: which agent produced a trace, and in which environment. LangSmith can then act on that context rather than asking you to filter for it, so an alert can watch production and stay quiet about local runs, and a prebuilt dashboard covers each environment without you naming a project for it.

## What changes

The organizing container changes, and everything scoped to it follows:

* **Traces** group under an agent and one of its environments instead of under a tracing project you named. Nothing is re-ingested or moved. When an existing workspace is migrated, each tracing project becomes an agent with a production environment, and that environment keeps the project's ID and name. A tracing project for a new environment takes the agent identifier, a hyphen, and the environment as its name: an agent whose identifier is `checkout` has its staging traces in `checkout-staging`.
* **Prebuilt dashboards** cover an environment rather than a named project. See [Monitor agent environments with dashboards](../../../../Monitor/Observe/Monitoring%20%26%20alerting/Monitor%20projects%20with%20dashboards.md).
* **Alerts** are scoped to an environment of an agent. See [Alerts](../../../../Monitor/Observe/Monitoring%20%26%20alerting/Alerts%20in%20LangSmith.md).
* **Evaluators** attach to an environment. See [Manage evaluators](../../../../Test/Evaluators/Manage%20evaluators.md).
* **Datasets** attach to one or more agents rather than to a project, and to no environment, so one dataset can serve several agents. See [Create and manage datasets in the UI](../../../../Test/Datasets%20%26%20Experiments/Datasets/Create%20a%20dataset/Create%20and%20manage%20datasets%20in%20the%20UI.md).
* **Navigation** gains an agent picker in the top bar, which moves between the agent list and a single agent's Overview. See [Navigate agents](../../../Overview/Agent-based%20workspaces/Navigate%20agents.md).
* **The top-left control** becomes a workspace switcher, as described in [Check which one you have](#check-which-one-you-have). In a project-based workspace, where Fleet is enabled, the logo opens a menu for moving between LangSmith and Fleet. Otherwise, it links to the LangSmith home page. In an agent-based workspace, where Fleet is enabled, the workspace list ends with a link to Fleet.

What does not change: your traces, datasets, prompts, and experiments are the same records, and existing tracing configuration keeps working. See [Configure legacy integrations](../../../Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project).

## How a workspace moves

A new organization on LangSmith Cloud gets agent-based workspaces. In an existing organization, LangChain migrates the workspaces, and the migration keeps your existing tracing projects as described in [What changes](#what-changes). No action is required from you.

> [!NOTE]
>
> This page describes the change, not its schedule. Timing is not published.

## See also

* [Agent Registry](../../../Overview/Agent-based%20workspaces/Agent%20Registry.md)
* [Agent environments](../../../Overview/Agent-based%20workspaces/Agent%20environments.md)
* [Workload isolation](Workload%20isolation.md)
* [Administration overview](../Overview.md#agents)
