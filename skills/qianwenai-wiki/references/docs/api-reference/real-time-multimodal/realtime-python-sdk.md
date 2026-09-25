> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Qwen-Omni Python SDK

> Qwen-Omni-Realtime Python SDK 接口参考

本文介绍 [Qwen-Omni-Realtime](/developer-guides/speech/realtime-multimodal-speech) DashScope Python SDK 的核心接口和请求参数。

## 快速开始

需要 DashScope Python SDK 1.26.5 或更高版本。教程、示例代码和交互模式详解请参见[实时多模态语音](/developer-guides/speech/realtime-multimodal-speech)。

## 请求参数

通过 `OmniRealtimeConversation` 类的构造方法（`__init__`）设置以下请求参数。

| 参数       | 类型                                                 | 说明                                                             |
| -------- | -------------------------------------------------- | -------------------------------------------------------------- |
| model    | str                                                | Qwen-Omni 模型名称。参见[模型列表](/developer-guides/speech/s2s-models)。  |
| callback | [OmniRealtimeCallback](#回调接口-omnirealtimecallback) | 处理服务端事件的回调对象实例。                                                |
| url      | str                                                | 端点 URL，默认值为 `wss://dashscope.aliyuncs.com/api-ws/v1/realtime`。 |

通过 `update_session` 方法配置以下请求参数。

| 参数                                     | 类型                   | 说明                                                                                                                                                                                                                      |
| -------------------------------------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| output\_modalities                     | list\[MultiModality] | 模型输出模态。设为 `[MultiModality.TEXT]` 仅输出文本，设为 `[MultiModality.TEXT, MultiModality.AUDIO]` 同时输出文本和音频。                                                                                                                        |
| voice                                  | str                  | 模型生成音频的音色。支持的音色列表参见[音色列表](/developer-guides/speech/realtime-multimodal-speech#音色列表)。默认音色：Qwen3.5-Omni-Realtime 系列模型：`"Tina"`，Qwen3-Omni-Flash-Realtime：`"Cherry"`，Qwen-Omni-Turbo-Realtime：`"Chelsie"`。                 |
| input\_audio\_config                   | AudioFormatConfig    | 用户输入音频格式配置。通过 `AudioFormatConfig` 同时设置格式（`type`：`pcm`/`wav`）和采样率（`sample_rate`：`8000`/`16000`/`24000`/`48000`，默认 16000 Hz）。**适用模型：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`。**                         |
| output\_audio\_config                  | AudioFormatConfig    | 模型输出音频格式配置。通过 `AudioFormatConfig` 同时设置格式（`type`：`pcm`/`wav`）和采样率（`sample_rate`：`8000`/`16000`/`24000`/`48000`，默认 24000 Hz）。**适用模型：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`。**                         |
| input\_audio\_format                   | AudioFormat          | 历史兼容字段，新增接入建议使用 `input_audio_config` 同时配置输入格式和采样率。                                                                                                                                                                      |
| output\_audio\_format                  | AudioFormat          | 历史兼容字段，新增接入建议使用 `output_audio_config` 同时配置输出格式和采样率。                                                                                                                                                                     |
| smooth\_output                         | bool                 | 仅 Qwen3-Omni-Flash-Realtime 系列模型支持。`True`：生成口语化的回复。`False`：生成更正式的书面风格回复（内容难以朗读时可能导致质量下降）。`None`：模型自动选择回复风格。                                                                                                             |
| instructions                           | str                  | 系统消息，用于设定模型的目标或角色。例如："你是一家五星级酒店的 AI 助手，负责回答客户关于房型、设施、价格和预订政策的问题。"                                                                                                                                                       |
| enable\_input\_audio\_transcription    | bool                 | 是否启用输入音频的语音识别。                                                                                                                                                                                                          |
| input\_audio\_transcription\_model     | str                  | 用于转写输入音频的语音识别模型。当前仅支持 `gummy-realtime-v1`。                                                                                                                                                                              |
| enable\_turn\_detection                | bool                 | 是否启用语音活动检测（VAD）。禁用时，需手动提交音频来触发模型响应。                                                                                                                                                                                     |
| turn\_detection\_type                  | str                  | 服务端语音活动检测（VAD）类型，固定为 `server_vad`。                                                                                                                                                                                      |
| turn\_detection\_threshold             | float                | VAD 检测阈值。噪声环境下应增大此值，安静环境下应减小此值。值越接近 -1，噪声越容易被识别为语音；值越接近 1，噪声越不容易被识别为语音。默认值：0.2。取值范围：\[-1.0, 1.0]。                                                                                                                       |
| turn\_detection\_silence\_duration\_ms | int                  | 标识说话结束的静默时长。超过此时长后，模型触发响应。默认值：800。取值范围：\[200, 6000]。                                                                                                                                                                    |
| turn\_detection\_param                 | dict                 | VAD 扩展参数字典，用于传入 `turn_detection` 的额外配置项。当前支持传入 `idle_timeout_ms`（int）：静默超时时间（毫秒）。仅在使用 `qwen3.5-omni-plus-realtime` 或 `qwen3.5-omni-flash-realtime` 模型且 VAD 类型为 `server_vad` 时生效。服务端完成音频响应后，在该时长内未收到新的用户音频输入，将自动触发一次空响应。 |
| temperature                            | float                | 采样温度，控制内容多样性。值越大多样性越高，值越小确定性越强。取值范围：\[0, 2)。`temperature` 和 `top_p` 都控制内容多样性，只需设置其中一个。默认值：`Qwen3.5-Omni-Realtime` 系列模型：0.7，`Qwen3-Omni-Flash-Realtime` 系列：0.9，`Qwen-Omni-Turbo-Realtime` 系列：1.0。                        |
| top\_p                                 | float                | 核采样概率阈值，控制内容多样性。值越大多样性越高，值越小确定性越强。取值范围：(0, 1.0]。`temperature` 和 `top_p` 都控制内容多样性，只需设置其中一个。默认值：`Qwen3.5-Omni-Realtime` 系列模型：0.8，`Qwen3-Omni-Flash-Realtime` 系列：1.0，`Qwen-Omni-Turbo-Realtime` 系列：0.01。                   |
| top\_k                                 | integer              | 生成时采样候选集的大小。值越大随机性越高，值越小确定性越强。设为 `None` 或大于 100 的值时不启用 `top_k` 策略，仅 `top_p` 策略生效。值必须大于等于 0。默认值：`Qwen3.5-Omni-Realtime` 系列模型：20，`Qwen3-Omni-Flash-Realtime` 系列：50，`Qwen-Omni-Turbo-Realtime` 系列：20。                      |
| max\_tokens                            | integer              | 当前请求返回的最大 Token 数。此参数不影响模型生成，当输出超过 `max_tokens` 时返回截断内容。默认值和最大值为模型的最大输出长度。`max_tokens` 适用于需要限制字数、控制成本或减少响应时间的场景。                                                                                                        |
| repetition\_penalty                    | float                | 模型生成时连续序列的重复惩罚程度。值越大重复越少，1.0 表示不惩罚。值必须大于 0。默认值：`Qwen3.5-Omni-Realtime` 系列模型：1.0，`Qwen3-Omni-Flash-Realtime` 系列：1.05。                                                                                                    |
| presence\_penalty                      | float                | 控制模型生成内容的重复程度。取值范围：\[-2.0, 2.0]。正值减少重复，负值增加重复。较高的值适用于创意写作或头脑风暴，较低的值适用于技术文档或正式文档。默认值：`Qwen3.5-Omni-Realtime` 系列模型：1.5，`Qwen3-Omni-Flash-Realtime` 系列：0.0。                                                                |
| seed                                   | integer              | 使模型生成更具确定性，确保多次运行得到一致结果。传入相同的 seed 值且其他参数不变时，模型尽量返回相同结果。取值范围：0 到 2^31-1。默认值：-1。                                                                                                                                         |

<Note>
  `qwen-omni-turbo-realtime` 模型不支持修改 `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty` 和 `seed`。
</Note>

## 核心接口

### OmniRealtimeConversation 类

通过 `from dashscope.audio.qwen_omni import OmniRealtimeConversation` 导入 `OmniRealtimeConversation` 类。

#### connect

```python
def connect(self) -> None
```

与服务端建立连接。

**服务端响应事件**：[session.created](/api-reference/real-time-multimodal/server-events#session-created)（会话已创建）、[session.updated](/api-reference/real-time-multimodal/server-events#session-updated)（会话配置已更新）。

#### update\_session

```python
def update_session(self,
                   output_modalities: list[MultiModality],
                   voice: str,
                   input_audio_format: AudioFormat = AudioFormat.PCM_16000HZ_MONO_16BIT,
                   output_audio_format: AudioFormat = AudioFormat.PCM_24000HZ_MONO_16BIT,
                   enable_input_audio_transcription: bool = True,
                   input_audio_transcription_model: str = None,
                   enable_turn_detection: bool = True,
                   turn_detection_type: str = 'server_vad',
                   prefix_padding_ms: int = 300,
                   turn_detection_threshold: float = 0.2,
                   turn_detection_silence_duration_ms: int = 800,
                   turn_detection_param: dict = None,
                   **kwargs) -> None
```

更新会话配置。建立连接后，服务端返回默认配置，应立即调用此方法覆盖默认值。服务端会验证参数，参数无效时返回错误。参数设置详见[请求参数](#请求参数)部分。

**服务端响应事件**：[session.updated](/api-reference/real-time-multimodal/server-events#session-updated)（会话配置已更新）。

#### append\_audio

```python
def append_audio(self, audio_b64: str) -> None
```

将 Base64 编码的音频追加到云端输入缓冲区（临时存储，待后续提交）。

- 启用 `turn_detection` 时，音频缓冲区用于语音检测，由服务端决定何时提交。
- 禁用 `turn_detection` 时，客户端可自行决定每次事件中放入的音频量，最大 15 MiB。以较小的数据块流式传输可以提高 VAD 的响应速度。

**服务端响应事件**：无。

#### append\_video

```python
def append_video(self, video_b64: str) -> None
```

将 Base64 编码的图像数据添加到云端视频缓冲区（本地或实时流）。

图像输入有以下限制：

- 图像格式必须为 JPG 或 JPEG。推荐分辨率为 480p 或 720p，最高不超过 1080p。
- 单张图片经 Base64 编码后不得超过 256 KB，建议编码前原始图片大小不超过 190 KB。
- 图像数据必须经过 Base64 编码。
- 以每秒 1 张的频率向服务端发送图像。

**服务端响应事件**：无。

#### clear\_appended\_audio

```python
def clear_appended_audio(self) -> None
```

清除云端缓冲区中的音频。

**服务端响应事件**：[input\_audio\_buffer.cleared](/api-reference/real-time-multimodal/server-events#input-audio-buffer-cleared)（清除服务端已接收的音频）。

#### commit

```python
def commit(self) -> None
```

提交通过 `append_audio` 和 `append_video` 添加的音频和视频。缓冲区为空时返回错误。

- 启用 `turn_detection` 时，客户端无需发送此事件，服务端自动提交音频缓冲区。
- 禁用 `turn_detection` 时，客户端必须手动提交音频缓冲区以创建用户消息项。

<Warning>
  1. 如果会话配置了 `input_audio_transcription`，系统会转写音频。
  2. 提交输入音频缓冲区不会触发模型生成响应。
</Warning>

**服务端响应事件**：[input\_audio\_buffer.committed](/api-reference/real-time-multimodal/server-events#input-audio-buffer-committed)（服务端已接收提交的音频）。

#### create\_response

```python
def create_response(self,
                    instructions: str = None,
                    output_modalities: list[MultiModality] = None) -> None
```

指示服务端创建模型响应（启用 `turn_detection` 时自动触发）。

**服务端响应事件**：[response.created](/api-reference/real-time-multimodal/server-events#response-created)、[response.output\_item.added](/api-reference/real-time-multimodal/server-events#response-output-item-added)、[conversation.item.created](/api-reference/real-time-multimodal/server-events#conversation-item-created)、[response.content\_part.added](/api-reference/real-time-multimodal/server-events#response-content-part-added)、[response.audio\_transcript.delta](/api-reference/real-time-multimodal/server-events#response-audio-transcript-delta)、[response.audio.delta](/api-reference/real-time-multimodal/server-events#response-audio-delta)、[response.audio\_transcript.done](/api-reference/real-time-multimodal/server-events#response-audio-transcript-done)、[response.audio.done](/api-reference/real-time-multimodal/server-events#response-audio-done)、[response.content\_part.done](/api-reference/real-time-multimodal/server-events#response-content-part-done)、[response.output\_item.done](/api-reference/real-time-multimodal/server-events#response-output-item-done)、[response.done](/api-reference/real-time-multimodal/server-events#response-done)。

#### cancel\_response

```python
def cancel_response(self) -> None
```

取消正在进行的响应（无进行中的响应时返回错误）。

**服务端响应事件**：无。

#### close

```python
def close(self) -> None
```

终止任务并关闭连接。

**服务端响应事件**：无。

#### get\_session\_id

```python
def get_session_id(self) -> str
```

获取当前任务的 `session_id`。

**服务端响应事件**：无。

#### get\_last\_response\_id

```python
def get_last_response_id(self) -> str
```

获取上一次响应的 `response_id`。

**服务端响应事件**：无。

#### get\_last\_first\_text\_delay

```python
def get_last_first_text_delay(self)
```

获取上一次响应的首包文本延迟。

**服务端响应事件**：无。

#### get\_last\_first\_audio\_delay

```python
def get_last_first_audio_delay(self)
```

获取上一次响应的首包音频延迟。

**服务端响应事件**：无。

### 回调接口 (OmniRealtimeCallback)

服务端通过回调返回事件和数据。实现回调方法以处理服务端响应。

通过 `from dashscope.audio.qwen_omni import OmniRealtimeCallback` 导入该接口。

| 方法                                             | 参数                                                              | 返回值 | 说明                                                                                |
| ---------------------------------------------- | --------------------------------------------------------------- | --- | --------------------------------------------------------------------------------- |
| `on_open(self)`                                | 无                                                               | 无   | 连接建立后立即调用。                                                                        |
| `on_event(self, message: str)`                 | `message`：服务端响应事件。                                              | 无   | 处理接口调用响应和模型生成的文本/音频。参见[服务端事件](/api-reference/real-time-multimodal/server-events)。 |
| `on_close(self, close_status_code, close_msg)` | `close_status_code`：WebSocket 关闭状态码。`close_msg`：WebSocket 关闭消息。 | 无   | 连接关闭后调用。                                                                          |
