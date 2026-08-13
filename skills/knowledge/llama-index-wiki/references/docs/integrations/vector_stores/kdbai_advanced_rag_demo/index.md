# developers.llamaindex.ai/python/framework/integrations/vector_stores/kdbai_advanced_rag_demo/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/kdbai_advanced_rag_demo/index.md

--- title: Advanced RAG with temporal filters using LlamaIndex and KDB.AI vector store | Developer Documentation ---

##### Note: This example requires a KDB.AI endpoint and API key. Sign up for a free KDB.AI account [1].
> KDB.AI [2] is a powerful knowledge-based vector database and search engine that allows you to build scalable, reliable AI applications, using real-time data, by providing advanced search, recommendation and personalization.
This example demonstrates how to use KDB.AI to run semantic search, summarization and analysis of financial regulations around some specific moment in time.
To access your end point and API keys, sign up to KDB.AI here.
To set up your development environment, follow the instructions on the KDB.AI pre-requisites page.
The following examples demonstrate some of the ways you can interact with KDB.AI through LlamaIndex.
## Install dependencies with Pip
In order to successfully run this sample, note the following steps depending on where you are running this notebook:
-***Run Locally / Private Environment:*** The Setup [3] steps in the repository’s `README.md` will guide you on prerequisites and how to run this with Jupyter.
-***Colab / Hosted Environment:*** Open this notebook in Colab and run through the cells.
``` !pip install llama-index llama-index-llms-openai llama-index-embeddings-openai llama-index-readers-file llama-index-vector-stores-kdbai !pip install kdbai_client pandas ```

## Import dependencies
``` from getpass import getpass import re import os import shutil import time import urllib import datetime

import pandas as pd
from llama_index.core import ( Settings, SimpleDirectoryReader, StorageContext, VectorStoreIndex, ) from llama_index.core.node_parser import SentenceSplitter from llama_index.core.retrievers import VectorIndexRetriever from llama_index.embeddings.openai import OpenAIEmbedding from llama_index.llms.openai import OpenAI from llama_index.vector_stores.kdbai import KDBAIVectorStore

import kdbai_client as kdbai
OUTDIR = "pdf" RESET = True ```
#### Set OpenAI API key and choose the LLM and Embedding model to use:
``` # os.environ["OPENAI_API_KEY"] = getpass("OpenAI API key: ") os.environ["OPENAI_API_KEY"] = ( os.environ["OPENAI_API_KEY"] if "OPENAI_API_KEY" in os.environ else getpass("OpenAI API Key: ") ) ```

``` import os from getpass import getpass

# Set OpenAI API if "OPENAI_API_KEY" in os.environ: KDBAI_API_KEY = os.environ["OPENAI_API_KEY"] else: # Prompt the user to enter the API key OPENAI_API_KEY = getpass("OPENAI API KEY: ") # Save the API key as an environment variable for the current session os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY ```

``` EMBEDDING_MODEL = "text-embedding-3-small" GENERATION_MODEL = "gpt-4o-mini"

llm = OpenAI(model=GENERATION_MODEL) embed_model = OpenAIEmbedding(model=EMBEDDING_MODEL)
Settings.llm = llm Settings.embed_model = embed_model ```
## Create KDB.AI session and table
``` # vector DB imports import os from getpass import getpass import kdbai_client as kdbai import time ```

##### Option 1. KDB.AI Cloud
To use KDB.AI Cloud, you will need two session details - a URL endpoint and an API key. To get these you can sign up for free here [4].
You can connect to a KDB.AI Cloud session using `kdbai.Session` and passing the session URL endpoint and API key details from your KDB.AI Cloud portal.
If the environment variables `KDBAI_ENDPOINTS` and `KDBAI_API_KEY` exist on your system containing your KDB.AI Cloud portal details, these variables will automatically be used to connect. If these do not exist, it will prompt you to enter your KDB.AI Cloud portal session URL endpoint and API key details.
``` # Set up KDB.AI endpoint and API key KDBAI_ENDPOINT = ( os.environ["KDBAI_ENDPOINT"] if "KDBAI_ENDPOINT" in os.environ else input("KDB.AI endpoint: ") ) KDBAI_API_KEY = ( os.environ["KDBAI_API_KEY"] if "KDBAI_API_KEY" in os.environ else getpass("KDB.AI API key: ") )

session = kdbai.Session(endpoint=KDBAI_ENDPOINT, api_key=KDBAI_API_KEY) ```
##### Option 2. KDB.AI Server
To use KDB.AI Server, you will need download and run your own container. To do this, you will first need to sign up for free here [5].
You will receive an email with the required license file and bearer token needed to download your instance. Follow instructions in the signup email to get your session up and running.
Once the setup steps [6] are complete you can then connect to your KDB.AI Server session using `kdbai.Session` and passing your local endpoint.
``` # session = kdbai.Session() ```
### Create the schema for your KDB.AI table
***!!! Note:*** The ‘dims’ parameter in the embedding column must reflect the output dimensions of the embedding model you choose.
- OpenAI ‘text-embedding-3-small’ outputs 1536 dimensions.
``` schema = [ {"name": "document_id", "type": "bytes"}, {"name": "text", "type": "bytes"}, {"name": "embeddings", "type": "float32s"}, {"name": "title", "type": "str"}, {"name": "publication_date", "type": "datetime64[ns]"}, ]

indexFlat = { "name": "flat_index", "type": "flat", "column": "embeddings", "params": {"dims": 1536, "metric": "L2"}, } ```
``` KDBAI_TABLE_NAME = "reports" database = session.database("default")
# First ensure the table does not already exist for table in database.tables: if table.name == KDBAI_TABLE_NAME: table.drop() break
# Create the table table = database.create_table( KDBAI_TABLE_NAME, schema=schema, indexes=[indexFlat] ) ```
## Financial reports urls and metadata
``` INPUT_URLS = [ "https://www.govinfo.gov/content/pkg/PLAW-106publ102/pdf/PLAW-106publ102.pdf", "https://www.govinfo.gov/content/pkg/PLAW-111publ203/pdf/PLAW-111publ203.pdf", ]
METADATA = { "pdf/PLAW-106publ102.pdf": { "title": "GRAMM–LEACH–BLILEY ACT, 1999", "publication_date": pd.to_datetime("1999-11-12"), }, "pdf/PLAW-111publ203.pdf": { "title": "DODD-FRANK WALL STREET REFORM AND CONSUMER PROTECTION ACT, 2010", "publication_date": pd.to_datetime("2010-07-21"), }, } ```

## Download PDF files locally

CHUNK_SIZE = 512 * 1024

def download_file(url): print("Downloading %s..." % url) out = os.path.join(OUTDIR, os.path.basename(url)) try: response = urllib.request.urlopen(url) except urllib.error.URLError as e: logging.exception("Failed to download %s !" % url) else: with open(out, "wb") as f: while True: chunk = response.read(CHUNK_SIZE) if chunk: f.write(chunk) else: break return out

if RESET: if os.path.exists(OUTDIR): shutil.rmtree(OUTDIR) os.mkdir(OUTDIR)
local_files = [download_file(x) for x in INPUT_URLS] local_files[:10] ```
``` Downloading https://www.govinfo.gov/content/pkg/PLAW-106publ102/pdf/PLAW-106publ102.pdf...

Downloading https://www.govinfo.gov/content/pkg/PLAW-111publ203/pdf/PLAW-111publ203.pdf... CPU times: user 52.6 ms, sys: 1.2 ms, total: 53.8 ms Wall time: 7.86 s ```
## Load local PDF files with LlamaIndex

def get_metadata(filepath): return METADATA[filepath]

documents = SimpleDirectoryReader( input_files=local_files, file_metadata=get_metadata, )
docs = documents.load_data() len(docs) ```
``` CPU times: user 8.22 s, sys: 9.04 ms, total: 8.23 s Wall time: 8.23 s

994 ```
## Setup LlamaIndex RAG pipeline using KDB.AI vector store

[Column 1]
# llm = OpenAI(temperature=0, model=LLM) vector_store = KDBAIVectorStore(table)
storage_context = StorageContext.from_defaults(vector_store=vector_store) index = VectorStoreIndex.from_documents( docs, storage_context=storage_context, transformations=[SentenceSplitter(chunk_size=2048, chunk_overlap=0)], ) ```
``` CPU times: user 3.67 s, sys: 31.9 ms, total: 3.7 s Wall time: 22.3 s ```
``` table.query() ```
``` .dataframe tbody tr th { vertical-align: top; }
.dataframe thead th { text-align: right; } ```

994 rows × 5 columns
## Setup the LlamaIndex Query Engine

[Column 2]
| | document\_id | text | embeddings | title | publication\_date | | --- | --------------------------------------- | ------------------------------------------------- | -------------------------------------------------- | ------------------------------------------------- | --------------- -- | | 0 | b'272d7d24-c232-41b6-823e-27aa6203c100' | b'PUBLIC LAW 106\xc2\xb1102\xc3\x90NOV. 12, 19... | \[0.034452137, 0.03166917, -0.011892043, 0.0184... | GRAMM–LEACH–BLILEY ACT, 1999 | 1999-11-12 | | 1 | b'89e3f2ee-f5a6-4e40-bb81-0632f08341f0' | b"113 STAT. 1338 PUBLIC LAW 106\xc2\xb1102\xc3... | \[0.02164333, 1.0030156e-05, 0.0028665832, 0.02... | GRAMM–LEACH–BLILEY ACT, 1999 | 1999-11-12 | | 2 | b'56fbe82a-5458-4a4a-a5ed-026d9399151d' | b'113 STAT. 1339 PUBLIC LAW 106\xc2\xb1102\xc3... | \[0.01380091, 0.026945233, 0.02838467, 0.043132... | GRAMM–LEACH–BLILEY ACT, 1999 | 1999-11-12 | | 3 | b'b6bf9e48-51b6-45d9-9259-b6346f93831f' | b'113 STAT. 1340 PUBLIC LAW 106\xc2\xb1102\xc3... | \[0.0070182937, 0.014063503, 0.026525516, 0.040... | GRAMM–LEACH–BLILEY ACT, 1999 | 1999-11-12 | | 4 | b'f398b133-b4f5-4a34-94d1-9a97fdb658e5' | b"113 STAT. 1341 PUBLIC LAW 106\xc2\xb1102\xc3... | \[0.025041763, 0.01968024, 0.030940715, 0.02899... | GRAMM–LEACH–BLILEY ACT, 1999 | 1999-11-12 | | ... | ... | ... | ... | ... | ... | | 989 | b'8e84d1d5-d87d-4351-b7eb-5d569fdb8d9c' | b'124 STAT. 2219 PUBLIC LAW 111\xe2\x80\x93203... | \[0.024505286, 0.015549232, 0.0536601, 0.028532... | DODD-FRANK WALL STREET REFORM AND CONSUMER PRO... | 2010-07-21 | | 990 | b'0c47f590-050c-4374-bf8c-2a4502dc980f' | b'124 STAT. 2220 PUBLIC LAW 111\xe2\x80\x93203... | \[0.014071382, -0.0044553108, 0.03662071, 0.035... | DODD-FRANK WALL STREET REFORM AND CONSUMER PRO... | 2010-07-21 |
| 991 | b'63a2235f-d368-43b8-a1a9-a5a11d497245' | b'124 STAT. 2221 PUBLIC LAW 111\xe2\x80\x93203... | \[0.0005448305, 0.013075933, 0.044821188, 0.031... | DODD-FRANK WALL STREET REFORM AND CONSUMER PRO... | 2010-07-21 | | 992 | b'bac4d75e-4867-4d89-a71e-09a6762bf3c4' | b'124 STAT. 2222 PUBLIC LAW 111\xe2\x80\x93203... | \[0.032077603, 0.016817383, 0.04507993, 0.03376... | DODD-FRANK WALL STREET REFORM AND CONSUMER PRO... | 2010-07-21 | | 993 | b'e262e4da-f6e1-4b9d-9232-77fc3f0c81a7' | b'124 STAT. 2223 PUBLIC LAW 111\xe2\x80\x93203... | \[0.0387719, -0.025150038, 0.030345473, 0.04303... | DODD-FRANK WALL STREET REFORM AND CONSUMER PRO... | 2010-07-21 |


query_engine = index.as_query_engine( similarity_top_k=K, vector_store_kwargs={ "index": "flat_index", "filter": [["<", "publication_date", datetime.date(2008, 9, 15)]], "sort_columns": "publication_date", }, ) ```
``` CPU times: user 512 μs, sys: 23 μs, total: 535 μs Wall time: 550 μs ```
## Before the 2008 crisis

result = query_engine.query( """ What was the main financial regulation in the US before the 2008 financial crisis ? """ ) print(result.response) ```
``` The main financial regulation in the US before the 2008 financial crisis was the Gramm-Leach-Bliley Act, enacted in 1999. This act facilitated the affiliation among banks, securities firms, and insurance companies, effectively repealing parts of the Glass-Steagall Act, which had previously separated these financial services. The Gramm-Leach-Bliley Act aimed to enhance competition in the financial services industry by providing a framework for the integration of various financial institutions.
CPU times: user 61.8 ms, sys: 0 ns, total: 61.8 ms Wall time: 4.24 s ```

result = query_engine.query( """ Is the Gramm-Leach-Bliley Act of 1999 enough to prevent the 2008 crisis. Search the document and explain its strenghts and weaknesses to regulate the US stock market. """ ) print(result.response) ```
``` The Gramm-Leach-Bliley Act of 1999 aimed to enhance competition in the financial services industry by allowing affiliations among banks, securities firms, and insurance companies. Its strengths include the repeal of the Glass-Steagall Act, which had previously separated commercial banking from investment banking, thereby enabling financial institutions to diversify their services and potentially increase competition. This diversification could lead to more innovative financial products and services.
However, the Act also has notable weaknesses. By allowing greater affiliations and reducing regulatory barriers, it may have contributed to the creation of "too big to fail" institutions, which posed systemic risks to the financial system. The lack of stringent oversight and the ability for financial holding companies to engage in a wide range of activities without adequate regulation may have led to excessive risk-taking. Additionally, the Act did not sufficiently address the complexities of modern financial products, such as derivatives, which played a significant role in the 2008 financial crisis.
In summary, while the Gramm-Leach-Bliley Act aimed to foster competition and innovation in the financial sector, its regulatory framework may have inadvertently facilitated the conditions that led to the financial crisis, highlighting the need for a more robust regulatory approach to oversee the interconnectedness and risks within the financial system. CPU times: user 45.7 ms, sys: 255 μs, total: 46 ms Wall time: 21.9 s ```
## After the 2008 crisis

# Using gpt-4o-mini, the 128k tokens context size can take 100 pages. K = 15
query_engine = index.as_query_engine( similarity_top_k=K, vector_store_kwargs={ "index": "flat_index", "filter": [[">=", "publication_date", datetime.date(2008, 9, 15)]], "sort_columns": "publication_date", }, ) ```

``` CPU times: user 171 μs, sys: 0 ns, total: 171 μs Wall time: 175 μs ```

result = query_engine.query( """ What happened on the 15th of September 2008 ? """ ) print(result.response) ```
``` On the 15th of September 2008, Lehman Brothers, a major global financial services firm, filed for bankruptcy. This event marked one of the largest bankruptcies in U.S. history and was a significant moment in the financial crisis of 2007-2008, leading to widespread panic in financial markets and contributing to the global economic downturn. CPU times: user 51.4 ms, sys: 0 ns, total: 51.4 ms Wall time: 3.6 s ```

result = query_engine.query( """ What was the new US financial regulation enacted after the 2008 crisis to increase the market regulation and to improve consumer sentiment ? """ ) print(result.response) ```
``` The new US financial regulation enacted after the 2008 crisis to increase market regulation and improve consumer sentiment is the Dodd-Frank Wall Street Reform and Consumer Protection Act, which was signed into law on July 21, 2010. This legislation aimed to promote financial stability, enhance accountability and transparency in the financial system, and protect consumers from abusive financial practices. CPU times: user 43.7 ms, sys: 0 ns, total: 43.7 ms Wall time: 4.55 s ```
## In depth analysis

[Column 1]
# Using gpt-4o-mini, the 128k tokens context size can take 100 pages. K = 20
query_engine = index.as_query_engine( similarity_top_k=K, vector_store_kwargs={ "index": "flat_index", "sort_columns": "publication_date", }, ) ```

``` CPU times: user 227 μs, sys: 10 μs, total: 237 μs Wall time: 243 μs ```
``` %%time

## Delete the KDB.AI Table
Once finished with the table, it is best practice to drop it.
``` table.drop() ```
#### Take Our Survey
Take the Survey [7]

[Column 2]
result = query_engine.query( """ Analyse the US financial regulations before and after the 2008 crisis and produce a report of all related arguments to explain what happened, and to ensure that does not happen again. Use both the provided context and your own knowledge but do mention explicitely which one you use. """ ) print(result.response) ```

``` The analysis of U.S. financial regulations before and after the 2008 financial crisis reveals significant changes aimed at preventing a recurrence of such a crisis.
Before the crisis, the regulatory framework was characterized by a lack of comprehensive oversight, particularly for nonbank financial institutions. The regulatory environment allowed for excessive risk-taking, inadequate capital requirements, and insufficient transparency in financial transactions. This environment contributed to the housing bubble and the subsequent collapse of major financial institutions, leading to widespread economic turmoil.
In response to the crisis, the Dodd-Frank Wall Street Reform and Consumer Protection Act of 2010 was enacted. This legislation introduced several key reforms:
1. **Creation of the Financial Stability Oversight Council (FSOC)**: This body was established to monitor systemic risks and coordinate regulatory efforts across different financial sectors. It has the authority to recommend heightened standards and safeguards for financial activities that could pose risks to financial stability.
2. **Enhanced Regulatory Oversight**: Dodd-Frank imposed stricter regulations on bank holding companies and nonbank financial companies, particularly those with significant assets. This includes requirements for stress testing, capital planning, and the submission of resolution plans to ensure orderly wind-downs in case of failure.
3. **Consumer Protection Measures**: The establishment of the Consumer Financial Protection Bureau (CFPB) aimed to protect consumers from predatory lending practices and ensure transparency in financial products.
4. **Volcker Rule**: This provision restricts proprietary trading by banks and limits their investments in hedge funds and private equity funds, thereby reducing conflicts of interest and excessive risk-taking.
5. **Increased Transparency and Reporting Requirements**: Financial institutions are now required to disclose more information regarding their risk exposures and financial health, which enhances market discipline and investor confidence.
The arguments for these reforms center around the need for a more resilient financial system that can withstand economic shocks. The reforms aim to address the systemic risks that were prevalent before the crisis, ensuring that financial institutions maintain adequate capital buffers and engage in prudent risk management practices.
In conclusion, the regulatory landscape has shifted significantly since the 2008 crisis, with a focus on preventing excessive risk-taking, enhancing transparency, and protecting consumers. These measures are designed to create a more stable financial environment and mitigate the likelihood of future crises. CPU times: user 180 ms, sys: 437 μs, total: 180 ms Wall time: 10.5 s ```

We hope you found this sample helpful! Your feedback is important to us, and we would appreciate it if you could take a moment to fill out our brief survey. Your input helps us improve our content.


[1] https://kdb.ai/get-started
[2] https://kdb.ai/
[3] https://github.com/KxSystems/kdbai-samples/blob/main/README.md#setup
[4] https://trykdb.kx.com/kdbai/signup
[5] https://trykdb.kx.com/kdbaiserver/signup/
[6] https://code.kx.com/kdbai/gettingStarted/kdb-ai-server-setup.html
[7] https://delighted.com/t/kWYXv316