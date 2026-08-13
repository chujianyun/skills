# developers.llamaindex.ai/python/framework/integrations/vector_stores/moorchehdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/moorchehdemo/index.md

--- title: Moorcheh Vector Store Demo | Developer Documentation ---

## Install Required Packages
``` !pip install llama_index !pip install moorcheh_sdk ```

## Import Required Libraries
demo.py
``` # --- Welcome to the Demo of the Moorcheh Vector Store --- # --- Import the following packages -- import logging import sys import os from moorcheh_sdk import MoorchehClient from IPython.display import Markdown, display from typing import Any, Callable, Dict, List, Optional, cast from llama_index.core import ( VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings, ) from llama_index.core.base.embeddings.base_sparse import BaseSparseEmbedding from llama_index.core.bridge.pydantic import PrivateAttr from llama_index.core.schema import BaseNode, MetadataMode, TextNode from llama_index.core.vector_stores.types import ( BasePydanticVectorStore, MetadataFilters, VectorStoreQuery, VectorStoreQueryMode, VectorStoreQueryResult, ) from llama_index.core.vector_stores.utils import ( DEFAULT_TEXT_KEY, legacy_metadata_dict_to_node, metadata_dict_to_node, node_to_metadata_dict, ) from llama_index.core.vector_stores.types import ( MetadataFilter, MetadataFilters, FilterOperator, FilterCondition, ) ```

## Configure Logging
``` # --- Logging Setup --- logging.basicConfig(stream=sys.stdout, level=logging.INFO) logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout)) ```

## Load Moorcheh API Key
``` # --- Set the values of the API Keys in your Environment Variables --- from google.colab import userdata

api_key = os.environ["MOORCHEH_API_KEY"] = userdata.get("MOORCHEH_API_KEY")
if "MOORCHEH_API_KEY" not in os.environ: raise EnvironmentError(f"Environment variable MOORCHEH_API_KEY is not set") ```
## Load and Chunk Documents
``` # --- Load Documents --- documents = SimpleDirectoryReader("./documents").load_data()

# --- Set chunk size and overlap --- Settings.chunk_size = 1024 Settings.chunk_overlap = 20 ```

## Initialize Vector Store and Create Index
``` # --- Initialize the Moorcheh Vector Store --- __all__ = ["MoorchehVectorStore"]

# Creates a Moorcheh Vector Store with the following parameters # For text-based namespaces, set namespace_type to "text" and vector_dimension to None # For vector-based namespaces, set namespace_type to "vector" and vector_dimension to the dimension of your uploaded vectors vector_store = MoorchehVectorStore( api_key=api_key, namespace="llamaindex_moorcheh", namespace_type="text", vector_dimension=None, add_sparse_vector=False, batch_size=100, )

# --- Create a Vector Store Index using the Vector Store and given Documents --- storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```
## Query the Vector Store
``` # --- Generate Response --- # --- Set Logging to DEBUG for more Detailed Outputs --- query_engine = index.as_query_engine() response = vector_store.generate_answer( query="Which company has had the highest revenue in 2025 and why?" ) moorcheh_response = vector_store.get_generative_answer( query="Which company has had the highest revenue in 2025 and why?", ai_model="anthropic.claude-3-7-sonnet-20250219-v1:0", )
display(Markdown(f"<b>{response}</b>")) print( "\n\n================================\n\n", response, "\n\n================================\n\n", ) print( "\n\n================================\n\n", moorcheh_response, "\n\n================================\n\n", )
# --- Filters for Metadata --- filter = MetadataFilters( filters=[ MetadataFilter( key="file_path", value="insert the file path to the document here", operator=FilterOperator.EQ, ) ], condition=FilterCondition.AND, ) ```