> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 数据安全与隐私

> 千问AI平台如何保护您的数据

千问AI平台在从 API 请求到模型推理的各个环节保护您的数据安全。本文介绍已实施的关键安全措施。

## 加密

| 数据状态  | 标准                              |
| ----- | ------------------------------- |
| 传输中数据 | 所有 API 连接使用 TLS 1.2 及以上版本       |
| 静态数据  | 存储数据（API Key、账户信息）使用 AES-256 加密 |

## API Key 安全

API Key 用于验证发送到千问AI平台的每个请求。请遵循以下最佳实践保护您的 Key：

- **不要在源代码中硬编码 Key**，也不要将其提交到版本控制系统。请使用环境变量或密钥管理服务。
- **为开发和生产环境使用不同的 Key**。
- **定期轮换 Key**。您可以在 [API Key](/developer-guides/administration/api-keys) 页面创建新 Key 并删除旧 Key。
- **限制访问权限**，在特定的[业务空间](/developer-guides/administration/workspace)中创建 Key 并配置相应权限。

API Key 的详细说明，请参阅 [API Key](/developer-guides/administration/api-keys)。

## 内容审核

所有 API 请求均经过自动内容审核，对输入和输出中的有害、违法或不当内容进行筛查。

## 负责任的 AI 实践

作为基于千问AI平台构建应用的开发者，您需要共同承担应用安全责任：

- 在将用户内容传递给 API 之前，实施输入校验。
- 根据使用场景设置合适的 `max_tokens` 限制。
- 在应用层添加速率限制，防止滥用。
- 利用千问AI平台内置的内容审核功能，监控输入和输出的内容安全。

## 了解更多

- [审计与访问日志](/developer-guides/security-compliance/audit-logs)：跟踪 API 使用情况，满足合规要求。
