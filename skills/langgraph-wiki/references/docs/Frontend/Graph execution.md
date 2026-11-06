# Graph execution

> Visualize multi-step graph pipelines with per-node status and streaming content

LangGraph agents aren't black boxes. Every graph is composed of **named nodes**
that execute in sequence or in parallel: classify, research, analyze,
synthesize. Graph execution cards make this pipeline visible by rendering a card
for each node, showing its status, streaming its content in real time, and
tracking completion across the entire workflow. Users see exactly what the agent
is doing, which step it's on, and what each step produced.

This pattern is especially useful for production agents because it turns graph
structure into product UX. Instead of treating the run as a single assistant
response, you can expose the same checkpoints, node names, state keys, and
stream metadata that LangGraph uses internally.

## How graph nodes map to UI cards

A LangGraph graph defines a series of nodes, each responsible for a specific
task. For example, a research pipeline might have:

1. **Classify**: categorize the user's query
2. **Research**: gather relevant information
3. **Analyze**: draw conclusions from the research
4. **Synthesize**: produce a final, polished response

Each node writes its output to a specific key in the graph's state. On the
frontend, you don't need to hardcode that mapping as [`useStream`](https://reference.langchain.com/javascript/langchain-react/index/useStream) discovers
each node as it runs via `stream.subgraphs` and exposes a
[`SubgraphDiscoverySnapshot`](https://reference.langchain.com/javascript/langchain-react/SubgraphDiscoverySnapshot) for every observed step:

```ts
// Nodes are discovered automatically — no hardcoded list needed
const graphNodes = [...stream.subgraphs.values()];

// Each snapshot carries the node name and current status
graphNodes.forEach((node) => {
  console.log(node.nodeName, node.status); // "classify", "running"
});
```

Use `node.nodeName` for labels in the progress bar and card headers. Pass each
snapshot to `useMessages(stream, node)` to render node-scoped streaming content
without coupling the UI to graph state key names.

This mapping becomes the contract between your graph and your UI. Backend
authors can add, rename, or reorder nodes intentionally, while frontend authors
decide how each state key should be visualized: a status badge, markdown panel,
table, chart, trace view, or approval card.

## Setting up `useStream`

Wire up [`useStream`](https://reference.langchain.com/javascript/langchain-react/index/useStream) as usual. The key properties you'll use are `messages`
(for the conversation) and `subgraphs` (for the graph nodes discovered in the
current run). Pass each discovered subgraph snapshot to a selector to read the
messages scoped to that node.

> [!NOTE]
>
> The code examples use `useStream<typeof myAgent>` for type-safe stream state. See Type inference for [Python](https://docs.langchain.com/oss/python/langchain/frontend/overview.md#type-inference) or [JavaScript](https://docs.langchain.com/oss/javascript/langchain/frontend/overview.md#type-inference) backends.

```tsx React
import { useStream } from "@langchain/react";

const AGENT_URL = "http://localhost:2024";

export function PipelineChat() {
  const stream = useStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "graph_execution_cards",
  });
  const graphNodes = [...stream.subgraphs.values()];

  return (
    <div>
      <PipelineProgress nodes={graphNodes} isLoading={stream.isLoading} />
      <NodeCardList nodes={graphNodes} stream={stream} isLoading={stream.isLoading} />
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
  assistantId: "graph_execution_cards",
});
</script>

<template>
  <div>
    <PipelineProgress
      :nodes="[...stream.subgraphs.value.values()]"
      :is-loading="stream.isLoading.value"
    />
    <NodeCardList
      :nodes="[...stream.subgraphs.value.values()]"
      :stream="stream"
      :is-loading="stream.isLoading.value"
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
    assistantId: "graph_execution_cards",
  });
</script>

<div>
  <PipelineProgress nodes={[...stream.subgraphs.values()]} isLoading={stream.isLoading} />
  <NodeCardList
    nodes={[...stream.subgraphs.values()]}
    {stream}
    isLoading={stream.isLoading}
  />
</div>
```

```ts Angular
import { Component, computed } from "@angular/core";
import { injectStream } from "@langchain/angular";

const AGENT_URL = "http://localhost:2024";

@Component({
  selector: "app-pipeline-chat",
  template: `
    <div>
      <app-pipeline-progress
        [nodes]="graphNodes()"
        [isLoading]="stream.isLoading()"
      />
      <app-node-card-list
        [nodes]="graphNodes()"
        [stream]="stream"
        [isLoading]="stream.isLoading()"
      />
    </div>
  `,
})
export class PipelineChatComponent {
  stream = injectStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "graph_execution_cards",
  });

  graphNodes = computed(() => [...this.stream.subgraphs().values()]);
}
```

## Routing streaming tokens to nodes

As the graph streams, each discovered subgraph snapshot identifies the node it
belongs to. Pass that snapshot to a selector hook or composable to read the
messages scoped to that node:

```tsx
import { AIMessage } from "langchain";
import { useMessages, type AnyStream, type SubgraphDiscoverySnapshot } from "@langchain/react";

function NodeCard({
  node,
  stream,
}: {
  node: SubgraphDiscoverySnapshot;
  stream: AnyStream;
}) {
  const messages = useMessages(stream, node);
  const lastAIMessage = messages.find(AIMessage.isInstance);
  const streamingContent = lastAIMessage?.text ?? "";

  return <NodeCardBody node={node} content={streamingContent} />;
}
```

The first mounted selector opens a scoped subscription for that node namespace.
When the node card unmounts, the subscription is released automatically.

## Determining node status

Each discovered node carries its current status. Use `node.status` directly;
the discovery snapshot reports `"pending"`, `"running"`, `"complete"`, or
`"error"`:

```ts
type NodeStatus = SubgraphDiscoverySnapshot["status"];

const status: NodeStatus = node.status;
```

## Building the pipeline progress bar

A horizontal progress bar at the top gives users a bird's-eye view of the
entire pipeline. Each step is a labeled segment that fills in as nodes complete:

```tsx
function PipelineProgress({
  nodes,
  isLoading,
}: {
  nodes: SubgraphDiscoverySnapshot[];
  isLoading: boolean;
}) {
  const firstIncompleteIdx = nodes.findIndex((node) => node.status !== "complete");

  return (
    <div className="flex items-center gap-1">
      {nodes.map((node, i) => {
        const isRunning =
          isLoading && node.status !== "complete" && firstIncompleteIdx === i;
        const colors = {
          pending: "bg-gray-200 text-gray-500",
          running: "bg-blue-400 text-white animate-pulse",
          complete: "bg-green-500 text-white",
          error: "bg-red-500 text-white",
        };
        const status = isRunning ? "running" : node.status;

        return (
          <div key={node.id} className="flex items-center">
            <div
              className={`rounded-full px-3 py-1 text-xs font-medium ${colors[status]}`}
            >
              {node.nodeName}
            </div>
            {i < nodes.length - 1 && (
              <div
                className={`mx-1 h-0.5 w-6 ${
                  status === "complete" ? "bg-green-500" : "bg-gray-200"
                }`}
              />
            )}
          </div>
        );
      })}
    </div>
  );
}
```

## Building collapsible NodeCard components

Each node gets its own card that shows the status badge, content (streaming or
final), and a collapsible body for long outputs:

```tsx
function NodeCard({
  node,
  stream,
}: {
  node: SubgraphDiscoverySnapshot;
  stream: AnyStream;
}) {
  const [open, setOpen] = useState(node.status === "running");
  const messages = useMessages(stream, node);
  const lastAIMessage = messages.find(AIMessage.isInstance);

  useEffect(() => {
    if (node.status === "running") setOpen(true);
    if (node.status === "complete") setOpen(false);
  }, [node.status]);

  return (
    <div className="rounded-lg border bg-white shadow-sm">
      <button
        onClick={() => setOpen(!open)}
        className="flex w-full items-center justify-between p-4"
      >
        <div className="flex items-center gap-3">
          <h3 className="font-semibold">{node.nodeName}</h3>
          <StatusBadge status={node.status} />
        </div>
        <span className={open ? "rotate-90" : ""}>▶</span>
      </button>

      {open && (
        <div className="border-t px-4 py-3">
          <div className="prose prose-sm max-w-none">
            {lastAIMessage?.text?.trim()
              ? <Markdown>{lastAIMessage.text}</Markdown>
              : <p className="italic text-gray-500">Processing...</p>}
          </div>
        </div>
      )}
    </div>
  );
}
```

## Streaming vs. completed content

The node card reads scoped messages for both streaming and final content. This
avoids assuming that a graph node name matches the state key it writes to (for
example, `do_research` writes to `research` in the playground graph):

| Source | When to use |
| - | - |
| `useMessages(stream, node)` | Render node-scoped streaming and final messages |
| `stream.values` | Read whole-graph state such as the final `synthesis` field, using the actual state key |

The pattern is: show the most recent scoped AI message in the node card, and
use `stream.values` only when you intentionally need a graph state field.

Because scoped messages are tied to the producing node, the UI can support
parallel graph paths without guessing from message order. Each card updates from
the stream events that belong to its node, and completed values remain available
through `stream.values`.

```ts
function NodeContent({ stream, node }: { stream: AnyStream; node: SubgraphDiscoverySnapshot }) {
  const messages = useMessages(stream, node);
  const content = messages.find(AIMessage.isInstance)?.text ?? "";

  return <Markdown>{content}</Markdown>;
}
```

> [!TIP]
>
> Streaming content may include partial tokens or markdown that hasn't been
> fully formed yet. If you render markdown, make sure your renderer handles
> incomplete syntax gracefully (e.g., an unclosed bold marker `**`).

## Putting it all together

Here's the full card list that combines routing, status detection, and card
rendering:

```tsx
function NodeCardList({
  nodes,
  stream,
  isLoading,
}: {
  nodes: SubgraphDiscoverySnapshot[];
  stream: AnyStream;
  isLoading: boolean;
}) {
  const firstIncompleteIdx = nodes.findIndex((node) => node.status !== "complete");

  return (
    <div className="space-y-3">
      {nodes.map((node, i) => {
        const isComplete = node.status === "complete";
        const isRunning = isLoading && !isComplete && firstIncompleteIdx === i;
        if (!isComplete && !isRunning) return null;

        return <NodeCard key={node.id} node={node} stream={stream} />;
      })}
    </div>
  );
}
```

## Use cases

Graph execution cards work well for any multi-step pipeline where visibility
matters:

* **Research pipelines**: classify → gather sources → analyze → synthesize a
  report
* **Content generation**: outline → draft → fact-check → edit → publish
* **Data processing**: ingest → validate → transform → aggregate → export
* **Code generation**: understand requirements → plan architecture → write
  code → review → test
* **Decision workflows**: gather context → evaluate options → score
  alternatives → recommend

## Handling dynamic pipelines

Not all graphs have a fixed set of nodes. Some pipelines add or skip nodes
based on the input. The discovery map contains only nodes observed for the
current thread:

```ts
const activeNodes = [...stream.subgraphs.values()];
```

This ensures your UI only shows cards for nodes that are relevant to the
current execution, avoiding empty placeholder cards.

> [!NOTE]
>
> If your graph has conditional branching (e.g., skip "Research" for simple
> factual queries), skipped nodes will not appear in `stream.subgraphs`. Your
> pipeline progress bar can render discovered nodes only or dim expected nodes
> that have no matching snapshot.

## Best practices

* **Discover nodes from the stream**. Render cards from `stream.subgraphs`
  rather than hardcoding expected nodes; conditional or skipped steps won't
  appear until they run.
* **Treat state keys as UI contracts**. Decide which graph outputs should be
  stable enough for the frontend to render, and keep those keys documented next
  to the graph definition.
* **Use scoped messages for node cards**. They work while a node is streaming
  and after it completes, without coupling UI cards to state key names.
* **Auto-collapse completed nodes**. In long pipelines, auto-collapse finished
  cards so users can focus on the currently active step.
* **Show estimated timing**. If you have historical data on how long each node
  takes, display a time estimate to set user expectations.
* **Add a global progress indicator**. Complement per-node cards with an
  overall progress bar (e.g., "Step 2 of 4") at the top of the pipeline view.
* **Handle errors per node**. If a node fails, show the error in its card
  without collapsing the entire pipeline. Other nodes may still complete
  successfully.
