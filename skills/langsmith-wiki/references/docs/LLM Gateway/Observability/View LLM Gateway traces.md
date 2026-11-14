# View LLM Gateway traces

> Find LLM Gateway traces, read their policy and cost metadata, triage policy violations in LangSmith Engine, and control who can see gateway traces.

> [!NOTE]
>
> The LLM Gateway is in [beta](../../LangSmith%20setup/Cloud/Reference/Release%20stages.md).

Each LLM Gateway request, including those that are blocked or fail, produces one LangSmith trace. The trace organizes provider attempts, policy checks, and LLM runs under one `gateway.request` root run. Policy violations surface in [LangSmith Engine](../../Engine/LangSmith%20Engine.md) for triage.

## Find gateway traces

Every gateway request is traced to a project named `gateway` in the [workspace](../../LangSmith%20setup/Govern/Organization/Overview.md#workspaces) associated with the caller's API key. To view gateway requests, go to **LLM Gateway** and select the **Traces** tab. The Simulator's **View trace** button opens its request in this tab. To see the requests behind one user's or API key's spend, select that user or key in the [**Usage** tab](Monitor%20LLM%20Gateway%20spend.md#analyze-the-chart-and-table), and click **View traces**. On the Developer plan, open the `gateway` tracing project in your workspace instead.

Trace content (request and response bodies) is off by default for all organizations, so gateway traces record only metadata, such as token counts, policy outcomes, and caller identity. These traces have `ls_metadata_only` set to `true`. Traces without content are not billed against your LangSmith trace quota. To store content, turn on **Trace content** in a [data policy](../Governance/Data%20policies.md#data-retention). A content-logged request counts once toward your plan's trace volume, regardless of how many provider attempts it makes.

> [!NOTE]
>
> Any user who can view runs in the workspace can view its gateway traces. To limit access, see [Restrict trace visibility](#restrict-trace-visibility).

## Read the trace tree

Expand `gateway.request` to inspect each attempt. Each attempt holds its own policy checks and provider call, so a request that falls back repeats the structure below once per attempt:

```text
gateway.request
├─ gateway.attempt #1
│  ├─ gateway.policy_check
│  │  └─ policy: <name>
│  ├─ gateway.data_policy
│  │  └─ policy: <name>
│  │     └─ rule: <rule_id>
│  └─ <provider LLM run>
└─ gateway.attempt #2
   └─ …
```

Gateway-specific keys appear under `gateway.` in each run's metadata, recorded as `langsmith.metadata.gateway.*` span attributes. The gateway sets these keys itself, so clients cannot override them through request headers. Each run below lists the keys most worth checking:

* **`gateway.request`**: The root run, which shows what happened to the request.
  * `gateway.request.outcome` is `success`, `upstream_error`, `blocked`, `rejected`, or `fallback_exhausted`.
  * `gateway.request.error_reason` explains a blocked or rejected request. A throttled request has outcome `blocked` and error reason `rate_limit`, not a separate `throttled` outcome.
  * `gateway.request.served_model` names the model that answered.
  * `gateway.request.id` correlates the root, attempt, policy, and provider runs for the request, including in bulk exports.
* **`gateway.attempt #N`**: A model candidate: the primary, a [fallback](../Models%20and%20reliability/Model%20fallbacks.md), or a `/routes` candidate. An attempt does not always make a provider call.
  * `gateway.attempt.outcome` records its result. A candidate skipped for cooldown has outcome `skipped` and no provider LLM run. `skipped` is an attempt-only outcome, not a request outcome.
  * `gateway.attempt.upstream_status_code` records the provider's status code when the call failed.
* **`gateway.policy_check`**: The check against [spend](../Governance/Spend%20policies.md), [rate limit](../Governance/Rate%20limit%20policies.md), [model access](../Governance/Model%20access%20policies.md), and routing policies. This run shows that the gateway evaluated policies for the attempt. To keep the trace uncluttered, only a policy that denied or throttled the request appears as a `policy: <name>` child run.
  * `gateway.policy.action`, on each `policy: <name>` run, records whether the policy denied or throttled the request.
  * `gateway.policy.matched_names` lists all matched policy names, including policies that did not deny or throttle the request.
* **`gateway.data_policy`**: The [data policy](../Governance/Data%20policies.md) scan for PII and secrets, which runs separately from the policy check. A data policy that redacted or blocked content appears as a `policy: <name>` child run, with a `rule: <rule_id>` run for each rule that matched.
  * `gateway.rule.matches`, on each `rule: <rule_id>` run, counts how many times the rule matched.
* **Provider LLM run**: The call to the provider, when one was made. Select it for token usage, cost, and, when trace content is on, the request and response.
  * `ls_model_name` and `ls_provider` identify the model and provider. These keys are on the provider LLM run, not the root run.
  * `gateway.credential_source` records which credential paid for the call, such as `byok` for the workspace's provider key or `credits` for [Gateway Credits](../Models%20and%20reliability/Gateway%20Credits.md).

> [!NOTE]
>
> A blocked attempt can have policy runs without a provider LLM run. A request rejected before any attempt has only the root run.

## Filter traces by caller

The root run and provider LLM runs record who made the request. The keys below are the most useful for finding one caller's traces:

* **`gateway.api_key_id`**: The API key that made the request.
* **`gateway.user_id`**: The user who made the request. Set only for personal access tokens, so service-key requests have no user.
* **`gateway.<name>`**: Each `X-Gateway-*` request header. For how names are normalized, see [Matchable headers](../Governance/Header-based%20policies.md#matchable-headers).

## Restrict trace visibility

Gateway traces are runs in a workspace project, so the same permissions govern them as other runs in the workspace. Any user with `runs:read` (and `projects:read` to see the project itself) on the workspace can view traces in that workspace's gateway project. The built-in Workspace Admin, Workspace Editor, and Workspace Viewer [roles](../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#workspace-roles) all include both permissions by default.

You have two options to limit access to gateway traces:

* **Separate workspaces** (works on any [plan](https://docs.langchain.com/langsmith/pricing-plans.md)): create one workspace with restricted membership and another for developer coding agents with broader membership. Each workspace has its own provider secrets and trace projects.
* **Project-level access policies** (requires an [Enterprise plan](https://docs.langchain.com/langsmith/pricing-plans.md)): write an [ABAC](../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Attribute-based%20access%20control.md) policy restricting `projects:read` and `runs:read` on the gateway project to specific users or roles.

## Triage policy violations

When a governance policy fires (such as when a spend limit is hit, PII is redacted, or a secret is caught), the event is recorded as metadata on the trace. These policy violations surface as [issues in LangSmith Engine](../../Engine/Find%20and%20fix%20your%20agent%27s%20issues%20with%20LangSmith%20Engine.md).

From an Engine issue, you can:

1. **See the violation:** find which policy fired and what it blocked or redacted.
2. **Click through to the trace:** see exactly what the agent was doing when the policy triggered.
3. **Diagnose the root cause:** such as a retry loop burning budget, a user pasting credentials into a prompt, or a legitimate workload that outgrew its cap.
4. **Take action:** update the agent's configuration, adjust the policy, or escalate.

## See also

* [Monitor LLM Gateway spend](Monitor%20LLM%20Gateway%20spend.md): track spend by user, API key, model, and provider.
* [Spend policies](../Governance/Spend%20policies.md): attach cost limits to API keys and users.
* [Data policies](../Governance/Data%20policies.md): configure data policies.
