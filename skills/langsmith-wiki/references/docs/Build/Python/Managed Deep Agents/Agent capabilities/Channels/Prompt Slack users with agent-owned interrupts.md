# Prompt Slack users with agent-owned interrupts

> Post a Slack form from a Managed Deep Agents tool, pause the run, and resume it when the user submits the form.

An agent-owned interrupt is a pause that your own code creates. A tool posts a Slack message or modal that you design in [Block Kit](https://api.slack.com/block-kit), then calls `interrupt()`. When the user presses a button or submits the modal, Managed Deep Agents delivers the answer to the deployment as a `user_prompt_response` channel event and resumes the paused run with it. You can ask a user for structured input mid-run, such as an approval, a choice, or a set of form fields, without building a Slack app or a webhook of your own.

This differs from the platform-owned interrupts that `interrupt_on` creates. Those pause before a tool call, and Slack or Studio renders the approval card for you. With an agent-owned interrupt, you own the blocks, the form state, and what happens after the answer arrives. The platform only carries the answer back. For platform-owned interrupts, see [Human-in-the-loop](../Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md#human-in-the-loop).

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

> [!NOTE]
>
> Agent-owned interrupts require `managed-deepagents>=0.8.0` and a [Slack channel](Connect%20a%20Managed%20Deep%20Agent%20to%20Slack.md) on a deployed agent. Forms render only in Slack. LangSmith Studio shows the raw interrupt value.

## How it works

1. A run starts from a Slack message. Your tool reads the conversation from `runtime.thread.origin.channel` and posts a Block Kit message into the same Slack thread, using the deployment's bot token.
2. The tool calls `interrupt()` with a value that carries a correlation ID. The thread parks at a checkpoint.
3. The user presses a button or submits a modal. Slack sends the interaction to Managed Deep Agents, which forwards it to the deployment as a `user_prompt_response` event.
4. The SDK matches the event to the parked interrupt and resumes the run. `interrupt()` returns the user's response, and the tool continues.

A tool that pauses this way runs again from the top when the run resumes, which is standard LangGraph interrupt behavior. Guard the post so it happens only once. See [Post a form and pause](#post-a-form-and-pause).

## Post a form and pause

The tool needs three things: the Slack conversation to post into, the bot token, and a correlation ID that ties the form to the interrupt.

* **Conversation**: `runtime.thread.origin.channel.raw_event` is the Slack event that started the run. It carries `channel`, `ts`, and, for a threaded message, `thread_ts`. Post into that thread so the answer routes back to the same agent thread.
* **Bot token**: `connections.get("mda/slack-bot-token", {"type": "agent"})` resolves the token of the Slack app that Managed Deep Agents provisioned for the deployment. The slug is reserved and cannot be created with `mda connections create`.
* **Correlation ID**: put the same string under `INTERRUPT_CORRELATION_KEY` in each button's `value` (as JSON) and in the value you pass to `interrupt()`.

The built-in Slack channel's `post` sends text only, so post Block Kit through the Slack Web API directly.

```python tools/approval.py expandable
import json
from langsmith import uuid7
import httpx
from langchain.tools import tool
from langgraph.types import interrupt
from managed_deepagents import (
    INTERRUPT_CORRELATION_KEY,
    ManagedDeepAgentRuntime,
    connections,
)


@tool(parse_docstring=True)
async def request_approval(amount: str, runtime: ManagedDeepAgentRuntime) -> str:
    """Ask the requester to approve or decline a spend.

    Args:
        amount: The spend to approve, such as "$1,200".
    """
    origin = runtime.thread.origin
    if origin is None or origin.channel.provider != "slack":
        return "Approval forms are available only in Slack."
    channel = origin.channel

    correlation_id = str(uuid7())
    # The tool runs again when the interrupt resumes. Post only in the run the Slack message started.
    if channel.event is not None and channel.event["type"] == "message":
        await post_approval_form(channel.raw_event, amount, correlation_id)

    response = interrupt({INTERRUPT_CORRELATION_KEY: correlation_id, "amount": amount})
    return f"The requester chose {response['action']} for {amount}."


async def post_approval_form(raw_event: dict, amount: str, correlation_id: str) -> None:
    bot_token = await connections.get("mda/slack-bot-token", {"type": "agent"})
    value = json.dumps({INTERRUPT_CORRELATION_KEY: correlation_id})
    blocks = [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"Approve a spend of *{amount}*?"},
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "action_id": "approve_spend",
                    "text": {"type": "plain_text", "text": "Approve"},
                    "value": value,
                },
                {
                    "type": "button",
                    "action_id": "decline_spend",
                    "text": {"type": "plain_text", "text": "Decline"},
                    "value": value,
                },
            ],
        },
    ]
    async with httpx.AsyncClient(timeout=30.0) as client:
        result = await client.post(
            "https://slack.com/api/chat.postMessage",
            headers={"Authorization": f"Bearer {bot_token}"},
            json={
                "channel": raw_event["channel"],
                "thread_ts": raw_event.get("thread_ts") or raw_event["ts"],
                "text": f"Approve a spend of {amount}?",
                "blocks": blocks,
            },
        )
        body = result.json()
        if not body.get("ok"):
            raise RuntimeError(f"Slack rejected the form: {body.get('error')}")
```

Register the tool in the agent definition as you would any other [custom tool](../Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md). The interrupt inherits the managed checkpointer, so no extra persistence setup is needed.

Any `action_id` works for a button in a message, except one that starts with `mda_modal::`. That prefix opens a modal instead. See [Open a modal](#open-a-modal).

## Read the response

`interrupt()` returns the normalized response. It holds only the fields every provider shares:

| Field | Type | Meaning |
| - | - | - |
| `provider` | `"slack"` | The channel provider that delivered the answer. |
| `action` | `string` | The button's `action_id`, or the modal's `callback_id`. |
| `value` | JSON, optional | The button's `value` string, or the modal's `state.values` object. Opaque to the platform. |
| `correlation_id` | `string`, optional | Present when the button's `value` was JSON with an `mda_correlation_id` key. Modal submissions never carry one. |

The same response is available on run context as `runtime.thread.origin.channel.event`, with `type` set to `user_prompt_response`. Slack's verbatim interaction payload is on `runtime.thread.origin.channel.raw_event`. For a form with inputs inside the message, the user's entries are at `raw_event["state"]["values"]`, keyed by block ID and action ID.

Managed Deep Agents reads only the first action in a Slack interaction payload, so one press must mean one event.

## How a response finds its interrupt

Slack does not know which interrupt a button belongs to, so the SDK reads the interrupts parked on the thread and decides:

| Parked interrupts | `correlation_id` on the response | Result |
| - | - | - |
| One | Absent | Resumes that interrupt. |
| One or more | Present and matches exactly one | Resumes the matching interrupt. |
| Several | Absent | Nothing runs. The SDK logs the ambiguity and acknowledges the event. |
| One or more | Present but matches none, or matches several | Nothing runs. Starting a turn would abandon the parked checkpoints. |
| None | Any | Starts a fresh run with no new message. The response is reachable only on `runtime.thread.origin.channel.event`. |

Carry a correlation ID whenever an agent might have more than one interrupt parked on a thread. Without one, a thread can only be answered while exactly one interrupt is pending.

## Open a modal

A modal gives you more room than a message and supports the full set of Block Kit input elements. Slack calls a modal a view. You author the view, and Managed Deep Agents opens it.

Slack issues a single-use `trigger_id` with each click that expires in about three seconds, and it is the only authorization to open a modal. Forwarding the click to the deployment and waiting for a run would miss that window, so Managed Deep Agents opens the view itself from content already in the click. The agent is not told about the click.

To open a modal, post a button whose `action_id` starts with `mda_modal::` and whose `value` is the complete view as JSON:

```json
{
  "type": "button",
  "action_id": "mda_modal::approve_spend",
  "text": { "type": "plain_text", "text": "Review" },
  "value": "{\"type\":\"modal\",\"title\":{\"type\":\"plain_text\",\"text\":\"Approve spend\"},\"submit\":{\"type\":\"plain_text\",\"text\":\"Submit\"},\"blocks\":[...]}"
}
```

When the user presses submit, the deployment receives a `user_prompt_response` with `action` set to the view's `callback_id`, which equals the button's `action_id`, and `value` set to the view's `state.values`. The modal then closes.

Two fields on the view belong to the platform:

* **`callback_id`**: Set to the button's `action_id` so the submission is identifiable.
* **`private_metadata`**: Holds the encrypted channel and thread the modal was opened from. A modal submission carries no channel or thread, so this is the only route back to the conversation. If your view already sets `private_metadata`, the modal does not open.

Every other field goes to Slack exactly as you wrote it. Managed Deep Agents does not validate the view, so a view that Slack rejects shows the user nothing.

Modal submissions never carry a `correlation_id`. A modal can answer a thread only while exactly one interrupt is parked.

The entire view has to fit inside the button's `value`, which Slack caps at 2000 characters. Slack rejects an oversized button when the tool posts the message, so the failure surfaces in the tool call rather than at click time.

## Post without pausing

A tool can post a form and let the run end instead of calling `interrupt()`. The submission then starts a fresh run with no new message, and your code reads the answer from `runtime.thread.origin.channel.event`. Nothing on the platform tracks that a prompt was outstanding, so your application owns the state of pending forms, expiry, and what a later chat message means while a form is open.

Prefer `interrupt()` when the next thing the user does is expected to be answering the prompt.

## Limits and reserved names

Names the platform reserves:

| Name | Where | Meaning |
| - | - | - |
| `mda_modal::` prefix | Button `action_id` | The click opens a modal and never reaches the agent. |
| `mda_correlation_id` | Key inside a button `value` | Matches a click to one parked interrupt. Exported as `INTERRUPT_CORRELATION_KEY`. |
| `callback_id` | App-defined view | Set to the button's `action_id`. |
| `private_metadata` | App-defined view | Set by the platform. Supplying it prevents the modal from opening. |
| `mda/slack-bot-token` | Connection slug | The deployment's Slack bot token. Cannot be created or overwritten with the CLI. |

Slack limits that Managed Deep Agents does not check before forwarding a view:

| Limit | Value |
| - | - |
| Button `value` | 2000 characters |
| Modal title | 24 characters |
| Blocks per view | 100 |
| `callback_id` | 255 characters |

Exceeding the last three makes the modal fail to open with nothing shown to the user.

## Understand failure modes

* **The modal does not open.** The view JSON is malformed, exceeds a Slack limit, or the `trigger_id` expired. The button press does nothing visible in Slack. The failure is logged on the platform.
* **The user dismisses the modal.** The interrupt stays parked. There is no cancel path and no expiry.
* **The user replies in the thread instead of using the form.** The message takes the ordinary message path, which does not consult interrupt state. The run starts with the new message and the parked checkpoint is abandoned, while the card keeps its live buttons.
* **Two people press the same button.** Both interactions are forwarded. The first resumes the interrupt and the second starts a fresh turn. Nothing deduplicates them.
* **Several interrupts are parked and the response has no correlation ID.** Nothing runs. Because modal submissions never carry a correlation ID, a modal cannot answer a thread with two parked interrupts.
* **A submission cannot return a `response_action`.** There are no per-field validation errors, no chained modals, and no in-place modal update.

## See also

* [Human-in-the-loop](../Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md#human-in-the-loop): pause before selected tool calls with platform-rendered approval cards.
* [Connect a Managed Deep Agent to Slack](Connect%20a%20Managed%20Deep%20Agent%20to%20Slack.md): add the Slack channel that delivers form responses.
* [Manage connections](../Manage%20connections.md): how `connections.get(...)` resolves agent-owned credentials.
* [Add custom tools](../Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md): register the tool that posts the form.
