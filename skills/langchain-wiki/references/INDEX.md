# LangChain Python 文档索引

本文件由 `scripts/sync_wiki_docs.py` 生成。日常问答优先运行 `scripts/search_docs.py`，需要浏览主题结构时再读取本索引。

- 来源：<https://docs.langchain.com/oss/python/langchain/overview>
- 文档数：77

## 顶层目录

- `Advanced usage`：16 篇
- `Agent development`：6 篇
- `Core components`：8 篇
- `Error reference`：7 篇
- `Frontend`：20 篇
- `Get started`：4 篇
- `Learn`：10 篇
- `Middleware`：3 篇
- `Overview`：1 篇
- `Production`：2 篇

## 目录树

```text
docs/
├── Advanced usage
│   ├── MCP
│   │   ├── Authentication.md
│   │   ├── Connections.md
│   │   ├── Model Context Protocol (MCP).md
│   │   └── Tools.md
│   ├── Multi-agent
│   │   ├── Custom workflow.md
│   │   ├── Handoffs.md
│   │   ├── Multi-agent.md
│   │   ├── Router.md
│   │   ├── Skills.md
│   │   └── Subagents.md
│   ├── Context engineering in agents.md
│   ├── Guardrails.md
│   ├── Human-in-the-loop.md
│   ├── Long-term memory.md
│   ├── Retrieval.md
│   └── Runtime.md
├── Agent development
│   ├── Test
│   │   ├── Agent Evals.md
│   │   ├── Integration testing.md
│   │   ├── Test.md
│   │   └── Unit testing.md
│   ├── Agent Chat UI.md
│   └── LangSmith Studio.md
├── Core components
│   ├── Agents.md
│   ├── Event streaming.md
│   ├── Messages.md
│   ├── Models.md
│   ├── Short-term memory.md
│   ├── Streaming.md
│   ├── Structured output.md
│   └── Tools.md
├── Error reference
│   ├── INVALID_PROMPT_INPUT.md
│   ├── INVALID_TOOL_RESULTS.md
│   ├── MESSAGE_COERCION_FAILURE.md
│   ├── MODEL_AUTHENTICATION.md
│   ├── MODEL_NOT_FOUND.md
│   ├── MODEL_RATE_LIMIT.md
│   └── OUTPUT_PARSING_FAILURE.md
├── Frontend
│   ├── Integrations
│   │   ├── AI Elements.md
│   │   ├── assistant-ui.md
│   │   ├── CopilotKit.md
│   │   ├── OpenUI.md
│   │   └── Overview.md
│   ├── Patterns
│   │   ├── Generative UI
│   │   │   ├── Controlled generative UI.md
│   │   │   ├── Declarative generative UI.md
│   │   │   ├── Generative UI overview.md
│   │   │   └── Open-ended generative UI.md
│   │   ├── Branching chat.md
│   │   ├── Headless tools.md
│   │   ├── Human-in-the-Loop.md
│   │   ├── Join & rejoin streams.md
│   │   ├── Markdown messages.md
│   │   ├── Message queues.md
│   │   ├── Reasoning tokens.md
│   │   ├── Structured output.md
│   │   ├── Time travel.md
│   │   └── Tool calling.md
│   └── Overview.md
├── Get started
│   ├── Changelog.md
│   ├── Install LangChain.md
│   ├── Philosophy.md
│   └── Quickstart.md
├── Learn
│   ├── Additional resources
│   │   └── Get help.md
│   ├── Conceptual overviews
│   │   └── Component architecture.md
│   └── Tutorials
│       ├── LangChain
│       │   ├── Build a data analysis agent from scratch.md
│       │   ├── Build a semantic search engine with LangChain.md
│       │   ├── Build a SQL agent.md
│       │   └── Build a voice agent with LangChain.md
│       └── Multi-agent
│           ├── Build a multi-source knowledge base with routing.md
│           ├── Build a personal assistant with subagents.md
│           ├── Build a SQL assistant with on-demand skills.md
│           └── Build customer support with handoffs.md
├── Middleware
│   ├── Custom middleware.md
│   ├── Middleware overview.md
│   └── Prebuilt middleware.md
├── Overview
│   └── LangChain overview.md
└── Production
    ├── Deployment.md
    └── LangSmith Observability.md
```

## 全部文档

| 路径 | 标题 | 摘要 / 关键词 | 来源 |
|---|---|---|---|
| `Advanced usage/Context engineering in agents.md` | Context engineering in agents | [!TIP]；Advanced usage, Context engineering in agents, context-engineering | [原文](<https://docs.langchain.com/oss/python/langchain/context-engineering>) |
| `Advanced usage/Guardrails.md` | Guardrails | Implement safety checks and content filtering for your agents；Advanced usage, Guardrails, guardrails | [原文](<https://docs.langchain.com/oss/python/langchain/guardrails>) |
| `Advanced usage/Human-in-the-loop.md` | Human-in-the-loop | [!TIP]；Advanced usage, Human-in-the-loop, human-in-the-loop | [原文](<https://docs.langchain.com/oss/python/langchain/human-in-the-loop>) |
| `Advanced usage/Long-term memory.md` | Long-term memory | Add long-term memory to LangChain agents to store and recall data across conversations and sessions；Advanced usage, Long-term memory, long-term-memory | [原文](<https://docs.langchain.com/oss/python/langchain/long-term-memory>) |
| `Advanced usage/MCP/Authentication.md` | Authentication | Authenticate MCP connections with bearer tokens, OAuth 2.1, or per-user credentials in LangChain.；Advanced usage, Authentication, MCP, auth | [原文](<https://docs.langchain.com/oss/python/langchain/mcp/auth>) |
| `Advanced usage/MCP/Connections.md` | Connections | Connection lifecycle, multiple servers, deployment scaling, protocol eras, and caching for MCP in LangChain.；Advanced usage, Connections, MCP, connections | [原文](<https://docs.langchain.com/oss/python/langchain/mcp/connections>) |
| `Advanced usage/MCP/Model Context Protocol (MCP).md` | Model Context Protocol (MCP) | Connect LangChain agents to MCP servers with MCPAdapter.；Advanced usage, MCP, Model Context Protocol (MCP), mcp | [原文](<https://docs.langchain.com/oss/python/langchain/mcp>) |
| `Advanced usage/MCP/Tools.md` | Tools | Load MCP tools into LangChain agents, control their execution, and handle server results and requests.；Advanced usage, MCP, Tools, tools | [原文](<https://docs.langchain.com/oss/python/langchain/mcp/tools>) |
| `Advanced usage/Multi-agent/Custom workflow.md` | Custom workflow | [card] [Tutorial: Build a multi-source knowledge base with routing](https://docs.langchain.com/oss/python/langchain/multi-agent/router-knowledge-base.md)；Advanced usage, Custom workflow, Multi-agent, custom-workflow | [原文](<https://docs.langchain.com/oss/python/langchain/multi-agent/custom-workflow>) |
| `Advanced usage/Multi-agent/Handoffs.md` | Handoffs | [!TIP]；Advanced usage, Handoffs, Multi-agent, handoffs | [原文](<https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs>) |
| `Advanced usage/Multi-agent/Multi-agent.md` | Multi-agent | [!TIP]；Advanced usage, Multi-agent, multi-agent | [原文](<https://docs.langchain.com/oss/python/langchain/multi-agent>) |
| `Advanced usage/Multi-agent/Router.md` | Router | [tab] Single agent；Advanced usage, Multi-agent, Router, router | [原文](<https://docs.langchain.com/oss/python/langchain/multi-agent/router>) |
| `Advanced usage/Multi-agent/Skills.md` | Skills | [!TIP]；Advanced usage, Multi-agent, Skills, skills | [原文](<https://docs.langchain.com/oss/python/langchain/multi-agent/skills>) |
| `Advanced usage/Multi-agent/Subagents.md` | Subagents | [!NOTE]；Advanced usage, Multi-agent, Subagents, subagents | [原文](<https://docs.langchain.com/oss/python/langchain/multi-agent/subagents>) |
| `Advanced usage/Retrieval.md` | Retrieval | [!NOTE]；Advanced usage, Retrieval, retrieval | [原文](<https://docs.langchain.com/oss/python/deepagents/retrieval>) |
| `Advanced usage/Runtime.md` | Runtime | [!TIP]；Advanced usage, Runtime, runtime | [原文](<https://docs.langchain.com/oss/python/langchain/runtime>) |
| `Agent development/Agent Chat UI.md` | Agent Chat UI | [!TIP]；Agent Chat UI, Agent development, ui | [原文](<https://docs.langchain.com/oss/python/langchain/ui>) |
| `Agent development/LangSmith Studio.md` | LangSmith Studio | [!NOTE]；Agent development, LangSmith Studio, studio | [原文](<https://docs.langchain.com/oss/python/langchain/studio>) |
| `Agent development/Test/Agent Evals.md` | Agent Evals | Evaluate agent trajectories using deterministic matching or LLM-as-judge evaluators with AgentEvals and LangSmith.；Agent Evals, Agent development, Test, evals | [原文](<https://docs.langchain.com/oss/python/langchain/test/evals>) |
| `Agent development/Test/Integration testing.md` | Integration testing | Test agents with real LLM APIs by organizing tests, managing keys, handling flakiness, and controlling costs.；Agent development, Integration testing, Test, integration-testing | [原文](<https://docs.langchain.com/oss/python/langchain/test/integration-testing>) |
| `Agent development/Test/Test.md` | Test | Strategies for testing LangChain agents, including unit tests, integration tests, and trajectory evaluations.；Agent development, Test, test | [原文](<https://docs.langchain.com/oss/python/langchain/test>) |
| `Agent development/Test/Unit testing.md` | Unit testing | Test agent logic without API calls using fake chat models and in-memory persistence.；Agent development, Test, Unit testing, unit-testing | [原文](<https://docs.langchain.com/oss/python/langchain/test/unit-testing>) |
| `Core components/Agents.md` | Agents | Build a LangChain agent: a model calling tools in a loop until a task is complete, shaped by a harness of prompt, tools, and middleware.；Agents, Core components, agents | [原文](<https://docs.langchain.com/oss/python/langchain/agents>) |
| `Core components/Event streaming.md` | Event streaming | Stream real-time updates from LangChain agent runs；Core components, Event streaming, event-streaming | [原文](<https://docs.langchain.com/oss/python/langchain/event-streaming>) |
| `Core components/Messages.md` | Messages | [!TIP]；Core components, Messages, messages | [原文](<https://docs.langchain.com/oss/python/langchain/messages>) |
| `Core components/Models.md` | Models | Initialize and configure chat models, the reasoning engine of LangChain agents, with support for tool calling, structured output, and multimodal inputs.；Core components, Models, models | [原文](<https://docs.langchain.com/oss/python/langchain/models>) |
| `Core components/Short-term memory.md` | Short-term memory | [!NOTE]；Core components, Short-term memory, short-term-memory | [原文](<https://docs.langchain.com/oss/python/langchain/short-term-memory>) |
| `Core components/Streaming.md` | Streaming | Stream real-time updates from agent runs；Core components, Streaming, streaming | [原文](<https://docs.langchain.com/oss/python/langchain/streaming>) |
| `Core components/Structured output.md` | Structured output | [!TIP]；Core components, Structured output, structured-output | [原文](<https://docs.langchain.com/oss/python/langchain/structured-output>) |
| `Core components/Tools.md` | Tools | Define tools that let LangChain agents fetch real-time data, execute code, query external databases, and take actions.；Core components, Tools, tools | [原文](<https://docs.langchain.com/oss/python/langchain/tools>) |
| `Error reference/INVALID_PROMPT_INPUT.md` | INVALID_PROMPT_INPUT | INVALID_PROMPT_INPUT；Error reference, INVALID_PROMPT_INPUT | [原文](<https://docs.langchain.com/oss/python/langchain/errors/INVALID_PROMPT_INPUT>) |
| `Error reference/INVALID_TOOL_RESULTS.md` | INVALID_TOOL_RESULTS | [!NOTE]；Error reference, INVALID_TOOL_RESULTS | [原文](<https://docs.langchain.com/oss/python/langchain/errors/INVALID_TOOL_RESULTS>) |
| `Error reference/MESSAGE_COERCION_FAILURE.md` | MESSAGE_COERCION_FAILURE | MESSAGE_COERCION_FAILURE；Error reference, MESSAGE_COERCION_FAILURE | [原文](<https://docs.langchain.com/oss/python/langchain/errors/MESSAGE_COERCION_FAILURE>) |
| `Error reference/MODEL_AUTHENTICATION.md` | MODEL_AUTHENTICATION | [!NOTE]；Error reference, MODEL_AUTHENTICATION | [原文](<https://docs.langchain.com/oss/python/langchain/errors/MODEL_AUTHENTICATION>) |
| `Error reference/MODEL_NOT_FOUND.md` | MODEL_NOT_FOUND | [!NOTE]；Error reference, MODEL_NOT_FOUND | [原文](<https://docs.langchain.com/oss/python/langchain/errors/MODEL_NOT_FOUND>) |
| `Error reference/MODEL_RATE_LIMIT.md` | MODEL_RATE_LIMIT | [!NOTE]；Error reference, MODEL_RATE_LIMIT | [原文](<https://docs.langchain.com/oss/python/langchain/errors/MODEL_RATE_LIMIT>) |
| `Error reference/OUTPUT_PARSING_FAILURE.md` | OUTPUT_PARSING_FAILURE | [!NOTE]；Error reference, OUTPUT_PARSING_FAILURE | [原文](<https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE>) |
| `Frontend/Integrations/AI Elements.md` | AI Elements | Composable shadcn/ui-based components for AI chat interfaces with useStream；AI Elements, Frontend, Integrations, ai-elements | [原文](<https://docs.langchain.com/oss/python/langchain/frontend/integrations/ai-elements>) |
| `Frontend/Integrations/CopilotKit.md` | CopilotKit | Use CopilotKit with LangGraph, Deep Agents, and React with custom endpoints, the Python AG-UI bridge, structured generative UI, and messaging-platform channels；CopilotKit, Frontend, Integrations, copilotkit | [原文](<https://docs.langchain.com/oss/python/langchain/frontend/integrations/copilotkit>) |
| `Frontend/Integrations/OpenUI.md` | OpenUI | Generate complete, interactive dashboards and reports using the OpenUI component library and openui-lang；Frontend, Integrations, OpenUI, openui | [原文](<https://docs.langchain.com/oss/python/langchain/frontend/integrations/openui>) |
| `Frontend/Integrations/Overview.md` | Overview | Connect useStream to any React UI component library or generative UI framework；Frontend, Integrations, Overview, overview | [原文](<https://docs.langchain.com/oss/python/langchain/frontend/integrations/overview>) |
| `Frontend/Integrations/assistant-ui.md` | assistant-ui | Headless React AI chat framework with a full runtime layer, bridged to useStream；Frontend, Integrations, assistant-ui | [原文](<https://docs.langchain.com/oss/python/langchain/frontend/integrations/assistant-ui>) |
| `Frontend/Overview.md` | Overview | Build generative UIs with real-time streaming from LangChain agents；Frontend, Overview, overview | [原文](<https://docs.langchain.com/oss/python/langchain/frontend/overview>) |
| `Frontend/Patterns/Branching chat.md` | Branching chat | Edit messages and regenerate responses by forking from checkpoints；Branching chat, Frontend, Patterns, branching-chat | [原文](<https://docs.langchain.com/oss/python/langchain/frontend/branching-chat>) |
| `Frontend/Patterns/Generative UI/Controlled generative UI.md` | Controlled generative UI | Render agent output with components you author using components as tools, tool-call rendering, state rendering, and reasoning；Controlled generative UI, Frontend, Generative UI, Patterns, controlled-generative-ui | [原文](<https://docs.langchain.com/oss/python/langchain/frontend/controlled-generative-ui>) |
| `Frontend/Patterns/Generative UI/Declarative generative UI.md` | Declarative generative UI | Compose agent-generated interfaces from a registered component catalog using json-render and A2UI；Declarative generative UI, Frontend, Generative UI, Patterns, declarative-generative-ui | [原文](<https://docs.langchain.com/oss/python/langchain/frontend/declarative-generative-ui>) |
| `Frontend/Patterns/Generative UI/Generative UI overview.md` | Generative UI overview | Understand the generative UI spectrum from controlled to declarative to open-ended interfaces；Frontend, Generative UI, Generative UI overview, Patterns, generative-ui-overview | [原文](<https://docs.langchain.com/oss/python/langchain/frontend/generative-ui-overview>) |
| `Frontend/Patterns/Generative UI/Open-ended generative UI.md` | Open-ended generative UI | Render UI created outside your application, such as sandboxed MCP Apps, at the open end of the generative UI spectrum；Frontend, Generative UI, Open-ended generative UI, Patterns, open-ended-generative-ui | [原文](<https://docs.langchain.com/oss/python/langchain/frontend/open-ended-generative-ui>) |
| `Frontend/Patterns/Headless tools.md` | Headless tools | Run browser and device APIs on the client with headless tool implementations；Frontend, Headless tools, Patterns, headless-tools | [原文](<https://docs.langchain.com/oss/python/langchain/frontend/headless-tools>) |
| `Frontend/Patterns/Human-in-the-Loop.md` | Human-in-the-Loop | Add approval workflows with interrupt-based human review；Frontend, Human-in-the-Loop, Patterns, human-in-the-loop | [原文](<https://docs.langchain.com/oss/python/langchain/frontend/human-in-the-loop>) |
| `Frontend/Patterns/Join & rejoin streams.md` | Join & rejoin streams | Disconnect from and reconnect to running agent streams；Frontend, Join & rejoin streams, Patterns, join-rejoin | [原文](<https://docs.langchain.com/oss/python/langchain/frontend/join-rejoin>) |
| `Frontend/Patterns/Markdown messages.md` | Markdown messages | Render LLM responses as rich, formatted markdown with proper streaming support；Frontend, Markdown messages, Patterns, markdown-messages | [原文](<https://docs.langchain.com/oss/python/langchain/frontend/markdown-messages>) |
| `Frontend/Patterns/Message queues.md` | Message queues | Queue multiple messages and manage them while the agent processes sequentially；Frontend, Message queues, Patterns, message-queues | [原文](<https://docs.langchain.com/oss/python/langchain/frontend/message-queues>) |
| `Frontend/Patterns/Reasoning tokens.md` | Reasoning tokens | Display model thinking and reasoning processes in collapsible blocks；Frontend, Patterns, Reasoning tokens, reasoning-tokens | [原文](<https://docs.langchain.com/oss/python/langchain/frontend/reasoning-tokens>) |
| `Frontend/Patterns/Structured output.md` | Structured output | Render structured agent responses with custom UI components instead of plain text；Frontend, Patterns, Structured output, structured-output | [原文](<https://docs.langchain.com/oss/python/langchain/frontend/structured-output>) |
| `Frontend/Patterns/Time travel.md` | Time travel | Inspect, navigate, and resume from any checkpoint in the conversation history；Frontend, Patterns, Time travel, time-travel | [原文](<https://docs.langchain.com/oss/python/langchain/frontend/time-travel>) |
| `Frontend/Patterns/Tool calling.md` | Tool calling | Display agent tool calls with rich, type-safe UI cards；Frontend, Patterns, Tool calling, tool-calling | [原文](<https://docs.langchain.com/oss/python/langchain/frontend/tool-calling>) |
| `Get started/Changelog.md` | Changelog | Log of updates and improvements to our Python packages；Changelog, Get started, changelog | [原文](<https://docs.langchain.com/oss/python/releases/changelog>) |
| `Get started/Install LangChain.md` | Install LangChain | Install the LangChain package and the independent provider packages for the models and integrations you use.；Get started, Install LangChain, install | [原文](<https://docs.langchain.com/oss/python/langchain/install>) |
| `Get started/Philosophy.md` | Philosophy | LangChain exists to be the easiest place to start building with LLMs, while also being flexible and production-ready.；Get started, Philosophy, philosophy | [原文](<https://docs.langchain.com/oss/python/langchain/philosophy>) |
| `Get started/Quickstart.md` | Quickstart | Build your first agent in minutes；Get started, Quickstart, quickstart | [原文](<https://docs.langchain.com/oss/python/langchain/quickstart>) |
| `Learn/Additional resources/Get help.md` | Get help | Get help；Additional resources, Get help, Learn, get-help | [原文](<https://docs.langchain.com/oss/python/langchain/get-help>) |
| `Learn/Conceptual overviews/Component architecture.md` | Component architecture | Component architecture；Component architecture, Conceptual overviews, Learn, component-architecture | [原文](<https://docs.langchain.com/oss/python/langchain/component-architecture>) |
| `Learn/Tutorials/LangChain/Build a SQL agent.md` | Build a SQL agent | [!WARNING]；Build a SQL agent, LangChain, Learn, Tutorials, sql-agent | [原文](<https://docs.langchain.com/oss/python/langchain/sql-agent>) |
| `Learn/Tutorials/LangChain/Build a data analysis agent from scratch.md` | Build a data analysis agent from scratch | Build a data analysis agent step by step using create_agent and Deep Agents middleware.；Build a data analysis agent from scratch, LangChain, Learn, Tutorials, deep-agent-from-scratch | [原文](<https://docs.langchain.com/oss/python/langchain/deep-agent-from-scratch>) |
| `Learn/Tutorials/LangChain/Build a semantic search engine with LangChain.md` | Build a semantic search engine with LangChain | [tab] OpenAI；Build a semantic search engine with LangChain, LangChain, Learn, Tutorials, knowledge-base | [原文](<https://docs.langchain.com/oss/python/langchain/knowledge-base>) |
| `Learn/Tutorials/LangChain/Build a voice agent with LangChain.md` | Build a voice agent with LangChain | [accordion] AssemblyAI Client；Build a voice agent with LangChain, LangChain, Learn, Tutorials, voice-agent | [原文](<https://docs.langchain.com/oss/python/langchain/voice-agent>) |
| `Learn/Tutorials/Multi-agent/Build a SQL assistant with on-demand skills.md` | Build a SQL assistant with on-demand skills | [!NOTE]；Build a SQL assistant with on-demand skills, Learn, Multi-agent, Tutorials, skills-sql-assistant | [原文](<https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant>) |
| `Learn/Tutorials/Multi-agent/Build a multi-source knowledge base with routing.md` | Build a multi-source knowledge base with routing | [!TIP]；Build a multi-source knowledge base with routing, Learn, Multi-agent, Tutorials, router-knowledge-base | [原文](<https://docs.langchain.com/oss/python/langchain/multi-agent/router-knowledge-base>) |
| `Learn/Tutorials/Multi-agent/Build a personal assistant with subagents.md` | Build a personal assistant with subagents | [!NOTE]；Build a personal assistant with subagents, Learn, Multi-agent, Tutorials, subagents-personal-assistant | [原文](<https://docs.langchain.com/oss/python/langchain/multi-agent/subagents-personal-assistant>) |
| `Learn/Tutorials/Multi-agent/Build customer support with handoffs.md` | Build customer support with handoffs | [tab] OpenAI；Build customer support with handoffs, Learn, Multi-agent, Tutorials, handoffs-customer-support | [原文](<https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs-customer-support>) |
| `Middleware/Custom middleware.md` | Custom middleware | [card] [Node-style hooks](#node-style-hooks)；Custom middleware, Middleware, custom | [原文](<https://docs.langchain.com/oss/python/langchain/middleware/custom>) |
| `Middleware/Middleware overview.md` | Middleware overview | Control and customize agent execution at every step；Middleware, Middleware overview, overview | [原文](<https://docs.langchain.com/oss/python/langchain/middleware/overview>) |
| `Middleware/Prebuilt middleware.md` | Prebuilt middleware | Prebuilt middleware for common agent use cases；Middleware, Prebuilt middleware, built-in | [原文](<https://docs.langchain.com/oss/python/langchain/middleware/built-in>) |
| `Overview/LangChain overview.md` | LangChain overview | LangChain provides create_agent: a minimal, highly configurable agent harness. Compose exactly the agent your use case needs from model, tools, prompt, and middleware.；LangChain overview, Overview, overview | [原文](<https://docs.langchain.com/oss/python/langchain/overview>) |
| `Production/Deployment.md` | Deployment | Deploy LangChain agents to production with LangSmith Cloud or JavaScript frameworks and hosting platforms.；Deployment, Production, deploy | [原文](<https://docs.langchain.com/oss/python/langchain/deploy>) |
| `Production/LangSmith Observability.md` | LangSmith Observability | [!NOTE]；LangSmith Observability, Production, observability | [原文](<https://docs.langchain.com/oss/python/langchain/observability>) |
