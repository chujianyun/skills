> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 创建数据集

> 上传训练数据或评测数据到千问AI平台，用于模型微调或模型评测。

本指南介绍如何在千问AI平台控制台中创建数据集。

## 前提条件

- 一个可访问控制台的千问AI平台账号。
- 已准备好数据文件。训练集使用 `.jsonl` 或 `.zip` 格式，评测集使用 `.jsonl` 格式。格式要求请参见[数据集概览](/developer-guides/datasets/overview)。

## 创建训练集

<Steps>
  <Step title="打开数据集页面">
    前往[数据集](https://platform.qianwenai.com/home/model-production/datasets)页面，点击**创建数据集**。
  </Step>

  <Step title="选择数据集类型">
    选择**训练集**。
  </Step>

  <Step title="输入数据集名称">
    为数据集提供一个描述性名称。
  </Step>

  <Step title="选择任务类型">
    根据微调目标选择任务类型：

| 任务类型          | 说明             |
| ------------- | -------------- |
| **文本生成**      | 用于文本类模型的微调     |
| **视觉理解**      | 用于视觉理解模型的微调    |
| **图生视频（首帧）**  | 用于图生视频模型的首帧微调  |
| **图生视频（首尾帧）** | 用于图生视频模型的首尾帧微调 |
  </Step>

  <Step title="选择微调算法">
    根据任务类型选择微调算法：

    - 文本生成：**SFT**（监督微调）、**DPO**（直接偏好优化）、**CPT**（持续预训练）
    - 视觉理解 / 图生视频：**SFT**
  </Step>

  <Step title="上传文件">
    将文件拖放到上传区域或点击浏览。

    - 文本生成：`.jsonl` 格式（每文件最大 200 MB，最多 10 个文件）
    - 视觉理解 / 图生视频：`.zip` 格式

    图生视频任务还支持**独立上传验证集**（`.zip` 格式）。
  </Step>

  <Step title="提交">
    根据任务类型和算法，提交方式不同：

    - 文本生成 **SFT** / **DPO**：可选择**存为草稿**（之后发布）或**立即发布**。
    - 其他（文本生成 CPT、视觉理解、图生视频）：仅支持**立即发布**。
  </Step>
</Steps>

<Note>
  选择**存为草稿**后，数据集处于**草稿**状态，必须先发布才能在微调任务中使用。详见[发布数据集](/developer-guides/datasets/manage-datasets#发布数据集)。文本生成 CPT、视觉理解和图生视频任务提交后直接发布，无需单独发布。
</Note>

<Tip>
  创建页面右侧面板显示文件格式要求和所选算法的示例文件下载链接。
</Tip>

## 创建评测集

<Steps>
  <Step title="打开数据集页面">
    前往[数据集](https://platform.qianwenai.com/home/model-production/datasets)页面，点击**创建数据集**。
  </Step>

  <Step title="选择数据集类型">
    选择**评测集**。
  </Step>

  <Step title="输入数据集名称">
    为数据集提供一个描述性名称。
  </Step>

  <Step title="上传文件">
    上传 JSONL 格式文件（`.jsonl`），每行包含 `prompt`（问题）和 `completion`（参考答案）字段。
  </Step>

  <Step title="提交">
    点击**立即发布**创建数据集，发布后即可在评测任务中使用。
  </Step>
</Steps>

## 下一步

- [管理数据集](/developer-guides/datasets/manage-datasets) -- 发布数据集使其可用于微调或评测。
- [数据集概览](/developer-guides/datasets/overview) -- 完整格式参考。
- [创建微调任务](/developer-guides/fine-tuning/create-fine-tuning-job) -- 使用已发布的训练集训练模型。
- [评测任务](/developer-guides/evaluation/evaluation-tasks) -- 使用已发布的评测集评测模型。
