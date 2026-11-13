# API 密钥

词元跳动使用 API Key 认证所有模型与开放平台请求。同一个 Key 可用于全部协议，并可独立设置名称、额度、
过期时间和 RPM。

## 创建密钥 {#create-key}

登录后进入 [API 密钥](https://tokendance.space/keys)，点击「创建密钥」。创建成功时完整 Key 只显示一次，请立即保存到密码管理器、
系统密钥链或部署 Secret；遗失后无法找回，只能删除旧 Key 并重新创建。

如果 CLI、桌面客户端或第三方产品需要在用户确认后自动创建 Key，请使用独立的
[OAuth 式 API Key 授权](OAuth%20%E5%BC%8F%20API%20Key%20%E6%8E%88%E6%9D%83.md)，不要要求用户复制控制台中的长期密钥。

## 使用密钥 {#use-key}

优先使用各协议的官方 SDK，并把 Key 交给 SDK 的 API Key 参数。SDK 会自动使用对应协议的原生认证头；
自定义 HTTP 客户端也可以统一使用：

```http
Authorization: Bearer YOUR_KEY
```

```bash title="环境变量"
export TOKENDANCE_API_KEY="YOUR_KEY"
```

```python title="Python"
import os

api_key = os.environ["TOKENDANCE_API_KEY"]
```

具体 base URL、端点和 SDK 示例见 [多协议支持](../../%E6%A8%A1%E5%9E%8B%E4%B8%8E%E5%8D%8F%E8%AE%AE/%E9%80%89%E6%8B%A9%E6%A8%A1%E5%9E%8B%E4%B8%8E%E5%8D%8F%E8%AE%AE/%E5%8D%8F%E8%AE%AE%E6%80%BB%E8%A7%88.md) 下的独立协议文档。

## 密钥安全 {#key-security}

- 不要把 Key 硬编码到源码、日志、聊天记录或浏览器前端代码中；
- 不要把 Key 提交到版本控制系统；
- 为不同产品、环境和用途创建不同 Key；
- 为临时任务设置过期时间和额度上限；
- 怀疑泄露时立即禁用或删除 Key。

## 额度限制 {#key-limits}

每个 Key 可以设置独立额度。达到上限后，该 Key 无法继续调用，同一账户下的其他 Key 不受影响。

| 周期 | 行为 |
|---|---|
| 不刷新 | 从创建起累计，达到上限后不自动恢复 |
| 每日 | 每天 00:00 刷新 |
| 每周 | 每周一 00:00 刷新 |
| 每月 | 每月 1 日 00:00 刷新 |

时间按中国时区计算。额度留空或设为 `0` 表示不限制；密钥详情页会展示总用量和各周期用量。

## RPM 限制 {#rpm-limits}

| 设置 | 行为 |
|---|---|
| 留空或 `0` | 跟随账户级 RPM |
| 正整数 | 使用 Key 与账户限制中的较小值 |

超过限制时接口返回 `429`。Key 级 RPM 是账户级 RPM 下的子限制，不会绕过账户并发或 RPM 上限。

## 禁用、删除与过期 {#lifecycle}

禁用后 Key 会立即失效，但可以重新启用。删除后 Key 立即失效并从控制台隐藏，且不可恢复。设置过期时间后，
Key 会在到期时自动停止工作。

通过 OAuth 式授权代用户持有 Key 的产品，可以根据 TokenDance API 返回的
`TokenDance-Recovery-Action` 引导充值、重新授权或等待周期额度刷新，具体规则见
[OAuth 式 API Key 授权：处理 Key 失效与余额不足](OAuth%20%E5%BC%8F%20API%20Key%20%E6%8E%88%E6%9D%83.md#recover-key)。

## 用量排查 {#usage}

在 [调用记录](https://tokendance.space/activity/requests) 中按 Key 名称、模型、供应商和费用排查调用来源与成本。若应用需要通过
API Key 或请求维度记录 App URL，请同时阅读 [应用归因](../%E5%BA%94%E7%94%A8%E4%B8%8E%E5%BC%80%E6%94%BE%E8%83%BD%E5%8A%9B/%E5%BA%94%E7%94%A8%E5%BD%92%E5%9B%A0.md)。

## 相关文档 {#related}

- [OAuth 式 API Key 授权](OAuth%20%E5%BC%8F%20API%20Key%20%E6%8E%88%E6%9D%83.md) — 让应用在用户确认后自动获得新 Key
- [快速开始](../%E5%BF%AB%E9%80%9F%E5%85%A5%E9%97%A8/%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B.md) — 完成第一次模型调用
- [多协议支持](../../%E6%A8%A1%E5%9E%8B%E4%B8%8E%E5%8D%8F%E8%AE%AE/%E9%80%89%E6%8B%A9%E6%A8%A1%E5%9E%8B%E4%B8%8E%E5%8D%8F%E8%AE%AE/%E5%8D%8F%E8%AE%AE%E6%80%BB%E8%A7%88.md) — 选择协议及对应 SDK
- [请求限流](../%E8%B7%AF%E7%94%B1%E4%B8%8E%E5%8F%AF%E7%94%A8%E6%80%A7/%E8%AF%B7%E6%B1%82%E9%99%90%E6%B5%81.md) — 账户与 Key 的限流规则
