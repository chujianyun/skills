# developers.llamaindex.ai/python/framework/module_guides/mcp/convert_existing/index.md
> https://developers.llamaindex.ai/python/framework/module_guides/mcp/convert_existing/index.md

--- title: Converting Existing LlamaIndex Workflows & Tools to MCP | Developer Documentation ---
Convert your LlamaIndex tools and workflows into MCP servers for broader ecosystem compatibility.
## Converting Workflows

Use `workflow_as_mcp` to convert any LlamaIndex Workflow into an FastMCP [1] server:

``` from workflows import Context, Workflow, step from workflows.events import StartEvent, StopEvent from llama_index.tools.mcp.utils import workflow_as_mcp

class QueryEvent(StartEvent): query: str

class SimpleWorkflow(Workflow): @ step def process_query(self, ctx: Context, ev: QueryEvent) -> StopEvent: result = f"Processed: {ev.query}" return StopEvent(result=result)

# Convert to MCP server workflow = SimpleWorkflow() mcp = workflow_as_mcp(workflow, start_event_model=QueryEvent) ```

If you were using FastMCP [1] directly, it would look something like this:

``` from fastmcp import FastMCP
# Workflow definition ...
mcp = FastMCP("Demo 🚀") workflow = SimpleWorkflow()

@mcp.tool async def run_my_workflow(input_args: QueryEvent) -> str: """Add two numbers""" if isintance(input_args, dict): input_args = QueryEvent.model_validate(input_args) result = await workflow.run(start_event=input_args) return str(result)

if __name__ == "__main__": mcp.run() ```
## Converting Individual Tools
We can also use FastMCP to directly convert existing functions and tools input MCP endpoints:
``` from fastmcp import FastMCP from llama_index.tools.notion import NotionToolSpec

# Get tools from ToolSpec tool_spec = NotionToolSpec(integration_token="your_token") tools = tool_spec.to_tool_list()

# Create MCP server mcp_server = FastMCP("Tool Server")
# Register tools for tool in tools: mcp_server.tool( name=tool.metadata.name, description=tool.metadata.description )(tool.real_fn) ```

## Running MCP Server
You can launch your server from the CLI (which is also great for debugging!):
Terminal window
``` # Install MCP CLI pip install "mcp[cli]"

# Run server mcp run your-server.py ```

[1] https://github.com/jlowin/fastmcp