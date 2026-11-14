# Bring your own keys (CMK)

> Encrypt a new LangSmith BYOC data plane on AWS with your own AWS KMS keys, using one key for every service or a separate key per service.

By default, AWS-managed keys encrypt the data plane at rest. You can instead use your own symmetric [AWS KMS keys](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#kms_keys), set when you create the data plane:

| Service | What the key encrypts |
| - | - |
| `s3` | The data plane's S3 buckets. |
| `ebs` | Node volumes. |
| `eks` | Kubernetes secrets in the EKS cluster. |
| `rds` | RDS storage, the RDS master user secrets, and Performance Insights data. |
| `elasticache` | ElastiCache data at rest. |

> [!NOTE]
>
> One key can encrypt every service. In the UI, choose **One key for all services**. In Terraform, set the same key ARN for each service in `cmk_service_key_arns`. You can also use a separate key per service.

Every service is optional: a service without a key keeps AWS-managed encryption. Keys must be in the data plane region. They can be in the data plane account or in another AWS account.

Keys cannot be added to existing data planes. After creation, the `ebs`, `eks`, `rds`, and `elasticache` keys cannot change. To change the `s3` key, contact the LangChain team.

To set up the keys:

1. In the [`langsmith-byoc-role` Terraform module](https://github.com/langchain-ai/terraform/tree/main/modules/byoc/aws/langsmith-byoc-role#customer-managed-kms-keys), set `cmk_service_key_arns` to a key ARN for each service. With [BYOIAM](Bring%20your%20own%20IAM%20roles%20%28AWS%29.md), set it in the BYOIAM module too.
2. Update the key policies as the [module README](https://github.com/langchain-ai/terraform/tree/main/modules/byoc/aws/langsmith-byoc-role#customer-managed-kms-keys) describes. The `ebs` key policy must allow the Auto Scaling service-linked role. When LangSmith manages the VPC, the `s3` key policy must allow VPC flow log delivery.
3. When you create the data plane, open **Encryption keys** under **Configuration** and enter the key ARNs. Through the API, set `customer_managed_keys.key_arn` for every service, or `customer_managed_keys.service_key_arns` per service.

Before it creates the data plane, LangSmith checks that each key exists and is enabled, and that the provisioning role can use it. For keys in the data plane account, LangSmith also checks that the `ebs` and `s3` key policies allow these principals.

A key in another AWS account also needs key policy statements that allow the provisioning role and each BYOIAM role. An `ebs` key in another account also needs a grant for the Auto Scaling service-linked role, created from the data plane account, as the [module README](https://github.com/langchain-ai/terraform/tree/main/modules/byoc/aws/langsmith-byoc-role#customer-managed-kms-keys) describes. LangSmith cannot read the policy of a key in another account, so make sure the policy is complete before you create the data plane.

> [!WARNING]
>
> If you disable or delete a key, every service that uses it stops working. Data encrypted with a deleted key cannot be recovered.
