# Build a custom frontend for a Managed Deep Agent

> Call a Managed Deep Agents deployment from your own web or Python application with the LangChain frontend SDKs and the LangGraph SDK.

A custom frontend is any application you write that calls a deployment directly instead of reaching the agent through a [channel](../Agent%20capabilities/Channels/Connect%20Managed%20Deep%20Agents%20to%20channels.md) or [LangSmith Studio](Develop%20locally%20with%20LangSmith%20Studio.md#start-local-studio). Use one when the agent belongs inside a product surface you control, such as a support console, an internal dashboard, or a customer-facing chat page.

Managed Deep Agents deployments run on [LangSmith Agent Server](../../../../Deploy/Agent%20Server/Agent%20Server.md), so a frontend talks to the same threads, runs, and streaming endpoints that every Agent Server client uses. Nothing on the agent side changes to support one.

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

## Choose an identity mode

Where your frontend code runs determines which [identity](../Agent%20capabilities/Add%20identity%20to%20Managed%20Deep%20Agents.md) mode it can use. A LangSmith API key grants access to the whole workspace, so it must never reach a browser.

| Frontend | Credential lives in | Identity mode |
| - | - | - |
| Browser application (React, Vue, Svelte, Angular) | The user's browser | [Supabase](../Agent%20capabilities/Add%20identity%20to%20Managed%20Deep%20Agents.md#configure-identity-with-supabase) |
| Server route or proxy that forwards browser requests | Your server | [LangSmith API key](../Agent%20capabilities/Add%20identity%20to%20Managed%20Deep%20Agents.md#configure-identity-with-a-langsmith-api-key) or [your own backend](../Agent%20capabilities/Add%20identity%20to%20Managed%20Deep%20Agents.md#configure-identity-with-your-own-backend) |
| Python application (Streamlit, Gradio, Dash) | Your server | LangSmith API key |
| Local development with `mda dev` | No credential required | Any |

With backend identity, the browser never calls the deployment. Your API authenticates the user, then calls the deployment with the ingress secret. Supabase and backend identity also give each signed-in user private threads. The API-key default does not: every caller holding the key shares the same thread space.

> [!WARNING]
>
> Anyone with a LangSmith API key can reach the deployment and every other resource in the workspace. Shipping one in browser JavaScript exposes it to every visitor. When the browser calls the deployment, use Supabase. Otherwise keep credentials on a server route the browser calls.

## Connect to the deployment

A frontend needs two values.

**Deployment API URL.** `mda deploy` prints the LangSmith deployment dashboard URL, not the API URL. Open that dashboard, then copy the **API URL** from the deployment details view. The local server started by [`mda dev`](Develop%20locally%20with%20LangSmith%20Studio.md) serves the same routes at the URL the CLI prints.

**Assistant ID.** Clients pass the agent's `name` from the [agent definition](../Agent%20capabilities/Define%20a%20Managed%20Deep%20Agent.md#parameters), which Managed Deep Agents also uses as the graph ID:

```python agent.py
from managed_deepagents import define_deep_agent

agent = define_deep_agent(
    name="research-assistant",  # [!code highlight]
    model="openai:gpt-6.1-sol",
)
```

Clients address an agent named `research-assistant` as `assistantId: "research-assistant"`. Renaming the agent changes the value clients send, so treat the name as part of the deployment's public interface.

## Build a web frontend

The [LangChain frontend SDKs](https://docs.langchain.com/oss/python/langchain/frontend/overview.md) connect a browser application to an Agent Server deployment. `useStream` exposes messages, tool calls, interrupts, and thread state as reactive values:

| Framework | Package | Entry point |
| - | - | - |
| React | `@langchain/react` | `useStream` |
| Vue | `@langchain/vue` | `useStream` |
| Svelte | `@langchain/svelte` | `useStream` |
| Angular | `@langchain/angular` | `injectStream` |

A frontend is a web application, so these examples are TypeScript whether the agent is written in Python or TypeScript.

Point the hook at the deployment API URL and the agent name:

```tsx Chat.tsx
import { useStream } from "@langchain/react";
import { useState } from "react";

export function Chat() {
  const [input, setInput] = useState("");
  const stream = useStream({
    apiUrl: import.meta.env.VITE_DEPLOYMENT_API_URL,
    assistantId: "research-assistant",
    defaultHeaders: { Authorization: `Bearer ${accessToken}` },
  });

  return (
    <main>
      {stream.messages.map((message) => (
        <p key={message.id}>{message.text}</p>
      ))}

      <form
        onSubmit={(event) => {
          event.preventDefault();
          stream.submit({ messages: [{ type: "human", content: input }] });
          setInput("");
        }}
      >
        <input value={input} onChange={(event) => setInput(event.target.value)} />
        <button type="submit" disabled={stream.isLoading}>
          Send
        </button>
      </form>
    </main>
  );
}
```

`defaultHeaders` carries the Supabase access token that the signed-in user obtained from your auth flow. For the API-key default, pass `apiKey` instead, which the SDK sends as `x-api-key`. Only do so from code that runs on a server.

These patterns apply unchanged to a Managed Deep Agents deployment: [tool-call rendering](https://docs.langchain.com/oss/python/langchain/frontend/tool-calling.md), [generative UI](https://docs.langchain.com/oss/python/langchain/frontend/generative-ui-overview.md), [human-in-the-loop approval](https://docs.langchain.com/oss/python/langchain/frontend/human-in-the-loop.md), [queued submissions](https://docs.langchain.com/oss/python/langchain/frontend/message-queues.md), and [durable rejoin](https://docs.langchain.com/oss/python/langchain/frontend/join-rejoin.md).

### Handle authorization interrupts

When the agent needs a [user-owned connection](../Agent%20capabilities/Manage%20connections.md) the caller has not granted, the run pauses and `stream.interrupt` carries a credential gate payload. A browser frontend renders the consent links and resumes with `stream.respond`. For the payload shape and a worked example, see [Handle the authorization interrupt](../Agent%20capabilities/Manage%20connections.md#handle-the-authorization-interrupt).

## Build a Python frontend

Streamlit, Gradio, and Dash render on the server, so the LangSmith API key stays out of the browser and the API-key default works without extra setup. All three use the same [LangGraph SDK](../../../../Deploy/Get%20started/Reference/Related/langgraph_sdk.md) client, so the connection code below applies to any of them.

Install the SDK alongside your application framework:

```bash
uv add langgraph-sdk streamlit
```

Create a client, then stream a run against a thread:

```python
from langgraph_sdk import get_sync_client

client = get_sync_client(
    url=DEPLOYMENT_API_URL,
    api_key=LANGSMITH_API_KEY,
)

thread = client.threads.create()

for chunk in client.runs.stream(
    thread["thread_id"],
    "research-assistant",
    input={"messages": [{"role": "user", "content": "Summarize this week's incidents."}]},
    stream_mode="messages",
):
    ...
```

Three details govern how that loop behaves:

* **`api_key`**: Sets the `x-api-key` header. Passing `headers={"x-api-key": ...}` instead raises `ValueError: Cannot set reserved header 'x-api-key'`.
* **Environment fallback**: When `api_key` is omitted, the client tries `LANGGRAPH_API_KEY`, then `LANGSMITH_API_KEY`, then `LANGCHAIN_API_KEY`. For Supabase or backend identity, pass `api_key=None` explicitly and put the token in `headers`, or a stray environment variable attaches a second credential.
* **`messages/partial`**: Carries the whole message so far, not a delta. Replace the rendered text on each event rather than appending, or the output repeats itself.

### Stream into a Streamlit chat

This application keeps one thread per browser session and rewrites the assistant bubble as each event arrives:

```python app.py
import os

import streamlit as st
from langgraph_sdk import get_sync_client

ASSISTANT_ID = "research-assistant"


@st.cache_resource
def get_agent_client():
    return get_sync_client(
        url=os.environ["DEPLOYMENT_API_URL"],
        api_key=os.environ["LANGSMITH_API_KEY"],
    )


def text_of(message):
    return "".join(
        block.get("text", "")
        for block in message.get("content", [])
        if block.get("type") == "text"
    )


client = get_agent_client()

if "thread_id" not in st.session_state:
    st.session_state.thread_id = client.threads.create()["thread_id"]
    st.session_state.history = []

for role, text in st.session_state.history:
    st.chat_message(role).markdown(text)

if prompt := st.chat_input("Message the agent"):
    st.session_state.history.append(("user", prompt))
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        answer = ""
        for chunk in client.runs.stream(
            st.session_state.thread_id,
            ASSISTANT_ID,
            input={"messages": [{"role": "user", "content": prompt}]},
            stream_mode="messages",
        ):
            if chunk.event != "messages/partial":
                continue
            for message in chunk.data:
                if message.get("type") == "ai":
                    answer = text_of(message)
                    placeholder.markdown(answer)  # [!code highlight]

    st.session_state.history.append(("assistant", answer))
```

The highlighted line replaces the bubble contents on every event. Appending there produces duplicated text, because each event repeats the message from the beginning.

`text_of` reads content blocks rather than a plain string. Agent messages arrive as a list of typed blocks, so a frontend that expects `message["content"]` to be text renders nothing. The web SDKs deserialize each event into a message object that exposes a `text` accessor, which is why the React example above reads `message.text`. The LangGraph SDK yields plain dictionaries, so a Python frontend extracts the text itself.

Gradio and Dash use the same client and the same loop. Substitute their streaming primitive for the Streamlit placeholder: a generator function for `gr.ChatInterface`, or a `dcc.Interval` callback for Dash.

## See also

* [Identity](../Agent%20capabilities/Add%20identity%20to%20Managed%20Deep%20Agents.md): configure how callers authenticate to the deployment.
* [Frontend overview](https://docs.langchain.com/oss/python/langchain/frontend/overview.md): message rendering, tool calls, interrupts, and generative UI patterns.
* [Connections](../Agent%20capabilities/Manage%20connections.md): handle the credential authorization interrupt in your UI.
* [MCP endpoint](Connect%20MCP%20clients%20to%20a%20Managed%20Deep%20Agent.md): expose the agent to MCP clients instead of calling the API.
* [Channels](../Agent%20capabilities/Channels/Connect%20Managed%20Deep%20Agents%20to%20channels.md): reach the agent from Slack or your own HTTP service.
