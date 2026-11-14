# Controlled generative UI

> Render agent output with components you author using components as tools, tool-call rendering, state rendering, and reasoning

## Overview

Controlled generative UI is at the author-controlled end of the
[generative UI spectrum](Generative%20UI%20overview.md). You write the
components, and the agent decides which one to render and what data to pass into
it. The agent never produces markup: it chooses from a fixed set of interfaces you
build and test.

This pattern gives the highest predictability of any generative UI approach.
Because every component ships from your codebase, you control branding, layout,
accessibility, and behavior exactly, and you can guarantee that whatever the agent
surfaces has already passed your review. The tradeoff is engineering cost: each new
capability needs a component you write in advance. Your component library is the
boundary: the agent can only render what you shipped.

## When to use this approach

Reach for controlled generative UI on your highest-traffic, brand-critical surfaces,
where the set of outputs is known ahead of time and correctness matters more than
novelty: forms, confirmation flows, and any surface with strict branding or
accessibility requirements. When you need the agent to compose layouts you did not
anticipate, across the long tail of secondary interactions, move one step further
along the spectrum to [declarative generative UI](Declarative%20generative%20UI.md).

Controlled generative UI covers four techniques, starting with the agent picking a
whole interface and ending with the frontend reacting to agent internals.

## Components as tools

You expose UI components to the agent the way you expose tools. Each component has a
name, a description, and a typed set of properties, and the agent selects a component
and supplies its data as part of its response. The frontend maps the agent's choice
to your real implementation. This keeps the agent's job small, deciding which
pre-approved interface fits the moment, while your code owns everything about how it
looks and behaves.

CopilotKit documents this pattern as [components as tools](https://docs.copilotkit.ai/generative-ui/tool-based).

## Tool-call rendering

When an agent calls a tool, the call moves through a lifecycle: pending, then
complete or failed. Tool-call rendering turns each stage into purpose-built UI, such
as a loading card while a search runs, a result card when it returns, and an error
state if it fails, instead of showing raw JSON. This makes the agent's actions
legible and gives users confidence in what is happening.

See the [Tool calling](../Tool%20calling.md) pattern.

## State rendering

Agents expose durable, typed state beyond the message list: todos, pipeline
outputs, citations, sandbox files, metrics, and custom business objects. State
rendering binds your components to that state so the UI becomes a live view of the
agent's work rather than a transcript. As the agent updates state, the interface
updates with it.

See [typed agent state](../../Overview.md) in the frontend overview.
For mapping a single typed response payload to custom UI, see
[Structured output](../Structured%20output.md).

## Reasoning

Models with extended thinking produce reasoning separate from their final answer.
Rendering reasoning shows users how the agent arrived at a result, which builds
trust, aids debugging, and supports auditing. You control how and when the reasoning
appears, for example in a collapsible block distinct from the response.

See the [Reasoning tokens](../Reasoning%20tokens.md) pattern.

## See also

* [Generative UI overview](Generative%20UI%20overview.md)
* [Declarative generative UI](Declarative%20generative%20UI.md)
* [Open-ended generative UI](Open-ended%20generative%20UI.md)

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/frontend/controlled-generative-ui.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
