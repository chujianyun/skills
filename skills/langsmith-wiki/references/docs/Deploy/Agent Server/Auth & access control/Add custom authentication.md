# Add custom authentication

This guide shows you how to add custom authentication to your LangSmith application. The steps on this page apply to both [cloud](../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [self-hosted](../../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) deployments. It does not apply to isolated usage of the [LangGraph open source library](https://docs.langchain.com/oss/python/langgraph/overview.md) in your own custom server.

## Add custom authentication to your deployment

To leverage custom authentication and access user-level metadata in your deployments, set up custom authentication to automatically populate the `config["configurable"]["langgraph_auth_user"]` object through a custom authentication handler. You can then access this object in your graph with the `langgraph_auth_user` key to [allow an agent to perform authenticated actions on behalf of the user](#enable-agent-authentication).

1. Implement authentication:

   > [!NOTE]
   >
   > Without a custom `@auth.authenticate` handler, LangGraph sees only the API-key owner (usually the developer), so requests aren’t scoped to individual end-users. To propagate custom tokens, you must implement your own handler.

   ```python
   from langgraph_sdk import Auth
   import requests

   auth = Auth()

   def is_valid_key(api_key: str) -> bool:
       is_valid = # your API key validation logic
       return is_valid

   @auth.authenticate # (1)!
   async def authenticate(headers: dict) -> Auth.types.MinimalUserDict:
       api_key = headers.get(b"x-api-key")
       if not api_key or not is_valid_key(api_key):
           raise Auth.exceptions.HTTPException(status_code=401, detail="Invalid API key")

       # Fetch user-specific tokens from your secret store
       user_tokens = await fetch_user_tokens(api_key)

       return { # (2)!
           "identity": api_key,  #  fetch user ID from LangSmith
           "github_token" : user_tokens.github_token
           "jira_token" : user_tokens.jira_token
           # ... custom fields/secrets here
       }
   ```

* This handler receives the request (headers, etc.), validates the user, and returns a dictionary with at least an identity field.
* You can add any custom fields you want (e.g., OAuth tokens, roles, org IDs, etc.).

2. In your [`langgraph.json`](../Develop%20your%20application/Application%20structure.md#configuration-file), add the path to your auth file:

   ```json highlight={7-9}
   {
       "dependencies": ["."],
       "graphs": {
       "agent": "./agent.py:graph"
       },
       "env": ".env",
       "auth": {
           "path": "./auth.py:my_auth"
       }
   }
   ```
3. Once you've set up authentication in your server, requests must include the required authorization information based on your chosen scheme. Assuming you are using JWT token authentication, you could access your deployments using any of the following methods:

   > [tab] Python Client
   >
   > ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
   > from langgraph_sdk import get_client
   >
   > my_token = "your-token" # In practice, you would generate a signed token with your auth provider
   > client = get_client(
   >     url="http://localhost:2024",
   >     headers={"Authorization": f"Bearer {my_token}"}
   > )
   > threads = await client.threads.search()
   > ```

   > [tab] Python RemoteGraph
   >
   > ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
   > from langgraph.pregel.remote import RemoteGraph
   >
   > my_token = "your-token" # In practice, you would generate a signed token with your auth provider
   > remote_graph = RemoteGraph(
   >     "agent",
   >     url="http://localhost:2024",
   >     headers={"Authorization": f"Bearer {my_token}"}
   > )
   > threads = await remote_graph.ainvoke(...)
   > ```

   > [tab] JavaScript Client
   >
   > ```javascript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
   > import { Client } from "@langchain/langgraph-sdk";
   >
   > const my_token = "your-token"; // In practice, you would generate a signed token with your auth provider
   > const client = new Client({
   > apiUrl: "http://localhost:2024",
   > defaultHeaders: { Authorization: `Bearer ${my_token}` },
   > });
   > const threads = await client.threads.search();
   > ```

   > [tab] JavaScript RemoteGraph
   >
   > ```javascript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
   > import { RemoteGraph } from "@langchain/langgraph/remote";
   >
   > const my_token = "your-token"; // In practice, you would generate a signed token with your auth provider
   > const remoteGraph = new RemoteGraph({
   > graphId: "agent",
   > url: "http://localhost:2024",
   > headers: { Authorization: `Bearer ${my_token}` },
   > });
   > const threads = await remoteGraph.invoke(...);
   > ```

   > [tab] cURL
   >
   > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
   > curl -H "Authorization: Bearer ${your-token}" http://localhost:2024/threads
   > ```

   For more details on RemoteGraph, refer to the [Use RemoteGraph](../Capabilities/How%20to%20interact%20with%20a%20deployment%20using%20RemoteGraph.md) guide.

## Enable agent authentication

After [authentication](#add-custom-authentication-to-your-deployment), the platform creates a special configuration object (`config`) that is passed to LangSmith deployment. This object contains information about the current user, including any custom fields you return from your `@auth.authenticate` handler.

To allow an agent to perform authenticated actions on behalf of the user, access this object in your graph with the `langgraph_auth_user` key:

```python
def my_node(state, config):
    user_config = config["configurable"].get("langgraph_auth_user")
    # token was resolved during the @auth.authenticate function
    token = user_config.get("github_token","")
    ...
```

> [!NOTE]
>
> Fetch user credentials from a secure secret store. Storing secrets in graph state is not recommended.

### Authorizing a user for Studio

By default, if you add custom authorization on your resources, this will also apply to interactions made from [Studio](../../../Test/Test%20from%20Studio/LangSmith%20Studio.md). If you want, you can handle logged-in Studio users differently by checking [is\_studio\_user()](https://reference.langchain.com/python/langgraph-sdk/auth/types/StudioUser).

> [!NOTE]
>
> `is_studio_user` was added in version 0.1.73 of the langgraph-sdk. If you're on an older version, you can still check whether `isinstance(ctx.user, StudioUser)`.

```python
from langgraph_sdk.auth import is_studio_user, Auth
auth = Auth()

# ... Setup authenticate, etc.

@auth.on
async def add_owner(
    ctx: Auth.types.AuthContext,
    value: dict  # The payload being sent to this access method
) -> dict:  # Returns a filter dict that restricts access to resources
    if is_studio_user(ctx.user):
        return {}

    filters = {"owner": ctx.user.identity}
    metadata = value.setdefault("metadata", {})
    metadata.update(filters)
    return filters
```

Only use this if you want to permit developer access to a graph deployed on the managed LangSmith SaaS.

## Learn more

* [Authentication & Access Control](Authentication%20%26%20access%20control.md)
* [Setting up custom authentication tutorial](Custom%20auth%20tutorial/Set%20up%20custom%20authentication.md)
