# Assistants

*Assistants* are an [Agent Server](../Agent%20Server.md) concept that allow you to manage configurations (e.g., prompts, LLM selection, tools) separately from your graph's core logic. This enables you to create multiple, specialized versions of the same graph architecture with different behavior at runtime. Through configuration variations (rather than structural graph changes), each assistant is optimized for a different [use case](#use-cases).

For example, imagine a general-purpose writing agent built on a common graph architecture. While the structure remains the same, different writing styles—such as blog posts and tweets—require tailored configurations to optimize performance. To support these variations, you can create multiple assistants (e.g., one for blogs and another for tweets) that share the underlying graph but differ in model selection and system prompt.

![assistant versions](../../../../../assets/images/9e0d7faf633f-assistants.png)

The Agent Server API provides several endpoints for creating and managing assistants and their versions. See the [API reference](../../../Get%20started/Reference/Agent%20Server%20API/Agent%20Server%20API%20reference.md) for more details.

> [!NOTE]
>
> Assistants are a [LangSmith Agent Server](../../../Get%20started/LangSmith%20Agent%20Server.md) concept. They are not available in the open source LangGraph library.

## How assistants work with deployments

When you deploy a graph to [LangSmith Agent Server](../Agent%20Server.md), it automatically creates a **default assistant** tied to that graph's default configuration. You can then create additional assistants for the same graph, each with its own configuration.

If your deployment defines multiple graphs in [`langgraph.json`](../../Develop%20your%20application/Application%20structure.md#configuration-file), each graph gets its own default assistant:

```json
{
    "graphs": {
        "graph_id_1": "path_to_graph_id_1",  // default assistant created for graph_id_1
        "graph_id_2": "path_to_graph_id_2"   // default assistant created for graph_id_2
    }
}
```

That is, there can be multiple default assistants—one for each graph defined in your deployment.

Assistants have several key features:

* **[Managed via API and UI](Manage%20assistants.md)**: Create, list, update, version, and get assistants using the Agent Server/LangGraph SDKs or the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-assistants).
* **One graph, multiple assistants**: A single deployed graph can support multiple assistants, each with different configurations (e.g., prompts, models, tools).
* **[Versioned](#versioning) configurations**: Each assistant maintains its own configuration history through versioning. Editing an assistant creates a new version, and you can promote or roll back to any version.
* **[Configuration](#configuration) updates without graph changes**: Update prompts, model selection, and other settings through assistant configurations, enabling rapid iteration without modifying or redeploying your graph code.

> [!NOTE]
>
> When invoking an assistant, you can specify either in [`langgraph.json`](../../Develop%20your%20application/Application%20structure.md#configuration-file):
>
> * A **graph ID** (e.g., `"agent"`): Uses the default assistant for that graph
> * An **assistant ID** (UUID): Uses a specific assistant configuration
>
> This flexibility allows you to quickly test with default settings or precisely control which configuration is used.

### Configuration

Assistants build on the LangGraph open source concept of [configuration](https://docs.langchain.com/oss/python/langgraph/graph-api.md#runtime-context).

While configuration is available in the open source LangGraph library, assistants are only present in [LangSmith Agent Server](../../../Get%20started/LangSmith%20Agent%20Server.md) because they are tightly coupled to your deployed graph. Upon deployment, [Agent Server](../Agent%20Server.md) will automatically create a default assistant for each graph using the graph's default configuration settings.

In practice, an assistant is just an *instance* of a graph with a specific configuration. Therefore, multiple assistants can reference the same graph but can contain different configurations (e.g. prompts, models, tools). The LangSmith Agent Server API provides several endpoints for creating and managing assistants. See the [API reference](../../../Get%20started/Reference/Agent%20Server%20API/Agent%20Server%20API%20reference.md) and [this how-to](Manage%20assistants.md) for more details on how to create assistants.

### Use cases

Assistants are ideal when you need to deploy the same graph architecture with different configurations. Common use cases include:

* **User-level personalization**
  * Customize model selection, system prompts, or tool availability per user.
  * Store user preferences and apply them automatically to each interaction.
  * Enable users to choose between different AI personalities or expertise levels.

* **Customer or organization-specific configurations**
  * Maintain separate configurations for different customers or organizations.
  * Customize behavior for each client without deploying separate infrastructure.
  * Isolate configuration changes to specific customers.

```mermaid actions={false}
graph TD
    A["Graph: agent<br/>(deployed)"]
    A --> B["Customer A Assistant<br/>━━━━━━━━━━━━━<br/>Model: GPT-4<br/>Tone: Legal<br/>Tools: Custom"]
    A --> C["Customer B Assistant<br/>━━━━━━━━━━━━━<br/>Model: Claude<br/>Tone: Casual<br/>Tools: Standard"]
    A --> D["Customer C Assistant<br/>━━━━━━━━━━━━━<br/>Model: GPT-3.5<br/>Tone: Formal<br/>Tools: Limited"]

    style A fill:#E5F4FF,stroke:#006DDD,stroke-width:3px,color:#030710
    style B fill:#B3E0F2,stroke:#4A90E2,stroke-width:2px,color:#1E3A5F
    style C fill:#B3E0F2,stroke:#4A90E2,stroke-width:2px,color:#1E3A5F
    style D fill:#B3E0F2,stroke:#4A90E2,stroke-width:2px,color:#1E3A5F
```

* **Environment-specific configurations**
  * Use different models or settings for development, staging, and production.
  * Test configuration changes in staging before promoting to production.
  * Reduce costs in non-production environments with smaller models.

* **A/B testing and experimentation**
  * Compare different prompts, models, or parameter settings.
  * Roll out configuration changes gradually to a subset of users.
  * Measure performance differences between configuration variants.

* **Specialized task variants**
  * Create domain-specific versions of a general-purpose agent.
  * Optimize configurations for different languages, regions, or industries.
  * Maintain consistent graph logic while varying the execution details.

```mermaid actions={false}
graph TD
    A["Graph: writing-agent<br/>(deployed)"]
    A --> B["Blog Assistant<br/>━━━━━━━━━━━━━<br/>Model: GPT-4<br/>Tone: Formal<br/>Style: Long-form<br/>Tools: SEO optimization"]
    A --> C["Tweet Assistant<br/>━━━━━━━━━━━━━<br/>Model: GPT-4-mini<br/>Tone: Casual<br/>Style: 280-char limit<br/>Tools: Hashtag suggestions"]
    A --> D["Email Assistant<br/>━━━━━━━━━━━━━<br/>Model: GPT-4<br/>Tone: Professional<br/>Style: Medium length<br/>Tools: Templates"]

    style A fill:#E5F4FF,stroke:#006DDD,stroke-width:3px,color:#030710
    style B fill:#B3E0F2,stroke:#4A90E2,stroke-width:2px,color:#1E3A5F
    style C fill:#B3E0F2,stroke:#4A90E2,stroke-width:2px,color:#1E3A5F
    style D fill:#B3E0F2,stroke:#4A90E2,stroke-width:2px,color:#1E3A5F
```

### Versioning

Assistants support versioning to track changes over time. Once you've created an assistant, subsequent edits will automatically create new versions.

* Each update creates a new version of the assistant.
* You can promote any version to be the active version.
* Rolling back to a previous version is as simple as setting it as active.
* All versions remain available for reference and rollback.

> [!WARNING]
>
> When updating an assistant, you must provide the entire configuration payload. The update endpoint creates new versions from scratch and does not merge with previous versions. Make sure to include all configuration fields you want to retain.

For more details on how to manage assistant versions, refer to the [Manage assistants guide](Manage%20assistants.md#create-a-new-version-for-your-assistant).
