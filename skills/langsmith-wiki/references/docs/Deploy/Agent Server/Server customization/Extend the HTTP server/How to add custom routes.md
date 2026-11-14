# How to add custom routes

When deploying agents to LangSmith Agent Server, your server automatically exposes routes for creating runs and threads, interacting with the long-term memory store, managing configurable assistants, and other core functionality ([see all default API endpoints](../../../Get%20started/Reference/Agent%20Server%20API/Agent%20Server%20API%20reference.md)).

You can add custom routes by providing your own app object and passing its path in `langgraph.json` (for example, a [`Starlette`](https://starlette.dev/applications/) app in Python or a [`Hono`](https://hono.dev/) app in TypeScript).

Defining a custom app object lets you add any routes you'd like, so you can do anything from adding a `/login` endpoint to writing an entire full-stack web-app, all deployed in a single Agent Server.

Below are examples for Python and TypeScript.

## Create app

Starting from an **existing** LangSmith application, add the following custom route code to your app file. If you are starting from scratch, you can create a new app from a template using the CLI.

> [tab] Python
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> langgraph new --template=new-langgraph-project-python my_new_project
> ```
>
> Once you have a LangGraph project, add the following app code:
>
> ```python {highlight={4}} theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # ./src/agent/webapp.py
> from fastapi import FastAPI
>
> app = FastAPI()
>
>
> @app.get("/hello")
> def read_root():
>     return {"Hello": "World"}
> ```

> [tab] TypeScript
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> yarn create langgraph
> npm install hono
> ```
>
> Once you have a LangGraph project, add the following app code:
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // ./src/custom-routes.ts
> import { Hono } from "hono";
>
> export const app = new Hono()
>   .get("/custom/hello", (c) => {
>     return c.json({ hello: "world" });
>   })
>   .post("/custom/webhook", async (c) => {
>     const body = await c.req.json();
>     return c.json({ received: true, payload: body });
>   });
> ```
>
> The `hono` package must be available in your project dependencies.

## Configure `langgraph.json`

Add the following to your `langgraph.json` configuration file. Make sure the path points to the app instance you created in the [previous section](#create-app).

> [tab] Python
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "dependencies": ["."],
>   "graphs": {
>     "agent": "./src/agent/graph.py:graph"
>   },
>   "env": ".env",
>   "http": {
>     "app": "./src/agent/webapp.py:app"
>   }
>   // Other configuration options like auth, store, etc.
> }
> ```

> [tab] TypeScript
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "node_version": "20",
>   "dependencies": ["."],
>   "graphs": { "agent": "./src/agent.ts:graph" },
>   "http": { "app": "./src/custom-routes.ts:app" },
>   "env": ".env"
> }
> ```

## Start server

Test the server out locally:

> [tab] Python
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> langgraph dev --no-browser
> ```

> [tab] TypeScript
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> npx @langchain/langgraph-cli@latest dev --no-browser
> ```

If you navigate to `localhost:2024/hello` in your browser (`2024` is the default development port), you should see the `/hello` endpoint returning a JSON response. For the TypeScript example, navigate to `localhost:2024/custom/hello`.

The TypeScript `http.app` configuration works in both local development with `langgraph dev` and Docker with `langgraph up`.

> [!NOTE]
>
> **Shadowing default endpoints**
> The routes you create in the app are given priority over the system defaults, meaning you can shadow and redefine the behavior of any default endpoint.

## Deploying

You can deploy this app as-is to LangSmith or to your self-hosted platform.

## Next steps

Now that you've added a custom route to your deployment, you can use this same technique to further customize how your server behaves, such as defining [custom middleware](How%20to%20add%20custom%20middleware.md) and [custom lifespan events](How%20to%20add%20custom%20lifespan%20events.md).
