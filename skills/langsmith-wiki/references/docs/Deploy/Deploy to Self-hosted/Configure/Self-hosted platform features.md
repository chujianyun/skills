# Self-hosted platform features

> Self-hosted-only platform features for LangSmith Agent Server, including custom databases, listeners, and resource customization.

This page describes the platform features that apply only to [self-hosted](../../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) deployments.

## Custom PostgreSQL

A custom PostgreSQL instance can be used instead of the [one automatically created by the control plane](../../Deploy%20to%20Cloud/Cloud%20platform%20features.md#database-provisioning). Specify the [`POSTGRES_URI_CUSTOM`](../Reference/Self-hosted%20Agent%20Server%20environment%20variables.md) environment variable to use a custom PostgreSQL instance. To authenticate with a cloud workload identity instead of a static password, see [Configure IAM authentication for data stores](../../Agent%20Server/Server%20customization/Configure%20IAM%20authentication%20for%20data%20stores.md).

Multiple deployments can share the same PostgreSQL instance. For example, for `Deployment A`, `POSTGRES_URI_CUSTOM` can be set to `postgres://<user>:<password>@/<database_name_1>?host=<hostname_1>` and for `Deployment B`, `POSTGRES_URI_CUSTOM` can be set to `postgres://<user>:<password>@/<database_name_2>?host=<hostname_1>`. `<database_name_1>` and `<database_name_2>` are different databases within the same instance, but `<hostname_1>` is shared. **The same database cannot be used for separate deployments**.

## Custom Redis

A custom Redis instance can be used instead of the one automatically created by the control plane. Specify the [`REDIS_URI_CUSTOM`](../Reference/Self-hosted%20Agent%20Server%20environment%20variables.md) environment variable to use a custom Redis instance. To authenticate with a cloud workload identity instead of a static password, see [Configure IAM authentication for data stores](../../Agent%20Server/Server%20customization/Configure%20IAM%20authentication%20for%20data%20stores.md).

Multiple deployments can share the same Redis instance. For example, for `Deployment A`, `REDIS_URI_CUSTOM` can be set to `redis://<hostname_1>:<port>/1` and for `Deployment B`, `REDIS_URI_CUSTOM` can be set to `redis://<hostname_1>:<port>/2`. `1` and `2` are different database numbers within the same instance, but `<hostname_1>` is shared. **The same database number cannot be used for separate deployments**.

Redis Cluster supports only database `0`, so deployments cannot share a Redis Cluster by database number. To share one Redis server across deployments, use a standalone Redis instance with a separate database number for each deployment.

## Listeners

A listener is an instance of a [listener application](../../Get%20started/Deployment%20components/LangSmith%20data%20plane.md#listener-application). A listener contains metadata about the application (such as its version) and metadata about the compute infrastructure where it can deploy to (such as Kubernetes namespaces).

The listener data model only applies to self-hosted deployments. The control plane and listener coordinate to provision and reconcile deployments running on your own infrastructure.

### Listener version requirements

Keep the listener current before you change a deployment's `resource_spec`. The control plane validates a `PATCH` against the rules of its own version. The listener then validates the stored `resource_spec` again against the rules of its own version when it applies the revision. If the listener is older than the control plane, a `PATCH` can return `200` and the revision then fails with `DEPLOY_FAILED`.

The rejected value stays in the stored `resource_spec`, so every later revision of that deployment also fails, including image-only deploys, until you `PATCH` the deployment with a value the listener accepts.

The following `resource_spec` fields depend on the listener version:

| Field | Minimum listener version |
| :- | :- |
| Fractional `cpu` and `queue_cpu` values (for example, `0.5`) | Later than 0.12.x. Listener 0.12.x rejects fractional values. |
| `redis_cpu` and `redis_cpu_limit` | 0.13.22 or later. Earlier listeners ignore these fields. |
| `redis_memory_mb` below `2048` | 0.13.27 or later. Earlier listeners require at least `2048`. |
| `volumes` and `volume_mounts` | 0.11.30 or later. Earlier listeners ignore these fields, and the deployment starts without the volume. |

Upgrading the listener does not restart existing deployments. After you upgrade, `PATCH` each deployment with its full `resource_spec` to apply the new values. For the accepted ranges and `PATCH` behavior, see [Resource spec](../../Get%20started/Reference/Control%20Plane%20API/Control%20plane%20API%20reference%20for%20Agent%20Server%20hosting.md#resource-spec).

## Resource customization

You set resources for each self-hosted deployment, including its Redis and PostgreSQL instances, through the deployment's `resource_spec`. Unlike Cloud, which exposes fixed Serverless and Dedicated [deployment types](../../Deploy%20to%20Cloud/Cloud%20platform%20features.md#deployment-types), self-hosted deployments size CPU, memory, replicas, and storage according to your infrastructure configuration. Some fields, such as Redis CPU, require a minimum listener version. See [Listener version requirements](#listener-version-requirements).

The `db_*` fields size the PostgreSQL instance that the control plane creates, and the `redis_*` fields size the Redis instance. If a deployment uses [custom PostgreSQL](#custom-postgresql) or [custom Redis](#custom-redis), the matching fields have no effect.

There are no organization or workspace defaults for deployment resources. Fields you do not set fall back to the defaults for the deployment type, so send a full `resource_spec` when you create each deployment. See [Configure Agent Server for scale](Configure%20Agent%20Server%20for%20scale.md) for tuning guidance.

## Volumes

You can mount Kubernetes volumes into a deployment's pods. For example, mount a PersistentVolumeClaim backed by Amazon EFS, NFS, or another CSI driver. A mounted volume lets your agent read and write files that persist across restarts, or that several replicas share. The operator adds the volumes to the main container of both the API server and the queue worker pods.

These volumes are storage for your agent's runtime. They are separate from the storage that the LangSmith platform itself uses, such as PostgreSQL, Redis, and blob storage. LangSmith does not provision the storage or create the PersistentVolumeClaim. You create both in your cluster, and the deployment only mounts them.

Set volumes in one of two places:

* **One deployment**: Set `volumes` and `volume_mounts` in the deployment's `resource_spec` through the [control plane API](../../Get%20started/Reference/Control%20Plane%20API/Control%20plane%20API%20reference%20for%20Agent%20Server%20hosting.md). These fields require listener 0.11.30 or later. See [Listener version requirements](#listener-version-requirements). You cannot add PersistentVolumeClaims or other general-purpose volumes in the LangSmith UI. Saving deployment settings in the UI keeps the volumes and mounts that you set through the API.
* **Every deployment**: Add `volumes` and `volumeMounts` to the operator's base deployment template in your Helm values (`operator.templates.deployment`). For an example of editing that template, see [Configure authentication for private registries](../../../LangSmith%20setup/Self-hosted/Install%20an%20instance/Additional%20features/Enable%20Agent%20Server%20hosting.md#configure-authentication-for-private-registries).

If the base template and the deployment's `resource_spec` both set a volume or volume mount with the same `name`, the deployment's `resource_spec` takes precedence.

To mount a volume on one deployment:

1. Create the PersistentVolumeClaim in the Kubernetes namespace where the deployment runs. For Amazon EFS, install the [Amazon EFS CSI driver](https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html), and use an EFS StorageClass with the `ReadWriteMany` access mode. `ReadWriteMany` lets every replica mount the volume.
2. Call `PATCH /v2/deployments/{deployment_id}` with the volume and its mount in `source_config.resource_spec`. A `PATCH` that includes `resource_spec` replaces the whole object, so include your existing `min_scale`, `max_scale`, `cpu`, `memory_mb`, and other `resource_spec` values. Each `volumes` entry takes a `name` and exactly one volume source: `persistentVolumeClaim`, `csi`, `nfs`, `configMap`, `secret`, `emptyDir`, `projected`, or `downwardAPI`. The control plane passes the source object to Kubernetes unchanged. Write its keys in Kubernetes camelCase, for example `claimName`:

   ```json
   {
     "source_config": {
       "resource_spec": {
         "min_scale": 1,
         "max_scale": 3,
         "cpu": 1,
         "memory_mb": 2048,
         "volumes": [
           {
             "name": "shared-files",
             "persistentVolumeClaim": { "claimName": "efs-claim" }
           }
         ],
         "volume_mounts": [
           { "name": "shared-files", "mountPath": "/mnt/shared" }
         ]
       }
     }
   }
   ```

   Volume names must be unique, valid DNS labels: lowercase letters, digits, and hyphens, up to 63 characters. Each `mountPath` must be an absolute path. No two entries in `volume_mounts` can use the same `mountPath`.

   For more information, see [Resource spec](../../Get%20started/Reference/Control%20Plane%20API/Control%20plane%20API%20reference%20for%20Agent%20Server%20hosting.md#resource-spec).
3. Poll the new revision until its `status` is `DEPLOYED`.
4. Confirm that the app container can read and write at `mountPath` in both the API server and queue worker pods. A `Bound` PersistentVolumeClaim does not guarantee that the container's user has write permission on the volume. To check write access, run the following command against each pod:

   ```bash
   kubectl exec <pod-name> -n <namespace> -- sh -c 'touch /mnt/shared/.write-test && rm /mnt/shared/.write-test'
   ```

## PodDisruptionBudgets

Starting in operator 0.1.60 (`langgraph-dataplane` chart 0.2.24), the operator creates a PodDisruptionBudget with `minAvailable: 1` for a deployment's API server and queue worker Deployments when their minimum replica count is 2 or more. You cannot turn these PodDisruptionBudgets off.

Before you upgrade to operator 0.1.60 or later, remove any PodDisruptionBudgets of your own that select the same pods. When two PodDisruptionBudgets select the same pod, Kubernetes cannot evict it, so node drains and other evictions fail.
