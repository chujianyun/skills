# Evaluation concepts

LLM outputs are non-deterministic, which makes response quality hard to assess. Evaluations (evals) are a way to breakdown what "good" looks like and measure it. LangSmith Evaluation provides a framework for measuring quality throughout the application lifecycle, from pre-deployment testing to production monitoring.

## What to evaluate

Before building evaluations, identify what matters for your application. Break down your system into its critical components—LLM calls, retrieval steps, tool invocations, output formatting—and determine quality criteria for each.

**Start with manually curated examples.** Create 5-10 examples of what "good" looks like for each critical component. These examples serve as your ground truth and inform which evaluation approaches to use. For instance:

* **RAG system**: Examples of good retrievals (relevant documents) and good answers (accurate, complete).
* **Agent**: Examples of correct tool selection and proper argument formatting or trajectory that the agent took.
* **Chatbot**: Examples of helpful, on-brand responses that address user intent.

Once you've defined "good" through examples, you can measure how often your system produces similar quality outputs.

## Offline and online evaluations

LangSmith supports two types of evaluations that serve different purposes in your development workflow:

### Offline evaluations

&#x20;Use offline evaluations for **pre-deployment testing**:

* **Benchmarking**: Compare multiple versions to find the best performer.
* **Regression testing**: Ensure new versions don't degrade quality.
* **Unit testing**: Verify correctness of individual components.
* **Backtesting**: Test new versions against historical data.

Offline evaluations target [*examples*](#examples) from [*datasets*](#datasets): curated test cases with reference outputs that define what "good" looks like.

### Online evaluations

&#x20;Use online evaluations for **production monitoring**:

* **Real-time monitoring**: Track quality continuously on live traffic.
* **Anomaly detection**: Flag unusual patterns or edge cases.
* **Production feedback**: Identify issues to add to offline datasets.

Online evaluations target [*runs*](#runs) and [*threads*](#threads) from [tracing](../../Monitor/Trace/Tracing%20quickstart.md): real production traces without reference outputs.

This difference in targets determines what you can evaluate: offline evaluations can check correctness against expected answers, while online evaluations focus on quality patterns, safety, and real-world behavior.

## Evaluation lifecycle

As you develop and [deploy your application](../../Deploy/Get%20started/LangSmith%20Agent%20Server.md), your evaluation strategy evolves from pre-deployment testing to production monitoring. During development and testing, offline evaluations validate functionality against curated datasets. After deployment, online evaluations monitor production behavior on live traffic. As applications mature, both evaluation types work together in an iterative feedback loop to improve quality continuously.

```mermaid
graph LR
    A[Development] --> B[Testing]
    B --> C[Deployment]
    C --> D[Monitoring]
    D --> E[Iteration]

    A -.-> F[Offline]
    B -.-> F
    C -.-> G[Online]
    D -.-> G
    E -.-> H[Both]

    classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710

    class A,B,C,D,E process

    style F fill:#EBD0F0,stroke:#885270,color:#441E33
    style G fill:#EBD0F0,stroke:#885270,color:#441E33
    style H fill:#EBD0F0,stroke:#885270,color:#441E33
```

### 1. Development with offline evaluation

Before production deployment, use offline evaluations to validate functionality, benchmark different approaches, and build confidence.

Follow the [quickstart](Evaluation%20quickstart.md) to run your first offline evaluation.

### 2. Initial deployment with online evaluation

After deployment, use online evaluations to monitor production quality, detect unexpected issues, and collect real-world data.

Learn how to [configure online evaluations](../../Monitor/Observe/Online%20evaluators/Set%20up%20LLM-as-a-judge%20online%20evaluators.md) for production monitoring.

### 3. Continuous improvement

Use both evaluation types together in an iterative feedback loop. Online evaluations surface issues that become offline test cases, offline evaluations validate fixes, and online evaluations confirm production improvements.

## Core evaluation targets

Evaluations run on different targets depending on whether they are offline or online.

### Targets for offline evaluation

Offline evaluations run on datasets and examples. The presence of reference outputs enables comparison between expected and actual results.

#### Datasets

A dataset is a *collection of examples* used for evaluating an application. An example is a test input, reference output pair.

![List of datasets on the Examples tab in the LangSmith UI.](../../../assets/images/d6c6dec87c98-datasets-light.png)

#### Examples

Each example consists of:

* **Inputs**: a dictionary of input variables to pass to your application.
* **Reference outputs** (optional): a dictionary of reference outputs. These do not get passed to your application, they are only used in evaluators.
* **Metadata** (optional): a dictionary of additional information that can be used to create filtered views of a dataset.

![Example in the LangSmith UI.](../../../assets/images/c58649ba9d9e-example-light.png)

Learn more about [managing datasets](../Datasets%20%26%20Experiments/Datasets/Manage%20datasets.md).

#### Experiment

An *experiment* represents the results of evaluating a specific application version on a dataset. Each experiment captures outputs, evaluator scores, and execution traces for every example in the dataset.

![Experiment view](../../../assets/images/bddd0eac6e1c-experiment-view.png)

Multiple experiments typically run on a given dataset to test different application configurations (e.g., different prompts or LLMs). LangSmith displays all experiments associated with a dataset and supports [comparing multiple experiments](../Datasets%20%26%20Experiments/Analyze%20experiment%20results/How%20to%20compare%20experiment%20results.md) side-by-side.

Learn [how to analyze experiment results](../Datasets%20%26%20Experiments/Analyze%20experiment%20results/Analyze%20an%20experiment.md).

### Targets for online evaluation

Online evaluations run on runs and threads from production traffic. Without reference outputs, evaluators focus on detecting issues, anomalies, and quality degradation in real-time.

#### Runs

A *run* is a single execution trace from your [deployed application](../../Deploy/Get%20started/LangSmith%20Agent%20Server.md). Each run contains:

* **Inputs**: The actual user inputs your application received.
* **Outputs**: What your application actually returned.
* **Intermediate steps**: All the child runs (tool calls, LLM calls, and so on).
* **Metadata**: Tags, user feedback, latency metrics, etc.

Unlike examples in datasets, runs do not include reference outputs. Online evaluators must assess quality without knowing what the "correct" answer should be, relying instead on quality heuristics, safety checks, and reference-free evaluation techniques.

Learn more about [runs and traces in the Observability concepts](../../Monitor/Trace/Observability%20concepts.md#runs).

#### Threads

*Threads* are collections of related runs representing multi-turn conversations. Online evaluators can run at the thread level to evaluate entire conversations rather than individual turns. This enables assessment of conversation-level properties like coherence across turns, topic maintenance, and user satisfaction throughout an interaction.

## Evaluators

*Evaluators* are workspace-level resources that score application performance. They provide the measurement layer for both offline and online evaluation, adapting their inputs based on what data is available. Because evaluators are scoped to the workspace, you can attach a single evaluator to multiple tracing projects and datasets without recreating it each time.

Run evaluators using any of the following:

* The [Evaluators](../Evaluators/Manage%20evaluators.md) page, to attach them to tracing projects, agent environments, or datasets
* The [Playground](../../Deploy/Prompt%20%26%20Context%20Hub/Prompts/Prompt%20engineering%20concepts.md#playground)
* The LangSmith SDK ([Python](../../Monitor/Reference/langsmith%20%28smith-python-sdk%29.md) and [TypeScript](../../Monitor/Reference/langsmith%20%28smith-js-ts-sdk%29.md))
* [Rules](../../Monitor/Observe/Automations/Set%20up%20automation%20rules.md), to run them automatically on tracing projects, agent environments, or datasets

### Attaching an evaluator to a tracing project or dataset

A single evaluator can be attached to many tracing projects, agent environments, and datasets. Configuration like sampling rate, filters, and [spend limits](../Evaluators/Track%20and%20limit%20evaluator%20spend.md) is set per attached project or dataset, not per evaluator. View an evaluator's attachments under its **Projects & Datasets** tab, called **Environments & Datasets** in an agent-based workspace.

### Evaluator inputs

Evaluator inputs differ based on evaluation type:

**Offline evaluators** receive:

* [Example](#examples): The example from your [dataset](#datasets), containing inputs, reference outputs, and metadata.
* [Run](../../Monitor/Trace/Observability%20concepts.md#runs): The actual outputs and intermediate steps from running the application on the example inputs.

**Online evaluators** receive:

* [Run](../../Monitor/Trace/Observability%20concepts.md#runs): The production trace containing inputs, outputs, and intermediate steps (no reference outputs available).

### Evaluator outputs

Evaluators return **feedback**, which is the scores from evaluation. Feedback is a dictionary or list of dictionaries. Each dictionary contains:

* `key`: The metric name.
* `score` | `value`: The metric value (`score` for numerical metrics, `value` for categorical metrics).
* `comment` (optional): Additional reasoning or explanation for the score.

### Evaluation techniques

LangSmith supports several evaluation approaches:

* [Human](#human)
* [Code](#code)
* [LLM-as-judge](#llm-as-judge)
* [Decision model](#decision-model)
* [Pairwise](#pairwise)

#### Human

*Human evaluation* involves manual review of application outputs and execution traces. This approach is [often an effective starting point for evaluation](https://hamel.dev/blog/posts/evals/#looking-at-your-traces). LangSmith provides tools to review application outputs and traces (all intermediate steps).

**Annotation queues**

[Annotation queues](../Annotation%20Queues/Use%20annotation%20queues.md) streamline structured collection of human feedback on runs. They complement [inline annotation](../Annotation%20Queues/Annotate%20traces%20and%20runs%20inline.md) by providing organized workflows with prescribed rubrics, team collaboration features, and progress tracking.

LangSmith supports two queue types:

* **Single-run queues**: Review one run at a time against custom rubric items. Useful for triaging issues or building datasets from production traces. Single-run queues also support [assertions](../Annotation%20Queues/Use%20assertions.md), free-form acceptance criteria that an offline evaluator can grade future runs against.
* **Pairwise queues**: Compare two runs side-by-side to judge which is better. Designed for fast A/B comparisons between experiments.

Key features include configuring multiple reviewers per run, enabling reservations to prevent conflicts, and exporting annotated runs directly to datasets for future evaluations.

#### Code

*Code evaluators* are deterministic, rule-based functions. They work well for checks such as verifying the structure of a chatbot's response is not empty, that generated code compiles, or that a classification matches exactly.

#### LLM-as-judge

*LLM-as-judge evaluators* use LLMs to score application outputs. The grading rules and criteria are typically encoded in the LLM prompt. These evaluators can be:

* **Reference-free**: Check if output contains offensive content or adheres to specific criteria.
* **Reference-based**: Compare output to a reference (e.g., check factual accuracy relative to the reference).

LLM-as-judge evaluators require careful review of scores and prompt tuning. Few-shot evaluators, which include examples of inputs, outputs, and expected grades in the grader prompt, often improve performance.

Learn about [how to define an LLM-as-a-judge evaluator](../Evaluators/Evaluator%20types/UI/How%20to%20define%20an%20LLM-as-a-judge%20evaluator.md).

#### Decision model

*Decision model evaluators* use a decision model, such as Jev, as the judge. Instead of a prompt and an output schema, you define typed questions: a probability that a statement is true, a choice from a fixed list, or a score along ordered levels. Each question's answer becomes its own piece of feedback.

Learn about [how to define a decision model evaluator](../Evaluators/Evaluator%20types/UI/How%20to%20define%20a%20decision%20model%20evaluator.md).

#### Pairwise

*Pairwise evaluators* compare outputs from two application versions using heuristics (e.g., which response is longer), LLMs (with pairwise prompts), or human reviewers.

Pairwise evaluation works well when directly scoring an output is difficult but comparing two outputs is straightforward. For example, in summarization tasks, choosing the more informative of two summaries is often easier than assigning an absolute score to a single summary.

Learn [how run pairwise evaluations](../Evaluators/Evaluator%20types/SDK/How%20to%20run%20a%20pairwise%20evaluation.md).

### Reference-free vs reference-based evaluators

Understanding whether an evaluator requires reference outputs is essential for determining when it can be used.

**Reference-free evaluators** assess quality without comparing to expected outputs. These work for both offline and online evaluation:

* **Safety checks**: Toxicity detection, PII detection, content policy violations
* **Format validation**: JSON structure, required fields, schema compliance
* **Quality heuristics**: Response length, latency, specific keywords
* **Reference-free LLM-as-judge**: Clarity, coherence, helpfulness, tone

**Reference-based evaluators** require reference outputs and only work for offline evaluation:

* **Correctness**: Semantic similarity to reference answer
* **Factual accuracy**: Fact-checking against ground truth
* **Exact match**: Classification tasks with known labels
* **Reference-based LLM-as-judge**: Comparing output quality to a reference

When designing an evaluation strategy, reference-free evaluators provide consistency across both offline testing and online monitoring, while reference-based evaluators enable more precise correctness checks during development.

## Evaluation types

LangSmith supports various evaluation approaches for different stages of development and deployment. Understanding when to use each type helps build a comprehensive evaluation strategy.

Offline and online evaluations serve different purposes:

* **Offline evaluation types** test pre-deployment on curated datasets with reference outputs
* **Online evaluation types** monitor production behavior on live traffic without reference outputs

Learn more about [evaluation types and when to use each](../Evaluators/Evaluation%20types.md).

## Best practices

### Building datasets

There are various strategies for building datasets:

**Manually curated examples**

This is the recommended starting point. Create 10–20 high-quality examples covering common scenarios and edge cases. These examples define what "good" looks like for your application.

**Historical traces**

Once in production, convert real traces into examples. For high-traffic applications:

* **User feedback**: Add runs that received negative feedback to test against.
* **Heuristics**: Identify interesting runs (e.g., long latency, errors).
* **LLM feedback**: Use LLMs to detect noteworthy conversations.

**Synthetic data**

Generate additional examples from existing ones. Works best when starting with several high-quality, hand-crafted examples as templates.

### Dataset organization

**Splits**

Splits are named subsets of a dataset used to segment examples into separate groups. Common patterns include:

* **ML-style splits**: divide examples into training, validation, and test sets to avoid overfitting, where a model performs well on training data but poorly on unseen data.
* **Category-based splits**: evaluate different input types separately when a dataset spans multiple task categories.
* **Staged rollout**: keep exploratory examples isolated until you're ready to include them in the main evaluation set.

Splits differ from metadata: use splits for high-level organizational grouping for evaluation, and metadata for per-example information such as tags and provenance.

In machine learning, best practice is for each example to belong to exactly one split. LangSmith allows examples to belong to multiple splits, which is useful when an example fits several evaluation categories.

Learn how to [create and manage dataset splits](../Datasets%20%26%20Experiments/Datasets/Create%20a%20dataset/Create%20and%20manage%20datasets%20in%20the%20UI.md#create-and-manage-dataset-splits).

**Versions**

LangSmith automatically creates dataset [versions](../Datasets%20%26%20Experiments/Datasets/Manage%20datasets.md#version-a-dataset) when examples change. [Tag versions](../Datasets%20%26%20Experiments/Datasets/Manage%20datasets.md#tag-a-version) to mark important milestones. Target specific versions in CI pipelines to ensure dataset updates don't break workflows.

### Human feedback collection

Human feedback often provides the most valuable assessment, particularly for subjective quality dimensions.

**Annotation queues**

[Annotation queues](../Annotation%20Queues/Use%20annotation%20queues.md) enable structured collection of human feedback. Flag specific runs for review, collect annotations in a streamlined interface, and transfer annotated runs to datasets for future evaluations.

Annotation queues complement [inline annotation](../Annotation%20Queues/Annotate%20traces%20and%20runs%20inline.md) by offering additional capabilities: grouping runs, specifying criteria, and configuring reviewer permissions.

### Evaluations vs testing

Testing and evaluation are similar but distinct concepts.

**Evaluation measures performance according to metrics.** Metrics can be fuzzy or subjective, and prove more useful in relative terms. They typically compare systems against each other.

**Testing asserts correctness.** A system can only be deployed if it passes all tests.

Evaluation metrics can be converted into tests. For example, regression tests can assert that new versions must outperform baseline versions on relevant metrics. Run tests and evaluations together for efficiency when systems are expensive to run.

Evaluations can be written using standard testing tools like [pytest](../Evaluators/Frameworks%20%26%20integrations/How%20to%20run%20evaluations%20with%20pytest.md) or [Vitest/Jest](../Evaluators/Frameworks%20%26%20integrations/How%20to%20run%20evaluations%20with%20Vitest-Jest.md).

## Quick reference: Offline vs online evaluation

The following table summarizes the key differences between offline and online evaluations:

| | **Offline Evaluation** | **Online Evaluation** |
| - | - | - |
| **Runs on** | Dataset (Examples) | Tracing Project (Runs/Threads) |
| **Data access** | Inputs, Outputs, Reference Outputs | Inputs, Outputs only |
| **When to use** | Pre-deployment, during development | Production, post-deployment |
| **Primary use cases** | Benchmarking, unit testing, regression testing, backtesting | Real-time monitoring, production feedback, anomaly detection |
| **Evaluation timing** | Batch processing on curated test sets | Real-time or near real-time on live traffic |
| **Setup location** | Evaluation tab (SDK, UI, Playground) | [Observability tab](../../Monitor/Observe/Online%20evaluators/Set%20up%20LLM-as-a-judge%20online%20evaluators.md) (automated rules) |
| **Data requirements** | Requires dataset curation | No dataset needed, evaluates live traces |
