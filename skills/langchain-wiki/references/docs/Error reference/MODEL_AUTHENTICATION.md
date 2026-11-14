# MODEL_AUTHENTICATION

> [!NOTE]
>
> Currently only used in `langchainjs` (JavaScript/TypeScript).

Your model provider is denying you access to their service.

This error typically occurs when there's an issue with your authentication credentials or API keys.

## Troubleshooting

* Confirm that your API key or authentication credentials are accurate and valid.
* If using environment-based authentication, verify:
  * The variable name is spelled correctly
  * The variable contains an assigned value
  * Third-party packages like `dotenv` haven't interfered with loading
* If using a proxy or non-standard endpoint, make sure that your custom provider does not expect an alternative authentication scheme.
* Bypass environment variable issues by passing credentials explicitly:

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(api_key="<API_KEY>")
```

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/errors/MODEL_AUTHENTICATION.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
