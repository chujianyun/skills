# developers.llamaindex.ai/python/framework/integrations/llm/openrouter/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/openrouter/index.md

--- title: OpenRouter | Developer Documentation ---
OpenRouter provides a standardized API to access many LLMs at the best price offered. You can find out more on their homepage [1].
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-llms-openrouter ```
``` !pip install llama-index ```
``` from llama_index.llms.openrouter import OpenRouter from llama_index.core.llms import ChatMessage ```
## Call `chat` with ChatMessage List
You need to either set env var `OPENROUTER_API_KEY` or set api\_key in the class constructor
``` # import os # os.environ['OPENROUTER_API_KEY'] = '<your-api-key>'
llm = OpenRouter( api_key="<API_KEY>", max_tokens=256, context_window=4096, model="gryphe/mythomax-l2-13b", ) ```

``` message = ChatMessage(role="user", content="Tell me a joke") resp = llm.chat([message]) print(resp) ```
``` assistant: Why did the tomato turn red? Because it saw the salad dressing! ```
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
``` # View options at https://openrouter.ai/models # This example uses Mistral's MoE, Mixtral: llm = OpenRouter(model="mistralai/mixtral-8x7b-instruct") ```
``` resp = llm.complete("Write a story about a dragon who can code in Rust") print(resp) ```

[1] https://openrouter.ai