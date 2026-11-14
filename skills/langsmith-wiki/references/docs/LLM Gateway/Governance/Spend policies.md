# Spend policies

> Set cost limits on LLM usage across your organization and prevent runaway spend before it reaches providers.

> [!NOTE]
>
> The LLM Gateway is in [beta](../../LangSmith%20setup/Cloud/Reference/Release%20stages.md).

A spend policy defines a cost cap for a specific scope (organization, workspace, user, or API key) over a time window (monthly, weekly, daily, or hourly). Once the spend recorded for the window reaches the cap, the [LLM Gateway](../Get%20started/LLM%20Gateway.md) blocks further requests with a `402` response that names the blocking policies:

```json
{"type":"error","error":{"message":"request blocked by gateway policies: <POLICY_NAME>"}}
```

The gateway records a request's cost after the request completes. The request that crosses the cap still succeeds, and only later requests are blocked, so spend for a window can exceed the cap. Requests sent close together can all pass before the first one is recorded, so the overshoot can be larger than one request.

The blocked request is traced to LangSmith with the policy violation recorded as metadata, so you can see exactly what was blocked and why. The violation also surfaces as an issue in [LangSmith Engine](../Observability/View%20LLM%20Gateway%20traces.md#triage-policy-violations).

> [!NOTE]
>
> Spend policies do not apply to calls billed to a [Claude subscription](../Call%20the%20gateway/Set%20up%20coding%20agents.md#use-claude-subscription-oauth), and those calls are left out of spend totals.

## Policy dimensions

Spend policies are evaluated from broadest to most specific. All matching policies are checked, and if any one returns a block, the request is rejected. You can set a policy as a default (applying a blanket spend cap to all workspaces, users, or API keys) or as a granular policy (individual limits or limits on a group of entities).

| Scope | What it caps | Example |
| - | - | - |
| **Organization** | Total spend across all workspaces in the org | "The entire org cannot spend more than \$10,000/month on LLM calls" |
| **Workspace** | Total spend within a single workspace or group of workspaces | "The workspaces related to R\&D cannot spend more than \$2,000/month" |
| **User** | Spend by a single user or group of users (resolved from the API key's identity) | "No individual developer can spend more than \$50/day" |
| **API key** | Spend by a single API key or group of API keys (maps to a service or agent) | "The customer support agent keys cannot spend more than \$500/month cumulatively" |

### Conflict resolution

By default, the gateway assesses the broadest scope first. Narrower scopes can only tighten limits, never loosen them. For example, if an org-level policy caps spend at \$10,000/month and a workspace-level policy caps at \$15,000/month, the \$10,000 org cap still applies.

### Defaults vs. granular policies

Spend policies have two aspects:

1. **Sums across a dimension:** the total cap for that scope. Example: "This workspace's total spend cannot exceed \$5,000/month."
2. **Defaults for each member of a dimension:** a base limit that applies to every API key or user within a scope unless overridden. Example: "Each API key in this workspace gets a \$200/month default cap." Individual API keys can receive additional policies that raise their specific limit, but no policy can loosen a cap set at a broader scope.

## Time window period

The time window sets the period over which spend accumulates against the cap. At the end of each window, recorded spend resets to zero:

| Period | Resets | Use case |
| - | - | - |
| **Monthly** | First of each month | Budget alignment, overall cost control |
| **Weekly** | Midnight UTC on the Monday of each week | Weekly budgeting |
| **Daily** | Midnight UTC | Prevent single-day cost spikes (for example, a coding agent in a retry loop overnight) |
| **Hourly** | Top of each hour | Catch runaway agents quickly |

> [!TIP]
>
> You can apply multiple time windows to the same scope. For example, a workspace can have both a \$5,000/month cap and a \$500/day cap. Both are enforced independently.

## Create a spend policy

> [!WARNING]
>
> Creating and managing policies requires `organization:gateway:manage` permission. Organization Admins and Organization Operators have it by default. For what each organization role can do, see [Organization roles](../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#organization-roles).

1. Go to **LLM Gateway** and select **Cost Controls**.
2. Click **Create spend limit**.
3. Select the **scope** (organization, workspace, user, or API key).
4. (Optional) To separate a default limit by header, select **Workspace**, **User**, or **API Key**. Apply the limit to every subject of that type by default. Alternatively, select exactly one subject to pin the limit to it. Select **Separate limits by custom header**, and enter the header name, such as `Customer-Id`. Send the full `X-Gateway-Customer-Id` header on requests. Each subject and header-value pair receives an independent limit.
5. Set the spend cap in USD and the time window period (monthly, weekly, daily, or hourly).
6. Click **Create spend limit**.

Policies take effect immediately. The gateway evaluates them on every incoming request with sub-second enforcement latency.

> [!TIP]
>
> A spend policy can also use a custom request header to give each end customer, tenant, or cost center an independent cap without issuing a separate API key for each. For more information, see [Header-based policies](Header-based%20policies.md).

## View spend

In **LLM Gateway** > **Cost Controls**, the **Usage** column shows how much each policy has spent, in dollars and as a percentage of its cap.

To analyze spend over time by user, API key, model, or request header, use the **Usage** tab. For more information, see [Monitor LLM Gateway spend](../Observability/Monitor%20LLM%20Gateway%20spend.md).

## See also

* [Header-based policies](Header-based%20policies.md): split a cap by a custom request header so each header value gets its own limit.
* [Data policies](Data%20policies.md): add data policies alongside cost controls.
