# Migrate to BYOC

> Copy users, datasets, prompts, experiments, Fleet resources, and other data from an existing LangSmith instance into a BYOC data plane.

The [LangSmith data migration tool](https://github.com/langchain-ai/langsmith-data-migration-tool) copies data from an existing LangSmith Cloud organization or [self-hosted](../Self-hosted/Self-hosted%20LangSmith.md) instance into a BYOC data plane. The tool copies data (as opposed to moving data over), so the source instance is unchanged and stays available during the move.

Run the migration after your data plane is [active and reachable](AWS/BYOC%20onboarding.md). Trace migration is supported on AWS. Contact the LangChain team to arrange it, and plan the [manual steps](#move-data-the-tool-does-not-migrate) alongside the tool.

## Supported resources

The tool migrates the following resources between a source instance and a destination data plane:

| Resource | Details |
| - | - |
| Users and roles | Custom roles, organization members, and workspace memberships. |
| Datasets | Datasets with their examples and file attachments. |
| Experiments | Experiments, experiment runs, and feedback, migrated with their datasets. |
| Annotation queues | Queue configuration and settings. Migrated queues start empty. |
| Automation rules | Project automation rules, mapped onto destination projects. |
| Prompts | Prompts with the full commit history. |
| Charts | Monitoring charts and dashboards. |
| Custom model pricing | Workspace-custom model price entries. |
| Engine issues | Per-project Engine configuration and detected issues. Issues migrate as metadata, including the proposed fix, without their linked traces or pull requests. |
| Fleet | Agents, shared skills, MCP servers, integrations, auth providers, schedules, triggers, webhooks, usage limits, sandbox policies, and workspace secrets. |
| Context Hub | Context Hub agents and skills, including files, repository metadata, commit history, and commit tags. |

Each resource type has its own command, flags, and caveats. For the command reference, see the [tool README](https://github.com/langchain-ai/langsmith-data-migration-tool/blob/main/README.md).

## Migrate with the tool

**1. Install the tool**

Install the latest release with `uv`, `uvx`, or `pip`. For the current install commands, see [Installation](https://github.com/langchain-ai/langsmith-data-migration-tool#installation).

Verify the install:

```bash
langsmith-migrator --help
```

**2. Create the destination workspaces**

Workspace IDs differ between instances, so create the target workspaces in the data plane first. See the `Create workspaces` section of the [BYOC onboarding docs](AWS/BYOC%20onboarding.md).

Migration commands run per workspace pair. Repeat them for each pair.

**3. Create the destination tracing projects**

The tool does not create tracing projects. Create the projects you need in the destination workspace before you migrate automation rules or charts, or those mappings have no target.

**4. Configure the connection details**

Set the source and destination credentials and endpoints:

```bash
export LANGSMITH_OLD_API_KEY="<SECRET>"
export LANGSMITH_NEW_API_KEY="<SECRET>"
export LANGSMITH_OLD_BASE_URL="<source_instance_api_url>"
export LANGSMITH_NEW_BASE_URL="https://<data_plane_host>"
export LANGSMITH_VERIFY_SSL=true
```

> [!NOTE]
>
> `OLD` refers to your current LangSmith deployment, and `NEW` refers to the destination BYOC data plane:
>
> * **`LANGSMITH_OLD_API_KEY`**: An API key from your current deployment with permission to read all resources you want to migrate. For LangSmith Cloud at [smith.langchain.com](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-byoc-migration), create it under **Settings > API Keys**. For another Cloud region or a self-hosted instance, use that deployment's UI.
> * **`LANGSMITH_NEW_API_KEY`**: An API key created under **Settings > API Keys** at [aws.smith.langchain.com](https://aws.smith.langchain.com). Scope it to a workspace in your destination BYOC data plane. See [Create an API key](../Account/Create%20an%20account%20and%20API%20key.md#api-keys).
> * **`LANGSMITH_OLD_BASE_URL`**: Your current deployment's API URL. For LangSmith Cloud in GCP US, use `https://api.smith.langchain.com`. For another Cloud region, use its [regional API URL](../Account/Create%20an%20account%20and%20API%20key.md#configure-the-sdk). For self-hosted LangSmith, use your instance's API URL.
> * **`LANGSMITH_NEW_BASE_URL`**: Your destination BYOC data plane's API URL, including `https://`. Find it under **Settings > Data Planes**. See [BYOC onboarding](AWS/BYOC%20onboarding.md).

> [!WARNING]
>
> The destination key must be scoped to a workspace in the target data plane. An organization-scoped key does not work.
>
> To migrate Fleet agents with an owner, use a personal access token (`lsv2_pt_*`) as the destination key. Workspace API keys carry no user identity, so agents created with them have no owner.

**5. Test both connections**

```bash
langsmith-migrator test
```

**6. Run the migration**

Use the interactive wizard to walk through every resource type:

```bash
langsmith-migrator migrate-all
```

To migrate one resource type at a time, run its command instead, such as `datasets`, `prompts`, or `fleet`. Add `--dry-run` to preview a step without writing, and `-v` for verbose output. Use `langsmith-migrator resume` to retry pending or failed items from a previous session.

For per-command flags, workspace mapping, and project mapping, see the [tool README](https://github.com/langchain-ai/langsmith-data-migration-tool/blob/main/README.md).

## Complete the Fleet manual steps

[Fleet](../../No-code%20agents/Fleet/No-code%20agents%20with%20LangSmith%20Fleet.md) resources migrate with the `fleet` command, but some values cannot cross instances. Complete the following in the destination workspace after migration:

* **Re-enter secret values**: The Fleet API does not return secret values. The tool creates workspace secrets and auth provider client secrets as empty placeholders.
* **Re-authenticate OAuth connections**: Per-user agent connections, such as Gmail, Slack, and GitHub, are tied to individual user tokens. Each user must reconnect.
* **Re-share agents**: Per-user access lists keep only user IDs that exist on the destination. The tool reports which users it removed.
* **Check agent models**: The tool substitutes a model when the destination catalog does not offer the source model. It logs every substitution.
* **Configure infrastructure-level settings**: OAuth providers, the GitHub App, and the Slack app can be recreated in the `Settings > Oauth Providers` and `Fleet > Integrations` UI.

Fleet migrators never overwrite resources that already exist on the destination, so re-running `fleet` is safe.

## Complete the Engine manual steps

[Engine](../../Engine/LangSmith%20Engine.md) issues migrate with the `issues` command. The command creates any tracing project that has Engine data and is missing on the destination. Issues migrate as metadata only, and the command skips issues and project configurations that already exist on the destination.

To run Engine in the data plane, complete these steps in order:

1. **Enable Engine for the data plane**: A LangChain operator enables Engine for your data plane. Contact your LangChain account team to request it.
2. **Turn on Engine**: An Organization Admin goes to **Settings** > **Engine**, selects the data plane, and turns on Engine.
3. **Add model provider credentials**: An Organization Admin adds credentials for your own model providers. Credentials are not migrated. See [Engine on BYOC](../../Engine/Self-hosted%20and%20BYOC/LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md#engine-on-byoc).
4. **Reconnect GitHub**: Configure your GitHub App in the destination, then reconnect repositories in each Engine project. Repository settings migrate, but they work only after the destination has a GitHub connection. See [Configure GitHub for Engine on BYOC](../../Engine/Self-hosted%20and%20BYOC/Configure%20GitHub%20for%20Engine%20on%20self-hosted%20and%20BYOC.md#configure-the-app-on-byoc).
5. **Recreate notification destinations**: Connect your Slack app and add Slack, Jira, or webhook destinations again. See [Engine notifications](../../Engine/LangSmith%20Engine%20notifications.md).
6. **Let Engine re-detect traces**: Migrated issues have no linked traces, pull requests, or suggested actions. Engine links new traces to the issues as it analyzes traces in the data plane.

## Move data the tool does not migrate

### Traces

Trace migration is supported on AWS. Contact the LangChain team to arrange trace migration to your BYOC data plane. The data migration tool does not migrate traces.

To keep a separate copy of historical traces, [bulk export](../../Monitor/Debug/Bulk%20export%20trace%20data/Bulk%20export%20trace%20data.md) them to an S3-compatible bucket.

To move tracing applications, create API keys scoped to a workspace in the data plane, then repoint the application:

* **Cut over**: Set `LANGSMITH_ENDPOINT` to the data plane endpoint and `LANGSMITH_API_KEY` to the new key. See [Trace to a data plane](BYOC%20usage.md#trace-to-a-data-plane).
* **Dual trace**: Write to the old instance and the data plane during the transition. See [Trace to multiple endpoints](BYOC%20usage.md#trace-to-multiple-endpoints).

### Deployed agents

Redeploy agents that run on your existing instance into a workspace in the data plane. Use the LangSmith UI or the API. You may also need to recreate service accounts, image pull secrets, and other resources in the data plane cluster.

For agent databases and caches, choose one of the following:

* Create new instances in the data plane and point the redeployed agents at them. Start empty, or restore from a backup of the old instance.
* Point the redeployed agents at your existing database instances, and reach them from the data plane cluster over PrivateLink or VPC peering.

For more information, see [LangSmith Agent Server](../../Deploy/Get%20started/LangSmith%20Agent%20Server.md).

### Insights reports

[Insights](../../Monitor/Observe/Monitoring%20%26%20alerting/Discover%20errors%20and%20usage%20patterns%20with%20Insights.md) reports are not migrated across instances. To keep a report, open its details in the LangSmith UI and select **Download**.

## See also

* [BYOC onboarding](AWS/BYOC%20onboarding.md)
* [BYOC usage](BYOC%20usage.md)
* [Bulk export trace data](../../Monitor/Debug/Bulk%20export%20trace%20data/Bulk%20export%20trace%20data.md)
