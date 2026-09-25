> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# API Key

> 创建和管理 API Key

## 概述

每个发送到千问AI平台的 API 请求都需要使用 API Key 进行身份验证。[API Keys](https://platform.qianwenai.com/home/api-keys) 页面集中管理您的所有访问凭证，包括按量付费 API Key 和 Token Plan API Key。

- **按量付费 API Key**：属于一个[业务空间](/developer-guides/administration/workspace)，继承该业务空间的模型访问权限和[限流](/developer-guides/administration/rate-limits)。
- **Token Plan API Key**：仅展示购买者的访问凭证，用于模型调用鉴权。席位分配和成员管理需前往 [Token Plan 管理平台](https://tokenplan-enterprise.qianwenai.com)。

如需快速获取第一个 API Key 的指南，请参阅[获取 API Key](/api-reference/preparation/api-key)。

## 创建 API Key

<Steps>
  <Step title="选择业务空间">
    前往 [API Key](https://platform.qianwenai.com/home/api-keys) 页面。如需切换业务空间，请前往**设置** > [业务空间](https://platform.qianwenai.com/home/settings/workspaces)，通过**当前业务空间**下拉菜单选择目标业务空间。
  </Step>

  <Step title="创建 API Key">
    点击**创建 API Key**。输入描述信息以便后续识别（例如"主应用的生产环境 API Key"），然后点击**生成 API Key**。
  </Step>

  <Step title="复制 API Key">
    请立即复制 API Key——**密钥仅显示一次**。关闭对话框后，您只能看到密钥的掩码版本。
  </Step>
</Steps>

每个业务空间最多支持 20 个 API Key。当前数量显示在**创建 API Key** 按钮上（例如 0/20）。

## 管理按量付费 API Key

在 [API Keys](https://platform.qianwenai.com/home/api-keys) 页面的**按量付费**区域，您可以：

- **搜索**：通过描述内容查找 API Key。
- **编辑**：点击**编辑**以更新 API Key 的描述信息。
- **删除**：点击**删除**以永久撤销 API Key。此操作不可撤消——使用该 API Key 的所有请求将立即失败。
- **启用/禁用**：通过状态开关启用或禁用 API Key。禁用后，使用该 Key 的请求将被拒绝；重新启用后立即恢复。
- **查看费用**：点击**查看费用**跳转至该 API Key 的费用明细页面。

API Key 表格显示每个密钥的 **ID**、**API Key**（已掩码）、**描述**、**创建时间**、**费用**、**状态**以及可用的**操作**。

## 管理 Token Plan API Key

在 [API Keys](https://platform.qianwenai.com/home/api-keys) 页面的 **Token Plan** 区域，展示购买者的 Token Plan 访问凭证，表格包含 **API Key**（已掩码）、**状态**、**席位类型**、**剩余天数**和**操作**（重置、管理）。

- **重置**：重新生成 API Key，原 Key 立即失效。
- **管理**：跳转至 [Token Plan 管理平台](https://tokenplan-enterprise.qianwenai.com)进行席位分配、成员管理等操作。

<Note>
  Token Plan API Key 的完整管理（席位分配、SSO 登录、成员管理）请在 [Token Plan 管理平台](https://tokenplan-enterprise.qianwenai.com)中操作。详见[团队管理](/token-plan/team-management)。
</Note>

## 按量付费 API Key 与业务空间

按量付费 API Key 的作用范围限定在其创建时所在的业务空间：

- **默认业务空间**中的 API Key 可以调用所有可用模型，使用账户级别的速率限制。
- **子业务空间**中的 API Key 只能调用已授权给该业务空间的模型，使用为该业务空间配置的速率限制。

要管理其他业务空间的 API Key，请先前往**设置** > [业务空间](https://platform.qianwenai.com/home/settings/workspaces)切换到目标业务空间。

## 安全最佳实践

- **安全存储密钥**：使用环境变量或密钥管理器。切勿将 API Key 硬编码在源代码中。
- **不要在客户端暴露密钥**：API Key 只应在服务端代码中使用。切勿将其包含在前端应用、移动应用或浏览器代码中。
- **定期轮换密钥**：删除已泄露或未使用的 API Key，并创建新密钥。
- **为不同环境使用独立密钥**：为开发、测试和生产环境创建不同的 API Key（或业务空间）。
