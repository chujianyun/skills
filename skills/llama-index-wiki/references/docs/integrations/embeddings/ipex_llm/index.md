# developers.llamaindex.ai/python/framework/integrations/embeddings/ipex_llm/index.md
> https://developers.llamaindex.ai/python/framework/integrations/embeddings/ipex_llm/index.md

--- title: Local Embeddings with IPEX-LLM on Intel CPU | Developer Documentation ---

> IPEX-LLM [1] is a PyTorch library for running LLM on Intel CPU and GPU (e.g., local PC with iGPU, discrete GPU such as Arc, Flex and Max) with very low latency.
This example goes over how to use LlamaIndex to conduct embedding tasks with `ipex-llm` optimizations on Intel CPU. This would be helpful in applications such as RAG, document QA, etc.
> **Note** > > You could refer to here [2] for full examples of `IpexLLMEmbedding`. Please note that for running on Intel CPU, please specify `-d 'cpu'` in command argument when running the examples.

## Install `llama-index-embeddings-ipex-llm`
This will also install `ipex-llm` and its dependencies.
``` %pip install llama-index-embeddings-ipex-llm ```
## `IpexLLMEmbedding`
``` from llama_index.embeddings.ipex_llm import IpexLLMEmbedding
embedding_model = IpexLLMEmbedding(model_name="BAAI/bge-large-en-v1.5") ```
> Please note that `IpexLLMEmbedding` currently only provides optimization for Hugging Face Bge models.
``` sentence = "IPEX-LLM is a PyTorch library for running LLM on Intel CPU and GPU (e.g., local PC with iGPU, discrete GPU such as Arc, Flex and Max) with very low latency." query = "What is IPEX-LLM?"

text_embedding = embedding_model.get_text_embedding(sentence) print(f"embedding[:10]: {text_embedding[:10]}")
text_embeddings = embedding_model.get_text_embedding_batch([sentence, query]) print(f"text_embeddings[0][:10]: {text_embeddings[0][:10]}") print(f"text_embeddings[1][:10]: {text_embeddings[1][:10]}")

query_embedding = embedding_model.get_query_embedding(query) print(f"query_embedding[:10]: {query_embedding[:10]}") ```
``` Batches: 0%| | 0/1 [00:00<?, ?it/s]

embedding[:10]: [0.03578318655490875, 0.032746609300374985, -0.016696255654096603, 0.0074520050548017025, 0.016294749453663826, -0.001968140248209238, -0.002897330094128847, -0.041390497237443924, 0.030955366790294647, 0.05438097193837166]

text_embeddings[0][:10]: [0.03578318655490875, 0.032746609300374985, -0.016696255654096603, 0.0074520050548017025, 0.016294749453663826, -0.001968140248209238, -0.002897330094128847, -0.041390497237443924, 0.030955366790294647, 0.05438097193837166] text_embeddings[1][:10]: [0.03155018016695976, 0.03177601844072342, -0.00304483063519001, 0.004364349413663149, 0.005002604331821203, -0.02680951915681362, -0.005840071476995945, -0.022466979920864105, 0.05162270367145538, 0.05928812175989151]

Batches: 0%| | 0/1 [00:00<?, ?it/s]

query_embedding[:10]: [0.053250256925821304, 0.0036771567538380623, 0.003390512429177761, 0.014903719536960125, -0.00263631297275424, -0.022365037351846695, -0.004524332471191883, -0.018143195658922195, 0.03799865022301674, 0.07393667846918106] ```

[1] https://github.com/intel-analytics/ipex-llm/
[2] https://github.com/run-llama/llama_index/tree/main/llama-index-integrations/embeddings/llama-index-embeddings-ipex-llm/examples