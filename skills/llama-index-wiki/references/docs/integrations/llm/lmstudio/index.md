# developers.llamaindex.ai/python/framework/integrations/llm/lmstudio/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/lmstudio/index.md

--- title: LM Studio | Developer Documentation ---
## Setup
1. Download and Install LM Studio 2. Follow the steps mentioned in the README [1].
If not already installed in collab, install *llama-index* and *lmstudio* integration.
``` %pip install llama-index-core llama-index llama-index-llms-lmstudio ```
Fix for “RuntimeError: This event loop is already running”
``` import nest_asyncio
nest_asyncio.apply() ```
``` from llama_index.llms.lmstudio import LMStudio from llama_index.core.base.llms.types import ChatMessage, MessageRole ```
``` llm = LMStudio( model_name="Hermes-2-Pro-Llama-3-8B", base_url="http://localhost:1234/v1", temperature=0.7, ) ```

``` response = llm.complete("Hey there, what is 2+2?") print(str(response)) ```
``` The result of 2 + 2 is 4. ```
``` # use llm.stream_complete response = llm.stream_complete("What is 7+3?") for r in response: print(r.delta, end="") ```

``` The result of 7 + 3 is 10. ```
``` messages = [ ChatMessage( role=MessageRole.SYSTEM, content="You an expert AI assistant. Help User with their queries.", ), ChatMessage( role=MessageRole.USER, content="What is the significance of the number 42?", ), ] ```

``` response = llm.chat(messages=messages) print(str(response)) ```
``` assistant: The number 42 has been significant in various contexts throughout history and across different cultures, often holding symbolic or philosophical meanings.
1. In mathematics: 42 is a relatively simple but still interesting whole number with no factors other than 1 and itself.
2. In popular culture: Douglas Adams' science fiction series "The Hitchhiker's Guide to the Galaxy" presents the ultimate answer to the meaning of life as 42, which has become a well-known joke and meme since its introduction in the first book published in 1979.
3. In religion and mythology: The number 42 appears in various religious texts or myths with different meanings, such as the Biblical Book of Numbers where Moses spent 42 years tending to his father-in-law's flock before receiving the call from God, or in Norse mythology when Odin spent 42 nights suspended on Yggdrasil (the World Tree) to gain knowledge.
4. In sports: In baseball, a perfect game is considered to be an immaculate game with no hits, errors, or runners allowed to reach base; only 15 players can achieve this in Major League Baseball history, and the number of their names added together equals 42 (6 + 2 = 8, 3 + 4 = 7).
5. In music: The English rock band Coldplay's popular song "42" is about lead singer Chris Martin reflecting on his age during the time it took for the band to gain success.
The significance of the number 42 varies depending on the context and cultural background. It has often been used symbolically or metaphorically, making it a versatile and intriguing number in various aspects of human life. ```
``` response = llm.stream_chat(messages=messages) for r in response: print(r.delta, end="") ```
``` The number 42 has various significances in different contexts:
1. In popular culture: The famous "Answer to the Ultimate Question of Life, the Universe and Everything" from Douglas Adams' science fiction series "The Hitchhiker's Guide to the Galaxy" is 42. This has led to widespread recognition of the number as something meaningful or profound.
2. Mathematics: The number 42 is a highly composite number with many divisors (1, 2, 3, 6, 7, 14, 21, and 42). In mathematics, the study of factors and divisors plays an essential role in various concepts such as prime factorization and greatest common denominators.
3. Christianity: According to a story from The Book of Kells (an illuminated manuscript), it is said that St. Patrick used the number 42 to calculate when to begin his mission to convert Ireland to Christianity.
4. Astrology: In astrology, the 42nd day after the Winter Solstice marks the beginning of the new astrological year and the start of a 13-month cycle in some traditions.
5. Literature: The number 42 is mentioned several times throughout William Shakespeare's plays, such as "Hamlet" and "Henry IV." It appears as a coincidence or possibly with symbolic intent in these works.
6. In the field of computer science, the popular programming language 'Python' uses 42 as its "magic number" to represent the start-up code for the interpreter.
Each context assigns a different significance to the number 42, making it multi-faceted and culturally relevant in various ways. ```

[1] https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/llms/llama-index-llms-lmstudio/README.md