# Generate query stats

As part of troubleshooting your self-hosted instance of LangSmith, the LangChain team may ask you to generate LangSmith query statistics that will help us understand the performance of various queries that drive the LangSmith product experience.

This command will generate a CSV that can be shared with the LangChain team.

### Prerequisites

Ensure you have the following tools/items ready.

1. kubectl

   * [https://kubernetes.io/docs/tasks/tools/](https://kubernetes.io/docs/tasks/tools/)

2. Clickhouse database credentials

   * Host
   * Port
   * Username
     * If using the bundled version, this is `default`
   * Password
     * If using the bundled version, this is `password`
   * Database name
     * If using the bundled version, this is `default`

3. Connectivity to the Clickhouse database from the machine you will be running the `get_query_stats` script on.

   * If you are using the bundled version, you may need to port forward the clickhouse service to your local machine.
   * Run `kubectl port-forward svc/langsmith-clickhouse 8123:8123` to port forward the clickhouse service to your local machine.

4. The script to generate query stats

   * Download the [query stats script](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/scripts/get_query_stats.sh)

### Running the query stats generation script

Run the following command to run the stats generation script:

```bash
sh get_query_stats.sh <clickhouse_url> --output path/to/file.csv
```

For example, if you are using the bundled version with port-forwarding, the command would look like:

```bash
sh get_query_stats.sh "clickhouse://default:password@localhost:8123/default" --output query_stats.csv
```

and after running this command you should see a file, query\_stats.csv, has been created with LangSmith query statistics.
