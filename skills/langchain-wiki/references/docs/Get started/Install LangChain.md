# Install LangChain

> Install the LangChain package and the independent provider packages for the models and integrations you use.

To install the LangChain package:

```bash pip
pip install -U langchain
# Requires Python 3.10+
```

```bash uv
uv add langchain
# Requires Python 3.10+
```

LangChain provides integrations to hundreds of LLMs and thousands of other integrations. These live in independent provider packages.

```bash pip
# Installing the OpenAI integration
pip install -U langchain-openai

# Installing the Anthropic integration
pip install -U langchain-anthropic
```

```bash uv
# Installing the OpenAI integration
uv add langchain-openai

# Installing the Anthropic integration
uv add langchain-anthropic
```

> [!TIP]
>
> See the [Integrations tab](https://docs.langchain.com/oss/python/integrations/providers/overview.md) for a full list of available integrations.

Now that you have LangChain installed, you can get started by following the [Quickstart guide](Quickstart.md).

> [!TIP]
>
> Set up [LangSmith](https://smith.langchain.com?utm_source=docs\&utm_medium=cta\&utm_campaign=langsmith-signup\&utm_content=oss-langchain-install) tracing to debug your first LangChain app. Follow the [tracing quickstart](https://docs.langchain.com/langsmith/trace-with-langchain.md) to get started. We recommend you also set up [LangSmith Engine](https://docs.langchain.com/langsmith/engine.md) which monitors your traces, detects issues, and proposes fixes.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/install.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
