# developers.llamaindex.ai/python/framework/getting_started/starter_example_local/index.md
> https://developers.llamaindex.ai/python/framework/getting_started/starter_example_local/index.md

--- title: Starter Tutorial (Using Local LLMs) | Developer Documentation ---

This tutorial will show you how to get started building agents with LlamaIndex. We’ll start with a basic example and then show how to add RAG (Retrieval-Augmented Generation) capabilities.

We will use `BAAI/bge-base-en-v1.5` [1] as our embedding model and `llama3.1 8B` served through `Ollama`.

Make sure you’ve followed the installation steps first.
## Setup
Ollama is a tool to help you get set up with LLMs locally with minimal setup.
Follow the README [2] to learn how to install it.
To download the Llama3 model just do `ollama pull llama3.1`.
**NOTE**: You will need a machine with at least \~32GB of RAM.

As explained in our installation guide, `llama-index` is actually a collection of packages. To run Ollama and Huggingface, we will need to install those integrations:

``` pip install llama-index-llms-ollama llama-index-embeddings-huggingface ```
The package names spell out the imports, which is very helpful for remembering how to import them or install them!
``` from llama_index.llms.ollama import Ollama from llama_index.embeddings.huggingface import HuggingFaceEmbedding ```

More integrations are all listed on <https://llamahub.ai>.
## Basic Agent Example
Let’s start with a simple example using an agent that can perform basic multiplication by calling a tool. Create a file called `starter.py`:
``` import asyncio from llama_index.core.agent.workflow import FunctionAgent from llama_index.llms.ollama import Ollama

# Define a simple calculator tool def multiply(a: float, b: float) -> float: """Useful for multiplying two numbers.""" return a * b

# Create an agent workflow with our calculator tool agent = FunctionAgent( tools=[multiply], llm=Ollama( model="llama3.1", request_timeout=360.0, # Manually set the context window to limit memory usage context_window=8000, ), system_prompt="You are a helpful assistant that can multiply two numbers.", )

async def main(): # Run the agent response = await agent.run("What is 1234 * 4567?") print(str(response))

This will output something like: `The answer to 1234 * 4567 is 5635678.`
What happened is:
- The agent was given a question: `What is 1234 * 4567?` - Under the hood, this question, plus the schema of the tools (name, docstring, and arguments) were passed to the LLM - The agent selected the `multiply` tool and wrote the arguments to the tool - The agent received the result from the tool and interpolated it into the final response

As you can see, we are using `async` python functions. Many LLMs and models support async calls, and using async code is recommended to improve performance of your application. To learn more about async code and python, we recommend this short section on async + python.

## Adding Chat History
The `AgentWorkflow` is also able to remember previous messages. This is contained inside the `Context` of the `AgentWorkflow`.
If the `Context` is passed in, the agent will use it to continue the conversation.
``` from llama_index.core.workflow import Context

# create context ctx = Context(agent)

# run agent with context response = await agent.run("My name is Logan", ctx=ctx) response = await agent.run("What is my name?", ctx=ctx) ```

## Adding RAG Capabilities
Now let’s enhance our agent by adding the ability to search through documents. First, let’s get some example data using our terminal:
Terminal window
``` mkdir data wget https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt -O data/paul_graham_essay.txt ```

Your directory structure should look like this now:
``` ├── starter.py └── data └── paul_graham_essay.txt ```

Now we can create a tool for searching through documents using LlamaIndex. By default, our `VectorStoreIndex` will use a `text-embedding-ada-002` embeddings from OpenAI to embed and retrieve the text.

Our modified `starter.py` should look like this:
``` from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings from llama_index.core.agent.workflow import AgentWorkflow from llama_index.llms.ollama import Ollama from llama_index.embeddings.huggingface import HuggingFaceEmbedding import asyncio import os

# Settings control global defaults Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5") Settings.llm = Ollama( model="llama3.1", request_timeout=360.0, # Manually set the context window to limit memory usage context_window=8000, )

# Create a RAG tool using LlamaIndex documents = SimpleDirectoryReader("data").load_data() index = VectorStoreIndex.from_documents( documents, # we can optionally override the embed_model here # embed_model=Settings.embed_model, ) query_engine = index.as_query_engine( # we can optionally override the llm here # llm=Settings.llm, )

def multiply(a: float, b: float) -> float: """Useful for multiplying two numbers.""" return a * b

async def search_documents(query: str) -> str: """Useful for answering natural language questions about an personal essay written by Paul Graham.""" response = await query_engine.aquery(query) return str(response)

# Create an enhanced workflow with both tools agent = AgentWorkflow.from_tools_or_functions( [multiply, search_documents], llm=Settings.llm, system_prompt="""You are a helpful assistant that can perform calculations and search through documents to answer questions.""", )

# Now we can ask questions about the documents or do calculations async def main(): response = await agent.run( "What did the author do in college? Also, what's 7 * 8?" ) print(response)

# Run the agent if __name__ == "__main__": asyncio.run(main()) ```

The agent can now seamlessly switch between using the calculator and searching through documents to answer questions.
## Storing the RAG Index
To avoid reprocessing documents every time, you can persist the index to disk:
``` # Save the index index.storage_context.persist("storage")

# Later, load the index from llama_index.core import StorageContext, load_index_from_storage

storage_context = StorageContext.from_defaults(persist_dir="storage") index = load_index_from_storage( storage_context, # we can optionally override the embed_model here # it's important to use the same embed_model as the one used to build the index # embed_model=Settings.embed_model, ) query_engine = index.as_query_engine( # we can optionally override the llm here # llm=Settings.llm, ) ```
Tip

If you used a vector store integration besides the default, chances are you can just reload from the vector store:

``` index = VectorStoreIndex.from_vector_store( vector_store, # it's important to use the same embed_model as the one used to build the index # embed_model=Settings.embed_model, ) ```

## What’s Next?
This is just the beginning of what you can do with LlamaIndex agents! You can:
- Add more tools to your agent - Use different LLMs - Customize the agent’s behavior using system prompts - Add streaming capabilities - Implement human-in-the-loop workflows - Use multiple agents to collaborate on tasks

Some helpful next links:
- See more advanced agent examples in our Agent documentation - Learn more about high-level concepts - Explore how to customize things - Check out the component guides

[1] https://huggingface.co/BAAI/bge-base-en-v1.5
[2] https://github.com/jmorganca/ollama