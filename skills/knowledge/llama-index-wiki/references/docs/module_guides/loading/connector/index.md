# developers.llamaindex.ai/python/framework/module_guides/loading/connector/index.md
> https://developers.llamaindex.ai/python/framework/module_guides/loading/connector/index.md

--- title: Data Connectors (LlamaHub) | Developer Documentation ---
## Concept
A data connector (aka `Reader`) ingest data from different data sources and data formats into a simple `Document` representation (text and simple metadata).
Tip
Once you’ve ingested your data, you can build an Index on top, ask questions using a Query Engine, and have a conversation using a Chat Engine.
## LlamaHub
Our data connectors are offered through LlamaHub [1] 🦙. LlamaHub is an open-source repository containing data loaders that you can easily plug and play into any LlamaIndex application.

## Usage Pattern
Get started with:
``` from llama_index.core import download_loader

from llama_index.readers.google import GoogleDocsReader

loader = GoogleDocsReader() documents = loader.load_data(document_ids=[...]) ```
See the full usage pattern guide for more details.
## Modules
Some sample data connectors:
- local file directory (`SimpleDirectoryReader`). Can support parsing a wide range of file types: `.pdf`, `.jpg`, `.png`, `.docx`, etc. - Notion [2] (`NotionPageReader`) - Google Docs [3] (`GoogleDocsReader`) - Slack [4] (`SlackReader`) - Discord [5] (`DiscordReader`) - Apify Actors [6] (`ApifyActor`). Can crawl the web, scrape webpages, extract text content, download files including `.pdf`, `.jpg`, `.png`, `.docx`, etc.

See the modules guide for more details.

[1] https://llamahub.ai/
[2] https://developers.notion.com/
[3] https://developers.google.com/docs/api
[4] https://api.slack.com/
[5] https://discord.com/developers/docs/intro
[6] https://llamahub.ai/l/readers/llama-index-readers-apify