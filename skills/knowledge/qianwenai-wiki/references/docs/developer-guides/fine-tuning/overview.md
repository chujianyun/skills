> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 模型微调概览

> 通过千问AI平台的 SFT、DPO、CPT 微调 Qwen 模型，支持 LoRA 和全参训练模式。

模型微调使用您的数据在基础模型上训练，让模型学会特定领域的知识、任务执行方式或输出风格。微调后的模型需要[部署](/developer-guides/deployment/overview)后才能调用。

<Tip>
  建议先尝试提示词工程或工具调用来优化应用。微调需要准备训练数据、消耗训练费用且迭代速度较慢，通常作为提升模型表现的最后手段。
</Tip>

## 前提条件

创建微调任务前，您需要：

- 一个千问AI平台账号。请登录[控制台](https://platform.qianwenai.com)。
- 一个已**发布**的训练集。参见[创建数据集](/developer-guides/datasets/create-dataset)和[管理数据集](/developer-guides/datasets/manage-datasets#发布数据集)进行发布。

## 训练方式

| 训练方式            | 核心目标         | 典型场景               |
| --------------- | ------------ | ------------------ |
| **CPT**（持续预训练）  | 补知识——注入领域知识  | 金融术语、医疗病理、法律判例     |
| **SFT**（监督微调）   | 学做事——学会执行任务  | 客服流程、编程范式、工具调用     |
| **DPO**（直接偏好优化） | 做得更好——对齐人类偏好 | 拒绝有害建议、回答更简洁、评价更客观 |

三种方式递进互补，推荐流程：

`CPT（可选）→ SFT → DPO（可选）`

- CPT 用无标签的领域语料做自监督学习（预测下一个词），让模型掌握专业词汇和事实。通常在 SFT 之前进行。
- SFT 用标注好的输入/输出对做监督学习，教模型对话格式和任务执行能力。大多数场景仅需 SFT。
- DPO 用正负样本对比学习，增大好答案概率、降低坏答案概率。在 SFT 之后作为对齐的最后一步。

## 训练模式

| 训练模式           | 说明                              | 适用场景                | 支持的训练方式     |
| -------------- | ------------------------------- | ------------------- | ----------- |
| **LoRA**（高效训练） | 冻结基础模型，仅训练低秩适配器权重。速度快、成本低       | 优化特定场景效果，对训练时间和成本敏感 | SFT、DPO     |
| **全参训练**       | 更新模型全部参数。训练时间更长、成本更高。CPT 仅支持此模式 | 需要模型学习全新能力，追求全局效果最优 | SFT、DPO、CPT |

大多数 SFT/DPO 场景使用 LoRA 即可。

## 支持的模型

| 模型类别 | 模型系列                   | 支持的训练方式         |
| ---- | ---------------------- | --------------- |
| 文本生成 | Qwen 系列                | SFT / DPO / CPT |
| 视觉理解 | Qwen3-VL、Qwen2.5-VL 系列 | SFT             |
| 图生视频 | Wan-I2V（万相）系列          | SFT             |

各训练方式和训练模式下可选的具体模型请在[创建微调任务](https://platform.qianwenai.com/home/model-production/fine-tuning/create)时查看。

您也可以选择之前微调过的自定义模型作为基础模型进行迭代训练。创建微调任务时，在基础模型选择器中切换到**自定义模型**标签页，即可选择您自己的模型。

## 数据格式

数据格式根据训练方式和任务类型不同。各算法及任务类型的格式示例和详细要求请参见[数据集概览](/developer-guides/datasets/overview)。

核心字段速览：

| 训练方式 / 任务类型 | 核心字段                                                                                  |
| ----------- | ------------------------------------------------------------------------------------- |
| SFT（文本）     | `messages`（含 system/user/assistant 多轮对话）                                              |
| DPO（文本）     | `messages`（上下文）+ `chosen` + `rejected`（偏好对）                                           |
| CPT（文本）     | `text`（纯文本）                                                                           |
| 视觉理解        | `messages`，`content` 为数组，含 `image` / `video`（视频支持路径模式和图片帧列表模式，仅 qwen3.5 及以后的 VL 模型支持） |
| 图生视频        | `data.jsonl` + 图片 + 视频，首帧与首尾帧目录结构不同                                                   |

## 数据要求

| 训练方式 | 推荐数据量     | 输入格式        |
| ---- | --------- | ----------- |
| CPT  | 一千万 Token | 无标签的领域文本    |
| SFT  | 1,000 条   | 高质量的输入-输出对  |
| DPO  | 100 组     | 同一输入下的正负偏好对 |

如果微调后模型表现不佳，最直接的改进方法是收集更多高质量数据。如果短期难以收集足够数据，建议先用 RAG 应用积累数据，再考虑微调。各场景的数据比例应符合实际使用比例，避免某类数据过多导致模型偏向该类特征。质量优先于数量——少量精准的训练数据优于大量低质量数据。

## 计费

按训练消耗的 Token 数计费：

`训练费用 = 训练数据 Token 总数 × 循环次数 × 训练单价`

各模型类别的训练单价、计费公式与计费示例详见[微调训练计费](/developer-guides/fine-tuning/training-billing)。

创建任务时，控制台底部显示预估训练费用，点击**计算详情**可查看训练 Token 总数、循环次数和训练单价明细。微调后的模型需[部署](/developer-guides/deployment/overview)后才能调用，部署和调用产生额外费用。

## 检查点与输出

训练过程中，控制台实时显示**训练 Loss** 和**验证 Loss** 曲线，帮助判断训练效果。训练完成后系统生成若干检查点（Checkpoint），在任务详情页发布检查点后，它将成为[自定义模型](/developer-guides/custom-models/overview)，可用于部署或作为基础模型迭代训练。检查点保存在云存储中，暂不支持下载。

## 下一步

- [创建数据集](/developer-guides/datasets/create-dataset) -- 准备微调训练数据
- [创建微调任务](/developer-guides/fine-tuning/create-fine-tuning-job)（控制台操作）
- [超参数参考](/developer-guides/fine-tuning/hyperparameters) -- 超参数说明与调参建议
- [管理微调任务](/developer-guides/fine-tuning/manage-fine-tuning-jobs) -- 监控进度并发布检查点以创建自定义模型
- [部署概览](/developer-guides/deployment/overview) -- 部署自定义模型以提供推理服务
