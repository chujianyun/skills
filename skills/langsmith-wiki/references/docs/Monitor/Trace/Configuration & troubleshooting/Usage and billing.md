# Usage and billing

> Understand LangSmith trace data retention tiers, pricing, rate limits, and usage limits.

## Data retention

This section covers how data retention works and how it's priced in LangSmith.

### Why retention matters

* **Privacy**: Many data privacy regulations, such as GDPR in Europe or CCPA in California, require organizations to delete personal data once it's no longer necessary for the purposes for which it was collected. Setting retention periods aids in compliance with such regulations.
* **Cost**: LangSmith charges less for traces that have low data retention. For more information, learn how to [enforce spend limits](../../../LangSmith%20setup/Account/Billing%20%26%20usage/Manage%20billing%20in%20your%20account.md#enforce-spend-limits).

> [!TIP]
>
> Plan your retention tiers before you start sending traces. Changes apply to new traces only—existing traces keep their original tier. See [Change project-level default retention](../../../LangSmith%20setup/Account/Billing%20%26%20usage/Manage%20billing%20in%20your%20account.md#change-project-level-default-retention).

### How it works

LangSmith has two tiers of traces based on Data Retention with the following characteristics:

| | Base | Extended |
| - | - | - |
| **Price** | [See pricing page](https://www.langchain.com/pricing-langsmith) | [See pricing page](https://www.langchain.com/pricing-langsmith) |
| **Retention Period** | 14 days | 180 days |

> [!WARNING]
>
> Starting September 14, 2026, the maximum long-lived trace retention period for SaaS customers is changing to 180 days. Enterprise customers can still customize the extended retention period per workspace up to this new maximum. Changes apply to new traces only—existing traces are unaffected. See [Customize extended retention policy](../../../LangSmith%20setup/Govern/Data%20%26%20compliance/Data%20purging%20for%20compliance.md#customize-extended-retention-policy).

**Data deletion after retention ends**

After the specified retention period, traces are no longer accessible in the tracing project UI or via the API. All user data associated with the trace (e.g. inputs and outputs) is deleted from our internal systems shortly after. Some metadata associated with each trace may be retained indefinitely for analytics and billing purposes.

**Where the tier is set**

A default retention tier belongs to a tracing project. In an [agent-based workspace](../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), each of an agent's [environments](../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20environments.md) is its own tracing project, so the tier is set per environment: one agent can hold production traces at extended retention and development traces at base. To change the tier for a whole agent, set it on each environment. See [Change project-level default retention](../../../LangSmith%20setup/Account/Billing%20%26%20usage/Manage%20billing%20in%20your%20account.md#change-project-level-default-retention).

### Data retention auto-upgrades

> [!WARNING]
>
> Auto upgrades can have an impact on your bill. Please read this section carefully to fully understand your estimated LangSmith tracing costs.

Most traces use base retention. Some actions, such as online evaluators and automation rules, can extend a trace to a longer retention period at a higher cost. You control which actions extend retention.

When you use certain features with `base` tier traces, their data retention may be automatically upgraded to `extended` tier. This increases both the retention period and the cost of the trace.

Retention behavior by action:

* **Feedback via API or SDK**: Feedback is added to any run on the trace (or any trace in the thread) through an API or SDK call that explicitly passes `extend_trace_retention=true` (`extendTraceRetention: true` in TypeScript). For more information, see [Attach user feedback](../../../Test/Annotation%20Queues/Feedback/Log%20user%20feedback%20using%20the%20SDK.md). The LangSmith UI sends feedback and notes without extending retention.
* **Online evaluators**: An online evaluator scores the trace and its retention setting is enabled. Both trace-level and thread-level evaluators can opt out of this upgrade.
* **Automation rules**: An [automation rule](../../Observe/Automations/Set%20up%20automation%20rules.md#create-a-rule) with retention extension enabled matches any run within a trace. Matching a single run upgrades the entire trace, not just that run. A rule whose [item type](../../Observe/Automations/Set%20up%20automation%20rules.md#set-the-item-type-to-runs-or-threads) is **Threads** upgrades every trace in the matched thread, not only the most recent one.
* **Manual annotation queue adds** (no upgrade): Manually adding runs or threads to an [annotation queue](../../../Test/Annotation%20Queues/Use%20annotation%20queues.md#assign-runs-and-threads-to-a-single-run-queue) does not upgrade retention by default.

This change applies to new actions only. Traces that were already upgraded by a previous action keep their extended retention.

> [!NOTE]
>
> When you create or edit an online evaluator on a tracing project, you can opt out of upgrading the traces that evaluator scores, keeping them at base retention. This option is available only when the project's default retention is the base tier. For step-by-step instructions, see [Manage evaluator trace retention](../../../Test/Evaluators/Manage%20evaluators.md#manage-evaluator-trace-retention).

> [!NOTE]
>
> Retention extension is enabled by default for new online evaluators and automation rules. You can opt out when configuring each evaluator or rule.

**Why auto-upgrade traces?**

We have two reasons behind the auto-upgrade model for tracing:

1. We think that traces that match any of these conditions are fundamentally more interesting than other traces, and therefore it is good for users to be able to keep them around longer.
2. We philosophically want to charge customers an order of magnitude lower for traces that may not be interacted with meaningfully. We think auto-upgrades align our pricing model with the value that LangSmith brings, where only traces with meaningful interaction are charged at a higher rate.

If you have questions or concerns about our pricing model, please feel free to contact support via [support.langchain.com](https://support.langchain.com) and let us know your thoughts!

**How does data retention affect downstream features?**

The following features interact with retention differently:

* **Experiments**: Runs are created at extended retention by default.
* **Automation rules and evaluators**: Upgrade matching traces to extended retention when their retention setting is enabled. Thread-level rules and evaluators upgrade every trace in the matched thread.
* **UI feedback, notes, and annotation queues**: Leave a trace's retention tier unchanged.

Other features behave independently of a trace's retention tier:

* **Monitoring**: The monitoring tab will continue to work even after a base tier trace's data retention period ends. It is powered by trace metadata that exists for >30 days, meaning that your monitoring graphs will continue to stay accurate even on `base` tier traces.
* **Datasets**: Datasets have an indefinite data retention period. Restated differently, if you add a trace's inputs and outputs to a dataset, they will never be deleted. We suggest that if you are using LangSmith for data collection, you take advantage of the datasets feature.

### Billing model

**Billable metrics**

On your LangSmith invoice, you will see two metrics that we charge for:

* LangSmith Traces (Base Charge)
* LangSmith Traces (Extended Data Retention Upgrades).

The first metric includes all traces, regardless of tier. The second metric just counts the number of extended retention traces.

**Why measure all traces + upgrades instead of base and extended traces?**

A natural question to ask when considering our pricing is why not just show the number of `base` tier and `extended` tier traces directly on the invoice?

While we understand this would be more straightforward, it doesn't fit trace upgrades properly. Consider a `base` tier trace that was recorded on June 30, and upgraded to `extended` tier on July 3. The `base` tier trace occurred in the June billing period, but the upgrade occurred in the July billing period. Therefore, we need to be able to measure these two events independently to properly bill our customers.

If your trace was recorded as an extended retention trace, then the `base` and `extended` metrics will both be recorded with the same timestamp.

## Rate limits

LangSmith has rate limits which are designed to ensure the stability of the service for all users.

To ensure access and stability, LangSmith will respond with HTTP Status Code 429 indicating that rate or usage limits have been exceeded under the following circumstances:

### Temporary throughput limit over a 1 minute period at our application load balancer

This 429 is the result of exceeding a fixed number of API calls over a 1 minute window on a per service key or PAT basis. The start of the window will vary slightly—it is not guaranteed to start at the start of a clock minute—and may change depending on application deployment events.

After the max events are received we will respond with a 429 until 60 seconds from the start of the evaluation window has been reached and then the process repeats.

This 429 is thrown by our application load balancer and is a mechanism in place for all LangSmith users independent of plan tier to ensure continuity of service for all users.

| Method | Endpoints | Limit | Window |
| - | - | - | - |
| `DELETE` | `/sessions*` | 30 | 1 minute |
| `POST` OR `PATCH` | `/runs*` | 5000 | 1 minute |
| `GET` | `/runs/:id` | 30 | 1 minute |
| `POST` | `/feedbacks*` | 5000 | 1 minute |
| `*` | `*` | 2000 | 1 minute |

> [!NOTE]
>
> The LangSmith SDK takes steps to minimize the likelihood of reaching these limits on run-related endpoints by batching up to 100 runs from a single session ID into a single API call.

### Plan-level hourly trace event limit

This 429 is the result of reaching your maximum hourly events ingested and is evaluated in a fixed window starting at the beginning of each clock hour in UTC and resets at the top of each new hour.

An event in this context is the creation or update of a run. If a run is created and then subsequently updated in the same hourly window, that counts as 2 events against this limit.

This is thrown by our application and varies by plan tier, with organizations on our Startup/Plus and Enterprise plan tiers having higher hourly limits than our Free and Developer Plan Tiers which are designed for personal use.

| Plan | Limit | Window |
| - | - | - |
| Developer (no payment on file) | 50,000 events | 1 hour |
| Developer (with payment on file) | 250,000 events | 1 hour |
| Startup/Plus | 500,000 events | 1 hour |
| Enterprise | Custom | Custom |

### Plan-level hourly trace data ingest limit

This 429 is the result of reaching the maximum amount of data ingested across your trace inputs, outputs, and metadata and is evaluated in a fixed window starting at the beginning of each clock hour in UTC and resets at the top of each new hour.

Typically, inputs, outputs, and metadata are sent on both run creation and update events. If a run is created at 2.0MB and updated to 3.0MB in the same hourly window, that counts as 5.0MB of storage against this limit.

This is thrown by our application and varies by plan tier, with organizations on our Startup/Plus and Enterprise plan tiers having higher hourly limits than our Free and Developer Plan Tiers which are designed for personal use.

| Plan | Limit | Window |
| - | - | - |
| Developer (no payment on file) | 500MB | 1 hour |
| Developer (with payment on file) | 2.5GB | 1 hour |
| Startup/Plus | 5.0GB | 1 hour |
| Enterprise | Custom | Custom |

### Plan-level monthly unique traces limit

This 429 is the result of reaching your maximum monthly traces ingested and is evaluated in a fixed window starting at the beginning of each calendar month in UTC and resets at the beginning of each new month.

This is thrown by our application and applies only to the Developer Plan Tier when there is no payment method on file.

| Plan | Limit | Window |
| - | - | - |
| Developer (no payment on file) | 5,000 traces | 1 month |

### Self-configured monthly usage limits

This 429 is the result of reaching your usage limit as configured by your organization admin and is evaluated in a fixed window starting at the beginning of each calendar month in UTC and resets at the beginning of each new month.

This is thrown by our application and varies by organization based on their configured settings.

### Maximum runs per trace

Each trace is limited to a maximum of 25,000 runs. Once the trace reaches this limit, LangSmith will reject any additional runs that you send for that trace.

### Run query endpoint

LangSmith exposes two versions of the run query endpoint with different rate limit profiles.

**v2 (recommended):** `POST /v2/runs/query` ([`list_runs`](https://reference.langchain.com/python/langsmith/client/Client/list_runs) in Python, [`listRuns`](https://reference.langchain.com/javascript/langsmith/client/Client/listRuns) in JavaScript) is backed by SmithDB and has a flat per-API-key limit with no time-window tiers:

| **Limit** | **Window** |
| - | - |
| 300 requests | 10 seconds |

API key requests that set `sem_filter` (semantic search) are also limited to 10 requests per minute per workspace.

**v1:** `POST /runs/query` has per-tenant rate limits that vary based on query parameters:

| **Query type** | **Limit** | **Window** |
| - | - | - |
| Short time window (≤ 7 days) | 10 requests | 10 seconds |
| Large time window (> 7 days) | 3 requests | 10 seconds |
| Full-text search, short time window (≤ 7 days) | 3 requests | 10 seconds |
| Full-text search, large time window (> 7 days) | 1 request | 10 seconds |
| Select `child_run_ids`, short time window (≤ 7 days) | 3 requests | 10 seconds |
| Select `child_run_ids`, large time window (> 7 days) | 1 request | 10 seconds |

The time window is determined by `end_time - start_time`. If `end_time` is not provided, LangSmith will use the current time. Queries without a `start_time` are treated as large time window queries.

To avoid hitting v1 rate limits and reduce query time:

* **Set `start_time`**: omitting it triggers the large time window tier (3 requests per 10 seconds instead of 10). Use a window of 7 days or less when possible.
* **Use `select`**: by default all fields are returned. Specifying only the fields you need (e.g., `select=["inputs", "outputs"]`) substantially reduces response size and query time.
* **Set `limit`**: cap the number of results if you don't need to paginate through everything.
* **Avoid full-text search**: `filter='search("...")'` has the strictest rate limits; use structured filters (e.g., `eq()`, `has()`) when possible.
* **Avoid selecting `child_run_ids`**: this also triggers a stricter rate limit tier.

### Run stats endpoint

The [`POST /runs/stats`](../../Reference/LangSmith%20REST%20API/Tracing/Stats%20runs.md) endpoint has per-tenant rate limits that vary based on the query time window:

| **Query type** | **Limit** | **Window** |
| - | - | - |
| Short time window (≤ 14 days) | 10 requests | 10 seconds |
| Large time window (> 14 days and \< 90 days) | 3 requests | 10 seconds |
| Extra-large time window (≥ 90 days) or no `start_time` | 1 request | 10 seconds |

The time window is determined by `end_time - start_time`. If `end_time` is not provided, LangSmith uses the current time. Queries without a `start_time` are subject to the strictest limit.

In the GCP-hosted US region, API key requests to this endpoint are also limited to 1 request per 10 seconds per API key.

To avoid hitting rate limits:

* **Set `start_time`**: use a window of 14 days or less when possible.
* **Avoid open-ended queries**: always provide a `start_time` to stay in the less-restrictive tier.

### Workspace invite batch endpoint

Workspace invite batch requests are rate limited per workspace to reduce bulk invitation abuse.

The `POST /workspaces/current/members/batch` endpoint allows 2 requests per second per workspace. This limit applies to LangSmith Cloud only.

### Handle 429 responses in your application

Since some 429 responses are temporary and may succeed on a successive call, if you are directly calling the LangSmith API in your application we recommend implementing retry logic with exponential backoff and jitter.

For convenience, LangChain applications built with the LangSmith SDK has this capability built-in.

> [!NOTE]
>
> It is important to note that if you are saturating the endpoints for extended periods of time, retries may not be effective as your application will eventually run large enough backlogs to exhaust all retries.
>
> If that is the case, we would like to discuss your needs more specifically. Please contact support via [LangSmith Support](https://support.langchain.com) with details about your applications throughput needs and sample code and we can work with you to better understand whether the best approach is fixing a bug, changes to your application code, or a different LangSmith plan.

## Usage limits

LangSmith lets you configure usage limits on tracing. Note that these are *usage* limits, not *spend* limits, which mean they let you limit the quantity of occurrences of some event rather than the total amount you will spend.

LangSmith lets you set two different monthly limits, mirroring our Billable Metrics discussed in the aforementioned data retention guide:

* All traces limit
* Extended data retention traces limit

These let you limit the number of total traces, and extended data retention traces respectively.

### Properties of usage limiting

Usage limiting is approximate, meaning that we do not guarantee the exactness of the limit. In rare cases, there may be a small period of time where additional traces are processed above the limit threshold before usage limiting begins to apply.

### Side effects of extended data retention traces limit

The extended data retention traces limit has side effects. If the limit is already reached, LangSmith blocks actions that would create another extended-retention trace. For example, you can no longer:

1. run automation rules that extend trace retention
2. run evaluators that extend trace retention

Actions that do not change trace retention are not counted against the extended-retention trace limit. You can still submit feedback in the LangSmith UI, add runs or threads to annotation queues, and run automation rules or evaluators with retention extension disabled when the limit is reached.

### Update usage limits

Usage limits can be updated from the `Settings` page under `Usage and Billing`. Limit values are cached, so it may take a minute or two before the new limits apply.

## Related content

* Tutorial on how to [enforce spend limits](../../../LangSmith%20setup/Account/Billing%20%26%20usage/Manage%20billing%20in%20your%20account.md#enforce-spend-limits)
