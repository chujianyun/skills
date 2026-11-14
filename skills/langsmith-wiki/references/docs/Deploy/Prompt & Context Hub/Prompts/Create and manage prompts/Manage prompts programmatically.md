# Manage prompts programmatically

You can use the LangSmith Python, TypeScript, and Java SDKs to manage prompts programmatically.

> [!NOTE]
>
> Previously this functionality lived in the `langchainhub` package which is now deprecated. All functionality going forward will live in the `langsmith` package.

## Install packages

In Python, you can directly use the LangSmith SDK (*recommended, full functionality*) or you can use through the LangChain package (limited to pushing and pulling prompts).

In TypeScript, you must use the LangChain npm package for pulling prompts (it also allows pushing). For all other functionality, use the LangSmith package.

```bash pip
pip install -U langsmith # version >= 0.1.99
```

```bash uv
uv add langsmith  # version >= 0.1.99
```

```bash TypeScript
yarn add langsmith langchain # langsmith version >= 0.1.99 and langchain version >= 0.2.14
```

```kotlin Java/Kotlin (Gradle)
implementation("com.langchain.smith:langsmith-java:0.1.0-beta.4")
```

## Configure environment variables

If you already have `LANGSMITH_API_KEY` set to your current workspace's api key from LangSmith, you can skip this step.

Otherwise, get an API key for your workspace by navigating to `Settings > API Keys > Create API Key` in LangSmith.

Set your environment variable.

```bash
export LANGSMITH_API_KEY="lsv2_..."
```

> [!NOTE]
>
> What we refer to as "prompts" used to be called "repos", so any references to "repo" in the code are referring to a prompt.

## Push a prompt

To create a new prompt or update an existing prompt, you can use the `push prompt` method.

```python Python
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate

client = Client()
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
url = client.push_prompt("joke-generator", object=prompt)
# url is a link to the prompt in the UI
print(url)
```

```python LangChain (Python)
from langchain_classic import hub as prompts
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
url = prompts.push("joke-generator", prompt)
# url is a link to the prompt in the UI
print(url)
```

```typescript TypeScript
import * as hub from "langchain/hub";
import { ChatPromptTemplate } from "@langchain/core/prompts";

const prompt = ChatPromptTemplate.fromTemplate("tell me a joke about {topic}");
const url = hub.push("joke-generator", {
  object: prompt,
});
// url is a link to the prompt in the UI
console.log(url);
```

```java Java
import com.langchain.smith.client.LangsmithClient;
import com.langchain.smith.client.okhttp.LangsmithOkHttpClient;
import com.langchain.smith.core.JsonValue;
import com.langchain.smith.models.commits.CommitCreateParams;
import com.langchain.smith.models.repos.RepoCreateParams;
import java.util.List;
import java.util.Map;

LangsmithClient client = LangsmithOkHttpClient.fromEnv();


client.repos().create(
    RepoCreateParams.builder()
        .repoHandle("joke-generator")
        .isPublic(false)
        .build()
);

Map<String, Object> manifest = Map.of(
    "lc", 1,
    "type", "constructor",
    "id", List.of("langchain_core", "prompts", "prompt", "PromptTemplate"),
    "kwargs", Map.of(
        "template", "tell me a joke about {topic}",
        "input_variables", List.of("topic")
    )
);

client.commits().create(
    CommitCreateParams.builder()
        .owner("-")
        .repo("joke-generator")
        .manifest(JsonValue.from(manifest))
        .build()
);
```

You can also push a prompt as a RunnableSequence of a prompt and a model. This is useful for storing the model configuration you want to use with this prompt. The provider must be supported by the Playground, see [supported model providers](../Model%20providers.md).

```python Python
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

client = Client()
model = ChatOpenAI(model="gpt-5.4-mini")
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
chain = prompt | model
client.push_prompt("joke-generator-with-model", object=chain)
```

```python LangChain (Python)
from langchain_classic import hub as prompts
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-5.4-mini")
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
chain = prompt | model
url = prompts.push("joke-generator-with-model", chain)
# url is a link to the prompt in the UI
print(url)
```

```typescript TypeScript
import * as hub from "langchain/hub";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { ChatOpenAI } from "@langchain/openai";

const model = new ChatOpenAI({ model: "gpt-5.4-mini" });
const prompt = ChatPromptTemplate.fromTemplate("tell me a joke about {topic}");
const chain = prompt.pipe(model);
await hub.push("joke-generator-with-model", {
  object: chain,
});
```

## Push a StructuredPrompt

A `StructuredPrompt` combines a prompt template with an output schema, ensuring the model returns data in a defined structure. Use `StructuredPrompt.from_messages_and_schema` (Python) or `StructuredPrompt.fromMessagesAndSchema` (TypeScript) to create one, then push it to the hub like any other prompt.

### Without a model

Push the structured prompt on its own when you want to store the template and schema independently of any model configuration.

```python Python
from langsmith import Client
from langchain_core.prompts.structured import StructuredPrompt
from pydantic import BaseModel, Field

class ResponseSchema(BaseModel):
    positive_sentiment: bool = Field(description="Was the user sentiment positive?")

prompt = StructuredPrompt.from_messages_and_schema(
    [
        ("system", "Evaluate the sentiment of the following conversation."),
        ("human", "{conversation}"),
    ],
    schema=ResponseSchema.model_json_schema(),
)

client = Client()
url = client.push_prompt("sentiment-evaluator", object=prompt)
print(url)
```

```typescript TypeScript
import * as hub from "langchain/hub";
import { StructuredPrompt } from "@langchain/core/prompts";

const schema = {
  title: "ResponseSchema",
  type: "object",
  properties: {
    positive_sentiment: {
      type: "boolean",
      description: "Was the user sentiment positive?",
    },
  },
  required: ["positive_sentiment"],
};

const prompt = StructuredPrompt.fromMessagesAndSchema(
  [
    ["system", "Evaluate the sentiment of the following conversation."],
    ["human", "{conversation}"],
  ],
  schema
);

const url = await hub.push("sentiment-evaluator", prompt);
console.log(url);
```

### With a model

Push the structured prompt as a RunnableSequence with a model to store the full pipeline, including model configuration, in the hub.

```python Python
from langsmith import Client
from langchain_core.prompts.structured import StructuredPrompt
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

class ResponseSchema(BaseModel):
    positive_sentiment: bool = Field(description="Was the user sentiment positive?")

prompt = StructuredPrompt.from_messages_and_schema(
    [
        ("system", "Evaluate the sentiment of the following conversation."),
        ("human", "{conversation}"),
    ],
    schema=ResponseSchema.model_json_schema(),
)

model = ChatOpenAI(model="gpt-5.4-mini")
chain = prompt | model

client = Client()
url = client.push_prompt("sentiment-evaluator-with-model", object=chain)
print(url)
```

## Pull a prompt

To pull a prompt, you can use the `pull prompt` method, which returns the prompt as a langchain `PromptTemplate`.

To pull a **private prompt** you do not need to specify the owner handle (though you can, if you have one set).

To pull a **public prompt** from the LangChain Hub, you need to specify the handle of the prompt's author.

```python Python
from langsmith import Client
from langchain_openai import ChatOpenAI

client = Client()
prompt = client.pull_prompt("joke-generator")
model = ChatOpenAI(model="gpt-5.4-mini")
chain = prompt | model
chain.invoke({"topic": "cats"})
```

```python LangChain (Python)
from langchain_classic import hub as prompts
from langchain_openai import ChatOpenAI

prompt = prompts.pull("joke-generator")
model = ChatOpenAI(model="gpt-5.4-mini")
chain = prompt | model
chain.invoke({"topic": "cats"})
```

```typescript TypeScript
import * as hub from "langchain/hub";
import { ChatOpenAI } from "@langchain/openai";

const prompt = await hub.pull("joke-generator");
const model = new ChatOpenAI({ model: "gpt-5.4-mini" });
const chain = prompt.pipe(model);
await chain.invoke({"topic": "cats"});
```

```java Java
import com.langchain.smith.client.LangsmithClient;
import com.langchain.smith.client.okhttp.LangsmithOkHttpClient;
import com.langchain.smith.prompts.Prompt;
import com.langchain.smith.prompts.PromptClient;
import com.langchain.smith.prompts.PromptValue;
import java.util.Map;

LangsmithClient client = LangsmithOkHttpClient.fromEnv();
PromptClient promptClient = PromptClient.create(client);

Prompt prompt = promptClient.pull("joke-generator");
PromptValue formattedPrompt = prompt.invoke(Map.of("topic", "cats"));
// Use formattedPrompt with your model provider — see "Use a prompt without LangChain" below.
```

Similar to pushing a prompt, you can also pull a prompt as a RunnableSequence of a prompt and a model. Just specify include\_model when pulling the prompt. If the stored prompt includes a model, it will be returned as a RunnableSequence. Make sure you have the proper environment variables set for the model you are using.

```python Python
from langsmith import Client

client = Client()
chain = client.pull_prompt("joke-generator-with-model", include_model=True)
chain.invoke({"topic": "cats"})
```

```python LangChain (Python)
from langchain_classic import hub as prompts

chain = prompts.pull("joke-generator-with-model", include_model=True)
chain.invoke({"topic": "cats"})
```

```typescript TypeScript
import * as hub from "langchain/hub";
import { Runnable } from "@langchain/core/runnables";

const chain = await hub.pull<Runnable>("joke-generator-with-model", { includeModel: true });
await chain.invoke({"topic": "cats"});
```

When pulling a prompt, you can also specify a specific commit hash or [commit tag](Manage%20prompts.md#commit-tags) to pull a specific version of the prompt.

```python Python
prompt = client.pull_prompt("joke-generator:12344e88")
```

```python LangChain (Python)
prompt = prompts.pull("joke-generator:12344e88")
```

```typescript TypeScript
const prompt = await hub.pull("joke-generator:12344e88")
```

```java Java
String commitHash = "12344e88";
Prompt promptAtCommit = promptClient.pull("joke-generator:" + commitHash);
```

To pull a public prompt from the LangChain Hub, you need to specify the handle of the prompt's author.

```python Python
prompt = client.pull_prompt("efriis/my-first-prompt")
```

```python LangChain (Python)
prompt = prompts.pull("efriis/my-first-prompt")
```

```typescript TypeScript
const prompt = await hub.pull("efriis/my-first-prompt")
```

```java Java
Prompt publicPrompt = promptClient.pull("efriis/my-first-prompt");
```

> [!NOTE]
>
> For pulling prompts, if you are using Node.js or an environment that supports dynamic imports, we recommend using the `langchain/hub/node` entrypoint, as it handles deserialization of models associated with your prompt configuration automatically.
>
> If you are in a non-Node environment, "includeModel" is not supported for non-OpenAI models and you should use the base `langchain/hub` entrypoint.

## Use with the LLM Gateway

If your workspace uses the [LLM Gateway](../../../../LLM%20Gateway/Get%20started/LLM%20Gateway.md), you can route prompt model calls through it by setting an environment variable before pulling and invoking your prompt. No other code changes are required.

```bash
export LANGSMITH_GATEWAY="true"
```

This uses your existing `LANGSMITH_API_KEY` for authentication. To use a regional gateway instance instead of the default, set `LANGSMITH_GATEWAY` to the full gateway URL:

```bash
export LANGSMITH_GATEWAY="https://eu.gateway.smith.langchain.com"
```

> [!NOTE]
>
> If you need to use a different API key for gateway calls than your default `LANGSMITH_API_KEY`, set `LANGSMITH_GATEWAY_API_KEY` as an override. It must be a workspace-scoped key with the `gateway:invoke` permission. For key types and permissions, see [Authenticate to the LLM Gateway](../../../../LLM%20Gateway/Authentication/Authenticate%20to%20the%20LLM%20Gateway.md).

Once the environment variables are set, pull and invoke a prompt with a model as normal:

```python Python
from langsmith import Client

client = Client()

# Pull a prompt that includes a stored model configuration
prompt_with_model = client.pull_prompt("my-prompt", include_model=True)

# The model call is routed through the gateway automatically
result = prompt_with_model.invoke({"topic": "cats"})
```

> [!NOTE]
>
> Gateway routing for LangChain chat models requires Python and a supported `langchain-*` integration package. With an older integration package, the call bypasses the gateway and goes directly to the provider.

For supported providers and regional endpoints, see [Configure LangChain and Deep Agents](../../../../LLM%20Gateway/Call%20the%20gateway/Direct%20model%20access.md#configure-langchain-and-deep-agents).

## Prompt caching

The LangSmith SDK includes built-in in-memory caching for prompts. When enabled, LangSmith will cache pulled prompts in memory, reducing latency and API calls for frequently used prompts. The cache uses a global singleton instance that is shared across all clients and persists for the lifetime of the process. It implements a stale-while-revalidate pattern, ensuring your application always gets a fast response while keeping prompts up-to-date in the background.

**Requirements:**

* Python SDK: `langsmith >= 0.7.0`
* TypeScript SDK: `langsmith >= 0.5.0`

### Default behavior

Caching is **enabled by default**. When enabled, the default settings are:

| Setting | Default | Description |
| - | - | - |
| `max_size` | 100 | Maximum number of prompts to cache |
| `ttl_seconds` | 300 (5 minutes) | Time before a cached prompt is considered stale |
| `refresh_interval_seconds` | 60 | How often to check for stale prompts and refresh them in the background |

When refreshing, the global cache will use the last client that requested a given prompt to fetch new data.

### Using the cache

By default, all clients use the global prompt cache. No configuration is needed:

```python Python
from langsmith import Client
# Obtain a reference to the global cache just for logging metrics
from langsmith.prompt_cache import prompt_cache_singleton

# Caching is enabled by default using the global singleton
client = Client()

# First pull - fetches from API and caches
prompt = client.pull_prompt("joke-generator")

# Subsequent pulls - returns cached version instantly
prompt = client.pull_prompt("joke-generator")

# Check cache metrics
print(f"Cache hits: {prompt_cache_singleton.metrics.hits}")
print(f"Cache misses: {prompt_cache_singleton.metrics.misses}")
print(f"Hit rate: {prompt_cache_singleton.metrics.hit_rate:.1%}")
```

```typescript TypeScript
import * as hub from "langchain/hub";
// Obtain a reference to the global cache just for logging metrics
import { promptCacheSingleton } from "langsmith";

// Caching is enabled by default
// First pull - fetches from API and caches
const prompt = await hub.pull("joke-generator");

// Subsequent pulls - returns cached version instantly
const prompt2 = await hub.pull("joke-generator");

// Check cache metrics
console.log(`Cache hits: ${promptCacheSingleton.metrics.hits}`);
console.log(`Cache misses: ${promptCacheSingleton.metrics.misses}`);
console.log(`Hit rate: ${(promptCacheSingleton.hitRate * 100).toFixed(1)}%`);
```

### Configuring the global cache

You can configure the global prompt cache that all clients use by default. This is useful when you want to customize caching behavior across your entire application:

```python Python
from langsmith import Client
from langsmith.prompt_cache import (
    configure_global_prompt_cache,
    prompt_cache_singleton,
)

# Configure global cache before creating any clients
configure_global_prompt_cache(
    max_size=200,  # Cache up to 200 prompts
    ttl_seconds=7200,  # Consider prompts stale after 2 hours
    refresh_interval_seconds=600,  # Check for stale prompts every 10 minutes
)

# All clients will use these settings
client1 = Client()
client2 = Client()

# Both clients share the same global cache with your custom settings
prompt1 = client1.pull_prompt("prompt-1")
prompt2 = client2.pull_prompt("prompt-2")

# Check global cache metrics
print(f"Global cache hits: {prompt_cache_singleton.metrics.hits}")
print(f"Global cache misses: {prompt_cache_singleton.metrics.misses}")
```

```typescript TypeScript
import * as hub from "langchain/hub";
import {
  configureGlobalPromptCache,
  promptCacheSingleton,
} from "langsmith";

// Configure global cache before pulling prompts
configureGlobalPromptCache({
  maxSize: 200,  // Cache up to 200 prompts
  ttlSeconds: 7200,  // Consider prompts stale after 2 hours
  refreshIntervalSeconds: 600,  // Check for stale prompts every 10 minutes
});

// All hub.pull calls will use these settings
const prompt1 = await hub.pull("prompt-1");
const prompt2 = await hub.pull("prompt-2");

// Check global cache metrics
console.log(`Global cache hits: ${promptCacheSingleton.metrics.hits}`);
console.log(`Global cache misses: ${promptCacheSingleton.metrics.misses}`);
```

### Disabling the cache

To disable caching for a specific client, pass `disable_prompt_cache=True`. You can also configure a max size of zero globally:

```python Python
from langsmith import Client

# Disable caching for this client
client = Client(disable_prompt_cache=True)

# Every pull will fetch from the API
prompt = client.pull_prompt("joke-generator")
```

```typescript TypeScript
import * as hub from "langchain/hub";
import { configureGlobalPromptCache } from "langsmith";

// Disable caching globally
configureGlobalPromptCache({ maxSize: 0 });

// Every pull will fetch from the API
const prompt = await hub.pull("joke-generator");
```

### Skipping the cache

To bypass the cache and fetch a fresh prompt from the API for an individual request, use the `skip_cache` parameter:

```python Python
# Force a fresh fetch, ignoring any cached version
prompt = client.pull_prompt("joke-generator", skip_cache=True)
```

```typescript TypeScript
import * as hub from "langchain/hub";

// Force a fresh fetch, ignoring any cached version
const prompt = await hub.pull("joke-generator", { skipCache: true });
```

This is useful when you need to ensure you have the latest version of a prompt, such as after making changes in the LangSmith UI.

### Offline mode

For environments with limited or no network connectivity, you can pre-populate the cache and use it offline. Set `ttl_seconds` to `None` (Python) or `null` (TypeScript) to prevent cache entries from expiring and disable background refresh.

**Step 1: Export your prompts to a cache file (while online)**

```python Python
from langsmith import Client
from langsmith.prompt_cache import prompt_cache_singleton

# Create client (caching is enabled by default)
client = Client()

# Pull the prompts you need
client.pull_prompt("prompt-1")
client.pull_prompt("prompt-2")
client.pull_prompt("prompt-3")

# Export cache to a file
prompt_cache_singleton.dump("prompts_cache.json")
```

```typescript TypeScript
import * as hub from "langchain/hub";
import { promptCacheSingleton } from "langsmith";

// Caching is enabled by default

// Pull the prompts you need
await hub.pull("prompt-1");
await hub.pull("prompt-2");
await hub.pull("prompt-3");

// Export cache to a file
promptCacheSingleton.dump("prompts_cache.json");
```

**Step 2: Load the cache file in your offline environment**

```python Python
from langsmith import Client
from langsmith.prompt_cache import (
    configure_global_prompt_cache,
    prompt_cache_singleton,
)

# Configure cache with infinite TTL (never expire, no background refresh)
configure_global_prompt_cache(ttl_seconds=None)

# Load the cache file
prompt_cache_singleton.load("prompts_cache.json")

# Create client (uses the loaded cache)
client = Client()

# Uses cached version without any API calls
prompt = client.pull_prompt("prompt-1")
```

```typescript TypeScript
import * as hub from "langchain/hub";
import {
  configureGlobalPromptCache,
  promptCacheSingleton,
} from "langsmith";

// Configure cache with infinite TTL (never expire, no background refresh)
configureGlobalPromptCache({ ttlSeconds: null });

// Load the cache file
promptCacheSingleton.load("prompts_cache.json");

// Uses cached version without any API calls
const prompt = await hub.pull("prompt-1");
```

### Cache operations

The cache supports several operations for managing cached prompts:

```python Python
from langsmith import Client
from langsmith.prompt_cache import prompt_cache_singleton

client = Client()

# Invalidate a specific prompt from cache
prompt_cache_singleton.invalidate("joke-generator:latest")

# Clear all cached prompts
prompt_cache_singleton.clear()

# Reset metrics
prompt_cache_singleton.reset_metrics()

# Check if cache is running background refresh
# (only runs if ttl_seconds is not None)
if prompt_cache_singleton._refresh_thread is not None:
    print("Background refresh is active")
```

```typescript TypeScript
import { promptCacheSingleton } from "langsmith";

// Invalidate a specific prompt from cache
promptCacheSingleton.invalidate("joke-generator:latest");

// Clear all cached prompts
promptCacheSingleton.clear();

// Reset metrics
promptCacheSingleton.resetMetrics();
```

### Cleanup

You can manually call `stop()` to stop the background refresh task:

```python Python
prompt_cache_singleton.stop()
```

```typescript TypeScript
promptCacheSingleton.stop();
```

> [!NOTE]
>
> The background refresh task is only started when you first set a value in the cache, and only if `ttl_seconds` is not `None`. If `ttl_seconds` is `None` (offline mode), no background task is created.

## Use a prompt without LangChain

If you want to store your prompts in LangSmith but use them directly with a model provider's API, you can use our conversion methods. These convert your prompt into the payload required for the OpenAI or Anthropic API.

These conversion methods rely on logic from within LangChain integration packages, and you will need to install the appropriate package as a dependency in addition to your official SDK of choice. Here are some examples:

### OpenAI

```bash Python
pip install -U langchain_openai
```

```bash TypeScript
yarn add @langchain/openai @langchain/core # @langchain/openai version >= 0.3.2
```

```python Python
from openai import OpenAI
from langsmith.client import Client, convert_prompt_to_openai_format

# langsmith client
client = Client()
# openai client
oai_client = OpenAI()

# pull prompt and invoke to populate the variables
prompt = client.pull_prompt("joke-generator")
prompt_value = prompt.invoke({"topic": "cats"})
openai_payload = convert_prompt_to_openai_format(prompt_value)
openai_response = oai_client.chat.completions.create(**openai_payload)
```

```typescript TypeScript
import * as hub from "langchain/hub";
import { convertPromptToOpenAI } from "@langchain/openai";
import OpenAI from "openai";

const prompt = await hub.pull("jacob/joke-generator");
const formattedPrompt = await prompt.invoke({
  topic: "cats",
});
const { messages } = convertPromptToOpenAI(formattedPrompt);

const openAIClient = new OpenAI();
const openAIResponse = await openAIClient.chat.completions.create({
  model: "gpt-5.4-mini",
  messages,
});
```

```java Java
import static com.langchain.smith.prompts.PromptConverters.convertToOpenAIParams;
import com.langchain.smith.client.LangsmithClient;
import com.langchain.smith.client.okhttp.LangsmithOkHttpClient;
import com.langchain.smith.prompts.Prompt;
import com.langchain.smith.prompts.PromptClient;
import com.langchain.smith.prompts.PromptValue;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.ChatModel;
import com.openai.models.chat.completions.ChatCompletion;
import java.util.Map;

LangsmithClient client = LangsmithOkHttpClient.fromEnv();
PromptClient promptClient = PromptClient.create(client);
OpenAIClient openai = OpenAIOkHttpClient.fromEnv();

Prompt prompt = promptClient.pull("jacob/joke-generator");
PromptValue formattedPrompt = prompt.invoke(Map.of("topic", "cats"));

ChatCompletion completion = openai.chat().completions().create(
    convertToOpenAIParams(formattedPrompt)
        .model(ChatModel.GPT_4_1_MINI)
        .build()
);
```

### Anthropic

```bash Python
pip install -U langchain_anthropic
```

```bash TypeScript
yarn add @langchain/anthropic @langchain/core # @langchain/anthropic version >= 0.3.3
```

```python Python
from anthropic import Anthropic
from langsmith.client import Client, convert_prompt_to_anthropic_format

# langsmith client
client = Client()
# anthropic client
anthropic_client = Anthropic()

# pull prompt and invoke to populate the variables
prompt = client.pull_prompt("joke-generator")
prompt_value = prompt.invoke({"topic": "cats"})
anthropic_payload = convert_prompt_to_anthropic_format(prompt_value)
anthropic_response = anthropic_client.messages.create(**anthropic_payload)
```

```typescript TypeScript
import * as hub from "langchain/hub";
import { convertPromptToAnthropic } from "@langchain/anthropic";
import Anthropic from "@anthropic-ai/sdk";

const prompt = await hub.pull("jacob/joke-generator");
const formattedPrompt = await prompt.invoke({
  topic: "cats",
});
const { messages, system } = convertPromptToAnthropic(formattedPrompt);

const anthropicClient = new Anthropic();
const anthropicResponse = await anthropicClient.messages.create({
  model: "claude-haiku-4-5-20251001",
  system,
  messages,
  max_tokens: 1024,
  stream: false,
});
```

```java Java
import static com.langchain.smith.prompts.PromptConverters.convertToAnthropicParams;
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.Model;
import com.langchain.smith.client.LangsmithClient;
import com.langchain.smith.client.okhttp.LangsmithOkHttpClient;
import com.langchain.smith.prompts.Prompt;
import com.langchain.smith.prompts.PromptClient;
import com.langchain.smith.prompts.PromptValue;
import java.util.Map;

LangsmithClient client = LangsmithOkHttpClient.fromEnv();
PromptClient promptClient = PromptClient.create(client);
AnthropicClient anthropic = AnthropicOkHttpClient.fromEnv();

Prompt prompt = promptClient.pull("jacob/joke-generator");
PromptValue formattedPrompt = prompt.invoke(Map.of("topic", "cats"));

Message message = anthropic.messages().create(
    convertToAnthropicParams(formattedPrompt)
        .model(Model.CLAUDE_SONNET_4_5)
        .maxTokens(1024)
        .build()
);
```

## List, delete, and like prompts

You can also list, delete, and like/unlike prompts using the `list prompts`, `delete prompt`, `like prompt` and `unlike prompt` methods. See the [Python SDK](https://github.com/langchain-ai/langsmith-python) and [JavaScript SDK](https://github.com/langchain-ai/langsmith-javascript) for extensive documentation on these methods.

```python Python
# List all prompts in my workspace
prompts = client.list_prompts()

# List my private prompts that include "joke"
prompts = client.list_prompts(query="joke", is_public=False)

# Delete a prompt
client.delete_prompt("joke-generator")

# Like a prompt
client.like_prompt("efriis/my-first-prompt")

# Unlike a prompt
client.unlike_prompt("efriis/my-first-prompt")
```

```typescript TypeScript
// List all prompts in my workspace
import Client from "langsmith";

const client = new Client({ apiKey: "lsv2_..." });
const prompts = client.listPrompts();

for await (const prompt of prompts) {
  console.log(prompt);
}

// List my private prompts that include "joke"
const private_joke_prompts = client.listPrompts({ query: "joke", isPublic: false});

// Delete a prompt
client.deletePrompt("joke-generator");

// Like a prompt
client.likePrompt("efriis/my-first-prompt");

// Unlike a prompt
client.unlikePrompt("efriis/my-first-prompt");
```

```java Java
import com.langchain.smith.client.LangsmithClient;
import com.langchain.smith.client.okhttp.LangsmithOkHttpClient;
import com.langchain.smith.models.repos.RepoDeleteParams;
import com.langchain.smith.models.repos.RepoListPage;
import com.langchain.smith.models.repos.RepoListParams;
import com.langchain.smith.models.repos.RepoWithLookups;

LangsmithClient client = LangsmithOkHttpClient.fromEnv();

// List all prompts in my workspace
RepoListPage prompts = client.repos().list();
for (RepoWithLookups prompt : prompts.repos()) {
    System.out.println(prompt.repoHandle());
}

// List my private prompts that include "joke"
RepoListPage jokePrompts = client.repos().list(
    RepoListParams.builder()
        .query("joke")
        .isPublic(RepoListParams.IsPublic.FALSE)
        .build()
);

// Delete a prompt
client.repos().delete(
    RepoDeleteParams.builder()
        .owner("-")
        .repo("joke-generator")
        .build()
);
```
