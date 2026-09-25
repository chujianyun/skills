> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 自定义视频输入

> 使用外部视频源代替设备摄像头

介绍 AOQ Client SDK 自定义视频输入的两种模式：原始帧模式和编码帧模式，以及各模式的配置方法和示例代码。

## 功能介绍

AOQ Client SDK 内部视频模块可满足应用中对基本视频功能的需求，但在特定场景中，SDK 内部的视频采集模块可能无法满足开发需求，需要实现自定义视频采集功能，例如：

- 解决摄像头设备被占用或不兼容问题。
- 需要从定制的采集系统、视频文件中获取视频数据后交给 SDK 传输。
- 需要将 AI 生成的画面、屏幕录制、虚拟摄像头等内容通过 SDK 推流传输。

AOQ Client SDK 支持两种自定义视频采集模式：

- **原始帧模式**：自行采集原始视频帧（BGRA、I420、NV12、NV21 等格式），通过 `pushExternalVideoCapturedFrame` 推送给 SDK 进行编码和传输。SDK 内部完成编码、传输等完整流程。
- **编码帧模式**：自行完成视频编码（目前支持 JPEG），通过 `pushExternalVideoEncodedFrame` 直推已编码数据给 SDK，跳过 SDK 内部编码器，直接打包发送。

## 示例代码

暂无

## 前提条件

- 已创建引擎实例（调用 `createEngine`）。
- 已成功连接服务器（`onConnectionStatusChange` 回调状态为 `AoqConnectionStatusConnected`）。

## 功能实现

根据业务场景选择以下两种模式之一。两种模式不可混用：同一时间只能使用其中一种推送接口。

## 模式一：原始帧模式

自行采集原始视频帧（BGRA、I420、NV12、NV21 等格式），推送给 SDK 进行编码和传输。SDK 内部完成编码、传输等完整流程。

### 1. 配置视频编码参数

SDK 内部编码器会对推送的原始帧进行编码，可根据业务需要调整编码参数。

```java
AoqClientEngine.AoqVideoCodecConfig config = new AoqClientEngine.AoqVideoCodecConfig();
config.width            = 1280;
config.height           = 720;
config.fps              = 2;
config.bitrate          = 500000;   // 起始码率 500kbps
config.minBitrate       = 128000;   // 最小码率 128kbps
config.keyframeInterval = 2;
// isExternal 保持默认 false，SDK 内部编码
engine.setVideoEncoderConfig(config);
```

**参数说明：**

| 参数               | 类型                 | 默认值                     | 说明            |
| ---------------- | ------------------ | ----------------------- | ------------- |
| trackType        | AoqTrackType       | AoqTrackTypeVideo       | 视频轨道类型        |
| codecType        | AoqEncoderType     | AoqEncoderTypeVideoH264 | 编码器类型         |
| width            | int                | 720                     | 编码宽度（像素）      |
| height           | int                | 1280                    | 编码高度（像素）      |
| fps              | int                | 5                       | 帧率            |
| bitrate          | int                | 500000                  | 起始码率（bps）     |
| minBitrate       | int                | 128000                  | 最小码率（bps）     |
| keyframeInterval | int                | 2                       | 关键帧间隔（秒）      |
| isExternal       | boolean            | false                   | 原始帧模式保持 false |
| mirrorMode       | AoqMirrorMode      | AoqMirrorModeDisabled   | 镜像模式          |
| orientationMode  | AoqOrientationMode | AoqOrientationModeAuto  | 画面方向模式        |

### 2. 以外部采集模式启动视频采集

调用 `startVideoCapture` 并设置 `isExternal=true`，告知 SDK 不打开摄像头，由外部源提供视频帧。这是原始帧模式的前置条件，未调用则 SDK 不会消费推送的帧数据。

```java
AoqClientEngine.AoqVideoCaptureConfig config = new AoqClientEngine.AoqVideoCaptureConfig();
config.isExternal = true;  // 不打开摄像头，由外部源推送视频帧
// isExternal=true 时 width/height/fps 无效，实际分辨率和帧率由推送数据决定
int ret = engine.startVideoCapture(config);
```

**参数说明：**

| 参数              | 类型                 | 默认值                     | 说明                           |
| --------------- | ------------------ | ----------------------- | ---------------------------- |
| width           | int                | 1280                    | 采集宽度（`isExternal=true` 时无效）  |
| height          | int                | 720                     | 采集高度（`isExternal=true` 时无效）  |
| fps             | int                | 15                      | 采集帧率（`isExternal=true` 时无效）  |
| isExternal      | boolean            | false                   | true：不打开摄像头，由外部源推送帧数据        |
| cameraDirection | AoqCameraDirection | AoqCameraDirectionFront | 摄像头方向（`isExternal=true` 时无效） |

### 3. 推送原始视频帧

调用 `pushExternalVideoCapturedFrame` 接口，将采集到的原始视频帧传入 SDK。SDK 内部完成编码和传输。

支持的视频帧格式：BGRA、I420、NV12、NV21、RGBA。Apple 平台额外支持 CVPixelBuffer 零拷贝格式。

#### 3.1 BGRA 格式

BGRA 为打包格式，每个像素 4 字节（Blue、Green、Red、Alpha），一帧数据量 = width x height x 4。

```java
// 构造 BGRA 视频帧
AoqClientEngine.AoqVideoFrame frame = new AoqClientEngine.AoqVideoFrame();
frame.format    = AoqClientEngine.AoqVideoPixelFormat.AoqVideoPixelFormatBGRA;
frame.width     = 1280;
frame.height    = 720;
frame.data      = bgraBytes; // byte[]，长度 = width * height * 4
frame.timeStamp = System.currentTimeMillis();
int ret = engine.pushExternalVideoCapturedFrame(
    AoqClientEngine.AoqTrackType.AoqTrackTypeVideo, frame);
```

#### 3.2 I420 格式

I420 为三平面格式（Y、U、V 分离），Y 平面大小 = width x height，U/V 平面各为 (width/2) x (height/2)。

```java
// 构造 I420 视频帧
AoqClientEngine.AoqVideoFrame frame = new AoqClientEngine.AoqVideoFrame();
frame.format    = AoqClientEngine.AoqVideoPixelFormat.AoqVideoPixelFormatI420;
frame.width     = 1280;
frame.height    = 720;
frame.dataY     = yPlane;  // byte[]，长度 = width * height
frame.dataU     = uPlane;  // byte[]，长度 = (width/2) * (height/2)
frame.dataV     = vPlane;  // byte[]，长度 = (width/2) * (height/2)
frame.strideY   = 1280;    // Y 平面行字节数
frame.strideU   = 640;     // U 平面行字节数
frame.strideV   = 640;     // V 平面行字节数
frame.timeStamp = System.currentTimeMillis();
int ret = engine.pushExternalVideoCapturedFrame(
    AoqClientEngine.AoqTrackType.AoqTrackTypeVideo, frame);
```

#### 3.3 NV12 / NV21 格式

NV12 和 NV21 为半平面格式，Y 平面 + UV 交错平面。NV12 为 UV 交替排列，NV21 为 VU 交替排列。数据量 = width x height x 3 / 2，打包在 `data` 字段中。

```java
// 构造 NV12 视频帧（NV21 同理，修改 format 即可）
AoqClientEngine.AoqVideoFrame frame = new AoqClientEngine.AoqVideoFrame();
frame.format    = AoqClientEngine.AoqVideoPixelFormat.AoqVideoPixelFormatNV12;
frame.width     = 1280;
frame.height    = 720;
frame.data      = nv12Bytes; // byte[]，长度 = width * height * 3 / 2
frame.timeStamp = System.currentTimeMillis();
int ret = engine.pushExternalVideoCapturedFrame(
    AoqClientEngine.AoqTrackType.AoqTrackTypeVideo, frame);
```

#### 3.4 CVPixelBuffer 格式（Apple 平台）

iOS / macOS 平台支持直接传递 `CVPixelBufferRef`，实现零拷贝传输，避免内存拷贝带来的性能开销。

```swift
// iOS / macOS 平台
let frame = AoqVideoFrame()
frame.format      = .cvPixelBuffer
frame.width       = 1280
frame.height      = 720
frame.pixelBuffer = pixelBuffer  // CVPixelBufferRef
frame.timeStamp   = Int64(Date().timeIntervalSince1970 * 1000)
// SDK 内部异步持有 pixelBuffer，需要额外 +1 引用计数
// SDK 消费完毕后会自行释放
let _ = Unmanaged.passRetained(pixelBuffer)
engine.pushExternalVideoCapturedFrame(.video, frame: frame)
```

### 4. 停止原始帧采集

当不再需要推送视频帧时，先停止推帧定时器，再调用 `stopVideoCapture` 关闭视频采集。

```java
// 1. 停止推帧定时器
stopExternalFramePush();
// 2. 停止视频采集
engine.stopVideoCapture();
```

## 模式二：编码帧模式

自行完成视频编码（目前支持 JPEG），直推已编码数据给 SDK，跳过 SDK 内部编码器，直接打包发送。此模式**不需要调用** `startVideoCapture` 等采集相关接口。

### 1. 配置视频编码参数并启用外部编码

调用 `setVideoEncoderConfig` 并设置 `isExternal=true`，告知 SDK 跳过内部编码器，由外部提供已编码数据。

```java
AoqClientEngine.AoqVideoCodecConfig config = new AoqClientEngine.AoqVideoCodecConfig();
config.width      = 1280;
config.height     = 720;
config.fps        = 2;
config.isExternal = true;  // 跳过内部编码，由外部推送已编码帧
engine.setVideoEncoderConfig(config);
```

设置完成后即可直接推送编码帧，无需调用 `startVideoCapture`。

### 2. 推送编码视频帧

调用 `pushExternalVideoEncodedFrame` 接口，将已编码的视频数据直传给 SDK。目前仅支持 JPEG 编码格式。

```java
// 从 Bitmap 生成 JPEG 数据
android.graphics.Bitmap bmp = android.graphics.Bitmap.createBitmap(
    width, height, android.graphics.Bitmap.Config.ARGB_8888);
// ... 填充 Bitmap 内容 ...
java.io.ByteArrayOutputStream baos = new java.io.ByteArrayOutputStream();
bmp.compress(android.graphics.Bitmap.CompressFormat.JPEG, 85, baos);
bmp.recycle();
// 构造编码帧并推送
AoqClientEngine.AoqVideoEncodedFrame frame = new AoqClientEngine.AoqVideoEncodedFrame();
frame.codec     = AoqClientEngine.AoqVideoCodecType.AoqVideoCodecTypeJPEG;
frame.data      = baos.toByteArray();
frame.width     = width;
frame.height    = height;
frame.timeStamp = System.currentTimeMillis();
int ret = engine.pushExternalVideoEncodedFrame(
    AoqClientEngine.AoqTrackType.AoqTrackTypeVideo, frame);
```

**AoqVideoEncodedFrame 参数说明：**

| 参数        | 类型                | 默认值                   | 说明                         |
| --------- | ----------------- | --------------------- | -------------------------- |
| codec     | AoqVideoCodecType | AoqVideoCodecTypeJPEG | 编码格式，目前仅支持 JPEG            |
| data      | byte\[]           | null                  | 编码后的数据                     |
| width     | int               | 0                     | 画面宽度（像素）                   |
| height    | int               | 0                     | 画面高度（像素）                   |
| timeStamp | long              | 0                     | 时间戳（毫秒），为 0 时 SDK 使用本地时钟补充 |

### 3. 停止编码帧推送

编码帧模式无需管理采集设备，停止推帧定时器即可。

```java
stopExternalFramePush();
```

## 视频帧格式参考

### AoqVideoFrame（原始帧模式使用）

| 字段              | 类型                  | 说明                                   |
| --------------- | ------------------- | ------------------------------------ |
| format          | AoqVideoPixelFormat | 像素格式                                 |
| width           | int                 | 画面宽度（像素）                             |
| height          | int                 | 画面高度（像素）                             |
| data            | byte\[]             | 打包格式数据（NV12/NV21/BGRA/RGBA）          |
| dataY           | byte\[]             | I420 Y 平面数据                          |
| dataU           | byte\[]             | I420 U 平面数据                          |
| dataV           | byte\[]             | I420 V 平面数据                          |
| strideY         | int                 | I420 Y 平面行字节数                        |
| strideU         | int                 | I420 U 平面行字节数                        |
| strideV         | int                 | I420 V 平面行字节数                        |
| textureId       | int                 | Android 纹理 ID（TextureOES/Texture2D）  |
| transformMatrix | float\[]            | 纹理变换矩阵（4x4 行优先）                      |
| eglContext      | EGLContext          | Android 共享 EGL context（纹理模式使用）       |
| pixelBuffer     | CVPixelBufferRef    | Apple 零拷贝 CVPixelBuffer（仅 iOS/macOS） |
| timeStamp       | long                | 时间戳（毫秒），为 0 时 SDK 用本地时钟补充            |

### AoqVideoPixelFormat 枚举值

| 枚举值                              | 数值 | 说明                               |
| -------------------------------- | -- | -------------------------------- |
| AoqVideoPixelFormatUnknown       | 0  | 未知格式                             |
| AoqVideoPixelFormatI420          | 1  | I420 三平面格式                       |
| AoqVideoPixelFormatNV12          | 2  | NV12 半平面格式（UV 交替）                |
| AoqVideoPixelFormatNV21          | 3  | NV21 半平面格式（VU 交替）                |
| AoqVideoPixelFormatBGRA          | 4  | BGRA 打包格式                        |
| AoqVideoPixelFormatRGBA          | 5  | RGBA 打包格式                        |
| AoqVideoPixelFormatCVPixelBuffer | 6  | Apple CVPixelBuffer（仅 iOS/macOS） |
| AoqVideoPixelFormatTextureOES    | 7  | Android OES 外部纹理                 |
| AoqVideoPixelFormatTexture2D     | 8  | Android 2D 纹理                    |

### AoqVideoEncodedFrame（编码帧模式使用）

| 字段        | 类型                | 说明                        |
| --------- | ----------------- | ------------------------- |
| codec     | AoqVideoCodecType | 编码格式                      |
| data      | byte\[]           | 编码后的数据                    |
| width     | int               | 画面宽度（像素）                  |
| height    | int               | 画面高度（像素）                  |
| timeStamp | long              | 时间戳（毫秒），为 0 时 SDK 用本地时钟补充 |

### AoqVideoCodecType 枚举值

| 枚举值                   | 数值 | 说明        |
| --------------------- | -- | --------- |
| AoqVideoCodecTypeJPEG | 0  | JPEG 编码格式 |

## 注意事项

- 原始帧模式：必须先调用 `startVideoCapture(isExternal=true)` 再推送帧，否则 SDK 返回参数错误。
- 编码帧模式：只需调用 `setVideoEncoderConfig(isExternal=true)` 即可推送，**不需要**调用 `startVideoCapture`。
- 原始帧模式与编码帧模式不可混用：同一时间只能使用其中一种推送接口。
- 编码帧模式目前仅支持 JPEG 格式。
- 视频帧数据在推送后由 SDK 内部管理生命周期，调用方无需在推送后继续持有数据引用。
