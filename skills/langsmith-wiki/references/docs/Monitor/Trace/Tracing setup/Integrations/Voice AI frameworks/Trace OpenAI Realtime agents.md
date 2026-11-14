# Trace OpenAI Realtime agents

> Trace OpenAI Realtime voice agents in LangSmith using the LangSmith SDK.

> [!NOTE]
>
> This integration is in beta, so its API may change.

OpenAI Realtime is a speech-to-speech model that streams typed events over a WebSocket. Regardless of whether you build it with a raw connection or the OpenAI Agents SDK, the integration captures each conversation as a single LangSmith trace, with a span for every meaningful event (transcripts, model responses, and tool calls) grouped by turn.

Trace your [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime) voice agents to LangSmith. For high-level conventions, see [Voice tracing fundamentals](Voice%20tracing%20fundamentals.md).

> [!NOTE]
>
> In an [agent-based workspace](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

## Choose an approach

There are two ways to build with the OpenAI Realtime API, and LangSmith provides a tracing integration for each:

* If you are connecting directly with the realtime client, use `wrap_realtime`.
* If you are building with the OpenAI Agents SDK, use `wrap_realtime_session` instead.

## Install

The `langsmith[openai-realtime]>=0.9.7` extra provides both wrappers:

```bash pip
pip install "langsmith[openai-realtime]"
```

```bash uv
uv add "langsmith[openai-realtime]"
```

## Set environment variables

Sending traces to an agent requires `langsmith>=0.14.9`.

```bash .env
LANGSMITH_API_KEY=<your-langsmith-api-key>
LANGSMITH_TRACING=true
LANGSMITH_AGENT_ID="<your-agent-id>"
LANGSMITH_AGENT_ENVIRONMENT="local"
OPENAI_API_KEY=<your-openai-api-key>
```

## Using the Realtime client

Use this when you open the WebSocket yourself with `client.realtime.connect()` and drive the event loop.

### Set up tracing

`wrap_realtime` returns a transparent proxy of your connection. Your existing `async for event in connection` loop, `session.update`, and tool handling stay the same:

```python
from langsmith.integrations.openai_realtime import wrap_realtime
from openai import AsyncOpenAI

client = AsyncOpenAI()

async with client.realtime.connect(model="gpt-realtime-2") as raw, wrap_realtime(
    raw,
) as connection:
    await connection.session.update(session={...})  # your existing config

    async for event in connection:
        ...  # your existing handling: play audio, run tools, update UI
```

> [!NOTE]
>
> Each conversation is captured as its own trace. To group it with related interactions in a LangSmith [thread](../../../../Debug/Configure%20threads.md) (for example to continue an earlier session or pick up from a text chat), pass a `thread_id`. Reusing the same ID across traces links their events together.

Any [`@traceable`](../../Manual%20instrumentation/Custom%20instrumentation.md) tools you run while handling an event nest under that event automatically.

> [!NOTE]
>
> Enable `input_audio_transcription` and the agent transcript in your `session.update` in order to view a transcript as part of the trace.

### Record the conversation audio

When you feed the proxy your microphone and playback audio, it attaches a single stereo recording (user left, agent right) to the trace. To flag barge-ins, use `is_agent_speaking`:

```python
import base64

async with client.realtime.connect(model="gpt-realtime-2") as raw, wrap_realtime(
    raw,
    is_agent_speaking=lambda: speaker.buffered_bytes() > 0,
) as connection:
    # Record the agent's audio from the speaker, so the recording reflects only
    # what was played — audio a barge-in discards before playback is never recorded.
    speaker.set_played_callback(connection.record_agent_audio)

    # Record the user's mic where you send it to the model.
    async def send_mic(mic_chunk):
        await connection.input_audio_buffer.append(
            audio=base64.b64encode(mic_chunk).decode("ascii")
        )
        connection.record_user_audio(mic_chunk)          # user mic PCM16 as sent

    async for event in connection:
        if event.type == "response.output_audio.delta":
            speaker.play(base64.b64decode(event.delta))
```

> [!NOTE]
>
> You should record the agent's audio from the speaker, so that the recording reflects only what was played. During a barge-in, generated audio is discarded before playback and should not be recorded. Doing this keeps the trace aligned with what the user actually heard.

## Using the OpenAI Agents SDK

Use this when you build the agent with the [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/realtime/guide/) (`RealtimeAgent` / `RealtimeRunner`), which owns the turn and tool-call loop.

> [!NOTE]
>
> The Agents SDK's built-in realtime tracing uploads to OpenAI's own dashboard. Call `agents.set_tracing_disabled(True)` to avoid a second, separate upload path.

### Set up tracing

`wrap_realtime_session` wraps the `RealtimeSession` and enters it for you. Iterate it as you would the original; the SDK runs tools and manages turns:

```python
from agents import set_tracing_disabled
from agents.realtime import RealtimeAgent, RealtimeRunner
from langsmith.integrations.openai_realtime import wrap_realtime_session

set_tracing_disabled(True)

runner = RealtimeRunner(
    starting_agent=RealtimeAgent(name="assistant", instructions="...", tools=[...]),
)
session = await runner.run()

async with wrap_realtime_session(
    session,
) as conn:
    async for event in conn:
        ...  # your handling: play audio, update UI
```

The conversation transcript is reconstructed from the session's `history` snapshots, so messages appear even though the SDK streams them as partials.

> [!NOTE]
>
> Each conversation is captured as its own trace. To group it with related interactions in a LangSmith [thread](../../../../Debug/Configure%20threads.md), for example to continue an earlier session or pick up from a text chat, pass a `thread_id`. Reusing the same ID across traces links their events together.

### Record the conversation audio

Feed the proxy your microphone and playback audio:

```python
# Record the agent's audio from the speaker, so the recording reflects only
# what was played — audio a barge-in discards before playback is never recorded.
speaker.set_played_callback(conn.record_agent_audio)

# Record the user's mic where you send it to the session.
async def send_mic(mic_chunk):
    await conn.send_audio(mic_chunk)
    conn.record_user_audio(mic_chunk)               # user mic PCM16 as sent

async for event in conn:
    if event.type == "audio":
        speaker.play(event.audio.data)
```

> [!NOTE]
>
> You should record the agent's audio from the speaker, so that the recording reflects only what was played. During a barge-in, generated audio is discarded before playback and should not be recorded. Doing this keeps the trace aligned with what the user actually heard.

## Next steps

> [card] [Voice fundamentals](Voice%20tracing%20fundamentals.md)
>
> Core conventions for tracing voice agents.

> [card] [Upload files with traces](../../Manual%20instrumentation/Upload%20files%20with%20traces.md)
>
> Attach the conversation audio recording to your trace.
