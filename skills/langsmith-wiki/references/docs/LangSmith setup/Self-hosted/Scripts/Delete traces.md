# Delete traces

The LangSmith UI does not currently support the deletion of an individual trace. This, however, can be accomplished by directly removing the trace from all materialized views in ClickHouse (except the runs\_history views) and the runs and feedback table themselves.

This command can either be run using a trace ID as an argument or using a file that is a list of trace IDs.

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

3. Connectivity to the Clickhouse database from the machine you will be running the `delete_trace_by_id` script on.

   * If you are using the bundled version, you may need to port forward the clickhouse service to your local machine.
   * Run `kubectl port-forward svc/langsmith-clickhouse 8123:8123` to port forward the clickhouse service to your local machine.

4. The script to delete a trace

   * Download the [trace script](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/scripts/delete_trace_by_id.sh)

> [!WARNING]
>
> **Batch size limits**
>
> This script issues `DELETE` mutations against multiple ClickHouse tables per batch. Large deletions can cause service disruption.
>
> * **Maximum 10,000 traces per run**: split larger files and process sequentially.
> * **Wait between batches**: allow time for deletions to complete before starting the next batch.
> * Use the `--sync` flag for sequential (slower but safer) deletion.

### Running the deletion script for a single trace

Run the following command to run the trace deletion script using a single trace ID:

```bash
sh delete_trace_by_id.sh <clickhouse_url> --trace_id <trace_id>
```

For example, if you are using the bundled version with port-forwarding, the command would look like:

```bash
sh delete_trace_by_id.sh "clickhouse://default:password@localhost:8123/default" --trace_id 4ec70ec7-0808-416a-b836-7100aeec934b
```

If you visit the LangSmith UI, you should now see specified trace ID is no longer present nor reflected in stats.

### Running the deletion script for a multiple traces from a file with one trace ID per line

Run the following command to run the trace deletion script using a list of trace IDs:

```bash
sh delete_trace_by_id.sh <clickhouse_url> --file <path/to/foo.txt>
```

For example, if you are using the bundled version with port-forwarding, the command would look like:

```bash
sh delete_trace_by_id.sh "clickhouse://default:password@localhost:8123/default" --file path/to/traces.txt
```

If you visit the LangSmith UI, you should now see all the specified traces have been removed.

## Troubleshooting

### "Could not find trace IDs" error

If you receive an error message stating that trace IDs could not be found, add the `--ssl` flag to your command. Without this flag, the script may not be able to properly connect to ClickHouse, resulting in false "trace ID not found" errors.

Example with SSL flag:

```bash
sh delete_trace_by_id.sh "clickhouse://default:password@localhost:8123/default" --file path/to/traces.txt --ssl
```

You can also verify that traces exist by connecting to ClickHouse directly using `clickhouse-cli` and querying for the trace IDs before running the deletion script.

### Service disruption after large deletion

If the service becomes unresponsive after deleting many traces, the deletion queue is likely overwhelmed.

**Prevention:** Limit deletions to 10,000 traces per run and wait several minutes between batches for deletions to process.

If you experience issues after a large deletion, contact [support](https://support.langchain.com/).
