# Coding agent metadata contract

> The metadata schema that standardizes what trace metadata coding agents must emit when sending runs to LangSmith.

This schema is the authoritative contract for metadata that coding agents attach to LangSmith runs. It defines which fields are required on every run, which fields are expected when the runtime can supply them, and which fields apply only to specific run types.

Coding agent integrations use this schema to ensure their traces are consistently structured, queryable, and compatible with LangSmith's observability and filtering features.

## Supported integrations

The following integrations implement this schema:

| Integration | `ls_integration` value |
| - | - |
| [Claude Code](Trace%20Claude%20Code%20sessions.md) | `claude-code` |
| [OpenAI Codex](Trace%20OpenAI%20Codex%20sessions.md) | `openai-codex` |
| [Deep Agents](../Agent%20frameworks/Trace%20Deep%20Agents.md) | `deepagents-code` |
| [Cursor](Trace%20Cursor%20sessions.md) | `cursor` |
| [Pi](Trace%20Pi%20coding%20agent%20sessions.md) | `pi` |
| [Opencode](Trace%20OpenCode%20sessions.md) | `opencode` |
| [GitHub Copilot](Trace%20Visual%20Studio%20Code%20Copilot%20Chat%20sessions.md) | `copilot` |

## Global identity block

Every run type must include the following identity fields in its metadata:

| Field | Description |
| - | - |
| `ls_agent_type` | The run's type within the agent. Should be one of `"root"`, `"subagent"`, `"middleware"`, or `"compaction"`. |
| `ls_agent_purpose` | High-level purpose of the agent, for example `"coding"`. |
| `ls_integration` | Identifier of the integration emitting the run (see [Supported integrations](#supported-integrations)). |
| `ls_agent_runtime` | Human-readable runtime name, for example `"Claude Code 1.0.28"`. |
| `thread_id` | Stable identifier for the conversation thread. Used to group related runs in LangSmith's Threads view. |
| `ls_trace_schema_version` | Currently `"coding-agent-v1"`. |

## Availability tiers

Fields in this schema are marked with one of three availability tiers:

| Tier | Meaning |
| - | - |
| **always** | Must be present on every run. |
| **where\_known** | Required whenever the runtime can expose the value. Omit only when the runtime genuinely cannot provide the information. |
| **contextual** | Optional metadata. Omit when not applicable. |

## Run types

This schema distinguishes five run types. Some fields apply only to a subset of run types.

| Run type | Description |
| - | - |
| `root` | The top-level run representing a full agent turn or session. |
| `llm` | A language model call within a turn. |
| `tool` | A tool invocation within a turn. |
| `subagent` | A nested or delegated agent run. |
| `interrupted` | A run that was interrupted before completion. |

## Required fields by run type

### All run types

The [global identity block](#global-identity-block) fields are **always** required on every run type.

Additional fields required on all run types:

| Field | Tier | Description |
| - | - | - |
| `ls_agent_version` | `where_known` | Version string for the agent runtime, for example `"1.0.28"`. |
| `ls_git_repo` | `where_known` | Repository name, for example `"langchain-ai/langsmith-sdk"`. |
| `ls_git_repo_url` | `where_known` | Remote URL of the repository. |
| `ls_repo_provider` | `where_known` | Host of the repository, for example `"github"`. |
| `ls_git_branch` | `where_known` | Active Git branch in the repository being edited. |
| `ls_git_commit_hash` | `where_known` | Full SHA of the current Git commit. |
| `working_directory` | `where_known` | Absolute path of the working directory. |

The Claude Code, Codex and Cursor plugins also send each Git field under its old name (like `git_branch` and `git_commit_sha`) so existing filters keep working. LangSmith does the same for Copilot traces from the Local harness.

### `llm` runs

| Field | Tier | Description |
| - | - | - |
| `ls_model_name` | `where_known` | Model identifier, for example `"claude-opus-4-5"`. |
| `ls_provider` | `where_known` | Model provider, for example `"anthropic"`. |

### `tool` runs

| Field | Tier | Description |
| - | - | - |
| `ls_tool_name` | `always` | Name of the tool invoked, for example `"bash"` or `"computer"`. |

### `subagent` runs

| Field | Tier | Description |
| - | - | - |
| `ls_subagent_id` | `always` | Stable identifier for the subagent. |
| `ls_subagent_type` | `always` | Type or role of the subagent, for example `"researcher"`. |

### `interrupted` runs

Interrupted runs carry the same fields as `root` runs. The run type itself signals the abnormal termination state; no additional required fields are added.

## Related

* [Metadata parameters reference](../../Manual%20instrumentation/Metadata%20parameters%20reference.md): `ls_` prefixed fields used in LangSmith runs generally.
* [Add metadata and tags](../../../Configuration%20%26%20troubleshooting/Data%20%26%20privacy/Add%20metadata%20and%20tags%20to%20traces.md): how to attach metadata to traces using the LangSmith SDK.
