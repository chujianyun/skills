# Trace with Google Gemini

This guide shows you how to trace and log [Google's Gemini](https://ai.google.dev/gemini-api/docs) models in LangSmith. You'll instrument Gemini calls using the latest [`google-genai` SDK](https://googleapis.github.io/python-genai/) (Python) or [`@google/genai` SDK](https://googleapis.github.io/js-genai/release_docs/index.html) (JavaScript), wrap the Gemini client for tracing, and try examples including basic prompts, metadata tagging, and multi-turn conversations.

> [!NOTE]
>
> The LangSmith Gemini wrappers are in **[beta](../../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)**. The API may change in future releases.

> [!NOTE]
>
> In an [agent-based workspace](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

## Installation

Install the required packages using your preferred package manager:

```bash pip
pip install langsmith google-genai
```

```bash npm
npm install langsmith@latest @google/genai
```

## Setup

Sending traces to an agent requires `langsmith>=0.14.9` in Python or `langsmith@>=0.11.0` in TypeScript.

Set your [API keys](../../../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md), agent identifier, and environment:

```bash
export LANGSMITH_API_KEY=<your_langsmith_api_key>
export LANGSMITH_AGENT_ID="<your-agent-id>"
export LANGSMITH_AGENT_ENVIRONMENT="local"
export LANGSMITH_TRACING=true
export GOOGLE_API_KEY=<your_google_api_key>
```

To create a Google API key, refer to [Google AI Studio](https://aistudio.google.com/apikey).

## Configure tracing

To trace Gemini API calls, use LangSmith's [`wrap_gemini`](https://reference.langchain.com/python/langsmith/wrappers/_gemini/wrap_gemini) (Python) or [`wrapGemini`](https://reference.langchain.com/javascript/langsmith/wrappers/gemini/wrapGemini) (JavaScript) wrapper function. This wrapper intercepts calls to the Gemini client and automatically logs them as traces in LangSmith. The wrapper preserves all of the original client's functionality while adding observability:

```python Python
from google import genai
from langsmith import wrappers

def main():
    # genai.Client() reads GOOGLE_API_KEY / GEMINI_API_KEY from the environment
    gemini_client = genai.Client()

    # Wrap the Gemini client to enable LangSmith tracing
    client = wrappers.wrap_gemini(
        gemini_client,
        tracing_extra={
            "tags": ["gemini", "python"],
            "metadata": {
                "integration": "google-genai",
            },
        },
    )

    # Make a traced Gemini call
    response = client.models.generate_content(
        model="gemini-4-hydrogen",
        contents="Explain quantum computing in simple terms.",
    )

    print(response.text)


if __name__ == "__main__":
    main()
```

```javascript JavaScript
import { GoogleGenAI } from "@google/genai";
import { wrapGemini } from "langsmith/wrappers/gemini";

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;

// Initialize the Gemini client
const geminiClient = new GoogleGenAI({ apiKey: GEMINI_API_KEY });

// Wrap the client to enable LangSmith tracing
// Configuration is applied to ALL calls made with this wrapped client
const client = wrapGemini(geminiClient, {
  tags: ["gemini", "javascript"],
  metadata: {
    integration: "google-genai",
  },
});

// Make a traced call - tracing happens automatically
const response = await client.models.generateContent({
  model: "gemini-4-hydrogen",
  contents: "Explain quantum computing in simple terms.",
});

console.log(response.text);
```

> [tab] Python
>
> You can customize tracing by passing [`tracing_extra`](https://reference.langchain.com/python/langsmith/wrappers/_gemini/wrap_gemini) when calling `wrap_gemini()`. This parameter applies to all subsequent requests you make with that wrapped client, which allows you to attach tags and metadata for filtering and organizing traces in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-trace-with-google-gemini). The `tracing_extra` parameter accepts:
>
> * `tags`: A list of strings to categorize traces (for example, `["production", "gemini"]`).
> * `metadata`: A dictionary of key-value pairs for additional context (for example, `{"team": "ml-research", "integration": "google-genai"}`).
> * `client`: An optional custom LangSmith client instance.
>
> These settings apply consistently across all traces from the wrapped client, so that you can include environment-level tags or team metadata that should remain constant throughout your agent.

> [tab] JavaScript
>
> You can customize tracing by passing configuration options to [`wrapGemini`](https://reference.langchain.com/javascript/langsmith/wrappers/gemini/wrapGemini). These options apply to all subsequent requests you make with that wrapped client, which allows you to attach tags and metadata for filtering and organizing traces in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-trace-with-google-gemini). The configuration accepts:
>
> * `tags`: An array of strings to categorize traces (for example, `["production", "gemini"]`).
> * `metadata`: An object with key-value pairs for additional context (for example, `{ team: "ml-research", integration: "google-genai" }`).
> * `client`: An optional custom LangSmith client instance.
>
> These settings apply consistently across all traces from the wrapped client, so that you can include environment-level tags or team metadata that should remain constant throughout your agent.

## View traces in LangSmith

After running your agent, you can view traces in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-trace-with-google-gemini) that include:

* **Model requests**: Complete prompts sent to Gemini models
* **Model responses**: Generated text and structured outputs
* **Function calls**: Tool invocations and results when using function calling
* **Chat sessions**: Multi-turn conversation context
* **Performance metrics**: Latency and token usage information
