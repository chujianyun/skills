> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 管理数据集

> 在千问AI平台平台上发布、编辑和删除数据集。

[数据集](https://platform.qianwenai.com/home/model-production/datasets)页面列出您账号中的所有数据集。使用搜索栏和筛选器查找特定数据集。

## 数据集列表

每个数据集条目显示：

- **数据集名称**：数据集的名称。
- **类型**：数据集类型和子类型。训练集显示具体的任务类型和微调算法（如 文本生成 / SFT），评测集显示"评测集"。
- **样本数**：数据集中的数据条目数。
- **导入状态**：数据是否已成功导入。
- **发布状态**：数据集是否已发布并可用于微调或评测。
- **创建时间**：数据集创建的时间戳。
- **操作**：可执行的操作。

## 数据集状态

数据集有两种状态：

- **草稿**：数据集已创建但尚未可用于微调或评测。您可以编辑数据集以添加或删除文件。
- **已发布**：数据集已定稿，可用于微调或评测任务。已发布的数据集不可编辑。

<Note>
  您必须先发布数据集，才能在微调或评测任务中选择它。
</Note>

## 可用操作

可用操作取决于数据集状态：

**草稿数据集：**

| 操作     | 说明                |
| ------ | ----------------- |
| **编辑** | 修改数据集名称或上传其他文件。   |
| **发布** | 定稿数据集，使其可用于微调或评测。 |
| **删除** | 从您的账号中永久移除数据集。    |

**已发布数据集：**

| 操作     | 说明                   |
| ------ | -------------------- |
| **详情** | 查看数据集详情，包括上传历史和数据预览。 |
| **克隆** | 基于此数据集创建一个副本。        |
| **删除** | 从您的账号中永久移除数据集。       |

<Warning>
  被微调或评测任务正在使用的已发布数据集无法删除。请在删除前先从所有任务中移出该数据集。
</Warning>

## 发布数据集

创建数据集（保存为草稿）后，必须发布才能用于微调或评测：

1. 前往[数据集](https://platform.qianwenai.com/home/model-production/datasets)页面。
2. 找到草稿数据集，在操作列中点击**发布**。
3. 数据集状态变为**已发布**，在[创建微调任务](/developer-guides/fine-tuning/create-fine-tuning-job)或[评测任务](/developer-guides/evaluation/evaluation-tasks)时即可在数据集选择器中使用。

## 查看数据集详情

对已发布的数据集点击**详情**可查看：

- 数据集名称、类型和算法。
- 上传历史和文件列表。
- 数据预览，显示上传文件中的样本条目。

## 下一步

- [创建数据集](/developer-guides/datasets/create-dataset) -- 上传新的训练数据或评测数据。
- [数据集概览](/developer-guides/datasets/overview) -- 查看格式要求。
- [创建微调任务](/developer-guides/fine-tuning/create-fine-tuning-job) -- 使用已发布的训练集训练模型。
- [评测任务](/developer-guides/evaluation/evaluation-tasks) -- 使用已发布的评测集评测模型。
