# Build a data analysis agent from scratch

> Build a data analysis agent step by step using create_agent and Deep Agents middleware.

This guide builds a data analysis agent from first principles using `create_agent` and Deep Agents middleware.

Both `create_agent` and `create_deep_agent` provide you with fine-grained control over tools, memory, and more.
The main difference between both is that Deep Agents comes with a range of commonly useful capabilities already built in, such as planning, file system tools, and subagents.
If the Deep Agents default harness does not fit your needs, this guide shows you how to start with `create_agent` and assemble the harness one piece at a time, so you can see exactly what each component adds and swap in only what your use case needs.

Follow this guide to build an agent that:

1. Accepts a CSV file for analysis
2. Writes and executes Python code in an isolated sandbox
3. Delegates visualization work to a specialized subagent
4. Loads data analysis patterns from a skills file

The final stack mirrors what `create_deep_agent` assembles by default.

## What you will learn

Each step adds one capability to the same data analysis agent:

| Step | Problem without it | What you add |
| - | - | - |
| Minimal agent | — | Baseline loop: model + tools, no harness |
| Sandbox + filesystem | Agent cannot read CSVs or run Python | Isolated [backend](https://docs.langchain.com/oss/python/deepagents/backends.md) + file and execute tools |
| Summarization | Long sessions hit context limits | Automatic history compression |
| Skills | Domain rules bloat the system prompt | On-demand expertise via [progressive disclosure](../Multi-agent/Build%20a%20SQL%20assistant%20with%20on-demand%20skills.md) |
| Subagent | Chart iteration crowds the main thread | Isolated worker + parallel delegation |

## Setup

**1. Install packages**

Install the packages for this tutorial:

```bash
pip install deepagents langsmith
```

**2. Set up LangSmith API keys**

This tutorial uses [`LangSmithSandbox`](https://reference.langchain.com/python/deepagents/backends/langsmith/LangSmithSandbox), which provisions sandboxes through `SandboxClient`. That client authenticates with LangSmith using `LANGSMITH_API_KEY` from your environment, so an API key is required to run the tutorial. Setting up LangSmith also allows you to see traces of what happens when your agent runs.

1. [Sign up for a free account](https://smith.langchain.com?utm_source=docs\&utm_medium=cta\&utm_campaign=langsmith-signup\&utm_content=oss-langchain-deep-agent-from-scratch). You can use Google, GitHub, or email.
2. [Create an API key](https://docs.langchain.com/langsmith/create-account-api-key.md) in **Settings > API Keys**.
3. Export the LangSmith API key:

```bash
export LANGSMITH_API_KEY=...
```

4. Enable tracing to inspect tool calls, middleware steps, and subagent delegation as you add each piece:

```bash
export LANGSMITH_TRACING=true
```

**3. Add a model provider API key**

Export the API key for the model provider you use in the code samples:

```bash Google
export GOOGLE_API_KEY=...
```

```bash OpenAI
export OPENAI_API_KEY=...
```

```bash Anthropic
export ANTHROPIC_API_KEY=...
```

```bash OpenRouter
export OPENROUTER_API_KEY=...
```

```bash Fireworks
export FIREWORKS_API_KEY=...
```

```bash Baseten
export BASETEN_API_KEY=...
```

```bash Ollama
# Local: Ollama must be running on your machine
# Cloud: Set your Ollama API key for hosted inference
export OLLAMA_API_KEY=...
```

## Build the agent

## Create the minimal agent

A data analysis agent needs more than a chat loop, but to begin with, start with the baseline: only a model and a loop.

Use [`create_agent`](https://reference.langchain.com/python/langchain/agents/factory/create_agent) and specify the model that you want to use:

```python Google
from langchain.agents import create_agent

agent = create_agent(model="google_genai:gemini-4-hydrogen", tools=[])
```

```python OpenAI
from langchain.agents import create_agent

agent = create_agent(model="openai:gpt-6.1-sol", tools=[])
```

```python Anthropic
from langchain.agents import create_agent

agent = create_agent(model="anthropic:claude-sonnet-5", tools=[])
```

```python OpenRouter
from langchain.agents import create_agent

agent = create_agent(model="openrouter:z-ai/glm-5.2", tools=[])
```

```python Fireworks
from langchain.agents import create_agent

agent = create_agent(model="fireworks:accounts/fireworks/models/glm-5p2", tools=[])
```

```python Baseten
from langchain.agents import create_agent

agent = create_agent(model="baseten:zai-org/GLM-5.2", tools=[])
```

```python Ollama
from langchain.agents import create_agent

agent = create_agent(model="ollama:north-mini-code-1.0", tools=[])
```

This runs, but the agent has no filesystem and no way to execute code. If you ask it to analyze a CSV, it can only guess from the prompt. The next steps add real file access and code execution.

## Add a sandbox backend

To analyze data efficiently, the agent needs to run code on files. This requires two things:

* An isolated [sandbox](https://docs.langchain.com/oss/python/deepagents/sandboxes.md) where the agent can place files and run code on the files without giving the agent access to your host machine.

* A [backend](https://docs.langchain.com/oss/python/deepagents/backends.md) which provides the file system tools to work with the sandbox (`read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`) using the [`FilesystemMiddleware`](https://reference.langchain.com/python/deepagents/middleware/filesystem/FilesystemMiddleware):\*\*. Because the `LangSmithSandbox` backend implements the sandbox protocol, [`FilesystemMiddleware`](https://reference.langchain.com/python/deepagents/middleware/filesystem/FilesystemMiddleware) also adds the `execute` tool, which allows the agent to run shell commands.

[`LangSmithSandbox`](https://reference.langchain.com/python/deepagents/backends/langsmith/LangSmithSandbox) is where files live and commands run. [`FilesystemMiddleware`](https://reference.langchain.com/python/deepagents/middleware/filesystem/FilesystemMiddleware) is what exposes that environment to the model as tools. The same middleware works with other backends if you swap the backend later.

[`LangSmithSandbox`](https://reference.langchain.com/python/deepagents/backends/langsmith/LangSmithSandbox) gives the agent an isolated environment with a filesystem and an `execute` tool for running shell commands. With it, the agent can install packages, write scripts, and run them without touching the host. To boot from a custom image instead of the default runtime, pass `snapshot_name` or `snapshot_id` to `create_sandbox()`; see [Sandbox snapshots](https://docs.langchain.com/langsmith/sandbox-snapshots.md).

Replace the agent from the previous step with one that includes [`FilesystemMiddleware`](https://reference.langchain.com/python/deepagents/middleware/filesystem/FilesystemMiddleware):

```python Google
from langchain.agents import create_agent
from deepagents.backends.langsmith import LangSmithSandbox
from deepagents.middleware import FilesystemMiddleware
from langsmith.sandbox import SandboxClient

client = SandboxClient()
sandbox = client.create_sandbox(name="langchain-docs", snapshot_name="docs-test-ci")
backend = LangSmithSandbox(sandbox=sandbox)

agent = create_agent(
    model="google_genai:gemini-4-hydrogen",
    tools=[],
    middleware=[FilesystemMiddleware(backend=backend)],
)
```

```python OpenAI
from langchain.agents import create_agent
from deepagents.backends.langsmith import LangSmithSandbox
from deepagents.middleware import FilesystemMiddleware
from langsmith.sandbox import SandboxClient

client = SandboxClient()
sandbox = client.create_sandbox(name="langchain-docs", snapshot_name="docs-test-ci")
backend = LangSmithSandbox(sandbox=sandbox)

agent = create_agent(
    model="openai:gpt-6.1-sol",
    tools=[],
    middleware=[FilesystemMiddleware(backend=backend)],
)
```

```python Anthropic
from langchain.agents import create_agent
from deepagents.backends.langsmith import LangSmithSandbox
from deepagents.middleware import FilesystemMiddleware
from langsmith.sandbox import SandboxClient

client = SandboxClient()
sandbox = client.create_sandbox(name="langchain-docs", snapshot_name="docs-test-ci")
backend = LangSmithSandbox(sandbox=sandbox)

agent = create_agent(
    model="anthropic:claude-sonnet-5",
    tools=[],
    middleware=[FilesystemMiddleware(backend=backend)],
)
```

```python OpenRouter
from langchain.agents import create_agent
from deepagents.backends.langsmith import LangSmithSandbox
from deepagents.middleware import FilesystemMiddleware
from langsmith.sandbox import SandboxClient

client = SandboxClient()
sandbox = client.create_sandbox(name="langchain-docs", snapshot_name="docs-test-ci")
backend = LangSmithSandbox(sandbox=sandbox)

agent = create_agent(
    model="openrouter:z-ai/glm-5.2",
    tools=[],
    middleware=[FilesystemMiddleware(backend=backend)],
)
```

```python Fireworks
from langchain.agents import create_agent
from deepagents.backends.langsmith import LangSmithSandbox
from deepagents.middleware import FilesystemMiddleware
from langsmith.sandbox import SandboxClient

client = SandboxClient()
sandbox = client.create_sandbox(name="langchain-docs", snapshot_name="docs-test-ci")
backend = LangSmithSandbox(sandbox=sandbox)

agent = create_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    tools=[],
    middleware=[FilesystemMiddleware(backend=backend)],
)
```

```python Baseten
from langchain.agents import create_agent
from deepagents.backends.langsmith import LangSmithSandbox
from deepagents.middleware import FilesystemMiddleware
from langsmith.sandbox import SandboxClient

client = SandboxClient()
sandbox = client.create_sandbox(name="langchain-docs", snapshot_name="docs-test-ci")
backend = LangSmithSandbox(sandbox=sandbox)

agent = create_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[],
    middleware=[FilesystemMiddleware(backend=backend)],
)
```

```python Ollama
from langchain.agents import create_agent
from deepagents.backends.langsmith import LangSmithSandbox
from deepagents.middleware import FilesystemMiddleware
from langsmith.sandbox import SandboxClient

client = SandboxClient()
sandbox = client.create_sandbox(name="langchain-docs", snapshot_name="docs-test-ci")
backend = LangSmithSandbox(sandbox=sandbox)

agent = create_agent(
    model="ollama:north-mini-code-1.0",
    tools=[],
    middleware=[FilesystemMiddleware(backend=backend)],
)
```

The sandbox filesystem is separate from your laptop. You must upload the files you need to it before you invoke the agent:

```python
import csv
import io

rows = [
    ["Date", "Product", "Units", "Revenue"],
    ["2025-08-01", "Widget A", 10, 250],
    ["2025-08-02", "Widget B", 5, 125],
    ["2025-08-03", "Widget A", 7, 175],
    ["2025-08-04", "Widget C", 3, 90],
]
buf = io.StringIO()
csv.writer(buf).writerows(rows)
backend.upload_files([("/sales.csv", buf.getvalue().encode())])

upload_stream = agent.stream_events(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Read /sales.csv and summarize total revenue by product in one "
                    "sentence. Do not run shell commands."
                ),
            }
        ]
    },
    version="v3",
    config={"recursion_limit": 8},
)
for item in upload_stream.messages:
    print(item.text)
upload_stream.output
```

> [!NOTE]
>
> With [`LangSmithSandbox`](https://reference.langchain.com/python/deepagents/backends/langsmith/LangSmithSandbox), upload paths must be absolute POSIX paths (for example, `/sales.csv`). Relative paths such as `sales.csv` are rejected with `invalid_path` and the file is not written to the sandbox.

Combine the code from the previous steps into one script and run it:

```bash
python analyze_sales.py
```

On the first run, LangSmith provisions a sandbox (this can take a few seconds). The script uploads `sales.csv`, streams the agent run, and prints assistant messages as they arrive. You should see an analysis of the sample sales data: product-level revenue, which widgets sold most, and brief trend notes. Exact wording varies by model run.

Open the run in [LangSmith](https://smith.langchain.com/?utm_source=docs\&utm_medium=cta\&utm_campaign=langsmith-signup\&utm_content=oss-langchain-deep-agent-from-scratch) and watch the agent use filesystem tools (`read_file`, and `execute` if it runs Python in the sandbox) before it replies.

## Add context management

After step 2, every tool result stays in the message history. A real analysis session (multiple plots, failed scripts, large `read_file` output) fills the context window quickly.

[`SummarizationMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/summarization/SummarizationMiddleware) compresses older turns when history grows too large, so the agent keeps working without you manually trimming messages. This matters less on the first `sales.csv` question and more on follow-ups such as "Now segment by product and plot monthly trends."

Update your agent from step 2 by adding [`SummarizationMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/summarization/SummarizationMiddleware) to the middleware list:

```python Google
from deepagents.middleware import FilesystemMiddleware, SummarizationMiddleware

model = "google_genai:gemini-4-hydrogen"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
    ],
)
```

```python OpenAI
from deepagents.middleware import FilesystemMiddleware, SummarizationMiddleware

model = "openai:gpt-6.1-sol"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
    ],
)
```

```python Anthropic
from deepagents.middleware import FilesystemMiddleware, SummarizationMiddleware

model = "anthropic:claude-sonnet-5"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
    ],
)
```

```python OpenRouter
from deepagents.middleware import FilesystemMiddleware, SummarizationMiddleware

model = "openrouter:z-ai/glm-5.2"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
    ],
)
```

```python Fireworks
from deepagents.middleware import FilesystemMiddleware, SummarizationMiddleware

model = "fireworks:accounts/fireworks/models/glm-5p2"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
    ],
)
```

```python Baseten
from deepagents.middleware import FilesystemMiddleware, SummarizationMiddleware

model = "baseten:zai-org/GLM-5.2"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
    ],
)
```

```python Ollama
from deepagents.middleware import FilesystemMiddleware, SummarizationMiddleware

model = "ollama:north-mini-code-1.0"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
    ],
)
```

Run a multi-turn session to see summarization in action. After the initial analysis, ask follow-up questions that trigger more file reads or script runs. In LangSmith, look for a summarization step before later model calls. For more information, [Context engineering](../../../Advanced%20usage/Context%20engineering%20in%20agents.md).

## Add skills

[Skills](../Multi-agent/Build%20a%20SQL%20assistant%20with%20on-demand%20skills.md) provide a way to give an agent on-demand domain knowledge when needed using progressive disclosure. Skills can include multi-step workflows, rules, and conventions. By placing this information in a skill, it isn't added to the system prompt by default which ensures the tokens are only used when the information from the skill is needed for a task.

When the agent starts, it sees only lightweight metadata about each skill. When a task needs a skill, the agent loads the full skill file on demand.

Create a skill file in a skills directory:

```
skills/
  pandas-patterns/
    SKILL.md
```

```markdown
---
name: pandas-patterns
description: Common pandas and matplotlib patterns for data analysis and visualization
---

## Data loading
Use `pd.read_csv()` for CSV files. Always check `df.info()` and `df.describe()` first.

## Visualization
Use `matplotlib` for bar charts, `seaborn` for statistical plots.
Save figures with `plt.savefig("output.png", dpi=150, bbox_inches="tight")`.

## Reporting
Write a markdown summary to `report.md` alongside any generated charts.
```

This skill contains information on how the visualization should be done.

With [`LangSmithSandbox`](https://reference.langchain.com/python/deepagents/backends/langsmith/LangSmithSandbox), skill paths resolve on the sandbox filesystem, not your local machine. Upload your local `skills/` directory before configuring [`SkillsMiddleware`](https://reference.langchain.com/python/deepagents/middleware/skills/SkillsMiddleware):

```python
from pathlib import Path

skills_dir = (Path(__file__).resolve().parent / "skills").resolve()
skill_files: list[tuple[str, bytes]] = []
for path in sorted(skills_dir.rglob("*")):
    if not path.is_file():
        continue
    rel = path.resolve().relative_to(skills_dir)
    skill_files.append((f"/skills/{rel.as_posix()}", path.read_bytes()))
backend.upload_files(skill_files)
```

Then create your agent with your skills by adding [`SkillsMiddleware`](https://reference.langchain.com/python/deepagents/middleware/skills/SkillsMiddleware):

```python Google
from deepagents.middleware import FilesystemMiddleware, SkillsMiddleware, SummarizationMiddleware

model = "google_genai:gemini-4-hydrogen"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
    ],
)
```

```python OpenAI
from deepagents.middleware import FilesystemMiddleware, SkillsMiddleware, SummarizationMiddleware

model = "openai:gpt-6.1-sol"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
    ],
)
```

```python Anthropic
from deepagents.middleware import FilesystemMiddleware, SkillsMiddleware, SummarizationMiddleware

model = "anthropic:claude-sonnet-5"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
    ],
)
```

```python OpenRouter
from deepagents.middleware import FilesystemMiddleware, SkillsMiddleware, SummarizationMiddleware

model = "openrouter:z-ai/glm-5.2"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
    ],
)
```

```python Fireworks
from deepagents.middleware import FilesystemMiddleware, SkillsMiddleware, SummarizationMiddleware

model = "fireworks:accounts/fireworks/models/glm-5p2"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
    ],
)
```

```python Baseten
from deepagents.middleware import FilesystemMiddleware, SkillsMiddleware, SummarizationMiddleware

model = "baseten:zai-org/GLM-5.2"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
    ],
)
```

```python Ollama
from deepagents.middleware import FilesystemMiddleware, SkillsMiddleware, SummarizationMiddleware

model = "ollama:north-mini-code-1.0"

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
    ],
)
```

You can try a prompt such as "Analyze sales.csv using our pandas patterns." The agent will load the skill when it needs plotting or reporting guidance. If you ask a different question that does not need the skill, the agent will not load it.

## Add a visualization subagent

Some tasks produce large intermediate output (script drafts, failed runs, file reads) that would crowd the main agent's context if kept in one thread. A [subagent](https://docs.langchain.com/oss/python/deepagents/subagents.md) runs in its own context window so the supervisor sees only the final result, not every tool call along the way. That keeps the main analysis focused and leaves room for follow-up questions.

One example where using a subagent makes sense is chart generation. Plotting often means iterating on Python scripts, installing packages, and reading error output before a figure is ready. The following `visualizer` subagent can handle that work in isolation while the main agent continues planning and analysis. With [`TodoListMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/todo/TodoListMiddleware), the main agent can also delegate that chart work in parallel instead of blocking on each plot.

Update your agent from step 4 by adding [`TodoListMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/todo/TodoListMiddleware) and [`SubAgentMiddleware`](https://reference.langchain.com/python/deepagents/middleware/subagents/SubAgentMiddleware):

```python Google
from deepagents import SubAgent
from deepagents.middleware import (
    FilesystemMiddleware,
    SkillsMiddleware,
    SubAgentMiddleware,
    SummarizationMiddleware,
)
from langchain.agents.middleware import TodoListMiddleware

model = "google_genai:gemini-4-hydrogen"

visualizer: SubAgent = {
    "name": "visualizer",
    "description": "Generates charts and visualizations from data files in the sandbox.",
    "system_prompt": "You are a data visualization specialist. Write Python scripts using matplotlib and seaborn. Save all figures as PNG files.",
    "tools": [],
    "model": model,
}

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
        TodoListMiddleware(),
        SubAgentMiddleware(backend=backend, subagents=[visualizer]),
    ],
)
```

```python OpenAI
from deepagents import SubAgent
from deepagents.middleware import (
    FilesystemMiddleware,
    SkillsMiddleware,
    SubAgentMiddleware,
    SummarizationMiddleware,
)
from langchain.agents.middleware import TodoListMiddleware

model = "openai:gpt-6.1-sol"

visualizer: SubAgent = {
    "name": "visualizer",
    "description": "Generates charts and visualizations from data files in the sandbox.",
    "system_prompt": "You are a data visualization specialist. Write Python scripts using matplotlib and seaborn. Save all figures as PNG files.",
    "tools": [],
    "model": model,
}

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
        TodoListMiddleware(),
        SubAgentMiddleware(backend=backend, subagents=[visualizer]),
    ],
)
```

```python Anthropic
from deepagents import SubAgent
from deepagents.middleware import (
    FilesystemMiddleware,
    SkillsMiddleware,
    SubAgentMiddleware,
    SummarizationMiddleware,
)
from langchain.agents.middleware import TodoListMiddleware

model = "anthropic:claude-sonnet-5"

visualizer: SubAgent = {
    "name": "visualizer",
    "description": "Generates charts and visualizations from data files in the sandbox.",
    "system_prompt": "You are a data visualization specialist. Write Python scripts using matplotlib and seaborn. Save all figures as PNG files.",
    "tools": [],
    "model": model,
}

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
        TodoListMiddleware(),
        SubAgentMiddleware(backend=backend, subagents=[visualizer]),
    ],
)
```

```python OpenRouter
from deepagents import SubAgent
from deepagents.middleware import (
    FilesystemMiddleware,
    SkillsMiddleware,
    SubAgentMiddleware,
    SummarizationMiddleware,
)
from langchain.agents.middleware import TodoListMiddleware

model = "openrouter:z-ai/glm-5.2"

visualizer: SubAgent = {
    "name": "visualizer",
    "description": "Generates charts and visualizations from data files in the sandbox.",
    "system_prompt": "You are a data visualization specialist. Write Python scripts using matplotlib and seaborn. Save all figures as PNG files.",
    "tools": [],
    "model": model,
}

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
        TodoListMiddleware(),
        SubAgentMiddleware(backend=backend, subagents=[visualizer]),
    ],
)
```

```python Fireworks
from deepagents import SubAgent
from deepagents.middleware import (
    FilesystemMiddleware,
    SkillsMiddleware,
    SubAgentMiddleware,
    SummarizationMiddleware,
)
from langchain.agents.middleware import TodoListMiddleware

model = "fireworks:accounts/fireworks/models/glm-5p2"

visualizer: SubAgent = {
    "name": "visualizer",
    "description": "Generates charts and visualizations from data files in the sandbox.",
    "system_prompt": "You are a data visualization specialist. Write Python scripts using matplotlib and seaborn. Save all figures as PNG files.",
    "tools": [],
    "model": model,
}

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
        TodoListMiddleware(),
        SubAgentMiddleware(backend=backend, subagents=[visualizer]),
    ],
)
```

```python Baseten
from deepagents import SubAgent
from deepagents.middleware import (
    FilesystemMiddleware,
    SkillsMiddleware,
    SubAgentMiddleware,
    SummarizationMiddleware,
)
from langchain.agents.middleware import TodoListMiddleware

model = "baseten:zai-org/GLM-5.2"

visualizer: SubAgent = {
    "name": "visualizer",
    "description": "Generates charts and visualizations from data files in the sandbox.",
    "system_prompt": "You are a data visualization specialist. Write Python scripts using matplotlib and seaborn. Save all figures as PNG files.",
    "tools": [],
    "model": model,
}

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
        TodoListMiddleware(),
        SubAgentMiddleware(backend=backend, subagents=[visualizer]),
    ],
)
```

```python Ollama
from deepagents import SubAgent
from deepagents.middleware import (
    FilesystemMiddleware,
    SkillsMiddleware,
    SubAgentMiddleware,
    SummarizationMiddleware,
)
from langchain.agents.middleware import TodoListMiddleware

model = "ollama:north-mini-code-1.0"

visualizer: SubAgent = {
    "name": "visualizer",
    "description": "Generates charts and visualizations from data files in the sandbox.",
    "system_prompt": "You are a data visualization specialist. Write Python scripts using matplotlib and seaborn. Save all figures as PNG files.",
    "tools": [],
    "model": model,
}

agent = create_agent(
    model=model,
    tools=[],
    middleware=[
        FilesystemMiddleware(backend=backend),
        SummarizationMiddleware(model=model, backend=backend),
        SkillsMiddleware(backend=backend, sources=["/skills/"]),
        TodoListMiddleware(),
        SubAgentMiddleware(backend=backend, subagents=[visualizer]),
    ],
)
```

Try a prompt such as "Analyze sales.csv, then create a bar chart of revenue by product." The main agent handles analysis and planning and delegates chart generation to the `visualizer` subagent via the `task` tool.

If you enabled tracing in [Setup](#setup), open the run in [LangSmith](https://smith.langchain.com/?utm_source=docs\&utm_medium=cta\&utm_campaign=langsmith-signup\&utm_content=oss-langchain-deep-agent-from-scratch). You should see a `task` call to `visualizer`, a separate sub-run with its own tool loop, and a short result returned to the supervisor.

## What you built

You've built a customized agent with the following middleware:

| Middleware | What it adds |
| - | - |
| [`FilesystemMiddleware`](https://reference.langchain.com/python/deepagents/middleware/filesystem/FilesystemMiddleware) + `LangSmithSandbox` | Isolated filesystem + `execute` tool |
| [`SummarizationMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/summarization/SummarizationMiddleware) | Automatic context compression |
| [`SkillsMiddleware`](https://reference.langchain.com/python/deepagents/middleware/skills/SkillsMiddleware) | Domain knowledge loaded on demand |
| [`TodoListMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/todo/TodoListMiddleware) + [`SubAgentMiddleware`](https://reference.langchain.com/python/deepagents/middleware/subagents/SubAgentMiddleware) | Parallel visualization subagent |

This is the same foundation as [`create_deep_agent`](https://reference.langchain.com/python/deepagents/graph/create_deep_agent): assembled manually so you control exactly what's included.

The possibilities don't end here: see [Prebuilt middleware](../../../Middleware/Prebuilt%20middleware.md) for the full list of composable capabilities, and the [`create_agent`](https://reference.langchain.com/python/langchain/agents/factory/create_agent) reference for all configuration options.

To work with the pre-assembled version, see [Customize Deep Agents](https://docs.langchain.com/oss/python/deepagents/customization.md). For the full data analysis example using `create_deep_agent`, see [Data analysis](https://docs.langchain.com/oss/python/deepagents/data-analysis.md).

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/deep-agent-from-scratch.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
