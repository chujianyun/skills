# Profile configuration

> Configure LangSmith SDK credentials and endpoints with a local profile file.

LangSmith SDK profiles let you keep [API keys](Create%20an%20account%20and%20API%20key.md), endpoints, and workspace IDs in a reusable JSON file instead of setting the same environment variables in every shell session.

Use profiles when:

* You switch between [LangSmith Cloud regions](../Cloud/Cloud%20%28SaaS%29.md#regions), self-hosted instances, or [workspaces](../Govern/Organization/Overview.md#workspaces) often.
* You want a remote runtime to load the same SDK configuration from a mounted file.

> [!WARNING]
>
> Profile files can contain API keys and OAuth refresh tokens. Do not commit them to source control, bake them into container images, or print them in logs. Store and mount them with the same care as other credentials.

## Minimum versions

Profile support is available in the following releases:

| Tool or SDK | Minimum version |
| - | - |
| LangSmith CLI profile commands | `v0.2.26` |
| `langsmith auth login` | `v0.2.30` |
| Go SDK | `v0.7.0` |
| Python SDK | `v0.8.1` |
| TypeScript SDK | `v0.6.1` |
| Java SDK | `v0.1.0-beta.3` |

## Profile file location

By default, [SDKs](../../Monitor/Reference/LangSmith%20reference.md) look for a profile file at:

```text
~/.langsmith/config.json
```

To use a different path, set `LANGSMITH_CONFIG_FILE`:

```shell
export LANGSMITH_CONFIG_FILE=/path/to/langsmith-config.json
```

The TypeScript SDK only loads profiles in Node.js-like runtimes. Browser and web worker runtimes do not have filesystem access, so pass configuration explicitly in those environments.

## Create a profile file

Create `~/.langsmith/config.json` with a `profiles` object. Each profile can define:

| Field | Description |
| - | - |
| `api_url` | LangSmith API endpoint. Use the same value you would use for `LANGSMITH_ENDPOINT`. |
| `api_key` | LangSmith API key. See [Create an account and API key](Create%20an%20account%20and%20API%20key.md). |
| `workspace_id` | Workspace ID. Required when the API key can access multiple workspaces. |
| `oauth` | OAuth token metadata created by LangSmith tooling. |

```json
{
  "current_profile": "dev",
  "profiles": {
    "dev": {
      "api_url": "https://api.smith.langchain.com",
      "api_key": "<LANGSMITH_API_KEY>",
      "workspace_id": "<WORKSPACE_ID>"
    },
    "eu": {
      "api_url": "https://eu.api.smith.langchain.com",
      "api_key": "<EU_LANGSMITH_API_KEY>",
      "workspace_id": "<EU_WORKSPACE_ID>"
    },
    "apac": {
      "api_url": "https://apac.api.smith.langchain.com",
      "api_key": "<APAC_LANGSMITH_API_KEY>",
      "workspace_id": "<APAC_WORKSPACE_ID>"
    }
  }
}
```

Restrict the file so only your user can read it:

```shell
chmod 600 ~/.langsmith/config.json
```

## Select a profile

SDKs select profiles in this order:

1. `LANGSMITH_PROFILE`, if set.
2. `current_profile` in the profile file, if set.
3. A profile named `default`, if present.

For example:

```shell
export LANGSMITH_PROFILE=eu
```

The [LangSmith CLI](../Govern/Tools/LangSmith%20CLI.md) also accepts a global `--profile` flag, which takes precedence over `LANGSMITH_PROFILE` for that command:

```shell
langsmith --profile eu project list
```

## Manage profiles with the CLI

Use the [LangSmith CLI](../Govern/Tools/LangSmith%20CLI.md) to create, inspect, switch, and delete profiles without editing the JSON file by hand.

To create an API-key profile from an existing API key:

```shell
export LANGSMITH_API_KEY=<LANGSMITH_API_KEY>
langsmith profile create dev \
  --workspace-id <WORKSPACE_ID> \
  --set-current
```

You can also pass the key and endpoint as flags. Prefer environment variables on shared machines, because shell history may record command flags.

```shell
langsmith profile create eu \
  --api-key <EU_LANGSMITH_API_KEY> \
  --api-url https://eu.api.smith.langchain.com \
  --workspace-id <EU_WORKSPACE_ID>
```

Common profile commands:

| Command | Description |
| - | - |
| `langsmith profile list` | List saved profiles. Alias: `langsmith profile ls`. |
| `langsmith profile show <name>` | Show a saved profile. Secret values are redacted in output. |
| `langsmith profile use <name>` | Set `current_profile` in the profile file. |
| `langsmith profile set-workspace <workspace-id>` | Set the default workspace for the selected profile. |
| `langsmith profile delete <name>` | Delete a saved profile. |

Output is a human-readable table by default. Use `--format json` for scriptable output:

```shell
langsmith --format json profile list
```

## Authenticate with `langsmith auth login`

Run `langsmith auth login` to authenticate with OAuth instead of manually creating an API-key profile. The command starts a browser-based device authorization flow, stores OAuth tokens in the selected profile, and sets that profile as current.

> [!NOTE]
>
> `langsmith auth login` also works against self-hosted instances from LangSmith CLI `v0.2.46` and later, provided the deployment is on LangSmith `0.16` or later with the OAuth authorization server enabled. The OAuth authorization server is enabled automatically when `config.hostname` is set in your Helm chart **and** a signing JWKS is configured (`config.signingJwks` or key `langsmith_signing_jwks` in `config.existingSecretName`). On earlier deployments, or if no signing JWKS is configured, create an API-key profile instead.

```shell
langsmith auth login
```

Choose the profile with `--profile` or `LANGSMITH_PROFILE`:

```shell
langsmith auth login --profile dev
```

For a self-hosted instance, pass its base URL. The CLI reads the deployment's authorization server metadata to find the OAuth endpoints:

```shell
langsmith auth login --api-url https://langsmith.example.com --profile self-hosted
```

Self-hosted OAuth login requires Helm chart `0.16.0` or later with a signing JWKS. For setup steps, see [Configure a signing JWKS](../Self-hosted/Install%20an%20instance/Self-host%20LangSmith%20on%20Kubernetes.md#configure-a-signing-jwks). Otherwise create an API-key profile.

For a headless environment, suppress automatic browser opening and pass a workspace ID:

```shell
langsmith auth login \
  --profile prod \
  --no-browser \
  --workspace-id <WORKSPACE_ID>
```

`langsmith auth login` chooses the profile name in this order:

1. `--profile`, if passed.
2. `LANGSMITH_PROFILE`, if set.
3. `current_profile` in the profile file, if set.
4. `default`.

It chooses the API URL in this order:

1. `--api-url`, if passed.
2. `LANGSMITH_ENDPOINT`, if set.
3. The selected profile's `api_url`, if present.
4. The default LangSmith Cloud endpoint.

After login, the CLI and SDKs can use the saved profile. The CLI refreshes OAuth tokens when needed and writes refreshed token fields back to the profile file. SDKs also use the OAuth access token from the profile when environment or constructor API-key auth is not set.

## Override profile values

Explicit client constructor arguments and environment variables take precedence over profile values.

| Setting | Precedence |
| - | - |
| Endpoint | Constructor `api_url` or `apiUrl`, then `LANGSMITH_ENDPOINT`, then profile `api_url`, then the default LangSmith Cloud endpoint. |
| Authentication | Constructor API key, then `LANGSMITH_API_KEY`, then profile OAuth access token, then profile `api_key`. |
| Workspace | Constructor `workspace_id` or `workspaceId`, then `LANGSMITH_WORKSPACE_ID`, then profile `workspace_id`. |

The older `LANGCHAIN_API_KEY`, `LANGCHAIN_ENDPOINT`, and `LANGCHAIN_WORKSPACE_ID` aliases still work, but prefer the `LANGSMITH_*` names for new configuration.

If a profile contains both `oauth.access_token` and `api_key`, SDKs use the OAuth access token first. If an OAuth refresh token is present and the access token is expired or close to expiring, SDKs can refresh the token and write the updated token fields back to the profile file.

> [!NOTE]
>
> If you mount a profile file as read-only, OAuth token refresh cannot persist updated tokens. Read-only mounts are appropriate for API-key profiles. Use a writable mount only when you intentionally rely on OAuth token refresh.

## Use profiles in code

When the profile file is present, create the client normally:

```python Python
from langsmith import Client

client = Client()
```

```typescript TypeScript
import { Client } from "langsmith";

const client = new Client();
```

To override a profile in code, pass the value explicitly:

```python Python
from langsmith import Client

client = Client(api_key="<SECRET>")
```

```typescript TypeScript
import { Client } from "langsmith";

const client = new Client({ apiKey: "<SECRET>" });
```

## Mount profiles in remote runtimes

For remote runtimes, mount the profile file as a secret file and set `LANGSMITH_CONFIG_FILE` to the mounted path. Do not copy the file into the image or repository.

### Docker

Mount your local profile directory into the container:

```shell
docker run --rm \
  -e LANGSMITH_CONFIG_FILE=/home/app/.langsmith/config.json \
  -e LANGSMITH_PROFILE=prod \
  -v "$HOME/.langsmith:/home/app/.langsmith:ro" \
  my-image
```

Use a read-write mount only when the profile uses OAuth refresh tokens:

```shell
docker run --rm \
  -e LANGSMITH_CONFIG_FILE=/home/app/.langsmith/config.json \
  -e LANGSMITH_PROFILE=prod \
  -v "$HOME/.langsmith:/home/app/.langsmith" \
  my-image
```

### Kubernetes

Create a Kubernetes secret from the profile file:

```shell
kubectl create secret generic langsmith-profile \
  --from-file=config.json="$HOME/.langsmith/config.json"
```

Mount the secret and point the SDK to it:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  template:
    spec:
      containers:
        - name: app
          image: my-image
          env:
            - name: LANGSMITH_CONFIG_FILE
              value: /var/run/langsmith/config.json
            - name: LANGSMITH_PROFILE
              value: prod
          volumeMounts:
            - name: langsmith-profile
              mountPath: /var/run/langsmith
              readOnly: true
      volumes:
        - name: langsmith-profile
          secret:
            secretName: langsmith-profile
```

Kubernetes secret volumes are read-only. Use API-key profiles for this pattern, or use a writable secret-sync mechanism if your OAuth profile must refresh and persist tokens.

### Remote development and CI

In remote development environments or CI jobs, store the profile JSON in the platform's secret store, write it to a temporary file at runtime, and set `LANGSMITH_CONFIG_FILE` to that file path.

```shell
mkdir -p "$RUNNER_TEMP/langsmith"
printf '%s' "$LANGSMITH_PROFILE_JSON" > "$RUNNER_TEMP/langsmith/config.json"
chmod 600 "$RUNNER_TEMP/langsmith/config.json"
export LANGSMITH_CONFIG_FILE="$RUNNER_TEMP/langsmith/config.json"
export LANGSMITH_PROFILE=prod
```

For hosted [LangSmith Cloud](../Cloud/Cloud%20%28SaaS%29.md), configure these values as environment variables or [workspace secrets](../Govern/Organization/Workspace%20setup/Set%20up%20hierarchy.md#configure-workspace-settings) unless the platform explicitly supports mounting secret files.
