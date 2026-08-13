# developers.llamaindex.ai/python/framework/integrations/llm/huggingface/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/huggingface/index.md

--- title: Hugging Face LLMs | Developer Documentation ---

There are many ways to interface with LLMs from Hugging Face [1], either locally or via Hugging Face’s Inference Providers [2]. Hugging Face itself provides several Python packages to enable access, which LlamaIndex wraps into `LLM` entities:
- The `transformers` [3] package: use `llama_index.llms.HuggingFaceLLM` - The Hugging Face Inference Providers [2], wrapped by `huggingface_hub[inference]` [4]: use `llama_index.llms.HuggingFaceInferenceAPI`
There are *many* possible permutations of these two, so this notebook only details a few. Let’s use Hugging Face’s Text Generation task [5] as our example.
In the below line, we install the packages necessary for this demo:
- `transformers[torch]` is needed for `HuggingFaceLLM` - `huggingface_hub[inference]` is needed for `HuggingFaceInferenceAPI` - The quotes are needed for Z shell (`zsh`)
``` %pip install llama-index-llms-huggingface # for local inference %pip install llama-index-llms-huggingface-api # for remote inference ```

``` !pip install "transformers[torch]" "huggingface_hub[inference]" ```

If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` !pip install llama-index ```
Now that we’re set up, let’s play around:
# Setup Hugging Face Account
First, you need to create a Hugging Face account and get a token. You can sign up here [6]. Then you’ll need to create a token here [7].
Terminal window
``` export HUGGING_FACE_TOKEN=hf_your_token_here ```
``` import os from typing import List, Optional

from llama_index.llms.huggingface import HuggingFaceLLM from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
HF_TOKEN: Optional[str] = os.getenv("HUGGING_FACE_TOKEN") # NOTE: None default will fall back on Hugging Face's token storage # when this token gets used within HuggingFaceInferenceAPI ```

## Use a model via Inference Providers
The easiest way to use an open source model is to use the Hugging Face Inference Providers [2]. Let’s use the DeepSeek R1 model, which is great for complex tasks.
With inference providers, you can use the model on serverless infrastructure from inference providers.
``` remotely_run = HuggingFaceInferenceAPI( model_name="deepseek-ai/DeepSeek-R1-0528", token=HF_TOKEN, provider="auto", # this will use the best provider available ) ```

We can also specify our preferred inference provider. Let’s use the `together` provider [8].
``` remotely_run = HuggingFaceInferenceAPI( model_name="Qwen/Qwen3-235B-A22B", token=HF_TOKEN, provider="together", # this will use the best provider available ) ```

## Use an open source model locally
First, we’ll use an open source model that’s optimized for local inference. This model is downloaded (if first invocation) to the local Hugging Face model cache, and actually runs the model on your local machine’s hardware.
We’ll use the Gemma 3N E4B [9] model, which is optimized for local inference.
``` locally_run = HuggingFaceLLM(model_name="google/gemma-3n-E4B-it") ```
## Use a dedicated Inference Endpoint
We can also spin up a dedicated Inference Endpoint for a model and use that to run the model.
``` endpoint_server = HuggingFaceInferenceAPI( model="https://(<your-endpoint>.eu-west-1.aws.endpoints.huggingface.cloud" ) ```

## Use a local inference engine (vLLM or TGI)
We can also use a local inference engine like vLLM [10] or TGI [11] to run the model.
``` # You can also connect to a model being served by a local or remote # Text Generation Inference server tgi_server = HuggingFaceInferenceAPI(model="http://localhost:8080") ```

Underlying a completion with `HuggingFaceInferenceAPI` is Hugging Face’s Text Generation task [5].
``` completion_response = remotely_run_recommended.complete("To infinity, and") print(completion_response) ```

``` beyond! The Infinity Wall Clock is a unique and stylish way to keep track of time. The clock is made of a durable, high-quality plastic and features a bright LED display. The Infinity Wall Clock is powered by batteries and can be mounted on any wall. It is a great addition to any home or office. ```

## Setting a tokenizer
If you are modifying the LLM, you should also change the global tokenizer to match!
``` from llama_index.core import set_global_tokenizer from transformers import AutoTokenizer

set_global_tokenizer( AutoTokenizer.from_pretrained("HuggingFaceH4/zephyr-7b-alpha").encode ) ```

If you’re curious, other Hugging Face Inference API tasks wrapped are:
- `llama_index.llms.HuggingFaceInferenceAPI.chat`: Conversational task [12] - `llama_index.embeddings.HuggingFaceInferenceAPIEmbedding`: Feature Extraction task [13]
And yes, Hugging Face embedding models are supported with:
- `transformers[torch]`: wrapped by `HuggingFaceEmbedding` - `huggingface_hub[inference]`: wrapped by `HuggingFaceInferenceAPIEmbedding`
Both of the above two subclass `llama_index.embeddings.base.BaseEmbedding`.

[1] https://huggingface.co/
[2] https://huggingface.co/docs/inference-providers
[3] https://github.com/huggingface/transformers
[4] https://github.com/huggingface/huggingface_hub
[5] https://huggingface.co/tasks/text-generation
[6] https://huggingface.co/join
[7] https://huggingface.co/settings/tokens
[8] https://huggingface.co/togethercomputer
[9] https://huggingface.co/google/gemma-3n-E4B-it
[10] https://github.com/vllm-project/vllm
[11] https://github.com/huggingface/text-generation-inference
[12] https://huggingface.co/tasks/conversational
[13] https://huggingface.co/tasks/feature-extraction