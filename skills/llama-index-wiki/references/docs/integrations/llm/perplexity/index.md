# developers.llamaindex.ai/python/framework/integrations/llm/perplexity/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/perplexity/index.md

--- title: Perplexity | Developer Documentation ---

Perplexity’s Sonar API offers a solution that combines real-time, grounded web search with advanced reasoning and deep research capabilities.
When to use:
- When your application requires timely, relevant data directly from the web, such as dynamic content updates or current event tracking. - For products that need to support complex user queries with integrated reasoning and deep research, like digital assistants or advanced search engines.
Before we get started, make sure you install `llama_index`
``` %pip install llama-index-llms-perplexity ```
``` !pip install llama-index ```
## Initial Setup
As of April 12th, 2025 - the following models are supported with the Perplexity LLM class in LLaMa Index:
| Model | Context Length | Model Type | | --------------------- | -------------- | --------------- | | `sonar-deep-research` | 128k | Chat Completion | | `sonar-reasoning-pro` | 128k | Chat Completion | | `sonar-reasoning` | 128k | Chat Completion | | `sonar-pro` | 200k | Chat Completion | | `sonar` | 128k | Chat Completion | | `r1-1776` | 128k | Chat Completion |

- `sonar-pro` has a max output token limit of 8k. - The reasoning models output Chain of Thought responses. - `r1-1776` is an offline chat model that does not use the Perplexity search subsystem.
You can find the latest supported models here [1]\ Rate limits are found here [2]\ Pricing can be found here [3].
``` import getpass import os

if "PPLX_API_KEY" not in os.environ: os.environ["PPLX_API_KEY"] = getpass.getpass( "Enter your Perplexity API key: " ) ```

``` from llama_index.llms.perplexity import Perplexity
PPLX_API_KEY = __import__("os").environ.get("PPLX_API_KEY")
llm = Perplexity(api_key=PPLX_API_KEY, model="sonar-pro", temperature=0.2) ```
``` # Import the ChatMessage class from the llama_index library. from llama_index.core.llms import ChatMessage

# Create a list of dictionaries where each dictionary represents a chat message. # Each dictionary contains a 'role' key (e.g., system or user) and a 'content' key with the corresponding message. messages_dict = [ {"role": "system", "content": "Be precise and concise."}, { "role": "user", "content": "Tell me the latest news about the US Stock Market.", }, ]

# Convert each dictionary in the list to a ChatMessage object using unpacking (**msg) in a list comprehension. messages = [ChatMessage(**msg) for msg in messages_dict]
# Print the list of ChatMessage objects to verify the conversion. print(messages) ```
``` [ChatMessage(role=<MessageRole.SYSTEM: 'system'>, additional_kwargs={}, blocks=[TextBlock(block_type='text', text='Be precise and concise.')]), ChatMessage(role=<MessageRole.USER: 'user'>, additional_kwargs={}, blocks= [TextBlock(block_type='text', text='Tell me the latest news about the US Stock Market.')])] ```

## Chat
``` response = llm.chat(messages) print(response) ```

``` assistant: The latest update on the U.S. stock market indicates a strong performance recently. A significant 10% rally occurred on Wednesday, which contributed substantially to market gains. Additionally, the market closed strongly on Friday, with a 2% increase, ending near the intraday high. This reflects robust momentum, particularly in mega and large-cap growth stocks[1]. ```

## Async Chat
For asynchronous conversation processing, use the `achat` method to send messages and await the response:
``` # Asynchronously send the list of chat messages to the LLM using the 'achat' method. # This method returns a ChatResponse object containing the model's answer. response = await llm.achat(messages)

print(response) ```
``` assistant: The U.S. stock market has recently experienced significant gains. A major rally on Wednesday resulted in a 10% surge, contributing substantially to the market's overall upside. Additionally, the market closed strongly on Friday, with a 2% increase, ending near the intraday high. This performance highlights robust momentum, particularly in mega-cap and large-cap growth stocks[1]. ```

## Stream Chat
For cases where you want to receive a response token by token in real time, use the `stream_chat` method:
``` # Call the stream_chat method on the LLM instance, which returns a generator or iterable # for streaming the chat response one delta (token or chunk) at a time. response = llm.stream_chat(messages)

# Iterate over each streaming response chunk. for r in response: # Print the delta (the new chunk of generated text) without adding a newline. print(r.delta, end="") ```

``` The latest news about the U.S. stock market indicates a strong performance recently. The New York Stock Exchange (NYSE) experienced a significant rally, with a 10% surge on Wednesday, followed by a 2% gain on Friday. This upward momentum brought the market near its intraday high, driven by strength in mega-cap and large-cap growth stocks[1]. ```

## Async Stream Chat
Similarly, for asynchronous streaming, the `astream_chat` method provides a way to process response deltas asynchronously:
``` # Asynchronously call the astream_chat method on the LLM instance, # which returns an asynchronous generator that yields response chunks. resp = await llm.astream_chat(messages)

# Asynchronously iterate over each response chunk from the generator. # For each chunk (delta), print the chunk's text content. async for delta in resp: print(delta.delta, end="") ```

``` The latest updates on the U.S. stock market indicate significant positive momentum. The New York Stock Exchange (NYSE) experienced a strong rally, with a notable 10% surge on Wednesday. This was followed by a 2% gain on Friday, closing near the intraday high. The market's performance has been driven by mega and large-cap growth stocks, contributing to the overall upside[1]. ```

### Tool calling
Perplexity models can easily be wrapped into a llamaindex tool so that it can be called as part of your data processing or conversational workflows. This tool uses real-time generative search powered by Perplexity, and it’s configured with the updated default model (“sonar-pro”) and the enable\_search\_classifier parameter enabled.
Below is an example of how to define and register the tool:
``` from llama_index.core.tools import FunctionTool from llama_index.llms.perplexity import Perplexity from llama_index.core.llms import ChatMessage

def query_perplexity(query: str) -> str: """ Queries the Perplexity API via the LlamaIndex integration.

This function instantiates a Perplexity LLM with updated default settings (using model "sonar-pro" and enabling search classifier so that the API can intelligently decide if a search is needed), wraps the query into a ChatMessage, and returns the generated response content. """ pplx_api_key = ( "your-perplexity-api-key" # Replace with your actual API key )

llm = Perplexity( api_key=pplx_api_key, model="sonar-pro", temperature=0.7, enable_search_classifier=True, # This will determine if the search component is necessary in this particular context )

messages = [ChatMessage(role="user", content=query)] response = llm.chat(messages) return response.message.content

# Create the tool from the query_perplexity function query_perplexity_tool = FunctionTool.from_defaults(fn=query_perplexity) ```

[1] https://docs.perplexity.ai/docs/model-cards
[2] https://docs.perplexity.ai/docs/rate-limits
[3] https://docs.perplexity.ai/guides/pricing