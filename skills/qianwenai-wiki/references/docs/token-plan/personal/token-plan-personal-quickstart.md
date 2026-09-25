> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 快速开始

> 三步完成 Token Plan 个人版订阅和接入

## 步骤一：订阅 Token Plan 个人版

访问 [Token Plan 个人版购买页面](https://platform.qianwenai.com/pricing/token-plan)，选择套餐档位和订阅周期，完成订阅。

购买须知：

- 同一实名认证主体限购一份。
- 个人版与团队版可同时持有，各自独立计费。

## 步骤二：获取 API Key 和 Base URL

- **API Key**：订阅完成后，在 Token Plan 控制台的**我的订阅**页面生成 API Key。API Key 仅在生成时完整显示一次，请立即复制并妥善保存。
- **Base URL**：根据 AI 工具支持的协议，选择对应的 Base URL。

| 协议           | Base URL                                                             |
| ------------ | -------------------------------------------------------------------- |
| OpenAI 兼容    | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Anthropic 兼容 | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`     |

<Warning>
  Token Plan 的 API Key 以`sk-sp-`开头，与千问AI平台通用 API Key（`sk-ws-`开头）格式不同，两者不可混用。Token Plan 和按量付费的 API Key 与 Base URL 完全隔离，必须配套使用。详见[两种 API Key 的区别](/api-reference/preparation/api-key)。
</Warning>

## 步骤三：接入 AI 工具

将 API Key 和 Base URL 配置到 AI 工具中，即可开始使用。

<CardGroup cols={3}>
  <Card title="OpenClaw" icon="https://unpkg.com/@lobehub/icons-static-svg@latest/icons/openclaw-color.svg" href="/developer-guides/clients-and-developer-tools/openclaw">
    开源、自托管个人 AI 助手
  </Card>

  <Card title="Hermes Agent" icon="https://unpkg.com/@lobehub/icons-static-svg@latest/icons/nousresearch.svg" href="/developer-guides/clients-and-developer-tools/hermes-agent">
    开源 AI 代理框架，内置自学习循环
  </Card>

  <Card title="Claude Code" icon="https://unpkg.com/@lobehub/icons-static-svg@latest/icons/claude-color.svg" href="/developer-guides/clients-and-developer-tools/claude-code">
    AI 终端编码助手，支持自然语言编程
  </Card>

  <Card title="OpenCode" icon="https://unpkg.com/@lobehub/icons-static-svg@latest/icons/opencode.svg" href="/developer-guides/clients-and-developer-tools/opencode">
    开源 AI 编程代理工具
  </Card>

  <Card title="Cursor" icon="https://unpkg.com/@lobehub/icons-static-svg@latest/icons/cursor.svg" href="/developer-guides/clients-and-developer-tools/cursor">
    AI 原生代码编辑器
  </Card>

  <Card title="Codex" icon="https://unpkg.com/@lobehub/icons-static-svg@latest/icons/codex.svg" href="/developer-guides/clients-and-developer-tools/codex">
    OpenAI 推出的命令行编程工具
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
    轻量高性能命令行编程工具
  </Card>

  <Card title="更多工具" href="/developer-guides/clients-and-developer-tools/other-tools">
    其他编程工具
  </Card>
</CardGroup>

## 可选：接入多模态生成模型

Token Plan 个人版支持多模态生成模型（wan2.7-image、happyhorse-1.1-t2v 等）。多模态生成模型使用独立的接口，需要通过 AI 工具的 Skill 或扩展机制接入，详见[接入多模态生成模型](/token-plan/best-practices/multimodal-generation)。

## 可选：接入 Harness 工具

部分 Qwen 模型（qwen3.7、qwen3.8 系列）内置 Harness 工具，可在对话中扩展联网搜索、文搜图、图搜图、网页抓取、代码解释器等能力。Harness 工具仅支持通过 Responses API 调用，按成功调用次数从套餐 Credits 中抵扣。详见[接入 Harness 工具](/token-plan/best-practices/built-in-tools)。

<Warning>
  Harness 工具需通过 Responses API 调用才会自动触发。若所用 AI 工具仅支持 Chat Completions 协议，模型可正常响应，但不会自动调用 Harness 工具，相关请求将按量付费计费，不消耗套餐 Credits 中的 Harness 工具额度。如需使用 Harness 工具，请选择兼容 Responses API 的 AI 工具（详见[接入 Harness 工具](/token-plan/best-practices/built-in-tools)）。
</Warning>
