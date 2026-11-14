# Create an Agent Server

> Create an Agent Server on LangSmith Cloud from the LangSmith UI or LangGraph CLI.

Create an Agent Server on LangSmith Cloud from a connected GitHub repository or directly from your local project. The LangSmith UI deploys from GitHub. The `langgraph deploy` CLI builds locally or triggers a remote build.

For a shorter walkthrough, see the [deployment quickstart](../../Get%20started/Deploy%20your%20app%20to%20cloud.md).

## Prerequisites

* A LangSmith account on the [Plus plan or above](https://www.langchain.com/pricing).
* An application that runs locally with `langgraph dev`. For more information, see [Local development and testing](../../Get%20started/Develop%20%26%20test/Local%20development%20%26%20testing.md).

## Create an Agent Server

> [tab] LangSmith UI
>
> A GitHub organization owner or admin must authorize LangChain's `hosted-langserve` GitHub app once for the workspace. After authorization, any user with deployment permissions can create Agent Servers from repositories that the app can access.
>
> To create an Agent Server:
>
> 1. From the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-deploy-to-cloud), select **Agent Servers**.
>
> 2. In the top-right corner, select **+ Agent Server**.
>
> 3. If the **Source** selector appears, select **GitHub repository** rather than **Docker image**. Complete the GitHub authorization flow if prompted.
>
> 4. Select a repository.
>
> 5. Enter a name for the Agent Server.
>
> 6. In **Git Ref (Branch or Tag)**, enter a branch name or a full tag ref such as `refs/tags/v1.0.0`.
>
> 7. Enter the full path to the [LangGraph API configuration file](../../Get%20started/Reference/LangGraph%20CLI.md#configuration-file), including the file name. For example, enter `langgraph.json` if the file is in the repository root.
>
> 8. For a branch, choose whether to enable **Automatically update Agent Server on push to branch**. This option is unavailable for tags. You can change it later in [Agent Server Settings](Manage%20an%20Agent%20Server.md#configure-deployment-settings).
>
> 9. For [Agent Server type](../Cloud%20platform%20features.md#deployment-types), select **Serverless** or **Dedicated**, depending on whether the workload can tolerate cold starts or needs always-on capacity.
>
> 10. Choose whether to make the Agent Server shareable through [Studio](../../../Test/Test%20from%20Studio/LangSmith%20Studio.md).
>
> 11. Add environment variables and secrets. For more information, see [Environment variables](../Reference/Cloud%20Agent%20Server%20environment%20variables.md).
>
> 12. Select **Submit**. LangSmith queues the Agent Server for provisioning. In a project-based workspace, LangSmith also creates a tracing project with the same name as the Agent Server. In an agent-based workspace, LangSmith instead binds the Agent Server to an [agent](../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md#agent), and the Agent Server reports into one of the agent's [environments](../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20environments.md).
>
> > [!NOTE]
> >
> > The GitHub user who authorizes the `hosted-langserve` app must own the GitHub organization or account. Other users with deployment permissions do not need GitHub administrator access after the initial authorization.

> [tab] LangGraph CLI
>
> > [!NOTE]
> >
> > The `langgraph deploy` command is in [beta](../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md). Local builds require Docker. On Apple silicon, local builds also require Docker Buildx to cross-compile for `linux/amd64`. If Docker is unavailable, the CLI triggers a remote build on LangSmith Cloud.
>
> To create an Agent Server:
>
> 1. Install the [LangGraph CLI](../../Get%20started/Reference/LangGraph%20CLI.md):
>
>    ```shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
>    uv tool install langgraph-cli
>    ```
>
> 2. Add your LangSmith API key to a `.env` file in the project root:
>
>    ```shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
>    LANGSMITH_API_KEY=lsv2_...
>    ```
>
> 3. Run:
>
>    ```shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
>    langgraph deploy
>    ```
>
>    The command creates a Serverless Agent Server named after the project directory. To set another name, or to create a Dedicated [Agent Server](../Cloud%20platform%20features.md#deployment-types) instead:
>
>    ```shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
>    langgraph deploy --name my-agent --agent-server-type dedicated
>    ```
>
> LangSmith queues the Agent Server for provisioning. Manage environment variables through the LangSmith UI or the [`env` field in `langgraph.json`](../../Get%20started/Reference/LangGraph%20CLI.md#configuration-file).

## Manage GitHub repository access

After you authorize the `hosted-langserve` GitHub app, configure which repositories it can access:

1. In GitHub, go to **Settings** > **Applications**.
2. Find `hosted-langserve`, then select **Configure**.
3. Under **Repository access**, select **All repositories** or **Only select repositories**.
4. If you selected **Only select repositories**, add or remove repositories as needed.
5. Select **Save**.

The repository list in the **Create Agent Server** pane reflects the updated access.

If you rename or transfer a repository that an Agent Server uses, [change the Agent Server's repository](Manage%20an%20Agent%20Server.md#change-the-repository).

## See also

* [Revisions](Revisions.md)
* [Preview builds](Preview%20builds.md)
* [Manage an Agent Server](Manage%20an%20Agent%20Server.md)
