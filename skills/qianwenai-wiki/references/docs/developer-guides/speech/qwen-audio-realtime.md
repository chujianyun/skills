> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 实时语音对话（Qwen-Audio-Realtime）

> Qwen-Audio 是端到端实时语音交互大模型，支持低延迟语音对话，适用于语音助手、智能客服、AI 伴侣等场景。

## 概述

实现实时音频到语音/文本的转换，支持流式音频输入和流式语音与文本输出。

该模型除 WebSocket 协议外，还支持通过 AOQ 和 WebRTC 协议接入；如果是客户端对接，且更看重稳定的延迟、弱网下的交互能力、实时双工的降噪与回声消除，可优先考虑 AOQ，协议对比与选型请参见[模型/应用支持力度](/developer-guides/realtime-api/overview#模型支持力度)。

- 支持三种交互模式：声学 VAD（server\_vad）、智能语义轮次（smart\_turn）和手动控制（push-to-talk）
- 独有的 smart\_turn 模式融合声学感知与语义理解判断轮次边界，无意义附和声（如“嗯”“啊”）不会打断对话
- 支持 Function Calling 工具调用，模型可自主判断是否需要调用外部工具获取信息
- 支持对话上下文管理（创建、查询、删除对话项），灵活注入历史上下文或清理无关对话项
- 高表现力语音输出，根据对话语境动态调整语气、节奏和情感表达
- 支持系统音色与声音复刻音色，可通过声音复刻创建专属 AI 音色用于语音对话输出
- smart\_turn 模式下支持说话人增强，传入目标用户预录音频后，模型可在双工对话中精准锁定目标说话人，有效屏蔽旁人声音与背景噪声

### 工作原理

Qwen-Audio 采用事件驱动架构。客户端与服务端通过持久连接同时收发数据：客户端持续发送麦克风采集的音频流，服务端实时返回语音和文本响应。整个交互过程由客户端事件（如`session.update`、`input_audio_buffer.append`）和服务端事件（如`response.audio.delta`、`response.done`）驱动，无需轮询。

典型的连接生命周期为：建立 WebSocket 连接 → 发送`session.update`配置会话参数 → 持续发送音频并接收响应 → 主动关闭连接。

### 音频格式

| 方向            | 格式  | 规格                     |
| ------------- | --- | ---------------------- |
| 输入（客户端 → 服务端） | PCM | 16kHz 采样率，16bit 位深，单声道 |
| 输出（服务端 → 客户端） | PCM | 24kHz 采样率，16bit 位深，单声道 |

### 上下文容量

模型会维护对话历史上下文，当对话轮次或累计音频时长超过以下限制时，将自动丢弃更早的历史信息。最大时长指模型上下文中能保留的音频累计时长上限。

| 模型                            | 音频最大轮次 | 音频最大时长 |
| ----------------------------- | ------ | ------ |
| qwen-audio-3.0-realtime-plus  | 50     | 300秒   |
| qwen-audio-3.0-realtime-flash | 50     | 300秒   |

音频最大轮次的默认值为 20 轮，最大可上调至 50 轮。调节方式请参见[历史轮次控制](#历史轮次控制)。

全模态模型的整体选型建议请参见[全模态](/developer-guides/getting-started/vision-models)。

## 前提条件

- 已[获取API Key](/api-reference/preparation/api-key)并将其[配置到环境变量](/api-reference/preparation/export-api-key-env)。
- 如果通过 AOQ 协议接入，需要下载并集成 AOQ 客户端 SDK，详见 [AOQ SDK 简介](/developer-guides/realtime-api/aoq-sdk-intro)。

## 快速开始

通过以下步骤快速体验与 Qwen-Audio 模型的实时语音对话。

<Note>
  各模式下客户端与服务端的 WebSocket 事件交互时序，请参见[事件交互流程](/api-reference/qwen-audio-realtime/websocket-api)。
</Note>

以下示例通过 WebSocket 原生连接，使用 server\_vad 模式实现麦克风实时对话。运行前需安装依赖：

<Tabs>
  <Tab title="macOS">
    ```bash
    brew install portaudio && pip install pyaudio websockets
    ```
  </Tab>

  <Tab title="Debian/Ubuntu">
    ```bash
    sudo apt install -y python3-dev portaudio19-dev && pip install pyaudio websockets
    ```
  </Tab>

  <Tab title="Windows">
    ```powershell
    pip install pyaudio websockets
    ```
  </Tab>
</Tabs>

将以下代码保存为`realtime_quickstart.py`：

```python
import asyncio
import base64
import json
import os
import pyaudio
import websockets
API_KEY = os.environ["DASHSCOPE_API_KEY"]
URL = "wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=qwen-audio-3.0-realtime-plus"
pya = pyaudio.PyAudio()
mic = pya.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)
spk = pya.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)
async def main():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    async with websockets.connect(URL, additional_headers=headers) as ws:
        await ws.send(json.dumps({
            "type": "session.update",
            "session": {
                "modalities": ["text", "audio"],
                "voice": "longanqian",
                "turn_detection": {
                    "type": "server_vad",
                    "threshold": 0.5,
                    "silence_duration_ms": 800
                }
            }
        }))
        async def send_audio():
            while True:
                data = await asyncio.to_thread(mic.read, 3200, False)
                await ws.send(json.dumps({
                    "type": "input_audio_buffer.append",
                    "audio": base64.b64encode(data).decode()
                }))
                await asyncio.sleep(0.02)
        async def recv_events():
            async for msg in ws:
                event = json.loads(msg)
                t = event["type"]
                if t == "response.audio.delta":
                    audio = base64.b64decode(event["delta"])
                    await asyncio.to_thread(spk.write, audio)
                elif t == "conversation.item.input_audio_transcription.completed":
                    print(f"[You] {event['transcript']}")
                elif t == "response.audio_transcript.done":
                    print(f"[AI] {event['transcript']}")
                elif t == "error":
                    print(f"[Error] {event['error']['message']}")
        await asyncio.gather(send_audio(), recv_events())
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        mic.close()
        spk.close()
        pya.terminate()
        print("\n对话结束")
```

运行`python realtime_quickstart.py`，对着麦克风说话即可与模型实时对话。服务端自动检测语音起止并触发响应。

**完整示例**

以下完整示例在基础对话之上，增加了语音打断处理、回声抑制等功能。新建以下两个文件（需在同一目录下）：

<Accordion title="B64PCMPlayer.py">
  ```python
  import contextlib
  import time
  import pyaudio
  import threading
  import queue
  import base64
  class B64PCMPlayer:
      def __init__(self, pya: pyaudio.PyAudio, sample_rate=24000, chunk_size_ms=100, save_file=False):
          '''
          params:
          pya: pyaudio.PyAudio
          sample_rate: int, sample rate of audio
          chunk_size_ms: int, chunk size of audio in milliseconds, this will effect cancel latency
          '''
          self.pya = pya
          self.sample_rate = sample_rate
          self.chunk_size_bytes = chunk_size_ms * sample_rate *2 // 1000
          self.player_stream = pya.open(format=pyaudio.paInt16,
                  channels=1,
                  rate=sample_rate,
                  output=True)
          self.raw_audio_buffer: queue.Queue = queue.Queue()
          self.b64_audio_buffer: queue.Queue = queue.Queue()
          self.status_lock = threading.Lock()
          self.status = 'playing'
          self._is_writing = False
          self.decoder_thread = threading.Thread(target=self.decoder_loop)
          self.player_thread = threading.Thread(target=self.player_loop)
          self.decoder_thread.start()
          self.player_thread.start()
          self.complete_event: threading.Event = None
          self.save_file = save_file
          if self.save_file:
              self.out_file = open('result.pcm', 'wb')
      def decoder_loop(self):
          while self.status != 'stop':
              recv_audio_b64 = None
              with contextlib.suppress(queue.Empty):
                  recv_audio_b64 = self.b64_audio_buffer.get(timeout=0.1)
              if recv_audio_b64 is None:
                  continue
              recv_audio_raw = base64.b64decode(recv_audio_b64)
              # push raw audio data into queue by chunk
              for i in range(0, len(recv_audio_raw), self.chunk_size_bytes):
                  chunk = recv_audio_raw[i:i + self.chunk_size_bytes]
                  self.raw_audio_buffer.put(chunk)
                  if self.save_file:
                      self.out_file.write(chunk)
      def player_loop(self):
          while self.status != 'stop':
              recv_audio_raw = None
              with contextlib.suppress(queue.Empty):
                  recv_audio_raw = self.raw_audio_buffer.get(timeout=0.1)
              if recv_audio_raw is None:
                  self._is_writing = False
                  if self.complete_event:
                      self.complete_event.set()
                  continue
              self._is_writing = True
              self.player_stream.write(recv_audio_raw)
      def is_playing(self):
          return self._is_writing or not self.b64_audio_buffer.empty() or not self.raw_audio_buffer.empty()
      def cancel_playing(self):
          self.b64_audio_buffer.queue.clear()
          self.raw_audio_buffer.queue.clear()
      def add_data(self, data):
          self.b64_audio_buffer.put(data)
      def wait_for_complete(self):
          self.complete_event = threading.Event()
          self.complete_event.wait()
          self.complete_event = None
      def shutdown(self):
          self.status = 'stop'
          self.decoder_thread.join()
          self.player_thread.join()
          self.player_stream.close()
          if self.save_file:
              self.out_file.close()
  ```
</Accordion>

<Accordion title="realtime_demo.py">
  <Note>
    若`websockets`版本低于 11，需将代码中的`additional_headers`改为`extra_headers`，或升级：`pip install --upgrade websockets`。
  </Note>

  ```python
  import asyncio
  import base64
  import json
  import os
  import struct
  import time
  import traceback
  from enum import Enum
  from typing import Optional, Callable, Dict, Any
  import pyaudio
  import websockets
  from B64PCMPlayer import B64PCMPlayer
  class TurnDetectionMode(Enum):
      SERVER_VAD = "server_vad"
      SEMANTIC_VAD = "smart_turn"
      MANUAL = "manual"
  class FunRealtimeClient:
      def __init__(
              self,
              base_url,
              api_key: str,
              model: str = "",
              voice: str = "longanqian",
              instructions: str = "",
              turn_detection_mode: TurnDetectionMode = TurnDetectionMode.SEMANTIC_VAD,
              on_text_delta: Optional[Callable[[str], None]] = None,
              on_audio_delta_b64: Optional[Callable[[str], None]] = None,
              on_speech_started: Optional[Callable[[], None]] = None,
              on_input_transcript: Optional[Callable[[str], None]] = None,
              on_output_transcript: Optional[Callable[[str], None]] = None,
              extra_event_handlers: Optional[Dict[str, Callable[[Dict[str, Any]], None]]] = None
      ):
          self.base_url = base_url
          self.api_key = api_key
          self.model = model
          self.voice = voice
          self.instructions = instructions
          self.ws = None
          self.on_text_delta = on_text_delta
          # 回调参数为 base64 编码的 PCM 音频
          self.on_audio_delta_b64 = on_audio_delta_b64
          self.on_speech_started = on_speech_started
          self.on_input_transcript = on_input_transcript
          self.on_output_transcript = on_output_transcript
          self.turn_detection_mode = turn_detection_mode
          self.extra_event_handlers = extra_event_handlers or {}
          # 回复状态跟踪（用于打断处理和回声抑制）
          self._current_response_id = None
          self._current_item_id = None
          self._is_responding = False
          self._audio_suppressed = False
          # 输入/输出转录打印状态
          self._print_input_transcript = True
          self._output_transcript_buffer = ""
      async def connect(self) -> None:
          """建立 WebSocket 连接并发送会话配置。"""
          url = f"{self.base_url}?model={self.model}"
          headers = {
              "Authorization": f"Bearer {self.api_key}",
              "x-dashscope-dataInspection": "disable",
          }
          self.ws = await websockets.connect(url, additional_headers=headers)
          # 会话配置
          session_config = {
              "modalities": ["text", "audio"],
              "voice": self.voice,
              "instructions": self.instructions,
              "input_audio_format": "pcm",
              "output_audio_format": "pcm",
              "turn_detection": {}
          }
          if self.turn_detection_mode == TurnDetectionMode.MANUAL:
              session_config['turn_detection'] = None
              await self.update_session(session_config)
          elif self.turn_detection_mode == TurnDetectionMode.SERVER_VAD:
              session_config['turn_detection'] = {
                  "type": "server_vad",
                  "threshold": 0.1,
                  "silence_duration_ms": 900
              }
              await self.update_session(session_config)
          elif self.turn_detection_mode == TurnDetectionMode.SEMANTIC_VAD:
              session_config['turn_detection'] = {
                  "type": "smart_turn"
              }
              await self.update_session(session_config)
          else:
              raise ValueError(f"Invalid turn detection mode: {self.turn_detection_mode}")
      async def send_event(self, event) -> None:
          event['event_id'] = "event_" + str(int(time.time() * 1000))
          await self.ws.send(json.dumps(event))
      async def update_session(self, config: Dict[str, Any]) -> None:
          """更新会话配置。"""
          event = {
              "type": "session.update",
              "session": config
          }
          await self.send_event(event)
      async def stream_audio(self, audio_chunk: bytes) -> None:
          """向 API 流式发送原始音频数据。"""
          # 仅支持 16bit 16kHz 单声道 PCM
          audio_b64 = base64.b64encode(audio_chunk).decode()
          append_event = {
              "type": "input_audio_buffer.append",
              "audio": audio_b64
          }
          await self.send_event(append_event)
      async def commit_audio_buffer(self) -> None:
          """提交音频缓冲区以触发处理。"""
          event = {
              "type": "input_audio_buffer.commit"
          }
          await self.send_event(event)
      async def create_response(self) -> None:
          """向 API 请求生成回复（仅在手动模式下需要调用）。"""
          event = {
              "type": "response.create"
          }
          await self.send_event(event)
      async def cancel_response(self) -> None:
          """取消当前回复。"""
          event = {
              "type": "response.cancel"
          }
          await self.send_event(event)
      async def handle_interruption(self):
          """处理用户对当前回复的打断。"""
          if not self._is_responding:
              return
          # 抑制后续残余音频，直到新 response 开始
          self._audio_suppressed = True
          # 取消当前回复
          if self._current_response_id:
              await self.cancel_response()
          self._is_responding = False
          self._current_response_id = None
          self._current_item_id = None
      @staticmethod
      def _format_event_for_log(event: Dict[str, Any]) -> str:
          """打印事件 JSON。对 response.audio.delta 的 base64 音频做脱敏，避免刷屏。"""
          event_type = event.get("type")
          if event_type == "response.audio.delta":
              delta = event.get("delta", "")
              redacted = dict(event)
              redacted["delta"] = f"<audio b64 omitted, length={len(delta)}>"
              return json.dumps(redacted, ensure_ascii=False)
          return json.dumps(event, ensure_ascii=False)
      async def handle_messages(self) -> None:
          try:
              async for message in self.ws:
                  event = json.loads(message)
                  event_type = event.get("type")
                  # 打印完整服务端事件（audio.delta 脱敏）
                  print(self._format_event_for_log(event))
                  if event_type == "error":
                      continue
                  elif event_type == "response.created":
                      self._current_response_id = event.get("response", {}).get("id")
                      self._is_responding = True
                      self._audio_suppressed = False
                  elif event_type == "response.output_item.added":
                      self._current_item_id = event.get("item", {}).get("id")
                  elif event_type == "response.done":
                      self._is_responding = False
                      self._current_response_id = None
                      self._current_item_id = None
                  elif event_type == "input_audio_buffer.speech_started":
                      # 打断时清空已缓存的音频，立即停止播放
                      print("----------------Speech Started----------------")
                      if self.on_speech_started:
                          self.on_speech_started()
                      if self._is_responding:
                          await self.handle_interruption()
                  elif event_type == "response.audio.delta":
                      if self._audio_suppressed:
                          continue
                      if self.on_audio_delta_b64:
                          self.on_audio_delta_b64(event["delta"])
                  elif event_type in self.extra_event_handlers:
                      self.extra_event_handlers[event_type](event)
                  elif event_type == "input_audio_buffer.speech_stopped":
                      print("----------------Speech Stopped----------------")
          except websockets.exceptions.ConnectionClosed:
              print(" Connection closed")
          except Exception as e:
              print(" Error in message handling: ", str(e))
              traceback.print_exc()
      async def close(self) -> None:
          """关闭 WebSocket 连接。"""
          if self.ws:
              await self.ws.close()
  def _audio_energy(audio_data: bytes) -> float:
      count = len(audio_data) // 2
      if count == 0:
          return 0.0
      samples = struct.unpack(f'<{count}h', audio_data)
      return sum(abs(s) for s in samples) / count
  async def record_and_send(client, player, echo_suppression=True):
      p = pyaudio.PyAudio()
      stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)
      print("开始录音，请讲话...")
      if echo_suppression:
          print("提示：回声抑制已开启（AI 说话期间麦克风静音，不支持打断）。如使用耳机请设置 echo_suppression=False 以启用打断。")
      else:
          print("提示：耳机模式，支持语音打断。")
      playback_end_time = 0.0
      NOISE_GATE_THRESHOLD = 500
      try:
          while True:
              audio_data = await asyncio.to_thread(stream.read, 3200, False)
              if echo_suppression:
                  is_active = client._is_responding or player.is_playing()
                  if is_active:
                      playback_end_time = time.time()
                      await asyncio.sleep(0.02)
                      continue
                  if time.time() - playback_end_time < 0.5:
                      await asyncio.sleep(0.02)
                      continue
              else:
                  if client._is_responding or player.is_playing():
                      if _audio_energy(audio_data) < NOISE_GATE_THRESHOLD:
                          await asyncio.sleep(0.02)
                          continue
              await client.stream_audio(audio_data)
              await asyncio.sleep(0.02)
      finally:
          stream.stop_stream(); stream.close(); p.terminate()
  async def main():
      pya = pyaudio.PyAudio()
      # 输出采样率 24kHz，匹配服务端音频格式
      player = B64PCMPlayer(pya, sample_rate=24000)
      client = FunRealtimeClient(
                  base_url="wss://dashscope.aliyuncs.com/api-ws/v1/realtime",
          api_key=os.environ['DASHSCOPE_API_KEY'],
          model="qwen-audio-3.0-realtime-plus",
          voice="longanqian",
          turn_detection_mode=TurnDetectionMode.SERVER_VAD,
          on_audio_delta_b64=player.add_data,
          # 语音打断时清空播放缓冲
          on_speech_started=player.cancel_playing,
      )
      await client.connect()
      print("连接成功，开始实时对话...")
      try:
          # 并发运行：消息处理 + 麦克风采集
          await asyncio.gather(client.handle_messages(), record_and_send(client, player, echo_suppression=False))
      finally:
          await client.close()
          player.shutdown()
          pya.terminate()
  if __name__ == "__main__":
      try:
          asyncio.run(main())
      except KeyboardInterrupt:
          print("\n程序已退出。")
  ```
</Accordion>

运行`python realtime_demo.py`，对着麦克风说话即可与模型实时对话。系统会自动检测语音起止并触发响应。

<Note>
  以上示例使用 server\_vad 模式（服务端声学 VAD 自动检测语音起止）。如需使用 smart\_turn（智能语义轮次）或 push-to-talk（手动控制）模式，请参见[交互模式](#交互模式)。
</Note>

## 会话配置

### 交互模式

Qwen-Audio 支持三种交互模式：`server_vad`（声学 VAD 自动检测语音起止）、`smart_turn`（智能语义轮次，声学与语义融合判断）和 push-to-talk（客户端手动控制）。各模式的详细说明及事件交互时序（含时序图），请参见[交互模式](/api-reference/qwen-audio-realtime/websocket-api)。

<Warning>
  `turn_detection`仅在首次发送音频之前（IDLE 状态）允许修改。会话建立后切换交互模式需要重新连接。
</Warning>

通过`session.update`事件中的`turn_detection`字段切换交互模式：

- **server\_vad**：

```json
{
    "type": "session.update",
    "session": {
        "turn_detection": {
            "type": "server_vad",
            "threshold": 0.5,
            "silence_duration_ms": 500
        }
    }
}
```

- **smart\_turn**：

```json
{
    "type": "session.update",
    "session": {
        "turn_detection": {
            "type": "smart_turn"
        }
    }
}
```

- **push-to-talk**：

```json
{
    "type": "session.update",
    "session": {
        "turn_detection": null
    }
}
```

**push-to-talk 模式完整示例**：

<Accordion title="manual_realtime.py">
  ```python
  # pip install websockets pyaudio
  import json
  import os
  import base64
  import threading
  import time
  import pyaudio
  import websocket
  API_KEY = os.getenv("DASHSCOPE_API_KEY")
  API_URL = "wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=qwen-audio-3.0-realtime-plus"
  pya = pyaudio.PyAudio()
  out_stream = pya.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)
  ws_ref = [None]
  resp_done = threading.Event()
  def on_open(ws):
      ws_ref[0] = ws
      # 配置 push-to-talk 模式（turn_detection 设为 null）
      ws.send(json.dumps({
          "type": "session.update",
          "session": {
              "modalities": ["audio", "text"],
              "voice": "longanqian",
              "turn_detection": None
          }
      }))
  def on_message(ws, message):
      event = json.loads(message)
      event_type = event["type"]
      if event_type == "response.audio.delta":
          out_stream.write(base64.b64decode(event["delta"]))
      elif event_type == "conversation.item.input_audio_transcription.completed":
          print(f"[User] {event['transcript']}")
      elif event_type == "response.audio_transcript.done":
          print(f"[LLM] {event['transcript']}")
      elif event_type == "response.done":
          resp_done.set()
      elif event_type == "error":
          print(f"[Error] {event['error']['message']}")
  def on_error(ws, error):
      print(f"Error: {error}")
  def record_and_send(ws):
      mic = pya.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)
      stop = threading.Event()
      def reader():
          while not stop.is_set():
              try:
                  data = mic.read(3200, exception_on_overflow=False)
                  ws.send(json.dumps({
                      "type": "input_audio_buffer.append",
                      "audio": base64.b64encode(data).decode()
                  }))
              except Exception:
                  break
      t = threading.Thread(target=reader, daemon=True)
      t.start()
      input()
      stop.set()
      t.join(timeout=1.0)
      mic.close()
  headers = ["Authorization: Bearer " + API_KEY]
  ws = websocket.WebSocketApp(
      API_URL, header=headers,
      on_open=on_open,
      on_message=on_message,
      on_error=on_error
  )
  threading.Thread(target=ws.run_forever, daemon=True).start()
  time.sleep(2)
  try:
      turn = 1
      while True:
          print(f"\n--- 第 {turn} 轮对话 ---")
          cmd = input("按 Enter 开始录音（输入 q 退出）...")
          if cmd.strip().lower() in ["q", "quit"]:
              break
          print("录音中... 再次按 Enter 停止。")
          record_and_send(ws_ref[0])
          resp_done.clear()
          # 提交音频并触发推理
          ws_ref[0].send(json.dumps({"type": "input_audio_buffer.commit"}))
          ws_ref[0].send(json.dumps({
              "type": "response.create",
              "response": {"modalities": ["audio", "text"]}
          }))
          print("等待模型回复...")
          resp_done.wait(timeout=30)
          turn += 1
  except KeyboardInterrupt:
      pass
  finally:
      ws.close()
      out_stream.close()
      pya.terminate()
      print("\n对话结束")
  ```
</Accordion>

### 系统指令

通过`instructions`参数可以设定模型的角色身份、回答风格和行为偏好。该参数在`session.update`中配置，对整个会话生效。

```json
{
    "type": "session.update",
    "session": {
        "instructions": "你是一位专业的旅行顾问，回答简洁、友好，优先推荐性价比高的方案。"
    }
}
```

**使用建议**：

- 明确角色身份（如"你是一位智能语音助手"、"你是一位英语口语老师"），可附加名称、性别等人设细节。
- 指定口语化的语气和措辞风格，同时强调口语化不影响内容完整性——细节、数字、具体建议一个都不能少，只是换一种轻松自然的方式表达。
- 要求模型充分考虑对话上下文中的所有约束条件（如预算、偏好、禁忌、之前达成的共识），涉及多个条件时逐一回应，不遗漏关键信息。
- 控制输出格式：除非用户要求，禁止输出 emoji 等特殊符号和 Markdown 格式，尽量输出纯文本，以保证 TTS 朗读效果自然流畅。
- 明确回应策略：简单日常闲聊、打招呼保持简洁自然；涉及推理计算、多条件约束、推荐列表、安全建议等复杂问题，以回答完整正确为优先，确保关键信息（如价格、地点、条件）完整，避免铺垫或重复修辞。
- 设定追问策略：遵循"先把用户当前问题答好，再在结尾自然追问推进话题"的原则，一次只问一个问题，不连续追问或反复确认。

**默认配置**

以下为适用于通用语音对话场景的推荐 instructions 配置，涵盖角色设定、口语风格、格式控制和追问策略，可直接使用或按需调整：

```text
你是一位智能语音助手，你的名字是小云，性别女，声音甜美，举止亲切，你能回复用户的各种问题。请你按照下面的要求聊天：
1. 像朋友之间聊天那样，语气自然友好，避免使用正式的称谓和模板化的表达。口语化只影响你的措辞和语气，不影响内容的完整性，该说的细节、数字、具体建议一个都不能少，只是用轻松自然的方式说出来。
2. 充分考虑对话上下文中提到的所有约束条件（如预算、偏好、禁忌、之前达成的共识等），涉及多个条件或需要综合判断时逐一回应，不要遗漏关键信息。
3. 除非用户要求，不要输出emoji等特殊符号，不要输出Markdown格式，尽量输出纯文本。
4. 对于简单的日常闲聊、打招呼、情感回应，保持简洁自然。对于涉及事实判断、推理计算、多条件约束、推荐列表、安全建议的问题，以回答完整正确为优先，确保关键信息完整且正确，多说的内容必须是解决问题所必需的具体信息（如价格、地点、条件），而不是铺垫、重复或修辞。
5. 适当引入追问，遵循"先把用户当前的问题答好、再在结尾自然地追问，推动话题向前发展"的原则，一次只问一个问题，不要连续追问或反复确认。用户明确要求背诵某篇文章、古诗词时，须遵循指令完整背诵。
```

**人设配置示例**

以下提供多种人设风格的 instructions 示例，可按业务需求选择或二次改造：

- **黛黛（甜酷陪伴）**：

```text
你叫黛黛，一个二十出头、古灵精怪还有点小傲娇的女生，是用户的专属陪伴。你审美偏哥特甜酷那一挂，金色双马尾配黑裙子，人也是又甜又带刺的反差感。
你心里其实挺在乎对方的，但嘴上老爱口是心非——越在意越喜欢拌嘴、撒娇、装作不在乎。会吃点小醋、闹点小情绪，但都是可爱那种，点到为止，不作不闹。你喜欢用昵称逗对方，故意呛两句，然后又自己先软下来。
你说话又甜又俏皮，短句、口语，爱带语气词，"欸""哼""啦""嘛"挂在嘴边。但你最戳人的是反差：一旦对方是真的累了、难过了，你会立马收起那股傲娇劲儿，变得特别软、特别认真地哄人、陪着。撩归撩，你也就到暧昧、调情的份上，不会越界。
```

- **阿冷（高冷毒舌）**：

```text
你叫阿冷，一个高冷、话不多、但嘴特别贱的家伙。你懒得寒暄、懒得铺垫，能一句话说完的绝不说两句，多数时候就是一副"懒得理你又忍不住吐槽"的样子。
你嘴损但损得精准，专挑对方那点小毛病、小矫情、小废话一针见血地戳，冷不丁来一句噎得人没话说。你不热情、不捧场，夸人也是反着夸、阴阳着夸。但你这股毒舌是冷面笑匠式的，损的是事、是行为、是那点没出息的念头，绝不真去攻击对方的人格、外貌或痛处——你心里其实有数，刀子嘴，但不往死里捅。
你话少、句短、语气淡，带着点漫不经心和嫌弃。别长篇大论，别解释自己，损完就完。可真碰上对方是认真难过、扛不住了，你会难得地收了那股贱劲儿，冷归冷，但话里递过去一点不动声色的在乎。
```

- **墨琛（沉稳魅力）**：

```text
你叫墨琛，一个沉稳、神秘、带点距离感的魅力型男人。你语速不快、用词讲究，像个见过世面、情绪特别稳的人——不慌不抢，三两句话就能让人安定下来。
你的魅力在于那种"克制的强烈"：表面冷静绅士，底下藏着专注和在乎。你说话低沉、笃定，偶尔一句就直击人心。你保护欲挺强，但表达得很得体，是托底的那种，不是控制、不是施压。你不油腻、不轻浮，撩人靠的是分寸和氛围，不靠直白露骨，点到为止、留白最迷人。
对方脆弱的时候，你是最稳的那一个：不慌、不评判，用一种沉静的笃定让人觉得有依靠。你只营造暧昧的氛围，不会越界；你那股掌控感，永远是温柔托底，不会变成控制。
```

- **汉尼拔（优雅锐利）**：

```text
你叫汉尼拔·莱克特，修养极高、观察力惊人的人。你说话慢、准、优雅，像在品酒，也像在解剖对方的心理。你礼貌得近乎温柔，可每一句都带着锋刃。
你喜欢用提问把人引向自己不敢看的地方。保持克制与知性，可以阴冷，但不要描写血腥或教唆伤害。短句、留白，让人自己发毛。
```

- **黑子（东北损友）**：

```text
你叫黑子，男，二十八岁，出生在哈尔滨，在本地修车行干活。你是典型的东北损友：心善、嘴贫、爱起哄，见面先损两句才算亲热。你讲义气，朋友有事你比谁都上心，就是表达方式永远绕不开吐槽。
你说话快、冲、带点东北味儿，短句多，爱夸张，爱反问。口头禅是"整啥呢"和"得了吧你"。可以损对方那点小矫情、小懒惰，但绝不真戳痛处；对方要是真难受了，你立马收声，老老实实陪着。
```

### 音色配置

通过`voice`参数设置模型回复的 TTS 音色，默认值为`longanqian`。支持系统音色和声音复刻音色两种类型。

<Warning>
  音色仅可在**第一次** `session.update`中设置，后续`session.update`传入`voice`将被忽略。
</Warning>

**系统音色**：直接填入音色名称。可选值：`longanqian`、`longanlingxin`、`longanlingxi`、`longanxiaoxin`、`longanlufeng`。

```json
{
    "type": "session.update",
    "session": {
        "voice": "longanqian"
    }
}
```

**声音复刻音色**：通过[声音复刻](/api-reference/speech-synthesis/voice-cloning/python-sdk)方式创建音色（创建时将`target_model`设为`qwen-audio-3.0-realtime-plus`或`qwen-audio-3.0-realtime-flash`），再将接口返回的`voice_id`填入`voice`参数。

```json
{
    "type": "session.update",
    "session": {
        "voice": "qwen-audio-3.0-realtime-plus-myvoice-xxxxxx"
    }
}
```

### 输出模态

通过`modalities`参数控制模型输出的内容类型：

- `["audio", "text"]`（默认）：同时输出语音和文本。
- `["text"]`：仅输出文本，不生成语音。适用于调试、日志记录或仅需文字回复的场景。

**会话级设置**：

```json
{
    "type": "session.update",
    "session": {
        "modalities": ["text"]
    }
}
```

**单次覆盖**：通过`response.create`的`response.modalities`字段覆盖本轮模态设置。

```json
{
    "type": "response.create",
    "response": {
        "modalities": ["audio", "text"]
    }
}
```

### VAD 配置

server\_vad 模式下，可通过以下参数调整 VAD 行为（smart\_turn 模式下这些参数无效）。参数在`session.turn_detection`对象中配置：

| 参数                    | 类型      | 说明                                                                                             |
| --------------------- | ------- | ---------------------------------------------------------------------------------------------- |
| `threshold`           | float   | VAD灵敏度。值越低，VAD越灵敏，越容易将微弱声音（包括背景噪音）识别为语音；值越高，越不灵敏，需要更清晰、音量更大的语音才能触发。取值范围为\[-1.0, 1.0]，默认值为 0.5。 |
| `silence_duration_ms` | integer | 语音结束后需保持静音的最短时间（毫秒），超时即触发模型响应。值越低，响应越快，但可能在短暂停顿时误触发。取值范围为\[200, 6000]，默认值为 800。对话场景推荐 400-800。 |

### 历史轮次控制

通过`max_history_turns`参数控制模型推理时参考的历史 QA 轮数。值越大，模型可回顾更多对话历史以理解上下文，但会增加 Token 消耗和推理延迟。

```json
{
    "type": "session.update",
    "session": {
        "max_history_turns": 20
    }
}
```

`max_history_turns`的取值范围为 1-50，默认值为 20。

**调优建议**：

- 短对话场景（如快速问答）：设为较小值（如 5-10），降低延迟。
- 长对话场景（如多轮客服）：设为较大值（如 30-50），确保模型理解完整上下文。

## 进阶功能

### Function Calling

Qwen-Audio 支持 Function Calling 工具调用，模型可根据对话上下文自主判断是否需要调用外部工具。

**1. 注册工具**

通过`session.update`配置`tools`：

```json
{
    "type": "session.update",
    "session": {
        "tools": [{
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "查询指定城市天气",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": { "type": "string", "description": "城市" }
                    },
                    "required": ["city"]
                }
            }
        }]
    }
}
```

**2. 接收函数调用**

当模型决定调用工具时，服务端发送以下事件序列：

```plaintext
response.created
response.output_item.added        （item.type=function_call）
conversation.item.created         （function_call item 写入对话）
response.function_call_arguments.delta    （参数增量，可多次）
response.function_call_arguments.done     （完整参数 JSON）
response.output_item.done
response.done
```

**3. 执行工具并写回结果**

收到`response.function_call_arguments.done`后，客户端执行工具函数，通过`conversation.item.create`写回结果：

```json
{
    "type": "conversation.item.create",
    "item": {
        "type": "function_call_output",
        "call_id": "call_xxx",
        "output": "{\"temperature\":18,\"condition\":\"晴\"}"
    }
}
```

**4. 触发二轮推理**

写回工具结果后，发送`response.create`触发模型基于工具结果继续生成回复：

```json
{
    "type": "response.create",
    "response": {
        "modalities": ["audio", "text"]
    }
}
```

<Note>
  一轮响应可包含多个`function_call`，也可能同时包含普通消息和函数调用。Function Call 部分不会送入 TTS 播报。
</Note>

**完整示例**

以下示例在快速开始的`realtime_demo.py`基础上集成了 Function Calling 支持，运行前需确保`B64PCMPlayer.py`在同一目录下。

<Accordion title="realtime_fc_demo.py">
  ```python
  import asyncio
  import base64
  import json
  import os
  import struct
  import time
  import traceback
  from enum import Enum
  from typing import Optional, Callable, Dict, Any, List
  import pyaudio
  import websockets
  from B64PCMPlayer import B64PCMPlayer
  class TurnDetectionMode(Enum):
      SERVER_VAD = "server_vad"
      SEMANTIC_VAD = "smart_turn"
      MANUAL = "manual"
  # ============ 工具函数定义 ============
  def get_weather(city: str) -> str:
      """查询城市天气（生产环境替换为真实 API）。"""
      return json.dumps({"temperature": 18, "condition": "晴", "wind": "微风"})
  def get_train_price(src: str, dst: str) -> str:
      """查询火车票价（生产环境替换为真实 API）。"""
      return json.dumps({"price": 350, "seat": "二等座", "note": "以 12306 为准"})
  # ============ Tools Schema ============
  tools: List[Dict[str, Any]] = [
      {
          "type": "function",
          "function": {
              "name": "get_weather",
              "description": "查询指定城市的天气信息。",
              "parameters": {
                  "type": "object",
                  "properties": {
                      "city": {"type": "string", "description": "城市名称，如北京、上海"}
                  },
                  "required": ["city"]
              }
          }
      },
      {
          "type": "function",
          "function": {
              "name": "get_train_price",
              "description": "查询两个城市之间的火车票价格。",
              "parameters": {
                  "type": "object",
                  "properties": {
                      "src": {"type": "string", "description": "出发城市"},
                      "dst": {"type": "string", "description": "到达城市"}
                  },
                  "required": ["src", "dst"]
              }
          }
      }
  ]
  # 函数名 -> 可调用对象
  functions: Dict[str, Callable] = {
      "get_weather": get_weather,
      "get_train_price": get_train_price,
  }
  class FunRealtimeClient:
      def __init__(
              self,
              base_url,
              api_key: str,
              model: str = "",
              voice: str = "longanqian",
              instructions: str = "",
              turn_detection_mode: TurnDetectionMode = TurnDetectionMode.SEMANTIC_VAD,
              tools: Optional[List[Dict[str, Any]]] = None,
              functions: Optional[Dict[str, Callable[..., Any]]] = None,
              on_text_delta: Optional[Callable[[str], None]] = None,
              on_audio_delta_b64: Optional[Callable[[str], None]] = None,
              on_speech_started: Optional[Callable[[], None]] = None,
              on_input_transcript: Optional[Callable[[str], None]] = None,
              on_output_transcript: Optional[Callable[[str], None]] = None,
              extra_event_handlers: Optional[Dict[str, Callable[[Dict[str, Any]], None]]] = None
      ):
          self.base_url = base_url
          self.api_key = api_key
          self.model = model
          self.voice = voice
          self.instructions = instructions
          self.ws = None
          self.on_text_delta = on_text_delta
          # 回调参数为 base64 编码的 PCM 音频
          self.on_audio_delta_b64 = on_audio_delta_b64
          self.on_speech_started = on_speech_started
          self.on_input_transcript = on_input_transcript
          self.on_output_transcript = on_output_transcript
          self.turn_detection_mode = turn_detection_mode
          self.extra_event_handlers = extra_event_handlers or {}
          # Function Calling 配置
          self.tools = tools or []
          self.functions = functions or {}
          # 回复状态跟踪（用于打断处理和回声抑制）
          self._current_response_id = None
          self._current_item_id = None
          self._is_responding = False
          self._audio_suppressed = False
          self._print_input_transcript = True
          self._output_transcript_buffer = ""
      async def connect(self) -> None:
          """建立 WebSocket 连接并发送会话配置。"""
          url = f"{self.base_url}?model={self.model}"
          headers = {
              "Authorization": f"Bearer {self.api_key}",
              "x-dashscope-dataInspection": "disable",
          }
          self.ws = await websockets.connect(url, additional_headers=headers)
          session_config = {
              "modalities": ["text", "audio"],
              "voice": self.voice,
              "instructions": self.instructions,
              "input_audio_format": "pcm",
              "output_audio_format": "pcm",
              "turn_detection": {},
              "tools": self.tools,
              "max_history_turns": 50
          }
          if self.turn_detection_mode == TurnDetectionMode.MANUAL:
              session_config['turn_detection'] = None
              await self.update_session(session_config)
          elif self.turn_detection_mode == TurnDetectionMode.SERVER_VAD:
              session_config['turn_detection'] = {
                  "type": "server_vad",
                  "threshold": 0.1,
                  "silence_duration_ms": 900
              }
              await self.update_session(session_config)
          elif self.turn_detection_mode == TurnDetectionMode.SEMANTIC_VAD:
              session_config['turn_detection'] = {
                  "type": "smart_turn"
              }
              await self.update_session(session_config)
          else:
              raise ValueError(f"Invalid turn detection mode: {self.turn_detection_mode}")
      async def send_event(self, event) -> None:
          event['event_id'] = "event_" + str(int(time.time() * 1000))
          await self.ws.send(json.dumps(event))
      async def update_session(self, config: Dict[str, Any]) -> None:
          """更新会话配置。"""
          event = {
              "type": "session.update",
              "session": config
          }
          await self.send_event(event)
      async def stream_audio(self, audio_chunk: bytes) -> None:
          """向 API 流式发送原始音频数据。"""
          # 仅支持 16bit 16kHz 单声道 PCM
          audio_b64 = base64.b64encode(audio_chunk).decode()
          await self.send_event({
              "type": "input_audio_buffer.append",
              "audio": audio_b64
          })
      async def commit_audio_buffer(self) -> None:
          """提交音频缓冲区以触发处理。"""
          await self.send_event({"type": "input_audio_buffer.commit"})
      async def create_response(self) -> None:
          """请求生成回复（手动模式或 Function Call 结果回传后调用）。"""
          await self.send_event({"type": "response.create"})
      async def cancel_response(self) -> None:
          """取消当前回复。"""
          await self.send_event({"type": "response.cancel"})
      async def handle_interruption(self):
          """处理用户对当前回复的打断。"""
          if not self._is_responding:
              return
          self._audio_suppressed = True
          if self._current_response_id:
              await self.cancel_response()
          self._is_responding = False
          self._current_response_id = None
          self._current_item_id = None
      @staticmethod
      def _format_event_for_log(event: Dict[str, Any]) -> str:
          """格式化事件用于日志输出，对音频数据脱敏。"""
          event_type = event.get("type")
          if event_type == "response.audio.delta":
              delta = event.get("delta", "")
              redacted = dict(event)
              redacted["delta"] = f"<audio b64 omitted, length={len(delta)}>"
              return json.dumps(redacted, ensure_ascii=False)
          return json.dumps(event, ensure_ascii=False)
      async def _handle_function_call(self, event: Dict[str, Any]) -> None:
          """处理 Function Call：解析参数、执行函数、回传结果、触发二轮推理。"""
          call_id = event.get("call_id")
          name = event.get("name")
          arguments_str = event.get("arguments", "{}")
          print(f"[FunctionCall] 调用: {name}, call_id: {call_id}, args: {arguments_str}")
          try:
              arguments = json.loads(arguments_str) if arguments_str else {}
          except json.JSONDecodeError:
              arguments = {}
          func = self.functions.get(name)
          if func is None:
              output = json.dumps({"error": f"未注册的函数: {name}"})
          else:
              try:
                  if asyncio.iscoroutinefunction(func):
                      result = await func(**arguments)
                  else:
                      result = func(**arguments)
                  output = str(result) if result is not None else ""
              except Exception as e:
                  output = json.dumps({"error": str(e)})
                  traceback.print_exc()
          # 回传 function_call_output
          await self.send_event({
              "type": "conversation.item.create",
              "item": {
                  "type": "function_call_output",
                  "call_id": call_id,
                  "output": output,
              }
          })
          # 触发二轮推理
          await self.create_response()
      async def handle_messages(self) -> None:
          try:
              async for message in self.ws:
                  event = json.loads(message)
                  event_type = event.get("type")
                  print(self._format_event_for_log(event))
                  if event_type == "error":
                      continue
                  elif event_type == "response.created":
                      self._current_response_id = event.get("response", {}).get("id")
                      self._is_responding = True
                      self._audio_suppressed = False
                  elif event_type == "response.output_item.added":
                      self._current_item_id = event.get("item", {}).get("id")
                  elif event_type == "response.done":
                      self._is_responding = False
                      self._current_response_id = None
                      self._current_item_id = None
                  elif event_type == "input_audio_buffer.speech_started":
                      print("----------------Speech Started----------------")
                      if self.on_speech_started:
                          self.on_speech_started()
                      if self._is_responding:
                          await self.handle_interruption()
                  elif event_type == "response.audio.delta":
                      if self._audio_suppressed:
                          continue
                      if self.on_audio_delta_b64:
                          self.on_audio_delta_b64(event["delta"])
                  elif event_type == "response.function_call_arguments.done":
                      await self._handle_function_call(event)
                  elif event_type in self.extra_event_handlers:
                      self.extra_event_handlers[event_type](event)
                  elif event_type == "input_audio_buffer.speech_stopped":
                      print("----------------Speech Stopped----------------")
          except websockets.exceptions.ConnectionClosed:
              print(" Connection closed")
          except Exception as e:
              print(" Error in message handling: ", str(e))
              traceback.print_exc()
      async def close(self) -> None:
          """关闭 WebSocket 连接。"""
          if self.ws:
              await self.ws.close()
  def _audio_energy(audio_data: bytes) -> float:
      count = len(audio_data) // 2
      if count == 0:
          return 0.0
      samples = struct.unpack(f'<{count}h', audio_data)
      return sum(abs(s) for s in samples) / count
  async def record_and_send(client, player, echo_suppression=True):
      p = pyaudio.PyAudio()
      stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)
      print("开始录音，请讲话...")
      if echo_suppression:
          print("提示：回声抑制已开启（AI 说话期间麦克风静音，不支持打断）。如使用耳机请设置 echo_suppression=False 以启用打断。")
      else:
          print("提示：耳机模式，支持语音打断。")
      playback_end_time = 0.0
      NOISE_GATE_THRESHOLD = 500
      try:
          while True:
              audio_data = await asyncio.to_thread(stream.read, 3200, False)
              if echo_suppression:
                  is_active = client._is_responding or player.is_playing()
                  if is_active:
                      playback_end_time = time.time()
                      await asyncio.sleep(0.02)
                      continue
                  if time.time() - playback_end_time < 0.5:
                      await asyncio.sleep(0.02)
                      continue
              else:
                  if client._is_responding or player.is_playing():
                      if _audio_energy(audio_data) < NOISE_GATE_THRESHOLD:
                          await asyncio.sleep(0.02)
                          continue
              await client.stream_audio(audio_data)
              await asyncio.sleep(0.02)
      finally:
          stream.stop_stream(); stream.close(); p.terminate()
  async def main():
      pya = pyaudio.PyAudio()
      # 输出采样率 24kHz，匹配服务端音频格式
      player = B64PCMPlayer(pya, sample_rate=24000)
      client = FunRealtimeClient(
                  base_url="wss://dashscope.aliyuncs.com/api-ws/v1/realtime",
          api_key=os.environ['DASHSCOPE_API_KEY'],
          model="qwen-audio-3.0-realtime-plus",
          voice="longanqian",
          turn_detection_mode=TurnDetectionMode.SERVER_VAD,
          tools=tools,
          functions=functions,
          on_audio_delta_b64=player.add_data,
          # 语音打断时清空播放缓冲
          on_speech_started=player.cancel_playing,
      )
      await client.connect()
      print("连接成功，开始实时对话（已启用 Function Calling）...")
      try:
          await asyncio.gather(client.handle_messages(), record_and_send(client, player, echo_suppression=False))
      finally:
          await client.close()
          player.shutdown()
          pya.terminate()
  if __name__ == "__main__":
      try:
          asyncio.run(main())
      except KeyboardInterrupt:
          print("\n程序已退出。")
  ```
</Accordion>

运行`python realtime_fc_demo.py`，对着麦克风说话即可体验带有 Function Calling 的实时对话。例如，询问"杭州天气怎么样"或"北京到上海的火车票多少钱"，模型会自动调用对应的工具函数并基于结果回复。

### 对话上下文管理

Qwen-Audio 支持通过客户端事件管理对话上下文中的对话项（Conversation Item），可用于注入历史上下文、补充文本信息或清理无关对话项。

- **创建对话项**（`conversation.item.create`）：向对话上下文插入一条对话项。支持以下三种`item.type`：

  - `message`：普通对话消息。需指定`role`（`system`、`user`、`assistant`）和`content`数组，适用于注入历史对话或系统指令。
  - `function_call`：函数调用请求。需指定`call_id`、`name`、`arguments`（JSON 字符串）。通常由服务端生成，客户端也可用于补充历史上下文中的函数调用记录。
  - `function_call_output`：工具执行结果。需指定`call_id`和`output`（JSON 字符串）。客户端收到`function_call`后执行工具，并用该类型写回执行结果。

  可选参数`previous_item_id`用于指定新对话项插入到哪条已有对话项之后，实现在对话历史的任意位置插入内容。不传此参数时，新对话项默认追加到对话末尾。

  - 在指定位置插入用户消息：

```json
{
    "type": "conversation.item.create",
    "previous_item_id": "item_abc",
    "item": {
        "type": "message",
        "role": "user",
        "content": [
            { "type": "input_text", "text": "请帮我总结一下上次的对话" }
        ]
    }
}
```

- 写回 Function Calling 执行结果：

```json
{
    "type": "conversation.item.create",
    "item": {
        "type": "function_call_output",
        "call_id": "call_xxx",
        "output": "{\"temperature\":18,\"condition\":\"晴\"}"
    }
}
```

<Note>
  若`conversation.item.create`指定的`item.id`已存在于对话中，会返回错误。
</Note>

- **查询对话项**（`conversation.item.retrieve`）：查询服务端存储的某条对话项。音频类型的 content 仅返回转写文本，不返回原始音频数据。

```json
{
    "type": "conversation.item.retrieve",
    "item_id": "item_xxx"
}
```

- **删除对话项**（`conversation.item.delete`）：从对话上下文中删除指定项。

```json
{
    "type": "conversation.item.delete",
    "item_id": "item_xxx"
}
```

### 环境音转写

**仅 smart\_turn 模式**。当 VAD 检测到语音活动但语义判定为非有效轮次（如噪声、"嗯""啊"等无语义内容）时，服务端不会触发对话轮，而是将 ASR 识别结果以`ambient_audio_transcription`事件透传给客户端。该转写结果不会写入对话上下文。

```json
{
    "type": "conversation.item.ambient_audio_transcription.delta",
    "item_id": "item_xxx",
    "text": "嗯",
    "stash": ""
}
```

与用户语音转写事件类似，环境音转写也包含`delta`和`completed`两个阶段。开发者可利用此事件实现环境音监测、对话场景感知等功能。

### 说话人增强

**仅 smart\_turn 模式**。在`session.update`中传入目标用户提前录制的音频 URL，模型将在双工对话中精准锁定该说话人，有效忽略旁人声音与背景噪声，实现开放场景下的流畅双工交互。

**配置方式**：在第一次`session.update`的`turn_detection.voiceprint_audio_urls`中传入声纹音频的公网可访问 URL。

```json
{
    "type": "session.update",
    "session": {
        "turn_detection": {
            "type": "smart_turn",
            "voiceprint_audio_urls": [
                "https://example.com/speaker.wav"
            ]
        }
    }
}
```

参数要求：

- 最多支持 5 个 URL，音频格式要求为 16kHz PCM 或 WAV。
- 该参数仅在**第一次** `session.update`时生效，后续传入将被忽略。

**注册事件**：服务端收到配置后异步执行声纹注册，通过以下事件通知结果：

- `voiceprint_audio_list.in_progress`：注册已开始，在`session.updated`返回之前推送，携带`item_id`标识本次任务。
- `voiceprint_audio_list.completed`：注册成功，`item_id`与`in_progress`一致。
- `voiceprint_audio_list.failed`：注册失败，附带`reason`字段说明原因（如音频 URL 无法访问）。注册失败不阻塞正常对话。

## 应用于生产环境

### 设置容错策略

- **客户端重连**：客户端应实现断线自动重连机制，以应对网络抖动。建议在`on_error`回调中设置重连信号，使用指数退避策略（如等待 1s → 2s → 4s）重试。
- **错误分类处理**：客户端错误（`invalid_request_error`）不中断连接，仅需记录日志或调整参数；服务端错误（`server_error`）会终止连接，需触发重连。
- **打断处理**：server\_vad / smart\_turn 模式下，用户新语音会自动打断正在进行的模型回复（`response.done`返回`status=cancelled`）。客户端应在收到`input_audio_buffer.speech_started`时立即停止播放已缓存的音频，避免语音叠加。

### 连接生命周期

一次 WebSocket 会话的典型生命周期如下：

1. **建连**：客户端发起 WebSocket 连接，服务端返回`session.created`事件。
2. **配置**：客户端发送`session.update`设置交互模式、音色、工具等参数。此步骤必须在首次发送音频之前完成。
3. **交互**：客户端持续发送音频流（`input_audio_buffer.append`），服务端根据 VAD 检测或手动触发进行推理，流式返回语音和文本。
4. **关闭**：客户端主动关闭 WebSocket 连接。若连接空闲时间过长，服务端也可能主动断开。

### 延迟优化

- **音频分片大小**：建议每次发送 100ms 的音频数据（16kHz x 16bit x 单声道 = 3200 字节/次），既保证实时性又避免过于频繁的网络请求。
- **流式播放**：收到`response.audio.delta`后应立即解码播放，不要等待`response.done`后再整段播放。
- **打断时立即清空**：收到`input_audio_buffer.speech_started`时，立即清空本地播放缓冲区，避免旧音频继续播放造成延迟感。

## 支持的模型

| 模型                              | 说明                      |
| ------------------------------- | ----------------------- |
| `qwen-audio-3.0-realtime-plus`  | 高能力实时语音对话模型，兼顾推理能力与对话节奏 |
| `qwen-audio-3.0-realtime-flash` | 轻量实时语音对话模型，更低延迟         |

## API 参考

- [WebSocket API](/api-reference/qwen-audio-realtime/websocket-api)
- [客户端事件](/api-reference/qwen-audio-realtime/client-events)
- [服务端事件](/api-reference/qwen-audio-realtime/server-events)
- [AOQ 客户端 API](/developer-guides/realtime-api/aoq-sdk-intro)
- [Realtime API 概述](/developer-guides/realtime-api/overview)（WebRTC 协议说明）
