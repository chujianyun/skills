# developers.llamaindex.ai/python/framework/integrations/embeddings/mixedbreadai/index.md
> https://developers.llamaindex.ai/python/framework/integrations/embeddings/mixedbreadai/index.md

--- title: Mixedbread AI Embeddings | Developer Documentation ---

Explore the capabilities of MixedBread AI’s embedding models with custom encoding formats (binary, int, float, base64, etc.), embedding dimensions (Matryoshka) and context prompts.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-embeddings-mixedbreadai ```
``` !pip install llama-index ```
``` import os from llama_index.embeddings.mixedbreadai import MixedbreadAIEmbedding ```

``` # API Key and Embedding Initialization
# You can visit https://www.mixedbread.ai/api-reference#quick-start-guide # to get an api key mixedbread_api_key = os.environ.get("MXBAI_API_KEY", "your-api-key")

# Please check https://www.mixedbread.ai/docs/embeddings/models#whats-new-in-the-mixedbread-embed-model-family # for our embedding models model_name = "mixedbread-ai/mxbai-embed-large-v1" ```

``` oven = MixedbreadAIEmbedding(api_key=mixedbread_api_key, model_name=model_name)
embeddings = oven.get_query_embedding("Why bread is so tasty?")
print(len(embeddings)) print(embeddings[:5]) ```
``` 1024 [0.01128387451171875, 0.031097412109375, -0.00606536865234375, 0.0291748046875, -0.038604736328125] ```

### Using prompt for contextual embedding
The prompt can improve the model’s understanding of how the embedding will be used in subsequent tasks, which in turn increases the performance. Our experiments show that having domain specific prompts can increase the performance.
``` prompt_for_retrieval = ( "Represent this sentence for searching relevant passages:" )

contextual_oven = MixedbreadAIEmbedding( api_key=mixedbread_api_key, model_name=model_name, prompt=prompt_for_retrieval, )

contextual_embeddings = contextual_oven.get_query_embedding( "What bread is invented in Germany?" )

print(len(contextual_embeddings)) print(contextual_embeddings[:5]) ```
``` 1024 [-0.0235443115234375, -0.0152435302734375, 0.008392333984375, 0.00336456298828125, -0.044647216796875] ```

## Quantization and Matryoshka support
The Mixedbread AI embedding supports quantization and matryoshka to reduce the size of embeddings for better storage while retaining most of the performance. See these posts for more information:
- Binary and Scalar Embedding Quantization for Significantly Faster & Cheaper Retrieval [1] - 64 bytes per embedding, yee-haw [2].
### Using different encoding formats
The default `encoding_format` is `float`. We also support `float16`, `binary`, `ubinary`, `int8`, `uint8`, `base64`.
``` # with `binary` embedding types binary_oven = MixedbreadAIEmbedding( api_key=mixedbread_api_key, model_name=model_name, encoding_format="binary", )

binary_embeddings = binary_oven.get_text_embedding( "The bread is tiny but still filling!" )

print(len(binary_embeddings)) print(binary_embeddings[:5]) ```
``` 128 [-121.0, 96.0, -108.0, 111.0, 110.0] ```

### Using different embedding dimensions
Mixedbread AI embedding models support Matryoshka dimension truncation. The default dimension is set to the model’s maximum. Keep an eye on our website to see what models support Matryoshka.
``` # with truncated dimension half_oven = MixedbreadAIEmbedding( api_key=mixedbread_api_key, model_name=model_name, dimensions=512, # 1024 is the maximum of `mxbai-embed-large-v1` )

half_embeddings = half_oven.get_text_embedding( "I want the better half of my bread." )

print(len(half_embeddings)) print(half_embeddings[:5]) ```
``` 512 [-0.014221191, -0.013671875, -0.03314209, 0.025909424, -0.035095215] ```

[1] https://huggingface.co/blog/embedding-quantization
[2] https://www.mixedbread.ai/blog/binary-mrl