# Include HTTP headers in server logs

By default, the [Agent Server](../../Capabilities/Agent%20Server.md) omits HTTP headers from server logs for privacy reasons. However, logging request and correlation IDs can help you debug issues and trace requests across distributed systems. You can opt-in to logging headers for all API calls by modifying the `logging_headers` section in your [`langgraph.json`](../../Develop%20your%20application/Application%20structure.md#configuration-file) file.

```json
{
  "$schema": "https://langgra.ph/schema.json",
  "http": {
    "logging_headers": {
      "includes": ["request-id", "x-purchase-id", "*-trace-*"],
      "excludes": ["authorization", "x-api-key", "x-organization-id", "x-user-id"]
    }
  }
}
```

The `includes` and `excludes` lists accept exact header names or glob patterns using `*` as a wildcard to match any number of characters (case-insensitive). For your security, no other pattern types are supported.

Note that exclusions take precedence over inclusions. For example, if you include `*-id` but exclude `x-user-id`, the `x-user-id` header will not be logged.
