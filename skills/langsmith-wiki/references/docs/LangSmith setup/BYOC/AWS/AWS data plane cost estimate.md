# AWS data plane cost estimate

> Rough AWS cost of a LangSmith BYOC data plane running SmithDB, with a legacy estimate for data planes created with ClickHouse.

> [!WARNING]
>
> These are estimates, not a quote. AWS changes its prices without notice. Your bill depends on region, usage, and any discount agreement with AWS, such as an Enterprise Discount Program or a Savings Plan.

This is a rough monthly cost for a LangSmith data plane in your AWS account.

> [!NOTE]
>
> Scaling capacity for any resource can be lowered when required, as long as the deployment remains within safe operating limits. For cost-conscious or pre-production deployments, Multi-AZ can be turned off. That lowers monthly cost but reduces fault tolerance.

> [tab] SmithDB
>
> Data planes created on or after October 21, 2026 run SmithDB only. They do not run ClickHouse or ZooKeeper. This estimate is for a low tracing volume, about 10 runs per second and 10 queries per second. See [Configure SmithDB for scale](../../Self-hosted/SmithDB/Install%20SmithDB/Configure%20SmithDB%20for%20scale.md). LangSmith increases capacity as tracing volume requires it.
>
> | Area | Rough monthly estimate | Notes |
> | - | - | - |
> | RDS PostgreSQL | \$100–\$150 | `db.t4g.medium`, Multi-AZ, 50 GB starting storage. |
> | ElastiCache Redis | \~\$285 | 3 shards with 1 replica each: 6 `cache.t4g.medium` nodes. |
> | EKS control plane | \~\$75 | One EKS cluster at standard hourly pricing. |
> | System node group | \~\$210 | 3 `m6i.large` on-demand nodes. |
> | Application worker nodes | \$700–\$2,000 | Karpenter nodes for LangSmith pods. |
> | EBS volumes | \$40–\$80 | Node boot disks. SmithDB cache uses the node disk, not a separate gp3 volume. |
> | Networking | \$150–\$300 | NAT gateways, load balancers, PrivateLink or VPC endpoints, and low-volume data processing. |
> | S3, Secrets Manager, CloudWatch | \$50–\$200 | Low-volume baseline. Grows with trace payloads, logs, and retention. |
> | SmithDB compute | \$1,400–\$2,045 | Low end is 1 x `c6id.8xlarge` plus 1 x `c6a.2xlarge`. High end is 1 x `i3.8xlarge`, or 2 x `i3.4xlarge`, plus 1 x `c6a.2xlarge`. Query, ingestion, and the compaction worker use the larger node. |
> | SmithDB metastore | \~\$120 | RDS PostgreSQL 18, `db.t4g.medium`, Multi-AZ, 100 GB gp3. |
> | SmithDB bucket | \$5–\$120 | S3 storage costs, would largely be dictated by trace payload size and retention. |
>
> Estimated monthly total: **\$3,135–\$5,585**
>
> ### SmithDB object store pricing
>
> | Stored size per trace | 14-day retention | 400-day retention |
> | - | - | - |
> | 10 KB | \$2 per year | \$74 per year |
> | 50 KB | \$15 per year | \$368 per year |
> | 200 KB | \$52 per year | \$1,472 per year |
>
> See [Prepare SmithDB supporting infrastructure](../../Self-hosted/SmithDB/Install%20SmithDB/Prepare%20SmithDB%20supporting%20infrastructure.md) for details of SmithDB infrastructure.

> [tab] ClickHouse (deprecated)
>
> > [!WARNING]
> >
> > ClickHouse is deprecated, and support ends in LangSmith v0.19. Data planes created on or after October 21, 2026 run SmithDB only. This estimate applies to data planes created with ClickHouse before that date that have not yet migrated to SmithDB.
>
> ClickHouse can also run as a single node instead of a replicated cluster. That lowers monthly cost but reduces fault tolerance.
>
> | Area | Rough monthly estimate | Notes |
> | - | - | - |
> | RDS PostgreSQL | \$100–\$150 | `db.t4g.medium`, Multi-AZ, 50 GB starting storage. |
> | ElastiCache Redis | \~\$285 | 3 shards with 1 replica each: 6 `cache.t4g.medium` nodes. |
> | EKS control plane | \~\$75 | One EKS cluster at standard hourly pricing. |
> | System node group | \~\$210 | 3 `m6i.large` on-demand nodes. |
> | Application, ClickHouse, and ZooKeeper worker nodes | \$1,000–\$1,500 | LangSmith pods and ClickHouse pods. |
> | EBS volumes | \$200–\$350 | ClickHouse, ZooKeeper, node volumes, and gp3 performance settings. |
> | Networking | \$150–\$300 | NAT gateways, load balancers, PrivateLink or VPC endpoints, and low-volume data processing. |
> | S3, Secrets Manager, CloudWatch | \$50–\$200 | Low-volume baseline. Grows with trace payloads, logs, and retention. |
>
> Estimated monthly total: **\$2,070–\$3,070**
