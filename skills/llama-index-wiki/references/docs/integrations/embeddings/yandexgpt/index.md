# developers.llamaindex.ai/python/framework/integrations/embeddings/yandexgpt/index.md
> https://developers.llamaindex.ai/python/framework/integrations/embeddings/yandexgpt/index.md

--- title: YandexGPT | Developer Documentation ---
``` %pip install llama-index-embeddings-yandexgpt ```
``` !pip install llama-index ```
``` from llama_index.embeddings.yandexgpt import YandexGPTEmbedding
yandexgpt_embedding = YandexGPTEmbedding( api_key="<API_KEY>", folder_id="your-folder-id" )
text_embedding = yandexgpt_embedding._get_text_embeddings( ["This is a passage!", "This is another passage"] ) print(text_embedding)
query_embedding = yandexgpt_embedding._get_query_embedding("Where is blue?") print(query_embedding) ```