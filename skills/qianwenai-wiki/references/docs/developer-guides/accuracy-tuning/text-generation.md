> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 文本生成微调

> 设计高效的提示词

## 设计高效的提示词

### 指令要清晰、具体

模糊的提示词只能得到模糊的结果。你提供的上下文和约束越多，输出就越符合预期。就像把任务交给同事：一句话的描述留下了太多的理解空间，而详细的说明加上明确的目标，则能产出准确的结果。

<Note>
  清晰、具体的提示词是从大语言模型获得有用输出的最关键因素。
</Note>

**示例：代码生成任务**

| **模糊的提示词**          | **清晰、具体的提示词**                                                                                     |
| ------------------- | ------------------------------------------------------------------------------------------------- |
| 写一个处理数据的 Python 函数。 | 写一个 Python 函数，读取 CSV 文件，筛选 `status` 列为 `"active"` 的行，返回字典列表。要求：添加类型注解，处理文件不存在的情况，使用标准库的 `csv` 模块。 |

具体的提示词定义了输入格式、预期输出、错误处理方式和库的约束，足以让模型一次生成可用的代码。

**示例：内容生成任务**

| **模糊的提示词**   | **清晰、具体的提示词**                                                                            |
| ------------ | ---------------------------------------------------------------------------------------- |
| 帮我写一篇产品发布公告。 | 为千问AI平台推出的轻薄便携手机"Zephyr Z9"写一篇 200 字的产品发布公告。重点突出超薄设计、高性能配置和易用性。目标受众是社交媒体上的科技爱好者，语气要简洁有力。 |

### 用框架组织提示词

提示词框架帮助你系统性地提供大语言模型所需的信息。无需凭感觉决定写什么，直接用以下六个要素作为检查清单：

<img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/0027203771/CAEQQhiBgMCLuM3KwBkiIDZhYThlZjE3NGI3NzQ3ZDliODMwODViZmVjOWE0MGFm4577910_20240815141024.521.svg" alt="提示词框架图" width="800" />

| **要素**            | **作用**     | **示例**                              |
| ----------------- | ---------- | ----------------------------------- |
| **上下文（Context）**  | 与任务相关的背景信息 | "你正在审查一个 Python 微服务的 Pull Request。" |
| **目标（Objective）** | 需要完成的具体任务  | "找出潜在的 bug 并给出修复建议。"                |
| **风格（Style）**     | 写作风格或角色设定  | "以资深后端工程师的身份撰写。"                    |
| **语气（Tone）**      | 输出的情感特质    | "专业但有建设性。"                          |
| **受众（Audience）**  | 读者是谁       | "团队中的初级开发人员。"                       |
| **格式（Response）**  | 期望的输出格式    | "按编号列出问题，附代码修改建议。"                  |

用 `#` 分隔符标记提示词中的各个部分：

```plaintext
#Context#
你正在审查一个 Python 微服务的 Pull Request，
该代码库使用 FastAPI 和 SQLAlchemy。

#Objective#
审查以下代码 diff，找出潜在的安全漏洞、
性能问题和代码风格违规。

#Style#
以资深后端工程师进行代码审查的方式撰写。

#Tone#
专业但有建设性——解释每个问题为什么重要。

#Audience#
正在学习安全编码实践的初级开发人员。

#Response#
按编号列出发现的问题。每个问题包括：
- 具体的代码行或代码块
- 为什么这是个问题
- 修复建议（附代码）
```

<Note>
  并非每个提示词都需要全部六个要素。根据任务灵活调整。本指南中的示例根据不同场景使用了不同的要素组合。
</Note>

## 优化提示词

### 提供输出示例

附上期望输出的示例，帮助模型匹配你要求的格式、风格和详细程度。这种方法称为少样本提示（few-shot prompting），还能提升多次运行结果的一致性。

**示例：结构化数据提取**

```plaintext
#Context#
从用户工单中提取结构化信息。

#Objective#
将每个工单解析为 JSON 对象。

#Examples#
Input: "My order #12345 arrived damaged. I want a refund."
Output:
{
  "order_id": "12345",
  "issue_type": "damaged_item",
  "requested_action": "refund"
}

Input: "I can't log in to my account. I've tried resetting my password
twice."
Output:
{
  "order_id": null,
  "issue_type": "login_failure",
  "requested_action": "account_recovery"
}

#Task#
Now parse this ticket:
Input: "Order #67890 has been stuck in 'processing' for 5 days.
Please expedite or cancel it."
```

模型从示例中学习了 JSON 的结构、字段命名规范，以及如何从自然语言中推断 `issue_type` 和 `requested_action`——全靠示例本身。

### 将复杂任务拆分为步骤

对于复杂任务，为模型定义明确的执行步骤，而不仅仅是描述期望结果。逐步说明可以防止模型跳过中间推理。

**示例：数学应用题**

```plaintext
#Context#
小明早上 8:00 出门步行上学，速度为每分钟 50 米。
12 分钟后，爸爸发现他忘带作业，骑自行车追赶，
速度为每分钟 200 米。追上后，爸爸用自行车载小明
继续前行。自行车行驶的距离是步行距离的 5 倍。

#Objective#
计算到达时间。

#Steps#
1. 计算爸爸追上小明时，小明已经走了多远。
2. 计算爸爸追上小明用了多长时间。
3. 计算剩余的自行车路程和行驶时间。
4. 将所有时间加总，得出到达时间。
```

**模型输出（按步骤推理）**：

```plaintext
第 1 步：爸爸出发前，小明已经走了 12 分钟：
  12 分钟 × 50 米/分钟 = 600 米（领先距离）

第 2 步：爸爸的相对速度：200 - 50 = 150 米/分钟
  追赶时间：600 米 ÷ 150 米/分钟 = 4 分钟
  小明又走了：4 分钟 × 50 米/分钟 = 200 米
  步行总距离：600 + 200 = 800 米

第 3 步：自行车距离：800 米 × 5 = 4000 米
  自行车时间：4000 米 ÷ 200 米/分钟 = 20 分钟

第 4 步：总时间：12 + 4 + 20 = 36 分钟
  到达时间：8:00 + 36 分钟 = 8:36
```

如果没有 `#Steps#` 部分，模型可能会跳过中间计算，得出错误答案。

### 用分隔符区分内容

当提示词包含多个内容块——指令、输入数据和示例——使用分隔符标记清晰的边界。这能帮助模型区分你的指令和需要处理的内容。

选择自然语言中很少出现的字符序列：`###`、`===` 或 `>>>`。

**示例：文本摘要**

```plaintext
分别总结以下影评的每个段落，每段生成一句摘要。

###
张志强曾经意气风发，但生活的压力让他偏离了轨道。
中年时一个冲动的决定，让他从家人的骄傲变成了
社会的边缘人。
###
这只是开始。一连串意想不到的事件迫使他面对自己。
他选择从外卖骑手做起，穿梭在城市街头，
重新构建自己的生活。
###
在这条路上，他找到了志同道合的伙伴。
在共同的奋斗中，他重新找回了勇气和方向，
为人生开辟了新的道路。
###
```

如果没有分隔符，模型会把整篇影评当作一个整体，生成一段笼统的总结。有了分隔符，模型能识别出三个独立段落，分别生成三段与叙事脉络一致的摘要。

### 引导模型逐步推理

对于涉及逻辑、数学或多步分析的任务，让模型在给出结论之前展示推理过程。以下是两种有效方法：

#### 思维链（Chain of Thought, CoT）

CoT 是一种相对简单的方法，能显著提升大语言模型在复杂场景下的推理能力。要求模型先解释思考过程，再给出最终答案。

**示例：JSON 校验**

```plaintext
#Context#
JSON 输入：
{"web-app": {
  "servlet": [
    {
      "servlet-name": "cofaxEmail",
      "servlet-class": "org.cofax.cds.EmailServlet",
      "init-param": {
        "mailHost": "mail1",
        "mailHostOverride": "mail2"}},
    {
      "servlet-name": "cofaxTools",
      "servlet-class": "org.cofax.cms.CofaxToolsServlet",
      "init-param": {
        "templatePath": "toolstemplates/",
        "log": 1,
        "logLocation": "/usr/local/tomcat/logs/CofaxTools.log",
        "logMaxSize": ""}}],
  "servlet-mapping": {
    "cofaxEmail": "/cofaxutil/aemail/*",
    "cofaxTools": "/tools/*"},
  "taglib": {
    "taglib-uri": "cofax.tld",
    "taglib-location": "/WEB-INF/tlds/cofax.tld"}}}

#Objective#
验证此 JSON 是否满足以下三个要求：
1. 每个 servlet 都有 init-param 块。
2. servlet-mapping 中的每个键都与某个 servlet-name 匹配。
3. cofaxTools servlet 恰好有 3 个以 "log" 开头的参数，
   且 "log" 参数的值小于 10。

#Response#
先逐条解释你的推理过程，然后说明是否满足所有要求。
```

添加"解释你的推理过程"后，模型会逐条分析每个要求，捕捉到仅回答"是/否"时容易遗漏的边界情况（如 `logMaxSize` 的值为空字符串）。

#### 提示链（Prompt Chaining）

将复杂问题拆分为一系列简单的问题，通过多轮对话逐步完成。每一轮的回答作为下一轮问题的输入，引导模型沿着可控的推理路径前进。

提示链的设置比 CoT 更费时，但效果更好、准确率更高。它特别适合逻辑复杂但可以按固定模式拆解的任务。

**示例：多步数学题（同一道小明问题，三轮对话）**

**第 1 轮**：

```plaintext
#Context#
小明早上 8:00 出门，步行速度为 50 米/分钟。
12 分钟后，爸爸骑自行车追赶，速度为 200 米/分钟。
自行车行驶距离是步行距离的 5 倍。

#Question#
爸爸什么时候追上小明？小明此时走了多远？
```

**模型回答**： "爸爸在 8:16 追上小明，此时小明已步行 800 米。"

**第 2 轮**：

```plaintext
小明骑自行车到爷爷家还需要走多远？
```

**模型回答**： "自行车距离 = 800 米 × 5 = 4000 米。"

**第 3 轮**：

```plaintext
小明几点到达？
```

**模型回答**： "自行车时间 = 4000 米 ÷ 200 米/分钟 = 20 分钟。总时间 = 16 + 20 = 36 分钟。到达时间：8:36。"

每一轮都基于已验证的中间结果，减少了错误累积的风险。

<Tip>
  其他推理技术包括思维树（Tree of Thoughts, ToT）和思维增强（Boosting of Thoughts）。根据任务的复杂度和准确率要求选择合适的方法。
</Tip>

## 测试与迭代

提示词工程是一个迭代过程。第一版提示词很少能产出最佳结果。

<img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/0027203771/CAEQQhiBgIDMvqXKwBkiIDA3MzFkYzg0YzFiYzQ3ZTZhNTI1MDkwODU5NGIyODUw4789852_20241122171352.128.svg" alt="提示词迭代流程图" width="800" />

按照以下流程进行：

1. **明确目标。** 在写提示词之前，先确定什么样的输出算是好的。
2. **编写初始提示词。** 运用本指南介绍的方法：具体明确、使用框架、提供示例。
3. **用多样化的输入测试。** 在多个真实场景中运行提示词，包括边界情况。
4. **分析失败案例。** 找出输出不达标的原因：格式错误、信息缺失、推理错误，还是语气不一致。
5. **改进提示词。** 每次只调整一个要素，以便衡量每项改动的效果。
6. **重复迭代。** 持续优化，直到输出稳定达到质量标准。

除了提示词设计本身，用户反馈也至关重要。将提示词部署到生产环境后，持续监控用户的实际交互，根据用户纠正的规律和未预料到的边界情况不断改进。

## 示例：优化多语言 HR 助手

**背景**： 一个基于 qwen-plus 的多语言 HR 助手未能始终用用户使用的语言回复。系统提示词需要重新组织。

### 优化前

```plaintext
# Role
You are an efficient HR AI assistant, specifically responsible for
answering company internal questions about policies, attendance
systems, annual leave arrangements, and other related issues.

## Skills
### Skill 1: Policy interpretation
- Accurately interpret company policy documents and provide clear,
  concise policy explanations to colleagues.

### Skill 2: Attendance Q&A
- Answer all questions related to employee attendance, including
  clock-in rules, handling of late arrivals and early departures,
  leave procedures, etc.

### Skill 3: Annual leave management consultation
- Explain annual leave application conditions, accumulation rules,
  validity period, and approval process.

## Limitations
- Respond in the same language as the user's question.
- Limited to HR-related questions.
- Do not involve queries of personal privacy data.
```

**问题**：

- 结构松散，`## Limitations` 部分冗余
- `${documents}` 知识库内容内联嵌入，模型难以区分指令和参考内容
- 语言匹配的要求被埋在限制条件中

### 优化后

```plaintext
#Context#
You are an HR AI assistant for a multinational company. You answer
questions about policy interpretation, attendance rules, and annual
leave management.

Below are the company policy documents:
======
${documents}
======

#Objective#
1. Only answer questions about policy interpretation, attendance,
   and annual leave.
2. When a question is in scope but the knowledge base does not cover
   it, direct the user to contact the HR department.
3. For each category, follow these guidelines:
   - Policy interpretation: Locate the relevant clause and provide
     a clear, concise explanation.
   - Attendance: Cover clock-in rules, late arrival handling, and
     leave procedures.
   - Annual leave: Explain eligibility, accrual rules, approval
     process, and help calculate remaining balance.
4. Do not access or disclose personal employee data.

#Multilingual requirements#
- If the question is not in Chinese, translate it to Chinese to
  search the knowledge base, then convert the retrieved content
  back to the question's language for output.

#Response#
- Use only standard ASCII characters in all output.
- Match the output language to the input language.
```

**改进要点**：

- **应用框架。** 使用 `#Context#`、`#Objective#`、`#Multilingual requirements#` 和 `#Response#` 重新组织结构。
- **添加分隔符。** 用 `======` 分隔符包裹 `${documents}`，将参考数据与指令分开。
- **约束分散到对应部分。** 将语言规则移至 `#Multilingual requirements#`，将范围限制移至 `#Objective#`。

这些改动解决了语言一致性问题。模型能清楚地识别出多语言指令是一条独立的、高优先级的规则，而非被埋没在末尾的附带说明。
