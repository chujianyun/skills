# developers.llamaindex.ai/python/framework/integrations/llm/openvino-genai/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/openvino-genai/index.md

--- title: OpenVINO GenAI LLMs | Developer Documentation ---

OpenVINO™ [1] is an open-source toolkit for optimizing and deploying AI inference. OpenVINO™ Runtime can enable running the same model optimized across various hardware [devices] [2]. Accelerate your deep learning performance across use cases like: language + LLMs, computer vision, automatic speech recognition, and more.
`OpenVINOGenAILLM` is a wrapper of OpenVINO-GenAI API [3]. OpenVINO models can be run locally through this entitiy wrapped by LlamaIndex :
In the below line, we install the packages necessary for this demo:
``` %pip install llama-index-llms-openvino-genai ```
``` %pip install optimum[openvino] ```
Now that we’re set up, let’s play around:
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` !pip install llama-index ```
``` from llama_index.llms.openvino_genai import OpenVINOGenAILLM ```
``` /home2/ethan/intel/llama_index/llama_test/lib/python3.10/site-packages/pydantic/_internal/_fields.py:132: UserWarning: Field "model_path" in OpenVINOGenAILLM has conflict with protected namespace "model_".
You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ()`. warnings.warn( ```
### Model Exporting
It is possible to export your model [4] to the OpenVINO IR format with the CLI, and load the model from local folder.
``` !optimum-cli export openvino --model microsoft/Phi-3-mini-4k-instruct --task text-generation-with-past --weight-format int4 model_path ```
You can download a optimized IR model from OpenVINO model hub of Hugging Face.
``` import huggingface_hub as hf_hub
model_id = "OpenVINO/Phi-3-mini-4k-instruct-int4-ov" model_path = "Phi-3-mini-4k-instruct-int4-ov"
hf_hub.snapshot_download(model_id, local_dir=model_path) ```
``` Fetching 17 files: 0%| | 0/17 [00:00<?, ?it/s]

'/home2/ethan/intel/llama_index/docs/examples/llm/Phi-3-mini-4k-instruct-int4-ov' ```
### Model Loading
Models can be loaded by specifying the model parameters using the `OpenVINOGenAILLM` method.
If you have an Intel GPU, you can specify `device="gpu"` to run inference on it.
``` ov_llm = OpenVINOGenAILLM( model_path=model_path, device="CPU", ) ```

You can pass the generation config parameters through `ov_llm.config`. The supported parameters are listed at the [openvino\_genai.GenerationConfig] [5].
``` ov_llm.config.max_new_tokens = 100 ```
``` response = ov_llm.complete("What is the meaning of life?") print(str(response)) ```

``` # Answer The meaning of life is a profound and complex question that has been debated by philosophers, theologians, scientists, and thinkers throughout history. Different cultures, religions, and individuals have their own interpretations and beliefs about what gives life purpose and significance.

From a philosophical standpoint, existentialists like Jean-Paul Sartre and Albert Camus have argued that life inherently has no meaning, and it is ```
### Streaming
Using `stream_complete` endpoint
``` response = ov_llm.stream_complete("Who is Paul Graham?") for r in response: print(r.delta, end="") ```

``` Paul Graham is a computer scientist and entrepreneur who is best known for founding the startup accelerator program Y Combinator. He is also the founder of the web development company Viaweb, which was acquired by PayPal for $497 million in 1raneworks.

What is Y Combinator?
Y Combinator is a startup accelerator program that provides funding, mentorship, and resources to early-stage start ```
Using `stream_chat` endpoint
``` from llama_index.core.llms import ChatMessage
messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage(role="user", content="What is your name"), ] resp = ov_llm.stream_chat(messages)

for r in resp: print(r.delta, end="") ```
``` I'm Phi, Microsoft's AI assistant. How can I assist you today? ```
For more information refer to:
- OpenVINO LLM guide [6].
- OpenVINO Documentation [7].
- OpenVINO Get Started Guide [8].
- RAG example with LlamaIndex [9].

[1] https://github.com/openvinotoolkit/openvino
[2] https://github.com/openvinotoolkit/openvino?tab=readme-ov-file#supported-hardware-matrix
[3] https://github.com/openvinotoolkit/openvino.genai
[4] https://github.com/huggingface/optimum-intel?tab=readme-ov-file#export
[5] https://docs.openvino.ai/2024/api/genai_api/_autosummary/openvino_genai.GenerationConfig.html
[6] https://docs.openvino.ai/2024/learn-openvino/llm_inference_guide.html
[7] https://docs.openvino.ai/2024/home.html
[8] https://www.intel.com/content/www/us/en/content-details/819067/openvino-get-started-guide.html
[9] https://github.com/openvinotoolkit/openvino_notebooks/tree/latest/notebooks/llm-rag-llamaindex