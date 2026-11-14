# Trace LiveKit agents

> [!NOTE]
>
> This integration is in beta, so its API may change.

Use the LangSmith LiveKit integration to trace your [LiveKit Agents](https://docs.livekit.io/agents/) voice agents, including their transcripts and audio recordings. For high-level conventions, see [Voice tracing fundamentals](Voice%20tracing%20fundamentals.md).

> [!NOTE]
>
> This setup requires `langsmith[livekit]>=0.11.2` and `livekit-agents>=1.6`. LiveKit Agents 1.7 and later require `langsmith[livekit]>=0.12.4`.

Each conversation appears as one LangSmith trace with its pipeline events, latency, and token metrics.

> [!NOTE]
>
> In an [agent-based workspace](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

## Install

Install the integration along with the LiveKit plugins your agent uses:

```bash pip
pip install "langsmith[livekit]" "livekit-agents[openai,silero,turn-detector]"
```

```bash uv
uv add "langsmith[livekit]" "livekit-agents[openai,silero,turn-detector]"
```

## Set environment variables

Sending traces to an agent requires `langsmith>=0.14.9`.

The integration reads your LangSmith credentials from the environment and exports to LangSmith for you via OpenTelemetry:

```bash .env
LANGSMITH_API_KEY=<your-langsmith-api-key>
LANGSMITH_TRACING=true
LANGSMITH_AGENT_ID="<your-agent-id>"
LANGSMITH_AGENT_ENVIRONMENT="local"
LIVEKIT_URL=<your-livekit-url>
LIVEKIT_API_KEY=<your-livekit-api-key>
LIVEKIT_API_SECRET=<your-livekit-api-secret>
OPENAI_API_KEY=<your-openai-api-key>
```

## Set up tracing

Call `configure_livekit` once before creating your `AgentServer`.

```python
from langsmith.integrations.livekit import configure_livekit
from livekit import agents
from livekit.agents import Agent, AgentServer, AgentSession

# Enable tracing before creating agents.
configure_livekit()

server = AgentServer()

@server.rtc_session()
async def my_agent(ctx: agents.JobContext):
    session = AgentSession(
        stt="openai/gpt-4o-mini-transcribe",
        llm="openai/gpt-4o-mini",
        tts="openai/tts-1:alloy",
    )
    await session.start(
        room=ctx.room,
        agent=Agent(instructions="You are a helpful assistant."),
        record={"audio": True},
    )
```

`configure_livekit()` uses LiveKit session recordings by default. The `record={"audio": True}` option tells LiveKit to create the recording.

This setup works for both STT/LLM/TTS cascades and speech-to-speech (realtime) models. Realtime models need one extra call to capture the user's transcript. For more information, see [Use a realtime model](#use-a-realtime-model).

### Use your own tracer provider

If your agent already manages an OpenTelemetry `TracerProvider`, add the LangSmith processor to that provider and register it with LiveKit:

```python
from langsmith.integrations.livekit import LiveKitLangSmithSpanProcessor
from livekit.agents import telemetry
from opentelemetry.sdk.trace import TracerProvider

provider = TracerProvider()  # your own provider
processor = LiveKitLangSmithSpanProcessor()
provider.add_span_processor(processor)
telemetry.set_tracer_provider(provider)
```

## Group a conversation into a thread

To group a conversation's runs into a LangSmith [thread](../../../../Debug/Configure%20threads.md), call `set_thread_id` inside the session handler. Use a unique ID for each active session:

```python
from langsmith.integrations.livekit import configure_livekit, set_thread_id

configure_livekit()

@server.rtc_session()
async def my_agent(ctx: agents.JobContext):
    thread_id = ctx.job.id  # or any id that identifies the conversation
    set_thread_id(thread_id)
    ...
```

## Use a realtime model

For a speech-to-speech (realtime) model, call `instrument_session` after creating the `AgentSession` to capture the user's transcript. Pass the same thread ID to `set_thread_id` and `instrument_session`:

```python
from langsmith.integrations.livekit import configure_livekit, set_thread_id
from livekit.plugins import openai as lk_openai

processor = configure_livekit()

@server.rtc_session()
async def my_agent(ctx: agents.JobContext):
    thread_id = ctx.job.id  # or any id that identifies the conversation
    set_thread_id(thread_id)

    session = AgentSession(llm=lk_openai.realtime.RealtimeModel(voice="marin"))
    processor.instrument_session(session, thread_id)  # capture the user transcript

    await session.start(
        room=ctx.room,
        agent=Agent(instructions="You are a helpful assistant."),
        record={"audio": True},
    )
```

Only call `instrument_session` for realtime models. STT/LLM/TTS cascades already capture the user's transcript, so calling it there records each user turn twice.

## Record the conversation audio

By default, the integration uses LiveKit's session recording. Use Egress mode when you record to external storage instead.

### Record with LiveKit's session recording

Turn on LiveKit's session recording.

```python
from langsmith.integrations.livekit import configure_livekit
from livekit import agents
from livekit.agents import Agent, AgentServer, AgentSession

configure_livekit()

server = AgentServer()

@server.rtc_session()
async def my_agent(ctx: agents.JobContext):
    session = AgentSession(...)
    await session.start(
        room=ctx.room,
        agent=Agent(instructions="You are a helpful assistant."),
        record={"audio": True},
    )
```

By default, the LiveKit integration will capture the recording from LiveKit if present.

> [!NOTE]
>
> In console mode, also pass `--record` on the command line (`python agent.py console --record`). Without it LiveKit creates the recorder but never starts it, so there is no file to attach. The recording reflects what was played to the client, so a barge-in shows up truncated.

### Record with Egress

Use [LiveKit Egress](https://docs.livekit.io/home/egress/overview/) when you want the recording in your own object storage or need video. Egress recording delivery requires a thread ID. Configure the integration for Egress, then call `complete_recording` after the Egress file is available:

```python
import asyncio
import os
import time

from langsmith.integrations.livekit import configure_livekit, set_thread_id
from livekit import agents, api
from livekit.agents import Agent, AgentServer, AgentSession

RECORDING_BUCKET = os.environ["RECORDING_BUCKET"]

processor = configure_livekit(
    recording_mode="egress",
    recording_timeout_seconds=180,
)
server = AgentServer()

async def wait_for_egress(
    lkapi: api.LiveKitAPI,
    egress_id: str,
    timeout_seconds: float = 120,
) -> api.EgressInfo:
    deadline = time.monotonic() + timeout_seconds
    failed_statuses = {
        api.EgressStatus.EGRESS_FAILED,
        api.EgressStatus.EGRESS_ABORTED,
        api.EgressStatus.EGRESS_LIMIT_REACHED,
    }
    while time.monotonic() < deadline:
        response = await lkapi.egress.list_egress(
            api.ListEgressRequest(egress_id=egress_id)
        )
        if response.items:
            info = response.items[0]
            if info.status == api.EgressStatus.EGRESS_COMPLETE:
                return info
            if info.status in failed_statuses:
                raise RuntimeError(f"Egress failed with status {info.status}")
        await asyncio.sleep(1)
    raise TimeoutError(f"Egress {egress_id} did not complete in time")

@server.rtc_session()
async def my_agent(ctx: agents.JobContext):
    thread_id = ctx.job.id  # unique per session; ctx.room.name is "console" in console mode
    set_thread_id(thread_id)  # routes the Egress recording to this trace
    key = f"recordings/{thread_id}.ogg"

    # Start an audio-only room-composite egress to your storage.
    lkapi = api.LiveKitAPI()  # reads LIVEKIT_URL / LIVEKIT_API_KEY / LIVEKIT_API_SECRET
    egress = await lkapi.egress.start_room_composite_egress(
        api.RoomCompositeEgressRequest(
            room_name=ctx.room.name,
            audio_only=True,
            file_outputs=[
                api.EncodedFileOutput(
                    file_type=api.EncodedFileType.OGG,
                    filepath=key,
                    s3=api.S3Upload(
                        bucket=RECORDING_BUCKET,
                        region=os.environ["AWS_REGION"],
                        access_key=os.environ["AWS_ACCESS_KEY_ID"],
                        secret=os.environ["AWS_SECRET_ACCESS_KEY"],
                    ),
                )
            ],
        )
    )

    async def attach_recording():
        try:
            info = await wait_for_egress(lkapi, egress.egress_id)  # poll until EGRESS_COMPLETE
            audio = download_from_storage(RECORDING_BUCKET, key)  # your storage client
            processor.complete_recording(
                thread_id,
                data=audio,
                # EgressInfo.started_at is a Unix timestamp in nanoseconds. This is
                # when the egress worker began recording, which is what aligns the
                # audio start with the trace.
                started_at=info.started_at / 1e9,
            )
        except Exception:
            processor.complete_recording(thread_id, data=None)

    ctx.add_shutdown_callback(attach_recording)

    session = AgentSession(...)
    await session.start(room=ctx.room, agent=Agent(instructions="..."))
```

`download_from_storage` represents your storage client's download operation. The default attachment name and MIME type are `recording.ogg` and `audio/ogg`. Set `name` or `mime_type` in `complete_recording` if your Egress output uses another format.

> [!NOTE]
>
> Always call `complete_recording`, including on failure with `data=None`. Otherwise, the integration waits for `recording_timeout_seconds` (30 seconds by default) before exporting the trace without audio. Using `complete_recording` to capture Egress recordings requires setting a `thread_id`.

## Next steps

> [card] [Voice fundamentals](Voice%20tracing%20fundamentals.md)
>
> Core conventions for tracing voice agents.

> [card] [Upload files with traces](../../Manual%20instrumentation/Upload%20files%20with%20traces.md)
>
> Attach the conversation audio recording to your trace.
