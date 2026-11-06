# LangSmith Studio

> [!NOTE]
>
> **Prerequisites**
>
> * [LangSmith](https://docs.langchain.com/langsmith/observability.md)
> * [Agent Server](https://docs.langchain.com/langsmith/agent-server.md)
> * [LangGraph CLI](https://docs.langchain.com/langsmith/cli.md)

Studio is a specialized agent IDE that enables visualization, interaction, and debugging of agentic systems that implement the Agent Server API protocol. Studio also integrates with [tracing](https://docs.langchain.com/langsmith/observability-concepts.md), [evaluation](https://docs.langchain.com/langsmith/evaluation.md), and [prompt engineering](https://docs.langchain.com/langsmith/prompt-context-hub.md#prompts).

## Features

Key features of Studio:

* Visualize your graph architecture
* [Run and interact with your agent](https://docs.langchain.com/langsmith/use-studio.md#run-application)
* [Manage assistants](https://docs.langchain.com/langsmith/use-studio.md#manage-assistants)
* [Manage threads](https://docs.langchain.com/langsmith/use-studio.md#manage-threads)
* [Iterate on prompts](https://docs.langchain.com/langsmith/observability-studio.md)
* [Run experiments over a dataset](https://docs.langchain.com/langsmith/observability-studio.md#run-experiments-over-a-dataset)
* Manage [long term memory](https://docs.langchain.com/oss/python/concepts/memory.md)
* Debug agent state via [time travel](Capabilities/Use%20time-travel.md)
* 1 Click deploy to LangSmith Cloud.

```mermaid actions={false}
flowchart
    subgraph LangSmith Deployment
        A[LangGraph CLI] -->|creates| B(Agent Server deployment)
        B <--> D[Studio]
        B <--> E[SDKs]
        B <--> F[RemoteGraph]
    end

    classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710

    class A,B,D,E,F process
```

Studio works for graphs that are deployed on [LangSmith](https://docs.langchain.com/langsmith/deployment-quickstart.md) or for graphs that are running locally via the [Agent Server](https://docs.langchain.com/langsmith/local-dev-testing.md).

Studio supports two modes:

### Graph mode

Graph mode exposes the full feature-set and is useful when you would like as many details about the execution of your agent, including the nodes traversed, intermediate states, and LangSmith integrations (such as adding to datasets and playground).

### Chat mode

Chat mode is a simpler UI for iterating on and testing chat-specific agents. It is useful for business users and those who want to test overall agent behavior. Chat mode is only supported for graph's whose state includes or extends [`MessagesState`](Build%20with%20the%20Graph%20API/Define%20and%20update%20state.md#messagesstate).

## Deploy from Studio

Go from [testing graphs locally](https://docs.langchain.com/langsmith/local-dev-testing.md) in Studio to deploying them on Langsmith Cloud in 1 Click, directly from Studio. You can use this to create a brand new deployment for quick prototyping or to redeploy an existing deployment.

## Learn more

* See this guide on how to [get started](https://docs.langchain.com/langsmith/quick-start-studio.md) with Studio.

## Video guide

[YouTube video player](https://www.youtube.com/embed/Mi1gSlHwZLM?si=oWCeHQ640zPHoLwn)
