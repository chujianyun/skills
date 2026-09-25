> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 语音合成 Sambert Python SDK

> 本文介绍语音合成 Sambert Python SDK 的参数和接口细节。

## 前提条件

- 已开通服务并[获取 API Key](/api-reference/preparation/api-key)。请[配置 API Key 到环境变量](/api-reference/preparation/export-api-key-env)，而非硬编码在代码中，防范因代码泄露导致的安全风险。
- [安装最新版 DashScope SDK](/api-reference/preparation/install-sdk)。

## 快速开始

### 非流式调用

不传入 `callback` 参数时，`call` 函数将在语音合成完成后返回所有语音合成结果。

```python
# coding=utf-8
import sys
from dashscope.audio.tts import SpeechSynthesizer

result = SpeechSynthesizer.call(model='sambert-zhichu-v1',
                                text='今天天气怎么样',
                                sample_rate=48000,
                                format='wav')
if result.get_audio_data() is not None:
  with open('output.wav', 'wb') as f:
    f.write(result.get_audio_data())
  print('SUCCESS: get audio data: %dbytes in output.wav' %
        (sys.getsizeof(result.get_audio_data())))
else:
  print('ERROR: response is %s' % (result.get_response()))
```

### 单向流式调用

传入 `callback` 参数时，在语音合成过程中，服务器将回调 `callback` 中对应函数，流式返回语音合成结果。

```python
# coding=utf-8
import sys
from dashscope.api_entities.dashscope_response import SpeechSynthesisResponse
from dashscope.audio.tts import ResultCallback, SpeechSynthesizer, SpeechSynthesisResult

class Callback(ResultCallback):
  def on_open(self):
    print('Speech synthesizer is opened.')

  def on_complete(self):
    print('Speech synthesizer is completed.')

  def on_error(self, response: SpeechSynthesisResponse):
    print('Speech synthesizer failed, response is %s' % (str(response)))

  def on_close(self):
    print('Speech synthesizer is closed.')

  def on_event(self, result: SpeechSynthesisResult):
    if result.get_audio_frame() is not None:
      print('audio result length:', sys.getsizeof(result.get_audio_frame()))
    if result.get_timestamp() is not None:
      print('timestamp result:', str(result.get_timestamp()))

callback = Callback()
SpeechSynthesizer.call(model='sambert-zhichu-v1',
                       text='今天天气怎么样',
                       sample_rate=48000,
                       callback=callback,
                       word_timestamp_enabled=True,
                       phoneme_timestamp_enabled=True)
```

## 请求参数

| 参数                          | 类型             | 默认值   | 是否必须 | 说明                           |
| --------------------------- | -------------- | ----- | ---- | ---------------------------- |
| model                       | str            | -     | 是    | 模型名，参见[模型列表](#模型列表)。         |
| text                        | str            | -     | 是    | 待合成文本。                       |
| format                      | str            | wav   | 否    | 音频格式，支持 `wav`、`mp3`、`pcm` 等。 |
| sample\_rate                | int            | 16000 | 否    | 音频采样率（Hz）。                   |
| volume                      | int            | 50    | 否    | 音量，取值范围 0\~100。              |
| rate                        | float          | 1.0   | 否    | 语速，取值范围 0.5\~2.0。            |
| pitch                       | float          | 1.0   | 否    | 语调，取值范围 0.5\~2.0。            |
| word\_timestamp\_enabled    | bool           | False | 否    | 是否开启字级别时间戳。                  |
| phoneme\_timestamp\_enabled | bool           | False | 否    | 是否开启音素级别时间戳。                 |
| callback                    | ResultCallback | -     | 否    | 回调接口，传入后启用单向流式调用模式。          |

## 关键接口

### SpeechSynthesizer 类

`SpeechSynthesizer` 可以通过 `from dashscope.audio.tts import SpeechSynthesizer` 方式引入。其关键接口如下：

| 接口/方法                                                                                                                                                  | 参数                                                                                                                                                         | 返回值                                                  | 描述                                                                                                                                   |
| ------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `@classmethod`<br />`def call(cls, model: str, text: str, callback: ResultCallback = None, workspace: str = None, **kwargs) -> SpeechSynthesisResult:` | `model`：模型名，参见[模型列表](#模型列表)<br />`text`：待合成文本<br />`callback`：回调接口（ResultCallback）<br />`workspace`：DashScope workspace id<br />`kwargs`：请求参数，如 `format` 等 | 合成结果 `SpeechSynthesisResult`，非流式调用时需要处理该返回，流式调用时不必处理 | 开启语音合成任务。根据是否传入参数 `callback`，有如下两种情况：不传入 `callback` 参数时，`call` 函数将在语音合成完成后返回所有结果；传入 `callback` 参数时，服务器将回调 `callback` 中对应函数，流式返回合成结果。 |

### 回调接口（ResultCallback）

单向流式调用时，服务端会通过回调的方式将关键流程信息和数据返回给客户端。您需要实现回调方法，处理服务端返回的信息或者数据。

```python
class Callback(ResultCallback):
  def on_open(self):
    print('和服务器成功建立连接')

  def on_complete(self):
    print('任务完成')

  def on_error(self, response: SpeechSynthesisResponse):
    print('报错：%s' % (str(response)))

  def on_close(self):
    print('和服务器之间的连接已关闭')

  def on_event(self, result: SpeechSynthesisResult):
    if result.get_audio_frame() is not None:
      print('收到二进制音频数据：', result.get_audio_frame())
    if result.get_timestamp() is not None:
      print('收到时间戳数据：', str(result.get_timestamp()))

callback = Callback()
```

| 接口/方法                                                       | 参数                                         | 返回值 | 描述                     |
| ----------------------------------------------------------- | ------------------------------------------ | --- | ---------------------- |
| `def on_open(self) -> None`                                 | 无                                          | 无   | 当和服务建立连接完成后立刻被回调。      |
| `def on_event(self, result: SpeechSynthesisResult) -> None` | `result`：音频数据和时间戳信息（SpeechSynthesisResult） | 无   | 当服务端返回合成数据时被回调。        |
| `def on_complete(self) -> None`                             | 无                                          | 无   | 当所有合成数据全部返回后被回调。       |
| `def on_error(self, response: SpeechSynthesisResponse)`     | `response`：异常信息                            | 无   | 当调用过程出现异常以及服务返回错误后被回调。 |
| `def on_close(self) -> None`                                | 无                                          | 无   | 服务关闭连接后被回调。            |

## 响应结果

### 音频数据和时间戳信息（SpeechSynthesisResult）

`SpeechSynthesisResult` 封装了语音合成结果，常用的接口为 `get_audio_frame`、`get_timestamp`、`get_audio_data` 和 `get_timestamps`。

| 接口/方法                                              | 参数 | 返回值             | 描述                                                                    |
| -------------------------------------------------- | -- | --------------- | --------------------------------------------------------------------- |
| `def get_audio_frame(self) -> bytes`               | 无  | 当前合成的二进制音频数据片段  | 流式合成中，获取当前合成的音频帧数据。<Note>该函数要在流式合成时，在回调方法 `on_event` 中使用。</Note>      |
| `def get_timestamp(self) -> Dict[str, str]`        | 无  | 当前合成的句子对应的时间戳信息 | 流式合成中，获取当前合成的句子对应的时间戳信息。<Note>该函数要在流式合成时，在回调方法 `on_event` 中使用。</Note> |
| `def get_audio_data(self) -> bytes`                | 无  | 完整的二进制音频数据      | 获取完整的二进制音频数据。                                                         |
| `def get_timestamps(self) -> List[Dict[str, str]]` | 无  | 所有句子对应的时间戳信息    | 获取所有句子对应的时间戳信息。                                                       |

### 时间戳信息

`get_timestamp` 函数获取当前合成句子的时间戳信息，`get_timestamps` 函数获取所有句子的时间戳信息。

单个句子的时间戳信息示例如下，其中 `words` 对应字级别时间戳信息，`phonemes` 对应音素级别时间戳信息：

```json
{
  "begin_time": 0,
  "end_time": 1412,
  "words": [
    {
      "text": "今",
      "begin_time": 0,
      "end_time": 200,
      "phonemes": [
        {"begin_time": 0, "end_time": 82, "text": "j_c", "tone": 1},
        {"begin_time": 82, "end_time": 200, "text": "in_c", "tone": 1}
      ]
    }
  ]
}
```

各参数含义如下：

| 参数          | 类型   | 说明                                                           |
| ----------- | ---- | ------------------------------------------------------------ |
| begin\_time | int  | 句子、字、音素开始时间，单位为 ms。                                          |
| end\_time   | int  | 句子、字、音素结束时间，单位为 ms。                                          |
| words       | list | 字级别时间戳信息，需要请求中 `word_timestamp_enabled` 也设置为 `true`。         |
| text        | str  | 文本信息。                                                        |
| phonemes    | list | 音素级别时间戳信息，需要请求中 `phoneme_timestamp_enabled` 也设置为 `true`。     |
| tone        | str  | 音调。英文中，0、1、2 分别代表轻音、重音和次重音。拼音中，1、2、3、4、5 分别代表一声、二声、三声、四声和轻声。 |

## 错误码

在使用 API 过程中，如果调用失败并返回错误信息，请参见[错误信息](/api-reference/preparation/error-messages)进行解决。

## 更多示例

更多示例，请参见 [GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo)。

## 常见问题

请参见 [GitHub QA](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/docs/QA)。

## 模型列表

| 音色      | model 参数               | 时间戳支持 | 适用场景               | 特色     | 语言    | 默认采样率（Hz） |
| ------- | ---------------------- | ----- | ------------------ | ------ | ----- | --------- |
| 知楠      | sambert-zhinan-v1      | 是     | 通用场景               | 广告男声   | 中文+英文 | 48k       |
| 知琪      | sambert-zhiqi-v1       | 是     | 通用场景               | 温柔女声   | 中文+英文 | 48k       |
| 知厨      | sambert-zhichu-v1      | 是     | 新闻播报               | 舌尖男声   | 中文+英文 | 48k       |
| 知德      | sambert-zhide-v1       | 是     | 新闻播报               | 新闻男声   | 中文+英文 | 48k       |
| 知佳      | sambert-zhijia-v1      | 是     | 新闻播报               | 标准女声   | 中文+英文 | 48k       |
| 知茹      | sambert-zhiru-v1       | 是     | 新闻播报               | 新闻女声   | 中文+英文 | 48k       |
| 知倩      | sambert-zhiqian-v1     | 是     | 配音解说、新闻播报          | 资讯女声   | 中文+英文 | 48k       |
| 知祥      | sambert-zhixiang-v1    | 是     | 配音解说               | 磁性男声   | 中文+英文 | 48k       |
| 知薇      | sambert-zhiwei-v1      | 是     | 阅读产品简介             | 萝莉女声   | 中文+英文 | 48k       |
| 知浩      | sambert-zhihao-v1      | 是     | 通用场景               | 咨询男声   | 中文+英文 | 16k       |
| 知婧      | sambert-zhijing-v1     | 是     | 通用场景               | 严厉女声   | 中文+英文 | 16k       |
| 知茗      | sambert-zhiming-v1     | 是     | 通用场景               | 诙谐男声   | 中文+英文 | 16k       |
| 知墨      | sambert-zhimo-v1       | 是     | 通用场景               | 情感男声   | 中文+英文 | 16k       |
| 知娜      | sambert-zhina-v1       | 是     | 通用场景               | 浙普女声   | 中文+英文 | 16k       |
| 知树      | sambert-zhishu-v1      | 是     | 通用场景               | 资讯男声   | 中文+英文 | 16k       |
| 知莎      | sambert-zhistella-v1   | 是     | 通用场景               | 知性女声   | 中文+英文 | 16k       |
| 知婷      | sambert-zhiting-v1     | 是     | 通用场景               | 电台女声   | 中文+英文 | 16k       |
| 知笑      | sambert-zhixiao-v1     | 是     | 通用场景               | 资讯女声   | 中文+英文 | 16k       |
| 知雅      | sambert-zhiya-v1       | 是     | 通用场景               | 严厉女声   | 中文+英文 | 16k       |
| 知晔      | sambert-zhiye-v1       | 是     | 通用场景               | 青年男声   | 中文+英文 | 16k       |
| 知颖      | sambert-zhiying-v1     | 是     | 通用场景               | 软萌童声   | 中文+英文 | 16k       |
| 知媛      | sambert-zhiyuan-v1     | 是     | 通用场景               | 知心姐姐   | 中文+英文 | 16k       |
| 知悦      | sambert-zhiyue-v1      | 是     | 客服                 | 温柔女声   | 中文+英文 | 16k       |
| 知柜      | sambert-zhigui-v1      | 是     | 阅读产品简介             | 直播女声   | 中文+英文 | 16k       |
| 知硕      | sambert-zhishuo-v1     | 是     | 数字人                | 自然男声   | 中文+英文 | 16k       |
| 知妙（多情感） | sambert-zhimiao-emo-v1 | 是     | 阅读产品简介、数字人、直播      | 多种情感女声 | 中文+英文 | 16k       |
| 知猫      | sambert-zhimao-v1      | 是     | 阅读产品简介、配音解说、数字人、直播 | 直播女声   | 中文+英文 | 16k       |
| 知伦      | sambert-zhilun-v1      | 是     | 配音解说               | 悬疑解说   | 中文+英文 | 16k       |
| 知飞      | sambert-zhifei-v1      | 是     | 配音解说               | 激昂解说   | 中文+英文 | 16k       |
| 知达      | sambert-zhida-v1       | 是     | 新闻播报               | 标准男声   | 中文+英文 | 16k       |
| Camila  | sambert-camila-v1      | 否     | 通用场景               | 西班牙语女声 | 西班牙语  | 16k       |
| Perla   | sambert-perla-v1       | 否     | 通用场景               | 意大利语女声 | 意大利语  | 16k       |
| Indah   | sambert-indah-v1       | 否     | 通用场景               | 印尼语女声  | 印尼语   | 16k       |
| Clara   | sambert-clara-v1       | 否     | 通用场景               | 法语女声   | 法语    | 16k       |
| Hanna   | sambert-hanna-v1       | 否     | 通用场景               | 德语女声   | 德语    | 16k       |
| Beth    | sambert-beth-v1        | 是     | 通用场景               | 咨询女声   | 美式英文  | 16k       |
| Betty   | sambert-betty-v1       | 是     | 通用场景               | 客服女声   | 美式英文  | 16k       |
| Cally   | sambert-cally-v1       | 是     | 通用场景               | 自然女声   | 美式英文  | 16k       |
| Cindy   | sambert-cindy-v1       | 是     | 通用场景               | 对话女声   | 美式英文  | 16k       |
| Eva     | sambert-eva-v1         | 是     | 通用场景               | 陪伴女声   | 美式英文  | 16k       |
| Donna   | sambert-donna-v1       | 是     | 通用场景               | 教育女声   | 美式英文  | 16k       |
| Brian   | sambert-brian-v1       | 是     | 通用场景               | 客服男声   | 美式英文  | 16k       |
| Waan    | sambert-waan-v1        | 否     | 通用场景               | 泰语女声   | 泰语    | 16k       |
