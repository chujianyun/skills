# Claude Code

[Claude Code](https://watcha.cn/products/claude-code?ref=tokendance-docs) 是 Anthropic 推出的命令行 AI 编程助手。通过将 Claude Code 指向词元跳动，你可以使用词元跳动上支持 Anthropic 协议的模型来驱动它，费用从词元跳动额度扣除，所有请求记录在 [调用日志](https://tokendance.space/activity) 中。

更多信息请访问 [观猹产品主页](https://watcha.cn/products/claude-code?ref=tokendance-docs)。

## 安装 Claude Code {#install}

:::group

```bash title="macOS / Linux"
curl -fsSL https://claude.ai/install.sh | bash
```

```bash title="npm"
# 需要 Node.js 18 或更高版本
npm install -g @anthropic-ai/claude-code
```

:::

## 配置 {#configuration}

编辑 `~/.claude/settings.json`，添加以下配置：

```json title="~/.claude/settings.json"
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "YOUR_KEY",
    "ANTHROPIC_BASE_URL": "https://tokendance.space/gateway",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-v4-flash-0731",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "deepseek-v4-flash-0731",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "deepseek-v4-flash-0731"
  },
  "model": "opus"
}
```

将 `YOUR_KEY` 替换为你的词元跳动 API Key，将模型 ID 替换为你想使用的模型（需支持 Anthropic 协议）。

### 字段说明 {#fields}

| 字段 | 说明 |
|---|---|
| ANTHROPIC_AUTH_TOKEN | 你的词元跳动 API Key |
| ANTHROPIC_BASE_URL | 词元跳动网关地址 |
| CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC | 设为 1 禁止向 Anthropic 发送非必要请求 |
| ANTHROPIC_DEFAULT_OPUS_MODEL | Opus 级别任务使用的模型（复杂推理） |
| ANTHROPIC_DEFAULT_SONNET_MODEL | Sonnet 级别任务使用的模型（常规编码） |
| ANTHROPIC_DEFAULT_HAIKU_MODEL | Haiku 级别任务使用的模型（快速补全） |
| model | 默认使用的模型级别，设为 opus 即使用 ANTHROPIC_DEFAULT_OPUS_MODEL 指定的模型 |

::: note
模型 ID 以词元跳动 [模型列表](https://tokendance.space/models) 中的为准，且需支持 Anthropic 协议。你可以为三个级别配置不同的模型，也可以像示例中一样统一使用同一个模型。
:::

## 启动与验证 {#start}

```bash
cd /path/to/your/project
claude
```

启动后在 Claude Code 中执行 `/status`，确认连接信息：

```text
> /status
Auth token: ANTHROPIC_AUTH_TOKEN
Anthropic base URL: https://tokendance.space/gateway
```

## 工作原理 {#how-it-works}

词元跳动原生支持 Anthropic Messages API。将 `ANTHROPIC_BASE_URL` 指向词元跳动后，Claude Code 会直接以 Anthropic 协议通信，无需本地代理或协议转换。费用按实际 token 用量从词元跳动额度中扣除。

## 常见问题 {#troubleshooting}

- **认证失败**：确认使用 `ANTHROPIC_AUTH_TOKEN`（而非 `ANTHROPIC_API_KEY`）传递密钥。
- **上下文超限**：尝试将任务拆分为更小的部分，或开启新会话。
- **模型不兼容**：Claude Code 对模型能力有一定要求，部分模型可能无法正常驱动，建议选择能力较强的模型。

## 相关文档 {#related}

- [Anthropic 协议](../../%E6%A8%A1%E5%9E%8B%E4%B8%8E%E5%8D%8F%E8%AE%AE/%E9%80%9A%E7%94%A8%E6%A8%A1%E5%9E%8B%E5%8D%8F%E8%AE%AE/Anthropic/Anthropic%20Messages.md) — 协议详情与使用方式
- [API 密钥](../../%E5%BC%80%E5%A7%8B%E4%BD%BF%E7%94%A8/%E8%AE%BF%E9%97%AE%E4%B8%8E%E8%AE%A4%E8%AF%81/API%20%E5%AF%86%E9%92%A5.md) — 创建和管理密钥
- [模型](../../%E6%A8%A1%E5%9E%8B%E4%B8%8E%E5%8D%8F%E8%AE%AE/%E9%80%89%E6%8B%A9%E6%A8%A1%E5%9E%8B%E4%B8%8E%E5%8D%8F%E8%AE%AE/%E6%A8%A1%E5%9E%8B%E4%B8%8E%E5%8D%8F%E8%AE%AE%E6%A6%82%E8%A7%88.md) — 查看支持 Anthropic 协议的模型
