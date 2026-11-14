# BYOC architecture

> How a LangSmith BYOC deployment is structured across the LangChain control plane and the data plane in your AWS account.

## Control plane and data plane model

A BYOC deployment is split across two planes. This page describes the components of each plane, how they communicate, and what LangChain provisions in your account.

This page covers BYOC on AWS. For BYOC on GCP, see [BYOC architecture on GCP](../GCP/BYOC%20architecture%20on%20GCP.md) or [BYOC architecture on Azure](../Azure/BYOC%20architecture%20on%20Azure.md).

The **control plane** runs in LangChain's cloud and handles authentication, organization configuration, and billing. It provisions, monitors, and orchestrates your deployment, but does not hold any sensitive application data.

The **data plane** runs in your AWS account and ingests, stores, and queries all of your sensitive application data. It holds your VPC, EKS cluster, databases, and other resources.

The table below summarizes the split:

| Plane | Where it runs | What it holds |
| - | - | - |
| **Control plane** | LangChain's cloud, `us-east-2` | Authentication, organization and workspace configuration, billing and usage metadata, LangSmith API keys, and the static frontend assets |
| **Data plane** | Your AWS account, in the region you choose | Traces, prompts, datasets, evaluators, experiments, insights runs, annotation queues, agent deployments, workspace secrets, and other application data |

![BYOC architecture diagram. The LangSmith UI and the client apps in your application VPC both reach the data plane over one private connection, using PrivateLink, VPC peering, or Tailscale, which terminates at a network load balancer. The load balancer feeds an Istio ingress in an EKS cluster in your AWS account, which routes to the LangSmith services that run the backend, SmithDB, and sandboxes, and those services read and write S3, RDS, and ElastiCache. The LangChain cloud control plane holds Crossplane, on-call engineers, alerting, and the LangSmith control plane services. It reaches the cluster over PrivateLink for scaling and upgrades, receives auth and telemetry back over a second PrivateLink, and assumes an IAM role in your account to provision resources.](../../../../assets/images/901f7f1388f3-byoc-architecture.png)

## Provisioned resources

LangChain provisions the following in your account:

* **VPC**: By default, a dedicated VPC spread across the region's availability zones, with private ingress. It uses VPC endpoints for private communication to AWS services, and PrivateLink for communication between the data plane and the control plane. With [BYOVPC](Bring%20your%20own%20VPC%20on%20AWS.md), you create and manage the VPC and its base network resources instead.
* **Managed databases**: RDS for relational workloads and the SmithDB metastore, and ElastiCache for caching.
* **Storage**: S3 buckets for the blob store holding trace data, the SmithDB object store, and VPC flow logs.
* **EKS**: A private EKS cluster with managed add-ons.
* **Compute**: A system node group for platform workloads, and application node groups through Karpenter.
* **In-cluster resources**: The LangSmith Helm chart, Istio, KEDA, and other in-cluster resources.
* **IAM roles**: The roles and permissions required for Kubernetes resources.

> [!NOTE]
>
> Data planes created on or after October 21, 2026 store and query traces in [SmithDB](../../Self-hosted/SmithDB/Overview/Enable%20SmithDB%20on%20self-hosted%20LangSmith.md) only. ClickHouse is deprecated, and support ends in LangSmith v0.19. Data planes created with ClickHouse keep it, along with its S3 backups, until they migrate to SmithDB.

## Cross-account IAM permissions

LangChain needs cross-account IAM permissions to provision and manage resources within your AWS account. These permissions let LangChain:

* **Provision infrastructure**: Create and configure the VPC, subnets, security groups, and other networking components. With BYOVPC, the role retains workload networking permissions, while you manage the base network.
* **Manage the Kubernetes cluster**: Deploy and maintain the EKS cluster, its node groups, and cluster add-ons.
* **Create storage resources**: Provision RDS, ElastiCache, and the S3 buckets used for application data and backups.
* **Create IAM roles**: Create and configure the roles used by Kubernetes service accounts and supporting services.
* **Operate supporting services**: Deploy and manage ingress and autoscaling, and scale and upgrade LangSmith workloads.

Permissions are granted through a single cross-account IAM role that you create during onboarding by applying the [`langsmith-byoc-role` Terraform module](https://github.com/langchain-ai/terraform/tree/main/modules/byoc/aws/langsmith-byoc-role).

For BYOVPC, disable base VPC creation permissions and scope security group creation to your supplied VPC IDs. See [Create the reduced-permission IAM role](Bring%20your%20own%20VPC%20on%20AWS.md#create-the-reduced-permission-iam-role).

LangChain provides the external ID used in the role's trust policy. Copy it using the button next to the **Data Planes** header in **Settings > Data Planes**, and use it when applying the module. The role's `ExternalId` condition must match this value.

### How least privilege is enforced

The role is scoped to only what BYOC operations require:

* **Scoped to LangSmith-owned resources**: Wherever AWS supports resource-level scoping, permissions are restricted to resources carrying specific tags and name prefixes, so the role cannot act on unrelated resources in the account.
* **Infrastructure-scoped, not data-scoped**: The role can manage the resources that hold your data, but cannot read the data itself through AWS data APIs. It holds no `s3:GetObject` on the trace bucket, no `rds-db:connect` to PostgreSQL, and no `elasticache:Connect` to Redis.

## Networking

### Data traffic

Sensitive data does not leave your VPC, and does not pass through LangChain's VPC.

1. When a user opens `aws.smith.langchain.com`, the browser fetches the LangSmith UI bundle of HTML, JavaScript, CSS, and images from LangChain's cloud. These assets are the same code that every BYOC and Cloud tenant runs, and contain no customer data.
2. Once loaded, the application resolves the data plane endpoint for the selected workspace and routes every request for sensitive data to your VPC.

To ingest or query data programmatically, point your client at your data plane directly. The data flow is always `browser or client → data plane → back to client`.

![Data traffic diagram. A user on their own machine, VPC, or network opens aws.smith.langchain.com in a browser. The browser makes two requests: first it fetches the UI bundle of HTML, CSS, and JavaScript from the static assets in LangChain's cloud, which hold no customer data; second it sends data plane API requests to the network load balancer in your BYOC VPC, which routes to the EKS cluster running LangSmith and on to S3, RDS, and the cache.](../../../../assets/images/ad36cb0c864c-byoc-data-flow.png)

### Connectivity

All communication between the control plane and your data plane travels over AWS PrivateLink, in both directions. LangChain does not reach your environment over the public internet. BYOC establishes two PrivateLink connections:

* **Control plane to data plane (management path)**: Exposes only your cluster's Kubernetes API server, which LangChain uses to install and reconcile the LangSmith components. Your data is not reachable over this connection.
* **Data plane to control plane (runtime path)**: The data plane calls the control plane to authenticate requests, validate API keys, resolve roles and permissions, and load organization and workspace configuration.

Container images are pulled read-only from LangChain's control plane ECR repositories through VPC endpoints.

With BYOVPC, you configure the customer-side AWS service endpoints and data-plane-to-control-plane PrivateLink endpoint. LangChain manages the endpoint service for the cluster management path. See [Configure connectivity](Bring%20your%20own%20VPC%20on%20AWS.md#configure-connectivity).

### DNS and ingress

Traffic reaches LangSmith through an Istio ingress fronted by an AWS NLB, using Route 53 for DNS resolution. Once your data plane is created, its API URL is listed under **Settings > Data Planes** in the LangSmith UI.

## See also

* [BYOC overview](../Bring%20Your%20Own%20Cloud%20%28BYOC%29.md)
* [Operations](BYOC%20operations.md)
* [Egress for billing and operational telemetry](../../Self-hosted/Configure%20an%20instance/Egress%20for%20billing%20and%20operational%20telemetry.md)
