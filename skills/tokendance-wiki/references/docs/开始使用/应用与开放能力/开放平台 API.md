# 开放平台 API

除了通过控制台管理账户，你还可以使用 API Key 直接调用开放平台接口，实现余额查询、兑换码兑换等账户管理操作。

AI 和其他机器客户端可以通过 [llms.txt](https://tokendance.space/llms.txt) 发现本文的 Markdown 版本。

::: note
开放平台 API 使用与模型调用相同的 API Key 进行认证，无需额外创建密钥。
:::

## 认证方式 {#authentication}

所有开放平台接口通过 `Authorization` 请求头传递 API Key：

```
Authorization: Bearer YOUR_KEY
```

## 查询余额 {#get-balance}

查询当前 API Key 所属用户的账户余额。

| 请求方式 | 路径 | 认证 |
|---|---|---|
| GET | /api/v1/user/balance | Bearer Token |

### 响应 {#balance-response}

```json title="200 OK"
{
  "balance": {
    "credits": 58000000,
    "credits_used": 57837189,
    "balance": 162811
  }
}
```

字段说明：

本文所有额度金额字段的单位均为微元，`1 元 = 1,000,000 微元`。

- `credits` — 总额度（充值获得）
- `credits_used` — 已消耗额度
- `balance` — 剩余可用额度（credits - credits_used）

### 调用示例 {#balance-examples}

:::group

```bash title="cURL"
curl https://tokendance.space/portal/api/v1/user/balance \
  -H "Authorization: Bearer YOUR_KEY"
```

```python title="Python"
import requests

response = requests.get(
    "https://tokendance.space/portal/api/v1/user/balance",
    headers={"Authorization": "Bearer YOUR_KEY"}
)
data = response.json()
print(f"剩余额度: {data['balance']['balance']}")
```

```javascript title="Node.js"
const response = await fetch('https://tokendance.space/portal/api/v1/user/balance', {
  headers: { 'Authorization': 'Bearer YOUR_KEY' },
});
const data = await response.json();
console.log('剩余额度:', data.balance.balance);
```

:::

## 使用兑换码 {#redeem-code}

使用兑换码为当前 API Key 所属用户增加额度。同一个用户不能重复兑换同一个兑换码。

| 请求方式 | 路径 | 认证 |
|---|---|---|
| POST | /api/v1/redemption/redeem | Bearer Token |

### 请求 {#redeem-code-request}

```json
{
  "code": "YOUR_REDEMPTION_CODE"
}
```

### 响应 {#redeem-code-response}

`credits` 是本次兑换获得的额度。

```json title="200 OK"
{
  "credits": 1000000
}
```

### 调用示例 {#redeem-code-example}

```bash title="cURL"
curl https://tokendance.space/portal/api/v1/redemption/redeem \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"code":"YOUR_REDEMPTION_CODE"}'
```

## 查询用量记录 {#get-usage}

按记录 ID 倒序返回当前 API Key 所属用户的调用记录，新的在前。`limit` 与 `offset` 仍可分页；若查询期间不断产生新记录，向更旧方向翻页时建议使用上一页最后一条记录的 ID 作为 `end_id`，避免新记录把页位置顶偏。

同一个用户 1 秒内最多调用 1 次，超出会返回 `429`。

目前只提供记录列表；按天、按小时聚合和 Top 模型等统计接口暂未对外开放。

| 请求方式 | 路径 | 认证 |
|---|---|---|
| GET | /api/v1/usage | Bearer Token |

### 请求参数 {#get-usage-request}

所有参数均为可选，以查询字符串传入。

| 参数          | 默认值   | 说明                                                                                    |
|---------------|----------|-----------------------------------------------------------------------------------------|
| limit         | 20       | 单页最多记录数量，取值范围为 1–500                                                      |
| offset        | 0        | 跳过的记录数，游标筛选后生效                                                            |
| start_id      | —        | 只查 ID 大于 start_id 的记录                                                            |
| end_id        | —        | 只查 ID 小于 end_id 的记录                                                              |
| window        | 不限时间 | 时间窗口，支持 `1h`、`24h`、`7d` 等时长，或 `YYYYMMDD-YYYYMMDD`（北京时间，含起止两天） |
| model_id      | —        | 按模型 ID 精确筛选                                                                      |
| provider_name | —        | 按服务商名称精确筛选，取值需与控制台用量页显示的名称完全一致                            |
| key_id        | —        | 按 API Key ID 筛选                                                                      |
| is_success    | —        | `true` 只看成功请求，`false` 只看失败请求                                               |

`start_id` 和 `end_id` 可单独传入。两者同时传入时共同限定 ID 区间：只返回严格位于较小 ID 与较大 ID 之间的记录，两端均不包含；传入顺序不影响结果。例如 `start_id=90&end_id=100` 只查 ID 为 91–99 的记录。游标筛选后再应用 `offset` 和 `limit`。本页首尾 ID 只能界定本页之间的范围；继续向更旧的记录翻页时只传 `end_id`。

### 响应 {#get-usage-response}

```json title="200 OK"
{
  "items": [
    {
      "id": "01M27QDHAS167659PEZ5J9YEPQ",
      "model_id": "01M204SS8083CA5ZCA6DRD24DQ",
      "key_id": "01KSQH2CFJPX4XWTGZY024HK3H",
      "key_name": "生产环境",
      "user_id": "01KNR96CWAWPQS527CSEY0XCX0",
      "endpoint_id": "01M205E3D1G54JYRQQTT64W4HF",
      "provider_name": "DeepSeek",
      "created_at": "2026-09-11T07:55:20Z",
      "input_tokens": 72730,
      "output_tokens": 434,
      "total_tokens": 73164,
      "cost": 7687,
      "pricing_version": 14,
      "streaming": false,
      "finish_reason": "stop_sequence",
      "trace_id": "b811d03df7e57743022347fb2c65b179",
      "latency_ms": 0,
      "e2e_ms": 3248,
      "throughput": 133.6206896551724,
      "cached_tokens": 72064
    }
  ],
  "total": 0,
  "offset": 0,
  "limit": 20
}
```

字段说明：

- `created_at` 为 UTC 时间（ISO 8601，以 `Z` 结尾）；
- `cost` 单位为微元，`1 元 = 1,000,000 微元`；
- `input_tokens` / `output_tokens` / `total_tokens` 为本次调用的 Token 用量，`cached_tokens` 为其中命中缓存的输入部分；
- `latency_ms` 是首事件延迟（近似首字延迟），`e2e_ms` 是端到端延迟，`throughput` 是输出吞吐（tokens/s）；
  非流式请求和异步任务没有首事件，`latency_ms` 为 `0`，历史非流式记录可能与 `e2e_ms` 相同；
- `user_id`、`endpoint_id`、`key_id`、`model_id`、`trace_id` 是平台内部标识，可用于与工单或日志对账；
- `model_slug` 仅在模型有展示别名时出现；
- `key_name` 是发起本次调用的 API Key 名称，Key 已删除时仍保留原名称；
- `error` 仅在请求失败时出现，成功时该字段缺失；
- 响应不会单独返回 `start_id` 或 `end_id`；客户端从 `items[0].id` 和 `items[items.length - 1].id` 取得本页首尾 ID。`items` 为空时没有可用游标；
- `total` 恒为 `0`，本接口不返回记录总数。请按 `items` 判断是否还有下一页：`items` 为空或条数少于 `limit` 时即为最后一页。

例如第一页返回 20 条记录后，下一次请求传入该页最后一条的 ID 作为 `end_id`，并保持相同筛选条件、将 `offset` 设为 `0`；这样会从它后面的更旧记录开始取。要检查是否出现更新记录，则传入当前页第一条的 ID 作为 `start_id`。只递增 `offset` 而不带游标时，新插入的记录仍可能导致跨页重复或遗漏。

### 调用示例 {#get-usage-example}

:::group

```bash title="cURL"
curl "https://tokendance.space/portal/api/v1/usage?window=7d&limit=20" \
  -H "Authorization: Bearer YOUR_KEY"

# 下一页：把上一页 items 中最后一条的 id 填入 end_id
curl "https://tokendance.space/portal/api/v1/usage?window=7d&limit=20&end_id=LAST_ITEM_ID" \
  -H "Authorization: Bearer YOUR_KEY"
```

```python title="Python"
import requests

response = requests.get(
    "https://tokendance.space/portal/api/v1/usage",
    headers={"Authorization": "Bearer YOUR_KEY"},
    params={"window": "7d", "limit": 20},
)
data = response.json()
print(f"本页 {len(data['items'])} 条记录")
```

```javascript title="Node.js"
const url = new URL('https://tokendance.space/portal/api/v1/usage');
url.searchParams.set('window', '7d');
url.searchParams.set('limit', '20');
const response = await fetch(url, {
  headers: { 'Authorization': 'Bearer YOUR_KEY' },
});
const data = await response.json();
console.log('本页记录数:', data.items.length);
```

:::

## 错误处理 {#errors}

接口返回统一的错误格式：

```json
{
  "error": {
    "code": "unauthorized",
    "message": "Invalid or expired API key"
  }
}
```

| HTTP 状态码 | code | 说明 |
|---|---|---|
| 400 | invalid_request | 参数校验失败，或兑换码无效、已使用、已过期、兑换过于频繁 |
| 401 | unauthorized | API Key 缺失、无效或已过期 |
| 403 | forbidden | 账户已被封禁 |
| 429 | rate_limit_exceeded | 请求过于频繁；用量记录查询限同一用户每秒 1 次 |
| 500 | internal_error | 服务内部错误 |

## 相关文档 {#related}

- [API 密钥](../%E8%AE%BF%E9%97%AE%E4%B8%8E%E8%AE%A4%E8%AF%81/API%20%E5%AF%86%E9%92%A5.md) — 创建和管理密钥
- [Agent 支付](Agent%20%E6%94%AF%E4%BB%98.md) — 使用 API Key 创建充值会话并查询支付状态
- [快速开始](../%E5%BF%AB%E9%80%9F%E5%85%A5%E9%97%A8/%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B.md) — 调用大模型
