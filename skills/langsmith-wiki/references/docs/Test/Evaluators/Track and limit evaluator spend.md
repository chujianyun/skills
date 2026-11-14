# Track and limit evaluator spend

> Cap weekly LLM spend on evaluators with an organization-wide default or per-evaluator overrides to keep evaluator costs predictable.

Cap weekly LLM spend per evaluator to prevent a single evaluator from exceeding your budget. LangSmith tracks week-to-date evaluator spend, resetting at Monday 12AM UTC. It lets [organization admins](../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#organization-admin) set a weekly cap on each evaluator's [attached projects and datasets](../Get%20started/Evaluation%20concepts.md#attaching-an-evaluator-to-a-tracing-project-or-dataset). The cap can be a single organization-wide default or a custom override on a specific attached project or dataset.

This guide shows you how to view and configure weekly evaluator spend caps.

> [!TIP]
>
> LangSmith also offers [per-trace and per-model cost tracking](../../Monitor/Trace/Configuration%20%26%20troubleshooting/Cost%20tracking.md) and [tracing usage limits](../../LangSmith%20setup/Govern/Organization/Overview.md#usage-limits) for cost control.

> [!WARNING]
>
> Setting spend limits is available for OpenAI, Anthropic, and Gemini models. Spend limits only enforce against runs on supported models that have [pricing configured](../../Monitor/Trace/Configuration%20%26%20troubleshooting/Cost%20tracking.md#create-a-new-or-modify-an-existing-model-price-entry) in LangSmith. Verify model pricing before relying on a limit. Unsupported models cannot be used in evaluators once a limit is set.

> [!NOTE]
>
> The UI labels the week-to-date window as **this week**.

## How enforcement works

LangSmith records spend after each evaluator run completes, then sums spend from Monday 12AM UTC to the current moment. When the total reaches the effective limit, LangSmith pauses the evaluator on that attached project or dataset. In-flight runs may push the total slightly above the cap before they finalize, so spend can briefly overshoot by a small amount.

The agent and the trace are unaffected. Only the evaluator stops producing scores until the spend limit resets or the limit is [manually increased](#override-the-default-for-an-attached-project-or-dataset).

## Spend views and controls

| View | Where to find it | Who can see or change it |
| - | - | - |
| [Evaluators page dashboard](#evaluators-page-dashboard) | **Evaluators** in the left sidebar | All workspace members |
| [Evaluators table](#evaluators-table) (Spend, Spend Status) | **Evaluators** in the left sidebar | All workspace members |
| [Projects & Datasets tab](#projects-%26-datasets-tab-on-an-evaluator) | Open an evaluator, **Projects & Datasets** (**Environments & Datasets** in an agent-based workspace) | All workspace members |
| [Organization default spend limit](#set-an-organization-default-spend-limit) | Organization **Settings** > **Usage Configuration** | `organization:manage` required to view and edit |
| [Per-evaluator override](#override-the-default-for-an-attached-project-or-dataset) | Edit evaluator > **Advanced** > **Spend limit** | All members can view, `organization:manage` required to edit |

> [card] [Set your first limit](#set-an-organization-default-spend-limit)
>
> Open organization **Settings** and define a single weekly cap that applies to all evaluator attachments to every project and dataset across all workspaces in the organization.

> [card] [Override for one project or dataset](#override-the-default-for-an-attached-project-or-dataset)
>
> Customize the limit for a specific project or dataset attached to an evaluator.

## View evaluator spend

You can find spend in the following UI locations:

### Evaluators page dashboard

Navigate to the **Evaluators** page from the left sidebar. The top of the page shows a weekly view across the workspace:

* **Daily evaluator spend**: Stacked bar chart of spend per day. Toggle between **Evaluator** and **Project / Dataset** breakdowns.
* **Evaluator spend this week**: Total USD spend across all evaluators, with the change versus the previous week.
* **Evaluator traces this week**: Total trace count across all evaluators, with the change versus the previous week.
* **Weekly evaluator spend limit monitoring**: Sorted list of top spenders with a per project or dataset progress bar against its `$ spent / $ limit`. The header surfaces the count of projects or datasets that have hit their limit (**Limit hit**) or are **on pace to hit limit**.

Use the **Prev week** and **Next week** controls in the page header to move the weekly view.

The tracing project, agent environment, or dataset view has an **Evaluators** tab that mirrors these widgets scoped to that one, for example, **Daily evaluator spend on this tracing project**.

### Evaluators table

The Evaluators table on the same page includes:

* **Spend (this week)**: Total LLM cost for the evaluator across all attached projects and datasets since Monday 12AM UTC. Evaluators that do not call an LLM (for example, code evaluators), disabled evaluators, and evaluators without an attached project or dataset show no value.
* **Spend Status**: One of the following:
  * **Under limits**: At least one attached project or dataset has a limit, and none are at the cap.
  * **N limit hit**: The evaluator has reached its limit in one or more projects or datasets it is attached to. The number reflects how many are paused.
  * **Unlimited**: No limits have been set.
  * No value is shown for evaluators that do not call an LLM (for example, code evaluators) and evaluators without an attached project or dataset.

### Projects & Datasets tab on an evaluator

Open an evaluator and select the **Projects & Datasets** tab to see per-project or dataset spend and limits. In an agent-based workspace, the tab is **Environments & Datasets**:

* **Spend (this week)**: Total LLM cost for the evaluator on that project or dataset since Monday 12AM UTC.
* **Percent of Spend Limit**: Progress bar showing spend against the limit since Monday 12AM UTC.
* **Weekly Limit**: Effective weekly limit for that project or dataset, either the organization default or a custom override.

For attachment management, refer to [Manage evaluators](Manage%20evaluators.md).

## Set an organization default spend limit

Organization admins set a single weekly cap that applies to every evaluator's attached projects and datasets across every workspace in the organization. There is one default per organization, not one per workspace.

> [!NOTE]
>
> Setting and editing the organization default requires the `organization:manage`[permission](../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md).

1. Open organization **Settings** and navigate to **Usage Configuration**.
2. For **Evaluator spend limit**, enter a USD amount. The unit is `/ week`. Leave blank for no limit.
3. Click **Save**.

If no organization default is set, attached projects and datasets are unlimited unless a custom override is configured. Clearing the default removes the cap from every attached project or dataset that currently inherits it.

Changing the default updates only attached projects and datasets that inherit it. Custom overrides are preserved.

## Override the default for an attached project or dataset

Organization admins can override the default for a specific project or dataset attached to an evaluator.

1. Navigate to **Evaluators** in the left sidebar and open the evaluator.
2. Click the **Edit evaluator** icon at the top right.
3. Under **Source**, select the specific project or dataset.
4. Scroll past **Filters** and **Sampling Rate**, then expand **Advanced**.
5. In the **Spend limit** field, set a custom USD amount. The unit is `/ week`.
6. **Save** the evaluator configuration.

The hint text below the field shows whether the current value is the organization default or a custom limit. To revert an override back to the organization default, click **Reset to organization default**.

Members without `organization:manage` see the limit but cannot change it. The read-only view shows one of:

* `Unlimited / week (organization default)`
* `$<amount> / week (organization default)`
* `$<amount> / week (custom limit)`

## When a limit is reached

When weekly spend on an attached project or dataset reaches its effective limit:

* LangSmith stops running the evaluator on new runs from that project or dataset.
* The Evaluators table **Spend Status** column shows **N limit hit**, and the Weekly evaluator spend limit monitoring widget surfaces the affected project or dataset.
* Skipped runs are not backfilled. Evaluation resumes automatically on new runs once the spend limit resets or the limit is [manually increased](#override-the-default-for-an-attached-project-or-dataset).

## Configure model pricing

When a spend limit is set, evaluators can only be run on supported models (OpenAI, Anthropic, and Gemini), and the models need to have pricing configured. Models without pricing configured cannot be used in evaluators.

Configure pricing for the models your evaluators use under [Model pricing](../../Monitor/Trace/Configuration%20%26%20troubleshooting/Cost%20tracking.md#create-a-new-or-modify-an-existing-model-price-entry).

## Troubleshooting

**Trouble creating an evaluator**: When a limit is set, evaluators must use a supported model (OpenAI, Anthropic, or Gemini) with a pricing entry in [Model pricing](../../Monitor/Trace/Configuration%20%26%20troubleshooting/Cost%20tracking.md#create-a-new-or-modify-an-existing-model-price-entry).

**LangSmith spend does not match my LLM provider invoice**: LangSmith computes spend from the per-model rates configured in [Model pricing](../../Monitor/Trace/Configuration%20%26%20troubleshooting/Cost%20tracking.md#create-a-new-or-modify-an-existing-model-price-entry), not from your provider's billing. Differences are expected if your provider applies discounts, custom contracts, or model variants you have not added to LangSmith.

## Related resources

* [Manage evaluators](Manage%20evaluators.md)
* [Set up LLM-as-a-judge online evaluators](../../Monitor/Observe/Online%20evaluators/Set%20up%20LLM-as-a-judge%20online%20evaluators.md)
* [Cost tracking](../../Monitor/Trace/Configuration%20%26%20troubleshooting/Cost%20tracking.md)
* [Model pricing](../../Monitor/Trace/Configuration%20%26%20troubleshooting/Cost%20tracking.md#create-a-new-or-modify-an-existing-model-price-entry)
* [Billing](../../LangSmith%20setup/Account/Billing%20%26%20usage/Manage%20billing%20in%20your%20account.md)
