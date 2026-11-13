# Qwen-Audio-3.0-ASR-Flash-Streaming

用 WebSocket 分块发送示例 WAV 音频，逐句读取转写结果。`parameters.format` 必填，且必须与发送的音频格式一致；此文件是 32 kHz、单声道、PCM16 编码的 WAV。

### Python

```python
import asyncio
import json
import uuid
from urllib.request import urlopen

import websockets

URL = "wss://tokendance.space/gateway/alibaba/api-ws/v1/inference"
AUDIO_URL = "https://au-tokendance.tos-cn-shanghai.volces.com/example/audio.wav"

async def main():
    task_id = str(uuid.uuid4())
    async with websockets.connect(
        URL, additional_headers={"Authorization": "Bearer YOUR_KEY"}
    ) as ws:
        await ws.send(json.dumps({
            "header": {"action": "run-task", "task_id": task_id, "streaming": "duplex"},
            "payload": {"task_group": "audio", "task": "asr", "function": "recognition",
                        "model": "MODEL_ID", "parameters": {"format": "wav", "sample_rate": 32000},
                        "input": {}},
        }))
        started = json.loads(await ws.recv())
        if started["header"]["event"] != "task-started":
            raise RuntimeError(started)

        with urlopen(AUDIO_URL) as response:
            audio = response.read()
        for offset in range(0, len(audio), 6400):  # 约每块 100 ms
            await ws.send(audio[offset:offset + 6400])
            await asyncio.sleep(0.1)
        await ws.send(json.dumps({
            "header": {"action": "finish-task", "task_id": task_id, "streaming": "duplex"},
            "payload": {"input": {}},
        }))

        async for raw in ws:
            event = json.loads(raw)
            kind = event["header"]["event"]
            if kind == "result-generated":
                sentence = event["payload"]["output"]["sentence"]
                if sentence.get("sentence_end"):
                    print(sentence["text"])
            elif kind == "task-failed":
                raise RuntimeError(event["header"])
            elif kind == "task-finished":
                break

asyncio.run(main())
```

上游可能返回 `payload.usage.duration`（秒）及 `payload.usage.input_tokens`、`payload.usage.output_tokens`；实际计费项由端点价格配置决定。中间结果的 `usage` 可能为 `null`。
