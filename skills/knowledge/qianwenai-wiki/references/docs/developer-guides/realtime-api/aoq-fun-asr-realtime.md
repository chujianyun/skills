> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 使用AOQ接入fun-asr-realtime实现实时语音识别

> 通过 AOQ 接入 fun-asr-realtime，发送麦克风音频并实时接收语音识别结果。客户端代码以 Android Java 为例，AOQ 支持的其他平台使用相同的接口。

## 方案概述

fun-asr-realtime 将音频流实时转写为带标点的文本。AOQ SDK 将媒体和事件分轨传输：客户端通过 Audio 轨上行音频，通过 Data 轨发送控制事件并接收识别事件。该模型使用 Inference 事件协议，而不是 Realtime 事件协议。

该方案适用于实时字幕、会议转写、语音输入和智能助手。Audio 轨避免客户端把音频编码成事件消息，Data 轨则保留 run-task、result-generated 和 finish-task 等完整任务语义。

1. 客户端向业务 AppServer 请求临时 AOQ 连接凭证。
2. AppServer 使用 API Key 向千问AI平台申请 Token，并把连接字段返回客户端。
3. 客户端建立 AOQ 连接并发送 run-task；收到 task-started 后开始上行麦克风音频。
4. 服务端持续返回 result-generated；客户端发送 finish-task 后等待最终结果和 task-finished。

## 准备工作

1. 开通千问AI平台，并按[获取与配置 API Key](/api-reference/preparation/api-key)获取 API Key。API Key 只保存在业务 AppServer，不要写入客户端代码或提交到代码仓库。
2. 根据业务部署地域确认 AOQ Endpoint。地域和接入地址的选择方法请参见[选择地域、服务部署范围和接入域名](/developer-guides/realtime-api/overview)。
3. 按[SDK 下载](/developer-guides/realtime-api/sdk-download)下载 AOQ Client SDK v1.1.0。本文传输 PCM 音频，不需要额外集成 Opus 插件。
4. 搭建业务 AppServer，并按[Token 鉴权](/developer-guides/realtime-api/token-auth)实现 AOQ Inference 协议的服务端代理鉴权。每次建立新连接前，客户端都应从 AppServer 获取新的连接凭证。

### 导入 SDK

根据开发平台选择相应的 SDK 导入方式。后续客户端实现以 Android Java 为例；其他平台使用相同的接口设计和事件流程。

<Tabs>
  <Tab title="Android">
    1. 将 AoqClientSdk-v1.1.0.aar 放入 app/libs 目录，并在 app/build.gradle 中配置依赖和 ABI：

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

    2. 在 AndroidManifest.xml 中声明网络和录音权限：

    ```xml
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />
    ```

    3. 在开始录音前动态申请 RECORD\_AUDIO 权限。纯语音识别不需要 CAMERA 权限。
  </Tab>

  <Tab title="iOS">
    1. 将 AoqClientSdk.framework 拖入 Xcode 工程，在 Target > General > Frameworks, Libraries, and Embedded Content 中选择 Embed & Sign。SDK 支持 iOS 13.0 及以上 arm64 设备。
    2. 在 Info.plist 中添加 NSMicrophoneUsageDescription。纯语音识别不需要 NSCameraUsageDescription。
    3. Swift 工程使用 import AoqClientSdk；Objective-C 工程使用 #import \<AoqClientSdk/AoqClientSdk.h>。
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

    2. 在 entry/src/main/module.json5 中声明网络和麦克风权限：

    ```json
    "requestPermissions": [
      { "name": "ohos.permission.INTERNET" },
      {
        "name": "ohos.permission.MICROPHONE",
        "reason": "$string:perm_mic_reason",
        "usedScene": { "abilities": ["EntryAbility"], "when": "inuse" }
      }
    ]
    ```

    3. 在开始录音前调用 abilityAccessCtrl.createAtManager().requestPermissionsFromUser 申请麦克风权限。
  </Tab>

  <Tab title="Linux (Python)">
    1. 解压 SDK，并保持 aoq\_client\_sdk.py、libAoqClientSdk.so 和 libonnxruntime.so.1.16.3 位于同一目录。
    2. 将 SDK 目录加入 Python 和动态库搜索路径：

    ```bash
    export PYTHONPATH="$PWD/AoqClientSdk:$PYTHONPATH"
    export LD_LIBRARY_PATH="$PWD/AoqClientSdk:$LD_LIBRARY_PATH"
    ```

    3. 在 Python 代码中使用 import aoq\_client\_sdk。也可通过 AOQ\_CLIENT\_SDK\_LIB 指定 libAoqClientSdk.so 的绝对路径。
  </Tab>
</Tabs>

## 实现流程

1. AppServer 使用 Inference Token 地址获取 fun-asr-realtime 的 AOQ 连接参数。
2. 客户端把 Token 响应转换为 AoqConnectConfig，发布 Audio 和 Data 轨，并订阅 Data 轨。
3. 客户端按业务需求和模型要求配置音频编码参数，启动麦克风采集但暂不发送音频，然后建立 AOQ 连接。
4. 连接成功后发送 run-task；收到 task-started 后开启 Audio 轨发送。
5. 客户端在 onDataMsg 中处理 result-generated；结束录音时先关闭 Audio 轨发送，再发送 finish-task。
6. 收到 task-finished 后，可在同一连接上使用新的 task\_id 发起下一轮识别，或断开连接并销毁引擎。

![aoq-realtime-asr-sequence-zh](http://icms-x-dita-hz.oss-cn-hangzhou.aliyuncs.com/zh-CN/images/p1094760.png)

## AppServer 获取 Token

在 AppServer 设置 DASHSCOPE\_API\_KEY，并使用所选地域的 Endpoint 发送请求。clientIp 为终端的真实公网 IP；该字段可选，但建议传入，以便服务分配合适的 Relay 接入点。

```bash
curl -X POST \
  "https://{endpoint}/api/v1/webrtc/inference?model=fun-asr-realtime" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  -H "x-dashscope-rtc-transport: moq" \
  -d "{\"clientIp\": \"${CLIENT_REAL_IP}\"}"
```

<Note>
  如果 AppServer 无法获取终端真实公网 IP，请从请求体中删除 clientIp 字段，不要传空字符串。
</Note>

AppServer 将响应中的以下字段返回客户端。生产环境中不要把 API Key 返回客户端。完整请求参数和响应字段请参见[Token 鉴权](/developer-guides/realtime-api/token-auth)。

| **响应字段**                   | **SDK 字段**                       |
| -------------------------- | -------------------------------- |
| aoqTokenForClient          | AoqConnectConfig.token           |
| sid                        | AoqConnectConfig.sid             |
| clientRelayCertFingerprint | AoqConnectConfig.certFingerprint |
| clientRelayEndpoints       | AoqConnectConfig.relayEndpoints  |
| extraInfo.workspaceIdHash  | AoqConnectConfig.workspaceIdHash |

## 实现 Android 客户端

以下步骤按连接和任务的实际执行顺序拆分 Android Java 客户端代码。各片段来自后文的完整示例。

### 1. 创建引擎并设置回调

创建 AOQ 客户端引擎，并注册连接状态和 Data 轨事件回调。请根据业务逻辑实现回调处理；连接成功后再启动识别任务。

```java
AoqClientListener listener = new AoqClientListener() {
  @Override
  public void onConnectionStatusChange(AoqClientEngine.AoqConnectionStatus status) {
    connected = status == AoqClientEngine.AoqConnectionStatus
            .AoqConnectionStatusConnected;
    if (connected) {
      beginRecognition();
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

### 2. 配置音频编码

配置发送给模型的音频编码。请根据业务需求和模型要求设置格式、采样率和声道数。以下代码以 16 kHz 单声道 PCM 为例；支持范围请参见[客户端事件](/api-reference/qwen-audio-realtime/client-events)中的 run-task 参数。

```java
AoqClientEngine.AoqAudioCodecConfig encoder =
        new AoqClientEngine.AoqAudioCodecConfig();
encoder.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeAudio;
encoder.codecType = AoqClientEngine.AoqEncoderType.AoqEncoderTypeAudioPCM;
encoder.sampleRate = 16000;
encoder.channel = 1;
encoder.bitrate = 24000;
engine.setAudioEncoderConfig(encoder);
```

### 3. 配置连接和传输轨道

使用 AppServer 返回的凭证配置 AOQ 连接，并根据业务需要选择发布和订阅的轨道。以下代码为实时语音识别发布 Audio 和 Data 轨，并订阅 Data 轨。

```java
addTrack(connectConfig, true,
        AoqClientEngine.AoqTrackType.AoqTrackTypeAudio,
        AoqClientEngine.AoqTrackMode.AoqTrackModeStream);
addTrack(connectConfig, true,
        AoqClientEngine.AoqTrackType.AoqTrackTypeData,
        AoqClientEngine.AoqTrackMode.AoqTrackModeSegment);
addTrack(connectConfig, false,
        AoqClientEngine.AoqTrackType.AoqTrackTypeData,
        AoqClientEngine.AoqTrackMode.AoqTrackModeSegment);
```

### 4. 启动音频采集并建立连接

配置音频采集方式并建立 AOQ 连接。请根据业务选择内置或外部采集、是否启用 VoIP 模式以及声道数。收到 task-started 前保持 Audio 轨发送关闭。

```java
AoqClientEngine.AoqAudioCaptureConfig capture =
        new AoqClientEngine.AoqAudioCaptureConfig();
capture.isExternal = false;
capture.isVoipMode = true;
capture.channel = 1;
engine.startAudioCapture(capture);
// 收到 task-started 前不要发送音频。
engine.enableSendMediaStream(
        AoqClientEngine.AoqTrackType.AoqTrackTypeAudio, false);
engine.connect(connectConfig);
```

### 5. 启动识别任务

连接成功后生成任务 ID，并发送 run-task 启动识别。请根据实际使用的模型和音频输入配置 model、format、sample\_rate 及其他任务参数，完整说明请参见[客户端事件](/api-reference/qwen-audio-realtime/client-events)。

```java
taskId = UUID.randomUUID().toString();
JSONObject header = createHeader("run-task");
JSONObject parameters = new JSONObject()
        .put("format", "pcm")
        .put("sample_rate", 16000);
JSONObject payload = new JSONObject()
        .put("task_group", "audio")
        .put("task", "asr")
        .put("function", "recognition")
        .put("model", "fun-asr-realtime")
        .put("parameters", parameters)
        .put("input", new JSONObject());
send(new JSONObject().put("header", header).put("payload", payload));
```

### 6. 处理服务端事件

处理任务状态、识别结果和错误事件，并将结果传递给业务层。请根据应用的展示和状态管理需求实现回调逻辑；收到 task-started 后再发送音频，展示结果时过滤心跳事件。完整响应结构请参见[服务端事件](/api-reference/qwen-audio-realtime/server-events)。

```java
String eventName = header.optString("event", "");
if ("task-started".equals(eventName)) {
  taskStarted = true;
  engine.enableSendMediaStream(
          AoqClientEngine.AoqTrackType.AoqTrackTypeAudio, true);
} else if ("result-generated".equals(eventName)) {
  JSONObject payload = event.optJSONObject("payload");
  JSONObject output = payload == null ? null : payload.optJSONObject("output");
  JSONObject sentence = output == null ? null : output.optJSONObject("sentence");
  if (sentence != null && !sentence.optBoolean("heartbeat", false)) {
    String text = sentence.optString("text", "");
    if (!text.isEmpty()) {
      resultListener.onResult(
              text, sentence.optBoolean("sentence_end", false));
    }
  }
} else if ("task-finished".equals(eventName)) {
  resetTaskState();
  resultListener.onTaskFinished();
} else if ("task-failed".equals(eventName)) {
  String message = header.optString("error_message", "识别失败");
  resetTaskState();
  resultListener.onError(message);
}
```

### 7. 结束识别任务

用户结束本轮录音时，停止音频上行并发送 finish-task。保持连接直至收到最终识别结果和 task-finished；后续可按业务需要启动新任务或释放连接。事件格式请参见[客户端事件](/api-reference/qwen-audio-realtime/client-events)。

```java
engine.enableSendMediaStream(
        AoqClientEngine.AoqTrackType.AoqTrackTypeAudio, false);
JSONObject payload = new JSONObject().put("input", new JSONObject());
send(new JSONObject()
        .put("header", createHeader("finish-task"))
        .put("payload", payload));
```

### 8. 断开连接并销毁引擎

页面销毁或不再需要识别时，释放音频采集、AOQ 连接和引擎资源。请根据应用生命周期决定释放时机，不要在刚发送 finish-task 时立即释放。

```java
engine.enableSendMediaStream(
        AoqClientEngine.AoqTrackType.AoqTrackTypeAudio, false);
engine.stopAudioCapture();
engine.disconnect();
AoqClientEngine.destroy();
```

## 完整示例

该 Android Java 类将 AppServer 返回的 JSON 转换为 AoqConnectConfig，并组合前述连接、采集、任务和资源释放逻辑。代码基于 AOQ Android SDK v1.1.0。

<Accordion title="AsrClient.java 完整代码">
  ```java
  import android.content.Context;
  import com.alibaba.aoq.clientsdk.AoqClientEngine;
  import com.alibaba.aoq.clientsdk.AoqClientListener;
  import org.json.JSONArray;
  import org.json.JSONObject;
  import java.nio.charset.StandardCharsets;
  import java.util.UUID;
  public final class AsrClient {
    public interface ResultListener {
      void onResult(String text, boolean sentenceEnd);
      void onTaskFinished();
      void onError(String message);
    }
    private final AoqClientEngine engine;
    private final ResultListener resultListener;
    private String taskId;
    private boolean connected;
    private boolean taskStarted;
    public AsrClient(Context context, AoqClientEngine.AoqConnectConfig connectConfig,
                     ResultListener resultListener) {
      this.resultListener = resultListener;
      AoqClientListener listener = new AoqClientListener() {
        @Override
        public void onConnectionStatusChange(AoqClientEngine.AoqConnectionStatus status) {
          connected = status == AoqClientEngine.AoqConnectionStatus
                  .AoqConnectionStatusConnected;
          if (connected) {
            beginRecognition();
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
      configureAudioEncoder();
      configureTracks(connectConfig);
      startAudioCapture();
      engine.connect(connectConfig);
    }
    private void configureAudioEncoder() {
      AoqClientEngine.AoqAudioCodecConfig encoder = new AoqClientEngine.AoqAudioCodecConfig();
      encoder.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeAudio;
      encoder.codecType = AoqClientEngine.AoqEncoderType.AoqEncoderTypeAudioPCM;
      encoder.sampleRate = 16000;
      encoder.channel = 1;
      encoder.bitrate = 24000;
      engine.setAudioEncoderConfig(encoder);
    }
    private static void configureTracks(AoqClientEngine.AoqConnectConfig connectConfig) {
      addTrack(connectConfig, true, AoqClientEngine.AoqTrackType.AoqTrackTypeAudio,
              AoqClientEngine.AoqTrackMode.AoqTrackModeStream);
      addTrack(connectConfig, true, AoqClientEngine.AoqTrackType.AoqTrackTypeData,
              AoqClientEngine.AoqTrackMode.AoqTrackModeSegment);
      addTrack(connectConfig, false, AoqClientEngine.AoqTrackType.AoqTrackTypeData,
              AoqClientEngine.AoqTrackMode.AoqTrackModeSegment);
    }
    private void startAudioCapture() {
      AoqClientEngine.AoqAudioCaptureConfig capture =
              new AoqClientEngine.AoqAudioCaptureConfig();
      capture.isExternal = false;
      capture.isVoipMode = true;
      capture.channel = 1;
      engine.startAudioCapture(capture);
      engine.enableSendMediaStream(AoqClientEngine.AoqTrackType.AoqTrackTypeAudio, false);
    }
    /** 在现有 AOQ 连接上启动新一轮识别任务。 */
    public void beginRecognition() {
      if (!connected || taskStarted || taskId != null) {
        return;
      }
      taskId = UUID.randomUUID().toString();
      JSONObject header = createHeader("run-task");
      JSONObject parameters = new JSONObject()
              .put("format", "pcm")
              .put("sample_rate", 16000);
      JSONObject payload = new JSONObject()
              .put("task_group", "audio")
              .put("task", "asr")
              .put("function", "recognition")
              .put("model", "fun-asr-realtime")
              .put("parameters", parameters)
              .put("input", new JSONObject());
      send(new JSONObject().put("header", header).put("payload", payload));
    }
    /** 结束当前任务。收到 task-finished 后再断开连接。 */
    public void finishRecognition() {
      if (taskId == null) {
        return;
      }
      engine.enableSendMediaStream(AoqClientEngine.AoqTrackType.AoqTrackTypeAudio, false);
      JSONObject payload = new JSONObject().put("input", new JSONObject());
      send(new JSONObject()
              .put("header", createHeader("finish-task"))
              .put("payload", payload));
    }
    public void close() {
      engine.enableSendMediaStream(AoqClientEngine.AoqTrackType.AoqTrackTypeAudio, false);
      engine.stopAudioCapture();
      engine.disconnect();
      AoqClientEngine.destroy();
    }
    private void handleServerEvent(AoqClientEngine.AoqDataMsg msg) {
      if (msg == null || msg.data == null) {
        return;
      }
      JSONObject event = new JSONObject(new String(msg.data, StandardCharsets.UTF_8));
      JSONObject header = event.optJSONObject("header");
      if (header == null) {
        return;
      }
      String eventName = header.optString("event", "");
      if ("task-started".equals(eventName)) {
        taskStarted = true;
        engine.enableSendMediaStream(
                AoqClientEngine.AoqTrackType.AoqTrackTypeAudio, true);
      } else if ("result-generated".equals(eventName)) {
        handleRecognitionResult(event);
      } else if ("task-finished".equals(eventName)) {
        resetTaskState();
        resultListener.onTaskFinished();
      } else if ("task-failed".equals(eventName)) {
        String message = header.optString("error_message", "识别失败");
        resetTaskState();
        resultListener.onError(message);
      }
    }
    private void handleRecognitionResult(JSONObject event) {
      JSONObject payload = event.optJSONObject("payload");
      JSONObject output = payload == null ? null : payload.optJSONObject("output");
      JSONObject sentence = output == null ? null : output.optJSONObject("sentence");
      if (sentence == null || sentence.optBoolean("heartbeat", false)) {
        return;
      }
      String text = sentence.optString("text", "");
      if (!text.isEmpty()) {
        resultListener.onResult(text, sentence.optBoolean("sentence_end", false));
      }
    }
    private void resetTaskState() {
      engine.enableSendMediaStream(AoqClientEngine.AoqTrackType.AoqTrackTypeAudio, false);
      taskStarted = false;
      taskId = null;
    }
    private JSONObject createHeader(String action) {
      return new JSONObject()
              .put("action", action)
              .put("task_id", taskId)
              .put("streaming", "duplex");
    }
    private void send(JSONObject event) {
      AoqClientEngine.AoqDataMsg msg = new AoqClientEngine.AoqDataMsg();
      msg.data = event.toString().getBytes(StandardCharsets.UTF_8);
      engine.sendDataMsg(msg);
    }
    private static void addTrack(AoqClientEngine.AoqConnectConfig config, boolean publish,
                                 AoqClientEngine.AoqTrackType type,
                                 AoqClientEngine.AoqTrackMode mode) {
      AoqClientEngine.AoqTrackParam track = new AoqClientEngine.AoqTrackParam();
      track.trackType = type;
      track.trackMode = mode;
      if (publish) {
        config.publishTracks.add(track);
      } else {
        config.subscribeTracks.add(track);
      }
    }
    /** 将 AppServer 返回的 Token 响应转换为 SDK 连接配置。 */
    public static AoqClientEngine.AoqConnectConfig parseConnectConfig(String responseText) {
      JSONObject response = new JSONObject(responseText);
      AoqClientEngine.AoqConnectConfig config = new AoqClientEngine.AoqConnectConfig();
      config.token = response.optString("aoqTokenForClient", "");
      config.sid = response.optString("sid", "");
      config.certFingerprint = response.optString("clientRelayCertFingerprint", "");
      JSONArray endpoints = response.optJSONArray("clientRelayEndpoints");
      if (endpoints != null) {
        for (int i = 0; i < endpoints.length(); i++) {
          JSONObject item = endpoints.optJSONObject(i);
          if (item == null) {
            continue;
          }
          AoqClientEngine.AoqRelayEndpoint endpoint =
                  new AoqClientEngine.AoqRelayEndpoint();
          endpoint.routeIndex = item.has("route_index")
                  ? item.optInt("route_index", i) : i;
          endpoint.endpoint = item.optString("endpoint", "");
          endpoint.port = item.optInt("port", 0);
          config.relayEndpoints.add(endpoint);
        }
      }
      JSONObject extraInfo = response.optJSONObject("extraInfo");
      config.workspaceIdHash = extraInfo == null
              ? "" : extraInfo.optString("workspaceIdHash", "");
      return config;
    }
  }
  ```
</Accordion>

### 调用示例

将 AppServer 的 Token 响应传给 parseConnectConfig，然后创建客户端。首次连接成功后自动开始识别。停止按钮只结束当前任务；页面销毁时才释放连接和本地资源。

```java
private AsrClient client;
void startRecognition(Context context, String tokenResponseText) {
  AoqClientEngine.AoqConnectConfig config =
          AsrClient.parseConnectConfig(tokenResponseText);
  client = new AsrClient(context, config, new AsrClient.ResultListener() {
    @Override
    public void onResult(String text, boolean sentenceEnd) {
      // 使用中间句或最终句更新界面。
    }
    @Override
    public void onTaskFinished() {
      // 启用开始按钮，或调用 beginRecognition() 开始新任务。
    }
    @Override
    public void onError(String message) {
      // 展示或记录错误。
    }
  });
}
void onStopButtonClick() {
  // 结束当前任务，并保持 AOQ 连接，直至收到 task-finished。
  client.finishRecognition();
}
void onPageDestroyed() {
  // 仅在页面关闭时释放本地资源。
  client.close();
}
```

## 运行并验证

1. 启动 AppServer，确认 Token 请求返回 HTTP 200，并包含 sid、aoqTokenForClient、clientRelayEndpoints、clientRelayCertFingerprint 和 extraInfo.workspaceIdHash。
2. 在 Android 设备上安装并运行应用，授予麦克风权限，然后说一段话。
3. 观察回调。正常事件顺序如下：

```plaintext
task-started
result-generated (sentence_end=false)
result-generated (sentence_end=true)
task-finished
```

说话过程中应持续收到中间识别文本。调用 finishRecognition 后，应收到当前句的最终文本和 task-finished。不要在 finish-task 发送后立即断开连接。

## 典型场景

### 同一连接多次识别

收到 task-finished 后调用 beginRecognition，可在同一 AOQ 连接上启动下一轮识别。每轮任务必须使用新的 task\_id，不需要重新申请 Token 或重建连接；如果连接已经断开，则需要重新获取连接凭证。

### Android 后台识别

Android 10 及以上版本中，如需在应用进入后台后继续采集麦克风音频，应使用 foregroundServiceType=microphone 的前台服务，并在应用仍对用户可见时启动该服务。

## 常见问题

| **问题**            | **处理方法**                                                                                                           |
| ----------------- | ------------------------------------------------------------------------------------------------------------------ |
| 连接失败              | 确认 Token 尚未过期、Endpoint 与业务地域一致，并检查 AppServer 是否传入了终端真实公网 IP。连接断开后不要复用旧 Token。                                      |
| 任务已启动但没有识别结果      | 确认收到 task-started 后才开启 Audio 轨发送，并根据当前模型的[客户端事件](/api-reference/qwen-audio-realtime/client-events)检查音频格式、采样率等输入参数。 |
| 收不到最终结果           | 先关闭 Audio 轨发送，再发送 finish-task；等待最终 result-generated 和 task-finished，不要立即断开连接。                                      |
| Android 加载 SDK 失败 | 确认 AAR 已加入依赖，并且应用只打包 SDK 支持的 armeabi-v7a 或 arm64-v8a ABI。                                                          |
| 同一连接的下一轮任务被拒绝     | 确认上一轮已经收到 task-finished，并为新一轮 run-task 生成新的 task\_id。                                                              |

## 相关文档

如需查询完整参数、事件字段或其他平台接口，请参见：

- [获取与配置 API Key](/api-reference/preparation/api-key)
- [选择地域、服务部署范围和接入域名](/developer-guides/realtime-api/overview)
- [SDK 简介](/developer-guides/realtime-api/aoq-sdk-intro)
- [SDK 下载](/developer-guides/realtime-api/sdk-download)
- [Token 鉴权](/developer-guides/realtime-api/token-auth)
- [实时语音识别](/api-reference/speech-recognition/fun-asr-realtime/python-sdk)
- [客户端事件](/api-reference/qwen-audio-realtime/client-events)
- [服务端事件](/api-reference/qwen-audio-realtime/server-events)
