# developers.llamaindex.ai/python/framework/integrations/llm/sagemaker_endpoint_llm/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/sagemaker_endpoint_llm/index.md

--- title: Interacting with LLM deployed in Amazon SageMaker Endpoint with LlamaIndex | Developer Documentation ---

An Amazon SageMaker endpoint is a fully managed resource that enables the deployment of machine learning models, specifically LLM (Large Language Models), for making predictions on new data.
This notebook demonstrates how to interact with LLM endpoints using `SageMakerLLM`, unlocking additional llamaIndex features. So, It is assumed that an LLM is deployed on a SageMaker endpoint.
## Setting Up
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-llms-sagemaker-endpoint ```
``` ! pip install llama-index ```
You have to specify the endpoint name to interact with.
``` ENDPOINT_NAME = "<-YOUR-ENDPOINT-NAME->" ```
Credentials should be provided to connect to the endpoint. You can either:
- use an AWS profile by specifying the `profile_name` parameter, if not specified, the default credential profile will be used. - Pass credentials as parameters (`aws_access_key_id`, `aws_secret_access_key`, `aws_session_token`, `region_name`).
for more details check this link [1].
**AWS profile name**

[Column 1]
AWS_ACCESS_KEY_ID = "<-YOUR-AWS-ACCESS-KEY-ID->" AWS_SECRET_ACCESS_KEY = "<-YOUR-AWS-SECRET-ACCESS-KEY->" AWS_SESSION_TOKEN = "<-YOUR-AWS-SESSION-TOKEN->" REGION_NAME = "<-YOUR-ENDPOINT-REGION-NAME->" ```

``` llm = SageMakerLLM( endpoint_name=ENDPOINT_NAME, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, aws_session_token=AWS_SESSION_TOKEN, region_name=REGION_NAME, ) ```

**With credentials**:
``` from llama_index.llms.sagemaker_endpoint import SageMakerLLM
ENDPOINT_NAME = "<-YOUR-ENDPOINT-NAME->" PROFILE_NAME = "<-YOUR-PROFILE-NAME->" llm = SageMakerLLM( endpoint_name=ENDPOINT_NAME, profile_name=PROFILE_NAME ) # Omit the profile name to use the default profile ```

## Basic Usage
### Call `complete` with a prompt
``` resp = llm.complete( "Paul Graham is ", formatted=True ) # formatted=True to avoid adding system prompt print(resp) ```

### Call `chat` with a list of messages

[Column 2]
``` 66 years old (birthdate: September 4, 1951). He is a British-American computer scientist, programmer, and entrepreneur who is known for his work in the fields of artificial intelligence, machine learning, and computer vision. He is a professor emeritus at Stanford University and a researcher at the Stanford Artificial Intelligence Lab (SAIL).
Graham has made significant contributions to the field of computer science, including the development of the concept of "n-grams," which are sequences of n items that occur together in a dataset. He has also worked on the development of machine learning algorithms and has written extensively on the topic of machine learning.
Graham has received numerous awards for his work, including the Association for Computing Machinery (ACM) A.M. Turing Award, the IEEE Neural Networks Pioneer Award, and the IJCAI Award ```


messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="What is your name"), ] resp = llm.chat(messages) ```

``` print(resp) ```
``` assistant: Arrrr, shiver me timbers! *adjusts eye patch* Me name be Cap'n Blackbeak, the most feared and infamous pirate on the seven seas! *winks*
*ahem* But enough about me, matey. What be bringin' ye to these fair waters? Are ye here to plunder some booty, or just to share a pint o' grog with a salty old sea dog like meself? *chuckles* ```
### Streaming
#### Using `stream_complete` endpoint
``` resp = llm.stream_complete("Paul Graham is ", formatted=True) ```
``` for r in resp: print(r.delta) ```

``` 64 today. He’s a computer sci ist, entrepreneur, and writer, best known for his work in the fields of artificial intelligence, machine learning, and computer graphics. Graham was born in 1956 in Boston, Massachusetts. He earned his Bachelor’s degree in Computer Science from Harvard University in 1978 and his PhD in Computer Science from the University of California, Berkeley in 1982. Graham’s early work focused on the development of the first computer graphics systems that could generate photorealistic images. In the 1980s, he became interested in the field of artificial intelligence and machine learning, and he co-founded a number of companies to explore these areas, including Viaweb, which was one of the first commercial web hosting services. Graham is also a prolific writer and has published a number of influential essays on topics such as the nature

```
#### Using `stream_chat` endpoint
``` from llama_index.core.llms import ChatMessage
messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="What is your name"), ] resp = llm.stream_chat(messages) ```

``` for r in resp: print(r.delta, end="") ```

``` ARRGH! *adjusts eye patch* Me hearty? *winks* Me name be Captain Blackbeak, the most feared and infamous pirate to ever sail the seven seas! *chuckles* Or, at least, that's what me matey mates tell me. *winks*
So, what be bringin' ye to these waters, matey? Are ye here to plunder some booty or just to hear me tales of the high seas? *grins* Either way, I be ready to share me treasure with ye! *winks* Just don't be tellin' any landlubbers about me hidden caches o' gold, or ye might be walkin' the plank, savvy? *winks* ```
## Configure Model
`SageMakerLLM` is an abstraction for interacting with different language models (LLM) deployed in Amazon SageMaker. All the default parameters are compatible with the Llama 2 model. Therefore, if you are using a different model, you will likely need to set the following parameters:
- `messages_to_prompt`: A callable that accepts a list of `ChatMessage` objects and, if not specified in the message, a system prompt. It should return a string containing the messages in the endpoint LLM-compatible format.
- `completion_to_prompt`: A callable that accepts a completion string with a system prompt and returns a string in the endpoint LLM-compatible format.
- `content_handler`: A class that inherits from `llama_index.llms.sagemaker_llm_endpoint_utils.BaseIOHandler` and implements the following methods: `serialize_input`, `deserialize_output`, `deserialize_streaming_output`, and `remove_prefix`.

[1] https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html