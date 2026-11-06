# Build checklist for the Functional API

> Decide how to compose entrypoints, tasks, streaming, interrupts, and memory with the Functional API.

This guide walks through the decisions you make when building with the Functional API. For install and an end-to-end agent example, see the [LangGraph quickstart](../../Get%20started/Quickstart.md). For a design walkthrough, see [Thinking in the Functional API](Thinking%20in%20the%20Functional%20API.md). For concepts, see the [Functional API overview](Functional%20API%20overview.md). To choose between the Graph API and the Functional API, see [Choosing between Graph and Functional APIs](../../Get%20started/Choosing%20between%20Graph%20and%20Functional%20APIs.md).

## Build your workflow

Work through these decisions in order. Each step links to the how-to for full recipes.

**1. Compose the workflow**

Define an entrypoint, wrap units of work in tasks, and choose how steps connect.

* Start from a single entrypoint and pass inputs as one argument (often a dict).
* Use tasks for discrete work that should checkpoint and retry independently.
* Fan out with parallel tasks when steps are independent.
* Call a compiled [Graph API](../../Build%20with%20the%20Graph%20API/Graph%20API%20overview.md) graph or another entrypoint when you need composition.

See [Compose Functional API workflows](Compose%20Functional%20API%20workflows.md).

**2. Configure tasks**

Add reliability controls when steps can fail, hang, or repeat.

* Retries for transient failures
* Timeouts for slow tasks or entrypoints
* Caching for expensive repeated work
* Resume after an error without redoing completed tasks

See [Configure Functional API tasks](Configure%20Functional%20API%20tasks.md).

**3. Stream progress**

Stream updates, model tokens, or custom data while the workflow runs.

See [Stream with the Functional API](Stream%20with%20the%20Functional%20API.md).

**4. Add human-in-the-loop**

Pause for approval or tool-call review with interrupts, then resume with `Command`.

See [Add human-in-the-loop with the Functional API](Add%20human-in-the-loop%20with%20the%20Functional%20API.md).

**5. Add memory**

Keep short-term thread state with a checkpointer, and long-term data with a store.

See [Add memory with the Functional API](Add%20memory%20with%20the%20Functional%20API.md).

## Next steps

* [Thinking in the Functional API](Thinking%20in%20the%20Functional%20API.md)
* [Functional API overview](Functional%20API%20overview.md)
* [Compose Functional API workflows](Compose%20Functional%20API%20workflows.md)
* [Configure Functional API tasks](Configure%20Functional%20API%20tasks.md)
* [Stream with the Functional API](Stream%20with%20the%20Functional%20API.md)
* [Add human-in-the-loop with the Functional API](Add%20human-in-the-loop%20with%20the%20Functional%20API.md)
* [Add memory with the Functional API](Add%20memory%20with%20the%20Functional%20API.md)
* [LangGraph quickstart](../../Get%20started/Quickstart.md)
* [Choosing between Graph and Functional APIs](../../Get%20started/Choosing%20between%20Graph%20and%20Functional%20APIs.md)
