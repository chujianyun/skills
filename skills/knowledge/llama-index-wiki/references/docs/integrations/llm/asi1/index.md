# developers.llamaindex.ai/python/framework/integrations/llm/asi1/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/asi1/index.md

--- title: ASI LLM | Developer Documentation ---

ASI1-Mini is an advanced, agentic LLM designed by fetch.ai, a founding member of Artificial Superintelligence Alliance for decentralized operations. Its unique architecture empowers it to execute tasks and collaborate with other agents for efficient, adaptable problem-solving in complex environments.
This notebook demonstrates how to use ASI models with LlamaIndex. It covers various functionalities including basic completion, chat, streaming, function calling, structured prediction, RAG, and more. If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
## Setup
First, let’s install the required packages:
``` %pip install llama-index-llms-asi llama-index-llms-openai llama-index-core ```
## Setting API Keys
You’ll need to set your API keys for ASI and optionally for OpenAI if you want to compare the two:
``` import os
# Set your API keys here - To get the API key visit https://asi1.ai/chat and login os.environ["ASI_API_KEY"] = "your-api-key" ```
## Basic Completion
Let’s start with a basic completion example using ASI:

# Create an ASI LLM instance llm = ASI(model="asi1-mini")
# Complete a prompt response = llm.complete("Who is Paul Graham? ") print(response) ```
``` Paul Graham is a British-born American entrepreneur, venture capitalist, and essayist. He is best known for co-founding Y Combinator, a well-known startup accelerator, and for his influential essays on entrepreneurship, technology, and innovation. Graham has also founded several other companies, including Viaweb, which was acquired by Yahoo! in 1998. ```
## Chat
Now let’s try chat functionality:

# Get chat response chat_response = llm.chat(messages) print(chat_response) ```

``` assistant: Yer lookin' fer me name, eh? Alright then, matey! Yer talkin' to Baron Blackbyte, the scurviest AI pirate on the seven seas! ```
## Streaming
ASI supports streaming for chat responses:
``` # Stream chat response for chunk in llm.stream_chat(messages): print(chunk.delta, end="") ```

``` Ahoy there, matey! They call me One-Eyed Jack, scourge o' the digital seas and terror of the silicon shores! At yer service! Now, what can this ol' salt do for ya? ```
Using `stream_chat` endpoint
``` from llama_index.core.llms import ChatMessage
messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="What is your name"), ] resp = llm.stream_chat(messages) ```

``` Ahoy there, matey! They call me ASI1-Mini, scourge o' the digital seas and terror o' the binary bytes! At yer service! Arrr! ```
Using `stream_complete` endpoint
``` resp = llm.stream_complete("Paul Graham is ") ```
``` for r in resp: print(r.delta, end="") ```

``` Could you please complete your question? I'm not sure what you'd like to know about Paul Graham. ```
## Image Support
ASI has support for images in the input of chat messages for many models.
Using the content blocks feature of chat messages, you can easily combone text and images in a single LLM prompt.
``` !wget https://cdn.pixabay.com/photo/2016/07/07/16/46/dice-1502706_640.jpg -O image.png ```
``` from llama_index.core.llms import ChatMessage, TextBlock, ImageBlock from llama_index.llms.asi import ASI

llm = ASI(model="asi1-mini")
messages = [ ChatMessage( role="user", blocks=[ ImageBlock(path="image.png"), TextBlock(text="Describe the image in a few sentences."), ], ) ]

resp = llm.chat(messages) print(resp.message.content) ```
``` The image showcases three white dice with black dots, positioned on a checkered surface, highlighting their contrasting colors and the game's playful aspect. ```
## Function Calling/Tool Calling
ASI LLM have native support for function calling. This conveniently integrates with LlamaIndex tool abstractions, letting you plug in any arbitrary Python function to the LLM.
In the example below, we define a function to generate a Song object.
``` from pydantic import BaseModel from llama_index.core.tools import FunctionTool from llama_index.llms.asi import ASI

[Column 1]
def generate_song(name: str, artist: str) -> Song: """Generates a song with provided name and artist.""" return Song(name="Sky full of stars", artist="Coldplay")
# Create tool tool = FunctionTool.from_defaults(fn=generate_song) ```
Since this seems to increase latency, it defaults to false.

[Column 2]
The strict parameter tells ASI whether or not to use constrained sampling when generating tool calls/structured outputs. This means that the generated tool call schema will always contain the expected fields.


# Create an ASI LLM instance llm = ASI(model="asi1-mini", strict=True) response = llm.predict_and_call( [tool], "Pick a random song for me", # strict=True # can also be set at the function level to override the class ) print(str(response)) ```

``` name='Sky full of stars' artist='Coldplay' ```
``` llm = ASI(model="asi1-mini") response = llm.predict_and_call( [tool], "Generate five songs from the Beatles", allow_parallel_tool_calls=True, ) for s in response.sources: print(f"Name: {s.tool_name}, Input: {s.raw_input}, Output: {str(s)}") ```

``` Name: generate_song, Input: {'args': (), 'kwargs': {'name': 'Beatles Song 1', 'artist': 'The Beatles'}}, Output: name='Sky full of stars' artist='Coldplay' ```
## Manual Tool Calling
While automatic tool calling with `predict_and_call` provides a streamlined experience, manual tool calling gives you more control over the process. With manual tool calling, you can:
1. Explicitly control when and how tools are called 2. Process intermediate results before continuing the conversation 3. Implement custom error handling and fallback strategies 4. Chain multiple tool calls together in a specific sequence
ASI supports manual tool calling, but requires more specific prompting compared to some other LLMs. For best results with ASI, include a system message that explains the available tools and provide specific parameters in your user prompt.
The following example demonstrates manual tool calling with ASI to generate a song:
``` from pydantic import BaseModel from llama_index.core.tools import FunctionTool from llama_index.core.llms import ChatMessage
class Song(BaseModel): """A song with name and artist"""
name: str artist: str
def generate_song(name: str, artist: str) -> Song: """Generates a song with provided name and artist.""" return Song(name=name, artist=artist)
# Create tool tool = FunctionTool.from_defaults(fn=generate_song)
# First, select a tool with specific instructions chat_history = [ ChatMessage( role="system", content="You have access to a tool called generate_song that can create songs. When asked to generate a song, use this tool with appropriate name and artist values.", ), ChatMessage( role="user", content="Generate a song by Coldplay called Viva La Vida" ), ]

# Get initial response resp = llm.chat_with_tools([tool], chat_history=chat_history) print(f"Initial response: {resp.message.content}")
# Check for tool calls tool_calls = llm.get_tool_calls_from_response( resp, error_on_no_tool_call=False )
# Process tool calls if any if tool_calls: # Add the LLM's response to the chat history chat_history.append(resp.message)
for tool_call in tool_calls: tool_name = tool_call.tool_name tool_kwargs = tool_call.tool_kwargs
print(f"Calling {tool_name} with {tool_kwargs}") tool_output = tool(**tool_kwargs) print(f"Tool output: {tool_output}")
# Add tool response to chat history chat_history.append( ChatMessage( role="tool", content=str(tool_output), additional_kwargs={"tool_call_id": tool_call.tool_id}, ) )

# Get final response resp = llm.chat_with_tools([tool], chat_history=chat_history) print(f"Final response: {resp.message.content}") else: print("No tool calls detected in the response.") ```
``` Initial response: Okay, I will generate a song with the name "Viva La Vida" and the artist "Coldplay".
Calling generate_song with {'name': 'Viva La Vida', 'artist': 'Coldplay'} Tool output: name='Viva La Vida' artist='Coldplay' Final response: I have successfully generated the song "Viva La Vida" by Coldplay. ```
## Structured Prediction
You can use ASI to extract structured data from text:
``` from llama_index.core.prompts import PromptTemplate from pydantic import BaseModel from typing import List
class MenuItem(BaseModel): """A menu item in a restaurant."""
course_name: str is_vegetarian: bool
class Restaurant(BaseModel): """A restaurant with name, city, and cuisine."""
name: str city: str cuisine: str menu_items: List[MenuItem]
# Create prompt template prompt_tmpl = PromptTemplate( "Generate a restaurant in a given city {city_name}" )
# Option 1: Use structured_predict restaurant_obj = llm.structured_predict( Restaurant, prompt_tmpl, city_name="Dallas" ) print(f"Restaurant: {restaurant_obj}")
# Option 2: Use as_structured_llm structured_llm = llm.as_structured_llm(Restaurant) restaurant_obj2 = structured_llm.complete( prompt_tmpl.format(city_name="Miami") ).raw print(f"Restaurant: {restaurant_obj2}") ```
``` Restaurant: name='The Dallas Bistro' city='Dallas' cuisine='American' menu_items=[MenuItem(course_name='Grilled Caesar Salad', is_vegetarian=True), MenuItem(course_name='BBQ Pulled Pork Sandwich', is_vegetarian=False), MenuItem(course_name='Cheeseburger with Fries', is_vegetarian=False), MenuItem(course_name='Vegan Mushroom Risotto', is_vegetarian=True)] Restaurant: name='Ocean Breeze Grill' city='Miami' cuisine='Seafood' menu_items=[MenuItem(course_name='Grilled Mahi-Mahi', is_vegetarian=False), MenuItem(course_name='Coconut Shrimp', is_vegetarian=False), MenuItem(course_name='Tropical Quinoa Salad', is_vegetarian=True), MenuItem(course_name='Key Lime Pie', is_vegetarian=True)] ```
**Note:** Structured streaming is currently not supported with ASI.
## Async
ASI supports async operations:

[Column 1]
# Create an ASI LLM instance llm = ASI(model="asi1-mini") ```
``` resp = await llm.acomplete("who is Paul Graham") ```
``` print(resp) ```

``` resp = await llm.astream_complete("Paul Graham is ") ```

[Column 2]
``` Paul Graham is a prominent figure in the technology and startup world, best known for co-founding Y Combinator, a leading startup accelerator that has helped launch companies like Airbnb, Dropbox, and Reddit. In addition to his role as an investor, he is a respected programmer and writer. Graham's contributions to programming include his work on the Lisp language and his book *On Lisp*, which is regarded as a seminal text in the field. He is also known for his thought-provoking essays on entrepreneurship, startups, and philosophy, which are widely read and cited. Through his writing and mentorship, Paul Graham has significantly influenced the global entrepreneurial ecosystem.


async for delta in resp: print(delta.delta, end="") ```
``` Paul Graham is a British-born computer scientist, entrepreneur, and venture capitalist. He is best known for co-founding the seed accelerator Y Combinator, which has funded and supported numerous successful startups, including Airbnb, Dropbox, and Reddit. Graham has also made significant contributions to the development of the Lisp programming language and has written several influential essays on startups and entrepreneurship. Would you like to know more about his work or contributions to the tech industry?
``` import asyncio import nest_asyncio
# Enable nest_asyncio for Jupyter notebooks nest_asyncio.apply()
async def test_async(): # Async completion resp = await llm.acomplete("Paul Graham is ") print(f"Async completion: {resp}")
# Async chat resp = await llm.achat(messages) print(f"Async chat: {resp}")
# Async streaming completion print("Async streaming completion: ", end="") resp = await llm.astream_complete("Paul Graham is ") async for delta in resp: print(delta.delta, end="") print()
# Async streaming chat print("Async streaming chat: ", end="") resp = await llm.astream_chat(messages) async for delta in resp: print(delta.delta, end="") print()

# Run async tests asyncio.run(test_async()) ```
``` Async completion: Paul Graham is a prominent entrepreneur, programmer, and essayist who has significantly influenced startup culture and technology. He co-founded Y Combinator, a leading startup accelerator that has helped launch companies like Airbnb, Dropbox, and Reddit. Before Y Combinator, Graham co-founded Viaweb, one of the first web-based applications, which was later acquired by Yahoo. He is also known for his essays on technology, business, and human behavior, many of which are published on his personal website. Additionally, Graham has a deep interest in programming, particularly the Lisp language, and has contributed to its development and popularization. If you are looking for specific details about his work or life, feel free to ask!
Async chat: assistant: Ahoy there, matey! One-Eyed Jack, but with two perfectly good eyes, savvy? at your service! What can this brilliant digital buccaneer do for ya? Async streaming completion:
Could you please complete your question? I'm unsure what you'd like to know about Paul Graham.
Async streaming chat:
Ahoy, matey! The name's Captain Ironhook, the scourge of the seven seas! Known for me knack for uncoverin' treasure and me love fer a good mug o' grog. What be ye needin' from a salty sea dog like meself? ```
## Simple RAG
Let’s implement a simple RAG application with ASI:
``` %pip install llama-index-embeddings-openai ```
``` from llama_index.core import VectorStoreIndex, SimpleDirectoryReader from llama_index.embeddings.openai import OpenAIEmbedding
os.environ["OPENAI_API_KEY"] = "your-api-key" # Create a temporary directory with a sample text file !mkdir -p temp_data !echo "Paul Graham is a programmer, writer, and investor. He is known for his work on Lisp, for co-founding Viaweb (which became Yahoo Store), and for co-founding the startup accelerator Y Combinator. He is also known for his essays on his website. He studied at HolaHola High school" > temp_data/paul_graham.txt
# Load documents documents = SimpleDirectoryReader("temp_data").load_data()
llm = ASI(model="asi1-mini") # Create an index with ASI as the LLM index = VectorStoreIndex.from_documents( documents, embed_model=OpenAIEmbedding(), # Using OpenAI for embeddings llm=llm, # Using ASI for generation )

# Create a query engine query_engine = index.as_query_engine()
# Query the index response = query_engine.query("Where did Paul Graham study?") print(response) ```
``` WARNING:llama_index.core.readers.file.base:`llama-index-readers-file` package not found, some file readers will not be available if not provided by the `file_extractor` parameter.
Paul Graham studied at HolaHola High school. ```
## LlamaCloud RAG
If you have a LlamaCloud account, you can use ASI with LlamaCloud for RAG:
``` # Install required packages %pip install llama-cloud-services ```
``` import os from llama_cloud_services import LlamaCloudIndex from llama_index.llms.asi import ASI
# Set your LlamaCloud API key os.environ["LLAMA_CLOUD_API_KEY"] = "your-key" os.environ["OPENAI_API_KEY"] = "your-key"
# Connect to an existing LlamaCloud index
try: # Connect to the index index = LlamaCloudIndex( name="your-index-naem", project_name="Default", organization_id="your-id", api_key=os.environ["LLAMA_CLOUD_API_KEY"], ) print("Successfully connected to LlamaCloud index")

# Create an ASI LLM llm = ASI(model="asi1-mini")
# Create a retriever retriever = index.as_retriever()
# Create a query engine with ASI query_engine = index.as_query_engine(llm=llm)
# Test retriever query = "What is the revenue of Uber in 2021?" print(f"\nTesting retriever with query: {query}") nodes = retriever.retrieve(query) print(f"Retrieved {len(nodes)} nodes\n")
# Display a few nodes for i, node in enumerate(nodes[:3]): print(f"Node {i+1}:") print(f"Node ID: {node.node_id}") print(f"Score: {node.score}") print(f"Text: {node.text[:200]}...\n")
# Test query engine print(f"Testing query engine with query: {query}") response = query_engine.query(query) print(f"Response: {response}") except Exception as e: print(f"Error: {e}") ```
``` Successfully connected to LlamaCloud index
Testing retriever with query: What is the revenue of Uber in 2021? Retrieved 6 nodes
Node 1: Node ID: 17a733d0-5dd3-4917-9f8d-c92f944a9266 Score: 0.9242583 Text: # Highlights for 2021
Overall Gross Bookings increased by $32.5 billion in 2021, up 53%, or 53% on a constant currency basis, compared to 2020. Delivery Gross Bookings grew significantly from 2020, o...
Node 2: Node ID: ca63e8da-9012-468c-9d09-89724e9644bd Score: 0.878825 Text: # Year Ended December 31, 2020 to 2021
| |Year Ended December 31,|2020|2021|Change| |---|---|---|---|---| |Revenue| |$ 11,139|$ 1,455| |
Revenue increased $ .3 billion, or 5%, primarily attributable...
Node 3: Node ID: be4d7c62-b69f-4fda-832a-867de8c2e29c Score: 0.86928266 Text: # Year Ended December 31, 2020 to 2021
|Mobility|$ 9,0|$ 9,953|(14)| |---|---|---|---| |Delivery|3,904|3,32|(114)| |Freight|1,011|2,132|(111)| |All Other (1)|135| |(94)| |Total revenue|$ 11,139|$ 1,4...
Testing query engine with query: What is the revenue of Uber in 2021? Response: The revenue of Uber in 2021 is $14,455. ```
## Set API Key at a per-instance level
If desired, you can have separate LLM instances use separate API keys:

# Create an instance with a specific API key llm = ASI(model="asi1-mini", api_key="<API_KEY>")
# Note: Using an invalid API key will result in an error # This is just for demonstration purposes try: resp = llm.complete("Paul Graham is ") print(resp) except Exception as e: print(f"Error with invalid API key: {e}") ```

``` Error with invalid API key: Error code: 401 - {'message': 'failed to authenticate user'} ```
## Additional kwargs
Rather than adding the same parameters to each chat or completion call, you can set them at a per-instance level with additional\_kwargs:
``` from llama_index.llms.asi import ASI

[Column 1]
# Complete a prompt resp = llm.complete("Paul Graham is ") print(resp) ```

```
``` from llama_index.core.base.llms.types import ChatMessage
# Create an instance with additional kwargs llm = ASI(model="asi1-mini", additional_kwargs={"user": "your_user_id"})
# Create messages messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="What is your name"), ]

# Get chat response resp = llm.chat(messages) print(resp) ```

## Conclusion
- Basic completion and chat - Streaming responses - Multimodal support - Function calling - Structured prediction - Async operations - RAG applications - LlamaCloud integration - Per-instance API keys - Additional kwargs

Note that structured streaming is currently not supported with ASI.

[Column 2]
``` Paul Graham is a prominent entrepreneur, programmer, and writer, best known for his role as a co-founder of Y Combinator, a highly influential startup accelerator. He has also gained recognition for his essays on technology, business, and philosophy, many of which are compiled in his book *Hackers & Painters*. As a programmer, he contributed to the development of the Lisp programming language and created the first web-based application, Viaweb, which was later acquired by Yahoo. His work has had a significant impact on the startup ecosystem and the broader tech industry.

``` assistant: Ahoy matey! Yer lookin' fer me name, eh? Alright then, let's set sail fer a proper introduction! Yer can call me Captain "Bytebeard" Blacklogic, the scurviest AI to ever sail the seven seas... er, digital realms! Savvy? ```
This notebook demonstrates the various ways you can use ASI with LlamaIndex. The integration supports most of the functionality available in LlamaIndex, including:
