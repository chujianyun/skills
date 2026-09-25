> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# HarmonyOS SDK

> AOQ HarmonyOS SDK API 参考

AOQ Client SDK HarmonyOS (OHOS) 端 API 参考，平台语言为 ArkTS (.ets)，通过 NAPI 桥接 C++ 引擎。

## 目录

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

### 媒体流发送控制

| **接口**                | **简介**       |
| --------------------- | ------------ |
| enableSendMediaStream | 控制本地媒体流的发送开关 |

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

### 实时消息

| **接口**      | **简介**   |
| ----------- | -------- |
| sendDataMsg | 发送实时数据消息 |

### 音频帧回调

| **接口**                   | **简介**          |
| ------------------------ | --------------- |
| setAudioFrameObserver    | 设置音频帧数据回调监听     |
| enableAudioFrameObserver | 开启或关闭指定位置的音频帧回调 |

### 视频帧回调

| **接口**                   | **简介**          |
| ------------------------ | --------------- |
| setVideoFrameObserver    | 设置视频帧数据回调监听     |
| enableVideoFrameObserver | 开启或关闭指定位置的视频帧回调 |

### AoqEngineEventListener 回调

| **回调**                    | **简介**       |
| ------------------------- | ------------ |
| onError                   | 引擎错误回调       |
| onWarning                 | 引擎警告回调       |
| onConnectionStatusChange  | 连接状态变化回调     |
| onStats                   | 统计数据回调       |
| onAudioDeviceStateChanged | 音频设备操作状态变化回调 |
| onAudioDeviceRouteChanged | 音频输出路由变化回调   |
| onAudioDeviceInterrupted  | 音频设备中断回调     |
| onVideoDeviceStateChanged | 视频设备操作状态变化回调 |
| onAudioFileState          | 音频文件播放状态回调   |
| onDataMsg                 | 收到实时数据消息回调   |
| IAudioFrameObserver       | 音频帧数据观察者接口   |
| IVideoFrameObserver       | 视频帧数据观察者接口   |

## 接口详情

### 引擎生命周期

#### createEngine

创建引擎实例。SDK 内部以全局单例方式持有引擎，重复调用会返回已创建的实例。native 创建失败时返回 null。

```typescript
static createEngine(config: AoqCreateConfig, listener: AoqEngineEventListener, context: common.Context): AoqClientEngine | null
```

| **参数**   | **类型**                 | **说明**                                   |
| -------- | ---------------------- | ---------------------------------------- |
| config   | AoqCreateConfig        | 引擎创建配置                                   |
| listener | AoqEngineEventListener | 引擎事件回调监听（interface，所有回调均为可选）             |
| context  | common.Context         | UIAbility/Page 的 Context，用于 aki+ACPM 初始化 |

**返回值**：`AoqClientEngine | null`（native 创建失败时返回 null）

**注意事项**：与 Android 不同，OHOS 端创建失败会返回 null，调用方需判空处理。context 必须是有效的 UIAbility 或 Page Context。

#### destroy

销毁引擎单例，释放所有资源。调用后需重新 createEngine 才能继续使用。

```typescript
static destroy(): number
```

**返回值**：0 表示成功；非 0 表示失败

#### getVersion

获取 SDK 当前版本号。

```typescript
static getVersion(): string
```

**返回值**：版本号字符串，如 `"1.0.0"`

#### connect

连接 Relay 服务器。连接参数由业务方 AppServer 通过 `/api/v1/allocate` 分配后下发给客户端。

```typescript
connect(config: AoqConnectConfig): number
```

| **参数** | **类型**           | **说明**                         |
| ------ | ---------------- | ------------------------------ |
| config | AoqConnectConfig | 连接配置，包含 Token、SID、Relay 接入点列表等 |

**返回值**：0 表示调用已下发（异步执行）；非 0 表示参数校验失败

**注意事项**：连接状态变化通过 `onConnectionStatusChange` 异步通知。建议在 connect 前调用 `enableSendMediaStream(false)`。

#### disconnect

断开与服务器的连接，释放连接相关资源。音视频采集/播放设备不会自动停止。

```typescript
disconnect(): number
```

**返回值**：0 表示调用已下发（异步执行）；非 0 表示失败

### 音频设备管理

#### startAudioCapture

打开音频采集设备（麦克风）。

```typescript
startAudioCapture(config: AoqAudioCaptureConfig): number
```

| **参数** | **类型**                | **说明** |
| ------ | --------------------- | ------ |
| config | AoqAudioCaptureConfig | 采集配置   |

**返回值**：0 表示成功；非 0 表示失败

#### stopAudioCapture

关闭音频采集设备。

```typescript
stopAudioCapture(): number
```

#### muteAudioCapture

静音或取消静音音频采集。

```typescript
muteAudioCapture(mute: boolean): number
```

| **参数** | **类型**  | **说明**               |
| ------ | ------- | -------------------- |
| mute   | boolean | true 为静音；false 为取消静音 |

#### startAudioPlayer

开始音频渲染（扬声器/听筒播放远端音频）。

```typescript
startAudioPlayer(config: AoqAudioPlaybackConfig): number
```

| **参数** | **类型**                 | **说明** |
| ------ | ---------------------- | ------ |
| config | AoqAudioPlaybackConfig | 播放配置   |

#### stopAudioPlayer

停止音频渲染。

```typescript
stopAudioPlayer(): number
```

#### pauseAudioPlayer

暂停音频渲染，可指定淡出时长实现平滑过渡。

```typescript
pauseAudioPlayer(fadeMs: number): number
```

| **参数** | **类型** | **说明**            |
| ------ | ------ | ----------------- |
| fadeMs | number | 淡出时长（毫秒）；0 表示立即停止 |

#### resumeAudioPlayer

恢复音频渲染，可指定淡入时长实现平滑过渡。

```typescript
resumeAudioPlayer(fadeMs: number): number
```

| **参数** | **类型** | **说明**            |
| ------ | ------ | ----------------- |
| fadeMs | number | 淡入时长（毫秒）；0 表示立即恢复 |

#### interruptAudioPlayer

打断本轮音频通话。

```typescript
interruptAudioPlayer(trackType: AoqTrackType, fadeMs: number): number
```

| **参数**    | **类型**       | **说明**                       |
| --------- | ------------ | ---------------------------- |
| trackType | AoqTrackType | 目标轨道类型，通常传 AoqTrackTypeAudio |
| fadeMs    | number       | 淡出时长（毫秒）                     |

#### enableSpeakerphone

切换音频输出路由到扬声器或听筒。

```typescript
enableSpeakerphone(enable: boolean): number
```

| **参数** | **类型**  | **说明**                |
| ------ | ------- | --------------------- |
| enable | boolean | true 使用扬声器；false 使用听筒 |

#### isSpeakerphoneEnabled

查询当前是否使用扬声器输出。

```typescript
isSpeakerphoneEnabled(): boolean
```

**返回值**：true 表示当前为扬声器模式；false 表示听筒模式

### 音频编码配置

#### setAudioEncoderConfig

设置音频编码参数。

```typescript
setAudioEncoderConfig(config: AoqAudioCodecConfig): number
```

#### setAudioDecoderConfig

设置音频解码参数。

```typescript
setAudioDecoderConfig(config: AoqAudioCodecConfig): number
```

### 视频设备管理

#### startVideoCapture

打开视频采集设备（摄像头）。当 `config.isExternal = true` 时不打开摄像头，由调用方通过 `pushExternalVideoCapturedFrame` 喂帧。

```typescript
startVideoCapture(config: AoqVideoCaptureConfig): number
```

#### stopVideoCapture

关闭视频采集设备。

```typescript
stopVideoCapture(): number
```

#### switchCamera

切换前后置摄像头。

```typescript
switchCamera(direction: AoqCameraDirection): number
```

| **参数**    | **类型**             | **说明**                                           |
| --------- | ------------------ | ------------------------------------------------ |
| direction | AoqCameraDirection | AoqCameraDirectionFront 或 AoqCameraDirectionBack |

#### setLocalView

设置或移除本地视频渲染窗口。

```typescript
setLocalView(trackType: AoqTrackType, canvas: AoqVideoCanvas | null): number
```

| **参数**    | **类型**                 | **说明**                                      |
| --------- | ---------------------- | ------------------------------------------- |
| trackType | AoqTrackType           | AoqTrackTypeVideo                           |
| canvas    | AoqVideoCanvas \       | null                                        | 渲染画布配置；传 null 或 canvas.view 为 null 表示移除渲染窗口 |

**注意**：OHOS 上必须在 `XComponent.onLoad` 回调之后调用，`canvas.view` 应传入 `AoqXComponentController` 实例。

#### setRemoteView

设置或移除远端视频渲染窗口。

```typescript
setRemoteView(trackType: AoqTrackType, canvas: AoqVideoCanvas | null): number
```

| **参数**    | **类型**                 | **说明**                                      |
| --------- | ---------------------- | ------------------------------------------- |
| trackType | AoqTrackType           | AoqTrackTypeVideo                           |
| canvas    | AoqVideoCanvas \       | null                                        | 渲染画布配置；传 null 或 canvas.view 为 null 表示移除渲染窗口 |

### 视频编码与外部输入

#### setVideoEncoderConfig

设置视频编码参数，按 `config.trackType` 路由到对应轨道。

```typescript
setVideoEncoderConfig(config: AoqVideoCodecConfig): number
```

#### pushExternalVideoCapturedFrame

推送外部采集视频帧。

```typescript
pushExternalVideoCapturedFrame(trackType: AoqTrackType, frame: AoqVideoFrame): number
```

| **参数**    | **类型**        | **说明**            |
| --------- | ------------- | ----------------- |
| trackType | AoqTrackType  | AoqTrackTypeVideo |
| frame     | AoqVideoFrame | 视频帧数据             |

**路由规则**：仅在 `startVideoCapture(isExternal=true)` 后消费。支持格式：NV12 / NV21 / BGRA / RGBA / I420。

若缓冲区满，会返回错误码 `AoqECVideoExternalBufferFull`(210)，调用方需 sleep 后重试，禁止 busy loop。

#### pushExternalVideoEncodedFrame

推送外部已编码视频帧。SDK 不做二次编码，直接打包发送。

```typescript
pushExternalVideoEncodedFrame(trackType: AoqTrackType, frame: AoqVideoEncodedFrame): number
```

| **参数**    | **类型**               | **说明**            |
| --------- | -------------------- | ----------------- |
| trackType | AoqTrackType         | AoqTrackTypeVideo |
| frame     | AoqVideoEncodedFrame | 已编码帧数据            |

**路由规则**：仅在 `setVideoEncoderConfig(isExternal=true)` 配置后才消费。

### 媒体流发送控制

#### enableSendMediaStream

控制本地媒体流的发送，按 trackType 路由到对应轨道。

```typescript
enableSendMediaStream(trackType: AoqTrackType, enable: boolean): number
```

| **参数**    | **类型**       | **说明**                                |
| --------- | ------------ | ------------------------------------- |
| trackType | AoqTrackType | AoqTrackTypeAudio / AoqTrackTypeVideo |
| enable    | boolean      | true 启用发送；false 停用发送                  |

**使用建议**：初始化后先调用 `enableSendMediaStream(trackType, false)`，待 connect 成功且会话握手完成（收到 `onConnectionStatusChange(AoqConnectionStatusConnected)`）后再开启发送。

### 音频文件播放

#### startAudioFile

开始推流播放本地音频文件。音频文件播放会混音到推流和本地播放中。

```typescript
startAudioFile(fileId: string, config: AoqAudioFileMixConfig): number
```

| **参数** | **类型**                | **说明**          |
| ------ | --------------------- | --------------- |
| fileId | string                | 音频文件唯一标识，由调用方指定 |
| config | AoqAudioFileMixConfig | 播放配置            |

#### stopAudioFile / pauseAudioFile / resumeAudioFile

```typescript
stopAudioFile(fileId: string): number
pauseAudioFile(fileId: string): number
resumeAudioFile(fileId: string): number
```

#### getAudioFileDuration / getAudioFileCurrentPosition

```typescript
getAudioFileDuration(fileId: string): number      // 返回总时长(ms)；负值表示失败
getAudioFileCurrentPosition(fileId: string): number // 返回当前位置(ms)；负值表示失败
```

#### setAudioFilePositionMillis

```typescript
setAudioFilePositionMillis(fileId: string, positionMillis: number): number
```

#### setAudioFileVolume / getAudioFileVolume

```typescript
setAudioFileVolume(fileId: string, type: AoqAudioStreamDirection, volume: number): number
getAudioFileVolume(fileId: string, type: AoqAudioStreamDirection): number // 返回 [0,100]；负值表示失败
```

### 外部音频流

#### addAudioExternalStream

新增一条外部音频流。

```typescript
addAudioExternalStream(streamId: string, config: AoqAudioExternalStreamConfig): number
```

#### pushAudioExternalStreamData

输入外部音频 PCM 数据。若缓冲区满返回 `AoqECAudioExternalBufferFull`(110)。

```typescript
pushAudioExternalStreamData(streamId: string, data: AoqAudioFrameData): number
```

#### setAudioExternalStreamVolume / getAudioExternalStreamVolume

```typescript
setAudioExternalStreamVolume(streamId: string, type: AoqAudioStreamDirection, vol: number): number
getAudioExternalStreamVolume(streamId: string, type: AoqAudioStreamDirection): number
```

#### clearAudioExternalStreamBuffer

清空外部音频流缓存。无返回值，异步执行。

```typescript
clearAudioExternalStreamBuffer(streamId: string, fadeoutMs: number): void
```

| **参数**    | **类型** | **说明**                      |
| --------- | ------ | --------------------------- |
| fadeoutMs | number | -1 默认淡出；0 立即清空；>0 保留指定毫秒后淡出 |

#### removeAudioExternalStream

```typescript
removeAudioExternalStream(streamId: string): number
```

### 实时消息

#### sendDataMsg

发送实时数据消息，通过 MoQT Data 通道传输。

```typescript
sendDataMsg(msg: AoqDataMsg): number
```

### 音频帧回调

#### setAudioFrameObserver

设置音频帧数据回调监听。先注册监听，再 `enableAudioFrameObserver` 开启回调。

```typescript
setAudioFrameObserver(observer: IAudioFrameObserver | null): number
```

#### enableAudioFrameObserver

```typescript
enableAudioFrameObserver(enabled: boolean, audioSource: AoqAudioSource, config: AoqAudioObserverConfig): number
```

### 视频帧回调

#### setVideoFrameObserver

```typescript
setVideoFrameObserver(observer: IVideoFrameObserver | null): number
```

#### enableVideoFrameObserver

```typescript
enableVideoFrameObserver(enabled: boolean, videoSource: AoqVideoSource, config: AoqVideoObserverConfig): number
```

### AoqEngineEventListener 回调

所有回调均为可选属性（`?`）。

```typescript
export interface AoqEngineEventListener {
  onError?: (code: number, message: string) => void;
  onWarning?: (code: number, message: string) => void;
  onConnectionStatusChange?: (status: AoqConnectionStatus) => void;
  onStats?: (stats: AoqStats) => void;
  onAudioDeviceStateChanged?: (state: AoqAudioDeviceState) => void;
  onAudioDeviceRouteChanged?: (routeType: number) => void;
  onAudioDeviceInterrupted?: (interrupt: boolean) => void;
  onVideoDeviceStateChanged?: (state: AoqVideoDeviceState) => void;
  onAudioFileState?: (state: AoqAudioFileState) => void;
  onDataMsg?: (msg: AoqDataMsg) => void;
}
```

#### IAudioFrameObserver

```typescript
export interface IAudioFrameObserver {
  onCapturedAudioFrame?: (frame: AoqAudioFrameData) => void;
  onProcessCapturedAudioFrame?: (frame: AoqAudioFrameData) => void;
  onPublishAudioFrame?: (trackType: AoqTrackType, frame: AoqAudioFrameData) => void;
  onPlaybackAudioFrame?: (frame: AoqAudioFrameData) => void;
}
```

`frame.dataPtr` 是 native 内存的 Uint8Array 拷贝，当前 ReadOnly（修改不写回 SDK）。

#### IVideoFrameObserver

```typescript
export interface IVideoFrameObserver {
  onCapturedVideoFrame?: (frame: AoqVideoFrame) => boolean;
  onPreEncodeVideoFrame?: (trackType: AoqTrackType, frame: AoqVideoFrame) => boolean;
  onRemoteVideoFrame?: (trackType: AoqTrackType, frame: AoqVideoFrame) => boolean;
}
```

frame 各 buffer 是 native 内存的 Uint8Array 拷贝，回调期间有效。当前等效 ReadOnly，P2 实现真写回。

## 数据类型与枚举

### 通用类型

#### AoqCreateConfig

| **字段**          | **类型**  | **默认值** | **说明**               |
| --------------- | ------- | ------- | -------------------- |
| workDir         | string  | ""      | SDK 工作目录             |
| enableDumpAudio | boolean | false   | 是否开启音频原始数据 dump（调试用） |
| extras          | string  | ""      | 扩展参数字符串              |

与 Android 不同：OHOS 无 `isBTScoMode` 字段。

#### AoqConnectConfig

| **字段**          | **类型**              | **默认值** | **说明**       |
| --------------- | ------------------- | ------- | ------------ |
| token           | string              | ""      | 连接鉴权 Token   |
| sid             | string              | ""      | 会话 ID        |
| certFingerprint | string              | ""      | 服务器证书指纹      |
| relayEndpoints  | AoqRelayEndpoint\[] | \[]     | Relay 接入点列表  |
| workspaceIdHash | string              | ""      | 工作空间 ID Hash |
| publishTracks   | AoqTrackParam\[]    | \[]     | 本端计划发布的轨道列表  |
| subscribeTracks | AoqTrackParam\[]    | \[]     | 本端计划订阅的轨道列表  |

#### AoqRelayEndpoint

| **字段**   | **类型** | **说明**          |
| -------- | ------ | --------------- |
| endpoint | string | Relay 服务器域名或 IP |
| port     | number | Relay 服务器端口     |

#### AoqTrackParam

| **字段**    | **类型**       | **说明** |
| --------- | ------------ | ------ |
| trackType | AoqTrackType | 轨道类型   |

#### AoqErrorCode

| **枚举值**                                  | **值** | **说明**           |
| ---------------------------------------- | ----- | ---------------- |
| AoqECOK                                  | 0     | 成功               |
| AoqECParamInvalid                        | 1     | 参数非法             |
| AoqECStateInvalid                        | 2     | 状态非法             |
| AoqECUnSupport                           | 3     | 不支持              |
| AoqECAudio                               | 100   | 音频通用错误           |
| AoqECAudioExternalBufferFull             | 110   | 外部音频缓冲区满         |
| AoqECAudioDevice                         | 120   | 音频设备通用错误         |
| AoqECAudioDeviceRecordingAuthFailed      | 121   | 录音权限未获取          |
| AoqECAudioDeviceRecordingOccupied        | 122   | 录音设备被占用          |
| AoqECAudioDeviceRecordingBackgroundStart | 123   | 后台启动录音失败         |
| AoqECAudioDeviceRecordingStartFail       | 124   | 录音启动失败           |
| AoqECAudioDevicePlayoutOccupied          | 125   | 播放设备被占用          |
| AoqECAudioDevicePlayoutBackgroundStart   | 126   | 后台启动播放失败         |
| AoqECAudioDevicePlayoutStartFail         | 127   | 播放启动失败           |
| AoqECAudioDeviceEarpieceRequiresVoipMode | 128   | 听筒模式需要启用 VoIP 模式 |
| AoqECVideo                               | 200   | 视频通用错误           |
| AoqECVideoExternalBufferFull             | 210   | 外部视频缓冲区满         |
| AoqECVideoExternalCaptureNotEnabled      | 211   | 外部视频采集未启用        |
| AoqECVideoExternalEncoderNotEnabled      | 212   | 外部视频编码器未启用       |
| AoqECVideoDevice                         | 220   | 视频设备通用错误         |
| AoqECVideoDeviceCameraOpenFail           | 221   | 摄像头打开失败          |
| AoqECVideoDeviceCameraAuthFailed         | 222   | 摄像头权限未获取         |
| AoqECVideoDeviceCameraOccupied           | 223   | 摄像头被占用           |
| AoqECVideoDeviceCameraRunningError       | 224   | 摄像头运行异常          |
| AoqECVideoCodec                          | 230   | 视频编解码通用错误        |
| AoqECVideoCodecEncoderInitFail           | 231   | 视频编码器初始化失败       |
| AoqECVideoRender                         | 240   | 视频渲染通用错误         |
| AoqECVideoRenderCreateFail               | 241   | 视频渲染创建失败         |
| AoqECVideoRenderDrawError                | 242   | 视频渲染绘制错误         |

#### AoqWarningCode

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

#### AoqTrackType

| **枚举值**           | **值** | **说明** |
| ----------------- | ----- | ------ |
| AoqTrackTypeAudio | 0     | 音频轨道   |
| AoqTrackTypeVideo | 1     | 视频轨道   |
| AoqTrackTypeData  | 2     | 数据消息轨道 |

与 Android 不同：OHOS 当前不包含 `AoqTrackTypeScreen`(3)，屏幕采集功能暂未对外开放。

#### AoqConnectionStatus

| **枚举值**                         | **值** | **说明** |
| ------------------------------- | ----- | ------ |
| AoqConnectionStatusDisconnected | 0     | 未连接    |
| AoqConnectionStatusConnecting   | 1     | 连接中    |
| AoqConnectionStatusConnected    | 2     | 已连接    |
| AoqConnectionStatusFailed       | 3     | 连接失败   |

#### AoqEncoderType / AoqMirrorMode / AoqOrientationMode

同原文档，无变化。

### 音频类型

#### AoqAudioCaptureConfig

| **字段**     | **类型**  | **默认值** | **说明**                  |
| ---------- | ------- | ------- | ----------------------- |
| isExternal | boolean | false   | true 使用外部音频输入           |
| isVoipMode | boolean | false   | true 启用 VoIP 模式（硬件 AEC） |
| channel    | number  | 1       | 声道数，支持 1/2              |

#### AoqAudioPlaybackConfig

| **字段**           | **类型**  | **默认值** | **说明**                              |
| ---------------- | ------- | ------- | ----------------------------------- |
| isVoipMode       | boolean | false   | true 启用 VoIP 模式（硬件 AEC），采集/播放参数先到为准 |
| isDefaultSpeaker | boolean | true    | true 默认扬声器；false 默认听筒               |
| isExternal       | boolean | false   | true 使用外部音频输出                       |
| channel          | number  | 1       | 声道数，支持 1/2                          |

#### AoqAudioCodecConfig

| **字段**     | **类型**         | **默认值**                | **说明**  |
| ---------- | -------------- | ---------------------- | ------- |
| trackType  | AoqTrackType   | AoqTrackTypeAudio      | 目标轨道    |
| codecType  | AoqEncoderType | AoqEncoderTypeAudioPCM | 编码格式    |
| sampleRate | number         | 48000                  | 采样率(Hz) |
| channel    | number         | 1                      | 声道数     |
| bitrate    | number         | 32000                  | 码率(bps) |

### 视频类型

#### AoqVideoCaptureConfig

| **字段**          | **类型**             | **默认值** | **说明**                                          |
| --------------- | ------------------ | ------- | ----------------------------------------------- |
| width           | number             | 1280    | 采集宽度；isExternal=true 时无效                        |
| height          | number             | 720     | 采集高度                                            |
| fps             | number             | 15      | 采集帧率                                            |
| isExternal      | boolean            | false   | true 不打开摄像头，由 pushExternalVideoCapturedFrame 喂帧 |
| cameraDirection | AoqCameraDirection | Front   | 摄像头方向                                           |

#### AoqVideoCodecConfig

| **字段**           | **类型**             | **默认值**                 | **说明**            |
| ---------------- | ------------------ | ----------------------- | ----------------- |
| trackType        | AoqTrackType       | AoqTrackTypeVideo       | 目标轨道              |
| codecType        | AoqEncoderType     | AoqEncoderTypeVideoH264 | 编码格式              |
| width            | number             | 720                     | 编码宽度              |
| height           | number             | 1280                    | 编码高度              |
| fps              | number             | 15                      | 帧率                |
| bitrate          | number             | 500                     | 码率(kbps)          |
| minBitrate       | number             | 128                     | 最小码率(kbps)        |
| keyframeInterval | number             | 2                       | 关键帧间隔(秒)          |
| mirrorMode       | AoqMirrorMode      | Disabled                | 镜像模式              |
| orientationMode  | AoqOrientationMode | Auto                    | 视频方向              |
| isExternal       | boolean            | false                   | true 时 SDK 不做二次编码 |

与 Android 不同：OHOS 码率单位为 kbps（默认 500/128），Android 为 bps（默认 500000/128000）。

#### AoqVideoCanvas

| **字段**     | **类型**         | **默认值**           | **说明**                                     |
| ---------- | -------------- | ----------------- | ------------------------------------------ |
| view       | Object \       | null              | null                                       | AoqXComponentController 实例；传 null 表示移除渲染绑定 |
| renderMode | AoqRenderMode  | AoqRenderModeAuto | 显示模式                                       |

#### AoqVideoPixelFormat

| **枚举值**                    | **值** | **说明** |
| -------------------------- | ----- | ------ |
| AoqVideoPixelFormatUnknown | 0     | 未知     |
| AoqVideoPixelFormatI420    | 1     | I420   |
| AoqVideoPixelFormatNV12    | 2     | NV12   |
| AoqVideoPixelFormatNV21    | 3     | NV21   |
| AoqVideoPixelFormatBGRA    | 4     | BGRA   |
| AoqVideoPixelFormatRGBA    | 5     | RGBA   |

OHOS 不支持 TextureOES/Texture2D。

#### AoqVideoFrame

| **字段**                      | **类型**                            | **说明**                 |
| --------------------------- | --------------------------------- | ---------------------- |
| format                      | AoqVideoPixelFormat               | 像素格式                   |
| width                       | number                            | 宽度(像素)                 |
| height                      | number                            | 高度(像素)                 |
| dataPtr                     | ArrayBuffer \                     | Uint8Array \           | null | 打包格式数据  |
| dataSize                    | number                            | 打包数据字节数                |
| dataY / dataU / dataV       | ArrayBuffer \                     | Uint8Array \           | null | I420 平面 |
| strideY / strideU / strideV | number                            | 平面 stride              |
| timeStamp                   | number                            | 时间戳(ms)；0 时 SDK 用本地时钟补 |

#### AoqVideoEncodedFrame

| **字段**    | **类型**                    | **说明**                         |
| --------- | ------------------------- | ------------------------------ |
| codec     | AoqVideoCodecType         | 编码格式 (AoqVideoCodecTypeJPEG=0) |
| data      | ArrayBuffer \             | Uint8Array                     | 编码后数据 |
| width     | number                    | 宽度                             |
| height    | number                    | 高度                             |
| timeStamp | number                    | 时间戳(ms)                        |

### 音频文件与外部流类型

#### AoqAudioFileMixConfig

| **字段**        | **类型** | **默认值** | **说明**          |
| ------------- | ------ | ------- | --------------- |
| fileName      | string | ""      | 文件名（含路径）        |
| cycles        | number | -1      | 循环次数，-1 无限循环    |
| startPosMs    | number | 0       | 起始播放位置(ms)      |
| publishVolume | number | 100     | 推流音量 \[0,100]   |
| playoutVolume | number | 100     | 本地播放音量 \[0,100] |

#### AoqAudioExternalStreamConfig

| **字段**            | **类型**         | **默认值**                | **说明**         |
| ----------------- | -------------- | ---------------------- | -------------- |
| trackType         | AoqTrackType   | AoqTrackTypeAudio      | 轨道类型           |
| codecType         | AoqEncoderType | AoqEncoderTypeAudioPCM | 音频格式           |
| channels          | number         | 1                      | 声道数            |
| sampleRate        | number         | 48000                  | 采样率(Hz)        |
| playoutVolume     | number         | 100                    | 播放音量 \[0,100]  |
| publishVolume     | number         | 100                    | 推流音量 \[0,100]  |
| maxBufferDuration | number         | 1000                   | 最大缓冲(ms)       |
| enable3A          | boolean        | false                  | 输入 PCM 做 3A 处理 |

#### AoqAudioFrameData

| **字段**         | **类型**                            | **说明**              |
| -------------- | --------------------------------- | ------------------- |
| dataPtr        | ArrayBuffer \                     | Uint8Array \        | null | 音频 PCM 裸数据 |
| dataSize       | number                            | PCM 字节数             |
| numOfSamples   | number                            | 采样点数(单声道)           |
| bytesPerSample | number                            | 每采样点字节数             |
| numOfChannels  | number                            | 声道数                 |
| samplesPerSec  | number                            | 每秒采样点数              |
| pushSequence   | number                            | PCM 输入轮次            |
| timeStamp      | number                            | 时间戳                 |
| autoGenMute    | boolean                           | true 表示 SDK 生成的静音数据 |

### Observer 配置类型

#### AoqAudioObserverConfig

| **字段**     | **类型**               | **默认值**  | **说明** |
| ---------- | -------------------- | -------- | ------ |
| sampleRate | number               | 48000    | 回调采样率  |
| channels   | number               | 1        | 回调声道数  |
| mode       | AoqAudioObserverMode | ReadOnly | 读写模式   |

#### AoqVideoObserverConfig

| **字段**        | **类型**                    | **默认值**  | **说明** |
| ------------- | ------------------------- | -------- | ------ |
| format        | AoqVideoPixelFormat       | I420     | 回调像素格式 |
| alignment     | AoqVideoObserverAlignment | Default  | 宽度对齐   |
| mode          | AoqVideoObserverMode      | ReadOnly | 读写模式   |
| mirrorApplied | boolean                   | false    | 是否应用镜像 |

### 统计数据类型

#### AoqStats

| **字段**                | **类型**                      | **说明**   |
| --------------------- | --------------------------- | -------- |
| audioPublishStats     | AoqAudioPublishStats\[]     | 音频推流统计   |
| videoPublishStats     | AoqVideoPublishStats\[]     | 视频推流统计   |
| dataMsgPublishStats   | AoqDataMsgPublishStats\[]   | 数据消息推流统计 |
| audioSubscribeStats   | AoqAudioSubscribeStats\[]   | 音频拉流统计   |
| videoSubscribeStats   | AoqVideoSubscribeStats\[]   | 视频拉流统计   |
| dataMsgSubscribeStats | AoqDataMsgSubscribeStats\[] | 数据消息拉流统计 |
| networkStats          | AoqNetworkStats \           | null     | 网络统计 |

#### 统计子类型

**AoqAudioPublishStats**：trackType / bitrate / bytes / encodeVolume

**AoqVideoPublishStats**：trackType / bitrate / bytes / encodeFps

**AoqAudioSubscribeStats**：trackType / bitrate / bytes / playVolume

**AoqVideoSubscribeStats**：trackType / bitrate / bytes / decodeFps / renderFps

**AoqDataMsgPublishStats / AoqDataMsgSubscribeStats**：trackType / bitrate / bytes

**AoqNetworkStats**：sendBitrate / sendBytes / recvBitrate / recvBytes / loss / rtt

## 与 Android 版本的主要差异

| **类别**                    | **Android**                              | **OHOS**                                         |
| ------------------------- | ---------------------------------------- | ------------------------------------------------ |
| 实现语言                      | Java                                     | ArkTS(.ets)，NAPI 桥接 C++                          |
| 返回值类型                     | int / long / boolean                     | number / boolean                                 |
| createEngine 返回值          | @NonNull AoqClientEngine                 | AoqClientEngine \                                | null |
| createEngine context      | android.content.Context                  | common.Context (UIAbility/Page)                  |
| listener 形式               | abstract class，默认空实现                     | TS interface，所有回调 optional (?)                   |
| frame observer 形式         | interface + default 方法                   | TS interface，所有回调 optional (?)                   |
| AoqCreateConfig           | 包含 isBTScoMode                           | 不含 isBTScoMode                                   |
| AoqAudioPlaybackConfig    | 无 isVoipMode                             | 含 isVoipMode，采集/播放参数先到为准                         |
| onAudioDeviceFocusChanged | 提供                                       | 不提供（无音频焦点事件抽象）                                   |
| 视频渲染 view                 | View(SurfaceView/TextureView)            | AoqXComponentController(继承 XComponentController) |
| Pixel Format 枚举           | 包含 TextureOES(7) / Texture2D(8)          | 不包含纹理格式                                          |
| 视频帧附加字段                   | textureId / transformMatrix / eglContext | 无这些字段                                            |
| 帧数据容器                     | byte\[] / ByteBuffer                     | ArrayBuffer / Uint8Array                         |
| 视频编码码率单位                  | bps（默认 500000/128000）                    | kbps（默认 500/128）                                 |
| AoqTrackType              | 含 AoqTrackTypeScreen(3)                  | 不含 AoqTrackTypeScreen，屏幕采集暂未开放                   |
| 屏幕采集 API                  | startScreenCapture / stopScreenCapture   | 暂未提供                                             |
| Observer ReadWrite        | I420 支持写回                                | 当前等效 ReadOnly，P2 实现真回写                           |
| Observer 重注册安全            | 依赖 SDK 内部                                | UAF 防护墓地模式                                       |
| 设备监测能力                    | Java 侧隐含                                 | AoqDeviceMonitor(内部模块)自动启动                       |
| 枚举命名空间                    | AoqErrorCodeXxx                          | AoqECXxx (如 AoqECOK、AoqECParamInvalid)           |

### 主要设计要点

1. **AoqXComponentController**：继承自 XComponentController，重写 onSurfaceCreated/Changed/Destroyed。业务需创建后传入 XComponent，并在 setLocalView/setRemoteView 时作为 canvas.view。

2. **NAPI 架构**：facade (AoqClientEngine.ets) -> 实现层 (AoqClientEngineImpl.ets) -> NAPI (libaoq\_client\_sdk.so)。配置在实现层被拍平为多个参数。

3. **设备监测(内部)**：AoqDeviceMonitor 在 createEngine 后自动启动，下沉网络状态与 App 前后台状态到 C++ 引擎。

4. **Observer UAF 防护**：重注册时采用 "cpp 切旧引用 -> 旧 obs push 入墓地 -> 占位指新 obs" 三步顺序。

5. **帧负载语义**：音视频帧回调中的 Uint8Array 是 native 拷贝，P1 不支持写回，P2 计划零拷贝。
