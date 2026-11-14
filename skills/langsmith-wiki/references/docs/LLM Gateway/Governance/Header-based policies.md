# Header-based policies

> Scope gateway spend caps, rate limits, and model access by a custom request header, such as a customer, tenant, or cost center identifier, without issuing a separate API key for each value.

> [!NOTE]
>
> The LLM Gateway is in [beta](../../LangSmith%20setup/Cloud/Reference/Release%20stages.md).

A header-based policy scopes a gateway policy by a request header that your application sends, such as a customer, tenant, or cost center identifier. Use one to give each header value its own limit without issuing a separate [LangSmith API key](../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md) for each value.

The same headers can also attribute spend for chargebacks. On the **Usage** tab, the **Custom Dimension** breakdown groups spend by header value. For this and other ways to attribute spend, see [Attribute spend for chargebacks](../Observability/Monitor%20LLM%20Gateway%20spend.md#attribute-spend-for-chargebacks).

A policy uses a header in one of two ways:

* **Default separated by header**: A default [spend](Spend%20policies.md) or [rate limit](Rate%20limit%20policies.md) policy applies its limit independently to every header value. For example, a default workspace spend limit separated by `X-Gateway-Customer-Id` gives `acme` and `globex` independent limits within each [workspace](../../LangSmith%20setup/Govern/Organization/Overview.md#workspaces). A default applies to every subject of its type unless you pin it to one workspace, user, or API key.
* **Explicit header condition**: A spend, rate limit, or [model access](Model%20access%20policies.md) policy matches one exact header value. For example, a policy with the condition `X-Gateway-Customer-Id: acme` limits only requests that carry that value.

> [!WARNING]
>
> Creating and managing policies requires the `organization:gateway:manage` permission. Organization Admins and Organization Operators have it by default. For what each organization role can do, see [Organization roles](../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#organization-roles).

## Matchable headers

The gateway matches on request headers prefixed with `X-Gateway-`, and on keys inside the `X-Gateway-Metadata` JSON header. No other request header is matchable.

Header names are normalized before matching:

* The `X-Gateway-` prefix is stripped, the remainder is lowercased, and every character outside `a-z`, `0-9`, and `_` is replaced with `_`.
* The headers `X-Gateway-Customer-Id`, `x-gateway-customer_id`, and `X-Gateway-CUSTOMER.ID` all resolve to the matcher key `customer_id`.
* Header values are compared as exact, case-sensitive strings, with no wildcard or pattern matching.

The gateway stamps caller identity itself and ignores client attempts to override it. It discards headers and `X-Gateway-Metadata` keys that resolve to any of the following:

* **Caller identity**: `organization_id`, `workspace_id`, `workspace_handle`, `user_id`, `user_email`, `api_key_id`, `api_key_short`, and `auth_mode`.
* **Credentials and client**: `credential_source`, `provider_key_hint`, and `user_agent`.
* **Applied policies**: `applied_policy_ids` and `applied_policy_names`.
* **Agents**: `agent_uuid`, `agent_id`, and `agent_environment_id`.
* **Gateway-prefixed keys**: any key whose normalized name starts with `gateway`.

A request that sets `ls_metadata_only` or `content_quota_exceeded`, either as a header or as an `X-Gateway-Metadata` key, is rejected with a `400` error, because the gateway sets those keys itself.

> [!WARNING]
>
> The gateway trusts the `X-Gateway-*` headers on an incoming request. Set the header in your own backend after you authenticate the end user, and do not distribute the gateway API key to end users. A caller that controls both the key and the header can choose which limit to use.

## Separate a default limit by header

A default spend or rate limit applies the same limit to every member of a subject dimension, such as every workspace or every API key. Separating it by a header applies that limit independently to every subject and header-value pair, without requiring a policy for each value. A separated default can also be pinned to one workspace, user, or API key, so that only that subject gets a limit for each header value.

Separated defaults follow these rules:

* **One header per default**: Enter the header name only. The request supplies the value that identifies the bucket.
* **Independent limits**: Each subject and header-value pair receives the configured limit. The gateway creates each of these limits the first time a request carries a new header value. Requests without the configured header share a fallback limit for their subject.
* **Replacement**: Creating an organization-wide default replaces the existing organization-wide default of the same policy type for the same subject type, even when the two defaults use different headers. Creating a pinned default replaces only a pinned default of the same policy type, subject, and header.
* **Pinned defaults take precedence**: For requests from its subject, a pinned default replaces the organization-wide default of the same policy type, subject type, and header. Defaults separated by a different header, or not separated by a header, still apply.

The UI offers header separation on default spend limits only. To separate a default spend limit by header:

1. Go to **LLM Gateway** and select **Cost Controls**.
2. Click **Create spend limit**.
3. Select **Workspace**, **User**, or **API Key**.
4. Choose the scope:
   * To apply the limit to every subject of that type, select the checkbox that applies the limit by default.
   * To pin the limit to one subject, select exactly one workspace, user, or API key.
5. Select **Separate limits by custom header**.
6. In **Header name**, enter the part of the header name after `X-Gateway-`, which the form shows in front of the field. For example, enter `Customer-Id` for the `X-Gateway-Customer-Id` request header.
7. Set the spend limit, and then click **Create spend limit**.

The policy table shows the header under the policy's scope, for example "Limits separated by X-Gateway-Customer-Id". You can also edit an existing default spend limit to add, change, or remove the header. To remove the header from a pinned default or change its subject, delete it and create a new policy.

To separate a default rate limit by header, create a `default_rate_limit` policy through the [LangSmith REST API](../../Monitor/Reference/LangSmith%20REST%20API/LangSmith%20API%20reference.md). To pin a default spend or rate limit through the API, set its subject matcher's value to the subject's ID. The **Rate Limiting** table does not show the header on a default rate limit that has one. Before you create a default through the API, list the existing defaults with `policy_type=default_spend_cap` or `policy_type=default_rate_limit`, so you do not replace a default that someone else configured.

Use an explicit policy instead when different header values need different limits.

## Add an explicit header condition

An explicit spend, rate limit, or model access policy can match one exact header value. Use an explicit policy to assign different limits to different header values.

Explicit header conditions follow these rules:

* **One condition per policy**: A policy accepts one header name and one value.
* **One subject scope**: Combine the condition with an organization, workspace, user, or API key scope. The subject side accepts several values and matches any of them.
* **Missing headers do not match**: A request without the configured header does not match the policy.
* **Every matching policy is enforced**: A request that matches both a plain subject policy and a policy with a header condition counts against both, and either one can block it.
* **At most 10 conditions**: A policy carries no more than 10 subject conditions in total.

The UI offers explicit header conditions on spend limits and rate limits, but not on defaults. To add one:

1. Go to **LLM Gateway**, then select **Cost Controls** for a spend limit or **Rate Limiting** for a rate limit.
2. Click **Create spend limit** or **Create rate limit**.
3. Select the subject type, and then select one or more subjects. Leave the **Apply to every ... by default** checkbox cleared, because selecting it hides the header condition. On a spend limit for one subject, also leave **Separate limits by custom header** cleared.
4. Under **Custom header condition (optional)**, enter the **Header name** without its `X-Gateway-` prefix (for example, `Customer-Id`) and the **Header value** to match (for example, `acme`).
5. Set the limits, and then click **Create spend limit** or **Create rate limit**.

The policy table shows the header value next to the subject, for example `my-key, acme`, but not the header name.

You cannot edit the header condition in the UI after the policy is created. To change it, delete the policy and create a new one, or update `subject_matchers` through the API.

Model access policies accept a header condition through the API only. The condition narrows the policy without changing its tier: a model access policy scoped to a workspace and a header ranks with the other workspace policies, so a matching request must satisfy all of them. For how tiers override each other, see [Policy overrides](Model%20access%20policies.md#policy-overrides). The **Model Access** table shows the header value next to the workspace name. The edit form does not display the header condition, but editing the policy in the UI keeps it.

## Cap spend per end customer

A reseller or multi-tenant application usually calls the gateway from its own backend, using one workspace-scoped API key on behalf of many end customers. Use an explicit header condition when each customer needs a different cap. If every customer uses the same cap, [separate one default spend limit by header](#separate-a-default-limit-by-header) instead.

### Step 1. Send a customer header on every call

Attach the header to each request your backend makes on behalf of an end customer. Replace `<MODEL_ID>` with a [model ID](../Call%20the%20gateway/API%20formats.md#choose-a-model-id):

```bash curl
curl https://gateway.smith.langchain.com/v1/chat/completions \
    -H "Authorization: Bearer $LANGSMITH_API_KEY" \
    -H "Content-Type: application/json" \
    -H "X-Gateway-Customer-Id: acme" \
    -d '{"model":"<MODEL_ID>","messages":[{"role":"user","content":"ping"}]}'
```

```python OpenAI SDK
import os

from openai import OpenAI

client = OpenAI(
    base_url="https://gateway.smith.langchain.com/v1",
    api_key=os.environ["LANGSMITH_API_KEY"],
)
customer_id = "acme"
response = client.chat.completions.create(
    model="<MODEL_ID>",
    messages=[{"role": "user", "content": "ping"}],
    extra_headers={"X-Gateway-Customer-Id": customer_id},
)
print(response.choices[0].message.content)
```

> [!NOTE]
>
> If your LangSmith account is on a regional instance, use the corresponding [regional gateway](../Get%20started/How%20the%20LLM%20Gateway%20works.md#use-a-regional-gateway).

### Step 2. Create a cap for one customer

Create one spend policy per end customer through the [LangSmith REST API](../../Monitor/Reference/LangSmith%20REST%20API/LangSmith%20API%20reference.md). Replace `<WORKSPACE_ID>` with the ID of the workspace that owns the API key your backend uses:

```bash curl
curl -X POST "https://api.smith.langchain.com/v1/platform/gateway-policies" \
    -H "X-Api-Key: $LANGSMITH_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "name": "customer-acme-monthly-cap",
          "policy_type": "spend_cap",
          "action": "block",
          "subject_matchers": [
            {"key": "workspace_id", "value": "<WORKSPACE_ID>"},
            {"key": "customer_id", "value": "acme"}
          ],
          "config": {"window": "monthly", "limit_usd": 250}
        }'
```

```python Python
import os

import httpx

response = httpx.post(
    "https://api.smith.langchain.com/v1/platform/gateway-policies",
    headers={"X-Api-Key": os.environ["LANGSMITH_API_KEY"]},
    json={
        "name": "customer-acme-monthly-cap",
        "policy_type": "spend_cap",
        "action": "block",
        "subject_matchers": [
            {"key": "workspace_id", "value": "<WORKSPACE_ID>"},
            {"key": "customer_id", "value": "acme"},
        ],
        "config": {"window": "monthly", "limit_usd": 250},
    },
    timeout=30.0,
)
response.raise_for_status()
```

The matcher key is the normalized name `customer_id`, not the header name `X-Gateway-Customer-Id`. The policy belongs to the organization that owns the API key.

Posting a policy whose `subject_matchers` already exist updates that policy instead of adding a duplicate, so this call is safe to repeat.

If a default workspace spend limit is [separated by the same header](#separate-a-default-limit-by-header), the explicit cap replaces the default for this customer in this workspace. When the default has already created a limit for the customer, posting the cap converts that limit into the explicit one. Deleting the explicit cap returns the customer to the default limit. A default on another subject type, such as a default API key limit separated by the same header, still enforces its own limit for the customer alongside the explicit cap.

### Step 3. Sync policies with your customer list

Because each end customer needs its own policy, keep the policy set in step with your customer list. The following script manages the caps in one workspace. It creates or updates a cap for every current customer, then deletes the caps of customers that are gone:

```python
import os

import httpx

API_URL = "https://api.smith.langchain.com/v1/platform/gateway-policies"
WORKSPACE_ID = os.environ["LANGSMITH_WORKSPACE_ID"]

# Your source of truth: end customer identifier mapped to a monthly cap in USD.
CUSTOMER_CAPS = {"acme": 250.0, "globex": 1000.0, "initech": 50.0}


def matchers_for(customer: str) -> list[dict[str, str]]:
    return [
        {"key": "workspace_id", "value": WORKSPACE_ID},
        {"key": "customer_id", "value": customer},
    ]


def existing_caps(client: httpx.Client) -> dict[str, dict]:
    """Return this workspace's explicit per-customer spend caps, keyed by customer."""
    response = client.get(
        API_URL,
        params={
            "policy_type": "spend_cap",
            "subject_matcher_key": "workspace_id",
            "subject_matcher_value": WORKSPACE_ID,
        },
    )
    response.raise_for_status()
    caps = {}
    for policy in response.json():
        if policy.get("parent_policy_id"):
            continue  # Created by a default spend limit, not by this script.
        matchers = policy["subject_matchers"]
        customer = next((m["value"] for m in matchers if m["key"] == "customer_id"), None)
        if customer is None or len(matchers) != 2:
            continue  # Not a workspace and customer cap.
        caps[customer] = policy
    return caps


def sync() -> None:
    headers = {"X-Api-Key": os.environ["LANGSMITH_API_KEY"]}
    with httpx.Client(headers=headers, timeout=30.0) as client:
        existing = existing_caps(client)

        # Posting an existing matcher set updates that policy, so this both
        # creates caps for new customers and corrects caps that changed.
        for customer, limit_usd in CUSTOMER_CAPS.items():
            client.post(
                API_URL,
                json={
                    "name": f"customer-{customer}-monthly-cap",
                    "policy_type": "spend_cap",
                    "action": "block",
                    "subject_matchers": matchers_for(customer),
                    "config": {"window": "monthly", "limit_usd": limit_usd},
                },
            ).raise_for_status()

        # Deletes this workspace's caps for customers missing from
        # CUSTOMER_CAPS, including caps created outside this script.
        for customer, policy in existing.items():
            if customer not in CUSTOMER_CAPS:
                client.delete(f"{API_URL}/{policy['id']}").raise_for_status()


if __name__ == "__main__":
    sync()
```

The list endpoint returns every policy in the organization, so the script asks only for policies whose matchers include this workspace. It also skips any policy with a `parent_policy_id`: when a default spend limit is separated by the same header, the gateway creates a limit for each header value, and those limits carry a `customer_id` matcher too. Without the skip, the script would treat them as its own caps and delete them.

Run the script whenever a customer signs up, churns, or moves to a different plan. Rerunning it with an unchanged customer list is safe.

### Step 4. Read spend per customer

Each spend policy returned by the API reports `current_spend_usd`, the spend accumulated in the policy's active window. Use it to show each end customer their usage, or to warn them before they reach the cap. The field is omitted when the spend lookup fails, so treat a missing value as unknown rather than as zero.

As in step 3, filter the list to one workspace with `subject_matcher_key` and `subject_matcher_value`, and skip the limits that a default spend limit creates. Otherwise, a customer under a default separated by the same header appears twice, with two different limits:

```python
import os

import httpx

WORKSPACE_ID = os.environ["LANGSMITH_WORKSPACE_ID"]

response = httpx.get(
    "https://api.smith.langchain.com/v1/platform/gateway-policies",
    headers={"X-Api-Key": os.environ["LANGSMITH_API_KEY"]},
    params={
        "policy_type": "spend_cap",
        "subject_matcher_key": "workspace_id",
        "subject_matcher_value": WORKSPACE_ID,
    },
    timeout=30.0,
)
response.raise_for_status()

for policy in response.json():
    if policy.get("parent_policy_id"):
        continue  # Created by a default spend limit, not one of your caps.
    matchers = policy["subject_matchers"]
    customer = next((m["value"] for m in matchers if m["key"] == "customer_id"), None)
    if customer is None or len(matchers) != 2:
        continue  # Not a workspace and customer cap.
    # current_spend_usd is absent when the spend lookup fails.
    print(customer, policy.get("current_spend_usd"), policy["config"]["limit_usd"])
```

## Limit throughput per end customer

Rate limits use the same subject matchers. Swap `policy_type` and `config` to give an end customer its own request and token allowance:

```bash
curl -X POST "https://api.smith.langchain.com/v1/platform/gateway-policies" \
    -H "X-Api-Key: $LANGSMITH_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "name": "customer-acme-rate-limit",
          "policy_type": "rate_limit",
          "action": "block",
          "subject_matchers": [
            {"key": "workspace_id", "value": "<WORKSPACE_ID>"},
            {"key": "customer_id", "value": "acme"}
          ],
          "config": {
            "version": 1,
            "limits": [
              {"metric": "requests", "window": "minute", "value": 100},
              {"metric": "tokens", "window": "hour", "value": 1000000}
            ]
          }
        }'
```

To keep rate limits in step with your customer list, adapt the [step 3 sync script](#step-3-sync-policies-with-your-customer-list): map each customer to a list of limits instead of one `limit_usd`, build `config` from that list, use `rate_limit` as the `policy_type` in both the list and create calls, and change the policy name. Keep the workspace filter and the `parent_policy_id` skip, because a default rate limit separated by a header also creates a limit for each header value.

Spend caps and rate limits are separate families, so an end customer can hold one of each on the same header value.

## See also

* [Spend policies](Spend%20policies.md): set cost caps for organizations, workspaces, users, and API keys.
* [Rate limit policies](Rate%20limit%20policies.md): limit requests and tokens in a rolling window.
* [Model access policies](Model%20access%20policies.md): control which models each subject can call.
* [Monitor LLM Gateway spend](../Observability/Monitor%20LLM%20Gateway%20spend.md): break down spend by header value and attribute it for chargebacks.
* [View LLM Gateway traces](../Observability/View%20LLM%20Gateway%20traces.md): understand where gateway traces land and who can configure policies.
