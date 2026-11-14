# Use environment variables for model providers

> [!NOTE]
>
> This feature is only available on Helm chart versions 0.10.27 (application version 0.10.74) and later.

Many model providers support setting credentials and other configuration options through environment variables. This is useful for self-hosted deployments where you want to avoid hardcoding sensitive information in your code or configuration files. In LangSmith, most model interactions are done through the `playground` service, which allows you to configure many of those environment variables directly on the pod itself. This can be useful to avoid having to set credentials in the UI.

## Requirements

* A self-hosted LangSmith instance with the `playground` service running.
* The provider you want to configure must support environment variables for configuration. Check the provider's Chat Model [documentation](https://docs.langchain.com/oss/python/integrations/providers/overview.md) for more information.
* The secrets/roles you may want to attach to the `playground` service.
  * Note that for [IRSA](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) you may need to grant the `langsmith-playground` service account the necessary permissions to access the secrets or roles in your cloud provider.

## Configuration

With the parameters from above, you can configure your LangSmith instance to use environment variables for model providers. You can do this by modifying the `langsmith_config.yaml` file for your LangSmith Helm Chart installation.

```yaml Helm
playground:
  deployment:
    extraEnv:
      - name: OPENAI_BASE_URL
        value: https://<my_proxy_url>
      - name: OPENAI_API_KEY
        valueFrom:
          secretKeyRef:
            name: <your_secret_name>
            key: api_key
  serviceAccount: # Can be useful if you want to use IRSA or workload identity
    annotations:
      eks.amazonaws.com/role-arn: <your_role_arn>
```

## Gemini Enterprise Agent Platform configuration

You can configure Gemini Enterprise Agent Platform credentials for the playground service using either environment variables with secrets or GCP Workload Identity for GKE.

### Using secrets

Configure Gemini Enterprise Agent Platform credentials using Kubernetes secrets:

```yaml Helm
playground:
  deployment:
    extraEnv:
      # Playground-specific secret (recommended)
      - name: GOOGLE_VERTEX_AI_WEB_CREDENTIALS
        valueFrom:
          secretKeyRef:
            name: gcp-vertexai-secret
            key: credentials_json  # Your full service account JSON as string
      # Standard fallback option
      - name: GOOGLE_APPLICATION_CREDENTIALS
        value: /secrets/gcp-key.json
      # Optional: Set project/location if not in model config
      - name: GOOGLE_CLOUD_PROJECT
        value: "your-gcp-project-id"
      - name: VERTEXAI_PROJECT_ID
        value: "your-gcp-project-id"
      - name: VERTEXAI_LOCATION
        value: "us-central1"
    extraVolumeMounts:
      - name: gcp-secret-volume
        mountPath: /secrets
        readOnly: true
    extraVolumes:
      - name: gcp-secret-volume
        secret:
          secretName: gcp-key-json  # JSON file secret
          defaultMode: 0444
```

### Using workload identity

On self-hosted LangSmith running on GKE, Playground can use Workload Identity Federation and ADC instead of a service account JSON key. See [Authenticate Vertex AI with GKE workload identity](Authenticate%20Vertex%20AI%20with%20GKE%20workload%20identity.md) to configure Playground alongside Chat and Insights.

## AWS IRSA (EKS)

For EKS clusters, you can use AWS IRSA (IAM Roles for Service Accounts) to grant the `playground` service account access to AWS resources without storing credentials. Annotate the service account with your IAM role ARN:

```yaml Helm
playground:
  serviceAccount:
    create: true  # Enable if not exists
    annotations:
      eks.amazonaws.com/role-arn: arn:aws:iam::<account>:role/LangSmith-Playground-Role
```

> [!NOTE]
>
> Ensure your AWS IAM role has the necessary permissions for the AWS resources the playground service needs to access.
