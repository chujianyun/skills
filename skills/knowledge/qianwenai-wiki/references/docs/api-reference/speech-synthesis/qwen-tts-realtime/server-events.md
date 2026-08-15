> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Qwen-TTS server events

> WebSocket 服务端事件参考

服务端通过 WebSocket 连接发送以下事件。

<Note>参考：[实时流式语音合成](/developer-guides/speech/realtime-streaming)。</Note>

## error

客户端或服务端发生错误时发送。

```json Example
{
  "event_id": "event_QzAVZRVa9hKqM5VOaHunh",
  "type": "error",
  "error": {
    "code": "invalid_value",
    "message": "Session update error: session already started or finished or failed."
  }
}
```

<ParamField body="event_id" type="string">
  事件 ID。
</ParamField>

<ParamField body="type" type="string">
  固定值 `error`。
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
  </Expandable>
</ParamField>

## session.created

客户端连接后立即发送，包含默认的会话配置。

```json Example
{
  "event_id": "event_xxx",
  "type": "session.created",
  "session": {
    "object": "realtime.session",
    "mode": "server_commit",
    "model": "qwen-tts-realtime",
    "voice": "Cherry",
    "response_format": "pcm",
    "sample_rate": 24000,
    "id": "sess_xxx"
  }
}
```

<ParamField body="event_id" type="string">
  事件 ID。
</ParamField>

<ParamField body="type" type="string">
  固定值 `session.created`。
</ParamField>

<ParamField body="session" type="object">
  会话配置。

  <Expandable title="properties">
    <ParamField body="id" type="string">
      会话 ID。
    </ParamField>

    <ParamField body="object" type="string">
      固定值 `realtime.session`。
    </ParamField>

    <ParamField body="mode" type="string">
      交互模式：`server_commit` 或 `commit`。
    </ParamField>

    <ParamField body="model" type="string">
      模型名称。
    </ParamField>

    <ParamField body="voice" type="string">
      音色名称。
    </ParamField>

    <ParamField body="response_format" type="string">
      音频格式。
    </ParamField>

    <ParamField body="sample_rate" type="integer">
      采样率，单位 Hz。
    </ParamField>
  </Expandable>
</ParamField>

## session.updated

服务端处理 `session.update` 请求后发送。如果处理失败，服务端会发送 `error` 事件。

```json Example
{
  "event_id": "event_xxx",
  "type": "session.updated",
  "session": {
    "id": "sess_xxx",
    "object": "realtime.session",
    "model": "qwen-tts-realtime",
    "voice": "Cherry",
    "language_type": "Chinese",
    "mode": "commit",
    "response_format": "pcm",
    "sample_rate": 24000
  }
}
```

<ParamField body="event_id" type="string">
  事件 ID。
</ParamField>

<ParamField body="type" type="string">
  固定值 `session.updated`。
</ParamField>

<ParamField body="session" type="object">
  会话配置。

  <Expandable title="properties">
    <ParamField body="id" type="string">
      会话 ID。
    </ParamField>

    <ParamField body="object" type="string">
      固定值 `realtime.session`。
    </ParamField>

    <ParamField body="mode" type="string">
      交互模式：`server_commit` 或 `commit`。
    </ParamField>

    <ParamField body="model" type="string">
      模型名称。
    </ParamField>

    <ParamField body="voice" type="string">
      音色名称。
    </ParamField>

    <ParamField body="response_format" type="string">
      音频格式。
    </ParamField>

    <ParamField body="sample_rate" type="integer">
      采样率，单位 Hz。
    </ParamField>

    <ParamField body="language_type" type="string">
      音频语言。
    </ParamField>
  </Expandable>
</ParamField>

## input\_text\_buffer.committed

服务端收到 `input_text_buffer.commit` 事件后发送。

```json Example
{
  "event_id": "event_FC6MA88wS2oEeXkPvWsxX",
  "type": "input_text_buffer.committed",
  "item_id": ""
}
```

<ParamField body="event_id" type="string">
  事件 ID。
</ParamField>

<ParamField body="type" type="string">
  固定值 `input_text_buffer.committed`。
</ParamField>

<ParamField body="item_id" type="string">
  待创建的用户消息项 ID。
</ParamField>

## input\_text\_buffer.cleared

服务端收到 `input_text_buffer.clear` 事件后发送。

```json Example
{
  "event_id": "event_1122",
  "type": "input_text_buffer.cleared"
}
```

<ParamField body="event_id" type="string">
  事件 ID。
</ParamField>

<ParamField body="type" type="string">
  固定值 `input_text_buffer.cleared`。
</ParamField>

## response.created

服务端收到 `input_text_buffer.commit` 事件后发送。

```json Example
{
  "event_id": "event_IMnLqDvG6Ahhk7sWV2uOs",
  "type": "response.created",
  "response": {
    "id": "resp_USvBwHktHcz76r6GaIJUV",
    "object": "realtime.response",
    "conversation_id": "",
    "status": "in_progress",
    "voice": "Cherry",
    "output": []
  }
}
```

<ParamField body="event_id" type="string">
  事件 ID。
</ParamField>

<ParamField body="type" type="string">
  固定值 `response.created`。
</ParamField>

<ParamField body="response" type="object">
  响应详情。

  <Expandable title="properties">
    <ParamField body="id" type="string">
      响应 ID。
    </ParamField>

    <ParamField body="object" type="string">
      固定值 `realtime.response`。
    </ParamField>

    <ParamField body="conversation_id" type="string">
      会话 ID。
    </ParamField>

    <ParamField body="status" type="string">
      响应状态：`completed`、`failed`、`in_progress` 或 `incomplete`。
    </ParamField>

    <ParamField body="voice" type="string">
      音色名称。
    </ParamField>

    <ParamField body="output" type="array">
      该事件中为空数组。
    </ParamField>
  </Expandable>
</ParamField>

## response.output\_item.added

新的输出项就绪时发送。

```json Example
{
  "event_id": "event_INDGnGNulaXCrStd9ZM5X",
  "type": "response.output_item.added",
  "response_id": "resp_USvBwHktHcz76r6GaIJUV",
  "output_index": 0,
  "item": {
    "id": "item_FIrYGaNVK3rbIZqeY4QjM",
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
  固定值 `response.output_item.added`。
</ParamField>

<ParamField body="response_id" type="string">
  响应 ID。
</ParamField>

<ParamField body="output_index" type="integer">
  响应输出项索引，固定值 `0`。
</ParamField>

<ParamField body="item" type="object">
  输出项详情。

  <Expandable title="properties">
    <ParamField body="id" type="string">
      输出项 ID。
    </ParamField>

    <ParamField body="object" type="string">
      固定值 `realtime.item`。
    </ParamField>

    <ParamField body="type" type="string">
      消息类型，固定值 `message`。
    </ParamField>

    <ParamField body="status" type="string">
      输出项状态。
    </ParamField>

    <ParamField body="role" type="string">
      消息角色，固定值 `assistant`。
    </ParamField>

    <ParamField body="content" type="array">
      消息内容。
    </ParamField>
  </Expandable>
</ParamField>

## response.content\_part.added

新的内容分片就绪时发送。

```json Example
{
  "event_id": "event_DigZ95MWN36YYyyjcENoq",
  "type": "response.content_part.added",
  "response_id": "resp_USvBwHktHcz76r6GaIJUV",
  "item_id": "item_FIrYGaNVK3rbIZqeY4QjM",
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
  固定值 `response.content_part.added`。
</ParamField>

<ParamField body="response_id" type="string">
  响应 ID。
</ParamField>

<ParamField body="item_id" type="string">
  消息项 ID。
</ParamField>

<ParamField body="output_index" type="integer">
  响应输出项索引，固定值 `0`。
</ParamField>

<ParamField body="content_index" type="integer">
  内容分片索引，固定值 `0`。
</ParamField>

<ParamField body="part" type="object">
  内容分片详情。

  <Expandable title="properties">
    <ParamField body="type" type="string">
      内容分片类型。
    </ParamField>

    <ParamField body="text" type="string">
      内容分片文本。
    </ParamField>
  </Expandable>
</ParamField>

## response.audio.delta

模型生成音频块时发送。

```json Example
{
  "event_id": "event_B1osWMZBtrEQbiIwW0qHQ",
  "type": "response.audio.delta",
  "response_id": "resp_B1osWTzBb8hO0WsELHgVP",
  "item_id": "item_B1osWH81fXDoyim1T5fsF",
  "output_index": 0,
  "content_index": 0,
  "delta": "base64 audio"
}
```

<ParamField body="event_id" type="string">
  事件 ID。
</ParamField>

<ParamField body="type" type="string">
  固定值 `response.audio.delta`。
</ParamField>

<ParamField body="response_id" type="string">
  响应 ID。
</ParamField>

<ParamField body="item_id" type="string">
  消息项 ID。
</ParamField>

<ParamField body="output_index" type="integer">
  响应输出项索引，固定值 `0`。
</ParamField>

<ParamField body="content_index" type="integer">
  内容分片索引，固定值 `0`。
</ParamField>

<ParamField body="delta" type="string">
  Base64 编码的音频数据块。
</ParamField>

## response.content\_part.done

内容分片完成时发送。

```json Example
{
  "event_id": "event_Vo2YUjlYQJ4colH8nVzkU",
  "type": "response.content_part.done",
  "response_id": "resp_USvBwHktHcz76r6GaIJUV",
  "item_id": "item_FIrYGaNVK3rbIZqeY4QjM",
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
  固定值 `response.content_part.done`。
</ParamField>

<ParamField body="response_id" type="string">
  响应 ID。
</ParamField>

<ParamField body="item_id" type="string">
  消息项 ID。
</ParamField>

<ParamField body="output_index" type="integer">
  响应输出项索引，固定值 `0`。
</ParamField>

<ParamField body="content_index" type="integer">
  内容分片索引，固定值 `0`。
</ParamField>

<ParamField body="part" type="object">
  已完成的内容分片。

  <Expandable title="properties">
    <ParamField body="type" type="string">
      内容分片类型。
    </ParamField>

    <ParamField body="text" type="string">
      内容分片文本。
    </ParamField>
  </Expandable>
</ParamField>

## response.output\_item.done

输出项完成时发送。

```json Example
{
  "event_id": "event_LO6SJRKIQ9NBayyYB8a1A",
  "type": "response.output_item.done",
  "response_id": "resp_USvBwHktHcz76r6GaIJUV",
  "output_index": 0,
  "item": {
    "id": "item_FIrYGaNVK3rbIZqeY4QjM",
    "object": "realtime.item",
    "type": "message",
    "status": "completed",
    "role": "assistant",
    "content": [
      {
        "type": "audio",
        "text": ""
      }
    ]
  }
}
```

<ParamField body="event_id" type="string">
  事件 ID。
</ParamField>

<ParamField body="type" type="string">
  固定值 `response.output_item.done`。
</ParamField>

<ParamField body="response_id" type="string">
  响应 ID。
</ParamField>

<ParamField body="output_index" type="integer">
  响应输出项索引，固定值 `0`。
</ParamField>

<ParamField body="item" type="object">
  输出项详情。

  <Expandable title="properties">
    <ParamField body="id" type="string">
      输出项 ID。
    </ParamField>

    <ParamField body="object" type="string">
      固定值 `realtime.item`。
    </ParamField>

    <ParamField body="type" type="string">
      消息类型，固定值 `message`。
    </ParamField>

    <ParamField body="status" type="string">
      输出项状态。
    </ParamField>

    <ParamField body="role" type="string">
      消息角色，固定值 `assistant`。
    </ParamField>

    <ParamField body="content" type="array">
      消息内容。
    </ParamField>
  </Expandable>
</ParamField>

## response.audio.done

音频生成完成时发送。

```json Example
{
  "event_id": "event_LZaOHPzXYMUXGBcVkBmKX",
  "type": "response.audio.done",
  "response_id": "resp_USvBwHktHcz76r6GaIJUV",
  "item_id": "item_FIrYGaNVK3rbIZqeY4QjM",
  "output_index": 0,
  "content_index": 0
}
```

<ParamField body="event_id" type="string">
  事件 ID。
</ParamField>

<ParamField body="type" type="string">
  固定值 `response.audio.done`。
</ParamField>

<ParamField body="response_id" type="string">
  响应 ID。
</ParamField>

<ParamField body="item_id" type="string">
  消息项 ID。
</ParamField>

<ParamField body="output_index" type="integer">
  响应输出项索引，固定值 `0`。
</ParamField>

<ParamField body="content_index" type="integer">
  内容分片索引，固定值 `0`。
</ParamField>

## response.done

响应生成完成时发送。`response` 对象包含所有输出项，但不包含已发送的原始音频数据。

<Tabs>
  <Tab title="Qwen3-TTS Realtime">
    ```json Example
    {
      "event_id": "event_Aemy83XqHFFDDSeJIDn6N",
      "type": "response.done",
      "response": {
        "id": "resp_LFeR42yXZ9SxUAeXjmyTz",
        "object": "realtime.response",
        "conversation_id": "",
        "status": "completed",
        "modalities": [
          "text",
          "audio"
        ],
        "voice": "Cherry",
        "output": [
          {
            "id": "item_Ae1lv2XmRljRSG96L8Zm1",
            "object": "realtime.item",
            "type": "message",
            "status": "completed",
            "role": "assistant",
            "content": [
              {
                "type": "audio",
                "transcript": ""
              }
            ]
          }
        ],
        "usage": {
          "characters": 25
        }
      }
    }
    ```
  </Tab>

  <Tab title="Qwen-TTS Realtime">
    ```json Example
    {
      "event_id": "event_xxx",
      "type": "response.done",
      "response": {
        "id": "resp_xxx",
        "object": "realtime.response",
        "conversation_id": "",
        "status": "completed",
        "modalities": [
          "text",
          "audio"
        ],
        "voice": "Cherry",
        "output": [
          {
            "id": "item_FIrYGaNVK3rbIZqeY4QjM",
            "object": "realtime.item",
            "type": "message",
            "status": "completed",
            "role": "assistant",
            "content": [
              {
                "type": "audio",
                "transcript": ""
              }
            ]
          }
        ],
        "usage": {
          "total_tokens": 67,
          "input_tokens": 3,
          "output_tokens": 64,
          "input_tokens_details": {
            "text_tokens": 3
          },
          "output_tokens_details": {
            "text_tokens": 0,
            "audio_tokens": 64
          }
        }
      }
    }
    ```
  </Tab>
</Tabs>

<ParamField body="event_id" type="string">
  事件 ID。
</ParamField>

<ParamField body="type" type="string">
  固定值 `response.done`。
</ParamField>

<ParamField body="response" type="object">
  响应详情。

  <Expandable title="properties">
    <ParamField body="id" type="string">
      响应 ID。
    </ParamField>

    <ParamField body="object" type="string">
      固定值 `realtime.response`。
    </ParamField>

    <ParamField body="conversation_id" type="string">
      会话 ID。
    </ParamField>

    <ParamField body="status" type="string">
      响应状态，`completed` 表示生成完成。
    </ParamField>

    <ParamField body="modalities" type="array">
      响应包含的模态列表，如 `["text", "audio"]`。
    </ParamField>

    <ParamField body="voice" type="string">
      音色名称。
    </ParamField>

    <ParamField body="output" type="array">
      响应输出。
    </ParamField>

    <ParamField body="usage" type="object">
      计费详情。

      <Expandable title="properties">
        <ParamField body="characters" type="integer">
          计费字符数（Qwen3-TTS Realtime）。
        </ParamField>

        <ParamField body="total_tokens" type="integer">
          输入和输出 token 总数（Qwen-TTS Realtime）。
        </ParamField>

        <ParamField body="input_tokens" type="integer">
          输入 token 数（Qwen-TTS Realtime）。
        </ParamField>

        <ParamField body="output_tokens" type="integer">
          输出 token 数（Qwen-TTS Realtime）。
        </ParamField>

        <ParamField body="input_tokens_details" type="object">
          输入 token 明细（Qwen-TTS Realtime）。

          <Expandable title="properties">
            <ParamField body="text_tokens" type="integer">
              输入文本 token 数。
            </ParamField>
          </Expandable>
        </ParamField>

        <ParamField body="output_tokens_details" type="object">
          输出 token 明细（Qwen-TTS Realtime）。

          <Expandable title="properties">
            <ParamField body="text_tokens" type="integer">
              输出文本 token 数。
            </ParamField>

            <ParamField body="audio_tokens" type="integer">
              输出音频 token 数。1 秒 = 50 个 token，不足 1 秒按 50 个 token 计算。
            </ParamField>
          </Expandable>
        </ParamField>
      </Expandable>
    </ParamField>
  </Expandable>
</ParamField>

## session.finished

所有响应生成完成时发送。

```json Example
{
  "event_id": "event_2239",
  "type": "session.finished"
}
```

<ParamField body="event_id" type="string">
  事件 ID。
</ParamField>

<ParamField body="type" type="string">
  固定值 `session.finished`。
</ParamField>
