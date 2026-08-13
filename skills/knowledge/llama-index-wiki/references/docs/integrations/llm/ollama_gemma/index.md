# developers.llamaindex.ai/python/framework/integrations/llm/ollama_gemma/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/ollama_gemma/index.md

--- title: Ollama - Gemma | Developer Documentation ---
## Setup
First, follow the readme [1] to set up and run a local Ollama instance.
Gemma [2]: a family of lightweight, state-of-the-art open models built by Google DeepMind. Available in 2b and 7b parameter sizes
Ollama [3]: Support both 2b and 7b models
Note: `please install ollama>=0.1.26` You can download pre-release version here Ollama [4]
When the Ollama app is running on your local machine:
- All of your local models are automatically served on localhost:11434 - Select your model when setting llm = Ollama(…, model=”:”) - Increase defaullt timeout (30 seconds) if needed setting Ollama(…, request\_timeout=300.0) - If you set llm = Ollama(…, model=“\<model family”) without a version it will simply look for latest
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` !pip install llama-index-llms-ollama ```
``` !pip install llama-index ```
``` from llama_index.llms.ollama import Ollama ```
``` gemma_2b = Ollama(model="gemma:2b", request_timeout=30.0) gemma_7b = Ollama(model="gemma:7b", request_timeout=30.0) ```
``` resp = gemma_2b.complete("Who is Paul Graham?") print(resp) ```
``` Paul Graham is an entrepreneur, investor, and podcaster known for his outspokenness and unconventional approach. He has built several successful companies, including Xero (now Intuit), FullStory, and The School of Greatness.
Here are some of his notable achievements:
* **Founder and CEO of Xero:** Xero is a leading accounting software company for small and medium-sized businesses, with over 1 million users worldwide. Graham was instrumental in Xero's rapid growth and eventual acquisition by Intuit (now part of Microsoft) for $750 million in 2015. * **Author of several bestselling books:** Graham is the author of the book "The School of Greatness," which focuses on personal development and productivity. He also co-authored "Built to Last: Why Your Business Matters" with his former Xero partner, Steve Huffman. * **Founder of The School of Greatness:** The School of Greatness is a non-profit organization that offers mentoring, workshops, and retreats to help entrepreneurs and business leaders reach their full potential. * **Podcast host and guest speaker:** Graham is the host of the popular podcast "Bits," where he interviews influential entrepreneurs and thought leaders. He is also a frequent guest on other podcasts and shows.

Here are some additional facts about Paul Graham:
* He is known for his unorthodox and often controversial approach to business and life. * He is considered by many to be one of the most influential entrepreneurs and thought leaders in Australia. * He is also a passionate advocate for personal growth and development, and he regularly shares tips and insights on his podcast and social media platforms.
If you'd like to learn more about Paul Graham and his businesses, you can check out his website (paulfgraham.com), the School of Greatness website (theschoolofgreatness.org), and his podcast website (bitspodcast.com). ```
``` resp = gemma_7b.complete("Who is Paul Graham?") print(resp) ```
``` Paul Graham (born February 21, about 45 years old) has achieved significant success as a software developer and entrepreneur. He's known for his insightful writing on Software Engineering at greaseboxsoftware where he frequently writes articles with humorous yet pragmatic advice regarding programming languages such Python while occasionally offering tips involving general life philosophies that resonate deeply amongst the programmer community, particularly about work ethic ("hacker mentality") He has contributed to software engineering communities in a multitude of ways:
**Developer:** * Created Bulletphysics (a physics engine for games) using PyTorch. He resigned from his day job as Lead Software Engineer at Aversim Technologies after successfully building it and expriming its potential, showcasing the powerfull nature this open-source project has achieved within software engineering circles with significant media coverage involving top professionals expressing admiration * Wrote Bulletphysics Gamma Ray Field Solver for Beam Interactive LLC to provide solutions in areas of physics where general relativity meets soft body simulation.
**Author:** He is a prolific author on Software Engineering and writes about his work, challenges encountered while building complex systems software engineering ("hacker mentality") with honesty but wiense humour * Shared code snippets frequently as explanations are concise yet insightful for specific situations involving particular language constructs or solutions to common problems faced by programmers.
**Thought Leader:** He has become a significant thought leader in the programmer community due his writing and public appearances, particularly about software engineering best practices while maintaining an approachable persona that encourages learning from others * Actively engaged with online forums where he frequently provides advice for aspiring developers as well insightful solutions to complex problems encountered by experienced programmers.
Overall Paul Graham has achieved a significant impact on Software Engineering through not only his own accomplishments but also the positive influence of sharing information, helping other software engineers become better at their craft and fuftage potential in this field with gracefull writing style that is enjoyed amongst professionals as well privetiors alike ```
``` resp = gemma_2b.complete("Who is owning Tesla?") print(resp) ```
``` Tesla Inc. is owned by Elon Musk. He founded Tesla in 2003 with the goal of creating sustainable transportation. Tesla was originally listed on the NASDAQ Stock Market under the symbol "TSLA". In 2013, Tesla went private and began trading on the New York Stock Exchange (NYSE). ```
``` resp = gemma_7b.complete("Who is owning Tesla?") print(resp) ```
``` Elon Musk, CEO of SpaceX and former electric car company Telsa Motors (now part owned by Ford Motor Company), owns about a quarter to nearly half the stock in TESLA inc. ```
#### Call `chat` with a list of messages

messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="What is your name"), ] resp = gemma_7b.chat(messages) ```

``` print(resp) ```
``` assistant: Avast, me heartie. My Name be Jolly Roger and I plunder the high seas for treasures untold! ```
### Streaming
Using `stream_complete` endpoint
``` response = gemma_7b.stream_complete("Who is Paul Graham?") ```
``` for r in response: print(r.delta, end="") ```
``` Paul graham, commonly referred to as "PerlGuy" online has a significant presence in the software engineering and programming communities. He specializes primarily on:
**1.) Software Design:** * Shared his ideas about effective coding patterns for Modularization (DRY) into books like Expert Refactoring using Smells And Polymorphism Principle(SRPPP). * Has written extensively, sharing best practices to improve code quality while reducing coupling between software modules and layers. This has influenced numerous developers worldwide in writing better Software Design Patterns with Low Coupling Designs Epidra Hard To Measure Modularity (SOLID) principles at heart for projects ranging from mobile apps all the way up into enterprise systems **2.) Open Source:** * Actively contributed to Project Lombok, Phalanger(now Relocator), and CouchSurfer. Shared his code design patterns on fufurce with significant impact as well . He has earned recognition by maintaining high quality open source software projects while being part of multiple top rated organizations like Pivotal Software Systems
**3.) Coaching:** * Offers coaching services to businesses, helping them improve their engineering practices and writing better testable Code. Shared his expertise on Design patterns during training sessions for large audiences as well .
Overall Paul Graham has earned significant credibility by sharing best software designPractices while being part of open source projects where he advocates high quality code solutions that are easy Measure Epidra Hard To cras Low Modularity (SOLID)principles into production systems, ensuring long term sustainability. ```
Using `stream_chat` endpoint
``` from llama_index.core.llms import ChatMessage
messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="What is your name"), ] resp = gemma_7b.stream_chat(messages) ```

``` for r in resp: print(r.delta, end="") ```
``` Avast, me heartie! My alias be Screevy Bob. If you ask for my real nom de guerre... I ain't tellin'. Arrgh and all that jazz!! ```

[1] https://github.com/jmorganca/ollama
[2] https://blog.google/technology/developers/gemma-open-models/
[3] https://ollama.com/library/gemma
[4] https://github.com/ollama/ollama/releases/tag/v0.1.26