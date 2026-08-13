# developers.llamaindex.ai/python/framework/integrations/embeddings/clarifai/index.md
> https://developers.llamaindex.ai/python/framework/integrations/embeddings/clarifai/index.md

--- title: Embeddings with Clarifai | Developer Documentation ---
LlamaIndex has support for Clarifai embeddings models.

You must have a Clarifai account and a Personal Access Token (PAT) key. Check here [1] to get or create a PAT.

Set CLARIFAI\_PAT as an environment variable or You can pass PAT as argument to ClarifaiEmbedding class
``` %pip install llama-index-embeddings-clarifai ```
``` !export CLARIFAI_PAT=YOUR_KEY ```
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` !pip install llama-index ```
Models can be referenced either by the full URL or by the model\_name, user ID, and app ID combination.
``` from llama_index.embeddings.clarifai import ClarifaiEmbedding
# Create a clarifai embedding class just with model_url, assuming that CLARIFAI_PAT is set as an environment variable embed_model = ClarifaiEmbedding( model_url="https://clarifai.com/clarifai/main/models/BAAI-bge-base-en" )

# Alternatively you can initialize the class with model_name, user_id, app_id and pat as well. embed_model = ClarifaiEmbedding( model_name="BAAI-bge-base-en", user_id="clarifai", app_id="main", pat=CLARIFAI_PAT, ) ```

``` embeddings = embed_model.get_text_embedding("Hello World!") print(len(embeddings)) print(embeddings[:5]) ```

Embed list of texts
``` text = "roses are red violets are blue." text2 = "Make hay while the sun shines." ```

``` embeddings = embed_model._get_text_embeddings([text2, text]) print(len(embeddings)) print(embeddings[0][:5]) print(embeddings[1][:5]) ```

[1] https://clarifai.com/settings/security