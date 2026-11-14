# Implement distributed tracing

Sometimes, you need to trace a request across multiple services.

LangSmith supports distributed tracing out of the box, linking runs within a trace across services using context propagation headers (`langsmith-trace` and optional `baggage` for metadata/tags).

Example client-server setup:

* Trace starts on client
* Continues on server

> [!WARNING]
>
> **Only accept distributed-tracing headers from trusted services.** The `langsmith-trace` and `baggage` headers are consumed as trusted tracing context. Do not add `TracingMiddleware` (or pass inbound request headers as the tracing `parent`) on a service that receives requests directly from untrusted third parties or the public internet. Keep distributed tracing to internal, service-to-service calls, and strip these headers from untrusted inbound requests at your gateway or proxy. Trusting `baggage` from an external caller lets them influence how your runs are recorded.

## Distributed tracing in Python

```python
# client.py
from langsmith.run_helpers import get_current_run_tree, traceable
import httpx

@traceable
async def my_client_function():
    headers = {}
    async with httpx.AsyncClient(base_url="...") as client:
        if run_tree := get_current_run_tree():
            # add langsmith-id to headers
            headers.update(run_tree.to_headers())
        return await client.post("/my-route", headers=headers)
```

Then the server (or other service) can continue the trace by handling the headers appropriately. If you are using an asgi app Starlette or FastAPI, you can connect the distributed trace using LangSmith's `TracingMiddleware`.

> [!NOTE]
>
> The `TracingMiddleware` class was added in `langsmith==0.1.133`.

Example using FastAPI:

```python
from langsmith import traceable
from langsmith.middleware import TracingMiddleware
from fastapi import FastAPI, Request

app = FastAPI()  # Or Flask, Django, or any other framework
app.add_middleware(TracingMiddleware)

@traceable
async def some_function():
    ...

@app.post("/my-route")
async def fake_route(request: Request):
    return await some_function()
```

Or in Starlette:

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware
from langsmith.middleware import TracingMiddleware

routes = ...
middleware = [
    Middleware(TracingMiddleware),
]
app = Starlette(..., middleware=middleware)
```

If you are using other server frameworks, you can always "receive" the distributed trace by passing the headers in through `langsmith_extra`:

```python
# server.py
import langsmith as ls
from fastapi import FastAPI, Request

@ls.traceable
async def my_application():
    ...

app = FastAPI()  # Or Flask, Django, or any other framework

@app.post("/my-route")
async def fake_route(request: Request):
    # request.headers:  {"langsmith-trace": "..."}
    # as well as optional metadata/tags in `baggage`
    with ls.tracing_context(parent=request.headers):
        return await my_application()
```

The example above uses the `tracing_context` context manager. You can also directly specify the parent run context in the `langsmith_extra` parameter of a method wrapped with `@traceable`.

```python
# ... same as above

@app.post("/my-route")
async def fake_route(request: Request):
    # request.headers:  {"langsmith-trace": "..."}
    my_application(langsmith_extra={"parent": request.headers})
```

## Distributed tracing in TypeScript

> [!NOTE]
>
> Distributed tracing in TypeScript requires `langsmith>=0.1.31`

First, we obtain the current run tree from the client and convert it to `langsmith-trace` and `baggage` header values, which we can pass to the server:

```typescript
// client.mts
import { getCurrentRunTree, traceable } from "langsmith/traceable";

const client = traceable(
    async () => {
        const runTree = getCurrentRunTree();
        return await fetch("...", {
            method: "POST",
            headers: runTree.toHeaders(),
        }).then((a) => a.text());
    },
    { name: "client" }
);

await client();
```

Then, the server converts the headers back to a run tree, which it uses to further continue the tracing.

To pass the newly created run tree to a traceable function, we can use the `withRunTree` helper, which will ensure the run tree is propagated within traceable invocations.

```typescript Express.JS
// server.mts
import { RunTree } from "langsmith";
import { traceable, withRunTree } from "langsmith/traceable";
import express from "express";
import bodyParser from "body-parser";

    const server = traceable(
        (text: string) => `Hello from the server! Received "${text}"`,
        { name: "server" }
    );

    const app = express();
    app.use(bodyParser.text());

app.post("/", async (req, res) => {
    const runTree = RunTree.fromHeaders(req.headers);
    const result = await withRunTree(runTree, () => server(req.body));
    res.send(result);
});
```

```typescript Hono
// server.mts
import { RunTree } from "langsmith";
import { traceable, withRunTree } from "langsmith/traceable";
import { Hono } from "hono";

    const server = traceable(
        (text: string) => `Hello from the server! Received "${text}"`,
        { name: "server" }
    );

    const app = new Hono();

app.post("/", async (c) => {
    const body = await c.req.text();
    const runTree = RunTree.fromHeaders(c.req.raw.headers);
    const result = await withRunTree(runTree, () => server(body));
    return c.body(result);
});
```
