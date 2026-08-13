# developers.llamaindex.ai/python/framework/integrations/embeddings/oci_data_science/index.md
> https://developers.llamaindex.ai/python/framework/integrations/embeddings/oci_data_science/index.md

--- title: Oracle Cloud Infrastructure (OCI) Data Science Service | Developer Documentation ---

Oracle Cloud Infrastructure (OCI) Data Science [1] is a fully managed, serverless platform for data science teams to build, train, and manage machine learning models in Oracle Cloud Infrastructure.
It offers AI Quick Actions [2], which can be used to deploy embedding models in OCI Data Science. AI Quick Actions target users who want to quickly leverage the capabilities of AI. They aim to expand the reach of foundation models to a broader set of users by providing a streamlined, code-free, and efficient environment for working with foundation models. AI Quick Actions can be accessed from the Data Science Notebook.
Detailed documentation on how to deploy embedding models in OCI Data Science using AI Quick Actions is available here [3] and here [4].
This notebook explains how to use OCI’s Data Science embedding models with LlamaIndex.
## Setup
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-embeddings-oci-data-science ```
``` !pip install llama-index ```
You will also need to install the oracle-ads [5] SDK.
``` !pip install -U oracle-ads ```
## Authentication
The authentication methods supported for LlamaIndex are equivalent to those used with other OCI services and follow the standard SDK authentication methods, specifically API Key, session token, instance principal, and resource principal. More details can be found here [6]. Make sure to have the required policies [7] to access the OCI Data Science Model Deployment endpoint. The oracle-ads [5] helps to simplify the authentication within OCI Data Science.

## Basic Usage

e1 = embeddings.get_text_embedding("This is a test document") print(e1)
e2 = embeddings.get_text_embedding_batch( ["This is a test document", "This is another test document"] ) print(e2) ```
## Async
``` import ads from llama_index.embeddings.oci_data_science import OCIDataScienceEmbedding
ads.set_auth(auth="security_token", profile="<replace-with-your-profile>")
embedding = OCIDataScienceEmbedding( endpoint="https://<MD_OCID>/predict", )
e1 = await embeddings.aget_text_embedding("This is a test document") print(e1)
e2 = await embeddings.aget_text_embedding_batch( ["This is a test document", "This is another test document"] ) print(e2) ```

[1] https://www.oracle.com/artificial-intelligence/data-science
[2] https://docs.oracle.com/en-us/iaas/data-science/using/ai-quick-actions.htm
[3] https://github.com/oracle-samples/oci-data-science-ai-samples/blob/main/ai-quick-actions/model- deployment-tips.md
[4] https://docs.oracle.com/en-us/iaas/data-science/using/ai-quick-actions-model-deploy.htm
[5] https://accelerated-data-science.readthedocs.io/en/latest/index.html
[6] https://accelerated-data-science.readthedocs.io/en/latest/user_guide/cli/authentication.html
[7] https://docs.oracle.com/en- us/iaas/data-science/using/model-dep-policies-auth.htm