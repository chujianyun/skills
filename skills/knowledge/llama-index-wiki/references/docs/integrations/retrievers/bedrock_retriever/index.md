# developers.llamaindex.ai/python/framework/integrations/retrievers/bedrock_retriever/index.md
> https://developers.llamaindex.ai/python/framework/integrations/retrievers/bedrock_retriever/index.md

[Column 1]
--- title: Bedrock (Knowledge Bases) | Developer Documentation ---

## Using the Knowledge Base Retriever
``` %pip install --upgrade --quiet boto3 botocore %pip install llama-index %pip install llama-index-retrievers-bedrock ```

``` from llama_index.retrievers.bedrock import AmazonKnowledgeBasesRetriever
retriever = AmazonKnowledgeBasesRetriever( knowledge_base_id="<knowledge-base-id>", retrieval_config={ "vectorSearchConfiguration": { "numberOfResults": 4, "overrideSearchType": "HYBRID", "filter": {"equals": {"key": "tag", "value": "space"}}, } }, ) ```

``` query = "How big is Milky Way as compared to the entire universe?" retrieved_results = retriever.retrieve(query)
# Prints the first retrieved result print(retrieved_results[0].get_content()) ```
## Use the retriever to query with Bedrock LLMs
``` %pip install llama-index-llms-bedrock ```
``` from llama_index.core import get_response_synthesizer from llama_index.llms.bedrock.base import Bedrock
llm = Bedrock(model="anthropic.claude-v2", temperature=0, max_tokens=3000) response_synthesizer = get_response_synthesizer( response_mode="compact", llm=llm ) response_obj = response_synthesizer.synthesize(query, retrieved_results) print(response_obj) ```

[Column 2]
Knowledge bases for Amazon Bedrock [1] is an Amazon Web Services (AWS) offering which lets you quickly build RAG applications by using your private data to customize FM response.
Implementing `RAG` requires organizations to perform several cumbersome steps to convert data into embeddings (vectors), store the embeddings in a specialized vector database, and build custom integrations into the database to search and retrieve text relevant to the user’s query. This can be time-consuming and inefficient.
With `Knowledge Bases for Amazon Bedrock`, simply point to the location of your data in `Amazon S3`, and `Knowledge Bases for Amazon Bedrock` takes care of the entire ingestion workflow into your vector database. If you do not have an existing vector database, Amazon Bedrock creates an Amazon OpenSearch Serverless vector store for you.
Knowledge base can be configured through AWS Console [2] or by using AWS SDKs [3].
In this notebook, we introduce AmazonKnowledgeBasesRetriever - Amazon Bedrock integration in Llama Index via the Retrieve API to retrieve relevant results for a user query from knowledge bases.

For more information about the supported parameters for `retrieval_config`, please check the boto3 documentation: link [4]
To use filters in the `retrieval_config` you will need to set up metadata.json file for your data source. For more info, see: link [5]


[1] https://aws.amazon.com/bedrock/knowledge-bases/
[2] https://aws.amazon.com/console/
[3] https://aws.amazon.com/developer/tools/
[4] https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent- runtime/client/retrieve.html
[5] https://aws.amazon.com/blogs/machine-learning/knowledge-bases-for-amazon-bedrock-now- supports-metadata-filtering-to-improve-retrieval-accuracy/