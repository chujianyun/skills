# OpenWiki

> CLI that writes and maintains agent wikis so coding agents work faster

OpenWiki is an open source CLI that writes and maintains a Markdown wiki about your codebase or personal knowledge. The wiki captures details such as architecture, integrations, evals, and workflows so [coding agents](../Deep%20Agents%20overview.md) can use it as durable context instead of rediscovering the repository on every task.

That makes agent work faster and cheaper in tokens: agents read a curated wiki first, then inspect source only where they need more detail. Humans can browse the same Markdown (and the local [visualizer](https://docs.langchain.com/oss/openwiki/visualize.md)), but the primary audience is agents.

OpenWiki is built on [Deep Agents](../Deep%20Agents%20overview.md) and supports tracing with [LangSmith](https://docs.langchain.com/langsmith/observability-quickstart.md).

## Get started

Install the CLI, then initialize documentation for the current repository:

```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
npm install -g openwiki
openwiki --init
```

See the [Quickstart](https://docs.langchain.com/oss/openwiki/quickstart.md) to choose a model provider, generate docs, and keep them up to date. To run OpenWiki inside a coding agent instead of a standalone model session, see [Coding-agent integrations](https://docs.langchain.com/oss/openwiki/integrations.md). To search an existing wiki or group related repositories, see [Search and link wikis](https://docs.langchain.com/oss/openwiki/search-and-link.md).

## Modes

OpenWiki has two modes:

| Mode | Command | Output | Use when |
| - | - | - | - |
| **Code** (default) | `openwiki` / `openwiki code` | `openwiki/` in the current repository | You want repository context and documentation for coding agents |
| **Personal** | `openwiki personal` | `~/.openwiki/wiki` | You want a local personal brain from configured sources |

Bare `openwiki --init` and `openwiki --update` run in code mode. Use `openwiki personal --init` or `openwiki personal --update` for the personal wiki.

## Capabilities

> [card] [Repository wikis](https://docs.langchain.com/oss/openwiki/code-mode.md)
>
> Generate Markdown docs under `openwiki/`, then wire them into `AGENTS.md` (and `CLAUDE.md` when present) so coding agents can find them.

> [card] [Coding-agent integrations](https://docs.langchain.com/oss/openwiki/integrations.md)
>
> Run OpenWiki inside Codex, Claude Code, OpenCode, Cursor, IBM Bob, Kiro, Oh My Pi, Antigravity, or Pi.

> [card] [Search and link](https://docs.langchain.com/oss/openwiki/search-and-link.md)
>
> Query wiki pages over MCP and group related repository wikis into workspaces.

> [card] [Personal brain](https://docs.langchain.com/oss/openwiki/personal-mode.md)
>
> Build a local wiki from git repos, Custom MCP, Gmail, Notion, web search, Hacker News, and X/Twitter.

> [card] [Grounded Claims](https://docs.langchain.com/oss/openwiki/code-mode.md#grounded-claims)
>
> Track material facts back to versioned source evidence and refresh pages when that evidence changes.

> [card] [Automatic updates](https://docs.langchain.com/oss/openwiki/automate-updates.md)
>
> Refresh docs from GitHub Actions, GitLab CI, or Bitbucket Pipelines and open a PR when content changes.

> [card] [Model providers](https://docs.langchain.com/oss/openwiki/providers.md)
>
> Use OpenAI, Anthropic, Gemini, Bedrock, OpenRouter, GitHub Copilot, IBM Bob, and other providers out of the box.

> [card] [Open Knowledge Format](https://docs.langchain.com/oss/openwiki/code-mode.md#open-knowledge-format)
>
> Emit OKF v0.2 Markdown bundles with front matter, indexes, and linked concepts.

> [card] [LangSmith tracing](https://docs.langchain.com/oss/openwiki/quickstart.md#trace-with-langsmith)
>
> Trace documentation runs with LangSmith.

## Next steps

> [card] [Quickstart](https://docs.langchain.com/oss/openwiki/quickstart.md)
>
> Install OpenWiki, configure a provider, and generate your first wiki.

> [card] [CLI reference](https://docs.langchain.com/oss/openwiki/cli-reference.md)
>
> Review commands, flags, and connector subcommands.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/openwiki/overview.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
