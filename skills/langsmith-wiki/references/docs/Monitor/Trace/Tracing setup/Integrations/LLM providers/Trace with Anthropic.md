# Trace with Anthropic

> Send Anthropic traces to LangSmith from the Claude Platform, from the Claude SDKs over OpenTelemetry, or with the LangSmith SDK wrapper.

You can send Anthropic traces to LangSmith from Anthropic's servers or from your own agent:

* **[From the Claude Platform](#trace-from-the-claude-platform)**: The Claude Platform sends traces directly from Anthropic's servers. You configure it in the Claude Console, with no changes to your agent code.
* **[From your agent](#trace-from-your-application)**: Your agent sends the traces, in one of two ways:
  * **[Claude SDKs](#use-the-claude-sdks)**: The Claude SDKs emit OpenTelemetry (OTel) spans, and an OTel exporter library sends them to LangSmith.
  * **[LangSmith SDK wrapper](#use-the-langsmith-sdk-wrapper)**: You wrap the Anthropic client with the LangSmith SDK (Python or TypeScript). You can combine the traces with `@traceable` spans for the rest of your code in a single trace.

> [!NOTE]
>
> Tracing from the Claude Platform and the Claude SDKs is in public beta.

> [!NOTE]
>
> In an [agent-based workspace](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

## Trace from the Claude Platform

The Claude Platform exports OTel traces of your [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) sessions and [Messages API](https://platform.claude.com/docs/en/api/messages) requests. It sends them to a *destination*, an OTel endpoint that you register in the Claude Console. You can add LangSmith as a destination and view these traces without changing your agent code. For details on destinations and delivery, see [Use OpenTelemetry with the Claude API](https://platform.claude.com/docs/en/manage-claude/opentelemetry/api) in the Anthropic docs.

Before you begin, you need:

* The admin role, or an equivalent permission, in your Claude Console organization. Without it, you cannot view or manage destinations.
* A LangSmith API key. You can use a [personal access token](../../../../../LangSmith%20setup/Govern/Organization/Overview.md#personal-access-tokens-pats), or a [service key](../../../../../LangSmith%20setup/Govern/Organization/Overview.md#service-keys) when you want tracing to be independent of your user account. To create a key, see [Create an account and API key](../../../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md).
* In an agent-based workspace, the selected agent environment's [`tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project), which goes in the destination's **Project** field.
* For self-hosted LangSmith, an endpoint that the Claude Platform can reach: HTTPS on port 443, at a hostname that resolves to a public IP address.

### Step 1. Add LangSmith as a destination

To add a destination:

1. In the Claude Console, open the [OpenTelemetry settings page](https://platform.claude.com/settings/telemetry-destinations) of your organization and click **Add destination**.
2. In the **Provider** drop-down, select **LangSmith**. The form changes to show the LangSmith fields.
3. Complete the fields:
   * **Name**: (Optional) A label for the destination, such as `LangSmith`.
   * **Region**: The region of your LangSmith deployment: **US**, **EU**, **APAC**, or **US on AWS**. For self-hosted LangSmith, select **Self-hosted**. In **LangSmith URL**, enter your LangSmith API URL (`LANGSMITH_ENDPOINT`) plus `/otel`. For the URL on each deployment type, see [Find your OTLP endpoint](../Agent%20frameworks/Trace%20with%20OpenTelemetry.md#find-your-otlp-endpoint).
   * **API key**: Your LangSmith API key.
   * **Project**: The [environment's `tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) to send traces to. Set it explicitly in an agent-based workspace. If omitted, the integration uses `default`.
   * **LangSmith workspace ID**: (Optional) The ID of the LangSmith workspace to send traces to. If you leave it empty, traces go to the workspace that the API key belongs to. Organization-scoped service keys require it. To find the ID, see [Create an account and API key](../../../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md).
   * **Content mode**: Select **Full content** to include prompts and responses in the spans. With **Metadata only**, spans omit the input and output content.
   * **Workspaces**: The Claude workspaces that send traces to this destination: **All**, **Selected**, or **All except**. For details on each option, see [Choose workspaces for a destination](https://platform.claude.com/docs/en/manage-claude/opentelemetry/api#choose-workspaces-for-a-destination) in the Anthropic docs.
4. Click **Add destination**.

When you edit the destination later, the form shows the generic **OTLP endpoint URL** and **Request headers** fields instead of the LangSmith fields. The **OTLP endpoint URL** holds the URL of your region, and the LangSmith fields become these request headers:

* `x-api-key`: The **API key**.
* `Langsmith-Project`: The **Project**, if you set one.
* `X-Tenant-Id`: The **LangSmith workspace ID**, if you set one.

If you change the host of the **OTLP endpoint URL**, enter the header values again.

### Step 2. Check that traces arrive

To check the setup:

1. Send a Messages API request or run a Claude Managed Agents session in a Claude workspace that uses the destination.
2. On the Claude Console OpenTelemetry settings page, check that the **Delivery** column of the destination shows **Healthy**. This can take about a minute.
3. In LangSmith, select the agent and environment whose `tracer_session_name` you entered in the **Project** field.

### Troubleshoot delivery

If the **Delivery** column on the Claude Console [OpenTelemetry settings page](https://platform.claude.com/settings/telemetry-destinations) shows **Failing**, hold the pointer over it to see the last error:

| Error | Cause | Fix |
| - | - | - |
| HTTP 401 | The destination sends no API key. | Set the `x-api-key` request header to your LangSmith API key. |
| HTTP 403 | The API key is wrong, expired, or deleted, or it is an organization-scoped service key without a workspace ID. | Set `x-api-key` to a valid key. For an organization-scoped service key, also set `X-Tenant-Id` to the workspace ID. |
| HTTP 404 | The endpoint URL is wrong. | Set **OTLP endpoint URL** to your LangSmith API URL (`LANGSMITH_ENDPOINT`) plus `/otel`, without `/v1/traces`. See [Find your OTLP endpoint](../Agent%20frameworks/Trace%20with%20OpenTelemetry.md#find-your-otlp-endpoint). |
| Invalid address | The hostname does not resolve to a public IP address. | Serve the LangSmith endpoint at a public hostname over HTTPS on port 443. |

For other errors, see [Delivery errors](https://platform.claude.com/docs/en/manage-claude/opentelemetry/api#delivery-errors) in the Anthropic docs.

If the **Delivery** column shows **Disabled**, hold the pointer over it to see why. For example, the Claude Platform disables a destination when all deliveries fail for 24 hours or when the endpoint sends a redirect, and it drops spans while the destination is disabled. See [Delivery and health](https://platform.claude.com/docs/en/manage-claude/opentelemetry/api#delivery-and-health) in the Anthropic docs.

## Trace from your agent

Use one of these methods when your agent should send the traces. To trace your Anthropic calls together with the rest of your code in a single trace, use the LangSmith SDK wrapper.

### Use the Claude SDKs

The Claude SDKs emit OTel spans in your agent for each request that they send and for each tool use that the tool runner runs. An OTel exporter library sends the spans to LangSmith. For details on the SDK options and the spans that the SDKs emit, see [Set up SDK tracing](https://platform.claude.com/docs/en/manage-claude/opentelemetry/sdk) in the Anthropic docs.

To send Claude SDK spans to LangSmith:

1. [Install or upgrade the Claude SDK](https://platform.claude.com/docs/en/manage-claude/opentelemetry/sdk#install-the-sdk) and [register a tracer provider](https://platform.claude.com/docs/en/manage-claude/opentelemetry/sdk#register-a-tracer-provider).
2. Configure an OTel exporter with your LangSmith API URL (`LANGSMITH_ENDPOINT`) plus `/otel` as the base endpoint. For the URL on each deployment type, see [Find your OTLP endpoint](../Agent%20frameworks/Trace%20with%20OpenTelemetry.md#find-your-otlp-endpoint).

   Set the following request headers:

   * `x-api-key`: Your LangSmith API key.
   * `Langsmith-Agent-Id`: The registered agent identifier.
   * `Langsmith-Agent-Environment`: The environment, such as `local`.
   * `X-Tenant-Id`: (Optional) The ID of the LangSmith workspace to send traces to. Without this header, traces go to the workspace that the API key belongs to. Organization-scoped service keys require it.

   For example, with the standard OTel environment variables:

   ```bash
   export OTEL_EXPORTER_OTLP_ENDPOINT=https://api.smith.langchain.com/otel
   export OTEL_EXPORTER_OTLP_HEADERS="x-api-key=<your-langsmith-api-key>,Langsmith-Agent-Id=<your-agent-id>,Langsmith-Agent-Environment=local"
   ```

   For more information on exporter setup, see [Trace a non-LangChain agent](../Agent%20frameworks/Trace%20with%20OpenTelemetry.md#trace-a-non-langchain-application).
3. (Optional) By default, the Claude SDKs record metadata only. To include prompts and responses in the spans, set the content mode. See [Configure the SDK](https://platform.claude.com/docs/en/manage-claude/opentelemetry/sdk#configure-the-sdk) in the Anthropic docs.

### Use the LangSmith SDK wrapper

The Anthropic wrapper methods in Python ([`wrap_anthropic`](https://reference.langchain.com/python/langsmith/wrappers/_anthropic/wrap_anthropic)) and TypeScript ([`wrapAnthropic`](https://reference.langchain.com/javascript/langsmith/wrappers/anthropic/wrapAnthropic)) wrap your Anthropic client to log traces automatically. With the wrapper, LangSmith renders messages, including tool calls and multimodal content blocks, in a readable format. The wrapper works alongside the `@traceable` decorator (Python) or `traceable` function (TypeScript), so you can trace your Anthropic calls with the wrapper and trace other parts of your agent with the decorator or function.

> [!NOTE]
>
> Set the `LANGSMITH_TRACING` environment variable to `'true'` to log traces to LangSmith, even when you use `wrap_anthropic` or `wrapAnthropic`. This lets you toggle tracing on and off without changing your code.
>
> Also set the `LANGSMITH_API_KEY` environment variable to your API key. To create a key, see [Create an account and API key](../../../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md).
>
> The wrapper sends traces through the LangSmith SDK, not OTLP, so set `LANGSMITH_ENDPOINT` to your LangSmith API URL without `/otel`.
>
> `LANGSMITH_ENDPOINT` defaults to `https://api.smith.langchain.com` (GCP US). Set it to your data plane URL on [BYOC](../../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md), your instance URL on [self-hosted](../../../../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md), or the [API URL for your region](../../../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md#configure-the-sdk) on other Cloud regions.
>
> If your LangSmith API key is linked to multiple workspaces, set the `LANGSMITH_WORKSPACE_ID` environment variable to specify which workspace to use.
>
> Set `LANGSMITH_AGENT_ID` and `LANGSMITH_AGENT_ENVIRONMENT` to the registered agent and environment. See [Configure tracing for the agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#configure-tracing-for-the-agent).

```python Python
import anthropic
from langsmith import traceable
from langsmith.wrappers import wrap_anthropic

client = wrap_anthropic(anthropic.Anthropic())

@traceable(run_type="tool", name="Retrieve Context")
def my_tool(question: str) -> str:
  return "During this morning's meeting, we solved all world conflict."

@traceable(name="Chat Pipeline")
def chat_pipeline(question: str):
  context = my_tool(question)
  messages = [
      { "role": "user", "content": f"Question: {question}\nContext: {context}"}
  ]
  message = client.messages.create(
      model="claude-sonnet-5-5",
      messages=messages,
      max_tokens=1024,
      system="You are a helpful assistant. Please respond to the user's request only based on the given context."
  )
  return message

chat_pipeline("Can you summarize this morning's meetings?")
```

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";
import { traceable } from "langsmith/traceable";
import { wrapAnthropic } from "langsmith/wrappers/anthropic";

const client = wrapAnthropic(new Anthropic());

const myTool = traceable(async (question: string) => {
  return "During this morning's meeting, we solved all world conflict.";
}, { name: "Retrieve Context", run_type: "tool" });

const chatPipeline = traceable(async (question: string) => {
  const context = await myTool(question);
  const messages = [
      { role: "user", content: `Question: ${question}\nContext: ${context}` }
  ];
  const message = await client.messages.create({
      model: "claude-sonnet-5-5",
      messages: messages,
      max_tokens: 1024,
      system: "You are a helpful assistant. Please respond to the user's request only based on the given context."
  });
  return message;
}, { name: "Chat Pipeline" });

await chatPipeline("Can you summarize this morning's meetings?");
```

To trace [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) sessions with the TypeScript `wrapAnthropic` wrapper, see [Trace Claude Managed Agents](../Agent%20frameworks/Trace%20Claude%20Managed%20Agents.md).
