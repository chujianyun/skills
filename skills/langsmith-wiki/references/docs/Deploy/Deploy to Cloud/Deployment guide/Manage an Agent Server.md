# Manage an Agent Server

> Configure the repository, branch, and automatic updates for an Agent Server on LangSmith Cloud, or delete it.

Manage the repository, branch, and automatic update settings for an Agent Server on LangSmith Cloud. You can also delete an Agent Server when you no longer need it.

## Configure Agent Server settings

To configure Agent Server settings:

1. From the **Agent Servers** view, select an Agent Server.
2. In the top-right corner, select the gear icon (**Agent Server Settings**).
3. (Optional) To build from a different GitHub repository, select **Change repository** and choose the repository. For details, see [Change the repository](#change-the-repository).
4. Update **Git Ref (Branch or Tag)** as needed. Enter a branch name or a full tag ref such as `refs/tags/v1.0.0`.
5. For a branch, enable or disable **Deploy on push**. This option is unavailable for tags.

Branch and tag creation or deletion events do not trigger revisions. Only pushes to an existing branch trigger an update.

When several pushes occur in quick succession, LangSmith queues the updates. After the current build completes, LangSmith builds the most recent commit and skips the other queued commits.

### Change the repository

Change the repository after you rename it, transfer it to another GitHub account, or move your agent to a different repository. LangSmith checks that the `hosted-langserve` GitHub app can access the repository and that the repository contains the Agent Server's configuration file on its Git branch. Saving does not create a revision; the next revision builds from the new repository.

If you transferred the repository to another GitHub account, first [give the app access to it](Create%20an%20Agent%20Server.md#manage-github-repository-access).

To change the repository through the API, send `source_config.repo_url` in a `PATCH /v2/deployments/{deployment_id}` request. For more information, see the [Control plane API reference](../../Get%20started/Reference/Control%20Plane%20API/Control%20plane%20API%20reference%20for%20Agent%20Server%20hosting.md).

## Delete an Agent Server

> [tab] LangSmith UI
>
> To delete an Agent Server:
>
> 1. From the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-manage-deployment), select **Agent Servers**.
> 2. Select the menu icon for the Agent Server, then select **Delete**.
> 3. In the confirmation modal, select **Delete**.

> [tab] LangGraph CLI
>
> To find the Agent Server ID, run:
>
> ```shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> langgraph deploy list
> ```
>
> Delete the Agent Server by ID:
>
> ```shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> langgraph deploy delete <AGENT_SERVER_ID>
> ```
>
> To skip the confirmation prompt, pass `--force`:
>
> ```shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> langgraph deploy delete --force <AGENT_SERVER_ID>
> ```

> [!NOTE]
>
> Deletion is asynchronous. The Agent Server disappears from the **Agent Servers** view immediately, but LangSmith removes its infrastructure and metadata in stages. The Agent Server name might remain unavailable until deletion finishes.

## See also

* [Create an Agent Server](Create%20an%20Agent%20Server.md)
* [Preview builds](Preview%20builds.md)
