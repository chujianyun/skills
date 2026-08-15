> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Paraformer 录音文件识别 Java SDK

> 使用Java SDK接入Paraformer录音文件识别服务，支持批量提交音频URL进行异步转写，获取识别结果。

## 前提条件

- 获取API Key：在使用前，您需要[获取API Key](/api-reference/preparation/api-key)并配置环境变量 `DASHSCOPE_API_KEY`。如需使用临时Token，请参考[临时Token](/api-reference/more/generate-a-temporary-api-key)。
- 安装Java SDK：参考[安装SDK](/api-reference/preparation/install-sdk)完成Maven依赖配置。

## 模型列表

|         | paraformer-v2（推荐） | paraformer-8k-v2（推荐） | paraformer-v1 | paraformer-8k-v1 | paraformer-mtl-v1 |
| ------- | ----------------- | -------------------- | ------------- | ---------------- | ----------------- |
| 适用场景    | 通用场景              | 电话客服/8kHz            | 通用场景          | 电话客服/8kHz        | 多语种               |
| 采样率     | 16kHz             | 8kHz                 | 16kHz         | 8kHz             | 16kHz             |
| 语种      | 中文+英/日/韩/德/法/俄    | 中文                   | 中文            | 中文               | 中英法德日韩俄西葡马        |
| 定制热词    | 支持（vocabularyId）  | 支持（vocabularyId）     | 支持（phraseId）  | 支持（phraseId）     | 不支持               |
| 指定待识别语种 | language\_hints   | 不支持                  | 不支持           | 不支持              | language\_hints   |
| 说话人分离   | 支持                | 不支持                  | 不支持           | 不支持              | 不支持               |

## 约束限制

- 支持格式：aac、amr、avi、flac、flv、m4a、mkv、mov、mp3、mp4、mpeg、ogg、opus、wav、webm、wma、wmv
- 单文件大小不超过 2GB，时长不超过 12 小时
- 单次请求最多提交 100 个文件URL

## 快速开始

安装DashScope Java SDK后，设置环境变量：

```bash
export DASHSCOPE_API_KEY="REDACTED"
```

### 方式一：asyncCall + wait（阻塞等待）

提交任务后阻塞等待，直到任务完成：

```java
import com.alibaba.dashscope.audio.asr.transcription.*;
import com.google.gson.*;
import java.util.Arrays;

public class Main {
  public static void main(String[] args) {
    TranscriptionParam param =
        TranscriptionParam.builder()
            //.apiKey("apikey")
            .model("paraformer-v2")
            .parameter("language_hints", new String[]{"zh", "en"})
            .fileUrls(
                Arrays.asList(
                    "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
                    "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav"))
            .build();
    try {
      Transcription transcription = new Transcription();
      TranscriptionResult result = transcription.asyncCall(param);
      System.out.println("RequestId: " + result.getRequestId());
      result = transcription.wait(
          TranscriptionQueryParam.FromTranscriptionParam(param, result.getTaskId()));
      System.out.println(result.getOutput());
    } catch (Exception e) {
      System.out.println("error: " + e);
    }
    System.exit(0);
  }
}
```

### 方式二：asyncCall + fetch（轮询查询）

提交任务后主动轮询任务状态：

```java
import com.alibaba.dashscope.audio.asr.transcription.*;
import com.alibaba.dashscope.common.TaskStatus;
import com.google.gson.*;
import java.util.Arrays;

public class Main {
  public static void main(String[] args) {
    TranscriptionParam param =
        TranscriptionParam.builder()
            //.apiKey("apikey")
            .model("paraformer-v2")
            .parameter("language_hints", new String[]{"zh", "en"})
            .fileUrls(
                Arrays.asList(
                    "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
                    "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav"))
            .build();
    try {
      Transcription transcription = new Transcription();
      TranscriptionResult result = transcription.asyncCall(param);
      System.out.println("RequestId: " + result.getRequestId());
      while (true) {
        result = transcription.fetch(TranscriptionQueryParam.FromTranscriptionParam(param, result.getTaskId()));
        if (result.getTaskStatus() == TaskStatus.SUCCEEDED || result.getTaskStatus() == TaskStatus.FAILED) {
          break;
        }
        Thread.sleep(1000);
      }
      System.out.println(result.getOutput());
    } catch (Exception e) {
      System.out.println("error: " + e);
    }
    System.exit(0);
  }
}
```

## 请求参数

`TranscriptionParam` 通过建造者模式构建，支持以下参数：

| 参数                        | 类型             | 说明                                                                                             |
| ------------------------- | -------------- | ---------------------------------------------------------------------------------------------- |
| model                     | String         | 模型名称，如 `paraformer-v2`                                                                         |
| fileUrls                  | List\<String>  | 音频文件URL列表，最多100个                                                                               |
| vocabularyId              | String         | 定制热词ID（v2模型），参考[定制热词](/developer-guides/speech/improve-recognition-accuracy)                   |
| phraseId                  | String         | 定制热词ID（v1模型），参考[Paraformer热词定制与管理](/api-reference/speech-recognition/custom-hotwords/http-api) |
| channelId                 | List\<Integer> | 指定识别的声道，如 `[0]` 表示仅识别左声道                                                                       |
| disfluencyRemovalEnabled  | Boolean        | 是否过滤语气词，默认 `false`                                                                             |
| timestampAlignmentEnabled | Boolean        | 是否开启时间戳对齐，默认 `false`                                                                           |
| specialWordFilter         | String         | 敏感词过滤配置，JSON格式                                                                                 |
| language\_hints           | String\[]      | 指定待识别语种，如 `["zh", "en"]`                                                                       |
| diarizationEnabled        | Boolean        | 是否开启说话人分离，默认 `false`（仅v2模型支持）                                                                  |
| speakerCount              | Integer        | 说话人数量，与 `diarizationEnabled=true` 配合使用                                                         |
| apiKey                    | String         | API Key，优先使用环境变量 `DASHSCOPE_API_KEY`                                                           |

### specialWordFilter 格式

```json
{
  "filter_with_signed": {"word_list": ["测试"]},
  "filter_with_empty": {"word_list": ["开始", "发生"]},
  "system_reserved_filter": true
}
```

- `filter_with_signed`：将词替换为 `**`
- `filter_with_empty`：将词替换为空字符串
- `system_reserved_filter`：启用系统内置敏感词过滤

## 响应结果

### TranscriptionResult 方法

| 方法              | 类型                             | 说明                                     |
| --------------- | ------------------------------ | -------------------------------------- |
| getRequestId()  | String                         | 请求唯一标识                                 |
| getTaskId()     | String                         | 任务ID，用于查询任务状态                          |
| getTaskStatus() | TaskStatus                     | 任务状态（PENDING/RUNNING/SUCCEEDED/FAILED） |
| getResults()    | List\<TranscriptionTaskResult> | 子任务结果列表                                |
| getOutput()     | Object                         | 完整输出对象                                 |

### TranscriptionTaskResult 方法

| 方法                    | 类型     | 说明                      |
| --------------------- | ------ | ----------------------- |
| getFileUrl()          | String | 对应的音频文件URL              |
| getTranscriptionUrl() | String | 识别结果JSON文件的下载URL        |
| getSubTaskStatus()    | String | 子任务状态（SUCCEEDED/FAILED） |
| getMessage()          | String | 失败时的错误信息                |

### 识别结果JSON结构

识别完成后，通过 `getTranscriptionUrl()` 下载的JSON文件结构如下：

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

### 识别结果字段说明

| 字段                                   | 说明                |
| ------------------------------------ | ----------------- |
| audio\_format                        | 音频编码格式            |
| channels                             | 声道列表              |
| original\_sampling\_rate             | 原始采样率（Hz）         |
| original\_duration\_in\_milliseconds | 音频总时长（毫秒）         |
| channel\_id                          | 声道ID              |
| content\_duration\_in\_milliseconds  | 有效语音时长（毫秒）        |
| text                                 | 完整识别文本            |
| sentences                            | 句子列表              |
| words                                | 词级时间戳列表           |
| begin\_time                          | 开始时间（毫秒）          |
| end\_time                            | 结束时间（毫秒）          |
| speaker\_id                          | 说话人ID（开启说话人分离时有效） |
| punctuation                          | 该词后的标点符号          |

## 关键接口

### TranscriptionQueryParam.FromTranscriptionParam

```java
TranscriptionQueryParam.FromTranscriptionParam(TranscriptionParam param, String taskId)
```

从 `TranscriptionParam` 和 `taskId` 构建查询参数，用于 `wait` 和 `fetch` 方法。

### Transcription 类方法

| 方法                                   | 说明                                             |
| ------------------------------------ | ---------------------------------------------- |
| asyncCall(TranscriptionParam param)  | 提交异步转写任务，返回包含 `taskId` 的 `TranscriptionResult` |
| wait(TranscriptionQueryParam param)  | 阻塞等待任务完成，返回最终结果                                |
| fetch(TranscriptionQueryParam param) | 查询一次任务状态，立即返回当前结果                              |

## 其他接口

如需通过HTTP API直接管理异步任务（查询状态、取消任务等），请参考[管理异步任务](/developer-guides/run-and-scale/async-task-management)。

## 错误码

常见错误码请参考[错误信息](/api-reference/preparation/error-messages)。

任务整体状态为 `SUCCEEDED` 时，仍需检查每个子任务的 `subtask_status`。部分文件可能因下载失败等原因返回 `FAILED`：

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
  "task_metrics": {"TOTAL": 2, "SUCCEEDED": 1, "FAILED": 1}
}
```

## 更多示例

更多完整示例代码请参考 [GitHub 示例仓库](https://github.com/aliyun/alibabacloud-bailian-speech-demo)。

## 常见问题

<Accordion title="是否支持Base64编码的音频文件？">
  不支持，仅支持通过公网可访问的URL传入音频文件。请将音频文件上传至阿里云OSS、Web服务器或CDN后，使用公网URL提交。
</Accordion>

<Accordion title="如何准备公网可访问的音频URL？">
  将音频文件上传至以下任意位置：

  - 阿里云OSS（推荐），开启公读权限或生成签名URL
  - 您自己的Web服务器
  - CDN

  确保URL可从公网直接访问，不需要登录或其他认证。
</Accordion>

<Accordion title="识别需要多长时间？">
  录音文件识别为异步任务，通常需要数分钟。识别时间与文件时长、并发任务数量有关。建议使用轮询方式（asyncCall + fetch）定期检查任务状态，而非设置过短的等待时间。
</Accordion>

<Accordion title="开启timestampAlignmentEnabled后结果不一致怎么办？">
  时间戳对齐功能会对识别结果进行二次对齐处理，可能导致文本与默认结果略有差异。如对文本准确性要求较高，建议关闭此功能（默认关闭）。
</Accordion>

<Accordion title="轮询时出现频率限制错误怎么办？">
  降低轮询频率，建议每隔1\~3秒查询一次。避免短时间内大量并发查询同一任务。
</Accordion>

<Accordion title="提交任务后无任何识别结果怎么办？">
  请检查以下几点：

  - 音频格式是否在支持列表内（aac/mp3/wav等）
  - 是否设置了正确的 `language_hints`（如中文音频需设置 `["zh"]`）
  - 是否需要配置定制热词（vocabularyId/phraseId）
  - 音频URL是否可从公网访问

  更多问题可参考 [GitHub 问题讨论](https://github.com/aliyun/alibabacloud-bailian-speech-demo)。
</Accordion>
