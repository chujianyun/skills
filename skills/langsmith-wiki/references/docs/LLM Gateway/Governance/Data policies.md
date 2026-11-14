# Data policies

> Create data policies that redact sensitive data and control trace content in the LLM Gateway.

> [!NOTE]
>
> The LLM Gateway is in [beta](../../LangSmith%20setup/Cloud/Reference/Release%20stages.md).

A data policy controls what happens to the content of requests that pass through the [LLM Gateway](../Get%20started/LLM%20Gateway.md):

* Whether LangSmith stores request and response bodies in traces
* Which sensitive data, such as personal information or API keys, the gateway redacts before a request reaches the LLM provider.

Administrators use data policies to keep customer data and credentials that developers or agents put in prompts away from third-party providers, and to limit what LangSmith stores, without changing application code.

Like the other gateway policies, a data policy can apply to an organization, a workspace, a user, or an API key. Each policy has two parts, matching the two sections of the create form:

* **Data retention**: whether the gateway writes request and response bodies to the LangSmith trace.
* **Data protection**: which sensitive data the gateway scans for and redacts before a request reaches the LLM provider, how long that scan may run, and whether a request proceeds when the limit is exceeded.

## Availability

Data policies are available to every organization with access to the LLM Gateway. Two entitlements shape what the **Data Policy** tab offers:

* **Data protection** is on by default. If the entitlement is turned off, cloud Enterprise organizations see the tab grayed out with a **Request access** link. Every other organization does not see the tab at all.
* **PII redaction** is off by default and enabled for selected organizations. Without it, the PII options are unavailable in the create and edit forms, and the API rejects any policy configured to detect PII.

Contact your account team to change either entitlement.

## Data retention

The **Trace content** toggle controls whether request and response bodies are stored in gateway traces. It is off for all organizations, and a data policy turns it on for the requests that policy matches. When several data policies match a request, the most specific scope decides. If policies at the same scope disagree, content is not stored. With content off, traces still record metadata such as token usage, latency, status, model information, and policy evaluation results.

For where gateway traces appear, what metadata they carry, and how trace content affects billing, see [View LLM Gateway traces](../Observability/View%20LLM%20Gateway%20traces.md).

## Data protection

When a data policy enables detection, the gateway scans outbound requests before they reach the LLM provider. Detected values are replaced with placeholders before the request is forwarded upstream, so the provider only ever sees the redacted payload. For successful responses, the gateway restores the placeholders to the original values before returning the response to the caller.

The **PII** and **Secrets** toggles are independent. On a new policy, PII detection starts on with every rule selected (for organizations that have the entitlement) and secrets detection starts off.

### PII detection

The **Personally Identifiable Information (PII)** toggle covers names, emails, US phone numbers, addresses, and US SSNs. Six rules sit beneath it, each selectable on its own, grouped by how the gateway detects them.

Rule-based categories are matched with regular expressions and are faster to detect:

| Category | Patterns detected |
| - | - |
| **Emails** | Email address patterns |
| **US phone numbers** | Common US formats, for example `415-555-1234` and `+1 (415) 555-1234`. A bare 10-digit number is not matched |
| **US Social Security numbers** | US SSN patterns, for example `123-45-6789` |

Model-based categories are matched by Presidio and are slower to detect:

| Category | Examples |
| - | - |
| **Names** | Person names in natural language |
| **Locations** | Addresses, cities, countries |
| **Nationality, religious, and political groups** | Nationality, religious affiliation, political affiliation |

### Secrets detection

The **Secrets** toggle detects common API keys, tokens, and credentials and redacts them from the request:

| Category | Patterns detected |
| - | - |
| **LangSmith** | Personal access tokens, service keys, legacy API keys |
| **AWS** | Access tokens |
| **GitHub** | Personal access tokens, fine-grained PATs, OAuth tokens, app tokens |
| **GitLab** | Personal access tokens |
| **AI providers** | OpenAI API keys, Anthropic API keys |
| **Cloud platforms** | GCP API keys, Azure AD client secrets, Google OAuth access tokens |
| **Collaboration tools** | Slack bot, user, and app tokens, Slack webhook URLs, Datadog access tokens |
| **Package registries** | PyPI upload tokens, npm access tokens |
| **Cryptographic** | Private keys, JWTs |
| **Other** | Stripe access tokens, SendGrid API tokens |

Detection is deliberately narrow: only rules anchored to a recognizable token shape are applied, so high-entropy prose in a prompt does not trigger a redaction.

### Scan time and timeout behavior

Each data policy caps how long the scanning pipeline may run and decides what happens when that cap is reached:

* **Max processing time (seconds)**: 2 by default, configurable from 0.1 to 30.
* **On timeout**: **Allow request** by default. Set it to **Block request** to reject a request whose scan does not finish in time.

Both fields appear only for organizations with the PII detection entitlement. Elsewhere the policy uses the defaults.

## Create a data policy

> [!WARNING]
>
> Creating and managing policies requires `organization:gateway:manage` permission.

1. In the LangSmith sidebar, click **LLM Gateway**.
2. Open the **Data Policy** tab.
3. Click **Create data policy**.
4. Select the scope: **Organization**, **Workspace**, **User**, or **API Key**.
5. Enter a **Policy name**, or keep the generated one.
6. For a workspace, user, or API key scope, select the specific subjects the policy applies to.
7. (Optional) Under **Data retention**, enable **Trace content** to store request and response bodies in traces.
8. Under **Data protection**, enable **Secrets**, **PII**, or both. For PII, select the rules to apply.
9. (Optional) Set **Max processing time (seconds)** and **On timeout**.
10. Click **Create data policy**.

Data policies apply to all requests that pass through the gateway in the scope where they are configured. They take effect immediately.

## How redacted content appears

When PII or a secret is detected, the content is replaced with a placeholder in both the request sent to the provider and the LangSmith trace. For example:

**Original request:**

```text
Please process the refund for John Smith, SSN 123-45-6789.
```

**Upstream redaction:**

```text
## disclaimer: Some values have been redacted by a reverse proxy and replaced with placeholders containing unique identifiers.

Please process the refund for [SAFE_TO_USE:PERSON_kbqdjxyz], SSN [SAFE_TO_USE:US_SSN_abqxlmwp].
```

The gateway prepends the disclaimer so the model treats the placeholders as values it can reuse verbatim.

Placeholders follow the format `[SAFE_TO_USE:<CATEGORY>_<suffix>]`:

* **SAFE\_TO\_USE:** fixed prefix marking the value as a redacted placeholder.
* **\<CATEGORY>:** the detected type. Examples: `PERSON`, `LOCATION`, `US_SSN`, `US_PHONE_NUMBER`, `OPENAI_API_KEY`, `GITHUB_PAT`, `LANGSMITH_PERSONAL_TOKEN`.
* **\<suffix>:** an 8-character tag. A value that appears twice in one request gets the same placeholder both times, and the tags cannot be correlated across requests.

The trace in LangSmith shows the redacted version along with metadata indicating that redaction occurred and which categories were detected.

**Downstream de-redacted response:**

When the upstream provider returns a successful response, the gateway replaces the placeholders with the caller's original values. Streamed responses are rewritten event by event, so de-redaction does not delay the stream. For example, your agent may see this response:

```text
Confirming John Smith's SSN as 123-45-6789. I will process the full refund.
```

## What redaction covers

**What it covers:**

* Outbound request content (the message sent to the LLM provider) is scanned and redacted before it leaves the gateway.
* The redacted version is what appears in LangSmith traces.
* Placeholders in a successful provider response, streamed or not, are restored to the original values before the response reaches the caller.

**What it does not cover:**

* **Responses from the LLM provider:** if the model generates sensitive data in its response, that content is not scanned or redacted. Only the request is scanned.
* **Provider errors:** when the provider returns a status of 400 or above, the gateway passes the body through untouched, so the caller sees the placeholders rather than the original values.
* **Application traces outside the gateway:** your application receives the restored values, so its own traces can capture them.
* **Data already in your traces:** redaction only applies to requests flowing through the gateway. Traces written directly to the LangSmith API (bypassing the gateway) are not scanned.
* **Platform-level ingestion:** if your requirement is to prevent PII from ever entering LangSmith regardless of how it arrives (for example, data residency compliance), gateway redaction alone is not sufficient. That requires ingestion-level redaction, which is a separate capability.
* **System and developer prompts:** these are skipped, along with assistant tool-call metadata and tool-call arguments that arrive as a single JSON string. User messages, tool results, and structured tool-call arguments are scanned.

**Scanner failures fail open:** if a scanner is unreachable or errors, the request continues to the provider with the content that stage produced. Only a scan timeout can block a request, and only when the policy's timeout action is set to **Block request**.

The coverage boundary matters. If your security model requires that sensitive data never reaches any system (not just the LLM provider), make sure you understand which surface the gateway covers and which surfaces require additional controls.

## Next steps

* [View LLM Gateway traces](../Observability/View%20LLM%20Gateway%20traces.md): see where gateway traces land and who can read them.
* [Spend policies](Spend%20policies.md): add cost controls alongside data protection.
