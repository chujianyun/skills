> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 实时语音识别（Qwen-ASR-Realtime）客户端事件

> WebSocket 客户端事件参考

Qwen-ASR Realtime WebSocket 会话中，客户端发送给服务端的事件。

## 连接

连接地址：

```
wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model={model_name}
```

认证请求头：

```
Authorization: Bearer $DASHSCOPE_API_KEY
OpenAI-Beta: realtime=v1
```

将 `{model_name}` 替换为 `qwen3-asr-flash-realtime` 等[支持的模型](/developer-guides/speech/speech-to-text-models)，将 `$DASHSCOPE_API_KEY` 替换为您的 [API Key](https://platform.qianwenai.com/home/api-keys)。

功能概述和示例代码请参考[实时语音识别](/developer-guides/speech/asr-realtime)。服务端事件请参考 [Qwen-ASR-Realtime 服务端事件](/api-reference/speech-recognition/qwen-asr-realtime/server-events)。

## 事件生命周期

典型会话流程：

1. 建立 WebSocket 连接。
2. 发送 `session.update` 设置音频格式、语言和 VAD 选项。
3. 持续发送 `input_audio_buffer.append` 流式传输音频。
4. 手动模式下，发送 `input_audio_buffer.commit` 触发识别。VAD 模式下，服务端自动触发识别。
5. 发送 `session.finish` 结束会话。收到 `session.finished` 后断开连接。

## session.update

连接成功后立即发送，用于设置音频格式、语言和语音活动检测（VAD）选项。省略时使用默认值。

设置成功后，服务端返回 [`session.updated`](/api-reference/speech-recognition/qwen-asr-realtime/server-events)。

```json Example
{
  "event_id": "event_123",
  "type": "session.update",
  "session": {
    "input_audio_format": "pcm",
    "sample_rate": 16000,
    "input_audio_transcription": {
      "language": "zh"
    },
    "turn_detection": {
      "type": "server_vad",
      "threshold": 0.0,
      "silence_duration_ms": 400
    }
  }
}
```

<ParamField body="type" type="string" required>
  固定值：`session.update`。
</ParamField>

<ParamField body="event_id" type="string" required>
  唯一的事件 ID。
</ParamField>

<ParamField body="session" type="object" required>
  会话配置。

  <Expandable title="properties">
    <ParamField body="input_audio_format" type="string">
      音频编码格式。可选值：`pcm`、`opus`。默认值：`pcm`。
    </ParamField>

    <ParamField body="sample_rate" type="integer">
      采样率，单位 Hz。可选值：`16000`、`8000`。默认值：`16000`。设置为 `8000` 时，服务端会上采样至 16,000 Hz，会增加少量延迟。仅在原始音频为 8 kHz 的场景（如电话录音）中使用 `8000`。
    </ParamField>

    <ParamField body="input_audio_transcription" type="object">
      识别设置。

      <Expandable title="properties">
        <ParamField body="language" type="string">
          音频语言。参见[支持的语言](#支持的语言)。
        </ParamField>

        <ParamField body="corpus" type="object">
          上下文偏置配置。

          <Expandable title="properties">
            <ParamField body="text" type="string">
              用于[上下文偏置](/developer-guides/speech/asr-realtime#core-usage-context-biasing-qwen-asr)的参考文本——可以是背景描述、实体列表或参考资料，帮助提升识别准确率。最大 10,000 个 token。
            </ParamField>
          </Expandable>
        </ParamField>
      </Expandable>
    </ParamField>

    <ParamField body="turn_detection" type="object">
      VAD 设置。设置为 `null` 可禁用 [VAD 模式](/developer-guides/speech/asr-realtime#interaction-flow-qwen-asr-realtime)，改用[手动模式](/developer-guides/speech/asr-realtime#interaction-flow-qwen-asr-realtime)。如果提供此字段，则启用 VAD 模式。

      <Expandable title="properties">
        <ParamField body="type" type="string" required>
          固定值：`server_vad`。
        </ParamField>

        <ParamField body="threshold" type="float">
          VAD 灵敏度。默认值：`0.2`。取值范围：`[-1, 1]`。值越低灵敏度越高，但可能误触背景噪音；值越高灵敏度越低，可避免噪音环境中的误触发。参见[推荐 VAD 预设](#推荐-vad-预设)。
        </ParamField>

        <ParamField body="silence_duration_ms" type="integer">
          标记语音结束的静音时长，单位毫秒。默认值：`800`。取值范围：`[200, 6000]`。较短的值（如 300 ms）可加快响应速度，但可能将句中停顿误判为断句；较长的值（如 1,200 ms）能更好地处理停顿，但会增加延迟。参见[推荐 VAD 预设](#推荐-vad-预设)。
        </ParamField>
      </Expandable>
    </ParamField>
  </Expandable>
</ParamField>

### 推荐 VAD 预设

可从以下预设开始，根据实际效果调整：

| 预设     | threshold | silence\_duration\_ms | 适用场景                           |
| ------ | --------- | --------------------- | ------------------------------ |
| 低延迟    | `0.0`     | `400`                 | 快速交互场景（语音指令、智能客服），响应速度优先于长停顿处理 |
| 均衡（默认） | `0.2`     | `800`                 | 通用转写，兼顾速度与准确率                  |

<a id="supported-languages" />

### 支持的语言

| 代码  | 语言                 |
| --- | ------------------ |
| zh  | 中文（普通话、四川话、闽南语、吴语） |
| yue | 粤语                 |
| en  | 英语                 |
| ja  | 日语                 |
| de  | 德语                 |
| ko  | 韩语                 |
| ru  | 俄语                 |
| fr  | 法语                 |
| pt  | 葡萄牙语               |
| ar  | 阿拉伯语               |
| it  | 意大利语               |
| es  | 西班牙语               |
| hi  | 印地语                |
| id  | 印尼语                |
| th  | 泰语                 |
| tr  | 土耳其语               |
| uk  | 乌克兰语               |
| vi  | 越南语                |
| cs  | 捷克语                |
| da  | 丹麦语                |
| fil | 菲律宾语               |
| fi  | 芬兰语                |
| is  | 冰岛语                |
| ms  | 马来语                |
| no  | 挪威语                |
| pl  | 波兰语                |
| sv  | 瑞典语                |

## input\_audio\_buffer.append

向服务端缓冲区流式发送音频数据。

不同模式下的行为：

- **VAD 模式**： 服务端自动监测缓冲区中的语音活动，并自动触发识别。
- **手动模式**： 您控制语音边界。发送较小的数据块可降低延迟。

<Warning>
  `audio` 字段为 Base64 编码。手动模式下，单个事件最大 15 MiB。无论哪种模式，服务端均不确认此事件。
</Warning>

```json Example
{
  "event_id": "event_2728",
  "type": "input_audio_buffer.append",
  "audio": "<Base64-encoded-audio-data>"
}
```

<ParamField body="type" type="string" required>
  固定值：`input_audio_buffer.append`。
</ParamField>

<ParamField body="event_id" type="string" required>
  唯一的事件 ID。
</ParamField>

<ParamField body="audio" type="string" required>
  Base64 编码的音频数据。
</ParamField>

## input\_audio\_buffer.commit

将缓冲区中的所有音频作为一段完整语音触发识别。用于手动模式下由您控制语音边界的场景（如按住说话，松开按钮标记语音结束）。

VAD 模式下不可用。

成功后，服务端返回 [`input_audio_buffer.committed`](/api-reference/speech-recognition/qwen-asr-realtime/server-events)。

```json Example
{
  "event_id": "event_789",
  "type": "input_audio_buffer.commit"
}
```

<ParamField body="type" type="string" required>
  固定值：`input_audio_buffer.commit`。
</ParamField>

<ParamField body="event_id" type="string" required>
  唯一的事件 ID。
</ParamField>

## session.finish

结束会话。服务端的响应取决于是否检测到语音：

- **检测到语音**： 服务端完成识别，先发送 [`conversation.item.input_audio_transcription.completed`](/api-reference/speech-recognition/qwen-asr-realtime/server-events) 返回识别结果，再发送 [`session.finished`](/api-reference/speech-recognition/qwen-asr-realtime/server-events)。
- **未检测到语音**： 服务端直接发送 [`session.finished`](/api-reference/speech-recognition/qwen-asr-realtime/server-events)。

收到 `session.finished` 后，断开 WebSocket 连接。

```json Example
{
  "event_id": "event_341",
  "type": "session.finish"
}
```

<ParamField body="type" type="string" required>
  固定值：`session.finish`。
</ParamField>

<ParamField body="event_id" type="string" required>
  唯一的事件 ID。
</ParamField>
