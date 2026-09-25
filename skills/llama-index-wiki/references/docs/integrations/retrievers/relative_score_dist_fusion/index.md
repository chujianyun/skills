# developers.llamaindex.ai/python/framework/integrations/retrievers/relative_score_dist_fusion/index.md
> https://developers.llamaindex.ai/python/framework/integrations/retrievers/relative_score_dist_fusion/index.md

--- title: Relative Score Fusion and Distribution-Based Score Fusion | Developer Documentation ---

In this example, we demonstrate using QueryFusionRetriever with two methods which aim to improve on Reciprocal Rank Fusion:
1. Relative Score Fusion (Weaviate [1]) 2. Distribution-Based Score Fusion (Mazzeschi: blog post [2])
``` %pip install llama-index-llms-openai %pip install llama-index-retrievers-bm25 ```

``` import os import openai

os.environ["OPENAI_API_KEY"] = "sk-..." openai.api_key = os.environ["OPENAI_API_KEY"] ```
## Setup
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
Download Data
``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

``` from llama_index.core import SimpleDirectoryReader
documents = SimpleDirectoryReader("./data/paul_graham/").load_data() ```
Next, we will setup a vector index over the documentation.
``` from llama_index.core import VectorStoreIndex from llama_index.core.node_parser import SentenceSplitter

splitter = SentenceSplitter(chunk_size=256)
index = VectorStoreIndex.from_documents( documents, transformations=[splitter], show_progress=True ) ```

``` Parsing nodes: 100%|██████████| 1/1 [00:00<00:00, 7.55it/s] Generating embeddings: 100%|██████████| 504/504 [00:03<00:00, 128.32it/s] ```

## Create a Hybrid Fusion Retriever using Relative Score Fusion
In this step, we fuse our index with a BM25 based retriever. This will enable us to capture both semantic relations and keywords in our input queries.
Since both of these retrievers calculate a score, we can use the `QueryFusionRetriever` to re-sort our nodes without using an additional models or excessive computation.
The following example uses the Relative Score Fusion [1] algorithm from Weaviate, which applies a MinMax scaler to each result set, then makes a weighted sum. Here, we’ll give the vector retriever slightly more weight than BM25 (0.6 vs. 0.4).
First, we create our retrievers. Each will retrieve the top-10 most similar nodes.
``` from llama_index.retrievers.bm25 import BM25Retriever
vector_retriever = index.as_retriever(similarity_top_k=5)
bm25_retriever = BM25Retriever.from_defaults( docstore=index.docstore, similarity_top_k=10 ) ```

Next, we can create our fusion retriever, which well return the top-10 most similar nodes from the 20 returned nodes from the retrievers.
Note that the vector and BM25 retrievers may have returned all the same nodes, only in different orders; in this case, it simply acts as a re-ranker.

retriever = QueryFusionRetriever( [vector_retriever, bm25_retriever], retriever_weights=[0.6, 0.4], similarity_top_k=10, num_queries=1, # set this to 1 to disable query generation mode="relative_score", use_async=True, verbose=True, ) ```

``` # apply nested async to run in a notebook import nest_asyncio
nest_asyncio.apply() ```
``` nodes_with_scores = retriever.retrieve( "What happened at Interleafe and Viaweb?" ) ```
``` for node in nodes_with_scores: print(f"Score: {node.score:.2f} - {node.text[:100]}...\n-----") ```
``` Score: 0.60 - You wouldn't need versions, or ports, or any of that crap. At Interleaf there had been a whole group... ----- Score: 0.59 - The UI was horrible, but it proved you could build a whole store through the browser, without any cl... ----- Score: 0.40 - We were determined to be the Microsoft Word, not the Interleaf. Which meant being easy to use and in... ----- Score: 0.36 - In its time, the editor was one of the best general-purpose site builders. I kept the code tight and... ----- Score: 0.25 - I kept the code tight and didn't have to integrate with any other software except Robert's and Trevo... ----- Score: 0.25 - If all I'd had to do was work on this software, the next 3 years would have been the easiest of my l...

----- Score: 0.21 - To find out, we decided to try making a version of our store builder that you could control through ... ----- Score: 0.11 - But the most important thing I learned, and which I used in both Viaweb and Y Combinator, is that th... ----- Score: 0.11 - The next year, from the summer of 1998 to the summer of 1999, must have been the least productive of... ----- Score: 0.07 - The point is that it was really cheap, less than half market price.

[8] Most software you can launc... ----- ```
### Distribution-Based Score Fusion
A variant on Relative Score Fusion, Distribution-Based Score Fusion [2] scales the scores a bit differently - based on the mean and standard deviation of the scores for each result set.
``` from llama_index.core.retrievers import QueryFusionRetriever
retriever = QueryFusionRetriever( [vector_retriever, bm25_retriever], retriever_weights=[0.6, 0.4], similarity_top_k=10, num_queries=1, # set this to 1 to disable query generation mode="dist_based_score", use_async=True, verbose=True, )

nodes_with_scores = retriever.retrieve( "What happened at Interleafe and Viaweb?" )
for node in nodes_with_scores: print(f"Score: {node.score:.2f} - {node.text[:100]}...\n-----") ```
``` Score: 0.42 - You wouldn't need versions, or ports, or any of that crap. At Interleaf there had been a whole group... ----- Score: 0.41 - The UI was horrible, but it proved you could build a whole store through the browser, without any cl... ----- Score: 0.32 - We were determined to be the Microsoft Word, not the Interleaf. Which meant being easy to use and in... ----- Score: 0.30 - In its time, the editor was one of the best general-purpose site builders. I kept the code tight and... ----- Score: 0.27 - To find out, we decided to try making a version of our store builder that you could control through ... ----- Score: 0.24 - I kept the code tight and didn't have to integrate with any other software except Robert's and Trevo...

----- Score: 0.24 - If all I'd had to do was work on this software, the next 3 years would have been the easiest of my l... ----- Score: 0.20 - Now we felt like we were really onto something. I had visions of a whole new generation of software ... ----- Score: 0.20 - Users wouldn't need anything more than a browser.

This kind of software, known as a web app, is com... ----- Score: 0.18 - But the most important thing I learned, and which I used in both Viaweb and Y Combinator, is that th... ----- ```
## Use in a Query Engine!
Now, we can plug our retriever into a query engine to synthesize natural language responses.
``` from llama_index.core.query_engine import RetrieverQueryEngine
query_engine = RetrieverQueryEngine.from_args(retriever) ```
``` response = query_engine.query("What happened at Interleafe and Viaweb?") ```
``` from llama_index.core.response.notebook_utils import display_response
display_response(response) ```
**`Final Response:`** At Interleaf, there was a group called Release Engineering that was as large as the group writing the software. They had to deal with versions, ports, and other complexities. In contrast, at Viaweb, the software could be updated directly on the server, simplifying the process. Viaweb was founded with $10,000 in seed funding, and the software allowed building a whole store through the browser without the need for client software or command line inputs on the server. The company aimed to be easy to use and inexpensive, offering low monthly prices for their services.

[1] https://weaviate.io/blog/hybrid-search-fusion-algorithms
[2] https://medium.com/plain-simple-software/distribution-based-score-fusion-dbsf-a-new-approach-to-vector-search-ranking-f87c37488b18