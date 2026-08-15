> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Qwen-Audio-3.0-ASR-Flash-Streaming/Fun-ASR-Realtime 实时语音识别 Python SDK

> Qwen-Audio-3.0-ASR-Flash-Streaming/Fun-ASR-Realtime 实时语音识别 Python SDK

**使用指南**： 模型选择请参见[实时语音识别](/developer-guides/speech/asr-realtime)。

## 快速开始

[Recognition 类](#recognition-类)支持非流式和双向流式两种调用方式。

- **非流式调用**： 识别本地文件，一次性返回完整结果。
- **双向流式调用**： 识别音频流并实时返回结果。音频流可来自麦克风或本地文件。

### 非流式调用

提交单个音频文件的语音识别任务，阻塞等待直到返回结果。

实例化 [Recognition 类](#recognition-类)，设置[请求参数](#请求参数)，调用 `call` 获取[识别结果 (RecognitionResult)](#识别结果-recognitionresult)。

<Accordion title="点击查看完整示例">
  ```python
  from http import HTTPStatus
  import dashscope
  from dashscope.audio.asr import Recognition
  import os

  # 如果未配置环境变量，请将下一行替换为：dashscope.api_key = "sk-xxx"
  dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

  dashscope.base_websocket_api_url='wss://dashscope.aliyuncs.com/api-ws/v1/inference'

  recognition = Recognition(model='qwen-audio-3.0-asr-flash-streaming',
                            format='wav',
                            sample_rate=16000,
                            callback=None)
  result = recognition.call('{YOUR_AUDIO_FILE}')
  if result.status_code == HTTPStatus.OK:
    print('识别结果：')
    print(result.get_sentence())
  else:
    print('错误：', result.message)

  print(
    '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
    .format(
      recognition.get_last_request_id(),
      recognition.get_first_package_delay(),
      recognition.get_last_package_delay(),
    ))
  ```
</Accordion>

### 双向流式调用

提交语音识别任务，通过回调接收结果。

<Steps>
  <Step title="启动流式识别">
    实例化 [Recognition 类](#recognition-类)，配置[请求参数](#请求参数)和[回调接口 (RecognitionCallback)](#回调接口-recognitioncallback)，调用 `start`。
  </Step>

  <Step title="发送音频">
    反复调用 `send_audio_frame` 发送来自本地文件或设备（如麦克风）的二进制音频数据。

    服务端通过 `on_event` 回调实时返回结果。

    每段音频约 100 ms，大小 1-16 KB。
  </Step>

  <Step title="停止识别">
    调用 `stop` 结束识别。

    该方法会阻塞等待，直到触发 `on_complete` 或 `on_error`。
  </Step>
</Steps>

<Accordion title="点击查看完整示例">
  <Tabs>
    <Tab title="识别麦克风语音">
      ```python
      import os
      import signal  # 用于处理键盘事件（按 Ctrl+C 终止录音）
      import sys

      import dashscope
      import pyaudio
      from dashscope.audio.asr import *

      mic = None
      stream = None

      # 设置录音参数
      sample_rate = 16000  # 采样率（Hz）
      channels = 1  # 单声道
      dtype = 'int16'  # 数据类型
      format_pcm = 'pcm'  # 音频数据格式
      block_size = 3200  # 每个缓冲区的帧数

      # 实时语音识别回调
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
          print('RecognitionCallback completed.')  # 识别完成

        def on_error(self, result: RecognitionResult) -> None:
          print('RecognitionCallback task_id: ', result.request_id)
          print('RecognitionCallback error: ', result.message)
          # 如果音频流正在运行，停止并关闭
          if 'stream' in globals() and stream.is_active():
            stream.stop()
            stream.close()
          # 强制退出程序
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
        print('按下 Ctrl+C，停止识别...')
        # 停止识别
        recognition.stop()
        print('识别已停止。')
        print(
          '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
          .format(
            recognition.get_last_request_id(),
            recognition.get_first_package_delay(),
            recognition.get_last_package_delay(),
          ))
        # 强制退出程序
        sys.exit(0)

      # 主函数
      if __name__ == '__main__':
        # 如果未配置环境变量，请将下一行替换为：dashscope.api_key = "sk-xxx"
        dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

        dashscope.base_websocket_api_url='wss://dashscope.aliyuncs.com/api-ws/v1/inference'

        # 创建识别回调
        callback = Callback()

        # 异步模式调用识别服务，可自定义识别参数，如 model、format、sample_rate
        recognition = Recognition(
          model='qwen-audio-3.0-asr-flash-streaming',
          format=format_pcm,
          # 'pcm', 'wav', 'mp3', 'opus', 'speex', 'aac', 'amr'。支持的格式请参见文档。
          sample_rate=sample_rate,
          # 支持 16000。
          semantic_punctuation_enabled=False,
          callback=callback)

        # 启动识别
        recognition.start()

        signal.signal(signal.SIGINT, signal_handler)
        print("按 Ctrl+C 停止录音和识别...")
        # 创建键盘监听，直到按下 Ctrl+C

        while True:
          if stream:
            data = stream.read(3200, exception_on_overflow=False)
            recognition.send_audio_frame(data)
          else:
            break

        recognition.stop()
      ```
    </Tab>

    <Tab title="识别本地音频文件">
      ```python
      import os
      import time
      import dashscope
      from dashscope.audio.asr import *

      # 如果未配置环境变量，请将下一行替换为：dashscope.api_key = "sk-xxx"
      dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

      dashscope.base_websocket_api_url='wss://dashscope.aliyuncs.com/api-ws/v1/inference'

      from datetime import datetime

      def get_timestamp():
        now = datetime.now()
        formatted_timestamp = now.strftime("[%Y-%m-%d %H:%M:%S.%f]")
        return formatted_timestamp

      class Callback(RecognitionCallback):
        def on_complete(self) -> None:
          print(get_timestamp() + ' 识别完成')  # 识别完成

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
                  ' RecognitionCallback sentence end, request_id:%s, usage:%s'
                  % (result.get_request_id(), result.get_usage(sentence)))

      callback = Callback()

      recognition = Recognition(model='qwen-audio-3.0-asr-flash-streaming',
                                format='wav',
                                sample_rate=16000,
                                callback=callback)

      try:
        audio_data: bytes = None
        f = open("{YOUR_AUDIO_FILE}", 'rb')
        if os.path.getsize("{YOUR_AUDIO_FILE}"):
          # 将整个文件读入缓冲区
          file_buffer = f.read()
          f.close()
          print("开始识别")
          recognition.start()

          # 每次发送 3200 字节
          buffer_size = len(file_buffer)
          offset = 0
          chunk_size = 3200

          while offset < buffer_size:
            # 计算当前分片大小
            remaining_bytes = buffer_size - offset
            current_chunk_size = min(chunk_size, remaining_bytes)

            # 从缓冲区中提取当前分片
            audio_data = file_buffer[offset:offset + current_chunk_size]

            # 发送音频帧
            recognition.send_audio_frame(audio_data)
            # 更新偏移量
            offset += current_chunk_size

            # 添加延迟以模拟实时传输
            time.sleep(0.1)

          recognition.stop()
        else:
          raise Exception(
            '提供的文件为空（长度为零字节）')
      except Exception as e:
        raise e

      print(
        '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
        .format(
          recognition.get_last_request_id(),
          recognition.get_first_package_delay(),
          recognition.get_last_package_delay(),
        ))
      ```
    </Tab>
  </Tabs>
</Accordion>

## 请求参数

在 [Recognition 类](#recognition-类)的构造函数（`__init__`）中设置请求参数。

| **参数**                           | **类型**              | **默认值**       | **是否必选** | **说明**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| -------------------------------- | ------------------- | ------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| model                            | str                 | -             | 是        | 用于实时语音识别的[支持的模型](/developer-guides/speech/speech-to-text-models)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| sample\_rate                     | int                 | -             | 是        | 音频采样率，单位 Hz。8k 模型仅支持 8000 Hz，其他模型支持任意采样率。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| format                           | str                 | -             | 是        | 音频格式：pcm、wav、mp3、opus、speex、aac、amr。 <br /><br /> **注意**： opus/speex 必须使用 Ogg 封装。wav 必须使用 PCM 编码。amr 仅支持 AMR-NB。                                                                                                                                                                                                                                                                                                                                                                                                                       |
| vocabulary\_id                   | str                 | -             | 否        | 热词表 ID，用于热词定制。参见[自定义热词](/developer-guides/speech/improve-recognition-accuracy)。                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| vocabulary                       | dict                | -             | 否        | 即时热词。以键值对形式传入，键为热词文本（`string`），值为热词权重（`integer`），无需预先创建热词列表。权重取值范围为 \[1, 5] 或 50：取 \[1, 5] 时值越大模型越倾向输出该词；取 50 时为超级热词，召回率大幅提升，但超级热词数量最多不超过 50 个。适用于临时性、会话级别的热词优化。与预编译热词同时配置时，仅即时热词生效。使用方法请参见[即时热词](/developer-guides/speech/improve-recognition-accuracy)。仅 `qwen-audio-3.0-asr-flash-streaming` 支持。                                                                                                                                                                                                                                    |
| semantic\_punctuation\_enabled   | bool                | False         | 否        | 是否启用语义标点。<ul><li>true：使用语义标点（禁用基于 VAD 的标点）。适用于会议转录等对准确率要求高的场景。</li><li>false（默认）：使用 VAD 标点（禁用语义标点）。适用于交互式场景，延迟更低。</li></ul>                                                                                                                                                                                                                                                                                                                                                                                                            |
| max\_sentence\_silence           | int                 | 1300          | 否        | VAD 断句静音阈值，单位 ms。静音超过该值则断句。当 `semantic_punctuation_enabled` 为 true 时，该参数不作为返回 `sentence_end` 的判定依据，但设置过低可能影响识别效果。取值范围：\[200, 6000]。                                                                                                                                                                                                                                                                                                                                                                                                    |
| multi\_threshold\_mode\_enabled  | bool                | False         | 否        | 防止 VAD 产生过长的分段。仅在 `semantic_punctuation_enabled` 为 false 时生效。                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| punctuation\_prediction\_enabled | bool                | True          | 否        | 自动为识别结果添加标点。此参数固定为 true，无法通过 SDK 覆盖；识别结果始终包含自动标点。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| heartbeat                        | bool                | False         | 否        | 保持服务端持久连接：<ul><li>true：持续发送静音音频以保持连接。</li><li>false（默认）：即使持续发送静音音频，连接也将在一定时间后因超时而断开。静音音频指无声音信号的音频，可通过音频编辑软件（Audacity、Adobe Audition）或 FFmpeg 生成。</li></ul> 需要 SDK 版本 1.23.1 及以上。                                                                                                                                                                                                                                                                                                                                                       |
| language\_hints                  | list\[str]          | \["zh", "en"] | 否        | 识别的语言代码。不设置时自动检测。支持的语言代码：<ul><li>fun-asr-realtime、fun-asr-realtime-2025-11-07：zh（中文）、en（英文）、ja（日语）、ko（韩语）、vi（越南语）、th（泰语）、id（印尼语）、ms（马来语）、tl（菲律宾语）、hi（印地语）、ar（阿拉伯语）、fr（法语）、de（德语）、es（西班牙语）、pt（葡萄牙语）、ru（俄语）、it（意大利语）、nl（荷兰语）、sv（瑞典语）、da（丹麦语）、fi（芬兰语）、no（挪威语）、el（希腊语）、pl（波兰语）、cs（捷克语）、hu（匈牙利语）、ro（罗马尼亚语）、bg（保加利亚语）、hr（克罗地亚语）、sk（斯洛伐克语）</li><li>fun-asr-realtime-2026-02-28：zh（中文）、en（英文）、ja（日语）</li><li>fun-asr-realtime-2025-09-15：zh（中文）、en（英文）</li><li>fun-asr-flash-8k-realtime、fun-asr-flash-8k-realtime-2026-01-28：zh（中文）</li></ul> |
| speech\_noise\_threshold         | float               | -             | 否        | 语音噪声检测阈值，用于调节 VAD 灵敏度。范围：\[-1.0, 1.0]。<ul><li>接近 -1：降低噪声阈值——更多噪声可能被识别为语音。</li><li>接近 +1：提高噪声阈值——部分语音可能被过滤为噪声。</li></ul> **注意**： 这是高级参数，调整会显著影响识别质量。请充分测试，并根据音频环境小幅调整（步长 0.1）。                                                                                                                                                                                                                                                                                                                                                          |
| special\_word\_filter            | str                 | -             | 否        | 敏感词过滤配置，仅 Fun-ASR 支持。最多支持设置 32 个敏感词。参见[敏感词过滤](#敏感词过滤)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| callback                         | RecognitionCallback | -             | 否        | [RecognitionCallback 回调接口](#回调接口-recognitioncallback)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |

即时热词示例：

```python
from dashscope.audio.asr import Recognition
vocab = {"张三": 5, "李四": 5}
recognition = Recognition(
    model='qwen-audio-3.0-asr-flash-streaming',
    format='wav',
    sample_rate=16000,
    vocabulary=vocab,
    callback=None)
```

<a id="敏感词过滤" />

#### 敏感词过滤

敏感词过滤可对识别结果中的敏感词执行替换或移除，适用于客服质检、内容合规、字幕审核等场景。仅 Fun-ASR 支持，最多支持设置 32 个敏感词。未传入 `special_word_filter` 参数时，不会对敏感词进行过滤。

`special_word_filter` 为 JSON 字符串，包含三个子字段：

- `filter_with_signed.word_list`：字符串数组，列出需要被替换为等长 `*` 的敏感词。例如 `["测试"]`，"帮我测试一下"会变成"帮我\*\*一下"。
- `filter_with_empty.word_list`：字符串数组，列出需要从结果中完全移除的敏感词。例如 `["开始"]`，"比赛这就要开始了吗"会变成"比赛这就要了吗"。
- `system_reserved_filter`：布尔值，默认 `false`。是否启用敏感词过滤功能。

配置示例：

```python
import json

special_word_filter = json.dumps({
    "filter_with_signed": {
        "word_list": ["测试"]
    },
    "filter_with_empty": {
        "word_list": ["开始", "发生"]
    },
    "system_reserved_filter": True
})

recognition = Recognition(model='qwen-audio-3.0-asr-flash-streaming',
                          format='wav',
                          sample_rate=16000,
                          special_word_filter=special_word_filter,
                          callback=None)
```

### 运行时参数

以下参数通过 `Recognition` 实例的 `call` 或 `start` 方法的关键字参数传入。

| **参数**     | **类型** | **默认值** | **是否必选** | **说明**                                                                                                                                                                           |
| ---------- | ------ | ------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| raw\_input | dict   | -       | 否        | 输入对象，用于传入对话上下文（context）。上下文用于辅助识别、提升专有词汇的识别准确率。使用方法详见[提升识别准确率](/developer-guides/speech/improve-recognition-accuracy)。仅 `fun-asr-realtime` 和 `fun-asr-realtime-2025-11-07` 模型支持。 |

<Warning>
  - 上下文消息（`input_text` 和 `text` 类型）各最多 5 条，超出时保留最近的 5 条。
  - 每轮上下文文本总长度不超过 400 个字符，超出部分从末尾截断。
  - 上下文消息必须按对话轮次排列，每轮中 `user`（`input_text` 类型）必须在对应的 `assistant`（`text` 类型）之前。
</Warning>

<Note>
  使用 `raw_input` 参数时，SDK 版本不能低于 1.25.23。
</Note>

`raw_input` 通过 `Recognition` 实例的 `start` 或 `call` 方法传入：

```python
input_context = {
  "context": [
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "你好啊"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "你好啊，我是通义千问，有什么可以帮助你的？"
        }
      ]
    }
  ]
}
recognition.start(raw_input=input_context)
# 或者
recognition.call(raw_input=input_context)
```

## 核心接口

### `Recognition` 类

通过 `from dashscope.audio.asr import *` 导入。

| **成员方法**                   | **方法签名**                                                                          | **说明**                                                                                               |
| -------------------------- | --------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| call                       | `def call(self, file: str, phrase_id: str = None, **kwargs) -> RecognitionResult` | 对本地文件执行非流式识别。阻塞等待处理完成后返回 `RecognitionResult`。                                                        |
| start                      | `def start(self, phrase_id: str = None, **kwargs)`                                | 启动流式识别，非阻塞。需配合 `send_audio_frame` 和 `stop` 使用。                                                       |
| send\_audio\_frame         | `def send_audio_frame(self, buffer: bytes)`                                       | 发送一个音频帧（每包约 100 ms，1-16 KB）。通过 [RecognitionCallback](#回调接口-recognitioncallback) 的 `on_event` 回调获取结果。 |
| stop                       | `def stop(self)`                                                                  | 停止识别。阻塞等待直到所有音频处理完成。                                                                                 |
| get\_last\_request\_id     | `def get_last_request_id(self)`                                                   | 返回请求 ID。Recognition 对象创建后即可调用。                                                                       |
| get\_first\_package\_delay | `def get_first_package_delay(self)`                                               | 返回首包延迟（从发送第一个音频包到收到第一个结果的时间）。任务完成后可用。                                                                |
| get\_last\_package\_delay  | `def get_last_package_delay(self)`                                                | 返回尾包延迟（从调用 `stop` 到收到最终结果的时间）。任务完成后可用。                                                               |

### 回调接口 (`RecognitionCallback`)

在[双向流式调用](#双向流式调用)中，服务端通过回调返回数据。实现回调接口以处理响应。

<Accordion title="点击查看示例">
  ```python
  class Callback(RecognitionCallback):
    def on_open(self) -> None:
      print('连接成功')

    def on_event(self, result: RecognitionResult) -> None:
      # 实现接收识别结果的逻辑
      pass

    def on_complete(self) -> None:
      print('任务完成')

    def on_error(self, result: RecognitionResult) -> None:
      print('发生异常：', result)

    def on_close(self) -> None:
      print('连接关闭')

  callback = Callback()
  ```
</Accordion>

| **方法**                                                  | **参数**                                                | **返回值** | **说明**      |
| ------------------------------------------------------- | ----------------------------------------------------- | ------- | ----------- |
| `def on_open(self) -> None`                             | 无                                                     | 无       | 建立服务端连接时调用。 |
| `def on_event(self, result: RecognitionResult) -> None` | `result`：[RecognitionResult](#识别结果-recognitionresult) | 无       | 返回识别结果时调用。  |
| `def on_complete(self) -> None`                         | 无                                                     | 无       | 所有结果返回后调用。  |
| `def on_error(self, result: RecognitionResult) -> None` | `result`：[RecognitionResult](#识别结果-recognitionresult) | 无       | 发生错误时调用。    |
| `def on_close(self) -> None`                            | 无                                                     | 无       | 连接关闭时调用。    |

## 响应

### 识别结果 (`RecognitionResult`)

`RecognitionResult` 表示[流式调用](#双向流式调用)或[非流式调用](#非流式调用)的识别结果。

| **成员方法**          | **方法签名**                                                              | **说明**                                                                  |
| ----------------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| get\_sentence     | `def get_sentence(self) -> Union[Dict[str, Any], List[Any]]`          | 返回当前识别的句子及时间戳。在回调中返回单个句子，类型为 `Dict[str, Any]`。参见[句子信息](#句子信息-sentence)。 |
| get\_request\_id  | `def get_request_id(self) -> str`                                     | 返回请求 ID。                                                                |
| get\_usage        | `def get_usage(self, sentence: Dict[str, Any]) -> Dict`               | 返回该句子的用量信息。                                                             |
| is\_sentence\_end | `@staticmethod def is_sentence_end(sentence: Dict[str, Any]) -> bool` | 判断句子是否结束。                                                               |

### 句子信息 (`Sentence`)

| **参数**      | **类型**                     | **说明**        |
| ----------- | -------------------------- | ------------- |
| begin\_time | int                        | 句子开始时间，单位 ms。 |
| end\_time   | int                        | 句子结束时间，单位 ms。 |
| text        | str                        | 识别文本。         |
| words       | [Word](#词级时间戳信息-word) 对象列表 | 词级时间戳信息。      |

### 词级时间戳信息 (`Word`)

| **参数**      | **类型** | **说明**        |
| ----------- | ------ | ------------- |
| begin\_time | int    | 词的开始时间，单位 ms。 |
| end\_time   | int    | 词的结束时间，单位 ms。 |
| text        | str    | 词文本。          |
| punctuation | str    | 标点符号。         |
