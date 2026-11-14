# LangSmith Observability

> Instrument your LLM application, investigate traces, and monitor performance in production with LangSmith.

# LangSmith Observability

LangSmith Observability provides full visibility into your LLM application: from individual traces to production-wide performance metrics. Traces are the record of what your agents did in production. Use them to debug failures, monitor quality, and build the datasets you evaluate against.

LangSmith works with many frameworks and providers. Browse [available integrations](../Trace/Tracing%20setup/Integrations/Integrations.md) to connect your stack including OpenAI, Anthropic, CrewAI, Vercel AI SDK, Pydantic AI, and more.

## Get started

**1. Create an account**

Sign up at [smith.langchain.com](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=snippets-langsmith-account-api-key-quickstart) (no credit card required).
You can log in with **Google**, **GitHub**, or **email**.

**2. Create an API key**

Go to your [Settings page](https://smith.langchain.com/settings) > **API Keys** > **Create API Key**.
Copy the key and save it securely.

Once your account and API key are ready, set up tracing:

> [card] [Set up tracing](../Trace/Tracing%20quickstart.md)
>
> Add tracing to your app in minutes with environment variables, framework integrations, or the SDK.

> [card] [Trace a RAG application](../Trace/Trace%20an%20agent.md)
>
> Follow a step-by-step tutorial to instrument a retrieval-augmented generation app from start to finish.

## Investigate and monitor

> [card] [View traces](../Debug/Viewing%20%26%20managing%20traces/View%20traces.md)
>
> Inspect threads and runs in the Messages, Turns, and Details views.

> [card] [Monitor performance](../Observe/Monitoring%20%26%20alerting/Monitor%20projects%20with%20dashboards.md)
>
> Build dashboards and set alerts to track quality and catch issues early.

> [card] [Configure automations](../Observe/Automations/Set%20up%20automation%20rules.md)
>
> Automate workflows with rules, webhooks, and online evaluations.

> [card] [Collect feedback](../../Test/Annotation%20Queues/Feedback/Log%20user%20feedback%20using%20the%20SDK.md)
>
> Annotate outputs and gather user feedback using queues or inline annotation.

> [card] [Find and fix failures with Engine](../../Engine/LangSmith%20Engine.md)
>
> Automatically detect recurring issues in your traces, diagnose their root cause, and resolve them with LangSmith Engine.

If your applications call models through the [LLM Gateway](../../LLM%20Gateway/Get%20started/LLM%20Gateway.md), the gateway traces every call itself, with no tracing setup in your code. For where those traces appear and what they record, see [View LLM Gateway traces](../../LLM%20Gateway/Observability/View%20LLM%20Gateway%20traces.md).

For terminology and core concepts, refer to [Observability concepts](../Trace/Observability%20concepts.md). For trace pricing, retention, and limits, see [Usage and billing](../Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md).

> [!NOTE]
>
> To set up a LangSmith instance, visit the [Platform setup section](../../LangSmith%20setup/Overview/Hosting/Set%20up%20LangSmith.md) to choose between cloud, hybrid, or self-hosted. All options include observability, evaluation, prompt engineering, and deployment.
