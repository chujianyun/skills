> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 语音合成 Qwen-Audio-TTS/CosyVoice iOS SDK

> 使用 Qwen-Audio-TTS/CosyVoice iOS SDK 将文本实时合成为高质量语音，支持流式与一次性文本输入两种调用方式

本文档提供了语音合成 CosyVoice iOS SDK 的详细使用指南，帮助您将文本转换为高质量、富有表现力的语音。

**用户指南**：关于模型介绍和选型建议请参见[语音合成模型](/developer-guides/speech/tts-models)。

## 限制与约束

### 文本长度限制

- **一次性输入待合成文本**：发送文本长度不得超过 20000 字符。
- **流式输入待合成文本**：单次发送文本长度不得超过 20000 字符，且累计发送文本总长度不得超过 20 万字符。

### 文本编码格式

需采用 UTF-8 编码。

## 快速开始

1. **获取 API Key**：[获取 API Key](/api-reference/preparation/api-key)

   <Note>
     当需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用临时 API Key。临时 API Key 拥有固定的 60 秒有效期，过期后需重新获取。
   </Note>

2. **下载 SDK 并运行示例代码**：

   - 下载最新 SDK 整合包。
   - 解压 ZIP 包，将其中的 `nuisdk.framework` 添加到工程。
   - 在 **Build Phases → Link Binary With Libraries** 中添加 `nuisdk.framework`。
   - 在 **General → Frameworks, Libraries, and Embedded Content** 中将 `nuisdk.framework` 设置为 **Embed & Sign**。
   - 用 Xcode 打开示例工程。示例代码位于 `DashCosyVoiceStreamInputTTSViewController`，替换 API Key 后体验功能。

### 调用方式

| 调用方式       | 说明                                                                                                                                                                                                                                                                                                                           |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 一次性输入待合成文本 | **调用步骤**：1. 初始化 SDK 和播放器组件。2. 按业务需求设置参数。3. 调用 `playStreamInputTts` 或 `asyncPlayStreamInputTts` 发送文本并开始语音合成。4. 接收到 `TTS_EVENT_SYNTHESIS_COMPLETE` 回调，语音合成结束。**适用场景**：短文本合成、需要使用 SSML 标记语言。                                                                                                                                    |
| 流式输入待合成文本  | **调用步骤**：1. 初始化 SDK 和播放器组件。2. 按业务需求设置参数。3. 调用 `startStreamInputTts` 开始流式文本语音合成。4. 调用 `sendStreamInputTts` 持续发送文本。5. 在 `onStreamInputTtsDataCallback` 中获取二进制音频数据。6. 调用 `stopStreamInputTts` 或 `asyncStopStreamInputTts` 结束发送，等待合成完成。7. 接收到 `TTS_EVENT_SYNTHESIS_COMPLETE` 回调，语音合成结束。**适用场景**：实时对话、长文本"边说边合"；此方式不支持 SSML 标记语言。 |

## 请求参数

### 连接与控制参数

通过在 `startStreamInputTts`、`playStreamInputTts` 和 `asyncPlayStreamInputTts` 接口的 `ticket` 参数中传入一个 JSON 字符串来配置。

**参数示例**（以下为 JSON 字符串示例，参数未完整列出，请按实际需求补充）：

```json
{
  "url": "wss://dashscope.aliyuncs.com/api-ws/v1/inference",
  "apikey": "$DASHSCOPE_API_KEY",
  "device_id": "my_device_id"
}
```

**参数说明**：

| 参数                    | 类型     | 是否必须 | 说明                                                                                                                                                                                                                         |
| --------------------- | ------ | ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url`                 | string | 是    | 服务地址，固定为 `wss://dashscope.aliyuncs.com/api-ws/v1/inference`。                                                                                                                                                               |
| `apikey`              | string | 是    | API Key。建议使用时效性短、安全性更高的临时 API Key，以降低长期有效 Key 泄露的风险。                                                                                                                                                                       |
| `device_id`           | string | 是    | 用于标识终端用户的唯一字符串，可设为应用内用户 ID 或客户端生成的设备唯一标识符。此 ID 主要用于日志追踪和问题排查。                                                                                                                                                              |
| `complete_waiting_ms` | int    | 否    | 调用 `stopStreamInputTts` 接口后，等待合成完成事件（`TTS_EVENT_SYNTHESIS_COMPLETE`）的超时时间（毫秒）。默认值：`10000`。                                                                                                                                 |
| `debug_path`          | string | 否    | 日志文件的存储路径。此参数仅在调用 `startStreamInputTts`、`playStreamInputTts` 或 `asyncPlayStreamInputTts` 接口时将 `saveLog` 设为 `YES` 时生效。此时必须设置日志文件路径，否则将报错。本地最多保留两个日志文件。                                                                      |
| `max_log_file_size`   | int    | 否    | 设定日志文件的最大字节数。此参数仅在 `saveLog` 设为 `YES` 时生效。默认值：`104857600`（100 MiB）。                                                                                                                                                        |
| `log_track_level`     | int    | 否    | 控制通过日志回调（`onStreamInputTtsLogTrackCallback`）对外发送的日志内容的过滤级别。默认值：`2`。取值范围：`0`（VERBOSE）、`1`（DEBUG）、`2`（INFO）、`3`（WARNING）、`4`（ERROR）、`5`（NONE，关闭此功能）。注意：`log_track_level` 与 `logLevel`（通过初始化接口设置）共同决定最终回调的日志，日志级别必须同时满足两者的阈值。 |

### 语音合成效果参数

通过在 `startStreamInputTts`、`playStreamInputTts` 和 `asyncPlayStreamInputTts` 接口的 `parameters` 参数中传入一个 JSON 字符串来配置。

**参数示例**（以下为 JSON 字符串示例，参数未完整列出，请按实际需求补充）：

```json
{
  "model": "cosyvoice-v2",
  "voice": "longxiaochun_v2",
  "format": "mp3",
  "sample_rate": 24000,
  "volume": 50,
  "rate": 1,
  "pitch": 1,
  "language_hints": ["zh"],
  "enable_ssml": false
}
```

**参数说明**：

| 参数                       | 类型             | 是否必须 | 说明                                                                                                                                                                                                                                                                                                            |
| ------------------------ | -------------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model`                  | string         | 是    | 语音合成模型。可选值：`cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`、`cosyvoice-v3-plus`、`cosyvoice-v3-flash`、`cosyvoice-v2`。                                                                                                                                                                                              |
| `voice`                  | string         | 是    | 音色。可选值：系统音色（参见[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)）、声音复刻音色、声音设计音色（创建方法参见 [CosyVoice 声音复刻/设计 API](/api-reference/speech-synthesis/voice-cloning/create-voice)）。                                                                                                               |
| `format`                 | string         | 否    | 音频编码格式。默认值：`mp3`。可选值：`mp3`、`pcm`、`wav`、`opus`。                                                                                                                                                                                                                                                                |
| `volume`                 | int            | 否    | 音量。默认值：`50`。取值范围：\[0, 100]。50 代表标准音量，0 为静音，100 为最大音量。                                                                                                                                                                                                                                                         |
| `sample_rate`            | int            | 否    | 音频采样率（单位：Hz）。默认值：`22050`。可选值：8000、16000、22050、24000、44100、48000。默认采样率代表当前音色的最佳采样率，同时支持降采样或升采样。                                                                                                                                                                                                                |
| `rate`                   | float          | 否    | 语速。默认值：`1.0`。取值范围：\[0.5, 2.0]。1.0 为标准语速，小于 1.0 则减慢，大于 1.0 则加快。                                                                                                                                                                                                                                                |
| `pitch`                  | float          | 否    | 音高。默认值：`1.0`。取值范围：\[0.5, 2.0]。1.0 为音色自然音高，大于 1.0 音高升高，小于 1.0 音高降低。                                                                                                                                                                                                                                            |
| `bit_rate`               | int            | 否    | 音频码率（单位：kbps）。默认值：`32`。取值范围：\[6, 510]。仅在 `format` 为 `opus` 时支持。                                                                                                                                                                                                                                               |
| `enable_ssml`            | boolean        | 否    | 是否开启 SSML 功能。SSML 的使用限制请参见 [SSML 使用限制](/developer-guides/speech/ssml#使用限制)。                                                                                                                                                                                                                                   |
| `word_timestamp_enabled` | boolean        | 否    | 是否开启字级别时间戳。默认值：`false`。仅在流式输出模式下可用。支持的音色范围：cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash、cosyvoice-v3-plus 和 cosyvoice-v2 模型的复刻音色，以及[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)中标记为支持的系统音色。其他模型的复刻音色不支持此功能。时间戳结果在 `onStreamInputTtsEventCallback` 的 `all_response` 中。 |
| `seed`                   | int            | 否    | 生成时使用的随机数种子，用于复现相同合成结果。在模型版本、文本、音色及其他参数均相同的前提下，使用相同的 seed 可复现相同的合成结果。默认值：`0`。取值范围：\[0, 65535]。                                                                                                                                                                                                                |
| `language_hints`         | array\[string] | 否    | 指定语音合成的目标语言，提升合成效果。可选值：`zh`、`en`、`fr`、`de`、`ja`、`ko`、`ru`、`pt`、`th`、`id`、`vi`、`it`、`ms`。注意：此参数为数组，当前版本仅处理第一个元素，建议只传入一个值。                                                                                                                                                                                      |
| `instruction`            | string         | 否    | 设置指令，用于控制方言、情感或角色等合成效果。长度限制：100 字符（汉字按 2 个字符计算）。仅适用于 cosyvoice-v3.5-flash、cosyvoice-v3.5-plus 和 cosyvoice-v3-flash 的复刻音色，以及音色列表中标记为支持 Instruct 的系统音色。                                                                                                                                                         |
| `enable_aigc_tag`        | boolean        | 否    | 是否在生成的音频中添加 AIGC 隐性标识。设置为 `true` 时，将隐性标识嵌入到支持格式（wav/mp3/opus）的音频中。默认值：`false`。                                                                                                                                                                                                                                |
| `aigc_propagator`        | string         | 否    | 设置 AIGC 隐性标识中的 `ContentPropagator` 字段，用于标识内容传播者。仅在 `enable_aigc_tag` 为 `true` 时生效。                                                                                                                                                                                                                            |
| `aigc_propagate_id`      | string         | 否    | 设置 AIGC 隐性标识中的 `PropagateID` 字段，用于唯一标识一次具体的传播行为。仅在 `enable_aigc_tag` 为 `true` 时生效。                                                                                                                                                                                                                            |

## 关键接口

### StreamInputTts

#### startStreamInputTts

启动流式语音合成任务，与服务端建立连接。

**方法签名**：

```objc
- (int) startStreamInputTts:(const char *)ticket
                 parameters:(const char *)parameters
                  sessionId:(const char *)sessionId
                   logLevel:(NuiSdkLogLevel)logLevel
                    saveLog:(BOOL)saveLog;
```

**参数说明**：

| 参数           | 类型               | 说明                                                                                            |
| ------------ | ---------------- | --------------------------------------------------------------------------------------------- |
| `ticket`     | `char*`          | JSON 字符串，包含鉴权、连接和调试参数。参见[连接与控制参数](#连接与控制参数)。                                                  |
| `parameters` | `char*`          | JSON 字符串，包含语音合成的具体效果参数。参见[语音合成效果参数](#语音合成效果参数)。                                               |
| `sessionId`  | `char*`          | 客户端指定的会话 ID。若不传入，服务端将自动生成。                                                                    |
| `logLevel`   | `NuiSdkLogLevel` | 控制 SDK 自身日志的打印级别。                                                                             |
| `saveLog`    | `BOOL`           | 是否保存本地日志。若为 `YES`，须在[连接与控制参数](#连接与控制参数)中通过 `debug_path` 指定路径，并可通过 `max_log_file_size` 设置文件大小。 |

**返回值**：返回错误码，参见[错误码查询](/api-reference/preparation/error-messages)。

#### sendStreamInputTts

发送待合成的文本，与 `startStreamInputTts` 搭配使用。

在调用 `startStreamInputTts` 后，使用此接口持续发送文本。所有文本发送完毕后，需调用 `stopStreamInputTts` 或 `asyncStopStreamInputTts` 来结束发送。

**方法签名**：

```objc
- (int) sendStreamInputTts:(const char *)text;
```

**参数说明**：

| 参数     | 类型      | 说明                                                     |
| ------ | ------- | ------------------------------------------------------ |
| `text` | `char*` | 待合成文本。不支持 SSML。如果传入的文本包含 SSML 标签，这些标签将被当作普通文本读出，不会被解析。 |

**返回值**：返回错误码，参见[错误码查询](/api-reference/preparation/error-messages)。

#### stopStreamInputTts

同步接口，通知服务端文本已全部发送，并阻塞等待所有音频数据合成并收到 `TTS_EVENT_SYNTHESIS_COMPLETE`。

阻塞等待的超时时间由参数 `complete_waiting_ms` 控制。

**方法签名**：

```objc
- (int) stopStreamInputTts;
```

**返回值**：返回错误码，参见[错误码查询](/api-reference/preparation/error-messages)。

#### asyncStopStreamInputTts

异步接口，通知服务端文本已全部发送。调用后立即返回，合成在后台继续进行。

通过 `TTS_EVENT_SYNTHESIS_COMPLETE` 判断合成是否完成。

**方法签名**：

```objc
- (int) asyncStopStreamInputTts;
```

**返回值**：返回错误码，参见[错误码查询](/api-reference/preparation/error-messages)。

#### cancelStreamInputTts

立即中断与服务端的连接并终止当前合成任务。调用后不会再收到任何音频数据回调。

**方法签名**：

```objc
- (int) cancelStreamInputTts;
```

**返回值**：返回错误码，参见[错误码查询](/api-reference/preparation/error-messages)。

#### playStreamInputTts

异步执行的一次性合成接口。调用后立即返回，合成任务在后台进行，结果通过回调返回。无需再调用 stop 接口。

该接口默认启用 SSML。如果在[语音合成效果参数](#语音合成效果参数)中显式设置 `enable_ssml`，则以用户设置为准。

**方法签名**：

```objc
- (int) playStreamInputTts:(const char *)ticket
                parameters:(const char *)parameters
                      text:(const char *)text
                 sessionId:(const char *)sessionId
                  logLevel:(NuiSdkLogLevel)logLevel
                   saveLog:(BOOL)saveLog;
```

**参数说明**：

`ticket`、`parameters` 等参数与 `startStreamInputTts` 接口中的定义相同。

| 参数     | 类型      | 说明                                              |
| ------ | ------- | ----------------------------------------------- |
| `text` | `char*` | 待合成文本。支持 [SSML](/developer-guides/speech/ssml)。 |

**返回值**：返回错误码，参见[错误码查询](/api-reference/preparation/error-messages)。

#### asyncPlayStreamInputTts

此接口异步发送全部待合成文本。调用后立即返回，不等待合成数据。无需再调用 stop 接口。

该接口默认启用 SSML。如果在[语音合成效果参数](#语音合成效果参数)中显式设置 `enable_ssml`，则以用户设置为准。

**方法签名**：

```objc
- (int) asyncPlayStreamInputTts:(const char *)ticket
                     parameters:(const char *)parameters
                           text:(const char *)text
                      sessionId:(const char *)sessionId
                       logLevel:(NuiSdkLogLevel)logLevel
                        saveLog:(BOOL)saveLog;
```

**参数说明**：

`ticket`、`parameters` 等参数与 `startStreamInputTts` 接口中的定义相同。

| 参数     | 类型      | 说明                                              |
| ------ | ------- | ----------------------------------------------- |
| `text` | `char*` | 待合成文本。支持 [SSML](/developer-guides/speech/ssml)。 |

**返回值**：返回错误码，参见[错误码查询](/api-reference/preparation/error-messages)。

### StreamInputTtsDelegate: 监听回调

#### onStreamInputTtsEventCallback: 监听事件

**方法签名**：

```objc
- (void)onStreamInputTtsEventCallback:(StreamInputTtsCallbackEvent)event
                                taskId:(char*)taskid
                             sessionId:(char*)sessionId
                              ret_code:(int)ret_code
                             error_msg:(char*)error_msg
                             timestamp:(char*)timestamp
                          all_response:(char*)all_response;
```

**参数说明**：

| 参数             | 类型                            | 说明                                                                                         |
| -------------- | ----------------------------- | ------------------------------------------------------------------------------------------ |
| `event`        | `StreamInputTtsCallbackEvent` | 回调事件。参见 [StreamInputTtsCallbackEvent](#streaminputttscallbackevent-事件类型)。                  |
| `taskid`       | `char*`                       | 语音合成任务 ID。                                                                                 |
| `sessionId`    | `char*`                       | 会话 ID。客户端传入则原样返回；未传入时由服务端生成。                                                               |
| `ret_code`     | `int`                         | 错误码，仅在事件 `TTS_EVENT_TASK_FAILED` 中有效。参见[错误码查询](/api-reference/preparation/error-messages)。 |
| `error_msg`    | `char*`                       | 错误信息，仅在事件 `TTS_EVENT_TASK_FAILED` 中有效。                                                     |
| `timestamp`    | `char*`                       | 合成结果的时间戳信息。                                                                                |
| `all_response` | `char*`                       | 完整的 JSON 字符串响应。可解析以获取所需数据。                                                                 |

#### onStreamInputTtsDataCallback: 监听音频数据

合成过程中，SDK 会连续触发此回调，需在回调中获取音频数据。

**方法签名**：

```objc
- (void)onStreamInputTtsDataCallback:(char*)buffer len:(int)len;
```

**参数说明**：

| 参数       | 类型      | 说明                                             |
| -------- | ------- | ---------------------------------------------- |
| `buffer` | `char*` | 返回当前片段的音频数据。可用于合成完整的音频文件并播放，或通过支持流式播放的播放器实时播放。 |
| `len`    | `int`   | 音频数据的长度（字节）。                                   |

<Note>
  - 对 mp3/opus 压缩格式，分段传输必须使用流式播放器，不能逐帧播放，否则可能解码失败。
  - 组装完整文件时需采用追加模式写入同一文件。
  - 对于 wav 和 mp3 格式，仅在第一次 `onStreamInputTtsDataCallback` 回调的数据中包含文件头，后续回调均为纯音频数据。处理时需将所有回调的 `buffer` 按顺序拼接。opus 格式的每一帧都是独立的 Ogg page，可直接拼接。
</Note>

#### onStreamInputTtsLogTrackCallback: 监听追踪日志

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

**方法签名**：

```objc
- (void)onStreamInputTtsLogTrackCallback:(NuiSdkLogLevel)level
                              logMessage:(const char *)log;
```

### StreamInputTtsCallbackEvent: 事件类型

| 事件                             | 说明                                                                                                               |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| `TTS_EVENT_SYNTHESIS_STARTED`  | 表示服务端已成功接收请求并开始处理。通常在此事件后，`onStreamInputTtsDataCallback` 将很快开始返回第一批音频数据。                                         |
| `TTS_EVENT_SENTENCE_SYNTHESIS` | 语音合成运行过程中的信息，包括计费信息等。                                                                                            |
| `TTS_EVENT_SYNTHESIS_COMPLETE` | 表示服务端已发送完全部音频数据，此后 `onStreamInputTtsDataCallback` 将不会再被调用。收到此事件是数据流结束的明确信号。                                      |
| `TTS_EVENT_TASK_FAILED`        | 表示任务失败。此时可从 `onStreamInputTtsEventCallback` 的 `all_response` 获得 `task_id`、`error_code`、`error_message` 用于判断具体错误。 |

`TTS_EVENT_TASK_FAILED` 时 `all_response` 示例：

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

**目的**：通过在文本中嵌入 XML 标签，实现对发音、语速、停顿等细节的精确控制。

**使用限制**：

- **模型**：仅适用于 `cosyvoice-v2` 模型。
- **调用方式**：仅支持一次性输入待合成文本（`playStreamInputTts` 或 `asyncPlayStreamInputTts` 接口），不支持流式输入待合成文本（`sendStreamInputTts` 接口）。

**使用方法**：调用 `playStreamInputTts` 或 `asyncPlayStreamInputTts` 接口时，SDK 会自动启用 SSML，此时直接在 `text` 参数中传入包含 SSML 标签的文本即可。

详细的标签用法参考 [SSML 标记语言](/developer-guides/speech/ssml)。

### 数学表达式

**目的**：使模型能够正确朗读常见的数学公式和表达式。

**使用限制**：仅适用于 `cosyvoice-v2` 模型。

**使用方法**：直接在 `text` 参数中传入包含 LaTeX 格式的数学表达式的文本即可。详情参见 [LaTeX 公式朗读](/developer-guides/speech/ssml#latex-公式转语音)。
