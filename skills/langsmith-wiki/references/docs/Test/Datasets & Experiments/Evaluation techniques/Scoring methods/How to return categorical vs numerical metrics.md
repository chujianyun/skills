# How to return categorical vs numerical metrics

LangSmith supports both categorical and numerical metrics, and you can return either when writing a custom evaluator.

For an evaluator result to be logged as a numerical metric, it must returned as:

* (Python only) an `int`, `float`, or `bool`
* a dict of the form `{"key": "metric_name", "score": int | float | bool}`

For an evaluator result to be logged as a categorical metric, it must be returned as:

* (Python only) a `str`
* a dict of the form `{"key": "metric_name", "value": str | int | float | bool}`

Here are some examples:

* Python: Requires `langsmith>=0.2.0`
* TypeScript: Support for multiple scores is available in `langsmith@0.1.32` and higher

```python Python
def numerical_metric(inputs: dict, outputs: dict, reference_outputs: dict) -> float:
    # Evaluation logic...
    return 0.8
    # Equivalently
    # return {"score": 0.8}
    # Or
    # return {"key": "numerical_metric", "score": 0.8}

def categorical_metric(inputs: dict, outputs: dict, reference_outputs: dict) -> str:
    # Evaluation logic...
    return "english"
    # Equivalently
    # return {"key": "categorical_metric", "score": "english"}
    # Or
    # return {"score": "english"}
```

```typescript TypeScript
import type { Run, Example } from "langsmith/schemas";

function numericalMetric(run: Run, example: Example) {
  // Your evaluation logic here
  return { key: "numerical_metric", score: 0.8};
}

function categoricalMetric(run: Run, example: Example) {
  // Your evaluation logic here
  return { key: "categorical_metric", value: "english"};
}
```

## Related

* [Return multiple metrics in one evaluator](How%20to%20return%20multiple%20scores%20in%20one%20evaluator.md)
