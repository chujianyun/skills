> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Fun-ASR 录音文件识别 Java SDK

> 录音文件转写 Java SDK

**使用指南**： 教程、代码示例和模型详情请参见[录音文件转写](/developer-guides/speech/asr)。

## 使用限制

**输入格式**：仅支持公开可访问的文件 URL（HTTP/HTTPS），不支持本地文件和 Base64 编码音频。

示例：`https://your-domain.com/file.mp3`

通过 `fileUrls` 参数设置文件 URL，每次请求最多 100 个 URL。

- **音频格式**：`aac`、`amr`、`avi`、`flac`、`flv`、`m4a`、`mkv`、`mov`、`mp3`、`mp4`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv`

<Warning>
  音视频格式变体众多，API 无法保证所有变体都能正确识别。请先测试您的文件，确认识别效果。
</Warning>

- **音频采样率**：不限
- **文件大小和时长**：最大 2 GB、12 小时。如果启用说话人分离功能，建议音频时长不超过 2 小时。更大文件请参见[预处理最佳实践](/developer-guides/speech/asr)。
- **批量大小**：每次请求最多 100 个文件 URL。
- **支持语言**： fun-asr 和 fun-asr-mtl（含所有版本）均支持中文、英语、日语、韩语等 30 种语言，详见[支持的语言](#支持的语言)。fun-asr-2025-08-25 仅支持中文和英文。

## 请求参数

通过 `TranscriptionParam` 构建器方法设置请求参数。

<Accordion title="点击查看示例">
  ```java
  TranscriptionParam param = TranscriptionParam.builder()
    .model("qwen-audio-3.0-asr-flash-filetrans")
    .fileUrls(
            Arrays.asList(
                    "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
                    "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav"))
    .build();
  ```
</Accordion>

| **参数**       | **类型**                | **默认值** | **是否必填** | **描述**                                                                                                                                                                                                                                               |
| ------------ | --------------------- | ------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| model        | String                | -       | 是        | 转写模型。支持 Qwen-Audio-3.0-ASR-Flash-Filetrans 和 Fun-ASR 系列模型，参见[支持的模型](/developer-guides/speech/speech-to-text-models#全部模型)。                                                                                                                            |
| fileUrls     | List\<String>         | -       | 是        | 待转写的音视频文件 URL 列表，支持 HTTP 和 HTTPS，每次请求最多 100 个 URL。                                                                                                                                                                                                   |
| vocabularyId | String                | -       | 否        | 预编译热词列表 ID。需预先调用创建热词列表接口生成，识别时传入该 ID 即可使用列表中的热词。适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景。参见[预编译热词](/developer-guides/speech/improve-recognition-accuracy#预编译热词)。                                                                                                  |
| vocabulary   | Map\<String, Integer> | -       | 否        | 即时热词。以键值对形式传入，键为热词文本，值为热词权重（取值 \[1, 5] 或 50，取 50 为超级热词）。与预编译热词同时配置时，仅即时热词生效。参见[即时热词](/developer-guides/speech/improve-recognition-accuracy#即时热词)。<br /><br />仅 `qwen-audio-3.0-asr-flash-filetrans` 支持即时热词。<br />通过 `parameter` 或 `parameters` 方法设置： |

````java
Map<String, Integer> vocab = new HashMap<>();
vocab.put("张三", 5);
vocab.put("李四", 5);
TranscriptionParam param = TranscriptionParam.builder()
  .model("qwen-audio-3.0-asr-flash-filetrans")
  .parameter("vocabulary", vocab)
  // 或：.parameters(Collections.singletonMap("vocabulary", vocab))
  .fileUrls(Arrays.asList("{YOUR_AUDIO_URL}"))
  .build();
``` |
| channelId          | List\<Integer\> | [0]   | 否 | 需要识别的音频声道索引（从 0 开始）。[0] 仅识别第一个声道；[0, 1] 识别两个声道。<Warning>每个声道单独计费。</Warning>                                               |
| specialWordFilter  | String          | ----- | 否 | 识别过程中需要过滤的敏感词。详见[敏感词过滤说明](#敏感词过滤说明)。                                                                                      |
| diarizationEnabled | Boolean         | false | 否 | 是否启用说话人分离（仅支持单声道音频）。启用后结果中包含 `speaker_id` 字段以区分说话人。参见[识别结果](#识别结果)。<Note>如果启用说话人分离功能，建议音频时长不超过 2 小时，否则可能导致识别失败或超时。</Note> |
| speakerCount       | Integer         | -     | 否 | 预期的说话人数量（2-100）。仅在 `diarizationEnabled` 为 true 时生效。该值用于指导算法，不保证输出的说话人数量完全一致。                                              |
| language_hints     | String[]        | -     | 否 | 语言代码。不设置则自动检测。参见[支持的语言](#支持的语言)。                                                                                          |
| apiKey             | String          | -     | 否 | API Key。如已设置环境变量则无需传入。                                                                                                    |

### 敏感词过滤说明

未设置 `specialWordFilter` 时，系统默认启用内置过滤（匹配 [千问AI平台敏感词列表](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/%E7%99%BE%E7%82%BC%E6%95%8F%E6%84%9F%E8%AF%8D%E5%88%97%E8%A1%A8_20230716.words.txt)（文件名为历史遗留）中的词将被替换为 `*`）。

设置后，可使用以下过滤策略：

- **替换为 `*`**：将匹配的词替换为等长的星号。
- **直接过滤**：从结果中删除匹配的词。

值为 JSON 字符串：

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

- `filter_with_signed`
  - 类型：object（可选）
  - 将匹配的词替换为等长的 `*`。
  - 示例："Help me test this piece of code" -> "Help me \*\*\*\* this piece of code"
  - 字段：`word_list`（需要替换的词数组）
- `filter_with_empty`
  - 类型：object（可选）
  - 从结果中删除匹配的词。
  - 示例："Is the game about to start?" -> "Is the game about to?"（过滤后结果可能形成语义不完整的句子）
  - 字段：`word_list`（需要删除的词数组）
- `system_reserved_filter`
  - 类型：boolean（默认值：true）
  - 启用系统预设的敏感词规则。为 true 时启用内置过滤（匹配 [千问AI平台敏感词列表](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/%E7%99%BE%E7%82%BC%E6%95%8F%E6%84%9F%E8%AF%8D%E5%88%97%E8%A1%A8_20230716.words.txt)（文件名为历史遗留）中的词将被替换为 `*`）。

### 支持的语言

各模型支持的语言代码：

- qwen-audio-3.0-asr-flash-filetrans、fun-asr、fun-asr-2025-11-07：
  - zh：中文
  - en：英语
  - ja：日语
  - ko：韩语
  - vi：越南语
  - th：泰语
  - id：印尼语
  - ms：马来语
  - tl：菲律宾语
  - hi：印地语
  - ar：阿拉伯语
  - fr：法语
  - de：德语
  - es：西班牙语
  - pt：葡萄牙语
  - ru：俄语
  - it：意大利语
  - nl：荷兰语
  - sv：瑞典语
  - da：丹麦语
  - fi：芬兰语
  - no：挪威语
  - el：希腊语
  - pl：波兰语
  - cs：捷克语
  - hu：匈牙利语
  - ro：罗马尼亚语
  - bg：保加利亚语
  - hr：克罗地亚语
  - sk：斯洛伐克语
- fun-asr-2025-08-25：
  - zh：中文
  - en：英文
- fun-asr-mtl、fun-asr-mtl-2025-08-25：
  - zh：中文
  - en：英语
  - ja：日语
  - ko：韩语
  - vi：越南语
  - th：泰语
  - id：印尼语
  - ms：马来语
  - tl：菲律宾语
  - hi：印地语
  - ar：阿拉伯语
  - fr：法语
  - de：德语
  - es：西班牙语
  - pt：葡萄牙语
  - ru：俄语
  - it：意大利语
  - nl：荷兰语
  - sv：瑞典语
  - da：丹麦语
  - fi：芬兰语
  - no：挪威语
  - el：希腊语
  - pl：波兰语
  - cs：捷克语
  - hu：匈牙利语
  - ro：罗马尼亚语
  - bg：保加利亚语
  - hr：克罗地亚语
  - sk：斯洛伐克语

<Note>
  通过 `TranscriptionParam` 的 `parameter` 或 `parameters` 方法设置 `language_hints`：

  <Tabs>
    <Tab title="使用 parameter 设置">
      ```java
      TranscriptionParam param = TranscriptionParam.builder()
        .model("qwen-audio-3.0-asr-flash-filetrans")
        .parameter("language_hints", new String[]{"zh", "en"})
        .build();
      ```
    </Tab>

    <Tab title="使用 parameters 设置">
      ```java
      TranscriptionParam param = TranscriptionParam.builder()
        .model("qwen-audio-3.0-asr-flash-filetrans")
        .parameters(Collections.singletonMap("language_hints", new String[]{"zh", "en"}))
        .build();
      ```
    </Tab>
  </Tabs>
</Note>

## 响应

<a id="任务结果-transcriptionresult" />

### 任务结果（`TranscriptionResult`）

`TranscriptionResult` 包含任务结果。

| **方法**                                              | **参数** | **返回值**                                                   | **描述**                                                                                                                                  |
| --------------------------------------------------- | ------ | --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `public String getRequestId()`                      | 无      | requestId                                                 | 获取请求 ID。                                                                                                                                |
| `public String getTaskId()`                         | 无      | taskId                                                    | 获取任务 ID。                                                                                                                                |
| `public TaskStatus getTaskStatus()`                 | 无      | `TaskStatus`                                              | 获取任务状态（`PENDING`、`RUNNING`、`SUCCEEDED` 或 `FAILED`）。<Note>包含多个子任务时，只要有一个子任务成功，整体状态即为 `SUCCEEDED`。请通过 `subtask_status` 查看每个子任务的状态。</Note> |
| `public List<TranscriptionTaskResult> getResults()` | 无      | [TranscriptionTaskResult](#子任务结果-transcriptiontaskresult) | 获取子任务结果列表。每个文件对应一个子任务。                                                                                                                  |
| `public JsonObject getOutput()`                     | 无      | JSON                                                      | 以 JSON 格式获取结果。参见 [JSON 输出示例](#json-输出示例)。                                                                                               |

#### JSON 输出示例

**成功示例**

<Note>
  `transcription_url` 的路径格式仅供参考，实际路径随模型和时间不同而异。
</Note>

```json
{
  "task_id":"0795ff8c-b666-4e91-bb8b-xxx",
  "task_status":"SUCCEEDED",
  "submit_time":"2025-02-13 16:12:09.109",
  "scheduled_time":"2025-02-13 16:12:09.128",
  "end_time":"2025-02-13 16:12:10.189",
  "results":[
    {
      "file_url":"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav",
      "transcription_url":"https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/prod/fun-asr/20250213/16%3A12/34604a7b-579a-4223-8797-5116a49b07ec-1.json?Expires=1739520730&OSSAccessKeyId=yourOSSAccessKeyId&Signature=tMqyH56oB5rDW9%2FFqD8Yo%2F3WaPk%3D",
      "subtask_status":"SUCCEEDED"
    },
    {
      "file_url":"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
      "transcription_url":"https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/prod/fun-asr/20250213/16%3A12/3baafe5f-d09d-46c6-8b01-724927670edb-1.json?Expires=1739520730&OSSAccessKeyId=yourOSSAccessKeyId&Signature=BF7vPxlsJN9hkJlY%2BLReezxOwK8%3D",
      "subtask_status":"SUCCEEDED"
    }
  ],
  "task_metrics":{
    "TOTAL":2,
    "SUCCEEDED":2,
    "FAILED":0
  }
}
```

**错误示例**

`code` 和 `message` 字段仅在出错时出现。

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
      "transcription_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/prod/fun-asr/20241216/xxxx",
      "subtask_status": "SUCCEEDED"
    },
    {
      "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/rich_text_exaple_1.wav",
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

<a id="子任务结果-transcriptiontaskresult" />

### 子任务结果（`TranscriptionTaskResult`）

`TranscriptionTaskResult` 包含单个文件的转写结果。

| **方法**                                 | **参数** | **返回值**      | **描述**                                                            |
| -------------------------------------- | ------ | ------------ | ----------------------------------------------------------------- |
| `public String getFileUrl()`           | 无      | 文件 URL       | 获取已识别文件的 URL。                                                     |
| `public String getTranscriptionUrl()`  | 无      | 结果 URL       | 获取转写结果 URL（有效期 24 小时）。结果为 JSON 文件，可通过 HTTP 下载或读取。参见[识别结果](#识别结果)。 |
| `public TaskStatus getSubTaskStatus()` | 无      | `TaskStatus` | 获取子任务状态（`PENDING`、`RUNNING`、`SUCCEEDED` 或 `FAILED`）。              |
| `public String getMessage()`           | 无      | 消息（可能为空）     | 获取错误详情。任务失败时请检查此字段。                                               |

### 识别结果

识别结果为 JSON 文件。

<Accordion title="点击查看识别结果示例">
  <Note>
    以下为启用说话人分离（diarizationEnabled=true）时的示例，结果中包含 `speaker_id` 字段。
  </Note>

  ```json
  {
    "file_url":"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
    "properties":{
      "audio_format":"pcm_s16le",
      "channels":[
        0
      ],
      "original_sampling_rate":16000,
      "original_duration_in_milliseconds":3834
    },
    "transcripts":[
      {
        "channel_id":0,
        "content_duration_in_milliseconds":3720,
        "text":"Hello world, this is Alibaba Speech Lab.",
        "sentences":[
          {
            "begin_time":100,
            "end_time":3820,
            "text":"Hello world, this is Alibaba Speech Lab.",
            "sentence_id":1,
            "speaker_id":0,
            "words":[
              {
                "begin_time":100,
                "end_time":596,
                "text":"Hello ",
                "punctuation":""
              },
              {
                "begin_time":596,
                "end_time":844,
                "text":"world",
                "punctuation":", "
              }
            ]
          }
        ]
      }
    ]
  }
  ```
</Accordion>

主要字段：

| **参数**                               | **类型**          | **描述**                                                                 |
| ------------------------------------ | --------------- | ---------------------------------------------------------------------- |
| audio\_format                        | string          | 源文件的音频格式。                                                              |
| channels                             | array\[integer] | 音频声道索引。单声道返回 \[0]，双声道返回 \[0, 1]，依此类推。                                  |
| original\_sampling\_rate             | integer         | 采样率（Hz）。                                                               |
| original\_duration\_in\_milliseconds | integer         | 原始音频时长（毫秒）。                                                            |
| channel\_id                          | integer         | 已转写的音频声道索引（从 0 开始）。                                                    |
| content\_duration\_in\_milliseconds  | integer         | 语音内容时长（毫秒）。<Warning>计费以语音时长为准，非语音内容不计费。AI 判定的语音时长可能与音频总时长不同。</Warning> |
| text                                 | string          | 转写文本（段落级、句子级或词级，取决于所在层级）。                                              |
| sentences                            | array           | 句子级转写结果。                                                               |
| words                                | array           | 词级转写结果。                                                                |
| begin\_time                          | integer         | 开始时间戳（毫秒）。                                                             |
| end\_time                            | integer         | 结束时间戳（毫秒）。                                                             |
| sentence\_id                         | integer         | 句子序号（从 1 开始）。                                                          |
| speaker\_id                          | integer         | 说话人索引（从 0 开始）。仅在启用说话人分离时出现。                                            |
| punctuation                          | string          | 该词后预测的标点符号（如有）。                                                        |

## 核心接口

### 查询参数类（`TranscriptionQueryParam`）

在 `Transcription` 实例上调用 `wait` 或 `fetch` 方法时，需要传入 `TranscriptionQueryParam`。

通过静态方法 `FromTranscriptionParam` 创建。

<Accordion title="点击查看示例">
  ```java
  // 创建转写请求参数
  TranscriptionParam param = TranscriptionParam.builder()
    // 如果未将 API Key 设置为环境变量，请将 apiKey 替换为您自己的 API Key
    //.apiKey("apikey")
    .model("qwen-audio-3.0-asr-flash-filetrans")
    .fileUrls(
        Arrays.asList(
            "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
            "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav"))
    .build();
  try {
    Transcription transcription = new Transcription();
    // 提交转写请求
    TranscriptionResult result = transcription.asyncCall(param);
    System.out.println("RequestId: " + result.getRequestId());
    TranscriptionQueryParam queryParam = TranscriptionQueryParam.FromTranscriptionParam(param, result.getTaskId());

  } catch (Exception e) {
    System.out.println("error: " + e);
  }
  ```
</Accordion>

| **方法**                                                                                                  | **参数**                                         | **返回值**                      | **描述**                           |
| ------------------------------------------------------------------------------------------------------- | ---------------------------------------------- | ---------------------------- | -------------------------------- |
| `public static TranscriptionQueryParam FromTranscriptionParam(TranscriptionParam param, String taskId)` | `param`：`TranscriptionParam` 实例，`taskId`：任务 ID | `TranscriptionQueryParam` 实例 | 创建 `TranscriptionQueryParam` 实例。 |

### 核心类（`Transcription`）

通过 `import com.alibaba.dashscope.audio.asr.transcription.*;` 导入。主要方法：

| **方法**                                                                 | **参数**                                    | **返回值**                                          | **描述**                                |
| ---------------------------------------------------------------------- | ----------------------------------------- | ------------------------------------------------ | ------------------------------------- |
| `public TranscriptionResult asyncCall(TranscriptionParam param)`       | `param`：`TranscriptionParam` 实例           | [TranscriptionResult](#任务结果-transcriptionresult) | 异步提交转写任务。                             |
| `public TranscriptionResult wait(TranscriptionQueryParam queryParam)`  | `queryParam`：`TranscriptionQueryParam` 实例 | [TranscriptionResult](#任务结果-transcriptionresult) | 阻塞等待，直到任务状态变为 `SUCCEEDED` 或 `FAILED`。 |
| `public TranscriptionResult fetch(TranscriptionQueryParam queryParam)` | `queryParam`：`TranscriptionQueryParam` 实例 | [TranscriptionResult](#任务结果-transcriptionresult) | 查询当前任务结果。                             |

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
