# Sandbox download links

> Share a single file from a sandbox as a link that needs no LangSmith credential.

A download link hands one sandbox file to something that cannot carry a LangSmith credential: a browser tab, an `<a href>` in an email, a webhook consumer, or a third-party service that fetches a URL you give it.

The link carries its own token. Reading a file with the SDK's `read()` needs a workspace API key on every request; a download link needs nothing beyond the URL itself.

## Quick start

```python
from langsmith.sandbox import SandboxClient

client = SandboxClient()

with client.sandbox() as sb:
    sb.run("python -c \"open('/app/report.csv','w').write('a,b\\n1,2\\n')\"")

    link = sb.generate_download_url("/app/report.csv")
    print(link.download_url)
```

Anyone can then fetch it with no credential:

```bash
curl -LO "<download_url>"
```

## What a link is pinned to

The token encodes the sandbox, the tenant, the exact file path, and the response headers, so a link cannot be edited to point at a different file or a different sandbox. Each link serves exactly one path.

A link is pinned to that path, not to a snapshot of the file. The file itself is not captured or copied when the link is minted.

> [!WARNING]
>
> Do not modify a file after minting a link for it. A later write to that path may or may not be reflected in what the link serves, so treat the file as immutable for the life of the link. When the contents change, write a new file and mint a new link for it.

Links are served from the sandbox service domain, on the sandbox's own host, never from the LangSmith API host. Downloaded content is therefore isolated from your LangSmith session.

## Create a link

```python Python
# Never expires
link = sb.generate_download_url("/app/report.csv")

# Expires in an hour
link = sb.generate_download_url("/app/report.csv", expires_in_seconds=3600)

# Rendered in the browser instead of downloaded
link = sb.generate_download_url(
    "/app/page.html",
    content_type="text/html",
    content_disposition="inline",
)

print(link.download_url)
print(link.expires_at)  # None when the link never expires
```

```ts TypeScript
// Never expires
let link = await sandbox.generateDownloadURL("/app/report.csv");

// Expires in an hour
link = await sandbox.generateDownloadURL("/app/report.csv", {
  expiresInSeconds: 3600,
});

// Rendered in the browser instead of downloaded
link = await sandbox.generateDownloadURL("/app/page.html", {
  contentType: "text/html",
  contentDisposition: "inline",
});

console.log(link.download_url);
console.log(link.expires_at); // null when the link never expires
```

Call it on the client instead of a sandbox instance to mint a link by sandbox name:

```python Python
link = client.generate_download_url("my-sandbox", "/app/report.csv")
```

```ts TypeScript
const link = await client.generateDownloadURL("my-sandbox", "/app/report.csv");
```

### Options

| Option | Default | Effect |
| - | - | - |
| `expires_in_seconds` | Omitted, so the link never expires | Link lifetime in seconds |
| `content_type` | inferred from the file extension | `Content-Type` the link responds with |
| `content_disposition` | `attachment` | `attachment` downloads the file; `inline` renders it in the browser |

## Create a link from the CLI

```bash
langsmith sandbox generate-download-url my-sandbox --path /app/report.csv
```

```bash
langsmith sandbox generate-download-url my-sandbox \
  --path /app/page.html \
  --expires-in-seconds 3600 \
  --content-disposition inline
```

## Create a link via the REST API

```bash
curl -X POST \
  "$LANGSMITH_ENDPOINT/api/v2/sandboxes/boxes/{sandbox_name}/download-url" \
  -H "x-api-key: $LANGSMITH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"path": "/app/report.csv", "expires_in_seconds": 3600}'
```

Response:

```json
{
  "download_url": "https://{sandbox-id}--dl.smithbox.dev/ey...",
  "token": "ey...",
  "expires_at": "2026-04-08T15:30:00Z"
}
```

`expires_at` is `null` when `expires_in_seconds` was omitted.

Minting a link requires the `sandboxes:exec` permission, the same access a credentialed download needs. See [Sandbox permissions](Sandbox%20access%20permissions.md).

## Fetch a link

`GET` and `HEAD` are supported, along with `Range` (for resumable and partial downloads), `If-Range`, and `If-None-Match`. No headers, query string, or body are needed or accepted.

Fetching a link **wakes a stopped sandbox**, so the first request after an idle stop takes as long as a start. The sandbox does not need to be running when you mint the link.

## Security considerations

> [!WARNING]
>
> A download link is a bearer credential embedded in a URL. Anyone who obtains it can read that one file until it expires. Treat a link like a password: send it over a channel you trust, and prefer a short `expires_in_seconds` for anything sensitive.

* **Links cannot be revoked.** A minted link stays valid until it expires, even if the API key that created it is deleted or loses `sandboxes:exec`. Set an expiry when that matters.
* **Links die with the sandbox.** Deleting the sandbox invalidates every link into it.
* **The file must not change.** A link is pinned to a path, so a write to that path after minting may or may not be reflected in what the link serves.
* **Guest headers are dropped.** The response is rebuilt from an allowlist of content, range, and validator headers. Cookies or other headers set by code inside the sandbox are never forwarded.
* **Rendered content is sandboxed.** Every response carries `X-Content-Type-Options: nosniff` and `Content-Security-Policy: sandbox`, so a file served with `content_disposition=inline` renders with no capabilities and no access to your LangSmith session.

## Download links vs other file access

| | Download links | `read()` | [Service URLs](Sandbox%20service%20URLs.md) |
| - | - | - | - |
| **Credential needed** | None | Workspace API key | Service token or browser cookie |
| **Scope** | One file, one path | Any file | Any HTTP service in the sandbox |
| **Sandbox must be running** | No (fetching wakes it) | No (waking on demand) | No (fetching wakes it) |
| **Shareable** | Yes | No | Yes |
| **Revocable before expiry** | No | Yes (rotate the key) | No |

Use a download link to hand one file to an outside consumer. Use `read()` to pull file bytes into your own code. Use a service URL to reach an HTTP server running inside the sandbox.

## Troubleshoot

| Error | Cause | Fix |
| - | - | - |
| **`501` on mint** | Download links are not configured for this deployment | Self-hosted deployments need a sandbox service domain configured; see [Sandbox service URLs](Sandbox%20service%20URLs.md) |
| **`403` on fetch** | The link expired, was altered, or was presented on the wrong host | Mint a fresh link; copy the URL verbatim |
| **`404` on fetch** | The file no longer exists at that path | Links are pinned to a path, not to file contents. Mint a link for a path that exists |
| **Browser downloads instead of rendering** | Default disposition is `attachment` | Mint with `content_disposition="inline"` and an explicit `content_type` |
| **Stale or partial contents** | The file was written or replaced after the link was minted | Do not modify a file that a link points at. Write a new file and mint a new link |
