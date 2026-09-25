# developers.llamaindex.ai/python/framework/integrations/llm/groq/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/groq/index.md

--- title: Groq | Developer Documentation ---

Welcome to Groq! 🚀 At Groq, we’ve developed the world’s first Language Processing Unit™, or LPU. The Groq LPU has a deterministic, single core streaming architecture that sets the standard for GenAI inference speed with predictable and repeatable performance for any given workload.
Beyond the architecture, our software is designed to empower developers like you with the tools you need to create innovative, powerful AI applications. With Groq as your engine, you can:
- Achieve uncompromised low latency and performance for real-time AI and HPC inferences 🔥 - Know the exact performance and compute time for any given workload 🔮 - Take advantage of our cutting-edge technology to stay ahead of the competition 💪

Want more Groq? Check out our website [1] for more resources and join our Discord community [2] to connect with our developers!
## Setup
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` % pip install llama-index-llms-groq ```
``` !pip install llama-index ```
``` from llama_index.llms.groq import Groq ```
``` None of PyTorch, TensorFlow >= 2.0, or Flax have been found. Models won't be available and only tokenizers, configuration and file/data utilities can be used. ```
Create an API key at the Groq console [3], then set it to the environment variable `GROQ_API_KEY`.
Terminal window
``` export GROQ_API_KEY=<your api key> ```
Alternatively, you can pass your API key to the LLM when you init it:
``` llm = Groq(model="llama3-70b-8192", api_key="<API_KEY>") ```
A list of available LLM models can be found here [4].
``` response = llm.complete("Explain the importance of low latency LLMs") ```
``` print(response) ```
``` Low latency Large Language Models (LLMs) are important in certain applications due to their ability to process and respond to inputs quickly. Latency refers to the time delay between a user's request and the system's response. In some real-time or time-sensitive applications, low latency is critical to ensure a smooth user experience and prevent delays or lag.

For example, in conversational agents or chatbots, users expect quick and responsive interactions. If the system takes too long to process and respond to user inputs, it can negatively impact the user experience and lead to frustration. Similarly, in applications such as real-time language translation or speech recognition, low latency is essential to provide accurate and timely feedback to the user.
Furthermore, low latency LLMs can enable new use cases and applications that require real-time or near real-time processing of language inputs. For instance, in the field of autonomous vehicles, low latency LLMs can be used for real-time speech recognition and natural language understanding, enabling voice-controlled interfaces that allow drivers to keep their hands on the wheel and eyes on the road.
In summary, low latency LLMs are important for providing a smooth and responsive user experience, enabling real-time or near real-time processing of language inputs, and unlocking new use cases and applications that require real-time or near real-time processing of language inputs. ```
#### Call `chat` with a list of messages

messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="What is your name"), ] resp = llm.chat(messages) ```

``` print(resp) ```
``` assistant: Arr, I be known as Captain Redbeard, the fiercest pirate on the seven seas! But ye can call me Cap'n Redbeard for short. I'm a fearsome pirate with a love for treasure and adventure, and I'm always ready for a good time! Whether I'm swabbin' the deck or swiggin' grog, I'm always up for a bit of fun. So hoist the Jolly Roger and let's set sail for adventure, me hearties! ```
### Streaming
Using `stream_complete` endpoint
``` response = llm.stream_complete("Explain the importance of low latency LLMs") ```
``` for r in response: print(r.delta, end="") ```
``` Low latency Large Language Models (LLMs) are important in the field of artificial intelligence and natural language processing (NLP) due to several reasons:
1. Real-time applications: Low latency LLMs are essential for real-time applications such as chatbots, voice assistants, and real-time translation services. These applications require immediate responses, and high latency can result in a poor user experience. 2. Improved user experience: Low latency LLMs can provide a more seamless and responsive user experience. Users are more likely to continue using a service that provides quick and accurate responses, leading to higher user engagement and satisfaction. 3. Better decision-making: In some applications, such as financial trading or autonomous vehicles, low latency LLMs can provide critical information in real-time, enabling better decision-making and reducing the risk of accidents. 4. Scalability: Low latency LLMs can handle a higher volume of requests, making them more scalable and suitable for large-scale applications.
5. Competitive advantage: Low latency LLMs can provide a competitive advantage in industries where real-time decision-making and responsiveness are critical. For example, in online gaming or e-commerce, low latency LLMs can provide a more immersive and engaging user experience, leading to higher customer loyalty and revenue.
In summary, low latency LLMs are essential for real-time applications, providing a better user experience, enabling better decision-making, improving scalability, and providing a competitive advantage. As LLMs continue to play an increasingly important role in various industries, low latency will become even more critical for their success. ```
Using `stream_chat` endpoint
``` from llama_index.core.llms import ChatMessage
messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="What is your name"), ] resp = llm.stream_chat(messages) ```

``` for r in resp: print(r.delta, end="") ```
``` Arr, I be known as Captain Candybeard! A more colorful and swashbuckling pirate, ye will never find! ```

[1] https://groq.com
[2] https://discord.gg/JvNsBDKeCG
[3] https://console.groq.com/keys
[4] https://console.groq.com/docs/models