# Markdown messages

> Render LLM responses as rich, formatted markdown with proper streaming support

LLMs naturally produce markdown-formatted text, including headings, lists, code blocks,
tables, and inline formatting. Rendering this content as plain text wastes the
structure the model is providing. This pattern shows you how to parse and render
markdown in real time as it streams from the agent, across all major frontend
frameworks.

## How markdown rendering works

The rendering pipeline has three steps:

1. **Receive:** [`useStream`](https://reference.langchain.com/javascript/langchain-react/index/useStream) accumulates the streamed text into `msg.text` on
   each AI message, updating reactively as new tokens arrive.
2. **Parse:** A markdown parser converts the raw text to HTML (or a React
   element tree). This runs on every update but is fast enough for chat-length
   content (\< 5ms for a 5 KB message).
3. **Render:** The parsed output is rendered into the DOM. React uses virtual
   DOM diffing; Vue and Svelte use `v-html` / `{@html}` with sanitized HTML.

## Setting up `useStream`

The markdown pattern uses a simple chat agent with no special configuration.
Wire up [`useStream`](https://reference.langchain.com/javascript/langchain-react/index/useStream) with your agent URL and assistant ID.

> [!NOTE]
>
> The code examples use `useStream<typeof myAgent>` for type-safe stream state. See Type inference for [Python](../Overview.md#type-inference) or [JavaScript](https://docs.langchain.com/oss/javascript/langchain/frontend/overview.md#type-inference) backends.

```tsx React
import { useStream } from "@langchain/react";
import { AIMessage, HumanMessage } from "langchain";

const AGENT_URL = "http://localhost:2024";

export function Chat() {
  const stream = useStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "simple_agent",
  });

  return (
    <div>
      {stream.messages.map((msg) => {
        if (AIMessage.isInstance(msg)) {
          return <Markdown key={msg.id}>{msg.text}</Markdown>;
        }
        if (HumanMessage.isInstance(msg)) {
          return <p key={msg.id}>{msg.text}</p>;
        }
      })}
    </div>
  );
}
```

```vue Vue
<script setup lang="ts">
import { useStream } from "@langchain/vue";
import { AIMessage, HumanMessage } from "langchain";

const AGENT_URL = "http://localhost:2024";

const stream = useStream<typeof myAgent>({
  apiUrl: AGENT_URL,
  assistantId: "simple_agent",
});
</script>

<template>
  <div>
    <template v-for="msg in stream.messages.value" :key="msg.id">
      <Markdown v-if="AIMessage.isInstance(msg)">{{ msg.text }}</Markdown>
      <p v-else-if="HumanMessage.isInstance(msg)">{{ msg.text }}</p>
    </template>
  </div>
</template>
```

```svelte Svelte
<script lang="ts">
  import { useStream } from "@langchain/svelte";
  import { AIMessage, HumanMessage } from "langchain";

  const AGENT_URL = "http://localhost:2024";

  const stream = useStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "simple_agent",
  });
</script>

<div>
  {#each stream.messages as msg (msg.id)}
    {#if AIMessage.isInstance(msg)}
      <Markdown content={msg.text} />
    {:else if HumanMessage.isInstance(msg)}
      <p>{msg.text}</p>
    {/if}
  {/each}
</div>
```

```ts Angular
import { Component } from "@angular/core";
import { injectStream } from "@langchain/angular";

const AGENT_URL = "http://localhost:2024";

@Component({
  selector: "app-chat",
  template: `
    @for (msg of stream.messages(); track msg.id) {
      <app-markdown [content]="msg.text" />
    }
  `,
})
export class ChatComponent {
  stream = injectStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "simple_agent",
  });
}
```

## Choosing a markdown library

Each framework has a natural choice for markdown rendering:

| Framework | Library | Output | Why |
| - | - | - | - |
| React | `react-markdown` + `remark-gfm` | React elements | Component-based, virtual DOM diffing, no `dangerouslySetInnerHTML` |
| Vue | `marked` + `dompurify` | Sanitized HTML via `v-html` | Lightweight, fast, GFM built-in |
| Svelte | `marked` + `dompurify` | Sanitized HTML via `{@html}` | Same as Vue, consistent API |
| Angular | `marked` + `dompurify` | Sanitized HTML via `[innerHTML]` | Same as Vue/Svelte |

> [!TIP]
>
> React's `react-markdown` converts markdown directly to React elements, so it
> doesn't need HTML sanitization. There's no `dangerouslySetInnerHTML` involved.
> For Vue, Svelte, and Angular, always sanitize the parsed HTML with `dompurify`
> before rendering.

## Building the Markdown component

```tsx React
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export function Markdown({ children }: { children: string }) {
  return (
    <div className="markdown-content">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>
        {children}
      </ReactMarkdown>
    </div>
  );
}
```

```vue Vue
<script setup lang="ts">
import { computed, useSlots } from "vue";
import { marked } from "marked";
import DOMPurify from "dompurify";

marked.setOptions({ gfm: true, breaks: true });

const slots = useSlots();

const html = computed(() => {
  const slot = slots.default?.();
  const text = slot
    ?.map((vnode) =>
      typeof vnode.children === "string" ? vnode.children : ""
    )
    .join("") ?? "";
  if (!text) return "";
  return DOMPurify.sanitize(marked.parse(text) as string);
});
</script>

<template>
  <div class="markdown-content" v-html="html" />
</template>
```

```svelte Svelte
<script lang="ts">
  import { marked } from "marked";
  import DOMPurify from "dompurify";

  let { content }: { content: string } = $props();

  marked.setOptions({ gfm: true, breaks: true });

  let html = $derived.by(() => {
    if (!content) return "";
    return DOMPurify.sanitize(marked.parse(content) as string);
  });
</script>

<div class="markdown-content">
  {@html html}
</div>
```

```ts Angular
import { Component, Input, computed, signal } from "@angular/core";
import { marked } from "marked";
import DOMPurify from "dompurify";

marked.setOptions({ gfm: true, breaks: true });

@Component({
  selector: "app-markdown",
  template: `<div class="markdown-content" [innerHTML]="html()"></div>`,
})
export class MarkdownComponent {
  @Input() set content(value: string) {
    this._content.set(value);
  }

  private _content = signal("");

  html = computed(() => {
    const text = this._content();
    if (!text) return "";
    return DOMPurify.sanitize(marked.parse(text) as string);
  });
}
```

## Sanitizing HTML output

When rendering parsed markdown as raw HTML (`v-html`, `{@html}`, `[innerHTML]`),
you must sanitize the output to prevent cross-site scripting (XSS). LLM
responses may contain arbitrary text, including markup that a markdown parser
could turn into executable HTML.

Use `dompurify` to strip dangerous elements:

```ts
import DOMPurify from "dompurify";

const safeHtml = DOMPurify.sanitize(rawHtml);
```

DOMPurify removes `<script>` tags, `onclick` attributes, `javascript:` URLs,
and other XSS vectors while preserving safe markdown output like headings,
lists, code blocks, tables, and links.

> [!NOTE]
>
> React's `react-markdown` does not need `dompurify` because it produces React
> elements directly, no raw HTML injection is involved.

## Streaming considerations

`useStream` updates `msg.text` reactively as each token arrives. The markdown
component re-parses on every update. For typical chat messages, this is
performant:

* `marked` parses at \~1 MB/s. A 5 KB message takes \< 5ms
* `react-markdown` + remark pipeline is similarly fast for chat-length content
* The browser's layout engine handles the DOM update efficiently

For very long responses (> 50 KB), consider these optimizations:

* **Throttle renders:** use `requestAnimationFrame` to batch updates at 60fps
  instead of re-rendering on every token
* **Incremental parsing:** parse only new content and append to a rendered
  buffer (advanced, typically not needed for chat UIs)

> [!NOTE]
>
> For most chat applications, the simple approach of re-parsing the full message
> on each token is sufficient. Only optimize if you observe janky scrolling or
> dropped frames with very long messages.

## Best practices

* **Always sanitize:** when using `v-html`, `{@html}`, or `[innerHTML]`,
  always run the parsed output through `dompurify`. Never trust raw HTML from a
  markdown parser fed with LLM output.
* **Enable GFM:** GitHub Flavored Markdown adds tables, strikethrough, task
  lists, and autolinks. These features are commonly used by LLMs.
* **Handle empty content:** check for empty strings before parsing to avoid
  rendering empty containers.
* **Use `breaks: true`:** enable line break conversion so single newlines in
  LLM output render as `<br>` rather than being ignored. LLMs often use single
  newlines for visual separation.
* **Style for chat context:** use compact margins and sizes appropriate for
  chat bubbles, not full-width article layouts.
* **Test with rich content:** verify rendering with headings, nested lists,
  code blocks with long lines, wide tables, and blockquotes to catch overflow
  or layout issues.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/frontend/markdown-messages.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
