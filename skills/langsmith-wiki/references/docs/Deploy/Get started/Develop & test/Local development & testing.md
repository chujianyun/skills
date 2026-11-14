# Local development & testing

> Compare langgraph dev and langgraph up for local development and production-like testing of Agent Server applications.

This guide covers how to develop and test [Agent Server](../../Agent%20Server/Capabilities/Agent%20Server.md) applications locally. The [LangGraph CLI](../Reference/LangGraph%20CLI.md) provides two commands for local development, each optimized for different stages of your workflow:

* [`langgraph dev`](#langgraph-dev): A lightweight development server for rapid iteration.
* [`langgraph up`](#langgraph-up): A production-like testing environment for validation.

| Feature | `langgraph dev` | `langgraph up` |
| - | - | - |
| **Docker required** | No | Yes |
| **Installation** | `pip install langgraph-cli[inmem]` | `pip install langgraph-cli` |
| **Primary use case** | Rapid development & testing | Production-like validation |
| **State persistence** | In-memory & pickled to local directory | PostgreSQL |
| **Hot reloading** | Yes (default) | Optional (`--watch` flag) |
| **Default port** | `2024` | `8123` |
| **Resource usage** | Lightweight | Heavier (build and run separate docker containers for the server, PostgreSQL, and Redis) |
| **IDE Debugging** | Built-in [DAP](https://microsoft.github.io/debug-adapter-protocol/) support | Regular container debugging |
| **Custom auth** | Yes | Yes (with license key) |

> [!TIP]
>
> For full reference details, refer to the [LangGraph CLI reference](../Reference/LangGraph%20CLI.md) page.

## Development

Here's the typical workflow when building applications:

```mermaid
flowchart LR
    A["Develop<br/><code>langgraph dev</code>"] --> B["Test Locally<br/><code>langgraph dev</code>"] --> C["Validate<br/><code>langgraph up</code>"] --> D["Deploy<br/>via UI or API"]

    style A fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
    style B fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
    style C fill:#FDF3FF,stroke:#7E65AE,stroke-width:2px,color:#504B5F
    style D fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
```

| Stage | Tool | Purpose |
| - | - | - |
| **Develop & Test Locally** | [`langgraph dev`](../Reference/LangGraph%20CLI.md#dev) | Write and iterate on your graph with hot reloading |
| **Validate** | [`langgraph up`](../Reference/LangGraph%20CLI.md#up) | Test production-like behavior with full stack |
| **Deploy** | [`langgraph deploy`](../Reference/LangGraph%20CLI.md#deploy) | Deploy to production with confidence |

### Recommended workflow

1. **Daily development**: Use `langgraph dev` for rapid iteration.
2. **Periodic validation**: Test major changes with `langgraph up`.
3. **Pre-deployment check**: Run `langgraph up --recreate` for a fresh build.
4. **Deploy**: Push to production via the [LangSmith UI](../Deploy%20your%20app%20to%20cloud.md) or [Control Plane API](../Reference/Control%20Plane%20API/Control%20plane%20API%20reference%20for%20Agent%20Server%20hosting.md).

## `langgraph dev`

The [`langgraph dev`](../Reference/LangGraph%20CLI.md#dev) command runs a lightweight server directly in your environment, designed for speed and convenience during active development. The key features include:

* **No Docker required**: Runs directly in your environment.
* **Hot reloading**: Automatically reloads when you change code.
* **Fast startup**: Ready in seconds.
* **Built-in [Debug Adapter Protocol](https://microsoft.github.io/debug-adapter-protocol/) support**: Attach your IDE debugger to the server for line-level breakpoints & debugging.
* **Local storage**: State persisted to local directory.

> [!NOTE]
>
> The `dev` server is tested with the same integration test suite as production to ensure its behavior is the same during development while using minimal resources.

> [accordion] Get started with langgraph dev
>
> Before you begin, ensure you have:
>
> * An API key for [LangSmith](https://smith.langchain.com/settings) (free to sign up).
> * [uv](https://docs.astral.sh/uv/getting-started/installation/) for Python or [npx](https://docs.npmjs.com/cli/commands/npx) for TypeScript.
>
> **1. Create a LangGraph app**
>
> Create a new app from the [`new-langgraph-project-python` template](https://github.com/langchain-ai/new-langgraph-project) or [`new-langgraph-project-js` template](https://github.com/langchain-ai/new-langgraphjs-project). This template demonstrates a single-node application you can extend with your own logic.
>
> > [tab] Python server
> >
> > ```shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > uvx --from langgraph-cli@latest langgraph new path/to/your/app --template new-langgraph-project-python
> > ```
>
> > [tab] Node server
> >
> > ```shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > npx @langchain/langgraph-cli new path/to/your/app --template new-langgraph-project-js
> > ```
>
> > [!TIP]
> >
> > **Additional templates**\\
> >
> > If you use [`langgraph new`](../Reference/LangGraph%20CLI.md) without specifying a template, you will be presented with an interactive menu that will allow you to choose from a list of available templates.
>
> **2. Install dependencies**
>
> > [tab] Python server
> >
> > ```shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > cd path/to/your/app
> > uv sync --dev -U
> > ```
>
> > [tab] Node server
> >
> > ```shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > cd path/to/your/app
> > yarn install
> > ```
>
> **3. Launch Agent Server**
>
> > [tab] Python server
> >
> > ```shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > uv run langgraph dev
> > ```
>
> > [tab] Node server
> >
> > ```shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > npx @langchain/langgraph-cli dev
> > ```
>
> Sample output:
>
> ```
> >    Ready!
> >
> >    - API: [http://localhost:2024](http://localhost:2024/)
> >
> >    - Docs: http://localhost:2024/docs
> >
> >    - Studio Web UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
> ```
>
> **4. Test the API**
>
> > [tab] Python SDK (async)
> >
> > 1. Install the LangGraph Python SDK:
> >
> > ```shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > pip install langgraph-sdk
> > ```
> >
> > 2. Send a message to the assistant (threadless run):
> >
> > ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langgraph_sdk import get_client
> > import asyncio
> >
> > client = get_client(url="http://localhost:2024")
> >
> > async def main():
> >     async for chunk in client.runs.stream(
> >         None,  # Threadless run
> >         "agent", # Name of assistant. Defined in langgraph.json.
> >         input={
> >         "messages": [{
> >             "role": "human",
> >             "content": "What is LangGraph?",
> >             }],
> >         },
> >     ):
> >         print(f"Receiving new event of type: {chunk.event}...")
> >         print(chunk.data)
> >         print("\n\n")
> >
> > asyncio.run(main())
> > ```
>
> > [tab] Python SDK (sync)
> >
> > 1. Install the LangGraph Python SDK:
> >
> > ```shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > pip install langgraph-sdk
> > ```
> >
> > 2. Send a message to the assistant (threadless run):
> >
> > ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > from langgraph_sdk import get_sync_client
> >
> > client = get_sync_client(url="http://localhost:2024")
> >
> > for chunk in client.runs.stream(
> >     None,  # Threadless run
> >     "agent", # Name of assistant. Defined in langgraph.json.
> >     input={
> >         "messages": [{
> >             "role": "human",
> >             "content": "What is LangGraph?",
> >         }],
> >     },
> >     stream_mode="messages-tuple",
> > ):
> >     print(f"Receiving new event of type: {chunk.event}...")
> >     print(chunk.data)
> >     print("\n\n")
> > ```
>
> > [tab] Javascript SDK
> >
> > 1. Install the LangGraph JS SDK:
> >
> > ```shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > npm install @langchain/langgraph-sdk
> > ```
> >
> > 2. Send a message to the assistant (threadless run):
> >
> > ```js theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > const { Client } = await import("@langchain/langgraph-sdk");
> >
> > // only set the apiUrl if you changed the default port when calling langgraph dev
> > const client = new Client({ apiUrl: "http://localhost:2024"});
> >
> > const streamResponse = client.runs.stream(
> >     null, // Threadless run
> >     "agent", // Assistant ID
> >     {
> >         input: {
> >             "messages": [
> >                 { "role": "user", "content": "What is LangGraph?"}
> >             ]
> >         },
> >         streamMode: "messages-tuple",
> >     }
> > );
> >
> > for await (const chunk of streamResponse) {
> >     console.log(`Receiving new event of type: ${chunk.event}...`);
> >     console.log(JSON.stringify(chunk.data));
> >     console.log("\n\n");
> > }
> > ```
>
> > [tab] Rest API
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > curl -s --request POST \
> >     --url "http://localhost:2024/runs/stream" \
> >     --header 'Content-Type: application/json' \
> >     --data "{
> >         \"assistant_id\": \"agent\",
> >         \"input\": {
> >             \"messages\": [
> >                 {
> >                     \"role\": \"human\",
> >                     \"content\": \"What is LangGraph?\"
> >                 }
> >             ]
> >         },
> >         \"stream_mode\": \"messages-tuple\"
> >     }"
> > ```

### Use cases

Use `langgraph dev` as your primary development tool for:

* **Daily feature development**: Make changes to your code and the server automatically reloads. Test immediately without rebuilding containers—perfect for fast iteration cycles.

* **Quick prototyping and experiments**: Spin up a server in seconds to test ideas without Docker setup overhead.

* **Environments without Docker**: In CI/CD pipelines or lightweight VMs where Docker isn't available:
  ```bash
  langgraph dev --no-browser
  ```

* **Debugger attachment**: Use `--debug-port` to attach your IDE debugger for step-through debugging during development.

## `langgraph up`

The [`langgraph up`](../Reference/LangGraph%20CLI.md#up) command orchestrates a full Docker-based stack that mirrors production infrastructure, helping catch deployment issues before production. The key features include:

* **Verify build & dependencies**: Tests your build process and dependencies.
* **Isolated networking**: Realistic container networking.
* **Production validation**: Verifies deployment readiness.

> [accordion] Get started with langgraph up
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Ensure Docker is running
> docker ps
>
> # Start production-like stack
> langgraph up
> ```
>
> Your server starts at `http://localhost:8123` with full persistent storage.

### Use cases

Use `langgraph up` for validation and production-readiness testing:

* **Pre-deployment validation**: Before deploying to production, you can run a final check with a fresh build to ensure your dependencies are all correctly specified.

  ```bash
  langgraph up --recreate
  ```

  This catches issues related to dependency resolution in containers and any other build process problems.

* **Major feature validation**: After implementing significant changes, test with the full production stack periodically to ensure everything works in a containerized environment.

* **Docker troubleshooting**: When debugging container-specific issues, networking problems, or environment variable configurations that only appear in production.

## Pre-deployment checklist

Before deploying an application, verify the following with `langgraph up`:

* All [dependencies](../../Agent%20Server/Develop%20your%20application/Set%20up%20dependencies/How%20to%20set%20up%20an%20application%20with%20requirements.txt.md) install correctly in the container.
* Application starts without errors.
* Graph executes successfully.
* All [environment variables](../../Deploy%20to%20Cloud/Reference/Cloud%20Agent%20Server%20environment%20variables.md) work correctly.
* [Authentication/authorization](../Reference/LangGraph%20CLI.md#adding-custom-authentication) works as expected.

## Dependencies configuration

Both `langgraph dev` and `langgraph up` read your application's [dependencies](../../Agent%20Server/Develop%20your%20application/Application%20structure.md#dependencies) from your [configuration files](../../Agent%20Server/Develop%20your%20application/Application%20structure.md#configuration-file), but they run in different environments:

* **`langgraph dev`** runs your code directly in your local environment (Python or Node.js) without Docker.
* **`langgraph up`** builds a Docker container and runs your code inside that isolated container.

Properly configuring your dependencies ensures both commands work correctly and that what you test locally matches what gets deployed to production.

### `langgraph.json` file

The `dependencies` field tells the [CLI](../Reference/LangGraph%20CLI.md) **where** to find your application code. The `dependencies` field can point to:

* **A directory with package config** (containing `pyproject.toml`, `setup.py`, `requirements.txt`, or `package.json`)
* **A specific subdirectory**: `"dependencies": ["./my_agent"]`
* **A specific package**: `"dependencies": ["my-package==1.0.0"]` (Python) or `"dependencies": ["my-package@1.0.0"]` (JavaScript)

> [tab] Python
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "dependencies": ["."],
>   "graphs": {
>     "my_agent": "./my_agent/agent.py:graph"
>   },
>   "env": "./.env"
> }
> ```

> [tab] JavaScript
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "dependencies": ["."],
>   "graphs": {
>     "my_agent": "./my_agent/agent.js:graph"
>   },
>   "env": "./.env"
> }
> ```

### Package dependency files

These files define **what** packages your application needs:

> [tab] Python
>
> **pyproject.toml example:**
>
> ```toml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> [project]
> name = "my-agent"
> version = "0.1.0"
> dependencies = [
>     "langchain-openai",
>     "langchain-anthropic",
>     "langgraph",
> ]
> ```
>
> **requirements.txt example:**
>
> ```
> langchain-openai
> langchain-anthropic
> langgraph
> ```

> [tab] JavaScript
>
> **package.json example:**
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "name": "my-agent",
>   "version": "1.0.0",
>   "dependencies": {
>     "@langchain/openai": "^0.3.0",
>     "@langchain/anthropic": "^0.3.0",
>     "@langchain/langgraph": "^0.2.0"
>   }
> }
> ```

### Dependency resolution process

When you run [`langgraph up`](../Reference/LangGraph%20CLI.md#up), the CLI follows these steps to install your application's dependencies:

1. [`langgraph.json`](../../Agent%20Server/Develop%20your%20application/Application%20structure.md#configuration-file) tells the CLI **where** to look for your application code. The `dependencies: ["."]` field points to the current directory.
2. **Find package configuration**: The CLI looks in that directory for a package configuration file ([`pyproject.toml`](../../Agent%20Server/Develop%20your%20application/Set%20up%20dependencies/How%20to%20set%20up%20an%20application%20with%20pyproject.toml.md), [`requirements.txt`](../../Agent%20Server/Develop%20your%20application/Set%20up%20dependencies/How%20to%20set%20up%20an%20application%20with%20requirements.txt.md), or [`package.json`](../../Agent%20Server/Develop%20your%20application/Set%20up%20dependencies/How%20to%20set%20up%20a%20JavaScript%20application.md)).
3. **Read dependencies list**: The CLI reads the list of packages from the configuration file.
4. **Install packages**: The CLI installs all the packages using the appropriate package manager for your language (`uv` or `pip` for Python, `npm` for JavaScript).

This two-file approach separates concerns: `langgraph.json` handles application structure and location, while the package configuration file handles language-specific package dependencies.

For more information on the installer, refer to [CLI configuration file](../Reference/LangGraph%20CLI.md#configuration-file).

### Troubleshooting

If you encounter issues with dependency installation, try switching to `pip`:

```json
{
  "dependencies": ["."],
  "pip_installer": "pip"
}
```

Then rebuild:

```bash
langgraph up --recreate
```

## Debug your local Docker setup

Production deployment might succeed even when `langgraph up` fails on your local machine. This happens because production uses managed infrastructure while `langgraph up` runs the full stack locally on your computer.

The following are common local environment issues that don't affect production.

### Docker configuration issues

`langgraph up` requires Docker locally:

```bash
# Check if Docker is running
docker ps
```

[Cloud deployments](../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) don't use your local Docker.

**Solution**: Install Docker, or use `langgraph dev` for local testing.

### Port conflicts

`langgraph up` uses ports `8123`, `5432`, and `6379` that might be occupied:

```bash
# Check for conflicts
lsof -i :8123  # API server
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis
```

**Solution**: Stop conflicting services or use the [`--port`](../Reference/LangGraph%20CLI.md#dev) flag.

### Resource constraints

`langgraph up` requires more RAM and disk for:

* PostgreSQL container
* Redis container
* API server container

**Solution**: Free up resources or use `langgraph dev`.

### Network configuration

VPN connections, firewall rules, or corporate proxy settings can affect local Docker networking.

**Solution**: Test with `langgraph dev` or temporarily disable VPN/firewall to isolate the issue.

## Next steps

Now that you have a LangGraph app running locally, you're ready to deploy it:

**Choose a hosting option for LangSmith:**

* [**Cloud**](../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md): Fastest setup, fully managed (recommended).
* [**Self-hosted**](../../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md): Full control in your infrastructure.

For more details, refer to the [Platform setup comparison](../../../LangSmith%20setup/Overview/Hosting/Set%20up%20LangSmith.md).

**Then deploy your app:**

* [Deploy to Cloud quickstart](../Deploy%20your%20app%20to%20cloud.md): Quick setup guide.
* [Full Cloud setup guide](../../Deploy%20to%20Cloud/Deployment%20guide/Create%20an%20Agent%20Server.md): Comprehensive deployment documentation.

**Explore features:**

* **[Studio](../../../Test/Test%20from%20Studio/LangSmith%20Studio.md)**: Visualize, interact with, and debug your application with the Studio UI. Try the [Studio quickstart](../../../Test/Test%20from%20Studio/Get%20started%20with%20Studio.md).
* **API References**: [LangSmith Agent Server API](../Reference/Agent%20Server%20API/Agent%20Server%20API%20reference.md), [Python SDK](../Reference/Related/langgraph_sdk.md), [JS/TS SDK](../Reference/Related/%40langchain-langgraph-sdk.md)

## Related resources

* [CLI Reference](../Reference/LangGraph%20CLI.md): Detailed documentation for all CLI commands
* [Application Structure](../../Agent%20Server/Develop%20your%20application/Application%20structure.md): How to structure your LangGraph application
* [Troubleshooting](../../../Test/Test%20from%20Studio/Studio%20troubleshooting.md): Common issues and solutions
* [Setting up with pyproject.toml](../../Agent%20Server/Develop%20your%20application/Set%20up%20dependencies/How%20to%20set%20up%20an%20application%20with%20pyproject.toml.md): Configure Python dependencies
* [Setting up with requirements.txt](../../Agent%20Server/Develop%20your%20application/Set%20up%20dependencies/How%20to%20set%20up%20an%20application%20with%20requirements.txt.md): Alternative dependency configuration
