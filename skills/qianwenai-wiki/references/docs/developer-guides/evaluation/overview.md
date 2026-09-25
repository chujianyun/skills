> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 模型评测概览

> 通过千问AI平台的模型评测功能，从多维度量化模型表现，支持 LLM 自动打分与人工标注两种方式。

模型评测用于从多维度量化模型的输出质量。您可以在[模型评测](https://platform.qianwenai.com/home/model-production/evaluations/tasks)控制台页面创建评测维度和评测任务。

## 核心概念

模型评测由两个子模块组成：

- **评测维度** — 定义"用什么标准打分"。支持 LLM 自动打分（数值型 / 分类型）和人工标注三种类型。
- **评测任务** — 选择评测维度 + 数据集 + 待评测模型，执行评测并查看结果。

## 评测流程

<Steps>
  <Step title="定义评测维度">
    创建一个或多个评测维度，选择维度类型、裁判模型和打分模板。参见[评测维度](/developer-guides/evaluation/evaluation-dimensions)。
  </Step>

  <Step title="准备评测数据">
    在[数据集](/developer-guides/datasets/create-dataset)中创建**评测集**类型的数据集并发布。
  </Step>

  <Step title="创建评测任务">
    选择数据来源、评测模型和评测维度，提交任务。参见[评测任务](/developer-guides/evaluation/evaluation-tasks)。
  </Step>

  <Step title="查看评测结果">
    在任务列表中查看得分、Token 用量等指标，点击详情查看每条样本的打分明细。
  </Step>
</Steps>

## 计费说明

模型评测的费用由两部分组成：

| 费用类型       | 是否计费 | 说明                                                           |
| ---------- | ---- | ------------------------------------------------------------ |
| 被评测模型的推理费用 | 是    | 使用"评测数据集"作为数据来源时，系统会调用被评测模型执行推理，按 Token 计费。使用"推理结果集"时不产生此费用。 |
| 裁判模型的评分费用  | 限时免费 | LLM 类型评测维度（数值型、分类型）的裁判模型打分过程目前限时免费。                          |

## 下一步

- [评测维度](/developer-guides/evaluation/evaluation-dimensions) -- 了解三种维度类型并创建自定义评测标准。
- [评测任务](/developer-guides/evaluation/evaluation-tasks) -- 创建评测任务并查看结果。
- [创建数据集](/developer-guides/datasets/create-dataset) -- 准备评测数据集。
