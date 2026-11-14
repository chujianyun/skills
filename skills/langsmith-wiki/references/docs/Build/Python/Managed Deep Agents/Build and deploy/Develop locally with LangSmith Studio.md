# Develop locally with LangSmith Studio

> Run and test a Managed Deep Agent locally with mda dev and LangSmith Studio.

`mda dev` compiles a Managed Deep Agents project and runs it on a local Agent Server. It opens [LangSmith Studio](../../../../Test/Test%20from%20Studio/LangSmith%20Studio.md) so you can interact with the agent and inspect its behavior before deploying.

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

## Start local Studio

Install the project dependencies and add the model provider credentials to `.env`.

Python projects also require [`uv`](https://docs.astral.sh/uv/).

From the project root, run:

```bash
uv run mda dev
```

The CLI prints the local server and Studio URLs and opens Studio in your browser. Send messages in Studio to inspect model responses, tool calls, state, and interrupts.

After changing project files, stop and rerun `mda dev` to recompile the project.

## What `mda dev` does

`mda dev`:

1. Validates the project and compiles it into `.mda/build`.
2. Copies the project `.env` into the local build and adds local-only identity configuration when needed.
3. Creates a local [Context Hub](Manage%20Context%20Hub%20for%20Managed%20Deep%20Agents.md) mock for instructions, skills, and memory.
4. Starts the language-specific LangGraph development server.
5. Opens the agent in Studio.

Local development does not create or update a hosted deployment.

## Trace local runs

`mda dev` sends traces to the agent's **Local** environment. The project name is `{name}-local`, taken from the `name` you pass to `define_deep_agent` or `defineDeepAgent`.

In an [agent-based workspace](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), LangSmith rejects those traces until the agent record exists. [`mda deploy`](Deploy%20a%20Managed%20Deep%20Agent.md) creates that record. `mda dev` alone does not.

Before you rely on local traces, [create the agent](../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once with that same identifier in the UI or API, or run `mda deploy` once. Studio chat still works while traces are rejected.

## Configure the local server

| Flag | Use |
| - | - |
| `--port PORT` | Set the local server port. |
| `--hostname HOSTNAME` | Set the hostname on which the server listens. |
| `--no-browser` | Start the server without opening Studio automatically. |
| `--no-reload` | Disable the LangGraph development server's hot reload. |

For all command details, see the [`mda dev` CLI reference](Managed%20Deep%20Agents%20CLI%20reference.md#develop-locally).

## Understand local behavior

`mda dev` uses local defaults to make testing easier:

* If the agent uses identity, Studio provides a local test user automatically.
* If the configured sandbox is unavailable, the agent uses a temporary local folder instead. The CLI prints the folder path.
* [Schedules](../Agent%20capabilities/Add%20schedules%20to%20Managed%20Deep%20Agents.md) do not run. `mda dev` lists each schedule at startup but does not provision it, so no scheduled run fires locally.

These defaults differ from a deployed agent. Test identity and sandbox behavior in a development deployment before using the agent in production.
