# developers.llamaindex.ai/python/framework/integrations/llm/fireworks_cookbook/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/fireworks_cookbook/index.md

--- title: Fireworks Function Calling Cookbook | Developer Documentation ---

Fireworks.ai supports function calling for its LLMs, similar to OpenAI. This lets users directly describe the set of tools/functions available and have the model dynamically pick the right function calls to invoke, without complex prompting on the user’s part.

Since our Fireworks LLM directly subclasses OpenAI, we can use our existing abstractions with Fireworks.
We show this on three levels: directly on the model API, as part of a Pydantic Program (structured output extraction), and as part of an agent.
``` %pip install llama-index-llms-fireworks ```
``` %pip install llama-index ```
``` import os
os.environ["FIREWORKS_API_KEY"] = "fw_3ZkvBpQyjRzbicpihhrihaEP" ```
``` from llama_index.llms.fireworks import Fireworks
## define fireworks model, for a list of function calling models see: https://app.fireworks.ai/models/?filter=LLM&functionCalling=true llm = Fireworks( model="accounts/fireworks/models/deepseek-v3p1-terminus", temperature=0 ) ```

## Function Calling on the LLM Module
You can directly input function calls on the LLM module.
``` import os import json from openai import OpenAI from pydantic import BaseModel, Field from llama_index.llms.openai.utils import to_openai_tool

class Song(BaseModel): """A song with name and artist"""
name: str = Field(description="The name of the song") artist: str = Field(description="The artist who performed the song")

song_fn = to_openai_tool(Song)
# Initialize Fireworks client client = OpenAI( api_key=os.environ.get("FIREWORKS_API_KEY"), base_url="https://api.fireworks.ai/inference/v1", )

response = client.chat.completions.create( model="accounts/fireworks/models/kimi-k2-instruct-0905", messages=[{"role": "user", "content": "Generate a song from Beyonce"}], tools=[song_fn], temperature=0.1, )

print(response)
if response.choices[0].message.tool_calls: tool_call = response.choices[0].message.tool_calls[0] print(f"\nTool called: {tool_call.function.name}")
# Parse the arguments to get structured output arguments = json.loads(tool_call.function.arguments) print(f"Arguments: {arguments}")
# Create Song instance from the structured output song = Song(**arguments) print(f"\nExtracted Song:") print(f"Name: {song.name}") print(f"Artist: {song.artist}") ```

```` ChatCompletion(id='07921e74-5dca-409c-a4d3-1a2e0c7cd1e7', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='```json\n{\n "name": "Halo",\n "artist": "Beyoncé"\n}\n```', refusal=None, role='assistant', annotations=None, audio=None, function_call=None, tool_calls=None))], created=1761704700, model='accounts/fireworks/models/kimi-k2-instruct-0905', object='chat.completion', service_tier=None, system_fingerprint=None, usage=CompletionUsage(completion_tokens=25, prompt_tokens=145, total_tokens=170, completion_tokens_details=None, prompt_tokens_details=PromptTokensDetails(audio_tokens=None, cached_tokens=0)))

````