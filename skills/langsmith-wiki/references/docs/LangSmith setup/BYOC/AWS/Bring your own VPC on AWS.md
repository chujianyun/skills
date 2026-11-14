# Bring your own VPC on AWS

> Create a customer-managed VPC for LangSmith BYOC, configure a reduced-permission IAM role, and supply your VPC and subnet IDs.

Bring your own VPC (BYOVPC) deploys a LangSmith BYOC data plane into an existing VPC that you create and manage. It lets you control the network configuration while LangChain provisions and operates the EKS cluster, databases, storage, and other workload resources. For a VPC provisioned by LangChain, follow the standard [BYOC onboarding guide](BYOC%20onboarding.md).

You own the:

* VPC
* Subnets
* Routing
* Gateways
* VPC endpoints
* Flow logs
* Egress controls.

LangChain retains the permissions needed to manage workload security groups, the PrivateLink endpoint service for access to your data plane's EKS API, and other LangSmith infrastructure inside the VPC (such as databases).

## Before you begin

Complete the [BYOC prerequisites](../Bring%20Your%20Own%20Cloud%20%28BYOC%29.md#prerequisites) and enable BYOC on your organization. Create the VPC:

* In the same AWS account as the cross-account IAM role, and
* In the region where you plan to deploy the data plane.

## Meet the network requirements

LangSmith checks the following requirements when you supply a VPC, including one created with the reference module.

### Configure the VPC and subnets

* **Ownership and region**: The VPC and every supplied subnet must belong to the AWS account containing the IAM role, exist in the requested region, and be in the `available` state.
* **VPC configuration**: Use default instance tenancy and a primary RFC 1918 IPv4 CIDR from `/16` through `/18`. Enable both DNS support and DNS hostnames.
* **Availability zones**: Supply exactly one application subnet and one database subnet in each of two or three standard regional availability zones. If you supply public subnets, provide one in each of the same zones.
* **Subnet ranges**: Every subnet must have a private IPv4 CIDR within the VPC's primary CIDR. Supplied subnet CIDRs must not overlap.
* **Subnet IDs and tags**: Each subnet ID must be unique across all tiers.

| Subnet tier | Minimum subnet size | Minimum available IPv4 addresses per subnet |
| - | - | - |
| Private application | `/20` or larger | 256 |
| Private database | `/26` or larger | 16 |
| Public, when supplied | `/26` or larger | 16 |

Larger subnets have smaller prefix lengths. Both subnet size and available address count must meet the requirements.

### Configure routes

The VPC must have a main route table. Validation uses each subnet's explicit route table association, or the main route table if there is no explicit association.

* **Private application subnets**: Each must have an active IPv4 default route (`0.0.0.0/0`) to customer-managed egress, such as a NAT gateway or transit gateway. A direct route to an internet gateway does not satisfy this requirement.
* **Public subnets**: Each supplied public subnet must have an active IPv4 default route to an internet gateway attached to the VPC.
* **Database subnets**: The reference module keeps these isolated, without a default egress route.

### Configure network ACLs

Each supplied subnet must have an associated network ACL that permits the traffic below. Validation evaluates rules in priority order, including deny rules.

| Subnet tier | Direction | Protocol and ports | Source or destination |
| - | - | - | - |
| All supplied subnets | Inbound and outbound | TCP and UDP, ports 1–65535 | VPC primary CIDR |
| Private application | Outbound | TCP 443 | `0.0.0.0/0` |
| Private application | Inbound | TCP 1024–65535, for return traffic | `0.0.0.0/0` |
| Public | Inbound | TCP 443 | `0.0.0.0/0` |
| Public | Outbound | TCP 1024–65535, for return traffic | `0.0.0.0/0` |

These are network ACL requirements. Workload security groups and your egress controls also govern which connections succeed.

## Create the VPC with Terraform

> [!NOTE]
>
> Using the Terraform module is optional. You can create the VPC with your own tooling and use the module as a reference to meet the [network requirements](#meet-the-network-requirements).

The [`byovpc` Terraform module](https://github.com/langchain-ai/terraform/tree/main/modules/byoc/aws/byovpc) creates a network aligned with the LangSmith data plane requirements. Use it to create a VPC, or configure an existing VPC to meet the [network requirements](#meet-the-network-requirements).

To create the VPC:

1. Configure the AWS provider for your target account and [supported region](../Bring%20Your%20Own%20Cloud%20%28BYOC%29.md#regions-and-cloud-providers).
2. Add the module to your Terraform configuration. Select a private CIDR range that does not overlap with networks you plan to peer with.
3. Initialize Terraform, review the plan, and apply it in your account.

The following configuration uses the module's default subnet layout and enables AWS service endpoints, control plane PrivateLink, and flow logs:

```hcl
provider "aws" {
  region = "us-west-2"
}

module "langsmith_byovpc" {
  source = "github.com/langchain-ai/terraform//modules/byoc/aws/byovpc?ref=main"

  name           = "langsmith-production"
  vpc_cidr_block = "10.0.0.0/16"

  enable_vpc_endpoints             = true
  enable_control_plane_privatelink = true
  enable_vpc_flow_logs             = true
}

output "langsmith_network_config" {
  value = module.langsmith_byovpc.langsmith_network_config
}
```

The `langsmith_network_config` output contains the VPC ID and subnet IDs to supply when you create the data plane.

### Configure connectivity

The VPC module lets you configure:

* AWS service endpoints.
* Control plane PrivateLink and private DNS.
* VPC flow logs.
* Public subnets for internet-facing load balancers.
* NAT and internet gateways, or customer-managed centralized egress.

For configuration options and requirements, see the [`byovpc` Terraform module](https://github.com/langchain-ai/terraform/tree/main/modules/byoc/aws/byovpc).

## Create the reduced-permission IAM role

The [`langsmith-byoc-role` Terraform module](https://github.com/langchain-ai/terraform/tree/main/modules/byoc/aws/langsmith-byoc-role) creates the cross-account role LangChain assumes to manage the data plane.

To create the role:

1. Copy the external ID using the button next to the **Data Planes** header in **Settings > Data Planes**. Pass it as `external_id`. The role's trust policy must use this value in its `ExternalId` condition.
2. Set `allow_vpc_creation_permissions = false` and supply the VPC ID in the `vpc_ids` input.
3. If you require internet-facing load balancers, set `allow_public_ingress = true`. Otherwise, leave it disabled.
4. Review and apply the role module, then retain its `crossplane_role_arn` output for data plane creation.

With VPC creation permissions disabled, the role cannot create or manage the base VPC, subnets, internet and NAT gateways, Elastic IPs, route tables and routes, customer-side VPC endpoints, or VPC flow logs. It retains workload networking permissions, including tagged security groups, VPC endpoint services, and permissions needed by Karpenter. Security group creation is limited to the VPC IDs in `vpc_ids`.

## Supply the VPC and subnet IDs

When creating the data plane, supply the name, AWS region, and IAM role ARN from [onboarding](BYOC%20onboarding.md), together with the following network values:

| Value | Terraform module output | Data plane creation field |
| - | - | - |
| VPC ID | `vpc_id` | `byovpc_id` |
| Private application subnet IDs | `private_app_subnet_ids` | `byovpc_private_app_subnet_ids` |
| Private database subnet IDs | `private_db_subnet_ids` | `byovpc_private_db_subnet_ids` |
| Public subnet IDs, required for public load balancers | `public_subnet_ids` | `byovpc_public_subnet_ids` |

LangSmith validates the network before provisioning. Correct any reported network or IAM permission errors, then submit the request again. Validation checks the AWS configuration; you remain responsible for working connectivity through any custom routing, DNS, endpoint policies, and egress filters.

After creation, continue with [provisioning and private connectivity (Step 4)](BYOC%20onboarding.md).

## Maintain the network

Keep the customer-managed network available throughout the data plane's lifetime. You manage changes to routes, gateways, endpoints, DNS, network ACLs, and flow logs.

The VPC, availability zones, and private subnet configuration cannot be changed after creation. You cannot convert a data plane between a LangChain-managed VPC and BYOVPC.

Deleting a data plane removes LangChain-managed resources. Your VPC and other customer-managed network resources remain under your control and require separate cleanup after the data plane is deprovisioned.

## See also

* [BYOC onboarding](BYOC%20onboarding.md)
* [BYOC architecture](BYOC%20architecture.md)
* [BYOC shared responsibility model](../BYOC%20shared%20responsibility%20model.md)
* [BYOC FAQ](../BYOC%20FAQ.md)
