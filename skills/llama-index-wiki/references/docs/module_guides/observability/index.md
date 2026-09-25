# developers.llamaindex.ai/python/framework/module_guides/observability/index.md
> https://developers.llamaindex.ai/python/framework/module_guides/observability/index.md

--- title: Observability | Developer Documentation ---

LlamaIndex provides **one-click observability** 🔭 to allow you to build principled LLM applications in a production setting.
A key requirement for principled development of LLM applications over your data (RAG systems, agents) is being able to observe, debug, and evaluate your system - both as a whole and for each component.
This feature allows you to seamlessly integrate the LlamaIndex library with powerful observability/evaluation tools offered by our partners. Configure a variable once, and you’ll be able to do things like the following:
- View LLM/prompt inputs/outputs - Ensure that the outputs of any component (LLMs, embeddings) are performing as expected - View call traces for both indexing and querying
Each provider has similarities and differences. Take a look below for the full set of guides for each one!
**NOTE:**
Observability is now being handled via the `instrumentation` module (available in v0.10.20 and later.)
A lot of the tooling and integrations mentioned in this page use our legacy `CallbackManager` or don’t use `set_global_handler`. We’ve marked these integrations as such!
## Usage Pattern
To toggle, you will generally just need to do the following:

# general usage set_global_handler("<handler_name>", **kwargs) ```
Note that all `kwargs` to `set_global_handler` are passed to the underlying callback handler.
And that’s it! Executions will get seamlessly piped to downstream service and you’ll be able to access features such as viewing execution traces of your application.
## Integrations
### OpenTelemetry
OpenTelemetry [1] is a widely used open-source service for tracing and observability, with numerous backend integrations (such as Jaeger, Zipkin or Prometheus).
Our OpenTelemetry integration traces all the events produced by pieces of LlamaIndex code, including LLMs, Agents, RAG pipeline components and many more: everything you would get out with LlamaIndex native instrumentation you can export in OpenTelemetry format!
You can install the library with:

``` pip install llama-index-observability-otel ```
And can use it in your code with the default settings, as in this example with a RAG pipeline:
``` from llama_index.observability.otel import LlamaIndexOpenTelemetry from llama_index.core import SimpleDirectoryReader, VectorStoreIndex from llama_index.llms.openai import OpenAI from llama_index.embeddings.openai import OpenAIEmbedding from llama_index.core import Settings
# initialize the instrumentation object instrumentor = LlamaIndexOpenTelemetry()
if __name__ == "__main__": embed_model = OpenAIEmbedding(model_name="text-embedding-3-small") llm = OpenAI(model="gpt-4.1-mini")
# start listening! instrumentor.start_registering()
# register events documents = SimpleDirectoryReader( input_dir="./data/paul_graham/" ).load_data()
index = VectorStoreIndex.from_documents(documents, embed_model=embed_model) query_engine = index.as_query_engine(llm=llm)
query_result_one = query_engine.query("Who is Paul?") query_result_two = query_engine.query("What did Paul do?") ```
Or you can use a more complex and customized set-up, such as in the following example:
``` import json from pydantic import BaseModel, Field from typing import List
from llama_index.observability.otel import LlamaIndexOpenTelemetry from opentelemetry.exporter.otlp.proto.http.trace_exporter import ( OTLPSpanExporter, )
# define a custom span exporter span_exporter = OTLPSpanExporter("http://0.0.0.0:4318/v1/traces")
# initialize the instrumentation object instrumentor = LlamaIndexOpenTelemetry( service_name_or_resource="my.test.service.1", span_exporter=span_exporter, debug=True, )

if __name__ == "__main__": instrumentor.start_registering() # ... your code here ```

We also have a demo repository [2] where we show how to trace agentic workflows and pipe the registered traces into a Postgres database.
### LlamaTrace (Hosted Arize Phoenix)
We’ve partnered with Arize on LlamaTrace [3], a hosted tracing, observability, and evaluation platform that works natively with LlamaIndex open-source users and has integrations with LlamaCloud.
This is built upon the open-source Arize Phoenix [4] project. Phoenix provides a notebook-first experience for monitoring your models and LLM Applications by providing:
- LLM Traces - Trace through the execution of your LLM Application to understand the internals of your LLM Application and to troubleshoot problems related to things like retrieval and tool execution. - LLM Evals - Leverage the power of large language models to evaluate your generative model or application’s relevance, toxicity, and more.

Then create an account on LlamaTrace: <https://llamatrace.com/login>. Create an API key and put it in the `PHOENIX_API_KEY` variable below.

# setup Arize Phoenix for logging/observability import llama_index.core import os
PHOENIX_API_KEY = "<API_KEY>" os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"api_key={PHOENIX_API_KEY}" llama_index.core.set_global_handler( "arize_phoenix", endpoint="https://llamatrace.com/v1/traces" )
... ```

- LlamaCloud Agent with LlamaTrace [5]

### SigNoz
SigNoz [6] is an open source observability framework. It is built natively off of OpenTelemetry, offers traces, logs, and metrics all in one pane, and has both self hosted and cloud deployment options. By using SigNoz with LlamaIndex, you can view detailed traces of all RAG and Agent workflows, while keeping track of important metrics like token usage, latency, error rates, LLM model distribution and much more.

Install the following dependencies:

``` pip install \ opentelemetry-distro \ opentelemetry-exporter-otlp \ opentelemetry-instrumentation-httpx \ opentelemetry-instrumentation-system-metrics \ llama-index \ openinference-instrumentation-llama-index ```
Next, add automatic instrumentation:

``` opentelemetry-bootstrap --action=install ```
Then, run your LlamaIndex application with auto-instrumentation:

``` OTEL_RESOURCE_ATTRIBUTES="service.name=<service_name>" \ OTEL_EXPORTER_OTLP_ENDPOINT="https://ingest.<region>.signoz.cloud:443" \ OTEL_EXPORTER_OTLP_HEADERS="signoz-ingestion-key=<your_ingestion_key>" \ OTEL_EXPORTER_OTLP_PROTOCOL=grpc \ OTEL_TRACES_EXPORTER=otlp \ OTEL_METRICS_EXPORTER=otlp \ OTEL_LOGS_EXPORTER=otlp \ OTEL_PYTHON_LOG_CORRELATION=true \ OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true \ opentelemetry-instrument <your_run_command> ```

- `<service_name>` is the name of your service - Set the `<region>` to match your SigNoz Cloud region [7] - Replace `<your_ingestion_key>` with your SigNoz ingestion key [8] - Replace `<your_run_command>` with the actual command you would use to run your application. For example: `python main.py`
> 📌 Note: Using self-hosted SigNoz? Most steps are identical. To adapt this guide, update the endpoint and remove the ingestion key header as shown in Cloud → Self-Hosted [9].
You will now be able to see any traces, logs, and metrics that are automatically or manually exported by your LlamaIndex application usage.
[10]

- SigNoz LlamaIndex Integration Docs [11] - SigNoz LLamaIndex Q\&A RAG Demo [12]
### Weights and Biases (W\&B) Weave
W\&B Weave [13] is a framework for tracking, experimenting with, evaluating, deploying, and improving LLM applications. Designed for scalability and flexibility, Weave supports every stage of your application development workflow.

The integration leverages LlamaIndex’s `instrumentation` module to register spans/events as Weave calls. By default, Weave automatically patches and tracks calls to common LLM libraries and frameworks [14].
Install the `weave` library:

``` pip install weave ```
Get a W\&B API Key:
If you don’t already have a W\&B account, create one by visiting <https://wandb.ai> and copy your API key from <https://wandb.ai/authorize>. When prompted to authenticate, enter the API key.
``` import weave from llama_index.llms.openai import OpenAI

# Initialize Weave with your project name weave.init("llamaindex-demo")
# All LlamaIndex operations are now automatically traced llm = OpenAI(model="gpt-4o-mini") response = llm.complete("William Shakespeare is ") print(response) ```

weave quickstart
Traces include execution time, token usage, cost, inputs/outputs, errors, nested operations, and streaming data. If you are new to Weave tracing, learn more about how to navigate it here [15].
If you have a custom function which is not traced, decorate it with `@weave.op()` [16].
You can also control the patching behavior using the `autopatch_settings` argument in `weave.init`. For example if you don’t want to trace a library/framework you can turn it off like this:
``` weave.init(..., autopatch_settings={"openai": {"enabled": False}}) ```
No additional LlamaIndex configuration is required; tracing begins once `weave.init()` is called.

The integration with LlamaIndex supports almost every component of LlamaIndex — streaming/async, completions, chat, tool calling, agents, workflows, and RAG support. Learn more about them in the official W\&B Weave × LlamaIndex [17] documentation.
### MLflow
MLflow [18] is an open-source MLOps/LLMOps platform, focuses on the full lifecycle for machine learning projects, ensuring that each phase is manageable, traceable, and reproducible. **MLflow Tracing** is an OpenTelemetry-based tracing capability and supports one-click instrumentation for LlamaIndex applications.

Since MLflow is open-source, you can start using it without any account creation or API key setup. Jump straight into the code after installing the MLflow package!
``` import mlflow
mlflow.llama_index.autolog() # Enable mlflow tracing ```


MLflow LlamaIndex integration also provides experiment tracking, evaluation, dependency management, and more. Check out the MLflow documentation [19] for more details.
#### Support Table
MLflow Tracing support the full range of LlamaIndex features. Some new features like AgentWorkflow [20] requires MLflow >= 2.18.0.
| Streaming | Async | Engine | Agents | Workflow | AgentWorkflow | | --------- | ----- | ------ | ------ | ----------- | ------------- | | ✅ | ✅ | ✅ | ✅ | ✅ (>= 2.18) | ✅ (>= 2.18)

### OpenLLMetry
OpenLLMetry [21] is an open-source project based on OpenTelemetry for tracing and monitoring LLM applications. It connects to [all major observability platforms] [22] and installs in minutes.

``` from traceloop.sdk import Traceloop
Traceloop.init() ```

- OpenLLMetry

### Arize Phoenix (local)
You can also choose to use a **local** instance of Phoenix through the open-source project.
In this case you don’t need to create an account on LlamaTrace or set an API key for Phoenix. The phoenix server will launch locally.

To install the integration package, do `pip install -U llama-index-callbacks-arize-phoenix`.
Then run the following code:
``` # Phoenix can display in real time the traces automatically # collected from your LlamaIndex application. # Run all of your LlamaIndex applications as usual and traces # will be collected and displayed in Phoenix.

import phoenix as px
# Look for a URL in the output to open the App in a browser. px.launch_app() # The App is initially empty, but as you proceed with the steps below, # traces will appear automatically as your LlamaIndex application runs.

import llama_index.core
llama_index.core.set_global_handler("arize_phoenix") ... ```

- Auto-Retrieval Guide with Pinecone and Arize Phoenix [23] - Arize Phoenix Tracing Tutorial [24]
### Langfuse 🪢
Langfuse [25] is an open source LLM engineering platform to help teams collaboratively debug, analyze and iterate on their LLM Applications. With the Langfuse integration, you can track and monitor performance, traces, and metrics of your LlamaIndex application. Detailed traces [26] of the context augmentation and the LLM querying processes are captured and can be inspected directly in the Langfuse UI.

Make sure you have both `llama-index` and `langfuse` installed.

``` pip install llama-index langfuse openinference-instrumentation-llama-index ```
Next, set up your Langfuse API keys. You can get these keys by signing up for a free Langfuse Cloud [27] account or by self-hosting Langfuse [28]. These environment variables are essential for the Langfuse client to authenticate and send data to your Langfuse project.

# Get keys for your project from the project settings page: https://cloud.langfuse.com
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..." os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..." os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com" # 🇪🇺 EU region # os.environ["LANGFUSE_HOST"] = "https://us.cloud.langfuse.com" # 🇺🇸 US region ```

With the environment variables set, we can now initialize the Langfuse client. `get_client()` initializes the Langfuse client using the credentials provided in the environment variables.
``` from langfuse import get_client
langfuse = get_client()
# Verify connection if langfuse.auth_check(): print("Langfuse client is authenticated and ready!") else: print("Authentication failed. Please check your credentials and host.") ```

Now, we initialize the OpenInference LlamaIndex instrumentation [29]. This third-party instrumentation automatically captures LlamaIndex operations and exports OpenTelemetry (OTel) spans to Langfuse.
``` from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
# Initialize LlamaIndex instrumentation LlamaIndexInstrumentor().instrument() ```
You can now see the logs of your LlamaIndex application in Langfuse:
LlamaIndex example trace [30]
*Example trace link in Langfuse [31]*

- Langfuse Documentation [32] - Tracing LlamaIndex Agents [33]
### Literal AI
Literal AI [34] is the go-to LLM evaluation and observability solution, enabling engineering and product teams to ship LLM applications reliably, faster and at scale. This is possible through a collaborative development cycle involving prompt engineering, LLM observability, LLM evaluation and LLM monitoring. Conversation Threads and Agent Runs can be automatically logged on Literal AI.
The simplest way to get started and try out Literal AI is to signup on our cloud instance [35]. You can then navigate to **Settings**, grab your API key, and start logging!

- Install the Literal AI Python SDK with `pip install literalai` - On your Literal AI project, go to **Settings** and grab your API key - If you are using a self-hosted instance of Literal AI, also make note of its base URL
Then add the following lines to your applicative code :

# You should provide your Literal AI API key and base url using the following environment variables: # LITERAL_API_KEY, LITERAL_API_URL set_global_handler("literalai") ```

- Literal AI integration with Llama Index [36] - Build a Q\&A application with LLamaIndex and monitor it with Literal AI [37]
### Comet Opik
Opik [38] is an open-source end to end LLM Evaluation Platform built by Comet.
To get started, simply sign up for an account on Comet [39] and grab your API key.

- Install the Opik Python SDK with `pip install opik` - In Opik, get your API key from the user menu. - If you are using a self-hosted instance of Opik, also make note of its base URL.
You can configure Opik using the environment variables `OPIK_API_KEY`, `OPIK_WORKSPACE` and `OPIK_URL_OVERRIDE` if you are using a self-hosted instance [40]. You can set these by calling:

``` export OPIK_API_KEY="<API_KEY>" export OPIK_WORKSPACE="<OPIK_WORKSPACE - Often the same as your API key>"
# Optional #export OPIK_URL_OVERRIDE="<OPIK_URL_OVERRIDE>" ```
You can now use the Opik integration with LlamaIndex by setting the global handler:
``` from llama_index.core import Document, VectorStoreIndex, set_global_handler
# You should provide your OPIK API key and Workspace using the following environment variables: # OPIK_API_KEY, OPIK_WORKSPACE set_global_handler( "opik", )
# This example uses OpenAI by default so don't forget to set an OPENAI_API_KEY index = VectorStoreIndex.from_documents([Document.example()]) query_engine = index.as_query_engine()
questions = [ "Tell me about LLMs", "How do you fine-tune a neural network ?", "What is RAG ?", ]
for question in questions: print(f"> \033[92m{question}\033[0m") response = query_engine.query(question) print(response) ```
You will see the following traces in Opik:
Opik integration with LlamaIndex

- Llama-index + Opik documentation page [41] - Llama-index integration cookbook [42]
### Argilla
Argilla [43] is a collaboration tool for AI engineers and domain experts who need to build high-quality datasets for their projects.
To get started, you need to deploy the Argilla server. If you have not done so, you can easily deploy it following this guide [44].

[Column 1]
``` from llama_index.core.instrumentation import get_dispatcher from argilla_llama_index import ArgillaHandler
argilla_handler = ArgillaHandler( dataset_name="query_llama_index", api_url="http://localhost:6900", api_key="<API_KEY>", number_of_retrievals=2, ) root_dispatcher = get_dispatcher() root_dispatcher.add_span_handler(argilla_handler) root_dispatcher.add_event_handler(argilla_handler) ```

[Column 2]
- Install the Argilla LlamaIndex integration package with `pip install argilla-llama-index` - Initialize the ArgillaHandler. The `<api_key>` is in the `My Settings` page of your Argilla Space but make sure you are logged in with the `owner` account you used to create the Space. The `<api_url>` is the URL shown in your browser. - Add the ArgillaHandler to the dispatcher.


- Getting started with Argilla’s LlamaIndex Integration [45] - Other example tutorials [46]
Argilla integration with LlamaIndex
### Agenta
Agenta [47] is an **open-source** LLMOps platform that helps developers and product teams build robust AI applications powered by LLMs. It offers all the tools for **observability**, **prompt management and engineering**, and **LLM evaluation**.

Install the necessary dependencies for the integration:

``` pip install agenta llama-index openinference-instrumentation-llama-index ```
Set up your API credentials and initialize Agenta:
``` import os import agenta as ag from openinference.instrumentation.llama_index import LlamaIndexInstrumentor

# Set your Agenta credentials os.environ["AGENTA_API_KEY"] = "your_agenta_api_key" os.environ[ "AGENTA_HOST" ] = "https://cloud.agenta.ai" # Use your self-hosted URL if applicable

# Initialize Agenta SDK ag.init()
# Enable LlamaIndex instrumentation LlamaIndexInstrumentor().instrument() ```
Build your instrumented application:
``` @ag.instrument() def document_search_app(user_query: str): """ Document search application using LlamaIndex. Loads documents, builds a searchable index, and answers user queries. """ # Load documents from local directory docs = SimpleDirectoryReader("data").load_data()

# Build vector search index search_index = VectorStoreIndex.from_documents(docs)
# Initialize query processor query_processor = search_index.as_query_engine()
# Process user query answer = query_processor.query(user_query)
return answer ```
Once this is set up, Agenta will automatically capture all execution steps. You can then view the traces in Agenta to debug your application, link them to specific configurations and prompts, evaluate their performance, query the data, and monitor key metrics.
Agenta integration with LlamaIndex
#### Example Guides
- Documentation Observability for LlamaIndex with Agenta [48] - Notebook Observability for LlamaIndex with Agenta [49]
### Deepeval
DeepEval (by Confident AI) [50] is an open-source evaluation framework for LLM applications. As you “unit test” your LLM app using DeepEval’s 14+ default metrics it currently offers (summarization, hallucination, answer relevancy, faithfulness, RAGAS, etc.), you can debug failing test cases through this tracing integration with LlamaIndex, or debug unsatisfactory evaluations in **production** through DeepEval’s hosted evaluation platform, Confident AI [51], that runs referenceless evaluations in production.

``` pip install -U deepeval llama-index ```
``` import deepeval from deepeval.integrations.llama_index import instrument_llama_index
import llama_index.core.instrumentation as instrument
# Login deepeval.login("<your-confident-api-key>")
# Let DeepEval collect traces instrument_llama_index(instrument.get_dispatcher()) ```
[52]

- Evaluate Llama Index Agents [53] - Tracing Llama Index Agents [54]
### Maxim AI
Maxim AI [55] is an Agent Simulation, Evaluation & Observability platform that helps developers build, monitor, and improve their LLM applications. The Maxim integration with LlamaIndex provides comprehensive tracing, monitoring, and evaluation capabilities for your RAG systems, agents, and other LLM workflows.

Install the required packages:

``` pip install maxim-py ```
Set up your environment variables:
``` import os from dotenv import load_dotenv
# Load environment variables from .env file load_dotenv()
# Get environment variables MAXIM_API_KEY = os.getenv("MAXIM_API_KEY") MAXIM_LOG_REPO_ID = os.getenv("MAXIM_LOG_REPO_ID")
# Verify required environment variables are set if not MAXIM_API_KEY: raise ValueError("MAXIM_API_KEY environment variable is required") if not MAXIM_LOG_REPO_ID: raise ValueError("MAXIM_LOG_REPO_ID environment variable is required") ```

Initialize Maxim and instrument LlamaIndex:
``` from maxim import Config, Maxim from maxim.logger import LoggerConfig from maxim.logger.llamaindex import instrument_llamaindex
# Initialize Maxim logger maxim = Maxim(Config(api_key=os.getenv("MAXIM_API_KEY"))) logger = maxim.logger(LoggerConfig(id=os.getenv("MAXIM_LOG_REPO_ID")))
# Instrument LlamaIndex with Maxim observability # Set debug=True to see detailed logs during development instrument_llamaindex(logger, debug=True)
print("✅ Maxim instrumentation enabled for LlamaIndex") ```
Now your LlamaIndex applications will automatically send traces to Maxim:
``` from llama_index.core.agent import FunctionAgent from llama_index.core.tools import FunctionTool from llama_index.llms.openai import OpenAI

# Define tools and create agent def add_numbers(a: float, b: float) -> float: """Add two numbers together.""" return a + b

add_tool = FunctionTool.from_defaults(fn=add_numbers) llm = OpenAI(model="gpt-4o-mini", temperature=0)
agent = FunctionAgent( tools=[add_tool], llm=llm, verbose=True, system_prompt="You are a helpful calculator assistant.", )
# This will be automatically logged by Maxim instrumentation import asyncio
response = await agent.run("What is 15 + 25?") print(f"Response: {response}") ```

- Maxim Instrumentation Cookbook - Maxim AI Documentation [56]
[57]
## Other Partner `One-Click` Integrations (Legacy Modules)
These partner integrations use our legacy `CallbackManager` or third-party calls.
### Langfuse
This integration is deprecated. We recommend using the new instrumentation-based integration with Langfuse as described here [32].

# Make sure you've installed the 'llama-index-callbacks-langfuse' integration package.
# NOTE: Set your environment variables 'LANGFUSE_SECRET_KEY', 'LANGFUSE_PUBLIC_KEY' and 'LANGFUSE_HOST' # as shown in your langfuse.com project settings.
set_global_handler("langfuse") ```

- Langfuse Callback Handler - Langfuse Tracing with PostHog
[58]
### OpenInference
OpenInference [59] is an open standard for capturing and storing AI model inferences. It enables experimentation, visualization, and evaluation of LLM applications using LLM observability solutions such as Phoenix [4].

llama_index.core.set_global_handler("openinference")
# NOTE: No need to do the following from llama_index.callbacks.openinference import OpenInferenceCallbackHandler from llama_index.core.callbacks import CallbackManager from llama_index.core import Settings
# callback_handler = OpenInferenceCallbackHandler() # Settings.callback_manager = CallbackManager([callback_handler])
# Run your LlamaIndex application here... for query in queries: query_engine.query(query)
# View your LLM app data as a dataframe in OpenInference format. from llama_index.core.callbacks.open_inference_callback import as_dataframe
query_data_buffer = llama_index.core.global_handler.flush_query_data_buffer() query_dataframe = as_dataframe(query_data_buffer) ```
**NOTE**: To unlock capabilities of Phoenix, you will need to define additional steps to feed in query/ context dataframes. See below!

- OpenInference Callback Handler - Evaluating Search and Retrieval with Arize Phoenix [60]
### TruEra TruLens
TruLens allows users to instrument/evaluate LlamaIndex applications, through features such as feedback functions and tracing.
#### Usage Pattern + Guides
``` # use trulens from trulens_eval import TruLlama

tru_query_engine = TruLlama(query_engine)
# query tru_query_engine.query("What did the author do growing up?") ```


- Trulens Guide - Quickstart Guide with LlamaIndex + TruLens [61] - Google Colab [62]
### HoneyHive
HoneyHive allows users to trace the execution flow of any LLM workflow. Users can then debug and analyze their traces, or customize feedback on specific trace events to create evaluation or fine-tuning datasets from production.

[Column 1]
set_global_handler( "honeyhive", project="My HoneyHive Project", name="My LLM Workflow Name", api_key="<API_KEY>", )
# NOTE: No need to do the following from llama_index.core.callbacks import CallbackManager
# from honeyhive.utils.llamaindex_tracer import HoneyHiveLlamaIndexTracer from llama_index.core import Settings
# hh_tracer = HoneyHiveLlamaIndexTracer( # project="My HoneyHive Project", # name="My LLM Workflow Name", # api_key="<API_KEY>", # ) # Settings.callback_manager = CallbackManager([hh_tracer]) ```

[Column 2]
  *Use Perfetto to debug and analyze your HoneyHive traces*


- HoneyHive Callback Handler
### PromptLayer
PromptLayer allows you to track analytics across LLM calls, tagging, analyzing, and evaluating prompts for various use-cases. Use it with LlamaIndex to track the performance of your RAG prompts and more.

``` import os
os.environ["PROMPTLAYER_API_KEY"] = "<PROMPTLAYER_API_KEY>"
from llama_index.core import set_global_handler
# pl_tags are optional, to help you organize your prompts and apps set_global_handler("promptlayer", pl_tags=["paul graham", "essay"]) ```

- PromptLayer
### Langtrace
Langtrace [63] is a robust open-source tool that supports OpenTelemetry and is designed to trace, evaluate, and manage LLM applications seamlessly. Langtrace integrates directly with LlamaIndex, offering detailed, real-time insights into performance metrics such as accuracy, evaluations, and latency.

``` pip install langtrace-python-sdk ```

``` from langtrace_python_sdk import ( langtrace, ) # Must precede any llm module imports
langtrace.init(api_key="<API_KEY>") ```

- Langtrace [64]
### OpenLIT
OpenLIT [65] is an OpenTelemetry-native GenAI and LLM Application Observability tool. It’s designed to make the integration process of observability into GenAI projects with just a single line of code. OpenLIT provides OpenTelemetry Auto instrumentation for various LLMs, VectorDBs and Frameworks like LlamaIndex. OpenLIT provides insights into your LLM Applications performance, tracing of requests, over view metrics on usage like costs, tokens and a lot more.

``` pip install openlit ```

``` import openlit
openlit.init() ```

- OpenLIT’s Official Documentation [66]
### AgentOps
AgentOps [67] helps developers build, evaluate, and monitor AI agents. AgentOps will help build agents from prototype to production, enabling agent monitoring, LLM cost tracking, benchmarking, and more.
#### Install
Terminal window
``` pip install llama-index-instrumentation-agentops ```

``` from llama_index.core import set_global_handler
# NOTE: Feel free to set your AgentOps environment variables (e.g., 'AGENTOPS_API_KEY') # as outlined in the AgentOps documentation, or pass the equivalent keyword arguments # anticipated by AgentOps' AOClient as **eval_params in set_global_handler.

set_global_handler("agentops") ```
### Simple (LLM Inputs/Outputs)
This simple observability tool prints every LLM input/output pair to the terminal. Most useful for when you need to quickly enable debug logging on your LLM application.
#### Usage Pattern
``` import llama_index.core
llama_index.core.set_global_handler("simple") ```
#### Guides
- MLflow [19]
## More observability
- Callbacks Guide

[1] https://opentelemetry.io
[2] https://github.com/run-llama/agents-observability-demo
[3] https://llamatrace.com/
[4] https://github.com/Arize-ai/phoenix
[5] https://github.com/run-llama/llamacloud-demo/blob/main/examples/tracing/llamacloud_tracing_phoenix.ipynb
[6] https://signoz.io/
[7] https://signoz.io/docs/ingestion/signoz-cloud/overview/#endpoint
[8] https://signoz.io/docs/ingestion/signoz-cloud/keys/
[9] https://signoz.io/docs/ingestion/cloud-vs-self- hosted/#cloud-to-self-hosted
[10] https://signoz.io/img/docs/llm/llamaindex/llamaindex-detailed-trace-view.webp
[11] https://signoz.io/docs/llamaindex-observability/
[12] https://github.com/SigNoz/llamaindex-rag-opentelemetry-demo
[13] https://weave-docs.wandb.ai/
[14] https://weave-docs.wandb.ai/guides/integrations/
[15] https://weave- docs.wandb.ai/guides/tracking/trace-tree
[16] https://weave-docs.wandb.ai/guides/tracking/ops
[17] https://weave-docs.wandb.ai/guides/integrations/llamaindex
[18] https://mlflow.org/docs/latest/llms/tracing/index.html
[19] https://mlflow.org/docs/latest/llms/llama-index/index.html
[20] https://www.llamaindex.ai/blog/introducing-agentworkflow-a-powerful-system-for-building-ai-agent-systems
[21] https://github.com/traceloop/openllmetry
[22] https://www.traceloop.com/docs/openllmetry/integrations/introduction
[23] https://docs.llamaindex.ai/en/latest/examples/vector_stores/pinecone_auto_retriever/?h=phoenix
[24] https://colab.research.google.com/github/Arize-ai/phoenix/blob/main/tutorials/tracing/llama_index_tracing_tutorial.ipynb
[25] https://langfuse.com/docs
[26] https://langfuse.com/docs/tracing
[27] https://cloud.langfuse.com/
[28] https://langfuse.com/self-hosting
[29] https://docs.arize.com/phoenix/tracing/integrations-tracing/llamaindex
[30] https://langfuse.com/images/cookbook/integration-llamaindex-workflows/llamaindex-trace.gif
[31] https://cloud.langfuse.com/project/cloramnkj0002jz088vzn1ja4/traces/6f554d6b-a2bc-4fba-904f-aa54de2897ca?display=preview
[32] https://langfuse.com/docs/integrations/llama-index/get-started
[33] https://langfuse.com/docs/integrations/llama-index/workflows
[34] https://literalai.com/
[35] https://cloud.getliteral.ai/
[36] https://docs.getliteral.ai/integrations/llama-index
[37] https://github.com/Chainlit/literal-cookbook/blob/main/python/llamaindex-integration
[38] https://www.comet.com/docs/opik/?utm_source=llama-index\&utm_medium=docs\&utm_campaign=opik\&utm_content=home_page
[39] https://www.comet.com/signup?from=llm\&utm_medium=github\&utm_source=llama-index\&utm_campaign=opik
[40] https://www.comet.com/docs/opik/self-host/self_hosting_opik
[41] https://www.comet.com/docs/opik/tracing/integrations/llama_index?utm_source=llamaindex\&utm_medium=docs\&utm_campaign=opik
[42] https://www.comet.com/docs/opik/cookbook/llama-index?utm_source=llama-index\&utm_medium=docs\&utm_campaign=opik
[43] https://github.com/argilla-io/argilla
[44] https://docs.argilla.io/latest/getting_started/quickstart/
[45] https://github.com/argilla-io/argilla-llama-index/blob/main/docs/tutorials/getting_started.ipynb
[46] https://github.com/argilla-io/argilla-llama-index/tree/main/docs/tutorials
[47] https://agenta.ai
[48] https://docs.agenta.ai/observability/integrations/llamaindex
[49] https://github.com/agenta-ai/agenta/blob/main/examples/jupyter/integrations/observability-openinference-llamaindex.ipynb
[50] https://github.com/confident-ai/deepeval
[51] https://documentation.confident-ai.com/docs
[52] https://confident-bucket.s3.us-east-1.amazonaws.com/llama-index%3Atrace.gif
[53] https://deepeval.com/integrations/frameworks/langchain
[54] https://documentation.confident-ai.com/docs/llm-tracing/integrations/llamaindex
[55] https://www.getmaxim.ai/
[56] https://www.getmaxim.ai/docs/sdk/python/integrations/llamaindex/llamaindex
[57] https://cdn.getmaxim.ai/public/images/llamaindex.gif
[58] https://static.langfuse.com/llamaindex-langfuse-docs.gif
[59] https://github.com/Arize-ai/open-inference-spec
[60] https://colab.research.google.com/github/Arize-ai/phoenix/blob/main/tutorials/llama_index_search_and_retrieval_tutorial.ipynb
[61] https://github.com/truera/trulens/blob/trulens-eval-0.20.3/trulens_eval/examples/quickstart/llama_index_quickstart.ipynb
[62] https://colab.research.google.com/github/truera/trulens/blob/trulens-eval-0.20.3/trulens_eval/examples/quickstart/llama_index_quickstart.ipynb
[63] https://github.com/Scale3-Labs/langtrace
[64] https://docs.langtrace.ai/supported-integrations/llm-frameworks/llamaindex
[65] https://github.com/openlit/openlit
[66] https://docs.openlit.io/latest/integrations/llama-index
[67] https://github.com/AgentOps-AI/agentops
