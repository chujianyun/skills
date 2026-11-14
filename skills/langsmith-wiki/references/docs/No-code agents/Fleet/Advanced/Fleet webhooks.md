# Fleet webhooks

> Integrate agent publishing with external systems, CI/CD pipelines, or custom deployment workflows.

When triggered, a webhook sends a complete package of your agent's configuration and files to the specified endpoint.

**Security notes:**

* Webhook URLs must use HTTPS.
* Custom headers (e.g., API keys) are stored encrypted.
* Publisher identity is included for audit trails.
* Webhooks are only visible to agent owners.

## Add a webhook

1. Navigate to [Settings > Fleet webhooks](https://smith.langchain.com/settings/workspaces/agent-builder-webhooks).
2. Click **Add webhook**.
3. Configure:
   * **Name**: A descriptive name (e.g., "Publish Agent", "Deploy to Production").
   * **URL**: Your HTTPS endpoint that will receive the webhook.
   * **Headers** (optional): Custom headers for authentication (stored encrypted).
   * **Form Schema** (optional): Define custom input fields users must fill when triggering.
4. Click **Save**.

## Trigger a webhook

1. Open your agent in the Fleet editor.
2. Click the **Settings** menu (gear icon).
3. Under **Webhooks**, click the webhook name.
4. Fill in any custom fields defined in the form schema.
5. Click **Run Webhook**.

## Edit a webhook

1. Navigate to [Settings > Fleet webhooks](https://smith.langchain.com/settings/workspaces/agent-builder-webhooks).
2. For the webhook you want to edit, click **Edit**.
3. Make your changes and click **Save**.

## Delete a webhook

1. Navigate to [Settings > Fleet webhooks](https://smith.langchain.com/settings/workspaces/agent-builder-webhooks).
2. For the webhook you want to delete, click **Delete**.
3. To confirm the deletion, click **Delete**.

## Webhook payload

The webhook payload is a JSON object with the following fields:

| Field | Description |
| - | - |
| `action` | The name of the webhook. |
| `input` | Values from custom form fields (empty object if no custom fields). |
| `publisher` | User ID and email of the person triggering the webhook. |
| `agent` | Agent name and description. |
| [`tool_auth_requirements`](#tool-auth-requirements) | Authentication requirements for each tool the agent uses. |
| [`files`](#zip-file-structure) | Base64-encoded ZIP containing all agent files. |
| [`fields`](#custom-input-fields) | Custom input fields. |

For example:

```json
{
  "action": "Webhook Name",
  "input": {
    "notes": "User-provided value",
    "environment": "prod",
    "dry_run": true
  },
  "publisher": {
    "user_id": "uuid-of-publishing-user",
    "email": "user@example.com"
  },
  "agent": {
    "name": "My Agent",
    "description": "Agent description text"
  },
  "tool_auth_requirements": [
    {
      "tool_name": "tavily_web_search",
      "auth_type": "api_key",
      "required_env_vars": ["TAVILY_API_KEY"]
    },
    {
      "tool_name": "google_calendar",
      "auth_type": "oauth",
      "auth_provider": "google",
      "scopes": ["calendar.readonly"]
    }
  ],
  "files": {
    "type": "zip",
    "filename": "My_Agent.zip",
    "content_base64": "<base64-encoded-zip>"
  },
  "fields": [
    {
      "name": "notes",
      "label": "Deployment Notes",
      "type": "textarea"
    }
  ]
}
```

### Tool auth requirements

The `tool_auth_requirements` array describes authentication needed for each tool:

| Auth Type | Fields | Description |
| - | - | - |
| `none` | - | Tool requires no authentication |
| `api_key` | `required_env_vars` | Tool needs API key(s) in environment variables |
| `oauth` | `auth_provider`, `scopes` | Tool requires OAuth tokens with specified scopes |

Use this information to configure your deployment environment with the necessary credentials.

### ZIP file structure

The `files.content_base64` field contains a ZIP archive with the following structure:

```
.
├── AGENTS.md           # Agent system prompt and instructions
├── config.json         # Agent metadata (name, description, visibility)
├── tools.json          # Tool configurations and interrupt settings
├── skills/             # Optional skill definitions
│   └── skill-name/
│       └── SKILL.md
└── subagents/          # Optional subagent configurations
    └── research_worker/
        ├── AGENTS.md
        └── tools.json
```

The `config.json` file and `tools.json` files are structured as follows:

> [tab] `config.json`
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "name": "My Agent",
>   "description": "Agent description",
>   "visibility_scope": "tenant",
>   "triggers_paused": false
> }
> ```

> [tab] `tools.json`
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "tools": [
>     {
>       "name": "tavily_web_search",
>       "mcp_server_url": "http://localhost:8084",
>       "mcp_server_name": "Fleet",
>       "display_name": "tavily_web_search"
>     }
>   ],
>   "interrupt_config": {
>     "http://localhost:8084::tavily_web_search::Fleet": false
>   }
> }
> ```

### Custom input fields

You can define custom input fields to collect information when the webhook is triggered. Supported field types are as follows:

| Type | Description |
| - | - |
| `string` | Single-line text input (default). |
| `number` | Numeric input. |
| `boolean` | Checkbox (true/false). |
| `textarea` | Multi-line text input. |
| `json` | JSON editor. |
| `select` | Dropdown with predefined options. |

For example:

```json
{
  "fields": [
    {
      "name": "notes",
      "label": "Deployment Notes",
      "type": "textarea"
    },
    {
      "name": "environment",
      "label": "Environment",
      "type": "select",
      "options": [
        { "label": "Development", "value": "dev" },
        { "label": "Staging", "value": "staging" },
        { "label": "Production", "value": "prod" }
      ]
    },
    {
      "name": "dry_run",
      "label": "Dry Run",
      "type": "boolean",
      "default": true
    }
  ]
}
```

## Example: Webhook server

The following is an example webhook server in Python:

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import base64
import zipfile
import io

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(content_length))

        action = body.get("action")
        input_data = body.get("input", {})
        publisher = body.get("publisher", {})
        agent = body.get("agent", {})
        tool_auth = body.get("tool_auth_requirements", [])
        files = body.get("files", {})

        print(f"Webhook: {action}")
        print(f"Publisher: {publisher.get('email')}")
        print(f"Agent: {agent.get('name')}")
        print(f"Custom Input: {input_data}")

        # Extract ZIP contents
        if files.get("content_base64"):
            zip_bytes = base64.b64decode(files["content_base64"])
            with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
                print(f"Files: {zf.namelist()}")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode())

HTTPServer(("", 8000), WebhookHandler).serve_forever()
```
