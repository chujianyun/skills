> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 非实时语音合成 Qwen-Audio-TTS/CosyVoice Python SDK

> Qwen-Audio-TTS/CosyVoice 非实时语音合成 Python SDK 参考，支持非流式和流式两种调用模式。

本文介绍非实时语音合成 Qwen-Audio-TTS/CosyVoice 的 Python SDK 调用方法，支持非流式和流式两种调用模式。

**用户指南**：参见[非实时语音合成](/developer-guides/speech/tts)。

<Warning>
  该功能仅支持非实时调用，不支持 WebSocket 实时流式调用。如需实时合成，请使用 [CosyVoice WebSocket API](/api-reference/speech-synthesis/cosyvoice/websocket-api)。
</Warning>

## 前提条件

- 已[获取 API Key](/api-reference/preparation/api-key) 并将其[配置到环境变量](/api-reference/preparation/export-api-key-env)
- 已安装 DashScope Python SDK，建议[安装最新版](/api-reference/preparation/install-sdk)，SDK 版本需 ≥ 1.25.17

## HttpSpeechSynthesizer 类

**包路径**：`dashscope.audio.http_tts.http_speech_synthesizer.HttpSpeechSynthesizer`

**功能**：基于 HTTP 的语音合成，通过 `stream` 参数控制非流式或流式调用模式。

### call() - 语音合成调用

**方法签名**：

```python
@classmethod
def call(cls, model: str, text: str, voice: str,
         format: str = "wav", sample_rate: int = 24000,
         volume: int = 50, rate: float = 1.0, pitch: float = 1.0,
         bit_rate: int = 32, enable_ssml: bool = False,
         word_timestamp_enabled: bool = False,
         seed: int = 0, language_hints: list = None,
         instruction: str = None,
         enable_aigc_tag: bool = False,
         aigc_propagator: str = None,
         aigc_propagate_id: str = None,
         hot_fix: dict = None,
         enable_markdown_filter: bool = False,
         stream: bool = False,
         api_key: str = None, **kwargs)
```

**参数说明**：

| 参数                       | 类型    | 必填 | 说明                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------------ | ----- | -- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| model                    | str   | 是  | 语音合成模型。可选值：`qwen-audio-3.0-tts-plus`、`qwen-audio-3.0-tts-flash`、`cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`、`cosyvoice-v3-plus`、`cosyvoice-v3-flash`、`cosyvoice-v2`                                                                                                                                                                                                             |
| text                     | str   | 是  | 待合成文本。支持 [SSML](/developer-guides/speech/ssml) 和 [LaTeX](/developer-guides/speech/ssml#latex-公式转语音) 格式输入。使用 SSML 时需设置 `enable_ssml=True`；使用 LaTeX 时无需额外配置                                                                                                                                                                                                                        |
| voice                    | str   | 是  | 音色。可选值：系统音色（参见[Qwen-Audio-TTS音色列表](/api-reference/speech-synthesis/qwen-audio-tts/voice-list)、[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)）、声音复刻音色、声音设计音色（创建方法参见 [CosyVoice 声音复刻/设计 API](/api-reference/speech-synthesis/voice-cloning/create-voice)）                                                                                                   |
| format                   | str   | 否  | 音频编码格式。默认值：`mp3`。可选值：`mp3`、`pcm`、`wav`、`opus`                                                                                                                                                                                                                                                                                                                                    |
| sample\_rate             | int   | 否  | 音频采样率（Hz）。可选值：8000、16000、22050（默认）、24000、44100、48000                                                                                                                                                                                                                                                                                                                             |
| volume                   | int   | 否  | 音量。默认值：`50`。取值范围：\[0, 100]                                                                                                                                                                                                                                                                                                                                                       |
| rate                     | float | 否  | 语速。默认值：`1.0`。取值范围：\[0.5, 2.0]                                                                                                                                                                                                                                                                                                                                                    |
| pitch                    | float | 否  | 音调。默认值：`1.0`。取值范围：\[0.5, 2.0]                                                                                                                                                                                                                                                                                                                                                    |
| bit\_rate                | int   | 否  | 音频码率（kbps）。默认值：`32`。取值范围：\[6, 510]。仅在 `format` 为 `opus` 时支持                                                                                                                                                                                                                                                                                                                      |
| enable\_ssml             | bool  | 否  | 是否开启 SSML 功能。当 `text` 使用 SSML 格式时需设为 `True`。默认为 `False`。仅 CosyVoice 系列模型支持，qwen-audio-3.0-tts-plus 和 qwen-audio-3.0-tts-flash 不支持                                                                                                                                                                                                                                                |
| word\_timestamp\_enabled | bool  | 否  | 是否开启字级别时间戳。默认值：`False`。仅在流式输出模式下可用。支持的音色范围：cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash、cosyvoice-v3-plus和cosyvoice-v2模型的复刻音色，以及[Qwen-Audio-TTS音色列表](/api-reference/speech-synthesis/qwen-audio-tts/voice-list)、[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)中标记为支持的系统音色。qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash及其他模型的复刻音色不支持此功能 |
| seed                     | int   | 否  | 随机数种子，用于复现相同合成结果。默认值：`0`。取值范围：\[0, 65535]                                                                                                                                                                                                                                                                                                                                        |
| language\_hints          | list  | 否  | 指定语音合成的目标语言，提升合成效果。可选值：`zh`、`en`、`fr`、`de`、`ja`、`ko`、`ru`、`pt`、`th`、`id`、`vi`、`es`、`it`、`ms`、`fil`、`ar`。当前版本仅处理第一个元素，建议只传入一个值                                                                                                                                                                                                                                                    |
| instruction              | str   | 否  | 设置指令，用于控制方言、情感或角色等合成效果。具体用法请参见[非实时语音合成](/developer-guides/speech/tts)                                                                                                                                                                                                                                                                                                            |
| enable\_aigc\_tag        | bool  | 否  | 是否在生成的音频中添加 AIGC 隐性标识。默认值：`False`。仅 qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2 支持                                                                                                                                                                                                                                        |
| aigc\_propagator         | str   | 否  | 设置 AIGC 隐性标识中的 `ContentPropagator` 字段。仅在 `enable_aigc_tag` 为 `True` 时生效。默认值：阿里云 UID                                                                                                                                                                                                                                                                                              |
| aigc\_propagate\_id      | str   | 否  | 设置 AIGC 隐性标识中的 `PropagateID` 字段。仅在 `enable_aigc_tag` 为 `True` 时生效。默认值：本次请求的 Request ID                                                                                                                                                                                                                                                                                           |
| hot\_fix                 | dict  | 否  | 文本热修复配置，用于自定义指定词语的发音或文本替换。qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、cosyvoice-v2 不支持。详见 [HTTP API hot\_fix 参数](/api-reference/speech-synthesis/cosyvoice/websocket-api#hot_fix)                                                                                                                                                                                           |
| enable\_markdown\_filter | bool  | 否  | 是否启用 Markdown 过滤。启用后系统自动过滤 Markdown 标记符号。默认值：`False`。仅 cosyvoice-v3-flash 复刻音色支持                                                                                                                                                                                                                                                                                                 |
| stream                   | bool  | 否  | 是否启用流式模式。`False`=非流式，返回包含音频 URL 的结果对象；`True`=流式，返回音频数据分片的迭代器。默认为 `False`                                                                                                                                                                                                                                                                                                         |
| api\_key                 | str   | 否  | API Key。未指定时从环境变量 `DASHSCOPE_API_KEY` 读取                                                                                                                                                                                                                                                                                                                                         |

**返回值**：

- **非流式模式**（`stream=False`）：返回结果对象，包含：
  - `audio_url`：音频下载 URL（有效期有限）
  - `audio_id`：音频 ID
  - `expires_at`：URL 过期时间

- **流式模式**（`stream=True`）：返回迭代器，每个元素包含：
  - `audio_data`：当前分片的音频二进制数据（bytes）
  - `sentences`：句子级别的合成信息（如有）

<Warning>
  流式模式下，迭代器的最后一个元素除了包含音频数据分片外，还会额外返回 `audio_url`（完整音频的下载地址）。如果在拼接音频数据时不跳过该元素，会导致音频内容重复播放。遍历迭代器时，需通过 `not chunk.audio_url` 条件过滤最后一个元素。
</Warning>

## 示例代码

以下示例展示 Qwen-Audio-TTS/CosyVoice 语音合成的非流式和流式调用方式。运行前请确保已设置环境变量 `DASHSCOPE_API_KEY`。

<Warning>
  不同模型版本需使用对应版本的音色。例如 `qwen-audio-3.0-tts-flash` 和 `qwen-audio-3.0-tts-plus` 使用 `longanlingxi` 等音色，`cosyvoice-v3-flash` 和 `cosyvoice-v3-plus` 使用 `longanhuan` 等音色，`cosyvoice-v2` 使用 `longxiaochun_v2` 等音色。更换模型时请同步更换为对应版本的音色。具体的模型与音色对应关系，请参见[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)。
</Warning>

### 非流式调用

非流式调用设置 `stream=False`，等待合成完成后返回音频 URL，通过 URL 下载音频文件。

```python
# -*- coding: utf-8 -*-
import os
from dashscope.audio.http_tts.http_speech_synthesizer import HttpSpeechSynthesizer

api_key = os.getenv("DASHSCOPE_API_KEY")

result = HttpSpeechSynthesizer.call(
  model="cosyvoice-v3-flash",
  text="今天是个好日子，适合构建人们喜爱的产品！",
  voice="longanhuan",
  format="wav",
  sample_rate=24000,
  stream=False,
  api_key=api_key,
)

print(f"音频 URL: {result.audio_url}")
print(f"音频 ID: {result.audio_id}")
if result.audio_id:
  request_id = result.audio_id.removeprefix("audio_")
  print(f"请求 Id: {request_id}")
print(f"过期时间: {result.expires_at}")
```

### 流式调用

流式调用设置 `stream=True`，返回迭代器，逐段获取音频数据。适用于对首包延迟有要求的实时播放场景。

```python
# -*- coding: utf-8 -*-
import os
from dashscope.audio.http_tts.http_speech_synthesizer import HttpSpeechSynthesizer

api_key = os.getenv("DASHSCOPE_API_KEY")

stream_result = HttpSpeechSynthesizer.call(
  model="cosyvoice-v3-flash",
  text="今天是个好日子，适合构建人们喜爱的产品！",
  voice="longanhuan",
  format="wav",
  sample_rate=24000,
  stream=True,
  api_key=api_key,
)

audio_chunks = []
for chunk in stream_result:
  if not chunk.audio_url and chunk.audio_data:
    audio_chunks.append(chunk.audio_data)
    print(f"收到音频数据块，大小: {len(chunk.audio_data)} bytes")
  if chunk.sentences:
    print(f"句子信息: {chunk.sentences}")
  if chunk.audio_id:
    print(f"Audio ID: {chunk.audio_id}")
    request_id = chunk.audio_id.removeprefix("audio_")
    print(f"请求 Id: {request_id}")

full_audio = b"".join(audio_chunks)
print(f"总音频大小: {len(full_audio)} bytes")
with open("output.wav", "wb") as f:
  f.write(full_audio)
print("音频已保存到 output.wav")
```
