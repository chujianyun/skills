# Manage evaluators with the SDK

> Create, retrieve, update, list, and delete LangSmith evaluators programmatically with the SDK.

Use the LangSmith SDK to create and manage [evaluators](../Get%20started/Evaluation%20concepts.md#evaluators) programmatically. Evaluators created through the SDK are [workspace-level](../../LangSmith%20setup/Govern/Organization/Overview.md#workspaces) resources that appear in the **Evaluators** table in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-manage-evaluators-sdk), the same as [evaluators created in the UI](Manage%20evaluators.md#create-an-evaluator-in-the-ui). You can attach them to datasets to run [offline evaluations](../Get%20started/Evaluation%20concepts.md#offline-evaluations) and to tracing projects to run [online evaluations](../Get%20started/Evaluation%20concepts.md#online-evaluations). Use the SDK to automate evaluator management and integrate evaluation into your existing workflows.

## Prerequisites

Managing evaluators through the SDK requires:

* Python: `langsmith>=0.9.8` (PyPI)
* TypeScript: `langsmith>=0.7.16` (npm)

> [!NOTE]
>
> For installation and setup, refer to the [Python SDK documentation](../../Monitor/Reference/langsmith%20%28smith-python-sdk%29.md) and [TypeScript SDK documentation](https://reference.langchain.com/javascript/modules/langsmith.html).

The examples on this page initialize the client with no arguments, so it reads the `LANGSMITH_API_KEY` and `LANGSMITH_ENDPOINT` environment variables. Configure your [API key](../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md) through environment variables rather than hardcoding it.

In the following examples, replace placeholders such as `<evaluator-uuid>` with the corresponding information from LangSmith. All Python async examples on this page assume they run inside `async def main(): ... asyncio.run(main())`, as shown in the create a code evaluator example.

## Create an evaluator

### Code evaluator

A code evaluator scores each run or example with a function that you define.

```python Python
import asyncio

from langsmith import Client


async def main():
    client = Client()

    created = await client.evaluators.create(
        name="Correctness evaluator",
        type="code",
        code_evaluator={
            "code": "def perform_eval(run, example):\n    return {'score': 1}",
            "language": "python",
        },
    )
    evaluator_id = created.evaluator.id
    print("Created evaluator:", evaluator_id)


asyncio.run(main())
```

```typescript TypeScript
import { Client } from "langsmith";

const client = new Client();

const created = await client.evaluators.create({
  name: "Correctness evaluator",
  type: "code",
  code_evaluator: {
    code: "def perform_eval(run, example):\n    return {'score': 1}",
    language: "python",
  },
});
const evaluatorId = created.evaluator?.id;
console.log("Created evaluator:", evaluatorId);
```

### LLM-as-a-judge evaluator

An LLM-as-a-judge evaluator references a prompt from the [prompt hub](../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Prompt%20engineering%20quickstart.md) and maps your run or example fields to the prompt variables.

> [!NOTE]
>
> The prompt must be a structured prompt (type `StructuredPrompt`). A `StructuredPrompt` combines a prompt template with an output schema, ensuring the model returns data in a defined structure.

```python Python
import asyncio

from langsmith import Client


async def main():
    client = Client()

    created = await client.evaluators.create(
        name="LLM judge",
        type="llm",
        llm_evaluator={
            "prompt_repo_handle": "<prompt-repo-handle>",
            "commit_hash_or_tag": "<commit-hash-or-tag>",
            "variable_mapping": {
                "input": "inputs.question",
                "output": "outputs.answer",
                "reference": "reference.answer",
            },
        },
    )
    evaluator_id = created.evaluator.id


asyncio.run(main())
```

```typescript TypeScript
const created = await client.evaluators.create({
  name: "LLM judge",
  type: "llm",
  llm_evaluator: {
    prompt_repo_handle: "<prompt-repo-handle>",
    commit_hash_or_tag: "<commit-hash-or-tag>",
    variable_mapping: {
      input: "inputs.question",
      output: "outputs.answer",
      reference: "reference.answer",
    },
  },
});
const evaluatorId = created.evaluator?.id;
```

The `prompt_repo_handle` is the prompt's internal repository name, not its display title or URL. To find it, list your workspace prompts and read the `repo_handle` field, or retrieve a specific prompt by its identifier in LangSmith. The identifier of a prompt can be in the format:

* `promptName` (for private prompts), for example `my-prompt`.
* `owner/promptName` (for public prompts), for example `langchain-ai/correctness`.

```python Python
# List workspace prompts and read each repo handle
for prompt in client.list_prompts(limit=10).repos:
    print("prompt-repo-handle:", prompt.repo_handle)   # value to use for prompt_repo_handle
    print("prompt-full-name:", prompt.full_name)     # display name
    print("description:", prompt.description)

# Or retrieve a specific prompt by identifier
prompt = client.get_prompt("<prompt-identifier>")
print("prompt-repo-handle:", prompt.repo_handle)
```

```typescript TypeScript
// List workspace prompts and read each repo handle.
// listPrompts() has no `limit` option in this SDK version — it's an async
// generator over all prompts, so cap the count client-side and break.
const prompts = client.listPrompts();
let count = 0;
for await (const prompt of prompts) {
  console.log("prompt-repo-handle:", prompt.repo_handle);
  console.log("prompt-full-name:", prompt.full_name);
  console.log("description:", prompt.description);
  console.log("---");
  if (++count >= 10) break; // first 10 only; stops further pagination
}

// Or retrieve a specific prompt by identifier
const prompt = await client.getPrompt("<prompt-identifier>");
console.log("prompt-repo-handle:", prompt.repo_handle);
```

## Retrieve an evaluator

Fetch a single evaluator by its ID to read its configuration, including its name, type, feedback keys, and run rules.

```python Python
import asyncio

from langsmith import Client


async def main():
    client = Client()
    evaluator_id = "<evaluator-uuid>"

    evaluator = await client.evaluators.retrieve(evaluator_id)
    print(evaluator.name)
    print(evaluator.type)
    print(evaluator.feedback_keys)
    print(evaluator.run_rules)


asyncio.run(main())
```

```typescript TypeScript
const evaluator = await client.evaluators.retrieve(evaluatorId);
console.log(evaluator.name);
console.log(evaluator.type);
console.log(evaluator.feedback_keys);
console.log(evaluator.run_rules);
```

## Update an evaluator

Pass the field that matches the evaluator type: `code_evaluator` for a code evaluator or `llm_evaluator` for an LLM-as-a-judge evaluator. `update` changes only the fields you pass.

```python Python
import asyncio

from langsmith import Client


async def main():
    client = Client()

    # Update a code evaluator
    code_evaluator_id = "<code-evaluator-uuid>"

    updated = await client.evaluators.update(
        code_evaluator_id,
        name="Updated correctness evaluator",
        code_evaluator={
            "code": "def perform_eval(run, example):\n    return {'score': 0.8}",
            "language": "python",
        },
    )
    print(updated.evaluator.name if updated.evaluator else None)

    # Update the name and prompt of an LLM-as-a-judge evaluator
    llm_evaluator_id = "<llm-evaluator-uuid>"

    await client.evaluators.update(
        llm_evaluator_id,
        name="Updated LLM judge",
        llm_evaluator={
            "prompt_repo_handle": "<prompt-repo-handle>",
            "commit_hash_or_tag": "<commit-hash-or-tag>",
        },
    )


asyncio.run(main())
```

```typescript TypeScript
// Update a code evaluator
const codeEvaluatorId = "<code-evaluator-uuid>";

const updated = await client.evaluators.update(codeEvaluatorId, {
  name: "Updated correctness evaluator",
  code_evaluator: {
    code: "def perform_eval(run, example):\n    return {'score': 0.8}",
    language: "python",
  },
});
console.log(updated.evaluator?.name);

// Update the name and prompt of an LLM-as-a-judge evaluator
const llmEvaluatorId = "<llm-evaluator-uuid>";

await client.evaluators.update(llmEvaluatorId, {
  name: "Updated LLM judge",
  llm_evaluator: {
    prompt_repo_handle: "<prompt-repo-handle>",
    commit_hash_or_tag: "<commit-hash-or-tag>",
  },
});
```

### Configure runtime settings

An LLM-as-a-judge evaluator accepts additional settings that control how it scores traces:

* **`variable_mapping`**: Maps run or example fields to the judge prompt variables. It applies when the evaluator runs.
* **`use_corrections_dataset`** and **`num_few_shot_examples`**: Enable few-shot learning from human score corrections. They apply only when the evaluator is attached to a project or dataset and corrections have been submitted.

> [!NOTE]
>
> These settings take effect on the next evaluation run, not when you call `update`.

```python Python
import asyncio

from langsmith import Client


async def main():
    client = Client()
    llm_evaluator_id = "<llm-evaluator-uuid>"

    await client.evaluators.update(
        llm_evaluator_id,
        llm_evaluator={
            "prompt_repo_handle": "<prompt-repo-handle>",
            "commit_hash_or_tag": "<commit-hash-or-tag>",
            "variable_mapping": {
                "input": "inputs.question",
                "output": "outputs.answer",
            },
            "use_corrections_dataset": True,
            "num_few_shot_examples": 3,
        },
    )


asyncio.run(main())
```

```typescript TypeScript
const llmEvaluatorId = "<llm-evaluator-uuid>";

await client.evaluators.update(llmEvaluatorId, {
  llm_evaluator: {
    prompt_repo_handle: "<prompt-repo-handle>",
    commit_hash_or_tag: "<commit-hash-or-tag>",
    variable_mapping: {
      input: "inputs.question",
      output: "outputs.answer",
    },
    use_corrections_dataset: true,
    num_few_shot_examples: 3,
  },
});
```

## List evaluators

Filter by name, type, feedback key, attached resource, or tag value, and sort or paginate the results. `list()` auto-paginates through every match when you iterate the returned object directly. `limit` sets the per-request page size (1 to 100), not the total number of results. `sort_by` is optional, accepts `created_at` or `updated_at`, and defaults to `created_at`.

```python Python
import asyncio

from langsmith import Client


async def main():
    client = Client()

    # Read a single page of results
    page = await client.evaluators.list(
        name_contains="correctness",
        type="code",
        limit=10,
    )
    for evaluator in page.evaluators:
        print(evaluator.id, evaluator.name, evaluator.type)

    # Collect every match into a list
    evaluators = [
        evaluator
        async for evaluator in client.evaluators.list(feedback_key="correctness", limit=20)
    ]

    # Filter, sort, and paginate
    page = await client.evaluators.list(
        feedback_key="correctness",
        name_contains="judge",
        resource_id=["<project-or-dataset-uuid>"],
        tag_value_id=["<tag-value-uuid>"],
        type="llm",
        sort_by="updated_at",  # "created_at" (default) or "updated_at"
        sort_by_desc=False,
        limit=20,
        offset=0,
    )


asyncio.run(main())
```

```typescript TypeScript
// Read a single page of results
const page = await client.evaluators.list({
  name_contains: "correctness",
  type: "code",
  limit: 10,
});
for (const evaluator of page.evaluators) {
  console.log(evaluator.id, evaluator.name, evaluator.type);
}

// Collect every match into an array
const evaluators = [];
for await (const evaluator of client.evaluators.list({
  feedback_key: "correctness",
  limit: 20,
})) {
  evaluators.push(evaluator);
}

// Filter, sort, and paginate
await client.evaluators.list({
  feedback_key: "correctness",
  name_contains: "judge",
  resource_id: ["<project-or-dataset-uuid>"],
  tag_value_id: ["<tag-value-uuid>"],
  type: "llm",
  sort_by: "updated_at", // "created_at" (default) or "updated_at"
  sort_by_desc: false,
  limit: 20,
  offset: 0,
});
```

## Track evaluator spend

Retrieve estimated USD spend and trace counts for your evaluators:

* **`period_start`**: A date-only ISO string, such as `2026-06-29`. Passing a datetime returns a 400 error.
  * **Window**: `period_start` starts a fixed 7-day window that includes `period_start` and the six days after it. The window is half-open, `[period_start, period_start + 7 days)`, so `period_end` (`period_start` plus 7 days) is excluded. For example, a `period_start` of `2026-06-29` covers `2026-06-29` through `2026-07-05`, and `2026-07-06` is excluded.
* **`type`**: Scopes results to a single evaluator type, `llm` or `code`. Omit it to include all types.
* **Empty result**: If no spend is recorded for the window, the returned `groups` list is empty.

> [!NOTE]
>
> Pass exactly one of `group_by`, `evaluator_id`, `session_id` (the LangSmith tracing project UUID), or `dataset_id`.

```python Python
import asyncio

from langsmith import Client


async def main():
    client = Client()
    evaluator_uuid = "<evaluator-uuid>"
    start_date = "<period-start-date>" # for example, "2026-06-29"

    # Spend for a single evaluator
    spend = await client.evaluators.spend(
        period_start=start_date,
        evaluator_id=evaluator_uuid,
    )
    for group in spend.groups or []:
        print(group.evaluator_name, group.total_spend_usd, group.total_trace_count)

    # Group spend by evaluator
    spend_by_evaluator = await client.evaluators.spend(
        period_start=start_date,
        group_by="evaluator",
        type="llm",
    )
    print("Group by evaluator")
    for group in spend_by_evaluator.groups or []:
        print(group.evaluator_name, group.total_spend_usd, group.total_trace_count)

    # Group spend by resource
    spend_by_resource = await client.evaluators.spend(
        period_start=start_date,
        group_by="resource",
        type="llm",
    )
    print("Group by resource")
    for group in spend_by_resource.groups or []:
        print(group.session_name, group.dataset_name, group.total_spend_usd, group.total_trace_count)

    # Group spend by run_rule
    spend_by_run_rule = await client.evaluators.spend(
        period_start=start_date,
        group_by="run_rule",
        type="llm",
    )
    print("Group by run_rule")
    for group in spend_by_run_rule.groups or []:
        print(group.run_rule_name, group.total_spend_usd, group.total_trace_count)


asyncio.run(main())
```

```typescript TypeScript
const evaluatorUUID = "<evaluator-uuid>";
const startDate = "<period-start-date>"; // for example, "2026-06-29"

// Spend for a single evaluator
const spend = await client.evaluators.spend({
  period_start: startDate,
  evaluator_id: evaluatorUUID,
});
for (const group of spend.groups ?? []) {
  console.log(group.evaluator_name, group.total_spend_usd, group.total_trace_count);
}

// Group spend by evaluator
const spendByEvaluator = await client.evaluators.spend({
  period_start: startDate,
  group_by: "evaluator",
  type: "llm",
});
console.log("Group by evaluator");
for (const group of spendByEvaluator.groups ?? []) {
  console.log(group.evaluator_name, group.total_spend_usd, group.total_trace_count);
}

// Group spend by resource
const spendByResource = await client.evaluators.spend({
  period_start: startDate,
  group_by: "resource",
  type: "llm",
});
console.log("Group by resource");
for (const group of spendByResource.groups ?? []) {
  console.log(group.session_name, group.dataset_name, group.total_spend_usd, group.total_trace_count);
}

// Group spend by run_rule
const spendByRunRule = await client.evaluators.spend({
  period_start: startDate,
  group_by: "run_rule",
  type: "llm",
});
console.log("Group by run_rule");
for (const group of spendByRunRule.groups ?? []) {
  console.log(group.run_rule_name, group.total_spend_usd, group.total_trace_count);
}
```

## Delete an evaluator

You cannot delete an evaluator while it is attached to a tracing project, an agent environment, or a dataset. Set `delete_run_rules` to `true` to delete the run rules that reference the evaluator before deleting the evaluator.

```python Python
import asyncio

from langsmith import Client


async def main():
    client = Client()
    evaluator_id = "<evaluator-uuid>"

    await client.evaluators.delete(
        evaluator_id,
        delete_run_rules=True, # run rules referencing the evaluator are deleted first
    )


asyncio.run(main())
```

```typescript TypeScript
const evaluatorId = "<evaluator-uuid>";

await client.evaluators.delete(evaluatorId, {
  delete_run_rules: true, // run rules referencing the evaluator are deleted first
});
```

## Related

* [Manage evaluators](Manage%20evaluators.md): View and manage evaluators in the LangSmith UI.
* [Set up LLM-as-a-judge online evaluators](../../Monitor/Observe/Online%20evaluators/Set%20up%20LLM-as-a-judge%20online%20evaluators.md): Configure LLM-as-a-judge online evaluators in the LangSmith UI.
* [Set up online code evaluators](../../Monitor/Observe/Online%20evaluators/Set%20up%20online%20code%20evaluators.md): Configure online code evaluators in the LangSmith UI.
