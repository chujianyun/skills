# Manage your organization using the API

LangSmith's API supports programmatic access via API key to all of the actions available in the UI, with only a few exceptions that are noted in [User-only endpoints](#user-only-endpoints).

> [!TIP]
>
> Prefer infrastructure-as-code? Use the [LangSmith Terraform provider](Manage%20LangSmith%20with%20Terraform.md) to manage workspaces, roles, members, evaluators, and alerts declaratively.

> [!TIP]
>
> Before diving into this content, it might be helpful to read the following:
>
> * [Conceptual guide on organizations and workspaces](Overview.md)
> * [Organization setup how-to guild](Workspace%20setup/Set%20up%20hierarchy.md#set-up-an-organization)

> [!NOTE]
>
> There are a few limitations that will be lifted soon:
>
> * The LangSmith SDKs do not support these organization management actions yet.
> * Organization-scoped [service keys](Overview.md#service-keys) with Organization Admin permission may be used for these actions.

> [!WARNING]
>
> Use the `X-Tenant-Id` header to specify which workspace to target. If the header is not present, operations will default to the workspace the key was initially created in if it is not organization-scoped.
>
> **If `X-Tenant-Id` is not specified when accessing workspace-scoped resources with an organization-scoped service key, the request will fail with `403 Forbidden`.**

Some commonly-used endpoints and use cases are listed below. For a complete list of available endpoints, see the [API docs](../../../Monitor/Reference/LangSmith%20REST%20API/LangSmith%20API%20reference.md). **The `X-Organization-Id` header should be present on all requests, and `X-Tenant-Id` header should be present on requests that are scoped to a particular workspace.**

## Workspaces

* [List workspaces](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/List%20workspaces.md)
* [Create workspace](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Create%20workspace.md)
* [Update workspace name](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Patch%20workspace.md)

## User management

### RBAC

* [List roles](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/List%20organization%20roles.md)
* [List permissions](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Update%20organization%20roles.md)
* [Create role](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Create%20organization%20roles.md)
* [Update role](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Update%20organization%20roles.md)

### Membership management

`List roles` under [RBAC](#rbac) should be used for retrieving role IDs of these operations. `List [organization|workspace] members` endpoints (below) response `"id"`s should be used as `identity_id` in these operations.

Organization level:

* [List active organization members](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Get%20current%20active%20org%20members.md)
* [List pending organization members](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Get%20current%20pending%20org%20members.md)
* [Invite a user to the organization and one or more workspaces](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Add%20members%20to%20current%20org%20batch.md). This should be used when the user is not already a member in the organization.
* [Update a user's organization role](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Add%20member%20to%20current%20workspace.md)
* [Remove someone from the organization](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Remove%20member%20from%20current%20org.md)

Workspace level:

* [List workspace members](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Get%20current%20workspace%20members.md)
* [Add a member to a workspace that is already part of the organization](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Add%20member%20to%20current%20workspace.md)
* [Update a user's workspace role](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Add%20member%20to%20current%20workspace.md)
* [Remove someone from a workspace](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Delete%20current%20workspace%20member.md)

> [!NOTE]
>
> These params should be omitted: `read_only` (deprecated), `password` and `full_name` ([basic auth](../Users%20%26%20access%20control/Authentication%20methods.md) only)

## API keys

For tracing-only credentials, refer to [Create, list, and delete tracing keys](../../Account/Create%20an%20account%20and%20API%20key.md#tracing-keys). Creation requires the dedicated workspace permission; organization key managers can use service-account credentials for deletion.

* [Create a service key](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Generate%20API%20key.md)
* [Update a service key role](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Update%20org%20service%20key.md)
* [Delete a service key](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Delete%20API%20key.md)

## Security settings

> [!NOTE]
>
> Organization Admin permissions are required to make these changes.

> [!NOTE]
>
> "Shared resources" in this context refer to [public prompts](../../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Create%20and%20manage%20prompts/Create%20a%20prompt.md#save-your-prompt), [shared runs](../../../Monitor/Debug/Viewing%20%26%20managing%20traces/Manage%20a%20trace.md#share-a-trace), and [shared datasets](../../../Test/Datasets%20%26%20Experiments/Datasets/Manage%20datasets.md#share-a-dataset).

> [!WARNING]
>
> Updating these settings affects **all resources in the organization**.

You can update these settings under the **Settings > Shared** tab for a workspace, or via API:

* [Update organization sharing settings](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Update%20current%20organization%20info.md)
  * use `unshare_all` to unshare **ALL** shared resources for the selected workspace - use `disable_public_sharing` to prevent future sharing of resources

These settings are only editable via API:

* [Disable/enable PAT creation](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Update%20current%20organization%20info.md) (for self-hosted, available in Helm chart version 0.11.25+)
  * Use `pat_creation_disabled` to disable PAT creation for the entire organization.
  * See the [admin guide](Overview.md#organization-roles) for information about the Organization Viewer role, which cannot create PATs.
  * For self-hosted deployments, you can also [globally disable PAT creation](../../Self-hosted/Platform%20auth%20%26%20access%20control/Customize%20user%20management.md#disabling-personal-access-token-creation) across all organizations using an environment variable.

## User-only endpoints

These endpoints are user-scoped and require a logged-in user's JWT, so they should only be executed through the UI.

* `/api-key/current` endpoints: these are related a user's PATs
* `/sso/email-verification/send` (Cloud-only): this endpoint is related to [SAML SSO](../Users%20%26%20access%20control/User%20management.md)

## Sample code

The sample code below goes through a few common workflows related to organization management. Make sure to make necessary replacements wherever `<replace_me>` is in the code.

```python
import os
import requests

def main():
    api_key = os.environ["LANGSMITH_API_KEY"]
    # LANGSMITH_ORGANIZATION_ID is not a standard environment variable in the SDK, just used for this example
    organization_id = os.environ["LANGSMITH_ORGANIZATION_ID"]
    base_url = os.environ.get("LANGSMITH_ENDPOINT")  # or "https://api.smith.langchain.com". Update appropriately for self-hosted installations or regional SaaS
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key,
        "X-Organization-Id": organization_id,
    }
    session = requests.Session()
    session.headers.update(headers)
    workspaces_path = f"{base_url}/api/v1/workspaces"
    orgs_path = f"{base_url}/api/v1/orgs/current"
    api_keys_path = f"{base_url}/api/v1/api-key"

    # Create a workspace
    workspace_res = session.post(workspaces_path, json={"display_name": "My Workspace"})
    workspace_res.raise_for_status()
    workspace = workspace_res.json()
    workspace_id = workspace["id"]
    new_workspace_headers = {
        "X-Tenant-Id": workspace_id,
    }

    # Grab roles - this includes both organization and workspace roles
    roles_res = session.get(f"{orgs_path}/roles")
    roles_res.raise_for_status()
    roles = roles_res.json()
    # system org roles are 'Organization Admin', 'Organization User'
    # system workspace roles are 'Admin', 'Editor', 'Viewer'
    org_roles_by_name = {role["display_name"]: role for role in roles if role["access_scope"] == "organization"}
    ws_roles_by_name = {role["display_name"]: role for role in roles if role["access_scope"] == "workspace"}

    # Invite a user to the org and the new workspace, as an Editor.
    # workspace_role_id is only allowed if RBAC is enabled (an enterprise feature).
    new_user_email = "<replace_me>"
    new_user_res = session.post(
        f"{orgs_path}/members",
        json={
            "email": new_user_email,
            "role_id": org_roles_by_name["Organization User"]["id"],
            "workspace_ids": [workspace_id],
            "workspace_role_id": ws_roles_by_name["Editor"]["id"],
        },
    )
    new_user_res.raise_for_status()

    # Add a user that already exists in the org to the new workspace, as a Viewer.
    # workspace_role_id is only allowed if RBAC is enabled (an enterprise feature).
    existing_user_email = "<replace_me>"
    org_members_res = session.get(f"{orgs_path}/members")
    org_members_res.raise_for_status()
    org_members = org_members_res.json()
    existing_org_member = next(
        (member for member in org_members["members"] if member["email"] == existing_user_email), None
    )
    existing_user_res = session.post(
        f"{workspaces_path}/current/members",
        json={
            "user_id": existing_org_member["user_id"],
            "workspace_ids": [workspace_id],
            "workspace_role_id": ws_roles_by_name["Viewer"]["id"],
        },
        headers=new_workspace_headers,
    )
    existing_user_res.raise_for_status()

    # List all members of the workspace
    members_res = session.get(f"{workspaces_path}/current/members", headers=new_workspace_headers)
    members_res.raise_for_status()
    members = members_res.json()
    workspace_member = next(
        (member for member in members["members"] if member["email"] == existing_user_email), None
    )

    # Update the user's workspace role to Admin (enterprise-only)
    existing_user_id = workspace_member["id"]
    update_res = session.patch(
        f"{workspaces_path}/current/members/{existing_user_id}",
        json={"role_id": ws_roles_by_name["Admin"]["id"]},
        headers=new_workspace_headers,
    )
    update_res.raise_for_status()

    # Update the user's organization role to Organization Admin
    update_res = session.patch(
        f"{orgs_path}/members/{existing_org_member['id']}",
        json={"role_id": org_roles_by_name["Organization Admin"]["id"]},
    )
    update_res.raise_for_status()

    # Create a new Service key
    api_key_res = session.post(
        api_keys_path,
        json={"description": "my key"},
        headers=new_workspace_headers,
    )
    api_key_res.raise_for_status()
    api_key_json = api_key_res.json()
    api_key = api_key_json["key"]

if __name__ == "__main__":
    main()
```
