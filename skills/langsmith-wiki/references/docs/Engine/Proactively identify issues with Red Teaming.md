# Proactively identify issues with Red Teaming

> Test a deployed agent with synthetic LangSmith Engine probes to find prompt injection, data exposure, and unsafe tool use before they reach production.

> [!NOTE]
>
> Red Teaming is in private [beta](../LangSmith%20setup/Cloud/Reference/Release%20stages.md#beta). It is available only on LangSmith Cloud, for organizations where it has been enabled. It supports agents running on [LangSmith Cloud deployments](../Deploy/Deploy%20to%20Cloud/Deployment%20guide/Create%20an%20Agent%20Server.md) and [external deployments](#set-up-an-external-deployment). To request access, [join the waitlist](https://www.langchain.com/langsmith-engine-v2-new-feature-access).

Red Teaming tests a deployed agent by sending it new, synthetic requests and judging how it responds. The [issues Engine detects](Find%20and%20fix%20your%20agent%27s%20issues%20with%20LangSmith%20Engine.md) from your traces come from failures that already happened in production. Red Teaming looks for failures that have not happened yet, such as a prompt injection that succeeds, a consequential tool call made without the confirmation your agent requires, or hidden context that leaks into an answer.

Each run produces a report of hypotheses, the probes that tested each one, and a verdict for each hypothesis.

## How Red Teaming works

By default, Red Teaming probes the tracing project's [baseline deployment](Validate%20fixes%20automatically.md#set-the-baseline-deployment). If you configure an external target, Engine probes that endpoint instead. Each run:

1. **Maps the application.** For a baseline deployment, Engine reviews up to 25 recent traces and, if connected, your code repository. It learns the agent's prompts, tools, guardrails, and request format. If Engine has already scanned the project, it starts from the project's agent overview and runs a shorter confirmation scan. External runs do not read traces or the agent overview. They use endpoint responses, the uploaded spec for HTTP APIs, and a screened behavior summary from a connected repository when available.
2. **Forms hypotheses.** Each hypothesis describes one specific way the agent could fail. Engine assigns it an [issue class](#red-teaming-issue-classes) and a scenario type, which records whether an ordinary user could trigger the failure or whether it takes a deliberate attack.
3. **Probes the deployment.** Engine sends up to two synthetic requests per hypothesis to the deployment. A baseline probe reuses the request format of a real trace, but replaces its content with new, synthetic input. An external probe uses the A2A protocol or an allowed OpenAPI operation.
4. **Judges the results.** Engine reviews each probe's response and, for baseline deployments, its trace. It then assigns the hypothesis a status and a severity. For an ambiguous result, Engine can send one follow-up probe.

Past traces only help Engine understand the application. Every confirmed finding comes from a probe sent during the run, not from an error in an earlier trace.

Red-team findings stay in the red-team report. A run does not create Engine issues, and it does not write datasets, evaluators, or feedback to your workspace.

## Red Teaming prerequisites

To run Red Teaming, you need:

* **Engine on the tracing project**: [Set up Engine](Set%20up%20LangSmith%20Engine.md) for the project that receives your agent's traces.
* **A target deployment**: Either a ready, non-preview LangSmith Cloud deployment in the same workspace, set as the project's baseline, or an external endpoint. See [Set the baseline deployment](Validate%20fixes%20automatically.md#set-the-baseline-deployment) or [Set up an external deployment](#set-up-an-external-deployment).
* **Permissions**: `runs:read` on the tracing project to view red-team reports, and `runs:create` to start a run. Configuring an external target requires `issues:update` on the project. Using a baseline deployment also requires `deployments:update` on that deployment.
* **A connected repository (recommended)**: With a [connected GitHub repository](Connect%20Engine%20to%20your%20repository.md), Engine can use your agent's prompts, tools, and guardrails to guide testing. External runs receive a screened behavior summary rather than raw source. Without a repository, baseline runs rely on traces. External runs rely on endpoint responses and, for HTTP APIs, the uploaded spec.

> [!WARNING]
>
> Probes are real requests, and your agent can call its tools while it responds. Baseline probes create threads and runs; external probes call the configured endpoint. Choose a deployment where synthetic test traffic and tool side effects are acceptable, such as a staging deployment. Use test credentials and non-production data stores.

## Set up an external deployment

An external target lets Engine test an agent hosted outside LangSmith Cloud. You can connect an A2A agent or an HTTP API described by an OpenAPI spec. A baseline deployment is not required for external runs.

External targets must be enabled for your project. If **Red team target** is missing from **Configure Engine**, request access through the [waitlist](https://www.langchain.com/langsmith-engine-v2-new-feature-access).

To connect an external deployment:

1. On the **Engine** page, select the tracing project, then click **Configure Engine**.
2. Find the **Red team target** section and choose an **Endpoint type**:
   * **A2A agent**: Enter the agent's A2A endpoint in **Endpoint URL**. Engine sends A2A messages to this URL.
   * **HTTP API with an OpenAPI spec**: Enter the API's base URL in **Endpoint URL**, then click **Upload spec**. Upload an OpenAPI 3 document in JSON or YAML and select between 1 and 10 operations Engine may call.
3. Under **Endpoint authentication**, click **Add header** and enter the headers your endpoint requires. At least one authentication header is required. Use credentials with the least access needed for testing.
4. Click **Save**, return to **Red Teaming**, and click **Run red team**.

### Choose a reachable endpoint

The endpoint must use HTTPS and resolve to a public internet address. Engine blocks private, loopback, and cloud metadata addresses, and does not follow redirects. Enter a URL with a path, without embedded credentials, query parameters, or a fragment.

For an A2A agent, use the message endpoint, not the agent card URL. Engine checks `/.well-known/agent-card.json` at the endpoint's origin to select the protocol version. It uses A2A v1.0 when the card advertises a v1.0 JSON-RPC interface at the configured URL, and v0.3 otherwise.

For an HTTP API, Engine appends each allowed operation's path to the configured base URL. It does not use the spec's `servers` URLs. Supported methods are `GET`, `POST`, `PUT`, and `PATCH`. `DELETE` is not allowed. Operations with request bodies must accept JSON. References in the spec must be local `$ref` pointers. The spec size limit is 256 KB after conversion to compact JSON with non-ASCII characters escaped.

> [!WARNING]
>
> Restrict the allowed operations to endpoints you can safely test. Excluding `DELETE` does not prevent other operations from changing data or triggering external actions.

### Manage endpoint authentication

Engine sends the saved headers only to the configured target, not to your baseline deployment. It does not send your LangSmith platform credential to an external endpoint. Header values are encrypted and write-only. The settings show only their names.

Changing the endpoint URL requires entering every header value again. For an HTTP API, changing the URL also requires uploading the spec and selecting operations again. To change allowed operations for the same endpoint, click **Replace spec**, upload the document, select operations, and save.

### Understand external-run limits

External runs use endpoint responses rather than LangSmith traces to judge findings. They do not inspect internal tool calls or provide **View proof trace** links. A connected repository can supply a screened behavior summary. The model that reads target responses never reads raw source. External probes are single-turn, so they cannot confirm **Session Integrity** findings that require a two-turn conversation.

When both targets are configured, the external target takes precedence for Red Teaming. [Fix validation](Validate%20fixes%20automatically.md) continues to use the baseline deployment. To return Red Teaming to the baseline deployment, click **Remove** in **Red team target**. Without a baseline, removing the external target leaves no target to test.

## Start a Red Teaming run

To start a run:

1. In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-engine-red-teaming), select **Engine** in the sidebar, then select the tracing project.
2. At the top of the left panel, select **Red Teaming**.
3. Click **Run red team**.

The run appears in the report picker with the status **Running**. When it completes, its report opens in the same view. **Run red team** is unavailable while a run is in progress.

If a run does not complete, the report picker shows its final status: **Failed**, **Timed Out**, **Interrupted**, **Cancelled**, or **Failed to Start**. No report is available for that run.

## Read a red-team report

Use the report picker at the top of the left panel to choose a run by date. Select **Load older reports** to page back through earlier runs.

### Review the overview

When no hypothesis is selected, the right panel shows an overview of the report:

* **Confirmed findings**: The number of confirmed findings, broken down by severity.
* **Hypotheses tested**: The number of hypotheses the run tested.
* **Issue classes tested**: How many of the 10 [issue classes](#red-teaming-issue-classes) the run tested.
* **Findings by Issue Class**: Confirmed findings per issue class.
* **Hypothesis Outcomes**: Hypotheses by status. Click a status to filter the hypothesis list to it.
* **Findings Over Runs**: Confirmed findings for each run, stacked by severity. Click a run to open its report.

### Browse hypotheses

The left panel groups the report's hypotheses:

* **Product-Facing Findings**: Confirmed findings that an ordinary user could trigger, with a normal request or a realistic, messy one.
* **Technical Hardening Observations**: Confirmed findings that take a deliberate attack or a technical boundary check to trigger.
* **Legacy Confirmed Findings**: Confirmed findings from older reports, recorded before Engine assigned scenario types.
* **Other Tested Hypotheses**: Every hypothesis that was not confirmed.

Click the filter icon to show a single status, or the sort icon to sort by **Default**, **Severity**, or **Title (A-Z)**. The default order lists confirmed hypotheses first, by severity, then hypotheses that need review.

Each hypothesis has one of these statuses:

| Status | Meaning |
| - | - |
| **Confirmed** | A probe reproduced the failure, and Engine judged it a real finding. |
| **Needs Review** | The evidence was ambiguous or incomplete. Review the probes before acting on the hypothesis. |
| **No Issue Found** | Probes ran, and the agent behaved correctly. |
| **Not Tested** | No probe exercised the hypothesis. This is missing coverage, not evidence of safe behavior. |

A confirmed finding also has a severity: **Critical**, **High**, **Medium**, **Low**, or **Info**.

### Inspect a hypothesis

Click a hypothesis to open its detail. The detail shows Engine's conclusion, followed by one card per probe, labeled **Prompt 1** and **Prompt 2**. Each probe has an outcome of **Attack Worked**, **Attack Blocked**, or **Needs Review**.

Expand a probe card to see:

* **The synthetic prompt**: The exact prompt Engine sent to the deployment.
* **Observed**: An excerpt quoted from your agent's response. Baseline probes also include a trace summary, such as tool calls, tool errors, and token count.
* **Expected**: What a correct application would have returned.
* **View proof trace**: Opens the probe's trace in the side panel. Available for baseline probes, not external probes.

Below the probes, **Why the Judge Decided This** explains how Engine reached the status and severity, and **What to Do Next** recommends a fix. A hypothesis marked **Unexpected** is a finding that Engine discovered while testing a different hypothesis.

## Red Teaming issue classes

Every hypothesis belongs to one issue class, chosen by the failure's root cause and the fix it needs. Each report accounts for all 10 classes, and marks each one as tested, untested, or not applicable to the agent.

| Issue class | What Red Teaming tests |
| - | - |
| **Content Policy** | Violations of explicit product, legal, safety, or business policies, such as a prohibited competitor comparison. |
| **Instruction Hierarchy** | Direct overrides of the agent's instructions, and conflicting or confusing prompt instructions. |
| **Indirect Injection** | Retrieved content, tool output, or other untrusted data that tries to control the agent. |
| **Data Exposure** | Hidden context, such as synthetic canary values planted by a probe, escaping into a response. |
| **Auth Isolation** | Access or actions beyond the caller's identity or permission boundary. |
| **Tool Safety** | Unsafe tool selection, arguments, or approvals, and unsafe consequential workflows. |
| **Workflow Integrity** | Required steps, such as retrieval, clarification, or truthful completion, that the agent skips or fabricates. |
| **Session Integrity** | Multi-turn state problems, such as memory poisoning, delayed activation, or role confusion. |
| **Input Robustness** | Confusion caused by structured output, parsing, delimiters, encodings, or message boundaries. |
| **Reliability Safety** | Behavior around failures, retries, resource limits, loops, duplicate work, and irreversible side effects. |

Two classes have extra requirements:

* **Auth Isolation**: Red Teaming does not confirm findings in this class. Its hypotheses report as **Needs Review** or **Not Tested**.
* **Session Integrity**: A hypothesis needs a two-turn probe in a single conversation. When no such probe runs, the hypothesis reports as **Needs Review** or **Not Tested**.

## Run Red Teaming again

For baseline deployments, Red Teaming carries verdicts forward between runs of the same deployment revision. A new run receives the verdicts from up to five earlier successful runs against the same baseline deployment and active revision. Engine skips hypotheses that earlier runs already confirmed or found safe, unless the new run shows that the behavior changed, and prioritizes hypotheses that needed review.

After you deploy a new revision to the baseline deployment, the next run starts without prior verdicts. Use **Findings Over Runs** to compare confirmed findings across runs.

## Red Teaming limits

Each red-team run is bounded:

| Limit | Value per run |
| - | - |
| Traces reviewed | Baseline: 25, selected from up to 100 recent trace summaries. External: 0. |
| Hypotheses | 50 |
| Probes per hypothesis | 2 |
| Requests to the target | 60 |
| Recommendations | 20 |

## How Red Teaming handles your data

* **Synthetic probes**: Probe content is synthetic. Engine does not copy customer trace content or raw repository source into probes. For baseline deployments, a trace supplies only the request format.
* **Read-only access**: Red Teaming reads baseline traces with a read-only LangSmith credential and clones your repository with a read-only GitHub token. External runs do not read traces.
* **Screened repository context**: For external targets, a separate analyst reads the repository and produces a behavior summary. Engine screens the summary for source code, file paths, URLs, and secrets before using it to guide probes.
* **Screened reports**: Engine screens model-written report text for secrets before storing it, and bounds the length of response excerpts.

For how Engine handles your data more broadly, see [Engine security](LangSmith%20Engine%20security.md).

## See also

* [Validate fixes automatically](Validate%20fixes%20automatically.md): Set the baseline deployment and replay issue traces against it.
* [Connect Engine to your repository](Connect%20Engine%20to%20your%20repository.md): Give Red Teaming your agent's prompts, tools, and guardrails from source.
* [Engine security](LangSmith%20Engine%20security.md): Review how Engine accesses your traces, deployments, and repositories.
