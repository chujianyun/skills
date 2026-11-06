# LangGraph Python 文档索引

本文件由 `scripts/sync_wiki_docs.py` 生成。日常问答优先运行 `scripts/search_docs.py`，需要浏览主题结构时再读取本索引。

- 来源：<https://docs.langchain.com/oss/python/langgraph>
- 文档数：53

## 顶层目录

- `(root)`：2 篇
- `Advanced`：9 篇
- `Build with the Graph API`：8 篇
- `Capabilities`：10 篇
- `Deployment`：8 篇
- `Frontend`：3 篇
- `Get started`：3 篇
- `Learn`：3 篇
- `Patterns`：1 篇
- `Reference`：6 篇

## 目录树

```text
docs/
├── Advanced
│   ├── Build with the Functional API
│   │   ├── Add human-in-the-loop with the Functional API.md
│   │   ├── Add memory with the Functional API.md
│   │   ├── Build checklist for the Functional API.md
│   │   ├── Compose Functional API workflows.md
│   │   ├── Configure Functional API tasks.md
│   │   ├── Functional API overview.md
│   │   ├── Stream with the Functional API.md
│   │   └── Thinking in the Functional API.md
│   └── LangGraph runtime.md
├── Build with the Graph API
│   ├── Build checklist for the Graph API.md
│   ├── Build sequences, branches, and loops.md
│   ├── Configure nodes.md
│   ├── Define and update state.md
│   ├── Graph API overview.md
│   ├── Thinking in the Graph API.md
│   ├── Use Send and Command.md
│   └── Visualize your graph.md
├── Capabilities
│   ├── Checkpointers.md
│   ├── Event streaming.md
│   ├── Fault tolerance.md
│   ├── Interrupts.md
│   ├── Memory.md
│   ├── Persistence.md
│   ├── Stores.md
│   ├── Streaming.md
│   ├── Subgraphs.md
│   └── Use time-travel.md
├── Deployment
│   ├── Agent Chat UI.md
│   ├── Application structure.md
│   ├── Backward compatibility.md
│   ├── Deployment.md
│   ├── LangSmith Observability.md
│   ├── LangSmith Studio.md
│   ├── Run a local server.md
│   └── Test.md
├── Frontend
│   ├── Custom stream channels.md
│   ├── Graph execution.md
│   └── Overview.md
├── Get started
│   ├── Changelog.md
│   ├── Choosing between Graph and Functional APIs.md
│   └── Quickstart.md
├── Learn
│   ├── Additional resources
│   │   └── Case studies.md
│   └── Tutorials
│       ├── Build a custom RAG agent with LangGraph.md
│       └── Build a custom SQL agent.md
├── Patterns
│   └── Workflows and agents.md
├── Reference
│   └── Errors
│       ├── GRAPH_RECURSION_LIMIT.md
│       ├── INVALID_CHAT_HISTORY.md
│       ├── INVALID_CONCURRENT_GRAPH_UPDATE.md
│       ├── INVALID_GRAPH_NODE_RETURN_VALUE.md
│       ├── MISSING_CHECKPOINTER.md
│       └── MULTIPLE_SUBGRAPHS.md
├── LangGraph overview.md
└── LangSmith Studio.md
```

## 全部文档

| 路径 | 标题 | 摘要 / 关键词 | 来源 |
|---|---|---|---|
| `Advanced/Build with the Functional API/Add human-in-the-loop with the Functional API.md` | Add human-in-the-loop with the Functional API | Pause Functional API workflows for approval and review tool calls with interrupts.；Advanced, Build with the Functional API, api, functional, human, in, loop, the | [原文](<https://docs.langchain.com/oss/python/langgraph/functional-api-human-in-the-loop>) |
| `Advanced/Build with the Functional API/Add memory with the Functional API.md` | Add memory with the Functional API | Use short-term checkpoints and long-term store memory in Functional API workflows.；Advanced, Build with the Functional API, api, functional, memory | [原文](<https://docs.langchain.com/oss/python/langgraph/functional-api-memory>) |
| `Advanced/Build with the Functional API/Build checklist for the Functional API.md` | Build checklist for the Functional API | Decide how to compose entrypoints, tasks, streaming, interrupts, and memory with the Functional API.；Advanced, Build with the Functional API, api, functional, use | [原文](<https://docs.langchain.com/oss/python/langgraph/use-functional-api>) |
| `Advanced/Build with the Functional API/Compose Functional API workflows.md` | Compose Functional API workflows | Build entrypoints and tasks, run work in parallel, and call graphs or other entrypoints.；Advanced, Build with the Functional API, api, functional, workflows | [原文](<https://docs.langchain.com/oss/python/langgraph/functional-api-workflows>) |
| `Advanced/Build with the Functional API/Configure Functional API tasks.md` | Configure Functional API tasks | Add retries, timeouts, caching, and error recovery to Functional API tasks and entrypoints.；Advanced, Build with the Functional API, api, functional, tasks | [原文](<https://docs.langchain.com/oss/python/langgraph/functional-api-tasks>) |
| `Advanced/Build with the Functional API/Functional API overview.md` | Functional API overview | Learn Functional API entrypoints and tasks, how checkpointing and replay work, and how to avoid common resume pitfalls.；Advanced, Build with the Functional API, api, functional | [原文](<https://docs.langchain.com/oss/python/langgraph/functional-api>) |
| `Advanced/Build with the Functional API/Stream with the Functional API.md` | Stream with the Functional API | Emit custom progress from Functional API entrypoints, or read state snapshots from the values stream.；Advanced, Build with the Functional API, api, functional, streaming | [原文](<https://docs.langchain.com/oss/python/langgraph/functional-api-streaming>) |
| `Advanced/Build with the Functional API/Thinking in the Functional API.md` | Thinking in the Functional API | Learn how to design agents with the LangGraph Functional API using entrypoints, tasks, and ordinary control flow.；Advanced, Build with the Functional API, api, functional, in, thinking | [原文](<https://docs.langchain.com/oss/python/langgraph/thinking-in-functional-api>) |
| `Advanced/LangGraph runtime.md` | LangGraph runtime | **Note:** The [`Pregel`](https://reference.langchain.com/python/langgraph/pregel/main/Pregel) runtime is named after [Google's Pregel algorithm](https://research.google/pubs/pub37252/), which describes an efficient method for large-scale parallel computation using graphs.；Advanced, pregel | [原文](<https://docs.langchain.com/oss/python/langgraph/pregel>) |
| `Build with the Graph API/Build checklist for the Graph API.md` | Build checklist for the Graph API | Decide state, control flow, Send, Command, and node options as you build with the Graph API.；Build with the Graph API, api, graph, use | [原文](<https://docs.langchain.com/oss/python/langgraph/use-graph-api>) |
| `Build with the Graph API/Build sequences, branches, and loops.md` | Build sequences, branches, and loops | Compose sequences, parallel branches, conditional edges, and loops with the LangGraph Graph API.；Build with the Graph API, api, control, flow, graph | [原文](<https://docs.langchain.com/oss/python/langgraph/graph-api-control-flow>) |
| `Build with the Graph API/Configure nodes.md` | Configure nodes | Add runtime configuration, retry policies, timeouts, error handling, defaults, and caching to LangGraph nodes.；Build with the Graph API, api, graph, nodes | [原文](<https://docs.langchain.com/oss/python/langgraph/graph-api-nodes>) |
| `Build with the Graph API/Define and update state.md` | Define and update state | Define graph state schemas, reducers, messages, and private state in the LangGraph Graph API.；Build with the Graph API, api, graph, state | [原文](<https://docs.langchain.com/oss/python/langgraph/graph-api-state>) |
| `Build with the Graph API/Graph API overview.md` | Graph API overview | Learn how LangGraph models agent workflows as graphs of shared state, nodes, and edges.；Build with the Graph API, api, graph | [原文](<https://docs.langchain.com/oss/python/langgraph/graph-api>) |
| `Build with the Graph API/Thinking in the Graph API.md` | Thinking in the Graph API | Learn how to design agents with the LangGraph Graph API using nodes, edges, and shared state.；Build with the Graph API, api, graph, in, thinking | [原文](<https://docs.langchain.com/oss/python/langgraph/thinking-in-graph-api>) |
| `Build with the Graph API/Use Send and Command.md` | Use Send and Command | Build map-reduce workflows with Send and combine state updates with routing using Command in LangGraph.；Build with the Graph API, api, command, graph, send | [原文](<https://docs.langchain.com/oss/python/langgraph/graph-api-send-command>) |
| `Build with the Graph API/Visualize your graph.md` | Visualize your graph | Render LangGraph graphs as Mermaid diagrams or PNG images for debugging and documentation.；Build with the Graph API, api, graph, visualize | [原文](<https://docs.langchain.com/oss/python/langgraph/graph-api-visualize>) |
| `Capabilities/Checkpointers.md` | Checkpointers | LangGraph checkpointers save graph state as checkpoints at each step, enabling persistence, human-in-the-loop, and fault-tolerant execution.；Capabilities, checkpointers | [原文](<https://docs.langchain.com/oss/python/langgraph/checkpointers>) |
| `Capabilities/Event streaming.md` | Event streaming | Stream LangGraph runs with typed projections for messages, state, subgraphs, output, and extensions.；Capabilities, event, streaming | [原文](<https://docs.langchain.com/oss/python/langgraph/event-streaming>) |
| `Capabilities/Fault tolerance.md` | Fault tolerance | Configure per-node timeouts, retries, error handlers, and recovery strategies in LangGraph.；Capabilities, fault, tolerance | [原文](<https://docs.langchain.com/oss/python/langgraph/fault-tolerance>) |
| `Capabilities/Interrupts.md` | Interrupts | [card] [View example trace](https://smith.langchain.com/public/cd7406ad-294e-4d98-b0ae-d9ed7930e117/r)；Capabilities, interrupts | [原文](<https://docs.langchain.com/oss/python/langgraph/interrupts>) |
| `Capabilities/Memory.md` | Memory | [accordion] Example: using Postgres checkpointer；Capabilities, add, memory | [原文](<https://docs.langchain.com/oss/python/langgraph/add-memory>) |
| `Capabilities/Persistence.md` | Persistence | LangGraph's persistence layer gives agents short-term memory through checkpointers and long-term memory through stores.；Capabilities, persistence | [原文](<https://docs.langchain.com/oss/python/langgraph/persistence>) |
| `Capabilities/Stores.md` | Stores | LangGraph stores provide cross-thread long-term memory, complementing per-thread checkpointer persistence.；Capabilities, stores | [原文](<https://docs.langchain.com/oss/python/langgraph/stores>) |
| `Capabilities/Streaming.md` | Streaming | [!TIP]；Capabilities, streaming | [原文](<https://docs.langchain.com/oss/python/langgraph/streaming>) |
| `Capabilities/Subgraphs.md` | Subgraphs | [!TIP]；Capabilities, subgraphs, use | [原文](<https://docs.langchain.com/oss/python/langgraph/use-subgraphs>) |
| `Capabilities/Use time-travel.md` | Use time-travel | Replay past executions and fork to explore alternative paths in LangGraph；Capabilities, time, travel, use | [原文](<https://docs.langchain.com/oss/python/langgraph/use-time-travel>) |
| `Deployment/Agent Chat UI.md` | Agent Chat UI | [!TIP]；Deployment, ui | [原文](<https://docs.langchain.com/oss/python/langgraph/ui>) |
| `Deployment/Application structure.md` | Application structure | [!NOTE]；Deployment, application, structure | [原文](<https://docs.langchain.com/oss/python/langgraph/application-structure>) |
| `Deployment/Backward compatibility.md` | Backward compatibility | Update LangGraph graph code in production without breaking in-flight runs.；Deployment, backward, compatibility | [原文](<https://docs.langchain.com/oss/python/langgraph/backward-compatibility>) |
| `Deployment/Deployment.md` | Deployment | Deploy LangGraph agents to production with LangSmith Cloud or JavaScript frameworks and hosting platforms.；Deployment, deploy | [原文](<https://docs.langchain.com/oss/python/langgraph/deploy>) |
| `Deployment/LangSmith Observability.md` | LangSmith Observability | [!NOTE]；Deployment, observability | [原文](<https://docs.langchain.com/oss/python/langgraph/observability>) |
| `Deployment/LangSmith Studio.md` | LangSmith Studio | [!NOTE]；Deployment, studio | [原文](<https://docs.langchain.com/oss/python/langgraph/studio>) |
| `Deployment/Run a local server.md` | Run a local server | [!TIP]；Deployment, local, server | [原文](<https://docs.langchain.com/oss/python/langgraph/local-server>) |
| `Deployment/Test.md` | Test | Deployment, test | [原文](<https://docs.langchain.com/oss/python/langgraph/test>) |
| `Frontend/Custom stream channels.md` | Custom stream channels | Stream custom server-side data to the frontend and read it with useExtension and useChannel；Frontend, channels, custom, stream | [原文](<https://docs.langchain.com/oss/python/langgraph/frontend/custom-stream-channels>) |
| `Frontend/Graph execution.md` | Graph execution | Visualize multi-step graph pipelines with per-node status and streaming content；Frontend, execution, graph | [原文](<https://docs.langchain.com/oss/python/langgraph/frontend/graph-execution>) |
| `Frontend/Overview.md` | Overview | Render LangGraph agents to the frontend；Frontend, overview | [原文](<https://docs.langchain.com/oss/python/langgraph/frontend/overview>) |
| `Get started/Changelog.md` | Changelog | Log of updates and improvements to our Python packages；Get started, changelog, py | [原文](<https://docs.langchain.com/oss/python/langgraph/changelog-py>) |
| `Get started/Choosing between Graph and Functional APIs.md` | Choosing between Graph and Functional APIs | Prefer the LangGraph Graph API for new workflows. Use the Functional API when wrapping other frameworks for LangSmith Deployment.；Get started, apis, choosing | [原文](<https://docs.langchain.com/oss/python/langgraph/choosing-apis>) |
| `Get started/Quickstart.md` | Quickstart | [!TIP]；Get started, quickstart | [原文](<https://docs.langchain.com/oss/python/langgraph/quickstart>) |
| `LangGraph overview.md` | LangGraph overview | Low-level orchestration framework and runtime for long-running, stateful agents；overview | [原文](<https://docs.langchain.com/oss/python/langgraph/overview>) |
| `LangSmith Studio.md` | LangSmith Studio | [!NOTE]；studio | [原文](<https://docs.langchain.com/oss/python/studio>) |
| `Learn/Additional resources/Case studies.md` | Case studies | Additional resources, Learn, case, studies | [原文](<https://docs.langchain.com/oss/python/langgraph/case-studies>) |
| `Learn/Tutorials/Build a custom RAG agent with LangGraph.md` | Build a custom RAG agent with LangGraph | Build a custom retrieval agent with LangGraph that decides when to search a vector store or respond directly.；Learn, Tutorials, agentic, rag | [原文](<https://docs.langchain.com/oss/python/langgraph/agentic-rag>) |
| `Learn/Tutorials/Build a custom SQL agent.md` | Build a custom SQL agent | [!WARNING]；Learn, Tutorials, agent, sql | [原文](<https://docs.langchain.com/oss/python/langgraph/sql-agent>) |
| `Patterns/Workflows and agents.md` | Workflows and agents | [!TIP]；Patterns, agents, workflows | [原文](<https://docs.langchain.com/oss/python/langgraph/workflows-agents>) |
| `Reference/Errors/GRAPH_RECURSION_LIMIT.md` | GRAPH_RECURSION_LIMIT | Errors, GRAPH_RECURSION_LIMIT, Reference | [原文](<https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT>) |
| `Reference/Errors/INVALID_CHAT_HISTORY.md` | INVALID_CHAT_HISTORY | Errors, INVALID_CHAT_HISTORY, Reference | [原文](<https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CHAT_HISTORY>) |
| `Reference/Errors/INVALID_CONCURRENT_GRAPH_UPDATE.md` | INVALID_CONCURRENT_GRAPH_UPDATE | Errors, INVALID_CONCURRENT_GRAPH_UPDATE, Reference | [原文](<https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE>) |
| `Reference/Errors/INVALID_GRAPH_NODE_RETURN_VALUE.md` | INVALID_GRAPH_NODE_RETURN_VALUE | Errors, INVALID_GRAPH_NODE_RETURN_VALUE, Reference | [原文](<https://docs.langchain.com/oss/python/langgraph/errors/INVALID_GRAPH_NODE_RETURN_VALUE>) |
| `Reference/Errors/MISSING_CHECKPOINTER.md` | MISSING_CHECKPOINTER | Errors, MISSING_CHECKPOINTER, Reference | [原文](<https://docs.langchain.com/oss/python/langgraph/errors/MISSING_CHECKPOINTER>) |
| `Reference/Errors/MULTIPLE_SUBGRAPHS.md` | MULTIPLE_SUBGRAPHS | Errors, MULTIPLE_SUBGRAPHS, Reference | [原文](<https://docs.langchain.com/oss/python/langgraph/errors/MULTIPLE_SUBGRAPHS>) |
