# Open-ended generative UI

> Render UI created outside your application, such as sandboxed MCP Apps, at the open end of the generative UI spectrum

## Overview

Open-ended generative UI is at the agent-created end of the
[generative UI spectrum](Generative%20UI%20overview.md). The interface is
authored outside your application, for example by an MCP server, and your frontend
renders it inside a sandbox. Neither you nor the agent writes the components: a
third party ships them, and your app hosts them.

This approach gives the widest expressive range: the agent owns the canvas. A
capability can arrive with its own interface already built, so you can surface
interactive tools you never implemented, with no frontend code on your side. It
suits one-off visualizations and bespoke answers where a result that is surprising
and good enough beats one that is predictable. It is also the most experimental
approach, the least deterministic, slower, and more expensive to run, and untrusted
UI is the hardest to make consistent, accessible, and safe, so it must be isolated
from the rest of your application.

## When to use this approach

Reach for open-ended generative UI when you want to surface capabilities and
interfaces that live outside your application and evolve independently of it, such
as tools published by an ecosystem of MCP servers. When you need to guarantee
branding, accessibility, or layout, move back along the spectrum toward
[declarative](Declarative%20generative%20UI.md) or
[controlled](Controlled%20generative%20UI.md) generative UI, where
your application owns the components.

## MCP Apps

The [Model Context Protocol](https://modelcontextprotocol.io) lets an agent connect
to external servers that provide tools and resources. MCP Apps extend that idea to
interface: an MCP server ships interactive UI, and the frontend renders it, usually
in an iframe, directly in the conversation. The server owns the components, the
data, and the interactions, while your application provides the frame and the
connection to the agent.

CopilotKit documents this pattern as [MCP Apps](https://docs.copilotkit.ai/generative-ui/mcp-apps).

## Sandboxing and safety

Because the interface comes from a third party, treat it as untrusted. Render it in
an isolated context, such as a sandboxed iframe, and constrain what it can access so
a misbehaving or malicious app cannot reach the rest of your page or your users'
data. Sandboxing is what makes the open end of the spectrum usable in production:
it contains the expressive range rather than limiting it.

## See also

* [Generative UI overview](Generative%20UI%20overview.md)
* [Controlled generative UI](Controlled%20generative%20UI.md)
* [Declarative generative UI](Declarative%20generative%20UI.md)

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/frontend/open-ended-generative-ui.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
