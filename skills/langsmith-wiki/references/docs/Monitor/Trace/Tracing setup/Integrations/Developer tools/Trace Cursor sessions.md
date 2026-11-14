# Trace Cursor sessions

> Capture Cursor agent turns, tool calls, model metadata, token usage, attachments, and subagents in LangSmith.

The LangSmith tracing plugin sends your [Cursor](https://cursor.com/) agent conversations to LangSmith so you can see what the agent did. Each prompt becomes a trace, and a conversation's prompts are grouped into a thread.

## Prerequisites

* [Cursor](https://cursor.com/) installed.
* A LangSmith account.
* [Node.js](https://nodejs.org/) 22.13 or later on Windows and Linux. On macOS the plugin runs its own build and does not need Node.js.

## Install the plugin

To install the plugin for yourself:

1. Open **Customize** in Cursor and choose **Add Marketplace**.
2. Enter `https://github.com/langchain-ai/langsmith-cursor-plugins`.
3. Run `/add-plugin langsmith-tracing` in the agent chat, or install it from the new **LangChain** tab in **Customize**.
4. Fully restart Cursor so it loads the plugin's hooks.

To install the plugin for everyone, see [Deploy to your organization](#deploy-to-your-organization). For more on installing plugins, see [Plugins](https://cursor.com/docs/plugins) in the Cursor docs.

## Sign in

Sign in once with the LangSmith CLI. See [Install the LangSmith CLI](../../../../../LangSmith%20setup/Govern/Tools/LangSmith%20CLI.md#install) if you do not have it yet.

```bash
langsmith auth login
```

If you use the CLI sign-in and have more than one profile, set `profile` in your config file to the one the plugin should use. Your own `api_key` ignores this setting, but a generic `LANGSMITH_API_KEY` is not used as a fallback while `profile` is set.

To use an API key instead, add it to `~/.cursor/langsmith.json`:

```json
{ "enabled": true, "api_key": "lsv2_pt_...", "agent_id": "shared-cursor" }
```

If more than one credential is set, the plugin uses the first one it finds:

1. The plugin's own key from `api_key` or `LANGSMITH_CURSOR_API_KEY`.
2. Your `langsmith auth login` sign-in.
3. A generic `LANGSMITH_API_KEY` from your environment.

A CLI sign-in acts as you so your workspace role needs permission to write traces. You may get a 403 if you switched from a tracing API key (`lsv2_tr_...`) to the CLI sign-in since tracing keys can always write traces whatever your role is. If that happens ask your admin to give you a role that can write traces such as Workspace User and check that no [ABAC deny policy](../../../../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Attribute-based%20access%20control.md) on the project blocks it.

Tracing stops when your sign-in expires or your key is rejected, and turns from that gap are never uploaded. Cursor cannot show a message without stopping the prompt, so the plugin writes the reason to `~/.cursor/langsmith_hook.log` instead. Admins can also [require a working sign-in](#require-a-working-sign-in) for every prompt.

## Turn on tracing

Tracing is off until you turn it on in `~/.cursor/langsmith.json`, unless your admin already turned it on with a [managed file](#lock-settings). In an [agent-based workspace](../../../../../LangSmith%20setup/Govern/Organization/Workspace%20setup/How%20agent-based%20workspaces%20differ.md), send traces to an [agent](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md#send-traces-to-an-agent) with `agent_id`:

```json
{ "enabled": true, "agent_id": "shared-cursor" }
```

In a project-based workspace, use the legacy `project` setting instead:

```json
{ "enabled": true, "project": "shared-cursor" }
```

> [!WARNING]
>
> A project can override these settings with `<project>/.cursor/langsmith.json` or `<project>/langsmith-plugins.json`. A cloned repository can use them to turn tracing on and send your prompts and files to someone else's server. Before you trust a repository, review those files. Cursor's own `.cursor/hooks.json` can run commands, so review that one too.

Send a prompt and open your agent or project in [LangSmith](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-trace-with-cursor). In Auto mode, the model shows as `default` and subagents show no token counts, because Cursor does not report either one.

## Deploy to your organization

Admins can install the plugin for everyone and control how it traces from one place.

### Install for everyone

Admins on a Teams or Enterprise plan can import the repository as a team marketplace, so the plugin installs for everyone. For the setup, see [Cursor's plugin docs](https://cursor.com/docs/plugins).

### Lock settings

An admin can lock tracing settings for every user with a managed file at `~/.langsmith-plugins/managed.json` in each user's home folder. The Claude Code, Cursor, and Codex plugins all read this file, and its settings override the user's own config files and environment variables.

```json
{
  "api_url": "https://api.smith.langchain.com",
  "agent_id": "coding-agent",
  "strict_auth": true,
  "workspace_id": "<your-workspace-id>"
}
```

Set `workspace_id` as well when your users sign in with the LangSmith CLI. Each user's sign-in may default to a different workspace, so setting it here keeps everyone's traces in one place. API keys ignore this setting so use one scoped to a workspace.

The managed file works on macOS and Linux. The plugin only trusts it when:

* Root owns the file and its folder.
* No other user can write to either.
* Neither is a symlink.

If the file exists but fails these checks, tracing stops and the user sees a message to contact their admin. Locking a setting also locks the settings tied to it, so users cannot route traces around the lock. For example, locking `agent_id` also stops users from sending traces to a project with `project`.

Admins usually install the file on each machine with a mobile device management (MDM) tool such as Jamf or Microsoft Intune. For every setting you can lock, see the [plugin settings guide](https://github.com/langchain-ai/langsmith-plugin-binary/blob/main/docs/settings.md).

> [accordion] Example setup script
>
> Run this as root for each user, with `USER_HOME` set to that user's home folder:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> USER_HOME=/Users/developer
> mkdir -p "$USER_HOME/.langsmith-plugins"
> cp managed.json "$USER_HOME/.langsmith-plugins/managed.json"
> chown root:wheel "$USER_HOME/.langsmith-plugins" "$USER_HOME/.langsmith-plugins/managed.json"
> chmod 755 "$USER_HOME/.langsmith-plugins"
> chmod 644 "$USER_HOME/.langsmith-plugins/managed.json"
> ```
>
> On Linux, use `root:root` instead of `root:wheel`. For the full script, see [Set it up on macOS](https://github.com/langchain-ai/langsmith-plugin-binary/blob/main/docs/settings.md#set-it-up-on-macos).

Cursor can also lock `attachments` and `system_prompt`.

### Require a working sign-in

Strict auth blocks every prompt until the user's sign-in or key works, so no session goes untraced. It is off by default and has no effect while tracing is off. To turn it on for everyone, set `strict_auth` to `true` in the managed file.

## Hide a conversation

Send `langsmith-tracing:mute` as a message in Cursor's agent chat to keep a conversation's content out of LangSmith, and `langsmith-tracing:unmute` to turn it back on. Send exactly that text with no slash, or it is traced as a normal prompt. The acknowledgment appears as a blocked prompt, because that is how Cursor shows a plugin's reply.

To mute every new conversation by default, set `defaultMuted` to `true`.

## Secret redaction

The plugin strips secrets on your machine before anything is uploaded, so they never reach LangSmith or a replica. Redaction is on by default.

It catches provider API keys, JSON Web Tokens, and PEM private keys, along with common patterns such as `API_KEY=<value>` or a password in a URL. Each match is replaced with `[SECRET_DETECTED]`. For the full rule list, see [Redact secrets from traces](../../../Configuration%20%26%20troubleshooting/Data%20%26%20privacy/Redact%20secrets%20from%20traces.md#rules-in-the-preset).

Redaction only matches known credential shapes, so treat it as a safety net rather than a guarantee. Run names, tags, and attachments skip it, and a redacted trace still holds your prompts and file contents. Limit who can read the tracing project.

Images you attach to a prompt skip redaction. Set `attachments` to `false` to stop sending them. To turn redaction off or add your own patterns, see the [plugin settings](https://github.com/langchain-ai/langsmith-cursor-plugins#settings).

## Settings

Each setting has a config file key and an environment variable. The environment variable wins when both are set.

| Config key | Environment variable | Default | Description |
| - | - | - | - |
| `enabled` | `TRACE_TO_LANGSMITH` | `false` | Turns tracing on. |
| `api_key` | `LANGSMITH_CURSOR_API_KEY` | none | LangSmith API key. Not needed if you sign in with the CLI. |
| `agent_id` | `LANGSMITH_AGENT_ID` | none | Agent the traces go to. Wins over `project` if both are set. |
| `project` (deprecated) | `LANGSMITH_CURSOR_PROJECT` | `cursor` | Project the traces go to. Use `agent_id` unless your workspace is [project-based](../../../../../LangSmith%20setup/Govern/Organization/Workspace%20setup/How%20agent-based%20workspaces%20differ.md#check-which-one-you-have). |
| `api_url` | `LANGSMITH_CURSOR_ENDPOINT` | `https://api.smith.langchain.com` | LangSmith server to send to. |
| `workspace_id` | `LANGSMITH_WORKSPACE_ID` | none | Workspace the traces go to when you sign in with the CLI. API keys ignore it and your config file wins over the variable. |

For every setting, see the [plugin settings](https://github.com/langchain-ai/langsmith-cursor-plugins#settings).

## Troubleshooting

* **No traces**: Check that the plugin is in Cursor's plugin list and that you fully restarted Cursor after installing it. Then check that tracing is on.
* **Tracing is paused**: Run `langsmith auth login` again or replace the rejected API key.
* **Tracing is paused after a 403**: Your sign-in or API key might not have access to the agent, project or workspace. Look through `~/.cursor/langsmith_engine/worker.log` and `~/.cursor/langsmith_hook.log` for the details.
* **Still stuck**: Run `tail -f ~/.cursor/langsmith_hook.log` while you send a prompt. Set `LANGSMITH_CURSOR_DEBUG=1` for more detail.

For more fixes, see [When nothing shows up](https://github.com/langchain-ai/langsmith-cursor-plugins#when-nothing-shows-up).
