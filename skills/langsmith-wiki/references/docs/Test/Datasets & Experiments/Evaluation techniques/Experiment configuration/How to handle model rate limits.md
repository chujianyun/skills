# How to handle model rate limits

A common issue when running large evaluation jobs is running into third-party API rate limits, usually from model providers. There are a few ways to deal with rate limits.

## Using `langchain` RateLimiters (Python only)

If you're using `langchain` Python chat models in your application or evaluators, you can add rate limiters to your model(s) that will add client-side control of the frequency with which requests are sent to the model provider API to avoid rate limit errors.

```python
from langchain.chat_models import init_chat_model
from langchain.rate_limiters import InMemoryRateLimiter

rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.1,  # <-- Super slow! We can only make a request once every 10 seconds!!
    check_every_n_seconds=0.1,  # Wake up every 100 ms to check whether allowed to make a request,
    max_bucket_size=10,  # Controls the maximum burst size.
)

model = init_chat_model("gpt-6.1-sol", rate_limiter=rate_limiter)

def app(inputs: dict) -> dict:
    response = model.invoke(...)
    ...

def evaluator(inputs: dict, outputs: dict, reference_outputs: dict) -> dict:
    response = model.invoke(...)
    ...
```

See the [`langchain`](https://docs.langchain.com/oss/python/langchain/models#rate-limiting) documentation for more on how to configure rate limiters.

## Retrying with exponential backoff

A very common way to deal with rate limit errors is retrying with exponential backoff. Retrying with exponential backoff means repeatedly retrying failed requests with an (exponentially) increasing wait time between each retry. This continues until either the request succeeds or a maximum number of requests is made.

#### With `langchain`

If you're using `langchain` components you can add retries to all model calls with the `.with_retry(...)` / `.withRetry()` method:

```python Python
from langchain.chat_models import init_chat_model

model_with_retry = init_chat_model("gpt-5.4-mini").with_retry(stop_after_attempt=6)
```

```typescript TypeScript
import { initChatModel } from "langchain";

const model = await initChatModel("gpt-6.1-sol", {
    modelProvider: "openai",
});

const modelWithRetry = model.withRetry({ stopAfterAttept: 2 });
```

See the `langchain` [Python](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.BaseChatModel.with_retry) and [JS](https://reference.langchain.com/javascript/langchain-core/language_models/chat_models/BaseChatModel/withRetry) API references for more.

#### Without `langchain`

If you're not using `langchain` you can use other libraries like `tenacity` (Python) or `backoff` (Python) to implement retries with exponential backoff, or you can implement it from scratch. See some examples of how to do this in the [OpenAI docs](https://platform.openai.com/docs/guides/rate-limits#retrying-with-exponential-backoff).

## Limiting `max_concurrency`

Limiting the number of concurrent calls you're making to your application and evaluators is another way to decrease the frequency of model calls you're making, and in that way avoid rate limit errors. `max_concurrency` can be set directly on the [evaluate()](https://reference.langchain.com/python/langsmith/evaluation/_runner/evaluate) / [aevaluate()](https://reference.langchain.com/python/langsmith/evaluation/_arunner/aevaluate) functions. This parallelizes evaluation by effectively splitting the dataset across threads.

```python Python
from langsmith import aevaluate

results = await aevaluate(
    ...
    max_concurrency=4,
)
```

```typescript TypeScript
import { evaluate } from "langsmith/evaluation";

await evaluate(..., {
  ...,
  maxConcurrency: 4,
});
```
