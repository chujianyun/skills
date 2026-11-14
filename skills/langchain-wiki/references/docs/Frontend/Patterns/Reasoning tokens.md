# Reasoning tokens

> Display model thinking and reasoning processes in collapsible blocks

Reasoning tokens expose the internal thought process of advanced models like OpenAI's GPT-5 and Anthropic's Claude with extended thinking. These models produce structured content blocks that separate reasoning from the final answer, letting you build UIs that show *how* the model arrived at its response.

## What are reasoning tokens?

When models with reasoning capabilities process a prompt, they generate two distinct types of content:

1. **Reasoning blocks**: the model's internal chain-of-thought, problem decomposition, and step-by-step analysis
2. **Text blocks**: the final, polished response presented to the user

These are delivered as typed content blocks within an `AIMessage`, accessible via the `contentBlocks` property:

```ts
// Reasoning block
{ type: "reasoning", reasoning: "Let me think about this step by step..." }

// Text block
{ type: "text", text: "The answer is 42." }
```

> [!NOTE]
>
> Not all models produce reasoning tokens. This pattern applies specifically to models that support extended thinking or chain-of-thought output. Standard chat models return only text blocks.

## Use cases

* **Transparency**: show users the model's reasoning process to build trust in its answers
* **Debugging**: inspect the model's thought process to identify where it goes wrong
* **Educational tools**: teach students problem-solving by revealing how an AI approaches questions
* **Decision support**: let domain experts validate the reasoning behind recommendations
* **Quality assurance**: audit reasoning chains for compliance in regulated industries

## Extracting reasoning and text blocks

The `contentBlocks` array on an `AIMessage` contains all blocks in the order they were generated. Filter them by `type` to separate reasoning from text:

```ts
import { AIMessage } from "langchain";

function extractBlocks(msg: AIMessage) {
  const reasoningBlocks = msg.contentBlocks
    .filter((b) => b.type === "reasoning")
    .map((b) => b.reasoning);

  const textBlocks = msg.contentBlocks
    .filter((b) => b.type === "text")
    .map((b) => b.text);

  return {
    reasoning: reasoningBlocks.join(""),
    text: textBlocks.join(""),
  };
}
```

A single message may contain multiple reasoning blocks (e.g., if the model pauses its reasoning, produces partial text, then reasons further). Joining them gives you the complete thought process.

## Accessing messages from `useStream`

Connect [`useStream`](https://reference.langchain.com/javascript/langchain-react/index/useStream) to your reasoning-capable agent and iterate
`stream.messages` in your chat UI. Branch on `HumanMessage.isInstance` and
`AIMessage.isInstance`, then pass each assistant message to a component that
reads `contentBlocks` and separates reasoning from text. Set `isStreaming` on
the last message while `stream.isLoading` is true so thinking blocks update as
tokens arrive.

> [!NOTE]
>
> The code examples use `useStream<typeof myAgent>` for type-safe stream state. See Type inference for [Python](../Overview.md#type-inference) or [JavaScript](https://docs.langchain.com/oss/javascript/langchain/frontend/overview.md#type-inference) backends.

```tsx React
import { useStream } from "@langchain/react";
import { AIMessage, HumanMessage } from "langchain";

function Chat() {
  const stream = useStream<typeof myAgent>({
    apiUrl: "http://localhost:2024",
    assistantId: "reasoning",
  });

  return (
    <div className="messages">
      {stream.messages.map((msg, i) => {
        if (HumanMessage.isInstance(msg)) {
          return <HumanBubble key={i} text={msg.text} />;
        }
        if (AIMessage.isInstance(msg)) {
          return (
            <AIResponse
              key={i}
              message={msg}
              isStreaming={stream.isLoading && i === stream.messages.length - 1}
            />
          );
        }
        return null;
      })}
    </div>
  );
}
```

```vue Vue
<script setup lang="ts">
import { useStream } from "@langchain/vue";
import { AIMessage, HumanMessage } from "langchain";

const stream = useStream<typeof myAgent>({
  apiUrl: "http://localhost:2024",
  assistantId: "reasoning",
});
</script>

<template>
  <div class="messages">
    <template v-for="(msg, i) in stream.messages.value" :key="i">
      <HumanBubble v-if="HumanMessage.isInstance(msg)" :text="msg.text" />
      <AIResponse
        v-else-if="AIMessage.isInstance(msg)"
        :message="msg"
        :isStreaming="stream.isLoading.value && i === stream.messages.value.length - 1"
      />
    </template>
  </div>
</template>
```

```svelte Svelte
<script lang="ts">
  import { useStream } from "@langchain/svelte";
  import { AIMessage, HumanMessage } from "langchain";

  const stream = useStream<typeof myAgent>({
    apiUrl: "http://localhost:2024",
    assistantId: "reasoning",
  });
</script>

<div class="messages">
  {#each stream.messages as msg, i}
    {#if HumanMessage.isInstance(msg)}
      <HumanBubble text={msg.text} />
    {:else if AIMessage.isInstance(msg)}
      <AIResponse
        message={msg}
        isStreaming={stream.isLoading && i === stream.messages.length - 1}
      />
    {/if}
  {/each}
</div>
```

```ts Angular
import { Component } from "@angular/core";
import { injectStream } from "@langchain/angular";
import { AIMessage, HumanMessage } from "langchain";

@Component({
  selector: "app-chat",
  template: `
    <div class="messages">
      @for (msg of stream.messages(); track $index) {
        @if (isHuman(msg)) {
          <human-bubble [text]="msg.text" />
        } @else if (isAI(msg)) {
          <ai-response
            [message]="msg"
            [isStreaming]="stream.isLoading() && $index === stream.messages().length - 1"
          />
        }
      }
    </div>
  `,
})
export class ChatComponent {
  stream = injectStream<typeof myAgent>({
    apiUrl: "http://localhost:2024",
    assistantId: "reasoning",
  });

  isHuman = HumanMessage.isInstance;
  isAI = AIMessage.isInstance;
}
```

## Building a ThinkingBubble component

The `ThinkingBubble` presents reasoning tokens in a visually distinct, collapsible container. Users can expand it to see the full thought process or collapse it to focus on the final answer.

```tsx
import { useState } from "react";

function ThinkingBubble({
  reasoning,
  isStreaming,
}: {
  reasoning: string;
  isStreaming: boolean;
}) {
  const [isExpanded, setIsExpanded] = useState(false);

  const charCount = reasoning.length;
  const previewLength = 120;
  const preview =
    reasoning.length > previewLength
      ? reasoning.slice(0, previewLength) + "..."
      : reasoning;

  return (
    <div className="thinking-bubble">
      <button
        className="thinking-header"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <span className="thinking-icon">
          {isStreaming ? (
            <span className="thinking-spinner" />
          ) : (
            "💭"
          )}
        </span>
        <span className="thinking-label">
          {isStreaming ? "Thinking..." : `Thought process (${charCount} chars)`}
        </span>
        <span className={`chevron ${isExpanded ? "expanded" : ""}`}>▶</span>
      </button>

      {isExpanded && (
        <div className="thinking-content">
          <pre>{reasoning}</pre>
        </div>
      )}

      {!isExpanded && !isStreaming && (
        <div className="thinking-preview">{preview}</div>
      )}
    </div>
  );
}
```

## Rendering the complete AI response

Combine the `ThinkingBubble` and a standard text bubble into a single `AIResponse` component:

```tsx
function AIResponse({
  message,
  isStreaming,
}: {
  message: AIMessage;
  isStreaming: boolean;
}) {
  const reasoningBlocks = message.contentBlocks
    .filter((b) => b.type === "reasoning")
    .map((b) => b.reasoning)
    .join("");

  const textBlocks = message.contentBlocks
    .filter((b) => b.type === "text")
    .map((b) => b.text)
    .join("");

  const hasReasoning = reasoningBlocks.length > 0;
  const hasText = textBlocks.length > 0;

  const isReasoningPhase = isStreaming && !hasText;
  const isTextPhase = isStreaming && hasText;

  return (
    <div className="ai-response">
      {hasReasoning && (
        <ThinkingBubble
          reasoning={reasoningBlocks}
          isStreaming={isReasoningPhase}
        />
      )}
      {hasText && (
        <div className="ai-text-bubble">
          <p>{textBlocks}</p>
          {isTextPhase && <span className="cursor-blink">▊</span>}
        </div>
      )}
    </div>
  );
}
```

## Handling edge cases

### Messages without reasoning

Not every AI message will contain reasoning blocks. When `contentBlocks` has only text blocks, render a standard message bubble without the ThinkingBubble.

### Empty reasoning blocks

Some models produce empty reasoning blocks as placeholders. Filter these out:

```ts
const meaningfulReasoning = message.contentBlocks
  .filter((b) => b.type === "reasoning" && b.reasoning.trim().length > 0);
```

### Multiple reasoning-text cycles

A single message can alternate between reasoning and text blocks. If you need to preserve this interleaving, iterate `contentBlocks` in order rather than grouping by type:

```ts
message.contentBlocks.forEach((block) => {
  if (block.type === "reasoning") {
    // Render ThinkingBubble
  } else if (block.type === "text") {
    // Render text paragraph
  }
});
```

## Best practices

* **Default to collapsed**: show reasoning on demand, not by default
* **Show character count**: gives users a quick sense of how much thinking went into the response
* **Differentiate visually**: use distinct colors, borders, or backgrounds so reasoning is never confused with the actual answer
* **Animate transitions**: smooth expand/collapse animations improve perceived quality
* **Consider accessibility**: use proper ARIA attributes (`aria-expanded`, `aria-controls`) on the toggle button
* **Truncate in previews**: show a short preview of the reasoning when collapsed so users can decide whether to expand

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/frontend/reasoning-tokens.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
