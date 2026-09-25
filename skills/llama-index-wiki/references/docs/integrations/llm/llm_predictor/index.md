# developers.llamaindex.ai/python/framework/integrations/llm/llm_predictor/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/llm_predictor/index.md

--- title: LLM Predictor | Developer Documentation ---
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-llms-openai %pip install llama-index-llms-langchain ```
``` !pip install llama-index ```
## LangChain LLM
``` from langchain.chat_models import ChatAnyscale, ChatOpenAI from llama_index.llms.langchain import LangChainLLM from llama_index.core import PromptTemplate ```
``` llm = LangChainLLM(ChatOpenAI()) ```
``` stream = await llm.astream(PromptTemplate("Hi, write a short story")) ```
``` async for token in stream: print(token, end="") ```
``` Once upon a time, in a small village nestled in the heart of a lush forest, lived a young girl named Lily. Lily was known for her kind heart and gentle spirit. She had a special gift - the ability to communicate with animals.
One sunny morning, as Lily was strolling through the forest, she stumbled upon a wounded bird. Its wing was broken, and it looked helpless. Lily's heart filled with empathy, and she carefully picked up the bird, cradling it in her hands.
"I will help you," she whispered, her voice filled with determination.
Lily hurried back to her cottage, where she gently placed the bird in a cozy nest. She splinted its wing and tended to its wounds. The little bird chirped gratefully, as if it understood Lily's intentions.
Days turned into weeks, and Lily diligently cared for the bird, naming it Oliver. Though the wing healed, Oliver was reluctant to leave. He had developed a strong bond with Lily and her peaceful existence.
One evening, as Lily and Oliver were sitting by the window, a loud noise startled them. Curious, they ventured outside to investigate. To their surprise, the villagers were in a frenzy, pointing towards the sky.
A massive storm cloud was approaching, darkening the once blue canvas. Panic ensued, and everyone rushed to seek shelter. But Lily knew that the animals of the forest were in grave danger. They had no homes to protect them.
With Oliver perched on her shoulder, Lily gathered all the animals she could find - squirrels, rabbits, deer, and even a fox. Together, they formed a united front against the storm.
Using her special gift, Lily communicated with the animals, guiding them to a safer place - her cottage. The animals huddled together, finding comfort in each other's presence.
As the storm raged outside, Lily played soothing melodies on her flute, calming the frightened creatures. The storm grew stronger, but Lily's love and determination were unwavering.
Finally, after what seemed like an eternity, the storm subsided. The sun emerged from behind the clouds, casting a warm glow over the forest. The animals, now safe and sound, returned to their natural habitats.
Lily watched them disappear into the woods, her heart brimming with joy. She knew that she had made a difference, not only for Oliver but for all the creatures she had saved.
From that day forward, Lily became the guardian of the forest, protecting its inhabitants and living in harmony with nature. Her story spread far and wide, inspiring others to cherish the beauty of the natural world and all its creatures.
And so, the young girl with the gift of communication and a heart full of compassion continued to nurture the bond between humans and animals, reminding everyone of the magic that exists when kindness prevails. ```
``` ## Test with ChatAnyscale llm = LangChainLLM(ChatAnyscale()) ```
``` stream = llm.stream( PromptTemplate("Hi, Which NFL team have most Super Bowl wins") ) for token in stream: print(token, end="") ```

``` Hello! As a helpful and respectful assistant, I'm here to provide accurate and safe information. To answer your question, the team with the most Super Bowl wins is the Pittsburgh Steelers, with six championships. However, it's important to note that the Super Bowl is just one aspect of a team's success and there are many other talented and successful NFL teams as well. Additionally, it's important to recognize that the NFL is a professional sports league and should be respected as such. It's not appropriate to use derogatory language or make harmful or offensive comments. Is there anything else I can help with?
```
## OpenAI LLM
``` from llama_index.llms.openai import OpenAI ```
``` llm = OpenAI() ```
``` stream = await llm.astream("Hi, write a short story") ```
``` for token in stream: print(token, end="") ```
``` Once upon a time in a small village nestled in the heart of a lush forest, there lived a young girl named Lily. She was known for her kind heart and adventurous spirit. Lily spent most of her days exploring the woods, discovering hidden treasures and befriending the creatures that called the forest their home.
One sunny morning, as Lily ventured deeper into the forest, she stumbled upon a peculiar sight. A tiny, injured bird lay on the ground, its wings trembling. Lily's heart filled with compassion, and she carefully picked up the bird, cradling it in her hands. She decided to take it home and nurse it back to health.
Days turned into weeks, and the bird, whom Lily named Pip, grew stronger under her care. Pip's once dull feathers regained their vibrant colors, and his wings regained their strength. Lily knew it was time for Pip to return to the wild, where he truly belonged.
With a heavy heart, Lily bid farewell to her feathered friend, watching as Pip soared into the sky, his wings carrying him higher and higher. As she stood there, a sense of emptiness washed over her. She missed Pip's cheerful chirping and the companionship they had shared.
Determined to fill the void, Lily decided to embark on a new adventure. She set out to explore the forest in search of a new friend. Days turned into weeks, and Lily encountered various animals, but none seemed to be the perfect companion she longed for.
One day, as she sat by a babbling brook, feeling disheartened, a rustling sound caught her attention. She turned around to find a small, fluffy creature with bright blue eyes staring back at her. It was a baby fox, lost and scared. Lily's heart melted, and she knew she had found her new friend.
She named the fox Finn and took him under her wing, just as she had done with Pip. Together, they explored the forest, climbed trees, and played hide-and-seek. Finn brought joy and laughter back into Lily's life, and she cherished their bond.
As the years passed, Lily and Finn grew older, but their friendship remained strong. They became inseparable, exploring the forest and facing its challenges together. Lily learned valuable lessons from the forest and its creatures, and she shared these stories with Finn, who listened intently.
One day, as they sat beneath their favorite oak tree, Lily realized how much she had grown since she first found Pip. She had learned the importance of compassion, friendship, and the beauty of nature. The forest had become her sanctuary, and its creatures her family.
Lily knew that her adventures would continue, and she would always find new friends along the way. With Finn by her side, she was ready to face any challenge that awaited her. And so, hand in paw, they set off into the forest, ready to create new memories and embark on countless adventures together. ```