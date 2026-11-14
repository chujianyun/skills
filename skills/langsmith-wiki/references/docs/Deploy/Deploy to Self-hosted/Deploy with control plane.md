# Deploy with control plane

> Build Docker images and deploy applications to a self-hosted LangSmith instance using the control plane UI.

> [!NOTE]
>
> **This guide is for self-hosted LangSmith customers** who have [enabled Agent Server hosting](../../LangSmith%20setup/Self-hosted/Install%20an%20instance/Additional%20features/Enable%20Agent%20Server%20hosting.md#enable-langsmith-deployment) on their instance. For Cloud customers, see [Deploy on Cloud](../Deploy%20to%20Cloud/Deployment%20guide/Create%20an%20Agent%20Server.md). For standalone Agent Servers without a control plane, see [Self-host standalone servers](Self-host%20standalone%20servers.md).

This guide shows you how to deploy your applications to a [self-hosted](../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) LangSmith instance using a [control plane](../Get%20started/Deployment%20components/LangSmith%20control%20plane.md). With a control plane, you build Docker images locally, push them to a registry that your Kubernetes cluster has access to, and deploy them with the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-deploy-with-control-plane).

## Topology

Enabling Agent Server hosting on an existing self-hosted LangSmith instance adds a control plane, a data plane listener, and an operator that provisions Agent Servers in your cluster. The base LangSmith platform continues to handle observability, evaluation, and prompts; deployed Agent Servers send traces back to it.

For details on the components added by enabling Agent Server hosting, see [Enable Agent Server hosting](../../LangSmith%20setup/Self-hosted/Install%20an%20instance/Additional%20features/Enable%20Agent%20Server%20hosting.md#enable-langsmith-deployment).

## Overview

Applications deployed to a self-hosted LangSmith instance with a control plane use Docker images. In this guide, the application deployment workflow is:

1. Test your application locally using `langgraph dev` or [Studio](../../Test/Test%20from%20Studio/LangSmith%20Studio.md).
2. Build a Docker image using the `langgraph build` command.
3. Push the image to a container registry accessible by your infrastructure.
4. Deploy from the [control plane UI](../Get%20started/Deployment%20components/LangSmith%20control%20plane.md#control-plane-ui) by specifying the image URL.

## Prerequisites

Before completing this guide, you'll need the following:

* [Agent Server hosting enabled](../../LangSmith%20setup/Self-hosted/Install%20an%20instance/Additional%20features/Enable%20Agent%20Server%20hosting.md#enable-langsmith-deployment) on your self-hosted LangSmith instance.
* Access to the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-deploy-with-control-plane) with Agent Server hosting enabled.
* A container registry accessible by your Kubernetes cluster. If using a private registry that requires authentication, you must configure image pull secrets as part of your infrastructure setup. Refer to [Private registry authentication](#private-registry-authentication).

## Step 1. Test locally

Before deploying, test your application locally. You can use the [LangGraph CLI](../Get%20started/Reference/LangGraph%20CLI.md#dev) to run an Agent Server in development mode:

```bash
langgraph dev
```

For a full guide local testing, refer to the [Local server quickstart](../Get%20started/Develop%20%26%20test/Local%20development%20%26%20testing.md).

## Step 2. Build Docker image

Build a Docker image of your application using the [`langgraph build`](../Get%20started/Reference/LangGraph%20CLI.md#build) command:

```bash
langgraph build -t my-image
```

Build command options include:

| Option | Default | Description |
| - | - | - |
| `-t, --tag TEXT` | Required | Tag for the Docker image |
| `--platform TEXT` | | Target platform(s) to build for (e.g., `linux/amd64,linux/arm64`) |
| `--pull / --no-pull` | `--pull` | Build with latest remote Docker image |
| `-c, --config FILE` | `langgraph.json` | Path to configuration file |

Example with platform specification:

```bash
langgraph build --platform linux/amd64 -t my-image:v1.0.0
```

For full details, see the [CLI reference](../Get%20started/Reference/LangGraph%20CLI.md#build).

## Step 3. Push to container registry

Push your image to a container registry accessible by your Kubernetes cluster. The specific commands depend on your registry provider.

> [!TIP]
>
> Tag your images with version information (e.g., `my-registry.com/my-app:v1.0.0`) to make rollbacks easier.

## Step 4. Deploy with the control plane UI

The [control plane UI](../Get%20started/Deployment%20components/LangSmith%20control%20plane.md#control-plane-ui) allows you to create and manage Agent Servers, view logs and metrics, and update configurations. To create a new Agent Server in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-deploy-with-control-plane):

1. In the left-hand navigation panel, select **Agent Servers**.
2. In the top-right corner, select **+ Agent Server**.
3. In the Agent Server configuration panel, provide:
   * **Image URL**: The full image URL you pushed in [Step 3](#step-3-push-to-container-registry).
   * **Listener/Compute ID**: Select the listener configured for your infrastructure.
   * **Namespace**: The Kubernetes namespace to deploy to.
   * **Environment variables**: Any required configuration (API keys, etc.).
   * Other Agent Server settings as needed.
4. Select **Submit**.

The control plane will coordinate with your [data plane](../Get%20started/Deployment%20components/LangSmith%20data%20plane.md) listener to deploy your application.

After creating an Agent Server, the infrastructure is [provisioned asynchronously](../Get%20started/Deployment%20components/LangSmith%20control%20plane.md#asynchronous-deployment). Deployment can take up to several minutes, with initial deployments taking longer due to database creation.

From the control plane UI, you can view build logs, server logs, and Agent Server metrics including CPU/memory usage, replicas, and API performance. For more details, refer to the [control plane monitoring documentation](../Get%20started/Deployment%20components/LangSmith%20control%20plane.md#monitoring).

> [!NOTE]
>
> A [LangSmith Observability tracing project](../../Monitor/Overview/LangSmith%20Observability.md) is automatically created for each Agent Server with the same name as the Agent Server. Tracing environment variables are set automatically by the control plane.

## Update an Agent Server

To deploy a new version of your application, create a [new revision](../Get%20started/Deployment%20components/LangSmith%20control%20plane.md#revisions):

Starting from the LangSmith UI:

1. In the left-hand navigation panel, select **Agent Servers**.
2. Select an existing Agent Server.
3. In the Agent Server view, select **+ New Revision** in the top-right corner.
4. Update the configuration:
   * Update the **Image URL** to your new image version.
   * Update environment variables if needed.
   * Adjust other settings as needed.
5. Select **Submit**.

## Private registry authentication

If your container registry requires authentication (e.g., AWS ECR, Azure ACR, GCP Artifact Registry, private Docker registry), you must configure Kubernetes image pull secrets before deploying applications. This is a one-time infrastructure configuration.

> [!NOTE]
>
> **This configuration is done at the infrastructure level, not per Agent Server.** Once configured, all Agent Servers automatically inherit the registry credentials.

Configure `imagePullSecrets` in your LangSmith Helm chart's `values.yaml` file. See the detailed steps in the [Enable Agent Server hosting guide](../../LangSmith%20setup/Self-hosted/Install%20an%20instance/Additional%20features/Enable%20Agent%20Server%20hosting.md#enable-langsmith-deployment).

For detailed steps on creating image pull secrets for different registry providers, refer to the [Kubernetes documentation on pulling images from private registries](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/).

## Next steps

* **[Control plane](../Get%20started/Deployment%20components/LangSmith%20control%20plane.md)**: Learn more about control plane features.
* **[Data plane](../Get%20started/Deployment%20components/LangSmith%20data%20plane.md)**: Understand data plane architecture.
* **[Observability](../../Monitor/Overview/LangSmith%20Observability.md)**: Monitor your Agent Servers with automatic tracing.
* **[Studio](../../Test/Test%20from%20Studio/LangSmith%20Studio.md)**: Test and debug deployed applications.
* **[LangGraph CLI](../Get%20started/Reference/LangGraph%20CLI.md)**: Full CLI reference documentation.
