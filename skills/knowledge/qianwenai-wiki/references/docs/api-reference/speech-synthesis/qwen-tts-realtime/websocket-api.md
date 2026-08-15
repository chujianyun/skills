> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Qwen-TTS-Realtime WebSocket API

> Qwen-TTS-Realtime WebSocket 连接协议、请求头和交互流程

Qwen-TTS-Realtime 使用 WebSocket 协议进行实时流式语音合成。WebSocket 支持全双工通信，客户端与服务器通过一次握手建立持久连接，然后实时相互推送数据。

DashScope SDK 支持 Python 和 Java。其他语言请直接使用 WebSocket 接口。

**用户指南**：模型概览和使用方法，参见[实时流式语音合成](/developer-guides/speech/realtime-streaming)。

## 前提条件

获取 [API Key](/api-reference/preparation/api-key)。

## 支持的模型

| 模型 ID                               | 说明            |
| ----------------------------------- | ------------- |
| `qwen3-tts-flash-realtime`          | 基础实时合成模型      |
| `qwen3-tts-instruct-flash-realtime` | 支持指令控制的实时合成模型 |
| `qwen3-tts-vc-realtime`             | 声音克隆实时合成模型    |
| `qwen3-tts-vd-realtime`             | 声音设计实时合成模型    |
| `qwen-tts-realtime`                 | 上一代实时合成模型     |

## 连接端点

```
wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model={model}
```

将 `{model}` 替换为上表中的模型 ID，例如 `qwen3-tts-flash-realtime`。

<Warning>
  URL 必须使用 `wss://` 协议。Authorization 在请求头中设置（参见下方[请求头](#请求头)），模型通过 URL 查询参数 `model` 指定。
</Warning>

## 请求头

| 参数                    | 类型     | 是否必选 | 说明                                    |
| --------------------- | ------ | ---- | ------------------------------------- |
| Authorization         | string | 是    | 鉴权令牌，格式为 `Bearer $DASHSCOPE_API_KEY`。 |
| user-agent            | string | 否    | 客户端标识，便于服务端追踪来源。                      |
| X-DashScope-WorkSpace | string | 否    | 千问AI平台业务空间 ID。                        |

<Warning>
  Authorization 鉴权在 WebSocket 握手阶段验证。如果 API Key 无效或缺失，握手将失败并返回 HTTP 401/403 错误。
</Warning>

## 浏览器中使用 WebSocket

浏览器环境中 WebSocket 无法设置自定义请求头（包括 Authorization）。如需在前端使用，建议通过后端服务代理 WebSocket 连接，由后端在握手时注入鉴权头。

## 交互模式

Qwen-TTS-Realtime 提供两种交互模式，通过 `session.update` 事件的 `session.mode` 参数切换：

- **server\_commit 模式**（推荐）：服务端智能处理文本分段和合成时机，适合大段文本的连续合成场景。客户端只需持续追加文本，无需关注切分。
- **commit 模式**：客户端主动提交文本缓冲区以触发合成，适合需要精确控制合成时机的场景（如对话式 AI 逐轮合成）。

## 交互流程

![Qwen-TTS interaction flow](https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2678667571/p992312.svg)

<Tabs>
  <Tab title="Server commit 模式">
    将 `session.update` 事件的 `session.mode` 属性设置为 `"server_commit"` 以启用此模式。服务端会智能处理文本分割和合成时机。

    **流程**：

    1. 客户端发送 `session.update` 事件。服务端返回 `session.created` 和 `session.updated` 事件。
    2. 客户端发送 `input_text_buffer.append` 事件，将文本追加到服务端缓冲区。
    3. 服务端智能处理文本分割和合成时机，返回 `response.created`、`response.output_item.added`、`response.content_part.added` 和 `response.audio.delta` 事件。
    4. 完成响应后，服务端返回 `response.audio.done`、`response.content_part.done`、`response.output_item.done` 和 `response.done`。
    5. 客户端发送 `session.finish`，服务端返回 `session.finished` 结束会话。

| 生命周期    | 客户端事件                                   | 服务端事件                                        |
| ------- | --------------------------------------- | -------------------------------------------- |
| 会话初始化   | `session.update` 会话配置                   | `session.created` 会话已创建                      |
|         |                                         | `session.updated` 会话配置已更新                    |
| 用户文本输入  | `input_text_buffer.append` 向服务端追加文本     |                                              |
|         | `input_text_buffer.commit` 立即合成服务端缓存的文本 |                                              |
|         | `session.finish` 通知服务端不再有文本输入           | `input_text_buffer.committed` 服务端已接收提交的文本    |
| 服务端音频输出 | 无                                       | `response.created` 服务端开始生成响应                 |
|         |                                         | `response.output_item.added` 响应中有新的输出内容      |
|         |                                         | `response.content_part.added` 助手消息中添加了新的输出内容 |
|         |                                         | `response.audio.delta` 模型生成的增量音频             |
|         |                                         | `response.content_part.done` 内容流已完成          |
|         |                                         | `response.output_item.done` 输出项流已完成          |
|         |                                         | `response.audio.done` 音频生成完成                 |
|         |                                         | `response.done` 响应完成                         |
  </Tab>

  <Tab title="Commit 模式">
    将 `session.update` 事件的 `session.mode` 属性设置为 `"commit"` 以启用此模式。客户端需要主动将文本缓冲区提交给服务端以触发合成。

    **流程**：

    1. 客户端发送 `session.update` 事件。服务端返回 `session.created` 和 `session.updated` 事件。
    2. 客户端发送 `input_text_buffer.append` 事件，将文本追加到缓冲区。
    3. 客户端发送 `input_text_buffer.commit` 事件将缓冲区提交给服务端。
    4. 服务端返回 `response.created`，开始生成响应。
    5. 服务端返回 `response.audio.delta` 等事件。
    6. 完成后客户端发送 `session.finish`，服务端返回 `session.finished` 结束会话。

| 生命周期    | 客户端事件                                 | 服务端事件                                        |
| ------- | ------------------------------------- | -------------------------------------------- |
| 会话初始化   | `session.update` 会话配置                 | `session.created` 会话已创建                      |
|         |                                       | `session.updated` 会话配置已更新                    |
| 用户文本输入  | `input_text_buffer.append` 向缓冲区追加文本   |                                              |
|         | `input_text_buffer.commit` 将缓冲区提交给服务端 |                                              |
|         | `input_text_buffer.clear` 清空缓冲区       | `input_text_buffer.committed` 服务端已接收提交的文本    |
|         |                                       | `input_text_buffer.cleared` 缓冲区已清空           |
| 服务端音频输出 | 无                                     | `response.created` 服务端开始生成响应                 |
|         |                                       | `response.output_item.added` 响应中有新的输出内容      |
|         |                                       | `response.content_part.added` 助手消息中添加了新的输出内容 |
|         |                                       | `response.audio.delta` 模型生成的增量音频             |
|         |                                       | `response.content_part.done` 内容流已完成          |
|         |                                       | `response.output_item.done` 输出项流已完成          |
|         |                                       | `response.audio.done` 音频生成完成                 |
|         |                                       | `response.done` 响应完成                         |
  </Tab>
</Tabs>

## 连接生命周期

每次 WebSocket 连接对应一个独立会话。会话结束后连接关闭，无法复用。如需新一轮合成，请重新建立连接。

典型生命周期：

1. **建立连接**：客户端发起 WebSocket 握手，服务端验证 Authorization。
2. **会话初始化**：服务端发送 `session.created`，客户端可发送 `session.update` 配置参数。
3. **文本输入与合成**：客户端持续追加文本，服务端流式返回音频。
4. **结束会话**：客户端发送 `session.finish`，服务端刷新剩余音频并返回 `session.finished`。
5. **关闭连接**：客户端收到 `session.finished` 后主动关闭 WebSocket。

## 常见错误

| 错误                                                 | 原因                                                | 解决方法                                              |
| -------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------- |
| HTTP 401/403 握手失败                                  | API Key 无效或缺失                                     | 确认 Authorization 头格式为 `Bearer $DASHSCOPE_API_KEY` |
| 连接立即断开                                             | URL 缺少 `model` 参数                                 | 确认 URL 包含 `?model=<model_id>`                     |
| `error` 事件                                         | 参数错误或模型不支持                                        | 检查 `session.update` 中的参数是否与所选模型兼容                 |
| `only client commit mode supports clear operation` | 在 server\_commit 模式下发送了 `input_text_buffer.clear` | 仅在 commit 模式下使用 clear 操作                          |
