# Hybrid

> A LangSmith Agent Server setup where you self-host Agent Servers in your infrastructure and send traces to LangSmith Cloud or a self-hosted LangSmith instance.

Hybrid is a hosting setup for [LangSmith Agent Server](../Get%20started/LangSmith%20Agent%20Server.md), which **deploys and runs agents in production**.

In a hybrid platform setup, you self-host [Agent Servers](../Agent%20Server/Capabilities/Agent%20Server.md) in your own infrastructure and send their traces to LangSmith, where LangSmith can be either a [self-hosted](../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) instance or [LangSmith Cloud](../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md).

This setup gives you control over where your agent workloads run while letting you choose the [LangSmith platform option](../../LangSmith%20setup/Overview/Hosting/Set%20up%20LangSmith.md) that best fits your observability and compliance requirements.

## Components

| Component | Where it runs | Who manages it |
| - | - | - |
| Agent Servers (The server that runs your applications.) | Your infrastructure | You |
| LangSmith (tracing, evaluation, prompts) | Self-hosted in your infrastructure, or LangSmith SaaS | You (self-hosted) or LangSmith (SaaS) |

> [!NOTE]
>
> Hybrid is an Agent Server hosting setup (agent serving). To set up LangSmith for observability, evaluation, and prompt engineering only, see [Set up LangSmith](../../LangSmith%20setup/Overview/Hosting/Set%20up%20LangSmith.md).

## Workflow

1. Build and test your agent locally.
2. Deploy your agent to an [Agent Server running in your infrastructure](#self-host-your-agent-servers).
3. Send the agent's traces to [LangSmith (self-hosted or SaaS) for observability and evaluation](#choose-where-traces-are-sent).

### Self-host your Agent Servers

Deploy standalone Agent Servers using Docker, Docker Compose, or Kubernetes. See the [standalone server guide](Self-host%20standalone%20servers.md) for prerequisites, environment variables, and platform-specific instructions.

### Choose where traces are sent

Agent Servers send traces to LangSmith based on the `LANGSMITH_ENDPOINT` environment variable:

* **LangSmith SaaS**: Omit `LANGSMITH_ENDPOINT` to use the default (GCP US), or set it to the endpoint for your region:

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
          `https://api.smith.langchain.com`
        </td>
      </tr>

      <tr>
        <td>GCP EU</td>

        <td>
          `https://eu.api.smith.langchain.com`
        </td>
      </tr>

      <tr>
        <td>GCP APAC</td>

        <td>
          `https://apac.api.smith.langchain.com`
        </td>
      </tr>

      <tr>
        <td>AWS US</td>

        <td>
          `https://aws.api.smith.langchain.com`
        </td>
      </tr>

      <tr><td>Azure US</td>
      <td>`https://azure.api.smith.langchain.com`</td></tr>
    </tbody>
  </table>

* **Self-hosted LangSmith**: Set `LANGSMITH_ENDPOINT` to the hostname of your [self-hosted LangSmith](../../LangSmith%20setup/Self-hosted/Self-hosted%20LangSmith.md) instance.

In both cases, authenticate with a [LangSmith API key](../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md) issued by the LangSmith instance you are tracing to.
