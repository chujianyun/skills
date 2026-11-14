# Agent environments

> How an agent's environments divide its traces, how to select one, and which parts of the set are fixed.

An *environment* records where an agent was running when it produced a trace. Every trace an [agent](Agent%20Registry.md#agent) records lands in exactly one of its environments, which are drawn from a fixed set of four.

Because the environment travels with the trace, where the agent was running is a property of the trace itself.

> [!NOTE]
>
> Agent-based workspaces are available on [LangSmith Cloud](../../Cloud/Cloud%20%28SaaS%29.md). They are not available on [self-hosted](../../Self-hosted/Self-hosted%20LangSmith.md) LangSmith. To check whether your workspace is agent-based, look at the control at the top left. In an agent-based workspace, it is a workspace switcher that names your workspace. In a [project-based](../../../Monitor/Trace/Observability%20concepts.md#tracing-projects) workspace, it shows the LangSmith logo.

## Environment names

The four environments are fixed, and custom names are not supported. The environment switcher lists them most production-like first:

* **Production**
* **Staging**
* **Development**
* **Local**

How many of the four an agent has depends on [how it was created](Create%20an%20agent.md). An agent [built in LangSmith Studio](../../../No-code%20agents/Studio/Build%20an%20agent%20with%20LangSmith%20Studio.md) starts with **Production** alone, and each of the others appears the first time a trace is addressed to it. An agent created any other way starts with all four.

LangSmith attaches no behavior to the choice beyond keeping each environment's traces apart. An environment does not change how an agent is instrumented, and the same build can report into a different environment by changing its [agent addressing](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md).

## Select an environment

Wherever LangSmith needs one environment instead of all of them, it uses the same control: a button showing the current environment, which opens the list. It lists the agent's environments in the order above.

The environment selected when you arrive depends on the section:

* **Studio and alerts**: **Production**.
* **Monitoring and Deployments**: The environment you last used for the agent, or **Production** when there is none.
* **Tracing**: The environment you last used for the agent, then **Local**, then the first environment the agent has.

On Deployments, **Local** does not display, and the list adds a **Preview** entry when preview builds are turned on and the agent has previews.

The list holds only the environments that exist for the agent.

This control drives environment selection on Tracing, Monitoring, alerts, [Engine](../../../Engine/LangSmith%20Engine.md), Studio, and Deployments. [Evaluators](../../../Test/Evaluators/Manage%20evaluators.md) and [Insights](../../../Monitor/Observe/Monitoring%20%26%20alerting/Discover%20errors%20and%20usage%20patterns%20with%20Insights.md) also scope to a single environment, but they do it without this dropdown.

## See also

* [Agent Registry](Agent%20Registry.md)
* [Log traces to an agent](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md)
* [Configure legacy integrations](Create%20an%20agent.md#use-an-environment-project)
* [Observability concepts](../../../Monitor/Trace/Observability%20concepts.md)
