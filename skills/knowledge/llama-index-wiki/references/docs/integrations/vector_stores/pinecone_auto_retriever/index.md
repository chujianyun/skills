# developers.llamaindex.ai/python/framework/integrations/vector_stores/pinecone_auto_retriever/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/pinecone_auto_retriever/index.md

--- title: A Simple to Advanced Guide with Auto-Retrieval (with Pinecone + Arize Phoenix) | Developer Documentation ---

In this notebook we showcase how to perform **auto-retrieval** against Pinecone, which lets you execute a broad range of semi-structured queries beyond what you can do with standard top-k semantic search.

We show both how to setup basic auto-retrieval, as well as how to extend it (by customizing the prompt and through dynamic metadata retrieval).
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-vector-stores-pinecone ```
``` # !pip install llama-index>=0.9.31 scikit-learn==1.2.2 arize-phoenix==2.4.1 pinecone-client>=3.0.0 ```
## Part 1: Setup Auto-Retrieval
To setup auto-retrieval, do the following:
1. We’ll do some setup, load data, build a Pinecone vector index. 2. We’ll define our autoretriever and run some sample queries. 3. We’ll use Phoenix to observe each trace and visualize the prompt inputs/outputs. 4. We’ll show you how to customize the auto-retrieval prompt.

### 1.a Setup Pinecone/Phoenix, Load Data, and Build Vector Index
In this section we setup pinecone and ingest some toy data on books/movies (with text data and metadata).
We also setup Phoenix so that it captures downstream traces.
``` # setup Phoenix import phoenix as px import llama_index.core

px.launch_app() llama_index.core.set_global_handler("arize_phoenix") ```
``` 🌍 To view the Phoenix app in your browser, visit http://127.0.0.1:6006/ 📺 To view the Phoenix app in a notebook, run `px.active_session().view()` 📖 For more information on how to use Phoenix, check out https://docs.arize.com/phoenix ```

``` import os
os.environ[ "PINECONE_API_KEY" ] = "<Your Pinecone API key, from app.pinecone.io>" # os.environ["OPENAI_API_KEY"] = "sk-..." ```

``` from pinecone import Pinecone from pinecone import ServerlessSpec

api_key = os.environ["PINECONE_API_KEY"] pc = Pinecone(api_key=api_key) ```
``` # delete if needed # pc.delete_index("quickstart-index") ```

``` # Dimensions are for text-embedding-ada-002 try: pc.create_index( "quickstart-index", dimension=1536, metric="euclidean", spec=ServerlessSpec(cloud="aws", region="us-west-2"), ) except Exception as e: # Most likely index already exists print(e) pass ```

``` pinecone_index = pc.Index("quickstart-index") ```
#### Load documents, build the PineconeVectorStore and VectorStoreIndex
``` from llama_index.core import VectorStoreIndex, StorageContext from llama_index.vector_stores.pinecone import PineconeVectorStore ```

``` from llama_index.core.schema import TextNode
nodes = [ TextNode( text="The Shawshank Redemption", metadata={ "author": "Stephen King", "theme": "Friendship", "year": 1994, }, ), TextNode( text="The Godfather", metadata={ "director": "Francis Ford Coppola", "theme": "Mafia", "year": 1972, }, ), TextNode( text="Inception", metadata={ "director": "Christopher Nolan", "theme": "Fiction", "year": 2010, }, ), TextNode( text="To Kill a Mockingbird", metadata={ "author": "Harper Lee", "theme": "Fiction", "year": 1960, }, ), TextNode( text="1984", metadata={ "author": "George Orwell", "theme": "Totalitarianism", "year": 1949, }, ), TextNode( text="The Great Gatsby", metadata={ "author": "F. Scott Fitzgerald", "theme": "The American Dream", "year": 1925, }, ), TextNode( text="Harry Potter and the Sorcerer's Stone", metadata={ "author": "J.K. Rowling", "theme": "Fiction", "year": 1997, }, ), ] ```

``` vector_store = PineconeVectorStore( pinecone_index=pinecone_index, namespace="test", ) storage_context = StorageContext.from_defaults(vector_store=vector_store) ```

``` index = VectorStoreIndex(nodes, storage_context=storage_context) ```
``` Upserted vectors: 0%| | 0/7 [00:00<?, ?it/s] ```
### 1.b Define Autoretriever, Run Some Sample Queries
#### Setup the `VectorIndexAutoRetriever`

One of the inputs is a `schema` describing what content the vector store collection contains. This is similar to a table schema describing a table in the SQL database. This schema information is then injected into the prompt, which is passed to the LLM to infer what the full query should be (including metadata filters).

``` from llama_index.core.retrievers import VectorIndexAutoRetriever from llama_index.core.vector_stores import MetadataInfo, VectorStoreInfo

vector_store_info = VectorStoreInfo( content_info="famous books and movies", metadata_info=[ MetadataInfo( name="director", type="str", description=("Name of the director"), ), MetadataInfo( name="theme", type="str", description=("Theme of the book/movie"), ), MetadataInfo( name="year", type="int", description=("Year of the book/movie"), ), ], ) retriever = VectorIndexAutoRetriever( index, vector_store_info=vector_store_info, empty_query_top_k=10, # this is a hack to allow for blank queries in pinecone default_empty_query_vector=[0] * 1536, verbose=True, ) ```

#### Let’s run some queries
Let’s run some sample queries that make use of the structured information.
``` nodes = retriever.retrieve( "Tell me about some books/movies after the year 2000" ) ```

``` Using query str: Using filters: [('year', '>', 2000)] ```

``` Inception {'director': 'Christopher Nolan', 'theme': 'Fiction', 'year': 2010} ```
``` nodes = retriever.retrieve("Tell me about some books that are Fiction") ```
``` Using query str: Fiction Using filters: [('theme', '==', 'Fiction')] ```

``` Inception {'director': 'Christopher Nolan', 'theme': 'Fiction', 'year': 2010} To Kill a Mockingbird {'author': 'Harper Lee', 'theme': 'Fiction', 'year': 1960} ```

#### Pass in Additional Metadata Filters
If you have additional metadata filters you want to pass in that aren’t autoinferred, do the following.
``` from llama_index.core.vector_stores import MetadataFilters
filter_dicts = [{"key": "year", "operator": "==", "value": 1997}] filters = MetadataFilters.from_dicts(filter_dicts) retriever2 = VectorIndexAutoRetriever( index, vector_store_info=vector_store_info, empty_query_top_k=10, # this is a hack to allow for blank queries in pinecone default_empty_query_vector=[0] * 1536, extra_filters=filters, ) ```

``` nodes = retriever2.retrieve("Tell me about some books that are Fiction") for node in nodes: print(node.text) print(node.metadata) ```

``` Harry Potter and the Sorcerer's Stone {'author': 'J.K. Rowling', 'theme': 'Fiction', 'year': 1997} ```

#### Example of a failing Query
Note that no results are retrieved! We’ll fix this later on.
``` nodes = retriever.retrieve("Tell me about some books that are mafia-themed") ```
``` Using query str: books Using filters: [('theme', '==', 'mafia')] ```

### Visualize Traces
Let’s open up Phoenix to take a look at the traces!
[1]
Let’s take a look at the auto-retrieval prompt. We see that the auto-retrieval prompt makes use of two few-shot examples.
## Part 2: Extending Auto-Retrieval (with Dynamic Metadata Retrieval)
We now extend auto-retrieval by customizing the prompt. In the first part, we explicitly add some rules.

In the second part we implement **dynamic metadata retrieval**, which will do a first-stage retrieval pass of fetching relevant metadata from the vector db, and insert that as few-shot examples to the auto-retrieval prompt. (Of course, the second stage retrieval pass retrieves the actual items from the vector db).

### 2.a Improve the Auto-retrieval Prompt

Our auto-retrieval prompt works, but it can be improved in various ways. Some examples include the fact that it includes 2 hardcoded few-shot examples (how can you include your own?), and also the fact that the auto- retrieval doesn’t “always” infer the right metadata filters.

For instance, all the `theme` fields are capitalized. How do we tell the LLM that, so it doesn’t erroneously infer a “theme” that’s in lower-case?
Let’s take a stab at modifying the prompt!
``` from llama_index.core.prompts import display_prompt_dict from llama_index.core import PromptTemplate ```

``` prompts_dict = retriever.get_prompts() ```
``` display_prompt_dict(prompts_dict) ```
``` # look at required template variables. prompts_dict["prompt"].template_vars ```

``` ['schema_str', 'info_str', 'query_str'] ```
#### Customize the Prompt
Let’s customize the prompt a little bit. We do the following:
- Take out the first few-shot example to save tokens - Add a message to always capitalize a letter if inferring “theme”.
Note that the prompt template expects `schema_str`, `info_str`, and `query_str` to be defined.
```` # write prompt template, and modify it.
prompt_tmpl_str = """\ Your goal is to structure the user's query to match the request schema provided below.
<< Structured Request Schema >> When responding use a markdown code snippet with a JSON object formatted in the following schema:
{schema_str}

The query string should contain only text that is expected to match the contents of documents. Any conditions in the filter should not be mentioned in the query as well.

Make sure that filters only refer to attributes that exist in the data source. Make sure that filters take into account the descriptions of attributes. Make sure that filters are only used as needed. If there are no filters that should be applied return [] for the filter value. If the user's query explicitly mentions number of documents to retrieve, set top_k to that number, otherwise do not set top_k. Do NOT EVER infer a null value for a filter. This will break the downstream program. Instead, don't include the filter.

<< Example 1. >> Data Source: ```json {{ "metadata_info": [ {{ "name": "author", "type": "str", "description": "Author name" }}, {{ "name": "book_title", "type": "str", "description": "Book title" }}, {{ "name": "year", "type": "int", "description": "Year Published" }}, {{ "name": "pages", "type": "int", "description": "Number of pages" }}, {{ "name": "summary", "type": "str", "description": "A short summary of the book" }} ], "content_info": "Classic literature" }} ````

User Query: What are some books by Jane Austen published after 1813 that explore the theme of marriage for social standing?
Additional Instructions: None
Structured Request:

``` {{"query": "Books related to theme of marriage for social standing", "filters": [{{"key": "year", "value": "1813", "operator": ">"}}, {{"key": "author", "value": "Jane Austen", "operator": "=="}}], "top_k": null}} ```

<< Example 2. >> Data Source:
``` {info_str} ```
User Query: {query\_str}
Additional Instructions: {additional\_instructions}
Structured Request: """
```` ```python prompt_tmpl = PromptTemplate(prompt_tmpl_str) ````

You’ll notice we added an `additional_instructions` template variable. This allows us to insert vector collection-specific instructions.
We’ll use `partial_format` to add the instruction.

``` add_instrs = """\ If one of the filters is 'theme', please make sure that the first letter of the inferred value is capitalized. Only words that are capitalized are valid values for "theme". \ """ prompt_tmpl = prompt_tmpl.partial_format(additional_instructions=add_instrs) ```

``` retriever.update_prompts({"prompt": prompt_tmpl}) ```

``` nodes = retriever.retrieve( "Tell me about some books that are friendship-themed" ) ```
``` for node in nodes: print(node.text) print(node.metadata) ```
### 2.b Implement Dynamic Metadata Retrieval

An option besides hardcoding rules in the prompt is to retrieve **relevant few-shot examples of metadata**, to help the LLM better infer the correct metadata filters.

This will better prevent the LLM from making mistakes when inferring “where” clauses, especially around aspects like spelling / correct formatting of the value.

We can do this via vector retrieval. The existing vector db collection stores the raw text + metadata; we could query this collection directly, or separately only index the metadata and retrieve from that. In this section we choose to do the former but in practice you may want to do the latter.

``` # define retriever that fetches the top 2 examples. metadata_retriever = index.as_retriever(similarity_top_k=2) ```
We use the same `prompt_tmpl_str` defined in the previous section.
``` from typing import List, Any
def format_additional_instrs(**kwargs: Any) -> str: """Format examples into a string."""
nodes = metadata_retriever.retrieve(kwargs["query_str"]) context_str = ( "Here is the metadata of relevant entries from the database collection. " "This should help you infer the right filters: \n" ) for node in nodes: context_str += str(node.node.metadata) + "\n" return context_str

ext_prompt_tmpl = PromptTemplate( prompt_tmpl_str, function_mappings={"additional_instructions": format_additional_instrs}, ) ```
``` retriever.update_prompts({"prompt": ext_prompt_tmpl}) ```
#### Re-run some queries
Now let’s try rerunning some queries, and we’ll see that the value is auto-inferred.
``` nodes = retriever.retrieve("Tell me about some books that are mafia-themed") for node in nodes: print(node.text) print(node.metadata) ```
``` Using query str: books Using filters: [('theme', '==', 'Mafia')] The Godfather {'director': 'Francis Ford Coppola', 'theme': 'Mafia', 'year': 1972} ```
``` nodes = retriever.retrieve("Tell me some books authored by HARPER LEE") for node in nodes: print(node.text) print(node.metadata) ```
``` Using query str: Books authored by Harper Lee Using filters: [('author', '==', 'Harper Lee')] To Kill a Mockingbird {'author': 'Harper Lee', 'theme': 'Fiction', 'year': 1960} ```

[1] https://drive.google.com/uc?export=view\&id=1PCEwIdv7GcInk3i6ebd2WWjTp9ducG5F