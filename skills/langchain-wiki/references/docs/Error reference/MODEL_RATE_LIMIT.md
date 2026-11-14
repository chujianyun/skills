# MODEL_RATE_LIMIT

> [!NOTE]
>
> Currently only used in `langchainjs` (JavaScript/TypeScript).

You have hit the maximum number of requests that a model provider allows over a given time period and are being temporarily blocked.

This error occurs when you exceed the maximum number of requests permitted by your model provider within a specific timeframe, resulting in temporary blocking. The restriction is generally temporary and lifts after the limit resets.

## Troubleshooting

To resolve this error, you can:

1. **Implement Rate Limiting**: Deploy a rate limiter to regulate the frequency of requests sent to the model.
   See [rate limiting](../Core%20components/Models.md#rate-limiting) docs.

2. **Implement Response Caching**: Use model response caching to reduce redundant requests when incoming queries are repetitive.

3. **Use Multiple Providers**: Distribute requests across multiple providers if your application architecture supports this approach

4. **Contact Your Provider**: Reach out to your model provider requesting an increase to your rate limits

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/errors/MODEL_RATE_LIMIT.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
