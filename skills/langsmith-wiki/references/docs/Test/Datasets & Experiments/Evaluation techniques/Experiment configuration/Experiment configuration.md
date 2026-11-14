# Experiment configuration

LangSmith supports several configuration options for experiments:

* [Repetitions](#repetitions)
* [Concurrency](#concurrency)
* [Caching](#caching)

### Repetitions

*Repetitions* run an experiment multiple times to account for LLM output variability. Since LLM outputs are non-deterministic, multiple repetitions provide a more accurate performance estimate.

Configure repetitions by passing the `num_repetitions` argument to `evaluate` / `aevaluate` ([Python](https://reference.langchain.com/python/langsmith/evaluation/_runner/evaluate), [TypeScript](https://reference.langchain.com/javascript/langsmith/evaluation/EvaluateOptions#member-numRepetitions-9)). Each repetition re-runs both the target function and all evaluators.

Learn more in the [repetitions how-to guide](How%20to%20evaluate%20with%20repetitions.md).

### Concurrency

*Concurrency* controls how many examples run simultaneously during an experiment. Configure it by passing the `max_concurrency` argument to `evaluate` / `aevaluate`. The semantics differ between the two functions:

#### `evaluate`

The `max_concurrency` argument specifies the maximum number of concurrent threads for running both the target function and evaluators.

#### `aevaluate`

The `max_concurrency` argument uses a semaphore to limit concurrent tasks. `aevaluate` creates a task for each example, where each task runs the target function and all evaluators for that example. The `max_concurrency` argument specifies the maximum number of concurrent examples to process.

### Caching

*Caching* stores API call results to disk to speed up future experiments. Set the `LANGSMITH_TEST_CACHE` environment variable to a valid folder path with write access. Future experiments that make identical API calls will reuse cached results instead of making new requests.
