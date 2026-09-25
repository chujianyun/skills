> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 使用 AOQ 接入 Qwen-Audio 实现实时语音对话

> 通过 AOQ 接入 qwen-audio-3.0-realtime-plus，使用服务端 VAD 自动划分轮次，实现低延迟的实时语音对话。客户端代码以 Android Java 为例。

## 方案概述

Qwen-Audio 是端到端实时语音交互模型，适用于语音助手、智能客服和 AI 伴侣等需要低延迟语音交互的场景。AOQ SDK 将音频与事件分轨传输：Audio 轨负责上行麦克风 PCM 和下行模型 PCM，Data 轨负责 Realtime 协议事件。

本教程使用 server\_vad：客户端持续上行音频，服务端自动识别用户开始和停止说话，并触发模型回复。

## 准备工作

1. 开通千问AI平台，并按[获取与配置 API Key](/api-reference/preparation/api-key)获取 API Key。API Key 只保存在业务 AppServer，不要写入客户端代码或提交到代码仓库。
2. 根据业务部署地域确认 AOQ Endpoint。地域和接入地址的选择方法请参见[选择地域、服务部署范围和接入域名](/developer-guides/realtime-api/overview)。
3. 按 [SDK 下载](/developer-guides/realtime-api/sdk-download)下载 AOQ Client SDK v1.1.0。
4. 搭建业务 AppServer，并按 [Token 鉴权](/developer-guides/realtime-api/token-auth)实现服务端代理鉴权。每次建立新连接前，客户端都应从 AppServer 获取新的连接凭证。

### 导入 SDK

根据开发平台导入对应 SDK。后续客户端代码以 Android Java 为例，其他平台使用相同的接口设计和事件流程。本文以 PCM 音频流为例。Opus 编码由插件提供；如果需要使用 Opus 编码上行，请导入 Opus 插件。

<Tabs>
  <Tab title="Android">
    1. 将 AoqClientSdk-v1.1.0.aar 放入 app/libs，并在 app/build.gradle 中配置依赖和 SDK 支持的 ABI：

    ```groovy
    android {
      defaultConfig {
        minSdk 21
        ndk { abiFilters 'armeabi-v7a', 'arm64-v8a' }
      }
    }
    dependencies {
      implementation fileTree(dir: 'libs', include: ['*.aar'])
    }
    ```

    2. 在 AndroidManifest.xml 中声明以下权限：

    ```xml
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />
    ```

    3. 在使用相应设备前动态申请 RECORD\_AUDIO 权限。
  </Tab>

  <Tab title="iOS">
    1. 将 AoqClientSdk.framework 拖入 Xcode 工程，在 Target > General > Frameworks, Libraries, and Embedded Content 中选择 Embed & Sign。SDK 支持 iOS 13.0 及以上 arm64 设备。
    2. 在 Info.plist 中添加 NSMicrophoneUsageDescription，并在使用相应设备前请求用户授权。
    3. Swift 工程使用 `import AoqClientSdk`；Objective-C 工程使用 `#import <AoqClientSdk/AoqClientSdk.h>`。
  </Tab>

  <Tab title="HarmonyOS">
    1. 将 AoqClientSdk-v1.1.0.har 放入 entry/libs，并在 entry/oh-package.json5 中声明依赖。该 SDK 兼容 API 12，支持 arm64-v8a：

    ```json
    {
      "dependencies": {
        "@aoq/client-sdk": "file:./libs/AoqClientSdk-v1.1.0.har"
      }
    }
    ```

    2. 在 entry/src/main/module.json5 中声明以下权限：

    ```json
    "requestPermissions": [
      { "name": "ohos.permission.INTERNET" },
      { "name": "ohos.permission.MICROPHONE",
        "reason": "$string:perm_mic_reason",
        "usedScene": { "abilities": ["EntryAbility"], "when": "inuse" } }
    ]
    ```

    3. 在使用相应设备前调用 `abilityAccessCtrl.createAtManager().requestPermissionsFromUser` 申请 `ohos.permission.MICROPHONE`。
  </Tab>

  <Tab title="Linux (Python)">
    1. 解压 SDK，并保持 aoq\_client\_sdk.py、libAoqClientSdk.so 和 libonnxruntime.so.1.16.3 位于同一目录。
    2. 将 SDK 目录加入 Python 和动态库搜索路径：

    ```bash
    export PYTHONPATH="$PWD/AoqClientSdk:$PYTHONPATH"
    export LD_LIBRARY_PATH="$PWD/AoqClientSdk:$LD_LIBRARY_PATH"
    ```

    3. 在 Python 代码中使用 `import aoq_client_sdk`。也可通过 `AOQ_CLIENT_SDK_LIB` 指定 libAoqClientSdk.so 的绝对路径。
  </Tab>
</Tabs>

## 实现流程

1. AppServer 通过 Realtime Token 地址获取 qwen-audio-3.0-realtime-plus 的本次 AOQ 连接凭证。
2. 客户端根据接入模型和业务音频格式配置 SDK 的上行编码与下行解码参数。
3. 客户端初始化录音和播放设备，创建 AoqConnectConfig，将本次连接凭证写入对应字段，并配置需要发布和订阅的 Audio、Data 轨。保持 Audio 轨发送关闭，调用 connect 建立 AOQ 连接。
4. 连接成功后发送 session.update；收到 session.updated 后才开启 Audio 轨发送。
5. 服务端 VAD 自动划分轮次，模型音频通过 Audio 轨自动播放，Data 轨持续返回对话事件。
6. 结束使用时断开连接并销毁引擎，SDK 会自动关闭音频设备。

![AOQ 实时语音对话时序图](http://icms-x-dita-hz.oss-cn-hangzhou.aliyuncs.com/zh-CN/images/p1094861.png)

## AppServer 获取 Token

在 AppServer 设置 DASHSCOPE\_API\_KEY，并使用所选地域的 Endpoint 发送请求。`clientIp` 为客户端的真实公网 IP；该字段可选，但建议传入，以便服务分配合适的 Relay 接入点。

```bash
curl -X POST \
  "https://{endpoint}/api/v1/webrtc/realtime?model=qwen-audio-3.0-realtime-plus" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  -H "x-dashscope-rtc-transport: moq" \
  -d "{\"clientIp\": \"${CLIENT_REAL_IP}\"}"
```

<Note>
  如果 AppServer 无法获取客户端真实公网 IP，请删除 clientIp 字段，不要传空字符串。
</Note>

AppServer 将响应中的以下字段返回客户端。AOQ Token 仅供一次连接使用，客户端每次调用 connect 前都必须重新请求，不能缓存或复用。生产环境中不要把 API Key 返回客户端。完整请求和响应字段请参见 [Token 鉴权](/developer-guides/realtime-api/token-auth)。

| 响应字段                       | SDK 字段                           |
| -------------------------- | -------------------------------- |
| aoqTokenForClient          | AoqConnectConfig.token           |
| sid                        | AoqConnectConfig.sid             |
| clientRelayCertFingerprint | AoqConnectConfig.certFingerprint |
| clientRelayEndpoints       | AoqConnectConfig.relayEndpoints  |
| extraInfo.workspaceIdHash  | AoqConnectConfig.workspaceIdHash |

## 实现 Android 客户端

每次建立连接前，客户端先从 AppServer 获取新的连接凭证，再创建 AoqConnectConfig：映射 Token 响应字段，并补充发布和订阅轨道等客户端连接参数。按以下步骤实现 Android 端实时语音对话。

### 1. 创建引擎并设置回调

创建 AOQ 单例引擎并注册事件回调。在连接成功时配置会话，并把服务端事件分发给 UI 和业务状态机。

```java
AoqClientListener listener = new AoqClientListener() {
    @Override
    public void onConnectionStatusChange(AoqClientEngine.AoqConnectionStatus status) {
        if (status == AoqClientEngine.AoqConnectionStatus.AoqConnectionStatusConnected) {
            configureSession();
        }
    }
    @Override
    public void onDataMsg(AoqClientEngine.AoqDataMsg msg) {
        handleServerEvent(msg);
    }
};
AoqClientEngine.AoqCreateConfig createConfig = new AoqClientEngine.AoqCreateConfig();
createConfig.workDir = context.getFilesDir().getAbsolutePath();
engine = AoqClientEngine.createEngine(context, createConfig, listener);
```

### 2. 配置音频编解码

根据接入模型和业务音频格式配置 SDK 的上行编码与下行解码参数。以下数值仅为本教程的 PCM 示例配置，不限制业务音频格式。

```java
AoqClientEngine.AoqAudioCodecConfig audioEncoderConfig =
        new AoqClientEngine.AoqAudioCodecConfig();
audioEncoderConfig.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeAudio;
audioEncoderConfig.codecType = AoqClientEngine.AoqEncoderType.AoqEncoderTypeAudioPCM;
audioEncoderConfig.sampleRate = 16000;
audioEncoderConfig.channel = 1;
engine.setAudioEncoderConfig(audioEncoderConfig);
AoqClientEngine.AoqAudioCodecConfig audioDecoderConfig =
        new AoqClientEngine.AoqAudioCodecConfig();
audioDecoderConfig.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeAudio;
audioDecoderConfig.codecType = AoqClientEngine.AoqEncoderType.AoqEncoderTypeAudioPCM;
audioDecoderConfig.sampleRate = 24000;
audioDecoderConfig.channel = 1;
engine.setAudioDecoderConfig(audioDecoderConfig);
```

### 3. 配置轨道并建立连接

使用 SDK 接口启动音频采集与播放。将本次 AppServer Token 响应映射到 AoqConnectConfig 的凭证字段，并在 publishTracks 和 subscribeTracks 中分别配置 Audio 和 Data 轨。保持 Audio 轨发送关闭，调用 connect 建立连接；后续收到 session.updated 后再开启发送。

```java
AoqClientEngine.AoqAudioCaptureConfig captureConfig =
        new AoqClientEngine.AoqAudioCaptureConfig();
captureConfig.channel = 1;
captureConfig.isVoipMode = true;
engine.startAudioCapture(captureConfig);
AoqClientEngine.AoqAudioPlaybackConfig playbackConfig =
        new AoqClientEngine.AoqAudioPlaybackConfig();
playbackConfig.channel = 1;
playbackConfig.isVoipMode = true;
playbackConfig.isDefaultSpeaker = true;
engine.startAudioPlayer(playbackConfig);
AoqClientEngine.AoqTrackParam publishAudioTrack = new AoqClientEngine.AoqTrackParam();
publishAudioTrack.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeAudio;
publishAudioTrack.trackMode = AoqClientEngine.AoqTrackMode.AoqTrackModeStream;
connectConfig.publishTracks.add(publishAudioTrack);
AoqClientEngine.AoqTrackParam publishDataTrack = new AoqClientEngine.AoqTrackParam();
publishDataTrack.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeData;
publishDataTrack.trackMode = AoqClientEngine.AoqTrackMode.AoqTrackModeSegment;
connectConfig.publishTracks.add(publishDataTrack);
AoqClientEngine.AoqTrackParam subscribeAudioTrack = new AoqClientEngine.AoqTrackParam();
subscribeAudioTrack.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeAudio;
subscribeAudioTrack.trackMode = AoqClientEngine.AoqTrackMode.AoqTrackModeStream;
connectConfig.subscribeTracks.add(subscribeAudioTrack);
AoqClientEngine.AoqTrackParam subscribeDataTrack = new AoqClientEngine.AoqTrackParam();
subscribeDataTrack.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeData;
subscribeDataTrack.trackMode = AoqClientEngine.AoqTrackMode.AoqTrackModeSegment;
connectConfig.subscribeTracks.add(subscribeDataTrack);
engine.enableSendMediaStream(
        AoqClientEngine.AoqTrackType.AoqTrackTypeAudio, false);
engine.connect(connectConfig);
```

### 4. 发送 session.update

连接成功后配置输出模态、音色、音频格式、系统指令和 VAD。input\_audio\_format 与 output\_audio\_format 的值均为 pcm；实际采样率由 SDK 编解码配置确定。完整参数请参见[客户端事件](/api-reference/qwen-audio-realtime/client-events)。

```java
JSONObject vad = new JSONObject()
        .put("type", "server_vad")
        .put("threshold", 0.5)
        .put("silence_duration_ms", 800);
JSONObject session = new JSONObject()
        .put("modalities", new JSONArray().put("text").put("audio"))
        .put("voice", "longanqian")
        .put("input_audio_format", "pcm")
        .put("output_audio_format", "pcm")
        .put("instructions", "You are a helpful voice assistant.")
        .put("turn_detection", vad);
JSONObject sessionUpdate = new JSONObject()
        .put("type", "session.update")
        .put("session", session);
AoqClientEngine.AoqDataMsg dataMessage = new AoqClientEngine.AoqDataMsg();
dataMessage.data = sessionUpdate.toString().getBytes(StandardCharsets.UTF_8);
engine.sendDataMsg(dataMessage);
```

### 5. 收到 session.updated 后开启上行

收到 session.updated 表示会话配置已生效，此时才开启 Audio 轨发送，确保此前采集的音频不会提前进入模型输入。

```java
if ("session.updated".equals(type)) {
    engine.enableSendMediaStream(
            AoqClientEngine.AoqTrackType.AoqTrackTypeAudio, true);
}
```

### 6. 处理服务端事件

在 onDataMsg 中按 `type` 展示用户和模型文本，并处理错误。完整事件字段请参见[服务端事件](/api-reference/qwen-audio-realtime/server-events)。

```java
if ("response.audio_transcript.delta".equals(type)) {
    String delta = event.optString("delta");
    // 将模型回复的文本增量展示在 UI 中。
} else if ("conversation.item.input_audio_transcription.completed".equals(type)) {
    String transcript = event.optString("transcript");
    // 将用户语音的最终转写结果展示在 UI 中。
} else if ("error".equals(type)) {
    // 读取错误字段并更新应用状态。
}
```

### 7. 断开连接并销毁引擎

结束通话时断开连接并销毁单例引擎。`disconnect` 或 `destroy` 会自动关闭音频采集与播放，无需额外调用停止设备的接口。

```java
engine.disconnect();
AoqClientEngine.destroy();
```

## 主要服务端事件

Data 轨事件以 `type` 标识，客户端需要处理以下关键事件。完整事件结构请参见[服务端事件](/api-reference/qwen-audio-realtime/server-events)。

| 事件                                                      | 说明                |
| ------------------------------------------------------- | ----------------- |
| session.created                                         | 会话已创建并返回默认配置      |
| session.updated                                         | 客户端配置已生效，可以开启音频上行 |
| input\_audio\_buffer.speech\_started                    | 检测到用户开始说话         |
| input\_audio\_buffer.speech\_stopped                    | 检测到用户停止说话         |
| input\_audio\_buffer.committed                          | 本轮音频已提交           |
| response.created                                        | 模型开始生成回复          |
| response.audio\_transcript.delta                        | 模型回复文本增量          |
| conversation.item.input\_audio\_transcription.completed | 用户语音转写完成          |
| response.done                                           | 本轮回复结束            |
| error                                                   | 服务端错误             |

## 完整示例

以下类接收已填入本次 AppServer 连接凭证的 AoqConnectConfig，并在类内补充音频设备和发布、订阅轨道配置。每次重新连接都必须获取新的凭证并创建连接配置。生产代码还需补充权限、UI 状态和连接重试。

```java
import android.content.Context;
import com.alibaba.aoq.clientsdk.AoqClientEngine;
import com.alibaba.aoq.clientsdk.AoqClientListener;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import java.nio.charset.StandardCharsets;
public final class RealtimeVoiceChatClient {
    private AoqClientEngine engine;
    public RealtimeVoiceChatClient(Context context, AoqClientEngine.AoqConnectConfig connectConfig) {
        AoqClientListener listener = new AoqClientListener() {
            @Override
            public void onConnectionStatusChange(AoqClientEngine.AoqConnectionStatus status) {
                if (status == AoqClientEngine.AoqConnectionStatus.AoqConnectionStatusConnected) {
                    configureSession();
                }
            }
            @Override
            public void onDataMsg(AoqClientEngine.AoqDataMsg msg) {
                try {
                    JSONObject event = new JSONObject(
                            new String(msg.data, StandardCharsets.UTF_8));
                    String type = event.optString("type");
                    if ("session.updated".equals(type)) {
                        engine.enableSendMediaStream(
                                AoqClientEngine.AoqTrackType.AoqTrackTypeAudio, true);
                    } else if ("response.audio_transcript.delta".equals(type)) {
                        String delta = event.optString("delta");
                        // 将 delta 展示在 UI 中。
                    } else if ("conversation.item.input_audio_transcription.completed".equals(type)) {
                        String transcript = event.optString("transcript");
                        // 将 transcript 展示在 UI 中。
                    } else if ("error".equals(type)) {
                        // 读取错误字段并更新应用状态。
                    }
                } catch (JSONException e) {
                    throw new IllegalArgumentException("Invalid server event", e);
                }
            }
        };
        AoqClientEngine.AoqCreateConfig createConfig = new AoqClientEngine.AoqCreateConfig();
        createConfig.workDir = context.getFilesDir().getAbsolutePath();
        engine = AoqClientEngine.createEngine(context, createConfig, listener);
        AoqClientEngine.AoqAudioCodecConfig audioEncoderConfig =
                new AoqClientEngine.AoqAudioCodecConfig();
        audioEncoderConfig.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeAudio;
        audioEncoderConfig.codecType = AoqClientEngine.AoqEncoderType.AoqEncoderTypeAudioPCM;
        audioEncoderConfig.sampleRate = 16000;
        audioEncoderConfig.channel = 1;
        engine.setAudioEncoderConfig(audioEncoderConfig);
        AoqClientEngine.AoqAudioCodecConfig audioDecoderConfig =
                new AoqClientEngine.AoqAudioCodecConfig();
        audioDecoderConfig.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeAudio;
        audioDecoderConfig.codecType = AoqClientEngine.AoqEncoderType.AoqEncoderTypeAudioPCM;
        audioDecoderConfig.sampleRate = 24000;
        audioDecoderConfig.channel = 1;
        engine.setAudioDecoderConfig(audioDecoderConfig);
        AoqClientEngine.AoqAudioCaptureConfig captureConfig =
                new AoqClientEngine.AoqAudioCaptureConfig();
        captureConfig.channel = 1;
        captureConfig.isVoipMode = true;
        engine.startAudioCapture(captureConfig);
        AoqClientEngine.AoqAudioPlaybackConfig playbackConfig =
                new AoqClientEngine.AoqAudioPlaybackConfig();
        playbackConfig.channel = 1;
        playbackConfig.isVoipMode = true;
        playbackConfig.isDefaultSpeaker = true;
        engine.startAudioPlayer(playbackConfig);
        AoqClientEngine.AoqTrackParam publishAudioTrack =
                new AoqClientEngine.AoqTrackParam();
        publishAudioTrack.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeAudio;
        publishAudioTrack.trackMode = AoqClientEngine.AoqTrackMode.AoqTrackModeStream;
        connectConfig.publishTracks.add(publishAudioTrack);
        AoqClientEngine.AoqTrackParam publishDataTrack =
                new AoqClientEngine.AoqTrackParam();
        publishDataTrack.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeData;
        publishDataTrack.trackMode = AoqClientEngine.AoqTrackMode.AoqTrackModeSegment;
        connectConfig.publishTracks.add(publishDataTrack);
        AoqClientEngine.AoqTrackParam subscribeAudioTrack =
                new AoqClientEngine.AoqTrackParam();
        subscribeAudioTrack.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeAudio;
        subscribeAudioTrack.trackMode = AoqClientEngine.AoqTrackMode.AoqTrackModeStream;
        connectConfig.subscribeTracks.add(subscribeAudioTrack);
        AoqClientEngine.AoqTrackParam subscribeDataTrack =
                new AoqClientEngine.AoqTrackParam();
        subscribeDataTrack.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeData;
        subscribeDataTrack.trackMode = AoqClientEngine.AoqTrackMode.AoqTrackModeSegment;
        connectConfig.subscribeTracks.add(subscribeDataTrack);
        engine.enableSendMediaStream(AoqClientEngine.AoqTrackType.AoqTrackTypeAudio, false);
        engine.connect(connectConfig);
    }
    private void configureSession() {
        try {
            JSONObject vad = new JSONObject()
                    .put("type", "server_vad")
                    .put("threshold", 0.5)
                    .put("silence_duration_ms", 800);
            JSONObject session = new JSONObject()
                    .put("modalities", new JSONArray().put("text").put("audio"))
                    .put("voice", "longanqian")
                    .put("input_audio_format", "pcm")
                    .put("output_audio_format", "pcm")
                    .put("turn_detection", vad);
            JSONObject sessionUpdate = new JSONObject()
                    .put("type", "session.update")
                    .put("session", session);
            AoqClientEngine.AoqDataMsg dataMessage = new AoqClientEngine.AoqDataMsg();
            dataMessage.data = sessionUpdate.toString().getBytes(StandardCharsets.UTF_8);
            engine.sendDataMsg(dataMessage);
        } catch (JSONException e) {
            throw new IllegalStateException("Failed to create session.update", e);
        }
    }
    public void close() {
        engine.disconnect();
        AoqClientEngine.destroy();
    }
}
```

## 运行并验证

1. 收到 session.updated 后才开始上行麦克风音频。
2. 用户停止说话后，服务端自动提交音频并开始回复；文本事件与 Audio 轨音频连续返回。

## 典型场景

### 切换交互模式

server\_vad 适合按静音时长判停；smart\_turn 结合声学与语义判断轮次；按键模式将 turn\_detection 设为 null。turn\_detection 只能在首次发送音频前修改，切换模式时应重新建立会话。

### 切换音色

在首次 session.update 中设置 `session.voice`。不同模型支持的系统音色可能不同；支持的音色与声音复刻用法请参见[实时语音对话（Qwen-Audio-Realtime）](/developer-guides/speech/qwen-audio-realtime)。

### 扬声器或听筒

通过 `AoqAudioPlaybackConfig.isDefaultSpeaker` 设置默认输出设备，运行中可调用 `enableSpeakerphone` 切换。

### Android 后台通话

Android 10 及以上版本如需在后台继续采集和播放，应使用 `foregroundServiceType="microphone|mediaPlayback"` 的前台服务，并在应用仍对用户可见时启动。

## 常见问题

| 问题        | 处理方法                                                            |
| --------- | --------------------------------------------------------------- |
| 连接失败      | 确认 Token 未过期、Endpoint 与部署地域一致，并检查 AoqConnectConfig 字段映射。        |
| 会话已建立但无回复 | 确认收到 session.updated 后已开启 Audio 轨，并检查 SDK 上行编码配置是否与模型和业务音频格式一致。 |
| 回复没有声音    | 确认已订阅 Audio 轨并启动音频播放器，然后检查 SDK 下行解码配置是否与模型输出音频格式一致。             |

## 相关文档

- [获取与配置 API Key](/api-reference/preparation/api-key)
- [选择地域、服务部署范围和接入域名](/developer-guides/realtime-api/overview)
- [AOQ Client SDK 简介](/developer-guides/realtime-api/aoq-sdk-intro)
- [SDK 下载](/developer-guides/realtime-api/sdk-download)
- [Token 鉴权](/developer-guides/realtime-api/token-auth)
- [实时语音对话（Qwen-Audio-Realtime）](/developer-guides/speech/qwen-audio-realtime)
- [客户端事件](/api-reference/qwen-audio-realtime/client-events)
- [服务端事件](/api-reference/qwen-audio-realtime/server-events)
