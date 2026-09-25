# Exceptions

> Handle TypeSafe API errors, rate limits, connection failures, and timeouts.

export function SdkSignature({children}) {
  async function copy(event) {
    const button = event.currentTarget;
    const code = button.parentElement.querySelector("pre code");
    try {
      await navigator.clipboard.writeText(code.textContent);
      button.setAttribute("aria-label", "Signature copied");
      button.dataset.copied = "true";
    } catch {
      button.setAttribute("aria-label", "Copy failed; select the signature to copy");
    }
    setTimeout(() => {
      button.setAttribute("aria-label", "Copy signature");
      delete button.dataset.copied;
    }, 2000);
  }
  return

        <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <rect x="8" y="8" width="12" height="12" rx="2" />
          <path d="M16 8V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h3" />
        </svg>

      `{children}`
    ;
}

<a id="exceptions" />

### Base exception

### typesafe\_sdk.TypeSafeError

Bases: `[Exception](https://docs.python.org/3/builtins/exceptions.html#Exception)`

Base exception for SDK failures.

### HTTP errors

### typesafe\_sdk.TypeSafeAPIError

Bases: `[TypeSafeError](Exceptions.md#typesafe_sdk.TypeSafeError)`

An unsuccessful HTTP response with its body and request metadata.

#### status

`instance-attribute`

```python
status = status
```

HTTP response status code.

#### body

`instance-attribute`

```python
body = body
```

The server's JSON error body, plain response text, or `None` for an empty body.

#### headers

`instance-attribute`

```python
headers = headers
```

HTTP response headers.

#### endpoint

`instance-attribute`

```python
endpoint = endpoint
```

The request method and URL, without credentials, query parameters, or fragment, when available.

#### request\_id

`property`

```python
request_id: str | None
```

The `x-typesafe-request-id` response header, or `None` if absent.

### typesafe\_sdk.TypeSafeBadRequestError

Bases: `[TypeSafeAPIError](Exceptions.md#typesafe_sdk.TypeSafeAPIError)`

The request was invalid (400).

### typesafe\_sdk.TypeSafeAuthenticationError

Bases: `[TypeSafeAPIError](Exceptions.md#typesafe_sdk.TypeSafeAPIError)`

Authentication failed (401).

### typesafe\_sdk.TypeSafePermissionDeniedError

Bases: `[TypeSafeAPIError](Exceptions.md#typesafe_sdk.TypeSafeAPIError)`

Access was denied (403).

### typesafe\_sdk.TypeSafeNotFoundError

Bases: `[TypeSafeAPIError](Exceptions.md#typesafe_sdk.TypeSafeAPIError)`

The resource was not found (404).

### typesafe\_sdk.TypeSafeUnprocessableEntityError

Bases: `[TypeSafeAPIError](Exceptions.md#typesafe_sdk.TypeSafeAPIError)`

The request failed server validation (422).

### typesafe\_sdk.TypeSafeRateLimitError

Bases: `[TypeSafeAPIError](Exceptions.md#typesafe_sdk.TypeSafeAPIError)`

The rate limit was exceeded (429).

#### retry\_after\_ms

`instance-attribute`

```python
retry_after_ms = parse_retry_after(headers)
```

The server's requested wait in milliseconds, or `None` if unavailable.

### typesafe\_sdk.TypeSafeInternalServerError

Bases: `[TypeSafeAPIError](Exceptions.md#typesafe_sdk.TypeSafeAPIError)`

The server failed to process the request (5xx).

### Connection errors

### typesafe\_sdk.TypeSafeAPIConnectionError

Bases: `[TypeSafeError](Exceptions.md#typesafe_sdk.TypeSafeError)`, `[ConnectionError](https://docs.python.org/3/builtins/exceptions.html#ConnectionError)`

A request failed without an HTTP response.

### typesafe\_sdk.TypeSafeAPITimeoutError

Bases: `[TypeSafeAPIConnectionError](Exceptions.md#typesafe_sdk.TypeSafeAPIConnectionError)`, `[TimeoutError](https://docs.python.org/3/builtins/exceptions.html#TimeoutError)`

A request exceeded its configured timeout.

#### timeout

`instance-attribute`

```python
timeout = timeout
```

The timeout setting used for the request, in seconds or as an `httpx2.Timeout`.

### Response validation

### typesafe\_sdk.TypeSafeAPIResponseValidationError

Bases: `[TypeSafeAPIError](Exceptions.md#typesafe_sdk.TypeSafeAPIError)`

A successful HTTP response whose body was missing or structurally invalid required data.

#### field\_path

`instance-attribute`

```python
field_path = field_path
```

Dotted path to the offending field, such as `answers.tone.confidence`.

#### args

`instance-attribute`

```python
args = (
    status,
    body,
    headers,
    field_path,
    endpoint,
)
```
