> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Paraformer 录音文件识别 Python SDK

> 使用DashScope Python SDK调用Paraformer模型，对录音文件进行异步转写识别。

## 前提条件

**获取API Key**：请[获取API Key](/api-reference/preparation/api-key)，并[配置API Key到环境变量](/api-reference/preparation/export-api-key-env)，避免在代码中硬编码：

```bash
export DASHSCOPE_API_KEY="REDACTED"
```

<Note>
  如需在代码中临时授权，也可使用以下方式设置API Key，但请注意该方式存在泄露风险，不建议在生产环境使用：

  ```python
  import dashscope
  dashscope.api_key = "REDACTED"
  ```
</Note>

**安装Python SDK**：请[安装最新版DashScope Python SDK](/api-reference/preparation/install-sdk)，或运行：

```bash
pip install dashscope
```

## 模型列表

### v2模型（推荐）

| 模型名称             | 支持语言                        | 采样率  | 标点预测 | 逆文本规范化 | 自定义热词 |
| ---------------- | --------------------------- | ---- | ---- | ------ | ----- |
| paraformer-v2    | 中文（含多种方言）、英语、日语、韩语、德语、法语、俄语 | 不限   | 支持   | 支持     | 支持    |
| paraformer-8k-v2 | 中文                          | 8kHz | 支持   | 支持     | 支持    |

### v1模型

| 模型名称              | 支持语言                                       | 采样率      | 标点预测 | 逆文本规范化 | 自定义热词 |
| ----------------- | ------------------------------------------ | -------- | ---- | ------ | ----- |
| paraformer-v1     | 中文、英语                                      | 不限       | 支持   | 支持     | 不支持   |
| paraformer-8k-v1  | 中文                                         | 8kHz     | 支持   | 支持     | 不支持   |
| paraformer-mtl-v1 | 中文（含多种方言）、英语、日语、韩语、西班牙语、印尼语、法语、德语、意大利语、马来语 | 16kHz及以上 | 支持   | 支持     | 不支持   |

## 约束

- **不支持本地文件上传**，也不支持Base64编码格式。输入音频必须为公网可访问的HTTP/HTTPS URL，例如 `https://your-domain.com/file.mp3`。
- **SDK不支持 `oss://` 前缀的URL**。RESTful API支持 `oss://` 前缀URL，但下载链接有效期仅48小时，不建议在生产环境使用。
- 每次请求最多支持100个URL。
- 支持的音频格式：aac、amr、avi、flac、flv、m4a、mkv、mov、mp3、mp4、mpeg、ogg、opus、wav、webm、wma、wmv。
- 采样率要求：
  - paraformer-v2：不限
  - paraformer-8k-v2、paraformer-8k-v1：仅支持8kHz
  - paraformer-mtl-v1：仅支持16kHz及以上
  - paraformer-v1：不限
- 单个文件最大2GB，最长12小时。
- 每次请求最多100个文件。

## 快速开始

### 异步提交任务并同步等待结果

使用 `async_call()` 提交转写任务，再用 `wait()` 同步等待任务完成：

```python
from http import HTTPStatus
from dashscope.audio.asr import Transcription
import json

# 若没有将API Key配置到环境变量中，需将下面这行代码注释放开，并将apiKey替换为自己的API Key
# import dashscope
# dashscope.api_key = "apiKey"

task_response = Transcription.async_call(
  model='paraformer-v2',
  file_urls=[
    'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav',
    'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav'
  ],
  language_hints=['zh', 'en']  # "language_hints"只支持paraformer-v2模型
)

transcribe_response = Transcription.wait(task=task_response.output.task_id)
if transcribe_response.status_code == HTTPStatus.OK:
  print(json.dumps(transcribe_response.output, indent=4, ensure_ascii=False))
  print('transcription done!')
```

<Note>
  任务提交后会进入PENDING（排队）状态，排队时长取决于当前队列长度和音频时长，通常在几分钟内完成。转写结果及下载链接有效期为24小时。
</Note>

### 异步提交任务并轮询查询结果

使用 `async_call()` 提交任务，再用 `fetch()` 循环轮询任务状态：

```python
from http import HTTPStatus
from dashscope.audio.asr import Transcription
import json

# 若没有将API Key配置到环境变量中，需将下面这行代码注释放开，并将apiKey替换为自己的API Key
# import dashscope
# dashscope.api_key = "apiKey"

transcribe_response = Transcription.async_call(
  model='paraformer-v2',
  file_urls=[
    'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav',
    'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav'
  ],
  language_hints=['zh', 'en']  # "language_hints"只支持paraformer-v2模型
)

while True:
  if transcribe_response.output.task_status == 'SUCCEEDED' or transcribe_response.output.task_status == 'FAILED':
    break
  transcribe_response = Transcription.fetch(task=transcribe_response.output.task_id)

if transcribe_response.status_code == HTTPStatus.OK:
  print(json.dumps(transcribe_response.output, indent=4, ensure_ascii=False))
  print('transcription done!')
```

<Note>
  任务提交后会进入PENDING（排队）状态，排队时长取决于当前队列长度和音频时长，通常在几分钟内完成。转写结果及下载链接有效期为24小时。
</Note>

## 请求参数

以下参数通过 `async_call()` 方法传入：

| 参数                            | 类型         | 默认值            | 是否必填 | 说明                                          |
| ----------------------------- | ---------- | -------------- | ---- | ------------------------------------------- |
| `model`                       | str        | -              | 必填   | Paraformer模型名称，参见模型列表                       |
| `file_urls`                   | list\[str] | -              | 必填   | 音视频文件的公网URL列表，最多100个                        |
| `vocabulary_id`               | str        | -              | 可选   | 热词表ID（最新版），仅支持v2模型                          |
| `phrase_id`                   | str        | -              | 可选   | 热词表ID（v1版），不适用于v2及以上模型                      |
| `channel_id`                  | list\[int] | \[0]           | 可选   | 音轨索引列表（从0开始），每条音轨单独计费                       |
| `disfluency_removal_enabled`  | bool       | False          | 可选   | 是否过滤语气词（如"嗯"、"啊"等）                          |
| `timestamp_alignment_enabled` | bool       | False          | 可选   | 是否开启时间戳对齐，解决识别结果与音频不同步的问题                   |
| `special_word_filter`         | str        | -              | 可选   | 敏感词过滤配置（JSON 字符串），支持自定义替换规则                 |
| `language_hints`              | list\[str] | `["zh", "en"]` | 可选   | 语言提示列表（如 `['zh', 'en']`），仅支持paraformer-v2模型 |
| `diarization_enabled`         | bool       | False          | 可选   | 是否开启说话人分离                                   |
| `speaker_count`               | int        | -              | 可选   | 说话人数量，与 `diarization_enabled` 配合使用          |

## 响应结果

### TranscriptionOutput字段

| 字段                            | 类型     | 说明                                    |
| ----------------------------- | ------ | ------------------------------------- |
| `task_id`                     | string | 任务ID                                  |
| `task_status`                 | string | 任务状态：PENDING、RUNNING、SUCCEEDED、FAILED |
| `results`                     | array  | 各文件的转写结果列表                            |
| `results[].file_url`          | string | 对应的输入音频URL                            |
| `results[].transcription_url` | string | 转写结果JSON文件的下载URL（有效期24小时）             |
| `results[].subtask_status`    | string | 该文件的子任务状态：SUCCEEDED或FAILED            |
| `results[].code`              | string | 子任务失败时的错误码                            |
| `results[].message`           | string | 子任务失败时的错误描述                           |

<Note>
  当一次请求包含多个文件时，只要有任意一个子任务成功，整体 `task_status` 即为SUCCEEDED。请通过 `subtask_status` 判断每个文件的识别结果。
</Note>

### 识别结果说明

`transcription_url` 指向的JSON文件结构如下：

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
      "text": "Hello world, 这里是阿里巴巴语音实验室。",
      "sentences": [
        {
          "begin_time": 100,
          "end_time": 3820,
          "text": "Hello world, 这里是阿里巴巴语音实验室。",
          "sentence_id": 1,
          "speaker_id": 0,
          "words": [
            {"begin_time": 100, "end_time": 596, "text": "Hello ", "punctuation": ""},
            {"begin_time": 596, "end_time": 844, "text": "world", "punctuation": ", "}
          ]
        }
      ]
    }
  ]
}
```

识别结果字段说明：

| 参数                                  | 类型              | 说明                       |
| ----------------------------------- | --------------- | ------------------------ |
| `audio_format`                      | string          | 源音频格式                    |
| `channels`                          | array\[integer] | 音轨索引列表                   |
| `original_sampling_rate`            | integer         | 采样率（Hz）                  |
| `original_duration_in_milliseconds` | integer         | 原始音频时长（毫秒）               |
| `channel_id`                        | integer         | 该转写结果对应的音轨索引             |
| `content_duration_in_milliseconds`  | integer         | 被判定为语音内容的时长（毫秒），按此时长计费   |
| `text`                              | string          | 段落级别转写结果                 |
| `sentences`                         | array           | 句子级别转写结果列表               |
| `words`                             | array           | 词级别转写结果列表                |
| `begin_time`                        | integer         | 开始时间戳（毫秒）                |
| `end_time`                          | integer         | 结束时间戳（毫秒）                |
| `speaker_id`                        | integer         | 说话人索引（从0开始），仅在开启说话人分离时返回 |
| `punctuation`                       | string          | 词后标点符号                   |

## 关键接口

### 核心类（Transcription）

```python
from dashscope.audio.asr import Transcription
```

**async\_call** — 异步提交转写任务：

```python
@classmethod
def async_call(
  cls,
  model: str,
  file_urls: list,
  phrase_id: str = None,
  api_key: str = None,
  workspace: str = None,
  **kwargs
) -> TranscriptionResponse
```

**wait** — 同步等待任务完成：

```python
@classmethod
def wait(
  cls,
  task,  # str或TranscriptionResponse
  api_key: str = None,
  workspace: str = None,
  **kwargs
) -> TranscriptionResponse
```

**fetch** — 查询当前任务状态（不阻塞）：

```python
@classmethod
def fetch(
  cls,
  task,  # str或TranscriptionResponse
  api_key: str = None,
  workspace: str = None,
  **kwargs
) -> TranscriptionResponse
```

### 其他接口

支持批量查询24小时内的任务状态，以及取消PENDING状态的任务。详见管理异步任务相关文档。

## 错误码

详见[错误信息](/api-reference/preparation/error-messages)。

当一次请求包含多个文件时，部分文件失败不影响整体任务状态为SUCCEEDED。示例响应：

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
      "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/rich_text_exaple_1.wav",
      "code": "InvalidFile.DownloadFailed",
      "message": "The audio file cannot be downloaded.",
      "subtask_status": "FAILED"
    }
  ],
  "task_metrics": {"TOTAL": 2, "SUCCEEDED": 1, "FAILED": 1}
}
```

## 更多示例

更多完整代码示例请访问 [GitHub 代码示例仓库](https://github.com/aliyun/alibabacloud-bailian-speech-demo)。

## 常见问题

### 功能特性

<AccordionGroup>
  <Accordion title="是否支持Base64编码方式的音频？">
    不支持。Paraformer录音文件识别仅支持公网可访问的HTTP/HTTPS URL，不支持本地文件上传或Base64编码格式。
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
  <Accordion title="识别结果和语音播放不同步怎么办？">
    在请求参数中设置 `timestamp_alignment_enabled=True`，开启时间戳对齐功能，可解决识别结果与音频播放不同步的问题。
  </Accordion>

  <Accordion title="一直轮询不到结果？">
    可能是当前服务负载较高导致排队时间较长，请耐心等待。如有大规模并发需求，可通过 [GitHub 代码示例仓库](https://github.com/aliyun/alibabacloud-bailian-speech-demo) 联系我们申请扩容。
  </Accordion>

  <Accordion title="无法识别语音（无识别结果）是什么原因？">
    请按以下顺序排查：

    1. 检查音频格式是否在支持列表内（aac、mp3、wav等）。
    2. 检查音频采样率是否符合所用模型的要求（例如paraformer-8k-v2仅支持8kHz）。
    3. 使用paraformer-v2时，确认 `language_hints` 参数中包含了正确的语言代码。
    4. 若识别专业术语或特定词汇效果不佳，考虑使用自定义热词功能。
  </Accordion>
</AccordionGroup>

### 更多问题

如有其他问题，请访问 [GitHub 代码示例仓库](https://github.com/aliyun/alibabacloud-bailian-speech-demo) 提问或查阅已有解答。
