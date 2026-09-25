> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Qwen-Omni client events

> WebSocket 客户端参考

客户端通过 WebSocket 向服务端发送的事件。

<Tip>
  如果不需要实时交互，Qwen-Omni 也支持 [Chat API](/api-reference/chat/openai-chat)。
</Tip>

<Note>
  参考：[实时多模态](/developer-guides/speech/realtime-multimodal-speech)。
</Note>

## session.update

连接建立后发送此事件，用于更新会话配置。服务端会校验参数并返回完整配置或错误信息。

```json Example
{
  "event_id": "event_ToPZqeobitzUJnt3QqtWg",
  "type": "session.update",
  "session": {
    "modalities": ["text", "audio"],
    "model": "qwen3.5-omni-flash-realtime",
    "voice": "Tina",
    "audio": {
      "input": {
        "format": {
          "type": "pcm",
          "sample_rate": 16000
        }
      },
      "output": {
        "format": {
          "type": "wav",
          "sample_rate": 24000
        }
      }
    },
    "instructions": "你是某五星级酒店的AI客服专员，请准确且友好地解答客户关于房型、设施、价格、预订政策的咨询。请始终以专业和乐于助人的态度回应，杜绝提供未经证实或超出酒店服务范围的信息。",
    "turn_detection": {
      "type": "server_vad",
      "threshold": 0.5,
      "silence_duration_ms": 800
    },
    "seed": 1314,
    "max_tokens": 16384,
    "repetition_penalty": 1.05,
    "presence_penalty": 0.0,
    "top_k": 50,
    "top_p": 1.0,
    "temperature": 0.9
  }
}
```

<ParamField body="type" type="string" required>
  事件类型，固定为 `session.update`。
</ParamField>

<ParamField body="session" type="object">
  会话配置。

  <Expandable title="properties">
    <ParamField body="modalities" type="array">
      输出模态。可选值：

      - `["text"]` — 仅文本。
      - `["text", "audio"]`（默认）— 文本和音频。
    </ParamField>

    <ParamField body="voice" type="string">
      音频输出的语音。支持的语音列表请参见 Voice list。各模型默认值：

      - Qwen3.5-Omni-Realtime 系列模型：Tina
      - Qwen3-Omni-Flash-Realtime：Cherry
      - Qwen-Omni-Turbo-Realtime：Chelsie
    </ParamField>

    <ParamField body="audio" type="object">
      输入和输出音频配置。未配置时沿用现有默认行为。适用模型：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`。

      <Expandable title="properties">
        <ParamField body="audio.input" type="object">
          用户输入音频配置。

          <Expandable title="properties">
            <ParamField body="audio.input.format" type="object">
              用户输入音频的格式和采样率。建议在会话 IDLE 阶段（首次发送音频前）完成配置，发送音频后不可再修改。

              <Expandable title="properties">
                <ParamField body="audio.input.format.type" type="string">
                  用户输入音频格式。可选值：`pcm`（默认值，单声道、16 bit 裸 PCM）、`wav`（WAV 容器封装的单声道、16 bit PCM）。
                </ParamField>

                <ParamField body="audio.input.format.sample_rate" type="integer">
                  用户输入音频采样率，单位为 Hz。可选值：`8000`、`16000`（默认值）、`24000`、`48000`。
                </ParamField>
              </Expandable>
            </ParamField>
          </Expandable>
        </ParamField>

        <ParamField body="audio.output" type="object">
          模型输出音频配置。

          <Expandable title="properties">
            <ParamField body="audio.output.format" type="object">
              模型输出音频的格式和采样率。建议在会话建立初期、尚未开始音频交互前完成配置。

              <Expandable title="properties">
                <ParamField body="audio.output.format.type" type="string">
                  模型输出音频格式。可选值：`pcm`（默认值，单声道、16 bit 裸 PCM）、`wav`（WAV 容器封装的单声道、16 bit PCM）。
                </ParamField>

                <ParamField body="audio.output.format.sample_rate" type="integer">
                  模型输出音频采样率，单位为 Hz。可选值：`8000`、`16000`、`24000`（默认值）、`48000`。
                </ParamField>
              </Expandable>
            </ParamField>
          </Expandable>
        </ParamField>
      </Expandable>
    </ParamField>

    <ParamField body="input_audio_format" type="string">
      历史兼容字段，新增接入建议使用 `audio.input.format` 同时配置输入格式和采样率。
    </ParamField>

    <ParamField body="output_audio_format" type="string">
      历史兼容字段，新增接入建议使用 `audio.output.format` 同时配置输出格式和采样率。
    </ParamField>

    <ParamField body="smooth_output" type="boolean | null">
      仅 Qwen3-Omni-Flash-Realtime 支持。控制回复风格：

      - `true`（默认）：口语化风格。
      - `false`：正式书面风格，可能不适合复杂内容。
      - `null`：由模型自动决定。
    </ParamField>

    <ParamField body="instructions" type="string">
      系统消息，用于定义模型的角色或目标。
    </ParamField>

    <ParamField body="turn_detection" type="object">
      语音活动检测（VAD）配置。设为 `null` 可关闭 VAD 并改为手动触发响应。省略此字段则使用默认参数启用 VAD。

      <Expandable title="properties">
        <ParamField body="type" type="string">
          服务端 VAD 类型。可选值：

          - `server_vad`（默认）：基于音频信号检测语音结束。
          - `semantic_vad`：基于语义有效性检测语音结束，可过滤回应语、背景音等无意义声音。仅 Qwen3.5-Omni-Realtime 系列模型支持。
        </ParamField>

        <ParamField body="threshold" type="float">
          VAD 灵敏度。值越低，检测到的声音越多（包括背景噪声）；值越高，需要更清晰的语音。建议取值范围：\[-1.0, 1.0]，默认值：0.5。
        </ParamField>

        <ParamField body="silence_duration_ms" type="integer">
          语音结束后到模型开始响应之间的静音时长（毫秒）。值越低响应越快，但可能在短暂停顿时误触发。建议取值范围：200-6000，默认值：800。
        </ParamField>

        <ParamField body="idle_timeout_ms" type="integer">
          仅适用于 `qwen3.5-omni-plus-realtime` 和 `qwen3.5-omni-flash-realtime` 模型的 `server_vad` 模式。静默超时时间（毫秒）。服务端完成音频播放后，若用户在该时长内保持静默（未触发 `speech.started`），模型会根据当前上下文主动生成响应以引导用户继续对话。超时计时从上一次模型响应音频播放完毕后开始。取值范围：5000-30000。
        </ParamField>
      </Expandable>
    </ParamField>

    <ParamField body="temperature" type="float">
      采样温度，控制输出多样性。值越高输出越多样，值越低越确定。取值范围：\[0, 2)。`temperature` 和 `top_p` 只能设置其中一个。各模型默认值：

      - Qwen3.5-Omni-Realtime 系列模型：0.7
      - qwen3-omni-flash-realtime 模型：0.9
      - qwen-omni-turbo-realtime 模型：1.0

      qwen-omni-turbo 模型会忽略此参数（设置不生效）。
    </ParamField>

    <ParamField body="top_p" type="float">
      核采样阈值，控制输出多样性。值越高输出越多样，值越低越确定。取值范围：(0, 1.0]。`temperature` 和 `top_p` 只能设置其中一个。各模型默认值：

      - Qwen3.5-Omni-Realtime 系列模型：0.8
      - qwen3-omni-flash-realtime 模型：1.0
      - qwen-omni-turbo-realtime 模型：0.01

      qwen-omni-turbo 模型会忽略此参数（设置不生效）。
    </ParamField>

    <ParamField body="top_k" type="integer">
      候选 token 数量。值越高随机性越大，值越低越确定。若为 null 或大于 100，则禁用 top\_k，仅 top\_p 生效。必须 >=0。各模型默认值：

      - Qwen3.5-Omni-Realtime 系列模型：20
      - qwen3-omni-flash-realtime 模型：50
      - qwen-omni-turbo-realtime 模型：20

      qwen-omni-turbo 模型会忽略此参数（设置不生效）。
    </ParamField>

    <ParamField body="max_tokens" type="integer">
      最大返回 token 数。超出此限制时输出会被截断，但不影响生成过程本身。默认值和上限与模型的最大输出长度一致（参见 Model list）。可用于控制字数、成本或延迟。qwen-omni-turbo 模型会忽略此参数（设置不生效）。
    </ParamField>

    <ParamField body="repetition_penalty" type="float">
      连续重复惩罚。值越高重复越少。1.0 表示不惩罚。必须大于 0。各模型默认值：qwen3.5-omni-realtime 模型为 1.0，qwen3-omni-flash-realtime 模型为 1.05。qwen-omni-turbo 模型会忽略此参数（设置不生效）。
    </ParamField>

    <ParamField body="presence_penalty" type="float">
      控制重复度。取值范围：\[-2.0, 2.0]。各模型默认值：qwen3.5-omni-realtime 模型为 1.5，qwen3-omni-flash-realtime 模型为 0.0。正值减少重复，负值增加重复。创意类任务建议用较高值，正式内容建议用较低值。qwen-omni-turbo 模型会忽略此参数（设置不生效）。
    </ParamField>

    <ParamField body="seed" type="integer">
      使输出具有确定性。相同 seed 和参数下，模型返回相同结果。取值范围：0 到 2^31-1，默认值：-1。qwen-omni-turbo 模型会忽略此参数（设置不生效）。
    </ParamField>
  </Expandable>
</ParamField>

## response.create

通知服务端生成模型响应。在 VAD 模式下，响应会自动生成，无需发送此事件。

服务端依次返回 `response.created`、`response.output_item.added`，然后是对话项和内容事件（`conversation.item.created`、`response.content_part.added`），最后是 `response.done`。

```json Example
{
  "type": "response.create",
  "event_id": "event_1718624400000"
}
```

<ParamField body="type" type="string" required>
  事件类型，固定为 `response.create`。
</ParamField>

## response.cancel

取消正在进行的响应。如果当前没有响应在进行，则返回错误。

```json Example
{
  "event_id": "event_B4o9RHSTWobB5OQdEHLTo",
  "type": "response.cancel"
}
```

<ParamField body="type" type="string" required>
  事件类型，固定为 `response.cancel`。
</ParamField>

## input\_audio\_buffer.append

向输入音频缓冲区追加音频数据。

```json Example
{
  "event_id": "event_B4o9RHSTWobB5OQdEHLTo",
  "type": "input_audio_buffer.append",
  "audio": "UklGR..."
}
```

<ParamField body="type" type="string" required>
  事件类型，固定为 `input_audio_buffer.append`。
</ParamField>

<ParamField body="audio" type="string" required>
  Base64 编码的音频数据。
</ParamField>

## input\_audio\_buffer.commit

提交输入音频缓冲区作为用户消息。缓冲区为空时返回错误。

- [VAD 模式](/developer-guides/speech/realtime-multimodal-speech)：自动提交，无需发送此事件。

- [手动模式](/developer-guides/speech/realtime-multimodal-speech)：必须发送此事件来创建用户消息。

提交缓冲区不会触发模型响应。服务端返回 `input_audio_buffer.committed`。

<Note>
  如果之前发送了 `input_image_buffer.append` 事件，`input_audio_buffer.commit` 会同时提交图像缓冲区和音频缓冲区。
</Note>

```json Example
{
  "event_id": "event_B4o9RHSTWobB5OQdEHLTo",
  "type": "input_audio_buffer.commit"
}
```

<ParamField body="type" type="string" required>
  事件类型，固定为 `input_audio_buffer.commit`。
</ParamField>

## input\_audio\_buffer.clear

清空音频缓冲区。服务端返回 `input_audio_buffer.cleared`。

```json Example
{
  "event_id": "event_xxx",
  "type": "input_audio_buffer.clear"
}
```

<ParamField body="type" type="string" required>
  事件类型，固定为 `input_audio_buffer.clear`。
</ParamField>

## input\_image\_buffer.append

将图像数据添加到图像缓冲区，支持本地文件或视频流。

限制：

- 格式：JPG 或 JPEG。推荐 480p 或 720p，最大 1080p。

- 大小：单张图片经 Base64 编码后不得超过 256 KB，建议编码前原始图片不超过 190 KB。

- 编码：Base64。

- 频率：每秒最多 1 张图像。

- 前提：必须先发送至少一个 `input_audio_buffer.append` 事件。

<Note>
  图像缓冲区通过 `input_audio_buffer.commit` 事件与音频缓冲区一起提交。
</Note>

```json Example
{
  "event_id": "event_xxx",
  "type": "input_image_buffer.append",
  "image": "xxx"
}
```

<ParamField body="type" type="string" required>
  事件类型，固定为 `input_image_buffer.append`。
</ParamField>

<ParamField body="image" type="string" required>
  Base64 编码的图像数据。
</ParamField>
