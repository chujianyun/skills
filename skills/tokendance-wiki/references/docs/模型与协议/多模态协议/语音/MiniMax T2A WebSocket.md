# MiniMax T2A WebSocket

WebSocket 双向流式文本转语音：客户端按段发 `task_continue`，模型边收边合成边推音频，适合长文本与低延迟场景。一次连接 = 一次任务。

### Python

```python
import asyncio
import json
import websockets

async def main():
    url = "wss://tokendance.space/gateway/minimax/v1/t2a_v2_ws"
    headers = [("Authorization", "Bearer YOUR_KEY")]

    async with websockets.connect(url, additional_headers=headers) as ws:
        # 1. 发 task_start（首帧）
        await ws.send(json.dumps({
            "event": "task_start",
            "model": "MODEL_ID",
            "voice_setting": {"voice_id": "male-qn-qingse", "speed": 1.0, "vol": 5.0, "pitch": 0},
            "audio_setting": {"sample_rate": 32000, "bitrate": 128000, "format": "mp3", "channel": 1},
            "language_boost": "auto",
        }))
        print("recv:", await ws.recv())  # connected_success
        print("recv:", await ws.recv())  # task_started

        # 2. 发 task_continue，循环读 task_continued 直到 is_final=true
        await ws.send(json.dumps({"event": "task_continue", "text": "今天天气真好。"}))
        total_chars = 0
        while True:
            msg = json.loads(await ws.recv())
            if msg.get("event") == "task_failed":
                print("failed:", msg["base_resp"]); return
            ei = msg.get("extra_info") or {}
            total_chars += ei.get("usage_characters", 0)
            if msg.get("is_final"):
                break

        # 3. 发 task_finish，等 task_finished
        await ws.send(json.dumps({"event": "task_finish"}))
        print("recv:", await ws.recv())  # task_finished
        print(f"usage_characters: {total_chars}")

asyncio.run(main())
```

### Node.js

```javascript
import WebSocket from "ws";

const ws = new WebSocket("wss://tokendance.space/gateway/minimax/v1/t2a_v2_ws", {
  headers: { Authorization: "Bearer YOUR_KEY" },
});

ws.on("open", () => {
  ws.send(JSON.stringify({
    event: "task_start",
    model: "MODEL_ID",
    voice_setting: { voice_id: "male-qn-qingse", speed: 1.0, vol: 5.0, pitch: 0 },
    audio_setting: { sample_rate: 32000, bitrate: 128000, format: "mp3", channel: 1 },
    language_boost: "auto",
  }));
});

let totalChars = 0;
ws.on("message", async (raw) => {
  const msg = JSON.parse(raw.toString());
  if (msg.event === "task_started") {
    ws.send(JSON.stringify({ event: "task_continue", text: "今天天气真好。" }));
  } else if (msg.event === "task_continued") {
    totalChars += msg.extra_info?.usage_characters ?? 0;
    if (msg.is_final) ws.send(JSON.stringify({ event: "task_finish" }));
  } else if (msg.event === "task_finished") {
    console.log("usage_characters:", totalChars);
    ws.close();
  } else if (msg.event === "task_failed") {
    console.error("failed:", msg.base_resp);
    ws.close();
  }
});
```

### wscat（手动调试）

```bash
wscat -c "wss://tokendance.space/gateway/minimax/v1/t2a_v2_ws" \
  -H "Authorization: Bearer YOUR_KEY"
# 连上后手动粘贴 JSON 帧：
> {"event":"task_start","model":"MODEL_ID","voice_setting":{"voice_id":"male-qn-qingse","speed":1.0,"vol":5.0,"pitch":0},"audio_setting":{"sample_rate":32000,"bitrate":128000,"format":"mp3","channel":1}}
> {"event":"task_continue","text":"今天天气真好。"}
> {"event":"task_finish"}
```

更多参数（`timbre_weights` / `pronunciation_dict` / `subtitle_enable` 等）见 [上游官方文档](https://platform.minimaxi.com/docs/api-reference/speech-t2a-websocket)。
