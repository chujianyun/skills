> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 计费说明

> API 按量计费说明

<Tip>千问AI平台提供新人免费额度。详见[免费额度](/resources/free-quota)。</Tip>

不同模型类型的计费方式各异：文本模型按 token 计费，图像生成按张计费，视频生成按秒计费，语音模型按字符数或音频时长计费。调用失败不产生任何费用，也不消耗免费额度。

<Note>
  各类别旗舰模型的价格与折扣信息请前往[定价页面](https://platform.qianwenai.com/pricing/api)查看；全量模型单价请前往[模型市场](https://www.qianwenai.com/models)查看。
</Note>

## 文本生成

按百万 token 计费，输入和输出分别计价。

**阶梯计费**：部分模型采用阶梯定价——单价取决于单次请求的输入 token 总量，该请求的所有 token 均按匹配到的阶梯单价结算。

<Accordion title="阶梯计费示例">
  假设某模型设有两档计费区间：0 \< token ≤ 32K 和 32K \< token ≤ 128K。若单次请求输入 100K token，因数值落在第二区间（32K \< 100K ≤ 128K），该请求的所有 token 均按第二档单价结算——而非前 32K 按第一档、后 68K 按第二档。
</Accordion>

**影响计费的因素**：

- **Batch 调用** — 输入和输出 token 单价均按实时推理价格的 50% 计费。[了解详情 →](/developer-guides/text-generation/batch)
- **上下文缓存** — 缓存命中的输入 token 享有折扣，具体折扣比例因模型而异。[了解详情 →](/developer-guides/run-and-scale/context-cache)
- **思考模式** — 思考 token 计入输出 token，按输出价格计费。[了解详情 →](/developer-guides/text-generation/thinking#计费说明)
- Batch 折扣和缓存折扣不能同时用于同一请求。

## 图像生成

按输入图像和成功生成的**图像张数**计费。未说明输入图像价格的模型，输入不计费，仅输出计费。

**计费公式**：

```
费用 = 输入图像单价 × 输入的图像张数 + 输出图像单价 × 输出的图像张数
```

**计费说明**：

- 部分模型按**输出图像分辨率**分档定价。
- 文生图无输入图像，不产生输入费用。
- 请求失败不产生任何费用，也不消耗免费额度。

<Accordion title="图像生成计费示例">
  假设某模型对输入图像和输出图像分别计费，输入单价为 0.02 元/张，输出单价按分辨率分档：1k 档 0.18 元/张、2k 档 0.50 元/张。

  **示例 1：图生图，输出 1k 分辨率，生成 1 张**

  - 输入费用：0.02 × 1 = 0.02 元
  - 输出费用：0.18 × 1 = 0.18 元
  - 合计：0.20 元

  **示例 2：文生图，输出 2k 分辨率，生成 2 张**

  文生图无输入图像，不产生输入费用：

  - 输出费用：0.50 × 2 = 1.00 元
  - 合计：1.00 元

  **示例 3：请求生成 4 张，仅 3 张成功**

  仅对成功生成的图像计费，失败的不收费。
</Accordion>

## 视频生成

输入不计费，输出按成功生成的**视频秒数**计费。

**计费公式**：

```
费用 = 视频单价 × 输出的视频时长（秒）
```

**计费说明**：

- 部分模型按**输出视频分辨率**定价（如 720P / 1080P 价格不同）。
- 部分模型按**输出视频模式**定价（如标准版 / 专业版价格不同）。
- 部分模型按**输出视频画幅**定价（如 1:1 / 3:4 价格不同）。
- 部分模型采用统一定价，与分辨率、模式或画幅无关。
- 请求失败不产生任何费用，也不消耗免费额度。

<Accordion title="视频生成计费示例">
  假设某模型 720P 单价为 0.60 元/秒。您请求生成一段视频，实际输出 5 秒：

  - 费用：0.60 × 5 = 3.00 元

  若该模型同时支持 1080P（单价 1.00 元/秒），同样生成 5 秒：

  - 费用：1.00 × 5 = 5.00 元
</Accordion>

## 文本转语音

按输入文本的**字符数**计费（每万字符），输出不计费。

**字符计算规则**：

- 一个汉字（含简体、繁体、日文汉字、韩文汉字）计为 2 个字符。
- 其他字符（英文字母、数字、标点、空格、日文假名、韩文字母）计为 1 个字符。
- 使用 SSML 时，SSML 标签本身不计入字符数，仅统计待合成的文本内容。

**示例**："你好"为 4 个字符（2+2）；"中A文123"为 8 个字符（2+1+2+1+1+1）。

## 语音转文本

按输入音频的**秒数**计费，输出不计费。适用于实时语音识别和录音文件识别。

## 语音对话

语音对话模型（Qwen-Omni 系列）支持文本、音频和图像/视频的输入与输出，按百万 token 计费，不同模态费率不同。

**多轮对话计费**：与文本模型一致，模型维护完整的对话上下文。历史对话内容会作为后续轮次的输入计费，因此每轮的输入 token 数会随对话轮次增加而逐步增长。

各模态的 token 转换规则因模型而异，详见 [Token 计算 →](/developer-guides/run-and-scale/token-counting)。

## 向量化与重排序

按百万输入 token 计费，输出不计费。

**影响计费的因素**：若模型支持 Batch 调用，输入 token 单价按实时推理价格的 50% 计费。

<a id="built-in-tools" />

## 内置工具

部分内置工具除模型 token 费用外，还会收取额外的调用费。

| 工具                                                       | 费用          | 备注           |
| -------------------------------------------------------- | ----------- | ------------ |
| [联网搜索](/developer-guides/tool-calling/web-search)        | 4 元 / 1K 次  | turbo 策略 3 元 |
| [网页抓取](/developer-guides/tool-calling/web-scraping)      | 免费          | 限时           |
| [代码解释器](/developer-guides/tool-calling/code-interpreter) | 免费          | 限时           |
| [文搜图](/developer-guides/tool-calling/image-search)       | 24 元 / 1K 次 |              |
| [图搜图](/developer-guides/tool-calling/image-search)       | 48 元 / 1K 次 |              |

[Function calling](/developer-guides/tool-calling/function-calling) 和 [MCP](/developer-guides/tool-calling/mcp) 不收取工具费——工具描述按输入 token 计费。

## 降低成本

- **Batch API** — 异步任务享 5 折优惠。[了解详情 →](/developer-guides/text-generation/batch)
- **上下文缓存** — 复用长 prompt，降低费用。[了解详情 →](/developer-guides/run-and-scale/context-cache)
- **模型选择** — 根据任务复杂度选择合适的模型。[模型对比 →](https://www.qianwenai.com/models)

更多计算示例和进阶策略，请参见[成本优化 →](/developer-guides/run-and-scale/cost-optimization)。

## 了解更多

- [免费额度](/resources/free-quota) — 资格与开通方式
- [成本优化](/developer-guides/run-and-scale/cost-optimization) — 进阶优化策略
- [Token Plan](/token-plan/overview) — AI 编程工具的订阅制方案（按 Credits 计费）
- [账单常见问题](/resources/faq-billing) — 常见问题解答
- [账单管理](/resources/bill-query) — 查看用量与发票
