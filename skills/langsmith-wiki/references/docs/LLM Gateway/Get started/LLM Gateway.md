# LLM Gateway

> Route model calls from your agents through one LangSmith endpoint, with each call traced in LangSmith and governed by your organization's policies.

> [!NOTE]
>
> The LLM Gateway is in [beta](../../LangSmith%20setup/Cloud/Reference/Release%20stages.md).

The LLM Gateway is the control layer between the agents and applications you run and the model providers your workspace has configured. Because the gateway is part of LangSmith, each call it routes becomes a LangSmith trace that records the routing and policy decisions made for it. Your application authenticates with a [LangSmith API key](../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md). The gateway routes each request to the provider named in its model ID, traces the call, and applies your organization's governance policies.

Without the gateway, each application and deployment holds its own provider keys. Reliability, spend, and data controls are set up separately for each provider account. With the gateway, provider keys stay in LangSmith, and [model fallbacks](../Models%20and%20reliability/Model%20fallbacks.md), [spend limits](../Governance/Spend%20policies.md), [rate limits](../Governance/Rate%20limit%20policies.md), and [data policies](../Governance/Data%20policies.md) apply to every call in their scope. When a fallback fires or a policy blocks a call, the [trace](../Observability/View%20LLM%20Gateway%20traces.md) shows each attempt and policy check. Moreover, policy violations surface in [LangSmith Engine](../../Engine/LangSmith%20Engine.md) for triage.

## Choose a request format

The gateway accepts OpenAI Chat Completions, Anthropic Messages, and OpenAI Responses requests. The request format and the provider are independent: a Chat Completions request can call an Anthropic model, and the gateway translates the request and response when the provider uses a different native format. Keep the format your application already uses, and switch providers by changing the model ID. For endpoints, model ID syntax, and translation behavior, see [API formats](../Call%20the%20gateway/API%20formats.md).

LangChain chat models and Deep Agents reach the gateway through the `LANGSMITH_GATEWAY` environment variable, which uses [direct model access](../Call%20the%20gateway/Direct%20model%20access.md) in each provider's native format, so no translation applies.

## Choose how credentials are managed

The gateway calls each provider with a credential that LangSmith holds: your own provider key, stored as a workspace secret, or [Gateway Credits](../Models%20and%20reliability/Gateway%20Credits.md), which LangChain bills to your LangSmith account. For every credential source and who bills it, see [Provider authentication](../Authentication/Provider%20authentication.md#choose-a-credential-source).

## Next steps

Start with the guide for your role:

> [card] [Set up the gateway for your organization](Set%20up%20the%20LLM%20Gateway.md)
>
> Complete the initial setup to route requests through the gateway.

> [card] [Send your first request](Send%20your%20first%20LLM%20Gateway%20request.md)
>
> Send a request from the Simulator, call the gateway from your code, and view the trace.

For further questions, contact [LangChain support](https://support.langchain.com).
