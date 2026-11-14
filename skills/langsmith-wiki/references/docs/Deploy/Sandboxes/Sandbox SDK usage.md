# Sandbox SDK usage

> Create and manage sandboxes programmatically with the Python or TypeScript SDK.

The [LangSmith SDK](../../Monitor/Reference/LangSmith%20reference.md) provides a programmatic interface to create and interact with sandboxes.

## Install

```bash Python
# uv
uv add langsmith

# pip
pip install langsmith
```

```bash TypeScript
npm install langsmith
# or
yarn add langsmith
```

The Python SDK includes `websockets`, which enables real-time streaming and `timeout=0`. For TypeScript, install the optional `ws` package for WebSocket streaming:

```bash
npm install ws
```

## Create and run a sandbox

The client reads `LANGSMITH_API_KEY` and `LANGSMITH_ENDPOINT` from the environment, so export both before you create a sandbox:

```bash
export LANGSMITH_API_KEY="<SECRET>"
export LANGSMITH_ENDPOINT="<LANGSMITH_ENDPOINT>"
```

`LANGSMITH_ENDPOINT` defaults to `https://api.smith.langchain.com` (GCP US). Set it to your data plane URL on [BYOC](../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md), your instance URL on [self-hosted](../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md), or the [API URL for your region](../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md#configure-the-sdk) on other Cloud regions.

Pass a snapshot ID or name when you want to boot from a reusable custom filesystem image; see [Snapshots](Sandbox%20snapshots.md) for that flow.

```python Python
from langsmith.sandbox import SandboxClient

# Client uses LANGSMITH_ENDPOINT and LANGSMITH_API_KEY from environment
client = SandboxClient()

# Create a sandbox with the default runtime and run code
with client.sandbox() as sb:
    result = sb.run("python3 -c 'print(2 + 2)'")
    print(result.stdout)  # "4\n"
    print(result.success)  # True
```

```ts TypeScript
import { SandboxClient } from "langsmith/sandbox";

// Client uses LANGSMITH_ENDPOINT and LANGSMITH_API_KEY from environment
const client = new SandboxClient();

// Create a sandbox with the default runtime and run code
const sandbox = await client.createSandbox();
const result = await sandbox.run("node -e 'console.log(2 + 2)'");
console.log(result.stdout); // "4\n"

// Don't forget to clean up
await sandbox.delete();
```

## Run commands

Every `run()` call returns an `ExecutionResult` with `stdout`, `stderr`, `exit_code`, and `success`.

```python Python
with client.sandbox() as sb:
    result = sb.run("echo 'Hello, World!'")

    print(result.stdout)     # "Hello, World!\n"
    print(result.stderr)     # ""
    print(result.exit_code)  # 0
    print(result.success)    # True

    # Commands that fail return non-zero exit codes
    result = sb.run("exit 1")
    print(result.success)    # False
    print(result.exit_code)  # 1
```

```ts TypeScript
const sandbox = await client.createSandbox();
try {
  const result = await sandbox.run("echo 'Hello, World!'");

  console.log(result.stdout);     // "Hello, World!\n"
  console.log(result.stderr);     // ""
  console.log(result.exit_code);  // 0

  // Pass environment variables and working directory
  const envResult = await sandbox.run("echo $MY_VAR", {
    env: { MY_VAR: "test-value" },
    cwd: "/tmp",
  });
} finally {
  await sandbox.delete();
}
```

## Stream output

For long-running commands, stream output in real time using callbacks or a `CommandHandle`.

### Stream with callbacks

```python Python
import sys

with client.sandbox() as sb:
    result = sb.run(
        "make build",
        timeout=600,
        on_stdout=lambda s: print(s, end=""),
        on_stderr=lambda s: print(s, end="", file=sys.stderr),
    )
    print(f"\nBuild {'succeeded' if result.success else 'failed'}")
```

```ts TypeScript
const result = await sandbox.run("make build", {
  timeout: 600,
  onStdout: (data) => process.stdout.write(data),
  onStderr: (data) => process.stderr.write(data),
});
console.log(`Exit code: ${result.exit_code}`);
```

### Stream with CommandHandle

Set `wait=False` to get a `CommandHandle` for full control over the output stream.

```python Python
with client.sandbox() as sb:
    handle = sb.run("make build", timeout=600, wait=False)

    print(f"Command ID: {handle.command_id}")

    for chunk in handle:
        prefix = "OUT" if chunk.stream == "stdout" else "ERR"
        print(f"[{prefix}] {chunk.data}", end="")

    result = handle.result
    print(f"\nExit code: {result.exit_code}")
```

```ts TypeScript
const handle = await sandbox.run("python train.py", {
  wait: false,
  timeout: 600,
});

console.log(`Command ID: ${handle.commandId}`);
console.log(`PID: ${handle.pid}`);

for await (const chunk of handle) {
  if (chunk.stream === "stdout") {
    process.stdout.write(chunk.data);
  } else {
    process.stderr.write(chunk.data);
  }
}

const result = await handle.result;
console.log(`Exit code: ${result.exit_code}`);
```

### Send stdin and kill commands

```python Python
with client.sandbox() as sb:
    handle = sb.run(
        "python -c 'name = input(\"Name: \"); print(f\"Hello {name}\")'",
        timeout=30,
        wait=False,
    )

    for chunk in handle:
        if "Name:" in chunk.data:
            handle.send_input("World\n")
        print(chunk.data, end="")

    result = handle.result
```

```ts TypeScript
const handle = await sandbox.run("python -i", { wait: false });

// Send input to stdin
handle.sendInput("print(2 + 2)\n");
handle.sendInput("exit()\n");

for await (const chunk of handle) {
  process.stdout.write(chunk.data);
}
```

Kill a running command:

```python Python
with client.sandbox() as sb:
    handle = sb.run("python server.py", timeout=0, wait=False)

    for chunk in handle:
        print(chunk.data, end="")
        if "Ready" in chunk.data:
            break

    handle.kill()
```

```ts TypeScript
const handle = await sandbox.run("sleep 300", { wait: false });
handle.kill();

const result = await handle.result;
console.log(result.exit_code); // non-zero
```

### Reconnect to a running command

If a client disconnects, reconnect using the command ID:

```python Python
with client.sandbox() as sb:
    handle = sb.run("make build", timeout=600, wait=False)
    command_id = handle.command_id

    # Later, possibly in a different process
    handle = sb.reconnect(command_id)
    for chunk in handle:
        print(chunk.data, end="")
    result = handle.result
```

```ts TypeScript
const handle = await sandbox.run("long-task", { wait: false });
const commandId = handle.commandId;

// Later, or from a different client
const newHandle = await sandbox.reconnect(commandId);
for await (const chunk of newHandle) {
  process.stdout.write(chunk.data);
}
```

## File operations

Read and write files in the sandbox:

```python Python
with client.sandbox() as sb:
    # Write a file
    sb.write("/app/script.py", "print('Hello from file!')")

    # Run the script
    result = sb.run("python /app/script.py")
    print(result.stdout)  # "Hello from file!\n"

    # Read a file (returns bytes)
    content = sb.read("/app/script.py")
    print(content.decode())  # "print('Hello from file!')"

    # Write binary files
    sb.write("/app/data.bin", b"\x00\x01\x02\x03")
```

```ts TypeScript
const sandbox = await client.createSandbox();
try {
  // Write a file (string content)
  await sandbox.write("/app/script.py", "print('Hello from file!')");

  // Run the script
  const result = await sandbox.run("python /app/script.py");
  console.log(result.stdout);  // "Hello from file!\n"

  // Read a file (returns Uint8Array)
  const content = await sandbox.read("/app/script.py");
  console.log(new TextDecoder().decode(content));

  // Write binary files
  await sandbox.write("/app/data.bin", new Uint8Array([0x00, 0x01, 0x02, 0x03]));
} finally {
  await sandbox.delete();
}
```

### Share a file as a link

To hand one file to something that cannot send an API key, such as a browser tab, an `<a href>`, or a webhook consumer, mint a download link instead of reading the bytes yourself:

```python Python
link = sb.generate_download_url("/app/report.csv", expires_in_seconds=3600)
print(link.download_url)
```

```ts TypeScript
const link = await sandbox.generateDownloadURL("/app/report.csv", {
  expiresInSeconds: 3600,
});
console.log(link.download_url);
```

Omit the expiry for a link that never expires. Do not modify the file afterwards: a link is pinned to a path, not to a snapshot of the contents, so a later write may or may not be reflected in what the link serves. See [Sandbox download links](Sandbox%20download%20links.md) for options and security considerations.

## Mount a Context Hub repo

Mount a [Context Hub](../Prompt%20%26%20Context%20Hub/Context%20Hub/Use%20the%20Context%20Hub.md) repo to give sandbox code filesystem access to your agents and skills. The repo's latest commit tree is mirrored into the mount path and kept in sync for the sandbox's lifetime, so a new commit shows up in the running sandbox without a restart.

> [!WARNING]
>
> Context Hub mounts are **read-only**. The sync is one-way, from the repo into the sandbox: files an agent writes under the mount path are never pushed back to the repo, and the next sync overwrites them. Write sandbox output to a path outside the mount, and [push it with the SDK](../Prompt%20%26%20Context%20Hub/Context%20Hub/Manage%20contexts%20with%20the%20SDK.md) if it belongs in the repo.

Pass the mount through `mount_config`. The API key that creates the sandbox must have access to the repo, otherwise creation fails with a `403`.

```python Python
from langsmith.sandbox import AsyncSandboxClient, context_hub_mount, mount_config


async def main():
    async with AsyncSandboxClient() as client:
        async with await client.sandbox(
            name="context-hub-mount-sandbox",
            mount_config=mount_config(
                mounts=[
                    context_hub_mount(
                        id="memories",
                        mount_path="/memories",
                        repo="-/my-agent",
                    )
                ],
            ),
        ) as sb:
            result = await sb.run("ls /memories")
            print(result.stdout)
```

```ts TypeScript
import {
  SandboxClient,
  contextHubMount,
  mountConfig,
} from "langsmith/sandbox";

const client = new SandboxClient();

const sandbox = await client.createSandbox({
  name: "context-hub-mount-sandbox",
  mountConfig: mountConfig({
    mounts: [
      contextHubMount({
        id: "memories",
        mountPath: "/memories",
        repo: "-/my-agent",
      }),
    ],
  }),
});

try {
  const result = await sandbox.run("ls /memories");
  console.log(result.stdout);
} finally {
  await sandbox.delete();
}
```

`repo` is the repo handle, optionally qualified as `owner/repo`, where `-` is the current workspace. `mount_path` must be an absolute, clean path outside the system directories, and unlike bucket and Git mounts it is not restricted to `/mnt/mounts`.

For sync behavior, sync limits, and mounting buckets and Git repositories alongside a repo, see [Sandbox mounts](Sandbox%20mounts.md#mount-a-context-hub-repo).

## Size a sandbox

Pass `vcpus`, `mem_bytes`, and `fs_capacity_bytes` (`vCpus`, `memBytes`, `fsCapacityBytes` in TypeScript) to size a sandbox at creation. Omit them and the sandbox gets the defaults below.

```python Python
sb = client.create_sandbox(
    name="big-vm",
    vcpus=4,
    mem_bytes=16 * 1024**3,        # 16 GiB
    fs_capacity_bytes=32 * 1024**3, # 32 GiB
)
```

```ts TypeScript
const sb = await client.createSandbox({
  name: "big-vm",
  vCpus: 4,
  memBytes: 17_179_869_184,        // 16 GiB
  fsCapacityBytes: 34_359_738_368, // 32 GiB
});
```

| Resource | Default | Range |
| - | - | - |
| CPU | 0.5 vCPU | 0.05 to 16 vCPU. Use `cpu_millicores` for sub-core requests (`500` is 0.5 vCPU); it takes precedence over `vcpus`. |
| Memory | 4 GiB per vCPU | Up to 64 GiB. Must stay within 50% of the per-vCPU target, so a 1 vCPU sandbox accepts 2 to 6 GiB. Set memory without CPU and the CPU is derived from the same ratio. |
| Filesystem | Snapshot capacity | Up to 64 GiB, and never smaller than the snapshot it boots from. |

Sandboxes burst to twice their requested CPU when the host has spare capacity. Resizing an existing sandbox with `update_sandbox` / `updateSandbox` takes effect at its next start, and a resize enforces only the 64 GiB ceiling rather than the per-vCPU ratio.

> [!NOTE]
>
> Free-form `labels` (up to 128 per sandbox, 256 bytes per key and 4096 bytes per value) can be set through the REST API on create. Sandboxes inherit their snapshot's labels unless overridden. The `langsmith.sandbox` clients do not expose this field yet.

## Create a non-persistent sandbox

A non-persistent sandbox keeps filesystem writes only while it runs. Use it for disposable code execution or evaluations that do not need files after a stop. Non-persistent sandboxes incur no storage charges; compute usage still applies.

Persistence is enabled by default. Set `persistent` to `false` when creating a sandbox to opt out. This setting applies to the new sandbox, not existing sandboxes.

> [!NOTE]
>
> These examples use Python `langsmith` version 0.14.17 or later, TypeScript `langsmith` version 0.11.7 or later, Go `github.com/langchain-ai/langsmith-go` v0.29.3, and Java `com.langchain.smith:langsmith-java` version 0.1.0-beta.28.

Set `LANGSMITH_API_KEY` and `LANGSMITH_ENDPOINT` as described in [Create and run a sandbox](#create-and-run-a-sandbox). Files remain available between commands while the sandbox runs:

```python Python
from langsmith.sandbox import SandboxClient

client = SandboxClient()
with client.sandbox(persistent=False) as sandbox:
    sandbox.run("echo hello > /tmp/example.txt")
    result = sandbox.run("cat /tmp/example.txt")
    print(result.stdout)
```

```ts TypeScript
import { SandboxClient } from "langsmith/sandbox";

const client = new SandboxClient();
const sandbox = await client.createSandbox({ persistent: false });
try {
  await sandbox.run("echo hello > /tmp/example.txt");
  const result = await sandbox.run("cat /tmp/example.txt");
  console.log(result.stdout);
} finally {
  await sandbox.delete();
}
```

```go Go
package main

import (
	"context"
	"fmt"
	"log"

	langsmith "github.com/langchain-ai/langsmith-go"
)

func main() {
	ctx := context.Background()
	client := langsmith.NewClient()
	sandbox, err := client.Sandboxes.Boxes.NewSandbox(ctx, langsmith.SandboxBoxNewParams{
		Persistent: langsmith.F(false),
	})
	if err != nil {
		log.Fatal(err)
	}
	defer sandbox.Delete(ctx)

	result, err := sandbox.Run(ctx, langsmith.SandboxBoxRunParams{
		Command: langsmith.F("echo hello > /tmp/example.txt && cat /tmp/example.txt"),
	})
	if err != nil {
		log.Print(err)
		return
	}
	fmt.Print(result.Stdout)
}
```

```java Java
import com.langchain.smith.client.okhttp.OkHttpClient;
import com.langchain.smith.core.ClientOptions;
import com.langchain.smith.models.sandboxes.boxes.BoxCreateParams;
import com.langchain.smith.sandbox.Sandbox;
import com.langchain.smith.sandbox.SandboxClient;

public class NonPersistentSandbox {
    public static void main(String[] args) {
        ClientOptions options = ClientOptions.builder()
            .fromEnv()
            .httpClient(OkHttpClient.builder().build())
            .build();
        try {
            SandboxClient client = SandboxClient.of(options);
            Sandbox sandbox = client.create(
                BoxCreateParams.builder().persistent(false).build()
            );
            try {
                sandbox.run("echo hello > /tmp/example.txt");
                System.out.print(sandbox.run("cat /tmp/example.txt").stdoutString());
            } finally {
                sandbox.delete();
            }
        } finally {
            options.close();
        }
    }
}
```

The Python context manager deletes the sandbox when the block exits. For manual cleanup, use `client.create_sandbox(persistent=False)` and call `sandbox.delete()` when finished. The TypeScript `finally` block deletes the sandbox even if a command fails.

> [!WARNING]
>
> Both an idle timeout and an explicit stop discard filesystem writes. The next start boots fresh from the snapshot. Save outputs outside the sandbox before it stops. Setting `delete_after_stop_seconds` does not preserve these writes.

Non-persistent sandboxes cannot preserve memory on stop or capture their filesystem as a snapshot. Some snapshots captured from other sandboxes cannot boot a non-persistent sandbox. Use the default snapshot or a compatible [custom snapshot](Sandbox%20snapshots.md). Disk capacity is limited to 16 GiB per vCPU.

## Sandbox lifetime and retention

Sandboxes are governed by a two-stage retention model anchored to **idle
activity** and the **`stopped`** state.

| Field | What it controls | When it fires |
| - | - | - |
| `idle_ttl_seconds` | The launcher stops the sandbox after this many seconds of inactivity. Any command execution or file I/O resets the timer. `0` disables the idle stop. | Default `600` (10 minutes) when omitted. |
| `delete_after_stop_seconds` | Once the sandbox enters the `stopped` state, this timer starts. After it elapses, the sandbox row + filesystem clone are permanently deleted by a server-side sweep. `0` disables stop-anchored deletion (manual cleanup required). | Server applies its configured default (typically 14 days) when omitted. |

Both values must be multiples of 60 (minute resolution), and `delete_after_stop_seconds` caps at 2592000 (30 days). The full lifecycle is:

```
running ──(idle for idle_ttl_seconds)──▶ stopped ──(delete_after_stop_seconds)──▶ deleted
```

You can also call `stop_sandbox` / `stopSandbox` explicitly to release resources before the idle timeout fires; that also populates `stopped_at` and starts the deletion timer. You do not need to start it again afterwards: a stopped sandbox wakes on the next command, file operation, or service-URL request.

```python Python
# Default retention (server defaults: 10-min idle stop, 14-day delete)
with client.sandbox() as sb:
    sb.run("echo hello")

# Aggressive: stop after 5 min idle, delete 1 hour after stop
sb = client.create_sandbox(
    idle_ttl_seconds=300,
    delete_after_stop_seconds=3600,
)

# Long-running: never auto-stop, delete 7 days after manual stop
sb = client.create_sandbox(
    idle_ttl_seconds=0,
    delete_after_stop_seconds=604800,
)

# Update retention on an existing sandbox
sb = client.update_sandbox(
    sb.name,
    idle_ttl_seconds=1800,
    delete_after_stop_seconds=2592000,  # 30 days
)
```

```ts TypeScript
// Default retention (server defaults applied)
const sandbox = await client.createSandbox();

// Aggressive: stop after 5 min idle, delete 1 hour after stop
const sb = await client.createSandbox({
  idleTtlSeconds: 300,
  deleteAfterStopSeconds: 3600,
});

// Long-running: never auto-stop, delete 7 days after manual stop
const longRunning = await client.createSandbox({
  idleTtlSeconds: 0,
  deleteAfterStopSeconds: 604800,
});

// Update retention on an existing sandbox
await client.updateSandbox(sb.name, {
  idleTtlSeconds: 1800,
  deleteAfterStopSeconds: 2592000, // 30 days
});
```

## Command lifecycle and TTL

The sandbox daemon manages command session lifecycles with two timeout mechanisms:

* **Session TTL (finished commands)**: After a command finishes, its session remains in memory for a TTL period (default: 5 minutes). During this window you can reconnect to retrieve output. After the TTL expires, the session is cleaned up. Set `ttl_seconds` to `-1` to keep the session indefinitely.
* **Idle timeout (running commands)**: Running commands with no connected clients are killed after an idle timeout (default: 1 hour). The idle timer resets each time a client connects. Set `idle_timeout` to `-1` for no idle timeout.

### Combine lifecycle options

```python Python
with client.sandbox() as sb:
    # Long-running task: 30-min idle timeout, 1-hour session TTL
    handle = sb.run(
        "python train.py",
        timeout=0,              # No command timeout
        idle_timeout=1800,      # Kill after 30min with no clients
        ttl_seconds=3600,       # Keep session for 1 hour after exit
        wait=False,
    )

    # Fire-and-forget: no idle timeout, infinite TTL
    handle = sb.run(
        "python background_job.py",
        timeout=0,
        idle_timeout=-1,        # Never kill due to idle
        ttl_seconds=-1,         # Keep session forever
        wait=False,
    )
```

```ts TypeScript
const sandbox = await client.createSandbox();
try {
  // Long-running task: 30-min idle timeout, 1-hour session TTL
  const handle = await sandbox.run("python train.py", {
    timeout: 0,              // No command timeout
    idleTimeout: 1800,       // Kill after 30min with no clients
    ttlSeconds: 3600,        // Keep session for 1 hour after exit
    wait: false,
  });

  // Fire-and-forget: no idle timeout, infinite TTL
  const bg = await sandbox.run("python background_job.py", {
    timeout: 0,
    idleTimeout: -1,         // Never kill due to idle
    ttlSeconds: -1,          // Keep session forever
    wait: false,
  });
} finally {
  await sandbox.delete();
}
```

Set `kill_on_disconnect=True` (Python) or `killOnDisconnect: true` (TypeScript) to kill the command immediately when the last client disconnects, instead of waiting for the idle timeout.

## Service URLs (Python)

Access an HTTP service running inside a sandbox via an authenticated URL. You can open it in a browser, call it from code, or share it with a teammate.

```python
with client.sandbox() as sb:
    sb.run("python -m http.server 8000", timeout=0, wait=False)

    svc = sb.service(port=8000)

    # Open in a browser
    print(svc.browser_url)

    # Or make requests with built-in helpers (auth is injected automatically)
    resp = svc.get("/api/data")
    resp = svc.post("/api/data", json={"key": "value"})
```

For more details, including use cases, REST API access, and a full FastAPI example, see [Service URLs](Sandbox%20service%20URLs.md).

## TCP tunnels (Python)

Access any TCP service running inside a sandbox as if it were local. The tunnel opens a local TCP port and forwards connections through a WebSocket to the target port inside the sandbox.

```python
import psycopg2

# Snapshot built from the official postgres:16 image
sb = client.create_sandbox(snapshot_id=postgres_snapshot_id)
pg_handle = sb.run(
    "POSTGRES_HOST_AUTH_METHOD=trust docker-entrypoint.sh postgres",
    timeout=0,
    wait=False,
)
import time; time.sleep(6)  # Wait for Postgres to start

try:
    with sb.tunnel(remote_port=5432, local_port=25432) as t:
        conn = psycopg2.connect(
            host="127.0.0.1",
            port=t.local_port,
            user="postgres",
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        print(cursor.fetchone())
        conn.close()
finally:
    pg_handle.kill()
    client.delete_sandbox(sb.name)
```

Tunnels work with any TCP service (Redis, HTTP servers, etc.) and you can open multiple tunnels simultaneously:

```python
with sb.tunnel(remote_port=5432, local_port=25432) as t1, \
     sb.tunnel(remote_port=6379, local_port=26379) as t2:
    # Use both Postgres and Redis simultaneously
    pass
```

## Async support (Python)

The Python SDK provides a full async client:

```python
from langsmith.sandbox import AsyncSandboxClient

async def main():
    async with AsyncSandboxClient() as client:
        async with await client.sandbox() as sb:
            result = await sb.run("python -c 'print(1 + 1)'")
            print(result.stdout)  # "2\n"

            await sb.write("/app/test.txt", "async content")
            content = await sb.read("/app/test.txt")
            print(content.decode())

            # Async streaming
            handle = await sb.run("make build", timeout=600, wait=False)
            async for chunk in handle:
                print(chunk.data, end="")
            result = await handle.result

            # Async service URLs
            svc = await sb.service(port=8000)
            resp = await svc.get("/api/data")
            url = await svc.get_service_url()
            token = await svc.get_token()
```

## Trace sandbox activity

For tracing in an agent-based workspace, [create an agent and configure agent addressing](../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#configure-tracing-for-the-agent) before running the examples.

Code inside the sandbox needs `langsmith>=0.14.9` in Python or `langsmith@>=0.11.0` in TypeScript to send traces to an agent.

Pass LangSmith tracing environment variables through the `env` parameter on `run()` to send traces from code running inside a sandbox. Call `flush()` before the process exits to ensure all traces are delivered.

```python Python
from langsmith.sandbox import SandboxClient

client = SandboxClient()

tracing_env = {
    "LANGSMITH_API_KEY": "lsv2_pt_...",
    "LANGSMITH_ENDPOINT": "https://api.smith.langchain.com",
    "LANGSMITH_TRACING": "true",
    "LANGSMITH_AGENT_ID": "<your-agent-id>",
    "LANGSMITH_AGENT_ENVIRONMENT": "production",
}

with client.sandbox() as sandbox:
    sandbox.run("pip install langsmith", timeout=120, env=tracing_env)
    result = sandbox.run("python3 my_agent.py", env=tracing_env)
    print(result.stdout)
```

```ts TypeScript
import { SandboxClient } from "langsmith/sandbox";

const client = new SandboxClient();

const tracingEnv = {
  LANGSMITH_API_KEY: "lsv2_pt_...",
  LANGSMITH_ENDPOINT: "https://api.smith.langchain.com",
  LANGSMITH_TRACING: "true",
  LANGSMITH_AGENT_ID: "<your-agent-id>",
  LANGSMITH_AGENT_ENVIRONMENT: "production",
};

const sandbox = await client.createSandbox();
try {
  await sandbox.run("pip install langsmith", { timeout: 120, env: tracingEnv });
  const result = await sandbox.run("python3 my_agent.py", { env: tracingEnv });
  console.log(result.stdout);
} finally {
  await sandbox.delete();
}
```

Inside the sandbox, any LangSmith-instrumented code (`@traceable`, LangChain, LangGraph) automatically picks up the tracing configuration from the injected environment variables.

> [!WARNING]
>
> Always call `flush()` before the sandbox process exits—`langsmith.Client().flush()` in Python or `await new Client().flush()` in TypeScript. Without it, traces may be lost because the container is destroyed when the command finishes.

## Error handling

Both SDKs provide typed exceptions for specific error handling:

```python Python
from langsmith.sandbox import (
    SandboxClientError,       # Base exception
    ResourceCreationError,    # Provisioning failed
    ResourceNotFoundError,    # Resource doesn't exist
    ResourceTimeoutError,     # Operation timed out
    SandboxNotReadyError,     # Sandbox not ready yet
    SandboxConnectionError,   # Network/WebSocket error
    CommandTimeoutError,      # Command exceeded timeout
    QuotaExceededError,       # Quota limit reached
)

try:
    with client.sandbox() as sb:
        result = sb.run("sleep 999", timeout=10)
except CommandTimeoutError as e:
    print(f"Command timed out: {e}")
except ResourceNotFoundError as e:
    print(f"{e.resource_type} not found: {e}")
except SandboxClientError as e:
    print(f"Error: {e}")
```

```ts TypeScript
import {
  LangSmithSandboxError,
  LangSmithResourceNotFoundError,
  LangSmithResourceTimeoutError,
  LangSmithSandboxConnectionError,
  LangSmithCommandTimeoutError,
  LangSmithQuotaExceededError,
} from "langsmith/sandbox";

try {
  const sandbox = await client.createSandbox("not-a-real-snapshot");
  await sandbox.delete();
} catch (e) {
  if (e instanceof LangSmithResourceNotFoundError) {
    console.log(`${e.resourceType} not found: ${e.message}`);
  } else if (e instanceof LangSmithResourceTimeoutError) {
    console.log(`Timeout waiting for ${e.resourceType}: ${e.message}`);
  } else if (e instanceof LangSmithSandboxError) {
    console.log(`Error: ${e.message}`);
  }
}
```

> [!NOTE]
>
> For more details, see the sandbox SDK reference on GitHub for [Python](https://github.com/langchain-ai/langsmith-python/tree/main/src/langsmith/sandbox) or [TypeScript](https://github.com/langchain-ai/langsmith-javascript/tree/main/src/lib/sandbox).
