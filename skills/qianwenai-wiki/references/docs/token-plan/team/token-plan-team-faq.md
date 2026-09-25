> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 常见问题

> Token Plan 团队版常见问题汇总，涵盖购买、使用、计量和性能相关的问题解答。

## 产品定位与套餐选择

### 个人版和团队版有什么区别？我该买哪个？

| 维度    | 个人版            | 团队版              |
| ----- | -------------- | ---------------- |
| 适用场景  | 个人开发者、日常 AI 编程 | 团队协作、统一管理席位和用量   |
| 额度机制  | 7 天窗口限额        | 月度总额度，无窗口限制      |
| 团队管理  | 不支持            | 支持席位分配、成员管理、用量分析 |
| 数据安全  | 数据用于服务改进与模型优化  | 承诺不使用对话数据训练模型    |
| 高峰期性能 | 高峰期可能排队        | 多租户隔离架构，不排队      |

个人开发者、日常使用 AI 编程工具，选择个人版即可；团队需要多人协作、统一管理席位和用量、对数据安全有更高要求，选择团队版。

### 个人版和团队版能同时买吗？额度是分开算的还是共享的？

可以同时购买。同一千问AI平台账号可以同时持有个人版和团队版，各自独立计费，额度不共享。

### 已有个人版，再买团队版会冲突吗？

不冲突。两者可以同时持有，各自独立计费。使用时根据 API Key 自动匹配对应套餐。

### 支持 Cursor / Claude Code / Cline 等第三方工具吗？

Token Plan 兼容 OpenAI 和 Anthropic 协议，任何支持自定义 Base URL 和 API Key 的工具均可接入，包括 Cursor、Claude Code、Qwen Code、Qoder、Qoder CN、Cline、OpenClaw、Cherry Studio、Chatbox 等。

## 接入与调用

### 如何在编程工具中使用图像生成模型？

图像生成模型使用独立的接口，无法通过文本模型的 Base URL 直接调用。需要通过工具的 Skill 或扩展机制接入，具体配置方法请参见[接入多模态生成模型](/token-plan/best-practices/multimodal-generation)。

### 常见报错及解决方案

| 报错信息                                                                                                                    | 可能原因                                                                         | 解决方案                                                                                                                                                             |
| ----------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **401 InvalidApiKey: No API-key provided.**                                                                             | 请求头中未携带 API Key（`Authorization: Bearer` 或 `x-api-key` 均未传）。                  | 在管理后台生成 API Key，并在工具中完成配置。                                                                                                                                       |
| **401 InvalidApiKey: Invalid API-key provided.**                                                                        | 误用了千问AI平台通用 API Key（sk-ws-xxx 格式，早期创建的 Key 为 sk-xxx）；订阅过期；API Key 复制不完整或包含空格 | 确认使用的是 Token Plan 专属 API Key，确保完整且无空格。确认订阅是否过期。如仍报错，重置 API Key 后使用新 Key 配置。                                                                                      |
| **404 model 'xxx' not found or not supported** / **400 Model not exist.**                                               | 模型名称拼写错误或大小写错误；模型 ID 不在套餐支持列表中                                               | 确认模型名称区分大小写，与套餐支持的模型 ID 一致。检查所选套餐是否包含该模型。                                                                                                                        |
| **401 invalid access token or token expired**                                                                           | 误用了其他套餐的 Base URL                                                            | Anthropic 兼容端点：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`；OpenAI 兼容端点：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| **401 Incorrect API key provided**                                                                                      | 误用了千问AI平台通用 Base URL（dashscope.aliyuncs.com）                                 | Anthropic 兼容端点：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`；OpenAI 兼容端点：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| **400 InvalidParameter: Range of input length should be \[1, xxx]**                                                     | 输入内容（含对话历史、代码上下文等）超出模型的最大上下文长度                                               | 新建会话清空历史，或使用工具自带的上下文压缩命令（如 Claude Code 的 `/compact`、Qwen Code 的 `/clear`）。也可切换上下文窗口更大的模型。                                                                        |
| **400 InvalidParameter: url error, please check url!**                                                                  | Base URL 路径与协议不匹配（如把 OpenAI 兼容路径配在 Anthropic 端点上）                            | Anthropic 兼容协议（Claude Code 等）以 `/apps/anthropic` 结尾；OpenAI 兼容协议（Cursor、Qwen Code 等）以 `/compatible-mode/v1` 结尾。                                                   |
| **400 InvalidParameter: Range of max\_tokens should be \[1, xxxx]**                                                     | `max_tokens` 超出当前模型支持的最大输出 Token 数                                           | 将 `max_tokens` 调整为不超过报错信息中提示的上限值。                                                                                                                                |
| **400 invalid\_parameter\_error: The thinking\_budget parameter must be a positive integer and not greater than xxxxx** | 思维链长度（`thinking_budget`、`budgetTokens`）超过当前模型上限                              | 将思维链长度调整为不超过报错提示的上限值，或在不支持思考模式的模型上移除该配置项。                                                                                                                        |
| **400 data\_inspection\_failed**                                                                                        | 输入或输出命中平台内容安全策略                                                              | 修改输入内容后重新提交。如多次触发，调整提示词避免敏感话题。                                                                                                                                   |
| **429 API-Key Requests rate limit exceeded**                                                                            | 短时间内请求过于密集，触发模型调用限流                                                          | 等待一分钟后重试；如频繁触发请降低请求频率，并确认 API Key 未被他人共享使用。                                                                                                                      |
| **429 Throttling.AllocationQuota / insufficient\_quota**                                                                | **套餐额度已用尽**：席位额度和加油包均已耗尽。或**触发模型调用限流**：TPS/TPM 超过模型限流阈值，限流按主账号维度计算。          | **额度已用尽**：增购席位、购买加油包，或等待下一计费周期额度自动重置。**触发限流**：等待约一分钟后重试，采用平滑请求策略避免瞬时高峰。                                                                                          |
| **Connection error**                                                                                                    | Base URL 域名拼写错误或网络连接异常                                                       | 检查 Base URL 域名拼写及网络连接。                                                                                                                                           |

## 产品功能相关

### Token Plan 团队版的 API Key 能与其他套餐或普通 API 混用吗？

不能。Token Plan 团队版和按量计费的 API Key 和 Base URL 互不相通，请勿混用。误用其他 API Key 不会抵扣 Token Plan 团队版的套餐额度。

### 团队版的 API Key 能用在个人版上吗？

不能。个人版和团队版各自生成独立的 API Key，不可混用。系统会根据 API Key 自动识别对应的套餐。

### Harness 工具是什么？

Harness 工具是模型内置的扩展能力，包括联网搜索、文搜图、图搜图、网页抓取、代码解释器等。团队版支持 Harness 工具，调用时按工具抵扣系数消耗 Credits。当前仅 qwen3.7 和 qwen3.8 系列模型支持原生 Harness 工具调用。

### 高峰期性能如何？

团队版基于多租户隔离架构，调用高峰期间不排队。

### 能在多个工具中使用同一订阅吗？

可以。同一 API Key 可在全部兼容的 AI 编程和智能体工具中使用，额度共享消耗。每个成员持有独立的 API Key，不可共享给其他成员。

### 有哪些使用限制？

仅限在兼容的 AI 编程和智能体工具中交互式使用，不可用于自动化脚本或应用后端。违规使用可能导致订阅暂停或 API Key 封禁。

### 团队管理入口在哪里？

在 [Token Plan 管理](https://platform.qianwenai.com/home/billing/subscription/token-plan) 页面点击**添加成员并分配席位**，即可进入[配置成员与席位](https://platform.qianwenai.com/home/billing/subscription/token-plan/config)页面，管理组织 SSO 配置、添加成员、分配和回收席位。也可通过独立的[管理平台](https://tokenplan-enterprise.qianwenai.com)访问完整的团队管理功能。详见[团队管理](/token-plan/team/team-management)。

### 成员如何获取 API Key？

管理员在管理后台创建成员账号并分配席位后，为成员生成 API Key。成员无法自行生成，需联系管理员获取。详见[团队管理](/token-plan/team/team-management)。

### 回收席位、修改角色、移出组织有什么区别？

这三个操作都在成员管理页面执行，但作用范围不同：

- **回收席位**：撤销成员的席位使用权并将席位释放回席位池。成员失去使用权，但仍留在组织中，可被重新分配席位。
- **修改角色**：变更成员的权限（如管理员/普通成员），不影响席位分配和组织归属。
- **移出组织**：将成员从团队完全移除，席位自动回收至席位池，成员从成员列表消失。

### 购买后为什么没有可分配的席位？

团队版席位购买后不会自动分配，需要管理员手动分配。前往[配置成员与席位](https://platform.qianwenai.com/home/billing/subscription/token-plan/config)页面，可查看剩余席位数量、各成员的分配状态，并进行席位分配。详见[团队管理](/token-plan/team/team-management)。

### 为什么 API Key 只能查看一次，丢失后如何处理？

为避免团队间 API Key 混用导致计费混乱，API Key 仅在首次生成或重置时显示，后续无法再次查看或复制。若 API Key 丢失，在**成员管理**页面找到对应成员，点击**重置**生成新 Key，原 Key 立即失效，需在工具中重新配置。

## 购买相关

### 可以同时购买多个套餐吗？

每个账号限购一个订阅，同一订阅下每种席位类型均可购买多个。加油包可叠加购买，单次最多 1000 个。

### 可以单独购买加油包吗？

不可以。加油包是 Token Plan 团队版的附加商品，需先订阅 Token Plan 团队版席位套餐后，才能购买加油包。

### 套餐是否支持退订？

支持按席位退订。在 [Token Plan 管理](https://platform.qianwenai.com/home/billing/subscription/token-plan) 页面的用量详情中，点击席位的**退席位**即可退订。已有用量消耗的席位不可退订。退款原路退回支付账户。

### 如何关闭或开启自动续费？

登录 [Token Plan 管理页面](https://platform.qianwenai.com/home/billing/subscription/token-plan)，通过页面上的**自动续费**开关关闭或开启自动续费。

### 续费时可以更换订阅时长吗？

不可以。续费仅支持按原订阅时长续费。如需更换订阅时长，可在订阅到期后重新购买。

### 限时优惠的计费规则是什么？

限时优惠适用于包月订阅的新购、续费和自动续费。加购席位或升级席位时，按剩余时长折算费用，实际收费取折算金额与限时价中的较低值。例如：标准席位原价 198 元/月、限时价 150 元/月，若加购时按剩余天数折算费用为 120 元（低于限时价），则收 120 元；若折算费用为 180 元（高于限时价），则收 150 元。

### 账号欠费是否影响 Token Plan 团队版的使用？

Token Plan 团队版为预付费订阅产品，只要套餐额度未用尽且订阅仍在有效期内，账号欠费不影响 Token Plan 团队版的正常使用。

## 计量相关

### Credits 抵扣规则是什么？

Token Plan 团队版实际消耗取决于每次请求中输入 Token、缓存 Token 和输出 Token 的组合。优先从席位额度抵扣，席位额度用尽后从加油包抵扣，全部用尽后服务暂停至下一计费周期或购买加油包补充额度。

### 如何查看用量？

在 [Token Plan 管理页面](https://platform.qianwenai.com/home/billing/subscription/token-plan)可查看套餐和加油包的用量详情。管理员还可在[管理后台](https://tokenplan-enterprise.qianwenai.com)的用量分析页面查看全部成员的消耗明细。

### 被分配席位的成员如何查看自己的用量？为什么在自己账号下看不到 Token Plan？

团队版订阅归属于购买者账号。被分配席位的成员无法在自己账号下查看 Token Plan 订阅或用量明细——**用量分析为所有者功能**，需由购买者（所有者）在 Token Plan 控制台「我的订阅 → 用量分析」查看各成员的 Credits 消耗（详见[团队管理](/token-plan/team/team-management)）。添加席位时系统会为成员自动生成专属 API Key，成员使用该 Key 即可调用模型，无需在自己账号下查看订阅。

### 用量如何重置？

席位额度在每个订阅月到期时重置，未用完的额度不累积到下月。加油包额度购买后有效期为 1 个月，到期后需重新购买，不随席位额度按月重置。

### 超出限额之后怎么办？

席位额度用尽后自动从加油包抵扣；全部额度用尽后服务暂停。可通过以下方式恢复：

- 购买加油包补充额度。
- 等待下一计费周期额度自动重置。
- 升配或加购坐席：升配后立即生效，限额按新坐席类型执行（需补缴差价，按剩余天数折算）；加购坐席按剩余时长折算费用。

### 续费后为什么 Credits 没有增加？

Token Plan 团队版的席位额度按订阅周期计算，每个订阅月到期时自动重置。续费仅延长订阅有效期或预定下一计费周期的额度，**不会叠加补充至当前计费周期**。

若当前周期额度已用尽且需立即恢复服务，可通过以下方式恢复：

- 购买加油包补充额度。
- 升级至更高规格的席位。

## 数据安全

### 数据安全如何保障？

Token Plan 团队版承诺不使用对话数据训练模型，传输过程采用 HTTPS 加密，并基于多租户隔离架构保障企业级数据隔离。
