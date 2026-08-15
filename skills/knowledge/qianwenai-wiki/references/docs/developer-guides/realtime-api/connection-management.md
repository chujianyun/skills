> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 连接状态管理

> AOQ SDK 连接状态图、状态迁移规则和 API

本章节介绍 AOQ Client SDK 的连接状态机及其对应的 API 调用。

## 连接状态图

下图描述了 AOQ Client SDK 的连接状态迁移关系：

![p1088081.png](https://g-adoc.alcasset.com/media/maas_docs/maas-cn/common/images/6a4b3c2d1e0f9ead.png)

## 状态说明

| 状态                | 枚举值 | 说明                                   |
| ----------------- | --- | ------------------------------------ |
| 链接中（Connecting）   | 1   | 调用 `connect` 后进入，正在与 AI Service 建立连接 |
| 已连接（Connected）    | 2   | 连接建立成功，可正常收发音视频和数据消息                 |
| 失败（Failed）        | 3   | 连接异常（鉴权失败/超时/服务端拒绝等），SDK 内部会自动迁移到已断开 |
| 已断开（Disconnected） | 0   | 初始状态/主动断开/异常断开后的终态                   |

## 状态迁移规则

1. **App 调用** `connect` → 进入 `Connecting` 状态。
2. **链接成功** → 从 `Connecting` 迁移到 `Connected`。
3. **链接异常** → 从 `Connecting` 迁移到 `Failed`，随后 SDK 自动迁移到 `Disconnected`。
4. **链接异常** → 从 `Connected` 迁移到 `Failed`，随后 SDK 自动迁移到 `Disconnected`。
5. **App 调用** `disconnect` → 从 `Connected` 迁移到 `Disconnected`。

<Note>
  `Failed` 是瞬态，SDK 触发 `onConnectionStatusChange(Failed)` 后会自动迁移到 `Disconnected`，业务层无需手动调用 disconnect。
</Note>

## connect API

调用 `connect` 发起与 AI Service 的连接，传入由 AppServer allocate 接口返回的鉴权凭证。

### 方法签名

<Tabs>
  <Tab title="Android">
    ```java
    public abstract int connect(@NonNull AoqConnectConfig config);
    ```
  </Tab>

  <Tab title="iOS">
    ```objectivec
    - (int)connect:(AoqConnectConfig * _Nonnull)config;
    ```
  </Tab>

  <Tab title="HarmonyOS">
    ```javascript
    connect(config: AoqConnectConfig): number;
    ```
  </Tab>
</Tabs>

**返回值：** `0` 表示调用成功（异步建连）；`< 0` 表示失败。

### 行为说明

- 调用后触发 `onConnectionStatusChange(connecting)` 回调。
- 如果链接成功时触发 `onConnectionStatusChange(connected)` 回调。
- 如果链接失败时触发 `onConnectionStatusChange(failed)` 回调。

## disconnect API

调用 `disconnect` 主动断开与 AI Service 的连接。

### 方法签名

<Tabs>
  <Tab title="Android">
    ```java
    public abstract int disconnect();
    ```
  </Tab>

  <Tab title="iOS">
    ```objectivec
    - (int)disconnect;
    ```
  </Tab>

  <Tab title="HarmonyOS">
    ```javascript
    disconnect(): number;
    ```
  </Tab>
</Tabs>

**返回值：** `0` 表示成功；`< 0` 表示失败。

### 行为说明

- 调用后触发 `onConnectionStatusChange(Disconnected)` 回调。
- 引擎不会自动释放，可重新调用 `connect` 进行重连。
- 未连接状态下调用 `disconnect` 是安全的，返回 0。

## onConnectionStatusChange 回调

连接状态变化时，SDK 通过此回调通知业务层。

<Tabs>
  <Tab title="Android">
    ```java
    public void onConnectionStatusChange(
      @NonNull AoqClientEngine.AoqConnectionStatus status) {}
    ```
  </Tab>

  <Tab title="iOS">
    ```objectivec
    - (void)onConnectionStatusChange:(AoqConnectionStatus)status;
    ```
  </Tab>

  <Tab title="HarmonyOS">
    ```javascript
    onConnectionStatusChange?: (status: AoqConnectionStatus) => void;
    ```
  </Tab>
</Tabs>

### 示例代码

```swift
func onConnectionStatusChange(_ status: AoqConnectionStatus) {
  switch status {
  case .connecting:
    print("正在连接...")
  case .connected:
    print("连接成功")
    // 连接成功后可发送 session.update
  case .failed:
    print("连接失败")
    // SDK 会自动迁移到 disconnected，无需手动 disconnect
  case .disconnected:
    print("已断开")
    // 可根据业务决定是否重连
  }
}
```
