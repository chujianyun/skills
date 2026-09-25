> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# CLI 工具

> 千问AI平台管理命令行工具，用于管理模型目录、账号、用量、账单、订阅和支持工单

> 版本 **1.4.0**

千问AI平台 CLI 已开源，欢迎查看源码、提交 Issue 或参与贡献：[GitHub](https://github.com/QianWen-AI/qianwen-cli)

## 快速开始

需要 Node.js 18 或更高版本。npm 包名及可安装版本以实际发布页为准。

1. 安装并验证：

```bash
npm install -g @qianwenai/qianwen-cli
qianwen version
```

2. 更新到最新版本（已安装用户）：

npm 用户直接运行以下命令即可更新到最新版：

```bash
npm install -g @qianwenai/qianwen-cli@latest
```

也可运行以下命令检查是否有新版本：

```bash
qianwen version --check
qianwen update
```

`update` 只检查并提示，不会自动安装，运行后按它输出的命令执行即可。刚完成第 1 步即为最新，可跳过本步。

3. 交互式登录：

```bash
qianwen auth login
```

4. 执行第一条查询：

```bash
qianwen models list
```

不带参数运行 `qianwen` 进入交互模式；带命令运行时执行一次后退出。

无需预设环境变量；登录流程会保存管理凭证。`models list` 返回结果即表示安装、网络与登录均可用。Agent 可运行 `qianwen config set output.format json` 固定 JSON 输出；验证失败时运行 `qianwen doctor --format json`。

## 模型与文档

> 想筛选可用模型、核对模型详情，或从官方文档找到接入说明？从这里开始。

### models list

列出可用模型，并按输入、输出模态筛选。

```text
qianwen models list [--input <text|image|video|audio|vector>] [--output <text|image|video|audio|vector>] [--page <integer>] [--per-page <integer>] [--all] [--verbose] [--format <auto|table|json|text>]
```

```bash
qianwen models list --input image --output text
qianwen models list --all --verbose --format json
```

| Flag                   | 类型 | 必填 | 默认    | 说明                                 |
| ---------------------- | -- | -- | ----- | ---------------------------------- |
| `--input <modality>`   | 枚举 | 否  | 未设置   | 输入模态：text、image、video、audio、vector |
| `--output <modality>`  | 枚举 | 否  | 未设置   | 输出模态：text、image、video、audio、vector |
| `--page <integer>`     | 整数 | 否  | 1     | 页码；非数字或小于 1 时回退 1                  |
| `--per-page <integer>` | 整数 | 否  | 20    | 每页模型数；非数字或 0 回退 20，负数归一为 1         |
| `--all`                | 布尔 | 否  | false | 返回全部模型并关闭分页；强制 JSON                |
| `--verbose`            | 布尔 | 否  | false | 补充详情字段；强制 JSON                     |

JSON 输出结构示例（示例值仅用于说明字段）：

```json
{
  "models": [
    {
      "id": "qwen3.6-plus",
      "modality": {
        "input": ["text", "image"],
        "output": ["text"]
      },
      "can_try": true,
      "free_tier": {
        "mode": "standard",
        "quota": {
          "remaining": 850000,
          "total": 1000000,
          "unit": "tokens",
          "used_pct": 15,
          "status": "valid",
          "resetDate": "2026-08-01T00:00:00.000Z"
        }
      },
      "pricing": {
        "tiers": [
          {
            "label": "输入<=256k",
            "input": 1.6,
            "output": 6.4,
            "cache_creation": 2,
            "cache_read": 0.16,
            "unit": "CNY/1M tokens"
          },
          {
            "label": "256k<输入<=1m",
            "input": 4.8,
            "output": 19.2,
            "cache_creation": 6,
            "cache_read": 0.48,
            "unit": "CNY/1M tokens"
          }
        ],
        "summary": {
          "cheapest_input": 1.6,
          "cheapest_output": 6.4,
          "unit": "CNY/1M tokens",
          "billing_type": "token"
        }
      },
      "features": ["function-calling"],
      "context": {
        "context_window": 131072,
        "max_input": 122880,
        "max_output": 8192
      }
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 20,
  "total_pages": 1
}
```

示例为默认（非 `--verbose`）分页场景：`features`、`context` 在列表接口返回时即出现，`--verbose` 另增 description、tags、rate\_limits、metadata；`free_tier` 恒为对象，无免费额度时其 `mode`/`quota` 为 null；`--all` 时顶层以 `all: true` 替代分页字段。

找到候选模型后，运行 `qianwen models info <id>` 查看完整定价、上下文和限流信息。

### models info

查看一个模型的完整详情；位置参数和 `--model` 至少提供一个。

```text
qianwen models info [id] [--model [id]] [--format <auto|table|json|text>]
```

```bash
qianwen models info qwen3.6-plus
qianwen models info --model qwen3.6-plus --format json
```

| Flag / 参数      | 类型  | 必填   | 默认 | 说明             |
| -------------- | --- | ---- | -- | -------------- |
| `[id]`         | 字符串 | 条件必填 | 无  | 模型 ID          |
| `--model [id]` | 字符串 | 条件必填 | 无  | 模型 ID；与位置参数二选一 |

需要继续比较候选模型时，运行 `qianwen models search <query>` 缩小范围。

### models search

按关键词或模态搜索模型。

```text
qianwen models search <query> [--page <integer>] [--per-page <integer>] [--all] [--format <auto|table|json|text>]
```

```bash
qianwen models search "function calling"
qianwen models search image --all --format json
```

| Flag / 参数              | 类型  | 必填 | 默认    | 说明              |
| ---------------------- | --- | -- | ----- | --------------- |
| `<query>`              | 字符串 | 是  | 无     | 搜索词             |
| `--page <integer>`     | 整数  | 否  | 1     | 页码              |
| `--per-page <integer>` | 整数  | 否  | 20    | 每页模型数           |
| `--all`                | 布尔  | 否  | false | 返回全部匹配项；强制 JSON |

### docs search

无需登录即可搜索官方文档，也可直接查看当前结果中的第 N 条。

```text
qianwen docs search <query> [--limit <integer>] [--page <integer>] [--language <en|zh>] [--view <integer>] [--format <auto|table|json|text>]
```

```bash
qianwen docs search "chat completions" --language zh --limit 10
qianwen docs search "API Key" --view 1
```

| Flag / 参数           | 类型  | 必填 | 默认  | 说明                                  |
| ------------------- | --- | -- | --- | ----------------------------------- |
| `<query>`           | 字符串 | 是  | 无   | 搜索词                                 |
| `--limit <integer>` | 整数  | 否  | 20  | JSON/text 每页 1-100 条；table 模式最多 5 条 |
| `--page <integer>`  | 整数  | 否  | 1   | 页码                                  |
| `--language <lang>` | 字符串 | 否  | zh  | 文档语言；en 映射 en，zh 开头映射 zh，其他值静默回退 zh |
| `--view <integer>`  | 整数  | 否  | 未设置 | 查看当前结果中从 1 开始的序号                    |

找到目标条目后，运行 `qianwen docs view <path-or-url>` 阅读正文。

### docs view

按文档路径或 URL 查看页面内容。

```text
qianwen docs view <path-or-url> [--format <auto|table|json|text>]
```

```bash
qianwen docs view /docs/model-api
```

| 参数              | 类型  | 必填 | 默认 | 说明        |
| --------------- | --- | -- | -- | --------- |
| `<path-or-url>` | 字符串 | 是  | 无  | 文档路径或 URL |

## 认证、账号与空间

> 想登录、确认凭证是否有效，或检查账号能访问哪些空间？用这组命令。

### auth login

登录并保存凭证；交互式终端优先 PKCE，非交互环境使用 Device Flow。

```text
qianwen auth login [--init-only] [--complete] [--timeout <seconds>] [--format <auto|table|json|text>]
```

```bash
qianwen auth login
qianwen auth login --init-only --format json
qianwen auth login --complete --timeout 180
```

| Flag                  | 类型 | 必填 | 默认    | 说明                   |
| --------------------- | -- | -- | ----- | -------------------- |
| `--init-only`         | 布尔 | 否  | false | 输出授权信息后立即退出          |
| `--complete`          | 布尔 | 否  | false | 继续并完成待处理的登录会话        |
| `--timeout <seconds>` | 整数 | 否  | 120   | `--complete` 的轮询超时秒数 |

非 TTY 且未指定 `--init-only`/`--complete` 时自动按 init-only 方式返回。凭证优先写入系统钥匙串，不可用时回退到加密文件。也可以直接运行 `qianwen login`。

登录成功后，运行 `qianwen auth status --format json` 检查凭证，再运行 `qianwen models list` 验证查询权限。

### auth status

检查本地凭证及服务端验证状态。

```text
qianwen auth status [--format <auto|table|json|text>]
```

```bash
qianwen auth status --format json
```

完整 JSON 结构示例：

```json
{
  "authenticated": true,
  "server_verified": true,
  "auth_mode": "device_flow",
  "source": "keychain",
  "user": {
    "aliyunId": "example-user"
  },
  "token": {
    "expires_at": "2026-08-01T00:00:00.000Z",
    "scopes": ["inference:read", "usage:read", "config:write"]
  }
}
```

服务端不可达但本地凭证仍有效时，`server_verified` 为 `false`，并可能带 `warning`。从 1.4.0 起，未登录或凭证过期也返回退出码 0；凭证过期时 JSON 还包含 `reason: "token_expired"`。

> 脚本迁移：不要再用 `auth status` 的退出码判断是否登录，请读取 JSON 中的 `authenticated` 字段。

若 `authenticated` 为 `false`，重新运行 `qianwen auth login`。

### auth logout

注销并删除本地凭证。也可以直接运行 `qianwen logout`。

```text
qianwen auth logout [--format <auto|table|json|text>]
```

```bash
qianwen auth logout
```

### workspace list

列出当前账号可访问的空间。

```text
qianwen workspace list [--format <auto|table|json|text>]
```

```bash
qianwen workspace list --format json
```

列出空间后，运行 `qianwen workspace limit` 判断账号是否还能新增空间。

### workspace limit

查看已用空间数与账号硬上限。

```text
qianwen workspace limit [--format <auto|table|json|text>]
```

```bash
qianwen workspace limit
```

## 用量、账单与订阅

> 想知道本月用了多少、花了多少、哪个模型或 API Key 成本最高，或订阅额度还剩多少？用这组命令。

日期选项以各命令表为准：`usage summary` 的日期只作用于 PAYG，`usage free-tier` 当前仅返回快照；其余相关查询按 `--from/--to` > `--days` > `--period` > 本月至今解析。常用 `--period` 值包括 `today`、`yesterday`、`week`、`month`、`last-month`、`quarter`、`year` 和 `YYYY-MM`。

金额不再固定舍入为四位小数；JSON 中 `cost` 仍为 number。

### usage summary

汇总免费额度、Token Plan 与按量付费用量。

```text
qianwen usage summary [--from <date>] [--to <date>] [--period <preset>] [--format <auto|table|json|text>]
```

```bash
qianwen usage summary --period month
qianwen usage summary --from 2026-07-01 --to 2026-07-21 --format json
```

| Flag                | 类型  | 必填 | 默认    | 说明                   |
| ------------------- | --- | -- | ----- | -------------------- |
| `--from <date>`     | 日期  | 否  | 当月首日  | PAYG 开始日期，YYYY-MM-DD |
| `--to <date>`       | 日期  | 否  | 今天    | PAYG 结束日期，YYYY-MM-DD |
| `--period <preset>` | 字符串 | 否  | month | PAYG 预设区间或 YYYY-MM   |

日期参数及 JSON 顶层 `period` 仅界定 `pay_as_you_go`；`free_tier` 与 `token_plan` 为查询时的当前快照。

JSON 输出结构示例（已订阅场景；示例值仅用于说明字段）：

```json
{
  "period": {
    "from": "2026-07-01",
    "to": "2026-07-21"
  },
  "free_tier": [
    {
      "model_id": "qwen-plus",
      "quota": {
        "remaining": 850000,
        "total": 1000000,
        "unit": "tokens",
        "used_pct": 15,
        "status": "valid",
        "resetDate": "2026-08-01T00:00:00.000Z"
      }
    }
  ],
  "token_plan": {
    "subscribed": true,
    "planName": "Token Plan",
    "status": "valid",
    "totalCredits": 25000,
    "remainingCredits": 18000,
    "usedPct": 28,
    "resetDate": "2026-08-01T00:00:00.000Z"
  },
  "pay_as_you_go": {
    "models": [
      {
        "model_id": "qwen-plus",
        "usage": {
          "tokens": 600000
        },
        "cost": 0.38,
        "currency": "CNY"
      }
    ],
    "total": {
      "cost": 0.38,
      "currency": "CNY"
    }
  }
}
```

模型无免费额度时 `free_tier[].quota` 为 null；`token_plan` 仅 `subscribed` 必有，其余字段按数据条件出现；`pay_as_you_go` 的计量字段随模型计费方式变化。

发现某个模型用量异常时，运行 `qianwen usage breakdown --model <id>`；需要查看请求级原因时，继续用 `qianwen usage logs`。

### usage breakdown

查看指定模型按日、月或季度拆分的按量付费用量。

```text
qianwen usage breakdown --model <id> [--granularity <day|month|quarter>] [--from <date>] [--to <date>] [--period <preset>] [--days <number>] [--format <auto|table|json|text>]
```

```bash
qianwen usage breakdown --model qwen-plus --days 7
qianwen usage breakdown --model qwen-plus --granularity month --period quarter
```

| Flag                | 类型  | 必填 | 默认    | 说明                          |
| ------------------- | --- | -- | ----- | --------------------------- |
| `--model <id>`      | 字符串 | 是  | 无     | 模型 ID；运行时校验                 |
| `--granularity <g>` | 枚举  | 否  | day   | day、month、quarter           |
| `--from <date>`     | 日期  | 否  | 未设置   | 开始日期                        |
| `--to <date>`       | 日期  | 否  | 未设置   | 结束日期                        |
| `--period <preset>` | 字符串 | 否  | month | 预设区间                        |
| `--days <number>`   | 数值  | 否  | 未设置   | 向前回看天数；请传正整数，CLI 当前未严格校验整数性 |

### usage free-tier

浏览全部模型的当前免费额度状态。

```text
qianwen usage free-tier [--from <date>] [--to <date>] [--period <preset>] [--format <auto|table|json|text>]
```

```bash
qianwen usage free-tier --format json
```

| Flag                | 类型  | 必填 | 默认  | 说明               |
| ------------------- | --- | -- | --- | ---------------- |
| `--from <date>`     | 日期  | 否  | 未设置 | 已注册；当前不影响返回的额度快照 |
| `--to <date>`       | 日期  | 否  | 未设置 | 已注册；当前不影响返回的额度快照 |
| `--period <preset>` | 字符串 | 否  | 未设置 | 已注册；当前不影响返回的额度快照 |

该命令始终返回当前免费额度快照；日期 Flag 当前不会筛选历史额度。

### usage payg

浏览全部模型的按量付费用量。

```text
qianwen usage payg [--from <date>] [--to <date>] [--period <preset>] [--days <number>] [--format <auto|table|json|text>]
```

```bash
qianwen usage payg --period last-month
qianwen usage payg --days 30 --format json
```

| Flag                | 类型  | 必填 | 默认    | 说明                          |
| ------------------- | --- | -- | ----- | --------------------------- |
| `--from <date>`     | 日期  | 否  | 未设置   | 开始日期                        |
| `--to <date>`       | 日期  | 否  | 未设置   | 结束日期                        |
| `--period <preset>` | 字符串 | 否  | month | 预设区间                        |
| `--days <number>`   | 数值  | 否  | 未设置   | 向前回看天数；请传正整数，CLI 当前未严格校验整数性 |

### usage logs

按时间、模型、状态或请求 ID 查询调用日志。

```text
qianwen usage logs [--from <date-or-rfc3339>] [--to <date-or-rfc3339>] [--period <preset>] [--model <id>]... [--status <type>]... [--request-id <id>] [--page <integer>] [--page-size <integer>] [--format <auto|table|json|text>]
```

```bash
qianwen usage logs --period 24h --status 4xx --status 5xx
qianwen usage logs --request-id 12345-abcdef --format json
```

| Flag                    | 类型     | 必填 | 默认         | 说明                                                                   |
| ----------------------- | ------ | -- | ---------- | -------------------------------------------------------------------- |
| `--from <value>`        | 日期/时间  | 否  | 7 天前 00:00 | YYYY-MM-DD 或 RFC3339                                                 |
| `--to <value>`          | 日期/时间  | 否  | 当前时间       | YYYY-MM-DD 或 RFC3339                                                 |
| `--period <preset>`     | 字符串    | 否  | 未设置        | 支持 `1h`、`24h`、`7d` 及日期预设                                             |
| `--model <id>`          | 可重复字符串 | 否  | 未设置        | 模型过滤，可重复                                                             |
| `--status <type>`       | 可重复字符串 | 否  | 未设置        | 支持 0/cancel、2xx/success、4xx/client-error、5xx/server-error 及别名；未知值被忽略 |
| `--request-id <id>`     | 字符串    | 否  | 未设置        | 精确请求 ID；设置后忽略其他过滤项                                                   |
| `--page <integer>`      | 整数     | 否  | 1          | 页码                                                                   |
| `--page-size <integer>` | 整数     | 否  | 20         | 每页 1-100 条                                                           |

单次时间跨度最多 14 天。

### billing summary

按结算月份汇总账单金额。

```text
qianwen billing summary [--from <yyyy-mm>] [--to <yyyy-mm>] [--charge-type <all|subscription|payg>] [--format <auto|table|json|text>]
```

```bash
qianwen billing summary --from 2026-06 --to 2026-07
```

| Flag                   | 类型 | 必填 | 默认  | 说明                    |
| ---------------------- | -- | -- | --- | --------------------- |
| `--from <yyyy-mm>`     | 月份 | 否  | 当前月 | 起始结算月                 |
| `--to <yyyy-mm>`       | 月份 | 否  | 当前月 | 结束结算月，含当月             |
| `--charge-type <type>` | 枚举 | 否  | all | all、subscription、payg |

`--from` 和 `--to` 必须使用 `YYYY-MM`，月份范围为 01-12；非法值返回退出码 4，错误 `code` 为 `INVALID_ARGUMENT`。区间内缺少账单记录的月份仍会补齐：table/text 显示 `No bill`，JSON 补齐项使用账期 `YYYYMM`、`aftertaxAmount: null` 和 `settled: false`；真实零元账单保留非 null 的金额字符串，并使用 `settled: true`。`totals` 只汇总 `settled: true` 的月份。

需要定位费用来源时，运行 `qianwen billing breakdown --group-by model` 或 `--group-by api-key`。

### billing breakdown

按模型或 API Key 拆分消费。

```text
qianwen billing breakdown [--granularity <day|month>] [--group-by <model|api-key>] [--from <date>] [--to <date>] [--period <preset>] [--charge-type <all|subscription|payg>] [--top <integer>] [--format <auto|table|json|text>]
```

```bash
qianwen billing breakdown --group-by api-key --top 20
qianwen billing breakdown --granularity day --period week
```

| Flag                   | 类型             | 必填 | 默认    | 说明                                                                                |
| ---------------------- | -------------- | -- | ----- | --------------------------------------------------------------------------------- |
| `--granularity <g>`    | 字符串（day/month） | 否  | month | day 或 month；其他值静默回退为 month                                                        |
| `--group-by <dim>`     | 枚举             | 否  | model | model 或 api-key                                                                   |
| `--from <date>`        | 日期/月           | 否  | 当前月   | day 使用 YYYY-MM-DD；month 可用 YYYY-MM                                                |
| `--to <date>`          | 日期/月           | 否  | 当前月   | 结束日期或月份                                                                           |
| `--period <preset>`    | 字符串            | 否  | 未设置   | today、yesterday、week、this-week、month、this-month、last-month、quarter、year 或 YYYY-MM |
| `--charge-type <type>` | 枚举             | 否  | all   | all、subscription、payg                                                             |
| `--top <integer>`      | 整数             | 否  | 10    | 返回前 N 项；仅数字小于 1 或大于 20 时报错退出 4。非数字输入回退默认 10，非整数取整数部分，均不报错                         |

day 粒度下起止日期相差不超过 31 天，month 粒度下起止月份相差不超过 12 个月（含首尾最多覆盖 32 个自然日或 13 个账期月）；day 跨度超限返回退出码 4，month 跨度超限返回退出码 1。

周期按名称分类：`today`、`yesterday`、`week`、`this-week` 为短周期；`month`、`this-month`、`last-month`、`quarter`、`year` 为长周期。自定义 `YYYY-MM` 按实际跨度判断，完整自然月归为短周期。仅传 `--period` 且未显式指定粒度时，短周期自动使用 day，长周期使用 month；短周期配 month 或长周期配 day 时返回退出码 4，错误 `code` 为 `INVALID_ARGUMENT`。

`--top` 超出 1-20 或 `--period` 不在上述范围时返回退出码 4，错误 `code` 为 `INVALID_ARGUMENT`。Top N 行合计小于权威总额时，CLI 会追加 `UNLISTED` / `Unlisted` 差额行；该行不计入 N 或 `totalRows`，每个周期最多返回 N+1 行。

### billing limit

查看消费上限和告警配置。

```text
qianwen billing limit [--format <auto|table|json|text>]
```

```bash
qianwen billing limit --format json
```

### billing balance summary

查看账号可用余额。

```text
qianwen billing balance summary [--format <auto|table|json|text>]
```

```bash
qianwen billing balance summary
```

余额不足时，运行 `qianwen billing balance recharge` 打开充值页。

### billing balance recharge

打开充值页面；浏览器无法自动打开时仍输出链接。

```text
qianwen billing balance recharge [--format <auto|table|json|text>]
```

```bash
qianwen billing balance recharge
```

JSON 中的 `opened` 反映浏览器启动是否成功；无法自动打开时仍返回充值链接。

### subscription status

汇总订阅状态；仅支持 Token Plan。

```text
qianwen subscription status [--plan <token>] [--format <auto|table|json|text>]
```

```bash
qianwen subscription status --plan token --format json
```

| Flag             | 类型         | 必填 | 默认      | 说明                      |
| ---------------- | ---------- | -- | ------- | ----------------------- |
| `--plan <token>` | 字符串（token） | 否  | 全部支持的计划 | 仅识别 token；其他值按未设置处理，不报错 |

使用团队 Token Plan 时，运行 `qianwen subscription tokenplan seats --format json` 查看席位实例。

### subscription orders

列出订阅的购买、续费和升级订单。

```text
qianwen subscription orders [--from <date>] [--to <date>] [--type <purchase|renew|upgrade>] [--page <integer>] [--page-size <integer>] [--format <auto|table|json|text>]
```

```bash
qianwen subscription orders --type purchase --page 1 --page-size 20
```

| Flag                    | 类型  | 必填 | 默认  | 说明                                      |
| ----------------------- | --- | -- | --- | --------------------------------------- |
| `--from <date>`         | 日期  | 否  | 未设置 | 开始日期，YYYY-MM-DD                         |
| `--to <date>`           | 日期  | 否  | 未设置 | 结束日期，YYYY-MM-DD                         |
| `--type <kind>`         | 字符串 | 否  | 未设置 | 识别 purchase、renew、upgrade；其他值按未设置处理，不报错 |
| `--page <integer>`      | 整数  | 否  | 1   | 页码                                      |
| `--page-size <integer>` | 整数  | 否  | 20  | 每页 1-100 条；超过 100 返回退出码 4               |

`--from`/`--to` 不做本地严格校验；无法解析的值会被忽略，对应过滤可能不生效。

### subscription tokenplan status

查看 Token Plan 席位类型、周期、续费状态与诊断信息。

```text
qianwen subscription tokenplan status [--format <auto|table|json|text>]
```

```bash
qianwen subscription tokenplan status --format json
```

自动续费明确关闭时，`seatSummary.groups[].nextCycleFlushTime` 为 `null`。

### subscription tokenplan seats

分页列出 Token Plan 席位实例。

```text
qianwen subscription tokenplan seats [--spec-type <pro|standard>] [--page <integer>] [--page-size <integer>] [--format <auto|table|json|text>]
```

```bash
qianwen subscription tokenplan seats --spec-type pro --format json
```

| Flag                    | 类型 | 必填 | 默认  | 说明                                |
| ----------------------- | -- | -- | --- | --------------------------------- |
| `--spec-type <type>`    | 枚举 | 否  | 未设置 | pro 或 standard（不区分大小写）；其他值返回退出码 4 |
| `--page <integer>`      | 整数 | 否  | 1   | 页码                                |
| `--page-size <integer>` | 整数 | 否  | 20  | 每页最多 100 条                        |

该命令未显式指定格式时默认使用 table；Agent 应显式传 `--format json`。

## 配置、诊断与补全

> 想固定机器可读输出、排查本地环境、启用 Shell 补全或确认版本？用这组命令。

### config list

列出用户可配置项；1.4.0 公开键仅有 `output.format`。

```text
qianwen config list [--format <auto|table|json|text>]
```

```bash
qianwen config list --format json
```

### config get

读取一个配置值。

```text
qianwen config get <key> [--format <auto|table|json|text>]
```

```bash
qianwen config get output.format
```

### config set

设置一个配置值。

```text
qianwen config set <key> <value> [--format <auto|table|json|text>]
```

```bash
qianwen config set output.format json
```

`output.format` 可取 `auto`、`table`、`json`、`text`。

设置后运行 `qianwen config get output.format` 确认生效。

### config unset

删除配置值并恢复默认行为。

```text
qianwen config unset <key> [--format <auto|table|json|text>]
```

```bash
qianwen config unset output.format
```

### doctor

检查版本、认证、Token、网络、Shell 补全和全局配置。

```text
qianwen doctor [--format <auto|table|json|text>]
```

```bash
qianwen doctor --format json
```

按诊断结果修复后重新运行 `qianwen doctor`，直到失败项消失。

### completion install

为当前或指定 Shell 安装命令补全。

```text
qianwen completion install [--shell <bash|zsh|fish>]
```

```bash
qianwen completion install --shell zsh
```

### completion generate

输出当前或指定 Shell 的补全脚本。

```text
qianwen completion generate [--shell <bash|zsh|fish>]
```

```bash
qianwen completion generate --shell bash
```

`--shell` 省略时自动检测，支持 bash、zsh、fish。

### version

输出版本；`--check` 同时检查新版本。

```text
qianwen version [--check]
```

```bash
qianwen version --check
```

## 技能市场

> 想从技能市场查找 Agent Skills，并安装到当前项目或本机 Agent 的技能目录？从这里开始。

这组命令无需登录。搜索不会修改本地文件；新装或更新时下载技能包并校验 SHA256，并只管理带有效 CLI 元数据的同名目录。

### skills search

按关键词搜索技能市场；query 可省略，精确且大小写一致的 slug 会排在结果首位。

```text
qianwen skills search [query] [--limit <integer>] [--format <auto|table|json|text>]
```

```bash
qianwen skills search qianwen --limit 10
qianwen skills search 文本生成
qianwen skills search qianwen-text --format json
```

| Flag / 参数           | 类型  | 必填 | 默认   | 说明                            |
| ------------------- | --- | -- | ---- | ----------------------------- |
| `[query]`           | 字符串 | 否  | 空字符串 | 搜索词，可为中文或英文，支持模糊匹配；省略时按空字符串搜索 |
| `--limit <integer>` | 整数  | 否  | 5    | 最多返回条数，接受 1-50 的整数            |

table 模式使用可滚动的交互表格；text 和 JSON 适合非交互环境。

JSON 输出结构示例（示例值仅用于说明字段）：

```json
{
  "query": "qianwen-text",
  "results": [
    {
      "slug": "qianwen-text",
      "name": "千问-文本生成",
      "description": "技能说明",
      "publisher": "千问AI平台",
      "currentVersion": "0.0.1",
      "verified": true
    }
  ]
}
```

`currentVersion` 在平台未返回版本时省略。`--limit` 不是整数或超出 1-50 时返回退出码 1，错误 `code` 为 `INVALID_ARGUMENT`；网络、平台及服务端错误（含技能不存在、限流）均归一为退出码 3。没有匹配项时返回空的 `results` 数组并退出 0。

找到 slug 后，运行 `qianwen skills install <slug>` 安装技能。

### skills install

下载并安装一个技能；slug 只能包含字母、数字、连字符或下划线，长度 1-64，首尾必须是字母或数字。

```text
qianwen skills install <slug> [--dir <directory>] [--format <auto|table|json|text>]
```

```bash
qianwen skills install qianwen-text
qianwen skills install qianwen-text --dir . --format json
```

| Flag / 参数           | 类型  | 必填 | 默认   | 说明                                           |
| ------------------- | --- | -- | ---- | -------------------------------------------- |
| `<slug>`            | 字符串 | 是  | 无    | 技能 slug                                      |
| `--dir <directory>` | 路径  | 否  | 当前目录 | 安装基目录；显式指定时必须已存在且可写，目标为 `<directory>/<slug>` |

table 模式下，未传 `--dir` 且当前目录不是已知 Agent 技能目录时出现选择界面：←/→ 在"继续当前目录"与"选择目标 Agent"之间切换（Enter 确认、Esc 取消）；选择 Agent 后用 ↑/↓ 在其列表中导航（Esc 返回上一层），安装到该 Agent 相对当前工作目录的技能目录。选择界面不接受手动输入路径；要指定其他目录，用 `--dir` 重跑。JSON/text 模式不显示选择界面，默认安装到当前目录下。

JSON 输出结构示例（示例值仅用于说明字段）：

```json
{
  "slug": "qianwen-text",
  "version": "0.0.1",
  "outcome": "updated",
  "targetDir": "/path/to/project/.claude/skills/qianwen-text",
  "security": "安全",
  "sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
  "downgrade": {
    "from": "0.0.2",
    "to": "0.0.1"
  }
}
```

`targetDir` 为实际安装目录：默认当前目录，table 模式选择 Agent 后为该 Agent 相对当前工作目录的技能目录，传 `--dir` 时为指定目录，末尾均为 `/<slug>`。`outcome` 为 `installed`、`updated` 或 `noop`；`noop` 表示同版本已安装，不写入文件。只有检测到降级更新时才出现 `downgrade`，CLI 同时给出警告；`security` 显示平台安全状态。下载包必须通过平台声明值与本地计算值的 SHA256 比对。目标同名目录没有有效 CLI 元数据时返回 `UNMANAGED_CONFLICT`，不会覆盖或修改该目录。

slug 格式不合法返回 `INVALID_ARGUMENT`（以 `-` 开头的输入会被当作未知选项，返回 `UNKNOWN_OPTION`，同样退出 1）；目录不存在或不是目录返回 `INSTALL_DIR_NOT_FOUND`；目录不可写返回 `INSTALL_DIR_NOT_WRITABLE`。这三类本地校验均退出 1，错误写入 stderr，且在此之前不发出任何网络请求。技能包下载、SHA256 校验或安装失败退出 1；技能市场接口（搜索、详情、下载链接）的网络、平台及服务端错误（含技能不存在、限流）均归一为退出码 3。

## 支持与更新

> 想提交并跟进问题、关闭或评价工单，或检查 CLI 更新？从这里选择动作。

### support list

分页列出支持工单。

```text
qianwen support list [--page <integer>] [--page-size <integer>] [--format <auto|table|json|text>]
```

```bash
qianwen support list --page 1 --page-size 10
```

| Flag                    | 类型 | 必填 | 默认 | 说明        |
| ----------------------- | -- | -- | -- | --------- |
| `--page <integer>`      | 整数 | 否  | 1  | 页码        |
| `--page-size <integer>` | 整数 | 否  | 10 | 每页 1-10 条 |

### support view

查看工单详情和消息记录。

```text
qianwen support view <ticket-id> [--format <auto|table|json|text>]
```

```bash
qianwen support view TICKET_ID --format json
```

### support create

交互式创建工单，或用成对参数进行非交互创建。

```text
qianwen support create [--list-categories] [--category-id <id>] [--description <text>] [--accept-language <zh_CN|en_US>] [--format <auto|table|json|text>]
```

```bash
qianwen support create --list-categories
qianwen support create --category-id CATEGORY_ID --description "问题描述" --accept-language zh_CN
```

| Flag                       | 类型  | 必填      | 默认     | 说明                         |
| -------------------------- | --- | ------- | ------ | -------------------------- |
| `--list-categories`        | 布尔  | 否       | false  | 列出分类后退出                    |
| `--category-id <id>`       | 字符串 | 非交互条件必填 | 无      | 与 `--description` 同时提供     |
| `--description <text>`     | 字符串 | 非交互条件必填 | 无      | 最长 2000 字符，超长截断            |
| `--accept-language <lang>` | 枚举  | 否       | zh\_CN | 工单语言：zh\_CN 或 en\_US；区分大小写 |

仅给 `--category-id`/`--description` 之一返回退出码 1；两者均未提供且非 TTY 返回退出码 4。

`--accept-language` 使用其他值时返回退出码 1，错误 `code` 为 `INVALID_ARGUMENT`。

创建成功后保存返回的工单 ID，并运行 `qianwen support view <ticket-id>` 跟进处理记录。

### support reply

回复工单；非交互环境必须提供消息正文。

```text
qianwen support reply <ticket-id> [--message <text>] [--format <auto|table|json|text>]
```

```bash
qianwen support reply TICKET_ID --message "请检查日志"
```

| Flag / 参数          | 类型  | 必填    | 默认 | 说明              |
| ------------------ | --- | ----- | -- | --------------- |
| `<ticket-id>`      | 字符串 | 是     | 无  | 工单 ID           |
| `--message <text>` | 字符串 | 非交互必填 | 无  | 最长 2000 字符，超长截断 |

非交互缺少 `--message` 返回退出码 4。

### support close

关闭工单；脚本中必须用 `--yes` 跳过确认。

```text
qianwen support close <ticket-id> [--yes] [--format <auto|table|json|text>]
```

```bash
qianwen support close TICKET_ID --yes
```

| Flag / 参数     | 类型  | 必填    | 默认    | 说明    |
| ------------- | --- | ----- | ----- | ----- |
| `<ticket-id>` | 字符串 | 是     | 无     | 工单 ID |
| `--yes`       | 布尔  | 非交互必填 | false | 跳过确认  |

非交互缺少 `--yes` 返回退出码 4。

### support rate

对已解决工单评分；评分范围为 0-2。

```text
qianwen support rate <ticket-id> [--rating <0|1|2>] [--comment <text>] [--format <auto|table|json|text>]
```

```bash
qianwen support rate TICKET_ID --rating 2 --comment "满意"
```

| Flag / 参数          | 类型  | 必填    | 默认  | 说明              |
| ------------------ | --- | ----- | --- | --------------- |
| `<ticket-id>`      | 字符串 | 是     | 无   | 工单 ID           |
| `--rating <n>`     | 整数  | 非交互必填 | 无   | 0=不满意，1=一般，2=满意 |
| `--comment <text>` | 字符串 | 否     | 未设置 | 最长 500 字符，超长截断  |

非交互缺少 `--rating`、非整数或越界均返回退出码 1，`code` 为 `INVALID_ARGUMENT`。

### update

检查版本并输出升级提示，不直接安装。版本比对来自 GitHub Releases；检测到新版本时按安装渠道输出升级命令：Node.js 安装按模块路径提示 npm、pnpm 或 Bun，Bun 单文件版本按平台提示运行 `install.sh` 或 `install.ps1`。检查请求失败或新版本尚未发布时按已是最新处理、不提示，核对版本以发布页为准。

```text
qianwen update
```

```bash
qianwen update
```

## 全局约定

```text
qianwen [--format <auto|table|json|text>] [--quiet] <area> <verb> [args] [flags]
```

| 全局 Flag          | 类型 | 默认    | 说明                             |
| ---------------- | -- | ----- | ------------------------------ |
| `--format <fmt>` | 枚举 | auto  | 显式格式优先于 `config output.format` |
| `-q, --quiet`    | 布尔 | false | 静默 stdout/stderr，仅以退出码表示结果     |
| `-v, --version`  | 布尔 | false | 顶层版本快捷项                        |
| `-h, --help`     | 布尔 | false | 顶层及各级命令帮助                      |

`auto` 在 TTY 使用 table，在 pipe/重定向中使用 JSON；非 TTY 显式请求 table 时降级为 text 并在 stderr 提示。成功数据写 stdout，错误和诊断写 stderr。JSON 结构由各命令定义，不提供统一外层 envelope；`CliError` 的退出码字段为 `exit_code`，Commander 参数错误仍可能使用 `exitCode`。

分页查询中，JSON 通常保留请求页并在越界时返回空数组；交互表格通常调整到有效页。Agent 应显式指定 `--format json`、页码和每页数量。

| 退出码 | 含义                               |
| --- | -------------------------------- |
| 0   | 成功                               |
| 1   | 通用错误；Commander 参数解析错误也使用 1       |
| 2   | 认证失败（`docs search` 空查询也退出 2）     |
| 3   | 网络错误                             |
| 4   | 配置或参数错误                          |
| 5   | 限流                               |
| 6   | 服务端错误                            |
| 7   | 资源未找到                            |
| 8   | 操作未完成的保留码                        |
| 10  | `docs view` 文档未找到或内容获取失败（超时退出 3） |
| 130 | 用户中断                             |

本地校验的退出码尚未完全统一：`billing summary` 的月份格式、`billing breakdown` 的周期/粒度冲突/top 越界、`usage logs` 的周期或跨度错误、`subscription orders` 的 --page-size 超限、`subscription tokenplan seats` 的 --spec-type 非法、`support reply/close` 非交互缺必填参数、`support create` 缺成对参数且非 TTY，返回 4，错误 `code` 为 `INVALID_ARGUMENT`；`skills search --limit` 的非法值或 `skills install` 的 slug 格式错误返回 1，错误 `code` 为 `INVALID_ARGUMENT`，目录错误返回 1，错误 `code` 为 `INSTALL_DIR_NOT_FOUND` 或 `INSTALL_DIR_NOT_WRITABLE`；`support create --accept-language` 非法值返回 1，错误 `code` 为 `INVALID_ARGUMENT`；`docs search ""` 返回纯文本错误并退出 2，不含 JSON `code`。脚本应先以 0/非 0 判断命令是否成功，再结合 JSON 错误对象中的 `code` 分流。`auth status` 是例外：未登录或凭证过期也退出 0，必须读取 `authenticated`。`skills` 两命令将技能市场接口错误（含技能不存在、限流）归一为退出码 3，不沿用表中 5/6/7；技能包下载失败仍为 1。

## 附录

### 命令速查表

| 命令                                      | 用途                 |
| --------------------------------------- | ------------------ |
| `qianwen auth login`                    | 获取并保存管理凭证          |
| `qianwen auth logout`                   | 删除本地凭证并注销          |
| `qianwen auth status`                   | 检查凭证与服务端验证状态       |
| `qianwen models list`                   | 筛选可用模型             |
| `qianwen models info`                   | 查看单模型完整详情          |
| `qianwen models search`                 | 按关键词或模态找模型         |
| `qianwen usage summary`                 | 汇总各计费方式用量          |
| `qianwen usage breakdown`               | 拆分指定模型用量           |
| `qianwen usage free-tier`               | 检查免费额度余额           |
| `qianwen usage payg`                    | 查看按量付费用量与成本        |
| `qianwen usage logs`                    | 按请求或状态查调用日志        |
| `qianwen billing limit`                 | 检查消费上限与告警          |
| `qianwen billing breakdown`             | 按模型或 API Key 拆账    |
| `qianwen billing summary`               | 查看月度结算总额           |
| `qianwen billing balance summary`       | 检查账号可用余额           |
| `qianwen billing balance recharge`      | 打开充值页面             |
| `qianwen subscription status`           | 确认 Token Plan 订阅状态 |
| `qianwen subscription orders`           | 查购买、续费和升级订单        |
| `qianwen subscription tokenplan status` | 查周期与续费状态           |
| `qianwen subscription tokenplan seats`  | 逐页查看席位实例           |
| `qianwen workspace list`                | 列出可访问空间            |
| `qianwen workspace limit`               | 检查空间数量上限           |
| `qianwen support list`                  | 分页查工单              |
| `qianwen support view`                  | 查看工单与消息记录          |
| `qianwen support create`                | 提交新工单              |
| `qianwen support reply`                 | 向工单追加消息            |
| `qianwen support close`                 | 关闭工单请求             |
| `qianwen support rate`                  | 评价已解决工单            |
| `qianwen docs search`                   | 按关键词找官方文档          |
| `qianwen docs view`                     | 打开文档正文             |
| `qianwen config list`                   | 查看公开配置项            |
| `qianwen config get`                    | 读取单项配置             |
| `qianwen config set`                    | 设置默认输出格式           |
| `qianwen config unset`                  | 恢复配置默认值            |
| `qianwen doctor`                        | 定位版本、认证或网络问题       |
| `qianwen completion install`            | 启用 Shell 补全        |
| `qianwen completion generate`           | 导出 Shell 补全脚本      |
| `qianwen version`                       | 查看版本并检查更新          |
| `qianwen update`                        | 获取升级提示             |
| `qianwen skills search`                 | 搜索技能市场技能           |
| `qianwen skills install`                | 下载并安装技能市场技能        |
