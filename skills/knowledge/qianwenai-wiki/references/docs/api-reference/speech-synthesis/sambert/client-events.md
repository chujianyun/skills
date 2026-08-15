> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Sambert 客户端事件

> Sambert 实时语音合成 WebSocket 客户端事件参考

**用户指南**： 关于模型介绍和选型建议请参见[语音合成](/developer-guides/speech/tts)。

## run-task

**说明**：启动语音合成任务，设置模型、采样率等参数，并一次性发送待合成文本。

**发送时机**：建立 WebSocket 连接后立即发送。

**响应事件**：服务端返回 task-started 事件。

<Warning>
  Sambert 不支持流式输入，待合成文本需要在 run-task 的 `input.text` 中一次性发送。不支持 continue-task 和 finish-task 指令。
</Warning>

```json Example
{
    "header": {
        "action": "run-task",
        "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
        "streaming": "out"
    },
    "payload": {
        "task_group": "audio",
        "task": "tts",
        "function": "SpeechSynthesizer",
        "model": "sambert-zhichu-v1",
        "parameters": {
            "text_type": "PlainText",
            "format": "wav",
            "sample_rate": 16000,
            "volume": 50,
            "rate": 1.0,
            "pitch": 1.0,
            "word_timestamp_enabled": true,
            "phoneme_timestamp_enabled": true
        },
        "input": {
            "text": "待合成文本"
        }
    }
}
```

<ParamField body="header" type="object" required>
  消息头。

  <Expandable title="属性">
    <ParamField body="action" type="string" required>
      指令类型，固定为 `run-task`。
    </ParamField>

    <ParamField body="task_id" type="string" required>
      客户端生成的任务 ID（UUID 格式），用于关联后续事件。
    </ParamField>

    <ParamField body="streaming" type="string" required>
      固定为 `out`。
    </ParamField>
  </Expandable>
</ParamField>

<ParamField body="payload" type="object" required>
  请求体。

  <Expandable title="属性">
    <ParamField body="task_group" type="string" required>
      任务组，固定为 `audio`。
    </ParamField>

    <ParamField body="task" type="string" required>
      任务类型，固定为 `tts`。
    </ParamField>

    <ParamField body="function" type="string" required>
      功能类型，固定为 `SpeechSynthesizer`。
    </ParamField>

    <ParamField body="model" type="string" required>
      模型名称，如 `sambert-zhichu-v1`。
    </ParamField>

    <ParamField body="input" type="object" required>
      输入数据，包含 `text` 字段，直接传入待合成文本。

      <Expandable title="属性">
        <ParamField body="text" type="string" required>
          待合成文本。
        </ParamField>
      </Expandable>
    </ParamField>

    <ParamField body="parameters" type="object" required>
      语音合成参数。

      <Expandable title="属性">
        <ParamField body="text_type" type="string" required>
          固定为 `PlainText`。
        </ParamField>

        <ParamField body="format" type="string">
          音频编码格式。取值范围：pcm、wav（默认）、mp3。
        </ParamField>

        <ParamField body="sample_rate" type="integer">
          音频采样率（Hz）。取值范围：8000, 16000（默认）, 22050, 24000。
        </ParamField>

        <ParamField body="volume" type="integer">
          音量。默认值：50。取值范围：\[0, 100]。
        </ParamField>

        <ParamField body="rate" type="float">
          语速。默认值：1.0。取值范围：\[0.5, 2.0]。
        </ParamField>

        <ParamField body="pitch" type="float">
          音调。默认值：1.0。取值范围：\[0.5, 2.0]。
        </ParamField>

        <ParamField body="word_timestamp_enabled" type="boolean">
          是否开启字级别时间戳。默认值：false。适用范围：所有 Sambert 模型。
        </ParamField>

        <ParamField body="phoneme_timestamp_enabled" type="boolean">
          是否开启音素级别时间戳。默认值：false。需要先开启 word\_timestamp\_enabled。
        </ParamField>
      </Expandable>
    </ParamField>
  </Expandable>
</ParamField>
