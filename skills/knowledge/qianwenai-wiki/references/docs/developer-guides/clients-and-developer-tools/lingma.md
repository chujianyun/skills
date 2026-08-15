> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Qoder CN（原 Lingma）

> 在 Qoder CN IDE 中使用千问AI平台模型

Qoder CN（原 Lingma）是阿里云智能编码助手，提供独立 IDE，可以通过 Token Plan 个人版、Token Plan 团队版或按量付费接入千问AI平台。

<Note>
  Qoder CN 个人社区版和个人专业版均支持接入千问AI平台，企业版不支持。
</Note>

## 安装与使用

1. 前往 [Qoder CN 官网](https://qoder.com.cn/)下载并安装 Qoder CN。

2. 初次启动后完成初始配置。

3. 在登录页面中，选择阿里云账号登录后，即可在 Qoder CN IDE 中看到已登录状态。

## 配置接入凭证

1. 在界面右上角打开 Qoder CN 设置，选择**模型**，点击**添加**。

2. 按照以下参数填入相关信息：

| 配置项     | 说明                                                                                                                                           |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| 提供商     | 在下拉菜单中选择**千问AI平台 - 中国**                                                                                                                      |
| 类型      | 根据计费方案选择 **Token Plan**（个人版或团队版）或**按量付费**                                                                                                    |
| 模型      | 在下拉菜单中选择模型                                                                                                                                   |
| API Key | 填写 Token Plan 个人版或团队版专属 [API Key](https://platform.qianwenai.com/home/api-keys)，或千问AI平台 [API Key](/developer-guides/administration/api-keys) |

<Note>
  仅支持文本生成类模型（如 qwen3.6-plus、glm-5 等）。
</Note>

3. 点击**添加**，通过校验后即可完成模型配置。

4. 在 Qoder CN 对话框中，选择对应模型即可开始使用。

## 了解更多

如需进一步了解 Qoder CN 的智能体、MCP、Skills 等扩展能力，请参考 [Qoder CN 官方文档](https://help.aliyun.com/zh/lingma/product-overview/introduction-of-lingma)。

## 常见问题

### 错误码

配置过程中遇到报错，请参考对应计费方案的常见问题文档：

- 按量付费：[错误码排查](/api-reference/preparation/error-messages)
- Token Plan 个人版：[Token Plan 常见问题](/token-plan/faq)
- Token Plan 团队版：[Token Plan 团队版常见问题](/token-plan/faq)

### 为什么在 Qoder CN 设置中找不到模型选项？

可能有以下原因：

- **未完成登录**：需要先完成登录，才能进行对话和配置模型。
- **当前版本不支持**：接入千问AI平台需要 Qoder CN 个人社区版或个人专业版，企业版不支持。

### API Key 认证失败（HTTP 401）

请确认以下几点：

- 确认使用的 API Key 与所选**类型**（Token Plan 个人版/团队版或按量付费）一致。
- 确认套餐未过期。
- API Key 复制完整、无空格。如仍报错，可在对应管理页面重置 API Key。

更多问题请参考[常见问题](/token-plan/faq)。

### 对话报错"自定义模型服务异常，请稍后重试或切换其他模型。Unknown Custom model Exception"

该报错是 Qoder CN 在收到无法识别的后端响应时的通用提示，常见触发原因如下：

- **提供商或类型与实际套餐不一致**：在 Qoder CN 模型配置中，**提供商**与**类型**需与所购套餐保持一致。例如使用 Token Plan 团队版的 API Key，但**类型**选成了按量付费。
- **选用了套餐不支持的模型**：仅支持当前套餐覆盖的文本生成模型。
- **临时网络或服务波动**：稍后重试。
