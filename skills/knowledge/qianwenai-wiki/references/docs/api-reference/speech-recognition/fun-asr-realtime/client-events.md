> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 实时语音识别（Qwen-Audio-3.0-ASR-Flash-Streaming/Fun-ASR-Realtime）客户端事件

> Qwen-Audio-3.0-ASR-Flash-Streaming/Fun-ASR-Realtime 实时语音识别 WebSocket 客户端事件参考

客户端事件是客户端通过 WebSocket 发送给 Qwen-Audio-3.0-ASR-Flash-Streaming/Fun-ASR-Realtime 实时语音识别服务的 JSON 指令：`run-task` 启动识别任务、`continue-task` 更新上下文、`finish-task` 结束任务。

**用户指南**：模型详情和选型建议请参见[语音识别模型](/developer-guides/speech/speech-to-text-models)。

**交互流程**：事件交互时序图请参见 [WebSocket API](/api-reference/speech-recognition/fun-asr-realtime/websocket-api)。服务端事件请参见[服务端事件](/api-reference/speech-recognition/fun-asr-realtime/server-events)。

## run-task

建立连接后，发送此指令启动识别任务并设置参数。

**发送时机**：WebSocket 连接建立后立即发送。

**响应**：服务端返回 [task-started](/api-reference/speech-recognition/fun-asr-realtime/server-events#task-started) 事件后，客户端方可开始发送音频。

**示例**：

<Tabs>
  <Tab title="基本请求">
    ```json
    {
      "header": {
        "action": "run-task",
        "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
        "streaming": "duplex"
      },
      "payload": {
        "task_group": "audio",
        "task": "asr",
        "function": "recognition",
        "model": "qwen-audio-3.0-asr-flash-streaming",
        "parameters": {
          "format": "pcm",
          "sample_rate": 16000,
          "vocabulary_id": "vocab-xxx-24ee19fa8cfb4d52902170a0xxxxxxxx"
        },
        "input": {}
      }
    }
    ```
  </Tab>

  <Tab title="即时热词">
    ```json
    {
      "header": {
        "action": "run-task",
        "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
        "streaming": "duplex"
      },
      "payload": {
        "task_group": "audio",
        "task": "asr",
        "function": "recognition",
        "model": "qwen-audio-3.0-asr-flash-streaming",
        "parameters": {
          "format": "pcm",
          "sample_rate": 16000,
          "vocabulary": {"张三": 5, "李四": 5}
        },
        "input": {}
      }
    }
    ```
  </Tab>

  <Tab title="携带上下文">
    ```json
    {
      "header": {
        "action": "run-task",
        "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
        "streaming": "duplex"
      },
      "payload": {
        "task_group": "audio",
        "task": "asr",
        "function": "recognition",
        "model": "qwen-audio-3.0-asr-flash-streaming",
        "parameters": {
          "format": "pcm",
          "sample_rate": 16000
        },
        "input": {
          "context": [
            {
              "role": "user",
              "content": [
                {
                  "type": "input_text",
                  "text": "你好啊"
                }
              ]
            },
            {
              "role": "assistant",
              "content": [
                {
                  "type": "text",
                  "text": "你好啊，我是通义千问，有什么可以帮助你的？"
                }
              ]
            }
          ]
        }
      }
    }
    ```
  </Tab>
</Tabs>

**`header` 参数**：

| **参数**           | **类型** | **是否必选** | **说明**                                           |
| ---------------- | ------ | -------- | ------------------------------------------------ |
| header.action    | string | 是        | 指令类型。设为 `run-task`。                              |
| header.task\_id  | string | 是        | 唯一任务 ID。在 [finish-task 指令](#finish-task)中须使用相同值。 |
| header.streaming | string | 是        | 通信模式。设为 `duplex`。                                |

**`payload` 参数**：

| **参数**                          | **类型**         | **是否必选** | **说明**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------------------------------- | -------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| payload.task\_group             | string         | 是        | 任务组。设为 `audio`。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| payload.task                    | string         | 是        | 任务类型。设为 `asr`。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| payload.function                | string         | 是        | 功能类型。设为 `recognition`。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| payload.model                   | string         | 是        | 指定模型名。支持 Qwen-Audio-3.0-ASR-Flash-Streaming 和 Fun-ASR-Realtime 系列模型，详情请参见[支持的模型与地域](/developer-guides/speech/speech-to-text-models)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| payload.input                   | object         | 是        | 输入对象。不携带上下文时传入 `{}`。详见下方 [context 参数](#context-参数)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **payload.parameters**          |                |          |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| format                          | string         | 是        | 音频格式：`pcm`、`wav`、`mp3`、`opus`、`speex`、`aac`、`amr`。详见 [WebSocket API 音频要求](/api-reference/speech-recognition/fun-asr-realtime/websocket-api#音频要求)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| sample\_rate                    | integer        | 是        | 音频采样率，单位 Hz。8k 模型仅支持 8000 Hz，其他模型支持任意采样率。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| vocabulary\_id                  | string         | 否        | 热词表 ID，用于热词识别。详见[自定义热词](/developer-guides/speech/improve-recognition-accuracy)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| vocabulary                      | object         | 否        | 即时热词。以内联字典形式传入热词及权重，例如 `{"张三": 5, "李四": 5}`。仅 `qwen-audio-3.0-asr-flash-streaming` 支持。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| semantic\_punctuation\_enabled  | boolean        | 否        | 是否启用语义标点。默认值：`false`。<br /> - `true`：高精度标点，适用于会议场景。启用后将禁用 VAD 标点。<br /> - `false`：低延迟 VAD 标点，适用于交互场景。<br /> 语义标点在断句准确性上更优，VAD 标点响应更快。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| max\_sentence\_silence          | integer        | 否        | VAD 静音阈值，单位毫秒。静音时长超过此值时断句。当 `semantic_punctuation_enabled` 为 `true` 时，该参数不作为返回 `sentence_end` 的判定依据，但设置过低可能影响识别效果。默认值：1300。取值范围：\[200, 6000]。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| multi\_threshold\_mode\_enabled | boolean        | 否        | 防止 VAD 模式下产生过长语句。默认值：`false`。仅在 `semantic_punctuation_enabled` 为 `false` 时生效。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| heartbeat                       | boolean        | 否        | 是否启用保活。默认值：`false`。<br /> - `true`：持续发送静音音频时保持连接不断开。<br /> - `false`（默认）：即使持续发送静音音频，连接也将在一定时间后因超时而断开。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| language\_hints                 | array\[string] | 否        | 识别语言代码。不设置时自动检测语言。系统仅读取数组中的首个值，多余值将被忽略。不同模型支持的语言代码如下：<br /> **fun-asr-realtime、fun-asr-realtime-2025-11-07**：`zh`（中文）、`en`（英文）、`ja`（日语）、`ko`（韩语）、`vi`（越南语）、`th`（泰语）、`id`（印尼语）、`ms`（马来语）、`tl`（菲律宾语）、`hi`（印地语）、`ar`（阿拉伯语）、`fr`（法语）、`de`（德语）、`es`（西班牙语）、`pt`（葡萄牙语）、`ru`（俄语）、`it`（意大利语）、`nl`（荷兰语）、`sv`（瑞典语）、`da`（丹麦语）、`fi`（芬兰语）、`no`（挪威语）、`el`（希腊语）、`pl`（波兰语）、`cs`（捷克语）、`hu`（匈牙利语）、`ro`（罗马尼亚语）、`bg`（保加利亚语）、`hr`（克罗地亚语）、`sk`（斯洛伐克语）<br /> **fun-asr-realtime-2026-02-28**：`zh`（中文）、`en`（英文）、`ja`（日语）<br /> **fun-asr-realtime-2025-09-15**：`zh`（中文）、`en`（英文）<br /> **fun-asr-flash-8k-realtime、fun-asr-flash-8k-realtime-2026-01-28**：`zh`（中文） |
| speech\_noise\_threshold        | float          | 否        | 语音噪声检测阈值，用于调节 VAD 灵敏度。取值范围：\[-1.0, 1.0]。接近 -1：更多噪声可能被识别为语音。接近 +1：部分语音可能被过滤为噪声。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| special\_word\_filter           | string         | 否        | 敏感词过滤配置，仅 Fun-ASR 支持。最多支持设置 32 个敏感词。参见[敏感词过滤](#敏感词过滤)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |

<Note>
  静音音频指的是在音频文件或数据流中没有声音信号的内容。静音音频可以通过多种方法生成，例如使用音频编辑软件如 Audacity 或 Adobe Audition，或者通过命令行工具如 FFmpeg。
</Note>

<Warning>
  `speech_noise_threshold` 是高级参数，微小的调整会显著影响识别质量。建议以 0.1 为步长逐步调整，并充分测试。
</Warning>

<a id="敏感词过滤" />

### 敏感词过滤

敏感词过滤可对识别结果中的敏感词执行替换或移除，适用于客服质检、内容合规、字幕审核等场景。仅 Fun-ASR 支持，最多支持设置 32 个敏感词。未传入 `special_word_filter` 参数时，不会对敏感词进行过滤。

`special_word_filter` 为 JSON 对象，包含三个子字段：

- `filter_with_signed.word_list`：字符串数组，列出需要被替换为等长 `*` 的敏感词。例如 `["测试"]`，"帮我测试一下"会变成"帮我\*\*一下"。
- `filter_with_empty.word_list`：字符串数组，列出需要从结果中完全移除的敏感词。例如 `["开始"]`，"比赛这就要开始了吗"会变成"比赛这就要了吗"。
- `system_reserved_filter`：布尔值，默认 `false`。是否启用敏感词过滤功能。

配置示例：

```json
{
  "special_word_filter": {
    "filter_with_signed": {
      "word_list": ["测试"]
    },
    "filter_with_empty": {
      "word_list": ["开始", "发生"]
    },
    "system_reserved_filter": true
  }
}
```

### context 参数

`payload.input.context` 字段用于传入对话上下文，辅助识别、提升专有词汇的识别准确率。使用方法详见[提升识别准确率](/developer-guides/speech/improve-recognition-accuracy)。

<Warning>
  仅 `qwen-audio-3.0-asr-flash-streaming`、`fun-asr-realtime` 和 `fun-asr-realtime-2025-11-07` 模型支持上下文。
</Warning>

| **参数**                     | **类型**         | **是否必选** | **说明**                                                                          |
| -------------------------- | -------------- | -------- | ------------------------------------------------------------------------------- |
| context                    | array\[object] | 否        | 对话上下文数组。                                                                        |
| context\[].role            | string         | 是        | 消息角色。`user`：前几轮用户语音的识别结果或领域相关的词表；`assistant`：前几轮大语言模型的回复内容。                     |
| context\[].content         | array\[object] | 是        | 消息内容列表。                                                                         |
| context\[].content\[].type | string         | 是        | 内容类型。`input_text`：用户语音识别结果或词表（role 为 user 时）；`text`：模型回复内容（role 为 assistant 时）。 |
| context\[].content\[].text | string         | 是        | 文本内容。                                                                           |

<Warning>
  - 上下文消息（`input_text` 和 `text` 类型）各最多 5 条，超出时保留最近的 5 条。
  - 每轮上下文文本总长度（`user` 和 `assistant` 的 `text` 字段长度之和）不超过 400 个字符，超出部分从末尾截断。
  - 上下文消息必须按对话轮次排列，每轮中 `user`（`input_text` 类型）必须在对应的 `assistant`（`text` 类型）之前。
</Warning>

## continue-task

在任务执行过程中更新对话上下文信息，用于辅助识别。

**发送时机**：任务运行中，需要更新对话上下文时发送。

<Warning>
  仅 `qwen-audio-3.0-asr-flash-streaming`、`fun-asr-realtime` 和 `fun-asr-realtime-2025-11-07` 模型支持该事件。
</Warning>

**示例**：

```json
{
  "header": {
    "action": "continue-task",
    "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
    "streaming": "duplex"
  },
  "payload": {
    "input": {
      "context": [
        {
          "role": "user",
          "content": [
            {
              "type": "input_text",
              "text": "你好啊"
            }
          ]
        },
        {
          "role": "assistant",
          "content": [
            {
              "type": "text",
              "text": "你好啊，我是通义千问，有什么可以帮助你的？"
            }
          ]
        }
      ]
    }
  }
}
```

**`header` 参数**：

| **参数**           | **类型** | **是否必选** | **说明**                                            |
| ---------------- | ------ | -------- | ------------------------------------------------- |
| header.action    | string | 是        | 指令类型。设为 `continue-task`。                          |
| header.task\_id  | string | 是        | 任务 ID。须与 [run-task 指令](#run-task)中的 `task_id` 一致。 |
| header.streaming | string | 是        | 通信模式。设为 `duplex`。                                 |

**`payload` 参数**：

| **参数**                | **类型**         | **是否必选** | **说明**                                 |
| --------------------- | -------------- | -------- | -------------------------------------- |
| payload.input         | object         | 是        | 输入对象。                                  |
| payload.input.context | array\[object] | 否        | 对话上下文。参数结构同 [context 参数](#context-参数)。 |

## finish-task

通知服务器音频传输已完成。

**发送时机**：所有音频数据发送完毕后。

**响应**：服务端返回 [task-finished](/api-reference/speech-recognition/fun-asr-realtime/server-events#task-finished) 事件。

**示例**：

```json
{
  "header": {
    "action": "finish-task",
    "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
    "streaming": "duplex"
  },
  "payload": {
    "input": {}
  }
}
```

**`header` 参数**：

| **参数**           | **类型** | **是否必选** | **说明**                                            |
| ---------------- | ------ | -------- | ------------------------------------------------- |
| header.action    | string | 是        | 指令类型。设为 `finish-task`。                            |
| header.task\_id  | string | 是        | 任务 ID。须与 [run-task 指令](#run-task)中的 `task_id` 一致。 |
| header.streaming | string | 是        | 通信模式。设为 `duplex`。                                 |

**`payload` 参数**：

| **参数**        | **类型** | **是否必选** | **说明**        |
| ------------- | ------ | -------- | ------------- |
| payload.input | object | 是        | 输入配置。设为 `{}`。 |
