# developers.llamaindex.ai/python/framework/community/faq/llms/index.md
> https://developers.llamaindex.ai/python/framework/community/faq/llms/index.md

--- title: Large Language Models | Developer Documentation ---
##### FAQ
1. How to use a custom/local embedding model? 2. How to use a local hugging face embedding model? 3. How can I customize my prompt 4. Is it required to fine-tune my model? 5. I want to the LLM answer in Chinese/Italian/French but only answers in English, how to proceed? 6. Is LlamaIndex GPU accelerated?

##### 1. How to define a custom LLM?
You can access Usage Custom to define a custom LLM.

##### 2. How to use a different OpenAI model?
To use a different OpenAI model you can access Configure Model to set your own custom model.

##### 3. How can I customize my prompt?
You can access Prompts to learn how to customize your prompts.

##### 4. Is it required to fine-tune my model?
No. there’s isolated modules which might provide better results, but isn’t required, you can use llamaindex without needing to fine-tune the model.

##### 5. I want to the LLM answer in Chinese/Italian/French but only answers in English, how to proceed?
To the LLM answer in another language more accurate you can update the prompts to enforce more the output language.
``` response = query_engine.query("Rest of your query... \nRespond in Italian") ```
Alternatively:
``` from llama_index.core import Settings from llama_index.llms.openai import OpenAI

llm = OpenAI(system_prompt="Always respond in Italian.")

# set a global llm Settings.llm = llm

query_engine = load_index_from_storage( storage_context, ).as_query_engine() ```

##### 6. Is LlamaIndex GPU accelerated?
Yes, you can run a language model (LLM) on a GPU when running it locally. You can find an example of setting up LLMs with GPU support in the llama2 setup documentation.
---