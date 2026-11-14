# INVALID_PROMPT_INPUT

Occurs when a [prompt template](https://github.com/langchain-ai/langchain/blob/v0.3/docs/docs/concepts/prompt_templates.mdx) received missing or invalid input variables.

## Troubleshooting

To resolve this error, you can:

1. Review your prompt template for correctness. When using f-string formats, ensure proper escaping of curly braces:
   * Use `{{` for single braces in f-strings
   * Use `{{{{` for double braces in f-strings
2. When using `MessagesPlaceholder` components, confirm you're passing message arrays or message-like objects. If using shorthand tuples, wrap variable names in curly braces like `["placeholder", "{messages}"]`
3. Debug by examining actual inputs to your prompt template by using [LangSmith](https://docs.langchain.com/langsmith/observability.md) or logging to verify they match expectations
4. If sourcing prompts from LangChain [Prompt Hub](https://smith.langchain.com/prompts), isolate and test the prompt with sample inputs to ensure it functions as intended

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/errors/INVALID_PROMPT_INPUT.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
