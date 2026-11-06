# Profiles

> Package per-provider and per-model defaults that Deep Agents applies when a model is selected

**Harness profiles** let you customize the Deep Agents harness for a specific model or provider. You can adjust system prompts and tool descriptions, exclude tools or middleware, add middleware, and configure the general-purpose subagent. Deep Agents applies these settings whenever you select a matching model, without requiring changes to your agent creation code.

**Provider profiles** define default settings for creating a model, such as temperature and timeout. These settings do not affect the harness. Most callers do not need provider profiles. They are useful when packaging an integration that needs shared defaults, credential checks, or settings computed at runtime.

## Harness profiles

Deep Agents includes **built-in harness profiles** with default settings for specific providers and models.

Use `HarnessProfile` to define settings that `create_deep_agent` applies after constructing the chat model:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import (
    GeneralPurposeSubagentProfile,
    HarnessProfile,
    register_harness_profile,
)

register_harness_profile(
    "openai:gpt-6-astra",
    HarnessProfile(
        system_prompt_suffix="Respond in under 100 words.",
        excluded_tools={"execute"},
        excluded_middleware={"SummarizationMiddleware"},
        general_purpose_subagent=GeneralPurposeSubagentProfile(enabled=False),
    ),
)
```

**base\_system\_prompt** `string`

Set the profile's base instructions. For the main agent, these follow the caller's system instructions; no base instructions are added by default. For declarative subagents, this replaces their authored system prompt.

**system\_prompt\_suffix** `string`

Append text after the caller's instructions and the profile's base instructions. Applied to the main agent, declarative subagents, and the auto-added general-purpose subagent.

**tool\_description\_overrides** `Mapping[str, str]`

Override individual tool descriptions, keyed by tool name.

**excluded\_tools** `frozenset[str]`

Remove specific harness-level tools from the tool set. Matched by tool name (string), applied as a post-injection filter so it can drop both user-supplied tools and tools added by harness middleware. See [Running without the default filesystem tools](../Deep%20Agents%20overview.md#virtual-filesystem-access) for a worked example.

**excluded\_middleware** `frozenset[type[AgentMiddleware] | str]`

Strip specific middleware classes from the [Deep Agents stack](../Get%20started/Customize%20Deep%20Agents.md#deep-agents-stack). Accepts middleware classes or string names.

**extra\_middleware** `Sequence[AgentMiddleware] | Callable[[], Sequence[AgentMiddleware]]`

Append middleware to every stack this profile applies to. See the [Deep Agents stack](../Get%20started/Customize%20Deep%20Agents.md#full-stack) for the built-in ordering.

**general\_purpose\_subagent** `GeneralPurposeSubagentProfile`

Disable, rename, or re-prompt the general-purpose subagent. When this field's `system_prompt` is set alongside `base_system_prompt`, the general-purpose-specific subagent prompt wins—see [General-purpose subagent prompt](../Get%20started/Customize%20Deep%20Agents.md#general-purpose-subagent-prompt).

> [!NOTE]
>
> Caller-supplied `system_prompt=` always sits at the front of the assembled prompt, and `system_prompt_suffix` always sits at the end—regardless of which model is selected. The same overlay rules apply to subagents: each subagent re-runs profile resolution against its own model. See [System prompt](../Get%20started/Customize%20Deep%20Agents.md#system-prompt) for custom instructions and subagent prompt behavior.

> [!WARNING]
>
> To run an agent without the `task` tool, see [Running without subagents](../Delegation/Subagents.md#running-without-subagents)—set `general_purpose_subagent=GeneralPurposeSubagentProfile(enabled=False)` and pass no synchronous subagents via `subagents=`. `SubAgentMiddleware` (and the `task` tool) is only attached when at least one synchronous subagent exists, so this configuration leaves it out cleanly. Async subagents are unaffected.
>
> Listing `FilesystemMiddleware`, `SubAgentMiddleware`, or the internal permission middleware in `excluded_middleware` raises a `ValueError`—they're required scaffolding in the [Deep Agents stack](../Get%20started/Customize%20Deep%20Agents.md#deep-agents-stack). To hide their tools from the model without removing the middleware, use `excluded_tools` instead—see [Running without the default filesystem tools](../Deep%20Agents%20overview.md#virtual-filesystem-access).

Entries in `excluded_middleware` accept two forms:

* A middleware *class* (matched by exact type), or a plain string that matches `AgentMiddleware.name`. Use plain strings for built-ins and public aliases such as `"SummarizationMiddleware"`.
* An `module:Class` import ref (for example, `"my_pkg.middleware:TelemetryMiddleware"`) to target an exact middleware class from a config file. Import refs resolve lazily, so use them only for trusted local configuration—loading one imports Python code.

Register profiles before creating an agent. Pass a model string or a model object you construct yourself; see [Configure model parameters](../Get%20started/Models.md#configure-model-parameters) for examples. Harness profiles apply in both cases.

Provider profiles supply construction settings only when you pass a string.

> [accordion] Lookup order for preconfigured model instances
>
> When you pass a model object, the harness looks up its profile using the provider and identifier reported by that object.
>
> 1. Exact `provider:identifier` match
> 2. Identifier-only (only when the identifier already contains `:`)
> 3. Reported provider's defaults, or the identifier prefix's defaults if the provider is unknown
>
> Both exact candidates take precedence over provider defaults.

## Registration keys

Profile registrations use these keys:

* **Provider-level**—a bare provider name like `"openai"` applies to every model from that provider.
* **Model-level**—a fully qualified `provider:model` key like `"openai:gpt-6-astra"` applies only to that specific model.

When both a provider-level and a model-level profile exist, they are merged at resolution time. Unset model-level fields inherit from the provider-level profile; explicit model-level values override them.

Only the first colon separates the provider from the model identifier. For the hypothetical key `my_provider:my-model:tag`, the provider is `my_provider` and the complete model identifier is `my-model:tag`. Any additional colons are part of the model identifier.

For example, exclude a tool for a hypothetical provider's models, then customize the prompt suffix for one model:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import HarnessProfile, register_harness_profile

# Set defaults for a hypothetical provider.
register_harness_profile(
    "my_provider",
    HarnessProfile(
        excluded_tools=frozenset({"execute"}),
        system_prompt_suffix="Respond in under 500 words.",
    ),
)

# Override the prompt suffix for one model; inherit the excluded tool.
register_harness_profile(
    "my_provider:my-model:tag",
    HarnessProfile(system_prompt_suffix="Respond in under 100 words."),
)
```

An agent using the model-specific registration excludes `execute` and receives the 100-word suffix. Other models from `my_provider` exclude `execute` and receive the 500-word suffix.

Re-registering under an existing key merges the new profile on top of the prior one; it does not replace it. This also lets you customize a built-in profile by registering under its key. See [Merge semantics](#merge-semantics) for the per-field rules.

Continuing the example, exclude one more tool for the same model:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
register_harness_profile(
    "my_provider:my-model:tag",
    HarnessProfile(excluded_tools=frozenset({"grep"})),
)
```

Agents created afterward with this model exclude both `execute` and `grep` and retain the 100-word suffix. Other models keep the provider defaults.

> [!NOTE]
>
> There is no wildcard key that matches every provider. To apply the same overrides everywhere—say, dropping `SummarizationMiddleware` regardless of which model is selected—register the profile under each provider key you use. Profiles are intended for adjustments that depend on the model being selected. Global adjustments that should apply regardless of model should be made on the `create_deep_agent` call site.

## Merge semantics

| Field | Merge behavior |
| - | - |
| `base_system_prompt`, `system_prompt_suffix` | New value wins when set; otherwise inherits |
| `tool_description_overrides` | Mappings merge per key; new value wins on a shared key |
| `excluded_tools`, `excluded_middleware` | Set union |
| `extra_middleware` | Merged by concrete type: new instance replaces existing at its position, novel types append |
| `general_purpose_subagent` | Merged field-wise (unset fields inherit) |
| `init_kwargs` (provider) | Dicts merge key-wise; new value wins on a shared key |
| `pre_init` (provider) | Callables chain: existing runs first, then the new one |
| `init_kwargs_factory` (provider) | Factories chain with their outputs merged on every model construction |

## Provider profiles

A `ProviderProfile` supplies model-construction settings when you pass a `provider:model` string to `create_deep_agent`. For the hypothetical provider below, set defaults for all its models, then override the temperature for one model:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import ProviderProfile, register_provider_profile

register_provider_profile(
    "my_provider",
    ProviderProfile(init_kwargs={"temperature": 0.7, "timeout": 30}),
)
register_provider_profile(
    "my_provider:my-model:tag",
    ProviderProfile(init_kwargs={"temperature": 0}),
)
```

Constructing `my_provider:my-model:tag` uses `temperature=0` and inherits `timeout=30`. Other models from `my_provider` use `temperature=0.7` and `timeout=30`.

To increase this model's timeout, register again under its key:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
register_provider_profile(
    "my_provider:my-model:tag",
    ProviderProfile(init_kwargs={"timeout": 60}),
)
```

Future construction of this model uses `temperature=0` and `timeout=60`. These registrations leave existing model objects unchanged.

**init\_kwargs** `Mapping[str, Any]`

Static initialization arguments forwarded to `init_chat_model`.

**pre\_init** `Callable[[str], None]`

Side effects to run before construction (for example, credential validation).

**init\_kwargs\_factory** `Callable[[], dict[str, Any]]`

Kwargs derived from runtime state (for example, headers pulled from environment variables).

## Load profiles from config files

For YAML/JSON-backed workflows, use `HarnessProfileConfig`. It mirrors the declarative subset of `HarnessProfile` (prompt text, tool-description overrides, excluded tools and middleware, general-purpose subagent edits) and owns `to_dict` / `from_dict`. Runtime-only state—middleware instances, factories, and class-form `excluded_middleware` entries—stays on `HarnessProfile`.

`register_harness_profile` accepts either type, so config-backed callers don't need a manual conversion step:

```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
# openai.yaml
base_system_prompt: You are helpful.
system_prompt_suffix: Respond briefly.
excluded_tools:
  - execute
  - grep
excluded_middleware:
  - SummarizationMiddleware
  - my_pkg.middleware:TelemetryMiddleware
general_purpose_subagent:
  enabled: false
```

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import yaml
from deepagents import HarnessProfileConfig, register_harness_profile

with open("openai.yaml") as f:
    register_harness_profile(
        "openai",
        HarnessProfileConfig.from_dict(yaml.safe_load(f)),
    )
```

To go the other direction, `HarnessProfileConfig.from_harness_profile(...)` exports a runtime profile back to the declarative shape when it only uses serializable features:

* Class-form `excluded_middleware` entries serialize as a public alias (when the class exposes one via `serialized_name: ClassVar[str]`) or as a `module:Class` import ref.
* Non-empty `extra_middleware` and middleware classes declared in `__main__` or inside a function scope cannot be serialized—export raises `ValueError`.

## Ship a profile as a plugin

Distributable profiles can register themselves via `importlib.metadata` entry points instead of requiring callers to run `register_*_profile` by hand. Load order is **built-ins first, then entry-point plugins, then any direct `register_*_profile` calls in user code**; all three paths funnel through the same additive registration, so later registrations layer on top of earlier ones under the same key.

Declare an entry point in the distribution's own `pyproject.toml` under the appropriate group:

```toml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
[project.entry-points."deepagents.harness_profiles"]
my_provider = "my_pkg.profiles:register_harness"

[project.entry-points."deepagents.provider_profiles"]
my_provider = "my_pkg.profiles:register_provider"
```

Each target resolves to a zero-arg callable that performs the registrations when `deepagents.profiles` is imported:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import (
    HarnessProfile,
    ProviderProfile,
    register_harness_profile,
    register_provider_profile,
)


def register_harness() -> None:
    register_harness_profile(
        "my_provider",
        HarnessProfile(system_prompt_suffix="Batch independent tool calls in parallel."),
    )


def register_provider() -> None:
    register_provider_profile(
        "my_provider",
        ProviderProfile(init_kwargs={"temperature": 0}),
    )
```

## Related

* [Harness Overview](../Deep%20Agents%20overview.md)—harness capabilities overview
* [Models](../Get%20started/Models.md)—configure model providers and parameters
* [Customization](../Get%20started/Customize%20Deep%20Agents.md)—full `create_deep_agent` configuration surface

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/deepagents/profiles.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
