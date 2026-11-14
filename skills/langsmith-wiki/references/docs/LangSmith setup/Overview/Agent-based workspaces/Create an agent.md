# Create an agent

> Register an agent before tracing, choose its identifier, and configure an environment with the UI, Python SDK, or REST API.

Creating an [agent](Agent%20Registry.md#agent) in LangSmith gives it an identifier and [environments](Agent%20environments.md) for its traces. Create it once, then use its identifier and an environment to send traces from your code.

If your agent runs outside LangSmith, first create its record in LangSmith using the UI, SDK, or API. This record organizes its traces. Your code still runs where you host it. Framework functions such as LangChain `create_agent` build the agent that runs in your code. They do not create its LangSmith record.

> [!NOTE]
>
> Agent-based workspaces are available on [LangSmith Cloud](../../Cloud/Cloud%20%28SaaS%29.md). They are not available on [self-hosted](../../Self-hosted/Self-hosted%20LangSmith.md) LangSmith. To check whether your workspace is agent-based, look at the control at the top left. In an agent-based workspace, it is a workspace switcher that names your workspace. In a [project-based](../../../Monitor/Trace/Observability%20concepts.md#tracing-projects) workspace, it shows the LangSmith logo.

## Compare the four routes

An agent can be created in four ways, which differ in how the identifier is set and which environments the agent starts with:

| Method | What you do | Identifier | Environments at creation |
| - | - | - | - |
| [Studio](../../../No-code%20agents/Studio/Build%20an%20agent%20with%20LangSmith%20Studio.md) | Describe an agent and let LangSmith Chat build it inside LangSmith | Generated for you | Production alone |
| [UI](#name-an-agent-traced-from-outside-langsmith) | Create an agent record by entering its name and ID in LangSmith | You set it | All four |
| [SDK or API](#create-an-agent-programmatically) | Create an agent record with an SDK call or API request | You set it | All four |
| [Deployment](Deploy%20to%20an%20agent%20environment.md) | Deploy your agent code to LangSmith | The agent ID you pass, or derived from the deployment name | All four |

Not every agent can have a [deployment](../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md). Deploying agent code creates the agent with a deployment from the start. An agent created with the SDK or API, or by the [**Connect an agent**](#name-an-agent-traced-from-outside-langsmith) dialog, has no deployment at first, but you can [deploy to it](Deploy%20to%20an%20agent%20environment.md) later. An agent built in Studio cannot have a deployment, because it runs on a Studio runtime. To inspect a deployed agent's Agent Servers and environments, select **Agent Server** in its Overview header.

An agent built in Studio gains its other environments the first time a trace is addressed to one. For what the four are, see [Agent environments](Agent%20environments.md#environment-names).

When LangSmith builds or deploys an agent through these flows, it handles registration. Reuse that agent for tracing. Do not create a separate external agent for the same deployment.

## Identifier rules

An identifier is 1 to 63 characters, using lowercase letters, digits, and hyphens. It must start with a letter and end with a letter or digit, so `support-agent` and `billing-v2` are valid. Anything else is rejected.

The rules apply wherever you supply the value: in the **Agent ID** field, in SDK and API creation requests, and in the agent ID you deploy to. Studio generates an identifier instead. A deployment without an agent ID derives one from the deployment name, appending a suffix when that value is already taken, so a deployed agent can end up with an identifier close to the deployment name rather than equal to it.

An identifier cannot be changed after the agent is created. The display name can. For which value is which, see [Identifiers and display names](Agent%20Registry.md#identifiers-and-display-names).

## Start from the new agent menu

Two controls open the new agent menu: **+ Agent** on the agent list, and the **+** button beside the search box in the agent switcher, which shows a **New agent** tooltip on hover. The switcher button appears only for users with the `projects:create` permission. The menu hands off to three flows:

* **Build** > **Without code**: Opens Studio, where you describe the agent and LangSmith Chat drafts it. See [Build an agent with LangSmith Studio](../../../No-code%20agents/Studio/Build%20an%20agent%20with%20LangSmith%20Studio.md).
* **Build** > **With code**: Opens the **Build with code** pane. **Hosted by LangSmith** covers [Managed Deep Agents](../../../Build/Python/Deep%20Agents/Deployment/Managed%20Deep%20Agents.md), which creates the agent when you deploy and requires a paid plan. **Host it yourself** covers building with the [open source frameworks](https://docs.langchain.com/oss/python/langchain/overview.md), then creating the agent's LangSmith record using the UI or API below.
* **Connect** > **Connect an existing agent**: Opens the **Connect an agent** dialog, where you name an agent traced from outside LangSmith. See the next section.

## Name an agent traced from outside LangSmith

Creating an external agent in the UI requires the `projects:create` permission. To register it, open the **Connect an agent** dialog from either of two places:

* **Connect an existing agent** in the new agent menu.
* **Connect an agent**, below the agent list on Tracing when no agent is selected.

The dialog takes an **Agent name** and, in its own field, an **Agent ID**, with a note that the ID is used in URLs and API calls and cannot be changed later. Click **Connect agent**. LangSmith creates the agent and opens it. From the new agent menu, it opens the agent's tracing page. To send the first traces, see the [tracing quickstart](../../../Monitor/Trace/Tracing%20quickstart.md).

After creation, configure your code to [send traces to the agent and environment](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md). For integrations that require `project_name`, use the [compatibility configuration](#use-an-environment-project).

## Create an agent programmatically

The agent creation API creates an agent record in LangSmith with all four environments. Call it once before sending traces, rather than each time your agent runs.

Use a [personal access token or service key](../../Account/Create%20an%20account%20and%20API%20key.md) with the [`projects:create` permission](../../Govern/Users%20%26%20access%20control/Organization%20and%20workspace%20operations%20reference.md#projects). A tracing key cannot call the agent creation API. After creating the agent, your code can use a tracing key to submit traces.

Set `LANGSMITH_API_KEY` to the setup credential. Set `LANGSMITH_WORKSPACE_ID` to the target workspace ID, and `LANGSMITH_ENDPOINT` to your [region's API URL](../../Account/Create%20an%20account%20and%20API%20key.md#configure-the-sdk).

> [tab] Python
>
> Install LangSmith v0.14.12 or later:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> pip install -U "langsmith>=0.14.12"
> ```
>
> Create the agent and print its identifier:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langsmith import Client
>
> client = Client()
> agent = client.agents.create(
>     id="support-agent",
>     name="Support agent",
>     source_type="EXTERNAL",
> )
> print(agent.id)  # Use as LANGSMITH_AGENT_ID
> ```

> [tab] REST
>
> Use the REST API from any language to register the agent. Include `source_type: "EXTERNAL"`:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --fail-with-body --request POST "$LANGSMITH_ENDPOINT/api/v1/agents" \
>   --header "x-api-key: $LANGSMITH_API_KEY" \
>   --header "x-tenant-id: $LANGSMITH_WORKSPACE_ID" \
>   --header "Content-Type: application/json" \
>   --data '{"id":"support-agent","name":"Support agent","source_type":"EXTERNAL"}'
> ```

`id` is the immutable agent identifier. `name` is its editable display name. The creation response includes `environments`, with each environment's `tracer_session_name` and `tracer_session_id`.

If the identifier already exists, creation returns `409`. Reuse the existing agent after checking its identity, or choose another identifier. Keep creation in your setup step. Retrieve an existing agent when your code needs its configuration.

## Configure tracing for the agent

Use the agent identifier and environment as the tracing destination:

```bash
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY="<API_KEY>"
export LANGSMITH_AGENT_ID="support-agent"
export LANGSMITH_AGENT_ENVIRONMENT="local"
```

Use the identifier returned by creation, not the display name. Remove legacy destination variables (`LANGSMITH_PROJECT`, `LANGCHAIN_PROJECT`, and `LANGCHAIN_SESSION`) from the environment where your code runs. For SDK versions and code-based configuration, see [Log traces to an agent](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md).

## Configure integrations that require a project name

Some integrations still require a `project_name` or `LANGSMITH_PROJECT` setting. For these integrations, use the selected agent environment's `tracer_session_name`. This is a compatibility value returned by LangSmith, not another resource to create.

Retrieve the agent with a credential that can read its environments. With the Python SDK:

```python
from langsmith import Client

client = Client()
agent = client.agents.retrieve("support-agent")
production = next(env for env in agent.environments if env.environment == "PRODUCTION")
print(production.tracer_session_name)  # Use as LANGSMITH_PROJECT
print(production.tracer_session_id)  # Use with APIs that take a project ID
```

With REST, call `GET /api/v1/agents/support-agent` using the same authentication headers as the creation request. In `environments`, select `PRODUCTION`, `STAGING`, `DEVELOPMENT`, or `LOCAL` and read its `tracer_session_name` or `tracer_session_id`.

Copy the selected environment's `tracer_session_name` into your integration's destination setting:

```bash
export LANGSMITH_PROJECT="<environment-tracer-session-name>"
```

Use the returned value rather than deriving it from the agent ID or display name. For example, an integration may call this setting `project_name`, `projectName`, `LANGCHAIN_PROJECT`, or `Langsmith-Project`. Replace every example destination, including overrides in code and replica destinations, with the selected environment's `tracer_session_name` in the target workspace.

If the integration supports [agent addressing](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md), set the agent ID and environment instead, for example `LANGSMITH_AGENT_ID` and `LANGSMITH_AGENT_ENVIRONMENT`. Do not combine those variables with legacy destination variables.

## Troubleshoot setup

* **Creation returns `403`**: Use a PAT or service key with the `projects:create` permission in the target workspace. A tracing key cannot call the agent creation API.
* **Tracing reports a missing agent**: Create the agent first, then retry tracing with its exact identifier and environment.
* **Creation returns `409`**: The identifier is already in use. Archived agents also retain their identifiers.
* **Traces appear in the wrong place**: Check the workspace, region, environment, and any destination overrides in code. Use the agent identifier, not its display name.

## See also

* [Agent Registry](Agent%20Registry.md)
* [Agent environments](Agent%20environments.md)
* [Build an agent with LangSmith Studio](../../../No-code%20agents/Studio/Build%20an%20agent%20with%20LangSmith%20Studio.md)
* [Deploy to an agent environment](Deploy%20to%20an%20agent%20environment.md)
* [Log traces to an agent](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md)
