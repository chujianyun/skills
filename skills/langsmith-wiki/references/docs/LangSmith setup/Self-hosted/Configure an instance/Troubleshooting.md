# Troubleshooting

This guide will walk you through common issues you may encounter when running a self-hosted instance of LangSmith.

While running LangSmith, you may encounter unexpected 500 errors, slow performance, or other issues. This guide will help you diagnose and resolve these issues.

## Getting helpful information

To diagnose and resolve an issue, you will first need to retrieve some relevant information. The following sections explain how to do this for a Kubernetes or a Docker setup, and how to pull helpful browser information.

Generally, the main services you will want to analyze are the:

* `langsmith-backend`: Handles CRUD API requests, business logic, requests from the frontend and SDK, trace preparation for ingestion, and the hub API.
* `langsmith-platform-backend`: Handles authentication, run ingestion, and other high-volume tasks.
* `langsmith-queue`: Handles incoming traces and feedback, asynchronous ingestion and persistence into the datastore, data integrity checks, and retries during database errors or connection issues.

For more details on these services, refer to the [self-hosted overview](../Self-hosted%20LangSmith.md).

#### Kubernetes

The first step in troubleshooting is to gather important debugging information about your LangSmith deployment. Service logs, kubernetes events, and resource utilization of containers can help identify the root cause of an issue.

You can run our [k8s troubleshooting script](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/scripts/get_k8s_debugging_info.sh) which will pull all of the relevant kubernetes information and output it to a folder for investigation. The script also compresses this folder into a zip file for sharing. Here is an example of how to run this script, assuming your langsmith deployment was brought up in a `langsmith` namespace:

```bash
bash get_k8s_debugging_info.sh --namespace langsmith
```

You can then inspect the contents of the produced folder for any relevant errors or information. If you would like the LangSmith team to assist in debugging, please share this zip file with the team.

#### Docker

If running on Docker, you can check the logs your deployment by running the following command:

```bash
docker compose logs >> logs.txt
```

#### Browser errors

If you are experiencing an issue that surfaces as a browser error, it may also be helpful to inspect a HAR file which may include key information. To get the HAR file, you can follow [this guide](https://support.langchain.com/articles/9042697994-how-to-generate-a-har-file-for-troubleshooting) which explains the short process for various browsers.

You can then use [Google's HAR analyzer](https://toolbox.googleapps.com/apps/har_analyzer/) to investigate. You can also send your HAR file to the LangSmith team to help with debugging.

## Common issues

### *DB::Exception: Cannot reserve 1.00 MiB, not enough space: While executing WaitForAsyncInsert. (NOT\_ENOUGH\_SPACE)*

This error occurs when ClickHouse runs out of disk space. You will need to increase the disk space available to ClickHouse.

#### Kubernetes

In Kubernetes, you will need to increase the size of the ClickHouse PVC. To achieve this, you can perform the following steps:

1. Get the storage class of the PVC: `kubectl get pvc data-langsmith-clickhouse-0 -n <namespace> -o jsonpath='{.spec.storageClassName}'`

2. Ensure the storage class has AllowVolumeExpansion: true: `kubectl get sc <storage-class-name> -o jsonpath='{.allowVolumeExpansion}'`

   * If it is false, some storage classes can be updated to allow volume expansion.
   * To update the storage class, you can run `kubectl patch sc <storage-class-name> -p '{"allowVolumeExpansion": true}'`
   * If this fails, you may need to create a new storage class with the correct settings.

3. Edit your pvc to have the new size: `kubectl edit pvc data-langsmith-clickhouse-0 -n <namespace>` or `kubectl patch pvc data-langsmith-clickhouse-0 '{"spec":{"resources":{"requests":{"storage":"100Gi"}}}}' -n <namespace>`

4. Update your helm chart `langsmith_config.yaml` to new size(e.g `100 Gi`)

5. Delete the clickhouse statefulset `kubectl delete statefulset langsmith-clickhouse --cascade=orphan -n <namespace>`

6. Apply helm chart with updated size (You can follow the [upgrade guide](../Manage%20an%20instance/Upgrade%20an%20installation.md))

7. Your pvc should now have the new size. Verify by running `kubectl get pvc` and `kubectl exec langsmith-clickhouse-0 -- bash -c "df"`

#### Docker

In Docker, you will need to increase the size of the ClickHouse volume. To achieve this, you can perform the following steps:

1. Stop your instance of LangSmith. `docker compose down`
2. If using bind mount, you will need to increase the size of the mount point.
3. If using a docker `volume`, you will need to allocate more space to the volume/docker.

### *error: Dirty database version 'version'. fix and force version*

This error occurs when the ClickHouse database is in an inconsistent state with our migrations. You will need to reset to an earlier database version and then rerun your upgrade/migrations.

#### Kubernetes

1. Force migration to an earlier version, where version = dirty version - 1.

```bash
kubectl exec -it deployments/langsmith-backend -- bash -c 'migrate -source "file://clickhouse/migrations" -database "clickhouse://$CLICKHOUSE_HOST:$CLICKHOUSE_NATIVE_PORT?username=$CLICKHOUSE_USER&password=$CLICKHOUSE_PASSWORD&database=$CLICKHOUSE_DB&x-multi-statement=true&x-migrations-table-engine=MergeTree&secure=$CLICKHOUSE_TLS" force <version>'
```

1. Rerun your upgrade/migrations.

#### Docker

1. Force migration to an earlier version, where version = dirty version - 1.

```bash
docker compose exec langchain-backend migrate -source "file://clickhouse/migrations" -database "clickhouse://$CLICKHOUSE_HOST:$CLICKHOUSE_NATIVE_PORT?username=$CLICKHOUSE_USER&password=$CLICKHOUSE_PASSWORD&database=$CLICKHOUSE_DB&x-multi-statement=true&x-migrations-table-engine=MergeTree&secure=$CLICKHOUSE_TLS" force <version>
```

1. Rerun your upgrade/migrations.

### *413 - request entity too large*

This error occurs when the request size exceeds the maximum allowed size. You will need to increase the maximum request size in your Nginx configuration.

#### Kubernetes

1. Edit your `langsmith_config.yaml` and increase the `frontend.maxBodySize` [value](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/values.yaml#L519). This might look something like this:

```yaml
frontend:
  maxBodySize: "100M"
```

2. Apply your changes to the cluster.

### *Details: code: 497, message: default: Not enough privileges. to execute this query, it's necessary to have the grant CREATE ROW POLICY ON default.feedbacks\_rmt*

This error occurs when your user does not have the necessary permissions to create row policies in Clickhouse. When deploying the Docker deployment, you need to copy the `users.xml` file from the github repo as well. This adds the `<access_management>` tag to the `users.xml` file, which allows the user to create row policies. Below is the default `users.xml` file that we expect to be used.

```xml
<clickhouse>
    <users>
        <default>
            <access_management>1</access_management>
            <named_collection_control>1</named_collection_control>
            <show_named_collections>1</show_named_collections>
            <show_named_collections_secrets>1</show_named_collections_secrets>
            <profile>default</profile>
        </default>
    </users>
    <profiles>
        <default>
            <async_insert>1</async_insert>
            <async_insert_max_data_size>2000000</async_insert_max_data_size>
            <wait_for_async_insert>0</wait_for_async_insert>
            <parallel_view_processing>1</parallel_view_processing>
            <allow_simdjson>0</allow_simdjson>
            <lightweight_deletes_sync>0</lightweight_deletes_sync>
        </default>
    </profiles>
</clickhouse>
```

In some environments, your mount point may not be writable by the container. In these cases we suggest building a custom image with the `users.xml` file included.

Example `Dockerfile`:

```dockerfile
FROM clickhouse/clickhouse-server:24.8
COPY ./users.xml /etc/clickhouse-server/users.d/users.xml
```

Then take the following steps:

1. Build your custom image.

```bash
docker build -t <image-name> .
```

2. Update your `docker-compose.yaml` to use the custom image. Make sure to remove the users.xml mount point.

```yaml
langchain-clickhouse:
  image: <image-name>
```

3. Restart your instance of LangSmith.

```bash
docker compose down --volumes
docker compose up
```

### *ClickHouse fails to start up when running a cluster with AquaSec*

In some environments, AquaSec may prevent ClickHouse from starting up correctly. This may manifest as the ClickHouse pod not emitting any logs and failing to get marked as ready.
Generally this is due to `LD_PRELOAD` being set by AquaSec, which interferes with ClickHouse. To resolve this, you can add the following environment variable to your ClickHouse deployment:

#### Kubernetes

Edit your `langsmith_config.yaml` (or corresponding config file) and set the `AQUA_SKIP_LD_PRELOAD` environment variable:

```yaml
clickhouse:
  statefulSet:
    extraEnv:
      - name: AQUA_SKIP_LD_PRELOAD
        value: "true"
```

#### Docker

Edit your `docker-compose.yaml` and set the `AQUA_SKIP_LD_PRELOAD` environment variable:

```yaml
langchain-clickhouse:
  environment:
    - AQUA_SKIP_LD_PRELOAD=true
```
