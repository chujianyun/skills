# BYOC FAQ

> Answers to common questions about LangSmith BYOC, covering data residency, access, setup, the data plane model, and ongoing operations.

## Setup

> [accordion] Which clouds and regions can I deploy to?
>
> BYOC is generally available (GA) on AWS with a US control plane. BYOC on GCP and Azure is available in [beta](../Cloud/Reference/Release%20stages.md). See [Regions and cloud providers](Bring%20Your%20Own%20Cloud%20%28BYOC%29.md#regions-and-cloud-providers) for the supported AWS regions and GCP and Azure region availability.

> [accordion] Does BYOC support government cloud regions or FIPS-compliant images?
>
> No. BYOC does not support government cloud regions, such as AWS GovCloud (US), and does not provide FIPS-compliant container images.

> [accordion] Can a control plane on one cloud manage a data plane on another cloud?
>
> No. Cross-cloud deployments are not supported. A data plane must run on the same cloud provider as its control plane. For example, the AWS control plane cannot manage a data plane on GCP.
>
> Each cloud provider has its own LangSmith instance, with separate users and organizations. To deploy data planes on more than one cloud provider, create a LangSmith organization on each provider's instance. See [Regions and cloud providers](Bring%20Your%20Own%20Cloud%20%28BYOC%29.md#regions-and-cloud-providers) for the instance URLs.

> [accordion] Do I need a dedicated AWS account?
>
> No. LangChain recommends a fresh account for clearer billing, and because some permissions cannot be scoped to specific resources, but it is not required.

> [accordion] Can I install BYOC into an existing VPC?
>
> Yes. With [Bring your own VPC (BYOVPC)](AWS/Bring%20your%20own%20VPC%20on%20AWS.md), you supply a VPC and subnets. You can create the VPC with the [reference Terraform module](https://github.com/langchain-ai/terraform/tree/main/modules/byoc/aws/byovpc) or use an existing VPC that meets the network requirements.
>
> To remove VPC creation permissions from the customer role, set `allow_vpc_creation_permissions = false` in the [`langsmith-byoc-role` Terraform module](https://github.com/langchain-ai/terraform/tree/main/modules/byoc/aws/langsmith-byoc-role) and include your VPC ID in `vpc_ids`.

> [accordion] Can I deploy multiple data planes in the same VPC?
>
> Yes. Deploying multiple data planes in the same VPC requires [Bring your own VPC (BYOVPC)](AWS/Bring%20your%20own%20VPC%20on%20AWS.md). Each data plane must use different subnets. Do not share subnets between data planes.

> [accordion] Can I move an existing data plane into my own VPC?
>
> No. Moving an existing data plane to a different VPC is not supported, nor is changing its VPC and subnet configuration after creation.

> [accordion] Can I install BYOC into an existing EKS cluster?
>
> No, and there are no plans to support it. LangChain operates the cluster on your behalf, including upgrades and patching, and a dedicated cluster is what makes managing it reliably possible.

> [accordion] Can I run my own workloads in the LangSmith VPC or cluster?
>
> Yes, as long as they do not interfere with the functioning of LangSmith.
>
> In the AWS account, keep in mind that some permissions granted to the cross-account role cannot be scoped by tag, which is why LangChain recommends a dedicated account.
>
> In the Kubernetes cluster, passive workloads that do not interfere with LangSmith are fine, such as observability and security monitoring agents. When you deploy them:
>
> * Use your own node groups and tolerations rather than the ones LangSmith runs on.
> * Deploy into namespaces other than the ones LangSmith uses.
> * Do not edit the resources LangChain provisions.
>
> LangChain is not responsible for downtime or issues caused by interfering workloads.

> [accordion] What value do I set to the external ID for my role?
>
> LangChain provides the external ID. Navigate to **Settings > Data Planes** and use the copy button next to the **Data Planes** header to copy it. Use this value when applying the `langsmith-byoc-role` Terraform module. The role's trust policy must use this value in its `ExternalId` condition.

> [accordion] How long does provisioning take?
>
> End-to-end provisioning of a data plane takes around 60 to 90 minutes. Provisioning time can vary, because AWS resource provisioning is inconsistent.

> [accordion] What happens if provisioning fails?
>
> The data plane transitions to `Provisioning Failed`. Failures are usually caused by missing permissions on the cross-account role, or by a service control policy (SCP) that blocks an action LangChain needs to take.
>
> Apply the [`langsmith-byoc-role` Terraform module](https://github.com/langchain-ai/terraform/tree/main/modules/byoc/aws/langsmith-byoc-role) exactly as published, with no edits or changes. A modified module is a common source of missing permissions.
>
> Contact the LangChain team. Once the permissions are corrected, provisioning reconciles automatically.

> [accordion] What VPC CIDR range should I use?
>
> A private RFC 1918 range between `/18` and `/16`. If you plan to use VPC peering, select a range that does not overlap with the VPC you intend to peer with. The CIDR range cannot be changed after provisioning.

> [accordion] How do I reach a data plane with a private endpoint?
>
> Data planes are provisioned with a private endpoint by default, so you need private connectivity such as Tailscale, AWS PrivateLink, or VPC peering.

> [accordion] Why does LangSmith say I may not have network access to this workspace?
>
> Your machine cannot reach the data plane that holds the workspace. After the browser loads the LangSmith UI, it sends data requests directly to your data plane. With a private endpoint, those requests succeed only from a network that can reach your VPC.
>
> ![LangSmith error screen titled You may not have network access to this workspace. It states that LangSmith cannot reach the data plane for the selected workspace and lists other workspaces grouped by data plane. Reachable data planes show a green header with active Switch buttons. The unreachable data plane shows a red header with disabled Switch buttons.](../../../assets/images/4c9d91cb2a75-byoc-data-plane-unreachable.png)
>
> The screen groups your workspaces by data plane. A green header marks a data plane your browser can reach, and a red header marks one it cannot.
>
> To fix it:
>
> 1. Connect to the network that has private connectivity to the data plane. If your organization uses a corporate VPN, ask your IT team to route the data plane's endpoint through it.
> 2. Refresh the page.
>
> To keep working in the meantime, select **Switch** next to a workspace on a reachable data plane. For more information, see [BYOC onboarding](AWS/BYOC%20onboarding.md) and [BYOC architecture](AWS/BYOC%20architecture.md).

> [accordion] Are my service endpoints exposed to the internet?
>
> No. Services sit behind a private load balancer by default, reachable only from inside your VPC or through the private connectivity you configure.
>
> Data plane endpoints can be made public at provisioning time. See [Onboarding](AWS/BYOC%20onboarding.md).

> [accordion] Can I use my own DNS domain?
>
> No. Data planes are provisioned under the standard LangChain BYOC domain. Find your data plane API URL under **Settings > Data Planes**.

> [accordion] How do I decommission a data plane?
>
> Re-apply the [`langsmith-byoc-role` Terraform module](https://github.com/langchain-ai/terraform/tree/main/modules/byoc/aws/langsmith-byoc-role) with `allow_delete_permissions = true`, which grants the permissions needed to delete LangSmith-managed resources.
>
> Then select **Delete Data Plane** in the LangSmith UI. LangChain deprovisions the infrastructure in your account.

## Data and security

> [accordion] Does sensitive data ever leave my VPC?
>
> No. When a user opens `aws.smith.langchain.com`, the browser fetches the LangSmith UI bundle from LangChain's cloud. Once loaded, the application routes every request for sensitive data to your VPC.
>
> See [Data traffic](AWS/BYOC%20architecture.md#data-traffic).

> [accordion] What can the LangChain team do in my account?
>
> LangChain can manage the infrastructure of the resources LangSmith created, and nothing else. Permissions are scoped by the `managed_by=langsmith` tag, so the role cannot act on unrelated resources in your account.
>
> The role holds no permissions that grant data access. See [How least privilege is enforced](AWS/BYOC%20architecture.md#how-least-privilege-is-enforced).

> [accordion] Can LangChain read my traces or database contents?
>
> No. The cross-account role is infrastructure-scoped rather than data-scoped. It can manage the resources that hold your data, but holds no `s3:GetObject` on the trace bucket, no `rds-db:connect` to PostgreSQL, and no `elasticache:Connect` to Redis.
>
> Access to the data itself requires you to explicitly grant it, such as during an incident. See [How least privilege is enforced](AWS/BYOC%20architecture.md#how-least-privilege-is-enforced).

> [accordion] What access do LangChain employees have to my environment and data?
>
> There is no standing data access. If an incident requires access to your data, LangChain either asks you to run the queries yourself, or requests break-glass access.

> [accordion] Does LangSmith support customer-managed encryption keys?
>
> Yes, on AWS. When you create a data plane, you can encrypt its S3 buckets, EBS volumes, EKS secrets, RDS databases, and ElastiCache with your own AWS KMS keys. See [Bring your own keys](AWS/Bring%20your%20own%20keys%20%28CMK%29.md). By default, data is encrypted at rest with cloud provider-managed keys.

> [accordion] How do I revoke LangChain's access?
>
> You create and own the cross-account role in your own account, so you can revoke access without involving LangChain. Removing the role, or its trust relationship with the LangChain account, stops the control plane from assuming it, and stops reconciliation of data plane resources.

> [accordion] Can I revoke individual permissions granted during provisioning?
>
> Yes, but the role needs its permissions for continuous reconciliation of the data plane, and to manage, upgrade, and scale it. Removing them can break those operations.
>
> If you need to remove specific permissions, contact the LangChain team first so the change can be reviewed. LangChain is not responsible for downtime or issues caused by permissions removed without that review.

> [accordion] What does LangChain hold in the control plane?
>
> Authentication, organization and workspace configuration, billing and usage metadata, hashed API keys, and the static frontend assets.
>
> Traces, prompts, datasets, evaluators, experiments, insights runs, annotation queues, agent deployments, and workspace secrets all live in your data plane.

> [accordion] What data leaves my account?
>
> Only operational data, and it travels over PrivateLink rather than the public internet:
>
> * **Authentication requests**: The data plane calls the control plane to authenticate requests, validate API keys, and resolve roles and permissions.
> * **Configuration**: Organization and workspace configuration loaded from the control plane.
> * **Billing and usage metadata**.
> * **Operational telemetry**.
>
> Sensitive data such as traces does not leave your account. It goes only from the data plane to the end user requesting it. See [Data traffic](AWS/BYOC%20architecture.md#data-traffic).

> [accordion] Does traffic go over the public internet?
>
> No.
>
> * **Control plane to data plane**: All communication travels over AWS PrivateLink, in both directions.
> * **S3**: Traffic goes over a VPC endpoint, encrypted with HTTPS.
> * **Container images**: Pulled from the LangChain account over a VPC endpoint.
>
> See [Connectivity](AWS/BYOC%20architecture.md#connectivity).

> [accordion] Can I restrict outbound network traffic from the data plane?
>
> Yes.
>
> For a LangChain-managed VPC, BYOC supports a network firewall that controls egress from the data plane. Contact the LangChain team to enable it.
>
> Once enabled, the firewall denies all outbound traffic by default. You then configure an allow list of the destinations the data plane is permitted to reach:
>
> * **Domains**: Fully qualified domain names, such as a model provider API endpoint or a public Docker registry.
> * **CIDR ranges**: IP ranges, such as an internal service or a private subnet.
>
> With BYOVPC, you manage your own firewall and egress controls. Your network must continue to meet the [BYOVPC network requirements](AWS/Bring%20your%20own%20VPC%20on%20AWS.md#meet-the-network-requirements).

> [accordion] Can I use my own private registry?
>
> Not today. Container images are pulled from the LangChain AWS account over a VPC endpoint. Support for private registries is on the roadmap.

> [accordion] How does the control plane reach my Kubernetes API server?
>
> Over AWS PrivateLink. The management path exposes only your cluster's Kubernetes API server, which LangChain uses to install and reconcile the LangSmith components.
>
> The EKS cluster is private: the API server endpoint has no public access, and worker nodes have no public IP addresses. Your data is not reachable over that connection, and LangChain does not reach your environment over the public internet. See [Connectivity](AWS/BYOC%20architecture.md#connectivity).

> [accordion] Where does the control plane run if my data plane is outside the US?
>
> The control plane runs in `us-east-2` regardless of where you place your data planes. If you provision a data plane outside the US, your sensitive application data stays in that region while control plane metadata remains in the US. See [Regions and cloud providers](Bring%20Your%20Own%20Cloud%20%28BYOC%29.md#regions-and-cloud-providers).

## Data planes and workspaces

> [accordion] How do organizations, data planes, and workspaces relate?
>
> Data planes belong to an organization, and workspaces belong to exactly one data plane. Use data planes for physical separation of data, and workspaces for logical separation within a data plane. See [Organizations, data planes, and workspaces](BYOC%20usage.md#organizations-data-planes-and-workspaces).

> [accordion] Can I run more than one data plane?
>
> Yes. An organization can have several data planes, each in its own AWS account and region.
>
> The default limit is five data planes per organization. To deploy more than that, contact the LangChain team.

> [accordion] Can one organization hold both Cloud and BYOC workspaces?
>
> Yes. A workspace on LangSmith Cloud routes to the LangChain-managed backend rather than to a data plane, so both can coexist in the same organization. This also means you can move from an AWS Cloud trial to BYOC while reusing the same organization, users, roles, and SSO configuration.

## Operations

> [accordion] Who is responsible for what in a BYOC deployment?
>
> LangChain runs the control plane and manages the data plane infrastructure through delegated, least privilege access. You own the AWS account, network connectivity, the data in the data plane, and security monitoring inside your account.
>
> For the full division across platform and infrastructure, data and security, and operations and support, see the [BYOC shared responsibility model](BYOC%20shared%20responsibility%20model.md).

> [accordion] Who upgrades LangSmith, and how often?
>
> LangChain upgrades the LangSmith version in your data plane daily. Upgrades are rolling, so there is no whole-service downtime. Supporting services such as Istio and KEDA are upgraded on a regular cadence, and LangChain manages all EKS cluster upgrades.
>
> Support for release channels is coming soon. See [Operations](AWS/BYOC%20operations.md).

> [accordion] What about Kubernetes upgrades?
>
> LangChain owns and performs EKS upgrades proactively, ahead of AWS end-of-support dates, and coordinates the window with you.
>
> Control plane upgrades are transparent. Node group upgrades roll nodes one by one with make-before-break semantics, so you might see brief connection resets as pods restart, but no data loss. See [Kubernetes cluster upgrades](AWS/BYOC%20operations.md#kubernetes-cluster-upgrades).

> [accordion] Do upgrades cause downtime?
>
> No. Services run multiple replicas sized by a horizontal pod autoscaler, and pod disruption budgets cap how many replicas can be unavailable at once, so neither a rolling update nor a node drain takes a service below the capacity it needs.
>
> Maintenance that could cause downtime, such as a restart of RDS or ElastiCache, happens in a scheduled maintenance window that LangChain coordinates with you in advance.

> [accordion] Who monitors the data plane?
>
> LangChain operates the data plane after provisioning, including monitoring for uptime and error recovery, scaling, upgrades, and security patching. Because the deployment runs in your own account, the cloud controls you already operate apply to it as well.

> [accordion] Can I set up my own observability for LangSmith BYOC?
>
> Yes. You can install observability tooling such as collectors and agents into the EKS cluster, as long as it does not interfere with the operation of LangSmith.
>
> LangSmith services emit logs, metrics, and traces the same way they do on self-hosted, so the same configuration applies. See [Export LangSmith telemetry to your observability backend](../Self-hosted/Self-hosted%20observability/Export%20LangSmith%20telemetry%20to%20your%20observability%20backend.md).

> [accordion] How are high availability and disaster recovery handled?
>
> Data planes are provisioned for high availability by default, running across multiple availability zones within a single region. All stateful components are backed up.
>
> A data plane does not span regions, so recovery from the loss of an entire region relies on those backups. See [High availability](AWS/BYOC%20operations.md#high-availability).

> [accordion] How are backups handled?
>
> Backups run in your own account:
>
> * **RDS**: Backups are taken daily.
> * **SmithDB**: Object storage in S3 holds the durable trace data.
> * **ClickHouse**: On data planes that still run it, backups are taken daily and stored in an S3 bucket.
> * **ElastiCache**: No backups are taken, because the data is ephemeral.

> [accordion] Does LangChain offer an uptime SLA for BYOC data planes?
>
> No. The data plane runs in your AWS account, so its availability depends on resources you control, including the account itself, the private connectivity you configure to reach the data plane, and the service quotas and policies that apply to the account. LangChain does not commit to an uptime target for infrastructure it does not solely control.
>
> LangChain still monitors the data plane for uptime and error recovery, scales it, and applies upgrades and security patches. See [Operations](AWS/BYOC%20operations.md).

## Cost

> [accordion] What do I pay for with BYOC?
>
> Two separate bills:
>
> * **Infrastructure**: The data plane runs in your own AWS account, so you own the infrastructure and pay for it through your cloud provider bill.
> * **LangSmith**: Invoiced by LangChain based on your contract and usage.
>
> LangChain provides integrations with AWS Marketplace.

## Features and migration

> [accordion] Which LangSmith features work on BYOC?
>
> See [Available features](Bring%20Your%20Own%20Cloud%20%28BYOC%29.md#available-features) for the current list of supported features.

> [accordion] Can I migrate an existing LangSmith instance to BYOC?
>
> Yes. Users, roles, datasets, experiments, prompts, annotation queue configuration, automation rules, dashboards, and Fleet resources can be copied over. Trace migration is supported on AWS. Contact the LangChain team to arrange it. See [Migrate to BYOC](Migrate%20to%20BYOC.md).

## See also

* [BYOC overview](Bring%20Your%20Own%20Cloud%20%28BYOC%29.md)
* [Why BYOC](Why%20BYOC.md)
* [BYOC architecture](AWS/BYOC%20architecture.md)
