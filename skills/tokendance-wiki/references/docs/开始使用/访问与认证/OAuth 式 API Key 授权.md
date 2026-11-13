# OAuth 式 API Key 授权

应用可以在用户确认后创建一个新的 TokenDance API Key，无需让用户进入控制台手动复制。该流程使用
Authorization Code，并支持 [PKCE](https://oauth.net/2/pkce/) 保护 code 交换。

## PKCE 接入指南

### 第一步：将用户带到 TokenDance {#authorize}

将用户跳转到 TokenDance 的 `/auth` 页面，并通过 `callback_url` 指定授权完成后的返回地址。

推荐使用 S256 code challenge：

```text title="使用 S256（推荐）"
https://tokendance.space/auth?callback_url=<CALLBACK_URL>&code_challenge=<CODE_CHALLENGE>&code_challenge_method=S256&app_url=<APP_URL>&key_name=<KEY_NAME>
```

有回调的应用也可以不使用 code challenge：

```text title="不使用 PKCE"
https://tokendance.space/auth?callback_url=<CALLBACK_URL>&app_url=<APP_URL>&key_name=<KEY_NAME>
```

授权参数：

- `callback_url`：授权完成后的回调地址；
- `code_challenge`、`code_challenge_method`：S256 PKCE 参数，callback 模式可选，Headless 模式必需；
- `app_url`：写入新 Key 的 App URL（应用归因的唯一要素），后续使用该 Key 的调用会自动继承，详见
  [应用归因](../%E5%BA%94%E7%94%A8%E4%B8%8E%E5%BC%80%E6%94%BE%E8%83%BD%E5%8A%9B/%E5%BA%94%E7%94%A8%E5%BD%92%E5%9B%A0.md#dimensions)；
- `key_name`：Key 名称和授权页中的应用展示名称。

用户登录后会确认 Key 的最终名称、额度、周期、过期时间和 RPM。授权完成后，TokenDance 会保留
callback URL 中已有的路径和查询参数，再追加 `code` 并重定向：

```text title="授权完成后的 callback"
<CALLBACK_URL>?code=<CODE>
```

调用方如需关联多个并发流程，可以自行把不透明流程标识放进 callback URL，或在本地维护对应关系。

::: tip
使用 S256 可以避免 callback 中的一次性 code 被截获后直接交换成 Key。生成 challenge 后，原始
`code_verifier` 只应保存在发起授权的客户端。
:::

#### 生成 S256 code challenge {#pkce}

```javascript title="生成 code challenge"
const verifier = crypto.randomUUID() + crypto.randomUUID()
const digest = await crypto.subtle.digest(
  'SHA-256',
  new TextEncoder().encode(verifier),
)
const challenge = btoa(String.fromCharCode(...new Uint8Array(digest)))
  .replace(/\+/g, '-')
  .replace(/\//g, '_')
  .replace(/=+$/, '')
```

`code_verifier` 必须使用 43–128 个字母、数字或 `-._~` 字符。

#### 本地应用

localhost/loopback callback 支持任意端口。桌面客户端和本机 CLI 可以先监听一个随机空闲端口，再使用
类似 `http://127.0.0.1:51423/callback` 的地址接收 code。

`app_url` 不应使用随机 callback 端口，而应填写稳定的 App URL。它会记录在新创建的 API Key 上并自动继承到
后续调用；单次请求仍可通过 `X-App-URL` 显式传递请求维度，并覆盖 Key 上的 App URL，详见
[应用归因](../%E5%BA%94%E7%94%A8%E4%B8%8E%E5%BC%80%E6%94%BE%E8%83%BD%E5%8A%9B/%E5%BA%94%E7%94%A8%E5%BD%92%E5%9B%A0.md#dimensions)。

#### Headless 应用（SSH、远程开发机、容器） {#headless}

如果客户端无法接收 localhost callback，可以省略 `callback_url`：

```text title="Headless（无回调）"
https://tokendance.space/auth?code_challenge=<CODE_CHALLENGE>&code_challenge_method=S256&app_url=<APP_URL>&key_name=<KEY_NAME>
```

用户确认后，授权页不会重定向，而是显示一个 10 分钟有效的一次性 code。用户将 code 复制回原客户端，
客户端再按照第二步完成交换。

Headless 模式必须使用 S256 PKCE。即使 code 被其他人看到，没有客户端保存的 `code_verifier` 也无法
交换出 Key。

::: note
Headless 仍然需要用户在浏览器中登录、确认并复制 code；浏览器可以位于另一台设备。完全无人值守的
CI、定时任务和后台服务无法完成交互授权，应预先安全配置 API Key。
:::

### 第二步：用 code 交换 API Key {#exchange}

有回调模式可以从 URL 中读取 code：

```javascript title="从 callback 读取 code"
const code = new URLSearchParams(window.location.search).get('code')
```

Headless 模式则从用户粘贴的内容中取得 code。客户端应在 10 分钟内向交换接口提交 code；使用 PKCE 时，
同时提交最初保存的 verifier：

```bash title="使用 PKCE 交换"
curl https://tokendance.space/portal/api/v1/auth/keys \
  -H 'Content-Type: application/json' \
  -d '{
    "code": "授权码",
    "code_verifier": "客户端保存的原始 verifier",
    "code_challenge_method": "S256"
  }'
```

只有未使用 PKCE 的有回调模式可以只提交 code：

```bash title="未使用 PKCE"
curl https://tokendance.space/portal/api/v1/auth/keys \
  -H 'Content-Type: application/json' \
  -d '{"code":"授权码"}'
```

成功响应：

```json title="成功响应"
{"key":"新创建的 TokenDance API Key"}
```

完整 Key 只在首次成功交换的响应中出现。错误 verifier 不会消费 code；正确交换后 code 立即失效，不能
重放。如果交换已成功但客户端丢失响应，平台无法再次展示该 Key，只能重新授权并删除旧 Key。

### 第三步：使用 API Key {#use-key}

客户端应立即把 Key 写入系统密钥链、部署 Secret 或受保护的环境配置。接下来根据所用 SDK 和接口阅读
[多协议支持](../../%E6%A8%A1%E5%9E%8B%E4%B8%8E%E5%8D%8F%E8%AE%AE/%E9%80%89%E6%8B%A9%E6%A8%A1%E5%9E%8B%E4%B8%8E%E5%8D%8F%E8%AE%AE/%E5%8D%8F%E8%AE%AE%E6%80%BB%E8%A7%88.md)，设置对应的 base URL、鉴权方式和模型 ID。

不要把完整 Key 写入日志、URL、Git 或不受信任的网页前端。

### 可选：处理 Key 失效与余额不足 {#recover-key}

使用 Key 调用 TokenDance API 失败时，产品可以检查响应头
`TokenDance-Recovery-Action`。只有 TokenDance 明确判断出恢复路径时，响应才会携带该字段。

| `TokenDance-Recovery-Action` | TokenDance 已确认的场景 | 产品应执行的动作 |
|---|---|---|
| `top_up_balance` | 用户账户可用余额不足 | 引导用户充值；当前 Key 仍然有效 |
| `reauthorize_api_key` | Key 缺失、不存在、禁用、过期，或达到不刷新的总额度 | 重新执行本文授权流程 |
| `api_key_quota` | Key 达到每日、每周或每月额度 | 选择提示用户等待额度刷新，或重新执行授权流程 |

浏览器跨域请求也可以直接读取该响应头：

```javascript title="读取恢复动作"
const response = await fetch(url, requestInit)

if (!response.ok) {
  switch (response.headers.get('TokenDance-Recovery-Action')) {
    case 'top_up_balance':
      showTopUpFlow()
      break
    case 'reauthorize_api_key':
      showAPIKeyAuthorizationFlow()
      break
    case 'api_key_quota':
      showAPIKeyQuotaRecoveryFlow()
      break
    default:
      handleProtocolError(response)
  }
}
```

响应头缺失或 action 未识别时，按接口原有错误信息处理。

## 错误处理 {#errors}

- `400`：callback URL 不合法，PKCE 参数不完整，或 method 不是 `S256`；
- `400`：Headless 模式没有提供 S256 challenge；
- `403`：code 无效、已过期、已使用，或 verifier 不匹配；
- 交换成功后丢失响应：完整 Key 无法恢复，需要重新授权。

## 相关文档 {#related}

- [API Key](API%20%E5%AF%86%E9%92%A5.md) — 使用、限制和管理 Key
- [应用归因](../%E5%BA%94%E7%94%A8%E4%B8%8E%E5%BC%80%E6%94%BE%E8%83%BD%E5%8A%9B/%E5%BA%94%E7%94%A8%E5%BD%92%E5%9B%A0.md) — 同一个 App URL 在 API Key 与单次请求上的两个维度
- [用 AI 接入](../%E5%BF%AB%E9%80%9F%E5%85%A5%E9%97%A8/%E7%94%A8%20AI%20%E6%8E%A5%E5%85%A5.md) — 让 coding agent 自动完成授权与项目配置
- [开放平台 API](../%E5%BA%94%E7%94%A8%E4%B8%8E%E5%BC%80%E6%94%BE%E8%83%BD%E5%8A%9B/%E5%BC%80%E6%94%BE%E5%B9%B3%E5%8F%B0%20API.md) — 使用已有 Key 管理账户
