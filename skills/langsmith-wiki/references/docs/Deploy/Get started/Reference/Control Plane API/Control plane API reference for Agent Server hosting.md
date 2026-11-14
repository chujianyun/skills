# Control plane API reference for Agent Server hosting

> Use the LangSmith control plane API to programmatically create, manage, and automate Agent Server deployments.

The control plane API manages [Agent Server hosting](../../LangSmith%20Agent%20Server.md). With the control plane API, you can programmatically create, manage, and automate your [Agent Server](../../../Agent%20Server/Capabilities/Agent%20Server.md) deployments—for example, as part of a custom CI/CD workflow.

Browse the full API reference in the **Control Plane API** section in the sidebar, or refer to the endpoint groups:

* [Integrations (v1)](https://docs.langchain.com/api-reference/integrations-v1/list-github-integrations.md): GitHub integrations and repository listings
* [Deployments (v2)](https://docs.langchain.com/api-reference/deployments-v2): Create, manage, and update Agent Server deployments
* [Listeners (v2)](https://docs.langchain.com/api-reference/listeners-v2): Listener resources for self-hosted enterprise organizations
* [Auth Service (v2)](https://docs.langchain.com/api-reference/auth-service-v2): OAuth provider configuration and authentication flows

## Host

The control plane hosts for Cloud data regions:

<table>
  <thead>
    <tr>
      <th>Region</th>

      <th>
        URL
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>GCP US</td>

      <td>
        `https://api.host.langchain.com`
      </td>
    </tr>

    <tr>
      <td>GCP EU</td>

      <td>
        `https://eu.api.host.langchain.com`
      </td>
    </tr>

    <tr>
      <td>GCP APAC</td>

      <td>
        `https://apac.api.host.langchain.com`
      </td>
    </tr>

    <tr>
      <td>AWS US</td>

      <td>
        `https://aws.api.host.langchain.com`
      </td>
    </tr>

    <tr><td>Azure US</td>
    <td>`https://azure.api.host.langchain.com`</td></tr>
  </tbody>
</table>

**Note**: Self-hosted deployments of LangSmith will have a custom host for the control plane. The control plane APIs can be accessed at the path `/api-host`. For example, `http(s)://<host>/api-host/v2/deployments`. See [the self-host usage guide](../../../../LangSmith%20setup/Self-hosted/Install%20an%20instance/Interact%20with%20your%20self-hosted%20instance%20of%20LangSmith.md#configuring-the-application-you-want-to-use-with-langsmith) for more details.

## Authentication

To authenticate with the control plane API, set the `X-Api-Key` header to a valid LangSmith API key and set the `X-Tenant-Id` header to a valid workspace ID to target.

Example `curl` command:

```shell
curl --request GET \
  --url http://localhost:8124/v2/deployments \
  --header 'X-Api-Key: LANGSMITH_API_KEY'
  --header 'X-Tenant-Id': WORKSPACE_ID'
```

## Versioning

Each endpoint path is prefixed with a version (e.g. `v1`, `v2`).

## Quick start

1. Call `POST /v2/deployments` to create a deployment. The response body contains the deployment ID (`id`) and the ID of the latest (and first) revision (`latest_revision_id`).
2. Call `GET /v2/deployments/{deployment_id}` to retrieve the deployment. Set `deployment_id` in the URL to the deployment ID (`id`) from step 1.
3. Poll for revision `status` until `status` is `DEPLOYED` by calling `GET /v2/deployments/{deployment_id}/revisions/{latest_revision_id}`.
4. Call `PATCH /v2/deployments/{deployment_id}` to update the deployment.

## Resource spec

The `resource_spec` object sets CPU, memory, and replica counts for a deployment's API servers, queue workers, Redis, and PostgreSQL. The field descriptions in the [Deployments (v2)](https://docs.langchain.com/api-reference/deployments-v2) reference list each field. The following behaviors apply across fields:

* **`PATCH` replaces the whole object**: A `PATCH` that includes `resource_spec` replaces the stored `resource_spec` and does not merge with it. Fields you leave out fall back to the defaults for the deployment type, not to their previous values. Send the full `resource_spec` on every `PATCH`.
* **Limits default to 2x the request**: If you set a CPU or memory request and omit its limit, the limit defaults to 2x the request. The Redis memory limit is the exception: `redis_memory_limit_mb` defaults to `redis_memory_mb`. On self-hosted data planes, the CPU limit also sets the [autoscaling target](../../Deployment%20components/LangSmith%20data%20plane.md#autoscaling).
* **CPU values are rounded to 1 decimal place**: Rounding uses floating-point arithmetic, so some values round down. For example, `0.25` is stored as `0.2`.
* **Redis memory has its own range**: `redis_memory_mb` and `redis_memory_limit_mb` accept 512 to 16384, in multiples of 128. The API enforces this range in a validator, so it does not appear in the OpenAPI schema.

For self-hosted deployments, the listener in the data plane validates the `resource_spec` again with the rules of its own version. A `PATCH` that returns `200` can still fail at deploy time on an older listener. See [Listener version requirements](../../../Deploy%20to%20Self-hosted/Configure/Self-hosted%20platform%20features.md#listener-version-requirements).

To mount persistent storage, such as Amazon EFS, into a self-hosted deployment's pods, set `volumes` and `volume_mounts` in `resource_spec`. For more information, see [Volumes](../../../Deploy%20to%20Self-hosted/Configure/Self-hosted%20platform%20features.md#volumes).

## Example Code

Below is example Python code that demonstrates how to orchestrate the control plane APIs to create a deployment, update the deployment, and delete the deployment.

```python
import os
import time

import requests
from dotenv import load_dotenv


load_dotenv()

# required environment variables
CONTROL_PLANE_HOST = os.getenv("CONTROL_PLANE_HOST")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
WORKSPACE_ID = os.getenv("WORKSPACE_ID")
INTEGRATION_ID = os.getenv("INTEGRATION_ID")
MAX_WAIT_TIME = 1800  # 30 mins


def get_headers() -> dict:
    """Return common headers for requests to the control plane API."""
    return {
        "X-Api-Key": LANGSMITH_API_KEY,
        "X-Tenant-Id": WORKSPACE_ID,
    }


def create_deployment() -> str:
    """Create deployment. Return deployment ID."""
    headers = get_headers()
    headers["Content-Type"] = "application/json"

    deployment_name = "my_deployment"

    request_body = {
        "name": deployment_name,
        "source": "github",
        "source_config": {
            "integration_id": INTEGRATION_ID,
            "repo_url": "https://github.com/langchain-ai/langgraph-example",
            "deployment_type": "serverless",
            "build_on_push": False,
            "custom_url": None,
            "resource_spec": None,
        },
        "source_revision_config": {
            "repo_ref": "main",
            "langgraph_config_path": "langgraph.json",
            "image_uri": None,
        },
        "secrets": [
            {
                "name": "OPENAI_API_KEY",
                "value": "test_openai_api_key",
            },
            {
                "name": "ANTHROPIC_API_KEY",
                "value": "test_anthropic_api_key",
            },
            {
                "name": "TAVILY_API_KEY",
                "value": "test_tavily_api_key",
            },
        ],
    }

    response = requests.post(
        url=f"{CONTROL_PLANE_HOST}/v2/deployments",
        headers=headers,
        json=request_body,
    )

    if response.status_code != 201:
        raise Exception(f"Failed to create deployment: {response.text}")

    deployment_id = response.json()["id"]
    print(f"Created deployment {deployment_name} ({deployment_id})")
    return deployment_id


def get_deployment(deployment_id: str) -> dict:
    """Get deployment."""
    response = requests.get(
        url=f"{CONTROL_PLANE_HOST}/v2/deployments/{deployment_id}",
        headers=get_headers(),
    )

    if response.status_code != 200:
        raise Exception(f"Failed to get deployment ID {deployment_id}: {response.text}")

    return response.json()


def list_revisions(deployment_id: str) -> list[dict]:
    """List revisions.

    Return list is sorted by created_at in descending order (latest first).
    """
    response = requests.get(
        url=f"{CONTROL_PLANE_HOST}/v2/deployments/{deployment_id}/revisions",
        headers=get_headers(),
    )

    if response.status_code != 200:
        raise Exception(
            f"Failed to list revisions for deployment ID {deployment_id}: {response.text}"
        )

    return response.json()


def get_revision(
    deployment_id: str,
    revision_id: str,
) -> dict:
    """Get revision."""
    response = requests.get(
        url=f"{CONTROL_PLANE_HOST}/v2/deployments/{deployment_id}/revisions/{revision_id}",
        headers=get_headers(),
    )

    if response.status_code != 200:
        raise Exception(f"Failed to get revision ID {revision_id}: {response.text}")

    return response.json()


def patch_deployment(deployment_id: str) -> None:
    """Patch deployment."""
    headers = get_headers()
    headers["Content-Type"] = "application/json"

    # This creates a new revision because source_revision_config is included
    response = requests.patch(
        url=f"{CONTROL_PLANE_HOST}/v2/deployments/{deployment_id}",
        headers=headers,
        json={
            "source_config": {
                "build_on_push": True,
            },
            "source_revision_config": {
                "repo_ref": "main",
                "langgraph_config_path": "langgraph.json",
            },
        },
    )

    if response.status_code != 200:
        raise Exception(f"Failed to patch deployment: {response.text}")

    print(f"Patched deployment ID {deployment_id}")


def wait_for_deployment(deployment_id: str, revision_id: str) -> None:
    """Wait for revision status to be DEPLOYED."""
    start_time = time.time()
    revision, status = None, None
    while time.time() - start_time < MAX_WAIT_TIME:
        revision = get_revision(deployment_id, revision_id)
        status = revision["status"]
        if status == "DEPLOYED":
            break
        elif "FAILED" in status:
            raise Exception(f"Revision ID {revision_id} failed: {revision}")

        print(f"Waiting for revision ID {revision_id} to be DEPLOYED...")
        time.sleep(60)

    if status != "DEPLOYED":
        raise Exception(
            f"Timeout waiting for revision ID {revision_id} to be DEPLOYED: {revision}"
        )


def delete_deployment(deployment_id: str) -> None:
    """Delete deployment."""
    response = requests.delete(
        url=f"{CONTROL_PLANE_HOST}/v2/deployments/{deployment_id}",
        headers=get_headers(),
    )

    if response.status_code != 204:
        raise Exception(
            f"Failed to delete deployment ID {deployment_id}: {response.text}"
        )

    print(f"Deployment ID {deployment_id} deleted")


if __name__ == "__main__":
    # create deployment and get the latest revision
    deployment_id = create_deployment()
    revisions = list_revisions(deployment_id)
    latest_revision = revisions["resources"][0]
    latest_revision_id = latest_revision["id"]

    # wait for latest revision to be DEPLOYED
    wait_for_deployment(deployment_id, latest_revision_id)

    # patch the deployment and get the latest revision
    patch_deployment(deployment_id)
    revisions = list_revisions(deployment_id)
    latest_revision = revisions["resources"][0]
    latest_revision_id = latest_revision["id"]

    # wait for latest revision to be DEPLOYED
    wait_for_deployment(deployment_id, latest_revision_id)

    # delete the deployment
    delete_deployment(deployment_id)
```
