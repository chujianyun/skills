# Browser use

> Give a deep agent a browser so it can take actions on websites and test web apps end to end.

Browser use gives a deep agent a browser that it controls through tools. The agent opens pages, reads what renders, clicks, types, and takes screenshots. Use it for work that happens on the web:

* **Actions with no public API**: Book a restaurant reservation, complete a checkout, or research a topic by following links across sites.
* **End-to-end testing**: QA a web app through its UI. [Open SWE](https://github.com/langchain-ai/open-swe), LangChain's open-source coding agent, gets a browser in each thread so it can open the app it changed and check the change in the UI.

To add a browser to a managed agent, see [Browser use in Managed Deep Agents](https://docs.langchain.com/langsmith/python/managed-deep-agents-browser-use.md).

## Understand the basics

An agent needs two components to use the web:

| Component | Options |
| - | - |
| A browser | <ul><li>**Local**: Chrome or Chromium on your machine or in a [sandbox](Sandboxes.md). Reaches apps on its own `localhost` and needs no provider account. You install and update Chrome yourself.</li><li>**Remote**: A cloud browser from a provider such as [Browserbase](https://www.browserbase.com). Isolated from your machine, needs an API key, and cannot reach `localhost` on your machine or in your sandbox.</li></ul> |
| Browser tools | [Stagehand v4](https://docs.stagehand.dev/v4/integrations/agent-frameworks/deep-agents) (recommended), [Playwright MCP](https://github.com/microsoft/playwright-mcp), or the [agent-browser](https://github.com/vercel-labs/agent-browser) CLI. |

### Use Stagehand with local or remote browsers

[Stagehand](https://docs.stagehand.dev/v4/first-steps/introduction) provides browser tools that work with both local Chrome and remote Browserbase sessions. Choose where the browser runs without changing the tools your agent uses. Stagehand exposes three tools over one persistent browser:

| Tool | Description |
| - | - |
| `snapshot` | Reads the active page's accessibility tree and labels interactive elements with IDs. |
| `run` | Acts on the page with a batch of snapshot actions (`click`, `hover`, `fill`, `type`, `press`, `select`) or with JavaScript that uses Playwright-style `page`, `context`, and `browser` objects. |
| `screenshot` | Captures the rendered page as a PNG or JPEG. |

An element ID is valid only for the latest snapshot of the active page, so the agent takes a new snapshot after it navigates.

Add these tools with `StagehandMiddleware` from [langchain-stagehand](https://github.com/langchain-ai/langchain-browserbase). Pass a configured Stagehand client to the middleware, then include it in `middleware`. No MCP server, custom tool definitions, or browser system prompt is needed.

For the full configuration reference, see the [Stagehand integration](https://docs.langchain.com/oss/python/integrations/tools/stagehand).

### Other browser tools

* **[Playwright MCP](https://github.com/microsoft/playwright-mcp)**: An MCP server from Microsoft that exposes Playwright browser actions. Connect it through an MCP adapter, with `npx @playwright/mcp@latest` as the command. See [Model Context Protocol](../Protocols/Model%20Context%20Protocol%20%28MCP%29.md).
* **[agent-browser](https://github.com/vercel-labs/agent-browser)**: A browser CLI from Vercel Labs. Install it in a [sandbox](Sandboxes.md), and the agent runs commands such as `agent-browser open` and `agent-browser snapshot` through the `execute` tool.

## Use Stagehand with Browserbase

This example gives a deep agent Stagehand tools that drive a Browserbase browser. The agent runs on your machine. The browser runs on Browserbase.

> [!NOTE]
>
> `langchain-stagehand` requires Python 3.11 or later, LangChain 1.4.7 or later, and Stagehand 4.3.0 or later.

Install the middleware, Deep Agents, and the model integration:

```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
pip install langchain-stagehand deepagents langchain-openai
```

Set your API keys:

```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
export OPENAI_API_KEY="<API_KEY>"
export BROWSERBASE_API_KEY="<API_KEY>"
```

Create the browser and pass its Stagehand client to the middleware:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import asyncio
import os

from deepagents import create_deep_agent
from langchain_stagehand import StagehandMiddleware
from stagehand import Stagehand, browserbase


async def main():
    browser = await browserbase.launch(api_key=os.environ["BROWSERBASE_API_KEY"])
    try:
        stagehand = await Stagehand.create(browser=browser)
        agent = create_deep_agent(
            model="openai:gpt-5.5-2026-04-23",
            middleware=[StagehandMiddleware(stagehand=stagehand)],
        )
        result = await agent.ainvoke({
            "messages": [{
                "role": "user",
                "content": (
                    "On opentable.com, find a table for two in San Francisco this Friday "
                    "at 7 PM. Stop before confirming, and report the restaurant, time, and booking link."
                ),
            }]
        })
        print(result["messages"][-1].content_blocks)
    finally:
        await browser.close()


asyncio.run(main())
```

Use `ainvoke` or `astream`: the browser tools are asynchronous. Your application owns the browser and closes it when finished. Keep it open across runs to reuse tabs and logins. The middleware leaves your system prompt unchanged and includes browser guidance in tool descriptions.

For local Chrome, screenshots, and use with LangChain's `create_agent`, see the [Stagehand integration](https://docs.langchain.com/oss/python/integrations/tools/stagehand).

> [!TIP]
>
> Snapshots can be long. To keep them out of the main agent's context, give the browser tools to a [subagent](../Delegation/Subagents.md) and let the main agent delegate browser tasks to it.

## Choose a browser scope

Reusing a browser retains cookies and website logins, so the agent does not need to sign in on every turn. Choose which conversations share that state:

* **Thread scope**: Keep one browser per conversation. For example, test a web app change using a test account. Reuse the tabs and login as you iterate in the same conversation. Another conversation gets a separate browser without those cookies or logins. Participants in a shared thread can use its signed-in accounts.
* **User scope**: Reuse browser login state across the same authenticated user's conversations. For example, a person signs in to a booking site once, then requests another reservation in a new thread.

Do not reuse a personal browser session across unrelated users. Anyone whose agent can access that browser can act as its signed-in accounts. Use verified identity from your application's authentication layer, not a user ID supplied in a prompt.

`StagehandMiddleware` does not select a scope or manage session storage. Your application chooses which Stagehand client to supply. Reuse that client for sequential runs within the intended scope. Give concurrent agents separate clients and browsers to avoid conflicting navigation.

Browser state is not part of a LangGraph checkpoint. Closing or replacing the browser can lose logins, and websites can expire them independently.

[Managed Deep Agents](https://docs.langchain.com/langsmith/python/managed-deep-agents-browser-use.md#choose-a-scope) manages thread and user scope for you, including separate per-thread windows with shared login state for user scope.

## Test an app with Chrome in a LangSmith sandbox

This example covers end-to-end testing: after a coding agent changes an app, an agent opens the app in a browser and checks the change. Open SWE gets its browser from [Managed Deep Agents](https://docs.langchain.com/langsmith/python/managed-deep-agents-browser-use.md). The steps below build the same check with a LangSmith sandbox.

A [LangSmith sandbox](https://docs.langchain.com/langsmith/sandboxes.md) runs your app and Chrome together, so the browser can open the app at `localhost`. The agent runs on your machine and uses the `LangSmithSandbox` backend for filesystem access and an `execute` tool.

This example uses agent-browser through `execute`, rather than MCP. Each CLI call reuses the named `qa` browser session inside the sandbox. You do not need a Browserbase account or a Docker daemon on your machine.

### Prepare the sandbox snapshot

A [snapshot](https://docs.langchain.com/langsmith/sandbox-snapshots.md) contains the filesystem and dependencies for new sandboxes. Create one containing your app, its dependencies, Node.js, and curl. During snapshot setup, install agent-browser and Chrome for Testing:

```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
npm install -g agent-browser@latest
agent-browser install --with-deps
```

Run installation as the same user that runs the browser. The Linux dependency installer requires permission to install system packages. Capture the prepared filesystem as a snapshot and keep its ID. For snapshot creation and capture, see [Create a snapshot from a running sandbox](https://docs.langchain.com/langsmith/sandbox-snapshots.md#capture-a-snapshot-from-a-running-sandbox).

Set these variables on the machine that runs the agent:

```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
export LANGSMITH_API_KEY="<API_KEY>"
export OPENAI_API_KEY="<API_KEY>"
export QA_SNAPSHOT_ID="your-prepared-snapshot-id"
export QA_START_COMMAND="cd /app && npm run dev -- --host 0.0.0.0 --port 3000"
```

Replace `QA_START_COMMAND` with your app's start command. The examples expect it to serve port `3000` inside the sandbox.

### Create the QA agent

The code starts the app, waits for it to respond, and opens the browser. The agent then interacts with the UI through `execute`. Download screenshots before cleanup: deleting the sandbox deletes its files.

Install the host-side packages:

```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
pip install deepagents langsmith langchain-openai
```

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import os
from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends.langsmith import LangSmithSandbox
from langsmith.sandbox import SandboxClient

client = SandboxClient()
sandbox = client.create_sandbox(snapshot_id=os.environ["QA_SNAPSHOT_ID"])
backend = LangSmithSandbox(sandbox=sandbox)

try:
    app = sandbox.run(os.environ["QA_START_COMMAND"], wait=False, timeout=0, idle_timeout=-1)
    for command in [
        "curl --fail --retry 20 --retry-connrefused --retry-delay 1 "
        "--retry-max-time 30 http://127.0.0.1:3000",
        'agent-browser --session qa --args "--no-sandbox" '
        "open http://127.0.0.1:3000",
    ]:
        response = backend.execute(command)
        if response.exit_code != 0:
            raise RuntimeError(response.output)

    agent = create_deep_agent(
        model="openai:gpt-5.5-2026-04-23",
        backend=backend,
        system_prompt=(
            "Test the app through its UI using execute and agent-browser. "
            "Use agent-browser --session qa for every browser command. "
            "Use snapshot -i to inspect controls, then click or fill them. "
            "Take a new snapshot after page changes. Do not edit the app "
            "or alter its state by executing JavaScript. Save a screenshot "
            "to /tmp/qa.png before reporting observed results and failures."
        ),
    )
    result = agent.invoke({
        "messages": [{
            "role": "user",
            "content": "Sign up as qa@example.com and confirm that the dashboard loads.",
        }]
    })
    print(result["messages"][-1].content_blocks)
    image = backend.download_files(["/tmp/qa.png"])[0]
    if image.error:
        raise RuntimeError(image.error)
    Path("qa.png").write_bytes(image.content)
finally:
    client.delete_sandbox(sandbox.name)
    client.close()
```

The examples disable Chrome's internal sandbox with `--no-sandbox` for root-run sandbox images. The disposable LangSmith sandbox supplies the outer isolation boundary. For images that support Chrome's internal sandbox, omit that flag.

The screenshot is an artifact downloaded to your machine, not an image automatically shown to the model. For model-visible images, see [Multimodal inputs](Multimodal%20inputs%20and%20outputs.md). Use independent assertions for deterministic test results: an agent's report and its instructions are not a security boundary.

## Secure browser sessions

Code that runs in the browser can use any account the session is signed in to and any site the browser can reach. Before you give an agent a browser:

* For Stagehand, use Browserbase as the isolation boundary for untrusted tasks. `run` executes model-authored JavaScript inside the browser. See Stagehand's [security boundary](https://docs.stagehand.dev/v4/integrations/agent-frameworks/overview#security-boundary).
* For the [sandbox QA path](#test-an-app-with-chrome-in-a-langsmith-sandbox), the LangSmith sandbox is the isolation boundary. The disposable sandbox isolates Chrome and the app from your machine.
* Use test accounts and test payment methods for checkout and form flows, and [require approval](../Steering/Human-in-the-loop.md) before any action that commits a purchase.
* Treat page content as untrusted input. A page can contain text written to redirect the agent.
* Keep credentials in your application environment, not in prompts or browser tool inputs. When using MCP, pass the server only the credentials it needs.

## See also

* [Stagehand integration](https://docs.langchain.com/oss/python/integrations/tools/stagehand)

* [Browserbase integrations](https://docs.langchain.com/oss/python/integrations/providers/browserbase.md)

* [Browser use in Managed Deep Agents](https://docs.langchain.com/langsmith/python/managed-deep-agents-browser-use.md)

* [Sandboxes](Sandboxes.md)

* [Human-in-the-loop](../Steering/Human-in-the-loop.md)

* [Model Context Protocol (MCP)](../Protocols/Model%20Context%20Protocol%20%28MCP%29.md)

* [Stagehand Deep Agents documentation](https://docs.stagehand.dev/v4/integrations/agent-frameworks/deep-agents)

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/deepagents/browser-use.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
