# Structured output

> Render structured agent responses with custom UI components instead of plain text

Structured output lets the agent return typed, machine-readable data instead of plain text. Instead of rendering a single string, you get a structured object you can map to any UI: cards, tables, charts, step-by-step breakdowns, or domain-specific renderers.

## What is structured output?

Instead of returning a free-form text response, the agent uses a tool call to return a structured object conforming to a predefined schema. This gives you:

* **Type-safe data**: parse the response into a known TypeScript type
* **Precise rendering control**: render each field with its own UI treatment
* **Consistent formatting**: every response follows the same structure regardless of the underlying model

The agent accomplishes this by calling a "structured output" tool whose arguments contain the response data. The tool itself doesn't execute any logic and is purely a vehicle for returning typed data.

## Use cases

* **Product comparisons**: feature tables, pros/cons lists, ratings
* **Data analysis**: summaries with metrics, breakdowns, and highlights
* **Step-by-step guides**: ordered instructions with descriptions and code snippets
* **Recipes**: ingredients, steps, timings, and nutritional info
* **Math and science**: formulas rendered with LaTeX, step-by-step derivations
* **Travel planning**: itineraries with dates, locations, and cost estimates

## Define a schema

Define a TypeScript type for the structured data the agent returns. The shape of this schema determines how you render the UI.

The following is the math-solution schema used by the embedded demo:

```ts
interface MathSolution {
  problem: string; // The original math problem
  steps: {
    explanation: string;
    latex: string; // Optional display math for this step
  }[]; // Step-by-step derivation
  finalAnswer: string; // Plain-text final answer
  finalAnswerLatex: string; // LaTeX representation of the final answer
}
```

Your schema can be anything. The pattern works the same way regardless of shape.

## Extract structured output from messages

The structured output lives in the `tool_calls` array of the last `AIMessage`. Extract it by finding the AI message and accessing the first tool call's arguments:

```ts
import { AIMessage } from "langchain";

function extractStructuredOutput<T>(messages: any[]): T | null {
  const aiMessage = messages.find(AIMessage.isInstance);
  const toolCall = aiMessage?.tool_calls?.[0];
  if (!toolCall) return null;

  return toolCall.args as T;
}
```

> [!NOTE]
>
> The structured output tool call may not have `args` populated until the agent finishes streaming. During streaming, `args` may be partially populated or undefined. Always check for completeness before rendering.

## Set up `useStream`

Connect [`useStream`](https://reference.langchain.com/javascript/langchain-react/index/useStream) to your structured-output agent, then read
`stream.messages` and extract the typed payload from the latest [`AIMessage`](https://reference.langchain.com/python/langchain-core/messages/ai/AIMessage)
tool call. Render your custom UI once `args` is complete, show a loading state
while `stream.isLoading` is true (tool arguments may stream in gradually), and
use `stream.submit()` to send the next prompt.

> [!NOTE]
>
> The code examples use `useStream<typeof myAgent>` for type-safe stream state. See Type inference for [Python](../Overview.md#type-inference) or [JavaScript](https://docs.langchain.com/oss/javascript/langchain/frontend/overview.md#type-inference) backends.

```tsx React
import { useStream } from "@langchain/react";
import { AIMessage } from "langchain";

function MathSolutionChat() {
  const stream = useStream<typeof myAgent>({
    apiUrl: "http://localhost:2024",
    assistantId: "structured_output_latex",
  });

  const solution = extractStructuredOutput<MathSolution>(stream.messages);

  return (
    <div>
      {!solution && !stream.isLoading && (
        <PromptInput onSubmit={(text) =>
          stream.submit({ messages: [{ type: "human", content: text }] })
        } />
      )}
      {stream.isLoading && <LoadingIndicator />}
      {solution && <SolutionCard solution={solution} />}
    </div>
  );
}
```

```vue Vue
<script setup lang="ts">
import { useStream } from "@langchain/vue";
import { AIMessage } from "langchain";
import { computed } from "vue";

const stream = useStream<typeof myAgent>({
  apiUrl: "http://localhost:2024",
  assistantId: "structured_output_latex",
});

const solution = computed(() =>
  extractStructuredOutput<MathSolution>(stream.messages.value)
);

function handleSubmit(text: string) {
  stream.submit({ messages: [{ type: "human", content: text }] });
}
</script>

<template>
  <div>
    <PromptInput v-if="!solution && !stream.isLoading" @submit="handleSubmit" />
    <LoadingIndicator v-if="stream.isLoading" />
    <SolutionCard v-if="solution" :solution="solution" />
  </div>
</template>
```

```svelte Svelte
<script lang="ts">
  import { useStream } from "@langchain/svelte";
  import { AIMessage } from "langchain";

  const stream = useStream<typeof myAgent>({
    apiUrl: "http://localhost:2024",
    assistantId: "structured_output_latex",
  });

  const solution = $derived(extractStructuredOutput<MathSolution>(stream.messages));

  function handleSubmit(text: string) {
    stream.submit({ messages: [{ type: "human", content: text }] });
  }
</script>

<div>
  {#if !solution && !stream.isLoading}
    <PromptInput on:submit={(e) => handleSubmit(e.detail)} />
  {/if}
  {#if stream.isLoading}
    <LoadingIndicator />
  {/if}
  {#if solution}
    <SolutionCard {solution} />
  {/if}
</div>
```

```ts Angular
import { Component, computed } from "@angular/core";
import { injectStream } from "@langchain/angular";

@Component({
  selector: "app-math-solution-chat",
  template: `
    @if (!solution() && !stream.isLoading()) {
      <prompt-input (onSubmit)="handleSubmit($event)" />
    }
    @if (stream.isLoading()) {
      <loading-indicator />
    }
    @if (solution()) {
      <solution-card [solution]="solution()" />
    }
  `,
})
export class MathSolutionChatComponent {
  stream = injectStream<typeof myAgent>({
    apiUrl: "http://localhost:2024",
    assistantId: "structured_output_latex",
  });

  solution = computed(() =>
    extractStructuredOutput<MathSolution>(this.stream.messages())
  );

  handleSubmit(text: string) {
    this.stream.submit({
      messages: [{ type: "human", content: text }],
    });
  }
}
```

## Render the structured data

Once you have a typed object, build a component that maps each field to the
appropriate UI element. This is the core of the pattern: turning structured
data into a purpose-built interface.

```tsx
function LatexBlock({ latex }: { latex: string }) {
  return <div className="latex-block">{latex}</div>; // Render with KaTeX or MathJax.
}

function SolutionCard({ solution }: { solution: MathSolution }) {
  return (
    <div className="solution-card">
      <h3>{solution.problem}</h3>
      <ol>
        {solution.steps.map((step, i) => (
          <li key={i}>
            <span>{step.explanation}</span>
            {step.latex && <LatexBlock latex={step.latex} />}
          </li>
        ))}
      </ol>
      <strong>{solution.finalAnswer}</strong>
      {solution.finalAnswerLatex && <LatexBlock latex={solution.finalAnswerLatex} />}
    </div>
  );
}
```

## Handle partial streaming data

During streaming, the tool call arguments may be incomplete JSON. Guard against this in your extraction logic:

```ts
function extractStructuredOutput<T>(
  messages: any[],
  requiredFields: string[] = [],
): T | null {
  const aiMessages = messages.filter(AIMessage.isInstance);
  if (aiMessages.length === 0) return null;

  const lastAI = aiMessages[aiMessages.length - 1];
  const toolCall = lastAI.tool_calls?.[0];
  if (!toolCall?.args) return null;

  const args = toolCall.args as Record<string, unknown>;
  const hasRequired = requiredFields.every(
    (field) => args[field] !== undefined
  );

  if (requiredFields.length > 0 && !hasRequired) return null;
  return args as T;
}
```

Use the `requiredFields` parameter to wait until critical fields are populated before rendering:

```ts
const solution = extractStructuredOutput<MathSolution>(stream.messages, [
  "problem",
  "steps",
  "finalAnswer",
]);
```

## Render progressively during streaming

Rather than waiting for the complete structured output, render fields as they arrive. This gives users immediate feedback while the agent is still generating:

```tsx
function ProgressiveSolutionCard({ messages }: { messages: any[] }) {
  const partial = extractStructuredOutput<Partial<MathSolution>>(messages);
  if (!partial) return null;

  return (
    <div className="solution-card">
      {partial.problem && <h3>{partial.problem}</h3>}

      {partial.steps && partial.steps.length > 0 && (
        <div className="solution-steps">
          <h4>Steps</h4>
          {partial.steps.map((step, i) => (
            <div key={i} className="step">
              <div className="step-number">Step {i + 1}</div>
              <p>{step.explanation}</p>
              {step.latex && <LatexBlock latex={step.latex} />}
            </div>
          ))}
        </div>
      )}

      {partial.finalAnswer && <strong>{partial.finalAnswer}</strong>}
    </div>
  );
}
```

> [!TIP]
>
> Progressive rendering works well when the schema has a natural top-to-bottom
> order: problem, then derivation steps, then final answer. The agent typically
> generates fields in schema order, so the UI fills in naturally.

## Best practices

* **Validate before rendering**: always check that required fields exist before rendering, since streaming may deliver partial data
* **Use a generic extraction function**: parameterize your extraction logic with a type and required fields so it works across different schemas
* **Render progressively**: show fields as they arrive rather than waiting for the complete object, so users see immediate feedback
* **Provide fallback representations**: if a field supports rich rendering (LaTeX, Markdown, charts), also include a plain-text equivalent in your schema as a fallback
* **Keep schemas flat when possible**: deeply nested schemas are harder to render progressively and more likely to break during partial streaming
* **Match UI to data**: choose the rendering strategy that best represents each field type (tables for arrays, cards for nested objects, badges for status fields)

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/frontend/structured-output.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
