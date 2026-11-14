# Generative UI overview

> Understand the generative UI spectrum from controlled to declarative to open-ended interfaces

Generative UI is any pattern where an agent's output presents a user interface
beyond text. Instead of streaming a paragraph into a chat bubble, the agent drives
forms, cards, dashboards, and interactive controls. This lets your UI communicate
results the way an application would, while the agent decides what to show and when.

Generative UI is not a single technique. It spans a spectrum defined by one
question: **who authors the interface?** At one end you write every component and
the agent only chooses among them. At the other end, the interface is created
entirely outside your application. Progressing along the spectrum trades
predictability for expressive range.

## The generative UI spectrum

The spectrum runs from full control over every pixel to full agent autonomy, using
three primary approaches:

```mermaid
%%{
  init: {
    "fontFamily": "monospace",
    "flowchart": {
      "curve": "curve"
    }
  }
}%%
graph LR
  C["Controlled<br/>you author components"]
  D["Declarative<br/>agent emits a UI spec"]
  O["Open-ended<br/>UI created externally"]

  C ~~~ D ~~~ O

  classDef light fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710;
  classDef mid fill:#CDE9FF,stroke:#006DDD,stroke-width:2px,color:#030710;
  classDef deep fill:#B8DFFF,stroke:#006DDD,stroke-width:2px,color:#030710;
  class C light;
  class D mid;
  class O deep;
```

More control

More autonomy

Moving left to right, predictability and per-capability engineering cost both fall,
while the agent's expressive range grows. Accessibility and visual consistency are
easiest to guarantee on the left and hardest to guarantee on the right.

### Controlled

You author the components, and the agent selects which one to render and what data
to pass. This gives the highest predictability and the tightest control over
branding and accessibility, at the cost of writing a component for every capability
you want to expose. It is the workhorse of generative UI and the right fit for
high-traffic, brand-critical surfaces where a layout must be exact, such as flight
tickets and booking confirmations. Your component library is the boundary: the agent
can only render what you shipped. Controlled generative UI covers components as
tools, tool-call rendering, state rendering, and reasoning.

For details, see [Controlled generative UI](Controlled%20generative%20UI.md).

### Declarative

The agent emits a structured specification, and the frontend composes the interface
from a catalog of components you register ahead of time. The catalog acts as a
guardrail and boundary: the agent can arrange and combine your components freely, but
cannot step outside the set you approve. This is where the long tail lives. It
trades pixel-perfection for breadth, which suits secondary interactions, internal
tools, and dashboards where showing something useful matters more than exact
control. [Declarative generative UI](Declarative%20generative%20UI.md)
covers this with [json-render](https://json-render.dev); Google's A2UI, integrated via
CopilotKit, offers the same shape with dynamic and fixed schema variants.

### Open-ended

The agent owns the canvas. The interface is created outside your application, for
example by an MCP server, and rendered in a sandbox. This gives the widest
expressive range and can add new interface capabilities with no frontend code on
your side, which suits one-off visualizations and bespoke answers where a result
that is surprising and good enough beats one that is predictable. It is also the most
experimental approach: the least deterministic, and the hardest in which to
guarantee accessibility, consistency, and safety, so the UI must be isolated. The
sandbox and your prompt are the boundary.

For details, see [Open-ended generative UI](Open-ended%20generative%20UI.md).

## Choosing an approach

Start from how much you need to constrain the interface:

| If you need to... | Choose |
| - | - |
| Guarantee branding, layout, and accessibility for a known set of outputs | [Controlled](Controlled%20generative%20UI.md) |
| Let the agent compose novel layouts using only approved components | [Declarative](Declarative%20generative%20UI.md) |
| Surface interfaces authored by third parties without building them yourself | [Open-ended](Open-ended%20generative%20UI.md) |

Choosing a single approach for an entire product is the most common mistake. Real
applications mix approaches and match each surface to its purpose: controlled
components for the high-traffic, brand-critical core, declarative composition for the
long tail of secondary interactions, and open-ended embeds for third-party
capabilities. A single session can move across all three.

The spectrum also applies beyond chat. The same three approaches describe generative
interfaces on mobile and in surfaces like Slack or email, not only in a chat
transcript.

## Explore the spectrum

> [card] [Controlled](Controlled%20generative%20UI.md)
>
> Author the components; the agent picks which to render and what data to pass.

> [card] [Declarative](Declarative%20generative%20UI.md)
>
> The agent emits a spec; the frontend composes from a registered catalog.

> [card] [Open-ended](Open-ended%20generative%20UI.md)
>
> Render UI created elsewhere, such as sandboxed MCP Apps.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/frontend/generative-ui-overview.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
