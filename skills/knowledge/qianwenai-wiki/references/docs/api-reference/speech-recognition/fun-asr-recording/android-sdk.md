> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Fun-ASR 录音文件识别 Android SDK

> 本文档提供了Fun-ASR录音文件识别Android SDK的详细使用指南，帮助您将语音转换为文本。

**用户指南**： 关于模型介绍和选型建议，请参见[录音文件识别](/developer-guides/speech/asr)。

## 快速开始

### 前提条件

1. **获取API Key** — 请[获取API Key](/api-reference/preparation/api-key)并配置到环境变量，而非硬编码在代码中，以防止因代码泄露导致的安全风险。

   <Note>
     当需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时鉴权Token](/api-reference/more/generate-a-temporary-api-key)。临时鉴权Token默认拥有60秒有效期，过期后需重新获取。
   </Note>

2. **下载SDK并运行示例代码**：
   - [下载最新SDK整合包](/api-reference/preparation/install-sdk)。
   - 解压ZIP包。在 `app/libs` 目录中获取AAR格式SDK，并添加到项目依赖。需要Android CPP接入时，使用ZIP包内的 `android_libs` 与 `android_include` 获取动态库和头文件。
   - 用Android Studio打开工程。示例代码位于 `DashFunAsrFileTranscriberActivity.java`，替换API Key后体验功能。

### 调用步骤

<Steps>
  <Step title="同步模式">
    <ol>
      <li>初始化SDK</li>
      <li>按业务需求配置相关参数</li>
      <li>调用 `startFileTranscriber` 启动识别任务（`async_request` 设为 `false`）</li>
      <li>在 `onFileTransEventCallback` 接口中监听 `EVENT_FILE_TRANS_RESULT` 事件，获取最终识别结果</li>
      <li>调用 `release` 释放SDK资源</li>
    </ol>
  </Step>

  <Step title="异步模式">
    <ol>
      <li>初始化SDK</li>
      <li>按业务需求配置相关参数</li>
      <li>调用 `startFileTranscriber` 启动识别任务（`async_request` 设为 `true`）</li>
      <li>调用 `queryFileTranscriber` 主动查询识别进度/结果</li>
      <li>在 `onFileTransEventCallback` 接口中监听 `EVENT_FILE_TRANS_QUERY_RESULT` 事件，获取当前查询结果</li>
      <li>在 `onFileTransEventCallback` 接口中监听 `EVENT_FILE_TRANS_RESULT` 事件，获取最终识别结果</li>
      <li>调用 `release` 释放SDK资源</li>
    </ol>
  </Step>
</Steps>

## 请求参数

### 连接与控制参数

通过 `initialize()` 方法的 `parameters` 参数传入，格式为JSON字符串。

```json
{
    "url": "wss://dashscope.aliyuncs.com/api-ws/v1/inference",
    "apikey": "st-****",
    "device_id": "my_device_id",
    "service_mode": "1"
}
```

| 参数                  | 类型     | 是否必须 | 说明                                                                                                                                                                                        |
| ------------------- | ------ | ---- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url`               | String | 是    | 服务地址，固定为 `wss://dashscope.aliyuncs.com/api-ws/v1/inference`。                                                                                                                              |
| `apikey`            | String | 是    | API Key。建议使用时效性短、安全性更高的[临时鉴权Token](/api-reference/more/generate-a-temporary-api-key)，以降低长期有效Key泄露的风险。                                                                                     |
| `service_mode`      | String | 是    | 运行模式。录音文件识别固定为 `"1"`。                                                                                                                                                                     |
| `device_id`         | String | 是    | 用于标识终端用户的唯一字符串，可设为应用内用户ID或客户端生成的设备唯一标识符。此ID主要用于日志追踪和问题排查。                                                                                                                                 |
| `debug_path`        | String | 否    | 日志文件的存储路径。仅在 `initialize` 接口的 `save_log` 设为 `true` 时生效。此时必须设置日志文件路径，否则将报错。本地最多保留两个日志文件。                                                                                                   |
| `max_log_file_size` | int    | 否    | 日志文件的最大字节数。仅在 `save_log=true` 时生效。默认值：`104857600`（100MiB）。                                                                                                                                |
| `log_track_level`   | int    | 否    | 控制通过 `onFileTransLogTrackCallback` 对外发送的日志内容过滤级别。默认值：`2`。取值范围：0（VERBOSE）、1（DEBUG）、2（INFO）、3（WARNING）、4（ERROR）、5（NONE，关闭此功能）。与 `initialize` 的 `level` 参数共同决定最终回调的日志，日志级别数值须同时大于等于两者才会触发回调。 |

### 语音识别效果参数

通过 `startFileTranscriber()` 方法的 `params` 参数传入（也可通过 `setParams()` 单独设置 `nls_config` 部分），格式为JSON字符串。

```json
{
    "file_urls": [
        "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
        "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav"
    ],
    "async_request": false,
    "nls_config": {
        "model": "qwen-audio-3.0-asr-flash-filetrans",
        "diarization_enabled": false,
        "parameters": {
            "speech_noise_threshold": 0.0
        }
    }
}
```

| 参数                                             | 类型              | 是否必须 | 说明                                                                                                                                                                                                                             |
| ---------------------------------------------- | --------------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `file_urls`                                    | array\[string]  | 是    | 音视频文件转写的URL列表，支持HTTP/HTTPS协议，单次请求最多100个URL。支持格式：aac、amr、avi、flac、flv、m4a、mkv、mov、mp3、mp4、mpeg、ogg、opus、wav、webm、wma、wmv。文件大小不超过2GB，时长不超过12小时。                                                                                  |
| `async_request`                                | boolean         | 否    | 是否为异步请求。默认值：`false`。`true` 为异步，`false` 为同步。                                                                                                                                                                                    |
| `apikey`                                       | string          | 否    | 若连接参数中使用临时鉴权Token，可在此处更新以防止超时失效。                                                                                                                                                                                               |
| `nls_config`                                   | object          | 是    | 语音识别核心配置对象。                                                                                                                                                                                                                    |
| `nls_config.model`                             | string          | 是    | 语音识别模型。支持 Qwen-Audio-3.0-ASR-Flash-Filetrans 和 Fun-ASR 系列模型，参见[模型列表](/developer-guides/speech/speech-to-text-models)。                                                                                                          |
| `nls_config.language_hints`                    | array\[string]  | 否    | 设置待识别语言代码。如果无法提前确定语种，可不设置，模型会自动识别语种。对于 Qwen-Audio-3.0-ASR-Flash-Filetrans 系列模型，最多支持设置 4 个值，超出 4 个时仅前 4 个生效；对于 Fun-ASR 系列模型，仅支持设置 1 个值。各模型支持的语言代码参见[支持的语言](/api-reference/speech-recognition/fun-asr-recording/java-sdk#支持的语言)。 |
| `nls_config.special_word_filter`               | object          | 否    | 敏感词处理配置。未传入时启用系统内置敏感词过滤（匹配词替换为等长 `*`）。传入时可自定义替换或过滤策略，参见下方说明。                                                                                                                                                                   |
| `nls_config.channel_id`                        | array\[integer] | 否    | 指定多音轨文件中需识别的音轨索引（从0开始）。默认值：`[0]`。每个指定音轨独立计费。                                                                                                                                                                                   |
| `nls_config.diarization_enabled`               | boolean         | 否    | 是否启用自动说话人分离。默认关闭，仅支持单声道音频。启用后识别结果含 `speaker_id` 字段。                                                                                                                                                                            |
| `nls_config.speaker_count`                     | integer         | 否    | 说话人数量参考值，需同时设置 `diarization_enabled=true`。取值范围：\[2, 100]。                                                                                                                                                                      |
| `nls_config.vocabulary_id`                     | string          | 否    | 预编译热词列表 ID。需预先调用创建热词列表接口生成，识别时传入该 ID 即可使用列表中的热词。适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景。参见[预编译热词](/developer-guides/speech/improve-recognition-accuracy#预编译热词)。                                                                            |
| `nls_config.parameters`                        | object          | 否    | 配置其他参数，内容为JSON Object格式。                                                                                                                                                                                                       |
| `nls_config.parameters.speech_noise_threshold` | float           | 否    | 语音噪声阈值。                                                                                                                                                                                                                        |

#### special\_word\_filter 格式

```json
{
  "filter_with_signed": {
    "word_list": ["测试"]
  },
  "filter_with_empty": {
    "word_list": ["开始", "发生"]
  },
  "system_reserved_filter": true
}
```

| 字段                       | 类型      | 说明                                     |
| ------------------------ | ------- | -------------------------------------- |
| `filter_with_signed`     | object  | 将匹配词替换为等长 `*`。`word_list` 为需替换的敏感词列表。  |
| `filter_with_empty`      | object  | 将匹配词从识别结果中完全移除。`word_list` 为需过滤的敏感词列表。 |
| `system_reserved_filter` | boolean | 是否同时启用系统内置敏感词规则，默认 `true`。             |

## 关键接口

### NativeNui

#### initialize

初始化语音识别SDK实例。SDK为单例模式，在调用 `release` 前禁止重复初始化。此接口会阻塞当前线程，须在非UI线程中调用。

```java
public synchronized int initialize(final INativeFileTransCallback callback,
                                   String parameters,
                                   final Constants.LogLevel level,
                                   final boolean save_log)
```

| 参数           | 类型                       | 说明                                                                                   |
| ------------ | ------------------------ | ------------------------------------------------------------------------------------ |
| `callback`   | INativeFileTransCallback | 事件和数据回调接口的实现。                                                                        |
| `parameters` | String                   | JSON字符串，包含鉴权、连接和调试参数，参见[连接与控制参数](#连接与控制参数)。                                          |
| `level`      | Constants.LogLevel       | 控制SDK自身日志的打印级别。                                                                      |
| `save_log`   | boolean                  | 是否保存本地日志。若为 `true`，须在连接与控制参数中通过 `debug_path` 指定路径，并可通过 `max_log_file_size` 设置文件大小上限。 |

**返回值**： 错误码，参见[错误信息](/api-reference/preparation/error-messages)。

#### setParams

独立设置或更新 `nls_config` 参数。如果所有参数都在 `startFileTranscriber` 中一次性提供，则无需调用此方法。

```java
public synchronized int setParams(String params);
```

| 参数       | 类型     | 说明                                                    |
| -------- | ------ | ----------------------------------------------------- |
| `params` | String | `nls_config` 参数的JSON字符串。`nls_config` 以外的参数不支持通过此方法设置。 |

示例：

```json
{
    "nls_config": {
        "model": "qwen-audio-3.0-asr-flash-filetrans",
        "diarization_enabled": false
    }
}
```

**返回值**： 错误码，参见[错误信息](/api-reference/preparation/error-messages)。

#### startFileTranscriber

启动识别任务。

```java
public synchronized int startFileTranscriber(String params, byte[] task_id)
```

| 参数        | 类型      | 说明                                        |
| --------- | ------- | ----------------------------------------- |
| `params`  | String  | 语音识别效果参数的JSON字符串，参见[语音识别效果参数](#语音识别效果参数)。 |
| `task_id` | byte\[] | 任务ID，由SDK内部生成随机字符串，接口调用成功后可获得。            |

**返回值**： 错误码，参见[错误信息](/api-reference/preparation/error-messages)。

#### queryFileTranscriber

主动查询异步任务的当前状态和结果。调用成功后，结果通过 `onFileTransEventCallback` 中的 `EVENT_FILE_TRANS_QUERY_RESULT` 事件返回。

```java
public synchronized int queryFileTranscriber(String task_id)
```

| 参数        | 类型     | 说明        |
| --------- | ------ | --------- |
| `task_id` | String | 待查询的任务ID。 |

**返回值**： 错误码，参见[错误信息](/api-reference/preparation/error-messages)。

#### cancelFileTranscriber

立即取消当前任务。

```java
public synchronized int cancelFileTranscriber(String task_id)
```

| 参数        | 类型     | 说明        |
| --------- | ------ | --------- |
| `task_id` | String | 待取消的任务ID。 |

**返回值**： 错误码，参见[错误信息](/api-reference/preparation/error-messages)。

#### release

释放SDK所有内部资源。调用后SDK实例将变为不可用状态，如需再次使用，须重新调用 `initialize` 进行初始化。

```java
public synchronized int release();
```

**返回值**： 错误码，参见[错误信息](/api-reference/preparation/error-messages)。

#### GetVersion

获取当前SDK版本信息。

```java
public synchronized String GetVersion();
```

**返回值**： SDK版本信息字符串。

### INativeFileTransCallback：监听回调

#### onFileTransEventCallback

监听事件和语音识别结果。

```java
void onFileTransEventCallback(NuiEvent event, final int resultCode, final int arg2, AsrResult asrResult, String taskId);
```

| 参数           | 类型        | 说明                                                                                  |
| ------------ | --------- | ----------------------------------------------------------------------------------- |
| `event`      | NuiEvent  | 回调事件，参见 [NuiEvent](#nuievent-事件类型)。                                                 |
| `resultCode` | int       | 错误码，仅在 `EVENT_ASR_ERROR` 事件时有效，参见[错误信息](/api-reference/preparation/error-messages)。 |
| `asrResult`  | AsrResult | 语音识别结果。                                                                             |
| `taskId`     | String    | 任务ID。                                                                               |
| `arg2`       | int       | 保留参数。                                                                               |

#### onFileTransLogTrackCallback

监听SDK内部追踪日志，用于问题定位和调试。

```java
default void onFileTransLogTrackCallback(Constants.LogLevel level, String log)
```

### NuiEvent: 事件类型

| 事件                              | 说明                                          |
| ------------------------------- | ------------------------------------------- |
| `EVENT_FILE_TRANS_CONNECTED`    | 连接服务成功。                                     |
| `EVENT_FILE_TRANS_UPLOADED`     | 上传待识别音频文件成功。                                |
| `EVENT_FILE_TRANS_QUERY_RESULT` | 查询任务结果（异步模式下调用 `queryFileTranscriber` 后触发）。 |
| `EVENT_FILE_TRANS_RESULT`       | 识别最终结果。                                     |
| `EVENT_ASR_ERROR`               | 语音识别过程中出现错误。                                |

## 错误码

如遇报错问题，请参见[错误信息](/api-reference/preparation/error-messages)进行排查。
