# Quickstart

> Build your first agent in minutes

This quickstart shows you how to create a fully functional AI agent in just a few minutes.

Build the LangChain quickstart agent

Build a basic LangChain agent in this working directory by following the LangChain quickstart.

## Step 1: Read the guide

Detect whether this project uses Python or TypeScript/JavaScript. Fetch and follow the matching page; treat it as the source of truth for package names, model strings, and code:

* Python: [https://docs.langchain.com/oss/python/langchain/quickstart.md](Quickstart.md)
* TypeScript: [https://docs.langchain.com/oss/javascript/langchain/quickstart.md](https://docs.langchain.com/oss/javascript/langchain/quickstart.md)

## Step 2: Install dependencies

Install the packages from the guide with the package manager already used in this project (`uv`, `pip`, `npm`, `pnpm`, `yarn`, or `bun`). Prefer pinning current stable versions over a floating `latest` tag when the project already pins versions.

## Step 3: Configure model credentials

Check whether a supported provider API key is already set (for example `OPENAI_API_KEY`, `GOOGLE_API_KEY`, or `ANTHROPIC_API_KEY`). If none is set, ask the user which provider to use, then stop and wait while they create a key and set it in the shell or a `.env` file. Do not invent, hardcode, or commit API keys.

## Step 4: Implement the basic agent

Create the "Build a basic agent" example from the guide: `create_agent`, a simple tool such as `get_weather`, a short system prompt, and an `invoke` call. Use a model string for the provider the user chose. Print the final message content (Python: `.content_blocks`) so the user can verify the run.

## Step 5: Optional LangSmith tracing

Ask the user if they want tracing. If yes, follow [https://docs.langchain.com/langsmith/create-an-agent](https://docs.langchain.com/langsmith/create-an-agent.md) to register an agent in an agent-based workspace. Have them set `LANGSMITH_AGENT_ID`, `LANGSMITH_AGENT_ENVIRONMENT`, `LANGSMITH_TRACING=true`, and `LANGSMITH_API_KEY`, then re-run. Do not invent a LangSmith key.

## Rules

* Stay scoped to this quickstart. Do not add unrelated frameworks, evals, or production deployment.
* Prefer `create_agent` from `langchain.agents` / `langchain` as shown in the guide.
* Ask rather than guess when a secret, provider choice, or project convention is unclear.

> [!TIP]
>
> **Using an AI coding assistant?**
>
> * Install the [LangChain Docs MCP servers](https://docs.langchain.com/use-these-docs.md) to give your agent access to up-to-date LangChain documentation and examples.
>
>   Connect LangChain docs MCP servers
>
>   Connect both LangChain documentation MCP servers to my coding agent so it can look up current LangChain, LangGraph, and LangSmith docs and API reference.
>
>   Servers to add:
>
>   * `docs-langchain`: [https://docs.langchain.com/mcp](https://docs.langchain.com/mcp)
>   * `reference-langchain`: [https://reference.langchain.com/mcp](https://reference.langchain.com/mcp)
>
>   Detect which agent or editor I am using (Claude Code, Cursor, Codex CLI, Claude Desktop, Deep Agents Code, VS Code, Antigravity, or another MCP-compatible client). Use the matching setup from [https://docs.langchain.com/use-these-docs.md](https://docs.langchain.com/use-these-docs.md):
>
>   * Claude Code: `claude mcp add --transport http` for each server (project scope by default; use `--scope user` only if I ask for global access).
>   * Codex CLI: `codex mcp add` with each server URL.
>   * Cursor, Deep Agents Code, VS Code, or Antigravity: merge both entries into the MCP settings JSON using the field names shown on that page for my client.
>   * Claude Desktop: add both URLs under Settings > Connectors.
>
>   Do not invent alternate MCP URLs. After configuring, confirm both servers are listed and reachable.
> * Install [LangChain Skills](https://github.com/langchain-ai/langchain-skills) to improve your agent's performance on LangChain ecosystem tasks.
>
>   Install LangChain Skills
>
>   Install LangChain Skills for my coding agent so it can perform better on LangChain, LangGraph, and Deep Agents tasks.
>
>   Use the Agent Skills installer from [https://github.com/langchain-ai/langchain-skills](https://github.com/langchain-ai/langchain-skills):
>
>   ```bash
>   npx skills add langchain-ai/langchain-skills --skill '*' --yes
>   ```
>
>   If I ask for a global install instead, use:
>
>   ```bash
>   npx skills add langchain-ai/langchain-skills --skill '*' --yes --global
>   ```
>
>   Detect which agent or editor I am using. If I use Claude Code and prefer the plugin path, follow the marketplace install from that repository README (`/plugin marketplace add` then `/plugin install`). Do not invent alternate skill package names or install URLs. After installing, confirm the skills are available to the agent.

## Install dependencies

Install the following packages to follow along:

```bash uv
uv python pin 3.11
uv init
uv add langchain
uv sync
```

```bash pip
# Install Python 3.11+ separately if needed.
pip install -U langchain
```

```bash venv
# Install Python 3.11+ separately if needed.
python3.11 -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -U langchain
```

## Set up API keys

Get an API key from [any supported model provider](https://docs.langchain.com/oss/python/integrations/providers/overview.md) (for example, Google Gemini or OpenAI).

Set the API keys in your shell or in a `.env` file, for example:

> [tab] OpenAI
>
> ```bash Shell
> export OPENAI_API_KEY="<API_KEY>"
> ```
>
> ```bash .env
> OPENAI_API_KEY=your-api-key
> ```

> [tab] Google Gemini
>
> ```bash Shell
> export GOOGLE_API_KEY="<API_KEY>"
> ```
>
> ```bash .env
> GOOGLE_API_KEY=your-api-key
> ```

> [tab] Claude (Anthropic)
>
> ```bash Shell
> export ANTHROPIC_API_KEY="<API_KEY>"
> ```
>
> ```bash .env
> ANTHROPIC_API_KEY=your-api-key
> ```

> [tab] OpenRouter
>
> ```bash Shell
> export OPENROUTER_API_KEY="<API_KEY>"
> ```
>
> ```bash .env
> OPENROUTER_API_KEY=your-api-key
> ```

> [tab] Fireworks
>
> ```bash Shell
> export FIREWORKS_API_KEY="<API_KEY>"
> ```
>
> ```bash .env
> FIREWORKS_API_KEY=your-api-key
> ```

> [tab] Baseten
>
> ```bash Shell
> export BASETEN_API_KEY="<API_KEY>"
> ```
>
> ```bash .env
> BASETEN_API_KEY=your-api-key
> ```

> [tab] Ollama
>
> ```bash Shell
> # Local: Ollama must be running (https://ollama.com)
> # Cloud: Set your Ollama API key for hosted inference
> export OLLAMA_API_KEY="<API_KEY>"
> ```
>
> ```bash .env
> # Local: Ollama must be running (https://ollama.com)
> # Cloud: Set your Ollama API key for hosted inference
> OLLAMA_API_KEY=your-api-key
> ```

> [tab] Azure
>
> ```bash Shell
> export AZURE_OPENAI_API_KEY="<API_KEY>"
> export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
> export AZURE_OPENAI_DEPLOYMENT_NAME="your-deployment"
> ```
>
> ```bash .env
> AZURE_OPENAI_API_KEY=your-api-key
> AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
> AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment
> ```

> [tab] AWS Bedrock
>
> ```bash Shell
> export AWS_ACCESS_KEY_ID="your-access-key"
> export AWS_SECRET_ACCESS_KEY="your-secret-key"
> export AWS_REGION="us-east-1"
> ```
>
> ```bash .env
> AWS_ACCESS_KEY_ID=your-access-key
> AWS_SECRET_ACCESS_KEY=your-secret-key
> AWS_REGION=us-east-1
> ```

> [tab] HuggingFace
>
> ```bash Shell
> export HUGGINGFACEHUB_API_TOKEN="hf_..."
> ```
>
> ```bash .env
> HUGGINGFACEHUB_API_TOKEN=hf_...
> ```

> [tab] Other
>
> See the full list of supported [chat model integrations](https://docs.langchain.com/oss/python/integrations/chat.md).

To load a `.env` file, use [`python-dotenv`](https://pypi.org/project/python-dotenv/) (`load_dotenv()`).

> [!TIP]
>
> If you are using the LangSmith [LLM Gateway](https://docs.langchain.com/langsmith/llm-gateway.md), traffic to providers is routed through LangSmith. Use the gateway key as the API key instead.

## Build a basic agent

Start by creating a simple agent that can answer questions and call tools. The agent in this example uses the chosen language model, a basic weather function as a tool, and a simple prompt to guide its behavior:

```python OpenAI
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="openai:gpt-6.1-sol",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```

```python Google Gemini
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="google_genai:gemini-2.5-flash-lite",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```

```python Claude (Anthropic)
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="claude-sonnet-4-6",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```

```python OpenRouter
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="openrouter:anthropic/claude-sonnet-4-6",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```

```python Fireworks
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="fireworks:accounts/fireworks/models/qwen3p5-397b-a17b",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```

```python Baseten
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="baseten:zai-org/GLM-5.2",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```

```python Ollama
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="ollama:devstral-2",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```

```python Azure
import os
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

model = init_chat_model(
    "azure_openai:gpt-6.1-sol",
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)
agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```

```python AWS Bedrock
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="bedrock_converse:us.anthropic.claude-sonnet-4-6",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```

```python HuggingFace
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="huggingface:microsoft/Phi-3-mini-4k-instruct",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
```

When you run the code and prompt the agent to tell you about the weather in San Francisco, the agent uses that input and its available context.
The agent understands that you are asking about the weather for the city San Francisco and therefore calls the weather tool with the provided city name.

> [!TIP]
>
> You can use [any supported model](https://docs.langchain.com/oss/python/integrations/providers/overview.md) by changing the model name and setting up the appropriate API key. Trace what is happening inside your agent with [LangSmith](https://smith.langchain.com?utm_source=docs\&utm_medium=cta\&utm_campaign=langsmith-signup\&utm_content=oss-langchain-quickstart). Follow the [tracing quickstart](https://docs.langchain.com/langsmith/trace-with-langchain.md) to get set up.
>
> We recommend you also set up [LangSmith Engine](https://docs.langchain.com/langsmith/engine.md) which monitors your traces, detects issues, and proposes fixes.

## Build a real-world agent

In the following example you will build a research agent that can answer questions about text files.
Along the way you will explore the following concepts:

1. **Detailed system prompts** for better agent behavior
2. **Create tools** that integrate with external data
3. **Model configuration** for consistent responses
4. **Conversational memory** for chat-like interactions
5. **Deep Agents** for built-in features
6. **Testing** your agent

**1. Define the system prompt**

The system prompt defines your agent’s role and behavior. Keep it specific and actionable:

```python wrap
SYSTEM_PROMPT = """You are a literary data assistant.

## Capabilities

- `fetch_text_from_url`: loads document text from a URL into the conversation.
Do not guess line counts or positions—ground them in tool results from the saved file."""
```

**2. Create tools**

[Tools](../Core%20components/Tools.md) let a model interact with external systems by calling functions you define.
Tools can depend on [runtime context](../Advanced%20usage/Runtime.md) and also interact with [agent memory](../Core%20components/Short-term%20memory.md).

This example uses a tool to load a document from a given URL:

```python
import urllib.error
import urllib.request

from langchain.tools import tool


@tool
def fetch_text_from_url(url: str) -> str:
    """Fetch the document from a URL.
    """
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; quickstart-research/1.0)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read()
    except urllib.error.URLError as e:
        return f"Fetch failed: {e}"
    text = raw.decode("utf-8", errors="replace")
    return text
```

> [!TIP]
>
> Tools should be well-documented: their name, description, and argument names become part of the model's prompt.
> LangChain's [`@tool` decorator](https://reference.langchain.com/python/langchain-core/tools/convert/tool) adds metadata and enables runtime injection with the `ToolRuntime` parameter.
> Learn more in the [tools guide](../Core%20components/Tools.md).

**3. Configure your model**

Set up your [language model](../Core%20components/Models.md) with the right parameters for your use case. For example:

```python OpenAI
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "openai:gpt-6.1-sol",
    temperature=0.5,
    timeout=300,
    max_tokens=25000,
)
```

```python Google Gemini
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "gemini-3.1-pro-preview",
    model_provider="google-genai",
    temperature=0.5,
    timeout=600,
    max_tokens=25000,
    streaming=True,
)
```

```python Claude (Anthropic)
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "claude-sonnet-4-6",
    temperature=0.5,
    timeout=600,
    max_tokens=25000,
    streaming=True,
)
```

```python OpenRouter
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "openrouter:anthropic/claude-sonnet-4-6",
    temperature=0.5,
    timeout=300,
    max_tokens=25000,
)
```

```python Fireworks
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "fireworks:accounts/fireworks/models/qwen3p5-397b-a17b",
    temperature=0.5,
    timeout=300,
    max_tokens=25000,
)
```

```python Baseten
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "baseten:zai-org/GLM-5.2",
    temperature=0.5,
    timeout=300,
    max_tokens=25000,
)
```

```python Ollama
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "ollama:devstral-2",
    temperature=0.5,
    timeout=300,
    max_tokens=25000,
)
```

```python Azure
import os
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "azure_openai:gpt-6.1-sol",
    temperature=0.5,
    timeout=300,
    max_tokens=25000,
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)
```

```python AWS Bedrock
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "us.anthropic.claude-sonnet-4-6",
    model_provider="bedrock_converse",
    temperature=0.5,
    timeout=300,
    max_tokens=25000,
)
```

```python HuggingFace
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "microsoft/Phi-3-mini-4k-instruct",
    model_provider="huggingface",
    temperature=0.5,
    timeout=300,
    max_tokens=25000,
)
```

Depending on the model and provider chosen, initialization parameters may vary; refer to their reference pages for details.

**4. Add memory**

Add [memory](../Core%20components/Short-term%20memory.md) to your agent to maintain state across interactions. This allows
the agent to remember previous conversations and context.

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
```

> [!NOTE]
>
> In production, use a persistent checkpointer that saves message history to a database.
> See [Add and manage memory](https://docs.langchain.com/oss/python/langgraph/add-memory.md#manage-short-term-memory) for more details.

**5. Create and run the agent**

Now assemble your agent with all the components and run it.

There are two different frameworks for creating agents: LangChain agents and deep agents.
Both LangChain and deep agents provide you with fine-grained control over tools, memory, and more.
The main difference between both is that deep agents come with a range of commonly useful capabilities already built in, such as planning, file system tools, and subagents.

Use deep agents when you want maximum capability with minimal setup; choose LangChain agents when you need fine-grained control.

To compare both in this step, install the `deepagents` package:

```bash uv
uv add deepagents
```

```bash pip
pip install -U deepagents
```

> [!WARNING]
>
> This example sends the entire text of The Great Gatsby to the model and may take a minute or two to respond. You can view example output in the next step.

Let's try both:

```python wrap
from langchain.agents import create_agent
from deepagents import create_deep_agent

agent = create_agent(
    model=model,
    tools=[fetch_text_from_url],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)

deep_agent = create_deep_agent(
    model=model,
    tools=[fetch_text_from_url],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)

content = f"""Project Gutenberg hosts a full plain-text copy of F. Scott Fitzgerald's The Great Gatsby.
URL: https://www.gutenberg.org/files/64317/64317-0.txt

Answer as much as you can:

1) How many lines in the complete Gutenberg file contain the substring `Gatsby` (count lines, not occurrences within a line, each line ends with a line break).
2) The 1-based line number of the first line in the file that contains `Daisy`.
3) A two-sentence neutral synopsis.

Do your best on (1) and (2). If at any point you realize you cannot **verify** an exact answer with
your available tools and reasoning, do not fabricate numbers: use `null` for that field and spell out
the limitation in `how_you_computed_counts`. If you encounter any errors please report what the error was and what the error message was."""

print("Running create_agent...", flush=True)
agent_result = agent.invoke(
    {"messages": [{"role": "user", "content": content}]},
    config={"configurable": {"thread_id": "great-gatsby-lc"}},
)
print("Running create_deep_agent...", flush=True)
deep_agent_result = deep_agent.invoke(
    {"messages": [{"role": "user", "content": content}]},
    config={"configurable": {"thread_id": "great-gatsby-da"}},
)
print("\ncreate_agent:")
print(agent_result["messages"][-1].content_blocks)
print("\ncreate_deep_agent:")
print(deep_agent_result["messages"][-1].content_blocks)
```

The following expander has everything together in a runnable script:

**Full example code**

```python wrap
import urllib.error
import urllib.request

from langchain.agents import create_agent
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

SYSTEM_PROMPT = """You are a literary data assistant.

## Capabilities

- `fetch_text_from_url`: loads document text from a URL into the conversation.
Do not guess line counts or positions—ground them in tool results from the saved file."""


@tool
def fetch_text_from_url(url: str) -> str:
    """Fetch the document from a URL.
    """
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; quickstart-research/1.0)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read()
    except urllib.error.URLError as e:
        return f"Fetch failed: {e}"
    text = raw.decode("utf-8", errors="replace")
    return text


model = init_chat_model(
    "gemini-3.1-pro-preview",
    model_provider="google-genai",
    temperature=0.5,
    timeout=600,
    max_tokens=25000,
    streaming=True,
)

checkpointer = InMemorySaver()

agent = create_agent(
    model=model,
    tools=[fetch_text_from_url],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)

deep_agent = create_deep_agent(
    model=model,
    tools=[fetch_text_from_url],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)

content = f"""Project Gutenberg hosts a full plain-text copy of F. Scott Fitzgerald's The Great Gatsby.
URL: https://www.gutenberg.org/files/64317/64317-0.txt

Answer as much as you can:

1) How many lines in the complete Gutenberg file contain the substring `Gatsby` (count lines, not occurrences within a line, each line ends with a line break).
2) The 1-based line number of the first line in the file that contains `Daisy`.
3) A two-sentence neutral synopsis.

Do your best on (1) and (2). If at any point you realize you cannot **verify** an exact answer with
your available tools and reasoning, do not fabricate numbers: use `null` for that field and spell out
the limitation in `how_you_computed_counts`. If you encounter any errors please report what the error was and what the error message was."""

print("Running create_agent...", flush=True)
agent_result = agent.invoke(
    {"messages": [{"role": "user", "content": content}]},
    config={"configurable": {"thread_id": "great-gatsby-lc"}},
)
print("Running create_deep_agent...", flush=True)
deep_agent_result = deep_agent.invoke(
    {"messages": [{"role": "user", "content": content}]},
    config={"configurable": {"thread_id": "great-gatsby-da"}},
)
print("\ncreate_agent:")
print(agent_result["messages"][-1].content_blocks)
print("\ncreate_deep_agent:")
print(deep_agent_result["messages"][-1].content_blocks)
```

**6. Review the results**

The results will differ based on the model and the execution.

> [tab] LangChain agents
>
> ```txt wrap expandable
> **1) Number of lines containing `Gatsby`:** `null`
>
> **2) First line containing `Daisy`:** `null`
>
> **3) Synopsis:**
> The Great Gatsby follows the mysterious millionaire Jay Gatsby and his obsession with reuniting with his former lover, Daisy Buchanan, as narrated by his neighbor Nick Carraway. Set against the backdrop of the Roaring Twenties on Long Island, the novel explores themes of wealth, class, and the elusive nature of the American Dream.
>
> **how_you_computed_counts:**
> I successfully fetched the full text of the eBook using the `fetch_text_from_url` tool. However, because I do not have access to a code execution environment (like Python) or text-processing tools (like `grep`), I cannot deterministically split the text by line breaks, iterate through the thousands of lines, and verify the exact line numbers or match counts. LLMs cannot reliably perform exact line-counting or indexing over massive texts within their context window without external computational tools. As instructed, rather than fabricating or guessing a number, I have output `null` for the exact counts and positions.
> ```

> [tab] Deep agents
>
> ```txt wrap expandable
> Based on the text fetched directly from the Gutenberg URL and analyzed using filesystem search tools, here are the answers to your questions:
>
> **1) Lines containing the substring `Gatsby`**
> **258** lines contain the exact substring `Gatsby`.
>
> **2) First line containing `Daisy`**
> Line **181** is the first line in the file that contains the exact substring `Daisy`.
> *(For context, the line reads: "Buchanans. Daisy was my second cousin once removed, and I’d known Tom")*
>
> **3) Two-sentence neutral synopsis**
> *The Great Gatsby* follows the mysterious millionaire Jay Gatsby and his obsessive pursuit to reunite with his former lover, Daisy Buchanan, in 1920s Long Island. The story is narrated by Nick Carraway, who observes the tragic consequences of Gatsby's relentless ambition and the shallow materialism of the era's wealthy elite.
>
> ***
>
> **How counts were computed:**
> When fetching the document from the URL, the file was too large for the standard output and was automatically saved to the local filesystem by the system (`/large_tool_results/x246ax2x`). I then used the `grep` tool to search the saved file for the exact literal substrings `Gatsby` and `Daisy`. The `grep` tool returned every matching line along with its 1-based line number. I manually counted the exact number of lines returned for `Gatsby` (which totaled 258) and identified the first line number returned for `Daisy` (which was 181). I also verified there were no uppercase variations (`GATSBY` or `DAISY`) that would have been missed. No errors were encountered during this process.
> ```

If you look at the output on both tabs, you notice that the LangChain agent provided answers but they are estimates. The agent lacks the tools to answer this question. You may also get errors that the prompt is too long.

The deep agent, on the other hand can:

1. **Plans its approach** using the built-in [`write_todos`](https://docs.langchain.com/oss/python/deepagents/harness#task-planning) tool to break down the research task.
2. **Loads the file** by calling the `fetch_text_from_url` tool to gather information.
3. **Manages context** by using file system tools ([`grep`](https://docs.langchain.com/oss/python/deepagents/harness#virtual-filesystem-access) and [`read_file`](https://docs.langchain.com/oss/python/deepagents/harness#virtual-filesystem-access)).
4. **Spawns subagents** as needed to delegate complex subtasks to specialized subagents.

For LangChain agents, you must implement more capabilities to get a similar level of service and can customize them along the way as needed.

## Trace agent calls

> [!NOTE]
>
> In an [agent-based workspace](https://docs.langchain.com/langsmith/agent-registry.md), [create an agent](https://docs.langchain.com/langsmith/create-an-agent.md) once before sending traces. Use [agent addressing](https://docs.langchain.com/langsmith/log-traces-to-agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](https://docs.langchain.com/langsmith/create-an-agent#use-an-environment-project) as a compatibility value.

Most interesting agents you build with LangChain make many calls to LLMs. As these agents get more complex, it becomes important to be able to inspect what exactly is going on inside your agent. The best way to do this is with [LangSmith](https://smith.langchain.com?utm_source=docs\&utm_medium=cta\&utm_campaign=langsmith-signup\&utm_content=oss-langchain-quickstart).

Sign up for a [LangSmith](https://smith.langchain.com?utm_source=docs\&utm_medium=cta\&utm_campaign=langsmith-signup\&utm_content=oss-langchain-quickstart) account and set these to start logging traces:

```shell
export LANGSMITH_AGENT_ID="<your-agent-id>"
export LANGSMITH_AGENT_ENVIRONMENT="local"
export LANGSMITH_TRACING="true"
export LANGSMITH_API_KEY="..."
```

Once set, run your script again and then inspect what happened during your agent calls on [LangSmith](https://smith.langchain.com?utm_source=docs\&utm_medium=cta\&utm_campaign=langsmith-signup\&utm_content=oss-langchain-quickstart) .

> [!TIP]
>
> To learn more about tracing your agent with LangSmith, see the [LangSmith documentation](https://docs.langchain.com/langsmith/trace-with-langchain.md).
>
> We recommend you also set up [LangSmith Engine](https://docs.langchain.com/langsmith/engine.md) which monitors your traces, detects issues, and proposes fixes.

## Next steps

You now have agents that can:

* **Understand context** and remember conversations
* **Use tools** intelligently
* **Provide structured responses** in a consistent format
* **Handle user-specific information** through context
* **Maintain conversation state** across interactions
* **Plan, research, and synthesize** (deep agents only)

Continue with:

* **LangChain agents**: [Add and manage memory](https://docs.langchain.com/oss/python/langgraph/add-memory.md#manage-short-term-memory), [deploy to production](https://docs.langchain.com/oss/python/langgraph/deploy.md)
* **Deep Agents**: [Customization options](https://docs.langchain.com/oss/python/deepagents/customization.md), [persistent memory](https://docs.langchain.com/oss/python/deepagents/memory.md), [deploy to production](https://docs.langchain.com/oss/python/langgraph/deploy.md)

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/quickstart.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
