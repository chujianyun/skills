# Custom Apps

> Build custom UIs that run inside LangSmith and call the LangSmith API, either by chatting with LangSmith Chat or locally with the LangSmith CLI.

> [!NOTE]
>
> Custom apps are available on [**Plus** and **Enterprise** plans](https://www.langchain.com/pricing).

A custom app is a UI you build that runs inside LangSmith and calls the [LangSmith API](../../Reference/LangSmith%20REST%20API/LangSmith%20API%20reference.md). Use one for a workflow the built-in UI does not cover, such as a purpose-built annotation surface, an experiment comparison view, or a dashboard scoped to your own traces.

Deployed apps appear under **Custom Apps** in the sidebar for everyone in the workspace with the `custom-apps:read` permission. You do not host a separate service or manage a separate login.

An app runs in a sandbox with no network access of its own. The host forwards its LangSmith API requests with the viewer's credentials, so each person sees only the data their [permissions](../../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Organization%20and%20workspace%20operations%20reference.md) allow. The host forwards nothing else, and it blocks the endpoints for API keys, members, users, identities, roles, permissions, SCIM, and service accounts.

## Configure self-hosted chat

> [!WARNING]
>
> On self-hosted deployments, building and editing apps with chat requires [sandbox service URLs](../../../LangSmith%20setup/Self-hosted/Install%20an%20instance/Additional%20features/Enable%20Sandboxes/Enable%20Sandboxes%20on%20self-hosted%20LangSmith.md#optional-enable-service-urls). Enabling Sandboxes alone is not sufficient.

> [!NOTE]
>
> Building and editing apps with chat is enabled starting with Helm chart version 0.17.3 for v0.17 and 0.18.0-rc.13 for the v0.18 preview.

## Build an app

Build an app by [chatting with LangSmith Chat](#build-with-chat) in the browser, or [locally with the CLI](#build-locally-with-the-cli) and your own coding agent. Both paths produce the same app and store the same source, so either one can [edit](#edit-an-app) what the other built.

### Build with chat

Building in the browser has two requirements:

* **Sandboxes**: Each session runs in a [sandbox](../../../Deploy/Sandboxes/LangSmith%20Sandboxes.md). On self-hosted deployments, complete the [self-hosted chat setup](#configure-self-hosted-chat) first.
* **Permissions**: The `custom-apps:create`, `custom-apps:update`, `custom-apps:delete`, and `custom-apps:download` permissions, plus the [sandbox permissions](#permissions).

Without both, the **App** action opens the CLI instructions instead. Chat also needs a [model API key set for the workspace](../../../Test/Datasets%20%26%20Experiments/Analyze%20experiment%20results/LangSmith%20Chat.md#get-started) before it can send a message.

To build an app with chat:

**1. Start a new app**

Go to **Custom Apps** and select **App** to open chat. In a workspace with no apps yet, the page opens chat directly.

**2. Describe what you want to build**

Type what the app should do into the composer, and select the model to build with from the model menu in the composer. The composer accepts a prompt while the sandbox behind it is still starting. When Chat starts writing files, LangSmith saves a draft and opens the **Preview** and **Code** tabs beside the chat.

**3. Review what Chat built**

The **Preview** tab renders a live build of your changes. The **Code** tab holds the file tree, the source, and the changes from the session. A badge in the header counts the changed files.

**4. Deploy the app**

Select **Deploy**. The first deploy asks for a name, builds the app, and publishes it to the workspace.

If you leave the page before the first deploy, LangSmith discards the app. Once Chat has started editing, LangSmith asks before discarding it.

### Build locally with the CLI

Building locally uses the [LangSmith CLI](../../../LangSmith%20setup/Govern/Tools/LangSmith%20CLI.md), which scaffolds a starter, runs it in a real sandbox on your machine, and uploads it when you are ready. To build an app locally:

**1. Install the CLI**

```bash
curl -fsSL https://cli.langsmith.com/install.sh | sh
```

For Windows, Homebrew, and other options, see [Install](../../../LangSmith%20setup/Govern/Tools/LangSmith%20CLI.md#install).

**2. Authenticate**

```bash
langsmith auth login
```

To use an API key instead, set `LANGSMITH_API_KEY`, plus `LANGSMITH_ENDPOINT` for a self-hosted instance. For profiles and other options, see [Authenticate](../../../LangSmith%20setup/Govern/Tools/LangSmith%20CLI.md#authenticate).

**3. Scaffold an app**

```bash
langsmith apps init --name my-annotation-view --template annotation-queue
```

`init` creates a directory named after the app and, if `npm` is on your `PATH`, installs its dependencies. It also writes an `AGENTS.md` that gives a coding agent the conventions and API surface it needs to produce a working app on the first pass. Omit `--template` for a blank single-file starter.

**4. Iterate locally**

```bash
cd my-annotation-view
langsmith apps dev
```

The app runs in the same kind of sandbox it gets inside LangSmith, with API calls proxied through your own credentials. Failed calls and uncaught errors stream to the terminal, so most debugging needs no browser devtools. Add `--verbose` for every successful call and all console output, or `--quiet` to silence the app.

**5. Push it live**

```bash
langsmith apps push
```

The first push creates the app and records its ID in `.langsmith/app.json`, which links the directory to it. Later pushes update the same app. Commit that file so teammates push to the same app.

#### Starter templates

Pass one of these to `langsmith apps init --template`:

| Template | What it scaffolds |
| - | - |
| `annotation-queue` | A queue-review UI: run and thread items, a type-specific viewer, and a feedback rubric. |
| `annotation-queue-grid` | The same review workflow as an editable spreadsheet. |
| `experiment-comparison` | A side-by-side comparison of evaluation experiments against a baseline. |
| `coding-agent-dashboard` | Charts over coding-agent runs: usage, cost, errors, and activity over time. |

## Edit an app

Edit an app in the browser with chat, or pull its source and edit it locally.

### Edit with chat

Open an app from **Custom Apps** and select **Edit**. The published app is replaced by the editing workspace: chat on the left, and the same **Preview** and **Code** tabs on the right.

Ask for the change in chat, or edit a file directly in **Code** and save it with `Cmd+S` (`Ctrl+S` on Windows and Linux). Either way, the preview rebuilds, and the badge in the header updates its count of changed files.

Two actions end the session:

* **Deploy**: Builds the app and publishes it as a new version for the workspace.
* **Cancel**: Leaves without deploying. Undeployed changes stay in the editing sandbox.

Editing runs in a sandbox that stops after a period of inactivity. Reopening the app wakes the sandbox with undeployed changes intact. If the sandbox has been deleted, select **Recreate from saved source** to rebuild the session from the last deployed source. Undeployed changes are lost.

To rename an app, copy its ID, or change who it is shared with, select **Edit** from the row menu in the app list.

### Edit locally with the CLI

A deploy from the browser stores the app's source, and so does `langsmith apps push`. To edit an app locally, pull it down:

```bash
langsmith apps pull my-app
npm install --prefix my-app
```

Edit the source with your own coding agent, then run `langsmith apps push` to publish it.

The scaffolded `AGENTS.md` asks the agent to keep a `context.md` at the app root as the app's memory: what the app does, which files matter, and the decisions behind them. Any root file travels with the source, so a teammate who pulls the app starts from what you learned rather than from scratch.

## Share an app with your organization

A custom app belongs to the workspace it was created in. To share one with the organization, open the row menu in the app list, select **Edit**, then select **Share with organization**. Every workspace in the organization can then see, update, and delete it.

To move a shared app back into a single workspace, select **Pull into this workspace** from that workspace. If the workspace already has an app with the same name, LangSmith asks you to rename it.

When the CLI resolves an app by name, a workspace app wins over an organization app of the same name.

## CLI reference

| Command | What it does |
| - | - |
| `langsmith apps init --name NAME [--template TEMPLATE]` | Scaffold a starter app in a new directory named after the app, and install its dependencies. |
| `langsmith apps dev` | Run the current directory's app locally in a real sandbox. |
| `langsmith apps push` | Upload the current directory as a custom app, creating it on the first push. Pass `--no-build` to upload the current files as-is. |
| `langsmith apps pull APP_ID_OR_NAME` | Download an app's source into a new directory. |
| `langsmith apps list` | List custom apps. |
| `langsmith apps delete APP_ID_OR_NAME` | Delete an app by ID or name. Pass `--yes` to skip the confirmation. |

`dev` and `push` act on the current directory, so change into the app's directory first.

## Permissions

The `custom-apps:*` permissions control access to custom apps. For the full table, see [Custom apps](../../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Organization%20and%20workspace%20operations%20reference.md#custom-apps).

Editing in the browser also requires the `sandboxes:create`, `sandboxes:read`, `sandboxes:update`, `sandboxes:delete`, and `sandboxes:exec` permissions, because each session runs in a sandbox. The **Edit** action appears only for users with `custom-apps:update`, `custom-apps:download`, and the sandbox permissions.
