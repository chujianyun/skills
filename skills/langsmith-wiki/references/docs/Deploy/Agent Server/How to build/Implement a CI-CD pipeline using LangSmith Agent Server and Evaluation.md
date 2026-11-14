# Implement a CI/CD pipeline using LangSmith Agent Server and Evaluation

This guide demonstrates how to implement a comprehensive CI/CD pipeline for AI agent applications deployed in LangSmith Agent Server. In this example, you'll use the [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview.md) open source framework for orchestrating and building the agent, [LangSmith](../../../Monitor/Overview/LangSmith%20Observability.md) for observability and evaluations. This pipeline is based on the [cicd-pipeline-example repository](https://github.com/langchain-ai/cicd-pipeline-example).

## Overview

The CI/CD pipeline provides:

* &#x20;**Automated testing**: Unit, integration, and end-to-end tests.
* &#x20;**Offline evaluations**: Performance assessment using [AgentEvals](https://docs.langchain.com/oss/python/langchain/test/evals.md), [OpenEvals](../../../Test/Evaluators/Frameworks%20%26%20integrations/Run%20evals%20with%20openevals%20package.md#setup) and [LangSmith](../../../Monitor/Overview/LangSmith%20Observability.md).
* &#x20;**Preview and production deployments**: Automated staging and quality-gated production releases using the Control Plane API.
* &#x20;**Monitoring**: Continuous evaluation and alerting.

## Pipeline architecture

The CI/CD pipeline consists of several key components that work together to ensure code quality and reliable deployments:

```mermaid
graph TD
    A1[Code or Graph Change] --> B1[Trigger CI Pipeline]
    A2[Prompt Commit in PromptHub] --> B1
    A3[Online Evaluation Alert] --> B1
    A4[PR Opened] --> B1

    subgraph "Testing"
        B1 --> C1[Run Unit Tests]
        B1 --> C2[Run Integration Tests]
        B1 --> C3[Run End to End Tests]
        B1 --> C4[Run Offline Evaluations]

        C4 --> D1[Evaluate with OpenEvals or AgentEvals]
        C4 --> D2[Assertions: Hard and Soft]

        C1 --> E1[Run LangGraph Dev Server Test]
        C2 --> E1
        C3 --> E1
        D1 --> E1
        D2 --> E1
    end

    E1 --> F1[Push to Staging Deployment - Deploy to LangSmith as Development Type]

    F1 --> G1[Run Online Evaluations on Live Data]
    G1 --> H1[Attach Scores to Traces]

    H1 --> I1[If Quality Below Threshold]
    I1 --> J1[Send to Annotation Queue]
    I1 --> J2[Trigger Alert via Webhook]
    I1 --> J3[Push Trace to Golden Dataset]

    F1 --> K1[Promote to Production if All Pass - Deploy to LangSmith Production]

    J2 --> L1[Slack or PagerDuty Notification]

    subgraph Manual Review
        J1 --> M1[Human Labeling]
        M1 --> J3
    end

    classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
    classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
    classDef decision fill:#FDF3FF,stroke:#7E65AE,stroke-width:2px,color:#504B5F
    classDef output fill:#EBD0F0,stroke:#885270,stroke-width:2px,color:#441E33
    classDef alert fill:#F8E8E6,stroke:#B27D75,stroke-width:2px,color:#634643
    classDef neutral fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#2F4B68

    class A1,A2,A3,A4 trigger
    class B1,C1,C2,C3,C4,D1,D2,E1 process
    class H1,I1 decision
    class F1,G1,K1 output
    class J2,L1 alert
    class J1,J3,M1 neutral
```

### Trigger sources

There are multiple ways you can trigger this pipeline, either during development or if your application is already live. The pipeline can be triggered by:

* &#x20;**Code changes**: Pushes to main/development branches where you can modify the LangGraph architecture, try different models, update agent logic, or make any code improvements.
* &#x20;**PromptHub updates**: Changes to prompt templates stored in LangSmith PromptHub—whenever there's a new prompt commit, the system triggers a webhook to run the pipeline.
* &#x20;**Online evaluation alerts**: Performance degradation notifications from live Agent Servers
* &#x20;**LangSmith traces webhooks**: Automated triggers based on trace analysis and performance metrics.
* &#x20;**Manual trigger**: Manual initiation of the pipeline for testing or emergency deployments.

### Testing layers

Compared to traditional software, testing AI agent applications also requires assessing response quality, so it is important to test each part of the workflow. The pipeline implements multiple testing layers:

1. &#x20;**Unit tests**: Individual node and utility function testing.
2. &#x20;**Integration tests**: Component interaction testing.
3. &#x20;**End-to-end tests**: Full graph execution testing.
4. &#x20;**Offline evaluations**: Performance assessment with real-world scenarios including end-to-end evaluations, single-step evaluations, agent trajectory analysis, and multi-turn simulations.
5. &#x20;**LangGraph dev server tests**: Use the [langgraph-cli](../../Get%20started/Reference/LangGraph%20CLI.md) tool for spinning up (inside the GitHub Action) a local server to run the LangGraph agent. This polls the `/ok` server API endpoint until it is available and for 30 seconds, after that it throws an error.

## GitHub actions workflow

The CI/CD pipeline uses GitHub Actions with the [Control Plane API](../../Get%20started/Reference/Control%20Plane%20API/Control%20plane%20API%20reference%20for%20Agent%20Server%20hosting.md) and [LangSmith API](../../../Monitor/Reference/LangSmith%20REST%20API/LangSmith%20API%20reference.md) to automate deployment. A helper script manages API interactions and deployments: [https://github.com/langchain-ai/cicd-pipeline-example/blob/main/.github/scripts/langgraph\_api.py](https://github.com/langchain-ai/cicd-pipeline-example/blob/main/.github/scripts/langgraph_api.py).

The workflow includes:

* **New agent deployment**: When a new PR is opened and tests pass, a new preview Agent Server is created using the [Control Plane API](../../Get%20started/Reference/Control%20Plane%20API/Control%20plane%20API%20reference%20for%20Agent%20Server%20hosting.md). This allows you to test the agent in a staging environment before promoting to production.

* **Agent deployment revision**: A revision happens when an existing Agent Server with the same ID is found, or when the PR is merged into main. In the case of merging to main, the preview Agent Server is deleted and a production Agent Server is created. This ensures that any updates to the agent are properly deployed and integrated into the production infrastructure.

  ![Agent Deployment Revision Workflow](../../../../assets/images/dae5b9400e07-cicd-new-lgp-revision.png)

* **Testing and evaluation workflow**: In addition to the more traditional testing phases (unit tests, integration tests, end-to-end tests, etc.), the pipeline includes [offline evaluations](../../../Test/Get%20started/Evaluation%20concepts.md#offline-evaluations) and [Agent dev server testing](../../Get%20started/Develop%20%26%20test/Local%20development%20%26%20testing.md) because you want to test the quality of your agent. These evaluations provide comprehensive assessment of the agent's performance using real-world scenarios and data.

  ![Test with Results Workflow](../../../../assets/images/5dbb3a03c304-cicd-test-with-results.png)

  > [accordion] Final Response Evaluation
  >
  > Evaluates the final output of your agent against expected results. This is the most common type of evaluation that checks if the agent's final response meets quality standards and answers the user's question correctly.

  > [accordion] Single Step Evaluation
  >
  > Tests individual steps or nodes within your LangGraph workflow. This allows you to validate specific components of your agent's logic in isolation, ensuring each step functions correctly before testing the full pipeline.

  > [accordion] Agent Trajectory Evaluation
  >
  > Analyzes the complete path your agent takes through the graph, including all intermediate steps and decision points. This helps identify bottlenecks, unnecessary steps, or suboptimal routing in your agent's workflow. It also evaluates whether your agent invoked the right tools in the right order or at the right time.

  > [accordion] Multi-Turn Evaluation
  >
  > Tests conversational flows where the agent maintains context across multiple interactions. This is crucial for agents that handle follow-up questions, clarifications, or extended dialogues with users.

  See the [LangGraph testing documentation](https://docs.langchain.com/oss/python/langgraph/test.md) for specific testing approaches and the [evaluation approaches guide](../../../Test/Get%20started/Application-specific%20evaluation%20approaches.md) for a comprehensive overview of offline evaluations.

### Prerequisites

Before setting up the CI/CD pipeline, ensure you have:

* &#x20;An AI agent application (in this case built using [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview.md))
* &#x20;A [LangSmith account](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-cicd-pipeline-example)
* &#x20;A [LangSmith API key](../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md) needed to deploy agents and retrieve experiment results
* &#x20;Project-specific environment variables configured in your repository secrets (e.g., LLM model API keys, vector store credentials, database connections)

> [!NOTE]
>
> While this example uses GitHub, the CI/CD pipeline works with other Git hosting platforms including GitLab, Bitbucket, and others.

## Deployment options

LangSmith supports multiple deployment methods, depending on how your [LangSmith instance is hosted](../../../LangSmith%20setup/Overview/Hosting/Set%20up%20LangSmith.md):

* &#x20;**Cloud LangSmith**: Direct GitHub integration.
* &#x20;**Self-Hosted/Hybrid**: Container registry-based deployments.

The deployment flow starts by modifying your agent implementation. At minimum, you must have a [`langgraph.json`](../Develop%20your%20application/Application%20structure.md) and dependency file in your project (`requirements.txt` or `pyproject.toml`). Use the `langgraph dev` CLI tool to check for errors—fix any errors; otherwise, the deployment will succeed when deployed to LangSmith Agent Server.

```mermaid actions={false}
graph TD
    A[Agent Implementation] --> B[langgraph.json + dependencies]
    B --> C[Test Locally with langgraph dev]
    C --> D{Errors?}
    D -->|Yes| E[Fix Issues]
    E --> C
    D -->|No| F[Choose LangSmith Instance]

    F --> G[Cloud LangSmith]
    F --> H[Self-Hosted/Hybrid LangSmith]

    subgraph "Cloud LangSmith"
        G --> I[Method 1: Connect GitHub Repo in UI]
        G --> J[Method 2: Control Plane API with GitHub Repo]
        I --> K[Deploy via LangSmith UI]
        J --> L[Deploy via Control Plane API]
    end

    subgraph "Self-Hosted/Hybrid LangSmith"
        H --> S[Build Docker Image langgraph build]
        S --> T[Push to Container Registry]
        T --> U{Deploy via?}
        U -->|UI| V[Specify Image URI in UI]
        U -->|API| W[Use Control Plane API]
        V --> X[Deploy via LangSmith UI]
        W --> Y[Deploy via Control Plane API]
    end

    K --> AA[Agent Ready for Use]
    L --> AA
    X --> AA
    Y --> AA

    AA --> BB{Connect via?}
    BB -->|LangGraph SDK| CC[Use LangGraph SDK]
    BB -->|RemoteGraph| DD[Use RemoteGraph]
    BB -->|REST API| EE[Use REST API]
    BB -->|LangGraph Studio UI| FF[Use LangGraph Studio UI]

    classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
    classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
    classDef decision fill:#FDF3FF,stroke:#7E65AE,stroke-width:2px,color:#504B5F
    classDef output fill:#EBD0F0,stroke:#885270,stroke-width:2px,color:#441E33

    class A trigger
    class B,C process
    class D,U,BB decision
    class E process
    class F decision
    class G,H process
    class I,J,S,T process
    class K,L,V,W process
    class X,Y,AA output
    class CC,DD,EE,FF output
```

### Prerequisites for manual deployment

Before deploying your agent, ensure you have:

1. &#x20;**LangGraph graph**: Your agent implementation (e.g., `./agents/simple_text2sql.py:agent`).
2. &#x20;**Dependencies**: Either `requirements.txt` or `pyproject.toml` with all required packages.
3. &#x20;**Configuration**: `langgraph.json` file specifying:
   * Path to your agent graph
   * Dependencies location
   * Environment variables
   * Python version

Example `langgraph.json`:

```json
{
    "graphs": {
        "simple_text2sql": "./agents/simple_text2sql.py:agent"
    },
    "env": ".env",
    "python_version": "3.11",
    "dependencies": ["."],
    "image_distro": "wolfi"
}
```

### Local development and testing

![Studio CLI Interface](../../../../assets/images/88604670f339-cicd-studio-cli.png)

First, test your agent locally using [Studio](../../../Test/Test%20from%20Studio/LangSmith%20Studio.md):

```bash
# Start local development server with Studio
langgraph dev
```

This will:

* Spin up a local server with Studio.
* Allow you to visualize and interact with your graph.
* Validate that your agent works correctly before deployment.

> [!NOTE]
>
> If your agent runs locally without any errors, it means that deployment to LangSmith will likely succeed. This local testing helps catch configuration issues, dependency problems, and agent logic errors before attempting deployment.

See the [LangGraph CLI documentation](../../Get%20started/Reference/LangGraph%20CLI.md#dev) for more details.

### Method 1: LangSmith Agent Server UI

Deploy your agent using the LangSmith Agent Server UI:

1. Go to your [LangSmith dashboard](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-cicd-pipeline-example).
2. Navigate to the **Agent Servers** section.
3. Click the **+ Agent Server** button in the top right.
4. Select your GitHub repository containing your LangGraph agent from the dropdown menu.

**Supported deployments:**

* &#x20;**Cloud LangSmith**: Direct GitHub integration with dropdown menu
* &#x20;**Self-Hosted/Hybrid LangSmith**: Specify your image URI in the Image Path field (e.g., `docker.io/username/my-agent:latest`)

> [!NOTE]
>
> **Benefits:**
>
> * Simple UI-based deployment
> * Direct integration with your GitHub repository (cloud)
> * No manual Docker image management required (cloud)

### Method 2: Control plane API

Deploy using the Control Plane API with different approaches for each deployment type:

**For Cloud LangSmith:**

* Use the Control Plane API to create deployments by pointing to your GitHub repository
* No Docker image building required for cloud deployments

**For Self-Hosted/Hybrid LangSmith:**

```bash
# Build Docker image
langgraph build -t my-agent:latest

# Push to your container registry
docker push my-agent:latest
```

You can push to any container registry (Docker Hub, AWS ECR, Azure ACR, Google GCR, etc.) that your deployment environment has access to.

**Supported deployments:**

* &#x20;**Cloud LangSmith**: Use the Control Plane API to create deployments from your GitHub repository
* &#x20;**Self-Hosted/Hybrid LangSmith**: Use the Control Plane API to create deployments from your container registry

See the [LangGraph CLI build documentation](../../Get%20started/Reference/LangGraph%20CLI.md#build) for more details.

### Connect to your deployed Agent

* &#x20;**[LangGraph SDK](../../Get%20started/Reference/Related/langgraph_sdk.md)**: Use the LangGraph SDK for programmatic integration.
* &#x20;**[RemoteGraph](../Capabilities/How%20to%20interact%20with%20a%20deployment%20using%20RemoteGraph.md)**: Connect using RemoteGraph for remote graph connections (to use your graph in other graphs).
* &#x20;**[REST API](../../Get%20started/Reference/Agent%20Server%20API/Agent%20Server%20API%20reference.md)**: Use HTTP-based interactions with your deployed agent.
* &#x20;**[Studio](../../../Test/Test%20from%20Studio/LangSmith%20Studio.md)**: Access the visual interface for testing and debugging.

### Environment configuration

#### Database & cache configuration

By default, Agent Server hosting provisions PostgreSQL and Redis instances for you. To use external services, set the following environment variables in your new Agent Server or revision:

```bash
# Set environment variables for external services
export POSTGRES_URI_CUSTOM="postgresql://user:pass@host:5432/db"
export REDIS_URI_CUSTOM="redis://host:6379/0"
```

See the [environment variables documentation](../../Deploy%20to%20Self-hosted/Reference/Self-hosted%20Agent%20Server%20environment%20variables.md) for more details.

## Troubleshooting

### Wrong API endpoints

If you're experiencing connection issues, verify you're using the correct endpoint format for your LangSmith instance. There are two different APIs with different endpoints:

#### LangSmith API (Traces, ingestion, etc.)

For LangSmith API operations (traces, evaluations, datasets):

<table>
  <thead>
    <tr>
      <th>Region</th>

      <th>
        URL
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>GCP US</td>

      <td>
        `https://api.smith.langchain.com`
      </td>
    </tr>

    <tr>
      <td>GCP EU</td>

      <td>
        `https://eu.api.smith.langchain.com`
      </td>
    </tr>

    <tr>
      <td>GCP APAC</td>

      <td>
        `https://apac.api.smith.langchain.com`
      </td>
    </tr>

    <tr>
      <td>AWS US</td>

      <td>
        `https://aws.api.smith.langchain.com`
      </td>
    </tr>

    <tr><td>Azure US</td>
    <td>`https://azure.api.smith.langchain.com`</td></tr>
  </tbody>
</table>

For self-hosted LangSmith instances, use `http(s)://<langsmith-url>/api` where `<langsmith-url>` is your self-hosted instance URL.

> [!NOTE]
>
> If you set the endpoint in the `LANGSMITH_ENDPOINT` environment variable, use the API URL, such as `https://api.smith.langchain.com` or `http(s)://<langsmith-url>/api` if self-hosted.

#### Control Plane API (Agent Server deployments)

For control plane operations (Agent Server deployments and revisions):

<table>
  <thead>
    <tr>
      <th>Region</th>

      <th>
        URL
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>GCP US</td>

      <td>
        `https://api.host.langchain.com`
      </td>
    </tr>

    <tr>
      <td>GCP EU</td>

      <td>
        `https://eu.api.host.langchain.com`
      </td>
    </tr>

    <tr>
      <td>GCP APAC</td>

      <td>
        `https://apac.api.host.langchain.com`
      </td>
    </tr>

    <tr>
      <td>AWS US</td>

      <td>
        `https://aws.api.host.langchain.com`
      </td>
    </tr>

    <tr><td>Azure US</td>
    <td>`https://azure.api.host.langchain.com`</td></tr>
  </tbody>
</table>

For self-hosted LangSmith instances, use `http(s)://<langsmith-url>/api-host` where `<langsmith-url>` is your self-hosted instance URL.
