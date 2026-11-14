# Get started with Studio

[Studio](LangSmith%20Studio.md) in the [LangSmith Agent Server UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-quick-start-studio) supports connecting to two types of graphs:

* Graphs deployed on [cloud or self-hosted](#deployed-graphs).
* Graphs running locally with [Agent Server](#local-development-server).

## Deployed graphs

Studio is accessed in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-quick-start-studio) from the **Agent Servers** navigation.

For applications that are [deployed](../../Deploy/Get%20started/Deploy%20your%20app%20to%20cloud.md), you can access Studio as part of that Agent Server. To do so, navigate to the Agent Server in the UI and select **Studio**.

This will load Studio connected to your live Agent Server, allowing you to create, read, and update the [threads](https://docs.langchain.com/oss/python/langgraph/checkpointers.md#threads), [assistants](../../Deploy/Agent%20Server/Capabilities/Assistants/Assistants.md), and [memory](https://docs.langchain.com/oss/python/concepts/memory.md) in that Agent Server.

## Local development server

### Prerequisites

To test your application locally using Studio:

* Follow the [local application quickstart](../../Deploy/Get%20started/Develop%20%26%20test/Local%20development%20%26%20testing.md) first.
* If you don't want data [traced](../../Monitor/Trace/Observability%20concepts.md#traces) to LangSmith, set `LANGSMITH_TRACING=false` in your application's `.env` file. With tracing disabled, no data leaves your local server.

### Setup

1. Install the [LangGraph CLI](../../Deploy/Get%20started/Reference/LangGraph%20CLI.md):

   ```bash pip
   pip install -U "langgraph-cli[inmem]"
   langgraph dev
   ```

   ```bash uv
   uv add "langgraph-cli[inmem]"
   langgraph dev
   ```

   ```bash npm
   npx @langchain/langgraph-cli dev
   ```

   > [!WARNING]
   >
   > **Browser Compatibility**
   > Safari blocks `localhost` connections to Studio. To work around this, run the command with `--tunnel` to access Studio via a secure tunnel. You'll need to manually add the tunnel URL to allowed origins by clicking **Connect to a local server** in the Studio UI. See the [troubleshooting guide](Studio%20troubleshooting.md#safari-connection-issues) for steps.

   This will start the Agent Server locally, running in-memory. The server will run in watch mode, listening for and automatically restarting on code changes. Read this [reference](../../Deploy/Get%20started/Reference/LangGraph%20CLI.md#dev) to learn about all the options for starting the API server.

   You will see the following logs:

   ```
   > Ready!
   >
   > - API: [http://localhost:2024](http://localhost:2024/)
   >
   > - Docs: http://localhost:2024/docs
   >
   > - LangSmith Studio Web UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
   ```

   Once running, you will automatically be directed to Studio.

2. For a running server, access the Dbugger with one of the following:

   1. Directly navigate to the following URL: `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`.
   2. Navigate to **Agent Servers** in the UI, click the **Studio** button on an Agent Server, enter `http://127.0.0.1:2024` and click **Connect**.

   If running your server at a different host or port, update the `baseUrl` to match.

### (Optional) Attach a debugger

For step-by-step debugging with breakpoints and variable inspection, run the following:

```bash pip
# Install debugpy package
pip install debugpy
# Start server with debugging enabled
langgraph dev --debug-port 5678
```

```bash uv
# Install debugpy package
uv add debugpy
# Start server with debugging enabled
langgraph dev --debug-port 5678
```

Then attach your preferred debugger:

> [tab] VS Code
>
> Add this configuration to `launch.json`:
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>     "name": "Attach to LangGraph",
>     "type": "debugpy",
>     "request": "attach",
>     "connect": {
>       "host": "0.0.0.0",
>       "port": 5678
>     }
> }
> ```

> [tab] PyCharm
>
> 1. Go to Run > Edit Configurations
> 2. Click + and select "Python Debug Server"
> 3. Set IDE host name: `localhost`
> 4. Set port: `5678` (or the port number you chose in the previous step)
> 5. Click "OK" and start debugging

> [!TIP]
>
> For issues getting started, refer to the [troubleshooting guide](Studio%20troubleshooting.md).

## Next steps

For more information on how to run Studio, refer to the following guides:

* [Run application](How%20to%20use%20Studio.md#run-application)
* [Manage assistants](How%20to%20use%20Studio.md#manage-assistants)
* [Manage threads](How%20to%20use%20Studio.md#manage-threads)
* [Iterate on prompts](Observability%20in%20Studio.md)
* [Debug LangSmith traces](Observability%20in%20Studio.md#debug-langsmith-traces)
* [Add node to dataset](Observability%20in%20Studio.md#add-node-to-dataset)
