# developers.llamaindex.ai/python/framework/integrations/llm/mistral_rs/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/mistral_rs/index.md

--- title: MistralRS LLM | Developer Documentation ---

**NOTE:** MistralRS requires a rust package manager called `cargo` to be installed. Visit <https://rustup.rs/> for installation details.

``` %pip install llama-index-core %pip install llama-index-readers-file %pip install llama-index-llms-mistral-rs %pip install llama-index-llms-huggingface ```
``` from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings from llama_index.core.embeddings import resolve_embed_model from llama_index.llms.mistral_rs import MistralRS from mistralrs import Which, Architecture
documents = SimpleDirectoryReader("data").load_data()
# bge embedding model Settings.embed_model = resolve_embed_model("local:BAAI/bge-small-en-v1.5") ```
MistralRS uses model IDs from huggingface hub.
``` # Full Model Settings.llm = MistralRS( which=Which.Plain( model_id="mistralai/Mistral-7B-Instruct-v0.1", arch=Architecture.Mistral, tokenizer_json=None, repeat_last_n=64, ), max_new_tokens=4096, context_window=1024 * 5, )

# GGUF Model, Quantized Settings.llm = MistralRS( which=Which.GGUF( tok_model_id="mistralai/Mistral-7B-Instruct-v0.1", quantized_model_id="TheBloke/Mistral-7B-Instruct-v0.1-GGUF", quantized_filename="mistral-7b-instruct-v0.1.Q4_K_M.gguf", tokenizer_json=None, repeat_last_n=64, ), max_new_tokens=4096, context_window=1024 * 5, ) ```

``` index = VectorStoreIndex.from_documents( documents, ) ```
``` query_engine = index.as_query_engine() response = query_engine.query("How do I pronounce graphene?") print(response) ```