# developers.llamaindex.ai/python/framework/understanding/rag/loading/llamacloud/index.md
> https://developers.llamaindex.ai/python/framework/understanding/rag/loading/llamacloud/index.md

[Column 1]
--- title: Loading from LlamaCloud | Developer Documentation ---
## Using LlamaCloud from LlamaIndex
``` import os from llama_cloud_services import LlamaCloudIndex
os.environ["LLAMA_CLOUD_API_KEY"] = "llx-..."
index = LlamaCloudIndex("my_first_index", project_name="Default") query_engine = index.as_query_engine() answer = query_engine.query("Example query") ```

[Column 2]
Our enterprise service, LlamaCloud [1], allows you to store and query your data in a fully-managed, scalable, and secure environment. For a full explanation of how to use LlamaCloud, see the LlamaCloud documentation [2], in particular the framework integration guide [3].
You can use LlamaCloud to connect to your data stores and automatically index them. Once an index is created, you can use it in just a few lines of code:

It’s also possible to programmatically load documents into a LlamaCloud index; check the documentation [3] for more details.


[1] https://cloud.llamaindex.ai/
[2] https://docs.cloud.llamaindex.ai/
[3] https://docs.cloud.llamaindex.ai/llamacloud/guides/framework_integration