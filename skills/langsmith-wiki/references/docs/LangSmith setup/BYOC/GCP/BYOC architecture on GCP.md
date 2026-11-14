# BYOC architecture on GCP

> What LangSmith BYOC deploys in your GCP project, how the data plane connects to the LangChain control plane, and the access LangSmith gets in your project.

BYOC on GCP runs the LangSmith data plane in your GCP project, while LangChain runs the control plane in its own GCP environment in `us-central1`. Your trace data stays in your project. This page describes what LangSmith deploys, how traffic flows, and the access LangSmith gets in your project. For BYOC on AWS, see [BYOC architecture](../AWS/BYOC%20architecture.md).

> [!NOTE]
>
> BYOC on GCP is in [beta](../../Cloud/Reference/Release%20stages.md). Resources and permissions can change between releases. The values on this page are the current defaults.

To set up a data plane, follow [BYOC onboarding on GCP](BYOC%20onboarding%20on%20GCP.md).

![BYOC architecture diagram for GCP. The LangSmith UI and the client apps in your application VPC reach the data plane over VPC peering or Cloud VPN, which terminates at an internal load balancer. The load balancer feeds an Istio ingress in a GKE cluster in your Google Cloud project, which routes to the LangSmith services that run the backend, SmithDB, and sandboxes, and those services read and write Cloud Storage, Cloud SQL, and Memorystore. The LangChain cloud control plane in us-central1 holds Crossplane, on-call engineers, alerting, and the LangSmith control plane services. Crossplane reaches the cluster through the GKE DNS endpoint with IAM for scaling and upgrades, the data plane sends auth and telemetry back over Private Service Connect, and the control plane impersonates a service account in your project to provision resources.](../../../../assets/images/4827b1139863-byoc-architecture-gcp.png)

## What gets deployed

LangSmith creates the following in your GCP project:

* **Network**: A VPC with a GKE subnet, Cloud NAT with a static egress IP address, and private services access.
* **GKE**: A regional, private GKE Standard cluster with Workload Identity and shielded nodes.
* **Cloud SQL for PostgreSQL**: One instance for LangSmith and one for the SmithDB metastore. Private IP only, high availability, TLS, and IAM database login, so no database password exists.
* **Memorystore for Redis Cluster**: TLS and IAM auth, reached through Private Service Connect.
* **Cloud Storage**: A bucket with public access prevention enforced.
* **DNS and ingress**: Cloud DNS zones for the data plane hostname, cert-manager with Let's Encrypt, External Secrets with Secret Manager, and an Istio ingress gateway.
* **Private Service Connect**: An endpoint to LangSmith, so the data plane reaches the control plane without the internet.

> [!NOTE]
>
> GCP data planes store and query traces in [SmithDB](../../Self-hosted/SmithDB/Overview/Enable%20SmithDB%20on%20self-hosted%20LangSmith.md), and do not run ClickHouse.

## How traffic flows

1. **Users to the data plane**: Users reach `https://<first 8 characters of the data plane ID>.gcp.langchain-byoc.com`. The hostname points at the Istio ingress gateway on a public or internal load balancer, which you choose when you create the data plane.
2. **Data plane to control plane**: The data plane reaches the LangSmith API at `us-central1.p.api.smith.langchain.com` through a Private Service Connect endpoint in its VPC. This path carries the heartbeat, sign-in and auth calls, and telemetry. It does not use the internet.
3. **Control plane to GCP APIs**: The control plane acts as one LangChain identity, `byoc-crossplane@langchain-prod.iam.gserviceaccount.com`. It impersonates your provisioner service account, so every GCP API call in your project is made as the provisioner. The LangSmith API writes the data plane secrets to Secret Manager, and Crossplane creates, updates, and deletes the other resources.
4. **Control plane to GKE**: Crossplane installs and updates the in-cluster resources through the cluster's DNS-based control plane endpoint. Each request needs a Google token for an identity with access to the cluster. Crossplane's Helm and Kubernetes providers cannot impersonate the provisioner, so the control plane service account itself holds `roles/container.admin`. Your Terraform module grants it only on GKE clusters tagged `managed_by: langsmith`, and LangSmith tags each data plane cluster when it creates it.
5. **DNS delegation**: The control plane writes the NS delegation for the data plane hostname in LangChain's parent zone, `gcp.langchain-byoc.com`. This record is in LangChain's project, not yours.

## Create and delete lifecycle

1. Your Terraform creates the provisioner service account and its roles, creates the `managed_by: langsmith` tag, and lets the control plane service account impersonate the provisioner.
2. You create the data plane with the API.
3. The control plane checks its access, writes the data plane secrets to Secret Manager, and hands the data plane to Crossplane.
4. Crossplane builds the network, GKE, Cloud SQL, Memorystore, Cloud Storage, and DNS, tags the GKE cluster and the Cloud SQL instances `managed_by: langsmith`, then installs LangSmith.
5. The data plane sends a heartbeat, and LangSmith shows it as `active`.
6. When you delete the data plane, the control plane lifts deletion protection, Crossplane deletes the resources, and the control plane deletes the secrets. The Cloud Storage bucket and the Cloud SQL backups stay. For more information, see [What teardown keeps](BYOC%20onboarding%20on%20GCP.md#what-teardown-keeps).

## Network

All subnets come from the `vpc_cidr` you choose, a range from `/16` to `/18`. All have Private Google Access on.

| Range | Size | Use |
| - | - | - |
| GKE subnet | First `/20` | GKE nodes. Pods use the secondary range `192.168.0.0/18`, and services use `192.168.64.0/18`. |
| Endpoints subnet | `/24` | Private Service Connect endpoints for Memorystore. |
| Control plane endpoint subnet | `/24` | The Private Service Connect endpoint to the LangSmith control plane, in `us-central1`. |
| Private services access | `/20` | Peered to Google services for the Cloud SQL private IP. |

The VPC is one regional VPC with custom subnets. Cloud NAT uses one static external IP address, so you can allowlist the data plane, and logs errors only.

## Storage

None of the data stores has a public endpoint.

| Store | Configuration |
| - | - |
| Cloud SQL for PostgreSQL | Enterprise edition, regional with a standby in another zone, with automatic storage growth. Private IP only. TLS required. IAM database login, so no application password exists. Automated backups (7 kept) and point-in-time recovery (7 days). Deletion protection on. At teardown, Cloud SQL takes a final backup, kept for 365 days, and keeps the automated backups. Two instances: one holds the LangSmith database, the other the SmithDB metastore. |
| Memorystore for Redis Cluster | One shard with one replica. IAM auth and TLS. Reached through a Private Service Connect endpoint. Deletion protection on. |
| Cloud Storage | One regional bucket for LangSmith blobs and SmithDB data. Uniform bucket-level access, with public access prevention enforced. Lifecycle rules delete objects under the TTL prefixes. Teardown keeps the bucket and its objects. |
| Secret Manager | Regional secrets for the data plane configuration and Postgres, plus one for sandboxes when they are enabled. Labeled with the data plane ID. The control plane writes them at create and deletes them at teardown. |

## GKE and compute

* **Cluster**: A regional GKE Standard cluster on the `REGULAR` release channel. Nodes repair and upgrade automatically.
* **Private cluster**: Private nodes and a private IP endpoint, with global access inside the VPC.
* **DNS-based control plane endpoint**: Accepts external traffic, and requires IAM: a Google token with `container.clusters.connect`, then Kubernetes RBAC. The kubeconfig that LangSmith keeps holds no credentials.
* **Workload Identity**: Enabled with the GKE metadata server on every node pool, so pods never see node credentials.
* **Dataplane V2**: Enforces Kubernetes NetworkPolicy.
* **Shielded nodes**: Secure Boot and integrity monitoring on every pool, with no kubelet read-only port.
* **Security posture**: Basic image vulnerability scanning. System metrics only, with Managed Service for Prometheus off.
* **Deletion protection**: On. Teardown lifts it first.
* **Node service accounts**: GKE's default node pool is removed, and no pool runs as the project's default Compute Engine service account.

The cluster runs a system node pool for platform workloads, and node auto-provisioning for the application. With `sandboxes_enabled`, it also runs a sandbox node pool with nested virtualization, tainted for sandbox hosts only and with its own node service account. Sandboxes cannot reach the metadata server.

Not on by default: application-layer Secrets encryption with your Cloud KMS key, Binary Authorization, and Confidential GKE Nodes.

## In-cluster resources

* **LangSmith**: The LangSmith Helm chart, with SmithDB. Every LangSmith pod runs as the workload service account through Workload Identity. SmithDB reaches its metastore instance through a Cloud SQL Auth Proxy sidecar.
* **KEDA**: Autoscales the LangSmith services.
* **External Secrets Operator**: A ClusterSecretStore on Secret Manager, usable only from the LangSmith namespace. It syncs the data plane secrets every hour.
* **cert-manager and trust-manager**: cert-manager uses a Let's Encrypt issuer with DNS-01 challenges in the data plane zones only. trust-manager builds one CA bundle with the public CAs and the Cloud SQL and Memorystore CAs.
* **Istio**: Base, istiod, and the ingress gateway.
* **Postgres setup job**: Creates the databases and the IAM database user, and grants it the database owner roles. It keeps no password.

## DNS and ingress

* **Hostname**: `<first 8 characters of the data plane ID>.gcp.langchain-byoc.com`. LangChain owns the parent zone.
* **Public zone**: A public Cloud DNS zone for the hostname in your project, which LangChain delegates from the parent zone.
* **Public endpoint**: An external passthrough load balancer. The hostname resolves on the internet.
* **Internal endpoint** (default): An internal passthrough load balancer in the GKE subnet, with global access. The address record is in a private zone, visible only in the data plane VPC, so the private address is never published. The public zone stays for the delegation and the certificate challenges.
* **TLS**: A Let's Encrypt certificate. HTTP redirects to HTTPS.
* **Gateway hardening**: The gateway normalizes paths before routing, rejects request bodies over 100 MiB, limits requests per gateway pod, and denies `TRACE`, `TRACK`, and `CONNECT`.
* **Control plane paths**: Paths such as sign-in are forwarded to the control plane over Private Service Connect.

## Private Service Connect

* LangChain publishes a service attachment in `us-central1`. LangSmith automatically adds your project to its accept list during data plane provisioning. No manual project allowlisting is required.
* The data plane creates the endpoint: an internal address in the control plane endpoint subnet, and a forwarding rule to the service attachment. Data planes in other regions reach the endpoint through global access.
* A private DNS zone for `us-central1.p.api.smith.langchain.com`, visible only in the data plane VPC, points at the endpoint.
* Private Service Connect carries traffic from the data plane to the control plane only. The control plane reaches the cluster through the GKE DNS-based endpoint.

## Access and permissions

### Terraform module resources

The [`langsmith-byoc-service-account` Terraform module](https://github.com/langchain-ai/terraform/tree/main/modules/byoc/gcp/langsmith-byoc-service-account) creates the following in your project:

| Resource | What it does |
| - | - |
| `langsmith-byoc-provisioner` service account | The service account LangSmith provisions as. Its description is your external ID. |
| Token Creator on the provisioner | Lets `byoc-crossplane@langchain-prod.iam.gserviceaccount.com` impersonate the provisioner. No other LangChain identity is trusted. |
| `langsmithByocProvisioner` custom role | The permissions to create, update, and delete data plane resources that a name condition cannot limit, bound on the project. |
| `langsmithByocNamed<Kind>` custom roles | One role per resource kind: Cloud SQL instances, GKE clusters, networks, subnets, Cloud Routers, addresses, forwarding rules, Memorystore for Redis clusters, service connection policies, Cloud Storage, and Secret Manager. Each is bound with an IAM condition on the resource name, so the provisioner can create, change, and delete only resources whose names start with `langsmith-`, and secrets whose IDs start with `ls-`. |
| `managed_by: langsmith` tag | A project tag. The provisioner can bind it only to GKE clusters and Cloud SQL instances whose names start with `langsmith-`. |
| `roles/container.admin` for the control plane | Granted to `byoc-crossplane@langchain-prod.iam.gserviceaccount.com` with the condition that the cluster has the `managed_by: langsmith` tag. It covers the GKE API and the Kubernetes API. |
| `langsmithByocClusterConnect` custom role | `container.clusters.connect` for the control plane service account, limited to clusters whose names start with `langsmith-`. The DNS-based endpoint checks it without the cluster's tags. Connecting gives no access inside a cluster. |
| `langsmithByocProjectIamGranter` custom role | `resourcemanager.projects.getIamPolicy` and `setIamPolicy`. An IAM condition lets the provisioner add or remove only these project roles: `artifactregistry.reader`, `cloudsql.admin`, `cloudsql.client`, `cloudsql.instanceUser`, `container.defaultNodeServiceAccount`, `redis.dbConnectionUser`, and `secretmanager.secretAccessor`. The condition limits which roles, not to whom. |
| `langsmithByocServiceAccountUser` custom role | `iam.serviceAccounts.actAs`, so GKE nodes and workloads can run as the data plane service accounts. IAM does not evaluate conditions for `actAs`, so this binding has none. |
| Project APIs | With `enable_apis` (default `true`): Compute Engine, GKE, Cloud DNS, IAM, IAM Service Account Credentials, Network Connectivity, Memorystore for Redis, Secret Manager, Service Directory, Service Networking, and Cloud SQL Admin. |

The custom role ID prefix is `langsmithByoc` by default. Set `custom_role_id_prefix` if the project already has roles with those IDs. Apply one copy of the module per project, because it creates the project's `managed_by` tag key. For the full permission list of each role, see the module's [README](https://github.com/langchain-ai/terraform/tree/main/modules/byoc/gcp/langsmith-byoc-service-account) and source.

### Checks at create

The control plane stops the create when one of these checks fails:

* It can impersonate the provisioner, and the provisioner has `resourcemanager.projects.get`, `secretmanager.secrets.create`, and `secretmanager.secrets.delete` on the project. It runs the same check before a delete.
* The provisioner is in the data plane project.
* The provisioner's description is your organization's external ID. Every customer's provisioner trusts the same control plane service account, so this check stops another LangSmith organization from using your provisioner.
* With `byoiam_enabled`, the project has the six service accounts listed in [Data plane service accounts](#data-plane-service-accounts).

### Data plane service accounts

Crossplane creates one Google service account per workload class for each data plane, and binds it to its Kubernetes service accounts with Workload Identity (`roles/iam.workloadIdentityUser`). With `byo_iam`, your Terraform creates them with fixed IDs, and all data planes in the project share them.

| Service account (default / `byo_iam`) | Used by | Roles |
| - | - | - |
| `lsa-<hash>` / `langsmith-workload` | LangSmith application and SmithDB | Project: `redis.dbConnectionUser`, `cloudsql.client`, `cloudsql.instanceUser`. Bucket: `storage.objectAdmin`. Token Creator on itself, to sign Cloud Storage URLs. |
| `lse-<hash>` / `langsmith-external-secrets` | External Secrets Operator | `secretmanager.secretAccessor`, with a condition for each of the data plane's secret IDs. With `byo_iam`: secrets whose IDs start with `ls-`. |
| `lsc-<hash>` / `langsmith-cert-manager` | cert-manager | `dns.admin` on the data plane's DNS zones only, never on the project. |
| `lsp-<hash>` / `langsmith-postgres-setup` | Postgres setup job | Project: `cloudsql.admin`, only on Cloud SQL instances tagged `managed_by: langsmith`. With `byo_iam`: `cloudsql.users.create`, `list`, and `update` (custom role `langsmithByocPostgresSetup`) on tagged instances, and `cloudsql.viewer` on instances whose names start with `langsmith-`. |
| `lsn-<hash>` / `langsmith-node` | GKE nodes | Project: `container.defaultNodeServiceAccount`, `artifactregistry.reader`. |
| `lsh-<hash>` / `langsmith-sandbox-host` | Sandbox nodes, with sandboxes enabled | Project: `container.defaultNodeServiceAccount`, `artifactregistry.reader`, `redis.dbConnectionUser`. Bucket: `storage.objectAdmin` on the `smithbox/` managed folder only. |

Your Terraform module grants `byoc-crossplane@langchain-prod.iam.gserviceaccount.com` its `roles/container.admin`, on tagged clusters only, with or without `byo_iam`. Crossplane makes no grant to it.

With `byo_iam`, do not give your own secrets in the project IDs that start with `ls-`, or External Secrets can read them.

### Bring your own IAM

Set `byo_iam = true` in the module before you create data planes in the project, and create the data plane with `byoiam_enabled` set to `true`. Use it when the project also holds resources that are not LangSmith's. Do not change `byo_iam` while data planes exist. With `byo_iam`:

* Your Terraform creates the six service accounts and their project roles.
* The provisioner role loses `iam.serviceAccounts.create`, `delete`, `update`, and `setIamPolicy`. It keeps `get`, `list`, and `getIamPolicy`.
* The module does not create the `ProjectIamGranter` or `ServiceAccountUser` roles, so the provisioner cannot change the project IAM policy.
* The provisioner gets `iam.serviceAccounts.getIamPolicy` and `setIamPolicy` (custom role `langsmithByocServiceAccountIamManager`) on the six accounts only, to add the Workload Identity bindings. It gets `roles/iam.serviceAccountUser` on `langsmith-node` and `langsmith-sandbox-host` only.
* LangSmith still grants `dns.admin` on the data plane zones to `langsmith-cert-manager`, because the zones do not exist before the data plane.

### What LangChain can and cannot access

* **Can**: Create, change, and delete the data plane resources through the provisioner, which for most kinds means resources whose names start with `langsmith-`. Read the project's IAM policy and service accounts. Act as cluster admin on GKE clusters tagged `managed_by: langsmith`, through `container.admin`. This is how LangSmith installs and upgrades the application.
* **Cannot, by role**: The provisioner has no `storage.objects.get`, so it cannot read objects in the bucket. It can list and delete them. It has no `secretmanager.versions.access`, so it cannot read secrets. It has no permissions on Cloud SQL databases or users, no database login permissions, and no permissions outside the project. The Postgres setup account's Cloud SQL permissions apply only to the data plane's instances, which LangSmith tags `managed_by: langsmith`, so it cannot manage users or settings on your other Cloud SQL instances.

These are limits of the provisioner's roles, not deny policies. The provisioner can still set IAM policies on `langsmith-` buckets, on every DNS zone and Artifact Registry repository in the project and, without `byo_iam`, on service accounts.

> [!WARNING]
>
> Use a project that holds only LangSmith resources. Name conditions limit the provisioner to `langsmith-` resources for most kinds, but not everywhere. If the project also holds other resources, `byo_iam` removes the service account and project role grant access below, but not the rest:
>
> * **Service accounts**: IAM checks a service account by its numeric unique ID, so a condition cannot limit service account permissions by account name. Without `byo_iam`, the provisioner's `setIamPolicy` and `actAs` apply to every service account in the project, so it could act as any of them.
> * **Project role grants**: Without `byo_iam`, the provisioner can grant the project roles listed above to any principal, including itself. With `cloudsql.admin` or `secretmanager.secretAccessor`, it could reach every Cloud SQL instance or secret in the project.
> * **DNS zones and Artifact Registry repositories**: The provisioner can change, delete, and set the IAM policy of any DNS zone and its records, and any Artifact Registry repository, in the project.
> * **Your own `langsmith-` resources**: The name conditions cannot tell your resources from LangSmith's if their names also start with `langsmith-`.

### Remove access

To remove LangChain's access to your project:

* **Recommended**: Delete the data plane in LangSmith. Wait until it is gone, then run `terraform destroy` if no other data planes use the project.
* **Immediate**: Remove the LangChain grants: the Token Creator binding on the provisioner (or the provisioner itself), and the tag-conditioned `roles/container.admin` and `langsmithByocClusterConnect` grants to `byoc-crossplane@langchain-prod.iam.gserviceaccount.com`. LangSmith then cannot change or delete the data plane. The resources stay, and you must delete them yourself.

## See also

* [BYOC onboarding on GCP](BYOC%20onboarding%20on%20GCP.md)
* [BYOC overview](../Bring%20Your%20Own%20Cloud%20%28BYOC%29.md)
* [BYOC shared responsibility model](../BYOC%20shared%20responsibility%20model.md)
