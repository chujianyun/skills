> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 实时语音识别（Qwen-ASR-Realtime）服务端事件

> WebSocket 服务端事件参考

WebSocket 会话中服务端发送的事件。

<Note>
  **使用指南**： 功能概述和示例代码请参见[实时语音识别](/developer-guides/speech/asr-realtime)。
</Note>

## error

客户端或服务端发生错误时发送。

```json Example
{
  "event_id": "event_B2uoU7VOt1AAITsPRPH9n",
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "code": "invalid_value",
    "message": "Invalid value: 'pcm16'. Supported values are: 'pcm', 'opus'.",
    "param": "session.input_audio_format",
    "event_id": "event_123"
  }
}
```

<ParamField body="event_id" type="string">
  事件的唯一标识符。
</ParamField>

<ParamField body="type" type="string">
  事件类型，固定为 `error`。
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
      错误信息。解决方案请参见[错误信息](/api-reference/preparation/error-messages)。
    </ParamField>

    <ParamField body="param" type="string">
      与错误相关的参数。
    </ParamField>

    <ParamField body="event_id" type="string">
      与错误相关的事件 ID。
    </ParamField>
  </Expandable>
</ParamField>

## session.created

连接建立后的第一个事件，包含默认的会话配置。

```json Example
{
  "event_id": "event_1234",
  "type": "session.created",
  "session": {
    "id": "sess_001",
    "object": "realtime.session",
    "model": "qwen3-asr-flash-realtime",
    "modalities": ["text"],
    "input_audio_format": "pcm",
    "input_audio_transcription": null,
    "turn_detection": {
      "type": "server_vad",
      "threshold": 0.2,
      "silence_duration_ms": 800
    }
  }
}
```

<ParamField body="event_id" type="string">
  事件的唯一标识符。
</ParamField>

<ParamField body="type" type="string">
  事件类型，固定为 `session.created`。
</ParamField>

<ParamField body="session" type="object">
  会话配置。

  <Expandable title="properties">
    <ParamField body="id" type="string">
      当前 WebSocket 会话的 ID。
    </ParamField>

    <ParamField body="object" type="string">
      固定为 `realtime.session`。
    </ParamField>

    <ParamField body="model" type="string">
      模型名称。
    </ParamField>

    <ParamField body="modalities" type="array">
      输出模态，固定为 `["text"]`。
    </ParamField>

    <ParamField body="input_audio_format" type="string">
      输入音频格式。
    </ParamField>

    <ParamField body="input_audio_transcription" type="object">
      语音识别设置。详见 [session.update](/api-reference/speech-recognition/qwen-asr-realtime/client-events) 客户端事件的 `input_audio_transcription` 参数。
    </ParamField>

    <ParamField body="turn_detection" type="object">
      语音活动检测（VAD）设置。

      <Expandable title="properties">
        <ParamField body="type" type="string">
          固定为 `server_vad`。
        </ParamField>

        <ParamField body="threshold" type="float">
          VAD 检测阈值。
        </ParamField>

        <ParamField body="silence_duration_ms" type="integer">
          检测到句子断点前的静默时长（毫秒）。
        </ParamField>
      </Expandable>
    </ParamField>
  </Expandable>
</ParamField>

## session.updated

[session.update](/api-reference/speech-recognition/qwen-asr-realtime/client-events) 事件处理完成后发送。如果处理失败，则发送 `error` 事件。

其他参数说明请参见 [session.created](#session-created)。

```json Example
{
  "event_id": "event_1234",
  "type": "session.updated",
  "session": {
    "id": "sess_001",
    "object": "realtime.session",
    "model": "qwen3-asr-flash-realtime",
    "modalities": ["text"],
    "input_audio_format": "pcm",
    "input_audio_transcription": null,
    "turn_detection": {
      "type": "server_vad",
      "threshold": 0.2,
      "silence_duration_ms": 800
    }
  }
}
```

<ParamField body="event_id" type="string">
  事件的唯一标识符。
</ParamField>

<ParamField body="type" type="string">
  事件类型，固定为 `session.updated`。
</ParamField>

## input\_audio\_buffer.speech\_started

VAD 模式下，检测到音频缓冲区中有语音开始时发送。

<Note>
  每次向缓冲区添加音频时都会触发，除非语音起始点已被检测到。
</Note>

```json Example
{
  "event_id": "event_B1lV7FPbgTv9qGxPI1tH4",
  "type": "input_audio_buffer.speech_started",
  "audio_start_ms": 64,
  "item_id": "item_B1lV7jWLscp4mMV8hSs8c"
}
```

<ParamField body="event_id" type="string">
  事件的唯一标识符。
</ParamField>

<ParamField body="type" type="string">
  事件类型，固定为 `input_audio_buffer.speech_started`。
</ParamField>

<ParamField body="audio_start_ms" type="integer">
  从缓冲区起始到检测到语音的时间（毫秒）。
</ParamField>

<ParamField body="item_id" type="string">
  即将创建的用户消息项 ID。
</ParamField>

## input\_audio\_buffer.speech\_stopped

VAD 模式下，检测到音频缓冲区中语音结束时发送。紧接着会发送 `conversation.item.created` 事件，包含用户消息项。

```json Example
{
  "event_id": "event_B3GGEYh2orwNIdhUagZPz",
  "type": "input_audio_buffer.speech_stopped",
  "audio_end_ms": 28128,
  "item_id": "item_B3GGE8ry4yqbqJGzrVhEM"
}
```

<ParamField body="event_id" type="string">
  事件的唯一标识符。
</ParamField>

<ParamField body="type" type="string">
  事件类型，固定为 `input_audio_buffer.speech_stopped`。
</ParamField>

<ParamField body="audio_end_ms" type="integer">
  从会话开始到语音结束的时间（毫秒）。
</ParamField>

<ParamField body="item_id" type="string">
  语音结束时创建的用户消息项 ID。
</ParamField>

## input\_audio\_buffer.committed

输入音频缓冲区提交后发送。

- **VAD 模式**： 服务端检测到语音段结束后自动触发。

- **手动模式**： 通过 [input\_audio\_buffer.append](/api-reference/speech-recognition/qwen-asr-realtime/client-events) 发送完音频，再发送 [input\_audio\_buffer.commit](/api-reference/speech-recognition/qwen-asr-realtime/client-events) 后触发。

```json Example
{
  "event_id": "event_1121",
  "type": "input_audio_buffer.committed",
  "previous_item_id": "msg_001",
  "item_id": "msg_002"
}
```

<ParamField body="event_id" type="string">
  事件的唯一标识符。
</ParamField>

<ParamField body="type" type="string">
  事件类型，固定为 `input_audio_buffer.committed`。
</ParamField>

<ParamField body="previous_item_id" type="string">
  上一个对话项的 ID。
</ParamField>

<ParamField body="item_id" type="string">
  即将创建的用户对话项 ID。
</ParamField>

## conversation.item.created

对话项创建时发送。

```json Example
{
  "type": "conversation.item.created",
  "event_id": "event_B3GGKbCfBZTpqFHZ0P8vg",
  "previous_item_id": "item_B3GGE8ry4yqbqJGzrVhEM",
  "item": {
    "id": "item_B3GGEPlolCqdMiVbYIf5L",
    "object": "realtime.item",
    "type": "message",
    "status": "completed",
    "role": "user",
    "content": [
      {
        "type": "input_audio",
        "transcript": null
      }
    ]
  }
}
```

<ParamField body="event_id" type="string">
  事件的唯一标识符。
</ParamField>

<ParamField body="type" type="string">
  事件类型，固定为 `conversation.item.created`。
</ParamField>

<ParamField body="previous_item_id" type="string">
  上一个对话项的 ID。
</ParamField>

<ParamField body="item" type="object">
  对话项。

  <Expandable title="properties">
    <ParamField body="id" type="string">
      对话项的唯一 ID。
    </ParamField>

    <ParamField body="object" type="string">
      固定为 `realtime.item`。
    </ParamField>

    <ParamField body="type" type="string">
      固定为 `message`。
    </ParamField>

    <ParamField body="status" type="string">
      对话项的状态。
    </ParamField>

    <ParamField body="role" type="string">
      消息发送者的角色。
    </ParamField>

    <ParamField body="content" type="array">
      消息内容。

      <Expandable title="properties">
        <ParamField body="type" type="string">
          固定为 `input_audio`。
        </ParamField>

        <ParamField body="transcript" type="string">
          固定为 `null`。最终结果在 [conversation.item.input\_audio\_transcription.completed](#conversation-item-input-audio-transcription-completed) 事件中返回。
        </ParamField>
      </Expandable>
    </ParamField>
  </Expandable>
</ParamField>

## conversation.item.input\_audio\_transcription.text

高频发送，包含实时识别结果。

```json Example
{
  "event_id": "event_R7Pfu8QVBfP5HmpcbEFSd",
  "type": "conversation.item.input_audio_transcription.text",
  "item_id": "item_MpJQPNQzqVRc9aC9zMwSj",
  "content_index": 0,
  "language": "en",
  "emotion": "neutral",
  "text": "",
  "stash": "Beijing's"
}
```

<ParamField body="event_id" type="string">
  事件的唯一标识符。
</ParamField>

<ParamField body="type" type="string">
  事件类型，固定为 `conversation.item.input_audio_transcription.text`。
</ParamField>

<ParamField body="item_id" type="string">
  关联的对话项 ID。
</ParamField>

<ParamField body="content_index" type="integer">
  包含音频的 content 部分的索引。
</ParamField>

<ParamField body="language" type="string">
  检测到的语言。如果您设置了 `language` 请求参数，此值与该设置一致。可选值：

  - `zh`：中文（普通话、四川话、闽南语、吴语）
  - `yue`：粤语
  - `en`：英语
  - `ja`：日语
  - `de`：德语
  - `ko`：韩语
  - `ru`：俄语
  - `fr`：法语
  - `pt`：葡萄牙语
  - `ar`：阿拉伯语
  - `it`：意大利语
  - `es`：西班牙语
  - `hi`：印地语
  - `id`：印尼语
  - `th`：泰语
  - `tr`：土耳其语
  - `uk`：乌克兰语
  - `vi`：越南语
  - `cs`：捷克语
  - `da`：丹麦语
  - `fil`：菲律宾语
  - `fi`：芬兰语
  - `is`：冰岛语
  - `ms`：马来语
  - `no`：挪威语
  - `pl`：波兰语
  - `sv`：瑞典语
</ParamField>

<ParamField body="emotion" type="string">
  检测到的情绪。可选值：`surprised`、`neutral`、`happy`、`sad`、`disgusted`、`angry`、`fearful`。
</ParamField>

<ParamField body="text" type="string">
  已确认的文本前缀。模型已完成对这部分内容的识别，不会再修改。
</ParamField>

<ParamField body="stash" type="string">
  预识别的文本后缀。跟在已确认部分之后的临时草稿，模型可能会修正。
</ParamField>

<Tip>
  拼接 `text + stash` 可获得最完整的实时预览。
</Tip>

<Expandable title="点击查看示例">
  假设用户说了"今天天气真不错，阳光明媚"，下表展示了您可能收到的事件：

| 时间点 | 用户语音进度      | API 返回（`text` 和 `stash`）                  | UI 显示（`text + stash`）                                                                                                                         |
| --- | ----------- | ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| T1  | "今天..."     | `text`: `""` / `stash`: `"今天"`            | 今天                                                                                                                                            |
| T2  | "...天气真..." | `text`: `""` / `stash`: `"今天天气真"`         | 今天天气真                                                                                                                                         |
| T3  | "...不错"     | `text`: `"今天"` / `stash`: `"天气真不错"`       | 今天天气真不错                                                                                                                                       |
| T4  | （短暂停顿）      | `text`: `"今天天气真不错，"` / `stash`: `""`      | 今天天气真不错，                                                                                                                                      |
| T5  | "...阳光..."  | `text`: `"今天天气真不错，"` / `stash`: `"阳光"`    | 今天天气真不错，阳光                                                                                                                                    |
| T6  | "...明媚。"    | `text`: `"今天天气真不错，"` / `stash`: `"阳光明媚。"` | 今天天气真不错，阳光明媚。                                                                                                                                 |
| T7  | （用户停止说话）    | -                                         | 以 [conversation.item.input\_audio\_transcription.completed](#conversation-item-input-audio-transcription-completed) 事件中的 `transcript` 作为最终结果。 |
</Expandable>

## conversation.item.input\_audio\_transcription.completed

发送最终识别结果，标志着一个对话项的结束。

```json Example
{
  "event_id": "event_B3GGEjPT2sLzjBM74W6kB",
  "type": "conversation.item.input_audio_transcription.completed",
  "item_id": "item_B3GGC53jGOuIFcjZkmEQ9",
  "content_index": 0,
  "language": "en",
  "emotion": "neutral",
  "transcript": "What's the weather like today?"
}
```

<ParamField body="event_id" type="string">
  事件的唯一标识符。
</ParamField>

<ParamField body="type" type="string">
  事件类型，固定为 `conversation.item.input_audio_transcription.completed`。
</ParamField>

<ParamField body="item_id" type="string">
  关联的对话项 ID。
</ParamField>

<ParamField body="content_index" type="integer">
  包含音频的 content 部分的索引。
</ParamField>

<ParamField body="language" type="string">
  检测到的语言。如果您设置了 `language` 请求参数，此值与该设置一致。可选值：

  - `zh`：中文（普通话、四川话、闽南语、吴语）
  - `yue`：粤语
  - `en`：英语
  - `ja`：日语
  - `de`：德语
  - `ko`：韩语
  - `ru`：俄语
  - `fr`：法语
  - `pt`：葡萄牙语
  - `ar`：阿拉伯语
  - `it`：意大利语
  - `es`：西班牙语
  - `hi`：印地语
  - `id`：印尼语
  - `th`：泰语
  - `tr`：土耳其语
  - `uk`：乌克兰语
  - `vi`：越南语
  - `cs`：捷克语
  - `da`：丹麦语
  - `fil`：菲律宾语
  - `fi`：芬兰语
  - `is`：冰岛语
  - `ms`：马来语
  - `no`：挪威语
  - `pl`：波兰语
  - `sv`：瑞典语
</ParamField>

<ParamField body="emotion" type="string">
  检测到的情绪。可选值：`surprised`、`neutral`、`happy`、`sad`、`disgusted`、`angry`、`fearful`。
</ParamField>

<ParamField body="transcript" type="string">
  转写结果。
</ParamField>

## conversation.item.input\_audio\_transcription.failed

输入音频识别失败时发送。该事件独立于其他 `error` 事件，便于定位失败的具体项。

```json Example
{
  "event_id": "event_B4KHRpC2nXs7dLmqTVo1f",
  "type": "conversation.item.input_audio_transcription.failed",
  "item_id": "item_B4KHRmVbcQwp9yZk2UeN3",
  "content_index": 0,
  "error": {
    "code": "audio_unintelligible",
    "message": "The audio could not be transcribed.",
    "param": null
  }
}
```

<ParamField body="event_id" type="string">
  事件的唯一标识符。
</ParamField>

<ParamField body="type" type="string">
  事件类型，固定为 `conversation.item.input_audio_transcription.failed`。
</ParamField>

<ParamField body="item_id" type="string">
  关联的对话项 ID。
</ParamField>

<ParamField body="content_index" type="integer">
  包含音频的 content 部分的索引。
</ParamField>

<ParamField body="error" type="object">
  错误详情。

  <Expandable title="properties">
    <ParamField body="code" type="string">
      错误码。
    </ParamField>

    <ParamField body="message" type="string">
      错误信息。解决方案请参见[错误信息](/api-reference/preparation/error-messages)。
    </ParamField>

    <ParamField body="param" type="string">
      与错误相关的参数。
    </ParamField>
  </Expandable>
</ParamField>

## session.finished

确认所有识别已完成。在您发送 [session.finish](/api-reference/speech-recognition/qwen-asr-realtime/client-events) 后返回。收到此事件后即可断开连接。

```json Example
{
  "event_id": "event_2239",
  "type": "session.finished"
}
```

<ParamField body="event_id" type="string">
  事件的唯一标识符。
</ParamField>

<ParamField body="type" type="string">
  事件类型，固定为 `session.finished`。
</ParamField>
