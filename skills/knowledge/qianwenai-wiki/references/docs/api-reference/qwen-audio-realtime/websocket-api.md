> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Qwen-Audio-Realtime WebSocket API

> Qwen-Audio-Realtime WebSocket 连接协议、请求头、核心概念和交互流程

Qwen-Audio Realtime API 通过 WebSocket 协议提供实时语音对话能力。客户端通过发送和接收 JSON 事件与服务端交互，支持语音输入、文本输入、语音活动检测（VAD）、流式语音和文本输出等功能。

**用户指南**：[实时语音对话（Qwen-Audio-Realtime）](/developer-guides/speech/qwen-audio-realtime)。客户端事件和服务端事件的详细说明，请参见[客户端事件](/api-reference/qwen-audio-realtime/client-events)和[服务端事件](/api-reference/qwen-audio-realtime/server-events)。

## 服务端点

WebSocket URL 固定如下，通过查询参数 `model` 指定要调用的模型名称（将 `<model_name>` 替换为实际的模型）：

```
wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=<model_name>
```

<Warning>
  URL 必须使用 `wss://` 协议。Authorization 在请求头中设置，模型通过 URL 查询参数 `model` 指定。
</Warning>

## 请求头

请求头中需添加如下信息：

| 参数                    | 类型     | 是否必选 | 说明                                                                          |
| --------------------- | ------ | ---- | --------------------------------------------------------------------------- |
| Authorization         | string | 是    | 鉴权令牌，格式为 `Bearer $DASHSCOPE_API_KEY`，将 `$DASHSCOPE_API_KEY` 替换为实际的 API Key。 |
| user-agent            | string | 否    | 客户端标识，便于服务端追踪来源。                                                            |
| X-DashScope-WorkSpace | string | 否    | 千问AI平台业务空间 ID。                                                              |

<Warning>
  Authorization 鉴权在 WebSocket 握手阶段验证。如果 API Key 无效或缺失，握手将失败并返回 HTTP 401/403 错误。
</Warning>

## 核心概念

- **Session（会话）**：一次 WebSocket 连接对应一个会话，会话内维护配置和对话上下文。
- **Conversation Item（对话项）**：对话中的每条消息，按链表顺序组织。
- **Response（响应）**：一次模型推理产生的输出，包含一个或多个输出项，输出项可以是助手消息，也可以是函数调用。
- **Function Call（函数调用）**：模型请求客户端执行工具函数时产生的输出项。客户端执行完成后通过 `function_call_output` 写回结果，再用 `response.create` 触发下一轮推理。
- **Turn Detection（轮次检测）**：控制何时触发推理。

## 交互模式

Qwen-Audio Realtime API 支持三种交互模式，通过 `session.update` 事件的 `turn_detection.type` 参数配置：

| 模式               | turn\_detection.type | 描述                                                          | 适用场景          |
| ---------------- | -------------------- | ----------------------------------------------------------- | ------------- |
| **server\_vad**  | `server_vad`         | 服务端 VAD 检测语音起止，自动触发推理。                                      | 免提对话、语音助手     |
| **smart\_turn**  | `smart_turn`         | 融合声学感知与语义理解判断轮次边界，而非仅依赖人声信号。无语义的声音（如"嗯"、"啊"）不会触发对话轮或打断模型播报。 | 低延迟自然对话、高质量打断 |
| **push-to-talk** | `null`               | 客户端手动提交音频、手动触发推理。                                           | 按键说话、精确控制     |

## 交互流程

客户端事件和服务端事件的详细说明，请参见[客户端事件](/api-reference/qwen-audio-realtime/client-events)和[服务端事件](/api-reference/qwen-audio-realtime/server-events)。

### server\_vad 模式

服务端对传入的音频进行语音活动检测，检测到语音结束后自动触发推理。

\*\*启用方式：\*\*配置 `session.update` 事件的 `turn_detection.type` 为 `server_vad`。

#### 一轮完整对话

按时间顺序，客户端与服务端的交互流程如下：

1. 客户端建立 WebSocket 连接，服务端返回 `session.created` 事件。
2. 客户端发送 `session.update` 配置会话参数，服务端返回 `session.updated`。
3. 客户端持续发送 `input_audio_buffer.append` 追加音频数据。
4. 服务端检测到语音开始，返回 `input_audio_buffer.speech_started`，同时流式返回 ASR 转写增量 `conversation.item.input_audio_transcription.delta`。
5. 服务端检测到语音结束，返回 `input_audio_buffer.speech_stopped`、`input_audio_buffer.committed` 和 `conversation.item.created`。
6. 服务端自动生成响应，流式返回文本和音频增量（`response.audio_transcript.delta`、`response.audio.delta`），最终返回 `response.done`。

完整事件序列：

| 阶段       | 方向               | 事件                                                      |
| -------- | ---------------- | ------------------------------------------------------- |
| 会话初始化    | Client -> Server | `connect`                                               |
|          | Server -> Client | `session.created`                                       |
|          | Client -> Server | `session.update`                                        |
|          | Server -> Client | `session.updated`                                       |
| 语音输入（循环） | Client -> Server | `input_audio_buffer.append`（持续发送）                       |
|          | Server -> Client | `input_audio_buffer.speech_started`                     |
|          | Client -> Server | `input_audio_buffer.append`（持续发送）                       |
|          | Server -> Client | `conversation.item.input_audio_transcription.delta`（流式） |
|          | Server -> Client | `input_audio_buffer.speech_stopped`                     |
|          | Server -> Client | `conversation.item.input_audio_transcription.completed` |
|          | Server（内部）       | commit audio buffer                                     |
|          | Server -> Client | `input_audio_buffer.committed`                          |
|          | Server -> Client | `conversation.item.created`                             |
| 响应生成     | Server -> Client | `response.created`                                      |
|          | Server -> Client | `response.output_item.added`                            |
|          | Server -> Client | `conversation.item.created`                             |
|          | Server -> Client | `response.content_part.added`                           |
| 流式输出（循环） | Server -> Client | `response.audio_transcript.delta`（流式）                   |
|          | Server -> Client | `response.audio.delta`（流式）                              |
| 输出完成     | Server -> Client | `response.audio_transcript.done`                        |
|          | Server -> Client | `response.audio.done`                                   |
|          | Server -> Client | `response.content_part.done`                            |
|          | Server -> Client | `response.output_item.done`                             |
|          | Server -> Client | `response.done`                                         |

#### 用户打断

模型播报期间，若 VAD 检测到用户开始说话，服务端会取消当前响应（返回 `response.done`，状态为 `cancelled`），随后开始新一轮语音输入和响应。

打断事件序列：

1. 服务端正在流式输出 `response.audio.delta`（循环）。
2. 客户端发送 `input_audio_buffer.append`（用户开始说话）。
3. 服务端返回 `response.done`（status=cancelled），取消当前响应。
4. 服务端返回 `input_audio_buffer.speech_started`。
5. 客户端持续发送 `input_audio_buffer.append`，服务端流式返回 `conversation.item.input_audio_transcription.delta`。
6. 服务端检测到语音结束，返回 `input_audio_buffer.speech_stopped`、`conversation.item.input_audio_transcription.completed`。
7. 服务端内部 commit audio buffer，返回 `input_audio_buffer.committed`、`conversation.item.created`。
8. 服务端自动开始新一轮推理，返回 `response.created`。

### smart\_turn 模式

融合声学感知与语义理解检测语音结束，可过滤回应语、背景音等无意义声音。无语义的声音通过 `conversation.item.ambient_audio_transcription.delta` 事件透传，不触发对话轮。

\*\*启用方式：\*\*配置 `session.update` 事件的 `turn_detection.type` 为 `smart_turn`。

#### 一轮完整对话

与 server\_vad 模式的主要区别：

- 无语义声音（"嗯"、"啊"等）不会触发推理，而是通过 `ambient_audio_transcription` 事件返回。
- 已判定有效的语音可能被撤回（`input_audio_buffer.speech_stopped` 返回 `reason=turn_invalid`），此时不触发推理。
- 在等待用户下一轮输入时，客户端可显式发送 `response.create` 触发推理。

完整事件序列：

| 阶段          | 方向               | 事件                                                        |
| ----------- | ---------------- | --------------------------------------------------------- |
| 会话初始化       | Client -> Server | `connect`                                                 |
|             | Server -> Client | `session.created`                                         |
|             | Client -> Server | `session.update`                                          |
|             | Server -> Client | `session.updated`                                         |
| 语音输入（循环）    | Client -> Server | `input_audio_buffer.append`（持续发送）                         |
| 无效语音（0\~N次） | Server -> Client | `conversation.item.ambient_audio_transcription.delta`（流式） |
|             | Server -> Client | `conversation.item.ambient_audio_transcription.completed` |
| 有效语音输入      | Client -> Server | `input_audio_buffer.append`（持续发送）                         |
|             | Server -> Client | `input_audio_buffer.speech_started`                       |
|             | Client -> Server | `input_audio_buffer.append`（持续发送）                         |
|             | Server -> Client | `conversation.item.input_audio_transcription.delta`（流式）   |
|             | Server -> Client | `input_audio_buffer.speech_stopped`                       |
|             | Server -> Client | `conversation.item.input_audio_transcription.completed`   |
|             | Server（内部）       | commit audio buffer                                       |
|             | Server -> Client | `input_audio_buffer.committed`                            |
|             | Server -> Client | `conversation.item.created`                               |
| 响应生成        | Server -> Client | `response.created`                                        |
|             | Server -> Client | `response.output_item.added`                              |
|             | Server -> Client | `conversation.item.created`                               |
|             | Server -> Client | `response.content_part.added`                             |
| 流式输出（循环）    | Server -> Client | `response.audio_transcript.delta`（流式）                     |
|             | Server -> Client | `response.audio.delta`（流式）                                |
| 输出完成        | Server -> Client | `response.audio_transcript.done`                          |
|             | Server -> Client | `response.audio.done`                                     |
|             | Server -> Client | `response.content_part.done`                              |
|             | Server -> Client | `response.output_item.done`                               |
|             | Server -> Client | `response.done`                                           |

#### 用户打断

与 server\_vad 模式的打断处理基本一致：

1. 服务端正在流式输出 `response.audio.delta`（循环）。
2. 客户端发送 `input_audio_buffer.append`（用户开始说话）。
3. 服务端返回 `response.done`（status=cancelled），取消当前响应。
4. 服务端返回 `input_audio_buffer.speech_started`。
5. 客户端持续发送 `input_audio_buffer.append`，服务端流式返回 `conversation.item.input_audio_transcription.delta`。
6. 服务端返回 `conversation.item.input_audio_transcription.completed`、`input_audio_buffer.speech_stopped`。
7. 服务端内部 commit audio buffer，返回 `input_audio_buffer.committed`、`conversation.item.created`。
8. 服务端自动开始新一轮推理，返回 `response.created`。

#### 无效轮次

已判定有效的语音可能被撤回（`input_audio_buffer.speech_stopped` 返回 `reason=turn_invalid`），此时不触发推理，客户端应继续发送音频等待下一轮有效语音。

无效轮次事件序列：

1. 客户端持续发送 `input_audio_buffer.append`。
2. 服务端返回 `input_audio_buffer.speech_started`。
3. 客户端继续发送 `input_audio_buffer.append`，服务端流式返回 `conversation.item.input_audio_transcription.delta`。
4. 服务端返回 `input_audio_buffer.speech_stopped`（reason=turn\_invalid）。
5. 客户端继续发送音频，等待下一轮有效语音。

#### 说话人增强配置流程

在 smart\_turn 模式下，首次 `session.update` 中传入 `voiceprint_audio_urls` 时，服务端将异步执行声纹注册（加载目标说话人音频特征），并通过事件通知注册进度。声纹注册失败不阻塞正常对话流程。

按时间顺序，声纹注册的交互流程如下：

1. 客户端发送 `session.update`，在 `turn_detection.voiceprint_audio_urls` 中传入声纹音频 URL，服务端返回 `session.updated`。
2. 服务端立即异步启动声纹注册，在 `session.updated` 返回**之前**先推送 `voiceprint_audio_list.in_progress` 事件，携带本次注册任务的唯一标识 `item_id`。
3. 服务端返回 `session.updated`，确认会话配置已生效。
4. 声纹注册完成后，服务端推送终态事件（`item_id` 与步骤 2 一致）：
   - 注册成功：`voiceprint_audio_list.completed`。
   - 注册失败：`voiceprint_audio_list.failed`，附带 `reason` 字段说明失败原因（如音频 URL 无法下载）。

<Note>
  `voiceprint_audio_urls` 仅在**第一次** `session.update` 时生效，后续传入该字段将被忽略。
</Note>

### push-to-talk 模式

客户端手动控制音频提交和推理触发，适用于按键说话场景。

\*\*启用方式：\*\*配置 `session.update` 事件的 `turn_detection` 为 `null`。

#### 一轮完整对话

按时间顺序，客户端与服务端的交互流程如下：

1. 客户端持续发送 `input_audio_buffer.append` 追加音频数据。
2. 用户说完话后，客户端发送 `input_audio_buffer.commit` 提交缓冲区。
3. 客户端发送 `response.create` 手动触发推理。
4. 服务端生成响应，流式返回文本和音频。

完整事件序列：

| 阶段       | 方向               | 事件                                                      |
| -------- | ---------------- | ------------------------------------------------------- |
| 会话初始化    | Client -> Server | `connect`                                               |
|          | Server -> Client | `session.created`                                       |
|          | Client -> Server | `session.update`                                        |
|          | Server -> Client | `session.updated`                                       |
| 语音输入（循环） | Client -> Server | `input_audio_buffer.append`（持续发送）                       |
|          | Server -> Client | `conversation.item.input_audio_transcription.delta`（流式） |
| 手动提交     | Client -> Server | `input_audio_buffer.commit`（用户松开按键）                     |
|          | Server -> Client | `conversation.item.input_audio_transcription.completed` |
|          | Server -> Client | `input_audio_buffer.committed`                          |
|          | Server -> Client | `conversation.item.created`                             |
| 手动触发推理   | Client -> Server | `response.create`（手动触发推理）                               |
| 响应生成     | Server -> Client | `response.created`                                      |
|          | Server -> Client | `response.output_item.added`                            |
|          | Server -> Client | `conversation.item.created`                             |
|          | Server -> Client | `response.content_part.added`                           |
| 流式输出（循环） | Server -> Client | `response.audio_transcript.delta`（流式）                   |
|          | Server -> Client | `response.audio.delta`（流式）                              |
| 输出完成     | Server -> Client | `response.audio_transcript.done`                        |
|          | Server -> Client | `response.audio.done`                                   |
|          | Server -> Client | `response.content_part.done`                            |
|          | Server -> Client | `response.output_item.done`                             |
|          | Server -> Client | `response.done`                                         |

#### 用户打断

客户端发送 `response.cancel` 取消当前响应，服务端返回 `response.done`（状态为 `cancelled`，原因为 `client_cancelled`）。

打断事件序列：

1. 服务端正在流式输出 `response.audio_transcript.delta` 和 `response.audio.delta`（循环）。
2. 客户端发送 `response.cancel`。
3. 服务端返回 `response.done`（status=cancelled, reason=client\_cancelled）。
4. 客户端持续发送 `input_audio_buffer.append`，服务端流式返回 `conversation.item.input_audio_transcription.delta`。
5. 客户端发送 `input_audio_buffer.commit` 提交缓冲区。
6. 服务端返回 `conversation.item.input_audio_transcription.completed`、`input_audio_buffer.committed`、`conversation.item.created`。
7. 客户端发送 `response.create` 手动触发新一轮推理。
8. 服务端返回 `response.created`，开始新一轮响应。

## 各模式操作约束

| 操作                                       | push-to-talk                                                   | server\_vad                  | smart\_turn                                                                                     |
| ---------------------------------------- | -------------------------------------------------------------- | ---------------------------- | ----------------------------------------------------------------------------------------------- |
| session.update                           | IDLE 时全部可改；非 IDLE 时部分受限                                        | IDLE 时全部可改；非 IDLE 时部分受限      | IDLE 时全部可改；非 IDLE 时部分受限                                                                         |
| input\_audio\_buffer.append              | 允许                                                             | 允许                           | 允许                                                                                              |
| input\_audio\_buffer.commit              | 允许                                                             | 忽略                           | 忽略                                                                                              |
| input\_audio\_buffer.clear               | 允许                                                             | 忽略                           | 忽略                                                                                              |
| response.create                          | 允许（需先通过 `input_audio_buffer.commit` 提交缓冲区音频；当前有响应正在生成时不允许重复触发） | 当前无响应正在生成时允许；有响应正在生成时不允许重复触发 | 等待用户下一轮输入时允许；当前处于一个 turn 内时（收到 `input_audio_buffer.speech_started` 到 `response.done` 期间）不允许重复触发 |
| response.cancel                          | 允许（推理中）                                                        | 允许（推理中）                      | 允许（推理中）                                                                                         |
| conversation.item.create/delete/retrieve | 允许                                                             | 允许                           | 允许                                                                                              |

<Note>
  `turn_detection` 和 `input_audio_format` 仅在首次发送音频之前（IDLE 状态）允许修改。
</Note>

## 错误处理

| 类型                             | 行为       | 示例                      |
| ------------------------------ | -------- | ----------------------- |
| 客户端错误（`invalid_request_error`） | 连接保持，仅通知 | 参数不合法、状态不允许、item\_id 重复 |
| 服务端错误（`server_error`）          | 连接终止     | LLM 连接失败、存储故障           |
