# Troubleshoot trace nesting

When tracing with the LangSmith SDK, LangGraph, and LangChain, tracing should automatically propagate the correct context so that code executed within a parent trace will be rendered in the expected location in the UI.

If you see a child run go to a separate trace (and appear on the top level), it may be caused by one of the following known "edge cases".

## Python

The following outlines common causes for "split" traces when building with python.

### Context propagation using asyncio

When using async calls (especially with streaming) in Python versions \< 3.11, you may encounter issues with trace nesting. This is because Python's `asyncio` only [added full support for passing context](https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task) in version 3.11.

#### Why

LangChain and LangSmith SDK use [contextvars](https://docs.python.org/3/library/contextvars.html) to propagate tracing information implicitly. In Python 3.11 and above, this works seamlessly. However, in earlier versions (3.8, 3.9, 3.10), `asyncio` tasks lack proper `contextvar` support, which can lead to disconnected traces.

#### To resolve

1. **Upgrade Python Version (Recommended)** If possible, upgrade to Python 3.11 or later for automatic context propagation.

2. **Manual Context Propagation** If upgrading isn't an option, you'll need to manually propagate the tracing context. The method varies depending on your setup:

   a) **Using LangGraph or LangChain** Pass the parent `config` to the child call:

   ```python
   import asyncio
   from langchain_core.runnables import RunnableConfig, RunnableLambda

   @RunnableLambda
   async def my_child_runnable(
       inputs: str,
       # The config arg (present in parent_runnable below) is optional
   ):
       yield "A"
       yield "response"

   @RunnableLambda
   async def parent_runnable(inputs: str, config: RunnableConfig):
       async for chunk in my_child_runnable.astream(inputs, config):
           yield chunk

   async def main():
       return [val async for val in parent_runnable.astream("call")]

   asyncio.run(main())
   ```

   b) **Using LangSmith Directly** Pass the run tree directly:

   ```python
   import asyncio
   import langsmith as ls

   @ls.traceable
   async def my_child_function(inputs: str):
       yield "A"
       yield "response"

   @ls.traceable
   async def parent_function(
       inputs: str,
       # The run tree can be auto-populated by the decorator
       run_tree: ls.RunTree,
   ):
       async for chunk in my_child_function(inputs, langsmith_extra={"parent": run_tree}):
           yield chunk

   async def main():
       return [val async for val in parent_function("call")]

   asyncio.run(main())
   ```

   c) **Combining Decorated Code with LangGraph/LangChain** Use a combination of techniques for manual handoff:

   ```python
   import asyncio
   import langsmith as ls
   from langchain_core.runnables import RunnableConfig, RunnableLambda

   @RunnableLambda
   async def my_child_runnable(inputs: str):
       yield "A"
       yield "response"

   @ls.traceable
   async def my_child_function(inputs: str, run_tree: ls.RunTree):
       with ls.tracing_context(parent=run_tree):
           async for chunk in my_child_runnable.astream(inputs):
               yield chunk

   @RunnableLambda
   async def parent_runnable(inputs: str, config: RunnableConfig):
       # @traceable decorated functions can directly accept a RunnableConfig when passed in via "config"
       async for chunk in my_child_function(inputs, langsmith_extra={"config": config}):
           yield chunk

   @ls.traceable
   async def parent_function(inputs: str, run_tree: ls.RunTree):
       # You can set the tracing context manually
       with ls.tracing_context(parent=run_tree):
           async for chunk in parent_runnable.astream(inputs):
               yield chunk

   async def main():
       return [val async for val in parent_function("call")]

   asyncio.run(main())
   ```

### Context propagation using threading

It's common to start tracing and want to apply some parallelism on child tasks all within a single trace. Python's stdlib `ThreadPoolExecutor` by default breaks tracing.

#### Why

Python's contextvars start empty within new threads. Here are two approaches to handle maintain trace contiguity:

#### To resolve

1. **Using LangSmith's ContextThreadPoolExecutor**

   LangSmith provides a `ContextThreadPoolExecutor` that automatically handles context propagation:

   ```python
   from langsmith.utils import ContextThreadPoolExecutor
   from langsmith import traceable

   @traceable
   def outer_func():
       with ContextThreadPoolExecutor() as executor:
           inputs = [1, 2]
           r = list(executor.map(inner_func, inputs))

   @traceable
   def inner_func(x):
       print(x)

   outer_func()
   ```

2. **Manually providing the parent run tree**

   Alternatively, you can manually pass the parent run tree to the inner function:

   ```python
   from langsmith import traceable, get_current_run_tree
   from concurrent.futures import ThreadPoolExecutor

   @traceable
   def outer_func():
       rt = get_current_run_tree()
       with ThreadPoolExecutor() as executor:
           r = list(
               executor.map(
                   lambda x: inner_func(x, langsmith_extra={"parent": rt}), [1, 2]
               )
           )

   @traceable
   def inner_func(x):
       print(x)

   outer_func()
   ```

In this approach, we use `get_current_run_tree()` to obtain the current run tree and pass it to the inner function using the `langsmith_extra` parameter.

Both methods ensure that the inner function calls are correctly aggregated under the initial trace stack, even when executed in separate threads.
