# Manage assistants

This page describes how to create, configure, and manage [assistants](Assistants.md). Assistants allow you to customize your [deployed](../../../Get%20started/LangSmith%20Agent%20Server.md) graph's behavior through configuration—such as model selection, prompts, and tool availability—without changing the underlying graph code.

You can work with the [SDK](../../../Get%20started/Reference/Deployment%20SDK.md) or in the LangSmith UI.

## Understand assistant configuration

Assistants store *context* values that customize graph behavior at runtime. You define a context schema in your graph code, then provide specific context values when creating an assistant via the [`context` parameter](https://reference.langchain.com/python/langsmith/deployment/sdk/#langgraph_sdk.client.AssistantsClient.create).

Consider this example of a `call_model` node that reads the `model_name` from the context:

```python Python
class ContextSchema(TypedDict):
    model_name: str

builder = StateGraph(AgentState, context_schema=ContextSchema)

def call_model(state, runtime: Runtime[ContextSchema]):
    messages = state["messages"]
    model = _get_model(runtime.context.get("model_name", "anthropic"))
    response = model.invoke(messages)
    return {"messages": [response]}
```

```javascript JavaScript
import { Annotation } from "@langchain/langgraph";

const ContextSchema = Annotation.Root({
    model_name: Annotation<string>,
    system_prompt: Annotation<string>,
});

const builder = new StateGraph(AgentState, ContextSchema)

function callModel(state: State, runtime: Runtime[ContextSchema]) {
  const messages = state.messages;
  const model = _getModel(runtime.context.model_name ?? "anthropic");
  const response = model.invoke(messages);
  return { messages: [response] };
}
```

When you create an assistant, you provide specific values for these configuration fields. The assistant stores this configuration and applies it whenever the graph runs.

For more information on configuration in [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview.md), refer to the [runtime context documentation](https://docs.langchain.com/oss/python/langgraph/graph-api.md#runtime-context).

## Create an assistant

> [tab] SDK
>
> Use the [`assistants.create`](https://reference.langchain.com/python/langsmith/deployment/sdk/#langgraph_sdk.client.AssistantsClient.create) method to create a new assistant. This method requires:
>
> * **Graph ID**: The name of the deployed graph this assistant will use (e.g., `"agent"`).
> * **Context**: Configuration values matching your graph's context schema.
> * **Name**: A descriptive name for the assistant.
>
> The following example creates an assistant with `model_name` set to `openai`:
>
> ```python Python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph_sdk import get_client
>
> # Initialize the client with your deployment URL
> client = get_client(url=<DEPLOYMENT_URL>)
>
> # Create an assistant for the "agent" graph
> # The first parameter is the graph ID (also called graph name)
> openai_assistant = await client.assistants.create(
>     "agent",  # Graph ID of the deployed graph
>     context={"model_name": "openai"},
>     name="Open AI Assistant"
> )
>
> print(openai_assistant)
> # Output includes the assistant_id (UUID) that uniquely identifies this assistant
> ```
>
> ```javascript JavaScript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { Client } from "@langchain/langgraph-sdk";
>
> // Initialize the client with your deployment URL
> const client = new Client({ apiUrl: <DEPLOYMENT_URL> });
>
> // Create an assistant for the "agent" graph
> const openAIAssistant = await client.assistants.create({
>     graphId: 'agent',  // Graph ID of the deployed graph
>     name: "Open AI Assistant",
>     context: { "model_name": "openai" },
> });
>
> console.log(openAIAssistant);
> // Output includes the assistant_id (UUID) that uniquely identifies this assistant
> ```
>
> ```bash cURL theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
>     --url <DEPLOYMENT_URL>/assistants \
>     --header 'Content-Type: application/json' \
>     --data '{"graph_id":"agent", "context":{"model_name":"openai"}, "name": "Open AI Assistant"}'
> ```
>
> **Response:**
>
> The API returns an assistant object containing:
>
> * `assistant_id`: A UUID that uniquely identifies this assistant
> * `graph_id`: The graph this assistant is configured for
> * `context`: The configuration values you provided
> * `name`, `metadata`, timestamps, and other fields
>
> ```json theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> {
>   "assistant_id": "62e209ca-9154-432a-b9e9-2d75c7a9219b",
>   "graph_id": "agent",
>   "name": "Open AI Assistant",
>   "context": {
>     "model_name": "openai"
>   },
>   "metadata": {},
>   "created_at": "2024-08-31T03:09:10.230718+00:00",
>   "updated_at": "2024-08-31T03:09:10.230718+00:00"
> }
> ```
>
> The `assistant_id` (a UUID like `"62e209ca-9154-432a-b9e9-2d75c7a9219b"`) uniquely identifies this assistant configuration. You'll use this ID when running your graph to specify which configuration to apply.
>
> > [!NOTE]
> >
> > **Graph ID vs Assistant ID**
> >
> > When creating an assistant, you specify a **graph ID** (graph name like `"agent"`). This returns an **assistant ID** (UUID like `"62e209ca..."`). You can use either when running your graph:
> >
> > * **Graph ID** (e.g., `"agent"`): Uses the default assistant for that graph
> > * **Assistant ID** (UUID): Uses the specific assistant configuration
> >
> > See [Use an assistant](#use-an-assistant).

> [tab] UI
>
> You can create assistants from the LangSmith UI:
>
> 1. Navigate to your deployment and select the **Assistants** tab.
> 2. Click **+ Assistant**.
> 3. In the form that opens:
>    * Select the graph this assistant is for.
>    * Provide a name and description.
>    * Configure the assistant using the configuration schema for that graph.
> 4. Click **Create assistant**.
>
> This will take you to [Studio](../../../../Test/Test%20from%20Studio/LangSmith%20Studio.md) where you can test the assistant. Return to the **Assistants** tab to see your newly created assistant in the table.

## Use an assistant

> [tab] SDK
>
> To use an assistant, pass its `assistant_id` when creating a run. The example below uses the assistant created above:
>
> ```python Python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Create a thread for the conversation
> thread = await client.threads.create()
>
> # Prepare the input
> input = {"messages": [{"role": "user", "content": "who made you?"}]}
>
> # Run the graph using the assistant's configuration
> # Pass the assistant_id (UUID) as the second parameter
> async for event in client.runs.stream(
>     thread["thread_id"],
>     openai_assistant["assistant_id"],  # Assistant ID (UUID)
>     input=input,
>     stream_mode="updates",
> ):
>     print(f"Receiving event of type: {event.event}")
>     print(event.data)
>     print("\n\n")
> ```
>
> ```javascript JavaScript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // Create a thread for the conversation
> const thread = await client.threads.create();
>
> // Prepare the input
> const input = { "messages": [{ "role": "user", "content": "who made you?" }] };
>
> // Run the graph using the assistant's configuration
> // Pass the assistant_id (UUID) as the second parameter
> const streamResponse = client.runs.stream(
>   thread["thread_id"],
>   openAIAssistant["assistant_id"],  // Assistant ID (UUID)
>   {
>     input,
>     streamMode: "updates"
>   }
> );
>
> for await (const event of streamResponse) {
>   console.log(`Receiving event of type: ${event.event}`);
>   console.log(event.data);
>   console.log("\n\n");
> }
> ```
>
> ```bash cURL theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # First, create a thread
> thread_id=$(curl --request POST \
>     --url <DEPLOYMENT_URL>/threads \
>     --header 'Content-Type: application/json' \
>     --data '{}' | jq -r '.thread_id')
>
> # Run the graph with the assistant ID (UUID)
> curl --request POST \
>     --url "<DEPLOYMENT_URL>/threads/${thread_id}/runs/stream" \
>     --header 'Content-Type: application/json' \
>     --data '{
>         "assistant_id": "<ASSISTANT_ID>",
>         "input": {
>             "messages": [
>                 {
>                     "role": "user",
>                     "content": "who made you?"
>                 }
>             ]
>         },
>         "stream_mode": ["updates"]
>     }' | \
>     sed 's/\r$//' | \
>     awk '
>     /^event:/ {
>         if (data_content != "") {
>             print data_content "\n"
>         }
>         sub(/^event: /, "Receiving event of type: ", $0)
>         printf "%s...\n", $0
>         data_content = ""
>     }
>     /^data:/ {
>         sub(/^data: /, "", $0)
>         data_content = $0
>     }
>     END {
>         if (data_content != "") {
>             print data_content "\n\n"
>         }
>     }
> '
> ```
>
> **Response:**
>
> The stream returns events as the graph executes with your assistant's configuration:
>
> ```
> Receiving event of type: metadata
> {'run_id': '1ef6746e-5893-67b1-978a-0f1cd4060e16'}
>
> Receiving event of type: updates
> {'agent': {'messages': [{'content': 'I was created by OpenAI...', ...}]}}
> ```
>
> To run the graph with its default assistant instead, pass the graph ID (for example, `"agent"`) in place of the assistant ID.

> [tab] UI
>
> To use an assistant in the LangSmith UI:
>
> 1. Navigate to your deployment and select the **Assistants** tab.
> 2. Find the assistant you want to use.
> 3. Click **Studio** for that assistant.
>
> This opens [Studio](../../../../Test/Test%20from%20Studio/LangSmith%20Studio.md) with the selected assistant. When you submit an input (in **Graph** or **Chat** mode), the assistant's configuration will be applied to the run.

## Create a new version for your assistant

Updating an assistant creates a new version and sets it as the active version. All future runs that use the assistant ID use the new configuration.

> [tab] SDK
>
> Use the [`assistants.update`](https://reference.langchain.com/python/langsmith/deployment/sdk/#langgraph_sdk.client.AssistantsClient.update) method to create a new version of an assistant.
>
> > [!WARNING]
> >
> > **Updates require full configuration**
> >
> > You must provide the **entire** configuration when updating. The update endpoint creates new versions from scratch and does not merge with previous versions. Include all configuration fields you want to retain.
>
> For example, to add a system prompt to the assistant:
>
> ```python Python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Update the assistant with a new configuration
> # IMPORTANT: Include ALL configuration fields, not just the ones you're changing
> openai_assistant_v2 = await client.assistants.update(
>     openai_assistant["assistant_id"],  # Assistant ID (UUID)
>     context={
>           "model_name": "openai",  # Must include existing fields
>           "system_prompt": "You are a mindful assistant!",  # New field
>     },
> )
>
> # This creates version 2 and sets it as the active version
> # Future runs using this assistant_id will use version 2
> ```
>
> ```javascript JavaScript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // Update the assistant with a new configuration
> // IMPORTANT: Include ALL configuration fields, not just the ones you're changing
> const openaiAssistantV2 = await client.assistants.update(
>     openAIAssistant["assistant_id"],  // Assistant ID (UUID)
>     {
>         context: {
>             model_name: 'openai',  // Must include existing fields
>             system_prompt: 'You are a mindful assistant!',  // New field
>         },
>     },
> );
>
> // This creates version 2 and sets it as the active version
> // Future runs using this assistant_id will use version 2
> ```
>
> ```bash cURL theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request PATCH \
> --url <DEPLOYMENT_URL>/assistants/<ASSISTANT_ID> \
> --header 'Content-Type: application/json' \
> --data '{
> "context": {"model_name": "openai", "system_prompt": "You are a mindful assistant!"}
> }'
> ```

> [tab] UI
>
> To create a new version from the Assistants tab:
>
> 1. Navigate to your deployment and select the **Assistants** tab.
> 2. Click the assistant's row to open the **Edit assistant** pane.
> 3. Modify the assistant's name, description, or configuration.
> 4. Click **Save**.
>
> To create a new version from Studio:
>
> 1. Open Studio for the assistant.
> 2. Click **Manage Assistants**.
> 3. Edit the assistant's configuration.
> 4. Click **Save**.

## Use a previous assistant version

You can set an earlier version of an assistant as active. All future runs that use the assistant ID then use that version's configuration.

> [tab] SDK
>
> Use the `setLatest` method to change which version is active:
>
> ```python Python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> # Roll back to version 1 of the assistant
> await client.assistants.set_latest(
>     openai_assistant['assistant_id'],  # Assistant ID (UUID)
>     1  # Version number
> )
>
> # All future runs using this assistant_id will now use version 1
> ```
>
> ```javascript JavaScript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // Roll back to version 1 of the assistant
> await client.assistants.setLatest(
>     openaiAssistant['assistant_id'],  // Assistant ID (UUID)
>     1  // Version number
> );
>
> // All future runs using this assistant_id will now use version 1
> ```
>
> ```bash cURL theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
> --url <DEPLOYMENT_URL>/assistants/<ASSISTANT_ID>/latest \
> --header 'Content-Type: application/json' \
> --data '{
> "version": 1
> }'
> ```

> [tab] UI
>
> To set a previous version as active from Studio:
>
> 1. Open Studio for the assistant.
> 2. Click **Manage Assistants**.
> 3. Locate the assistant and select the version you want to use.
> 4. Toggle the **Active** switch for that version.

## Delete an assistant

Deleting an assistant permanently removes it and all of its versions. You cannot delete a single version. To stop using a version, [set a different version as active](#use-a-previous-assistant-version).

It also deletes the assistant's cron jobs and interrupts any of its runs that are in progress. The deployment keeps running. To stop it, [delete the deployment](../../../Deploy%20to%20Cloud/Deployment%20guide/Manage%20an%20Agent%20Server.md#delete-a-deployment).

> [tab] SDK
>
> Use the `assistants.delete` method to delete an assistant by its UUID. To also delete its threads, set `delete_threads` (Python) or `deleteThreads` (JavaScript) to `true`. This deletes every thread whose metadata `assistant_id` matches the assistant, along with the runs and checkpoints in those threads:
>
> ```python Python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> await client.assistants.delete(
>     openai_assistant["assistant_id"],  # Assistant ID (UUID)
>     delete_threads=True,
> )
> ```
>
> ```javascript JavaScript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> await client.assistants.delete(
>     openAIAssistant["assistant_id"],  // Assistant ID (UUID)
>     { deleteThreads: true },
> );
> ```
>
> ```bash cURL theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request DELETE \
>     --url "<DEPLOYMENT_URL>/assistants/<ASSISTANT_ID>?delete_threads=true" \
>     --header 'Content-Type: application/json'
> ```
>
> `delete_threads` defaults to `false`. If your deployment uses [custom authorization](../../Auth%20%26%20access%20control/Authentication%20%26%20access%20control.md), it deletes only the threads the caller is authorized to access.

> [tab] UI
>
> You can delete an assistant from the Assistants tab or from Studio. Deleting from the UI keeps the assistant's threads. To delete its threads as well, use the SDK with `delete_threads` set to `true`. You cannot delete the default assistant that the deployment creates for each graph.
>
> To delete an assistant from the Assistants tab:
>
> 1. Navigate to your deployment and select the **Assistants** tab.
> 2. Select the checkbox for the assistant you want to delete. You can delete one assistant at a time.
> 3. Click **Delete**.
> 4. In the confirmation dialog, click **Delete**.
>
> To delete an assistant from Studio:
>
> 1. Open Studio for the assistant.
> 2. Click **Manage Assistants**. If an assistant is selected, the button shows that assistant's name instead.
> 3. Select the assistant you want to delete, then click **Delete Assistant**.
> 4. In the confirmation dialog, click **Delete**.
