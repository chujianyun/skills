# developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/sambanovasystems/index.md

--- title: SambaNova Systems | Developer Documentation ---
In this notebook you will know how to install, setup and use the SambaNova Cloud [1] and SambaStudio [2] platforms. Take a look and try it yourself!
# SambaNova Cloud
SambaNova Cloud [1] is a high-performance inference service that delivers rapid and precise results. Customers can seamlessly leverage SambaNova technology to enhance their user experience by integrating FastAPI inference APIs with their applications. This service provides an easy-to-use REST interface for streaming the inference results. Users are able to customize the inference parameters and pass the ML model on to the service.
To access SambaNova Cloud model you will need to create a SambaNovaCloud [3] account, get an API key, install the `llama-index-llms-sambanova` integration package, and install the `SSEClient` Package.
``` %pip install llama-index-llms-sambanovasystems %pip install sseclient-py ```

Get an API Key from cloud.sambanova.ai [3] and add it to your environment variables:
``` export SAMBANOVA_API_KEY="<API_KEY>" ```
If you don’t have it in your env variables, you can also add it in the pop-up input text.

if not os.getenv("SAMBANOVA_API_KEY"): os.environ["SAMBANOVA_API_KEY"] = getpass.getpass( "Enter your SambaNova Cloud API key: " ) ```

``` from llama_index.llms.sambanovasystems import SambaNovaCloud
llm = SambaNovaCloud( model="Meta-Llama-3.1-70B-Instruct", context_window=100000, max_tokens=1024, temperature=0.7, top_k=1, top_p=0.01, ) ```

# SambaStudio
SambaStudio [2] is a rich, GUI-based platform that provides the functionality to train, deploy, and manage models.
## Setup
To access SambaStudio models you will need to be a **SambaNova customer**, deploy an endpoint using the GUI or CLI, and use the URL and API Key to connect to the endpoint, as described in the SambaStudio endpoint documentation [4]. Then, install the `llama-index-llms-sambanova` integration package, and install the `SSEClient` Package.
``` %pip install llama-index-llms-sambanova %pip install sseclient-py ```

### Credentials
An endpoint must be deployed in SambaStudio to get the URL and API Key. Once they’re available, include them to your environment variables:
Terminal window
``` export SAMBASTUDIO_URL="your-url-here" export SAMBASTUDIO_API_KEY="<API_KEY>" ```

``` import getpass import os

if not os.getenv("SAMBASTUDIO_URL"): os.environ["SAMBASTUDIO_URL"] = getpass.getpass( "Enter your SambaStudio endpoint's URL: " )

if not os.getenv("SAMBASTUDIO_API_KEY"): os.environ["SAMBASTUDIO_API_KEY"] = getpass.getpass( "Enter your SambaStudio endpoint's API key: " ) ```

## Instantiation
Now we can instantiate our model object and generate chat completions:
``` from llama_index.llms.sambanovasystems import SambaStudio
llm = SambaStudio( model="Meta-Llama-3-70B-Instruct-4096", context_window=100000, max_tokens=1024, temperature=0.7, top_k=1, top_p=0.01, ) ```

## Invocation
Given the following system and user messages, let’s explore different ways of calling a SambaNova Cloud model.
``` from llama_index.core.base.llms.types import ( ChatMessage, MessageRole, )

system_msg = ChatMessage( role=MessageRole.SYSTEM, content="You are a helpful assistant that translates English to French. Translate the user sentence.", ) user_msg = ChatMessage(role=MessageRole.USER, content="I love programming.")

messages = [ system_msg, user_msg, ] ```

``` ai_msg = llm.chat(messages) ai_msg.message ```

``` ai_msg = llm.complete(user_msg.content) ai_msg ```

## Streaming
``` ai_stream_msgs = [] for stream in llm.stream_chat(messages): ai_stream_msgs.append(stream) ai_stream_msgs ```

``` ai_stream_msgs = [] for stream in llm.stream_complete(user_msg.content): ai_stream_msgs.append(stream) ai_stream_msgs ```

``` print(ai_stream_msgs[-1]) ```
## Async
### Chat
``` ai_msg = await llm.achat(messages) ai_msg ```

``` print(ai_msg.message.content) ```
### Complete
``` ai_msg = await llm.acomplete(user_msg.content) ai_msg ```

``` print(ai_msg.text) ```
## Async Streaming
Not supported yet. Coming soon!

[1] https://cloud.sambanova.ai/
[2] https://docs.sambanova.ai/sambastudio/latest/sambastudio-intro.html
[3] https://cloud.sambanova.ai/apis
[4] https://docs.sambanova.ai/sambastudio/latest/endpoints.html#_endpoint_api_keys