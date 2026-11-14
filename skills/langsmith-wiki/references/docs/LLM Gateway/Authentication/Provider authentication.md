# Provider authentication

> Choose how the LLM Gateway authenticates to each model provider, add provider keys as workspace secrets, and fix provider credential errors.

> [!NOTE]
>
> The LLM Gateway is in [beta](../../LangSmith%20setup/Cloud/Reference/Release%20stages.md).

Provider authentication is the credential the [LLM Gateway](../Get%20started/LLM%20Gateway.md) uses to call a model provider on your behalf. Because LangSmith holds that credential, developers and agents never need a copy of a provider key.

Each gateway request passes through two layers of authentication:

* The caller [authenticates to the gateway](Authenticate%20to%20the%20LLM%20Gateway.md) with a LangSmith API key.
* The gateway then authenticates to the provider with one of the credential sources discussed on this page.

## Choose a credential source

Each request uses one of these credential sources. Each source has a different billing owner:

| Source | Who holds the credential | Who bills the call | Set up |
| - | - | - | - |
| Your provider key | LangSmith, as a workspace secret | The provider, on your account | [Add a provider key](#add-a-provider-key) |
| [Model configuration](../Models%20and%20reliability/Custom%20model%20configurations.md) (`custom/<name>`) | LangSmith, as the secret the configuration names | The provider, on your account | Create the configuration |
| [Gateway Credits](../Models%20and%20reliability/Gateway%20Credits.md) | LangChain | LangSmith, on your LangSmith account | No provider credential |
| [Claude subscription](../Call%20the%20gateway/Set%20up%20coding%20agents.md#use-claude-subscription-oauth) | The user's Claude Code login, sent with each request | Anthropic, on the user's subscription | Claude Code only |

The gateway picks the source from the request:

* **Model ID**: a `<provider>/<model>` ID, such as `anthropic/claude-opus-5`, uses your provider key for that provider. A `custom/<name>` ID uses the configuration's secret. A hosted model ID listed on [Gateway Credits](../Models%20and%20reliability/Gateway%20Credits.md#available-models), such as `moonshotai/kimi-k3`, uses Gateway Credits.
* **Claude subscription**: when a request carries an Anthropic OAuth token, the gateway forwards it to Anthropic and does not load the workspace's `ANTHROPIC_API_KEY`.

## Add a provider key

The gateway reads provider keys from the secrets of the workspace that the caller's API key belongs to. Each workspace that calls a provider needs its own copy of that provider's key. For `<provider>/<model>` calls, the gateway does not fall back to organization secrets. Organization secrets apply only to [organization-scoped model configurations](../Models%20and%20reliability/Custom%20model%20configurations.md).

Adding a provider key requires [permission to manage secrets](../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#workspace-roles) in that workspace. Without it, the **Provider secrets** page hides the add button and asks you to contact a workspace admin.

To add a provider key:

1. In LangSmith, select the workspace that calls the provider.
2. Go to **Settings > Integrations > Provider secrets**.
3. Click **+ Secret**. Under **Provider**, select the provider, which fills in the secret name.
4. Enter the provider key as the value, and click **Save**.

If a workspace has no key for a provider, the Simulator marks that provider's models as **Needs key** and prompts for one before it runs a request. The key you enter there is saved as a secret in the current workspace, the same as the one added on the **Provider secrets** page.

LangSmith does not check a provider key when you save it. A wrong key shows up as the provider's error on the first request.

The gateway reads these secret names:

| Provider | Secret name |
| - | - |
| Anthropic | `ANTHROPIC_API_KEY` |
| AWS Bedrock | `AWS_IAM_ROLE_ARN`, access keys, or `AWS_BEARER_TOKEN_BEDROCK`. See [Configure Amazon Bedrock](#configure-amazon-bedrock). |
| Azure Foundry | `AZURE_FOUNDRY_API_KEY` and `AZURE_FOUNDRY_RESOURCE_NAME`. For Entra ID, see [Configure Azure Foundry](#configure-azure-foundry). |
| Baseten | `BASETEN_API_KEY` |
| Fireworks | `FIREWORKS_API_KEY` |
| Gemini Enterprise Agent Platform | `GOOGLE_VERTEX_AI_WEB_CREDENTIALS`. See [Configure Gemini Enterprise Agent Platform](#configure-gemini-enterprise-agent-platform). |
| Google Gemini | `GOOGLE_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| ScaleDown | `SCALEDOWN_API_KEY` |
| TypeSafe | `TYPESAFE_API_KEY` |
| xAI | `XAI_API_KEY` |

## Configure Amazon Bedrock

Amazon Bedrock supports three credential methods, which you set in the provider form:

| Method | Secrets | Notes |
| - | - | - |
| IAM role (recommended) | `AWS_IAM_ROLE_ARN` | The gateway assumes the role and uses short-lived credentials, so LangSmith stores no long-lived AWS secret. Available on LangSmith Cloud and on BYOC AWS data planes. |
| AWS credentials | `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`, plus `AWS_SESSION_TOKEN` for temporary credentials | Both keys are required. Temporary credentials stop working when they expire. |
| Bearer token | `AWS_BEARER_TOKEN_BEDROCK` | An [Amazon Bedrock API key](https://docs.aws.amazon.com/bedrock/latest/userguide/api-keys.html). |

On self-hosted LangSmith, the gateway can also use the AWS credentials of its own pod, such as an IAM role for the `agent-gateway` service account, when the workspace has no Bedrock secrets. Set the role annotation in `agentGateway.serviceAccount.annotations` in your Helm values.

If a workspace has secrets for more than one method, the gateway uses the first it finds in this order: bearer token, IAM role, AWS credentials, then, on self-hosted, the pod's credentials.

Every method also reads an optional `AWS_BEDROCK_REGION`, which defaults to `us-east-1`. Set it to a bare Region name, not a URL. When it is unset and the model ID is a [cross-Region inference profile](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html), such as one starting with `eu.`, the gateway uses a Region in that profile's geography.

### Use an IAM role

> [!NOTE]
>
> The IAM role method is not available on [self-hosted LangSmith](../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) or on BYOC GCP and Azure data planes. On self-hosted, give the gateway pod its own AWS credentials instead, as described in [Configure Amazon Bedrock](#configure-amazon-bedrock). On BYOC GCP and Azure data planes, use AWS credentials or a bearer token. On [BYOC](../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md) AWS data planes, the role needs the `LangSmithBedrock=true` tag and a different trust policy. See [IAM trusted entity on BYOC](../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Model%20providers.md#iam-trusted-entity-on-byoc).

On LangSmith Cloud, the `AWS_IAM_ROLE_ARN` secret set here is shared with the [Playground and LLM-as-a-judge evaluators](../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Model%20providers.md#iam-trusted-entity-recommended). One role covers all three. The permissions below also cover the Playground and evaluators.

To let the gateway assume an IAM role:

1. In AWS, create an IAM role with permission to invoke the Bedrock models you use. The gateway calls Bedrock with short-term API keys. The role therefore also needs `bedrock:CallWithBearerToken` and `bedrock-mantle:*`:

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "bedrock:InvokeModel",
           "bedrock:InvokeModelWithResponseStream",
           "bedrock:CallWithBearerToken",
           "bedrock-mantle:*"
         ],
         "Resource": "*"
       }
     ]
   }
   ```

2. In LangSmith, select the workspace that calls Bedrock. Go to **Settings > Integrations > Provider secrets** and click **+ Secret**.

3. Under **Provider**, select **Amazon Bedrock**, then select the **IAM role** method. Enter the role ARN and, optionally, the AWS Region.

4. Copy the example trust policy that the form shows, and add it to the role in AWS. On LangSmith Cloud, the policy lets LangSmith's AWS account assume the role. On BYOC AWS data planes, it lets your data plane's roles assume the role instead. In both cases, the policy requires your workspace ID as the external ID.

5. Click **Save**.

The gateway limits each session to Bedrock actions, even if the role allows more. Sessions last one hour, and the gateway renews them automatically. In AWS CloudTrail, the session name is `langsmith-gw-` followed by the workspace ID.

### Verify the Bedrock setup

Send a test request with a `bedrock/<model-id>` model ID, using a model ID from your Bedrock console. These errors point to the credential:

* **`400` with `bedrock credentials not found`**: the workspace has no Bedrock secrets. Bedrock returns a `400` here, not the `424` other providers return for a missing key.
* **`400` with `incomplete AWS access-key credentials`**: one of `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` is missing.
* **`403` with `STS denied AssumeRole for the configured Bedrock role`**: the role's trust policy does not allow LangSmith, or its external ID is not the workspace ID. On self-hosted LangSmith, the trust policy must allow the pod's own identity instead.

## Configure Azure Foundry

Azure Foundry supports either an API key or a Microsoft Entra ID service principal. Service principal authentication lets you use resources that [disable local authentication](https://learn.microsoft.com/en-us/azure/ai-services/disable-local-auth).

Both methods require `AZURE_FOUNDRY_RESOURCE_NAME`. Set it to the Azure resource name, not a URL or deployment name. The gateway sends requests to `<resource-name>.openai.azure.com` in the Azure public cloud.

For API key authentication, add `AZURE_FOUNDRY_API_KEY` and `AZURE_FOUNDRY_RESOURCE_NAME` through the Azure Foundry provider form, as described in [Add a provider key](#add-a-provider-key).

### Use an Entra ID service principal

To use an Entra ID service principal instead of an API key:

1. Deploy a model on a Foundry resource, or use an existing deployment. Record the resource name and the deployment name. Use the deployment name as the `model` value in requests.

2. [Register an application](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app) in Microsoft Entra ID, or use an existing app registration. Record its directory (tenant) ID and application (client) ID.

3. [Add a client secret](https://learn.microsoft.com/en-us/entra/identity-platform/how-to-add-credentials) to the app registration. Record the secret's value, not its ID.

4. On the Foundry resource, not a project inside it, [assign the app's service principal](https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry) the `Foundry User` role (formerly `Azure AI User`). The generic `Owner`, `Contributor`, and `Reader` roles do not [grant permission to call models](https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry#permissions-for-each-built-in-role).

5. In LangSmith, select the workspace that routes Azure requests. Go to **Settings > Integrations > Provider secrets** and add each of the following as a custom secret:

   | Secret name | Value |
   | - | - |
   | `AZURE_FOUNDRY_RESOURCE_NAME` | Azure resource name. |
   | `AZURE_TENANT_ID` | Directory (tenant) ID. |
   | `AZURE_CLIENT_ID` | Application (client) ID. |
   | `AZURE_CLIENT_SECRET` | Client secret value. |

   Select **Custom** in the provider selector to enter each secret's name and value. The Azure Foundry provider form only exposes API key authentication.

6. Remove `AZURE_FOUNDRY_API_KEY` from the workspace if it is set. An API key takes precedence over service principal credentials, even when the resource disables API key authentication.

All three Entra ID secrets are required. The gateway obtains and refreshes Azure access tokens automatically. Users continue to authenticate to the gateway with their LangSmith API key, not the Azure credentials.

This method uses a client secret. It does not use managed identity or workload identity federation. Client secrets expire, so update `AZURE_CLIENT_SECRET` when you rotate the secret in Entra ID.

### Verify the setup

After you [grant gateway access](Authenticate%20to%20the%20LLM%20Gateway.md#grant-permission-to-call-the-gateway), send a test request through the gateway with your LangSmith API key:

```bash
curl https://gateway.smith.langchain.com/azure/v1/chat/completions \
  --header "Authorization: Bearer $LANGSMITH_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "<deployment-name>",
    "messages": [{"role": "user", "content": "Say hello"}]
  }'
```

A `chat.completion` response confirms the setup. For other Cloud regions, replace the hostname with your [regional gateway](../Get%20started/How%20the%20LLM%20Gateway%20works.md#use-a-regional-gateway).

If Azure returns `PermissionDenied`, confirm that the `Foundry User` role is assigned on the Foundry resource, not a project. A new role assignment can take [up to 10 minutes](https://learn.microsoft.com/en-us/azure/role-based-access-control/troubleshooting#symptom---role-assignment-changes-are-not-being-detected) to take effect.

## Configure Gemini Enterprise Agent Platform

Gemini Enterprise Agent Platform, listed as **Google Vertex AI** in the provider form, authenticates with a Google Cloud service account key in JSON format. The gateway exchanges the key for short-lived access tokens. It does not support workload identity federation, Application Default Credentials, or other external account credentials. A credential file whose `type` is not `service_account` returns a `400`.

To add the service account key:

1. In Google Cloud, [create a service account key](https://cloud.google.com/iam/docs/keys-create-delete) for a service account that can call the models you use.
2. In LangSmith, select the workspace that calls the provider. Go to **Settings > Integrations > Provider secrets** and click **+ Secret**.
3. Under **Provider**, select **Google Vertex AI**. Paste the key's JSON contents as the value, and click **Save**.

The form saves the key as `GOOGLE_VERTEX_AI_WEB_CREDENTIALS`, the same secret the [Playground](../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Create%20and%20manage%20prompts/Configure%20prompt%20settings.md) uses. The gateway also reads `VERTEX_SERVICE_ACCOUNT_JSON`, and uses it first when both are set.

The gateway reads two optional custom secrets:

* **`VERTEX_PROJECT`**: the Google Cloud project to call. Defaults to the `project_id` in the key.
* **`VERTEX_LOCATION`**: `global` or a Google Cloud region, such as `us-central1`. Defaults to `global`.

On self-hosted LangSmith, [GKE workload identity](../../LangSmith%20setup/Self-hosted/Configure%20an%20instance/Authenticate%20Vertex%20AI%20with%20GKE%20workload%20identity.md) covers the Playground, Chat, and Insights, not the gateway. The gateway still needs a service account key.

## Fix provider credential errors

The gateway passes provider errors through to the caller, so most credential problems show up as the provider's own status code and error body. The [`X-LangSmith-Gateway-Metadata`](../Call%20the%20gateway/API%20formats.md#read-response-metadata) response header tells the two apart: for a provider error, it includes `"outcome":"upstream_error"` and `"upstream_error_source":"provider_response"`, with the provider's status in `upstream_status_code`.

To see which providers the caller's workspace can reach, call [`GET /v1/models`](../Call%20the%20gateway/API%20formats.md#list-models). It lists `<provider>/<model>` IDs only for providers that have a key in that workspace.

| Status and response | Cause | Fix |
| - | - | - |
| `424` with `Required workspace secret "<SECRET_NAME>" is missing.` | The workspace that the caller's API key belongs to has no key for the provider in the model ID. | [Add the provider key](#add-a-provider-key) to that workspace, or use an API key from a workspace that has one. |
| An API key error from the provider, such as OpenAI's `Incorrect API key provided: sk-...`, or a `400` from xAI with `Incorrect API key provided.` | The provider key stored in LangSmith is invalid or revoked. | Replace the stored provider key. |
| Anthropic's `invalid x-api-key`, with the client's base URL set to the gateway | The stored Anthropic key is invalid or revoked. | Replace the stored `ANTHROPIC_API_KEY`. |

Amazon Bedrock and Gemini Enterprise Agent Platform return a `400` naming the missing credentials instead of a `424`. See [Verify the Bedrock setup](#verify-the-bedrock-setup).

For errors from the caller's LangSmith API key, such as `401` and `403`, or an `invalid x-api-key` from a client that bypasses the gateway, see [Fix authentication errors](Authenticate%20to%20the%20LLM%20Gateway.md#fix-authentication-errors).

## See also

* [Authenticate to the LLM Gateway](Authenticate%20to%20the%20LLM%20Gateway.md): choose and send the LangSmith API key that callers use.
* [Set up the LLM Gateway](../Get%20started/Set%20up%20the%20LLM%20Gateway.md): set up provider keys, permissions, and policies for your organization.
* [Direct model access](../Call%20the%20gateway/Direct%20model%20access.md): call provider APIs through provider-specific gateway paths.
* [Self-hosted LLM Gateway](../../LangSmith%20setup/Self-hosted/Install%20an%20instance/Additional%20features/Enable%20the%20LLM%20Gateway.md): enable the gateway on self-hosted LangSmith.
