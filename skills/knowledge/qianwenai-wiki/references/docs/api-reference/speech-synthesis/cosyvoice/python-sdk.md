> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 实时语音合成 Qwen-Audio-TTS/CosyVoice Python SDK

> Qwen-Audio-TTS/CosyVoice 实时语音合成 Python SDK 参考文档

**使用指南**： 模型概览和音色选择请参见[语音合成模型](/developer-guides/speech/tts-models)。

## 服务端点

SDK 默认服务端点为 `wss://dashscope.aliyuncs.com/api-ws/v1/inference`。如需修改，可在初始化前设置 `dashscope.base_websocket_api_url`。

## 文本与格式限制

### 文本长度限制

- [非流式](#非流式)和[单向流式](#单向流式)：单次请求最多 20,000 字符。
- [双向流式](#双向流式)：单次请求最多 20,000 字符，累计不超过 200,000 字符。

### 字符计数规则

- 中文字符（简体/繁体、日文汉字、韩文汉字）计为 2 个字符，其他字符（标点、字母、数字、假名、韩文字母）计为 1 个字符。
- SSML 标签不计入字符数。
- 示例：
  - `"你好"` → 2（中文字符）+ 2（中文字符）= 4 个字符
  - `"中A文123"` → 2（中文字符）+ 1（A）+ 2（中文字符）+ 1（1）+ 1（2）+ 1（3）= 8 个字符
  - `"中文。"` → 2（中文字符）+ 2（中文字符）+ 1（。）= 5 个字符
  - `"中 文。"` → 2（中文字符）+ 1（空格）+ 2（中文字符）+ 1（。）= 6 个字符
  - `"<speak>你好</speak>"` → 2（中文字符）+ 2（中文字符）= 4 个字符

### 编码格式

使用 UTF-8 编码。

### 数学表达式支持

cosyvoice-v3-flash 和 cosyvoice-v3-plus 支持数学表达式解析（基本运算、代数、几何），适用于中小学数学表达式。

<Note>
  该功能仅支持中文。
</Note>

详见 [LaTeX 公式转语音（仅中文）](/developer-guides/speech/ssml#latex-公式转语音)。

### [SSML](/developer-guides/speech/ssml) 支持

cosyvoice-v3-flash 和 v3-plus 的自定义音色（声音设计/克隆）以及[Qwen-Audio-TTS音色列表](/api-reference/speech-synthesis/qwen-audio-tts/voice-list)、[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)中标注支持的系统音色均可使用 [SSML](/developer-guides/speech/ssml)。

- 需要 [DashScope SDK](/api-reference/preparation/install-sdk) 1.23.4 或更高版本。
- 支持的调用方式：[非流式](#非流式)和[单向流式](#单向流式)（仅 `call` 方法）。不支持[双向流式](#双向流式)（`streaming_call`）。
- 将 SSML 文本传入 `call` 方法即可，用法与普通文本相同。

## 快速开始

[SpeechSynthesizer](#speechsynthesizer-类) 类支持三种调用方式：

- **非流式**：阻塞调用。发送完整文本，返回完整音频。适合短文本。
- **单向流式**：非阻塞。发送完整文本，通过回调接收音频。适合对延迟敏感的短文本场景。
- **双向流式**：非阻塞。增量发送文本片段，通过回调实时接收音频。适合对延迟敏感的长文本场景。

三种方式的完整代码示例请参见[实时语音合成](/developer-guides/speech/realtime-streaming)。

### 非流式

一次性发送完整文本，无需回调。返回完整音频数据。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9332072771/CAEQUxiBgIDPub6m4hkiIGMwYWZjOGRmODQ1YTQ3ZmU5YzkzYjM0ZGVhNWIwNGUw4709861_20241015153444.149.svg)

使用[请求参数](#请求参数)实例化 [SpeechSynthesizer](#speechsynthesizer-类)，然后调用 `call` 获取二进制音频数据。

单次最多 20,000 字符（详见 [SpeechSynthesizer](#speechsynthesizer-类) 的 `call` 方法）。

<Warning>
  每次调用 `call` 前，必须重新初始化 `SpeechSynthesizer` 实例。
</Warning>

### 单向流式

发送完整文本，通过 `ResultCallback` 流式接收音频，实时获取合成结果。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9332072771/CAEQUxiBgMC23sGm4hkiIDdkY2FhYzg1MDVlYzRhMzRiZWRiM2JmMTZkNGI5NjI44709861_20241015153444.149.svg)

使用[请求参数](#请求参数)和[回调接口（ResultCallback）](#回调接口-resultcallback)实例化 [SpeechSynthesizer](#speechsynthesizer-类)，然后调用 `call`。通过 `on_data` 回调接收结果。

单次最多 20,000 字符（详见 [SpeechSynthesizer](#speechsynthesizer-类) 的 `call` 方法）。

<Warning>
  每次调用 `call` 前，必须重新初始化 `SpeechSynthesizer` 实例。
</Warning>

### 双向流式

在单个任务中分多次提交文本，通过回调实时接收合成结果。

<Note>
  - 多次调用 `streaming_call` 按顺序提交文本片段。服务端自动断句：

    - 完整句子：立即合成
    - 不完整句子：缓存等待补全后再合成

    调用 `streaming_complete` 可强制合成所有剩余片段。

  - 片段提交间隔不超过 23 秒（服务端固定超时，不可配置）。超时会抛出 "request timeout after 23 seconds" 错误。文本发送完毕后应立即调用 `streaming_complete`。
</Note>

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9332072771/CAEQUxiBgMDY1qPC4hkiIDlmZDQ0MjEyN2MxYzQxYzg5YTQ1ZTkzZjc5YjFkMmI04709861_20241015153444.149.svg)

<Steps>
  <Step title="实例化 SpeechSynthesizer">
    使用[请求参数](#请求参数)和[回调接口（ResultCallback）](#回调接口-resultcallback)实例化 [SpeechSynthesizer](#speechsynthesizer-类)。
  </Step>

  <Step title="流式发送文本">
    多次调用 `streaming_call` 提交文本片段，服务端通过 `on_data` 回调实时返回音频。

    每个片段不超过 20,000 字符，累计不超过 200,000 字符。
  </Step>

  <Step title="完成合成">
    调用 `streaming_complete` 结束合成。该方法会阻塞直到 `on_complete` 或 `on_error` 触发。

    必须调用此方法，否则末尾文本可能无法转为语音。
  </Step>
</Steps>

## 请求参数

通过 [SpeechSynthesizer](#speechsynthesizer-类) 构造函数设置参数。

| 参数                       | 类型             | 必选 | 说明                                                                                                                                                                                                                                                                                                                                         |
| ------------------------ | -------------- | -- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| model                    | str            | 是  | [语音合成模型](/developer-guides/speech/tts-models)。所有可选值参见[Qwen-Audio-TTS音色列表](/api-reference/speech-synthesis/qwen-audio-tts/voice-list)、[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)。                                                                                                                                |
| voice                    | str            | 是  | 合成音色。可用的系统音色参见[Qwen-Audio-TTS音色列表](/api-reference/speech-synthesis/qwen-audio-tts/voice-list)、[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)。                                                                                                                                                                       |
| format                   | enum           | 否  | 音频格式和采样率。默认：MP3，22.05 kHz。<br /><br />**说明**： 默认采样率是所选音色的最佳值。支持降采样和升采样。<br /><br />所有模型支持 WAV、MP3 和 PCM，采样率可选 8/16/22.05/24/44.1/48 kHz。OPUS（OGG\_OPUS）支持 8/16/24/48 kHz，可配置比特率（需 SDK 1.24.0+）。详见[格式参考](#格式参考)。                                                                                                                            |
| volume                   | int            | 否  | 音量。默认：50。范围：\[0, 100]。线性缩放（0 = 静音，50 = 默认，100 = 最大）。<br /><br />**注意**： SDK 1.20.10 及以上版本字段名为 `volume`。                                                                                                                                                                                                                                    |
| speech\_rate             | float          | 否  | 语速。默认：1.0。范围：\[0.5, 2.0]。小于 1.0 减慢语速，大于 1.0 加快语速。                                                                                                                                                                                                                                                                                          |
| pitch\_rate              | float          | 否  | 音调倍率。音调倍率与感知音高之间是非线性关系，建议通过测试确定合适的值。默认：1.0。范围：\[0.5, 2.0]。>1.0 = 音调升高，\<1.0 = 音调降低。                                                                                                                                                                                                                                                        |
| bit\_rate                | int            | 否  | 音频比特率，单位 kbps。MP3 或 Opus 格式可通过 `bit_rate` 调整。默认：32。范围：\[6, 510]。通过 `additional_params` 设置（见下方示例）。                                                                                                                                                                                                                                          |
| word\_timestamp\_enabled | bool           | 否  | 启用字级时间戳。默认：False。适用于 cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash、cosyvoice-v3-plus 和 cosyvoice-v2 模型的复刻音色，以及[Qwen-Audio-TTS音色列表](/api-reference/speech-synthesis/qwen-audio-tts/voice-list)、[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)中标注支持的系统音色。时间戳仅通过回调接口获取。通过 `additional_params` 设置（见下方示例）。 |
| seed                     | int            | 否  | 随机种子。不同种子产生不同结果。模型、文本、音色和其他参数相同时，相同种子可复现相同输出。默认：0。范围：\[0, 65535]。                                                                                                                                                                                                                                                                          |
| language\_hints          | list\[str]     | 否  | 目标语言。可选值：zh、en、fr、de、ja、ko、ru、pt、th、id、vi、es、it、ms、fil、ar。数组参数，仅使用第一个元素。                                                                                                                                                                                                                                                                   |
| instruction              | str            | 否  | 控制方言、情感或说话风格。仅适用于[Qwen-Audio-TTS音色列表](/api-reference/speech-synthesis/qwen-audio-tts/voice-list)、[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)中标注支持 Instruct 的系统音色。**最大长度**：100 字符。详见 [instruction 示例](#instruction-示例)。                                                                                           |
| enable\_aigc\_tag        | bool           | 否  | 为生成的音频添加不可见的 AIGC 标识。设为 True 时，标识嵌入支持的格式（WAV、MP3、OPUS）。默认：False。支持 qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2。通过 `additional_params` 设置（见下方示例）。                                                                                                                                    |
| aigc\_propagator         | str            | 否  | 设置 AIGC 标识中的 `ContentPropagator` 字段。仅在 `enable_aigc_tag` 为 `True` 时生效。默认：UID。支持 qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2。通过 `additional_params` 设置。                                                                                                                              |
| aigc\_propagate\_id      | str            | 否  | 设置 AIGC 标识中的 `PropagateID` 字段。仅在 `enable_aigc_tag` 为 `True` 时生效。默认：请求 ID。支持 qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2。通过 `additional_params` 设置。                                                                                                                                  |
| hot\_fix                 | dict           | 否  | 文本热修正。自定义特定词语的发音或在合成前替换文本。仅适用于 cosyvoice-v3-flash。详见 [hot\_fix 示例](#hot-fix-示例)。                                                                                                                                                                                                                                                           |
| enable\_markdown\_filter | bool           | 否  | 启用 Markdown 过滤。启用后，合成前会移除输入文本中的 Markdown 符号。仅适用于 cosyvoice-v3-flash。默认：False。通过 `additional_params` 设置。                                                                                                                                                                                                                                    |
| callback                 | ResultCallback | 否  | [回调接口（ResultCallback）](#回调接口-resultcallback)。                                                                                                                                                                                                                                                                                              |

### `additional_params` 示例

**设置 `bit_rate`**：

```python
synthesizer = SpeechSynthesizer(
  model="qwen-audio-3.0-tts-flash",
  voice="longanhuan_v3.6",
  format=AudioFormat.OGG_OPUS_16KHZ_MONO_16KBPS,
  additional_params={"bit_rate": 32}
)
```

**设置 `word_timestamp_enabled`**：

```python
synthesizer = SpeechSynthesizer(
  model="qwen-audio-3.0-tts-flash",
  voice="longanhuan_v3.6",
  callback=callback, # 时间戳仅通过回调接口获取
  additional_params={'word_timestamp_enabled': True}
)
```

<Accordion title="查看字级时间戳完整示例代码">
  ```python
  # coding=utf-8

  import os
  import dashscope
  from dashscope.audio.tts_v2 import *
  import json
  from datetime import datetime

  def get_timestamp():
    now = datetime.now()
    formatted_timestamp = now.strftime("[%Y-%m-%d %H:%M:%S.%f]")
    return formatted_timestamp

  # 如果未在环境变量中配置 API Key，请取消注释并替换为实际的 Key
  # dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

  model = "qwen-audio-3.0-tts-flash"
  # 音色
  voice = "longanhuan_v3.6"

  # 定义回调接口
  class Callback(ResultCallback):
    _player = None
    _stream = None

    def on_open(self):
      self.file = open("output.mp3", "wb")
      print("连接已建立：" + get_timestamp())

    def on_complete(self):
      print("语音合成完成，已接收全部结果：" + get_timestamp())

    def on_error(self, message: str):
      print(f"语音合成错误：{message}")

    def on_close(self):
      print("连接已关闭：" + get_timestamp())
      self.file.close()

    def on_event(self, message):
      json_data = json.loads(message)
      if json_data['payload'] and json_data['payload']['output'] and json_data['payload']['output']['sentence']:
        sentence = json_data['payload']['output']['sentence']
        print(f'sentence: {sentence}')
        # 获取句子索引
        # index = sentence['index']
        words = sentence['words']
        if words:
          for word in words:
            print(f'word: {word}')
            # 示例：word: {'text': 'T', 'begin_index': 0, 'end_index': 1, 'begin_time': 80, 'end_time': 200}

    def on_data(self, data: bytes) -> None:
      print(get_timestamp() + " 二进制音频长度：" + str(len(data)))
      self.file.write(data)

  callback = Callback()

  # 实例化 SpeechSynthesizer，通过构造函数传入 model、voice 等请求参数
  synthesizer = SpeechSynthesizer(
    model=model,
    voice=voice,
    callback=callback,
    additional_params={'word_timestamp_enabled': True}
  )

  # 发送文本进行合成，通过回调接口的 on_data 方法实时获取二进制音频
  synthesizer.call("今天天气怎么样？")
  # 首次请求包含 WebSocket 连接建立时间
  print('[Metric] requestId: {}, 首包延迟: {} ms'.format(
    synthesizer.get_last_request_id(),
    synthesizer.get_first_package_delay()))
  ```
</Accordion>

**设置 `enable_aigc_tag`**：

```python
synthesizer = SpeechSynthesizer(
  model="qwen-audio-3.0-tts-flash",
  voice="longanhuan_v3.6",
  format=AudioFormat.OGG_OPUS_16KHZ_MONO_16KBPS,
  additional_params={"enable_aigc_tag": True}
)
```

**设置 `aigc_propagator`**：

```python
synthesizer = SpeechSynthesizer(
  model="qwen-audio-3.0-tts-flash",
  voice="longanhuan_v3.6",
  format=AudioFormat.OGG_OPUS_16KHZ_MONO_16KBPS,
  additional_params={"enable_aigc_tag": True, "aigc_propagator": "xxxx"}
)
```

**设置 `aigc_propagate_id`**：

```python
synthesizer = SpeechSynthesizer(
  model="qwen-audio-3.0-tts-flash",
  voice="longanhuan_v3.6",
  format=AudioFormat.OGG_OPUS_16KHZ_MONO_16KBPS,
  additional_params={"enable_aigc_tag": True, "aigc_propagate_id": "xxxx"}
)
```

**设置 `enable_markdown_filter`**：

```python
synthesizer = SpeechSynthesizer(
  model="cosyvoice-v3-flash",
  voice="longanhuan_v3.6", # 音色
  additional_params={"enable_markdown_filter": True}
)
```

### hot\_fix 示例

```python
synthesizer = SpeechSynthesizer(
  model="cosyvoice-v3-flash",
  voice="longanhuan_v3.6", # 音色
  hot_fix={
    "pronunciation": [{"weather": "tian1 qi4"}],
    "replace": [{"today": "jin1 tian1"}]
  }
)
```

### Instruction 示例

<Tabs>
  <Tab title="cosyvoice-v3-flash（克隆音色）">
    使用任意自然语言指令控制合成效果。

    ```plaintext
    请用粤语说话。（支持的方言：粤语、东北话、甘肃话、贵州话、河南话、湖北话、江西话、闽南话、宁夏话、山西话、陕西话、山东话、上海话、四川话、天津话、云南话。）
    请尽量大声地说一句话。
    请尽量慢地说一句话。
    请尽量快地说一句话。
    请非常轻柔地说一句话。
    你能说慢一点吗？
    你能说得非常快吗？
    你能说得非常慢吗？
    你能说快一点吗？
    请非常愤怒地说一句话。
    请非常开心地说一句话。
    请非常恐惧地说一句话。
    请非常悲伤地说一句话。
    请非常惊讶地说一句话。
    请尽量坚定地说话。
    请尽量愤怒地说话。
    请用亲切的语气说话。
    请用冷淡的语气说话。
    请用威严的语气说话。
    我想听自然的语气。
    我想听你表达威胁。
    我想听你表达智慧。
    我想听你表达诱惑。
    我想听你活泼地说话。
    我想听你充满激情地说话。
    我想听你沉稳地说话。
    我想听你自信地说话。
    你能用兴奋的语气和我说话吗？
    你能展示一下傲慢的情绪吗？
    你能展示一下优雅的情绪吗？
    你能开心地回答问题吗？
    你能展示一下温柔的情绪吗？
    你能用平静的语气和我说话吗？
    你能用深沉的方式回答我吗？
    你能用粗犷的态度和我说话吗？
    用阴森的声音告诉我答案。
    用坚韧的声音告诉我答案。
    用自然亲切的聊天风格来叙述。
    用广播剧播客的语气说话。
    ```
  </Tab>

  <Tab title="cosyvoice-v3-flash（系统音色）">
    使用[Qwen-Audio-TTS音色列表](/api-reference/speech-synthesis/qwen-audio-tts/voice-list)、[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)中指定的固定格式。
  </Tab>
</Tabs>

### 格式参考

所有模型支持以下格式和采样率：

- `AudioFormat.WAV_8000HZ_MONO_16BIT`：WAV 格式，8 kHz 采样率
- `AudioFormat.WAV_16000HZ_MONO_16BIT`：WAV 格式，16 kHz 采样率
- `AudioFormat.WAV_22050HZ_MONO_16BIT`：WAV 格式，22.05 kHz 采样率
- `AudioFormat.WAV_24000HZ_MONO_16BIT`：WAV 格式，24 kHz 采样率
- `AudioFormat.WAV_44100HZ_MONO_16BIT`：WAV 格式，44.1 kHz 采样率
- `AudioFormat.WAV_48000HZ_MONO_16BIT`：WAV 格式，48 kHz 采样率
- `AudioFormat.MP3_8000HZ_MONO_128KBPS`：MP3 格式，8 kHz 采样率
- `AudioFormat.MP3_16000HZ_MONO_128KBPS`：MP3 格式，16 kHz 采样率
- `AudioFormat.MP3_22050HZ_MONO_256KBPS`：MP3 格式，22.05 kHz 采样率
- `AudioFormat.MP3_24000HZ_MONO_256KBPS`：MP3 格式，24 kHz 采样率
- `AudioFormat.MP3_44100HZ_MONO_256KBPS`：MP3 格式，44.1 kHz 采样率
- `AudioFormat.MP3_48000HZ_MONO_256KBPS`：MP3 格式，48 kHz 采样率
- `AudioFormat.PCM_8000HZ_MONO_16BIT`：PCM 格式，8 kHz 采样率
- `AudioFormat.PCM_16000HZ_MONO_16BIT`：PCM 格式，16 kHz 采样率
- `AudioFormat.PCM_22050HZ_MONO_16BIT`：PCM 格式，22.05 kHz 采样率
- `AudioFormat.PCM_24000HZ_MONO_16BIT`：PCM 格式，24 kHz 采样率
- `AudioFormat.PCM_44100HZ_MONO_16BIT`：PCM 格式，44.1 kHz 采样率
- `AudioFormat.PCM_48000HZ_MONO_16BIT`：PCM 格式，48 kHz 采样率

OPUS 格式可通过 `bit_rate` 参数调整比特率，需要 DashScope SDK 1.24.0 或更高版本：

- `AudioFormat.OGG_OPUS_8KHZ_MONO_32KBPS`：OPUS 格式，8 kHz 采样率，32 kbps 比特率
- `AudioFormat.OGG_OPUS_16KHZ_MONO_16KBPS`：OPUS 格式，16 kHz 采样率，16 kbps 比特率
- `AudioFormat.OGG_OPUS_16KHZ_MONO_32KBPS`：OPUS 格式，16 kHz 采样率，32 kbps 比特率
- `AudioFormat.OGG_OPUS_16KHZ_MONO_64KBPS`：OPUS 格式，16 kHz 采样率，64 kbps 比特率
- `AudioFormat.OGG_OPUS_24KHZ_MONO_16KBPS`：OPUS 格式，24 kHz 采样率，16 kbps 比特率
- `AudioFormat.OGG_OPUS_24KHZ_MONO_32KBPS`：OPUS 格式，24 kHz 采样率，32 kbps 比特率
- `AudioFormat.OGG_OPUS_24KHZ_MONO_64KBPS`：OPUS 格式，24 kHz 采样率，64 kbps 比特率
- `AudioFormat.OGG_OPUS_48KHZ_MONO_16KBPS`：OPUS 格式，48 kHz 采样率，16 kbps 比特率
- `AudioFormat.OGG_OPUS_48KHZ_MONO_32KBPS`：OPUS 格式，48 kHz 采样率，32 kbps 比特率
- `AudioFormat.OGG_OPUS_48KHZ_MONO_64KBPS`：OPUS 格式，48 kHz 采样率，64 kbps 比特率

## 核心接口

### `SpeechSynthesizer` 类

通过 `from dashscope.audio.tts_v2 import *` 导入 `SpeechSynthesizer`。该类提供语音合成的核心接口。

| 方法                                                                 | 参数                                                                      | 返回值                                        | 说明                                                                                                                                                                                                                                                                        |
| ------------------------------------------------------------------ | ----------------------------------------------------------------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `def call(self, text: str, timeout_millis=None)`                   | `text`：待合成文本。`timeout_millis`：超时时间（毫秒）。未设置或为 0 时无效。                     | 未设置 `ResultCallback` 时返回二进制音频数据；否则返回 None。 | 将文本（纯文本或 [SSML](/developer-guides/speech/ssml)）转为语音。<br /><br />**无回调**：阻塞直到完成，返回二进制音频。详见[非流式](#非流式)。<br /><br />**有回调**：立即返回 None，通过 `on_data` 传递结果。详见[单向流式](#单向流式)。<br /><br />**注意**： 每次调用前必须重新初始化 `SpeechSynthesizer`。                                                |
| `def streaming_call(self, text: str)`                              | `text`：待合成的文本片段                                                         | None                                       | 流式提交文本片段进行合成（不支持 SSML）。可多次调用发送片段。结果通过 [ResultCallback](#回调接口-resultcallback) 的 `on_data` 传递。详见[双向流式](#双向流式)。                                                                                                                                                              |
| `def streaming_complete(self, complete_timeout_millis=600000)`     | `complete_timeout_millis`：等待时间（毫秒）                                      | None                                       | 结束流式合成。阻塞 `complete_timeout_millis` 毫秒直到任务结束。0 = 无限等待。默认：10 分钟。详见[双向流式](#双向流式)。<br /><br />**注意**： 双向流式必须调用此方法，否则可能丢失末尾语音。                                                                                                                                                |
| `def streaming_cancel(self, complete_timeout_millis: int = 10000)` | `complete_timeout_millis`：等待服务端返回 `task-finished` 事件的超时时间（毫秒），默认 10000。 | None                                       | 取消当前轮次的流式语音合成任务。调用后 SDK 立即结束当前任务，可在当前连接上继续发起新的合成任务，无需重新初始化 `SpeechSynthesizer` 实例。需 Python SDK 版本不低于 1.26.4。Qwen-Audio-TTS 系列模型的所有模型都支持该功能，CosyVoice 系列模型仅 v2 及以上版本支持该功能。                                                                                                 |
| `def get_last_request_id(self)`                                    | 无                                                                       | 请求 ID                                      | 获取上一次任务的请求 ID。                                                                                                                                                                                                                                                            |
| `def get_first_package_delay(self)`                                | 无                                                                       | 首包延迟（毫秒）                                   | 获取首包延迟（从发送文本到收到第一个音频包的时间）。需在任务完成后调用。单向流式场景请在 `on_complete` 触发后调用；提前调用可能返回无效值。<br /><br />**影响因素**：WebSocket 连接建立（首次调用）、音色加载、服务负载、网络延迟。<br /><br />**典型范围**：约 500 ms（复用连接/音色），1,500-2,000 ms（首次连接或切换音色）。<br /><br />**持续超过 2,000 ms 时**：1. 高并发场景使用连接池。2. 检查网络质量。3. 避开高峰时段。 |
| `def get_response(self)`                                           | 无                                                                       | 最后一条消息（JSON）                               | 获取最后一条消息，可用于检测任务失败错误。                                                                                                                                                                                                                                                     |

<a id="回调接口-resultcallback" />

### 回调接口（`ResultCallback`）

[单向流式](#单向流式)或[双向流式](#双向流式)模式下，服务端通过回调返回过程信息和数据。实现以下方法来处理服务端响应。

通过 `from dashscope.audio.tts_v2 import *` 导入。

<Accordion title="查看示例">
  ```python
  class Callback(ResultCallback):
    def on_open(self) -> None:
      print('连接成功')

    def on_data(self, data: bytes) -> None:
      # 实现二进制音频数据处理逻辑
      pass

    def on_complete(self) -> None:
      print('合成完成')

    def on_error(self, message) -> None:
      print('错误：', message)

    def on_close(self) -> None:
      print('连接已关闭')

  callback = Callback()
  ```
</Accordion>

| 方法                                         | 参数                        | 返回值 | 说明                                                                                                                                                        |
| ------------------------------------------ | ------------------------- | --- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `def on_open(self) -> None`                | 无                         | 无   | 客户端连接到服务端时触发。                                                                                                                                             |
| `def on_event(self, message: str) -> None` | `message`：服务端消息（JSON 字符串） | 无   | 服务端发送消息时触发。消息包含 `header`（请求信息）和 `payload`（输出信息）。解析 `payload.output` 可获取事件类型、原始文本和句子信息。详见下方 `on_event` 消息中的 output 字段说明。                                   |
| `def on_complete(self) -> None`            | 无                         | 无   | 所有音频数据返回完毕时触发。                                                                                                                                            |
| `def on_error(self, message) -> None`      | `message`：错误信息            | 无   | 发生错误时触发。                                                                                                                                                  |
| `def on_data(self, data: bytes) -> None`   | `data`：二进制音频数据            | 无   | 收到合成音频时触发。将二进制数据拼接为完整文件或使用流式播放器播放。**注意**： 压缩格式（MP3、Opus）需使用流式播放器（FFmpeg、PyAudio、AudioFormat、MediaSource），不可逐帧播放，否则会导致解码失败。写入文件时使用追加模式。WAV 和 MP3 仅首帧包含头信息。 |
| `def on_close(self) -> None`               | 无                         | 无   | 服务端关闭连接时触发。                                                                                                                                               |

### on\_event 消息中的 output 字段

`on_event` 回调接收的 JSON 消息中，`payload.output` 包含合成事件的输出信息，可用于跟踪合成进度和获取逐句信息。

| 字段             | 类型   | 说明                                                                                     |
| -------------- | ---- | -------------------------------------------------------------------------------------- |
| type           | str  | 事件类型。取值为 `sentence-begin`（句子合成开始）、`sentence-synthesis`（句子合成中）或 `sentence-end`（句子合成结束）。 |
| original\_text | str  | 当前句子的原始文本。在 `sentence-begin` 和 `sentence-end` 事件中返回。                                   |
| sentence       | dict | 句子信息。包含 `index`（句子序号）和 `words`（词列表，开启 `word_timestamp_enabled` 时返回时间戳信息）。              |

**消息示例**：

```json
{
  "header": {
    "task_id": "xxx",
    "event": "result-generated",
    "attributes": {}
  },
  "payload": {
    "output": {
      "type": "sentence-begin",
      "original_text": "今天天气怎么样？",
      "sentence": {
        "index": 0,
        "words": []
      }
    }
  }
}
```

**解析示例**：

```python
import json

def on_event(self, message):
  data = json.loads(message)
  output = data.get('payload', {}).get('output', {})
  event_type = output.get('type', '')
  original_text = output.get('original_text', '')
  if event_type:
    print(f'事件类型: {event_type}, 原始文本: {original_text}')
```

## 响应

服务端返回二进制音频数据：

- [非流式](#非流式)：处理 [SpeechSynthesizer](#speechsynthesizer-类) 的 `call` 返回的二进制数据。
- [单向流式](#单向流式)或[双向流式](#双向流式)：处理 [ResultCallback](#回调接口-resultcallback) 的 `on_data` 中的 `data` 参数（bytes）。

## 更多示例

更多示例请参见 [GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo)。
