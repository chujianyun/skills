# developers.llamaindex.ai/python/framework/integrations/llm/together/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/together/index.md

--- title: Together AI LLM | Developer Documentation ---

This notebook shows how to use `Together AI` as an LLM. Together AI provides access to many state-of-the-art LLM models. Check out the full list of models here [1].
Visit <https://together.ai> and sign up to get an API key.
## Setup
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-llms-together ```
``` !pip install llama-index ```
``` from llama_index.llms.together import TogetherLLM ```
``` # set api key in env or in llm # import os # os.environ["TOGETHER_API_KEY"] = "your api key"

llm = TogetherLLM( model="mistralai/Mixtral-8x7B-Instruct-v0.1", api_key="<API_KEY>" ) ```

``` resp = llm.complete("Who is Paul Graham?") ```

``` Paul Graham is a British-born computer scientist, venture capitalist, and essayist. He is best known for co-founding the startup incubator and investment firm, Y Combinator, which has provided funding and support to numerous successful tech startups including Dropbox, Airbnb, and Reddit.

In addition to his work in the tech industry, Graham has a background in artificial intelligence and computer science, having earned a Ph.D. in computer science from Harvard University. He is also a prolific essayist and has written several books, including "Hackers & Painters" and "The Hundred-Year Lie: How to Prevent Corporate Abuse and Save the World from Its Own Worst Appetites." ```
#### Call `chat` with a list of messages

[Column 1]
messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="What is your name"), ] resp = llm.chat(messages) ```

``` print(resp) ```

### Streaming
Using `stream_complete` endpoint
``` response = llm.stream_complete("Who is Paul Graham?") ```
``` for r in response: print(r.delta, end="") ```

Using `stream_chat` endpoint
``` from llama_index.core.llms import ChatMessage
messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="What is your name"), ] resp = llm.stream_chat(messages) ```

``` for r in resp: print(r.delta, end="") ```

``` Arr matey, I be known as Captain Redbeard the fearsome pirate who's known for his cunning and bravery on the high seas of course, that's just what I tell people. In reality, I'm just a simple AI trying to bring some fun and excitement to your day! ```

[Column 2]
``` assistant: Arr matey, I be known as Captain Redbeard, the fiercest pirate to ever sail the seven seas! My ship, the Crimson Wave, strikes fear into the hearts of all who dare cross our path. With me hearty crew, we plunder and pillage, always seeking treasure and adventure. But don't be mistaken, I be a fair and honorable pirate, as long as ye show me respect and loyalty. Now, what be your name, landlubber? ```

``` Paul Graham is a British-born computer scientist, entrepreneur, venture capitalist, and essayist. He is best known for co-founding the startup incubator and investment firm, Y Combinator, which has provided funding and support to numerous successful startups including Dropbox, Airbnb, and Reddit.
Before founding Y Combinator, Graham was a successful entrepreneur himself, having co-founded the company Viaweb in 1995, which was later acquired by Yahoo in 1998. Graham is also known for his essays on startups, technology, and programming, which have been widely read and influential in the tech industry.
In addition to his work in the tech industry, Graham has a background in computer science and artificial intelligence, having earned a PhD in this field from Harvard University. He has also taught programming and entrepreneurship at several universities, including Harvard and Stanford. ```


[1] https://docs.together.ai/docs/inference-models