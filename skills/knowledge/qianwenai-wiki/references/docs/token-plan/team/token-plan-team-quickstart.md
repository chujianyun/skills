> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 快速开始

> 三步完成 Token Plan 团队版订阅和接入

## 步骤一：订阅 Token Plan 团队版

访问 [Token Plan 团队版购买页面](https://platform.qianwenai.com/pricing/token-plan)，选择席位类型和数量并完成订阅。

## 步骤二：获取 API Key 与 Base URL

1. 进入 [Token Plan 管理平台](https://tokenplan-enterprise.qianwenai.com)，在**成员管理**页面点击**分配席位**，选择席位版本后点击**确定**。
2. 分配完成后，点击该成员对应的**生成**，创建专属 API Key（格式：`sk-sp-xxxxx`，生成后仅显示一次，请立即复制保存）。
3. 在**API Key**页面查看套餐专属 Base URL。

<Note>
  - 生成 API Key 前，需在**成员管理**页面为对应账号分配席位。
  - Token Plan 专属 API Key 仅在创建或重置时完整显示一次，之后控制台仅显示脱敏信息（如 `sk-sp-****`），无法再次查看完整内容。请在生成时立即复制并妥善保存。
  - Token Plan 专属 API Key 以 `sk-sp-` 开头，与千问AI平台通用 API Key（`sk-ws-` 开头）格式不同，两者不可混用。详见[两种 API Key 的区别](/api-reference/preparation/api-key)。
</Note>

根据 AI 工具支持的协议选择对应 Base URL：

| 协议           | Base URL                                                             |
| ------------ | -------------------------------------------------------------------- |
| OpenAI 兼容    | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Anthropic 兼容 | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`     |

<Warning>
  Token Plan 和按量付费的 API Key 与 Base URL 完全隔离，必须配套使用，不可混用。

  - **Token Plan 团队版**：使用 `sk-sp-` 开头的专属 API Key + 上方表格中的 Base URL。
  - **按量付费**：使用千问AI平台通用 API Key（`sk-ws-` 开头）+ API Key 页面显示的 Base URL。

  如果购买了 Token Plan 但使用了通用 API Key 或其他计费模式的 Base URL，会导致调用走按量计费通道产生意外扣费，或返回 401/403 鉴权失败错误。
</Warning>

## 步骤三：配置 AI 工具

<CardGroup cols={3}>
  <Card title="OpenClaw" icon="https://unpkg.com/@lobehub/icons-static-svg@latest/icons/openclaw-color.svg" href="/developer-guides/clients-and-developer-tools/openclaw">
    开源自托管个人 AI 助手
  </Card>

  <Card title="Hermes Agent" icon="https://unpkg.com/@lobehub/icons-static-svg@latest/icons/nousresearch.svg" href="/developer-guides/clients-and-developer-tools/hermes-agent">
    开源 AI 代理框架
  </Card>

  <Card title="Claude Code" icon="https://unpkg.com/@lobehub/icons-static-svg@latest/icons/claude-color.svg" href="/developer-guides/clients-and-developer-tools/claude-code">
    AI 终端编码助手
  </Card>

  <Card title="OpenCode" icon="https://unpkg.com/@lobehub/icons-static-svg@latest/icons/opencode.svg" href="/developer-guides/clients-and-developer-tools/opencode">
    开源 AI 编程代理
  </Card>

  <Card title="Cursor" icon="https://unpkg.com/@lobehub/icons-static-svg@latest/icons/cursor.svg" href="/developer-guides/clients-and-developer-tools/cursor">
    AI 原生代码编辑器
  </Card>

  <Card title="Codex" icon="https://unpkg.com/@lobehub/icons-static-svg@latest/icons/codex.svg" href="/developer-guides/clients-and-developer-tools/codex">
    OpenAI 命令行编程工具
  </Card>

  <Card title="Qwen Code" icon="https://unpkg.com/@lobehub/icons-static-svg@latest/icons/qwen-color.svg" href="/developer-guides/clients-and-developer-tools/qwen-code">
    开源命令行 AI 编码工具
  </Card>

  <Card title="QwenPaw" icon="https://cdn.jsdelivr.net/gh/agentscope-ai/QwenPaw@main/website/public/qwenpaw-symbol.svg" href="/developer-guides/clients-and-developer-tools/qwenpaw">
    开源个人 AI 助手，支持本地与云端部署
  </Card>

  <Card title="Cherry Studio" icon="https://unpkg.com/@lobehub/icons-static-svg@latest/icons/cherrystudio-color.svg" href="/developer-guides/clients-and-developer-tools/cherry-studio">
    多模型桌面客户端
  </Card>

  <Card title="Chatbox" icon="https://cdn.jsdelivr.net/gh/chatboxai/chatbox@main/assets/icon.png" href="/developer-guides/clients-and-developer-tools/chatbox">
    跨平台 AI 桌面客户端
  </Card>

  <Card title="Cline" icon="https://unpkg.com/@lobehub/icons-static-svg@latest/icons/cline.svg" href="/developer-guides/clients-and-developer-tools/cline">
    VS Code 扩展，智能代码补全和调试
  </Card>

  <Card title="Qoder" icon="https://unpkg.com/@lobehub/icons-static-svg@latest/icons/qoder-color.svg" href="/developer-guides/clients-and-developer-tools/qoder">
    面向真实软件开发的 Agentic 编码平台
  </Card>

  <Card title="Qoder CN" icon="https://unpkg.com/@lobehub/icons-static-svg@latest/icons/bailian-color.svg" href="/developer-guides/clients-and-developer-tools/lingma">
    阿里云智能编码助手，提供独立 IDE
  </Card>

  <Card title="Kilo CLI" icon="https://unpkg.com/@lobehub/icons-static-svg@latest/icons/kilocode.svg" href="/developer-guides/clients-and-developer-tools/kilo-cli">
    轻量命令行编程工具
  </Card>
</CardGroup>

其他编程工具，请参见[更多工具](/developer-guides/clients-and-developer-tools/other-tools)。

## 可选：接入图像生成模型

Token Plan 团队版支持图像生成模型（qwen-image-2.0、wan2.7-image 等）。图像生成模型使用独立的接口，需要通过 AI 工具的 Skill 或扩展机制接入。

具体配置方法请参见[接入多模态生成模型](/token-plan/best-practices/multimodal-generation)。

## 可选：工具调用

通过接入工具调用，模型可以在对话中调用联网搜索、代码解释器等扩展能力。

- **Qwen 模型**：qwen3.8-max、qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash 内置联网搜索、代码解释器、网页抓取、以图搜图、文搜图等工具，通过 Responses API 直接调用。内置工具不额外收费，产生的 token 消耗统一从套餐 Credits 中抵扣。
- **其他模型**：通过 MCP 服务接入工具。

详细说明请参见[工具调用](/token-plan/best-practices/built-in-tools)。
