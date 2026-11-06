# Deep Agents 文档索引

本文件由 `scripts/sync_wiki_docs.py` 生成。日常问答优先运行 `scripts/search_docs.py`，需要浏览主题结构时再读取本索引。

- 来源：<https://docs.langchain.com/oss/python/deepagents>
- 文档数：44

## 顶层目录

- `(root)`：1 篇
- `Context management`：6 篇
- `Delegation`：3 篇
- `Deployment`：3 篇
- `Examples`：4 篇
- `Execution environment`：9 篇
- `Frontend`：4 篇
- `Get started`：5 篇
- `Middleware`：3 篇
- `Protocols`：4 篇
- `Steering`：2 篇

## 目录树

```text
docs/
├── Context management
│   ├── Context engineering in Deep Agents.md
│   ├── Memory.md
│   ├── OpenWiki.md
│   ├── Profiles.md
│   ├── Retrieval.md
│   └── Skills.md
├── Delegation
│   ├── Async subagents.md
│   ├── Dynamic subagents.md
│   └── Subagents.md
├── Deployment
│   ├── Going to production
│   │   ├── Fault tolerance.md
│   │   └── index.md
│   └── Managed Deep Agents.md
├── Examples
│   └── Deep Agents
│       ├── Build a content builder agent.md
│       ├── Build a data analysis agent.md
│       ├── Build a deep research agent.md
│       └── Retrieval Augmented Generation (RAG) with Deep Agents.md
├── Execution environment
│   ├── Backends.md
│   ├── Browser use.md
│   ├── Event streaming.md
│   ├── Interpreters.md
│   ├── Multimodal inputs and outputs.md
│   ├── Permissions.md
│   ├── Sandboxes.md
│   ├── Streaming.md
│   └── Tools.md
├── Frontend
│   ├── Patterns
│   │   ├── Sandbox.md
│   │   ├── Subagent streaming.md
│   │   └── Todo list.md
│   └── Overview.md
├── Get started
│   ├── Changelog.md
│   ├── Comparison with Claude Agent SDK.md
│   ├── Customize Deep Agents.md
│   ├── Models.md
│   └── Quickstart.md
├── Middleware
│   ├── Custom middleware.md
│   ├── Middleware overview.md
│   └── Prebuilt middleware.md
├── Protocols
│   ├── A2A endpoint in Agent Server.md
│   ├── Agent Client Protocol (ACP).md
│   ├── Agent User Interaction Protocol (AG-UI).md
│   └── Model Context Protocol (MCP).md
├── Steering
│   ├── Grading rubrics.md
│   └── Human-in-the-loop.md
└── Deep Agents overview.md
```

## 全部文档

| 路径 | 标题 | 摘要 / 关键词 | 来源 |
|---|---|---|---|
| `Context management/Context engineering in Deep Agents.md` | Context engineering in Deep Agents | Control what context your deep agent has access to and how it is managed across long-running tasks；Context management, context-engineering | [原文](<https://docs.langchain.com/oss/python/deepagents/context-engineering>) |
| `Context management/Memory.md` | Memory | Add persistent memory to agents built with Deep Agents so they learn and improve across conversations；Context management, memory | [原文](<https://docs.langchain.com/oss/python/deepagents/memory>) |
| `Context management/OpenWiki.md` | OpenWiki | CLI that writes and maintains agent wikis so coding agents work faster；Context management, openwiki | [原文](<https://docs.langchain.com/oss/openwiki/overview>) |
| `Context management/Profiles.md` | Profiles | Package per-provider and per-model defaults that Deep Agents applies when a model is selected；Context management, profiles | [原文](<https://docs.langchain.com/oss/python/deepagents/profiles>) |
| `Context management/Retrieval.md` | Retrieval | [!NOTE]；Context management, retrieval | [原文](<https://docs.langchain.com/oss/python/deepagents/retrieval>) |
| `Context management/Skills.md` | Skills | Learn how to extend your deep agent's capabilities with skills；Context management, skills | [原文](<https://docs.langchain.com/oss/python/deepagents/skills>) |
| `Deep Agents overview.md` | Deep Agents overview | Agent harness for planning, subagents, and file-system context, available as Managed Deep Agents or the Deep Agents SDK；overview | [原文](<https://docs.langchain.com/oss/python/deepagents/overview>) |
| `Delegation/Async subagents.md` | Async subagents | Launch background subagents that run concurrently while the supervisor continues interacting with the user；Delegation, async-subagents | [原文](<https://docs.langchain.com/oss/python/deepagents/async-subagents>) |
| `Delegation/Dynamic subagents.md` | Dynamic subagents | Use interpreters to dispatch and orchestrate Deep Agents subagents from code；Delegation, dynamic-subagents | [原文](<https://docs.langchain.com/oss/python/deepagents/dynamic-subagents>) |
| `Delegation/Subagents.md` | Subagents | Learn how to use subagents to delegate work and keep context clean；Delegation, subagents | [原文](<https://docs.langchain.com/oss/python/deepagents/subagents>) |
| `Deployment/Going to production/Fault tolerance.md` | Fault tolerance | Make your deep agent resilient with rate limiting, retries, fallbacks, and error handling；Deployment, Going to production, fault-tolerance | [原文](<https://docs.langchain.com/oss/python/deepagents/fault-tolerance>) |
| `Deployment/Going to production/index.md` | Going to production | Take your deep agent to production with persistent memory, sandboxes, resilience middleware, and deployment options；Deployment, Going to production, going-to-production | [原文](<https://docs.langchain.com/oss/python/deepagents/going-to-production>) |
| `Deployment/Managed Deep Agents.md` | Managed Deep Agents | Build your agent as a directory of files while LangSmith runs the harness and runtime.；Deployment, managed-deep-agents | [原文](<https://docs.langchain.com/langsmith/python/managed-deep-agents-overview>) |
| `Examples/Deep Agents/Build a content builder agent.md` | Build a content builder agent | Build a content writing agent with brand voice, skills, subagents, and image generation using Managed Deep Agents or the Deep Agents SDK；Deep Agents, Examples, content-builder | [原文](<https://docs.langchain.com/oss/python/deepagents/content-builder>) |
| `Examples/Deep Agents/Build a data analysis agent.md` | Build a data analysis agent | Build an agent that analyzes data files, generates visualizations, and shares results；Deep Agents, Examples, data-analysis | [原文](<https://docs.langchain.com/oss/python/deepagents/data-analysis>) |
| `Examples/Deep Agents/Build a deep research agent.md` | Build a deep research agent | Build a multi-step web research agent with subagent delegation using Managed Deep Agents or the Deep Agents SDK；Deep Agents, Examples, deep-research | [原文](<https://docs.langchain.com/oss/python/deepagents/deep-research>) |
| `Examples/Deep Agents/Retrieval Augmented Generation (RAG) with Deep Agents.md` | Retrieval Augmented Generation (RAG) with Deep Agents | RAG patterns for Deep Agents, including skills-guided retrieval, rubric grading, and a tutorial that indexes LangChain docs, offloads chunks to the filesystem, and delegates analysis to subagents；Deep Agents, Examples, rag | [原文](<https://docs.langchain.com/oss/python/deepagents/rag>) |
| `Execution environment/Backends.md` | Backends | Choose and configure filesystem backends for Deep Agents. You can specify routes to different backends, implement virtual filesystems, and enforce policies.；Execution environment, backends | [原文](<https://docs.langchain.com/oss/python/deepagents/backends>) |
| `Execution environment/Browser use.md` | Browser use | Give a deep agent a browser so it can take actions on websites and test web apps end to end.；Execution environment, browser-use | [原文](<https://docs.langchain.com/oss/python/deepagents/browser-use>) |
| `Execution environment/Event streaming.md` | Event streaming | Stream subagents, messages, tool calls, and final output from Deep Agents.；Execution environment, event-streaming | [原文](<https://docs.langchain.com/oss/python/deepagents/event-streaming>) |
| `Execution environment/Interpreters.md` | Interpreters | Run lightweight code inside Deep Agents to compose tools, orchestrate subagents, and transform structured data；Execution environment, interpreters | [原文](<https://docs.langchain.com/oss/python/deepagents/interpreters>) |
| `Execution environment/Multimodal inputs and outputs.md` | Multimodal inputs and outputs | Use images, audio, video, and documents with Deep Agents when your model supports multimodal inputs and tool results；Execution environment, multimodal | [原文](<https://docs.langchain.com/oss/python/deepagents/multimodal>) |
| `Execution environment/Permissions.md` | Permissions | Control filesystem access with declarative permission rules for Deep Agents；Execution environment, permissions | [原文](<https://docs.langchain.com/oss/python/deepagents/permissions>) |
| `Execution environment/Sandboxes.md` | Sandboxes | Execute code in isolated environments with sandbox backends；Execution environment, sandboxes | [原文](<https://docs.langchain.com/oss/python/deepagents/sandboxes>) |
| `Execution environment/Streaming.md` | Streaming | Stream real-time updates from deep agent runs and subagent execution；Execution environment, streaming | [原文](<https://docs.langchain.com/oss/python/deepagents/streaming>) |
| `Execution environment/Tools.md` | Tools | Connect Deep Agents to custom functions, APIs, databases, and any MCP server；Execution environment, tools | [原文](<https://docs.langchain.com/oss/python/deepagents/tools>) |
| `Frontend/Overview.md` | Overview | Build UIs that display real-time subagent streams, task progress, and sandbox for Deep Agents；Frontend, overview | [原文](<https://docs.langchain.com/oss/python/deepagents/frontend/overview>) |
| `Frontend/Patterns/Sandbox.md` | Sandbox | Build an IDE-like UI for a coding agent backed by a sandbox environment；Frontend, Patterns, sandbox | [原文](<https://docs.langchain.com/oss/python/deepagents/frontend/sandbox>) |
| `Frontend/Patterns/Subagent streaming.md` | Subagent streaming | Display specialist subagents with streaming content, progress tracking, and collapsible cards；Frontend, Patterns, subagent-streaming | [原文](<https://docs.langchain.com/oss/python/deepagents/frontend/subagent-streaming>) |
| `Frontend/Patterns/Todo list.md` | Todo list | Track agent progress with a real-time todo list synced from agent state；Frontend, Patterns, todo-list | [原文](<https://docs.langchain.com/oss/python/deepagents/frontend/todo-list>) |
| `Get started/Changelog.md` | Changelog | Log of updates and improvements to our Python packages；Get started, changelog-py | [原文](<https://docs.langchain.com/oss/python/releases/changelog>) |
| `Get started/Comparison with Claude Agent SDK.md` | Comparison with Claude Agent SDK | Compare LangChain Deep Agents and Managed Deep Agents with the Claude Agent SDK to choose the right tool for your use case.；Get started, comparison | [原文](<https://docs.langchain.com/oss/python/deepagents/comparison>) |
| `Get started/Customize Deep Agents.md` | Customize Deep Agents | Learn how to customize Deep Agents with system prompts, tools, subagents, and more；Get started, customization | [原文](<https://docs.langchain.com/oss/python/deepagents/customization>) |
| `Get started/Models.md` | Models | Configure model providers and parameters for Deep Agents；Get started, models | [原文](<https://docs.langchain.com/oss/python/deepagents/models>) |
| `Get started/Quickstart.md` | Quickstart | Build your first deep agent in minutes；Get started, quickstart | [原文](<https://docs.langchain.com/oss/python/deepagents/quickstart>) |
| `Middleware/Custom middleware.md` | Custom middleware | [card] [Node-style hooks](#node-style-hooks)；Middleware, custom | [原文](<https://docs.langchain.com/oss/python/langchain/middleware/custom>) |
| `Middleware/Middleware overview.md` | Middleware overview | Control and customize agent execution at every step；Middleware, overview | [原文](<https://docs.langchain.com/oss/python/langchain/middleware/overview>) |
| `Middleware/Prebuilt middleware.md` | Prebuilt middleware | Prebuilt middleware for common agent use cases；Middleware, built-in | [原文](<https://docs.langchain.com/oss/python/langchain/middleware/built-in>) |
| `Protocols/A2A endpoint in Agent Server.md` | A2A endpoint in Agent Server | Use the A2A protocol to enable agent-to-agent communication with distributed tracing in LangSmith.；Protocols, a2a | [原文](<https://docs.langchain.com/langsmith/server-a2a>) |
| `Protocols/Agent Client Protocol (ACP).md` | Agent Client Protocol (ACP) | Expose Deep Agents over the Agent Client Protocol (ACP) to integrate with code editors and IDEs.；Protocols, acp | [原文](<https://docs.langchain.com/oss/python/deepagents/acp>) |
| `Protocols/Agent User Interaction Protocol (AG-UI).md` | Agent User Interaction Protocol (AG-UI) | Expose deep agents over the Agent User Interaction Protocol (AG-UI) to stream events to any AG-UI client or frontend.；Protocols, ag-ui | [原文](<https://docs.langchain.com/oss/python/deepagents/ag-ui>) |
| `Protocols/Model Context Protocol (MCP).md` | Model Context Protocol (MCP) | Connect LangChain agents to MCP servers with MCPAdapter.；Protocols, mcp | [原文](<https://docs.langchain.com/oss/python/langchain/mcp>) |
| `Steering/Grading rubrics.md` | Grading rubrics | LLM-as-a-judge grading for agents that iterate against a rubric until done；Steering, rubric | [原文](<https://docs.langchain.com/oss/python/deepagents/rubric>) |
| `Steering/Human-in-the-loop.md` | Human-in-the-loop | Learn how to configure human approval for sensitive tool operations；Steering, human-in-the-loop | [原文](<https://docs.langchain.com/oss/python/deepagents/human-in-the-loop>) |
