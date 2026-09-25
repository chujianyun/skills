# developers.llamaindex.ai/python/framework/understanding/using_llms/index.md
> https://developers.llamaindex.ai/python/framework/understanding/using_llms/index.md

--- title: Using LLMs | Developer Documentation ---

For a list of our supported LLMs and a comparison of their functionality, check out our LLM module guide.
One of the first steps when building an LLM-based application is which LLM to use; they have different strengths and price points and you may wish to use more than one.
LlamaIndex provides a single interface to a large number of different LLMs. Using an LLM can be as simple as installing the appropriate integration:
Terminal window
``` pip install llama-index-llms-openai ```
And then calling it in a one-liner:
``` from llama_index.llms.openai import OpenAI

[Column 1]
response = OpenAI().complete("William Shakespeare is ") print(response) ```
`complete` is also available as an async method, `acomplete`.
``` handle = OpenAI().stream_complete("William Shakespeare is ")

[Column 2]
Note that this requires an API key called `OPENAI_API_KEY` in your environment; see the starter tutorial for more details.
You can also get a streaming response by calling `stream_complete`, which returns a generator that yields tokens as they are produced:


for token in handle: print(token.delta, end="", flush=True) ```
`stream_complete` is also available as an async method, `astream_complete`.
## Chat interface
The LLM class also implements a `chat` method, which allows you to have more sophisticated interactions:
``` messages = [ ChatMessage(role="system", content="You are a helpful assistant."), ChatMessage(role="user", content="Tell me a joke."), ] chat_response = llm.chat(messages) ```

For streaming responses (where tokens are yielded as they are generated), `stream_chat` and `astream_chat` are available.
**Synchronous (`stream_chat`):**
Use this in standard Python scripts or notebooks where blocking operations are acceptable. It returns a generator directly.
``` stream_response = llm.stream_chat(messages)

for token in stream_response: print(token.delta, end="", flush=True) ```
**Asynchronous (`astream_chat`):**
When using async frameworks (like FastAPI), remember to `await` the method call and iterate over the returned async stream.
``` stream_response = await llm.astream_chat(messages)

async for token in stream_response: print(token.delta, end="", flush=True) ```
## Specifying models
Many LLM integrations provide more than one model. You can specify a model by passing the `model` parameter to the LLM constructor:
``` llm = OpenAI(model="gpt-4o-mini") response = llm.complete("Who is Laurie Voss?") print(response) ```

## Multi-Modal LLMs
Some LLMs support multi-modal chat messages. This means that you can pass in a mix of text and other modalities (images, audio, video, etc.) and the LLM will handle it.
Currently, LlamaIndex supports text, images, and audio inside ChatMessages using content blocks.
``` from llama_index.core.llms import ChatMessage, TextBlock, ImageBlock from llama_index.llms.openai import OpenAI

llm = OpenAI(model="gpt-4o")

messages = [ ChatMessage( role="user", blocks=[ ImageBlock(path="image.png"), TextBlock(text="Describe the image in a few sentences."), ], ) ]

resp = llm.chat(messages) print(resp.message.content) ```
## Tool Calling
Some LLMs (OpenAI, Anthropic, Gemini, Ollama, etc.) support tool calling directly over API calls — this means tools and functions can be called without specific prompts and parsing mechanisms.
``` from llama_index.core.tools import FunctionTool from llama_index.llms.openai import OpenAI

def generate_song(name: str, artist: str) -> Song: """Generates a song with provided name and artist.""" return {"name": name, "artist": artist}

tool = FunctionTool.from_defaults(fn=generate_song)

llm = OpenAI(model="gpt-4o") response = llm.predict_and_call( [tool], "Pick a random song for me", ) print(str(response)) ```

For more details on even more advanced tool calling, check out the in-depth guide using OpenAI. The same approaches work for any LLM that supports tools/functions (e.g. Anthropic, Gemini, Ollama, etc.).
You can learn more about tools and agents in the tools guide.
## Available LLMs
We support integrations with OpenAI, Anthropic, Mistral, DeepSeek, Hugging Face, and dozens more. Check out our module guide to LLMs for a full list, including how to run a local model.
Tip
A general note on privacy and LLM usage can be found on the privacy page.
### Using a local LLM
LlamaIndex doesn’t just support hosted LLM APIs; you can also run a local model such as Meta’s Llama 3 locally. For example, if you have Ollama [1] installed and running:
``` from llama_index.llms.ollama import Ollama

llm = Ollama( model="llama3.3", request_timeout=60.0, # Manually set the context window to limit memory usage context_window=8000, ) ```
See the custom LLM’s How-To for more details on using and configuring LLM models.

[1] https://github.com/ollama/ollama