# developers.llamaindex.ai/python/framework/integrations/llm/fireworks/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/fireworks/index.md

--- title: Fireworks | Developer Documentation ---

If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index llama-index-llms-fireworks ```
## Basic Usage
``` from llama_index.llms.fireworks import Fireworks
# For updated list of available models see: https://app.fireworks.ai/models llm = Fireworks( model="accounts/fireworks/models/llama-v3p1-8b-instruct", # api_key="some key", # uses FIREWORKS_API_KEY env var by default ) ```

#### Call `complete` with a prompt
``` resp = llm.complete("Paul Graham is ") ```

``` A well-known figure in the tech industry and entrepreneurship world. Paul Graham is a:
1. **Venture capitalist**: He co-founded Y Combinator (YC), a startup accelerator and seed fund that has invested in many successful companies, including Airbnb, Dropbox, and Reddit. 2. **Entrepreneur**: Graham co-founded Viaweb, an online auction company that was acquired by Yahoo! in 1998 for $49 million. 3. **Author**: He has written several books on entrepreneurship, including "Hackers & Painters: Big Ideas from the Computer Age" and "The Startup Owner's Manual". 4. **Blogger**: Graham writes a popular blog, "Paul Graham's Essays", where he shares his thoughts on entrepreneurship, startups, and technology. 5. **Philosopher**: His writings often explore the intersection of technology, economics, and philosophy, and he has been influenced by thinkers like Friedrich Hayek and Ayn Rand.
Graham is known for his contrarian views on entrepreneurship and his emphasis on the importance of experimentation, iteration, and learning from failure. He has also been a vocal advocate for the idea that startups should focus on building a product that solves a real problem, rather than trying to create a "unicorn" company. ```
#### Call `chat` with a list of messages

[Column 1]
messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="What is your name"), ] resp = llm.chat(messages) ```

``` print(resp) ```

## Streaming
Using `stream_complete` endpoint
``` resp = llm.stream_complete("Paul Graham is ") ```

[Column 2]
``` assistant: Me hearty! Me name be Captain Blackbeak Betty, the most feared and infamous pirate to ever sail the Seven Seas! Me be a swashbucklin' scallywag with a heart o' gold and a spirit o' adventure. Me ship, the "Maverick's Revenge", be me home and me pride, and me crew be the most loyal and trusty scurvy dogs on the high seas!
Now, what be bringin' ye to these fair waters? Are ye lookin' to join me crew and sail the seas in search o' treasure and glory? Or be ye just lookin' for a bit o' trouble and a taste o' the pirate life? Either way, ye be in luck, matey, 'cause Captain Blackbeak Betty be here to guide ye through the choppiest o' waters and the most treacherous o' seas! ```


``` A well-known figure in the tech industry!
Paul Graham is a British-American programmer, venture capitalist, and essayist. He is best known for:
1. **Co-founding Y Combinator**: In 2005, Graham co-founded Y Combinator, a startup accelerator that provides seed funding and mentorship to early-stage startups. Y Combinator has become one of the most successful and influential startup accelerators in the world. 2. **Writing essays on entrepreneurship and programming**: Graham is a prolific writer and has written many essays on topics such as entrepreneurship, programming, and the startup ecosystem. His essays are widely read and respected in the tech industry. 3. **Being a successful entrepreneur**: Before co-founding Y Combinator, Graham co-founded Viaweb, an online auction company that was acquired by Yahoo! in 1998 for $49 million. 4. **Investing in startups**: Graham has invested in many successful startups through Y Combinator, including Dropbox, Airbnb, and Reddit.

Graham's ideas and writings have had a significant impact on the startup ecosystem, and he is widely regarded as one of the most influential figures in the tech industry. ```
Using `stream_chat` endpoint
``` from llama_index.core.llms import ChatMessage
messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="What is your name"), ] resp = llm.stream_chat(messages) ```

``` for r in resp: print(r.delta, end="") ```
``` Me hearty! Me name be Captain Blackbeak Betty, the most feared and infamous pirate to ever sail the Seven Seas! Me be a swashbucklin' scallywag with a heart o' gold and a spirit o' adventure. Me and me trusty parrot, Polly, have been sailin' the high seas for nigh on 20 years, plunderin' treasure and bringin' joy to all who cross me path.
Me ship, the "Maverick's Revenge", be a beauty, with three masts and a hull as black as coal. She be fast, she be fierce, and she be me home sweet home. Me and me crew, the "Maverick's Men", be a motley bunch, but we be loyal to each other and to our captain, that be me!
So, what be bringin' ye to these fair waters? Are ye lookin' to join me crew and sail the seas with the greatest pirate of all time? Or be ye just lookin' for a bit o' treasure and a tale to tell? Either way, ye be in luck, matey! Captain Blackbeak Betty be here to help ye find what ye be lookin' for! ```