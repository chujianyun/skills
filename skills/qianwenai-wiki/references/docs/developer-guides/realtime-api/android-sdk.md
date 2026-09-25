> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Android SDK

> AOQ Android SDK API 参考

AOQ Client SDK Android 版提供完整的实时音视频通信能力，包括引擎生命周期管理、音频/视频采集与播放、编解码配置、外部音频流注入、音频文件混音、实时消息收发、音视频帧数据回调等功能。本文档为 Android 平台 Java API 的完整参考。

## 接口目录

### 引擎生命周期

| **接口**       | **简介**       |
| ------------ | ------------ |
| createEngine | 创建引擎实例（单例模式） |
| destroy      | 销毁引擎实例       |
| getVersion   | 获取 SDK 版本号   |
| connect      | 连接 Relay 服务器 |
| disconnect   | 断开服务器连接      |

### 音频设备管理

| **接口**                | **简介**         |
| --------------------- | -------------- |
| startAudioCapture     | 打开音频采集设备（麦克风）  |
| stopAudioCapture      | 关闭音频采集设备       |
| muteAudioCapture      | 静音或取消静音音频采集    |
| startAudioPlayer      | 开始音频渲染（播放远端音频） |
| stopAudioPlayer       | 停止音频渲染         |
| pauseAudioPlayer      | 暂停音频渲染，支持淡出    |
| resumeAudioPlayer     | 恢复音频渲染，支持淡入    |
| interruptAudioPlayer  | 打断本轮音频通话       |
| enableSpeakerphone    | 切换音频输出到扬声器或听筒  |
| isSpeakerphoneEnabled | 查询当前是否使用扬声器输出  |

### 音频编码配置

| **接口**                | **简介**   |
| --------------------- | -------- |
| setAudioEncoderConfig | 设置音频编码参数 |
| setAudioDecoderConfig | 设置音频解码参数 |

### 视频设备管理

| **接口**            | **简介**        |
| ----------------- | ------------- |
| startVideoCapture | 打开视频采集设备（摄像头） |
| stopVideoCapture  | 关闭视频采集设备      |
| switchCamera      | 切换前后置摄像头      |
| setLocalView      | 设置或移除本地视频渲染窗口 |
| setRemoteView     | 设置或移除远端视频渲染窗口 |

### 视频编码与外部输入

| **接口**                         | **简介**     |
| ------------------------------ | ---------- |
| setVideoEncoderConfig          | 设置视频编码参数   |
| pushExternalVideoCapturedFrame | 推送外部采集视频帧  |
| pushExternalVideoEncodedFrame  | 推送外部已编码视频帧 |

### 媒体流发送控制 / 实时消息

| **接口**                | **简介**       |
| --------------------- | ------------ |
| enableSendMediaStream | 控制本地媒体流的发送开关 |
| sendDataMsg           | 发送实时数据消息     |

### 音频文件播放

| **接口**                      | **简介**           |
| --------------------------- | ---------------- |
| startAudioFile              | 开始推流播放本地音频文件     |
| stopAudioFile               | 停止音频文件播放         |
| pauseAudioFile              | 暂停音频文件播放         |
| resumeAudioFile             | 恢复音频文件播放         |
| getAudioFileDuration        | 获取音频文件总时长        |
| getAudioFileCurrentPosition | 获取音频文件当前播放位置     |
| setAudioFilePositionMillis  | 设置音频文件播放位置（seek） |
| setAudioFileVolume          | 设置音频文件音量         |
| getAudioFileVolume          | 获取音频文件当前音量       |

### 外部音频流

| **接口**                         | **简介**        |
| ------------------------------ | ------------- |
| addAudioExternalStream         | 新增一条外部音频流     |
| removeAudioExternalStream      | 移除外部音频流       |
| pushAudioExternalStreamData    | 输入外部音频 PCM 数据 |
| setAudioExternalStreamVolume   | 设置外部音频流音量     |
| getAudioExternalStreamVolume   | 获取外部音频流音量     |
| clearAudioExternalStreamBuffer | 清空外部音频流缓存     |

### 音视频帧回调

| **接口**                   | **简介**          |
| ------------------------ | --------------- |
| setAudioFrameObserver    | 设置音频帧数据回调监听     |
| enableAudioFrameObserver | 开启或关闭指定位置的音频帧回调 |
| setVideoFrameObserver    | 设置视频帧数据回调监听     |
| enableVideoFrameObserver | 开启或关闭指定位置的视频帧回调 |

### AoqClientListener 回调

| **回调**                    | **简介**       |
| ------------------------- | ------------ |
| onError                   | 引擎错误回调       |
| onWarning                 | 引擎警告回调       |
| onConnectionStatusChange  | 连接状态变化回调     |
| onStats                   | 引擎统计信息回调     |
| onAudioDeviceStateChanged | 音频设备操作状态变化回调 |
| onAudioDeviceRouteChanged | 音频输出路由变化回调   |
| onAudioDeviceInterrupted  | 音频设备中断回调     |
| onVideoDeviceStateChanged | 视频设备操作状态变化回调 |
| onAudioDeviceFocusChanged | 音频焦点变化回调     |
| onAudioFileState          | 音频文件播放状态回调   |
| onDataMsg                 | 收到实时数据消息回调   |

## 接口详情

### 引擎生命周期

**createEngine**

创建引擎实例。SDK 内部以全局单例方式持有引擎，重复调用会返回已创建的实例。

```java
@NonNull
public static AoqClientEngine createEngine(
    @NonNull Context context,
    @NonNull AoqCreateConfig config,
    @NonNull AoqClientListener listener)
```

| **参数**   | **类型**            | **说明**        |
| -------- | ----------------- | ------------- |
| context  | Context           | Android 应用上下文 |
| config   | AoqCreateConfig   | 引擎创建配置        |
| listener | AoqClientListener | 引擎事件回调监听      |

返回值：AoqClientEngine 引擎实例，不会返回 null。

**destroy**

销毁引擎实例，释放所有资源。

```java
public static int destroy()
```

返回值：0 表示成功；非 0 表示失败。

**getVersion**

```java
@NonNull
public static String getVersion()
```

返回值：版本号字符串，如 "1.0.0"。

**connect**

连接 Relay 服务器。连接参数由业务方 AppServer 通过 /api/v1/allocate 分配后下发给客户端。

```java
public abstract int connect(@NonNull AoqConnectConfig config)
```

返回值：0 表示调用已下发（异步执行）；非 0 表示参数校验失败。

**disconnect**

```java
public abstract int disconnect()
```

返回值：0 表示调用已下发（异步执行）；非 0 表示失败。

### 音频设备管理

```java
public abstract int startAudioCapture(@NonNull AoqAudioCaptureConfig config)
public abstract int stopAudioCapture()
public abstract int muteAudioCapture(boolean mute)
public abstract int startAudioPlayer(@NonNull AoqAudioPlaybackConfig config)
public abstract int stopAudioPlayer()
public abstract int pauseAudioPlayer(int fadeMs)
public abstract int resumeAudioPlayer(int fadeMs)
public abstract int interruptAudioPlayer(@NonNull AoqTrackType trackType, int fadeMs)
public abstract int enableSpeakerphone(boolean enable)
public abstract boolean isSpeakerphoneEnabled()
```

`fadeMs`：淡出/淡入时长（毫秒）；0 表示立即执行。

### 音频编码配置

```java
public abstract int setAudioEncoderConfig(@NonNull AoqAudioCodecConfig config)
public abstract int setAudioDecoderConfig(@NonNull AoqAudioCodecConfig config)
```

### 视频设备管理

```java
public abstract int startVideoCapture(@NonNull AoqVideoCaptureConfig config)
public abstract int stopVideoCapture()
public abstract int switchCamera(@NonNull AoqCameraDirection direction)
public abstract int setLocalView(@NonNull AoqTrackType trackType, @Nullable AoqVideoCanvas canvas)
public abstract int setRemoteView(@NonNull AoqTrackType trackType, @Nullable AoqVideoCanvas canvas)
```

setLocalView/setRemoteView 的 trackType 参数传 AoqTrackTypeVideo。

### 视频编码与外部输入

```java
public abstract int setVideoEncoderConfig(@NonNull AoqVideoCodecConfig config)
public abstract int pushExternalVideoCapturedFrame(@NonNull AoqTrackType trackType, @NonNull AoqVideoFrame frame)
public abstract int pushExternalVideoEncodedFrame(@NonNull AoqTrackType trackType, @NonNull AoqVideoEncodedFrame frame)
```

<Note>
  pushExternalVideoCapturedFrame 仅在 startVideoCapture(isExternal=true) 后消费。若缓冲区满返回 AoqErrorCodeVideoExternalBufferFull(210)。
</Note>

### 媒体流发送控制

```java
public abstract int enableSendMediaStream(@NonNull AoqTrackType trackType, boolean enable)
```

建议初始化后先 enableSendMediaStream(false)，待 onConnectionStatusChange(Connected) 后再开启。

### 音频文件播放

```java
public abstract int startAudioFile(@NonNull String fileId, @NonNull AoqAudioFileMixConfig config)
public abstract int stopAudioFile(@NonNull String fileId)
public abstract int pauseAudioFile(@NonNull String fileId)
public abstract int resumeAudioFile(@NonNull String fileId)
public abstract long getAudioFileDuration(@NonNull String fileId)
public abstract long getAudioFileCurrentPosition(@NonNull String fileId)
public abstract int setAudioFilePositionMillis(@NonNull String fileId, long positionMillis)
public abstract int setAudioFileVolume(@NonNull String fileId, @NonNull AoqAudioStreamDirection type, int volume)
public abstract int getAudioFileVolume(@NonNull String fileId, @NonNull AoqAudioStreamDirection type)
```

### 外部音频流

```java
public abstract int addAudioExternalStream(@NonNull String streamId, @NonNull AoqAudioExternalStreamConfig config)
public abstract int removeAudioExternalStream(@NonNull String streamId)
public abstract int pushAudioExternalStreamData(@NonNull String streamId, @NonNull AoqAudioFrameData data)
public abstract int setAudioExternalStreamVolume(@NonNull String streamId, @NonNull AoqAudioStreamDirection type, int volume)
public abstract int getAudioExternalStreamVolume(@NonNull String streamId, @NonNull AoqAudioStreamDirection type)
public abstract void clearAudioExternalStreamBuffer(@NonNull String streamId, int fadeoutMs)
```

<Note>
  pushAudioExternalStreamData 缓冲区满时返回 AoqErrorCodeAudioExternalBufferFull(110)，建议 Sleep 30ms 后重试。
</Note>

### 实时消息

```java
public abstract int sendDataMsg(@NonNull AoqDataMsg msg)
```

### 音频帧回调

```java
public abstract int setAudioFrameObserver(@Nullable AoqClientListener.AoqAudioFrameListener listener)
public abstract int enableAudioFrameObserver(boolean enabled, @NonNull AoqAudioSource audioSource, @NonNull AoqAudioObserverConfig config)
```

### 视频帧回调

```java
public abstract int setVideoFrameObserver(@Nullable AoqClientListener.AoqVideoFrameListener listener)
public abstract int enableVideoFrameObserver(boolean enabled, @NonNull AoqVideoSource videoSource, @NonNull AoqVideoObserverConfig config)
```

## AoqClientListener 回调

AoqClientListener 是 SDK 所有异步事件通知的统一出口。所有回调方法都带有默认空实现，无需强制重写不关心的方法。

```java
public void onError(int code, String message)
public void onWarning(int code, String message)
public void onConnectionStatusChange(@NonNull AoqConnectionStatus status)
public void onStats(@NonNull AoqStats stats)
public void onAudioDeviceStateChanged(@NonNull AoqAudioDeviceState state)
public void onAudioDeviceRouteChanged(int routeType)
public void onAudioDeviceInterrupted(boolean interrupt)
public void onVideoDeviceStateChanged(@NonNull AoqVideoDeviceState state)
public void onAudioDeviceFocusChanged(int audioFocus)
public void onAudioFileState(@NonNull AoqAudioFileState state)
public void onDataMsg(@NonNull AoqDataMsg msg)
```

连接状态流转：Disconnected → Connecting → Connected/Failed → Disconnected。

### AoqAudioFrameListener

```java
public interface AoqAudioFrameListener {
    default void onCapturedAudioFrame(@NonNull AoqAudioFrameData frame) {}
    default void onProcessCapturedAudioFrame(@NonNull AoqAudioFrameData frame) {}
    default void onPublishAudioFrame(@NonNull AoqTrackType trackType, @NonNull AoqAudioFrameData frame) {}
    default void onPlaybackAudioFrame(@NonNull AoqAudioFrameData frame) {}
}
```

### AoqVideoFrameListener

```java
public interface AoqVideoFrameListener {
    default boolean onCapturedVideoFrame(@NonNull AoqVideoFrameData frame) { return false; }
    default boolean onPreEncodeVideoFrame(@NonNull AoqTrackType trackType, @NonNull AoqVideoFrameData frame) { return false; }
    default boolean onRemoteVideoFrame(@NonNull AoqTrackType trackType, @NonNull AoqVideoFrameData frame) { return false; }
}
```

返回 true 表示数据已修改需写回 SDK（仅 I420 写回生效）。frame 中 ByteBuffer/textureId 仅在回调期间有效，异步使用需自行拷贝。

## 数据类型与枚举

### 通用类型

**AoqCreateConfig**

| **字段**          | **类型**  | **默认值** | **说明**                       |
| --------------- | ------- | ------- | ---------------------------- |
| workDir         | String  | ""      | SDK 工作目录                     |
| isBTScoMode     | boolean | false   | true 蓝牙 SCO 模式；false A2DP 模式 |
| enableDumpAudio | boolean | false   | 是否开启音频 dump（调试用）             |
| extras          | String  | ""      | 扩展参数字符串                      |

**AoqConnectConfig**

| **字段**          | **类型**                  | **默认值** | **说明**       |
| --------------- | ----------------------- | ------- | ------------ |
| token           | String                  | ""      | 连接鉴权 Token   |
| sid             | String                  | ""      | 会话 ID        |
| certFingerprint | String                  | ""      | 服务器证书指纹      |
| relayEndpoints  | List\<AoqRelayEndpoint> | 空       | Relay 接入点列表  |
| workspaceIdHash | String                  | ""      | 工作空间 ID Hash |
| publishTracks   | List\<AoqTrackParam>    | 空       | 本端发布轨道列表     |
| subscribeTracks | List\<AoqTrackParam>    | 空       | 本端订阅轨道列表     |

### 统计信息类型

**AoqNetworkStats**

| **字段**      | **类型** | **说明**     |
| ----------- | ------ | ---------- |
| sendBitrate | int    | 发送码率（bps）  |
| sendBytes   | long   | 累计发送字节数    |
| recvBitrate | int    | 接收码率（bps）  |
| recvBytes   | long   | 累计接收字节数    |
| loss        | int    | 丢包率（0-100） |
| rtt         | int    | 往返延迟（ms）   |

### 枚举类型

**AoqErrorCode**

| **枚举值**                                         | **值** | **说明**       |
| ----------------------------------------------- | ----- | ------------ |
| AoqErrorCodeOK                                  | 0     | 成功           |
| AoqErrorCodeParamInvalid                        | 1     | 参数非法         |
| AoqErrorCodeStateInvalid                        | 2     | 状态非法         |
| AoqErrorCodeUnSupport                           | 3     | 不支持          |
| AoqErrorCodeAudio                               | 100   | 音频通用错误       |
| AoqErrorCodeAudioExternalBufferFull             | 110   | 外部音频缓冲区满     |
| AoqErrorCodeAudioDevice                         | 120   | 音频设备通用错误     |
| AoqErrorCodeAudioDeviceRecordingAuthFailed      | 121   | 录音权限未获取      |
| AoqErrorCodeAudioDeviceRecordingOccupied        | 122   | 录音设备被占用      |
| AoqErrorCodeAudioDeviceRecordingBackgroundStart | 123   | 后台启动录音失败     |
| AoqErrorCodeAudioDeviceRecordingStartFail       | 124   | 录音启动失败       |
| AoqErrorCodeAudioDevicePlayoutOccupied          | 125   | 播放设备被占用      |
| AoqErrorCodeAudioDevicePlayoutBackgroundStart   | 126   | 后台启动播放失败     |
| AoqErrorCodeAudioDevicePlayoutStartFail         | 127   | 播放启动失败       |
| AoqErrorCodeAudioDeviceEarpieceRequiresVoipMode | 128   | 听筒需要 VoIP 模式 |
| AoqErrorCodeVideo                               | 200   | 视频通用错误       |
| AoqErrorCodeVideoExternalBufferFull             | 210   | 外部视频缓冲区满     |
| AoqErrorCodeVideoExternalCaptureNotEnabled      | 211   | 外部视频采集未启用    |
| AoqErrorCodeVideoExternalEncoderNotEnabled      | 212   | 外部视频编码未启用    |
| AoqErrorCodeVideoDevice                         | 220   | 视频设备通用错误     |
| AoqErrorCodeVideoDeviceCameraOpenFail           | 221   | 摄像头打开失败      |
| AoqErrorCodeVideoDeviceCameraAuthFailed         | 222   | 摄像头权限未获取     |
| AoqErrorCodeVideoDeviceCameraOccupied           | 223   | 摄像头被占用       |
| AoqErrorCodeVideoDeviceCameraRunningError       | 224   | 摄像头运行异常      |
| AoqErrorCodeVideoCodec                          | 230   | 视频编解码通用错误    |
| AoqErrorCodeVideoCodecEncoderInitFail           | 231   | 视频编码器初始化失败   |
| AoqErrorCodeVideoRender                         | 240   | 视频渲染通用错误     |
| AoqErrorCodeVideoRenderCreateFail               | 241   | 视频渲染创建失败     |
| AoqErrorCodeVideoRenderDrawError                | 242   | 视频渲染绘制错误     |

**AoqWarningCode**

| **枚举值**                               | **值** | **说明**   |
| ------------------------------------- | ----- | -------- |
| AoqWCOK                               | 0     | 无警告      |
| AoqWCAudio                            | 100   | 音频通用警告   |
| AoqWCAudioHowling                     | 101   | 音频啸叫检测   |
| AoqWCAudioDevice                      | 120   | 音频设备通用警告 |
| AoqWCAudioDeviceMicEnumerateError     | 121   | 麦克风枚举错误  |
| AoqWCAudioDeviceMicStartTimeout       | 122   | 麦克风启动超时  |
| AoqWCAudioDeviceRecordingError        | 123   | 录音过程错误   |
| AoqWCAudioDeviceSpeakerEnumerateError | 124   | 扬声器枚举错误  |
| AoqWCAudioDeviceSpeakerStartTimeout   | 125   | 扬声器启动超时  |
| AoqWCAudioDevicePlayoutError          | 126   | 播放过程错误   |
| AoqWCVideo                            | 200   | 视频通用警告   |
| AoqWCVideoCameraEnumerateError        | 201   | 摄像头枚举错误  |
| AoqWCVideoEncoderSwitched             | 202   | 视频编码器已切换 |
| AoqWCVideoRenderDowngrade             | 203   | 视频渲染降级   |

**AoqTrackType**

| **枚举值**           | **值** | **说明** |
| ----------------- | ----- | ------ |
| AoqTrackTypeAudio | 0     | 音频轨道   |
| AoqTrackTypeVideo | 1     | 视频轨道   |
| AoqTrackTypeData  | 2     | 数据消息轨道 |

**AoqEncoderType**

| **枚举值**                 | **值** | **说明**   |
| ----------------------- | ----- | -------- |
| AoqEncoderTypeUnknown   | 0     | 未知格式     |
| AoqEncoderTypeAudioPCM  | 1     | 音频 PCM   |
| AoqEncoderTypeAudioOpus | 2     | 音频 Opus  |
| AoqEncoderTypeVideoH264 | 3     | 视频 H.264 |
| AoqEncoderTypeVideoJpeg | 4     | 视频 JPEG  |
| AoqEncoderTypeDataText  | 5     | 数据文本     |

**AoqConnectionStatus**

| **枚举值**                         | **值** | **说明** |
| ------------------------------- | ----- | ------ |
| AoqConnectionStatusDisconnected | 0     | 未连接    |
| AoqConnectionStatusConnecting   | 1     | 连接中    |
| AoqConnectionStatusConnected    | 2     | 已连接    |
| AoqConnectionStatusFailed       | 3     | 连接失败   |

### 音频类型

**AoqAudioCaptureConfig**

| **字段**     | **类型**  | **默认值** | **说明**                   |
| ---------- | ------- | ------- | ------------------------ |
| isExternal | boolean | false   | 是否为外部采集模式                |
| isVoipMode | boolean | false   | 是否启用 VoIP 模式（影响设备路由，如听筒） |
| channel    | int     | 1       | 声道数（默认单声道）               |

**AoqAudioPlaybackConfig**

| **字段**           | **类型**  | **默认值** | **说明**                     |
| ---------------- | ------- | ------- | -------------------------- |
| isVoipMode       | boolean | false   | 是否启用 VoIP 模式（硬件 AEC），移动端有效 |
| isDefaultSpeaker | boolean | true    | 是否默认扬声器，移动端有效              |
| isExternal       | boolean | false   | 是否为外部播放模式                  |
| channel          | int     | 1       | 声道数（默认单声道）                 |

**AoqAudioCodecConfig**

| **字段**     | **类型**         | **默认值**  | **说明**   |
| ---------- | -------------- | -------- | -------- |
| trackType  | AoqTrackType   | Audio    | 轨道类型     |
| codecType  | AoqEncoderType | AudioPCM | 编码格式     |
| sampleRate | int            | 48000    | 采样率（Hz）  |
| channel    | int            | 1        | 声道数      |
| bitrate    | int            | 32000    | 比特率（bps） |

### 视频类型

**AoqVideoCaptureConfig**

| **字段**          | **类型**             | **默认值** | **说明**                       |
| --------------- | ------------------ | ------- | ---------------------------- |
| width           | int                | 1280    | 采集宽度（像素），isExternal=true 时无效 |
| height          | int                | 720     | 采集高度（像素），isExternal=true 时无效 |
| fps             | int                | 15      | 采集帧率，isExternal=true 时无效     |
| isExternal      | boolean            | false   | 是否外部采集，true 时不打开摄像头          |
| cameraDirection | AoqCameraDirection | Front   | 摄像头方向，isExternal=true 时无效    |

**AoqVideoCodecConfig**

| **字段**           | **类型**             | **默认值**   | **说明**                                               |
| ---------------- | ------------------ | --------- | ---------------------------------------------------- |
| trackType        | AoqTrackType       | Video     | 轨道类型                                                 |
| codecType        | AoqEncoderType     | VideoH264 | 编码格式                                                 |
| width            | int                | 720       | 编码宽度（像素）                                             |
| height           | int                | 1280      | 编码高度（像素）                                             |
| fps              | int                | 5         | 编码帧率                                                 |
| bitrate          | int                | 500000    | 目标比特率（bps）                                           |
| minBitrate       | int                | 128000    | 最小比特率（bps）                                           |
| keyframeInterval | int                | 2         | 关键帧间隔（秒）                                             |
| mirrorMode       | AoqMirrorMode      | Disabled  | 镜像模式                                                 |
| orientationMode  | AoqOrientationMode | Auto      | 视频方向模式                                               |
| isExternal       | boolean            | false     | true 时 SDK 不做二次编码，由 pushExternalVideoEncodedFrame 直推 |

**AoqVideoPixelFormat**

| **枚举值**                       | **值** | **说明**          |
| ----------------------------- | ----- | --------------- |
| AoqVideoPixelFormatUnknown    | 0     | 未知格式            |
| AoqVideoPixelFormatI420       | 1     | I420（YUV 三平面格式） |
| AoqVideoPixelFormatNV12       | 2     | NV12（YUV 半平面格式） |
| AoqVideoPixelFormatNV21       | 3     | NV21（YUV 半平面格式） |
| AoqVideoPixelFormatBGRA       | 4     | BGRA（32 位）      |
| AoqVideoPixelFormatRGBA       | 5     | RGBA（32 位）      |
| AoqVideoPixelFormatTextureOES | 7     | 外部 OES 纹理       |
| AoqVideoPixelFormatTexture2D  | 8     | 普通 2D 纹理        |

### 外部音频流类型

**AoqAudioExternalStreamConfig**

| **字段**            | **类型**         | **默认值**  | **说明**             |
| ----------------- | -------------- | -------- | ------------------ |
| trackType         | AoqTrackType   | Audio    | 音频轨道类型             |
| codecType         | AoqEncoderType | AudioPCM | 音频流格式              |
| channels          | int            | 1        | 声道数                |
| sampleRate        | int            | 48000    | 采样率（Hz）            |
| playoutVolume     | int            | 100      | 播放音量 \[0-100]      |
| publishVolume     | int            | 100      | 推流音量 \[0-100]      |
| maxBufferDuration | int            | 1000     | 最大缓冲时长（毫秒）         |
| enable3A          | boolean        | false    | 是否对输入 PCM 进行 3A 处理 |

**AoqAudioStreamDirection**

| **枚举值**               | **值** | **说明**  |
| --------------------- | ----- | ------- |
| AoqAudioStreamPublish | 0     | 发布流（推流） |
| AoqAudioStreamPlayout | 1     | 播放流（拉流） |

### 数据消息类型

**AoqDataMsg**

| **字段** | **类型**  | **默认值**      | **说明**     |
| ------ | ------- | ------------ | ---------- |
| data   | byte\[] | new byte\[0] | 消息数据（字节数组） |
