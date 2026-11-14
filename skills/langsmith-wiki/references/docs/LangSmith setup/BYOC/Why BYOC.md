# Why BYOC

> Compare LangSmith BYOC with self-hosted LangSmith to decide which deployment model fits your organization.

BYOC is for organizations that want the data ownership and network isolation of self-hosting, without spending engineering time building and operating the full LangSmith platform themselves. The data plane stays in your AWS account, and LangChain manages the LangSmith infrastructure.

## What BYOC provides

* **Faster time to value**: You provision an AWS account and the required roles, and LangChain handles the rest of the provisioning flow.
* **Customer-owned data**: Databases, object storage, and compute run in infrastructure that you own.
* **Private networking**: The data plane runs inside your AWS account and can connect privately to your systems without exposing them publicly.
* **SaaS-aligned architecture**: The data plane is provisioned using a tried and tested architecture.
* **Monitoring out of the box**: LangChain has visibility into data plane health and metrics, and can proactively identify, investigate, and remediate issues.
* **Less platform maintenance**: Your engineering team spends more time driving value with LangSmith and less time managing LangSmith infrastructure, upgrades, scaling, and operational drift.
* **Automatic upgrades**: You receive automatic upgrades to a recent version of LangSmith.
* **Lower barrier to multi-environment and multi-region rollout**: Run multiple LangSmith data planes across environments, accounts, or regions without rebuilding the architecture from scratch each time.

## Compare BYOC and self-hosted

The table below compares the two deployment models:

| Dimension | BYOC | Self-hosted |
| - | - | - |
| **Primary value** | Customer-owned data plane with a managed LangSmith operating model | Maximum control over the full LangSmith deployment |
| **Time to value** | Faster: provision the account and role, then LangChain provisions the supported data plane architecture | Longer: you design, provision, connect, secure, and operate the full stack |
| **Operations** | LangChain owns more of the product operating model, upgrade path, and supportable infrastructure pattern | You own deployment, upgrades, scaling, monitoring, and incident response for the full stack |
| **Architecture** | Standardized and close to LangChain SaaS production architecture | More flexible, but easier to drift from supported patterns |
| **Best fit** | Teams that need data isolation and private networking, but do not want to operate every LangSmith component themselves | Teams that require full-stack ownership, unsupported infrastructure patterns, or cannot use a managed control plane |

## Move from self-hosted to BYOC

You can move to BYOC from an existing self-hosted deployment. Users, roles, datasets, experiments, prompts, annotation queue configuration, automation rules, and dashboards can be copied over. Trace migration is supported on AWS. Contact the LangChain team to arrange it.

To plan a migration, [contact our sales team](https://www.langchain.com/contact-sales).

## See also

* [BYOC overview](Bring%20Your%20Own%20Cloud%20%28BYOC%29.md)
* [BYOC architecture](AWS/BYOC%20architecture.md)
* [Self-hosted LangSmith](../Self-hosted/Self-hosted%20LangSmith.md)
