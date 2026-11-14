# Validate fixes automatically

> Confirm that a LangSmith Engine issue reproduces on your deployment, and that Engine's fix resolves it, by replaying the issue's traces.

> [!NOTE]
>
> Fix validation is in private [beta](../LangSmith%20setup/Cloud/Reference/Release%20stages.md#beta). It is available only on LangSmith Cloud, for organizations where it has been enabled. It supports only agents running on [LangSmith Cloud deployments](../Deploy/Deploy%20to%20Cloud/Deployment%20guide/Create%20an%20Agent%20Server.md), not externally hosted agents. To request access, [join the waitlist](https://www.langchain.com/langsmith-engine-v2-new-feature-access).

Engine validates issues and fixes by running your agent:

* To validate an issue, Engine replays its linked traces against a configured baseline deployment to confirm that the issue reproduces.
* To verify a fix, Engine replays the same traces against a preview deployment built from Engine's proposed fix.

Engine records each validation as an [experiment](../Test/Get%20started/Evaluation%20concepts.md#experiment) on a dataset built from the issue's traces, so you can compare the baseline and the fix trace by trace.

## Set the baseline deployment

The baseline deployment is the deployment Engine replays issue traces against. [Red Teaming](Proactively%20identify%20issues%20with%20Red%20Teaming.md) sends its probes to the same deployment unless you [configure an external target](Proactively%20identify%20issues%20with%20Red%20Teaming.md#set-up-an-external-deployment). Fix validation still uses the baseline deployment. It must be a ready, non-preview [LangSmith Cloud deployment](../Deploy/Deploy%20to%20Cloud/Deployment%20guide/Create%20an%20Agent%20Server.md) of your agent in the same workspace, and selecting it requires `deployments:update` on that deployment.

To set the baseline deployment:

1. On the **Engine** page, select the tracing project, then click **Configure Engine**.
2. In the **Agent Server** section, find the **Baseline Agent Server** field.
3. Search for a deployment, or paste its LangSmith URL or deployment ID. Preview deployments and deployments that are not ready cannot be selected from the list. The baseline can be a production or staging deployment, but use staging when possible so validation does not exercise production credentials and services.
4. Click **Save**.

### Authenticate with your deployment

By default, Engine calls your deployment with a LangSmith credential, and the deployment sees the caller as a Studio user. Deployments that accept LangSmith platform authentication need no further setup.

If your deployment authenticates callers itself, give Engine the headers it expects:

1. In the **Agent Server** section, under **Agent Server authentication**, click **Add custom headers**.
2. Enter every header your deployment requires, then click **Save**.
3. In your deployment's authentication handler, map those headers to an identity with the least access validation needs.

Header values are encrypted and write-only: LangSmith shows only their names, so replacing them means entering every value again. Headers that LangSmith manages itself cannot be overridden. To go back to the default, click **Use platform authentication**.

> [!NOTE]
>
> Custom headers only decide whether your deployment accepts the request. They do not tell your agent that a run is a validation replay, which is a separate signal described in [Make replayed runs side-effect free](#make-replayed-runs-side-effect-free).

## Set up fix verification

To have Engine verify its own fixes against a preview deployment:

1. [Set the baseline deployment](#set-the-baseline-deployment).
2. [Connect the GitHub repository](Connect%20Engine%20to%20your%20repository.md) Engine should modify. Engine opens its fix as a pull request there. In the repository settings, select the base branch for Engine's fixes, or leave it blank to use the repository's default branch.
3. [Enable preview builds](../Deploy/Deploy%20to%20Cloud/Deployment%20guide/Preview%20builds.md#enable-preview-builds) on the baseline deployment, triggered by label. Use the following starting configuration:
   * Set **Preview base branch** to the same branch configured for Engine.
   * Select **Label only** and set **Trigger label** to `preview`. Engine applies this label to its fix pull request.
   * Set **Idle TTL** to 6 hours.
   * Set **Max concurrent previews** to 20.
4. In the **Agent Server** section of **Configure Engine**, select **Verify fixes with preview Agent Servers**.
5. Click **Save**.

With this setup, Engine applies the preview label, waits for LangSmith to build a temporary deployment from the proposed fix, replays the validation against it, and shows the verdict and replay traces on the issue.

> [!WARNING]
>
> Validation sends the inputs from an issue's traces to the baseline deployment, and to the preview deployment when it verifies a fix. Each replay creates a thread and a run on that deployment, and your agent can call its tools while it responds.
>
> [Preview deployments inherit the baseline deployment's secrets](../Deploy/Deploy%20to%20Cloud/Deployment%20guide/Preview%20builds.md#manage-secrets) when LangSmith creates them. Confirm that every inherited secret is appropriate for temporary deployments before enabling fix verification. Changes to the baseline's secrets do not propagate to previews that already exist.

## Prepare a deployment to test against

Engine confirms an issue by running your agent, so the deployment you select needs to be one you can exercise repeatedly without consequences.

### Use a deployment you can safely exercise

Choose a deployment that mirrors the configuration of the agent you want to test, but that is not the one serving your users. Point it at test credentials, test accounts, and non-production data stores for any service your agent writes to.

### Make replayed runs side-effect free

Engine sets `config.configurable.__engine_validation_replay__ = true` on every replay, so your agent can recognize one and respond more conservatively. At the HTTP boundary, validation requests also include `X-LangSmith-Source: engine`. Use the configurable marker in graph code and the header in request middleware.

Use the marker to skip or block tools whose effects leave your agent, such as sending email or messages, charging customers, filing tickets, writing to production data stores, scheduling work, and calling partner APIs.

> [accordion] Copy-paste allowlist middleware
>
> Add the following middleware to your agent project:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from __future__ import annotations
>
> from collections.abc import Awaitable, Callable, Collection, Mapping
> from typing import Any, cast
>
> from langchain.agents.middleware import AgentMiddleware
> from langchain.messages import ToolMessage
> from langchain.tools.tool_node import ToolCallRequest
> from langchain_core.runnables import RunnableConfig
> from langgraph.types import Command
>
> ENGINE_VALIDATION_CONFIG_KEY = "__engine_validation_replay__"
> LANGGRAPH_AUTH_USER_ID_CONFIG_KEY = "langgraph_auth_user_id"
>
>
> def _configurable(config: RunnableConfig | None) -> Mapping[str, object]:
>     configurable = (config or {}).get("configurable")
>     return configurable if isinstance(configurable, Mapping) else {}
>
>
> def is_engine_validation(config: RunnableConfig | None) -> bool:
>     """Return whether the caller requested reduced-privilege validation mode."""
>     return _configurable(config).get(ENGINE_VALIDATION_CONFIG_KEY) is True
>
>
> def is_trusted_engine_validation(
>     config: RunnableConfig | None,
>     *,
>     expected_user_id: str,
> ) -> bool:
>     """Verify the validation marker and authenticated Engine identity."""
>     configurable = _configurable(config)
>     return (
>         bool(expected_user_id)
>         and configurable.get(ENGINE_VALIDATION_CONFIG_KEY) is True
>         and configurable.get(LANGGRAPH_AUTH_USER_ID_CONFIG_KEY) == expected_user_id
>     )
>
>
> def _request_config(request: ToolCallRequest) -> RunnableConfig | None:
>     runtime = getattr(request, "runtime", None)
>     config = getattr(runtime, "config", None)
>     return cast(RunnableConfig, config) if isinstance(config, dict) else None
>
>
> class EngineValidationSafetyMiddleware(AgentMiddleware):
>     """Allow only explicitly safe tools during Engine validation."""
>
>     def __init__(self, *, safe_tools: Collection[str]) -> None:
>         self._safe_tools = frozenset(safe_tools)
>
>     def _rejection(self, request: ToolCallRequest) -> ToolMessage | None:
>         if not is_engine_validation(_request_config(request)):
>             return None
>         call = request.tool_call
>         name = call.get("name") or "tool"
>         if name in self._safe_tools:
>             return None
>         return ToolMessage(
>             content=f"{name} is blocked during Engine validation.",
>             tool_call_id=call["id"],
>             name=name,
>             status="error",
>         )
>
>     def wrap_tool_call(
>         self,
>         request: ToolCallRequest,
>         handler: Callable[[ToolCallRequest], ToolMessage | Command[Any]],
>     ) -> ToolMessage | Command[Any]:
>         rejection = self._rejection(request)
>         return rejection if rejection is not None else handler(request)
>
>     async def awrap_tool_call(
>         self,
>         request: ToolCallRequest,
>         handler: Callable[
>             [ToolCallRequest],
>             Awaitable[ToolMessage | Command[Any]],
>         ],
>     ) -> ToolMessage | Command[Any]:
>         rejection = self._rejection(request)
>         return rejection if rejection is not None else await handler(request)
> ```
>
> Register it on every run and allow only tools that are read-only and isolated:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langchain.agents import create_agent
>
> from engine_validation import EngineValidationSafetyMiddleware
>
> agent = create_agent(
>     model=model,
>     tools=[search_catalog, lookup_order, send_message],
>     middleware=[
>         EngineValidationSafetyMiddleware(
>             safe_tools={"search_catalog", "lookup_order"},
>         )
>     ],
> )
> ```
>
> Without the replay marker, the middleware passes tool calls through unchanged. During validation, it invokes only tools in `safe_tools` and returns an error `ToolMessage` for every other tool. An empty allowlist blocks all tools.

Only allow tools that are read-only and isolated. Do not allow tools that send messages, deliver notifications, schedule or queue work, persist data, or write to external systems.

> [!WARNING]
>
> Treat the marker and source header as untrusted hints that can only reduce what a run may do. Anything that can reach your deployment can set them, so never use them to grant access, skip authentication, or widen permissions.

#### Verify trusted Engine context

The replay marker is not proof of identity because any caller can set configurable values. If your deployment reconstructs user context or accesses protected data during validation, verify the authenticated Engine identity first:

```python
if is_trusted_engine_validation(
    config,
    expected_user_id=settings.engine_user_id,
):
    context = load_context_from_checkpoint()
```

Read identity and application context from authenticated runtime configuration and the copied checkpoint. Do not read them from replay input or metadata.

For deployments with [custom authentication](../Deploy/Agent%20Server/Auth%20%26%20access%20control/Add%20custom%20authentication.md), map the authenticated Engine service principal to `langgraph_auth_user_id` in your authentication handler before applying the same check. Authentication headers establish caller identity, while the replay marker activates the reduced-privilege tool policy.

### Expect a burst of traffic

Engine replays an issue's traces at the same time, so a validation can start up to five runs at once and each one runs to completion. Fix verification repeats the same set against the preview deployment. Confirm that the deployment's rate limits, quotas, and any downstream service it calls tolerate that burst.

### Keep the deployment available

Engine can only replay against a ready, non-preview deployment, and it records the deployment and revision that produced each result. Keep the deployment running while validation is in progress, and expect a result to describe the revision that was active when Engine tested it.

## Test an issue

When a baseline deployment is set, Engine validates each new issue automatically when it creates the issue. To validate an issue again, open it and click **Test issue**.

**Test issue** is unavailable when no baseline deployment is set, when the issue has no linked traces, or when the monthly LSU spend limit is reached.

For each validation, Engine:

1. Selects up to five distinct traces linked to the issue, in the order they were linked.
2. Replays each trace's input against the baseline deployment. For a trace from a multi-turn thread, Engine includes the earlier turns of the conversation, so a follow-up failure is judged in the same context.
3. Judges whether each replay shows the issue's reported behavior again. Each trace is **Reproduced**, **Not reproduced**, or **Inconclusive**.

The issue as a whole is reproduced when at least one trace reproduces. It is not reproduced only when every replay completed without the reported behavior. Otherwise, the result is inconclusive. When validation does not reproduce an open issue, Engine closes the issue.

## Verify a fix

When **Verify fixes with preview Agent Servers** is selected, Engine verifies each fix it generates:

1. When a fix run completes, Engine opens a pull request for the fix if one is not already open, then adds the preview build label to it.
2. LangSmith builds a preview deployment from the pull request.
3. When the preview revision is live, Engine replays the traces from the issue's validation against the preview deployment.
4. If the issue still occurs on the preview, Engine revises the fix on the same pull request and verifies it again, for up to three attempts in total.

## Read a validation result

Each issue reports a baseline result and, once a fix exists, a verification result.

The baseline result answers whether the issue still happens on your deployment:

| Status | Meaning |
| - | - |
| **Awaiting test** | Engine has not recorded a baseline result yet. |
| **Reproduced** | At least one replay showed the reported behavior again. |
| **Not reproduced** | Every replay finished without the reported behavior, so Engine closes an open issue. |
| **Inconclusive** | Engine could not judge the replays confidently. |
| **Error** | Validation could not complete. |

The verification result answers whether Engine's fix resolved it:

| Status | Meaning |
| - | - |
| **Not run** | The issue did not reproduce, so there is nothing to verify. |
| **Generating fix** or **Awaiting fix** | Engine is still producing a fix to verify. |
| **Awaiting preview** or **Running** | A preview deployment is building, or replays are in progress. |
| **Verified** | The issue no longer occurred on the fix's preview deployment. |
| **Not fixed** | The issue still occurred, so Engine revises the fix and tries again. |
| **Inconclusive**, **Timed out**, or **Error** | Engine could not establish a verdict for this attempt. |

> [!WARNING]
>
> **Inconclusive** means Engine could not gather trustworthy evidence, not that the issue is absent or fixed. Treat it as a signal to re-test rather than as a passing result.

## Review validation experiments

Engine stores each issue's validation evidence in your workspace:

* **Dataset**: One per issue, described as `Engine validation evidence`, with one example per replayed trace.
* **Baseline experiment**: The replays against the baseline deployment.
* **Fix experiment**: The replays against a fix's preview deployment, one experiment per verification attempt.

Engine records its verdict on each conclusive replay as feedback with the key `engine_issue_validation`. The value is `reproduced` or `not_reproduced`, and the feedback comment explains the verdict.

When Engine verifies a fix against a preview deployment, the issue's **Evidence** section shows the overall verdict and one row per trace:

* **Flagged traces**: What Engine saw in the original trace. Click **Original trace** to open it.
* **Reproduced on prod**: The baseline result, **Reproduced**, **Not reproduced**, or **Inconclusive**. Click **Repro trace** to open the replay.
* **After PR #\<number>**: The result on the fix's preview, **Fix verified**, **Recurred**, or **Inconclusive**. Click the trace link to open the replay.

Each column header counts how many traces reproduced on the baseline or were resolved by the fix. Click **View Experiment** to open the baseline and fix experiments side by side in the dataset's comparison view. For more information, see [Compare experiment results](../Test/Datasets%20%26%20Experiments/Analyze%20experiment%20results/How%20to%20compare%20experiment%20results.md).

Until fix verification runs, the issue shows a validation summary instead: the baseline result, the fix's verification status, and links to each replayed example.

## Troubleshoot validation

If an issue stays on **Awaiting test**, or a result comes back inconclusive, check the following before testing it again:

* **The baseline deployment**: Confirm it is still ready, is not a preview, and is in the same workspace as the tracing project.
* **Authentication**: If your deployment authenticates callers itself, confirm the saved headers are current. Replacing a credential requires re-entering every header value.
* **The replays themselves**: Open the replayed runs from the issue's **Evidence** section or validation summary and read what your agent returned.
* **Deployment limits**: Look for rate limiting, quota exhaustion, or timeouts caused by the concurrent replays, and for very large responses, which Engine may not be able to judge.
* **Restricted tools**: If your agent blocks tools during a replay, confirm the stubbed tools still return a usable result rather than an error that ends the run.

After correcting the deployment or its settings, open the issue and click **Test issue** to run validation again.

## See also

* [Find and fix issues](Find%20and%20fix%20your%20agent%27s%20issues%20with%20LangSmith%20Engine.md): Review the issues Engine validates.
* [Red Teaming](Proactively%20identify%20issues%20with%20Red%20Teaming.md): Probe the same baseline deployment with synthetic requests.
* [Preview builds](../Deploy/Deploy%20to%20Cloud/Deployment%20guide/Preview%20builds.md): Create the preview deployments Engine verifies fixes against.
* [Compare experiment results](../Test/Datasets%20%26%20Experiments/Analyze%20experiment%20results/How%20to%20compare%20experiment%20results.md): Compare the baseline and fix experiments side by side.
* [Engine security](LangSmith%20Engine%20security.md): Review how Engine accesses your traces, deployments, and repositories.
