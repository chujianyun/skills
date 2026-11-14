# LangSmith for Enterprise

> Hosting options, access control, data privacy, cost controls, and security compliance for Enterprise users.

This page is a reference hub for enterprise teams and includes information on features that are important for your organization, like [hosting options](#hosting-options), [access control](#access-control), [data privacy](#data-privacy-and-pii), and [cost controls](#cost-controls-and-usage).

For questions about Enterprise [pricing](https://docs.langchain.com/langsmith/pricing-plans.md) or to get started, [contact our sales team](https://www.langchain.com/contact-sales).

## Hosting options

Choose how to host LangSmith to match your infrastructure and data residency requirements.

> [card] [Cloud](../Cloud/Cloud%20%28SaaS%29.md)
>
> Host LangSmith in LangSmith's managed cloud with US or EU data residency.

> [card] [Hybrid](../../Deploy/Deploy%20to%20Self-hosted/Hybrid.md)
>
> Run the control plane in LangSmith's cloud and your data plane in your own VPC for full data isolation.

> [card] [Self-hosted](../Self-hosted/Self-hosted%20LangSmith.md)
>
> Host LangSmith entirely within your own infrastructure using Kubernetes.

## User management

Manage users and automate provisioning across your organization.

> [card] [User management](../Govern/Users%20%26%20access%20control/User%20management.md)
>
> Invite users, assign roles, and configure SCIM for automated provisioning and deprovisioning.

> [card] [SSO & JIT provisioning](../Govern/Users%20%26%20access%20control/Authentication%20methods.md)
>
> Configure SAML or OIDC single sign-on and just-in-time user provisioning for your identity provider.

> [card] [Organization setup](../Govern/Organization/Workspace%20setup/Set%20up%20hierarchy.md)
>
> Create and configure organizations, workspaces, and the user hierarchy within your enterprise.

> [card] [Manage by API](../Govern/Organization/Manage%20your%20organization%20using%20the%20API.md)
>
> Programmatically manage users, configure security settings, and administer your organization via API.

## Access control

Control who can access what within your organization.

> [card] [Role-based access control (RBAC)](../Govern/Users%20%26%20access%20control/Role-based%20access%20control.md)
>
> Define permissions per workspace using built-in or custom roles. Available exclusively on Enterprise plans.

> [card] [Attribute-based access control (ABAC)](../Govern/Users%20%26%20access%20control/Attribute-based%20access%20control.md)
>
> Apply fine-grained, tag-based access policies to restrict resource access—including blocking PII data from specific users.

> [card] [Workload isolation](../Govern/Organization/Workspace%20setup/Workload%20isolation.md)
>
> Use multi-workspace models to isolate teams, establish trust boundaries, and separate environments.

> [card] [Resource tags](../Govern/Organization/Workspace%20setup/Set%20up%20resource%20tags.md)
>
> Tag resources for use with ABAC policies and to organize environments like dev, staging, and prod.

## Data privacy and PII

Control how sensitive data is stored and accessed.

> [card] [Data storage & privacy](../Govern/Data%20%26%20compliance/Data%20storage%20and%20privacy.md)
>
> Understand what LangSmith stores, how encryption works, and how to opt out of telemetry and tracing.

> [card] [PII controls with ABAC](../Govern/Users%20%26%20access%20control/Attribute-based%20access%20control.md)
>
> Use ABAC deny policies to restrict access to traces and datasets that contain personally identifiable information.

## Data retention & cleanup

Configure how long data is retained and how to delete it.

> [card] [Data purging for compliance](../Govern/Data%20%26%20compliance/Data%20purging%20for%20compliance.md)
>
> Set custom retention periods, delete traces by metadata, and meet deletion requirements.

> [card] [Data retention settings](../../Monitor/Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#data-retention)
>
> Understand base vs. extended retention tiers, auto-upgrades, and how retention affects billing.

## Cost controls and usage

Track and limit spending across your organization.

> [card] [Billing & spend limits](Billing%20%26%20usage/Manage%20billing%20in%20your%20account.md)
>
> Set monthly usage limits, track prepaid contract usage, and optimize tracing spend.

> [card] [Granular usage reporting](Billing%20%26%20usage/Granular%20billable%20usage.md)
>
> Break down trace usage by workspace, project, user, or API key to attribute costs across teams.

## Security & compliance

Review LangSmith's security posture and compliance certifications.

> [card] [Shared responsibility model](../Govern/Data%20%26%20compliance/LangSmith%20shared%20responsibility%20model.md)
>
> Review the security responsibilities shared between LangChain and your organization. LangSmith holds SOC 2 Type II, HIPAA, and GDPR certifications.

> [card] [Scalability & resilience](../Govern/Data%20%26%20compliance/Scalability%20%26%20resilience.md)
>
> Review SLA guarantees, disaster recovery strategies, and high availability configurations.
