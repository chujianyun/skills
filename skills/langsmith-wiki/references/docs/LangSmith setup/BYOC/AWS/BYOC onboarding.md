# BYOC onboarding

> Set up a LangSmith BYOC data plane, from enabling BYOC on your organization to creating workspaces and connecting privately.

This page covers BYOC on AWS. For BYOC on GCP, see [BYOC onboarding on GCP](../GCP/BYOC%20onboarding%20on%20GCP.md) or [BYOC onboarding on Azure](../Azure/BYOC%20onboarding%20on%20Azure.md).

Before you start, review the [prerequisites](../Bring%20Your%20Own%20Cloud%20%28BYOC%29.md#prerequisites).

By default, LangChain creates a VPC for your data plane. To create and manage the network yourself, follow [Bring your own VPC on AWS](Bring%20your%20own%20VPC%20on%20AWS.md) before creating the IAM role and data plane below.

**1. Enable BYOC on your organization**

Create an organization in LangSmith on AWS at [aws.smith.langchain.com](https://aws.smith.langchain.com), or reuse an existing one.

Send your organization ID to the LangChain team to enable BYOC.

**2. Create the IAM role**

LangChain provides the external ID for the IAM role. Navigate to **Settings > Data Planes** and use the copy button next to the **Data Planes** header to copy it.

Apply the [`langsmith-byoc-role` Terraform module](https://github.com/langchain-ai/terraform/tree/main/modules/byoc/aws/langsmith-byoc-role) in your AWS account using the copied external ID. This creates the cross-account role LangChain assumes to provision and manage the data plane. The role's trust policy must use this value in its `ExternalId` condition.

For BYOVPC, set `allow_vpc_creation_permissions = false` and supply your VPC ID in `vpc_ids`. See [Create the reduced-permission IAM role](Bring%20your%20own%20VPC%20on%20AWS.md#create-the-reduced-permission-iam-role).

To encrypt the data plane with your own KMS keys, also set `cmk_service_key_arns`. See [Bring your own keys](Bring%20your%20own%20keys%20%28CMK%29.md).

> [!NOTE]
>
> LangChain recommends a fresh AWS account dedicated to LangSmith BYOC.

**3. Create the data plane**

Navigate to **Settings > Data Planes** and create a data plane with the following parameters:

* **Name**: Lowercase letters, digits, and hyphens, up to 24 characters.
* **AWS region**: One of the [supported regions](../Bring%20Your%20Own%20Cloud%20%28BYOC%29.md#regions-and-cloud-providers).
* **AWS IAM role ARN**: The ARN of the role you created in the previous step, which LangSmith assumes in your account.

Under **Configuration**, the defaults work for most data planes. You can change these settings:

* **Network**: By default, LangSmith creates a VPC from a private RFC 1918 CIDR range from `/16` to `/18`, such as `10.20.0.0/16`. To use your own VPC, select **Use existing VPC** and supply the [VPC and subnet IDs](Bring%20your%20own%20VPC%20on%20AWS.md#supply-the-vpc-and-subnet-ids). The load balancer is **Private** by default, reachable only from inside your VPC. Select **Internet-facing** to give your applications a public endpoint. With your own VPC, an internet-facing load balancer requires public subnet IDs.
* **IAM roles**: By default, LangSmith creates the data plane IAM roles. To use roles you create, select **Use existing IAM roles** and follow [Bring your own IAM roles](Bring%20your%20own%20IAM%20roles%20%28AWS%29.md).
* **Encryption keys**: By default, AWS-managed keys encrypt data at rest. To use your own KMS keys, choose one key for all services or a key per service. See [Bring your own keys](Bring%20your%20own%20keys%20%28CMK%29.md).
* **Sandboxes**: Off by default. Turn them on to run [sandboxes](../../../Deploy/Sandboxes/LangSmith%20Sandboxes.md), which Engine and some evaluators require.
* **EKS API access**: New data planes reach the EKS API over PrivateLink by default.
* **Tags**: Up to 40 custom tags applied to the AWS resources LangSmith creates. Keys must be unique, and values can be empty. AWS and LangSmith system tags are reserved.

**4. Wait for provisioning**

LangChain provisions the infrastructure on your behalf. The data plane moves from `Requested` to `Provisioning` to `Active`.

For BYOVPC, LangSmith validates your VPC and subnets before provisioning, then creates the workload infrastructure inside your VPC.

> [!NOTE]
>
> End-to-end provisioning of a data plane takes around 60 to 90 minutes.

Track its state in **Settings > Data Planes**. If the data plane transitions to `Provisioning Failed`, contact the LangChain team.

**5. Set up private connectivity**

Data planes are provisioned with a private endpoint by default, so you need private connectivity to reach it, such as Tailscale, AWS PrivateLink, or VPC peering.

Find the API URL under **Settings > Data Planes**.

If you open a workspace and see the following screen, your machine does not have network access to that workspace's data plane. The LangSmith frontend runs in your browser and calls the data plane directly, so your machine must be on a network that can reach the data plane's private endpoint. Connect through your private connectivity option, then refresh the page.

![LangSmith error screen titled You may not have network access to this workspace. It states that LangSmith cannot reach the data plane for the selected workspace and lists other workspaces grouped by data plane. Reachable data planes show a green header with active Switch buttons. The unreachable data plane shows a red header with disabled Switch buttons.](../../../../assets/images/4c9d91cb2a75-byoc-data-plane-unreachable.png)

From this screen, you can switch to a workspace on a data plane that is reachable, which can be a Cloud workspace.

**6. Create workspaces**

A workspace named `dp-<data_plane_name>` is provisioned automatically inside the new data plane. It is not accessible until the data plane is reachable.

You can create additional workspaces in the data plane. Select the target data plane when you create each one: a workspace belongs to exactly one data plane, and a data plane can hold many workspaces.

> [!WARNING]
>
> Pick the correct data plane carefully when you create a workspace. A workspace cannot be moved to another data plane after creation.

**7. (Optional) Migrate existing data**

If you are moving from an existing LangSmith Cloud or [self-hosted](../../Self-hosted/Self-hosted%20LangSmith.md) instance, users, roles, datasets, prompts, experiments, annotation queue configuration, automation rules, dashboards, and Fleet resources can be copied over. Trace migration is supported on AWS. Contact the LangChain team to arrange it.

For more information, see [Migrate to BYOC](../Migrate%20to%20BYOC.md).

## Next steps

* [Use your data plane](../BYOC%20usage.md) to point applications and API clients at the right endpoint.
* [BYOC architecture](BYOC%20architecture.md) covers what LangChain provisions and how the planes communicate.
