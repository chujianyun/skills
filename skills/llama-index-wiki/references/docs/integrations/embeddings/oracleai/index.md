# developers.llamaindex.ai/python/framework/integrations/embeddings/oracleai/index.md
> https://developers.llamaindex.ai/python/framework/integrations/embeddings/oracleai/index.md

--- title: Oracle AI Vector Search: Generate Embeddings | Developer Documentation ---

Oracle AI Vector Search is designed for Artificial Intelligence (AI) workloads that allows you to query data based on semantics, rather than keywords. One of the biggest benefits of Oracle AI Vector Search is that semantic search on unstructured data can be combined with relational search on business data in one single system. This is not only powerful but also significantly more effective because you don’t need to add a specialized vector database, eliminating the pain of data fragmentation between multiple systems.
In addition, your vectors can benefit from all of Oracle Database’s most powerful features, like the following:
- Partitioning Support [1] - Real Application Clusters scalability [2] - Exadata smart scans [3] - Shard processing across geographically distributed databases [4] - Transactions [5] - Parallel SQL [6] - Disaster recovery [7] - Security [8] - Oracle Machine Learning [9] - Oracle Graph Database [10] - Oracle Spatial and Graph [11] - Oracle Blockchain [12] - JSON [13]

The guide demonstrates how to use Embedding Capabilities within Oracle AI Vector Search to generate embeddings for your documents using OracleEmbeddings.
If you are just starting with Oracle Database, consider exploring the free Oracle 23 AI [14] which provides a great introduction to setting up your database environment. While working with the database, it is often advisable to avoid using the system user by default; instead, you can create your own user for enhanced security and customization. For detailed steps on user creation, refer to our end-to-end guide [15] which also shows how to set up a user in Oracle. Additionally, understanding user privileges is crucial for managing database security effectively. You can learn more about this topic in the official Oracle guide [16] on administering user accounts and security.

### Prerequisites
Ensure you have the Oracle Python Client driver installed to facilitate the integration of llama\_index with Oracle AI Vector Search.
``` %pip install llama-index-embeddings-oracleai ```
### Connect to Oracle Database
The following sample code will show how to connect to Oracle Database. By default, python-oracledb runs in a ‘Thin’ mode which connects directly to Oracle Database. This mode does not need Oracle Client libraries. However, some additional functionality is available when python-oracledb uses them. Python-oracledb is said to be in ‘Thick’ mode when Oracle Client libraries are used. Both modes have comprehensive functionality supporting the Python Database API v2.0 Specification. See the following guide [17] that talks about features supported in each mode. You might want to switch to thick-mode if you are unable to use thin-mode.

``` import sys
import oracledb
# Update the following variables with your Oracle database credentials and connection details username = "<username>" password = "<password>" dsn = "<hostname>/<service_name>"

try: conn = oracledb.connect(user=username, password=password, dsn=dsn) print("Connection successful!") except Exception as e: print("Connection failed!") sys.exit(1) ```

For embedding generation, several provider options are available to users, including embedding generation within the database and third-party services such as OcigenAI, Hugging Face, and OpenAI. Users opting for third- party providers must establish credentials that include the requisite authentication information. Alternatively, if users select ‘database’ as their provider, they are required to load an ONNX model into the Oracle Database to facilitate embeddings.
### Load ONNX Model
Oracle accommodates a variety of embedding providers, enabling users to choose between proprietary database solutions and third-party services such as OCIGENAI and HuggingFace. This selection dictates the methodology for generating and managing embeddings.
***Important*** : Should users opt for the database option, they must upload an ONNX model into the Oracle Database. Conversely, if a third-party provider is selected for embedding generation, uploading an ONNX model to Oracle Database is not required.
A significant advantage of utilizing an ONNX model directly within Oracle is the enhanced security and performance it offers by eliminating the need to transmit data to external parties. Additionally, this method avoids the latency typically associated with network or REST API calls.
Below is the example code to upload an ONNX model into Oracle Database:

# please update with your related information # make sure that you have onnx file in the system onnx_dir = "DEMO_DIR" onnx_file = "tinybert.onnx" model_name = "demo_model"

try: OracleEmbeddings.load_onnx_model(conn, onnx_dir, onnx_file, model_name) print("ONNX model loaded.") except Exception as e: print("ONNX model loading failed!") sys.exit(1) ```

### Create Credential
When selecting third-party providers for generating embeddings, users are required to establish credentials to securely access the provider’s endpoints.
***Important:*** No credentials are necessary when opting for the ‘database’ provider to generate embeddings. However, should users decide to utilize a third-party provider, they must create credentials specific to the chosen provider.
Below is an illustrative example:
``` try: cursor = conn.cursor() cursor.execute( """ declare jo json_object_t; begin -- HuggingFace dbms_vector_chain.drop_credential(credential_name => 'HF_CRED'); jo := json_object_t(); jo.put('access_token', '<access_token>'); dbms_vector_chain.create_credential( credential_name => 'HF_CRED', params => json(jo.to_string));

-- OCIGENAI dbms_vector_chain.drop_credential(credential_name => 'OCI_CRED'); jo := json_object_t(); jo.put('user_ocid','<user_ocid>'); jo.put('tenancy_ocid','<tenancy_ocid>'); jo.put('compartment_ocid','<compartment_ocid>'); jo.put('private_key','<private_key>'); jo.put('fingerprint','<fingerprint>'); dbms_vector_chain.create_credential( credential_name => 'OCI_CRED', params => json(jo.to_string)); end; """ ) cursor.close() print("Credentials created.") except Exception as ex: cursor.close() raise ```

### Generate Embeddings
Oracle AI Vector Search provides multiple methods for generating embeddings, utilizing either locally hosted ONNX models or third-party APIs. For comprehensive instructions on configuring these alternatives, please refer to the Oracle AI Vector Search Guide [18].
***Note:*** Users may need to configure a proxy to utilize third-party embedding generation providers, excluding the ‘database’ provider that utilizes an ONNX model.
``` # proxy to be used when we instantiate summary and embedder object proxy = "<proxy>" ```

The following sample code will show how to generate embeddings:
``` from llama_index.embeddings.oracleai import OracleEmbeddings
""" # using ocigenai embedder_params = { "provider": "ocigenai", "credential_name": "OCI_CRED", "url": "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/embedText", "model": "cohere.embed-english-light-v3.0", }

# using huggingface embedder_params = { "provider": "huggingface", "credential_name": "HF_CRED", "url": "https://api-inference.huggingface.co/pipeline/feature-extraction/", "model": "sentence-transformers/all-MiniLM-L6-v2", "wait_for_model": "true" } """

# using ONNX model loaded to Oracle Database embedder_params = {"provider": "database", "model": "demo_model"}
# Remove proxy if not required embedder = OracleEmbeddings(conn=conn, params=embedder_params, proxy=proxy) embed = embedder._get_text_embedding("Hello World!")

""" verify """ print(f"Embedding generated by OracleEmbeddings: {embed}") ```
### End to End Demo
Please refer to our complete demo guide Oracle AI Vector Search End-to-End Demo Guide [15] to build an end to end RAG pipeline with the help of Oracle AI Vector Search.

[1] https://www.oracle.com/database/technologies/partitioning.html
[2] https://www.oracle.com/database/real-application-clusters/
[3] https://www.oracle.com/database/technologies/exadata/software/smartscan/
[4] https://www.oracle.com/database/distributed-database/
[5] https://docs.oracle.com/en/database/oracle/oracle-database/23/cncpt/transactions.html
[6] https://docs.oracle.com/en/database/oracle/oracle-database/21/vldbg/parallel-exec-intro.html#GUID-D28717E4-0F77-44F5-BB4E-234C31D4E4BA
[7] https://www.oracle.com/database/data-guard/
[8] https://www.oracle.com/security/database-security/
[9] https://www.oracle.com/artificial-intelligence/database-machine-learning/
[10] https://www.oracle.com/database/integrated-graph-database/
[11] https://www.oracle.com/database/spatial/
[12] https://docs.oracle.com/en/database/oracle/oracle-database/23/arpls/dbms_blockchain_table.html#GUID-B469E277-978E-4378-A8C1-26D3FF96C9A6
[13] https://docs.oracle.com/en/database/oracle/oracle-database/23/adjsn/json-in-oracle-database.html
[14] https://www.oracle.com/database/free/#resources
[15] https://github.com/run-llama/llama_index/blob/main/docs/examples/cookbooks/oracleai_demo.ipynb
[16] https://docs.oracle.com/en/database/oracle/oracle-database/19/admqs/administering-user-accounts-and- security.html#GUID-36B21D72-1BBB-46C9-A0C9-F0D2A8591B8D
[17] https://python-oracledb.readthedocs.io/en/latest/user_guide/appendix_a.html#featuresummary
[18] https://docs.oracle.com/en/database/oracle/oracle-database/23/arpls/dbms_vector_chain1.html#GUID-C6439E94-4E86-4ECD-954E-4B73D53579DE