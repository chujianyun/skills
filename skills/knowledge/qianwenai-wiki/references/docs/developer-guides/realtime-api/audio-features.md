> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 音频常用功能介绍

> AOQ SDK 音频采集、播放、编解码配置

AOQ Client SDK 提供了完整的音频能力，覆盖音频采集、播放、编解码配置、扬声器管理、文件混音、外部音频流注入、音频帧数据回调等核心场景。本文档基于 Android（Java）、iOS（Objective-C）、Ohos（ArkTS）三个平台的公开 API，对音频常用功能进行统一介绍。

## 音频采集

音频采集用于打开设备麦克风，将实时音频数据送入 SDK 编码推流管线。SDK 支持两种采集模式：

- **内部采集**（默认）：SDK 自动管理麦克风设备的打开、录音和关闭。
- **外部采集**：由应用自行管理麦克风，采集到的 PCM 数据通过外部音频流接口输入 SDK。

### 配置参数

| **参数**     | **类型** | **默认值** | **说明**                                |
| ---------- | ------ | ------- | ------------------------------------- |
| isExternal | bool   | false   | 是否使用外部采集模式                            |
| isVoipMode | bool   | false   | 是否启用 VoIP 模式（硬件 AEC），移动端有效，采集播放参数先到为准 |
| channel    | int    | 1       | 采集通道数，支持 1（单声道）/ 2（立体声）               |

### API 对照

| **功能**  | **Android**                 | **iOS**                     | **Ohos**                    |
| ------- | --------------------------- | --------------------------- | --------------------------- |
| 开启采集    | `startAudioCapture(config)` | `startAudioCapture:config:` | `startAudioCapture(config)` |
| 关闭采集    | `stopAudioCapture()`        | `stopAudioCapture`          | `stopAudioCapture()`        |
| 静音/取消静音 | `muteAudioCapture(mute)`    | `muteAudioCapture:`         | `muteAudioCapture(mute)`    |

### 使用示例

**Android**

```java
AoqAudioCaptureConfig config = new AoqAudioCaptureConfig();
config.isVoipMode = true;
config.channel = 1;
engine.startAudioCapture(config);
```

**iOS**

```objectivec
AoqAudioCaptureConfig *config = [[AoqAudioCaptureConfig alloc] init];
config.isVoipMode = YES;
config.channel = 1;
[engine startAudioCapture:config];
```

**Ohos**

```javascript
const config: AoqAudioCaptureConfig = { isVoipMode: true, channel: 1 };
engine.startAudioCapture(config);
```

## 音频播放

音频播放用于将接收到的远端音频数据渲染到本地扬声器或耳机。SDK 支持播放暂停/恢复（带淡入淡出）、打断当前轮音频通话等高级控制。

### 配置参数

| **参数**           | **类型** | **默认值** | **说明**                               |
| ---------------- | ------ | ------- | ------------------------------------ |
| isVoipMode       | bool   | false   | 是否启用 VoIP 模式（硬件AEC），移动端有效，采集播放参数先到为准 |
| isDefaultSpeaker | bool   | true    | 是否默认使用扬声器（移动端有效，非VoIP时无效）            |
| isExternal       | bool   | false   | 是否使用外部播放模式                           |
| channel          | int    | 1       | 播放通道数，支持 1（单声道）/ 2（立体声）              |

### API 对照

| **功能** | **Android**                               | **iOS**                        | **Ohos**                                  |
| ------ | ----------------------------------------- | ------------------------------ | ----------------------------------------- |
| 开始播放   | `startAudioPlayer(config)`                | `startAudioPlayer:config:`     | `startAudioPlayer(config)`                |
| 停止播放   | `stopAudioPlayer()`                       | `stopAudioPlayer`              | `stopAudioPlayer()`                       |
| 暂停播放   | `pauseAudioPlayer(fadeMs)`                | `pauseAudioPlayer:`            | `pauseAudioPlayer(fadeMs)`                |
| 恢复播放   | `resumeAudioPlayer(fadeMs)`               | `resumeAudioPlayer:`           | `resumeAudioPlayer(fadeMs)`               |
| 打断通话   | `interruptAudioPlayer(trackType, fadeMs)` | `interruptAudioPlayer:fadeMs:` | `interruptAudioPlayer(trackType, fadeMs)` |

<Note>
  **fadeMs 参数**：暂停和恢复播放时的淡入/淡出时长（毫秒），设为 0 则立即切换。
</Note>

## 扬声器管理

控制音频输出设备在扬声器和听筒之间切换。

| **功能**  | **Android**                  | **iOS**                 | **Ohos**                     |
| ------- | ---------------------------- | ----------------------- | ---------------------------- |
| 切换扬声器   | `enableSpeakerphone(enable)` | `enableSpeakerphone:`   | `enableSpeakerphone(enable)` |
| 查询扬声器状态 | `isSpeakerphoneEnabled()`    | `isSpeakerphoneEnabled` | `isSpeakerphoneEnabled()`    |

<Note>
  需要在 VoIP 模式下才允许切换，非 VoIP 时，`enableSpeakerphone` 调用有 OnError(AoqECAudioDeviceEarpieceRequiresVoipMode) 错误通知。
</Note>

<Note>
  **iOS 特殊行为**：iPad 设备只有扬声器模式；当 AVAudioSession 不是 PlayAndRecord 类别时，也始终返回 YES。
</Note>

## 音频编解码配置

设置音频上行（编码器）和下行（解码器）的编码格式、采样率、声道数和码率。表示推流/拉流的格式。

### 配置参数

| **参数**     | **类型**         | **默认值**  | **说明**                                       |
| ---------- | -------------- | -------- | -------------------------------------------- |
| trackType  | AoqTrackType   | Audio    | 音频轨道类型，当前只支持一条音频流                            |
| codecType  | AoqEncoderType | AudioPCM | 编码类型：AudioPCM(1) 或 AudioOpus(2)              |
| sampleRate | int            | 48000    | 采样率，Opus 支持 8K/16K/48K，PCM 支持 8K/16K/32K/48K |
| channel    | int            | 1        | 声道数，支持 1（单声道）/ 2（立体声）                        |
| bitrate    | int            | 32000    | 码率（bps）                                      |

### API 对照

| **功能** | **Android**                     | **iOS**                  | **Ohos**                        |
| ------ | ------------------------------- | ------------------------ | ------------------------------- |
| 设置编码参数 | `setAudioEncoderConfig(config)` | `setAudioEncoderConfig:` | `setAudioEncoderConfig(config)` |
| 设置解码参数 | `setAudioDecoderConfig(config)` | `setAudioDecoderConfig:` | `setAudioDecoderConfig(config)` |

### 支持的编码格式

| **枚举值**                 | **数值** | **说明**  |
| ----------------------- | ------ | ------- |
| AoqEncoderTypeAudioPCM  | 1      | PCM 裸音频 |
| AoqEncoderTypeAudioOpus | 2      | Opus 编码 |

## 音频文件混音

支持将本地音频文件混入当前音频流中一起推流和/或本地播放。每个音频文件通过业务自分配的 `fileId` 标识，可同时管理多个文件实例。

### 混音配置参数

| **参数**        | **类型** | **默认值** | **说明**          |
| ------------- | ------ | ------- | --------------- |
| fileName      | String | -       | 音频文件路径（含文件名）    |
| cycles        | int    | -1      | 循环次数，-1 表示无限循环  |
| startPosMs    | long   | 0       | 起始播放位置（毫秒）      |
| publishVolume | int    | 100     | 推流音量 \[0-100]   |
| playoutVolume | int    | 100     | 本地播放音量 \[0-100] |

### API 对照

| **功能** | **Android**                               | **iOS**                                      | **Ohos**                                  |
| ------ | ----------------------------------------- | -------------------------------------------- | ----------------------------------------- |
| 开始播放   | `startAudioFile(fileId, config)`          | `startAudioFile:config:`                     | `startAudioFile(fileId, config)`          |
| 停止播放   | `stopAudioFile(fileId)`                   | `stopAudioFile:`                             | `stopAudioFile(fileId)`                   |
| 暂停     | `pauseAudioFile(fileId)`                  | `pauseAudioFile:`                            | `pauseAudioFile(fileId)`                  |
| 恢复     | `resumeAudioFile(fileId)`                 | `resumeAudioFile:`                           | `resumeAudioFile(fileId)`                 |
| 获取文件时长 | `getAudioFileDuration(fileId)`            | `getAudioFileDuration:`                      | `getAudioFileDuration(fileId)`            |
| 获取当前位置 | `getAudioFileCurrentPosition(fileId)`     | `getAudioFileCurrentPosition:`               | `getAudioFileCurrentPosition(fileId)`     |
| 设置播放位置 | `setAudioFilePositionMillis(fileId, pos)` | `setAudioFilePositionMillis:positionMillis:` | `setAudioFilePositionMillis(fileId, pos)` |
| 设置音量   | `setAudioFileVolume(fileId, type, vol)`   | `setAudioFileVolume:type:volume:`            | `setAudioFileVolume(fileId, type, vol)`   |
| 获取音量   | `getAudioFileVolume(fileId, type)`        | `getAudioFileVolume:type:`                   | `getAudioFileVolume(fileId, type)`        |

<Note>
  **音量方向（type）**：`AoqAudioStreamPublish(0)` 控制推流音量；`AoqAudioStreamPlayout(1)` 控制本地播放音量。
</Note>

### 状态回调

| **状态码**                  | **数值** | **说明** |
| ------------------------ | ------ | ------ |
| AoqAudioFileNone         | 0      | 初始状态   |
| AoqAudioFileStarted      | 1      | 已开始播放  |
| AoqAudioFileStopped      | 2      | 已停止    |
| AoqAudioFilePaused       | 3      | 已暂停    |
| AoqAudioFileResumed      | 4      | 已恢复    |
| AoqAudioFileEnded        | 5      | 播放结束   |
| AoqAudioFileBuffering    | 6      | 缓冲中    |
| AoqAudioFileBufferingEnd | 7      | 缓冲结束   |
| AoqAudioFileFailed       | 8      | 播放失败   |

## 外部音频流

外部音频流允许将应用生成的 PCM 音频数据注入到 SDK 的音频管线中，支持推流和/或本地播放。典型场景包括 TTS 语音合成输出、AI 模型音频输出、背景音效等。每个外部音频流通过业务自分配的 `streamId` 标识。

### 配置参数

| **参数**            | **类型**         | **默认值**  | **说明**                                             |
| ----------------- | -------------- | -------- | -------------------------------------------------- |
| trackType         | AoqTrackType   | Audio    | 音频轨道类型                                             |
| codecType         | AoqEncoderType | AudioPCM | 音频流格式                                              |
| channels          | int            | 1        | 声道数                                                |
| sampleRate        | int            | 48000    | 采样率，支持 8/12/16/24/32/44.1/48/64/88.2/96/176.4/192K |
| playoutVolume     | int            | 100      | 本地播放音量 \[0-100]                                    |
| publishVolume     | int            | 100      | 推流音量 \[0-100]                                      |
| maxBufferDuration | int            | 600000   | 最大缓冲时长（毫秒），取值范围 \[100, \~]，超过时 Push 失败             |
| enable3A          | bool           | false    | 输入 PCM 是否经过 3A 处理                                  |

### API 对照

| **功能**  | **Android**                                           | **iOS**                                     | **Ohos**                                              |
| ------- | ----------------------------------------------------- | ------------------------------------------- | ----------------------------------------------------- |
| 新增外部音频流 | `addAudioExternalStream(streamId, config)`            | `addAudioExternalStream:config:`            | `addAudioExternalStream(streamId, config)`            |
| 输入音频数据  | `pushAudioExternalStreamData(streamId, data)`         | `pushAudioExternalStreamData:data:`         | `pushAudioExternalStreamData(streamId, data)`         |
| 设置音量    | `setAudioExternalStreamVolume(streamId, type, vol)`   | `setAudioExternalStreamVolume:type:volume:` | `setAudioExternalStreamVolume(streamId, type, vol)`   |
| 获取音量    | `getAudioExternalStreamVolume(streamId, type)`        | `getAudioExternalStreamVolume:type:`        | `getAudioExternalStreamVolume(streamId, type)`        |
| 清空缓存    | `clearAudioExternalStreamBuffer(streamId, fadeoutMs)` | `clearAudioExternalStreamBuffer:fadeoutMs:` | `clearAudioExternalStreamBuffer(streamId, fadeoutMs)` |
| 移除流     | `removeAudioExternalStream(streamId)`                 | `removeAudioExternalStream:`                | `removeAudioExternalStream(streamId)`                 |

### Push 数据最佳实践

- 需要循环调用 `pushAudioExternalStreamData`，保证数据 push 成功
- 返回错误码 110（缓冲区满）时短暂 Sleep 30ms 后重试，不要丢弃数据
- 引擎退出前先停止推送循环，再调用 `removeAudioExternalStream`
- 实时采集每帧 10ms 长，有数据就调用 push；从文件解析每帧 40ms 长，间隔 30ms 调用 push 一次

## 音频帧数据回调

音频帧回调允许开发者在音频管线的不同位置获取原始 PCM 数据，用于音频分析、自定义处理、录制等场景。

### 支持的数据源位置

| **数据源**         | **枚举值** | **说明**                             |
| --------------- | ------- | ---------------------------------- |
| Captured        | 0       | 采集后的原始音频数据（未经 3A 处理）               |
| ProcessCaptured | 1       | 经过 3A 处理后的音频数据，需要 Connect 成功后才回调数据 |
| Publish         | 2       | 即将推流的音频数据（需要 Connect 成功）           |
| Playback        | 3       | 即将播放的音频数据（远端下行）                    |

### 回调配置参数

| **参数**     | **类型**               | **默认值**  | **说明**          |
| ---------- | -------------------- | -------- | --------------- |
| sampleRate | int                  | 48000    | 回调音频的采样率        |
| channels   | int                  | 1        | 回调音频的声道数，支持 1/2 |
| mode       | AoqAudioObserverMode | ReadOnly | 只读(0)/读写(1) 模式  |

### 使用步骤

1. **注册观察者**：调用 `setAudioFrameObserver` 设置音频帧回调监听器
2. **启用数据源**：调用 `enableAudioFrameObserver` 选择需要监听的数据源位置，开启回调
3. **处理回调数据**：在回调函数中获取 PCM 数据

### API 对照

| **功能** | **Android**                                         | **iOS**                                        | **Ohos**                                            |
| ------ | --------------------------------------------------- | ---------------------------------------------- | --------------------------------------------------- |
| 注册观察者  | `setAudioFrameObserver(listener)`                   | `setAudioFrameObserver:`                       | `setAudioFrameObserver(observer)`                   |
| 启用回调   | `enableAudioFrameObserver(enabled, source, config)` | `enableAudioFrameObserver:audioSource:config:` | `enableAudioFrameObserver(enabled, source, config)` |

### 回调方法

| **回调** | **Android**                             | **iOS**                        | **Ohos**                                |
| ------ | --------------------------------------- | ------------------------------ | --------------------------------------- |
| 采集数据   | `onCapturedAudioFrame(frame)`           | `onCapturedAudioFrame:`        | `onCapturedAudioFrame(frame)`           |
| 3A 后数据 | `onProcessCapturedAudioFrame(frame)`    | `onProcessCapturedAudioFrame:` | `onProcessCapturedAudioFrame(frame)`    |
| 推流数据   | `onPublishAudioFrame(trackType, frame)` | `onPublishAudioFrame:frame:`   | `onPublishAudioFrame(trackType, frame)` |
| 播放数据   | `onPlaybackAudioFrame(frame)`           | `onPlaybackAudioFrame:`        | `onPlaybackAudioFrame(frame)`           |

## 音频状态与路由

SDK 自动监测音频设备的状态变化和路由切换，并通过回调通知应用层。

### 设备状态码

| **状态码**            | **值** | **说明** |
| ------------------ | ----- | ------ |
| AoqAudioDeviceNone | 0     | 初始状态   |
| RecordStarting     | 1     | 采集启动中  |
| RecordStarted      | 2     | 采集已启动  |
| RecordStopping     | 3     | 采集停止中  |
| RecordStopped      | 4     | 采集已停止  |
| RecordFail         | 5     | 采集失败   |
| PlayStarting       | 6     | 播放启动中  |
| PlayStarted        | 7     | 播放已启动  |
| PlayStopping       | 8     | 播放停止中  |
| PlayStopped        | 9     | 播放已停止  |
| PlayFail           | 10    | 播放失败   |

### 设备路由类型

| **路由**        | **值** | **说明**  |
| ------------- | ----- | ------- |
| Default       | 0     | 默认      |
| Headset       | 1     | 有线耳机    |
| Earpiece      | 2     | 听筒      |
| HeadsetNoMic  | 3     | 无麦克风耳机  |
| SpeakerPhone  | 4     | 扬声器     |
| Usb           | 5     | USB 设备  |
| Bluetooth     | 6     | 蓝牙 SCO  |
| BluetoothA2dp | 7     | 蓝牙 A2DP |

### 回调对照

| **回调** | **Android**                            | **iOS**                      | **Ohos**                                         |
| ------ | -------------------------------------- | ---------------------------- | ------------------------------------------------ |
| 设备状态变化 | `onAudioDeviceStateChanged(state)`     | `onAudioDeviceStateChanged:` | `onAudioDeviceStateChanged(state, reason)`       |
| 路由变化   | `onAudioDeviceRouteChanged(routeType)` | `onAudioDeviceRouteChanged:` | `onAudioDeviceRouteChanged(routeType)`           |
| 设备中断   | `onAudioDeviceInterrupted(interrupt)`  | `onAudioDeviceInterrupted:`  | `onAudioDeviceInterrupted(interrupt)`            |
| 文件状态   | `onAudioFileState(state)`              | `onAudioFileState:`          | `onAudioFileState(fileId, stateCode, errorCode)` |

## 音频错误码与警告码

### 音频错误码

| **错误码**                  | **值** | **说明**         |
| ------------------------ | ----- | -------------- |
| AoqErrorCodeAudio        | 100   | 通用音频错误         |
| AudioExternalBufferFull  | 110   | 外部缓冲区已满        |
| AudioDevice              | 120   | 设备通用错误         |
| RecordingAuthFailed      | 121   | 麦克风权限失败        |
| RecordingOccupied        | 122   | 麦克风被占用         |
| RecordingBackgroundStart | 123   | 后台启动录音         |
| RecordingStartFail       | 124   | 录音启动失败         |
| PlayoutOccupied          | 125   | 播放设备被占用        |
| PlayoutBackgroundStart   | 126   | 后台启动播放         |
| PlayoutStartFail         | 127   | 播放启动失败         |
| EarpieceRequiresVoipMode | 128   | 听筒需要启用 VoIP 模式 |

### 音频警告码

| **警告码**               | **值** | **说明**  |
| --------------------- | ----- | ------- |
| AoqWCAudio            | 100   | 通用音频警告  |
| AudioHowling          | 101   | 啸叫检测    |
| AudioDevice           | 120   | 设备通用警告  |
| MicEnumerateError     | 121   | 麦克风枚举错误 |
| MicStartTimeout       | 122   | 麦克风启动超时 |
| RecordingError        | 123   | 录音错误    |
| SpeakerEnumerateError | 124   | 扬声器枚举错误 |
| SpeakerStartTimeout   | 125   | 扬声器启动超时 |
| PlayoutError          | 126   | 播放错误    |

## iOS 专有：AVAudioSession 控制

iOS 平台提供了 `setAudioSessionRestriction` 接口，可精细控制 SDK 对系统 AVAudioSession 的管理权限。

| **控制项**           | **说明**                |
| ----------------- | --------------------- |
| SetCategory       | SDK 是否有权设置 Session 类别 |
| ConfigureSession  | SDK 是否有权配置 Session 参数 |
| DeactivateSession | SDK 是否有权停用 Session    |
| ActivateSession   | SDK 是否有权激活 Session    |

通过按位组合传入 restriction 值，可限制 SDK 对 AVAudioSession 的控制范围，避免与应用层其他音频组件冲突。
