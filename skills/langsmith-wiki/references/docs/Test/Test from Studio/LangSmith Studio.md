# LangSmith Studio

> [!NOTE]
>
> **Prerequisites**
>
> * [LangSmith](../../Monitor/Overview/LangSmith%20Observability.md)
> * [Agent Server](../../Deploy/Agent%20Server/Capabilities/Agent%20Server.md)
> * [LangGraph CLI](../../Deploy/Get%20started/Reference/LangGraph%20CLI.md)

Studio is a specialized agent IDE that enables visualization, interaction, and debugging of agentic systems that implement the Agent Server API protocol. Studio also integrates with [tracing](../../Monitor/Trace/Observability%20concepts.md), [evaluation](../Get%20started/LangSmith%20Evaluation.md), and [prompt engineering](../../Deploy/Prompt%20%26%20Context%20Hub/Prompt%20%26%20Context%20Hub.md#prompts).

## Features

Key features of Studio:

* Visualize your graph architecture
* [Run and interact with your agent](How%20to%20use%20Studio.md#run-application)
* [Manage assistants](How%20to%20use%20Studio.md#manage-assistants)
* [Manage threads](How%20to%20use%20Studio.md#manage-threads)
* [Iterate on prompts](Observability%20in%20Studio.md)
* [Run experiments over a dataset](Observability%20in%20Studio.md#run-experiments-over-a-dataset)
* Manage [long term memory](https://docs.langchain.com/oss/python/concepts/memory.md)
* Debug agent state via [time travel](https://docs.langchain.com/oss/python/langgraph/use-time-travel.md)
* 1 Click deploy to LangSmith Cloud.
* [Build a no-code agent](../../No-code%20agents/Studio/Build%20an%20agent%20with%20LangSmith%20Studio.md) by describing it

```mermaid actions={false}
flowchart
    subgraph LangSmith Agent Server
        A[LangGraph CLI] -->|creates| B(Agent Server deployment)
        B <--> D[Studio]
        B <--> E[SDKs]
        B <--> F[RemoteGraph]
    end

    classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710

    class A,B,D,E,F process
```

Studio works for graphs that are deployed on [LangSmith](../../Deploy/Get%20started/Deploy%20your%20app%20to%20cloud.md) or for graphs that are running locally via the [Agent Server](../../Deploy/Get%20started/Develop%20%26%20test/Local%20development%20%26%20testing.md).

Studio supports two modes:

### Graph mode

Graph mode exposes the full feature-set and is useful when you would like as many details about the execution of your agent, including the nodes traversed, intermediate states, and LangSmith integrations (such as adding to datasets and playground).

### Chat mode

Chat mode is a simpler UI for iterating on and testing chat-specific agents. It is useful for business users and those who want to test overall agent behavior. Chat mode is only supported for graph's whose state includes or extends [`MessagesState`](https://docs.langchain.com/oss/python/langgraph/graph-api-state#messagesstate).

## Build a no-code agent

Studio also builds no-code agents. Building agents in Studio is available on [LangSmith Cloud](../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and not on [self-hosted](../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) LangSmith. Describe the agent you want, and [LangSmith Chat](../Datasets%20%26%20Experiments/Analyze%20experiment%20results/LangSmith%20Chat.md) drafts its name, description, and instructions, then suggests its connections, channels, and schedules. Review and save the configuration, then chat with the agent and watch its traces in the same view. For more information, see [Build an agent with LangSmith Studio](../../No-code%20agents/Studio/Build%20an%20agent%20with%20LangSmith%20Studio.md).

## Deploy from Studio

Go from [testing graphs locally](../../Deploy/Get%20started/Develop%20%26%20test/Local%20development%20%26%20testing.md) in Studio to deploying them on Langsmith Cloud in 1 Click, directly from Studio. You can use this to create a brand new deployment for quick prototyping or to redeploy an existing deployment.

## Learn more

* See this guide on how to [get started](Get%20started%20with%20Studio.md) with Studio.

## Video guide

[YouTube video player](https://www.youtube.com/embed/Mi1gSlHwZLM?si=oWCeHQ640zPHoLwn)
