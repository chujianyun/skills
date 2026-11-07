# Dify 服务的反向调用

> 在插件中调用 Dify 平台的 App、Model、Tool 和 Node 服务

> 本文档由 AI 自动翻译。如有任何不准确之处，请参考 [英文原版](https://docs.dify.ai/en/develop-plugin/features-and-specs/advanced-development/reverse-invocation.md)。

借助反向调用，插件可调用 Dify 主平台内的服务来扩展自身能力。

## 可调用的 Dify 模块

* **[App](%E5%BA%94%E7%94%A8.md)**：访问 Dify 平台内 App 的数据。
* **[Model](%E5%8F%8D%E5%90%91%E8%B0%83%E7%94%A8%E6%A8%A1%E5%9E%8B.md)**：调用 Dify 平台内的 LLM 能力，涵盖所有模型类型及 TTS、Rerank 等功能。
* **[Tool](%E5%B7%A5%E5%85%B7.md)**：调用 Dify 平台内的其他工具类型插件。
* **[Node](%E8%8A%82%E7%82%B9.md)**：调用 Dify 平台内特定 Chatflow/Workflow 应用中的节点。

## 相关资源

* [开发扩展插件](../../../%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97%E4%B8%8E%E7%A4%BA%E4%BE%8B/%E6%8C%89%E6%8F%92%E4%BB%B6%E7%B1%BB%E5%9E%8B/Endpoint%20%E6%8F%92%E4%BB%B6.md) - 了解如何开发与外部系统集成的插件
* [开发 Slack Bot 插件](../../../%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97%E4%B8%8E%E7%A4%BA%E4%BE%8B/%E5%AE%8C%E6%95%B4%E7%A4%BA%E4%BE%8B/Slack%20Bot.md) - 使用反向调用与 Slack 平台集成的示例
* [Bundle 类型插件](Bundle%20%E6%8F%92%E4%BB%B6%E5%8C%85.md) - 了解如何打包使用反向调用的多个插件
* [使用持久化存储](../../%E6%8F%92%E4%BB%B6%E7%B1%BB%E5%9E%8B/%E6%8C%81%E4%B9%85%E5%8C%96%E5%AD%98%E5%82%A8.md) - 通过 KV 存储增强插件能力
