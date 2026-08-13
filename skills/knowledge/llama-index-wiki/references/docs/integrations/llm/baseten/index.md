# developers.llamaindex.ai/python/framework/integrations/llm/baseten/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/baseten/index.md

[Column 1]
--- title: Baseten Cookbook | Developer Documentation ---
``` %pip install llama-index llama-index-llms-baseten ```
``` from llama_index.llms.baseten import Baseten ```
## Model APIs vs. Dedicated Deployments
Baseten offers two main ways for inference.

#### Instantiation

#### Call `complete` with a prompt
``` llm_response = llm.complete("Paul Graham is") print(llm_response.text) ```

#### Call `chat` with a list of messages

[Column 2]
1. Model APIs are public endpoints for popular open source models (GPT-OSS, Kimi K2, DeepSeek etc) where you can directly use a frontier model via slug e.g. `deepseek-ai/DeepSeek-V3-0324` and you will be charged on a per- token basis. You can find the list of supported models here: <https://docs.baseten.co/development/model-apis/overview#supported-models>.
2. Dedicated deployments are useful for serving custom models where you want to autoscale production workloads and have fine-grain configuration. You need to deploy a model in your Baseten dashboard and provide the 8 character model id like `abcd1234`.
By default, we set the `model_apis` parameter to `True`. If you want to use a dedicated deployment, you must set the `model_apis` parameter to `False` when instantiating the Baseten object.
``` # Model APIs, you can find the model_slug here: https://docs.baseten.co/development/model-apis/overview#supported-models llm = Baseten( model_id="MODEL_SLUG", api_key="<API_KEY>", model_apis=True, # Default, so not strictly necessary )

# Dedicated Deployments, you can find the model_id by in the Baseten dashboard here: https://app.baseten.co/overview llm = Baseten( model_id="MODEL_ID", api_key="<API_KEY>", model_apis=False, ) ```

``` Paul Graham is a British-American entrepreneur, essayist, and programmer, best known for co-founding the startup accelerator **Y Combinator (YC)** and for his influential essays on technology, startups, and philosophy. Here are some key highlights about him:
### **Background & Career** - Born in 1964 in England, Graham studied at **Cornell University** and earned a PhD in **Computer Science** from **Harvard**. - He created **Viaweb** (1995), the first web-based application, which was later acquired by Yahoo! in 1998 and became **Yahoo! Store**. - Co-founded **Y Combinator (2005)** with Jessica Livingston, Robert Morris, and Trevor Blackwell. YC has funded companies like **Airbnb, Dropbox, Stripe, Reddit, and DoorDash**.
### **Writing & Influence** - Known for his **essays** on startups, technology, and life philosophy (hosted on his website paulgraham.com [1]). - Popular essays include: - *"How to Start a Startup"* - *"Do Things That Don't Scale"* - *"The Hardest Lessons for Start ```


[Column 1]
messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="What is your name"), ] resp = llm.chat(messages) ```

``` print(resp) ```

## Streaming
Using `stream_complete` endpoint
``` resp = llm.stream_complete("Paul Graham is ") ```

[Column 2]
``` assistant: Arrr, matey! I be known as Captain Crimsonbeard—though me beard be more fiery red than crimson, truth be told! A pirate of legend, scourge of the seven memes, and connoisseur of questionable life choices. But ye can call me Cap’n if ye like, or "That Weird Pirate Who Won’t Stop Talking About Pineapples." Now, what mischief brings ye to me ship today? 🏴☠️🍍 ```


[Column 1]
Using `stream_chat` endpoint
``` from llama_index.core.llms import ChatMessage
messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="What is your name"), ] resp = llm.stream_chat(messages) ```

``` for r in resp: print(r.delta, end="") ```

What be yer name, matey? Or shall I just call ye "Lucky Crewmember" for now? *winks and adjusts my feathered hat* ```
# Async
Async operations are used for long-running inference tasks that may hit request timeouts, batch inference jobs, and prioritizing certain requests.
(1) In the integation, `acomplete` async function is implemented using the aiohttp library, an asynchronous HTTP client in python. The function invokes the async\_predict at the approriate Baseten model endpoint, then the user receives a response with the request\_id if successful. The user can then check the status or cancel the async\_predict request using the returned request\_id.
(2) Once the model finishes executing the request, the async result will be posted to the user provided webhook endpoint. The user’s endpoint is responsible for validating the webhook signature for security, then processing and storing the output.
Baseten: Get request\_id → result is posted to webhook
##### Note: Async is only available for dedicated deployments and not for model APIs. `achat` is not supported because chat does not make sense for async operations.
``` async_llm = Baseten( model_id="YOUR_MODEL_ID", api_key="<API_KEY>", webhook_endpoint="YOUR_WEBHOOK_ENDPOINT", ) response = await async_llm.acomplete("Paul Graham is") print(response) # This is the request id ```

``` 35643965636d4c3da6f54b5c3b354aa0 ```
``` """ This will return the status information of a request using an async_predict request's request_id and the model_id the async_predict request was made with. """

import requests import os
model_id = "YOUR_MODEL_ID" request_id = "YOUR_REQUEST_ID" # Read secrets from environment variables baseten_api_key = "<API_KEY>"

resp = requests.get( f"https://model-{model_id}.api.baseten.co/async_request/{request_id}", headers={"Authorization": f"Api-Key {baseten_api_key}"}, )

print(resp.json()) ```
``` {'request_id': '35643965636d4c3da6f54b5c3b354aa0', 'model_id': 'yqvr2lxw', 'deployment_id': '31kmg1w', 'status': 'SUCCEEDED', 'webhook_status': 'SUCCEEDED', 'created_at': '2025-03-27T00:17:51.578558Z', 'status_at': '2025- 03-27T00:18:38.768572Z', 'errors': []} ```

[Column 2]
``` Paul Graham is a British-American entrepreneur, essayist, and venture capitalist, best known as a co-founder of **Y Combinator**, a highly influential startup accelerator that has helped launch companies like Airbnb, Dropbox, Stripe, and Reddit.
### Key Facts About Paul Graham: 1. **Early Career**: Originally a programmer, he developed **Viaweb**, one of the first web-based applications, which was acquired by Yahoo! in 1998 and became Yahoo! Store. 2. **Y Combinator**: In 2005, he co-founded Y Combinator with Jessica Livingston, Robert Morris, and Trevor Blackwell. It pioneered the "seed accelerator" model, providing funding and mentorship to early-stage startups. 3. **Essays**: Graham is known for his insightful essays on startups, technology, and life philosophy, available on his website (paulgraham.com [1]). Popular ones include *"How to Get Startup Ideas"* and *"Do Things That Don't Scale."* 4. **Investments**: Through YC, he has backed thousands of startups, shaping Silicon Valley’s tech landscape. 5. **Lisp Advocate**: A proponent of the Lisp programming language, ```

``` Arrr, me name be Captain Crimsonbeard! A fearsome and flamboyant pirate with a beard as red as the setting sun and a wardrobe brighter than a treasure chest full o’ jewels! I sail the seven seas in search of adventure, gold, and the finest rum—always with a dramatic flair and a twinkle in me eye.


[1] http://www.paulgraham.com