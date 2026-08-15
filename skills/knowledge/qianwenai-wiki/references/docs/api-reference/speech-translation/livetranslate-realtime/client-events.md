> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# LiveTranslate client events

> WebSocket 客户端事件参考

客户端通过 WebSocket 向服务端发送的事件。

<Note>参考：[语音翻译](/developer-guides/speech/realtime-translation)。</Note>

## Connect

建立 WebSocket 连接以启动会话。连接就绪后，服务端会发送 `session.created` 事件。

| 配置项  | 值                                                 |
| ---- | ------------------------------------------------- |
| 端点   | `wss://dashscope.aliyuncs.com/api-ws/v1/realtime` |
| 查询参数 | `model=qwen3.5-livetranslate-flash-realtime`      |
| 鉴权头  | `Authorization: Bearer $DASHSCOPE_API_KEY`        |
| 协议   | JSON 文本帧                                          |

完整 URL：

```
wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=qwen3.5-livetranslate-flash-realtime
```

## session.update

连接建立后更新会话配置。服务端会校验参数并返回完整配置；如果参数无效则返回错误。

```json Example
{
  "event_id": "event_ToPZqeobitzUJnt3QqtWg",
  "type": "session.update",
  "session": {
    "modalities": [
      "text",
      "audio"
    ],
    "voice": "Tina",
    "sample_rate": 16000,
    "input_audio_format": "pcm",
    "output_audio_format": "pcm",
    "input_audio_transcription": {
      "model": "qwen3-asr-flash-realtime",
      "language": "zh"
    },
    "translation": {
      "language": "en"
    }
  }
}
```

启用声音复刻（`frequency=once`）的示例：

```json Example (voice clone)
{
  "event_id": "event_ToPZqeobitzUJnt3QqtWg",
  "type": "session.update",
  "session": {
    "modalities": [
      "text",
      "audio"
    ],
    "voice": "default",
    "enable_voice_clone": true,
    "voice_clone_options": {
      "frequency": "once"
    },
    "sample_rate": 16000,
    "input_audio_format": "pcm",
    "output_audio_format": "pcm",
    "translation": {
      "language": "en"
    }
  }
}
```

源语种和目标语种均为英语，并跳过文本和音频输出的示例：

```json Example (same-language skip)
{
  "event_id": "event_xxx",
  "type": "session.update",
  "session": {
    "input_audio_transcription": {
      "language": "en"
    },
    "translation": {
      "language": "en",
      "same_language_skip_options": {
        "skip_text": true,
        "skip_audio": true
      }
    }
  }
}
```

<ParamField body="type" type="string" required>
  固定为 `"session.update"`。
</ParamField>

<ParamField body="session" type="object">
  会话配置。

  <Expandable title="properties">
    <ParamField body="modalities" type="array">
      输出类型。可选值：

      - `["text"]` — 仅文本。
      - `["text", "audio"]`（默认）— 文本和音频。
    </ParamField>

    <ParamField body="voice" type="string">
      生成音频的音色。未启用声音复刻时，可设置为系统预设音色，参见[支持的音色](/developer-guides/speech/realtime-translation#支持的音色)。Qwen3.5-LiveTranslate-Flash-Realtime 默认音色为 `Tina`，Qwen3-LiveTranslate-Flash-Realtime 默认音色为 `Cherry`。

      启用声音复刻（`enable_voice_clone` 为 `true`）时，`voice` 的取值取决于 `frequency`：当 `frequency` 为 `once` 或 `always` 时，必须设置为 `default`；当 `frequency` 为 `never` 时，设置为用户预先复刻的音色 ID。
    </ParamField>

    <ParamField body="enable_voice_clone" type="boolean">
      是否启用声音复刻。默认值为 `false`。启用后，模型会基于输入音频复刻音色用于翻译输出，此时 `voice` 不再使用系统预设音色，需设置为 `default` 或用户预先复刻的音色 ID。
    </ParamField>

    <ParamField body="voice_clone_options" type="object">
      声音复刻控制参数，仅在 `enable_voice_clone` 为 `true` 时生效。

      <Expandable title="properties">
        <ParamField body="frequency" type="string">
          音色复刻频率。可选值：

          - `never` — 不在服务端进行音色复刻，使用用户预先复刻好的音色。此时 `voice` 需设置为用户的复刻音色 ID。
          - `once` — 会话开始时基于输入音频进行一次音色复刻，后续输出复用该音色。适合单人演讲场景。此时 `voice` 需设置为 `default`。
          - `always` — 每次输出前基于输入音频进行实时音色复刻，音色跟随输入动态变化。适合多人对话场景。此时 `voice` 需设置为 `default`。
        </ParamField>
      </Expandable>
    </ParamField>

    <ParamField body="sample_rate" type="integer">
      输入音频的采样率，单位为 Hz。可选值：`8000`、`16000`（默认）。
    </ParamField>

    <ParamField body="input_audio_transcription" type="object">
      输入音频设置。

      <Expandable title="properties">
        <ParamField body="model" type="string">
          语音识别模型，默认值为 `qwen3-asr-flash-realtime`，ASR 默认启用。服务端会在翻译的同时返回输入音频的语音识别结果（源语言原文），通过 `conversation.item.input_audio_transcription.text` 和 `conversation.item.input_audio_transcription.completed` 事件返回。如需关闭 ASR，请将此参数显式设置为 `null`。

          可选值：`qwen3-asr-flash-realtime`（默认，启用 ASR）、`null`（关闭 ASR）。
        </ParamField>

        <ParamField body="language" type="string">
          源语言。参见[支持的语种](/developer-guides/speech/realtime-translation#支持的语种)。默认不填写，此时模型会自动识别源语种。
        </ParamField>
      </Expandable>
    </ParamField>

    <ParamField body="input_audio_format" type="string">
      输入音频格式。可选值：

      - `pcm`（默认）— 未压缩的原始音频数据。
      - `opus` — 有损压缩音频编码，支持低延迟传输，适用于网络语音场景。
    </ParamField>

    <ParamField body="output_audio_format" type="string">
      输出音频格式。当前仅支持设为 `pcm`。
    </ParamField>

    <ParamField body="turn_detection" type="object">
      语音活动检测（VAD，Voice Activity Detection）配置，用于控制语音起止的检测方式：

      - 设为配置对象（默认值）：启用 VAD 模式。服务端自动检测语音起止，自动提交音频缓冲区并触发翻译响应，客户端无需发送 `input_audio_buffer.commit` 事件。
      - 设为 `null`：启用 Manual 模式。由客户端通过 `input_audio_buffer.commit` 事件手动提交音频缓冲区，服务端收到后自动开始生成翻译响应。

      <Expandable title="properties">
        <ParamField body="type" type="string">
          VAD 类型，固定为 `server_vad`。
        </ParamField>

        <ParamField body="threshold" type="float">
          VAD 检测灵敏度。值越低，越容易将微弱声音（包括背景噪音）识别为语音；值越高，需要更清晰、音量更大的语音才能触发。取值范围：`[-1.0, 1.0]`，默认值为 `0.2`。
        </ParamField>

        <ParamField body="silence_duration_ms" type="integer">
          语音结束后需保持静音的最短时长（毫秒）。超过该时长后判定语音结束，服务端自动提交音频缓冲区并触发翻译响应。取值范围：`[200, 6000]`，默认值为 `1000`。
        </ParamField>
      </Expandable>
    </ParamField>

    <ParamField body="translation" type="object">
      翻译设置。

      <Expandable title="properties">
        <ParamField body="language" type="string">
          目标语言。参见[支持的语种](/developer-guides/speech/realtime-translation#支持的语种)。默认值：`en`。
        </ParamField>

        <ParamField body="corpus" type="object">
          热词配置，用于提升特定词汇的翻译准确性。

          <Expandable title="properties">
            <ParamField body="phrases" type="object">
              热词映射表。key 为源语言词汇，value 为目标语言对应翻译。示例：`{"人工智能": "Artificial Intelligence"}`。
            </ParamField>
          </Expandable>
        </ParamField>

        <ParamField body="same_language_skip_options" type="object">
          同语种输出配置。当源语种与目标语种相同时，可跳过文本输出、音频输出或两者。仅当 `translation.language` 为 `zh` 或 `en` 时生效。

          <Expandable title="properties">
            <ParamField body="skip_text" type="boolean">
              是否在源语种与目标语种相同时跳过文本输出。
            </ParamField>

            <ParamField body="skip_audio" type="boolean">
              是否在源语种与目标语种相同时跳过音频输出。
            </ParamField>
          </Expandable>
        </ParamField>
      </Expandable>
    </ParamField>
  </Expandable>
</ParamField>

## input\_audio\_buffer.append

向输入缓冲区追加音频数据。服务端使用该缓冲区进行语音检测和提交时机判断。

```json Example
{
  "event_id": "event_xxx",
  "type": "input_audio_buffer.append",
  "audio": "xxx"
}
```

<ParamField body="type" type="string" required>
  固定为 `"input_audio_buffer.append"`。
</ParamField>

<ParamField body="audio" type="string" required>
  Base64 编码的音频数据。
</ParamField>

## input\_image\_buffer.append

从本地文件或实时视频流添加图像数据到缓冲区。

图像限制：

- 格式：JPG 或 JPEG。推荐分辨率：480p 或 720p。最大：1080p。
- 最大文件大小：500 KB（Base64 编码前）。
- 必须进行 Base64 编码。
- 最大速率：每秒 2 张图像。
- 建议先发送至少一个 `input_audio_buffer.append` 事件，以确保服务端有音频上下文。

```json Example
{
  "event_id": "event_xxx",
  "type": "input_image_buffer.append",
  "image": "xxx"
}
```

<ParamField body="type" type="string" required>
  固定为 `"input_image_buffer.append"`。
</ParamField>

<ParamField body="image" type="string" required>
  Base64 编码的图像数据。
</ParamField>

## input\_audio\_buffer.commit

提交输入音频缓冲区。仅在 Manual 模式（`turn_detection` 设为 `null`）下需要发送此事件；VAD 模式下服务端会自动提交，客户端无需发送。

服务端收到该事件后，会返回 `input_audio_buffer.committed` 事件确认，并自动开始生成翻译响应（无需再发送其他事件触发响应）。若音频缓冲区为空，服务端将返回错误事件。

```json Example
{
  "event_id": "event_xxx",
  "type": "input_audio_buffer.commit"
}
```

<ParamField body="type" type="string" required>
  固定为 `"input_audio_buffer.commit"`。
</ParamField>

## input\_audio\_buffer.clear

清空输入音频缓冲区中尚未提交的音频数据。

```json Example
{
  "event_id": "event_xxx",
  "type": "input_audio_buffer.clear"
}
```

<ParamField body="type" type="string" required>
  固定为 `"input_audio_buffer.clear"`。
</ParamField>

## session.finish

结束会话。服务端根据是否检测到语音做出不同响应：

- **检测到语音**： 服务端完成识别，先发送 [conversation.item.input\_audio\_transcription.completed](/api-reference/speech-translation/livetranslate-realtime/server-events) 返回结果，再发送 [session.finished](/api-reference/speech-translation/livetranslate-realtime/server-events)。
- **未检测到语音**： 服务端直接发送 [session.finished](/api-reference/speech-translation/livetranslate-realtime/server-events)。

收到 `session.finished` 后断开连接。

```json Example
{
  "event_id": "event_xxx",
  "type": "session.finish"
}
```

<ParamField body="type" type="string" required>
  固定为 `"session.finish"`。
</ParamField>
