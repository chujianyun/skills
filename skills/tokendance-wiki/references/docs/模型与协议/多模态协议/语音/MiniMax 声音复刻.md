# MiniMax 声音复刻

只需要先通过minimax专属的文件上传接口，上传一段参考音频，就能复刻成可复用的自定义 `voice_id`，之后进行语音合成时即可引用该音色。

### 步骤 1：上传参考音频

参考音频需满足以下要求（详见 [MiniMax 官方文档](https://platform.minimaxi.com/docs/api-reference/file-management-upload)）：

- 时长 ≥ 10 秒，建议 30 秒左右
- 格式：mp3 / wav / m4a / flac / aac 等
- 单声道、采样率 ≥ 16kHz、清晰人声、低背景噪声

:::group

```bash title="cURL"
curl https://tokendance.space/gateway/minimax/v1/files/upload \
  -H "Authorization: Bearer YOUR_KEY" \
  -F "purpose=voice_clone" \
  -F "file=@sample.mp3"
```

```python title="Python"
import requests

resp = requests.post(
    "https://tokendance.space/gateway/minimax/v1/files/upload",
    headers={
        "Authorization": "Bearer YOUR_KEY",
    },
    data={"purpose": "voice_clone"},
    files={"file": open("sample.mp3", "rb")},
)
file_id = resp.json()["file"]["file_id"]
print("file_id:", file_id)
```

```javascript title="Node.js"
import { readFileSync } from "node:fs";

const form = new FormData();
form.set("purpose", "voice_clone");
form.set("file", new Blob([readFileSync("sample.mp3")]), "sample.mp3");

const resp = await fetch("https://tokendance.space/gateway/minimax/v1/files/upload", {
  method: "POST",
  headers: {
    Authorization: "Bearer YOUR_KEY",
  },
  body: form,
});
const { file } = await resp.json();
console.log("file_id:", file.file_id);
```

:::

网关会把文件广播到全部可用的 MiniMax 上游，并返回统一的本地 `file_id`；
后续语音克隆无论路由到哪个上游都能解析该文件。

返回示例：

```json
{
  "file": { "file_id": "01JABCDEFGHJKMNPQRSTVWXYZ0", "bytes": 125120, "created_at": 1781702203, "filename": "sample.mp3", "purpose": "voice_clone" },
  "base_resp": { "status_code": 0, "status_msg": "success" }
}
```

音频文件上传不产生计费。

### 步骤 2：注册自定义音色

使用上一步拿到的 `file_id` 进行注册，指定 `voice_id`（自定义命名）、`model` 以及一段用于试听的 `text`：

:::group

```bash title="cURL"
curl https://tokendance.space/gateway/minimax/v1/voice_clone \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "file_id": "01JABCDEFGHJKMNPQRSTVWXYZ0",
    "voice_id": "my-voice-9f3a",
    "text": "你好，这是我克隆的音色。"
  }'
```

```python title="Python"
import requests

resp = requests.post(
    "https://tokendance.space/gateway/minimax/v1/voice_clone",
    headers={
        "Authorization": "Bearer YOUR_KEY",
        "Content-Type": "application/json",
    },
    json={
        "model": "MODEL_ID",
        "file_id": "01JABCDEFGHJKMNPQRSTVWXYZ0",
        "voice_id": "my-voice-9f3a",
        "text": "你好，这是我克隆的音色。",
    },
)
data = resp.json()
print("demo_audio:", data["demo_audio"])
print("usage_characters:", data["extra_info"]["usage_characters"])
```

```javascript title="Node.js"
const resp = await fetch("https://tokendance.space/gateway/minimax/v1/voice_clone", {
  method: "POST",
  headers: {
    Authorization: "Bearer YOUR_KEY",
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    model: "MODEL_ID",
    file_id: "01JABCDEFGHJKMNPQRSTVWXYZ0",
    voice_id: "my-voice-9f3a",
    text: "你好，这是我克隆的音色。",
  }),
});
const data = await resp.json();
console.log("demo_audio:", data.demo_audio);
console.log("usage_characters:", data.extra_info.usage_characters);
```

:::

返回示例：

```json
{
  "demo_audio": "https://.../demo.mp3",
  "extra_info": { "audio_length": 3672, "usage_characters": 35, "word_count": 19 },
  "base_resp": { "status_code": 0, "status_msg": "success" }
}
```

复刻成功后，`demo_audio` 是用新音色合成的试听音频链接，`extra_info.usage_characters` 是试听文本的字符数。

### 步骤 3：用自定义音色合成语音

复刻完成后，将 `voice_id` 作为 `voice_setting.voice_id` 传给语音合成接口即可使用该音色合成语音：

```bash title="cURL"
curl https://tokendance.space/gateway/minimax/v1/t2a_v2 \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "text": "今天天气真好。",
    "voice_setting": { "voice_id": "my-voice-9f3a", "speed": 1, "vol": 1, "pitch": 0 },
    "audio_setting": { "sample_rate": 32000, "bitrate": 128000, "format": "mp3", "channel": 1 }
  }'
```

更多参数与字段说明请参考 MiniMax 官方文档：[files/upload](https://platform.minimaxi.com/docs/api-reference/file-management-upload) / [voice_clone](https://platform.minimaxi.com/docs/api-reference/voice-cloning-clone)。
