> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 计费与定价

> 付费和费用常见问题

## 计费方式

### 按量付费和 Token Plan 有什么区别？

**按量付费（API 调用）**

- 按百万 token 消耗量计费
- 输入和输出分别定价
- 适合：API 集成、应用开发、批量处理
- 灵活：用多少付多少
- 支持所有优化功能（Batch API、上下文缓存）

**Token Plan 团队版（订阅制）**

- 按 Credits 计费（以 token 用量换算，非按请求次数）
- 多种坐席套餐（¥198–¥1,398/坐席/月）
- 适合：团队使用 AI 编程工具（Claude Code、Qwen Code、OpenClaw 等）
- 费用可预测，支持文本与图像生成
- 使用专属 API Key（`sk-sp-xxxxx`）

### 如何选择计费方式？

- **开发应用或做 API 集成？** → 选择按量付费
- **团队每天使用 AI 编程工具？** → 选择 Token Plan
- **刚开始体验？** → 先用按量付费，搭配免费额度

## 账单分析

### 如何查看账单明细？

账单支持按模型、API Key、业务空间进行精细化对账。

1. 进入[按量付费](https://platform.qianwenai.com/home/billing/pay-as-you-go)页面。
2. 在**消费趋势**区域，点击右上角的**列表**切换到列表视图。
3. 使用筛选器按**模型**或 **API Key** 筛选，快速定位具体消费。

列表中各列含义如下：

- **模型**：产生费用的模型名称。
- **用量**：Token 消耗量或调用次数。
- **应付金额**：该条目的费用。
- **业务空间名称**：对应[业务空间](https://platform.qianwenai.com/home/settings/workspaces)页面中的空间。
- **描述/API Key**：对应 [API Key](https://platform.qianwenai.com/home/api-keys) 页面中的 Key。
- **费用类型**：例如"云资源按量费用"。

### 为什么调用模型后没有立即看到账单？

可能原因：

1. **账单延迟**：账单按小时更新，高峰期可能延迟（16:00-17:00 的消费可能在 19:30 才出现）。
2. **免费额度**：使用免费额度或调用免费模型时，不产生费用，也不生成账单。

### 在哪里查看模型调用统计？

前往[用量分析](https://platform.qianwenai.com/home/analytics)页面查看。

## 付费与扣费

### 按量付费是实时扣费吗？

不是。系统会预先冻结额度，在月末（次月初）统一结算。

### 如何停止计费？

- 停止使用模型体验或停止 API 调用。
- 在 [API Key](https://platform.qianwenai.com/home/api-keys) 页面删除 API Key，防止意外调用。

### 充值未消费的金额如何退回？

如需提取账户中未消费的余额，请参考[余额提现](https://help.aliyun.com/zh/user-center/balance-withdrawal)。

### 内置工具（如联网搜索）是否额外收费？

是的。部分内置工具在模型 token 费用之外，还会按调用次数收费。联网搜索每 1,000 次调用收费 4 元，文搜图每 1,000 次调用收费 24 元，图搜图每 1,000 次调用收费 48 元。网页抓取和代码解释器暂时免费。详见[计费说明](/developer-guides/getting-started/pricing#built-in-tools)。工具调用费用不在免费额度覆盖范围内。
