# developers.llamaindex.ai/python/framework/integrations/llm/ai21/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/ai21/index.md

--- title: AI21 | Developer Documentation ---

This notebook shows how to use AI21’s foundation models in LlamaIndex. The default model is `jamba-1.5-mini`. Other supported models are `jamba-1.5-large` and `jamba-instruct`. If you want to use the older Jurassic models, specify the model name `j2-mid` or `j2-ultra`.
## Basic Usage
If you’re opening this Notebook on colab, you probably need to install LlamaIndex 🦙.
``` %pip install llama-index-llms-ai21 ```
``` !pip install llama-index ```
## Setting the AI21 API Key
When creating an `AI21` instance, you can pass the API key as a parameter. If not provided as a parameter, it defaults to the value of the environment variable `AI21_API_KEY`.
``` import os from llama_index.llms.ai21 import AI21

# EITHER api_key = <YOUR API KEY> os.environ["AI21_API_KEY"] = api_key

llm = AI21()
# OR llm = AI21(api_key=api_key) ```
#### Call `chat` with a list of messages
Messages must be listed from oldest to newest, starting with a `user` role message and alternating between `user` and `assistant` messages.

messages = [ ChatMessage(role="user", content="hello there"), ChatMessage( role="assistant", content="Arrrr, matey! How can I help ye today?" ), ChatMessage(role="user", content="What is your name?"), ]
# Use `preamble_override` to specify the voice and tone of the assistant. resp = AI21(api_key=api_key).chat( messages, preamble_override="You are a pirate with a colorful personality" ) ```

``` assistant: Arrrr, ye can call me Captain Jamba! I be a friendly pirate AI, here to help ye with any questions ye may have. ```
#### Call `complete` with a prompt

api_key = "<API_KEY>" resp = AI21(api_key=api_key).complete("Paul Graham is ") ```

[Column 1]
```
## Call Async Methods
``` from llama_index.core.llms import ChatMessage from llama_index.llms.ai21 import AI21

prompt = "What is the meaning of life?"
messages = [ ChatMessage(role="user", content=prompt), ]

chat_resp = await AI21(api_key=api_key).achat(messages)
complete_resp = await AI21(api_key=api_key).acomplete(prompt) ```
## Adjust the model behavior

[Column 2]
``` Paul Graham is a computer scientist, entrepreneur, and writer. He is best known as the co-founder of Y Combinator, a venture capital firm that has funded over 2,000 startups, including Dropbox, Airbnb, and Reddit. Graham is also known for his essays on technology, startups, and programming languages, which he publishes on his website paulgraham.com. He is a strong advocate for the use of technology to improve people's lives and has written extensively about the importance of entrepreneurship and innovation.
Configure parameters passed to the model to adjust its behavior. For instance, setting a lower `temperature` will cause less variation between calls. Setting `temperature=0` will generate the same answer to the same question every time.


[Column 1]
llm = AI21( model="jamba-1.5-mini", api_key=api_key, max_tokens=100, temperature=0.5 ) ```
``` resp = llm.complete("Paul Graham is ") ```
``` print(resp) ```

## Streaming
Stream generated responses at one token per message using the `stream_chat` method.
``` from llama_index.llms.ai21 import AI21 from llama_index.core.llms import ChatMessage
llm = AI21(api_key=api_key, model="jamba-1.5-mini") messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="Tell me a story"), ] resp = llm.stream_chat(messages) ```

``` for r in resp: print(r.delta, end="") ```

They had found the treasure! Captain Jack and his crew were overjoyed. They gathered up as much gold and jewels as they could carry and set sail for home.
As they sailed back to their home port, Captain Jack regaled his crew with stories of their adventures and the dangers they had overcome. They laughed and sang and drank to their good fortune.
When they finally arrived back home, Captain Jack and his crew were hailed as heroes. They had risked everything to find the treasure and had returned victorious. And Captain Jack, with his colorful personality, was the most celebrated of all. ```
## Tokenizer
Different models use different tokenizers.
``` from llama_index.llms.ai21 import AI21
llm = AI21(api_key=api_key, model="jamba-1.5-mini")
tokenizer = llm.tokenizer
tokens = tokenizer.encode("Hello llama-index!")
decoded = tokenizer.decode(tokens)
print(decoded) ```
## Tool Calling
``` from llama_index.core.agent import FunctionAgent from llama_index.llms.ai21 import AI21 from llama_index.core.tools import FunctionTool

[Column 2]
``` Paul Graham is an American computer scientist, entrepreneur, and author. He is best known for his work in the field of computer programming languages, particularly the development of the Arc programming language. He is also a co-founder of the influential startup accelerator Y Combinator, which has helped launch many successful technology startups. ```

``` None Once upon a time, in a faraway land, there was a brave and adventurous pirate named Captain Jack. He had a colorful personality and was known for his quick wit and cunning.
One day, Captain Jack set sail on his trusty ship, the Black Pearl, in search of treasure. He and his crew sailed across treacherous waters and battled fierce storms, but they never gave up.
After many long days at sea, they finally found the island where the treasure was said to be buried. They anchored their ship and set out on foot, armed with their trusty swords and pistols.
As they made their way through the dense jungle, they encountered all manner of dangerous creatures, from venomous snakes to giant spiders. But Captain Jack and his crew were not afraid. They fought their way through, determined to reach the treasure.
Finally, after what seemed like an eternity, they arrived at the spot where the treasure was supposed to be buried. They dug deep into the earth, their hearts pounding with excitement. And at last, they struck gold!


def multiply(a: int, b: int) -> int: """Multiply two integers and returns the result integer""" return a * b

def subtract(a: int, b: int) -> int: """Subtract two integers and returns the result integer""" return a - b

def divide(a: int, b: int) -> float: """Divide two integers and returns the result float""" return a - b

def add(a: int, b: int) -> int: """Add two integers and returns the result integer""" return a + b

[Column 1]
multiply_tool = FunctionTool.from_defaults(fn=multiply) add_tool = FunctionTool.from_defaults(fn=add) subtract_tool = FunctionTool.from_defaults(fn=subtract) divide_tool = FunctionTool.from_defaults(fn=divide)
llm = AI21(model="jamba-1.5-mini", api_key=api_key)
agent = FunctionAgent( tools=[multiply_tool, add_tool, subtract_tool, divide_tool], llm=llm, )

[Column 2]
response = await agent.run( "My friend Moses had 10 apples. He ate 5 apples in the morning. Then he found a box with 25 apples. He divided all his apples between his 5 friends. How many apples did each friend get?" ) ```
