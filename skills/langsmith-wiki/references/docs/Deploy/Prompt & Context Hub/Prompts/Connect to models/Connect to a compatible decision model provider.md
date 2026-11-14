# Connect to a compatible decision model provider

> Point LangSmith decision model evaluators at any server that implements the OpenAI Decisions API or the TypeSafe System One API, such as OpenRouter or a self-hosted model.

A compatible endpoint is a saved [model configuration](../../../../LangSmith%20setup/Govern/Organization/Workspace%20setup/Manage%20model%20configurations.md) that sends a decision model evaluator's requests to a server you choose. With a compatible endpoint, you can call a decision model through another provider, such as OpenRouter, or call a decision model you host yourself. LangSmith supports two kinds:

* **OpenAI-Decisions-compatible endpoint**: Calls any server that implements the [OpenAI Decisions API](https://developers.openai.com/api/docs/guides/decisions), with any model name that server serves.
* **TypeSafe-compatible endpoint**: Calls any server that implements the [TypeSafe System One API](https://docs.typesafe.ai).

Compatible endpoints are available in [decision model evaluators](../../../../Test/Evaluators/Evaluator%20types/UI/How%20to%20define%20a%20decision%20model%20evaluator.md). You can also call a TypeSafe-compatible endpoint through the LLM Gateway as a [custom model configuration](../../../../LLM%20Gateway/Models%20and%20reliability/Custom%20model%20configurations.md). To use `gpt-6-luna` directly from OpenAI or Jev directly from TypeSafe, you do not need a compatible endpoint. For chat models that implement the OpenAI API, see [Connect to an OpenAI compliant model provider/proxy](Connect%20to%20an%20OpenAI%20compliant%20model%20provider-proxy.md).

## Configuration

A compatible endpoint has three settings:

* **Model**: The model ID the server expects.
* **API Key Name**: The name of the workspace secret that stores the server's API key.
* **Base URL**: The root of the server's API. See [Base URL format](#base-url-format).

The defaults depend on the kind of endpoint:

| Setting | OpenAI-Decisions-compatible endpoint | TypeSafe-compatible endpoint |
| - | - | - |
| Model | `gpt-6-luna` | `jev-latest` |
| API Key Name | `OPENAI_API_KEY` | `TYPESAFE_API_KEY` |

## Use the endpoint in an evaluator

An evaluator can use a compatible endpoint only after you save the endpoint as a model configuration.

To use a compatible endpoint in an evaluator:

1. Add the server's API key as a workspace secret. Go to **Settings > Integrations > Provider secrets**, click **+ Secret**, and select **Custom** to enter your own secret name. To use the default name, select **OpenAI** or **TypeSafe** instead.
2. In the evaluator, under **Prompt & Model**, open **Model Configuration**.
3. For **Provider**, select **OpenAI Decisions Compatible Endpoint** or **TypeSafe Compatible Endpoint**. Both appear under **Other**.
4. Enter the **Model**, **API Key Name**, and **Base URL**.
5. Click **Save as preset** and name the configuration.
6. Select the saved configuration as the evaluator's model.

When the evaluator runs, it calls the endpoint with the API key stored in the secret you entered in **API Key Name**. Next, add questions and save the evaluator, as described in [How to define a decision model evaluator](../../../../Test/Evaluators/Evaluator%20types/UI/How%20to%20define%20a%20decision%20model%20evaluator.md).

## Base URL format

The **Base URL** should point to the root of the server's API. The path LangSmith adds depends on the kind of endpoint.

### OpenAI-Decisions-compatible endpoints

LangSmith appends `/v1/decisions` to the Base URL, so do not include it.

| Provider | Model | Example Base URL |
| - | - | - |
| [OpenAI](https://developers.openai.com/api/docs/guides/decisions) | `gpt-6-luna` | `https://api.openai.com` |
| Self-hosted (remote) | Your model ID | `https://decisions.example.com` |

### TypeSafe-compatible endpoints

LangSmith appends `/v1/systemone` to the Base URL, so do not include it. To call the URL exactly as entered, including its path, clear **Append /v1/systemone**.

| Provider | Model | Example Base URL |
| - | - | - |
| [TypeSafe](https://docs.typesafe.ai) | `jev-latest` | `https://api.typesafe.ai` |
| [OpenRouter](https://openrouter.ai) | `~typesafe/jev-latest` | `https://openrouter.ai/api` |
| Self-hosted (remote) | Your model ID | `https://my-model-server.example.com` |

## See also

* [How to define a decision model evaluator](../../../../Test/Evaluators/Evaluator%20types/UI/How%20to%20define%20a%20decision%20model%20evaluator.md): Set up an evaluator that uses a decision model.
* [Decision models in the LLM Gateway](../../../../LLM%20Gateway/Call%20the%20gateway/Decision%20models.md): Call decision models through the LLM Gateway from your own application.
* [Model configurations](../../../../LangSmith%20setup/Govern/Organization/Workspace%20setup/Manage%20model%20configurations.md): Manage saved model configurations for your workspace.
