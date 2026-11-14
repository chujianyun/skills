# Resolve an agent environment

> Resolve an agent environment, experiment, or workspace evaluator traces to the session ID required by query and feedback APIs.

Some APIs identify an [agent environment](../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20environments.md) by its backing trace-storage UUID, returned as `session_id`. Resolve the agent identifier and environment to get this UUID. Use it in API fields named `session_id`, `project_id`, or `project_ids`. These are existing API names for the same identifier. Resolution also supports [experiments](../../../Test/Get%20started/Evaluation%20concepts.md) and workspace [evaluator](../../../Test/Evaluators/Manage%20evaluators.md) traces. Use the returned ID for operations such as:

* Querying runs, threads, and traces with `project_ids`
* Reading or updating the environment's trace-storage settings, saved views, insights, and alerts

> [!NOTE]
>
> Resolving an agent needs LangSmith 0.18.7rc1 or later, and is not supported on BYOC data planes yet. The examples need the following SDK versions:
>
> * **Python**: `langsmith>=0.14.9`
> * **TypeScript**: `langsmith@>=0.11.0`
> * **Java**: `com.langchain.smith:langsmith-java` 0.1.0-beta.26 or later
> * **Go**: `github.com/langchain-ai/langsmith-go` v0.28.0 or later

For integrations that require `project_name`, [retrieve the agent environment](../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) and use its `tracer_session_name`.

## What you can resolve

Resolve any of the following to get its `session_id`:

> [tab] Python
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import langsmith as ls
>
> agent = ls.agent_address("checkout", "production")  # An agent's environment
> experiment = ls.experiment_address("<experiment-id>")  # An experiment
> evaluators = ls.evaluator_address()  # The workspace's evaluators
> ```

> [tab] TypeScript
>
> ```typescript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { AgentAddress, EvaluatorAddress, ExperimentAddress } from "langsmith";
>
> const agent = new AgentAddress("checkout", "production"); // An agent's environment
> const experiment = new ExperimentAddress("<experiment-id>"); // An experiment
> const evaluators = new EvaluatorAddress(); // The workspace's evaluators
> ```

> [tab] Java
>
> ```java theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import com.langchain.smith.address.AgentAddress;
> import com.langchain.smith.address.EvaluatorAddress;
> import com.langchain.smith.address.ExperimentAddress;
>
> AgentAddress agent = new AgentAddress("checkout", "production"); // An agent's environment
> ExperimentAddress experiment = new ExperimentAddress("<experiment-id>"); // An experiment
> EvaluatorAddress evaluators = new EvaluatorAddress(); // The workspace's evaluators
> ```

> [tab] Go
>
> ```go theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> // An agent's environment
> agent, err := langsmith.NewAgentAddress("checkout", "production")
> // An experiment
> experiment, err := langsmith.NewExperimentAddress("<experiment-id>")
> // The workspace's evaluators
> evaluators := langsmith.NewEvaluatorAddress()
> ```

## Resolve an agent and query its runs

> [tab] Python
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import asyncio
>
> import langsmith as ls
>
> client = ls.Client()
> agent = ls.agent_address("checkout", "production")
>
>
> async def main() -> None:
>     project = await client.sessions.resolve(**agent)
>
>     async for run in client.runs.query(project_ids=[project.session_id]):
>         print(run.id)
>
>
> asyncio.run(main())
> ```

> [tab] TypeScript
>
> ```ts theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { AgentAddress, Client } from "langsmith";
>
> const client = new Client();
> const agent = new AgentAddress("checkout", "production");
>
> const project = await client.sessions.resolve(agent);
>
> for await (const run of client.runs.query({
>   project_ids: [project.session_id],
> })) {
>   console.log(run.id);
> }
> ```

> [tab] Java
>
> ```java Java theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import com.langchain.smith.address.AgentAddress;
> import com.langchain.smith.client.LangsmithClient;
> import com.langchain.smith.client.okhttp.LangsmithOkHttpClient;
> import com.langchain.smith.models.runs.RunQueryV2Params;
> import java.time.OffsetDateTime;
>
> public class ResolveAgentExample {
>   public static void main(String[] args) throws Exception {
>     LangsmithClient client = LangsmithOkHttpClient.fromEnv();
>     AgentAddress agent = new AgentAddress("checkout", "production");
>
>     String projectId = client.sessions().resolve(agent.toApiAddress()).sessionId();
>
>     client
>         .runs()
>         .queryV2(
>             RunQueryV2Params.builder()
>                 .addProjectId(projectId)
>                 .minStartTime(OffsetDateTime.now().minusMonths(1))
>                 .build())
>         .items()
>         .forEach(run -> System.out.println(run.id().get()));
>   }
> }
> ```

> [tab] Go
>
> ```go theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> package main
>
> import (
> 	"context"
> 	"fmt"
> 	"time"
>
> 	"github.com/langchain-ai/langsmith-go"
> )
>
> func main() {
> 	ctx := context.Background()
> 	client := langsmith.NewClient()
> 	agent, err := langsmith.NewAgentAddress("checkout", "production")
> 	if err != nil {
> 		panic(err.Error())
> 	}
>
> 	project, err := client.Sessions.Resolve(ctx, langsmith.NewSessionResolveParams(agent))
> 	if err != nil {
> 		panic(err.Error())
> 	}
>
> 	runs, err := client.Runs.QueryV2(ctx, langsmith.RunQueryV2Params{
> 		ProjectIDs:   langsmith.F([]string{project.SessionID}),
> 		MinStartTime: langsmith.F(time.Now().UTC().AddDate(0, -1, 0)),
> 	})
> 	if err != nil {
> 		panic(err.Error())
> 	}
> 	for _, run := range runs.Items {
> 		fmt.Println(run.ID)
> 	}
> }
> ```

## Resolve an experiment and query its runs

Pass the experiment ID. The endpoint returns that same ID as `session_id`.

> [tab] Python
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import asyncio
>
> import langsmith as ls
>
> client = ls.Client()
> experiment_id = "<experiment-id>"
> experiment = ls.experiment_address(experiment_id)
>
>
> async def main() -> None:
>     project = await client.sessions.resolve(**experiment)
>
>     async for run in client.runs.query(project_ids=[project.session_id]):
>         print(run.id)
>
>
> asyncio.run(main())
> ```

> [tab] TypeScript
>
> ```ts theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { Client, ExperimentAddress } from "langsmith";
>
> const client = new Client();
> let experimentId = "<experiment-id>";
> const experiment = new ExperimentAddress(experimentId);
>
> const project = await client.sessions.resolve(experiment);
>
> for await (const run of client.runs.query({
>   project_ids: [project.session_id],
> })) {
>   console.log(run.id);
> }
> ```

> [tab] Java
>
> ```java Java theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import com.langchain.smith.address.ExperimentAddress;
> import com.langchain.smith.client.LangsmithClient;
> import com.langchain.smith.client.okhttp.LangsmithOkHttpClient;
> import com.langchain.smith.models.runs.RunQueryV2Params;
> import java.time.OffsetDateTime;
>
> public class ResolveExperimentExample {
>   public static void main(String[] args) {
>     LangsmithClient client = LangsmithOkHttpClient.fromEnv();
>     String experimentId = "<experiment-id>";
>     ExperimentAddress experiment = new ExperimentAddress(experimentId);
>
>     String projectId = client.sessions().resolve(experiment.toApiAddress()).sessionId();
>
>     client
>         .runs()
>         .queryV2(
>             RunQueryV2Params.builder()
>                 .addProjectId(projectId)
>                 .minStartTime(OffsetDateTime.now().minusMonths(1))
>                 .build())
>         .items()
>         .forEach(run -> System.out.println(run.id().get()));
>   }
> }
> ```

> [tab] Go
>
> ```go theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> package main
>
> import (
> 	"context"
> 	"fmt"
> 	"time"
>
> 	"github.com/langchain-ai/langsmith-go"
> )
>
> func main() {
> 	ctx := context.Background()
> 	client := langsmith.NewClient()
> 	experimentID := "<experiment-id>"
> 	experiment, err := langsmith.NewExperimentAddress(experimentID)
> 	if err != nil {
> 		panic(err.Error())
> 	}
>
> 	project, err := client.Sessions.Resolve(ctx, langsmith.NewSessionResolveParams(experiment))
> 	if err != nil {
> 		panic(err.Error())
> 	}
>
> 	runs, err := client.Runs.QueryV2(ctx, langsmith.RunQueryV2Params{
> 		ProjectIDs:   langsmith.F([]string{project.SessionID}),
> 		MinStartTime: langsmith.F(time.Now().UTC().AddDate(0, -1, 0)),
> 	})
> 	if err != nil {
> 		panic(err.Error())
> 	}
> 	for _, run := range runs.Items {
> 		fmt.Println(run.ID)
> 	}
> }
> ```

## Resolve the evaluators and query their runs

Evaluator traces share one storage destination per workspace, so the evaluator address takes no ID.

> [tab] Python
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import asyncio
>
> import langsmith as ls
>
> client = ls.Client()
> evaluators = ls.evaluator_address()
>
>
> async def main() -> None:
>     project = await client.sessions.resolve(**evaluators)
>
>     async for run in client.runs.query(project_ids=[project.session_id]):
>         print(run.id)
>
>
> asyncio.run(main())
> ```

> [tab] TypeScript
>
> ```ts theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { Client, EvaluatorAddress } from "langsmith";
>
> const client = new Client();
> const evaluators = new EvaluatorAddress();
>
> const project = await client.sessions.resolve(evaluators);
>
> for await (const run of client.runs.query({
>   project_ids: [project.session_id],
> })) {
>   console.log(run.id);
> }
> ```

> [tab] Java
>
> ```java Java theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import com.langchain.smith.address.EvaluatorAddress;
> import com.langchain.smith.client.LangsmithClient;
> import com.langchain.smith.client.okhttp.LangsmithOkHttpClient;
> import com.langchain.smith.models.runs.RunQueryV2Params;
> import java.time.OffsetDateTime;
>
> public class ResolveEvaluatorsExample {
>   public static void main(String[] args) {
>     LangsmithClient client = LangsmithOkHttpClient.fromEnv();
>     EvaluatorAddress evaluators = new EvaluatorAddress();
>
>     String projectId = client.sessions().resolve(evaluators.toApiAddress()).sessionId();
>
>     client
>         .runs()
>         .queryV2(
>             RunQueryV2Params.builder()
>                 .addProjectId(projectId)
>                 .minStartTime(OffsetDateTime.now().minusMonths(1))
>                 .build())
>         .items()
>         .forEach(run -> System.out.println(run.id().get()));
>   }
> }
> ```

> [tab] Go
>
> ```go theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> package main
>
> import (
> 	"context"
> 	"fmt"
> 	"time"
>
> 	"github.com/langchain-ai/langsmith-go"
> )
>
> func main() {
> 	ctx := context.Background()
> 	client := langsmith.NewClient()
> 	evaluators := langsmith.NewEvaluatorAddress()
>
> 	project, err := client.Sessions.Resolve(ctx, langsmith.NewSessionResolveParams(evaluators))
> 	if err != nil {
> 		panic(err.Error())
> 	}
>
> 	runs, err := client.Runs.QueryV2(ctx, langsmith.RunQueryV2Params{
> 		ProjectIDs:   langsmith.F([]string{project.SessionID}),
> 		MinStartTime: langsmith.F(time.Now().UTC().AddDate(0, -1, 0)),
> 	})
> 	if err != nil {
> 		panic(err.Error())
> 	}
> 	for _, run := range runs.Items {
> 		fmt.Println(run.ID)
> 	}
> }
> ```

## Errors

* LangSmith returns a `404` if nothing in the workspace matches, if the agent is archived, or if you cannot read the selected environment's traces. An agent's environments exist once the agent exists.
* On a BYOC data plane, the endpoint returns a `501`, because resolving is not supported there yet.

## See also

* [Log traces to an agent](../../Trace/Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md)
* [Agent Registry](../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md)
* [Agent environments](../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20environments.md)
