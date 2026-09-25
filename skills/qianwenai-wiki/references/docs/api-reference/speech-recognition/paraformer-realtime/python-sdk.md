> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Paraformer 实时语音识别 Python SDK

> 本文介绍Paraformer实时语音识别Python SDK的参数和接口细节。

**用户指南**： 关于模型介绍和选型建议，请参见[实时语音识别](/developer-guides/speech/asr-realtime)。

**模型体验**： 仅 paraformer-realtime-v2、paraformer-realtime-8k-v2 支持，可前往[千问AI平台](https://platform.qianwenai.com/home/try-ai)体验。

## 前提条件

- 已开通服务并[获取API Key](/api-reference/preparation/api-key)。请[配置API Key到环境变量](/api-reference/preparation/export-api-key-env)，而非硬编码在代码中，防范因代码泄露导致的安全风险。

  <Note>
    当您需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时鉴权Token](/api-reference/more/generate-a-temporary-api-key)。与长期有效的 API Key 相比，临时鉴权 Token 具备时效性短（60秒）、安全性高的特点，适用于临时调用场景，能有效降低API Key泄露的风险。使用方式：在代码中，将原本用于鉴权的 API Key 替换为获取到的临时鉴权 Token 即可。
  </Note>

- [安装最新版DashScope SDK](/api-reference/preparation/install-sdk)。

## 模型列表

|                 | paraformer-realtime-v2（推荐）                                                             | paraformer-realtime-8k-v2（推荐）                                                          | paraformer-realtime-v1                                                                                   | paraformer-realtime-8k-v1                                                                                |
| --------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **适用场景**        | 直播、会议等场景                                                                               | 电话客服、语音信箱等 8kHz 音频的识别场景                                                                | 直播、会议等场景                                                                                                 | 电话客服、语音信箱等 8kHz 音频的识别场景                                                                                  |
| **采样率**         | 任意                                                                                     | 8kHz                                                                                   | 16kHz                                                                                                    | 8kHz                                                                                                     |
| **语种**          | 中文（含普通话及方言）、英文、日语、韩语、德语、法语、俄语                                                          | 中文                                                                                     | 中文                                                                                                       | 中文                                                                                                       |
| **标点符号预测**      | 默认支持，无需配置                                                                              | 默认支持，无需配置                                                                              | 默认支持，无需配置                                                                                                | 默认支持，无需配置                                                                                                |
| **逆文本正则化（ITN）** | 默认支持，无需配置                                                                              | 默认支持，无需配置                                                                              | 默认支持，无需配置                                                                                                | 默认支持，无需配置                                                                                                |
| **定制热词**        | 支持（通过 `vocabulary_id`，参见[定制热词](/developer-guides/speech/improve-recognition-accuracy)） | 支持（通过 `vocabulary_id`，参见[定制热词](/developer-guides/speech/improve-recognition-accuracy)） | 支持（通过 `phrase_id`，参见[Paraformer语音识别热词定制与管理](/api-reference/speech-recognition/custom-hotwords/http-api)） | 支持（通过 `phrase_id`，参见[Paraformer语音识别热词定制与管理](/api-reference/speech-recognition/custom-hotwords/http-api)） |
| **指定待识别语种**     | 支持（通过 `language_hints` 参数指定）                                                           | 不支持                                                                                    | 不支持                                                                                                      | 不支持                                                                                                      |
| **情感识别**        | 不支持                                                                                    | 支持（须关闭语义断句，通过 `emo_tag` 和 `emo_confidence` 字段获取）                                       | 不支持                                                                                                      | 不支持                                                                                                      |

paraformer-realtime-v2 支持的中文方言：上海话、吴语、闽南语、东北话、甘肃话、贵州话、河南话、湖北话、湖南话、江西话、宁夏话、山西话、陕西话、山东话、四川话、天津话、云南话、粤语。

## 快速开始

Paraformer Python SDK 提供非流式调用和双向流式调用两种接口。请根据实际需求选择合适的调用方式：

- **非流式调用**： 针对本地文件进行识别，并一次性返回完整的处理结果。适合处理录制好的音频。
- **双向流式调用**： 可直接对音频流进行识别，并实时输出结果。音频流可以来自外部设备（如麦克风）或从本地文件读取。适合需要即时反馈的场景。

### 非流式调用

提交单个语音实时转写任务，通过传入本地文件的方式同步阻塞地拿到转写结果。

实例化 [Recognition类](#recognition类) 绑定[请求参数](#请求参数)，调用 `call` 进行识别并最终获取[识别结果（RecognitionResult）](#识别结果-recognitionresult)。

示例中用到的音频为：[asr\_example.wav](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250210/iwaouc/asr_example.wav)。

```python
from http import HTTPStatus
from dashscope.audio.asr import Recognition

# 若没有将API Key配置到环境变量中，需将下面这行代码注释放开，并将apiKey替换为自己的API Key
# import dashscope
# dashscope.api_key = "apiKey"

recognition = Recognition(model='paraformer-realtime-v2',
  format='wav',
  sample_rate=16000,
  # "language_hints"只支持paraformer-realtime-v2模型
  language_hints=['zh', 'en'],
  callback=None)
result = recognition.call('asr_example.wav')
if result.status_code == HTTPStatus.OK:
  print('识别结果：')
  print(result.get_sentence())
else:
  print('Error: ', result.message)

print(
  '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
  .format(
    recognition.get_last_request_id(),
    recognition.get_first_package_delay(),
    recognition.get_last_package_delay(),
  ))
```

### 双向流式调用

提交单个语音实时转写任务，通过实现回调接口的方式流式输出实时识别结果。

**步骤**：

1. **启动流式语音识别** — 实例化 [Recognition类](#recognition类) 绑定[请求参数](#请求参数)和[回调接口（RecognitionCallback）](#回调接口-recognitioncallback)，调用 `start` 方法启动流式语音识别。

2. **流式传输** — 循环调用 [Recognition类](#recognition类) 的 `send_audio_frame` 方法，将从本地文件或设备（如麦克风）读取的二进制音频流分段发送至服务端。在发送音频数据的过程中，服务端会通过[回调接口（RecognitionCallback）](#回调接口-recognitioncallback)的 `on_event` 方法，将识别结果实时返回给客户端。建议每次发送的音频时长约为100毫秒，数据大小保持在1KB至16KB之间。

3. **结束处理** — 调用 [Recognition类](#recognition类) 的 `stop` 方法结束语音识别。该方法会阻塞当前线程，直到[回调接口（RecognitionCallback）](#回调接口-recognitioncallback)的 `on_complete` 或者 `on_error` 回调触发后才会释放线程阻塞。

<CodeGroup>
  ```python 识别传入麦克风的语音
  import os
  import signal  # for keyboard events handling (press "Ctrl+C" to terminate recording)
  import sys

  import dashscope
  import pyaudio
  from dashscope.audio.asr import *

  mic = None
  stream = None

  # Set recording parameters
  sample_rate = 16000  # sampling rate (Hz)
  channels = 1  # mono channel
  dtype = 'int16'  # data type
  format_pcm = 'pcm'  # the format of the audio data
  block_size = 3200  # number of frames per buffer

  def init_dashscope_api_key():
    """
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """
    if 'DASHSCOPE_API_KEY' in os.environ:
      dashscope.api_key = os.environ['DASHSCOPE_API_KEY']
    else:
      dashscope.api_key = 'REDACTED'

  # Real-time speech recognition callback
  class Callback(RecognitionCallback):
    def on_open(self) -> None:
      global mic
      global stream
      print('RecognitionCallback open.')
      mic = pyaudio.PyAudio()
      stream = mic.open(format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True)

    def on_close(self) -> None:
      global mic
      global stream
      print('RecognitionCallback close.')
      stream.stop_stream()
      stream.close()
      mic.terminate()
      stream = None
      mic = None

    def on_complete(self) -> None:
      print('RecognitionCallback completed.')

    def on_error(self, message) -> None:
      print('RecognitionCallback task_id: ', message.request_id)
      print('RecognitionCallback error: ', message.message)
      if 'stream' in globals() and stream.active:
        stream.stop()
        stream.close()
      sys.exit(1)

    def on_event(self, result: RecognitionResult) -> None:
      sentence = result.get_sentence()
      if 'text' in sentence:
        print('RecognitionCallback text: ', sentence['text'])
        if RecognitionResult.is_sentence_end(sentence):
          print(
            'RecognitionCallback sentence end, request_id:%s, usage:%s'
            % (result.get_request_id(), result.get_usage(sentence)))

  def signal_handler(sig, frame):
    print('Ctrl+C pressed, stop recognition ...')
    recognition.stop()
    print('Recognition stopped.')
    print(
      '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
      .format(
        recognition.get_last_request_id(),
        recognition.get_first_package_delay(),
        recognition.get_last_package_delay(),
      ))
    sys.exit(0)

  if __name__ == '__main__':
    init_dashscope_api_key()
    print('Initializing ...')

    callback = Callback()

    recognition = Recognition(
      model='paraformer-realtime-v2',
      format=format_pcm,
      sample_rate=sample_rate,
      semantic_punctuation_enabled=False,
      callback=callback)

    recognition.start()

    signal.signal(signal.SIGINT, signal_handler)
    print("Press 'Ctrl+C' to stop recording and recognition...")

    while True:
      if stream:
        data = stream.read(3200, exception_on_overflow=False)
        recognition.send_audio_frame(data)
      else:
        break

    recognition.stop()
  ```

  ```python 识别本地语音文件
  import os
  import time
  from dashscope.audio.asr import *

  # 若没有将API Key配置到环境变量中，需将下面这行代码注释放开，并将apiKey替换为自己的API Key
  # import dashscope
  # dashscope.api_key = "apiKey"

  from datetime import datetime

  def get_timestamp():
    now = datetime.now()
    formatted_timestamp = now.strftime("[%Y-%m-%d %H:%M:%S.%f]")
    return formatted_timestamp

  class Callback(RecognitionCallback):
    def on_complete(self) -> None:
      print(get_timestamp() + ' Recognition completed')

    def on_error(self, result: RecognitionResult) -> None:
      print('Recognition task_id: ', result.request_id)
      print('Recognition error: ', result.message)
      exit(0)

    def on_event(self, result: RecognitionResult) -> None:
      sentence = result.get_sentence()
      if 'text' in sentence:
        print(get_timestamp() + ' RecognitionCallback text: ', sentence['text'])
        if RecognitionResult.is_sentence_end(sentence):
          print(get_timestamp() +
            'RecognitionCallback sentence end, request_id:%s, usage:%s'
            % (result.get_request_id(), result.get_usage(sentence)))

  callback = Callback()

  recognition = Recognition(model='paraformer-realtime-v2',
    format='wav',
    sample_rate=16000,
    # "language_hints"只支持paraformer-realtime-v2模型
    language_hints=['zh', 'en'],
    callback=callback)

  recognition.start()

  try:
    audio_data: bytes = None
    f = open("asr_example.wav", 'rb')
    if os.path.getsize("asr_example.wav"):
      while True:
        audio_data = f.read(3200)
        if not audio_data:
          break
        else:
          recognition.send_audio_frame(audio_data)
        time.sleep(0.1)
    else:
      raise Exception('The supplied file was empty (zero bytes long)')
    f.close()
  except Exception as e:
    raise e

  recognition.stop()

  print(
    '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
    .format(
      recognition.get_last_request_id(),
      recognition.get_first_package_delay(),
      recognition.get_last_package_delay(),
    ))
  ```
</CodeGroup>

### 并发调用

在Python中，由于存在[全局解释器锁](https://docs.python.org/zh-cn/3/glossary.html#term-global-interpreter-lock)，同一时刻只有一个线程可以执行Python代码（虽然某些性能导向的库可能会去除此限制）。如果您想更好地利用多核心计算机的计算资源，推荐使用 [multiprocessing](https://docs.python.org/zh-cn/3.11/library/multiprocessing.html#module-multiprocessing) 或 [concurrent.futures.ProcessPoolExecutor](https://docs.python.org/zh-cn/3.11/library/concurrent.futures.html#concurrent.futures.ProcessPoolExecutor)。多线程在较高并发下会显著增加SDK调用延迟。

## 请求参数

请求参数通过 [Recognition类](#recognition类) 的构造方法（`__init__`）进行设置。

| 参数                                   | 类型                  | 默认值          | 是否必须 | 说明                                                                                                                                                       |
| ------------------------------------ | ------------------- | ------------ | ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model`                              | str                 | -            | 是    | 用于实时语音识别的模型（参见[模型列表](#模型列表)）。                                                                                                                            |
| `sample_rate`                        | int                 | -            | 是    | 设置待识别音频采样率（单位Hz）。因模型而异：paraformer-realtime-v2 支持任意采样率；paraformer-realtime-v1 仅支持16000Hz；paraformer-realtime-8k-v2 和 paraformer-realtime-8k-v1 仅支持8000Hz。 |
| `format`                             | str                 | -            | 是    | 设置待识别音频格式。支持：pcm、wav、mp3、opus、speex、aac、amr。注意：opus/speex 必须使用Ogg封装；wav 必须为PCM编码；amr 仅支持AMR-NB类型。                                                        |
| `vocabulary_id`                      | str                 | -            | 否    | 热词ID，适用于 paraformer-realtime-v2 和 paraformer-realtime-8k-v2（参见[定制热词](/developer-guides/speech/improve-recognition-accuracy)）。                            |
| `phrase_id`                          | str                 | -            | 否    | 热词ID，适用于 paraformer-realtime-v1 和 paraformer-realtime-8k-v1（参见[Paraformer语音识别热词定制与管理](/api-reference/speech-recognition/custom-hotwords/http-api)）。      |
| `disfluency_removal_enabled`         | bool                | False        | 否    | 是否过滤语气词（如"嗯"、"啊"等）。                                                                                                                                      |
| `language_hints`                     | list\[str]          | \["zh","en"] | 否    | 语言代码列表，指定待识别语种，仅 paraformer-realtime-v2 支持。                                                                                                              |
| `semantic_punctuation_enabled`       | bool                | False        | 否    | 是否开启语义断句。仅 paraformer-realtime-v2 及以上版本支持。                                                                                                               |
| `max_sentence_silence`               | int                 | 800          | 否    | VAD断句静音阈值（单位ms），范围200-6000。仅 paraformer-realtime-v2 及以上版本且使用VAD断句时有效。                                                                                    |
| `multi_threshold_mode_enabled`       | bool                | False        | 否    | 是否启用多阈值模式，防止VAD断句将过长的句子切断。仅 paraformer-realtime-v2 及以上版本且使用VAD断句时有效。                                                                                     |
| `punctuation_prediction_enabled`     | bool                | True         | 否    | 是否自动添加标点符号。仅 paraformer-realtime-v2 及以上版本支持。                                                                                                             |
| `heartbeat`                          | bool                | False        | 否    | 是否开启长连接保持。仅 paraformer-realtime-v2 及以上版本支持，需SDK版本≥1.23.1。                                                                                                |
| `inverse_text_normalization_enabled` | bool                | True         | 否    | 是否开启逆文本正则化（ITN）。仅 paraformer-realtime-v2 及以上版本支持。                                                                                                        |
| `callback`                           | RecognitionCallback | -            | 否    | 回调接口，用于双向流式调用（参见[回调接口（RecognitionCallback）](#回调接口-recognitioncallback)）。                                                                                 |

## 关键接口

### Recognition类

| 方法签名                                                                          | 说明                                           |
| ----------------------------------------------------------------------------- | -------------------------------------------- |
| `call(self, file: str, phrase_id: str = None, **kwargs) -> RecognitionResult` | 非流式调用：传入本地音频文件路径，同步阻塞地返回完整识别结果。              |
| `start(self, phrase_id: str = None, **kwargs)`                                | 启动双向流式语音识别。                                  |
| `send_audio_frame(self, buffer: bytes)`                                       | 向服务端发送音频二进制数据帧（双向流式调用）。                      |
| `stop(self)`                                                                  | 结束语音识别，阻塞直到 `on_complete` 或 `on_error` 回调触发。 |
| `get_last_request_id(self)`                                                   | 获取最近一次请求的 Request ID。                        |
| `get_first_package_delay(self)`                                               | 获取首包延迟（ms）。                                  |
| `get_last_package_delay(self)`                                                | 获取尾包延迟（ms）。                                  |

### 回调接口 RecognitionCallback

在双向流式调用中，通过实现 `RecognitionCallback` 接口来接收实时识别结果。

| 方法签名                                                | 说明                    |
| --------------------------------------------------- | --------------------- |
| `on_open(self) -> None`                             | 连接建立时触发。              |
| `on_event(self, result: RecognitionResult) -> None` | 收到识别结果时触发，实时返回当前识别状态。 |
| `on_complete(self) -> None`                         | 识别完成时触发。              |
| `on_error(self, result: RecognitionResult) -> None` | 发生错误时触发。              |
| `on_close(self) -> None`                            | 连接关闭时触发。              |

## 识别结果 RecognitionResult

### RecognitionResult

| 方法签名                                                              | 说明                      |
| ----------------------------------------------------------------- | ----------------------- |
| `get_sentence(self) -> Union[Dict[str, Any], List[Any]]`          | 获取当前识别结果，返回单个句子字典或句子列表。 |
| `get_request_id(self) -> str`                                     | 获取当前识别结果对应的 Request ID。 |
| `@staticmethod is_sentence_end(sentence: Dict[str, Any]) -> bool` | 判断当前句子是否已结束（句子结束标志）。    |

### 单句信息 Sentence

| 字段               | 类型          | 说明                                                                             |
| ---------------- | ----------- | ------------------------------------------------------------------------------ |
| `begin_time`     | int         | 句子起始时间（ms）。                                                                    |
| `end_time`       | int         | 句子结束时间（ms）。                                                                    |
| `text`           | str         | 识别文本。                                                                          |
| `words`          | list\[Word] | 词级别识别结果（参见[词信息 Word](#词信息-word)）。                                              |
| `emo_tag`        | str         | 情感标签（仅 paraformer-realtime-8k-v2 且句子结束时返回），取值：`positive`、`negative`、`neutral`。 |
| `emo_confidence` | float       | 情感置信度（范围 0.0–1.0）。                                                             |

### 词信息 Word

| 字段            | 类型  | 说明         |
| ------------- | --- | ---------- |
| `begin_time`  | int | 词起始时间（ms）。 |
| `end_time`    | int | 词结束时间（ms）。 |
| `text`        | str | 词文本。       |
| `punctuation` | str | 词后跟随的标点符号。 |

## 错误码

如遇报错问题，请参见[错误信息](/api-reference/preparation/error-messages)进行排查。

若问题仍未解决，请加入[开发者群](https://github.com/aliyun/alibabacloud-bailian-speech-demo)反馈遇到的问题，并提供Request ID，以便进一步排查问题。

## 更多示例

更多示例，请参见 [GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo)。

## 常见问题

### 功能特性

<AccordionGroup>
  <Accordion title="Q：在长时间静默的情况下，如何保持与服务端长连接？">
    将请求参数 `heartbeat` 设置为 `true`，并持续向服务端发送静音音频。

    静音音频指的是在音频文件或数据流中没有声音信号的内容。静音音频可以通过多种方法生成，例如使用音频编辑软件如 Audacity 或 Adobe Audition，或者通过命令行工具如 FFmpeg。
  </Accordion>

  <Accordion title="Q：如何将音频格式转换为满足要求的格式？">
    可使用 [FFmpeg工具](https://ffmpeg.en.lo4d.com/download)，更多用法请参见FFmpeg官网。

    ```bash
    # 基础转换命令（万能模板）
    # -i，作用：输入文件路径，常用值示例：audio.wav
    # -c:a，作用：音频编码器，常用值示例：aac, libmp3lame, pcm_s16le
    # -b:a，作用：比特率（音质控制），常用值示例：192k, 320k
    # -ar，作用：采样率，常用值示例：44100 (CD), 48000, 16000
    # -ac，作用：声道数，常用值示例：1(单声道), 2(立体声)
    # -y，作用：覆盖已存在文件(无需值)
    ffmpeg -i input_audio.ext -c:a 编码器名 -b:a 比特率 -ar 采样率 -ac 声道数 output.ext

    # 例如：WAV → MP3（保持原始质量）
    ffmpeg -i input.wav -c:a libmp3lame -q:a 0 output.mp3
    # 例如：MP3 → WAV（16bit PCM标准格式）
    ffmpeg -i input.mp3 -c:a pcm_s16le -ar 44100 -ac 2 output.wav
    # 例如：M4A → AAC（提取/转换苹果音频）
    ffmpeg -i input.m4a -c:a copy output.aac  # 直接提取不重编码
    ffmpeg -i input.m4a -c:a aac -b:a 256k output.aac  # 重编码提高质量
    # 例如：FLAC无损 → Opus（高压缩）
    ffmpeg -i input.flac -c:a libopus -b:a 128k -vbr on output.opus
    ```
  </Accordion>

  <Accordion title="Q：是否支持查看每句话对应的时间范围？">
    支持。语音识别结果中会包含每句话的开始时间戳和结束时间戳，可通过它们确定每句话的时间范围。详见[单句信息（Sentence）](#单句信息-sentence)中的 `begin_time` 和 `end_time` 字段。
  </Accordion>

  <Accordion title="Q：如何识别本地文件（录音文件）？">
    识别本地文件有两种方式：

    - **直接传入本地文件路径**： 此种方式在最终识别结束后获取完整识别结果，不适合即时反馈的场景。参见[非流式调用](#非流式调用)，在 [Recognition类](#recognition类) 的 `call` 方法中传入文件路径对录音文件直接进行识别。

    - **将本地文件转成二进制流进行识别**： 此种方式一边识别文件一边流式获取识别结果，适合即时反馈的场景。参见[双向流式调用](#双向流式调用)，通过 [Recognition类](#recognition类) 的 `send_audio_frame` 方法向服务端发送二进制流对其进行识别。
  </Accordion>
</AccordionGroup>

### 故障排查

<AccordionGroup>
  <Accordion title="Q：无法识别语音（无识别结果）是什么原因？">
    1. 请检查请求参数中的音频格式（`format`）和采样率（`sample_rate`）设置是否正确且符合参数约束。以下为常见错误示例：

       - 音频文件扩展名为 .wav，但实际为 MP3 格式，而请求参数 `format` 设置为 `mp3`（参数设置错误）。
       - 音频采样率为 3600Hz，但请求参数 `sample_rate` 设置为 48000（参数设置错误）。

       可以使用 [ffprobe](https://ffmpeg.org/ffprobe.html) 工具获取音频的容器、编码、采样率、声道等信息：

    ```bash
    ffprobe -v error -show_entries format=format_name -show_entries stream=codec_name,sample_rate,channels -of default=noprint_wrappers=1 input.xxx
    ```

    2. 使用 `paraformer-realtime-v2` 模型时，请检查 `language_hints` 设置的语言是否与音频实际语言一致。例如：音频实际为中文，但 `language_hints` 设置为 `en`（英文）。

    3. 若以上检查均无问题，可通过定制热词提升对特定词语的识别效果。
  </Accordion>
</AccordionGroup>
