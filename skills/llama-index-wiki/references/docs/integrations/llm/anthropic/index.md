# developers.llamaindex.ai/python/framework/integrations/llm/anthropic/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/anthropic/index.md

--- title: Anthropic | Developer Documentation ---

Anthropic offers many state-of-the-art models from the haiku, sonnet, and opus families.
Read on to learn how to use these models with LlamaIndex!
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-llms-anthropic ```
#### Set Tokenizer
First we want to set the tokenizer, which is slightly different than TikToken. This ensures that token counting is accurate throughout the library.
**NOTE**: Anthropic recently updated their token counting API. Older models like claude-2.1 are no longer supported for token counting in the latest versions of the Anthropic python client.
``` from llama_index.llms.anthropic import Anthropic from llama_index.core import Settings

tokenizer = Anthropic().tokenizer Settings.tokenizer = tokenizer ```
## Basic Usage

os.environ["ANTHROPIC_API_KEY"] = "sk-..." ```
You can call `complete` with a prompt:

# To customize your API key, do this # otherwise it will lookup ANTHROPIC_API_KEY from your env variable # llm = Anthropic(api_key="<api_key>") llm = Anthropic(model="claude-sonnet-4-0")

``` print(resp) ```

You can also call `chat` with a list of chat messages:

messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="Tell me a story"), ] llm = Anthropic(model="claude-sonnet-4-0") resp = llm.chat(messages)

print(resp) ```
``` assistant: Ahoy there, matey! *adjusts tricorn hat and strokes beard*
Let me spin ye a tale from me seafarin' days, when the ocean was as wild as a kraken's temper and twice as unpredictable!
**The Tale of the Singing Compass**
'Twas a foggy mornin' when me crew and I discovered the strangest treasure - not gold or jewels, mind ye, but a compass that hummed sea shanties! Aye, ye heard right! This peculiar little instrument would warble different tunes dependin' on which direction it pointed.
North brought forth a melancholy ballad about lost loves, while South sang a jaunty tune that made even our grumpiest sailor, One-Eyed Pete, tap his peg leg. But here's the curious part - when it pointed West, it sang a mysterious melody none of us had ever heard, with words in an ancient tongue.
Bein' the adventurous sort (and perhaps a wee bit foolish), we followed that western song for three days and three nights. The compass led us through treacherous waters, past islands that seemed to shimmer like mirages, until we reached a hidden cove where the water glowed like liquid emeralds.
And there, me hearty friend, we found the greatest treasure of all - not riches, but a family of merfolk who had been waitin' centuries for someone to return their enchanted compass! They rewarded our kindness with safe passage through any storm and the secret locations of three genuine treasure islands.
*winks and takes a swig from an imaginary bottle*
Sometimes the best adventures come from followin' the strangest songs, savvy? ```
## Streaming Support
Every method supports streaming through the `stream_` prefix.

resp = llm.stream_complete("Who is Paul Graham?") for r in resp: print(r.delta, end="") ```

**Y Combinator Co-founder**: He co-founded Y Combinator in 2005, one of the most successful startup accelerators in the world. Y Combinator has funded companies like Airbnb, Dropbox, Stripe, Reddit, and hundreds of others.
**Programming and Lisp**: He's a strong advocate for the Lisp programming language and wrote influential books including "On Lisp" and "ANSI Common Lisp."
**Viaweb**: In the 1990s, he co-founded Viaweb, one of the first web-based software companies, which was acquired by Yahoo in 1998 and became Yahoo Store.
**Essays**: He's written many influential essays on startups, programming, and technology, published on his website paulgraham.com. His essays are widely read in the tech community and cover topics like how to start a startup, what makes a good programmer, and the nature of innovation.
**Art and Academia**: He has a PhD in Computer Science from Harvard and also studied painting at the Rhode Island School of Design and the Accademia di Belle Arti in Florence.
Graham is considered one of the most influential figures in the startup ecosystem and has helped shape modern thinking about entrepreneurship and technology startups. ```
``` from llama_index.core.llms import ChatMessage
messages = [ ChatMessage(role="user", content="Who is Paul Graham?"), ]
resp = llm.stream_chat(messages) for r in resp: print(r.delta, end="") ```

**Writing**: Graham is well-known for his thoughtful essays on startups, technology, programming, and entrepreneurship, published on his website paulgraham.com. His essays are widely read in tech circles and cover topics like how to start a startup, the nature of innovation, and technology trends.
**Influence**: He's considered one of the most influential people in Silicon Valley's startup ecosystem, both through Y Combinator's success and his writings that have shaped how many people think about entrepreneurship and technology.
His combination of technical expertise, business acumen, and clear writing has made him a prominent voice in the tech industry for over two decades. ```
## Async Usage
Every synchronous method has an async counterpart.

resp = await llm.astream_complete("Who is Paul Graham?") async for r in resp: print(r.delta, end="") ```
``` Paul Graham is a computer programmer, entrepreneur, venture capitalist, and essayist. Here are the key things he's known for:

**Programming**: He's a respected figure in the programming community, particularly known for his work with Lisp programming language. He wrote influential books like "On Lisp" and "ANSI Common Lisp."
**Essays**: Graham writes widely-read essays on startups, technology, programming, and society, published on his website paulgraham.com. His essays like "Do Things That Don't Scale" and "How to Start a Startup" are considered essential reading in the tech world.
**Entrepreneur**: Before Y Combinator, he co-founded Viaweb (one of the first web-based applications for building online stores), which was acquired by Yahoo in 1998 for about $49 million and became Yahoo Store.
**Art background**: Interestingly, he also has a background in art and studied painting, which influences his perspective on creativity and aesthetics in technology.
Graham is considered one of the most influential voices in Silicon Valley and the broader startup ecosystem. ```
``` messages = [ ChatMessage(role="user", content="Who is Paul Graham?"), ]
resp = await llm.achat(messages) print(resp) ```
``` assistant: Paul Graham is a computer programmer, entrepreneur, venture capitalist, and essayist. Here are the key things he's known for:
**Y Combinator**: He co-founded this highly influential startup accelerator in 2005, which has helped launch companies like Airbnb, Dropbox, Stripe, and Reddit. Y Combinator provides seed funding and mentorship to early- stage startups.
**Programming**: He's a respected figure in the programming community, particularly known for his work with Lisp programming language and for co-creating the first web-based application, Viaweb, in the 1990s (which was sold to Yahoo and became Yahoo Store).
**Writing**: Graham is well-known for his thoughtful essays on startups, technology, programming, and society, published on his website paulgraham.com. His essays are widely read in tech circles and cover topics like how to start a startup, the nature of innovation, and social commentary.
**Books**: He's authored several books including "Hackers & Painters" and "On Lisp."
**Influence**: He's considered one of the most influential people in Silicon Valley's startup ecosystem, both through Y Combinator's impact and his writings on entrepreneurship and technology.
Graham is known for his analytical thinking and contrarian perspectives on business, technology, and culture. ```
## Vertex AI Support
By providing the `region` and `project_id` parameters (either through environment variables or directly), you can use an Anthropic model through Vertex AI.
``` import os
os.environ["ANTHROPIC_PROJECT_ID"] = "YOUR PROJECT ID HERE" os.environ["ANTHROPIC_REGION"] = "YOUR PROJECT REGION HERE" ```
Do keep in mind that setting region and project\_id here will make Anthropic use the Vertex AI client
## Bedrock Support
LlamaIndex also supports Anthropic models through AWS Bedrock.

# Note: this assumes you have standard AWS credentials configured in your environment llm = Anthropic( model="anthropic.claude-3-7-sonnet-20250219-v1:0", aws_region="us-east-1", )

resp = llm.complete("Who is Paul Graham?") ```
## Multi-Modal Support
Using `ChatMessage` objects, you can pass in images and text to the LLM.
``` !wget https://cdn.pixabay.com/photo/2021/12/12/20/00/play-6865967_640.jpg -O image.jpg ```
``` from llama_index.core.llms import ChatMessage, TextBlock, ImageBlock from llama_index.llms.anthropic import Anthropic

[Column 1]
messages = [ ChatMessage( role="user", blocks=[ ImageBlock(path="image.jpg"), TextBlock(text="What is in this image?"), ], ) ]
resp = llm.chat(messages) print(resp) ```
## Prompt Caching
``` from llama_index.core.llms import ChatMessage from llama_index.llms.anthropic import Anthropic

[Column 2]
``` assistant: This image shows four wooden dice on a dark fabric surface. The dice appear to be made of light-colored wood and have the traditional black dots (pips) marking the numbers on each face. They are scattered casually on what looks like a dark blue or black cloth background. ```

Anthropic models support the idea of prompt cahcing — wherein if a prompt is repeated multiple times, or the start of a prompt is repeated, the LLM can reuse pre-calculated attention results to speed up the response and lower costs.
To enable prompt caching, you can set `cache_control` on your `ChatMessage` objects, or set `cache_idx` on the LLM to always cache the first X messages (with -1 being all messages).


[Column 1]
# cache individual message(s) messages = [ ChatMessage( role="user", content="<some very long prompt>", additional_kwargs={"cache_control": {"type": "ephemeral"}}, ), ]

resp = llm.chat(messages)
# cache first X messages (with -1 being all messages) llm = Anthropic(model="claude-sonnet-4-0", cache_idx=-1)
resp = llm.chat(messages) ```
## Structured Prediction
``` from llama_index.llms.anthropic import Anthropic from llama_index.core.prompts import PromptTemplate from llama_index.core.bridge.pydantic import BaseModel from typing import List

[Column 2]
LlamaIndex provides an intuitive interface for converting any Anthropic LLMs into a structured LLM through `structured_predict` - simply define the target Pydantic class (can be nested), and given a prompt, we extract out the desired object.


class MenuItem(BaseModel): """A menu item in a restaurant."""
course_name: str is_vegetarian: bool

class Restaurant(BaseModel): """A restaurant with name, city, and cuisine."""
name: str city: str cuisine: str menu_items: List[MenuItem]

[Column 1]
llm = Anthropic(model="claude-sonnet-4-0") prompt_tmpl = PromptTemplate( "Generate a restaurant in a given city {city_name}" )
# Option 1: Use `as_structured_llm` restaurant_obj = ( llm.as_structured_llm(Restaurant) .complete(prompt_tmpl.format(city_name="Miami")) .raw ) # Option 2: Use `structured_predict` # restaurant_obj = llm.structured_predict(Restaurant, prompt_tmpl, city_name="Miami") ```

``` restaurant_obj ```

#### Structured Prediction with Streaming
Any LLM wrapped with `as_structured_llm` supports streaming through `stream_chat`.
``` from llama_index.core.llms import ChatMessage from IPython.display import clear_output from pprint import pprint
input_msg = ChatMessage.from_str("Generate a restaurant in San Francisco")
sllm = llm.as_structured_llm(Restaurant) stream_output = sllm.stream_chat([input_msg]) for partial_output in stream_output: clear_output(wait=True) pprint(partial_output.raw.dict()) restaurant_obj = partial_output.raw

restaurant_obj ```
``` {'city': 'San Francisco', 'cuisine': 'California Fusion', 'menu_items': [{'course_name': 'Dungeness Crab Cakes', 'is_vegetarian': False}, {'course_name': 'Roasted Beet and Arugula Salad', 'is_vegetarian': True}, {'course_name': 'Grilled Pacific Salmon', 'is_vegetarian': False}, {'course_name': 'Wild Mushroom Risotto', 'is_vegetarian': True}, {'course_name': 'Grass-Fed Beef Tenderloin', 'is_vegetarian': False}, {'course_name': 'Chocolate Lava Cake', 'is_vegetarian': True}], 'name': 'Golden Gate Bistro'}

[Column 2]
``` Restaurant(name='Ocean Breeze Bistro', city='Miami', cuisine='Seafood', menu_items=[MenuItem(course_name='Grilled Mahi-Mahi with Mango Salsa', is_vegetarian=False), MenuItem(course_name='Coconut Shrimp with Pineapple Dipping Sauce', is_vegetarian=False), MenuItem(course_name='Quinoa and Black Bean Bowl', is_vegetarian=True), MenuItem(course_name='Key Lime Pie', is_vegetarian=True), MenuItem(course_name='Lobster Bisque', is_vegetarian=False), MenuItem(course_name='Grilled Vegetable Platter with Chimichurri', is_vegetarian=True)])


[Column 1]
## Model Thinking
``` from llama_index.llms.anthropic import Anthropic from llama_index.core.llms import ChatMessage
llm = Anthropic( model="claude-sonnet-4-0", # max_tokens must be greater than budget_tokens max_tokens=64000, # temperature must be 1.0 for thinking to work temperature=1.0, thinking_dict={"type": "enabled", "budget_tokens": 1600}, ) ```

``` messages = [ ChatMessage(role="user", content="(1234 * 3421) / (231 + 2341) = ?") ]
resp_gen = llm.stream_chat(messages)
for r in resp_gen: print(r.delta, end="")
print() print(r.message.content) ```
``` I'll solve this step by step.

[Column 2]
Restaurant(name='Golden Gate Bistro', city='San Francisco', cuisine='California Fusion', menu_items=[MenuItem(course_name='Dungeness Crab Cakes', is_vegetarian=False), MenuItem(course_name='Roasted Beet and Arugula Salad', is_vegetarian=True), MenuItem(course_name='Grilled Pacific Salmon', is_vegetarian=False), MenuItem(course_name='Wild Mushroom Risotto', is_vegetarian=True), MenuItem(course_name='Grass-Fed Beef Tenderloin', is_vegetarian=False), MenuItem(course_name='Chocolate Lava Cake', is_vegetarian=True)])

With `claude-3.7 Sonnet`, you can enable the model to “think” harder about a task, generating a chain-of-thought response before writing out the final answer.
You can enable this by passing in the `thinking_dict` parameter to the constructor, specififying the amount of tokens to reserve for the thinking process.


[Column 1]
Therefore: (1234 × 3421) ÷ (231 + 2341) = **1,641.42** I'll solve this step by step.
First, let me calculate the numerator: 1234 × 3421 = 4,221,514
Next, let me calculate the denominator: 231 + 2341 = 2,572
Now I can divide: 4,221,514 ÷ 2,572 = 1,641.42 (rounded to 2 decimal places)
Therefore: (1234 × 3421) ÷ (231 + 2341) = **1,641.42** ```
``` print(r.message.additional_kwargs["thinking"]["signature"]) ```

```
We can also expose the exact thinking process:
``` print(r.message.additional_kwargs["thinking"]["thinking"]) ```
``` I need to calculate (1234 * 3421) / (231 + 2341).
Let me do this step by step.
First, let me calculate the numerator: 1234 * 3421 1234 * 3421 = 1234 * (3000 + 400 + 20 + 1) = 1234 * 3000 + 1234 * 400 + 1234 * 20 + 1234 * 1 = 3,702,000 + 493,600 + 24,680 + 1,234 = 4,221,514

Now let me calculate the denominator: 231 + 2341 231 + 2341 = 2,572
So the expression becomes: 4,221,514 / 2,572
Let me do this division: 4,221,514 ÷ 2,572 = 1,641.4...
Let me be more precise: 4,221,514 ÷ 2,572 = 1,641.42...
Actually, let me double-check my multiplication: 1234 * 3421
1234 ×3421 ----- 1234 (1234 × 1) 2468 (1234 × 2, shifted one place) 4936 (1234 × 4, shifted two places) 3702 (1234 × 3, shifted three places) -----

Let me be more careful: 1234 × 1 = 1234 1234 × 20 = 24680 1234 × 400 = 493600 1234 × 3000 = 3702000

1234 + 24680 + 493600 + 3702000 = 4,221,514
That's correct.
Now 4,221,514 ÷ 2,572 ≈ 1,641.42 ```
## Tool/Function Calling
``` from llama_index.core.tools import FunctionTool from llama_index.core.llms import ChatMessage from llama_index.llms.anthropic import Anthropic from datetime import datetime

llm = Anthropic(model="claude-sonnet-4-0")

[Column 2]
``` EsgICkYIAxgCKkBcW71ZZ3zt/vVxd0Aw2evRNOsyewVAaXXFcHa2zRC5O/TG/Db+RfgHqKNF7EWL0WuJKRXJZ20Y/vfuHrqMZPS3EgytQs6cFIcaRHzCK4UaDPxTA/o9OoluSRUt+CIw3ivbQzQiJz4rxrk+anAcYu8kGwe16Ig9vHtamNNJG0C3Ou2cy9bshhs5Wg0TFksMKq8HeFZ7D0AurTGciR 7JkmeNAFWED0AWlMXBwaX910DSs9dqGkd8ZKVnj5hH/+pVs6KjD0rdttpu62PEZS0TAT+1i0nWoydpSZRj2QByzway45NNBitBoZGnc60G+Hu+oE3Ju4JNthVpbGR9NI0YGk/+hkh+xF4LMoWJJn6sXufxo6z0nUGGmysxF/+v3SKo0BrZhA18yDV8LY327StLKaGj6/D4khxLWLbWV 2IboHq2jcKscBgmH91Rems3/Lo1ziNAq05Tg4l/Avx4l6WdiEF8g/lyT5XTGN+YxN8UOR7PqNVaQ9iHxMMVGk+mO9F3AwbP+9F7nhlrim9JPm4v4BhmGgzuKNVEFjm8woj3wmdc2Iw95RiNZY1TRAAt2bZXlwVUy+gINE4xtVjY1pPmEEmXlR1P4I2+Vjax05d4BfBsCE83aPxH/WYNYnZ95bOIz2 DmAImEZXa3ineKz2JZWnWj5/T/lyEnaiB4bFqiSkUxOo+rWJrS2S8JGmyMg/zHpzHxdrrLxQQ0KmNICfDTJZDW8X0QR18DfuoVHZcOIkYgUM14GWngNcwmQeS2QiLbu+03husqHTFL27f4K8qyUn/E2hqtC/U2HNjEZFQhAsLNIunlQb4WnD6bhdx8s9DdD+rRWdyGcOe4rjW7syD/fxwrZQHDzXhb 40xA6BfHrg/vbbYfABd+fVopFzccFVfe/8rleKzLXn8OS6O+KE3rx5L+Rh0gfoc08RolFMzA/S+LGIkWN1I9JCxvsqjEcgAoYY+zkW44i6nNvbGFWuGWA/jK/D6vI1sjpO9YJ9XvGgfcXC9jmhpx86polTSIXYHOxkdNnTKTrvR/54DWKS6orSdA6+glA4ecC7ZnF+qpMkXDscSdH+Pnj+SEZMAYI 5tRhn6y1/XUxJtchWv2b3ZBQmsYCvs7YxoH3ryhSGG6SVtY9269o7a2zqwLtVMU5WqV9Jcq6NITW/RLJ7xGs/zX67u64ZaIto9VsSnRXIgaRY8HRybKB3ABXo27hiJadIecgvwO12+ds+x4O+su91gjCILOYSujTcjZ7EFXiaDOkIuFbEo6xg+wIcXxNtDcn7mQlqQ1s/JsARMxl7B9aQbz1B 6J49aIwMS03cAZrOgmmUHqy3b3ABQxMfMQOmvkm18kcypqNdW5JaXw3N0aKeboDT6StpduP+AL+fULF/uiqqxfZ+NgSEzGmqQQiPYX4djqH6O+M2cwam1BBYaDX/dGsKqRgB
Anthropic supports direct tool/function calling through the API. Using LlamaIndex, we can implement some core agentic tool calling patterns.


def get_current_time() -> dict: """Get the current time""" return {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

# uses the tool name, any type annotations, and docstring to describe the tool tool = FunctionTool.from_defaults(fn=get_current_time) ```
We can simply do a single pass to call the tool and get the result:
``` resp = llm.predict_and_call([tool], "What is the current time?") print(resp) ```

``` {'time': '2025-05-22 12:45:48'} ```
We can also use lower-level APIs to implement an agentic tool-calling loop!
``` chat_history = [ChatMessage(role="user", content="What is the current time?")] tools_by_name = {t.metadata.name: t for t in [tool]}

resp = llm.chat_with_tools([tool], chat_history=chat_history) tool_calls = llm.get_tool_calls_from_response( resp, error_on_no_tool_call=False )

if not tool_calls: print(resp) else: while tool_calls: # add the LLM's response to the chat history chat_history.append(resp.message)

for tool_call in tool_calls: tool_name = tool_call.tool_name tool_kwargs = tool_call.tool_kwargs

print(f"Calling {tool_name} with {tool_kwargs}") tool_output = tool.call(**tool_kwargs) print("Tool output: ", tool_output) chat_history.append( ChatMessage( role="tool", content=str(tool_output), # most LLMs like Anthropic, OpenAI, etc. need to know the tool call id additional_kwargs={"tool_call_id": tool_call.tool_id}, ) )

resp = llm.chat_with_tools([tool], chat_history=chat_history) tool_calls = llm.get_tool_calls_from_response( resp, error_on_no_tool_call=False ) print("Final response: ", resp.message.content) ```

``` Calling get_current_time with {} Tool output: {'time': '2025-05-22 12:45:51'} Final response: The current time is 12:45:51 on May 22, 2025. ```

## Server-Side Tool Calling
Anthropic now also supports server-side tool calling in latest versions.
Here’s an example of how to use it:

llm = Anthropic( model="claude-sonnet-4-0", max_tokens=1024, tools=[ { "type": "web_search_20250305", "name": "web_search", "max_uses": 3, # Limit to 3 searches } ], )

# Get response with citations response = llm.complete("What are the latest AI research trends?")
# Access the main response content print(response.text)
# Access citations if available for citation in response.citations: print(f"Source: {citation.get('url')} - {citation.get('cited_text')}") ```
``` Based on the latest research and industry reports, here are the key AI trends shaping 2025:
## 1. Agentic AI Takes Center Stage
Agentic AI - AI systems that can perform tasks independently with minimal human intervention - is emerging as the most significant trend for 2025. "Think of agents as the apps of the AI era," according to Microsoft executives. Early implementations will focus on small, structured internal tasks like password changes or vacation requests, with companies being cautious about deploying agents for customer-facing activities involving real money.
## 2. Advanced Reasoning Capabilities
AI models with advanced reasoning capabilities, like OpenAI's o1, can solve complex problems with logical steps similar to human thinking, making them particularly useful in science, coding, math, law, and medicine. Tech companies are competing to develop frontier models that push boundaries in natural-language processing, image generation, and coding.
## 3. Focus on Measurable ROI and Enterprise Adoption
In 2025, businesses are pushing harder for measurable outcomes from generative AI: reduced costs, demonstrable ROI, and efficiency gains. Despite over 90% of organizations increasing their generative AI use, only 8% consider their initiatives mature, indicating significant room for growth in practical implementation.
## 4. Scientific Discovery and Materials Science
AI is increasingly being applied to scientific discovery, with materials science emerging as a promising area following AI's success in protein research. Meta has released massive datasets and models to help scientists discover new materials faster.
## 5. Multimodal AI and Beyond Chatbots
As AI technology matures, developers and businesses are looking beyond chatbots toward building sophisticated software applications on top of large language models rather than deploying chatbots as standalone tools.
## 6. Dramatic Cost Reductions
Inference costs are falling dramatically - from $20 per million tokens to $0.07 per million tokens in less than a year, with the cost for GPT-3.5-level performance dropping over 280-fold between November 2022 and October 2024.
## 7. Closing Performance Gaps
The performance gap between top U.S. and Chinese AI models has narrowed from 9.26% to just 1.70% in one year, while open-weight models are closing the gap with closed models, reducing the performance difference from 8% to 1.7% on some benchmarks.
## 8. Increased Regulatory Activity
U.S. federal agencies introduced 59 AI-related regulations in 2024 - more than double the number in 2023 - while globally, legislative mentions of AI rose 21.3% across 75 countries.
## 9. Data Management Revolution
Generative AI is making unstructured data important again, with 94% of data and AI leaders saying AI interest is leading to greater focus on data, driving a "data lakehouse revolution" that combines data lakes' flexibility with data warehouses' structure.
## 10. Defense and Military Applications
Defense-tech companies are capitalizing on classified military data to train AI models, with mainstream AI companies like OpenAI pivoting toward military partnerships, joining Microsoft, Amazon, and Google in working with the Pentagon.
These trends indicate that 2025 Source: https://news.microsoft.com/source/features/ai/6-ai-trends-youll-see-more-of-in-2025/ - · AI-powered agents will do more with greater autonomy and help simplify your life at home and on the job. Source: https://news.microsoft.com/source/features/ai/6-ai-trends-youll-see-more-of-in-2025/ - In 2025, a new generation of AI-powered agents will do more — even handling certain tasks on your behalf. Source: https://sloanreview.mit.edu/article/five-trends-in-ai-and-data-science-for-2025/ - Let’s get agentic AI — the kind of AI that does tasks independently — out of the way first: It’s a sure bet for 2025’s “most trending AI trend.” Agent... Source: https://news.microsoft.com/source/features/ai/6-ai-trends-youll-see-more-of-in-2025/ - · “Think of agents as the apps of the AI era,” says Charles Lamanna, corporate vice president of business and industry Copilot. Source: https://sloanreview.mit.edu/article/five-trends-in-ai-and-data-science-for-2025/ - The earliest agents will be those for small, structured internal tasks with little money involved — for instance, helping change your password on the ...

Source: https://news.microsoft.com/source/features/ai/6-ai-trends-youll-see-more-of-in-2025/ - Models with advanced reasoning capabilities, like OpenAI o1, can already solve complex problems with logical steps that are similar to how humans thin... Source: https://www.morganstanley.com/insights/articles/ai-trends-reasoning-frontier-models-2025-tmt - The world’s biggest tech companies are vying to refine cutting-edge uses for artificial intelligence utilizations: large language models’ ability to r... Source: https://www.techtarget.com/searchenterpriseai/tip/9-top-AI-and-machine-learning-trends - In 2025, expect businesses to push harder for measurable outcomes from generative AI: reduced costs, demonstrable ROI and efficiency gains. Source: https://www.techtarget.com/searchenterpriseai/tip/9-top-AI-and-machine-learning-trends - In 2025, expect businesses to push harder for measurable outcomes from generative AI: reduced costs, demonstrable ROI and efficiency gains. Source: https://www.techtarget.com/searchenterpriseai/tip/9-top-AI-and-machine-learning-trends - In a September 2024 research report, Informa TechTarget's Enterprise Strategy Group found that, although over 90% of organizations had increased their... Source: https://www.technologyreview.com/2025/01/08/1109188/whats-next-for-ai-in-2025/ - Expect this trend to continue next year, and to see more data sets and models that are aimed specifically at scientific discovery.

Source: https://www.technologyreview.com/2025/01/08/1109188/whats-next-for-ai-in-2025/ - One potential area is materials science. Meta has released massive data sets and models that could help scientists use AI to discover new materials mu... Source: https://www.technologyreview.com/2025/01/08/1109188/whats-next-for-ai-in-2025/ - Meta has released massive data sets and models that could help scientists use AI to discover new materials much faster, and in December, Hugging Face,... Source: https://www.techtarget.com/searchenterpriseai/tip/9-top-AI-and-machine-learning-trends - But, as the technology matures, AI developers, end users and business customers alike are looking beyond chatbots. "People need to think more creative... Source: https://spectrum.ieee.org/ai-index-2025 - That means inference costs, or the expense of querying a trained model, are falling dramatically. Source: https://spectrum.ieee.org/ai-index-2025 - The report notes that the blue line represents a drop from $20 per million tokens to $0.07 per million tokens; the pink line shows a drop from $15 per...

Source: https://hai.stanford.edu/ai-index/2025-ai-index-report - Driven by increasingly capable small models, the inference cost for a system performing at the level of GPT-3.5 dropped over 280-fold between November... Source: https://spectrum.ieee.org/ai-index-2025 - In January 2024, the top U.S. model outperformed the best Chinese model by 9.26 percent; by February 2025, this gap had narrowed to just 1.70 percent.... Source: https://hai.stanford.edu/ai-index/2025-ai-index-report - Open-weight models are also closing the gap with closed models, reducing the performance difference from 8% to just 1.7% on some benchmarks in a singl... Source: https://hai.stanford.edu/ai-index/2025-ai-index-report - In 2024, U.S. federal agencies introduced 59 AI-related regulations—more than double the number in 2023—and issued by twice as many agencies. Globally... Source: https://sloanreview.mit.edu/article/five-trends-in-ai-and-data-science-for-2025/ - Generative AI has had another impact on organizations: It’s making unstructured data important again. In the 2025 AI & Data Leadership Executive Bench...
Source: https://www.morganstanley.com/insights/articles/ai-trends-reasoning-frontier-models-2025-tmt - Executives also highlighted the “data lakehouse revolution”—a trend to create unified data platforms that combine data lakes’ low-cost storage and fle... Source: https://www.technologyreview.com/2025/01/08/1109188/whats-next-for-ai-in-2025/ - In 2025, these trends will continue to be a boon for defense-tech companies like Palantir, Anduril, and others, which are now capitalizing on classifi... ```
## Tool Calling + Citations
In `llama-index-core>=0.12.46` + `llama-index-llms-anthropic>=0.7.6`, we’ve added support for outputting citable tool results!
Using Anthropic, you can now utilize server-side citations to cite specific parts of your tool results.
If the LLM cites a tool result, the citation will appear in the output as a `CitationBlock`, containing the source, title, and cited content.
Let’s cover a few ways to do this in practice.
First, let’s define a dummy tool/function that returns a citable block.
``` from llama_index.core import Document from llama_index.core.llms import CitableBlock, TextBlock from llama_index.core.tools import FunctionTool
dummy_text = Document.example().text

async def search_fn(query: str): """Useful for searching the web to answer questions.""" return CitableBlock( content=[TextBlock(text=dummy_text)], title="Facts about LLMs and LlamaIndex", source="https://docs.llamaindex.ai", )

search_tool = FunctionTool.from_defaults(search_fn) ```
``` from llama_index.llms.anthropic import Anthropic
llm = Anthropic( model="claude-sonnet-4-0", # api_key="sk-...", ) ```
### Agents + Citable Tools
You can also use these tools directly in pre-built agents, like the `FunctionAgent`, to get the same citations in the output.
``` from llama_index.core.agent.workflow import FunctionAgent
agent = FunctionAgent( tools=[search_tool], llm=llm, # Since we have a fake tool that returns a static result, we don't want to waste LLM tokens system_prompt="Only make one search query per user message.", timeout=None, ) ```

``` output = await agent.run("How do LlamaIndex and LLMs work together?") ```
``` from llama_index.core.llms import CitationBlock
print(output.response.content) print("----" * 20) for block in output.response.blocks: if isinstance(block, CitationBlock): print("Source: ", block.source) print("Title: ", block.title) print("Cited Content:\n", block.cited_content.text) print("----" * 20) ```

LLMs are a phenomenal piece of technology for knowledge generation and reasoning. They are pre-trained on large amounts of publicly available data. However, there's a key challenge: How do we best augment LLMs with our own private data?
This is where LlamaIndex comes in as the solution. LlamaIndex is a "data framework" to help you build LLM apps. Here's how they work together:
## Data Integration and Structure LlamaIndex offers data connectors to ingest your existing data sources and data formats (APIs, PDFs, docs, SQL, etc.) and provides ways to structure your data (indices, graphs) so that this data can be easily used with LLMs.
## Enhanced Query Interface LlamaIndex provides an advanced retrieval/query interface over your data: Feed in any LLM input prompt, get back retrieved context and knowledge-augmented output. This means when you ask a question, LlamaIndex retrieves relevant information from your private data and provides it as context to the LLM, enabling more accurate and personalized responses.
## Flexible Integration LlamaIndex allows easy integrations with your outer application framework (e.g. with LangChain, Flask, Docker, ChatGPT, anything else).
## User-Friendly Design LlamaIndex provides tools for both beginner users and advanced users. The high-level API allows beginner users to use LlamaIndex to ingest and query their data in 5 lines of code. The lower-level APIs allow advanced users to customize and extend any module (data connectors, indices, retrievers, query engines, reranking modules), to fit -------------------------------------------------------------------------------- Source: https://docs.llamaindex.ai Title: Facts about LLMs and LlamaIndex Cited Content:

### Manual Tool Calling + Citations
Using our tool that returns a citable block, we can manually call the LLM with the given tool in a manual agent loop.
Once the LLM stops making tool calls, we can return the final response and parse the citations from the response.
``` from llama_index.core.llms import ChatMessage, CitationBlock
chat_history = [ ChatMessage( role="system", # Since we have a fake tool that returns a static result, we don't want to waste LLM tokens content="Only make one search query per user message.", ), ChatMessage( role="user", content="How do LlamaIndex and LLMs work together?" ), ] resp = llm.chat_with_tools([search_tool], chat_history=chat_history) chat_history.append(resp.message)

tool_calls = llm.get_tool_calls_from_response( resp, error_on_no_tool_call=False ) while tool_calls: for tool_call in tool_calls: if tool_call.tool_name == "search_fn": tool_result = search_tool.call(tool_call.tool_kwargs) chat_history.append( ChatMessage( role="tool", blocks=tool_result.blocks, additional_kwargs={"tool_call_id": tool_call.tool_id}, ) )

resp = llm.chat_with_tools([search_tool], chat_history=chat_history) chat_history.append(resp.message) tool_calls = llm.get_tool_calls_from_response( resp, error_on_no_tool_call=False )

print(resp.message.content) print("----" * 20) for block in resp.message.blocks: if isinstance(block, CitationBlock): print("Source: ", block.source) print("Title: ", block.title) print("Cited Content:\n", block.cited_content.text) print("----" * 20) ```

``` Based on the search results, I can explain how LlamaIndex and LLMs work together:

[Column 1]
Here's how LlamaIndex and LLMs work together:
## Data Integration
LlamaIndex offers data connectors to ingest your existing data sources and data formats (APIs, PDFs, docs, SQL, etc.) , allowing you to bring your private data into a format that LLMs can work with.
## Data Structuring
LlamaIndex provides ways to structure your data (indices, graphs) so that this data can be easily used with LLMs . This structuring is crucial for making your data accessible and searchable by the LLM.
## Enhanced Querying
LlamaIndex provides an advanced retrieval/query interface over your data: Feed in any LLM input prompt, get back retrieved context and knowledge-augmented output . This means when you ask the LLM a question, LlamaIndex retrieves relevant information from your data and provides it as context to enhance the LLM's response.
## Application Integration
LlamaIndex allows easy integrations with your outer application framework (e.g. with LangChain, Flask, Docker, ChatGPT, anything else) , making it flexible to incorporate into existing systems.
The framework is designed to be accessible to users at different levels: LlamaIndex's high-level API allows beginner users to use LlamaIndex to ingest and query their data in 5 lines of code, while -------------------------------------------------------------------------------- Source: https://docs.llamaindex.ai Title: Facts about LLMs and LlamaIndex Cited Content:

Context LLMs are a phenomenal piece of technology for knowledge generation and reasoning. They are pre-trained on large amounts of publicly available data. How do we best augment LLMs with our own private data? We need a comprehensive toolkit to help perform this data augmentation for LLMs.

Proposed Solution That's where LlamaIndex comes in. LlamaIndex is a "data framework" to help you build LLM apps. It provides the following tools:
Offers data connectors to ingest your existing data sources and data formats (APIs, PDFs, docs, SQL, etc.) Provides ways to structure your data (indices, graphs) so that this data can be easily used with LLMs. Provides an advanced retrieval/query interface over your data: Feed in any LLM input prompt, get back retrieved context and knowledge-augmented output. Allows easy integrations with your outer application framework (e.g. with LangChain, Flask, Docker, ChatGPT, anything else). LlamaIndex provides tools for both beginner users and advanced users. Our high-level API allows beginner users to use LlamaIndex to ingest and query their data in 5 lines of code. Our lower-level APIs allow advanced users to customize and extend any module (data connectors, indices, retrievers, query engines, reranking modules), to fit their needs.

-------------------------------------------------------------------------------- ```

[Column 2]
LlamaIndex is a "data framework" to help you build LLM apps . The integration works by addressing a key challenge: while LLMs are a phenomenal piece of technology for knowledge generation and reasoning and are pre-trained on large amounts of publicly available data, we need a comprehensive toolkit to help perform data augmentation for LLMs with our own private data .
