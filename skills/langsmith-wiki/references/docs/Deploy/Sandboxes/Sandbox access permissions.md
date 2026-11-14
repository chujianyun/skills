# Sandbox access permissions

> Control who in your workspace can interact with a sandbox after it has been created.

Each sandbox has a recorded **creator**, the workspace member whose API key or session created it. By default, only the creator can run commands, read or write files, open tunnels, or reach service URLs on that sandbox. Other workspace members need the `sandboxes:exec` [permission](../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Role-based%20access%20control.md) to interact with sandboxes they did not create. Sandboxes are never reachable from workspaces other than the one they were created in.

## Who can do what

| Caller | Default | With `sandboxes:exec` |
| - | - | - |
| Sandbox creator | ✅ All runtime actions | ✅ All runtime actions |
| Other workspace member | ❌ Denied | ✅ All runtime actions |
| Different workspace | ❌ Hidden (treated as not found) | ❌ Hidden (treated as not found) |

"Runtime actions" covers the four ways you interact with a running sandbox after creation:

* **Execute** a command (`langsmith sandbox exec`, `SandboxClient.exec`)
* **File** operations (read, write, list paths inside the sandbox)
* **Tunnel** a TCP port back to your machine (`langsmith sandbox tunnel`)
* **Proxy** requests through a [service URL](Sandbox%20service%20URLs.md)

Lifecycle operations—creating, listing, updating, deleting sandboxes—continue to use the existing `sandboxes:create` / `sandboxes:read` / `sandboxes:update` / `sandboxes:delete` permissions. Those are unchanged.

## Denied requests

When a request is denied, the sandbox returns `HTTP 403` with a body that names the rule that fired:

```json
{
  "detail": {
    "error": "Forbidden",
    "message": "sandbox access denied: not the creator and missing sandboxes:exec"
  }
}
```

Requests for a sandbox that exists in another workspace return `404 Not Found` rather than `403`, so the response does not reveal whether the sandbox exists elsewhere.

## Sharing a sandbox

You have two ways to let teammates work with a sandbox you own:

1. **Grant `sandboxes:exec`** to a custom role and assign that role in the workspace. Anyone with the role can interact with every sandbox in the workspace.
2. **Use a [service URL](Sandbox%20service%20URLs.md)** for HTTP services running inside the sandbox. Service URLs use their own access tokens and do not require the recipient to be a workspace member.

For ad-hoc collaboration the service-URL approach is usually simpler; reach for `sandboxes:exec` when a teammate needs broad access to operate sandboxes they did not create.
