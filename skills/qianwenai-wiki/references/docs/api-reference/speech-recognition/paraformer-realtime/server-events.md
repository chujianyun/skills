> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 实时语音识别（Paraformer）服务端事件

> Paraformer 实时语音识别服务通过 WebSocket 推送给客户端的服务端事件，包括 task-started、result-generated、task-finished、task-failed 四类事件。

本文介绍 Paraformer 实时语音识别服务通过 WebSocket 推送给客户端的服务端事件，包括 task-started、result-generated、task-finished、task-failed 四类事件的数据结构与字段含义。

**用户指南**：关于模型介绍和选型建议请参见[语音识别](/developer-guides/speech/speech-to-text-models)。

**事件交互流程**：如需了解事件交互时序，请参见 [WebSocket API](/api-reference/speech-recognition/paraformer-realtime/websocket-api)。

## task-started

**说明**：任务启动成功，客户端可开始发送音频数据。

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

| **参数**     | **类型** | **说明**                   |
| ---------- | ------ | ------------------------ |
| task\_id   | string | 客户端生成的任务 ID（UUID 格式）。    |
| event      | string | 事件类型，固定为 `task-started`。 |
| attributes | object | 附加属性（通常为空）。              |

**`payload`**：固定为 `{}`。

## result-generated

**说明**：识别结果，包含中间结果（sentence\_end=false）和最终结果（sentence\_end=true）。

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
        "end_time": null,
        "text": "好，我知道了",
        "heartbeat": false,
        "sentence_end": true,
        "words": [
          {"begin_time": 170, "end_time": 295, "text": "好", "punctuation": "，"},
          {"begin_time": 295, "end_time": 503, "text": "我", "punctuation": ""},
          {"begin_time": 503, "end_time": 711, "text": "知道", "punctuation": ""},
          {"begin_time": 711, "end_time": 920, "text": "了", "punctuation": ""}
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

| **参数**   | **类型** | **说明**                       |
| -------- | ------ | ---------------------------- |
| task\_id | string | 客户端生成的任务 ID（UUID 格式）。        |
| event    | string | 事件类型，固定为 `result-generated`。 |

**`payload.usage` 参数**：

当 `sentence_end` 为 `false`（当前句子未结束）时，`usage` 为 `null`。当 `sentence_end` 为 `true`（当前句子已结束）时，`usage.duration` 为当前任务计费时长。

| **参数**   | **类型**  | **说明**     |
| -------- | ------- | ---------- |
| duration | integer | 任务计费时长（秒）。 |

**`payload.output.sentence` 参数**：

| **参数**          | **类型**         | **说明**                                                                                            |
| --------------- | -------------- | ------------------------------------------------------------------------------------------------- |
| begin\_time     | integer        | 句子开始时间（ms）。                                                                                       |
| end\_time       | integer        | 句子结束时间（ms）。                                                                                       |
| text            | string         | 识别文本。                                                                                             |
| heartbeat       | boolean        | 若为 `true`，可跳过该结果（心跳包）。                                                                            |
| sentence\_end   | boolean        | 是否句子结束（`true`=最终结果，`false`=中间结果）。                                                                 |
| emo\_tag        | string         | 当前句子的情感。取值：<br /> - `positive`：正面情感，如开心、满意<br /> - `negative`：负面情感，如愤怒、沉闷<br /> - `neutral`：无明显情感 |
| emo\_confidence | float          | 情感置信度，取值范围 \[0.0, 1.0]，值越大表示置信度越高。                                                                |
| words           | array\[object] | 字时间戳信息，见下方。                                                                                       |

<Warning>
  `emo_tag` 和 `emo_confidence` 的使用条件：

  - 仅 paraformer-realtime-8k-v2 支持该功能
  - 必须关闭语义断句（将 [run-task](/api-reference/speech-recognition/paraformer-realtime/client-events#run-task) 事件的 `semantic_punctuation_enabled` 设为 `false`）才支持该功能
  - 只有在 `sentence_end` 的值为 `true` 时才显示情感识别结果
</Warning>

**`payload.output.sentence.words` 参数**：

| **参数**      | **类型**  | **说明**     |
| ----------- | ------- | ---------- |
| begin\_time | integer | 字开始时间（ms）。 |
| end\_time   | integer | 字结束时间（ms）。 |
| text        | string  | 识别文本。      |
| punctuation | string  | 标点符号。      |

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

| **参数**     | **类型** | **说明**                    |
| ---------- | ------ | ------------------------- |
| task\_id   | string | 客户端生成的任务 ID（UUID 格式）。     |
| event      | string | 事件类型，固定为 `task-finished`。 |
| attributes | object | 附加属性（通常为空）。               |

**`payload`**：无需关注其中内容，通常为 `{}`。

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

| **参数**         | **类型** | **说明**                  |
| -------------- | ------ | ----------------------- |
| task\_id       | string | 客户端生成的任务 ID（UUID 格式）。   |
| event          | string | 事件类型，固定为 `task-failed`。 |
| error\_code    | string | 错误类型描述。                 |
| error\_message | string | 具体错误原因。                 |
| attributes     | object | 附加属性（通常为空）。             |

**`payload`**：固定为 `{}`。
