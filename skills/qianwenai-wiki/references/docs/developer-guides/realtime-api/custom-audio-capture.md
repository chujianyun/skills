> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 自定义音频采集

> 使用外部音频源代替设备麦克风

介绍如何使用 AOQ Client SDK 实现自定义音频采集功能，包括外部音频流的添加、PCM 数据推送和管理。

## 功能介绍

AOQ Client SDK 内部音频模块可满足应用中对基本音频功能的需求，但在特定场景中，SDK 内部的音频采集模块可能无法满足开发需求，需要实现自定义音频采集功能，例如：

- 解决音频采集设备被占用问题。
- 需要从定制的采集系统、音频文件中获取音频数据后交给 SDK 传输。
- 需要将 AI TTS 生成的音频数据通过 SDK 推流传输。

AOQ Client SDK 支持灵活的自定义采集功能，允许用户根据业务场景自行管理音频设备与音频源。外部音频流的数据会与内部采集的音频数据混音后一起推流发送。

## 示例代码

暂无

## 前提条件

- 已创建引擎实例（调用 `createEngine`）。
- 已成功连接服务器（`onConnectionStatusChange` 回调状态为 `AoqConnectionStatusConnected`）。

## 功能实现

### 1. 打开或关闭音频采集

需要先开启音频采集，外部音频流输入的数据会与内部采集数据混音后一起推流。如果不需要内部麦克风采集，可以设置 `isExternal=true` 关闭内部采集设备。

```java
// 方式一：开启内部采集，外部音频流数据会与麦克风数据混音推流
AoqClientEngine.AoqAudioCaptureConfig config = new AoqClientEngine.AoqAudioCaptureConfig();
config.isExternal = false; // 使用内部麦克风采集
config.isVoipMode = false;
engine.startAudioCapture(config);
// 方式二：关闭内部采集，仅推送外部音频流数据
AoqClientEngine.AoqAudioCaptureConfig config = new AoqClientEngine.AoqAudioCaptureConfig();
config.isExternal = true; // 不打开麦克风，由外部音频流提供数据
engine.startAudioCapture(config);
```

### 2. 连接成功后，添加外部音频流

在 `onConnectionStatusChange` 回调状态变为 `AoqConnectionStatusConnected` 后，调用 `addAudioExternalStream` 添加外部音频流。需要指定一个唯一的 `streamId` 用于后续推送数据和管理。

如果需要音频 3A 处理（回声消除、噪声抑制、自动增益），请配置 `AoqAudioExternalStreamConfig` 中的 `enable3A` 参数。

```java
// 在 onConnectionStatusChange 回调中确认连接成功后添加
@Override
public void onConnectionStatusChange(AoqClientEngine.AoqConnectionStatus status) {
  if (status == AoqClientEngine.AoqConnectionStatus.AoqConnectionStatusConnected) {
    addExternalAudioStream();
  }
}
private void addExternalAudioStream() {
  AoqClientEngine.AoqAudioExternalStreamConfig config = new AoqClientEngine.AoqAudioExternalStreamConfig();
  config.sampleRate = 48000;       // 采样率，需与实际音频数据一致
  config.channels = 1;             // 声道数
  config.publishVolume = 100;      // 推流音量 [0-100]
  config.playoutVolume = 0;        // 本地播放音量 [0-100]，0 表示不本地播放
  config.maxBufferDuration = 1000; // 最大缓冲时长（毫秒）
  config.enable3A = true;          // 是否对输入 PCM 进行 3A 处理
  String streamId = "external_audio_1";
  int ret = engine.addAudioExternalStream(streamId, config);
  if (ret == 0) {
    mExternalStreamId = streamId;
  }
}
```

**参数说明：**

| 参数                | 类型             | 默认值                    | 说明                 |
| ----------------- | -------------- | ---------------------- | ------------------ |
| trackType         | AoqTrackType   | AoqTrackTypeAudio      | 音频轨道类型             |
| codecType         | AoqEncoderType | AoqEncoderTypeAudioPCM | 音频流格式              |
| channels          | int            | 1                      | 声道数                |
| sampleRate        | int            | 48000                  | 采样率（Hz）            |
| playoutVolume     | int            | 100                    | 播放音量 \[0-100]      |
| publishVolume     | int            | 100                    | 推流音量 \[0-100]      |
| maxBufferDuration | int            | 1000                   | 最大缓冲时长（毫秒）         |
| enable3A          | boolean        | false                  | 是否对输入 PCM 进行 3A 处理 |

### 3. 实现自采集模块或从文件获取 PCM 数据

自定义采集功能需要根据业务场景自行采集并处理音频数据，之后将数据传入 SDK 进行传输。常见的数据来源：

- **麦克风采集**：通过 Android AudioRecord 采集 PCM 数据。
- **文件读取**：从本地 PCM/WAV 音频文件中解析获取 PCM 数据。
- **AI TTS**：从语音合成引擎获取 PCM 数据。
- **网络流**：从网络音频流中解码获取 PCM 数据。

音频数据需要为 PCM 格式，并记录对应的采样率、声道数等参数，用于构造 `AoqAudioFrameData` 对象。

### 4. 通过外部音频流 ID 推送音频数据到 SDK

调用 `pushAudioExternalStreamData` 接口，将采集到的 PCM 音频数据传入 SDK。

- 从硬件采集：建议采集 10ms 为一帧数据，采集到数据就 push 给 SDK。
- 从文件解析：建议 40ms 为一帧数据，每 push 一帧 Sleep 30ms 后 push 下一帧。
- 需要维护一个 `running` 标记，当引擎退出或 stream ID 被删除时退出推送循环。

```java
// 成员变量：控制推送循环的运行标记
private volatile boolean mPushRunning = false;
// 推送单帧音频数据
private void pushAudioData(byte[] audioData, int bytesRead) {
  if (engine == null || mExternalStreamId == null || bytesRead <= 0) {
    return;
  }
  int channels = 1;
  int bytesPerSample = 2; // 16bit PCM
  int sampleRate = 48000;
  // 构造音频帧数据
  AoqClientEngine.AoqAudioFrameData frameData = new AoqClientEngine.AoqAudioFrameData();
  frameData.dataPtr = audioData;
  frameData.dataSize = bytesRead;
  frameData.numOfSamples = bytesRead / (channels * bytesPerSample);
  frameData.bytesPerSample = bytesPerSample;
  frameData.numOfChannels = channels;
  frameData.samplesPerSec = sampleRate;
  // 推送数据，处理缓冲区满的情况
  int ret;
  final int WAIT_MS = 30;
  do {
    // 检查运行标记和 stream ID 是否仍有效
    if (!mPushRunning || mExternalStreamId == null) {
      break;
    }
    ret = engine.pushAudioExternalStreamData(mExternalStreamId, frameData);
    if (ret == 110) { // AoqErrorCodeAudioExternalBufferFull
      try {
        Thread.sleep(WAIT_MS);
      } catch (InterruptedException e) {
        break;
      }
    } else {
      break;
    }
  } while (true);
}
```

**注意事项：**

- 需要在连接成功且添加外部音频流之后再开始推送数据。
- 需要按照数据的实际长度设置 `AoqAudioFrameData` 的 `numOfSamples`。
- 调用 `pushAudioExternalStreamData` 时，可能出现内部缓冲区满（错误码 110）而导致失败，需要等待重试。
- 实时采集建议 10ms 一帧数据 push，有数据就调用 push，注意处理内部缓冲区满（错误码 110）。
- 从文件解析建议 40ms 一帧数据，间隔 30ms 调用 push，注意处理内部缓冲区满（错误码 110）。
- 引擎退出（`destroy`）或 stream ID 被移除前，必须先设置 `mPushRunning = false` 停止推送循环，避免在已释放的资源上操作。

### 5. 移除外部音频流

当不再需要发布自定义采集的音频时，先停止推送循环，再调用 `removeAudioExternalStream` 接口移除外部音频流。

```java
// 先停止推送
stopPushAudio();
// 再移除外部音频流
engine.removeAudioExternalStream(mExternalStreamId);
mExternalStreamId = null;
```
