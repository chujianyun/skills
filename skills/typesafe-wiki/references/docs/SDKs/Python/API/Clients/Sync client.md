# Sync client

> Use TypeSafeClient to ask questions, list models, and configure synchronous TypeSafe API requests.

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

<a id="synchronous-client" />

### typesafe\_sdk.TypeSafeClient

```python
TypeSafeClient(
    *,
    api_key: str | None = None,
    model: str | None = None,
    retry: RetryPolicy | None = None,
    timeout: float
    | httpx2.Timeout
    | None = None,
    headers: Mapping[str, str] | None = None,
    transport: httpx2.BaseTransport
    | None = None,
    http_client: httpx2.Client | None = None,
    base_url: str | None = None,
)
```

Create an HTTP client for [TypeSafe AI API](https://typesafe.ai).

Explicit options take precedence over environment variables; empty or whitespace-only environment values are ignored.

**Tip:**

**Logging setup**

  The SDK logs to the `typesafe_sdk` logger; configure it through standard logging, or set `TYPESAFE_LOG_LEVEL` (`debug`, `info`, ...) for a quick default. Secret headers are redacted from log output; request and response bodies are not.

Parameters:

* **`api_key`** (`[str](https://docs.python.org/3/builtins/stdtypes.html#str) | None`, default: `None` ) –

  Required API key; may be set via the `TYPESAFE_API_KEY` environment variable.
* **`model`** (`[str](https://docs.python.org/3/builtins/stdtypes.html#str) | None`, default: `None` ) –

  Model name; may be set via the `TYPESAFE_DEFAULT_MODEL` environment variable.
* **`retry`** (`[RetryPolicy](../Retries.md#typesafe_sdk.RetryPolicy) | None`, default: `None` ) –

  A `RetryPolicy` controlling retry behavior; see `RetryPolicy` for the available options and their defaults. Pass `RetryPolicy(max_retries=0)` to disable retries.
* **`timeout`** (`[float](https://docs.python.org/3/builtins/functions.html#float) | httpx2.Timeout | None`, default: `None` ) –

  Timeout for HTTP operations. Inherits `http_client.timeout` when supplied, otherwise the SDK default.
* **`headers`** (`[Mapping](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping)\[[str](https://docs.python.org/3/builtins/stdtypes.html#str), [str](https://docs.python.org/3/builtins/stdtypes.html#str)] | None`, default: `None` ) –

  Additional request headers to set.
* **`transport`** (`httpx2.BaseTransport | None`, default: `None` ) –

  Optional custom HTTP transport, closed when this SDK client closes.
* **`http_client`** (`httpx2.[Client](https://pydantic.dev/docs/httpx2/api/api/#httpx2.Client) | None`, default: `None` ) –

  Optional `httpx2.Client`; mutually exclusive with `transport`. Closed when this SDK client closes.
* **`base_url`** (`[str](https://docs.python.org/3/builtins/stdtypes.html#str) | None`, default: `None` ) –

  API root; may be set via the `TYPESAFE_BASE_URL` environment variable.

Raises:

* `[TypeSafeError](../Exceptions.md#typesafe_sdk.TypeSafeError)` –

  The API key is missing or the timeout is invalid.
* `[ValueError](https://docs.python.org/3/builtins/exceptions.html#ValueError)` –

  Both `transport` and `http_client` are supplied.

Examples:

```python
from typesafe_sdk import Choice, Noul, TypeSafeClient

with TypeSafeClient() as client:
    result = client.system_one(
        state="I was charged twice. Please help.",
        questions={
            "billing": Noul(instructions="Is this about billing?"),
            "tone": Choice(
                instructions="What is the tone?",
                criteria={"calm": None, "angry": None},
            ),
        },
    )
    assert 0 <= result.nouls["billing"].noul <= 1
    assert result.choices["tone"].choice in {"calm", "angry"}
```

#### models

`cached` `property`

```python
models: Models
```

An accessor for the Models API resource.

Examples:

```python
with TypeSafeClient() as client:
    models = client.models.list()
```

#### system\_one


**Implementation**


```python
system_one(
    state: JSONContent,
    questions: Mapping[str, Question],
    *,
    model: str | None = None,
    retry: RetryPolicy | None = None,
    timeout: float
    | httpx2.Timeout
    | None = None,
    extra_headers: Mapping[str, str]
    | None = None,
    extra_body: Mapping[str, JSONValue | None]
    | None = None,
    response_model: type[ResponseT]
    | None = None,
) -> SystemOneResponse | ResponseT
```




**Overload 1**


```python
system_one(
    state: JSONContent,
    questions: Mapping[str, Question],
    *,
    model: str | None = None,
    retry: RetryPolicy | None = None,
    timeout: float
    | httpx2.Timeout
    | None = None,
    extra_headers: Mapping[str, str]
    | None = None,
    extra_body: Mapping[str, JSONValue | None]
    | None = None,
    response_model: None = None,
) -> SystemOneResponse
```




**Overload 2**


```python
system_one(
    state: JSONContent,
    questions: Mapping[str, Question],
    *,
    model: str | None = None,
    retry: RetryPolicy | None = None,
    timeout: float
    | httpx2.Timeout
    | None = None,
    extra_headers: Mapping[str, str]
    | None = None,
    extra_body: Mapping[str, JSONValue | None]
    | None = None,
    response_model: type[ResponseT],
) -> ResponseT
```



Answer named questions about text or structured state.

See [System One](../../../../Concepts/System One.md) for details.

Parameters:

* **`state`** (`[JSONContent](../Types/Common types.md#typesafe_sdk.JSONContent)`) –

  Text, a JSON object, or an array to evaluate. See [state](../../../../Concepts/State.md) for details.
* **`questions`** (`[Mapping](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping)\[[str](https://docs.python.org/3/builtins/stdtypes.html#str), [Question](../Types/Questions.md#typesafe_sdk.Question)]`) –

  Nonempty mapping of names to question objects or raw dictionaries.
* **`model`** (`[str](https://docs.python.org/3/builtins/stdtypes.html#str) | None`, default: `None` ) –

  Model override; `None` inherits the client default.
* **`retry`** (`[RetryPolicy](../Retries.md#typesafe_sdk.RetryPolicy) | None`, default: `None` ) –

  An optional retry policy to override the client-level value for this call only.
* **`timeout`** (`[float](https://docs.python.org/3/builtins/functions.html#float) | httpx2.Timeout | None`, default: `None` ) –

  An optional timeout for http operations to override the client-level value for this call only, in seconds.
* **`extra_headers`** (`[Mapping](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping)\[[str](https://docs.python.org/3/builtins/stdtypes.html#str), [str](https://docs.python.org/3/builtins/stdtypes.html#str)] | None`, default: `None` ) –

  Additional request headers to set.
* **`extra_body`** (`[Mapping](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping)\[[str](https://docs.python.org/3/builtins/stdtypes.html#str), [JSONValue](../Types/Common types.md#typesafe_sdk.JSONValue) | None] | None`, default: `None` ) –

  Additional top-level request-body fields, shallow-merged over the body after `state`, `model`, and `questions` are set. Merging is last-write-wins: a key that collides with `state`, `model`, or `questions` overrides it, and object values are replaced rather than deep-merged.
* **`response_model`** (`[type](https://docs.python.org/3/builtins/functions.html#type)\[ResponseT] | None`, default: `None` ) –

  Optional Pydantic `BaseModel` type describing the JSON response body, including any nested answer models.

Returns:

* `[SystemOneResponse](../Types/Answers and responses.md#typesafe_sdk.SystemOneResponse) | ResponseT` –

  An instance of `response_model`, or `SystemOneResponse` with answers keyed by question
* `[SystemOneResponse](../Types/Answers and responses.md#typesafe_sdk.SystemOneResponse) | ResponseT` –

  name and model and token usage details when no custom model is supplied.

Raises:

* `[TypeSafeError](../Exceptions.md#typesafe_sdk.TypeSafeError)` –

  Questions are empty or a score question's criteria list is empty.
* `[TypeSafeAPIError](../Exceptions.md#typesafe_sdk.TypeSafeAPIError)` –

  The server returns an unsuccessful HTTP response after any retries.
* `[TypeSafeAPIConnectionError](../Exceptions.md#typesafe_sdk.TypeSafeAPIConnectionError)` –

  The request cannot connect or times out after any retries.
* `[TypeSafeAPIResponseValidationError](../Exceptions.md#typesafe_sdk.TypeSafeAPIResponseValidationError)` –

  The response body does not match the response model.

Examples:

Create questions with named arguments:

```python
with TypeSafeClient() as client:
    result = client.system_one(
        state="I was charged twice. Please help.",
        questions={
            "billing": Noul(instructions="Is this about billing?"),
            "tone": Choice(
                instructions="What is the tone?",
                criteria={"calm": None, "angry": None},
            ),
        },
    )
    assert 0 <= result.nouls["billing"].noul <= 1
    assert result.choices["tone"].choice in {"calm", "angry"}
```

Pass questions as dictionaries:

```python
with TypeSafeClient() as client:
    result = client.system_one(
        state={"message": "I was charged twice. Please help."},
        questions={
            "billing": {"type": "noul", "instructions": "Is this about billing?"},
            "tone": {
                "type": "choice",
                "instructions": "What is the tone?",
                "criteria": {"calm": None, "angry": None},
            },
        },
    )
    assert 0 <= result.nouls["billing"].noul <= 1
    assert result.choices["tone"].choice in {"calm", "angry"}
```

#### close

```python
close() -> None
```

Release network resources and close the underlying HTTP client, including a supplied one.

### Models resource

Reached through [`TypeSafeClient.models`](Sync client.md#typesafe_sdk.TypeSafeClient.models).

#### typesafe\_sdk.Models

Access to the models available to the account, reached through `TypeSafeClient.models`.

##### list

```python
list(
    *,
    retry: RetryPolicy | None = None,
    timeout: float
    | httpx2.Timeout
    | None = None,
    extra_headers: Mapping[str, str]
    | None = None,
) -> ListModelsResponse
```

List the models available to the account.

Parameters:

* **`retry`** (`[RetryPolicy](../Retries.md#typesafe_sdk.RetryPolicy) | None`, default: `None` ) –

  An optional retry policy to override the client-level value for this call only.
* **`timeout`** (`[float](https://docs.python.org/3/builtins/functions.html#float) | httpx2.Timeout | None`, default: `None` ) –

  Per-operation timeout override; `None` inherits the client setting.
* **`extra_headers`** (`[Mapping](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping)\[[str](https://docs.python.org/3/builtins/stdtypes.html#str), [str](https://docs.python.org/3/builtins/stdtypes.html#str)] | None`, default: `None` ) –

  Overrides for additional request headers; authentication, SDK identification, and `Accept` remain protected.

Returns:

* `[ListModelsResponse](../Types/Answers and responses.md#typesafe_sdk.ListModelsResponse)` –

  A `ListModelsResponse` whose `models` holds each model's name, description,
* `[ListModelsResponse](../Types/Answers and responses.md#typesafe_sdk.ListModelsResponse)` –

  and release date.

Raises:

* `[TypeSafeAPIError](../Exceptions.md#typesafe_sdk.TypeSafeAPIError)` –

  The server returns an unsuccessful HTTP response after any retries.
* `[TypeSafeAPIConnectionError](../Exceptions.md#typesafe_sdk.TypeSafeAPIConnectionError)` –

  The request cannot connect or times out after any retries.

Examples:

```python
from typesafe_sdk import TypeSafeClient

with TypeSafeClient() as client:
    models = client.models.list()
```
