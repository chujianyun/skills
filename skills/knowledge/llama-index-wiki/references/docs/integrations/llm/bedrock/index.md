# developers.llamaindex.ai/python/framework/integrations/llm/bedrock/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/bedrock/index.md

--- title: Bedrock | Developer Documentation ---

**Deprecated**: Use llama-index-llms-bedrock-converse [1] instead, the converse API is the recommended way to use Bedrock.
## Basic Usage
#### Call `complete` with a prompt
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-llms-bedrock ```
``` !pip install llama-index ```

profile_name = "Your aws profile name" resp = Bedrock( model="amazon.titan-text-express-v1", profile_name=profile_name ).complete("Paul Graham is ") ```

[Column 1]
#### Call `chat` with a list of messages
``` from llama_index.core.llms import ChatMessage from llama_index.llms.bedrock import Bedrock

messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="Tell me a story"), ]

resp = Bedrock( model="amazon.titan-text-express-v1", profile_name=profile_name ).chat(messages) ```

[Column 2]
``` Paul Graham is a computer scientist and entrepreneur, best known for co-founding the Silicon Valley startup incubator Y Combinator. He is also a prominent writer and speaker on technology and business topics, and his essays have been collected in a book titled "Hackers & Painters." ```


``` assistant: Alright, matey! Here's a story for you:
Once upon a time, there was a pirate named Captain Jack Sparrow who sailed the seas in search of his next adventure. He was a notorious rogue with a reputation for being unpredictable and a bit of a scallywag.
One day, Captain Jack encountered a group of treasure-hunting rivals who were also after the same treasure. The rivals tried to steal the treasure from Captain Jack, but he outsmarted them and managed to keep the treasure for himself.
However, Captain Jack soon discovered that the treasure he had stolen was cursed. Every time he tried to use it, it would cause him some sort of trouble or inconvenience. For example, whenever he tried to spend it, it would turn into a pile of sand or a bunch of sea turtles.
Despite the curse, Captain Jack was determined to find a way to break it. He set out on a journey to find a wise old seer who could help him lift the curse. Along the way, he encountered all sorts of strange and magical creatures, including a talking parrot and a sea witch.
Finally, Captain Jack found the seer and explained his predicament. The seer told him that the only way to break the curse was to return the treasure to its rightful owner.
Captain Jack was hesitant at first, but he knew that it was the right thing to do. He set out on a new adventure to find the rightful owner of the treasure, and along the way, he discovered that sometimes the greatest treasures are not the ones that can be measured in gold or silver, but the ones that come with a sense of purpose and meaning.
And so, Captain Jack returned the treasure to its rightful owner, and the curse was lifted. He sailed off into the sunset, a hero who had learned that the true treasure of life is not found in material possessions, but in the experiences and connections we make with others.
Yarr! Hope you enjoyed that tale, matey! ```
## Streaming
Using `stream_complete` endpoint

llm = Bedrock(model="amazon.titan-text-express-v1", profile_name=profile_name) resp = llm.stream_complete("Paul Graham is ") ```

``` Paul Graham is a computer programmer, entrepreneur, investor, and writer, best known for co-founding the internet firm Y Combinator. He is also the author of several books, including "The Innovator's Dilemma" and "On the Internet."
Graham has been a strong supporter of the startup community and the concept of "disruption" in the technology sector. He has written extensively about the challenges faced by early-stage companies and the importance of creating new and innovative products.
Graham is also known for his contrarian views on a variety of topics, including education, government, and the future of the internet. He has been an outspoken critic of the way higher education is administered in the United States and has advocated for a more experimental and entrepreneurial approach to learning.
Overall, Paul Graham is a highly influential figure in the technology industry, known for his thoughtful and thought-provoking writing and his support for innovative startups and entrepreneurs. ```
Using `stream_chat` endpoint

llm = Bedrock(model="amazon.titan-text-express-v1", profile_name=profile_name) messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="Tell me a story"), ] resp = llm.stream_chat(messages) ```

``` for r in resp: print(r.delta, end="") ```
``` Once upon a time, there was a pirate with a colorful personality who sailed the high seas in search of adventure. She was known for her boldness, her wit, and her love of all things flashy and fancy. But beneath her swashbuckling exterior, there was a heart full of gold, and a desire to do good in the world.
One day, while on her usual voyages, the pirate came across a small island in distress. The villagers were suffering from a terrible drought, and their crops were failing. The pirate knew that she had to help them, and so she set out to find a way to bring water to the island.
After much searching, the pirate discovered a hidden spring deep in the heart of the island. She worked tirelessly to build a system of pipes and aqueducts that would carry the spring water to the villages, and finally, after many long months of hard work, the drought was over, and the people were saved.
The pirate was hailed as a hero, and the villagers threw a grand celebration in her honor. But she knew that her work was not yet done. She continued to sail the seas, seeking out other ways to help those in need, and to spread joy and happiness wherever she went.
And so, the pirate with the colorful personality lived out her days in a blaze of glory, inspiring others with her courage, her kindness, and her unquenchable sense of adventure. ```
## Configure Model

llm = Bedrock(model="amazon.titan-text-express-v1", profile_name=profile_name) ```
``` resp = llm.complete("Paul Graham is ") ```

``` Paul Graham is a computer scientist, entrepreneur, investor, and writer. He co-founded Viaweb, the first commercial web browser, and was a founder of Y Combinator, a startup accelerator. He is the author of several books, including "The Art of Computer Programming" and "On Lisp." He is known for his essays on technology and business, and his perspective on the tech industry. ```
# Connect to Bedrock with Access Keys
``` from llama_index.llms.bedrock import Bedrock
llm = Bedrock( model="amazon.titan-text-express-v1", aws_access_key_id="AWS Access Key ID to use", aws_secret_access_key="AWS Secret Access Key to use", aws_session_token="AWS Session Token to use", region_name="AWS Region to use, eg. us-east-1", )

resp = llm.complete("Paul Graham is ") ```
``` print(resp) ```
``` Paul Graham is an American computer scientist, entrepreneur, investor, and author, best known for co-founding Viaweb, the first commercial web browser. He was a co-founder of Netscape Communications and the creator of the Mozilla Foundation. He was also a Y Combinator partner and a prominent early-stage investor in companies such as Airbnb, Dropbox, Facebook, and Twitter. ```

[1] https://docs.llamaindex.ai/en/stable/examples/llm/bedrock_converse/