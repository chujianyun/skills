# developers.llamaindex.ai/python/framework/integrations/embeddings/vertex_embedding_endpoint/index.md
> https://developers.llamaindex.ai/python/framework/integrations/embeddings/vertex_embedding_endpoint/index.md

--- title: Interacting with Embeddings deployed in Vertex AI Endpoint with LlamaIndex | Developer Documentation ---

A Vertex AI endpoint is a managed resource that enables the deployment of machine learning models, such as embeddings, for making predictions on new data.
This notebook demonstrates how to interact with embedding endpoints using the `VertexEndpointEmbedding` class, leveraging the LlamaIndex.
## Setting Up
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-embeddings-vertex-endpoint ```
``` ! pip install llama-index ```
You need to specify the endpoint information (endpoint ID, project ID, and region) to interact with the model deployed in Vertex AI.
``` ENDPOINT_ID = "<-YOUR-ENDPOINT-ID->" PROJECT_ID = "<-YOUR-PROJECT-ID->" LOCATION = "<-YOUR-GCP-REGION->" ```

Credentials should be provided to connect to the endpoint. You can either:
- Use a service account JSON file by specifying the `service_account_file` parameter. - Provide the service account information directly through the `service_account_info` parameter.
**Example using a service account file:**

[Column 1]
SERVICE_ACCOUNT_FILE = "<-YOUR-SERVICE-ACCOUNT-FILE-PATH->.json"
embed_model = VertexEndpointEmbedding( endpoint_id=ENDPOINT_ID, project_id=PROJECT_ID, location=LOCATION, service_account_file=SERVICE_ACCOUNT_FILE, ) ```
**Example using direct service account info:**:
``` from llama_index.embeddings.vertex_endpoint import VertexEndpointEmbedding
SERVICE_ACCOUNT_INFO = { "private_key": "<-PRIVATE-KEY->", "client_email": "<-SERVICE-ACCOUNT-EMAIL->", "token_uri": "https://oauth2.googleapis.com/token", }
embed_model = VertexEndpointEmbedding( endpoint_id=ENDPOINT_ID, project_id=PROJECT_ID, location=LOCATION, service_account_info=SERVICE_ACCOUNT_INFO, ) ```
## Basic Usage
### Call `get_text_embedding`

``` embeddings[:10] ```
``` [0.011612358, 0.01030837, -0.04710829, -0.030719217, 0.027658276, -0.031597693, 0.012065322, -0.037609763, 0.02321099, 0.012868305] ```

### Call `get_text_embedding_batch`

``` len(embeddings) ```
``` 2 ```

[Column 2]
``` embeddings = embed_model.get_text_embedding( "Vertex AI is a managed machine learning (ML) platform provided by Google Cloud. It allows data scientists and developers to build, deploy, and scale machine learning models efficiently, leveraging Google's ML infrastructure." ) ```
``` embeddings = embed_model.get_text_embedding_batch( [ "Vertex AI is a managed machine learning (ML) platform provided by Google Cloud. It allows data scientists and developers to build, deploy, and scale machine learning models efficiently, leveraging Google's ML infrastructure.", "Vertex is integrated with llamaIndex", ] ) ```
