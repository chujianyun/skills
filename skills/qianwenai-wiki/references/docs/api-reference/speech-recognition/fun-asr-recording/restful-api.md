> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Fun-ASR 录音文件识别 HTTP API

> 录音文件转写 REST API

**使用指南**： 教程、代码示例和模型详情请参见[录音文件转写](/developer-guides/speech/asr)。

该服务包含两个 API：[任务提交](#任务提交-api)和[任务查询](#任务查询-api)。先提交任务，再轮询查询 API 获取结果。

## 限制条件

该服务不支持上传本地文件或 Base64 编码的音频。您必须提供通过 HTTP 或 HTTPS 协议**公开访问的文件 URL**，例如 `https://your-domain.com/file.mp3`。

通过 `file_urls` 参数指定 URL，单次请求最多支持 100 个 URL。

- **音频格式**：`aac`、`amr`、`avi`、`flac`、`flv`、`m4a`、`mkv`、`mov`、`mp3`、`mp4`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv`

<Warning>
  音频格式存在众多变体，API 无法保证所有格式都能正确处理。请先测试您的文件以验证结果。
</Warning>

- **音频采样率**： 不限
- **文件大小和时长**：最大 2 GB，最长 12 小时。超出限制的文件需先预处理，参见[使用 FFmpeg 预处理音频文件](/resources/faq-audio-speech#common-audio-issues)。
- **批量大小**：单次请求最多 100 个文件 URL。
- **支持语言**：fun-asr 系列支持 30 种语言，详见[支持的语言](#支持的语言)。
- **前端调用**：不支持从前端直接调用该 API，请使用后端代理。

## 任务提交 API

### 基本信息

| 项目   | 说明                                                                       |
| ---- | ------------------------------------------------------------------------ |
| 描述   | 提交语音识别任务。                                                                |
| URL  | `https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription` |
| 请求方式 | POST                                                                     |
| 请求头  | 见下文                                                                      |
| 请求体  | 见下文                                                                      |

**请求头**：

```http
Authorization: Bearer $DASHSCOPE_API_KEY
Content-Type: application/json
X-DashScope-Async: enable
```

<Warning>
  必须包含 `X-DashScope-Async: enable` 请求头。
</Warning>

**请求体**（包含所有[请求参数](#请求参数)，可选字段可省略）：

<Tabs>
  <Tab title="普通调用">
    ```json
    {
      "model": "qwen-audio-3.0-asr-flash-filetrans",
      "input": {
        "file_urls": [
          "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
          "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav"
        ]
      },
      "parameters": {
        "channel_id": [0],
        "diarization_enabled": false,
        "speaker_count": 2
      }
    }
    ```
  </Tab>

  <Tab title="即时热词">
    使用即时热词时格式如下：

    ```json
    {
      "model": "qwen-audio-3.0-asr-flash-filetrans",
      "input": {
        "file_urls": [
          "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav"
        ]
      },
      "parameters": {
        "vocabulary": {"张三": 5, "李四": 5}
      }
    }
    ```
  </Tab>

  <Tab title="上下文">
    使用上下文时格式如下：

    ```json
    {
      "model": "qwen-audio-3.0-asr-flash-filetrans",
      "input": {
        "file_urls": [
          "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav"
        ],
        "context": [
          {
            "role": "user",
            "content": [
              { "type": "input_text", "text": "你好啊" }
            ]
          },
          {
            "role": "assistant",
            "content": [
              { "type": "text", "text": "你好啊，我是通义千问，有什么可以帮助你的？" }
            ]
          }
        ]
      },
      "parameters": {
        "vocabulary": {"张三": 5, "李四": 5}
      }
    }
    ```
  </Tab>
</Tabs>

### 请求参数

<Accordion title="点击查看请求示例">
  ```bash
  curl --location 'https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription' \
       --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
       --header "Content-Type: application/json" \
       --header "X-DashScope-Async: enable" \
       --data '{"model":"qwen-audio-3.0-asr-flash-filetrans","input":{"file_urls":["https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
                "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav"]},"parameters":{"channel_id":[0]}}'
  ```
</Accordion>

| 参数                         | 类型              | 默认值           | 是否必填 | 说明                                                                                                                                                                                                                                                                                                                  |
| -------------------------- | --------------- | ------------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| model                      | string          | -             | 是    | 模型名称。支持 Qwen-Audio-3.0-ASR-Flash-Filetrans 和 Fun-ASR 系列模型，参见[语音识别模型](/developer-guides/speech/speech-to-text-models)。                                                                                                                                                                                               |
| file\_urls                 | array\[string]  | -             | 是    | 音频或视频文件 URL 列表（HTTP/HTTPS），单次请求最多 100 个 URL。                                                                                                                                                                                                                                                                        |
| context                    | array\[object]  | -             | 否    | 消息列表，包含可选的对话上下文（用于提升识别效果）。参见[上下文增强](/developer-guides/speech/improve-recognition-accuracy#上下文增强)。SDK 暂不支持该功能。                                                                                                                                                                                                       |
| context\[].role            | string          | -             | 否    | 消息角色。`user`：前几轮的识别结果或领域相关的词表；`assistant`：前几轮大语言模型的回复内容。                                                                                                                                                                                                                                                             |
| context\[].content         | array\[object]  | -             | 否    | 消息内容列表。                                                                                                                                                                                                                                                                                                             |
| context\[].content\[].type | string          | -             | 否    | 内容类型。`input_text`（上下文，前几轮用户语音的识别结果或词表，`role` 为 `user`，需同时传入 `text`）；`text`（上下文，前几轮大语言模型的回复内容，`role` 为 `assistant`，需同时传入 `text`）。                                                                                                                                                                                    |
| context\[].content\[].text | string          | -             | 条件必选 | `type` 为 `input_text` 或 `text` 时必填。上下文文本内容，每轮所有消息的 `text` 字段长度之和不超过 400 个字符，超出部分从末尾截断。                                                                                                                                                                                                                              |
| vocabulary\_id             | string          | -             | 否    | 预编译热词列表 ID。需预先调用创建热词列表接口生成，识别时传入该 ID 即可使用列表中的热词。适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景。参见[预编译热词](/developer-guides/speech/improve-recognition-accuracy#预编译热词)。                                                                                                                                                                 |
| vocabulary                 | object          | -             | 否    | 即时热词。以键值对形式传入，键为热词文本（`string`），值为热词权重（`integer`），无需预先创建热词列表。权重取值范围为 \[1, 5] 或 50：取 \[1, 5] 时值越大模型越倾向输出该词；取 50 时为超级热词，召回率大幅提升，但超级热词数量最多不超过 50 个。适用于临时性、会话级别的热词优化。与预编译热词同时配置时，仅即时热词生效。参见[即时热词](/developer-guides/speech/improve-recognition-accuracy#即时热词)。<br /><br />仅 `qwen-audio-3.0-asr-flash-filetrans` 支持即时热词。 |
| channel\_id                | array\[integer] | \[0]          | 否    | 多音轨文件中要识别的音轨索引，从 0 开始。例如 `[0]` 识别第一音轨，`[0, 1]` 识别前两个音轨。默认识别第一音轨。                                                                                                                                                                                                                                                    |
| special\_word\_filter      | string          | -             | 否    | 配置敏感词处理方式。参见[敏感词过滤详情](#敏感词过滤详情)。                                                                                                                                                                                                                                                                                    |
| diarization\_enabled       | boolean         | false         | 否    | 启用说话人分离。仅支持单声道音频。启用后，结果中包含 `speaker_id` 字段以区分不同说话人。参见[识别结果说明](#识别结果说明)。                                                                                                                                                                                                                                             |
| speaker\_count             | integer         | -             | 否    | 说话人数量参考值（2 到 100）。仅在 `diarization_enabled` 为 `true` 时生效。算法会尽量输出指定数量的说话人，但不保证准确。默认自动检测。                                                                                                                                                                                                                              |
| language\_hints            | array\[string]  | \["zh", "en"] | 否    | 识别语言代码。未设置时模型自动检测语言。对于 Qwen-Audio-3.0-ASR-Flash-Filetrans 系列模型，最多支持设置 4 个值，超出 4 个时仅前 4 个生效；对于 Fun-ASR 系列模型，仅支持设置 1 个值。参见[支持的语言](#支持的语言)。                                                                                                                                                                            |

<Warning>
  `channel_id` 中的每个音轨单独计费。例如：对一个文件使用 `[0, 1]` 会产生两次计费。
</Warning>

#### 敏感词过滤详情

未设置 `special_word_filter` 时，内置过滤器将匹配的词替换为等长的星号（`*`）。

设置后，可使用以下策略：

- **替换为 `*`**：将匹配的词替换为等长的星号。
- **过滤删除**：从结果中移除匹配的词。

值必须为 JSON 字符串：

```json
{
  "filter_with_signed": {
    "word_list": ["test"]
  },
  "filter_with_empty": {
    "word_list": ["start", "happen"]
  },
  "system_reserved_filter": true
}
```

**字段说明**：

- `filter_with_signed`
  - 类型：object。是否必填：否。
  - 将匹配的词替换为等长的星号。
  - 示例："Help me test this piece of code" 变为 "Help me \*\*\*\* this piece of code"。
  - 内部字段：`word_list` -- 要替换的词的字符串数组。

- `filter_with_empty`
  - 类型：object。是否必填：否。
  - 从结果中移除匹配的词。
  - 示例："Is the game about to start?" 变为 "Is the game about to ?"。
  - 内部字段：`word_list` -- 要移除的词的字符串数组。

- `system_reserved_filter`
  - 类型：Boolean。是否必填：否。默认值：`true`。
  - 启用系统预设的敏感词规则。设为 `true` 时，匹配 [千问AI平台敏感词列表](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/%E7%99%BE%E7%82%BC%E6%95%8F%E6%84%9F%E8%AF%8D%E5%88%97%E8%A1%A8_20230716.words.txt)的词会被替换为等长的星号。

#### 支持的语言

各模型支持的语言代码：

- **qwen-audio-3.0-asr-flash-filetrans, fun-asr, fun-asr-2025-11-07, fun-asr-mtl, fun-asr-mtl-2025-08-25**：
  - `zh`：中文、`en`：英文、`ja`：日语、`ko`：韩语、`vi`：越南语、`th`：泰语、`id`：印尼语、`ms`：马来语、`tl`：菲律宾语、`hi`：印地语、`ar`：阿拉伯语、`fr`：法语、`de`：德语、`es`：西班牙语、`pt`：葡萄牙语、`ru`：俄语、`it`：意大利语、`nl`：荷兰语、`sv`：瑞典语、`da`：丹麦语、`fi`：芬兰语、`no`：挪威语、`el`：希腊语、`pl`：波兰语、`cs`：捷克语、`hu`：匈牙利语、`ro`：罗马尼亚语、`bg`：保加利亚语、`hr`：克罗地亚语、`sk`：斯洛伐克语

- **fun-asr-2025-08-25**：
  - `zh`：中文、`en`：英文

### 响应参数

<Accordion title="点击查看响应示例">
  ```json
  {
    "output": {
      "task_status": "PENDING",
      "task_id": "c2e5d63b-96e1-4607-bb91-************"
    },
    "request_id": "77ae55ae-be17-97b8-9942-************"
  }
  ```
</Accordion>

| 参数           | 类型     | 说明                                               |
| ------------ | ------ | ------------------------------------------------ |
| task\_status | string | 任务状态：`PENDING`、`RUNNING`、`SUCCEEDED` 或 `FAILED`。 |
| task\_id     | string | 任务 ID，用于[任务查询 API](#任务查询-api) 获取结果。              |
| request\_id  | string | 请求 ID。                                           |

## 任务查询 API

### 基本信息

| 项目   | 说明                                                        |
| ---- | --------------------------------------------------------- |
| 描述   | 查询语音识别任务的状态和结果。                                           |
| URL  | `https://dashscope.aliyuncs.com/api/v1/tasks/\{task_id\}` |
| 请求方式 | GET                                                       |
| 请求头  | 见下文                                                       |
| 请求体  | 无                                                         |

**请求头**：

```http
Authorization: Bearer $DASHSCOPE_API_KEY
```

### 请求参数

<Accordion title="点击查看请求示例">
  ```bash
  curl --location 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
       --header "Authorization: Bearer $DASHSCOPE_API_KEY"
  ```
</Accordion>

| 参数       | 类型     | 默认值 | 是否必填 | 说明                              |
| -------- | ------ | --- | ---- | ------------------------------- |
| task\_id | string | -   | 是    | [任务提交 API](#任务提交-api) 返回的任务 ID。 |

### 响应参数

<Note>
  多子任务场景：只要有任何一个子任务成功，整体状态即为 `SUCCEEDED`。请检查 `subtask_status` 了解各子任务的实际结果。
</Note>

<Accordion title="点击查看响应示例（成功）">
  ```json
  {
    "request_id": "f9e1afad-94d3-997e-a83b-************",
    "output": {
      "task_id": "f86ec806-4d73-485f-a24f-************",
      "task_status": "SUCCEEDED",
      "submit_time": "2024-09-12 15:11:40.041",
      "scheduled_time": "2024-09-12 15:11:40.071",
      "end_time": "2024-09-12 15:11:40.903",
      "results": [
        {
          "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav",
          "transcription_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/pre/filetrans-16k/20240912/15%3A11/3bdf7689-b598-409d-806a-121cff5e4a31-1.json?Expires=1726211500&OSSAccessKeyId=yourOSSAccessKeyId&Signature=Fj%2BaF%2FH0Kayj3w3My2ECBeP****%3D",
          "subtask_status": "SUCCEEDED"
        },
        {
          "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
          "transcription_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/pre/filetrans-16k/20240912/15%3A11/409a4b92-445b-4dd8-8c1d-f110954d82d8-1.json?Expires=1726211500&OSSAccessKeyId=yourOSSAccessKeyId&Signature=v5Owy5qoAfT7mzGmQgH0g8C****%3D",
          "subtask_status": "SUCCEEDED"
        }
      ],
      "task_metrics": {
        "TOTAL": 2,
        "SUCCEEDED": 2,
        "FAILED": 0
      }
    },
    "usage": {
      "duration": 9
    }
  }
  ```
</Accordion>

<Accordion title="点击查看响应示例（部分失败）">
  `code` 字段包含错误码，`message` 字段包含错误信息。这些字段仅在出错时出现。

  ```json
  {
    "request_id": "a1b2c3d4-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "output": {
      "task_id": "7bac899c-06ec-4a79-8875-xxxxxxxxxxxx",
      "task_status": "SUCCEEDED",
      "submit_time": "2024-12-16 16:30:59.170",
      "scheduled_time": "2024-12-16 16:30:59.204",
      "end_time": "2024-12-16 16:31:02.375",
      "results": [
        {
          "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/long_audio_demo_cn.mp3",
          "transcription_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/prod/paraformer-v2/20241216/xxxx",
          "subtask_status": "SUCCEEDED"
        },
        {
          "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/rich_text_example_1.wav",
          "code": "InvalidFile.DownloadFailed",
          "message": "The audio file cannot be downloaded.",
          "subtask_status": "FAILED"
        }
      ],
      "task_metrics": {
        "TOTAL": 2,
        "SUCCEEDED": 1,
        "FAILED": 1
      }
    }
  }
  ```
</Accordion>

<Accordion title="点击查看响应示例（进行中）">
  ```json
  {
    "request_id": "b3c4d5e6-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "output": {
      "task_id": "9d1f2a3b-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "task_status": "RUNNING",
      "submit_time": "2024-09-12 15:11:40.041",
      "scheduled_time": "2024-09-12 15:11:40.071",
      "task_metrics": {
        "TOTAL": 2,
        "SUCCEEDED": 0,
        "FAILED": 0
      }
    }
  }
  ```
</Accordion>

| 参数                 | 类型     | 说明                                                                              |
| ------------------ | ------ | ------------------------------------------------------------------------------- |
| task\_id           | string | 任务 ID。                                                                          |
| task\_status       | string | 任务状态。                                                                           |
| subtask\_status    | string | 子任务状态。                                                                          |
| file\_url          | string | 已处理文件的 URL。                                                                     |
| transcription\_url | string | 识别结果链接，有效期 24 小时。过期后无法查询任务或下载结果。结果为 JSON 文件，可通过 HTTP 下载或读取。参见[识别结果说明](#识别结果说明)。 |
| submit\_time       | string | 任务提交时间。                                                                         |
| scheduled\_time    | string | 任务调度时间。                                                                         |
| end\_time          | string | 任务结束时间。                                                                         |
| task\_metrics      | object | 任务指标：包含 `TOTAL`（总数）、`SUCCEEDED`（成功数）和 `FAILED`（失败数）。                            |
| usage              | object | 用量信息。`duration` 为总时长，单位为秒。                                                      |

### 识别结果说明

识别结果为 JSON 文件。

<Accordion title="点击查看识别结果示例">
  以下为启用说话人分离（diarization\_enabled=true）时的识别结果示例：

  ```json
  {
    "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
    "properties": {
      "audio_format": "pcm_s16le",
      "channels": [0],
      "original_sampling_rate": 16000,
      "original_duration_in_milliseconds": 3834
    },
    "transcripts": [
      {
        "channel_id": 0,
        "content_duration_in_milliseconds": 3720,
        "text": "Hello world, this is Alibaba Speech Lab.",
        "sentences": [
          {
            "begin_time": 100,
            "end_time": 3820,
            "text": "Hello world, this is Alibaba Speech Lab.",
            "sentence_id": 1,
            "speaker_id": 0,
            "words": [
              {
                "begin_time": 100,
                "end_time": 596,
                "text": "Hello ",
                "punctuation": ""
              },
              {
                "begin_time": 596,
                "end_time": 844,
                "text": "world",
                "punctuation": ", "
              }
            ]
          }
        ]
      }
    ]
  }
  ```

  <Note>
    `speaker_id` 字段仅在启用说话人分离时出现。为简洁起见，其他词条目已省略。
  </Note>
</Accordion>

主要参数：

| 参数                                   | 类型              | 说明                                    |
| ------------------------------------ | --------------- | ------------------------------------- |
| audio\_format                        | string          | 源文件的音频格式。                             |
| channels                             | array\[integer] | 音轨索引。单音轨返回 `[0]`，双音轨返回 `[0, 1]`，以此类推。 |
| original\_sampling\_rate             | integer         | 采样率（Hz）。                              |
| original\_duration\_in\_milliseconds | integer         | 原始音频时长（毫秒）。                           |
| channel\_id                          | integer         | 转写的音轨索引，从 0 开始。                       |
| content\_duration\_in\_milliseconds  | integer         | 音轨中语音内容的时长（毫秒）。                       |
| text                                 | string          | 转写文本（段落级或词级，取决于上下文）。                  |
| sentences                            | array           | 句级转写结果。                               |
| sentence\_id                         | integer         | 句子序号，从 1 开始。                          |
| words                                | array           | 词级转写结果。                               |
| begin\_time                          | integer         | 起始时间戳（毫秒）。                            |
| end\_time                            | integer         | 结束时间戳（毫秒）。                            |
| speaker\_id                          | integer         | 说话人索引，从 0 开始。仅在启用说话人分离时出现。            |
| punctuation                          | string          | 词后的预测标点符号（如有）。                        |

<Warning>
  计费仅基于语音片段，而非文件总时长。非语音片段不计费。由于语音检测使用 AI 模型，计费时长可能与预期内容时长略有差异。
</Warning>

## DashScope 同步调用

与上述异步调用（提交-轮询）不同，同步调用适用于短音频场景，一次请求立即返回识别结果。该模式包含两个模型：`qwen-audio-3.0-asr-flash`（离线，最长 5 分钟音频，支持上下文增强）和 `fun-asr-realtime`（在线，仅支持北京地域）。此功能均不支持 SDK 调用。

### Qwen-Audio-3.0-ASR-Flash / Fun-ASR-Flash

#### 服务端点

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
```

#### 请求头

| 参数              | 类型     | 是否必选 | 说明                                                         |
| --------------- | ------ | ---- | ---------------------------------------------------------- |
| Authorization   | string | 是    | 鉴权令牌，格式为 `Bearer $DASHSCOPE_API_KEY`。                      |
| Content-Type    | string | 是    | 固定为 `application/json`。                                    |
| X-DashScope-SSE | string | 否    | 设为 `enable` 时以 SSE 流式方式返回中间和最终结果；设为 `disable` 或不传则仅返回最终结果。 |

#### 请求参数

<Note>
  润色顺滑功能默认关闭，**暂未开放**。

  润色顺滑：模型在识别语音的同时，自动清理无意义语气词和口吃重复，处理说话过程中的自我纠正，理顺口语表达，并规范标点与文本格式。输出结果更加简洁、流畅、易读，同时尽可能保留用户的最终意图和关键信息。
</Note>

| 参数                                             | 类型             | 是否必选 | 说明                                                                                                                                                                                                                                     |
| ---------------------------------------------- | -------------- | ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| model                                          | string         | 是    | 模型名称。支持 Qwen-Audio-3.0-ASR-Flash 和 Fun-ASR-Flash 系列模型，参见[语音识别模型](/developer-guides/speech/speech-to-text-models)。                                                                                                                      |
| input.messages                                 | array\[object] | 是    | 消息列表。包含当前待识别的音频，以及可选的对话上下文（用于提升专有词汇的识别准确率），参见[上下文增强](/developer-guides/speech/improve-recognition-accuracy#上下文增强)。                                                                                                                     |
| input.messages\[].role                         | string         | 是    | 消息角色。`user`：用户消息，`type` 为 `input_audio` 时表示当前待识别的音频，为 `input_text` 时表示上下文中前几轮的识别结果或词表。`assistant`：上下文中前几轮大语言模型的回复内容。                                                                                                                   |
| input.messages\[].content\[].type              | string         | 是    | 内容类型。每个请求至少需要一条 `input_audio` 类型的消息。取值：`input_audio`（当前待识别的音频，`role` 为 `user`）、`input_text`（上下文中前几轮的识别结果或词表，`role` 为 `user`）、`text`（上下文中前几轮大语言模型的回复内容，`role` 为 `assistant`）。                                                           |
| input.messages\[].content\[].input\_audio.data | string         | 条件必选 | `type` 为 `input_audio` 时必填。待识别音频数据，支持音频文件 URL 或 Base64 Data URI（格式：`data:{MIME_TYPE};base64,{BASE64_ENCODED_DATA}`，支持的 MIME 类型包括 `audio/wav`、`audio/mp3` 等）。                                                                           |
| input.messages\[].content\[].text              | string         | 条件必选 | `type` 为 `input_text` 或 `text` 时必填。上下文文本内容，每轮所有消息的 `text` 字段长度之和不超过 400 个字符，超出部分从末尾截断。                                                                                                                                                 |
| parameters.format                              | string         | 是    | 音频格式，如 `wav`、`mp3`、`opus`。                                                                                                                                                                                                             |
| parameters.sample\_rate                        | string         | 否    | 音频采样率，单位 Hz，例如 `16000` 表示 16kHz。                                                                                                                                                                                                       |
| parameters.vocabulary\_id                      | string         | 否    | 预编译热词列表 ID。需预先调用创建热词列表接口生成，识别时传入该 ID 即可使用列表中的热词。适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景。参见[预编译热词](/developer-guides/speech/improve-recognition-accuracy#预编译热词)。                                                                                    |
| parameters.vocabulary                          | object         | 否    | 即时热词。以键值对形式传入，键为热词文本（`string`），值为热词权重（`integer`），无需预先创建热词列表。权重取值范围为 \[1, 5] 或 50：取 50 时为超级热词。与预编译热词同时配置时，仅即时热词生效。参见[即时热词](/developer-guides/speech/improve-recognition-accuracy#即时热词)。<br /><br />仅 `qwen-audio-3.0-asr-flash` 支持即时热词。 |
| parameters.language\_hints                     | array\[string] | 否    | 识别语言代码。未设置时模型自动检测语言。对于 Qwen-Audio-3.0-ASR-Flash 系列模型，最多支持设置 4 个值，超出 4 个时仅前 4 个生效；对于 Fun-ASR-Flash 系列模型，仅支持设置 1 个值。参见[支持的语言](#支持的语言)。                                                                                                   |

#### 示例

<Tabs>
  <Tab title="非流式">
    ```bash
    curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header "Content-Type: application/json" \
      --header "X-DashScope-SSE: disable" \
      --data '{
      "model": "qwen-audio-3.0-asr-flash",
      "input": {
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "input_audio",
                "input_audio": {
                  "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav"
                }
              }
            ]
          }
        ]
      },
      "parameters": {
        "format": "wav",
        "sample_rate": "16000"
      }
    }'
    ```
  </Tab>

  <Tab title="流式（SSE）">
    ```bash
    curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header "Content-Type: application/json" \
      --header "X-DashScope-SSE: enable" \
      --data '{
      "model": "qwen-audio-3.0-asr-flash",
      "input": {
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "input_audio",
                "input_audio": {
                  "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav"
                }
              }
            ]
          }
        ]
      },
      "parameters": {
        "format": "wav",
        "sample_rate": "16000"
      }
    }'
    ```
  </Tab>

  <Tab title="即时热词">
    ```bash
    curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header "Content-Type: application/json" \
      --header "X-DashScope-SSE: disable" \
      --data '{
      "model": "qwen-audio-3.0-asr-flash",
      "input": {
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "input_audio",
                "input_audio": {
                  "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav"
                }
              }
            ]
          }
        ]
      },
      "parameters": {
        "format": "wav",
        "sample_rate": "16000",
        "vocabulary": {"张三": 5, "李四": 5}
      }
    }'
    ```
  </Tab>

  <Tab title="携带上下文-非流式">
    ```bash
    curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header "Content-Type: application/json" \
      --header "X-DashScope-SSE: disable" \
      --data '{
      "model": "qwen-audio-3.0-asr-flash",
      "input": {
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "input_text",
                "text": "你好啊"
              }
            ]
          },
          {
            "role": "assistant",
            "content": [
              {
                "type": "text",
                "text": "你好啊，我是通义千问，有什么可以帮助你的？"
              }
            ]
          },
          {
            "role": "user",
            "content": [
              {
                "type": "input_audio",
                "input_audio": {
                  "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav"
                }
              }
            ]
          }
        ]
      },
      "parameters": {
        "format": "wav",
        "sample_rate": "16000"
      }
    }'
    ```
  </Tab>

  <Tab title="携带上下文-流式（SSE）">
    ```bash
    curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header "Content-Type: application/json" \
      --header "X-DashScope-SSE: enable" \
      --data '{
      "model": "qwen-audio-3.0-asr-flash",
      "input": {
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "input_text",
                "text": "你好啊"
              }
            ]
          },
          {
            "role": "assistant",
            "content": [
              {
                "type": "text",
                "text": "你好啊，我是通义千问，有什么可以帮助你的？"
              }
            ]
          },
          {
            "role": "user",
            "content": [
              {
                "type": "input_audio",
                "input_audio": {
                  "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav"
                }
              }
            ]
          }
        ]
      },
      "parameters": {
        "format": "wav",
        "sample_rate": "16000"
      }
    }'
    ```
  </Tab>
</Tabs>

#### Base64 音频上传

可输入 Base64 编码数据（[Data URL](https://www.rfc-editor.org/rfc/rfc2397)），格式为：

```
data:<mediatype>;base64,<data>
```

- `<mediatype>`：MIME 类型，因音频格式而异，例如：
  - WAV：`audio/wav`
  - MP3：`audio/mpeg`
- `<data>`：音频转成的 Base64 编码字符串。Base64 编码会增大体积，请控制原文件大小，确保编码后仍符合输入音频大小限制（10MB）。

示例：`data:audio/wav;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5LjEwMAAAAAAAAAAAAAAA//PAxABQ/BXRbMPe4IQAhl9`

将本地音频文件转换为 Base64 Data URI：

<Tabs>
  <Tab title="Python">
    ```python
    import base64, pathlib
    # input.mp3 为待识别的本地音频文件，请替换为自己的音频文件路径，确保其符合音频要求
    file_path = pathlib.Path("input.mp3")
    base64_str = base64.b64encode(file_path.read_bytes()).decode()
    data_uri = f"data:audio/mpeg;base64,{base64_str}"
    ```
  </Tab>

  <Tab title="Java">
    ```java
    import java.nio.file.*;
    import java.util.Base64;

    public class Main {
      /**
       * filePath 为待识别的本地音频文件，请替换为自己的音频文件路径，确保其符合音频要求
       */
      public static String toDataUrl(String filePath) throws Exception {
        byte[] bytes = Files.readAllBytes(Paths.get(filePath));
        String encoded = Base64.getEncoder().encodeToString(bytes);
        return "data:audio/mpeg;base64," + encoded;
      }

      public static void main(String[] args) throws Exception {
        System.out.println(toDataUrl("input.mp3"));
      }
    }
    ```
  </Tab>
</Tabs>

使用 Base64 Data URI 调用识别接口的完整示例：

```python
import base64, pathlib
import os
import requests

# input.wav 为待识别的本地音频文件，请替换为自己的音频文件路径，确保其符合音频要求
file_path = pathlib.Path("input.wav")
base64_str = base64.b64encode(file_path.read_bytes()).decode()
data_uri = f"data:audio/wav;base64,{base64_str}"

url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
headers = {
    "Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}",
    "Content-Type": "application/json",
    "X-DashScope-SSE": "disable",
}
payload = {
    "model": "qwen-audio-3.0-asr-flash",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": data_uri,
                        },
                    }
                ],
            }
        ]
    },
    "parameters": {
        "format": "wav",
        "sample_rate": "16000",
    },
}
response = requests.post(url, headers=headers, json=payload)
print(response.status_code)
print(response.json())
```

#### 响应字段

| 参数                            | 类型      | 说明                                                                          |
| ----------------------------- | ------- | --------------------------------------------------------------------------- |
| request\_id                   | string  | 本次请求的唯一标识。                                                                  |
| output.text                   | string  | 当前累积的完整识别文本。                                                                |
| output.sentence.sentence\_id  | integer | 句子编号，从 1 开始。                                                                |
| output.sentence.sentence\_end | boolean | 是否为该句的最终结果（`true`=识别完成，`false`=识别中）。                                        |
| output.sentence.begin\_time   | integer | 句子开始时间，单位毫秒。                                                                |
| output.sentence.end\_time     | integer | 句子结束时间，单位毫秒。仅在 `sentence_end` 为 `true` 时返回。                                 |
| output.sentence.channel\_id   | integer | 声道编号，从 0 开始。                                                                |
| output.sentence.words         | array   | 词级别时间戳列表，每个词包含 `text`、`begin_time`、`end_time`、`punctuation`、`fixed`（是否已确认）。 |
| usage.duration                | integer | 已处理的音频时长，单位秒。仅在 `sentence_end` 为 `true` 时返回。                                |

### Fun-ASR-Realtime

<Note>
  该功能只支持北京地域。
</Note>

#### 服务端点

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
```

#### 请求头

| 参数              | 类型     | 是否必选 | 说明                                                         |
| --------------- | ------ | ---- | ---------------------------------------------------------- |
| Authorization   | string | 是    | 鉴权令牌，格式为 `Bearer $DASHSCOPE_API_KEY`。                      |
| Content-Type    | string | 是    | 固定为 `application/json`。                                    |
| X-DashScope-SSE | string | 否    | 设为 `enable` 时以 SSE 流式方式返回中间和最终结果；设为 `disable` 或不传则仅返回最终结果。 |

#### 请求参数

| 参数                                 | 类型             | 是否必选 | 说明                                                                                                     |
| ---------------------------------- | -------------- | ---- | ------------------------------------------------------------------------------------------------------ |
| model                              | string         | 是    | 模型名称。取值：`fun-asr-realtime`（稳定版）、`fun-asr-realtime-2026-02-28`。                                         |
| input.messages                     | array\[object] | 条件必选 | 消息列表，使用 Base64 方式上传音频时填写。与 `parameters.audio_address` 二选一。                                             |
| input.messages\[].content\[].audio | string         | 是    | 待识别音频，Data URI 格式：`data:audio/wav;base64,{BASE64_ENCODED_DATA}`。支持的 MIME 类型：`audio/wav`、`audio/mp3` 等。 |
| input.messages\[].role             | string         | 是    | 固定为 `user`。                                                                                            |
| parameters.audio\_address          | string         | 条件必选 | 音频文件 URL（HTTP/HTTPS）。与 `input.messages` 二选一。                                                           |
| parameters.format                  | string         | 否    | 音频格式，如 `mp3`、`wav`。                                                                                    |
| parameters.vad\_enabled            | boolean        | 否    | 是否启用 VAD。默认值：`false`。启用后对音频做端点检测再识别。                                                                   |

#### 示例

<Tabs>
  <Tab title="非流式">
    ```bash
    curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header "Content-Type: application/json" \
      --header "X-DashScope-SSE: disable" \
      --data '{
      "model": "fun-asr-realtime",
      "input": {
        "messages": []
      },
      "parameters": {
        "audio_address": "https://example.com/audio/sample.mp3",
        "format": "mp3"
      },
      "resources": []
    }'
    ```
  </Tab>

  <Tab title="流式（SSE）">
    ```bash
    curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header "Content-Type: application/json" \
      --header "X-DashScope-SSE: enable" \
      --data '{
      "model": "fun-asr-realtime",
      "input": {
        "messages": []
      },
      "parameters": {
        "audio_address": "https://example.com/audio/sample.mp3",
        "format": "mp3"
      },
      "resources": []
    }'
    ```
  </Tab>
</Tabs>

#### 响应字段

流式（SSE）模式下，每个事件的 `output.sentence` 包含以下字段：

| 参数              | 类型      | 说明                                                                       |
| --------------- | ------- | ------------------------------------------------------------------------ |
| text            | string  | 识别文本。                                                                    |
| sentence\_id    | integer | 句子序号，从 1 开始递增。                                                           |
| sentence\_end   | boolean | 是否句子结束（`true`=最终结果，`false`=中间结果）。                                        |
| sentence\_begin | boolean | 是否为语句起始帧。                                                                |
| begin\_time     | integer | 语句开始时间（ms）。                                                              |
| end\_time       | integer | 语句结束时间（ms）。                                                              |
| channel\_id     | integer | 音频通道编号。                                                                  |
| words           | array   | 词级时间戳。每个词包含 `begin_time`、`end_time`、`text`、`punctuation`、`fixed`（是否已确认）。 |

## 常见问题

### 功能特性

<AccordionGroup>
  <Accordion title="是否支持Base64编码方式的音频？">
    异步任务提交 API 不支持。Fun-ASR 非实时语音识别仅支持公网可访问的 HTTP/HTTPS URL，不支持本地文件上传或 Base64 编码格式。
  </Accordion>

  <Accordion title="如何将音频文件以公网可访问的URL形式提供？">
    可通过以下方式获取公网URL：

    1. **选择存储服务**：使用对象存储、自建Web服务器或CDN等。
    2. **上传文件**：将音频文件上传至所选存储服务。
    3. **生成URL**：获取文件的公网访问链接。
    4. **验证URL**：在浏览器中访问该URL，确认可以正常下载文件。

    <Warning>
      使用SDK时，不支持 `oss://` 前缀的URL。使用RESTful API时，虽然支持 `oss://` 前缀，但生成的下载链接有效期仅48小时、且QPS限制为100，不建议在生产环境使用。
    </Warning>
  </Accordion>

  <Accordion title="多久能获取识别结果？">
    任务提交后会进入PENDING（排队）状态，排队时长取决于当前队列长度和音频时长，通常在几分钟内完成。音频越长，等待时间可能越长。
  </Accordion>
</AccordionGroup>

### 故障排查

<AccordionGroup>
  <Accordion title="一直轮询不到结果？">
    可能是当前服务负载较高导致排队时间较长，请耐心等待。
  </Accordion>

  <Accordion title="无法识别语音（无识别结果）是什么原因？">
    请检查音频格式和采样率是否正确且符合参数约束。可以使用 `ffprobe` 工具获取音频的容器、编码、采样率、声道等信息：

    ```bash
    ffprobe -v error -show_entries format=format_name -show_entries stream=codec_name,sample_rate,channels -of default=noprint_wrappers=1 input.xxx
    ```
  </Accordion>
</AccordionGroup>
