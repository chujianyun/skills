# LangGraph CLI

**LangGraph CLI** is a command-line tool for building and running the [Agent Server](../../Agent%20Server/Capabilities/Agent%20Server.md) locally. The resulting server exposes all API endpoints for runs, threads, assistants, etc., and includes supporting services such as a managed database for checkpointing and storage.

## Installation

1. Ensure Docker is installed (e.g., `docker --version`).

2. Install the CLI:

   ```bash [Python (pip)]
   pip install langgraph-cli
   ```

   ```bash JavaScript
   # Use latest on demand
   npx @langchain/langgraph-cli

   # Or install globally (available as `langgraphjs`)
   npm install -g @langchain/langgraph-cli
   ```

3. Verify the install

   ```bash [Python (pip)]
   langgraph --help
   ```

   ```bash JavaScript
   npx @langchain/langgraph-cli --help
   ```

### Quick commands

| Command | What it does |
| - | - |
| [`langgraph dev`](#dev) | Starts a lightweight local dev server (no Docker required), ideal for rapid testing. |
| [`langgraph build`](#build) | Builds a Docker image of your Agent Server for deployment. |
| [`langgraph deploy`](#deploy) | Builds and deploys a LangGraph image directly to LangSmith Agent Server in a single step. |
| [`langgraph dockerfile`](#dockerfile) | Emits a Dockerfile derived from your config for custom builds. |
| [`langgraph up`](#up) | Starts the Agent Server locally in Docker. Requires Docker running; LangSmith API key for local dev; license for production. |

For JS, use `npx @langchain/langgraph-cli <command>` (or `langgraphjs` if installed globally).

## Configuration file

To build and run a valid application, the LangGraph CLI requires a JSON configuration file that follows this [schema](https://raw.githubusercontent.com/langchain-ai/langgraph/refs/heads/main/libs/cli/schemas/schema.json). It contains the following properties:

> [!NOTE]
>
> The LangGraph CLI defaults to using the configuration file named **langgraph.json** in the current directory.

> [tab] Python
>
> | Key | Description |
> | - | - |
> | `dependencies` | **Required** unless [`source`](#configuration-file) is set. Array of dependencies for the Agent Server. Dependencies can be one of the following: <ul><li>A single period (`"."`), which will look for local Python packages.</li><li>The directory path where `pyproject.toml`, `setup.py` or `requirements.txt` is located. For example, if `requirements.txt` is located in the root of the project directory, specify `"./"`. If it's located in a subdirectory called `local_package`, specify `"./local_package"`. Do not specify the string `"requirements.txt"` itself.</li><li>A Python package name.</li></ul> |
> | `graphs` | **Required**. Mapping from graph ID to path where the compiled graph or a function that makes a graph is defined. Example: <ul><li>`./your_package/your_file.py:variable`, where `variable` is an instance of `langgraph.graph.state.CompiledStateGraph`</li><li>`./your_package/your_file.py:make_graph`, where `make_graph` is a function that takes a config dictionary (`langchain_core.runnables.RunnableConfig`) and returns an instance of `langgraph.graph.state.StateGraph` or `langgraph.graph.state.CompiledStateGraph`. See [how to rebuild a graph at runtime](../../Agent%20Server/Server%20customization/Rebuild%20graph%20at%20runtime.md) for more details.</li></ul> |
> | `auth` | *(Added in v0.0.11)* Authentication and authorization configuration. Contains: <ul><li>`path` (required): Path to your authentication handler (e.g., `./your_package/auth.py:auth`), where `auth` is an instance of `langgraph_sdk.Auth`. See [authentication guide](../../Agent%20Server/Auth%20%26%20access%20control/Authentication%20%26%20access%20control.md).</li><li>`disable_studio_auth` (optional): If `true`, Studio cannot use LangSmith auth as a fallback. Defaults to `false`.</li><li>`allow_langsmith_api_keys` (optional, Agent Server v0.14.0rc2+): If `true`, run LangSmith API-key auth alongside custom auth. Requests with an `Authorization` header go to custom auth; all others go to LangSmith (`x-api-key`). Custom `@auth.on` handlers still run. Defaults to `false`.</li><li>`openapi` (optional): Security schemes to document in OpenAPI. See [OpenAPI security](../../Agent%20Server/Auth%20%26%20access%20control/Document%20API%20authentication%20in%20OpenAPI.md).</li></ul> |
> | `priority` | *(Added in v0.18.0)* Run priority configuration. Contains: <ul><li>`path` (required): Path to your `Priority` instance (e.g., `./priority.py:priority`), where `priority` is an instance of `langgraph_sdk.Priority`. Requires `langgraph-cli>=0.4.38`.</li></ul> See [Prioritize runs](../../Agent%20Server/Capabilities/Runs/Prioritize%20runs.md). |
> | `base_image` | Optional. Base image to use for the Agent Server. Defaults to `langchain/langgraph-api` or `langchain/langgraphjs-api`. Use this to pin your builds to a particular version of the langgraph API, such as `"langchain/langgraph-server:0.2"`. See [https://hub.docker.com/r/langchain/langgraph-server/tags](https://hub.docker.com/r/langchain/langgraph-server/tags) for more details. (added in `langgraph-cli==0.2.8`) |
> | `image_distro` | Optional. Linux distribution for the base image. Must be one of `"debian"`, `"wolfi"`, `"bookworm"`, or `"bullseye"`. If omitted, defaults to `"debian"`. Available in `langgraph-cli>=0.2.11`. |
> | `env` | Path to `.env` file or a mapping from environment variable to its value. |
> | `store` | Configuration for adding semantic search and/or time-to-live (TTL) to the BaseStore. Contains the following fields: <ul><li>`index` (optional): Configuration for semantic search indexing with fields `embed`, `dims`, and optional `fields`.</li><li>`ttl` (optional): Configuration for item expiration. An object with optional fields: `refresh_on_read` (boolean, defaults to `true`), `default_ttl` (float, lifespan in **minutes**; applied to newly created items only; existing items are unchanged; defaults to no expiration), and `sweep_interval_minutes` (integer, how often to check for expired items, defaults to no sweeping).</li></ul> |
> | `ui` | Optional. Named definitions of UI components emitted by the agent, each pointing to a JS/TS file. (added in `langgraph-cli==0.1.84`) |
> | `python_version` | `3.11`, `3.12`, or `3.13`. Defaults to `3.11`. |
> | `node_version` | Specify `node_version: 20` to use LangGraph.js. |
> | `pip_config_file` | Path to `pip` config file. |
> | `pip_installer` | *(Added in v0.3)* Optional. Python package installer selector for the `dependencies`-based install path. It can be set to `"auto"`, `"pip"`, or `"uv"`. From version 0.3 onward the default strategy is to run `uv pip`, which typically delivers faster builds while remaining a drop-in replacement. In the uncommon situation where `uv` cannot handle your dependency graph or the structure of your `pyproject.toml`, specify `"pip"` here to revert to the earlier behaviour. This field does not control whether the build uses a `uv.lock` file; use [`source`](#configuration-file) for lockfile installs. |
> | `source` | *(Added in `langgraph-cli>=0.4.20`)* Optional. Install Python dependencies from a [uv](https://docs.astral.sh/uv/) project or workspace lockfile instead of from `dependencies`. Object fields: <ul><li>`kind` (required): Must be `"uv"`.</li><li>`root` (optional): Path to the directory that contains `pyproject.toml` and `uv.lock`. Defaults to `"."` (next to `langgraph.json`). Use a relative path such as `"../.."` when `langgraph.json` lives inside a workspace member.</li><li>`package` (optional): Workspace member package name to deploy when `root` is a uv workspace and the target is ambiguous.</li></ul> Requires `python_version`. Mutually exclusive with `dependencies`: omit `dependencies` when `source` is set. The build runs `uv export --frozen` from the lockfile, then installs the exported requirements. Prefer this when the project already manages dependencies with uv so Cloud and local installs use the same pinned versions. |
> | `keep_pkg_tools` | *(Added in v0.3.4)* Optional. Control whether to retain Python packaging tools (`pip`, `setuptools`, `wheel`) in the final image. Accepted values: <ul><li>`true` : Keep all three tools (skip uninstall).</li><li>`false` / omitted : Uninstall all three tools (default behaviour).</li><li>`list[str]` : Names of tools **to retain**. Each value must be one of "pip", "setuptools", "wheel".</li></ul>. By default, all three tools are uninstalled. |
> | `dockerfile_lines` | Array of additional lines to add to Dockerfile following the import from parent image. |
> | `checkpointer` | Configuration for the checkpointer. Supports: <ul><li>`backend` (optional): `"default"`, `"mongo"`, or `"custom"`. Defaults to `"default"` (PostgreSQL). See [Configure checkpointer backend](../../Agent%20Server/Develop%20your%20application/Persistence/Configure%20checkpointer%20backend.md).</li><li>`path` (optional): Path to a custom checkpointer factory (when `backend` is `"custom"`). See [Custom checkpointer](../../Agent%20Server/Server%20customization/Replace%20built-in%20backends/How%20to%20use%20a%20custom%20checkpointer.md).</li><li>`ttl` (optional): Object with `strategy`, `sweep_interval_minutes`, `default_ttl`, and `sweep_limit` (Agent Server v0.8+) controlling checkpoint expiry.</li><li>`serde` (optional, Agent Server v0.5+): Object with `allowed_json_modules` and `pickle_fallback` to tune deserialization behavior.</li></ul> |
> | `http` | HTTP server configuration with the following fields: <ul><li>`app`: Path to custom Starlette/FastAPI app (e.g., `"./src/agent/webapp.py:app"`). See [custom routes guide](../../Agent%20Server/Server%20customization/Extend%20the%20HTTP%20server/How%20to%20add%20custom%20routes.md).</li><li>`cors`: CORS configuration with fields such as `allow_origins`, `allow_methods`, `allow_headers`, `allow_credentials`, `allow_origin_regex`, `expose_headers`, and `max_age`.</li><li>`configurable_headers`: Define which request headers to expose as configurable values via `includes` / `excludes` patterns.</li><li>`logging_headers`: Mirror of `configurable_headers` for excluding sensitive headers from logs.</li><li>`middleware_order`: Choose how custom middleware and auth interact. `auth_first` runs authentication hooks before custom middleware, while `middleware_first` (default) runs your middleware first.</li><li>`enable_custom_route_auth`: Apply auth checks to routes added through `app`.</li><li>Route disable flags, which selectively turn off groups of built-in endpoints:<ul><li>`disable_meta`: Disables the `/` (root), `/info`, `/metrics`, `/docs`, and `/openapi.json` system routes. The `/ok` health check remains available.</li><li>`disable_assistants`: Disables all `/assistants/*` routes.</li><li>`disable_runs`: Disables all `/runs/*` routes.</li><li>`disable_threads`: Disables all `/threads/*` routes.</li><li>`disable_store`: Disables all `/store/*` routes.</li><li>`disable_ui`: Disables all `/ui/*` routes.</li><li>`disable_mcp`: Disables the `/mcp` endpoint. See [Disable MCP](../../Agent%20Server/Capabilities/MCP%20endpoint%20in%20Agent%20Server.md#disable-mcp).</li><li>`disable_a2a`: Disables the `/a2a/*` endpoint. See [Disable A2A](../../Agent%20Server/Capabilities/A2A%20endpoint%20in%20Agent%20Server.md#disable-a2a).</li><li>`disable_webhooks`: Disables webhook delivery on run completion (not a route toggle). See [Disable webhooks](../../Agent%20Server/Capabilities/Use%20webhooks.md#disable-webhooks).</li></ul></li><li>`mount_prefix`: Prefix for mounted routes (e.g., "/my-deployment/api").</li></ul> |
> | `webhooks` | *(Added in v0.5.36)* Configuration for outbound webhook delivery. Contains: <ul><li>`env_prefix`: Required prefix for environment variables referenced in header templates (defaults to `LG_WEBHOOK_`).</li><li>`headers`: Static headers to include with webhook requests. Values may contain templates like `${{ env.VAR }}`.</li><li>`url`: URL validation policy with `allowed_domains`, `allowed_ports`, `require_https`, `disable_loopback`, and `max_url_length`.</li></ul> |
> | `api_version` | *(Added in v0.3.7)* Which semantic version of the Agent Server to use (e.g., `"0.3"`). Defaults to latest. Check the server [changelog](Agent%20Server%20changelog.md) for details on each release. |

> [tab] JS
>
> | Key | Description |
> | - | - |
> | `graphs` | **Required**. Mapping from graph ID to path where the compiled graph or a function that makes a graph is defined. Example: <ul><li>`./src/graph.ts:variable`, where `variable` is an instance of [`CompiledStateGraph`](https://reference.langchain.com/python/langgraph/graph/state/CompiledStateGraph)</li><li>`./src/graph.ts:makeGraph`, where `makeGraph` is a function that takes a config dictionary (`LangGraphRunnableConfig`) and returns an instance of [`StateGraph`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph) or [`CompiledStateGraph`](https://reference.langchain.com/python/langgraph/graph/state/CompiledStateGraph). See [how to rebuild a graph at runtime](../../Agent%20Server/Server%20customization/Rebuild%20graph%20at%20runtime.md) for more details.</li></ul> |
> | `env` | Path to `.env` file or a mapping from environment variable to its value. |
> | `store` | Configuration for adding semantic search and/or time-to-live (TTL) to the BaseStore. Contains the following fields: <ul><li>`index` (optional): Configuration for semantic search indexing with fields `embed`, `dims`, and optional `fields`.</li><li>`ttl` (optional): Configuration for item expiration. An object with optional fields: `refresh_on_read` (boolean, defaults to `true`), `default_ttl` (float, lifespan in **minutes**; applied to newly created items only; existing items are unchanged; defaults to no expiration), and `sweep_interval_minutes` (integer, how often to check for expired items, defaults to no sweeping).</li></ul> |
> | `node_version` | Specify `node_version: 20` to use LangGraph.js. |
> | `dockerfile_lines` | Array of additional lines to add to Dockerfile following the import from parent image. |
> | `checkpointer` | Configuration for the checkpointer. Supports: <ul><li>`backend` (optional): `"default"`, `"mongo"`, or `"custom"`. Defaults to `"default"` (PostgreSQL). See [Configure checkpointer backend](../../Agent%20Server/Develop%20your%20application/Persistence/Configure%20checkpointer%20backend.md).</li><li>`path` (optional): Path to a custom checkpointer factory (when `backend` is `"custom"`). See [Custom checkpointer](../../Agent%20Server/Server%20customization/Replace%20built-in%20backends/How%20to%20use%20a%20custom%20checkpointer.md).</li><li>`ttl` (optional): Object with `strategy`, `sweep_interval_minutes`, `default_ttl`, and `sweep_limit` (Agent Server v0.8+) controlling checkpoint expiry.</li><li>`serde` (optional, Agent Server v0.5+): Object with `allowed_json_modules` and `pickle_fallback` to tune deserialization behavior.</li></ul> |
> | `http` | HTTP server configuration mirroring the Python options: <ul><li>`cors` with `allow_origins`, `allow_methods`, `allow_headers`, `allow_credentials`, `allow_origin_regex`, `expose_headers`, `max_age`.</li><li>`configurable_headers` and `logging_headers` pattern lists.</li><li>`middleware_order` (`auth_first` or `middleware_first`).</li><li>`enable_custom_route_auth` plus the same boolean route toggles as above.</li></ul> |
> | `webhooks` | *(Added in v0.5.36)* Configuration for outbound webhook delivery. Contains: <ul><li>`env_prefix`: Required prefix for environment variables referenced in header templates (defaults to `LG_WEBHOOK_`).</li><li>`headers`: Static headers to include with webhook requests. Values may contain templates like `${{ env.VAR }}`.</li><li>`url`: URL validation policy with `allowed_domains`, `allowed_ports`, `require_https`, `disable_loopback`, and `max_url_length`.</li></ul> |
> | `api_version` | *(Added in v0.3.7)* Which semantic version of the LangGraph API server to use (e.g., `"0.3"`). Defaults to latest. Check the server [changelog](Agent%20Server%20changelog.md) for details on each release. |

### Examples

> [tab] Python
>
> #### Basic configuration
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "$schema": "https://langgra.ph/schema.json",
>   "dependencies": ["."],
>   "graphs": {
>     "chat": "chat.graph:graph"
>   }
> }
> ```
>
> #### Install from a uv lockfile
>
> When the project already has a `uv.lock`, set `source.kind` to `"uv"` so image builds install the locked versions. Omit `dependencies` in this mode. The CLI exports requirements with `uv export --frozen` and installs them into the image.
>
> **Single-package project** (`pyproject.toml` and `uv.lock` next to `langgraph.json`):
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "$schema": "https://langgra.ph/schema.json",
>   "python_version": "3.12",
>   "graphs": {
>     "chat": "./src/agent/graph.py:graph"
>   },
>   "source": {
>     "kind": "uv"
>   }
> }
> ```
>
> **uv workspace** (`langgraph.json` inside a member; lockfile at the workspace root):
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "$schema": "https://langgra.ph/schema.json",
>   "python_version": "3.12",
>   "graphs": {
>     "chat": "./src/agent/graph.py:graph"
>   },
>   "source": {
>     "kind": "uv",
>     "root": "../..",
>     "package": "agent"
>   }
> }
> ```
>
> Without `source`, a `"dependencies": ["."]` build re-resolves packages from `pyproject.toml` at image build time and does not use `uv.lock`. Pin versions in `pyproject.toml` or use `source.kind: "uv"` when lockfile reproducibility matters.
>
> #### Using Wolfi base images
>
> You can specify the Linux distribution for your base image using the `image_distro` field. Valid options are `debian`, `wolfi`, `bookworm`, or `bullseye`. Wolfi is the recommended option as it provides smaller and more secure images. This is available in `langgraph-cli>=0.2.11`.
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "$schema": "https://langgra.ph/schema.json",
>   "dependencies": ["."],
>   "graphs": {
>     "chat": "chat.graph:graph"
>   },
>   "image_distro": "wolfi"
> }
> ```
>
> #### Adding semantic search to the store
>
> All Agent Servers come with a DB-backed BaseStore. Adding an "index" configuration to your `langgraph.json` will enable [semantic search](../../Agent%20Server/Develop%20your%20application/Persistence/How%20to%20add%20semantic%20search%20to%20your%20agent%20deployment.md) within the BaseStore of your Agent Server.
>
> The `index.fields` configuration determines which parts of your documents to embed:
>
> * If omitted or set to `["$"]`, the entire document will be embedded
> * To embed specific fields, use JSON path notation: `["metadata.title", "content.text"]`
> * Documents missing specified fields will still be stored but won't have embeddings for those fields
> * You can still override which fields to embed on a specific item at `put` time using the `index` parameter
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "dependencies": ["."],
>   "graphs": {
>     "memory_agent": "./agent/graph.py:graph"
>   },
>   "store": {
>     "index": {
>       "embed": "openai:text-embedding-3-small",
>       "dims": 1536,
>       "fields": ["$"]
>     }
>   }
> }
> ```
>
> > [!NOTE]
> >
> > **Common model dimensions**
> >
> > * `openai:text-embedding-3-large`: 3072
> > * `openai:text-embedding-3-small`: 1536
> > * `openai:text-embedding-ada-002`: 1536
> > * `cohere:embed-english-v3.0`: 1024
> > * `cohere:embed-english-light-v3.0`: 384
> > * `cohere:embed-multilingual-v3.0`: 1024
> > * `cohere:embed-multilingual-light-v3.0`: 384
>
> #### Semantic search with a custom embedding function
>
> If you want to use semantic search with a custom embedding function, you can pass a path to a custom embedding function:
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "dependencies": ["."],
>   "graphs": {
>     "memory_agent": "./agent/graph.py:graph"
>   },
>   "store": {
>     "index": {
>       "embed": "./embeddings.py:embed_texts",
>       "dims": 768,
>       "fields": ["text", "summary"]
>     }
>   }
> }
> ```
>
> The `embed` field in store configuration can reference a custom function that takes a list of strings and returns a list of embeddings. Example implementation:
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # embeddings.py
> def embed_texts(texts: list[str]) -> list[list[float]]:
>     """Custom embedding function for semantic search."""
>     # Implementation using your preferred embedding model
>     return [[0.1, 0.2, ...] for _ in texts]  # dims-dimensional vectors
> ```
>
> #### Adding custom authentication
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "$schema": "https://langgra.ph/schema.json",
>   "dependencies": ["."],
>   "graphs": {
>     "chat": "chat.graph:graph"
>   },
>   "auth": {
>     "path": "./auth.py:auth",
>     "openapi": {
>       "securitySchemes": {
>         "apiKeyAuth": {
>           "type": "apiKey",
>           "in": "header",
>           "name": "X-API-Key"
>         }
>       },
>       "security": [{ "apiKeyAuth": [] }]
>     },
>     "disable_studio_auth": false,
>     "allow_langsmith_api_keys": false
>   }
> }
> ```
>
> See the [authentication conceptual guide](../../Agent%20Server/Auth%20%26%20access%20control/Authentication%20%26%20access%20control.md) for details, and the [setting up custom authentication](../../Agent%20Server/Auth%20%26%20access%20control/Custom%20auth%20tutorial/Set%20up%20custom%20authentication.md) guide for a practical walk through of the process.
>
> #### Configuring store item Time-to-Live
>
> You can configure default data expiration for items/memories in the BaseStore using the `store.ttl` key. This determines how long items are retained after they are last accessed (with reads potentially refreshing the timer based on `refresh_on_read`). Note that these defaults can be overwritten on a per-call basis by modifying the corresponding arguments in `get`, `search`, etc.
>
> The `ttl` configuration is an object containing optional fields:
>
> * `refresh_on_read`: If `true` (the default), accessing an item via `get` or `search` resets its expiration timer. Set to `false` to only refresh TTL on writes (`put`).
> * `default_ttl`: The default lifespan of an item in **minutes**. Applies only to newly created items; existing items are not modified. If not set, items do not expire by default.
> * `sweep_interval_minutes`: How frequently (in minutes) the system should run a background process to delete expired items. If not set, sweeping does not occur automatically.
>
> Here is an example enabling a 7-day TTL (10080 minutes), refreshing on reads, and sweeping every hour:
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "$schema": "https://langgra.ph/schema.json",
>   "dependencies": ["."],
>   "graphs": {
>     "memory_agent": "./agent/graph.py:graph"
>   },
>   "store": {
>     "ttl": {
>       "refresh_on_read": true,
>       "sweep_interval_minutes": 60,
>       "default_ttl": 10080
>     }
>   }
> }
> ```
>
> #### Configuring checkpoint Time-to-Live
>
> You can configure the time-to-live (TTL) for checkpoints using the `checkpointer` key. This determines how long checkpoint data is retained before being automatically handled according to the specified strategy (e.g., deletion). Two optional sub-objects are supported:
>
> * `ttl`: Includes `strategy`, `sweep_interval_minutes`, `default_ttl`, and `sweep_limit` (Agent Server v0.8+), which collectively set how checkpoints expire.
> * `serde` *(Agent Server v0.5+)* : Lets you control deserialization behavior for checkpoint payloads.
>
> Here's an example setting a default TTL of 30 days (43200 minutes):
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "$schema": "https://langgra.ph/schema.json",
>   "dependencies": ["."],
>   "graphs": {
>     "chat": "chat.graph:graph"
>   },
>   "checkpointer": {
>     "ttl": {
>       "strategy": "delete",
>       "sweep_interval_minutes": 10,
>       "default_ttl": 43200
>     }
>   }
> }
> ```
>
> In this example, checkpoints older than 30 days will be deleted, and the check runs every 10 minutes.
>
> #### Configuring checkpointer serde
>
> The `checkpointer.serde` object shapes deserialization:
>
> * `allowed_json_modules` defines an allow list for custom Python objects you want the server to be able to deserialize from payloads saved in "json" mode. This is a list of `[path, to, module, file, symbol]` sequences. If omitted, only LangChain-safe defaults are allowed. You can unsafely set to `true` to allow any module to be deserialized.
> * `pickle_fallback`: Whether to fall back to pickle deserialization when JSON decoding fails.
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "checkpointer": {
>     "serde": {
>       "allowed_json_modules": [
>         ["my_agent", "auth", "SessionState"]
>       ]
>     }
>   }
> }
> ```
>
> #### Customizing HTTP middleware and headers
>
> The `http` block lets you fine-tune request handling:
>
> * `middleware_order`: Choose `"auth_first"` to run authentication before your middleware, or `"middleware_first"` (default) to invert that order.
> * `enable_custom_route_auth`: Extend authentication to routes you mount through `http.app`.
> * `configurable_headers` / `logging_headers`: Each accepts an object with optional `includes` and `excludes` arrays; wildcards are supported and exclusions run before inclusions.
> * `cors`: Customize your server's CORS (Cross-Origin Resource Sharing) configuration. Example `langgraph.json` file for configuring CORS:
>
>   ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
>   {
>     ...
>     "http": {
>       "cors": {
>         "allow_origins": ["https://example.com", "https://app.example.com"],
>         "allow_methods": ["GET", "POST"],
>         "allow_headers": ["Authorization", "Content-Type"],
>         "allow_credentials": true,
>         "allow_origin_regex": "^https://.*\\.example\\.com$",
>         "expose_headers": ["x-pagination-total", "x-pagination-next", "x-request-id"],
>         "max_age": 600
>       }
>     },
>     ...
>   }
>   ```
>
>   > [!NOTE]
>   >
>   > Customizing your server's CORS configuration will override the functionality of setting the [`CORS_ALLOW_ORIGINS` environment variable](../../Deploy%20to%20Cloud/Reference/Cloud%20Agent%20Server%20environment%20variables.md).
>
> #### Configuring webhooks
>
> You can configure custom headers and URL restrictions for outbound webhook requests:
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "$schema": "https://langgra.ph/schema.json",
>   "dependencies": ["."],
>   "graphs": {
>     "chat": "chat.graph:graph"
>   },
>   "webhooks": {
>     "headers": {
>       "Authorization": "Bearer ${{ env.LG_WEBHOOK_TOKEN }}"
>     },
>     "url": {
>       "allowed_domains": ["*.mycompany.com"],
>       "require_https": true
>     }
>   }
> }
> ```
>
> See [Use webhooks](../../Agent%20Server/Capabilities/Use%20webhooks.md#add-headers-to-webhook-requests) for details on header configuration, environment variable templating, and URL restrictions.
>
> #### Pinning API version
>
> *(Added in v0.3.7)*
>
> You can pin the API version of the Agent Server by using the `api_version` key. This is useful if you want to ensure that your server uses a specific version of the API.
> By default, builds for Agent Servers on Cloud use the latest stable version of the server. This can be pinned by setting the `api_version` key to a specific version.
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "$schema": "https://langgra.ph/schema.json",
>   "dependencies": ["."],
>   "graphs": {
>     "chat": "chat.graph:graph"
>   },
>   "api_version": "0.2"
> }
> ```
>
> #### Disabling built-in routes
>
> You can selectively disable groups of built-in HTTP routes using boolean flags in the `http` configuration block. This is useful for production Agent Servers where you want to minimize the server's exposed surface area.
>
> For example, to disable the system information and documentation routes:
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "$schema": "https://langgra.ph/schema.json",
>   "dependencies": ["."],
>   "graphs": {
>     "chat": "chat.graph:graph"
>   },
>   "http": {
>     "disable_meta": true
>   }
> }
> ```
>
> Setting `disable_meta` to `true` disables the following routes:
>
> * `/` — root health check
> * `/info` — server version and configuration info
> * `/metrics` — Prometheus and JSON metrics
> * `/docs` — API documentation UI
> * `/openapi.json` — OpenAPI specification
>
> The `/ok` health check endpoint remains available even when `disable_meta` is set, so orchestrators like Kubernetes can still perform liveness and readiness probes.
>
> Other route disable flags include `disable_assistants`, `disable_runs`, `disable_threads`, `disable_store`, and `disable_ui`. For MCP, A2A, and webhooks, see their respective guides: [Disable MCP](../../Agent%20Server/Capabilities/MCP%20endpoint%20in%20Agent%20Server.md#disable-mcp), [Disable A2A](../../Agent%20Server/Capabilities/A2A%20endpoint%20in%20Agent%20Server.md#disable-a2a), [Disable webhooks](../../Agent%20Server/Capabilities/Use%20webhooks.md#disable-webhooks).

> [tab] JS
>
> #### Basic configuration
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "$schema": "https://langgra.ph/schema.json",
>   "graphs": {
>     "chat": "./src/graph.ts:graph"
>   }
> }
> ```
>
> #### Pinning API version
>
> *(Added in v0.3.7)*
>
> You can pin the API version of the Agent Server by using the `api_version` key. This is useful if you want to ensure that your server uses a specific version of the API.
> By default, builds for Agent Servers on Cloud use the latest stable version of the server. This can be pinned by setting the `api_version` key to a specific version.
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "$schema": "https://langgra.ph/schema.json",
>   "dependencies": ["."],
>   "graphs": {
>     "chat": "./src/chat/graph.ts:graph"
>   },
>   "api_version": "0.2"
> }
> ```
>
> #### Disabling built-in routes
>
> You can selectively disable groups of built-in HTTP routes using boolean flags in the `http` configuration block. This is useful for production Agent Servers where you want to minimize the server's exposed surface area.
>
> For example, to disable the system information and documentation routes:
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "$schema": "https://langgra.ph/schema.json",
>   "graphs": {
>     "chat": "./src/chat/graph.ts:graph"
>   },
>   "http": {
>     "disable_meta": true
>   }
> }
> ```
>
> Setting `disable_meta` to `true` disables the following routes:
>
> * `/` — root health check
> * `/info` — server version and configuration info
> * `/metrics` — Prometheus and JSON metrics
> * `/docs` — API documentation UI
> * `/openapi.json` — OpenAPI specification
>
> The `/ok` health check endpoint remains available even when `disable_meta` is set, so orchestrators like Kubernetes can still perform liveness and readiness probes.
>
> Other route disable flags include `disable_assistants`, `disable_runs`, `disable_threads`, `disable_store`, and `disable_ui`. For MCP, A2A, and webhooks, see their respective guides: [Disable MCP](../../Agent%20Server/Capabilities/MCP%20endpoint%20in%20Agent%20Server.md#disable-mcp), [Disable A2A](../../Agent%20Server/Capabilities/A2A%20endpoint%20in%20Agent%20Server.md#disable-a2a), [Disable webhooks](../../Agent%20Server/Capabilities/Use%20webhooks.md#disable-webhooks).

## Commands

**Usage**

> [tab] Python
>
> The base command for the LangGraph CLI is `langgraph`.
>
> ```
> langgraph [OPTIONS] COMMAND [ARGS]
> ```

> [tab] JS
>
> The base command for the LangGraph.js CLI is `langgraphjs`.
>
> ```
> npx @langchain/langgraph-cli [OPTIONS] COMMAND [ARGS]
> ```
>
> We recommend using `npx` to always use the latest version of the CLI.

### `dev`

> [tab] Python
>
> Run Agent Server in development mode with hot reloading and debugging capabilities. This lightweight server requires no Docker installation and is suitable for development and testing. State is persisted to a local directory.
>
> > [!NOTE]
> >
> > Currently, the CLI only supports Python 3.11 or later
>
> > [!TIP]
> >
> > If you need more information on when to use `langgraph dev` vs `langgraph up`, refer to the [Local development & testing guide](../Develop%20%26%20test/Local%20development%20%26%20testing.md) for a detailed comparison.
>
> **Installation**
>
> This command requires the "inmem" extra to be installed:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> pip install -U "langgraph-cli[inmem]"
> ```
>
> **Usage**
>
> ```
> langgraph dev [OPTIONS]
> ```
>
> **Options**
>
> | Option | Default | Description |
> | - | - | - |
> | `-c, --config FILE` | `langgraph.json` | Path to configuration file declaring dependencies, graphs and environment variables |
> | `--host TEXT` | `127.0.0.1` | Host to bind the server to |
> | `--port INTEGER` | `2024` | Port to bind the server to |
> | `--no-reload` | | Disable auto-reload |
> | `--n-jobs-per-worker INTEGER` | `1` | Maximum number of concurrent jobs per worker |
> | `--debug-port INTEGER` | | Port for debugger to listen on |
> | `--wait-for-client` | `False` | Wait for a debugger client to connect to the debug port before starting the server |
> | `--no-browser` | | Skip automatically opening the browser when the server starts |
> | `--studio-url TEXT` | | URL of the Studio instance to connect to. Defaults to [https://smith.langchain.com](https://smith.langchain.com) |
> | `--allow-blocking` | `False` | Do not raise errors for synchronous I/O blocking operations in your code (added in `0.2.6`) |
> | `--tunnel` | `False` | Expose the local server via a public tunnel (Cloudflare) for remote frontend access. This avoids issues with browsers like Safari or networks blocking localhost connections |
> | `--help` | | Display command documentation |

> [tab] JS
>
> Run LangGraph API server in development mode with hot reloading capabilities. This lightweight server requires no Docker installation and is suitable for development and testing. State is persisted to a local directory.
>
> **Usage**
>
> ```
> npx @langchain/langgraph-cli dev [OPTIONS]
> ```
>
> **Options**
>
> | Option | Default | Description |
> | - | - | - |
> | `-c, --config FILE` | `langgraph.json` | Path to configuration file declaring dependencies, graphs and environment variables |
> | `--host TEXT` | `127.0.0.1` | Host to bind the server to |
> | `--port INTEGER` | `2024` | Port to bind the server to |
> | `--no-reload` | | Disable auto-reload |
> | `--n-jobs-per-worker INTEGER` | | Number of jobs per worker. Default is 10 |
> | `--debug-port INTEGER` | | Port for debugger to listen on |
> | `--wait-for-client` | `False` | Wait for a debugger client to connect to the debug port before starting the server |
> | `--no-browser` | | Skip automatically opening the browser when the server starts |
> | `--studio-url TEXT` | | URL of the Studio instance to connect to. Defaults to [https://smith.langchain.com](https://smith.langchain.com) |
> | `--allow-blocking` | `False` | Do not raise errors for synchronous I/O blocking operations in your code |
> | `--tunnel` | `False` | Expose the local server via a public tunnel (Cloudflare) for remote frontend access. This avoids issues with browsers or networks blocking localhost connections |
> | `--help` | | Display command documentation |

### `build`

> [tab] Python
>
> Build Agent Server Docker image.
>
> **Usage**
>
> ```
> langgraph build [OPTIONS]
> ```
>
> **Options**
>
> | Option | Default | Description |
> | - | - | - |
> | `--platform TEXT` | | Target platform(s) to build the Docker image for. Example: `langgraph build --platform linux/amd64,linux/arm64` |
> | `-t, --tag TEXT` | | **Required**. Tag for the Docker image. Example: `langgraph build -t my-image` |
> | `--pull / --no-pull` | `--pull` | Build with latest remote Docker image. Use `--no-pull` for running the Agent Server with locally built images. |
> | `-c, --config FILE` | `langgraph.json` | Path to configuration file declaring dependencies, graphs and environment variables. |
> | `--build-command TEXT`<sup>\*</sup> | | Build command to run. Runs from the directory where your `langgraph.json` file lives. Example: `langgraph build --build-command "yarn run turbo build"` |
> | `--install-command TEXT`<sup>\*</sup> | | Install command to run. Runs from the directory where you call `langgraph build` from. Example: `langgraph build --install-command "yarn install"` |
> | `--help` | | Display command documentation. |
>
> <sup>\*</sup>Only supported for JS Agent Servers, will have no impact on Python Agent Servers.

> [tab] JS
>
> Build Agent Server Docker image.
>
> **Usage**
>
> ```
> npx @langchain/langgraph-cli build [OPTIONS]
> ```
>
> **Options**
>
> | Option | Default | Description |
> | - | - | - |
> | `--platform TEXT` | | Target platform(s) to build the Docker image for. Example: `langgraph build --platform linux/amd64,linux/arm64` |
> | `-t, --tag TEXT` | | **Required**. Tag for the Docker image. Example: `langgraph build -t my-image` |
> | `--no-pull` | | Use locally built images. Defaults to `false` to build with latest remote Docker image. |
> | `-c, --config FILE` | `langgraph.json` | Path to configuration file declaring dependencies, graphs and environment variables. |
> | `--help` | | Display command documentation. |

### `deploy`

> [tab] Python
>
> > [!NOTE]
> >
> > This command is in [beta](../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md) and under active development. Expect frequent updates and improvements. On LangSmith Cloud (SaaS) in AWS, local builds require `langgraph-cli` 0.4.35 or later.
>
> Build and deploy a LangGraph image directly to [LangSmith Agent Server](../LangSmith%20Agent%20Server.md). This command builds a Docker image locally, pushes it to a managed registry, and creates or updates an Agent Server—all in a single step. If Docker is not installed, it triggers a remote build.
>
> **Prerequisites**
>
> * A [**LangSmith API key**](../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md) with access to LangSmith Agent Server.
>
> * (Optional) **Docker** must be installed and the Docker daemon must be running for local builds. Not required for remote builds. [Install Docker Desktop](https://docs.docker.com/get-docker/).
>
> > [!NOTE]
> >
> > On LangSmith Cloud, the CLI pushes to a managed registry. Self-hosted LangSmith, and Cloud workspaces that deploy through a [listener](../Deployment%20components/LangSmith%20control%20plane.md#listeners) in your own cluster, push to a registry you manage with `--push-to`. See [Deploy from a registry you manage](#deploy-from-a-registry-you-manage).
>
> **Usage**
>
> ```
> langgraph deploy [OPTIONS] [DOCKER_BUILD_ARGS]
> ```
>
> This command also accepts all [`langgraph build`](#build) flags (`--platform`, `-t`, `--pull`, `--no-pull`, `-c`). For details, refer to `langgraph build --help`.
>
> **Options**
>
> | Option | Default | Description |
> | - | - | - |
> | `--api-key TEXT` | | API key. Can also be set via `LANGGRAPH_HOST_API_KEY`, `LANGSMITH_API_KEY`, or `LANGCHAIN_API_KEY` environment variable or `.env` file. |
> | `--name TEXT` | Current directory name | Agent Server name. Can also be set via `LANGSMITH_DEPLOYMENT_NAME` environment variable or `.env` file. |
> | `--agent-server-id TEXT` | | ID of an existing Agent Server to update. If omitted, `--name` is used to find or create the Agent Server. |
> | `--agent-id TEXT` | | Agent to deploy to in an agent-based workspace, by identifier. Requires `--agent-environment`, and cannot be combined with `--name` or `--agent-server-id`. Can also be set via `LANGSMITH_AGENT_ID`. See [Deploy to an agent environment](../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Deploy%20to%20an%20agent%20environment.md). Available in `langgraph-cli>=0.4.32`. |
> | `--agent-environment TEXT` | | Environment the Agent Server reports into: `development`, `staging`, or `production`. Requires `--agent-id`. Can also be set via `LANGSMITH_AGENT_ENVIRONMENT`. Available in `langgraph-cli>=0.4.32`. |
> | `--agent-server-type TEXT` | `serverless` | Agent Server type when creating a new Agent Server on Cloud. Pass `dedicated` for always-on capacity. Legacy `dev` and `prod` are also accepted. |
> | `--remote / --no-remote` | | Force remote or local build. By default, builds remotely if Docker is not available locally. |
> | `--push-to TEXT` | | Push the image to this repository in a registry you manage (for example `123456789.dkr.ecr.us-east-1.amazonaws.com/agents/my-agent`), then deploy from it. Required for self-hosted LangSmith and for workspaces that deploy through a listener, unless you use `--image-uri` instead. Uses your existing Docker credentials. Give the tag in the value or with `-t`. Cannot be combined with `--remote` or `--image-uri`. |
> | `--image TEXT` | | Use an existing local image (for example `my-agent:dev`) instead of building. The image must target `linux/amd64`. With `--push-to`, the image is retagged and pushed. |
> | `-t, --tag TEXT` | `latest` | Tag for the pushed image. |
> | `--image-uri TEXT` | | Deploy an image that's already in a registry you manage (for example `123456789.dkr.ecr.us-east-1.amazonaws.com/agents/my-agent@sha256:<digest>`), with no build, retag, or push. For self-hosted LangSmith and for workspaces that deploy through a listener. Must include a digest; a mutable tag is rejected, since Kubernetes can cache images by tag and would silently keep running the previous one. Cannot be combined with `--push-to`, `--image`, `-t`, or `--remote`. |
> | `--listener-id TEXT` | | Listener that will run the Agent Server, for workspaces that deploy through a listener in your own cluster. Used only when creating an Agent Server with `--push-to` or `--image-uri`. On LangSmith Cloud, defaults to the workspace's only listener. |
> | `--k8s-namespace TEXT` | | Kubernetes namespace the listener deploys into. Used only when creating an Agent Server with `--push-to` or `--image-uri`. Defaults to the listener's only namespace. |
> | `--image-pull-secret TEXT` | | Name of a Kubernetes secret (type `kubernetes.io/dockerconfigjson`) in the Agent Server's namespace to use for pulling the image from a private registry. Repeat to give more than one. Only used when creating an Agent Server with `--push-to` or `--image-uri`. |
> | `--no-wait` | `False` | Skip waiting for deployment status after pushing. |
> | `--verbose` | `False` | Show detailed output including Docker build and push logs. |
> | `--help` | | Display command documentation. |
>
> > [!NOTE]
> >
> > The Python CLI uses `--agent-server-id` and `--agent-server-type`. It also accepts `--deployment-id` and `--deployment-type` as hidden compatibility aliases. If your installed version does not recognize the Agent Server flags, use the legacy spellings or upgrade. Check `langgraph deploy --help` for the flags your version supports.
> >
> > `langgraph deploy` creates a Serverless Agent Server by default (`langgraph-cli>=0.4.37`; earlier versions default to the legacy `dev` type). This version requirement describes the default type, not the availability of the Agent Server flag names. To create a Dedicated Agent Server, pass `--agent-server-type dedicated`. If your CLI only accepts `dev` and `prod`, upgrade it to use the `serverless` and `dedicated` values.
>
> **Example**
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Deploy with API key from .env file
> langgraph deploy
>
> # Deploy with inline API key
> LANGSMITH_API_KEY=lsv2_... langgraph deploy
>
> # Create a Dedicated deployment
> langgraph deploy --agent-server-type dedicated
>
> # Update an existing deployment
> langgraph deploy --agent-server-id abc123
>
> # Deploy with inline deployment name
> LANGSMITH_DEPLOYMENT_NAME=my-agent langgraph deploy
>
> # Deploy to EU region
> LANGGRAPH_HOST_URL=https://eu.api.host.langchain.com langgraph deploy
> ```
>
> > [!NOTE]
> >
> > CLI updates depend on the Agent Server's source and the selected build mode. Local builds pushed to the managed registry require an `internal_docker` source. To update an Agent Server from a registry you manage, use `--push-to` or `--image-uri`. Do not assume every Agent Server created through the UI or GitHub integration supports every CLI build mode.
>
> #### Deploy from a registry you manage
>
> Self-hosted LangSmith, and LangSmith Cloud workspaces that deploy through a listener in your own cluster (the [legacy hybrid model](../../../LangSmith%20setup/Self-hosted/Hybrid/Setup%20guide%20%28legacy%29.md)), run images from a registry you manage. Pass `--push-to` with a repository in that registry. The CLI builds the image, pushes it with your existing Docker credentials, and creates or updates the Agent Server from the pushed image.
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Log in to your registry first, for example with AWS ECR
> aws ecr get-login-password | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com
>
> # Self-hosted: point the CLI at your LangSmith instance
> LANGSMITH_ENDPOINT=https://langsmith.example.com/api \
> langgraph deploy --push-to 123456789.dkr.ecr.us-east-1.amazonaws.com/agents/my-agent
>
> # LangSmith Cloud workspace with a listener: only the image location changes
> langgraph deploy --push-to 123456789.dkr.ecr.us-east-1.amazonaws.com/agents/my-agent --tag v1.2.0
>
> # Push an image you already built
> langgraph deploy --image my-agent:dev --push-to 123456789.dkr.ecr.us-east-1.amazonaws.com/agents/my-agent
> ```
>
> The control plane URL is derived from `LANGSMITH_ENDPOINT`, read from the project `.env` file or the environment: `https://<host>/api-host` for a self-hosted instance, and the matching LangSmith Cloud control plane for cloud endpoints. To override it, set the `LANGGRAPH_HOST_URL` environment variable to the full control plane URL, including `/api-host` on a self-hosted instance (for example `https://langsmith.example.com/api-host`).
>
> #### Deploy an image you've already pushed
>
> If your CI/CD pipeline builds and pushes the image in a separate job from the one that deploys, `--push-to` does not work: it always builds (or retags a local `--image`) and pushes, and `--image` requires the image to be present in the local Docker daemon. Use `--image-uri` instead to deploy an image that's already in a registry, with no build, retag, or push at all:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> langgraph deploy --image-uri 123456789.dkr.ecr.us-east-1.amazonaws.com/agents/my-agent@sha256:1a2b3c4d...
> ```
>
> `--image-uri` must include a digest (`@sha256:<digest>`), not a mutable tag. Kubernetes can cache images by tag, so redeploying the same tag could silently keep running the previous image. If your pipeline already captures the digest from its push step, pass it straight through; otherwise resolve it first, for example with `docker buildx imagetools inspect <repository>:<tag> --format '{{json .Manifest.Digest}}'` or your registry's own CLI.
>
> Agent Servers created with `--image-uri` use the same `external_docker` source as `--push-to`, so either option can update an Agent Server the other one created.
>
> #### Choose a listener and namespace
>
> When a workspace deploys through a listener, the control plane needs to know which listener runs a new Agent Server and which Kubernetes namespace it deploys into.
>
> On LangSmith Cloud, you do not have to pass either when there is only one possible answer. If your workspace has a single listener that serves a single namespace, the CLI uses it:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> langgraph deploy --push-to 123456789.dkr.ecr.us-east-1.amazonaws.com/agents/my-agent
> ```
>
> When there is a choice, the CLI lists the listeners with their clusters and namespaces, and you pick one:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> langgraph deploy --push-to 123456789.dkr.ecr.us-east-1.amazonaws.com/agents/my-agent \
>   --listener-id 2b1f0e9c-2d4a-4f1e-9a3b-2c7d8e5f4a10 --k8s-namespace agents
> ```
>
> On a self-hosted instance, the CLI looks up listeners only when you pass `--listener-id` or `--k8s-namespace`. To find a listener's id and namespaces ahead of time, for example to pass `--listener-id` from a script without hardcoding it, use [`deploy listeners list`](#deploy-listeners-list) with `--json`:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> listener_id=$(langgraph deploy listeners list --json | jq -r '.[0].id')
> langgraph deploy --push-to 123456789.dkr.ecr.us-east-1.amazonaws.com/agents/my-agent \
>   --listener-id "$listener_id" --k8s-namespace agents
> ```
>
> The listener and the namespace are fixed when the Agent Server is created and cannot be changed afterward, so both options are refused on an existing Agent Server. Later revisions need only `--push-to`.
>
> Agent Servers created with `--push-to` use the `external_docker` source. An Agent Server created without `--push-to` cannot be switched to it; use a new `--name` instead.
>
> #### Authenticate to a private registry
>
> If the registry you push to with `--push-to` or deploy from with `--image-uri` requires authentication to pull the image, the cluster needs a Kubernetes secret of type `kubernetes.io/dockerconfigjson` in the Agent Server's namespace. Create it ahead of time (for example with `kubectl create secret docker-registry`), then pass its name with `--image-pull-secret`:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> langgraph deploy --push-to 123456789.dkr.ecr.us-east-1.amazonaws.com/agents/my-agent \
>   --image-pull-secret regcred
> ```
>
> Repeat `--image-pull-secret` to attach more than one secret. Like the listener and namespace, image pull secrets are fixed when the Agent Server is created; the CLI doesn't support changing them on an existing Agent Server, but you can update the Agent Server's `resource_spec` through the API or the LangSmith UI.
>
> #### `deploy list`
>
> List Agent Servers.
>
> **Usage**
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> langgraph deploy list [OPTIONS]
> ```
>
> **Options**
>
> | Option | Default | Description |
> | - | - | - |
> | `--name-contains TEXT` | | Only show Agent Servers whose names contain this value. |
> | `--api-key TEXT` | | API key. Can also be set via `LANGGRAPH_HOST_API_KEY`, `LANGSMITH_API_KEY`, or `LANGCHAIN_API_KEY` environment variable or `.env` file. |
> | `--help` | | Show this message and exit. |
>
> #### `deploy listeners`
>
> \[Beta] Inspect listeners available to this workspace.
>
> **Usage**
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> langgraph deploy listeners [OPTIONS] COMMAND [ARGS]...
> ```
>
> **Options**
>
> | Option | Default | Description |
> | - | - | - |
> | `--help` | | Show this message and exit. |
>
> **Commands**
>
> | Command | Description |
> | - | - |
> | `list` | \[Beta] List listeners available to this workspace. |
>
> #### `deploy listeners list`
>
> \[Beta] List listeners available to this workspace, with their cluster (`compute_id`) and Kubernetes namespaces.
>
> Pass a listener's id to `langgraph deploy --listener-id` to deploy through it. See [Choose a listener and namespace](#choose-a-listener-and-namespace).
>
> Pass `--json` to get the listeners as a JSON array instead of a table, for scripting (for example, to pipe a listener's id into `--listener-id`).
>
> **Usage**
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> langgraph deploy listeners list [OPTIONS]
> ```
>
> **Options**
>
> | Option | Default | Description |
> | - | - | - |
> | `--json` | | Emit the listeners as a JSON array instead of a table. |
> | `--api-key TEXT` | | API key. Can also be set via `LANGGRAPH_HOST_API_KEY`, `LANGSMITH_API_KEY`, or `LANGCHAIN_API_KEY` environment variable or `.env` file. |
> | `--help` | | Show this message and exit. |
>
> #### `deploy revisions`
>
> \[Beta] Manage Agent Server revisions.
>
> **Usage**
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> langgraph deploy revisions [OPTIONS] COMMAND [ARGS]...
> ```
>
> **Options**
>
> | Option | Default | Description |
> | - | - | - |
> | `--help` | | Show this message and exit. |
>
> **Commands**
>
> | Command | Description |
> | - | - |
> | `list` | \[Beta] List revisions for an Agent Server. |
>
> #### `deploy revisions list`
>
> \[Beta] List revisions for an Agent Server.
>
> Use [`deploy list`](#deploy-list) to list Agent Server IDs.
>
> **Usage**
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> langgraph deploy revisions list [OPTIONS] AGENT_SERVER_ID
> ```
>
> **Options**
>
> | Option | Default | Description |
> | - | - | - |
> | `--limit INTEGER` | `10` | Maximum number of revisions to return. |
> | `--api-key TEXT` | | API key. Can also be set via `LANGGRAPH_HOST_API_KEY`, `LANGSMITH_API_KEY`, or `LANGCHAIN_API_KEY` environment variable or `.env` file. |
> | `--help` | | Show this message and exit. |
>
> #### `deploy delete`
>
> Delete an Agent Server.
>
> Use [`deploy list`](#deploy-list) to find the Agent Server ID to delete.
>
> **Usage**
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> langgraph deploy delete [OPTIONS] AGENT_SERVER_ID
> ```
>
> **Options**
>
> | Option | Default | Description |
> | - | - | - |
> | `--force` | | Delete without prompting for confirmation. |
> | `--api-key TEXT` | | API key. Can also be set via `LANGGRAPH_HOST_API_KEY`, `LANGSMITH_API_KEY`, or `LANGCHAIN_API_KEY` environment variable or `.env` file. |
> | `--help` | | Show this message and exit. |
>
> #### `deploy logs`
>
> Fetch Agent Server logs. Use `deploy` for Agent Server runtime logs, or `build` for remote build logs.
>
> **Usage**
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> langgraph deploy logs [OPTIONS]
> ```
>
> **Options**
>
> | Option | Default | Description |
> | - | - | - |
> | `-f, --follow` | `False` | Continuously poll for new logs. |
> | `--end-time TEXT` | | ISO8601 end time. Example: `2026-03-08T00:00:00Z`. |
> | `--start-time TEXT` | | ISO8601 start time. Example: `2026-03-08T00:00:00Z`. |
> | `-q, --query TEXT` | | Search string filter. |
> | `--limit INTEGER` | `100` | Max log entries to fetch. |
> | `--level [DEBUG\|INFO\|WARNING\|ERROR\|CRITICAL]` | | Filter by log level. |
> | `--revision-id TEXT` | | Specific revision ID. For build logs, defaults to the latest revision. |
> | `--type [deploy\|build]` | `deploy` | Log stream to fetch. `deploy` shows Agent Server runtime logs. `build` shows remote build logs. |
> | `--agent-server-id TEXT` | | Agent Server ID. If omitted, `--name` is used to find the Agent Server. |
> | `--name TEXT` | Current directory name | Agent Server name. Can also be set via `LANGSMITH_DEPLOYMENT_NAME` environment variable or `.env` file. Used when `--agent-server-id` is not provided. |
> | `--api-key TEXT` | | API key. Can also be set via `LANGGRAPH_HOST_API_KEY`, `LANGSMITH_API_KEY`, or `LANGCHAIN_API_KEY` environment variable or `.env` file. |
> | `--help` | | Show this message and exit. |

### `up`

> [tab] Python
>
> Start Agent Server. For local testing, requires a LangSmith API key with access to LangSmith. Requires a license key for production use.
>
> > [!TIP]
> >
> > If you need more information on when to use `langgraph dev` vs `langgraph up`, refer to the [Local development & testing guide](../Develop%20%26%20test/Local%20development%20%26%20testing.md) for a detailed comparison.
>
> **Usage**
>
> ```
> langgraph up [OPTIONS]
> ```
>
> **Options**
>
> | Option | Default | Description |
> | - | - | - |
> | `--wait` | | Wait for services to start before returning. Implies --detach |
> | `--base-image TEXT` | `langchain/langgraph-api` | Base image to use for the Agent Server. Pin to specific versions using version tags. |
> | `--image TEXT` | | Docker image to use for the langgraph-api service. If specified, skips building and uses this image directly. |
> | `--postgres-uri TEXT` | Local database | Postgres URI to use for the database. |
> | `--watch` | | Restart on file changes |
> | `--debugger-base-url TEXT` | `http://127.0.0.1:[PORT]` | URL used by the debugger to access LangGraph API. |
> | `--debugger-port INTEGER` | | Pull the debugger image locally and serve the UI on specified port |
> | `--verbose` | | Show more output from the server logs. |
> | `-c, --config FILE` | `langgraph.json` | Path to configuration file declaring dependencies, graphs and environment variables. |
> | `-d, --docker-compose FILE` | | Path to docker-compose.yml file with additional services to launch. |
> | `-p, --port INTEGER` | `8123` | Port to expose. Example: `langgraph up --port 8000` |
> | `--pull / --no-pull` | `pull` | Pull latest images. Use `--no-pull` for running the server with locally-built images. Example: `langgraph up --no-pull` |
> | `--recreate / --no-recreate` | `no-recreate` | Recreate containers even if their configuration and image haven't changed |
> | `--help` | | Display command documentation. |

> [tab] JS
>
> Start LangGraph API server. For local testing, requires a LangSmith API key with access to LangSmith. Requires a license key for production use.
>
> **Usage**
>
> ```
> npx @langchain/langgraph-cli up [OPTIONS]
> ```
>
> **Options**
>
> | Option | Default | Description |
> | - | - | - |
> | `--wait` | | Wait for services to start before returning. Implies --detach |
> | `--base-image TEXT` | `langchain/langgraph-api` | Base image to use for the LangGraph API server. Pin to specific versions using version tags. |
> | `--image TEXT` | | Docker image to use for the langgraph-api service. If specified, skips building and uses this image directly. |
> | `--postgres-uri TEXT` | Local database | Postgres URI to use for the database. |
> | `--watch` | | Restart on file changes |
> | `-c, --config FILE` | `langgraph.json` | Path to configuration file declaring dependencies, graphs and environment variables. |
> | `-d, --docker-compose FILE` | | Path to docker-compose.yml file with additional services to launch. |
> | `-p, --port INTEGER` | `8123` | Port to expose. Example: `langgraph up --port 8000` |
> | `--no-pull` | | Use locally built images. Defaults to `false` to build with latest remote Docker image. |
> | `--recreate` | | Recreate containers even if their configuration and image haven't changed |
> | `--help` | | Display command documentation. |

### `dockerfile`

> [tab] Python
>
> Generate a Dockerfile for building an Agent Server Docker image.
>
> **Usage**
>
> ```
> langgraph dockerfile [OPTIONS] SAVE_PATH
> ```
>
> **Options**
>
> | Option | Default | Description |
> | - | - | - |
> | `-c, --config FILE` | `langgraph.json` | Path to the [configuration file](#configuration-file) declaring dependencies, graphs and environment variables. |
> | `--help` | | Show this message and exit. |
>
> Example:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> langgraph dockerfile -c langgraph.json Dockerfile
> ```
>
> This generates a Dockerfile that looks similar to:
>
> ```dockerfile theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> FROM langchain/langgraph-api:3.11
>
> ADD ./pipconf.txt /pipconfig.txt
>
> RUN PIP_CONFIG_FILE=/pipconfig.txt PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -c /api/constraints.txt langchain_anthropic langchain_openai wikipedia scikit-learn
>
> ADD ./graphs /deps/__outer_graphs/src
> RUN set -ex && \
>     for line in '[project]' \
>                 'name = "graphs"' \
>                 'version = "0.1"' \
>                 '[tool.setuptools.package-data]' \
>                 '"*" = ["**/*"]'; do \
>         echo "$line" >> /deps/__outer_graphs/pyproject.toml; \
>     done
>
> RUN PIP_CONFIG_FILE=/pipconfig.txt PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -c /api/constraints.txt -e /deps/*
>
> ENV LANGSERVE_GRAPHS='{"agent": "/deps/__outer_graphs/src/agent.py:graph", "storm": "/deps/__outer_graphs/src/storm.py:graph"}'
> ```
>
> > [!NOTE]
> >
> > The `langgraph dockerfile` command translates all the configuration in your `langgraph.json` file into Dockerfile commands. When using this command, you will have to re-run it whenever you update your `langgraph.json` file. Otherwise, your changes will not be reflected when you build or run the dockerfile.

> [tab] JS
>
> Generate a Dockerfile for building an Agent Server Docker image.
>
> **Usage**
>
> ```
> npx @langchain/langgraph-cli dockerfile [OPTIONS] SAVE_PATH
> ```
>
> **Options**
>
> | Option | Default | Description |
> | - | - | - |
> | `-c, --config FILE` | `langgraph.json` | Path to the [configuration file](#configuration-file) declaring dependencies, graphs and environment variables. |
> | `--help` | | Show this message and exit. |
>
> Example:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> npx @langchain/langgraph-cli dockerfile -c langgraph.json Dockerfile
> ```
>
> This generates a Dockerfile that looks similar to:
>
> ```dockerfile theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> FROM langchain/langgraphjs-api:20
>
> ADD . /deps/agent
>
> RUN cd /deps/agent && yarn install
>
> ENV LANGSERVE_GRAPHS='{"agent":"./src/react_agent/graph.ts:graph"}'
>
> WORKDIR /deps/agent
>
> RUN (test ! -f /api/langgraph_api/js/build.mts && echo "Prebuild script not found, skipping") || tsx /api/langgraph_api/js/build.mts
> ```
>
> > [!NOTE]
> >
> > The `npx @langchain/langgraph-cli dockerfile` command translates all the configuration in your `langgraph.json` file into Dockerfile commands. When using this command, you will have to re-run it whenever you update your `langgraph.json` file. Otherwise, your changes will not be reflected when you build or run the dockerfile.
