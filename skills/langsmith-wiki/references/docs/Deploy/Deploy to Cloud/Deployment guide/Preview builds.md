# Preview builds

> Create temporary preview Agent Servers for pull requests to test Agent Server changes before merging.

Preview builds create temporary **preview Agent Servers** for pull requests. Use a preview Agent Server to test changes in isolation before you merge them into the branch that runs your parent Agent Server.

When a pull request triggers a preview build, LangSmith builds the latest commit from the source branch as the preview Agent Server's first revision. Each subsequent commit to that branch triggers a new revision.

> [!NOTE]
>
> Preview builds are in public beta and are available only on LangSmith Cloud for Agent Servers created through the GitHub integration.

## Enable preview builds

To enable preview builds:

1. From the **Agent Servers** view, select an Agent Server.
2. In the top-right corner, select the gear icon (**Agent Server Settings**).
3. Scroll to the **Preview Builds** section.
4. Select **Enable preview builds**.
5. Set **Base Branch**, or leave it blank to use the Agent Server's Git ref.
6. In **Create Previews For**, select a trigger mode:
   * **Every pull request**: Pull requests into the base branch trigger preview builds, except those from forks.
   * **Labeled pull requests**: A pull request triggers a preview build when it has the exact **Trigger Label**. Removing the label deletes the preview.
7. Configure the preview limits:
   * **Idle Timeout (Hours)**: Delete a preview after this period without pull request activity, such as new commits. Leave it blank to keep the preview until the pull request closes. This setting applies to new previews.
   * **Preview Limit**: The maximum number of preview Agent Servers for the parent Agent Server. Pull requests over the limit receive no preview until another closes.
8. Select **Save**.

## Manage secrets

A preview Agent Server inherits the parent Agent Server's secrets when LangSmith creates it. You can override the inherited secrets on the preview Agent Server.

Changes to the parent Agent Server's secrets do not propagate to existing preview Agent Servers.

## Delete preview Agent Servers

LangSmith deletes a preview Agent Server when its pull request closes, its trigger label is removed, or its configured idle timeout expires. You can also delete it manually at any time.

Deleting the parent Agent Server deletes all of its preview Agent Servers.

## See also

* [Deploy on Cloud](Create%20an%20Agent%20Server.md)
* [Implement a CI/CD pipeline](../../Agent%20Server/How%20to%20build/Implement%20a%20CI-CD%20pipeline%20using%20LangSmith%20Agent%20Server%20and%20Evaluation.md)
