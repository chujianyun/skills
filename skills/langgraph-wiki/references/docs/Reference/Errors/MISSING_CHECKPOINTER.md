# MISSING_CHECKPOINTER

You are attempting to use built-in LangGraph persistence without providing a checkpointer.

This happens when a `checkpointer` is missing in the `compile()` method of [`StateGraph`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph) or [`@entrypoint`](https://reference.langchain.com/python/langgraph/func/entrypoint).

## Troubleshooting

The following may help resolve this error:

* Initialize and pass a checkpointer to the `compile()` method of [`StateGraph`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph) or [`@entrypoint`](https://reference.langchain.com/python/langgraph/func/entrypoint).

```python
from langgraph.checkpoint.memory import InMemorySaver
checkpointer = InMemorySaver()

# Graph API
from langgraph.graph import StateGraph
graph = StateGraph(...).compile(checkpointer=checkpointer)

# Functional API
from langgraph.func import entrypoint
@entrypoint(checkpointer=checkpointer)
def workflow(messages: list[str]) -> str:
    ...
```

* Use the LangGraph API so you don't need to implement or configure checkpointers manually. The API handles all persistence infrastructure for you.

## Related

* Read more about [persistence](../../Capabilities/Persistence.md).
