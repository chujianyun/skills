# OUTPUT_PARSING_FAILURE

An [output parser](https://reference.langchain.com/python/langchain-core/output_parsers) was unable to handle model output as expected.

> [!NOTE]
>
> Some prebuilt constructs like legacy LangChain agents and chains may use output parsers internally, so you may see this error even if you're not visibly instantiating and using an output parser.

## Troubleshooting

* Consider using tool calling or other structured output techniques if possible without an output parser to reliably output parseable values.
* Add more precise formatting instructions to your prompt.
* If you are using a smaller or less capable model, try using a more capable one.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/errors/OUTPUT_PARSING_FAILURE.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
