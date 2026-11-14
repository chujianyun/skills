# Troubleshooting for self-hosted deployments

> Diagnostic steps for troubleshooting self-hosted LangSmith Agent Server issues before contacting support.

This page provides diagnostic steps to help you troubleshoot issues with self-hosted [LangSmith Agent Server](../../Get%20started/LangSmith%20Agent%20Server.md) before reaching out to support. Follow these steps systematically to identify and resolve common deployment issues.

If you complete these diagnostic steps and still need assistance, refer to [Support](#support) at the end of this guide for information on what to gather before reaching out.

## Prerequisites

Before beginning the diagnostic steps, ensure you have:

* `kubectl` access to your Kubernetes cluster.
* Appropriate permissions to view pods, deployments, services, etc.
* Familiarity with your [Helm chart configuration](../../../LangSmith%20setup/Self-hosted/Install%20an%20instance/Self-host%20LangSmith%20on%20Kubernetes.md#configure-your-helm-charts:).

## Step 1. Understand your deployment

Verify what was deployed and understand the baseline state of your system. This helps you recognize what normal operation looks like and identify deviations when issues occur.

Run the following commands to view all deployed Kubernetes resources.

> [!NOTE]
>
> Ensure that you're in the correct namespace when you run the commands in this section. Or, specify the namespace explicitly with the `-n` flag. For example: `kubectl get deployments -n langsmith`.

List all deployments:

```bash
kubectl get deployments
```

List all pods:

```bash
kubectl get pods
```

List all services:

```bash
kubectl get services
```

List all `lgps` resources (only present after creating an [Agent Server](../../Agent%20Server/Capabilities/Agent%20Server.md)):

```bash
kubectl get lgps
```

### Key deployed components

Your deployment includes the following core components:

* **`langsmith-frontend`**: The LangSmith frontend UI where you create Agent Servers. This app makes API calls to `langsmith-host-backend`. Part of the [control plane](../../Get%20started/Deployment%20components/LangSmith%20control%20plane.md).
* **`langsmith-host-backend`**: The LangSmith Agent Server [control plane](../../Get%20started/Deployment%20components/LangSmith%20control%20plane.md) that receives requests from `langsmith-frontend` and persists deployment requests to the control plane Postgres database.
* **`langsmith-listener`**: Part of the LangSmith Agent Server [data plane](../../Get%20started/Deployment%20components/LangSmith%20data%20plane.md). Polls `langsmith-host-backend` via HTTP API for deployments to create, update, or delete. Enqueues tasks for worker processes to handle.
* **`langsmith-redis`**: The [Redis](../../Get%20started/Deployment%20components/LangSmith%20data%20plane.md#redis) instance serving as the task queue for `langsmith-listener`. The listener enqueues tasks here and workers pull tasks from this queue.
* **`langsmith-operator`**: The `lgps` Kubernetes operator that reconciles underlying Kubernetes resources for `lgps` resources. Part of the data plane infrastructure.

> [!NOTE]
>
> Additional components may be present in your deployment depending on your configuration. For an overview, refer to [LangSmith Agent Server components](../../Get%20started/Deployment%20components/LangSmith%20Agent%20Server%20components.md).

## Step 2. Enable debug logging

When troubleshooting issues, the first step is typically to enable debug-level logging to gather more detailed information about what's happening in your system.

### For control plane or data plane deployments

If you are experiencing issues with a control plane deployment (for example, `langsmith-host-backend`) or a data plane deployment (for example, `langsmith-listener`), reinstall the Helm chart with the `LOG_LEVEL=DEBUG` environment variable. Add the following to your `values.yaml` file:

```yaml
extraEnv:
  - name: LOG_LEVEL
    value: DEBUG
```

### For Agent Servers

If the issue is with an individual Agent Server:

1. Navigate to the **Agent Servers** tab in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-diagnostics-self-hosted).
2. On an Agent Server's view, select **+ New Revision**.
3. Add a new environment variable `LOG_LEVEL` and set it to `DEBUG`.

> [!NOTE]
>
> You can also find debug logs in the UI on an Agent Server's view, click on **Server Logs** and select **Debug** for the **Log level: Info** dropdown.

### For widespread issues

If you are unsure where the issue originates, enable `DEBUG` logging everywhere (control plane, data plane, and all Agent Servers).

### Review application logs

Tail the logs of each pod to understand baseline behavior:

```bash
kubectl logs -f <pod_name>
```

Then look for these log lines:

* **`langsmith-listener`**: `Reconciling projects...` (appears every 10 seconds)
* **`langsmith-operator`**: `Starting reconciliation` (appears periodically)

In a healthy deployment, you should not see any errors. All logs should appear normal and routine.

### Interpret debug logs

Look for the following problem indicators:

* Exceptions or stack traces.
* Error messages (the word `"ERROR"`).
* Unusual patterns that differ from normal operation.

Based on the errors you find:

* **Configuration issue**: If you suspect a configuration problem, raise the issue with the person who ran [`helm install`](../../../LangSmith%20setup/Self-hosted/Install%20an%20instance/Self-host%20LangSmith%20on%20Kubernetes.md).
* **User code bug**: If you suspect a bug in user code (for example, the LangGraph OSS graph implementation), raise the issue with the owner of the Agent Server application who created the [`langgraph.json`](../../Agent%20Server/Develop%20your%20application/Application%20structure.md#configuration-file) file.

## Step 3. Describe deployments and pods

Describing Kubernetes resources reveals error events and statuses that may not appear in application logs. These errors are typically caused by configuration or infrastructure issues rather than application code bugs. Describing resources also shows their configuration (such as environment variables), which is helpful for debugging.

Run the following commands to describe your resources.

Describe a Kubernetes deployment:

```bash
kubectl describe deployment <deployment_name>
```

Describe a Kubernetes pod:

```bash
kubectl describe pod <pod_name>
```

Describe an `lgps` resource (only relevant after creating an Agent Server):

```bash
kubectl describe lgps <lgps_name>
```

### Interpret results

Review the `Events:` section of the output and verify that everything is normal. Common issues that appear include:

* Failed liveness or readiness probes
* Image pull errors
* Resource constraints (CPU, memory)
* Volume mount issues
* Configuration errors

Make sure there are no error events and that all events indicate healthy operation.

## Additional resources

For more troubleshooting information, refer to:

* [Troubleshooting](../../../LangSmith%20setup/Self-hosted/Configure%20an%20instance/Troubleshooting.md): General troubleshooting guide with solutions to common issues.
* [Self-hosted overview](../../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md): Details on system architecture and component interactions.

## Support

If you have followed these diagnostic steps and still need assistance, gather the following information and contact [Technical Support](https://support.langchain.com/):

* Capture the [diagnostic bundle](https://support.langchain.com/articles/2087799075-how-to-share-diags).
* Description of what you were trying to do when the issue occurred.

Having this information in the ticket will help the [support](https://support.langchain.com/) team diagnose and resolve your issue more quickly.
