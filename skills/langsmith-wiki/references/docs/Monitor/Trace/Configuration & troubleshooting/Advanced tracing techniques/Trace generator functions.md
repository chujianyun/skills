# Trace generator functions

In most LLM applications, you will want to stream outputs to minimize the time to the first token seen by the user.

LangSmith's tracing functionality natively supports streamed outputs via `generator` functions. Below is an example.

```python Python
from langsmith import traceable
@traceable
def my_generator():
  for chunk in ["Hello", "World", "!"]:
      yield chunk
# Stream to the user
for output in my_generator():
  print(output)
# It also works with async functions
import asyncio
@traceable
async def my_async_generator():
  for chunk in ["Hello", "World", "!"]:
      yield chunk
# Stream to the user
async def main():
  async for output in my_async_generator():
      print(output)
asyncio.run(main())
```

```typescript TypeScript
import { traceable } from "langsmith/traceable";
const myGenerator = traceable(function* () {
  for (const chunk of ["Hello", "World", "!"]) {
      yield chunk;
  }
});
for (const output of myGenerator()) {
  console.log(output);
}
```

## Aggregate results[ ](#aggregate-results "Direct link to aggregate results")

By default, the `outputs` of the traced function are aggregated into a single array in LangSmith. If you want to customize how it is stored (for instance, concatenating the outputs into a single string), you can use the `aggregate` option (`reduce_fn` in python). This is especially useful for aggregating streamed LLM outputs.

> [!NOTE]
>
> Aggregating outputs **only** impacts the traced representation of the outputs. It doesn not alter the values returned by your function.

```python Python
from langsmith import traceable
def concatenate_strings(outputs: list):
  return "".join(outputs)
@traceable(reduce_fn=concatenate_strings)
def my_generator():
  for chunk in ["Hello", "World", "!"]:
      yield chunk
# Stream to the user
for output in my_generator():
  print(output)
# It also works with async functions
import asyncio
@traceable(reduce_fn=concatenate_strings)
async def my_async_generator():
  for chunk in ["Hello", "World", "!"]:
      yield chunk
# Stream to the user
async def main():
  async for output in my_async_generator():
      print(output)
asyncio.run(main())
```

```typescript TypeScript
import { traceable } from "langsmith/traceable";
const concatenateStrings = (outputs: string[]) => outputs.join("");
const myGenerator = traceable(function* () {
  for (const chunk of ["Hello", "World", "!"]) {
      yield chunk;
  }
}, { aggregator: concatenateStrings });
for (const output of await myGenerator()) {
  console.log(output);
}
```
