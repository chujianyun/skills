# Configure model providers for Engine on self-hosted and BYOC

> Choose the model providers LangSmith Engine uses on a self-hosted LangSmith instance, authenticate with credentials or cloud identity, and keep model traffic on private networking.

> [!NOTE]
>
> Running Engine on your own model providers requires LangSmith Helm chart `0.17.0` or later. Earlier chart versions run Engine only on [LangSmith Intelligence](LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md#langsmith-intelligence).

On self-hosted LangSmith, an Organization Admin chooses where [LangSmith Engine](../LangSmith%20Engine.md) runs its model calls: on LangSmith Intelligence (LSI), on your own model providers, or both. Running Engine on your own providers keeps prompts and responses under your agreements with those providers. This page covers how to select providers, authenticate to them, and connect to them or to LSI over private networking. For a comparison of the two options, see [Choose how Engine runs its models](LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md#choose-how-engine-runs-its-models). Complete [Install Engine](LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md#install-engine) first.

> [!NOTE]
>
> On [BYOC](LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md#engine-on-byoc), LangSmith Intelligence is not available, and Engine runs only on your own model providers. Amazon Bedrock can use your data plane's cloud identity, which LangChain configures. The [cloud identity](#use-cloud-identity-for-your-model-providers) and [private connection](#connect-privately) sections apply to self-hosted LangSmith only.

## Use your own model providers

Engine calls your providers directly from your cluster. Prompts and responses go only to your provider, under your agreement with that provider. LangChain does not receive them.

Sandbox usage by Engine is included in Engine's LSU billing. The sandboxes Engine uses to diagnose issues, generate fixes, and write evaluators do not incur additional Sandboxes product charges.

Engine supports Anthropic, OpenAI, Amazon Bedrock, Google Vertex AI, and Azure AI Foundry, and can also call Claude and GPT through [your own model gateway](#use-a-model-gateway). It uses a mix of models from the providers you select, so for the best results, add credentials for every provider you have access to.

Enable access to Anthropic's Claude models and OpenAI's GPT models in your provider accounts, where your provider offers them. On Azure, use an Azure AI Foundry resource. To confirm that Engine can reach the models it uses, run [**Test connection**](#test-a-provider).

## Choose model providers

Under **Settings > Engine > Model providers**, an Organization Admin selects LangSmith Intelligence, one or more of your own providers, or both. Credentials are saved as organization secrets and apply to every workspace in the organization.

LangSmith Intelligence appears only when your installation's `engine.intelligenceBaseUrl` serves Engine's models.

When LangSmith Intelligence is available and selected, it takes priority over your selected providers. Leave it unselected to keep inference on your own providers.

Engine selects models from the providers you enable. Enable access to Claude 5.5-class models or GPT 5.6-class models in your provider accounts, depending on which models each provider offers. Model requirements follow the Engine image tag in `images.engineInsightsAgentImage.tag`, not the Helm chart version. Run [**Test connection**](#test-a-provider) to identify the required models and confirm access for your installed Engine image.

To use your own providers:

**1. Add credentials**

Click **Add credentials** next to the provider and enter:

> [tab] Anthropic
>
> An Anthropic API key.

> [tab] Amazon Bedrock
>
> An AWS access key ID and secret access key, with an optional session token, or a Bedrock API key (bearer token). Optionally, an AWS region.
>
> Engine uses the Bedrock Mantle API. To use Bedrock Runtime instead, see [Use Bedrock Runtime](#use-bedrock-runtime).
>
> Enable access to the required models in the selected AWS account and region. Grant the calling identity Mantle inference and model-subscription permissions. See [AmazonBedrockMantleInferenceAccess](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonBedrockMantleInferenceAccess.html) for the required actions.
>
> If no region is saved, Engine uses `us-east-1`, including with workload identity. It does not inherit the EKS cluster's region.
>
> To use the cloud identity of Engine's pods instead, see [Use cloud identity for your model providers](#use-cloud-identity-for-your-model-providers).

> [tab] Google Vertex AI
>
> A service account key in JSON format. Engine uses the JSON's `project_id` as the inference project and calls the `global` location.
>
> Enable the required models through [Model Garden](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/use-partner-models) in that project. Grant the service account `roles/aiplatform.user` in the same project.
>
> To use the cloud identity of Engine's pods instead, see [Use cloud identity for your model providers](#use-cloud-identity-for-your-model-providers).

> [tab] Azure AI Foundry
>
> Confirm that your resource region has access and quota for the models required by your installed Engine image. To configure Azure:
>
> 1. Create the required model deployments in the same Azure AI Foundry resource. Deployment names must exactly match the model names (model IDs). Engine uses Claude as its primary model and GPT as its fallback. Custom deployment aliases are not supported for either model family.
>
>    Follow the [Claude deployment instructions](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry) and check [Azure OpenAI model availability](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/responses). Accept the Azure Marketplace terms when creating your first Claude deployment.
> 2. Enter an API key and the resource name, not its full URL. To use the cloud identity of Engine's pods instead of an API key, see [Use cloud identity for your model providers](#use-cloud-identity-for-your-model-providers).
> 3. Run [**Test connection**](#test-a-provider) and confirm that both Claude and GPT requests succeed, including when selecting additional providers. After saving, [start an Engine analysis](LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md#verify-the-installation) to verify the complete setup.

> [tab] OpenAI
>
> An OpenAI API key, and optionally your OpenAI organization ID.

A provider with complete credentials shows as configured. To change them later, click the key icon next to the provider.

**2. Test the provider**

Click **Test connection**. Engine sends a small request to each model it uses on that provider, with the saved credentials or configured cloud identity. It shows whether each request succeeded and, if not, why.

**3. Select providers and save**

Select the providers Engine may use, then save.

If Engine runs fail after you save:

* **No provider selected:** Engine does not start runs until at least one provider is selected and saved.
* **Rejected credentials:** **Test connection** reports which provider rejected them. Update the credentials and test again.
* **Model not available:** enable the model in your provider account, then test again.

## Use Bedrock Runtime

To have Engine call Amazon Bedrock Runtime instead of Mantle, set two environment variables on both Engine workloads:

```yaml
engineInsightsAgent:
  apiServer:
    deployment:
      extraEnv:
        - name: ENGINE_BEDROCK_API
          value: "runtime"
        - name: ENGINE_BEDROCK_INFERENCE_PROFILE
          value: "<system-inference-profile-id>"
  queue:
    deployment:
      extraEnv:
        - name: ENGINE_BEDROCK_API
          value: "runtime"
        - name: ENGINE_BEDROCK_INFERENCE_PROFILE
          value: "<system-inference-profile-id>"
```

Set `ENGINE_BEDROCK_INFERENCE_PROFILE` to a system inference profile ID for Engine's Claude model, such as `us.anthropic.<model-id>`. Supported prefixes are `us.`, `eu.`, `apac.`, and `global.`. Profile ARNs and application inference profiles are not supported.

Grant the calling identity Bedrock Runtime access to that profile. Then apply the Helm values, restart both deployments, and run [**Test connection**](#test-a-provider). If an Engine upgrade changes its Claude model, update the profile ID.

On BYOC, contact LangChain to make this change.

## Use cloud identity for your model providers

Instead of saving credentials, Amazon Bedrock, Google Vertex AI, and Azure AI Foundry can authenticate with the cloud identity of Engine's pods instead of credentials saved in LangSmith. List those providers in `engine.workloadIdentityProviders`. Configure identity for both the API server and queue of the shared Engine and Insights deployment:

> [tab] Amazon EKS
>
> Configure IAM roles for service accounts (IRSA). Trust the namespace and service account of both Engine workloads, and grant the role access to the Bedrock models Engine uses.
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> engine:
>   workloadIdentityProviders:
>     - bedrock
>
> engineInsightsAgent:
>   apiServer:
>     serviceAccount:
>       annotations:
>         eks.amazonaws.com/role-arn: "arn:aws:iam::<account-id>:role/<engine-model-access-role>"
>   queue:
>     serviceAccount:
>       annotations:
>         eks.amazonaws.com/role-arn: "arn:aws:iam::<account-id>:role/<engine-model-access-role>"
> ```

> [tab] Google GKE
>
> Enable Workload Identity Federation for GKE on the cluster and the node pools that run Engine. Grant each Engine Kubernetes service account `roles/iam.workloadIdentityUser` on the Google service account. Bind each member as `serviceAccount:<cluster-project-id>.svc.id.goog[<namespace>/<kubernetes-service-account>]`.
>
> Grant the Google service account Vertex AI inference permissions, such as `roles/aiplatform.user`, in the project that hosts the models. Enable the required models in that project.
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> engine:
>   workloadIdentityProviders:
>     - vertex
>
> engineInsightsAgent:
>   apiServer:
>     serviceAccount:
>       annotations:
>         iam.gke.io/gcp-service-account: "<service-account>@<project-id>.iam.gserviceaccount.com"
>     deployment:
>       extraEnv:
>         - name: GOOGLE_CLOUD_PROJECT
>           value: "<vertex-project-id>"
>   queue:
>     serviceAccount:
>       annotations:
>         iam.gke.io/gcp-service-account: "<service-account>@<project-id>.iam.gserviceaccount.com"
>     deployment:
>       extraEnv:
>         - name: GOOGLE_CLOUD_PROJECT
>           value: "<vertex-project-id>"
> ```
>
> Engine uses Application Default Credentials (ADC) to resolve the identity and project. Set `GOOGLE_CLOUD_PROJECT` on both workloads to the intended Vertex AI project. Engine currently uses the `global` Vertex AI location, so the required models must be available there.

> [tab] Azure AKS
>
> Enable the AKS OIDC issuer and Microsoft Entra Workload ID. Create a federated identity credential for each Engine Kubernetes service account on your managed identity. Use the cluster's OIDC issuer, audience `api://AzureADTokenExchange`, and subject `system:serviceaccount:<namespace>:<kubernetes-service-account>` for each.
>
> Grant the identity the Cognitive Services User role, scoped to the Azure AI Foundry resource that hosts Engine's models. An Azure OpenAI role alone does not establish access to Claude models.
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> engine:
>   workloadIdentityProviders:
>     - azure
>
> engineInsightsAgent:
>   apiServer:
>     serviceAccount:
>       annotations:
>         azure.workload.identity/client-id: "<managed-identity-client-id>"
>     deployment:
>       labels:
>         azure.workload.identity/use: "true"
>   queue:
>     serviceAccount:
>       annotations:
>         azure.workload.identity/client-id: "<managed-identity-client-id>"
>     deployment:
>       labels:
>         azure.workload.identity/use: "true"
> ```
>
> Both workloads need the service account annotation and pod label. Save the Foundry resource name under **Settings > Engine > Model providers**.

> [!WARNING]
>
> A provider listed in `engine.workloadIdentityProviders` counts as configured without saved credentials, so any Organization Admin can select it. Scope the identity to the models Engine uses.

Saved credentials take precedence over cloud identity. When switching a provider, apply the cloud identity configuration before removing its saved credentials. Then remove only that provider's saved API keys or service account JSON under **Settings > Engine > Model providers**. For Bedrock, also remove any saved access key, secret access key, and session token. Keep the Azure AI Foundry resource name and any Bedrock region setting, then [test the provider](#test-a-provider) again.

## Use a model gateway

If your organization routes model traffic through its own LLM gateway, Engine can send its Claude and GPT calls through it instead of calling providers directly. The gateway appears under **Settings > Engine > Model providers** as **Model gateway**.

> [!NOTE]
>
> Model gateway support requires LangSmith Helm chart `0.17.31` or later.

Whoever installs LangSmith configures the gateway in the Helm values, not in the UI. Gateway URLs are often private addresses, so an organization setting would let any Organization Admin point Engine at internal services. On [BYOC](LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md#engine-on-byoc) data planes on AWS, LangChain configures the gateway for you. See [Use a gateway on BYOC](#use-a-gateway-on-byoc).

### Gateway requirements

Your gateway must:

* **Serve the Anthropic Messages API for Claude, the OpenAI Responses API for GPT, or both.** Engine runs on either model family. For the best results, serve both.
* **Forward the `anthropic-beta` header and the request body unchanged.** Engine's Claude requests use a beta feature, and Anthropic can reject them without it.
* **Return token usage on every response.** Engine fails a call whose response has no usage.
* **Accept the provider model IDs Engine requests.** If your gateway maps them to its own deployments, keep the response's model the same model family.
* **Set the base URL to the gateway's final address.** Engine doesn't follow redirects, so a base URL that redirects, for example from `http` to `https`, fails every call.

Engine sends only the model request. With API key authentication, it does not send organization, workspace, or project identifiers to the gateway.

### Configure the gateway

**1. Declare the APIs your gateway serves**

Tell LangSmith which APIs the gateway serves. LangSmith shows **Model gateway** only when this is set:

```yaml
commonEnv:
  - name: ENGINE_GATEWAY_APIS
    value: '["anthropic","openai"]'
```

List only the APIs your gateway serves: `anthropic`, `openai`, or both.

**2. Point Engine at the gateway**

Set the gateway's base URLs on both Engine workloads. Engine appends the API path to each URL:

* `ENGINE_GATEWAY_ANTHROPIC_BASE_URL`: the URL an Anthropic SDK client would use as its base URL. Engine calls `<base URL>/v1/messages`.
* `ENGINE_GATEWAY_OPENAI_BASE_URL`: the URL an OpenAI SDK client would use, usually ending in `/v1`. Engine calls `<base URL>/responses`.

Set only the URLs for the APIs you listed in `ENGINE_GATEWAY_APIS`. The URLs must use HTTPS. To trust a private certificate authority, see [Mount internal CAs for TLS](../../LangSmith%20setup/Self-hosted/Platform%20auth%20%26%20access%20control/Configure%20custom%20TLS%20certificates.md#mount-internal-cas-for-tls). For a plain-HTTP address inside your cluster, also set `ENGINE_GATEWAY_ALLOW_INSECURE_HTTP` to `"true"`.

**3. Configure authentication**

Choose how Engine authenticates to the gateway:

> [tab] API key
>
> Store the gateway key in a Kubernetes secret and mount it into both Engine workloads. Set `ENGINE_GATEWAY_API_KEY_FILE` to the mounted file's path.
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> engineInsightsAgent:
>   apiServer:
>     deployment:
>       extraEnv:
>         - name: ENGINE_GATEWAY_ANTHROPIC_BASE_URL
>           value: "https://<gateway-host>/anthropic"
>         - name: ENGINE_GATEWAY_OPENAI_BASE_URL
>           value: "https://<gateway-host>/openai/v1"
>         - name: ENGINE_GATEWAY_API_KEY_FILE
>           value: "/etc/engine-gateway/api-key"
>       volumes:
>         - name: engine-gateway
>           secret:
>             secretName: engine-model-gateway
>       volumeMounts:
>         - name: engine-gateway
>           mountPath: /etc/engine-gateway
>           readOnly: true
>   queue:
>     deployment:
>       # The same extraEnv, volumes, and volumeMounts as apiServer.
> ```
>
> By default, Engine sends the key as `Authorization: Bearer <key>`. If your gateway expects the key in another header, set `ENGINE_GATEWAY_AUTH_HEADER` to that header's name, such as `x-api-key`. Engine then sends the key as the header's value.
>
> To send additional headers, mount a directory with one file per header and set `ENGINE_GATEWAY_HEADERS_DIR` to its path. Each file's name is the header name, and its contents are the value. Engine reserves `host`, `content-length`, `content-type`, `transfer-encoding`, `connection`, and headers that start with `x-langsmith-`.
>
> Engine reads the key and header files at the start of each run, so you can rotate them without restarting Engine.

> [tab] LLM auth proxy
>
> If your gateway sits behind the [LLM auth proxy](../../LangSmith%20setup/Self-hosted/Configure%20an%20instance/Set%20up%20the%20LLM%20auth%20proxy.md), Engine can authenticate with short-lived LangSmith tokens instead of a static key. See [Use the LLM auth proxy](#use-the-llm-auth-proxy).

Apply the Helm values and restart both Engine workloads so they pick up the new environment variables.

**4. Test and select the gateway**

Under **Settings > Engine > Model providers**, click **Test connection** next to **Model gateway**. Engine sends a small request through the gateway for each API you configured and shows whether each one succeeded. If the gateway rejects a request, the result includes the gateway's error message. Then select **Model gateway** and save.

### Use the LLM auth proxy

With the LLM auth proxy, Engine never holds a gateway key. The proxy validates a token that LangSmith signs, and your proxy configuration adds the gateway's credentials.

For each run, Engine requests a token from your LangSmith installation and sends it in the `X-LangSmith-LLM-Auth` header on every model call. Tokens are valid for five minutes, and Engine requests a new one before the current token expires. **Test connection** uses the same flow.

To set it up:

1. Complete steps 1 through 4 of [Set up the LLM auth proxy](../../LangSmith%20setup/Self-hosted/Configure%20an%20instance/Set%20up%20the%20LLM%20auth%20proxy.md): configure JWT signing and the issuer, enable the proxy for your organization, set the JWT audience, and install the auth proxy chart with your gateway as its upstream.
2. On both Engine workloads, set `ENGINE_GATEWAY_AUTH` to `llm_auth_proxy`, and point the base URLs at the auth proxy service instead of the gateway. Don't set `ENGINE_GATEWAY_API_KEY_FILE`: Engine fails its runs when both are set.

   The proxy appends each request's path to the chart's `authProxy.upstream` URL, so keep the path each API has on your gateway. For example, with `authProxy.upstream` set to `https://gateway.example.com` and the gateway serving the Anthropic API at `https://gateway.example.com/anthropic`, set `ENGINE_GATEWAY_ANTHROPIC_BASE_URL` to the proxy's address followed by `/anthropic`. The chart names the service `<release>-auth-proxy` and listens on port `10000` by default (`authProxy.service.port`).

   ```yaml
   engineInsightsAgent:
     apiServer:
       deployment:
         extraEnv:
           - name: ENGINE_GATEWAY_AUTH
             value: "llm_auth_proxy"
           - name: ENGINE_GATEWAY_ANTHROPIC_BASE_URL
             value: "http://<auth-proxy-service>.<namespace>.svc.cluster.local:10000/anthropic"
           - name: ENGINE_GATEWAY_OPENAI_BASE_URL
             value: "http://<auth-proxy-service>.<namespace>.svc.cluster.local:10000/openai/v1"
           - name: ENGINE_GATEWAY_ALLOW_INSECURE_HTTP
             value: "true"
     queue:
       deployment:
         # The same extraEnv as apiServer.
   ```

   `ENGINE_GATEWAY_ALLOW_INSECURE_HTTP` is needed only when Engine reaches the auth proxy over plain HTTP inside your cluster.
3. If your organization's **Allowed URLs** setting is **Custom**, add the auth proxy's hostname to the list.

Engine runs on a schedule, not as a signed-in user. Its tokens identify the organization and workspace, with `actor_type` set to `api_key:service`, and they do not include an IdP token. If your `ext_authz` or `ext_proc` service exchanges a user's IdP token for gateway credentials, handle Engine's requests separately, for example by mapping the workspace to gateway credentials.

If Engine reports that the LLM auth proxy is not enabled for the organization, or that the organization has no JWT audience, complete [Configure organization settings in LangSmith](../../LangSmith%20setup/Self-hosted/Configure%20an%20instance/Set%20up%20the%20LLM%20auth%20proxy.md#3-configure-organization-settings-in-langsmith).

### Use a gateway on BYOC

On [BYOC](LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md#engine-on-byoc) data planes on AWS, LangChain configures the gateway, so you don't edit Helm values. Model gateways are not yet available on BYOC data planes on Azure or Google Cloud.

1. Check that your gateway meets the [gateway requirements](#gateway-requirements) and that your data plane can reach it.

2. Choose how Engine authenticates to the gateway:

   * **API key**: Store the gateway key in AWS Secrets Manager, in the AWS account and region that host your data plane. The secret's name must start with `langsmith/`, because your data plane can read only secrets with that prefix. Store the key as a plain string, or as a field of a JSON secret. Encrypt the secret with the default `aws/secretsmanager` key. If you use your own KMS key instead, ask LangChain which role to allow in its key policy.
   * **LLM auth proxy**: Install the [LLM auth proxy](../../LangSmith%20setup/Self-hosted/Configure%20an%20instance/Set%20up%20the%20LLM%20auth%20proxy.md) where your data plane can reach it, and complete its organization settings. Set the proxy's `jwksUri` to `https://<data-plane-host>/api/.well-known/jwks.json`. Your data plane signs the tokens Engine sends with its own key, and this URL publishes that key.

3. Contact LangChain with:
   * The APIs your gateway serves: Anthropic, OpenAI, or both.
   * The base URL for each API, as described in [Configure the gateway](#configure-the-gateway). For the LLM auth proxy, give the proxy's URLs instead.
   * The authentication method. For an API key, include the secret's ARN, the JSON field that holds the key if the secret is JSON, and the header name if your gateway doesn't expect `Authorization: Bearer <key>`.

4. After LangChain confirms the change, [test and select the gateway](#configure-the-gateway) under **Settings > Engine > Model providers**.

If the key can't be read, for example because the secret was deleted or its KMS key doesn't allow LangSmith, **Test connection** fails for the gateway. Engine's other providers and the rest of LangSmith keep working.

## Connect privately

Engine works over public egress. To keep its traffic on private networking, connect to LangSmith Intelligence with AWS PrivateLink, or connect to your own model providers through your cloud's private endpoints.

### Connect with AWS PrivateLink

The LangSmith Intelligence gateway, `beacon.aws.langchain.com`, routes requests to Amazon Bedrock in LangChain's AWS environment.

Before configuring PrivateLink, complete [Install Engine](LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md#install-engine), including its Helm and egress configuration.

[AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/) routes Engine traffic from your VPC to LSI without exposing that traffic to the public internet. The LSI endpoint service is hosted in `us-east-2`, and AWS supports access from VPCs in other regions.

Before you begin, collect your AWS account ID, VPC ID, private subnet IDs, and a security group for the interface endpoint. Configure that endpoint security group to allow inbound TCP traffic on port 443 only from the security group attached to the nodes or workloads that run Engine, or from the smallest private CIDR that contains them. Do not allow `0.0.0.0/0`.

To connect your VPC to LSI:

**1. Request access**

Contact your account representative or [sales@langchain.dev](mailto:sales@langchain.dev) with your AWS account ID. LangChain adds your account to the endpoint service's allowed principals list.

**2. Create the interface VPC endpoint**

Configure the AWS provider for the region that contains your VPC. Keep `service_region` set to `us-east-2`, including when your VPC is in another region. Select one private subnet per availability zone.

> [!NOTE]
>
> The `service_region` argument requires HashiCorp AWS provider `5.82.0` or later.

```hcl
resource "aws_vpc_endpoint" "langsmith_intelligence" {
  vpc_id              = var.vpc_id
  service_name        = "com.amazonaws.vpce.us-east-2.vpce-svc-054f37092752bff6b"
  service_region      = "us-east-2"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = var.private_subnet_ids
  security_group_ids  = [var.security_group_id]
  private_dns_enabled = false
}
```

**3. Wait for LangChain to accept the connection**

The endpoint status changes from `pendingAcceptance` to `available` after LangChain accepts the connection. Allow a few minutes for the change to propagate before testing connectivity.

**4. Route the LSI hostname to the endpoint**

Enable DNS resolution and DNS hostnames for your VPC. Then, create a Route 53 private hosted zone and alias record so `beacon.aws.langchain.com` resolves to the VPC endpoint inside your VPC. Keep this hostname unchanged so TLS certificate validation succeeds. The private hosted zone also prevents fallback to public DNS when the endpoint is unavailable.

```hcl
resource "aws_route53_zone" "langsmith_intelligence" {
  name = "beacon.aws.langchain.com"

  vpc {
    vpc_id = var.vpc_id
  }
}

resource "aws_route53_record" "langsmith_intelligence" {
  zone_id = aws_route53_zone.langsmith_intelligence.zone_id
  name    = "beacon.aws.langchain.com"
  type    = "A"

  alias {
    name                   = aws_vpc_endpoint.langsmith_intelligence.dns_entry[0].dns_name
    zone_id                = aws_vpc_endpoint.langsmith_intelligence.dns_entry[0].hosted_zone_id
    evaluate_target_health = true
  }
}
```

If workloads use a corporate DNS resolver instead of the Amazon-provided resolver, configure conditional forwarding to Route 53 Resolver or create an equivalent private DNS override for `beacon.aws.langchain.com` that points to the endpoint DNS name.

**5. Verify private connectivity**

From a node or container that runs Engine, resolve the gateway hostname:

```bash
getent ahostsv4 beacon.aws.langchain.com
```

Confirm that the result contains the private IP addresses assigned to the endpoint network interfaces. Then start an analysis and confirm that it completes successfully. If the analysis does not complete, review the Engine installation and egress configuration.

### Connect to your providers privately

Engine calls each provider's standard API hostname from the `standalone-insights` pods. To keep that traffic off the public internet, set up your cloud's private connection to the provider so the same hostname resolves to private addresses inside your network:

| **Provider** | **Hostname Engine calls** | **Private connection** |
| - | - | - |
| Amazon Bedrock (Mantle) | `bedrock-mantle.<region>.api.aws` | An interface VPC endpoint for `com.amazonaws.<region>.bedrock-mantle`, with private DNS enabled or a Route 53 private hosted zone for the hostname |
| Amazon Bedrock (Runtime) | `bedrock-runtime.<region>.amazonaws.com` | An interface VPC endpoint for `com.amazonaws.<region>.bedrock-runtime`, with private DNS enabled |
| Google Vertex AI | `<region>-aiplatform.googleapis.com`, or `aiplatform.googleapis.com` for the global region | Private Service Connect for Google APIs, with private DNS for `googleapis.com` |
| Azure AI Foundry | `<resource>.openai.azure.com` and `<resource>.services.ai.azure.com` | A private endpoint for the Foundry resource, with its private DNS zones |
| Anthropic, OpenAI | `api.anthropic.com`, `api.openai.com` | Not available. These providers need public egress, unless you route them through a [model gateway](#use-a-model-gateway). |

Engine does not accept custom endpoint URLs for these providers, so private connectivity works through DNS: the standard hostname must resolve to your private endpoint from the Engine pods. To send model traffic to an address you choose, use a [model gateway](#use-a-model-gateway).

If Engine authenticates with [cloud identity](#use-cloud-identity-for-your-model-providers), the pods also need to reach your cloud's token service, such as an interface VPC endpoint for AWS STS on AWS.

With saved Vertex AI service account JSON, also allow HTTPS to `oauth2.googleapis.com` for token exchange, alongside `aiplatform.googleapis.com` for inference.

Usage reporting to LangSmith Intelligence is a separate connection. On AWS, `https://beacon.aws.langchain.com/intelligence` records usage and supports [AWS PrivateLink](#connect-with-aws-privatelink), so an installation can run Engine on Bedrock and report usage without public egress. The default `https://beacon.langchain.com/intelligence` needs public egress.

## See also

* [Engine on self-hosted](LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md): Install Engine and choose how it runs its models.
* [Engine security](../LangSmith%20Engine%20security.md#model-subprocessors): Model subprocessor controls.
* [Configure egress](../../LangSmith%20setup/Self-hosted/Configure%20an%20instance/Egress%20for%20billing%20and%20operational%20telemetry.md): Other outbound traffic from self-hosted LangSmith.
