# Monitor LLM Gateway spend

> View and analyze LLM Gateway costs by user, API key, model, provider, and request header.

> [!NOTE]
>
> The LLM Gateway is in [beta](../../LangSmith%20setup/Cloud/Reference/Release%20stages.md).

The LLM Gateway **Usage** tab shows how much LLM cost a [workspace](../../LangSmith%20setup/Govern/Organization/Overview.md#workspaces) has accrued through the gateway. Use it to:

* Compare spend over time.
* Identify the users, API keys, models, providers, and request header values that account for that spend.
* Attribute that spend for [chargebacks](#attribute-spend-for-chargebacks).

Viewing the **Usage** tab requires the `runs:read-stats` and `projects:read` [permissions](../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md) in the workspace, and a Plus or Enterprise [plan](https://docs.langchain.com/langsmith/pricing-plans.md).

## Group and filter LLM spend

Within the Usage tab, select **Breakdown by** to group spend by one of the following dimensions:

* **User**: Attributes spend to the user associated with the personal access token that invoked the gateway. Requests made with a workspace or organization-scoped service key appear as **Unaffiliated with any user**.
* **API key**: Attributes spend to the LangSmith API key that invoked the gateway.
* **Model**: Attributes spend to the model used for the request.
* **Model Provider**: Attributes spend to the provider that served the request, such as OpenAI or Anthropic.
* **Custom Dimension**: Attributes spend to the value of an `X-Gateway-*` request header that your application sends.

When you select **Custom Dimension**, enter the header name in the field that appears. The field defaults to `X-Gateway-Service`, and the `X-Gateway-` prefix is optional. Requests without the header appear under **No value**. For how to send these headers, see [Header-based policies](../Governance/Header-based%20policies.md).

After you select a dimension, use the adjacent filter to show only the entities you select.

## Set the time range and granularity

Use the controls to the chart's top right to define the period covered by every summary, chart, and table on the page:

* **Time range**: Select a preset range from one day to one year, or choose custom dates. Dates and time buckets use UTC.
* **Aggregation granularity**: Group spend into hourly, daily, or weekly buckets. The available options depend on the length of the selected time range.
* **Previous or next period**: Shift backward or forward by one period of the same length to compare adjacent time ranges.

## Interpret the spend summary

The cards above the chart summarize spend and tokens for the selected workspace, time range, dimension, and filters:

* **Total Spend**: The sum of gateway spend over the selected time range.
* **Hourly, Daily, or Weekly Avg**: Total spend divided by the number of time buckets in the selected range.
* **Hourly, Daily, or Weekly Avg / dimension**: Average spend per selected entity for each time bucket. When you have not applied an entity filter, this metric uses the top 10 entities by spend.
* **Total Tokens**: The number of tokens in requests routed through the gateway over the selected time range.

## Analyze the chart and table

The stacked bar chart shows how each entity contributed to spend in every time bucket. Hover over a bar to view the bucket total and the contribution from each visible entity.

The table summarizes the same selection with one row per visible entity. Use it to compare:

* **Hourly, Daily, or Weekly Avg**: The entity's total spend divided by the number of time buckets.
* **Spend Share**: The percentage of spend attributed to the entity.
* **Total Spend**: The entity's total spend over the selected time range.

To drill down, select a row to open a detailed view of that entity. Select a dimension from **Group by** to break its spend down further, for example an API key's spend by user or by custom header. The detailed view has its own filter, time range, and granularity controls, which do not change the controls on the main view.

> [!TIP]
>
> In the detailed view for a user, an API key, or a custom header value, click **View traces** to open the **Traces** tab filtered to that entity's requests over the detailed view's time range. For what each trace records, see [View LLM Gateway traces](View%20LLM%20Gateway%20traces.md).

## Attribute spend for chargebacks

A chargeback bills LLM costs back to the customer, tenant, or cost center that incurred them. Because every request routes through the gateway, the **Usage** tab can split spend along the same lines you bill against. Choose the dimension that matches who you charge:

* **Cost Centers, such as departments, internal groups, or products**: Give each group its own [service key](../Authentication/Authenticate%20to%20the%20LLM%20Gateway.md#choose-a-key-type), then break down by **API key**. Alternatively, have each group's applications send a header such as `X-Gateway-Cost-Center`, then break down by **Custom Dimension**.
* **End customers of your application**: Have your backend send a header such as `X-Gateway-Customer-Id` on each request it makes for a customer, then break down by **Custom Dimension**. To also cap each customer's spend, see [Cap spend per end customer](../Governance/Header-based%20policies.md#cap-spend-per-end-customer).
* **Individual users**: Have each user call the gateway with their own personal access token, then break down by **User**.
* **Custom dimensions**: To bill against any other attribute, such as environment, have your applications send its value in an `X-Gateway-*` header, then break down by **Custom Dimension**.

## See also

* [Spend policies](../Governance/Spend%20policies.md): cap spend for organizations, workspaces, users, and API keys.
* [Header-based policies](../Governance/Header-based%20policies.md): send the request headers that **Custom Dimension** groups by, and limit spend per header value.
* [View LLM Gateway traces](View%20LLM%20Gateway%20traces.md): inspect the individual requests behind the spend.
* [View usage](../../LangSmith%20setup/Account/Billing%20%26%20usage/View%20usage.md): view LangSmith trace usage and billing, which is separate from LLM Gateway spend.
