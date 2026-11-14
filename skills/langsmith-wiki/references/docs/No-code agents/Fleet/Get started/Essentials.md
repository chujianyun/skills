# Essentials

> Fleet's core features

LangSmith Fleet essentials are the core features that make up the foundation of your agents. They include tools, channels, memory, sub-agents, and approvals.

## Agent identity

Agent identity controls whose [credentials](../Configure/Manage%20workspace%20administration.md) the agent uses when it interacts with apps and services.

See [Agent identity](../Configure/Agent%20identity.md) for more information.

## Agent sidebar

Configure your agent from the sidebar built into the agent chat page. The sidebar organizes agent configuration into drawers:

* **Channels**: Connect the places your agent runs in, such as Slack, Gmail, and Microsoft Teams. See [Channels](../Tools%20and%20automation/Channels.md).
* **Sharing**: Control who can use the agent, with options for private, workspace, or specific people. See [Change access to the agent](../Configure/Manage%20agent%20settings.md#change-access-to-the-agent).
* **Connections**: Manage the integrations and tools your agent can use, set the connection format, and set each tool to run automatically or ask for approval. See [Tools](#tools), [Agent identity](#agent-identity), and [Human-in-the-loop](#human-in-the-loop).
* **Knowledge**: Manage the agent's instructions, skills, and memory. See [Instructions](#instructions), [Skills](#skills), and [Memory](#memory).
* **Schedule**: Run your agent on a recurring basis. See [Schedules](../Tools%20and%20automation/Schedules.md).
* **Advanced settings**: Configure the model, API keys, sub-agents, diagnostics, and developer options for your agent.

> [!TIP]
>
> You can also configure your agent by chatting with it. In the agent chat, tell the agent how to improve itself, for example: "Add the Slack tools so you can respond to messages."

## Channels

Channels define when your agent should start running. You can connect your agent to external tools or time-based schedules, letting it respond automatically to messages, emails, or recurring events.

See [Channels](../Tools%20and%20automation/Channels.md) for setup instructions and supported channel types.

## Human-in-the-loop

Stay in control of important decisions. You can set up your agent to pause and ask for your approval before taking certain actions. This ensures your agent handles most tasks automatically, while you retain oversight.

### Set an approval mode

Each tool has an approval mode you can set in the **Connections** drawer of the [agent sidebar](#agent-sidebar):

* **Auto**: The tool runs automatically without approval.
* **Ask**: The agent pauses and waits for your approval before the tool runs.

To require approval for a tool, set it to **Ask**. When the agent reaches that tool, it pauses until you respond.

### What you can do when your agent pauses

When your agent stops to ask for approval, you have two options:

> [card] Accept
>
> Give the green light and let your agent proceed with its plan.

> [card] Reject
>
> Decline the action and tell the agent what to change.

> [!NOTE]
>
> When an agent is triggered from Slack, it raises the approval request directly in the Slack thread with **Approve** and **Deny** buttons, so you can respond without leaving Slack. See [Approve or deny actions in Slack](../Tools%20and%20automation/Integrate%20Slack%20with%20an%20agent.md#approve-or-deny-actions-in-slack).

## Instructions

Instructions are the system prompt that defines your agent's behavior, personality, and capabilities. They guide how the agent interprets requests, uses its tools, and responds to users.

To edit instructions:

1. In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-essentials), open your agent.
2. In the sidebar, expand the **Knowledge** drawer.
3. In the **Instructions** section, edit the agent instructions.

> [!TIP]
>
> You can also update instructions by prompting the agent directly in the chat. For example: "Update your instructions to always respond in bullet points."

## LangChain Standard Units (LSUs)

Fleet usage is measured in LangChain Standard Units (LSUs). LSU usage is based on the [model](#models) work your agent performs, including the selected tier and the amount of content it processes and generates.

> [!NOTE]
>
> The new [model tiers](#models) and LSU pricing apply to Fleet usage starting **October 1, 2026**. If you use a custom model, [contact our sales team](https://www.langchain.com/contact-sales) about your transition.

Allowances are shared across your organization and reset monthly:

* **Free plan**: 7 LSUs per organization each month. When the allowance is used up, Fleet pauses new runs until the allowance resets or the organization upgrades to Plus.
* **Plus plan**: 37 LSUs per organization each month. Additional usage is billed. For current rates, see the [LangSmith pricing page](https://www.langchain.com/pricing).

Runs vary in cost. A Fleet run can make multiple model calls, and tasks vary in length and complexity. A longer task, a larger amount of context, or a higher tier can consume more LSUs than a short task in the Fast tier.

If your organization has grandfathered Plus seat or trace pricing, those rates do not change when Fleet moves to LSU pricing. [Contact our sales team](https://www.langchain.com/contact-sales) to confirm your organization's pricing.

## Memory

Agents remember important information from previous conversations and can update themselves to work better. Fleet agents use two sources of memory:

* **Thread-scoped memory**: Context from the current conversation thread, including messages and actions in that thread.
* **Long-term memory**: Persistent files in the agent workspace, such as `AGENTS.md`, `tools.json` (tool configuration), `subagents/*`, and `skills/*`. These are loaded at runtime and available from the start of each run. `AGENTS.md` is inserted into the system prompt automatically. Other long-term files are not added to the prompt automatically; the agent must read them on demand (for example, using the `read_file` tool).

Agents persist relevant details from past interactions by writing files to a **memories folder** (using `write_file` and `edit_file` tool calls). This helps them make better decisions in future conversations.

> [!NOTE]
>
> By default, agents require approval before saving to the memories folder. You can change this in the **Knowledge** drawer under **Memory**.
>
> For agents that run on automated [schedules](../Tools%20and%20automation/Schedules.md#add-a-schedule), we recommend [disabling the approval requirement](../Configure/Manage%20agent%20settings.md#disable-required-approval-for-memory-updates) so the agent can persist information without manual intervention.

For more information, see [How we built the memory system for Fleet (formerly known as Agent Builder)](https://www.langchain.com/blog/how-we-built-agent-builders-memory).

## Models

Fleet manages models for you. It selects and maintains a strong model for each task, so you get good results without having to choose a provider, configure a model, or supply an API key. Usage is billed in [LangChain Standard Units (LSUs)](#langchain-standard-units-lsus).

> [!NOTE]
>
> The new model tiers and [LSU](#langchain-standard-units-lsus) pricing apply to Fleet usage starting **October 1, 2026**. If you use a custom model, [contact our sales team](https://www.langchain.com/contact-sales) about your transition.

Fleet provides three managed tiers. The model behind each tier may change over time as new models become available, so you can choose based on the work you need done instead of a specific provider or model.

| Tier | Best for | Relative cost (Higher tiers typically cost more and take longer.) |
| - | - | - |
| **Fast** | Everyday tasks such as research, summaries, and drafting | Low |
| **Pro** | More complex tasks that benefit from stronger reasoning | Medium |
| **Max** | The most demanding tasks, where maximum capability matters most | High |

### Custom models

Custom models are not available alongside Fast, Pro, and Max in the managed Fleet model picker. LangChain manages model-provider access for the managed tiers, so you do not need your own model-provider API key. If custom models are a requirement for an enterprise deployment, [contact our sales team](https://www.langchain.com/contact-sales).

## Self-updates

Agents can update themselves: they can add new tools, remove ones they don't need, or adjust their instructions. However, agents can't change their name, description, or the channels that start them.

## Skills

Skills are a way to bundle capabilities and provide more specific information in situations where the context is not universally relevant.

Using skills can help:

* Save on token usage by only providing the context that is relevant to the current task.
* Prevent the agent from having too much context in the system prompt, which can lead to hallucinations and incorrect responses.

To add a skill, expand the **Knowledge** drawer in the agent sidebar and click **+ Add skill**.

For more information, see [Skills](../Tools%20and%20automation/Skills.md).

## Sub-agents

Build complex agents by breaking big tasks into smaller, specialized helpers. Think of sub-agents as a team of specialists, each one handling a specific part of the job while working with your main agent.

This approach makes it easier to build sophisticated systems. Instead of one agent trying to do everything, you can have specialized helpers that each excel at their part of the task.

Here are some ways you might use sub-agents:

* Split into sub-tasks: Have one agent fetch data, another summarize it, and a third format the results.
* Specialized tools: Give different agents access to different tools based on what they need to do.
* Independent work: Let sub-agents work on their own, then bring their results back to the main agent.

To add a sub-agent, open your agent, expand the **Advanced settings** drawer in the sidebar, and under **Subagents** click **+ Add subagent**.

## Threads

Threads are conversations between you and your agent. Each thread contains messages, agent responses, and any actions the agent takes.

To view threads, navigate to your agent in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-essentials). The inbox shows all threads for that agent. Click on a thread to view the conversation.

### Read and unread status

How threads are marked depends on whether the agent uses channels:

* **Chat agents (no channel):** Responses mark the thread as **unread**. Viewing the thread marks it as read.
* **Channel-based agents:** Responses keep the thread as **read** by default.

You can manually mark any thread as read or unread at any time.

## Tools

Tools let your agents interact with your apps and services. Your agents can send emails, create calendar events, post messages, search the web, and more. Choose from built-in tools for Gmail, Slack, Google Calendar, GitHub, and many others.

Tools work regardless of how the agent was triggered. For example, you can start a task in the Fleet chat UI and have the agent send you a [Slack message](../Tools%20and%20automation/Integrate%20Slack%20with%20an%20agent.md#add-slack-tools) when it's done.

See [Tool integrations](../Tools%20and%20automation/Tool%20integrations.md) for more information.

## Traces

Traces are a series of steps that your agent takes to go from input to output. You can use [LangSmith](../../../Monitor/Overview/LangSmith%20Observability.md) to visualize these execution steps.

To view all traces for your agent:

1. In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-essentials), open your agent.
2. In the sidebar, expand the **Advanced settings** drawer.
3. Under **Diagnostics**, click **View agent traces**.

To view a trace for a specific thread:

1. In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-fleet-essentials), navigate to your agent's inbox.
2. Right-click on the thread you want to trace and select **View trace**.

For more information, see [LangSmith Observability](../../../Monitor/Overview/LangSmith%20Observability.md).

> [!NOTE]
>
> Fleet traces all agent runs and stores them in LangSmith. LLM providers do not retain your data. On LangSmith Cloud, trace data is stored with a 14-day retention period by default.

## Next steps

* [Set up your workspace](../Configure/Manage%20workspace%20administration.md)
* [Connect apps and services](../Tools%20and%20automation/Tool%20integrations.md)
* [Use remote servers for tools](../Tools%20and%20automation/Remote%20MCP%20servers.md)
* [Choose between workspace and private agents](../Configure/Manage%20agent%20settings.md)
* [Call agents from your app](../Advanced/Use%20Fleet%20agents%20in%20code.md)
