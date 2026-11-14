# LangSmith control plane

The *control plane* is the part of LangSmith that manages deployments. It includes the control plane UI, where users create and update [Agent Servers](../../Agent%20Server/Capabilities/Agent%20Server.md), and the control plane APIs, which support the UI and provide programmatic access.

When you make an update through the control plane, the update is stored in the control plane state. The [data plane](LangSmith%20data%20plane.md) listener polls for these updates by calling the control plane APIs. The control plane never connects to the data plane directly.

## Control plane UI

From the control plane UI, you can:

* View a list of outstanding deployments.
* View details of an individual deployment.
* Create a new deployment.
* Update a deployment.
* Update environment variables for a deployment.
* View build and server logs of a deployment.
* View deployment metrics such as CPU and memory usage.
* Delete a deployment.

The Control plane UI is embedded in [LangSmith](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-control-plane).

## Control plane API

This section describes the data model of the control plane API. The API is used to create, update, and delete deployments. See the [control plane API reference](../Reference/Control%20Plane%20API/Control%20plane%20API%20reference%20for%20Agent%20Server%20hosting.md) for more details.

### Integrations

An integration is an abstraction for a `git` repository provider (e.g. GitHub). It contains all of the required metadata needed to connect with and deploy from a `git` repository.

### Deployments

A deployment is an instance of an Agent Server. A single deployment can have many revisions.

### Revisions

A revision is an iteration of a deployment. When a new deployment is created, an initial revision is automatically created. To deploy code changes or update secrets for a deployment, a new revision must be created.

### Listeners

A listener is an instance of a [listener application](LangSmith%20data%20plane.md#listener-application). A listener contains metadata about the application (e.g. version) and metadata about the compute infrastructure where it can deploy to (e.g. Kubernetes namespaces).

## Control plane features

This section describes various features of the control plane. For platform-specific behavior such as Cloud deployment types or self-hosted resource customization, see [Cloud platform features](../../Deploy%20to%20Cloud/Cloud%20platform%20features.md) or [Deploy to self-hosted](../../Deploy%20to%20Self-hosted/Deploy%20to%20self-hosted.md).

### Asynchronous deployment

Infrastructure for deployments and revisions are provisioned and deployed asynchronously. They are not deployed immediately after submission. Currently, deployment can take up to several minutes.

* When a new deployment is created, a new database is created for the deployment. Database creation is a one-time step. This step contributes to a longer deployment time for the initial revision of the deployment.
* When a subsequent revision is created for a deployment, there is no database creation step. The deployment time for a subsequent revision is significantly faster compared to the deployment time of the initial revision.
* The deployment process for each revision contains a build step, which can take up to a few minutes.

The control plane and [data plane](LangSmith%20data%20plane.md) listener application coordinate to achieve asynchronous deployments.

### Monitoring

After a deployment is ready, the control plane monitors the deployment and records various metrics, such as:

* CPU and memory usage of the deployment.
* Number of container restarts.
* Number of replicas (this will increase with [autoscaling](LangSmith%20data%20plane.md#autoscaling)).
* [PostgreSQL](LangSmith%20data%20plane.md#postgresql) CPU, memory usage, and disk usage.
* [Agent Server queue](../../Agent%20Server/Capabilities/Agent%20Server.md#task-queue) pending/active run count.
* [Agent Server API](../../Agent%20Server/Capabilities/Agent%20Server.md) success response count, error response count, and latency.

These metrics are displayed as charts in the Control Plane UI.

### LangSmith integration

A [LangSmith](../../../Monitor/Overview/LangSmith%20Observability.md) tracing project is automatically created for each deployment. The tracing project has the same name as the deployment. When creating a deployment, the `LANGCHAIN_TRACING` and `LANGSMITH_API_KEY`/`LANGCHAIN_API_KEY` environment variables do not need to be specified; they are set automatically by the control plane.

When a deployment is deleted, the traces and the tracing project are not deleted.
