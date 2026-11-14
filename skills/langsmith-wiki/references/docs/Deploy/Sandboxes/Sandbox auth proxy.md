# Sandbox auth proxy

> Inject credentials into outbound requests and control which destinations a sandbox can reach.

The auth proxy lets sandbox code call external APIs (OpenAI, Anthropic, GitHub, etc.) without hardcoding credentials. When configured on a sandbox, an egress proxy running outside the sandbox automatically injects authentication headers into matching outbound requests using your workspace secrets or write-only credentials you provide in the proxy config.

> [!WARNING]
>
> You must configure your secrets (e.g., `OPENAI_API_KEY`) in your LangSmith [workspace](../../LangSmith%20setup/Govern/Organization/Overview.md#workspaces) settings before creating a sandbox that references them.

## Delegate LangSmith access

Access delegation lets sandbox code call the LangSmith API without an API key inside the sandbox. The auth proxy injects credentials for requests to your LangSmith API host.

Set `access_delegation` in the top-level request body when creating a sandbox with `POST /v2/sandboxes/boxes`:

* **`INHERIT`**: Set `{"mode": "INHERIT"}` to inherit the caller's current delegatable permissions. Do not include `permissions`.
* **`EXPLICIT`**: Set `{"mode": "EXPLICIT", "permissions": ["sandboxes:read"]}` to restrict access to specific permissions you hold. The list must be nonempty.

Both modes remain capped by the caller's current permissions on every request. Workspace and organization administration permissions cannot be delegated. A workspace service key can also delegate access; narrowing its role narrows the sandbox's access, and deleting the key revokes it.

Inside the sandbox, call the HTTPS LangSmith API endpoint without supplying your own credentials. A sandbox acting under a delegation grant cannot grant access to another sandbox.

## Egress and network access control

The same `proxy_config` that injects credentials also controls which destinations a sandbox can reach. Access control is enforced per connection on the sandbox host, so changes to `access_control` take effect immediately.

### How egress works

* **Access control applies to every outbound TCP connection**, HTTP or not.
* **HTTPS to a host matched by a rule or callback is decrypted by the proxy** so it can inject headers; sandboxes trust the proxy's CA. HTTPS to unmatched hosts and every non-HTTP connection, including PostgreSQL, SSH, and Redis, passes through unchanged. Ports 80 and 443 are reserved for HTTP and TLS; a non-HTTP protocol on either port does not work.
* **Use hostnames for direct connections by default.** Raw TCP to a public literal IP requires an explicitly matching IP or CIDR entry in `allow_list` and is unavailable in deny-list mode. HTTPS to a literal IP is dropped because the proxy needs a hostname in the TLS handshake. Cleartext HTTP on port 80 can use a literal IP.
* **Only TCP leaves the sandbox.** UDP (including QUIC) and ICMP are dropped.

### Default egress posture

With no `access_control`, **every hostname is reachable on every TCP port**, unless your organization is on [restricted egress](#organization-level-restricted-egress). The only exception is hosts that resolve to private, loopback, or cloud-metadata addresses, which the proxy refuses to dial. For a sandbox created with `access_delegation`, your LangSmith API host is exempt from the private-address check, so a self-hosted install whose hostname resolves to a private address, such as an internal load balancer, can still serve delegated requests. No other private destination is opened, and loopback and cloud-metadata addresses stay blocked. On a self-hosted installation, an `allow_list` entry that matches a private destination also opens it; see [Reach private services directly](../../LangSmith%20setup/Self-hosted/Install%20an%20instance/Additional%20features/Enable%20Sandboxes/Route%20self-hosted%20Sandbox%20egress%20through%20a%20forward%20proxy.md#reach-private-services-directly). Add an `access_control` to restrict this.

* **HTTP and HTTPS (ports 80 and 443) to any hostname are allowed.** Outbound HTTP(S) is transparently routed through the proxy, where your `rules` and `callbacks` inject credentials.
* **Raw TCP to hostnames is allowed.** Connections to non-HTTP ports, such as databases (`psql` or `dbt` on 5432), SSH (22), and Redis (6379), pass through without protocol interception.
* **Raw TCP to a literal public IP address requires an explicit IP or CIDR entry in an `allow_list`.** Private, reserved, loopback, link-local, and cloud-metadata destinations remain subject to SSRF protections; see the self-hosted and delegation exceptions above.

To allow HTTP and HTTPS to any host while blocking every other port, use a port-qualified allow list. `*` matches every hostname:

```json
{
  "access_control": {
    "allow_list": ["*:80", "*:443"]
  }
}
```

Add `host:PORT` entries to open specific raw TCP destinations on top of that, such as `db.example.com:5432`.

On a self-hosted installation, this list also lets the Sandbox reach private destinations on ports 80 and 443. List specific public hosts instead when Sandboxes must not reach your internal network.

### Allow and deny lists

Add an `access_control` object to `proxy_config` with **either** an `allow_list` **or** a `deny_list` (not both—the request is rejected if both are set):

| Mode | Behavior |
| - | - |
| `allow_list` | **Default-deny.** Only listed destinations are reachable, on any protocol. List every host the sandbox needs, including the HTTP(S) hosts your `rules` and `callbacks` target. |
| `deny_list` | **Default-allow for hostnames.** Hostname-based HTTP, HTTPS, and raw TCP remain reachable except where a matching entry blocks them. You cannot use direct IP connections in deny-list mode, even when the destination IP does not match a deny-list entry. |

> [!NOTE]
>
> To enable raw TCP to a literal public IP address, use allow-list mode and allow the IP on every port or on a specific port, such as `8.8.8.8` or `8.8.8.8:53`. A containing CIDR also allows every port in that range. Hostname, glob, and regex entries do not authorize applications that connect to a literal IP address.

Access-control entries are evaluated for HTTP, HTTPS, and raw TCP connections to hostnames alike. Use a port suffix to restrict an entry to one port. Direct IP connections require allow-list mode and an explicit IP or CIDR entry.

> [!WARNING]
>
> A `deny_list` only blocks the hostnames you list. `{"deny_list": ["example.com"]}` blocks `example.com` on every port and leaves every other hostname reachable on every port, including DNS, SSH, and database ports. To turn off raw TCP everywhere, use an `allow_list` such as `["*:80", "*:443"]`.

### Pattern syntax

Each `allow_list`/`deny_list` entry uses the following forms:

| Pattern | Meaning |
| - | - |
| `host` | Bare host on every port. |
| `host:PORT` | Host on exactly `PORT`. `:22` grants only 22, not 80 or 443. List the host separately if you need other ports. |
| `*.example.com` | Glob (RFC 1034-style). The apex (`example.com`) is **not** included. May carry a port. |
| `~regex` | Regex matched against the hostname, every port. No port suffix is parsed. |
| `1.2.3.4` / `1.2.3.4:443` / `[::1]` / `[::1]:22` | Literal IP, optionally qualified by a port. |
| `10.0.0.0/8` | CIDR. Cannot carry a port. Private and reserved destinations remain blocked by SSRF protections. |

Matching is on the destination exactly as the sandbox addressed it. A hostname entry matches requests made to that hostname; an IP or CIDR entry matches requests made to a literal IP address. Neither is resolved: `deny_list: ["203.0.113.0/24"]` does not block `foo.example.com` even when it resolves into that range, and `allow_list: ["203.0.113.7"]` does not allow it either. In allow-list mode, an IP or CIDR entry also permits raw TCP to a matching public literal IP. Direct IP connections are unavailable in deny-list mode, and HTTPS to a literal IP is dropped because the proxy needs a hostname in the TLS handshake. Cleartext HTTP on port 80 can use a literal IP when allowed by the active access control.

Entries that do not parse—`example.com:abc`, `example.com:99999`, or a CIDR with a port—are rejected when the sandbox is created or updated.

### Organization-level restricted egress

Restricted egress limits sandbox connections to a LangSmith-managed allowlist of hosts and ports. It applies to non-Enterprise organizations by default and to organizations that request it. Organizations with an approved exemption can use unrestricted egress.

The allowlist supports common development tasks, including installing packages, accessing source repositories, and calling model APIs. It includes PyPI, npm, GitHub, OpenAI, Anthropic, and LangSmith, primarily over HTTPS on port 443. Selected package repositories also allow HTTP on port 80.

When restricted egress is enabled for your organization, LangSmith blocks destinations outside this allowlist. The organization policy replaces caller-supplied `access_control` settings and disables `no_proxy` bypasses. Adding a destination to your sandbox's `allow_list` or configuring credentials for it does not grant access beyond the organization policy.

An organization policy change does not automatically update existing sandboxes. Starting or waking an existing sandbox reuses its stored network configuration.

### Request unrestricted access

If your sandbox needs destinations outside the managed allowlist, [file a support ticket](https://support.langchain.com) to request unrestricted egress for your organization. Include the following details:

* **Organization**: Your organization or workspace ID and deployment region.
* **Network requirements**: The destination hostnames, ports, and a description of your use case.
* **Affected sandbox**: For an existing sandbox, its ID and the connection error.

An approved exemption removes the organization-managed allowlist requirement. Your sandbox's own access controls and platform protections against access to private or reserved IP addresses still apply. Existing sandbox configurations are not automatically changed by an exemption.

### Connecting to a database (raw TCP)

If your organization has restricted egress, [request unrestricted access](#request-unrestricted-access) before connecting to a database outside the managed allowlist.

To let sandbox code reach an external PostgreSQL database with `psql`, `dbt`, or any driver, allow-list the host on its port. Because `allow_list` is default-deny, also list any HTTP(S) hosts the sandbox needs. Pin them to `:443` unless you need other ports too:

```bash
curl -X POST "$LANGSMITH_ENDPOINT/v2/sandboxes/boxes" \
  -H "x-api-key: $LANGSMITH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "db-sandbox",
    "proxy_config": {
      "access_control": {
        "allow_list": [
          "db.example.com:5432",
          "api.openai.com:443"
        ]
      }
    }
  }'
```

The connection to `db.example.com:5432` is passed through at the TCP layer with no interception, so the PostgreSQL wire protocol—and TLS, host-key checking, and any other end-to-end protocol on top of it—works unchanged.

> [!NOTE]
>
> Creating a sandbox boots it and returns once it reports `ready`, so there is no wait step to add. `GET /api/v2/sandboxes/boxes/{name}/status` reports the current state if you need to re-check it later.

### Configure via SDK

```python Python
from langsmith.sandbox import SandboxClient

client = SandboxClient()

client.create_sandbox(
    name="db-sandbox",
    proxy_config={
        "access_control": {
            "allow_list": ["db.example.com:5432", "api.openai.com:443"]
        }
    },
)
```

```ts TypeScript
import { SandboxClient } from "langsmith/sandbox";

const client = new SandboxClient();

await client.createSandbox({
  name: "db-sandbox",
  proxyConfig: {
    access_control: {
      allow_list: ["db.example.com:5432", "api.openai.com:443"],
    },
  },
});
```

## Configure auth proxy rules

Add a `proxy_config` when creating a sandbox, or update an existing sandbox by patching its `proxy_config`. A `proxy_config` has:

| Field | Description |
| - | - |
| `rules` | Header-injection and provider-auth rules. Enabled header rules are matched first-match-wins in list order; `aws` and `gcp` rules match their providers' hosts regardless of position |
| `callbacks` | Dynamic credential lookups; see [Callback credential example](#callback-credential-example) |
| `access_control` | `allow_list` or `deny_list`; see [Allow and deny lists](#allow-and-deny-lists) |
| `description` | Optional, up to 1024 characters. What this configuration lets the sandbox reach, for handing to an agent |

Each rule specifies:

| Field | Description |
| - | - |
| `name` | Required. Identifier for the rule |
| `type` | Omit for header injection; `aws` or `gcp` for provider auth; `relay` to send matching connections through a [relay](../../LangSmith%20setup/Govern/Organization/Relays.md) |
| `match_hosts` | Required for header rules; rejected on `aws` and `gcp` rules. Bare hostnames, or a leading `*.` wildcard in front of a registrable domain (`*.github.com`, not `*.com` or `*`). No scheme, path, or port. The wildcard does not match the apex domain |
| `match_paths` | Paths to match (empty = all paths). Header rules only. Patterns are matched against the request path without the query string; see [Match rules by path or header](#match-rules-by-path-or-header) |
| `match_headers` | Request headers that must all be present, each written `"name: value"` with a lowercase name and an exact value. Header rules only; see [Match rules by path or header](#match-rules-by-path-or-header) |
| `headers` | Headers to inject, each with a `name`, `type`, and `value`. Header rules only |
| `aws` / `gcp` | Provider credentials; see [Authenticate AWS requests](#authenticate-aws-requests) and [Authenticate GCP requests](#authenticate-gcp-requests) |
| `env_vars` | Environment variables to set in the sandbox while the rule is enabled |
| `enabled` | Defaults to `true` |
| `description` | Optional, up to 1024 characters. What this rule lets the sandbox reach |

### Header types

Each header has a required `type` that controls how its value is stored and displayed:

| Type | Description |
| - | - |
| `workspace_secret` | References a workspace secret using `{KEY}` syntax. Resolved when the proxy configuration is applied. |
| `plaintext` | Value is stored and returned as-is. Use for non-sensitive headers. |
| `opaque` | Write-only. Value is encrypted at rest and never returned via the API. |

### Match rules by path or header

`match_hosts` alone sends every request to a host through one rule. Add `match_paths` or `match_headers` to give different requests to the same host different credentials. The proxy checks enabled header rules in list order and applies the first rule whose host, path, and headers all match, so put the more specific rule first.

`match_paths` patterns are compared with the request path, not the query string:

| Pattern | Matches |
| - | - |
| `/v1/runs` | Exactly `/v1/runs` |
| `/v1/*` or `/v1/**` | Any path that starts with `/v1`. The match is on the text before `/*`, so `/v1/*` also matches `/v10` |
| `*/runs` | Any path that ends with the text after the slash, `runs`. It also matches `/v1/xruns` |
| `*` or `**` | Every path |

A pattern cannot put a wildcard in the middle of a path, such as `/v1/*/runs`.

The same host can use a different credential per route. This example sends one secret for requests under `/ingest` and another for requests under `/query`:

```json
{
  "rules": [
    {
      "name": "ingest",
      "match_hosts": ["api.example.com"],
      "match_paths": ["/ingest/*"],
      "headers": [
        {"name": "x-api-key", "type": "workspace_secret", "value": "{INGEST_API_KEY}"}
      ]
    },
    {
      "name": "query",
      "match_hosts": ["api.example.com"],
      "match_paths": ["/query/*"],
      "headers": [
        {"name": "x-api-key", "type": "workspace_secret", "value": "{QUERY_API_KEY}"}
      ]
    }
  ]
}
```

When routes share a path, or the credential depends on which account the code is acting for, switch on a request header instead. Each `match_headers` entry is `"name: value"` with a lowercase name and an exact value, and the rule matches only when the request carries every listed header. Have the sandbox send a placeholder, and the rule replaces it with the real credential:

```json
{
  "rules": [
    {
      "name": "account-a",
      "match_hosts": ["api.example.com"],
      "match_headers": ["authorization: Bearer account-a"],
      "headers": [
        {"name": "Authorization", "type": "workspace_secret", "value": "Bearer {ACCOUNT_A_TOKEN}"}
      ]
    },
    {
      "name": "account-b",
      "match_hosts": ["api.example.com"],
      "match_headers": ["authorization: Bearer account-b"],
      "headers": [
        {"name": "Authorization", "type": "workspace_secret", "value": "Bearer {ACCOUNT_B_TOKEN}"}
      ]
    }
  ]
}
```

`match_paths` and `match_headers` are accepted on header rules only. `aws`, `gcp`, and `relay` rules reject both.

### Set environment variables from a rule

A rule's `env_vars` are plaintext environment variables set for every command in the sandbox while that rule is enabled. Use them for tools that refuse to run unless a credential variable is present, even though the proxy injects the real credential on the wire: give the variable a placeholder value so the command starts, and the proxy supplies the real credential.

Values are plaintext and are returned by the API, so never put a secret in `env_vars`. Use a header with the `workspace_secret` or `opaque` type instead.

Environment variables resolve in this order, from lowest precedence to highest:

1. **The snapshot image's `ENV`**, when the sandbox opted into `apply_image_config`.
2. **Enabled proxy rules**: When two enabled rules declare the same name, the later rule in `rules` wins.
3. **The sandbox's own `env_vars`**: Explicit per-sandbox values override values from rules.

Variables managed by an enabled AWS or GCP auth rule (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_EC2_METADATA_DISABLED`, `AWS_CA_BUNDLE`; `CLOUDSDK_AUTH_ACCESS_TOKEN`, `CLOUDSDK_CORE_CUSTOM_CA_CERTS_FILE`) sit outside this order: a rule or a sandbox `env_vars` entry that declares one of them is rejected while the matching auth rule is enabled.

Every sandbox also has the common CA-bundle environment variables pointed at the system trust store, which includes the proxy's CA, so tools that pin their own bundle still verify proxy-injected hosts. Set any of them yourself to override.

```json
{
  "name": "github-api",
  "match_hosts": ["api.github.com"],
  "headers": [
    {"name": "Authorization", "type": "opaque", "value": "Bearer <github-token>"}
  ],
  "env_vars": {"GH_TOKEN": "proxy-injected"}
}
```

## Authenticate AWS requests

Use an AWS auth rule when sandbox code needs to call AWS services with an AWS SDK or CLI. The proxy keeps the real AWS credentials outside the sandbox, then signs outbound HTTPS requests to `*.amazonaws.com` endpoints with AWS SigV4.

This is useful when agent code needs to inspect S3 objects, call Bedrock, or use another AWS endpoint without exposing long-lived AWS access keys in sandbox files, environment variables, shell history, or logs. The sandbox receives placeholder `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` values (plus `AWS_EC2_METADATA_DISABLED=true` and `AWS_CA_BUNDLE`) so SDK credential detection works, while the proxy replaces whatever the request carries with a real SigV4 signature. Only `service.region.amazonaws.com` hosts, S3 virtual-hosted and path-style hosts, and a few global endpoints such as `iam`, `sts`, and `s3` are signed; plaintext HTTP to a matched AWS host is rejected with `403`.

> [!WARNING]
>
> Do not set real AWS access keys as sandbox environment variables. Configure them as `workspace_secret` or `opaque` proxy values. Plaintext AWS credential values are rejected.

AWS auth rules are different from header injection rules:

* Set `type` to `aws`.
* Put credentials under the `aws` object.
* Do not set `match_hosts`, `match_paths`, or `headers`; AWS host matching is built into the proxy.
* Configure at most one AWS auth rule per sandbox. The limit counts every AWS rule, including disabled ones.

```bash
curl -X POST "$LANGSMITH_ENDPOINT/v2/sandboxes/boxes" \
  -H "x-api-key: $LANGSMITH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "aws-sandbox",
    "proxy_config": {
      "rules": [
        {
          "name": "aws",
          "type": "aws",
          "enabled": true,
          "aws": {
            "access_key_id": {
              "type": "workspace_secret",
              "value": "{AWS_ACCESS_KEY_ID}"
            },
            "secret_access_key": {
              "type": "workspace_secret",
              "value": "{AWS_SECRET_ACCESS_KEY}"
            }
          }
        }
      ]
    }
  }'
```

### Configure AWS auth via SDK

```python Python
from langsmith.sandbox import (
    SandboxClient,
    aws_auth,
    proxy_config,
    workspace_secret,
)

client = SandboxClient()

client.create_sandbox(
    name="aws-sandbox",
    proxy_config=proxy_config(
        rules=[
            aws_auth(
                access_key_id=workspace_secret("AWS_ACCESS_KEY_ID"),
                secret_access_key=workspace_secret("AWS_SECRET_ACCESS_KEY"),
            )
        ]
    ),
)
```

```ts TypeScript
import {
  SandboxClient,
  awsAuth,
  proxyConfig,
  workspaceSecret,
} from "langsmith/sandbox";

const client = new SandboxClient();

await client.createSandbox({
  name: "aws-sandbox",
  proxyConfig: proxyConfig({
    rules: [
      awsAuth({
        accessKeyId: workspaceSecret("AWS_ACCESS_KEY_ID"),
        secretAccessKey: workspaceSecret("AWS_SECRET_ACCESS_KEY"),
      }),
    ],
  }),
});
```

After the sandbox is ready, use AWS SDKs or CLIs normally inside the sandbox. The SDK or CLI discovers the placeholder AWS environment variables, and the proxy applies the real SigV4 signature to outbound AWS requests. The proxy does not set a region: set `AWS_REGION` through the sandbox's `env_vars` or the rule's `env_vars`, or most SDK and CLI calls fail before they reach the proxy.

> [!NOTE]
>
> Static AWS auth accepts an access key ID and secret access key, but not a caller-supplied session token. Deployments with AWS proxy role authentication enabled also support an IAM role as described below.

### Authenticate with an IAM role

An AWS proxy role lets LangSmith assume a customer IAM role and sign supported AWS HTTPS requests with renewable temporary credentials. It works with or without [S3 mounts](Sandbox%20mounts.md#authenticate-with-an-iam-role), without exposing real credentials to sandbox code.

This option requires deployment support for AWS proxy role authentication. ECR registry role authentication is a separate feature. In **Create sandbox > Network**, enable AWS authentication and select **AWS IAM role**. The form shows the exact LangSmith principal and workspace External ID that the customer role must trust. Follow the linked setup instructions to configure the trust and permissions policies, then enter the customer role in **AWS role ARN**.

> [!NOTE]
>
> The SDK examples below require a release that supports `aws_auth(role_arn=...)` in Python or `awsAuth({ roleArn })` in TypeScript. Backend support alone does not add these helpers to an older SDK release.

To configure a role without mounts, pass it in the proxy configuration:

```python Python
from langsmith.sandbox import SandboxClient, aws_auth, proxy_config

client = SandboxClient()

sandbox = client.create_sandbox(
    name="aws-role-sandbox",
    proxy_config=proxy_config(
        rules=[
            aws_auth(role_arn="arn:aws:iam::123456789012:role/LangSmithSandbox")
        ]
    ),
)
```

```ts TypeScript
import { SandboxClient, awsAuth, proxyConfig } from "langsmith/sandbox";

const client = new SandboxClient();

const sandbox = await client.createSandbox({
  name: "aws-role-sandbox",
  proxyConfig: proxyConfig({
    rules: [
      awsAuth({ roleArn: "arn:aws:iam::123456789012:role/LangSmithSandbox" }),
    ],
  }),
});
```

For the HTTP API, supply `aws.role_arn` instead of static credential fields:

```bash
curl -X POST "$LANGSMITH_ENDPOINT/v2/sandboxes/boxes" \
  -H "x-api-key: $LANGSMITH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "aws-role-sandbox",
    "proxy_config": {
      "rules": [
        {
          "name": "aws",
          "type": "aws",
          "enabled": true,
          "aws": {
            "role_arn": "arn:aws:iam::123456789012:role/LangSmithSandbox"
          }
        }
      ]
    }
  }'
```

Replace the example ARN with your configured customer role. The single-rule limit still applies. Role authentication is configured at creation: an update can preserve the existing role, but cannot add, remove, change, or disable it. Create a new sandbox to change role authentication.

The role's effective AWS permissions apply to all supported requests. LangSmith does not add a mount-derived session policy to this rule. A read-only S3 mount blocks filesystem writes, not direct S3 API writes that IAM allows. Restrict the customer role to the services, resources, and actions the sandbox needs.

LangSmith renews temporary credentials on demand and reacquires them after stop/start. If renewal is temporarily unavailable, cached credentials remain usable only until expiration. Authorization denial or expiration fails closed, without falling back to static keys.

## Authenticate GCP requests

Use a GCP auth rule when sandbox code needs to call Google APIs with Google SDKs or CLIs. The proxy keeps the service account JSON outside the sandbox, then authenticates outbound HTTPS requests to `googleapis.com` and its subdomains.

This is useful when agent code needs to inspect GCS objects or call another Google API without exposing service account JSON in sandbox files, environment variables, shell history, or logs. The sandbox receives a placeholder `CLOUDSDK_AUTH_ACCESS_TOKEN` (plus `CLOUDSDK_CORE_CUSTOM_CA_CERTS_FILE`) so `gcloud` runs, while the proxy replaces whatever authorization the request carries with a token minted from the configured service account. Google client libraries that discover credentials through Application Default Credentials do not read these variables and fail to find credentials; only `gcloud` and direct HTTPS calls are supported.

> [!WARNING]
>
> Do not set real service account JSON as a sandbox environment variable. Configure it as a `workspace_secret` or `opaque` proxy value. Plaintext GCP credential values are rejected.

GCP auth rules are different from header injection rules:

* Set `type` to `gcp`.
* Put credentials under `gcp.service_account_json`.
* Set `gcp.scopes` to a non-empty list of OAuth scopes.
* The proxy matches `googleapis.com` and its subdomains automatically and authenticates those requests with the configured service account. Hosts under `google.com` are not matched. Plaintext HTTP to a matched host is rejected with `403`.
* Configure at most one GCP auth rule per sandbox. The limit counts every GCP rule, including disabled ones.

The SDK `gcp_auth` and `gcpAuth` helpers build this same rule shape.

```bash
curl -X POST "$LANGSMITH_ENDPOINT/v2/sandboxes/boxes" \
  -H "x-api-key: $LANGSMITH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "gcp-sandbox",
    "proxy_config": {
      "rules": [
        {
          "name": "gcp",
          "type": "gcp",
          "enabled": true,
          "gcp": {
            "service_account_json": {
              "type": "workspace_secret",
              "value": "{GCP_SERVICE_ACCOUNT_JSON}"
            },
            "scopes": [
              "https://www.googleapis.com/auth/devstorage.read_only"
            ]
          }
        }
      ]
    }
  }'
```

### Configure GCP auth via SDK

```python Python
from langsmith.sandbox import (
    SandboxClient,
    gcp_auth,
    proxy_config,
    workspace_secret,
)

client = SandboxClient()

client.create_sandbox(
    name="gcp-sandbox",
    proxy_config=proxy_config(
        rules=[
            gcp_auth(
                service_account_json=workspace_secret("GCP_SERVICE_ACCOUNT_JSON"),
                scopes=["https://www.googleapis.com/auth/devstorage.read_only"],
            )
        ]
    ),
)
```

```ts TypeScript
import {
  SandboxClient,
  gcpAuth,
  proxyConfig,
  workspaceSecret,
} from "langsmith/sandbox";

const client = new SandboxClient();

await client.createSandbox({
  name: "gcp-sandbox",
  proxyConfig: proxyConfig({
    rules: [
      gcpAuth({
        serviceAccountJson: workspaceSecret("GCP_SERVICE_ACCOUNT_JSON"),
        scopes: ["https://www.googleapis.com/auth/devstorage.read_only"],
      }),
    ],
  }),
});
```

After the sandbox is ready, use `gcloud` or direct HTTPS calls to `googleapis.com` hosts normally inside the sandbox. The proxy applies the real GCP authentication without exposing service account JSON inside the sandbox.

## Single API example

Create a sandbox that automatically injects an OpenAI API key into outbound requests:

```bash
curl -X POST "$LANGSMITH_ENDPOINT/v2/sandboxes/boxes" \
  -H "x-api-key: $LANGSMITH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "openai-sandbox",
    "proxy_config": {
      "rules": [
        {
          "name": "openai-api",
          "match_hosts": ["api.openai.com"],
          "headers": [
            {
              "name": "Authorization",
              "type": "workspace_secret",
              "value": "Bearer {OPENAI_API_KEY}"
            }
          ]
        }
      ]
    }
  }'
```

Requests to `api.openai.com` are now authenticated by the proxy; no real key is stored in the sandbox. SDKs that refuse to start without an API key still need a placeholder—set one with the rule's `env_vars`, as in the [GitHub example](#github-example).

## Multiple API example

Add multiple rules to authenticate with several services at once:

```bash
curl -X POST "$LANGSMITH_ENDPOINT/v2/sandboxes/boxes" \
  -H "x-api-key: $LANGSMITH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "multi-api-sandbox",
    "proxy_config": {
      "rules": [
        {
          "name": "openai-api",
          "match_hosts": ["api.openai.com"],
          "headers": [
            {
              "name": "Authorization",
              "type": "workspace_secret",
              "value": "Bearer {OPENAI_API_KEY}"
            }
          ]
        },
        {
          "name": "anthropic-api",
          "match_hosts": ["api.anthropic.com"],
          "headers": [
            {
              "name": "x-api-key",
              "type": "workspace_secret",
              "value": "{ANTHROPIC_API_KEY}"
            },
            {
              "name": "anthropic-version",
              "type": "plaintext",
              "value": "2023-06-01"
            }
          ]
        },
        {
          "name": "github-api",
          "match_hosts": ["api.github.com"],
          "match_paths": ["/repos/*", "/user"],
          "headers": [
            {
              "name": "Authorization",
              "type": "workspace_secret",
              "value": "Bearer {GITHUB_TOKEN}"
            }
          ]
        }
      ]
    }
  }'
```

## GitHub example

[Open SWE](https://github.com/langchain-ai/open-swe/blob/main/openswe/sandboxes/providers/langsmith.py) authenticates GitHub access by minting a short-lived GitHub App installation token outside the sandbox, then patching the sandbox with write-only `opaque` proxy rules. This keeps the short-lived GitHub access token out of the sandbox filesystem and out of deployment environment variables.

Configure two rules:

| Host | Header |
| - | - |
| `api.github.com` | `Authorization: Bearer <github-token>` for `gh` and REST API calls |
| `github.com`, `*.github.com` | `Authorization: Basic <base64("x-access-token:<github-token>")>` for Git over HTTPS operations like clone, fetch, and push |

```python Python
import base64
import os
from typing import Any

import httpx


def github_proxy_rules(github_token: str) -> list[dict[str, Any]]:
    basic_auth = base64.b64encode(
        f"x-access-token:{github_token}".encode()
    ).decode()

    return [
        {
            "name": "github-api",
            "match_hosts": ["api.github.com"],
            "headers": [
                {
                    "name": "Authorization",
                    "type": "opaque",
                    "value": f"Bearer {github_token}",
                }
            ],
            "env_vars": {"GH_TOKEN": "proxy-injected"},
        },
        {
            "name": "github",
            "match_hosts": ["github.com", "*.github.com"],
            "headers": [
                {
                    "name": "Authorization",
                    "type": "opaque",
                    "value": f"Basic {basic_auth}",
                }
            ],
        },
    ]


def configure_github_proxy(sandbox_name: str, github_token: str) -> None:
    endpoint = os.environ.get(
        "LANGSMITH_ENDPOINT", "https://api.smith.langchain.com"
    )
    response = httpx.patch(
        f"{endpoint}/v2/sandboxes/boxes/{sandbox_name}",
        headers={"x-api-key": os.environ["LANGSMITH_API_KEY"]},
        json={"proxy_config": {"rules": github_proxy_rules(github_token)}},
        timeout=180.0,
    )
    response.raise_for_status()
```

Call `configure_github_proxy` after creating or reattaching to a sandbox. GitHub App installation tokens expire, so refresh the proxy config whenever you reuse a sandbox for a new run.

> [!WARNING]
>
> `PATCH` replaces the stored `proxy_config` wholesale. If the sandbox also uses `access_control` or `callbacks`, include them in every update or they are dropped. Opaque header values you leave empty are carried over from the current config.

The `github-api` rule sets `GH_TOKEN` to a non-secret placeholder, which satisfies the `gh` CLI's local credential check. Commands then run without a per-command prefix:

```bash
gh repo view langchain-ai/langchain
gh pr list --repo langchain-ai/langchain
gh repo clone langchain-ai/langchain
```

The placeholder never leaves the sandbox. The proxy injects the real `Authorization` header into the outbound request.

## Configure via SDK

```python Python
from langsmith.sandbox import SandboxClient

client = SandboxClient()

client.create_sandbox(
    name="openai-sandbox",
    proxy_config={
        "rules": [
            {
                "name": "openai-api",
                "match_hosts": ["api.openai.com"],
                "headers": [
                    {
                        "name": "Authorization",
                        "type": "workspace_secret",
                        "value": "Bearer {OPENAI_API_KEY}",
                    }
                ],
            }
        ]
    },
)
```

```ts TypeScript
import { SandboxClient } from "langsmith/sandbox";

const client = new SandboxClient();

await client.createSandbox({
  name: "openai-sandbox",
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

## Callback credential example

Static `workspace_secret` rules pull credentials from your workspace when the proxy configuration is applied, and `opaque` rules let your application patch in short-lived credentials such as the [GitHub token example](#github-example). For credentials that must be resolved by your own service at proxy time, use a **callback**. The proxy POSTs to a URL you provide, your endpoint returns the headers to inject, and the proxy caches the result.

Callbacks are configured alongside rules under `proxy_config`:

| Field | Description |
| - | - |
| `match_hosts` | Hosts to intercept (same syntax as rules; supports globs like `*.github.com`). |
| `url` | Your callback endpoint. Must be an `http://` or `https://` URL that resolves to a public address; private, loopback, Kubernetes-internal, and cloud-metadata targets are rejected. |
| `request_headers` | Headers attached to the proxy → callback request, e.g., an HMAC or shared secret your endpoint uses to verify the request. Only `plaintext` and `opaque` types are permitted (no `workspace_secret`). |
| `ttl_seconds` | Required. How long resolved headers are cached before re-invoking the callback. Must be between 60 and 3600. |
| `full_request` | When `true`, every request to a matched host invokes the callback (nothing is cached) and the body includes a `request` snapshot: `method`, `url`, `scheme`, `host`, `path`, `query`, `headers`, and up to 1 MiB of the body as `body_base64` (`body_truncated` marks a cut). |

**Static rules win.** If an enabled header-injection rule matches both the host and the path, the callback is skipped for that request. Within rules, first-match-wins; the same applies between callbacks if multiple match.

### Callback contract

The proxy makes the following request whenever it needs to resolve credentials for a matched host on a cache miss:

```
POST <callback.url>
Content-Type: application/json
X-LangSmith-Signature-JWT: <signature>
<request_headers from your config, attached verbatim except Content-Type and X-LangSmith-Signature-JWT, which the proxy always sets>

{
  "host": "api.example.com",
  "port": 443,
  "identity": {
    "tenant_id": "<workspace-uuid>",
    "sandbox_id": "<sandbox-uuid>",
    "organization_id": "<organization-uuid>",
    "ls_user_id": "<creator-uuid>"
  }
}
```

`identity` tells your endpoint which sandbox is asking, so one callback URL can serve many sandboxes and mint per-sandbox or per-user credentials. `ls_user_id` is the creating user and is omitted when the sandbox was created with a workspace or service key. Ignore fields and headers you do not recognize; the proxy may add more.

Your endpoint must respond `2xx` with a JSON body:

```json
{
  "headers": {
    "Authorization": "Bearer <token>",
    "X-Org-Id": "..."
  }
}
```

The proxy injects every header in the response into the sandbox's outbound request and caches the response for `ttl_seconds`. Any non-2xx response, transport error, or malformed JSON fails closed: the sandbox's request is rejected with `502 callback resolution failed` (no headers injected, response not cached). Redirects are not followed and count as failures.

### Verify callback requests

`request_headers` let your endpoint check a shared secret you chose. To verify that a request came from LangSmith and was not altered in transit, check the `X-LangSmith-Signature-JWT` header. It is a JWT signed with an Ed25519 key (`alg: EdDSA`) whose public half is published at `<LANGSMITH_ENDPOINT>/.well-known/jwks.json`, selected by the token's `kid`.

| Claim | Expected value |
| - | - |
| `iss` | Your LangSmith endpoint origin, e.g. `https://api.smith.langchain.com` |
| `sub` | `langsmith-sandbox-callback` |
| `aud` | Your callback URL, exactly as configured |
| `exp` | Five minutes after issue; reject expired tokens |
| `body_sha256` | Hex SHA-256 of the raw request body |

Verify the signature against the JWKS, check every claim above, hash the body you received, and compare it to `body_sha256`. Then trust `identity` in the body.

### Example

Use a callback when your OAuth tokens are minted on demand by your own service:

```bash
curl -X POST "$LANGSMITH_ENDPOINT/v2/sandboxes/boxes" \
  -H "x-api-key: $LANGSMITH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "snapshot_id": "<snapshot-uuid>",
    "name": "callback-sandbox",
    "proxy_config": {
      "callbacks": [
        {
          "match_hosts": ["api.github.com", "*.githubusercontent.com"],
          "url": "https://auth.your-app.example.com/sandbox-credentials",
          "request_headers": [
            {
              "name": "X-Integrator-Secret",
              "type": "opaque",
              "value": "<shared-secret-your-endpoint-verifies>"
            }
          ],
          "ttl_seconds": 300
        }
      ]
    }
  }'
```

### Configure via SDK

```python Python
from langsmith.sandbox import SandboxClient

client = SandboxClient()

client.create_sandbox(
    name="callback-sandbox",
    proxy_config={
        "callbacks": [
            {
                "match_hosts": ["api.github.com", "*.githubusercontent.com"],
                "url": "https://auth.your-app.example.com/sandbox-credentials",
                "request_headers": [
                    {
                        "name": "X-Integrator-Secret",
                        "type": "opaque",
                        "value": "<shared-secret-your-endpoint-verifies>",
                    }
                ],
                "ttl_seconds": 300,
            }
        ]
    },
)
```

```ts TypeScript
import { SandboxClient } from "langsmith/sandbox";

const client = new SandboxClient();

await client.createSandbox({
  name: "callback-sandbox",
  proxyConfig: {
    callbacks: [
      {
        match_hosts: ["api.github.com", "*.githubusercontent.com"],
        url: "https://auth.your-app.example.com/sandbox-credentials",
        request_headers: [
          {
            name: "X-Integrator-Secret",
            type: "opaque",
            value: "<shared-secret-your-endpoint-verifies>",
          },
        ],
        ttl_seconds: 300,
      },
    ],
  },
});
```
