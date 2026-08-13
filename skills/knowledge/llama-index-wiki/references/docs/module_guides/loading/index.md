# developers.llamaindex.ai/python/framework/module_guides/loading/index.md
> https://developers.llamaindex.ai/python/framework/module_guides/loading/index.md

[Column 1]
--- title: Loading Data | Developer Documentation ---
### Loading
### Transformations
This includes common operations like splitting text.
### Putting it all Together
### Abstractions

[Column 2]
The key to data ingestion in LlamaIndex is loading and transformations. Once you have loaded Documents, you can process them via transformations and output Nodes.
Once you have learned about the basics of loading data in our Understanding section, you can read on to learn more about:
- SimpleDirectoryReader, our built-in loader for loading all sorts of file types from a local directory - LlamaParse, LlamaIndex’s official tool for PDF parsing, available as a managed API. - LlamaHub, our registry of hundreds of data loading libraries to ingest data from any source
- Node Parser Usage Pattern, showing you how to use our node parsers - Node Parser Modules, showing our text splitters (sentence, token, HTML, JSON) and other parser modules.
- The ingestion pipeline which allows you to set up a repeatable, cache-optimized process for loading data.
- Document and Node objects and how to customize them for more advanced use cases
