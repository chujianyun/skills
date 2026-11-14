# Sandbox mounts

> Mount S3 buckets, GCS buckets, public Git repositories, and Context Hub repos into LangSmith sandboxes.

Sandbox mounts attach external data sources to a sandbox filesystem when the sandbox is created. Use mounts when sandbox code needs direct file access to object storage buckets, public Git repositories, or [Context Hub](../Prompt%20%26%20Context%20Hub/Context%20Hub/Use%20the%20Context%20Hub.md) repos without copying the data into the sandbox image.

Mounts are configured through `mount_config` in Python or `mountConfig` in TypeScript. The SDK sends the mount specs to LangSmith and composes the required [auth proxy](Sandbox%20auth%20proxy.md) rules for provider credentials.

> [!NOTE]
>
> Sandbox mounts require `langsmith>=0.8.16` for Python or `langsmith>=0.7.10` for TypeScript. Context Hub mounts require `langsmith>=0.11.0` for Python or `langsmith>=0.8.11` for TypeScript.

> [!WARNING]
>
> When using static AWS keys or a GCP service account, store cloud credentials as LangSmith workspace secrets before creating the sandbox. S3 mounts authenticated with an IAM role do not require stored AWS access keys. Do not pass real cloud credentials as sandbox environment variables, command arguments, or files.

## Configure mount paths

Each mount has an `id`, a `type`, and a `mount_path` / `mountPath`. Bucket and Git mounts must use an absolute path under `/mnt/mounts`. Context Hub mount paths can be any absolute path outside the system directories, so an agent can read its context from the location it already expects.

Use stable paths that describe the mounted source:

| Source | Example path |
| - | - |
| S3 bucket prefix | `/mnt/mounts/customer-data` |
| GCS bucket prefix | `/mnt/mounts/eval-datasets` |
| Git repository | `/mnt/mounts/repo` |
| Context Hub repo | `/memories` |

Mount IDs can contain ASCII letters, digits, underscores, and hyphens. Do not reuse an ID or mount path within the same sandbox.

## Mount an S3 bucket

S3 mounts require AWS authentication. Use static access keys or an IAM role when your deployment and SDK support role authentication. The LangSmith UI also supports role setup. Both methods keep real AWS credentials outside the sandbox.

### Authenticate with static access keys

The SDK creates an AWS auth proxy rule from `aws_auth` / `awsAuth`, so the sandbox can access the bucket without seeing the real access keys.

```python Python
from langsmith.sandbox import (
    SandboxClient,
    aws_auth,
    mount_config,
    s3_mount,
    workspace_secret,
)

client = SandboxClient()

mount_cfg = mount_config(
    auth=[
        aws_auth(
            access_key_id=workspace_secret("SANDBOX_AWS_ACCESS_KEY_ID"),
            secret_access_key=workspace_secret("SANDBOX_AWS_SECRET_ACCESS_KEY"),
        )
    ],
    mounts=[
        s3_mount(
            id="customer_data",
            mount_path="/mnt/mounts/customer-data",
            bucket="example-bucket",
            prefix="datasets/customer-data",
            region="us-east-1",
            path_style=False,
            read_only=True,
        )
    ],
)

with client.sandbox(name="s3-mount-sandbox", mount_config=mount_cfg) as sb:
    result = sb.run("ls /mnt/mounts/customer-data")
    print(result.stdout)
```

```ts TypeScript
import {
  SandboxClient,
  awsAuth,
  mountConfig,
  s3Mount,
  workspaceSecret,
} from "langsmith/sandbox";

const client = new SandboxClient();

const mountCfg = mountConfig({
  auth: [
    awsAuth({
      accessKeyId: workspaceSecret("SANDBOX_AWS_ACCESS_KEY_ID"),
      secretAccessKey: workspaceSecret("SANDBOX_AWS_SECRET_ACCESS_KEY"),
    }),
  ],
  mounts: [
    s3Mount({
      id: "customer_data",
      mountPath: "/mnt/mounts/customer-data",
      bucket: "example-bucket",
      prefix: "datasets/customer-data",
      region: "us-east-1",
      pathStyle: false,
      readOnly: true,
    }),
  ],
});

const sandbox = await client.createSandbox({
  name: "s3-mount-sandbox",
  mountConfig: mountCfg,
});

try {
  const result = await sandbox.run("ls /mnt/mounts/customer-data");
  console.log(result.stdout);
} finally {
  await sandbox.delete();
}
```

### Authenticate with an IAM role

IAM role authentication lets the [AWS auth proxy](Sandbox%20auth%20proxy.md#authenticate-with-an-iam-role) assume a role in your AWS account. S3 mounts use the same authentication as other supported AWS requests from the sandbox. LangSmith obtains and renews temporary AWS credentials, so you do not need to store or rotate access keys in workspace secrets.

> [!NOTE]
>
> This option requires your LangSmith deployment to enable AWS proxy role authentication. Enabling IAM roles for ECR registries does not enable them for the auth proxy. If **AWS IAM role** is absent from the AWS authentication options, use static access keys or contact your LangSmith administrator. The role-based SDK examples require a release with `aws_auth(role_arn=...)` and `mount_config(proxy_config=...)` in Python, or `awsAuth({ roleArn })` and `mountConfig({ proxyConfig })` in TypeScript. The mount versions listed at the top of this page do not establish support for these newer options.

You need permission to configure the customer IAM role's trust and access policies. One AWS auth rule applies to the sandbox's AWS requests, including all S3 mounts. Choose either static access keys or an IAM role; do not configure both. Role authentication is configured at creation. Create a new sandbox to add, remove, disable, or change its role.

The LangSmith principal also needs permission to assume the customer role. For self-hosted deployments, your administrator configures that permission and any required role tags. Cross-account S3 buckets may also require a bucket policy that permits the customer role.

To configure the role and create the sandbox:

1. Open **Sandboxes > Create sandbox**, add an **S3 bucket** in the **Mounts** section, and configure its bucket, region, prefix, mount path, and read-only setting.
2. Go to the **Network** section, enable AWS authentication, and select **AWS IAM role**. To use the role without mounts, skip the mount configuration in step 1.
3. Use the two values displayed below **AWS role ARN** in your IAM role's trust policy:
   * **Principal**: The exact AWS role ARN that this LangSmith deployment uses to assume customer roles. Use the displayed principal, not an ARN copied from another environment or from an ECR registry.
   * **External ID**: Your current LangSmith workspace UUID. LangSmith supplies this value when assuming the role; you do not choose a separate external ID.
4. Expand **AWS role setup**, select **Copy trust policy**, and apply that policy to the customer role in AWS IAM. It permits `sts:AssumeRole` only for the displayed principal with the matching `sts:ExternalId`.
5. Attach a least-privilege permissions policy for the AWS services and resources the sandbox needs. For configured S3 mounts, **Copy S3 permissions** supplies a starting policy. Review it before attaching it; LangSmith does not apply it automatically.
6. Enter the customer role's ARN in **AWS role ARN**. This is the role you configured in your account, not the LangSmith principal shown in the setup instructions.
7. Select **Create Sandbox**, then verify that sandbox code can read the mounted path and, for writable mounts, write to it.

The generated trust policy has this structure. Replace the placeholders with the principal and external ID displayed in the form, or copy the completed policy from the form:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "<LANGSMITH_AWS_PROXY_PRINCIPAL_ARN>"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "<LANGSMITH_WORKSPACE_ID>"
        }
      }
    }
  ]
}
```

Do not replace the principal with `*` or remove the external ID condition. Entering the customer role ARN in LangSmith does not create the role or update its AWS policies.

#### Limit S3 access

The optional S3 permissions example grants access based on the mount settings:

* **All S3 mounts**: Bucket-location access, prefix-scoped listing, and object reads.
* **Writable mounts**: Additional object-write, delete, and multipart-upload permissions.
* **Empty prefix**: Object access throughout the bucket. Use a prefix to restrict access to a subtree.

The role's effective AWS permissions control all supported AWS proxy requests. LangSmith does not restrict a general AWS role session to the configured mounts. Limit the role's IAM policy to the required buckets, prefixes, operations, and other AWS resources.

> [!WARNING]
>
> A read-only mount rejects filesystem writes, but does not block direct S3 API writes that the role permits. Use the role's IAM policy to enforce read-only AWS access.

Use a commercial AWS role and supported AWS HTTPS endpoints. The S3 permissions example does not include KMS permissions. For buckets encrypted with a KMS key, see [Encrypt uploads with a KMS key](#encrypt-uploads-with-a-kms-key).

#### Use a shared role in the SDK

A shared AWS proxy role authenticates both S3 mounts and supported application requests, just like the UI setup above. Configure the trust and permissions policies first, then replace the example role ARN and bucket with your own values.

Pass the same proxy configuration to the mount helper and sandbox creation. The mount helper does not copy it into mount-specific authentication:

```python Python
from langsmith.sandbox import (
    SandboxClient,
    aws_auth,
    mount_config,
    proxy_config,
    s3_mount,
)

proxy_cfg = proxy_config(
    rules=[aws_auth(role_arn="arn:aws:iam::123456789012:role/LangSmithSandbox")]
)
mount_cfg = mount_config(
    proxy_config=proxy_cfg,
    mounts=[
        s3_mount(
            id="customer_data",
            mount_path="/mnt/mounts/customer-data",
            bucket="example-bucket",
            prefix="datasets/customer-data",
            region="us-east-1",
            read_only=True,
        )
    ],
)

client = SandboxClient()
sandbox = client.create_sandbox(
    name="shared-role-mount-sandbox",
    mount_config=mount_cfg,
    proxy_config=proxy_cfg,
)
```

```ts TypeScript
import {
  SandboxClient,
  awsAuth,
  mountConfig,
  proxyConfig,
  s3Mount,
} from "langsmith/sandbox";

const proxyCfg = proxyConfig({
  rules: [
    awsAuth({ roleArn: "arn:aws:iam::123456789012:role/LangSmithSandbox" }),
  ],
});
const mountCfg = mountConfig({
  proxyConfig: proxyCfg,
  mounts: [
    s3Mount({
      id: "customer_data",
      mountPath: "/mnt/mounts/customer-data",
      bucket: "example-bucket",
      prefix: "datasets/customer-data",
      region: "us-east-1",
      readOnly: true,
    }),
  ],
});

const client = new SandboxClient();
const sandbox = await client.createSandbox({
  name: "shared-role-mount-sandbox",
  mountConfig: mountCfg,
  proxyConfig: proxyCfg,
});
```

The shared rule retains its effective IAM permissions. The read-only mount in this example does not prevent direct S3 API writes that the role allows. Shared proxy authentication is supported for S3 mounts, not GCS mounts; GCS still requires explicit mount authentication.

#### Restrict a role to S3 mount scopes

Mount-specific role authentication adds a session policy that restricts AWS access to the configured S3 buckets, prefixes, and read-only settings. Use this API alternative when sandbox AWS access must stay within those mount scopes. The customer role still needs the trust and permissions policies described above.

Pass the role in `auth` to serialize it as `mount_config.auth.aws.role_arn`. Do not also pass an AWS proxy rule:

```python Python
from langsmith.sandbox import SandboxClient, aws_auth, mount_config, s3_mount

mount_cfg = mount_config(
    auth=[aws_auth(role_arn="arn:aws:iam::123456789012:role/LangSmithSandbox")],
    mounts=[
        s3_mount(
            id="customer_data",
            mount_path="/mnt/mounts/customer-data",
            bucket="example-bucket",
            prefix="datasets/customer-data",
            region="us-east-1",
            read_only=True,
        )
    ],
)

client = SandboxClient()
sandbox = client.create_sandbox(
    name="mount-scoped-role-sandbox",
    mount_config=mount_cfg,
)
```

```ts TypeScript
import { SandboxClient, awsAuth, mountConfig, s3Mount } from "langsmith/sandbox";

const mountCfg = mountConfig({
  auth: [
    awsAuth({ roleArn: "arn:aws:iam::123456789012:role/LangSmithSandbox" }),
  ],
  mounts: [
    s3Mount({
      id: "customer_data",
      mountPath: "/mnt/mounts/customer-data",
      bucket: "example-bucket",
      prefix: "datasets/customer-data",
      region: "us-east-1",
      readOnly: true,
    }),
  ],
});

const client = new SandboxClient();
const sandbox = await client.createSandbox({
  name: "mount-scoped-role-sandbox",
  mountConfig: mountCfg,
});
```

The mount-specific `mount_config.auth.aws` API accepts either `role_arn` or the static `access_key_id` and `secret_access_key` pair, not both. It cannot be combined with an AWS proxy rule. Static-key examples earlier on this page continue to work unchanged.

#### Renew credentials

LangSmith renews temporary credentials as AWS requests need them, including after a sandbox stops and resumes. You do not supply a saved STS token or renew it manually. Keep the role's trust and access permissions in place for continued access.

If renewal is temporarily unavailable, the mount can use cached credentials only until they expire. An authorization denial or expired credentials causes authenticated S3 requests to fail; the mount does not fall back to static keys.

### Encrypt uploads with a KMS key

Set `encryption` on an S3 mount to encrypt every object the sandbox uploads through the mount with a customer-managed AWS KMS key (SSE-KMS). Use it when a bucket policy requires uploads to name a specific key, or to choose the key instead of relying on the bucket's default encryption.

> [!NOTE]
>
> Mount encryption requires `langsmith>=0.14.8` for Python or `langsmith>=0.10.12` for TypeScript. Self-hosted deployments require LangSmith v0.17.35 or later.

```python Python
s3_mount(
    id="customer_data",
    mount_path="/mnt/mounts/customer-data",
    bucket="example-bucket",
    region="us-east-1",
    encryption={
        "kms_key": "arn:aws:kms:us-east-1:123456789012:key/1234abcd-12ab-34cd-56ef-1234567890ab",
    },
)
```

```ts TypeScript
s3Mount({
  id: "customer_data",
  mountPath: "/mnt/mounts/customer-data",
  bucket: "example-bucket",
  region: "us-east-1",
  encryption: {
    kms_key:
      "arn:aws:kms:us-east-1:123456789012:key/1234abcd-12ab-34cd-56ef-1234567890ab",
  },
});
```

* **Key format**: `kms_key` must be a KMS key ARN in the mount's region and AWS partition. LangSmith rejects key aliases and bare key IDs.
* **Mount types**: Only S3 mounts accept `encryption`. LangSmith rejects it on GCS, Git, and Context Hub mounts.
* **Static keys and shared roles**: Grant the IAM identity `kms:GenerateDataKey` on the key for uploads and `kms:Decrypt` for reads and multipart uploads. The key policy must also allow that identity.
* **Mount-scoped roles**: The session policy lets S3, and only S3, use the configured key: `kms:Decrypt` for every mount, and `kms:GenerateDataKey` only when a writable mount uses the key. All role-backed mounts in a sandbox must name the same key. The customer role and the key policy must still grant both permissions.

A bucket whose default encryption is SSE-KMS works without `encryption` when the mount's AWS identity can use the bucket's default key. Uploads then use that default key. Mount-scoped role authentication denies KMS access for mounts without `encryption`, so those mounts cannot read or write objects encrypted with a KMS key.

## Mount a GCS bucket

GCS mounts require GCP auth. The OAuth scope is supplied by the backend, derived from the mounts themselves: read-only mounts get `devstorage.read_only` and writable mounts get `devstorage.read_write`.

Because a single `mount_config` resolves to one scope, all of its GCS mounts must agree: mixing read-only and writable GCS mounts in one config is rejected. Use writable mounts throughout, or create separate sandboxes.

```python Python
from langsmith.sandbox import (
    SandboxClient,
    gcp_auth,
    gcs_mount,
    mount_config,
    workspace_secret,
)

client = SandboxClient()

mount_cfg = mount_config(
    auth=[
        gcp_auth(
            service_account_json=workspace_secret(
                "SANDBOX_GCP_SERVICE_ACCOUNT_JSON"
            ),
        )
    ],
    mounts=[
        gcs_mount(
            id="eval_datasets",
            mount_path="/mnt/mounts/eval-datasets",
            bucket="example-bucket",
            prefix="datasets/evals",
            read_only=False,
        )
    ],
)

with client.sandbox(name="gcs-mount-sandbox", mount_config=mount_cfg) as sb:
    result = sb.run("ls /mnt/mounts/eval-datasets")
    print(result.stdout)
```

```ts TypeScript
import {
  SandboxClient,
  gcpAuth,
  gcsMount,
  mountConfig,
  workspaceSecret,
} from "langsmith/sandbox";

const client = new SandboxClient();

const mountCfg = mountConfig({
  auth: [
    gcpAuth({
      serviceAccountJson: workspaceSecret("SANDBOX_GCP_SERVICE_ACCOUNT_JSON"),
    }),
  ],
  mounts: [
    gcsMount({
      id: "eval_datasets",
      mountPath: "/mnt/mounts/eval-datasets",
      bucket: "example-bucket",
      prefix: "datasets/evals",
      readOnly: false,
    }),
  ],
});

const sandbox = await client.createSandbox({
  name: "gcs-mount-sandbox",
  mountConfig: mountCfg,
});

try {
  const result = await sandbox.run("ls /mnt/mounts/eval-datasets");
  console.log(result.stdout);
} finally {
  await sandbox.delete();
}
```

## Mount a public Git repository

Public Git mounts do not require AWS or GCP auth. Use an HTTPS remote URL and optionally pin a branch or tag.

```python Python
from langsmith.sandbox import SandboxClient, git_mount, mount_config

client = SandboxClient()

mount_cfg = mount_config(
    mounts=[
        git_mount(
            id="repo",
            mount_path="/mnt/mounts/repo",
            remote_url="https://github.com/langchain-ai/langsmith-sdk.git",
            ref={"type": "branch", "name": "main"},
            refresh_interval_seconds=60,
        )
    ],
)

with client.sandbox(name="git-mount-sandbox", mount_config=mount_cfg) as sb:
    result = sb.run("ls /mnt/mounts/repo")
    print(result.stdout)
```

```ts TypeScript
import { SandboxClient, gitMount, mountConfig } from "langsmith/sandbox";

const client = new SandboxClient();

const mountCfg = mountConfig({
  mounts: [
    gitMount({
      id: "repo",
      mountPath: "/mnt/mounts/repo",
      remoteUrl: "https://github.com/langchain-ai/langsmith-sdk.git",
      ref: { type: "branch", name: "main" },
      refreshIntervalSeconds: 60,
    }),
  ],
});

const sandbox = await client.createSandbox({
  name: "git-mount-sandbox",
  mountConfig: mountCfg,
});

try {
  const result = await sandbox.run("ls /mnt/mounts/repo");
  console.log(result.stdout);
} finally {
  await sandbox.delete();
}
```

Private Git repositories can use low-level `proxy_config` / `proxyConfig` rules when the remote requires proxy-managed auth. There is not yet a high-level private Git auth helper.

## Mount a Context Hub repo

A Context Hub mount mirrors the latest commit of an agent or skill repo into the sandbox filesystem. Use it to give sandbox code the same instructions, skills, and tools your production agents pull, without packaging them into the sandbox image or copying them in at startup.

Identify the repo as `owner/repo`. Use `-` as the owner for a repo in the current workspace, such as `-/my-agent`. The caller's API key must have read access to the repo. LangSmith rejects sandbox creation for a repo private to another workspace, and does not distinguish a missing repo from an inaccessible one. Context Hub mounts do not require AWS or GCP auth.

```python Python
from langsmith.sandbox import SandboxClient, context_hub_mount, mount_config

client = SandboxClient()

mount_cfg = mount_config(
    mounts=[
        context_hub_mount(
            id="memories",
            mount_path="/memories",
            repo="-/my-agent",
        )
    ],
)

with client.sandbox(
    name="context-hub-mount-sandbox", mount_config=mount_cfg
) as sb:
    result = sb.run("ls /memories")
    print(result.stdout)
```

```ts TypeScript
import { SandboxClient, contextHubMount, mountConfig } from "langsmith/sandbox";

const client = new SandboxClient();

const mountCfg = mountConfig({
  mounts: [
    contextHubMount({
      id: "memories",
      mountPath: "/memories",
      repo: "-/my-agent",
    }),
  ],
});

const sandbox = await client.createSandbox({
  name: "context-hub-mount-sandbox",
  mountConfig: mountCfg,
});

try {
  const result = await sandbox.run("ls /memories");
  console.log(result.stdout);
} finally {
  await sandbox.delete();
}
```

The mount contains the flattened file tree of the repo's latest commit. A file linked from another agent or skill repo appears at the path where the parent repo references it, so a mounted agent also carries the skills it composes. For more information on composing repos, see [Manage contexts with the SDK](../Prompt%20%26%20Context%20Hub/Context%20Hub/Manage%20contexts%20with%20the%20SDK.md).

### Read a repo as it changes

Context Hub mounts are read-only, and the sync is one-way. Files written under the mount path inside the sandbox are never pushed back to the repo, and the next refresh overwrites them. Write sandbox output to a path outside the mount, and push it with the Context Hub SDK when it belongs in the repo.

LangSmith keeps the mount in sync for the sandbox's lifetime. New commits reach a running sandbox within roughly 30 seconds. Treat that cadence as best effort rather than a freshness guarantee. A refresh replaces the whole tree at once, so a reader sees either the previous commit or the new one, never a mix.

A mount always tracks the latest commit. To read a fixed version, pull the commit or environment tag you want with the Context Hub SDK instead of mounting the repo.

Pass `initial_pull_only` / `initialPullOnly` to sync once at startup and then stop polling:

```python Python
context_hub_mount(
    id="memories",
    mount_path="/memories",
    repo="-/my-agent",
    initial_pull_only=True,
)
```

```ts TypeScript
contextHubMount({
  id: "memories",
  mountPath: "/memories",
  repo: "-/my-agent",
  initialPullOnly: true,
});
```

Use a single pull for a run that must read one commit from start to finish, such as an evaluation whose results you compare against a specific version of an agent.

### Handle startup and failures

The mount directory exists as soon as the sandbox is ready, but reads under it block until the first commit tree arrives. Code that reads the mount immediately at startup waits for the initial sync rather than seeing an empty directory.

LangSmith retries a failed refresh and keeps serving the last commit it published, so a transient error does not empty a working mount. Two conditions do surface to sandbox code:

* **A rejected request**: Reads fail with `EIO`. Revoking the caller's access to the repo after the sandbox starts rejects later pulls, because LangSmith re-checks access on every pull.
* **A repo that exceeds the sync limits**: The mount serves no tree. A synced commit can hold at most 2,500 files and 25 MiB of file content, counting everything the repo links.

## Combine mounts

A sandbox can mount multiple sources, including a Context Hub repo alongside bucket and Git mounts. Build one `mount_config` / `mountConfig` with all mount specs, and include provider auth for every bucket provider used by those specs.

```python Python
from langsmith.sandbox import (
    aws_auth,
    git_mount,
    gcp_auth,
    gcs_mount,
    mount_config,
    s3_mount,
    workspace_secret,
)

mount_cfg = mount_config(
    auth=[
        aws_auth(
            access_key_id=workspace_secret("SANDBOX_AWS_ACCESS_KEY_ID"),
            secret_access_key=workspace_secret("SANDBOX_AWS_SECRET_ACCESS_KEY"),
        ),
        gcp_auth(
            service_account_json=workspace_secret(
                "SANDBOX_GCP_SERVICE_ACCOUNT_JSON"
            ),
        ),
    ],
    mounts=[
        s3_mount(
            id="s3_data",
            mount_path="/mnt/mounts/s3-data",
            bucket="example-s3-bucket",
        ),
        gcs_mount(
            id="gcs_data",
            mount_path="/mnt/mounts/gcs-data",
            bucket="example-gcs-bucket",
        ),
        git_mount(
            id="repo",
            mount_path="/mnt/mounts/repo",
            remote_url="https://github.com/langchain-ai/langsmith-sdk.git",
        ),
    ],
)
```

```ts TypeScript
import {
  awsAuth,
  gitMount,
  gcpAuth,
  gcsMount,
  mountConfig,
  s3Mount,
  workspaceSecret,
} from "langsmith/sandbox";

const mountCfg = mountConfig({
  auth: [
    awsAuth({
      accessKeyId: workspaceSecret("SANDBOX_AWS_ACCESS_KEY_ID"),
      secretAccessKey: workspaceSecret("SANDBOX_AWS_SECRET_ACCESS_KEY"),
    }),
    gcpAuth({
      serviceAccountJson: workspaceSecret("SANDBOX_GCP_SERVICE_ACCOUNT_JSON"),
    }),
  ],
  mounts: [
    s3Mount({
      id: "s3_data",
      mountPath: "/mnt/mounts/s3-data",
      bucket: "example-s3-bucket",
    }),
    gcsMount({
      id: "gcs_data",
      mountPath: "/mnt/mounts/gcs-data",
      bucket: "example-gcs-bucket",
    }),
    gitMount({
      id: "repo",
      mountPath: "/mnt/mounts/repo",
      remoteUrl: "https://github.com/langchain-ai/langsmith-sdk.git",
    }),
  ],
});
```

## Cache bucket mounts

S3 and GCS mounts support optional cache settings. Cache settings tune the local
VFS cache used by the bucket mount; the bucket remains the source of truth. Use
cache settings to control local disk usage and writeback timing, not as a
separate persistence layer. Cache settings do not apply to Git mounts.

| Field | Description |
| - | - |
| `max_size_bytes` | Optional maximum size, in bytes, for the local mount cache. Set a positive value to add an explicit cap; omit it to leave the runtime default. |
| `writeback_seconds` | Optional delay, in seconds, before cached writes are written back to the bucket. The default is `0`. Lower values make writes visible to the bucket sooner; higher values can reduce write traffic for workloads that rewrite the same files. |

For read-only dataset mounts, configure `max_size_bytes` only when you need a
specific local cache cap. For writable mounts, keep `writeback_seconds` low when
another process needs to read the objects from S3 or GCS soon after the sandbox
writes them.

```python Python
s3_mount(
    id="customer_data",
    mount_path="/mnt/mounts/customer-data",
    bucket="example-bucket",
    cache={
        "max_size_bytes": 2 * 1024**3,
        "writeback_seconds": 5,
    },
)
```

```ts TypeScript
s3Mount({
  id: "customer_data",
  mountPath: "/mnt/mounts/customer-data",
  bucket: "example-bucket",
  cache: {
    max_size_bytes: 2 * 1024 ** 3,
    writeback_seconds: 5,
  },
});
```

The same cache settings can be used on GCS mounts:

```python Python
gcs_mount(
    id="eval_datasets",
    mount_path="/mnt/mounts/eval-datasets",
    bucket="example-bucket",
    cache={
        "max_size_bytes": 2 * 1024**3,
        "writeback_seconds": 5,
    },
)
```

```ts TypeScript
gcsMount({
  id: "eval_datasets",
  mountPath: "/mnt/mounts/eval-datasets",
  bucket: "example-bucket",
  cache: {
    max_size_bytes: 2 * 1024 ** 3,
    writeback_seconds: 5,
  },
});
```

## Limits

* Mounts are attached when the sandbox is created. Create a new sandbox to change mounts.
* S3 mounts in China (`cn-*`) and AWS GovCloud (`us-gov-*`) regions must set `endpoint_url` / `endpointUrl` to the region's S3 endpoint. The default endpoint, `https://s3.amazonaws.com`, serves only commercial regions.
* Mount-scoped role authentication must fit AWS's 2,048-character session policy limit. Many mounts, long bucket names or prefixes, or a KMS key can exceed it, and LangSmith then rejects the sandbox.
* Configure each cloud provider's credentials in one auth surface per sandbox. If mount auth supplies AWS or GCP credentials, do not also add an auth proxy rule for the same provider.
* Git refs can be omitted or set to a branch or tag. Commit refs are not supported.
* Git mounts do not support `read_only` / `readOnly` or cache settings.
* Context Hub mounts are always read-only and do not support cache settings.
* Context Hub mounts accept agent and skill repos. LangSmith rejects other repo types and repos with no commits.
* A Context Hub mount path cannot be the filesystem root or sit at or under a system directory such as `/etc`, `/usr`, or `/var`.
* Restoring a sandbox reconnects each Context Hub mount at its configured path. A restored process that holds an open file or working directory inside the mount must reopen it.
