# Use server-side caching

> Cache values server-side in your agent deployment using stale-while-revalidate and key-value cache APIs.

Agents deployed on [Agent Server](../Capabilities/Agent%20Server.md) often call external services, such as config stores, auth providers, and feature-flag systems. The data these services return rarely needs to be re-fetched on every invocation. The built-in cache lets you store those results server-side so subsequent runs read from memory instead of making redundant network calls.

The cache exposes two layers:

* **`swr`**: stale-while-revalidate. Pass a key and an async loader; the server caches the result, serves it on future reads, and revalidates in the background when the entry goes stale. Use this for most caching needs.
* **`cache_get` / `cache_set`**: low-level key-value API for when you need manual control over reads and writes.

All cache APIs are server-side only and require the Agent Server runtime. Values must be JSON-serializable.

> [!NOTE]
>
> `swr` requires Agent Server runtime **v0.7.79** or later and is currently in **[beta](../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)**.
> `cache_get` and `cache_set` require **v0.7.29** or later.

## Quick start

Pass a key and an async loader function. `swr` returns the cached value if available, or calls your loader to fetch it:

```python
from langgraph_sdk.cache import swr

async def fetch_config() -> dict:
    """Call your config service, database, or external API."""
    ...

result = await swr("config:global", fetch_config)
config = result.value
```

On the first call, `swr` awaits `fetch_config()` and caches the result. On subsequent calls, it returns the cached value instantly and revalidates in the background.

## Control freshness and expiry

Control how long cached values are considered fresh and when they expire:

```python
from datetime import timedelta
from langgraph_sdk.cache import swr

result = await swr(
    "config:global",
    fetch_config,  # async loader defined above
    fresh_for=timedelta(minutes=5),
    max_age=timedelta(hours=1),
)
```

| Parameter | Default | Description |
| - | - | - |
| `fresh_for` | `timedelta(0)` | Duration to treat a cached value as fresh. During this window, `swr` returns the cached value with no revalidation. |
| `max_age` | `timedelta(days=1)` | Maximum lifetime of a cached entry. After this, `swr` blocks on the loader before returning. Capped at 1 day. |

### How revalidation works

| Cache state | Condition | Behavior |
| - | - | - |
| **Miss** | Key not in cache | Awaits `loader()`, stores result, returns it. |
| **Fresh** | `age < fresh_for` | Returns cached value, no revalidation. |
| **Stale** | `fresh_for <= age < max_age` | Returns cached value immediately, triggers background refresh. |
| **Expired** | `age >= max_age` | Awaits `loader()`, stores result, returns it. |

## Inspect and update cached values

`swr` returns an `SWRResult` object with the value and cache status:

```python
result = await swr("config:global", fetch_config)

result.value   # the cached or freshly loaded value
result.status  # "miss" | "fresh" | "stale" | "expired"

# Update the cached value directly
await result.mutate({"model": "gpt-5.4-mini", "temperature": 0.5})

# Or force revalidation by calling the loader again
await result.mutate()
```

`.status` tells you whether the value came from cache or was freshly loaded. Call `.mutate(new_value)` to replace the cached entry, or `.mutate()` with no arguments to force the loader to run again.

## Cache auth credentials

Cache credential validation in a [custom auth handler](../Auth%20%26%20access%20control/Add%20custom%20authentication.md) to avoid hitting your identity provider on every request:

```python
from datetime import timedelta

import httpx
from langgraph_sdk import Auth
from langgraph_sdk.cache import swr

auth = Auth()
http_client = httpx.AsyncClient()

async def validate_token(token: str) -> dict:
    """Validate a bearer token against your identity provider."""
    resp = await http_client.get(
        "https://idp.example.com/userinfo",
        headers={"Authorization": f"Bearer {token}"},
    )
    resp.raise_for_status()
    return resp.json()

@auth.authenticate
async def authenticate(headers: dict) -> Auth.types.MinimalUserDict:
    token = (headers.get(b"authorization") or b"").decode()
    if not token:
        raise Auth.exceptions.HTTPException(status_code=401, detail="Missing token")

    result = await swr(
        f"auth:token:{token}",
        lambda: validate_token(token),
        fresh_for=timedelta(minutes=5),
        max_age=timedelta(hours=1),
    )
    return result.value
```

With this setup, the server returns the cached user for 5 minutes without contacting the identity provider. After that, it revalidates in the background for up to 1 hour. After 1 hour, the next request blocks until `validate_token` completes.

## Use with Pydantic models

Pass a `model` parameter to automatically serialize and deserialize Pydantic models:

```python
from pydantic import BaseModel
from langgraph_sdk.cache import swr

class UserProfile(BaseModel):
    name: str
    email: str
    role: str

async def fetch_profile(user_id: str) -> dict:
    """Fetch a user profile from your user service."""
    ...

user_id = "user-123"
result = await swr(
    f"profile:{user_id}",
    lambda: fetch_profile(user_id),
    model=UserProfile,
)
profile: UserProfile = result.value  # deserialized as UserProfile
```

`swr` calls `model_dump(mode="json")` before storing and `model.model_validate()` when reading back.

## Low-level cache API

For simple get/set caching without revalidation, use `cache_get` and `cache_set` directly:

```python
from datetime import timedelta
from langgraph_sdk.cache import cache_get, cache_set

async def compute_embeddings(text: str) -> list[float]:
    """Call an embeddings API or run an expensive computation."""
    ...

key = "embeddings:doc-42"
value = await cache_get(key)

if value is None:
    value = await compute_embeddings("hello world")
    await cache_set(key, value, ttl=timedelta(hours=1))
```

### `cache_get`

```python
async def cache_get(key: str) -> Any | None
```

Return the deserialized value, or `None` if the key does not exist or has expired.

### `cache_set`

```python
async def cache_set(key: str, value: Any, *, ttl: timedelta | None = None) -> None
```

| Parameter | Type | Default | Description |
| - | - | - | - |
| `key` | `str` | required | The cache key |
| `value` | `Any` | required | Value to cache. Must be JSON-serializable |
| `ttl` | `timedelta \| None` | `None` | Time-to-live. The server caps this at 1 day. `None` or zero defaults to 1 day |

## Next steps

* [Add custom authentication](../Auth%20%26%20access%20control/Add%20custom%20authentication.md) to your deployment.
* [Add custom lifespan events](Extend%20the%20HTTP%20server/How%20to%20add%20custom%20lifespan%20events.md) to initialize resources at server startup.
* Learn about the [Agent Server architecture](../Capabilities/Agent%20Server.md).
