# developers.llamaindex.ai/python/framework/integrations/embeddings/nvidia/index.md
> https://developers.llamaindex.ai/python/framework/integrations/embeddings/nvidia/index.md

--- title: NVIDIA NIMs | Developer Documentation ---

The `llama-index-embeddings-nvidia` package contains LlamaIndex integrations building applications with models on NVIDIA NIM inference microservice. NIM supports models across domains like chat, embedding, and re-ranking models from the community as well as NVIDIA. These models are optimized by NVIDIA to deliver the best performance on NVIDIA accelerated infrastructure and deployed as a NIM, an easy-to-use, prebuilt containers that deploy anywhere using a single command on NVIDIA accelerated infrastructure.
NVIDIA hosted deployments of NIMs are available to test on the NVIDIA API catalog [1]. After testing, NIMs can be exported from NVIDIA’s API catalog using the NVIDIA AI Enterprise license and run on-premises or in the cloud, giving enterprises ownership and full control of their IP and AI application.
NIMs are packaged as container images on a per model basis and are distributed as NGC container images through the NVIDIA NGC Catalog. At their core, NIMs provide easy, consistent, and familiar APIs for running inference on an AI model.
## Installation
``` %pip install --upgrade --quiet llama-index-embeddings-nvidia ```
## Setup
**To get started:**
1. Create a free account with NVIDIA [1], which hosts NVIDIA AI Foundation models.
2. Select the `Retrieval` tab, then select your model of choice.
3. Under `Input` select the `Python` tab, and click `Get API Key`. Then click `Generate Key`.
4. Copy and save the generated key as `NVIDIA_API_KEY`. From there, you should have access to the endpoints.
``` import getpass import os

# del os.environ['NVIDIA_API_KEY'] ## delete key and reset if os.environ.get("NVIDIA_API_KEY", "").startswith("nvapi-"): print("Valid NVIDIA_API_KEY already in environment. Delete to reset") else: nvapi_key = getpass.getpass("NVAPI Key (starts with nvapi-): ") assert nvapi_key.startswith( "nvapi-" ), f"{nvapi_key[:5]}... is not a valid key" os.environ["NVIDIA_API_KEY"] = nvapi_key ```

## Working with the NVIDIA API Catalog
When initializing an embedding model, you can select a model by passing a model name (for example, `NV-Embed-QA`), or use the default by not passing any arguments.

embedder = NVIDIAEmbedding(model="NV-Embed-QA") ```
This model is a fine-tuned E5-large model which supports the expected `Embeddings` [2] methods including:
- `get_query_embedding`: Generate query embedding for a query sample.
- `get_text_embedding_batch`: Generate text embeddings for a list of documents which you would like to search over.
- And asynchronous versions of the above.
## Working with NVIDIA NIMs
In addition to connecting to hosted NVIDIA NIMs [3], this connector can be used to connect to local NIM instances. This helps you take your applications local when necessary.
For instructions on how to set up local NIM instances, refer to NVIDIA NIM [4].
``` from llama_index.embeddings.nvidia import NVIDIAEmbedding

# Connect to an embedding NIM running at localhost:8080 embedder = NVIDIAEmbedding(base_url="http://localhost:8080/v1") embedder.available_models ```
``` /home/raspawar/Desktop/llama_index/llama-index-integrations/embeddings/llama-index-embeddings-nvidia/llama_index/embeddings/nvidia/base.py:161: UserWarning: Default model is set as: NV-Embed-QA. Set model using model parameter. To get available models use available_models property. warnings.warn(

[Model(id='NV-Embed-QA', base_model=None)] ```
### **Similarity**
The following is a quick test of the similarity for these data points:

### Embed queries
``` print("\nSequential Embedding: ") q_embeddings = [ embedder.get_query_embedding("What's the weather like in Komchatka?"), embedder.get_query_embedding("What kinds of food is Italy known for?"), embedder.get_query_embedding( "What's my name? I bet you don't remember..." ), embedder.get_query_embedding("What's the point of life anyways?"), embedder.get_query_embedding("The point of life is to have fun :D"), ] print("Shape:", (len(q_embeddings), len(q_embeddings[0]))) ```

### Embed documents
``` print("\nBatch Document Embedding: ") d_embeddings = embedder.get_text_embedding_batch( [ "Komchatka's weather is cold, with long, severe winters.", "Italy is famous for pasta, pizza, gelato, and espresso.", "I can't recall personal names, only provide information.", "Life's purpose varies, often seen as personal fulfillment.", "Enjoying life's moments is indeed a wonderful approach.", ] ) print("Shape:", (len(d_embeddings), len(d_embeddings[0]))) ```

Now that we’ve generated our embeddings, we can do a simple similarity check on the results to see which documents would have triggered as reasonable answers in a retrieval task:
``` %pip install --upgrade --quiet matplotlib scikit-learn ```
``` import matplotlib.pyplot as plt import numpy as np from sklearn.metrics.pairwise import cosine_similarity

# Compute the similarity matrix between q_embeddings and d_embeddings cross_similarity_matrix = cosine_similarity( np.array(q_embeddings), np.array(d_embeddings), )

# Plotting the cross-similarity matrix plt.figure(figsize=(8, 6)) plt.imshow(cross_similarity_matrix, cmap="Greens", interpolation="nearest") plt.colorbar() plt.title("Cross-Similarity Matrix") plt.xlabel("Query Embeddings") plt.ylabel("Document Embeddings") plt.grid(True) plt.show() ```

As a reminder, the queries and documents sent to our system were:
**Queries:**
- What’s the weather like in Komchatka?
- What kinds of food is Italy known for?
- What’s my name? I bet you don’t remember…
- What’s the point of life anyways?
- The point of life is to have fun :D
**Texts:**
- Komchatka’s weather is cold, with long, severe winters.
- Italy is famous for pasta, pizza, gelato, and espresso.
- I can’t recall personal names, only provide information.
- Life’s purpose varies, often seen as personal fulfillment.
- Enjoying life’s moments is indeed a wonderful approach.
## Truncation
Embedding models typically have a fixed context window that determines the maximum number of input tokens that can be embedded. This limit could be a hard limit, equal to the model’s maximum input token length, or an effective limit, beyond which the accuracy of the embedding decreases.
Since models operate on tokens and applications usually work with text, it can be challenging for an application to ensure that its input stays within the model’s token limits. By default, an exception is thrown if the input is too large.
To assist with this, NVIDIA NIMs provide a `truncate` parameter that truncates the input on the server side if it’s too large.
The `truncate` parameter has three options:
- “NONE”: The default option. An exception is thrown if the input is too large. - “START”: The server truncates the input from the start (left), discarding tokens as necessary. - “END”: The server truncates the input from the end (right), discarding tokens as necessary.
``` long_text = "AI is amazing, amazing is " * 100 ```
``` strict_embedder = NVIDIAEmbedding() try: strict_embedder.get_query_embedding(long_text) except Exception as e: print("Error:", e) ```

``` truncating_embedder = NVIDIAEmbedding(truncate="END") truncating_embedder.get_query_embedding(long_text)[:5] ```

[1] https://build.nvidia.com/
[2] https://docs.llamaindex.ai/en/stable/api_reference/embeddings/
[3] https://ai.nvidia.com
[4] https://developer.nvidia.com/nim