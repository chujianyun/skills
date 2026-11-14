# LangSmith Evaluation

> Evaluate and test agent quality at scale with datasets, evaluators, prompts, and Studio.

LangSmith's testing tools help you measure agent quality, iterate on prompts, and debug live in an interactive environment. Evaluation is the core of testing: it scores your agent's outputs against datasets and criteria so you can benchmark versions, catch regressions, and track quality over time.

Add real traces to a dataset so a failure you saw once becomes a test you run every time.

LangSmith supports two types of evaluation based on when and where they run:

> [card] Offline Evaluation
>
> **Test before you ship**
>
> Run evaluations on curated datasets during development to compare versions, benchmark performance, and catch regressions.

> [card] Online Evaluation
>
> **Monitor in production**
>
> Evaluate real user interactions in real-time to detect issues and measure quality on live traffic.

## Set up your account

**1. Create an account**

Sign up at [smith.langchain.com](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=snippets-langsmith-account-api-key-quickstart) (no credit card required).
You can log in with **Google**, **GitHub**, or **email**.

**2. Create an API key**

Go to your [Settings page](https://smith.langchain.com/settings) > **API Keys** > **Create API Key**.
Copy the key and save it securely.

Once your account and API key are ready, [run your first evaluation](Evaluation%20quickstart.md).

## Evaluation workflow

> [tab] Offline evaluation flow
>
> **1. Create a dataset**
>
> Create a [dataset](../Datasets%20%26%20Experiments/Datasets/Manage%20datasets.md) with [examples](Evaluation%20concepts.md#examples) (Individual test cases with inputs and reference outputs) from manually curated test cases, historical production traces, or synthetic data generation.
>
> **2. Define evaluators**
>
> Create [evaluators](Evaluation%20concepts.md#evaluators) (Functions that score how well your application performs) to score performance:
>
> * [Human](Evaluation%20concepts.md#human) review
> * [Code](Evaluation%20concepts.md#code) rules
> * [LLM-as-judge](../Evaluators/Evaluator%20types/UI/How%20to%20define%20an%20LLM-as-a-judge%20evaluator.md)
> * [Pairwise](../Evaluators/Evaluator%20types/SDK/How%20to%20run%20a%20pairwise%20evaluation.md) comparison
>
> **3. Run an experiment**
>
> Execute your application on the dataset to create an [experiment](Evaluation%20concepts.md#experiment) (Results of evaluating a specific application version on a dataset). Configure [repetitions, concurrency, and caching](../Datasets%20%26%20Experiments/Evaluation%20techniques/Experiment%20configuration/Experiment%20configuration.md) to optimize runs.
>
> **4. Analyze results**
>
> Compare experiments for [benchmarking](../Evaluators/Evaluation%20types.md#benchmarking), [unit tests](../Evaluators/Evaluation%20types.md#unit-tests), [regression tests](../Evaluators/Evaluation%20types.md#regression-tests), or [backtesting](../Evaluators/Evaluation%20types.md#backtesting).

> [tab] Online evaluation flow
>
> **1. Deploy your application**
>
> Each interaction creates a [run](Evaluation%20concepts.md#runs) (A single execution trace including inputs, outputs, and intermediate steps) without reference outputs.
>
> **2. Configure online evaluators**
>
> Set up [evaluators](../../Monitor/Observe/Online%20evaluators/Set%20up%20LLM-as-a-judge%20online%20evaluators.md) to run automatically on production traces: safety checks, format validation, quality heuristics, and reference-free LLM-as-judge. Apply [filters and sampling rates](../../Monitor/Observe/Online%20evaluators/Set%20up%20LLM-as-a-judge%20online%20evaluators.md#configure-a-sampling-rate) to control costs.
>
> **3. Monitor in real-time**
>
> Evaluators run automatically on [runs](Evaluation%20concepts.md#runs) or [threads](../../Monitor/Observe/Online%20evaluators/Set%20up%20multi-turn%20online%20evaluators.md) (Collections of related runs forming multi-turn conversations), providing real-time monitoring, anomaly detection, and alerting.
>
> **4. Establish a feedback loop**
>
> Add failing production traces to your [dataset](../Datasets%20%26%20Experiments/Datasets/Manage%20datasets.md), create targeted evaluators, validate fixes with offline experiments, and redeploy.

> [!TIP]
>
> For more on the differences between offline and online evaluation, refer to the [Evaluation concepts](Evaluation%20concepts.md#quick-reference-offline-vs-online-evaluation) page.

## Get started

> [card] [Evaluation quickstart](Evaluation%20quickstart.md)
>
> Get started with offline evaluation.

> [card] [Manage datasets](../Datasets%20%26%20Experiments/Datasets/Manage%20datasets.md)
>
> Create and manage datasets for evaluation through the UI or SDK.

> [card] [Run offline evaluations](../Datasets%20%26%20Experiments/Run%20an%20evaluation/How%20to%20evaluate%20agents.md)
>
> Explore evaluation types, techniques, and frameworks for comprehensive testing.

> [card] [Analyze results](../Datasets%20%26%20Experiments/Analyze%20experiment%20results/Analyze%20an%20experiment.md)
>
> View and analyze evaluation results, compare experiments, filter data, and export findings.

> [card] [Run online evaluations](../../Monitor/Observe/Online%20evaluators/Set%20up%20LLM-as-a-judge%20online%20evaluators.md)
>
> Monitor production quality in real-time from the Observability tab.

> [card] [Follow tutorials](../Datasets%20%26%20Experiments/Tutorials/Evaluate%20a%20chatbot.md)
>
> Learn by following step-by-step tutorials, from simple chatbots to complex agent evaluations.

> [card] [Studio](../Test%20from%20Studio/LangSmith%20Studio.md)
>
> Use an interactive environment for developing and debugging agents.

> [!NOTE]
>
> To set up a LangSmith instance, visit the [Platform setup section](../../LangSmith%20setup/Overview/Hosting/Set%20up%20LangSmith.md) to choose between cloud, hybrid, or self-hosted. All options include observability, evaluation, prompt engineering, and deployment.
