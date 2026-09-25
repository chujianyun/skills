# Retries

> Configure retries with RetryPolicy — attempt count, retryable statuses, backoff, and retry headers handling.

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

<a id="retries" />

### typesafe\_sdk.RetryPolicy

`dataclass`

```python
RetryPolicy(
    max_retries: int = 2,
    backoff_initial: float = 0.5,
    backoff_max: float = 5.0,
    backoff_jitter: float = 0.25,
    http_statuses: set[int] = (
        lambda: {408, 429, *range(500, 600)}
    )(),
    respect_retry_after: bool = True,
    api_connection_error: bool = True,
    api_timeout_error: bool = True,
    exceptions: set[
        type[BaseException]
    ] = set(),
    predicate: Callable[[BaseException], bool]
    | None = None,
    timeout: float | None = 30.0,
)
```

Configuration for SDK retry behavior.

Examples:

```python
from typesafe_sdk import RetryPolicy, TypeSafeClient

client = TypeSafeClient(
    retry=RetryPolicy(
        max_retries=3, timeout=10.0, http_statuses={429, 500, 502, 503, 504}
    )
)
```

#### max\_retries

`class-attribute` `instance-attribute`

```python
max_retries: int = 2
```

Maximum retries after the initial attempt; `0` disables retries.

#### backoff\_initial

`class-attribute` `instance-attribute`

```python
backoff_initial: float = 0.5
```

First backoff delay in seconds, doubled each attempt up to `backoff_max`; zero disables backoff.

#### backoff\_max

`class-attribute` `instance-attribute`

```python
backoff_max: float = 5.0
```

Maximum backoff delay in seconds; zero disables backoff.

#### backoff\_jitter

`class-attribute` `instance-attribute`

```python
backoff_jitter: float = 0.25
```

Fraction of each backoff delay randomly subtracted, between 0 and 1.

#### http\_statuses

`class-attribute` `instance-attribute`

```python
http_statuses: set[int] = field(
    default_factory=lambda: {
        408,
        429,
        *range(500, 600),
    }
)
```

HTTP status codes that are retried.

#### respect\_retry\_after

`class-attribute` `instance-attribute`

```python
respect_retry_after: bool = True
```

Whether to honor `Retry-After` and `retry-after-ms` response headers.

#### api\_connection\_error

`class-attribute` `instance-attribute`

```python
api_connection_error: bool = True
```

Whether to retry `TypeSafeAPIConnectionError`, raised when the request cannot reach or read from the server.

#### api\_timeout\_error

`class-attribute` `instance-attribute`

```python
api_timeout_error: bool = True
```

Whether to retry `TypeSafeAPITimeoutError`, raised when the request exceeds its timeout.

#### exceptions

`class-attribute` `instance-attribute`

```python
exceptions: set[type[BaseException]] = field(
    default_factory=set
)
```

Additional exception types that trigger a retry, on top of the built-in rules.

#### predicate

`class-attribute` `instance-attribute`

```python
predicate: (
    Callable[[BaseException], bool] | None
) = None
```

An optional predicate called with the raised exception; returning `True` triggers a retry in addition to the other rules.

#### timeout

`class-attribute` `instance-attribute`

```python
timeout: float | None = 30.0
```

Total retry budget in seconds per SDK call, including the initial attempt and delays; `None` disables the limit.

Stops before a retry whose delay would reach or exceed the budget, re-raising the last error.
