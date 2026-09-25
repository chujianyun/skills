> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Sambert 服务端事件

> Sambert 实时语音合成 WebSocket 服务端事件参考

**用户指南**： 关于模型介绍和选型建议请参见[语音合成](/developer-guides/speech/tts)。

## task-started

当客户端发送 `run-task` 指令后，服务端返回 `task-started` 事件，标志任务已成功开启。

```json Example
{
  "header": {
    "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
    "event": "task-started",
    "attributes": {}
  },
  "payload": {}
}
```

| 字段              | 类型     | 说明                       |
| --------------- | ------ | ------------------------ |
| header.task\_id | string | 客户端生成的任务 ID。             |
| header.event    | string | 事件类型，固定为 `task-started`。 |
| payload         | object | 无内容，为空对象。                |

## result-generated

客户端发送文本后，服务端持续返回 `result-generated` 事件。该事件在 `output.sentence` 中直接返回完整的时间戳信息，包括字级别和音素级别时间戳（需启用相应参数）。

```json Example
{
  "header": {
    "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
    "event": "result-generated",
    "attributes": {}
  },
  "payload": {
    "output": {
      "sentence": {
        "begin_time": 0,
        "end_time": 1162,
        "words": [
          {
            "text": "床",
            "begin_time": 0,
            "end_time": 263,
            "phonemes": [
              {
                "begin_time": 0,
                "end_time": 119,
                "text": "ch_c",
                "tone": 2
              }
            ]
          }
        ]
      }
    },
    "usage": {
      "characters": 6
    }
  }
}
```

| 字段                                                       | 类型      | 说明                                            |
| -------------------------------------------------------- | ------- | --------------------------------------------- |
| header.task\_id                                          | string  | 客户端生成的任务 ID。                                  |
| header.event                                             | string  | 事件类型，固定为 `result-generated`。                  |
| payload.output.sentence.begin\_time                      | integer | 句子开始时间戳，单位：毫秒。                                |
| payload.output.sentence.end\_time                        | integer | 句子结束时间戳，单位：毫秒。                                |
| payload.output.sentence.words                            | array   | 字级别时间戳信息数组。                                   |
| payload.output.sentence.words\[].text                    | string  | 字的文本内容。                                       |
| payload.output.sentence.words\[].begin\_time             | integer | 字对应音频的开始时间戳，单位：毫秒。                            |
| payload.output.sentence.words\[].end\_time               | integer | 字对应音频的结束时间戳，单位：毫秒。                            |
| payload.output.sentence.words\[].phonemes                | array   | 音素级别时间戳信息数组（需启用 phoneme\_timestamp\_enabled）。 |
| payload.output.sentence.words\[].phonemes\[].text        | string  | 音素文本。                                         |
| payload.output.sentence.words\[].phonemes\[].tone        | integer | 音调。                                           |
| payload.output.sentence.words\[].phonemes\[].begin\_time | integer | 音素开始时间戳，单位：毫秒。                                |
| payload.output.sentence.words\[].phonemes\[].end\_time   | integer | 音素结束时间戳，单位：毫秒。                                |
| payload.usage.characters                                 | integer | 截止当前累计的计费字符数。                                 |

## task-finished

服务端返回 `task-finished` 事件，标志任务已结束。客户端可以关闭 WebSocket 连接或复用连接开启新任务。

```json Example
{
  "header": {
    "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
    "event": "task-finished",
    "attributes": {
      "request_uuid": "0a9dba9e-d3a6-45a4-be6d-xxxxxxxxxxxx"
    }
  },
  "payload": {
    "usage": {
      "characters": 13
    }
  }
}
```

| 字段                       | 类型      | 说明                        |
| ------------------------ | ------- | ------------------------- |
| header.task\_id          | string  | 客户端生成的任务 ID。              |
| header.event             | string  | 事件类型，固定为 `task-finished`。 |
| payload.usage.characters | integer | 截止当前累计的计费字符数。             |

## task-failed

当任务失败时，服务端返回 `task-failed` 事件。客户端需要关闭 WebSocket 连接并处理错误。

```json Example
{
  "header": {
    "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
    "event": "task-failed",
    "error_code": "InvalidParameter",
    "error_message": "[tts:]Engine return error code: 418",
    "attributes": {}
  },
  "payload": {}
}
```

| 字段                    | 类型     | 说明                      |
| --------------------- | ------ | ----------------------- |
| header.task\_id       | string | 客户端生成的任务 ID。            |
| header.event          | string | 事件类型，固定为 `task-failed`。 |
| header.error\_code    | string | 错误码。                    |
| header.error\_message | string | 具体错误信息。                 |
