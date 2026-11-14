# Sandbox CLI

> Create, inspect, connect to, and tunnel into LangSmith sandboxes from the command line.

The [LangSmith CLI](../../LangSmith%20setup/Govern/Tools/LangSmith%20CLI.md) includes sandbox commands for creating snapshots, booting sandboxes, running commands, opening interactive shells, and tunneling TCP connections into a sandbox.

Sandbox CLI commands require LangSmith CLI `v0.2.26` or later.

## Install and authenticate

Install or upgrade the LangSmith CLI:

```bash
curl -fsSL https://cli.langsmith.com/install.sh | sh
langsmith self-update
```

Authenticate the CLI with your LangSmith API key, and point it at the environment that key belongs to:

```bash
export LANGSMITH_API_KEY="<SECRET>"
export LANGSMITH_ENDPOINT="<LANGSMITH_ENDPOINT>"
```

`LANGSMITH_ENDPOINT` defaults to `https://api.smith.langchain.com` (GCP US). Set it to your data plane URL on [BYOC](../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md), your instance URL on [self-hosted](../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md), or the [API URL for your region](../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md#configure-the-sdk) on other Cloud regions.

CLI output is human-readable tables by default. Add `--format json` for scriptable output:

```bash
langsmith --format json sandbox list
```

## End-to-end workflow

Create a sandbox, then run commands inside it:

```bash
langsmith sandbox create my-vm

langsmith sandbox exec my-vm -- python --version
```

`create` boots the sandbox and returns once it reports `ready`, so the next command can run straight away. There is no separate wait step. Pass `--console` to drop into an interactive shell as soon as the sandbox comes up.

When you are done with a sandbox, delete it:

```bash
langsmith sandbox delete my-vm
```

## Manage snapshots

Build snapshots from Docker images:

```bash
langsmith sandbox snapshot build my-snapshot \
  --docker-image ubuntu:24.04 \
  --capacity 8gb
```

`build` queues the build and returns immediately with the snapshot's `status`. Poll `langsmith sandbox snapshot get <SNAPSHOT_ID>` until it reports `ready`. `--capacity` defaults to `4gb` and caps at `64gb`.

For private images, create a registry first (see [Private registries](Sandbox%20snapshots.md#private-registries)), then pass its id with `--registry-id`:

```bash
langsmith sandbox snapshot build internal-python \
  --docker-image registry.example.com/internal/python:3.12 \
  --registry-id "$REGISTRY_ID"
```

Capture the filesystem from a running sandbox:

```bash
langsmith sandbox snapshot capture ml-ready --box my-vm
```

List, inspect, and delete snapshots:

```bash
langsmith sandbox snapshot list
langsmith sandbox snapshot get <SNAPSHOT_ID>
langsmith sandbox snapshot delete <SNAPSHOT_ID>
```

## Manage sandboxes

Create a sandbox with the default runtime. Add `--snapshot-id` only when you want to boot from a reusable custom snapshot:

```bash
langsmith sandbox create my-vm --rootfs-capacity 8gb
```

Size the sandbox with `--vcpus` and `--memory`. Memory is tied to CPU at 4 GiB per vCPU and must stay within 50% of that target, so a 2-vCPU sandbox accepts 4 to 12 GiB. Omit `--memory` and it follows the ratio.

```bash
langsmith sandbox create my-vm --vcpus 2 --memory 8gb
```

List and inspect sandboxes:

```bash
langsmith sandbox list
langsmith sandbox get my-vm
```

Stop a sandbox to release resources early. Its filesystem is preserved, and the next `exec`, `console`, or service request wakes it automatically, so there is no start step to run:

```bash
langsmith sandbox stop my-vm
langsmith sandbox exec my-vm -- echo awake
```

Update resources or proxy configuration:

```bash
langsmith sandbox update my-vm --rootfs-capacity 16gb
langsmith sandbox update my-vm --proxy-config @proxy.json
```

Resource changes take effect the next time the sandbox boots. Proxy configuration changes take effect immediately.

### Proxy configuration

Use `--proxy-config @proxy.json` on `create` or `update` to configure the sandbox auth proxy. Prefer workspace secrets for credential injection instead of placing raw secrets in local files.

```json
{
  "rules": [
    {
      "name": "openai",
      "match_hosts": ["api.openai.com"],
      "match_paths": [],
      "headers": [
        {
          "name": "Authorization",
          "type": "workspace_secret",
          "value": "Bearer {OPENAI_API_KEY}"
        }
      ],
      "enabled": true
    }
  ],
  "access_control": {
    "allow_list": ["api.openai.com"],
    "deny_list": []
  }
}
```

For more on proxy rules, see [Sandbox auth proxy](Sandbox%20auth%20proxy.md).

## Run commands

Use `sandbox exec` for one-off commands:

```bash
langsmith sandbox exec my-vm -- uname -a
langsmith sandbox exec my-vm -- ls -la /
langsmith sandbox exec my-vm -- cat /etc/os-release
```

Everything after `--` is sent to the sandbox as the command. The CLI prints stdout to stdout, stderr to stderr, and exits with the sandbox command's exit code.

## Open an interactive console

Use `sandbox console` for a PTY-backed interactive shell:

```bash
langsmith sandbox console my-vm
langsmith sandbox console my-vm --shell /bin/sh
```

You can forward your local SSH agent into the console session:

```bash
langsmith sandbox console my-vm --forward-ssh-agent
```

`--forward-ssh-agent` requires `SSH_AUTH_SOCK` to be set locally. Interactive console sessions are not supported on Windows; use SSH access instead.

## Share a file as a link

Mint a link that downloads a single file from the sandbox with no LangSmith credential, for a browser tab or anything else that cannot send an API key:

```bash
langsmith sandbox generate-download-url my-vm --path /app/report.csv
```

Without `--expires-in-seconds` the link never expires. Add `--content-type` and `--content-disposition inline` to have the browser render the file instead of downloading it. Do not modify the file afterwards: a link is pinned to a path, not to a snapshot of the contents, so a later write may or may not be reflected in what the link serves. See [Sandbox download links](Sandbox%20download%20links.md).

## Tunnel TCP ports

Use `sandbox tunnel` when you need a local TCP port that forwards to a service listening inside the sandbox. This is useful for databases, language servers, custom protocols, or local tools that expect `localhost`.

Start a service in the sandbox, then tunnel to it:

```bash
langsmith sandbox exec my-vm -- sh -c 'cd /tmp && nohup python -m http.server 8000 > /tmp/http.log 2>&1 &'
langsmith sandbox tunnel my-vm --remote-port 8000 --local-port 18000
```

Then connect locally:

```bash
curl http://127.0.0.1:18000
```

If you omit `--local-port`, the CLI uses the same value as `--remote-port`:

```bash
langsmith sandbox tunnel my-vm --remote-port 5432
```

The tunnel process stays in the foreground. Stop it with `Ctrl+C`.

You can also tunnel by sandbox URL instead of name:

```bash
langsmith sandbox tunnel \
  --url <SANDBOX_URL> \
  --remote-port 5432
```

> [!TIP]
>
> For HTTP applications you want to open in a browser or share with teammates, use [Sandbox service URLs](Sandbox%20service%20URLs.md). Use tunnels for raw TCP protocols or local development tools.

## Set up SSH access

Use `sandbox ssh-setup` to configure standard SSH tools such as `ssh`, `scp`, `rsync`, and `sftp` through a sandbox tunnel.

```bash
langsmith sandbox ssh-setup my-vm
langsmith sandbox ssh-setup my-vm --identity ~/.ssh/id_ed25519.pub
```

The command uploads your SSH public key to the sandbox, fetches the sandbox host key when available, writes a `Host sandbox-<name>` block to `~/.ssh/config`, and writes sandbox host keys to `~/.ssh/known_hosts_sandboxes`.

After setup, connect with:

```bash
ssh sandbox-my-vm
```

The sandbox image must run `sshd` on port `22`. If `sshd` is not running, `ssh-setup` warns and the SSH connection will not work until you start it inside the sandbox.

> [!WARNING]
>
> `ssh-setup` modifies local SSH configuration and writes a `ProxyCommand` that calls `langsmith sandbox tunnel`. Depending on how the CLI is authenticated, the generated block may contain credentials or references to credentials. Run it only on trusted machines and do not commit or share the generated SSH config block.

## Command reference

| Command | Description |
| - | - |
| `langsmith sandbox snapshot list` | List snapshots. |
| `langsmith sandbox snapshot build <name> --docker-image <image>` | Build a snapshot from a Docker image. |
| `langsmith sandbox snapshot capture <name> --box <sandbox>` | Capture a snapshot from a running sandbox. |
| `langsmith sandbox snapshot get <snapshot-id>` | Inspect a snapshot. |
| `langsmith sandbox snapshot delete <snapshot-id>` | Delete a snapshot. |
| `langsmith sandbox create <name>` | Create a sandbox with the default runtime. |
| `langsmith sandbox list` | List sandboxes. |
| `langsmith sandbox get <name>` | Inspect a sandbox. |
| `langsmith sandbox update <name>` | Update sandbox resources or proxy config. |
| `langsmith sandbox stop <name>` | Stop a running sandbox while preserving filesystem state. A later `exec`, `console`, or service request wakes it again. |
| `langsmith sandbox delete <name>` | Delete a sandbox. |
| `langsmith sandbox exec <name> -- <command>` | Run a one-off command inside a sandbox. |
| `langsmith sandbox console <name>` | Open an interactive shell inside a sandbox. |
| `langsmith sandbox generate-download-url <name> --path <path>` | Mint a link that downloads one sandbox file with no credential. |
| `langsmith sandbox tunnel <name> --remote-port <port>` | Forward a local TCP port to a sandbox port. |
| `langsmith sandbox ssh-setup <name>` | Configure local SSH access through `sandbox tunnel --stdio`. |
