# INVALID_TOOL_RESULTS

> [!NOTE]
>
> Currently only used in `langchainjs` (JavaScript/TypeScript).

This error occurs when passing mismatched, insufficient, or excessive [`ToolMessage`](https://reference.langchain.com/python/langchain-core/messages/tool/ToolMessage) objects to a model during tool calling operations.

The error stems from a fundamental requirement: an assistant message with `tool_calls` must be followed by tool messages responding to each `tool_call_id`.

When a model returns an [`AIMessage`](https://reference.langchain.com/python/langchain-core/messages/ai/AIMessage) with tool calls, you must provide exactly one corresponding [`ToolMessage`](https://reference.langchain.com/python/langchain-core/messages/tool/ToolMessage) for each tool call, with matching `tool_call_id` values.

## Common causes

* **Insufficient responses**: If a model requests two tool executions but you only provide one response message, the model rejects the incomplete message chain
* **Duplicate responses**: Providing multiple [`ToolMessage`](https://reference.langchain.com/python/langchain-core/messages/tool/ToolMessage) objects for the same tool call ID results in rejection, as does having unmatched IDs
* **Orphaned tool messages**: Sending a [`ToolMessage`](https://reference.langchain.com/python/langchain-core/messages/tool/ToolMessage) without a preceding [`AIMessage`](https://reference.langchain.com/python/langchain-core/messages/ai/AIMessage) containing tool calls violates protocol requirements

Here's an example of a problematic pattern:

```python
# Model requests two tool calls
response_message.tool_calls  # Returns 2 calls

# But only one ToolMessage provided
chat_history.append(ToolMessage(
    content=str(tool_response),
    tool_call_id=tool_call.get("id")
))

model_with_tools.invoke(chat_history)
```

## Troubleshooting

To resolve this error:

* **Count matching pairs**: Ensure one [`ToolMessage`](https://reference.langchain.com/python/langchain-core/messages/tool/ToolMessage) exists per tool call in the preceding [`AIMessage`](https://reference.langchain.com/python/langchain-core/messages/ai/AIMessage)
* **Verify IDs**: Confirm each `ToolMessage.tool_call_id` matches an actual tool call identifier

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/errors/INVALID_TOOL_RESULTS.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
