> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Qwen-Omni Java SDK

> Qwen-Omni-Realtime Java SDK 接口说明

[Qwen-Omni-Realtime](/developer-guides/speech/realtime-multimodal-speech) DashScope Java SDK 的核心接口与请求参数。

## 快速开始

需要 DashScope Java SDK 2.20.9 及以上版本。教程、示例代码和交互模式详解请参见[实时多模态语音](/developer-guides/speech/realtime-multimodal-speech)。

## 请求参数

通过 `OmniRealtimeParam` 对象的链式方法或 setter 配置以下请求参数，然后将该对象与回调实例一起传入 `OmniRealtimeConversation` 构造函数。

| 参数    | 类型     | 说明                                                              |
| ----- | ------ | --------------------------------------------------------------- |
| model | String | Qwen-Omni 实时模型名称。参见[模型列表](/developer-guides/speech/s2s-models)。 |
| url   | String | 端点 URL，默认值为 `wss://dashscope.aliyuncs.com/api-ws/v1/realtime`。  |

通过 `OmniRealtimeConfig` 对象的链式方法或 setter 配置以下请求参数，然后将该对象作为参数传入 `updateSession` 接口。

| 参数                             | 类型                          | 说明                                                                                                                                                                                                                        |
| ------------------------------ | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| modalities                     | List\<OmniRealtimeModality> | 模型的输出模态。设置为 `[OmniRealtimeModality.TEXT]` 仅输出文本，或设置为 `[OmniRealtimeModality.TEXT, OmniRealtimeModality.AUDIO]` 同时输出音频和文本。                                                                                                 |
| voice                          | String                      | 模型音频输出所使用的声音。支持的声音列表请参见[声音列表](/developer-guides/speech/realtime-multimodal-speech#音色列表)。默认声音：`Qwen3.5-Omni-Realtime`：`"Tina"`，`Qwen3-Omni-Flash-Realtime`：`"Cherry"`，`Qwen-Omni-Turbo-Realtime`：`"Chelsie"`。              |
| inputAudioFormat               | OmniRealtimeAudioFormat     | 用户输入音频的格式，当前仅支持设为 `PCM_16000HZ_MONO_16BIT`，表示 16 kHz 采样率的 PCM 音频流。                                                                                                                                                        |
| outputAudioFormat              | OmniRealtimeAudioFormat     | 模型输出音频的格式，当前仅支持设为 `PCM_24000HZ_MONO_16BIT`，表示 24 kHz 采样率的 PCM 音频流。当前不支持自定义输出采样率。                                                                                                                                          |
| smooth\_output                 | Boolean                     | 仅 `Qwen3-Omni-Flash-Realtime` 系列支持。`true`：口语化回复。`false`：书面化回复（内容不易朗读时效果可能不佳）。`null`：模型自动选择口语化或书面化回复风格。                                                                                                                    |
| instructions                   | String                      | 系统消息，用于设定模型的目标或角色。示例："你是一家五星级酒店的 AI 客服，负责解答客户关于房型、设施、价格和预订政策的问题。"                                                                                                                                                         |
| enableInputAudioTranscription  | Boolean                     | 是否对输入音频启用语音识别。                                                                                                                                                                                                            |
| inputAudioTranscription        | String                      | 用于转录输入音频的语音识别模型。当前仅支持 `gummy-realtime-v1`。                                                                                                                                                                                |
| enableTurnDetection            | Boolean                     | 是否启用语音活动检测（VAD）。禁用后，需手动提交音频以触发模型响应。                                                                                                                                                                                       |
| turnDetectionType              | String                      | 服务端 VAD 类型。固定值：`"server_vad"`。                                                                                                                                                                                            |
| turnDetectionThreshold         | Float                       | VAD 阈值。嘈杂环境下可增大该值，安静环境下可减小。值越接近 -1，噪音被识别为语音的概率越高；值越接近 1，概率越低。默认值：0.5。取值范围：\[-1.0, 1.0]。                                                                                                                                   |
| turnDetectionSilenceDurationMs | Integer                     | 表示语音结束的静默时长（毫秒）。静默持续超过该时长后，模型触发响应。默认值：800。取值范围：\[200, 6000]。                                                                                                                                                              |
| turnDetectionParam             | Map                         | VAD 扩展参数，用于传入 `turn_detection` 的额外配置项。当前支持传入 `idle_timeout_ms`（Integer）：静默超时时间（毫秒）。仅在使用 `qwen3.5-omni-plus-realtime` 或 `qwen3.5-omni-flash-realtime` 模型且 VAD 类型为 `server_vad` 时生效。服务端完成音频响应后，在该时长内未收到新的用户音频输入，将自动触发一次空响应。 |
| temperature                    | float                       | 采样温度，控制生成内容的多样性。值越高，内容越多样；值越低，内容越确定。取值范围：\[0, 2)。由于 `temperature` 和 `top_p` 都控制内容多样性，建议只设置其中一个。默认值：`qwen3.5-omni-realtime` 系列：0.7，`qwen3-omni-flash-realtime` 系列：0.9，`qwen-omni-turbo-realtime` 系列：1.0。                   |
| top\_p                         | float                       | 核采样的概率阈值，控制生成内容的多样性。值越高，内容越多样；值越低，内容越确定。取值范围：(0, 1.0]。由于 `temperature` 和 `top_p` 都控制内容多样性，建议只设置其中一个。默认值：`qwen3.5-omni-realtime` 系列：0.8，`qwen3-omni-flash-realtime` 系列：1.0，`qwen-omni-turbo-realtime` 系列：0.01。             |
| top\_k                         | integer                     | 生成时采样的候选 token 集合大小。值越大随机性越强，值越小确定性越强。如果值为 `null` 或大于 100，则禁用 `top_k` 采样，仅 `top_p` 采样生效。值必须大于等于 0。默认值：`qwen3.5-omni-realtime` 系列：20，`qwen3-omni-flash-realtime` 系列：50，`qwen-omni-turbo-realtime` 系列：20。                   |
| max\_tokens                    | integer                     | 响应中可返回的最大 token 数。该参数不影响模型的生成过程。如果模型生成的 token 数超过 `max_tokens`，返回内容将被截断。默认值和最大值为模型的最大输出长度。在需要限制输出长度、控制成本或降低响应延迟的场景中使用 `max_tokens`。                                                                                       |
| repetition\_penalty            | float                       | 控制模型生成时连续序列的重复惩罚。值越高，重复越少。值为 1.0 表示不施加惩罚。值必须大于 0。默认值：`qwen3.5-omni-realtime` 系列：1.0，`qwen3-omni-flash-realtime` 系列：1.05。                                                                                                  |
| presence\_penalty              | float                       | 控制生成内容中重复 token 的可能性。取值范围：\[-2.0, 2.0]。正值减少重复，负值增加重复。较高的值适合创意写作或头脑风暴，较低的值适合技术文档或正式写作。默认值：`qwen3.5-omni-realtime` 系列：1.5，`qwen3-omni-flash-realtime` 系列：0.0。                                                               |
| seed                           | integer                     | 设置 seed 参数可使模型输出更具确定性。如果每次调用使用相同的 seed 值且其他参数不变，模型将尽可能返回相同的结果。取值范围：0 至 2^31-1。默认值：-1。                                                                                                                                     |

<Note>
  `qwen-omni-turbo-realtime` 模型不支持修改 `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty` 和 `seed`。对于其他模型，通过 `OmniRealtimeConfig` 实例的 `parameters` 方法设置这些参数（以及 `smooth_output` 和 `instructions`）：

  ```java
  conversation.updateSession(OmniRealtimeConfig.builder()
    .modalities(Arrays.asList(OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT))
    .voice("Cherry")
    .enableTurnDetection(true)
    .enableInputAudioTranscription(true)
    .parameters(Map.of(
      "smooth_output", true))
    .build()
  );
  ```
</Note>

## 核心接口

### OmniRealtimeConversation 类

通过 `import com.alibaba.dashscope.audio.omni.OmniRealtimeConversation;` 导入 `OmniRealtimeConversation` 类。

#### 构造函数

```java
public OmniRealtimeConversation(OmniRealtimeParam param, OmniRealtimeCallback callback)
```

创建 `OmniRealtimeConversation` 实例。

**参数**：

| 参数       | 类型                   | 说明                                                 |
| -------- | -------------------- | -------------------------------------------------- |
| param    | OmniRealtimeParam    | 会话的配置参数，包括模型、URL 和 API Key。                        |
| callback | OmniRealtimeCallback | 处理服务端事件的回调实例。参见[回调接口](#回调接口-omnirealtimecallback)。 |

#### connect

```java
public void connect() throws NoApiKeyException, InterruptedException
```

创建与服务端的连接。

**服务端响应事件**：[session.created](/api-reference/real-time-multimodal/server-events#session-created)（会话已创建）、[session.updated](/api-reference/real-time-multimodal/server-events#session-updated)（会话配置已更新）。

#### updateSession

```java
public void updateSession(OmniRealtimeConfig config)
```

更新当前会话的默认配置。参数设置请参见[请求参数](#请求参数)部分。

建立连接后，服务端会返回会话的默认输入和输出配置。如需更新默认会话配置，建议在连接建立后立即调用此方法。

服务端收到 `session.update` 事件后会验证参数。如果参数无效，返回错误；否则更新服务端的会话配置。

**服务端响应事件**：[session.updated](/api-reference/real-time-multimodal/server-events#session-updated)（会话配置已更新）。

#### appendAudio

```java
public void appendAudio(String audioBase64)
```

将 Base64 编码的音频数据追加到云端输入音频缓冲区（提交前的临时数据存储区）。

- 如果启用了 `turn_detection`，服务端使用缓冲区检测语音并决定何时提交。
- 如果禁用了 `turn_detection`，由客户端控制每个事件的音频量（最大 15 MiB）。较小的数据块可提高 VAD 的响应速度。

**服务端响应事件**：无。

#### appendVideo

```java
public void appendVideo(String videoBase64)
```

将 Base64 编码的图像数据添加到云端视频缓冲区（本地图像或实时视频流截图）。

图像输入限制：

- 格式：JPG 或 JPEG。推荐分辨率：480p 或 720p（最大 1080p）。
- 大小：单张图片经 Base64 编码后不得超过 256 KB，建议编码前原始图片不超过 190 KB。
- 编码：必须经过 Base64 编码。
- 频率：每秒 1 张图像。

**服务端响应事件**：无。

#### clearAppendedAudio

```java
public void clearAppendedAudio()
```

清除当前云端缓冲区中的音频。

**服务端响应事件**：[input\_audio\_buffer.cleared](/api-reference/real-time-multimodal/server-events#input-audio-buffer-cleared)（服务端接收的音频已清除）。

#### commit

```java
public void commit()
```

提交之前通过 append 添加到云端缓冲区的音频和视频。如果输入音频缓冲区为空，返回错误。

- 如果启用了 `turn_detection`，服务端会自动提交音频缓冲区（客户端无需发送此事件）。
- 如果禁用了 `turn_detection`，客户端必须提交音频缓冲区以创建用户消息项。

<Warning>
  1. 如果配置了 `input_audio_transcription`，系统会对音频进行转录。
  2. 提交缓冲区不会触发模型响应。
</Warning>

**服务端响应事件**：[input\_audio\_buffer.committed](/api-reference/real-time-multimodal/server-events#input-audio-buffer-committed)（服务端已接收提交的音频）。

#### createResponse

```java
public void createResponse(String instructions, List<OmniRealtimeModality> modalities)
```

指示服务端创建模型响应。当会话配置为启用 `turn_detection` 模式时，服务端会自动创建模型响应。

**服务端响应事件**：[response.created](/api-reference/real-time-multimodal/server-events#response-created)、[response.output\_item.added](/api-reference/real-time-multimodal/server-events#response-output-item-added)、[conversation.item.created](/api-reference/real-time-multimodal/server-events#conversation-item-created)、[response.content\_part.added](/api-reference/real-time-multimodal/server-events#response-content-part-added)、[response.audio\_transcript.delta](/api-reference/real-time-multimodal/server-events#response-audio-transcript-delta)、[response.audio.delta](/api-reference/real-time-multimodal/server-events#response-audio-delta)、[response.audio\_transcript.done](/api-reference/real-time-multimodal/server-events#response-audio-transcript-done)、[response.audio.done](/api-reference/real-time-multimodal/server-events#response-audio-done)、[response.content\_part.done](/api-reference/real-time-multimodal/server-events#response-content-part-done)、[response.output\_item.done](/api-reference/real-time-multimodal/server-events#response-output-item-done)、[response.done](/api-reference/real-time-multimodal/server-events#response-done)。

#### cancelResponse

```java
public void cancelResponse()
```

取消正在进行的响应。如果没有可取消的响应，返回错误。

**服务端响应事件**：无。

#### close

```java
public void close(int code, String reason)
```

停止任务并关闭 WebSocket 连接。

**参数**：

| 参数     | 类型     | 说明               |
| ------ | ------ | ---------------- |
| code   | int    | WebSocket 关闭状态码。 |
| reason | String | WebSocket 关闭原因。  |

**服务端响应事件**：无。

#### getSessionId

```java
public String getSessionId()
```

获取当前任务的会话 ID。

**服务端响应事件**：无。

#### getResponseId

```java
public String getResponseId()
```

获取最近一次响应的响应 ID。

**服务端响应事件**：无。

#### getFirstTextDelay

```java
public long getFirstTextDelay()
```

获取最近一次响应的首包文本延迟。

**服务端响应事件**：无。

#### getFirstAudioDelay

```java
public long getFirstAudioDelay()
```

获取最近一次响应的首包音频延迟。

**服务端响应事件**：无。

### 回调接口 (OmniRealtimeCallback)

服务端通过回调向客户端返回事件和数据。实现以下回调方法以处理服务端事件和数据。

通过 `import com.alibaba.dashscope.audio.omni.OmniRealtimeCallback;` 导入该接口。

| 方法                                 | 参数                                              | 返回值 | 说明                                                                                  |
| ---------------------------------- | ----------------------------------------------- | --- | ----------------------------------------------------------------------------------- |
| `onOpen()`                         | 无                                               | 无   | 与服务端建立连接后立即调用。                                                                      |
| `onEvent(JsonObject message)`      | `message`：服务端响应事件。                              | 无   | 包含方法调用的响应以及模型生成的文本和音频。参见[服务端事件](/api-reference/real-time-multimodal/server-events)。 |
| `onClose(int code, String reason)` | `code`：WebSocket 关闭状态码。`reason`：WebSocket 关闭原因。 | 无   | 与服务端的连接关闭后调用。                                                                       |
