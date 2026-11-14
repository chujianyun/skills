# Monorepo support

LangSmith supports deploying agents from monorepo setups where your agent code may depend on shared packages located elsewhere in the repository. This guide shows how to structure your monorepo and configure your `langgraph.json` file to work with shared dependencies.

## Repository structure

For complete working examples, see:

* [Python monorepo example](https://github.com/langchain-ai/python-langraph-monorepo-example)
* [JS monorepo example](https://github.com/langchain-ai/js-langgraph-monorepo-example)

```plaintext Python
my-monorepo/
├── shared-utils/           # Shared Python package
│   ├── __init__.py
│   ├── common.py
│   └── pyproject.toml      # Or setup.py
├── agents/
│   └── customer-support/   # Agent directory
│       ├── agent/
│       │   ├── __init__.py
│       │   └── graph.py
│       ├── langgraph.json  # Config file in agent directory
│       ├── .env
│       └── pyproject.toml  # Agent dependencies
└── other-service/
    └── ...
```

```plaintext JS
my-monorepo/
├── package.json            # Root package.json with workspaces
├── shared-utils/           # Shared TypeScript package
│   ├── package.json
│   ├── src/
│   │   └── index.ts
│   └── tsconfig.json
├── agents/
│   └── customer-support/   # Agent directory
│       ├── src/
│       │   └── agent.ts
│       ├── langgraph.json  # Config file in agent directory
│       ├── package.json    # Agent dependencies
│       ├── .env
│       └── tsconfig.json
└── other-service/
    └── ...
```

## LangGraph.json configuration

Place the langgraph.json file in your agent’s directory (not in the monorepo root). Ensure the file follows the required structure:

```json Python
{
  "dependencies": [
    ".",
    "../../shared-utils"
  ],
  "graphs": {
    "customer_support": "./agent/graph.py:graph"
  },
  "env": ".env"
}
```

```json JS
{
  "node_version": "20",
  "graphs": {
    "customer_support": "./src/agent.ts:graph"
  },
  "env": ".env"
}
```

In the Python example, `"."` is the current agent package and `"../../shared-utils"` is the relative path to a shared package.

The Python implementation automatically handles packages in parent directories by:

* Detecting relative paths that start with `"."`.
* Adding parent directories to the Docker build context as needed.
* Supporting both real packages (with `pyproject.toml`/`setup.py`) and simple Python modules.

For JavaScript monorepos:

* Shared workspace dependencies are resolved automatically by your package manager.
* Your `package.json` should reference shared packages using workspace syntax.

Example `package.json` in the agent directory:

```json
{
  "name": "customer-support-agent",
  "dependencies": {
    "@company/shared-utils": "workspace:*",
    "@langchain/langgraph": "^0.2.0"
  }
}
```

## Building the application

Run `langgraph build`:

```bash Python
cd agents/customer-support
langgraph build -t my-customer-support-agent
```

```bash JS
# Run from the root of the monorepo
langgraph build -t my-customer-support-agent -c agents/customer-support/langgraph.json
```

The Python build process:

1. Automatically detects relative dependency paths.
2. Copies shared packages into the Docker build context.
3. Installs all dependencies in the correct order.
4. No special flags or commands required.

The JavaScript build process:

1. Uses the directory you called `langgraph build` from (the monorepo root in this case) as the build context.
2. Automatically detects your package manager (yarn, npm, pnpm, bun).
3. Runs the appropriate install flow based on your project configuration.
4. Uses the directory containing `langgraph.json` to locate the app being built.

## Tips and best practices

1. **Keep agent configs in agent directories**: Place `langgraph.json` files in the specific agent directories, not at the monorepo root. This allows you to support multiple agents in the same monorepo, without having to deploy them all in the same LangSmith deployment.

2. **Use relative paths for Python**: For Python monorepos, use relative paths like `"../../shared-package"` in the `dependencies` array.

3. **Leverage workspace features for JS**: For JavaScript/TypeScript, use your package manager's workspace features to manage dependencies between packages.

4. **Test locally first**: Always test your build locally before deploying to ensure all dependencies are correctly resolved.

5. **Environment variables**: Keep environment files (`.env`) in your agent directories for environment-specific configuration.
