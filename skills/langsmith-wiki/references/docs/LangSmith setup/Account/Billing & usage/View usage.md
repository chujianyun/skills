# View usage

> What usage data is available in LangSmith, what each metric means, and what differs for Self-hosted.

LangSmith provides several views into your [organization's](../../Govern/Organization/Overview.md) usage, depending on your [plan](https://docs.langchain.com/langsmith/pricing-plans.md) and [hosting type](../../Overview/Hosting/Set%20up%20LangSmith.md). This page explains what data is available, what each metric means, and what limitations apply to [Self-hosted](../../Self-hosted/Self-hosted%20LangSmith.md).

## Usage views

| View | Where to find it | Who can see it | Plan availability |
| - | - | - | - |
| [Usage graph](#usage-graph) | **Enterprise**: Settings > Usage > Usage graph **Self-serve**: Settings > Billing > Usage graph | All org members | All plans |
| [Granular usage](#granular-usage) | **Enterprise**: Settings > Usage > Granular usage **Self-serve**: Settings > Billing > Granular usage | All org members | All plans |
| [Contract usage](#contract-usage) | **Enterprise**: Settings > Usage > Contract usage **Self-serve**: Settings > Billing > Contract usage | Org admins only (`organization:manage`) | Enterprise only |
| [Invoices](#invoices) | Settings > Billing > Invoices | All org members | Self-serve Cloud only |
| [Evaluator spend](../../../Test/Evaluators/Track%20and%20limit%20evaluator%20spend.md) | Evaluators page, evaluator detail | All workspace members | Tracked weekly, resetting at Monday 12AM UTC, separate from the monthly billing period below |
| [LLM Gateway spend](../../../LLM%20Gateway/Observability/Monitor%20LLM%20Gateway%20spend.md) | LLM Gateway > Usage | Workspace members with `runs:read-stats` and `projects:read` | Plus and Enterprise |

## Usage graph

The usage graph shows aggregate trace consumption for your [organization](../../Govern/Organization/Overview.md#organizations), broken down by [workspace](../../Govern/Organization/Overview.md#workspaces). It covers the current billing period and does not show spend—for spend, refer to the invoice.

Navigate to **Settings** > **Billing and Usage** > **Usage Graph**.

### Billable metrics

| Metric | What it counts |
| - | - |
| **LangSmith Traces (Base Charge)** | Every trace sent to LangSmith during the billing period, regardless of data retention tier. |
| **LangSmith Traces (Extended Data Retention Upgrades)** | Traces upgraded to extended retention (180 days by default as of September 14, 2026, [customizable for Enterprise customers](../../Govern/Data%20%26%20compliance/Data%20purging%20for%20compliance.md#customize-extended-retention-policy)). These are charged in addition to the base charge. |
| **LangSmith Deployment Runs** | End-to-end invocations of deployed LangGraph agents. See [LangSmith Agent Server billing](Manage%20billing%20in%20your%20account.md#langsmith-deployment-billing) for pricing details. |
| **LangSmith Fleet Runs** | End-to-end invocations of [Fleet](../../../Additional%20documentation/No-code%20agents%20with%20LangSmith%20Fleet.md) agents. Tracked separately for Cloud-hosted and Self-hosted deployments. |
| **LangSmith Deployment Nodes Executed** | Individual LangGraph node executions across deployed agents. Each step in a deployed agent's graph counts as one node execution. Tracked separately for Cloud-hosted and Self-hosted deployments. |

For more details on trace retention tiers, refer to [Data retention](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#data-retention).

> [!NOTE]
>
> The usage graph uses the term `tenant_id` interchangeably with workspace ID.

## Contract usage

Enterprise customers with prepaid commitments can view how much of their contract has been consumed.

Navigate to **Settings** > **Usage Configuration** > **Contract Usage**.

This view shows:

* **Usage summary**: Total usage, total credits, and any overages. Overages occur when usage exceeds your total prepaid commitment.
* **Commitment progress bars**: Visual indicators for each commitment showing percentage consumed and dollar amounts for used vs. remaining. Contracts can have multiple commitments that apply to different time periods (e.g., year 1 and year 2 of a multi-year contract) or different products.
* **Monthly usage chart**: Bar chart showing usage amounts for each month within your contract period.
* **Product rates**: Table of your entitled products and their pricing.

> [!NOTE]
>
> Contract usage requires the [`organization:manage` permission](../../Govern/Users%20%26%20access%20control/Organization%20and%20workspace%20operations%20reference.md) and is only available to Enterprise customers with prepaid commitments.

> [!NOTE]
>
> If your contract spans multiple organizations under the same billing entity, the contract usage view shows the **combined** usage accrued across all of those organizations, not just the one you're currently viewing. [Granular usage](#granular-usage) is always scoped to a single organization, so to view granular usage for a specific org, switch to that org and view its granular usage separately.

## Invoices

Invoices are available on **self-serve Cloud plans only**. Enterprise Cloud organizations have a separate usage view for tracking spend.

Navigate to **Settings** > **Billing and Usage** > **Invoices** to see how your usage translates to spend. The first invoice shown is a draft of your current month's invoice, reflecting your running spend to date.

## Granular usage

Granular usage gives trace counts broken down by a dimension you choose (workspace, project, user, or API key) over a time range you select. This is useful for tasks such as charging back trace usage, identifying high-usage users, or auditing trace activity.

> [!NOTE]
>
> Granular usage attributes trace counts, which determine your LangSmith trace charges. It does not attribute model spend. To charge back model spend for requests routed through the LLM Gateway, see [Attribute spend for chargebacks](../../../LLM%20Gateway/Observability/Monitor%20LLM%20Gateway%20spend.md#attribute-spend-for-chargebacks). For model costs recorded on other traces, see [Cost tracking](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Cost%20tracking.md).

Navigate to **Settings** > **Billing and Usage** > **Granular Usage**, or use the [granular usage API](Granular%20billable%20usage.md).

### What "traces" means here

The granular usage view counts **traces**: root-level runs and all their child spans counted as a single unit. This is the same unit used for [billing](Manage%20billing%20in%20your%20account.md). It does not count individual spans, tokens, or model calls separately.

### When usage is recorded

Granular usage records traces by **insertion time** (when the trace was received and stored by LangSmith), not by when it ran in your application. In practice this difference is usually negligible, but traces sent with significant delay (e.g., buffered SDK uploads) may appear in a later time bucket than expected.

For grouping options, time bucket sizes, and API reference, refer to [Granular billable usage](Granular%20billable%20usage.md).

## Self-hosted limitations

[Self-hosted](../../Self-hosted/Self-hosted%20LangSmith.md) LangSmith have a different set of usage views available compared to [Cloud](../../Cloud/Cloud%20%28SaaS%29.md), due to differences in billing infrastructure.

| **Feature** | **Self-hosted availability** |
| - | - |
| Granular usage (trace attribution) | Available with feature flags or version ≥ 0.13.12 |
| Usage graph (aggregate traces) | Available on Helm chart 0.9.5 and later |
| Contract usage | Available when Beacon phone-home is enabled |
| Invoices and payment management | Not available (billing is handled outside LangSmith) |

### Granular usage on self-hosted

Granular usage is available on [Self-hosted](../../Self-hosted/Self-hosted%20LangSmith.md) but requires explicit opt-in:

* On **LangSmith 0.13.12 and later**, granular usage collection is enabled by default.
* On **earlier versions**, enable it by setting both of the following environment variables:

  ```env
  DEFAULT_ORG_FEATURE_ENABLE_GRANULAR_USAGE_REPORTING=true
  GRANULAR_USAGE_TABLE_ENABLED=true
  ```

> [!WARNING]
>
> Data collection begins from the moment the feature is enabled. There is no backfill of historical usage data prior to enabling it. Plan accordingly when choosing when to enable this feature.

### Aggregate usage on Self-hosted

The usage graph is available on [Self-hosted](../../Self-hosted/Self-hosted%20LangSmith.md) running Helm chart 0.9.5 or later. LangSmith automatically generates and syncs organization usage charts, available under **Settings** > **Usage and billing** > **Usage graph**:

* **Usage by Workspace**: trace counts (root runs) per workspace
* **Organization Usage**: total trace counts across the organization

Charts refresh every 5 minutes to include new workspaces and are not editable.

For programmatic access to trace counts, see [View trace counts across your organization](../../Self-hosted/Manage%20an%20instance/View%20trace%20counts%20across%20your%20organization.md).

## Related resources

* [Granular billable usage API reference](Granular%20billable%20usage.md)
* [Manage billing](Manage%20billing%20in%20your%20account.md)
* [Data retention and usage limits](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#data-retention)
* [Track and limit evaluator spend](../../../Test/Evaluators/Track%20and%20limit%20evaluator%20spend.md)
* [Monitor LLM Gateway spend](../../../LLM%20Gateway/Observability/Monitor%20LLM%20Gateway%20spend.md)
* [Organization and workspace operations](../../Govern/Users%20%26%20access%20control/Organization%20and%20workspace%20operations%20reference.md)
