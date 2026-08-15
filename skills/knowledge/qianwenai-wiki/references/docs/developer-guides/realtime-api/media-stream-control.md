> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 媒体流发送管理

> AOQ SDK 媒体流发送的启停控制

`enableSendMediaStream`用于控制客户端是否向 AI 服务发送音频/视频媒体流，在 AOQ 协议接入场景中精确控制发送时机。

## 概述

`enableSendMediaStream`用于控制客户端是否向 AI 服务发送音频/视频媒体流。在 AOQ 协议接入场景中，部分模型要求在收到`session.updated`确认后才能接收媒体数据，因此需要通过此接口精确控制发送时机。

## API 定义

<Tabs>
  <Tab title="iOS / Mac">
    ```swift
    // iOS / Mac
    func enableSendMediaStream(_ trackType: AoqTrackType, enable: Bool)
    ```
  </Tab>

  <Tab title="Android">
    ```java
    // Android
    void enableSendMediaStream(AoqTrackType trackType, boolean enable)
    ```
  </Tab>

  <Tab title="HarmonyOS (ArkTS)">
    ```javascript
    // HarmonyOS (ArkTS)
    enableSendMediaStream(trackType: AoqTrackType, enable: boolean): void
    ```
  </Tab>
</Tabs>

**参数说明：**

| 参数        | 类型           | 说明                         |
| --------- | ------------ | -------------------------- |
| trackType | AoqTrackType | 媒体轨道类型：`.audio`或`.video`   |
| enable    | Bool         | `true`= 开启发送，`false`= 暂停发送 |

## 控制流程

典型的媒体流控制流程如下：

![媒体流控制流程](https://help-static-aliyun-doc.aliyuncs.com/zh-CN/images/p1088082.svg)

## 使用示例（iOS Swift）

### connect 前禁用发送

```swift
// 连接前关闭音视频发送，避免模型未就绪时收到数据
engine.enableSendMediaStream(.audio, enable: false)
engine.enableSendMediaStream(.video, enable: false)
// 发起连接
engine.connect(config)
```

### 收到 session.updated 后开启

```swift
func onDataMsg(_ msg: AoqDataMsg) {
  guard let obj = try? JSONSerialization.jsonObject(with: msg.data) as? [String: Any],
        let type = obj["type"] as? String else { return }
  if type == "session.updated" {
    // AI 侧已确认会话配置，开启媒体发送
    engine.enableSendMediaStream(.audio, enable: true)
    engine.enableSendMediaStream(.video, enable: true)
  }
}
```

## 注意事项

- **调用时机**：必须在`createEngine`之后调用，引擎未创建时调用无效。
- **默认行为**：如果不调用此接口，connect 成功后 SDK 会立即开始发送媒体流。
- **模型兼容性**：部分模型要求先收到`session.updated`再接收媒体数据，建议统一采用"先禁用、后开启"模式。
- **独立控制**：音频和视频可独立控制，例如仅发送音频不发送视频。

## 常见场景

| 场景                 | 操作                      | 说明                     |
| ------------------ | ----------------------- | ---------------------- |
| 连接模型前              | `enable(.audio, false)` | 等待 session.updated 再发送 |
| 收到 session.updated | `enable(.audio, true)`  | AI 已就绪，开始发送            |
