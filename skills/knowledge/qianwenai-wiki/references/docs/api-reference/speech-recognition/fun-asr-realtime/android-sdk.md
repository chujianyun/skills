> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Fun-ASR 实时语音识别 Android SDK

> 本文档提供了Fun-ASR实时语音识别Android SDK的详细使用指南，帮助您将语音转换为文本。

**用户指南**： 关于模型介绍和选型建议，请参见[实时语音识别](/developer-guides/speech/asr-realtime)。

## 快速开始

### 前提条件

1. **获取API Key** — 请[获取API Key](/api-reference/preparation/api-key)并配置到环境变量，而非硬编码在代码中，以防止因代码泄露导致的安全风险。

   <Note>
     当您需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问等高风险操作时，建议使用[临时鉴权Token](/api-reference/more/generate-a-temporary-api-key)。与长期有效的API Key相比，临时鉴权Token具备时效性短（60秒）、安全性高的特点，适用于临时调用场景，能有效降低API Key泄露的风险。
   </Note>

2. **下载SDK并运行示例代码**：
   - [下载最新SDK整合包](/api-reference/preparation/install-sdk)。
   - 解压ZIP包。在`app/libs`目录中获取AAR格式SDK，并添加到项目依赖。需要Android CPP接入时，使用ZIP包内的`android_libs`与`android_include`获取动态库和头文件。
   - 用Android Studio打开工程。示例代码位于`DashFunAsrSpeechTranscriberActivity.java`，替换API Key后体验功能。

### 调用步骤

<Steps>
  <Step title="初始化SDK">
    调用`initialize`方法完成SDK初始化。SDK采用单例模式，在`release`之前不得重复初始化。该方法会阻塞当前线程，须在非UI线程中调用。
  </Step>

  <Step title="设置参数">
    通过`initialize`的`parameters`参数设置[连接与控制参数](#连接与控制参数)，通过`setParams`的`params`参数设置[语音识别效果参数](#语音识别效果参数)。
  </Step>

  <Step title="调用startDialog启动识别">
    调用`startDialog`方法启动语音识别。
  </Step>

  <Step title="在onNuiAudioStateChanged中开启录音">
    实现`onNuiAudioStateChanged`回调，在收到`STATE_OPEN`状态时开启麦克风录音。
  </Step>

  <Step title="在onNuiNeedAudioData中持续提供音频数据">
    实现`onNuiNeedAudioData`回调，持续向SDK填充从麦克风采集的PCM音频数据。
  </Step>

  <Step title="在onNuiEventCallback中监听事件和获取结果">
    实现`onNuiEventCallback`回调，监听识别事件并获取实时识别结果。
  </Step>

  <Step title="停止识别">
    调用`stopDialog`停止识别。服务端返回最终识别结果后，将触发`EVENT_TRANSCRIBER_COMPLETE`事件。
  </Step>

  <Step title="释放资源">
    调用`release`释放所有内部资源。释放后如需再次使用，须重新调用`initialize`进行初始化。
  </Step>
</Steps>

## 请求参数

### 连接与控制参数

通过`initialize()`方法的`parameters`参数传入，格式为JSON字符串。

```json
{
    "url": "wss://dashscope.aliyuncs.com/api-ws/v1/inference",
    "apikey": "st-****",
    "device_id": "my_device_id",
    "service_mode": "1"
}
```

| 参数                  | 类型     | 是否必须 | 说明                                                                                                                 |
| ------------------- | ------ | ---- | ------------------------------------------------------------------------------------------------------------------ |
| `url`               | String | 是    | 服务地址，固定为 `wss://dashscope.aliyuncs.com/api-ws/v1/inference`。                                                       |
| `apikey`            | String | 是    | API Key。建议使用[临时鉴权Token](/api-reference/more/generate-a-temporary-api-key)。                                         |
| `service_mode`      | String | 是    | 运行模式，实时语音识别固定为 `"1"`。                                                                                              |
| `device_id`         | String | 是    | 用于标识终端用户的唯一字符串，可设为应用内用户ID或客户端生成的设备唯一标识符。此ID主要用于日志追踪和问题排查。                                                          |
| `debug_path`        | String | 否    | 日志文件存储路径，`save_log=true`时生效，本地最多保留两个日志文件。                                                                          |
| `save_wav`          | String | 否    | 是否保存调试音频，默认 `"false"`。需`save_log=true`且`debug_path`已设置时生效。                                                         |
| `max_log_file_size` | int    | 否    | 日志文件最大字节数，默认 `104857600`（100MiB），`save_log=true`时生效。                                                               |
| `log_track_level`   | int    | 否    | `onNuiLogTrackCallback`过滤级别，默认 `2`，取值 0--5（VERBOSE/DEBUG/INFO/WARNING/ERROR/NONE），与`initialize`的`level`参数共同决定回调日志。 |

### 语音识别效果参数

通过`setParams()`方法的`params`参数传入，格式为JSON字符串。

```json
{
    "service_type": 4,
    "nls_config": {
        "model": "fun-asr-realtime",
        "sr_format": "pcm",
        "sample_rate": "16000",
        "parameters": {
            "speech_noise_threshold": 0.0
        }
    }
}
```

| 参数                                             | 类型             | 是否必须 | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ---------------------------------------------- | -------------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `service_type`                                 | int            | 是    | 固定为 `4`。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `nls_config`                                   | object         | 是    | 语音识别核心配置。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `nls_config.model`                             | string         | 是    | 识别模型，参见[模型列表](/developer-guides/speech/speech-to-text-models)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `nls_config.sr_format`                         | string         | 是    | 音频格式，支持 `pcm`、`wav`、`opus`。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `nls_config.sample_rate`                       | int            | 是    | 待识别音频采样率（Hz）。8k 模型仅支持 8000 Hz，其他模型支持任意采样率。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `nls_config.semantic_punctuation_enabled`      | boolean        | 否    | 是否开启语义断句模式，默认 `false`（使用VAD断句）。语义断句准确性更高，适合会议转写场景；VAD断句延迟较低，适合实时交互场景。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `nls_config.max_sentence_silence`              | int            | 否    | VAD断句静音阈值（ms），默认 `800`，范围 200--6000。当一段语音后的静音时长超过该阈值时，系统判定该句结束。`semantic_punctuation_enabled=false`时生效。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `nls_config.multi_threshold_mode_enabled`      | boolean        | 否    | 是否启用多阈值模式，防止过长句子被切断，默认 `false`。`semantic_punctuation_enabled=false`时生效。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `nls_config.heartbeat`                         | boolean        | 否    | 是否开启长连接保持，默认 `false`。`true`时持续发送静音可保持连接；`false`时60秒超时断开。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `nls_config.vocabulary_id`                     | string         | 否    | 热词词表ID，参见[定制热词](/developer-guides/speech/improve-recognition-accuracy)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `nls_config.language_hints`                    | array\[string] | 否    | 识别语言代码。不设置时自动检测。不同模型支持的语言代码如下：<br /> **fun-asr-realtime、fun-asr-realtime-2025-11-07**：`zh`（中文）、`en`（英文）、`ja`（日语）、`ko`（韩语）、`vi`（越南语）、`th`（泰语）、`id`（印尼语）、`ms`（马来语）、`tl`（菲律宾语）、`hi`（印地语）、`ar`（阿拉伯语）、`fr`（法语）、`de`（德语）、`es`（西班牙语）、`pt`（葡萄牙语）、`ru`（俄语）、`it`（意大利语）、`nl`（荷兰语）、`sv`（瑞典语）、`da`（丹麦语）、`fi`（芬兰语）、`no`（挪威语）、`el`（希腊语）、`pl`（波兰语）、`cs`（捷克语）、`hu`（匈牙利语）、`ro`（罗马尼亚语）、`bg`（保加利亚语）、`hr`（克罗地亚语）、`sk`（斯洛伐克语）<br /> **fun-asr-realtime-2026-02-28**：`zh`（中文）、`en`（英文）、`ja`（日语）<br /> **fun-asr-realtime-2025-09-15**：`zh`（中文）、`en`（英文）<br /> **fun-asr-flash-8k-realtime、fun-asr-flash-8k-realtime-2026-01-28**：`zh`（中文） |
| `nls_config.parameters`                        | object         | 否    | 其他参数配置，内容为JSON Object格式。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `nls_config.parameters.speech_noise_threshold` | float          | 否    | 语音噪声检测阈值，用于调节VAD灵敏度。取值范围：\[-1.0, 1.0]。接近 -1：更多噪声可能被识别为语音。接近 +1：部分语音可能被过滤为噪声。这是高级参数，调整会显著影响识别质量，建议以 0.1 为步长逐步调整并充分测试。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |

<Warning>
  `sr_format`为`opus`时，须向SDK提供原始PCM数据，由SDK负责编码为Opus格式；`sr_format`为`wav`或`pcm`时，须提供PCM编码数据。
</Warning>

## 关键接口

### NativeNui

#### initialize

初始化SDK。SDK采用单例模式，`release`之前禁止重复初始化。该方法会阻塞当前线程，须在非UI线程中调用。

```java
public synchronized int initialize(final INativeNuiCallback callback,
                                   String parameters,
                                   final Constants.LogLevel level,
                                   final boolean save_log)
```

| 参数           | 类型                 | 说明                                                   |
| ------------ | ------------------ | ---------------------------------------------------- |
| `callback`   | INativeNuiCallback | 回调接口实例，参见 [INativeNuiCallback](#inativenuicallback)。 |
| `parameters` | String             | 连接与控制参数的JSON字符串，参见[连接与控制参数](#连接与控制参数)。               |
| `level`      | Constants.LogLevel | 日志级别。                                                |
| `save_log`   | boolean            | 是否保存日志，`true`时须在`parameters`中设置`debug_path`。         |

**返回值**： 错误码，参见[错误信息](/api-reference/preparation/error-messages)。

#### setParams

以JSON格式设置语音识别效果参数，须在`startDialog`之前调用。

```java
public synchronized int setParams(String params)
```

| 参数       | 类型     | 说明                                        |
| -------- | ------ | ----------------------------------------- |
| `params` | String | 语音识别效果参数的JSON字符串，参见[语音识别效果参数](#语音识别效果参数)。 |

**返回值**： 错误码，参见[错误信息](/api-reference/preparation/error-messages)。

#### startDialog

开始语音识别。

```java
public synchronized int startDialog(VadMode vad_mode, String dialog_params)
```

| 参数              | 类型      | 说明                              |
| --------------- | ------- | ------------------------------- |
| `vad_mode`      | VadMode | 固定传入 `VadMode.TYPE_P2T`。        |
| `dialog_params` | String  | 用于临时鉴权Token过期时更新apikey的JSON字符串。 |

`dialog_params`格式：

```json
{"apikey": "st-****"}
```

**返回值**： 错误码，参见[错误信息](/api-reference/preparation/error-messages)。

#### stopDialog

结束语音识别。服务端返回最终识别结果后任务结束。

```java
public synchronized int stopDialog();
```

**返回值**： 错误码，参见[错误信息](/api-reference/preparation/error-messages)。

#### cancelDialog

立即结束语音识别，不等待服务端返回最终识别结果。

```java
public synchronized int cancelDialog();
```

**返回值**： 错误码，参见[错误信息](/api-reference/preparation/error-messages)。

#### release

释放所有内部资源。释放后如需再次使用，须重新调用`initialize`进行初始化。

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

### INativeNuiCallback

实现此接口以监听SDK回调事件。

#### onNuiEventCallback

监听事件和语音识别结果。

```java
void onNuiEventCallback(NuiEvent event, final int resultCode, final int arg2, KwsResult kwsResult, AsrResult asrResult);
```

| 参数           | 类型        | 说明                                                                               |
| ------------ | --------- | -------------------------------------------------------------------------------- |
| `event`      | NuiEvent  | 事件类型，参见 [NuiEvent](#nuievent)。                                                   |
| `resultCode` | int       | 错误码，仅`EVENT_ASR_ERROR`事件时有效，参见[错误信息](/api-reference/preparation/error-messages)。 |
| `asrResult`  | AsrResult | 语音识别结果。                                                                          |
| `kwsResult`  | KwsResult | 语音唤醒结果，实时语音识别场景无需关注。                                                             |
| `arg2`       | int       | 保留参数。                                                                            |

#### onNuiAudioStateChanged

监听音频状态变化。SDK通过此回调通知应用何时开启或停止录音。

```java
void onNuiAudioStateChanged(AudioState state);
```

| AudioState    | 说明               |
| ------------- | ---------------- |
| `STATE_OPEN`  | 交互启动，应打开录音。      |
| `STATE_PAUSE` | 交互停止，应停止录音。      |
| `STATE_CLOSE` | SDK实例释放，应彻底关闭录音。 |

#### onNuiNeedAudioData

持续提供待识别的音频数据。开始识别后，SDK会连续触发此回调。

```java
int onNuiNeedAudioData(byte[] buffer, int len);
```

| 参数       | 类型      | 说明           |
| -------- | ------- | ------------ |
| `buffer` | byte\[] | 需填充的音频数据缓冲区。 |
| `len`    | int     | 需填充的字节数。     |

**返回值**： 实际填充的字节数。

#### onNuiLogTrackCallback

监听SDK内部追踪日志。

```java
default void onNuiLogTrackCallback(Constants.LogLevel level, String log)
```

### NuiEvent

语音识别事件类型。

| 事件                           | 说明                         |
| ---------------------------- | -------------------------- |
| `EVENT_TRANSCRIBER_STARTED`  | 任务启动成功。                    |
| `EVENT_VAD_START`            | 任务启动后即触发，不代表检测到人声起点。       |
| `EVENT_VAD_END`              | 检测到人声终点。                   |
| `EVENT_ASR_PARTIAL_RESULT`   | 返回中间识别结果（非最终结果）。           |
| `EVENT_ASR_ERROR`            | 识别过程出错。                    |
| `EVENT_MIC_ERROR`            | 连续2秒未收到音频数据。               |
| `EVENT_SENTENCE_END`         | 检测到一句话结束，返回完整识别结果。         |
| `EVENT_TRANSCRIBER_COMPLETE` | 语音识别结束（调用`stopDialog`后触发）。 |

## 错误码

如遇报错问题，请参见[错误信息](/api-reference/preparation/error-messages)进行排查。
