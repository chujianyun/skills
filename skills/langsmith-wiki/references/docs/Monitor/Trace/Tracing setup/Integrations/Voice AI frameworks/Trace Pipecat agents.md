# Trace Pipecat agents

> [!NOTE]
>
> This integration is in beta, so its API may change.

Trace your [Pipecat](https://pipecat.ai/) voice agents to LangSmith with the LangSmith Pipecat integration. For high-level conventions, see [Voice tracing fundamentals](Voice%20tracing%20fundamentals.md).

> [!NOTE]
>
> The Pipecat integration requires `langsmith[pipecat]>=0.9.7`.

The integration hooks into the spans Pipecat already emits and maps them onto LangSmith's tracing format, so each conversation becomes a single LangSmith trace, with a span per pipeline stage (STT, LLM, TTS). This covers both the STT/LLM/TTS cascade and speech-to-speech (realtime) models. Realtime models (for example, `OpenAIRealtimeLLMService`) need one extra call to capture the user's transcript. See [When using Pipecat with a realtime model](#when-using-pipecat-with-a-realtime-model).

> [!NOTE]
>
> In an [agent-based workspace](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

## Install

Install the integration along with the Pipecat service extras your pipeline uses:

```bash pip
pip install "langsmith[pipecat]" "pipecat-ai[openai,local,tracing]"
```

```bash uv
uv add "langsmith[pipecat]" "pipecat-ai[openai,local,tracing]"
```

## Set environment variables

Sending traces to an agent requires `langsmith>=0.14.9`.

The integration reads your LangSmith credentials from the environment and exports to LangSmith for you via OpenTelemetry:

```bash .env
LANGSMITH_API_KEY=<your-langsmith-api-key>
LANGSMITH_TRACING=true
LANGSMITH_AGENT_ID="<your-agent-id>"
LANGSMITH_AGENT_ENVIRONMENT="local"
OPENAI_API_KEY=<your-openai-api-key>
```

## Set up tracing

Import `configure_pipecat` and call it once before building your pipeline. Enable tracing on the `PipelineTask`:

```python
from langsmith.integrations.pipecat import configure_pipecat
from pipecat.pipeline.task import PipelineParams, PipelineTask

# Install the tracer and the LangSmith span processor.
configure_pipecat()

task = PipelineTask(
    pipeline,
    params=PipelineParams(enable_metrics=True),
    enable_tracing=True,
    enable_turn_tracking=True,
    conversation_id=conversation_id,
)
```

> [!NOTE]
>
> Set `enable_tracing=True`, `enable_turn_tracking=True`, and `enable_metrics=True`. Turn tracking is required for tracing, and metrics drive the latency and token data on each span.

### Use a LangGraph or LangChain agent as the LLM

If your LLM stage is an in-process [LangGraph or LangChain](https://docs.langchain.com/oss/python/langgraph/overview.md) agent, its model and tool runs should nest inside Pipecat's `llm` span rather than forming a separate trace. To achieve this:

* Pass `configure_pipecat(llm_span_kind="chain")`. This avoids nested `llm` spans that don't actually represent inference requests.
* Set `LANGSMITH_TRACING_MODE=otel` in the environment. Without it, those runs post to LangSmith directly and form a separate trace instead of nesting.

### Use your own tracer provider

`configure_pipecat()` builds a `TracerProvider`, registers the LangSmith span processor, and wires it into Pipecat. To send spans through a `TracerProvider` you already manage (for example, one that also exports to another OpenTelemetry backend), skip `configure_pipecat` and add the processor to your provider directly:

```python
from langsmith.integrations.pipecat import PipecatLangSmithSpanProcessor

provider.add_span_processor(PipecatLangSmithSpanProcessor())
```

## Group a conversation into a thread

To group a conversation's runs into a LangSmith [thread](../../../../Debug/Configure%20threads.md) for thread-level views and token and cost aggregation, call `set_thread_id` once per conversation before its spans are emitted:

```python
from langsmith.integrations.pipecat import configure_pipecat, set_thread_id

configure_pipecat()
set_thread_id(conversation_id)
```

## When using Pipecat with a realtime model

With a speech-to-speech (realtime) model there is no separate speech-to-text stage, so the user's transcript is never emitted as an OTel span. Instead it arrives through the user context aggregator's `on_user_turn_message_added` callback, which Pipecat fires once it has the finalized user text. Without wiring it up, the trace shows only the assistant side.

Call `instrument_user_aggregator` once, right after building the context aggregator, so the SDK subscribes to that callback for you and pairs each transcript with its turn. It correlates by the id you pass to `set_thread_id`, so set that first and pass the same id:

> [!NOTE]
>
> `instrument_user_aggregator` requires `langsmith[pipecat]>=0.10.6`.

```python
from langsmith.integrations.pipecat import configure_pipecat, set_thread_id
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
from pipecat.services.openai.realtime.events import (
    AudioConfiguration,
    AudioInput,
    AudioOutput,
    InputAudioTranscription,
    SessionProperties,
)
from pipecat.services.openai.realtime.llm import OpenAIRealtimeLLMService

conversation_id = "..."  # any id that identifies the conversation
span_processor = configure_pipecat()
set_thread_id(conversation_id)

llm = OpenAIRealtimeLLMService(
    api_key=openai_api_key,
    settings=OpenAIRealtimeLLMService.Settings(
        model="gpt-realtime",
        session_properties=SessionProperties(
            # Enable input-audio transcription: OpenAI Realtime sends the model
            # raw audio and, by default, produces no user-side text. Without this
            # the context aggregator never fires, so the user's turns never reach
            # the trace.
            audio=AudioConfiguration(
                input=AudioInput(transcription=InputAudioTranscription()),
                output=AudioOutput(voice="marin"),
            ),
        ),
    ),
)

context = LLMContext(messages=[{"role": "system", "content": "..."}])
context_aggregator = LLMContextAggregatorPair(context, realtime_service_mode=True)
span_processor.instrument_user_aggregator(context_aggregator, conversation_id)  # capture the user transcript
```

For OpenAI Realtime, also enable input-audio transcription (`InputAudioTranscription`) on the session; otherwise the model receives raw audio and produces no user-side text, so the aggregator never fires. Other realtime services that surface the user's text through the aggregator themselves (for example, Gemini Live) need only the `instrument_user_aggregator` call, with no extra session configuration.

Only call `instrument_user_aggregator` for realtime models. In the STT/LLM/TTS cascade the transcript is already captured (from the speech-to-text stage), so calling it there would record the user's turns a second time.

## Record the conversation audio

Attach the conversation audio to the trace using Pipecat's [`AudioBufferProcessor`](https://docs.pipecat.ai/api-reference/server/utilities/audio/audio-buffer-processor). Place it after `transport.output()` so it captures what was actually played (after any barge-in truncation), hand it to the integration, and start it once the session is running:

```python
from pipecat.processors.audio.audio_buffer_processor import AudioBufferProcessor

span_processor = configure_pipecat()

# Stereo: user on the left channel, agent on the right.
audiobuffer = AudioBufferProcessor(num_channels=2, buffer_size=32_000)
span_processor.attach_audio_buffer(audiobuffer, conversation_id=conversation_id)

pipeline = Pipeline([
    transport.input(),
    stt,
    context_aggregator.user(),
    llm,
    tts,
    transport.output(),
    audiobuffer,                     # after output(): records what was heard
    context_aggregator.assistant(),
])

await audiobuffer.start_recording()
```

The integration attaches the recording to the conversation root when it ends. For the underlying attachment API, see [Upload files with traces](../../Manual%20instrumentation/Upload%20files%20with%20traces.md).

## Next steps

> [card] [Voice fundamentals](Voice%20tracing%20fundamentals.md)
>
> Core conventions for tracing voice agents.

> [card] [Upload files with traces](../../Manual%20instrumentation/Upload%20files%20with%20traces.md)
>
> Attach the conversation audio recording to your trace.
