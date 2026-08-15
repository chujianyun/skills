> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 实时音视频理解

> 通过 WebSocket 或 WebRTC 接入 Qwen-Omni 系列模型，实现音频和视频的低延迟实时对话。

## 使用方法

### 1. 建立连接

Qwen-Omni-Realtime 支持 WebSocket 和 WebRTC 两种协议接入。WebSocket 适合服务端集成和快速接入；WebRTC 适合浏览器端、低延迟语音场景，音频通过 UDP 直接传输，内置回声消除和降噪。该模型除以上两种协议外，还支持通过 AOQ 协议接入；如果是客户端对接，且更看重稳定的延迟、弱网下的交互能力、实时双工的降噪与回声消除，可优先考虑 AOQ，协议对比与选型请参见 [Realtime API 概述](/developer-guides/realtime-api/overview)。

<Note>
  单个 Qwen-Omni-Realtime WebSocket 会话最长持续 **120 分钟**。超时后服务会自动关闭连接。
</Note>

<Tabs>
  <Tab title="WebSocket">
    <Tabs>
      <Tab title="原生 WebSocket 连接">
        所需配置项如下：

| 配置项  | 说明                                                                                                                                             |
| ---- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| 接入地址 | `wss://dashscope.aliyuncs.com/api-ws/v1/realtime`                                                                                              |
| 查询参数 | 查询参数为 `model`，设置为要访问的模型名称。参见[模型选择](/developer-guides/speech/s2s-models)。示例：`?model=qwen3.5-omni-plus-realtime`                                 |
| 请求头  | 使用 Bearer Token 认证：`Authorization: Bearer $DASHSCOPE_API_KEY`。DASHSCOPE\_API\_KEY 是你在千问AI平台上申请的 [API Key](/api-reference/preparation/api-key)。 |

        ```python
        # pip install websocket-client
        import json
        import websocket
        import os

        API_KEY=os.getenv("DASHSCOPE_API_KEY")
        API_URL = "wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=qwen3.5-omni-plus-realtime"

        headers = [
          "Authorization: Bearer " + API_KEY
        ]

        def on_open(ws):
          print(f"已连接到服务器: {API_URL}")
        def on_message(ws, message):
          data = json.loads(message)
          print("收到事件:", json.dumps(data, indent=2))
        def on_error(ws, error):
          print("错误:", error)

        ws = websocket.WebSocketApp(
          API_URL,
          header=headers,
          on_open=on_open,
          on_message=on_message,
          on_error=on_error
        )

        ws.run_forever()
        ```
      </Tab>

      <Tab title="DashScope SDK">
        <CodeGroup>
          ```python Python
          # SDK 1.23.9 及以上版本
          import os
          import json
          from dashscope.audio.qwen_omni import OmniRealtimeConversation,OmniRealtimeCallback
          import dashscope
          # 如果未配置 API Key，请将下一行替换为 dashscope.api_key = "sk-xxx"
          dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

          class PrintCallback(OmniRealtimeCallback):
            def on_open(self) -> None:
              print("连接成功")
            def on_event(self, response: dict) -> None:
              print("收到事件:")
              print(json.dumps(response, indent=2, ensure_ascii=False))
            def on_close(self, close_status_code: int, close_msg: str) -> None:
              print(f"连接已关闭 (code={close_status_code}, msg={close_msg})。")

          callback = PrintCallback()
          conversation = OmniRealtimeConversation(
            model="qwen3.5-omni-plus-realtime",
            callback=callback,
            url="wss://dashscope.aliyuncs.com/api-ws/v1/realtime"
          )
          try:
            conversation.connect()
            print("会话已启动。按 Ctrl+C 退出。")
            conversation.thread.join()
          except KeyboardInterrupt:
            conversation.close()
          ```

          ```java Java
          // SDK 2.20.9 及以上版本
          import com.alibaba.dashscope.audio.omni.*;
          import com.alibaba.dashscope.exception.NoApiKeyException;
          import com.google.gson.JsonObject;
          import java.util.concurrent.CountDownLatch;

          public class Main {
            public static void main(String[] args) throws InterruptedException, NoApiKeyException {
              CountDownLatch latch = new CountDownLatch(1);
              OmniRealtimeParam param = OmniRealtimeParam.builder()
                  .model("qwen3.5-omni-plus-realtime")
                  .apikey(System.getenv("DASHSCOPE_API_KEY"))
                  .url("wss://dashscope.aliyuncs.com/api-ws/v1/realtime")
                  .build();

              OmniRealtimeConversation conversation = new OmniRealtimeConversation(param, new OmniRealtimeCallback() {
                @Override
                public void onOpen() {
                  System.out.println("连接成功");
                }
                @Override
                public void onEvent(JsonObject message) {
                  System.out.println(message);
                }
                @Override
                public void onClose(int code, String reason) {
                  System.out.println("连接已关闭 code: " + code + ", reason: " + reason);
                  latch.countDown();
                }
              });
              conversation.connect();
              latch.await();
              conversation.close(1000, "bye");
              System.exit(0);
            }
          }
          ```
        </CodeGroup>
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="WebRTC">
    WebRTC 建立连接分为两个阶段：

    1. **SDP 交换（HTTP）**：客户端先将自身的媒体能力和网络地址（Offer SDP）通过 HTTP POST 发送给服务端，服务端返回自身信息（Answer SDP），双方完成能力协商。
    2. **建连（自动）**：协商完成后，WebRTC 底层自动建立音频传输通道。

    SDP 交换的配置项：

| 配置项          | 说明                                                                                                        |
| ------------ | --------------------------------------------------------------------------------------------------------- |
| 请求地址         | POST https\://{endpoint}/api/v1/webrtc/realtime <br /> <Note>WebRTC 功能目前为白名单开放，请联系商务经理获取 Endpoint。</Note> |
| 查询参数         | 查询参数为 `model`，需指定为访问的模型名。示例：`?model=qwen3.5-omni-plus-realtime`                                           |
| Content-Type | application/sdp                                                                                           |
| 请求头          | Authorization: Bearer DASHSCOPE\_API\_KEY                                                                 |
| 请求体          | 客户端生成的 Offer SDP 字符串                                                                                      |
| 响应           | 成功：HTTP 200，返回服务端 Answer SDP 字符串。失败：HTTP 4xx，返回 JSON 错误信息。                                                |

    建连示例代码：

    <CodeGroup>
      ```python Python
      # pip install aiortc aiohttp certifi
      import asyncio, aiohttp, ssl, certifi
      from aiortc import RTCPeerConnection, RTCConfiguration, RTCSessionDescription
      from aiortc.mediastreams import AudioStreamTrack

      API_KEY = "REDACTED"
      MODEL = "qwen3.5-omni-plus-realtime"
      SIGNALING_URL = f"https://{{endpoint}}/api/v1/webrtc/realtime?model={MODEL}"

      async def connect():
        pc = RTCPeerConnection(RTCConfiguration(iceServers=[]))

        # 添加音频轨道，确保 Offer SDP 包含 m=audio（服务端必需）
        pc.addTrack(AudioStreamTrack())

        # 创建 DataChannel 以触发 SDP 协商（名称可自定义，服务端会通过名为 "txt" 的通道推送事件）
        pc.createDataChannel("oai-events")

        # SDP 交换：创建 Offer 并发送到服务端
        offer = await pc.createOffer()
        await pc.setLocalDescription(offer)

        async with aiohttp.ClientSession() as session:
          async with session.post(
            SIGNALING_URL,
            ssl=ssl.create_default_context(cafile=certifi.where()),
            data=offer.sdp.encode("utf-8"),
            headers={
              "Content-Type": "application/sdp",
              "Authorization": f"Bearer {API_KEY}",
            },
          ) as resp:
            if not resp.ok:
              raise Exception(f"SDP 交换失败: {resp.status} {await resp.text()}")
            answer_sdp = await resp.text()

        print("=== Offer SDP ===")
        print(offer.sdp)
        print("=== Answer SDP ===")
        print(answer_sdp)

        # ICE 建连自动完成
        await pc.setRemoteDescription(RTCSessionDescription(sdp=answer_sdp, type="answer"))
        print("WebRTC 连接已建立")
        return pc
      ```

      ```javascript JavaScript
      const API_KEY = 'REDACTED';
      const API_URL = 'https://{endpoint}/api/v1/webrtc/realtime?model=qwen3.5-omni-plus-realtime';

      async function connect() {
        const pc = new RTCPeerConnection({ iceServers: [] });

        // 添加音频轨道，确保 Offer SDP 包含 m=audio（服务端必需）
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        stream.getAudioTracks().forEach(t => pc.addTrack(t, stream));

        // 创建 DataChannel 以触发 SDP 协商（名称可自定义，服务端会通过名为 "txt" 的通道推送事件）
        pc.createDataChannel('oai-events');

        // 等待 ICE 收集完成后发送 Offer 获取 Answer
        pc.onicegatheringstatechange = async () => {
          if (pc.iceGatheringState !== 'complete') return;
          const resp = await fetch(API_URL, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/sdp',
              'Authorization': `Bearer ${API_KEY}`,
            },
            body: pc.localDescription.sdp,
          });
          if (!resp.ok) throw new Error('SDP 交换失败: ' + resp.status);
          const answerSdp = await resp.text();
          // ICE 建连自动完成
          await pc.setRemoteDescription({ type: 'answer', sdp: answerSdp });
          console.log('WebRTC 连接已建立');
        };

        // 创建 Offer
        const offer = await pc.createOffer();
        await pc.setLocalDescription(offer);
        return pc;
      }
      ```
    </CodeGroup>
  </Tab>
</Tabs>

### 2. 配置会话

发送 [session.update](/api-reference/real-time-multimodal/client-events) 客户端事件：

```json
{
  // 事件 ID，由客户端生成
  "event_id": "event_ToPZqeobitzUJnt3QqtWg",
  // 事件类型，固定为 session.update
  "type": "session.update",
  // 会话配置
  "session": {
    // 输出模态。支持 ["text"]（仅文本）或 ["text", "audio"]（文本和音频）
    "modalities": [
      "text",
      "audio"
    ],
    // 输出音色
    "voice": "Ethan",
    // 推荐写法：同时配置音频格式和采样率（仅 qwen3.5-omni-plus-realtime / qwen3.5-omni-flash-realtime 支持）
    // 输入格式：pcm / wav，默认 pcm；采样率：8000/16000/24000/48000，默认 16000
    // 输出格式：pcm / wav，默认 pcm；采样率：8000/16000/24000/48000，默认 24000
    "audio": {
      "input": {
        "format": {
          "type": "pcm",
          "sample_rate": 16000
        }
      },
      "output": {
        "format": {
          "type": "pcm",
          "sample_rate": 24000
        }
      }
    },
    // 系统消息，用于设置模型的目标或角色
    "instructions": "你是某五星级酒店的AI客服专员，请准确且友好地解答客户关于房型、设施、价格、预订政策的咨询。请始终以专业和乐于助人的态度回应，杜绝提供未经证实或超出酒店服务范围的信息。",
    // 是否启用语音活动检测。启用时传入配置对象，服务端会自动检测说话的开始和结束。
    // 设为 null 则由客户端决定何时触发模型响应
    "turn_detection": {
      // VAD 类型
      "type": "semantic_vad",
      // VAD 检测阈值。嘈杂环境调高，安静环境调低
      "threshold": 0.5,
      // 检测语音停止的静音持续时间，超过此值后会触发模型响应。取值范围 200-6000，默认 800。金融核实等短回答场景建议 500-600。
      "silence_duration_ms": 800
    }
  }
}
```

<Note>
  音频格式与采样率可配置能力仅适用于 `qwen3.5-omni-plus-realtime` 和 `qwen3.5-omni-flash-realtime` 模型，历史兼容字段 `input_audio_format` / `output_audio_format` 仍有效，建议采用 `audio.input.format` / `audio.output.format` 字段。
</Note>

每通会话结束后，发送 `session.finish` 事件关闭会话，或直接断开 WebSocket 连接。同一会话不关闭会导致上下文持续累积。

### 3. 输入音频和图像

<Tabs>
  <Tab title="WebSocket">
    音频输入是推荐的主要输入方式；图片输入可选。模型也支持纯文本输入：通过 `conversation.item.create` 发送 `input_text` 类型内容，无需音频，适用于非实时对话场景。模型目录标注的"支持文本输入"包括用户纯文本对话、system instructions 和 `function_call_output`。输入方式取决于接入协议。

    <Info>
      启用服务端语音活动检测（VAD）时，服务端会自动提交数据并在检测到说话结束时触发响应。未启用 VAD（手动模式）时，客户端必须调用 [input\_audio\_buffer.commit](/api-reference/real-time-multimodal/client-events) 事件来提交数据。
    </Info>
  </Tab>

  <Tab title="WebRTC">
    建连时添加的音频轨道和视频轨道（即 RTP 媒体通道）会自动将数据传输到服务端。

    - **音频**：通过音频轨道（RTP）直接传输，无需发送 `input_audio_buffer.append` 事件。
    - **图片**：通过视频轨道（RTP）发送画面帧，不支持 `input_image_buffer.append` 事件。

    <Note>WebRTC 仅支持服务端 VAD 模式（`server_vad` 或 `semantic_vad`），不支持手动模式。</Note>
  </Tab>
</Tabs>

### 4. 接收模型响应

模型响应的格式取决于配置的输出模态。

<Tabs>
  <Tab title="WebSocket">
    - **仅文本**

      通过 [response.text.delta](/api-reference/real-time-multimodal/server-events) 事件接收流式文本。通过 [response.text.done](/api-reference/real-time-multimodal/server-events) 事件获取完整文本。

    - **文本和音频**

      - **文本**：通过 [response.audio\_transcript.delta](/api-reference/real-time-multimodal/server-events) 事件接收流式文本。通过 [response.audio\_transcript.done](/api-reference/real-time-multimodal/server-events) 事件获取完整文本。
      - **音频**：通过 [response.audio.delta](/api-reference/real-time-multimodal/server-events) 事件获取 Base64 编码的流式音频输出数据。[response.audio.done](/api-reference/real-time-multimodal/server-events) 事件表示音频生成完毕。
  </Tab>

  <Tab title="WebRTC">
    - **仅输出文本**

      通过 DataChannel 接收 `response.text.delta` 和 `response.text.done` 等流式文本事件。

    - **输出文本+音频**

      - **文本**：通过 DataChannel 接收 `response.text.delta` 和 `response.text.done` 等流式文本事件。
      - **音频**：通过 RTP 轨道实时接收和播放，无需通过 `response.audio.delta` 事件获取音频数据。
  </Tab>
</Tabs>

## 响应延迟与优化

Qwen3.5-Omni-Realtime 系列这类端到端实时多模态模型，在单个模型内同时完成语音识别、语义理解与语音生成，各环节无法像 ASR+LLM+TTS 拼接方案那样独立并行、单独优化，因此端到端方案的总响应时间通常高于拼接方案中单独的 LLM 环节。以 DashScope WebSocket API 为例，文本输入、`voice=Tina`、`silence_duration_ms=800` 场景下的实测参考值：qwen3.5-omni-flash-realtime 总响应约 5.1 秒，拼接方案中 LLM 环节单独调用约 3.1 秒，端到端比该 LLM 环节慢约 2.0 秒。以上为特定参数下的单次实测参考值，实际耗时会随输入长度、网络状况和语音活动检测（VAD）配置变化。

### 优化建议

1. **优先使用 Flash 版本**：实测 qwen3.5-omni-flash-realtime 总响应约 5.1 秒，qwen3.5-omni-plus-realtime 约 5.8 秒，flash 比 plus 快约 0.7 秒（714 毫秒）。对响应时效性敏感的场景建议优先选用 flash 版本。
2. **降低网络延迟**：WebSocket 连接的往返时延会直接叠加到端到端响应时间上，建议将业务服务部署在靠近所调用地域服务端的区域（该模型支持华北 2（北京）和新加坡地域），并按"1. 建立连接"中的地域说明选择对应的调用地址。

## 快速开始

[获取 API Key](/api-reference/preparation/api-key)并[设置为环境变量](/api-reference/preparation/export-api-key-env)。

<Tabs>
  <Tab title="DashScope Python SDK">
    **准备运行环境**

    Python 版本需为 3.10 或以上。

    首先根据操作系统安装 PyAudio。

    <Tabs>
      <Tab title="macOS">
        ```bash
        brew install portaudio && pip install pyaudio
        ```
      </Tab>

      <Tab title="Debian/Ubuntu">
        - **未使用虚拟环境**时，使用系统包管理器直接安装：

        ```bash
        sudo apt-get install python3-pyaudio
        ```

        - **使用虚拟环境**时，先安装编译依赖：

        ```bash
        sudo apt update
        sudo apt install -y python3-dev portaudio19-dev
        ```

        然后在已激活的虚拟环境中使用 pip 安装：

        ```bash
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

    安装完成后，使用 pip 安装剩余依赖：

    ```bash
    pip install websocket-client dashscope
    ```

    **选择交互模式**

    - VAD 模式（自动检测说话的开始和结束）

      服务端自动判断用户何时开始和停止说话并作出响应。

    - 手动模式（按住说话，松开发送）

      由客户端控制说话的开始和结束。用户说完后，客户端需主动向服务端发送消息。

    <Tabs>
      <Tab title="VAD 模式">
        新建 Python 文件 `vad_dash.py`，将以下代码复制到文件中：

        <Accordion title="vad_dash.py">
          ```python
          # 依赖: dashscope >= 1.23.9, pyaudio
          import os
          import base64
          import time
          import pyaudio
          from dashscope.audio.qwen_omni import MultiModality, AudioFormat,OmniRealtimeCallback,OmniRealtimeConversation
          import dashscope

          # 配置参数: 接入地址, API Key, 音色, 模型, 模型角色
          url = 'wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
          # 配置 API Key。如果未设置环境变量，请将下一行替换为 dashscope.api_key = "sk-xxx"
          dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')
          # 指定音色
          voice = 'Tina'
          # 指定模型
          model = 'qwen3.5-omni-plus-realtime'
          # 指定模型角色
          instructions = "你是小云，一个私人助手。请用幽默风趣的方式回答用户的问题。"
          class SimpleCallback(OmniRealtimeCallback):
            def __init__(self, pya):
              self.pya = pya
              self.out = None
            def on_open(self):
              # 初始化音频输出
              self.out = self.pya.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=24000,
                output=True
              )
            def on_event(self, response):
              if response['type'] == 'response.audio.delta':
                # 播放音频
                self.out.write(base64.b64decode(response['delta']))
              elif response['type'] == 'conversation.item.input_audio_transcription.delta':
                # 流式预览：text为已确认前缀，stash为待确认后缀
                preview = response.get('text', '') + response.get('stash', '')
                print(f"\r[用户] {preview}", end='', flush=True)
              elif response['type'] == 'conversation.item.input_audio_transcription.completed':
                # 转录完成，打印最终文本并换行
                print(f"\r[用户] {response['transcript']}")
              elif response['type'] == 'response.audio_transcript.done':
                # 打印模型回复的文本
                print(f"[模型] {response['transcript']}")

          # 1. 初始化音频设备
          pya = pyaudio.PyAudio()
          # 2. 创建回调函数和会话
          callback = SimpleCallback(pya)
          conv = OmniRealtimeConversation(model=model, callback=callback, url=url)
          # 3. 建立连接并配置会话
          conv.connect()
          conv.update_session(output_modalities=[MultiModality.AUDIO, MultiModality.TEXT], voice=voice, instructions=instructions)
          # 4. 初始化音频输入
          mic = pya.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)
          # 5. 主循环处理音频输入
          print("会话已启动。对着麦克风说话（按 Ctrl+C 退出）...")
          try:
            while True:
              audio_data = mic.read(3200, exception_on_overflow=False)
              conv.append_audio(base64.b64encode(audio_data).decode())
              time.sleep(0.01)
          except KeyboardInterrupt:
            # 清理资源
            conv.close()
            mic.close()
            callback.out.close()
            pya.terminate()
            print("\n会话已结束")
          ```
        </Accordion>

        运行 `vad_dash.py`，即可通过麦克风与 Qwen-Omni-Realtime 进行实时对话。系统会自动检测说话的开始和结束并发送到服务端，无需手动操作。
      </Tab>

      <Tab title="手动模式">
        新建 Python 文件 `manual_dash.py`，将以下代码复制到文件中：

        <Accordion title="manual_dash.py">
          ```python
          # 依赖: dashscope >= 1.23.9, pyaudio
          import os
          import base64
          import sys
          import threading
          import pyaudio
          from dashscope.audio.qwen_omni import *
          import dashscope

          # 如果未设置环境变量，请将下一行替换为你的 API Key: dashscope.api_key = "sk-xxx"
          dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')
          voice = 'Tina'

          class MyCallback(OmniRealtimeCallback):
            """最简回调: 连接后初始化扬声器，直接在事件中播放返回的音频"""
            def __init__(self, ctx):
              super().__init__()
              self.ctx = ctx

            def on_open(self) -> None:
              # 连接建立后初始化 PyAudio 和扬声器 (24k/单声道/16bit)
              print('连接已打开')
              try:
                self.ctx['pya'] = pyaudio.PyAudio()
                self.ctx['out'] = self.ctx['pya'].open(
                  format=pyaudio.paInt16,
                  channels=1,
                  rate=24000,
                  output=True
                )
                print('音频输出已初始化')
              except Exception as e:
                print('[错误] 初始化失败: {}'.format(e))

            def on_close(self, close_status_code, close_msg) -> None:
              print('连接已关闭 code: {}, msg: {}'.format(close_status_code, close_msg))
              sys.exit(0)

            def on_event(self, response: str) -> None:
              try:
                t = response['type']
                handlers = {
                  'session.created': lambda r: print('会话开始: {}'.format(r['session']['id'])),
                  'conversation.item.input_audio_transcription.delta': lambda r: print('\r用户问题: {}'.format(r.get('text', '') + r.get('stash', '')), end='', flush=True),
                  'conversation.item.input_audio_transcription.completed': self._transcription_completed,
                  'response.audio_transcript.delta': lambda r: print('模型回复: {}'.format(r['delta'])),
                  'response.audio.delta': self._play_audio,
                  'response.done': self._response_done,
                }
                h = handlers.get(t)
                if h:
                  h(response)
              except Exception as e:
                print('[错误] {}'.format(e))

            def _transcription_completed(self, response):
              print()
              self.ctx['transcription_done'].set()

            def _play_audio(self, response):
              # 直接解码 base64 并写入输出流播放
              if self.ctx['out'] is None:
                return
              try:
                data = base64.b64decode(response['delta'])
                self.ctx['out'].write(data)
              except Exception as e:
                print('[错误] 音频播放失败: {}'.format(e))

            def _response_done(self, response):
              # 标记本轮对话完成，用于主循环等待
              if self.ctx['conv'] is not None:
                print('[Metric] response: {}, first text delay: {}, first audio delay: {}'.format(
                  self.ctx['conv'].get_last_response_id(),
                  self.ctx['conv'].get_last_first_text_delay(),
                  self.ctx['conv'].get_last_first_audio_delay(),
                ))
              if self.ctx['resp_done'] is not None:
                self.ctx['resp_done'].set()

          def shutdown_ctx(ctx):
            """安全释放音频和 PyAudio 资源"""
            try:
              if ctx['out'] is not None:
                ctx['out'].close()
                ctx['out'] = None
            except Exception:
              pass
            try:
              if ctx['pya'] is not None:
                ctx['pya'].terminate()
                ctx['pya'] = None
            except Exception:
              pass

          def stream_record_and_send(pya_inst, conversation, sample_rate=16000, chunk_size=3200):
            stop_evt = threading.Event()
            stream = pya_inst.open(
              format=pyaudio.paInt16,
              channels=1,
              rate=sample_rate,
              input=True,
              frames_per_buffer=chunk_size
            )

            def _reader():
              while not stop_evt.is_set():
                try:
                  data = stream.read(chunk_size, exception_on_overflow=False)
                  conversation.append_audio(base64.b64encode(data).decode())
                except Exception:
                  break

            t = threading.Thread(target=_reader, daemon=True)
            t.start()
            input()
            stop_evt.set()
            t.join(timeout=1.0)
            stream.close()

          if __name__  == '__main__':
            print('初始化中 ...')
            # 运行时上下文: 存储音频和会话句柄
            ctx = {'pya': None, 'out': None, 'conv': None, 'resp_done': threading.Event(), 'transcription_done': threading.Event()}
            callback = MyCallback(ctx)
            conversation = OmniRealtimeConversation(
              model='qwen3.5-omni-plus-realtime',
              callback=callback,
              url="wss://dashscope.aliyuncs.com/api-ws/v1/realtime",
            )
            try:
              conversation.connect()
            except Exception as e:
              print('[错误] 连接失败: {}'.format(e))
              sys.exit(1)

            ctx['conv'] = conversation
            # 会话配置: 开启文本和音频输出 (关闭服务端 VAD，切换为手动录音)
            conversation.update_session(
              output_modalities=[MultiModality.AUDIO, MultiModality.TEXT],
              voice=voice,
              enable_input_audio_transcription=True,
              # 用于转写输入音频的模型，仅支持 gummy-realtime-v1
              input_audio_transcription_model='gummy-realtime-v1',
              enable_turn_detection=False,
              instructions="你是小云，一个私人助手。请准确、友好地回答用户的问题，始终保持乐于助人的态度。"
            )

            try:
              turn = 1
              while True:
                print(f"\n--- 第 {turn} 轮 ---")
                print("按 Enter 开始录音（输入 q 退出）...")
                user_input = input()
                if user_input.strip().lower() in ['q', 'quit']:
                  print("用户请求退出...")
                  break
                print("录音中... 再次按 Enter 停止。")
                if ctx['pya'] is None:
                  ctx['pya'] = pyaudio.PyAudio()
                stream_record_and_send(ctx['pya'], conversation)

                ctx['transcription_done'].clear()
                ctx['resp_done'].clear()
                conversation.commit()
                ctx['transcription_done'].wait(timeout=10)
                print("等待模型回复...")
                conversation.create_response()
                ctx['resp_done'].wait()
                turn += 1
            except KeyboardInterrupt:
              print("\n程序被用户中断。")
            finally:
              shutdown_ctx(ctx)
              print("程序已退出。")
          ```
        </Accordion>

        运行 `manual_dash.py`。按 Enter 开始录音说话。再次按 Enter 停止录音并接收模型的音频回复。
      </Tab>
    </Tabs>

    **GitHub 示例代码**

    从 GitHub 下载[完整示例代码](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/conversation/omni/python)，包括：

    1. **音频对话**：通过麦克风捕获实时音频，VAD 模式（`enable_turn_detection` = True），支持语音打断。
    2. **音视频对话**：通过麦克风和摄像头捕获实时音频和视频，VAD 模式，支持语音打断。
    3. **本地调用**：使用本地音频和图像作为输入，手动模式（`enable_turn_detection` = False）。

    <Note>请使用耳机进行音频播放，避免回声触发语音打断。</Note>
  </Tab>

  <Tab title="DashScope Java SDK">
    DashScope Java SDK 需 2.20.9 及以上版本。Maven 和 Gradle 配置参见[安装 SDK](/api-reference/preparation/install-sdk)。

    **选择交互模式**

    - VAD 模式（自动检测说话的开始和结束）

      Realtime API 自动判断用户何时开始和停止说话并作出响应。

    - 手动模式（按住说话，松开发送）

      由客户端控制说话的开始和结束。用户说完后，客户端需主动向服务端发送消息。

    <Tabs>
      <Tab title="VAD 模式">
        <Accordion title="OmniServerVad.java">
          ```java
          import com.alibaba.dashscope.audio.omni.*;
          import com.alibaba.dashscope.exception.NoApiKeyException;
          import com.google.gson.JsonObject;
          import javax.sound.sampled.*;
          import java.nio.ByteBuffer;
          import java.util.Arrays;
          import java.util.Base64;
          import java.util.Map;
          import java.util.Queue;
          import java.util.concurrent.ConcurrentLinkedQueue;
          import java.util.concurrent.atomic.AtomicBoolean;

          public class OmniServerVad {
            static class SequentialAudioPlayer {
              private final SourceDataLine line;
              private final Queue<byte[]> audioQueue = new ConcurrentLinkedQueue<>();
              private final Thread playerThread;
              private final AtomicBoolean shouldStop = new AtomicBoolean(false);

              public SequentialAudioPlayer() throws LineUnavailableException {
                AudioFormat format = new AudioFormat(24000, 16, 1, true, false);
                line = AudioSystem.getSourceDataLine(format);
                line.open(format);
                line.start();

                playerThread = new Thread(() -> {
                  while (!shouldStop.get()) {
                    byte[] audio = audioQueue.poll();
                    if (audio != null) {
                      line.write(audio, 0, audio.length);
                    } else {
                      try { Thread.sleep(10); } catch (InterruptedException ignored) {}
                    }
                  }
                }, "AudioPlayer");
                playerThread.start();
              }

              public void play(String base64Audio) {
                try {
                  byte[] audio = Base64.getDecoder().decode(base64Audio);
                  audioQueue.add(audio);
                } catch (Exception e) {
                  System.err.println("音频解码失败: " + e.getMessage());
                }
              }

              public void cancel() {
                audioQueue.clear();
                line.flush();
              }

              public void close() {
                shouldStop.set(true);
                try { playerThread.join(1000); } catch (InterruptedException ignored) {}
                line.drain();
                line.close();
              }
            }

            public static void main(String[] args) {
              try {
                SequentialAudioPlayer player = new SequentialAudioPlayer();
                AtomicBoolean userIsSpeaking = new AtomicBoolean(false);
                AtomicBoolean shouldStop = new AtomicBoolean(false);

                OmniRealtimeParam param = OmniRealtimeParam.builder()
                    .model("qwen3.5-omni-plus-realtime")
                    .apikey(System.getenv("DASHSCOPE_API_KEY"))
                    .url("wss://dashscope.aliyuncs.com/api-ws/v1/realtime")
                    .build();

                OmniRealtimeConversation conversation = new OmniRealtimeConversation(param, new OmniRealtimeCallback() {
                  @Override public void onOpen() {
                    System.out.println("连接已建立");
                  }
                  @Override public void onClose(int code, String reason) {
                    System.out.println("连接已关闭 (" + code + "): " + reason);
                    shouldStop.set(true);
                  }
                  @Override public void onEvent(JsonObject event) {
                    handleEvent(event, player, userIsSpeaking);
                  }
                });

                conversation.connect();
                conversation.updateSession(OmniRealtimeConfig.builder()
                    .modalities(Arrays.asList(OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT))
                    .voice("Tina")
                    .enableTurnDetection(true)
                    .enableInputAudioTranscription(true)
                    .parameters(Map.of("instructions",
                        "你是五星级酒店的 AI 客服。请准确、友好地回答客户关于房型、设施、价格和预订政策的问题。始终保持专业和乐于助人的态度。不要提供未经确认的信息或超出酒店服务范围的信息。"))
                    .build()
                );

                System.out.println("请开始说话（自动检测说话开始/结束，按 Ctrl+C 退出）...");
                AudioFormat format = new AudioFormat(16000, 16, 1, true, false);
                TargetDataLine mic = AudioSystem.getTargetDataLine(format);
                mic.open(format);
                mic.start();

                ByteBuffer buffer = ByteBuffer.allocate(3200);
                while (!shouldStop.get()) {
                  int bytesRead = mic.read(buffer.array(), 0, buffer.capacity());
                  if (bytesRead > 0) {
                    try {
                      conversation.appendAudio(Base64.getEncoder().encodeToString(buffer.array()));
                    } catch (Exception e) {
                      if (e.getMessage() != null && e.getMessage().contains("closed")) {
                        System.out.println("会话已关闭。停止录音。");
                        break;
                      }
                    }
                  }
                  Thread.sleep(20);
                }

                conversation.close(1000, "正常退出");
                player.close();
                mic.close();
                System.out.println("\n程序已退出。");

              } catch (NoApiKeyException e) {
                System.err.println("未找到 API KEY: 请设置 DASHSCOPE_API_KEY 环境变量。");
                System.exit(1);
              } catch (Exception e) {
                e.printStackTrace();
              }
            }

            private static void handleEvent(JsonObject event, SequentialAudioPlayer player, AtomicBoolean userIsSpeaking) {
              String type = event.get("type").getAsString();
              switch (type) {
                case "input_audio_buffer.speech_started":
                  System.out.println("\n[用户开始说话]");
                  player.cancel();
                  userIsSpeaking.set(true);
                  break;
                case "input_audio_buffer.speech_stopped":
                  System.out.println("[用户停止说话]");
                  userIsSpeaking.set(false);
                  break;
                case "response.audio.delta":
                  if (!userIsSpeaking.get()) {
                    player.play(event.get("delta").getAsString());
                  }
                  break;
                case "conversation.item.input_audio_transcription.delta":
                  // 流式预览：text为已确认前缀，stash为待确认后缀
                  String preview = event.get("text").getAsString() + event.get("stash").getAsString();
                  System.out.print("\r用户: " + preview);
                  break;
                case "conversation.item.input_audio_transcription.completed":
                  System.out.println();
                  break;
                case "response.audio_transcript.done":
                  System.out.println("助手: " + event.get("transcript").getAsString());
                  break;
                case "response.done":
                  System.out.println("回复完成");
                  break;
              }
            }
          }
          ```
        </Accordion>

        运行 `OmniServerVad.main()` 方法，即可通过麦克风与 Realtime 模型进行实时对话。系统会自动检测音频开始并发送到服务端，无需手动发送。
      </Tab>

      <Tab title="手动模式">
        <Accordion title="OmniWithoutServerVad.java">
          ```java
          // DashScope Java SDK 2.20.9 及以上版本

          import com.alibaba.dashscope.audio.omni.*;
          import com.alibaba.dashscope.exception.NoApiKeyException;
          import com.google.gson.JsonObject;
          import javax.sound.sampled.*;
          import java.io.ByteArrayOutputStream;
          import java.io.IOException;
          import java.util.Arrays;
          import java.util.Base64;
          import java.util.HashMap;
          import java.util.Queue;
          import java.util.concurrent.ConcurrentLinkedQueue;
          import java.util.concurrent.CountDownLatch;
          import java.util.concurrent.atomic.AtomicBoolean;
          import java.util.concurrent.atomic.AtomicReference;

          public class Main {
            // RealtimePcmPlayer 类定义开始
            public static class RealtimePcmPlayer {
              private int sampleRate;
              private SourceDataLine line;
              private AudioFormat audioFormat;
              private Thread decoderThread;
              private Thread playerThread;
              private AtomicBoolean stopped = new AtomicBoolean(false);
              private Queue<String> b64AudioBuffer = new ConcurrentLinkedQueue<>();
              private Queue<byte[]> RawAudioBuffer = new ConcurrentLinkedQueue<>();

              // 构造函数初始化音频格式和音频线
              public RealtimePcmPlayer(int sampleRate) throws LineUnavailableException {
                this.sampleRate = sampleRate;
                this.audioFormat = new AudioFormat(this.sampleRate, 16, 1, true, false);
                DataLine.Info info = new DataLine.Info(SourceDataLine.class, audioFormat);
                line = (SourceDataLine) AudioSystem.getLine(info);
                line.open(audioFormat);
                line.start();
                decoderThread = new Thread(new Runnable() {
                  @Override
                  public void run() {
                    while (!stopped.get()) {
                      String b64Audio = b64AudioBuffer.poll();
                      if (b64Audio != null) {
                        byte[] rawAudio = Base64.getDecoder().decode(b64Audio);
                        RawAudioBuffer.add(rawAudio);
                      } else {
                        try {
                          Thread.sleep(100);
                        } catch (InterruptedException e) {
                          throw new RuntimeException(e);
                        }
                      }
                    }
                  }
                });
                playerThread = new Thread(new Runnable() {
                  @Override
                  public void run() {
                    while (!stopped.get()) {
                      byte[] rawAudio = RawAudioBuffer.poll();
                      if (rawAudio != null) {
                        try {
                          playChunk(rawAudio);
                        } catch (IOException e) {
                          throw new RuntimeException(e);
                        } catch (InterruptedException e) {
                          throw new RuntimeException(e);
                        }
                      } else {
                        try {
                          Thread.sleep(100);
                        } catch (InterruptedException e) {
                          throw new RuntimeException(e);
                        }
                      }
                    }
                  }
                });
                decoderThread.start();
                playerThread.start();
              }

              // 播放一段音频，阻塞直到播放完成
              private void playChunk(byte[] chunk) throws IOException, InterruptedException {
                if (chunk == null || chunk.length == 0) return;

                int bytesWritten = 0;
                while (bytesWritten < chunk.length) {
                  bytesWritten += line.write(chunk, bytesWritten, chunk.length - bytesWritten);
                }
                int audioLength = chunk.length / (this.sampleRate*2/1000);
                // 等待缓冲区中的音频播放完毕
                Thread.sleep(audioLength - 10);
              }

              public void write(String b64Audio) {
                b64AudioBuffer.add(b64Audio);
              }

              public void cancel() {
                b64AudioBuffer.clear();
                RawAudioBuffer.clear();
              }

              public void waitForComplete() throws InterruptedException {
                while (!b64AudioBuffer.isEmpty() || !RawAudioBuffer.isEmpty()) {
                  Thread.sleep(100);
                }
                line.drain();
              }

              public void shutdown() throws InterruptedException {
                stopped.set(true);
                decoderThread.join();
                playerThread.join();
                if (line != null && line.isRunning()) {
                  line.drain();
                  line.close();
                }
              }
            } // RealtimePcmPlayer 类定义结束
            // 添加录音方法
            private static void recordAndSend(TargetDataLine line, OmniRealtimeConversation conversation) throws IOException {
              ByteArrayOutputStream out = new ByteArrayOutputStream();
              byte[] buffer = new byte[3200];
              AtomicBoolean stopRecording = new AtomicBoolean(false);

              // 启动一个线程监听 Enter 键
              Thread enterKeyListener = new Thread(() -> {
                try {
                  System.in.read();
                  stopRecording.set(true);
                } catch (IOException e) {
                  e.printStackTrace();
                }
              });
              enterKeyListener.start();

              // 录音循环
              while (!stopRecording.get()) {
                int count = line.read(buffer, 0, buffer.length);
                if (count > 0) {
                  out.write(buffer, 0, count);
                }
              }

              // 发送录音数据
              byte[] audioData = out.toByteArray();
              String audioB64 = Base64.getEncoder().encodeToString(audioData);
              conversation.appendAudio(audioB64);
              out.close();
            }

            public static void main(String[] args) throws InterruptedException, LineUnavailableException {
              OmniRealtimeParam param = OmniRealtimeParam.builder()
                  .model("qwen3.5-omni-plus-realtime")
                  // 如果未配置环境变量，请将下一行替换为你的 API Key: .apikey("sk-xxx")
                  .apikey(System.getenv("DASHSCOPE_API_KEY"))
                  .url("wss://dashscope.aliyuncs.com/api-ws/v1/realtime")
                  .build();
              AtomicReference<CountDownLatch> responseDoneLatch = new AtomicReference<>(null);
              responseDoneLatch.set(new CountDownLatch(1));

              RealtimePcmPlayer audioPlayer = new RealtimePcmPlayer(24000);
              final AtomicReference<OmniRealtimeConversation> conversationRef = new AtomicReference<>(null);
              OmniRealtimeConversation conversation = new OmniRealtimeConversation(param, new OmniRealtimeCallback() {
                @Override
                public void onOpen() {
                  System.out.println("连接已打开");
                }
                @Override
                public void onEvent(JsonObject message) {
                  String type = message.get("type").getAsString();
                  switch(type) {
                    case "session.created":
                      System.out.println("会话开始: " + message.get("session").getAsJsonObject().get("id").getAsString());
                      break;
                    case "conversation.item.input_audio_transcription.delta":
                      // 流式预览：text为已确认前缀，stash为待确认后缀
                      String transcriptPreview = message.get("text").getAsString() + message.get("stash").getAsString();
                      System.out.print("\r用户问题: " + transcriptPreview);
                      break;
                    case "conversation.item.input_audio_transcription.completed":
                      System.out.println();
                      transcriptionDoneLatch.get().countDown();
                      break;
                    case "response.audio_transcript.delta":
                      System.out.println("收到模型回复: " + message.get("delta").getAsString());
                      break;
                    case "response.audio.delta":
                      String recvAudioB64 = message.get("delta").getAsString();
                      audioPlayer.write(recvAudioB64);
                      break;
                    case "response.done":
                      System.out.println("======回复完成======");
                      if (conversationRef.get() != null) {
                        System.out.println("[性能] response: " + conversationRef.get().getResponseId() +
                            ", 首文本延迟: " + conversationRef.get().getFirstTextDelay() +
                            " ms, 首音频延迟: " + conversationRef.get().getFirstAudioDelay() + " ms");
                      }
                      responseDoneLatch.get().countDown();
                      break;
                    default:
                      break;
                  }
                }
                @Override
                public void onClose(int code, String reason) {
                  System.out.println("连接已关闭 code: " + code + ", reason: " + reason);
                }
              });
              conversationRef.set(conversation);
              try {
                conversation.connect();
              } catch (NoApiKeyException e) {
                throw new RuntimeException(e);
              }
              OmniRealtimeConfig config = OmniRealtimeConfig.builder()
                  .modalities(Arrays.asList(OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT))
                  .voice("Tina")
                  .enableTurnDetection(false)
                  // 设置模型角色
                  .parameters(new HashMap<String, Object>() {{
                    put("instructions","你是小云，一个私人助手。请准确、友好地回答用户的问题，始终保持乐于助人的态度。");
                  }})
                  .build();
              conversation.updateSession(config);

              // 添加麦克风录音功能
              AudioFormat format = new AudioFormat(16000, 16, 1, true, false);
              DataLine.Info info = new DataLine.Info(TargetDataLine.class, format);

              if (!AudioSystem.isLineSupported(info)) {
                System.out.println("不支持的音频设备");
                return;
              }

              TargetDataLine line = null;
              try {
                line = (TargetDataLine) AudioSystem.getLine(info);
                line.open(format);
                line.start();

                while (true) {
                  System.out.println("按 Enter 开始录音...");
                  System.in.read();
                  System.out.println("录音已开始。请说话...再次按 Enter 停止录音并发送。");
                  recordAndSend(line, conversation);
                  conversation.commit();
                  conversation.createResponse(null, null);
                  responseDoneLatch.get().await();
                  // 重置 latch 以便下次等待
                  responseDoneLatch.set(new CountDownLatch(1));
                }
              } catch (LineUnavailableException e) {
                e.printStackTrace();
              } finally {
                if (line != null) {
                  line.stop();
                  line.close();
                }
              }
            }
          }
          ```
        </Accordion>

        运行 `Main.main()` 方法。按 Enter 开始录音。录音过程中再次按 Enter 停止录音并发送音频。随后接收并播放模型的回复。
      </Tab>
    </Tabs>

    **GitHub 示例代码**

    从 GitHub 下载[完整示例代码](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/conversation/omni/java)，包括：

    1. **音频对话**：通过麦克风捕获实时音频，VAD 模式（`enableTurnDetection` = true），支持语音打断。
    2. **音视频对话**：通过麦克风和摄像头捕获实时音频和视频，VAD 模式，支持语音打断。
    3. **本地调用**：使用本地音频和图像作为输入，手动模式（`enableTurnDetection` = false）。

    <Note>将 `enableTurnDetection` 参数设为 `true` 为 VAD 模式，设为 `false` 为手动模式。请使用耳机进行音频播放，避免回声触发语音打断。</Note>
  </Tab>

  <Tab title="WebSocket（Python）">
    <Steps>
      <Step title="准备运行环境">
        Python 版本需为 3.10 或以上。

        首先根据操作系统安装 PyAudio。

        <Tabs>
          <Tab title="macOS">
            ```bash
            brew install portaudio && pip install pyaudio
            ```
          </Tab>

          <Tab title="Debian/Ubuntu">
            ```bash
            sudo apt-get install python3-pyaudio

            或

            pip install pyaudio
            ```

            <Info>
              推荐直接运行 `pip install pyaudio`。如果安装失败，请先为操作系统安装 `portaudio` 依赖。
            </Info>
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

        安装完成后，使用 pip 安装 WebSocket 相关依赖：

        ```bash
        pip install websockets==15.0.1
        ```

        联网搜索示例（`search_ws.py`）额外依赖 `websocket-client` 库：

        ```bash
        pip install websocket-client
        ```
      </Step>

      <Step title="创建客户端">
        在本地目录新建 Python 文件 `omni_realtime_client.py`，将以下代码复制到文件中：

        <Accordion title="omni_realtime_client.py">
          ```python
          import asyncio
          import websockets
          import json
          import base64
          import time
          from typing import Optional, Callable, List, Dict, Any
          from enum import Enum

          class TurnDetectionMode(Enum):
            SERVER_VAD = "server_vad"
            MANUAL = "manual"

          class OmniRealtimeClient:

            def __init__(
                self,
                base_url,
                api_key: str,
                model: str = "",
                voice: str = "Tina",
                instructions: str = "你是小云，一个私人助手。请用幽默风趣的方式回答用户的问题。",
                turn_detection_mode: TurnDetectionMode = TurnDetectionMode.SERVER_VAD,
                on_text_delta: Optional[Callable[[str], None]] = None,
                on_audio_delta: Optional[Callable[[bytes], None]] = None,
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
              self.on_audio_delta = on_audio_delta
              self.on_input_transcript = on_input_transcript
              self.on_output_transcript = on_output_transcript
              self.turn_detection_mode = turn_detection_mode
              self.extra_event_handlers = extra_event_handlers or {}

              # 当前响应状态
              self._current_response_id = None
              self._current_item_id = None
              self._is_responding = False
              # 输入/输出转写打印状态
              self._print_input_transcript = True
              self._output_transcript_buffer = ""

            async def connect(self) -> None:
              """建立 WebSocket 连接。"""
              url = f"{self.base_url}?model={self.model}"
              headers = {
                "Authorization": f"Bearer {self.api_key}"
              }
              self.ws = await websockets.connect(url, additional_headers=headers)

              # 会话配置
              session_config = {
                "modalities": ["text", "audio"],
                "voice": self.voice,
                "instructions": self.instructions,
                # 配置音频输入/输出格式和采样率
                "audio": {
                  "input": {"format": {"type": "pcm", "sample_rate": 16000}},
                  "output": {"format": {"type": "pcm", "sample_rate": 24000}}
                },
                "input_audio_transcription": {
                  "model": "qwen3-asr-flash-realtime"
                }
              }

              if self.turn_detection_mode == TurnDetectionMode.MANUAL:
                session_config['turn_detection'] = None
                await self.update_session(session_config)
              elif self.turn_detection_mode == TurnDetectionMode.SERVER_VAD:
                session_config['turn_detection'] = {
                  "type": "server_vad",
                  "threshold": 0.1,
                  "prefix_padding_ms": 500,
                  "silence_duration_ms": 900
                }
                await self.update_session(session_config)
              else:
                raise ValueError(f"无效的交互检测模式: {self.turn_detection_mode}")

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
              """流式发送原始音频数据。"""
              # 仅支持 16 位、16 kHz、单声道 PCM
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

            async def append_image(self, image_chunk: bytes) -> None:
              """将图像数据追加到图像缓冲区。
              图像数据可来自本地文件或实时视频流。
              注意：
                - 图像格式必须为 JPG 或 JPEG。推荐分辨率为 480p 或 720p，最高支持 1080p。
                - 单张图片经 Base64 编码后不得超过 256 KB，建议编码前原始图片不超过 190 KB。
                - 发送前需将图像数据编码为 Base64。
                - 建议以不超过每秒 1 帧的速率向服务器发送图像数据。
                - 发送图像数据之前，必须至少发送一次音频数据。
              """
              image_b64 = base64.b64encode(image_chunk).decode()
              event = {
                "type": "input_image_buffer.append",
                "image": image_b64
              }
              await self.send_event(event)

            async def create_response(self) -> None:
              """请求 API 生成响应（仅在手动模式下调用）。"""
              event = {
                "type": "response.create"
              }
              await self.send_event(event)

            async def cancel_response(self) -> None:
              """取消当前响应。"""
              event = {
                "type": "response.cancel"
              }
              await self.send_event(event)

            async def handle_interruption(self):
              """处理用户中断当前响应。"""
              if not self._is_responding:
                return
              # 1. 取消当前响应
              if self._current_response_id:
                await self.cancel_response()

              self._is_responding = False
              self._current_response_id = None
              self._current_item_id = None

            async def handle_messages(self) -> None:
              try:
                async for message in self.ws:
                  event = json.loads(message)
                  event_type = event.get("type")
                  if event_type == "error":
                    print(" 错误: ", event['error'])
                    continue
                  elif event_type == "response.created":
                    self._current_response_id = event.get("response", {}).get("id")
                    self._is_responding = True
                  elif event_type == "response.output_item.added":
                    self._current_item_id = event.get("item", {}).get("id")
                  elif event_type == "response.done":
                    self._is_responding = False
                    self._current_response_id = None
                    self._current_item_id = None
                  elif event_type == "input_audio_buffer.speech_started":
                    print("检测到说话开始")
                    if self._is_responding:
                      print("处理打断")
                      await self.handle_interruption()
                  elif event_type == "input_audio_buffer.speech_stopped":
                    print("检测到说话结束")
                  elif event_type == "response.text.delta":
                    if self.on_text_delta:
                      self.on_text_delta(event["delta"])
                  elif event_type == "response.audio.delta":
                    if self.on_audio_delta:
                      audio_bytes = base64.b64decode(event["delta"])
                      self.on_audio_delta(audio_bytes)
                  elif event_type == "conversation.item.input_audio_transcription.delta":
                    preview = event.get("text", "") + event.get("stash", "")
                    print(f"\r用户: {preview}", end='', flush=True)
                  elif event_type == "conversation.item.input_audio_transcription.completed":
                    transcript = event.get("transcript", "")
                    print()
                    if self.on_input_transcript:
                      await asyncio.to_thread(self.on_input_transcript, transcript)
                      self._print_input_transcript = True
                  elif event_type == "response.audio_transcript.delta":
                    if self.on_output_transcript:
                      delta = event.get("delta", "")
                      if not self._print_input_transcript:
                        self._output_transcript_buffer += delta
                      else:
                        if self._output_transcript_buffer:
                          await asyncio.to_thread(self.on_output_transcript, self._output_transcript_buffer)
                          self._output_transcript_buffer = ""
                        await asyncio.to_thread(self.on_output_transcript, delta)
                  elif event_type == "response.audio_transcript.done":
                    print(f"模型: {event.get('transcript', '')}")
                    self._print_input_transcript = False
                  elif event_type in self.extra_event_handlers:
                    self.extra_event_handlers[event_type](event)
              except websockets.exceptions.ConnectionClosed:
                print(" 连接已关闭")
              except Exception as e:
                print(" 消息处理出错: ", str(e))
            async def close(self) -> None:
              """关闭 WebSocket 连接。"""
              if self.ws:
                await self.ws.close()
          ```
        </Accordion>
      </Step>

      <Step title="选择交互模式">
        - VAD 模式（自动检测说话的开始和结束）

          服务端自动判断用户何时开始和停止说话并作出响应。

        - 手动模式（按住说话，松开发送）

          由客户端控制说话的开始和结束。用户说完后，客户端需主动向服务端发送消息。

        <Tabs>
          <Tab title="VAD 模式">
            在 `omni_realtime_client.py` 所在目录新建 Python 文件 `vad_mode.py`，将以下代码复制到文件中：

            <Accordion title="vad_mode.py">
              ```python
              # -- coding: utf-8 --
              import os, asyncio, pyaudio, queue, threading
              from omni_realtime_client import OmniRealtimeClient, TurnDetectionMode

              # 音频播放类（处理打断）
              class AudioPlayer:
                def __init__(self, pyaudio_instance, rate=24000):
                  self.stream = pyaudio_instance.open(format=pyaudio.paInt16, channels=1, rate=rate, output=True)
                  self.queue = queue.Queue()
                  self.stop_evt = threading.Event()
                  self.interrupt_evt = threading.Event()
                  threading.Thread(target=self._run, daemon=True).start()

                def _run(self):
                  while not self.stop_evt.is_set():
                    try:
                      data = self.queue.get(timeout=0.5)
                      if data is None: break
                      if not self.interrupt_evt.is_set(): self.stream.write(data)
                      self.queue.task_done()
                    except queue.Empty: continue

                def add_audio(self, data): self.queue.put(data)
                def handle_interrupt(self): self.interrupt_evt.set(); self.queue.queue.clear()
                def stop(self): self.stop_evt.set(); self.queue.put(None); self.stream.stop_stream(); self.stream.close()

              # 从麦克风录音并发送
              async def record_and_send(client):
                p = pyaudio.PyAudio()
                stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=3200)
                print("录音已开始。请说话...")
                try:
                  while True:
                    audio_data = stream.read(3200)
                    await client.stream_audio(audio_data)
                    await asyncio.sleep(0.02)
                finally:
                  stream.stop_stream(); stream.close(); p.terminate()

              async def main():
                p = pyaudio.PyAudio()
                player = AudioPlayer(pyaudio_instance=p)

                client = OmniRealtimeClient(
                  base_url="wss://dashscope.aliyuncs.com/api-ws/v1/realtime",
                  api_key=os.environ.get("DASHSCOPE_API_KEY"),
                  model="qwen3.5-omni-plus-realtime",
                  voice="Tina",
                  instructions="你是小云，一个风趣幽默的助手。",
                  turn_detection_mode=TurnDetectionMode.SERVER_VAD,
                  on_text_delta=lambda t: print(f"\n助手: {t}", end="", flush=True),
                  on_audio_delta=player.add_audio,
                )

                await client.connect()
                print("连接成功。开始实时对话...")

                # 并发运行
                await asyncio.gather(client.handle_messages(), record_and_send(client))

              if __name__ == "__main__":
                try:
                  asyncio.run(main())
                except KeyboardInterrupt:
                  print("\n程序已退出。")
              ```
            </Accordion>

            运行 `vad_mode.py`，即可通过麦克风与 Qwen-Omni-Realtime 进行实时对话。系统会自动检测说话的开始和结束并发送到服务端，无需手动操作。
          </Tab>

          <Tab title="手动模式">
            在 `omni_realtime_client.py` 所在目录新建 Python 文件 `manual_mode.py`，将以下代码复制到文件中：

            <Accordion title="manual_mode.py">
              ```python
              # -- coding: utf-8 --
              import os
              import asyncio
              import time
              import threading
              import queue
              import pyaudio
              from omni_realtime_client import OmniRealtimeClient, TurnDetectionMode

              class AudioPlayer:
                """实时音频播放器"""

                def __init__(self, sample_rate=24000, channels=1, sample_width=2):
                  self.sample_rate = sample_rate
                  self.channels = channels
                  self.sample_width = sample_width  # 16 位占 2 字节
                  self.audio_queue = queue.Queue()
                  self.is_playing = False
                  self.play_thread = None
                  self.pyaudio_instance = None
                  self.stream = None
                  self._lock = threading.Lock()  # 用于同步访问的锁
                  self._last_data_time = time.time()  # 最后一次接收数据的时间
                  self._response_done = False  # 标记响应是否完成的标志
                  self._waiting_for_response = False  # 等待服务器响应的标志
                  # 最后一次写入音频流的时间和最近音频块的时长，用于更精确地检测播放结束
                  self._last_play_time = time.time()
                  self._last_chunk_duration = 0.0

                def start(self):
                  """启动音频播放器"""
                  with self._lock:
                    if self.is_playing:
                      return

                    self.is_playing = True

                    try:
                      self.pyaudio_instance = pyaudio.PyAudio()

                      # 创建音频输出流
                      self.stream = self.pyaudio_instance.open(
                        format=pyaudio.paInt16,  # 16 位
                        channels=self.channels,
                        rate=self.sample_rate,
                        output=True,
                        frames_per_buffer=1024
                      )

                      # 启动播放线程
                      self.play_thread = threading.Thread(target=self._play_audio)
                      self.play_thread.daemon = True
                      self.play_thread.start()

                      print("音频播放器已启动")
                    except Exception as e:
                      print(f"启动音频播放器失败: {e}")
                      self._cleanup_resources()
                      raise

                def stop(self):
                  """停止音频播放器"""
                  with self._lock:
                    if not self.is_playing:
                      return

                    self.is_playing = False

                  # 清空队列
                  while not self.audio_queue.empty():
                    try:
                      self.audio_queue.get_nowait()
                    except queue.Empty:
                      break

                  # 等待播放线程结束（在锁外等待，避免死锁）
                  if self.play_thread and self.play_thread.is_alive():
                    self.play_thread.join(timeout=2.0)

                  # 再次获取锁以清理资源
                  with self._lock:
                    self._cleanup_resources()

                  print("音频播放器已停止")

                def _cleanup_resources(self):
                  """清理音频资源（必须在持有锁的情况下调用）"""
                  try:
                    # 关闭音频流
                    if self.stream:
                      if not self.stream.is_stopped():
                        self.stream.stop_stream()
                      self.stream.close()
                      self.stream = None
                  except Exception as e:
                    print(f"关闭音频流出错: {e}")

                  try:
                    if self.pyaudio_instance:
                      self.pyaudio_instance.terminate()
                      self.pyaudio_instance = None
                  except Exception as e:
                    print(f"终止 PyAudio 出错: {e}")

                def add_audio_data(self, audio_data):
                  """将音频数据添加到播放队列"""
                  if self.is_playing and audio_data:
                    self.audio_queue.put(audio_data)
                    with self._lock:
                      self._last_data_time = time.time()  # 更新最后一次接收数据的时间
                      self._waiting_for_response = False  # 收到数据，不再等待

                def stop_receiving_data(self):
                  """标记不再有新的音频数据接收"""
                  with self._lock:
                    self._response_done = True
                    self._waiting_for_response = False  # 响应结束，不再等待

                def prepare_for_next_turn(self):
                  """重置播放器状态，为下一轮对话做准备。"""
                  with self._lock:
                    self._response_done = False
                    self._last_data_time = time.time()
                    self._last_play_time = time.time()
                    self._last_chunk_duration = 0.0
                    self._waiting_for_response = True  # 开始等待下一个响应

                  # 清除上一轮对话的剩余音频数据
                  while not self.audio_queue.empty():
                    try:
                      self.audio_queue.get_nowait()
                    except queue.Empty:
                      break

                def is_finished_playing(self):
                  """检查是否所有音频数据已播放完毕"""
                  with self._lock:
                    queue_size = self.audio_queue.qsize()
                    time_since_last_data = time.time() - self._last_data_time
                    time_since_last_play = time.time() - self._last_play_time

                    # ---------------------- 智能结束检测 ----------------------
                    # 1. 首选：如果服务器已标记完成且播放队列为空。
                    #    等待最近一个音频块播放完毕（块时长 + 0.1s 容差）。
                    if self._response_done and queue_size == 0:
                      min_wait = max(self._last_chunk_duration + 0.1, 0.5)  # 至少等待 0.5s
                      if time_since_last_play >= min_wait:
                        return True

                    # 2. 备选：如果长时间没有收到新数据且播放队列为空。
                    #    此逻辑作为服务器未明确发送 response.done 时的兜底方案。
                    if not self._waiting_for_response and queue_size == 0 and time_since_last_data > 1.0:
                      print("\n（长时间未收到新音频，假设播放已完成）")
                      return True

                    return False

                def _play_audio(self):
                  """播放音频数据的 worker 线程"""
                  while True:
                    # 检查是否应停止
                    with self._lock:
                      if not self.is_playing:
                        break
                      stream_ref = self.stream  # 获取流的引用

                    try:
                      # 从队列获取音频数据，超时时间 0.1 秒
                      audio_data = self.audio_queue.get(timeout=0.1)

                      # 再次检查状态和流的有效性
                      with self._lock:
                        if self.is_playing and stream_ref and not stream_ref.is_stopped():
                          try:
                            # 播放音频数据
                            stream_ref.write(audio_data)
                            # 更新最新的播放信息
                            self._last_play_time = time.time()
                            self._last_chunk_duration = len(audio_data) / (
                                  self.channels * self.sample_width) / self.sample_rate
                          except Exception as e:
                            print(f"写入音频流出错: {e}")
                            break

                      # 标记此数据块已处理
                      self.audio_queue.task_done()

                    except queue.Empty:
                      # 队列为空，继续等待
                      continue
                    except Exception as e:
                      print(f"播放音频出错: {e}")
                      break

              class MicrophoneRecorder:
                """实时麦克风录音器"""

                def __init__(self, sample_rate=16000, channels=1, chunk_size=3200):
                  self.sample_rate = sample_rate
                  self.channels = channels
                  self.chunk_size = chunk_size
                  self.pyaudio_instance = None
                  self.stream = None
                  self.frames = []
                  self._is_recording = False
                  self._record_thread = None

                def _recording_thread(self):
                  """录音 worker 线程"""
                  # 当 _is_recording 为 True 时持续从音频流读取数据
                  while self._is_recording:
                    try:
                      # 使用 exception_on_overflow=False 避免缓冲区溢出导致崩溃
                      data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                      self.frames.append(data)
                    except (IOError, OSError) as e:
                      # 当流被关闭时可能会报错
                      print(f"读取录音流出错，可能已被关闭: {e}")
                      break

                def start(self):
                  """开始录音"""
                  if self._is_recording:
                    print("录音已在进行中。")
                    return

                  self.frames = []
                  self._is_recording = True

                  try:
                    self.pyaudio_instance = pyaudio.PyAudio()
                    self.stream = self.pyaudio_instance.open(
                      format=pyaudio.paInt16,
                      channels=self.channels,
                      rate=self.sample_rate,
                      input=True,
                      frames_per_buffer=self.chunk_size
                    )

                    self._record_thread = threading.Thread(target=self._recording_thread)
                    self._record_thread.daemon = True
                    self._record_thread.start()
                    print("麦克风录音已开始...")
                  except Exception as e:
                    print(f"启动麦克风失败: {e}")
                    self._is_recording = False
                    self._cleanup()
                    raise

                def stop(self):
                  """停止录音并返回音频数据"""
                  if not self._is_recording:
                    return None

                  self._is_recording = False

                  # 等待录音线程安全退出
                  if self._record_thread:
                    self._record_thread.join(timeout=1.0)

                  self._cleanup()

                  print("麦克风录音已停止。")
                  return b''.join(self.frames)

                def _cleanup(self):
                  """安全清理 PyAudio 资源"""
                  if self.stream:
                    try:
                      if self.stream.is_active():
                        self.stream.stop_stream()
                      self.stream.close()
                    except Exception as e:
                      print(f"关闭音频流出错: {e}")

                  if self.pyaudio_instance:
                    try:
                      self.pyaudio_instance.terminate()
                    except Exception as e:
                      print(f"终止 PyAudio 实例出错: {e}")

                  self.stream = None
                  self.pyaudio_instance = None

              async def interactive_test():
                """
                交互式测试脚本：支持多轮对话，每轮可发送音频和图像。
                """
                # ------------------- 1. 初始化并建立连接（一次性） -------------------
                api_key = os.environ.get("DASHSCOPE_API_KEY")
                if not api_key:
                  print("请设置 DASHSCOPE_API_KEY 环境变量。")
                  return

                print("--- 实时音视频多模态对话客户端 ---")
                print("正在初始化音频播放器和客户端...")

                audio_player = AudioPlayer()
                audio_player.start()

                def on_audio_received(audio_data):
                  audio_player.add_audio_data(audio_data)

                transcription_done = threading.Event()

                def on_transcription_completed(transcript):
                  transcription_done.set()

                def on_response_done(event):
                  print("\n（收到响应结束标记）")
                  audio_player.stop_receiving_data()

                realtime_client = OmniRealtimeClient(
                  base_url="wss://dashscope.aliyuncs.com/api-ws/v1/realtime",
                  api_key=api_key,
                  model="qwen3.5-omni-plus-realtime",
                  voice="Tina",
                  instructions="你是小云，一个私人助手。请准确、友好地回答用户的问题，始终保持乐于助人的态度。", # 设置模型角色
                  on_text_delta=lambda text: print(f"助手回复: {text}", end="", flush=True),
                  on_audio_delta=on_audio_received,
                  on_input_transcript=on_transcription_completed,
                  turn_detection_mode=TurnDetectionMode.MANUAL,
                  extra_event_handlers={"response.done": on_response_done}
                )

                message_handler_task = None
                try:
                  await realtime_client.connect()
                  print("已连接到服务器。随时输入 'q' 或 'quit' 退出。")
                  message_handler_task = asyncio.create_task(realtime_client.handle_messages())
                  await asyncio.sleep(0.5)

                  turn_counter = 1
                  # ------------------- 2. 多轮对话循环 -------------------
                  while True:
                    print(f"\n--- 第 {turn_counter} 轮 ---")
                    audio_player.prepare_for_next_turn()

                    recorded_audio = None
                    image_paths = []

                    # --- 获取用户输入：从麦克风录音 ---
                    loop = asyncio.get_event_loop()
                    recorder = MicrophoneRecorder(sample_rate=16000)  # 推荐 16k 采样率用于语音识别

                    print("准备录音。按 Enter 开始录音（或输入 'q' 退出）...")
                    user_input = await loop.run_in_executor(None, input)
                    if user_input.strip().lower() in ['q', 'quit']:
                      print("用户请求退出...")
                      return

                    try:
                      recorder.start()
                    except Exception:
                      print("无法启动录音。请检查麦克风权限和设备。跳过本轮。")
                      continue

                    print("录音中...再次按 Enter 停止录音。")
                    await loop.run_in_executor(None, input)

                    recorded_audio = recorder.stop()

                    if not recorded_audio or len(recorded_audio) == 0:
                      print("未录制到有效音频。请重新开始本轮。")
                      continue

                    # --- 3. 发送数据并获取响应 ---
                    print("\n--- 输入确认 ---")
                    print(f"待处理音频: 1（来自麦克风），图像: {len(image_paths)}")
                    print("------------------")

                    # 3.1 发送音频数据
                    try:
                      print(f"发送麦克风录音（{len(recorded_audio)} 字节）")
                      await realtime_client.stream_audio(recorded_audio)
                      await asyncio.sleep(0.1)
                    except Exception as e:
                      print(f"发送麦克风录音失败: {e}")
                      continue

                    # 3.3 提交并等待响应
                    print("录音结束，等待模型回复...")
                    await realtime_client.commit_audio_buffer()
                    # 等待转录完成后再触发模型回复，避免输出交错
                    await asyncio.to_thread(transcription_done.wait, 10)
                    transcription_done.clear()
                    await realtime_client.create_response()

                    print("等待并播放服务器响应音频...")
                    start_time = time.time()
                    max_wait_time = 60
                    while not audio_player.is_finished_playing():
                      if time.time() - start_time > max_wait_time:
                        print(f"\n等待超时（{max_wait_time} 秒）。进入下一轮。")
                        break
                      await asyncio.sleep(0.2)

                    print("\n本轮音频播放完成！")
                    turn_counter += 1

                except (asyncio.CancelledError, KeyboardInterrupt):
                  print("\n程序被中断。")
                except Exception as e:
                  print(f"发生未处理的错误: {e}")
                finally:
                  # ------------------- 4. 清理资源 -------------------
                  print("\n正在关闭连接并清理资源...")
                  if message_handler_task and not message_handler_task.done():
                    message_handler_task.cancel()

                  if 'realtime_client' in locals() and realtime_client.ws and not realtime_client.ws.closed:
                    await realtime_client.close()
                    print("连接已关闭。")

                  audio_player.stop()
                  print("程序已退出。")

              if __name__ == "__main__":
                try:
                  asyncio.run(interactive_test())
                except KeyboardInterrupt:
                  print("\n程序被用户强制退出。")
              ```
            </Accordion>

            运行 `manual_mode.py`。按 Enter 开始录音说话。再次按 Enter 停止录音并接收模型的音频回复。
          </Tab>
        </Tabs>
      </Step>
    </Steps>
  </Tab>

  <Tab title="WebRTC">
    <Tabs>
      <Tab title="Python">
        **准备运行环境**

        您的 Python 版本需要不低于 3.10。安装以下依赖：

        ```bash
        pip install aiortc aiohttp sounddevice numpy certifi av
        ```

        **运行示例**

        新建一个 Python 文件，命名为 `webrtc_demo.py`，并将以下代码复制到文件中：

        <Accordion title="webrtc_demo.py">
          ```python
          # 依赖安装：pip install aiortc aiohttp sounddevice numpy certifi av
          import asyncio
          import json
          import os
          import queue
          import ssl
          import threading

          import aiohttp
          import certifi
          import numpy as np
          import sounddevice as sd
          from aiortc import RTCPeerConnection, RTCConfiguration, RTCSessionDescription
          from aiortc.contrib.media import MediaPlayer
          from av import AudioFrame

          # 替换为您的 API Key，或通过环境变量 DASHSCOPE_API_KEY 设置
          API_KEY = os.getenv("DASHSCOPE_API_KEY", "your-api-key")
          MODEL = "qwen3.5-omni-plus-realtime"
          # 替换 {endpoint} 为您联系商务经理获取的接入地址
          SIGNALING_URL = f"https://{{endpoint}}/api/v1/webrtc/realtime?model={MODEL}"

          # --------------- 音频帧解析 ---------------

          def _nb_channels(frame: AudioFrame) -> int:
            """获取音频帧的声道数，兼容不同版本的 PyAV"""
            if hasattr(frame.layout, "nb_channels"):
              return int(frame.layout.nb_channels)
            ch = getattr(frame.layout, "channels", 1)
            if isinstance(ch, (tuple, list)):
              return len(ch)
            return int(ch)

          def audioframe_to_s16_samples(frame: AudioFrame) -> np.ndarray:
            """
            服务端返回的音频帧是双声道交错排列，直接 reshape 会声道错乱，需要按实际声道数重排为 (采样数, 声道数)。
            aiortc 底层解码库不同版本对同一份音频返回的数组形状不同，这里做统一处理。
            """
            arr = np.asarray(frame.to_ndarray())
            ch = _nb_channels(frame)
            samples = int(frame.samples)

            if arr.ndim == 2 and arr.shape[0] == ch and arr.shape[1] == samples:
              return arr.T.copy()
            if arr.ndim == 2 and arr.shape[0] == 1 and arr.shape[1] == samples * ch:
              return arr.reshape(-1).reshape(samples, ch).copy()
            if arr.ndim == 1 and arr.shape[0] == samples * ch:
              return arr.reshape(samples, ch).copy()

            flat = arr.reshape(-1)
            if ch > 0 and flat.size % ch == 0:
              return flat.reshape(flat.size // ch, ch).copy()
            raise ValueError(f"unexpected shape={arr.shape}, ch={ch}, samples={samples}")

          # --------------- 低延迟音频播放器 ---------------

          class RemoteAudioPlayer:
            """
            低延迟音频播放器，每次只取 5ms 的音频块播放，减少延迟。
            支持语音打断：用户开始说话时清空缓存，停止播放模型的旧回复。
            播放时将服务端返回的双声道音频合并为单声道（左右声道取均值）。
            """
            def __init__(self, samplerate=48000, out_channels=1, blocksize=240, max_seconds=0.2):
              self.samplerate = samplerate
              self.out_channels = out_channels
              self.blocksize = blocksize
              self._q = queue.Queue(maxsize=max(5, int(max_seconds * samplerate / blocksize) + 5))
              self._lock = threading.Lock()
              self._rb_size = max(1, int(max_seconds * samplerate))
              self._rb = np.zeros((self._rb_size, out_channels), dtype=np.int16)
              self._rb_w = 0
              self._rb_r = 0
              self._rb_len = 0
              self._stream = None
              self._closed = False

            def start(self):
              if self._stream:
                return

              def callback(outdata, frames, _time, status):
                if self._closed:
                  outdata[:] = np.zeros((frames, self.out_channels), dtype=np.int16)
                  return
                while True:
                  try:
                    chunk = self._q.get_nowait()
                  except queue.Empty:
                    break
                  with self._lock:
                    self._write_rb(chunk)
                with self._lock:
                  out = self._read_rb(frames)
                outdata[:] = out

              self._stream = sd.OutputStream(
                samplerate=self.samplerate,
                channels=self.out_channels,
                dtype="int16",
                blocksize=self.blocksize,
                callback=callback,
              )
              self._stream.start()

            def clear(self):
              """清空播放缓存，用于语音打断"""
              try:
                while True:
                  self._q.get_nowait()
              except queue.Empty:
                pass
              with self._lock:
                self._rb_w = 0
                self._rb_r = 0
                self._rb_len = 0
                self._rb[:] = 0

            def _write_rb(self, chunk: np.ndarray):
              n = int(chunk.shape[0])
              if n <= 0:
                return
              overflow = max(0, self._rb_len + n - self._rb_size)
              if overflow > 0:
                self._rb_r = (self._rb_r + overflow) % self._rb_size
                self._rb_len -= overflow
              end = self._rb_size - self._rb_w
              if n <= end:
                self._rb[self._rb_w:self._rb_w + n] = chunk
              else:
                self._rb[self._rb_w:] = chunk[:end]
                self._rb[:n - end] = chunk[end:]
              self._rb_w = (self._rb_w + n) % self._rb_size
              self._rb_len += n

            def _read_rb(self, frames: int) -> np.ndarray:
              if self._rb_len <= 0:
                return np.zeros((frames, self.out_channels), dtype=np.int16)
              n = min(frames, self._rb_len)
              out = np.zeros((frames, self.out_channels), dtype=np.int16)
              end = self._rb_size - self._rb_r
              if n <= end:
                out[:n] = self._rb[self._rb_r:self._rb_r + n]
              else:
                out[:end] = self._rb[self._rb_r:]
                out[end:n] = self._rb[:n - end]
              self._rb_r = (self._rb_r + n) % self._rb_size
              self._rb_len -= n
              return out

            async def push_frame(self, frame: AudioFrame):
              """接收音频帧，自动合并声道后入队"""
              if self._closed:
                return
              pcm = audioframe_to_s16_samples(frame)
              in_ch = pcm.shape[1]
              if self.out_channels == 1:
                if in_ch == 1:
                  out = pcm
                else:
                  out = np.mean(pcm.astype(np.int32), axis=1).astype(np.int16).reshape(-1, 1)
              else:
                if in_ch == self.out_channels:
                  out = pcm
                elif in_ch == 1 and self.out_channels == 2:
                  out = np.repeat(pcm, 2, axis=1)
                else:
                  out = pcm[:, :self.out_channels]
              try:
                self._q.put_nowait(out)
              except queue.Full:
                try:
                  self._q.get_nowait()
                except queue.Empty:
                  pass
                try:
                  self._q.put_nowait(out)
                except queue.Full:
                  pass

            async def close(self):
              self._closed = True
              if self._stream:
                self._stream.stop()
                self._stream.close()
                self._stream = None

          # --------------- main ---------------

          async def main():
            pc = RTCPeerConnection(RTCConfiguration(iceServers=[]))

            # 初始化音频播放器（单声道输出，5ms blocksize 低延迟）
            speaker = RemoteAudioPlayer(samplerate=48000, out_channels=1, blocksize=240, max_seconds=0.2)
            speaker.start()

            # 初始化麦克风（macOS avfoundation，Linux 请改为 pulse 或 alsa）
            mic = MediaPlayer("none:0", format="avfoundation",
                     options={"sample_rate": "48000", "channels": "1"})
            if not mic.audio:
              raise RuntimeError("未检测到麦克风，请检查 avfoundation 音频设备索引")
            pc.addTrack(mic.audio)

            # 客户端创建 DataChannel（名称可自定义），服务端会通过固定名为 "txt" 的通道推送事件
            pc.createDataChannel("oai-events")

            remote_dc = None
            got_first_txt_msg = False

            def make_session_update() -> dict:
              """构造 session.update 配置：音色、音频格式、VAD 策略、推理参数"""
              return {
                "type": "session.update",
                "session": {
                  "modalities": ["text", "audio"],
                  "voice": "Tina",
                  # 配置音频输入/输出格式和采样率
                  "audio": {
                    "input": {"format": {"type": "pcm", "sample_rate": 16000}},
                    "output": {"format": {"type": "pcm", "sample_rate": 24000}}
                  },
                  "instructions": "你是一个友好的AI助手。",
                  "turn_detection": {"type": "server_vad", "threshold": 0.5, "silence_duration_ms": 800},
                  "max_tokens": 16384,
                  "temperature": 0.9,
                },
              }

            # 处理服务端推送的 DataChannel 事件
            @pc.on("datachannel")
            def on_datachannel(ch):
              nonlocal remote_dc, got_first_txt_msg
              print(f"[DC] 收到服务端 DataChannel: {ch.label}")
              if ch.label == "txt":
                remote_dc = ch

              @ch.on("message")
              def on_msg(msg):
                nonlocal got_first_txt_msg
                try:
                  evt = json.loads(msg)
                except Exception:
                  return
                print(f"[{ch.label}] {evt.get('type')}")

                # 用户开始说话时清空播放缓存，实现语音打断
                if isinstance(evt, dict) and evt.get("type") == "input_audio_buffer.speech_started":
                  speaker.clear()
                  print("[播放] 检测到用户说话，清空播放缓存（打断）")

                # 收到 txt 通道首条消息后发送 session.update 配置会话
                if ch.label == "txt" and not got_first_txt_msg:
                  got_first_txt_msg = True
                  if remote_dc and remote_dc.readyState == "open":
                    remote_dc.send(json.dumps(make_session_update(), ensure_ascii=False))
                    print("[DC] 已发送 session.update")

            # 接收服务端音频并通过播放器低延迟输出
            @pc.on("track")
            async def on_track(track):
              if track.kind == "audio":
                async def _play():
                  try:
                    while True:
                      frame = await track.recv()
                      await speaker.push_frame(frame)
                  except Exception:
                    pass
                asyncio.create_task(_play())

            @pc.on("iceconnectionstatechange")
            def on_ice():
              print(f"[ICE] {pc.iceConnectionState}")

            @pc.on("connectionstatechange")
            async def on_conn():
              print(f"[连接] {pc.connectionState}")
              if pc.connectionState in ("failed", "closed", "disconnected"):
                await pc.close()

            # SDP 交换：创建 Offer 并 POST 到信令服务端，获取 Answer
            offer = await pc.createOffer()
            await pc.setLocalDescription(offer)

            async with aiohttp.ClientSession() as session:
              async with session.post(
                SIGNALING_URL,
                ssl=ssl.create_default_context(cafile=certifi.where()),
                data=offer.sdp.encode("utf-8"),
                headers={
                  "Content-Type": "application/sdp",
                  "Authorization": f"Bearer {API_KEY}",
                },
                timeout=aiohttp.ClientTimeout(total=10),
              ) as resp:
                if not resp.ok:
                  raise Exception(f"SDP 交换失败: {resp.status} {await resp.text()}")
                answer_sdp = await resp.text()

            await pc.setRemoteDescription(RTCSessionDescription(sdp=answer_sdp, type="answer"))
            print("SDP 交换完成，等待连接...")

            try:
              await asyncio.Event().wait()
            except (KeyboardInterrupt, asyncio.CancelledError):
              pass
            finally:
              print(f"\n退出。最终状态: 连接={pc.connectionState}, ICE={pc.iceConnectionState}")
              await speaker.close()
              try:
                if mic and mic.audio:
                  mic.audio.stop()
              except Exception:
                pass
              await pc.close()

          asyncio.run(main())
          ```
        </Accordion>

        运行 `webrtc_demo.py`，通过麦克风即可与 Qwen-Omni-Realtime 模型实时对话，系统会检测您的音频起始位置并自动发送到服务器，无需您手动发送。
      </Tab>

      <Tab title="JavaScript">
        **前提条件**

        - 使用支持 WebRTC 的现代浏览器（Chrome、Edge、Firefox、Safari 等）。
        - 浏览器需要麦克风权限。
        - 浏览器无法直接向服务端发起建立连接的请求（受浏览器跨域安全策略限制），因此需要通过终端执行 curl 命令来完成连接建立。

        **运行示例**

        新建一个 HTML 文件，命名为 `webrtc_demo.html`，并将以下代码复制到文件中：

        <Accordion title="webrtc_demo.html">
          ```html
          <!DOCTYPE html>
          <html lang="zh-CN">
          <head>
            <meta charset="UTF-8" />
            <title>WebRTC Realtime 语音对话</title>
            <style>
              * { box-sizing: border-box; margin: 0; padding: 0; }
              body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; background: #f5f7fa; color: #1d2129; padding: 24px; line-height: 1.6; }

              .container { max-width: 800px; margin: 0 auto; }

              h1 { font-size: 22px; font-weight: 600; margin-bottom: 20px; color: #1d2129; }

              /* 顶部吸顶栏 */
              .sticky-top { position: sticky; top: 0; z-index: 100; background: #f5f7fa; margin: 0 -24px 16px; padding: 12px 24px; border-bottom: 1px solid transparent; transition: border-color .2s; }
              .sticky-top.scrolled { border-bottom-color: #e5e6eb; }

              /* 控制栏 */
              .toolbar { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin-bottom: 12px; }
              .toolbar label { display: flex; align-items: center; gap: 6px; font-size: 13px; color: #4e5969; cursor: pointer; }

              /* 按钮 */
              button { padding: 8px 18px; font-size: 13px; font-weight: 500; border: 1px solid #c9cdd4; border-radius: 6px; background: #fff; color: #1d2129; cursor: pointer; transition: all .15s; }
              button:hover:not(:disabled) { border-color: #165dff; color: #165dff; }
              button:disabled { opacity: .4; cursor: not-allowed; }
              .btn-primary { background: #165dff; border-color: #165dff; color: #fff; }
              .btn-primary:hover:not(:disabled) { background: #4080ff; border-color: #4080ff; color: #fff; }
              .btn-danger { border-color: #f53f3f; color: #f53f3f; }
              .btn-danger:hover:not(:disabled) { background: #f53f3f; color: #fff; }

              /* 状态指示 */
              .status-bar { display: flex; align-items: center; gap: 8px; padding: 10px 14px; border-radius: 8px; background: #fff; border: 1px solid #e5e6eb; font-size: 13px; }
              .status-dot { width: 8px; height: 8px; border-radius: 50%; background: #c9cdd4; flex-shrink: 0; }
              .status-dot.connected { background: #00b42a; }
              .status-dot.connecting { background: #ff7d00; animation: pulse 1s infinite; }
              .status-dot.error { background: #f53f3f; }
              @keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: .4; } }

              /* SDP 卡片 */
              .card { background: #fff; border: 1px solid #e5e6eb; border-radius: 10px; padding: 16px; margin-bottom: 16px; }
              .card-title { font-size: 13px; font-weight: 600; color: #4e5969; margin-bottom: 8px; }
              .step-num { display: inline-flex; align-items: center; justify-content: center; width: 20px; height: 20px; border-radius: 50%; background: #165dff; color: #fff; font-size: 11px; font-weight: 600; margin-right: 6px; }
              .card-hint { font-size: 12px; color: #86909c; margin-top: 6px; }

              textarea { width: 100%; font-family: "SF Mono", "Fira Code", "Fira Mono", Menlo, Consolas, monospace; font-size: 12px; padding: 10px; border: 1px solid #e5e6eb; border-radius: 6px; resize: vertical; background: #f7f8fa; color: #1d2129; transition: border-color .15s; }
              textarea:focus { outline: none; border-color: #165dff; background: #fff; }

              /* 视频 */
              .video-section { margin-bottom: 16px; }
              .video-label { font-size: 13px; color: #86909c; margin-bottom: 6px; }
              video { width: 320px; max-width: 100%; background: #000; border-radius: 8px; display: block; }

              /* 事件面板 */
              .events-title { font-size: 14px; font-weight: 600; color: #1d2129; margin-bottom: 10px; }
              .events-container { display: flex; flex-direction: column; gap: 6px; }
              .event-item { background: #fff; border: 1px solid #e5e6eb; border-radius: 8px; overflow: hidden; }
              .event-header { display: flex; align-items: center; gap: 8px; padding: 8px 12px; cursor: pointer; user-select: none; font-size: 12px; }
              .event-header:hover { background: #f7f8fa; }
              .event-arrow { font-size: 14px; font-weight: 700; width: 18px; text-align: center; }
              .event-arrow.server { color: #00b42a; }
              .event-arrow.client { color: #165dff; }
              .event-label { color: #4e5969; }
              .event-time { color: #c9cdd4; margin-left: auto; font-size: 11px; }
              .event-body { display: none; padding: 10px 12px; background: #f7f8fa; border-top: 1px solid #e5e6eb; }
              .event-body pre { margin: 0; font-size: 11px; font-family: "SF Mono", Menlo, Consolas, monospace; color: #4e5969; white-space: pre-wrap; word-break: break-all; }
              .events-empty { font-size: 13px; color: #c9cdd4; padding: 16px 0; text-align: center; }
            </style>
          </head>
          <body>
          <div class="container">
            <h1>WebRTC Realtime 语音对话</h1>

            <div class="sticky-top">
              <div class="toolbar">
                <button id="startBtn" class="btn-primary">开始会话</button>
                <button id="setAnswerBtn" disabled>设置 Answer</button>
                <button id="endBtn" class="btn-danger" disabled>结束会话</button>
                <button id="downloadBtn" disabled>下载远端音频</button>
                <label>
                  <input id="sendVideoCheckbox" type="checkbox" />
                  开启视频
                </label>
              </div>

              <div class="status-bar">
                <span class="status-dot" id="statusDot"></span>
                <span id="statusText">就绪</span>
              </div>
            </div>

            <div class="card">
              <div class="card-title"><span class="step-num">1</span>Offer SDP</div>
              <div style="margin-bottom: 8px;">
                <button id="copyOfferBtn" disabled>复制 Offer SDP</button>
              </div>
              <textarea id="offerBox" rows="6" readonly placeholder="点击"开始会话"后自动生成"></textarea>
              <div class="card-hint">ICE 收集完成后自动生成，复制后通过 curl 命令发送到服务端获取 Answer</div>
            </div>

            <div class="card">
              <div class="card-title"><span class="step-num">2</span>curl 命令</div>
              <div style="margin-bottom: 8px;">
                <button id="copyCurlBtn" disabled>复制 curl 命令</button>
              </div>
              <textarea id="curlBox" rows="6" readonly placeholder="Offer SDP 生成后自动填充 curl 命令"></textarea>
              <div class="card-hint">复制此命令到终端执行，将返回的 Answer SDP 粘贴到下方</div>
            </div>

            <div class="card">
              <div class="card-title"><span class="step-num">3</span>Answer SDP</div>
              <textarea id="answerBox" rows="6" placeholder="将 curl 返回的 Answer SDP 粘贴到这里"></textarea>
              <div class="card-hint">粘贴后点击上方"设置 Answer"按钮建立连接</div>
            </div>

            <div class="video-section" id="videoSection" style="display:none;">
              <div class="video-label">本端视频预览</div>
              <video id="localVideo" autoplay playsinline muted></video>
            </div>

            <div class="events-title">事件（DataChannel）</div>
            <div id="events" class="events-container"></div>
          </div>

          <script>
            const eventsDiv = document.getElementById('events');
            const startBtn = document.getElementById('startBtn');
            const setAnswerBtn = document.getElementById('setAnswerBtn');
            const endBtn = document.getElementById('endBtn');
            const downloadBtn = document.getElementById('downloadBtn');
            const copyOfferBtn = document.getElementById('copyOfferBtn');
            const statusDot = document.getElementById('statusDot');
            const statusText = document.getElementById('statusText');

            const copyCurlBtn = document.getElementById('copyCurlBtn');
            const curlBox = document.getElementById('curlBox');

            const sendVideoCheckbox = document.getElementById('sendVideoCheckbox');
            const localVideo = document.getElementById('localVideo');

            const offerBox = document.getElementById('offerBox');
            const answerBox = document.getElementById('answerBox');

            let pc = null;
            let hiddenRemoteAudioEl = null;

            let mediaRecorder = null;
            let recordedChunks = [];
            let audioBlob = null;

            let localStream = null;

            let sendCanvas = null;
            let sendCanvasCtx = null;
            let sendCanvasStream = null;
            let sendRafId = 0;

            let gatedAudioTracks = [];
            let gatedVideoTracks = [];
            let audioSender = null;
            let videoSender = null;
            let audioTrack = null;
            let videoTrack = null;

            function setStatus(text, state) {
             statusText.textContent = text;
             statusDot.className = 'status-dot' + (state ? ' ' + state : '');
            }

            function gateMedia(on) {
             for (const t of gatedAudioTracks) t.enabled = !!on;
             for (const t of gatedVideoTracks) t.enabled = !!on;
            }

            function sendUpdate(channel) {
             const update = {
              event_id: `event_${Date.now()}`,
              type: "session.update",
              session: {
               // 配置音频输入/输出格式和采样率
               audio: {
                input: { format: { type: "pcm", sample_rate: 16000 } },
                output: { format: { type: "pcm", sample_rate: 24000 } }
               },
               input_audio_transcription: { model: "qwen3-asr-flash-realtime" },
               instructions: "You are a helpful assistant.",
               modalities: ["text", "audio"],
               smooth_output: false,
               turn_detection: {
                prefix_padding_ms: 500,
                silence_duration_ms: 800,
                threshold: 0.5,
                type: "server_vad",
               },
              },
             };
             if (channel && channel.readyState === "open") channel.send(JSON.stringify(update));
            }

            // ===== 事件面板 =====
            const events = [];
            function nowTs() { return new Date().toLocaleTimeString(); }

            function renderEvents() {
             eventsDiv.innerHTML = "";
             if (events.length === 0) {
              const empty = document.createElement("div");
              empty.className = "events-empty";
              empty.textContent = "等待事件...";
              eventsDiv.appendChild(empty);
              return;
             }

             for (const item of events) {
              const { event, timestamp } = item;
              const isClient = event?.type?.includes("update") || event?.type?.includes("create");

              const wrap = document.createElement("div");
              wrap.className = "event-item";

              const header = document.createElement("div");
              header.className = "event-header";

              const arrow = document.createElement("span");
              arrow.className = "event-arrow " + (isClient ? "client" : "server");
              arrow.textContent = isClient ? "↓" : "↑";

              const label = document.createElement("span");
              label.className = "event-label";
              const who = isClient ? "client" : "server";
              const type = event?.type ?? "message";
              label.textContent = `${who}: ${type}`;

              const time = document.createElement("span");
              time.className = "event-time";
              time.textContent = timestamp;

              const body = document.createElement("div");
              body.className = "event-body";
              const pre = document.createElement("pre");
              pre.textContent = JSON.stringify(event, null, 2);
              body.appendChild(pre);

              header.onclick = () => { body.style.display = body.style.display === "block" ? "none" : "block"; };

              header.appendChild(arrow);
              header.appendChild(label);
              header.appendChild(time);
              wrap.appendChild(header);
              wrap.appendChild(body);

              eventsDiv.appendChild(wrap);
             }
            }

            function clearUIEvents() { events.length = 0; renderEvents(); }
            function pushEventFromDataChannel(eventObj) {
             const ts = eventObj.timestamp || nowTs();
             if (!eventObj.timestamp) eventObj.timestamp = ts;
             events.unshift({ event: eventObj, timestamp: ts });
             renderEvents();
            }

            function normalizeSdpForSetRemote(sdp) {
             sdp = String(sdp).trim().replace(/\r?\n/g, "\r\n");
             if (!sdp.endsWith("\r\n")) sdp += "\r\n";
             return sdp;
            }

            // ===== WebRTC =====
            startBtn.onclick = () => startSession().catch(err => console.log("startSession error:", err));
            endBtn.onclick = () => endSession();
            setAnswerBtn.onclick = () => setRemoteAnswerFromUI().catch(err => console.log("setRemoteAnswer error:", err));
            copyOfferBtn.onclick = async () => {
             const txt = offerBox.value;
             if (!txt) return;
             await navigator.clipboard.writeText(txt);
             alert("Offer SDP 已复制");
            };
            copyCurlBtn.onclick = async () => {
             const txt = curlBox.value;
             if (!txt) return;
             await navigator.clipboard.writeText(txt);
             alert("curl 命令已复制，请在终端执行");
            };
            downloadBtn.onclick = () => {
             if (audioBlob) downloadBlob(audioBlob, 'remote-audio.webm');
             else alert('没有可下载的录音数据');
            };

            async function startSession() {
             if (pc) return;

             pc = new RTCPeerConnection({ iceServers: [] });
             clearUIEvents();
             setStatus('正在获取麦克风权限...', 'connecting');

             offerBox.value = "";
             answerBox.value = "";
             curlBox.value = "";
             setAnswerBtn.disabled = true;
             copyOfferBtn.disabled = true;
             copyCurlBtn.disabled = true;

             endBtn.disabled = false;
             downloadBtn.disabled = true;

             pc.onconnectionstatechange = () => {
              if (!pc) return;
              if (pc.connectionState === 'connected') {
               setStatus('已连接，请说话', 'connected');
              } else if (["failed", "closed", "disconnected"].includes(pc.connectionState)) {
               console.log("onconnectionstatechange:", pc.connectionState);
               endSession(true);
              }
             };

             pc.ontrack = async (e) => {
              const stream = e.streams[0];
              ensureHiddenAudioEl();
              hiddenRemoteAudioEl.srcObject = stream;
              try { await hiddenRemoteAudioEl.play(); } catch {}
              startRecordingRemoteStream(stream);
             };

             const wantVideo = !!sendVideoCheckbox.checked;

             const localPreviewFps = 30;
             const sendFps = 2;

             const constraints = wantVideo
              ? {
                audio: true,
                video: {
                 facingMode: { ideal: "user" },
                 frameRate: { ideal: localPreviewFps, max: localPreviewFps },
                 width: { ideal: 640 },
                 height: { ideal: 480 },
                }
               }
              : { audio: true };

             localStream = await navigator.mediaDevices.getUserMedia(constraints);

             const videoSection = document.getElementById('videoSection');
             if (wantVideo) {
              localVideo.srcObject = localStream;
              localVideo.style.display = "block";
              videoSection.style.display = "";
              try { await localVideo.play(); } catch {}
             } else {
              localVideo.srcObject = null;
              localVideo.style.display = "none";
              videoSection.style.display = "none";
             }

             gatedAudioTracks = [];
             gatedVideoTracks = [];

             localStream.getAudioTracks().forEach(t => {
              pc.addTrack(t, localStream);
              gatedAudioTracks.push(t);
             });

             if (wantVideo) {
              if (sendRafId) cancelAnimationFrame(sendRafId);
              sendRafId = 0;
              if (sendCanvasStream) sendCanvasStream.getTracks().forEach(t => t.stop());
              sendCanvasStream = null;
              sendCanvasCtx = null;
              sendCanvas = null;

              const settings = localStream.getVideoTracks()[0].getSettings();
              sendCanvas = document.createElement("canvas");
              sendCanvas.width = settings.width || 640;
              sendCanvas.height = settings.height || 480;
              sendCanvasCtx = sendCanvas.getContext("2d", { alpha: false });

              sendCanvasStream = sendCanvas.captureStream(sendFps);
              const lowFpsTrack = sendCanvasStream.getVideoTracks()[0];
              pc.addTrack(lowFpsTrack, sendCanvasStream);
              gatedVideoTracks.push(lowFpsTrack);

              const pump = () => {
               if (!sendCanvasCtx || !sendCanvas) return;
               try { sendCanvasCtx.drawImage(localVideo, 0, 0, sendCanvas.width, sendCanvas.height); } catch {}
               sendRafId = requestAnimationFrame(pump);
              };
              sendRafId = requestAnimationFrame(pump);
             }

             gateMedia(false);

             audioSender = pc.getSenders().find(s => s.track?.kind === 'audio');
             videoSender = pc.getSenders().find(s => s.track?.kind === 'video');
             audioTrack = audioSender?.track;
             videoTrack = videoSender?.track;

             await audioSender?.replaceTrack(null);
             await videoSender?.replaceTrack(videoTrack ? null : undefined);

             const dc = pc.createDataChannel('oai-events');

             dc.onopen = () => console.log("DC open");
             dc.onmessage = (e) => {
              handleDcMessage(e.data, dc);
             };

             pc.ondatachannel = (event) => {
              const ch = event.channel;
              ch.onmessage = (e) => {
                handleDcMessage(e.data, ch);
              };
             };

             function handleDcMessage(data, channel) {
               let obj;
               try { obj = JSON.parse(data); }
               catch (err) {
                pushEventFromDataChannel({ type: "raw", data: String(data), parseError: String(err) });
                return;
               }
               pushEventFromDataChannel(obj);

               if (obj?.type === "session.created") {
                console.log("Session created, opening media gate.");
                gateMedia(true);
                if(audioSender) audioSender.replaceTrack(audioTrack);
                if(videoSender && videoTrack) videoSender.replaceTrack(videoTrack);

                sendUpdate(channel);
               }
             }

             pc.onicegatheringstatechange = () => {
              if (!pc) return;
              if (pc.iceGatheringState === "complete" && pc.localDescription?.sdp) {
               const sdp = pc.localDescription.sdp;
               offerBox.value = sdp;
               copyOfferBtn.disabled = false;
               setAnswerBtn.disabled = false;

               const escapedSdp = sdp.replace(/'/g, "'\\''");
               curlBox.value = `curl -X POST 'https://{endpoint}/api/v1/webrtc/realtime?model=qwen3.5-omni-plus-realtime' \\\n  -H 'Content-Type: application/sdp' \\\n  -H 'Authorization: Bearer $DASHSCOPE_API_KEY' \\\n  --data-binary '${escapedSdp}'`;
               copyCurlBtn.disabled = false;

               setStatus('Offer SDP 已生成，复制 curl 命令到终端获取 Answer SDP', 'connecting');
               console.log("ICE Gathering Complete. Ready to set remote description.");
              }
             };

             const offer = await pc.createOffer();
             await pc.setLocalDescription(offer);
            }

            async function setRemoteAnswerFromUI() {
             if (!pc) return alert('请先点击"开始会话"生成 Offer。');
             const txt = answerBox.value.trim();
             if (!txt) return alert("请粘贴 Answer SDP");

             const answerSdp = normalizeSdpForSetRemote(txt);
             try {
               await pc.setRemoteDescription({ type: 'answer', sdp: answerSdp });
               setStatus('正在建立连接...', 'connecting');
             } catch (e) {
               alert("设置 Answer 失败: " + e.message);
               console.error(e);
             }
            }

            function endSession(silent = false) {
             if (sendRafId) cancelAnimationFrame(sendRafId);
             sendRafId = 0;

             if (sendCanvasStream) {
              sendCanvasStream.getTracks().forEach(t => t.stop());
             }
             sendCanvasStream = null;
             sendCanvasCtx = null;
             sendCanvas = null;

             try { if (mediaRecorder && mediaRecorder.state !== "inactive") mediaRecorder.stop(); } catch {}
             mediaRecorder = null;

             if (localStream) {
              localStream.getTracks().forEach(t => t.stop());
              localStream = null;
             }
             localVideo.srcObject = null;
             localVideo.style.display = "none";
             document.getElementById('videoSection').style.display = "none";

             if (pc) {
              try { pc.close(); } catch {}
              pc = null;
             }

             gatedAudioTracks = [];
             gatedVideoTracks = [];

             if (hiddenRemoteAudioEl) {
              try { hiddenRemoteAudioEl.pause(); } catch {}
              hiddenRemoteAudioEl.srcObject = null;
              hiddenRemoteAudioEl.remove();
              hiddenRemoteAudioEl = null;
             }

             endBtn.disabled = true;
             setAnswerBtn.disabled = true;
             copyOfferBtn.disabled = true;
             copyCurlBtn.disabled = true;
             downloadBtn.disabled = !audioBlob;

             setStatus('已断开', '');
             if (!silent) console.log("session ended");
            }

            function ensureHiddenAudioEl() {
             if (hiddenRemoteAudioEl) return;
             hiddenRemoteAudioEl = document.createElement("audio");
             hiddenRemoteAudioEl.autoplay = true;
             hiddenRemoteAudioEl.playsInline = true;
             hiddenRemoteAudioEl.muted = false;
             hiddenRemoteAudioEl.style.display = "none";
             document.body.appendChild(hiddenRemoteAudioEl);
            }

            function startRecordingRemoteStream(remoteStream) {
             const audioTracks = remoteStream.getAudioTracks();
             if (!audioTracks.length) return;

             const audioStream = new MediaStream(audioTracks);
             recordedChunks = [];
             audioBlob = null;
             downloadBtn.disabled = true;

             try {
              mediaRecorder = new MediaRecorder(audioStream, { mimeType: 'audio/webm' });
             } catch (err) {
              console.log("MediaRecorder create failed:", err);
              return;
             }

             mediaRecorder.ondataavailable = (e) => {
              if (e.data && e.data.size > 0) recordedChunks.push(e.data);
             };

             mediaRecorder.onstop = () => {
              audioBlob = new Blob(recordedChunks, { type: 'audio/webm' });
              downloadBtn.disabled = !audioBlob || audioBlob.size === 0;
             };

             mediaRecorder.start();
            }

            function downloadBlob(blob, filename) {
             const url = URL.createObjectURL(blob);
             const a = document.createElement('a');
             a.style.display = 'none';
             a.href = url;
             a.download = filename;
             document.body.appendChild(a);
             a.click();
             URL.revokeObjectURL(url);
             a.remove();
            }

            renderEvents();

            const stickyTop = document.querySelector('.sticky-top');
            window.addEventListener('scroll', () => {
             stickyTop.classList.toggle('scrolled', window.scrollY > 10);
            }, { passive: true });
          </script>
          </body>
          </html>
          ```
        </Accordion>

        在浏览器中打开此文件，按以下步骤操作：

        1. 点击**开始会话**，页面会自动生成 Offer SDP 和对应的 curl 命令。
        2. 点击**复制 curl 命令**，在终端中执行。命令返回的内容即为 Answer SDP。
        3. 将 Answer SDP 粘贴到页面的 **Answer SDP** 文本框中，点击**设置 Answer**即可建立连接并开始语音对话。
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

## 交互流程

<Tabs>
  <Tab title="VAD 模式">
    在 [session.update](/api-reference/real-time-multimodal/client-events) 事件中将 `session.turn_detection.type` 设为 `"server_vad"` 或 `"semantic_vad"` 即可启用 VAD 模式。适用于语音通话场景。WebSocket 和 WebRTC 均支持 VAD 模式，两者的服务端事件一致，区别在于音频和图片的传输方式不同。

    <Note>
      WebRTC 仅支持 VAD 模式，不支持 Manual 模式。WebRTC 的音频通过 RTP 直接传输，无需发送 `input_audio_buffer.append` 事件；图片通过视频轨道传输，不支持 `input_image_buffer.append` 事件。控制指令和服务端事件通过 DataChannel 传输，事件类型与 WebSocket 一致。
    </Note>

    交互流程如下：

    1. 客户端发送音频数据。WebSocket 通过 [input\_audio\_buffer.append](/api-reference/real-time-multimodal/client-events) 事件发送；WebRTC 通过音频轨道（RTP）自动传输，无需手动发送事件。
    2. 服务端检测到语音开始，通过 DataChannel（WebRTC）或 WebSocket 发送 [input\_audio\_buffer.speech\_started](/api-reference/real-time-multimodal/server-events) 事件。
    3. 服务端检测到语音结束，发送 [input\_audio\_buffer.speech\_stopped](/api-reference/real-time-multimodal/server-events) 事件。
    4. 服务端自动提交音频缓冲区，发送 [input\_audio\_buffer.committed](/api-reference/real-time-multimodal/server-events) 事件。
    5. 服务端开始生成响应，依次发送 [response.created](/api-reference/real-time-multimodal/server-events)、[conversation.item.created](/api-reference/real-time-multimodal/server-events) 等事件。模型的音频回复通过 WebSocket 的 [response.audio.delta](/api-reference/real-time-multimodal/server-events) 事件增量返回，或通过 WebRTC 的音频轨道（RTP）直接传输。
    6. 响应过程中，服务端通过 [response.audio\_transcript.delta](/api-reference/real-time-multimodal/server-events) 事件增量返回文字转录，最终发送 [response.done](/api-reference/real-time-multimodal/server-events) 事件标志响应完成。

| 生命周期    | 客户端事件                                                                                                                                                                                                                                             | 服务端事件                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 会话初始化   | [session.update](/api-reference/real-time-multimodal/client-events) - 会话配置                                                                                                                                                                        | [session.created](/api-reference/real-time-multimodal/server-events) - 会话已创建。[session.updated](/api-reference/real-time-multimodal/server-events) - 会话配置已更新                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 用户音频输入  | WebSocket：[input\_audio\_buffer.append](/api-reference/real-time-multimodal/client-events) - 将音频追加到缓冲区。[input\_image\_buffer.append](/api-reference/real-time-multimodal/client-events) - 将图像追加到缓冲区。WebRTC：音频通过 RTP 音频轨道自动传输，图片通过视频轨道传输，无需发送上述事件。 | [input\_audio\_buffer.speech\_started](/api-reference/real-time-multimodal/server-events) - 检测到语音开始。[input\_audio\_buffer.speech\_stopped](/api-reference/real-time-multimodal/server-events) - 检测到语音结束。[input\_audio\_buffer.committed](/api-reference/real-time-multimodal/server-events) - 服务端已收到提交的音频                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 服务端音频输出 | 无                                                                                                                                                                                                                                                 | [response.created](/api-reference/real-time-multimodal/server-events) - 服务端开始生成响应。[conversation.item.created](/api-reference/real-time-multimodal/server-events) - 对话项已创建。[response.audio\_transcript.delta](/api-reference/real-time-multimodal/server-events) - 增量生成的转写文本。WebSocket：[response.audio.delta](/api-reference/real-time-multimodal/server-events) - 模型增量生成的音频。WebRTC：音频通过 RTP 音频轨道直接传输，不返回此事件。[response.audio\_transcript.done](/api-reference/real-time-multimodal/server-events) - 文本转写完成。[response.audio.done](/api-reference/real-time-multimodal/server-events) - 音频生成完成。[response.done](/api-reference/real-time-multimodal/server-events) - 响应完成。`conversation.item.input_audio_transcription.delta` - 用户语音输入的文字流式转录（需在 session.update 中启用 input\_audio\_transcription）。`conversation.item.input_audio_transcription.completed` - 用户语音输入的文字转录完成（需在 session.update 中启用 input\_audio\_transcription） |
  </Tab>

  <Tab title="手动模式">
    在 [session.update](/api-reference/real-time-multimodal/client-events) 事件中将 `session.turn_detection` 设为 `null` 即可启用手动模式。在此模式下，客户端通过显式发送 `input_audio_buffer.commit` 和 `response.create` 事件来请求服务端响应。该模式适用于按键说话场景，如聊天应用中的语音消息。

    交互流程如下：

    1. 客户端可随时发送 [input\_audio\_buffer.append](/api-reference/real-time-multimodal/client-events) 和 [input\_image\_buffer.append](/api-reference/real-time-multimodal/client-events) 事件，将音频和图像数据追加到缓冲区。
       <Info>在发送 input\_image\_buffer.append 事件之前，需至少发送一次 input\_audio\_buffer.append 事件。</Info>
    2. 客户端发送 [input\_audio\_buffer.commit](/api-reference/real-time-multimodal/client-events) 事件，提交音频和图像缓冲区。这告知服务端当前轮次的所有用户输入（包括音频和图像）已发送完毕。
    3. 服务端返回 [input\_audio\_buffer.committed](/api-reference/real-time-multimodal/server-events) 事件。
    4. 客户端发送 [response.create](/api-reference/real-time-multimodal/client-events) 事件，等待服务端的模型输出。
    5. 服务端返回 [conversation.item.created](/api-reference/real-time-multimodal/server-events) 事件。

| 生命周期    | 客户端事件                                                                                                                                                                                                                                                                                                                                                                  | 服务端事件                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 会话初始化   | [session.update](/api-reference/real-time-multimodal/client-events) - 会话配置                                                                                                                                                                                                                                                                                             | [session.created](/api-reference/real-time-multimodal/server-events) - 会话创建。[session.updated](/api-reference/real-time-multimodal/server-events) - 会话配置已更新                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 用户音频输入  | [input\_audio\_buffer.append](/api-reference/real-time-multimodal/client-events) - 将音频追加到缓冲区。[input\_image\_buffer.append](/api-reference/real-time-multimodal/client-events) - 将图像追加到缓冲区。[input\_audio\_buffer.commit](/api-reference/real-time-multimodal/client-events) - 向服务端提交音频和图像。[response.create](/api-reference/real-time-multimodal/client-events) - 创建模型响应 | [input\_audio\_buffer.committed](/api-reference/real-time-multimodal/server-events) - 服务端已收到提交的音频                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 服务端音频输出 | [input\_audio\_buffer.clear](/api-reference/real-time-multimodal/client-events) - 清空音频缓冲区中的音频                                                                                                                                                                                                                                                                          | [response.created](/api-reference/real-time-multimodal/server-events) - 服务端开始生成响应。[response.output\_item.added](/api-reference/real-time-multimodal/server-events) - 响应期间新增输出内容。[conversation.item.created](/api-reference/real-time-multimodal/server-events) - 对话项已创建。[response.content\_part.added](/api-reference/real-time-multimodal/server-events) - 助手消息项中新增输出内容。[response.audio\_transcript.delta](/api-reference/real-time-multimodal/server-events) - 增量生成的转写文本。[response.audio.delta](/api-reference/real-time-multimodal/server-events) - 模型增量生成的音频。[response.audio\_transcript.done](/api-reference/real-time-multimodal/server-events) - 文本转写完成。[response.audio.done](/api-reference/real-time-multimodal/server-events) - 音频生成完成。[response.content\_part.done](/api-reference/real-time-multimodal/server-events) - 助手消息的文本或音频流式输出完成。[response.output\_item.done](/api-reference/real-time-multimodal/server-events) - 助手消息的整个输出项流式传输完成。[response.done](/api-reference/real-time-multimodal/server-events) - 响应完成 |
  </Tab>
</Tabs>

## 联网搜索

联网搜索功能允许模型使用实时检索到的信息进行回复，适用于需要最新信息的场景，如股票价格、天气预报等。模型会自主决定是否进行联网搜索。

<Info>
  仅 `Qwen3.5-Omni-Plus-Realtime` 模型支持联网搜索。默认情况下该功能处于关闭状态，需要通过 `session.update` 事件开启。

  有关计费详情，请参阅[计费说明](/developer-guides/getting-started/pricing)中 `agent` 策略的说明。
</Info>

### 如何开启

在 `session.update` 事件中，增加以下参数：

- `enable_search`：设为 `true` 以开启联网搜索。
- `search_options.enable_source`：设为 `true` 以返回搜索结果来源列表。

完整参数说明请参阅 [session.update](/api-reference/real-time-multimodal/client-events)。

### 响应格式

开启联网搜索后，`response.done` 事件的 `usage` 对象中新增 `plugins` 字段，用于记录搜索使用量：

```json
{
  "usage": {
    "total_tokens": 2937,
    "input_tokens": 2554,
    "output_tokens": 383,
    "input_tokens_details": {
      "text_tokens": 2512,
      "audio_tokens": 42
    },
    "output_tokens_details": {
      "text_tokens": 90,
      "audio_tokens": 293
    },
    "plugins": {
      "search": {
        "count": 1,
        "strategy": "agent"
      }
    }
  }
}
```

### 代码示例

以下示例展示如何开启联网搜索功能。

<Tabs>
  <Tab title="DashScope Python SDK">
    在 `update_session` 调用中传入 `enable_search` 和 `search_options` 参数：

    ```python
    import os
    import base64
    import time
    import json
    import pyaudio
    from dashscope.audio.qwen_omni import MultiModality, AudioFormat, OmniRealtimeCallback, OmniRealtimeConversation
    import dashscope

    dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')
    url = 'wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
    model = 'qwen3.5-omni-plus-realtime'
    voice = 'Tina'

    class SearchCallback(OmniRealtimeCallback):
      def __init__(self, pya):
        self.pya = pya
        self.out = None
      def on_open(self):
        self.out = self.pya.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)
      def on_event(self, response):
        if response['type'] == 'response.audio.delta':
          self.out.write(base64.b64decode(response['delta']))
        elif response['type'] == 'conversation.item.input_audio_transcription.delta':
          preview = response.get('text', '') + response.get('stash', '')
          print(f"\r[用户] {preview}", end='', flush=True)
        elif response['type'] == 'conversation.item.input_audio_transcription.completed':
          print(f"\r[用户] {response['transcript']}")
        elif response['type'] == 'response.audio_transcript.done':
          print(f"[模型] {response['transcript']}")
        elif response['type'] == 'response.done':
          usage = response.get('response', {}).get('usage', {})
          plugins = usage.get('plugins', {})
          if plugins.get('search'):
            print(f"[搜索] count={plugins['search']['count']}, strategy={plugins['search']['strategy']}")

    pya = pyaudio.PyAudio()
    callback = SearchCallback(pya)
    conv = OmniRealtimeConversation(model=model, callback=callback, url=url)
    conv.connect()
    conv.update_session(
      output_modalities=[MultiModality.AUDIO, MultiModality.TEXT],
      voice=voice,
      instructions="你是小云，一个私人助手",
      enable_search=True,
      search_options={'enable_source': True}
    )
    mic = pya.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)
    print("联网搜索已开启。对着麦克风说话（按 Ctrl+C 退出）...")
    try:
      while True:
        audio_data = mic.read(3200, exception_on_overflow=False)
        conv.append_audio(base64.b64encode(audio_data).decode())
        time.sleep(0.01)
    except KeyboardInterrupt:
      conv.close()
      mic.close()
      callback.out.close()
      pya.terminate()
      print("\n对话已结束")
    ```
  </Tab>

  <Tab title="DashScope Java SDK">
    在 `updateSession` 中通过 `parameters` 映射传入联网搜索参数：

    ```java
    import com.alibaba.dashscope.audio.omni.*;
    import com.alibaba.dashscope.exception.NoApiKeyException;
    import com.google.gson.JsonObject;
    import javax.sound.sampled.*;
    import java.nio.ByteBuffer;
    import java.util.*;
    import java.util.concurrent.ConcurrentLinkedQueue;
    import java.util.concurrent.atomic.AtomicBoolean;

    public class OmniSearch {
      static class SequentialAudioPlayer {
        private final SourceDataLine line;
        private final Queue<byte[]> audioQueue = new ConcurrentLinkedQueue<>();
        private final Thread playerThread;
        private final AtomicBoolean shouldStop = new AtomicBoolean(false);

        public SequentialAudioPlayer() throws LineUnavailableException {
          AudioFormat format = new AudioFormat(24000, 16, 1, true, false);
          line = AudioSystem.getSourceDataLine(format);
          line.open(format);
          line.start();
          playerThread = new Thread(() -> {
            while (!shouldStop.get()) {
              byte[] audio = audioQueue.poll();
              if (audio != null) {
                line.write(audio, 0, audio.length);
              } else {
                try { Thread.sleep(10); } catch (InterruptedException ignored) {}
              }
            }
          }, "AudioPlayer");
          playerThread.start();
        }

        public void play(String base64Audio) {
          audioQueue.add(Base64.getDecoder().decode(base64Audio));
        }
        public void close() {
          shouldStop.set(true);
          try { playerThread.join(1000); } catch (InterruptedException ignored) {}
          line.drain();
          line.close();
        }
      }

      public static void main(String[] args) {
        try {
          SequentialAudioPlayer player = new SequentialAudioPlayer();
          AtomicBoolean shouldStop = new AtomicBoolean(false);

          OmniRealtimeParam param = OmniRealtimeParam.builder()
              .model("qwen3.5-omni-plus-realtime")
              .apikey(System.getenv("DASHSCOPE_API_KEY"))
              .url("wss://dashscope.aliyuncs.com/api-ws/v1/realtime")
              .build();

          OmniRealtimeConversation conversation = new OmniRealtimeConversation(param, new OmniRealtimeCallback() {
            @Override public void onOpen() {
              System.out.println("连接已建立");
            }
            @Override public void onClose(int code, String reason) {
              System.out.println("连接已关闭");
              shouldStop.set(true);
            }
            @Override public void onEvent(JsonObject event) {
              String type = event.get("type").getAsString();
              if ("response.audio.delta".equals(type)) {
                player.play(event.get("delta").getAsString());
              } else if ("response.audio_transcript.done".equals(type)) {
                System.out.println("[模型] " + event.get("transcript").getAsString());
              } else if ("response.done".equals(type)) {
                JsonObject response = event.getAsJsonObject("response");
                if (response != null && response.has("usage")) {
                  JsonObject usage = response.getAsJsonObject("usage");
                  if (usage.has("plugins")) {
                    JsonObject plugins = usage.getAsJsonObject("plugins");
                    if (plugins.has("search")) {
                      JsonObject search = plugins.getAsJsonObject("search");
                      System.out.println("[搜索] count=" + search.get("count").getAsInt()
                          + ", strategy=" + search.get("strategy").getAsString());
                    }
                  }
                }
              }
            }
          });

          conversation.connect();
          conversation.updateSession(OmniRealtimeConfig.builder()
              .modalities(Arrays.asList(OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT))
              .voice("Tina")
              .enableTurnDetection(true)
              .enableInputAudioTranscription(true)
              .parameters(Map.of(
                  "instructions", "你是小云，一个私人助手",
                  "enable_search", true,
                  "search_options", Map.of("enable_source", true)
              ))
              .build()
          );

          System.out.println("联网搜索已开启。开始说话（按 Ctrl+C 退出）...");
          AudioFormat format = new AudioFormat(16000, 16, 1, true, false);
          TargetDataLine mic = AudioSystem.getTargetDataLine(format);
          mic.open(format);
          mic.start();

          ByteBuffer buffer = ByteBuffer.allocate(3200);
          while (!shouldStop.get()) {
            int bytesRead = mic.read(buffer.array(), 0, buffer.capacity());
            if (bytesRead > 0) {
              conversation.appendAudio(Base64.getEncoder().encodeToString(buffer.array()));
            }
            Thread.sleep(20);
          }

          conversation.close(1000, "正常退出");
          player.close();
          mic.close();
        } catch (NoApiKeyException e) {
          System.err.println("未找到 API KEY：请设置 DASHSCOPE_API_KEY 环境变量。");
        } catch (Exception e) {
          e.printStackTrace();
        }
      }
    }
    ```
  </Tab>

  <Tab title="WebSocket（Python）">
    在 `session.update` 的 JSON 数据中增加 `enable_search` 和 `search_options` 字段：

    ```python
    import json
    import os
    import websocket
    import base64
    import pyaudio
    import threading

    API_KEY = os.getenv("DASHSCOPE_API_KEY")
    API_URL = "wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=qwen3.5-omni-plus-realtime"

    pya = pyaudio.PyAudio()
    out_stream = pya.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

    def on_open(ws):
      ws.send(json.dumps({
        "type": "session.update",
        "session": {
          "modalities": ["text", "audio"],
          "voice": "Tina",
          "instructions": "你是个人助理小云",
          # 配置音频输入/输出格式和采样率
          "audio": {
            "input": {"format": {"type": "pcm", "sample_rate": 16000}},
            "output": {"format": {"type": "pcm", "sample_rate": 24000}}
          },
          "enable_search": True,
          "search_options": {
            "enable_source": True
          }
        }
      }))
      print("联网搜索已开启。对着麦克风说话...")
      def send_audio():
        mic = pya.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)
        try:
          while True:
            audio = mic.read(3200, exception_on_overflow=False)
            ws.send(json.dumps({
              "type": "input_audio_buffer.append",
              "audio": base64.b64encode(audio).decode()
            }))
        except Exception:
          mic.close()
      threading.Thread(target=send_audio, daemon=True).start()

    def on_message(ws, message):
      event = json.loads(message)
      if event["type"] == "response.audio.delta":
        out_stream.write(base64.b64decode(event["delta"]))
      elif event["type"] == "response.audio_transcript.done":
        print(f"[模型] {event['transcript']}")
      elif event["type"] == "response.done":
        usage = event.get("response", {}).get("usage", {})
        plugins = usage.get("plugins", {})
        if plugins.get("search"):
          print(f"[搜索] count={plugins['search']['count']}, strategy={plugins['search']['strategy']}")

    def on_error(ws, error):
      print(f"错误: {error}")

    headers = ["Authorization: Bearer " + API_KEY]
    ws = websocket.WebSocketApp(API_URL, header=headers, on_open=on_open, on_message=on_message, on_error=on_error)
    ws.run_forever()
    ```
  </Tab>
</Tabs>

- [服务端事件](/api-reference/real-time-multimodal/server-events)

## 计费与限流

### 计费规则

Qwen-Omni-Realtime 按不同输入模态（如音频和图像）消耗的 Token 数量计费。有关计费的详细信息，请参阅[计费说明](/developer-guides/getting-started/pricing)。

<Note>
  在多轮实时对话中，模型每次生成响应时，需要将上下文窗口内的所有历史对话内容（包括之前各轮的音频、图片和文本）与本轮新增输入一并作为输入 Token 进行处理。因此，输入 Token 会随对话轮次的增加而逐轮累积，而非仅计算当前轮次的新增输入。

  例如，假设一段 10 秒的音频输入转换为 70 个 Token（Qwen3.5-Omni-Realtime 系列模型），在第 3 轮对话时，该音频仍在上下文窗口内，则它依然会被计入第 3 轮的输入 Token。实际计费的输入 Token 数 = 上下文窗口内所有历史轮次的内容 Token 数 + 本轮新增输入的 Token 数。
</Note>

<Accordion title="音频和图片 Token 换算规则">
  <Tabs>
    <Tab title="音频">
      - Qwen3.5-Omni-Realtime：输入音频总 Token 数 = 音频时长（秒）x 7；输出音频总 Token 数 = 音频时长（秒）x 12.5
      - Qwen3-Omni-Flash-Realtime：输入与输出音频的总 Token 数 = 音频时长（秒）x 12.5
      - Qwen-Omni-Turbo-Realtime：输入与输出音频的总 Token 数 = 音频时长（秒）x 25

      若音频时长不足 1 秒，按 1 秒计算。
    </Tab>

    <Tab title="图片">
      - `Qwen3.5-Omni-Plus-Realtime` 模型：每 `32x32` 像素消耗 1 Token
      - `Qwen3-Omni-Flash-Realtime` 系列模型：每 `32x32` 像素消耗 1 Token
      - `Qwen-Omni-Turbo-Realtime` 模型：每 `28x28` 像素消耗 1 Token

      单张图片最少消耗 4 个 Token，最多支持 1,280 个 Token。可使用以下代码估算图片消耗的总 Token 数：

      ```python
      # 安装 Pillow 库：pip install Pillow
      from PIL import Image
      import math

      # Qwen-Omni-Turbo-Realtime 模型的缩放因子为 28
      # factor = 28
      # Qwen3-Omni-Flash-Realtime 和 Qwen3.5-Omni-Realtime 系列模型的缩放因子为 32
      factor = 32

      def token_calculate(image_path='', duration=10):
        """
        :param image_path: 图片路径
        :param duration: 会话连接时长（秒）
        :return: 图片消耗的 Token 数
        """
        if len(image_path) > 0:
          # 打开指定的 PNG 图片文件
          image = Image.open(image_path)
          # 获取图片原始宽高
          height = image.height
          width = image.width
          print(f"缩放前图片尺寸: height={height}, width={width}")
          # 将高度调整为 factor 的整数倍
          h_bar = round(height / factor) * factor
          # 将宽度调整为 factor 的整数倍
          w_bar = round(width / factor) * factor
          # 图片 Token 下限：4 个 Token
          min_pixels = factor * factor * 4
          # 图片 Token 上限：1,280 个 Token
          max_pixels = 1280 * factor * factor
          # 缩放图片，确保总像素在 [min_pixels, max_pixels] 范围内
          if h_bar * w_bar > max_pixels:
            # 计算缩放比例 beta，使缩放后总像素不超过 max_pixels
            beta = math.sqrt((height * width) / max_pixels)
            # 重新计算调整后的高度，确保为 factor 的整数倍
            h_bar = math.floor(height / beta / factor) * factor
            # 重新计算调整后的宽度，确保为 factor 的整数倍
            w_bar = math.floor(width / beta / factor) * factor
          elif h_bar * w_bar < min_pixels:
            # 计算缩放比例 beta，使缩放后总像素不低于 min_pixels
            beta = math.sqrt(min_pixels / (height * width))
            # 重新计算调整后的高度，确保为 factor 的整数倍
            h_bar = math.ceil(height * beta / factor) * factor
            # 重新计算调整后的宽度，确保为 factor 的整数倍
            w_bar = math.ceil(width * beta / factor) * factor
          print(f"缩放后图片尺寸: height={h_bar}, width={w_bar}")
          # 计算图片 Token 数：总像素除以 (factor x factor)
          token = int((h_bar * w_bar) / (factor * factor))
          print(f"缩放后 Token 数: {token}")
          total_token = token * math.ceil(duration / 2)
          print(f"总 Token 数: {total_token}")
          return total_token
        else:
          print("错误：image_path 为空，无法计算 Token 数")
          return 0

      if __name__ == "__main__":
        total_token = token_calculate(image_path="xxx/test.jpg", duration=10)
      ```
    </Tab>
  </Tabs>
</Accordion>

### 限流

有关模型限流规则的详细信息，请参阅[限流说明](/developer-guides/administration/rate-limits)。

## 常见问题

### 怎么向模型输入图片？

A：输入方式取决于接入协议。

**WebSocket**：通过客户端发送 [input\_image\_buffer.append](/api-reference/real-time-multimodal/client-events) 事件。

- VAD 模式：该模式会根据语音检测情况自动提交音频与图片，请在服务端响应前发送 [input\_image\_buffer.append](/api-reference/real-time-multimodal/client-events) 事件。
- Manual 模式：参见快速开始中的手动模式代码，将图片输入与提交的两部分代码取消注释，即可传入本地图片。

**WebRTC**：通过视频轨道（RTP）发送画面帧，无需发送 `input_image_buffer.append` 事件。

若用于视频通话场景，可以对视频抽帧，建议以 1张/秒 的频率向服务端发送图像。DashScope SDK 代码请参见 [Omni-Realtime 示例代码](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/conversation/omni)。

### 收不到 ASR 转录文本（transcript）怎么办？

A：如果您收不到 `conversation.item.input_audio_transcription.completed` 事件，或事件中的 transcript 字段为空，请按以下顺序排查。

1. **确认已开启输入音频转录**。转录事件由 `session.update` 的 `enable_input_audio_transcription` 参数控制，该参数默认为 `true`。关闭该参数后，服务端不会下发 `conversation.item.input_audio_transcription.completed` 事件，这是预期行为，并非异常，请确认会话配置中该参数为 `true`。
2. **监听转录失败事件**。除 `completed` 事件外，请同时监听 `conversation.item.input_audio_transcription.failed` 事件。转录失败时，该事件会通过 `error.code`、`error.message` 和 `error.param` 返回失败原因，可据此定位是参数问题还是音频问题。
3. **升级 DashScope SDK**。较低版本的 DashScope SDK 可能不支持输入音频转录相关参数，导致配置未生效，请将 DashScope SDK 升级到较新版本后重试。
4. **检查 VAD 配置与网络**。语音活动检测由 `session.turn_detection` 配置，`type` 取值为 `server_vad` 或 `semantic_vad`。VAD 灵敏度与实际环境不匹配（例如在嘈杂环境中阈值过低）会导致音频分段异常，进而影响转录结果，可参见本文档"2. 配置会话"章节调整 `threshold` 与 `silence_duration_ms`。此外，网络不稳定会造成 WebSocket 连接中断，导致转录事件丢失，请确认连接在整个会话期间保持稳定。
5. **显式指定转录模型**。可通过 `session.update` 的 `input_audio_transcription_model` 参数指定 ASR 转录模型（例如 `qwen3-asr-flash-realtime`）。未显式指定时，服务端使用默认转录模型；当默认模型的转录效果不满足需求时，建议显式指定。

## 错误码

调用失败时，请参阅[错误码](/api-reference/preparation/error-messages)。

## 音色列表

<Info>
  将请求参数 `voice` 设置为**voice 参数**列中的值。不填写该参数时，模型将使用各节顶部标注的默认音色。
</Info>

<Tabs>
  <Tab title="qwen3.5-omni-plus-realtime 模型">
| 音色名称        | voice 参数    | 音色试听                                                                                                                                                                                                                                  | 描述                           | 支持语言                                                                                                                        |
| ----------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Tina        | Tina        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/xyppdv/12-%E7%B2%BE%E5%93%81%E4%B8%AD%E8%8B%B1-Tina%E5%AE%A2%E6%9C%8D-%E7%94%9C%E7%94%9C.wav" controls />                                    | 像暖奶茶一样的声音，甜而绵软，解决问题时又十分犀利    | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Cindy       | Cindy       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/aclrvj/15-%E7%B2%BE%E5%93%81%E4%B8%AD%E8%8B%B1-Cindy%E6%9E%97%E6%AC%A3%E5%AE%9C.wav" controls />                                             | 甜言蜜语的台湾小女生                   | 中文（台湾腔）、中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文 |
| Liora Mira  | Liora Mira  | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/persfp/55-%E8%B6%85%E8%87%AA%E7%84%B6-Liora+Mira%E6%B8%85%E6%AC%A2.wav" controls />                                                          | 用温柔将日常温暖编织的声音                | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Sunnybobi   | Sunnybobi   | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/qrllli/56-%E8%B6%85%E8%87%AA%E7%84%B6-Sunnybobi%E7%9F%A5%E8%8A%9D.wav" controls />                                                           | 开朗又有些社恐的邻家女孩                 | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Raymond     | Raymond     | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/xmgmiq/57-%E8%B6%85%E8%87%AA%E7%84%B6-Raymond%E6%9E%97%E5%B7%9D%E9%87%8E.wav" controls />                                                    | 声音清澈、爱吃外卖的宅男                 | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Ethan       | Ethan       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/yiltdj/2-%E7%B2%BE%E5%93%81%E4%B8%AD%E8%8B%B1-Ethan%E6%99%A8%E7%85%A6.wav" controls />                                                       | 标准的普通话略带北方口音，明亮、温暖、充满活力和少年感  | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Theo Calm   | Theo Calm   | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/ahrmvm/14-%E7%B2%BE%E5%93%81%E4%B8%AD%E8%8B%B1-Theo+Calm%E4%BA%88%E5%AE%89.wav" controls />                                                  | 在沉默中表达理解，用语言进行治愈             | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Serena      | Serena      | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/fwbyvg/3-%E7%B2%BE%E5%93%81%E4%B8%AD%E8%8B%B1-Serena%E8%8B%8F%E7%91%B6.wav" controls />                                                      | 温柔的小女生                       | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Harvey      | Harvey      | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/zerjrv/13-%E7%B2%BE%E5%93%81%E4%B8%AD%E8%8B%B1-Harvey%E5%8E%9A.wav" controls />                                                              | 带着岁月沉淀感的嗓音，低沉醇厚，弥漫着咖啡与旧书页的气息 | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Maia        | Maia        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/sjijzk/4-%E7%B2%BE%E5%93%81%E4%B8%AD%E8%8B%B1-Maia%E5%9B%9B%E6%9C%88.wav" controls />                                                        | 知性与温柔的融合                     | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Evan        | Evan        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/ofoawp/16-%E7%B2%BE%E5%93%81%E4%B8%AD%E8%8B%B1-Evan%E6%B1%9F%E6%99%A8.wav" controls />                                                       | 大学生——青春可人                    | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Qiao        | Qiao        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/mmeiqp/9-%E7%B2%BE%E5%93%81%E4%B8%AD%E8%8B%B1-Qiao%E5%B0%8F%E4%B9%94%E5%A6%B9.wav" controls />                                               | 不只是可爱——表面甜美，内在充满个性           | 中文（台湾腔）、中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文 |
| Momo        | Momo        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/oceaso/7-%E7%B2%BE%E5%93%81%E4%B8%AD%E8%8B%B1-Momo%E8%8C%89%E5%85%94.wav" controls />                                                        | 调皮捣蛋，专门来逗你开心的                | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Wil         | Wil         | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/rikanp/18-%E7%B2%BE%E5%93%81%E4%B8%AD%E8%8B%B1-Wil%E4%BC%9F%E4%BC%A6.wav" controls />                                                        | 说话带有港台腔的深圳小伙子                | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Angel       | Angel       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/rvlqxi/22-%E7%99%BE%E4%BA%BA%E4%B8%AD%E8%8B%B1-Angel%E5%8F%B0%E6%99%AE-%E5%AE%89%E7%90%AA.wav" controls />                                   | 带点台湾腔，而且特别甜                  | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Li Cassian  | Li Cassian  | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/zrumyi/20-%E7%99%BE%E4%BA%BA%E4%B8%AD%E8%8B%B1-Li+Cassian%E4%B8%9C%E5%8E%82-%E6%9D%8E%E5%85%AC%E5%85%AC.wav" controls />                     | 说话克制，三分留白，七分看眼色              | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Mia         | Mia         | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/mvvjsr/23-%E7%99%BE%E4%BA%BA%E4%B8%AD%E8%8B%B1-Mia%E6%B8%A9%E6%9F%94%E7%94%9F%E6%B4%BB%E5%8D%9A%E4%B8%BB-%E8%88%92%E7%84%B6.wav" controls /> | 生活艺术家，用舒缓的声音分享慢生活美学与日常的舒适    | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Joyner      | Joyner      | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/kqdpuc/21-%E7%99%BE%E4%BA%BA%E4%B8%AD%E8%8B%B1-Joyner%E5%96%9C%E5%89%A7%E6%8B%85%E5%BD%93-%E9%98%BF%E9%80%97.wav" controls />                | 搞笑、夸张、接地气                    | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Gold        | Gold        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/itneib/17-%E7%B2%BE%E5%93%81%E4%B8%AD%E8%8B%B1-Gold%E9%87%91%E7%88%B7.wav" controls />                                                       | 美国西海岸黑人说唱歌手                  | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Katerina    | Katerina    | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/snmpko/1-%E7%B2%BE%E5%93%81%E4%B8%AD%E8%8B%B1-Katerina%E5%8D%A1%E6%8D%B7%E7%90%B3%E5%A8%9C.wav" controls />                                  | 成熟御姐音，节奏感和共鸣感十足              | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Ryan        | Ryan        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/qoberf/6-%E7%B2%BE%E5%93%81%E4%B8%AD%E8%8B%B1-Ryan%E7%94%9C%E8%8C%B6.wav" controls />                                                        | 节奏紧凑，充满戏剧张力，真实与张力并存          | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Jennifer    | Jennifer    | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/jlniab/5-%E7%B2%BE%E5%93%81%E4%B8%AD%E8%8B%B1-Jennifer%E8%A9%B9%E5%A6%AE%E5%BC%97.wav" controls />                                           | 电影级质感的高级美式女声                 | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Aiden       | Aiden       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/kpjpsh/8-%E7%B2%BE%E5%93%81%E4%B8%AD%E8%8B%B1-Aiden%E8%89%BE%E7%99%BB.wav" controls />                                                       | 擅长烹饪的美式青年                    | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Mione       | Mione       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/egonpc/10-%E7%B2%BE%E5%93%81%E4%B8%AD%E8%8B%B1-%E6%95%8F%E5%84%BFMione.wav" controls />                                                      | 成熟知性的英国邻家女孩                  | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| 四川 - Sunny  | Sunny       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/sapgqb/24-%E6%96%B9%E8%A8%80-Sunny%E5%9B%9B%E5%B7%9D-%E6%99%B4%E5%84%BF.wav" controls />                                                     | 甜系四川女孩，暖到你心窝                 | 中文（四川话）、中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文 |
| 北京 - Dylan  | Dylan       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/dyfsbo/25-%E6%96%B9%E8%A8%80-Dylan%E5%8C%97%E4%BA%AC-%E6%99%93%E4%B8%9C.wav" controls />                                                     | 北京胡同里长大的小爷                   | 中文（北京话）、中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文 |
| 四川 - Eric   | Eric        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/ryrviu/29-%E6%96%B9%E8%A8%80-Eric%E5%9B%9B%E5%B7%9D-%E7%A8%8B%E5%B7%9D.wav" controls />                                                      | 四川成都的耙耳朵                     | 中文（四川话）、中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文 |
| 天津 - Peter  | Peter       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/ijvjvm/30-%E6%96%B9%E8%A8%80-Peter%E5%A4%A9%E6%B4%A5-%E6%9D%8E%E5%BD%BC%E5%BE%97.wav" controls />                                            | 天津范儿相声演员，专业捧哏                | 中文（天津话）、中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文 |
| Joseph Chen | Joseph Chen | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/hoevpf/31-%E6%96%B9%E8%A8%80-Joseph+Chen%E9%98%BF%E6%A8%B8%E4%BC%AF.wav" controls />                                                         | 久居东南亚的华侨，温暖而怀旧的声音            | 中文（闽南话）、中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文 |
| 陕西 - Marcus | Marcus      | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/aeujio/27-%E6%96%B9%E8%A8%80-Marcus%E9%99%95%E8%A5%BF-%E7%A7%A6%E5%B7%9D.wav" controls />                                                    | 脸宽话少心眼实，嗓子低沉——最地道的陕西味        | 中文（陕西话）、中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文 |
| 南京 - Li     | Li          | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/qzvjna/26-%E6%96%B9%E8%A8%80-Li%E5%8D%97%E4%BA%AC-%E8%80%81%E6%9D%8E.wav" controls />                                                        | 脾气暴躁的舅舅                      | 中文（南京话）、中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文 |
| 粤语 - Rocky  | Rocky       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/tqrrbv/28-%E6%96%B9%E8%A8%80-Rocky%E7%B2%A4%E8%AF%AD-%E9%98%BF%E5%BC%BA.wav" controls />                                                     | 风趣幽默的线上聊天搭子                  | 中文（粤语）、中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文  |
| Sohee       | Sohee       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/uzquwr/32-%E5%A4%9A%E8%AF%AD%E7%A7%8D-Sohee%E7%B4%A0%E7%86%99.wav" controls />                                                               | 温暖开朗、充满情感的韩国欧尼               | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Lenn        | Lenn        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/ouyvix/36-%E5%A4%9A%E8%AF%AD%E7%A7%8D-Lenn%E8%8E%B1%E6%81%A9.wav" controls />                                                                | 理性内核，叛逆细节——穿西装听朋克后摇的德国青年     | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Ono Anna    | Ono Anna    | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/hroefj/41-%E5%A4%9A%E8%AF%AD%E7%A7%8D-Ono+Anna%E5%B0%8F%E9%87%8E%E6%9D%8F.wav" controls />                                                   | 古灵精怪的青梅竹马                    | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Sonrisa     | Sonrisa     | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/yenlcd/33-%E5%A4%9A%E8%AF%AD%E7%A7%8D-Sonrisa%E7%B4%A2%E5%B0%BC%E8%8E%8E.wav" controls />                                                    | 温暖外向的拉美女性                    | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Bodega      | Bodega      | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/fxupdt/40-%E5%A4%9A%E8%AF%AD%E7%A7%8D-_Bodega%E5%8D%9A%E5%BE%B7%E5%8A%A0_.wav" controls />                                                   | 热情温暖的西班牙男士                   | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Emilien     | Emilien     | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/nccsml/39-%E5%A4%9A%E8%AF%AD%E7%A7%8D-Emilien%E5%9F%83%E7%B1%B3%E5%B0%94%E5%AE%89.wav" controls />                                           | 浪漫的法国大哥哥                     | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Andre       | Andre       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/brawiq/35-%E5%A4%9A%E8%AF%AD%E7%A7%8D-Andre%E5%AE%89%E5%BE%B7%E9%9B%B7.wav" controls />                                                      | 充满磁性、自然且沉稳的男声                | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Radio Gol   | Radio Gol   | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/fdwthh/38-%E5%A4%9A%E8%AF%AD%E7%A7%8D-Radio+Gol%E6%8B%89%E8%BF%AA%E5%A5%A5%C2%B7%E6%88%88%E5%B0%94.wav" controls />                          | 充满激情的足球解说员，用诗意的方式解说比赛        | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Alek        | Alek        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/qnvjpt/34-%E5%A4%9A%E8%AF%AD%E7%A7%8D-Alek%E9%98%BF%E5%88%97%E5%85%8B.wav" controls />                                                       | 冷如俄罗斯灵魂，暖如大衣毛衬               | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Rizky       | Rizky       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/ayiemz/53-%E5%A4%9A%E8%AF%AD%E7%A7%8D-Rizky%E9%98%BF%E5%8A%9B.wav" controls />                                                               | 声音辨识度高的印尼青年                  | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Roya        | Roya        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/cdwqkx/51-%E5%A4%9A%E8%AF%AD%E7%A7%8D-Roya%E8%90%9D%E9%9B%85.wav" controls />                                                                | 热爱运动的自由女孩                    | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Arda        | Arda        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/fwyavd/44-%E5%A4%9A%E8%AF%AD%E7%A7%8D-Arda%E9%98%BF%E5%B0%94%E8%BE%BE.wav" controls />                                                       | 不高不低——干净、清脆、微暖               | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Hana        | Hana        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/cjnmjx/49-%E5%A4%9A%E8%AF%AD%E7%A7%8D-Hana%E9%98%BF%E5%B9%B8.wav" controls />                                                                | 爱狗的成熟越南女性                    | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Dolce       | Dolce       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/ucuzdb/37-%E5%A4%9A%E8%AF%AD%E7%A7%8D-Dolce%E5%A4%9A%E5%B0%94%E5%88%87.wav" controls />                                                      | 慵懒的意大利男士                     | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Jakub       | Jakub       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/hihfhl/52-%E5%A4%9A%E8%AF%AD%E7%A7%8D-Jakub%E9%9B%85%E5%85%8B.wav" controls />                                                               | 有魅力的波兰小镇文艺青年                 | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Griet       | Griet       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/faclxs/47-%E5%A4%9A%E8%AF%AD%E7%A7%8D-Griet%E6%B5%B7%E5%A8%9C.wav" controls />                                                               | 成熟有艺术感的荷兰女性                  | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Eliska      | Eliska      | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/yxcryo/42-%E5%A4%9A%E8%AF%AD%E7%A7%8D-Elis%CC%8Cka%E8%89%BE%E8%8E%89%E5%8D%A1.wav" controls />                                               | 每个词都带着中欧的手工艺感和温暖             | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Marina      | Marina      | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/lcwqne/54-%E5%A4%9A%E8%AF%AD%E7%A7%8D-Marina%E7%8E%9B%E4%B8%BD%E5%A8%9C.wav" controls />                                                     | 在多元文化城市长大的女孩                 | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Siiri       | Siiri       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/cmisss/43-%E5%A4%9A%E8%AF%AD%E7%A7%8D-Siiri%E8%A5%BF%E8%8A%AC.wav" controls />                                                               | 克制而柔和——说话节奏像平静的湖面            | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Ingrid      | Ingrid      | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/trlafw/45-%E5%A4%9A%E8%AF%AD%E7%A7%8D-Ingrid%E6%9E%97%E6%81%A9.wav" controls />                                                              | 来自挪威乡村的女性                    | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Sigga       | Sigga       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/ddoxbu/50-%E5%A4%9A%E8%AF%AD%E7%A7%8D-Sigga%E6%B5%B7%E5%A8%9C.wav" controls />                                                               | 冰岛小镇走出的知性女生                  | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Bea         | Bea         | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/cxvkiu/48-%E5%A4%9A%E8%AF%AD%E7%A7%8D-Bea%E9%9B%85%E5%A8%9C.wav" controls />                                                                 | 爱喝咖啡的甜美菲律宾女性                 | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Chloe       | Chloe       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/pdgxsp/46-%E5%A4%9A%E8%AF%AD%E7%A7%8D-Chloe%E6%80%9D%E6%80%A1.wav" controls />                                                               | 马来西亚上班族                      | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Cherry      | Cherry      | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250804/beuyzk/cherry.wav" controls />                                                                                                               | 阳光、积极、友好、自然的小女生              | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| Chelsie     | Chelsie     | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250804/vwbycc/chelsie.wav" controls />                                                                                                              | 二次元虚拟女友                      | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文         |
| 粤语 - Kiki   | Kiki        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/uytsln/Kiki.wav" controls />                                                                                                                 | 甜甜的香港闺蜜型女孩                   | 中文（粤语）、中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文、泰文、印尼文、阿拉伯文、越南文、土耳其文、芬兰文、波兰文、印地文、荷兰文、捷克文、乌尔都文、塔加洛文、瑞典文、丹麦文、希伯来文、冰岛文、马来文、挪威文、波斯文  |
  </Tab>

  <Tab title="qwen3-omni-flash-realtime-2025-12-01 模型">
| 音色名称        | voice 参数    | 音色试听                                                                                                                         | 描述                          | 支持语言                                 |
| ----------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------- | --------------------------- | ------------------------------------ |
| Cherry      | Cherry      | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250804/beuyzk/cherry.wav" controls />      | 阳光、积极、友好、自然的小女生             | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Serena      | Serena      | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250804/jaryjr/serena.wav" controls />      | 温柔的小女生                      | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Ethan       | Ethan       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250804/zdypqw/ethan.wav" controls />       | 标准的普通话略带北方口音，阳光、温暖、充满活力和少年感 | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Chelsie     | Chelsie     | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250804/vwbycc/chelsie.wav" controls />     | 二次元虚拟女友                     | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Momo        | Momo        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/wwvnai/Momo.wav" controls />        | 调皮捣蛋，专门来逗你开心的               | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Vivian      | Vivian      | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/nsceii/Vivian.wav" controls />      | 自信、可爱，带点小脾气                 | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Moon        | Moon        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/ofwrbi/Moon.wav" controls />        | 酷感十足的月白                     | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Maia        | Maia        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/nyolrs/Maia.wav" controls />        | 知性与温柔的融合                    | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Kai         | Kai         | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/auvfor/Kai.wav" controls />         | 耳朵的听觉 SPA                   | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Nofish      | Nofish      | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/xfujvu/Nofish.wav" controls />      | 不会发翘舌音的设计师                  | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Bella       | Bella       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/sqifuq/Bella.wav" controls />       | 爱喝酒，但醉了不打人的小女生              | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Jennifer    | Jennifer    | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/mpnadj/Jennifer.wav" controls />    | 电影级质感的高级美式英语女声              | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Ryan        | Ryan        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/golfay/Ryan.wav" controls />        | 节奏紧凑，充满戏剧张力，真实与张力并存         | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Katerina    | Katerina    | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/kccink/Katerina.wav" controls />    | 成熟御姐音，节奏感令人难忘               | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Aiden       | Aiden       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/tqvufz/Aiden.wav" controls />       | 擅长烹饪的美式英语青年                 | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Eldric Sage | Eldric Sage | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/spivxs/Eldric+Sage.wav" controls /> | 沉稳睿智的长者                     | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Mia         | Mia         | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/lmltol/Mia.wav" controls />         | 温柔如春水，乖巧如新雪                 | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Mochi       | Mochi       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/rkufkm/Mochi.wav" controls />       | 聪明伶俐的青年                     | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Bellona     | Bellona     | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/tygsle/Bellona.wav" controls />     | 有力而清晰的声音，赋予角色生命             | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Vincent     | Vincent     | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/kebnyr/Vincent.wav" controls />     | 独特的烟嗓                       | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Bunny       | Bunny       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/ghplhs/Bunny.wav" controls />       | 萌度爆棚的小女生                    | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Neil        | Neil        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/pijnzm/Neil.wav" controls />        | 平直基线音准，精准清晰的咬字              | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Elias       | Elias       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/nmmxxu/Elias.wav" controls />       | 保持学术严谨的同时运用故事叙述技巧           | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Arthur      | Arthur      | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/meallp/Arthur.wav" controls />      | 简单质朴的声音，沉浸在岁月与烟草的气息中        | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Nini        | Nini        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/eyqilp/Nini.wav" controls />        | 软糯如年糕的黏糯音                   | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Ebona       | Ebona       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/luobgc/Ebona.wav" controls />       | 神秘的耳语声                      | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Seren       | Seren       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/dgkixm/Seren.wav" controls />       | 温柔舒缓的入眠音，让你更快入睡             | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Pip         | Pip         | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/imoqkf/Pip.wav" controls />         | 古灵精怪、充满童趣的小男孩               | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Stella      | Stella      | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/yaveza/Stella.wav" controls />      | 甜美迷离的少女音，正义绝不偏航             | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Bodega      | Bodega      | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/zmgtoy/Bodega.wav" controls />      | 热情满满的西班牙男士                  | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Sonrisa     | Sonrisa     | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/vvfnbj/Sonrisa.wav" controls />     | 开朗外向的拉美女性                   | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Alek        | Alek        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/zhsjeg/Alek.wav" controls />        | 冷如伏特加，暖如羊绒衫                 | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Dolce       | Dolce       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/relmip/Dolce.wav" controls />       | 慵懒的意大利男士                    | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Sohee       | Sohee       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/rtwsqc/Sohee.wav" controls />       | 温暖开朗、充满情感的韩国欧尼              | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Ono Anna    | Ono Anna    | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/zuyjhc/Ono+Anna.wav" controls />    | 古灵精怪的青梅竹马                   | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Lenn        | Lenn        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/aydjlf/Lenn.wav" controls />        | 穿西装听朋克后摇的德国青年               | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Emilien     | Emilien     | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/uyxxsv/Emilien.wav" controls />     | 浪漫的法国大哥哥                    | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Andre       | Andre       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/nvvnme/Andre.wav" controls />       | 充满磁性、自然且沉稳的男声               | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Radio Gol   | Radio Gol   | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251120/wqzuwr/Radio+Gol.wav" controls />   | 足球诗人 Radio Gol              | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| 上海 - Jada   | Jada        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/yivmnv/Jada.wav" controls />        | 语速快、精力充沛的上海阿姨               | 上海话、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文 |
| 北京 - Dylan  | Dylan       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/zpcsut/Dylan.wav" controls />       | 北京胡同里长大的小伙子                 | 北京话、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文 |
| 南京 - Li     | Li          | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/qnznyp/Li.wav" controls />          | 耐心的瑜伽老师                     | 南京话、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文 |
| 陕西 - Marcus | Marcus      | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/jrzvli/Marcus.wav" controls />      | 脸宽话少心眼实，嗓子低沉                | 陕西话、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文 |
| 闽南话 - Roy   | Roy         | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/mbnpyn/Roy.wav" controls />         | 幽默直爽的台湾小伙子                  | 闽南话、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文 |
| 天津 - Peter  | Peter       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/myvkvo/Peter.wav" controls />       | 天津味儿相声，专业捧哏                 | 天津话、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文 |
| 四川 - Sunny  | Sunny       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/xyenuq/Sunny.wav" controls />       | 甜到化不开的四川女孩                  | 四川话、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文 |
| 四川 - Eric   | Eric        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/nmvyje/Eric.wav" controls />        | 在成都街头走一走的四川男子               | 四川话、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文 |
| 粤语 - Rocky  | Rocky       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/ppiqel/Rocky.wav" controls />       | 幽默风趣的阿强，线上聊天搭子              | 粤语、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| 粤语 - Kiki   | Kiki        | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/uytsln/Kiki.wav" controls />        | 甜甜的香港闺蜜型女孩                  | 粤语、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
  </Tab>

  <Tab title="qwen3-omni-flash-realtime / qwen3-omni-flash-realtime-2025-09-15 模型">
| 音色名称        | voice 参数 | 音色试听                                                                                                                         | 描述                          | 支持语言                                 |
| ----------- | -------- | ---------------------------------------------------------------------------------------------------------------------------- | --------------------------- | ------------------------------------ |
| Cherry      | Cherry   | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250804/beuyzk/cherry.wav" controls />      | 阳光、积极、友好、自然的小女生             | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Ethan       | Ethan    | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250804/zdypqw/ethan.wav" controls />       | 标准的普通话略带北方口音，阳光、温暖、充满活力和少年感 | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Nofish      | Nofish   | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/mstuvi/Nofish.wav" controls />      | 不会发翘舌音的设计师                  | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Jennifer    | Jennifer | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/gttbqe/Jennifer.wav" controls />    | 电影级质感的高级美式女声                | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Ryan        | Ryan     | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/gobhpm/Ryan.wav" controls />        | 节奏紧凑，充满戏剧张力，真实与张力并存         | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Katerina    | Katerina | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/kzqjth/Katerina_01.wav" controls /> | 成熟御姐音，节奏感令人难忘               | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| Elias       | Elias    | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/xdilkl/Elias.wav" controls />       | 保持学术严谨的同时运用故事叙述技巧           | 中文、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| 上海 - Jada   | Jada     | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/yivmnv/Jada.wav" controls />        | 语速快、精力充沛的上海阿姨               | 上海话、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文 |
| 北京 - Dylan  | Dylan    | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/zpcsut/Dylan.wav" controls />       | 北京胡同里长大的小伙子                 | 北京话、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文 |
| 四川 - Sunny  | Sunny    | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/xyenuq/Sunny.wav" controls />       | 甜到化不开的四川女孩                  | 四川话、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文 |
| 南京 - Li     | Li       | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/qnznyp/Li.wav" controls />          | 耐心的瑜伽老师                     | 南京话、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文 |
| 陕西 - Marcus | Marcus   | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/jrzvli/Marcus.wav" controls />      | 脸宽话少心眼实，嗓子低沉                | 陕西话、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文 |
| 闽南话 - Roy   | Roy      | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/mbnpyn/Roy.wav" controls />         | 幽默直爽的台湾小伙子                  | 闽南话、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文 |
| 天津 - Peter  | Peter    | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/myvkvo/Peter.wav" controls />       | 天津味儿相声，专业捧哏                 | 天津话、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文 |
| 粤语 - Rocky  | Rocky    | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/ppiqel/Rocky.wav" controls />       | 幽默风趣的阿强，线上聊天搭子              | 粤语、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| 粤语 - Kiki   | Kiki     | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/uytsln/Kiki.wav" controls />        | 甜甜的香港闺蜜型女孩                  | 粤语、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文  |
| 四川 - Eric   | Eric     | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250916/nmvyje/Eric.wav" controls />        | 在成都街头走一走的四川男子               | 四川话、英文、法文、德文、俄文、意大利文、西班牙文、葡萄牙文、日文、韩文 |
  </Tab>

  <Tab title="Qwen-Omni-Turbo-Realtime 模型">
| 音色名称    | voice 参数 | 音色试听                                                                                                                     | 描述                          | 支持语言  |
| ------- | -------- | ------------------------------------------------------------------------------------------------------------------------ | --------------------------- | ----- |
| Cherry  | Cherry   | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250804/beuyzk/cherry.wav" controls />  | 阳光、积极、友好、自然的小女生             | 中文、英文 |
| Serena  | Serena   | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250804/jaryjr/serena.wav" controls />  | 温柔的小女生                      | 中文、英文 |
| Ethan   | Ethan    | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250804/zdypqw/ethan.wav" controls />   | 标准的普通话略带北方口音，阳光、温暖、充满活力和少年感 | 中文、英文 |
| Chelsie | Chelsie  | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250804/vwbycc/chelsie.wav" controls /> | 二次元虚拟女友                     | 中文、英文 |
  </Tab>
</Tabs>
