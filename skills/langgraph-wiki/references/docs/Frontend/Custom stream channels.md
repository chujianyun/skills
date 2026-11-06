# Custom stream channels

> Stream custom server-side data to the frontend and read it with useExtension and useChannel

LangGraph agents stream more than messages and tool calls. A server-side
**stream transformer** can inspect or rewrite the protocol as it flows to the
client and publish its own structured data on a named **custom channel**. The
frontend reads that channel with two selectors: [`useExtension`](https://reference.langchain.com/javascript/langchain-react/useExtension) for the latest
payload, and [`useChannel`](https://reference.langchain.com/javascript/langchain-react/useChannel) as a raw-events escape hatch.

The example below is a customer-support agent whose transformer redacts PII
(emails, phone numbers, SSNs, card numbers, IPs) from every event before it
reaches the browser, and publishes running redaction counts on a
`redaction-stats` channel. The side panel renders those counts live.

## How custom channels work

A custom channel has two ends. On the server, a [`StreamTransformer`](https://reference.langchain.com/python/langgraph/stream/_types/StreamTransformer) opens a
named [`StreamChannel`](https://reference.langchain.com/python/langgraph/stream/stream_channel/StreamChannel) and pushes payloads onto it. On the client, a selector
subscribes to the matching `custom:<name>` channel and exposes the payloads as
reactive state.

The transformer's `process` method runs for every protocol event. It can mutate
the event in place (here, scrubbing PII from `messages`, `tools`, and `values`
data) and push side-channel updates whenever it has something to report.

The client-side selectors (`useExtension`, `useChannel`) ship with the v1
frontend SDK packages (`@langchain/react`, `@langchain/vue`,
`@langchain/svelte`, `@langchain/angular`).

> [!NOTE]
>
> Stream transformers and `StreamChannel` require `langgraph>=1.2`.

```python
import time

from langgraph.stream import ProtocolEvent, StreamChannel, StreamTransformer


class RedactionStatsTransformer(StreamTransformer):
    def __init__(self, scope: tuple[str, ...] = ()) -> None:
        super().__init__(scope)
        # Open a channel named "redaction-stats".
        self.redaction_stats = StreamChannel("redaction-stats")
        self.counts = empty_counts()

    def init(self) -> dict[str, StreamChannel]:
        return {"redactionStats": self.redaction_stats}

    def process(self, event: ProtocolEvent) -> bool:
        # Redact event["params"]["data"] in place and tally what was found.
        delta = redact_in_place(event, self.counts)
        if delta:
            # Publish a payload on the channel.
            self.redaction_stats.push(
                {
                    "kind": "update",
                    "at": int(time.time() * 1000),
                    "delta": delta,
                    "counts": dict(self.counts),
                    "total": sum(self.counts.values()),
                }
            )
        return True  # Keep the (now-redacted) event in the stream.


def create_redaction_stats_transformer() -> RedactionStatsTransformer:
    return RedactionStatsTransformer()
```

Attach the transformer when you build the agent:

```python
from langchain.agents import create_agent

agent = create_agent(
    model="anthropic:claude-haiku-4-5",
    tools=[...],
    transformers=[create_redaction_stats_transformer],
)
```

The payload type is whatever the transformer pushes. The client examples below
read this shape:

```ts
type PiiType = "email" | "phone" | "ssn" | "credit_card" | "ip_address";

type RedactionStatsEvent = {
  kind: "update";
  at: number;
  delta: Partial<Record<PiiType, number>>;
  counts: Record<PiiType, number>;
  total: number;
};
```

## Setting up `useStream`

Wire up [`useStream`](https://reference.langchain.com/javascript/langchain-react/index/useStream) as usual. The custom-channel selectors take the same
`stream` handle returned here.

> [!NOTE]
>
> The code examples use `useStream<typeof myAgent>` for type-safe stream state. See Type inference for [Python](https://docs.langchain.com/oss/python/langchain/frontend/overview.md#type-inference) or [JavaScript](https://docs.langchain.com/oss/javascript/langchain/frontend/overview.md#type-inference) backends.

```tsx React
import { useStream } from "@langchain/react";

const AGENT_URL = "http://localhost:2024";

export function RedactionChat() {
  const stream = useStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "custom_stream_channel",
  });

  return <RedactionStatsPanel stream={stream} />;
}
```

```vue Vue
<script setup lang="ts">
import { useStream } from "@langchain/vue";

const AGENT_URL = "http://localhost:2024";

const stream = useStream<typeof myAgent>({
  apiUrl: AGENT_URL,
  assistantId: "custom_stream_channel",
});
</script>

<template>
  <RedactionStatsPanel :stream="stream" />
</template>
```

```svelte Svelte
<script lang="ts">
  import { useStream } from "@langchain/svelte";

  const AGENT_URL = "http://localhost:2024";

  const stream = useStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "custom_stream_channel",
  });
</script>

<RedactionStatsPanel {stream} />
```

```ts Angular
import { Component } from "@angular/core";
import { injectStream } from "@langchain/angular";

const AGENT_URL = "http://localhost:2024";

@Component({
  selector: "app-redaction-chat",
  template: `<app-redaction-stats-panel [stream]="stream" />`,
})
export class RedactionChatComponent {
  stream = injectStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "custom_stream_channel",
  });
}
```

## Read the latest payload with `useExtension`

`useExtension` subscribes to a `custom:<name>` channel and returns the most
recent payload the transformer pushed, already unwrapped and typed. It is the
ergonomic choice when the UI only needs the current value, such as a live
counter, progress percentage, or status badge.

Pass the bare channel name (`"redaction-stats"`), not the `custom:` prefix:

```tsx React
import { useExtension } from "@langchain/react";

const latest = useExtension<RedactionStatsEvent>(stream, "redaction-stats");
// latest?.total, latest?.counts.email, latest?.delta
```

```vue Vue
import { useExtension } from "@langchain/vue";

const latest = useExtension<RedactionStatsEvent>(stream, "redaction-stats");
// latest.value?.total
```

```svelte Svelte
import { useExtension } from "@langchain/svelte";

const latest = useExtension<RedactionStatsEvent>(stream, "redaction-stats");
// latest?.total
```

```ts Angular
import { injectExtension } from "@langchain/angular";

const latest = injectExtension<RedactionStatsEvent>(stream, "redaction-stats");
// latest()?.total
```

The return value follows each framework's reactivity model: a plain value in
React and Svelte, a `Ref` in Vue (`latest.value`), and a signal in Angular
(`latest()`). The value is `undefined` until the first payload arrives.

An optional third `target` argument scopes the subscription to a namespace, the
same way `useMessages(stream, node)` scopes messages to a discovered graph node.
See [Graph execution](Graph%20execution.md) for namespace
targeting.

## Buffer raw events with `useChannel`

`useChannel` is the raw-events escape hatch. It subscribes to one or more
channels and returns a bounded buffer of the underlying protocol events rather
than a single unwrapped value. Reach for it when you need history instead of the
latest value, such as an event log or audit trail, or when you need a channel
that no higher-level selector covers.

Pass the full channel id (`"custom:redaction-stats"`):

```tsx React
import { useChannel } from "@langchain/react";

const rawEvents = useChannel(stream, ["custom:redaction-stats"]);
```

```vue Vue
import { useChannel } from "@langchain/vue";

const rawEvents = useChannel(stream, ["custom:redaction-stats"]);
// rawEvents.value
```

```svelte Svelte
import { useChannel } from "@langchain/svelte";

const rawEvents = useChannel(stream, ["custom:redaction-stats"]);
```

```ts Angular
import { injectChannel } from "@langchain/angular";

const rawEvents = injectChannel(stream, ["custom:redaction-stats"]);
// rawEvents()
```

Each entry is a raw protocol event, so the payload sits under
`event.params.data`. Unwrap it yourself:

```ts
function parseRedactionStatsEvents(rawEvents: Event[]): RedactionStatsEvent[] {
  const out: RedactionStatsEvent[] = [];
  for (const event of rawEvents) {
    const data = event.params?.data;
    const payload = data?.payload ?? data;
    if (payload?.kind === "update") out.push(payload);
  }
  return out;
}
```

Control the buffer with the options argument:

```ts
const rawEvents = useChannel(
  stream,
  ["custom:redaction-stats"],
  undefined, // target namespace
  { bufferSize: 200, replay: true },
);
```

| Option | Default | Effect |
| - | - | - |
| `bufferSize` | `"default"` | Maximum number of buffered events. Older events drop once the cap is reached. |
| `replay` | `true` | Replay events already seen on the channel when the selector mounts, instead of only live events. |

> [!NOTE]
>
> Prefer the higher-level selectors (`useExtension`, `useMessages`,
> `useToolCalls`, `useValues`) for common cases. They return typed, unwrapped
> values and track only what you render. Use `useChannel` when you specifically
> need the raw event stream.

## Choosing between `useExtension` and `useChannel`

Both read the same custom channel but differ in what they return:

| | `useExtension` | `useChannel` |
| - | - | - |
| **Returns** | Latest payload (`T \| undefined`) | Bounded buffer of raw events (`Event[]`) |
| **Shape** | Unwrapped, typed payload | Raw protocol events; unwrap `event.params.data` yourself |
| **Subscribe by** | Channel name (`"redaction-stats"`) | Full channel id (`["custom:redaction-stats"]`) |
| **Use when** | You need the current value | You need history, a log, or multiple channels |
| **Options** | — | `bufferSize`, `replay` |

A common pattern is to use both on the same channel: `useExtension` drives a
live summary (current totals), while `useChannel` backs a scrolling event log of
every update across the thread.

## Use cases

Custom channels fit any server-side signal that does not map cleanly to
messages, tool calls, or graph state:

* **Compliance and redaction stats**: counts of scrubbed PII, blocked content,
  or policy hits, as in the example above.
* **Progress reporting**: percentage complete or step labels emitted by a
  long-running tool.
* **Live metrics**: token usage, latency, or cost accumulating during a run.
* **Sources and citations**: retrieved documents pushed to a side panel as the
  agent grounds its answer.
* **Domain events**: any structured update your backend wants to surface
  without changing the message transcript.

## Related

* [Overview](Overview.md) — the LangGraph frontend stream
  API and architecture.
* [Graph execution](Graph%20execution.md) — namespace-scoped
  selectors for multi-node pipelines.
