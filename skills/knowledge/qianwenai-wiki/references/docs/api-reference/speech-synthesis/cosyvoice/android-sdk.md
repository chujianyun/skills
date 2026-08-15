> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 语音合成 Qwen-Audio-TTS/CosyVoice Android SDK

> 使用原生 SDK 将 Qwen-Audio-TTS/CosyVoice 模型的实时文本转语音功能集成到 Android 应用中。

CosyVoice Android SDK 为 Android 应用提供原生实时语音合成能力。SDK 支持两种调用方式：一次性输入文本合成和流式输入文本合成，通过 WebSocket 连接在合成过程中流式传输音频数据。

## 快速开始

<Steps>
  <Step title="获取 API Key">
    [获取 API Key](/api-reference/preparation/api-key) 并将其配置为环境变量以确保安全。

    为第三方应用或用户提供临时访问权限，或需要对敏感操作进行严格控制时，使用[临时 API Key](/api-reference/more/generate-a-temporary-api-key)。临时 API Key 默认 60 秒后过期。
  </Step>

  <Step title="下载 SDK 并运行示例">
    下载最新 SDK 整合包。

    解压后，在 `app/libs` 目录下找到 AAR 格式的 SDK 并添加到项目依赖中。如需在 Android C++ 工程中集成，可使用压缩包中的 `android_libs` 和 `android_include` 获取动态库和头文件。

    在 Android Studio 中打开项目，示例代码位于 `DashCosyVoiceStreamTtsActivity.java`。替换 API Key 后运行示例即可体验功能。
  </Step>

  <Step title="选择调用方式">
    根据场景选择合适的调用方式。

| 调用方式    | 说明                                                                                                                                                                              |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 一次性输入文本 | 适用于短文本合成，支持 SSML 标记语言。调用 `playStreamInputTts` 或 `asyncPlayStreamInputTts` 发送文本并开始合成。发送文本长度不超过 20000 字符。                                                                         |
| 流式输入文本  | 适用于实时对话、长文本"边说边合"，不支持 SSML。调用 `startStreamInputTts` 开始合成，通过 `sendStreamInputTts` 持续发送文本，最后调用 `stopStreamInputTts` 或 `asyncStopStreamInputTts` 结束。单次发送不超过 20000 字符，累计不超过 20 万字符。 |
  </Step>

  <Step title="接收音频数据">
    在 `onStreamInputTtsDataCallback` 回调中接收音频数据。建议流式播放，如需本地保存，将音频数据追加到同一文件中直至合成结束。
  </Step>
</Steps>

## 请求参数

### 连接与控制参数

通过 `startStreamInputTts`、`playStreamInputTts` 和 `asyncPlayStreamInputTts` 接口的 `ticket` 参数传入 JSON 字符串来配置。

```json
{
  "url": "wss://dashscope.aliyuncs.com/api-ws/v1/inference",
  "apikey": "st-****",
  "device_id": "my_device_id"
}
```

| 参数                    | 类型     | 是否必填 | 描述                                                                                                                                                                                                 |
| --------------------- | ------ | ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url`                 | String | 是    | 服务地址，固定为 `wss://dashscope.aliyuncs.com/api-ws/v1/inference`。                                                                                                                                       |
| `apikey`              | String | 是    | API Key。建议使用短效[临时 API Key](/api-reference/more/generate-a-temporary-api-key)以降低长期密钥泄露风险。                                                                                                           |
| `device_id`           | String | 是    | 唯一标识终端用户的字符串，如应用内用户 ID 或客户端生成的设备标识。用于日志追踪和问题排查。                                                                                                                                                    |
| `complete_waiting_ms` | int    | 否    | 调用 stop 接口后等待合成完成事件（`STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE`）的超时时间（毫秒）。默认值 `10000`。                                                                                                             |
| `debug_path`          | String | 否    | 日志文件存储路径。仅在 `save_log` 设置为 `true` 时生效。开启时必须设置该路径否则会报错。本地最多保留两个日志文件。                                                                                                                                |
| `max_log_file_size`   | int    | 否    | 单个日志文件最大大小（字节）。仅在 `save_log` 为 `true` 时生效。默认值 `104857600`（100 MiB）。                                                                                                                                |
| `log_track_level`     | int    | 否    | 过滤通过 `onStreamInputTtsLogTrackCallback` 回调发送的日志内容。默认值 `2`。取值：`0` = VERBOSE，`1` = DEBUG，`2` = INFO，`3` = WARNING，`4` = ERROR，`5` = NONE（关闭回调）。日志条目仅在级别同时大于等于 `log_track_level` 和 `log_level` 时才会发送。 |

### 语音合成效果参数

通过 `startStreamInputTts`、`playStreamInputTts` 和 `asyncPlayStreamInputTts` 接口的 `parameters` 参数传入 JSON 字符串来配置。

```json
{
  "model": "cosyvoice-v2",
  "voice": "longxiaochun_v2",
  "format": "mp3",
  "sample_rate": 24000,
  "volume": 50,
  "rate": 1,
  "pitch": 1,
  "language_hints": ["zh"]
}
```

| 参数                       | 类型        | 是否必填 | 描述                                                                                                                                                                                                                                                                                                              |
| ------------------------ | --------- | ---- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model`                  | String    | 是    | 语音合成模型。在资源与预算允许的情况下，优先选择 `cosyvoice-v3-plus` 获取最佳合成效果，对成本敏感时可选 `cosyvoice-v3` 平衡质量与价格。                                                                                                                                                                                                                          |
| `voice`                  | String    | 是    | 音色名称，参见[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)。                                                                                                                                                                                                                                   |
| `format`                 | String    | 否    | 音频编码格式。默认值 `mp3`。取值范围：`pcm`/`wav`/`mp3`/`opus`（`cosyvoice-v1` 不支持 `opus` 格式）。                                                                                                                                                                                                                                   |
| `volume`                 | int       | 否    | 音量大小。默认值 `50`，取值范围 `[0, 100]`。音量与该值呈线性关系，`0` 为静音，`100` 为最大音量。                                                                                                                                                                                                                                                   |
| `sample_rate`            | int       | 否    | 采样率（Hz）。默认值 `22050`。取值范围：`8000`/`16000`/`22050`/`24000`/`44100`/`48000`。                                                                                                                                                                                                                                        |
| `rate`                   | float     | 否    | 语速。默认值 `1.0`，取值范围 `[0.5, 2.0]`。小于 `1.0` 减慢，大于 `1.0` 加快。                                                                                                                                                                                                                                                         |
| `pitch`                  | float     | 否    | 音调倍数。默认值 `1.0`，取值范围 `[0.5, 2.0]`。大于 `1.0` 升高音调，小于 `1.0` 降低音调。                                                                                                                                                                                                                                                   |
| `bit_rate`               | int       | 否    | 音频比特率。仅在 `format` 为 `mp3` 或 `opus` 时有效。                                                                                                                                                                                                                                                                         |
| `enable_ssml`            | boolean   | 否    | 是否开启 SSML 功能。默认值 `false`。`playStreamInputTts` 和 `asyncPlayStreamInputTts` 接口默认启用 SSML，如需关闭可显式设置为 `false`。SSML 的使用限制请参见 [SSML 使用限制](/developer-guides/speech/ssml#使用限制)。                                                                                                                                         |
| `word_timestamp_enabled` | boolean   | 否    | 是否开启词级别时间戳。默认值 `false`。仅在流式输出模式下可用。支持的音色范围：cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash、cosyvoice-v3-plus 和 cosyvoice-v2 模型的复刻音色，以及[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)中标记为支持的系统音色。其他模型的复刻音色不支持此功能。时间戳结果在 `onStreamInputTtsEventCallback` 的 `all_response` 中返回。 |
| `seed`                   | int       | 否    | 随机数种子，使合成效果产生变化。在模型版本、文本、音色及其他参数均相同的前提下，使用相同的 seed 可复现相同的合成结果。默认值 `0`，取值范围 `[0, 65535]`。`cosyvoice-v1` 不支持该功能。                                                                                                                                                                                                  |
| `language_hints`         | String\[] | 否    | 语言提示。                                                                                                                                                                                                                                                                                                           |
| `instruction`            | String    | 否    | 情感或风格指令。                                                                                                                                                                                                                                                                                                        |

## 核心接口

### NativeNui

#### startStreamInputTts

启动双向流式语音合成，建立与服务端的连接，并注册回调以接收事件和音频数据。

<Warning>
  该方法会阻塞调用线程，请在非 UI 线程中调用。
</Warning>

**方法签名**

```java
public synchronized int startStreamInputTts(INativeStreamInputTtsCallback callback,
                                            String ticket,
                                            String parameters,
                                            String session_id,
                                            int log_level,
                                            boolean save_log)
```

**参数**

| 参数           | 类型                            | 描述                                                                                             |
| ------------ | ----------------------------- | ---------------------------------------------------------------------------------------------- |
| `callback`   | INativeStreamInputTtsCallback | 事件和数据回调接口的实现。                                                                                  |
| `ticket`     | String                        | JSON 字符串，包含认证、连接和调试参数。参见[连接与控制参数](#连接与控制参数)。                                                   |
| `parameters` | String                        | JSON 字符串，包含语音合成的具体效果参数。参见[语音合成效果参数](#语音合成效果参数)。                                                |
| `session_id` | String                        | 客户端指定的会话 ID。若不传入，服务端将自动生成。                                                                     |
| `log_level`  | int                           | 控制 SDK 自身日志的打印级别。取值：`0` = VERBOSE，`1` = DEBUG，`2` = INFO，`3` = WARNING，`4` = ERROR，`5` = NONE。 |
| `save_log`   | boolean                       | 是否保存本地日志。若为 `true`，需在[连接与控制参数](#连接与控制参数)中通过 `debug_path` 指定路径，可选设置 `max_log_file_size`。        |

**返回值**

返回错误码，参见[错误码参考](/api-reference/preparation/error-messages)。

---

#### sendStreamInputTts

发送待合成的文本，与 `startStreamInputTts` 搭配使用。在调用 `startStreamInputTts` 后，使用此接口持续发送文本。所有文本发送完毕后，需调用 `stopStreamInputTts` 或 `asyncStopStreamInputTts` 来结束发送。

**方法签名**

```java
public synchronized int sendStreamInputTts(String text)
```

**参数**

| 参数     | 类型     | 描述                                               |
| ------ | ------ | ------------------------------------------------ |
| `text` | String | 待合成文本。不支持 SSML，如果传入的文本包含 SSML 标签，这些标签将被当作普通文本读出。 |

**返回值**

返回错误码，参见[错误码参考](/api-reference/preparation/error-messages)。

---

#### stopStreamInputTts

同步接口，通知服务端文本已全部发送，并阻塞等待所有音频数据合成并收到 `STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE`。阻塞等待的超时时间由参数 `complete_waiting_ms` 控制。

**方法签名**

```java
public synchronized int stopStreamInputTts()
```

**返回值**

返回错误码，参见[错误码参考](/api-reference/preparation/error-messages)。

---

#### asyncStopStreamInputTts

异步接口，通知服务端文本已全部发送。调用后立即返回，合成在后台继续进行。通过 `STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE` 事件判断合成是否完成。

**方法签名**

```java
public synchronized int asyncStopStreamInputTts()
```

**返回值**

返回错误码，参见[错误码参考](/api-reference/preparation/error-messages)。

---

#### cancelStreamInputTts

立即中断与服务端的连接并终止当前合成任务。调用后不会再收到任何音频数据回调。

**方法签名**

```java
public synchronized int cancelStreamInputTts()
```

**返回值**

返回错误码，参见[错误码参考](/api-reference/preparation/error-messages)。

---

#### playStreamInputTts

同步执行的一次性合成接口。该接口会发送文本、阻塞并等待接收所有音频数据，直到合成完成后才返回。无需再调用 stop 接口。

该接口默认启用 SSML。如果在[语音合成效果参数](#语音合成效果参数)中显式设置 `enable_ssml`，则以用户设置为准。

<Warning>
  该方法会阻塞调用线程，请在非 UI 线程中调用。
</Warning>

**方法签名**

```java
public synchronized int playStreamInputTts(INativeStreamInputTtsCallback callback,
                                           String ticket,
                                           String parameters,
                                           String text,
                                           String session_id,
                                           int log_level,
                                           boolean save_log)
```

**参数**

`callback`、`ticket` 等参数与 `startStreamInputTts` 接口中的定义相同。

| 参数     | 类型     | 描述             |
| ------ | ------ | -------------- |
| `text` | String | 待合成文本。支持 SSML。 |

**返回值**

返回错误码，参见[错误码参考](/api-reference/preparation/error-messages)。

---

#### asyncPlayStreamInputTts

异步执行的一次性合成接口。调用后立即返回，合成任务在后台进行，结果通过回调返回。无需再调用 stop 接口。

该接口默认启用 SSML。如果在[语音合成效果参数](#语音合成效果参数)中显式设置 `enable_ssml`，则以用户设置为准。

**方法签名**

```java
public synchronized int asyncPlayStreamInputTts(INativeStreamInputTtsCallback callback,
                                           String ticket,
                                           String parameters,
                                           String text,
                                           String session_id,
                                           int log_level,
                                           boolean save_log)
```

**参数**

`callback`、`ticket` 等参数与 `startStreamInputTts` 接口中的定义相同。

| 参数     | 类型     | 描述             |
| ------ | ------ | -------------- |
| `text` | String | 待合成文本。支持 SSML。 |

**返回值**

返回错误码，参见[错误码参考](/api-reference/preparation/error-messages)。

---

### INativeStreamInputTtsCallback

#### onStreamInputTtsEventCallback

合成生命周期事件回调。

**方法签名**

```java
void onStreamInputTtsEventCallback(StreamInputTtsEvent event,
                                   String task_id,
                                   String session_id,
                                   int ret_code,
                                   String error_msg,
                                   String timestamp,
                                   String all_response);
```

**参数**

| 参数             | 类型                  | 描述                                                                                                       |
| -------------- | ------------------- | -------------------------------------------------------------------------------------------------------- |
| `event`        | StreamInputTtsEvent | 回调事件，参见下方 [StreamInputTtsEvent](#streaminputttsevent)。                                                   |
| `task_id`      | String              | 语音合成任务 ID。                                                                                               |
| `session_id`   | String              | 会话 ID。客户端传入则原样返回；未传入时由服务端生成。                                                                             |
| `ret_code`     | int                 | 错误码，仅当事件为 `STREAM_INPUT_TTS_EVENT_TASK_FAILED` 时有效。参见[错误码参考](/api-reference/preparation/error-messages)。 |
| `error_msg`    | String              | 错误信息，仅当事件为 `STREAM_INPUT_TTS_EVENT_TASK_FAILED` 时有效。                                                     |
| `timestamp`    | String              | 合成结果的时间戳信息。                                                                                              |
| `all_response` | String              | 完整的 JSON 字符串响应。可解析以获取所需数据。                                                                               |

---

#### onStreamInputTtsDataCallback

合成过程中，SDK 会连续触发此回调，需在回调中获取音频数据。

**方法签名**

```java
void onStreamInputTtsDataCallback(byte[] data);
```

**参数**

| 参数     | 类型      | 描述         |
| ------ | ------- | ---------- |
| `data` | byte\[] | 当前片段的音频数据。 |

<Note>
  - 对 mp3/opus 压缩格式，分段传输必须使用流式播放器，不能逐帧播放，否则可能解码失败。
  - 组装完整文件时需采用追加模式写入同一文件。
  - 对于 wav 和 mp3 格式，仅在第一次回调的数据中包含文件头，后续回调均为纯音频数据。处理时需将所有回调的 `buffer` 按顺序拼接。opus 格式的每一帧都是独立的 Ogg page，可直接拼接。
</Note>

---

#### onStreamInputTtsLogTrackCallback

SDK 内部追踪日志回调，用于问题排查和调试。

**方法签名**

```java
default void onStreamInputTtsLogTrackCallback(Constants.LogLevel level, String log)
```

---

### StreamInputTtsEvent

| 事件                                          | 描述                                                                                                             |
| ------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `STREAM_INPUT_TTS_EVENT_SYNTHESIS_STARTED`  | 服务端已成功接收请求并开始处理。通常在此事件后，`onStreamInputTtsDataCallback` 将很快开始返回第一批音频数据。                                         |
| `STREAM_INPUT_TTS_EVENT_SENTENCE_SYNTHESIS` | 语音合成运行过程中的信息，包括计费信息等。                                                                                          |
| `STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE` | 服务端已发送完全部音频数据，此后 `onStreamInputTtsDataCallback` 将不会再被调用。收到此事件是数据流结束的明确信号。                                      |
| `STREAM_INPUT_TTS_EVENT_TASK_FAILED`        | 任务失败。此时可从 `onStreamInputTtsEventCallback` 的 `all_response` 获得 `task_id`、`error_code`、`error_message` 用于判断具体错误。 |

错误响应结构示例：

```json
{
  "header": {
    "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
    "event": "task-failed",
    "error_code": "InvalidParameter",
    "error_message": "[tts:]Engine return error code: 418",
    "attributes": {}
  },
  "payload": {}
}
```

## 高级功能

### SSML 标记语言

通过在文本中嵌入 XML 标签，实现对发音、语速、停顿等细节的精确控制。

**使用限制**：

- 仅适用于 `cosyvoice-v2` 模型。
- 仅支持一次性输入文本方式（`playStreamInputTts` 或 `asyncPlayStreamInputTts` 接口），不支持流式输入文本方式（`sendStreamInputTts` 接口）。

**使用方法**：调用 `playStreamInputTts` 或 `asyncPlayStreamInputTts` 接口时，SDK 会自动启用 SSML，直接在 `text` 参数中传入包含 SSML 标签的文本即可。

### 数学表达式

使模型能够正确朗读常见的数学公式和表达式。

**使用限制**：仅适用于 `cosyvoice-v2` 模型。

**使用方法**：直接在 `text` 参数中传入包含 LaTeX 格式的数学表达式的文本即可。

## 限制与约束

### 文本长度限制

- **一次性输入文本**（`playStreamInputTts`/`asyncPlayStreamInputTts`）：发送文本长度不超过 20000 字符。
- **流式输入文本**（`sendStreamInputTts`）：单次发送文本长度不超过 20000 字符，且累计发送文本总长度不超过 20 万字符。

### 文本编码格式

需采用 UTF-8 编码。
