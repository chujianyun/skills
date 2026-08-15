> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 实时语音识别（Fun-ASR）服务端事件

> Fun-ASR 实时语音识别 WebSocket 服务端事件参考

Fun-ASR 实时语音识别服务通过 WebSocket 向客户端发送四种服务端事件：`task-started`、`result-generated`、`task-finished` 和 `task-failed`。

**用户指南**：模型详情和选型建议请参见[语音识别模型](/developer-guides/speech/speech-to-text-models)。

**交互流程**：事件交互时序图请参见 [WebSocket API](/api-reference/speech-recognition/fun-asr-realtime/websocket-api)。客户端事件请参见[客户端事件](/api-reference/speech-recognition/fun-asr-realtime/client-events)。

## task-started

服务器处理 [run-task 指令](/api-reference/speech-recognition/fun-asr-realtime/client-events#run-task)后返回此事件，表示可以开始发送音频。

**示例**：

```json
{
  "header": {
    "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
    "event": "task-started",
    "attributes": {}
  },
  "payload": {}
}
```

**`header` 参数**：

| **参数**            | **类型** | **说明**                  |
| ----------------- | ------ | ----------------------- |
| header.task\_id   | string | 任务 ID。                  |
| header.event      | string | 事件类型。值为 `task-started`。 |
| header.attributes | object | 附加属性（通常为空）。             |

## result-generated

服务器产生识别结果时返回此事件，包含中间结果和最终结果。

**示例**：

```json
{
  "header": {
    "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
    "event": "result-generated",
    "attributes": {}
  },
  "payload": {
    "output": {
      "sentence": {
        "begin_time": 170,
        "end_time": 920,
        "text": "好，我知道了",
        "heartbeat": false,
        "sentence_end": true,
        "words": [
          {
            "begin_time": 170,
            "end_time": 295,
            "text": "好的",
            "punctuation": "，"
          },
          {
            "begin_time": 295,
            "end_time": 503,
            "text": "我",
            "punctuation": ""
          },
          {
            "begin_time": 503,
            "end_time": 711,
            "text": "知道",
            "punctuation": ""
          },
          {
            "begin_time": 711,
            "end_time": 920,
            "text": "了",
            "punctuation": ""
          }
        ]
      }
    },
    "usage": {
      "duration": 3
    }
  }
}
```

**`header` 参数**：

| **参数**          | **类型** | **说明**                      |
| --------------- | ------ | --------------------------- |
| header.event    | string | 事件类型。值为 `result-generated`。 |
| header.task\_id | string | 任务 ID。                      |

**`payload` 参数**：

| **参数** | **类型** | **说明**                                                                                             |
| ------ | ------ | -------------------------------------------------------------------------------------------------- |
| output | object | `output.sentence` 包含识别结果，详见下方。                                                                     |
| usage  | object | 语句未完成时（`sentence_end` = `false`）为 `null`。语句完成时（`sentence_end` = `true`），`usage.duration` 为计费时长（秒）。 |

**`payload.usage` 参数**：

| **参数**   | **类型**  | **说明**    |
| -------- | ------- | --------- |
| duration | integer | 计费时长，单位秒。 |

**`payload.output.sentence` 参数**：

| **参数**        | **类型**  | **说明**                                                                                                                         |
| ------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------ |
| begin\_time   | integer | 语句开始时间，单位毫秒。                                                                                                                   |
| end\_time     | integer | 语句结束时间，单位毫秒。                                                                                                                   |
| text          | string  | 识别文本。                                                                                                                          |
| words         | array   | 词级别时间戳。                                                                                                                        |
| heartbeat     | boolean | 为 `true` 时跳过此结果。与 [run-task 指令](/api-reference/speech-recognition/fun-asr-realtime/client-events#run-task)中的 `heartbeat` 设置对应。 |
| sentence\_end | boolean | 语句是否已结束（`true`=最终结果，`false`=中间结果）。                                                                                             |
| sentence\_id  | integer | 句子的序号标识。正常识别结果中，sentence\_id 从 1 开始递增。当 heartbeat 为 `true` 时（即心跳包），sentence\_id 固定为 0。                                         |

**`payload.output.sentence.words` 参数**：

| **参数**      | **类型**  | **说明**      |
| ----------- | ------- | ----------- |
| begin\_time | integer | 词开始时间，单位毫秒。 |
| end\_time   | integer | 词结束时间，单位毫秒。 |
| text        | string  | 识别的词。       |
| punctuation | string  | 标点符号。       |

## task-finished

**说明**：任务正常结束，可关闭连接或复用连接。

**示例**：

```json
{
  "header": {
    "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
    "event": "task-finished",
    "attributes": {}
  },
  "payload": {
    "output": {},
    "usage": null
  }
}
```

**`header` 参数**：

| **参数**            | **类型** | **说明**                   |
| ----------------- | ------ | ------------------------ |
| header.task\_id   | string | 任务 ID。                   |
| header.event      | string | 事件类型。值为 `task-finished`。 |
| header.attributes | object | 附加属性（通常为空）。              |

## task-failed

**说明**：任务失败，连接会被关闭，无法复用。

**示例**：

```json
{
  "header": {
    "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
    "event": "task-failed",
    "error_code": "CLIENT_ERROR",
    "error_message": "request timeout after 23 seconds.",
    "attributes": {}
  },
  "payload": {}
}
```

**`header` 参数**：

| **参数**                | **类型** | **说明**                 |
| --------------------- | ------ | ---------------------- |
| header.task\_id       | string | 任务 ID。                 |
| header.event          | string | 事件类型。值为 `task-failed`。 |
| header.error\_code    | string | 错误类型描述。                |
| header.error\_message | string | 具体错误原因。                |
| header.attributes     | object | 附加属性（通常为空）。            |
