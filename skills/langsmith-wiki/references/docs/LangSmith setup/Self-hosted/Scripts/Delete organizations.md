# Delete organizations

The LangSmith UI does not currently support the deletion of an individual organization from a self-hosted instance of LangSmith. This, however, can be accomplished by directly removing all traces from all materialized views in ClickHouse (except the runs\_history views) and the runs and feedbacks tables and then removing the Organization from the Postgres tenants table.

This command using the Organization ID as an argument.

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

7. The script to delete an organization

   * Download the [delete organization script](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/scripts/delete_organization_sh)

### Running the deletion script for a single organization

Run the following command to run the organization removal script:

```bash
sh delete_organization.sh <postgres_url> <clickhouse_url> --organization_id <organization_id>
```

For example, if you are using the bundled version with port-forwarding, the command would look like:

```bash
sh delete_organization.sh "postgres://postgres:postgres@localhost:5432/postgres" "clickhouse://default:password@localhost:8123/default" --organization_id 4ec70ec7-0808-416a-b836-7100aeec934b
```

If you visit the LangSmith UI, you should now see organization is no longer present.
