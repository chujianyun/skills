# Permissions

> Control filesystem access with declarative permission rules for Deep Agents

Control which files and directories an agent can read or write to using declarative permission rules. Pass a list of rules to `permissions=` and the agent's built-in filesystem tools respect them.

> [!NOTE]
>
> Permissions require `deepagents>=0.5.2`.

Permissions only apply to the built-in filesystem tools (`ls`, `read_file`, `glob`, `grep`, `write_file`, `edit_file`, `delete`). Custom tools and MCP tools that access the filesystem are not covered. Permissions also do not apply to [sandbox backends](Sandboxes.md), which support arbitrary command execution via the `execute` tool.

> [!TIP]
>
> Use `permissions` when you need **path-based allow/deny rules** on the built-in filesystem tools. Use [backend policy hooks](Backends.md#add-policy-hooks) when you need custom validation logic (rate limiting, audit logging, content inspection) or need to control custom tools.

## Basic usage

Pass a list of [`FilesystemPermission`](https://reference.langchain.com/python/deepagents/middleware/permissions/FilesystemPermission) rules to [`create_deep_agent`](https://reference.langchain.com/python/deepagents/graph/create_deep_agent). Rules are evaluated in declaration order. The first matching rule wins. If no rule matches, the operation is allowed.

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import FilesystemPermission, create_deep_agent


# Read-only agent: deny all writes
agent = create_deep_agent(
    model=model,
    backend=backend,
    permissions=[
        FilesystemPermission(
            operations=["write"],
            paths=["/**"],
            mode="deny",
        ),
    ],
)
```

## Rule structure

Each `FilesystemPermission` has three fields:

| Field | Type | Description |
| - | - | - |
| `operations` | `list["read" \| "write"]` | Operations this rule applies to. `"read"` covers `ls`, `read_file`, `glob`, `grep`. `"write"` covers `write_file`, `edit_file`, `delete`. |
| `paths` | `list[str]` | Glob patterns for matching file paths (e.g., `["/workspace/**"]`). Supports `**` for recursive matching and `{a,b}` for alternation. |
| `mode` | `"allow" \| "deny" \| "interrupt"` | Whether to allow, deny, or pause for human approval on matching operations. Defaults to `"allow"`. See [Pause for human approval](#pause-for-human-approval). |

Rules use first-match-wins evaluation: the first rule whose `operations` and `paths` match the current call determines the outcome. If no rule matches, the call is **allowed** (permissive default).

## Pause for human approval

> [!NOTE]
>
> The `"interrupt"` mode requires `deepagents>=0.6.8`.

Set `mode="interrupt"` to pause for human approval instead of allowing or denying a matching operation outright. When the agent calls a built-in write tool (`write_file`, `edit_file`, `delete`) on a path that matches an interrupt-mode rule, `create_deep_agent` raises a human-in-the-loop interrupt rather than running the tool, and a reviewer can approve, edit, or reject the call.

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import FilesystemPermission, create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver

agent = create_deep_agent(
    model=model,
    permissions=[
        # Pause for approval before writing anything under /secrets.
        FilesystemPermission(
            operations=["write"],
            paths=["/secrets/**"],
            mode="interrupt",
        ),
    ],
    # Interrupt mode requires a checkpointer to pause and resume.
    checkpointer=InMemorySaver(),
)
```

Interrupt-mode rules are wired into the agent's human-in-the-loop middleware automatically and merge with any `interrupt_on` you pass, so you handle and resume them the same way as tool-call interrupts. See [Human-in-the-loop](../Steering/Human-in-the-loop.md) for the resume flow.

> [!NOTE]
>
> Deleting a directory is all-or-nothing: `delete` checks the `write` permission on the target and every descendant path, and refuses the entire operation if any of them is denied, rather than removing part of the tree. `delete` applies this same conservative check to an existing empty directory, since it is still a directory rather than a confirmed leaf target.
>
> Deleting a plain file is an exact-match case instead: `delete` resolves the target the same way `write_file` and `edit_file` do, using first-match-wins evaluation, so an earlier, narrower `allow` rule wins over a later catch-all `deny`. `deepagents>=0.7.3` is required for this exact-match behavior.

> [!TIP]
>
> Anchor interrupt patterns with a literal leading segment (for example, `/secrets/**` or `/projects/*/secrets/**`). Bulk tools (`ls`, `glob`, `grep`, and `delete` on a directory) fire the interrupt when their search subtree could overlap the rule's anchored prefix, so a fully unanchored pattern like `/**/secrets` conservatively over-fires.

## Examples

### Isolate to a workspace directory

Allow reads and writes only under `/workspace/` and deny everything else:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
agent = create_deep_agent(
    model=model,
    backend=backend,
    permissions=[
        FilesystemPermission(
            operations=["read", "write"],
            paths=["/workspace/**"],
            mode="allow",
        ),
        FilesystemPermission(
            operations=["read", "write"],
            paths=["/**"],
            mode="deny",
        ),
    ],
)
```

### Protect specific files

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
agent = create_deep_agent(
    model=model,
    backend=backend,
    permissions=[
        FilesystemPermission(
            operations=["read", "write"],
            paths=["/workspace/.env", "/workspace/examples/**"],
            mode="deny",
        ),
        FilesystemPermission(
            operations=["read", "write"],
            paths=["/workspace/**"],
            mode="allow",
        ),
        FilesystemPermission(
            operations=["read", "write"],
            paths=["/**"],
            mode="deny",
        ),
    ],
)
```

### Read-only memory

Allow the agent to read memory files but prevent it from modifying them. This is useful for organization-wide policies or shared knowledge bases that should only be updated by application code. See [read-only vs writable memory](../Context%20management/Memory.md#read-only-vs-writable-memory) for more context.

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend

agent = create_deep_agent(
    model=model,
    backend=CompositeBackend(
        default=StateBackend(),
        routes={
            "/memories/": StoreBackend(
                namespace=lambda rt: (rt.server_info.user.identity,),
            ),
            "/policies/": StoreBackend(
                namespace=lambda rt: (rt.context.org_id,),
            ),
        },
    ),
    permissions=[
        FilesystemPermission(
            operations=["write"],
            paths=["/memories/**", "/policies/**"],
            mode="deny",
        ),
    ],
)
```

### Deny all access

Block all reads and writes. This is a restrictive baseline you can layer more specific allow rules on top of:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
agent = create_deep_agent(
    model=model,
    backend=backend,
    permissions=[
        FilesystemPermission(
            operations=["read", "write"],
            paths=["/**"],
            mode="deny",
        ),
    ],
)
```

### Rule ordering

Because of first-match-wins, rule order matters. Place more specific rules before broader ones:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
# Correct: deny .env, allow workspace, deny everything else
correct_permissions = [
    FilesystemPermission(
        operations=["read", "write"],
        paths=["/workspace/.env"],
        mode="deny",
    ),
    FilesystemPermission(
        operations=["read", "write"],
        paths=["/workspace/**"],
        mode="allow",
    ),
    FilesystemPermission(
        operations=["read", "write"],
        paths=["/**"],
        mode="deny",
    ),
]

# Bug: /workspace/** matches .env first, so the deny never triggers
incorrect_permissions = [
    FilesystemPermission(
        operations=["read", "write"],
        paths=["/workspace/**"],
        mode="allow",
    ),
    FilesystemPermission(
        operations=["read", "write"],
        paths=["/workspace/.env"],
        mode="deny",  # never reached
    ),
    FilesystemPermission(
        operations=["read", "write"],
        paths=["/**"],
        mode="deny",
    ),
]
```

## Subagent permissions

[Subagents](../Delegation/Subagents.md) inherit the parent agent's permissions by default. To give a subagent different permissions, set the `permissions` field in its spec. This **replaces** the parent's rules entirely.

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
agent = create_deep_agent(
    model=model,
    backend=backend,
    permissions=[
        FilesystemPermission(
            operations=["read", "write"],
            paths=["/workspace/**"],
            mode="allow",
        ),
        FilesystemPermission(
            operations=["read", "write"],
            paths=["/**"],
            mode="deny",
        ),
    ],
    subagents=[
        {
            "name": "auditor",
            "description": "Read-only code reviewer",
            "system_prompt": "Review the code for issues.",
            "permissions": [
                FilesystemPermission(
                    operations=["write"],
                    paths=["/**"],
                    mode="deny",
                ),
                FilesystemPermission(
                    operations=["read"],
                    paths=["/workspace/**"],
                    mode="allow",
                ),
                FilesystemPermission(
                    operations=["read"],
                    paths=["/**"],
                    mode="deny",
                ),
            ],
        }
    ],
)
```

## Composite backends

When using a [`CompositeBackend`](https://reference.langchain.com/python/deepagents/backends/composite/CompositeBackend) with a sandbox default, every permission path must be scoped under a known route prefix. Sandboxes support arbitrary command execution, so path-based restrictions alone cannot prevent filesystem access through shell commands. Scoping permissions to route-specific [backends](Backends.md) avoids this conflict.

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents.backends import CompositeBackend


composite = CompositeBackend(
    default=sandbox,
    routes={"/memories/": memories_backend},
)

# Works: permissions are scoped to the /memories/ route
agent = create_deep_agent(
    model=model,
    backend=composite,
    permissions=[
        FilesystemPermission(
            operations=["write"],
            paths=["/memories/**"],
            mode="deny",
        ),
    ],
)
```

Permissions that include paths outside any route raise `NotImplementedError`:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
# Raises NotImplementedError: /workspace/** hits the sandbox default
try:
    create_deep_agent(
        model=model,
        backend=composite,
        permissions=[
            FilesystemPermission(
                operations=["write"],
                paths=["/workspace/**"],
                mode="deny",
            ),
        ],
    )
except NotImplementedError:
    pass

# Also raises: /** covers both routes and the default
try:
    create_deep_agent(
        model=model,
        backend=composite,
        permissions=[
            FilesystemPermission(
                operations=["read"],
                paths=["/**"],
                mode="deny",
            ),
        ],
    )
except NotImplementedError:
    pass
```

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/deepagents/permissions.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
