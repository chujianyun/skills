# BYOC shared responsibility model

> How LangChain and your organization divide responsibility for a LangSmith BYOC deployment across operations, security, support, and compliance.

The BYOC shared responsibility model defines what LangChain manages and what your organization manages in a LangSmith BYOC deployment. Under this model, sensitive data does not transit LangChain infrastructure during normal operation. The sections below cover this division across platform and infrastructure, data and security, and operations and support.

For the multi-tenant SaaS equivalent, see the [LangSmith shared responsibility model](../Govern/Data%20%26%20compliance/LangSmith%20shared%20responsibility%20model.md). For the technical structure of the control plane and data plane, see [BYOC architecture](AWS/BYOC%20architecture.md).

## Access model

* **Control plane and data plane are split**: LangChain runs the control plane. You own the cloud environment that contains the data plane, and LangChain manages the infrastructure inside that environment through delegated access.
* **Access is least privilege, with break-glass as the exception**: The routine access LangChain holds is scoped to provisioning and operations. Data access is not required for normal operations. Incident troubleshooting may require customer-approved break-glass access, granted through the shared support channel.
* **You remain accountable for your cloud account**: You control your cloud account or subscription governance, network connectivity, and internal access policies.

For GCP project access and networking requirements, see [GCP onboarding](GCP/BYOC%20onboarding%20on%20GCP.md).

For Azure resource group access, Key Vault setup, and networking requirements, see [Azure onboarding](Azure/BYOC%20onboarding%20on%20Azure.md). For Azure resources and permissions, see [Azure architecture](Azure/BYOC%20architecture%20on%20Azure.md).

## Platform and infrastructure

| Area | LangChain responsibilities | Your responsibilities |
| :- | :- | :- |
| **Service scope and architecture** | <ul><li>Define the BYOC architecture</li><li>Operate the control plane, covering organization configuration, authentication, billing metadata, and frontend assets</li></ul> | <ul><li>Get sign-off from your security, infrastructure, and application teams</li><li>Confirm the BYOC architecture meets your requirements</li></ul> |
| **Cloud account ownership** | <ul><li>Operate only through customer-delegated roles and in-scope permissions</li></ul> | <ul><li>Own your cloud accounts or subscriptions and budgets</li><li>Own account guardrails, such as service control policies on AWS</li><li>Own organization structure and account lifecycle</li></ul> |
| **Provisioning and changes** | <ul><li>Provision the BYOC infrastructure and Kubernetes resources that run the LangSmith data plane</li><li>Manage updates and rollouts for BYOC-managed components</li><li>Acknowledge and schedule change requests through the shared support channel</li></ul> | <ul><li>Approve onboarding steps and provide the required account and region details</li><li>Avoid manual edits to BYOC-managed resources</li><li>Request changes through the shared support channel</li></ul> |
| **Networking** | <ul><li>Configure LangSmith components for the supported connectivity model, such as PrivateLink</li><li>Communicate the required endpoints and constraints</li></ul> | <ul><li>Own the internal connectivity your users and applications need to reach the LangSmith BYOC data plane</li></ul> |
| **Control plane** | <ul><li>Operate authentication, organization configuration, and API key management</li><li>Serve the static frontend assets and operate the usage and billing surfaces</li></ul> | <ul><li>Manage organization-level admins and govern who can create and manage data planes and workspaces</li></ul> |
| **Data plane services** | <ul><li>Operate the services that ingest and query traces, prompts, datasets, evaluations, insights, and deployments</li><li>Keep those services healthy through monitoring, scaling, and upgrades</li></ul> | <ul><li>Do not co-locate unrelated workloads in the BYOC cluster or private network</li><li>Validate application behavior in your environment</li></ul> |
| **Scaling and capacity** | <ul><li>Monitor and scale BYOC-managed services</li><li>Give advance notice before material scaling events where possible, with the expected cost impact</li></ul> | <ul><li>Ensure cloud service quotas are high enough for the deployed services, and request increases as needed</li><li>Accept the cost implications in your cloud account</li><li>Define internal cost guardrails and alerts</li></ul> |
| **Upgrades and patching** | <ul><li>Roll out upgrades and patches to BYOC-managed components</li><li>Coordinate for major changes and maintenance windows</li></ul> | <ul><li>Plan change management internally, including stakeholder communication and staging validation</li><li>Follow your own change control processes</li></ul> |

For details on how upgrades, autoscaling, and maintenance windows work, see [BYOC operations](AWS/BYOC%20operations.md).

> [!NOTE]
>
> On AWS, with [BYOVPC](AWS/Bring%20your%20own%20VPC%20on%20AWS.md), you also create and maintain:
>
> * VPC
> * Subnets
> * Routes,
> * Gateways
> * Customer-side VPC endpoints
> * Flow logs
> * Egress controls
>
> LangChain validates the supplied network before provisioning and manages the workload infrastructure inside it. Customer-managed network resources remain your responsibility during operation and after data plane deletion.

## Data and security

| Area | LangChain responsibilities | Your responsibilities |
| :- | :- | :- |
| **Customer data** | <ul><li>Design the system so that sensitive data does not transit LangChain infrastructure for normal operation</li><li>Avoid access to customer data in normal operation</li></ul> | <ul><li>Own the data in the data plane, including classification, retention, and access controls</li><li>Own the legal and compliance obligations for that data</li><li>Approve any data export or sharing internally</li></ul> |
| **Data residency** | <ul><li>Provision all data plane components and storage only within the cloud region you designate</li><li>Keep customer data out of LangChain-managed infrastructure during normal operation</li></ul> | <ul><li>Specify the required cloud region at onboarding</li><li>Communicate any change to your data residency requirements in advance</li></ul> |
| **Secrets management** | <ul><li>Use secret stores in the customer account for runtime secrets</li><li>Reference secrets without persisting sensitive values in the control plane</li></ul> | <ul><li>Apply any organization-specific key management requirements</li></ul> |
| **Break-glass access** | <ul><li>Use break-glass access only for incident mitigation, with customer approval and a defined process</li><li>Minimize the duration and scope of that access</li><li>Give advance notice where possible</li><li>Deliver a post-access summary covering timestamps, actions taken, and any data accessed</li></ul> | <ul><li>Approve break-glass access when it is required</li><li>Define the internal approval workflow</li><li>Review post-incident access logs and notes</li></ul> |
| **Access audit logs** | <ul><li>Provision the logging infrastructure in your account so LangChain access is recorded, including EKS audit logs</li><li>Do not view, analyze, or alert on those logs on your behalf</li></ul> | <ul><li>Retain AWS CloudTrail and account-level logs for all LangChain-assumed roles</li><li>View and analyze those logs, and set up your own alerting on them</li><li>Escalate anomalies to LangChain through the shared support channel</li></ul> |
| **Security incident notification** | <ul><li>Notify you of a confirmed security incident in LangChain-owned infrastructure that affects your deployment, covering the control plane, corporate systems, and the BYOC build and release pipeline</li><li>Share the incident scope, impact assessment, and remediation steps</li><li>Cooperate on joint forensics</li><li>Do not run security monitoring inside your cloud account</li></ul> | <ul><li>Deploy and operate security monitoring for the BYOC components in your account, such as EDR, IDS, container security, cloud security posture management, and log aggregation</li><li>Keep that monitoring from affecting the operation of BYOC-managed resources</li><li>Designate a security contact and define internal incident response procedures</li><li>Notify LangChain promptly of any suspected compromise of customer-side credentials or access</li></ul> |
| **Compliance and audits** | <ul><li>Provide documentation on the BYOC architecture and operational model</li><li>Supply audit evidence for LangChain-operated controls, including access logs, change history, security policies, and penetration test summaries</li><li>Support SOC 2, ISO 27001, and equivalent audit programs</li></ul> | <ul><li>Own the compliance posture of your cloud environment and all customer-managed controls</li><li>Run or coordinate audits and evidence collection for that environment</li></ul> |

The IAM permissions that scope LangChain access are described in [Cross-account IAM permissions](AWS/BYOC%20architecture.md#cross-account-iam-permissions). For how break-glass access works in practice, see [Troubleshooting](AWS/BYOC%20operations.md#troubleshooting). For where the audit logs live and how to access them, see [Auditing](AWS/BYOC%20operations.md#auditing).

## Operations and support

| Area | LangChain responsibilities | Your responsibilities |
| :- | :- | :- |
| **Observability** | <ul><li>Provide and operate service-level monitoring and alerts for BYOC-managed components</li><li>Request customer-provided signals when they are needed for diagnosis</li></ul> | <ul><li>Provide requested logs, metrics, and timestamps from your own systems</li><li>Provide the same from your networking layers when troubleshooting requires it</li></ul> |
| **Incident response and support** | <ul><li>Act as primary responder for LangChain-managed components, covering the control plane and the BYOC-managed data plane services</li><li>Coordinate communication through the shared support channel</li></ul> | <ul><li>Act as primary responder for customer-owned layers, including cloud policies, internal networking, and access controls</li><li>Provide timely access and approvals for investigation</li></ul> |
| **Backup and disaster recovery** | <ul><li>Define and operate backup processes for LangChain-managed data plane components</li><li>Provision data planes for high availability across multiple availability zones in a single region</li></ul> | <ul><li>Define your internal recovery objectives and validate them with the LangChain team</li><li>Own backups for any customer-managed data stores outside the BYOC scope</li></ul> |
| **Maintenance windows and change freezes** | <ul><li>Perform infrastructure maintenance and upgrades inside the agreed maintenance window</li><li>Act outside that window only when a change is required to keep the data plane functioning correctly, such as under increased load</li><li>Accommodate requested change freezes for sensitive business periods, with reasonable advance notice</li></ul> | <ul><li>Set an AWS maintenance window in the LangSmith UI, or use the API for GCP and Azure</li><li>Communicate upcoming change freezes, such as fiscal close or major releases, with reasonable advance notice</li></ul> |
| **Offboarding and termination** | <ul><li>Remove all LangChain-managed resources, IAM roles, and delegated access within the agreed timeframe on contract termination</li><li>Provide written confirmation that deprovisioning is complete</li></ul> | <ul><li>Initiate offboarding through the shared support channel</li><li>Verify resource and access cleanup after confirmation</li><li>Revoke customer-managed roles and access grants tied to BYOC</li></ul> |

## See also

* [BYOC architecture](AWS/BYOC%20architecture.md)
* [BYOC operations](AWS/BYOC%20operations.md)
* [BYOC FAQ](BYOC%20FAQ.md)
* [LangSmith shared responsibility model](../Govern/Data%20%26%20compliance/LangSmith%20shared%20responsibility%20model.md)
