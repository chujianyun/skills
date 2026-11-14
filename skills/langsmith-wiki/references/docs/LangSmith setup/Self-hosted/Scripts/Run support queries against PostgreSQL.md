# Run support queries against PostgreSQL

This Helm repository contains queries to produce output that the LangSmith UI does not currently support directly (e.g. obtaining trace counts for multiple organizations in a single query).

This command takes a PostgreSQL connection string that contains an embedded name and password (which can be passed in from a call to a secrets manager) and executes a query from an input file. The following example uses the `pg_get_historic_trace_counts_daily.sql` input file in the `support_queries/postgres` directory.

## Prerequisites

Ensure you have the following tools/items ready.

1. kubectl

   * [https://kubernetes.io/docs/tasks/tools/](https://kubernetes.io/docs/tasks/tools/)

2. PostgreSQL client

   * [https://www.postgresql.org/download/](https://www.postgresql.org/download/)

3. PostgreSQL database connection:

   * Host
   * Port
   * Username
     * If using the bundled version, this is `postgres`
   * Password
     * If using the bundled version, this is `postgres`
   * Database name
     * If using the bundled version, this is `postgres`

4. Connectivity to the PostgreSQL database from the machine you will be running the migration script on.

   * If you are using the bundled version, you may need to port forward the postgresql service to your local machine.
   * Run `kubectl port-forward svc/langsmith-postgres 5432:5432` to port forward the postgresql service to your local machine.

5. The script to run a support query

   * Download the [PostgreSQL support query script](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/scripts/run_support_query_pg.sh)

## Running the query script

Run the following command to run the desired query:

```bash
sh run_support_query_pg.sh <postgres_url> --input path/to/query.sql
```

For example, if you are using the bundled version with port-forwarding, the command might look like:

```bash
sh run_support_query_pg.sh "postgres://postgres:postgres@localhost:5432/postgres" --input support_queries/postgres/pg_get_historic_trace_counts_daily.sql
```

which will output the count of daily traces by workspace ID and organization ID. To extract this to a file add the flag `--output path/to/file.csv`

## Export usage data

The UI and API exports cover all workspaces and organizations, with usage for:

* LangSmith traces
* LangSmith Deployments
* Fleet (Agent Builder)
* Usage snapshots (daily entity counts)
* Sandboxes
* LangSmith Engine
* LangSmith LLM Gateway

> [!NOTE]
>
> The UI and API exports require both of the following:
>
> * The `organization:manage` permission.
> * The caller's email must be listed in `USAGE_EXPORT_ADMIN_EMAILS`, or `ORG_ADMINS_INSTALLATION_USAGE_EXPORT_ENABLED` must be set to `true`.
>
> ```env theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> USAGE_EXPORT_ADMIN_EMAILS='["admin@example.com", "admin2@example.com"]'
> ORG_ADMINS_INSTALLATION_USAGE_EXPORT_ENABLED=true
> ```

### Export from the UI (recommended)

1. Navigate to **Settings** > **Usage and billing** > **Usage export**.
2. Click **Export usage data**.
3. A ZIP file containing all usage data will download.

### Export via API

If you prefer to export usage data programmatically, you can call the export API endpoint directly.

```bash
curl -OJ \
  -H "X-API-Key: <your_api_key>" \
  https://<langsmith_url>/api/v1/orgs/current/usage/backfill-export
```

### Export via SQL scripts

You can also run SQL scripts directly against your PostgreSQL database to export trace, node, Fleet, and usage snapshot data. This requires database access credentials. No application-level permissions apply.

To export trace usage (requires Helm chart version 0.11.4 or later):

```bash
sh run_support_query_pg.sh <postgres_url> \
  --input support_queries/postgres/pg_usage_traces_full_export.sql \
  --output ls_export.csv
```

To export node usage (requires Helm chart version 0.11.4 or later):

```bash
sh run_support_query_pg.sh <postgres_url> \
  --input support_queries/postgres/pg_usage_nodes_full_export.sql \
  --output lgp_export.csv
```

To export Fleet run counts (requires Helm chart version 0.13.25 or later):

```bash
sh run_support_query_pg.sh <postgres_url> \
  --input support_queries/postgres/pg_usage_agent_builder_full_export.sql \
  --output ab_export.csv
```

To export usage snapshots (daily entity counts such as workspaces, projects, datasets, prompts, and active users):

```bash
sh run_support_query_pg.sh <postgres_url> \
  --input support_queries/postgres/pg_usage_snapshots_full_export.sql \
  --output usage_snapshots_export.csv
```
