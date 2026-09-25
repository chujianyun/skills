> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Paraformer 录音文件识别 RESTful API — 创建任务

> 提交 Paraformer 录音文件识别异步任务

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

## 模型概览

| 模型名               | 推荐程度 | 适用场景                         |
| ----------------- | ---- | ---------------------------- |
| paraformer-v2     | 推荐   | 通用多语言识别，支持 zh/en/ja/ko/yue 等 |
| paraformer-8k-v2  | 推荐   | 8 kHz 采样率音频（如电话录音）           |
| paraformer-v1     | —    | 上一代通用模型                      |
| paraformer-8k-v1  | —    | 上一代 8 kHz 模型                 |
| paraformer-mtl-v1 | —    | 上一代多语言模型                     |

## 输入约束

- 音频 / 视频文件必须通过 **HTTP/HTTPS 公网 URL** 提供，不支持 Base64 编码或本地文件路径。
- 单次请求仅支持 **1 个 URL**。
- 单个文件大小不超过 **2 GB**，时长不超过 **12 小时**。
- 支持格式：aac、amr、avi、flac、flv、m4a、mkv、mov、mp3、mp4、mpeg、ogg、opus、wav、webm、wma、wmv。

<Note>
  如需使用 OSS 内网地址（`oss://` 前缀），须在请求头中添加 `X-DashScope-OssResourceResolve: enable`，并确保已授权 DashScope 访问对应 Bucket。临时 URL 有效期建议设置为 48 小时以上，**不建议在生产环境使用临时 URL**。
</Note>

## 异步流程

1. 调用本接口提交任务，响应中包含 `task_id`。
2. 使用 `task_id` 轮询[查询结果接口](/api-reference/speech-recognition/paraformer-asr-file/query-result)，直至 `task_status` 为 `SUCCEEDED` 或 `FAILED`。

## 识别结果说明

任务成功后，每个文件对应一个 `transcription_url`（有效期 **24 小时**），请及时下载。下载内容为 JSON 文件，以下示例展示了所有可能出现的字段（`speaker_id` 仅在启用说话人分离时返回）：

```json
{
  "file_url": "https://example.com/audio.wav",
  "properties": {
    "audio_format": "wav",
    "channels": [0],
    "original_sampling_rate": 16000,
    "original_duration_in_milliseconds": 3680
  },
  "transcripts": [
    {
      "channel_id": 0,
      "content_duration_in_milliseconds": 2640,
      "text": "北京的天气。",
      "sentences": [
        {
          "begin_time": 100,
          "end_time": 1380,
          "text": "北京的天气。",
          "words": [
            {
              "begin_time": 100,
              "end_time": 460,
              "text": "北京",
              "punctuation": "的"
            }
          ],
          "speaker_id": "spk0"
        }
      ]
    }
  ]
}
```

**字段说明**

| 字段                                               | 类型      | 说明                                   |
| ------------------------------------------------ | ------- | ------------------------------------ |
| `file_url`                                       | string  | 对应的音频文件 URL（与请求中的 URL 一致）            |
| `properties.audio_format`                        | string  | 音频格式                                 |
| `properties.channels`                            | array   | 识别的音轨索引列表                            |
| `properties.original_sampling_rate`              | integer | 原始采样率（Hz）                            |
| `properties.original_duration_in_milliseconds`   | integer | 音频总时长（毫秒）                            |
| `transcripts[].channel_id`                       | integer | 音轨索引                                 |
| `transcripts[].content_duration_in_milliseconds` | integer | 有效语音时长（毫秒），不含静音片段                    |
| `transcripts[].text`                             | string  | 完整识别文本                               |
| `transcripts[].sentences[].begin_time`           | integer | 句子开始时间（毫秒）                           |
| `transcripts[].sentences[].end_time`             | integer | 句子结束时间（毫秒）                           |
| `transcripts[].sentences[].text`                 | string  | 句子文本                                 |
| `transcripts[].sentences[].words[].begin_time`   | integer | 词开始时间（毫秒）                            |
| `transcripts[].sentences[].words[].end_time`     | integer | 词结束时间（毫秒）                            |
| `transcripts[].sentences[].words[].text`         | string  | 词文本                                  |
| `transcripts[].sentences[].words[].punctuation`  | string  | 该词后的标点符号                             |
| `transcripts[].sentences[].speaker_id`           | string  | 说话人 ID（启用 `diarization_enabled` 时返回） |

## 常见问题

### 提交后如何获取结果？

任务提交后返回 `task_id`，需轮询[查询结果接口](/api-reference/speech-recognition/paraformer-asr-file/query-result)。建议每隔 1 秒查询一次，避免过于频繁。

### 多文件中部分失败如何处理？

当任务包含多个文件时，只要有一个文件成功，整体 `task_status` 即为 `SUCCEEDED`。需检查每个 `results[].subtask_status` 确认各子任务状态，失败条目会返回 `code` 和 `message` 字段。

### 音频文件无法下载报错

错误码 `InvalidFile.DownloadFailed` 表示服务无法访问音频 URL。请确认：

- URL 是否公网可访问
- 临时签名 URL 是否已过期
- 文件大小是否超过 2 GB

### 多音轨计费说明

`channel_id` 中每个音轨单独计费。例如，`[0, 1]` 对一个文件产生两次计费。

## 错误码

大模型服务通用状态码请查阅[错误信息](/api-reference/preparation/error-messages)。

## OpenAPI

````yaml post /services/audio/asr/transcription
openapi: 3.1.0
info:
  title: Paraformer 录音文件识别 API
  description: Paraformer 录音文件识别 RESTful API。采用异步任务模式——先提交任务，再轮询查询结果。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: DashScope API 服务器
security:
  - BearerAuth: []
paths:
  /services/audio/asr/transcription:
    post:
      operationId: createParaformerAsrTask
      summary: 提交识别任务
      description: 提交录音文件识别异步任务。任务提交后返回 `task_id`，使用 `GET /tasks/{task_id}` 轮询结果。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 异步任务提交时必须设置为 `enable`。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/AsrTaskRequest"
      responses:
        "200":
          description: 任务提交成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AsyncTaskSubmitResponse"
              example:
                output:
                  task_status: PENDING
                  task_id: c2e5d63b-96e1-4607-bb91-xxxxxxxxxxxx
                request_id: 77ae55ae-be17-97b8-9942-xxxxxxxxxxxx
        "400":
          description: 请求参数无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription' \
              --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
              --header 'Content-Type: application/json' \
              --header 'X-DashScope-Async: enable' \
              --data '{
                "model": "paraformer-v2",
                "input": {
                  "file_urls": [
                    "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
                    "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav"
                  ]
                },
                "parameters": {
                  "language_hints": ["zh", "en"]
                }
              }'
        - lang: python
          label: Python
          source: |-
            import os
            import requests
            import time

            api_key = os.environ.get("DASHSCOPE_API_KEY")
            file_urls = [
              "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
              "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav"
            ]

            def submit_task(apikey, file_urls):
              url = "https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription"
              headers = {
                "Authorization": f"Bearer {apikey}",
                "Content-Type": "application/json",
                "X-DashScope-Async": "enable"
              }
              body = {
                "model": "paraformer-v2",
                "input": {
                  "file_urls": file_urls
                },
                "parameters": {
                  "language_hints": ["zh", "en"]
                }
              }
              response = requests.post(url, headers=headers, json=body)
              return response.json()["output"]["task_id"]

            def wait_for_complete(task_id):
              pending = True
              url = "https://dashscope.aliyuncs.com/api/v1/tasks/" + task_id
              headers = {
                "Authorization": f"Bearer {api_key}"
              }
              while pending:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                  status = response.json()["output"]["task_status"]
                  if status == "SUCCEEDED":
                    print("task succeeded!")
                    pending = False
                    return response.json()["output"]["results"]
                  elif status == "RUNNING" or status == "PENDING":
                    pass
                  else:
                    print("task failed!")
                    pending = False
                else:
                  print("query failed!")
                  pending = False
                print(response.json())
                time.sleep(1)

            task_id = submit_task(apikey=api_key, file_urls=file_urls)
            print("task_id: ", task_id)
            result = wait_for_complete(task_id)
            print("transcription result: ", result)
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    AsrTaskRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。可用模型：`paraformer-v2`（推荐，支持多语言）、`paraformer-8k-v2`（8kHz 采样率优化）、`paraformer-v1`、`paraformer-8k-v1`、`paraformer-mtl-v1`（多语言）。
          enum:
            - paraformer-v2
            - paraformer-8k-v2
            - paraformer-v1
            - paraformer-8k-v1
            - paraformer-mtl-v1
          example: paraformer-v2
        input:
          type: object
          required:
            - file_urls
          description: 识别任务的输入数据。
          properties:
            file_urls:
              type: array
              items:
                type: string
                format: uri
              description: 音频或视频文件的 HTTP/HTTPS 公网访问 URL 列表。不支持 Base64 编码或本地文件。单次最多 100 个 URL。
              example:
                - https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav
        parameters:
          type: object
          description: 识别参数（可选）。
          properties:
            vocabulary_id:
              type: string
              description: 热词 ID。将自定义热词应用于当前任务。参见[自定义热词](/developer-guides/speech/improve-recognition-accuracy)。
            resource_id:
              type: string
              description: 定制模型的资源 ID。与 `resource_type` 配合使用。
            resource_type:
              type: string
              description: 定制资源类型，固定值 `asr_resource`。
              enum:
                - asr_resource
            channel_id:
              type: array
              items:
                type: integer
              description: 多音轨文件中要识别的音轨索引（从 0 开始）。例如 `[0]` 识别第一音轨，`[0, 1]` 识别前两个音轨。**注意：每个音轨单独计费。**
              default:
                - 0
              example:
                - 0
            disfluency_removal_enabled:
              type: boolean
              description: 是否开启去除语气词功能（如「嗯」「啊」等）。默认 `false`。
              default: false
            timestamp_alignment_enabled:
              type: boolean
              description: 是否开启时间戳校准功能。启用后，识别结果与语音播放同步。默认 `false`。
              default: false
            special_word_filter:
              type: string
              description: 敏感词处理配置（JSON 字符串）。支持 `filter_with_signed`（替换为等长星号）、`filter_with_empty`（删除）、`system_reserved_filter`（使用系统预设规则）。
            language_hints:
              type: array
              items:
                type: string
              description: 识别语言提示。未设置时模型自动检测语言。`paraformer-v2` 支持 `zh`、`en`、`ja`、`ko`、`yue` 等。
              example:
                - zh
                - en
            diarization_enabled:
              type: boolean
              description: 是否开启说话人分离。启用后，结果中包含 `speaker_id` 字段。仅支持单声道音频。默认 `false`。
              default: false
            speaker_count:
              type: integer
              description: 说话人数量参考值（2 到 100）。仅在 `diarization_enabled` 为 `true` 时生效。默认自动检测。
              minimum: 2
              maximum: 100
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交的响应结果。
      properties:
        request_id:
          type: string
          description: 请求的唯一标识符。
          example: 77ae55ae-be17-97b8-9942-xxxxxxxxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，用于轮询 `GET /tasks/{task_id}`。
              example: c2e5d63b-96e1-4607-bb91-xxxxxxxxxxxx
            task_status:
              type: string
              description: 任务初始状态，通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
    AsrTaskStatusResponse:
      type: object
      description: 查询录音文件识别任务状态的响应结果。
      properties:
        request_id:
          type: string
          description: 请求的唯一标识符。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。
            task_status:
              type: string
              description: 当前任务状态。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
            submit_time:
              type: string
              description: 任务提交时间。
            scheduled_time:
              type: string
              description: 任务调度时间。
            end_time:
              type: string
              description: 任务结束时间。
            results:
              type: array
              description: 各子任务识别结果列表。
              items:
                type: object
                properties:
                  file_url:
                    type: string
                    description: 对应的音频文件 URL。
                  transcription_url:
                    type: string
                    description: 识别结果 JSON 文件的下载链接，**有效期 24 小时**。仅在 `subtask_status` 为 `SUCCEEDED` 时返回。
                  subtask_status:
                    type: string
                    description: 子任务状态：`SUCCEEDED` 或 `FAILED`。
                    enum:
                      - SUCCEEDED
                      - FAILED
                  code:
                    type: string
                    description: 错误码。仅在 `subtask_status` 为 `FAILED` 时返回。
                  message:
                    type: string
                    description: 错误信息。仅在 `subtask_status` 为 `FAILED` 时返回。
            task_metrics:
              type: object
              description: 任务结果统计。
              properties:
                TOTAL:
                  type: integer
                  description: 子任务总数。
                SUCCEEDED:
                  type: integer
                  description: 成功子任务数。
                FAILED:
                  type: integer
                  description: 失败子任务数。
        usage:
          type: object
          description: 用量统计（仅任务成功时返回）。
          properties:
            duration:
              type: integer
              description: 识别的语音总时长（秒）。仅计算语音片段，非语音片段不计费。
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求的唯一标识符。
        code:
          type: string
          description: 错误代码。
          example: InvalidParameter
        message:
          type: string
          description: 错误信息。
          example: Invalid model name
````
