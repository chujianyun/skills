# developers.llamaindex.ai/python/framework/integrations/vector_stores/deeplakeindexdemo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/deeplakeindexdemo/index.md

--- title: Deep Lake Vector Store Quickstart | Developer Documentation ---

Deep Lake can be installed using pip.
``` %pip install llama-index-vector-stores-deeplake ```
``` !pip install llama-index !pip install deeplake ```

Next, let’s import the required modules and set the needed environmental variables:
``` import os import textwrap

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document from llama_index.vector_stores.deeplake import DeepLakeVectorStore
os.environ["OPENAI_API_KEY"] = "sk-********************************" os.environ["ACTIVELOOP_TOKEN"] = "********************************" ```

We are going to embed and store one of Paul Graham’s essays in a Deep Lake Vector Store stored locally. First, we download the data to a directory called `data/paul_graham`

``` import urllib.request
urllib.request.urlretrieve( "https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt", "data/paul_graham/paul_graham_essay.txt", ) ```
We can now create documents from the source data file.
``` # load documents documents = SimpleDirectoryReader("./data/paul_graham/").load_data() print( "Document ID:", documents[0].doc_id, "Document Hash:", documents[0].hash, ) ```

``` Document ID: a98b6686-e666-41a9-a0bc-b79f0d666bde Document Hash: beaa54b3e9cea641e91e6975d2207af4f4200f4b2d629725d688f272372ce5bb ```

Finally, let’s create the Deep Lake Vector Store and populate it with data. We use a default tensor configuration, which creates tensors with `text (str)`, `metadata(json)`, `id (str, auto-populated)`, `embedding (float32)`. Learn more about tensor customizability here [1].

``` from llama_index.core import StorageContext
dataset_path = "./dataset/paul_graham"
# Create an index over the documents vector_store = DeepLakeVectorStore(dataset_path=dataset_path, overwrite=True) storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( documents, storage_context=storage_context ) ```

``` Uploading data to deeplake dataset.
100%|██████████| 22/22 [00:00<00:00, 684.80it/s]
Dataset(path='./dataset/paul_graham', tensors=['text', 'metadata', 'embedding', 'id'])
tensor htype shape dtype compression ------- ------- ------- ------- ------- text text (22, 1) str None metadata json (22, 1) str None embedding embedding (22, 1536) float32 None id text (22, 1) str None ```

## Performing Vector Search

Deep Lake offers highly-flexible vector search and hybrid search options discussed in detail in these tutorials [2]. In this Quickstart, we show a simple example using default options.

``` query_engine = index.as_query_engine() response = query_engine.query( "What did the author learn?", ) ```

``` The author learned that working on things that are not prestigious can be a good thing, as it can lead to discovering something real and avoiding the wrong track. The author also learned that ignorance can be beneficial, as it can lead to discovering something new and unexpected. The author also learned the importance of working hard, even at the parts of the job they don't like, in order to set an example for others. The author also learned the value of unsolicited advice, as it can be beneficial in unexpected ways, such as when Robert Morris suggested that the author should make sure Y Combinator wasn't the last cool thing they did. ```

``` response = query_engine.query("What was a hard moment for the author?") ```
``` print(textwrap.fill(str(response), 100)) ```

``` query_engine = index.as_query_engine() response = query_engine.query("What was a hard moment for the author?") print(textwrap.fill(str(response), 100)) ```

``` The author experienced a hard moment when one of his programs on the IBM 1401 computer did not terminate. This was a social as well as a technical error, as the data center manager's expression made clear. ```

## Deleting items from the database
To find the id of a document to delete, you can query the underlying deeplake dataset directly
``` import deeplake
ds = deeplake.load(dataset_path)
idx = ds.id[0].numpy().tolist() idx ```
``` ./dataset/paul_graham loaded successfully.

['42f8220e-673d-4c65-884d-5a48a1a15b03'] ```
``` index.delete(idx[0]) ```

[1] https://docs.activeloop.ai/example-code/getting-started/vector-store/step-4-customizing-vector-stores
[2] https://docs.activeloop.ai/example-code/tutorials/vector-store/vector-search-options