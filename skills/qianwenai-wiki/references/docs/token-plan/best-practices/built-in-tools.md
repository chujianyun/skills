> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 接入 Harness 工具

> 通过 Qwen 模型内置 Harness 工具扩展 AI 编程工具的能力

Token Plan 支持的部分 Qwen 模型内置 Harness 工具，可为 AI 编程工具扩展联网搜索、代码解释器、网页抓取等能力。

## 工具概览

| 工具    | 说明                                     |
| ----- | -------------------------------------- |
| 联网搜索  | 检索互联网信息，结合搜索结果生成回答                     |
| 代码解释器 | 在沙箱环境中编写与运行 Python 代码，用于数学计算、数据分析等场景   |
| 网页抓取  | 访问指定 URL 并提取内容，为大模型提供所需信息              |
| 以图搜图  | 根据输入图片从互联网搜索视觉相似的图片，适用于以图找同款、视觉内容溯源等场景 |
| 文搜图   | 根据文本描述从互联网搜索相关图片，适用于可视化问答、配图推荐等场景      |

## 支持的模型和工具

### 个人版

| 模型           | 支持的工具                    |
| ------------ | ------------------------ |
| qwen3.8-max  | 联网搜索、代码解释器、网页抓取、以图搜图、文搜图 |
| qwen3.7-max  | 联网搜索、代码解释器、网页抓取          |
| qwen3.7-plus | 联网搜索、代码解释器、网页抓取、以图搜图、文搜图 |

### 团队版

| 模型           | 支持的工具                    |
| ------------ | ------------------------ |
| qwen3.8-max  | 联网搜索、代码解释器、网页抓取、以图搜图、文搜图 |
| qwen3.7-max  | 联网搜索、代码解释器、网页抓取          |
| qwen3.7-plus | 联网搜索、代码解释器、网页抓取、以图搜图、文搜图 |

## 费用说明

Harness 工具按成功调用次数计费，费用从套餐 Credits 中抵扣。各工具的单次调用价格以[控制台模型详情页](https://www.qianwenai.com/models/qwen3.6-plus#overview)为准。

## 使用方式

将 AI 编程工具的模型切换为上述支持 Harness 的 Qwen 模型，在对话中直接提问即可。模型会根据问题自动调用相应的内置工具，无需额外配置。

<Note>
  Harness 工具依赖模型的内置工具（联网搜索、代码解释器、网页抓取等）能力，需通过 Responses API 调用才会自动触发。若所用客户端仅支持 OpenAI Chat Completions 协议，模型不会自动调用这些内置工具。请选择兼容 Responses API 的 AI 编程工具，或改用 [Responses API](/api-reference/chat/openai-responses) 接入。
</Note>
