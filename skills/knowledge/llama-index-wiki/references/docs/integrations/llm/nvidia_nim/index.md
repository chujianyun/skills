# developers.llamaindex.ai/python/framework/integrations/llm/nvidia_nim/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/nvidia_nim/index.md

--- title: NVIDIA NIMs | Developer Documentation ---

The `llama-index-llms-nvidia` package contains LlamaIndex integrations building applications with models on NVIDIA NIM inference microservice. NIM supports models across domains like chat, embedding, and re-ranking models from the community as well as NVIDIA. These models are optimized by NVIDIA to deliver the best performance on NVIDIA accelerated infrastructure and deployed as a NIM, an easy-to-use, prebuilt containers that deploy anywhere using a single command on NVIDIA accelerated infrastructure.
NVIDIA hosted deployments of NIMs are available to test on the NVIDIA API catalog [1]. After testing, NIMs can be exported from NVIDIA’s API catalog using the NVIDIA AI Enterprise license and run on-premises or in the cloud, giving enterprises ownership and full control of their IP and AI application.
NIMs are packaged as container images on a per model basis and are distributed as NGC container images through the NVIDIA NGC Catalog. At their core, NIMs provide easy, consistent, and familiar APIs for running inference on an AI model.
``` %pip install --upgrade --quiet llama-index-core llama-index-readers-file llama-index-llms-nvidia llama-index-embeddings-nvidia llama-index-postprocessor-nvidia-rerank ```
Bring in a test dataset, a PDF about housing construction in San Francisco in 2021.
``` !mkdir data !wget "https://www.dropbox.com/scl/fi/p33j9112y0ysgwg77fdjz/2021_Housing_Inventory.pdf?rlkey=yyok6bb18s5o31snjd2dxkxz3&dl=0" -O "data/housing_data.pdf" ```

``` --2024-05-28 17:42:44-- https://www.dropbox.com/scl/fi/p33j9112y0ysgwg77fdjz/2021_Housing_Inventory.pdf?rlkey=yyok6bb18s5o31snjd2dxkxz3&dl=0 Resolving www.dropbox.com (www.dropbox.com)... 162.125.1.18, 2620:100:6016:18::a27d:112 Connecting to www.dropbox.com (www.dropbox.com)|162.125.1.18|:443... connected. HTTP request sent, awaiting response... 302 Found Location: https://ucc6b49e945b8d71944c85f4a76d.dl.dropboxusercontent.com/cd/0/inline/CTzJ0ZeHC3AFIV3iv1bv9v0oMNXW03OW2waLdeKJNs0X6Tto0MSewm9RZBHwSLhqk4jWFaCmbhMGVXeWa6xPO4mAR4hC3xflJfwgS9Z4lpPUyE4AtlDXpnfsltjEaNeFCSY/file# [following] --2024-05-28 17:42:45-- https://ucc6b49e945b8d71944c85f4a76d.dl.dropboxusercontent.com/cd/0/inline/CTzJ0ZeHC3AFIV3iv1bv9v0oMNXW03OW2waLdeKJNs0X6Tto0MSewm9RZBHwSLhqk4jWFaCmbhMGVXeWa6xPO4mAR4hC3xflJfwgS9Z4lpPUyE4AtlDXpnfsltjEaNeFCSY/file Resolving ucc6b49e945b8d71944c85f4a76d.dl.dropboxusercontent.com (ucc6b49e945b8d71944c85f4a76d.dl.dropboxusercontent.com)... 162.125.4.15, 2620:100:6016:15::a27d:10f Connecting to ucc6b49e945b8d71944c85f4a76d.dl.dropboxusercontent.com (ucc6b49e945b8d71944c85f4a76d.dl.dropboxusercontent.com)|162.125.4.15|:443... connected. HTTP request sent, awaiting response... 302 Found Location: /cd/0/inline2/CTySzMwupnuXzKpccOeYJ-7RI0NK0f7XMKBkpicHxSBuuwqAvFly51Fm0oCOwFctgeTqmD3thJsTqfFNOFHNe2JSIkJerj3mMr4Du3C7x1BcSy8t5raSfHQ_qSXF1eHrhdFII8Ou59jbofYVLe0punOl-RIa9k_v722SwkxVbg0KL9MrRL48XjX7JbsYHKTHq- gZSdAmpXpIGqS22eJavcSTuYMIy_GSZtDIs3quHM3PGU4849rG34RjpvAa-XkYDBdE996CxWupZ1C2Red9jEc5Tc6miGgt8-4LbGoxKwKF5I_Q3EqHCbvkibVR8OuKSKPtQZcNJSjsvIImzDLJ2WB6BAp2CBxz8szFF3jF3Gp6Iw/file [following] --2024-05-28 17:42:45-- https://ucc6b49e945b8d71944c85f4a76d.dl.dropboxusercontent.com/cd/0/inline2/CTySzMwupnuXzKpccOeYJ- 7RI0NK0f7XMKBkpicHxSBuuwqAvFly51Fm0oCOwFctgeTqmD3thJsTqfFNOFHNe2JSIkJerj3mMr4Du3C7x1BcSy8t5raSfHQ_qSXF1eHrhdFII8Ou59jbofYVLe0punOl-RIa9k_v722SwkxVbg0KL9MrRL48XjX7JbsYHKTHq- gZSdAmpXpIGqS22eJavcSTuYMIy_GSZtDIs3quHM3PGU4849rG34RjpvAa-XkYDBdE996CxWupZ1C2Red9jEc5Tc6miGgt8-4LbGoxKwKF5I_Q3EqHCbvkibVR8OuKSKPtQZcNJSjsvIImzDLJ2WB6BAp2CBxz8szFF3jF3Gp6Iw/file

Reusing existing connection to ucc6b49e945b8d71944c85f4a76d.dl.dropboxusercontent.com:443. HTTP request sent, awaiting response... 200 OK Length: 4808625 (4.6M) [application/pdf] Saving to: ‘data/housing_data.pdf’

data/housing_data.p 100%[===================>] 4.58M 8.26MB/s in 0.6s
2024-05-28 17:42:47 (8.26 MB/s) - ‘data/housing_data.pdf’ saved [4808625/4808625] ```
## Setup
Import dependencies and set up your NVIDIA API key from the NVIDIA API Catalog [2].
**To get started:**
1. Create a free account with NVIDIA [1], which hosts NVIDIA AI Foundation models.
2. Click on your model of choice.
3. Under **Input**, select the **Python** tab, and click **Get API Key**. Then click **Generate Key**.
4. Copy and save the generated key as `NVIDIA_API_KEY`. From there, you should have access to the endpoints.
``` from llama_index.core import SimpleDirectoryReader, Settings, VectorStoreIndex from llama_index.embeddings.nvidia import NVIDIAEmbedding from llama_index.llms.nvidia import NVIDIA from llama_index.core.node_parser import SentenceSplitter from llama_index.core import Settings from google.colab import userdata import os

os.environ["NVIDIA_API_KEY"] = userdata.get("nvidia-api-key") ```
Use an NVIDIA-hosted NIM for the embedding model.
NVIDIA’s default embeddings only embed the first 512 tokens, so set the chunk size to 500 to maximize the accuracy of embeddings.
``` Settings.text_splitter = SentenceSplitter(chunk_size=500)
documents = SimpleDirectoryReader("./data").load_data() ```
Set the embedding model to NVIDIA’s default. If a chunk exceeds the number of tokens the model can encode, the default behavior is to throw an error, so set `truncate="END"` to instead discard tokens that go over the limit.
``` Settings.embed_model = NVIDIAEmbedding(model="NV-Embed-QA", truncate="END")
index = VectorStoreIndex.from_documents(documents) ```
Now that the data is embedded and indexed in memory, set up the LLM. NIM can be hosted locally using Docker in 5 minutes by following the NIM quick start guide [3].
The following example shows how to:
- Use Meta’s open-source `meta/llama-3.1-8b-instruct` model as a local NIM. - Use `meta/llama-3.1-70b-instruct` as a NIM from the API Catalog hosted by NVIDIA.
If you are using a local NIM, change the `base_url` to your deployed NIM URL.
The example retrieves the top 20 most relevant chunks to answer the question.
``` # Self-hosted NIM: uncomment the line below and comment the API Catalog line # Settings.llm = NVIDIA(model="meta/llama-3.1-8b-instruct", base_url="http://your-nim-host-address:8000/v1")

# API Catalog NIM: comment this line if using a self-hosted NIM Settings.llm = NVIDIA(model="meta/llama-3.1-70b-instruct")
query_engine = index.as_query_engine(similarity_top_k=20) ```
Ask a simple question that is answered in one place in the document (on page 18).
``` response = query_engine.query( "How many new housing units were built in San Francisco in 2021?" ) print(response) ```

``` There was a net addition of 4,649 units to the City’s housing stock in 2021. ```
Now ask a more complicated question that requires reading a table (on page 41 of the document):
``` response = query_engine.query( "What was the net gain in housing units in the Mission in 2021?" ) print(response) ```

``` There is no specific information about the net gain in housing units in the Mission in 2021. The provided data is about the city's overall housing stock and production, but it does not provide a breakdown by neighborhood, including the Mission. ```

That’s not the right answer. Try a more advanced PDF parser, LlamaParse:
``` !pip install llama-parse ```
``` from llama_parse import LlamaParse
# in a notebook, LlamaParse requires this to work import nest_asyncio
nest_asyncio.apply()
# you can get a key at cloud.llamaindex.ai os.environ["LLAMA_CLOUD_API_KEY"] = userdata.get("llama-cloud-key")
# set up parser parser = LlamaParse( result_type="markdown" # "markdown" and "text" are available )

# use SimpleDirectoryReader to parse our file file_extractor = {".pdf": parser} documents2 = SimpleDirectoryReader( "./data", file_extractor=file_extractor ).load_data() ```

``` Started parsing the file under job_id 84cb91f7-45ec-4b99-8281-0f4beef6a892 ```
``` index2 = VectorStoreIndex.from_documents(documents2) query_engine2 = index2.as_query_engine(similarity_top_k=20) ```

``` response = query_engine2.query( "What was the net gain in housing units in the Mission in 2021?" ) print(response) ```

``` The net gain in housing units in the Mission in 2021 was 1,305 units. ```
With a better parser, the LLM is able to answer the question correctly.
Now try a trickier question:
``` response = query_engine2.query( "How many affordable housing units were completed in 2021?" ) print(response) ```

``` Repeat: 110 ```
The LLM is getting confused; this appears to be the percentage increase in housing units.
Try giving the LLM more context (40 instead of 20) and then sorting those chunks with a reranker. Use NVIDIA’s reranker for this:
``` from llama_index.postprocessor.nvidia_rerank import NVIDIARerank
query_engine3 = index2.as_query_engine( similarity_top_k=40, node_postprocessors=[NVIDIARerank(top_n=10)] ) ```

``` response = query_engine3.query( "How many affordable housing units were completed in 2021?" ) print(response) ```

``` 1,495 ```
Excellent! Now the figure is correct (this is on page 35, in case you’re wondering).

[1] https://build.nvidia.com/
[2] https://build.nvidia.com
[3] https://docs.nvidia.com/nim/large-language- models/latest/getting-started.html