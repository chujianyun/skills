# Subagents

> Delegate work to subagents that run inline or in the background for a managed deep agent.

Give a managed deep agent subagents to delegate specialized or context-heavy work, such as researching a topic, reviewing a change, or running a long task in the background with an async subagent while the agent keeps talking to the user. Each subagent has its own prompt and context window. It can also use its own model and tools.

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

There are two types of subagents:

| Type | How the agent uses it | Use it for |
| - | - | - |
| Subagent | Calls it with `task` and waits for its answer | Focused work whose result the agent needs before it continues |
| Async subagent | Starts it with `start_async_task` and keeps working; the subagent reports back when it finishes | Long-running or parallel work the agent doesn't need to wait for |

A subagent runs inside the agent's graph. Managed Deep Agents builds each async subagent as its own graph in the same deployment. Both kinds work in the agent's [sandbox](Add%20a%20sandbox%20to%20Managed%20Deep%20Agents.md). For how subagents work in the open source Deep Agents SDK, see [Subagents](https://docs.langchain.com/oss/python/deepagents/subagents.md) and [Async subagents](https://docs.langchain.com/oss/python/deepagents/async-subagents.md).

> [!NOTE]
>
> Async subagents require `managed-deepagents>=0.10.0`.

## Declare a subagent

Add subagent definitions to `subagents` in the [agent definition](Define%20a%20Managed%20Deep%20Agent.md). Each one needs a `name` and a `description`; the agent uses the description to decide when to delegate. To make a subagent async, add `async` to its definition:

> [tab] Subagent
>
> ```python agent.py theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from managed_deepagents import define_deep_agent
>
> agent = define_deep_agent(
>     name="research-assistant",
>     model="openai:gpt-6.1-sol",
>     subagents=[
>         {
>             "name": "reviewer",
>             "description": "Reviews a draft for accuracy and clarity.",
>             "system_prompt": "Review the draft and list concrete fixes.",
>         },
>     ],
> )
> ```

> [tab] Async subagent
>
> ```python agent.py theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from managed_deepagents import define_deep_agent
>
> agent = define_deep_agent(
>     name="research-assistant",
>     model="openai:gpt-6.1-sol",
>     subagents=[
>         {
>             "name": "researcher",
>             "description": "Researches a topic in the background.",
>             "system_prompt": "Research the topic and report your findings.",
>             "async": True,
>         },
>     ],
> )
> ```

## Subagents

The agent runs a subagent with the `task` tool and waits for its answer. The subagent runs inside the agent's graph and works in the agent's [sandbox](Add%20a%20sandbox%20to%20Managed%20Deep%20Agents.md).

Every agent also gets a `general-purpose` subagent for delegated work that doesn't match a declared subagent. See [The general-purpose subagent](https://docs.langchain.com/oss/python/deepagents/subagents.md#the-general-purpose-subagent).

### What a subagent inherits

A subagent starts from the agent's configuration and replaces what its definition sets:

| Setting | Behavior |
| - | - |
| `model`, `tools`, `permissions`, `interrupt_on` | Uses the agent's setting unless the subagent sets its own |
| `system_prompt` | Uses only the subagent's prompt, not the agent's [instructions](Add%20instructions%20to%20Managed%20Deep%20Agents.md) |
| `skills` | Loads only the skills the subagent lists; list `"/skills/"` to load the agent's |
| `middleware`, `response_format` | Uses only the subagent's own |
| Memory | Not loaded |

A subagent in fork mode starts with a copy of the agent's conversation and also uses the agent's instructions, middleware, skills, and memory. See [Choose a launch mode](https://docs.langchain.com/oss/python/deepagents/async-subagents.md#choose-a-launch-mode).

### Select MCP servers

Set `mcp` on a subagent to choose which [MCP server](Connect%20to%20MCP%20servers.md) definitions give it tools. `mcp` does not affect the subagent's other tools.

> [!NOTE]
>
> Subagent MCP selection requires `managed-deepagents>=0.10.2`.

| `mcp` value | Subagent | Async subagent |
| - | - | - |
| Omitted | Inherits the agent's tools | Inherits the agent's MCP servers |
| List of definitions | Keeps MCP tools only from these definitions. The agent must also load them. | Loads only these definitions |
| `[]` or `None` | No MCP tools | No MCP tools |

An async subagent connects only to the servers it selects and asks only for their credentials.

Only a [graph factory](Define%20a%20Managed%20Deep%20Agent.md#select-configuration-per-run) can set `mcp` on the agent.

```python agent.py expandable
from managed_deepagents import ManagedServerRuntime, connections, define_deep_agent, define_mcp

knowledge = define_mcp(
    servers={
        "langchainDocs": {"transport": "http", "url": "https://docs.langchain.com/mcp"},
        "notion": {
            "transport": "http",
            "url": "https://mcp.notion.com/mcp",
            "connection": connections.get("engineering-notion", {"type": "user"}),
        },
    },
)

planning = define_mcp(
    servers={
        "linear": {
            "transport": "http",
            "url": "https://mcp.linear.app/mcp",
            "connection": connections.get("engineering-linear", {"type": "user"}),
        },
    },
)

def agent(runtime: ManagedServerRuntime):
    return define_deep_agent(
        name="research-assistant",
        model="openai:gpt-5.5",
        mcp=[knowledge, planning],
        subagents=[
            {
                "name": "researcher",
                "description": "Answers questions from the docs and the team wiki.",
                "system_prompt": "Search the docs and Notion, and cite the pages you use.",
                "mcp": [knowledge],
            },
            {
                "name": "planner",
                "description": "Turns findings into Linear issues.",
                "system_prompt": "Create one Linear issue for each follow-up.",
                "mcp": [planning],
            },
        ],
    )
```

## Async subagents

The agent starts an async subagent with `start_async_task` and keeps working while the subagent runs on its own thread. The subagent reports back when it finishes.

### How async subagents run

Each async subagent appears in the deployment as its own graph, named after the agent and the subagent, such as `research-assistant--researcher`. Managed Deep Agents finds async subagents by reading your agent file when it builds, not by running it. Write each one directly in `subagents` or in a variable, with a fixed `name` and `async` value. An async subagent built by a function or a loop gets no graph, and the agent fails to start. A [graph factory](Define%20a%20Managed%20Deep%20Agent.md#select-configuration-per-run) can declare async subagents too, as long as it returns the agent definition directly.

Agents served by `mda dev` or a deployment also get an async version of the `general-purpose` subagent, so the agent can run delegated work in the foreground or in the background.

The agent manages async subagents with these tools:

| Tool | What it does |
| - | - |
| `start_async_task` | Starts an async subagent on its own thread and returns a task ID right away |
| `check_async_task` | Gets a task's status and, once it finishes, its result |
| `update_async_task` | Sends new instructions to a task |
| `cancel_async_task` | Stops a running task |
| `list_async_tasks` | Lists the agent's tasks and their statuses |

The tools come with the async `general-purpose` subagent, so every agent served by `mda dev` or a deployment has them. Agents run with `mda eval` don't.

### Get notified when a subagent finishes

Async subagents report back on their own, whether the agent is busy, idle, or waiting on an approval. The agent doesn't need to poll with `check_async_task`:

| When the subagent finishes, the agent is | What happens |
| - | - |
| Busy | The agent checks its unfinished tasks before each model call, so it gets the result mid-run |
| Idle | The subagent wakes the agent with a new run |
| Paused on an approval | The approval is left alone; the agent gets the result once the user answers |

Each result is reported once. Before each model call, the agent makes one status check per unfinished task, capped at 5 seconds.

If a subagent pauses for approval, the agent sees its task as `waiting` until someone answers on the subagent's thread. See [Answer approvals in channels](#answer-approvals-in-channels).

### Configure an async subagent

Do not set `graph_id`, `url`, `headers`, or `runnable` on an async subagent: Managed Deep Agents builds and launches its graph itself. These options pass through to Deep Agents:

| Option | Default | Description |
| - | - | - |
| `update_strategy` | `"interrupt"` | `"enqueue"` queues a follow-up behind the current run instead of interrupting it |
| `notify_parent` | `True` | Wake the agent when the subagent finishes while the agent is idle. Set to `False` to handle results yourself, such as with `webhook` |
| `webhook` | Not set | URL the Agent Server calls whenever a run of the subagent finishes, with the run's thread ID, run ID, and status. See [Deliver results through your app](https://docs.langchain.com/oss/python/deepagents/async-subagents.md#deliver-results-through-your-app) |
| `mode` | `"isolated"` | `"fork"` starts the subagent with a copy of the agent's conversation |

For how each option behaves, see [Async subagents](https://docs.langchain.com/oss/python/deepagents/async-subagents.md).

To use an agent on another deployment as an async subagent, declare it with its graph ID and `url` and without `async`, and Managed Deep Agents passes it to Deep Agents unchanged. For a Managed Deep Agent, the graph ID is its `name`. See [remote subagents](https://docs.langchain.com/oss/python/deepagents/async-subagents.md#http-transport-remote).

### What an async subagent inherits

An async subagent inherits from the agent the same way a [subagent](#what-a-subagent-inherits) does. In fork mode, it starts with a copy of the agent's conversation but keeps its own prompt, tools, and middleware, so it usually doesn't reuse the agent's [prompt cache](https://docs.langchain.com/oss/python/deepagents/async-subagents.md#fork-mode).

### Share the sandbox and trace

An async subagent starts on a new thread, separate from the agent's. Because the agent starts it as the same user, it shares the agent's sandbox. With [private threads](Add%20identity%20to%20Managed%20Deep%20Agents.md), a run of the subagent from a different user gets its own sandbox. When it shares the sandbox, it uses the agent's files as they are and only refreshes connector credentials. If the agent hasn't used its sandbox yet, the subagent creates it, and the agent uses the same sandbox later.

When tracing is on, an async subagent's run appears under the agent's run in LangSmith.

### Answer approvals in channels

When an agent runs in a [channel](Channels/Connect%20Managed%20Deep%20Agents%20to%20channels.md), its async subagents report to the same channel thread:

1. The user asks the agent for work in a channel thread, and the agent starts an async subagent.
2. If the subagent pauses for [approval](Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md#human-in-the-loop), Slack shows the request in the thread, and answering it there resumes the subagent. Other channels don't post the request; resume the subagent's thread as you would any [interrupt](Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md#respond-to-an-interrupt), in Studio or through the API.
3. When the subagent finishes, the agent gets its result and replies in the thread: in its current run if it's still working, or in a new run if it's idle. Turning off parent notifications stops the new run.

Managed Deep Agents doesn't post a subagent's answer to the channel; the agent decides what to tell the user.

### Evaluate an agent

`mda eval` runs without an Agent Server, so it can't evaluate an agent that declares async subagents. Evaluated agents also don't get the async `general-purpose` subagent or the async task tools.

## See also

* [Subagents](https://docs.langchain.com/oss/python/deepagents/subagents.md)
* [Async subagents](https://docs.langchain.com/oss/python/deepagents/async-subagents.md)
* [Agent definition](Define%20a%20Managed%20Deep%20Agent.md)
* [Sandboxes](Add%20a%20sandbox%20to%20Managed%20Deep%20Agents.md)
* [Channels](Channels/Connect%20Managed%20Deep%20Agents%20to%20channels.md)
