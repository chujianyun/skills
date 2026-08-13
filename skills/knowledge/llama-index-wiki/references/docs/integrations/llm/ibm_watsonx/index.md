# developers.llamaindex.ai/python/framework/integrations/llm/ibm_watsonx/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/ibm_watsonx/index.md

--- title: IBM watsonx.ai | Developer Documentation ---

> WatsonxLLM is a wrapper for IBM watsonx.ai [1] foundation models.
The aim of these examples is to show how to communicate with `watsonx.ai` models using the `LlamaIndex` LLMs API.
## Setting up
Install the `llama-index-llms-ibm` package:
``` !pip install -qU llama-index-llms-ibm ```
The cell below defines the credentials required to work with watsonx Foundation Model inferencing.
**Action:** Provide the IBM Cloud user API key. For details, see Managing user API keys [2].
``` import os from getpass import getpass

watsonx_api_key = getpass() os.environ["WATSONX_APIKEY"] = watsonx_api_key ```
Additionally, you can pass additional secrets as an environment variable:
``` import os
os.environ["WATSONX_URL"] = "your service instance url" os.environ["WATSONX_TOKEN"] = "your token for accessing the CPD cluster" os.environ["WATSONX_PASSWORD"] = "your password for accessing the CPD cluster" os.environ["WATSONX_USERNAME"] = "your username for accessing the CPD cluster" os.environ[ "WATSONX_INSTANCE_ID" ] = "your instance_id for accessing the CPD cluster" ```

## Load the model
You might need to adjust model `parameters` for different models or tasks. For details, refer to Available MetaNames [3].
``` temperature = 0.5 max_new_tokens = 50 additional_params = { "decoding_method": "sample", "min_new_tokens": 1, "top_k": 50, "top_p": 1, } ```

Initialize the `WatsonxLLM` class with the previously set parameters.
**Note**:
- To provide context for the API call, you must pass the `project_id` or `space_id`. To get your project or space ID, open your project or space, go to the **Manage** tab, and click **General**. For more information see: Project documentation [4] or Deployment space documentation [5]. - Depending on the region of your provisioned service instance, use one of the urls listed in watsonx.ai API Authentication [6].
In this example, we’ll use the `project_id` and Dallas URL.
You need to specify the `model_id` that will be used for inferencing. You can find the list of all the available models in Supported foundation models [7].
``` from llama_index.llms.ibm import WatsonxLLM
watsonx_llm = WatsonxLLM( model_id="ibm/granite-13b-instruct-v2", url="https://us-south.ml.cloud.ibm.com", project_id="PASTE YOUR PROJECT_ID HERE", temperature=temperature, max_new_tokens=max_new_tokens, additional_params=additional_params, ) ```

Alternatively, you can use Cloud Pak for Data credentials. For details, see watsonx.ai software setup [8].
``` watsonx_llm = WatsonxLLM( model_id="ibm/granite-13b-instruct-v2", url="PASTE YOUR URL HERE", username="PASTE YOUR USERNAME HERE", password="PASTE YOUR PASSWORD HERE", instance_id="openshift", version="4.8", project_id="PASTE YOUR PROJECT_ID HERE", temperature=temperature, max_new_tokens=max_new_tokens, additional_params=additional_params, ) ```

Instead of `model_id`, you can also pass the `deployment_id` of the previously tuned model. The entire model tuning workflow is described in Working with TuneExperiment and PromptTuner [9].
``` watsonx_llm = WatsonxLLM( deployment_id="PASTE YOUR DEPLOYMENT_ID HERE", url="https://us-south.ml.cloud.ibm.com", project_id="PASTE YOUR PROJECT_ID HERE", temperature=temperature, max_new_tokens=max_new_tokens, additional_params=additional_params, ) ```

## Create a Completion
Call the model directly using a string type prompt:
``` response = watsonx_llm.complete("What is a Generative AI?") print(response) ```

``` A generative AI is a computer program that can create new text, images, or other types of content. These programs are trained on large datasets of existing content, and they use that data to generate new content that is similar to the training data. ```

From the `CompletionResponse`, you can also retrieve a raw response returned by the service:
``` print(response.raw) ```
``` {'model_id': 'ibm/granite-13b-instruct-v2', 'created_at': '2024-05-20T07:11:57.984Z', 'results': [{'generated_text': 'A generative AI is a computer program that can create new text, images, or other types of content. These programs are trained on large datasets of existing content, and they use that data to generate new content that is similar to the training data.', 'generated_token_count': 50, 'input_token_count': 7, 'stop_reason': 'max_tokens', 'seed': 494448017}]}
```
You can also call a model that provides a prompt template:
``` from llama_index.core import PromptTemplate
template = "What is {object} and how does it work?" prompt_template = PromptTemplate(template=template)
prompt = prompt_template.format(object="a loan")
response = watsonx_llm.complete(prompt) print(response) ```
``` A loan is a sum of money that is borrowed to buy something, such as a house or a car. The borrower must repay the loan plus interest. The interest is a fee charged for using the money. The interest rate is the amount of ```
## Calling `chat` with a list of messages
Create `chat` completions by providing a list of messages:
``` from llama_index.core.llms import ChatMessage
messages = [ ChatMessage(role="system", content="You are an AI assistant"), ChatMessage(role="user", content="Who are you?"), ] response = watsonx_llm.chat( messages, max_new_tokens=20, decoding_method="greedy" ) print(response) ```

``` assistant: I am an AI assistant. ```
Note that we changed the `max_new_tokens` parameter to `20` and the `decoding_method` parameter to `greedy`.
## Streaming the model output
Stream the model’s response:
``` for chunk in watsonx_llm.stream_complete( "Describe your favorite city and why it is your favorite." ): print(chunk.delta, end="") ```

``` I like New York because it is the city of dreams. You can achieve anything you want here. ```
Similarly, to stream the `chat` completions, use the following code:
``` messages = [ ChatMessage(role="system", content="You are an AI assistant"), ChatMessage(role="user", content="Who are you?"), ]

for chunk in watsonx_llm.stream_chat(messages): print(chunk.delta, end="") ```
``` I am an AI assistant. ```

[1] https://www.ibm.com/products/watsonx-ai
[2] https://cloud.ibm.com/docs/account?topic=account-userapikey\&interface=ui
[3] https://ibm.github.io/watsonx-ai-python-sdk/fm_model.html#metanames.GenTextParamsMetaNames
[4] https://www.ibm.com/docs/en/watsonx-as-a-service?topic=projects
[5] https://www.ibm.com/docs/en/watsonx/saas?topic=spaces-creating-deployment
[6] https://ibm.github.io/watsonx-ai-python-sdk/setup_cloud.html#authentication
[7] https://ibm.github.io/watsonx-ai-python- sdk/fm_model.html#ibm_watsonx_ai.foundation_models.utils.enums.ModelTypes
[8] https://ibm.github.io/watsonx-ai-python-sdk/setup_cpd.html
[9] https://ibm.github.io/watsonx-ai- python-sdk/pt_working_with_class_and_prompt_tuner.html