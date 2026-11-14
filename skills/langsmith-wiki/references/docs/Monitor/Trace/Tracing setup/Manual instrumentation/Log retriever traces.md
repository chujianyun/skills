# Log retriever traces

> Log retrieval steps in LangSmith traces for document-level visibility into your RAG pipeline.

Many LLM applications retrieve documents from vector databases, knowledge graphs, or other indexes as part of a retrieval-augmented generation (RAG) pipeline. LangSmith provides dedicated rendering for retriever steps, which makes it easier to inspect retrieved documents and diagnose retrieval issues.

> [!NOTE]
>
> These steps are **optional**. If you skip them, your retriever data will still be logged, but LangSmith will not render it with retriever-specific formatting.

To enable retriever-specific rendering, complete the following two steps.

## Set `run_type` to retriever

Pass [`run_type="retriever"`](../../../Debug/Data%20type%20reference/Run%20%28span%29%20data%20format.md#run-types) to the [traceable](https://reference.langchain.com/python/langsmith/run_helpers/traceable) decorator (Python) or `traceable` wrapper (TypeScript). This tells LangSmith to treat the step as a retrieval run and apply retriever-specific rendering in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-log-retriever-trace):

```python
from langsmith import traceable

@traceable(run_type="retriever")
def retrieve_docs(query):
    ...
```

If you are using the [RunTree API](Custom%20instrumentation.md#use-the-runtree-api) instead of `traceable`, pass `run_type="retriever"` when creating the `RunTree` object.

## Return documents in the expected format

Return a list of dictionaries (Python) or objects (TypeScript) from your retriever function. Each item in the list represents a retrieved document and must contain the following fields:

| Field | Type | Description |
| - | - | - |
| `page_content` | string | The text content of the retrieved document. |
| `type` | string | Must always be `"Document"`. |
| `metadata` | object | Key-value pairs with metadata about the document, such as source URL, chunk ID, or score. This metadata is displayed alongside the document in the trace. |

The following examples show a complete retriever implementation with both requirements applied:

```python Python wrap
from langsmith import traceable

def _convert_docs(results):
    return [
        {
            "page_content": r,
            "type": "Document",
            "metadata": {"foo": "bar"}
        }
        for r in results
    ]

@traceable(run_type="retriever")
def retrieve_docs(query):
    # Returning hardcoded placeholder documents.
    # In production, replace with a real vector database or document index.
    contents = ["Document contents 1", "Document contents 2", "Document contents 3"]
    return _convert_docs(contents)

retrieve_docs("User query")
```

```typescript TypeScript wrap
import { traceable } from "langsmith/traceable";

interface Document {
    page_content: string;
    type: string;
    metadata: { foo: string };
}

function convertDocs(results: string[]): Document[] {
    return results.map((r) => ({
        page_content: r,
        type: "Document",
        metadata: { foo: "bar" }
    }));
}

const retrieveDocs = traceable((query: string): Document[] => {
    // Returning hardcoded placeholder documents.
    // In production, replace with a real vector database or document index.
    const contents = ["Document contents 1", "Document contents 2", "Document contents 3"];
    return convertDocs(contents);
}, {
    name: "retrieveDocs",
    run_type: "retriever"
});

await retrieveDocs("User query");
```

In the LangSmith UI, you'll find each retrieved document with its contents and metadata.

## Related

* [Annotate code for tracing](Custom%20instrumentation.md): Overview of all tracing methods, including `traceable`, `RunTree`, and the REST API.
* [Log LLM calls](Log%20LLM%20calls.md): Similar custom logging requirements for LLM steps.
