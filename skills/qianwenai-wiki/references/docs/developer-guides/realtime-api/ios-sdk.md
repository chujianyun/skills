> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# iOS SDK

> AOQ iOS SDK API 参考

AOQ Client SDK iOS API 参考，涵盖引擎生命周期、音视频设备管理、编码配置、媒体流控制、音频文件播放、外部音频流、实时消息、帧回调、委托协议以及数据类型与枚举。

## 目录

### 引擎生命周期

| **接口**                 | **简介**       |
| ---------------------- | ------------ |
| createEngine:delegate: | 创建引擎实例（单例模式） |
| destroy                | 销毁引擎实例       |
| getVersion             | 获取 SDK 版本号   |
| connect:               | 连接 Relay 服务器 |
| disconnect             | 断开服务器连接      |

### 音频设备管理

| **接口**                       | **简介**                 |
| ---------------------------- | ---------------------- |
| startAudioCapture:           | 打开音频采集设备（麦克风）          |
| stopAudioCapture             | 关闭音频采集设备               |
| muteAudioCapture:            | 静音或取消静音音频采集            |
| startAudioPlayer:            | 开始音频渲染（播放远端音频）         |
| stopAudioPlayer              | 停止音频渲染                 |
| pauseAudioPlayer:            | 暂停音频渲染，支持淡出            |
| resumeAudioPlayer:           | 恢复音频渲染，支持淡入            |
| interruptAudioPlayer:fadeMs: | 打断本轮音频通话               |
| enableSpeakerphone:          | 切换音频输出到扬声器或听筒          |
| isSpeakerphoneEnabled        | 查询当前是否使用扬声器输出          |
| setAudioSessionRestriction:  | 设置 AVAudioSession 控制权限 |

### 音频编码配置

| **接口**                 | **简介**   |
| ---------------------- | -------- |
| setAudioEncoderConfig: | 设置音频编码参数 |
| setAudioDecoderConfig: | 设置音频解码参数 |

### 视频设备管理

| **接口**                | **简介**        |
| --------------------- | ------------- |
| startVideoCapture:    | 打开视频采集设备（摄像头） |
| stopVideoCapture      | 关闭视频采集设备      |
| switchCamera:         | 切换前后置摄像头      |
| setLocalView:canvas:  | 设置或移除本地视频渲染窗口 |
| setRemoteView:canvas: | 设置或移除远端视频渲染窗口 |

### 视频编码与外部输入

| **接口**                                | **简介**     |
| ------------------------------------- | ---------- |
| setVideoEncoderConfig:                | 设置视频编码参数   |
| pushExternalVideoCapturedFrame:frame: | 推送外部采集视频帧  |
| pushExternalVideoEncodedFrame:frame:  | 推送外部已编码视频帧 |

### 媒体流发送控制

| **接口**                        | **简介**       |
| ----------------------------- | ------------ |
| enableSendMediaStream:enable: | 控制本地媒体流的发送开关 |

### 音频文件播放

| **接口**                                     | **简介**           |
| ------------------------------------------ | ---------------- |
| startAudioFile:config:                     | 开始推流播放本地音频文件     |
| stopAudioFile:                             | 停止音频文件播放         |
| pauseAudioFile:                            | 暂停音频文件播放         |
| resumeAudioFile:                           | 恢复音频文件播放         |
| getAudioFileDuration:                      | 获取音频文件总时长        |
| getAudioFileCurrentPosition:               | 获取音频文件当前播放位置     |
| setAudioFilePositionMillis:positionMillis: | 设置音频文件播放位置（seek） |
| setAudioFileVolume:type:volume:            | 设置音频文件音量         |
| getAudioFileVolume:type:                   | 获取音频文件当前音量       |

### 外部音频流

| **接口**                                    | **简介**        |
| ----------------------------------------- | ------------- |
| addAudioExternalStream:config:            | 新增一条外部音频流     |
| removeAudioExternalStream:                | 移除外部音频流       |
| pushAudioExternalStreamData:data:         | 输入外部音频 PCM 数据 |
| setAudioExternalStreamVolume:type:volume: | 设置外部音频流音量     |
| getAudioExternalStreamVolume:type:        | 获取外部音频流音量     |
| clearAudioExternalStreamBuffer:fadeoutMs: | 清空外部音频流缓存     |

### 实时消息

| **接口**       | **简介**   |
| ------------ | -------- |
| sendDataMsg: | 发送实时数据消息 |

### 音频帧回调

| **接口**                                       | **简介**             |
| -------------------------------------------- | ------------------ |
| setAudioFrameObserver:                       | 设置音频帧数据回调 delegate |
| enableAudioFrameObserver:audioSource:config: | 开启或关闭指定位置的音频帧回调    |

### 视频帧回调

| **接口**                                       | **简介**             |
| -------------------------------------------- | ------------------ |
| setVideoFrameObserver:                       | 设置视频帧数据回调 delegate |
| enableVideoFrameObserver:videoSource:config: | 开启或关闭指定位置的视频帧回调    |

### AoqEngineDelegate 回调

| **回调**                     | **简介**       |
| -------------------------- | ------------ |
| onError:message:           | 引擎错误回调       |
| onWarning:message:         | 引擎警告回调       |
| onConnectionStatusChange:  | 连接状态变化回调     |
| onStats:                   | 统计数据回调       |
| onAudioDeviceStateChanged: | 音频设备操作状态变化回调 |
| onAudioDeviceRouteChanged: | 音频输出路由变化回调   |
| onAudioDeviceInterrupted:  | 音频设备中断回调     |
| onVideoDeviceStateChanged: | 视频设备操作状态变化回调 |
| onAudioFileState:          | 音频文件播放状态回调   |
| onDataMsg:                 | 收到实时数据消息回调   |
| AoqAudioFrameDelegate      | 音频帧数据监听协议    |
| AoqVideoFrameDelegate      | 视频帧数据监听协议    |

## 接口详情

### 引擎生命周期

#### createEngine:delegate:

创建引擎实例。SDK 内部以全局单例方式持有引擎。

```objectivec
+ (instancetype _Nonnull)createEngine:(AoqCreateConfig * _Nonnull)config
                             delegate:(id<AoqEngineDelegate> _Nonnull)delegate;
```

#### destroy

```objectivec
+ (int)destroy;
```

#### getVersion

```objectivec
+ (NSString * _Nonnull)getVersion;
```

#### connect:

```objectivec
- (int)connect:(AoqConnectConfig * _Nonnull)config;
```

#### disconnect

```objectivec
- (int)disconnect;
```

### 音频设备管理

```objectivec
- (int)startAudioCapture:(AoqAudioCaptureConfig * _Nonnull)config;
- (int)stopAudioCapture;
- (int)muteAudioCapture:(BOOL)mute;
- (int)startAudioPlayer:(AoqAudioPlaybackConfig * _Nonnull)config;
- (int)stopAudioPlayer;
- (int)pauseAudioPlayer:(NSInteger)fadeMs;
- (int)resumeAudioPlayer:(NSInteger)fadeMs;
- (int)interruptAudioPlayer:(AoqTrackType)trackType fadeMs:(NSInteger)fadeMs;
- (int)enableSpeakerphone:(BOOL)enable;
- (BOOL)isSpeakerphoneEnabled;
- (int)setAudioSessionRestriction:(int)restriction;
```

### 音频编码配置

```objectivec
- (int)setAudioEncoderConfig:(AoqAudioCodecConfig * _Nonnull)config;
- (int)setAudioDecoderConfig:(AoqAudioCodecConfig * _Nonnull)config;
```

### 视频设备管理

```objectivec
- (int)startVideoCapture:(AoqVideoCaptureConfig * _Nonnull)config;
- (int)stopVideoCapture;
- (int)switchCamera:(AoqCameraDirection)direction;
- (int)setLocalView:(AoqTrackType)trackType canvas:(AoqVideoCanvas * _Nullable)canvas;
- (int)setRemoteView:(AoqTrackType)trackType canvas:(AoqVideoCanvas * _Nullable)canvas;
```

setLocalView/setRemoteView 的 trackType 参数传 AoqTrackTypeVideo。

### 视频编码与外部输入

```objectivec
- (int)setVideoEncoderConfig:(AoqVideoCodecConfig * _Nonnull)config;
- (int)pushExternalVideoCapturedFrame:(AoqTrackType)trackType frame:(AoqVideoFrame * _Nonnull)frame;
- (int)pushExternalVideoEncodedFrame:(AoqTrackType)trackType frame:(AoqVideoEncodedFrame * _Nonnull)frame;
```

trackType 参数传 AoqTrackTypeVideo。

### 媒体流发送控制

```objectivec
- (int)enableSendMediaStream:(AoqTrackType)trackType enable:(BOOL)enable;
```

trackType 支持 AoqTrackTypeAudio / AoqTrackTypeVideo。

### 音频文件播放

```objectivec
- (int)startAudioFile:(NSString * _Nonnull)fileId config:(AoqAudioFileMixConfig * _Nonnull)config;
- (int)stopAudioFile:(NSString * _Nonnull)fileId;
- (int)pauseAudioFile:(NSString * _Nonnull)fileId;
- (int)resumeAudioFile:(NSString * _Nonnull)fileId;
- (long long)getAudioFileDuration:(NSString * _Nonnull)fileId;
- (long long)getAudioFileCurrentPosition:(NSString * _Nonnull)fileId;
- (int)setAudioFilePositionMillis:(NSString * _Nonnull)fileId positionMillis:(long long)positionMillis;
- (int)setAudioFileVolume:(NSString * _Nonnull)fileId type:(AoqAudioStreamDirection)type volume:(NSInteger)volume;
- (int)getAudioFileVolume:(NSString * _Nonnull)fileId type:(AoqAudioStreamDirection)type;
```

### 外部音频流

```objectivec
- (int)addAudioExternalStream:(NSString * _Nonnull)streamId config:(AoqAudioExternalStreamConfig * _Nonnull)config;
- (int)pushAudioExternalStreamData:(NSString * _Nonnull)streamId data:(AoqAudioFrameData * _Nonnull)data;
- (int)setAudioExternalStreamVolume:(NSString * _Nonnull)streamId type:(AoqAudioStreamDirection)type volume:(NSInteger)volume;
- (int)getAudioExternalStreamVolume:(NSString * _Nonnull)streamId type:(AoqAudioStreamDirection)type;
- (void)clearAudioExternalStreamBuffer:(NSString * _Nonnull)streamId fadeoutMs:(NSInteger)fadeoutMs;
- (int)removeAudioExternalStream:(NSString * _Nonnull)streamId;
```

### 实时消息

```objectivec
- (int)sendDataMsg:(AoqDataMsg * _Nonnull)msg;
```

### 音频帧回调

```objectivec
- (int)setAudioFrameObserver:(id<AoqAudioFrameDelegate> _Nullable)delegate;
- (int)enableAudioFrameObserver:(BOOL)enabled audioSource:(AoqAudioSource)audioSource config:(AoqAudioObserverConfig * _Nonnull)config;
```

### 视频帧回调

```objectivec
- (int)setVideoFrameObserver:(id<AoqVideoFrameDelegate> _Nullable)delegate;
- (int)enableVideoFrameObserver:(BOOL)enabled videoSource:(AoqVideoSource)videoSource config:(AoqVideoObserverConfig * _Nonnull)config;
```

### AoqEngineDelegate 回调

所有回调方法均为 @required。

```objectivec
- (void)onError:(NSInteger)code message:(NSString * _Nonnull)message;
- (void)onWarning:(NSInteger)code message:(NSString * _Nonnull)message;
- (void)onConnectionStatusChange:(AoqConnectionStatus)status;
- (void)onStats:(AoqStats * _Nonnull)stats;
- (void)onAudioDeviceStateChanged:(AoqAudioDeviceState * _Nonnull)state;
- (void)onAudioDeviceRouteChanged:(NSInteger)routeType;
- (void)onAudioDeviceInterrupted:(BOOL)interrupt;
- (void)onAudioFileState:(AoqAudioFileState * _Nonnull)state;
- (void)onVideoDeviceStateChanged:(AoqVideoDeviceState * _Nonnull)state;
- (void)onDataMsg:(AoqDataMsg * _Nonnull)msg;
```

#### AoqAudioFrameDelegate (@optional)

```objectivec
- (void)onCapturedAudioFrame:(AoqAudioFrameData * _Nonnull)frame;
- (void)onProcessCapturedAudioFrame:(AoqAudioFrameData * _Nonnull)frame;
- (void)onPublishAudioFrame:(AoqTrackType)trackType frame:(AoqAudioFrameData * _Nonnull)frame;
- (void)onPlaybackAudioFrame:(AoqAudioFrameData * _Nonnull)frame;
```

#### AoqVideoFrameDelegate (@optional)

```objectivec
- (BOOL)onCapturedVideoFrame:(AoqVideoFrame * _Nonnull)frame;
- (BOOL)onPreEncodeVideoFrame:(AoqTrackType)trackType frame:(AoqVideoFrame * _Nonnull)frame;
- (BOOL)onRemoteVideoFrame:(AoqTrackType)trackType frame:(AoqVideoFrame * _Nonnull)frame;
```

## 数据类型与枚举

### AoqErrorCode

| **枚举值**                                         | **值** | **说明**         |
| ----------------------------------------------- | ----- | -------------- |
| AoqErrorCodeOK                                  | 0     | 成功             |
| AoqErrorCodeParamInvalid                        | 1     | 参数非法           |
| AoqErrorCodeStateInvalid                        | 2     | 状态非法           |
| AoqErrorCodeUnSupport                           | 3     | 不支持的操作         |
| AoqErrorCodeAudio                               | 100   | 音频通用错误         |
| AoqErrorCodeAudioExternalBufferFull             | 110   | 外部音频缓冲区满       |
| AoqErrorCodeAudioDevice                         | 120   | 音频设备通用错误       |
| AoqErrorCodeAudioDeviceRecordingAuthFailed      | 121   | 录音权限未获取        |
| AoqErrorCodeAudioDeviceRecordingOccupied        | 122   | 录音设备被占用        |
| AoqErrorCodeAudioDeviceRecordingBackgroundStart | 123   | 后台启动录音失败       |
| AoqErrorCodeAudioDeviceRecordingStartFail       | 124   | 录音启动失败         |
| AoqErrorCodeAudioDevicePlayoutOccupied          | 125   | 播放设备被占用        |
| AoqErrorCodeAudioDevicePlayoutBackgroundStart   | 126   | 后台启动播放失败       |
| AoqErrorCodeAudioDevicePlayoutStartFail         | 127   | 播放启动失败         |
| AoqErrorCodeAudioDeviceEarpieceRequiresVoipMode | 128   | 听筒输出需要 VoIP 模式 |
| AoqErrorCodeVideo                               | 200   | 视频通用错误         |
| AoqErrorCodeVideoExternalBufferFull             | 210   | 外部视频缓冲区满       |
| AoqErrorCodeVideoExternalCaptureNotEnabled      | 211   | 外部视频采集未启用      |
| AoqErrorCodeVideoExternalEncoderNotEnabled      | 212   | 外部视频编码未启用      |
| AoqErrorCodeVideoDevice                         | 220   | 视频设备通用错误       |
| AoqErrorCodeVideoDeviceCameraOpenFail           | 221   | 摄像头打开失败        |
| AoqErrorCodeVideoDeviceCameraAuthFailed         | 222   | 摄像头权限未获取       |
| AoqErrorCodeVideoDeviceCameraOccupied           | 223   | 摄像头被占用         |
| AoqErrorCodeVideoDeviceCameraRunningError       | 224   | 摄像头运行异常        |
| AoqErrorCodeVideoCodec                          | 230   | 视频编解码通用错误      |
| AoqErrorCodeVideoCodecEncoderInitFail           | 231   | 视频编码器初始化失败     |
| AoqErrorCodeVideoRender                         | 240   | 视频渲染通用错误       |
| AoqErrorCodeVideoRenderCreateFail               | 241   | 视频渲染创建失败       |
| AoqErrorCodeVideoRenderDrawError                | 242   | 视频渲染绘制错误       |

### AoqTrackType

| **枚举值**           | **值** | **说明** |
| ----------------- | ----- | ------ |
| AoqTrackTypeAudio | 0     | 音频轨道   |
| AoqTrackTypeVideo | 1     | 视频轨道   |
| AoqTrackTypeData  | 2     | 数据消息轨道 |

### AoqConnectConfig

| **字段**          | **类型**                           | **说明**       |
| --------------- | -------------------------------- | ------------ |
| token           | NSString \*                      | 连接鉴权 Token   |
| sid             | NSString \*                      | 会话 ID        |
| certFingerprint | NSString \*                      | 服务器证书指纹      |
| relayEndpoints  | NSArray\<AoqRelayEndpoint \*> \* | Relay 接入点列表  |
| workspaceIdHash | NSString \*                      | 工作空间 ID Hash |
| publishTracks   | NSArray\<AoqTrackParam \*> \*    | 本端计划发布的轨道列表  |
| subscribeTracks | NSArray\<AoqTrackParam \*> \*    | 本端计划订阅的轨道列表  |

### AoqAudioPlaybackConfig

| **字段**           | **类型**    | **默认值** | **说明**                       |
| ---------------- | --------- | ------- | ---------------------------- |
| isVoipMode       | BOOL      | NO      | YES 启用 VoIP 模式（硬件 AEC），移动端有效 |
| isDefaultSpeaker | BOOL      | YES     | YES 默认扬声器；NO 听筒              |
| isExternal       | BOOL      | NO      | YES 外部音频输出                   |
| channel          | NSInteger | 1       | 声道数 1/2                      |

### 统计数据类型

#### AoqStats

| **字段**                | **类型**                                   | **说明**   |
| --------------------- | ---------------------------------------- | -------- |
| audioPublishStats     | NSArray\<AoqAudioPublishStats \*> \*     | 音频推流统计   |
| videoPublishStats     | NSArray\<AoqVideoPublishStats \*> \*     | 视频推流统计   |
| dataMsgPublishStats   | NSArray\<AoqDataMsgPublishStats \*> \*   | 数据消息推流统计 |
| audioSubscribeStats   | NSArray\<AoqAudioSubscribeStats \*> \*   | 音频拉流统计   |
| videoSubscribeStats   | NSArray\<AoqVideoSubscribeStats \*> \*   | 视频拉流统计   |
| dataMsgSubscribeStats | NSArray\<AoqDataMsgSubscribeStats \*> \* | 数据消息拉流统计 |
| networkStats          | AoqNetworkStats \*                       | 网络统计     |

#### AoqNetworkStats

| **字段**      | **类型**     | **说明**    |
| ----------- | ---------- | --------- |
| sendBitrate | NSUInteger | 发送码率(bps) |
| sendBytes   | NSUInteger | 累计发送字节    |
| recvBitrate | NSUInteger | 接收码率(bps) |
| recvBytes   | NSUInteger | 累计接收字节    |
| loss        | NSUInteger | 丢包率       |
| rtt         | NSUInteger | 往返时延(ms)  |

#### AoqAudioPublishStats

trackType / bitrate / bytes / encodeVolume

#### AoqVideoPublishStats

trackType / bitrate / bytes / encodeFps

#### AoqAudioSubscribeStats

trackType / bitrate / bytes / playVolume

#### AoqVideoSubscribeStats

trackType / bitrate / bytes / decodeFps / renderFps

#### AoqDataMsgPublishStats / AoqDataMsgSubscribeStats

trackType / bitrate / bytes

## 与 Android 版本的主要差异

| **差异点**           | **iOS**                               | **Android**                 |
| ----------------- | ------------------------------------- | --------------------------- |
| 回调模式              | @protocol delegate                    | abstract class listener     |
| AVAudioSession 控制 | setAudioSessionRestriction:（iOS 独有）   | 无对应接口                       |
| 音频焦点回调            | 无（iOS 用 onAudioDeviceInterrupted: 代替） | onAudioDeviceFocusChanged   |
| 视频像素格式            | 支持 CVPixelBuffer 零拷贝                  | 支持 TextureOES / Texture2D   |
| 视频渲染 View         | UIView                                | SurfaceView / TextureView   |
| 蓝牙模式配置            | 无 isBTScoMode（系统自动管理）                 | AoqCreateConfig.isBTScoMode |
| 视频帧回调写回           | I420 / CVPixelBuffer                  | I420                        |
