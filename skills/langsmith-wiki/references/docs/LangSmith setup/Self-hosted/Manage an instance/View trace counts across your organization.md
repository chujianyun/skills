# View trace counts across your organization

> [!NOTE]
>
> This feature is available on Helm chart versions 0.9.5 and later.

LangSmith automatically generates and syncs organization usage charts for self-hosted installations.

These charts are available under `Settings > Usage and billing > Usage graph`:

* Usage by Workspace: this counts traces (root runs) by workspace
* Organization Usage: this counts all traces (root runs) for the organization

The charts are refreshed to include any new workspaces every 5 minutes. Note that the charts are not editable.

## Programmatically fetch trace counts

You can retrieve trace counts programmatically using two different methods:

### Method 1: Use the LangSmith REST API

If your self-hosted installation uses an online key, you can use the [LangSmith REST API](../../../Monitor/Reference/LangSmith%20REST%20API/Administration/Get%20org%20usage.md) to fetch organization usage data.

```bash
curl -X GET "https://your-langsmith-instance.com/api/v1/orgs/current/billing/usage" \
  -H "Accept: application/json" \
  -H "X-API-Key: your-api-key" \
  -G \
  -d "starting_on=2025-09-01T00:00:00Z" \
  -d "ending_before=2025-10-01T00:00:00Z" \
  -d "on_current_plan=true"
```

### Method 2: Use PostgreSQL support queries

For installations using offline keys or when you need more detailed export capabilities, you can run support queries directly against the PostgreSQL database. All available scripts are in the [support queries repository](https://github.com/langchain-ai/helm/tree/main/charts/langsmith/scripts/support_queries/postgres).

```bash
sh run_support_query_pg.sh "postgres://postgres:postgres@localhost:5432/postgres" \
  --input support_queries/postgres/pg_get_historic_trace_counts_daily.sql \
  --output trace_counts.csv
```

For more detailed information about running support queries, see the [Run support queries against PostgreSQL](../Scripts/Run%20support%20queries%20against%20PostgreSQL.md) guide.
