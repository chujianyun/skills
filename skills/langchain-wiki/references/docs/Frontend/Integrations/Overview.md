# Overview

> Connect useStream to any React UI component library or generative UI framework

[`useStream`](https://reference.langchain.com/javascript/langchain-react/index/useStream) is UI-agnostic. It returns plain reactive state with messages, tool calls, loading flags, values, and thread metadata that you wire to any visual layer you choose. These pages show how different libraries integrate with LangChain frontends, each with a different philosophy for building AI chat and generative UI.

## Integrations

> [card] [CopilotKit](CopilotKit.md)
>
> Full AI chat runtime with structured generative UI support. Add a custom CopilotKit endpoint to your LangGraph deployment, then render dynamic component trees in React.

> [card] [AI Elements](AI%20Elements.md)
>
> Composable shadcn/ui-based components for AI chat. Drop in `Conversation`, `Message`, `Tool`, and `Reasoning` and wire them directly to `stream.messages`.

> [card] [assistant-ui](assistant-ui.md)
>
> Headless React framework with a full runtime layer. Bridge `useStream` to `AssistantRuntimeProvider` via the `useExternalStoreRuntime` adapter.

> [card] [OpenUI](OpenUI.md)
>
> Generative UI library that lets the agent produce complete, interactive dashboards in a declarative component DSL. Purpose-built for data-rich, report-style UIs.

## Choosing a library

Each library fits a slightly different integration model. The choice depends on what kind of UI you're building:

| | CopilotKit | AI Elements | assistant-ui | OpenUI |
| - | - | - | - | - |
| **Best for** | Full chat runtime plus structured generative UI | Chat with rich message types | Full-featured chat with minimal setup | Generated dashboards and reports |
| **UI style** | CopilotKit chat shell + custom message renderers | Composable shadcn/ui components | Headless slots + default theme | Prebuilt component library with declarative DSL |
| **Customization** | Custom backend endpoint, agent context, and renderers | Edit source files directly | Override component slots | Theme via CSS custom properties |
| **Streaming UX** | Runtime-managed chat stream with structured assistant payloads | Component-level progressive render | Built-in thread management | Hoisting: shell appears immediately, data fills in |
| **Tool calls** | Via CopilotKit runtime and custom renderers | `Tool` / `ToolHeader` / `ToolOutput` | Custom via message slots | Inline in the generated UI |
| **Agent format** | Structured assistant responses plus optional Markdown | Any `stream.messages` | Any `stream.messages` | Agent outputs openui-lang text |

All four work well with LangChain agents, and the latter three also connect directly to [`useStream`](https://reference.langchain.com/javascript/langchain-react/index/useStream). CopilotKit is especially useful when you want a richer runtime layer and a dedicated endpoint that can sit alongside a [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview.md) deployment.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/frontend/integrations/overview.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
