# Deployment

> Deploy LangChain agents to production with LangSmith Cloud or JavaScript frameworks and hosting platforms.

When you are ready to deploy your LangChain agent to production, choose a hosting model that fits your stack. **[LangSmith Cloud](https://docs.langchain.com/langsmith/deploy-to-cloud.md)** provides fully managed infrastructure for stateful, long-running agents with persistent state and background execution.

> [!TIP]
>
> LangSmith offers multiple deployment options beyond Cloud, including [hybrid](https://docs.langchain.com/langsmith/hybrid.md), [standalone servers](https://docs.langchain.com/langsmith/deploy-standalone-server.md), and [self-hosted with control plane](https://docs.langchain.com/langsmith/deploy-with-control-plane.md). For more information, see the [LangSmith Agent Server overview](https://docs.langchain.com/langsmith/deployment.md).

## LangSmith Cloud

This section walks through deploying your agent to LangSmith Cloud from a GitHub repository. LangSmith handles infrastructure, scaling, and operational concerns.

### Prerequisites

Before you begin, ensure you have the following:

* A [GitHub account](https://github.com/)
* A [LangSmith account](https://smith.langchain.com?utm_source=docs\&utm_medium=cta\&utm_campaign=langsmith-signup\&utm_content=oss-langchain-deploy) (free to sign up)

### Deploy your agent

#### 1. Create a repository on GitHub

Your application's code must reside in a GitHub repository to be deployed on LangSmith. Both public and private repositories are supported. For this quickstart, first make sure your app is LangGraph-compatible by following the [local server setup guide](../Agent%20development/LangSmith%20Studio.md). Then, push your code to the repository.

#### 2. Deploy to LangSmith

**1. Navigate to Agent Servers**

Log in to [LangSmith](https://smith.langchain.com?utm_source=docs\&utm_medium=cta\&utm_campaign=langsmith-signup\&utm_content=snippets-oss-deploy-py). In the left sidebar, select **Agent Servers**.

**2. Create an Agent Server**

Click the **+ Agent Server** button. A pane will open where you can fill in the required fields.

**3. Link repository**

If you are a first time user or adding a private repository that has not been previously connected, click the **Add new account** button and follow the instructions to connect your GitHub account.

**4. Deploy repository**

Select your application's repository. Click **Submit** to deploy. This may take about 15 minutes to complete. You can check the status in the **Agent Server details** view.

#### 3. Test your application in Studio

Once your application is deployed:

1. Select the Agent Server you just created to view more details.
2. Click the **Studio** button in the top right corner. Studio will open to display your graph.

#### 4. Get the API URL for your Agent Server

In the **Agent Server details** view in LangSmith, find the **URL** row. Click **Copy Agent Server URL** to copy the address to your clipboard.

#### 5. Test the API

You can now test the API:

> [tab] Python
>
> 1. Install LangGraph Python:
>
> ```bash pip
> pip install -U langgraph-sdk
> ```
>
> ```bash uv
> uv add langgraph-sdk
> ```
>
> 2. Send a message to the agent:
>
> ```python
> from langgraph_sdk import get_sync_client # or get_client for async
>
> client = get_sync_client(url="your-deployment-url", api_key="<API_KEY>")
>
> for chunk in client.runs.stream(
>     None,    # Threadless run
>     "agent", # Name of agent. Defined in langgraph.json.
>     input={
>         "messages": [{
>             "role": "human",
>             "content": "What is LangGraph?",
>         }],
>     },
>     stream_mode="updates",
> ):
>     print(f"Receiving new event of type: {chunk.event}...")
>     print(chunk.data)
>     print("\n\n")
> ```

> [tab] Rest API
>
> ```bash
> curl -s --request POST \
>     --url <DEPLOYMENT_URL>/runs/stream \
>     --header 'Content-Type: application/json' \
>     --header "X-Api-Key: <LANGSMITH API KEY> \
>     --data "{
>         \"assistant_id\": \"agent\", `# Name of agent. Defined in langgraph.json.`
>         \"input\": {
>             \"messages\": [
>                 {
>                     \"role\": \"human\",
>                     \"content\": \"What is LangGraph?\"
>                 }
>             ]
>         },
>         \"stream_mode\": \"updates\"
>     }"
> ```

> [!TIP]
>
> LangSmith offers additional hosting options, including self-hosted and hybrid. For more information, please see the [Platform setup overview](https://docs.langchain.com/langsmith/platform-setup.md).

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/deploy.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
