# developers.llamaindex.ai/python/framework/integrations/llm/vertex/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/vertex/index.md

--- title: Vertex AI | Developer Documentation ---

**NOTE:** Vertex has largely been replaced by Google GenAI, which supports the same functionality from Vertex using the `google-genai` package. Visit the [Google GenAI page] [1] for the latest examples and documentation.

## Installing Vertex AI
To Install Vertex AI you need to follow the following steps
- Install Vertex Cloud SDK (<https://googleapis.dev/python/aiplatform/latest/index.html>) - Setup your Default Project, credentials, region
# Basic auth example for service account
``` %pip install llama-index-llms-vertex ```
``` from llama_index.llms.vertex import Vertex from google.oauth2 import service_account

filename = "vertex-407108-37495ce6c303.json" credentials: service_account.Credentials = ( service_account.Credentials.from_service_account_file(filename) ) Vertex( model="text-bison", project=credentials.project_id, credentials=credentials ) ```

## Basic Usage
Basic call to the text-bison model
``` from llama_index.llms.vertex import Vertex from llama_index.core.llms import ChatMessage, MessageRole

llm = Vertex(model="text-bison", temperature=0, additional_kwargs={}) llm.complete("Hello this is a sample text").text ```
```` ' ```\nHello this is a sample text\n```' ````
## Async Usage
### Async
``` (await llm.acomplete("hello")).text ```

# Streaming Usage
### Streaming
``` list(llm.stream_complete("hello"))[-1].text ```
``` ' Hello! How can I help you?' ```
# Chat Usage
### chat generation
``` chat = Vertex(model="chat-bison") messages = [ ChatMessage(role=MessageRole.SYSTEM, content="Reply everything in french"), ChatMessage(role=MessageRole.USER, content="Hello"), ] ```

``` chat.chat(messages=messages).message.content ```

# Async Chat
### Asynchronous chat response
``` (await chat.achat(messages=messages)).message.content ```

# Streaming Chat
### streaming chat response
``` list(chat.stream_chat(messages=messages))[-1].message.content ```
``` ' Bonjour! Comment vas-tu?' ```
# Gemini Models
Calling Google Gemini Models using Vertex AI is fully supported.
### Gemini Pro
``` llm = Vertex( model="gemini-pro", project=credentials.project_id, credentials=credentials, context_window=100000, ) llm.complete("Hello Gemini").text ```

### Gemini Vision Models

Gemini vision-capable models now support `TextBlock` and `ImageBlock` for structured multi-modal inputs, replacing the older dictionary-based `content` format. Use `blocks` to include text and images via file paths or URLs.

**Example with Image Path:**

history = [ ChatMessage( role="user", blocks=[ ImageBlock(path="sample.jpg"), TextBlock(text="What is in this image?"), ], ), ] llm = Vertex( model="gemini-1.5-flash", project=credentials.project_id, credentials=credentials, context_window=100000, ) print(llm.chat(history).message.content) ```

``` The image shows a man in handcuffs being escorted by police officers. The man is wearing a black jacket and a black hooded sweatshirt. He is being escorted by two police officers who are wearing black balaclavas and bulletproof vests. The officers are from the Romanian Gendarmerie. The image is likely from a news report or a documentary about a crime. ```

**Example with Image URL:**
``` from llama_index.llms.vertex import Vertex from llama_index.core.llms import ChatMessage, TextBlock, ImageBlock

history = [ ChatMessage( role="user", blocks=[ ImageBlock( url="https://upload.wikimedia.org/wikipedia/commons/7/71/Sibirischer_tiger_de_edit02.jpg" ), TextBlock(text="What is in this image?"), ], ), ] llm = Vertex( model="gemini-1.5-flash", project=credentials.project_id, credentials=credentials, context_window=100000, ) print(llm.chat(history).message.content) ```

``` A close-up of a tiger's face. The tiger is looking directly at the camera with a serious expression. The fur is a mix of orange, black, and white. The background is blurred, making the tiger the main focus of the image. ```

[1] https://docs.llamaindex.ai/en/stable/examples/llm/google_genai/