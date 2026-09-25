# developers.llamaindex.ai/python/framework/community/integrations/graph_stores/index.md
> https://developers.llamaindex.ai/python/framework/community/integrations/graph_stores/index.md

--- title: Using Graph Stores | Developer Documentation ---
## `Neo4jGraphStore`
`Neo4j` is supported as a graph store integration. You can persist, visualize, and query graphs using LlamaIndex and Neo4j. Furthermore, existing Neo4j graphs are directly supported using `text2cypher` and the `KnowledgeGraphQueryEngine`.
If you’ve never used Neo4j before, you can download the desktop client here [1].
Once you open the client, create a new project and install the `apoc` integration. Full instructions here [2]. Just click on your project, select `Plugins` on the left side menu, install APOC and restart your server.
See the example of using the Neo4j Graph Store.
## `NebulaGraphStore`
We support a `NebulaGraphStore` integration, for persisting graphs directly in Nebula! Furthermore, you can generate cypher queries and return natural language responses for your Nebula graphs using the `KnowledgeGraphQueryEngine`.

- Nebula Graph Store - Knowledge Graph Query Engine
## `FalkorDBGraphStore`
We support a `FalkorDBGraphStore` integration, for persisting graphs directly in FalkorDB! Furthermore, you can generate cypher queries and return natural language responses for your FalkorDB graphs using the `KnowledgeGraphQueryEngine`.

- FalkorDB Graph Store
## `Amazon Neptune Graph Stores`
We support `Amazon Neptune` integrations for both Neptune Database [3] and Neptune Analytics [4] as a graph store integration.

- Amazon Neptune Graph Store.
## `TiDB Graph Store`
We support a `TiDBGraphStore` integration, for persisting graphs directly in TiDB [5]!
See the associated guides below:
- TiDB Graph Store

[1] https://neo4j.com/download/
[2] https://neo4j.com/labs/apoc/4.1/installation/
[3] https://docs.aws.amazon.com/neptune/latest/userguide/feature-overview.html
[4] https://docs.aws.amazon.com/neptune- analytics/latest/userguide/what-is-neptune-analytics.html
[5] https://docs.pingcap.com/tidb/stable/overview