> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 视频常用功能介绍

> AOQ SDK 视频采集、预览、编码配置

AOQ Client SDK 提供了完整的视频能力，覆盖视频采集、渲染显示、编码配置、帧数据回调、外部视频输入等核心场景。本文档基于 Android（Java）、iOS（Objective-C）、Ohos（ArkTS）三个平台的公开 API，对视频常用功能进行统一介绍。

## 1. 视频采集

### 1.1 功能说明

视频采集用于打开设备摄像头，将实时视频帧数据送入 SDK 编码推流管线。SDK 支持两种采集模式：

- **内部采集（默认）**：SDK 自动管理摄像头设备的打开、帧采集和关闭，支持前后置摄像头切换。
- **外部采集**：由应用自行管理摄像头或其他视频源，采集到的帧数据通过 `pushExternalVideoCapturedFrame` 接口输入 SDK。

### 1.2 采集配置参数

| **参数**          | **类型**             | **默认值**  | **说明**            |
| --------------- | ------------------ | -------- | ----------------- |
| width           | int                | 1280     | 采集宽度（像素），外部采集时无效  |
| height          | int                | 720      | 采集高度（像素），外部采集时无效  |
| fps             | int                | 15       | 采集帧率，外部采集时由送帧节奏决定 |
| isExternal      | bool               | false    | 是否使用外部采集模式        |
| cameraDirection | AoqCameraDirection | Front(0) | 摄像头方向，外部采集时无效     |

### 1.3 摄像头方向枚举

| **枚举值**                 | **数值** | **说明** |
| ----------------------- | ------ | ------ |
| AoqCameraDirectionFront | 0      | 前置摄像头  |
| AoqCameraDirectionBack  | 1      | 后置摄像头  |

### 1.4 API 对照

| **功能** | **Android**               | **iOS**                   | **Ohos**                  |
| ------ | ------------------------- | ------------------------- | ------------------------- |
| 开启采集   | startVideoCapture(config) | startVideoCapture:config: | startVideoCapture(config) |
| 关闭采集   | stopVideoCapture()        | stopVideoCapture          | stopVideoCapture()        |
| 切换摄像头  | switchCamera(direction)   | switchCamera:             | switchCamera(direction)   |

### 1.5 使用示例

<Tabs>
  <Tab title="Android">
    ```java
    AoqVideoCaptureConfig config = new AoqVideoCaptureConfig();
    config.width = 1280;
    config.height = 720;
    config.fps = 15;
    config.cameraDirection = AoqCameraDirection.AoqCameraDirectionFront;
    engine.startVideoCapture(config);
    ```
  </Tab>

  <Tab title="iOS">
    ```objectivec
    AoqVideoCaptureConfig *config = [[AoqVideoCaptureConfig alloc] init];
    config.width = 1280;
    config.height = 720;
    config.fps = 15;
    config.cameraDirection = AoqCameraDirectionFront;
    [engine startVideoCapture:config];
    ```
  </Tab>

  <Tab title="Ohos">
    ```javascript
    let config: AoqVideoCaptureConfig = {
      width: 1280,
      height: 720,
      fps: 15,
      cameraDirection: AoqCameraDirection.AoqCameraDirectionFront
    };
    engine.startVideoCapture(config);
    ```
  </Tab>
</Tabs>

## 2. 视频渲染

### 2.1 功能说明

视频渲染用于将本地采集或远端接收的视频帧数据显示到屏幕上。SDK 支持设置本地预览窗口和远端渲染窗口，通过 `trackType` 区分视频流（Video）和屏幕共享流（Screen）。

### 2.2 渲染模式

| **枚举值**              | **数值** | **说明**        |
| -------------------- | ------ | ------------- |
| AoqRenderModeAuto    | 0      | 自动模式          |
| AoqRenderModeStretch | 1      | 拉伸平铺，画面可能变形   |
| AoqRenderModeFill    | 2      | 填充黑边，画面完整显示   |
| AoqRenderModeCrop    | 3      | 裁剪模式，画面内容可能丢失 |

### 2.3 画布配置

| **参数**     | **类型**        | **默认值** | **说明**                                                                |
| ---------- | ------------- | ------- | --------------------------------------------------------------------- |
| view       | 平台视图          | null    | 渲染视图（Android: SurfaceView/TextureView, iOS: UIView, Ohos: XComponent） |
| renderMode | AoqRenderMode | Auto(0) | 渲染显示模式                                                                |

### 2.4 API 对照

| **功能** | **Android**                      | **iOS**                         | **Ohos**                         |
| ------ | -------------------------------- | ------------------------------- | -------------------------------- |
| 设置本地预览 | setLocalView(trackType, canvas)  | setLocalView:trackType:canvas:  | setLocalView(trackType, canvas)  |
| 设置远端渲染 | setRemoteView(trackType, canvas) | setRemoteView:trackType:canvas: | setRemoteView(trackType, canvas) |

<Note>
  **平台差异**：Android 使用 SurfaceView 或 TextureView 作为渲染容器；iOS 使用 UIView（内部通过 AoqRenderView 封装，支持 Metal 加速）；Ohos 使用 XComponent（通过 AoqXComponentController 管理 native 渲染视图）。
</Note>

## 3. 视频编码配置

### 3.1 功能说明

设置视频编码参数，包括编码格式、分辨率、帧率、码率、关键帧间隔、镜像和方向等。通过 `trackType` 区分视频轨道和屏幕共享轨道的编码配置。

### 3.2 编码配置参数

| **参数**           | **类型**             | **默认值**      | **说明**                  |
| ---------------- | ------------------ | ------------ | ----------------------- |
| trackType        | AoqTrackType       | Video(1)     | 轨道类型：Video              |
| codecType        | AoqEncoderType     | VideoH264(3) | 编码格式                    |
| width            | int                | 720          | 编码宽度                    |
| height           | int                | 1280         | 编码高度                    |
| fps              | int                | 5            | 编码帧率                    |
| bitrate          | int                | 500000       | 目标码率（bps）               |
| minBitrate       | int                | 128000       | 最小码率（bps）               |
| keyframeInterval | int                | 2            | 关键帧间隔（秒）                |
| mirrorMode       | AoqMirrorMode      | Disabled(0)  | 镜像模式                    |
| orientationMode  | AoqOrientationMode | Auto(0)      | 方向模式                    |
| isExternal       | bool               | false        | 外部编码模式（true 时由应用推送已编码帧） |

### 3.3 编码格式枚举

| **枚举值**                 | **数值** | **说明**           |
| ----------------------- | ------ | ---------------- |
| AoqEncoderTypeVideoH264 | 3      | H.264 编码         |
| AoqEncoderTypeVideoJpeg | 4      | JPEG 编码（用于外部编码帧） |

### 3.4 镜像模式

| **枚举值**               | **数值** | **说明** |
| --------------------- | ------ | ------ |
| AoqMirrorModeDisabled | 0      | 禁用镜像   |
| AoqMirrorModeEnabled  | 1      | 启用镜像   |

### 3.5 方向模式

| **枚举值**                     | **数值** | **说明** |
| --------------------------- | ------ | ------ |
| AoqOrientationModeAuto      | 0      | 自动方向   |
| AoqOrientationModePortrait  | 1      | 竖屏方向   |
| AoqOrientationModeLandscape | 2      | 横屏方向   |

### 3.6 API 对照

| **功能** | **Android**                   | **iOS**                | **Ohos**                      |
| ------ | ----------------------------- | ---------------------- | ----------------------------- |
| 设置编码参数 | setVideoEncoderConfig(config) | setVideoEncoderConfig: | setVideoEncoderConfig(config) |

## 4. 外部视频帧输入

### 4.1 功能说明

外部视频帧输入允许应用将自定义的视频帧数据推送到 SDK，用于外部采集或外部编码场景。支持两种推送方式：

- **推送原始帧**：将未编码的像素数据（I420/NV12/NV21/BGRA/RGBA 等格式）推送给 SDK，由 SDK 进行编码。
- **推送已编码帧**：将已编码的数据（如 JPEG）直推给 SDK，SDK 不做二次编码，直接打包发送。

通过 `trackType` 路由，`AoqTrackTypeVideo` 对应视频采集的外部帧，`AoqTrackTypeScreen` 对应屏幕共享的外部帧。

### 4.2 像素格式枚举

| **枚举值**                          | **数值** | **说明**    | **平台支持**  |
| -------------------------------- | ------ | --------- | --------- |
| AoqVideoPixelFormatI420          | 1      | I420 三平面  | 全平台       |
| AoqVideoPixelFormatNV12          | 2      | NV12 双平面  | 全平台       |
| AoqVideoPixelFormatNV21          | 3      | NV21 双平面  | 全平台       |
| AoqVideoPixelFormatBGRA          | 4      | BGRA 打包   | 全平台       |
| AoqVideoPixelFormatRGBA          | 5      | RGBA 打包   | 全平台       |
| AoqVideoPixelFormatCVPixelBuffer | 6      | Apple 零拷贝 | 仅 iOS     |
| AoqVideoPixelFormatTextureOES    | 7      | OES 纹理    | 仅 Android |
| AoqVideoPixelFormatTexture2D     | 8      | 2D 纹理     | 仅 Android |

### 4.3 原始视频帧数据结构 (AoqVideoFrame)

| **字段**                      | **类型**                | **说明**                                  |
| --------------------------- | --------------------- | --------------------------------------- |
| format                      | AoqVideoPixelFormat   | 像素格式                                    |
| width                       | int                   | 宽度（像素）                                  |
| height                      | int                   | 高度（像素）                                  |
| data                        | byte\[] / ArrayBuffer | 打包格式数据（NV12/NV21/BGRA/RGBA）             |
| dataY / dataU / dataV       | byte\[] / ArrayBuffer | I420 三平面数据                              |
| strideY / strideU / strideV | int                   | I420 三平面步长                              |
| textureId                   | int                   | 纹理 ID（Android TextureOES/Texture2D 时有效） |
| transformMatrix             | float\[16]            | 4x4 纹理变换矩阵（Android）                     |
| eglContext                  | EGLContext            | 共享 EGL 上下文（Android）                     |
| pixelBuffer                 | CVPixelBufferRef      | Apple 零拷贝（iOS）                          |
| timeStamp                   | long                  | 时间戳（ms），0 时 SDK 用本地时钟补                  |

### 4.4 已编码视频帧数据结构 (AoqVideoEncodedFrame)

| **字段**    | **类型**                | **默认值** | **说明**  |
| --------- | --------------------- | ------- | ------- |
| codec     | AoqVideoCodecType     | JPEG(0) | 编码格式    |
| data      | byte\[] / ArrayBuffer | -       | 编码后数据   |
| width     | int                   | -       | 宽度（像素）  |
| height    | int                   | -       | 高度（像素）  |
| timeStamp | long                  | 0       | 时间戳（ms） |

### 4.5 API 对照

| **功能** | **Android**                                      | **iOS**                               | **Ohos**                                         |
| ------ | ------------------------------------------------ | ------------------------------------- | ------------------------------------------------ |
| 推送原始帧  | pushExternalVideoCapturedFrame(trackType, frame) | pushExternalVideoCapturedFrame:frame: | pushExternalVideoCapturedFrame(trackType, frame) |
| 推送已编码帧 | pushExternalVideoEncodedFrame(trackType, frame)  | pushExternalVideoEncodedFrame:frame:  | pushExternalVideoEncodedFrame(trackType, frame)  |

## 5. 视频帧数据回调

### 5.1 功能说明

视频帧回调允许开发者在视频管线的不同位置获取原始帧数据，用于视频分析、自定义处理、录制等场景。支持只读和读写两种模式，读写模式下可修改帧数据并写回 SDK。

### 5.2 支持的数据源位置

| **数据源**   | **枚举值** | **说明**         |
| --------- | ------- | -------------- |
| Captured  | 0       | 采集后的视频数据（前处理前） |
| PreEncode | 1       | 编码前的视频数据（前处理后） |
| Remote    | 2       | 远端解码后、渲染前的视频数据 |

### 5.3 回调配置参数

| **参数**        | **类型**                    | **默认值**     | **说明**         |
| ------------- | ------------------------- | ----------- | -------------- |
| format        | AoqVideoPixelFormat       | I420(1)     | 期望回调的像素格式      |
| alignment     | AoqVideoObserverAlignment | Default(0)  | 宽度对齐策略         |
| mode          | AoqVideoObserverMode      | ReadOnly(0) | 只读(0)/读写(1) 模式 |
| mirrorApplied | bool                      | false       | 是否对回调数据应用镜像    |

### 5.4 宽度对齐枚举

| **枚举值**                          | **数值** | **说明**  |
| -------------------------------- | ------ | ------- |
| AoqVideoObserverAlignmentDefault | 0      | 默认对齐    |
| AoqVideoObserverAlignmentEven    | 1      | 2 字节对齐  |
| AoqVideoObserverAlignment4       | 2      | 4 字节对齐  |
| AoqVideoObserverAlignment8       | 3      | 8 字节对齐  |
| AoqVideoObserverAlignment16      | 4      | 16 字节对齐 |

### 5.5 使用步骤

1. **注册观察者**：调用 `setVideoFrameObserver` 设置视频帧回调监听器
2. **启用数据源**：调用 `enableVideoFrameObserver` 选择需要监听的数据源位置，开启回调
3. **处理回调数据**：在回调函数中获取帧数据（仅回调期间有效，异步使用需自行拷贝）

### 5.6 API 对照

| **功能** | **Android**                                       | **iOS**                                      | **Ohos**                                          |
| ------ | ------------------------------------------------- | -------------------------------------------- | ------------------------------------------------- |
| 注册观察者  | setVideoFrameObserver(listener)                   | setVideoFrameObserver:                       | setVideoFrameObserver(observer)                   |
| 启用回调   | enableVideoFrameObserver(enabled, source, config) | enableVideoFrameObserver:videoSource:config: | enableVideoFrameObserver(enabled, source, config) |

### 5.7 回调方法

| **回调** | **Android**                             | **iOS**                      | **Ohos**                                |
| ------ | --------------------------------------- | ---------------------------- | --------------------------------------- |
| 采集后数据  | onCapturedVideoFrame(frame)             | onCapturedVideoFrame:        | onCapturedVideoFrame(frame)             |
| 编码前数据  | onPreEncodeVideoFrame(trackType, frame) | onPreEncodeVideoFrame:frame: | onPreEncodeVideoFrame(trackType, frame) |
| 远端数据   | onRemoteVideoFrame(trackType, frame)    | onRemoteVideoFrame:frame:    | onRemoteVideoFrame(trackType, frame)    |

<Note>
  回调方法返回 `true`/`YES` 表示数据已修改、需写回 SDK（仅 ReadWrite 模式且 I420 格式时生效）。
</Note>

## 7. 媒体流发送控制

### 7.1 功能说明

控制本地媒体流的发送开关，通过 `trackType` 路由到不同轨道（Audio/Video/Screen）。停用发送后，采集和编码继续运行，但数据不会发送到远端。

### 7.2 API 对照

| **功能** | **Android**                              | **iOS**                       | **Ohos**                                 |
| ------ | ---------------------------------------- | ----------------------------- | ---------------------------------------- |
| 控制流发送  | enableSendMediaStream(trackType, enable) | enableSendMediaStream:enable: | enableSendMediaStream(trackType, enable) |

### 7.3 轨道类型枚举

| **枚举值**           | **数值** | **说明** |
| ----------------- | ------ | ------ |
| AoqTrackTypeAudio | 0      | 音频轨道   |
| AoqTrackTypeVideo | 1      | 视频轨道   |
| AoqTrackTypeData  | 2      | 数据轨道   |

## 8. 视频设备状态监控

### 8.1 功能说明

SDK 自动监测视频采集设备（摄像头）的状态变化，并通过 `onVideoDeviceStateChanged` 回调通知应用层。

### 8.2 设备状态码

| **状态码**                       | **值** | **说明** |
| ----------------------------- | ----- | ------ |
| AoqVideoDeviceNone            | 0     | 初始状态   |
| AoqVideoDeviceCaptureStarting | 1     | 采集启动中  |
| AoqVideoDeviceCaptureStarted  | 2     | 采集已启动  |
| AoqVideoDeviceCaptureStopping | 3     | 采集停止中  |
| AoqVideoDeviceCaptureStopped  | 4     | 采集已停止  |
| AoqVideoDeviceCaptureFail     | 5     | 采集失败   |

### 8.3 回调对照

| **回调** | **Android**                      | **iOS**                    | **Ohos**                         |
| ------ | -------------------------------- | -------------------------- | -------------------------------- |
| 设备状态变化 | onVideoDeviceStateChanged(state) | onVideoDeviceStateChanged: | onVideoDeviceStateChanged(state) |

## 9. 视频错误码与警告码

### 9.1 视频错误码

| **错误码**                 | **值** | **说明**    |
| ----------------------- | ----- | --------- |
| AoqErrorCodeVideo       | 200   | 通用视频错误    |
| VideoExternalBufferFull | 210   | 视频外部缓冲区已满 |
| VideoDevice             | 220   | 视频设备通用错误  |
| CameraOpenFail          | 221   | 摄像头打开失败   |
| CameraAuthFailed        | 222   | 摄像头权限被拒绝  |
| CameraOccupied          | 223   | 摄像头被占用    |
| CameraRunningError      | 224   | 摄像头运行错误   |
| VideoCodec              | 230   | 视频编解码通用错误 |
| EncoderInitFail         | 231   | 编码器初始化失败  |
| VideoRender             | 240   | 视频渲染通用错误  |
| RenderCreateFail        | 241   | 渲染器创建失败   |
| RenderDrawError         | 242   | 渲染绘制错误    |
| Screen                  | 300   | 屏幕共享通用错误  |

<Note>
  Android 额外错误码：ScreenPermissionDenied(310) 屏幕共享权限被拒绝、ScreenForegroundServiceFailed(311) 前台服务启动失败。
</Note>

### 9.2 视频警告码

| **警告码**              | **值** | **说明**  |
| -------------------- | ----- | ------- |
| AoqWCVideo           | 200   | 通用视频警告  |
| CameraEnumerateError | 201   | 摄像头枚举错误 |
| EncoderSwitched      | 202   | 编码器切换警告 |
| RenderDowngrade      | 203   | 渲染降级警告  |

## 附录：完整视频 API 方法列表

| **分类** | **方法名**                        | **说明**     |
| ------ | ------------------------------ | ---------- |
| 采集控制   | startVideoCapture              | 打开视频采集设备   |
| 采集控制   | stopVideoCapture               | 关闭视频采集设备   |
| 采集控制   | switchCamera                   | 切换前后置摄像头   |
| 渲染控制   | setLocalView                   | 设置本地预览窗口   |
| 渲染控制   | setRemoteView                  | 设置远端渲染窗口   |
| 编解码    | setVideoEncoderConfig          | 设置视频编码参数   |
| 外部输入   | pushExternalVideoCapturedFrame | 推送原始视频帧    |
| 外部输入   | pushExternalVideoEncodedFrame  | 推送已编码视频帧   |
| 屏幕共享   | startScreenCapture             | 启动屏幕采集     |
| 屏幕共享   | stopScreenCapture              | 停止屏幕采集     |
| 流控制    | enableSendMediaStream          | 控制媒体流发送    |
| 帧回调    | setVideoFrameObserver          | 注册视频帧观察者   |
| 帧回调    | enableVideoFrameObserver       | 启用/禁用视频帧回调 |
