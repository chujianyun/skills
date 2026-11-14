# Deploy the open-source paid media agent

> Deploy the open-source paid media agent to Slack as a Managed Deep Agents project for campaign analysis, scheduled reports, and reviewed changes.

The [paid media agent](https://github.com/langchain-ai/paid-media-agent) is an open-source agent for cross-channel ad analysis built with Managed Deep Agents. Your team asks questions in Slack, and the agent answers from connected Google Ads, Meta Ads, LinkedIn Ads, Reddit Ads, X Ads, and OpenAI Ads accounts.

It compares spend and conversions across accounts, explains performance shifts with supporting data, posts weekly and monthly reports, and prepares budget or campaign changes that stay paused until a reviewer approves them. A paid-media wiki covers attribution, platform differences, and budget decisions. Business context in the project supplies goals and conversion definitions.

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

## Deploy the agent

Before you start, make sure you have:

* A [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) account. Use a personal access token (an [API key](../../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md) that starts with `lsv2_pt_`), or sign in with your browser on the first deploy. A service key cannot set up the Slack app.
* A key for your model provider. On the [LLM Gateway](../../../../LLM%20Gateway/Get%20started/LLM%20Gateway.md), the agent uses your LangSmith key instead.
* A [Pipeboard](https://pipeboard.co/integrations) account for Google Ads, Meta Ads, LinkedIn Ads, TikTok Ads, Pinterest Ads, Snap Ads, Reddit Ads, and Google Analytics. Check [Pipeboard pricing](https://pipeboard.co/pricing) for plan limits. X Ads and OpenAI Ads use separate keys and stay read-only.
* Permission to install apps in your Slack workspace, or a workspace admin who can approve the agent's Slack app.

To deploy with a coding agent such as Claude Code, Codex, or Cursor, paste this prompt. It installs the agent, checks the setup, and asks before anything that bills or deploys.

Deploy the paid media agent with your coding agent

Deploy the open-source paid media agent to my Slack workspace with Managed Deep Agents.

1. Install it with `curl -fsSL https://raw.githubusercontent.com/langchain-ai/paid-media-agent/main/install.sh | bash`, then work in the `paid-media-agent` folder it creates.
2. Read `AGENTS.md` and follow the `paid-media-onboarding` skill.
3. Run `uv run paid-media-agent demo --with-proposal` to check the install.
4. Tell me which keys you need. I will type them myself with `uv run paid-media-agent config set <KEY>` in my terminal, or in the setup console (`uv run paid-media-agent setup`); never ask me to paste a key in chat.
5. Help me connect my ad accounts and write my business context.
6. Run `uv run paid-media-agent mda check` until it has no blockers. Then have me run the first deploy, `uv run paid-media-agent mda deploy --yes`, in my own terminal, since it sets up the Slack app.
7. When it is live, walk me through messaging the app in Slack and asking a first question.

To deploy it yourself:

**1. Install the project**

The installer installs uv if needed, then clones the repository and sets it up.

```bash
curl -fsSL https://raw.githubusercontent.com/langchain-ai/paid-media-agent/main/install.sh | bash
cd paid-media-agent
uv run paid-media-agent demo --with-proposal
```

The demo analyzes synthetic accounts and simulates a budget change, with no keys.

**2. Add your keys**

In Pipeboard, connect your ad platforms and create a token under **Settings** > **API Tokens**. Then save your keys:

```bash
uv run paid-media-agent config set LANGSMITH_API_KEY ANTHROPIC_API_KEY PIPEBOARD_API_TOKEN
```

The command asks for each key and keeps it hidden. The setup console, `uv run paid-media-agent setup`, does the same in your browser. On the [LLM Gateway](../../../../LLM%20Gateway/Get%20started/LLM%20Gateway.md), skip the provider key and run `uv run paid-media-agent config set PAID_MEDIA_MODEL=langsmith:anthropic/claude-opus-5-5` instead. To sign in with your browser instead of a LangSmith key, leave `LANGSMITH_API_KEY` out.

**3. Connect your ad accounts**

```bash
uv run paid-media-agent accounts discover --add
```

The command finds every ad account your Pipeboard token reaches and gives each one an alias. X Ads and OpenAI Ads use their own keys and stay read-only. Settings go to `.env` and account mappings to `config/accounts.toml`. Git ignores both files.

**4. Add your business context**

The agent reads your goals, conversion definitions, and campaign briefs from `workspace/skills/company-context/`. Start from the [template](https://github.com/langchain-ai/paid-media-agent/blob/main/docs/customization.md#business-context), or ask your coding agent to follow `.agents/skills/paid-media-org-onboarding/SKILL.md`. Add this context before the first real analysis.

**5. Deploy**

```bash
uv run paid-media-agent mda deploy --yes
```

The command checks the project first: it stops while a key is missing, and warns when the agent would answer from demo data. Then it deploys a copy of the project without your local working files. It also builds `sandbox/setup.sh`, which installs Python tools and PDF libraries, into a snapshot. The sandbox is small, so it needs no separate publish step.

Run the first deploy in your own terminal, since it sets up the Slack app. Choose the app that LangSmith manages. If the command prints a link, open it and approve the app for your workspace. The deploy waits until Slack reports the approval done. A workspace admin may need to approve the app.

**6. Ask a first question**

In Slack, find the app under **Apps** and send it a message, or invite it to a channel and mention it. Ask a question such as how much you spent in Europe versus the US last month. The agent reads the connected accounts, calculates the metrics in code, and answers in the thread with the caveats that change the conclusion.

![A Slack thread. A person asks the paid media agent how much was spent on Europe versus the US in August. The agent answers with totals and a per-platform split, then lists caveats: one platform has no country-level data, some countries fall outside both groups, and the split is by delivery geography.](../../../../../assets/images/be56f804fe2b-paid-media-agent-slack-thread.png)

Example Slack thread with a spend comparison and caveats.

## Customize the paid media agent

Most changes are edits to files in the repository. Common ones:

* **Business context**: Goals, conversion definitions, and campaign briefs live in `workspace/skills/company-context/`.
* **Reports**: The weekly and monthly reports run from `schedules/`, on Mondays and the first of each month at 13:00 UTC. Set `deliver_to` in a schedule to post the result to a Slack channel.
* **Report design**: Colors, typography, and layout live in `workspace/skills/report-design/DESIGN.md`. Ask your coding agent to follow `.agents/skills/paid-media-design/SKILL.md` to keep the renderer in step.
* **Slack app**: Set the name, description, and triggers in `channels/slack.py`.
* **Memory**: Memory is off by default. Add a `memory.py` to turn on [memory](../Agent%20capabilities/Add%20memory%20to%20Managed%20Deep%20Agents.md) when every caller may share what the agent learns.
* **Live changes**: Writes to ad accounts need a write policy from `config/write-policy.example.toml`, the [release checks](https://github.com/langchain-ai/paid-media-agent/blob/main/docs/operations/live-write-runbook.md), and an authorized reviewer. Pending proposals live in the deployment process, and the default serverless deployment can scale down and lose one before approval, so deploy with `--agent-server-type dedicated` before you turn on live changes.

To try a change and ship it, use these [`mda` commands](../Build%20and%20deploy/Managed%20Deep%20Agents%20CLI%20reference.md):

| Command | What it does |
| - | - |
| `uv run mda dev` | Runs the agent locally and opens it in [LangSmith Studio](../../../../Test/Test%20from%20Studio/LangSmith%20Studio.md) |
| `uv run paid-media-agent mda deploy --yes --name paid-media-agent-test` | Deploys a separate copy to test changes without touching the one your team uses |
| `uv run paid-media-agent mda deploy --yes` | Checks the project, then ships your changes to the deployment your team uses |
| `uv run mda logs` | Tails the logs of the deployed agent |
| `uv run mda build` | Compiles what would ship into `.mda/build/` without deploying |

For more information, see the [deploy guide](https://github.com/langchain-ai/paid-media-agent/blob/main/docs/deploy-mda.md), [Customization](https://github.com/langchain-ai/paid-media-agent/blob/main/docs/customization.md), and [Operations](https://github.com/langchain-ai/paid-media-agent/blob/main/OPERATIONS.md) in the repository.

## Explore the project

Each managed capability is a file or folder at the root of the repository:

| Path | In this agent | Learn more |
| - | - | - |
| `agent.py` | Builds the agent with `define_deep_agent` from one shared assembly of model, tools, middleware, and approval policy | [Agent definition](../Agent%20capabilities/Define%20a%20Managed%20Deep%20Agent.md) |
| `instructions.md` | The always-on prompt | [Instructions](../Agent%20capabilities/Add%20instructions%20to%20Managed%20Deep%20Agents.md) |
| `skills/` | Skills for analysis, reports, report design, and change proposals, plus a paid-media wiki, edited in `workspace/skills/` | [Skills](../Agent%20capabilities/Add%20skills%20to%20Managed%20Deep%20Agents.md) |
| `sandbox/` | Python 3.13 with ripgrep, jq, and PDF libraries, built by `mda deploy` | [Sandboxes](../Agent%20capabilities/Add%20a%20sandbox%20to%20Managed%20Deep%20Agents.md) |
| `channels/slack.py` | The managed Slack app for mentions, DMs, threads, and approval buttons | [Slack channel](../Agent%20capabilities/Channels/Connect%20a%20Managed%20Deep%20Agent%20to%20Slack.md) |
| `schedules/` | The weekly and monthly reports, and daily housekeeping | [Schedules](../Agent%20capabilities/Add%20schedules%20to%20Managed%20Deep%20Agents.md) |
| `identity.py` | Authenticates callers with a LangSmith API key | [Identity](../Agent%20capabilities/Add%20identity%20to%20Managed%20Deep%20Agents.md) |
| `src/paid_media_agent/` | Application code the agent entry imports, such as ad platform tools, metrics, and report rendering | [Tools](../Agent%20capabilities/Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md) |

## Architecture

Managed Deep Agents provides the Slack app, identity, schedules, and a sandbox per thread. The repository adds ad platform tools, analysis skills, and the approval policy.

![A Slack question or a weekly or monthly report reaches the main agent on Managed Deep Agents. The agent reads skills and a wiki, calls ad platform tools whose keys stay on the host, works in a sandbox per thread, and answers in the same Slack thread, where a proposed change waits for approval. Managed Deep Agents provides Slack, identity, schedules, durable runs, tracing, and mda deploy.](../../../../../assets/images/7f045c120bcb-paid-media-agent-architecture-light.png)

Request path from Slack or a schedule through the agent back to the thread.

The model decides what to investigate. Code calculates the metrics and checks report figures against the source data. Large tool results stay in files. The model reads summaries with the source, date window, and data quality flags.

A campaign change starts as a proposal: the before and after values, a reason, and a plan to check and undo it. The run pauses, and a reviewer on the approver list approves or rejects that exact proposal in Slack. An edit makes a new proposal that needs its own approval.

![A Slack approval card for a new Google Search campaign. It lists the campaign type, bidding strategy, a daily budget of 30 dollars, the market, and network settings, notes that the campaign starts paused, and ends with Approve all, Edit details, and Reject buttons.](../../../../../assets/images/d091646b111c-paid-media-agent-approval-card.png)

Slack approval card for a proposed campaign change.

After approval, the host checks every gate before it touches the account, makes one change, and reads it back to record a receipt. Live changes are off by default. To turn them on, follow the [live-write runbook](https://github.com/langchain-ai/paid-media-agent/blob/main/docs/operations/live-write-runbook.md).

![Five steps from left to right. Propose: before and after values, a reason, and how to check and undo it. Approve: a reviewer on the approver list approves the exact proposal in Slack. Check gates: kill switch, writes turned on, a released tool, and a signed approval; if any gate fails, the proposal is rejected and nothing changes. Execute: one change with the approved payload and no automatic retries. Verify: read the object back and record a receipt that is verified, failed, or unknown. An edit at the approval step loops back to a new proposal.](../../../../../assets/images/f1a7d46b26ad-paid-media-agent-approval-flow-light.png)

Approval path for a live write once an operator enables writes.

## See also

* [Paid media agent repository](https://github.com/langchain-ai/paid-media-agent)
* [Design agent template](Deploy%20the%20open-source%20design%20agent.md)
* [Managed Deep Agents project structure](../Get%20started/Managed%20Deep%20Agents%20project%20structure.md)
* [Deploy a Managed Deep Agents project](../Build%20and%20deploy/Deploy%20a%20Managed%20Deep%20Agent.md)
