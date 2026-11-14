# Set up coding agents

> Configure Claude Code, Codex, Gemini CLI, and Deep Agents Code to route LLM calls through the LLM Gateway.

> [!NOTE]
>
> The LLM Gateway is in [beta](../../LangSmith%20setup/Cloud/Reference/Release%20stages.md).

Configure coding agents to use the standard LLM Gateway endpoint for centralized cost controls, observability, and audit trails. The gateway authenticates each caller, routes by model ID, enforces policies, and traces each call.

## Prerequisites

* An admin has completed any required [gateway setup](../Get%20started/Set%20up%20the%20LLM%20Gateway.md).
* You have a workspace-scoped LangSmith API key. For key types, permissions, and the header each client sends, see [Authenticate to the LLM Gateway](../Authentication/Authenticate%20to%20the%20LLM%20Gateway.md).
* For bring-your-own-key models, your workspace has the corresponding provider secret. [Gateway Credits models](../Models%20and%20reliability/Gateway%20Credits.md) do not require a provider secret.

Set your LangSmith API key before configuring a client:

```bash
export LANGSMITH_API_KEY="<SECRET>"
```

Then configure your agent:

* [Claude Code](#claude-code-cli) uses the standard Anthropic Messages format.
* [Codex](#codex-cli) and [Deep Agents Code](#deep-agents-code) use the standard OpenAI-compatible formats.
* [Gemini CLI](#gemini-cli) uses Google's native API and requires [direct model access](Direct%20model%20access.md).

## Claude Code CLI

Claude Code always authenticates to the gateway with your LangSmith API key. It supports two ways for the gateway to authenticate to Anthropic, each with a different billing owner. Choose one before configuring:

* **Workspace provider secret**: The organization manages billing and policies through a provider key stored in workspace secrets. Use this method for org-managed usage.
* **Claude subscription OAuth**: Anthropic bills LLM calls to the user's personal Claude Plus or Max subscription instead of the workspace provider secret. LangSmith still enforces gateway permissions, rate limit, model access, and data policies, and traces each call. Spend limits do not apply. Use this method when developers have their own subscriptions.

### Use a workspace provider secret

Set `ANTHROPIC_API_KEY` to your LangSmith API key. Claude Code reads these variables from your shell environment or from the `env` block in a settings file passed with `--settings`.

If your LangSmith deployment is on a regional instance, replace the gateway hostname in the examples below with your [regional gateway](../Get%20started/How%20the%20LLM%20Gateway%20works.md#use-a-regional-gateway) hostname. On a [self-hosted installation](../Get%20started/How%20the%20LLM%20Gateway%20works.md#use-a-self-hosted-installation), replace `https://gateway.smith.langchain.com` with `https://<your-hostname>/gateway`.

#### Use Anthropic models only

Set `ANTHROPIC_BASE_URL` to the Anthropic-format gateway endpoint. The gateway infers the `anthropic/` provider prefix from the endpoint.

> [tab] Settings file (recommended)
>
> Variables declared in a `--settings` file take precedence over anything already exported in your shell, so the gateway URL and API key are guaranteed to override any ambient `ANTHROPIC_*` values that may already be set in your environment (for example, from a global shell profile or another tool).
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> touch ~/.claude/langsmith_gateway.settings.json
> echo '{"env": {"ANTHROPIC_BASE_URL": "https://gateway.smith.langchain.com/anthropic/","ANTHROPIC_API_KEY": "YOUR_LANGSMITH_KEY_HERE"}}' > ~/.claude/langsmith_gateway.settings.json
> claude --settings ~/.claude/langsmith_gateway.settings.json
> ```
>
> Replace `YOUR_LANGSMITH_KEY_HERE` with your LangSmith API key.

> [tab] Environment variables
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> export ANTHROPIC_BASE_URL="https://gateway.smith.langchain.com/anthropic/"
> export ANTHROPIC_API_KEY="<SECRET>"
>
> claude
> ```

#### Route model tiers across providers

Set `ANTHROPIC_BASE_URL` to the gateway root, then map each Claude model tier to a provider-prefixed gateway model ID.

> [tab] Settings file (recommended)
>
> Variables declared in a `--settings` file take precedence over anything already exported in your shell, so gateway URLs, the API key, and model mappings are guaranteed to override any ambient `ANTHROPIC_*` values.
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> touch ~/.claude/langsmith_gateway.settings.json
> echo '{"env": {"ANTHROPIC_BASE_URL": "https://gateway.smith.langchain.com","ANTHROPIC_API_KEY": "YOUR_LANGSMITH_KEY_HERE","ANTHROPIC_DEFAULT_OPUS_MODEL": "anthropic/claude-opus-5","ANTHROPIC_DEFAULT_SONNET_MODEL": "openai/gpt-5.6-terra","ANTHROPIC_DEFAULT_HAIKU_MODEL": "fireworks/accounts/fireworks/models/glm-5p2"}}' > ~/.claude/langsmith_gateway.settings.json
> claude --settings ~/.claude/langsmith_gateway.settings.json
> ```
>
> Replace `YOUR_LANGSMITH_KEY_HERE` with your LangSmith API key.

> [tab] Environment variables
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> export ANTHROPIC_BASE_URL="https://gateway.smith.langchain.com"
> export ANTHROPIC_API_KEY="<SECRET>"
> export ANTHROPIC_DEFAULT_OPUS_MODEL="anthropic/claude-opus-5"
> export ANTHROPIC_DEFAULT_SONNET_MODEL="openai/gpt-5.6-terra"
> export ANTHROPIC_DEFAULT_HAIKU_MODEL="fireworks/accounts/fireworks/models/glm-5p2"
>
> claude
> ```

The model IDs are examples. Map each tier to any model configured in your workspace secrets or available through [Gateway Credits](../Models%20and%20reliability/Gateway%20Credits.md); the gateway handles request translation across providers. For details, see [API formats](API%20formats.md#understand-translation-behavior).

> [!WARNING]
>
> Claude Code uses [tool search](https://code.claude.com/docs/en/agent-sdk/tool-search) by default, and the gateway cannot translate tool search into the Chat Completions format. A tier mapped to a model that the gateway reaches only over Chat Completions, such as a Google Gemini model or an OpenAI-compatible [custom configuration](../Models%20and%20reliability/Custom%20model%20configurations.md), fails with a `400` error that mentions `deferred tools, tool search` before the gateway calls the provider.
>
> To avoid the error, do one of the following:
>
> * Map the tier to a model from Anthropic, OpenAI, or Fireworks, which the gateway reaches over the Messages or Responses format.
> * Use an Anthropic-compatible configuration, or an OpenAI-compatible configuration set to the Responses API.
> * Set `ENABLE_TOOL_SEARCH=false` in your settings file or environment. Claude Code then loads every tool definition into context on every turn, which uses more input tokens.

### Use Claude subscription OAuth

> [!NOTE]
>
> Claude subscription OAuth requires an active Claude Code Plus or Max subscription. If you are using a workspace Anthropic API key, use the [workspace provider secret](#use-a-workspace-provider-secret) method instead.

Claude Code Plus and Max users can send their saved Anthropic OAuth credential through the gateway. This mode does not require an `ANTHROPIC_API_KEY` in workspace provider secrets.

Log in to Claude Code with your subscription, then configure the gateway.

> [tab] Settings file (recommended)
>
> Variables declared in a `--settings` file take precedence over anything already exported in your shell, so the gateway URL and custom headers are guaranteed to override any ambient `ANTHROPIC_*` values. The settings file also keeps your LangSmith API key out of your shell history and dotfiles.
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> touch ~/.claude/langsmith_gateway.settings.json
> echo '{"env": {"ANTHROPIC_BASE_URL": "https://gateway.smith.langchain.com/anthropic","ANTHROPIC_CUSTOM_HEADERS": "X-Api-Key: YOUR_LANGSMITH_KEY_HERE"}}' > ~/.claude/langsmith_gateway.settings.json
> claude --settings ~/.claude/langsmith_gateway.settings.json
> ```
>
> Replace `YOUR_LANGSMITH_KEY_HERE` with your LangSmith API key.

> [tab] Environment variables
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> export ANTHROPIC_BASE_URL="https://gateway.smith.langchain.com/anthropic"
> export ANTHROPIC_CUSTOM_HEADERS="X-Api-Key: $LANGSMITH_API_KEY"
>
> claude
> ```
>
> Treat the `ANTHROPIC_CUSTOM_HEADERS` value as a secret: it embeds your LangSmith API key, so keep it out of shell history, dotfiles, and shared configuration.

Claude Code uses and refreshes the OAuth credential from its saved login, including the required OAuth capability in the `anthropic-beta` header.

The LangSmith API key authenticates the gateway request and remains subject to gateway permissions and to rate limit, model access, and data policies. The gateway forwards the OAuth bearer to Anthropic, so Anthropic bills the call to the user's Claude subscription instead of the workspace provider secret. [Spend limits](../Governance/Spend%20policies.md) do not apply to these calls, and the calls are left out of spend totals. To confirm calls route through the gateway, check that traces appear in the `gateway` tracing project as described in [Verify the setup](#verify-the-setup).

> [!WARNING]
>
> Leave `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_API_KEY` unset for this mode. Either variable takes precedence over the saved subscription login.

> [!WARNING]
>
> Claude Desktop plugins break when the gateway is configured.

## Codex CLI

Codex uses the Responses API. Add the following to `~/.codex/config.toml` to call the hosted Kimi K3 model with Gateway Credits through the standard endpoint:

```toml
model = "moonshotai/kimi-k3"
model_provider = "langsmith-gateway"

[model_providers.langsmith-gateway]
name = "LangSmith Gateway"
base_url = "https://gateway.smith.langchain.com/v1"
env_key = "LANGSMITH_API_KEY"
wire_api = "responses"
supports_websockets = false
```

Then run:

```bash
codex
```

To use a bring-your-own-key model instead, replace `model` with its provider-prefixed ID, such as `openai/gpt-5.4-mini`.

> [!WARNING]
>
> Codex Desktop plugins break when the gateway is configured. The TOML configuration forces authentication through the gateway, so OpenAI no longer handles plugin authentication directly.

## Gemini CLI

Gemini CLI sends Google's native Generate Content requests, which the standard endpoint does not expose. Follow [Direct model access](Direct%20model%20access.md#configure-provider-sdks) to configure the `/gemini` route, then run:

```bash
gemini
```

## Deep Agents Code

Use the OpenAI-compatible client with the standard endpoint, then pass the hosted model slug through the `openai` integration:

```bash
export OPENAI_BASE_URL="https://gateway.smith.langchain.com/v1"
export OPENAI_API_KEY="<SECRET>"

dcode --model openai:moonshotai/kimi-k3
```

To use a bring-your-own-key model, keep the standard base URL and pass a provider-prefixed model after `openai:`, for example, `openai:anthropic/claude-opus-5`. For provider-native integrations and model IDs, see [Direct model access](Direct%20model%20access.md#configure-langchain-and-deep-agents).

## Company-wide deployment

For organizations rolling the gateway out to all developers, distribute the configuration through mobile device management or a shared shell profile. Distribute:

1. The standard gateway base URL for each client.
2. A workspace-scoped [LangSmith API key](../Authentication/Authenticate%20to%20the%20LLM%20Gateway.md#choose-a-key-type) per user or per cost center, depending on your policy granularity.
3. The model IDs approved for each coding agent.
4. The Codex `config.toml` if your organization uses Codex.

Provider API keys stay centralized in LangSmith workspace secrets.

## Group calls into conversation threads

The gateway maps recognized coding-agent session headers to LangSmith `thread_id` metadata. Calls with the same ID belong to the same conversation thread within a tracing project.

Header detection works across all providers, request paths, and API formats. The gateway checks these headers in order:

1. `X-Claude-Code-Session-Id`
2. `X-Deepseek-Harness-Session-Id`
3. `thread-id`
4. `thread_id`
5. `session-id`
6. `session_id`

The gateway trims whitespace, skips blank values, and uses the first nonblank header value.

If no header supplies an ID, the gateway can read the ID from the body of a Chat Completions or Responses request. It uses the `conversation` field, either a string or an object's `id`, and falls back to `prompt_cache_key`. The gateway reads these fields only when it already loads the request body for another reason, such as a guard policy. Send a header for consistent threading.

To set a thread ID explicitly, send `X-Gateway-Thread-Id` or set `thread_id` in the JSON object in `X-Gateway-Metadata`. A nonblank explicit value overrides automatic detection. If both metadata headers specify a thread ID, `X-Gateway-Metadata` takes precedence.

If the gateway finds no explicit ID, recognized session header, or body field, it does not add `thread_id` metadata.

## Verify the setup

After configuring a coding agent, make a test call and confirm that:

1. The call succeeds and the agent receives a response.
2. A trace appears in the `gateway` tracing project in your LangSmith workspace.

If the call fails with a `401` or `403`, see [Fix authentication errors](../Authentication/Authenticate%20to%20the%20LLM%20Gateway.md#fix-authentication-errors). If a bring-your-own-key call fails with a `424` mentioning a missing provider key, ask a workspace admin to add the provider's key to workspace secrets. For details, see [Fix provider credential errors](../Authentication/Provider%20authentication.md#fix-provider-credential-errors).

## See also

* [Gateway Credits](../Models%20and%20reliability/Gateway%20Credits.md): call hosted models without a provider secret.
* [Direct model access](Direct%20model%20access.md): configure provider-native routes for coding agents that require them.
* [Spend policies](../Governance/Spend%20policies.md): set cost limits on developer LLM usage.
* [View LLM Gateway traces](../Observability/View%20LLM%20Gateway%20traces.md): understand where gateway traces appear.
