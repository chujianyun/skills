# Self-host standalone servers

> Deploy standalone Agent Servers using Docker, Docker Compose, or Kubernetes without the LangSmith control plane.

This guide shows you how to deploy standalone [Agent Servers](../Agent%20Server/Capabilities/Agent%20Server.md) directly, without a [control plane](../Get%20started/Deployment%20components/LangSmith%20control%20plane.md). You can deploy the server independently and still send traces to LangSmith ([self-hosted](../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) or [Cloud](../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md)) for [observability](../../Monitor/Overview/LangSmith%20Observability.md) and [evaluation](../../Test/Get%20started/LangSmith%20Evaluation.md). Standalone servers are production-ready and provide the most lightweight option for running agents.

## Overview

You manage a simplified data plane (The runtime environment where your Agent Servers and agents execute.) made up of Agent Servers and their required backing services (PostgreSQL, Redis, etc.):

| Component | Responsibilities | Where it runs | Who manages it |
| - | - | - | - |
| **Control plane** | n/a | n/a | n/a |
| **Data plane** | <ul><li>Agent Servers</li><li>Postgres, Redis, etc.</li></ul> | Your infrastructure | You |

This option gives you full control over scaling, deployment, and CI/CD pipelines, while still allowing optional integration with LangSmith for tracing and evaluation.

> [!WARNING]
>
> Do not run standalone servers in serverless environments. Scale-to-zero may cause task loss and scaling up will not work reliably.

![Standalone server architecture](../../../assets/images/7e6a405387de-standalone-server-light.png)

### Workflow

1. Define and test your graph locally using the `langgraph-cli` or [Studio](../../Test/Test%20from%20Studio/LangSmith%20Studio.md).
2. Package your agent as a Docker image.
3. Deploy the Agent Server to your compute platform of choice (Kubernetes, Docker, VM).
4. Optionally, configure LangSmith API keys and endpoints so the server reports traces and evaluations back to LangSmith (self-hosted or SaaS).

### Supported compute platforms

* **Kubernetes**: Use the LangSmith Helm chart to run Agent Servers in a Kubernetes cluster. This is the recommended option for production-grade deployments.
* **Docker**: Run in any Docker-supported compute platform (local dev machine, VM, ECS, etc.). This is best suited for development or small-scale workloads.

> [!WARNING]
>
> For production deployments, use Kubernetes with the maintained LangSmith Helm chart. This is the production path that LangChain regularly tests. LangChain does not regularly test other orchestrators.
>
> Non-Kubernetes deployments have known gaps that you must implement and maintain yourself. These deployments may diverge further from the tested production path as the Helm chart evolves:
>
> * **Independent queue autoscaling**: Configure scaling policies and queue metrics for bursty, write-heavy workloads.
> * **Graceful run draining**: Configure shutdown draining and sufficient termination windows so in-flight runs can finish during deployments and scale-down events.
> * **Split-mode wiring**: Provision and connect separate API and queue services. The Helm chart handles this when `queue.enabled` is `true`.
> * **Reference scaling configuration**: Translate the [Agent Server scaling](Configure/Configure%20Agent%20Server%20for%20scale.md) settings, including `api.replicas`, `queue.replicas`, `numberOfJobsPerWorker`, and read replicas, into your orchestrator's task definitions and scaling policies.
> * **Version upgrades and support**: Maintain task definitions and apply version updates. LangChain tests and ships supported Helm chart version updates.

## Prerequisites

1. Use the [LangGraph CLI](../Get%20started/Reference/LangGraph%20CLI.md) to [test your application locally](../Get%20started/Develop%20%26%20test/Local%20development%20%26%20testing.md).
2. Use the [LangGraph CLI](../Get%20started/Reference/LangGraph%20CLI.md) to build a Docker image (i.e. `langgraph build`). To build on a network with no public internet access, see [Set up a build machine on a restricted network](Configure/Set%20up%20a%20build%20machine%20on%20a%20restricted%20network.md).
3. The following environment variables are needed for a data plane deployment.
   * `REDIS_URI`: Connection details to a Redis instance. Redis will be used as a pub-sub broker to enable streaming real time output from background runs. The value of `REDIS_URI` must be a valid [Redis connection URI](https://redis.readthedocs.io/en/stable/connections.html#redis.Redis.from_url).

     > [!NOTE]
     >
     > **Shared Redis Instance**
     > Multiple self-hosted deployments can share the same Redis instance. For example, for `Deployment A`, `REDIS_URI` can be set to `redis://<hostname_1>:<port>/1` and for `Deployment B`, `REDIS_URI` can be set to `redis://<hostname_1>:<port>/2`.
     >
     > `1` and `2` are different database numbers within the same instance, but `<hostname_1>` is shared. **The same database number cannot be used for separate deployments**.
   * `DATABASE_URI`: Postgres connection details. Postgres will be used to store assistants, threads, runs, persist thread state and long term memory, and to manage the state of the background task queue with 'exactly once' semantics. The value of `DATABASE_URI` must be a valid [Postgres connection URI](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING-URIS).

     > [!NOTE]
     >
     > **Shared Postgres Instance**
     > Multiple self-hosted deployments can share the same Postgres instance. For example, for `Deployment A`, `DATABASE_URI` can be set to `postgres://<user>:<password>@/<database_name_1>?host=<hostname_1>` and for `Deployment B`, `DATABASE_URI` can be set to `postgres://<user>:<password>@/<database_name_2>?host=<hostname_1>`.
     >
     > `<database_name_1>` and `database_name_2` are different databases within the same instance, but `<hostname_1>` is shared. **The same database cannot be used for separate deployments**.

     > [!TIP]
     >
     > You can optionally store checkpoint data in MongoDB instead of PostgreSQL. PostgreSQL is still required for all other server data. See [Configure checkpointer backend](../Agent%20Server/Develop%20your%20application/Persistence/Configure%20checkpointer%20backend.md) for details.
   * `LANGSMITH_API_KEY`: LangSmith API key.
   * `LANGGRAPH_CLOUD_LICENSE_KEY`: LangSmith license key. This will be used to authenticate ONCE at server start up.
   * `LANGSMITH_ENDPOINT`: To send traces to a [self-hosted LangSmith](../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) instance, set `LANGSMITH_ENDPOINT` to the hostname of the self-hosted LangSmith instance.
4. Egress to `https://beacon.langchain.com` from your network. This is required for license verification and usage reporting if not running in air-gapped mode. See the [Egress documentation](../../LangSmith%20setup/Self-hosted/Configure%20an%20instance/Egress%20for%20billing%20and%20operational%20telemetry.md) for more details.

> [!NOTE]
>
> Agent Server services listen on both IPv4 and IPv6 by default as of 0.14.0. No additional configuration is required for dual-stack clusters. To listen on a single address family, set `LANGGRAPH_SERVER_HOST` to `0.0.0.0` for IPv4 only or `::` for IPv6 only. See [Self-hosted Agent Server environment variables](Reference/Self-hosted%20Agent%20Server%20environment%20variables.md).

## Kubernetes

Use this [Helm chart](https://github.com/langchain-ai/helm/blob/main/charts/langgraph-cloud/README.md) to deploy an Agent Server to a Kubernetes cluster. This is the recommended setup for production standalone server deployments.

The Helm chart (v0.2.6+) supports MongoDB checkpointing with a bundled instance (dev/testing) or an external deployment (production). Set `mongo.enabled: true` in your values file. See [Configure checkpointer backend](../Agent%20Server/Develop%20your%20application/Persistence/Configure%20checkpointer%20backend.md#deploy-by-environment) for full configuration details.

## Docker

> [!WARNING]
>
> This Docker example is intended for local development and testing. For production, use the Kubernetes deployment.

Run the following `docker` command:

```shell
docker run \
    --env-file .env \
    -p 8123:8000 \
    -e REDIS_URI="foo" \
    -e DATABASE_URI="bar" \
    -e LANGSMITH_API_KEY="baz" \
    my-image
```

> [!NOTE]
>
> * You need to replace `my-image` with the name of the image you built in the prerequisite steps (from `langgraph build`)
>
> and you should provide appropriate values for `REDIS_URI`, `DATABASE_URI`, and `LANGSMITH_API_KEY`.
>
> * If your application requires additional environment variables, you can pass them in a similar way.

## Docker Compose

> [!WARNING]
>
> This Docker Compose example is intended for local development and testing. For production, use the Kubernetes deployment.

Use the following Docker Compose file:

```yml
volumes:
    langgraph-data:
        driver: local
services:
    langgraph-redis:
        image: redis:6
        healthcheck:
            test: redis-cli ping
            interval: 5s
            timeout: 1s
            retries: 5
    langgraph-postgres:
        image: postgres:16
        ports:
            - "5432:5432"
        environment:
            POSTGRES_DB: postgres
            POSTGRES_USER: postgres
            POSTGRES_PASSWORD: postgres
        volumes:
            - langgraph-data:/var/lib/postgresql/data
        healthcheck:
            test: pg_isready -U postgres
            start_period: 10s
            timeout: 1s
            retries: 5
            interval: 5s
    langgraph-api:
        image: ${IMAGE_NAME}
        ports:
            - "8123:8000"
        depends_on:
            langgraph-redis:
                condition: service_healthy
            langgraph-postgres:
                condition: service_healthy
        env_file:
            - .env
        environment:
            REDIS_URI: redis://langgraph-redis:6379
            LANGSMITH_API_KEY: ${LANGSMITH_API_KEY}
            DATABASE_URI: postgres://postgres:postgres@langgraph-postgres:5432/postgres?sslmode=disable
```

Run `docker compose up` with this file in the same folder.

> [accordion] With MongoDB checkpointing
>
> To store checkpoints in MongoDB instead of PostgreSQL, add a MongoDB service and configure the checkpointer backend. Set the backend to `"mongo"` in your `langgraph.json` or use the `LS_DEFAULT_CHECKPOINTER_BACKEND` environment variable. PostgreSQL is still required for all other server data.
>
> ```yml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> volumes:
>     langgraph-data:
>         driver: local
>     langgraph-mongo-data:
>         driver: local
> services:
>     langgraph-redis:
>         image: redis:6
>         healthcheck:
>             test: redis-cli ping
>             interval: 5s
>             timeout: 1s
>             retries: 5
>     langgraph-postgres:
>         image: postgres:16
>         ports:
>             - "5432:5432"
>         environment:
>             POSTGRES_DB: postgres
>             POSTGRES_USER: postgres
>             POSTGRES_PASSWORD: postgres
>         volumes:
>             - langgraph-data:/var/lib/postgresql/data
>         healthcheck:
>             test: pg_isready -U postgres
>             start_period: 10s
>             timeout: 1s
>             retries: 5
>             interval: 5s
>     langgraph-mongo:
>         image: mongo:7
>         command: ["mongod", "--replSet", "rs0"]
>         ports:
>             - "27017:27017"
>         volumes:
>             - langgraph-mongo-data:/data/db
>         healthcheck:
>             test: mongosh --eval "try { rs.status().ok } catch(e) { rs.initiate({_id:'rs0',members:[{_id:0,host:'langgraph-mongo:27017'}]}).ok }" --quiet
>             interval: 5s
>             timeout: 10s
>             retries: 10
>             start_period: 10s
>     langgraph-api:
>         image: ${IMAGE_NAME}
>         ports:
>             - "8123:8000"
>         depends_on:
>             langgraph-redis:
>                 condition: service_healthy
>             langgraph-postgres:
>                 condition: service_healthy
>             langgraph-mongo:
>                 condition: service_healthy
>         env_file:
>             - .env
>         environment:
>             REDIS_URI: redis://langgraph-redis:6379
>             LANGSMITH_API_KEY: ${LANGSMITH_API_KEY}
>             DATABASE_URI: postgres://postgres:postgres@langgraph-postgres:5432/postgres?sslmode=disable
>             LS_DEFAULT_CHECKPOINTER_BACKEND: mongo
>             LS_MONGODB_URI: mongodb://langgraph-mongo:27017/langgraph?replicaSet=rs0
> ```
>
> See [Configure checkpointer backend](../Agent%20Server/Develop%20your%20application/Persistence/Configure%20checkpointer%20backend.md) for more details on MongoDB configuration options.

This will launch an Agent Server on port `8123` (change the port mapping in `langgraph-api` if needed). Test if the application is healthy:

```shell
curl --request GET --url 0.0.0.0:8123/ok
```

Assuming everything is running correctly, you should see a response like:

```shell
{"ok":true}
```
