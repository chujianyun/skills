> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 实时语音识别（Qwen-ASR-Realtime）Java SDK

> Qwen ASR Java 集成指南

**使用指南**： 模型概述、功能特性和完整示例代码请参见[实时语音识别](/developer-guides/speech/asr-realtime)。

<Note>请确保 DashScope Java SDK 版本不低于 2.22.5。</Note>

## 交互模式

Qwen-ASR-Realtime 支持两种模式：

| 模式             | `enableTurnDetection` | 工作方式                            |
| -------------- | --------------------- | ------------------------------- |
| **VAD 模式**（默认） | `true`                | 服务端通过 VAD 检测语音边界，自动提交音频缓冲区进行识别。 |
| **手动模式**       | `false`               | 您通过调用 `commit()` 手动控制音频提交时机。    |

详情请参见 [VAD 模式](/developer-guides/speech/asr-realtime#interaction-flow-qwen-asr-realtime)和[手动模式](/developer-guides/speech/asr-realtime#manual-mode)。

## 请求参数

### 连接参数 (OmniRealtimeParam)

通过 `OmniRealtimeParam` 的链式方法设置。

<Accordion title="点击查看示例代码">
  ```java
  OmniRealtimeParam param = OmniRealtimeParam.builder()
    .model("qwen3-asr-flash-realtime")
    .url("wss://dashscope.aliyuncs.com/api-ws/v1/realtime")
    // 如果未配置环境变量，请将下面一行替换为 .apikey("sk-xxx")。
    .apikey(System.getenv("DASHSCOPE_API_KEY"))
    .build();
  ```
</Accordion>

| 参数       | 类型       | 必选 | 说明                                                      |
| -------- | -------- | -- | ------------------------------------------------------- |
| `model`  | `String` | 是  | 模型名称。示例：`qwen3-asr-flash-realtime`。                     |
| `url`    | `String` | 是  | 服务端点：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime`。 |
| `apikey` | `String` | 否  | API Key。                                                |

### 会话配置 (OmniRealtimeConfig)

通过 `OmniRealtimeConfig` 的链式方法设置。

<Accordion title="点击查看示例代码">
  ```java
  OmniRealtimeTranscriptionParam transcriptionParam = new OmniRealtimeTranscriptionParam();
  transcriptionParam.setLanguage("zh");
  transcriptionParam.setInputSampleRate(16000);
  transcriptionParam.setInputAudioFormat("pcm");

  OmniRealtimeConfig config = OmniRealtimeConfig.builder()
    .modalities(Collections.singletonList(OmniRealtimeModality.TEXT))
    .enableTurnDetection(true)
    .turnDetectionType("server_vad")
    .turnDetectionThreshold(0.0f)
    .turnDetectionSilenceDurationMs(400)
    .transcriptionConfig(transcriptionParam)
    .build();
  ```
</Accordion>

| 参数                               | 类型                               | 必选 | 说明                                                                                                                                  |
| -------------------------------- | -------------------------------- | -- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `modalities`                     | `List<OmniRealtimeModality>`     | 是  | 输出模态。固定为 `[OmniRealtimeModality.TEXT]`。                                                                                             |
| `enableTurnDetection`            | `boolean`                        | 否  | 是否启用服务端 VAD。禁用后需调用 `commit()` 手动触发识别。默认值：`true`。                                                                                    |
| `turnDetectionType`              | `String`                         | 否  | VAD 类型。固定为 `server_vad`。                                                                                                            |
| `turnDetectionThreshold`         | `float`                          | 否  | VAD 阈值。推荐值：`0.0`。默认值：`0.2`。取值范围：`[-1, 1]`。值越低灵敏度越高，但可能将背景噪音误判为语音；值越高灵敏度越低，适合嘈杂环境。                                                   |
| `turnDetectionSilenceDurationMs` | `int`                            | 否  | VAD 静音阈值，单位毫秒。静音超过该时长即视为一句话结束。推荐值：`400`。默认值：`800`。取值范围：`[200, 6000]`。较低值（如 300 ms）可加快响应，但可能在正常停顿处断句；较高值（如 1200 ms）能更好地处理长停顿，但会增加延迟。 |
| `transcriptionConfig`            | `OmniRealtimeTranscriptionParam` | 否  | 语音识别设置。详见[转写参数](#转写参数-omnirealtimetranscriptionparam)。                                                                              |

### 转写参数 (OmniRealtimeTranscriptionParam)

通过 `OmniRealtimeTranscriptionParam` 的 setter 方法设置。

<Accordion title="点击查看示例代码">
  ```java
  OmniRealtimeTranscriptionParam transcriptionParam = new OmniRealtimeTranscriptionParam();
  transcriptionParam.setLanguage("zh");
  transcriptionParam.setInputSampleRate(16000);
  transcriptionParam.setInputAudioFormat("pcm");
  ```
</Accordion>

| 参数                 | 类型       | 必选 | 说明                                                                                                                                                                                                                                                                                                         |
| ------------------ | -------- | -- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `language`         | `String` | 否  | 音频的源语言。支持的值：`zh`（中文——普通话、四川话、闽南话和吴语）、`yue`（粤语）、`en`（英语）、`ja`（日语）、`de`（德语）、`ko`（韩语）、`ru`（俄语）、`fr`（法语）、`pt`（葡萄牙语）、`ar`（阿拉伯语）、`it`（意大利语）、`es`（西班牙语）、`hi`（印地语）、`id`（印尼语）、`th`（泰语）、`tr`（土耳其语）、`uk`（乌克兰语）、`vi`（越南语）、`cs`（捷克语）、`da`（丹麦语）、`fil`（菲律宾语）、`fi`（芬兰语）、`is`（冰岛语）、`ms`（马来语）、`no`（挪威语）、`pl`（波兰语）、`sv`（瑞典语）。 |
| `inputSampleRate`  | `int`    | 否  | 音频采样率，单位 Hz。支持：`16000`、`8000`。默认值：`16000`。设为 `8000` 时服务端会上采样至 16000 Hz，可能带来轻微延迟。仅在音频源为 8000 Hz（如电话线路）时使用 `8000`。                                                                                                                                                                                           |
| `inputAudioFormat` | `String` | 否  | 音频格式。支持：`pcm`、`opus`。默认值：`pcm`。                                                                                                                                                                                                                                                                            |
| `corpusText`       | `String` | 否  | 上下文信息（背景文本、实体词表、参考资料），用于定制识别效果。上限：10,000 个 token。详见[上下文偏置](/developer-guides/speech/asr-realtime#core-usage-context-biasing-qwen-asr)。                                                                                                                                                                     |

## 核心接口

### OmniRealtimeConversation

导入路径：`com.alibaba.dashscope.audio.omni.OmniRealtimeConversation`

管理 WebSocket 的生命周期：建立连接、发送音频和结束会话。

#### 创建会话

```java
OmniRealtimeConversation conversation =
  new OmniRealtimeConversation(param, callback);
```

使用指定的连接参数和回调处理器创建会话。

#### 连接服务端

```java
conversation.connect();
```

建立 WebSocket 连接。服务端发送 [session.created](/api-reference/speech-recognition/qwen-asr-realtime/server-events) 和 [session.updated](/api-reference/speech-recognition/qwen-asr-realtime/server-events) 事件。

异常类型：`NoApiKeyException`、`InterruptedException`。

#### 配置会话

```java
conversation.updateSession(config);
```

连接建立后更新会话配置。服务端发送 [session.updated](/api-reference/speech-recognition/qwen-asr-realtime/server-events) 事件。如果未调用此方法，服务端使用默认配置。

#### 发送音频数据

```java
conversation.appendAudio(audioBase64);
```

将 Base64 编码的音频追加到服务端音频缓冲区。

- **VAD 模式**（`enableTurnDetection=true`）：服务端检测语音边界，自动决定何时处理缓冲区。
- **手动模式**（`enableTurnDetection=false`）：音频持续累积，直到您调用 `commit()`。每次事件最多可包含 **15 MiB** 的音频数据。

#### 提交音频缓冲区

```java
conversation.commit();
```

提交已缓冲的音频进行识别。服务端发送 [input\_audio\_buffer.committed](/api-reference/speech-recognition/qwen-asr-realtime/server-events) 事件。

<Note>
  仅在手动模式（`enableTurnDetection=false`）下可用。如果音频缓冲区为空则返回错误。
</Note>

#### 结束会话

```java
conversation.endSession();  // 同步
// 或
conversation.endSessionAsync();  // 异步
```

通知服务端完成剩余音频的处理并结束会话。服务端发送 [session.finished](/api-reference/speech-recognition/qwen-asr-realtime/server-events) 事件。

调用时机：

- **VAD 模式**：音频发送完毕后调用。
- **手动模式**：调用 `commit()` 之后调用。

#### 关闭连接

```java
conversation.close();
```

立即停止任务并关闭 WebSocket 连接。

#### 获取会话 ID 和响应 ID

```java
String sessionId = conversation.getSessionId();
String responseId = conversation.getResponseId();
```

- `getSessionId()` 返回当前任务的会话 ID。
- `getResponseId()` 返回最近一次服务端响应的响应 ID。

### OmniRealtimeCallback

导入路径：`com.alibaba.dashscope.audio.omni.OmniRealtimeCallback`

实现此接口以处理服务端事件。

| 方法                                 | 参数                                                                                                                                                                                                                                               | 触发条件                             |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------- |
| `onOpen()`                         | 无                                                                                                                                                                                                                                                | WebSocket 连接建立时触发。               |
| `onEvent(JsonObject message)`      | `message`：JSON 格式的[服务端事件](/api-reference/speech-recognition/qwen-asr-realtime/server-events)。常见类型：`session.created`、`session.updated`、`input_audio_buffer.committed`、`conversation.item.input_audio_transcription.completed`、`session.finished`。 | 收到服务端事件时触发。通过解析 `type` 字段判断事件类型。 |
| `onClose(int code, String reason)` | `code`：状态码。`reason`：关闭原因。                                                                                                                                                                                                                        | WebSocket 连接关闭时触发。               |
