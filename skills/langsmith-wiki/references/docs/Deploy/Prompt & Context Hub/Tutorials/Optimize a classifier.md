# Optimize a classifier

This tutorial shows you how to optimize a classifier based on user feedback. Classifiers are great to optimize because its generally pretty simple to collect the desired output, which makes it easy to create few shot examples based on user feedback. That is exactly what we will do in this example.

> [!NOTE]
>
> In an [agent-based workspace](../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](../../../Monitor/Trace/Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

## The objective

In this example, we will build a bot that classify GitHub issues based on their title. It will take in a title and classify it into one of many different classes. Then, we will start to collect user feedback and use that to shape how this classifier performs.

## Getting started

Register the classifier agent, then configure its identifier and environment:

```python
import os
os.environ["LANGSMITH_AGENT_ID"] = "<your-agent-id>"
os.environ["LANGSMITH_AGENT_ENVIRONMENT"] = "local"
```

We can then create our initial agent. This will be a really simple function that just takes in a GitHub issue title and tries to label it.

```python
import openai
from langsmith import traceable, Client
client = openai.Client()

available_topics = [
    "bug",
    "improvement",
    "new_feature",
    "documentation",
    "integration",
]

prompt_template = """Classify the type of the issue as one of {topics}.
Issue: {text}"""

@traceable(
    run_type="chain",
    name="Classifier",
)
def topic_classifier(
    topic: str):
    return client.chat.completions.create(
        model="gpt-5.4-mini",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt_template.format(
                    topics=','.join(available_topics),
                    text=topic,
                )
            }
        ],
    ).choices[0].message.content
```

We can then start to interact with it. When interacting with it, we will generate the LangSmith run id ahead of time and pass that into this function. We do this so we can attach feedback later on.

Here's how we can invoke the agent:

```python
from langsmith import uuid7

run_id = uuid7()
topic_classifier(
    "fix bug in LCEL",
    langsmith_extra={"run_id": run_id})
```

Here's how we can attach feedback after. We can collect feedback in two forms.

First, we can collect "positive" feedback - this is for examples that the model got right.

```python
import asyncio
from langsmith import agent_address

ls_client = Client()
run_id = uuid7()
topic_classifier(
    "fix bug in LCEL",
    langsmith_extra={"run_id": run_id})
# Resolve the session_id for the agent environment
address = agent_address(os.environ["LANGSMITH_AGENT_ID"], os.environ["LANGSMITH_AGENT_ENVIRONMENT"])
resolved = asyncio.run(ls_client.sessions.resolve(**address))
session_id = resolved.session_id
ls_client.create_feedback(
    run_id,
    key="user-score",
    score=1.0,
    session_id=session_id,
)
```

Next, we can focus on collecting feedback that corresponds to a "correction" to the generation. In this example the model will classify it as a bug, whereas I really want this to be classified as documentation.

```python
import asyncio
from langsmith import agent_address

ls_client = Client()
run_id = uuid7()
topic_classifier(
    "fix bug in documentation",
    langsmith_extra={"run_id": run_id})
address = agent_address(os.environ["LANGSMITH_AGENT_ID"], os.environ["LANGSMITH_AGENT_ENVIRONMENT"])
resolved = asyncio.run(ls_client.sessions.resolve(**address))
session_id = resolved.session_id
ls_client.create_feedback(
    run_id,
    key="correction",
    correction="documentation",
    session_id=session_id)
```

## Set up automations

We can now set up automations to move examples with feedback of some form into a dataset. We will set up two automations, one for positive feedback and the other for negative feedback.

The first will take all runs with positive feedback and automatically add them to a dataset. The logic behind this is that any run with positive feedback we can use as a good example in future iterations. Let's create a dataset called `classifier-github-issues` to add this data to.

![Optimization Negative](../../../../assets/images/9f9c8ac6f7db-class-optimization-neg.png)

The second will take all runs with a correction and use a webhook to add them to a dataset. When creating this webhook, we will select the option to "Use Corrections". This option will make it so that when creating a dataset from a run, rather than using the output of the run as the gold-truth output of the datapoint, it will use the correction.

![Optimization Positive](../../../../assets/images/fba23c9cdb39-class-optimization-pos.png)

## Update the agent

We can now update our code to pull down the dataset we are sending runs to. Once we pull it down, we can create a string with the examples in it. We can then put this string as part of the prompt!

```python
### NEW CODE ###
# Initialize the LangSmith Client so we can use to get the dataset
ls_client = Client()

# Create a function that will take in a list of examples and format them into a string
def create_example_string(examples):
    final_strings = []
    for e in examples:
        final_strings.append(f"Input: {e.inputs['topic']}\n> {e.outputs['output']}")
    return "\n\n".join(final_strings)
### NEW CODE ###

client = openai.Client()

available_topics = [
    "bug",
    "improvement",
    "new_feature",
    "documentation",
    "integration",
]

prompt_template = """Classify the type of the issue as one of {topics}.

Here are some examples:
{examples}

Begin!
Issue: {text}
>"""

@traceable(
    run_type="chain",
    name="Classifier",
)
def topic_classifier(
    topic: str):
    # We can now pull down the examples from the dataset
    # We do this inside the function so it always get the most up-to-date examples,
    # But this can be done outside and cached for speed if desired
    examples = list(ls_client.list_examples(dataset_name="classifier-github-issues"))  # <- New Code
    example_string = create_example_string(examples)
    return client.chat.completions.create(
        model="gpt-5.4-mini",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt_template.format(
                    topics=','.join(available_topics),
                    text=topic,
                    examples=example_string,
                )
            }
        ],
    ).choices[0].message.content
```

If now run the agent with a similar input as before, we can see that it correctly learns that anything related to docs (even if a bug) should be classified as `documentation`

```python
import asyncio
from langsmith import agent_address

ls_client = Client()
run_id = uuid7()
topic_classifier(
    "address bug in documentation",
    langsmith_extra={"run_id": run_id})
```

## Semantic search over examples

One additional thing we can do is only use the most semantically similar examples. This is useful when you start to build up a lot of examples.

In order to do this, we can first define an example to find the `k` most similar examples:

```python
import numpy as np

def find_similar(examples, topic, k=5):
    inputs = [e.inputs['topic'] for e in examples] + [topic]
    vectors = client.embeddings.create(input=inputs, model="text-embedding-3-small")
    vectors = [e.embedding for e in vectors.data]
    vectors = np.array(vectors)
    args = np.argsort(-vectors.dot(vectors[-1])[:-1])[:5]
    examples = [examples[i] for i in args]
    return examples
```

We can then use that in the agent

```python
import asyncio
from langsmith import agent_address

ls_client = Client()

def create_example_string(examples):
    final_strings = []
    for e in examples:
        final_strings.append(f"Input: {e.inputs['topic']}\n> {e.outputs['output']}")
    return "\n\n".join(final_strings)

client = openai.Client()

available_topics = [
    "bug",
    "improvement",
    "new_feature",
    "documentation",
    "integration",
]

prompt_template = """Classify the type of the issue as one of {topics}.

Here are some examples:
{examples}

Begin!
Issue: {text}
>"""

@traceable(
    run_type="chain",
    name="Classifier",
)
def topic_classifier(
    topic: str):
    examples = list(ls_client.list_examples(dataset_name="classifier-github-issues"))
    examples = find_similar(examples, topic)
    example_string = create_example_string(examples)
    return client.chat.completions.create(
        model="gpt-5.4-mini",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt_template.format(
                    topics=','.join(available_topics),
                    text=topic,
                    examples=example_string,
                )
            }
        ],
    ).choices[0].message.content
```
