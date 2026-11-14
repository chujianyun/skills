# Prompt & Context Hub

> Store, version, and update the prompts and contexts your agents use in production.

Prompts, retrieval context, skills, and task instructions change more often than the application code around them, and often need to be edited by people who are not engineers. Use the Prompt & Context Hub to store, version, review, and update the non-code parts of your agent so you can change behavior without a full deploy and let domain experts own the context they know best.

[Prompts](#prompts) are individual message templates you send to a model. [Contexts](#context-hub) are versioned bundles of instructions and tools that define a skill or a full agent, promoted through environments so your agents pull the right version.

## Prompts

> [card] [Create and update prompts](Prompts/Create%20and%20manage%20prompts/Create%20a%20prompt.md)
>
> Build prompts via the UI or SDK, configure settings, use tools, add multimodal inputs, and connect model providers.

> [card] [Manage prompts](Prompts/Create%20and%20manage%20prompts/Manage%20prompts.md)
>
> Organize with tags, commit changes, trigger webhooks, and share through the public prompt hub.

> [card] [Explore the prompt hub](Prompts/Create%20and%20manage%20prompts/Manage%20prompts.md#public-prompt-hub)
>
> Browse and manage prompt tags and discover community prompts from the LangChain Hub.

> [card] [Open the Playground](Prompts/Prompt%20engineering%20concepts.md#playground)
>
> Test and experiment with prompts using custom endpoints and model configurations.

> [card] [Follow tutorials](Tutorials/Optimize%20a%20classifier.md)
>
> Learn step-by-step techniques, like optimizing classifiers and advanced prompt engineering.

Use the **[Chat](../../Test/Datasets%20%26%20Experiments/Analyze%20experiment%20results/LangSmith%20Chat.md)** in the Playground to optimize prompts, generate tools, and create output schemas with AI-powered assistance.

## Context Hub

> [card] [Concepts](Context%20Hub/Context%20engineering%20concepts.md)
>
> Learn the core concepts of context engineering: skills, agents, versioning, and sharing.

> [card] [Use the Context Hub](Context%20Hub/Use%20the%20Context%20Hub.md)
>
> Create a context, view its files and history, and promote it to an environment.

> [card] [Manage contexts with the SDK](Context%20Hub/Manage%20contexts%20with%20the%20SDK.md)
>
> Push, pull, list, and delete agent and skill repos in the Context Hub programmatically.

> [card] [Configure commit webhooks](Context%20Hub/Configure%20Context%20Hub%20commit%20webhooks.md)
>
> Send every agent and skill commit in your workspace to an external HTTPS endpoint.

> [!NOTE]
>
> To set up a LangSmith instance, visit the [Platform setup section](../../LangSmith%20setup/Overview/Hosting/Set%20up%20LangSmith.md) to choose between cloud, hybrid, or self-hosted. All options include observability, evaluation, prompt engineering, and deployment.
