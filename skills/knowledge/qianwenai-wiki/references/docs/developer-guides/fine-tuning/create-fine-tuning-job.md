> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 创建微调任务

> 在千问AI平台控制台中创建模型微调任务的步骤指南。

本指南介绍如何使用 [千问AI平台控制台](https://platform.qianwenai.com/home/model-production/fine-tuning)创建微调任务。

## 前提条件

- 一个千问AI平台账号。请登录[控制台](https://platform.qianwenai.com)。
- 一个已发布的训练集。参见[创建数据集](/developer-guides/datasets/create-dataset)上传数据，以及[数据集概览](/developer-guides/datasets/overview)了解格式要求。

## 创建任务

前往控制台的[模型微调页面](https://platform.qianwenai.com/home/model-production/fine-tuning)，点击**创建微调任务**。

### 1. 训练方式

选择本次训练任务的训练方式及模型：

- **训练方式**：选择 **SFT**（监督微调）、**DPO**（直接偏好优化）或 **CPT**（持续预训练）。
- **选择模型**：从下拉菜单中选择基础模型。可选模型根据所选训练方式和训练模式不同而变化，切换到**自定义模型**标签页可使用之前微调过的模型进行迭代训练。
- **训练模式**：选择 **LoRA**（高效训练）或**全参训练**。CPT 仅支持全参训练。
- **任务名称**：输入名称或留空自动生成。
- **超参数**：选择模型后显示超参数配置表（批次大小、学习率、验证步数等）。默认值已优化，点击**恢复默认**可重置。详见[超参数参考](/developer-guides/fine-tuning/hyperparameters)。

### 2. 训练数据

点击**选择训练数据集**，从您的[数据集](https://platform.qianwenai.com/home/model-production/datasets)库中选择一个已发布的训练集。

### 3. 验证

可选配置验证以监控训练质量：

- **自动拆分**：自动从训练数据中拆分一部分用于验证。通过滑块调整拆分比例。
- **自定义数据集**：选择单独的数据集用于验证。

### 4. 训练产出

配置输出模型和检查点保存策略：

- **模型名称**：为微调后的模型输入名称。
- **导出数量上限**：设置最多保存的检查点数量。
- **检查点保存间隔**：按**轮次**或按**步骤**保存，并设置保存频率。

### 5. 预估费用

审核基于所选模型和数据集大小的预估费用，然后点击**创建微调任务**提交。

## 创建后

任务提交后将经历以下状态：

1. **初始化中** -- 任务已提交，正在分配资源并排队调度。
2. **运行中** -- 训练进行中。可在任务详情页监控指标。
3. **已完成** -- 训练成功完成。自定义模型已就绪。

如果训练遇到错误，状态将变为 **失败**。完整的任务状态说明请参见[管理微调任务](/developer-guides/fine-tuning/manage-fine-tuning-jobs#任务状态)。

<Tip>
  任务完成后，您可以发布检查点并部署模型。详见[管理微调任务](/developer-guides/fine-tuning/manage-fine-tuning-jobs)。
</Tip>
