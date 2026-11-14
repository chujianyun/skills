# BYOC onboarding on Azure

> Set up a LangSmith BYOC data plane in your Azure subscription, from granting LangSmith access to a resource group to creating, changing, and deleting the data plane.

> [!NOTE]
>
> BYOC on Azure is in **[beta](../../Cloud/Reference/Release%20stages.md)**. To get started, [contact our sales team](https://www.langchain.com/contact-sales).

This page describes how to create a LangSmith BYOC data plane in your Azure subscription. For how the data plane is built and secured, see [BYOC architecture on Azure](BYOC%20architecture%20on%20Azure.md). For the AWS guide, see [BYOC onboarding](../AWS/BYOC%20onboarding.md).

Each data plane runs in its own resource group in your subscription. A Terraform module creates the resource group and a Key Vault in it, and gives the LangSmith BYOC application roles on that resource group only. LangChain then creates and operates the data plane resources in the resource group.

## Before you start

You need the following:

* **A LangSmith organization on Azure**: Use the LangSmith control plane on Azure at [azure.smith.langchain.com](https://azure.smith.langchain.com). Send your organization ID to the LangChain team to enable BYOC.
* **An Azure subscription**: LangChain recommends a subscription dedicated to LangSmith BYOC, but it is not required.
* **Azure permissions**: The person who applies Terraform needs the `Owner` role on the subscription, because the Terraform module creates custom roles and role assignments and registers resource providers. You also need a Microsoft Entra role that can create and update the service principal of a multi-tenant application in your tenant, such as `Cloud Application Administrator`.
* **Terraform**: Terraform 1.11.0 or later.
* **An organization admin in LangSmith**: Creating, changing, and deleting a data plane requires the organization admin role.
* **vCPU quota**: The AKS system node pool uses three `Standard_D2s_v6` VMs. LangSmith checks at create time that the region has at least 6 free vCPUs in both the **Total Regional vCPUs** quota and the Dsv6 VM family quota. Application nodes use D, E, and F series VMs of version 5 or later, so also plan quota for those families. See [Node pools](BYOC%20architecture%20on%20Azure.md#compute).
* **A region**: BYOC on Azure can run in any Azure region. If you need a region that is not yet enabled, contact the LangChain team, who can add it.

## Create a data plane

**1. Copy the external ID**

LangChain assigns your organization an external ID. Navigate to **Settings > Data Planes** in LangSmith and use the copy button next to the **Data Planes** header to copy it. Do not create your own value.

LangSmith uses the external ID to confirm that the role assignments in your subscription belong to your organization.

**2. Grant LangSmith access with Terraform**

Apply the [`langsmith-byoc-access` Terraform module](https://github.com/langchain-ai/terraform/blob/main/modules/byoc/azure/langsmith-byoc-access/main.tf) in your Azure subscription with the external ID you copied. You must use this module. For each data plane in its `data_planes` input, it creates:

* **The LangSmith BYOC service principal**: The service principal of the LangSmith BYOC multi-tenant application, with application (client) ID `5b0a74cb-9f37-4797-b557-c15d7be80d3b`, in your Microsoft Entra tenant. It is created once per tenant, and the application requests no Microsoft Graph permissions.
* **A dedicated resource group**, `langsmith-byoc-<key>`: LangSmith deploys the data plane into it. Do not put other workloads in it.
* **A Key Vault in the resource group**: It uses Azure RBAC authorization and has public network access disabled. LangSmith writes the data plane's bootstrap secret to it, and the data plane reads it through a private endpoint.
* **Two role assignments for the service principal on the resource group**: A `langsmith-byoc-<key>-<suffix>` custom role with the actions LangSmith needs, and `User Access Administrator`. Both roles can only be used in that resource group, and both assignments carry your external ID as their description.

```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 4.42.0, < 5.0.0"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  subscription_id = "<subscription-id>"
  features {}

  # The data plane needs these resource providers. LangSmith cannot
  # register them, because its roles stop at the resource group.
  resource_providers_to_register = [
    "Microsoft.Cache",
    "Microsoft.Compute",
    "Microsoft.ContainerService",
    "Microsoft.DBforPostgreSQL",
    "Microsoft.KeyVault",
    "Microsoft.ManagedIdentity",
    "Microsoft.Network",
    "Microsoft.Storage",
  ]
}

provider "azuread" {}

variable "external_id" {
  description = "The external ID from Settings > Data Planes in LangSmith."
  type        = string
}

module "langsmith_byoc_access" {
  source = "github.com/langchain-ai/terraform//modules/byoc/azure/langsmith-byoc-access?ref=main"

  langsmith_app_client_id = "5b0a74cb-9f37-4797-b557-c15d7be80d3b"
  external_id             = var.external_id

  data_planes = {
    prod = {
      location = "eastus"
    }
  }
}

output "langsmith_byoc_access" {
  value = module.langsmith_byoc_access
}
```

Replace the subscription ID and the region. The `data_planes` key (`prod` in the example) names the resource group: 1 to 63 lowercase letters, digits, and hyphens, starting with a letter and ending with a letter or digit, with no consecutive hyphens. Apply the configuration with your external ID, for example `terraform apply -var 'external_id=<external-id>'`.

Then read the outputs for the next step:

```bash
terraform output -json langsmith_byoc_access
```

You need `azure_entra_tenant_id`, and the `region` and `resource_group_id` of the data plane under `data_planes`.

For what each role allows, see [Access and permissions](BYOC%20architecture%20on%20Azure.md#access-and-permissions). For all module inputs, see the [module README](https://github.com/langchain-ai/terraform/tree/main/modules/byoc/azure/langsmith-byoc-access).

**3. Create the data plane**

1. In [LangSmith on Azure](https://azure.smith.langchain.com), go to **Settings > Data Planes** and click **+ Data Plane**.

2. Fill in the **Create a data plane** form using the Terraform outputs from the previous step:

   | Field | Description |
   | - | - |
   | **Name** | Up to 24 lowercase letters, digits, and hyphens. Starts and ends with a letter or digit, and does not start with `internal`. For example, `prod`. |
   | **Azure region** | Select the region of the resource group. |
   | **Microsoft Entra tenant ID** | Use the `azure_entra_tenant_id` output, in `8-4-4-4-12` UUID form. |
   | **Azure resource group ID** | Use the `resource_group_id` output, in the form `/subscriptions/<subscription-id>/resourceGroups/<name>`. Each resource group serves one data plane. |
   | **Use existing managed identities** | Select this only if you set `byo_iam = true` for this data plane in the module's `data_planes` input, so that Terraform creates the identities and their role assignments. Set `byo_iam` before you create the data plane, because it cannot change later. See [Bring your own identities](https://github.com/langchain-ai/terraform/tree/main/modules/byoc/azure/langsmith-byoc-access#bring-your-own-identities-optional). Otherwise, leave it cleared. |
   | **VNet CIDR Range** | The address range of the VNet that LangSmith creates for the data plane. Use a private RFC 1918 range from `/16` to `/18` that does not overlap your other networks. |
   | **Load balancer access** | Leave on **Private**, the default, for access from the data plane VNet and connected networks only. Switch to **Public** for an internet-facing endpoint. |

3. Click **Create data plane**. LangSmith confirms with **Data plane requested**.

Before LangSmith accepts the request, it checks that:

* The role assignments of the LangSmith service principal on the resource group have your external ID as their description.
* The service principal has the permissions it needs on the resource group.
* The resource group contains exactly one Key Vault, and the vault uses Azure RBAC.
* Your subscription can create the AKS system node size and the PostgreSQL size in the region, and has enough vCPU quota for the system node pool.

If a check fails, the form shows the error. Fix the problem and click **Create data plane** again. See [Troubleshoot data plane creation](#troubleshoot-data-plane-creation).

**4. Wait for provisioning**

LangChain provisions the data plane resources in your resource group. The data plane moves from `requested` to `provisioning` to `active`. Track its state in **Settings > Data Planes**.

If the data plane does not become active within 3 hours, it moves to `provisioning_failed`. If that happens, contact the LangChain team.

**5. Connect to the data plane**

The data plane URL has the form `https://<data_plane_id>.azure.langchain-byoc.com`. Find it under **Settings > Data Planes**.

* **Internal load balancer** (`public_load_balancer: false`): Users and applications reach the data plane only from its VNet. Connect your network to that VNet, for example with VNet peering or a VPN gateway. Configure DNS resolution from your network to the VNet-linked private DNS zone. Peering or a VPN alone does not provide DNS resolution.
* **Public load balancer** (`public_load_balancer: true`): Users and applications reach the data plane over the internet.

If the LangSmith UI cannot reach your data plane, it prompts you to switch to a workspace on a data plane that is reachable.

**6. Create workspaces**

A workspace named `dp-<data_plane_name>` is created automatically in the new data plane. It is not accessible until the data plane is reachable.

You can create more workspaces in the data plane. Select the target data plane when you create each one: a workspace belongs to exactly one data plane, and a data plane can hold many workspaces.

> [!WARNING]
>
> A workspace cannot be moved to another data plane after creation.

**7. (Optional) Migrate existing data**

If you are moving from LangSmith Cloud or a [self-hosted](../../Self-hosted/Self-hosted%20LangSmith.md) instance, contact the LangChain team to arrange a migration. Trace migration is supported on AWS only.

For more information, see [Migrate to BYOC](../Migrate%20to%20BYOC.md).

To send traces and API requests to the data plane, see [BYOC usage](../BYOC%20usage.md).

## Troubleshoot data plane creation

| Code | HTTP status | Cause | Fix |
| - | - | - | - |
| `azure_external_id_mismatch` | 403 | A role assignment of the LangSmith service principal on the resource group does not have your organization's external ID as its description. | Apply the Terraform module with the external ID from **Settings > Data Planes**, then retry. |
| `azure_permissions` | 403 | The LangSmith service principal cannot access the resource group, or lacks a required permission. The remedy lists the missing actions. | Check that the resource group exists and that you applied the Terraform module without `reduced_access`, then retry. |
| `azure_policy_denied` | 403 | An Azure Policy assignment in your subscription denied a request. | Exempt the data plane resource group from the policy, then retry. |
| `azure_resource_group_invalid` | 400 | The resource group does not exist, does not contain exactly one Key Vault, or its vault does not use Azure RBAC. | Fix the resource group, then retry. |
| `azure_region_unavailable` | 400 | Your subscription cannot use the region, or cannot create the AKS system node size or the PostgreSQL size in it. | Choose another region, or ask Azure support to enable the VM size or PostgreSQL for your subscription in the region. |
| `insufficient_azure_quota` | 422 | The region does not have enough free vCPU quota for the AKS system node pool. | Request a quota increase, or choose another region. |
| `azure_resource_group_in_use` | 409 | Another data plane uses the resource group. | Create a new resource group for the data plane. |
| `data_plane_name_taken` | 409 | Your organization already has a data plane with this name. | Choose another name. |
| `azure_throttled` | 429 | Azure is rate limiting requests for your subscription. | Wait a minute, then retry. |
| `azure_unavailable` | 502 or 503 | Azure returned a server error, or did not report the vCPU quota. | Wait a minute, then retry. |

Invalid field values return HTTP 400 with the field name and the rule that the value breaks.

## Change data plane settings

The settings form in the LangSmith UI supports AWS maintenance windows only. To change the maintenance window of an Azure data plane, use the [Update data plane settings](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Update%20data%20plane%20settings.md) API:

```bash
curl -X PATCH 'https://azure.api.smith.langchain.com/orgs/current/data-planes/<data-plane-id>' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: <api-key>' \
  -H 'X-Organization-Id: <organization-id>' \
  -d '{"maintenance_window": "sun:07:00-sun:11:00"}'
```

You can change the following settings of an Azure data plane while it is `provisioning` or `active`:

| Setting | Field | Azure |
| - | - | - |
| Maintenance window | `maintenance_window` | A weekly UTC window of exactly 4 hours that starts on the hour, in the form `ddd:HH:00-ddd:HH:00`. The default is `sun:07:00-sun:11:00`. AKS upgrades and PostgreSQL maintenance happen in this window. |
| Trace payload retention | `ttl` | Supported. By default, `short_days` is 14 and `long_days` is 400. |
| Network firewall | `firewall` | Not available on Azure. |
| Fleet OIDC | `fleet_oidc` | Not available on Azure. |

## Reduce access after deployment

Once the data plane is `active`, you can reduce the permissions of its `langsmith-byoc-<key>-<suffix>` custom role. Set `reduced_access = true` for the data plane in the Terraform module and run `terraform apply`:

```hcl
data_planes = {
  prod = {
    location       = "eastus"
    reduced_access = true
  }
}
```

Terraform updates the custom role actions in place and deletes the `User Access Administrator` assignment. The custom role assignment stays, so LangSmith keeps access. Azure applies the change in up to 5 minutes. With the reduced role, LangChain can still upgrade, scale, and repair the data plane, but cannot delete the data plane, its databases, its storage accounts, or its network, and cannot create role assignments. Set `reduced_access` back to `false` before an upgrade that adds a role assignment, and before you delete or re-create the data plane.

## Delete a data plane

> [!WARNING]
>
> Do not remove the data plane from the Terraform module before you delete it in LangSmith. LangSmith needs its role assignments to delete the data plane resources.

1. If the data plane has `reduced_access = true`, set it to `false`, run `terraform apply`, and wait 5 minutes for Azure to apply the role change.
2. Delete the data plane in **Settings > Data Planes**, or with the `DELETE /orgs/current/data-planes/<data-plane-id>` API. You can delete an Azure data plane while it is `provisioning`, `active`, or `provisioning_failed`. LangSmith first checks that it can still access your resource group.
3. Wait until the data plane is gone from **Settings > Data Planes**.

LangSmith deletes the AKS cluster, PostgreSQL, Redis, the network, and the private DNS zones. It keeps the following in your resource group:

* The resource group and the Key Vault.
* The Blob storage accounts that hold your trace data and SmithDB data.

Azure keeps the backups of a deleted PostgreSQL server for a limited time, during which you can restore it. See [Restore a dropped Azure Database for PostgreSQL flexible server](https://learn.microsoft.com/azure/postgresql/flexible-server/how-to-restore-dropped-server).

If you create a new data plane with the same name in the same resource group, it reuses the Key Vault and the retained Blob storage accounts.

When you no longer need the retained data, delete the Blob storage accounts in the resource group, then remove the data plane's key from `data_planes` and run `terraform apply`. Terraform then deletes the resource group, the Key Vault, and the role assignments. With the default `features {}` block, the AzureRM provider refuses to delete a resource group that still contains resources Terraform does not manage, such as the retained storage accounts.

## Remove LangSmith access

To stop LangSmith from changing or deleting a data plane, remove the role assignments of the LangSmith service principal on its resource group and on its AKS cluster. Removing the Terraform module removes the service principal and all role assignments, so LangSmith loses access to every data plane in the tenant. The data plane resources stay in your subscription, and LangChain can no longer upgrade or repair them. Delete the data plane first if you want LangSmith to clean up its resources.

## Next steps

* [BYOC architecture on Azure](BYOC%20architecture%20on%20Azure.md) covers the resources in your subscription, the network paths, and how LangSmith accesses them.
* [BYOC usage](../BYOC%20usage.md) covers how to point applications and API clients at the data plane.
