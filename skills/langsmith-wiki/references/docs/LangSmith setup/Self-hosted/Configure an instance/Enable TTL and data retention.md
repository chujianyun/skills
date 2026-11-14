# Enable TTL and data retention

LangSmith Self-Hosted supports automatic TTL and data retention for traces. Use this to comply with data privacy regulations or to reduce storage by automatically cleaning up old traces. Run rules and other qualifying actions can also extend a trace's retention period automatically.

> [!NOTE]
>
> **Self-hosted [Enterprise](https://docs.langchain.com/langsmith/pricing-plans.md) customers:** You can configure extended data retention at the workspace level through the UI. No environment variable changes are required. See [Customize extended retention policy](../../Govern/Data%20%26%20compliance/Data%20purging%20for%20compliance.md#customize-extended-retention-policy). The system-wide TTL configuration on this page is still supported.

## TTL configuration precedence

LangSmith determines how long to keep a trace in two steps: which retention tier the trace belongs to, and what period applies to that tier.

LangSmith assigns the tier in the following order, highest precedence first:

1. **Trace upgrade**: A run rule or other qualifying action promotes an individual trace to `longlived`, overriding whatever tier would otherwise apply.
2. **Project tier**: The tier configured for the tracing project.
3. **Workspace default**: New projects inherit this tier. Changing it affects new projects only unless you apply it to all existing projects.
4. **Organization default**: Applies to workspaces with no default of their own.
5. **`shortlived`**: The fallback when no default is set.

LangSmith then resolves the retention period for the assigned tier:

* **`longlived`**: The workspace extended retention period (if set through the UI), otherwise the `longlived` value from the [Helm configuration](#requirements).
* **`shortlived`**: The `shortlived` value from the [Helm configuration](#requirements).

The Helm chart defaults to 14 days for `shortlived` and 400 days for `longlived`.

## Requirements

Configure retention through Helm or environment variable settings:

* **Enabled**: Enable or disable automatic data retention. When enabled, set your default organization and project TTL tiers through the UI (see [data retention guide](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Usage%20and%20billing.md#data-retention)).
* **Retention periods**: Set system-wide retention periods for `shortlived` and `longlived` traces. Once set, manage retention at the project level or set an organization-wide default for new projects.

```yaml Helm
config:
  ttl:
    enabled: true
    ttl_period_seconds:
      # -- 400 day longlived and 14 day shortlived
      longlived: "34560000"
      shortlived: "1209600"
```

## ClickHouse TTL cleanup job

As of version 0.11, a cron job runs on weekends to delete expired data that ClickHouse's built-in TTL mechanism may not have cleaned up.

> [!WARNING]
>
> This job uses **mutations** (`ALTER TABLE DELETE`), which are expensive operations that can affect ClickHouse performance. Run them only during off-peak hours (nights and weekends). Testing with **1 concurrent active** mutation (the default) did not produce significant CPU, memory, or latency increases.

### Default schedule

By default, the cleanup job runs:

* **Saturday**: 8pm and 10pm UTC.
* **Sunday**: 12am, 2am, and 4am UTC.

### Disabling the job

To disable the cleanup job entirely:

```yaml
queue:
  deployment:
    extraEnv:
      - name: "ENABLE_CLICKHOUSE_TTL_CLEANUP_CRON"
        value: "false"
```

### Configuring the schedule

Customize when the cleanup job runs by modifying the cron expressions:

```yaml
queue:
  deployment:
    extraEnv:
      # UTC: Sunday 12am/2am/4am
      - name: "CLICKHOUSE_TTL_CLEANUP_CRON_WEEKEND_MORNING"
        value: "0 0,2,4 * * 0"
      # UTC: Saturday 8pm/10pm
      - name: "CLICKHOUSE_TTL_CLEANUP_CRON_WEEKEND_EVENING"
        value: "0 20,22 * * 6"
```

> [!TIP]
>
> To use a single cron schedule, set both `CLICKHOUSE_TTL_CLEANUP_CRON_WEEKEND_EVENING` and `CLICKHOUSE_TTL_CLEANUP_CRON_WEEKEND_MORNING` to the same value. Job locking prevents overlapping executions.

### Configuring minimum expired rows per part

The job works through the tables one at a time. Within each table it scans the parts and deletes data from any part holding at least a minimum number of expired rows. This threshold balances efficiency and thoroughness:

* **Too low**: The job scans entire parts to clear minimal data (inefficient).
* **Too high**: The job skips parts with significant expired data.

```yaml
queue:
  deployment:
    extraEnv:
      - name: "CLICKHOUSE_TTL_CRON_MIN_EXPIRED_ROWS_PER_PART"
        value: "100000" # 100k expired rows
```

#### Checking expired rows

Run this query to see expired rows per table part, then tune your minimum value:

```sql
-- Query for Runs table. For other tables, replace 'ttl_seconds' with 'trace_ttl_seconds'
SELECT
    _part,
    count() AS expired_rows
FROM runs
WHERE trace_first_received_at IS NOT NULL
AND ttl_seconds IS NOT NULL
AND toDateTime(assumeNotNull(trace_first_received_at) + toIntervalSecond(assumeNotNull(ttl_seconds))) < now()
GROUP BY _part
ORDER BY expired_rows DESC
```

### Configuring maximum active mutations

Delete operations can take around 50 minutes for a 100 GB part. Increase concurrent mutations to speed up cleanup:

```yaml
queue:
  deployment:
    extraEnv:
      - name: "CLICKHOUSE_TTL_CRON_MAX_ACTIVE_MUTATIONS"
        value: "1"
```

> [!WARNING]
>
> More concurrent `DELETE` operations can significantly slow inserts and reads. Increase this value only if you can tolerate slower insert and read latencies, and monitor the system after you do.

### Emergency: Stopping running mutations

If you see latency spikes and need to stop a running mutation:

1. **Find active mutations**:

   ```sql
   SELECT * FROM system.mutations WHERE is_done = 0;
   ```

   Find the `mutation_id` where the `command` column contains a `DELETE` statement.

2. **Kill the mutation**:

   ```sql
   KILL MUTATION WHERE mutation_id = '<mutation_id>';
   ```

### Backups and data retention

If disk space does not decrease after the job runs, or keeps growing, backups may be the cause. Backup processes create filesystem hard links that prevent ClickHouse from releasing data.

Check these directories inside your ClickHouse pod:

* `/var/lib/clickhouse/backup`
* `/var/lib/clickhouse/shadow`

If backups are present, copy them to external storage (for example, S3), then clear the directories. Disk space should start releasing within a few minutes.

## Keep run statistics after traces expire

After traces expire, LangSmith keeps their run statistics, such as run counts, latency, and error rates, until the extended (`longlived`) retention period passes. LangSmith then removes the remaining stored data, and those run statistics are no longer available. For how LangSmith resolves the `longlived` period, see [TTL configuration precedence](#ttl-configuration-precedence).

> [!NOTE]
>
> This applies to [SmithDB](../SmithDB/Overview/Enable%20SmithDB%20on%20self-hosted%20LangSmith.md) installations on LangSmith 0.18 (Helm chart `0.18.0` or later).

To keep run statistics available for longer, set `SMITHDB_COMPACTION__EXPIRY_CYCLE__RETENTION_CLEANUP_BUFFER` to a duration such as `30d` or `720h`. LangSmith waits this long past the `longlived` period before it removes the data. The default is `0s`.

For example, with the default 400-day `longlived` period and a `30d` buffer, run statistics stay available for at least 430 days after LangSmith receives a trace.

```yaml Helm
smithdb:
  compaction:
    deployment:
      extraEnv:
        - name: SMITHDB_COMPACTION__EXPIRY_CYCLE__RETENTION_CLEANUP_BUFFER
          value: "30d"
```

If SmithDB runs as a single pod, set the variable under `smithdb.single.deployment.extraEnv` instead.
