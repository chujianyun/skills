# Data purging for compliance

This guide covers the various features available after data reaches LangSmith Cloud servers to help you achieve your privacy goals.

## Data retention

LangSmith provides automatic data retention capabilities to help with compliance and storage management. Data retention policies can be configured at two levels:

* **Workspace level**: Enterprise customers with the required permissions can set extended retention as the workspace default and customize the retention duration (up to 180 days as of September 14, 2026). See [Customize extended retention policy](#customize-extended-retention-policy).
* **Project level**: Customers with the required permissions can set the default retention tier per tracing project, choosing between base (14 days) or extended retention (180 days). See [Change project-level default retention](../../Account/Billing%20%26%20usage/Manage%20billing%20in%20your%20account.md#change-project-level-default-retention).

For detailed information about data retention configuration and management, please refer to the [Data Retention concepts](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#data-retention) documentation.

## Customize extended retention policy

> [!NOTE]
>
> This feature is available for [Enterprise](https://docs.langchain.com/langsmith/pricing-plans.md) plan customers. For [self-hosted](../../Self-hosted/Self-hosted%20LangSmith.md) Enterprise customers, refer to the [workspace-level configuration section](#workspace-level-extended-retention-for-self-hosted).

[Enterprise](https://docs.langchain.com/langsmith/pricing-plans.md) customers can customize the extended data retention period for traces at the [workspace](../Organization/Overview.md#workspaces) level to meet specific compliance requirements. Beginning September 14, 2026, the maximum long-lived trace retention period for SaaS customers is 180 days. You can adjust the retention period below this maximum based on your organization's needs. Changes to the retention period apply to new traces only.

> [!NOTE]
>
> Changes to the retention period apply to new traces only. Existing traces are not affected.

### Configure extended retention

Organization Admins and Operators (`organization:manage`) can configure retention for any workspace. Workspace Admins can configure their own workspace (`workspaces:manage`). For a full permissions reference, see [Organization and workspace operations](../Users%20%26%20access%20control/Organization%20and%20workspace%20operations%20reference.md).

> [tab] UI
>
> In the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-data-purging-compliance):
>
> 1. Navigate to **Settings** at the bottom of the page.
> 2. Select **Usage configuration** from the left-hand menu.
> 3. Find the workspace in the list that you would like to configure.
> 4. Click on the value under the **Data retention policy** column for that workspace.
> 5. On the **workspace usage configurations** modal, customize the extended policy using the dropdown for **Extended - All traces are retained for** option. Available durations for SaaS customers are: 30d, 60d, 90d, 120d, 150d, and 180d (maximum as of September 14, 2026). Self-hosted deployments are not subject to this cap.
> 6. Select **Save**.

> [tab] API
>
> To read current settings:
>
> **Organization level** (`organization:manage`)
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl -X GET "https://api.smith.langchain.com/api/v1/orgs/ttl-settings" \
>   -H "x-api-key: YOUR_API_KEY"
> ```
>
> **Workspace level** (`workspaces:manage`)
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl -X GET "https://api.smith.langchain.com/api/v1/ttl-settings" \
>   -H "x-api-key: YOUR_API_KEY"
> ```
>
> To update the retention period, set `resource_type` to `"run"` for traces and `ttl_days` to your desired duration. Available durations for SaaS customers are: 30, 60, 90, 120, 150, and 180 days (maximum as of September 14, 2026).
>
> **Organization level** (`organization:manage`)
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl -X PUT "https://api.smith.langchain.com/api/v1/orgs/ttl-settings" \
>   -H "x-api-key: YOUR_API_KEY" \
>   -H "Content-Type: application/json" \
>   -d '{"resource_type": "run", "ttl_days": 90}'
> ```
>
> **Workspace level** (`workspaces:manage`)
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl -X PUT "https://api.smith.langchain.com/api/v1/ttl-settings" \
>   -H "x-api-key: YOUR_API_KEY" \
>   -H "Content-Type: application/json" \
>   -d '{"resource_type": "run", "ttl_days": 90}'
> ```

### Workspace-level extended retention for self-hosted

Self-hosted [Enterprise](https://docs.langchain.com/langsmith/pricing-plans.md) customers can also use workspace-level extended retention configuration instead of system-wide TTL settings. This provides more granular control over data retention for different workspaces without requiring environment variable changes.

> [!WARNING]
>
> If you use blob storage, you **must** add a lifecycle rule for each custom retention period you configure. For example, setting a workspace to 90-day retention means blob data is written to the `ttl_90d/` prefix, which requires a matching lifecycle rule to be cleaned up automatically. See [blob storage TTL configuration](../../Self-hosted/Connect%20external%20services/Enable%20blob%20storage.md#custom-workspace-level-retention-prefixes) for details and examples.

To configure this for self-hosted deployments, refer to the [self-hosted TTL documentation](../../Self-hosted/Configure%20an%20instance/Enable%20TTL%20and%20data%20retention.md) for the legacy system-wide approach or contact [support](https://support.langchain.com).

## Trace deletes

You can use the API to complete trace deletes. The API supports two methods for deleting traces:

1. **By trace IDs and session ID**: Delete specific traces by providing a list of trace IDs and their corresponding session ID (up to 1000 traces per request)
2. **By metadata**: Delete traces across a workspace that match any of the specified metadata key-value pairs

For more details, refer to the [API spec](../../../Monitor/Reference/LangSmith%20REST%20API/Tracing/Delete%20runs.md).

> [!WARNING]
>
> All trace deletions will delete related entities like feedbacks, aggregations, and stats across all data storages.

### Deletion timeline

Trace deletions are processed during non-peak usage times and are not instant. SmithDB may make traces unqueryable right away. Most deletes are hardened within 6 hours or sooner. To confirm deletion, query the data again to verify it has been removed.

### Delete specific traces

To delete specific traces by their trace IDs from a single session:

> [!NOTE]
>
> The `session_id` is the project ID for the trace you are trying to delete. You can find it on the tracing project page in the LangSmith UI.

```bash
curl -X POST "https://api.smith.langchain.com/api/v1/runs/delete" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "trace_ids": ["trace-id-1", "trace-id-2", "trace-id-3"],
    "session_id": "session-id-1"
  }'
```

## Example deletes

You can delete dataset examples self-serve via our API, which supports both soft and hard deletion methods depending on your data retention needs.

> [!WARNING]
>
> Hard deletes will permanently remove inputs, outputs, and metadata from ALL versions of the specified examples across the entire dataset history.

### Deleting examples is a two-step process

For bulk operations, example deletion follows a two-step process:

#### 1. Search for examples by metadata

Find all examples with matching metadata across all datasets in a workspace.

[GET /examples](../../../Monitor/Reference/LangSmith%20REST%20API/Datasets/Read%20examples.md)

* `as_of` must be explicitly specified as a timestamp. Only examples created before the `as_of` date will be returned

```bash
curl -X GET "https://api.smith.langchain.com/api/v1/examples?as_of=2024-01-01T00:00:00Z" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {
      "user_id": "user123",
      "environment": "staging"
    }
  }'
```

This will return examples that have either `user_id: "user123"` **or** `environment: "staging"` in their metadata across all datasets in your workspace.

#### 2. Hard delete examples

Once you have the example IDs, send a delete request. This will zero-out the inputs, outputs, and metadata from all versions of the dataset for that example.

[POST /v1/platform/datasets/examples/delete/](../../../Monitor/Reference/LangSmith%20REST%20API/Datasets/Hard%20delete%20examples.md)

* Specify `example_ids` (list of example IDs) and `hard_delete` (boolean) in the request body

```bash
curl -X POST "https://api.smith.langchain.com/v1/platform/datasets/examples/delete/" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "example_ids": ["example-id-1", "example-id-2", "example-id-3"],
    "hard_delete": true
  }'
```

### Deletion types

#### Soft delete (default)

* Creates tombstoned entries with NULL inputs/outputs in the dataset
* Preserves historical data and maintains dataset versioning
* Only affects the current version of the dataset

#### Hard delete

* Permanently removes inputs, outputs, and metadata from ALL dataset versions
* Complete data removal when compliance requires zero-out across all versions
* Set `"hard_delete": true` in the request body
