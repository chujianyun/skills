# Voice tracing fundamentals

> Best practices for tracing voice and audio agents in LangSmith, including conversation audio, single-trace conversations, and the audio modality flag.

[Tracing](../../../Observability%20concepts.md#traces) a voice agent is different from tracing a text agent. A conversation is continuous, bidirectional, and interruptible: users talk over the agent, change topics mid-sentence, and expect sub-second responses. To debug and evaluate these systems, your traces need to capture the conversation as a single, audio-aware unit rather than a series of disconnected text exchanges.

This page covers the core conventions for tracing voice applications in LangSmith. Follow these patterns regardless of which framework or model provider you use ([OpenAI Realtime](Trace%20OpenAI%20Realtime%20agents.md), [Gemini Live](Trace%20Gemini%20Live%20agents.md), [LiveKit](Trace%20LiveKit%20agents.md), [Pipecat](Trace%20Pipecat%20agents.md), or your own).

> [!NOTE]
>
> These conventions assume you are exporting traces to LangSmith through one of the supported [tracing setups](../../../../Overview/LangSmith%20Observability.md). For audio rendering and playback in the UI, see [Log multimodal traces](../../../Configuration%20%26%20troubleshooting/Advanced%20tracing%20techniques/Log%20multimodal%20traces.md) and [Upload files with traces](../../Manual%20instrumentation/Upload%20files%20with%20traces.md).

## Two architectures, two trace shapes

How you build a voice agent determines what the trace looks like. There are two common architectures, and they produce fundamentally different traces.

### Cascade

A cascade chains together separate, single-purpose models: speech-to-text (STT) transcribes the user's audio, a language model (LLM) reasons over the text and decides what to do, and text-to-speech (TTS) synthesizes the reply. Middleware, tool calls, and retrieval steps sit in between.

Because each stage is a discrete model call with a clear input and output, a cascade traces like any other agent pipeline. The trace is a tree of `STT`, `LLM`, `TTS`, tool, and middleware runs: stages can run in parallel, and a new STT → LLM → TTS cycle repeats for each turn of the conversation. These runs have meaningful input/output pairs (audio in → transcript out, prompt in → completion out).

The two most common frameworks for building cascade voice agents are [LiveKit](Trace%20LiveKit%20agents.md) and [Pipecat](Trace%20Pipecat%20agents.md).

### Speech-to-speech (S2S)

A speech-to-speech model (such as the [OpenAI Realtime API](Trace%20OpenAI%20Realtime%20agents.md) or [Gemini Live](Trace%20Gemini%20Live%20agents.md)) processes audio natively and replies with audio over a single persistent connection, typically a WebSocket. There is no STT/LLM/TTS decomposition to trace.

Instead, the model server and your client exchange a stream of **events** over the wire: audio chunks, transcription fragments, tool-call requests, turn boundaries, interruptions, and errors. The natural unit to trace is the **event payload**, not a request/response pair. Each event you record becomes one span whose content is the payload that crossed the wire.

The rest of this page describes conventions that apply to both architectures. The provider guides cover the event-stream specifics for [OpenAI Realtime](Trace%20OpenAI%20Realtime%20agents.md) and [Gemini Live](Trace%20Gemini%20Live%20agents.md).

## Core conventions

These are the practices we recommend for getting the most out of voice traces in LangSmith. You should trace your voice applications however best suits your infrastructure and implementations, but following the structure we suggest here will help to make your traces consistent and easy to debug and evaluate.

We recommend three high-level conventions:

1. [**Trace each conversation as a single trace**](#trace-each-conversation-as-a-single-trace) instead of splitting it into multiple traces.
2. [**Record a single combined audio file**](#record-a-single-combined-audio-file) and attach it to the root run.
3. [**Mark the trace as audio**](#mark-the-trace-as-audio) with `ls_modality` so it renders and filters as a voice trace.

### Trace each conversation as a single trace

A conversation is a single interaction, so we recommend keeping it in a single trace, with the individual model calls or events nested underneath one root run that represents the whole conversation.

Do not split a conversation into multiple traces. If you start a new trace for each exchange, you lose the information that lives **between** exchanges:

* **Interruptions**: when the user talks over the agent and the agent stops (barge-in).
* **Timing and latency**: gaps between speakers, and how long the agent took to respond.
* **Context**: references back to earlier parts of the conversation.
* **Conversation-level outcomes**: whether the user's goal was ultimately resolved.

What hangs under the root run depends on your [architecture](#two-architectures-two-trace-shapes). For a [cascade](#cascade), the children are the model calls and middleware:

```text
conversation                      ← root run (whole conversation; combined audio; ls_modality="audio")
│
├─ stt                            ← a transcription call
├─ llm                            ← a model call (may include middleware and tool runs)
├─ tts                            ← a synthesis call
└─ ...                            ← the pattern repeats as the conversation continues
```

For a [speech-to-speech](#speech-to-speech-s2s) agent, the children are the **events** that crossed the socket:

```text
conversation                      ← root run (whole conversation; combined audio; ls_modality="audio")
│
├─ input_transcription            ← a fragment of the user's speech transcript
├─ output_transcription           ← a fragment of the agent's speech transcript
├─ function_call: get_weather     ← the model requested a tool
├─ function_response: get_weather ← the tool result heading back to the model
├─ turn_complete                  ← a turn boundary reported by the server
└─ interrupted                    ← the server detected user barge-in
```

> [!NOTE]
>
> A voice agent has no reliable notion of a "turn". Speakers overlap, interrupt, and trail off. Do not group runs into synthetic turns. Trace the real units instead: the model calls in a cascade, or the event payloads in a speech-to-speech stream.

For background on grouping related runs, see [Nest traces](../../../Configuration%20%26%20troubleshooting/Troubleshooting%20guides/Troubleshoot%20trace%20nesting.md). To group several separate sessions for one user, use [Threads](../../../../Debug/Configure%20threads.md).

### Record a single combined audio file

Attach **one** audio file to the root run that contains **both** the user and the agent, recorded from **what was actually played to the client**, not the audio the model generated.

Record at the client. A common approach is a stereo WAV with the user's microphone on one channel and the agent's speech, captured at the speaker, on the other. This matters because the generated audio and the heard audio are not the same thing: network delay, dropped or reordered packets, and barge-in all change what the user actually experiences. A barge-in that cuts the agent off mid-sentence should appear truncated in the recording, because that is what happened. Recording what was played, rather than what was generated but possibly never heard, is what makes the trace faithful to the real interaction.

Attach the file using the [attachments API](../../Manual%20instrumentation/Upload%20files%20with%20traces.md):

```python Python
from langsmith import traceable
from langsmith.schemas import Attachment

@traceable(name="conversation", metadata={"ls_modality": "audio"})
def run_conversation(session_id: str, conversation_audio: bytes):
    # conversation_audio: a single recording of what was played to the client
    # (e.g. stereo WAV: user mic on L, agent speech at the speaker on R)
    ...
    return {"conversation": Attachment(mime_type="audio/wav", data=conversation_audio)}
```

> [!TIP]
>
> Audio files can be large. For high-volume production workloads, consider downsampling, using a compressed format (such as MP3 or Opus), or sampling which conversations you record in full.

### Mark the trace as audio

Set the `ls_modality` metadata field to `"audio"` on the root run. This flags the trace as a voice trace so LangSmith can render it appropriately and so you can [filter](../../../../Debug/Viewing%20%26%20managing%20traces/Filter%20traces.md) for voice traces in your project.

```python Python
from langsmith import traceable

@traceable(
    name="conversation",
    metadata={"ls_modality": "audio"},
)
def run_conversation(session_id: str):
    ...
```

> [!NOTE]
>
> For other `ls_` metadata fields, refer to [Metadata parameters reference](../../Manual%20instrumentation/Metadata%20parameters%20reference.md).

## Next steps

> [card] [Trace OpenAI Realtime](Trace%20OpenAI%20Realtime%20agents.md)
>
> Trace voice agents built on the OpenAI Realtime API.

> [card] [Trace Gemini Live](Trace%20Gemini%20Live%20agents.md)
>
> Trace voice agents built on the Gemini Live API.

> [card] [Trace LiveKit](Trace%20LiveKit%20agents.md)
>
> Trace voice agents built with LiveKit Agents.

> [card] [Trace Pipecat](Trace%20Pipecat%20agents.md)
>
> Trace voice agents built with Pipecat.

> [card] [Upload files with traces](../../Manual%20instrumentation/Upload%20files%20with%20traces.md)
>
> Attach the conversation audio recording to your trace.

> [card] [Log multimodal traces](../../../Configuration%20%26%20troubleshooting/Advanced%20tracing%20techniques/Log%20multimodal%20traces.md)
>
> Render audio and other media in the LangSmith UI.
