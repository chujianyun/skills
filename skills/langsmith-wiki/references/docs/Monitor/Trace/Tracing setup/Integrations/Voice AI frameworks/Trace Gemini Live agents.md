# Trace Gemini Live agents

> Trace Gemini Live voice agents in LangSmith using the LangSmith SDK.

> [!NOTE]
>
> This integration is in beta, so its API may change.

Gemini Live is a speech-to-speech model that streams typed events over a WebSocket. Whether you build with a raw `google-genai` connection or the Google Agent Development Kit (ADK), the integration captures each conversation as a single LangSmith trace with spans for transcripts, model responses, tool calls, turn boundaries, and interruptions.

Trace your [Gemini Live](https://ai.google.dev/gemini-api/docs/live-api) voice agents to LangSmith. For high-level conventions, see [Voice tracing fundamentals](Voice%20tracing%20fundamentals.md).

To trace non-live text agents, tools, and multi-agent workflows built with ADK, see [Trace Google ADK agents](../Agent%20frameworks/Trace%20Google%20ADK%20agents.md).

> [!NOTE]
>
> In an [agent-based workspace](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

## Choose an approach

LangSmith provides a tracing integration for each way to connect to Gemini Live:

* If you connect directly with `client.aio.live.connect(...)`, use `wrap_gemini_live`.
* If you build with [Google ADK](https://google.github.io/adk-docs/streaming/), use `LangSmithGoogleADKLivePlugin`.

## Install

### Use the Gemini Live client

Install the `gemini-live` extra for a raw `google-genai` connection:

```bash pip
pip install "langsmith[gemini-live]"
```

```bash uv
uv add "langsmith[gemini-live]"
```

### Use Google ADK

Install the `google-adk-live` extra for an ADK agent:

```bash pip
pip install "langsmith[google-adk-live]"
```

```bash uv
uv add "langsmith[google-adk-live]"
```

> [!NOTE]
>
> The ADK Live integration requires `langsmith[google-adk-live]>=0.9.7`. This extra is separate from the `langsmith[google-adk]` batch integration.

## Set environment variables

Sending traces to an agent requires `langsmith>=0.14.9`.

```bash .env
LANGSMITH_API_KEY=<your-langsmith-api-key>
LANGSMITH_TRACING=true
LANGSMITH_AGENT_ID="<your-agent-id>"
LANGSMITH_AGENT_ENVIRONMENT="local"
GOOGLE_API_KEY=<your-google-api-key>
GEMINI_LIVE_MODEL=<your-gemini-live-model>
```

## Use the Gemini Live client

Use this approach when your agent opens the WebSocket with `client.aio.live.connect(...)` and owns the audio and tool loops.

### Set up tracing

Enable input and output transcription in the live configuration. `wrap_gemini_live` returns a transparent proxy for the connected session, so your existing receive loop, audio handling, and tool dispatch remain unchanged:

```python
import os

from google import genai
from google.genai import types
from langsmith.integrations.gemini_live import wrap_gemini_live

model = os.environ["GEMINI_LIVE_MODEL"]
client = genai.Client()
config = types.LiveConnectConfig(
    response_modalities=[types.Modality.AUDIO],
    input_audio_transcription=types.AudioTranscriptionConfig(),
    output_audio_transcription=types.AudioTranscriptionConfig(),
)

async with (
    client.aio.live.connect(model=model, config=config) as raw,
    wrap_gemini_live(
        raw,
        model=model,
    ) as session,
):
    async for message in session.receive():
        ...  # play audio, run tools, handle barge-ins, and update the UI
```

> [!NOTE]
>
> Transcription is opt-in. To show transcripts in the trace, set both `input_audio_transcription` and `output_audio_transcription` on `LiveConnectConfig`.

### Group a conversation into a thread

Each wrapped session is captured as its own trace with its own thread ID. To supply an ID, for example to group the conversation with related interactions in a LangSmith [thread](../../../../Debug/Configure%20threads.md), pass `thread_id`:

```python
wrap_gemini_live(
    raw,
    model=model,
    thread_id=thread_id,
)
```

Create one wrapper per connected Gemini Live session. Each wrapper owns isolated tracing and transcript state, so concurrent conversations remain separate.

### Record the conversation audio

Feed microphone and playback audio to the wrapped session to attach a single stereo recording, with the user on the left channel and the agent on the right channel:

```python
RECORDING_SAMPLE_RATE = 24_000

async with (
    client.aio.live.connect(model=model, config=config) as raw,
    wrap_gemini_live(
        raw,
        model=model,
        sample_rate=RECORDING_SAMPLE_RATE,
        is_agent_speaking=lambda: speaker.buffered_bytes() > 0,
    ) as session,
):
    # Record audio after playback so discarded audio from a barge-in is omitted.
    speaker.set_played_callback(session.record_agent_audio)

    async def send_mic(mic_chunk):
        await session.send_realtime_input(
            audio=types.Blob(
                data=mic_chunk,
                mime_type=f"audio/pcm;rate={microphone.sample_rate}",
            )
        )
        session.record_user_audio(
            resample_pcm16(
                mic_chunk,
                microphone.sample_rate,
                RECORDING_SAMPLE_RATE,
            )
        )
```

Record both channels as PCM16 at the wrapper's `sample_rate`. Record the agent's audio from the speaker so the attachment reflects only what the user heard. For the underlying attachment API, see [Upload files with traces](../../Manual%20instrumentation/Upload%20files%20with%20traces.md).

## Use Google ADK

Use this approach when ADK owns the Gemini Live session and tool loop.

### Set up tracing

Import `LangSmithGoogleADKLivePlugin` and register it on your `Runner`. It runs alongside your `run_live` loop, so your loop only handles audio playback, barge-ins, and UI updates:

```python
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.runners import Runner
from google.genai import types as genai_types
from langsmith.integrations.google_adk_live import LangSmithGoogleADKLivePlugin

plugin = LangSmithGoogleADKLivePlugin()

runner = Runner(
    app_name="voice-app",
    agent=root_agent,
    session_service=session_service,
    plugins=[plugin],
)

run_config = RunConfig(
    response_modalities=["AUDIO"],
    streaming_mode=StreamingMode.BIDI,
    input_audio_transcription=genai_types.AudioTranscriptionConfig(),
    output_audio_transcription=genai_types.AudioTranscriptionConfig(),
)

async for event in runner.run_live(
    user_id=user_id,
    session_id=adk_session.id,
    live_request_queue=queue,
    run_config=run_config,
):
    ...  # play audio, handle barge-ins, and update the UI
```

> [!NOTE]
>
> Transcription is opt-in. To show transcripts, set both `input_audio_transcription` and `output_audio_transcription` on `RunConfig`.

> [!NOTE]
>
> On a graceful end, when the live request queue closes, ADK sends its `after_run` callback and the plugin finalizes the trace.
>
> On a cancelled run, such as a console app that stops `run_live` on Ctrl-C, ADK might not send that callback. Call `plugin.finalize(session_id=adk_session.id)` during teardown so the trace and audio attachment are finalized. The call is idempotent, so it does nothing if ADK's callback already ran.

### Group a conversation into a thread

Each conversation is captured as its own trace with its own thread ID. To supply an ID, for example to group the conversation with related interactions in a LangSmith [thread](../../../../Debug/Configure%20threads.md), pass a `thread_id_provider` to the plugin:

```python
plugin = LangSmithGoogleADKLivePlugin(
    thread_id_provider=lambda: thread_id,
)
```

A single plugin instance is shared across every `run_live` call and resolves the thread ID once at the start of each conversation. The default keeps concurrent conversations separate. If you pass a `thread_id_provider` on a server handling concurrent conversations, return the ID for the current conversation, for example by reading a `ContextVar` set at the start of each run.

### Record the conversation audio

Feed microphone and playback audio to the plugin to attach a single stereo recording, with the user on the left channel and the agent on the right channel:

```python
plugin.record_user_audio(mic_chunk)      # user mic PCM16
plugin.record_agent_audio(played_chunk)  # agent PCM16 as played
```

Record the user's microphone capture before resampling it for ADK, and record the agent's audio from the speaker. Feed both channels at the same sample rate. The plugin's `sample_rate` is 24 kHz by default. For the underlying attachment API, see [Upload files with traces](../../Manual%20instrumentation/Upload%20files%20with%20traces.md).

## Next steps

> [card] [Voice fundamentals](Voice%20tracing%20fundamentals.md)
>
> Core conventions for tracing voice agents.

> [card] [Upload files with traces](../../Manual%20instrumentation/Upload%20files%20with%20traces.md)
>
> Attach the conversation audio recording to your trace.
