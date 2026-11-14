# Enable the LLM Gateway

> Enable the agent-gateway service on a self-hosted LangSmith install using the Helm chart, then make your first gateway call.

> [!NOTE]
>
> The LLM Gateway is in [beta](../../../Cloud/Reference/Release%20stages.md).

The LLM Gateway (the `agent-gateway` service) proxies model calls from agents and coding agents to upstream LLM providers. The gateway applies policies at granular scopes for reliability, spend limits, and redaction of PII and secrets. You can also route your LangSmith deployment's model calls through the gateway.

This guide enables it on a self-hosted Kubernetes install using the Helm chart. For the SaaS equivalent, see [LLM Gateway](../../../../LLM%20Gateway/Get%20started/LLM%20Gateway.md).

> [!NOTE]
>
> Enabling the gateway requires Helm chart version 0.17.1 or later, which ships LangSmith version 0.17.30.

> [!NOTE]
>
> The [Spend Monitoring dashboard](../../../../LLM%20Gateway/Observability/Monitor%20LLM%20Gateway%20spend.md) is available with SmithDB, but not ClickHouse.

## Enable the gateway

**1. Add Helm values**

> [!NOTE]
>
> The `agent-gateway` service requires access to Postgres and Redis, and network access to other LangSmith pods, similar to `backend` and `platform-backend`. You may need to configure network policies, Kubernetes service accounts, and pod annotations to enable this access.

Add these values to your Helm values file:

```yaml
agentGateway:
  enabled: true

  # Defaults shown for reference—override only if you have a reason.
  # containerPort: 8083
  # deployment:
  #   replicas: 1
  #   resources:
  #     limits:   { cpu: 2, memory: 2Gi }
  #     requests: { cpu: 1, memory: 1Gi }
  # autoscaling:
  #   enabled: true
  #   minReplicas: 1
  #   maxReplicas: 5
  #   targetCPUUtilizationPercentage: 50
  #   targetMemoryUtilizationPercentage: 70
  # service:
  #   type: ClusterIP
  #   port: 8083
```

Autoscaling is enabled by default. With the default resources, each replica handled \~100 concurrent streams on N2 instances or similar in testing, with prompts from \~40 to \~7,500 tokens.

**2. Apply and verify**

Apply the chart with chart version 0.17.1 or later. See [Upgrade an installation](../../Manage%20an%20instance/Upgrade%20an%20installation.md) for additional instructions.

```bash
helm search repo langchain/langsmith --versions

helm upgrade --install langsmith langchain/langsmith \
  --version <chart-version> \
  -f values.yaml --timeout=20m
```

Verify the deployment is healthy. The Deployment is named `<release-fullname>-agent-gateway`, which is `langsmith-agent-gateway` for a release named `langsmith`:

```bash
kubectl get deploy langsmith-agent-gateway
kubectl rollout status deploy/langsmith-agent-gateway
```

`agentGateway.enabled: true` turns the gateway on for every organization on the install. There is no separate enable step in the UI.

## Enable Presidio PII detection (optional)

[Presidio Analyzer](https://microsoft.github.io/presidio/) is a Microsoft-maintained NER service the gateway can call to detect PII in prompts before they reach upstream providers.

```yaml
presidioAnalyzer:
  enabled: true
```

When enabled, the chart injects `PRESIDIO_ANALYZER_URL` into the gateway pod so it discovers the analyzer in-cluster. No further app configuration is required.

## Expose the gateway externally

The gateway uses the same Ingress as the LangSmith UI and API. If `ingress.enabled=true` is already set in your Helm values, the gateway becomes reachable at `https://<your-hostname>/gateway/` as soon as you set `agentGateway.enabled=true`. No separate Ingress, LoadBalancer, or DNS record is required. If you set `config.basePath`, the route moves to `https://<your-hostname>/<basePath>/gateway/`, and every gateway URL on this page needs the same prefix.

Check from any host that can reach your Ingress:

```bash
curl -sS -o /dev/null -w '%{http_code}\n' https://<your-hostname>/gateway/health
# Expected: 200
```

The chart does not create a dedicated Ingress for `langsmith-agent-gateway`, and the Service is `ClusterIP` by default. Exposing port `8083` directly (through a separate Ingress, `service.type: LoadBalancer`, or `hostNetwork`) is supported by the chart's service block (`agentGateway.service.type`, `loadBalancerIP`, `loadBalancerSourceRanges`), but it is not the intended path. Use the frontend `/gateway/` route unless you have a specific reason not to.

## Roll back

Disabling the gateway removes the Deployment and Service and disables gateway features in the UI. Model calls routed to the gateway fail.

```yaml
agentGateway:
  enabled: false
```

## Make your first call

This mirrors the [Cloud first request guide](../../../../LLM%20Gateway/Get%20started/Send%20your%20first%20LLM%20Gateway%20request.md) with the base URL adjusted for self-hosted. Complete the steps above (gateway deployed, Ingress up) before continuing.

> [!NOTE]
>
> Before your first call, [add a provider key](../../../../LLM%20Gateway/Authentication/Provider%20authentication.md#add-a-provider-key) as a secret in each workspace that calls that provider, grant users a role with the `gateway:invoke` and `workspaces:read` [permissions](../../../Govern/Users%20%26%20access%20control/Organization%20and%20workspace%20operations%20reference.md), and [distribute a workspace-scoped API key](../../../../LLM%20Gateway/Authentication/Authenticate%20to%20the%20LLM%20Gateway.md#use-a-workspace-scoped-key). See [Set up the LLM Gateway](../../../../LLM%20Gateway/Get%20started/Set%20up%20the%20LLM%20Gateway.md).

**1. Set environment variables**

```bash
# Replace with your Ingress hostname.
export LANGSMITH_GATEWAY_BASE_URL="https://<your-hostname>/gateway/v1"
export LANGSMITH_API_KEY="lsv2_..."
```

For LangChain and Deep Agents, the convenience variables work the same way as the SaaS docs describe: they append `/openai/v1` to whatever you set if you're using OpenAI models.

```bash
export LANGSMITH_GATEWAY="https://<your-hostname>/gateway"
export LANGSMITH_GATEWAY_API_KEY="<SECRET>"
```

**2. Make a call**

Either header works: `Authorization: Bearer <key>` or `X-Api-Key: <key>`. The examples below use the `Authorization` header.

```bash cURL
curl "$LANGSMITH_GATEWAY_BASE_URL/chat/completions" \
    -H "Authorization: Bearer $LANGSMITH_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"openai/gpt-5.4-mini","messages":[{"role":"user","content":"ping"}]}'
```

```python Python (OpenAI SDK)
import os

from openai import OpenAI

client = OpenAI(
    base_url=os.environ["LANGSMITH_GATEWAY_BASE_URL"],
    api_key=os.environ["LANGSMITH_API_KEY"],
)
response = client.chat.completions.create(
    model="openai/gpt-5.4-mini",
    messages=[{"role": "user", "content": "ping"}],
)
print(response.choices[0].message.content)
```

```typescript TypeScript (OpenAI SDK)
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: process.env.LANGSMITH_GATEWAY_BASE_URL,
  apiKey: process.env.LANGSMITH_API_KEY,
});
const response = await client.chat.completions.create({
  model: "openai/gpt-5.4-mini",
  messages: [{ role: "user", content: "ping" }],
});
console.log(response.choices[0].message.content);
```

```python Python (LangChain)
import os

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

model = init_chat_model(
    model="openai/gpt-5.4-mini",
    model_provider="openai",
    base_url=os.environ["LANGSMITH_GATEWAY_BASE_URL"],
    api_key=os.environ["LANGSMITH_API_KEY"],
)
agent = create_agent(model=model, system_prompt="You are a helpful assistant.")
result = agent.invoke({"messages": [{"role": "user", "content": "ping"}]})
print(result["messages"][-1].content)
```

A `200` confirms the gateway, API key, and provider secret are all wired correctly.

**3. View the trace**

In the LangSmith UI, go to the tracing project named `gateway` in the workspace tied to your API key. Every call routed through the gateway appears there with input, output, latency, and token usage, if tracing contents are enabled.

**4. Set a spend policy (optional)**

Go to **LLM Gateway** and select **Cost Controls** to cap spend per workspace or per API key. Once a request exceeds the cap, the gateway returns a `402` with a message naming the policies that blocked the request:

```json
{"type": "error", "error": {"message": "request blocked by gateway policies: R&D Spend Cap"}}
```

For the full guide, see [Spend policies](../../../../LLM%20Gateway/Governance/Spend%20policies.md).

## Troubleshooting

* **Gateway pod `CrashLoopBackOff` immediately after upgrade**: Check `kubectl logs deploy/langsmith-agent-gateway`.
* **Model calls fail with connection refused or timeout to `agent-gateway`**: Verify the gateway pod is `Running` and that no NetworkPolicy in your cluster blocks port `8083` between pods in the LangSmith namespace.

## Security notes

* The gateway makes outbound HTTP calls to provider LLM endpoints. Any custom provider URLs you configure must be validated against your egress policy; the service uses LangSmith's SSRF-protection library for custom and configured provider URLs. Built-in providers resolve to fixed, provider-owned hostnames and aren't a user-controlled-URL path.
* External clients should reach the gateway through the frontend's `/gateway/` path so requests inherit the same TLS termination, auth, and rate limiting as the rest of the LangSmith API. Creating a second Ingress or LoadBalancer directly to port `8083` bypasses those controls.
* `AGENT_GATEWAY_URL` is derived from the Helm release fullname and the chart's `agentGateway.name`, `agentGateway.service.port`, `namespace`, and `clusterDomain` values. Overriding any of those on an existing install requires a rolling restart of every pod that reads the value.

## Next steps

* [Set up the LLM Gateway](../../../../LLM%20Gateway/Get%20started/Set%20up%20the%20LLM%20Gateway.md): connect providers, grant users gateway access, and configure policies for your organization.
* [How the LLM Gateway works](../../../../LLM%20Gateway/Get%20started/How%20the%20LLM%20Gateway%20works.md): follow a request through the gateway, including self-hosted base URLs.
* [Authenticate to the LLM Gateway](../../../../LLM%20Gateway/Authentication/Authenticate%20to%20the%20LLM%20Gateway.md): choose and send the API key that callers use.
