# 发布应用到 Marketplace

> 将你的应用发布到 Dify Marketplace，与全世界分享

> 本文档由 AI 自动翻译。如有任何不准确之处，请参考 [英文原版](https://docs.dify.ai/en/cloud/use-dify/publish/publish-to-marketplace.md)。

将你的应用作为模板发布到 Dify Marketplace，让其他 Dify 用户可以发现和使用。

## 提交模板

若要发布模板，请通过 [创作者中心](https://creators.dify.ai) 提交。若只有你需要查看使用数据和反馈，请选择个人账户；若团队也需要访问，请选择组织。

提交后，模板进入 **Pending** 状态。通过审核后，即可发布到 Marketplace。

模板处于 **Pending** 状态时，可随时撤回。撤回后，模板将回到 **Draft** 状态，你可修改任意内容后重新提交。

> [!NOTE]
>
> 提交前：
>
> * 请确保应用中使用的所有插件都 **直接从 Marketplace 安装**。
> * 至少运行一次应用，确认其正常工作。

### 提交方式

> [tab] 从 Dify Studio
>
> 在应用内部，点击 **发布** > **发布更新**，然后点击 **发布到 Marketplace**。
>
> 随后跳转到创作者中心，应用已自动上传，其中不含 Secret 类型环境变量的值。填写模板详情并提交审核即可。

> [tab] 从创作者中心
>
> 1. [导出应用](../%E5%B7%A5%E4%BD%9C%E7%A9%BA%E9%97%B4/%E5%AF%BC%E5%87%BA%E5%92%8C%E5%AF%BC%E5%85%A5%E5%BA%94%E7%94%A8.md#export-an-app)，导出时不勾选 **导出 secret 值**，因为任何人都能下载你上传的应用包。
>
> 2. 在创作者中心上传 `.ifpkg` 应用包（最大 10 MB），填写模板详情并提交审核。
>
>    如果应用包超过 10 MB，可按需采用以下方法精简应用，然后重新导出。
>
>    * 删除不需要的节点和连线。
>    * 精简过长的提示词、代码、模板文本、HTTP 请求正文或变量值。
>    * 如果应用是 Agent 或用到了 Agent 节点，删掉其中不需要的 Skill 和文件。

### 模板填写指南

#### 模板名称和图标

仅从名称，用户就应该知道它在哪里运行以及做什么。

* 使用简短、清晰的名称。
* 推荐模式：\[渠道 / 目标] + \[核心任务]，例如：
  * WeChat Customer Support Bot
  * CSV Data Analyzer with Natural Language
  * Internal Docs Q\&A Assistant
  * GitHub Issue Triage Agent
* 包含用户可能搜索的关键词：渠道名称 (Slack, WeChat, Email, Notion) 和任务名称 (Summarizer, Assistant, Generator, Bot)。
* 使用一个能清楚反映模板主题和用途的图标，而不是默认头像。

#### 分类

帮助用户在浏览或按分类筛选时发现你的模板。

* 仅选择 **1～3** 个最能描述你模板的分类。
* 不要为了增加曝光而勾选所有分类。

#### 语言

帮助用户通过语言筛选找到你的模板。

* 选择模板使用的语言，并在模板名称、概述和设置步骤中使用相同语言。
* 发布多种语言版本时，每种语言需分别提交一个模板。

#### 概述

用 2～4 句话说明它做什么以及面向谁。

> [!NOTE]
>
> 你无需在此列出先决条件、输入或输出。

**推荐结构**

1. 第 1 句：**它做什么**

   一句话概括主要功能。
2. 第 2～3 句：**面向谁、什么场景**

   典型用户角色或场景（客服团队、营销人员、创始人、个人知识工作者等）。

> [accordion] 示例：Stock Investment Analysis Copilot 的概述
>
> This template creates a stock investment analysis copilot that uses Yahoo Finance tools to fetch news, analytics, and ticker data for any listed company.
>
> It helps investors and analysts quickly generate structured research summaries, compare companies, and prepare reports without manually switching between multiple finance websites.

#### 设置步骤

将设置步骤写成 Markdown 编号列表（1., 2., 3.），每一步简要说明一个操作。

新用户只需按照这些步骤操作，即可在几分钟内让模板运行起来。

**撰写原则**

1. 按照实际设置顺序，通常为：
   1. 使用/导入模板
   2. 连接账户 / 添加 API 密钥
   3. 连接数据源（文档、数据库、表格等）
   4. 可选自定义（助手名称、语气、过滤器）
   5. 激活工作流并运行测试

2. 每一步应回答：
   * 在界面中点击哪里
   * 需要配置或填写什么

3. 目标 3～8 步。太少显得不完整，太多则会令人生畏。

> [accordion] 示例：Stock Investment Analysis Copilot (Yahoo Finance) 的设置步骤
>
> 1. Click **Use template** to copy the "Investment Analysis Copilot (Yahoo Finance)" agent into your workspace.
>
> 2. Go to **Integrations** > **Model Provider** and add your LLM API key. For example, OpenAI, Anthropic, or another supported provider.
>
> 3. Open the agent's **Orchestrate** page and make sure the Yahoo Finance tools are enabled in the **Tools** section:
>
> * `yahoo Analytics`
>
> * `yahoo News`
>
> * `yahoo Ticker`
>
> 4. (Optional) Customize the analysis style:
>    * In the **INSTRUCTIONS** area, adjust the system prompt to match your target users. For example, tone, report length, preferred language, or risk preference.
>    * Update the suggested questions in the **Debug & Preview** panel if you want different example queries.
> 5. Click **Publish** to make the agent available, then use the preview panel to test it:
>    * Enter a company name or ticker (e.g., `Nvidia`, `AAPL`, `TSLA`).
>    * Confirm that the copilot calls the Yahoo Finance tools and returns a structured investment analysis report.

#### 提交前快速检查清单

* 名称是简短的短语，能清楚地说明它在哪里运行、做什么。
* 概述用 2～4 句话解释价值和典型用例。
* 仅选择了 1～3 个相关分类。
* 设置步骤是清晰的编号列表。
* 整个模板均使用所选语言。

## 查看模板使用情况和反馈

模板发布后，可在 [**模板**](https://creators.dify.ai/dashboard/templates) 页面查看使用总数、整体评分、评分数量和点赞总数。如需逐条查看评分、点赞和反馈消息，请打开 [**消息**](https://creators.dify.ai/dashboard/inbox)。

## 更新已发布的模板

更新已发布的模板时，具体方法取决于你要修改的内容。

* **修改应用本身**（如提示词、工具、模型设置等）

  将更新后的应用作为新模板提交。这会生成一个独立的模板，而非替换原有模板；新模板发布后，你可手动下架旧版本。

* **仅修改展示内容**（如概述或设置步骤）

  下架模板，使其进入 **Delisted** 状态。完成修改后，重新提交审核。
