# developers.llamaindex.ai/python/framework/integrations/llm/oci_data_science/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/oci_data_science/index.md

--- title: Oracle Cloud Infrastructure Data Science | Developer Documentation ---

Oracle Cloud Infrastructure (OCI) Data Science [1] is a fully managed, serverless platform for data science teams to build, train, and manage machine learning models in Oracle Cloud Infrastructure.

It offers AI Quick Actions [2], which can be used to deploy, evaluate, and fine-tune foundation LLM models in OCI Data Science. AI Quick Actions target users who want to quickly leverage the capabilities of AI. They aim to expand the reach of foundation models to a broader set of users by providing a streamlined, code-free, and efficient environment for working with foundation models. AI Quick Actions can be accessed from the Data Science Notebook.

Detailed documentation on how to deploy LLM models in OCI Data Science using AI Quick Actions is available here [3] and here [4].

This notebook explains how to use OCI’s Data Science models with LlamaIndex.
## Setup
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-llms-oci-data-science ```
``` !pip install llama-index ```
You will also need to install the oracle-ads [5] SDK.
``` !pip install -U oracle-ads ```
## Authentication

The authentication methods supported for LlamaIndex are equivalent to those used with other OCI services and follow the standard SDK authentication methods, specifically API Key, session token, instance principal, and resource principal. More details can be found here [6]. Make sure to have the required policies [7] to access the OCI Data Science Model Deployment endpoint. The oracle-ads [5] helps to simplify the authentication within OCI Data Science.

## Basic Usage

Using LLMs offered by OCI Data Science AI with LlamaIndex only requires you to initialize the `OCIDataScience` interface with your Data Science Model Deployment endpoint and model ID. By default the all deployed models in AI Quick Actions get `odsc-model` ID. However this ID cna be changed during the deployment.

#### Call `complete` with a prompt

llm = OCIDataScience( model="odsc-llm", endpoint="https://<MD_OCID>/predict", ) response = llm.complete("Tell me a joke")

### Call `chat` with a list of messages

llm = OCIDataScience( model="odsc-llm", endpoint="https://<MD_OCID>/predict", ) response = llm.chat( [ ChatMessage(role="user", content="Tell me a joke"), ChatMessage( role="assistant", content="Why did the chicken cross the road?" ), ChatMessage(role="user", content="I don't know, why?"), ] )

## Streaming
**Using Dedicated Streaming endpoint**
``` from llama_index.llms.oci_data_science import OCIDataScience import ads

ads.set_auth(auth="security_token", profile="OC1")
llm = OCIDataScience( endpoint="https://<MD_OCID>/predictWithResponseStream", model="odsc-llm", )

prompt = "What is the capital of France?" response = llm.stream_complete(prompt) for chunk in response: print(chunk.delta, end="") ```

### Using `stream_complete` endpoint

for chunk in llm.stream_complete("Tell me a joke"): print(chunk.delta, end="") ```
### Using `stream_chat` endpoint

llm = OCIDataScience( model="odsc-llm", endpoint="https://<MD_OCID>/predict", ) response = llm.stream_chat( [ ChatMessage(role="user", content="Tell me a joke"), ChatMessage( role="assistant", content="Why did the chicken cross the road?" ), ChatMessage(role="user", content="I don't know, why?"), ] )

for chunk in response: print(chunk.delta, end="") ```
## Async
### Call `acomplete` with a prompt

llm = OCIDataScience( model="odsc-llm", endpoint="https://<MD_OCID>/predict", ) response = await llm.acomplete("Tell me a joke")

### Call `achat` with a list of messages

llm = OCIDataScience( model="odsc-llm", endpoint="https://<MD_OCID>/predict", ) response = await llm.achat( [ ChatMessage(role="user", content="Tell me a joke"), ChatMessage( role="assistant", content="Why did the chicken cross the road?" ), ChatMessage(role="user", content="I don't know, why?"), ] )

### Using `astream_complete` endpoint

llm = OCIDataScience( model="odsc-llm", endpoint="https://<MD_OCID>/predict", )

async for chunk in await llm.astream_complete("Tell me a joke"): print(chunk.delta, end="") ```
### Using `astream_chat` endpoint
``` import ads from llama_index.llms.oci_data_science import OCIDataScience from llama_index.core.base.llms.types import ChatMessage

llm = OCIDataScience( model="odsc-llm", endpoint="https://<MD_OCID>/predict", ) response = await llm.stream_chat( [ ChatMessage(role="user", content="Tell me a joke"), ChatMessage( role="assistant", content="Why did the chicken cross the road?" ), ChatMessage(role="user", content="I don't know, why?"), ] )

async for chunk in response: print(chunk.delta, end="") ```
## Configure Model
``` import ads from llama_index.llms.oci_data_science import OCIDataScience

llm = OCIDataScience( model="odsc-llm", endpoint="https://<MD_OCID>/predict", temperature=0.2, max_tokens=500, timeout=120, context_window=2500, additional_kwargs={ "top_p": 0.75, "logprobs": True, "top_logprobs": 3, }, ) response = llm.chat( [ ChatMessage(role="user", content="Tell me a joke"), ] ) print(response) ```
## Function Calling

The AI Quick Actions [2] offers prebuilt service containers that make deploying and serving a large language model very easy. Either one of vLLM (a high-throughput and memory-efficient inference and serving engine for LLMs) or TGI (a high-performance text generation server for the popular open-source LLMs) is used in the service container to host the model, the end point created supports the OpenAI API protocol. This allows the model deployment to be used as a drop-in replacement for applications using OpenAI API. If the deployed model supports function calling, then integration with LlamaIndex tools, through the predict\_and\_call function on the llm allows to attach any tools and let the LLM decide which tools to call (if any).

``` import ads from llama_index.llms.oci_data_science import OCIDataScience from llama_index.core.tools import FunctionTool

response = llm.predict_and_call( [multiply_tool, add_tool, sub_tool, divide_tool], user_msg="Calculate the result of `8 + 2 - 6`.", verbose=True, )

### Using `FunctionAgent`
``` import ads from llama_index.llms.oci_data_science import OCIDataScience from llama_index.core.tools import FunctionTool from llama_index.core.agent.workflow import FunctionAgent
ads.set_auth(auth="security_token", profile="<replace-with-your-profile>")
llm = OCIDataScience( model="odsc-llm", endpoint="https://<MD_OCID>/predict", temperature=0.2, max_tokens=500, timeout=120, context_window=2500, additional_kwargs={ "top_p": 0.75, "logprobs": True, "top_logprobs": 3, }, )

def multiply(a: float, b: float) -> float: print(f"---> {a} * {b}") return a * b
def add(a: float, b: float) -> float: print(f"---> {a} + {b}") return a + b
def subtract(a: float, b: float) -> float: print(f"---> {a} - {b}") return a - b
def divide(a: float, b: float) -> float: print(f"---> {a} / {b}") return a / b
multiply_tool = FunctionTool.from_defaults(fn=multiply) add_tool = FunctionTool.from_defaults(fn=add) sub_tool = FunctionTool.from_defaults(fn=subtract) divide_tool = FunctionTool.from_defaults(fn=divide)
agent = FunctionAgent( tools=[multiply_tool, add_tool, sub_tool, divide_tool], llm=llm, ) response = await agent.run( "Calculate the result of `8 + 2 - 6`. Use tools. Return the calculated result." )
print(response) ```

[1] https://www.oracle.com/artificial-intelligence/data-science
[2] https://docs.oracle.com/en-us/iaas/data-science/using/ai-quick-actions.htm
[3] https://github.com/oracle-samples/oci-data-science-ai-samples/blob/main/ai-quick-actions/model-deployment- tips.md
[4] https://docs.oracle.com/en-us/iaas/data-science/using/ai-quick-actions-model-deploy.htm
[5] https://accelerated-data-science.readthedocs.io/en/latest/index.html
[6] https://accelerated-data-science.readthedocs.io/en/latest/user_guide/cli/authentication.html
[7] https://docs.oracle.com/en- us/iaas/data-science/using/model-dep-policies-auth.htm