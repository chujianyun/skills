> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话

> 通过 WebRTC 协议使用 qwen3.5-omni-plus-realtime 模型实现实时通话

本文档说明如何在浏览器端通过 WebRTC + JavaScript 接入千问AI平台 Realtime API，实现与 qwen3.5-omni-plus-realtime 模型的实时音视频通话。

<Note>
  WebRTC 适合浏览器端、低延迟语音场景，音频通过 UDP 直接传输，内置回声消除和降噪。WebRTC 仅支持服务端 VAD 模式（`server_vad`或`semantic_vad`），不支持手动模式。
</Note>

## 前提条件及注意事项

1. 已[配置 API Key](/developer-guides/administration/api-keys)并将其[设置到环境变量](/api-reference/preparation/export-api-key-env)。
2. 使用支持 WebRTC 的现代浏览器（Chrome、Edge、Firefox、Safari 等）。
3. 浏览器需要麦克风权限；如需视频通话，还需摄像头权限。
4. 浏览器无法直接向服务端发起 SDP 交换请求（受 CORS 限制），Demo 中通过终端执行 curl 命令完成连接建立；正式使用时由业务 AppServer 代理完成，无此限制。

## 实现 AI 音视频通话

以下时序图展示了整个 WebRTC 音视频通话的完整流程：

WebRTC 音视频通话流程时序图

![image](https://help-static-aliyun-doc.aliyuncs.com/zh-CN/images/p1088079.png)

### 创建 RTCPeerConnection

调用浏览器原生`RTCPeerConnection`创建连接实例，无需配置 ICE 服务器（服务端会处理 NAT 穿透）。

```javascript
pc = new RTCPeerConnection({ iceServers: [ ] });
```

注册关键回调：

```javascript
// 连接状态监听
pc.onconnectionstatechange = () => {
  if (!pc) return;
  if (pc.connectionState === 'connected') {
    setStatus('已连接，请说话', 'connected');
  } else if (["failed", "closed", "disconnected"].includes(pc.connectionState)) {
    endSession(true);
  }
};
// 接收远端音频流并播放 + 启动录制
pc.ontrack = async (e) => {
  const stream = e.streams[0];
  ensureHiddenAudioEl();
  hiddenRemoteAudioEl.srcObject = stream;
  try { await hiddenRemoteAudioEl.play(); } catch {}
  startRecordingRemoteStream(stream);
};
```

### 获取本地媒体流

通过一次`getUserMedia`调用获取所需的音频（必须）和视频（可选）。是否开启视频由用户勾选"开启视频"复选框决定。

```javascript
const wantVideo = !!sendVideoCheckbox.checked;
const constraints = wantVideo
  ? {
      audio: true,
      video: {
        facingMode: { ideal: "user" },
        frameRate: { ideal: 30, max: 30 },
        width: { ideal: 640 },
        height: { ideal: 480 },
      }
    }
  : { audio: true };
localStream = await navigator.mediaDevices.getUserMedia(constraints);
```

<Note>
  音频和视频通过**同一次** `getUserMedia`调用获取，而非分开请求。视频预览帧率为 30fps（本地流畅预览），发送帧率会通过 Canvas 降至 2fps。
</Note>

### 添加媒体轨道到 PeerConnection

**添加音频轨道：**

```javascript
localStream.getAudioTracks().forEach(t => {
  pc.addTrack(t, localStream);
  gatedAudioTracks.push(t);
});
```

**添加视频轨道（可选，通过 Canvas 降帧至 2fps）：**

Canvas 尺寸从摄像头实际分辨率动态获取，而非硬编码：

```javascript
const sendFps = 2;
const settings = localStream.getVideoTracks()[0].getSettings();
sendCanvas = document.createElement("canvas");
sendCanvas.width = settings.width || 640;   // 动态获取实际宽度
sendCanvas.height = settings.height || 480;  // 动态获取实际高度
sendCanvasCtx = sendCanvas.getContext("2d", { alpha: false });
sendCanvasStream = sendCanvas.captureStream(sendFps); // 2fps
const lowFpsTrack = sendCanvasStream.getVideoTracks()[0];
pc.addTrack(lowFpsTrack, sendCanvasStream);
gatedVideoTracks.push(lowFpsTrack);
// requestAnimationFrame 循环：将摄像头画面绘制到 Canvas
const pump = () => {
  if (!sendCanvasCtx || !sendCanvas) return;
  try { sendCanvasCtx.drawImage(localVideo, 0, 0, sendCanvas.width, sendCanvas.height); } catch {}
  sendRafId = requestAnimationFrame(pump);
};
sendRafId = requestAnimationFrame(pump);
```

**媒体门控（关键）：**

添加轨道后立即禁止发送，确保在收到`session.created`之前不推送媒体数据：

```javascript
// 1. 禁用所有轨道的 enabled
gateMedia(false);  // track.enabled = false
// 2. 将 sender 的 track 替换为 null，彻底阻止发送
audioSender = pc.getSenders().find(s => s.track?.kind === 'audio');
videoSender = pc.getSenders().find(s => s.track?.kind === 'video');
audioTrack = audioSender?.track;
videoTrack = videoSender?.track;
await audioSender?.replaceTrack(null);
await videoSender?.replaceTrack(videoTrack ? null : undefined);
```

<Note>
  等价于其他 SDK 中的`enableSendMediaStream(false)`，必须在收到`session.created`后才恢复发送。
</Note>

### 创建 DataChannel

创建名为`oai-events`的 DataChannel，用于与 AI 服务端交换会话控制事件。

```javascript
const dc = pc.createDataChannel('oai-events');
dc.onopen = () => console.log("DC open");
dc.onmessage = (e) => {
  handleDcMessage(e.data, dc);
};
// 同时监听服务端主动创建的 DataChannel
pc.ondatachannel = (event) => {
  const ch = event.channel;
  ch.onmessage = (e) => {
    handleDcMessage(e.data, ch);
  };
};
```

### 生成 Offer SDP

调用`createOffer()`并设置本地描述，等待 ICE 候选收集完成后获取完整的 Offer SDP。

```javascript
pc.onicegatheringstatechange = () => {
  if (!pc) return;
  if (pc.iceGatheringState === "complete" && pc.localDescription?.sdp) {
    const sdp = pc.localDescription.sdp;
    // ICE 收集完成，Offer SDP 可用
    // 自动生成 curl 命令供用户使用
  }
};
const offer = await pc.createOffer();
await pc.setLocalDescription(offer);
```

<Note>
  必须等待`iceGatheringState === "complete"`后再使用 SDP，此时 SDP 中包含所有 ICE 候选信息。
</Note>

### 交换 SDP（通过 curl 命令或业务 AppServer）

将 Offer SDP 发送到千问AI平台服务端，获取 Answer SDP。Demo 中通过 curl 命令完成：

```shell
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/webrtc/realtime?model=qwen3.5-omni-plus-realtime' \
  -H 'Content-Type: application/sdp' \
  -H 'Authorization: Bearer $DASHSCOPE_API_KEY' \
  --data-binary '<Offer SDP 内容>'
```

<Note>
  生产环境中，此步骤应由业务 AppServer 代理完成，避免前端暴露 API Key。
</Note>

### 设置 Answer SDP 建立连接

将服务端返回的 Answer SDP 设置为远端描述，WebRTC 连接即开始建立。注意 SDP 格式需要规范化处理：

```javascript
function normalizeSdpForSetRemote(sdp) {
  sdp = String(sdp).trim().replace(/\r?\n/g, "\r\n");
  if (!sdp.endsWith("\r\n")) sdp += "\r\n";
  return sdp;
}
const answerSdp = normalizeSdpForSetRemote(txt);
await pc.setRemoteDescription({ type: 'answer', sdp: answerSdp });
```

<Note>
  SDP 规范要求行尾为`\r\n`，`normalizeSdpForSetRemote`负责处理不同来源的换行符兼容问题。
</Note>

### 配置 AI 会话（session.update）

连接建立后，服务端通过 DataChannel 发送`session.created`事件。收到后需：

1. 解除媒体门控，恢复音视频发送
2. 发送`session.update`配置会话参数

**解除门控并恢复媒体：**

```javascript
function handleDcMessage(data, channel) {
  let obj;
  try { obj = JSON.parse(data); } catch (err) { return; }
  if (obj?.type === "session.created") {
    // 解除门控：恢复 track.enabled
    gateMedia(true);
    // 恢复 sender 的实际 track
    if (audioSender) audioSender.replaceTrack(audioTrack);
    if (videoSender && videoTrack) videoSender.replaceTrack(videoTrack);
    // 发送会话配置
    sendUpdate(channel);
  }
}
```

**session.update 消息体：**

```javascript
const update = {
  event_id: `event_${Date.now()}`,
  type: "session.update",
  session: {
    input_audio_format: "pcm",
    input_audio_transcription: { model: "qwen3-asr-flash-realtime" },
    instructions: "You are a helpful assistant.",
    modalities: ["text", "audio"],
    output_audio_format: "pcm",
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
```

<Note>
  `turn_detection.type`可设为`server_vad`（基于音量检测）或`semantic_vad`（基于语义检测）。WebRTC 模式不支持手动 VAD。
</Note>

### 实时对话

连接建立后，音视频通过 RTP 实时传输。远端 AI 语音通过`ontrack`回调接收并播放，同时使用 MediaRecorder 录制以便下载。

**接收远端音频并录制：**

```javascript
pc.ontrack = async (e) => {
  const stream = e.streams[0];
  ensureHiddenAudioEl();
  hiddenRemoteAudioEl.srcObject = stream;
  try { await hiddenRemoteAudioEl.play(); } catch {}
  startRecordingRemoteStream(stream); // 启动录制
};
function startRecordingRemoteStream(remoteStream) {
  const audioTracks = remoteStream.getAudioTracks();
  if (!audioTracks.length) return;
  const audioStream = new MediaStream(audioTracks);
  recordedChunks = [ ];
  mediaRecorder = new MediaRecorder(audioStream, { mimeType: 'audio/webm' });
  mediaRecorder.ondataavailable = (e) => {
    if (e.data && e.data.size > 0) recordedChunks.push(e.data);
  };
  mediaRecorder.onstop = () => {
    audioBlob = new Blob(recordedChunks, { type: 'audio/webm' });
    // 录制结束后可下载
  };
  mediaRecorder.start();
}
```

**DataChannel 事件统一展示：**

所有通过 DataChannel 收发的事件（包括`session.created`、`response.audio_transcript.done`等）统一通过事件面板展示，支持展开查看完整 JSON：

```javascript
function pushEventFromDataChannel(eventObj) {
  const ts = eventObj.timestamp || nowTs();
  events.unshift({ event: eventObj, timestamp: ts });
  renderEvents();
}
```

### 结束会话与资源清理

结束通话时需依次清理所有资源，顺序很重要：

```javascript
function endSession(silent = false) {
  // 1. 停止 Canvas 降帧循环
  if (sendRafId) cancelAnimationFrame(sendRafId);
  sendRafId = 0;
  if (sendCanvasStream) sendCanvasStream.getTracks().forEach(t => t.stop());
  sendCanvasStream = null; sendCanvasCtx = null; sendCanvas = null;
  // 2. 停止录制
  try { if (mediaRecorder && mediaRecorder.state !== "inactive") mediaRecorder.stop(); } catch {}
  mediaRecorder = null;
  // 3. 停止本地媒体流
  if (localStream) {
    localStream.getTracks().forEach(t => t.stop());
    localStream = null;
  }
  // 4. 关闭 PeerConnection
  if (pc) { try { pc.close(); } catch {} pc = null; }
  // 5. 清理远端音频元素
  if (hiddenRemoteAudioEl) {
    try { hiddenRemoteAudioEl.pause(); } catch {}
    hiddenRemoteAudioEl.srcObject = null;
    hiddenRemoteAudioEl.remove();
    hiddenRemoteAudioEl = null;
  }
}
```

<Note>
  结束后可通过"下载远端音频"按钮下载 AI 回复的录音（WebM 格式）。
</Note>

## 注意事项

1. **媒体门控必须在 session.created 后解除**：在服务端发送`session.created`之前推送媒体数据会被丢弃，必须通过`replaceTrack(null)`彻底阻断发送。
2. **视频降帧通过 Canvas 实现**：本地预览 30fps，发送至服务端仅 2fps，通过`captureStream(2)`控制，节省带宽。
3. **SDP 格式规范化**：设置 Answer SDP 前必须确保行尾为`\r\n`，否则`setRemoteDescription`可能失败。
4. **视频为可选功能**：用户未勾选视频时，仅请求音频权限，不会触发摄像头授权弹窗。
5. **远端音频自动录制**：通过 MediaRecorder 录制 AI 回复的音频流，会话结束后可下载 WebM 格式文件。
6. **WebRTC 仅支持服务端 VAD**：不支持`manual`模式，可选`server_vad`（音量检测）或`semantic_vad`（语义检测）。

## 完整 demo 下载

完整示例代码请下载：[webrtc\_demo.html](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260715/ychtmj/webrtc_demo.html)。

## 相关文档

- [WebRTC API (MDN)](https://developer.mozilla.org/zh-CN/docs/Web/API/WebRTC_API)
- [RTCPeerConnection (MDN)](https://developer.mozilla.org/zh-CN/docs/Web/API/RTCPeerConnection)
- qwen3.5-omni-plus-realtime 模型客户端事件：[客户端事件](/api-reference/real-time-multimodal/client-events)
- qwen3.5-omni-plus-realtime 模型服务端事件：[服务端事件](/api-reference/real-time-multimodal/server-events)
- [WebRTC 接入模型/应用](/developer-guides/realtime-api/connect-model#conn-rtc-title)
