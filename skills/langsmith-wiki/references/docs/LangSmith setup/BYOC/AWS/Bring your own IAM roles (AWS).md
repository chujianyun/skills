# Bring your own IAM roles (AWS)

> Create customer-managed IAM roles for LangSmith BYOC, remove IAM management permissions from the provisioning role, and deploy with existing roles.

Bring your own IAM (BYOIAM) lets you create and manage the AWS IAM resources used by LangSmith BYOC data planes. You control the roles, policies, and permissions boundaries while LangChain provisions and operates the data plane using those resources.

If you want LangChain to manage IAM resources, follow the standard [BYOC onboarding guide](BYOC%20onboarding.md).

## Before you begin

Complete the [BYOC prerequisites](../Bring%20Your%20Own%20Cloud%20%28BYOC%29.md#prerequisites) to have a LangSmith org, with BYOC enabled.

## Create the IAM resources

The [`byoiam` Terraform module](https://github.com/langchain-ai/terraform/tree/main/modules/byoc/aws/byoiam) creates the shared data plane roles, policies, and Karpenter instance profile. Apply it once per AWS account for all regions and data planes that use these roles.

To create the IAM resources:

1. Configure the AWS provider for the account where you plan to deploy your data planes.
2. Add the module to your Terraform configuration. Set `regions` to the [supported AWS regions](../Bring%20Your%20Own%20Cloud%20%28BYOC%29.md#regions-and-cloud-providers) where the roles need to operate.
3. (Optional) Set `permissions_boundary_arn` to the ARN of your IAM permissions boundary policy. The module applies it to all roles it creates, except service-linked roles.
4. Use `service_linked_roles_to_create` to create missing service-linked roles. None are created by default. Omit existing roles, or import them into Terraform first.
5. Initialize Terraform, review the plan, and apply it in your account.

The following configuration creates shared IAM resources for two regions:

```hcl
module "byoiam" {
  source = "github.com/langchain-ai/terraform//modules/byoc/aws/byoiam?ref=main"

  regions = ["us-east-1", "us-west-1"]
}
```

### Use custom IAM names

By default, the module names its resources with a `byoc-smith-` prefix. If your organization enforces an IAM naming convention, such as a mandatory prefix, override the names with these inputs:

* **`role_names`**: A map of custom role names, keyed by role purpose. The keys match the module's `role_names` output, such as `eks-cluster-role` or `workload-iam-role`. Roles you omit keep their default names.
* **`karpenter_instance_profile_name`**: A custom name for the Karpenter node instance profile.
* **`karpenter_controller_policy_name`**: A custom name for the Karpenter controller policy.

Each role name must be unique and at most 64 characters.

```hcl
module "byoiam" {
  source = "github.com/langchain-ai/terraform//modules/byoc/aws/byoiam?ref=main"

  regions                  = ["us-east-1"]
  permissions_boundary_arn = "arn:aws:iam::<account-id>:policy/<boundary>"
  role_names = {
    eks-cluster-role                  = "ACME-langsmith-eks-cluster"
    eks-node-role                     = "ACME-langsmith-eks-node"
    ebs-csi-role                      = "ACME-langsmith-ebs-csi"
    karpenter-node-role               = "ACME-langsmith-karpenter-node"
    karpenter-controller-role         = "ACME-langsmith-karpenter-controller"
    postgres-monitoring-role          = "ACME-langsmith-postgres-monitoring"
    smithdb-metastore-monitoring-role = "ACME-langsmith-smithdb-metastore-monitoring"
    workload-iam-role                 = "ACME-langsmith-workload"
    postgres-setup-iam-role           = "ACME-langsmith-postgres-setup"
    smithdb-iam-role                  = "ACME-langsmith-smithdb"
    smithdb-setup-iam-role            = "ACME-langsmith-smithdb-setup"
    external-secrets-iam-role         = "ACME-langsmith-external-secrets"
    lbc-role                          = "ACME-langsmith-lbc"
    clickhouse-backup-iam-role        = "ACME-langsmith-clickhouse-backup"
    privatelink-lambda-role           = "ACME-langsmith-privatelink-lambda"
    juicefs-csi-iam-role              = "ACME-langsmith-juicefs-csi"
    playground-iam-role               = "ACME-langsmith-playground"
  }
  karpenter_instance_profile_name  = "ACME-langsmith-karpenter-node"
  karpenter_controller_policy_name = "ACME-langsmith-karpenter-controller"
}
```

Retain the `module.byoiam.role_names` and `module.byoiam.karpenter_instance_profile_name` outputs. You paste them into the data plane form when you [create the data plane](#deploy-the-data-plane-with-existing-roles). You do not paste the Karpenter controller policy name into LangSmith.

## Remove IAM management permissions from the provisioning role

The [`langsmith-byoc-role` Terraform module](https://github.com/langchain-ai/terraform/tree/main/modules/byoc/aws/langsmith-byoc-role) creates the cross-account role LangChain assumes to manage your data plane.

After creating the IAM resources, configure the provisioning role:

1. Copy the external ID using the button next to the **Data Planes** header in **Settings > Data Planes**. Pass it to the role module as `external_id`. The role's trust policy must use this value in its `ExternalId` condition.

2. Set `allow_iam_management_permissions = false` in your `langsmith-byoc-role` module configuration.

3. Pass the outputs of the `byoiam` module, which you applied in [Create the IAM resources](#create-the-iam-resources), to the role module:

   ```hcl
   module "langsmith_byoc_role" {
     # ... other inputs ...

     # Outputs from the byoiam module
     byoiam_role_arns                       = values(module.byoiam.role_arns)
     byoiam_instance_profile_name           = module.byoiam.karpenter_instance_profile_name
     byoiam_karpenter_controller_policy_arn = module.byoiam.karpenter_controller_policy_arn
   }
   ```

4. Review and apply the Terraform changes. Retain the `crossplane_role_arn` output for data plane creation.

The provisioning role's default permissions match only the default `byoc-smith-` names. With [custom IAM names](#use-custom-iam-names), these inputs are required. They grant read and `iam:PassRole` access on the exact ARNs. With default names, they are redundant but harmless.
Setting `allow_iam_management_permissions = false` changes the role's permissions:

* **Removed**: IAM creation, modification, and deletion permissions, including service-linked role creation.
* **Retained**: IAM read permissions, scoped `iam:PassRole`, and `iam:SimulatePrincipalPolicy` to use and validate your existing resources.

Enabling `allow_delete_permissions` does not restore IAM management permissions.

If you also want to [bring your own VPC](Bring%20your%20own%20VPC%20on%20AWS.md), set `allow_vpc_creation_permissions = false` and supply the VPC ID in `vpc_ids`.

## Deploy the data plane with existing roles

> [!WARNING]
>
> You must use the [`byoiam` Terraform module](https://github.com/langchain-ai/terraform/tree/main/modules/byoc/aws/byoiam) to create the exact IAM roles required by LangSmith. LangSmith performs extensive validation of these IAM resources before deploying the data plane.

The **Use existing IAM roles** checkbox configures the data plane to use the IAM resources you created.

To deploy the data plane:

1. Go to **Settings > Data Planes** and create a data plane.
2. Supply the name, AWS region, network configuration, and load balancer access described in [BYOC onboarding](BYOC%20onboarding.md). Choose a region included in the module's `regions` input.
3. Use the provisioning role's `crossplane_role_arn` output for the **AWS IAM role ARN**.
4. Select **Use existing IAM roles**.
5. If you set [custom IAM names](#use-custom-iam-names), paste the values of `module.byoiam.role_names` and `module.byoiam.karpenter_instance_profile_name` into the data plane form.
6. Submit the request.

Continue with provisioning and private connectivity in the onboarding guide.

## See also

* [BYOC onboarding](BYOC%20onboarding.md)
* [Bring your own VPC on AWS](Bring%20your%20own%20VPC%20on%20AWS.md)
* [BYOC shared responsibility model](../BYOC%20shared%20responsibility%20model.md)
