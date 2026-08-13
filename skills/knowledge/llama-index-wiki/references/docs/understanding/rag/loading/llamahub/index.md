# developers.llamaindex.ai/python/framework/understanding/rag/loading/llamahub/index.md
> https://developers.llamaindex.ai/python/framework/understanding/rag/loading/llamahub/index.md

--- title: LlamaHub | Developer Documentation ---

Our data connectors are offered through LlamaHub [1] 🦙. LlamaHub contains a registry of open-source data connectors that you can easily plug into any LlamaIndex application (+ Agent Tools, and Llama Packs).

## Usage Pattern
Get started with:
``` from llama_index.core import download_loader

from llama_index.readers.google import GoogleDocsReader

[Column 1]
loader = GoogleDocsReader() documents = loader.load_data(document_ids=[...]) ```
## Built-in connector: SimpleDirectoryReader
``` from llama_index.core import SimpleDirectoryReader

[Column 2]
`SimpleDirectoryReader`. Can support parsing a wide range of file types including `.md`, `.pdf`, `.jpg`, `.png`, `.docx`, as well as audio and video types. It is available directly as part of LlamaIndex:


documents = SimpleDirectoryReader("./data").load_data() ```
## Available connectors
Browse LlamaHub [1] directly to see the hundreds of connectors available, including:
- Notion [2] (`NotionPageReader`) - Google Docs [3] (`GoogleDocsReader`) - Slack [4] (`SlackReader`) - Discord [5] (`DiscordReader`) - Apify Actors [6] (`ApifyActor`). Can crawl the web, scrape webpages, extract text content, download files including `.pdf`, `.jpg`, `.png`, `.docx`, etc.

[1] https://llamahub.ai/
[2] https://developers.notion.com/
[3] https://developers.google.com/docs/api
[4] https://api.slack.com/
[5] https://discord.com/developers/docs/intro
[6] https://llamahub.ai/l/apify-actor