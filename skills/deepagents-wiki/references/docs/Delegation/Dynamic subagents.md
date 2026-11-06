# Dynamic subagents

> Use interpreters to dispatch and orchestrate Deep Agents subagents from code

Dynamic subagents let an agent dispatch [subagents](Subagents.md) from interpreter code. Instead of asking the model to choose one subagent call at a time, the agent can use JavaScript loops, branches, and parallel batches to route work across configured subagents and synthesize the results.

Use this pattern when work spans many independent units, needs multiple perspectives, or benefits from recursive analysis. For general interpreter setup, see [Interpreters](../Execution%20environment/Interpreters.md).

> [!WARNING]
>
> Dynamic subagents use the interpreter runtime, which is in [**beta**](https://docs.langchain.com/oss/python/versioning.md). APIs and lifecycle behavior may change between releases.

> [!NOTE]
>
> Interpreters require `langchain-quickjs>=0.2.0` and Python 3.11 or later.

## Quickstart

Dynamic subagents require [interpreter](../Execution%20environment/Interpreters.md) middleware. Install and wire up the interpreter first. The built-in [general-purpose subagent](Subagents.md#default-subagent) handles basic fan-out without extra configuration.

```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    subagents=[{
        "name": "reviewer",
        "description": "Reviews code for security issues, citing lines and severity",
        "system_prompt": "You are a security-focused code reviewer. Report issues with line numbers and severity.",
    }],
    middleware=[CodeInterpreterMiddleware()],
)
```

```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="openai:gpt-5.5",
    subagents=[{
        "name": "reviewer",
        "description": "Reviews code for security issues, citing lines and severity",
        "system_prompt": "You are a security-focused code reviewer. Report issues with line numbers and severity.",
    }],
    middleware=[CodeInterpreterMiddleware()],
)
```

```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="anthropic:claude-sonnet-5",
    subagents=[{
        "name": "reviewer",
        "description": "Reviews code for security issues, citing lines and severity",
        "system_prompt": "You are a security-focused code reviewer. Report issues with line numbers and severity.",
    }],
    middleware=[CodeInterpreterMiddleware()],
)
```

```python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="openrouter:z-ai/glm-5.2",
    subagents=[{
        "name": "reviewer",
        "description": "Reviews code for security issues, citing lines and severity",
        "system_prompt": "You are a security-focused code reviewer. Report issues with line numbers and severity.",
    }],
    middleware=[CodeInterpreterMiddleware()],
)
```

```python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    subagents=[{
        "name": "reviewer",
        "description": "Reviews code for security issues, citing lines and severity",
        "system_prompt": "You are a security-focused code reviewer. Report issues with line numbers and severity.",
    }],
    middleware=[CodeInterpreterMiddleware()],
)
```

```python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="baseten:zai-org/GLM-5.2",
    subagents=[{
        "name": "reviewer",
        "description": "Reviews code for security issues, citing lines and severity",
        "system_prompt": "You are a security-focused code reviewer. Report issues with line numbers and severity.",
    }],
    middleware=[CodeInterpreterMiddleware()],
)
```

```python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="ollama:north-mini-code-1.0",
    subagents=[{
        "name": "reviewer",
        "description": "Reviews code for security issues, citing lines and severity",
        "system_prompt": "You are a security-focused code reviewer. Report issues with line numbers and severity.",
    }],
    middleware=[CodeInterpreterMiddleware()],
)
```

For install steps and interpreter setup, see [Interpreters](../Execution%20environment/Interpreters.md#quickstart).

For specialized work, configure custom [subagents](Subagents.md) with their own names, descriptions, and system prompts. The subagents' names and descriptions serve as information for the agent to evaluate which role to reach for.

To trigger dynamic subagents, prompt the agent with the word "workflow":

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
result = agent.invoke({
    "messages": [{"role": "user", "content": "Run a workflow that reviews every file in src/routes/ and summarizes the top risks."}]
})
```

> [!TIP]
>
> **The word "workflow" is a useful trigger.** The interpreter system prompt treats "workflow" as a signal to organize work through the interpreter, dispatching subagents with `task()` from code rather than grinding through items one model-chosen tool call at a time. Phrasing a request as a "workflow" is a deliberate lever you can pull to opt into dynamic orchestration. For a single, direct delegation, phrase the request plainly instead.

> [!NOTE]
>
> Using dynamic subagents with `dcode`, the LangChain terminal coding agent? `dcode` ships with the code interpreter enabled, so dynamic subagents work out of the box. See the [dcode subagents page](https://docs.langchain.com/oss/deepagents/code/subagents.md) for setup and usage details.

## How it works

When an agent has [subagents](Subagents.md) and interpreter middleware, the interpreter exposes a built-in `task()` global that dispatches subagents from code. A task spanning many independent units (reviewing every file in a directory, triaging a batch of tickets) becomes a loop that fans the work out, so it runs deterministically instead of one model-chosen tool call at a time.

Subagent orchestration also supports recursive language model (RLM) workflows, the approach described in the [Recursive Language Models paper](https://arxiv.org/abs/2512.24601): keep the working set in interpreter variables, select slices, call subagents with `task()`, and synthesize the results.

Many orchestration workflows combine dynamic subagents with [programmatic tool calling (PTC)](../Execution%20environment/Interpreters.md#programmatic-tool-calling-ptc): use `tools.*` from interpreter code to discover or filter inputs, then dispatch subagents with `task()`. PTC is off by default; enable it with an explicit allowlist on interpreter middleware.

`task()` is a capability bridge into subagent execution, similar to PTC for tools. For isolation defaults, approval boundaries, and middleware options, see [Security](../Execution%20environment/Interpreters.md#security) and [Configuration](../Execution%20environment/Interpreters.md#configuration).

> [!NOTE]
>
> Multi-turn orchestration can persist interpreter variables across agent turns when using `mode="thread"` (the default). See [Persistence](../Execution%20environment/Interpreters.md#persistence) on the interpreters page.

`task()` takes the following inputs:

* `description`: The prompt for the subagent
* `subagentType`: Which configured subagent to run
* `responseSchema` (optional): Structured output

A `task()` runs a full agentic loop and resolves to the subagent's result:

```ts theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
const review = await task({
  description: "Review src/auth/login.ts for auth issues. Cite line numbers.",
  subagentType: "reviewer",
  responseSchema: {
    type: "object",
    properties: {
      issues: { type: "array", items: { type: "object", properties: {
        file: { type: "string" }, line: { type: "number" },
        severity: { type: "string" }, description: { type: "string" },
      }}},
    },
  },
});

// With responseSchema, the result is already a typed value, so no JSON.parse is needed.
const critical = review.issues.filter((issue) => issue.severity === "high");
```

When you pass `responseSchema`, the resolved value is already a typed JavaScript object; only call `JSON.parse` if a subagent intentionally returned a JSON string.

## Patterns

The agent picks a strategy from the shape of the task; these emerge from how it writes interpreter code, not from configuration, and the subagents you make available determine what it can do. Every pattern shares the same orchestration approach: hold work in JS variables, dispatch subagents with `task()`, and combine results in code. The diagrams below show the common shapes, each with a runnable example.

### Classify and act

Items are classified first, then each item is handled by a specialized subagent based on its classification. This lets you process mixed inputs where different items need different expertise.

```mermaid theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
graph LR
    Task[Task] --> Classify{Classifier}
    Classify --> |bug| A[Agent A]
    Classify --> |feature| B[Agent B]
    Classify --> |question| C[Agent C]
```

**Use cases:** Triaging support tickets, error logs, user feedback, or any batch of items that need different handling depending on their type.

> [accordion] Example: classify and act
>
> **What you configure**
>
> ```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="google_genai:gemini-3.6-flash",
>     subagents=[
>         {
>             "name": "bug-fixer",
>             "description": "Investigates bug reports and provides reproduction steps",
>             "system_prompt": "You are a bug triage specialist. Investigate each bug report and provide clear reproduction steps.",
>         },
>         {
>             "name": "feature-analyst",
>             "description": "Evaluates feature requests for feasibility and effort",
>             "system_prompt": "You are a product analyst. Evaluate each feature request for technical feasibility, estimated effort, and potential impact.",
>         },
>         {
>             "name": "support-agent",
>             "description": "Answers user questions based on documentation",
>             "system_prompt": "You are a support specialist. Answer user questions clearly based on the available documentation.",
>         },
>     ],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="openai:gpt-5.5",
>     subagents=[
>         {
>             "name": "bug-fixer",
>             "description": "Investigates bug reports and provides reproduction steps",
>             "system_prompt": "You are a bug triage specialist. Investigate each bug report and provide clear reproduction steps.",
>         },
>         {
>             "name": "feature-analyst",
>             "description": "Evaluates feature requests for feasibility and effort",
>             "system_prompt": "You are a product analyst. Evaluate each feature request for technical feasibility, estimated effort, and potential impact.",
>         },
>         {
>             "name": "support-agent",
>             "description": "Answers user questions based on documentation",
>             "system_prompt": "You are a support specialist. Answer user questions clearly based on the available documentation.",
>         },
>     ],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="anthropic:claude-sonnet-5",
>     subagents=[
>         {
>             "name": "bug-fixer",
>             "description": "Investigates bug reports and provides reproduction steps",
>             "system_prompt": "You are a bug triage specialist. Investigate each bug report and provide clear reproduction steps.",
>         },
>         {
>             "name": "feature-analyst",
>             "description": "Evaluates feature requests for feasibility and effort",
>             "system_prompt": "You are a product analyst. Evaluate each feature request for technical feasibility, estimated effort, and potential impact.",
>         },
>         {
>             "name": "support-agent",
>             "description": "Answers user questions based on documentation",
>             "system_prompt": "You are a support specialist. Answer user questions clearly based on the available documentation.",
>         },
>     ],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="openrouter:z-ai/glm-5.2",
>     subagents=[
>         {
>             "name": "bug-fixer",
>             "description": "Investigates bug reports and provides reproduction steps",
>             "system_prompt": "You are a bug triage specialist. Investigate each bug report and provide clear reproduction steps.",
>         },
>         {
>             "name": "feature-analyst",
>             "description": "Evaluates feature requests for feasibility and effort",
>             "system_prompt": "You are a product analyst. Evaluate each feature request for technical feasibility, estimated effort, and potential impact.",
>         },
>         {
>             "name": "support-agent",
>             "description": "Answers user questions based on documentation",
>             "system_prompt": "You are a support specialist. Answer user questions clearly based on the available documentation.",
>         },
>     ],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="fireworks:accounts/fireworks/models/glm-5p2",
>     subagents=[
>         {
>             "name": "bug-fixer",
>             "description": "Investigates bug reports and provides reproduction steps",
>             "system_prompt": "You are a bug triage specialist. Investigate each bug report and provide clear reproduction steps.",
>         },
>         {
>             "name": "feature-analyst",
>             "description": "Evaluates feature requests for feasibility and effort",
>             "system_prompt": "You are a product analyst. Evaluate each feature request for technical feasibility, estimated effort, and potential impact.",
>         },
>         {
>             "name": "support-agent",
>             "description": "Answers user questions based on documentation",
>             "system_prompt": "You are a support specialist. Answer user questions clearly based on the available documentation.",
>         },
>     ],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="baseten:zai-org/GLM-5.2",
>     subagents=[
>         {
>             "name": "bug-fixer",
>             "description": "Investigates bug reports and provides reproduction steps",
>             "system_prompt": "You are a bug triage specialist. Investigate each bug report and provide clear reproduction steps.",
>         },
>         {
>             "name": "feature-analyst",
>             "description": "Evaluates feature requests for feasibility and effort",
>             "system_prompt": "You are a product analyst. Evaluate each feature request for technical feasibility, estimated effort, and potential impact.",
>         },
>         {
>             "name": "support-agent",
>             "description": "Answers user questions based on documentation",
>             "system_prompt": "You are a support specialist. Answer user questions clearly based on the available documentation.",
>         },
>     ],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="ollama:north-mini-code-1.0",
>     subagents=[
>         {
>             "name": "bug-fixer",
>             "description": "Investigates bug reports and provides reproduction steps",
>             "system_prompt": "You are a bug triage specialist. Investigate each bug report and provide clear reproduction steps.",
>         },
>         {
>             "name": "feature-analyst",
>             "description": "Evaluates feature requests for feasibility and effort",
>             "system_prompt": "You are a product analyst. Evaluate each feature request for technical feasibility, estimated effort, and potential impact.",
>         },
>         {
>             "name": "support-agent",
>             "description": "Answers user questions based on documentation",
>             "system_prompt": "You are a support specialist. Answer user questions clearly based on the available documentation.",
>         },
>     ],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> **What the agent writes**
>
> ```ts theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // The agent has already classified each ticket; this routes every item to
> // the right specialist and collects the handled results.
> const SPECIALIST = { bug: "bug-fixer", feature: "feature-analyst", question: "support-agent" };
>
> const handled = await Promise.all(
>   tickets.map((ticket) =>
>     task({
>       description: `Handle this ${ticket.category}:\n${ticket.text}`,
>       subagentType: SPECIALIST[ticket.category],
>     }),
>   ),
> );
> // ... group handled results by category into a single triage report
> handled;
> ```

### Fan-out and synthesize

The agent dispatches the same kind of work across many items in parallel, then combines the results.

```mermaid theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
graph LR
    Items[Items] --> W1[Worker]
    Items --> W2[Worker]
    Items --> W3[Worker]
    W1 --> Collect[Collect]
    W2 --> Collect
    W3 --> Collect
    Collect --> Synth[Synthesize]
```

**Use cases:** Code review across a directory, analyzing a batch of documents, processing log files, running the same check across many services.

Discovering files from interpreter code requires [programmatic tool calling (PTC)](../Execution%20environment/Interpreters.md#programmatic-tool-calling-ptc). Enable `glob` in the PTC allowlist on interpreter middleware.

> [accordion] Example: fan-out and synthesize
>
> **What you configure**
>
> ```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="google_genai:gemini-3.6-flash",
>     subagents=[{
>         "name": "reviewer",
>         "description": "Reviews code for security issues, citing lines and severity",
>         "system_prompt": "You are a security-focused code reviewer. Read the file carefully and report any authentication or authorization issues with line numbers and severity.",
>     }],
>     middleware=[CodeInterpreterMiddleware(ptc=["glob"])],
> )
> ```
>
> ```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="openai:gpt-5.5",
>     subagents=[{
>         "name": "reviewer",
>         "description": "Reviews code for security issues, citing lines and severity",
>         "system_prompt": "You are a security-focused code reviewer. Read the file carefully and report any authentication or authorization issues with line numbers and severity.",
>     }],
>     middleware=[CodeInterpreterMiddleware(ptc=["glob"])],
> )
> ```
>
> ```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="anthropic:claude-sonnet-5",
>     subagents=[{
>         "name": "reviewer",
>         "description": "Reviews code for security issues, citing lines and severity",
>         "system_prompt": "You are a security-focused code reviewer. Read the file carefully and report any authentication or authorization issues with line numbers and severity.",
>     }],
>     middleware=[CodeInterpreterMiddleware(ptc=["glob"])],
> )
> ```
>
> ```python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="openrouter:z-ai/glm-5.2",
>     subagents=[{
>         "name": "reviewer",
>         "description": "Reviews code for security issues, citing lines and severity",
>         "system_prompt": "You are a security-focused code reviewer. Read the file carefully and report any authentication or authorization issues with line numbers and severity.",
>     }],
>     middleware=[CodeInterpreterMiddleware(ptc=["glob"])],
> )
> ```
>
> ```python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="fireworks:accounts/fireworks/models/glm-5p2",
>     subagents=[{
>         "name": "reviewer",
>         "description": "Reviews code for security issues, citing lines and severity",
>         "system_prompt": "You are a security-focused code reviewer. Read the file carefully and report any authentication or authorization issues with line numbers and severity.",
>     }],
>     middleware=[CodeInterpreterMiddleware(ptc=["glob"])],
> )
> ```
>
> ```python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="baseten:zai-org/GLM-5.2",
>     subagents=[{
>         "name": "reviewer",
>         "description": "Reviews code for security issues, citing lines and severity",
>         "system_prompt": "You are a security-focused code reviewer. Read the file carefully and report any authentication or authorization issues with line numbers and severity.",
>     }],
>     middleware=[CodeInterpreterMiddleware(ptc=["glob"])],
> )
> ```
>
> ```python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="ollama:north-mini-code-1.0",
>     subagents=[{
>         "name": "reviewer",
>         "description": "Reviews code for security issues, citing lines and severity",
>         "system_prompt": "You are a security-focused code reviewer. Read the file carefully and report any authentication or authorization issues with line numbers and severity.",
>     }],
>     middleware=[CodeInterpreterMiddleware(ptc=["glob"])],
> )
> ```
>
> **What the agent writes**
>
> ```ts theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // One reviewer per file, dispatched in parallel, then findings merged.
> const files = (await tools.glob({ pattern: "src/routes/**/*.ts" }))
>   .split("\n")
>   .filter(Boolean);
>
> const reviews = await Promise.all(
>   files.map((file) =>
>     task({
>       description: `Review ${file} for authentication issues. Cite line numbers.`,
>       subagentType: "reviewer",
>       responseSchema: issuesSchema, // -> { issues: [{ file, line, severity }] }
>     }),
>   ),
> );
>
> const issues = reviews.flatMap((r) => r.issues);
> // ... sort by severity, drop duplicates, summarize the top risks
> issues;
> ```

### Adversarial verification

A two-pass pattern. The first pass produces findings. The second pass sends each finding to independent verifiers, and only findings that survive agreement are kept. This reduces false positives when confidence matters more than speed.

```mermaid theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
graph LR
    Items[Items] --> Workers[Workers]
    Workers --> Findings[Findings]
    Findings --> V1[Verifier]
    Findings --> V2[Verifier]
    Findings --> V3[Verifier]
    V1 --> Vote[Majority vote]
    V2 --> Vote
    V3 --> Vote
    Vote --> Confirmed[Confirmed]
```

**Use cases:** Security audits where false positives are costly, compliance checks, any review where you need high confidence in findings.

> [accordion] Example: adversarial verification
>
> **What you configure**
>
> ```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="google_genai:gemini-3.6-flash",
>     subagents=[
>         {
>             "name": "reviewer",
>             "description": "Finds potential security vulnerabilities in code",
>             "system_prompt": "You are a security auditor. Find potential vulnerabilities and report each with file, line, and description.",
>         },
>         {
>             "name": "verifier",
>             "description": "Independently verifies whether a reported vulnerability is real",
>             "system_prompt": "You are a security verification specialist. Given a reported vulnerability, independently verify whether it is exploitable. Be skeptical. Only confirm real issues.",
>         },
>     ],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="openai:gpt-5.5",
>     subagents=[
>         {
>             "name": "reviewer",
>             "description": "Finds potential security vulnerabilities in code",
>             "system_prompt": "You are a security auditor. Find potential vulnerabilities and report each with file, line, and description.",
>         },
>         {
>             "name": "verifier",
>             "description": "Independently verifies whether a reported vulnerability is real",
>             "system_prompt": "You are a security verification specialist. Given a reported vulnerability, independently verify whether it is exploitable. Be skeptical. Only confirm real issues.",
>         },
>     ],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="anthropic:claude-sonnet-5",
>     subagents=[
>         {
>             "name": "reviewer",
>             "description": "Finds potential security vulnerabilities in code",
>             "system_prompt": "You are a security auditor. Find potential vulnerabilities and report each with file, line, and description.",
>         },
>         {
>             "name": "verifier",
>             "description": "Independently verifies whether a reported vulnerability is real",
>             "system_prompt": "You are a security verification specialist. Given a reported vulnerability, independently verify whether it is exploitable. Be skeptical. Only confirm real issues.",
>         },
>     ],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="openrouter:z-ai/glm-5.2",
>     subagents=[
>         {
>             "name": "reviewer",
>             "description": "Finds potential security vulnerabilities in code",
>             "system_prompt": "You are a security auditor. Find potential vulnerabilities and report each with file, line, and description.",
>         },
>         {
>             "name": "verifier",
>             "description": "Independently verifies whether a reported vulnerability is real",
>             "system_prompt": "You are a security verification specialist. Given a reported vulnerability, independently verify whether it is exploitable. Be skeptical. Only confirm real issues.",
>         },
>     ],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="fireworks:accounts/fireworks/models/glm-5p2",
>     subagents=[
>         {
>             "name": "reviewer",
>             "description": "Finds potential security vulnerabilities in code",
>             "system_prompt": "You are a security auditor. Find potential vulnerabilities and report each with file, line, and description.",
>         },
>         {
>             "name": "verifier",
>             "description": "Independently verifies whether a reported vulnerability is real",
>             "system_prompt": "You are a security verification specialist. Given a reported vulnerability, independently verify whether it is exploitable. Be skeptical. Only confirm real issues.",
>         },
>     ],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="baseten:zai-org/GLM-5.2",
>     subagents=[
>         {
>             "name": "reviewer",
>             "description": "Finds potential security vulnerabilities in code",
>             "system_prompt": "You are a security auditor. Find potential vulnerabilities and report each with file, line, and description.",
>         },
>         {
>             "name": "verifier",
>             "description": "Independently verifies whether a reported vulnerability is real",
>             "system_prompt": "You are a security verification specialist. Given a reported vulnerability, independently verify whether it is exploitable. Be skeptical. Only confirm real issues.",
>         },
>     ],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="ollama:north-mini-code-1.0",
>     subagents=[
>         {
>             "name": "reviewer",
>             "description": "Finds potential security vulnerabilities in code",
>             "system_prompt": "You are a security auditor. Find potential vulnerabilities and report each with file, line, and description.",
>         },
>         {
>             "name": "verifier",
>             "description": "Independently verifies whether a reported vulnerability is real",
>             "system_prompt": "You are a security verification specialist. Given a reported vulnerability, independently verify whether it is exploitable. Be skeptical. Only confirm real issues.",
>         },
>     ],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> **What the agent writes**
>
> ```ts theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // Pass 1: audit. Pass 2: verify each finding independently; keep only confirmed.
> const { findings } = await task({
>   description: "Audit the payments module for vulnerabilities.",
>   subagentType: "reviewer",
>   responseSchema: findingsSchema, // -> { findings: [{ id, file, line, description }] }
> });
>
> const verdicts = await Promise.all(
>   findings.map((f) =>
>     task({
>       description: `Verify ${f.file}:${f.line} (${f.description}). Confirm or refute.`,
>       subagentType: "verifier",
>       responseSchema: verdictSchema, // -> { confirmed: boolean }
>     }),
>   ),
> );
>
> const confirmed = findings.filter((_, i) => verdicts[i]?.confirmed);
> // ... report only the confirmed vulnerabilities
> confirmed;
> ```

### Generate and filter

Multiple subagents generate independent solutions to the same problem. The agent compares, scores, and filters the results in code, keeping only the best.

```mermaid theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
graph LR
    Prompt[Prompt] --> G1[Generator]
    Prompt --> G2[Generator]
    Prompt --> G3[Generator]
    G1 --> Filter[Filter + rank]
    G2 --> Filter
    G3 --> Filter
    Filter --> Best[Best result]
```

**Use cases:** Architecture proposals, refactoring strategies, content variations, any task where exploring multiple options before committing produces a better outcome.

> [accordion] Example: generate and filter
>
> **What you configure**
>
> ```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="google_genai:gemini-3.6-flash",
>     subagents=[{
>         "name": "architect",
>         "description": "Proposes a database schema design with tradeoff analysis",
>         "system_prompt": "You are a database architect. Propose a schema design for the given requirements. Include tradeoffs, migration considerations, and a clear rationale.",
>     }],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="openai:gpt-5.5",
>     subagents=[{
>         "name": "architect",
>         "description": "Proposes a database schema design with tradeoff analysis",
>         "system_prompt": "You are a database architect. Propose a schema design for the given requirements. Include tradeoffs, migration considerations, and a clear rationale.",
>     }],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="anthropic:claude-sonnet-5",
>     subagents=[{
>         "name": "architect",
>         "description": "Proposes a database schema design with tradeoff analysis",
>         "system_prompt": "You are a database architect. Propose a schema design for the given requirements. Include tradeoffs, migration considerations, and a clear rationale.",
>     }],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="openrouter:z-ai/glm-5.2",
>     subagents=[{
>         "name": "architect",
>         "description": "Proposes a database schema design with tradeoff analysis",
>         "system_prompt": "You are a database architect. Propose a schema design for the given requirements. Include tradeoffs, migration considerations, and a clear rationale.",
>     }],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="fireworks:accounts/fireworks/models/glm-5p2",
>     subagents=[{
>         "name": "architect",
>         "description": "Proposes a database schema design with tradeoff analysis",
>         "system_prompt": "You are a database architect. Propose a schema design for the given requirements. Include tradeoffs, migration considerations, and a clear rationale.",
>     }],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="baseten:zai-org/GLM-5.2",
>     subagents=[{
>         "name": "architect",
>         "description": "Proposes a database schema design with tradeoff analysis",
>         "system_prompt": "You are a database architect. Propose a schema design for the given requirements. Include tradeoffs, migration considerations, and a clear rationale.",
>     }],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="ollama:north-mini-code-1.0",
>     subagents=[{
>         "name": "architect",
>         "description": "Proposes a database schema design with tradeoff analysis",
>         "system_prompt": "You are a database architect. Propose a schema design for the given requirements. Include tradeoffs, migration considerations, and a clear rationale.",
>     }],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> **What the agent writes**
>
> ```ts theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // Generate independent proposals in parallel, then score and keep the best.
> const proposals = await Promise.all(
>   [1, 2, 3].map((n) =>
>     task({
>       description: `Approach ${n}: redesign the orders schema, with tradeoffs.`,
>       subagentType: "architect",
>       responseSchema: designSchema, // -> { design, tradeoffs }
>     }),
>   ),
> );
>
> // ... score each proposal against the requirements
> const best = proposals.sort((a, b) => score(b) - score(a))[0];
> best;
> ```

### Tournament

Variations are compared head-to-head by a judge subagent, with winners advancing through elimination rounds.

```mermaid theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
graph LR
    A1[Attempt] --> J1{Judge}
    A2[Attempt] --> J1
    A3[Attempt] --> J2{Judge}
    A4[Attempt] --> J2
    J1 --> JF{Final}
    J2 --> JF
    JF --> Winner[Winner]
```

**Use cases:** Optimization under subjective criteria, style selection, choosing between competing implementations.

> [accordion] Example: tournament
>
> **What you configure**
>
> ```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="google_genai:gemini-3.6-flash",
>     subagents=[
>         {
>             "name": "writer",
>             "description": "Rewrites a function with a focus on readability and clarity",
>             "system_prompt": "You are an expert programmer focused on clean code. Rewrite the given function to maximize readability. Explain your choices.",
>         },
>         {
>             "name": "judge",
>             "description": "Compares two code implementations and picks the more readable one",
>             "system_prompt": "You are a code quality judge. Compare two implementations and pick the more readable one. Justify your choice with specific criteria.",
>         },
>     ],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="openai:gpt-5.5",
>     subagents=[
>         {
>             "name": "writer",
>             "description": "Rewrites a function with a focus on readability and clarity",
>             "system_prompt": "You are an expert programmer focused on clean code. Rewrite the given function to maximize readability. Explain your choices.",
>         },
>         {
>             "name": "judge",
>             "description": "Compares two code implementations and picks the more readable one",
>             "system_prompt": "You are a code quality judge. Compare two implementations and pick the more readable one. Justify your choice with specific criteria.",
>         },
>     ],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="anthropic:claude-sonnet-5",
>     subagents=[
>         {
>             "name": "writer",
>             "description": "Rewrites a function with a focus on readability and clarity",
>             "system_prompt": "You are an expert programmer focused on clean code. Rewrite the given function to maximize readability. Explain your choices.",
>         },
>         {
>             "name": "judge",
>             "description": "Compares two code implementations and picks the more readable one",
>             "system_prompt": "You are a code quality judge. Compare two implementations and pick the more readable one. Justify your choice with specific criteria.",
>         },
>     ],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="openrouter:z-ai/glm-5.2",
>     subagents=[
>         {
>             "name": "writer",
>             "description": "Rewrites a function with a focus on readability and clarity",
>             "system_prompt": "You are an expert programmer focused on clean code. Rewrite the given function to maximize readability. Explain your choices.",
>         },
>         {
>             "name": "judge",
>             "description": "Compares two code implementations and picks the more readable one",
>             "system_prompt": "You are a code quality judge. Compare two implementations and pick the more readable one. Justify your choice with specific criteria.",
>         },
>     ],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="fireworks:accounts/fireworks/models/glm-5p2",
>     subagents=[
>         {
>             "name": "writer",
>             "description": "Rewrites a function with a focus on readability and clarity",
>             "system_prompt": "You are an expert programmer focused on clean code. Rewrite the given function to maximize readability. Explain your choices.",
>         },
>         {
>             "name": "judge",
>             "description": "Compares two code implementations and picks the more readable one",
>             "system_prompt": "You are a code quality judge. Compare two implementations and pick the more readable one. Justify your choice with specific criteria.",
>         },
>     ],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="baseten:zai-org/GLM-5.2",
>     subagents=[
>         {
>             "name": "writer",
>             "description": "Rewrites a function with a focus on readability and clarity",
>             "system_prompt": "You are an expert programmer focused on clean code. Rewrite the given function to maximize readability. Explain your choices.",
>         },
>         {
>             "name": "judge",
>             "description": "Compares two code implementations and picks the more readable one",
>             "system_prompt": "You are a code quality judge. Compare two implementations and pick the more readable one. Justify your choice with specific criteria.",
>         },
>     ],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="ollama:north-mini-code-1.0",
>     subagents=[
>         {
>             "name": "writer",
>             "description": "Rewrites a function with a focus on readability and clarity",
>             "system_prompt": "You are an expert programmer focused on clean code. Rewrite the given function to maximize readability. Explain your choices.",
>         },
>         {
>             "name": "judge",
>             "description": "Compares two code implementations and picks the more readable one",
>             "system_prompt": "You are a code quality judge. Compare two implementations and pick the more readable one. Justify your choice with specific criteria.",
>         },
>     ],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> **What the agent writes**
>
> ```ts theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // Generate variants, then judge pairwise until a single winner remains.
> let bracket = await Promise.all(
>   [1, 2, 3, 4, 5].map((n) =>
>     task({ description: `Rewrite processOrder for readability (variant ${n}).`, subagentType: "writer" }),
>   ),
> );
>
> while (bracket.length > 1) {
>   const winners = [];
>   for (let i = 0; i < bracket.length; i += 2) {
>     if (bracket[i + 1] === undefined) { winners.push(bracket[i]); break; }
>     const { winner } = await task({
>       description: `Pick the more readable:\n\nA:\n${bracket[i]}\n\nB:\n${bracket[i + 1]}`,
>       subagentType: "judge",
>       responseSchema: pickSchema, // -> { winner: "A" | "B" }
>     });
>     winners.push(winner === "A" ? bracket[i] : bracket[i + 1]);
>   }
>   bracket = winners;
> }
> bracket[0]; // the winning rewrite
> ```

### Loop until done

The agent runs a discovery loop, deduplicating against what it has already found, until no new results appear. Useful when the scope of the work is not known upfront.

```mermaid theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
graph LR
    Agent[Agent] --> Check{New findings?}
    Check --> |yes| Agent
    Check --> |no| Done[Done]
```

**Use cases:** Exhaustive search, dead code detection, dependency audits, any sweep where you want completeness rather than a fixed number of results.

> [accordion] Example: loop until done
>
> **What you configure**
>
> ```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="google_genai:gemini-3.6-flash",
>     subagents=[{
>         "name": "analyzer",
>         "description": "Analyzes code for unused exports, functions, and dead code paths",
>         "system_prompt": "You are a code analyst specializing in dead code detection. Find unused exports, unreachable functions, and orphaned modules. Report each with file path and evidence.",
>     }],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="openai:gpt-5.5",
>     subagents=[{
>         "name": "analyzer",
>         "description": "Analyzes code for unused exports, functions, and dead code paths",
>         "system_prompt": "You are a code analyst specializing in dead code detection. Find unused exports, unreachable functions, and orphaned modules. Report each with file path and evidence.",
>     }],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="anthropic:claude-sonnet-5",
>     subagents=[{
>         "name": "analyzer",
>         "description": "Analyzes code for unused exports, functions, and dead code paths",
>         "system_prompt": "You are a code analyst specializing in dead code detection. Find unused exports, unreachable functions, and orphaned modules. Report each with file path and evidence.",
>     }],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="openrouter:z-ai/glm-5.2",
>     subagents=[{
>         "name": "analyzer",
>         "description": "Analyzes code for unused exports, functions, and dead code paths",
>         "system_prompt": "You are a code analyst specializing in dead code detection. Find unused exports, unreachable functions, and orphaned modules. Report each with file path and evidence.",
>     }],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="fireworks:accounts/fireworks/models/glm-5p2",
>     subagents=[{
>         "name": "analyzer",
>         "description": "Analyzes code for unused exports, functions, and dead code paths",
>         "system_prompt": "You are a code analyst specializing in dead code detection. Find unused exports, unreachable functions, and orphaned modules. Report each with file path and evidence.",
>     }],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="baseten:zai-org/GLM-5.2",
>     subagents=[{
>         "name": "analyzer",
>         "description": "Analyzes code for unused exports, functions, and dead code paths",
>         "system_prompt": "You are a code analyst specializing in dead code detection. Find unused exports, unreachable functions, and orphaned modules. Report each with file path and evidence.",
>     }],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> ```python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from deepagents import create_deep_agent
> from langchain_quickjs import CodeInterpreterMiddleware
>
> agent = create_deep_agent(
>     model="ollama:north-mini-code-1.0",
>     subagents=[{
>         "name": "analyzer",
>         "description": "Analyzes code for unused exports, functions, and dead code paths",
>         "system_prompt": "You are a code analyst specializing in dead code detection. Find unused exports, unreachable functions, and orphaned modules. Report each with file path and evidence.",
>     }],
>     middleware=[CodeInterpreterMiddleware()],
> )
> ```
>
> **What the agent writes**
>
> ```ts theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // Keep dispatching rounds, deduping against what's found, until a round adds nothing.
> const seen = new Set();
> const found = [];
>
> while (true) {
>   const { items } = await task({
>     description: `Find dead code. Already found: ${[...seen].join(", ") || "(none)"}.`,
>     subagentType: "analyzer",
>     responseSchema: itemsSchema, // -> { items: [{ id, file }] }
>   });
>   const fresh = items.filter((i) => !seen.has(i.id));
>   if (fresh.length === 0) break; // converged: nothing new
>   for (const i of fresh) { seen.add(i.id); found.push(i); }
> }
> found;
> ```

> [!WARNING]
>
> `task()` dispatches from inside an already-running `eval` call. It does not go through the normal tool calling path, so `interrupt_on` approval workflows on the parent agent are not enforced per dispatch. Gate the `eval` tool itself if you need approval before subagent orchestration runs.

## Disable dynamic subagents

Subagent dispatch is on by default whenever the agent has subagents. Disable it if you want subagents to be available only through the normal `task` tool path. For other middleware options, see [Configuration](../Execution%20environment/Interpreters.md#configuration) on the interpreters page.

```python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    subagents=[{"name": "reviewer", "description": "Reviews code", "system_prompt": "Review code."}],
    middleware=[CodeInterpreterMiddleware(subagents=False)],
)
```

```python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="openai:gpt-5.5",
    subagents=[{"name": "reviewer", "description": "Reviews code", "system_prompt": "Review code."}],
    middleware=[CodeInterpreterMiddleware(subagents=False)],
)
```

```python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="anthropic:claude-sonnet-5",
    subagents=[{"name": "reviewer", "description": "Reviews code", "system_prompt": "Review code."}],
    middleware=[CodeInterpreterMiddleware(subagents=False)],
)
```

```python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="openrouter:z-ai/glm-5.2",
    subagents=[{"name": "reviewer", "description": "Reviews code", "system_prompt": "Review code."}],
    middleware=[CodeInterpreterMiddleware(subagents=False)],
)
```

```python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="fireworks:accounts/fireworks/models/glm-5p2",
    subagents=[{"name": "reviewer", "description": "Reviews code", "system_prompt": "Review code."}],
    middleware=[CodeInterpreterMiddleware(subagents=False)],
)
```

```python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="baseten:zai-org/GLM-5.2",
    subagents=[{"name": "reviewer", "description": "Reviews code", "system_prompt": "Review code."}],
    middleware=[CodeInterpreterMiddleware(subagents=False)],
)
```

```python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="ollama:north-mini-code-1.0",
    subagents=[{"name": "reviewer", "description": "Reviews code", "system_prompt": "Review code."}],
    middleware=[CodeInterpreterMiddleware(subagents=False)],
)
```

## See also

* [Interpreters](../Execution%20environment/Interpreters.md): QuickJS setup, programmatic tool calling, persistence, security, and middleware configuration
* [Subagents](Subagents.md): Configure subagent names, descriptions, and system prompts
* [Event streaming](../Execution%20environment/Event%20streaming.md): Stream updates from the coordinator and delegated subagents

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/deepagents/dynamic-subagents.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
