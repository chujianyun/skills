# LangSmith Sandboxes

> Use LangSmith managed sandboxes to safely execute code and interact with the filesystem in isolated environments.

Sandboxes are isolated environments that allow agents to safely execute potentially risky operations, like running arbitrary code or interacting with the filesystem, without affecting your main infrastructure.

From the [LangSmith homepage](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-sandboxes), select **Sandboxes** to manage all your sandbox resources.

![Sandboxes overview page](../../../assets/images/e59e49377a5b-sb-overview.png)

## Availability

Sandboxes are generally available in all [LangSmith Cloud regions](../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md#regional-storage), on [BYOC](../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md), and on [self-hosted](../../LangSmith%20setup/Self-hosted/Install%20an%20instance/Additional%20features/Enable%20Sandboxes/Enable%20Sandboxes%20on%20self-hosted%20LangSmith.md) deployments. On BYOC, use an API key that belongs to a BYOC workspace.

For the self-hosted infrastructure model, scaling, and upgrades, see [Self-hosted Sandbox architecture](../../LangSmith%20setup/Self-hosted/Install%20an%20instance/Additional%20features/Enable%20Sandboxes/Self-hosted%20Sandbox%20architecture.md).

## Network access

Restricted egress applies to non-Enterprise organizations by default and to organizations that request it. Organizations with an approved exemption can use unrestricted egress. Restricted sandboxes use a managed allowlist for common package registries, source repositories, and model APIs. LangSmith blocks destinations outside the allowlist, even if you add them to a sandbox's proxy configuration.

If you need unrestricted egress, [file a support ticket](https://support.langchain.com) with your organization or workspace ID, region, required destinations and ports, and use case. For more information, see [restricted egress and access requests](Sandbox%20auth%20proxy.md#organization-level-restricted-egress).

## Get started

### 1. Install the SDK

```bash Python
# uv
uv add langsmith

# pip
pip install langsmith
```

```bash TypeScript
npm install langsmith
```

### 2. Set your API key

```bash
export LANGSMITH_API_KEY="<API_KEY>"
```

### 3. Create and run a sandbox

```python Python
from langsmith.sandbox import SandboxClient

client = SandboxClient()

with client.sandbox() as sb:
    result = sb.run("python3 -c 'print(2 + 2)'")
    print(result.stdout)  # "4\n"
```

```ts TypeScript
import { SandboxClient } from "langsmith/sandbox";

const client = new SandboxClient();
const sandbox = await client.createSandbox();
const result = await sandbox.run("node -e 'console.log(2 + 2)'");
console.log(result.stdout); // "4\n"
await sandbox.delete();
```

> [!TIP]
>
> Prefer the command line? The [Sandbox CLI](Sandbox%20CLI.md) lets you create sandboxes, run commands, and open interactive shells without writing any code.

### 4. Use sandboxes with your agents

To wire sandboxes into agent code, see the open source documentation:

* **Deep Agents**: [Use `LangSmithSandbox` as a backend](https://docs.langchain.com/oss/python/integrations/sandboxes/langsmith), covering installation, backend creation, and cleanup.
* **Sandboxes as agent backends**: [Configure any sandbox as the execution backend](https://docs.langchain.com/oss/python/deepagents/sandboxes.md) to give your agent `execute` and filesystem tools automatically.
* **LangChain / LangGraph integrations**: Use LangSmith sandboxes as a first-party option, or [connect third-party providers](https://docs.langchain.com/oss/python/integrations/sandboxes.md) such as AgentCore, Daytona, E2B, Modal, Runloop, and Vercel.

## Resources

> [card] [Snapshots](Sandbox%20snapshots.md)
>
> Build filesystem images from Docker images or capture a running sandbox, then boot sandboxes from them.

> [card] [Service URLs](Sandbox%20service%20URLs.md)
>
> Access HTTP services running inside sandboxes via authenticated URLs.

> [card] [Auth proxy](Sandbox%20auth%20proxy.md)
>
> Inject credentials into outbound API requests without hardcoding secrets.

> [card] [Mounts](Sandbox%20mounts.md)
>
> Attach S3 buckets, GCS buckets, and public Git repositories to a sandbox filesystem.

> [card] [Permissions](Sandbox%20access%20permissions.md)
>
> Control which workspace members can interact with a sandbox after it is created.

> [card] [CLI](Sandbox%20CLI.md)
>
> Build snapshots, manage sandboxes, open consoles, and tunnel TCP ports from the command line.

> [card] [SDK usage](Sandbox%20SDK%20usage.md)
>
> Create and manage sandboxes programmatically with the Python or TypeScript SDK.

> [card] [Self-hosted setup](../../LangSmith%20setup/Self-hosted/Install%20an%20instance/Additional%20features/Enable%20Sandboxes/Enable%20Sandboxes%20on%20self-hosted%20LangSmith.md)
>
> Enable Sandboxes on self-hosted LangSmith deployments with Helm or Terraform.

> [card] [Harbor](../../Test/Evaluators/Frameworks%20%26%20integrations/Harbor%20integrations.md#sandboxes)
>
> Run Harbor evaluations and rollouts on LangSmith sandboxes.
