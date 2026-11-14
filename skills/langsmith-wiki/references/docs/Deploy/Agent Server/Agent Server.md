# Agent Server

> Configure and operate the LangSmith Agent Server runtime, including capabilities, application structure, auth, and customization.

Configure and build applications on the [Agent Server](Capabilities/Agent%20Server.md) runtime. Once deployed, agents work with three primitives: [**assistants**](Capabilities/Assistants/Assistants.md) for configuration, [**threads**](Capabilities/Use%20threads.md) for state, and [**runs**](Capabilities/Runs/Runs.md) for workloads. The pages in this tab cover the capabilities Agent Server provides, how to [structure your application](Develop%20your%20application/Application%20structure.md), and how to [secure](Auth%20%26%20access%20control/Authentication%20%26%20access%20control.md) and [customize](Server%20customization/Extend%20the%20HTTP%20server/How%20to%20add%20custom%20routes.md) the server.

## Capabilities

> [card] [Develop your application](Develop%20your%20application/Application%20structure.md)
>
> Structure your app, configure dependencies for Python, JavaScript, and monorepos, and connect agents with RemoteGraph, semantic search, TTLs, and CI/CD.

> [card] [Agent Server runtime](Capabilities/Agent%20Server.md)
>
> Work with assistants, threads, runs, and cron jobs. Stream to users, pause for human review, handle concurrent input, and connect via MCP and A2A.

> [card] [Auth & access control](Auth%20%26%20access%20control/Authentication%20%26%20access%20control.md)
>
> Authenticate users, enforce resource-level access, and connect external OAuth2 identity providers.

> [card] [Server customization](Server%20customization/Use%20server-side%20caching.md)
>
> Add caching, custom stores and checkpointers, lifespan hooks, middleware, custom routes, encryption, and configurable headers and logs.

> [card] [REST API](../Get%20started/Reference/Agent%20Server%20API/Agent%20Server%20API%20reference.md)
>
> Full REST API reference for assistants, threads, runs, crons, store, A2A, MCP, and system endpoints.

## Tutorials

* [Collect user feedback for Agent Server runs](How%20to%20build/How%20to%20collect%20user%20feedback%20for%20Agent%20Server%20runs.md): Attach end-user feedback to runs and traces
* [Deploy other frameworks (e.g., Strands, CrewAI)](../Get%20started/Frameworks%20and%20platforms/Deploy%20other%20frameworks.md): Wrap existing agents with Functional API and deploy
* [Implement generative user interfaces with LangGraph](How%20to%20build/How%20to%20implement%20generative%20user%20interfaces%20with%20LangGraph.md): Stream UI elements to a React client
* [Implement a CI/CD pipeline](How%20to%20build/Implement%20a%20CI-CD%20pipeline%20using%20LangSmith%20Agent%20Server%20and%20Evaluation.md): Automate tests, evaluations, and deployments with GitHub Actions

## Securing and customizing your server

* [Custom auth](Auth%20%26%20access%20control/Authentication%20%26%20access%20control.md): Authentication and multi-tenant access control
* [Server customization](Server%20customization/Extend%20the%20HTTP%20server/How%20to%20add%20custom%20routes.md): Custom routes, [middleware](Server%20customization/Extend%20the%20HTTP%20server/How%20to%20add%20custom%20middleware.md), [lifespan hooks](Server%20customization/Extend%20the%20HTTP%20server/How%20to%20add%20custom%20lifespan%20events.md), [encryption](Server%20customization/Encryption%20at%20rest/Encryption%20at%20rest.md)

## Operations

* [CI/CD pipelines](How%20to%20build/Implement%20a%20CI-CD%20pipeline%20using%20LangSmith%20Agent%20Server%20and%20Evaluation.md)
* [TTL configuration](Develop%20your%20application/Persistence/How%20to%20add%20TTLs%20to%20your%20application.md) for state and thread management
* [Semantic search](Develop%20your%20application/Persistence/How%20to%20add%20semantic%20search%20to%20your%20agent%20deployment.md)
