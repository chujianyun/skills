> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 自定义模型概览

> 查看和管理您在千问AI平台上微调的模型。

自定义模型是您通过微调任务创建的模型。微调任务完成后，您[发布检查点](/developer-guides/fine-tuning/manage-fine-tuning-jobs#发布检查点)将其添加到自定义模型列表中。[自定义模型](https://platform.qianwenai.com/home/model-production/custom-models)页面列出了您从微调检查点发布的所有模型。

## 模型列表

列表页展示所有自定义模型，使用顶部筛选器缩小范围：

- **全部类型**：按模型类型筛选（如按模态或训练方式过滤）。

每条记录显示模型名称 / ID、基础模型、来源和当前状态。**来源**列显示该模型的微调任务，可点击跳转到对应的微调任务详情页。

<Note>
  如果对应的微调任务已被删除，来源链接将置灰且无法跳转，但自定义模型本身仍保留可用。
</Note>

## 可用操作

您可以对任何自定义模型执行以下操作：

- **部署** -- 创建部署，将模型作为 API 端点提供服务。自定义模型必须部署后才能通过 API 调用。详见[部署概览](/developer-guides/deployment/overview)。
- **增量训练** -- 将此模型作为另一次微调任务的基础模型。这使您可以通过额外的数据或不同的超参数迭代改进模型。在[创建微调任务](/developer-guides/fine-tuning/create-fine-tuning-job)时，该模型会出现在基础模型选择器的**自定义模型**标签页中。
- **删除** -- 从您的账号中永久移除模型。删除后，对应微调任务详情的输出区将显示"已删除"状态。

## 下一步

- [部署概览](/developer-guides/deployment/overview) -- 部署自定义模型以供 API 访问。
- [微调概览](/developer-guides/fine-tuning/overview) -- 训练新的自定义模型。
