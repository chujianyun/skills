> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Token鉴权

> AOQ、WebRTC 和 WebSocket 三种协议的鉴权方式

介绍 Realtime API 的 Token 鉴权机制，包括 API Key 的获取方式以及 WebSocket、WebRTC、AOQ 三种协议的建连鉴权方法。

Realtime API 使用 **API Key** 进行身份认证。无论选择 AOQ、WebRTC 还是 WebSocket 协议接入，均通过 HTTP 请求头中的 `Authorization` 字段携带 Bearer Token 完成身份验证。

鉴权仅发生在**建连阶段**，连接建立后的数据传输无需重复鉴权。

三种协议的鉴权方式对比如下：

| **协议**    | **鉴权时机**           | **鉴权方式**                                               | **说明**                           |
| --------- | ------------------ | ------------------------------------------------------ | -------------------------------- |
| AOQ       | 业务 AppServer 请求网关时 | HTTP Header `Authorization: Bearer $DASHSCOPE_API_KEY` | API Key 仅在服务端使用，客户端使用网关返回的 Token |
| WebRTC    | SDP 交换 HTTP 请求时    | HTTP Header `Authorization: Bearer $DASHSCOPE_API_KEY` | 客户端或服务端携带 API Key 发起 SDP 交换      |
| WebSocket | WebSocket 连接握手时    | HTTP Header `Authorization: Bearer $DASHSCOPE_API_KEY` | 客户端或服务端直接携带 API Key 建连           |

## 获取 API Key

### 步骤 1：开通千问AI平台服务

1. 访问[千问AI平台控制台](https://platform.qianwenai.com)并登录您的千问AI平台账号。

2. 如果是首次使用，按照页面提示完成服务开通。

### 步骤 2：创建 API Key

1. 在控制台左侧导航栏中，选择 **API Key**。

2. 点击 **创建 API Key**，选择关联的业务空间。

3. 创建完成后，请**立即复制并妥善保存** API Key。

<Warning>
  **安全提示**：API Key 是您访问服务的唯一凭证，请勿将其硬编码到客户端代码中或提交到代码仓库。建议通过环境变量或后端服务下发的方式管理。
</Warning>

## 建连鉴权详解

### AOQ 协议鉴权

AOQ 采用**服务端代理鉴权**模式：API Key 仅在业务 AppServer 侧使用，客户端使用网关返回的临时 Token 建连，避免 API Key 暴露在客户端。

<img src="https://help-static-aliyun-doc.aliyuncs.com/zh-CN/images/p1088069.jpg" alt="Token鉴权" />

<Tabs>
  <Tab title="Realtime 协议">
    ```curl
    curl -X POST \
      "https://{endpoint}/api/v1/webrtc/realtime?model=qwen3.5-omni-plus-realtime" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "x-dashscope-rtc-transport: moq" \
      -d "{\"clientIp\": \"${CLIENT_REAL_IP}\"}"
    ```
  </Tab>

  <Tab title="Inference 协议">
    ```curl
    curl -X POST \
      "https://{endpoint}/api/v1/webrtc/inference?model=fun-asr-realtime" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "x-dashscope-rtc-transport: moq" \
      -d "{\"clientIp\": \"${CLIENT_REAL_IP}\"}"
    ```
  </Tab>
</Tabs>

#### 参数说明

| **配置项**                   | **值**                       | **说明**                                                                             |
| ------------------------- | --------------------------- | ---------------------------------------------------------------------------------- |
| endpoint                  | 根据业务情况选择接入域名                | 指定对应的接入域名                                                                          |
| Content-Type              | `application/json`          | -                                                                                  |
| Authorization             | `Bearer $DASHSCOPE_API_KEY` | 填写 API Key                                                                         |
| x-dashscope-rtc-transport | `moq`                       | **指定使用 AOQ 协议**                                                                    |
| clientIp                  | 客户端真实公网 IP                  | 选填。不填写时，默认使用请求千问AI平台网关的 IP；填写后以 clientIp 为准。Realtime API 会根据客户端 IP 分配最佳的 Relay 接入点 |

#### 响应示例

```json
{
  "sid": "1d06b55683db49bba67a407902f62d02:1782706970:69aecdc5...",
  "aoqTokenForClient": "ecc1a46015d5496ca4ff7a48281eb739",
  "clientRelayEndpoints": [{"endpoint": "121.199.XX.XX", "port": 8443, "route_index": 0}],
  "clientRelayCertFingerprint": "sha256/99843495...",
  "sidExpiresInSecs": 7200,
  "extraInfo": {"workspaceIdHash": "2021b6f98cea4cff"}
}
```

#### 响应参数说明

| **字段**                     | **说明**                       |
| -------------------------- | ---------------------------- |
| sid                        | 会话唯一标识                       |
| aoqTokenForClient          | 客户端连接令牌，传给 SDK 的 token 字段    |
| clientRelayEndpoints       | Relay 接入点数组（endpoint + port） |
| clientRelayCertFingerprint | Relay TLS 证书指纹               |
| sidExpiresInSecs           | 会话过期时间（秒）                    |
| extraInfo.workspaceIdHash  | 工作区 ID 哈希                    |

#### AOQ Client SDK 连接示例

<Note>
  `clientIp` 为请求体中的选填字段。不填写时，默认使用请求千问AI平台网关的 IP 作为客户端 IP；填写后则以指定的 clientIp 为准。建议由业务 AppServer 获取客户端真实 IP 后填入，以获得最佳的 Relay 接入点。
</Note>

<Tabs>
  <Tab title="iOS (Swift)">
    ```swift
    let resp = try JSONDecoder().decode(AllocateResponse.self, from: responseData)
    let config = AoqConnectConfig()
    config.token = resp.aoqTokenForClient
    config.sid = resp.sid
    config.certFingerprint = resp.clientRelayCertFingerprint
    config.relayEndpoints = resp.clientRelayEndpoints.enumerated().map { index, item in
      let ep = AoqRelayEndpoint()
      // route_index 缺省时按数组下标兜底
      ep.routeIndex = item.routeIndex ?? index
      ep.endpoint = item.endpoint
      ep.port = item.port
      return ep
    }
    config.workspaceIdHash = resp.extraInfo?.workspaceIdHash ?? ""
    let audioTrack = AoqTrackParam()
    audioTrack.trackType = .audio
    let dataTrack = AoqTrackParam()
    dataTrack.trackType = .data
    config.publishTracks = [audioTrack, dataTrack]
    config.subscribeTracks = [audioTrack, dataTrack]
    engine.connect(config)
    ```
  </Tab>

  <Tab title="Android (Java)">
    ```java
    JSONObject obj = new JSONObject(responseText);
    AoqClientEngine.AoqConnectConfig cfg = new AoqClientEngine.AoqConnectConfig();
    cfg.token = obj.optString("aoqTokenForClient", "");
    cfg.sid = obj.optString("sid", "");
    cfg.certFingerprint = obj.optString("clientRelayCertFingerprint", "");
    JSONArray arr = obj.optJSONArray("clientRelayEndpoints");
    if (arr != null) {
      for (int i = 0; i < arr.length(); i++) {
        JSONObject o = arr.optJSONObject(i);
        AoqClientEngine.AoqRelayEndpoint ep = new AoqClientEngine.AoqRelayEndpoint();
        // route_index 缺省时按数组下标兜底
        ep.routeIndex = o.has("route_index") ? o.optInt("route_index", i) : i;
        ep.endpoint = o.optString("endpoint", "");
        ep.port = o.optInt("port", 0);
        cfg.relayEndpoints.add(ep);
      }
    }
    JSONObject ext = obj.optJSONObject("extraInfo");
    cfg.workspaceIdHash = ext != null ? ext.optString("workspaceIdHash", "") : "";
    AoqClientEngine.AoqTrackParam audio = new AoqClientEngine.AoqTrackParam();
    audio.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeAudio;
    AoqClientEngine.AoqTrackParam data = new AoqClientEngine.AoqTrackParam();
    data.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeData;
    cfg.publishTracks.add(audio);
    cfg.publishTracks.add(data);
    cfg.subscribeTracks.add(audio);
    cfg.subscribeTracks.add(data);
    engine.connect(cfg);
    ```
  </Tab>

  <Tab title="OHOS (ArkTS)">
    ```javascript
    const obj = JSON.parse(responseText) as Record<string, Object | undefined>;
    const cfg: AoqConnectConfig = {
      token: String(obj['aoqTokenForClient'] ?? ''),
      sid: String(obj['sid'] ?? ''),
      certFingerprint: String(obj['clientRelayCertFingerprint'] ?? ''),
      relayEndpoints: (obj['clientRelayEndpoints'] as Array<any>).map((item, index) => ({
        // route_index 缺省时按数组下标兜底
        routeIndex: Number(item['route_index'] ?? index),
        endpoint: String(item['endpoint'] ?? ''),
        port: Number(item['port'] ?? 0)
      })),
      workspaceIdHash: String((obj['extraInfo'] as any)?.['workspaceIdHash'] ?? ''),
      publishTracks: [
        { trackType: AoqTrackType.AoqTrackTypeAudio },
        { trackType: AoqTrackType.AoqTrackTypeData }
      ],
      subscribeTracks: [
        { trackType: AoqTrackType.AoqTrackTypeAudio },
        { trackType: AoqTrackType.AoqTrackTypeData }
      ]
    };
    engine.connect(cfg);
    ```
  </Tab>
</Tabs>

### WebRTC 协议鉴权

WebRTC 通过 HTTP POST 请求完成 SDP 交换，鉴权在此阶段完成。客户端将 Offer SDP 发送至服务端，服务端返回 Answer SDP。

| **配置项**       | **值**                                                          | **说明**                                                                                                                 |
| ------------- | -------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| 请求方法          | POST                                                           | -                                                                                                                      |
| 请求地址          | `https://{endpoint}/api/v1/webrtc/realtime?model={model_name}` | 使用时替换 endpoint 和 model\_name，不同模型的连接地址不同，详情请参见[WebRTC 接入](/developer-guides/realtime-api/connect-model#conn-rtc-title) |
| Content-Type  | `application/sdp`                                              | 请求体为 SDP 字符串                                                                                                           |
| Authorization | `Bearer $DASHSCOPE_API_KEY`                                    | 填写 API Key                                                                                                             |
| 响应            | HTTP 200，返回 Answer SDP                                         | 失败返回 4xx                                                                                                               |

```javascript
const pc = new RTCPeerConnection();
const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
stream.getAudioTracks().forEach(t => pc.addTrack(t, stream));
pc.createDataChannel('oai-events');
const offer = await pc.createOffer();
await pc.setLocalDescription(offer);
// 等待 ICE 收集完成后发送
const resp = await fetch(API_URL, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/sdp',
    'Authorization': `Bearer ${API_KEY}`,
  },
  body: pc.localDescription.sdp,
});
const answerSdp = await resp.text();
await pc.setRemoteDescription({ type: 'answer', sdp: answerSdp });
```

### WebSocket 协议鉴权

WebSocket 的鉴权方式最为简单，在建立连接时直接通过 HTTP Header 携带 API Key 即可。

| **配置项**       | **值**                                                                | **说明**                                                                                      |
| ------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| 连接地址          | `wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model={model_name}` | 不同模型的连接地址不同，详情请参见[WebSocket 接入](/developer-guides/realtime-api/connect-model#conn-ws-title) |
| Authorization | `Bearer $DASHSCOPE_API_KEY`                                          | 填写 API Key                                                                                  |

```python
import websocket, os
API_KEY = os.getenv("DASHSCOPE_API_KEY")
URL = "wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=qwen3.5-omni-plus-realtime"
ws = websocket.WebSocketApp(URL, header=["Authorization: Bearer " + API_KEY])
ws.run_forever()
```
