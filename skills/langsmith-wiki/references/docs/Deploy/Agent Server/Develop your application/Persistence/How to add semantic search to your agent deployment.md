# How to add semantic search to your agent deployment

Semantic search lets your agent recall stored memories and documents by meaning rather than exact wording. For example, a query for "UI preferences" surfaces a memory written as "user prefers dark interfaces". This guide shows you how to enable semantic search on your deployment's cross-thread [store](https://docs.langchain.com/oss/python/langgraph/stores.md) so your agent retains context across conversations and personalizes responses based on prior interactions.

## Prerequisites

* A deployment (refer to [how to set up an application for deployment](../Set%20up%20dependencies/How%20to%20set%20up%20an%20application%20with%20requirements.txt.md)) and details on [hosting options](../../../../LangSmith%20setup/Overview/Hosting/Set%20up%20LangSmith.md).
* API keys for your embedding provider (in this case, OpenAI).
* `langchain >= 0.3.8` (if you specify using the string format in this guide).

## Steps

1. Update your [`langgraph.json` configuration file](../Application%20structure.md#configuration-file) to include the store configuration:

   ```json
   {
       ...
       "store": {
           "index": {
               "embed": "openai:text-embedding-3-small",
               "dims": 1536,
               "fields": ["$"]
           }
       }
   }
   ```

   This configuration:

   * Uses OpenAI's text-embedding-3-small model for generating embeddings.
   * Sets the embedding dimension to 1536 (matching the model's output).
   * Indexes all fields in your stored data (`["$"]` means index everything, or specify specific fields like `["text", "metadata.title"]`).

   > [!NOTE]
   >
   > Each deployment supports a single embedding model. LangSmith does not support configuring multiple embedding models, because it would cause ambiguity in `/store` endpoints and result in mixed-index issues.

2. To use the string embedding format, make sure your dependencies include `langchain >= 0.3.8`:

   ```toml
   # In pyproject.toml
   [project]
   dependencies = [
       "langchain>=0.3.8"
   ]
   ```

   Or, if using [requirements.txt](../Set%20up%20dependencies/How%20to%20set%20up%20an%20application%20with%20requirements.txt.md):

   ```
   langchain>=0.3.8
   ```

## Usage

Once configured, you can use semantic search in your [nodes](https://docs.langchain.com/oss/python/langgraph/graph-api.md#nodes). The store requires a namespace tuple to organize memories:

```python
async def search_memory(state: State, *, store: BaseStore):
    # Search the store using semantic similarity
    # The namespace tuple helps organize different types of memories
    # e.g., ("user_facts", "preferences") or ("conversation", "summaries")
    results = await store.asearch(
        namespace=("memory", "facts"),  # Organize memories by type
        query="your search query",
        limit=3  # number of results to return
    )
    return results
```

Each result is a `SearchItem` (extends `Item` with an additional `score` field). When semantic search is configured, `score` contains the similarity score:

```python
results[0].key       # "07e0caf4-1631-47b7-b15f-65515d4c1843"
results[0].value     # {"text": "User prefers dark mode"}
results[0].namespace # ("memory", "facts")
results[0].score     # 0.92 (similarity score, present when semantic search is configured)
```

### Changing your embedding model

> [!WARNING]
>
> Changing the embedding model or dimensions requires re-embedding all existing data. There is no automated migration tooling for this. Plan accordingly if you need to switch models.

## Custom embeddings

If you want to use custom embeddings, you can pass a path to a custom embedding function:

```json
{
    ...
    "store": {
        "index": {
            "embed": "path/to/embedding_function.py:embed",
            "dims": 1536,
            "fields": ["$"]
        }
    }
}
```

The deployment will look for the function in the specified path. The function must be async and accept a list of strings:

```python
# path/to/embedding_function.py
from openai import AsyncOpenAI

client = AsyncOpenAI()

async def aembed_texts(texts: list[str]) -> list[list[float]]:
    """Custom embedding function that must:
    1. Be async
    2. Accept a list of strings
    3. Return a list of float arrays (embeddings)
    """
    response = await client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [e.embedding for e in response.data]
```

## Querying via the API

You can also query the store using the [LangGraph SDK](../../../Get%20started/Reference/Related/langgraph_sdk.md). Since the SDK uses async operations:

```python
from langgraph_sdk import get_client

async def search_store():
    client = get_client()
    results = await client.store.search_items(
        ("memory", "facts"),
        query="your search query",
        limit=3  # number of results to return
    )
    return results

# Use in an async context
results = await search_store()
```

Each result item includes a `score` field when semantic search is configured:

```python
results["items"][0]["key"]       # "07e0caf4-1631-47b7-b15f-65515d4c1843"
results["items"][0]["value"]     # {"text": "User prefers dark mode"}
results["items"][0]["namespace"] # ["memory", "facts"]
results["items"][0]["score"]     # 0.92 (similarity score)
```
