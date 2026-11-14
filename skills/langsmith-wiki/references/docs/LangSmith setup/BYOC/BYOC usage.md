# BYOC usage

> Route tracing and API traffic to a LangSmith BYOC data plane, including tracing to multiple endpoints and the path prefixes for each service.

Once your data plane is active, all API traffic for its workspaces goes to the data plane endpoint rather than to the LangSmith Cloud backend. This page explains how to route requests to the right service.

The LangSmith UI handles this automatically: it routes to the correct data plane based on the workspace you have selected. The guidance below applies to your own client code and direct API calls.

## Organizations, data planes, and workspaces

A BYOC deployment adds one level to the standard LangSmith [resource hierarchy](../Govern/Organization/Overview.md#resource-hierarchy): the data plane, which sits between the organization and the workspace.

* **Organization**: The top level. Users, roles, billing, SSO configuration, and API keys belong to the organization and live in the control plane.
* **Data plane**: Belongs to an organization and represents physical separation of data. An organization can have several data planes, each in its own AWS account and region.
* **Workspace**: Belongs to exactly one data plane, which you select when you create the workspace. Traces, datasets, experiments, and other agent data live in a workspace.

![Nesting diagram of a BYOC deployment. An organization contains two data planes, each labeled as physical separation. The first is in us-east-1 and the second is in eu-west-1. Each data plane holds one workspace per team, and every workspace is labeled as logical separation within its data plane.](../../../assets/images/6b2ceb6692dd-byoc-org-structure.png)

Use data planes for physical separation of data, and workspaces for logical separation within a data plane. Common ways to divide data planes are:

* **Per region**, such as `us-east-1` and `us-west-2`, to keep sensitive agent data in a specific region.
* **Per environment and region**, such as prod `us-east-1` and dev `us-east-1`, to hold production and development data in separate AWS accounts.
* **Per business unit**, when each unit owns its own AWS account.

Below the data plane, workspace isolation works the same as on Cloud or self-hosted. For more information, see [Administration overview](../Govern/Organization/Overview.md) and [Workload isolation](../Govern/Organization/Workspace%20setup/Workload%20isolation.md).

## Find your data plane endpoint

Each data plane has a base URL. Navigate to **Settings > Data Planes** to see each of your data planes, its state, and its API URL.

> [!WARNING]
>
> Data planes are provisioned with a private endpoint by default, so you need private connectivity to reach the base URL, such as Tailscale, AWS PrivateLink, or VPC peering.

## Trace to a data plane

For tracing in an agent-based workspace, [create an agent and configure agent addressing](../Overview/Agent-based%20workspaces/Create%20an%20agent.md#configure-tracing-for-the-agent) before running the examples.

To send traces to a workspace that lives in your data plane, point the LangSmith SDK at the data plane endpoint and authenticate with an API key scoped to a workspace in that data plane:

```bash
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY="<API_KEY>"
export LANGSMITH_ENDPOINT="https://<data_plane_host>"
```

> [!WARNING]
>
> Create `LANGSMITH_API_KEY` from a workspace inside the target data plane. Traces are tenant-scoped, so an API key from a workspace on a different data plane, including a Cloud workspace, is rejected.

For a complete, runnable example, follow the [Observability quickstart](../../Monitor/Trace/Tracing%20quickstart.md) and substitute the environment variables above.

## Route API requests

The base URL routes to different services depending on the path prefix:

| Service | Path prefix | Example |
| - | - | - |
| LangSmith | None | `https://<data_plane_host>/v1/sessions` |
| OTLP ingestion | `/otel` | `https://<data_plane_host>/otel/v1/traces` |
| LangSmith Agent Server | `/api-host` | `https://<data_plane_host>/api-host/v2/deployments` |
| LLM Gateway | `/gateway` | `https://<data_plane_host>/gateway/v1/chat/completions` |

The LangSmith API also accepts an `/api` prefix, so `https://<data_plane_host>/api/v1/sessions` reaches the same endpoint. The SDK uses the bare data plane host, as shown in [Trace to a data plane](#trace-to-a-data-plane).

## Trace to multiple endpoints

Use these patterns to trace to both Cloud and a data plane, or to multiple data planes.

### Dual write to two endpoints

Set `LANGSMITH_RUNS_ENDPOINTS` to write to multiple endpoints. These replica settings use each agent environment's [`tracer_session_name`](../Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as `project_name`:

```bash
export LANGSMITH_RUNS_ENDPOINTS='[
  {"api_url": "https://aws.api.smith.langchain.com", "api_key": "ls__key1", "project_name": "<cloud-environment-tracer-session-name>"},
  {"api_url": "https://<data_plane_host>", "api_key": "ls__key2", "project_name": "<byoc-environment-tracer-session-name>"}
]'
```

### Choose the destination in agent logic

To decide where to trace at runtime, create a client per endpoint and select between them. Set `LANGSMITH_CLOUD_PROJECT` and `LANGSMITH_BYOC_PROJECT` to the corresponding agent environments' `tracer_session_name` values:

```python
import os

from langsmith import Client, traceable, tracing_context

CLOUD_ENDPOINT = "https://aws.api.smith.langchain.com"
BYOC_ENDPOINT = "https://<data_plane_host>"


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


cloud_client = Client(
    api_key=require_env("LANGSMITH_CLOUD_API_KEY"),
    api_url=CLOUD_ENDPOINT,
    workspace_id=os.getenv("LANGSMITH_CLOUD_WORKSPACE_ID"),
)

byoc_client = Client(
    api_key=require_env("LANGSMITH_BYOC_API_KEY"),
    api_url=BYOC_ENDPOINT,
    workspace_id=os.getenv("LANGSMITH_BYOC_WORKSPACE_ID"),
)


def get_workspace_routing(tenant_id: str):
    """Select the tracing destination for this tenant."""
    if tenant_id.startswith("byoc_"):
        return byoc_client, require_env("LANGSMITH_BYOC_PROJECT")
    return cloud_client, require_env("LANGSMITH_CLOUD_PROJECT")


@traceable
def run_agent_workflow(query: str):
    return f"Processed: {query}"


def handle_request(tenant_id: str, query: str):
    client, project_name = get_workspace_routing(tenant_id)

    with tracing_context(enabled=True, client=client, project_name=project_name):
        return run_agent_workflow(query)
```

## See also

* [BYOC onboarding](AWS/BYOC%20onboarding.md)
* [BYOC architecture](AWS/BYOC%20architecture.md)
