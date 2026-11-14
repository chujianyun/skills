# BYOC billing

> How LangSmith BYOC is billed across your AWS account and your LangSmith contract, which AWS services carry cost, and the account quotas to check before you deploy.

## Cost model

A BYOC deployment produces two separate bills:

* **AWS**: The data plane runs in your own AWS account, so AWS bills you directly for the infrastructure it creates.
* **LangSmith**: LangChain invoices you based on your contract and usage.

LangSmith BYOC can integrate with AWS Marketplace.

## Billable AWS services

The following resources contribute to data plane costs in your account. AWS charges for them at its own rates, independently of your LangSmith contract. With [BYOVPC](Bring%20your%20own%20VPC%20on%20AWS.md), networking costs depend on the gateways, endpoints, and logging you configure and manage.

| Service | What it covers | Billing basis |
| - | - | - |
| **Amazon EKS** | The Kubernetes control plane for the data plane cluster | Per cluster-hour |
| **Amazon EC2** | Nodes running in the EKS cluster | Per instance-hour |
| **Amazon RDS** | Instances for relational workloads. SmithDB uses an Aurora PostgreSQL Serverless v2 metastore. | Per instance-hour, including Multi-AZ, plus storage, backups, and snapshots. Aurora is billed per ACU-hour, plus storage and I/O. |
| **Amazon ElastiCache** | Redis instance for caching and queueing workloads | Per node-hour |
| **Amazon S3** | Buckets for LangSmith workloads, the SmithDB object store, and VPC flow logs. Data planes that still run ClickHouse also store its backups here. | Storage, requests, and data transfer |
| **Amazon EBS** | Node root disks, including the SmithDB node boot volumes, and the ClickHouse volumes on data planes that still run it | Per GB-month, plus provisioned IOPS and throughput above the gp3 baseline |
| **Regional NAT gateway** | Outbound egress from the private subnets | Per hour, plus data processed |
| **Elastic Load Balancing** | Two network load balancers: one in front of the Istio ingress, and one for the EKS API PrivateLink endpoint | Per NLB-hour, plus NLCUs |
| **AWS PrivateLink** | The interface VPC endpoints the data plane uses | Per interface endpoint per availability zone-hour, plus data processed |
| **AWS Lambda and Amazon EventBridge** | Reconciliation of the PrivateLink endpoints | Per invocation, and per event published |
| **Amazon CloudWatch Logs** | EKS control plane logs | Ingestion and storage |
| **VPC flow logs** | Delivery of flow logs to S3 | Per GB delivered |
| **Amazon Route 53** | Private hosted zone | Per hosted zone-month, plus queries |
| **AWS Secrets Manager** | RDS-generated master secrets, and the application secrets LangSmith references | Per secret-month, plus API calls |

### Data transfer

There are a few data transfer cost drivers in BYOC:

* Cross-availability-zone traffic, since the data plane runs [highly available](BYOC%20operations.md#high-availability) across zones.
* Egress through the NAT gateway, for example if calling model providers, or an external API through a webhook.
* Public IPv4 addresses, which AWS charges per address-hour. The regional NAT gateway uses one, and an internet-facing load balancer uses another when public ingress is enabled.

## Service limits

AWS enforces default quotas per region and per account. Defaults are often too low for production on new or lightly used accounts, so check the following before you deploy, and request increases where needed:

* **EC2 vCPU quotas**: At minimum, 64 vCPU of On-Demand capacity, covering the 3 system nodes and Karpenter workloads.
* **Subnet IP capacity**: Room for pods, nodes, EKS ENIs, load balancers, and at least 12 interface endpoints per application subnet.
* **VPC endpoints**: Capacity for 12 interface endpoints and 1 S3 gateway endpoint.
* **Load balancers**: Capacity for 2 Network Load Balancers and their target groups.
* **EKS**: Capacity for 1 EKS cluster.
* **Storage**: EBS volume and storage capacity for node disks and other persistent workloads, plus ClickHouse and ZooKeeper on data planes that still run them.
* **Databases**: Capacity for 2 RDS instances, one Aurora cluster for the SmithDB metastore (writer and reader), and 3 ElastiCache replicas.
* **PrivateLink and networking**: Capacity for 1 endpoint service and 1 regional NAT gateway.

For current default values, see [AWS service quotas](https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html).

With BYOVPC, account for existing resource usage and your chosen endpoint and egress configuration when checking quotas. Your supplied subnets must also meet the [subnet size and available IP requirements](Bring%20your%20own%20VPC%20on%20AWS.md#configure-the-vpc-and-subnets).

If provisioning stalls or fails, an exhausted quota is a common cause, alongside missing permissions and service control policies. See [What happens if provisioning fails?](../BYOC%20FAQ.md).

## See also

* [BYOC architecture](BYOC%20architecture.md)
* [Operations](BYOC%20operations.md)
* [BYOC FAQ](../BYOC%20FAQ.md)
