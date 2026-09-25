> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 深入研究 (Qwen-Deep-Research)

> 自动化多步研究与网络搜索

面对复杂研究课题，传统的手动搜索耗时费力，而大模型结合联网搜索的功能也往往难以进行深度、系统的分析。深入研究模型（Qwen-Deep-Research）能自动规划研究步骤、执行多轮的深入搜索与信息整合，并最终生成一份结构化的研究报告。

## 快速开始

您需要已[获取API Key](/api-reference/preparation/api-key)并[配置API Key到环境变量](/api-reference/preparation/export-api-key-env)。如果通过SDK调用，还需要[安装DashScope SDK](/api-reference/preparation/install-sdk)。

模型采用两步式工作流程：反问确认（明确研究范围）和深入研究（执行搜索并生成报告）。以下示例展示了包含两个步骤的完整调用流程。

<Note>
  模型目前仅可通过 DashScope SDK 调用，暂不支持 Java 版 DashScope SDK，也不支持 OpenAI 兼容接口调用。
</Note>

<CodeGroup>
  ```python Python
  import os
  import dashscope

  # 配置API Key
  # 若没有配置环境变量，请用千问AI平台API Key将下行替换为：API_KEY = "sk-xxx"
  API_KEY = os.getenv('DASHSCOPE_API_KEY')

  def call_deep_research_model(messages, step_name):
    print(f"\n=== {step_name} ===")

    try:
      responses = dashscope.Generation.call(
        api_key=API_KEY,
        model="qwen-deep-research",
        messages=messages,
        # qwen-deep-research模型目前仅支持流式输出
        stream=True
        # incremental_output=True 使用增量输出请添加此参数
      )

      return process_responses(responses, step_name)

    except Exception as e:
      print(f"调用API时发生错误: {e}")
      return ""

  # 显示阶段内容
  def display_phase_content(phase, content, status):
    if content:
      print(f"\n[{phase}] {status}: {content}")
    else:
      print(f"\n[{phase}] {status}")

  # 处理响应
  def process_responses(responses, step_name):
    current_phase = None
    phase_content = ""
    research_goal = ""
    web_sites = []
    references = []
    keepalive_shown = False  # 标记是否已经显示过KeepAlive提示

    for response in responses:
      # 检查响应状态码
      if hasattr(response, 'status_code') and response.status_code != 200:
        print(f"HTTP返回码：{response.status_code}")
        if hasattr(response, 'code'):
          print(f"错误码：{response.code}")
        if hasattr(response, 'message'):
          print(f"错误信息：{response.message}")
        print("请参考文档：/api-reference/preparation/error-messages")
        continue

      if hasattr(response, 'output') and response.output:
        message = response.output.get('message', {})
        phase = message.get('phase')
        content = message.get('content', '')
        status = message.get('status')
        extra = message.get('extra', {})

        # 阶段变化检测
        if phase != current_phase:
          if current_phase and phase_content:
            # 根据阶段名称和步骤名称来显示不同的完成描述
            if step_name == "第一步：模型反问确认" and current_phase == "answer":
              print(f"\n 模型反问阶段完成")
            else:
              print(f"\n {current_phase} 阶段完成")
          current_phase = phase
          phase_content = ""
          keepalive_shown = False  # 重置KeepAlive提示标记

          # 根据阶段名称和步骤名称来显示不同的描述
          if step_name == "第一步：模型反问确认" and phase == "answer":
            print(f"\n 进入模型反问阶段")
          else:
            print(f"\n 进入 {phase} 阶段")

        # 处理Answer阶段的references信息
        if phase == "answer":
          if extra.get('deep_research', {}).get('references'):
            new_references = extra['deep_research']['references']
            if new_references and new_references != references:  # 避免重复显示
              references = new_references
              print(f"\n   引用来源 ({len(references)} 个):")
              for i, ref in enumerate(references, 1):
                print(f"     {i}. {ref.get('title', '无标题')}")
                if ref.get('url'):
                  print(f"        URL: {ref['url']}")
                if ref.get('description'):
                  print(f"        描述: {ref['description'][:100]}...")
                print()

        # 处理WebResearch阶段的特殊信息
        # 注意：qwen-deep-research-2025-12-15模型使用streamingThinking状态
        # 替代streamingQueries和streamingWebResult
        if phase == "WebResearch":
          if extra.get('deep_research', {}).get('research'):
            research_info = extra['deep_research']['research']

            # 处理streamingThinking（快照模型）或streamingQueries（主线模型）状态
            if status in ("streamingThinking", "streamingQueries"):
              if 'researchGoal' in research_info:
                goal = research_info['researchGoal']
                if goal:
                  research_goal += goal
                  print(f"\n   研究目标: {goal}", end='', flush=True)

            # 处理streamingWebResult状态（主线模型）
            # 快照模型使用streamingThinking合并了此状态
            elif status == "streamingWebResult":
              if 'webSites' in research_info:
                sites = research_info['webSites']
                if sites and sites != web_sites:  # 避免重复显示
                  web_sites = sites
                  print(f"\n   找到 {len(sites)} 个相关网站:")
                  for i, site in enumerate(sites, 1):
                    print(f"     {i}. {site.get('title', '无标题')}")
                    print(f"        描述: {site.get('description', '无描述')[:100]}...")
                    print(f"        URL: {site.get('url', '无链接')}")
                    if site.get('favicon'):
                      print(f"        图标: {site['favicon']}")
                    print()

            # 处理WebResultFinished状态
            elif status == "WebResultFinished":
              print(f"\n   网络搜索完成，共找到 {len(web_sites)} 个参考信息源")
              if research_goal:
                print(f"   研究目标: {research_goal}")

        # 累积内容并显示
        if content:
          phase_content += content
          # 实时显示内容
          print(content, end='', flush=True)

        # 显示阶段状态变化
        if status and status != "typing":
          print(f"\n   状态: {status}")

          # 显示状态说明
          if status == "streamingThinking":
            print("   → 正在拆解研究任务并总结网页内容（WebResearch阶段）")
          elif status == "streamingQueries":
            print("   → 正在生成研究目标和搜索查询（WebResearch阶段）")
          elif status == "streamingWebResult":
            print("   → 正在执行搜索、网页阅读和代码执行（WebResearch阶段）")
          elif status == "WebResultFinished":
            print("   → 网络搜索阶段完成（WebResearch阶段）")

        # 当状态为finished时，显示token消耗情况
        if status == "finished":
          if hasattr(response, 'usage') and response.usage:
            usage = response.usage
            print(f"\n    Token消耗统计:")
            print(f"      输入tokens: {usage.get('input_tokens', 0)}")
            print(f"      输出tokens: {usage.get('output_tokens', 0)}")
            print(f"      请求ID: {response.get('request_id', '未知')}")

        if phase == "KeepAlive":
          # 只在第一次进入KeepAlive阶段时显示提示
          if not keepalive_shown:
            print("当前步骤已经完成，准备开始下一步骤工作")
            keepalive_shown = True
          continue

    if current_phase and phase_content:
      if step_name == "第一步：模型反问确认" and current_phase == "answer":
        print(f"\n 模型反问阶段完成")
      else:
        print(f"\n {current_phase} 阶段完成")

    return phase_content

  def main():
    # 检查API Key
    if not API_KEY:
      print("错误：未设置 DASHSCOPE_API_KEY 环境变量")
      print("请设置环境变量或直接在代码中修改 API_KEY 变量")
      return

    print("用户发起对话：研究一下人工智能在教育中的应用")

    # 第一步：模型反问确认
    # 模型会分析用户问题，提出细化问题来明确研究方向
    messages = [{'role': 'user', 'content': '研究一下人工智能在教育中的应用'}]
    step1_content = call_deep_research_model(messages, "第一步：模型反问确认")

    # 第二步：深入研究
    # 基于第一步的反问内容，模型会执行完整的研究流程
    messages = [
      {'role': 'user', 'content': '研究一下人工智能在教育中的应用'},
      {'role': 'assistant', 'content': step1_content},  # 包含模型的反问内容
      {'role': 'user', 'content': '我主要关注个性化学习和智能评估这两个方面'}
    ]

    call_deep_research_model(messages, "第二步：深入研究")
    print("\n 研究完成！")

  if __name__ == "__main__":
    main()
  ```

  ```bash curl
  echo "第一步：模型反问确认"
  curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation' \
  --header 'X-DashScope-SSE: enable' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
      "input": {
          "messages": [
              {
                  "content": "研究一下人工智能在教育中的应用",
                  "role": "user"
              }
          ]
      },
      "model": "qwen-deep-research"
  }'

  echo -e "\n\n"
  echo "第二步：深入研究"
  curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation' \
  --header 'X-DashScope-SSE: enable' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
      "input": {
          "messages": [
              {
                  "content": "研究一下人工智能在教育中的应用",
                  "role": "user"
              },
              {
                  "content": "请告诉我您希望重点研究人工智能在教育中的哪些具体应用场景？",
                  "role": "assistant"
              },
              {
                  "content": "我主要关注个性化学习方面",
                  "role": "user"
              }
          ]
      },
      "model": "qwen-deep-research"
  }'
  ```
</CodeGroup>

## 模型列表

| 模型名称                          | 上下文长度 (Token) | 最大输入 (Token) | 最大输出 (Token) |
| ----------------------------- | ------------- | ------------ | ------------ |
| qwen-deep-research            | 1,000,000     | 997,952      | 32,768       |
| qwen-deep-research-2025-12-15 | 1,000,000     | 997,952      | 32,768       |

<Note>
  `qwen-deep-research`为主线模型，持续更新优化。`qwen-deep-research-2025-12-15`为快照版本，在研究深度和报告质量上更优，且额外支持**MCP 工具调用**能力。两个模型均支持**图片输入**。两者独立计费。
</Note>

## 核心能力

模型通过 `phase` 和 `status` 字段展示工作流程。`phase` 表示当前执行的核心任务，`status` 表示该任务的内部进度。

**反问确认与报告生成 (phase: "answer")**

模型分析用户初始问题，提出细化问题确认研究范围。在生成最终报告时，此阶段复用。

状态变化：

- `typing`: 正在生成文本内容
- `finished`: 文本内容生成完毕

**研究规划 (phase: "ResearchPlanning")**

根据用户需求制定研究大纲。

状态变化：

- `typing`: 正在生成研究计划
- `finished`: 研究计划制定完成

**网络搜索 (phase: "WebResearch")**

执行多轮搜索并处理信息。每轮搜索结束时返回`WebResultFinished`状态，整个阶段结束后返回`finished`状态。

状态变化：

- `streamingThinking`: 正在拆解研究任务并总结网页内容（`qwen-deep-research-2025-12-15`模型专用，替代`streamingQueries`和`streamingWebResult`）
- `streamingQueries`: 正在生成搜索查询词（仅`qwen-deep-research`模型）
- `streamingWebResult`: 正在执行网络搜索并分析网页内容（仅`qwen-deep-research`模型）
- `WebResultFinished`: 单轮搜索结束
- `finished`: 网络搜索阶段整体完成

**连接保持 (phase: "KeepAlive")**

在长任务间隙发送，维持连接。此阶段不包含业务内容，可忽略。

## 图片输入

深入研究模型支持在用户消息中传入图片，模型能理解图片内容并结合图片进行深入研究分析。传入图片时，`content`字段需使用数组格式，包含`image`和`text`对象。

- 支持 JPEG、PNG、BMP、WEBP 等常见格式，单张图片不超过 10MB。
- 单次请求最多传入 5 张图片，支持公网 URL 和 Base64 编码两种传入方式。
- 响应格式与纯文本请求一致，模型会结合图片内容进行研究并返回报告。

**请求示例**

<CodeGroup>
  ```python Python
  import os
  import dashscope

  API_KEY = os.getenv('DASHSCOPE_API_KEY')

  messages = [
    {
      "role": "user",
      "content": [
        {"image": "https://example.com/example.png"},
        {"text": "分析这张图表中的数据趋势，并对关键发现进行深入研究"}
      ]
    }
  ]

  responses = dashscope.Generation.call(
    api_key=API_KEY,
    model="qwen-deep-research",
    messages=messages,
    stream=True
  )

  for response in responses:
    if hasattr(response, 'output') and response.output:
      message = response.output.get('message', {})
      content = message.get('content', '')
      if content:
        print(content, end='', flush=True)
  ```

  ```bash curl
  curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation' \
  --header 'X-DashScope-SSE: enable' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
      "input": {
          "messages": [
              {
                  "content": [
                      {"image": "https://example.com/example.png"},
                      {"text": "分析这张图表中的数据趋势，并对关键发现进行深入研究"}
                  ],
                  "role": "user"
              }
          ]
      },
      "model": "qwen-deep-research"
  }'
  ```
</CodeGroup>

## MCP 工具调用

<Note>
  MCP 工具调用仅`qwen-deep-research-2025-12-15`模型支持，主线模型`qwen-deep-research`不支持此功能。
</Note>

`qwen-deep-research-2025-12-15`模型支持通过`research_tools`参数接入 MCP（Model Context Protocol）服务，使模型在研究过程中能够调用外部工具进行信息检索。响应格式与标准调用一致，模型会在 WebResearch 阶段通过 MCP Server 调用指定工具。

<Note>
  `research_tools`的完整参数说明和 MCP 工具规范请参考 [API 参考文档](/api-reference/specialized-models/deep-research-api)。
</Note>

### 请求示例

<CodeGroup>
  ```python Python
  import os
  import dashscope

  API_KEY = os.getenv('DASHSCOPE_API_KEY')

  messages = [
    {
      "role": "user",
      "content": "使用知识库搜索近期发布的产品更新公告，并整理成研究报告"
    }
  ]

  responses = dashscope.Generation.call(
    api_key=API_KEY,
    model="qwen-deep-research-2025-12-15",
    messages=messages,
    stream=True,
    enable_feedback=False,
    research_tools=[{
      "type": "mcp",
      "server_label": "my-server",
      "server_url": "https://your-mcp-server.example.com/sse",
      "allowed_tools": ["search", "fetch"],
      "authentication": {
        "bearer": "your_jwt_token_here"
      }
    }]
  )

  for response in responses:
    if hasattr(response, 'output') and response.output:
      message = response.output.get('message', {})
      content = message.get('content', '')
      if content:
        print(content, end='', flush=True)
  ```

  ```bash curl
  curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation' \
  --header 'X-DashScope-SSE: enable' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
      "input": {
          "messages": [
              {
                  "content": "使用知识库搜索近期发布的产品更新公告，并整理成研究报告",
                  "role": "user"
              }
          ]
      },
      "model": "qwen-deep-research-2025-12-15",
      "parameters": {
          "enable_feedback": false,
          "research_tools": [{
              "type": "mcp",
              "server_label": "my-server",
              "server_url": "https://your-mcp-server.example.com/sse",
              "allowed_tools": ["search", "fetch"],
              "authentication": {
                  "bearer": "your_jwt_token_here"
              }
          }]
      }
  }'
  ```
</CodeGroup>

## 计费说明

<Note>
  以下价格为目录价。具体优惠活动及折扣价格请前往[模型市场](https://www.qianwenai.com/models)查看。
</Note>

| 模型名称                          | 输入成本 (每千Token) | 输出成本 (每千Token) |
| ----------------------------- | -------------- | -------------- |
| qwen-deep-research            | 0.054元         | 0.163元         |
| qwen-deep-research-2025-12-15 | 0.079元         | 0.236元         |

**计费方式**：计费基于输入和输出Token总量。输入Token包含用户消息内容和模型内置的系统提示词。输出Token包含反问确认、研究计划、研究目标、搜索查询和最终研究报告等所有生成内容。

## 应用于生产环境

**流式输出处理**

模型仅支持流式输出（`stream=True`）。处理响应时需正确解析 `phase` 和 `status` 字段，判断当前阶段和完成状态。

**错误处理**

检查响应状态码，非200状态需处理错误。流式响应早期阶段某些响应块可能只包含元数据，后续块会包含实际内容。

**Token消耗监控**

在 `status` 为 `finished` 时，通过 `response.usage` 获取Token消耗统计，包括输入Tokens、输出Tokens和请求ID。

**连接管理**

模型可能在长任务间隙发送 `KeepAlive` 阶段响应，用于维持连接。可忽略此阶段内容，继续处理后续响应。

## 常见问题

<Accordion title="为什么某些响应块的output为空？">
  在流式响应的早期阶段，某些响应块可能只包含元数据信息，后续块会包含实际内容。
</Accordion>

<Accordion title="如何判断某个阶段是否完成？">
  当 `status` 字段变为 "finished" 时，表示当前阶段完成。
</Accordion>

<Accordion title="模型是否支持OpenAI兼容接口调用？">
  模型目前暂不支持通过OpenAI兼容接口调用。
</Accordion>

<Accordion title="模型的输入与输出Token数量是如何计算的？">
  输入Token包含用户发送的消息内容和模型内置的系统提示词，包括用户问题、用户回答和系统提示词。输出Token包含模型在整个研究过程中生成的所有内容，包括反问确认内容、研究计划、研究目标、搜索查询和最终研究报告。
</Accordion>

<Accordion title="qwen-deep-research 和 qwen-deep-research-2025-12-15 有什么区别？">
  `qwen-deep-research`是主线模型，持续更新。`qwen-deep-research-2025-12-15`是快照版本，效果更优，额外支持 MCP 工具调用能力。两个模型均支持图片输入。两者独立计费，快照版本的价格略高于主线版本。
</Accordion>

<Accordion title="如何传入图片进行研究？">
  将`content`字段设为数组格式，包含`{"image": "图片URL"}`和`{"text": "文本描述"}`。两个模型均支持图片输入。
</Accordion>

<Accordion title="如何跳过反问确认，让模型直接进入研究？">
  在`parameters`中设置`enable_feedback`为`false`即可跳过反问确认阶段，模型将直接进入研究流程。
</Accordion>

## API参考

关于Qwen-Deep-Research模型的输入与输出参数，请参考 [API 参考文档](/api-reference/specialized-models/deep-research-api)。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](/api-reference/preparation/error-messages)进行解决。

## 限流

模型限流触发条件请参考：[限流](/developer-guides/administration/rate-limits)。
