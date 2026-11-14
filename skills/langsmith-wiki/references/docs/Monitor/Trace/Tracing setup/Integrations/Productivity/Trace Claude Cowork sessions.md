# Trace Claude Cowork sessions

> Send Claude Cowork tasks, tool calls, and skill use to LangSmith with the LangSmith tracing plugin for Claude.

[Claude Cowork](https://claude.com/docs/cowork/guide/plugins) runs the same plugins as Claude Code, so the [LangSmith tracing plugin for Claude Code](../Developer%20tools/Trace%20Claude%20Code%20sessions.md) also traces Cowork tasks. Each turn becomes a trace, and a task's turns are grouped into a thread.

## Prerequisites

* Access to Claude Cowork in the Claude desktop app.
* A LangSmith account.

## Install the plugin

Cowork installs plugins from your claude.ai account. To install the plugin for yourself:

1. Go to **Customize** > **Plugins** on claude.ai.
2. Add `langchain-ai/langsmith-claude-code-plugins` or `https://github.com/langchain-ai/langsmith-claude-code-plugins` as a marketplace.
3. Install the `langsmith-tracing` plugin from that marketplace.

The plugin loads into the next Cowork task you start. To install it for everyone see [Deploy to your organization](#deploy-to-your-organization). For more on installing plugins, see [Cowork plugins](https://claude.com/docs/cowork/guide/plugins) in the Claude docs.

## Sign in

Sign in once with the LangSmith CLI. See [Install the LangSmith CLI](../../../../../LangSmith%20setup/Govern/Tools/LangSmith%20CLI.md#install) if you do not have it yet.

```bash
langsmith auth login
```

If you use the CLI sign-in and have more than one profile, set `profile` in your config file to the one the plugin should use. Your own `api_key` ignores this setting, but a generic `LANGSMITH_API_KEY` is not used as a fallback while `profile` is set.

To use an API key instead, add it to `~/.claude/langsmith.json`, the same file Claude Code reads:

```json
{ "enabled": true, "api_key": "lsv2_pt_...", "agent_id": "shared-claude" }
```

If more than one credential is set, the plugin uses the first one it finds:

1. The plugin's own key from `api_key` or `CC_LANGSMITH_API_KEY`.
2. Your `langsmith auth login` sign-in.
3. A generic `LANGSMITH_API_KEY` from your environment.

A CLI sign-in acts as you so your workspace role needs permission to write traces. You may get a 403 if you switched from a tracing API key (`lsv2_tr_...`) to the CLI sign-in since tracing keys can always write traces whatever your role is. If that happens ask your admin to give you a role that can write traces such as Workspace User and check that no [ABAC deny policy](../../../../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Attribute-based%20access%20control.md) on the project blocks it.

Tracing stops when your sign-in expires or your key is rejected, and turns from that gap are never uploaded. Admins can also [require a working sign-in](#require-a-working-sign-in) for every prompt.

## Turn on tracing

Tracing is off until you turn it on in `~/.claude/langsmith.json`, unless your admin already turned it on with a [managed file](#lock-settings). In an [agent-based workspace](../../../../../LangSmith%20setup/Govern/Organization/Workspace%20setup/How%20agent-based%20workspaces%20differ.md), send traces to an [agent](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md#send-traces-to-an-agent) with `agent_id`:

```json
{ "enabled": true, "agent_id": "shared-claude" }
```

In a project-based workspace, use the legacy `project` setting instead:

```json
{ "enabled": true, "project": "shared-claude" }
```

Start a Cowork task and open your agent or project in [LangSmith](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-trace-claude-cowork). Skill calls record which skill ran, so you can filter traces by skill.

## Deploy to your organization

Admins can install the plugin for everyone and control how it traces from one place.

### Install for everyone

Organization owners can add the plugin to every member's claude.ai account, so it reaches Cowork and Claude Code together. For the setup, see [Choose a rollout route](https://claude.com/docs/plugins/org-rollout).

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

### Require a working sign-in

Strict auth blocks every prompt until the user's sign-in or key works, so no session goes untraced. It is off by default and has no effect while tracing is off. To turn it on for everyone, set `strict_auth` to `true` in the managed file.

## Hide a conversation

Run `/langsmith-tracing:mute` in a Cowork task to keep its content out of LangSmith, and `/langsmith-tracing:unmute` to turn it back on. To mute every task by default, set `defaultMuted` to `true`.

## Secret redaction

The plugin strips secrets on your machine before anything is uploaded, so they never reach LangSmith or a replica. Redaction is on by default.

It catches provider API keys, JSON Web Tokens, and PEM private keys, along with common patterns such as `API_KEY=<value>` or a password in a URL. Each match is replaced with `[SECRET_DETECTED]`. For the full rule list, see [Redact secrets from traces](../../../Configuration%20%26%20troubleshooting/Data%20%26%20privacy/Redact%20secrets%20from%20traces.md#rules-in-the-preset).

Redaction only matches known credential shapes, so treat it as a safety net rather than a guarantee. Run names, tags, and attachments skip it, and a redacted trace still holds your prompts and file contents. Limit who can read the tracing project.

## Settings

Cowork uses the same settings as Claude Code. For the main ones, see [Settings](../Developer%20tools/Trace%20Claude%20Code%20sessions.md#settings). For every setting, see the [plugin settings](https://github.com/langchain-ai/langsmith-claude-code-plugins#settings).
