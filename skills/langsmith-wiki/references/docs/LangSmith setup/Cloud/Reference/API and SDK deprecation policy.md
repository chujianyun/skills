# API and SDK deprecation policy

> How LangSmith deprecates and removes API endpoints and SDK methods in cloud and self-hosted deployments.

LangSmith deprecates API endpoints and SDK methods before removing them, so you have time to migrate to a replacement. This page describes how deprecations are announced and how long they stay supported.

> [!NOTE]
>
> This policy applies only to public endpoints documented in the [LangSmith API reference](../../../Monitor/Reference/LangSmith%20REST%20API/LangSmith%20API%20reference.md) and the [Agent Server API reference](../../../Deploy/Get%20started/Reference/Agent%20Server%20API/Agent%20Server%20API%20reference.md). Internal, undocumented endpoints are not covered and can change, including with breaking changes, at any time.

## Deprecation lifecycle

Every deprecation follows the same stages:

1. **Announced**: the deprecation is published in the [changelog](LangSmith%20Cloud%20changelog.md) with the removal date, once known, and, where call-site changes are needed, in a migration guide that documents the replacement.
2. **Marked**: the deprecated API endpoint returns `Deprecation: true` and `Sunset: <date>` response headers. Deprecated SDK methods are marked in the documentation and, where supported, raise a deprecation warning at call time.
3. **Supported**: the deprecated endpoint continues to function for a minimum window that depends on your deployment. See [Deprecation window by deployment](#deprecation-window-by-deployment).
4. **Removed**: after the support window ends, the endpoint is removed.

In Cloud, if active consumers remain close to the removal date, LangSmith may apply rate limits and increased latency to the deprecated endpoint, and return an explicit error message on a portion of requests, as a last resort to catch the attention of remaining usage before removal. Affected customers are contacted directly beforehand.

## Deprecation window by deployment

| Deployment | Minimum support window |
| - | - |
| Cloud | 6 months from announcement to removal |
| Self-hosted | At least one major release |

Self-hosted major releases ship on a roughly six-week cadence. For details, see [Release policy](../../Self-hosted/Reference/Release%20policy.md).

## SDK method deprecation

Most SDK methods are thin wrappers around an API endpoint, so a method deprecates on the same timeline as the endpoint it calls, and is removed from the SDK when the endpoint is removed.

A method that does not map one-to-one to an endpoint, or is deprecated independently of any endpoint change, can have a different deprecation timeline. It is announced explicitly in both places: in the SDK, through documentation and a deprecation warning, and in the API, through the process described above.

## Field-level deprecation

A deprecated field is removed at a version boundary, not on a date:

* **API fields and parameters**: a deprecated response field, request body field, or query parameter continues to work within the same endpoint version. Removal is a breaking change, so it ships only with the next endpoint version, for example v1 to v2.
* **SDK method fields and parameters**: continue working within the current major SDK version. Removal requires a new major SDK version, independent of the API's own versioning.

## See also

* [Changelog](LangSmith%20Cloud%20changelog.md) for recent LangSmith updates
* [Release stages](Release%20stages.md) for how features move from alpha to GA
* [Release policy](../../Self-hosted/Reference/Release%20policy.md) for self-hosted release channels, cadence, and version support
