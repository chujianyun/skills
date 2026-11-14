# Manage bulk export destinations

> Configure and manage S3-compatible export destinations for LangSmith bulk exports.

> [!NOTE]
>
> **For self-hosted, GCP EU, GCP APAC, AWS US, and Azure US SaaS**
>
> Update the LangSmith URL in the requests below for self-hosted installs, GCP EU (`eu.api.smith.langchain.com`), GCP APAC (`apac.api.smith.langchain.com`), AWS US (`aws.api.smith.langchain.com`), or Azure US (`azure.api.smith.langchain.com`).

A destination is a named configuration that tells LangSmith where to write exported trace data. You [create a destination](Bulk%20export%20trace%20data.md#1-create-a-destination) once, then reference it by ID when [creating export jobs](Bulk%20export%20trace%20data.md#2-create-an-export-job). LangSmith currently supports S3 and any S3-compatible bucket (such as GCS or MinIO) as a destination. Exported data is written in [Parquet](https://parquet.apache.org/docs/overview/) columnar format and contains equivalent fields to the [Run data format](../Data%20type%20reference/Run%20%28span%29%20data%20format.md).

This page covers:

* The [configuration fields](#configuration-fields) needed to set up a destination.
* Required bucket [permissions](#permissions-required) for AWS S3 and GCS.
* How to [create a destination](#create-a-destination) via the API, including provider-specific examples and credential options.
* How to [rotate destination credentials](#rotate-destination-credentials) without recreating the destination.
* How to [switch authentication mode](#switch-authentication-mode) between static credentials and AWS IAM role assumption.
* How to [debug destination errors](#debug-destination-errors).

## Configuration fields

The following information is needed to configure a destination:

* **Bucket Name**: The name of the S3 bucket where the data will be exported to.
* **Prefix**: The root prefix within the bucket where the data will be exported to.
* **S3 Region**: The region of the bucket—required for AWS S3 buckets.
* **Endpoint URL**: The endpoint URL for the S3 bucket—required for S3 API compatible buckets.
* **Access Key**: The access key for the S3 bucket.
* **Secret Key**: The secret key for the S3 bucket.
* **Include Bucket in Prefix** (optional): Whether to include the bucket name as part of the path prefix. Defaults to `true`. Set to `false` when using virtual-hosted style endpoints where the bucket name is already in the endpoint URL.
* **S3 Config Options** (`config_kwargs_s3`, optional): Advanced S3 addressing style and request settings passed to botocore. The most common use is setting `addressing_style` for S3-compatible services that require virtual-hosted or path-style requests:
  * `"virtual"`: bucket name is part of the hostname (e.g. `bucket.endpoint/key`). Required for some S3-compatible services such as Volcengine TOS.
  * `"path"`: bucket name is part of the URL path (e.g. `endpoint/bucket/key`).
  * `"auto"` (default): boto3 decides based on the endpoint.

We support any S3 compatible bucket. For non-AWS buckets such as GCS or MinIO, you will need to provide the endpoint URL.

## Permissions required

Both the `backend` and `queue` services require write access to the destination bucket:

* The `backend` service attempts to write a test file to the destination bucket when the export destination is created. It will delete the test file if it has permission to do so (delete access is optional).
* The `queue` service is responsible for bulk export execution and uploading the files to the bucket.

### AWS S3 permissions

The minimal AWS S3 permission policy relies on the following permissions:

* `s3:PutObject` (required): Allows writing Parquet files to the bucket.
* `s3:DeleteObject` (optional): Cleans up test files during destination creation. If this permission isn't present, the file is left under the `/tmp` directory after destination creation.
* `s3:GetObject` (optional but recommended): Verifies file size after writing.
* `s3:AbortMultipartUpload` (optional but recommended): Avoids dangling multipart uploads.

Minimal IAM policy example:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:::YOUR_BUCKET_NAME/*"
      ]
    }
  ]
}
```

Recommended IAM policy example with additional permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:GetObject"
      ],
      "Resource": [
        "arn:aws:s3:::YOUR_BUCKET_NAME/*"
      ]
    }
  ]
}
```

### Google Cloud Storage (GCS) permissions

When using GCS with the S3-compatible XML API, the following IAM permissions are required:

* `storage.objects.create` (required): Allows writing files to the bucket.
* `storage.objects.delete` (optional): Cleans up test files during destination creation. If this permission isn't present, the file is left under the `/tmp` directory after destination creation.
* `storage.objects.get` (optional but recommended): Verifies file size after writing.

These permissions can be granted through the "Storage Object Admin" predefined role or a custom role.

## Create a destination

The following example demonstrates how to create a destination using cURL. Replace the placeholder values with your actual configuration details.
Note that credentials will be stored securely in an encrypted form in our system.

```bash
curl --request POST \
  --url 'https://api.smith.langchain.com/api/v1/bulk-exports/destinations' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY' \
  --header 'X-Tenant-Id: YOUR_WORKSPACE_ID' \
  --data '{
    "destination_type": "s3",
    "display_name": "My S3 Destination",
    "config": {
      "bucket_name": "your-s3-bucket-name",
      "prefix": "root_folder_prefix",
      "region": "your aws s3 region",
      "endpoint_url": "your endpoint url for s3 compatible buckets",
      "include_bucket_in_prefix": true // defaults to true, can be omitted
    },
    "credentials": {
      "access_key_id": "YOUR_S3_ACCESS_KEY_ID",
      "secret_access_key": "YOUR_S3_SECRET_ACCESS_KEY"
    }
  }'
```

Use the returned `id` to reference this destination in subsequent bulk export operations.

**If you receive an error while creating a destination, see [Debug destination errors](#debug-destination-errors) for details on how to debug this.**

### Credentials configuration

> [!NOTE]
>
> **Requires LangSmith Helm version `0.10.34` or later (application version `0.10.91` or later)**

We support the following additional credentials formats besides static `access_key_id` and `secret_access_key`:

* To use [temporary credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html) that include an AWS session token,
  additionally provide the `credentials.session_token` key when creating the bulk export destination.
* (Self-hosted only): To use environment-based credentials such as with [AWS IAM Roles for Service Accounts](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) (IRSA),
  omit the `credentials` key from the request when creating the bulk export destination.
  In this case, the [standard Boto3 credentials locations](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#credentials) will be checked in the order defined by the library.

### AWS S3 bucket

For AWS S3, you can leave off the `endpoint_url` and supply the region that matches the region of your bucket.

```bash
curl --request POST \
  --url 'https://api.smith.langchain.com/api/v1/bulk-exports/destinations' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY' \
  --header 'X-Tenant-Id: YOUR_WORKSPACE_ID' \
  --data '{
    "destination_type": "s3",
    "display_name": "My AWS S3 Destination",
    "config": {
      "bucket_name": "my_bucket",
      "prefix": "data_exports",
      "region": "us-east-1"
    },
    "credentials": {
      "access_key_id": "YOUR_S3_ACCESS_KEY_ID",
      "secret_access_key": "YOUR_S3_SECRET_ACCESS_KEY"
    }
  }'
```

### Google GCS XML S3 compatible bucket

When using Google's GCS bucket, you need to use the XML S3 compatible API, and supply the `endpoint_url`
which is typically `https://storage.googleapis.com`.
Here is an example of the API request when using the GCS XML API which is compatible with S3:

```bash
curl --request POST \
  --url 'https://api.smith.langchain.com/api/v1/bulk-exports/destinations' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY' \
  --header 'X-Tenant-Id: YOUR_WORKSPACE_ID' \
  --data '{
    "destination_type": "s3",
    "display_name": "My GCS Destination",
    "config": {
      "bucket_name": "my_bucket",
      "prefix": "data_exports",
      "endpoint_url": "https://storage.googleapis.com"
      "include_bucket_in_prefix": true // defaults to true, can be omitted
    },
    "credentials": {
      "access_key_id": "YOUR_S3_ACCESS_KEY_ID",
      "secret_access_key": "YOUR_S3_SECRET_ACCESS_KEY"
    }
  }'
```

See [Google documentation](https://cloud.google.com/storage/docs/interoperability#xml_api) for more info

### S3-compatible bucket with virtual-hosted style addressing

Some S3-compatible services (such as Volcengine TOS) require virtual-hosted style addressing, where the bucket name is part of the hostname rather than the URL path. Use `config_kwargs_s3` with `addressing_style: "virtual"` to enable this:

```bash
curl --request POST \
  --url 'https://api.smith.langchain.com/api/v1/bulk-exports/destinations' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY' \
  --header 'X-Tenant-Id: YOUR_WORKSPACE_ID' \
  --data '{
    "destination_type": "s3",
    "display_name": "My Volcengine TOS Destination",
    "config": {
      "bucket_name": "my_bucket",
      "prefix": "data_exports",
      "endpoint_url": "https://tos-s3-cn-beijing.volces.com",
      "config_kwargs_s3": {
        "addressing_style": "virtual"
      }
    },
    "credentials": {
      "access_key_id": "YOUR_ACCESS_KEY_ID",
      "secret_access_key": "YOUR_SECRET_ACCESS_KEY"
    }
  }'
```

### S3-compatible bucket with virtual-hosted style endpoint

If your endpoint URL already includes the bucket name (virtual-hosted style), set `include_bucket_in_prefix` to `false` to avoid duplicating the bucket name in the path:

```bash
curl --request POST \
  --url 'https://api.smith.langchain.com/api/v1/bulk-exports/destinations' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY' \
  --header 'X-Tenant-Id: YOUR_WORKSPACE_ID' \
  --data '{
    "destination_type": "s3",
    "display_name": "My Virtual-Hosted Destination",
    "config": {
      "bucket_name": "my_bucket",
      "prefix": "data_exports",
      "endpoint_url": "https://my_bucket.s3.us-east-1.amazonaws.com",
      "include_bucket_in_prefix": false
    },
    "credentials": {
      "access_key_id": "YOUR_S3_ACCESS_KEY_ID",
      "secret_access_key": "YOUR_S3_SECRET_ACCESS_KEY"
    }
  }'
```

## Rotate destination credentials

Use `PATCH /api/v1/bulk-exports/destinations/{destination_id}` to update the credentials on an existing destination. This lets you rotate or replace credentials without recreating the destination or its associated bulk exports. The destination configuration (bucket, prefix, region, endpoint, etc.) is unchanged—only the credentials are replaced.

### Credential rotation behavior

The changeover is not instantaneous:

* **New bulk export runs** use the updated credentials immediately after the PATCH completes.
* **Already running bulk export runs** continue using the previous credentials until they finish.
* **Both sets of credentials are active simultaneously** during the transition period. This window lasts up to the maximum runtime of a single bulk export run.

Plan your rotation accordingly: the old credentials must remain valid until all in-flight runs complete.

### Request

```bash
curl --request PATCH \
  --url 'https://api.smith.langchain.com/api/v1/bulk-exports/destinations/{destination_id}' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY' \
  --header 'X-Tenant-Id: YOUR_WORKSPACE_ID' \
  --data '{
    "credentials": {
      "access_key_id": "YOUR_NEW_ACCESS_KEY_ID",
      "secret_access_key": "YOUR_NEW_SECRET_ACCESS_KEY"
    }
  }'
```

The `session_token` field is optional, which you can include for [temporary credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html).

[**Required permission**](../../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Organization%20and%20workspace%20operations%20reference.md#bulk-exports): `bulk-exports:manage`.

Before storing new credentials, LangSmith validates them by performing a test write to the bucket using the existing destination configuration. The request fails with `400` if the credentials do not have sufficient write permissions. If the request fails, refer to [Debug destination errors](#debug-destination-errors).

### Response

Returns the updated destination object. Credential values are never returned—only the credential field names are included in the response under `credentials_keys`.

```json
{
  "id": "destination-uuid",
  "tenant_id": "tenant-uuid",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-06-01T00:00:00Z",
  "credentials_keys": ["access_key_id", "secret_access_key"]
}
```

### Rotation checklist

1. Provision new credentials in your cloud provider with write access to the destination bucket and prefix.
2. Call the PATCH endpoint with the new credentials. LangSmith validates them before saving.
3. Keep old credentials active until all in-flight bulk export runs finish (up to the [maximum run duration](Monitor%20and%20troubleshoot%20bulk%20exports.md#automatic-retry-behavior)).
4. Revoke old credentials once no runs are using them.

## Authenticate with an AWS IAM role

AWS IAM role assumption lets GCP-hosted LangSmith SaaS export to S3 without storing static AWS credentials. Configure an AWS role that trusts the LangSmith service accounts for your production region, then provide its ARN when you create or update a destination.

Pass `aws_role_arn` instead of `credentials` to use IAM role assumption.

> [!NOTE]
>
> IAM role assumption is available only on GCP-hosted LangSmith SaaS. It is not available on AWS-hosted SaaS or self-hosted deployments.

### Create the AWS role

Create an AWS IAM role with a trust policy that permits web identity federation from the three subject IDs for your region. Grant the role access to your export bucket. Select your LangSmith region to use the corresponding subject IDs. Each Terraform example uses the minimum required `s3:PutObject` permission:

```hcl US
resource "aws_iam_role" "langsmith_bulk_export" {
  name                 = "langsmith-bulk-export"
  max_session_duration = 43200

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Federated = "accounts.google.com" }
      Action    = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringEquals = {
          "accounts.google.com:oaud" = "langsmith-bulk-export"
          "accounts.google.com:sub" = [
            "110136955440523778103",
            "116331607438151298187",
            "115251468294701876731",
          ]
        }
      }
    }]
  })

  inline_policy {
    name = "langsmith-bulk-export-s3"
    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [{
        Effect   = "Allow"
        Action   = "s3:PutObject"
        Resource = "arn:aws:s3:::YOUR_BUCKET_NAME/*"
      }]
    })
  }
}
```

```hcl EU
resource "aws_iam_role" "langsmith_bulk_export" {
  name                 = "langsmith-bulk-export"
  max_session_duration = 43200

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Federated = "accounts.google.com" }
      Action    = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringEquals = {
          "accounts.google.com:oaud" = "langsmith-bulk-export"
          "accounts.google.com:sub" = [
            "110207823358662523645",
            "115689110758588220909",
            "109691164801275818274",
          ]
        }
      }
    }]
  })

  inline_policy {
    name = "langsmith-bulk-export-s3"
    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [{
        Effect   = "Allow"
        Action   = "s3:PutObject"
        Resource = "arn:aws:s3:::YOUR_BUCKET_NAME/*"
      }]
    })
  }
}
```

```hcl APAC
resource "aws_iam_role" "langsmith_bulk_export" {
  name                 = "langsmith-bulk-export"
  max_session_duration = 43200

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Federated = "accounts.google.com" }
      Action    = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringEquals = {
          "accounts.google.com:oaud" = "langsmith-bulk-export"
          "accounts.google.com:sub" = [
            "105923862603785245337",
            "114288557158507552617",
            "116622461022404604716",
          ]
        }
      }
    }]
  })

  inline_policy {
    name = "langsmith-bulk-export-s3"
    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [{
        Effect   = "Allow"
        Action   = "s3:PutObject"
        Resource = "arn:aws:s3:::YOUR_BUCKET_NAME/*"
      }]
    })
  }
}
```

See [AWS S3 permissions](#aws-s3-permissions) for optional permissions.

## Switch authentication mode

Switch an existing destination between static credentials and [AWS IAM role assumption](#authenticate-with-an-aws-iam-role) without recreating it. Use `PATCH /api/v1/bulk-exports/destinations/{destination_id}`.

[**Required permission**](../../../LangSmith%20setup/Govern/Users%20%26%20access%20control/Organization%20and%20workspace%20operations%20reference.md#bulk-exports): `bulk-exports:manage`.

LangSmith supports two mutually exclusive modes:

* **Static credentials** (`credentials`): An `access_key_id` and `secret_access_key` (with an optional `session_token` for temporary credentials).
* **IAM role assumption** (`aws_role_arn`): LangSmith assumes the specified AWS IAM role, so no static credentials are stored.

To switch to AWS IAM role assumption, provide `aws_role_arn` in the PATCH body. To switch to static credentials, provide `credentials`. When either field is present and nonempty, LangSmith clears the other.

Before switching, ensure the new authentication configuration has write access to the destination bucket. LangSmith validates the configuration with a test write before saving it.

### Switch from static credentials to AWS IAM role

Provide `aws_role_arn` in the PATCH body. This clears any previously stored credentials.

```bash
curl --request PATCH \
  --url 'https://api.smith.langchain.com/api/v1/bulk-exports/destinations/{destination_id}' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY' \
  --header 'X-Tenant-Id: YOUR_WORKSPACE_ID' \
  --data '{
    "aws_role_arn": "arn:aws:iam::123456789012:role/LangSmithBulkExportRole"
  }'
```

### Switch from AWS IAM role to static credentials

Provide a `credentials` object in the PATCH body. This clears the stored role ARN.

```bash
curl --request PATCH \
  --url 'https://api.smith.langchain.com/api/v1/bulk-exports/destinations/{destination_id}' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY' \
  --header 'X-Tenant-Id: YOUR_WORKSPACE_ID' \
  --data '{
    "credentials": {
      "access_key_id": "YOUR_NEW_ACCESS_KEY_ID",
      "secret_access_key": "YOUR_NEW_SECRET_ACCESS_KEY"
    }
  }'
```

### Behavior during the switch

The same transition behavior described in [credential rotation](#credential-rotation-behavior) applies when switching authentication modes:

* **New bulk export runs** use the new authentication mode immediately after the PATCH completes.
* **Already running bulk export runs** continue using the previous authentication mode until they finish.

If the test write fails because the new configuration does not have sufficient write permissions, the request returns `400`.

## Debug destination errors

The destinations API endpoint will validate that the destination and credentials are valid and that write access
is present for the bucket.

If you receive an error, and would like to debug this error, you can use the [AWS CLI](https://aws.amazon.com/cli/)
to test the connectivity to the bucket. You should be able to write a file with the CLI using the same
data that you supplied to the destinations API above.

**AWS S3:**

```bash
aws configure

# set the same access key credentials and region as you used for the destination
> AWS Access Key ID: <access_key_id>
> AWS Secret Access Key: <secret_access_key>
> Default region name [us-east-1]: <region>

# List buckets
aws s3 ls /

# test write permissions
touch ./test.txt
aws s3 cp ./test.txt s3://<bucket-name>/tmp/test.txt
```

**GCS Compatible Buckets:**

You will need to supply the endpoint\_url with `--endpoint-url` option.
For GCS, the `endpoint_url` is typically `https://storage.googleapis.com`:

```bash
aws configure

# set the same access key credentials and region as you used for the destination
> AWS Access Key ID: <access_key_id>
> AWS Secret Access Key: <secret_access_key>
> Default region name [us-east-1]: <region>

# List buckets
aws s3 --endpoint-url=<endpoint_url> ls /

# test write permissions
touch ./test.txt
aws s3 --endpoint-url=<endpoint_url> cp ./test.txt s3://<bucket-name>/tmp/test.txt
```

### Common errors

Here are some common errors:

| Error | Description |
| - | - |
| Access denied | The blob store credentials or bucket are not valid. This error occurs when the provided access key and secret key combination doesn't have the necessary permissions to access the specified bucket or perform the required operations. |
| Bucket is not valid | The specified blob store bucket is not valid. This error is thrown when the bucket doesn't exist or there is not enough access to perform writes on the bucket. |
| Key ID you provided does not exist | The blob store credentials provided are not valid. This error occurs when the access key ID used for authentication is not a valid key. |
| Invalid endpoint | The endpoint\_url provided is invalid. This error is raised when the specified endpoint is an invalid endpoint. Only S3 compatible endpoints are supported, for example `https://storage.googleapis.com` for GCS, `https://play.min.io` for minio, etc. If using AWS, you should omit the endpoint\_url. |
| InvalidBucketName | The S3-compatible service rejected the request due to addressing style mismatch. Some services require virtual-hosted style addressing. Set `config_kwargs_s3: {"addressing_style": "virtual"}` in your destination config to resolve this. |
