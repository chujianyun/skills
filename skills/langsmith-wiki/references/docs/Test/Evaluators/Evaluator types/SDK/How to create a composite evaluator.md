# How to create a composite evaluator

*Composite evaluators* are a way to combine multiple evaluator scores into a single [score](../../../Get%20started/Evaluation%20concepts.md#evaluator-outputs). This is useful when you want to evaluate multiple aspects of your application and combine the results into a single result.

This guide describes setting up an evaluation that uses multiple evaluators and combines their scores with a custom aggregation function using the [LangSmith SDK](../../../../Monitor/Reference/langsmith%20%28smith-python-sdk%29.md).

> [!NOTE]
>
> Requires langsmith>=0.4.29

> [!TIP]
>
> To create composite evaluators in the LangSmith UI, refer to [How to create a composite evaluator (UI)](../UI/How%20to%20create%20a%20composite%20evaluator.md).

## 1. Configure evaluators on a dataset

Start by configuring your evaluators. In this example, the application generates a tweet from a blog introduction and uses three evaluators—summary, tone, and formatting—to assess the output.

If you already have your own dataset with evaluators configured, you can skip this step.

```python
import os
from dotenv import load_dotenv
from openai import OpenAI
from langsmith import Client
from pydantic import BaseModel
import json

# Load environment variables from .env file
load_dotenv()

# Access environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
langsmith_api_key = os.getenv('LANGSMITH_API_KEY')
langsmith_project = os.getenv('LANGSMITH_PROJECT', 'default')


# Create a dataset. Only need to do this once.
client = Client()
oai_client = OpenAI()

examples = [
  {
    "inputs": {"blog_intro": "Today we're excited to announce the general availability of LangSmith—our purpose-built infrastructure and management layer for deploying and scaling long-running, stateful agents. Since our beta last June, nearly 400 companies have used LangSmith to deploy their agents into production. Agent deployment is the next hard hurdle for shipping reliable agents, and LangSmith dramatically lowers this barrier with: 1-click deployment to go live in minutes, 30 API endpoints for designing custom user experiences that fit any interaction pattern, Horizontal scaling to handle bursty, long-running traffic, A persistence layer to support memory, conversational history, and async collaboration with human-in-the-loop or multi-agent workflows, Native Studio, the agent IDE, for easy debugging, visibility, and iteration "},
  },
  {
    "inputs": {"blog_intro": "Klarna has reshaped global commerce with its consumer-centric, AI-powered payment and shopping solutions. With over 85 million active users and 2.5 million daily transactions on its platform, Klarna is a fintech leader that simplifies shopping while empowering consumers with smarter, more flexible financial solutions. Klarna's flagship AI Assistant is revolutionizing the shopping and payments experience. Built on LangGraph and powered by LangSmith, the AI Assistant handles tasks ranging from customer payments, to refunds, to other payment escalations. With 2.5 million conversations to date, the AI Assistant is more than just a chatbot; it's a transformative agent that performs the work equivalent of 700 full-time staff, delivering results quickly and improving company efficiency."},
  },
]

dataset = client.create_dataset(dataset_name="Blog Intros")

client.create_examples(
  dataset_id=dataset.id,
  examples=examples,
)

# Define a target function. In this case, we're using a simple function that generates a tweet from a blog intro.
def generate_tweet(inputs: dict) -> dict:
    instructions = (
      "Given the blog introduction, please generate a catchy yet professional tweet that can be used to promote the blog post on social media. Summarize the key point of the blog post in the tweet. Use emojis in a tasteful manner."
    )
    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": inputs["blog_intro"]},
    ]
    result = oai_client.responses.create(
        input=messages, model="gpt-5.4-mini"
    )
    return {"tweet": result.output_text}

# Define evaluators. In this case, we're using three evaluators: summary, formatting, and tone.
def summary(inputs: dict, outputs: dict) -> bool:
    """Judge whether the tweet is a good summary of the blog intro."""
    instructions = "Given the following text and summary, determine if the summary is a good summary of the text."

    class Response(BaseModel):
        summary: bool

    msg = f"Question: {inputs['blog_intro']}\nAnswer: {outputs['tweet']}"
    response = oai_client.responses.parse(
        model="gpt-5.4-mini",
        input=[{"role": "system", "content": instructions,}, {"role": "user", "content": msg}],
        text_format=Response
    )

    parsed_response = json.loads(response.output_text)
    return parsed_response["summary"]

def formatting(inputs: dict, outputs: dict) -> bool:
    """Judge whether the tweet is formatted for easy human readability."""
    instructions = "Given the following text, determine if it is formatted well so that a human can easily read it. Pay particular attention to spacing and punctuation."

    class Response(BaseModel):
        formatting: bool

    msg = f"{outputs['tweet']}"
    response = oai_client.responses.parse(
        model="gpt-5.4-mini",
        input=[{"role": "system", "content": instructions,}, {"role": "user", "content": msg}],
        text_format=Response
    )

    parsed_response = json.loads(response.output_text)
    return parsed_response["formatting"]

def tone(inputs: dict, outputs: dict) -> bool:
    """Judge whether the tweet's tone is informative, friendly, and engaging."""
    instructions = "Given the following text, determine if the tweet is informative, yet friendly and engaging."

    class Response(BaseModel):
        tone: bool

    msg = f"{outputs['tweet']}"
    response = oai_client.responses.parse(
        model="gpt-5.4-mini",
        input=[{"role": "system", "content": instructions,}, {"role": "user", "content": msg}],
        text_format=Response
    )
    parsed_response = json.loads(response.output_text)
    return parsed_response["tone"]

# Calling evaluate() with the dataset, target function, and evaluators.
results = client.evaluate(
    generate_tweet,
    data=dataset.name,
    evaluators=[summary, tone, formatting],
    experiment_prefix="gpt-5.4-mini",
)

# Get the experiment name to be used in the next section
experiment_name = results.experiment_name
```

## 2. Create composite feedback

Create composite feedback that aggregates the individual evaluator scores using your custom function. This example uses a weighted average of the individual evaluator scores.

```python
import asyncio
import math
from typing import Dict

from langsmith import Client
from dotenv import load_dotenv

load_dotenv()

# TODO: Replace with your experiment name. Can be found in UI or from the above client.evaluate() result
YOUR_EXPERIMENT_NAME = "placeholder_experiment_name"

# Set weights for the individual evaluator scores
DEFAULT_WEIGHTS: Dict[str, float] = {
    "summary": 0.7,
    "tone": 0.2,
    "formatting": 0.1,
}
WEIGHTED_FEEDBACK_NAME = "weighted_summary"


# Calculate weighted score for each run
def calculate_weighted_score(feedback_stats: dict) -> float:
    if not feedback_stats:
        return float("nan")

    # Check if all required metrics are present and have data
    required_metrics = set(DEFAULT_WEIGHTS.keys())
    available_metrics = set(feedback_stats.keys())

    if not required_metrics.issubset(available_metrics):
        return float("nan")

    # Calculate weighted score
    total_score = 0.0
    for metric, weight in DEFAULT_WEIGHTS.items():
        metric_data = feedback_stats[metric]
        if (metric_data.n or 0) > 0 and metric_data.avg is not None:
            total_score += metric_data.avg * weight
        else:
            return float("nan")

    return total_score


async def main():
    client = Client()
    # The experiment is a tracing project; its root runs carry the evaluator scores
    experiment = client.read_project(project_name=YOUR_EXPERIMENT_NAME)

    # Process each run and write feedback
    # Note that experiment results need to finish processing before this should be called.
    async for run in client.runs.query(
        project_ids=[str(experiment.id)],
        min_start_time=experiment.start_time,
        is_root=True,
        selects=["ID", "FEEDBACK_STATS"],
    ):
        if run.feedback_stats:
            score = calculate_weighted_score(run.feedback_stats)
            if not math.isnan(score):
                client.create_feedback(
                    run_id=run.id,
                    key=WEIGHTED_FEEDBACK_NAME,
                    score=float(score),
                    session_id=experiment.id,
                )


asyncio.run(main())
```
