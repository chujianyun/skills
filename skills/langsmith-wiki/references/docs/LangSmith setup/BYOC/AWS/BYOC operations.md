# BYOC operations

> How LangChain upgrades, patches, and maintains a LangSmith BYOC data plane, and when maintenance requires a scheduled window.

LangChain operates your data plane after provisioning, including upgrades, scaling, monitoring, and security patching. Most maintenance is non-disruptive and requires no action from you.

## Autoscaling

LangChain scales your data plane as load changes, so you do not need to size or tune it:

* **Stateless LangSmith services**: Scaled horizontally by a horizontal pod autoscaler, with Karpenter provisioning and removing node capacity as pod demand changes.
* **Databases**: LangChain sizes and scales RDS and ElastiCache.

## High availability

Data planes are provisioned for high availability by default. The deployment spans multiple availability zones in your region, and RDS and ElastiCache run Multi-AZ with automatic failover.

> [!NOTE]
>
> To run a data plane without high availability, contact the LangChain team.

## Instance sizes

Data planes are provisioned with default instance sizes for the databases and node groups. To run a data plane on smaller instances, contact the LangChain team.

## LangSmith upgrades

LangChain upgrades the LangSmith version in your data plane daily. Upgrades are rolling, replica-by-replica, so there is no whole-service downtime.

Two mechanisms keep upgrades free of downtime:

* **Horizontal pod autoscaling**: LangSmith services run multiple replicas, sized by a horizontal pod autoscaler, so pods are replaced a few at a time while the remaining replicas continue serving traffic.
* **Pod disruption budgets**: A pod disruption budget caps how many replicas of a service can be unavailable at once, so neither a rolling update nor a node drain takes a service below the capacity it needs to stay available.

## Supporting service upgrades

Background services such as Istio and KEDA are upgraded on a regular cadence. Data planes that still run ClickHouse also receive ClickHouse operator upgrades. These upgrades are non-intrusive, and no service interruption is expected.

## Kubernetes cluster upgrades

The EKS cluster that hosts your data plane requires periodic upgrades to maintain security, compatibility, and access to new features. LangChain performs these upgrades proactively, ahead of AWS end-of-support dates, and coordinates the window with you.

Cluster upgrades fall into two types:

* **Control plane upgrades**: Cover the Kubernetes API server and the components AWS manages alongside it. These are transparent to your workloads and do not restart pods.
* **Node group upgrades**: Roll nodes one by one with make-before-break semantics. New nodes are provisioned on the updated version, pods move onto them, and the old nodes are terminated once migration completes. Pod disruption budgets apply to the drain, so each service stays available, though you might see brief connection resets as individual pods restart. No data is lost.

## Maintenance windows

Any maintenance or upgrade that could cause downtime, such as a restart of RDS or ElastiCache, happens in a scheduled maintenance window that LangChain coordinates with you in advance.

## Observability

You can deploy observability tooling into the cluster, such as a Datadog agent or an OpenTelemetry collector, and your own security monitoring agents, as long as they do not interfere with LangSmith workloads.

LangSmith services emit logs, metrics, and traces the same way they do on self-hosted, so the same configuration applies. See [Export LangSmith telemetry to your observability backend](../../Self-hosted/Self-hosted%20observability/Export%20LangSmith%20telemetry%20to%20your%20observability%20backend.md).

## Troubleshooting

The LangChain team has no standing access to your data, and can only manage the infrastructure of your data plane. When troubleshooting requires access to data, there are two paths:

* **You run the query**: You run the query yourself, and validate and sanitize the output before sharing it with LangChain.
* **Break-glass access**: You allowlist a specific engineer to perform the operation. You can revoke that access at any time.

> [!NOTE]
>
> If break-glass access is needed, the LangChain team reaches out with instructions.

## Auditing

* **LangSmith audit logs**: Operations on data plane resources are recorded in the data plane and accessible at your data plane endpoint. Control plane actions, such as creating a user, are audited in the control plane. For how to access both, see [Audit logs](../../Govern/Auditing/Audit%20logs.md).
* **EKS audit logs**: Sent to CloudWatch in your account, so you can monitor the commands that were run.
* **VPC flow logs**: Recorded in an S3 bucket in your account. With [BYOVPC](Bring%20your%20own%20VPC%20on%20AWS.md), you configure VPC flow logs yourself.

Setting up alerts on those logs is your responsibility.

## See also

* [BYOC architecture](BYOC%20architecture.md)
* [Using BYOC](../BYOC%20usage.md)
