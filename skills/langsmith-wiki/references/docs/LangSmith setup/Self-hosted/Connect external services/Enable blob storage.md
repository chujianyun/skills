# Enable blob storage

By default, LangSmith stores run inputs, outputs, errors, manifests, extras, and events in ClickHouse. If you so choose, you can instead store this information in blob storage, which has a couple of notable benefits. For the best results in production deployments, we **strongly** recommend using blob storage, which offers the following benefits:

1. In high trace environments, inputs, outputs, errors, manifests, extras, and events may balloon the size of your databases.
2. If using LangSmith Managed ClickHouse, you may want sensitive information in blob storage that resides in your environment. To alleviate this, LangSmith supports storing run inputs, outputs, errors, manifests, extras, events, and attachments in an external blob storage system.

> [!TIP]
>
> **For cloud-specific setup**, choose your platform:
>
> * [Amazon S3 (AWS)](#amazon-s3)
> * [Google Cloud Storage (GCP)](#google-cloud-storage)
> * [Azure Blob Storage](#azure-blob-storage)
> * [Neon Object Storage](#neon-object-storage)
>
> For complete cloud-specific setup and architecture guides, see [AWS](../Get%20started%20by%20cloud%20provider/Self-hosted%20LangSmith%20on%20AWS.md), [GCP](../Get%20started%20by%20cloud%20provider/Self-hosted%20LangSmith%20on%20GCP.md), or [Azure](../Get%20started%20by%20cloud%20provider/Self-hosted%20LangSmith%20on%20Azure.md).

## Requirements

> [!NOTE]
>
> Azure blob storage is available in Helm chart versions 0.8.9 and greater. [Deleting trace projects](../../../Monitor/Trace/Observability%20concepts.md#data-retention) is supported in Azure starting in Helm chart version 0.10.43.
>
> Native GCS blob storage engine support (using `engine: "GCS"`) is available in Helm chart versions 0.13.29 and greater. For earlier versions, GCS is supported via the S3-compatible API by setting `engine: "S3"` with HMAC credentials.

* Access to a valid blob storage service

  * [Amazon S3](https://aws.amazon.com/s3/)
  * [Google Cloud Storage (GCS)](https://cloud.google.com/storage?hl=en)
  * [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs)
  * [Neon Object Storage](https://neon.com/docs/storage/get-started) (S3-compatible)

* A bucket/directory in your blob storage to store the data. We highly recommend creating a separate bucket/directory for LangSmith data.
  * **If you are using TTLs**, you will need to set up a lifecycle policy to delete old data. For more information, see [configuring TTLs](../Configure%20an%20instance/Enable%20TTL%20and%20data%20retention.md). These policies should mirror the TTLs you have set in your LangSmith configuration, or you may experience data loss. See [TTL configuration for blob storage](#ttl-configuration) for how to set up the lifecycle rules.

* Credentials to permit LangSmith Services to access the bucket/directory
  * You will need to provide your LangSmith instance with the necessary credentials to access the bucket/directory. Read the authentication [section](#authentication) below for more information.

* If using S3 or GCS, an API URL for your blob storage service

  * This will be the URL that LangSmith uses to access your blob storage system
  * For Amazon S3, this will be the URL of the S3 endpoint. Something like: `https://s3.amazonaws.com` or `https://s3.us-west-1.amazonaws.com` if using a regional endpoint.
  * For Google Cloud Storage, this will be the URL of the GCS endpoint. Something like: `https://storage.googleapis.com`
  * For Neon Object Storage, this is the storage endpoint of your Neon branch. Something like: `https://br-cool-darkness-a1b2c3d4.storage.c-1.us-east-2.aws.neon.tech`

## Authentication

> [tab] AWS
>
> ### Amazon S3
>
> To authenticate to [Amazon S3](https://aws.amazon.com/s3/), you will need to create an IAM policy granting the following permissions on your bucket.
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "Version": "2012-10-17",
>   "Statement": [
>     {
>       "Effect": "Allow",
>       "Action": [
>         "s3:GetObject",
>         "s3:PutObject",
>         "s3:DeleteObject",
>         "s3:ListBucket"
>       ],
>       "Resource": [
>         "arn:aws:s3:::your-bucket-name",
>         "arn:aws:s3:::your-bucket-name/*"
>       ]
>     }
>   ]
> }
> ```
>
> Once you have the correct policy, there are three ways to authenticate with Amazon S3:
>
> 1. [IAM Roles for Service Accounts (IRSA)](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) (Recommended): You can create an IAM role for your LangSmith instance and attach the policy to that role. This is the recommended way to authenticate with Amazon S3 in production.
>    1. You will need to create an IAM role with the policy attached.
>    2. You will need to allow LangSmith service accounts to assume the role. The `langsmith-queue`, `langsmith-backend`, `langsmith-platform-backend`, and `langsmith-ingest-queue` service accounts will need to be able to assume the role.
>       > [!WARNING]
>       >
>       > The service account names will be different if you are using a custom release name. You can find the service account names by running `kubectl get serviceaccounts` in your cluster.
>    3. You will need to provide the role ARN to LangSmith. You can do this by adding the `eks.amazonaws.com/role-arn: "<role_arn>"` annotation to the `queue`, `backend`, `platform-backend`, and `ingest-queue` services in your Helm Chart installation.
> 2. [Access Key and Secret Key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html): You can provide LangSmith with an access key and secret key. This is the simplest way to authenticate with Amazon S3. However, it is not recommended for production use as it is less secure.
>    1. You will need to create a user with the policy attached. Then you can provision an access key and secret key for that user.
> 3. [VPC Endpoint Access](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html): You can enable access to your S3 bucket via a VPC endpoint, which allows traffic to flow securely from your VPC to your S3 bucket.
>    1. You'll need to provision a VPC endpoint and configure it to allow access to your S3 bucket.
>    2. You can refer to our [public Terraform modules](https://github.com/langchain-ai/terraform/tree/main/modules/aws) for guidance and an example of configuring this.
>
> ### KMS encryption header support
>
> Starting with LangSmith Helm chart version **0.11.24**, you can pass a KMS encryption key header and enforce a specific KMS key for writes by providing its ARN. To enable this, set the following values in your Helm chart:
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> config:
>   blobStorage:
>     kmsEncryptionEnabled: true
>     kmsKeyArn: <your_kms_key_arn>
> ```

> [tab] GCP
>
> ### Google Cloud Storage
>
> To authenticate with [Google Cloud Storage](https://cloud.google.com/storage?hl=en), you will need to create a [`service account`](https://cloud.google.com/iam/docs/service-account-overview) with the necessary permissions to access your bucket.
>
> Your service account will need the `Storage Admin` role or a custom role with equivalent permissions. This can be scoped to the bucket that LangSmith will be using.
>
> Once you have a provisioned service account, you will need to generate a [`HMAC key`](https://cloud.google.com/storage/docs/authentication/hmackeys) for that service account. This key and secret will be used to authenticate with Google Cloud Storage.
>
> > [!NOTE]
> >
> > As of Helm chart version **0.13.29**, you can set the blob storage engine to `"GCS"` directly. This supports two authentication methods:
> >
> > 1. **GCP Workload Identity (recommended)**: Leave `accessKey` and `accessKeySecret` empty. LangSmith will use [Application Default Credentials](https://cloud.google.com/docs/authentication/application-default-credentials). You will need to add the workload identity annotation to the `backend`, `platform-backend`, `queue`, and `ingest-queue` service accounts.
> > 2. **HMAC keys**: Set `accessKey` and `accessKeySecret` to your GCS [HMAC credentials](https://cloud.google.com/storage/docs/authentication/hmackeys).
> >
> > For both methods, set `apiURL` to `https://storage.googleapis.com` and `bucketName` to your GCS bucket name.
> >
> > For Helm chart versions prior to 0.13.29, GCS is supported via the S3-compatible API by setting `engine: "S3"` with HMAC credentials.

> [tab] Azure
>
> ### Azure Blob Storage
>
> To authenticate with [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs), you will need to use one of the following methods to grant LangSmith workloads permission to access your [container](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction#containers) (listed in order of precedence):
>
> 1. [Storage account and access key](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage)
> 2. [Connection string](https://learn.microsoft.com/en-us/azure/storage/common/storage-configure-connection-string)
> 3. [Workload identity](https://azure.github.io/azure-workload-identity/docs/introduction.html) (recommended), managed identity, or environment variables supported by [`DefaultAzureCredential`](https://learn.microsoft.com/en-us/azure/developer/go/azure-sdk-authentication?tabs=bash#2-authenticate-with-azure). This is the default authentication method when configuration for either option above is not present.
>    1. To use workload identity, add the label `azure.workload.identity/use: true` to the `queue`, `backend`, `platform-backend`, and `ingest-queue` deployments. Additionally, add the `azure.workload.identity/client-id` annotation to the corresponding service accounts, which should be an existing Azure AD Application's client ID or user-assigned managed identity's client ID. See [Azure's documentation](https://azure.github.io/azure-workload-identity/docs/topics/service-account-labels-and-annotations.html) for additional details.
>
> > [!NOTE]
> >
> > Some deployments may need further customization of the connection configuration using a Service URL Override instead of the default service URL (`https://<storage_account_name>.blob.core.windows.net/`). For example, this override is necessary in order to use a different blob storage domain (e.g. government or china).

> [tab] Neon
>
> ### Neon Object Storage
>
> [Neon Object Storage](https://neon.com/docs/storage/get-started) is S3-compatible object storage attached to a Neon branch. LangSmith connects to it with the `S3` engine and an access key and secret key.
>
> To set up Neon Object Storage for LangSmith:
>
> 1. Create a private bucket on your Neon branch, for example `langsmith`. For more information, see [Neon buckets](https://neon.com/docs/storage/buckets).
>
> 2. Create a credential with both the `storage:read` and `storage:write` scopes. LangSmith reads, writes, and deletes objects, so it needs both scopes:
>
>    ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
>    neon credentials create --scope storage:read --scope storage:write --name langsmith-blob-storage
>    ```
>
> 3. Use the credential's `token_id` (starts with `nak_live_`) as `accessKey` and its `s3_secret_access_key` (starts with `nsk_live_`) as `accessKeySecret`. For more information, see [Neon Object Storage authentication](https://neon.com/docs/storage/authentication).
>
> 4. Use the branch's storage endpoint as `apiURL`. In the Neon Console, click **Connect** and open the **Storage** tab to find it as `AWS_ENDPOINT_URL_S3`.
>
> 5. Set `s3UsePathStyle: true` in your [configuration](#configuration):
>
>    ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
>    config:
>      blobStorage:
>        enabled: true
>        engine: "S3"
>        bucketName: "langsmith"
>        apiURL: "https://br-cool-darkness-a1b2c3d4.storage.c-1.us-east-2.aws.neon.tech"
>        accessKey: "nak_live_..."
>        accessKeySecret: "<SECRET>"
>        s3UsePathStyle: true
>    ```
>
> > [!WARNING]
> >
> > Neon Object Storage serves buckets at path-style URLs only (`<apiURL>/<bucket>/<key>`). Without `s3UsePathStyle: true`, LangSmith sends requests to `<bucket>.<endpoint>`, which fail TLS verification because the Neon certificate does not cover that hostname. `s3UsePathStyle` requires Helm chart version 0.12.4 or later.
>
> Neon does not run lifecycle rules, so plan how to expire data before you enable [TTLs](#ttl-configuration). For more information, see [Neon Object Storage lifecycle rules](#neon-object-storage-lifecycle-rules).

## CH search

By default, LangSmith will still store tokens for search in ClickHouse. If you are using LangSmith Managed Clickhouse, you may want to disable this feature to avoid sending potentially sensitive information to ClickHouse. You can do this in your blob storage configuration.

## Configuration

After creating your bucket and obtaining the necessary credentials, you can configure LangSmith to use your blob storage system.

```yaml Helm
config:
  blobStorage:
    enabled: true
    engine: "S3" # Or "GCS" or "Azure". This is case-sensitive.
    chSearchEnabled: true # Set to false if you want to disable CH search (Recommended for LangSmith Managed Clickhouse)
    bucketName: "your-bucket-name"
    apiURL: "Your connection url"
    accessKey: "Your access key" # Optional. Only required if using S3 access key and secret key
    accessKeySecret: "<API_KEY>" # Optional. Only required if using access key and secret key
    s3UsePathStyle: false # Optional. Set to true for S3-compatible services that require path-style URLs, such as Neon Object Storage or MinIO
    # The following blob storage configuration values are for Azure and require blobStorage.engine = "Azure". Omit otherwise.
    azureStorageAccountName: "Your storage account name" # Optional. Only required if using storage account and access key.
    azureStorageAccountKey: "Your storage account access key" # Optional. Only required if using storage account and access key.
    azureStorageContainerName: "your-container-name" # Required
    azureStorageConnectionString: "" # Optional.
    azureStorageServiceUrlOverride: "" # Optional
  backend: # Optional, only required if using IAM role for service account on AWS, workload identity on GKE, or workload identity on AKS
    deployment: # Azure only
      labels:
        azure.workload.identity/use: true
    serviceAccount:
      annotations:
        azure.workload.identity/client-id: "<client_id>" # Azure only
        eks.amazonaws.com/role-arn: "<role_arn>" # AWS only
        iam.gke.io/gcp-service-account: "<gsa_name>@<project_id>.iam.gserviceaccount.com" # GCP only
  platformBackend: # Optional, only required if using IAM role for service account on AWS, workload identity on GKE, or workload identity on AKS
    deployment: # Azure only
      labels:
        azure.workload.identity/use: true
    serviceAccount:
      annotations:
        azure.workload.identity/client-id: "<client_id>" # Azure only
        eks.amazonaws.com/role-arn: "<role_arn>" # AWS only
        iam.gke.io/gcp-service-account: "<gsa_name>@<project_id>.iam.gserviceaccount.com" # GCP only
  queue: # Optional, only required if using IAM role for service account on AWS, workload identity on GKE, or workload identity on AKS
    deployment: # Azure only
      labels:
        azure.workload.identity/use: true
    serviceAccount:
      annotations:
        azure.workload.identity/client-id: "<client_id>" # Azure only
        eks.amazonaws.com/role-arn: "<role_arn>" # AWS only
        iam.gke.io/gcp-service-account: "<gsa_name>@<project_id>.iam.gserviceaccount.com" # GCP only
  ingestQueue: # Optional, only required if using IAM role for service account on AWS, workload identity on GKE, or workload identity on AKS
    deployment: # Azure only
      labels:
        azure.workload.identity/use: true
    serviceAccount:
      annotations:
        azure.workload.identity/client-id: "<client_id>" # Azure only
        eks.amazonaws.com/role-arn: "<role_arn>" # AWS only
        iam.gke.io/gcp-service-account: "<gsa_name>@<project_id>.iam.gserviceaccount.com" # GCP only
```

> [!NOTE]
>
> If using an access key and secret, you can also provide an existing Kubernetes secret that contains the authentication information. This is recommended over providing the access key and secret key directly in your config. See the [generated secret template](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/templates/secrets.yaml) for the expected secret keys.

## TTL configuration

If using the [TTL](../Configure%20an%20instance/Enable%20TTL%20and%20data%20retention.md) feature with LangSmith, you'll also have to configure TTL rules for your blob storage. Trace information stored on blob storage is stored on a particular prefix path, which determines the TTL for the data. When a trace's retention is extended, its corresponding blob storage path changes to ensure that it matches the new extended retention.

The following TTL prefixes are used:

* `ttl_s/`: Short term (base) TTL, configured for 14 days.
* `ttl_l/`: Long term (extended) TTL, configured for 400 days by default.

### Custom workspace-level retention prefixes

If you use [workspace-level extended retention](../../Govern/Data%20%26%20compliance/Data%20purging%20for%20compliance.md#customize-extended-retention-policy), LangSmith writes blob data to prefixes of the form `ttl_XXd/`, where `XX` is the number of days configured for that workspace. For example, if a workspace is configured with 90-day extended retention, blob data for that workspace is written to the `ttl_90d/` prefix.

You must create a lifecycle rule for **each** custom retention period configured across your workspaces. Common examples:

* `ttl_90d/` — 90-day retention
* `ttl_180d/` — 180-day retention
* `ttl_365d/` — 365-day retention

> [!WARNING]
>
> If a lifecycle rule is missing for a configured retention period, blob data under that prefix will never be automatically deleted. Ensure you add a matching lifecycle rule whenever you configure a new workspace retention period.

For example, if you have workspaces configured with 90-day and 180-day extended retention, you would add the following lifecycle rules **in addition to** the [default `ttl_s` and `ttl_l` rules](#ttl-configuration):

> [tab] AWS
>
> ```hcl theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> rule {
>   id      = "ttl-90d"
>   prefix  = "ttl_90d/"
>   enabled = true
>   expiration {
>     days = 90
>   }
> }
> rule {
>   id      = "ttl-180d"
>   prefix  = "ttl_180d/"
>   enabled = true
>   expiration {
>     days = 180
>   }
> }
> ```

> [tab] GCP
>
> ```hcl theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> lifecycle_rule {
>   condition {
>     age            = 90
>     matches_prefix = ["ttl_90d"]
>   }
>   action {
>     type = "Delete"
>   }
> }
> lifecycle_rule {
>   condition {
>     age            = 180
>     matches_prefix = ["ttl_180d"]
>   }
>   action {
>     type = "Delete"
>   }
> }
> ```

> [tab] Azure
>
> ```hcl theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> rule {
>   name    = "ttl-90d"
>   enabled = true
>   type    = "Lifecycle"
>   filters {
>     prefix_match = ["my-container/ttl_90d"]
>     blob_types   = ["blockBlob"]
>   }
>   actions {
>     base_blob {
>       delete_after_days_since_creation_greater_than = 90
>     }
>     snapshot {
>       delete_after_days_since_creation_greater_than = 90
>     }
>     version {
>       delete_after_days_since_creation_greater_than = 90
>     }
>   }
> }
> rule {
>   name    = "ttl-180d"
>   enabled = true
>   type    = "Lifecycle"
>   filters {
>     prefix_match = ["my-container/ttl_180d"]
>     blob_types   = ["blockBlob"]
>   }
>   actions {
>     base_blob {
>       delete_after_days_since_creation_greater_than = 180
>     }
>     snapshot {
>       delete_after_days_since_creation_greater_than = 180
>     }
>     version {
>       delete_after_days_since_creation_greater_than = 180
>     }
>   }
> }
> ```

> [tab] Neon
>
> Neon Object Storage does not run lifecycle rules. Make sure your [cleanup job](#neon-object-storage-lifecycle-rules) deletes objects under each custom prefix, such as `ttl_90d/` and `ttl_180d/`, once they are older than that prefix's TTL.

If you have customized the TTLs in your LangSmith configuration, you will need to adjust the TTLs in your blob storage configuration to match.

> [tab] AWS
>
> ### Amazon S3 lifecycle rules
>
> If using S3 for your blob storage, you will need to setup a filter lifecycle configuration that matches the prefixes above. You can find information for this [in the Amazon Documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html#intro-lifecycle-rules-filter).
>
> As an example, if you are using Terraform to manage your S3 bucket, you would setup something like this:
>
> ```hcl theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> rule {
>   id      = "short-term-ttl"
>   prefix  = "ttl_s/"
>   enabled = true
>   expiration {
>     days = 14
>   }
> }
> rule {
>   id      = "long-term-ttl"
>   prefix  = "ttl_l/"
>   enabled = true
>   expiration {
>     days = 400
>   }
> }
> ```

> [tab] GCP
>
> ### Google Cloud Storage lifecycle rules
>
> You will need to setup lifecycle conditions for your GCS buckets that you are using. You can find information for this [in the Google Documentation](https://cloud.google.com/storage/docs/lifecycle#conditions), specifically using matchesPrefix.
>
> As an example, if you are using Terraform to manage your GCS bucket, you would setup something like this:
>
> ```hcl theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> lifecycle_rule {
>   condition {
>     age            = 14
>     matches_prefix = ["ttl_s"]
>   }
>   action {
>     type = "Delete"
>   }
> }
> lifecycle_rule {
>   condition {
>     age            = 400
>     matches_prefix = ["ttl_l"]
>   }
>   action {
>     type = "Delete"
>   }
> }
> ```

> [tab] Azure
>
> ### Azure blob storage lifecycle management
>
> You will need to configure a [lifecycle management policy](https://learn.microsoft.com/en-us/azure/storage/blobs/lifecycle-management-policy-configure) on the container in order to expire objects matching the prefixes above.
>
> As an example, if you are [using Terraform to manage your blob storage container](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_management_policy), you would setup something like this:
>
> ```hcl theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> resource "azurerm_storage_management_policy" "example" {
>   storage_account_id = "my-storage-account-id"
>   rule {
>     name = "base"
>     enabled = true
>     type = "Lifecycle"
>     filters {
>       prefix_match = ["my-container/ttl_s"]
>       blob_types = ["blockBlob"]
>     }
>     actions {
>       base_blob {
>         delete_after_days_since_creation_greater_than = 14
>       }
>       snapshot {
>         delete_after_days_since_creation_greater_than = 14
>       }
>       version {
>         delete_after_days_since_creation_greater_than = 14
>       }
>     }
>   }
>   rule {
>     name = "extended"
>     enabled = true
>     type = "Lifecycle"
>     filters {
>       prefix_match = ["my-container/ttl_l"]
>       blob_types = ["blockBlob"]
>     }
>     actions {
>       base_blob {
>         delete_after_days_since_creation_greater_than = 400
>       }
>       snapshot {
>         delete_after_days_since_creation_greater_than = 400
>       }
>       version {
>         delete_after_days_since_creation_greater_than = 400
>       }
>     }
>   }
> }
> ```

> [tab] Neon
>
> ### Neon Object Storage lifecycle rules
>
> > [!WARNING]
> >
> > Neon Object Storage accepts and stores lifecycle configurations, but does not run expiration rules. Objects under the `ttl_s/`, `ttl_l/`, and `ttl_XXd/` prefixes are not deleted automatically, so blob data outlives the TTLs configured in LangSmith. For more information, see [Neon Object Storage troubleshooting](https://neon.com/docs/storage/troubleshooting).
>
> To enforce TTLs, run a scheduled job (for example, a Kubernetes CronJob) that deletes objects older than each prefix's TTL.
