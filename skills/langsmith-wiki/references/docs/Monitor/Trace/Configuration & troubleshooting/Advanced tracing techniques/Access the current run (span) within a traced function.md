# Access the current run (span) within a traced function

In some cases you will want to access the current run (span) within a traced function. This can be useful for extracting UUIDs, tags, or other information from the current run.

You can access the current run by calling the `get_current_run_tree`/`getCurrentRunTree` function in the Python or TypeScript SDK, respectively.

For a full list of available properties on the `RunTree` object, see [this reference](../../../Debug/Data%20type%20reference/Run%20%28span%29%20data%20format.md).

```python Python
from langsmith import traceable
from langsmith.run_helpers import get_current_run_tree
from openai import Client

    openai = Client()

    @traceable
    def format_prompt(subject):
        run = get_current_run_tree()
        print(f"format_prompt Run Id: {run.id}")
        print(f"format_prompt Trace Id: {run.trace_id}")
        print(f"format_prompt Parent Run Id: {run.parent_run.id}")
        return [
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": f"What's a good name for a store that sells {subject}?"
            }
        ]

    @traceable(run_type="llm")
    def invoke_llm(messages):
        run = get_current_run_tree()
        print(f"invoke_llm Run Id: {run.id}")
        print(f"invoke_llm Trace Id: {run.trace_id}")
        print(f"invoke_llm Parent Run Id: {run.parent_run.id}")
        return openai.chat.completions.create(
            messages=messages, model="gpt-5.4-mini", temperature=0
        )

    @traceable
    def parse_output(response):
        run = get_current_run_tree()
        print(f"parse_output Run Id: {run.id}")
        print(f"parse_output Trace Id: {run.trace_id}")
        print(f"parse_output Parent Run Id: {run.parent_run.id}")
        return response.choices[0].message.content

    @traceable
    def run_pipeline():
        run = get_current_run_tree()
        print(f"run_pipeline Run Id: {run.id}")
        print(f"run_pipeline Trace Id: {run.trace_id}")
        messages = format_prompt("colorful socks")
        response = invoke_llm(messages)
        return parse_output(response)

run_pipeline()
```

```typescript TypeScript
import { traceable, getCurrentRunTree } from "langsmith/traceable";
import OpenAI from "openai";

    const openai = new OpenAI();

    const formatPrompt = traceable((subject: string) => {
        const run = getCurrentRunTree();
        console.log("formatPrompt Run ID", run.id)
        console.log("formatPrompt Trace ID", run.trace_id)
        console.log("formatPrompt Parent Run ID", run.parent_run.id)
        return [
            {
                role: "system" as const,
                content: "You are a helpful assistant.",
            },
            {
                role: "user" as const,
                content: `What's a good name for a store that sells ${subject}?`,
            },
        ];
    }, { name: "formatPrompt" });

    const invokeLLM = traceable(
        async (messages: { role: string; content: string }[]) => {
            const run = getCurrentRunTree();
            console.log("invokeLLM Run ID", run.id)
            console.log("invokeLLM Trace ID", run.trace_id)
            console.log("invokeLLM Parent Run ID", run.parent_run.id)
            return openai.chat.completions.create({
                model: "gpt-5.4-mini",
                messages: messages,
                temperature: 0,
            });
        },
        { run_type: "llm", name: "invokeLLM" }
    );

    const parseOutput = traceable(
        (response: any) => {
            const run = getCurrentRunTree();
            console.log("parseOutput Run ID", run.id)
            console.log("parseOutput Trace ID", run.trace_id)
            console.log("parseOutput Parent Run ID", run.parent_run.id)
            return response.choices[0].message.content;
        },
        { name: "parseOutput" }
    );

    const runPipeline = traceable(
        async () => {
            const run = getCurrentRunTree();
            console.log("runPipline Run ID", run.id)
            console.log("runPipline Trace ID", run.trace_id)
            console.log("runPipline Parent Run ID", run.parent_run?.id)
            const messages = await formatPrompt("colorful socks");
            const response = await invokeLLM(messages);
            return parseOutput(response);
        },
        { name: "runPipeline" }
    );

await runPipeline();
```
