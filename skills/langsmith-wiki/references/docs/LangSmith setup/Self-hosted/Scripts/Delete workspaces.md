# Delete workspaces

> [!NOTE]
>
> Deleting a workspace is supported **nativley in LangSmith Self-Hosted v0.10**. View [instructions for deleting a workspace](../../Govern/Organization/Workspace%20setup/Set%20up%20hierarchy.md#delete-a-workspace).
>
> Follow the guide below for Self-Hosted versions before v0.10.

The LangSmith UI does not currently support the deletion of an individual workspace from an organization. This, however, can be accomplished by directly removing all traces from all materialized views in ClickHouse (except the runs\_history views) and the runs and feedbacks tables and then removing the Workspace from the Postgres tenants table.

This command using the Workspace ID as an argument.

### Prerequisites

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

4. Clickhouse database credentials

   * Host
   * Port
   * Username
     * If using the bundled version, this is `default`
   * Password
     * If using the bundled version, this is `password`
   * Database name
     * If using the bundled version, this is `default`

5. Connectivity to the PostgreSQL database from the machine you will be running the migration script on.

   * If you are using the bundled version, you may need to port forward the postgresql service to your local machine.
   * Run `kubectl port-forward svc/langsmith-postgres 5432:5432` to port forward the postgresql service to your local machine.

6. Connectivity to the Clickhouse database from the machine you will be running the migration script on.

   * If you are using the bundled version, you may need to port forward the clickhouse service to your local machine.
     * Run `kubectl port-forward svc/langsmith-clickhouse 8123:8123` to port forward the clickhouse service to your local machine.
   * If you are using Clickhouse Cloud you will want to specify the --ssl flag and use port `8443`

7. The script to delete a workspace

   * Download the [workspace script](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/scripts/delete_workspace.sh)

### Running the deletion script for a single workspace

Run the following command to run the workspace removal script:

```bash
sh delete_workspace.sh <postgres_url> <clickhouse_url> --workspace_id <workspace_id>
```

For example, if you are using the bundled version with port-forwarding, the command would look like:

```bash
sh delete_workspace.sh "postgres://postgres:postgres@localhost:5432/postgres" "clickhouse://default:password@localhost:8123/default" --workspace_id 4ec70ec7-0808-416a-b836-7100aeec934b
```

If you visit the LangSmith UI, you should now see workspace is deleted.
