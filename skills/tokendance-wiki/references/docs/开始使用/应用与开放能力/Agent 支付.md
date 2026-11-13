# Agent 支付

当模型调用返回余额不足时，Agent 可以使用当前 API Key 发起充值。用户完成支付后，Agent 确认到账并重试
原请求即可。

接入流程：

1. 询问用户是否充值，并确认充值金额；
2. 创建支付会话，将支付链接交给用户；
3. 查询支付状态；
4. 支付成功后重试原模型请求。

## 认证与入口 {#authentication}

支付接口使用与模型调用相同的 API Key：

```text
Authorization: Bearer YOUR_KEY
```

充值会进入该 API Key 所属的 TokenDance 账户，实际付款必须由用户确认。

## 创建充值会话 {#create-session}

请求只需传入充值金额。`amount` 是以元为单位的整数，单笔金额最低 1 元、最高 10 万元，不支持小数。

```bash title="创建 10 元充值会话"
curl https://tokendance.space/portal/api/v1/payment/sessions \
  -H 'Authorization: Bearer YOUR_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"amount":10}'
```

```json title="201 Created"
{
  "session": {
    "id": "SESSION_ID",
    "amount": 10,
    "status": "pending",
    "payment_url": "https://pay.example.com/session/...",
    "alipay_url": "alipays://platformapi/startapp?appId=...&url=https%3A%2F%2Fpay.example.com%2Fsession%2F...",
    "status_url": "https://tokendance.space/portal/api/v1/payment/sessions/SESSION_ID",
    "expired_at": 1786500000,
    "created_at": 1786499400
  }
}
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | string | 支付会话 ID |
| `amount` | integer | 充值金额，单位为元 |
| `status` | string | 会话状态；创建时为 `pending` |
| `payment_url` | string | 支付渠道返回的聚合码内容，供 PC 端渲染二维码 |
| `alipay_url` | string，可选 | 支付宝 App 深链，供移动端由用户点击后唤起支付宝；旧会话或暂不可用时可能缺失 |
| `status_url` | string | 查询支付结果的完整 URL |
| `expired_at` | integer | 会话过期时间，Unix 秒 |
| `created_at` | integer | 会话创建时间，Unix 秒 |

### PC 与移动端支付链路 {#payment-flow}

- PC 端将 `payment_url` 渲染成二维码，用户可以使用微信或支付宝扫码支付；
- 移动端仅支持支付宝。界面应明确显示“支付宝支付”，并在用户点击按钮时打开 `alipay_url`，不要在创建会话的
  异步响应返回后自动跳转；
- 移动端不要打开或展示 `payment_url`，它是聚合码的二维码内容，不是移动网页的支付跳转地址；
- `alipay_url` 缺失时，应提示用户改用 PC 端扫码或稍后重试；支付宝未安装或深链被浏览器拦截时，应提示用户
  检查安装状态、允许浏览器打开 App，或换用系统浏览器；
- 唤起支付宝和用户返回页面都不代表支付成功。客户端必须继续使用完整的 `status_url` 查询结果，只有状态变为
  `paid` 才能展示支付成功并重试模型请求。

## 查询支付状态 {#get-session}

使用创建响应中的 `status_url` 查询状态：

```bash
curl https://tokendance.space/portal/api/v1/payment/sessions/SESSION_ID \
  -H 'Authorization: Bearer YOUR_KEY'
```

建议每 3 秒查询一次，并在 `expired_at` 后停止：

- `pending`：等待用户支付；
- `paid`：充值已经到账，可以重试模型请求；
- `failed`、`closed` 或 `refunded`：本次支付未完成，请向用户说明结果；如需继续充值，重新创建支付会话。

支付成功的响应还会包含 `paid_at`。

## 相关文档 {#related}

- [开放平台 API](%E5%BC%80%E6%94%BE%E5%B9%B3%E5%8F%B0%20API.md) — API Key 认证与余额查询
- [API 密钥](../%E8%AE%BF%E9%97%AE%E4%B8%8E%E8%AE%A4%E8%AF%81/API%20%E5%AF%86%E9%92%A5.md) — 创建和管理密钥
- [用 AI 接入](../%E5%BF%AB%E9%80%9F%E5%85%A5%E9%97%A8/%E7%94%A8%20AI%20%E6%8E%A5%E5%85%A5.md) — 让 Agent 选择完整接入方案
