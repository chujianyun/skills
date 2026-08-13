# developers.llamaindex.ai/python/framework/integrations/llm/cerebras/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/cerebras/index.md

--- title: Cerebras | Developer Documentation ---

At Cerebras, we’ve developed the world’s largest and fastest AI processor, the Wafer-Scale Engine-3 (WSE-3). The Cerebras CS-3 system, powered by the WSE-3, represents a new class of AI supercomputer that sets the standard for generative AI training and inference with unparalleled performance and scalability.
With Cerebras as your inference provider, you can:
- Achieve unprecedented speed for AI inference workloads - Build commercially with high throughput - Effortlessly scale your AI workloads with our seamless clustering technology
Our CS-3 systems can be quickly and easily clustered to create the largest AI supercomputers in the world, making it simple to place and run the largest models. Leading corporations, research institutions, and governments are already using Cerebras solutions to develop proprietary models and train popular open-source models.
Want to experience the power of Cerebras? Check out our website [1] for more resources and explore options for accessing our technology through the Cerebras Cloud or on-premise deployments!
For more information about Cerebras Cloud, visit cloud.cerebras.ai [2]. Our API reference is available at inference-docs.cerebras.ai [3].
## Setup
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` % pip install llama-index-llms-cerebras ```
``` !pip install llama-index ```
``` from llama_index.llms.cerebras import Cerebras ```
Get an API Key from cloud.cerebras.ai [2] and add it to your environment variables:
Terminal window
``` export CEREBRAS_API_KEY=<your api key> ```
Alternatively, you can pass your API key to the LLM when you init it:
``` import os import getpass

os.environ["CEREBRAS_API_KEY"] = getpass.getpass( "Enter your Cerebras API key: " )

llm = Cerebras(model="llama-3.3-70b", api_key=os.environ["CEREBRAS_API_KEY"]) ```
``` Enter your Cerebras API key: ········ ```
A list of available LLM models can be found at inference-docs.cerebras.ai [3].
``` response = llm.complete("What is Generative AI?") ```
``` print(response) ```

#### Call `chat` with a list of messages

messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="What is your name"), ] resp = llm.chat(messages) ```

``` print(resp) ```
``` assistant: Arrrr, me hearty! Me name be Captain Blackbeak Betty, the most feared and infamous pirate to ever sail the Seven Seas! Me and me trusty parrot, Polly, have been plunderin' and pillagin' for nigh on 20 years, and me reputation be known from the Caribbean to the coast of Africa!

[Column 1]
### Streaming
Using `stream_complete` endpoint
``` response = llm.stream_complete("What is Generative AI?") ```
``` for r in response: print(r.delta, end="") ```

Generative AI has many potential applications, including:

Some examples of generative AI include:
1. Language models like GPT-3, which can generate human-like text based on a prompt. 2. Image generation models like Generative Adversarial Networks (GANs), which can generate realistic images of faces, objects, or scenes. 3. Music generation models like Amper Music, which can generate original music tracks based on a set of parameters. 4. Video generation models like DeepMotion, which can generate realistic videos of human movements and actions.
Overall, generative AI has the potential to revolutionize the way we create and interact with content, and has many exciting applications across various industries. ```
Using `stream_chat` endpoint
``` from llama_index.core.llms import ChatMessage
messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="What is your name"), ] resp = llm.stream_chat(messages) ```

``` for r in resp: print(r.delta, end="") ```
``` Arrrr, me hearty! Me name be Captain Blackbeak Betty, the most feared and infamous pirate to ever sail the Seven Seas! Me and me trusty parrot, Polly, have been plunderin' and pillagin' for nigh on 20 years, and me reputation be known from the Caribbean to the coast of Africa!
Now, I be a bit of a legend in me own right, with me black beard and me eye patch, and me ship, the "Maverick's Revenge", be the fastest and most feared on the high seas! So, if ye be lookin' for a swashbucklin' adventure, just give ol' Blackbeak Betty a shout, and we'll set sail fer a life o' plunder and pillage! Savvy? ```

[Column 2]
``` Generative AI refers to a type of artificial intelligence (AI) that is capable of generating new, original content, such as text, images, music, or videos, based on patterns and structures it has learned from a dataset or a set of examples. This type of AI is designed to create new content that is similar in style, tone, and quality to the original content it was trained on.
Generative AI models use various techniques, such as neural networks, to analyze and learn from large datasets, and then generate new content that is similar to the patterns and structures they have learned. These models can be trained on a wide range of data, including text, images, audio, and video, and can be used to generate a variety of content, such as:
1. Text: Generative AI models can generate text that is similar in style and tone to a given text, such as articles, blog posts, or social media updates. 2. Images: Generative AI models can generate images that are similar in style and content to a given image, such as photographs, illustrations, or graphics. 3. Music: Generative AI models can generate music that is similar in style and tone to a given piece of music, such as melodies, harmonies, or beats. 4. Videos: Generative AI models can generate videos that are similar in style and content to a given video, such as animations, movies, or TV shows.

1. Content creation: Generative AI can be used to generate content for various industries, such as marketing, advertising, and entertainment. 2. Data augmentation: Generative AI can be used to generate new data that can be used to train and improve machine learning models. 3. Creative collaboration: Generative AI can be used to collaborate with humans in the creative process, such as generating ideas or providing inspiration. 4. Personalization: Generative AI can be used to generate personalized content for individuals, such as customized recommendations or tailored marketing messages.


[1] https://cerebras.net
[2] https://cloud.cerebras.ai/
[3] https://inference-docs.cerebras.ai/