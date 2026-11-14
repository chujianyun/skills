# Trace with API

> Learn how to trace LLM applications using the LangSmith REST API directly.

This guide covers two approaches to tracing with the [REST API](../../../Reference/LangSmith%20REST%20API/LangSmith%20API%20reference.md): basic tracing using the `POST /runs` and `PATCH /runs` endpoints, and batch ingestion using `POST /runs/multipart` for higher throughput.

For a full list of endpoints and request/response schemas, refer to the [API reference](../../../Reference/LangSmith%20REST%20API/LangSmith%20API%20reference.md).

> [!WARNING]
>
> We strongly recommend using the [Python](../../../Reference/langsmith%20%28smith-python-sdk%29.md) or [TypeScript](../../../Reference/langsmith%20%28smith-js-ts-sdk%29.md) SDK to send traces to LangSmith instead of the REST API directly. The SDKs include batching and background sending optimizations that prevent tracing from affecting your application's performance.
>
> If you cannot use an SDK, note that sending traces synchronously may impact application performance.

> [!NOTE]
>
> We recommend using **UUID v7** for run IDs. UUIDv7 embeds a timestamp, which preserves correct time-ordering of runs in a trace. Use `uuid7()` from the LangSmith SDK to generate them, or see [Specify a custom run ID](Custom%20instrumentation.md#specify-a-custom-run-id) for more details.

## Basic tracing

The simplest way to log runs is via the `POST /runs` and `PATCH /runs` endpoints. This approach requires minimal information to establish the trace hierarchy.

> [!NOTE]
>
> When using the LangSmith REST API, provide your [API key](../../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md) in the request headers as `"x-api-key"`.
>
> If your API key is linked to multiple workspaces, specify the workspace in the header with `"x-tenant-id"`.
>
> In this approach, you do not need to set the `dotted_order` or `trace_id` fields—the system generates them automatically. Though simpler, it is slower and subject to lower rate limits than batch ingestion.

The following example traces a chat completion with a parent chain run and a child LLM run. Set [`parent_run_id`](../../../Debug/Data%20type%20reference/Run%20%28span%29%20data%20format.md) on a child run to attach it to its parent:

```python expandable wrap
import openai
import os
import requests
from datetime import datetime, timezone
from langsmith import uuid7

# Send your API Key in the request headers
headers = {
    "x-api-key": os.environ["LANGSMITH_API_KEY"],
    "x-tenant-id": os.environ["LANGSMITH_WORKSPACE_ID"]
}

def post_run(run_id, name, run_type, inputs, parent_id=None):
    """Function to post a new run to the API."""
    data = {
        "id": run_id.hex,
        "name": name,
        "run_type": run_type,
        "inputs": inputs,
        "start_time": datetime.utcnow().isoformat(),
        # "session_name": "project-name",  # the name of the project to trace to
        # "session_id": "project-id",  # the ID of the project to trace to. specify one of session_name or session_id
    }
    if parent_id:
        data["parent_run_id"] = parent_id.hex

    requests.post(
        "https://api.smith.langchain.com/runs",  # Update for self-hosted, GCP EU (`eu.api...`), GCP APAC (`apac.api...`), or AWS US (`aws.api...`)
        json=data,
        headers=headers
    )

def patch_run(run_id, outputs):
    """Function to patch a run with outputs."""
    requests.patch(
        f"https://api.smith.langchain.com/runs/{run_id}",
        json={
            "outputs": outputs,
            "end_time": datetime.now(timezone.utc).isoformat(),
        },
        headers=headers,
    )

# This can be a user input to your app
question = "Can you summarize this morning's meetings?"

# This can be retrieved in a retrieval step
context = "During this morning's meeting, we solved all world conflict."

messages = [
    {"role": "system", "content": "You are a helpful assistant. Please respond to the user's request only based on the given context."},
    {"role": "user", "content": f"Question: {question}\nContext: {context}"}
]

# Create parent run
parent_run_id = uuid7()
post_run(parent_run_id, "Chat Pipeline", "chain", {"question": question})

# Create child run
child_run_id = uuid7()
post_run(child_run_id, "OpenAI Call", "llm", {"messages": messages}, parent_run_id)

# Generate a completion
client = openai.Client()
chat_completion = client.chat.completions.create(
    model="gpt-6-luna",
    messages=messages
)

# End runs
patch_run(child_run_id, chat_completion.dict())
patch_run(parent_run_id, {"answer": chat_completion.choices[0].message.content})
```

For more information, refer to [Run (span) data format](../../../Debug/Data%20type%20reference/Run%20%28span%29%20data%20format.md).

## Batch ingestion

For faster ingestion and higher rate limits, use the [`POST /runs/multipart`](../../../Reference/LangSmith%20REST%20API/Tracing/Ingest%20runs%20%28multipart%29.md) endpoint. This requires the [`requests-toolbelt`](https://pypi.org/project/requests-toolbelt/) and [`uuid-utils`](https://pypi.org/project/uuid-utils/) packages.

Unlike basic tracing, this endpoint requires you to compute and set [`dotted_order`](../../../Debug/Data%20type%20reference/Run%20%28span%29%20data%20format.md#what-is-dotted_order) and [`trace_id`](../../../Debug/Data%20type%20reference/Run%20%28span%29%20data%20format.md) yourself. `dotted_order` encodes each run's timestamp and UUID with parent and child entries joined by dots (e.g., `20240101T000000Z<parent-uuid>.20240101T000001Z<child-uuid>`), telling LangSmith how runs relate and in what order they occurred. `trace_id` is the UUID of the root run.

The following example creates a parent run and a child run, sends them in a single batch request, then patches both with their outputs:

```python expandable
import json
import os
import uuid
from datetime import datetime, timezone
from typing import Dict, List
import requests
from requests_toolbelt import MultipartEncoder
from uuid_utils.compat import uuid7

def create_dotted_order(
    start_time: datetime | None = None,
    run_id: uuid.UUID | None = None
) -> str:
    """Create a dotted order string for run ordering and hierarchy.

    The dotted order is used to establish the sequence and relationships between runs.
    It combines a timestamp with a unique identifier to ensure proper ordering and tracing.
    """
    st = start_time or datetime.now(timezone.utc)
    id_ = run_id or uuid7()
    return f"{st.strftime('%Y%m%dT%H%M%S%fZ')}{id_}"

def create_run_base(
    name: str,
    run_type: str,
    inputs: dict,
    start_time: datetime
) -> dict:
    """Create the base structure for a run."""
    run_id = uuid7()
    return {
        "id": str(run_id),
        "trace_id": str(run_id),
        "name": name,
        "start_time": start_time.isoformat(),
        "inputs": inputs,
        "run_type": run_type,
    }

def construct_run(
    name: str,
    run_type: str,
    inputs: dict,
    parent_dotted_order: str | None = None,
) -> dict:
    """Construct a run dictionary with the given parameters.

    This function creates a run with a unique ID and dotted order, establishing its place
    in the trace hierarchy if it's a child run.
    """
    start_time = datetime.now(timezone.utc)
    run = create_run_base(name, run_type, inputs, start_time)
    current_dotted_order = create_dotted_order(start_time, uuid.UUID(run["id"]))

    if parent_dotted_order:
        current_dotted_order = f"{parent_dotted_order}.{current_dotted_order}"
        run["trace_id"] = parent_dotted_order.split(".")[0].split("Z")[1]
        run["parent_run_id"] = parent_dotted_order.split(".")[-1].split("Z")[1]

    run["dotted_order"] = current_dotted_order
    return run

def serialize_run(operation: str, run_data: dict) -> List[tuple]:
    """Serialize a run for the multipart request.

    This function separates the run data into parts for efficient transmission and storage.
    The main run data and optional fields (inputs, outputs, events) are serialized separately.
    """
    run_id = run_data.get("id", str(uuid7()))

    # Separate optional fields
    inputs = run_data.pop("inputs", None)
    outputs = run_data.pop("outputs", None)
    events = run_data.pop("events", None)

    parts = []

    # Serialize main run data
    run_data_json = json.dumps(run_data).encode("utf-8")
    parts.append(
        (
            f"{operation}.{run_id}",
            (
                None,
                run_data_json,
                "application/json",
                {"Content-Length": str(len(run_data_json))},
            ),
        )
    )

    # Serialize optional fields
    for key, value in [("inputs", inputs), ("outputs", outputs), ("events", events)]:
        if value:
            serialized_value = json.dumps(value).encode("utf-8")
            parts.append(
                (
                    f"{operation}.{run_id}.{key}",
                    (
                        None,
                        serialized_value,
                        "application/json",
                        {"Content-Length": str(len(serialized_value))},
                    ),
                )
            )

    return parts

def batch_ingest_runs(
    api_url: str,
    api_key: str,
    posts: list[dict] | None = None,
    patches: list[dict] | None = None,
) -> None:
    """Ingest multiple runs in a single batch request.

    This function handles both creating new runs (posts) and updating existing runs (patches).
    It's more efficient for ingesting multiple runs compared to individual API calls.
    """
    boundary = uuid.uuid4().hex
    all_parts = []

    for operation, runs in zip(("post", "patch"), (posts, patches)):
        if runs:
            all_parts.extend(
                [part for run in runs for part in serialize_run(operation, run)]
            )

    encoder = MultipartEncoder(fields=all_parts, boundary=boundary)
    headers = {"Content-Type": encoder.content_type, "x-api-key": api_key}

    try:
        response = requests.post(
            f"{api_url}/runs/multipart",
            data=encoder,
            headers=headers
        )
        response.raise_for_status()
        print("Successfully ingested runs.")
    except requests.RequestException as e:
        print(f"Error ingesting runs: {e}")
        # In a production environment, you might want to log this error or handle it more robustly

# Configure API URL and key
# For production use, consider using a configuration file or environment variables
api_url = "https://api.smith.langchain.com"  # GCP EU: eu.api...; GCP APAC: apac.api...; AWS US: aws.api... for regional SaaS
api_key = os.environ.get("LANGSMITH_API_KEY")

if not api_key:
    raise ValueError("LANGSMITH_API_KEY environment variable is not set")

# Create a parent run
parent_run = construct_run(
    name="Parent Run",
    run_type="chain",
    inputs={"main_question": "Tell me about France"},
)

# Create a child run, linked to the parent
child_run = construct_run(
    name="Child Run",
    run_type="llm",
    inputs={"question": "What is the capital of France?"},
    parent_dotted_order=parent_run["dotted_order"],
)

# First, post the runs to create them
posts = [parent_run, child_run]
batch_ingest_runs(api_url, api_key, posts=posts)

# Then, update the runs with their end times and any outputs
child_run_update = {
    **child_run,
    "end_time": datetime.now(timezone.utc).isoformat(),
    "outputs": {"answer": "Paris is the capital of France."},
}

parent_run_update = {
    **parent_run,
    "end_time": datetime.now(timezone.utc).isoformat(),
    "outputs": {"summary": "Discussion about France, including its capital."},
}

patches = [parent_run_update, child_run_update]
batch_ingest_runs(api_url, api_key, patches=patches)

# Note: This example requires the `requests` and `requests_toolbelt` libraries.
# You can install them using pip:
# pip install requests requests_toolbelt
```

## Related

* [Run (span) data format](../../../Debug/Data%20type%20reference/Run%20%28span%29%20data%20format.md)
* [Specify a custom run ID](Custom%20instrumentation.md#specify-a-custom-run-id)
* [Custom instrumentation](Custom%20instrumentation.md)
