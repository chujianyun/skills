# developers.llamaindex.ai/python/framework/integrations/embeddings/optimum_intel/index.md
> https://developers.llamaindex.ai/python/framework/integrations/embeddings/optimum_intel/index.md

--- title: Optimized Embedding Model using Optimum-Intel | Developer Documentation ---

LlamaIndex has support for loading quantized embedding models for Intel, using the Optimum-Intel library [1].
Optimized models are smaller and faster, with minimal accuracy loss, see the documentation [2] and an [optimization guide] [2] using the IntelLabs/fastRAG library.
Optimization is based on math instructions in the Xeon® 4th generation or newer processors.
In order to be able to load and use the quantized models, install the required dependency `pip install optimum[exporters] optimum-intel neural-compressor intel_extension_for_pytorch`.
Loading is done using the class `IntelEmbedding`; usage is similar to any HuggingFace local embedding model; See example:
``` %pip install llama-index-embeddings-huggingface-optimum-intel ```
``` from llama_index.embeddings.huggingface_optimum_intel import IntelEmbedding
embed_model = IntelEmbedding("Intel/bge-small-en-v1.5-rag-int8-static") ```
``` embeddings = embed_model.get_text_embedding("Hello World!") print(len(embeddings)) print(embeddings[:5]) ```

``` 384 [-0.0032782123889774084, -0.013396517373621464, 0.037944991141557693, -0.04642259329557419, 0.027709005400538445] ```

[1] https://huggingface.co/docs/optimum/main/en/intel/index
[2] https://huggingface.co/docs/optimum/main/en/intel/optimization_inc