# How to use Studio

This page describes the core workflows you’ll use in Studio. It explains how to run your application, manage assistant configurations, and work with conversation threads. Each section includes steps in both graph mode (full-featured view of your graph’s execution) and chat mode (lightweight conversational interface):

* [Run application](#run-application): Execute your application or agent and observe its behavior.
* [Manage assistants](#manage-assistants): Create, edit, and select the assistant configuration used by your application.
* [Manage threads](#manage-threads): View and organize the threads, including forking or editing past runs for debugging.

## Run application

> [tab] Graph
>
> ### Specify input
>
> 1. Define the input to your graph in the **Input** section on the left side of the page, below the graph interface. Studio will attempt to render a form for your input based on the graph's defined [state schema](https://docs.langchain.com/oss/python/langgraph/graph-api.md#schema). To disable this, click the **View Raw** button, which will present you with a JSON editor.
> 2. Click the up or down arrows at the top of the **Input** section to toggle through and use previously submitted inputs.
>
> ### Run settings
>
> #### Assistant
>
> To specify the [assistant](../../Deploy/Agent%20Server/Capabilities/Assistants/Assistants.md) that is used for the run:
>
> 1. Click the **Settings** button in the bottom left corner. If an assistant is currently selected the button will also list the assistant name. If no assistant is selected it will say **Manage Assistants**.
> 2. Select the assistant to run.
> 3. Click the **Active** toggle at the top of the modal to activate it.
>
> For more information, refer to [Manage assistants](#manage-assistants).
>
> #### Streaming
>
> Click the dropdown next to **Submit** and click the toggle to enable or disable streaming.
>
> #### Breakpoints
>
> To run your graph with breakpoints:
>
> 1. Click **Interrupt**.
> 2. Select a node and whether to pause before or after that node has executed.
> 3. Click **Continue** in the thread log to resume execution.
>
> For more information on breakpoints, refer to [Human-in-the-loop](https://docs.langchain.com/oss/python/langchain/human-in-the-loop.md).
>
> ### Submit run
>
> To submit the run with the specified input and run settings:
>
> 1. Click the **Submit** button. This will add a [run](../../Deploy/Agent%20Server/Capabilities/Runs/Runs.md) to the existing selected [thread](https://docs.langchain.com/oss/python/langgraph/checkpointers.md#threads). If no thread is currently selected, a new one will be created.
> 2. To cancel the ongoing run, click the **Cancel** button.

> [tab] Chat
>
> Specify the input to your chat application in the bottom of the conversation panel.
>
> 1. Click the **Send message** button to submit the input as a Human message and have the response streamed back.
>
> To cancel the ongoing run:
>
> 1. Click **Cancel**.
> 2. Click the **Show tool calls** toggle to hide or show tool calls in the conversation.

## Manage assistants

Studio lets you view and edit your assistants, and allows you to run your graph using these assistant configurations.

For more conceptual details, refer to the [Assistants overview](../../Deploy/Agent%20Server/Capabilities/Assistants/Assistants.md).

> [tab] Graph
>
> To view your assistants:
>
> 1. Click **Manage Assistants** in the bottom left corner. This opens a modal for you to view all the assistants for the selected graph.
> 2. Specify the assistant and its version you would like to mark as **Active**. LangSmith will use this assistant when runs are submitted.
>
> The **Default configuration** option will be active, which reflects the default configuration defined in your graph. Edits made to this configuration will be used to update the run-time configuration, but will not update or create a new assistant unless you click **Create new assistant**.

> [tab] Chat
>
> Chat mode enables you to switch through the different assistants in your graph via the dropdown selector at the top of the page. To create, edit, or delete assistants, use Graph mode.

## Manage threads

Studio provides tools to view all [threads](https://docs.langchain.com/oss/python/langgraph/checkpointers.md#threads) saved on the server and edit their state. You can create new threads, switch between threads, and modify past states both in graph mode and chat mode.

> [tab] Graph
>
> ### View threads
>
> 1. In the top of the right-hand pane, select the dropdown menu to view existing threads.
> 2. Select the desired thread, and the thread history will populate in the right-hand side of the page.
> 3. To create a new thread, click **+ New Thread** and [submit a run](#run-application).
> 4. To view more granular information in the thread, drag the slider at the top of the page to the right. To view less information, drag the slider to the left. Additionally, collapse or expand individual turns, nodes, and keys of the state.
> 5. Switch between `Pretty` and `JSON` mode for different rendering formats.
>
> ### Edit thread history
>
> To edit the state of the thread:
>
> 1. Select  **Edit node state** next to the desired node.
> 2. Edit the node's output as desired and click **Fork** to confirm. This will create a new forked run from the checkpoint of the selected node.
>
> If you instead want to re-run the thread from a given checkpoint without editing the state, click **Re-run from here**. This will again create a new forked run from the selected checkpoint. This is useful for re-running with changes that are not specific to the state, such as the selected assistant.

> [tab] Chat
>
> 1. View all threads in the right-hand pane of the page.
> 2. Select the desired thread and the thread history will populate in the center panel.
> 3. To create a new thread, click **+** and submit a run.
>
> To edit a human message in the thread:
>
> 1. Click  **Edit node state** below the human message.
> 2. Edit the message as desired and submit. This will create a new fork of the conversation history.
> 3. To re-generate an AI message, click the retry icon below the AI message.

## Next steps

Refer to the following guides for more detail on tasks you can complete in Studio:

* [Iterate on prompts](Observability%20in%20Studio.md)
* [Run experiments over datasets](Observability%20in%20Studio.md#run-experiments-over-a-dataset)
