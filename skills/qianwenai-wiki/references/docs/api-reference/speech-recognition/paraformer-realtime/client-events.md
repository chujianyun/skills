> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 实时语音识别（Paraformer）客户端事件

> Paraformer 实时语音识别服务中客户端通过 WebSocket 发送给服务端的客户端事件，包括 run-task（启动任务）和 finish-task（结束任务）。

本文介绍 Paraformer 实时语音识别服务中客户端通过 WebSocket 发送给服务端的客户端事件，包括 run-task（启动任务）和 finish-task（结束任务）两类指令的数据结构与字段含义。

**用户指南**：关于模型介绍和选型建议请参见[语音识别](/developer-guides/speech/speech-to-text-models)。

**事件交互流程**：如需了解事件交互时序，请参见 [WebSocket API](/api-reference/speech-recognition/paraformer-realtime/websocket-api)。

## run-task

**说明**：启动语音识别任务，设置模型、音频格式、采样率等参数。

**发送时机**：建立 WebSocket 连接后立即发送。

**响应事件**：服务端返回 [task-started](/api-reference/speech-recognition/paraformer-realtime/server-events#task-started) 事件后才能发送音频。

**示例**：

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
    "model": "paraformer-realtime-v2",
    "parameters": {
      "format": "pcm",
      "sample_rate": 16000,
      "disfluency_removal_enabled": false,
      "language_hints": ["en"]
    },
    "input": {}
  }
}
```

**`header` 参数**：

| **参数**    | **类型** | **是否必选** | **说明**                         |
| --------- | ------ | -------- | ------------------------------ |
| action    | string | 是        | 指令类型，固定为 `run-task`。           |
| task\_id  | string | 是        | 客户端生成的任务 ID（UUID 格式），用于关联后续事件。 |
| streaming | string | 是        | 固定为 `duplex`。                  |

**`payload` 参数**：

| **参数**         | **类型**     | **是否必选** | **说明**                  |
| -------------- | ---------- | -------- | ----------------------- |
| task\_group    | string     | 是        | 任务组，固定为 `audio`。        |
| task           | string     | 是        | 任务类型，固定为 `asr`。         |
| function       | string     | 是        | 功能类型，固定为 `recognition`。 |
| model          | string     | 是        | 模型名称。                   |
| input          | object     | 是        | 固定为 `{}`。               |
| **parameters** | **object** | **是**    | **语音识别参数，见下方。**         |

**`payload.parameters` 参数**：

| **参数**                                | **类型**         | **是否必选** | **说明**                                                                                                                                                                                        |
| ------------------------------------- | -------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| format                                | string         | 是        | 音频格式。取值：`pcm`、`wav`、`mp3`、`opus`、`speex`、`aac`、`amr`。                                                                                                                                         |
| sample\_rate                          | integer        | 是        | 采样率（Hz）。因模型而异：<br /> - paraformer-realtime-v2：支持任意采样率<br /> - paraformer-realtime-v1：仅支持 16000 Hz<br /> - paraformer-realtime-8k-v2：仅支持 8000 Hz<br /> - paraformer-realtime-8k-v1：仅支持 8000 Hz |
| vocabulary\_id                        | string         | 否        | 热词列表 ID。                                                                                                                                                                                      |
| disfluency\_removal\_enabled          | boolean        | 否        | 是否过滤语气词。默认值：`false`。                                                                                                                                                                          |
| language\_hints                       | array\[string] | 否        | 待识别音频语种。不设置时模型自动识别。取值：`zh`（中文）、`en`（英文）、`ja`（日语）、`yue`（粤语）、`ko`（韩语）、`de`（德语）、`fr`（法语）、`ru`（俄语）。                                                                                               |
| semantic\_punctuation\_enabled        | boolean        | 否        | 是否启用语义断句。默认值：`false`。<br /> - `true`：开启语义断句，关闭 VAD 断句。<br /> - `false`（默认）：开启 VAD 断句，关闭语义断句。<br /> 语义断句准确性更高，适合会议转写场景；VAD 断句延迟较低，适合交互场景。                                                      |
| max\_sentence\_silence                | integer        | 否        | VAD 断句静音阈值（ms）。当一段语音后的静音时长超过该阈值时，系统判定该句子已结束。默认值：1300。取值范围：\[200, 6000]。                                                                                                                       |
| multi\_threshold\_mode\_enabled       | boolean        | 否        | 是否启用多阈值模式。启用后可防止 VAD 断句切割过长。默认值：`false`。                                                                                                                                                      |
| punctuation\_prediction\_enabled      | boolean        | 否        | 是否在识别结果中添加标点符号。默认值：`true`。                                                                                                                                                                    |
| heartbeat                             | boolean        | 否        | 是否启用心跳包。默认值：`false`。<br /> - `true`：在持续发送静音音频的情况下，可保持与服务端的连接不中断。<br /> - `false`（默认）：即使持续发送静音音频，连接也将在 60 秒后因超时而断开。                                                                            |
| inverse\_text\_normalization\_enabled | boolean        | 否        | 是否启用逆文本正则化（ITN）。启用后，中文数字将转换为阿拉伯数字。默认值：`true`。                                                                                                                                                 |

<Warning>
  - Paraformer 须遵循如下音频约束：opus/speex 必须使用 Ogg 封装；wav 必须为 PCM 编码；amr 仅支持 AMR-NB 类型。
  - 仅 Paraformer 支持 `disfluency_removal_enabled` 参数。
  - 仅 Paraformer（v2）支持 `semantic_punctuation_enabled`、`max_sentence_silence`、`multi_threshold_mode_enabled`、`punctuation_prediction_enabled`、`heartbeat`、`inverse_text_normalization_enabled` 参数。
  - `max_sentence_silence` 和 `multi_threshold_mode_enabled` 仅在 `semantic_punctuation_enabled` 为 `false` 时生效。
</Warning>

## finish-task

**说明**：通知服务端音频发送完毕，请求结束任务。

**发送时机**：所有音频数据发送完毕后。

**响应事件**：服务端返回 [task-finished](/api-reference/speech-recognition/paraformer-realtime/server-events#task-finished) 事件。

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

| **参数**    | **类型** | **是否必选** | **说明**                                                            |
| --------- | ------ | -------- | ----------------------------------------------------------------- |
| action    | string | 是        | 指令类型，固定为 `finish-task`。                                           |
| task\_id  | string | 是        | 客户端生成的任务 ID（UUID 格式），需与 [run-task](#run-task) 事件中的 task\_id 保持一致。 |
| streaming | string | 是        | 固定为 `duplex`。                                                     |

**`payload` 参数**：

| **参数** | **类型** | **是否必选** | **说明**    |
| ------ | ------ | -------- | --------- |
| input  | object | 是        | 固定为 `{}`。 |
