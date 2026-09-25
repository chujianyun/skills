> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 实时语音识别（Qwen-ASR-Realtime）WebSocket API

> Qwen-ASR-Realtime WebSocket 连接、请求头和交互流程

Qwen-ASR-Realtime 通过 WebSocket 接收音频流并实时转写语音。服务支持两种交互模式：[VAD 模式](#vad-模式)和[手动模式](#手动模式)。

**用户指南**：模型详情和选型建议请参见[语音识别模型](/developer-guides/speech/speech-to-text-models)。示例代码请参见[实时语音识别](/developer-guides/speech/asr-realtime)。

## 连接端点

使用以下 WebSocket 地址。`model` 查询参数指定模型名称，将 `<model_name>` 替换为模型名：

```
wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=<model_name>
```

<Note>
  使用 `wss://` 协议。在请求头中设置认证信息（见[请求头](#请求头)）。通过 `model` 查询参数指定模型。
</Note>

## 请求头

请求中需包含以下请求头：

| **参数**                     | **类型** | **是否必选** | **说明**                               |
| -------------------------- | ------ | -------- | ------------------------------------ |
| Authorization              | string | 是        | 认证令牌。格式：`Bearer $DASHSCOPE_API_KEY`。 |
| user-agent                 | string | 否        | 客户端标识。用于帮助服务器追踪请求来源。                 |
| X-DashScope-WorkSpace      | string | 否        | 千问AI平台业务空间 ID。                       |
| X-DashScope-DataInspection | string | 否        | 是否开启数据合规检查。默认不设置；需要时设为 `enable`。     |

<Note>
  Authorization 在 WebSocket 握手阶段验证。如果 API Key 无效或缺失，握手失败并返回 HTTP 401 或 403 错误。
</Note>

## 交互流程

客户端事件和服务端事件的详细参数说明请参见[客户端事件](/api-reference/speech-recognition/qwen-asr-realtime/client-events)和[服务端事件](/api-reference/speech-recognition/qwen-asr-realtime/server-events)。

Qwen-ASR-Realtime 支持两种交互模式：

- **VAD 模式（默认）**：服务端使用语音活动检测（VAD）自动检测每个语句的起止。适用于实时对话、会议转写等场景。
- **手动模式**：客户端控制语句边界。适用于客户端能明确确定语句边界的场景，例如发送语音消息。

### VAD 模式

服务端自动检测每个语句的起止。持续发送音频流即可，服务端会在检测到语句结束后返回最终转写结果。

**启用方式**：在客户端 [session.update](/api-reference/speech-recognition/qwen-asr-realtime/client-events#session-update) 事件中配置 `session.turn_detection` 参数。

1. 客户端发送 `input_audio_buffer.append` 事件向缓冲区追加音频。
2. 服务端检测到语音时返回 `conversation.item.input_audio_transcription.text` 事件。
3. 客户端继续发送 `input_audio_buffer.append` 事件。
4. 所有音频发送完毕后，客户端发送 `session.finish` 事件结束会话。

<Warning>
  在 VAD 模式下，推完音频后必须先发送 `session.finish` 事件再关闭连接。如果客户端直接关闭 WebSocket 连接而未发送该事件，服务端将丢弃当前 in\_progress item，`conversation.item.input_audio_transcription.completed` 等事件将不会到达。建议在调用 `ws.Close()` 之前，先发送 `{"type":"session.finish"}`，并等待收到 `session.finished` 事件后再关闭连接。
</Warning>

5. 服务端检测到语音结束时返回 `conversation.item.input_audio_transcription.text` 事件。
6. 服务端返回包含部分转写结果的 `conversation.item.input_audio_transcription.text` 事件。
7. 服务端返回包含最终转写结果的 `conversation.item.input_audio_transcription.completed` 事件。
8. 服务端返回 `session.finished` 事件，表示识别完成。客户端须关闭连接。

<Note>
  如果客户端在步骤 5 之前发送 `session.finish`，服务端将立即返回 `session.finished` 事件。客户端须关闭连接。
</Note>

### 手动模式

客户端控制语句边界。发送完一段完整语音后，客户端发送 `input_audio_buffer.commit` 事件通知服务端。

**启用方式**：在客户端 [session.update](/api-reference/speech-recognition/qwen-asr-realtime/client-events#session-update) 事件中将 `session.turn_detection` 设为 `null`。

1. 客户端发送 `input_audio_buffer.append` 事件向缓冲区追加音频。
2. 客户端发送 `input_audio_buffer.commit` 事件提交输入音频缓冲区。提交后在会话中创建一条新的用户消息。
3. 客户端发送 `session.finish` 事件结束会话。
4. 服务端返回包含部分转写结果的 `conversation.item.input_audio_transcription.text` 事件。
5. 服务端返回包含最终转写结果的 `conversation.item.input_audio_transcription.completed` 事件。
6. 服务端返回 `session.finished` 事件，表示识别完成。客户端须关闭连接。
