# developers.llamaindex.ai/python/framework/integrations/vector_stores/qdrant_using_qdrant_filters/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/qdrant_using_qdrant_filters/index.md

--- title: Qdrant Vector Store - Default Qdrant Filters | Developer Documentation ---
Example on how to use Filters from the qdrant\_client SDK directly in your Retriever / Query Engine
``` %pip install llama-index-vector-stores-qdrant ```
``` !pip3 install llama-index qdrant_client ```
``` import openai import qdrant_client from IPython.display import Markdown, display from llama_index.core import VectorStoreIndex from llama_index.core import StorageContext from llama_index.vector_stores.qdrant import QdrantVectorStore from qdrant_client.http.models import Filter, FieldCondition, MatchValue

client = qdrant_client.QdrantClient(location=":memory:") from llama_index.core.schema import TextNode
nodes = [ TextNode( text="りんごとは", metadata={"author": "Tanaka", "fruit": "apple", "city": "Tokyo"}, ), TextNode( text="Was ist Apfel?", metadata={"author": "David", "fruit": "apple", "city": "Berlin"}, ), TextNode( text="Orange like the sun", metadata={"author": "Jane", "fruit": "orange", "city": "Hong Kong"}, ), TextNode( text="Grape is...", metadata={"author": "Jane", "fruit": "grape", "city": "Hong Kong"}, ), TextNode( text="T-dot > G-dot", metadata={"author": "George", "fruit": "grape", "city": "Toronto"}, ), TextNode( text="6ix Watermelons", metadata={ "author": "George", "fruit": "watermelon", "city": "Toronto", }, ), ]

openai.api_key = "<API_KEY>" vector_store = QdrantVectorStore( client=client, collection_name="fruit_collection" ) storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex(nodes, storage_context=storage_context)

# Use filters directly from qdrant_client python library # View python examples here for more info https://qdrant.tech/documentation/concepts/filtering/
filters = Filter( should=[ Filter( must=[ FieldCondition( key="fruit", match=MatchValue(value="apple"), ), FieldCondition( key="city", match=MatchValue(value="Tokyo"), ), ] ), Filter( must=[ FieldCondition( key="fruit", match=MatchValue(value="grape"), ), FieldCondition( key="city", match=MatchValue(value="Toronto"), ), ] ), ] )

retriever = index.as_retriever(vector_store_kwargs={"qdrant_filters": filters})
response = retriever.retrieve("Who makes grapes?") for node in response: print("node", node.score) print("node", node.text) print("node", node.metadata) ```