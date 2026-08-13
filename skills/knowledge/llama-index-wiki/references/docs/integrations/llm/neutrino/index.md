# developers.llamaindex.ai/python/framework/integrations/llm/neutrino/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/neutrino/index.md

--- title: Neutrino AI | Developer Documentation ---

Neutrino lets you intelligently route queries to the best-suited LLM for the prompt, maximizing performance while optimizing for costs and latency.
Check us out at: neutrinoapp.com [1] Docs: docs.neutrinoapp.com [2] Create an API key: platform.neutrinoapp.com [3]
``` %pip install llama-index-llms-neutrino ```
``` !pip install llama-index ```
#### Set Neutrino API Key env variable
You can create an API key at: platform.neutrinoapp.com [3]
``` import os
os.environ["NEUTRINO_API_KEY"] = "<your-neutrino-api-key>" ```
#### Using Your Router
A router is a collection of LLMs that you can route queries to. You can create a router in the Neutrino dashboard [3] or use the default router, which includes all supported models. You can treat a router as a LLM.
``` from llama_index.llms.neutrino import Neutrino from llama_index.core.llms import ChatMessage

llm = Neutrino( # api_key="<API_KEY>", # router="<your-router-id>" # (or 'default') )

response = llm.complete("In short, a Neutrino is") print(f"Optimal model: {response.raw['model']}") print(response) ```

``` Optimal model: gpt-3.5-turbo a subatomic particle that is electrically neutral and has a very small mass. It is one of the fundamental particles that make up the universe. Neutrinos are extremely difficult to detect because they interact very weakly with matter, making them able to pass through most materials without any interaction. They are produced in various natural processes, such as nuclear reactions in the Sun and other stars, as well as in particle interactions on Earth. Neutrinos have played a significant role in advancing our understanding of particle physics and the universe.

```
``` message = ChatMessage( role="user", content="Explain the difference between statically typed and dynamically typed languages.", ) resp = llm.chat([message]) print(f"Optimal model: {resp.raw['model']}") print(resp) ```

``` Optimal model: mistralai/Mixtral-8x7B-Instruct-v0.1 assistant: Statically typed languages and dynamically typed languages are categories of programming languages based on how they handle variable types.

In statically typed languages, the type of a variable is determined at compile-time, which means that the type is checked before the program is run. This ensures that variables are always used in a type-safe manner, preventing many types of errors from occurring at runtime. Examples of statically typed languages include Java, C, C++, and C#.
In dynamically typed languages, the type of a variable is determined at runtime, which means that the type is checked as the program is running. This provides more flexibility, as variables can be assigned values of different types at different times, but it also means that type errors may not be caught until the program is running, which can make debugging more difficult. Examples of dynamically typed languages include Python, Ruby, JavaScript, and PHP.

One key difference between statically typed and dynamically typed languages is that statically typed languages tend to be more verbose, requiring explicit type declarations for variables, while dynamically typed languages are more concise and allow for implicit type declarations. However, this also means that statically typed languages can catch type errors earlier in the ```
#### Streaming Responses
``` message = ChatMessage( role="user", content="What is the approximate population of Mexico?" ) resp = llm.stream_chat([message]) for i, r in enumerate(resp): if i == 0: print(f"Optimal model: {r.raw['model']}") print(r.delta, end="") ```

``` Optimal model: anthropic.claude-instant-v1 According to the latest UN estimates, the population of Mexico is approximately 128 million as of 2020. Mexico has the 10th largest population in the world. ```

[1] https://www.neutrinoapp.com/
[2] https://docs.neutrinoapp.com/
[3] https://platform.neutrinoapp.com/