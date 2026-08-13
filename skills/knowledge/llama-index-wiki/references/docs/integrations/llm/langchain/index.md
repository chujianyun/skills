# developers.llamaindex.ai/python/framework/integrations/llm/langchain/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/langchain/index.md

--- title: LangChain LLM | Developer Documentation ---
``` %pip install llama-index-llms-langchain ```
``` from langchain.llms import OpenAI ```
``` from llama_index.llms.langchain import LangChainLLM ```
``` llm = LangChainLLM(llm=OpenAI()) ```
``` response_gen = llm.stream_complete("Hi this is") ```
``` for delta in response_gen: print(delta.delta, end="") ```
``` a test
Hello! Welcome to the test. What would you like to learn about? ```