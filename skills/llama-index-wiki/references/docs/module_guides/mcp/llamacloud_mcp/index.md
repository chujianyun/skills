# developers.llamaindex.ai/python/framework/module_guides/mcp/llamacloud_mcp/index.md
> https://developers.llamaindex.ai/python/framework/module_guides/mcp/llamacloud_mcp/index.md

--- title: LlamaCloud MCP Servers & Tools | Developer Documentation ---
LlamaIndex provides official MCP servers that integrate with LlamaCloud services like LlamaCloud Indexes and LlamaExtract.
The `llamacloud-mcp` [1] Python package provides an alternative implementation that supports both query and extraction capabilities, using LlamaCloud indexes as knowledge bases and LlamaExtract agents for structured extraction.
## Installation

[Column 1]
``` pip install llamacloud-mcp *# or* uvx llamacloud-mcp@latest ```

## Claude Usage
To use with an MCP host like claude-code, you can set your configuration file like so:
``` { "mcpServers": { "llama_index_docs_server": { "command": "uvx", "args": [ "llamacloud-mcp@latest", "--index", "your-index-name:Description of your index", "--index", "your-other-index-name:Description of your other index", "--extract-agent", "extract-agent-name:Description of your extract agent", "--project-name", "<Your LlamaCloud Project Name>", "--org-id", "<Your LlamaCloud Org ID>", "--api-key", "<Your LlamaCloud API Key>" ] }, "filesystem": { "command": "npx", "args": [ "-y", "@modelcontextprotocol/server-filesystem", "<your directory you want filesystem tool to have access to>" ] } } } ```

## General Usage

You can launch the server directly from the command line:
Terminal window

[Column 2]
By default, the MCP server is launched with the `stdio` transport. This is useful for hosts like Claude Desktop that support MCP servers via stdin/stdout, but you can also launch the server with the `streamable-http` or `sse` transport, which is useful for hosts that support MCP servers via HTTP.
``` llamacloud-mcp --index "index-name:Description" --extract-agent "name:description" --org-id YOUR_ORG_ID --project-id YOUR_PROJECT_ID --api-key YOUR_API_KEY --transport streamable-http ```


[1] https://github.com/run-llama/llamacloud-mcp