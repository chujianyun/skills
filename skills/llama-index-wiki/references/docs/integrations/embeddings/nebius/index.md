# developers.llamaindex.ai/python/framework/integrations/embeddings/nebius/index.md
> https://developers.llamaindex.ai/python/framework/integrations/embeddings/nebius/index.md

--- title: Nebius Embeddings | Developer Documentation ---

This notebook demonstrates how to use Nebius AI Studio [1] Embeddings with LlamaIndex. Nebius AI Studio implements all state-of-the-art embeddings models, available for commercial use.

First, let’s install LlamaIndex and dependencies of Nebius AI Studio.
``` %pip install llama-index-embeddings-nebius llama-index ```

Upload your Nebius AI Studio key from system variables below or simply insert it. You can get it by registering for free at Nebius AI Studio [2] and issuing the key at [API Keys section] [3].

``` import os
NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY") # NEBIUS_API_KEY = "" ```
Now let’s get embeddings using Nebius AI Studio
``` from llama_index.embeddings.nebius import NebiusEmbedding
embed_model = NebiusEmbedding(api_key=NEBIUS_API_KEY) ```
### Basic usage
``` text = "Everyone loves justice at another person's expense" embeddings = embed_model.get_text_embedding(text) assert len(embeddings) == 4096 print(len(embeddings), embeddings[:5], sep="\n") ```

### Asynchronous usage
``` text = "Everyone loves justice at another person's expense" embeddings = await embed_model.aget_text_embedding(text) assert len(embeddings) == 4096 print(len(embeddings), embeddings[:5], sep="\n") ```

``` 4096 [-0.0024051666259765625, 0.0083770751953125, -0.005413055419921875, 0.007396697998046875, -0.022247314453125] ```

### Batched usage

embeddings = embed_model.get_text_embedding_batch(texts) assert len(embeddings) == 4 assert len(embeddings[0]) == 4096 print(*[x[:3] for x in embeddings], sep="\n") ```

### Async batched usage
``` texts = [ "As the hours pass", "I will let you know", "That I need to ask", "Before I'm alone", ]

embeddings = await embed_model.aget_text_embedding_batch(texts) assert len(embeddings) == 4 assert len(embeddings[0]) == 4096 print(*[x[:3] for x in embeddings], sep="\n") ```

``` [-0.0003848075866699219, 0.0004799365997314453, 0.011199951171875] [-0.0037078857421875, 0.0114288330078125, 0.00878143310546875] [0.005924224853515625, 0.005153656005859375, 0.001438140869140625] [-0.009490966796875, -0.004852294921875, 0.004779815673828125] ```

[1] https://studio.nebius.ai/
[2] https://auth.eu.nebius.com/ui/login
[3] https://studio.nebius.ai/settings/api-keys