> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 接入模型与应用

> 通过 AOQ、WebRTC 或 WebSocket 接入模型的完整流程

介绍如何通过 AOQ、WebRTC、WebSocket 三种协议接入 Realtime API 模型，包含各协议的连接流程、时序图和代码示例。

## 前提条件

- 接入前请先确认[模型/应用支持力度](/developer-guides/realtime-api/overview#模型支持力度)
- 了解如何进行[Token鉴权](/developer-guides/realtime-api/token-auth)

## AOQ 接入

AOQ 基于 QUIC 协议深度定制，适合移动端原生应用，支持音频/视频/数据混合传输，内置极致抗弱网能力。以下以实时全模态（Omni）的 iOS Demo 为例介绍 AOQ 接入流程。AOQ SDK API 详情请参见[AOQ客户端SDK](/developer-guides/realtime-api/aoq-sdk-intro)。

### 整体流程时序图

<img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/p1088073.jpg" alt="AOQ 整体流程时序图" />

### 创建引擎并设置回调

```swift
let config = AoqCreateConfig()
config.workDir = workDir
config.enableDumpAudio = false
engine = AoqClientEngine.createEngine(config, delegate: self)
```

实现 `AoqEngineDelegate` 协议监听 `onConnectionStatusChange`、`onDataMsg`、`onError` 等回调。

### 启动音频采集与播放

```swift
// 音频采集
let capCfg = AoqAudioCaptureConfig()
capCfg.channel = 1; capCfg.isExternal = false
engine.startAudioCapture(capCfg)
// 音频播放
let playCfg = AoqAudioPlaybackConfig()
playCfg.channel = 1; playCfg.isExternal = false
engine.startAudioPlayer(playCfg)
// 视频采集（可选）
let vidCfg = AoqVideoCaptureConfig()
vidCfg.width = 720; vidCfg.height = 1280; vidCfg.fps = 15
engine.startVideoCapture(vidCfg)
```

### 获取连接凭证

由业务 AppServer 代理千问AI平台请求，参见[Token鉴权](/developer-guides/realtime-api/token-auth)。

### 设置编解码及建立连接

设置编解码参数后调用 `connect`：

```swift
// 音频编解码配置
let encCfg = AoqAudioCodecConfig()
encCfg.codecType = .audioPCM; encCfg.sampleRate = 16000; encCfg.channel = 1
engine.setAudioEncoderConfig(encCfg)
engine.setAudioDecoderConfig(encCfg)
// connect 前关闭媒体发送，待 session.updated 后再开启
engine.enableSendMediaStream(.audio, enable: false)
let config = AoqConnectConfig()
config.token = token
config.sid = sid
config.certFingerprint = certificate
config.relayEndpoints = relayEndpoints
config.workspaceIdHash = workspaceIdHash
config.publishTracks = [audioTrack, dataTrack]
config.subscribeTracks = [audioTrack, dataTrack]
engine.connect(config)
```

<Warning>
  AOQ SDK 在建连后会默认发送媒体数据，此示例演示了在连接模型时先关闭媒体发送，待会话就绪后再开启的流程。
</Warning>

### 配置 AI 会话

连接成功后发送 `session.update` 的示例，详见[模型客户端事件参考](/api-reference/real-time-multimodal/client-events)：

```swift
func onConnectionStatusChange(_ status: AoqConnectionStatus) {
  if status == .connected { sendSessionUpdate() }
}
private func sendSessionUpdate() {
  let json = """
  {
    // 该事件的id，由客户端生成
    "event_id": "event_ToPZqeobitzUJnt3QqtWg",
    // 事件类型，固定为session.update
    "type": "session.update",
    // 会话配置
    "session": {
        // 输出模态，支持设置为["text"]（仅输出文本）或["text","audio"]（输出文本与音频）。
        "modalities": [
            "text",
            "audio"
        ],
        // 输出音频的音色
        "voice": "Ethan",
        // 输入音频格式，当前仅支持设置为pcm。输入音频为16 kHz采样率的PCM音频流。
        "input_audio_format": "pcm",
        // 输出音频格式，当前仅支持设置为pcm。输出音频为24 kHz采样率的PCM音频流。
        "output_audio_format": "pcm",
        // 系统消息，用于设定模型的目标或角色。
        "instructions": "你是某五星级酒店的AI客服专员，请准确且友好地解答客户关于房型、设施、价格、预订政策的咨询。请始终以专业和乐于助人的态度回应，杜绝提供未经证实或超出酒店服务范围的信息。",
        // 是否开启语音活动检测。若需启用，需传入一个配置对象，服务端将据此自动检测语音起止。
        // 设置为null表示由客户端决定何时发起模型响应。
        "turn_detection": {
            // VAD类型，取值为server_vad或semantic_vad。使用qwen3.5-omni-realtime系列模型时推荐设为semantic_vad。
            "type": "semantic_vad",
            // VAD检测阈值。建议在嘈杂的环境中增加，在安静的环境中降低。
            "threshold": 0.5,
            // 检测语音停止的静音持续时间，超过此值后会触发模型响应
            "silence_duration_ms": 800
        }
    }
  }
  """
  let msg = AoqDataMsg()
  msg.data = json.data(using: .utf8)!
  engine.send(msg)
}
```

### 收到 session.updated 后开启媒体发送

收到模型回复 `session.updated` 的示例，详见[模型服务器事件参考](/api-reference/real-time-multimodal/server-events)：

```swift
func onDataMsg(_ msg: AoqDataMsg) {
  guard let obj = try? JSONSerialization.jsonObject(with: msg.data) as? [String: Any],
        let type = obj["type"] as? String else { return }
  if type == "session.updated" {
    engine.enableSendMediaStream(.audio, enable: true)
    engine.enableSendMediaStream(.video, enable: true)
  }
}
```

<Warning>
  1. 必须在收到 `session.updated` 后才开启媒体流发送，否则服务端可能尚未准备好接收数据。
  2. 建连时添加的音频轨道和视频轨道（即 AOQ 媒体通道）会自动将数据传输到服务端。
     - 音频：通过音频轨道直接传输，无需发送 `input_audio_buffer.append` 事件。
     - 视频：通过视频轨道发送画面帧，无需发送 `input_image_buffer.append` 事件。
</Warning>

### 断开连接与销毁引擎

```swift
engine.disconnect()
AoqClientEngine.destroy()
```

<span id="conn-rtc-title" />

## WebRTC 接入

WebRTC 不提供专用 SDK。Web 端可直接使用浏览器原生 JavaScript API 接入，其他端可通过开源 WebRTC 库或支持标准 WebRTC 协议的第三方 RTC 服务接入。以下以 Web 端 JavaScript 为例进行介绍。

### 整体流程图

<img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/p1088074.jpg" alt="WebRTC 整体流程图" />

### 建立连接

```python
# pip install aiortc aiohttp certifi
import asyncio, aiohttp, ssl, certifi
from aiortc import RTCPeerConnection, RTCConfiguration, RTCSessionDescription
from aiortc.mediastreams import AudioStreamTrack
API_KEY = "REDACTED"
MODEL = "目标模型"
SIGNALING_URL = f"https://dashscope.aliyuncs.com/api/v1/webrtc/realtime?model={MODEL}"
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

### 配置目标模型参数

监听模型通过 DataChannel 返回的消息，确保交互时序正确：

```javascript
pc.ondatachannel = (event) => {
  const ch = event.channel;
  ch.onmessage = (e) => {
    let obj;
    try { obj = JSON.parse(e.data); }
    catch (err) {
      return;
    }
    if (obj?.type === "session.created") {
      sendUpdate(event.channel);
      //开始推送音视频
      audioSender?.replaceTrack(audioTrack);
      videoSender?.replaceTrack(videoTrack);
    }
  };
};
```

### 收发媒体数据

建连时添加的音频轨道和视频轨道（即 RTP 媒体通道）会自动将数据传输到服务端。

- 音频：通过音频轨道（RTP）直接传输，无需发送 `input_audio_buffer.append` 事件。
- 图片：通过视频轨道（RTP）发送画面帧，不支持 `input_image_buffer.append` 事件。

<Note>
  WebRTC 仅支持服务端 VAD 模式（`server_vad` 或 `semantic_vad`），不支持手动模式。
</Note>

### Demo 源码

#### 前提条件

- 使用支持 WebRTC 的现代浏览器（Chrome、Edge、Firefox、Safari 等）。
- 浏览器需要麦克风权限。
- 浏览器受跨域安全策略限制，无法直接向服务端发起建连请求，因此需要通过终端执行 curl 命令完成连接建立。

#### 运行示例

新建一个 HTML 文件，命名为 `webrtc_demo.html`，并将以下代码复制到文件中：

[webrtc\_demo.html](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260715/crtwmi/webrtc_demo.html)。

在浏览器中打开此文件，按以下步骤操作：

1. 点击开始会话，页面会自动生成 Offer SDP 和对应的 curl 命令。
2. 点击复制 curl 命令，在终端中执行。命令返回的内容即为 Answer SDP。
3. 将 Answer SDP 粘贴到页面的 Answer SDP 文本框中，点击设置 Answer 即可建立连接并开始语音对话。

<span id="conn-ws-title" />

## WebSocket 接入

不同模型的接入方式和流程不同，详情请参见：

- [实时全模态](/developer-guides/speech/realtime-multimodal-speech)
- [实时语音翻译](/developer-guides/speech/realtime-translation)
- [实时语音对话](/developer-guides/speech/qwen-audio-realtime)
- [实时语音识别](/developer-guides/speech/asr-realtime)
- [实时语音合成](/developer-guides/speech/realtime-streaming)
