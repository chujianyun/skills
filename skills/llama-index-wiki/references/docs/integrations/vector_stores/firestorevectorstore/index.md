# developers.llamaindex.ai/python/framework/integrations/vector_stores/firestorevectorstore/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/firestorevectorstore/index.md

--- title: Firestore Vector Store | Developer Documentation ---

# Google Firestore (Native Mode)
> Firestore [1] is a serverless document-oriented database that scales to meet any demand. Extend your database application to build AI-powered experiences leveraging Firestore’s Langchain integrations.
This notebook goes over how to use Firestore [1] to store vectors and query them using the `FirestoreVectorStore` class.
## Before You Begin
To run this notebook, you will need to do the following:
- Create a Google Cloud Project [2] - Enable the Firestore API [3] - Create a Firestore database [4]
After confirmed access to database in the runtime environment of this notebook, filling the following values and run the cell before running example scripts.
## Library Installation
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙. For this notebook, we will also install `langchain-google-genai` to use Google Generative AI embeddings.
``` %pip install --quiet llama-index %pip install --quiet llama-index-vector-stores-firestore llama-index-embeddings-huggingface ```

### ☁ Set Your Google Cloud Project
Set your Google Cloud project so that you can leverage Google Cloud resources within this notebook.
If you don’t know your project ID, try the following:
- Run `gcloud config list`. - Run `gcloud projects list`. - See the support page: Locate the project ID [5].
``` # @markdown Please fill in the value below with your Google Cloud project ID and then run the cell.
PROJECT_ID = "YOUR_PROJECT_ID" # @param {type:"string"}
# Set the project id !gcloud config set project {PROJECT_ID} ```

### 🔐 Authentication
Authenticate to Google Cloud as the IAM user logged into this notebook in order to access your Google Cloud Project.
- If you are using Colab to run this notebook, use the cell below and continue. - If you are using Vertex AI Workbench, check out the setup instructions here [6].
``` from google.colab import auth
auth.authenticate_user() ```
# Basic Usage
### Initialize FirestoreVectorStore
`FirestoreVectroStore` allows you to load data into Firestore and query it.
``` # @markdown Please specify a source for demo purpose. COLLECTION_NAME = "test_collection" ```

``` from llama_index.core import SimpleDirectoryReader
# Load documents and build index documents = SimpleDirectoryReader( "../../examples/data/paul_graham" ).load_data() ```

``` from llama_index.embeddings.huggingface import HuggingFaceEmbedding from llama_index.core import Settings

# Set the embedding model, this is a local model embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5") ```
``` from llama_index.core import VectorStoreIndex from llama_index.core import StorageContext, ServiceContext

from llama_index.vector_stores.firestore import FirestoreVectorStore
# Create a Firestore vector store store = FirestoreVectorStore(collection_name=COLLECTION_NAME)
storage_context = StorageContext.from_defaults(vector_store=store) service_context = ServiceContext.from_defaults( llm=None, embed_model=embed_model )

index = VectorStoreIndex.from_documents( documents, storage_context=storage_context, service_context=service_context ) ```

``` /var/folders/mh/cqn7wzgs3j79rbg243_gfcx80000gn/T/ipykernel_29666/1668628626.py:10: DeprecationWarning: Call to deprecated class method from_defaults. (ServiceContext is deprecated, please use `llama_index.settings.Settings` instead.) -- Deprecated since version 0.10.0. service_context = ServiceContext.from_defaults(llm=None, embed_model=embed_model)

LLM is explicitly disabled. Using MockLLM. ```
### Perform search
You can use the `FirestoreVectorStore` to perform similarity searches on the vectors you have stored. This is useful for finding similar documents or text.
``` query_engine = index.as_query_engine() res = query_engine.query("What did the author do growing up?") print(str(res.source_nodes[0].text)) ```
``` None What I Worked On
February 2021
Before college the two main things I worked on, outside of school, were writing and programming. I didn't write essays. I wrote what beginning writers were supposed to write then, and probably still are: short stories. My stories were awful. They had hardly any plot, just characters with strong feelings, which I imagined made them deep.
The first programs I tried writing were on the IBM 1401 that our school district used for what was then called "data processing." This was in 9th grade, so I was 13 or 14. The school district's 1401 happened to be in the basement of our junior high school, and my friend Rich Draves and I got permission to use it. It was like a mini Bond villain's lair down there, with all these alien-looking machines — CPU, disk drives, printer, card reader — sitting up on a raised floor under bright fluorescent lights.
The language we used was an early version of Fortran. You had to type programs on punch cards, then stack them in the card reader and press a button to load the program into memory and run it. The result would ordinarily be to print something on the spectacularly loud printer.
I was puzzled by the 1401. I couldn't figure out what to do with it. And in retrospect there's not much I could have done with it. The only form of input to programs was data stored on punched cards, and I didn't have any data stored on punched cards. The only other option was to do things that didn't rely on any input, like calculate approximations of pi, but I didn't know enough math to do anything interesting of that type. So I'm not surprised I can't remember any programs I wrote, because they can't have done much. My clearest memory is of the moment I learned it was possible for programs not to terminate, when one of mine didn't. On a machine without time-sharing, this was a social as well as a technical error, as the data center manager's expression made clear.
With microcomputers, everything changed. Now you could have a computer sitting right in front of you, on a desk, that could respond to your keystrokes as it was running instead of just churning through a stack of punch cards and then stopping. [1]
The first of my friends to get a microcomputer built it himself. It was sold as a kit by Heathkit. I remember vividly how impressed and envious I felt watching him sitting in front of it, typing programs right into the computer.
Computers were expensive in those days and it took me years of nagging before I convinced my father to buy one, a TRS-80, in about 1980. The gold standard then was the Apple II, but a TRS-80 was good enough. This was when I really started programming. I wrote simple games, a program to predict how high my model rockets would fly, and a word processor that my father used to write at least one book. There was only room in memory for about 2 pages of text, so he'd write 2 pages at a time and then print them out, but it was a lot better than a typewriter.
Though I liked programming, I didn't plan to study it in college. In college I was going to study philosophy, which sounded much more powerful. It seemed, to my naive high school self, to be the study of the ultimate truths, compared to which the things studied in other fields would be mere domain knowledge. What I discovered when I got to college was that the other fields took up so much of the space of ideas that there wasn't much left for these supposed ultimate truths. All that seemed left for philosophy were edge cases that people in other fields felt could safely be ignored.
I couldn't have put this into words when I was 18. All I knew at the time was that I kept taking philosophy courses and they kept being boring. So I decided to switch to AI.
AI was in the air in the mid 1980s, but there were two things especially that made me want to work on it: a novel by Heinlein called The Moon is a Harsh Mistress, which featured an intelligent computer called Mike, and a PBS documentary that showed Terry Winograd using SHRDLU. I haven't tried rereading The Moon is a Harsh Mistress, so I don't know how well it has aged, but when I read it I was drawn entirely into its world. ```
You can apply pre-filtering to the search results by specifying a `filters` argument.
``` from llama_index.core.vector_stores.types import ( MetadataFilters, ExactMatchFilter, MetadataFilter, )

filters = MetadataFilters( filters=[MetadataFilter(key="author", value="Paul Graham")] ) query_engine = index.as_query_engine(filters=filters) res = query_engine.query("What did the author do growing up?") print(str(res.source_nodes[0].text)) ```

[1] https://cloud.google.com/firestore
[2] https://developers.google.com/workspace/guides/create-project
[3] https://console.cloud.google.com/flows/enableapi?apiid=firestore.googleapis.com
[4] https://cloud.google.com/firestore/docs/manage-databases
[5] https://support.google.com/googleapi/answer/7014113
[6] https://github.com/GoogleCloudPlatform/generative-ai/tree/main/setup-env