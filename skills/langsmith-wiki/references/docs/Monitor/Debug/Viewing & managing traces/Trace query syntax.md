# Trace query syntax

The [LangSmith SDK](https://reference.langchain.com/python/langsmith/) and [REST API](../../Reference/LangSmith%20REST%20API/LangSmith%20API%20reference.md) let you filter, query, and export [runs](../../Trace/Observability%20concepts.md#runs) programmatically using a set of filter arguments and a structured filter query language. This page documents the filter arguments and query language, with examples for common queries.

For runnable end-to-end examples that combine these filters with the SDK, refer to [Query traces using the SDK](Query%20traces%20using%20the%20SDK.md).

## Filter arguments

| Keys | Description |
| - | - |
| `project_id` / `project_name` | The project(s) to fetch runs from, as a single project or a list of projects. |
| `trace_id` | Fetch runs that are part of a specific trace. |
| `run_type` | The [type of run](../Data%20type%20reference/Run%20%28span%29%20data%20format.md#run-types) to get, for example, `llm`, `chain`, `tool`, `retriever`. |
| `dataset_name` / `dataset_id` | Fetch runs that are associated with an example row in the specified dataset. This is useful for comparing prompts or models over a given dataset. |
| `reference_example_id` | Fetch runs that are associated with a specific example row. This is useful for comparing prompts or models on a given input. |
| `parent_run_id` | Fetch runs that are children of a given run. This is useful for fetching runs grouped together using the context manager or for fetching an agent trajectory. |
| `error` | Fetch runs that errored or did not error. |
| `run_ids` | Fetch runs with a given list of run ids. Note: **This will ignore all other filtering arguments.** |
| `filter` | Fetch runs that match a given structured filter statement. For more details, refer to the [filter query language](#filter-query-language) section. |
| `trace_filter` | Filter applied to the root run of the trace. Use with `filter` to narrow by attributes of the root run. |
| `tree_filter` | Filter applied to any run in the trace tree (root, sibling, or child). Use with `filter` to narrow by attributes of any run within a trace. |
| `is_root` | Only return root runs. |
| `select` | Select the fields to return in the response. By default, all fields are returned. See [run data format](../Data%20type%20reference/Run%20%28span%29%20data%20format.md) for available fields. |

> [!NOTE]
>
> **Performance tip**: Passing the `select` parameter and excluding `inputs` and `outputs` from the list can significantly improve query performance and reduce response sizes, especially for large runs.

## Filter query language

LangSmith supports filtering capabilities with a filter query language to permit complex filtering operations when fetching runs. This is especially useful when querying traces programmatically via the SDK or API. For example, in [evaluation](../../../Test/Get%20started/LangSmith%20Evaluation.md) pipelines, monitoring scripts, or agentic workflows that inspect prior [traces](../../Trace/Observability%20concepts.md#traces).

### Comparators

The filtering grammar is based on comparator functions applied to fields of the run object:

| Comparator | Description | Example |
| - | - | - |
| `eq` | Equal to | `eq(run_type, "llm")` |
| `neq` | Not equal to | `neq(status, "error")` |
| `gt` | Greater than | `gt(latency, "5s")` |
| `gte` | Greater than or equal to | `gte(latency, 1.5)` |
| `lt` | Less than | `lt(start_time, "2024-01-01T00:00:00Z")` |
| `lte` | Less than or equal to | `lte(feedback_score, 0.5)` |
| `like` | Pattern match; `%` matches any sequence of characters | `like(metadata_value, "%prod%")` |
| `notlike` | Inverse of `like` | `notlike(metadata_value, "%staging%")` |
| `has` | Check if the run contains a tag or metadata key-value | `has(tags, "production")` |
| `search` | Search for a substring across all string fields | `search("invoice")` |
| `in` | Check if a field value is in a list | `in(metadata_key, ["session_id", "thread_id"])` |

### Wildcard pattern matching

`like` and `notlike` match a field value against a pattern. How the pattern applies depends on the field:

* **`name`, `metadata_key`, and `metadata_value`**: `%` matches any sequence of characters, including none. Matching is case-sensitive. Without `%`, `like` matches only the exact value, the same as `eq`.
* **`inputs`, `outputs`, and `error`**: Matching is case-insensitive and always matches a substring, so `%` is optional. LangSmith can match each word of the pattern separately rather than as a phrase, so do not rely on `like` to match an exact phrase in these fields.

For example:

* `like(metadata_value, "%prod%")` matches any value that contains `prod`, such as `production` or `eu-prod-1`.
* `notlike(metadata_value, "%staging%")` matches any value that does not contain `staging`.

In the UI filter builder, the **contains** and **does not contain** operators produce `like` and `notlike` filters. To translate a search bar query, refer to the [UI-to-API operator map](#ui-to-api-operator-map).

### Logical operators

Use `and` and `or` to combine multiple comparators:

```text
and(eq(run_type, "llm"), gt(latency, "2s"))
or(eq(status, "error"), and(eq(feedback_key, "score"), lt(feedback_score, 0.5)))
```

### Filterable fields

| Field | Type | Notes |
| - | - | - |
| `id` | string (UUID) | Run ID |
| `name` | string | Name of the run |
| `run_type` | string | One of `llm`, `chain`, `tool`, `retriever`, `embedding`, `prompt`, `parser` |
| `status` | string | `"success"`, `"error"`, or `"pending"`. Use this to filter errored vs. successful runs. |
| `start_time` | ISO 8601 string | e.g. `"2024-01-15T00:00:00Z"` |
| `end_time` | ISO 8601 string | |
| `latency` | duration string or number | Seconds, e.g. `"5s"`, `"1.5s"`, or `1.5`. Only the `s` suffix is supported. |
| `tags` | list of strings | Use `has(tags, "value")` |
| `metadata_key` | string | Key in the run's metadata dict |
| `metadata_value` | string | Value in the run's metadata dict |
| `feedback_key` | string | Name of a feedback score |
| `feedback_score` | number | Numeric value of a feedback score |

### Value formatting

* **Strings**: wrap in double or single quotes, `eq(name, "MyChain")` or `eq(name, 'MyChain')`.
* **Timestamps**: ISO 8601 format, `"2024-06-01T00:00:00Z"`.
* **Durations**: seconds, as either a number or a string with the `s` suffix, `"5s"`, `"1.5s"`, `"90s"`, or `1.5`. Other unit suffixes (`m`, `h`) are not supported.
* **Lists**: JSON array syntax, `["session_id", "thread_id"]`.

## UI-to-API operator map

The search bar in the LangSmith UI uses its own syntax, documented in [Filter traces](Filter%20traces.md#operators). The following table maps each search bar operator to the comparator that does the same job in this language:

| Search bar operator | Search bar syntax | API comparator |
| - | - | - |
| is | `name:value` | `eq(name, "value")` |
| is not | `-name:value` | `neq(name, "value")` |
| wildcard | `name:*value*` | `like(name, "%value%")`. Replace each `*` with `%`. |
| matches | `input:~value` | `like(inputs, "%value%")`. Also applies to `outputs` and `error`. |
| does not match | `-input:~value` | `notlike(inputs, "%value%")` |
| comparison | `latency:>5` | `gt(latency, 5)`. Use `gte`, `lt`, and `lte` for `>=`, `<`, and `<=`. |
| exists | `metadata.env:*` | `eq(metadata_key, "env")` |

## Alert filters

Alert rules accept the same filter query language in their `filter` and `denominator_filter` fields:

* **`filter`**: Selects the runs that count toward the alert.
* **`denominator_filter`**: Selects the baseline population for a percentage-based alert. When it is empty, every run counts toward the baseline.

Alert filters accept only `and`. Combining conditions with `or` is not supported.

Example alert filter that matches runs whose `env` metadata value does not contain `staging`:

```text
and(eq(metadata_key, "env"), notlike(metadata_value, "%staging%"))
```

## Quick reference examples

The following examples show the filter string only. Pass the string as the `filter`, `trace_filter`, or `tree_filter` argument in `client.runs.query()` or the `POST /api/v2/runs/query` API endpoint.

> [!TIP]
>
> For complete SDK examples with Python, TypeScript, and Java code, refer to [Query traces using the SDK](Query%20traces%20using%20the%20SDK.md#use-filter-query-language).

### Filter by run name

```text
eq(name, "my_chain")
```

### Filter by error status

```text
# Runs that errored
eq(status, "error")

# Runs that did not error
eq(status, "success")
```

### Filter by latency

```text
# Runs slower than 5 seconds
gt(latency, "5s")

# Runs faster than 1 second
lt(latency, "1s")
```

### Filter by time range

```text
and(gt(start_time, "2024-01-01T00:00:00Z"), lt(start_time, "2024-02-01T00:00:00Z"))
```

### Filter by tags

```text
has(tags, "production")

# Multiple tags (any match)
or(has(tags, "production"), has(tags, "staging"))
```

### Filter by metadata key or value

```text
# Runs with a "user_id" metadata key
eq(metadata_key, "user_id")

# Runs with a specific user ID value
and(eq(metadata_key, "user_id"), eq(metadata_value, "usr_abc123"))

# Runs from the production environment
and(eq(metadata_key, "environment"), eq(metadata_value, "production"))

# Runs whose "env" metadata value contains "prod" (like: contains)
and(eq(metadata_key, "env"), like(metadata_value, "%prod%"))

# Runs whose "env" metadata value does not contain "staging" (notlike: does not contain)
and(eq(metadata_key, "env"), notlike(metadata_value, "%staging%"))
```

### Filter by thread ID

```text
and(in(metadata_key, ["session_id", "thread_id"]), eq(metadata_value, "<your_thread_id>"))
```

### Filter by feedback score

```text
# Runs with a "thumbs_up" score of 1
and(eq(feedback_key, "thumbs_up"), eq(feedback_score, 1))

# Runs with a "correctness" score below 0.5
and(eq(feedback_key, "correctness"), lt(feedback_score, 0.5))
```

### Full-text search across all string fields

```text
search("my search term")
```

### Combining conditions

```text
# Errors that started after a specific time
and(gt(start_time, "2024-06-01T00:00:00Z"), eq(status, "error"))

# Slow LLM runs with low correctness feedback
and(gt(latency, "10s"), eq(feedback_key, "correctness"), lt(feedback_score, 0.5))

# Complex: errors OR low score, both starting after a timestamp
and(gt(start_time, "2023-07-15T12:34:56Z"), or(eq(status, "error"), and(eq(feedback_key, "Correctness"), eq(feedback_score, 0.0))))
```

### Using trace\_filter and tree\_filter

`filter` applies to the returned run. `trace_filter` applies to the root run of the trace. `tree_filter` applies to any run anywhere in the trace tree.

```text
# filter: the run you want
eq(name, "RetrieveDocs")

# trace_filter: condition on the root run (e.g. human feedback on the overall trace)
and(eq(feedback_key, "user_score"), eq(feedback_score, 1))

# tree_filter: condition on any run in the trace tree
eq(name, "ExpandQuery")
```

> [!NOTE]
>
> `tree_filter` applies the same query syntax to runs anywhere in the trace tree. For predicates over arbitrary nested child-run fields, such as returned `inputs`, `outputs`, or `extra` payload paths, first narrow candidates with server-side filters, then hydrate root traces with child runs and traverse them locally. See [Query trace trees with child-run predicates](Query%20traces%20using%20the%20SDK.md#query-trace-trees-with-child-run-predicates).
