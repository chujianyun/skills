> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 显式缓存最佳实践

> 显式缓存通过在请求中添加缓存标记，确保相同输入内容确定性命中缓存，从而显著降低成本和延迟。

本文介绍显式缓存的使用方法和最佳实践。显式缓存通过在请求中添加缓存标记，确保相同输入内容确定性命中缓存，从而显著降低成本和延迟。

## 什么时候使用显式缓存

- **需要稳定命中缓存的场景**：当业务对缓存命中有明确要求，需要确保指定内容被稳定复用时，建议使用显式缓存。显式缓存可做到 100% 确定性命中，不受后端资源调度影响。

- **高频复用相同 Prompt 的场景**：当相同或高度一致的 Prompt 会被反复提交时，显式缓存可以显著降低调用成本。首次写入缓存仅产生标准价格 25% 的额外开销，后续命中可节省 90% 成本；只要发生至少一次命中，总体成本即低于不使用缓存的方案。

- **工业级 Agent 的长上下文管理场景**：在 Agent 应用中，常见的压缩、recap、system reminder 等机制会导致上下文持续变化。显式缓存可对关键上下文片段进行标记和固定复用，确保这些内容在复杂上下文演进过程中仍能稳定命中缓存。

## 常用 Agent 和 Coding 工具

以下 Agent 和 Coding 工具可通过 Anthropic 协议接入千问AI平台，原生支持显式缓存。只需按对应文档完成配置，工具在运行过程中会自动使用显式缓存优化上下文管理。

以下示例以华北2（北京）端点为例，其他地域请替换为对应的地域端点。

<Tabs>
  <Tab title="Claude Code">
    Claude Code 自 v2.x 起默认在请求中携带`cache_control`标记（system、env、最近 user message 三处），接入千问AI平台 Anthropic 兼容端点后无需额外配置。

    **接入配置**

    新建`~/.claude/settings.json`（Windows：`C:\Users\<用户名>\.claude\settings.json`），写入对应套餐的配置。或通过环境变量接入：

    ```bash
    export ANTHROPIC_BASE_URL="https://dashscope.aliyuncs.com/apps/anthropic"
    export ANTHROPIC_AUTH_TOKEN="${DASHSCOPE_API_KEY}"
    export ANTHROPIC_MODEL="qwen3.8-max"
    claude
    ```

    确保接入端点为 Anthropic 协议：

    - Token Plan 团队版：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
    - 按量计费：`https://dashscope.aliyuncs.com/apps/anthropic`

    详见 [Claude Code](/developer-guides/clients-and-developer-tools/claude-code)。

    **可选：提升跨会话命中率**

    Claude Code 默认会在 system prompt 中包含当前目录、日期、git 状态等动态信息，可能导致跨会话命中率下降。启动时增加以下参数可将动态部分移至 user message：

    ```bash
    claude --exclude-dynamic-system-prompt-sections
    ```

    **可选：关闭显式缓存**

    如需关闭（一般无须关闭）：

    ```bash
    export DISABLE_PROMPT_CACHING=1
    ```

    支持按模型粒度关闭：`DISABLE_PROMPT_CACHING_HAIKU`、`DISABLE_PROMPT_CACHING_SONNET`、`DISABLE_PROMPT_CACHING_OPUS`。
  </Tab>

  <Tab title="Open Code">
    OpenCode 通过`@ai-sdk/anthropic`接入千问AI平台 Anthropic 兼容端点时，默认对 system 与最近的非 system 消息注入`cache_control`。

    **安装**

    ```bash
    npm install -g opencode-ai
    ```

    **配置**

    创建配置文件`~/.config/opencode/opencode.json`（Windows：`C:\Users\<用户名>\.config\opencode\opencode.json`）：

    ```json
    {
      "$schema": "https://opencode.ai/config.json",
      "provider": {
        "bailian": {
          "npm": "@ai-sdk/anthropic",
          "name": "Alibaba Cloud Model Studio",
          "options": {
            "baseURL": "https://dashscope.aliyuncs.com/apps/anthropic/v1",
            "apiKey": "{env:DASHSCOPE_API_KEY}"
          },
          "models": {
            "qwen3.8-max": { "name": "qwen3.8-max" }
          }
        }
      }
    }
    ```

    <Note>
      `baseURL`末尾需带`/v1`。
    </Note>

    ```bash
    export DASHSCOPE_API_KEY=sk-xxxxx
    opencode run -m "bailian/qwen3.8-max" "..."
    ```

    其他套餐 base URL：

    - Token Plan 团队版：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1`

    详见 [OpenCode](/developer-guides/clients-and-developer-tools/opencode)。
  </Tab>

  <Tab title="OpenClaw">
    OpenClaw 走 Anthropic 兼容端点时默认对每次请求注入`cache_control`标记（系统提示词与最近用户消息），无需任何额外开关。只要 provider 的 Base URL 指向`/apps/anthropic`，显式缓存即自动启用。

    **安装**

    ```bash
    npm install -g openclaw
    # 或
    curl -fsSL https://openclaw.ai/install.sh | bash
    ```

    **配置**

    打开配置文件`~/.openclaw/openclaw.json`，将`"api"`设置为`"anthropic-messages"`，并设置 base URL：

    - Token Plan 团队版：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1`
    - 按量计费：`https://dashscope.aliyuncs.com/apps/anthropic/v1`

    详见 [OpenClaw](/developer-guides/clients-and-developer-tools/openclaw)。

    **可选：自定义缓存边界**

    如果 system prompt 中既有稳定模板又有动态内容（时间戳、CWD 等），可在中间插入`<!-- OPENCLAW_CACHE_BOUNDARY -->`标记。OpenClaw 会把标记前的稳定前缀挂`cache_control`，后面的动态后缀不挂，提升跨会话命中率：

    ```plaintext
    你是一个 Python 工程师，遵循以下规范：
    - type hints 必填
    - docstring 采用 Google 格式
    <!-- OPENCLAW_CACHE_BOUNDARY -->
    当前时间：2026-05-25 18:42
    工作目录：/Users/.../project
    ```

    未使用该标记时，OpenClaw 按内置策略整体挂`cache_control`，仍可享受显式缓存，不影响基础使用。
  </Tab>

  <Tab title="Hermes">
    通过`hermes config set`命令配置接入参数，设置 base URL：

    - Token Plan 团队版：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1`
    - 按量计费：`https://dashscope.aliyuncs.com/apps/anthropic/v1`

    详见 [Hermes Agent](/developer-guides/clients-and-developer-tools/hermes-agent)。
  </Tab>
</Tabs>

## API 接入

### 核心要点

- 在需要缓存的消息上添加`"cache_control": {"type": "ephemeral"}`，从 messages 数组开头到该标记位置之间的所有内容将被创建为缓存块。
- 缓存内容最少需要**1024 Token**。
- 单次请求最多支持**4**个缓存标记。
- 缓存有效期为**5 分钟**，每次命中自动续期。
- Tools 定义是 System Prompt 的一部分参与缓存计算，如果 Tools 改变则无法命中缓存。

### 快速开始

以下示例展示了显式缓存的基本使用方式：第一次请求创建缓存，第二次请求命中缓存。

<Tabs>
  <Tab title="OpenAI 兼容">
    ```python
    from openai import OpenAI
    import os
    client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    # 需要缓存的长文本（需超过 1024 Token）
    long_text_content = "<Your Long Text Here>" * 400
    def get_completion(user_input):
      messages = [
        {
          "role": "system",
          "content": [
            {
              "type": "text",
              "text": long_text_content,
              # 添加缓存标记：从 messages 开头到此位置的内容将被缓存
              "cache_control": {"type": "ephemeral"},
            }
          ],
        },
        {"role": "user", "content": user_input},
      ]
      completion = client.chat.completions.create(
        model="qwen3.8-max",
        messages=messages,
        extra_body={"enable_thinking": False},
      )
      return completion
    # 第一次请求：创建缓存
    first = get_completion("请总结文档的核心要点")
    print(f"创建缓存 Token：{first.usage.prompt_tokens_details.cache_creation_input_tokens}")
    print(f"命中缓存 Token：{first.usage.prompt_tokens_details.cached_tokens}")
    # 第二次请求：相同 system 内容，不同问题，命中缓存
    second = get_completion("文档中提到了哪些注意事项？")
    print(f"创建缓存 Token：{second.usage.prompt_tokens_details.cache_creation_input_tokens}")
    print(f"命中缓存 Token：{second.usage.prompt_tokens_details.cached_tokens}")
    ```
  </Tab>

  <Tab title="Anthropic 兼容">
    ```python
    import anthropic
    import os
    client = anthropic.Anthropic(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/apps/anthropic",
    )
    # 需要缓存的长文本（需超过 1024 Token）
    long_text_content = "<Your Long Text Here>" * 400
    def get_completion(user_input):
      response = client.messages.create(
        model="qwen3.8-max",
        max_tokens=1024,
        system=[
          {
            "type": "text",
            "text": long_text_content,
            # 添加缓存标记
            "cache_control": {"type": "ephemeral"},
          }
        ],
        messages=[
          {"role": "user", "content": user_input},
        ],
      )
      return response
    # 第一次请求：创建缓存
    first = get_completion("请总结文档的核心要点")
    print(f"创建缓存 Token：{first.usage.cache_creation_input_tokens}")
    print(f"命中缓存 Token：{first.usage.cache_read_input_tokens}")
    # 第二次请求：命中缓存
    second = get_completion("文档中提到了哪些注意事项？")
    print(f"创建缓存 Token：{second.usage.cache_creation_input_tokens}")
    print(f"命中缓存 Token：{second.usage.cache_read_input_tokens}")
    ```
  </Tab>
</Tabs>

运行上述代码，预期输出类似如下：

```plaintext
创建缓存 Token：2005
命中缓存 Token：0
创建缓存 Token：0
命中缓存 Token：2005
```

第一次请求时系统创建缓存块，第二次请求因 System Prompt 内容完全一致，成功命中缓存。命中缓存的 Token 仅按标准输入价格的 10% 计费。

### 确认缓存状态

请求完成后，可以通过响应中的`usage`字段确认缓存状态：

- `cache_creation_input_tokens`：本次请求新创建缓存的 Token 数。该值大于 0 说明创建了新缓存。
- `cached_tokens`（OpenAI 兼容）或`cache_read_input_tokens`（Anthropic 兼容）：本次请求命中缓存的 Token 数。该值大于 0 说明成功命中缓存。

## 不同场景下的最佳实践

### 多轮对话场景

**场景特点：**

- 用户与模型进行多轮交互，每轮请求携带完整对话历史
- 典型应用：客服对话、知识问答、代码辅助等

\*\*最佳实践：\*\*在每次请求的最后一条消息上添加`cache_control`标记。每轮对话都会命中上一轮创建的缓存（对话历史部分），同时为下一轮创建包含当前完整对话的新缓存。

**示例：**

```python
from openai import OpenAI
import os
client = OpenAI(
  api_key=os.getenv("DASHSCOPE_API_KEY"),
  base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
# System Prompt（产品手册，需超过 1024 Token）
product_manual = """你是智能家居产品"千问智家"的客服助手。以下是完整产品手册：
## 产品概述
千问智家 是一款全屋智能中控设备，支持语音控制、场景联动、能耗管理等功能...
## 安装指南
1. 选择中心位置安装，确保 WiFi 信号覆盖...
2. 连接电源适配器（5V/2A）...
## 常见问题
Q: 设备无法连接 WiFi？A: 请确认路由器支持 2.4GHz...
""" * 80  # 重复以确保超过 1024 Token
messages = [{"role": "system", "content": product_manual}]
def chat(user_input):
  # 关键：在最后一条用户消息上添加 cache_control
  messages.append({
    "role": "user",
    "content": [
      {
        "type": "text",
        "text": user_input,
        "cache_control": {"type": "ephemeral"},
      }
    ],
  })
  completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=messages,
    extra_body={"enable_thinking": False},
  )
  assistant_msg = completion.choices[0].message.content
  messages.append({"role": "assistant", "content": assistant_msg})
  usage = completion.usage
  created = usage.prompt_tokens_details.cache_creation_input_tokens
  cached = usage.prompt_tokens_details.cached_tokens
  print(f"  [缓存] 创建: {created} Token, 命中: {cached} Token")
  return assistant_msg
# 模拟多轮客服对话
print("用户: 千问智家 支持哪些语音助手？")
print(f"客服: {chat('千问智家 支持哪些语音助手？')[:60]}...\n")
print("用户: WiFi 连不上怎么办？")
print(f"客服: {chat('WiFi 连不上怎么办？')[:60]}...\n")
print("用户: 可以同时控制多少个设备？")
print(f"客服: {chat('可以同时控制多少个设备？')[:60]}...")
```

从第二轮开始，每轮对话都命中了上一轮创建的缓存（即之前完整的对话历史），同时创建包含当前轮新内容的缓存。对话轮数越多，节约越显著。

### 复杂工业级 Agent 场景

**场景特点：**

- 超长多轮对话，包含：长 System Prompt + skills/tools 说明 + project 上下文 + 用户对话 / 工具调用
- 不同部分的变化频率不同
- 典型应用：AI 编程助手（如 Claude Code、OpenClaw）、RAG 问答系统等

\*\*最佳实践：\*\*使用多个缓存标记（最多 4 个），分别标记不同稳定性层级的内容。每个标记需放在不同的 message 上才能作为独立截断点：

- System Prompt 加一个（几乎不变）
- skills/tools 说明加一个（可能出现组合变化）
- project 上下文加一个（可能切换/压缩）
- 用户对话 / 工具调用加一个（每轮增长）

\*\*示例：\*\*以下示例中，系统人设几乎不变（缓存标记 1），知识库随商品切换而变化（缓存标记 2），对话历史每轮增长（缓存标记 3）。注意：知识库放在 user message 中，以确保它有独立的缓存截断点——多条 system message 会被内部合并，无法作为独立截断点：

```python
from openai import OpenAI
import os
client = OpenAI(
  api_key=os.getenv("DASHSCOPE_API_KEY"),
  base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
# 第一层：系统人设（几乎不变）
system_persona = """你是"千问电子"的高级客服 AI 助手。你需要：
1. 基于知识库内容准确回答用户问题
2. 对于知识库中没有的信息，如实告知"我需要为您转接人工客服"
3. 始终保持专业、友善的语气
4. 如用户表示不满，先致歉再解决问题
以下是你的完整服务规范和话术指南：
""" + "服务规范详细说明..." * 200  # 确保超过 1024 Token
# 第二层：知识库检索结果（半稳定，随用户咨询的商品变化）
knowledge_base_product_a = """### 当前咨询商品：千问 Pro Max 无线耳机
- SKU: QW-PM-2024
- 价格: 599 元
- 颜色: 极夜黑 / 星云白 / 冰晶蓝
- 续航: 主动降噪开启 8 小时，关闭 12 小时
- 防水等级: IPX5
- 保修: 1 年质保，支持 7 天无理由退换
- 当前库存: 极夜黑（充足）/ 星云白（少量）/ 冰晶蓝（缺货）
""" * 50  # 确保超过 1024 Token
def ask_about_product_a(user_question, history=None):
  if history is None:
    history = []
  messages = [
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": system_persona,
          "cache_control": {"type": "ephemeral"},  # 缓存标记 1：系统人设
        }
      ],
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": f"以下是当前商品的知识库信息：\n{knowledge_base_product_a}",
          "cache_control": {"type": "ephemeral"},  # 缓存标记 2：知识库
        }
      ],
    },
    {"role": "assistant", "content": "好的，我已了解该商品的详细信息，请问有什么可以帮您？"},
  ]
  # 添加对话历史
  messages.extend(history)
  # 添加当前问题（带缓存标记 3）
  messages.append({
    "role": "user",
    "content": [
      {
        "type": "text",
        "text": user_question,
        "cache_control": {"type": "ephemeral"},  # 缓存标记 3：对话历史
      }
    ],
  })
  completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=messages,
    extra_body={"enable_thinking": False},
  )
  usage = completion.usage
  print(f"  创建缓存: {usage.prompt_tokens_details.cache_creation_input_tokens}, "
        f"命中缓存: {usage.prompt_tokens_details.cached_tokens}")
  return completion.choices[0].message.content
# 第一次：用户询问商品 A
print("Q1: 这款耳机有冰晶蓝色吗？")
a1 = ask_about_product_a("这款耳机有冰晶蓝色吗？")
print(f"A1: {a1}\n")
# 第二次：继续追问商品 A（系统人设 + 知识库均命中）
history = [
  {"role": "user", "content": "这款耳机有冰晶蓝色吗？"},
  {"role": "assistant", "content": a1},
]
print("Q2: 那什么时候能补货？")
a2 = ask_about_product_a("那什么时候能补货？", history)
print(f"A2: {a2}")
```

**多标记缓存的命中逻辑：**

- **用户继续追问同一商品**：系统人设 + 知识库均未变化，命中缓存标记 2 处的缓存（最长前缀匹配），节约最大。
- **对话轮次增加**：前面的内容（系统人设 + 知识库 + 历史对话）命中上一轮的缓存，仅新增部分需创建新缓存。

<Tip>
  建议将内容按稳定性从高到低排列：将变化最少的内容放在最前面（如系统人设），变化最频繁的内容放在最后面（如当前对话），以最大化缓存命中率。
</Tip>

### 任务完成型场景（批量处理）

**场景特点：**

- 单轮对话，不需要上下文记忆
- 不变的长 System Prompt（任务说明）+ 变化的用户输入（待处理数据）
- 典型应用：文本分类、意图识别、数据提取、内容审核等

\*\*最佳实践：\*\*仅在 System Prompt 上添加`cache_control`标记。后续每次请求只要 System Prompt 不变，即可命中缓存。

### Function Calling 时缓存工具列表

**场景特点：**

- 使用 Function Calling 功能，工具定义列表较长
- 工具定义在多次请求间保持不变

**最佳实践：**`tools`参数的内容会作为 System Prompt 的一部分参与缓存。只需确保每次请求的工具定义完全一致（工具顺序、字段顺序、字段结构），并在 messages 的 content 上添加`cache_control`标记即可。

<Warning>
  提高 Function Calling 缓存命中率的关键：

  - **工具列表顺序一致**：tools 数组中各工具的排列顺序需保持一致。
  - **字段顺序一致**：同一个 tool 的 JSON 字段顺序需保持一致。
  - **字段结构一致**：不要遗漏或新增字段，即使该字段为空或可选。
</Warning>

## 注意事项

- **content 格式要求**：添加`cache_control`时，必须将 content 字段改为数组形式。字符串形式的 content 不支持添加缓存标记。

- **缓存标记粒度**：Qwen3.5 及之后的模型仅支持消息级别的缓存截断点。在同一条 message 的 content 数组内放置多个`cache_control`不会产生多个截断点——系统仅在该 message 的最后一个 marker 位置存储缓存，无法在中间 block 处截断命中。此外，多条 system message 会被内部合并为一个整体，也无法在中间截断。如需多个独立截断点，应将带`cache_control`的内容分布在不同角色的 message 上（如 system 放一个，user 放一个）。Qwen3.5 之前的模型支持 content 级别（消息内部）的缓存截断。

- **与隐式缓存互斥**：同一请求只能使用一种缓存模式。若请求中包含`cache_control`标记则使用显式缓存，否则系统自动使用隐式缓存。

## 支持的模型

支持显式缓存的模型列表请参见[上下文缓存](/developer-guides/run-and-scale/context-cache#显式缓存)。
