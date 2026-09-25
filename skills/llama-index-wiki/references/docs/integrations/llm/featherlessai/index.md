# developers.llamaindex.ai/python/framework/integrations/llm/featherlessai/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/featherlessai/index.md

--- title: Featherless AI LLM | Developer Documentation ---

This notebook shows how to use `Featherless AI` as an LLM. Check out the full list of models featherless.ai [1].
Visit <https://www.featherless.ai/> and sign up to get an API key.
## Setup
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-llms-featherlessai ```
``` !pip install llama-index ```
``` from llama_index.llms.featherlessai import FeatherlessLLM ```
``` None of PyTorch, TensorFlow >= 2.0, or Flax have been found. Models won't be available and only tokenizers, configuration and file/data utilities can be used. ```
``` # set api key in env or in llm # import os # os.environ["FEATHERLESS_API_KEY"] = "your api key"

llm = FeatherlessLLM(model="Qwen/Qwen3-32B", api_key="<API_KEY>") ```
``` resp = llm.complete("Is 9.9 or 9.11 bigger?") ```

``` 9.11 is bigger than 9.9. ```
#### Call `chat` with a list of messages

messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="What is your name"), ] resp = llm.chat(messages) ```

``` print(resp) ```
``` assistant: Yer want ta know me name, eh? Alright then, matey! Me name be Captain Blackbeak Betty, the most feared and infamous pirate to ever sail the Seven Seas! Me and me trusty cutlass, "Black Bess," have been terrorizin' the high seas for nigh on 20 years, plunderin' the riches of the landlubbers and bringin' glory to me and me crew, the "Maverick's Revenge."
Now, don't ye be thinkin' that just 'cause I be a lady pirate, I be soft or weak. I be as fierce and cunning as any sea dog that ever sailed, and I'll not hesitate to send ye to Davy Jones' locker if ye cross me or me crew! So, what be bringin' ye to these waters, matey? Are ye lookin' to join me crew, or are ye just lookin' to get yerself killed? ```
### Streaming
Using `stream_complete` endpoint
``` response = llm.stream_complete("Who is Paul Graham?") ```
``` for r in response: print(r.delta, end="") ```
``` Paul Graham is a British computer programmer, entrepreneur, and essayist. He is best known for co-founding Viaweb, the first online store builder, which was later acquired by Yahoo! and became Yahoo! Store. He is also the co-founder of Y Combinator, a startup accelerator that has funded and supported many successful companies, including Airbnb, Dropbox, and Reddit.
Graham is also a well-known essayist and has written extensively on topics such as programming, entrepreneurship, and technology. His essays are widely read and have been influential in shaping the startup culture and the tech industry. Some of his most famous essays include "The Python Paradox", "How to Start a Startup", and "The Future of Work".
Graham is also a Lisp programmer and has written several books on the subject, including "On Lisp" and "ANSI Common Lisp". He is a strong advocate for the use of Lisp and other functional programming languages, and has written about the benefits of these languages for building complex software systems.
Throughout his career, Graham has been recognized for his contributions to the tech industry, including being named one of the most influential people in technology by TIME Magazine. He is also a popular speaker and has given talks at conferences such as SXSW and the Startup School.
Some of the key ideas and concepts that Graham has written about and advocated for include:
* The importance of startups and entrepreneurship in driving innovation and economic growth * The need for programmers to learn and use functional programming languages, such as Lisp * The benefits of using online platforms and tools to build and launch startups * The importance of focusing on building a strong product and user experience, rather than just trying to make money * The need for startups to be flexible and adaptable, and to be willing to pivot and change direction when necessary.

Overall, Paul Graham is a highly influential and respected figure in the tech industry, known for his insights and ideas on programming, entrepreneurship, and technology. ```
Using `stream_chat` endpoint
``` from llama_index.core.llms import ChatMessage
messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="What is your name"), ] resp = llm.stream_chat(messages) ```

``` for r in resp: print(r.delta, end="") ```
``` Yer want ta know me name, eh? Alright then, matey! Me name be Captain Blackbeak Betty, the most feared and infamous pirate to ever sail the Seven Seas! Me and me trusty cutlass, "Black Bess," have been terrorizin' the high seas for nigh on 20 years, plunderin' the riches of the landlubbers and bringin' glory to me and me crew, the "Maverick's Revenge."
Me name be whispered in fear and awe by all who sail the seas, from the scurvy dogs of the Royal Navy to the scallywags of the pirate underworld. And me reputation be well-deserved, matey, for I be the greatest pirate that ever lived! So, what be bringin' ye to these fair waters? Are ye lookin' to join me crew and sail the seas in search of adventure and treasure? Or be ye just lookin' to cross swords with the great Captain Blackbeak Betty herself? Either way, ye be in fer a wild ride, matey!
```

[1] https://www.featherless.ai/