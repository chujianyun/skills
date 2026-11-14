# Trace Claude Managed Agents

> Automatically trace Claude Managed Agent sessions and events with LangSmith.

[Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) are Anthropic's hosted, cloud-based agents that run in managed environments. LangSmith supports tracing Claude Managed Agent sessions via the `wrapAnthropic` wrapper, giving you visibility into session events and message flows.

> [!NOTE]
>
> Claude Managed Agents tracing is currently supported in **TypeScript only**.

> [!NOTE]
>
> In an [agent-based workspace](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

## Installation

```bash npm
npm install langsmith @anthropic-ai/sdk
```

```bash yarn
yarn add langsmith @anthropic-ai/sdk
```

## Environment setup

```bash Shell
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=<your-langsmith-api-key>
export LANGSMITH_AGENT_ID="<your-agent-id>"
export LANGSMITH_AGENT_ENVIRONMENT="local"
export ANTHROPIC_API_KEY=<your-anthropic-api-key>
```

## Trace Claude Managed Agents

Wrap the Anthropic client with `wrapAnthropic`. The wrapper traces all events that flow through the session.

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";
import { wrapAnthropic } from "langsmith/wrappers/anthropic";

const anthropic = wrapAnthropic(new Anthropic());

// Create a managed agent
const agent = await anthropic.beta.agents.create({
  name: "my-agent",
  model: "claude-opus-4-8",
  system: "You are a helpful assistant.",
  tools: [
    // ... your tools here
  ],
});

// Create a cloud environment for the agent to run in
const environment = await anthropic.beta.environments.create({
  name: "my-environment",
  config: {
    type: "cloud",
    networking: { type: "unrestricted" },
  },
});

// Create a session connecting the agent and environment
const session = await anthropic.beta.sessions.create({
  agent: agent.id,
  environment_id: environment.id,
  title: "My session",
});

// Stream session events
const stream = await anthropic.beta.sessions.events.stream(session.id);

// Send a message to the agent
await anthropic.beta.sessions.events.send(session.id, {
  events: [
    {
      type: "user.message",
      content: [
        {
          type: "text",
          text: "Hello! Can you help me with something?",
        },
      ],
    },
  ],
});

// Consume the event stream until the session is idle
for await (const event of stream) {
  if (event.type === "session.status_idle") {
    break;
  }
}
```

> [!NOTE]
>
> Full tracing of subagents in Anthropic's multi-agent architecture requires
> tapping into a separate event stream and is not yet supported. Only top-level
> session events are traced.

## Next steps

* [Trace Anthropic models](../LLM%20providers/Trace%20with%20Anthropic.md): Trace standard Anthropic API calls and tool use
* [Trace Claude Agent SDK agents](Trace%20with%20the%20Claude%20Agent%20SDK.md): Trace agents running locally with the Claude Agent SDK
* [Monitor your agent](../../../../Observe/Monitoring%20%26%20alerting/Monitor%20projects%20with%20dashboards.md): Set up dashboards and alerts for production agents
