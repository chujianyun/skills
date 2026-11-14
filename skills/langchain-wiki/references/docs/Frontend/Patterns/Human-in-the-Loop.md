# Human-in-the-Loop

> Add approval workflows with interrupt-based human review

Not every agent action should run unsupervised. When an agent is about to send
an email, delete a record, execute a financial transaction, or perform any
irreversible operation, you need a human to review and approve the action first.
The Human-in-the-Loop (HITL) pattern lets your agent pause execution, present
the pending action to the user, and resume only after explicit approval.

Because HITL is built on LangGraph interrupts and checkpoints, the pause is
durable. A user can refresh the page, a reviewer can answer from a different
component, and the agent still resumes from the exact point where execution
stopped instead of replaying the whole run.

> [!NOTE]
>
> This page uses the default batched interrupt mode. For per-call interrupts (`interrupt_mode="per_call"`), see [Pause once per tool call](../../Advanced%20usage/Human-in-the-loop.md#pause-once-per-tool-call).

## How interrupts work

LangGraph agents support **interrupts**, explicit pause points where the agent
yields control back to the client. When the agent hits an interrupt:

1. The agent stops executing and emits an interrupt payload
2. The [`useStream`](https://reference.langchain.com/javascript/langchain-react/index/useStream) hook surfaces the interrupt via `stream.interrupt`
3. Your UI renders a review card with approve/reject/edit options
4. The user makes a decision
5. Your code calls `stream.submit()` with a resume command
6. The agent picks up where it left off

The frontend SDK keeps the interrupt alongside the rest of the thread state, so
your UI can render it wherever it makes sense: inline in the transcript, in a
review queue, in an admin dashboard, or in a modal that blocks the next user
action until the decision is made.

## Setting up `useStream`

Connect [`useStream`](https://reference.langchain.com/javascript/langchain-react/index/useStream) to your human-in-the-loop agent. When the graph hits an
interrupt, the hook exposes the pending payload on `stream.interrupt`. Render an
approval card while that value is set, then resume the run with
`stream.submit(null, { command: { resume: response } })` after the user
approves, rejects, or edits the action.

> [!NOTE]
>
> The code examples use `useStream<typeof myAgent>` for type-safe stream state. See Type inference for [Python](../Overview.md#type-inference) or [JavaScript](https://docs.langchain.com/oss/javascript/langchain/frontend/overview.md#type-inference) backends.

```tsx React
import { useStream } from "@langchain/react";

const AGENT_URL = "http://localhost:2024";

export function Chat() {
  const stream = useStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "human_in_the_loop",
  });

  const interrupt = stream.interrupt;

  return (
    <div>
      {stream.messages.map((msg) => (
        <Message key={msg.id} message={msg} />
      ))}
      {interrupt && (
        <ApprovalCard
          interrupt={interrupt}
          onRespond={(response) =>
            stream.submit(null, { command: { resume: response } })
          }
        />
      )}
    </div>
  );
}
```

```vue Vue
<script setup lang="ts">
import { useStream } from "@langchain/vue";

const AGENT_URL = "http://localhost:2024";

const stream = useStream<typeof myAgent>({
  apiUrl: AGENT_URL,
  assistantId: "human_in_the_loop",
});

function handleRespond(response: HITLResponse) {
  stream.submit(null, { command: { resume: response } });
}
</script>

<template>
  <div>
    <Message
      v-for="msg in stream.messages.value"
      :key="msg.id"
      :message="msg"
    />
    <ApprovalCard
      v-if="stream.interrupt.value"
      :interrupt="stream.interrupt.value"
      @respond="handleRespond"
    />
  </div>
</template>
```

```svelte Svelte
<script lang="ts">
  import { useStream } from "@langchain/svelte";

  const AGENT_URL = "http://localhost:2024";

  const stream = useStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "human_in_the_loop",
  });

  function handleRespond(response: HITLResponse) {
    stream.submit(null, { command: { resume: response } });
  }
</script>

<div>
  {#each stream.messages as msg (msg.id)}
    <Message message={msg} />
  {/each}

  {#if stream.interrupt}
    <ApprovalCard interrupt={stream.interrupt} onRespond={handleRespond} />
  {/if}
</div>
```

```ts Angular
import { Component } from "@angular/core";
import { injectStream } from "@langchain/angular";
import type { HITLResponse } from "langchain";

const AGENT_URL = "http://localhost:2024";

@Component({
  selector: "app-chat",
  template: `
    @for (msg of stream.messages(); track msg.id) {
      <app-message [message]="msg" />
    }
    @if (stream.interrupt()) {
      <app-approval-card
        [interrupt]="stream.interrupt()"
        (respond)="handleRespond($event)"
      />
    }
  `,
})
export class ChatComponent {
  stream = injectStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "human_in_the_loop",
  });

  handleRespond(response: HITLResponse) {
    this.stream.submit(null, { command: { resume: response } });
  }
}
```

## The interrupt payload

When the agent pauses, `stream.interrupt` contains a [HITLRequest](https://reference.langchain.com/python/langchain/agents/middleware/human_in_the_loop/HITLRequest) with the
following structure:

```ts
interface HITLRequest {
  actionRequests: ActionRequest[];
  reviewConfigs: ReviewConfig[];
}

interface ActionRequest {
  name: string;
  args: Record<string, unknown>;
  description?: string;
}

interface ReviewConfig {
  allowedDecisions: ("approve" | "reject" | "edit" | "respond")[];
}
```

| Property | Description |
| - | - |
| `actionRequests` | Array of pending actions the agent wants to perform |
| `actionRequests[].name` | The action name (e.g. `"send_email"`, `"delete_record"`) |
| `actionRequests[].args` | Structured arguments for the action |
| `actionRequests[].description` | Optional human-readable description of what the action does |
| `reviewConfigs` | Per-action configuration controlling which decisions are allowed |
| `reviewConfigs[].allowedDecisions` | Which buttons to show: `"approve"`, `"reject"`, `"edit"`, `"respond"` |

## Decision types

The HITL pattern supports four decision types:

### Approve

The user confirms the action should proceed as-is:

```ts
const response: HITLResponse = {
  decisions: [{ type: "approve" }],
};

stream.submit(null, { command: { resume: response } });
```

### Reject

The user denies the action with an optional reason. The tool is not executed:

```ts
const response: HITLResponse = {
  decisions: [
    {
      type: "reject",
      message: "The email tone is too aggressive. Do not send it.",
    },
  ],
};

stream.submit(null, { command: { resume: response } });
```

> [!NOTE]
>
> When an action is rejected, the agent receives the rejection reason and can
> decide how to proceed. If you omit `message`, the backend uses a default
> message that tells the model the tool was not executed and not to retry the
> same tool call unless the user asks. For side-effecting tools, pass a clear
> message that tells the agent whether to abandon the action, ask a follow-up
> question, or try a safer alternative.

### Edit

The user modifies the action's arguments before approving:

```ts
const response: HITLResponse = {
  decisions: [
    {
      type: "edit",
      editedAction: {
        name: actionRequest.name,
        args: {
          ...actionRequest.args,
          subject: "Updated subject line",
          body: "Revised email body with softer language.",
        },
      },
    },
  ],
};

stream.submit(null, { command: { resume: response } });
```

### Respond

The user provides a direct reply for "ask user" style tools. The `message` becomes the tool result and the tool itself is not executed:

```ts
const response: HITLResponse = {
  decisions: [{ type: "respond", message: "Blue." }],
};

stream.submit(null, { command: { resume: response } });
```

> [!NOTE]
>
> Use `respond` when the tool is intentionally a placeholder for human input, for example, an `ask_user` tool that prompts the agent to collect information from the user. Do not use `respond` to deny a proposed action, because it is returned to the model as a successful tool result.

## Building the ApprovalCard

Here is the decision wiring used by the approval cards. The UI can split each
action into its own card, but the resume payload is a single `HITLResponse`
with one decision per pending action:

```tsx
async function approveAll() {
  const resume: HITLResponse = {
    decisions: actionRequests.map(() => ({ type: "approve" })),
  };
  await stream.submit(null, { command: { resume } });
}

async function rejectOne(index: number, message: string) {
  const resume: HITLResponse = {
    decisions: actionRequests.map((_, i) =>
      i === index
        ? { type: "reject", message }
        : { type: "reject", message: "Rejected along with other actions" },
    ),
  };
  await stream.submit(null, { command: { resume } });
}

async function editOne(index: number, editedArgs: Record<string, unknown>) {
  const originalAction = actionRequests[index];
  const resume: HITLResponse = {
    decisions: actionRequests.map((_, i) =>
      i === index
        ? {
            type: "edit",
            editedAction: { name: originalAction.name, args: editedArgs },
          }
        : { type: "approve" },
    ),
  };
  await stream.submit(null, { command: { resume } });
}
```

## The resume flow

After the user makes a decision, the full cycle looks like this:

1. Call `stream.submit(null, { command: { resume: hitlResponse } })`
2. The [`useStream`](https://reference.langchain.com/javascript/langchain-react/index/useStream) hook sends the resume command to the LangGraph backend
3. The agent receives the `HITLResponse` and continues execution. Each entry in
   `decisions` may be one of:
   * `{ type: "approve" }`: The agent continues executing the action
   * `{ type: "reject", message }`: The tool is not executed, and the agent receives the rejection message before deciding its next step
   * `{ type: "edit", editedAction }`: The agent runs the tool with edited arguments
   * `{ type: "respond", message }`: The human's message is returned directly as the tool result without executing the tool
4. The `interrupt` property resets to `null` as the agent resumes streaming

> [!TIP]
>
> You can chain multiple HITL checkpoints in a single agent run. For example, an
> agent might ask for approval to search, then ask again before sending an email
> with the results. Each interrupt is handled independently.

## Handling multiple pending actions

An interrupt can contain multiple `actionRequests` when the agent wants to
perform several actions at once. Render a card for each and collect all
decisions before resuming:

```tsx
function MultiActionReview({
  interrupt,
  onRespond,
}: {
  interrupt: { value: HITLRequest };
  onRespond: (response: HITLResponse) => void;
}) {
  const [decisions, setDecisions] = useState<Record<number, HITLResponse["decisions"][number]>>({});
  const request = interrupt.value;

  const allDecided =
    Object.keys(decisions).length === request.actionRequests.length;

  return (
    <div className="space-y-4">
      {request.actionRequests.map((action, i) => (
        <SingleActionCard
          key={i}
          action={action}
          config={request.reviewConfigs[i]}
          onDecide={(response) =>
            setDecisions((prev) => ({ ...prev, [i]: response }))
          }
        />
      ))}
      {allDecided && (
        <button
          className="rounded bg-green-600 px-4 py-2 text-white"
          onClick={() =>
            onRespond({
              decisions: request.actionRequests.map((_, i) => decisions[i]),
            })
          }
        >
          Submit All Decisions
        </button>
      )}
    </div>
  );
}
```

## Custom interrupt forms

The [resume flow](#the-resume-flow) uses `humanInTheLoopMiddleware`, which wraps a tool with a
generic approve / reject / edit / respond card. Sometimes a single set of
buttons is not enough: booking a flight, approving a refund, and reviewing a
social post each need a *different* form, with their own fields, validation, and
copy. For that, raise the `interrupt()` **from inside the tool** and let the
payload describe the exact form the UI should render. Each tool can surface a
completely different interface.

### Describe the form in the interrupt payload

`interrupt()` accepts any JSON-serializable value, which allows you to provide a "card"
that the frontend knows how to render, for example, a form type, a title, the context the
human is reviewing, and the fields to collect. `interrupt()` is generic over its
input and return types (`interrupt<I, R>(value: I): R`) so you can type both
the card you send (`InterruptCard`) and the value the user resolves with
(`ReviewDecision`). Export those types so the frontend can import them and stay
in sync:

```ts
import { createAgent, tool } from "langchain";
import { interrupt } from "@langchain/langgraph";
import { z } from "zod";

export interface FormField {
  name: string;
  label: string;
  type: "select" | "checkbox" | "textarea" | "currency";
  options?: string[];
  default?: unknown;
}

/** What the user resolves the interrupt with. */
export interface ReviewDecision {
  approved: boolean;
  /** Edited / collected form values the tool should act on. */
  values?: Record<string, unknown>;
}

/** The form spec ("card") an interrupt hands to the frontend. */
export interface InterruptCard {
  formType: "flight-booking" | "refund-approval" | "content-review";
  tool: string;
  title: string;
  context: Record<string, unknown>;
  fields: FormField[];
  /** Populated by the frontend when it commits the resolved card to state. */
  resolved?: boolean;
  decision?: ReviewDecision;
}

const bookFlight = tool(
  async ({ origin, destination, date, passengers }) => {
    // Pause the tool and hand the frontend a typed form spec; the typed return
    // is whatever the UI resolves the interrupt with.
    const decision = interrupt<InterruptCard, ReviewDecision>({
      formType: "flight-booking",
      tool: "book_flight",
      title: "Confirm flight booking",
      context: { origin, destination, date, passengers },
      fields: [
        {
          name: "seatClass",
          label: "Seat class",
          type: "select",
          options: ["Economy", "Premium Economy", "Business"],
          default: "Economy",
        },
        { name: "insurance", label: "Add trip insurance", type: "checkbox", default: false },
      ],
    });

    if (!decision.approved) {
      return `Booking cancelled. No flight from ${origin} to ${destination} was reserved.`;
    }

    // Run the real (possibly slow) work with the values the human confirmed.
    const seatClass = String(decision.values?.seatClass ?? "Economy");
    return `Flight booked from ${origin} to ${destination} in ${seatClass}.`;
  },
  {
    name: "book_flight",
    description: "Book a flight. Requires human confirmation of trip details.",
    schema: z.object({
      origin: z.string(),
      destination: z.string(),
      date: z.string(),
      passengers: z.number().int().min(1),
    }),
  },
);
```

Give each tool a distinct `formType` (e.g. `"refund-approval"`,
`"content-review"`) so the frontend can switch on it and render the matching
form.

### Render a different form per tool

On the client, the card arrives as `stream.interrupt.value`. Import the
`InterruptCard` and `ReviewDecision` types from your agent module so the form
and the payload stay in sync, switch on `formType` to pick the right form, and
feed `fields` into your inputs:

```tsx
import { useStream } from "@langchain/react";
import type { InterruptCard, ReviewDecision } from "./agent";

function Chat() {
  const stream = useStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "hitl_interrupt_forms",
  });

  const card = stream.interrupt?.value as InterruptCard | undefined;

  return (
    <div>
      {stream.messages.map((msg) => (
        <Message key={msg.id} message={msg} />
      ))}
      {card && <InterruptForm card={card} onResolve={handleResolve} />}
    </div>
  );
}

// `InterruptForm` renders a flight / refund / content card based on
// `card.formType`, collects `card.fields`, and calls `onResolve` with the
// user's decision and edited values.
```

### Keep the card on screen with `respond(decision, { update })`

When you resolve a plain interrupt, the card disappears the instant the
interrupt clears and only the tool result comes back. That means a rich review card
would vanish mid-run. To keep it on screen, resolve the interrupt **and** commit
a message carrying the card to state in the *same* superstep using
[`useStream`](https://reference.langchain.com/javascript/langchain-react/index/useStream)'s `respond`:

```tsx
import { AIMessage } from "langchain";

function handleResolve(decision: ReviewDecision) {
  // Snapshot the card with the decision baked in so it renders read-only.
  const resolvedCard = { ...card, resolved: true, decision };
  const cardMessage = new AIMessage({
    content: `Review ${decision.approved ? "approved" : "declined"}.`,
    response_metadata: { cards: resolvedCard },
  });

  // Resume the interrupt AND push the card into state atomically. Maps to
  // LangGraph's `Command(resume, update)`: one checkpoint, no extra state write.
  stream.respond(decision, { update: { messages: [cardMessage] } });
}
```

`respond(response, { update })` applies the `update` **optimistically**: the
card paints immediately and is reconciled by ID once the resumed run echoes the
same message back. The backend never re-emits the card, so it stays rendered
without a flicker while the (potentially slow) tool runs. Render the resolved
card by reading it back off the message:

```tsx
{stream.messages.map((msg) => {
  const card = (msg.response_metadata as { cards?: InterruptCard })?.cards;
  if (card) return <InterruptForm key={msg.id} card={card} readOnly />;
  return <Message key={msg.id} message={msg} />;
})}
```

> [!TIP]
>
> Because the resolved card lives in the message history, it survives refreshes
> and is visible to every component reading the thread and the human's decision
> becomes part of the durable transcript, not just transient UI state.

## Best practices

Keep these guidelines in mind when implementing HITL workflows:

* **Show clear context**. Always display *what* the agent wants to do and
  *why*. Include the action description and the full arguments.
* **Make approve the easiest path**. If the action looks correct, approving
  should be a single click. Reserve multi-step flows for reject/edit.
* **Validate edited args**. When users edit action arguments, validate the
  JSON structure before sending. Show inline errors for malformed input.
* **Persist the interrupt state**. If the user refreshes the page, the
  interrupt should still be visible. [`useStream`](https://reference.langchain.com/javascript/langchain-react/index/useStream) handles this via the thread's
  checkpoint.
* **Log all decisions**. For audit trails, log every approve/reject/edit
  decision with timestamps and the user who made the decision.
* **Set timeouts thoughtfully**. Long-running agents should not block
  indefinitely on human review. Consider showing how long the agent has been
  waiting.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/frontend/human-in-the-loop.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
