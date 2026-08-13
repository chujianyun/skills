# developers.llamaindex.ai/python/framework/integrations/retrievers/reciprocal_rerank_fusion/index.md
> https://developers.llamaindex.ai/python/framework/integrations/retrievers/reciprocal_rerank_fusion/index.md

--- title: Reciprocal Rerank Fusion Retriever | Developer Documentation ---

In this example, we walk through how you can combine retrieval results from multiple queries and multiple indexes.
The retrieved nodes will be reranked according to the `Reciprocal Rerank Fusion` algorithm demonstrated in this paper [1]. It provides an effecient method for rerranking retrieval results without excessive computation or reliance on external models.
Full credits go to @Raduaschl on github for their example implementation here [2].
``` %pip install llama-index-llms-openai %pip install llama-index-retrievers-bm25 ```

``` import os import openai

os.environ["OPENAI_API_KEY"] = "sk-..." openai.api_key = os.environ["OPENAI_API_KEY"] ```
## Setup
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
Download Data
``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```

``` --2024-02-12 17:59:58-- https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 2606:50c0:8003::154, 2606:50c0:8001::154, 2606:50c0:8002::154, ... Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|2606:50c0:8003::154|:443... connected. HTTP request sent, awaiting response... 200 OK Length: 75042 (73K) [text/plain] Saving to: ‘data/paul_graham/paul_graham_essay.txt’

data/paul_graham/pa 100%[===================>] 73.28K 327KB/s in 0.2s
2024-02-12 17:59:59 (327 KB/s) - ‘data/paul_graham/paul_graham_essay.txt’ saved [75042/75042] ```
``` from llama_index.core import SimpleDirectoryReader
documents = SimpleDirectoryReader("./data/paul_graham/").load_data() ```
Next, we will setup a vector index over the documentation.
``` from llama_index.core import VectorStoreIndex from llama_index.core.node_parser import SentenceSplitter

splitter = SentenceSplitter(chunk_size=256)
index = VectorStoreIndex.from_documents(documents, transformations=[splitter]) ```
## Create a Hybrid Fusion Retriever
In this step, we fuse our index with a BM25 based retriever. This will enable us to capture both semantic relations and keywords in our input queries.
Since both of these retrievers calculate a score, we can use the reciprocal rerank algorithm to re-sort our nodes without using an additional models or excessive computation.
This setup will also query 4 times, once with your original query, and generate 3 more queries.
By default, it uses the following prompt to generate extra queries:
``` QUERY_GEN_PROMPT = ( "You are a helpful assistant that generates multiple search queries based on a " "single input query. Generate {num_queries} search queries, one on each line, " "related to the following input query:\n" "Query: {query}\n" "Queries:\n" ) ```

First, we create our retrievers. Each will retrieve the top-2 most similar nodes:
``` from llama_index.retrievers.bm25 import BM25Retriever
vector_retriever = index.as_retriever(similarity_top_k=2)
bm25_retriever = BM25Retriever.from_defaults( docstore=index.docstore, similarity_top_k=2 ) ```

Next, we can create our fusion retriever, which well return the top-2 most similar nodes from the 4 returned nodes from the retrievers:
``` from llama_index.core.retrievers import QueryFusionRetriever
retriever = QueryFusionRetriever( [vector_retriever, bm25_retriever], similarity_top_k=2, num_queries=4, # set this to 1 to disable query generation mode="reciprocal_rerank", use_async=True, verbose=True, # query_gen_prompt="...", # we could override the query generation prompt here ) ```

``` # apply nested async to run in a notebook import nest_asyncio

nest_asyncio.apply() ```
``` nodes_with_scores = retriever.retrieve( "What happened at Interleafe and Viaweb?" ) ```

``` Generated queries: 1. What were the major events or milestones in the history of Interleafe and Viaweb? 2. Can you provide a timeline of the key developments and achievements of Interleafe and Viaweb? 3. What were the successes and failures of Interleafe and Viaweb as companies? ```

``` for node in nodes_with_scores: print(f"Score: {node.score:.2f} - {node.text}...\n-----\n") ```

``` Score: 0.03 - The UI was horrible, but it proved you could build a whole store through the browser, without any client software or typing anything into the command line on the server.
Now we felt like we were really onto something. I had visions of a whole new generation of software working this way. You wouldn't need versions, or ports, or any of that crap. At Interleaf there had been a whole group called Release Engineering that seemed to be at least as big as the group that actually wrote the software. Now you could just update the software right on the server.
We started a new company we called Viaweb, after the fact that our software worked via the web, and we got $10,000 in seed funding from Idelle's husband Julian. In return for that and doing the initial legal work and giving us business advice, we gave him 10% of the company. Ten years later this deal became the model for Y Combinator's. We knew founders needed something like this, because we'd needed it ourselves.... -----

Score: 0.03 - Now we felt like we were really onto something. I had visions of a whole new generation of software working this way. You wouldn't need versions, or ports, or any of that crap. At Interleaf there had been a whole group called Release Engineering that seemed to be at least as big as the group that actually wrote the software. Now you could just update the software right on the server.
We started a new company we called Viaweb, after the fact that our software worked via the web, and we got $10,000 in seed funding from Idelle's husband Julian. In return for that and doing the initial legal work and giving us business advice, we gave him 10% of the company. Ten years later this deal became the model for Y Combinator's. We knew founders needed something like this, because we'd needed it ourselves.
At this stage I had a negative net worth, because the thousand dollars or so I had in the bank was more than counterbalanced by what I owed the government in taxes. (Had I diligently set aside the proper proportion of the money I'd made consulting for Interleaf?... ----- ```

As we can see, both retruned nodes correctly mention Viaweb and Interleaf!
## Use in a Query Engine!
Now, we can plug our retriever into a query engine to synthesize natural language responses.
``` from llama_index.core.query_engine import RetrieverQueryEngine
query_engine = RetrieverQueryEngine.from_args(retriever) ```
``` response = query_engine.query("What happened at Interleafe and Viaweb?") ```
``` Generated queries: 1. What were the major events or milestones in the history of Interleafe and Viaweb? 2. Can you provide a timeline of the key developments and achievements of Interleafe and Viaweb? 3. What were the outcomes or impacts of Interleafe and Viaweb on the respective industries they operated in? ```

``` from llama_index.core.response.notebook_utils import display_response
display_response(response) ```
**`Final Response:`** At Interleaf, there was a group called Release Engineering that was as big as the group that actually wrote the software. This suggests that there was a significant focus on managing versions and ports of the software. However, at Viaweb, the founders realized that they could update the software directly on the server, eliminating the need for versions and ports. They started Viaweb, a company that built software that worked via the web. They received $10,000 in seed funding and gave 10% of the company to Julian, who provided the funding and business advice. This deal later became the model for Y Combinator’s.

[1] https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf
[2] https://github.com/Raudaschl/rag-fusion