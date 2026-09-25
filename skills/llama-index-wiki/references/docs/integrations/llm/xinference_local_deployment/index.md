# developers.llamaindex.ai/python/framework/integrations/llm/xinference_local_deployment/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/xinference_local_deployment/index.md

--- title: Xorbits Inference | Developer Documentation ---

In this demo notebook, we show how to use Xorbits Inference (Xinference for short) to deploy local LLMs in three steps.
We will be using the Llama 2 chat model in GGML format in the example, but the code should be easily transfrerable to all LLM chat models supported by Xinference. Below are a few examples:
| Name | Type | Language | Format | Size (in billions) | Quantization | | ------------- | ---------- | -------- | ------ | ------------------ | ------------------------------------------- | | llama-2-chat | RLHF Model | en | ggmlv3 | 7, 13, 70 | ’q2\_K’, ‘q3\_K\_L’, … , ‘q6\_K’, ‘q8\_0’ | | chatglm | SFT Model | en, zh | ggmlv3 | 6 | ’q4\_0’, ‘q4\_1’, ‘q5\_0’, ‘q5\_1’, ‘q8\_0’ | | chatglm2 | SFT Model | en, zh | ggmlv3 | 6 | ’q4\_0’, ‘q4\_1’, ‘q5\_0’, ‘q5\_1’, ‘q8\_0’ | | wizardlm-v1.0 | SFT Model | en | ggmlv3 | 7, 13, 33 | ’q2\_K’, ‘q3\_K\_L’, … , ‘q6\_K’, ‘q8\_0’ | | wizardlm-v1.1 | SFT Model | en | ggmlv3 | 13 | ’q2\_K’, ‘q3\_K\_L’, … , ‘q6\_K’, ‘q8\_0’ | | vicuna-v1.3 | SFT Model | en | ggmlv3 | 7, 13 | ’q2\_K’, ‘q3\_K\_L’, … , ‘q6\_K’, ‘q8\_0’ |

The latest complete list of supported models can be found in Xorbits Inference’s official GitHub page [1].
## 🤖 Install Xinference
i. Run `pip install "xinference[all]"` in a terminal window.
ii. After installation is complete, restart this jupyter notebook.
iii. Run `xinference` in a new terminal window.
iv. You should see something similar to the following output:
``` INFO:xinference:Xinference successfully started. Endpoint: http://127.0.0.1:9997 INFO:xinference.core.service:Worker 127.0.0.1:21561 has been added successfully INFO:xinference.deploy.worker:Xinference worker successfully started. ```

v. In the endpoint description, locate the endpoint port number after the colon. In the above case it is `9997`.
vi. Set the port number with the following cell:
``` %pip install llama-index-llms-xinference ```
``` port = 9997 # replace with your endpoint port number ```

## 🚀 Launch Local Models
In this step, we begin with importing the relevant libraries from `llama_index`
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` !pip install llama-index ```
``` # If Xinference can not be imported, you may need to restart jupyter notebook from llama_index.core import SummaryIndex from llama_index.core import ( TreeIndex, VectorStoreIndex, KeywordTableIndex, KnowledgeGraphIndex, SimpleDirectoryReader, ) from llama_index.llms.xinference import Xinference from xinference.client import RESTfulClient from IPython.display import Markdown, display ```

Then, we launch a model and use it. This allows us to connect the model to documents and queries in later steps.
Feel free to change the parameters for better performance! In order to achieve optimal results, it is recommended to use models above 13B in size. That being said, 7B models is more than enough for this short demo.
Here are some more parameter options for the Llama 2 chat model in GGML format, listed from the least space-consuming to the most resource-intensive but high-performing.
model\_size\_in\_billions:
`7`, `13`, `70`
quantization for 7B and 13B models:
`q2_K`, `q3_K_L`, `q3_K_M`, `q3_K_S`, `q4_0`, `q4_1`, `q4_K_M`, `q4_K_S`, `q5_0`, `q5_1`, `q5_K_M`, `q5_K_S`, `q6_K`, `q8_0`
quantizations for 70B models:
`q4_0`
``` # Define a client to send commands to xinference client = RESTfulClient(f"http://localhost:{port}")

# Download and Launch a model, this may take a while the first time model_uid = client.launch_model( model_name="llama-2-chat", model_size_in_billions=7, model_format="ggmlv3", quantization="q2_K", )

# Initiate Xinference object to use the LLM llm = Xinference( endpoint=f"http://localhost:{port}", model_uid=model_uid, temperature=0.0, max_tokens=512, ) ```

## 🕺 Index the Data… and Chat!
In this step, we combine the model and the data to create a query engine. The query engine can then be used as a chat bot, answering our queries based on the given data.
We will be using `VetorStoreIndex` since it is relatively fast. That being said, feel free to change the index for different experiences. Here are some available indexes already imported from the previous step:
`ListIndex`, `TreeIndex`, `VetorStoreIndex`, `KeywordTableIndex`, `KnowledgeGraphIndex`
To change index, simply replace `VetorStoreIndex` with another index in the following code.
The latest complete list of all available indexes can be found in Llama Index’s official Docs [2]
``` # create index from the data documents = SimpleDirectoryReader("../data/paul_graham").load_data()

# change index name in the following line index = VectorStoreIndex.from_documents(documents=documents)

# create the query engine query_engine = index.as_query_engine(llm=llm) ```
We can optionally set the temperature and the max answer length (in tokens) directly through the `Xinference` object before asking a question. This allows us to change parameters for different questions without rebuilding the query engine every time.
`temperature` is a number between 0 and 1 that controls the randomness of responses. Higher values increase creativity but may lead to off-topic replies. Setting to zero guarentees the same response every time.
`max_tokens` is an integer that sets an upper bound for the response length. Increase it if answers seem cut off, but be aware that too long a response may exceed the context window and cause errors.
``` # optionally, update the temperature and max answer length (in tokens) llm.__dict__.update({"temperature": 0.0}) llm.__dict__.update({"max_tokens": 2048})

# ask a question and display the answer question = "What did the author do after his time at Y Combinator?"

response = query_engine.query(question) display(Markdown(f"<b>{response}</b>")) ```

[1] https://github.com/xorbitsai/inference/blob/main/README.md
[2] https://gpt-index.readthedocs.io/en/latest/core_modules/data_modules/index/modules.html