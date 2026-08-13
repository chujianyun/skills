# developers.llamaindex.ai/python/framework/integrations/llm/opus_4_1/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/opus_4_1/index.md

--- title: Using Opus 4.1 with LlamaIndex | Developer Documentation ---

In this notebook we are going to exploit Claude Opus 4.1 by Anthropic [1] advanced coding capabilities to create a cute website, and we’re going to do it within LlamaIndex!

## Build an LLM-based assistant with Opus 4.1
**1. Install needed dependencies**
``` ! pip install -q llama-index-llms-anthropic get-code-from-markdown ```
Let’s just define a helper function to help us fetch the code from Markdown:
``` from get_code_from_markdown import get_code_from_markdown

def fetch_code_from_markdown(markdown: str) -> str: return get_code_from_markdown(markdown, language="html") ```
Let’s now initialize our LLM:
``` import os import getpass

os.environ["ANTHROPIC_API_KEY"] = getpass.getpass() ```
``` from llama_index.llms.anthropic import Anthropic
llm = Anthropic(model="claude-opus-4-1-20250805", max_tokens=12000) ```
``` res = llm.complete( "Can you build a llama-themed static HTML page, with cute little bouncing animations and blue/white/indigo as theme colors?" ) ```

Let’s now get the code and write it to an HTML file!
``` html_code = fetch_code_from_markdown(res.text)
with open("index.html", "w") as f: for block in html_code: f.write(block) ```

You can now download `index.html` and take a look at the results :)
Llama Paradise HTML
## Build an agent with Opus 4.1
We can also build a simple calculator agent using Claude Opus 4.1
``` from llama_index.core.agent.workflow import FunctionAgent

def multiply(a: int, b: int) -> int: """Multiply two integers and return an integer""" return a * b

def add(a: int, b: int) -> int: """Sum two integers and return an integer""" return a + b

agent = FunctionAgent( name="CalculatorAgent", description="Useful to perform basic arithmetic operations", system_prompt="You are a calculator agent, you should perform arithmetic operations using the tools available to you.", tools=[multiply, add], llm=llm, ) ```
Let’s now run the agent through and get the result for a multiplication:

handler = agent.run("What is 60 multiplied by 95?")

``` Calling tool multiply with arguments:
{'a': 60, 'b': 95} Result from calling tool multiply:
5700 Final response 60 multiplied by 95 equals 5,700. ```
Let’s also run it with a sum!
``` from llama_index.core.agent.workflow import ToolCall, ToolCallResult
handler = agent.run("What is 1234 plus 5678?")
async for event in handler.stream_events(): if isinstance(event, ToolCallResult): print( f"Result from calling tool {event.tool_name}:\n\n{event.tool_output}" ) if isinstance(event, ToolCall): print( f"Calling tool {event.tool_name} with arguments:\n\n{event.tool_kwargs}" )

response = await handler
print("Final response") print(response) ```
``` Calling tool add with arguments:
{'a': 1234, 'b': 5678} Result from calling tool add:
6912 Final response 1234 plus 5678 equals 6912. ```
If you want more content around Anthropic, make sure to check out our general example notebook

[1] https://www.anthropic.com/news/claude-opus-4-1