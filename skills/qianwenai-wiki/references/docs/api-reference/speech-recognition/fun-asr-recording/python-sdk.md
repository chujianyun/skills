> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Fun-ASR 录音文件识别 Python SDK

> 录音文件转写 Python SDK

**使用指南**： 教程、代码示例和模型详情请参见[录音文件转写](/developer-guides/speech/asr)。

## 限制条件

文件必须为公开 URL（HTTP/HTTPS，如 `https://your-domain.com/file.mp3`）。不支持本地文件和 Base64 编码。

通过 `file_urls` 参数传入 URL，每次请求最多 100 个。

- **音频格式**：`aac`、`amr`、`avi`、`flac`、`flv`、`m4a`、`mkv`、`mov`、`mp3`、`mp4`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv`

<Warning>
  并非所有格式变体都经过测试，请先测试文件以验证转写效果。
</Warning>

- **音频采样率**： 无限制
- **文件大小和时长**：最大 2 GB，最长 12 小时。更大的文件请参见[音频裁剪](/developer-guides/speech/asr#q-how-do-i-process-audio-to-meet-model-requirements)。
- **批量处理**：每次请求最多 100 个 URL。
- **语言支持**： 各模型支持的语言代码详见[支持的语言](#supported-languages)。

## 请求参数

通过 [Transcription 类](#transcription-class)的 `async_call` 方法传入以下参数。

| **参数**         | **类型**     | **默认值** | **是否必选** | **说明**                                                                                                                                                                                                                                             |
| -------------- | ---------- | ------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| model          | str        | -       | 是        | 模型 ID。支持 Qwen-Audio-3.0-ASR-Flash-Filetrans 和 Fun-ASR 系列模型，参见[模型可用性](/developer-guides/speech/speech-to-text-models#全部模型)。                                                                                                                         |
| file\_urls     | list\[str] | -       | 是        | 音频/视频文件 URL（HTTP/HTTPS），每次请求最多 100 个。                                                                                                                                                                                                              |
| vocabulary\_id | str        | -       | 否        | 预编译热词列表 ID。需预先调用创建热词列表接口生成，识别时传入该 ID 即可使用列表中的热词。适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景。参见[预编译热词](/developer-guides/speech/improve-recognition-accuracy#预编译热词)。                                                                                                |
| vocabulary     | dict       | -       | 否        | 即时热词。以键值对形式传入，键为热词文本（`str`），值为热词权重（`int`），无需预先创建热词列表。权重取值范围为 \[1, 5] 或 50：取 50 时为超级热词。与预编译热词同时配置时，仅即时热词生效。参见[即时热词](/developer-guides/speech/improve-recognition-accuracy#即时热词)。<br /><br />仅 `qwen-audio-3.0-asr-flash-filetrans` 支持即时热词。<br />示例： |

````python
from dashscope.audio.asr import Transcription
vocab = {"张三": 5, "李四": 5}
result = Transcription.async_call(
    model="qwen-audio-3.0-asr-flash-filetrans",
    vocabulary=vocab,
    file_urls=['{YOUR_AUDIO_URL}']
)
``` |
| channel_id             | list[int] | [0]          | 否 | 要识别的音轨索引（从 0 开始）。`[0]` = 第一条音轨，`[0, 1]` = 第一条和第二条。<Warning>每条音轨单独计费。</Warning> |
| special_word_filter    | str       | ------------ | 否 | 敏感词过滤配置。参见[敏感词过滤](#sensitive-word-filter)。                                     |
| diarization_enabled    | bool      | False        | 否 | 启用说话人分离（仅限单声道）。结果中包含 `speaker_id`。参见[识别结果](#recognition-result)。               |
| speaker_count          | int       | -            | 否 | 预期说话人数量（2-100）。仅在 `diarization_enabled` 为 true 时生效，默认自动检测。该参数仅作为算法引导，不保证精确匹配。  |
| language_hints         | list[str] | ["zh", "en"] | 否 | 语言代码。不设置时自动检测。参见[支持的语言](#supported-languages)。                                 |
| speech_noise_threshold | float     | -            | 否 | 语音噪声阈值。                                                                        |

<a id="sensitive-word-filter"></a>
### 敏感词过滤
默认情况下，[系统敏感词列表](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/%E7%99%BE%E7%82%BC%E6%95%8F%E6%84%9F%E8%AF%8D%E5%88%97%E8%A1%A8_20230716.words.txt)中的词会被替换为星号（`*`）。

通过 `special_word_filter`，您可以：

- **替换为 `*`**：匹配的词变为星号。
- **过滤掉**：匹配的词被移除。

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
````

字段说明：

- `filter_with_signed`（object，可选）：要替换为 `*` 的词。
  - 示例："Help me <u>test</u> this code" 变为 "Help me <u>\*\*\*\*</u> this code"
  - `word_list`：要替换的词列表。
- `filter_with_empty`（object，可选）：要移除的词。
  - 示例："Is the game about to <u>start</u>?" 变为 "Is the game about to?"
  - `word_list`：要移除的词列表。
- `system_reserved_filter`（boolean，可选，默认值：true）：启用系统过滤。为 true 时，[系统敏感词列表](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/%E7%99%BE%E7%82%BC%E6%95%8F%E6%84%9F%E8%AF%8D%E5%88%97%E8%A1%A8_20230716.words.txt)中的词会被替换为 `*`。

<a id="supported-languages" />

### 支持的语言

各模型支持的语言代码：

- **qwen-audio-3.0-asr-flash-filetrans, fun-asr, fun-asr-2025-11-07**：
  - `zh`：中文
  - `en`：英文
  - `ja`：日语
- **fun-asr-2025-08-25**：
  - `zh`：中文
  - `en`：英文
- **fun-asr-mtl, fun-asr-mtl-2025-08-25**：
  - `zh`：中文
  - `en`：英文
  - `ja`：日语
  - `ko`：韩语
  - `vi`：越南语
  - `id`：印尼语
  - `th`：泰语
  - `ms`：马来语
  - `tl`：菲律宾语
  - `ar`：阿拉伯语
  - `hi`：印地语
  - `bg`：保加利亚语
  - `hr`：克罗地亚语
  - `cs`：捷克语
  - `da`：丹麦语
  - `nl`：荷兰语
  - `et`：爱沙尼亚语
  - `fi`：芬兰语
  - `el`：希腊语
  - `hu`：匈牙利语
  - `ga`：爱尔兰语
  - `lv`：拉脱维亚语
  - `lt`：立陶宛语
  - `mt`：马耳他语
  - `pl`：波兰语
  - `pt`：葡萄牙语
  - `ro`：罗马尼亚语
  - `sk`：斯洛伐克语
  - `sl`：斯洛文尼亚语
  - `sv`：瑞典语

## 响应结果

### TranscriptionResponse

`TranscriptionResponse` 包含任务信息（`task_id`、`task_status`）和 `output` 中的结果。参见 [TranscriptionOutput](#transcriptionoutput)。

<Accordion title="点击查看 TranscriptionResponse 结构示例">
  <Tabs>
    <Tab title="PENDING 状态">
      ```json
      {
        "status_code": 200,
        "request_id": "251aceab-a6aa-9fc4-b7f7-0cc6d3e2a9f3",
        "code": null,
        "message": "",
        "output": {
          "task_id": "7d0a58a3-1dbe-4de9-8cff-5f48213128b0",
          "task_status": "PENDING",
          "submit_time": "2025-02-13 16:55:08.573",
          "scheduled_time": "2025-02-13 16:55:08.592",
          "task_metrics": {
            "TOTAL": 2,
            "SUCCEEDED": 0,
            "FAILED": 0
          }
        },
        "usage": null
      }
      ```
    </Tab>

    <Tab title="RUNNING 状态">
      ```json
      {
        "status_code": 200,
        "request_id": "d9d530f1-853c-9848-a5f1-f5de59086ff7",
        "code": null,
        "message": "",
        "output": {
          "task_id": "6351feef-9694-45d2-9d32-63454f2ffb8d",
          "task_status": "RUNNING",
          "submit_time": "2025-02-13 17:31:20.681",
          "scheduled_time": "2025-02-13 17:31:20.703",
          "task_metrics": {
            "TOTAL": 2,
            "SUCCEEDED": 1,
            "FAILED": 0
          }
        },
        "usage": null
      }
      ```
    </Tab>

    <Tab title="SUCCEEDED 状态">
      ```json
      {
        "status_code": 200,
        "request_id": "16668704-6702-9e03-8ab7-a32a5d7bb095",
        "code": null,
        "message": "",
        "output": {
          "task_id": "6351feef-9694-45d2-9d32-63454f2ffb8d",
          "task_status": "SUCCEEDED",
          "submit_time": "2025-02-13 17:31:20.681",
          "scheduled_time": "2025-02-13 17:31:20.703",
          "end_time": "2025-02-13 17:31:21.867",
          "results": [
            {
              "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
              "transcription_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/prod/paraformer-v2/...",
              "subtask_status": "SUCCEEDED"
            },
            {
              "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav",
              "transcription_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/prod/paraformer-v2/...",
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
    </Tab>

    <Tab title="FAILED 状态">
      ```json
      {
        "status_code": 200,
        "request_id": "16668704-6702-9e03-8ab7-a32a5d7bb095",
        "code": null,
        "message": "",
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
        },
        "usage": {
          "duration": 9
        }
      }
      ```
    </Tab>
  </Tabs>
</Accordion>

关键参数：

| **参数**             | **说明**                                                                                                      |
| ------------------ | ----------------------------------------------------------------------------------------------------------- |
| status\_code       | HTTP 状态码。                                                                                                   |
| code               | 忽略顶层 `code`，请检查 `output.results[].code` 获取错误信息。                                                             |
| message            | 忽略顶层 `message`，请检查 `output.results[].message` 获取错误信息。                                                       |
| task\_id           | 任务 ID。                                                                                                      |
| task\_status       | 任务状态：`PENDING`、`RUNNING`、`SUCCEEDED`、`FAILED`。只要有一个子任务成功，任务状态即为 `SUCCEEDED`。请通过 `subtask_status` 查看各子任务的结果。 |
| results            | 子任务结果。                                                                                                      |
| subtask\_status    | 子任务状态：`PENDING`、`RUNNING`、`SUCCEEDED`、`FAILED`。                                                             |
| file\_url          | 音频文件 URL。                                                                                                   |
| transcription\_url | 结果 URL（JSON 文件），可通过 HTTP 下载或读取。参见[识别结果](#recognition-result)。                                               |

### TranscriptionOutput

`TranscriptionOutput` 是 [TranscriptionResponse](#transcriptionresponse) 的 `output` 属性。

<Accordion title="点击查看 TranscriptionOutput 结构示例">
  <Tabs>
    <Tab title="PENDING 状态">
      ```json
      {
        "task_id": "f2f7c2fa-0cd9-4bb2-a283-27b26ee4bb67",
        "task_status": "PENDING",
        "submit_time": "2025-02-13 17:59:27.754",
        "scheduled_time": "2025-02-13 17:59:27.789",
        "task_metrics": {
          "TOTAL": 2,
          "SUCCEEDED": 0,
          "FAILED": 0
        }
      }
      ```
    </Tab>

    <Tab title="RUNNING 状态">
      ```json
      {
        "task_id": "f2f7c2fa-0cd9-4bb2-a283-27b26ee4bb67",
        "task_status": "RUNNING",
        "submit_time": "2025-02-13 17:59:27.754",
        "scheduled_time": "2025-02-13 17:59:27.789",
        "task_metrics": {
          "TOTAL": 2,
          "SUCCEEDED": 0,
          "FAILED": 0
        }
      }
      ```
    </Tab>

    <Tab title="SUCCEEDED 状态">
      ```json
      {
        "task_id": "f2f7c2fa-0cd9-4bb2-a283-27b26ee4bb67",
        "task_status": "SUCCEEDED",
        "submit_time": "2025-02-13 17:59:27.754",
        "scheduled_time": "2025-02-13 17:59:27.789",
        "end_time": "2025-02-13 17:59:28.828",
        "results": [
          {
            "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
            "transcription_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/prod/paraformer-v2/...",
            "subtask_status": "SUCCEEDED"
          },
          {
            "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav",
            "transcription_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/prod/paraformer-v2/...",
            "subtask_status": "SUCCEEDED"
          }
        ],
        "task_metrics": {
          "TOTAL": 2,
          "SUCCEEDED": 2,
          "FAILED": 0
        }
      }
      ```
    </Tab>

    <Tab title="FAILED 状态">
      `code` 和 `message` 仅在出错时出现。

      ```json
      {
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
      ```
    </Tab>
  </Tabs>
</Accordion>

关键参数：

| **参数**             | **说明**                                                                                                      |
| ------------------ | ----------------------------------------------------------------------------------------------------------- |
| code               | 错误码。                                                                                                        |
| message            | 错误信息。                                                                                                       |
| task\_id           | 任务 ID。                                                                                                      |
| task\_status       | 任务状态：`PENDING`、`RUNNING`、`SUCCEEDED`、`FAILED`。只要有一个子任务成功，任务状态即为 `SUCCEEDED`。请通过 `subtask_status` 查看各子任务的结果。 |
| results            | 子任务结果。                                                                                                      |
| subtask\_status    | 子任务状态：`PENDING`、`RUNNING`、`SUCCEEDED`、`FAILED`。                                                             |
| file\_url          | 音频文件 URL。                                                                                                   |
| transcription\_url | 结果 URL（JSON 文件），可通过 HTTP 下载或读取。参见[识别结果](#recognition-result)。                                               |

<a id="recognition-result" />

### 识别结果

结果为 JSON 文件。

<Accordion title="点击查看识别结果示例">
  ```json
  {
    "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
    "properties": {
      "audio_format": "pcm_s16le",
      "channels": [
        0
      ],
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
    `speaker_id` 仅在启用说话人分离时出现。
  </Note>
</Accordion>

关键参数：

| **参数**                               | **类型**          | **说明**                                                          |
| ------------------------------------ | --------------- | --------------------------------------------------------------- |
| audio\_format                        | string          | 音频格式。                                                           |
| channels                             | array\[integer] | 音轨索引。`[0]` = 单音轨，`[0, 1]` = 双音轨。                                |
| original\_sampling\_rate             | integer         | 采样率（Hz）。                                                        |
| original\_duration\_in\_milliseconds | integer         | 音频时长（毫秒）。                                                       |
| channel\_id                          | integer         | 音轨索引（从 0 开始）。                                                   |
| content\_duration\_in\_milliseconds  | integer         | 语音时长（毫秒）。<Warning>仅语音部分会被转写和计费，非语音部分不计入。语音时长通常短于音频时长。</Warning> |
| transcripts                          | string          | 段落级文本。                                                          |
| sentences                            | array           | 句子级结果。                                                          |
| words                                | array           | 词级结果。                                                           |
| begin\_time                          | integer         | 开始时间（毫秒）。                                                       |
| end\_time                            | integer         | 结束时间（毫秒）。                                                       |
| text                                 | string          | 转写文本。                                                           |
| speaker\_id                          | integer         | 说话人索引（从 0 开始），仅在启用说话人分离时出现。                                     |
| punctuation                          | string          | 该词之后预测的标点符号。                                                    |

<a id="transcription-class" />

## Transcription 类

通过 `from dashscope.audio.asr import Transcription` 导入。

| **方法**      | **签名**                                                                                                                                                                     | **说明**                                                                               |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| async\_call | `@classmethod def async_call(cls, model: str, file_urls: List[str], phrase_id: str = None, api_key: str = None, workspace: str = None, **kwargs) -> TranscriptionResponse` | 提交识别任务。                                                                              |
| wait        | `@classmethod def wait(cls, task: Union[str, TranscriptionResponse], api_key: str = None, workspace: str = None, **kwargs) -> TranscriptionResponse`                       | 阻塞等待直到完成（`SUCCEEDED` 或 `FAILED`）。返回 [TranscriptionResponse](#transcriptionresponse)。 |
| fetch       | `@classmethod def fetch(cls, task: Union[str, TranscriptionResponse], api_key: str = None, workspace: str = None, **kwargs) -> TranscriptionResponse`                      | 查询任务状态。返回 [TranscriptionResponse](#transcriptionresponse)。                           |

## 常见问题

### 功能特性

<AccordionGroup>
  <Accordion title="是否支持Base64编码方式的音频？">
    不支持。Fun-ASR 非实时语音识别仅支持公网可访问的 HTTP/HTTPS URL，不支持本地文件上传或 Base64 编码格式。
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
