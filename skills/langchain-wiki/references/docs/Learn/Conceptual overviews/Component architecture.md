# Component architecture

LangChain's power comes from how its components work together to create sophisticated AI applications. This page provides diagrams showcasing the relationships between different components.

## Core component ecosystem

The diagram below shows how LangChain's major components connect to form complete AI applications:

```mermaid
graph TD
    %% Input processing
    subgraph "📥 Input processing"
        A[Text input] --> B[Document loaders]
        B --> C[Text splitters]
        C --> D[Documents]
    end

    %% Embedding & storage
    subgraph "🔢 Embedding & storage"
        D --> E[Embedding models]
        E --> F[Vectors]
        F --> G[(Vector stores)]
    end

    %% Retrieval
    subgraph "🔍 Retrieval"
        H[User Query] --> I[Embedding models]
        I --> J[Query vector]
        J --> K[Retrievers]
        K --> G
        G --> L[Relevant context]
    end

    %% Generation
    subgraph "🤖 Generation"
        M[Chat models] --> N[Tools]
        N --> O[Tool results]
        O --> M
        L --> M
        M --> P[AI response]
    end

    %% Orchestration
    subgraph "🎯 Orchestration"
        Q[Agents] --> M
        Q --> N
        Q --> K
        Q --> R[Memory]
    end

    classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
    classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
    classDef output fill:#EBD0F0,stroke:#885270,stroke-width:2px,color:#441E33
    classDef neutral fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#2F4B68

    class A,H trigger
    class B,C,E,I,K,M,N,Q process
    class D,F,J,L,O,P,R neutral
    class G output
```

### How components connect

Each component layer builds on the previous ones:

1. **Input processing** – Transform raw data into structured documents
2. **Embedding & storage** – Convert text into searchable vector representations
3. **Retrieval** – Find relevant information based on user queries
4. **Generation** – Use AI models to create responses, optionally with tools
5. **Orchestration** – Coordinate everything through agents and memory systems

## Component categories

LangChain organizes components into these main categories:

| Category | Purpose | Key Components | Use Cases |
| - | - | - | - |
| **[Models](../../Core%20components/Models.md)** | AI reasoning and generation | Chat models, LLMs, Embedding models | Text generation, reasoning, semantic understanding |
| **[Tools](../../Core%20components/Tools.md)** | External capabilities | APIs, databases, etc. | Web search, data access, computations |
| **[Agents](../../Core%20components/Agents.md)** | Orchestration and reasoning | ReAct agents, tool calling agents | Nondeterministic workflows, decision making |
| **[Memory](../../Core%20components/Short-term%20memory.md)** | Context preservation | Message history, custom state | Conversations, stateful interactions |
| **[Retrievers](https://docs.langchain.com/oss/python/integrations/retrievers.md)** | Information access | Vector retrievers, web retrievers | RAG, knowledge base search |
| **[Document processing](https://docs.langchain.com/oss/python/integrations/document_loaders.md)** | Data ingestion | Loaders, splitters, transformers | PDF processing, web scraping |
| **[Vector Stores](https://docs.langchain.com/oss/python/integrations/vectorstores.md)** | Semantic search | Chroma, Pinecone, FAISS | Similarity search, embeddings storage |

## Common patterns

### RAG (Retrieval-Augmented generation)

```mermaid
graph LR
    A[User question] --> B[Retriever]
    B --> C[Relevant docs]
    C --> D[Chat model]
    A --> D
    D --> E[Informed response]

    classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
    classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
    classDef neutral fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#2F4B68

    class A trigger
    class B,D process
    class C,E neutral
```

### Agent with tools

```mermaid
graph LR
    A[User request] --> B[Agent]
    B --> C{Need tool?}
    C -->|Yes| D[Call tool]
    D --> E[Tool result]
    E --> B
    C -->|No| F[Final answer]

    classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
    classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
    classDef decision fill:#FDF3FF,stroke:#7E65AE,stroke-width:2px,color:#504B5F
    classDef neutral fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#2F4B68

    class A trigger
    class B,D process
    class C decision
    class E,F neutral
```

### Multi-agent system

```mermaid
graph LR
    A[Complex Task] --> B[Supervisor agent]
    B --> C[Specialist agent 1]
    B --> D[Specialist agent 2]
    C --> E[Results]
    D --> E
    E --> B
    B --> F[Coordinated response]

    classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
    classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
    classDef neutral fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#2F4B68

    class A trigger
    class B,C,D process
    class E,F neutral
```

## Learn more

* [Creating agents](../../Core%20components/Agents.md)
* [Working with tools](../../Core%20components/Tools.md)
* [Browse integrations](https://docs.langchain.com/oss/python/integrations/providers/overview.md)

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/component-architecture.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
