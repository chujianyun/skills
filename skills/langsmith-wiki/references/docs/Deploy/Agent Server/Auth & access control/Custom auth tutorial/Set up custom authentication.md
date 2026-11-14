# Set up custom authentication

In this tutorial, we will build a chatbot that only lets specific users access it. We'll start with the LangGraph template and add token-based security step by step. By the end, you'll have a working chatbot that checks for valid tokens before allowing access.

This is part 1 of our authentication series:

1. Set up custom authentication (you are here) - Control who can access your bot
2. [Make conversations private](Make%20conversations%20private.md) - Let users have private conversations
3. [Connect an authentication provider](Connect%20an%20authentication%20provider.md) - Add real user accounts and validate using OAuth2 for production

This guide assumes basic familiarity with the following concepts:

* [**Authentication & Access Control**](../Authentication%20%26%20access%20control.md)
* [**LangSmith**](../../../../Monitor/Overview/LangSmith%20Observability.md)

> [!NOTE]
>
> Custom auth is only available for LangSmith SaaS deployments or Enterprise Self-Hosted deployments.

## 1. Create your app

Create a new chatbot using the LangGraph starter template:

```bash pip
pip install -U "langgraph-cli[inmem]"
langgraph new --template=new-langgraph-project-python custom-auth
cd custom-auth
```

```bash uv
uv add "langgraph-cli[inmem]"
langgraph new --template=new-langgraph-project-python custom-auth
cd custom-auth
```

The template gives us a placeholder LangGraph app. Try it out by installing the local dependencies and running the development server:

```bash pip
pip install -e .
langgraph dev
```

```bash uv
uv add .
langgraph dev
```

```bash npm
npx @langchain/langgraph-cli dev
```

The server will start and open [Studio](../../../../Test/Test%20from%20Studio/LangSmith%20Studio.md) in your browser:

```
> - 🚀 API: http://127.0.0.1:2024
> - 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
> - 📚 API Docs: http://127.0.0.1:2024/docs
>
> This in-memory server is designed for development and testing.
> For production use, please use LangSmith.
```

If you were to self-host this on the public internet, anyone could access it.

![No authentication: the dev server is publicly reachable, anyone can access the bot if exposed to the internet.](../../../../../assets/images/d2d3fe46f0c9-no-auth.png)

## 2. Add authentication

Now that you have a base LangGraph app, add authentication to it.

> [!NOTE]
>
> In this tutorial, you will start with a hard-coded token for example purposes. You will get to a "production-ready" authentication scheme in the third tutorial.

The [Auth](https://reference.langchain.com/python/langgraph-sdk/auth/Auth) object lets you register an authentication function that the LangSmith deployment will run on every request. This function receives each request and decides whether to accept or reject.

Create a new file `src/security/auth.py`. This is where your code will live to check if users are allowed to access your bot:

```python {highlight={10,15-16}} title="src/security/auth.py"
from langgraph_sdk import Auth

# This is our toy user database. Do not do this in production
VALID_TOKENS = {
    "user1-token": {"id": "user1", "name": "Alice"},
    "user2-token": {"id": "user2", "name": "Bob"},
}

# The "Auth" object is a container that LangGraph will use to mark our authentication function
auth = Auth()


# The `authenticate` decorator tells LangGraph to call this function as middleware
# for every request. This will determine whether the request is allowed or not
@auth.authenticate
async def get_current_user(authorization: str | None) -> Auth.types.MinimalUserDict:
    """Check if the user's token is valid."""
    assert authorization
    scheme, token = authorization.split()
    assert scheme.lower() == "bearer"
    # Check if token is valid
    if token not in VALID_TOKENS:
        raise Auth.exceptions.HTTPException(status_code=401, detail="Invalid token")

    # Return user info if valid
    user_data = VALID_TOKENS[token]
    return {
        "identity": user_data["id"],
    }
```

Notice that your [Auth.authenticate](https://reference.langchain.com/python/langgraph-sdk/auth/Auth/authenticate) handler does two important things:

1. Checks if a valid token is provided in the request's [Authorization header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization)
2. Returns the user's [MinimalUserDict](https://reference.langchain.com/python/langgraph-sdk/auth/types/MinimalUserDict)

Now tell LangGraph to use authentication by adding the following to the [langgraph.json](https://reference.langchain.com/python/cloud/reference/cli/#configuration-file) configuration:

```json {highlight={7-9}} title="langgraph.json"
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./src/agent/graph.py:graph"
  },
  "env": ".env",
  "auth": {
    "path": "src/security/auth.py:auth"
  }
}
```

## 3. Test your bot

Start the server again to test everything out:

```bash
langgraph dev --no-browser
```

If you didn't add the `--no-browser`, the Studio UI will open in the browser. By default, we also permit access from Studio, even when using custom auth. This makes it easier to develop and test your bot in Studio. You can remove this alternative authentication option by setting `disable_studio_auth: true` in your auth configuration:

```json
{
    "auth": {
        "path": "src/security/auth.py:auth",
        "disable_studio_auth": true
    }
}
```

To accept LangSmith API keys (`x-api-key`) alongside your custom handler outside of Studio, set `allow_langsmith_api_keys: true`. Requests with an `Authorization` header still use custom auth. All other requests use LangSmith auth. Set the `x-auth-scheme: langsmith` header to force LangSmith auth even when `Authorization` is present. LangSmith-authenticated callers expose `ctx.user.identity` as the LangSmith user ID (or missing) and `ctx.permissions` as `["authenticated"]`. Custom `@auth.on` handlers still run, so design them to accept that shape if both paths should share resource rules. This option requires `disable_studio_auth` unset or `false`.

> [!NOTE]
>
> `allow_langsmith_api_keys` requires Agent Server `0.14.0rc2` or later.

## 4. Chat with your bot

You should now only be able to access the bot if you provide a valid token in the request header. Users will still, however, be able to access each other's resources until you add [resource authorization handlers](../Authentication%20%26%20access%20control.md#resource-specific-handlers) in the next section of the tutorial.

![Auth gate passes requests with a valid token, but no per-resource filters are applied yet—so users share visibility until authorization handlers are added in the next step.](../../../../../assets/images/6037686927e2-authentication.png)

Run the following code in a file or notebook:

```python
import asyncio

from langgraph_sdk import get_client


async def main():
    # Try without a token (should fail)
    client = get_client(url="http://localhost:2024")
    try:
        thread = await client.threads.create()
        print("❌ Should have failed without token!")
    except Exception as e:
        print("✅ Correctly blocked access:", e)

    # Try with a valid token
    client = get_client(
        url="http://localhost:2024", headers={"Authorization": "Bearer user1-token"}
    )

    # Create a thread and chat
    thread = await client.threads.create()
    print(f"✅ Created thread as Alice: {thread['thread_id']}")

    response = await client.runs.create(
        thread_id=thread["thread_id"],
        assistant_id="agent",
        input={"messages": [{"role": "user", "content": "Hello!"}]},
    )
    print("✅ Bot responded:")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
```

You should see that:

1. Without a valid token, we can't access the bot
2. With a valid token, we can create threads and chat

Congratulations! You've built a chatbot that only lets "authenticated" users access it. While this system doesn't (yet) implement a production-ready security scheme, we've learned the basic mechanics of how to control access to our bot. In the next tutorial, we'll learn how to give each user their own private conversations.

## Next steps

Now that you can control who accesses your bot, you might want to:

1. Continue the tutorial by going to [Make conversations private](Make%20conversations%20private.md) to learn about resource authorization.
2. Read more about [authentication concepts](../Authentication%20%26%20access%20control.md).
3. Check out the API reference for [Auth](https://reference.langchain.com/python/langgraph-sdk/auth/Auth), [Auth.authenticate](https://reference.langchain.com/python/langgraph-sdk/auth/Auth/authenticate), and [MinimalUserDict](https://reference.langchain.com/python/langgraph-sdk/auth/types/MinimalUserDict) for more authentication details.
