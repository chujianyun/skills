> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 账单查询与费用管理

> 查看按量付费账单、还款及成本管理

了解如何查询账单明细、完成还款以及控制费用。

关于计费类型和定价的详细信息，请参见[定价](/developer-guides/getting-started/pricing)。

## 按量付费账单

按量付费页面顶部显示本月已出账金额和消费限额。下方可通过图表或列表查看账单明细。

在[按量付费](https://platform.qianwenai.com/home/billing/pay-as-you-go)页面：

1. 在**列表**和**图表**视图之间切换：
   - **列表**：查看逐条账单记录
   - **图表**：可视化消费趋势
2. 使用筛选条件缩小范围：
   - **全部 API Key**：按 API Key 筛选
   - **全部模型**：按模型筛选
   - **按月/按日**：切换时间粒度
   - 选择账单月份

<Tip>
  如需申请发票，请参见[发票管理](/resources/invoice)。
</Tip>

## 账单结算与还款

### 还款到期日

| 用户类型  | 计费方式      | 还款时间            |
| ----- | --------- | --------------- |
| 非信控用户 | 预付费       | 下单时立即扣款         |
| 非信控用户 | 后付费（按量付费） | 次月 1 日系统自动结算    |
| 信控用户  | 按合同约定     | 依据合同中的结算周期和付款账期 |

### 自动核销

当账单到期时，系统自动从可用额度中扣款（自动核销）。自动核销的触发条件：

```
现金余额 + 信控额度 - 已冻结金额 > 0
```

若可用额度不足，账单将保持**未结清**状态，需手动处理。

### 手动还款

有两种方式完成还款：

**方式一：充值后自动结清**

在[账单概览](https://platform.qianwenai.com/home/billing/overview)页面充值，系统将在充值到账后自动结清所有未结清账单。

**方式二：手动还款历史欠款**

在[账单概览](https://platform.qianwenai.com/home/billing/overview)页面点击**去还款**，可针对历史未结清账单进行还款。

<Note>
  **去还款**仅覆盖历史未结清账单，不包含当月未结清金额（当月账单将在月末自动结算）。
</Note>

## Token Plan 计费

Token Plan 是一种订阅制方案，按 Credits（token 用量）计费。在 [Token Plan](https://platform.qianwenai.com/home/billing/subscription/token-plan) 页面可以查看：

- 当前套餐的总用量、剩余用量、状态和生效周期
- **加油包**的数量和剩余用量
- **订阅历史**：查看和筛选历史订阅订单

方案详情和定价请参见 [Token Plan 团队版概览](/token-plan/overview)。

## 费用管理

### 设置消费限额和告警

在[按量付费](https://platform.qianwenai.com/home/billing/pay-as-you-go)页面，点击**限额**旁的设置图标，打开**消费限额与告警**对话框：

1. 启用**月度限额**
2. 在**新限额**字段中设置消费上限
3. 配置告警：
   - **告警阈值**：拖动滑块设置通知百分比（如 80%）
   - **通知方式**：添加接收告警的手机号和邮箱地址
4. 点击**保存设置**

<Note>
  消费限额和告警仅针对按量付费的消费金额进行预警，不包含预付费订阅套餐（如 Token Plan）的消费金额。
</Note>

消费达到告警阈值时会收到通知。告警通常在 15 分钟内发送，但具体时间可能有所浮动。

<Note>
  消费限额帮助您控制成本，在费用超出预算前及时收到告警。更多降本策略请参见[费用优化](/developer-guides/run-and-scale/cost-optimization)。
</Note>

### 停止计费

如果不再需要使用千问AI平台，可通过以下方式避免产生费用：

- 停止使用模型体验或发起 API 调用。
- 在 [API Key](https://platform.qianwenai.com/home/api-keys) 页面删除 API Key，防止意外调用。

## 常见问题

### 调用模型后为什么没有立即看到账单？

1. **账单延迟**：账单每小时更新一次，高峰期可能延迟（如 16:00-17:00 的消费可能在 19:30 才出账）。
2. **免费额度**：使用免费额度或调用免费模型时不产生费用，也不会生成账单。

### 按量付费是实时计费吗？

不是。系统会预冻结额度，在月底（次月初）结算。

### 在哪里查看模型调用次数和统计信息？

在[用量分析](https://platform.qianwenai.com/home/analytics)页面可以查询模型调用统计信息。

### 为什么没怎么用却产生了欠费？

**原因：** 千问AI平台的[联网搜索](/developer-guides/tool-calling/web-search)等附加功能按调用次数单独计费（后付费），与模型推理费用分开出账。即使您近期未主动操作控制台，历史创建的应用或代码中若开启了`enable_search`参数，每次被调用仍会产生联网搜索费用。

**解决方案：**

1. 在[按量付费](https://platform.qianwenai.com/home/billing/pay-as-you-go)页面，查看账单明细确认产生费用的模型名称和调用渠道。
2. 检查应用代码或应用配置中是否开启了`enable_search`，如不再需要联网搜索，将该参数设为`false`或移除。
3. 如已停止所有调用但仍有扣费，检查是否有其他 API Key 或应用仍在运行，可在 [API Key 管理](https://platform.qianwenai.com/home/api-keys)页面逐一排查或删除不再使用的 Key。

### 为什么没有主动调用 API 也会产生费用？

**原因：** 千问AI平台的模型部署按使用时长计费，模型完成部署即状态为**运行中**时开始收费，不依赖 API 调用。即使未主动通过 API 调用该模型，只要部署状态为**运行中**就会持续产生费用。

**解决方案：**

1. 前往[模型部署](https://platform.qianwenai.com/home/model-production/deployments)页面，下线不再使用的已部署模型，停止按时长计费。
2. 如需防止意外调用产生推理费用，可在 [API Key](https://platform.qianwenai.com/home/api-keys) 页面删除不再使用的 Key（注意：删除后无法恢复，请谨慎操作）。

### 如何判断账户是否被盗用？

如果怀疑账户被他人盗用产生非预期费用，按以下步骤排查：

1. 在[按量付费](https://platform.qianwenai.com/home/billing/pay-as-you-go)页面，查看账单明细确认产生费用的 API Key。
2. 前往 [API Key 管理](https://platform.qianwenai.com/home/api-keys)页面，核对每个 Key 的**创建时间**，确认是否为本人创建。API Key 管理页面仅显示创建时间，不显示调用时间。
3. 查看调用时段分布，判断是否存在非本人操作的异常调用模式：进入[用量分析](https://platform.qianwenai.com/home/analytics)页面，按**模型**或 **API Key ID** 筛选，切换至**列表**视图查看调用时间分布。
4. 如发现未授权调用，立即在 [API Key 管理](https://platform.qianwenai.com/home/api-keys)页面删除对应 API Key 并重新生成，并更新所有合法调用方使用新 Key。
