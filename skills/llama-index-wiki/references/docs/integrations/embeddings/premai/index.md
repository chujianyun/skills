# developers.llamaindex.ai/python/framework/integrations/embeddings/premai/index.md
> https://developers.llamaindex.ai/python/framework/integrations/embeddings/premai/index.md

--- title: PremAI Embeddings | Developer Documentation ---

PremAI [1] is an all-in-one platform that simplifies the creation of robust, production-ready applications powered by Generative AI. By streamlining the development process, PremAI allows you to concentrate on enhancing user experience and driving overall growth for your application. You can quickly start using our platform here [2].
In this section we are going to dicuss how we can get access to different embedding model using `PremEmbeddings` with llama-index
## Installation and setup
We start by installing `llama-index` and `premai-sdk`. You can type the following command to install:
Terminal window
``` pip install premai llama-index ```
Before proceeding further, please make sure that you have made an account on PremAI and already created a project. If not, please refer to the quick start [3] guide to get started with the PremAI platform. Create your first project and grab your API key.
``` %pip install llama-index-llms-premai ```
``` from llama_index.embeddings.premai import PremAIEmbeddings ```
## Setup PremAIEmbeddings instance in LlamaIndex
Once we imported our required modules, let’s setup our client. For now let’s assume that our `project_id` is `8`. But make sure you use your project-id, otherwise it will throw error.
In order to use llama-index with PremAI, you do not need to pass any model name or set any parameters with our chat-client. By default it will use the model name and parameters used in the [LaunchPad] [4].
We support lots of state of the art embedding models. You can view our list of supported LLMs and embedding models here [5]. For now let’s go for `text-embedding-3-large` model for this example.
``` import os import getpass

if os.environ.get("PREMAI_API_KEY") is None: os.environ["PREMAI_API_KEY"] = getpass.getpass("PremAI API Key:")
prem_embedding = PremAIEmbeddings( project_id=8, model_name="text-embedding-3-large" ) ```

## Calling the Embedding Model
Now you are all set. Now let’s start using our embedding model with a single query followed by multiple queries (which is also called as a document)
``` query = "Hello, this is a test query" query_result = prem_embedding.get_text_embedding(query) ```

``` print(f"Dimension of embeddings: {len(query_result)}") ```
``` Dimension of embeddings: 3072 ```
``` query_result[:5] ```
``` [-0.02129288576543331, 0.0008162345038726926, -0.004556538071483374, 0.02918623760342598, -0.02547479420900345] ```

[1] https://premai.io/
[2] https://docs.premai.io/quick-start
[3] https://docs.premai.io/introduction
[4] https://docs.premai.io/get-started/launchpad
[5] https://docs.premai.io/get-started/supported-models