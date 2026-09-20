# Usage

> Guides and patterns for working with the TypeSafe Python SDK.

<a id="usage" />

### Calling the System One API


**Async**

    ```python
    import asyncio

    from typesafe_sdk import AsyncTypeSafeClient, Choice, Noul, Score

    async def main() -> None:
        async with AsyncTypeSafeClient() as client:
            result = await client.system_one(
                "I was charged twice. Please help ASAP.",
                {
                    "billing": Noul(instructions="Is this about billing?"),
                    "tone": Choice(
                        instructions="What is the tone?",
                        criteria={"calm": None, "angry": None},
                    ),
                    "urgency": Score(
                        instructions="How urgent is this?",
                        criteria=["low", "medium", "high"],
                    ),
                },
            )
            print(
                result.nouls["billing"].noul,
                result.choices["tone"].choice,
                result.scores["urgency"].score,
            )

    asyncio.run(main())
    ```



**Sync**

    ```python
    from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

    client = TypeSafeClient()
    state = "I was charged twice. Please help ASAP."
    questions = {
        "billing": Noul(instructions="Is this about billing?"),
        "tone": Choice(
            instructions="What is the tone?", criteria={"calm": None, "angry": None}
        ),
        "urgency": Score(
            instructions="How urgent is this?", criteria=["low", "medium", "high"]
        ),
    }
    result = client.system_one(state, questions)
    print(
        result.nouls["billing"].noul,
        result.choices["tone"].choice,
        result.scores["urgency"].score,
    )
    ```


### Typed system\_one responses

It is possible to provide a response model to `system_one` to make using the response more *type-safe*:

```python
from typesafe_sdk import Noul, NoulAnswer, SystemOneResponse, TypeSafeClient

class BillingResponse(SystemOneResponse):
    billing: NoulAnswer

with TypeSafeClient() as client:
    result = client.system_one(
        "I was charged twice.",
        {"billing": Noul(instructions="Is this about billing?")},
        response_model=BillingResponse,
    )
    assert 0 <= result.billing.noul <= 1
    assert result.billing == result.nouls["billing"]
    print(result.request_id)
```

#### Custom response types

It is also possible to define a completely new response model without inheriting from `SystemOneResponse`:

```python
from pydantic import BaseModel

from typesafe_sdk import Noul, NoulAnswer, TypeSafeClient

class BillingAnswers(BaseModel):
    billing: NoulAnswer

class BillingResponse(BaseModel):
    answers: BillingAnswers

result = TypeSafeClient().system_one(
    "I was charged twice.",
    {"billing": Noul(instructions="Is this about billing?")},
    response_model=BillingResponse,
)
assert 0 <= result.answers.billing.noul <= 1
```

### Choosing a model

Inspect the available models:

```python
from typesafe_sdk import TypeSafeClient

print(TypeSafeClient().models.list())
```

Select the model when constructing a client:

```python
client = TypeSafeClient(model="jev")
```

See the [Models resource reference](API/Clients/Sync client.md#models-resource) for details.

### Retries

Pass a custom [`RetryPolicy`](API/Retries.md) as `retry` on the client or per call.


**Client**

    ```python
    from typesafe_sdk import RetryPolicy, TypeSafeClient

    client = TypeSafeClient(retry=RetryPolicy(max_retries=3, backoff_max=0.2, timeout=1.0))
    ```



**Per-call**

    ```python
    from typesafe_sdk import RetryPolicy

    client.system_one(
        state, questions, retry=RetryPolicy(max_retries=3, backoff_max=0.2, timeout=1.0)
    )
    ```


### Error handling

Handle [exceptions](API/Exceptions.md) raised by the SDK:

```python
from typesafe_sdk import TypeSafeAPIError

try:
    client.system_one(state, questions)
except TypeSafeAPIError as error:
    print(error.status, error.request_id)
```

### Logging

The SDK logs to the `typesafe_sdk` logger. Configure it according to [standard logging](https://docs.python.org/3/library/logging.html) guide:

```python
import logging

logging.getLogger("typesafe_sdk").setLevel(logging.DEBUG)
```

Or set `TYPESAFE_LOG_LEVEL` to one of `debug`, `info`, `warning`, `error`, or `off` before importing the SDK.

`info` logs one summary line per request; `debug` also logs request and response headers and bodies. Secret headers — authorization, API keys, cookies, and any header whose name contains `token` or `secret` — are redacted from log output. Request and response bodies are **not** redacted.

### Environment variables

The SDK reads and uses the following environment variables:

| Variable                 | Configures                                          | Default                   |
| ------------------------ | --------------------------------------------------- | ------------------------- |
| `TYPESAFE_API_KEY`       | API key (required)                                  | —                         |
| `TYPESAFE_BASE_URL`      | API root URL                                        | `https://api.typesafe.ai` |
| `TYPESAFE_DEFAULT_MODEL` | Default model                                       | `jev-latest`              |
| `TYPESAFE_LOG_LEVEL`     | `typesafe_sdk` logger level, applied once at import | unset                     |

See the [constants reference](API/Constants.md) for SDK defaults.

### Forward compatibility

The SDK keeps working as the TypeSafe API evolves, so you can adopt new API features before an SDK release adds first-class support for them.

#### Extra request fields

Send request fields this SDK version predates with [`extra_body`](API/Clients/Sync client.md):

```python
from typesafe_sdk import Noul, TypeSafeClient

with TypeSafeClient() as client:
    client.system_one(
        "I was charged twice.",
        {"billing": Noul(instructions="About billing?")},
        extra_body={"beam_width": 4},
    )
```

#### Raw question dictionaries

```python
from typesafe_sdk import TypeSafeClient

with TypeSafeClient() as client:
    client.system_one(
        "I was charged twice.",
        {"billing": {"type": "noul", "instructions": "About billing?", "weight": 2}},
    )
```

**Tip:**

**Tip**

  Unknown fields are a forward-compatibility escape hatch. Ignore their type-checking errors and prefer upgrading the SDK instead.

#### Unknown answer kinds

The SDK logs a warning and skips unrecognized answer kinds. Use `raw_http_response` to inspect the complete API response, including those answers:

```python
from typesafe_sdk import Noul, TypeSafeClient

result = TypeSafeClient().system_one(
    "I was charged twice.",
    {"billing": Noul(instructions="Is this about billing?")},
)
raw_answers = result.raw_http_response.json()["answers"]
```

#### Unknown response fields

Unknown extra fields on recognized responses are ignored.
