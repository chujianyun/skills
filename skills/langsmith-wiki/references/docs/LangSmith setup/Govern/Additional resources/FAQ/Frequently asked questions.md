# Frequently asked questions

## Observability

### *I can't create API keys or manage users in the UI, what's wrong?*

* You have likely deployed LangSmith without setting up SSO. LangSmith requires SSO to manage users and API keys. You can find more information on setting up SSO in the [configuration section.](../../../Self-hosted/Platform%20auth%20%26%20access%20control/Set%20up%20SSO%20with%20OAuth2.0%20and%20OIDC.md)

### *How does load balancing/ingress work*?

* You will need to expose the frontend container/service to your applications/users. This will handle routing to all downstream services.
* You will need to terminate SSL at the ingress level. We recommend using a managed service like AWS ALB, GCP Load Balancer, or Nginx.

### *How can we authenticate to the application?*

* Currently, our self-hosted solution supports SSO with OAuth2.0 and OIDC as an authn solution. Note, we do offer a no-auth solution but highly recommend setting up oauth before moving into production.

You can find more information on setting up SSO in the [configuration section.](../../../Self-hosted/Platform%20auth%20%26%20access%20control/Set%20up%20SSO%20with%20OAuth2.0%20and%20OIDC.md)

### *Can I use external storage services?*

* You can configure LangSmith to use external versions of all storage services. In a production setting, we strongly recommend using external storage services. Check out the [configuration section](../../../Self-hosted/Self-hosted%20LangSmith.md) for more information.

### *Does my application need egress to function properly?*

Our deployment only needs egress for a few things (most of which can reside within your VPC):

* Fetching images (If mirroring your images, this may not be needed)

* Talking to any LLM endpoints

* Talking to any external storage services you may have configured

* Fetching OAuth information

* Subscription Metrics and Operational Metadata (if not running in offline mode)

  * Requires egress to `https://beacon.langchain.com`
  * See [Egress](../../../Self-hosted/Configure%20an%20instance/Egress%20for%20billing%20and%20operational%20telemetry.md) for more information

Your VPC can set up rules to limit any other access. Note: We require the `X-Organization-Id` and `X-Tenant-Id` headers to be allowed to be passed through to the backend service. These are used to determine which organization and workspace (previously called "tenant") the request is for.

### *Resource requirements for the application?*

* In kubernetes, we recommend a minimum helm configuration which you can see in the [medium size example](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/examples/medium_size.yaml). For docker, we recommend a minimum of 16GB of RAM and 4 CPUs.
* For Postgres, we recommend a minimum of 8GB of RAM and 2 CPUs.
* For Redis, we recommend 4GB of RAM and 2 CPUs.
* For Clickhouse, we recommend 32GB of RAM and 8 CPUs.

### SAML SSO FAQs

#### *How do I change a SAML SSO user's email address?*

Some identity providers retain the original `User ID` through an email change while others do not, so we recommend that you follow these steps to avoid duplicate users in LangSmith:

1. Remove the user from the organization (see [manage users](../../Organization/Workspace%20setup/Set%20up%20hierarchy.md#manage-users))
2. Change their email address in the IdP
3. Have them login to LangSmith again via SAML SSO - this will trigger the usual [JIT provisioning](../../Users%20%26%20access%20control/User%20management.md#just-in-time-jit-provisioning) flow with their new email address

Changing email address via SCIM or otherwise is not currently supported for users with multiple linked login methods. This error message is shown: `email update not supported with linked login methods`. For example, if a user previously logged in via email/password or Google social login, and then is added with the same email address via SSO, changing their email address is not supported. This applies to both self-hosted and cloud.

#### *Can I change identity providers?*

Reach out to the LangChain support team through our portal at [https://support.langchain.com](https://support.langchain.com) for support on migration.

#### *How do I fix "405 method not allowed"?*

Ensure you're using the correct ACS URL: [https://auth.langchain.com/auth/v1/sso/saml/acs](https://auth.langchain.com/auth/v1/sso/saml/acs)

### SCIM FAQs

#### *Can I use SCIM without SAML SSO?*

* **Cloud**: No, SAML SSO is required for SCIM in cloud deployments
* **Self-hosted**: Yes, SCIM works with OAuth with Client Secret authentication mode

#### *What happens if I have both JIT provisioning and SCIM enabled?*

JIT provisioning and SCIM can conflict with each other. We recommend disabling JIT provisioning before enabling SCIM to ensure consistent user provisioning behavior.

#### *How do I change a user's role or workspace access?*

Update the user's group membership in your IdP. The changes will be synchronized to LangSmith according to the [role precedence rules](../../Users%20%26%20access%20control/User%20management.md#role-precedence).

#### *What happens when a user is removed from all groups?*

The user will be deprovisioned from your LangSmith organization according to your IdP's deprovisioning settings.

#### *Can I use custom group names?*

Yes. If your identity provider supports syncing alternate fields to the `displayName` group attribute, you may use an alternate attribute (like `description`) as the `displayName` in LangSmith and retain full customizability of the identity provider group name. Otherwise, groups must follow the specific naming convention described in the [Group Naming Convention](../../Users%20%26%20access%20control/User%20management.md#group-naming-convention) section to properly map to LangSmith roles and workspaces.

A group can also use any name and map to a [team](../../Users%20%26%20access%20control/Teams.md#sync-team-members-from-your-identity-provider). Enter the group's name as the team's IdP group, and the team's workspace access applies to the group's members.

You can also [configure a custom separator](../../Users%20%26%20access%20control/User%20management.md#configure-custom-separator) (e.g., `-`, `_`, `&`) instead of the default colon (`:`) to accommodate identity providers with restrictions on group name characters.

#### *Why is my Okta integration not working?*

See Okta's troubleshooting guide here: [https://help.okta.com/en-us/content/topics/users-groups-profiles/usgp-group-push-troubleshoot.htm](https://help.okta.com/en-us/content/topics/users-groups-profiles/usgp-group-push-troubleshoot.htm).

### *Are downgrades supported?*

Downgrades are not officially supported. LangSmith upgrades may include database migrations and other changes that are not backward-compatible. If you need to roll back to a previous version, contact technical support via the [Support Portal](https://support.langchain.com) for guidance.

## Deployment

### Do I need to use LangChain to use LangGraph? what's the difference?

No. LangGraph is an orchestration framework for complex agentic systems and is more low-level and controllable than LangChain agents. LangChain provides a standard interface to interact with models and other components, useful for straight-forward chains and retrieval flows.

### How is LangGraph different from other agent frameworks?

Other agentic frameworks can work for simple, generic tasks but fall short for complex tasks bespoke to a company’s needs. LangGraph provides a more expressive framework to handle companies’ unique tasks without restricting users to a single black-box cognitive architecture.

### Does LangGraph impact the performance of my app?

LangGraph will not add any overhead to your code and is specifically designed with streaming workflows in mind.

### Is LangGraph open source? is it free?

Yes. LangGraph is an MIT-licensed open-source library and is free to use.

### How are LangGraph and LangSmith different?

LangGraph is a stateful, orchestration framework that brings added control to agent workflows. LangSmith is a service for deploying and scaling agentic applications, with an opinionated API for building agent UXs, plus an integrated developer UI.

| Features | LangGraph (open source) | LangSmith |
| - | - | - |
| Description | Stateful orchestration framework for agentic applications | Scalable infrastructure for deploying LangGraph applications |
| SDKs | Python and JavaScript | Python and JavaScript |
| HTTP APIs | None | Yes - useful for retrieving & updating state or long-term memory, or creating a configurable assistant |
| Streaming | Basic | Dedicated mode for token-by-token messages |
| Checkpointer | Community contributed | Supported out-of-the-box |
| Persistence Layer | Self-managed | Managed Postgres with efficient storage |
| Deployment | Self-managed | • Cloud  • Free self-hosted  • Enterprise (paid self-hosted) |
| Scalability | Self-managed | Auto-scaling of task queues and servers |
| Fault-tolerance | Self-managed | Automated retries |
| Concurrency Control | Simple threading | Supports double-texting |
| Scheduling | None | Cron scheduling |
| Monitoring | None | Integrated with LangSmith for observability |
| IDE integration | Studio | Studio |

### Is LangSmith open source?

No. LangSmith is proprietary software.

For more information, see our [LangSmith pricing page](https://www.langchain.com/pricing).

### Does LangGraph work with LLMs that do not support tool calling?

Yes! You can use LangGraph with any LLMs. The main reason we use LLMs that support tool calling is that this is often the most convenient way to have the LLM make its decision about what to do. If your LLM does not support tool calling, you can still use it - you just need to write a bit of logic to convert the raw LLM string response to a decision about what to do.

### Does LangGraph work with OSS LLMs?

Yes! LangGraph is totally ambivalent to what LLMs are used under the hood. The main reason we use closed LLMs in most of the tutorials is that they seamlessly support tool calling, while OSS LLMs often don't. But tool calling is not necessary (see [Does LangGraph work with LLMs that do not support tool calling?](#does-langgraph-work-with-llms-that-do-not-support-tool-calling)) so you can totally use LangGraph with OSS LLMs.

### Can I use Studio without logging in to LangSmith?

Yes! You can use the [development version of Agent Server](../../../../Deploy/Get%20started/Develop%20%26%20test/Local%20development%20%26%20testing.md) to run the backend locally.
This will connect to the Studio frontend hosted as part of LangSmith.
If you set an environment variable of `LANGSMITH_TRACING=false`, then no traces will be sent to LangSmith.

### What is a Deployment Run?

A Deployment Run is one end-to-end invocation of a LangGraph agent deployed via LangSmith Agent Server. Nodes and subgraphs are not charged separately. Calls to other LangGraph agents (through RemoteGraph or the LangGraph SDK or the API directly) are charged separately, to the deployment that hosts the agent being called. An interrupt for human-in-the-loop creates a separate Deployment Run when resuming.
