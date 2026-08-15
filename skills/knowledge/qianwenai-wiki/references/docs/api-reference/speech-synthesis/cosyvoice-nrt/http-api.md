> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 非实时语音合成 Qwen-Audio-TTS/CosyVoice HTTP API

> Qwen-Audio-TTS/CosyVoice 非实时语音合成 HTTP API 参考，支持非流式和流式（SSE）两种调用模式。

本文介绍非实时语音合成 Qwen-Audio-TTS/CosyVoice 的 HTTP 调用方法，支持非流式和流式两种调用模式。

**用户指南**：参见[非实时语音合成](/developer-guides/speech/tts)。

<Warning>
  该功能仅支持非实时调用，不支持 WebSocket 实时流式调用。如需实时合成，请使用 [CosyVoice WebSocket API](/api-reference/speech-synthesis/cosyvoice/websocket-api)。
</Warning>

## 请求端点

```
POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer
```

## 请求头

| 参数              | 类型     | 是否必选 | 说明                                   |
| --------------- | ------ | ---- | ------------------------------------ |
| Authorization   | string | 必选   | 鉴权令牌，格式为 `Bearer $DASHSCOPE_API_KEY` |
| Content-Type    | string | 必选   | 请求体的媒体类型，固定为 `application/json`      |
| X-DashScope-SSE | string | 可选   | 设置为 `enable` 时开启 SSE 流式输出            |

## 请求体

### 顶层字段

| 参数    | 类型     | 是否必选 | 说明                                                                                                                                                                   |
| ----- | ------ | ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| model | string | 必选   | 语音合成模型。可选值：`qwen-audio-3.0-tts-plus`、`qwen-audio-3.0-tts-flash`、`cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`、`cosyvoice-v3-plus`、`cosyvoice-v3-flash`、`cosyvoice-v2` |
| input | object | 必选   | 输入参数对象，详见 [input 参数](#input-参数)                                                                                                                                      |

### input 参数

| 参数                       | 类型             | 是否必选 | 说明                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------------ | -------------- | ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| text                     | string         | 必选   | 待合成文本。支持 [SSML](/developer-guides/speech/ssml) 和 [LaTeX](/developer-guides/speech/ssml#latex-公式转语音) 格式输入。使用 SSML 时需同时将 `enable_ssml` 设置为 `true`；使用 LaTeX 时无需额外配置                                                                                                                                                                                                                 |
| voice                    | string         | 必选   | 音色。可选值：系统音色（参见[Qwen-Audio-TTS音色列表](/api-reference/speech-synthesis/qwen-audio-tts/voice-list)、[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)）、声音复刻音色、声音设计音色（创建方法参见 [CosyVoice 声音复刻/设计 API](/api-reference/speech-synthesis/voice-cloning/create-voice)）                                                                                                   |
| format                   | string         | 可选   | 音频编码格式。默认值：`mp3`。可选值：`mp3`、`pcm`、`wav`、`opus`                                                                                                                                                                                                                                                                                                                                    |
| sample\_rate             | integer        | 可选   | 音频采样率（单位：Hz）。默认值：`22050`。可选值：8000、16000、22050、24000、44100、48000                                                                                                                                                                                                                                                                                                                  |
| volume                   | integer        | 可选   | 音量。默认值：`50`。取值范围：\[0, 100]                                                                                                                                                                                                                                                                                                                                                       |
| rate                     | float          | 可选   | 语速。默认值：`1.0`。取值范围：\[0.5, 2.0]                                                                                                                                                                                                                                                                                                                                                    |
| bit\_rate                | integer        | 可选   | 音频码率（单位：kbps）。默认值：`32`。取值范围：\[6, 510]。仅在 `format` 为 `opus` 时支持                                                                                                                                                                                                                                                                                                                   |
| pitch                    | float          | 可选   | 音调。默认值：`1.0`。取值范围：\[0.5, 2.0]                                                                                                                                                                                                                                                                                                                                                    |
| enable\_ssml             | boolean        | 可选   | 是否开启 SSML 功能。当 `text` 使用 SSML 格式时需设为 `true`。仅 CosyVoice 系列模型支持，qwen-audio-3.0-tts-plus 和 qwen-audio-3.0-tts-flash 不支持                                                                                                                                                                                                                                                            |
| word\_timestamp\_enabled | boolean        | 可选   | 是否开启字级别时间戳。默认值：`false`。仅在流式输出模式下可用。支持的音色范围：cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash、cosyvoice-v3-plus和cosyvoice-v2模型的复刻音色，以及[Qwen-Audio-TTS音色列表](/api-reference/speech-synthesis/qwen-audio-tts/voice-list)、[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)中标记为支持的系统音色。qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash及其他模型的复刻音色不支持此功能 |
| seed                     | integer        | 可选   | 随机数种子，用于复现相同合成结果。默认值：`0`。取值范围：\[0, 65535]                                                                                                                                                                                                                                                                                                                                        |
| language\_hints          | array\[string] | 可选   | 指定语音合成的目标语言，提升合成效果。可选值：`zh`、`en`、`fr`、`de`、`ja`、`ko`、`ru`、`pt`、`th`、`id`、`vi`、`es`、`it`、`ms`、`fil`、`ar`。当前版本仅处理第一个元素，建议只传入一个值                                                                                                                                                                                                                                                    |
| instruction              | string         | 可选   | 设置指令，用于控制方言、情感或角色等合成效果。具体用法请参见[非实时语音合成](/developer-guides/speech/tts)                                                                                                                                                                                                                                                                                                            |
| enable\_aigc\_tag        | boolean        | 可选   | 是否在生成的音频中添加 AIGC 隐性标识。设置为 `true` 时，将隐性标识嵌入到支持格式（wav/mp3/opus）的音频中。默认值：`false`。仅 qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2 支持                                                                                                                                                                                            |
| aigc\_propagator         | string         | 可选   | 设置 AIGC 隐性标识中的 `ContentPropagator` 字段，用于标识内容传播者。仅在 `enable_aigc_tag` 为 `true` 时生效。默认值：阿里云 UID                                                                                                                                                                                                                                                                                    |
| aigc\_propagate\_id      | string         | 可选   | 设置 AIGC 隐性标识中的 `PropagateID` 字段，用于唯一标识一次具体的传播行为。仅在 `enable_aigc_tag` 为 `true` 时生效。默认值：本次请求的 Request ID                                                                                                                                                                                                                                                                           |
| hot\_fix                 | object         | 可选   | 文本热修复配置，用于自定义指定词语的发音或对待合成文本进行替换。qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、cosyvoice-v2 不支持该功能。详见 [hot\_fix 参数](#hot_fix-参数)                                                                                                                                                                                                                                               |
| enable\_markdown\_filter | boolean        | 可选   | 是否启用 Markdown 过滤。启用后，系统在合成语音前自动过滤输入文本中的 Markdown 标记符号。默认值：`false`。仅 cosyvoice-v3-flash 复刻音色支持                                                                                                                                                                                                                                                                                    |

<a id="hot_fix-参数" />

### hot\_fix 参数

| 参数            | 类型             | 说明                                                            |
| ------------- | -------------- | ------------------------------------------------------------- |
| pronunciation | array\[object] | 自定义发音。指定词语的拼音标注，用于纠正默认发音不准确的情况。格式：`[{"词语": "pin1 yin1"}]`     |
| replace       | array\[object] | 文本替换。在语音合成前将指定词语替换为目标文本，替换后的文本将作为实际合成内容。格式：`[{"原文": "替换文本"}]` |

示例：

```json
{
  "hot_fix": {
    "pronunciation": [
      {"天气": "tian1 qi4"}
    ],
    "replace": [
      {"今天": "金天"}
    ]
  }
}
```

## 请求示例

<CodeGroup>
  ```bash 非流式
  curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen-audio-3.0-tts-flash",
    "input": {
      "text": "我家的后面有一个很大的花园。",
      "voice": "longanhuan_v3.6",
      "format": "wav",
      "sample_rate": 24000
    }
  }'
  ```

  ```bash 流式（SSE）
  curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-DashScope-SSE: enable" \
  -d '{
    "model": "qwen-audio-3.0-tts-flash",
    "input": {
      "text": "我家的后面有一个很大的花园。",
      "voice": "longanhuan_v3.6",
      "format": "wav",
      "sample_rate": 24000
    }
  }'
  ```
</CodeGroup>

## 响应体

### 顶层字段

| 参数          | 类型     | 说明                                 |
| ----------- | ------ | ---------------------------------- |
| request\_id | string | 本次调用的唯一标识符                         |
| output      | object | 模型返回的数据，详见 [output 字段](#output-字段) |
| usage       | object | 用量信息，详见 [usage 字段](#usage-字段)      |

### output 字段

| 参数             | 类型     | 说明                                                                                  |
| -------------- | ------ | ----------------------------------------------------------------------------------- |
| finish\_reason | string | 任务停止原因。`"null"`=语音合成中；`"stop"`=语音合成结束                                               |
| type           | string | 子事件类型，仅流式合成时返回。`sentence-begin`=句子开始；`sentence-synthesis`=音频数据块；`sentence-end`=句子结束 |
| original\_text | string | 对用户输入文本进行分句后的句内容                                                                    |
| sentence       | object | 句子信息，详见 [sentence 字段](#sentence-字段)                                                 |
| audio          | object | 合成的音频数据，详见 [audio 字段](#audio-字段)                                                    |

### sentence 字段

| 参数    | 类型      | 说明                                  |
| ----- | ------- | ----------------------------------- |
| index | integer | 句子的编号，从 0 开始                        |
| words | array   | 每句话对应的字的信息，详见 [words 字段](#words-字段) |

### words 字段

| 参数           | 类型      | 说明                  |
| ------------ | ------- | ------------------- |
| text         | string  | 字                   |
| begin\_index | integer | 字在句子中的开始位置索引，从 0 开始 |
| end\_index   | integer | 字在句子中的结束位置索引，从 1 开始 |
| begin\_time  | integer | 字对应音频的开始时间戳（毫秒）     |
| end\_time    | integer | 字对应音频的结束时间戳（毫秒）     |

### audio 字段

| 参数          | 类型      | 说明                             |
| ----------- | ------- | ------------------------------ |
| data        | string  | 流式合成时输出 Base64 格式音频数据；非流式合成时为空 |
| url         | string  | 模型输出的完整音频文件的 URL，有效期 24 小时     |
| id          | string  | 模型输出的音频信息对应的 ID                |
| expires\_at | integer | `url` 过期的 Unix 时间戳（秒）          |

### usage 字段

| 参数         | 类型      | 说明            |
| ---------- | ------- | ------------- |
| characters | integer | 本次请求中计费的有效字符数 |

## 响应示例

<CodeGroup>
  ```json 非流式
  {
    "request_id": "ee88b03d-0457-9286-8c67-xxxxxxxxxxxx",
    "output": {
      "finish_reason": "stop",
      "audio": {
        "data": "",
        "url": "http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/pre/cosyvoice-v3-flash/20260304/xxxxxxxx/ee88b03d-0457-9286-8c67-xxxxxxxxxxxx.wav?xxxxxxx",
        "id": "audio_ee88b03d-0457-9286-8c67-xxxxxxxxxxxx",
        "expires_at": 1772697707
      }
    },
    "usage": {
      "characters": 15
    }
  }
  ```

  ```json 流式（SSE）中间结果
  {
    "request_id": "8ac1cd04-06af-9a63-b031-xxxxxxxxxxxx",
    "output": {
      "finish_reason": "null",
      "type": "sentence-begin",
      "original_text": "我家的后面有一个很大的花园。",
      "sentence": {
        "index": 0,
        "words": []
      },
      "audio": {
        "data": "",
        "id": "audio_ee88b03d-0457-9286-8c67-xxxxxxxxxxxx",
        "expires_at": 1772697707
      }
    },
    "usage": {
      "characters": 15
    }
  }
  ```

  ```json 流式（SSE）最终结果
  {
    "request_id": "8ac1cd04-06af-9a63-b031-xxxxxxxxxxxx",
    "output": {
      "finish_reason": "stop",
      "audio": {
        "data": "",
        "url": "http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/pre/cosyvoice-v3-flash/20260304/xxxxxxxx/8ac1cd04-06af-9a63-b031-xxxxxxxxxxxx.wav?xxxxxxx",
        "id": "audio_8ac1cd04-06af-9a63-b031-xxxxxxxxxxxx",
        "expires_at": 1772698611
      }
    },
    "usage": {
      "characters": 15
    }
  }
  ```
</CodeGroup>
