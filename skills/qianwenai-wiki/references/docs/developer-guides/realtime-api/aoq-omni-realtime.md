> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话

> 通过 AOQ 协议使用 qwen3.5-omni-plus-realtime 模型实现实时通话

本文档说明如何在 Android、iOS、HarmonyOS 平台接入 AOQ Client SDK，实现 AOQ+qwen3.5-omni-plus-realtime 音视频通话功能。

## SDK 获取

AOQ Client SDK 及音频 Opus 插件请参见[SDK下载](/developer-guides/realtime-api/sdk-download)。Opus 编码以独立插件形式提供，请根据您的场景按需引入。

## SDK 导入

请根据不同平台将核心 SDK 产物导入工程依赖目录，并在工程配置中声明相关权限。

### Android

将`AoqClientSdk-release.aar`放入工程`app/libs/`目录，将`libPluginOpus.so`按 ABI 放入`app/libs/armeabi-v7a/`和`app/libs/arm64-v8a/`，并在`app/build.gradle`中：

```groovy
android {
  defaultConfig {
    minSdk 21
    ndk { abiFilters 'armeabi-v7a', 'arm64-v8a' }
  }
  sourceSets { main { jniLibs.srcDirs = ['libs'] } }
  packagingOptions {
    // 避免与宿主工程的同名 so 冲突
    pickFirsts += ['lib/*/*.so']
  }
}
dependencies {
  implementation fileTree(dir: 'libs', include: ['*.aar'])
}
```

在`AndroidManifest.xml`声明权限：

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />
<uses-permission android:name="android.permission.CAMERA" />
```

其中`RECORD_AUDIO`和`CAMERA`为运行时权限，应用需在运行时调用 Android `ActivityCompat.requestPermissions()`方法，主动向 Android 系统申请用户授权。

### iOS（framework）

1. 将`AoqClientSdk.framework`与`PluginOpus.framework`拖入 Xcode 工程，在 Target > General > Frameworks, Libraries, and Embedded Content 中选择**Embed & Sign**。

2. 权限声明：在 Xcode 中选中您的 Target > Info > Custom iOS Target Properties，添加以下两项权限用途描述：

| **Key**                        | **Value** |
| ------------------------------ | --------- |
| `NSMicrophoneUsageDescription` | 用于实时语音通话  |
| `NSCameraUsageDescription`     | 用于实时视频通话  |

3. Swift 工程：`import AoqClientSdk`；Objective-C 工程：`#import <AoqClientSdk/AoqClientSdk.h>`。

### HarmonyOS（har）

1. 将`aoq-client-sdk.har`放入工程`libs/`目录，将`libPluginOpus.so`按 ABI 放入`entry/libs/armeabi-v7a/`和`entry/libs/arm64-v8a/`；并在`entry/oh-package.json5`中声明。

2. 在`entry/src/main/module.json5`添加权限：

```json
"requestPermissions": [
  { "name": "ohos.permission.INTERNET" },
  { "name": "ohos.permission.MICROPHONE",
    "reason": "$string:perm_mic_reason",
    "usedScene": { "abilities": ["EntryAbility"], "when": "inuse" } },
  { "name": "ohos.permission.CAMERA",
    "reason": "$string:perm_camera_reason",
    "usedScene": { "abilities": ["EntryAbility"], "when": "inuse" } }
]
```

3. 在`EntryAbility`中通过`abilityAccessCtrl.createAtManager().requestPermissionsFromUser`触发运行时授权。

## AppServer获取Token

请按照[Token鉴权](/developer-guides/realtime-api/token-auth)的 AOQ 章节搭建获取 Token 的 AppServer。每次通话前，客户端需要向业务侧 AppServer 请求一次 Token。

## 实现 AI 音视频通话

![111](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/images/p1088080.svg)

### 创建引擎并设置回调

调用`createEngine`接口创建`AoqClientEngine`实例。

<Tabs>
  <Tab title="iOS">
    ```swift
    let config = AoqCreateConfig()
    config.workDir = workDir
    engine = AoqClientEngine.createEngine(config, delegate: self)
    ```

    实现`AoqEngineDelegate`协议监听`onConnectionStatusChange`、`onDataMsg`、`onError`等回调。
  </Tab>

  <Tab title="Android">
    ```java
    AoqCreateConfig config = new AoqCreateConfig();
    config.workDir = appCtx.getFilesDir().getAbsolutePath();
    engine = AoqClientEngine.createEngine(appCtx, config, this);
    ```
  </Tab>

  <Tab title="HarmonyOS">
    ```typescript
    const config: AoqCreateConfig = { workDir: context.filesDir, extras: '' };
    engine = AoqClientEngine.createEngine(config, this, context);
    ```
  </Tab>
</Tabs>

### 启动音视频采集与播放

调用`startAudioCapture`与`startAudioPlayer`启动本地音频采集与播放；调用`startVideoCapture`启动摄像头，并通过`setLocalView`将 SDK 渲染目标绑定到业务侧的预览控件。

<Tabs>
  <Tab title="iOS">
    ```swift
    // 音频采集
    let capCfg = AoqAudioCaptureConfig()
    capCfg.channel = 1; capCfg.isExternal = false
    engine.startAudioCapture(capCfg)
    // 音频播放
    let playCfg = AoqAudioPlaybackConfig()
    playCfg.channel = 1; playCfg.isExternal = false
    engine.startAudioPlayer(playCfg)
    // 视频采集
    let vidCfg = AoqVideoCaptureConfig()
    vidCfg.width = 720; vidCfg.height = 1280; vidCfg.fps = 15
    engine.startVideoCapture(vidCfg)
    // 为本地预览画面设置渲染视图
    let canvas = AoqVideoCanvas()
    canvas.view = localPreview
    canvas.renderMode = .crop
    engine.setLocalView(.video, canvas: canvas)
    ```
  </Tab>

  <Tab title="Android">
    ```java
    // 音频采集
    AoqAudioCaptureConfig capCfg = new AoqAudioCaptureConfig();
    capCfg.channel = 1; capCfg.isExternal = false;
    engine.startAudioCapture(capCfg);
    // 音频播放
    AoqAudioPlaybackConfig playCfg = new AoqAudioPlaybackConfig();
    playCfg.channel = 1; playCfg.isExternal = false;
    engine.startAudioPlayer(playCfg);
    // 视频采集
    AoqVideoCaptureConfig vidCfg = new AoqVideoCaptureConfig();
    vidCfg.width = 720; vidCfg.height = 1280; vidCfg.fps = 15;
    engine.startVideoCapture(vidCfg);
    // 为本地预览画面设置渲染视图
    AoqVideoCanvas canvas = new AoqVideoCanvas();
    canvas.view = localPreview;
    canvas.renderMode = AoqRenderMode.AoqRenderModeCrop;
    engine.setLocalView(AoqTrackType.AoqTrackTypeVideo, canvas);
    ```
  </Tab>

  <Tab title="HarmonyOS">
    ```typescript
    // 音频采集
    const capCfg: AoqAudioCaptureConfig = { channel: 1, isExternal: false };
    engine.startAudioCapture(capCfg);
    // 音频播放
    const playCfg: AoqAudioPlaybackConfig = { channel: 1, isExternal: false };
    engine.startAudioPlayer(playCfg);
    // 视频采集
    const vidCfg: AoqVideoCaptureConfig = { width: 720, height: 1280, fps: 15, isExternal: false };
    engine.startVideoCapture(vidCfg);
    // 为本地预览画面设置渲染视图
    const canvas: AoqVideoCanvas = { view: localCtrl, renderMode: AoqRenderMode.AoqRenderModeCrop };
    engine.setLocalView(AoqTrackType.AoqTrackTypeVideo, canvas);
    ```
  </Tab>
</Tabs>

### 获取连接凭证

由业务 AppServer 代理千问AI平台请求，参见[Token鉴权](/developer-guides/realtime-api/token-auth)。

### 设置编解码及建立连接

设置编解码参数后调用`connect`。

注意：qwen3.5-omni-plus-realtime 要求客户端在收到服务端的`session.updated`之后才能开始发送媒体数据。为避免`connect`建联成功到`session.updated`到达之间的空档期误推媒体，在`connect`之前对上行音频与视频轨道分别调用`enableSendMediaStream(trackType, false)`，将上行推流暂时关闭。WebSocket事件说明详见[客户端事件](/api-reference/real-time-multimodal/client-events)。

<Tabs>
  <Tab title="iOS">
    ```swift
    // 音频编解码配置
    let encCfg = AoqAudioCodecConfig()
    encCfg.codecType = .audioPCM; encCfg.sampleRate = 16000; encCfg.channel = 1
    engine.setAudioEncoderConfig(encCfg)
    engine.setAudioDecoderConfig(encCfg)
    // connect 前关闭媒体发送，待 session.updated 后再开启
    engine.enableSendMediaStream(.audio, enable: false)
    engine.enableSendMediaStream(.video, enable: false)
    // 建立连接
    let conn = AoqConnectConfig()
    conn.token = token; conn.sid = sid; conn.certFingerprint = cert
    conn.relayEndpoints = endpoints; conn.workspaceIdHash = workspaceIdHash
    let aTrack = AoqTrackParam(); aTrack.trackType = .audio
    let vTrack = AoqTrackParam(); vTrack.trackType = .video
    let dTrack = AoqTrackParam(); dTrack.trackType = .data
    conn.publishTracks   = [aTrack, vTrack, dTrack]
    conn.subscribeTracks = [aTrack, dTrack]
    engine.connect(conn)
    ```
  </Tab>

  <Tab title="Android">
    ```java
    // 音频编解码配置
    AoqAudioCodecConfig encCfg = new AoqAudioCodecConfig();
    encCfg.codecType = AoqEncoderType.AoqEncoderTypeAudioPCM;
    encCfg.sampleRate = 16000; encCfg.channel = 1;
    engine.setAudioEncoderConfig(encCfg);
    engine.setAudioDecoderConfig(encCfg);
    // connect 前关闭媒体发送，待 session.updated 后再开启
    engine.enableSendMediaStream(AoqTrackType.AoqTrackTypeAudio, false);
    engine.enableSendMediaStream(AoqTrackType.AoqTrackTypeVideo, false);
    // 建立连接
    AoqConnectConfig conn = new AoqConnectConfig();
    conn.token = token; conn.sid = sid; conn.certFingerprint = cert;
    conn.relayEndpoints.addAll(endpoints); conn.workspaceIdHash = workspaceIdHash;
    AoqTrackParam aTrack = new AoqTrackParam(); aTrack.trackType = AoqTrackType.AoqTrackTypeAudio;
    AoqTrackParam vTrack = new AoqTrackParam(); vTrack.trackType = AoqTrackType.AoqTrackTypeVideo;
    AoqTrackParam dTrack = new AoqTrackParam(); dTrack.trackType = AoqTrackType.AoqTrackTypeData;
    conn.publishTracks.add(aTrack);
    conn.publishTracks.add(vTrack);
    conn.publishTracks.add(dTrack);
    conn.subscribeTracks.add(aTrack);
    conn.subscribeTracks.add(dTrack);
    engine.connect(conn);
    ```
  </Tab>

  <Tab title="HarmonyOS">
    ```typescript
    // 音频编解码配置
    const encCfg: AoqAudioCodecConfig = {
      codecType: AoqEncoderType.AoqEncoderTypeAudioPCM,
      sampleRate: 16000, channel: 1
    };
    engine.setAudioEncoderConfig(encCfg);
    engine.setAudioDecoderConfig(encCfg);
    // connect 前关闭媒体发送，待 session.updated 后再开启
    engine.enableSendMediaStream(AoqTrackType.AoqTrackTypeAudio, false);
    engine.enableSendMediaStream(AoqTrackType.AoqTrackTypeVideo, false);
    // 建立连接
    const conn: AoqConnectConfig = {
      token, sid, certFingerprint: cert,
      relayEndpoints: endpoints,
      workspaceIdHash,
      publishTracks: [
        { trackType: AoqTrackType.AoqTrackTypeAudio },
        { trackType: AoqTrackType.AoqTrackTypeVideo },
        { trackType: AoqTrackType.AoqTrackTypeData }
      ],
      subscribeTracks: [
        { trackType: AoqTrackType.AoqTrackTypeAudio },
        { trackType: AoqTrackType.AoqTrackTypeData }
      ]
    };
    engine.connect(conn);
    ```
  </Tab>
</Tabs>

<Warning>
  AOQ SDK 在建联后会默认发送媒体数据，此示例演示了连接模型时关闭媒体发送的能力。
</Warning>

### 配置 AI 会话

在`onConnectionStatusChange(Connected)`回调中通过`sendDataMsg`发送`session.update`消息（业务自定义 JSON，包含 modalities、voice、instructions、turn\_detection 等会话参数），完成会话握手，WebSocket事件说明详见[客户端事件](/api-reference/real-time-multimodal/client-events)。

<Tabs>
  <Tab title="iOS">
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
                // VAD类型，取值为server_vad或semantic_vad。使用qwen3.5-omni-realtime模型时推荐设为semantic_vad。
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
  </Tab>

  <Tab title="Android">
    ```java
    @Override
    public void onConnectionStatusChange(AoqConnectionStatus status) {
      if (status == AoqConnectionStatus.AoqConnectionStatusConnected) {
        sendSessionUpdate();
      }
    }
    private void sendSessionUpdate() {
      String sessionUpdateJson = /* 与 Swift 示例中相同的 session.update JSON */;
      AoqDataMsg msg = new AoqDataMsg();
      msg.data = sessionUpdateJson.getBytes(StandardCharsets.UTF_8);
      engine.sendDataMsg(msg);
    }
    ```
  </Tab>

  <Tab title="HarmonyOS">
    ```typescript
    onConnectionStatusChange(status: AoqConnectionStatus): void {
      if (status === AoqConnectionStatus.AoqConnectionStatusConnected) {
        this.sendSessionUpdate();
      }
    }
    private sendSessionUpdate(): void {
      const sessionUpdateJson = /* 与 Swift 示例中相同的 session.update JSON */;
      const msg: AoqDataMsg = { data: new TextEncoder().encode(sessionUpdateJson).buffer };
      this.engine.sendDataMsg(msg);
    }
    ```
  </Tab>
</Tabs>

### 收到 session.updated 后开启媒体发送

在`onDataMsg`回调中解析下行消息，收到模型回复`session.updated`的时候，对上一步禁推的每个轨道类型调用`enableSendMediaStream(trackType, true)`放开推流。下面为代码示例，WebSocket事件说明详见[服务端事件](/api-reference/real-time-multimodal/server-events)。

<Tabs>
  <Tab title="iOS">
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
  </Tab>

  <Tab title="Android">
    ```java
    @Override
    public void onDataMsg(AoqDataMsg msg) {
      if (msg == null || msg.data == null) return;
      try {
        JSONObject obj = new JSONObject(new String(msg.data, StandardCharsets.UTF_8));
        if ("session.updated".equals(obj.optString("type"))) {
          engine.enableSendMediaStream(AoqTrackType.AoqTrackTypeAudio, true);
          engine.enableSendMediaStream(AoqTrackType.AoqTrackTypeVideo, true);
        }
      } catch (JSONException ignored) {}
    }
    ```
  </Tab>

  <Tab title="HarmonyOS">
    ```typescript
    onDataMsg(msg: AoqDataMsg): void {
      if (!msg?.data) return;
      try {
        const text = new TextDecoder('utf-8').decode(new Uint8Array(msg.data));
        const obj = JSON.parse(text) as { type?: string };
        if (obj.type === 'session.updated') {
          this.engine.enableSendMediaStream(AoqTrackType.AoqTrackTypeAudio, true);
          this.engine.enableSendMediaStream(AoqTrackType.AoqTrackTypeVideo, true);
        }
      } catch (_) { /* 非 JSON，忽略 */ }
    }
    ```
  </Tab>
</Tabs>

<Warning>
  1. 模型必须在收到`session.updated`后才开启媒体流发送，否则 AI 侧可能还未准备好接收数据。
  2. 建连时添加的音频轨道和视频轨道（即 AOQ 媒体通道）会自动将数据传输到服务端。
     - 音频：通过音频轨道直接传输，无需发送`input_audio_buffer.append`事件。
     - 视频：通过视频轨道发送画面帧，无需发送`input_image_buffer.append`事件。
</Warning>

### 断开连接与销毁引擎

```swift
engine.disconnect()
AoqClientEngine.destroy()
```

## 典型场景

### 打断（Barge-in）

- SDK 与千问AI平台深度融合，支持千问AI平台模型的打断消息会在新一轮对话开始时打断上一轮次。
- SDK 提供**本地播放器打断**接口`interruptAudioPlayer`，当用户主动需要停止时可以调用打断 API 实现此功能。

```swift
// iOS
engine.interruptAudioPlayer(.audio, fadeMs: 100)
```

### 静音 / 取消静音

静音后 SDK 仍在采集音频，但只推送静音帧，`session`不会中断。

```swift
engine.muteAudioCapture(true);   // 静音麦克风（采集仍在跑，但只送静音帧）
engine.muteAudioCapture(false);  // 恢复
```

### 切换前后摄像头

```typescript
// 传入期望切换到的方向枚举即可
engine.switchCamera(AoqCameraDirection.AoqCameraDirectionFront);
engine.switchCamera(AoqCameraDirection.AoqCameraDirectionBack);
```

### 通话字幕与ASR结果显示

服务端通过下行数据消息推送 ASR 结果与 AI 文本回复。业务侧在`onDataMsg`回调中根据`type`字段分流即可。WebSocket事件说明详见[服务端事件](/api-reference/real-time-multimodal/server-events)。

## 注意事项

1. **单例语义**：`createEngine`是单例，重复调用返回同一实例；`destroy`后才能重新创建。多页面共用建议在 Application/Ability 级管理引擎生命周期。

2. **本地预览 View 类型**：
   - Android：`SurfaceView`或`TextureView`；其它类型不支持。
   - iOS：任意`UIView`子类。
   - HarmonyOS：请参考 SDK 文档。

3. **音频路由变化**：耳机插拔、蓝牙连接等会触发`onAudioDeviceRouteChanged`，业务侧通常无需处理；如果 UI 上显示"扬声器/听筒"开关，需要根据该回调同步状态。

4. **后台续传**：如需通话切到后台后继续传音频，`Info.plist`必须开启`UIBackgroundModes = audio`，并在前台时正确激活`AVAudioSession`（SDK 会处理大部分情况，业务侧用`setAudioSessionRestriction:`可精细控制是否让 SDK 接管）。

## Demo 示例下载

![image](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/images/p1087917.png)

示例源码下载：

**iOS：**[aoqdemo.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260715/grpnos/aoqdemo.zip)

## 相关文档

- AOQ Client SDK 详细 API：[AOQ SDK简介](/developer-guides/realtime-api/aoq-sdk-intro)
- qwen3.5-omni-plus-realtime 模型客户端事件：[客户端事件](/api-reference/real-time-multimodal/client-events)
- qwen3.5-omni-plus-realtime 模型服务端事件：[服务端事件](/api-reference/real-time-multimodal/server-events)
