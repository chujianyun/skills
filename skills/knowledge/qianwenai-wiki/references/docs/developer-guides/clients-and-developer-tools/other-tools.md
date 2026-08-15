> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 其他 AI 工具

> 兼容 OpenAI/Anthropic 协议的工具

除已列出的工具外，千问AI平台还支持接入兼容 OpenAI / Anthropic API 协议且支持自定义服务端点的第三方编程工具。可通过按量计费、Token Plan 个人版或 Token Plan 团队版接入。

## 配置接入凭证

### Token Plan 个人版

| API 协议    | Base URL                                                             | API Key                                                                                         | 支持模型                                                                     |
| --------- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| OpenAI    | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | Token Plan 个人版专属 [API Key](https://platform.qianwenai.com/home/billing/subscription/token-plan) | [支持的模型](/token-plan/personal/token-plan-personal-overview#支持的模型)（仅文本生成类） |
| Anthropic | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`     | Token Plan 个人版专属 [API Key](https://platform.qianwenai.com/home/billing/subscription/token-plan) | [支持的模型](/token-plan/personal/token-plan-personal-overview#支持的模型)（仅文本生成类） |

### Token Plan 团队版

| API 协议    | Base URL                                                             | API Key                                                                                         | 支持模型                                                             |
| --------- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| OpenAI    | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | Token Plan 团队版专属 [API Key](https://platform.qianwenai.com/home/billing/subscription/token-plan) | [支持的模型](/token-plan/team/token-plan-team-overview#支持的模型)（仅文本生成类） |
| Anthropic | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`     | Token Plan 团队版专属 [API Key](https://platform.qianwenai.com/home/billing/subscription/token-plan) | [支持的模型](/token-plan/team/token-plan-team-overview#支持的模型)（仅文本生成类） |

<Note>
  部分工具（如 Kilo Code、OpenCode）使用的 `@ai-sdk/anthropic` SDK 仅追加 `/messages` 而非 `/v1/messages`，需将 Base URL 设为 `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1`。具体配置请参考各工具的接入文档。
</Note>

### 按量计费

| API 协议    | Base URL                                            | API Key                                              | 支持模型                                                              |
| --------- | --------------------------------------------------- | ---------------------------------------------------- | ----------------------------------------------------------------- |
| OpenAI    | `https://dashscope.aliyuncs.com/compatible-mode/v1` | 千问AI平台 [API Key](/api-reference/preparation/api-key) | [支持的模型](/developer-guides/getting-started/text-generation-models) |
| Anthropic | `https://dashscope.aliyuncs.com/apps/anthropic`     | 千问AI平台 [API Key](/api-reference/preparation/api-key) | [支持的模型](/developer-guides/getting-started/text-generation-models) |

## 不支持的工具类型

Token Plan 个人版和 Token Plan 团队版仅限在 AI 编程工具和 OpenClaw 类型 Agent 中使用，以下类型的工具**不支持**接入：

- **工作流/自动化平台**：如 Dify、n8n、Coze 等。
- **API 测试工具**：如 Postman、Insomnia 等。
- **自定义应用程序**：直接在自动化脚本、应用后端代码中调用 API 等。

<Warning>
  将套餐 API Key 用于允许范围之外的调用将被视为违规或滥用，可能会导致订阅被暂停或 API Key 被封禁。
</Warning>

## 配置示例：Trae

Trae 支持接入自定义模型，无需安装插件即可直接配置上述任一方案的服务端点接入千问AI平台。以下以 Trae 为例说明配置步骤：

1. 在 Trae 中前往**设置** > **模型**，单击**添加**，选择**自定义配置**。
2. **API 格式**：根据所选服务端点的协议，选择**兼容 OpenAI** 或**兼容 Anthropic**。
3. **请求地址**：填写上表中对应方案的 Base URL。
4. **模型 ID**：填写对应方案支持的模型名称。
5. **API 密钥**：填写对应方案的专属 API Key。
6. 保存后，在对话框右下角的模型列表中即可选择并使用该模型。

## 在 IDE 中使用

如需在 VS Code 系列或 JetBrains IDE 中使用，可通过安装以下插件接入：

| 插件              | 支持 IDE                | 接入文档                                                                     |
| --------------- | --------------------- | ------------------------------------------------------------------------ |
| **Claude Code** | VS Code、JetBrains IDE | [Claude Code](/developer-guides/clients-and-developer-tools/claude-code) |
| **Kilo Code**   | VS Code、JetBrains IDE | [Kilo CLI](/developer-guides/clients-and-developer-tools/kilo-cli)       |
| **Qwen Code**   | VS Code               | [Qwen Code](/developer-guides/clients-and-developer-tools/qwen-code)     |
