> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# MiniMax 语音合成 API 参考

> MiniMax 同步语音合成 API，支持非流式和 SSE 流式两种模式，将文本转换为音频。

## 支持的模型

支持的模型：MiniMax/speech-2.8-hd、MiniMax/speech-02-hd、MiniMax/speech-2.8-turbo、MiniMax/speech-02-turbo。

## 请求端点

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
```

<Note>
  第三方模型（MiniMax）目前仅支持通过 `dashscope.aliyuncs.com` 域名调用，暂不支持业务空间专属域名。
</Note>

## 请求头

| 参数              | 类型     | 是否必选 | 说明                                   |
| --------------- | ------ | ---- | ------------------------------------ |
| Authorization   | string | 必选   | 鉴权信息，格式为 `Bearer $DASHSCOPE_API_KEY` |
| Content-Type    | string | 必选   | 请求体格式，固定为 `application/json`         |
| X-DashScope-SSE | string | 可选   | 设置为 `enable` 时开启 SSE 流式输出            |

## 请求体

### 顶层字段

| 参数    | 类型     | 是否必选 | 说明                            |
| ----- | ------ | ---- | ----------------------------- |
| model | string | 必选   | 模型名称，可选值见[支持的模型](#支持的模型)      |
| input | object | 必选   | 输入数据，详见 [input 参数](#input-参数) |

### input 参数

| 参数                  | 类型        | 是否必选 | 说明                                                                                                                                                       |
| ------------------- | --------- | ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| text                | string    | 必选   | 待合成的文本，最多 10000 个字符。超过 3000 个字符时建议使用流式模式                                                                                                                 |
| stream\_options     | object    | 可选   | 流式输出的配置项，仅在请求头 `X-DashScope-SSE: enable` 时生效。详见 [stream\_options 参数](#stream-options-参数)                                                                 |
| voice\_setting      | object    | 必选   | 音色设置，详见 [voice\_setting 参数](#voice-setting-参数)                                                                                                           |
| audio\_setting      | object    | 可选   | 音频输出设置，详见 [audio\_setting 参数](#audio-setting-参数)                                                                                                         |
| pronunciation\_dict | object    | 可选   | 自定义发音词典，详见 [pronunciation\_dict 参数](#pronunciation-dict-参数)                                                                                              |
| timbre\_weights     | object\[] | 可选   | 混合音色配置，最多支持 4 个音色，详见 [timbre\_weights 参数](#timbre-weights-参数)                                                                                            |
| language\_boost     | string    | 可选   | 语言增强，默认为 null。支持 `auto` 或指定语言，详见[支持的语言](#language-boost-支持的语言)                                                                                           |
| voice\_modify       | object    | 可选   | 音效调整，详见 [voice\_modify 参数](#voice-modify-参数)                                                                                                             |
| subtitle\_enable    | boolean   | 可选   | 是否返回字幕信息，默认为 `false`。仅非流式模式可用，支持 speech-2.8-hd、speech-2.8-turbo、speech-2.6-hd、speech-2.6-turbo、speech-02-hd、speech-02-turbo、speech-01-hd、speech-01-turbo |
| output\_format      | string    | 可选   | 音频数据返回格式，默认为 `hex`。可选值：`url`（有效期24小时）或 `hex`（二进制 hex 编码）。仅非流式模式可用                                                                                        |
| aigc\_watermark     | boolean   | 可选   | 是否在音频末尾添加 AIGC 隐水印，默认为 `false`。仅非流式模式可用                                                                                                                  |

<a id="stream_options-参数" />

### stream\_options 参数

流式输出的配置项，仅在请求头 `X-DashScope-SSE: enable` 时生效。

| 参数                         | 类型      | 是否必选 | 说明                                                                                                                                                                                                                                                                                   |
| -------------------------- | ------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| exclude\_aggregated\_audio | boolean | 可选   | 控制流式输出的合成结束帧中，`audio` 字段是否返回本次合成的完整音频（即此前所有合成中分块拼接后的整段 hex 数据）。默认为 `false`。设置为 `false` 时，合成结束帧的 `audio` 字段返回所有分块拼接后的完整音频，客户端可在流结束时直接取用整段音频，无需自行拼接前面的分块。设置为 `true` 时，合成结束帧的 `audio` 字段为空字符串，整段音频需由客户端将此前所有合成中分块的 `audio` 按顺序自行拼接得到。可显著减少尾包体积与传输耗时，适用于客户端已经按 chunk 边接收边播放、或自行累积保存音频的场景 |

<Note>该参数仅在流式输出场景下生效；非流式输出场景下设置无效。</Note>

<a id="voice_setting-参数" />

### voice\_setting 参数

| 参数                  | 类型      | 是否必选 | 说明                                                                                                                                  |
| ------------------- | ------- | ---- | ----------------------------------------------------------------------------------------------------------------------------------- |
| voice\_id           | string  | 必选   | 音色 ID。使用 `timbre_weights` 混合音色时可留空                                                                                                  |
| speed               | float   | 可选   | 语速，默认 `1.0`，范围 \[0.5, 2.0]                                                                                                          |
| vol                 | float   | 可选   | 音量，默认 `1.0`，范围 (0.0, 10.0]                                                                                                          |
| pitch               | integer | 可选   | 音调，默认 `0`，范围 \[-12, 12]                                                                                                             |
| emotion             | string  | 可选   | 情感风格。可选值：`happy`、`sad`、`angry`、`fearful`、`disgusted`、`surprised`、`calm`、`whisper`。注意：speech-2.8-hd 和 speech-2.8-turbo 不支持 `whisper` |
| text\_normalization | boolean | 可选   | 是否对数字等内容进行中英文文本规范化处理，默认 `false`                                                                                                     |
| latex\_read         | boolean | 可选   | 是否朗读 LaTeX 公式，默认 `false`。仅支持中文，启用后自动将 `language_boost` 设置为中文。公式需用 `$` 包裹，反斜杠需转义为 `\\`                                               |

<a id="audio_setting-参数" />

### audio\_setting 参数

| 参数           | 类型      | 是否必选 | 说明                                                                    |
| ------------ | ------- | ---- | --------------------------------------------------------------------- |
| sample\_rate | integer | 可选   | 采样率，默认 `32000`。可选值：8000、16000、22050、24000、32000、44100                 |
| bitrate      | integer | 可选   | 比特率，默认 `128000`。可选值：32000、64000、128000、256000。仅在 `format` 为 `mp3` 时生效 |
| format       | string  | 可选   | 音频格式，默认 `mp3`。可选值：`mp3`、`pcm`、`flac`、`wav`                            |
| channel      | integer | 可选   | 声道数，默认 `1`。可选值：`1`（单声道）或 `2`（立体声）                                     |
| force\_cbr   | boolean | 可选   | 是否使用固定码率编码，默认 `false`。仅在流式 mp3 模式下生效                                  |

<a id="pronunciation_dict-参数" />

### pronunciation\_dict 参数

| 参数   | 类型        | 是否必选 | 说明                                                                                  |
| ---- | --------- | ---- | ----------------------------------------------------------------------------------- |
| tone | string\[] | 可选   | 自定义读音规则列表。分隔符为 `/`，中文声调用数字 1-5 表示。示例：`["燕少飞/(yan4)(shao3)(fei1)", "omg/oh my god"]` |

<a id="timbre_weights-参数" />

### timbre\_weights 参数

数组中每个对象包含以下字段：

| 参数        | 类型      | 是否必选 | 说明                  |
| --------- | ------- | ---- | ------------------- |
| voice\_id | string  | 必选   | 音色 ID               |
| weight    | integer | 必选   | 该音色的权重，范围 \[1, 100] |

<a id="voice_modify-参数" />

### voice\_modify 参数

非流式模式支持 mp3、wav、flac 格式；流式模式仅支持 mp3 格式。

| 参数             | 类型      | 是否必选 | 说明                                                                                           |
| -------------- | ------- | ---- | -------------------------------------------------------------------------------------------- |
| pitch          | integer | 可选   | 音调，范围 \[-100, 100]，值越低音调越低                                                                   |
| intensity      | integer | 可选   | 强度，范围 \[-100, 100]，值越低强度越强                                                                   |
| timbre         | integer | 可选   | 音色，范围 \[-100, 100]，值越低音色越浑厚                                                                  |
| sound\_effects | string  | 可选   | 音效效果。可选值：`spacious_echo`（宽阔回声）、`auditorium_echo`（礼堂回声）、`lofi_telephone`（复古电话）、`robotic`（机械音） |

<a id="language_boost-支持的语言" />

### language\_boost 支持的语言

`language_boost` 支持以下语言值：

`Chinese`、`Chinese,Yue`、`English`、`Arabic`、`Russian`、`Spanish`、`French`、`Portuguese`、`German`、`Turkish`、`Dutch`、`Ukrainian`、`Vietnamese`、`Indonesian`、`Japanese`、`Italian`、`Korean`、`Thai`、`Polish`、`Romanian`、`Greek`、`Czech`、`Finnish`、`Hindi`、`Bulgarian`、`Danish`、`Hebrew`、`Malay`、`Persian`、`Slovak`、`Swedish`、`Croatian`、`Filipino`、`Hungarian`、`Norwegian`、`Slovenian`、`Catalan`、`Nynorsk`、`Tamil`、`Afrikaans`、`auto`

## 请求示例

<CodeGroup>
  ```bash 非流式
  curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
    "model": "minimax/speech-2.8-hd",
    "input": {
      "text": "今天是不是很开心呀(laughs)，当然了！",
      "voice_setting": {
        "voice_id": "male-qn-qingse",
        "speed": 1,
        "vol": 1,
        "pitch": 0,
        "emotion": "happy"
      },
      "audio_setting": {
        "sample_rate": 32000,
        "bitrate": 128000,
        "format": "mp3",
        "channel": 1
      },
      "pronunciation_dict": {
        "tone": [
          "处理/(chu3)(li3)",
          "危险/dangerous"
        ]
      },
      "subtitle_enable": false
    }
  }'
  ```

  ```bash 流式（SSE）
  curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -H "X-DashScope-SSE: enable" \
    -d '{
    "model": "minimax/speech-2.8-hd",
    "input": {
      "text": "今天是不是很开心呀(laughs)，当然了！",
      "voice_setting": {
        "voice_id": "male-qn-qingse",
        "speed": 1,
        "vol": 1,
        "pitch": 0,
        "emotion": "happy"
      },
      "audio_setting": {
        "sample_rate": 32000,
        "bitrate": 128000,
        "format": "mp3",
        "channel": 1
      },
      "pronunciation_dict": {
        "tone": [
          "处理/(chu3)(li3)",
          "危险/dangerous"
        ]
      },
      "subtitle_enable": false
    }
  }'
  ```
</CodeGroup>

## 响应体

### 顶层字段

| 参数          | 类型     | 说明                                |
| ----------- | ------ | --------------------------------- |
| request\_id | string | 本次调用的唯一标识                         |
| output      | object | 模型输出数据，详见 [output 字段](#output-字段) |
| usage       | object | 用量信息，详见 [usage 字段](#usage-字段)     |

### output 字段

| 参数          | 类型     | 说明                                       |
| ----------- | ------ | ---------------------------------------- |
| base\_resp  | object | 状态信息，详见 [base\_resp 字段](#base-resp-字段)   |
| data        | object | 音频数据，合成失败时为 null，详见 [data 字段](#data-字段)  |
| extra\_info | object | 附加信息，详见 [extra\_info 字段](#extra-info-字段) |
| trace\_id   | string | 本次会话 ID，用于问题排查                           |

<a id="base_resp-字段" />

### base\_resp 字段

| 参数           | 类型      | 说明                                                                                                         |
| ------------ | ------- | ---------------------------------------------------------------------------------------------------------- |
| status\_code | integer | 状态码。`0`=成功；`1000`=未知错误；`1001`=超时；`1002`=触发限流；`1004`=鉴权失败；`1039`=触发 TPM 限流；`1042`=超过 10% 的无效字符；`2013`=参数不合法 |
| status\_msg  | string  | 状态描述                                                                                                       |

### data 字段

| 参数     | 类型      | 说明                    |
| ------ | ------- | --------------------- |
| audio  | string  | hex 编码的音频二进制数据        |
| status | integer | 合成状态。`1`=合成中；`2`=合成完成 |

<a id="extra_info-字段" />

### extra\_info 字段

| 参数                          | 类型      | 说明                                |
| --------------------------- | ------- | --------------------------------- |
| audio\_length               | integer | 音频时长（毫秒）                          |
| audio\_sample\_rate         | integer | 音频采样率                             |
| audio\_size                 | integer | 音频大小（字节）                          |
| bitrate                     | integer | 音频比特率                             |
| audio\_format               | string  | 音频格式，可选值：`mp3`、`pcm`、`flac`       |
| audio\_channel              | integer | 声道数，`1` 表示单声道，`2` 表示立体声           |
| invisible\_character\_ratio | float   | 无效字符占比。不超过 10% 时正常合成；超过 10% 时返回错误 |
| usage\_characters           | integer | 计费字符数                             |
| word\_count                 | integer | 词语数量（不含标点符号）                      |

### usage 字段

| 参数         | 类型      | 说明       |
| ---------- | ------- | -------- |
| characters | integer | 输入文本的字符数 |

## 响应示例

<CodeGroup>
  ```json 非流式
  {
    "output": {
      "base_resp": {
        "status_code": 0,
        "status_msg": "success"
      },
      "data": {
        "audio": "<hex编码的audio>",
        "status": 2
      },
      "extra_info": {
        "audio_channel": 1,
        "audio_format": "mp3",
        "audio_length": 3528,
        "audio_sample_rate": 16000,
        "audio_size": 58164,
        "bitrate": 128000,
        "invisible_character_ratio": 0,
        "usage_characters": 26,
        "word_count": 14
      },
      "trace_id": "05fdef92e4c1b32283e3d1c456971a80"
    },
    "usage": {
      "characters": 26
    },
    "request_id": "233b9516-1038-9697-b458-87e95a1f8108"
  }
  ```

  ```json 流式（SSE）
  {
    "output": {
      "base_resp": {
        "status_code": 0,
        "status_msg": "success"
      },
      "data": {
        "audio": "<hex编码的audio>",
        "status": 1
      },
      "extra_info": {
        "audio_channel": 1,
        "audio_format": "mp3",
        "audio_length": 3528,
        "audio_sample_rate": 16000,
        "audio_size": 58164,
        "bitrate": 128000,
        "invisible_character_ratio": 0,
        "usage_characters": 26,
        "word_count": 14
      },
      "trace_id": "05fdef92e4c1b32283e3d1c456971a80"
    },
    "usage": {
      "characters": 26
    },
    "request_id": "233b9516-1038-9697-b458-87e95a1f8108"
  }
  ```
</CodeGroup>
