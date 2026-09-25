> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Qwen-TTS client events

> WebSocket 客户端事件参考

客户端事件是通过 WebSocket 发送的 JSON 消息，用于配置语音参数、流式传输文本以及标记输入完成。

<Note>连接端点、请求头和交互流程请参阅 [WebSocket API](/api-reference/speech-synthesis/qwen-tts-realtime/websocket-api)。完整用户指南请参阅[实时流式语音合成](/developer-guides/speech/realtime-streaming)。</Note>

## 事件概览

| 客户端事件                      | 服务端响应                         | 说明                                        |
| -------------------------- | ----------------------------- | ----------------------------------------- |
| （连接建立时，服务端主动发送）            | `session.created`             | 服务端推送默认会话配置，客户端可据此决定是否发送 `session.update` |
| `session.update`           | `session.updated`             | 设置语音、音频格式、模式等会话参数                         |
| `input_text_buffer.append` | `response.created`            | 向合成缓冲区追加文本                                |
| `input_text_buffer.commit` | `input_text_buffer.committed` | 提交缓冲文本，开始合成                               |
| `input_text_buffer.clear`  | `input_text_buffer.cleared`   | 清空缓冲区中的所有文本                               |
| `session.finish`           | `session.finished`            | 结束会话；服务端刷新剩余音频，客户端收到后应主动关闭连接              |

## session.update

WebSocket 连接建立后，服务端会主动发送 `session.created` 事件，包含默认会话配置。客户端可在收到后发送 `session.update` 覆盖默认配置；省略则保持默认值。服务端返回 `session.updated` 确认。

```json Example
{
  "event_id": "event_123",
  "type": "session.update",
  "session": {
    "voice": "Cherry",
    "mode": "server_commit",
    "language_type": "Chinese",
    "response_format": "pcm",
    "sample_rate": 24000,
    "instructions": "",
    "optimize_instructions": false
  }
}
```

<ParamField body="event_id" type="string" required>
  事件唯一标识符，在会话中必须唯一。
</ParamField>

<ParamField body="type" type="string" required>
  设置为 `session.update`。
</ParamField>

<ParamField body="session" type="object">
  会话配置。

  <Expandable title="properties">
    <ParamField body="voice" type="string" required>
      合成语音。

      - **系统语音**：适用于 Qwen3-TTS-Instruct-Flash-Realtime、Qwen3-TTS-Flash-Realtime 和 Qwen-TTS-Realtime。
      - **自定义语音**：
        - [声音克隆](/api-reference/speech-synthesis/voice-cloning/create-voice)：仅限 Qwen3-TTS-VC-Realtime。
        - [声音设计](/api-reference/speech-synthesis/voice-design/create-voice)：仅限 Qwen3-TTS-VD-Realtime。
    </ParamField>

    <ParamField body="mode" type="string">
      控制缓冲文本的合成时机。默认值：`server_commit`。

| 值               | 行为                                                      |
| --------------- | ------------------------------------------------------- |
| `server_commit` | 由服务端决定合成时机，自动平衡延迟与质量。推荐使用。                              |
| `commit`        | 由客户端发送 `input_text_buffer.commit` 触发合成。延迟最低，但需自行管理句子边界。 |
    </ParamField>

    <ParamField body="language_type" type="string">
      输出音频的语言。默认值：`Auto`。

      - `Auto` -- 适用于语言未知或多语言混合的文本。模型自动匹配各片段的发音，但无法保证每段都准确。
      - 指定语言可提升质量。支持的值：

| 值          | 值            | 值         |
| ---------- | ------------ | --------- |
| `Chinese`  | `English`    | `German`  |
| `Italian`  | `Portuguese` | `Spanish` |
| `Japanese` | `Korean`     | `French`  |
| `Russian`  |              |           |
    </ParamField>

    <ParamField body="response_format" type="string">
      音频输出格式。默认值：`pcm`。

| 值      | 说明                             |
| ------ | ------------------------------ |
| `pcm`  | 默认格式。Qwen-TTS-Realtime 仅支持此格式。 |
| `wav`  |                                |
| `mp3`  |                                |
| `opus` | 支持通过 `bit_rate` 配置比特率。         |
    </ParamField>

    <ParamField body="sample_rate" type="integer">
      音频采样率，单位 Hz。默认值：`24000`。

      支持的值：`8000`、`16000`、`24000`、`48000`。

      <Note>Qwen-TTS-Realtime 仅支持 `24000`。</Note>
    </ParamField>

    <ParamField body="speech_rate" type="float">
      播放速度。小于 1.0 减速，大于 1.0 加速。默认值：`1.0`。范围：0.5--2.0。

      <Note>Qwen-TTS-Realtime 不支持此参数。</Note>
    </ParamField>

    <ParamField body="volume" type="integer">
      音频音量。默认值：`50`。范围：0--100。

      <Note>Qwen-TTS-Realtime 不支持此参数。</Note>
    </ParamField>

    <ParamField body="pitch_rate" type="float">
      音频音调。默认值：`1.0`。范围：0.5--2.0。

      <Note>Qwen-TTS-Realtime 不支持此参数。</Note>
    </ParamField>

    <ParamField body="bit_rate" type="integer">
      音频[比特率](https://opus-codec.org/)，单位 kbps。值越高质量越好，但文件体积也越大。仅在 `response_format` 为 `opus` 时生效。默认值：`128`。范围：6--510。

      <Note>Qwen-TTS-Realtime 不支持此参数。</Note>
    </ParamField>

    <ParamField body="instructions" type="string">
      控制输出语音的风格和表现力。详情参阅[实时流式语音合成](/developer-guides/speech/realtime-streaming)。最大长度：1600 tokens。

      支持语言：仅中文和英文。

      <Note>仅 Qwen3-TTS-Instruct-Flash-Realtime 支持此参数。</Note>
    </ParamField>

    <ParamField body="optimize_instructions" type="boolean">
      设为 `true` 时，系统会自动优化 `instructions` 以提升语音的自然度和表现力。适用于精细的语音风格控制。默认值：`false`。

      `instructions` 为空时不生效。

      <Note>仅 Qwen3-TTS-Instruct-Flash-Realtime 支持此参数。</Note>
    </ParamField>
  </Expandable>
</ParamField>

## input\_text\_buffer.append

向合成缓冲区追加文本。`server_commit` 模式下缓冲区在服务端，`commit` 模式下在客户端。

新的响应开始时，服务端返回 `response.created`。

```json Example
{
  "event_id": "event_B4o9RHSTWobB5OQdEHLTo",
  "type": "input_text_buffer.append",
  "text": "Hello, I am Qwen."
}
```

<ParamField body="event_id" type="string" required>
  事件唯一标识符，在会话中必须唯一。
</ParamField>

<ParamField body="type" type="string" required>
  设置为 `input_text_buffer.append`。
</ParamField>

<ParamField body="text" type="string" required>
  待合成的文本。
</ParamField>

## input\_text\_buffer.commit

提交缓冲文本并创建用户消息项。服务端返回 `input_text_buffer.committed`。对空缓冲区执行此操作会返回错误。

不同模式下的行为：

- **`server_commit`**：立即合成所有缓冲文本。服务端停止缓存并处理全部内容。
- **`commit`**：将缓冲文本创建为用户消息项。

<Note>提交仅触发语音合成，不会触发模型响应生成。</Note>

```json Example
{
  "event_id": "event_C7p2MKVFXqrA3TBzNJUse",
  "type": "input_text_buffer.commit"
}
```

<ParamField body="event_id" type="string" required>
  事件唯一标识符，在会话中必须唯一。
</ParamField>

<ParamField body="type" type="string" required>
  设置为 `input_text_buffer.commit`。
</ParamField>

## input\_text\_buffer.clear

清空缓冲区中的所有文本。服务端返回 `input_text_buffer.cleared`。

<Note>仅在 `mode: "commit"` 时可用。`server_commit` 模式下发送此事件，服务端会返回错误：`only client commit mode supports clear operation`。</Note>

```json Example
{
  "event_id": "event_2728",
  "type": "input_text_buffer.clear"
}
```

<ParamField body="event_id" type="string" required>
  事件唯一标识符，在会话中必须唯一。
</ParamField>

<ParamField body="type" type="string" required>
  设置为 `input_text_buffer.clear`。
</ParamField>

## session.finish

通知服务端没有更多文本需要发送。服务端刷新剩余音频，返回 `session.finished`；客户端应在收到此事件后主动关闭连接。

```json Example
{
  "event_id": "event_2239",
  "type": "session.finish"
}
```

<ParamField body="event_id" type="string" required>
  事件唯一标识符，在会话中必须唯一。
</ParamField>

<ParamField body="type" type="string" required>
  设置为 `session.finish`。
</ParamField>
