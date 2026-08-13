# developers.llamaindex.ai/python/framework/integrations/embeddings/huggingface/index.md
> https://developers.llamaindex.ai/python/framework/integrations/embeddings/huggingface/index.md

--- title: Local Embeddings with HuggingFace | Developer Documentation ---

LlamaIndex has support for HuggingFace embedding models, including Sentence Transformer models like BGE, Mixedbread, Nomic, Jina, E5, etc. We can use these models to create embeddings for our documents and queries for retrieval.
Furthermore, we provide utilities to create and use ONNX and OpenVINO models using the Optimum library [1] from HuggingFace.
## HuggingFaceEmbedding
The base `HuggingFaceEmbedding` class is a generic wrapper around any HuggingFace model for embeddings. All embedding models [2] on Hugging Face should work. You can refer to the embeddings leaderboard [3] for more recommendations.
This class depends on the sentence-transformers package, which you can install with `pip install sentence-transformers`.
NOTE: if you were previously using a `HuggingFaceEmbeddings` from LangChain, this should give equivalent results.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-embeddings-huggingface ```
``` !pip install llama-index ```

# loads https://huggingface.co/BAAI/bge-small-en-v1.5 embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5") ```
``` embeddings = embed_model.get_text_embedding("Hello World!") print(len(embeddings)) print(embeddings[:5]) ```
``` 384 [-0.003275700844824314, -0.011690810322761536, 0.041559211909770966, -0.03814814239740372, 0.024183044210076332] ```
## Benchmarking
Let’s try comparing using a classic large document — the IPCC climate report, chapter 3.
``` !curl https://www.ipcc.ch/report/ar6/wg2/downloads/report/IPCC_AR6_WGII_Chapter03.pdf --output IPCC_AR6_WGII_Chapter03.pdf ```
``` % Total % Received % Xferd Average Speed Time Time Time Current Dload Upload Total Spent Left Speed
0 0 0 0 0 0 0 0 --:--:-- --:--:-- --:--:-- 0 100 20.7M 100 20.7M 0 0 69.6M 0 --:--:-- --:--:-- --:--:-- 70.0M ```
``` from llama_index.core import VectorStoreIndex, SimpleDirectoryReader from llama_index.core import Settings
documents = SimpleDirectoryReader( input_files=["IPCC_AR6_WGII_Chapter03.pdf"] ).load_data() ```
### Base HuggingFace Embeddings
``` from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# loads BAAI/bge-small-en-v1.5 with the default torch backend embed_model = HuggingFaceEmbedding( model_name="BAAI/bge-small-en-v1.5", device="cpu", embed_batch_size=8, ) test_embeds = embed_model.get_text_embedding("Hello World!")

``` Parsing nodes: 100%|██████████| 172/172 [00:00<00:00, 428.44it/s] Generating embeddings: 100%|██████████| 459/459 [00:19<00:00, 23.32it/s]

20.2 s ± 0 ns per loop (mean ± std. dev. of 1 run, 1 loop each) ```
### ONNX Embeddings
``` # pip install sentence-transformers[onnx]
# loads BAAI/bge-small-en-v1.5 with the onnx backend embed_model = HuggingFaceEmbedding( model_name="BAAI/bge-small-en-v1.5", device="cpu", backend="onnx", model_kwargs={ "provider": "CPUExecutionProvider" }, # For ONNX, you can specify the provider, see https://sbert.net/docs/sentence_transformer/usage/efficiency.html ) test_embeds = embed_model.get_text_embedding("Hello World!")

[Column 1]
``` Parsing nodes: 100%|██████████| 172/172 [00:00<00:00, 421.63it/s] Generating embeddings: 100%|██████████| 459/459 [00:31<00:00, 14.53it/s]
32.1 s ± 0 ns per loop (mean ± std. dev. of 1 run, 1 loop each) ```
### OpenVINO Embeddings
``` # pip install sentence-transformers[openvino]

Settings.embed_model = embed_model ```
``` %%timeit -r 1 -n 1 index = VectorStoreIndex.from_documents(documents, show_progress=True) ```
``` Parsing nodes: 100%|██████████| 172/172 [00:00<00:00, 403.15it/s] Generating embeddings: 100%|██████████| 459/459 [00:08<00:00, 53.83it/s]

[Column 2]
# loads BAAI/bge-small-en-v1.5 with the openvino backend embed_model = HuggingFaceEmbedding( model_name="BAAI/bge-small-en-v1.5", device="cpu", backend="openvino", # OpenVINO is very strong on CPUs revision="refs/pr/16", # BAAI/bge-small-en-v1.5 itself doesn't have an OpenVINO model currently, but there's a PR with it that we can load: https://huggingface.co/BAAI/bge-small-en-v1.5/discussions/16 model_kwargs={ "file_name": "openvino_model_qint8_quantized.xml" }, # If we're using an optimized/quantized model, we need to specify the file name like this ) test_embeds = embed_model.get_text_embedding("Hello World!")


9.03 s ± 0 ns per loop (mean ± std. dev. of 1 run, 1 loop each) ```
### References
- Local Embedding Models [4] explains more about using local models like these. - Sentence Transformers > Speeding up Inference [5] contains extensive documentation on how to use the backend options effectively, including optimization and quantization for ONNX and OpenVINO.

[1] https://huggingface.co/docs/optimum
[2] https://huggingface.co/models?library=sentence-transformers
[3] https://huggingface.co/spaces/mteb/leaderboard
[4] https://docs.llamaindex.ai/en/stable/module_guides/models/embeddings/#local-embedding-models
[5] https://sbert.net/docs/sentence_transformer/usage/efficiency.html