> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Qwen-Omni server events

> WebSocket 服务端事件参考

Qwen-Omni-Realtime API 的服务端事件。

<Note>参考：[实时多模态](/developer-guides/speech/realtime-multimodal-speech)。</Note>

## error

服务端错误消息。

```json Example
{
  "event_id": "event_RoUu4T8yExPMI37GKwaOC",
  "type": "error",
  "error": {
  "type": "invalid_request_error",
  "code": "invalid_value",
  "message": "Invalid modalities: ['audio']. Supported combinations are: ['text'] and ['audio', 'text'].",
  "param": "session.modalities"
  }
}
```

<ParamField body="event_id" type="string">
  事件唯一标识。
</ParamField>

<ParamField body="type" type="string">
  固定为 `error`。
</ParamField>

<ParamField body="error" type="object">
  错误详情。

  <Expandable title="properties">
    <ParamField body="type" type="string">
      错误类型。
    </ParamField>

    <ParamField body="code" type="string">
      错误码。
    </ParamField>

    <ParamField body="message" type="string">
      错误信息。
    </ParamField>

    <ParamField body="param" type="string">
      相关参数（如 `session.modalities`）。
    </ParamField>
  </Expandable>
</ParamField>

## session.created

连接后收到的第一个事件，包含默认会话配置。

```json Example
{
  "event_id": "event_RdvlSpbBb2ssyBjYrDHjt",
  "type": "session.created",
  "session": {
  "object": "realtime.session",
  "model": "qwen3.5-omni-flash-realtime",
  "modalities": [
      "text",
      "audio"
  ],
  "audio": {
      "input": {
          "format": {
              "type": "pcm",
              "sample_rate": 16000
          }
      },
      "output": {
          "format": {
              "type": "wav",
              "sample_rate": 24000
          }
      }
  },
  "voice": "Tina",
  "input_audio_format": "pcm",
  "output_audio_format": "pcm",
  "input_audio_transcription": {
      "model": "qwen3-asr-flash-realtime"
  },
  "turn_detection": {
      "type": "server_vad",
      "threshold": 0.5,
      "prefix_padding_ms": 300,
      "silence_duration_ms": 800,
      "create_response": true,
      "interrupt_response": true
  },
  "tools": [],
  "tool_choice": "auto",
  "temperature": 0.8,
  "id": "sess_Ov7GOXoNXhNjlxXtOGKQS"
  }
}
```

<ParamField body="event_id" type="string">
  事件唯一标识。
</ParamField>

<ParamField body="type" type="string">
  固定为 `session.created`。
</ParamField>

<ParamField body="session" type="object">
  会话配置。

  <Expandable title="properties">
    <ParamField body="object" type="string">
      固定为 `realtime.session`。
    </ParamField>

    <ParamField body="model" type="string">
      模型名称。
    </ParamField>

    <ParamField body="modalities" type="array">
      输出模态。
    </ParamField>

    <ParamField body="voice" type="string">
      音频输出的语音。
    </ParamField>

    <ParamField body="input_audio_format" type="string">
      用户输入音频的格式，当前仅支持 `pcm`。输入音频要求为 16 kHz 采样率的 PCM 音频流。
    </ParamField>

    <ParamField body="output_audio_format" type="string">
      模型输出音频的格式，当前仅支持 `pcm`。输出音频为 24 kHz 采样率的 PCM 音频流。当前不支持自定义输出采样率。
    </ParamField>

    <ParamField body="input_audio_transcription" type="object">
      语音转录配置。

      <Expandable title="properties">
        <ParamField body="model" type="string">
          转录模型，固定为 `qwen3-asr-flash-realtime`，不支持修改。
        </ParamField>
      </Expandable>
    </ParamField>

    <ParamField body="turn_detection" type="object">
      语音活动检测（VAD）配置。

      <Expandable title="properties">
        <ParamField body="type" type="string">
          VAD 类型。取值：`server_vad`（默认值）或 `semantic_vad`。详情请参见[客户端事件](/api-reference/real-time-multimodal/client-events)。
        </ParamField>

        <ParamField body="threshold" type="float">
          VAD 检测阈值。
        </ParamField>

        <ParamField body="silence_duration_ms" type="integer">
          判定语音结束前的静默时长（毫秒）。
        </ParamField>

        <ParamField body="idle_timeout_ms" type="integer">
          静默超时时间（毫秒）。仅在`server_vad`模式下，使用`qwen3.5-omni-plus-realtime`或`qwen3.5-omni-flash-realtime`模型时返回。
        </ParamField>

        <ParamField body="prefix_padding_ms" type="integer">
          语音开始前保留的音频时长（毫秒）。
        </ParamField>

        <ParamField body="create_response" type="boolean">
          检测到语音结束后是否自动创建响应。
        </ParamField>

        <ParamField body="interrupt_response" type="boolean">
          检测到新语音时是否中断当前响应。
        </ParamField>
      </Expandable>
    </ParamField>

    <ParamField body="tools" type="array">
      可供模型调用的工具列表。
    </ParamField>

    <ParamField body="tool_choice" type="string">
      工具调用策略。
    </ParamField>

    <ParamField body="id" type="string">
      会话唯一 ID。
    </ParamField>

    <ParamField body="temperature" type="float">
      采样温度。
    </ParamField>
  </Expandable>
</ParamField>

## session.updated

成功处理 `session.update` 请求后发送。如果出错，服务端会发送 `error` 事件。

```json Example
{
  "event_id": "event_X1HsXS4b4uptp6yo1LgKd",
  "type": "session.updated",
  "session": {
  "id": "sess_Aih6vAcY5Ddt6jwFx1tCa",
  "object": "realtime.session",
  "model": "qwen3.5-omni-flash-realtime",
  "modalities": [
      "text",
      "audio"
  ],
  "audio": {
      "input": {
          "format": {
              "type": "pcm",
              "sample_rate": 16000
          }
      },
      "output": {
          "format": {
              "type": "wav",
              "sample_rate": 24000
          }
      }
  },
  "instructions": "你是个人助理小云，请你准确且友好地解答用户的问题，始终以乐于助人的态度回应。",
  "voice": "Tina",
  "input_audio_format": "pcm",
  "output_audio_format": "pcm",
  "input_audio_transcription": {
      "model": "qwen3-asr-flash-realtime"
  },
  "turn_detection": {
      "type": "server_vad",
      "threshold": 0.1,
      "prefix_padding_ms": 500,
      "silence_duration_ms": 900,
      "create_response": true,
      "interrupt_response": true
  },
  "temperature": 0.8,
  "max_response_output_token": "inf",
  "max_tokens": 16384,
  "repetition_penalty": 1.05,
  "presence_penalty": 0.0,
  "top_k": 50,
  "top_p": 1.0,
  "seed": -1
  }
}
```

<ParamField body="event_id" type="string">
  事件唯一标识。
</ParamField>

<ParamField body="type" type="string">
  固定为 `session.updated`。
</ParamField>

<ParamField body="session" type="object">
  会话配置。

  <Expandable title="properties">
    <ParamField body="id" type="string">
      会话唯一 ID。
    </ParamField>

    <ParamField body="object" type="string">
      固定为 `realtime.session`。
    </ParamField>

    <ParamField body="model" type="string">
      模型名称。
    </ParamField>

    <ParamField body="temperature" type="float">
      采样温度。
    </ParamField>

    <ParamField body="modalities" type="array">
      输出模态。
    </ParamField>

    <ParamField body="voice" type="string">
      音频输出的语音。
    </ParamField>

    <ParamField body="instructions" type="string">
      模型的系统指令。
    </ParamField>

    <ParamField body="audio" type="object">
      回显的音频格式配置。若客户端传入了 `session.audio.input.format` / `session.audio.output.format`，服务端将在 `session.updated` 中按相同嵌套结构回显。未使用嵌套字段的客户端，服务端事件结构保持原有行为。

      <Expandable title="properties">
        <ParamField body="audio.input.format.type" type="string">
          用户输入音频格式。可选值：`pcm`（默认值）、`wav`。
        </ParamField>

        <ParamField body="audio.input.format.sample_rate" type="integer">
          用户输入音频采样率，单位为 Hz。
        </ParamField>

        <ParamField body="audio.output.format.type" type="string">
          模型输出音频格式。可选值：`pcm`（默认值）、`wav`。
        </ParamField>

        <ParamField body="audio.output.format.sample_rate" type="integer">
          模型输出音频采样率，单位为 Hz。
        </ParamField>
      </Expandable>
    </ParamField>

    <ParamField body="input_audio_format" type="string">
      历史兼容字段，回显客户端配置的输入音频格式。
    </ParamField>

    <ParamField body="output_audio_format" type="string">
      历史兼容字段，回显客户端配置的输出音频格式。
    </ParamField>

    <ParamField body="input_audio_transcription" type="object">
      语音转录配置。

      <Expandable title="properties">
        <ParamField body="model" type="string">
          转录模型，固定为 `qwen3-asr-flash-realtime`，不支持修改。
        </ParamField>
      </Expandable>
    </ParamField>

    <ParamField body="turn_detection" type="object">
      VAD 配置。

      <Expandable title="properties">
        <ParamField body="type" type="string">
          VAD 类型。取值：`server_vad`（默认值）或 `semantic_vad`。详情请参见[客户端事件](/api-reference/real-time-multimodal/client-events)。
        </ParamField>

        <ParamField body="threshold" type="float">
          VAD 检测阈值。
        </ParamField>

        <ParamField body="silence_duration_ms" type="integer">
          判定语音结束前的静默时长（毫秒）。
        </ParamField>

        <ParamField body="idle_timeout_ms" type="integer">
          静默超时时间（毫秒）。仅在`server_vad`模式下，使用`qwen3.5-omni-plus-realtime`或`qwen3.5-omni-flash-realtime`模型时返回。
        </ParamField>

        <ParamField body="prefix_padding_ms" type="integer">
          语音开始前保留的音频时长（毫秒）。
        </ParamField>

        <ParamField body="create_response" type="boolean">
          检测到语音结束后是否自动创建响应。
        </ParamField>

        <ParamField body="interrupt_response" type="boolean">
          检测到新语音时是否中断当前响应。
        </ParamField>
      </Expandable>
    </ParamField>

    <ParamField body="max_response_output_token" type="string">
      响应输出的最大 token 数，`"inf"` 表示不限制。
    </ParamField>

    <ParamField body="top_p" type="float">
      核采样概率阈值。
    </ParamField>

    <ParamField body="top_k" type="integer">
      采样时的候选 token 数量。
    </ParamField>

    <ParamField body="max_tokens" type="integer">
      响应的最大 token 数。
    </ParamField>

    <ParamField body="repetition_penalty" type="float">
      重复序列惩罚系数。
    </ParamField>

    <ParamField body="presence_penalty" type="float">
      重复内容惩罚系数。
    </ParamField>

    <ParamField body="seed" type="integer">
      用于结果复现的随机种子。
    </ParamField>
  </Expandable>
</ParamField>

## input\_audio\_buffer.speech\_started

VAD 模式下，当音频缓冲区中检测到语音开始时发送。

<Note>在检测到语音之前，每次向缓冲区添加音频时也可能触发此事件。</Note>

```json Example
{
  "event_id": "event_Pvp8nEhsQuGCQbFJ9x58n",
  "type": "input_audio_buffer.speech_started",
  "audio_start_ms": 3647,
  "item_id": "item_YbAiGvK2H7YaS34o4R6Ba"
}
```

<ParamField body="event_id" type="string">
  事件唯一标识。
</ParamField>

<ParamField body="type" type="string">
  固定为 `input_audio_buffer.speech_started`。
</ParamField>

<ParamField body="audio_start_ms" type="integer">
  从音频输入开始到首次检测到语音的毫秒数。
</ParamField>

<ParamField body="item_id" type="string">
  用户消息项 ID，在语音结束时创建。该消息项将用户输入追加到对话历史中用于推理。
</ParamField>

## input\_audio\_buffer.speech\_stopped

VAD 模式下，当音频缓冲区中语音结束时发送。服务端同时会发送 `conversation.item.created` 来创建用户消息项。

```json Example
{
  "event_id": "event_UhQiqNVRsgUiq4KUS5Xb5",
  "type": "input_audio_buffer.speech_stopped",
  "audio_end_ms": 4453,
  "item_id": "item_YbAiGvK2H7YaS34o4R6Ba"
}
```

<ParamField body="event_id" type="string">
  事件唯一标识。
</ParamField>

<ParamField body="type" type="string">
  固定为 `input_audio_buffer.speech_stopped`。
</ParamField>

<ParamField body="audio_end_ms" type="integer">
  从会话开始到语音结束的毫秒数。
</ParamField>

<ParamField body="item_id" type="string">
  用户消息项 ID（将被创建）。
</ParamField>

## input\_audio\_buffer.committed

输入音频缓冲区提交时发送。

- VAD 模式下，用户说话结束后缓冲区自动提交。

- 手动模式下，在客户端发送 `input_audio_buffer.commit` 后触发。

```json Example
{
  "event_id": "event_Iy6sUzL1nmdFgshFYxJEz",
  "type": "input_audio_buffer.committed",
  "item_id": "item_YbAiGvK2H7YaS34o4R6Ba"
}
```

<ParamField body="event_id" type="string">
  事件唯一标识。
</ParamField>

<ParamField body="type" type="string">
  固定为 `input_audio_buffer.committed`。
</ParamField>

<ParamField body="item_id" type="string">
  用户消息项 ID（将被创建）。
</ParamField>

## input\_audio\_buffer.cleared

客户端发送 `input_audio_buffer.clear` 后触发。

```json Example
{
  "event_id": "event_RoUu4T8yExPMI37GKwaOC",
  "type": "input_audio_buffer.cleared"
}
```

<ParamField body="event_id" type="string">
  事件唯一标识。
</ParamField>

<ParamField body="type" type="string">
  固定为 `input_audio_buffer.cleared`。
</ParamField>

## conversation.item.created

创建对话项时发送。

```json Example
{
  "event_id": "event_JEfkrr9gO3Ny7Xcv9bGVd",
  "type": "conversation.item.created",
  "item": {
  "id": "item_YbAiGvK2H7YaS34o4R6Ba",
  "object": "realtime.item",
  "type": "message",
  "status": "in_progress",
  "role": "user",
  "content": [
      {
    "type": "input_audio"
      }
  ]
  }
}
```

<ParamField body="event_id" type="string">
  事件唯一标识。
</ParamField>

<ParamField body="type" type="string">
  固定为 `conversation.item.created`。
</ParamField>

<ParamField body="item" type="object">
  对话项。

  <Expandable title="properties">
    <ParamField body="id" type="string">
      对话项唯一 ID。
    </ParamField>

    <ParamField body="object" type="string">
      固定为 `realtime.item`。
    </ParamField>

    <ParamField body="type" type="string">
      对话项类型，当前值为 `message`。
    </ParamField>

    <ParamField body="status" type="string">
      对话项状态。
    </ParamField>

    <ParamField body="role" type="string">
      消息角色。
    </ParamField>

    <ParamField body="content" type="array">
      消息内容。
    </ParamField>
  </Expandable>
</ParamField>

## conversation.item.input\_audio\_transcription.delta

开启输入音频转录后，此事件会在用户说话过程中高频发送，用于展示实时识别的中间结果。您可以通过拼接 `text` + `stash` 获取当前最完整的句子预览。

```json Example
{
  "event_id": "event_C7jzoeSFuiwOZS6tR14yx",
  "type": "conversation.item.input_audio_transcription.delta",
  "item_id": "item_ThVYhLHOdeXb4bBSvzSFF",
  "content_index": 0,
  "text": "",
  "stash": "今天天气怎么样？",
  "language": "zh",
  "emotion": "neutral",
  "obfuscation": "ABEXGYmxdmc97u"
}
```

在任何时刻，要获取当前最完整的句子预览，都需要将这两个字段拼接起来：实时预览句子 = `text` + `stash`。

<Accordion title="点击查看示例">
  假设用户正在说："今天天气不错，阳光明媚。"

  以下是您可能会收到的事件流以及如何解读它们：

| 时间点 | 用户说话进度   | API 响应 (text 和 stash)            | 客户端 UI 应显示 (text + stash)                                                         |
| --- | -------- | -------------------------------- | --------------------------------------------------------------------------------- |
| T1  | "今天……"   | text: "" / stash: "今天"           | 今天                                                                                |
| T2  | "……天气……" | text: "" / stash: "今天天气"         | 今天天气                                                                              |
| T3  | "……不错"   | text: "今天" / stash: "天气不错"       | 今天天气不错（"今天"已被确认并移入 text）                                                          |
| T4  | （短暂停顿）   | text: "今天天气不错，" / stash: ""      | 今天天气不错，（前半句完全确认）                                                                  |
| T5  | "……阳光……" | text: "今天天气不错，" / stash: "阳光"    | 今天天气不错，阳光                                                                         |
| T6  | "……明媚。"  | text: "今天天气不错，" / stash: "阳光明媚。" | 今天天气不错，阳光明媚。                                                                      |
| T7  | （结束说话）   | -                                | 使用 conversation.item.input\_audio\_transcription.completed 的 transcript 内容作为最终结果。 |
</Accordion>

<ParamField body="event_id" type="string">
  本次事件唯一标识符。
</ParamField>

<ParamField body="type" type="string">
  事件类型，固定为 `conversation.item.input_audio_transcription.delta`。
</ParamField>

<ParamField body="item_id" type="string">
  关联的对话项 ID。
</ParamField>

<ParamField body="content_index" type="integer">
  包含音频的内容部分的索引。
</ParamField>

<ParamField body="text" type="string">
  已确认的文本前缀。这是当前句子中，模型已确认不会再变更的部分。
</ParamField>

<ParamField body="stash" type="string">
  预识别的文本后缀。这是紧跟在已确认部分之后，模型仍在处理、可能会被修正的临时草稿。
</ParamField>

<ParamField body="language" type="string">
  当前识别到的语言代码（如 `zh`、`en`）。
</ParamField>

<ParamField body="emotion" type="string">
  当前检测到的用户情绪（如 `neutral`、`happy`）。
</ParamField>

## conversation.item.input\_audio\_transcription.completed

音频缓冲并转录完成后发送。转录由内置的语音识别模型（`qwen3-asr-flash-realtime`）处理，不支持修改。

<Note>转录文本可能与 Qwen-Omni-Realtime 处理的文本有所不同，仅供参考。</Note>

```json Example
{
  "event_id": "event_FrrZcxiDfTB9LD9p4pVng",
  "type": "conversation.item.input_audio_transcription.completed",
  "item_id": "item_YbAiGvK2H7YaS34o4R6Ba",
  "content_index": 0,
  "transcript": "Hello."
}
```

<ParamField body="event_id" type="string">
  事件唯一标识。
</ParamField>

<ParamField body="type" type="string">
  固定为 `conversation.item.input_audio_transcription.completed`。
</ParamField>

<ParamField body="item_id" type="string">
  用户消息项 ID。
</ParamField>

<ParamField body="content_index" type="integer">
  固定为 0。
</ParamField>

<ParamField body="transcript" type="string">
  转录文本。
</ParamField>

## conversation.item.input\_audio\_transcription.failed

输入音频转录失败时发送（需已启用转录功能）。与 `error` 事件相互独立。

```json Example
{
  "event_id": "event_RoUu4T8yExPMI37GKwaOC",
  "type": "conversation.item.input_audio_transcription.failed",
  "item_id": "<item_id>",
  "content_index": 0,
  "error": {
  "code": "<code>",
  "message": "<message>",
  "param": "<param>"
  }
}
```

<ParamField body="event_id" type="string">
  事件唯一标识。
</ParamField>

<ParamField body="type" type="string">
  固定为 `conversation.item.input_audio_transcription.failed`。
</ParamField>

<ParamField body="item_id" type="string">
  用户消息项 ID。
</ParamField>

<ParamField body="content_index" type="integer">
  固定为 0。
</ParamField>

<ParamField body="error" type="object">
  错误详情。

  <Expandable title="properties">
    <ParamField body="code" type="string">
      错误码。
    </ParamField>

    <ParamField body="message" type="string">
      错误信息。
    </ParamField>

    <ParamField body="param" type="string">
      相关参数。
    </ParamField>
  </Expandable>
</ParamField>

## response.created

模型开始生成响应时发送。

```json Example
{
  "event_id": "event_XuDavMzQN3KKepqGu3KRh",
  "type": "response.created",
  "response": {
  "id": "resp_HaVOPdbmX6vifiV5pAfJY",
  "object": "realtime.response",
  "conversation_id": "conv_FjJaccpnvwHNo9cPVuzGc",
  "status": "in_progress",
  "modalities": [
      "text",
      "audio"
  ],
  "voice": "Cherry",
  "output_audio_format": "pcm",
  "output": []
  }
}
```

<ParamField body="event_id" type="string">
  事件唯一标识。
</ParamField>

<ParamField body="type" type="string">
  固定为 `response.created`。
</ParamField>

<ParamField body="response" type="object">
  响应对象。

  <Expandable title="properties">
    <ParamField body="id" type="string">
      响应唯一 ID。
    </ParamField>

    <ParamField body="conversation_id" type="string">
      会话 ID。
    </ParamField>

    <ParamField body="object" type="string">
      固定为 `realtime.response`。
    </ParamField>

    <ParamField body="status" type="string">
      响应状态：`completed`、`failed`、`in_progress` 或 `incomplete`。
    </ParamField>

    <ParamField body="modalities" type="array">
      响应模态。
    </ParamField>

    <ParamField body="voice" type="string">
      音频输出的语音。
    </ParamField>

    <ParamField body="output_audio_format" type="string">
      输出音频格式。
    </ParamField>

    <ParamField body="output" type="array">
      该事件中为空。
    </ParamField>
  </Expandable>
</ParamField>

## response.done

响应生成完成后发送。`response` 对象包含所有输出项，但不含原始音频数据。

```json Example
{
  "event_id": "event_CSaxRRYLvbrfexDXAEuDG",
  "type": "response.done",
  "response": {
  "id": "resp_HaVOPdbmX6vifiV5pAfJY",
  "object": "realtime.response",
  "conversation_id": "conv_FjJaccpnvwHNo9cPVuzGc",
  "status": "completed",
  "modalities": [
      "text",
      "audio"
  ],
  "voice": "Cherry",
  "output_audio_format": "pcm",
  "output": [
      {
    "id": "item_Ls6MtCUWO7LM4E59QziNv",
    "object": "realtime.item",
    "type": "message",
    "status": "completed",
    "role": "assistant",
    "content": [
          {
      "type": "audio",
      "transcript": "Hello! Is there anything I can help you with?"
          }
    ]
      }
  ],
  "usage": {
      "total_tokens": 377,
      "input_tokens": 336,
      "output_tokens": 41,
      "input_tokens_details": {
    "text_tokens": 228,
    "audio_tokens": 108
      },
      "output_tokens_details": {
    "text_tokens": 9,
    "audio_tokens": 32
      }
  }
  }
}
```

<ParamField body="event_id" type="string">
  事件唯一标识。
</ParamField>

<ParamField body="type" type="string">
  固定为 `response.done`。
</ParamField>

<ParamField body="response" type="object">
  响应对象。

  <Expandable title="properties">
    <ParamField body="id" type="string">
      响应唯一 ID。
    </ParamField>

    <ParamField body="conversation_id" type="string">
      会话 ID。
    </ParamField>

    <ParamField body="object" type="string">
      固定为 `realtime.response`。
    </ParamField>

    <ParamField body="status" type="string">
      响应状态。
    </ParamField>

    <ParamField body="modalities" type="array">
      响应模态。
    </ParamField>

    <ParamField body="voice" type="string">
      音频输出的语音。
    </ParamField>

    <ParamField body="output_audio_format" type="string">
      输出音频格式。
    </ParamField>

    <ParamField body="output" type="array">
      响应输出。

      <Expandable title="properties">
        <ParamField body="id" type="string">
          输出项 ID。
        </ParamField>

        <ParamField body="type" type="string">
          输出项类型，当前为 `message`。
        </ParamField>

        <ParamField body="object" type="string">
          输出项对象类型，当前为 `realtime.item`。
        </ParamField>

        <ParamField body="status" type="string">
          输出项状态。
        </ParamField>

        <ParamField body="role" type="string">
          输出项角色。
        </ParamField>

        <ParamField body="content" type="array">
          输出项内容。

          <Expandable title="properties">
            <ParamField body="type" type="string">
              内容类型：`text` 为纯文本，`audio` 为音频输出。
            </ParamField>

            <ParamField body="text" type="string">
              文本内容。
            </ParamField>

            <ParamField body="transcript" type="string">
              音频的转录文本。
            </ParamField>
          </Expandable>
        </ParamField>
      </Expandable>
    </ParamField>

    <ParamField body="usage" type="object">
      本次响应的 token 用量。
    </ParamField>
  </Expandable>
</ParamField>

## response.text.delta

输出模态为纯文本时，模型生成文本片段时发送。

```json Example
{
  "delta": "Hello",
  "event_id": "event_TH49MauuPmRo1RGaMSlP7",
  "type": "response.text.delta",
  "response_id": "resp_PrRSvPVpnCExdUOGHHLuP",
  "item_id": "item_L8IRm9kRXFpxoOjDqDC96",
  "output_index": 0,
  "content_index": 0
}
```

<ParamField body="event_id" type="string">
  事件唯一标识。
</ParamField>

<ParamField body="type" type="string">
  固定为 `response.text.delta`。
</ParamField>

<ParamField body="delta" type="string">
  增量文本片段。
</ParamField>

<ParamField body="response_id" type="string">
  响应 ID。
</ParamField>

<ParamField body="item_id" type="string">
  消息项 ID，用于关联同一消息的各项内容。
</ParamField>

<ParamField body="output_index" type="integer">
  输出项索引，固定为 0。
</ParamField>

<ParamField body="content_index" type="integer">
  内容部分索引，固定为 0。
</ParamField>

## response.text.done

纯文本输出生成完成时发送。

<Note>响应被中断、未完成或取消时也会发送此事件。</Note>

```json Example
{
  "event_id": "event_B1lIeE2Nac33zn5V7h2mm",
  "type": "response.text.done",
  "response_id": "resp_B1lIdtjF4Noqpn5NOjznj",
  "item_id": "item_B1lIdJsAJlJiFs8ztWpJt",
  "output_index": 0,
  "content_index": 0,
  "text": "How can I assist you today?"
}
```

<ParamField body="event_id" type="string">
  事件唯一标识。
</ParamField>

<ParamField body="type" type="string">
  固定为 `response.text.done`。
</ParamField>

<ParamField body="response_id" type="string">
  响应 ID。
</ParamField>

<ParamField body="item_id" type="string">
  消息项 ID。
</ParamField>

<ParamField body="output_index" type="integer">
  输出项索引。
</ParamField>

<ParamField body="content_index" type="integer">
  内容部分索引。
</ParamField>

<ParamField body="text" type="string">
  完整文本输出。
</ParamField>

## response.audio.delta

输出模态包含音频时，模型生成音频片段时发送。

```json Example
{
  "event_id": "event_B1osWMZBtrEQbiIwW0qHQ",
  "type": "response.audio.delta",
  "response_id": "resp_P79OOMs8LnrXVpiIHUCKR",
  "item_id": "item_OFaPGtzfWCPyGzxnuEX9i",
  "output_index": 0,
  "content_index": 0,
  "delta": "{base64 audio}"
}
```

<ParamField body="event_id" type="string">
  事件唯一标识。
</ParamField>

<ParamField body="type" type="string">
  固定为 `response.audio.delta`。
</ParamField>

<ParamField body="response_id" type="string">
  响应 ID。
</ParamField>

<ParamField body="item_id" type="string">
  消息项 ID。
</ParamField>

<ParamField body="output_index" type="integer">
  输出项索引。
</ParamField>

<ParamField body="content_index" type="integer">
  内容部分索引。
</ParamField>

<ParamField body="delta" type="string">
  Base64 编码的音频片段。
</ParamField>

## response.audio.done

音频输出生成完成时发送。

<Note>响应被中断、未完成或取消时也会发送此事件。</Note>

```json Example
{
  "event_id": "event_Le1TDl7VfyHQxl47DtGxI",
  "type": "response.audio.done",
  "response_id": "resp_HaVOPdbmX6vifiV5pAfJY",
  "item_id": "item_Ls6MtCUWO7LM4E59QziNv",
  "output_index": 0,
  "content_index": 0
}
```

<ParamField body="event_id" type="string">
  事件唯一标识。
</ParamField>

<ParamField body="type" type="string">
  固定为 `response.audio.done`。
</ParamField>

<ParamField body="response_id" type="string">
  响应 ID。
</ParamField>

<ParamField body="item_id" type="string">
  消息项 ID。
</ParamField>

<ParamField body="output_index" type="integer">
  输出项索引。
</ParamField>

<ParamField body="content_index" type="integer">
  内容部分索引。
</ParamField>

## response.audio\_transcript.delta

输出模态包含音频时，模型生成转录文本片段时发送。

```json Example
{
  "event_id": "event_BksW7fOwnyavZdDxIzZYM",
  "type": "response.audio_transcript.delta",
  "response_id": "resp_HaVOPdbmX6vifiV5pAfJY",
  "item_id": "item_Ls6MtCUWO7LM4E59QziNv",
  "output_index": 0,
  "content_index": 0,
  "delta": "Is there anything"
}
```

<ParamField body="event_id" type="string">
  事件唯一标识。
</ParamField>

<ParamField body="type" type="string">
  固定为 `response.audio_transcript.delta`。
</ParamField>

<ParamField body="response_id" type="string">
  响应 ID。
</ParamField>

<ParamField body="item_id" type="string">
  消息项 ID。
</ParamField>

<ParamField body="output_index" type="integer">
  输出项索引。
</ParamField>

<ParamField body="content_index" type="integer">
  内容部分索引。
</ParamField>

<ParamField body="delta" type="string">
  增量转录文本。
</ParamField>

## response.audio\_transcript.done

音频转录文本生成完成时发送。

```json Example
{
  "event_id": "event_X49tL2WerT4WjxcmH16lS",
  "type": "response.audio_transcript.done",
  "response_id": "resp_HaVOPdbmX6vifiV5pAfJY",
  "item_id": "item_Ls6MtCUWO7LM4E59QziNv",
  "output_index": 0,
  "content_index": 0,
  "transcript": "Hello! Is there anything I can help you with?"
}
```

<ParamField body="event_id" type="string">
  事件唯一标识。
</ParamField>

<ParamField body="type" type="string">
  固定为 `response.audio_transcript.done`。
</ParamField>

<ParamField body="response_id" type="string">
  响应 ID。
</ParamField>

<ParamField body="item_id" type="string">
  消息项 ID。
</ParamField>

<ParamField body="output_index" type="integer">
  输出项索引。
</ParamField>

<ParamField body="content_index" type="integer">
  内容部分索引。
</ParamField>

<ParamField body="transcript" type="string">
  完整转录文本。
</ParamField>

## response.output\_item.added

响应生成过程中创建新输出项时发送。

```json Example
{
  "event_id": "event_DsCO341DEVtiATtCB6BUY",
  "type": "response.output_item.added",
  "response_id": "resp_HaVOPdbmX6vifiV5pAfJY",
  "output_index": 0,
  "item": {
  "id": "item_Ls6MtCUWO7LM4E59QziNv",
  "object": "realtime.item",
  "type": "message",
  "status": "in_progress",
  "role": "assistant",
  "content": []
  }
}
```

<ParamField body="event_id" type="string">
  事件唯一标识。
</ParamField>

<ParamField body="type" type="string">
  固定为 `response.output_item.added`。
</ParamField>

<ParamField body="response_id" type="string">
  响应 ID。
</ParamField>

<ParamField body="output_index" type="integer">
  输出项索引。
</ParamField>

<ParamField body="item" type="object">
  输出项。

  <Expandable title="properties">
    <ParamField body="id" type="string">
      输出项唯一 ID。
    </ParamField>

    <ParamField body="object" type="string">
      固定为 `realtime.item`。
    </ParamField>

    <ParamField body="status" type="string">
      输出项状态。
    </ParamField>

    <ParamField body="role" type="string">
      发送者角色。
    </ParamField>

    <ParamField body="content" type="array">
      消息内容。
    </ParamField>
  </Expandable>
</ParamField>

## response.output\_item.done

输出项完成时发送。

```json Example
{
  "event_id": "event_MEu5nlLw1LsOguHiehIP8",
  "type": "response.output_item.done",
  "response_id": "resp_HaVOPdbmX6vifiV5pAfJY",
  "output_index": 0,
  "item": {
  "id": "item_Ls6MtCUWO7LM4E59QziNv",
  "object": "realtime.item",
  "type": "message",
  "status": "completed",
  "role": "assistant",
  "content": [
      {
    "type": "audio",
    "transcript": "Hello! Is there anything I can help you with?"
      }
  ]
  }
}
```

<ParamField body="event_id" type="string">
  事件唯一标识。
</ParamField>

<ParamField body="type" type="string">
  固定为 `response.output_item.done`。
</ParamField>

<ParamField body="response_id" type="string">
  响应 ID。
</ParamField>

<ParamField body="output_index" type="integer">
  输出项索引。
</ParamField>

<ParamField body="item" type="object">
  输出项。

  <Expandable title="properties">
    <ParamField body="id" type="string">
      输出项唯一 ID。
    </ParamField>

    <ParamField body="object" type="string">
      固定为 `realtime.item`。
    </ParamField>

    <ParamField body="status" type="string">
      输出项状态。
    </ParamField>

    <ParamField body="role" type="string">
      发送者角色。
    </ParamField>

    <ParamField body="content" type="array">
      消息内容。
    </ParamField>
  </Expandable>
</ParamField>

## response.content\_part.added

响应生成过程中，向助手消息添加新内容部分时发送。

```json Example
{
  "event_id": "event_AVBOmrgY3C8bjlRajfSUT",
  "type": "response.content_part.added",
  "response_id": "resp_HaVOPdbmX6vifiV5pAfJY",
  "item_id": "item_Ls6MtCUWO7LM4E59QziNv",
  "output_index": 0,
  "content_index": 0,
  "part": {
  "type": "audio",
  "text": ""
  }
}
```

<ParamField body="event_id" type="string">
  事件唯一标识。
</ParamField>

<ParamField body="type" type="string">
  固定为 `response.content_part.added`。
</ParamField>

<ParamField body="response_id" type="string">
  响应 ID。
</ParamField>

<ParamField body="item_id" type="string">
  消息项 ID。
</ParamField>

<ParamField body="output_index" type="integer">
  输出项索引，固定为 0。
</ParamField>

<ParamField body="content_index" type="integer">
  内容部分索引，固定为 0。
</ParamField>

<ParamField body="part" type="object">
  内容部分。

  <Expandable title="properties">
    <ParamField body="type" type="string">
      内容类型。
    </ParamField>

    <ParamField body="text" type="string">
      文本内容。
    </ParamField>
  </Expandable>
</ParamField>

## response.content\_part.done

助手消息中的内容部分流式传输完成时发送。

```json Example
{
  "event_id": "event_Il8HD19v58Qr5IBkw7LtN",
  "type": "response.content_part.done",
  "response_id": "resp_HaVOPdbmX6vifiV5pAfJY",
  "item_id": "item_Ls6MtCUWO7LM4E59QziNv",
  "output_index": 0,
  "content_index": 0,
  "part": {
  "type": "audio",
  "text": "Hello! Is there anything I can help you with?"
  }
}
```

<ParamField body="event_id" type="string">
  事件唯一标识。
</ParamField>

<ParamField body="type" type="string">
  固定为 `response.content_part.done`。
</ParamField>

<ParamField body="response_id" type="string">
  响应 ID。
</ParamField>

<ParamField body="item_id" type="string">
  消息项 ID。
</ParamField>

<ParamField body="output_index" type="integer">
  输出项索引，固定为 0。
</ParamField>

<ParamField body="content_index" type="integer">
  内容部分索引，固定为 0。
</ParamField>

<ParamField body="part" type="object">
  内容部分。

  <Expandable title="properties">
    <ParamField body="type" type="string">
      内容类型。
    </ParamField>

    <ParamField body="text" type="string">
      文本内容。
    </ParamField>
  </Expandable>
</ParamField>
