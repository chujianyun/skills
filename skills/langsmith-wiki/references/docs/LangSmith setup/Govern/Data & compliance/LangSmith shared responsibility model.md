# LangSmith shared responsibility model

> Overview of how LangChain and customers share security responsibilities for the LangSmith platform.

LangSmith is a multi-tenant SaaS product. Under the shared responsibility model, LangChain secures the platform infrastructure and application, and you secure your usage, data inputs, and the agents you build.

For the Bring Your Own Cloud (BYOC) equivalent, see the [BYOC shared responsibility model](../../BYOC/BYOC%20shared%20responsibility%20model.md).

## Responsibility matrix

| Domain | LangChain responsibility (provider) | Customer responsibility (user) |
| :- | :- | :- |
| **Infrastructure** | We manage the underlying cloud infrastructure (on AWS, Azure, or GCP, depending on your region), including servers, networking, OS patching, and capacity planning. The cloud provider owns the physical data centers. | N/A. You do not provision or maintain compute resources in the SaaS environment. |
| **Application** | We secure the LangSmith application code, API endpoints, and database clusters, including code scanning and penetration testing. | You are responsible for the security and safety of the AI chains and agents you build using our SDKs. |
| **Data** | We enforce tenant isolation and encrypt data at rest using AES-256 and in transit using TLS 1.2 or higher. | You control what data is sent to us and must filter sensitive PII via the SDK before it leaves your environment. |
| **Identity** | We provide the guardrails, including SSO/SCIM, MFA enforcement options, and RBAC frameworks. | You manage your user roster, assign roles (e.g., Admin vs. Viewer), and revoke access for terminated employees. |
| **Secrets** | We securely store the secrets you entrust to the platform. | You are responsible for rotating your API keys and ensuring they are not hard-coded in your applications. |

## LangChain responsibilities (the platform)

* We maintain SOC 2 Type II, GDPR, and HIPAA compliance and undergo annual third-party audits and penetration testing.
* We manage all underlying infrastructure on Amazon Web Services (AWS), Microsoft Azure, and Google Cloud Platform (GCP), including network firewalls, DDoS protection, and container security.
* We maintain high availability in accordance with our SLA, maintain daily backups, and handle disaster recovery for the LangSmith service.
* We patch confirmed platform vulnerabilities within strict service level agreements, with critical severity issues remediated in less than 2 weeks and high severity issues within 30 days.
* We encrypt all customer data at rest using AES-256 and in transit using TLS 1.2 or higher.

## Customer responsibilities (the usage)

* You must enforce least privilege access and immediately remove access for employees who leave your organization.
* You must ensure no prohibited data, such as PCI DSS cardholder data, is sent to the platform and use the masking features in the SDK to redact PII at the source.
* You are responsible for the security of the environment where you run the LangChain SDK, including your laptops and servers.
* You must rotate your API keys periodically and ensure they are stored in environment variables rather than hard-coded in your source code.

## Customer security best practices

To align with the security assumptions in our SOC 2 Type II framework, we recommend customers maintain the following internal guidelines:

* Maintain up-to-date technical and security contact details in your tenant settings so our team can reach you during an incident.
* Cycle your keys immediately via the self-serve portal if you suspect a compromise. You can always reach out to the LangChain security team if you have questions or need assistance with a breach.
* Develop a disaster recovery plan for your specific application to handle scenarios where the LangSmith service may be unavailable.
* Ensure that workstations and endpoints used to access the LangSmith UI are regularly patched and secured.
