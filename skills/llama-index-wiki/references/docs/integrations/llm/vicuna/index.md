# developers.llamaindex.ai/python/framework/integrations/llm/vicuna/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/vicuna/index.md

--- title: Replicate - Vicuna 13B | Developer Documentation ---

## Setup
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-llms-replicate ```
``` !pip install llama-index ```
Make sure you have the `REPLICATE_API_TOKEN` environment variable set.\ If you don’t have one yet, go to <https://replicate.com/> to obtain one.
``` import os ```
``` os.environ["REPLICATE_API_TOKEN"] = "<your API key>" ```
## Basic Usage
We showcase the “vicuna-13b” model, which you can play with directly at: <https://replicate.com/replicate/vicuna-13b>

llm = Replicate( model="replicate/vicuna-13b:6282abe6a492de4145d7bb601023762212f9ddbbe78278bd6771c8b3b2f2a13b" ) ```
#### Call `complete` with a prompt

``` PaulGraham is a British physicist, mathematician, and computer scientist. He is best known for his work on the foundations of quantum mechanics and his contributions to the development of the field of quantum computing.
Graham was born on August 15, 1957, in Cambridge, England. He received his undergraduate degree in mathematics from the University of Cambridge in 1979 and later earned his Ph.D. in theoretical physics from the University of California, Berkeley in 1984.
Throughout his career, Graham has made significant contributions to the field of quantum mechanics. He has published a number of influential papers on the subject, including "Quantum mechanics at 1/2 price," "The holonomy of quantum mechanics," and "Quantum mechanics in the presence of bounded self-adjoint operators."
Graham has also been a key figure in the development of quantum computing. He is a co-founder of the quantum computing company, QxBranch, and has played a leading role in efforts to develop practical quantum algorithms and build large-scale quantum computers.
In addition ```
#### Call `chat` with a list of messages

messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="What is your name"), ] resp = llm.chat(messages) ```

[Column 1]
``` assistant: ```
### Streaming
Using `stream_complete` endpoint
``` response = llm.stream_complete("Who is Paul Graham?") ```
``` for r in response: print(r.delta, end="") ```

Using `stream_chat` endpoint
``` from llama_index.core.llms import ChatMessage
messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="What is your name"), ] resp = llm.stream_chat(messages) ```

``` for r in resp: print(r.delta, end="") ```

[Column 2]
``` PaulGraham is a British philosopher, cognitive scientist, and entrepreneur. He is best known for his work on the philosophy of the mind and consciousness, as well as his contributions to the development of the field of Artificial Intelligence (AI).
Graham was born in London in 1938 and received his education at the University of Cambridge, where he studied philosophy and the natural sciences. After completing his studies, he went on to hold academic appointments at several prestigious universities, including the University of Oxford and the University of California, Berkeley.
Throughout his career, Graham has been a prolific writer and thinker, publishing numerous articles and books on a wide range of topics, including the philosophy of mind, consciousness, AI, and the relationship between science and religion. He has also been involved in the development of several successful technology startups, including Viaweb (which was later acquired by Yahoo!) and Palantir Technologies.
Despite his many achievements, Graham is perhaps best known for his contributions to the philosophy of the mind and consciousness. In particular, his work on the concept of ```


```
## Configure Model
``` from llama_index.llms.replicate import Replicate
llm = Replicate( model="replicate/vicuna-13b:6282abe6a492de4145d7bb601023762212f9ddbbe78278bd6771c8b3b2f2a13b", temperature=0.9, max_tokens=32, ) ```

``` resp = llm.complete("Who is Paul Graham?") ```
``` print(resp) ```
``` PaulGraham is an influential computer scientist, venture capitalist, and essayist. He is best known as ```