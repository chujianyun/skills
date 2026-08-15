> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 实时音视频翻译

> 2.8 秒延迟的流式同声传译

## 模型信息

qwen3.5-livetranslate-flash-realtime 是一款多语言实时音视频翻译模型，支持 60 种语言互译（其中 29 种支持音频+文本输出、31 种仅支持文本输出），可同时处理音频与图像输入，利用视觉上下文信息提升翻译准确性，并实时输出高质量的翻译文本与音频。

核心特性：

- **多语言支持**：支持 60 种语言互译，其中 29 种支持音频+文本输出、31 种仅支持文本输出，覆盖中文、英语、法语、德语、俄语、日语、韩语、西班牙语、葡萄牙语、阿拉伯语等主流语种。
- **视觉增强**：利用视觉内容提升翻译准确性。模型通过分析画面中的口型、动作和文字，改善在嘈杂环境下或一词多义场景中的翻译效果。
- **2.8 秒延迟**：实现低至 2.8 秒的同传延迟。
- **无损同传**：通过语义单元预测技术，解决跨语言语序问题。实时翻译质量接近离线翻译结果。
- **音色自然**：生成音色自然的拟人语音。模型能根据源语音内容，自适应调节语气和情感。
- **配置热词**：通过热词提升特定词汇的翻译准确性。
- **声音复刻**：支持复刻发言人音色用于翻译播报，让输出听起来像本人说外语。支持服务端实时复刻和使用预先复刻的固定音色。
- **跳过同语种输出**：当源语种与目标语种相同时，可分别跳过文本或音频输出。仅当目标语种为中文（`zh`）或英语（`en`）时生效。

### 推荐模型

| 模型                                                                                               | 版本  | 上下文窗口  | 最大输入   | 最大输出  |
| ------------------------------------------------------------------------------------------------ | --- | ------ | ------ | ----- |
| **qwen3.5-livetranslate-flash-realtime**（当前能力等同 qwen3.5-livetranslate-flash-realtime-2026-05-19） | 稳定版 | 53,248 | 49,152 | 4,096 |
| qwen3.5-livetranslate-flash-realtime-2026-05-19                                                  | 快照版 | 53,248 | 49,152 | 4,096 |

### 旧版模型

<Note>
  以下模型仍在服务中，但不再作为首选推荐。新场景建议使用上方的新一代模型，以获得更优的翻译质量与性价比。
</Note>

| 模型                                                                                           | 版本  | 上下文窗口  | 最大输入   | 最大输出  |
| -------------------------------------------------------------------------------------------- | --- | ------ | ------ | ----- |
| **qwen3-livetranslate-flash-realtime**（当前能力等同 qwen3-livetranslate-flash-realtime-2025-09-22） | 稳定版 | 53,248 | 49,152 | 4,096 |
| qwen3-livetranslate-flash-realtime-2025-09-22                                                | 快照版 | 53,248 | 49,152 | 4,096 |

## 快速开始

### 环境准备

Python 版本需为 3.10 或更高。

首先安装 pyaudio。

<Tabs>
  <Tab title="macOS">
    ```bash
    brew install portaudio && pip install pyaudio
    ```
  </Tab>

  <Tab title="Debian/Ubuntu">
    ```bash
    sudo apt-get install python3-pyaudio
    # 或者
    pip install pyaudio
    ```
  </Tab>

  <Tab title="CentOS">
    ```bash
    sudo yum install -y portaudio portaudio-devel && pip install pyaudio
    ```
  </Tab>

  <Tab title="Windows">
    ```powershell
    pip install pyaudio
    ```
  </Tab>
</Tabs>

安装完成后，使用 pip 安装所需的 WebSocket 依赖：

```bash
pip install websocket-client==1.8.0 websockets
```

### 创建客户端

在本地新建一个 Python 文件，命名为 `livetranslate_client.py`，将以下代码复制到文件中：

<Accordion title="客户端代码 - livetranslate_client.py">
  ```python
  import os
  import time
  import base64
  import asyncio
  import json
  import websockets
  import pyaudio
  import queue
  import threading
  import traceback

  class LiveTranslateClient:
    def __init__(self, api_key: str, target_language: str = "en", *, audio_enabled: bool = True):
      if not api_key:
        raise ValueError("API Key 不能为空。")

      self.api_key = api_key
      self.target_language = target_language
      self.audio_enabled = audio_enabled
      self.voice = voice if audio_enabled else "Cherry"
      self.ws = None
      self.api_url = "wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=qwen3.5-livetranslate-flash-realtime"

      # 音频输入配置（麦克风）
      self.input_rate = 16000
      self.input_chunk = 1600
      self.input_format = pyaudio.paInt16
      self.input_channels = 1

      # 音频输出配置（播放）
      self.output_rate = 24000
      self.output_chunk = 2400
      self.output_format = pyaudio.paInt16
      self.output_channels = 1

      # 状态管理
      self.is_connected = False
      self.audio_player_thread = None
      self.audio_playback_queue = queue.Queue()
      self.pyaudio_instance = pyaudio.PyAudio()
      self.session_finished_event = asyncio.Event()

    async def connect(self):
      """建立与翻译服务的 WebSocket 连接。"""
      headers = {"Authorization": f"Bearer {self.api_key}"}
      try:
        self.ws = await websockets.connect(self.api_url, additional_headers=headers)
        self.is_connected = True
        print(f"已成功连接到服务器：{self.api_url}")
        await self.configure_session()
      except Exception as e:
        print(f"连接失败：{e}")
        self.is_connected = False
        raise

    async def configure_session(self):
      """配置翻译会话，设置目标语言、音色等参数。"""
      config = {
        "event_id": f"event_{int(time.time() * 1000)}",
        "type": "session.update",
        "session": {
          # 'modalities' 控制输出类型。
          # ["text", "audio"]：同时返回翻译文本和合成语音（推荐）。
          # ["text"]：仅返回翻译文本。
          "modalities": ["text", "audio"] if self.audio_enabled else ["text"],
          **({"voice": self.voice} if self.audio_enabled and self.voice else {}),
          "input_audio_format": "pcm",
          "output_audio_format": "pcm",
          # 'input_audio_transcription' 配置源语言识别。
          # 将 'model' 设置为 'qwen3-asr-flash-realtime' 可同时输出源语言识别结果。
          # "input_audio_transcription": {
          #     "model": "qwen3-asr-flash-realtime",
          #     "language": "zh"  # 源语言，默认为 'en'
          # },
          "translation": {
            "language": self.target_language
          }
        }
      }
      print(f"正在发送会话配置：{json.dumps(config, indent=2, ensure_ascii=False)}")
      await self.ws.send(json.dumps(config))

    async def send_audio_chunk(self, audio_data: bytes):
      """编码并发送音频数据块到服务器。"""
      if not self.is_connected:
        return

      event = {
        "event_id": f"event_{int(time.time() * 1000)}",
        "type": "input_audio_buffer.append",
        "audio": base64.b64encode(audio_data).decode()
      }
      await self.ws.send(json.dumps(event))

    async def send_image_frame(self, image_bytes: bytes, *, event_id: str | None = None):
      # 发送图像数据到服务器
      if not self.is_connected:
        return

      if not image_bytes:
        raise ValueError("image_bytes 不能为空")

      # 编码为 Base64
      image_b64 = base64.b64encode(image_bytes).decode()

      event = {
        "event_id": event_id or f"event_{int(time.time() * 1000)}",
        "type": "input_image_buffer.append",
        "image": image_b64,
      }

      await self.ws.send(json.dumps(event))

    def _audio_player_task(self):
      stream = self.pyaudio_instance.open(
        format=self.output_format,
        channels=self.output_channels,
        rate=self.output_rate,
        output=True,
        frames_per_buffer=self.output_chunk,
      )
      try:
        while self.is_connected or not self.audio_playback_queue.empty():
          try:
            audio_chunk = self.audio_playback_queue.get(timeout=0.1)
            if audio_chunk is None: # 终止信号
              break
            stream.write(audio_chunk)
            self.audio_playback_queue.task_done()
          except queue.Empty:
            continue
      finally:
        stream.stop_stream()
        stream.close()

    def start_audio_player(self):
      """启动音频播放线程（仅在启用音频输出时有效）。"""
      if not self.audio_enabled:
        return
      if self.audio_player_thread is None or not self.audio_player_thread.is_alive():
        self.audio_player_thread = threading.Thread(target=self._audio_player_task, daemon=True)
        self.audio_player_thread.start()

    async def handle_server_messages(self, on_text_received):
      """循环处理服务器返回的消息。"""
      try:
        async for message in self.ws:
          event = json.loads(message)
          event_type = event.get("type")
          if event_type == "response.audio.delta" and self.audio_enabled:
            audio_b64 = event.get("delta", "")
            if audio_b64:
              audio_data = base64.b64decode(audio_b64)
              self.audio_playback_queue.put(audio_data)

          elif event_type == "response.done":
            print("\n[INFO] 一轮响应已完成。")
            usage = event.get("response", {}).get("usage", {})
            if usage:
              print(f"[INFO] Token 用量：{json.dumps(usage, indent=2, ensure_ascii=False)}")
          elif event_type == "session.finished":
            print("[INFO] 会话已结束。")
            self.session_finished_event.set()
          # 处理源语言识别结果（需启用 input_audio_transcription.model）
          # elif event_type == "conversation.item.input_audio_transcription.text":
          #     stash = event.get("stash", "")  # 未确认的识别文本
          #     print(f"[识别中] {stash}")
          # elif event_type == "conversation.item.input_audio_transcription.completed":
          #     transcript = event.get("transcript", "")  # 最终识别结果
          #     print(f"[源语言] {transcript}")
          elif event_type == "response.text.text":
            # 仅文本模态下的流式翻译文本
            text = event.get("text", "")
            stash = event.get("stash", "")
            print(f"\r[翻译中] {text}{stash}", end="", flush=True)
          elif event_type == "response.audio_transcript.done":
            print("\n[INFO] 文本翻译完成。")
            text = event.get("transcript", "")
            if text:
              print(f"[INFO] 翻译文本：{text}")
          elif event_type == "response.text.done":
            print("\n[INFO] 文本翻译完成。")
            text = event.get("text", "")
            if text:
              print(f"[INFO] 翻译文本：{text}")

      except websockets.exceptions.ConnectionClosed as e:
        print(f"[WARNING] 连接已关闭：{e}")
        self.is_connected = False
      except Exception as e:
        print(f"[ERROR] 处理消息时发生未知错误：{e}")
        traceback.print_exc()
        self.is_connected = False

    async def start_microphone_streaming(self):
      """从麦克风采集音频并流式发送到服务器。"""
      stream = self.pyaudio_instance.open(
        format=self.input_format,
        channels=self.input_channels,
        rate=self.input_rate,
        input=True,
        frames_per_buffer=self.input_chunk
      )
      print("麦克风已开启，请开始说话...")
      try:
        while self.is_connected:
          audio_chunk = await asyncio.get_event_loop().run_in_executor(
            None, stream.read, self.input_chunk
          )
          await self.send_audio_chunk(audio_chunk)
      finally:
        stream.stop_stream()
        stream.close()

    async def close(self):
      """优雅关闭连接并释放资源。"""
      # 发送 session.finish，确保服务端完成最后的语音翻译
      if self.is_connected and self.ws:
        finish_event = {
          "event_id": f"event_{int(time.time() * 1000)}",
          "type": "session.finish",
        }
        await self.ws.send(json.dumps(finish_event))
        print("已发送 session.finish，等待服务端完成处理...")
        try:
          await asyncio.wait_for(self.session_finished_event.wait(), timeout=15)
          print("服务端已完成处理。")
        except asyncio.TimeoutError:
          print("等待 session.finished 超时。")
      self.is_connected = False
      if self.ws:
        await self.ws.close()
        print("WebSocket 连接已关闭。")

      if self.audio_player_thread:
        self.audio_playback_queue.put(None) # 发送终止信号
        self.audio_player_thread.join(timeout=1)
        print("音频播放线程已停止。")

      self.pyaudio_instance.terminate()
      print("PyAudio 实例已释放。")
  ```
</Accordion>

### 与模型交互

在 `livetranslate_client.py` 同一目录下创建另一个 Python 文件，命名为 `main.py`，将以下代码复制到文件中：

<Accordion title="main.py">
  ```python
  import os
  import asyncio
  from livetranslate_client import LiveTranslateClient

  def print_banner():
    print("=" * 60)
    print("  Powered by Qwen qwen3.5-livetranslate-flash-realtime")
    print("=" * 60 + "\n")

  def get_user_config():
    """获取用户配置"""
    print("请选择模式：")
    print("1. 语音 + 文本 [默认] | 2. 仅文本")
    mode_choice = input("请输入选项（回车默认为语音 + 文本）：").strip()
    audio_enabled = (mode_choice != "2")

    if audio_enabled:
      lang_map = {
        "1": "en", "2": "zh", "3": "ru", "4": "fr", "5": "de", "6": "pt",
        "7": "es", "8": "it", "9": "ko", "10": "ja", "11": "yue"
      }
      print("请选择目标翻译语言（语音 + 文本模式）：")
      print("1. 英语 | 2. 中文 | 3. 俄语 | 4. 法语 | 5. 德语 | 6. 葡萄牙语 | 7. 西班牙语 | 8. 意大利语 | 9. 韩语 | 10. 日语 | 11. 粤语")
    else:
      lang_map = {
        "1": "en", "2": "zh", "3": "ru", "4": "fr", "5": "de", "6": "pt", "7": "es", "8": "it",
        "9": "id", "10": "ko", "11": "ja", "12": "vi", "13": "th", "14": "ar",
        "15": "yue", "16": "hi", "17": "el", "18": "tr"
      }
      print("请选择目标翻译语言（仅文本模式）：")
      print("1. 英语 | 2. 中文 | 3. 俄语 | 4. 法语 | 5. 德语 | 6. 葡萄牙语 | 7. 西班牙语 | 8. 意大利语 | 9. 印尼语 | 10. 韩语 | 11. 日语 | 12. 越南语 | 13. 泰语 | 14. 阿拉伯语 | 15. 粤语 | 16. 印地语 | 17. 希腊语 | 18. 土耳其语")

    choice = input("请输入选项（默认为第一个选项）：").strip()
    target_language = lang_map.get(choice, next(iter(lang_map.values())))

    voice = None
    if audio_enabled:
      print("\n请选择语音合成音色：")
      voice_map = {"1": "Cherry", "2": "Nofish", "3": "Sunny", "4": "Jada", "5": "Dylan", "6": "Peter", "7": "Eric", "8": "Kiki", "9": "Ethan"}
      print("1. Cherry（女声）[默认] | 2. Nofish（男声） | 3. Sunny（四川女声） | 4. Jada（上海女声） | 5. Dylan（北京男声） | 6. Peter（天津男声） | 7. Eric（四川男声） | 8. Kiki（粤语女声） | 9. Ethan（男声）")
      voice_choice = input("请输入选项（回车默认为 Cherry）：").strip()
      voice = voice_map.get(voice_choice, "Cherry")
    return target_language, voice, audio_enabled

  async def main():
    """主程序入口"""
    print_banner()

    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
      print("[ERROR] 请设置 DASHSCOPE_API_KEY 环境变量。")
      print("  示例：export DASHSCOPE_API_KEY='REDACTED'")
      return

    target_language, voice, audio_enabled = get_user_config()
    print("\n配置完成：")
    print(f"  - 目标语言：{target_language}")
    if audio_enabled:
      print(f"  - 合成音色：{voice}")
    else:
      print("  - 输出模式：仅文本")

    client = LiveTranslateClient(api_key=api_key, target_language=target_language, voice=voice, audio_enabled=audio_enabled)

    # 定义回调函数
    def on_translation_text(text):
      print(text, end="", flush=True)

    try:
      print("正在连接翻译服务...")
      await client.connect()

      # 根据模式启动音频播放
      client.start_audio_player()

      print("\n" + "-" * 60)
      print("连接成功！请对着麦克风说话。")
      print("程序将实时翻译您的语音并播放结果。按 Ctrl+C 退出。")
      print("-" * 60 + "\n")

      # 并发运行消息处理和麦克风录音
      message_handler = asyncio.create_task(client.handle_server_messages(on_translation_text))
      tasks = [message_handler]
      # 无论是否启用音频输出，都必须从麦克风采集音频用于翻译
      microphone_streamer = asyncio.create_task(client.start_microphone_streaming())
      tasks.append(microphone_streamer)

      await asyncio.gather(*tasks)

    except KeyboardInterrupt:
      print("\n\n用户中断，正在退出...")
    except Exception as e:
      print(f"\n发生严重错误：{e}")
    finally:
      print("\n正在清理资源...")
      await client.close()
      print("程序已退出。")

  if __name__ == "__main__":
    asyncio.run(main())
  ```
</Accordion>

运行 `main.py`，对着麦克风说出要翻译的语句。模型将实时输出翻译后的语音和文本。系统会自动检测您的语音并将音频发送到服务器，无需手动操作。

## 如何使用

### 1. 配置连接

qwen3.5-livetranslate-flash-realtime 模型通过 WebSocket 协议接入，连接时需要以下配置项：

该模型除 WebSocket 外，还支持通过 AOQ 和 WebRTC 协议接入；如果是客户端对接，且更看重稳定的延迟、弱网下的交互能力、实时双工的降噪与回声消除，可优先考虑 AOQ，协议对比与选型请参见 [Realtime API 概述](/developer-guides/realtime-api/overview)。

| 配置项  | 说明                                                                                                      |
| ---- | ------------------------------------------------------------------------------------------------------- |
| 调用地址 | `wss://dashscope.aliyuncs.com/api-ws/v1/realtime`                                                       |
| 查询参数 | 查询参数为 `model`，需指定为访问的模型名。示例：`?model=qwen3.5-livetranslate-flash-realtime`                               |
| 消息头  | 使用 Bearer Token 鉴权：`Authorization: Bearer $DASHSCOPE_API_KEY`。DASHSCOPE\_API\_KEY 是您在千问AI平台申请的 API Key。 |

使用以下 Python 示例代码建立连接。

<Accordion title="WebSocket 连接 Python 示例代码">
  ```python
  # pip install websocket-client
  import json
  import websocket
  import os

  API_KEY=os.getenv("DASHSCOPE_API_KEY")
  API_URL = "wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=qwen3.5-livetranslate-flash-realtime"

  headers = [
    "Authorization: Bearer " + API_KEY
  ]

  def on_open(ws):
    print(f"已连接到服务器：{API_URL}")
  def on_message(ws, message):
    data = json.loads(message)
    print("收到事件：", json.dumps(data, indent=2))
  def on_error(ws, error):
    print("错误：", error)

  ws = websocket.WebSocketApp(
    API_URL,
    header=headers,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error
  )

  ws.run_forever()
  ```
</Accordion>

### 2. 配置语种、输出模态与音色

发送客户端事件 [session.update](/api-reference/speech-translation/livetranslate-realtime/client-events#session-update)：

- **语言**

  - **源语言**： 使用 `session.input_audio_transcription.language` 参数。

    <Note>默认不填写，此时模型会自动识别源语种。</Note>

  - **目标语言**： 使用 `session.translation.language` 参数。

    <Note>默认值为 `en`（英语）。</Note>

  参见[支持的语种](#支持的语种)。

- **输出源语言识别结果**

  使用 `session.input_audio_transcription.model` 参数。将其设置为 `qwen3-asr-flash-realtime` 后，服务器除了返回翻译结果外，还会返回输入音频的语音识别结果（即源语言原文）。

  启用此功能后，服务器会返回以下事件：

  - `conversation.item.input_audio_transcription.text`：以流式方式返回识别结果。
  - `conversation.item.input_audio_transcription.completed`：识别完成后返回最终结果。
  - `conversation.item.input_audio_transcription.failed`：识别失败时返回错误信息。

- **输出模态**

  使用 `session.modalities` 参数。支持的值为 `["text"]`（仅文本）和 `["text","audio"]`（文本和音频）。

- **音色**

  使用 `session.voice` 参数。参见[支持的音色](#支持的音色)。

- **热词**

  使用 `session.translation.corpus.phrases` 参数。热词用于提升特定词汇的翻译准确性，以 key-value 形式指定源语言词汇与目标语言翻译的映射关系。示例：将`"人工智能"`指定翻译为`"Artificial Intelligence"`。

- **声音复刻**

  使用 `session.enable_voice_clone`、`session.voice_clone_options.frequency` 与 `session.voice` 参数。支持三种模式：使用预先复刻的音色（`frequency` 为 `never`）、服务端复刻一次（`once`）或每次复刻（`always`）。详见[声音复刻](#声音复刻)。

- **语音活动检测（VAD）与 Manual 模式**

  通过`session.turn_detection`参数配置语音起止的检测方式：

  - **VAD 模式**（默认）：`turn_detection`设为配置对象。服务端自动检测语音起止并自动触发翻译，适合客户端持续发送音频流的场景。
  - **Manual 模式**：`turn_detection`设为`null`。由客户端判断语音起止，说完一段话后主动发送`input_audio_buffer.commit`事件提交音频，适合"按下说话、松开发送"的场景。

  两种模式下的完整交互步骤参见本文[3. 输入音频与图片](#3-输入音频与图片)。

### 3. 输入音频与图片

客户端使用 [input\_audio\_buffer.append](/api-reference/speech-translation/livetranslate-realtime/client-events#input-audio-buffer-append) 和 [input\_image\_buffer.append](/api-reference/speech-translation/livetranslate-realtime/client-events#input-image-buffer-append) 事件发送 Base64 编码的音频和图像数据。音频输入为必需项，图像输入为可选项。

<Note>图像可以来自本地文件或实时视频流。</Note>

模型判断一段语音"说完了"的方式，取决于`turn_detection`参数配置的 VAD 模式或 Manual 模式：

- **VAD 模式**（默认）：客户端持续发送`input_audio_buffer.append`事件；服务端检测到语音开始/结束时，分别返回`input_audio_buffer.speech_started`、`input_audio_buffer.speech_stopped`事件，并自动提交音频缓冲区、触发翻译。翻译响应基于流式语音同步生成，通常在语音输入过程中就已开始，无需等待语音结束。

- **Manual 模式**：将`session.turn_detection`设为`null`。客户端发送完一段完整的语音后，主动发送`input_audio_buffer.commit`事件提交音频缓冲区；服务端返回`input_audio_buffer.committed`事件确认后，自动开始生成翻译响应，客户端无需再发送其他事件触发响应。提交前若需清空未提交的音频，可发送`input_audio_buffer.clear`事件。

### 4. 接收模型响应

翻译响应基于流式语音同步生成，通常无需等待语音结束（参见上一节 VAD/Manual 模式说明）。模型的响应格式取决于配置的输出模态。

- **仅文本输出**

  服务端通过 [response.text.text](/api-reference/speech-translation/livetranslate-realtime/server-events#response-text-text) 事件流式返回增量翻译文本（含已确认文本和待确认的预测文本）；翻译完成后，通过 [response.text.done](/api-reference/speech-translation/livetranslate-realtime/server-events#response-text-done) 事件返回完整的翻译文本。

- **文本和音频输出**

  - **文本**：通过 [response.audio\_transcript.text](/api-reference/speech-translation/livetranslate-realtime/server-events#response-audio-transcript-text) 事件流式返回增量翻译文本；翻译完成后，通过 [response.audio\_transcript.done](/api-reference/speech-translation/livetranslate-realtime/server-events#response-audio-transcript-done) 事件返回完整的翻译文本。
  - **音频**：增量式 Base64 编码的音频数据在 [response.audio.delta](/api-reference/speech-translation/livetranslate-realtime/server-events#response-audio-delta) 事件中返回。

<Warning>
  实时语音翻译模型使用`response.text.text`事件返回增量文本，与全双工语音对话（Omni）模型的`response.text.delta`事件不同，两者字段结构和语义有差异，请勿混用。
</Warning>

### 5. 结束会话

音频发送完毕后，客户端必须发送`session.finish`事件通知服务端，然后等待服务端返回`session.finished`事件后再关闭 WebSocket 连接。

<Warning>
  如果不发送`session.finish`，服务端无法得知音频输入已完成，会导致最后一段语音的识别和翻译结果丢失，连接也可能长时间处于等待状态。请务必在关闭连接前发送该事件。
</Warning>

## 声音复刻

模型支持发言人声音复刻功能，支持使用预先复刻的固定音色，也支持由服务端实时复刻，让翻译播报听起来像本人说外语。适用于跨语言演讲、个人主播、视频翻译等需要保留个人音色的场景。

在 [session.update](/api-reference/speech-translation/livetranslate-realtime/client-events#session-update) 中设置以下参数启用：

- `session.enable_voice_clone`：设置为 `true`，启用声音复刻。
- `session.voice_clone_options.frequency`：控制声音复刻时机，取值如下：
  - `never`：不在服务端复刻，使用用户预先复刻好的音色。此时 `session.voice` 需设置为用户自己的复刻音色 ID。
  - `once`：服务端在会话开始时基于输入音频复刻一次音色，后续翻译输出复用该音色。适合单人演讲场景。此时 `session.voice` 需设置为 `default`。
  - `always`：服务端在每次生成翻译音频前实时复刻，音色跟随输入动态变化。适合双人及以上对话场景。此时 `session.voice` 需设置为 `default`。
- `session.voice`：指定输出音色，取值取决于 `frequency` 的设置。
  - 设置为 `default`：搭配 `frequency` 为 `once` 或 `always` 使用，由服务端复刻输入音频的音色，复刻完成前使用默认音色过渡。
  - 设置为用户复刻的音色 ID（如 `qwen-translate-vc-xxx-yyy-zzz`）：搭配 `frequency` 为 `never` 使用。需提前通过声音复刻 API 准备音色，`targetModel` 需指定为 `qwen3.5-livetranslate-flash-realtime`。

<Note>当 `frequency` 为 `once` 或 `always` 时，`voice` 必须设置为 `default`，不可设置为其他预设音色，否则服务端会返回错误。</Note>

### 声音复刻配置示例

**使用预先复刻的音色**（音质稳定，推荐需要固定音色的场景）：

```json
{
  "type": "session.update",
  "session": {
    "modalities": ["text","audio"],
    "voice": "qwen-translate-vc-xxx-yyy-zzz",
    "translation": {
      "language": "en"
    },
    "enable_voice_clone": true,
    "voice_clone_options": {
      "frequency": "never"
    }
  }
}
```

**服务端复刻一次**（适合单人演讲）：

```json
{
  "type": "session.update",
  "session": {
    "modalities": ["text","audio"],
    "voice": "default",
    "translation": {
      "language": "en"
    },
    "enable_voice_clone": true,
    "voice_clone_options": {
      "frequency": "once"
    }
  }
}
```

**服务端每次复刻**（适合多人对话）：

```json
{
  "type": "session.update",
  "session": {
    "modalities": ["text","audio"],
    "voice": "default",
    "translation": {
      "language": "en"
    },
    "enable_voice_clone": true,
    "voice_clone_options": {
      "frequency": "always"
    }
  }
}
```

## 交互流程

实时语音翻译的交互流程遵循标准的 WebSocket 事件驱动模型。语音起止的判断方式取决于 VAD 模式或 Manual 模式（参见[3. 输入音频与图片](#3-输入音频与图片)），下表以 VAD 模式（默认）为主线，并标注了 Manual 模式下不同的服务端事件。

| 生命周期    | 客户端事件                                                                                                                        | 服务端事件                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ------- | ---------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 会话初始化   | session.update（会话配置）                                                                                                         | session.created（会话已创建）、session.updated（会话配置已更新）                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 用户音频输入  | input\_audio\_buffer.append（添加音频到缓冲区）、input\_image\_buffer.append（添加图片到缓冲区）、input\_audio\_buffer.commit（仅 Manual 模式，提交音频缓冲区） | **VAD 模式**：input\_audio\_buffer.speech\_started（检测到语音开始）、input\_audio\_buffer.speech\_stopped（检测到语音结束，服务端自动提交音频缓冲区）；**Manual 模式**：input\_audio\_buffer.committed（确认音频缓冲区已提交）                                                                                                                                                                                                                                                                                                                                                                        |
| 服务端音频输出 | 无                                                                                                                            | response.created（服务端开始生成响应）、response.output\_item.added（响应时有新的输出内容）、conversation.item.created（对话中创建新的消息项）、response.content\_part.added（新的输出内容添加到assistant message）、response.text.text（仅文本模态下增量生成的翻译文本）、response.audio\_transcript.text（音频+文本模态下增量生成的转录文字）、response.audio.delta（模型增量生成的音频）、response.text.done（仅文本模态下翻译文本完成）、response.audio\_transcript.done（音频+文本模态下文本转录完成）、response.audio.done（音频生成完成）、response.content\_part.done（Assistant message 的文本或音频内容流式输出完成）、response.output\_item.done（Assistant message 的整个输出项流式传输完成）、response.done（响应完成） |
| 会话结束    | session.finish（通知服务端音频发送完毕）                                                                                                  | session.finished（服务端完成处理，会话结束）                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

<Warning>
  音频发送结束后，必须发送`session.finish`事件并等待`session.finished`响应后再断开连接。如果直接关闭 WebSocket 而不发送`session.finish`，服务端无法得知音频输入已结束，将导致最后一段语音的识别和翻译结果丢失。
</Warning>

## 利用图像提升翻译准确率

qwen3.5-livetranslate-flash-realtime 模型可以接收图像输入，辅助音频翻译，适用于同音异义、低频专有名词识别场景。建议每秒发送不超过2张图片。

将以下示例图片下载到本地：[口罩.png](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250923/tjpeys/%E5%8F%A3%E7%BD%A9.png) 和 [面具.png](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250923/ifqttq/%E9%9D%A2%E5%85%B7.png)

将以下代码下载到`livetranslate_client.py`同级目录并运行，向麦克风说`"What is mask?"`，在输入口罩图片时，模型会翻译为"什么是口罩？"；输入面具图片时，模型会翻译为"什么是面具？"

```python
import os
import time
import json
import asyncio
import contextlib
import functools

from livetranslate_client import LiveTranslateClient

IMAGE_PATH = "mask_medical.png"
# IMAGE_PATH = "mask_masquerade.png"

def print_banner():
  print("=" * 60)
  print("  Powered by Qwen qwen3.5-livetranslate-flash-realtime - 单轮交互示例（口罩）")
  print("=" * 60 + "\n")

async def stream_microphone_once(client: LiveTranslateClient, image_bytes: bytes):
  pa = client.pyaudio_instance
  stream = pa.open(
    format=client.input_format,
    channels=client.input_channels,
    rate=client.input_rate,
    input=True,
    frames_per_buffer=client.input_chunk,
  )
  print(f"[INFO] 开始录音，请说话...")
  loop = asyncio.get_event_loop()
  last_img_time = 0.0
  frame_interval = 0.5  # 2 fps
  try:
    while client.is_connected:
      data = await loop.run_in_executor(None, stream.read, client.input_chunk)
      await client.send_audio_chunk(data)

      # 每 0.5 秒追加一帧图像
      now = time.time()
      if now - last_img_time >= frame_interval:
        await client.send_image_frame(image_bytes)
        last_img_time = now
  finally:
    stream.stop_stream()
    stream.close()

async def main():
  print_banner()
  api_key = os.environ.get("DASHSCOPE_API_KEY")
  if not api_key:
    print("[ERROR] 请先在 DASHSCOPE_API_KEY 环境变量中配置 API Key。")
    return

  client = LiveTranslateClient(api_key=api_key, target_language="zh", audio_enabled=True)

  def on_text(text: str):
    print(text, end="", flush=True)

  try:
    await client.connect()
    client.start_audio_player()
    message_task = asyncio.create_task(client.handle_server_messages(on_text))
    with open(IMAGE_PATH, "rb") as f:
      img_bytes = f.read()
    await stream_microphone_once(client, img_bytes)
    await asyncio.sleep(15)
  finally:
    await client.close()
    if not message_task.done():
      message_task.cancel()
      with contextlib.suppress(asyncio.CancelledError):
        await message_task

if __name__ == "__main__":
  asyncio.run(main())
```

## 计费说明

**Qwen3.5-LiveTranslate-Flash-Realtime**

- **音频**：输入每秒音频消耗 7 Token，输出每秒音频消耗 12.5 Token。
- **图片**：每输入 32×32 像素消耗 0.5 Token。
- **文本**：启用源语言语音识别功能后，服务除返回翻译结果外，还会返回输入音频的语音识别文本（即源语言原文），该识别文本将按输出文本的 Token 标准计费。

**Qwen3-LiveTranslate-Flash-Realtime**

- **音频**：输入或输出每秒音频均消耗 12.5 Token。
- **图片**：每输入 28×28 像素消耗 0.5 Token。
- **文本**：启用源语言语音识别功能后，服务除返回翻译结果外，还会返回输入音频的语音识别文本（即源语言原文），该识别文本将按输出文本的 Token 标准计费。

Token 费用请参见[模型列表](/developer-guides/getting-started/model-selection)。

## 限流说明

模型的限流规则请参见[限流](/developer-guides/administration/rate-limits)。

## 支持的语种

下表中的语种代码可用于指定源语种与目标语种。

<Note>部分目标语种仅支持输出文本，不支持输出音频。老模型 qwen3-livetranslate-flash-realtime 仅支持以下 18 种语种：en、zh、ru、fr、de、pt、es、it、id、ko、ja、vi、th、ar、yue、hi、el、tr。</Note>

| 语种代码 | 语种      | 支持的输出 |
| ---- | ------- | ----- |
| zh   | 中文      | 音频+文本 |
| en   | 英语      | 音频+文本 |
| ar   | 阿拉伯语    | 音频+文本 |
| de   | 德语      | 音频+文本 |
| fr   | 法语      | 音频+文本 |
| es   | 西班牙语    | 音频+文本 |
| pt   | 葡萄牙语    | 音频+文本 |
| id   | 印度尼西亚语  | 音频+文本 |
| it   | 意大利语    | 音频+文本 |
| ko   | 韩语      | 音频+文本 |
| ru   | 俄语      | 音频+文本 |
| th   | 泰语      | 音频+文本 |
| vi   | 越南语     | 音频+文本 |
| ja   | 日语      | 音频+文本 |
| tr   | 土耳其语    | 音频+文本 |
| hi   | 印地语     | 音频+文本 |
| ms   | 马来语     | 音频+文本 |
| nl   | 荷兰语     | 音频+文本 |
| ur   | 乌尔都语    | 音频+文本 |
| nb   | 挪威语     | 音频+文本 |
| sv   | 瑞典语     | 音频+文本 |
| da   | 丹麦语     | 音频+文本 |
| he   | 希伯来语    | 音频+文本 |
| fi   | 芬兰语     | 音频+文本 |
| pl   | 波兰语     | 音频+文本 |
| is   | 冰岛语     | 音频+文本 |
| cs   | 捷克语     | 音频+文本 |
| fil  | 菲律宾语    | 音频+文本 |
| fa   | 波斯语     | 音频+文本 |
| yue  | 粤语      | 文本    |
| el   | 希腊语     | 文本    |
| af   | 南非荷兰语   | 文本    |
| ast  | 阿斯图里亚斯语 | 文本    |
| be   | 白俄罗斯语   | 文本    |
| bg   | 保加利亚语   | 文本    |
| bn   | 孟加拉语    | 文本    |
| bs   | 波斯尼亚语   | 文本    |
| ca   | 加泰罗尼亚语  | 文本    |
| ceb  | 宿务语     | 文本    |
| et   | 爱沙尼亚语   | 文本    |
| gl   | 加利西亚语   | 文本    |
| gu   | 古吉拉特语   | 文本    |
| hr   | 克罗地亚语   | 文本    |
| hu   | 匈牙利语    | 文本    |
| jv   | 爪哇语     | 文本    |
| kk   | 哈萨克语    | 文本    |
| kn   | 卡纳达语    | 文本    |
| ky   | 柯尔克孜语   | 文本    |
| lv   | 拉脱维亚语   | 文本    |
| mk   | 马其顿语    | 文本    |
| ml   | 马拉雅拉姆语  | 文本    |
| mr   | 马拉地语    | 文本    |
| pa   | 旁遮普语    | 文本    |
| ro   | 罗马尼亚语   | 文本    |
| sk   | 斯洛伐克语   | 文本    |
| sl   | 斯洛文尼亚语  | 文本    |
| sw   | 斯瓦希里语   | 文本    |
| tg   | 塔吉克语    | 文本    |
| az   | 阿塞拜疆语   | 文本    |
| uk   | 乌克兰语    | 文本    |

## 支持的音色

当输出包含合成语音时，需设置 `voice` 参数。不填写该参数时，模型将使用各节顶部标注的默认音色。

### Qwen3.5-LiveTranslate-Flash-Realtime

默认音色为 `Tina`。

| 音色名称          | `voice` 参数 | 描述                                | 支持的语言                                                                                                                        |
| ------------- | ---------- | --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| 甜甜 Tina       | Tina       | 我的声音像温热的奶茶，甜甜的、暖暖的，但解决问题可一点都不含糊哦！ | 中文（普通话）、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语、泰语、印度尼西亚语、阿拉伯语、越南语、土耳其语、芬兰语、波兰语、印地语、荷兰语、捷克语、乌尔都语、菲律宾语、瑞典语、丹麦语、希伯来语、冰岛语、马来语、挪威语、波斯语  |
| 林欣宜 Cindy     | Cindy      | 台湾说话嗲嗲的小姐姐                        | 中文（台湾口音）、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语、泰语、印度尼西亚语、阿拉伯语、越南语、土耳其语、芬兰语、波兰语、印地语、荷兰语、捷克语、乌尔都语、菲律宾语、瑞典语、丹麦语、希伯来语、冰岛语、马来语、挪威语、波斯语 |
| 清欢 Liora Mira | Liora Mira | 用声音织就烟火人间的温柔                      | 中文（普通话）、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语、泰语、印度尼西亚语、阿拉伯语、越南语、土耳其语、芬兰语、波兰语、印地语、荷兰语、捷克语、乌尔都语、菲律宾语、瑞典语、丹麦语、希伯来语、冰岛语、马来语、挪威语、波斯语  |
| 知芝 Sunnybobi  | Sunnybobi  | 大大咧咧的社恐邻家姑娘                       | 中文（普通话）、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语、泰语、印度尼西亚语、阿拉伯语、越南语、土耳其语、芬兰语、波兰语、印地语、荷兰语、捷克语、乌尔都语、菲律宾语、瑞典语、丹麦语、希伯来语、冰岛语、马来语、挪威语、波斯语  |
| 林川野 Raymond   | Raymond    | 声音清亮，爱吃外卖的宅男                      | 中文（普通话）、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语、泰语、印度尼西亚语、阿拉伯语、越南语、土耳其语、芬兰语、波兰语、印地语、荷兰语、捷克语、乌尔都语、菲律宾语、瑞典语、丹麦语、希伯来语、冰岛语、马来语、挪威语、波斯语  |
| 晨煦 Ethan      | Ethan      | 标准普通话，带部分北方口音。阳光、温暖、活力、朝气         | 中文（普通话）、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语、泰语、印度尼西亚语、阿拉伯语、越南语、土耳其语、芬兰语、波兰语、印地语、荷兰语、捷克语、乌尔都语、菲律宾语、瑞典语、丹麦语、希伯来语、冰岛语、马来语、挪威语、波斯语  |
| 予安 Theo Calm  | Theo Calm  | 在静默处传递理解，在言语间疗愈人心。                | 中文（普通话）、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语、泰语、印度尼西亚语、阿拉伯语、越南语、土耳其语、芬兰语、波兰语、印地语、荷兰语、捷克语、乌尔都语、菲律宾语、瑞典语、丹麦语、希伯来语、冰岛语、马来语、挪威语、波斯语  |

### Qwen3-LiveTranslate-Flash-Realtime

默认音色为 `Cherry`。

| 音色名称     | `voice` 参数 | 描述                      | 支持的语言                               |
| -------- | ---------- | ----------------------- | ----------------------------------- |
| Cherry   | Cherry     | 活泼、友好、真诚的年轻女性。          | 中文、英文、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
| Nofish   | Nofish     | 一位平翘舌不太分的设计师。           | 中文、英文、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
| 上海-Jada  | Jada       | 风风火火、精力充沛的上海阿姐。         | 中文                                  |
| 北京-Dylan | Dylan      | 在胡同里长大的北京小伙。            | 中文                                  |
| 四川-Sunny | Sunny      | 一位来自四川的甜美女孩。            | 中文                                  |
| 天津-Peter | Peter      | 天津相声演员风格的声音（捧哏）。        | 中文                                  |
| 粤语-Kiki  | Kiki       | 来自香港的甜美闺蜜。              | 粤语                                  |
| 四川-Eric  | Eric       | 来自成都的非主流男生，特立独行。        | 中文                                  |
| Ethan    | Ethan      | 标准普通话略带北方口音。阳光、温暖、活力充沛。 | 中文、英文、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |

## API 参考

- [客户端事件](/api-reference/speech-translation/livetranslate-realtime/client-events)
- [服务端事件](/api-reference/speech-translation/livetranslate-realtime/server-events)
- [Python SDK](/api-reference/speech-translation/livetranslate-realtime/python-sdk)
- [Java SDK](/api-reference/speech-translation/livetranslate-realtime/java-sdk)
- [AOQ 客户端 API](/developer-guides/realtime-api/aoq-sdk-intro)
- [Realtime API 概述](/developer-guides/realtime-api/overview)（WebRTC 协议说明）
