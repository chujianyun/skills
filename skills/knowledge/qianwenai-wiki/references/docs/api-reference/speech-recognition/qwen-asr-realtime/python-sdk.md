> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 实时语音识别（Qwen-ASR-Realtime）Python SDK

> Qwen ASR Python 流式识别

支持的模型、功能和完整示例代码，请参阅[实时语音识别](/developer-guides/speech/asr-realtime)。

## 请求参数

### OmniRealtimeConversation 构造函数

创建 `OmniRealtimeConversation` 实例。

<Accordion title="点击查看示例代码">
  ```python
  from dashscope.audio.qwen_omni import OmniRealtimeConversation, OmniRealtimeCallback

  class MyCallback(OmniRealtimeCallback):
    """实时识别回调"""
    def __init__(self, conversation):
      self.conversation = conversation
      self.handlers = {
        'session.created': self._handle_session_created,
        'conversation.item.input_audio_transcription.completed': self._handle_final_text,
        'conversation.item.input_audio_transcription.text': self._handle_stash_text,
        'input_audio_buffer.speech_started': lambda r: print('======语音开始======'),
        'input_audio_buffer.speech_stopped': lambda r: print('======语音结束======')
      }

    def on_open(self):
      print('连接已打开')

    def on_close(self, code, msg):
      print(f'连接已关闭，状态码: {code}，消息: {msg}')

    def on_event(self, response):
      try:
        handler = self.handlers.get(response['type'])
        if handler:
          handler(response)
      except Exception as e:
        print(f'[Error] {e}')

    def _handle_session_created(self, response):
      print(f"会话已创建: {response['session']['id']}")

    def _handle_final_text(self, response):
      print(f"最终识别文本: {response['transcript']}")

    def _handle_stash_text(self, response):
      print(f"中间识别结果: {response['stash']}")

  conversation = OmniRealtimeConversation(
    model='qwen3-asr-flash-realtime',
    url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime',
    callback=MyCallback(conversation=None)  # 先传 None，之后再注入。
  )
  # 将 conversation 注入回调。
  conversation.callback.conversation = conversation
  ```
</Accordion>

| 参数         | 类型                     | 必选 | 说明                                                                                             |
| ---------- | ---------------------- | -- | ---------------------------------------------------------------------------------------------- |
| `model`    | `str`                  | 是  | 模型名称。                                                                                          |
| `callback` | `OmniRealtimeCallback` | 是  | 处理服务端事件的回调对象。                                                                                  |
| `url`      | `str`                  | 否  | WebSocket 端点。默认值：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime`（SDK 自动附加 `?model={model}`）。 |

### 会话配置

连接成功后，设置会话参数。

<Accordion title="点击查看示例代码">
  ```python
  from dashscope.audio.qwen_omni import MultiModality
  from dashscope.audio.qwen_omni.omni_realtime import TranscriptionParams

  transcription_params = TranscriptionParams(
    language='zh',
    sample_rate=16000,
    input_audio_format="pcm"
  )

  conversation.update_session(
    output_modalities=[MultiModality.TEXT],
    enable_turn_detection=True,
    turn_detection_type="server_vad",
    turn_detection_threshold=0.0,
    turn_detection_silence_duration_ms=400,
    enable_input_audio_transcription=True,
    transcription_params=transcription_params
  )
  ```
</Accordion>

| 参数                                   | 类型                    | 必选 | 说明                                                                                        |
| ------------------------------------ | --------------------- | -- | ----------------------------------------------------------------------------------------- |
| `output_modalities`                  | `List[MultiModality]` | 是  | 输出类型，固定为 `[MultiModality.TEXT]`。                                                          |
| `enable_turn_detection`              | `bool`                | 否  | 启用服务端 VAD。默认值：`True`。设为 `False` 时需手动调用 `commit()` 触发识别。                                   |
| `turn_detection_type`                | `str`                 | 否  | VAD 类型，固定为 `server_vad`。                                                                  |
| `turn_detection_threshold`           | `float`               | 否  | VAD 灵敏度。默认值：`0.2`，建议值：`0.0`，范围：`[-1, 1]`。值越低灵敏度越高，但可能将噪音误判为语音；值越高则减少误触发。                  |
| `turn_detection_silence_duration_ms` | `int`                 | 否  | 判定语句结束的静音时长（毫秒）。默认值：`800`，建议值：`400`，范围：`[200, 6000]`。值越低响应越快，但可能在停顿处截断；值越高可包含更长停顿，但会增加延迟。 |
| `enable_input_audio_transcription`   | `bool`                | 否  | 启用音频转写。默认值：`True`。设为 `False` 时禁用转写。                                                       |
| `transcription_params`               | `TranscriptionParams` | 否  | 识别配置，详见 [TranscriptionParams](#transcriptionparams)。                                      |

### TranscriptionParams

通过 `TranscriptionParams` 设置识别选项。

<Accordion title="点击查看示例代码">
  ```python
  transcription_params = TranscriptionParams(
    language='zh',
    sample_rate=16000,
    input_audio_format="pcm"
  )
  ```
</Accordion>

| 参数                   | 类型               | 必选 | 说明                                                                                                                                                                                                                                                                                                     |
| -------------------- | ---------------- | -- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `language`           | `str`            | 否  | 音频语言。支持的值：`zh`（中文：普通话、四川话、闽南语、吴语）、`yue`（粤语）、`en`（英语）、`ja`（日语）、`ko`（韩语）、`de`（德语）、`fr`（法语）、`es`（西班牙语）、`pt`（葡萄牙语）、`it`（意大利语）、`ru`（俄语）、`ar`（阿拉伯语）、`hi`（印地语）、`id`（印尼语）、`th`（泰语）、`tr`（土耳其语）、`uk`（乌克兰语）、`vi`（越南语）、`cs`（捷克语）、`da`（丹麦语）、`fi`（芬兰语）、`fil`（菲律宾语）、`is`（冰岛语）、`ms`（马来语）、`no`（挪威语）、`pl`（波兰语）、`sv`（瑞典语） |
| `sample_rate`        | `int`            | 否  | 音频采样率（Hz）。默认值：`16000`。支持：`16000`、`8000`。8 kHz 音频会被服务端上采样至 16 kHz，可能增加少许延迟。仅在音频源为 8 kHz（如电话录音）时使用 `8000`。                                                                                                                                                                                               |
| `input_audio_format` | `str`            | 否  | 音频格式。默认值：`pcm`。支持：`pcm`、`opus`。                                                                                                                                                                                                                                                                        |
| `corpus`             | `Dict[str, Any]` | 否  | 热词配置（字典格式）。如需更简便的字符串接口，请使用 `corpus_text`。                                                                                                                                                                                                                                                              |
| `corpus_text`        | `str`            | 否  | 热词参考文本（如专有名词或领域词汇），上限 10,000 个 token。详见[热词](/developer-guides/speech/improve-recognition-accuracy)。                                                                                                                                                                                                    |

## 核心接口

### OmniRealtimeConversation 类

```python
from dashscope.audio.qwen_omni import OmniRealtimeConversation
```

| 方法                               | 服务端响应事件                                                                                                                                                                                                       | 说明                                                                                                                                                                                                    |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `connect()`                      | [`session.created`](/api-reference/speech-recognition/qwen-asr-realtime/server-events#session-created)、[`session.updated`](/api-reference/speech-recognition/qwen-asr-realtime/server-events#session-updated) | 建立 WebSocket 连接。                                                                                                                                                                                      |
| `update_session(...)`            | [`session.updated`](/api-reference/speech-recognition/qwen-asr-realtime/server-events#session-updated)                                                                                                        | 设置会话参数。在 `connect()` 之后调用。不调用则使用默认值。详见[会话配置](#会话配置)。                                                                                                                                                  |
| `append_audio(audio_b64: str)`   | 无                                                                                                                                                                                                             | 向输入缓冲区发送 Base64 编码的音频。当 `enable_turn_detection=True` 时，服务端在语音边界自动提交；为 `False` 时由客户端控制提交。单次事件上限 15 MiB，较小的音频块可提升 VAD 响应速度。                                                                             |
| `commit()`                       | [`input_audio_buffer.committed`](/api-reference/speech-recognition/qwen-asr-realtime/server-events#input-audio-buffer-committed)                                                                              | 提交缓冲区音频进行识别。缓冲区为空时返回错误。`enable_turn_detection=True` 时不可用。                                                                                                                                             |
| `end_session(timeout: int = 20)` | [`session.finished`](/api-reference/speech-recognition/qwen-asr-realtime/server-events#session-finished)                                                                                                      | 等待最后一次识别完成后结束会话。[VAD 模式](/developer-guides/speech/asr-realtime#vad-mode-default)（默认）下在音频发送完毕后调用；[手动模式](/developer-guides/speech/asr-realtime#manual-mode)下在 `commit()` 之后调用。异步版本：`end_session_async`。 |
| `close()`                        | 无                                                                                                                                                                                                             | 停止任务并关闭连接。                                                                                                                                                                                            |
| `get_session_id()`               | 无                                                                                                                                                                                                             | 返回会话 ID。                                                                                                                                                                                              |
| `get_last_response_id()`         | 无                                                                                                                                                                                                             | 返回最近一次响应 ID。                                                                                                                                                                                          |

### OmniRealtimeCallback 接口

继承 `OmniRealtimeCallback` 来处理服务端事件。

```python
from dashscope.audio.qwen_omni import OmniRealtimeCallback
```

| 方法                                       | 参数                                                                                                                    | 说明                 |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ------------------ |
| `on_open()`                              | 无                                                                                                                     | WebSocket 连接建立时调用。 |
| `on_event(message: dict)`                | `message`：一个[服务端事件](/api-reference/speech-recognition/qwen-asr-realtime/server-events)（已解析的 `dict`，无需手动 `json.loads`） | 收到服务端事件时调用。        |
| `on_close(close_status_code, close_msg)` | `close_status_code`：状态码；`close_msg`：日志消息                                                                              | WebSocket 连接关闭时调用。 |
