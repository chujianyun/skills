# Add instructions to Managed Deep Agents

> Define the system prompt for a managed deep agent in instructions.md.

Instructions define always-on agent behavior. They form the core of the agent's system prompt.

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

Put the instructions for your agent into `instructions.md` at the project root:

```text
my-agent/
  instructions.md
```

For the full project layout, see [Project structure](../Get%20started/Managed%20Deep%20Agents%20project%20structure.md).

## Add instructions

Create or modify `instructions.md` to define the agent's role, behavior, constraints, and guidance for using its tools:

```markdown instructions.md
# Assistant

You are a helpful assistant.
```

MDA inserts instructions into the agent's system prompt on every run.
The agent cannot modify these instructions at runtime.

## Deployment

When you run `mda deploy`, MDA syncs `instructions.md` to the agent's [Context Hub](../Build%20and%20deploy/Manage%20Context%20Hub%20for%20Managed%20Deep%20Agents.md).

You can then edit the instructions in the LangSmith UI and have those changes apply to the agent.

It is best to keep the `instructions.md` file in the repo as the source of truth for lasting changes, as later deployments sync the project copy again.

For what syncs, what does not, and how to open the repo from a deployment, see [Context Hub](../Build%20and%20deploy/Manage%20Context%20Hub%20for%20Managed%20Deep%20Agents.md).

## When to use instructions

| Concept | Role | Loaded when |
| - | - | - |
| **Instructions** | Always-on system prompt | Every run |
| **[Skills](Add%20skills%20to%20Managed%20Deep%20Agents.md)** | Task-specific procedures | When the agent selects them |
| **[Memory](Add%20memory%20to%20Managed%20Deep%20Agents.md)** | Knowledge the agent can update | When durable memory is enabled |

For more information, see [Project structure](../Get%20started/Managed%20Deep%20Agents%20project%20structure.md).
