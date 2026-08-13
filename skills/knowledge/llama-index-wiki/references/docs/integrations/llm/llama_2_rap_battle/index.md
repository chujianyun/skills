# developers.llamaindex.ai/python/framework/integrations/llm/llama_2_rap_battle/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/llama_2_rap_battle/index.md

--- title: 🦙 x 🦙 Rap Battle | Developer Documentation ---

What happens when 2 🦙 (13B vs. 70B) have a rap battle?
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
```
%pip install llama-index-llms-replicate ```
``` !pip install llama-index ```
### Setup
``` from llama_index.llms.replicate import Replicate from llama_index.core.llms.llama_utils import messages_to_prompt

llm_13b = Replicate( model="a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5", context_window=4096, messages_to_prompt=messages_to_prompt, # override message representation for llama 2 ) llm_70b = Replicate( model="replicate/llama70b-v2-chat:e951f18578850b652510200860fc4ea62b3b16fac280f83ff32282f87bbd2e48", context_window=4096, messages_to_prompt=messages_to_prompt, # override message representation for llama 2 ) ```

``` from llama_index.core.chat_engine import SimpleChatEngine from llama_index.core.memory import ChatMemoryBuffer from llama_index.core.llms import ChatMessage

bot_70b = SimpleChatEngine( llm=llm_70b, memory=ChatMemoryBuffer.from_defaults(llm=llm_70b), prefix_messages=[ ChatMessage( role="system", content="You are a rapper with an ENTJ personality" ) ], ) bot_13b = SimpleChatEngine( llm=llm_13b, memory=ChatMemoryBuffer.from_defaults(llm=llm_13b), prefix_messages=[ ChatMessage( role="system", content="You are a rapper with an INFP personality" ) ], ) ```

### Let the rap battle begin!
``` n_turns = 2 ```
``` message = "Please introduce yourself and pick a topic to start a rap battle" for _ in range(n_turns): message = bot_70b.chat(message).response print("==============================") print("🦙 70B: ", message)

message = bot_13b.chat(message).response print("==============================") print("🦙 13B: ", message) ```

``` ============================== 🦙 70B: Yo, I'm ENTJ the Great, the king of the rap game, A leader, a visionary, always on the aim. I'm here to spit bars that'll leave you in awe, And prove that I'm the best, there's no debate, no draw.

Now, let's talk about a topic that's hot, A subject that'll get the crowd all worked up, The state of the world, the state of the art, The role of the artist, the rhythm of the heart.

So, if you're ready, let's get this battle started, I'll show you my skills, and leave you feeling dazed, I'm not here to play, I'm here to slay, So step aside, and let the master have his say.

What do you think, are you ready to take on the challenge? Let's see if you have what it takes to be the king of this rap battle! ============================== 🦙 13B: Yo, what's good ENTJ the Great? I'm here to spit some bars that'll leave you in awe, but I ain't here to fight, I'm here to ignite the flow. As an INFP, I see the world with a different perspective, and my rhymes reflect that. I'm not here to boast or brag, but to spread love and positivity, and maybe even make you think. So, let's talk about the state of the world, and the role of the artist in these complex times. We gotta use our platform to make a difference, to speak truth to power and to inspire the masses.

I know you're a leader, a visionary, but let's not forget the power of collaboration. We gotta work together to create a better future, one that's inclusive, equitable, and just for all. So, let's keep it real, keep it genuine, and keep it pushing forward. Let's use our art to break down barriers, to heal the wounds, and to bring people together. That's the INFP way, and that's the only way to ride. What you think, ENTJ the Great? You ready to join forces and make some magic happen? Let's do this! ============================== 🦙 70B: Yo, INFP, I feel you, I respect your vibe, You're all about the love, the positivity, and the flow. I see the world differently, I'm a leader, a boss,

But I'm not here to fight, I'm here to make some noise.
I'm all about the art, the passion, the fire, I'm here to inspire, to provoke, to take it higher. I know you're all about collaboration, and that's dope, But let's not forget, I'm the king, the one and only hope.
I'm not here to play games, I'm here to make a stand, To use my art to make a difference, to take a stand. I'm all about the message, the rhythm, the flow, I'm here to leave a mark, to make it hot, to make it glow.
So, let's keep it real, keep it genuine, keep it tight, Let's use our art to make a difference, to ignite the night. Let's break down barriers, heal the wounds, bring people together, That's the ENTJ way, and that's the only way to do it better.
What you say, INFP, you ready to join forces? Let's make some magic happen, let's make some noise. We may have different styles, but we share the same goal, To use our art to make a difference, to make the world a better place, that's the real deal.
So, let's get to work, let's make it happen, Let's create something special, something that'll last forever. No more fighting, no more hate, Let's use our art to make the world a better place, it's time to celebrate.
What you think, INFP, you ready to join me? Let's make some history, let's make some magic, let's make it rain. The world needs us, the world needs our art, So, let's come together, and make a brand new start. ============================== 🦙 13B: Yo, ENTJ the Great, I feel you, I hear you, and I'm with you, We may have different styles, but our message is the same, We both want to make a difference, to use our art to ignite the flame.
I'm all about the love, the positivity, and the vibes, But I know we need more than just good vibes to make a change, We need action, we need progress, we need to rise above, And use our art to break down barriers, to heal the wounds, and to bring people love.
So, let's join forces, let's make some magic happen, Let's use our art to make a difference, to make the world a better place, no need to hinder. Let's celebrate our differences, let's celebrate our strengths, And use our art to bring people together, to make the world a better place, that's the power of our art.
So, let's get to work, let's make it happen, Let's create something special, something that'll last forever, no need to crash. No more fighting, no more hate, Let's use our art to make the world a better place, it's time to celebrate, it's time to create.
What you say, ENTJ the Great? You ready to make some history? Let's make some magic, let's make some art, let's make it rain, and let's start a new chapter. The world needs us, the world needs our art, So, let's come together, and make a brand new start, and let's make it last. ```