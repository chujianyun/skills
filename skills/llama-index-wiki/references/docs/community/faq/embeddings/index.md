# developers.llamaindex.ai/python/framework/community/faq/embeddings/index.md
> https://developers.llamaindex.ai/python/framework/community/faq/embeddings/index.md

--- title: Embeddings | Developer Documentation ---
##### FAQ
1. How to use a custom/local embedding model? 2. How to use a local hugging face embedding model? 3. How to use embedding model to generate embeddings for text? 4. How to use Huggingface Text-Embedding Inference with LlamaIndex?

##### 1. How to use a custom/local embedding model?
To create your customized embedding class you can follow Custom Embeddings guide.

##### 2. How to use a local hugging face embedding model?
To use a local HuggingFace embedding model you can follow Local Embeddings with HuggingFace guide.

##### 3. How to use embedding model to generate embeddings for text?
You can generate embeddings for texts with the following piece of code.
``` text_embedding = embed_model.get_text_embedding("YOUR_TEXT") ```
---
##### 4. How to use Huggingface Text-Embedding Inference with LlamaIndex?
To use HuggingFace Text-Embedding Inference you can follow Text-Embedding-Inference tutorial.