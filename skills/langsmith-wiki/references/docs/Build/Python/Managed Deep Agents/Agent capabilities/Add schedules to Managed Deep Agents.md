# Add schedules to Managed Deep Agents

> Declare managed cron schedules for Managed Deep Agents deployments, or create them at runtime.

Managed Deep Agents can run agents on a cron schedule. When you deploy the project, `mda deploy` provisions each schedule as a LangSmith cron after the deployment is live.

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

## Project structure

Schedule declarations live in the project-level `schedules/` directory, with one schedule per file:

```text
my-agent/
  agent.py
  schedules/
    daily_digest.py
```

## Add a schedule

The file name becomes the managed schedule name.

The schedule module must define a named `schedule` declaration.

```python schedules/daily_digest.py
from managed_deepagents import define_schedule

schedule = define_schedule(
    cron="0 8 * * 1-5",
    timezone="America/Los_Angeles",
    prompt="Write the daily digest.",
)
```

## Configure schedule input

Each schedule must define exactly one of:

* `prompt`: A natural-language prompt. Managed Deep Agents converts it to a user message when the cron fires.
* `input`: A structured LangGraph input object. Use this when you need to pass custom graph input instead of a single prompt.

```python schedules/nightly_sweep.py
from managed_deepagents import define_schedule

schedule = define_schedule(
    cron="30 2 * * *",
    input={
        "messages": [
            {"role": "user", "content": "Sweep stale tickets and summarize changes."}
        ]
    },
)
```

`cron` must be a standard five-field cron expression: minute, hour, day of month, month, and day of week. If `timezone` is omitted, LangSmith crons use UTC.

## Choose thread behavior

Schedules use ephemeral threads by default. Managed Deep Agents creates a fresh thread for each run and asks LangSmith to delete that temporary thread after the run completes.

Use a persistent thread when scheduled runs should share one thread history. When you omit `id`, `mda deploy` creates a thread for the schedule, keyed on the agent and schedule names. Renaming the schedule file starts a new thread. To use a specific thread, set `id` to a UUID. `mda deploy` creates the thread if it does not exist, and refuses a thread that another caller owns.

> [!NOTE]
>
> Omitting `id` requires `managed-deepagents>=0.10.2`. Earlier versions require the UUID of an existing thread.

### Declare the persistent schedule

> [!NOTE]
>
> The following example requires [durable memory](Add%20memory%20to%20Managed%20Deep%20Agents.md).

```python schedules/nightly_memory.py
from managed_deepagents import define_schedule

schedule = define_schedule(
    cron="0 3 * * *",
    prompt="Review the current project memory and list follow-up tasks.",
    thread={"mode": "persistent"},
)
```

## Deliver results to Slack

Set `deliver_to` to post the final response through a configured [Slack channel](Channels/Connect%20a%20Managed%20Deep%20Agent%20to%20Slack.md).

Use a Slack channel ID because scheduled runs have no originating thread.

> [!NOTE]
>
> Schedule delivery requires `managed-deepagents>=0.4.0`.

```python schedules/monday_greeting.py
from managed_deepagents import define_schedule

schedule = define_schedule(
    cron="0 9 * * 1",
    prompt="Write a short Monday greeting.",
    deliver_to={
        "channel": "slack",
        "to": {
            "type": "provider_conversation",
            "conversation_id": "C0123456789",
        },
    },
)
```

The Slack bot must have access to the destination.

## Use static declarations

Schedule declarations are extracted at compile time. Keep schedule configuration statically serializable:

* Use literals, lists, dictionaries, and references to top-level literal constants.

* Do not read environment variables, call functions, use `**kwargs`, or compute schedule values dynamically.

* Put dynamic behavior in the agent, tools, middleware, or runtime context instead.

## Test schedules locally

`mda dev` creates a cron job on the local server for each schedule in `schedules/`, so schedules fire locally as they do on a deployment. When `schedules/` changes, `mda dev` deletes and recreates them. Pass `--no-schedules` to stop schedules from firing while you iterate.

> [!NOTE]
>
> Local schedules require `managed-deepagents>=0.9.3`. Earlier versions list schedules at startup but do not run them.

## Deploy schedules

Test the project locally with [`mda dev`](../Build%20and%20deploy/Managed%20Deep%20Agents%20CLI%20reference.md#develop-locally), then deploy it with [`mda deploy`](../Build%20and%20deploy/Deploy%20a%20Managed%20Deep%20Agent.md). Open deployment traces in LangSmith to inspect model calls, tool calls, errors, and latency.

When the deployment reaches `DEPLOYED`, `mda deploy` deletes the cron jobs that earlier `schedules/` declarations created and creates cron jobs for the current declarations. Removing a local schedule file and redeploying removes the corresponding managed cron. Schedules created at runtime are unaffected.

> [!WARNING]
>
> If you deploy with `--no-wait`, the CLI triggers the remote build and exits before the deployment reaches `DEPLOYED`, so it does not reconcile schedules during that invocation. Run `mda deploy` without `--no-wait` when adding, changing, or removing schedules.

## Create schedules at runtime

> [!NOTE]
>
> Runtime schedules require `managed-deepagents` 0.9.0 or later.

Declarations in `schedules/` are fixed when you deploy. `runtime.schedules` creates schedules while the agent runs, so the agent can set up recurring or one-time work in response to a conversation. It is available on the runtime that tools and [middleware](Add%20custom%20middleware%20to%20Managed%20Deep%20Agents.md) receive, and it acts for the caller of the current run. Each schedule belongs to the current user or to the agent.

The agent reaches this API only through tools that you write. Expose the calls the agent needs, and leave out the ones it should not reach.

When a tool creates a schedule during a [channel](Channels/Connect%20Managed%20Deep%20Agents%20to%20channels.md) run, such as a Slack conversation, the schedule inherits that channel. Each run posts its final answer back to it. A new thread posts a new Slack message, and the current thread replies in the existing Slack thread.

`new_thread` decides which of the two a schedule uses.

### Create a recurring schedule

`remind_me` gives the agent a way to set up a recurring reminder for the person it is talking to. The agent calls it with the prompt to run and a cron expression for how often to run it. Each time the cron fires, a new run starts with that prompt as its user message. The agent decides what each scheduled run is asked to do.

```python tools/schedules.py
from langchain.tools import tool
from managed_deepagents import ManagedDeepAgentRuntime


@tool
async def remind_me(
    prompt: str, cron: str, runtime: ManagedDeepAgentRuntime, timezone: str = "UTC"
) -> str:
    """Run a prompt for the current user on a cron schedule."""
    item = await runtime.schedules.create(
        owner={"type": "user"},
        cron=cron,
        timezone=timezone,
        prompt=prompt,
    )
    return f"Created schedule {item['id']}."
```

Asked in Slack to send a standup reminder every weekday, the agent calls `remind_me`. It passes a prompt of its own wording and the cron `0 9 * * 1-5`. Each weekday run posts its answer to that Slack conversation as a new message, because `cron` schedules default to a new thread.

### Create a one-time schedule

Pass `at` in place of `cron` for work that runs once. `follow_up_later` gives the agent a way to set a single follow-up, such as checking a deploy after it finishes.

```python tools/follow_up.py
from datetime import datetime, timedelta, timezone

from langchain.tools import tool
from managed_deepagents import ManagedDeepAgentRuntime


@tool
async def follow_up_later(prompt: str, hours: int, runtime: ManagedDeepAgentRuntime) -> str:
    """Run a prompt once, a number of hours from now."""
    item = await runtime.schedules.create(
        owner={"type": "user"},
        at=datetime.now(timezone.utc) + timedelta(hours=hours),
        prompt=prompt,
    )
    return f"Scheduled a one-time follow-up: {item['id']}."
```

A one-time schedule defaults to the current thread, so its run continues the conversation that created it and replies in the same Slack thread.

### Create options

**owner** `object` *required*

`{ type: "user" }` selects the authenticated person of the current run, and the schedule runs as that person. An optional `id` must match that person. `{ type: "agent" }` selects the schedules the agent owns, which run as the agent's service identity.

**cron** `string`

A five-field cron expression for a recurring schedule. Give exactly one of `cron` and `at`.

**at** `datetime | str`

A `datetime` with a time zone, or an ISO 8601 timestamp that ends with `Z` or a UTC offset. The schedule runs once. The runtime rounds it up to the next whole minute. It must be at least one minute and at most 365 days in the future.

**timezone** `string` (default: UTC)

An IANA time zone for `cron`, such as `America/Los_Angeles`. Do not pass it with `at`.

**prompt** `string`

A prompt that each run receives as a user message. Give exactly one of `prompt` and `input`.

**input** `object | object[]`

A structured LangGraph input for each run.

**new\_thread** `bool`

`True` starts each run on a new thread. `False` continues the current thread. Defaults to `True` with `cron` and `False` with `at`.

**paused** `boolean` (default: false)

Create the schedule without running it.

**metadata** `object`

JSON metadata for your own use. Keys that start with `mda_` are reserved.

### Manage schedules

`list`, `get`, `update`, and `delete` on `runtime.schedules` cover the rest of a schedule's life. Expose them as tools when the agent should manage the schedules it created. An agent with `list` and `delete` can answer "what reminders do I have?" and cancel one on request. Pause a schedule with `update` instead of deleting it when the person wants it back later.

```python
owner = {"type": "user"}

page = await runtime.schedules.list(owner=owner, limit=20)
item = await runtime.schedules.get(page["items"][0]["id"], owner=owner)
await runtime.schedules.update(item["id"], {"paused": True}, owner=owner)
await runtime.schedules.delete(item["id"], owner=owner)
```

`update` accepts `cron`, `at`, `timezone`, `prompt`, `input`, `paused`, and `metadata`. The channel and the thread choice are fixed at creation. `list` hides expired one-time schedules unless you pass `include_expired=True`. For the agent owner, `list` and `get` also return the schedules in `schedules/`, which you change in code.

### Schedule limits

Each owner can have at most 20 runtime schedules per agent. Paused schedules count. Expired one-time schedules and schedules in `schedules/` do not count. A create or update past the limit fails with `Schedule limit reached`.

To change the limit, set these variables in the deployment environment:

| Variable | Limit for |
| - | - |
| `MDA_MAX_AGENT_SCHEDULES` | Schedules owned by the agent |
| `MDA_MAX_USER_SCHEDULES` | Schedules owned by each user |

> [!NOTE]
>
> Schedule limits require `managed-deepagents>=0.9.3`.

## Troubleshoot schedules

* `must export a named schedule declaration`: Define a top-level `schedule` in each file in `schedules/`.

* `must define exactly one of prompt or input`: Add either `prompt` or `input`, but not both.

* `cron must be a standard 5-field expression`: Use five cron fields, not seconds-based cron syntax.

* `schedule is not static`: Replace computed values with literals or top-level literal constants.

* `failed to create cron for schedule`: Open the deployment URL in LangSmith and confirm the deployed Agent Server is healthy.

* `schedule '<name>' persistent thread id must be a UUID`: A persistent schedule declares a thread ID that is not a UUID. Earlier versions report `Invalid thread ID: must be a UUID (HTTP 422)` from the Agent Server. Replace it with a UUID, or omit `id`. See [Choose thread behavior](#choose-thread-behavior).

* `Schedule limit reached`: The owner has reached the runtime schedule limit. Delete a schedule, or raise the limit. See [Schedule limits](#schedule-limits).

* **A schedule does not run during local development**: Confirm that you did not pass `--no-schedules` to `mda dev`. See [Test schedules locally](#test-schedules-locally).

## Next steps

> [card] [Deploy an agent](../Build%20and%20deploy/Deploy%20a%20Managed%20Deep%20Agent.md)
>
> Deploy and reconcile schedule changes.

> [card] [Paid media agent template](../Templates/Deploy%20the%20open-source%20paid%20media%20agent.md)
>
> A full project with weekly and monthly report schedules.

> [card] [CLI reference](../Build%20and%20deploy/Managed%20Deep%20Agents%20CLI%20reference.md)
>
> Look up `mda deploy` flags and troubleshooting.
