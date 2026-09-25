# developers.llamaindex.ai/python/framework/community/integrations/graphsignal/index.md
> https://developers.llamaindex.ai/python/framework/community/integrations/graphsignal/index.md

--- title: Tracing with Graphsignal | Developer Documentation ---
Graphsignal [1] provides observability for AI agents and LLM-powered applications. It helps developers ensure AI applications run as expected and users have the best experience.
Graphsignal **automatically** traces and monitors LlamaIndex. Traces and metrics provide execution details for query, retrieval, and index operations. These insights include **prompts**, **completions**, **embedding statistics**, **retrieved nodes**, **parameters**, **latency**, and **exceptions**.
When OpenAI APIs are used, Graphsignal provides additional insights such as **token counts** and **costs** per deployment, model or any context.
### Installation and Setup
Adding Graphsignal tracer [2] is simple, just install and configure it:
Terminal window
``` pip install graphsignal ```
``` import graphsignal

# Provide an API key directly or via GRAPHSIGNAL_API_KEY environment variable graphsignal.configure( api_key="my-api-key", deployment="my-llama-index-app-prod" ) ```

You can get an API key here [3].
See the Quick Start guide [4], Integration guide [5], and an [example app] [6] for more information.
### Tracing Other Functions
To additionally trace any function or code, you can use a decorator or a context manager:
``` with graphsignal.start_trace("load-external-data"): reader.load_data() ```

See Python API Reference [7] for complete instructions.
### Useful Links
- Tracing and Monitoring LlamaIndex Applications [8] - Monitor OpenAI API Latency, Tokens, Rate Limits, and More [9] - OpenAI API Cost Tracking: Analyzing Expenses by Model, Deployment, and Context [10]

[1] https://graphsignal.com/
[2] https://github.com/graphsignal/graphsignal-python
[3] https://app.graphsignal.com/
[4] https://graphsignal.com/docs/guides/quick-start/
[5] https://graphsignal.com/docs/integrations/llama-index/
[6] https://github.com/graphsignal/examples/blob/main/llama-index-app/main.py
[7] https://graphsignal.com/docs/reference/python-api/
[8] https://graphsignal.com/blog/tracing-and-monitoring-llama-index-applications/
[9] https://graphsignal.com/blog/monitor-open-ai-api-latency-tokens-rate-limits-and-more/
[10] https://graphsignal.com/blog/open-ai-api-cost-tracking-analyzing-expenses-by-model-deployment-and-context/