# Qwen3-ASR-Flash-Realtime

用 WebSocket 分块发送 16 kHz、单声道、PCM16 音频，逐段读取转写结果。

### Python

```python
import asyncio
import base64
import json
import uuid

import websockets

URL = "wss://tokendance.space/gateway/alibaba/api-ws/v1/realtime?model=MODEL_ID"

async def main():
    async with websockets.connect(
        URL, additional_headers={"Authorization": "Bearer YOUR_KEY"}
    ) as ws:
        await ws.recv()  # session.created
        await ws.send(json.dumps({
            "type": "session.update", "event_id": uuid.uuid4().hex,
            "session": {"input_audio_format": "pcm", "sample_rate": 16000,
                        "modalities": ["text"], "turn_detection": None},
        }))
        await ws.recv()  # session.updated

        with open("audio.pcm", "rb") as audio:
            while chunk := audio.read(3200):  # 每块 100 ms
                await ws.send(json.dumps({
                    "type": "input_audio_buffer.append", "event_id": uuid.uuid4().hex,
                    "audio": base64.b64encode(chunk).decode(),
                }))
                await asyncio.sleep(0.1)
        await ws.send(json.dumps({"type": "input_audio_buffer.commit", "event_id": uuid.uuid4().hex}))
        await ws.send(json.dumps({"type": "session.finish", "event_id": uuid.uuid4().hex}))

        async for raw in ws:
            event = json.loads(raw)
            if event["type"] == "conversation.item.input_audio_transcription.completed":
                print(event["transcript"])
            elif event["type"] == "error":
                raise RuntimeError(event)
            elif event["type"] == "session.finished":
                break

asyncio.run(main())
```

`completed.usage.duration` 为该段音频的计费秒数。
