> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# LiveTranslate Python SDK

> LiveTranslate Python SDK 参考文档

通过 DashScope Python SDK 调用 Qwen-LiveTranslate，实现实时语音翻译。

**使用指南**： 教程和完整示例请参见[实时翻译](/developer-guides/speech/realtime-translation)。

## 前提条件

1. [安装SDK](/api-reference/preparation/install-sdk)，确保DashScope SDK版本不低于1.25.6。
2. [获取API Key](/api-reference/preparation/api-key)。

## 请求参数

在 `OmniRealtimeConversation` 构造函数中设置以下参数：

<Accordion title="点击查看示例代码">
  ```python
  from dashscope.audio.qwen_omni import (
    OmniRealtimeConversation,
    OmniRealtimeCallback,
    MultiModality,
  )
  from dashscope.audio.qwen_omni.omni_realtime import TranslationParams

  class MyCallback(OmniRealtimeCallback):
    """实时翻译回调处理器"""
    def __init__(self, conversation=None):
      self.conversation = conversation
      self.handlers = {
        'session.created': self._handle_session_created,
        'response.audio_transcript.done': self._handle_translation_done,
        'response.audio.delta': self._handle_audio_delta,
        'response.done': lambda r: print('======Response Done======'),
        'input_audio_buffer.speech_started': lambda r: print('======Speech Start======'),
        'input_audio_buffer.speech_stopped': lambda r: print('======Speech Stop======'),
      }

    def on_open(self):
      print('Connection opened')

    def on_close(self, code, msg):
      print(f'Connection closed, code: {code}, msg: {msg}')

    def on_event(self, response):
      try:
        handler = self.handlers.get(response['type'])
        if handler:
          handler(response)
      except Exception as e:
        print(f'[Error] {e}')

    def _handle_session_created(self, response):
      print(f"Session created: {response['session']['id']}")

    def _handle_translation_done(self, response):
      print(f"Translation result: {response['transcript']}")

    def _handle_audio_delta(self, response):
      # 处理增量音频数据
      audio_b64 = response.get('delta', '')
      # 解码音频数据，用于播放或保存

  conversation = OmniRealtimeConversation(
    model='qwen3.5-livetranslate-flash-realtime',
    url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime',
    callback=MyCallback(conversation=None)  # 临时传入 None，稍后注入
  )
  # 将 conversation 注入回调对象
  conversation.callback.conversation = conversation
  ```
</Accordion>

| 参数         | 类型                                                   | 必选 | 说明                                                                                           |
| ---------- | ---------------------------------------------------- | -- | -------------------------------------------------------------------------------------------- |
| `model`    | `str`                                                | 是  | 模型名称。推荐使用 `qwen3.5-livetranslate-flash-realtime`。`qwen3-livetranslate-flash-realtime` 为旧版模型。 |
| `callback` | [`OmniRealtimeCallback`](#回调接口-omnirealtimecallback) | 是  | 处理服务端事件的回调对象。                                                                                |
| `url`      | `str`                                                | 否  | 服务端点：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime`。默认为 DashScope 端点。                     |

通过 `OmniRealtimeConversation.update_session` 设置以下参数：

<Accordion title="点击查看示例代码">
  ```python
  # 设置翻译参数
  translation_params = TranslationParams(
    language='en',  # 目标语言
    corpus=TranslationParams.Corpus(
      phrases={
        '人工智能': 'Artificial Intelligence',
        '机器学习': 'Machine Learning'
      }
    )
  )

  # 更新会话配置
  conversation.update_session(
    output_modalities=[MultiModality.TEXT, MultiModality.AUDIO],
    voice='Tina',
    translation_params=translation_params,
  )
  ```
</Accordion>

| 参数                                | 类型                    | 必选 | 说明                                                                                                                                                                                                                       |
| --------------------------------- | --------------------- | -- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `output_modalities`               | `List[MultiModality]` | 否  | 输出类型。默认值：`[MultiModality.TEXT, MultiModality.AUDIO]`。可选值：`[MultiModality.TEXT]`（仅文本）或 `[MultiModality.TEXT, MultiModality.AUDIO]`（文本和音频）。                                                                                |
| `voice`                           | `str`                 | 否  | 音频输出的音色。Qwen3.5-LiveTranslate-Flash-Realtime 默认音色为 `Tina`，Qwen3-LiveTranslate-Flash-Realtime 默认音色为 `Cherry`。参见[支持的音色](/developer-guides/speech/realtime-translation#支持的音色)。                                              |
| `input_audio_transcription_model` | `str`                 | 否  | 设为 `qwen3-asr-flash-realtime` 可获取源语言的语音识别结果。使用时须同时设置 `translation_params`，否则服务端返回参数无效错误。                                                                                                                                 |
| `translation_params`              | `TranslationParams`   | 否  | 翻译设置。                                                                                                                                                                                                                    |
| `enable_turn_detection`           | `bool`                | 否  | 是否启用 VAD（语音活动检测）。默认值：`True`，启用 VAD 模式，服务端自动检测语音起止并自动触发翻译。设为 `False` 切换为 Manual 模式，由客户端通过 `commit` 方法手动提交音频。详细参数说明见[客户端事件](/api-reference/speech-translation/livetranslate-realtime/client-events)中的 `turn_detection` 描述。 |

在 `TranslationParams` 构造函数中设置以下参数：

<Accordion title="点击查看示例代码">
  ```python
  translation_params = TranslationParams(
    language='en',  # 目标语言代码
    corpus=TranslationParams.Corpus(
      phrases={
        '人工智能': 'Artificial Intelligence',  # 源语言词汇: 目标翻译
        '机器学习': 'Machine Learning'
      }
    )
  )
  ```
</Accordion>

| 参数               | 类型                         | 必选 | 说明                                                                              |
| ---------------- | -------------------------- | -- | ------------------------------------------------------------------------------- |
| `language`       | `str`                      | 否  | 目标语言代码。默认值：`en`。参见[支持的语种](/developer-guides/speech/realtime-translation#支持的语种)。 |
| `corpus`         | `TranslationParams.Corpus` | 否  | 热词设置，用于提高特定术语的翻译准确度。                                                            |
| `corpus.phrases` | `dict`                     | 否  | 热词映射（key：源语言术语，value：目标语言翻译）。示例：`{'人工智能': 'Artificial Intelligence'}`           |

## 关键接口

### OmniRealtimeConversation 类

导入方式：`from dashscope.audio.qwen_omni import OmniRealtimeConversation`

| 方法签名                                                                                                                                                   | 服务端事件（通过回调返回）                                                                                                                                                                 | 说明                                                                                       |
| ------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `def connect(self) -> None:`                                                                                                                           | [服务端事件](/api-reference/speech-translation/livetranslate-realtime/server-events)：会话已创建；[服务端事件](/api-reference/speech-translation/livetranslate-realtime/server-events)：会话配置已更新 | 连接服务端。                                                                                   |
| `def update_session(self, output_modalities: List[MultiModality], voice: str = None, translation_params: TranslationParams = None, **kwargs) -> None:` | [服务端事件](/api-reference/speech-translation/livetranslate-realtime/server-events)：会话配置已更新                                                                                       | 更新会话设置。连接后立即调用。未调用时使用默认值。参见 `OmniRealtimeConversation.update_session` 参数。                |
| `def end_session(self, timeout: int = 20) -> None:`                                                                                                    | [session.finished](/api-reference/speech-translation/livetranslate-realtime/server-events)：服务端完成翻译并结束会话                                                                       | 结束会话。服务端会完成剩余翻译后再关闭。                                                                     |
| `def append_audio(self, audio_b64: str) -> None:`                                                                                                      | 无                                                                                                                                                                             | 向输入缓冲区发送 Base64 编码的音频数据。服务端自动检测语音边界并触发翻译。                                                |
| `def commit(self) -> None:`                                                                                                                            | [input\_audio\_buffer.committed](/api-reference/speech-translation/livetranslate-realtime/server-events)：输入音频缓冲区已提交                                                           | Manual 模式下，提交此前通过 `append_audio` 方法追加到云端缓冲区的音频，服务端收到后自动开始生成翻译响应。VAD 模式下无需调用此方法，服务端会自动提交。 |
| `def clear_appended_audio(self) -> None:`                                                                                                              | [input\_audio\_buffer.cleared](/api-reference/speech-translation/livetranslate-realtime/server-events)：输入音频缓冲区已清空                                                             | 清空当前云端缓冲区中尚未提交的音频数据。                                                                     |
| `def close(self) -> None:`                                                                                                                             | 无                                                                                                                                                                             | 停止任务并关闭连接。                                                                               |
| `def get_session_id(self) -> str:`                                                                                                                     | 无                                                                                                                                                                             | 返回当前会话 ID。                                                                               |
| `def get_last_response_id(self) -> str:`                                                                                                               | 无                                                                                                                                                                             | 返回最近一次响应 ID。                                                                             |

### 回调接口 (OmniRealtimeCallback)

服务端通过回调向客户端发送事件。继承此类并实现相应方法来处理事件。

导入方式：`from dashscope.audio.qwen_omni import OmniRealtimeCallback`

| 方法签名                                                        | 参数                                                                                      | 说明                 |
| ----------------------------------------------------------- | --------------------------------------------------------------------------------------- | ------------------ |
| `def on_open(self) -> None:`                                | 无                                                                                       | WebSocket 连接建立时调用。 |
| `def on_event(self, message: dict) -> None:`                | message：[服务端事件](/api-reference/speech-translation/livetranslate-realtime/server-events) | 收到服务端事件时调用。        |
| `def on_close(self, close_status_code, close_msg) -> None:` | close\_status\_code：状态码。close\_msg：日志信息。                                                | WebSocket 连接关闭时调用。 |

## 完整示例

以下示例展示如何从麦克风实时录音并进行翻译。

<Accordion title="麦克风实时翻译示例代码">
  ```python
  import os
  import sys
  import base64
  import signal
  import pyaudio
  from dashscope.audio.qwen_omni import (
    OmniRealtimeConversation,
    OmniRealtimeCallback,
    MultiModality,
  )
  from dashscope.audio.qwen_omni.omni_realtime import TranslationParams

  class Callback(OmniRealtimeCallback):
    """实时翻译回调处理类"""
    def __init__(self, speaker):
      self.speaker = speaker

    def on_open(self):
      print("[连接已建立]")

    def on_close(self, code, msg):
      print(f"[连接已关闭] code: {code}, msg: {msg}")

    def on_event(self, response):
      event_type = response.get("type", "")
      if event_type == "input_audio_buffer.speech_started":
        print("====== 检测到语音输入 ======")
      elif event_type == "input_audio_buffer.speech_stopped":
        print("====== 语音输入结束 ======")
      elif event_type == "conversation.item.input_audio_transcription.completed":
        print(f"[原文] {response.get('transcript', '')}")
      elif event_type == "response.audio_transcript.done":
        print(f"[翻译结果] {response.get('transcript', '')}")
      elif event_type == "response.audio.delta":
        audio_b64 = response.get("delta", "")
        if audio_b64:
          self.speaker.write(base64.b64decode(audio_b64))
      elif event_type == "error":
        print(f"[错误] {response.get('error', {}).get('message', '')}")

  def main():
    if not os.environ.get("DASHSCOPE_API_KEY"):
      print("请设置环境变量 DASHSCOPE_API_KEY")
      sys.exit(1)

    pya = pyaudio.PyAudio()

    speaker = pya.open(
      format=pyaudio.paInt16,
      channels=1,
      rate=24000,
      output=True,
      frames_per_buffer=2400
    )

    mic = pya.open(
      format=pyaudio.paInt16,
      channels=1,
      rate=16000,
      input=True,
      frames_per_buffer=1600
    )

    callback = Callback(speaker=speaker)

    conversation = OmniRealtimeConversation(
      model="qwen3.5-livetranslate-flash-realtime",
      url="wss://dashscope.aliyuncs.com/api-ws/v1/realtime",
      callback=callback
    )

    conversation.connect()

    translation_params = TranslationParams(
      language="en",
      corpus=TranslationParams.Corpus(
        phrases={
          "人工智能": "Artificial Intelligence",
          "机器学习": "Machine Learning"
        }
      )
    )

    conversation.update_session(
      output_modalities=[MultiModality.TEXT, MultiModality.AUDIO],
      input_audio_transcription_model="qwen3-asr-flash-realtime",
      voice="Tina",
      translation_params=translation_params,
    )

    def on_exit(sig, frame):
      print("\n[正在退出...]")
      mic.stop_stream()
      mic.close()
      speaker.stop_stream()
      speaker.close()
      pya.terminate()
      conversation.end_session()
      conversation.close()
      sys.exit(0)

    signal.signal(signal.SIGINT, on_exit)

    print("[开始实时翻译] 请对着麦克风说话，按 Ctrl+C 退出")

    while True:
      audio_data = mic.read(1600, exception_on_overflow=False)
      conversation.append_audio(base64.b64encode(audio_data).decode("ascii"))

  if __name__ == "__main__":
    main()
  ```
</Accordion>
