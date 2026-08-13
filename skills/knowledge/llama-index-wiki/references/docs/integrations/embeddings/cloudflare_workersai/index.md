# developers.llamaindex.ai/python/framework/integrations/embeddings/cloudflare_workersai/index.md
> https://developers.llamaindex.ai/python/framework/integrations/embeddings/cloudflare_workersai/index.md

--- title: Cloudflare Workers AI Embeddings | Developer Documentation ---

## Setup
Install library via pip
``` %pip install llama-index-embeddings-cloudflare-workersai # %pip install -e ~/llama_index/llama-index-integrations/embeddings/llama-index-embeddings-cloudflare-workersai ```

To acess Cloudflare Workers AI, both Cloudflare account ID and API token are required. To get your account ID and API token, please follow the instructions on this document [1].

``` # Initilise with account ID and API token
# import os
# my_account_id = "example_id" # my_api_token = "example_token" # os.environ["CLOUDFLARE_AUTH_TOKEN"] = "my_api_token"
import getpass
my_account_id = getpass.getpass("Enter your Cloudflare account ID:\n\n") my_api_token = getpass.getpass("Enter your Cloudflare API token:\n\n") ```
## Text embeddings example
``` from llama_index.embeddings.cloudflare_workersai import CloudflareEmbedding
my_embed = CloudflareEmbedding( account_id=my_account_id, auth_token=my_api_token, model="@cf/baai/bge-small-en-v1.5", )

embeddings = my_embed.get_text_embedding("Why sky is blue")
print(len(embeddings)) print(embeddings[:5]) ```
``` 384 [-0.04786296561360359, -0.030788540840148926, -0.07126234471797943, -0.04107927531003952, 0.02904760278761387] ```
#### Embed in batches
As for batch size, Cloudflare’s limit is a maximum of 100, as seen on 2024-03-31.
``` embeddings = my_embed.get_text_embedding_batch( ["Why sky is blue", "Why roses are red"] ) print(len(embeddings)) print(len(embeddings[0])) print(embeddings[0][:5]) print(embeddings[1][:5]) ```

``` 2 384 [-0.04786296561360359, -0.030788540840148926, -0.07126234471797943, -0.04107927531003952, 0.02904760278761387] [-0.08951402455568314, -0.015274363569915295, 0.04728245735168457, 0.05478525161743164, 0.05978189781308174] ```

[1] https://developers.cloudflare.com/workers- ai/get-started/rest-api/