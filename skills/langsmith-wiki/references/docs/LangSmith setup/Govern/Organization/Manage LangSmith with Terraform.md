# Manage LangSmith with Terraform

> Use the official LangSmith Terraform provider to manage workspaces, access controls, resource tags, evaluators, run rules, and alert rules as code.

The official [LangSmith Terraform provider](https://registry.terraform.io/providers/langchain-ai/langsmith/latest) lets you manage LangSmith organization and workspace resources as code: workspaces, custom roles, organization and workspace members, resource tags, access policies, evaluators, run rules, and alert rules. It is the infrastructure-as-code counterpart to [managing your organization using the API](Manage%20your%20organization%20using%20the%20API.md).

> [!NOTE]
>
> Managing resource tags and access policies requires LangSmith Terraform provider v0.0.6 or later.

> [!TIP]
>
> Before diving in, it might be helpful to read:
>
> * [Conceptual guide on organizations and workspaces](Overview.md)
> * [Organization setup how-to](Workspace%20setup/Set%20up%20hierarchy.md#set-up-an-organization)

## Install and configure

Add the provider to your Terraform configuration and pin a version:

```hcl
terraform {
  required_providers {
    langsmith = {
      source  = "langchain-ai/langsmith"
      version = "~> 0.0.6"
    }
  }
}

provider "langsmith" {
  # Cloud (US). Use https://eu.api.smith.langchain.com for the EU region,
  # or your self-hosted URL. Can also be set via LANGSMITH_ENDPOINT.
  api_url = "https://api.smith.langchain.com"

  # Optional: scope workspace-level resources to a specific workspace.
  workspace_id = "00000000-0000-0000-0000-000000000000"
}
```

Then run `terraform init` to download the provider.

## Authentication

The provider resolves credentials the same way as the LangSmith SDK and CLI. Prefer environment variables or a profile over hardcoding `api_key`:

* **Environment**—`LANGSMITH_API_KEY`, `LANGSMITH_ENDPOINT` (API URL), `LANGSMITH_WORKSPACE_ID`.
* **Profile**—set `profile` (or `LANGSMITH_PROFILE`) to use a LangSmith CLI profile.
* **Provider arguments**—`api_key`, `api_url`, `workspace_id`, `profile`.

Create an API key or [service key](Overview.md#service-keys) in your LangSmith settings. See [Authentication methods](../Users%20%26%20access%20control/Authentication%20methods.md) for the available key types.

> [!WARNING]
>
> Organization-scoped operations, like creating workspaces, inviting organization members, and managing access policies, require an **organization-scoped service key with Organization Admin permissions**. Set `workspace_id` (or `LANGSMITH_WORKSPACE_ID`) to target workspace-scoped resources such as workspace memberships, resource tags, evaluators, and run rules.

## Examples

### Create a workspace

```hcl
resource "langsmith_workspace" "demo" {
  display_name  = "Demo Workspace"
  tenant_handle = "demo-workspace"
}
```

### Manage roles and members

Look up built-in roles with data sources, then assign them. This invites a user to the organization and grants them admin on the workspace:

```hcl
data "langsmith_org_role" "user" {
  name = "ORGANIZATION_USER"
}

data "langsmith_workspace_role" "admin" {
  name = "WORKSPACE_ADMIN"
}

resource "langsmith_org_membership" "alice" {
  email   = "alice@example.com"
  role_id = data.langsmith_org_role.user.id
}

resource "langsmith_workspace_membership" "alice_demo" {
  workspace_id = langsmith_workspace.demo.id
  email        = langsmith_org_membership.alice.email
  role_id      = data.langsmith_workspace_role.admin.id
}
```

You can also define a custom workspace role, for example by cloning an existing role's permissions:

```hcl
resource "langsmith_workspace_role" "issues_agent" {
  display_name = "Issues Agent"
  description  = data.langsmith_workspace_role.admin.description
  permissions  = data.langsmith_workspace_role.admin.permissions
}
```

### Manage resource tags and access policies

Use [resource tags](Workspace%20setup/Set%20up%20resource%20tags.md) to organize workspace resources and apply [attribute-based access control (ABAC)](../Users%20%26%20access%20control/Attribute-based%20access%20control.md). The `langsmith_tag` convenience resource owns one tag key and one value. Use the independent `langsmith_tag_key` and `langsmith_tag_value` resources when keys or values are shared across configurations.

The following configuration creates an `Environment=production` tag, applies it to a tracing project, and limits a workspace role to production projects:

```hcl
resource "langsmith_tag" "production" {
  key               = "Environment"
  value             = "production"
  key_description   = "Deployment environment"
  value_description = "Production workloads"
}

resource "langsmith_tagging" "production_project" {
  tag_value_id  = langsmith_tag.production.tag_value_id
  resource_type = "project"
  resource_id   = "00000000-0000-0000-0000-000000000000" # tracing project ID
}

resource "langsmith_workspace_role" "production_reader" {
  display_name = "Production Reader"
  description  = "Can read production projects"
  permissions  = ["projects:read"]
}

resource "langsmith_access_policy" "production_readers" {
  name        = "Production readers"
  description = "Read access to production projects"
  effect      = "allow"

  condition_groups = [{
    permission    = "projects:read"
    resource_type = "project"
    conditions = [{
      attribute_name  = "resource_tag_key"
      attribute_key   = "Environment"
      operator        = "equals"
      attribute_value = "production"
    }]
  }]
}

resource "langsmith_access_policy_attachment" "production_reader" {
  role_id          = langsmith_workspace_role.production_reader.id
  access_policy_id = langsmith_access_policy.production_readers.id
}
```

### Automate evaluators, run rules, and alerts

The provider manages more than accounts. You can codify [online code evaluators](../../../Monitor/Observe/Online%20evaluators/Set%20up%20online%20code%20evaluators.md), the [run rules](../../../Monitor/Observe/Automations/Set%20up%20automation%20rules.md) that apply them, and [alerts](../../../Monitor/Observe/Monitoring%20%26%20alerting/Alerts%20in%20LangSmith.md) alongside your workspaces:

```hcl
resource "langsmith_evaluator" "tool_calls" {
  workspace_id = langsmith_workspace.demo.id
  name         = "tool call counts"
  type         = "code"

  code_evaluator = {
    language = "javascript"
    code     = file("${path.module}/evaluator.js")
  }
}

# A run rule applies the evaluator to matching runs in a tracing project.
# Run rules can also add runs to a dataset or annotation queue, or call webhooks.
resource "langsmith_run_rule" "score_root_runs" {
  workspace_id  = langsmith_workspace.demo.id
  display_name  = "score root runs"
  session_id    = "00000000-0000-0000-0000-000000000000" # tracing project ID
  sampling_rate = 1
  filter        = "eq(is_root, true)"

  evaluator_id = langsmith_evaluator.tool_calls.id
}

resource "langsmith_alert_rule" "error_rate" {
  session_id     = "00000000-0000-0000-0000-000000000000" # tracing project ID
  name           = "run error count high"
  type           = "threshold"
  attribute      = "error_count"
  aggregation    = "sum"
  window_minutes = 15
  operator       = "gte"
  threshold      = 10
  filter         = "eq(is_root, true)"

  actions = [{
    target  = "webhook"
    url_env = "LANGSMITH_ALERTS_WEBHOOK_URL"
    config_json = jsonencode({
      body = jsonencode({ text = "Error rate elevated" })
    })
  }]
}
```

## Resource reference

The full list of resources and data sources—with every argument and attribute—is published and kept in sync on the Terraform Registry:

> [card] [LangSmith provider on the Terraform Registry](https://registry.terraform.io/providers/langchain-ai/langsmith/latest/docs)
>
> Browse the complete reference for all resources and data sources.
