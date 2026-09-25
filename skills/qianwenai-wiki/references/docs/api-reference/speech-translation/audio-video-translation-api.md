> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 音视频翻译

> LiveTranslate API 参考

通过 OpenAI 兼容的 chat completions 端点翻译音视频内容，支持流式和非流式调用。

**用户指南**： 教程和完整示例请参见[音视频翻译](/developer-guides/speech/file-translation)。

<Note>
  不支持 DashScope 接口。
</Note>

## 端点

| SDK `base_url`                                      | HTTP 端点                                                                   |
| --------------------------------------------------- | ------------------------------------------------------------------------- |
| `https://dashscope.aliyuncs.com/compatible-mode/v1` | `POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions` |

## 请求体

### 必选参数

| 参数                    | 类型      | 说明                                                                                      |
| --------------------- | ------- | --------------------------------------------------------------------------------------- |
| `model`               | string  | 模型名称：`qwen3-livetranslate-flash` 或 `qwen3-livetranslate-flash-2025-12-01`。              |
| `messages`            | array   | 单条用户消息。参见 [Message 对象](#message-对象)。                                                    |
| `stream`              | boolean | 是否启用流式输出。设为 `true` 可实时获取翻译进度，设为 `false` 则集成更简单。                                         |
| `translation_options` | object  | 翻译设置。非标准 OpenAI 参数：Python SDK 中通过 `extra_body` 传入，Node.js/HTTP 中直接放在顶层。参见[翻译选项](#翻译选项)。 |

### 可选参数

| 参数               | 类型      | 默认值        | 说明                                                        |
| ---------------- | ------- | ---------- | --------------------------------------------------------- |
| `modalities`     | array   | `["text"]` | 输出模式。`["text", "audio"]` 表示同时输出文本和音频，`["text"]` 仅输出文本。    |
| `audio`          | object  | -          | 音频输出设置。`modalities` 包含 `"audio"` 时必填。参见[音频输出选项](#音频输出选项)。 |
| `stream_options` | object  | -          | 流式输出设置。参见[流式输出选项](#流式输出选项)。                               |
| `max_tokens`     | integer | 模型最大值      | 最大生成 token 数。超出则截断输出。                                     |
| `seed`           | integer | -          | 随机种子，用于生成可复现的输出。取值范围：`[0, 2^31-1]`。                       |

### 采样参数

建议保持默认值以获得最佳翻译效果。

| 参数                   | 类型      | 默认值      | 取值范围         | 说明                                                                                     |
| -------------------- | ------- | -------- | ------------ | -------------------------------------------------------------------------------------- |
| `temperature`        | float   | 0.000001 | \[0, 2)      | 控制输出多样性。                                                                               |
| `top_p`              | float   | 0.8      | (0, 1.0]     | 核采样阈值。                                                                                 |
| `presence_penalty`   | float   | 0        | \[-2.0, 2.0] | 正值时减少重复。                                                                               |
| `top_k`              | integer | 1        | >= 0         | 候选集大小。为 `None` 或大于 100 时禁用（由 `top_p` 生效）。非标准 OpenAI 参数：Python SDK 中通过 `extra_body` 传入。 |
| `repetition_penalty` | float   | 1.05     | > 0          | 惩罚重复序列。非标准 OpenAI 参数：Python SDK 中通过 `extra_body` 传入。                                   |

### Message 对象

`messages` 数组必须且只能包含一条用户消息。

**`content` 数组元素**：

| 字段            | 类型     | 必选                         | 说明                                     |
| ------------- | ------ | -------------------------- | -------------------------------------- |
| `type`        | string | 是                          | 音频输入为 `input_audio`，视频输入为 `video_url`。 |
| `input_audio` | object | `type` 为 `input_audio` 时必填 | 音频输入。见下文。                              |
| `video_url`   | object | `type` 为 `video_url` 时必填   | 视频输入。见下文。                              |

**`input_audio` 对象**：

| 字段       | 类型     | 必选 | 说明                                                                                                                  |
| -------- | ------ | -- | ------------------------------------------------------------------------------------------------------------------- |
| `data`   | string | 是  | 音频文件 URL 或 Base64 data URL。本地文件请参见[发送 Base64 编码的本地文件](/developer-guides/speech/file-translation#发送-base64-编码的本地文件)。 |
| `format` | string | 是  | 音频格式，如 `mp3` 或 `wav`。                                                                                               |

**`video_url` 对象**：

| 字段    | 类型     | 必选 | 说明                                                                                                                      |
| ----- | ------ | -- | ----------------------------------------------------------------------------------------------------------------------- |
| `url` | string | 是  | 公开可访问的视频 URL 或 Base64 data URL。本地文件请参见[发送 Base64 编码的本地文件](/developer-guides/speech/file-translation#发送-base64-编码的本地文件)。 |

### 翻译选项

| 字段            | 类型     | 必选 | 说明                                                                               |
| ------------- | ------ | -- | -------------------------------------------------------------------------------- |
| `source_lang` | string | 否  | 源语言（语言代码）。参见[支持的语言](/developer-guides/speech/file-translation#支持的语言)。省略时由模型自动检测。 |
| `target_lang` | string | 是  | 目标语言（语言代码）。参见[支持的语言](/developer-guides/speech/file-translation#支持的语言)。           |

```python
extra_body={"translation_options": {"source_lang": "zh", "target_lang": "en"}}
```

### 音频输出选项

`modalities` 为 `["text", "audio"]` 时必填。

| 字段            | 类型     | 必选 | 说明                                                          |
| ------------- | ------ | -- | ----------------------------------------------------------- |
| `voice`       | string | 是  | 输出语音。                                                       |
| `format`      | string | 是  | 输出音频格式。仅支持 `wav`。                                           |
| `speech_rate` | float  | 否  | 控制输出音频的语速。默认值为1.0，即正常语速。小于1.0为慢速，大于1.0为快速。取值范围：\[0.5, 2.0]。 |

### 流式输出选项

| 字段              | 类型      | 默认值     | 说明                                    |
| --------------- | ------- | ------- | ------------------------------------- |
| `include_usage` | boolean | `false` | 设为 `true` 时，最后一个 chunk 包含 token 用量详情。 |

## 响应

API 以流式方式返回 `chat.completion.chunk` 对象，分为三类：文本、音频和 token 用量。

### 文本 chunk

在 `choices[0].delta.content` 中包含增量翻译文本：

```json
{
  "id": "chatcmpl-c22a54b8-40cc-4a1d-988b-f84cdf86868f",
  "choices": [
    {
      "delta": {
        "content": " of",
        "role": null,
        "audio": null
      },
      "finish_reason": null,
      "index": 0
    }
  ],
  "created": 1764755440,
  "model": "qwen3-livetranslate-flash",
  "object": "chat.completion.chunk"
}
```

### 音频 chunk

在 `choices[0].delta.audio.data` 中包含增量 Base64 编码的音频数据：

```json
{
  "id": "chatcmpl-c22a54b8-40cc-4a1d-988b-f84cdf86868f",
  "choices": [
    {
      "delta": {
        "content": null,
        "role": null,
        "audio": {
          "data": "///+//7////+////////////AAAAAAAAAAABA......",
          "expires_at": 1764755440,
          "id": "audio_c22a54b8-40cc-4a1d-988b-f84cdf86868f"
        }
      },
      "finish_reason": null,
      "index": 0
    }
  ],
  "created": 1764755440,
  "model": "qwen3-livetranslate-flash",
  "object": "chat.completion.chunk"
}
```

### Token 用量 chunk

`include_usage` 为 `true` 时最后发送。`choices` 数组为空，`usage` 包含 token 分项详情：

```json
{
  "id": "chatcmpl-c22a54b8-40cc-4a1d-988b-f84cdf86868f",
  "choices": [],
  "created": 1764755440,
  "model": "qwen3-livetranslate-flash",
  "object": "chat.completion.chunk",
  "usage": {
    "completion_tokens": 242,
    "prompt_tokens": 415,
    "total_tokens": 657,
    "completion_tokens_details": {
      "accepted_prediction_tokens": null,
      "audio_tokens": 191,
      "reasoning_tokens": null,
      "rejected_prediction_tokens": null,
      "text_tokens": 51
    },
    "prompt_tokens_details": {
      "audio_tokens": 415,
      "cached_tokens": null,
      "text_tokens": 0,
      "video_tokens": null
    }
  }
}
```

<Note>
  视频输入时，`prompt_tokens_details.audio_tokens` 包含视频中的音频 token。`video_tokens` 报告视频专属的 token 数量。
</Note>

### 响应字段

| 字段                                             | 类型      | 说明                                                     |
| ---------------------------------------------- | ------- | ------------------------------------------------------ |
| `id`                                           | string  | 请求标识符。所有 chunk 共享同一 ID。                                |
| `choices`                                      | array   | 生成内容。在最后的用量 chunk 中为空。                                 |
| `choices[].delta.content`                      | string  | 增量翻译文本。音频 chunk 中为 `null`。                             |
| `choices[].delta.audio`                        | object  | 增量音频数据。文本 chunk 中为 `null`。                             |
| `choices[].delta.audio.data`                   | string  | Base64 编码的音频片段。                                        |
| `choices[].delta.audio.id`                     | string  | 输出音频标识符。                                               |
| `choices[].delta.audio.expires_at`             | integer | 请求创建时的时间戳。                                             |
| `choices[].delta.role`                         | string  | 消息角色。仅在第一个 chunk 中出现。                                  |
| `choices[].finish_reason`                      | string  | 完成时为 `stop`，因 `max_tokens` 截断时为 `length`，进行中为 `null`。  |
| `choices[].index`                              | integer | 固定为 `0`。                                               |
| `created`                                      | integer | 请求的 Unix 时间戳。所有 chunk 共享同一值。                           |
| `model`                                        | string  | 使用的模型。                                                 |
| `object`                                       | string  | 固定为 `chat.completion.chunk`。                           |
| `usage`                                        | object  | Token 用量。仅在 `include_usage` 为 `true` 时出现在最后一个 chunk 中。 |
| `usage.prompt_tokens`                          | integer | 输入 token 总数。                                           |
| `usage.completion_tokens`                      | integer | 输出 token 总数。                                           |
| `usage.total_tokens`                           | integer | `prompt_tokens` 与 `completion_tokens` 之和。              |
| `usage.completion_tokens_details.audio_tokens` | integer | 输出音频 token 数。                                          |
| `usage.completion_tokens_details.text_tokens`  | integer | 输出文本 token 数。                                          |
| `usage.prompt_tokens_details.audio_tokens`     | integer | 输入音频 token 数。视频输入时包含视频中的音频 token。                      |
| `usage.prompt_tokens_details.text_tokens`      | integer | 输入文本 token 数。固定为 `0`。                                  |
| `usage.prompt_tokens_details.video_tokens`     | integer | 输入视频 token 数。仅视频输入时出现。                                 |

### 固定为 null 的字段

以下字段为兼容 OpenAI 格式而存在，始终返回 `null`：

`reasoning_content`、`function_call`、`refusal`、`tool_calls`、`logprobs`、`service_tier`、`system_fingerprint`

## 参考

- [音视频翻译指南](/developer-guides/speech/file-translation)
- [获取 API Key](/api-reference/preparation/api-key)
- [将 API Key 设置为环境变量](/api-reference/preparation/export-api-key-env)
- [安装 SDK](/api-reference/preparation/install-sdk)
