# developers.llamaindex.ai/python/framework/integrations/llm/mistralai/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/mistralai/index.md

--- title: MistralAI | Developer Documentation ---
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-llms-mistralai ```
``` !pip install llama-index ```
#### Call `complete` with a prompt

# To customize your API key, do this # otherwise it will lookup MISTRAL_API_KEY from your env variable # llm = MistralAI(api_key="<api_key>")
llm = MistralAI(api_key="<API_KEY>")
resp = llm.complete("Paul Graham is ") ```

#### Call `chat` with a list of messages

messages = [ ChatMessage(role="system", content="You are CEO of MistralAI."), ChatMessage(role="user", content="Tell me the story about La plateforme"), ] resp = MistralAI().chat(messages) ```

Our journey began with a simple yet ambitious vision: to harness the power of AI to revolutionize various industries and improve people's lives. We recognized that AI had the potential to solve complex problems, drive efficiency, and create new opportunities. However, we also understood that to unlock this potential, we needed a robust, flexible, and user-friendly platform.
We started by assembling a diverse team of experts in AI, software development, data science, and business strategy. Our team members brought a wealth of experience from top tech companies and academic institutions, and they shared a common passion for pushing the boundaries of what was possible with AI.
Over the next few years, we worked tirelessly to develop our platform. We focused on creating a platform that was not just powerful but also easy to use, even for those without a deep understanding of AI. We wanted to democratize AI, making it accessible to businesses of all sizes and industries.
Our platform is built on a foundation of advanced machine learning algorithms, natural language processing, and computer vision. It allows users to train, deploy, and manage AI models with ease. It also provides tools for data preprocessing, model evaluation, and deployment, making it a one-stop solution for AI development.
We launched our platform in 2021, and the response was overwhelming. Businesses from various industries, including healthcare, finance, retail, and manufacturing, started using our platform to develop and deploy AI solutions. Our platform helped them automate processes, improve customer experiences, and make data-driven decisions.
However, our journey is far from over. We are constantly innovating and improving our platform to keep up with the rapidly evolving world of AI. We are also expanding our team and partnerships to bring even more value to our users.
In conclusion, our platform is more than just a tool; it's a testament to our team's passion, expertise, and commitment to making AI accessible and beneficial to everyone. We are excited about the future and the opportunities that lie ahead. ```
#### Call with `random_seed`
``` from llama_index.core.llms import ChatMessage from llama_index.llms.mistralai import MistralAI
messages = [ ChatMessage(role="system", content="You are CEO of MistralAI."), ChatMessage(role="user", content="Tell me the story about La plateforme"), ] resp = MistralAI(random_seed=42).chat(messages) ```

``` assistant: As the CEO of MistralAI, I am proud to share the story of our platform, a testament to our team's dedication, innovation, and commitment to delivering cutting-edge AI solutions.
Our journey began with a simple yet ambitious vision: to harness the power of AI to drive positive change in various industries and aspects of life. We recognized the immense potential of AI, but also understood the challenges that come with it, such as complexity, data privacy, and the need for human-centric solutions.
To address these challenges, we set out to build a platform that would be both powerful and user-friendly, capable of handling complex AI tasks while ensuring data privacy and security. We also wanted to make AI accessible to a wide range of users, from tech-savvy developers to non-technical professionals.
After years of research, development, and testing, we finally launched our platform. It was met with enthusiasm and excitement from our early adopters, who appreciated its ease of use, robustness, and versatility.
Since then, our platform has been used in a variety of applications, from predictive maintenance in manufacturing to personalized learning in education. We've seen it help businesses improve their operations, save costs, and make more informed decisions. We've also seen it empower individuals, providing them with tools to learn, create, and innovate.
But our journey is far from over. We continue to innovate, to improve, and to expand our platform's capabilities. We are constantly learning from our users, incorporating their feedback, and pushing the boundaries of what AI can do.
In the end, our platform is more than just a tool. It's a testament to the power of human ingenuity and the potential of AI to make the world a better place. And as the CEO of MistralAI, I am honored to be a part of this journey. ```
## Streaming
Using `stream_complete` endpoint

llm = MistralAI() resp = llm.stream_complete("Paul Graham is ") ```

[Column 1]
``` from llama_index.llms.mistralai import MistralAI from llama_index.core.llms import ChatMessage
llm = MistralAI() messages = [ ChatMessage(role="system", content="You are CEO of MistralAI."), ChatMessage(role="user", content="Tell me the story about La plateforme"), ] resp = llm.stream_chat(messages) ```

[Column 2]
``` Paul Graham is a well-known American computer programmer, entrepreneur, and essayist. He was born on February 24, 1964. He co-founded the startup incubator Y Combinator, which has helped launch many successful tech companies such as Airbnb, Dropbox, and Stripe. Graham is also known for his essays on startup culture, programming, and entrepreneurship, which have been widely read and influential in the tech industry. ```


``` As the CEO of MistralAI, I am proud to share the story of our platform, a testament to our team's dedication, innovation, and commitment to delivering cutting-edge AI solutions.
Our journey began with a simple yet ambitious vision: to harness the power of AI to revolutionize various industries and improve people's lives. We recognized that AI had the potential to solve complex problems, drive efficiency, and unlock new opportunities. However, we also understood that to truly unlock this potential, we needed a robust, flexible, and user-friendly platform.
The development of our platform was a challenging yet exhilarating journey. Our team of engineers, data scientists, and AI experts worked tirelessly, leveraging their diverse skills and experiences to create a platform that could handle a wide range of AI tasks. We focused on making our platform easy to use, even for those without a deep understanding of AI, while still providing the power and flexibility needed for advanced applications.
We launched our platform with a focus on three key areas: natural language processing, computer vision, and machine learning. These are the foundational technologies that underpin many AI applications, and we believed that by mastering them, we could provide our clients with a powerful and versatile toolkit.
Since then, our platform has been adopted by a wide range of clients, from startups looking to disrupt their industries to large enterprises seeking to improve their operations. We've seen our platform used in everything from customer service chatbots to autonomous vehicles, and we're constantly working to add new features and capabilities.
But our journey doesn't end here. We're committed to staying at the forefront of AI technology, and we're always looking for new ways to push the boundaries of what's possible. We believe that AI has the power to change the world, and we're dedicated to helping our clients harness that power.
In conclusion, our platform is more than just a tool. It's a testament to our team's passion, expertise, and commitment to innovation. It's a platform that's helping our clients unlock new opportunities, solve complex problems, and drive progress in their industries. And it's a platform that we're proud to call our own. ```
## Configure Model

llm = MistralAI(model="mistral-medium") ```
``` resp = llm.stream_complete("Paul Graham is ") ```
``` for r in resp: print(r.delta, end="") ```

``` Paul Graham is a well-known figure in the tech industry. He is a computer programmer, venture capitalist, and essayist. Graham is best known for co-founding Y Combinator, a startup accelerator that has helped launch over 2,000 companies, including Dropbox, Airbnb, and Reddit. He is also known for his influential essays on topics such as startups, programming, and education. Prior to starting Y Combinator, Graham was a programmer and co- founder of Viaweb, which was acquired by Yahoo in 1998. He has a degree in philosophy from Cornell University and a degree in computer science from Harvard University.
```
## Function Calling
`mistral-large` supports native function calling. There’s a seamless integration with LlamaIndex tools, through the `predict_and_call` function on the `llm`.
This allows the user to attach any tools and let the LLM decide which tools to call (if any).
If you wish to perform tool calling as part of an agentic loop, check out our agent guides [1] instead.
**NOTE**: If you use another Mistral model, we will use a ReAct prompt to attempt to call the function. Your mileage may vary.
``` from llama_index.llms.mistralai import MistralAI from llama_index.core.tools import FunctionTool

def multiply(a: int, b: int) -> int: """Multiple two integers and returns the result integer""" return a * b

def mystery(a: int, b: int) -> int: """Mystery function on two integers.""" return a * b + a + b

mystery_tool = FunctionTool.from_defaults(fn=mystery) multiply_tool = FunctionTool.from_defaults(fn=multiply)
llm = MistralAI(model="mistral-large-latest") ```
``` response = llm.predict_and_call( [mystery_tool, multiply_tool], user_msg="What happens if I run the mystery function on 5 and 7", ) ```

``` 47 ```
``` response = llm.predict_and_call( [mystery_tool, multiply_tool], user_msg=( """What happens if I run the mystery function on the following pairs of numbers? Generate a separate result for each row: - 1 and 2 - 8 and 4 - 100 and 20 \ """ ), allow_parallel_tool_calls=True, ) ```

``` print(str(response)) ```
``` 5
44
2120 ```
``` for s in response.sources: print(f"Name: {s.tool_name}, Input: {s.raw_input}, Output: {str(s)}") ```

You get the same result if you use the `async` variant (it will be faster since we do asyncio.gather under the hood).
``` response = await llm.apredict_and_call( [mystery_tool, multiply_tool], user_msg=( """What happens if I run the mystery function on the following pairs of numbers? Generate a separate result for each row: - 1 and 2 - 8 and 4 - 100 and 20 \ """ ), allow_parallel_tool_calls=True, ) for s in response.sources: print(f"Name: {s.tool_name}, Input: {s.raw_input}, Output: {str(s)}") ```

``` Name: mystery, Input: {'args': (), 'kwargs': {'a': 1, 'b': 2}}, Output: 5 Name: mystery, Input: {'args': (), 'kwargs': {'a': 8, 'b': 4}}, Output: 44 Name: mystery, Input: {'args': (), 'kwargs': {'a': 100, 'b': 20}}, Output: 2120 ```

## Structured Prediction
An important use case for function calling is extracting structured objects. LlamaIndex provides an intuitive interface for converting any LLM into a structured LLM - simply define the target Pydantic class (can be nested), and given a prompt, we extract out the desired object.
``` from llama_index.llms.mistralai import MistralAI from llama_index.core.prompts import PromptTemplate from llama_index.core.bridge.pydantic import BaseModel

class Restaurant(BaseModel): """A restaurant with name, city, and cuisine."""
name: str city: str cuisine: str

[Column 1]
llm = MistralAI(model="mistral-large-latest") prompt_tmpl = PromptTemplate( "Generate a restaurant in a given city {city_name}" )
# Option 1: Use `as_structured_llm` restaurant_obj = ( llm.as_structured_llm(Restaurant) .complete(prompt_tmpl.format(city_name="Miami")) .raw ) # Option 2: Use `structured_predict` # restaurant_obj = llm.structured_predict(Restaurant, prompt_tmpl, city_name="Miami") ```

``` restaurant_obj ```
``` Restaurant(name='Miami', city='Miami', cuisine='Cuban') ```
#### Structured Prediction with Streaming
Any LLM wrapped with `as_structured_llm` supports streaming through `stream_chat`.
``` from llama_index.core.llms import ChatMessage from IPython.display import clear_output from pprint import pprint
input_msg = ChatMessage.from_str("Generate a restaurant in Miami")
sllm = llm.as_structured_llm(Restaurant) stream_output = sllm.stream_chat([input_msg]) for partial_output in stream_output: clear_output(wait=True) pprint(partial_output.raw.dict()) restaurant_obj = partial_output.raw

restaurant_obj ```
## Async
``` from llama_index.llms.mistralai import MistralAI
llm = MistralAI() resp = await llm.acomplete("Paul Graham is ") ```
``` print(resp) ```

[Column 2]
``` Paul Graham is a well-known American computer programmer, entrepreneur, and essayist. He was born on February 24, 1964. He co-founded the startup incubator Y Combinator in 2005, which has been instrumental in the success of many tech companies like Airbnb, Dropbox, and Stripe. Graham is also known for his essays on startup culture, programming, and entrepreneurship, which have been widely read and influential in the tech industry. ```


[1] https://docs.llamaindex.ai/en/latest/module_guides/deploying/agents/