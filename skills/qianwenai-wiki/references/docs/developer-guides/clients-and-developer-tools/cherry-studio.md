> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Cherry Studio

> 在 Cherry Studio 中使用千问AI平台模型

Cherry Studio 是一款开源 AI 桌面客户端，可以通过 Token Plan 个人版、Token Plan 团队版或按量计费接入千问AI平台。

## 安装 Cherry Studio

前往 [Cherry Studio 下载页面](https://www.cherry-ai.com/download)，根据操作系统下载安装包并完成安装。

## 配置接入凭证

打开 Cherry Studio，点击右上角的设置按钮，在**模型**栏点击**添加**，填写供应商名称（如 Token Plan 团队版），提供商类型选择 OpenAI。

千问AI平台提供以下计费方案，根据需要选择：

- **Token Plan 个人版**：按 token 消耗抵扣个人 Credits。
- **Token Plan 团队版**：按坐席订阅，按 token 消耗抵扣 Credits。
- **按量计费**：按实际调用量后付费。

### Token Plan 个人版

| 配置项        | 说明                                                                                      |
| ---------- | --------------------------------------------------------------------------------------- |
| **API 密钥** | 填入 Token Plan 个人版专属 [API Key](https://platform.qianwenai.com/home/api-keys)。            |
| **API 地址** | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`                    |
| **模型**     | 可用模型请参考 Token Plan 个人版[支持的模型](/token-plan/personal/token-plan-personal-overview#支持的模型)。 |

### Token Plan 团队版

| 配置项        | 说明                                                                           |
| ---------- | ---------------------------------------------------------------------------- |
| **API 密钥** | 填入 Token Plan 团队版专属 [API Key](https://platform.qianwenai.com/home/api-keys)。 |
| **API 地址** | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`         |
| **模型**     | 可用模型请参考 Token Plan 团队版[支持的模型](/token-plan/overview)。                         |

### 按量计费

| 配置项        | 说明                                                                   |
| ---------- | -------------------------------------------------------------------- |
| **API 密钥** | 填入千问AI平台 [API Key](/developer-guides/administration/api-keys)。       |
| **API 地址** | `https://dashscope.aliyuncs.com/compatible-mode/v1`                  |
| **模型**     | 填入[支持的模型](/developer-guides/getting-started/text-generation-models)。 |

## 验证配置

在**模型 ID** 填入需要使用的模型（如 `qwen3.7-max`），点击**添加**。返回对话界面，输入任意问题，模型正常返回响应即配置成功。

<Note>
  如果是 RAM 子账号，请参见[获取 API Key](/developer-guides/administration/api-keys)，确保拥有模型的调用权限。
</Note>

## 常见问题

### 错误码

配置过程中遇到报错，请参考对应计费方案的常见问题文档：

- 按量计费：[错误码排查](/api-reference/preparation/error-messages)
- Token Plan 个人版：[Token Plan 个人版常见问题](/token-plan/faq)
- Token Plan 团队版：[Token Plan 团队版常见问题](/token-plan/faq)

### 报错 The value of the enable\_thinking parameter is restricted to True

**原因**：该模型仅支持在思考模式下运行，但调用时未开启思考模式。

**解决方案**：在客户端中开启思考模式。

### 接入按量计费时，有免费额度但产生了费用

可能的原因：

- **额度按模型独立计算**：各模型的免费额度相互独立，不可跨模型共享。
- **数据更新延迟**：控制台显示的免费额度数据每小时更新。即使控制台显示仍有余量，实际额度也可能已耗尽。

可通过[费用明细](/resources/billing-overview)确认费用详情。
