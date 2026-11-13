# MiniMax T2A v2

一次调用同步返回完整音频；`stream:true` 时按 SSE 分帧推送增量音频。

### 非流式调用

:::group

```bash title="cURL"
curl https://tokendance.space/gateway/minimax/v1/t2a_v2 \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "text": "今天是不是很开心呀，当然了！",
    "voice_setting": {
      "voice_id": "male-qn-qingse",
      "speed": 1,
      "vol": 1,
      "pitch": 0
    },
    "audio_setting": {
      "sample_rate": 32000,
      "bitrate": 128000,
      "format": "mp3",
      "channel": 1
    }
  }'
```

```python title="Python"
import requests

resp = requests.post(
    "https://tokendance.space/gateway/minimax/v1/t2a_v2",
    headers={"Authorization": "Bearer YOUR_KEY"},
    json={
        "model": "MODEL_ID",
        "text": "今天是不是很开心呀，当然了！",
        "voice_setting": {"voice_id": "male-qn-qingse", "speed": 1, "vol": 1, "pitch": 0},
        "audio_setting": {"sample_rate": 32000, "bitrate": 128000, "format": "mp3", "channel": 1},
    },
)
data = resp.json()

# data.audio 默认是 hex 编码的二进制音频，写文件即可播放
with open("out.mp3", "wb") as f:
    f.write(bytes.fromhex(data["data"]["audio"]))
print("usage_characters:", data["extra_info"]["usage_characters"])
```

```javascript title="Node.js"
import { writeFileSync } from "node:fs";

const resp = await fetch("https://tokendance.space/gateway/minimax/v1/t2a_v2", {
  method: "POST",
  headers: {
    "Authorization": "Bearer YOUR_KEY",
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    model: "MODEL_ID",
    text: "今天是不是很开心呀，当然了！",
    voice_setting: { voice_id: "male-qn-qingse", speed: 1, vol: 1, pitch: 0 },
    audio_setting: { sample_rate: 32000, bitrate: 128000, format: "mp3", channel: 1 },
  }),
});
const data = await resp.json();
writeFileSync("out.mp3", Buffer.from(data.data.audio, "hex"));
console.log("usage_characters:", data.extra_info.usage_characters);
```

:::

### 流式调用

把请求体里的 `stream` 改为 `true`，响应即变为 SSE。每个事件是一段独立 JSON：

- `data.status == 1` → 中间增量帧（含本段 hex 音频）
- `data.status == 2` → 终态帧（含完整音频与 `extra_info.usage_characters`）
- `base_resp.status_code != 0` → 错误帧

```bash title="流式 cURL"
curl -N https://tokendance.space/gateway/minimax/v1/t2a_v2 \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "text": "今天天气真好",
    "stream": true,
    "voice_setting": {"voice_id": "male-qn-qingse", "speed": 1, "vol": 1, "pitch": 0},
    "audio_setting": {"sample_rate": 32000, "bitrate": 128000, "format": "mp3", "channel": 1}
  }'
```

### 文本特殊语法

::: tip
`text` 字段支持几种行内控制语法，混合使用可以做出更自然的语音：

- 停顿：`<#x#>` 其中 x 为秒数（0.01–99.99，最多两位小数），不能连续出现
- 行内发音替换：英文小括号包拼音 / IPA / 粤拼，例 `(he2)平`、`The word live is pronounced (lɪv)`
- 语气词标签（仅 `speech-2.8-*` 模型）：`(laughs) (chuckle) (coughs) (sighs)` 等
:::

### 输出格式选项

- `audio_setting.format`：`mp3` / `wav` / `flac`
- `output_format`：默认 `hex`；改为 `url` 时返回 24h 有效的下载链接（仅非流式）
- `subtitle_enable: true` 可同时返回字幕，`subtitle_type` 选 `sentence` / `word` / `word_streaming`

更多参数与字段说明请参考 [上游官方文档](https://platform.minimaxi.com/docs/api-reference/speech-t2a-http)。
