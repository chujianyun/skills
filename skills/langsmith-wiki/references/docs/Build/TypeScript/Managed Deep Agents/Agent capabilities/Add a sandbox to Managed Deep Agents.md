# Add a sandbox to Managed Deep Agents

> Configure an isolated filesystem and shell for a managed deep agent.

A sandbox gives a managed deep agent an isolated filesystem and shell for working with files, running code, and executing commands.

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

Put the sandbox declaration under `sandbox/`. Add `sandbox/setup.sh` only if you want to provision a snapshot:

```text
my-agent/
  agent.ts
  sandbox/
    index.ts
    setup.sh   # optional
```

For the full project layout, see [Project structure](../Get%20started/Managed%20Deep%20Agents%20project%20structure.md).

## Configure a sandbox

Use a sandbox when the agent needs to write files, run code, or execute shell commands.

`mda init` scaffolds a sandbox declaration. Managed Deep Agents enables the sandbox only while the `sandbox/` directory is present.

`mda init` does not create `setup.sh`. Add that file yourself if the snapshot should install packages, clone a tree, or otherwise change the image.

Managed Deep Agents uses [LangSmith Sandboxes](../../../../Deploy/Sandboxes/LangSmith%20Sandboxes.md) for this backend. Reuse is always one sandbox per durable thread.

Declare the sandbox with `defineSandbox`:

```ts sandbox/index.ts
import { defineSandbox } from "managed-deepagents";

export const sandbox = defineSandbox({
  idleTtlSeconds: 600,
  defaultTimeout: 600,
});
```

| Option | Default | Description |
| - | - | - |
| `idleTtlSeconds` | `600` | Seconds of inactivity before the sandbox and its contents are deleted. Deletion is not recoverable. |
| `defaultTimeout` | `600` | Seconds allowed for each command. |

## Configure the sandbox proxy

The sandbox proxy injects headers into matching outbound requests and controls which destinations the sandbox can reach. The proxy runs outside the sandbox, so sandbox code can call authenticated APIs without handling the credentials.

For example, to call the OpenAI API from the sandbox, store `OPENAI_API_KEY` in your LangSmith workspace secrets and configure this proxy rule:

```ts sandbox/index.ts
import { defineSandbox } from "managed-deepagents";

export const sandbox = defineSandbox({
  proxyConfig: {
    rules: [
      {
        name: "openai-api",
        match_hosts: ["api.openai.com"],
        headers: [
          {
            name: "Authorization",
            type: "workspace_secret",
            value: "Bearer {OPENAI_API_KEY}",
          },
        ],
      },
    ],
  },
});
```

For configuration options and network restrictions, see [Sandbox auth proxy](../../../../Deploy/Sandboxes/Sandbox%20auth%20proxy.md).

### Use connections in proxy headers

Use [Connections](Manage%20connections.md) in sandboxes to authenticate CLI commands and API requests.

For example, to call the GitHub API from the sandbox as the current user, create the `github` connection first, then configure the proxy:

```ts sandbox/index.ts
import { bearer, connections, defineSandbox } from "managed-deepagents";

const github = connections.get("github", { type: "user" });

export const sandbox = defineSandbox({
  proxyConfig: {
    rules: [
      {
        name: "github-api",
        match_hosts: ["api.github.com"],
        headers: [{ name: "Authorization", value: bearer(github) }],
      },
    ],
    access_control: { allow_list: ["api.github.com"] },
  },
});
```

Use a connection reference as the header value, or format it with `bearer(ref)` or `basic(username, ref)`. Omit the header's `type` for connection values. Managed Deep Agents sets it to `opaque`.

## Provision a snapshot

If `sandbox/setup.sh` exists, `mda deploy` and `mda dev` run the script once and save the resulting environment as a snapshot. Modifications from that run, such as cloned repositories and installed packages, persist in the snapshot. New threads clone that snapshot instead of running `setup.sh`. The snapshot is reused until `setup.sh` changes, at which point it is rebuilt.

The script runs with `bash -e`. A non-zero exit fails the snapshot and the deploy or `mda dev` session. LangSmith does not update the live deployment to the failed snapshot. Any previously successful snapshot continues to serve.

```bash sandbox/setup.sh
#!/usr/bin/env bash
set -euo pipefail

apt-get update && apt-get install -y jq
mkdir -p /workspace
```

Project `.env` values that deploy forwards are available as environment variables when `setup.sh` runs, for example a token used to clone a private repo. Thread sandboxes that clone the snapshot do not inherit those variables. Do not write secrets onto the filesystem while `setup.sh` runs; anything on disk is part of every thread's image.

Editing `setup.sh` and redeploying does not wipe `/workspace` on live threads. Those boxes keep the files they already have. A new thread clones the new snapshot.

## Choose a bake base

With no bake base, LangSmith's default sandbox template is the starting point. To start from something else, set exactly one of these:

| Option | Use |
| - | - |
| `snapshotName` | LangSmith snapshot name. Tags are allowed. |
| `snapshotId` | LangSmith snapshot id. |
| `dockerImage` | Published Docker image. |

```ts sandbox/index.ts
import { defineSandbox } from "managed-deepagents";

export const sandbox = defineSandbox({
  idleTtlSeconds: 600,
  dockerImage: "python:3.12-slim",
});
```

For a private image, pass the image and a `registry`. Managed Deep Agents creates or updates a deployment-owned Host registry at bake time. Only the variable name is compiled; the credential value does not enter the build or the snapshot.

Name the password in `passwordEnv`:

```ts sandbox/index.ts
import { defineSandbox } from "managed-deepagents";

export const sandbox = defineSandbox({
  dockerImage: "ghcr.io/acme/agent-base:1",
  registry: {
    url: "ghcr.io",
    username: "octocat",
    passwordEnv: "GHCR_TOKEN",
  },
});
```

Put `GHCR_TOKEN` in the project `.env` or the process environment. After bake, Managed Deep Agents does not forward that value to the running Agent Server.

## How the agent uses the sandbox

The agent uses built-in filesystem tools such as [`ls`](https://docs.langchain.com/oss/javascript/deepagents/tools#built-in-harness-tools), [`read_file`](https://docs.langchain.com/oss/javascript/deepagents/tools#built-in-harness-tools), [`write_file`](https://docs.langchain.com/oss/javascript/deepagents/tools#built-in-harness-tools), [`edit_file`](https://docs.langchain.com/oss/javascript/deepagents/tools#built-in-harness-tools), [`delete`](https://docs.langchain.com/oss/javascript/deepagents/tools#built-in-harness-tools), [`glob`](https://docs.langchain.com/oss/javascript/deepagents/tools#built-in-harness-tools), and [`grep`](https://docs.langchain.com/oss/javascript/deepagents/tools#built-in-harness-tools), and runs shell commands with [`execute`](https://docs.langchain.com/oss/javascript/deepagents/tools#built-in-harness-tools). Use [instructions](Add%20instructions%20to%20Managed%20Deep%20Agents.md) to specify where the agent should work and what it must not modify.

## Read and write sandbox files from code

[Authored tools](Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md) and [middleware](Add%20custom%20middleware%20to%20Managed%20Deep%20Agents.md) reach the sandbox filesystem through `runtime.backend`. Use it when your own code needs a file, rather than prompting the agent to fetch one for you.

> [!NOTE]
>
> `runtime.backend` requires `managed-deepagents>=0.8.0`.

Annotate the `runtime` parameter to receive the typed surface:

```ts tools/report.ts
import { tool } from "langchain";
import type { ManagedDeepAgentRuntime } from "managed-deepagents";
import { z } from "zod";

export const writeReport = tool(
  async ({ summary }, runtime: ManagedDeepAgentRuntime) => {
    if (!runtime.backend) {
      throw new Error("write_report requires a sandbox");
    }
    const result = await runtime.backend.write("/workspace/report.txt", summary);
    if (result.error) {
      throw new Error(result.error);
    }
    return "/workspace/report.txt";
  },
  {
    name: "write_report",
    description: "Write a summary to the sandbox and return its path.",
    schema: z.object({
      summary: z.string().describe("Report body to store."),
    }),
  },
);
```

Each operation binds to the sandbox of the thread handling the current run, so two threads reading `/workspace/report.txt` see their own copy. The backend resolves lazily, and a tool that never touches it never provisions a sandbox.

### Available operations

| Method | Purpose |
| - | - |
| `ls(path)` | List a directory. |
| `read(filePath, offset, limit)` | Read text, 2000 lines by default. |
| `readRaw(filePath)` | Read a file without line formatting. |
| `write(filePath, content)` | Write text, replacing any existing file. |
| `edit(filePath, oldString, newString, replaceAll)` | Replace a substring in place. |
| `delete(filePath)` | Remove a file. |
| `grep(pattern, path, glob, maxCount)` | Search file contents. |
| `glob(pattern, path)` | Match paths. |
| `execute(command)` | Run a shell command. |
| `uploadFiles(files)` | Write `Uint8Array` content from `[path, content]` pairs. |
| `downloadFiles(paths)` | Read each path as a `Uint8Array`. |

Every method returns a promise.

Arguments and return types come from the Deep Agents backend contract. See [Backends](https://docs.langchain.com/oss/javascript/deepagents/backends.md).

### Transfer binary files

`upload_files` and `download_files` move raw bytes, so they suit images, archives, and any other file that text operations would corrupt. Download returns the bytes for each requested path:

```ts tools/checksum.ts
import { createHash } from "node:crypto";

import { tool } from "langchain";
import type { ManagedDeepAgentRuntime } from "managed-deepagents";
import { z } from "zod";

export const checksumFile = tool(
  async ({ filePath }, runtime: ManagedDeepAgentRuntime) => {
    if (!runtime.backend) {
      throw new Error("checksum_file requires a sandbox");
    }
    const [result] = await runtime.backend.downloadFiles([filePath]);
    if (result.error || !result.content) {
      throw new Error(result.error ?? "file_not_found");
    }
    return createHash("sha256").update(result.content).digest("hex");
  },
  {
    name: "checksum_file",
    description: "Return the SHA-256 checksum of a sandbox file.",
    schema: z.object({
      filePath: z.string().describe("Absolute path inside the sandbox."),
    }),
  },
);
```

Upload takes path and content pairs, one per file:

```ts
const [uploaded] = await runtime.backend.uploadFiles([
  ["/workspace/logo.png", payload],
]);
if (uploaded.error) {
  throw new Error(uploaded.error);
}
```

Each result carries `path` and `error`, and a download also carries `content`. On failure, `error` is one of `file_not_found`, `permission_denied`, `is_directory`, or `invalid_path`, and the downloaded `content` is empty. Check `error` rather than assuming the transfer succeeded.

### Limits

`runtime.backend` covers the sandbox only. It has no route to [Context Hub](../Build%20and%20deploy/Manage%20Context%20Hub%20for%20Managed%20Deep%20Agents.md), so [skills](Add%20skills%20to%20Managed%20Deep%20Agents.md), [instructions](Add%20instructions%20to%20Managed%20Deep%20Agents.md), and [memory](Add%20memory%20to%20Managed%20Deep%20Agents.md) are not reachable through it.

Without a sandbox, `runtime.backend` is `undefined`. Guard on it before every call, because a project can remove `sandbox/` after the tool ships.

`delete`, `uploadFiles`, and `downloadFiles` depend on the installed backend and throw when it does not implement them. A root `glob` returns an error instead of provisioning a sandbox.

## Disable the sandbox

Delete the `sandbox/` directory to opt out, such as for an agent that only needs its prompt, memory, and tools.

For existing deployments, deleting the deployment with `mda delete` also deletes the managed sandboxes associated with it, the `{deployment}--setup-*` recipe snapshots, and the deployment-owned registry when one exists.

## Deployment

Managed Deep Agents owns sandbox naming, recipe bake, reuse, recovery, and cleanup. Each durable thread gets its own sandbox, cloned from the current recipe snapshot. For platform-level lifecycle details, see [Sandboxes](../../../../Deploy/Sandboxes/LangSmith%20Sandboxes.md).

## When to use a sandbox

| Goal | Use |
| - | - |
| Write files, run code, or execute shell commands in isolation | Sandbox |
| Store durable knowledge across threads | [Memory](Add%20memory%20to%20Managed%20Deep%20Agents.md) |
| Always-on behavior without a filesystem | [Instructions](Add%20instructions%20to%20Managed%20Deep%20Agents.md) |

For more information, see [Project structure](../Get%20started/Managed%20Deep%20Agents%20project%20structure.md). For a project that publishes a larger sandbox snapshot before deploy, see the [design agent template](../Templates/Deploy%20the%20open-source%20design%20agent.md).
