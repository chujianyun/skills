> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# LiveTranslate server events

> WebSocket 服务端事件参考

qwen3.5-livetranslate-flash-realtime API 的服务端事件。

<Note>参考：[语音翻译](/developer-guides/speech/realtime-translation)。</Note>

## error

服务端返回的错误。

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
  事件 ID。
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
      相关参数，如 `session.modalities`。
    </ParamField>
  </Expandable>
</ParamField>

## session.created

连接建立时发送，包含默认会话配置。

```json Example
{
  "event_id": "event_QxBGpjBDmDDQQWDtrqBKB",
  "type": "session.created",
  "session": {
    "id": "sess_OozZ1vtbPt2muDflHODIH",
    "object": "realtime.session",
    "model": "qwen3.5-livetranslate-flash-realtime",
    "modalities": [
      "text",
      "audio"
    ],
    "voice": "Cherry",
    "sample_rate": 16000,
    "input_audio_format": "pcm",
    "output_audio_format": "pcm",
    "input_audio_transcription": {
      "model": "qwen3-asr-flash-realtime",
      "language": "zh"
    },
    "turn_detection": {
      "type": "server_vad",
      "threshold": 0.2,
      "prefix_padding_ms": 300,
      "silence_duration_ms": 1000,
      "create_response": true,
      "interrupt_response": true
    },
    "translation": {
      "language": "en",
      "corpus": {
        "phrases": {
          "人工智能": "Artificial Intelligence",
          "机器学习": "Machine Learning"
        }
      }
    },
    "enable_voice_clone": true,
    "voice_clone_options": {
      "frequency": "once"
    }
  }
}
```

<ParamField body="event_id" type="string">
  事件 ID。
</ParamField>

<ParamField body="type" type="string">
  固定为 `session.created`。
</ParamField>

<ParamField body="session" type="object">
  会话配置。

  <Expandable title="properties">
    <ParamField body="id" type="string">
      会话 ID。
    </ParamField>

    <ParamField body="object" type="string">
      固定为 `realtime.session`。
    </ParamField>

    <ParamField body="model" type="string">
      使用的模型。
    </ParamField>

    <ParamField body="modalities" type="array">
      输出模态。
    </ParamField>

    <ParamField body="voice" type="string">
      音频输出的音色。
    </ParamField>

    <ParamField body="sample_rate" type="integer">
      输入音频的采样率，单位为 Hz。
    </ParamField>

    <ParamField body="input_audio_format" type="string">
      输入音频格式（默认为 `pcm`）。
    </ParamField>

    <ParamField body="output_audio_format" type="string">
      输出音频格式（默认为 `pcm`）。
    </ParamField>

    <ParamField body="input_audio_transcription" type="object">
      输入音频转录配置。仅在会话配置了 `input_audio_transcription.model` 参数时返回。

      <Expandable title="properties">
        <ParamField body="model" type="string">
          语音识别模型。
        </ParamField>

        <ParamField body="language" type="string">
          设置的语音识别语种。
        </ParamField>
      </Expandable>
    </ParamField>

    <ParamField body="turn_detection" type="object">
      VAD（语音活动检测）配置。Manual 模式下（客户端在 `session.update` 中将该参数设为 `null`）不返回此字段。

      <Expandable title="properties">
        <ParamField body="type" type="string">
          VAD 类型，固定为 `server_vad`。
        </ParamField>

        <ParamField body="threshold" type="float">
          VAD 检测灵敏度。
        </ParamField>

        <ParamField body="prefix_padding_ms" type="integer">
          语音开始前保留的音频时长（毫秒），避免丢失语音起始部分。
        </ParamField>

        <ParamField body="silence_duration_ms" type="integer">
          语音结束后需保持静音的最短时长（毫秒），超过该时长即判定语音结束。
        </ParamField>

        <ParamField body="create_response" type="boolean">
          VAD 检测到语音结束后，是否自动触发翻译响应。
        </ParamField>

        <ParamField body="interrupt_response" type="boolean">
          VAD 检测到新一轮语音开始时，是否打断当前正在生成的翻译响应。
        </ParamField>
      </Expandable>
    </ParamField>

    <ParamField body="translation" type="object">
      翻译设置。

      <Expandable title="properties">
        <ParamField body="language" type="string">
          目标语言。
        </ParamField>

        <ParamField body="corpus" type="object">
          热词配置，用于提升特定词汇的翻译准确性。

          <Expandable title="properties">
            <ParamField body="phrases" type="object">
              热词映射表。key 为源语言词汇，value 为目标语言对应翻译。
            </ParamField>
          </Expandable>
        </ParamField>
      </Expandable>
    </ParamField>

    <ParamField body="enable_voice_clone" type="boolean">
      是否启用声音复刻。
    </ParamField>

    <ParamField body="voice_clone_options" type="object">
      声音复刻控制参数，仅在 `enable_voice_clone` 为 `true` 时返回。

      <Expandable title="properties">
        <ParamField body="frequency" type="string">
          音色复刻频率。
        </ParamField>
      </Expandable>
    </ParamField>
  </Expandable>
</ParamField>

## session.updated

`session.update` 请求成功后发送。如果出错，服务端会返回 `error` 事件。

```json Example
{
  "event_id": "event_RmNPqjCeFFGRRXEusrCLA",
  "type": "session.updated",
  "session": {
    "id": "sess_OozZ1vtbPt2muDflHODIH",
    "object": "realtime.session",
    "model": "qwen3.5-livetranslate-flash-realtime",
    "modalities": [
      "text",
      "audio"
    ],
    "voice": "Ethan",
    "sample_rate": 16000,
    "input_audio_format": "pcm",
    "output_audio_format": "pcm",
    "translation": {
      "language": "en",
      "corpus": {
        "phrases": {
          "人工智能": "Artificial Intelligence",
          "机器学习": "Machine Learning"
        }
      }
    }
  }
}
```

<ParamField body="event_id" type="string">
  事件 ID。
</ParamField>

<ParamField body="type" type="string">
  固定为 `session.updated`。
</ParamField>

<ParamField body="session" type="object">
  会话配置。

  <Expandable title="properties">
    <ParamField body="id" type="string">
      会话 ID。
    </ParamField>

    <ParamField body="object" type="string">
      固定为 `realtime.session`。
    </ParamField>

    <ParamField body="model" type="string">
      使用的模型。
    </ParamField>

    <ParamField body="modalities" type="array">
      输出模态。
    </ParamField>

    <ParamField body="voice" type="string">
      音频输出的音色。
    </ParamField>

    <ParamField body="sample_rate" type="integer">
      输入音频的采样率。
    </ParamField>

    <ParamField body="input_audio_format" type="string">
      输入音频格式（固定为 `pcm`）。
    </ParamField>

    <ParamField body="output_audio_format" type="string">
      输出音频格式（固定为 `pcm`）。
    </ParamField>

    <ParamField body="translation" type="object">
      翻译设置。

      <Expandable title="properties">
        <ParamField body="language" type="string">
          目标语言。
        </ParamField>

        <ParamField body="corpus" type="object">
          热词配置，用于提升特定词汇的翻译准确性。

          <Expandable title="properties">
            <ParamField body="phrases" type="object">
              热词映射表。key 为源语言词汇，value 为目标语言对应翻译。
            </ParamField>
          </Expandable>
        </ParamField>
      </Expandable>
    </ParamField>
  </Expandable>
</ParamField>

## session.finished

所有翻译完成后发送。

仅在您发送 [session.finish](/api-reference/speech-translation/livetranslate-realtime/client-events#session-finish) 后触发。收到此事件后可以断开连接。

```json Example
{
  "event_id": "event_xxx",
  "type": "session.finished"
}
```

<ParamField body="event_id" type="string">
  事件 ID。
</ParamField>

<ParamField body="type" type="string">
  固定为 `session.finished`。
</ParamField>

## input\_audio\_buffer.speech\_started

服务端检测到音频流中出现语音活动时发送。

```json Example
{
  "event_id": "event_xxx",
  "type": "input_audio_buffer.speech_started",
  "audio_start_ms": 1200
}
```

<ParamField body="event_id" type="string">
  事件 ID。
</ParamField>

<ParamField body="type" type="string">
  固定为 `input_audio_buffer.speech_started`。
</ParamField>

<ParamField body="audio_start_ms" type="integer">
  检测到语音起始位置的时间偏移（毫秒）。
</ParamField>

## input\_audio\_buffer.speech\_stopped

服务端检测到语音片段结束时发送。

```json Example
{
  "event_id": "event_xxx",
  "type": "input_audio_buffer.speech_stopped",
  "audio_end_ms": 3400
}
```

<ParamField body="event_id" type="string">
  事件 ID。
</ParamField>

<ParamField body="type" type="string">
  固定为 `input_audio_buffer.speech_stopped`。
</ParamField>

<ParamField body="audio_end_ms" type="integer">
  检测到语音结束位置的时间偏移（毫秒）。
</ParamField>

## input\_audio\_buffer.committed

Manual 模式（`turn_detection` 为 `null`）下，客户端发送 `input_audio_buffer.commit` 事件后，服务端返回此事件进行确认，并自动开始生成翻译响应。

```json Example
{
  "event_id": "event_xxx",
  "type": "input_audio_buffer.committed"
}
```

<ParamField body="event_id" type="string">
  本次事件唯一标识符。
</ParamField>

<ParamField body="type" type="string">
  固定为 `input_audio_buffer.committed`。
</ParamField>

## input\_audio\_buffer.cleared

客户端发送 `input_audio_buffer.clear` 事件后，服务端返回此事件进行确认，表示已清空缓冲区中尚未提交的音频数据。

```json Example
{
  "event_id": "event_xxx",
  "type": "input_audio_buffer.cleared"
}
```

<ParamField body="event_id" type="string">
  本次事件唯一标识符。
</ParamField>

<ParamField body="type" type="string">
  固定为 `input_audio_buffer.cleared`。
</ParamField>

## conversation.item.created

当对话中创建新的消息项时，服务端返回此事件。以下场景会触发此事件：

- 服务端开始生成翻译响应时，创建对应的 assistant 消息项（此时 `content` 为空数组，内容随流式响应逐步填充）。
- Manual 模式下，客户端发送 `input_audio_buffer.commit` 事件后，服务端会额外创建一个对应用户输入音频的消息项（`content` 中包含 `{"type": "input_audio"}`）。

对于同一个 VAD 片段，服务端会分别创建语音识别结果和翻译结果消息项。语音识别结果消息项的 `item.id` 与翻译结果事件的 `previous_item_id` 相同。客户端可据此关联原文和译文，并同时展示。

```json Example
{
  "event_id": "event_xxx",
  "type": "conversation.item.created",
  "previous_item_id": "item_asr_xxx",
  "item": {
    "id": "item_translation_xxx",
    "object": "realtime.item",
    "type": "message",
    "status": "in_progress",
    "role": "assistant",
    "content": []
  }
}
```

<ParamField body="event_id" type="string">
  本次事件唯一标识符。
</ParamField>

<ParamField body="type" type="string">
  固定为 `conversation.item.created`。
</ParamField>

<ParamField body="previous_item_id" type="string">
  前一消息项的唯一标识符。对于翻译结果事件，该值与同一 VAD 片段的语音识别结果消息项 `item.id` 相同。
</ParamField>

<ParamField body="item" type="object">
  消息项信息。

  <Expandable title="properties">
    <ParamField body="id" type="string">
      消息项的唯一标识符。
    </ParamField>

    <ParamField body="object" type="string">
      固定为 `realtime.item`。
    </ParamField>

    <ParamField body="type" type="string">
      固定为 `message`。
    </ParamField>

    <ParamField body="status" type="string">
      消息项的状态。
    </ParamField>

    <ParamField body="role" type="string">
      消息的角色，取值为 `assistant` 或 `user`。
    </ParamField>

    <ParamField body="content" type="array">
      消息的内容。响应刚创建时为空数组，随流式响应逐步填充；Manual 模式下 commit 产生的用户消息项中包含 `{"type": "input_audio"}`。
    </ParamField>
  </Expandable>
</ParamField>

## response.created

服务端开始生成新响应时发送。

```json Example
{
  "event_id": "event_L8hHVI5jYis6BzAjnPWJh",
  "type": "response.created",
  "response": {
    "id": "resp_P79OOMs8LnrXVpiIHUCKR",
    "object": "realtime.response",
    "conversation_id": "conv_UFClXtYkRkFXrs48y8pmK",
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
  事件 ID。
</ParamField>

<ParamField body="type" type="string">
  固定为 `response.created`。
</ParamField>

<ParamField body="response" type="object">
  响应对象。

  <Expandable title="properties">
    <ParamField body="id" type="string">
      响应 ID。
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
      音频输出的音色。
    </ParamField>

    <ParamField body="output_audio_format" type="string">
      输出音频格式（固定为 `pcm`）。
    </ParamField>

    <ParamField body="output" type="array">
      当前为空。
    </ParamField>
  </Expandable>
</ParamField>

## response.done

响应生成完成时发送。`response` 对象包含所有输出项，但不包含原始音频数据。

```json Example
{
  "event_id": "event_CNea8oXNipVanSg2VIzkO",
  "type": "response.done",
  "response": {
    "id": "resp_TfhYTqej692vsGA2jNEtH",
    "object": "realtime.response",
    "conversation_id": "conv_ZtyLfKVm8XqLwYRlsuDih",
    "status": "completed",
    "modalities": [
      "text",
      "audio"
    ],
    "voice": "Cherry",
    "output_audio_format": "pcm",
    "output": [
      {
        "id": "item_MKtkMwN9RtcyE9eJShyWy",
        "object": "realtime.item",
        "type": "message",
        "status": "completed",
        "role": "assistant",
        "content": [
          {
            "type": "audio",
            "transcript": "Hello? "
          }
        ]
      }
    ],
    "usage": {
      "total_tokens": 56,
      "input_tokens": 47,
      "output_tokens": 9,
      "input_tokens_details": {
        "text_tokens": 20,
        "audio_tokens": 27
      },
      "output_tokens_details": {
        "text_tokens": 2,
        "audio_tokens": 7
      }
    }
  }
}
```

<ParamField body="event_id" type="string">
  事件 ID。
</ParamField>

<ParamField body="type" type="string">
  固定为 `response.done`。
</ParamField>

<ParamField body="response" type="object">
  响应对象。

  <Expandable title="properties">
    <ParamField body="id" type="string">
      响应 ID。
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
      音频输出的音色。
    </ParamField>

    <ParamField body="output_audio_format" type="string">
      输出音频格式（固定为 `pcm`）。
    </ParamField>

    <ParamField body="output" type="array">
      响应输出。

      <Expandable title="properties">
        <ParamField body="id" type="string">
          输出项 ID。
        </ParamField>

        <ParamField body="type" type="string">
          固定为 `message`。
        </ParamField>

        <ParamField body="object" type="string">
          固定为 `realtime.item`。
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
              内容类型：`text` 表示纯文本，`audio` 表示输出包含音频。
            </ParamField>

            <ParamField body="text" type="string">
              文本输出。
            </ParamField>

            <ParamField body="transcript" type="string">
              音频转写文本。
            </ParamField>
          </Expandable>
        </ParamField>
      </Expandable>
    </ParamField>

    <ParamField body="usage" type="object">
      该响应的 Token 用量。
    </ParamField>
  </Expandable>
</ParamField>

## response.text.text

纯文本模式下，模型增量生成文本时发送。

```json Example
{
  "event_id": "event_B1lIeyOXR7qJMEExbqtTG",
  "type": "response.text.text",
  "response_id": "resp_B1lIdtjF4Noqpn5NOjznj",
  "item_id": "item_B1lIdJsAJlJiFs8ztWpJt",
  "output_index": 0,
  "content_index": 0,
  "text": "How are"
}
```

<ParamField body="event_id" type="string">
  事件 ID。
</ParamField>

<ParamField body="type" type="string">
  固定为 `response.text.text`。
</ParamField>

<ParamField body="text" type="string">
  增量文本片段。
</ParamField>

<ParamField body="response_id" type="string">
  响应 ID。
</ParamField>

<ParamField body="item_id" type="string">
  消息项 ID。
</ParamField>

<ParamField body="output_index" type="integer">
  固定为 0。
</ParamField>

<ParamField body="content_index" type="integer">
  固定为 0。
</ParamField>

## response.text.done

纯文本输出完成时发送。

<Note>
  响应被中断、未完成或取消时也会发送此事件。
</Note>

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
  事件 ID。
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
  固定为 0。
</ParamField>

<ParamField body="content_index" type="integer">
  固定为 0。
</ParamField>

<ParamField body="text" type="string">
  完整文本输出。
</ParamField>

## response.audio.delta

模型增量生成音频数据时发送。

```json Example
{
  "event_id": "event_B1osWMZBtrEQbiIwW0qHQ",
  "type": "response.audio.delta",
  "response_id": "resp_P79OOMs8LnrXVpiIHUCKR",
  "item_id": "item_OFaPGtzfWCPyGzxnuEX9i",
  "output_index": 0,
  "content_index": 0,
  "delta": "UklGRnoGAABXQVZFZm10IBAAAAAB..."
}
```

<ParamField body="event_id" type="string">
  事件 ID。
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
  固定为 0。
</ParamField>

<ParamField body="content_index" type="integer">
  固定为 0。
</ParamField>

<ParamField body="delta" type="string">
  Base64 编码的音频数据片段。
</ParamField>

## response.audio.done

音频生成完成时发送。

<Note>
  响应被中断、未完成或取消时也会发送此事件。此事件不包含完整音频数据。
</Note>

```json Example
{
  "event_id": "event_B1osWMWoDRYyITDyNYcBu",
  "type": "response.audio.done",
  "response_id": "resp_P79OOMs8LnrXVpiIHUCKR",
  "item_id": "item_OFaPGtzfWCPyGzxnuEX9i",
  "output_index": 0,
  "content_index": 0
}
```

<ParamField body="event_id" type="string">
  事件 ID。
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
  固定为 0。
</ParamField>

<ParamField body="content_index" type="integer">
  固定为 0。
</ParamField>

## conversation.item.input\_audio\_transcription.text

流式返回源语言的语音识别结果。需要设置 `input_audio_transcription.model`。

```json Example
{
  "event_id": "event_xxx",
  "type": "conversation.item.input_audio_transcription.text",
  "item_id": "item_xxx",
  "content_index": 0,
  "text": "",
  "stash": "The weather is really nice today",
  "language": "en",
  "emotion": "neutral"
}
```

<ParamField body="event_id" type="string">
  事件 ID。
</ParamField>

<ParamField body="type" type="string">
  固定为 `conversation.item.input_audio_transcription.text`。
</ParamField>

<ParamField body="item_id" type="string">
  消息项 ID。
</ParamField>

<ParamField body="content_index" type="integer">
  固定为 0。
</ParamField>

<ParamField body="text" type="string">
  已确认的识别文本。
</ParamField>

<ParamField body="stash" type="string">
  待确认的识别文本，可能被后续事件修正。
</ParamField>

<ParamField body="language" type="string">
  检测到的源语言。
</ParamField>

<ParamField body="emotion" type="string">
  被识别音频的情感。支持的情感如下：

  - `surprised`：惊讶
  - `neutral`：平静
  - `happy`：愉快
  - `sad`：悲伤
  - `disgusted`：厌恶
  - `angry`：愤怒
  - `fearful`：恐惧
</ParamField>

## conversation.item.input\_audio\_transcription.completed

语音识别完成时发送，包含最终识别结果。需要设置 `input_audio_transcription.model`。

```json Example
{
  "event_id": "event_xxx",
  "type": "conversation.item.input_audio_transcription.completed",
  "item_id": "item_xxx",
  "content_index": 0,
  "transcript": "The weather is really nice today, let's go for a walk in the park.",
  "language": "en",
  "emotion": ""
}
```

<ParamField body="event_id" type="string">
  事件 ID。
</ParamField>

<ParamField body="type" type="string">
  固定为 `conversation.item.input_audio_transcription.completed`。
</ParamField>

<ParamField body="item_id" type="string">
  消息项 ID。
</ParamField>

<ParamField body="content_index" type="integer">
  固定为 0。
</ParamField>

<ParamField body="transcript" type="string">
  源语言的最终识别结果。
</ParamField>

<ParamField body="language" type="string">
  检测到的源语言。
</ParamField>

<ParamField body="emotion" type="string">
  被识别音频的情感。支持的情感如下：

  - `surprised`：惊讶
  - `neutral`：平静
  - `happy`：愉快
  - `sad`：悲伤
  - `disgusted`：厌恶
  - `angry`：愤怒
  - `fearful`：恐惧
</ParamField>

## conversation.item.input\_audio\_transcription.failed

当输入了音频但识别失败时，服务端发送该事件。与其他 `error` 事件分开处理，便于客户端识别相关的具体项目。

```json Example
{
  "event_id": "event_xxx",
  "type": "conversation.item.input_audio_transcription.failed",
  "item_id": "item_xxx",
  "content_index": 0,
  "error": {
    "code": "xxx",
    "message": "xxx",
    "param": "xxx"
  }
}
```

<ParamField body="event_id" type="string">
  本次事件唯一标识符。
</ParamField>

<ParamField body="type" type="string">
  固定为 `conversation.item.input_audio_transcription.failed`。
</ParamField>

<ParamField body="item_id" type="string">
  关联的对话项 ID。
</ParamField>

<ParamField body="content_index" type="integer">
  包含音频的内容部分的索引。
</ParamField>

<ParamField body="error.code" type="string">
  错误代码。
</ParamField>

<ParamField body="error.message" type="string">
  错误消息。
</ParamField>

## response.audio\_transcript.text

输出包含音频时，实时流式返回翻译文本。

```json Example
{
  "event_id": "event_xxx",
  "type": "response.audio_transcript.text",
  "response_id": "resp_xxx",
  "item_id": "item_xxx",
  "output_index": 0,
  "content_index": 0,
  "text": "Hello,",
  "stash": " who are you?"
}
```

<ParamField body="event_id" type="string">
  事件 ID。
</ParamField>

<ParamField body="type" type="string">
  固定为 `response.audio_transcript.text`。
</ParamField>

<ParamField body="response_id" type="string">
  响应 ID。
</ParamField>

<ParamField body="item_id" type="string">
  消息项 ID。
</ParamField>

<ParamField body="output_index" type="integer">
  固定为 0。
</ParamField>

<ParamField body="content_index" type="integer">
  固定为 0。
</ParamField>

<ParamField body="text" type="string">
  已确认的翻译片段。
</ParamField>

<ParamField body="stash" type="string">
  追加在 `text` 之后的临时文本，构成部分翻译结果。服务端通过 `response.audio_transcript.text` 事件持续更新 `text` 和 `stash`，直到 [response.audio\_transcript.done](#response-audio-transcript-done) 事件返回最终翻译结果（`transcript` 字段）。
</ParamField>

## response.audio\_transcript.done

音频输出的翻译文本生成完成时发送。

```json Example
{
  "event_id": "event_VN4Q4GJugLcc1S23viW8E",
  "type": "response.audio_transcript.done",
  "response_id": "resp_P79OOMs8LnrXVpiIHUCKR",
  "item_id": "item_JvJauNH2CTXb1D9WV6pD4",
  "output_index": 0,
  "content_index": 0,
  "transcript": "How can I assist you today?"
}
```

<ParamField body="event_id" type="string">
  事件 ID。
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
  固定为 0。
</ParamField>

<ParamField body="content_index" type="integer">
  固定为 0。
</ParamField>

<ParamField body="transcript" type="string">
  最终翻译文本。
</ParamField>

## response.output\_item.added

响应生成过程中创建新输出项时发送。

```json Example
{
  "event_id": "event_B4O5yPt3Gjnjy5eYH3plG",
  "type": "response.output_item.added",
  "response_id": "resp_P79OOMs8LnrXVpiIHUCKR",
  "output_index": 0,
  "item": {
    "id": "item_OFaPGtzfWCPyGzxnuEX9i",
    "object": "realtime.item",
    "type": "message",
    "status": "in_progress",
    "role": "assistant",
    "content": []
  }
}
```

<ParamField body="event_id" type="string">
  事件 ID。
</ParamField>

<ParamField body="type" type="string">
  固定为 `response.output_item.added`。
</ParamField>

<ParamField body="response_id" type="string">
  响应 ID。
</ParamField>

<ParamField body="output_index" type="integer">
  固定为 0。
</ParamField>

<ParamField body="item" type="object">
  输出项。

  <Expandable title="properties">
    <ParamField body="id" type="string">
      输出项 ID。
    </ParamField>

    <ParamField body="type" type="string">
      固定为 `message`。
    </ParamField>

    <ParamField body="object" type="string">
      固定为 `realtime.item`。
    </ParamField>

    <ParamField body="status" type="string">
      输出项状态。
    </ParamField>

    <ParamField body="role" type="string">
      消息角色。
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
  "event_id": "event_XkiwbYTBC9Wcdwy6uYJ2G",
  "type": "response.output_item.done",
  "response_id": "resp_P79OOMs8LnrXVpiIHUCKR",
  "output_index": 0,
  "item": {
    "id": "item_JvJauNH2CTXb1D9WV6pD4",
    "object": "realtime.item",
    "type": "message",
    "status": "completed",
    "role": "assistant",
    "content": [
      {
        "type": "audio",
        "text": "Hello, I am a large language model developed by Alibaba Cloud. My name is Qwen. How can I help you?"
      }
    ]
  }
}
```

<ParamField body="event_id" type="string">
  事件 ID。
</ParamField>

<ParamField body="type" type="string">
  固定为 `response.output_item.done`。
</ParamField>

<ParamField body="response_id" type="string">
  响应 ID。
</ParamField>

<ParamField body="output_index" type="integer">
  固定为 0。
</ParamField>

<ParamField body="item" type="object">
  输出项。

  <Expandable title="properties">
    <ParamField body="id" type="string">
      输出项 ID。
    </ParamField>

    <ParamField body="object" type="string">
      固定为 `realtime.item`。
    </ParamField>

    <ParamField body="type" type="string">
      固定为 `message`。
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

新的内容部分开始时发送。

```json Example
{
  "event_id": "event_J2UixwYKZsXg7c9YXZetL",
  "type": "response.content_part.added",
  "response_id": "resp_P79OOMs8LnrXVpiIHUCKR",
  "item_id": "item_OFaPGtzfWCPyGzxnuEX9i",
  "output_index": 0,
  "content_index": 0,
  "part": {
    "type": "audio",
    "text": ""
  }
}
```

<ParamField body="event_id" type="string">
  事件 ID。
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
  固定为 0。
</ParamField>

<ParamField body="content_index" type="integer">
  固定为 0。
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

内容部分完成时发送。

```json Example
{
  "event_id": "event_VN4Q4GJugLcc1S23viW8E",
  "type": "response.content_part.done",
  "response_id": "resp_P79OOMs8LnrXVpiIHUCKR",
  "item_id": "item_JvJauNH2CTXb1D9WV6pD4",
  "output_index": 0,
  "content_index": 0,
  "part": {
    "type": "audio",
    "text": "Hello, I am a large language model developed by Alibaba Cloud. My name is Qwen. How can I help you?"
  }
}
```

<ParamField body="event_id" type="string">
  事件 ID。
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
  固定为 0。
</ParamField>

<ParamField body="content_index" type="integer">
  固定为 0。
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
