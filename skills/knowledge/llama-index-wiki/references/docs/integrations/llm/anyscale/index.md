# developers.llamaindex.ai/python/framework/integrations/llm/anyscale/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/anyscale/index.md

--- title: Anyscale | Developer Documentation ---

If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-llms-anyscale ```
``` !pip install llama-index ```
``` from llama_index.llms.anyscale import Anyscale from llama_index.core.llms import ChatMessage ```

## Call `chat` with ChatMessage List
You need to either set env var `ANYSCALE_API_KEY` or set api\_key in the class constructor
``` # import os # os.environ['ANYSCALE_API_KEY'] = '<your-api-key>'

llm = Anyscale(api_key="<API_KEY>") ```
``` message = ChatMessage(role="user", content="Tell me a joke") resp = llm.chat([message]) print(resp) ```

``` assistant: Sure, here's a joke for you:

I hope that brought a smile to your face! Is there anything else I can assist you with? ```
### Streaming
``` message = ChatMessage(role="user", content="Tell me a story in 250 words") resp = llm.stream_chat([message]) for r in resp: print(r.delta, end="") ```

``` Once upon a time, there was a young girl named Maria who lived in a small village surrounded by lush green forests. Maria was a kind and gentle soul, loved by everyone in the village. She spent most of her days exploring the forests, discovering new species of plants and animals, and helping the villagers with their daily chores.
One day, while Maria was out on a walk, she stumbled upon a hidden path she had never seen before. The path was overgrown with weeds and vines, but something about it called to her. She decided to follow it, and it led her deeper and deeper into the forest.
As she walked, the trees grew taller and the air grew colder. Maria began to feel a sense of unease, but she was determined to see where the path led. Finally, she came to a clearing, and in the center of it stood an enormous tree, its trunk as wide as a house.
Maria approached the tree and saw that it was covered in strange symbols. She reached out to touch one of the symbols, and suddenly, the tree began to glow. The glow grew brighter and brighter, until Maria ```
## Call `complete` with Prompt
``` resp = llm.complete("Tell me a joke") print(resp) ```
``` Sure, here's a joke for you:
Why couldn't the bicycle stand up by itself?
Because it was two-tired!
I hope that brought a smile to your face! ```
``` resp = llm.stream_complete("Tell me a story in 250 words") for r in resp: print(r.delta, end="") ```
``` Once upon a time, there was a young girl named Maria. She lived in a small village surrounded by lush green forests and sparkling rivers. Maria was a kind and gentle soul, loved by everyone in the village. She spent her days helping her parents with their farm work and exploring the surrounding nature.
One day, while wandering in the forest, Maria stumbled upon a hidden path she had never seen before. She decided to follow it, and it led her to a beautiful meadow filled with wildflowers. In the center of the meadow, she found a small pond, where she saw her own reflection in the water.
As she gazed into the pond, Maria saw a figure approaching her. It was a wise old woman, who introduced herself as the guardian of the meadow. The old woman told Maria that she had been chosen to receive a special gift, one that would bring her great joy and happiness.
The old woman then presented Maria with a small, delicate flower. She told her that this flower had the power to heal any wound, both physical and emotional. Maria was amazed and grateful, and she promised to use the flower wisely. ```
## Model Configuration
``` llm = Anyscale(model="codellama/CodeLlama-34b-Instruct-hf") ```
``` resp = llm.complete("Show me the c++ code to send requests to HTTP Server") print(resp) ```
```` To send requests to an HTTP server in C++, you can use the `curl` library. Here's an example of how to use it: ``` #include <curl/curl.h>
int main() { CURL *curl; CURLcode res; curl = curl_easy_init(); if (curl) { curl_easy_setopt(curl, CURLOPT_URL, "http://example.com"); curl_easy_setopt(curl, CURLOPT_POSTFIELDS, "name=John&age=25"); res = curl_easy_perform(curl); if (res != CURLE_OK) { fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res)); } curl_easy_cleanup(curl); } return 0; } ``` This code initializes the `curl` library, sets the URL and POST fields, performs the request, and cleans up the resources.

You can also use the `libcurl` library ````