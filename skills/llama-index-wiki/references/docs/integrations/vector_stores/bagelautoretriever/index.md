# developers.llamaindex.ai/python/framework/integrations/vector_stores/bagelautoretriever/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/bagelautoretriever/index.md

--- title: Bagel Vector Store | Developer Documentation ---
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-vector-stores-bagel %pip install llama-index %pip install bagelML ```
``` import logging import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO) logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout)) ```
``` # set up OpenAI import os import getpass
os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:") import openai
openai.api_key = os.environ["OPENAI_API_KEY"] ```
``` import os
# Set environment variable os.environ["BAGEL_API_KEY"] = getpass.getpass("Bagel API Key:") ```
``` import bagel from bagel import Settings ```
``` server_settings = Settings( bagel_api_impl="rest", bagel_server_host="api.bageldb.ai" )
client = bagel.Client(server_settings)
collection = client.get_or_create_cluster( "testing_embeddings_3", embedding_model="custom", dimension=1536 ) ```
``` from llama_index.core import VectorStoreIndex, StorageContext from llama_index.vector_stores.bagel import BagelVectorStore ```
``` from llama_index.core.schema import TextNode
nodes = [ TextNode( text=( "Michael Jordan is a retired professional basketball player," " widely regarded as one of the greatest basketball players of all" " time." ), metadata={ "category": "Sports", "country": "United States", }, ), TextNode( text=( "Angelina Jolie is an American actress, filmmaker, and" " humanitarian. She has received numerous awards for her acting" " and is known for her philanthropic work." ), metadata={ "category": "Entertainment", "country": "United States", }, ), TextNode( text=( "Elon Musk is a business magnate, industrial designer, and" " engineer. He is the founder, CEO, and lead designer of SpaceX," " Tesla, Inc., Neuralink, and The Boring Company." ), metadata={ "category": "Business", "country": "United States", }, ), TextNode( text=( "Rihanna is a Barbadian singer, actress, and businesswoman. She" " has achieved significant success in the music industry and is" " known for her versatile musical style."

), metadata={ "category": "Music", "country": "Barbados", }, ), TextNode( text=( "Cristiano Ronaldo is a Portuguese professional footballer who is" " considered one of the greatest football players of all time. He" " has won numerous awards and set multiple records during his" " career." ), metadata={ "category": "Sports", "country": "Portugal", }, ), ] ```

``` vector_store = BagelVectorStore(collection=collection) storage_context = StorageContext.from_defaults(vector_store=vector_store) ```
``` index = VectorStoreIndex(nodes, storage_context=storage_context) ```
``` from llama_index.core.retrievers import VectorIndexAutoRetriever from llama_index.core.vector_stores import MetadataInfo, VectorStoreInfo
vector_store_info = VectorStoreInfo( content_info="brief biography of celebrities", metadata_info=[ MetadataInfo( name="category", type="str", description=( "Category of the celebrity, one of [Sports, Entertainment," " Business, Music]" ), ), MetadataInfo( name="country", type="str", description=( "Country of the celebrity, one of [United States, Barbados," " Portugal]" ), ), ], ) retriever = VectorIndexAutoRetriever( index, vector_store_info=vector_store_info ) ```

``` retriever.retrieve("celebrity") ```