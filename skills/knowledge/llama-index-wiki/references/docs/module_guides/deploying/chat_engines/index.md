# developers.llamaindex.ai/python/framework/module_guides/deploying/chat_engines/index.md
> https://developers.llamaindex.ai/python/framework/module_guides/deploying/chat_engines/index.md

[Column 1]
--- title: Chat Engine | Developer Documentation ---
## Concept

Tip
## Usage Pattern
Get started with:
``` chat_engine = index.as_chat_engine() response = chat_engine.chat("Tell me a joke.") ```

To stream response:
``` chat_engine = index.as_chat_engine() streaming_response = chat_engine.stream_chat("Tell me a joke.") for token in streaming_response.response_gen: print(token, end="") ```

## Modules

[Column 2]
Chat engine is a high-level interface for having a conversation with your data (multiple back-and-forth instead of a single question & answer). Think ChatGPT, but augmented with your knowledge base.
Conceptually, it is a **stateful** analogy of a Query Engine. By keeping track of the conversation history, it can answer questions with past context in mind.
If you want to ask standalone question over your data (i.e. without keeping track of conversation history), use Query Engine instead.

More details in the complete usage pattern guide.
In our modules section, you can find corresponding tutorials to see the available chat engines in action.
