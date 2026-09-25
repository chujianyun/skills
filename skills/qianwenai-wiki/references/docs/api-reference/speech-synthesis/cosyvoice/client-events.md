> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Qwen-Audio-TTS/CosyVoice 客户端事件

> Qwen-Audio-TTS/CosyVoice 实时语音合成 WebSocket 客户端事件参考

**用户指南**： 关于模型介绍和选型建议请参见[语音合成](/developer-guides/speech/tts)。

## run-task

**说明**：启动语音合成任务，设置模型、音色、采样率等参数。

**发送时机**：建立 WebSocket 连接后立即发送。

**响应事件**：服务端返回 task-started 事件后才能发送后续指令。

```json Example
{
    "header": {
        "action": "run-task",
        "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
        "streaming": "duplex"
    },
    "payload": {
        "task_group": "audio",
        "task": "tts",
        "function": "SpeechSynthesizer",
        "model": "qwen-audio-3.0-tts-flash",
        "parameters": {
            "text_type": "PlainText",
            "voice": "longanhuan_v3.6",
            "format": "mp3",
            "sample_rate": 22050,
            "volume": 50,
            "rate": 1.0,
            "pitch": 1.0,
            "enable_ssml": false
        },
        "input": {}
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
      客户端生成的任务 ID（UUID 格式），用于关联后续事件。和后续 continue-task、finish-task 中的 task\_id 保持一致。
    </ParamField>

    <ParamField body="streaming" type="string" required>
      固定为 `duplex`。
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
      模型名称。
    </ParamField>

    <ParamField body="input" type="object" required>
      输入数据：固定为空对象 `{}`，待合成文本通过 continue-task 指令发送。
    </ParamField>

    <ParamField body="parameters" type="object" required>
      语音合成参数。

      <Expandable title="属性">
        <ParamField body="text_type" type="string" required>
          固定为 `PlainText`。
        </ParamField>

        <ParamField body="voice" type="string" required>
          语音合成所使用的音色。

          - **系统音色**：参见[Qwen-Audio-TTS音色列表](/api-reference/speech-synthesis/qwen-audio-tts/voice-list)、[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)
          - **复刻音色**：通过声音复刻功能定制
          - **声音设计音色**：通过声音设计功能定制
        </ParamField>

        <ParamField body="format" type="string">
          音频编码格式。取值范围：pcm、wav、mp3（默认）、opus。

          <Note>`cosyvoice-v1` 不支持 opus 格式。</Note>
        </ParamField>

        <ParamField body="sample_rate" type="integer">
          音频采样率（Hz）。取值范围：8000, 16000, 22050（默认）, 24000, 44100, 48000。
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

        <ParamField body="bit_rate" type="integer">
          音频码率（kbps）。音频格式为 mp3 或 opus 时，支持通过 `bit_rate` 参数调整码率。默认值：32。取值范围：\[6, 510]。

          `cosyvoice-v1` 模型不支持该参数。
        </ParamField>

        <ParamField body="enable_ssml" type="boolean">
          是否开启 SSML 功能。默认值：false。设为 true 后，仅允许发送一次 continue-task 指令。

          <Note>SSML 的使用限制请参见 [SSML 使用限制](/developer-guides/speech/ssml#使用限制)。</Note>
        </ParamField>

        <ParamField body="word_timestamp_enabled" type="boolean">
          是否开启字级别时间戳。默认值：false。

          仅在流式输出模式下可用。支持的音色范围：cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash、cosyvoice-v3-plus 和 cosyvoice-v2 模型的复刻音色，以及[Qwen-Audio-TTS音色列表](/api-reference/speech-synthesis/qwen-audio-tts/voice-list)、[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)中标记为支持的系统音色。qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash及其他模型的复刻音色不支持此功能。
        </ParamField>

        <ParamField body="seed" type="integer">
          生成时使用的随机数种子，使合成的效果产生变化。在模型版本、文本、音色及其他参数均相同的前提下，使用相同的 seed 可复现相同的合成结果。默认值：0。取值范围：\[0, 65535]。

          cosyvoice-v1 不支持该参数。
        </ParamField>

        <ParamField body="language_hints" type="array[string]">
          指定语音合成的目标语言，提升合成效果。

          <Note>
            - 此参数为数组，但当前版本仅处理第一个元素，因此建议只传入一个值。
            - 此参数用于指定语音合成的目标语言，该设置与声音复刻时的样本音频的语种无关。
          </Note>

          当数字、缩写、符号等朗读方式或者小语种合成效果不符合预期时使用。

          取值范围：zh（中文）、en（英语）、fr（法语）、de（德语）、ja（日语）、ko（韩语）、ru（俄语）、pt（葡萄牙语）、th（泰语）、id（印尼语）、vi（越南语）、es（西班牙语）、it（意大利语）、ms（马来西亚语）、fil（菲律宾语）、ar（阿拉伯语）。

          cosyvoice-v1 不支持该功能。
        </ParamField>

        <ParamField body="instruction" type="string">
          设置指令，用于控制方言、情感或角色等合成效果。具体使用说明请参见[指令控制](/developer-guides/speech/realtime-streaming#指令控制)。
        </ParamField>

        <ParamField body="enable_aigc_tag" type="boolean">
          是否在生成的音频中添加 AIGC 隐性标识。设置为 true 时，会将隐性标识嵌入到支持格式（wav/mp3/opus）的音频中。默认值：false。仅 qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2 支持该功能。
        </ParamField>

        <ParamField body="aigc_propagator" type="string">
          设置 AIGC 隐性标识中的 `ContentPropagator` 字段，用于标识内容的传播者。仅在 `enable_aigc_tag` 为 `true` 时生效。默认值：阿里云 UID。仅 qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2 支持该功能。
        </ParamField>

        <ParamField body="aigc_propagate_id" type="string">
          设置 AIGC 隐性标识中的 `PropagateID` 字段，用于唯一标识一次具体的传播行为。仅在 `enable_aigc_tag` 为 `true` 时生效。默认值：本次语音合成请求 Request ID。仅 qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2 支持该功能。
        </ParamField>

        <ParamField body="hot_fix" type="object">
          文本热修复配置，用于自定义指定词语的发音或对待合成文本进行替换。cosyvoice-v2、cosyvoice-v1 不支持该功能。

          - `pronunciation`：自定义发音。指定词语的拼音标注，用于纠正默认发音不准确的情况。
          - `replace`：文本替换。在语音合成前将指定词语替换为目标文本。

          ```json
          "hot_fix": {
            "pronunciation": [
              {"天气": "tian1 qi4"}
            ],
            "replace": [
              {"今天": "金天"}
            ]
          }
          ```
        </ParamField>

        <ParamField body="enable_markdown_filter" type="boolean">
          是否启用 Markdown 过滤。启用该功能后，系统在合成语音前自动过滤输入文本中的 Markdown 标记符号。默认值：false。仅 cosyvoice-v3-flash 复刻音色支持该功能。
        </ParamField>
      </Expandable>
    </ParamField>
  </Expandable>
</ParamField>

## continue-task

**说明**：用于发送待合成文本。可一次性发送，也可分段按顺序发送。

**发送时机**：在接收到服务端返回的 task-started 事件后。

**数量限制**：

- 单次调用最多发送 20000 字符
- 累计最多发送 200000 字符
- 发送间隔不得超过 23 秒，否则连接超时

```json Example
{
    "header": {
        "action": "continue-task",
        "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
        "streaming": "duplex"
    },
    "payload": {
        "input": {
            "text": "床前明月光，疑是地上霜"
        }
    }
}
```

<ParamField body="header" type="object" required>
  消息头。

  <Expandable title="属性">
    <ParamField body="action" type="string" required>
      指令类型，固定为 `continue-task`。
    </ParamField>

    <ParamField body="task_id" type="string" required>
      任务 ID（UUID 格式），需要和 run-task 中的 task\_id 保持一致。
    </ParamField>

    <ParamField body="streaming" type="string" required>
      固定为 `duplex`。
    </ParamField>
  </Expandable>
</ParamField>

<ParamField body="payload" type="object" required>
  请求体。

  <Expandable title="属性">
    <ParamField body="input" type="object" required>
      包含待合成文本。

      <Expandable title="属性">
        <ParamField body="text" type="string" required>
          待合成文本。单次最多 20000 字符，累计最多 200000 字符。
        </ParamField>
      </Expandable>
    </ParamField>
  </Expandable>
</ParamField>

## finish-task

**说明**：通知服务端文本发送完毕，请求结束任务。如需取消当前轮次的语音合成任务，可在 input 中设置 directive 为 cancel。

**发送时机**：所有文本发送完毕后立即发送。

**响应事件**：服务端返回 task-finished 事件。

```json Example
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

**取消任务示例**：

```json Example
{
    "header": {
        "action": "finish-task",
        "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
        "streaming": "duplex"
    },
    "payload": {
        "input": {
            "directive": "cancel"
        }
    }
}
```

<ParamField body="header" type="object" required>
  消息头。

  <Expandable title="属性">
    <ParamField body="action" type="string" required>
      指令类型，固定为 `finish-task`。
    </ParamField>

    <ParamField body="task_id" type="string" required>
      任务 ID（UUID 格式），需要和 run-task 中的 task\_id 保持一致。
    </ParamField>

    <ParamField body="streaming" type="string" required>
      固定为 `duplex`。
    </ParamField>
  </Expandable>
</ParamField>

<ParamField body="payload" type="object" required>
  请求体。

  <Expandable title="属性">
    <ParamField body="input" type="object" required>
      任务输入。为空对象 `{}` 时表示正常结束任务；包含 `directive` 时可用于取消当前轮次的语音合成任务。

      <Expandable title="属性">
        <ParamField body="directive" type="string">
          控制任务结束行为。当前仅支持取值为 `cancel`，表示取消当前轮次的语音合成任务，服务端会立即返回 `task-finished` 事件，且不会输出后续音频。

          取消后，可在当前 WebSocket 连接上重新发起语音合成任务（发送新的 `run-task` 事件），无需重新建立连接。

          <Warning>
            **模型限制**：Qwen-Audio-TTS 系列模型的所有模型都支持该功能；CosyVoice 系列模型仅 v2 及以上版本支持该功能。
          </Warning>
        </ParamField>
      </Expandable>
    </ParamField>
  </Expandable>
</ParamField>
