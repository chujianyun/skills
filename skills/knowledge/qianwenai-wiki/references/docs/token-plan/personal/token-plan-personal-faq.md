> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 常见问题

> Token Plan 个人版的额度、购买、订阅和接入常见问题。

## 额度与限额

### 7 天限额是什么意思？

Token Plan 个人版采用每 7 天固定窗口限额，限额单位为 Credits。窗口期内累计消耗达到限额后暂停服务，需等待窗口结束后额度重置。窗口期内未用完的额度不结转至下一周期。

例如：Standard 套餐的 7 天限额为 10,000 Credits。您在 7 月 20 日首次调用，系统开启窗口（7 月 20 日 \~ 7 月 27 日）。7 月 20 日消耗 4,000 Credits，7 月 22 日消耗 6,000 Credits，累计 10,000 Credits 触顶暂停。需等到 7 月 27 日窗口结束，额度重置为 10,000 Credits，服务恢复。

各档位限额如下：

| 档位          | 7 天限额          |
| ----------- | -------------- |
| Lite 套餐     | 2,500 Credits  |
| Standard 套餐 | 10,000 Credits |
| Pro 套餐      | 40,000 Credits |

### 7 天限额是固定日期重置吗？

不是。7 天限额采用固定窗口机制，自首次调用起计时 7 天，到期后额度重置。重置时间取决于您首次调用的时间，而非固定的日历日期（如每周一）。

### 额度用完了怎么办？

限额用完后调用会被阻断，不会按量计费。恢复方式：

- 使用限额重置权益，立即刷新恢复额度。
- 等待额度释放。
- 升级套餐。
- 购买加油包，获得不受限额约束的额外额度。

### 什么是重置卡？如何使用？

重置卡是 Token Plan 个人版订阅用户的一次性额度重置权益。在 Token Plan 订阅页面的套餐额度区域，可以看到**重置限额**按钮，按钮旁标注剩余可用次数（如"1 次可用"），单击旁边的 info 图标可查看提示"使用重置卡可立即重置套餐额度"。单击**重置限额**按钮即可立即重置套餐额度。该权益为一次性发放，非定期发放，发放时不单独发送邮件通知。

### 开通 Token Plan 后为什么仍产生按量扣费？

开通 Token Plan 后仍看到按量扣费，通常是以下原因导致：

- **生效前调用**：开通 Token Plan 之前发生的调用属于独立计费，无法被套餐抵扣。
- **配置错误**：未使用 Token Plan 专属 API Key 和 Base URL（例如误用通用 dashscope.aliyuncs.com 的 Key），导致请求走按量计费通道。
- **模型不支持**：调用了 Token Plan 白名单之外的模型。

已产生的按量费用无法通过 Credits 事后抵扣或退款。请立即检查并更正 API Key 和 Base URL 配置，确保后续调用正常抵扣。

### 加油包和套餐是什么关系？需要先买套餐吗？

加油包是套餐的补充，提供不受套餐限额约束的额外 Credits，需先订阅有效套餐后才能购买，最多同时持有 5 个。

### 加油包的额度有窗口限制吗？

没有。加油包额度不受套餐的 7 天窗口限额约束，购买后即可使用。

### 加油包有效期多久？在哪里购买？

加油包有效期为 1 个月，到期后未使用的额度自动作废，不支持退款。购买入口在 [Token Plan 个人版管理页面](https://platform.qianwenai.com/home/billing/subscription/token-plan-individual)。

### Token Plan 的用量在哪里查看？

在 [千问AI平台控制台](https://platform.qianwenai.com/home/billing/subscription/token-plan-individual)的 **Token Plan > 我的订阅** 页面查看当前订阅的 Credits 额度及消耗情况。

### 为什么账单/插件统计的 Credits 消耗与预期不一致？

Credits 消耗与账单或插件统计出现差异，常见原因：

- **上下文缓存命中**：命中缓存时抵扣系数较低，未命中时抵扣系数较高。
- **模型系列差异**：不同模型（如 Qwen 系列与 GLM 系列）的 Credits 抵扣系数不同。
- **功能模式影响**：频繁切换工具调用或思考模式可能影响计费。

验证方法：对比具体时间段内的抵扣记录，通过"抵扣 Credits ÷ 消耗 Token"计算实际系数进行核实。

### Token Plan 是否提供免费试用额度或赠送 Token？

Token Plan 套餐本身不提供试用额度，也不包含免费赠送的 Token 额度。千问AI平台针对部分模型提供独立的免费额度，可以在控制台查询可用免费额度的模型列表。

### 如何减少 Token Plan 的 Credits 消耗？

- 压缩历史消息或新开对话窗口，避免长上下文累积消耗。
- 关闭思考模式（Thinking Mode）以降低推理开销。
- 非复杂任务场景下切换至轻量模型（如 qwen3.6-plus 替代 qwen3.7-max）。
- 利用缓存机制，缓存命中的 Token 计费价格低于正常 Input Token。
- 通过**用量分析**页面监控消耗明细，及时调整使用策略。

### 为什么第三方工具（如 Claude Code）显示的 Token 用量与控制台统计不一致？

- **统计口径不同**：第三方工具仅显示模型层面的输入输出 Token；控制台统计包含完整消耗项。
- **隐藏消耗项**：系统提示词、工具定义（Schema）、用户配置、项目约定、多轮对话历史累积、工具调用参数与返回结果、模型内部推理内容（reasoning）等，均会计入 Credits 消耗但不在第三方工具中显示。
- **模型单价影响**：Credits 消耗与模型抵扣系数相关，高价模型（如 qwen3.7-max）会导致相同 Token 数下 Credits 消耗更高。
- **优化建议**：通过控制台 Token Plan 订阅页的**用量分析**查看官方统计；使用 `/compact` 压缩历史消息或 `/clear` 新开对话以减少上下文累积。

## 接入报错

### 常见报错及解决方案

| 报错信息                                                            | 可能原因                                         | 解决方案                                   |
| --------------------------------------------------------------- | -------------------------------------------- | -------------------------------------- |
| 401 InvalidApiKey: No API-key provided.                         | 请求头中未携带 API Key                              | 生成 API Key 并在工具中完成配置                   |
| 401 InvalidApiKey: Invalid API-key provided.                    | 误用了按量计费的 API Key；订阅过期；Key 复制不完整              | 确认使用 Token Plan 个人版专属 API Key，确保完整且无空格 |
| 404 model\_not\_found: Model not exist.                         | 模型名称拼写错误或不在支持列表                              | 确认模型名称区分大小写，与套餐支持的模型 ID 一致。            |
| 403 AccessDenied.Unpurchased: Access to model denied.           | 调用的模型仅团队版支持，个人版不支持                           | 改用个人版支持的模型，或使用 Token Plan 团队版          |
| 401 invalid access token or token expired                       | 误用了其他计费模式的 Base URL                          | 使用 Token Plan 个人版专属 Base URL           |
| 401 Incorrect API key provided                                  | 误用了千问AI平台通用 Base URL（dashscope.aliyuncs.com） | 使用 Token Plan 个人版专属 Base URL           |
| 429 Requests rate limit exceeded                                | 短时间内请求过于密集                                   | 等待一分钟后重试，降低请求频率                        |
| 429 Allocated quota exceeded                                    | 7 天限额用尽                                      | 使用限额重置权益、购买加油包或等待窗口释放额度                |
| 400 invalid\_parameter\_error: Unexpected item type in content. | 向纯文本模型传入了图像等非文本内容                            | 改用支持该模态的模型，或确认请求内容与模型能力匹配              |
| 502 Bad Gateway                                                 | 服务端偶发异常                                      | 稍后重试                                   |

### Token Plan 用量显示为 0 或调用仍扣费/欠费怎么办？

- 用量显示为 0 通常是因为尚未产生实际消耗，或使用了非 Token Plan 专属 API Key。
- 调用仍扣余额或产生欠费，是因为配置了普通 API Key 而非套餐专属 Key。

## 并发与性能

### 最多支持多少个 Agent 并发？

并发能力与套餐档位相关：

| 档位          | 建议并发                   |
| ----------- | ---------------------- |
| Lite 套餐     | 可同时支持 1-2 个 Agent 并发运行 |
| Standard 套餐 | 可同时支持 3-4 个 Agent 并发运行 |
| Pro 套餐      | 可同时支持 6-8 个 Agent 并发运行 |

### 高峰期响应会变慢吗？

高峰期可能出现排队等待。如需更稳定的吞吐，可升级到更高档位或使用团队版。

### Token Plan 的限流阈值（TPM/RPM）是多少？能否提升？

官方未公开具体的 TPM/TPS/RPM 数值，限流阈值会根据整体负载动态调整以保障服务稳定性。套餐限流额度不支持提升。

优化建议：精简上下文、降低任务复杂度以减少单次输入 Token 数量；遇到限流时等待约 1 分钟后重试。

## 使用规则

### "禁止 API 生产自动化调用"具体是什么意思？

Token Plan 个人版仅供个人通过官方指定工具（如 Cursor、Claude Code、Windsurf 等）进行交互式开发。不允许将 API Key 用于生产环境的自动化服务、批量脚本或后台定时任务等非交互场景。

### 多人共用一个账号可以吗？

不可以。Token Plan 个人版限单人使用，不允许多人共用同一账号或 API Key。如需多人协作，请使用 Token Plan 团队版。

### 可以在多台设备上使用同一个 API Key 吗？

可以。Token Plan 个人版每个订阅对应一个专属 API Key，生成后请立即复制并妥善保存。您可以将同一个 API Key 配置到多台设备（如家庭电脑和公司电脑）上使用，无需为每台设备重新生成。

重置 API Key 会使旧 Key 立即失效，届时需在所有设备上更新为新 Key。建议仅在 Key 泄露时才重置。

## 购买与订阅

### 可以升配吗？升配后额度怎么算？

支持从低档位升级到更高档位。前往 [Token Plan 个人版购买页面](https://platform.qianwenai.com/pricing/token-plan) 选择目标档位完成升级。升级按剩余时长补缴差价，升级后限额立即提升至新档位对应额度。

### 可以降配吗？

不支持降配。如需更换为更低档位，可在订阅到期后重新购买。

### 自动续费怎么取消？

登录 [Token Plan 管理页面](https://platform.qianwenai.com/pricing/token-plan)，在订阅管理中关闭自动续费。

### 如何查看 Token Plan 套餐的生效时间和剩余天数？

- **生效时间查看路径**：登录[千问AI平台控制台](https://platform.qianwenai.com/home/billing/subscription/token-plan-individual)的 **Token Plan** 页面查看套餐生效时间。
- **剩余天数显示逻辑**：控制台显示的剩余天数为向下取整后的完整 24 小时周期数，实际有效期以具体结束时间戳为准（例如剩余 22 天 20 小时会显示为 22 天），属正常显示逻辑。

### Token Plan 是否支持学生代金券购买？

不支持。学生代金券仅适用于活动界面指定的产品，不能用于购买 Token Plan。
