# Trace with Amazon Bedrock

This guide shows you how to trace [Amazon Bedrock](https://aws.amazon.com/bedrock) model calls with LangSmith using the native AWS SDKs. LangSmith also works seamlessly with [LangChain's Bedrock integrations](https://docs.langchain.com/oss/python/integrations/providers/aws.md). Either approach provides insights into:

* Request and response payloads
* Token usage and costs
* Latency and performance metrics
* Custom tags and metadata for filtering and analysis
* Multi-step chains and agent workflows

> [!NOTE]
>
> In an [agent-based workspace](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

## Installation

```bash pip
pip install boto3 langsmith
```

```bash npm
npm install @aws-sdk/client-bedrock-runtime langsmith
```

This integration uses the native AWS SDKs with LangSmith's tracing capabilities. For Python, you'll use [`boto3`](https://pypi.org/project/boto3/) (the AWS SDK for Python) along with [`langsmith`](https://pypi.org/project/langsmith/) to capture traces. For JavaScript/TypeScript, you'll use [`@aws-sdk/client-bedrock-runtime`](https://www.npmjs.com/package/@aws-sdk/client-bedrock-runtime) with the [`langsmith`](https://www.npmjs.com/package/langsmith) package. Both implementations use the [Bedrock Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html), which provides a unified interface for interacting with foundation models.

## Setup

To enable LangSmith tracing, configure your [LangSmith API key](../../../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md), agent identifier, and environment. You'll also need to set up your AWS credentials to authenticate with Bedrock.

### LangSmith configuration

Sending traces to an agent requires `langsmith>=0.14.9` in Python or `langsmith@>=0.11.0` in TypeScript.

```bash
export LANGSMITH_API_KEY=<your_langsmith_api_key>
export LANGSMITH_AGENT_ID="<your-agent-id>"
export LANGSMITH_AGENT_ENVIRONMENT="local"
export LANGSMITH_TRACING=true
```

You can obtain your LangSmith API key from [smith.langchain.com](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-trace-bedrock) by navigating to **Settings** > **API Keys**. The agent identifier and environment select where traces appear.

### AWS credentials

Configure your AWS credentials to authenticate with Bedrock. You'll need an AWS account with Bedrock access enabled. Follow the [AWS setup instructions](https://docs.aws.amazon.com/bedrock/latest/userguide/setting-up.html) to create your credentials and [enable model access](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html):

```bash
export AWS_ACCESS_KEY_ID=<your_aws_access_key_id>
export AWS_SECRET_ACCESS_KEY=<your_aws_secret_key>
export AWS_SESSION_TOKEN=<your_session_token> # only if using temporary credentials
export AWS_DEFAULT_REGION=<your_bedrock_region> # e.g., us-east-1 or us-west-2
```

## Configure tracing

Once your environment variables are set, you can trace Bedrock model calls by wrapping your invocation functions with LangSmith's `@traceable` decorator (Python) or `traceable` function (TypeScript).

The following example demonstrates how to use the Bedrock Converse API with LangSmith tracing. The Converse API is AWS's recommended unified interface for foundation models, providing consistent request and response handling across different model providers. You can enhance traces with custom tags and metadata—tags help you categorize traces (e.g., by environment, feature, or test type), while metadata allows you to attach arbitrary key-value pairs for detailed context:

```python Python
import boto3
from langsmith import traceable

# Initialize Bedrock runtime client (ensure AWS creds and region are set)
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
model_id = "anthropic.claude-haiku-4-5-20251001-v1:0"  # Example Bedrock model ID

# Decorate the model invocation function to auto-capture a trace with tags/metadata
@traceable(tags=["aws-bedrock", "langsmith", "integration-test"],
           metadata={"env": "dev", "model_provider": "bedrock", "model_id": "claude-haiku-4-5"})
def generate_text(prompt: str) -> str:
    # Prepare a single-turn conversation input for the Converse API
    messages = [
        {"role": "user", "content": [{"text": prompt}]}
    ]
    # Invoke the Bedrock model using the unified Converse API
    response = bedrock.converse(
        modelId=model_id,
        messages=messages,
        inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9}
    )
    # Extract the model's reply text from the response
    output_text = response["output"]["message"]["content"][0]["text"]
    return output_text

# Call the traced function with a prompt
result = generate_text("How can I trace AWS Bedrock model outputs to LangSmith for debugging?")
print(result)
```

```typescript TypeScript
import { BedrockRuntimeClient, ConverseCommand } from "@aws-sdk/client-bedrock-runtime";
import { traceable } from "langsmith";

const client = new BedrockRuntimeClient({ region: "us-east-1" });
const modelId = "anthropic.claude-haiku-4-5-20251001-v1:0";

// Wrap the Bedrock invocation in a traceable function with tags and metadata
const invokeBedrock = traceable(
  async (userInput: string) => {
    // Prepare the conversation message for the Bedrock Converse API
    const conversation = [
      { role: "user", content: [{ text: userInput }] }
    ];
    // Create and send a Bedrock Converse command (single-turn chat)
    const command = new ConverseCommand({
      modelId,
      messages: conversation,
      inferenceConfig: { maxTokens: 512, temperature: 0.5, topP: 0.9 }
    });
    const response = await client.send(command);
    // Extract the assistant's reply text from the response
    const outputText = response.output?.message?.content[0]?.text;
    return outputText;
  },
  {
    tags: ["aws-bedrock", "langsmith", "integration-test"],
    metadata: { env: "dev", model_provider: "bedrock", model_id: "claude-haiku-4-5" }
  }
);

// Invoke the traced function with a prompt
const answer = await invokeBedrock("How can I trace AWS Bedrock model outputs to LangSmith for debugging?");
console.log(answer);
```

> [tab] Python
>
> * `boto3.client("bedrock-runtime")` creates a Bedrock Runtime client.
> * The `converse` method sends a chat prompt (as a list of messages) to the specified model and returns a structured response.
> * The `generate_text` function is decorated with `@traceable`, logging each call to LangSmith as a trace (using the function name as the default trace name).
> * Custom tags (`aws-bedrock`, `langsmith`, `integration-test`) and metadata (environment, model info) are passed into the decorator and attached to the trace record for filtering in the LangSmith UI.
> * When you run this code (with `LANGSMITH_TRACING=true` and your API key set), LangSmith automatically captures the input prompt, model output, token usage, and latency.

> [tab] TypeScript
>
> * `BedrockRuntimeClient` from the AWS SDK v3 provides the Bedrock runtime interface.
> * `ConverseCommand` offers a unified chat interface that sends a user message and returns the assistant's response in a structured format (no manual JSON parsing needed).
> * The Bedrock call is wrapped with LangSmith's `traceable` function, converting `invokeBedrock` into a traced function that logs its execution to LangSmith.
> * Custom tags and metadata are provided in the traceable options object and attached to each trace.
> * When you run this script (with `LANGSMITH_TRACING=true` and your API key configured), check your LangSmith dashboard for trace entries that include the input prompt, model output, timing info, and specified tags/metadata.

## View traces in LangSmith

After running your code, select your agent and environment, then open **Tracing** at [smith.langchain.com](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-trace-bedrock) to view the traces. Each trace includes:

* **Request details**: Input messages, model parameters, and configuration
* **Response details**: Model output, token usage, and response metadata
* **Performance metrics**: Latency, tokens per second, and cost estimates
* **Custom metadata**: Tags and metadata you provided to the `@traceable` decorator

You can filter traces by tags (e.g., `aws-bedrock` or `integration-test`), search by metadata fields, or drill into specific traces to debug issues.

## Next steps

* Learn more about [LangSmith features](../../../../Overview/LangSmith%20Observability.md) including evaluation, datasets, and feedback
* Explore [Bedrock model capabilities](https://docs.aws.amazon.com/bedrock/latest/userguide/models-features.html) like tool calling, streaming, and prompt caching
* Review [LangChain Bedrock integration documentation](https://docs.langchain.com/oss/python/integrations/chat/bedrock) for advanced features like extended thinking and citations
