# Fine-tune models with Smithtune

> Use Smithtune to fine-tune models on LangSmith conversations and compare the results in LangSmith.

> [!NOTE]
>
> Smithtune is in [beta](../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md).

Smithtune is a command-line tool for fine-tuning models on [trajectories](../../../Monitor/Trace/Observability%20concepts.md#trajectories) recorded in LangSmith. It trains a model with [Fireworks](https://fireworks.ai/) or [Baseten](https://www.baseten.co/) and compares the base and tuned models in a LangSmith [experiment](../../Get%20started/Evaluation%20concepts.md#experiment). You can optionally deploy the tuned model as an endpoint for your application.

## How Smithtune works

**1. Create a dataset**

Select trajectories from a tracing project with a [trace query](../../../Monitor/Debug/Viewing%20%26%20managing%20traces/Trace%20query%20syntax.md) filter, a model judge, or both.

**2. Prepare data**

Validate the trajectories, then split them into training, validation, and test data. Each trajectory stays in one split.

**3. Train a model**

Preview the run, then fine-tune a supported model with your provider.

**4. Compare results**

Evaluate the base and tuned models on the test data, then [compare the experiments](../Analyze%20experiment%20results/How%20to%20compare%20experiment%20results.md) in LangSmith. Evaluation does not require a deployed endpoint.

**5. Deploy an endpoint (optional)**

Serve the tuned model for your application. To run an agent that uses it in production, see [LangSmith Agent Server](../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md).

> [!TIP]
>
> To have your coding agent drive the fine-tuning process end to end, use the [Smithtune skill](https://github.com/langchain-ai/smithtune/blob/main/src/smithtune/skills/smithtune/SKILL.md).

Evaluation scores measure how closely each model matches the recorded behavior, not whether it completes tasks end to end. Smithtune does not execute the tool calls the model generates.

## Set up Smithtune

Smithtune requires trajectories in a tracing project or a LangSmith trajectory dataset. You also need API keys for LangSmith, your training provider, and a judge model. Training, evaluation, and deployed endpoints incur charges from the services you use.

To set up Smithtune:

1. Install Smithtune and the [LangSmith CLI](../../../LangSmith%20setup/Govern/Tools/LangSmith%20CLI.md), and set your API keys. Follow the [Smithtune README](https://github.com/langchain-ai/smithtune#readme) for the install command and the environment variables each provider needs.

2. Read the [data rights and permitted use terms](https://github.com/langchain-ai/smithtune/blob/main/docs/data-rights-and-permitted-use.md) linked from the [README](https://github.com/langchain-ai/smithtune#readme), then acknowledge them before your first run:

   ```bash
   smithtune acknowledge-data-rights
   ```

3. Check your local setup:

   ```bash
   smithtune doctor
   ```

For the commands in each step, see the [README](https://github.com/langchain-ai/smithtune#readme) or run `smithtune --help`.

## See also

* [Trajectory evaluations](../Evaluation%20techniques/Define%20evaluation%20target/How%20to%20evaluate%20your%20agent%20with%20trajectory%20evaluations.md)
* [Query threads](../../../Monitor/Debug/Viewing%20%26%20managing%20traces/Query%20threads%20using%20the%20SDK.md)
* [Manage datasets](../Datasets/Manage%20datasets.md)
