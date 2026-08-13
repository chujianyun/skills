# developers.llamaindex.ai/python/framework/integrations/embeddings/ipex_llm_gpu/index.md
> https://developers.llamaindex.ai/python/framework/integrations/embeddings/ipex_llm_gpu/index.md

--- title: Local Embeddings with IPEX-LLM on Intel GPU | Developer Documentation ---

> IPEX-LLM [1] is a PyTorch library for running LLM on Intel CPU and GPU (e.g., local PC with iGPU, discrete GPU such as Arc, Flex and Max) with very low latency.
This example goes over how to use LlamaIndex to conduct embedding tasks with `ipex-llm` optimizations on Intel GPU. This would be helpful in applications such as RAG, document QA, etc.
> **Note** > > You could refer to here [2] for full examples of `IpexLLMEmbedding`. Please note that for running on Intel GPU, please specify `-d 'xpu'` or `-d 'xpu:<device_id>'` in command argument when running the examples.

## Install Prerequisites
To benefit from IPEX-LLM on Intel GPUs, there are several prerequisite steps for tools installation and environment preparation.
If you are a Windows user, visit the Install IPEX-LLM on Windows with Intel GPU Guide [3], and follow [**Install Prerequisites**] [4] to update GPU driver (optional) and install Conda.
If you are a Linux user, visit the Install IPEX-LLM on Linux with Intel GPU [5], and follow **Install Prerequisites** [6] to install GPU driver, Intel® oneAPI Base Toolkit 2024.0, and Conda.
## Install `llama-index-embeddings-ipex-llm`
After the prerequisites installation, you should have created a conda environment with all prerequisites installed, activate your conda environment and install `llama-index-embeddings-ipex-llm` as follows:

``` conda activate <your-conda-env-name>
pip install llama-index-embeddings-ipex-llm[xpu] --extra-index-url https://pytorch-extension.intel.com/release-whl/stable/xpu/us/ ```
This step will also install `ipex-llm` and its dependencies.
> **Note** > > You can also use `https://pytorch-extension.intel.com/release-whl/stable/xpu/cn/` as the `extra-indel-url`.
## Runtime Configuration
For optimal performance, it is recommended to set several environment variables based on your device:
### For Windows Users with Intel Core Ultra integrated GPU
In Anaconda Prompt:
``` set SYCL_CACHE_PERSISTENT=1 set BIGDL_LLM_XMX_DISABLED=1 ```

### For Linux Users with Intel Arc A-Series GPU
Terminal window
``` # Configure oneAPI environment variables. Required step for APT or offline installed oneAPI. # Skip this step for PIP-installed oneAPI since the environment has already been configured in LD_LIBRARY_PATH. source /opt/intel/oneapi/setvars.sh

# Recommended Environment Variables for optimal performance export USE_XETLA=OFF export SYCL_PI_LEVEL_ZERO_USE_IMMEDIATE_COMMANDLISTS=1 export SYCL_CACHE_PERSISTENT=1 ```

> **Note** > > For the first time that each model runs on Intel iGPU/Intel Arc A300-Series or Pro A60, it may take several minutes to compile. > > For other GPU type, please refer to here [7] for Windows users, and here [8] for Linux users.

## `IpexLLMEmbedding`
Setting `device="xpu"` when initializing `IpexLLMEmbedding` will put the embedding model on Intel GPU and benefit from IPEX-LLM optimizations:
``` from llama_index.embeddings.ipex_llm import IpexLLMEmbedding
embedding_model = IpexLLMEmbedding( model_name="BAAI/bge-large-en-v1.5", device="xpu" ) ```

> Please note that `IpexLLMEmbedding` currently only provides optimization for Hugging Face Bge models. > > If you have multiple Intel GPUs available, you could set `device="xpu:<device_id>"`, in which `device_id` is counted from 0. `device="xpu"` is equal to `device="xpu:0"` by default.
You could then conduct the embedding tasks as normal:
``` sentence = "IPEX-LLM is a PyTorch library for running LLM on Intel CPU and GPU (e.g., local PC with iGPU, discrete GPU such as Arc, Flex and Max) with very low latency." query = "What is IPEX-LLM?"

text_embedding = embedding_model.get_text_embedding(sentence) print(f"embedding[:10]: {text_embedding[:10]}")
text_embeddings = embedding_model.get_text_embedding_batch([sentence, query]) print(f"text_embeddings[0][:10]: {text_embeddings[0][:10]}") print(f"text_embeddings[1][:10]: {text_embeddings[1][:10]}")

query_embedding = embedding_model.get_query_embedding(query) print(f"query_embedding[:10]: {query_embedding[:10]}") ```

[1] https://github.com/intel-analytics/ipex-llm/
[2] https://github.com/run-llama/llama_index/tree/main/llama-index-integrations/embeddings/llama-index-embeddings-ipex-llm/examples
[3] https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Quickstart/install_windows_gpu.html
[4] https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Quickstart/install_windows_gpu.html#install-prerequisites
[5] https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Quickstart/install_linux_gpu.html
[6] https://ipex- llm.readthedocs.io/en/latest/doc/LLM/Quickstart/install_linux_gpu.html#install-prerequisites
[7] https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Overview/install_gpu.html#runtime-configuration
[8] https://ipex- llm.readthedocs.io/en/latest/doc/LLM/Overview/install_gpu.html#id5