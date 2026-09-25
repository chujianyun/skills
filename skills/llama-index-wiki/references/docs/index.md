# developers.llamaindex.ai/python/framework/index.md
> https://developers.llamaindex.ai/python/framework/index.md

--- title: Welcome to LlamaIndex 🦙 ! | Developer Documentation ---

LlamaIndex is the leading framework for building LLM-powered agents over your data with LLMs [1] and workflows.
- Introduction
What is context augmentation? What are agents and workflows? How does LlamaIndex help build them?
- Use cases
What kind of apps can you build with LlamaIndex? Who should use it?
- Getting started
Get started in Python or TypeScript in just 5 lines of code!
- LlamaCloud [2]
Managed services for LlamaIndex including LlamaParse [3], the world’s best document parser.
- Community
Get help and meet collaborators on Discord, Twitter, LinkedIn, and learn how to contribute to the project.
- Related projects
Check out our library of connectors, readers, and other integrations at LlamaHub [4] as well as demos and starter apps like create-llama [5].
## Introduction
### What are agents?
Agents are LLM-powered knowledge assistants that use tools to perform tasks like research, data extraction, and more. Agents range from simple question-answering to being able to sense, decide and take actions in order to complete tasks.
LlamaIndex provides a framework for building agents including the ability to use RAG pipelines as one of many tools to complete a task.
### What are workflows?
Workflows are multi-step processes that combine one or more agents, data connectors, and other tools to complete a task. They are event-driven software that allows you to combine RAG data sources and multiple agents to create a complex application that can perform a wide variety of tasks with reflection, error-correction, and other hallmarks of advanced LLM applications. You can then deploy these agentic workflows as production microservices.
### What is context augmentation?
LLMs offer a natural language interface between humans and data. LLMs come pre-trained on huge amounts of publicly available data, but they are not trained on **your** data. Your data may be private or specific to the problem you’re trying to solve. It’s behind APIs, in SQL databases, or trapped in PDFs and slide decks.
Context augmentation makes your data available to the LLM to solve the problem at hand. LlamaIndex provides the tools to build any of context-augmentation use case, from prototype to production. Our tools allow you to ingest, parse, index and process your data and quickly implement complex query workflows combining data access with LLM prompting.
The most popular example of context-augmentation is Retrieval-Augmented Generation or RAG, which combines context with LLMs at inference time.
### LlamaIndex is the framework for Context-Augmented LLM Applications
LlamaIndex imposes no restriction on how you use LLMs. You can use LLMs as auto-complete, chatbots, agents, and more. It just makes using them easier. We provide tools like:
- **Data connectors** ingest your existing data from their native source and format. These could be APIs, PDFs, SQL, and (much) more.
- **Data indexes** structure your data in intermediate representations that are easy and performant for LLMs to consume.
- **Engines** provide natural language access to your data. For example:
- Query engines are powerful interfaces for question-answering (e.g. a RAG flow). - Chat engines are conversational interfaces for multi-message, “back and forth” interactions with your data.
- **Agents** are LLM-powered knowledge workers augmented by tools, from simple helper functions to API integrations and more.
- **Observability/Evaluation** integrations that enable you to rigorously experiment, evaluate, and monitor your app in a virtuous cycle.
- **Workflows** allow you to combine all of the above into an event-driven system far more flexible than other, graph-based approaches.
## Use cases
Some popular use cases for LlamaIndex and context augmentation in general include:
- Question-Answering (Retrieval-Augmented Generation aka RAG) - Chatbots - Document Understanding and Data Extraction - Autonomous Agents that can perform research and take actions - Multi-modal applications that combine text, images, and other data types - Fine-tuning models on data to improve performance

Check out our use cases documentation for more examples and links to tutorials.
### 👨👩👧👦 Who is LlamaIndex
LlamaIndex provides tools for beginners, advanced users, and everyone in between.
Our high-level API allows beginner users to use LlamaIndex to ingest and query their data in 5 lines of code.
For more complex applications, our lower-level APIs allow advanced users to customize and extend any module — data connectors, indices, retrievers, query engines, and reranking modules — to fit their needs.
## Getting Started
LlamaIndex is available in Python (these docs) and Typescript [6]. If you’re not sure where to start, we recommend reading [how to read these docs] (/python/framework/getting_started/reading/index.md) which will point you to the right place based on your experience level.
### 30 second quickstart
Set an environment variable called `OPENAI_API_KEY` with an OpenAI API key [7]. Install the Python library:
Terminal window
``` pip install llama-index ```
Put some documents in a folder called `data`, then ask questions about them with our famous 5-line starter:
``` from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data() index = VectorStoreIndex.from_documents(documents) query_engine = index.as_query_engine() response = query_engine.query("Some question about the data should go here") print(response) ```

If any part of this trips you up, don’t worry! Check out our more comprehensive starter tutorials using remote APIs like OpenAI or any model that runs on your laptop.
## LlamaCloud
If you’re an enterprise developer, check out **LlamaCloud** [8]. It is an end-to-end managed service for document parsing, extraction, indexing, and retrieval - allowing you to get production-quality data for your AI agent. You can sign up [9] and get 10,000 free credits per month, sign up for one of our plans [10], or [come talk to us] [11] if you’re interested in an enterprise solution. We offer both SaaS and self-hosted plans.
You can also check out the LlamaCloud documentation [2] for more details.
- **Document Parsing (LlamaParse)**: LlamaParse is the best-in-class document parsing solution. It’s powered by VLMs and perfect for even the most complex documents (nested tables, embedded charts/images, and more). Learn more [12] or check out the docs [13]. - **Document Extraction (LlamaExtract)**: Given a human-defined or inferred schema, extract structured data from any document. Learn more [14] or check out the [docs] [17]. - **Indexing/Retrieval**: Set up an e2e pipeline to index a collection of documents for retrieval. Connect your data source (e.g. Sharepoint, Google Drive, S3), your vector DB data sink, and we automatically handle the document processing and syncing. Learn more [15] or check out the docs [16].

## Community
Need help? Have a feature suggestion? Join the LlamaIndex community:
- Twitter [18] - Discord [19] - LinkedIn [20]
### Getting the library
- LlamaIndex Python
- LlamaIndex Python Github [21] - Python Docs [22] (what you’re reading now) - LlamaIndex on PyPi [23]
- LlamaIndex.TS (Typescript/Javascript package):
- LlamaIndex.TS Github [24] - TypeScript Docs [6] - LlamaIndex.TS on npm [25]
### Contributing
We are open-source and always welcome contributions to the project! Check out our contributing guide [26] for full details on how to extend the core library or add an integration to a third party like an LLM, a vector store, an agent tool and more.
## LlamaIndex Ecosystem
There’s more to the LlamaIndex universe! Check out some of our other projects:
- llama\_deploy [27] | Deploy your agentic workflows as production microservices - LlamaHub [4] | A large (and growing!) collection of custom data connectors - SEC Insights [28] | A LlamaIndex-powered application for financial research - create-llama [5] | A CLI tool to quickly scaffold LlamaIndex projects

[1] https://en.wikipedia.org/wiki/Large_language_model
[2] https://docs.cloud.llamaindex.ai/
[3] https://developers.llamaindex.ai/python/cloud/llamaparse/
[4] https://llamahub.ai
[5] https://www.npmjs.com/package/create-llama
[6] https://ts.llamaindex.ai/
[7] https://platform.openai.com/api-keys
[8] https://llamaindex.ai/enterprise
[9] https://cloud.llamaindex.ai/
[10] https://www.llamaindex.ai/pricing
[11] https://www.llamaindex.ai/contact
[12] https://www.llamaindex.ai/llamaparse
[13] https://docs.cloud.llamaindex.ai/llamaparse
[14] https://www.llamaindex.ai/llamaextract
[15] https://www.llamaindex.ai/enterprise
[16] https://docs.cloud.llamaindex.ai/llamacloud/getting_started
[17] https://docs.cloud.llamaindex.ai/llamaextract/getting_started
[18] https://twitter.com/llama_index
[19] https://discord.gg/dGcwcsnxhU
[20] https://www.linkedin.com/company/llamaindex/
[21] https://github.com/run-llama/llama_index
[22] https://docs.llamaindex.ai/
[23] https://pypi.org/project/llama-index/
[24] https://github.com/run-llama/LlamaIndexTS
[25] https://www.npmjs.com/package/llamaindex
[26] https://github.com/run-llama/llama_index/blob/main/CONTRIBUTING.md
[27] https://github.com/run-llama/llama_deploy
[28] https://secinsights.ai