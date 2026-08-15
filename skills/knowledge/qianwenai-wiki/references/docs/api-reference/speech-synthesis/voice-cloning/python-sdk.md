> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Python SDK

> Qwen-Audio-TTS/CosyVoice 声音复刻 Python SDK 参考（VoiceEnrollmentService）。

通过 DashScope Python SDK 的 `VoiceEnrollmentService` 类调用 Qwen-Audio-TTS/CosyVoice 声音复刻。该 SDK 仅覆盖声音复刻功能，CosyVoice 声音设计以及所有 Qwen 声音复刻/设计请使用 [HTTP API](/api-reference/speech-synthesis/voice-cloning/create-voice)。

**用户指南**：[声音复刻](/developer-guides/speech/voice-cloning)。

## 前提条件

- [API Key](/api-reference/preparation/api-key)，配置为 `DASHSCOPE_API_KEY` 环境变量
- [最新版 DashScope SDK](/api-reference/preparation/install-sdk)

## Service URL

创建服务前设置 base URL：

```python
import dashscope

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
```

## VoiceEnrollmentService 类

**包路径**：`dashscope.audio.tts_v2.VoiceEnrollmentService`

管理 Qwen-Audio-TTS/CosyVoice 克隆音色的完整生命周期（创建、列表、查询、更新、删除）。

### 构造方法

```python
VoiceEnrollmentService()
```

### create\_voice()

从音频创建克隆音色。

```python
def create_voice(self, target_model: str, prefix: str, url: str,
                 **kwargs) -> str
```

| 参数                            | 类型         | 必选 | 说明                                                                                                                                                                                                                       |
| ----------------------------- | ---------- | -- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| target\_model                 | str        | 是  | 克隆音色绑定的语音合成模型。后续合成调用的 model 必须与此一致。                                                                                                                                                                                      |
| prefix                        | str        | 是  | 音色名称前缀，仅限字母和数字，最长 10 个字符。生成的名称格式：`{target_model}-{prefix}-{unique_id}`。                                                                                                                                                  |
| url                           | str        | 是  | 用于克隆的音频文件 URL，必须可公开访问。                                                                                                                                                                                                   |
| language\_hints               | List\[str] | 否  | 音频的语言提示，仅使用第一个元素。默认：`["zh"]`。`qwen-audio-3.0-tts-plus`、`qwen-audio-3.0-tts-flash` 支持的语言：zh（中文）、en（英语）、fr（法语）、de（德语）、ja（日语）、ko（韩语）、ru（俄语）、pt（葡萄牙语）、th（泰语）、id（印尼语）、vi（越南语）、it（意大利语）、es（西班牙语）、ms（马来西亚语）、fil（菲律宾语）、ar（阿拉伯语）。 |
| max\_prompt\_audio\_length    | float      | 否  | 预处理后的最大音频时长（秒）。范围：\[3.0, 30.0]。默认：10.0。                                                                                                                                                                                  |
| enable\_preprocess            | bool       | 否  | 是否启用音频预处理（降噪、增强）。默认：`False`。                                                                                                                                                                                             |
| enable\_volume\_normalization | bool       | 否  | 是否对用于声音复刻的样本音频进行音量归一化。通过关键字参数直接传入。默认：`False`。设置为 `True` 后，使用所创建音色合成的音频，其音量可能与关闭该参数时创建的音色不同。                                                                                                                              |

**返回值**：`str`，生成的音色 ID（`voice_id`）。

<Expandable title="示例">
  ```python
  import dashscope
  from dashscope.audio.tts_v2 import VoiceEnrollmentService

  dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

  service = VoiceEnrollmentService()

  voice_id = service.create_voice(
    target_model="qwen-audio-3.0-tts-flash",
    prefix="myvoice",
    url="https://your-audio-url.wav",
    language_hints=["zh"]
  )

  print(f"Created voice: {voice_id}")
  ```
</Expandable>

### list\_voices()

列出克隆音色，支持前缀过滤和分页。

```python
def list_voices(self, prefix: str = None, page_index: int = 0, page_size: int = 10) -> list
```

| 参数          | 类型  | 必选 | 说明              |
| ----------- | --- | -- | --------------- |
| prefix      | str | 否  | 按名称前缀过滤。        |
| page\_index | int | 否  | 页码，从 0 开始。默认：0。 |
| page\_size  | int | 否  | 每页条数。默认：10。     |

**返回值**：`list`，音色对象列表。

<Expandable title="示例">
  ```python
  service = VoiceEnrollmentService()

  voices = service.list_voices(prefix="myvoice", page_size=10)

  for voice in voices:
    print(voice)
  ```
</Expandable>

### query\_voice()

查询指定克隆音色的详细信息。

```python
def query_voice(self, voice_id: str) -> dict
```

| 参数        | 类型  | 必选 | 说明         |
| --------- | --- | -- | ---------- |
| voice\_id | str | 是  | 要查询的音色 ID。 |

**返回值**：`dict`，包含 `status`、`resource_link`、`target_model` 等信息。

<Expandable title="示例">
  ```python
  service = VoiceEnrollmentService()

  details = service.query_voice(voice_id="qwen-audio-3.0-tts-flash-myvoice-xxxxxx")

  print(f"Status: {details['status']}")
  print(f"Target model: {details['target_model']}")
  ```
</Expandable>

### update\_voice()

用新音频更新已有克隆音色。

```python
def update_voice(self, voice_id: str, url: str,
                 language_hints: List[str] = None,
                 max_prompt_audio_length: float = None,
                 enable_preprocess: bool = None) -> None
```

| 参数                         | 类型         | 必选 | 说明                  |
| -------------------------- | ---------- | -- | ------------------- |
| voice\_id                  | str        | 是  | 要更新的音色 ID。          |
| url                        | str        | 是  | 新的音频文件 URL，必须可公开访问。 |
| language\_hints            | List\[str] | 否  | 新音频的语言提示。           |
| max\_prompt\_audio\_length | float      | 否  | 预处理后的最大音频时长（秒）。     |
| enable\_preprocess         | bool       | 否  | 是否启用音频预处理。          |

**返回值**：`None`

<Expandable title="示例">
  ```python
  service = VoiceEnrollmentService()

  service.update_voice(
    voice_id="qwen-audio-3.0-tts-flash-myvoice-xxxxxx",
    url="https://new-audio-url.wav",
    language_hints=["en"]
  )

  print("Voice updated successfully")
  ```
</Expandable>

### delete\_voice()

删除克隆音色。

```python
def delete_voice(self, voice_id: str) -> None
```

| 参数        | 类型  | 必选 | 说明         |
| --------- | --- | -- | ---------- |
| voice\_id | str | 是  | 要删除的音色 ID。 |

**返回值**：`None`

<Expandable title="示例">
  ```python
  service = VoiceEnrollmentService()

  service.delete_voice(voice_id="qwen-audio-3.0-tts-flash-myvoice-xxxxxx")

  print("Voice deleted successfully")
  ```
</Expandable>

## 完整示例

### 创建音色

```python
import dashscope
from dashscope.audio.tts_v2 import VoiceEnrollmentService

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
TARGET_MODEL = 'qwen-audio-3.0-tts-flash'
voice_prefix = 'myvoice'
url = 'https://your-audio-file-url'

service = VoiceEnrollmentService()

voice_id = service.create_voice(
  target_model=TARGET_MODEL,
  prefix=voice_prefix,
  url=url,
  max_prompt_audio_length=10,
  # enable_preprocess=False,
  # enable_volume_normalization=True
)

print(f"Request ID: {service.get_last_request_id()}")
print(f"Voice ID: {voice_id}")
```

### 查询音色列表

```python
import dashscope
from dashscope.audio.tts_v2 import VoiceEnrollmentService

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

service = VoiceEnrollmentService()

voices = service.list_voices(prefix="myvoice", page_index=0, page_size=10)

print(f"Request ID: {service.get_last_request_id()}")
for voice in voices:
  print(voice)
```

### 查询音色详情

```python
import dashscope
from dashscope.audio.tts_v2 import VoiceEnrollmentService

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

service = VoiceEnrollmentService()

voice_id = 'qwen-audio-3.0-tts-flash-myvoice-xxxxxxxx'
voice_details = service.query_voice(voice_id=voice_id)

print(f"Request ID: {service.get_last_request_id()}")
print(f"Voice Details: {voice_details}")
```

### 更新音色

```python
import dashscope
from dashscope.audio.tts_v2 import VoiceEnrollmentService

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

service = VoiceEnrollmentService()

service.update_voice(
  voice_id='qwen-audio-3.0-tts-flash-myvoice-xxxxxxxx',
  url='https://your-new-audio-file-url'
)

print(f"Update submitted. Request ID: {service.get_last_request_id()}")
```

### 删除音色

```python
import dashscope
from dashscope.audio.tts_v2 import VoiceEnrollmentService

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

service = VoiceEnrollmentService()

service.delete_voice(voice_id='qwen-audio-3.0-tts-flash-myvoice-xxxxxxxx')

print(f"Deletion submitted. Request ID: {service.get_last_request_id()}")
```
