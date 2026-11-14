# Agent Server API reference

> Browse the Agent Server API reference, available within each Agent Server at the /docs endpoint.

The Agent Server API reference is available within each [deployment](../../LangSmith%20Agent%20Server.md) at the `/docs` endpoint (e.g. `http://localhost:8124/docs`).

Browse the full API reference in the **Agent Server API** section in the sidebar, or see the endpoint groups below:

* [Assistants](https://docs.langchain.com/langsmith/agent-server-api/assistants) - Configured instances of a graph
* [Threads](https://docs.langchain.com/langsmith/agent-server-api/threads) - Accumulated outputs of a group of runs
* [Thread Runs](https://docs.langchain.com/langsmith/agent-server-api/thread-runs) - Invocations of a graph/assistant on a thread
* [Stateless Runs](https://docs.langchain.com/langsmith/agent-server-api/stateless-runs) - Invocations with no state persistence
* [Crons](https://docs.langchain.com/langsmith/agent-server-api/crons) - Periodic runs on a schedule
* [Store](https://docs.langchain.com/langsmith/agent-server-api/store) - Persistent key-value store for long-term memory
* [A2A](https://docs.langchain.com/langsmith/agent-server-api/a2a) - Agent-to-Agent Protocol endpoints
* [MCP](https://docs.langchain.com/langsmith/agent-server-api/mcp) - Model Context Protocol endpoints
* [System](https://docs.langchain.com/langsmith/agent-server-api/system) - Health checks and server info

## Authentication

For deployments to LangSmith, authentication is required. Pass the `X-Api-Key` header with each request to the Agent Server. The value of the header should be set to a valid LangSmith API key for the organization where the Agent Server is deployed.

Example `curl` command:

```shell
curl --request POST \
  --url http://localhost:8124/assistants/search \
  --header 'Content-Type: application/json' \
  --header 'X-Api-Key: LANGSMITH_API_KEY' \
  --data '{
  "metadata": {},
  "limit": 10,
  "offset": 0
}'
```
