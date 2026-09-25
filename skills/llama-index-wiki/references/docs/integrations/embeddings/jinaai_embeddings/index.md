# developers.llamaindex.ai/python/framework/integrations/embeddings/jinaai_embeddings/index.md
> https://developers.llamaindex.ai/python/framework/integrations/embeddings/jinaai_embeddings/index.md

--- title: Jina Embeddings | Developer Documentation ---

If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-embeddings-jinaai %pip install llama-index-llms-openai ```

``` !pip install llama-index ```
You may also need other packages that do not come direcly with llama-index
``` !pip install Pillow ```
For this example, you will need an API key which you can get from <https://jina.ai/embeddings/>
``` # Initilise with your api key import os

jinaai_api_key = "<API_KEY>" os.environ["JINAAI_API_KEY"] = jinaai_api_key ```
## Embed text and queries with Jina embedding models through JinaAI API
You can encode your text and your queries using the JinaEmbedding class. Jina offers a range of models adaptable to various use cases.
| Model | Dimension | Language | MRL (matryoshka) | Context | | :------------------------: | :-------: | :-------------------------: | :--------------: | :-----: | | jina-embeddings-v3 | 1024 | Multilingual (89 languages) | Yes | 8192 | | jina-embeddings-v2-base-en | 768 | English | No | 8192 | | jina-embeddings-v2-base-de | 768 | German & English | No | 8192 | | jina-embeddings-v2-base-es | 768 | Spanish & English | No | 8192 | | jina-embeddings-v2-base-zh | 768 | Chinese & English | No | 8192 |

**Recommended Model: jina-embeddings-v3 :**

We recommend `jina-embeddings-v3` as the latest and most performant embedding model from Jina AI. This model features 5 task-specific adapters trained on top of its backbone, optimizing various embedding use cases.

By default `JinaEmbedding` class uses `jina-embeddings-v3`. On top of the backbone, `jina-embeddings-v3` has been trained with 5 task-specific adapters for different embedding uses.

**Task-Specific Adapters:**
Include `task` in your request to optimize your downstream application:
- **retrieval.query**: Used to encode user queries or questions in retrieval tasks. - **retrieval.passage**: Used to encode large documents in retrieval tasks at indexing time. - **classification**: Used to encode text for text classification tasks. - **text-matching**: Used to encode text for similarity matching, such as measuring similarity between two sentences. - **separation**: Used for clustering or reranking tasks.

**Matryoshka Representation Learning**:
`jina-embeddings-v3` supports Matryoshka Representation Learning, allowing users to control the embedding dimension with minimal performance loss.\ Include `dimensions` in your request to select the desired dimension.\ By default, **dimensions** is set to 1024, and a number between 256 and 1024 is recommended.\ You can reference the table below for hints on dimension vs. performance:

| Dimension | 32 | 64 | 128 | 256 | 512 | 768 | 1024 | | :--------------------------------------: | :---: | :---: | :---: | :---: | :---: | :--: | :---: | | Average Retrieval Performance (nDCG\@10) | 52.54 | 58.54 | 61.64 | 62.72 | 63.16 | 63.3 | 63.35 |
**Late Chunking in Long-Context Embedding Models**

`jina-embeddings-v3` supports Late Chunking [1], the technique to leverage the model’s long-context capabilities for generating contextual chunk embeddings. Include `late_chunking=True` in your request to enable contextual chunked representation. When set to true, Jina AI API will concatenate all sentences in the input field and feed them as a single string to the model. Internally, the model embeds this long concatenated string and then performs late chunking, returning a list of embeddings that matches the size of the input list.

``` from llama_index.embeddings.jinaai import JinaEmbedding
text_embed_model = JinaEmbedding( api_key=jinaai_api_key, model="jina-embeddings-v3", # choose `retrieval.passage` to get passage embeddings task="retrieval.passage", )
embeddings = text_embed_model.get_text_embedding("This is the text to embed") print("Text dim:", len(embeddings)) print("Text embed:", embeddings[:5])
query_embed_model = JinaEmbedding( api_key=jinaai_api_key, model="jina-embeddings-v3", # choose `retrieval.query` to get query embeddings, or choose your desired task type task="retrieval.query", # `dimensions` allows users to control the embedding dimension with minimal performance loss. by default it is 1024. # A number between 256 and 1024 is recommended. dimensions=512, )

embeddings = query_embed_model.get_query_embedding( "This is the query to embed" ) print("Query dim:", len(embeddings)) print("Query embed:", embeddings[:5]) ```
## Embed images and queries with Jina CLIP through JinaAI API
You can also encode your images and your queries using the JinaEmbedding class
``` from llama_index.embeddings.jinaai import JinaEmbedding from PIL import Image import requests from numpy import dot from numpy.linalg import norm
embed_model = JinaEmbedding( api_key=jinaai_api_key, model="jina-clip-v1", )
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStMP8S3VbNCqOQd7QQQcbvC_FLa1HlftCiJw&s" im = Image.open(requests.get(image_url, stream=True).raw) print("Image:") display(im)
image_embeddings = embed_model.get_image_embedding(image_url) print("Image dim:", len(image_embeddings)) print("Image embed:", image_embeddings[:5])
text_embeddings = embed_model.get_text_embedding( "Logo of a pink blue llama on dark background" ) print("Text dim:", len(text_embeddings)) print("Text embed:", text_embeddings[:5])
cos_sim = dot(image_embeddings, text_embeddings) / ( norm(image_embeddings) * norm(text_embeddings) ) print("Cosine similarity:", cos_sim) ```
## Embed in batches

You can also embed text in batches, the batch size can be controlled by setting the `embed_batch_size` parameter (the default value will be 10 if not passed, and it should not be larger than 2048)

``` embed_model = JinaEmbedding( api_key=jinaai_api_key, model="jina-embeddings-v3", embed_batch_size=16, task="retrieval.passage", )

embeddings = embed_model.get_text_embedding_batch( ["This is the text to embed", "More text can be provided in a batch"] )
print(len(embeddings)) print(embeddings[0][:5]) ```
## Let’s build a RAG pipeline using Jina AI Embeddings
#### Download Data

``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

#### Imports
``` import logging import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO) logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI from llama_index.core.response.notebook_utils import display_source_node
from IPython.display import Markdown, display ```
#### Load Data
``` documents = SimpleDirectoryReader("./data/paul_graham/").load_data() ```
#### Build index
``` your_openai_key = "YOUR_OPENAI_KEY" llm = OpenAI(api_key=your_openai_key) embed_model = JinaEmbedding( api_key=jinaai_api_key, model="jina-embeddings-v3", embed_batch_size=16, task="retrieval.passage", )

index = VectorStoreIndex.from_documents( documents=documents, embed_model=embed_model ) ```

#### Build retriever
``` search_query_retriever = index.as_retriever()
search_query_retrieved_nodes = search_query_retriever.retrieve( "What happened after the thesis?" ) ```

``` for n in search_query_retrieved_nodes: display_source_node(n, source_length=2000) ```

[1] https://jina.ai/news/late-chunking-in-long-context-embedding-models/