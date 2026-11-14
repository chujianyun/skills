# How to add custom middleware

When deploying agents to LangSmith, you can add custom middleware to your server to handle concerns like logging request metrics, injecting or checking headers, and enforcing security policies without modifying core server logic. This works the same way as [adding custom routes](How%20to%20add%20custom%20routes.md). You just need to provide your own [`Starlette`](https://starlette.dev/applications/) app (including [`FastAPI`](https://fastapi.tiangolo.com/), [`FastHTML`](https://fastht.ml/) and other compatible apps).

Adding middleware lets you intercept and modify requests and responses globally across your deployment, whether they're hitting your custom endpoints or the built-in LangSmith APIs.

Below is an example using FastAPI.

> [!NOTE]
>
> "Python only"
> We currently only support custom middleware in Python deployments with `langgraph-api>=0.0.26`.

## Create app

Starting from an **existing** LangSmith application, add the following middleware code to your `webapp.py` file. If you are starting from scratch, you can create a new app from a template using the CLI.

```bash
langgraph new --template=new-langgraph-project-python my_new_project
```

Once you have a LangGraph project, add the following app code:

```python {highlight={5}}
# ./src/agent/webapp.py
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

class CustomHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers['X-Custom-Header'] = 'Hello from middleware!'
        return response

# Add the middleware to the app
app.add_middleware(CustomHeaderMiddleware)
```

## Configure `langgraph.json`

Add the following to your `langgraph.json` configuration file. Make sure the path points to the `webapp.py` file you created above.

```json
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./src/agent/graph.py:graph"
  },
  "env": ".env",
  "http": {
    "app": "./src/agent/webapp.py:app"
  }
  // Other configuration options like auth, store, etc.
}
```

### Customize middleware ordering

By default, custom middleware runs before authentication logic. To run custom middleware *after* authentication, set `middleware_order` to `auth_first` in your `http` configuration. (This customization is supported starting with API server v0.4.35 and later.)

```json
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./src/agent/graph.py:graph"
  },
  "env": ".env",
  "http": {
    "app": "./src/agent/webapp.py:app",
    "middleware_order": "auth_first"
  },
  "auth": {
    "path": "./auth.py:my_auth"
  }
}
```

## Start server

Test the server out locally:

```bash
langgraph dev --no-browser
```

Now any request to your server will include the custom header `X-Custom-Header` in its response.

## Deploying

You can deploy this app as-is to cloud or to your self-hosted platform.

## Next steps

Now that you've added custom middleware to your deployment, you can use similar techniques to add [custom routes](How%20to%20add%20custom%20routes.md) or define [custom lifespan events](How%20to%20add%20custom%20lifespan%20events.md) to further customize your server's behavior.
