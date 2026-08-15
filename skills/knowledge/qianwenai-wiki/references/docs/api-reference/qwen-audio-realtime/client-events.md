> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Qwen-Audio-Realtime 客户端事件

> Qwen-Audio-Realtime API 客户端事件参考

客户端事件由客户端发送到服务端，用于配置会话、发送音频、管理对话和控制推理。

**用户指南**：[实时语音对话（Qwen-Audio-Realtime）](/developer-guides/speech/qwen-audio-realtime)。如需了解事件交互时序，请参见 [WebSocket API](/api-reference/qwen-audio-realtime/websocket-api)。

## session.update

建立连接后，发送此事件更新会话的默认配置。仅包含需要变更的字段，未传字段保持原值。服务端收到后校验参数，若参数不合法则返回错误，若参数合法则应用更改并返回完整配置。

<Note>
  `turn_detection` 仅在首次发送音频之前（IDLE 状态）允许修改。
</Note>

| 字段                                              | 类型           | 必选/可选 | 描述                                                                                                                                                                                       |
| ----------------------------------------------- | ------------ | ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| type                                            | string       | 必选    | 事件类型，固定为 `session.update`。                                                                                                                                                               |
| session                                         | object       | 可选    | 会话配置。                                                                                                                                                                                    |
| session.modalities                              | array        | 可选    | 模型输出模态设置。可选值：`["text"]`（仅输出文本）；`["audio", "text"]`（默认值，同时输出文本和音频）。                                                                                                                       |
| session.voice                                   | string       | 可选    | TTS 音色名称，默认值为 `longanqian`。仅可在第一次 `session.update` 中设置，后续传入将被忽略。支持系统音色（`longanqian`、`longanlingxin`、`longanlingxi`、`longanxiaoxin`、`longanlufeng`）和声音复刻音色（通过声音复刻 API 创建的 `voice_id`）。    |
| session.enable\_speech\_emotion                 | boolean      | 可选    | 是否开启情绪增强功能。开启后，回复音色的情绪变化更明显。默认值为 `true`。可选值：`true`、`false`。                                                                                                                              |
| session.instructions                            | string       | 可选    | 系统指令，用于设定模型的角色身份、回答风格和行为偏好。对整个会话生效。                                                                                                                                                      |
| session.input\_audio\_format                    | string       | 可选    | 输入音频格式。当前仅支持 `pcm`（16kHz 16bit 单声道），为默认值。仅在首次发送音频之前（IDLE 状态）允许修改。                                                                                                                        |
| session.output\_audio\_format                   | string       | 可选    | 输出音频格式。当前仅支持 `pcm`（24kHz 16bit 单声道），为默认值。                                                                                                                                                |
| session.max\_history\_turns                     | integer      | 可选    | 允许单次请求的最大历史 QA 轮数。取值范围为 1-50，默认值为 20。                                                                                                                                                    |
| session.tools                                   | array        | 可选    | Function Calling 工具定义列表。配置后模型可根据用户输入自主决定是否调用工具。每个工具包含 `type`（固定为 `function`）、`function.name`（必选）、`function.description`（可选）、`function.parameters`（可选，包含 `type`、`properties`、`required`）。 |
| session.turn\_detection                         | object\      | null  | 可选                                                                                                                                                                                       | 轮次检测配置。设为 `null` 可切换为 push-to-talk 模式（手动提交音频并触发推理）。若不提供此字段，系统将使用默认参数启用 VAD。 |
| session.turn\_detection.type                    | string       | 可选    | VAD 类型。`server_vad`（默认值）：基于声学特征检测语音起止，自动触发推理。`smart_turn`：融合声学感知与语义理解的智能轮次检测，无语义的声音（如"嗯"、"啊"）不会触发对话轮或打断模型播报。                                                                             |
| session.turn\_detection.threshold               | float        | 可选    | VAD 灵敏度，仅在 server\_vad 模式下生效（smart\_turn 模式下无效）。值越低越灵敏。取值范围为 \[-1.0, 1.0]，默认值为 0.5。                                                                                                      |
| session.turn\_detection.silence\_duration\_ms   | integer      | 可选    | 语音结束后需保持静音的最短时间（毫秒），仅在 server\_vad 模式下生效（smart\_turn 模式下无效）。超时即触发模型响应。取值范围为 \[200, 6000]，默认值为 800。对话场景推荐 400-800。                                                                        |
| session.turn\_detection.voiceprint\_audio\_urls | array        | 可选    | 仅在 smart\_turn 模式下生效。目标用户预录音频的公网可访问 URL 列表，用于说话人增强。最多支持 5 个 URL。音频格式要求：16kHz PCM 或 WAV。仅在第一次发送 `session.update` 事件时可配置，后续传入该字段将被忽略。                                                      |

基本配置示例：

```json
{
    "type": "session.update",
    "session": {
        "modalities": [
            "text",
            "audio"
        ],
        "voice": "longanqian",
        "turn_detection": {
            "type": "server_vad",
            "threshold": 0.5,
            "silence_duration_ms": 800
        }
    }
}
```

Function Calling 示例：

```json
{
    "type": "session.update",
    "session": {
        "modalities": [
            "text",
            "audio"
        ],
        "voice": "longanqian",
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "查询指定城市天气",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "title": "城市"
                            }
                        },
                        "required": ["city"]
                    }
                }
            }
        ],
        "turn_detection": {
            "type": "server_vad",
            "threshold": 0.5,
            "silence_duration_ms": 800
        }
    }
}
```

声纹注册（voiceprint\_audio\_urls）示例：

```json
{
    "type": "session.update",
    "session": {
        "turn_detection": {
            "type": "smart_turn",
            "voiceprint_audio_urls": [
                "https://example.com/speaker1.pcm",
                "https://example.com/speaker2.wav"
            ]
        }
    }
}
```

## input\_audio\_buffer.append

追加音频数据到输入缓冲区。应持续、高频发送（如每 20\~40 ms 一帧）。此事件无服务端确认回包。

| 字段    | 类型     | 必选/可选 | 描述                                    |
| ----- | ------ | ----- | ------------------------------------- |
| type  | string | 必选    | 事件类型，固定为 `input_audio_buffer.append`。 |
| audio | string | 必选    | Base64 编码的音频数据。                       |

```json
{
    "type": "input_audio_buffer.append",
    "audio": "<base64 编码的音频数据>"
}
```

## input\_audio\_buffer.commit

**仅 push-to-talk 模式。** 将缓冲区音频提交为一条用户消息。提交后不会自动触发推理，需要发送 `response.create` 手动触发。

server\_vad / smart\_turn 模式下此事件被忽略。

| 字段   | 类型     | 必选/可选 | 描述                                    |
| ---- | ------ | ----- | ------------------------------------- |
| type | string | 必选    | 事件类型，固定为 `input_audio_buffer.commit`。 |

```json
{
    "type": "input_audio_buffer.commit"
}
```

## input\_audio\_buffer.clear

**仅 push-to-talk 模式。** 清空缓冲区中尚未提交的音频。server\_vad / smart\_turn 模式下此事件被忽略。服务端以 `input_audio_buffer.cleared` 事件响应。

| 字段   | 类型     | 必选/可选 | 描述                                   |
| ---- | ------ | ----- | ------------------------------------ |
| type | string | 必选    | 事件类型，固定为 `input_audio_buffer.clear`。 |

```json
{
    "type": "input_audio_buffer.clear"
}
```

## conversation.item.create

手动向对话上下文插入一条对话项。可用于注入历史上下文、补充文本信息，或写回 Function Calling 的工具执行结果。

<Note>
  若 `item.id` 已存在于对话中，会返回错误并拒绝创建。
</Note>

| 字段                 | 类型     | 必选/可选                                       | 描述                                                                                                                                                                                  |
| ------------------ | ------ | ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| type               | string | 必选                                          | 事件类型，固定为 `conversation.item.create`。                                                                                                                                                |
| previous\_item\_id | string | 可选                                          | 指定新项插入到哪条对话项之后。不传时追加到对话末尾。                                                                                                                                                          |
| item               | object | 必选                                          | 要创建的对话项。                                                                                                                                                                            |
| item.id            | string | 可选                                          | 对话项的唯一标识符。不传时由服务端自动生成。若指定的 ID 已存在于对话中，会返回错误。                                                                                                                                        |
| item.type          | string | 必选                                          | 对话项类型。`message`：普通对话消息；`function_call`：函数调用请求（通常由服务端生成，客户端也可用于补充历史上下文）；`function_call_output`：工具执行结果（客户端收到 `function_call` 后执行工具，并用该类型写回结果）。                                        |
| item.role          | string | `message` 类型必选                              | 消息角色，可选值：`system`、`user`、`assistant`。                                                                                                                                               |
| item.content       | array  | `message` 类型必选                              | 消息内容列表。每个元素包含 `type` 和对应的数据字段。system 支持 `input_text`（必填字段 `text`）；user 支持 `input_text`（必填字段 `text`）和 `input_audio`（必填字段 `audio`，Base64 编码）；assistant 支持 `output_text`（必填字段 `text`）。 |
| item.call\_id      | string | `function_call`/`function_call_output` 类型必选 | 函数调用的唯一标识符，用于关联请求和结果。                                                                                                                                                               |
| item.name          | string | `function_call` 类型必选                        | 要调用的函数名称。                                                                                                                                                                           |
| item.arguments     | string | `function_call` 类型必选                        | 函数调用参数，JSON 字符串格式。                                                                                                                                                                  |
| item.output        | string | `function_call_output` 类型必选                 | 工具执行结果，JSON 字符串格式。                                                                                                                                                                  |

注入用户文本消息：

```json
{
    "type": "conversation.item.create",
    "previous_item_id": "item_xxx",
    "item": {
        "id": "my_item_001",
        "type": "message",
        "role": "user",
        "content": [
            {
                "type": "input_text",
                "text": "请帮我总结一下上次的对话"
            }
        ]
    }
}
```

写回 Function Calling 结果：

```json
{
    "type": "conversation.item.create",
    "item": {
        "type": "function_call_output",
        "call_id": "call_xxx",
        "output": "{\"temperature\":18,\"condition\":\"晴\"}"
    }
}
```

## conversation.item.retrieve

查询服务端存储的某条对话项。返回的音频类型 content 仅包含转写文本（`transcript`），不包含原始音频数据。

| 字段       | 类型     | 必选/可选 | 描述                                                      |
| -------- | ------ | ----- | ------------------------------------------------------- |
| type     | string | 必选    | 事件类型，固定为 `conversation.item.retrieve`。                  |
| item\_id | string | 必选    | 要查询的对话项 ID。服务端以 `conversation.item.retrieved` 事件返回查询结果。 |

```json
{
    "type": "conversation.item.retrieve",
    "item_id": "item_xxx"
}
```

## conversation.item.delete

从对话上下文中删除指定对话项。服务端以 `conversation.item.deleted` 事件确认。

| 字段       | 类型     | 必选/可选 | 描述                                   |
| -------- | ------ | ----- | ------------------------------------ |
| type     | string | 必选    | 事件类型，固定为 `conversation.item.delete`。 |
| item\_id | string | 必选    | 要删除的对话项 ID。                          |

```json
{
    "type": "conversation.item.delete",
    "item_id": "item_xxx"
}
```

## response.create

显式触发一次模型推理。各模式下的行为如下：

- **push-to-talk 模式**：必须手动调用，需先通过 `input_audio_buffer.commit` 提交缓冲区音频或写入 `function_call_output` 后触发。当前有响应正在生成时不允许重复触发。
- **server\_vad 模式**：通常由服务端自动触发。当前无响应正在生成时，客户端也允许手动调用；有响应正在生成时不允许重复触发。
- **smart\_turn 模式**：等待用户下一轮输入时允许调用。当前处于一个 turn 内时（收到 `input_audio_buffer.speech_started` 到 `response.done` 期间）不允许重复触发。

`response` 字段可选，用于覆盖本轮推理的会话默认配置。Function Calling 场景下，客户端写入 `function_call_output` 后也通过该事件触发二轮推理。

<Note>
  server\_vad / smart\_turn 模式下，手动触发的推理仍可能被新语音打断。
</Note>

| 字段                  | 类型     | 必选/可选 | 描述                                                    |
| ------------------- | ------ | ----- | ----------------------------------------------------- |
| type                | string | 必选    | 事件类型，固定为 `response.create`。                           |
| response            | object | 可选    | 用于覆盖本轮推理的会话默认配置。不传时使用当前会话配置。                          |
| response.modalities | array  | 可选    | 覆盖本轮的输出模态设置。可选值与 `session.update` 中的 `modalities` 一致。 |
| response.voice      | string | 可选    | 覆盖本轮的 TTS 音色。                                         |

```json
{
    "type": "response.create",
    "response": {
        "modalities": ["audio", "text"]
    }
}
```

## response.cancel

取消当前正在进行的推理。已输出的部分文本会写入 item 链表，服务端返回 `status=cancelled` 的 `response.done`。

若当前无进行中的推理，返回错误。

| 字段   | 类型     | 必选/可选 | 描述                          |
| ---- | ------ | ----- | --------------------------- |
| type | string | 必选    | 事件类型，固定为 `response.cancel`。 |

```json
{
    "type": "response.cancel"
}
```
