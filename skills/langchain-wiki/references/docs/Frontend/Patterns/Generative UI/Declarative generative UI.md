# Declarative generative UI

> Compose agent-generated interfaces from a registered component catalog using json-render and A2UI

## Overview

Declarative generative UI is in the middle of the
[generative UI spectrum](Generative%20UI%20overview.md). The agent emits a
structured specification, and the frontend composes the interface from a catalog of
components you register ahead of time. Instead of rendering text responses in chat
bubbles, the agent output **is** the UI: forms, cards, dashboards, and more. You
define which components are available (the "catalog"), and the agent composes them
into a valid UI tree.

The catalog is the guardrail that makes this approach safe: the agent can arrange
and combine your components freely, but cannot step outside the set you approve.
This balances creativity against predictability. It is where the long tail lives,
trading pixel-perfection for breadth, which suits secondary interactions, internal
tools, and dashboards where showing something useful matters more than exact
control. This page covers declarative generative UI with
[json-render](https://json-render.dev), a generative UI framework
that defines component catalogs, generates specs with AI, and renders them safely
across React, Vue, Svelte, and Angular. For Google's A2UI specification (integrated
via CopilotKit), see [A2UI](#a2ui-an-alternative-declarative-spec) below.

## When to use this approach

Use declarative generative UI for the long tail of your product, where the
agent can compose layouts you did not fully anticipate while staying inside a set
of components you approve: secondary interactions, internal tools, and dashboards.
When a surface is high-traffic or brand-critical and must be exact, move toward
[controlled generative UI](Controlled%20generative%20UI.md). When
you want interfaces created outside your application, move toward
[open-ended generative UI](Open-ended%20generative%20UI.md).

## How it works

1. **Define a catalog**: declare what components the AI can use, with typed props
2. **Prompt the AI**: describe the UI you want in natural language
3. **AI generates a spec**: a JSON document describing the component tree
4. **Render safely**: json-render's `Renderer` renders the spec using your components

The catalog acts as a guardrail: the AI can only use components you've defined,
with props that match your schema. The output is always predictable and safe.

## Define a component catalog

The catalog describes every component the AI is allowed to use. Each component has a
Zod schema for its props and a description that the AI reads to understand when to
use it:

```ts
import { defineCatalog } from "@json-render/core";
import { schema } from "@json-render/react/schema";
import { z } from "zod";

const catalog = defineCatalog(schema, {
  components: {
    Card: {
      description: "A card container with optional title and padding",
      props: z.object({
        title: z.string().optional(),
        padding: z.enum(["sm", "md", "lg"]).optional(),
      }),
    },
    Stack: {
      description: "Layout children vertically or horizontally with consistent spacing",
      props: z.object({
        direction: z.enum(["vertical", "horizontal"]).optional(),
        gap: z.enum(["sm", "md", "lg"]).optional(),
      }),
    },
    TextInput: {
      description: "A text input field with optional label and placeholder",
      props: z.object({
        label: z.string().optional(),
        placeholder: z.string().optional(),
        type: z.enum(["text", "email", "password", "number", "textarea"]).optional(),
      }),
    },
    Button: {
      description: "A clickable button with label and style variants",
      props: z.object({
        label: z.string(),
        variant: z.enum(["primary", "secondary", "ghost", "link"]).optional(),
        fullWidth: z.boolean().optional(),
      }),
    },
  },
  actions: {},
});
```

> [!TIP]
>
> Keep catalogs focused. Include only components the AI needs for the use case.
> A smaller catalog produces better results than a kitchen-sink approach.

## Build a component registry

The registry maps each catalog component to its actual rendering implementation.
Use `defineRegistry` to get type-safe bindings between the catalog props and
your component functions:

```tsx React
import { defineRegistry, Renderer, JSONUIProvider } from "@json-render/react";

const { registry } = defineRegistry(catalog, {
  components: {
    Card: ({ props, children }) => (
      <div className="card">
        {props.title && <h2>{props.title}</h2>}
        {children}
      </div>
    ),
    Stack: ({ props, children }) => (
      <div className={`stack stack-${props.direction ?? "vertical"} gap-${props.gap ?? "md"}`}>
        {children}
      </div>
    ),
    TextInput: ({ props }) => (
      <div>
        {props.label && <label>{props.label}</label>}
        <input type={props.type ?? "text"} placeholder={props.placeholder} />
      </div>
    ),
    Button: ({ props }) => (
      <button className={props.variant ?? "primary"}>
        {props.label}
      </button>
    ),
  },
});
```

```vue Vue
<script setup lang="ts">
import { h } from "vue";
import { defineRegistry, Renderer, JSONUIProvider } from "@json-render/vue";

const { registry } = defineRegistry(catalog, {
  components: {
    Card: ({ props, children }) =>
      h("div", { class: "card" }, [
        props.title ? h("h2", null, props.title) : null,
        children,
      ]),
    Stack: ({ props, children }) =>
      h("div", { class: `stack stack-${props.direction ?? "vertical"} gap-${props.gap ?? "md"}` }, children),
    TextInput: ({ props }) =>
      h("div", null, [
        props.label ? h("label", null, props.label) : null,
        h("input", { type: props.type ?? "text", placeholder: props.placeholder }),
      ]),
    Button: ({ props }) =>
      h("button", { class: props.variant ?? "primary" }, props.label),
  },
});
</script>
```

## Connect to the agent

The agent uses structured output to return a json-render spec. Set up `useStream`
with your agent's assistant ID, then extract the spec from the AI message's
`tool_calls`:

```tsx React
import { useStream } from "@langchain/react";
import { AIMessage } from "langchain";

function GenerativeUI() {
  const stream = useStream<typeof myAgent>({
    apiUrl: "http://localhost:2024",
    assistantId: "generative_ui",
  });

  const aiMessage = stream.messages.find(AIMessage.isInstance);
  const rawSpec = aiMessage?.tool_calls?.[0]?.args;

  // ... filter and render (see streaming section below)
}
```

```vue Vue
<script setup lang="ts">
import { useStream } from "@langchain/vue";
import { AIMessage } from "langchain";
import { computed } from "vue";

const stream = useStream<typeof myAgent>({
  apiUrl: "http://localhost:2024",
  assistantId: "generative_ui",
});

const aiMessage = computed(() => stream.messages.value.find(AIMessage.isInstance));
const rawSpec = computed(() => aiMessage.value?.tool_calls?.[0]?.args);
</script>
```

```svelte Svelte
<script lang="ts">
  import { useStream } from "@langchain/svelte";
  import { AIMessage } from "langchain";

  const stream = useStream<typeof myAgent>({
    apiUrl: "http://localhost:2024",
    assistantId: "generative_ui",
  });

  const aiMessage = $derived(stream.messages.find((m) => AIMessage.isInstance(m)));
  const rawSpec = $derived(aiMessage?.tool_calls?.[0]?.args);
</script>
```

```ts Angular
import { Component } from "@angular/core";
import { injectStream } from "@langchain/angular";
import { AIMessage } from "langchain";

@Component({
  selector: "app-generative-ui",
  template: `...`,
})
export class GenerativeUIComponent {
  stream = injectStream<typeof myAgent>({
    apiUrl: "http://localhost:2024",
    assistantId: "generative_ui",
  });

  get rawSpec() {
    const ai = this.stream.messages().find(AIMessage.isInstance);
    return ai?.tool_calls?.[0]?.args;
  }
}
```

## Stream and render progressively

During streaming, the spec is built up incrementally. Elements arrive one at a
time and may initially lack `type` or `props`. Filter to only complete elements
and pass `loading={true}` to the `Renderer`, which tells it to silently skip
children that haven't arrived yet. The UI builds up component by component:

```tsx
/*
 * Filter the streamed spec to only include elements with valid type/props,
 * enabling progressive rendering as the AI response builds up. Passing
 * loading={true} to the Renderer tells it to skip missing children silently.
 */
const spec = (() => {
  if (!rawSpec?.root || !rawSpec?.elements) return null;
  const rootEl = rawSpec.elements[rawSpec.root];
  if (!rootEl?.type || rootEl?.props == null) return null;

  const safeElements = {};
  for (const [key, el] of Object.entries(rawSpec.elements)) {
    if (el?.type && el?.props != null) {
      safeElements[key] = el;
    }
  }
  return { root: rawSpec.root, elements: safeElements };
})();

return (
  <>
    {spec && (
      <JSONUIProvider registry={registry}>
        <Renderer spec={spec} registry={registry} loading={stream.isLoading} />
      </JSONUIProvider>
    )}
  </>
);
```

> [!NOTE]
>
> The `JSONUIProvider` is required to set up json-render's internal context
> providers (state, visibility, validation, actions). The `Renderer` component
> must be rendered inside it.

## The spec format

The AI agent generates a flat JSON spec with a `root` key pointing to the
root element and an `elements` map containing all components:

```json
{
  "root": "login-card",
  "elements": {
    "login-card": {
      "type": "Card",
      "props": { "title": "Login" },
      "children": ["login-stack"]
    },
    "login-stack": {
      "type": "Stack",
      "props": { "direction": "vertical", "gap": "md" },
      "children": ["email-input", "password-input", "submit-btn"]
    },
    "email-input": {
      "type": "TextInput",
      "props": { "label": "Email", "placeholder": "Enter your email", "type": "email" },
      "children": []
    },
    "password-input": {
      "type": "TextInput",
      "props": { "label": "Password", "placeholder": "Enter your password", "type": "password" },
      "children": []
    },
    "submit-btn": {
      "type": "Button",
      "props": { "label": "Sign In", "variant": "primary", "fullWidth": true },
      "children": []
    }
  }
}
```

Each element references its children by ID, and leaf elements like `TextInput`
and `Button` have empty `children` arrays.

## A2UI: an alternative declarative spec

One way to describe an interface declaratively is json-render. A2UI is another:
Google's declarative, streaming-first generative UI specification, integrated via
CopilotKit. Like json-render, it composes interfaces from components you
register, so the agent stays inside guardrails you define. A2UI comes in two
variants:

* **Dynamic schema**: a secondary model generates the full interface, including
  schema, data, and layout, from the conversation, for maximum flexibility.
* **Fixed schema**: the component tree is defined on the frontend and the agent
  streams only data into it, for the fastest and most predictable rendering.

For details, see CopilotKit's docs on [A2UI](https://docs.copilotkit.ai/generative-ui/a2ui),
[dynamic schema](https://docs.copilotkit.ai/generative-ui/a2ui/dynamic-schema), and
[fixed schema](https://docs.copilotkit.ai/generative-ui/a2ui/fixed-schema). To
wire CopilotKit to a LangGraph deployment, see [CopilotKit](../../Integrations/CopilotKit.md).

## Best practices

* **Use descriptive component descriptions**: the AI uses these to understand when
  to use each component. Clear descriptions lead to better UI generation.
* **Validate before rendering**: always check that elements have valid `type` and
  non-null `props` before passing to the Renderer, since streaming delivers partial data.
* **Design for streaming**: pass `loading={true}` during streaming so the Renderer
  gracefully handles children that haven't arrived yet. Users see the UI build up
  in real time rather than waiting for the full response.
* **Style with design tokens**: use CSS custom properties so rendered components
  adapt to light and dark themes automatically.
* **Wrap with JSONUIProvider**: the `Renderer` must be inside a `JSONUIProvider`
  to access json-render's internal context for state, visibility, and actions.

## See also

* [Generative UI overview](Generative%20UI%20overview.md)
* [Controlled generative UI](Controlled%20generative%20UI.md)
* [Open-ended generative UI](Open-ended%20generative%20UI.md)

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/frontend/declarative-generative-ui.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
