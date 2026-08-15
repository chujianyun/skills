> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 对话管理

> 自动管理的多轮对话上下文

Conversations API 自动管理跨设备、跨会话的多轮对话上下文。配合 Responses API 使用，无需手动管理，即可跨会话自动关联历史上下文。

使用示例和多轮对话模式请参阅[多轮对话](/developer-guides/run-and-scale/multi-turn#使用-conversations)。

## 服务端点

SDK 的 `base_url`：`https://dashscope.aliyuncs.com/api/v2/apps/protocols/compatible-mode/v1`

HTTP 基础端点：`https://dashscope.aliyuncs.com/api/v2/apps/protocols/compatible-mode/v1/conversations`

## 接口列表

| 接口                                                                      | 说明            |
| ----------------------------------------------------------------------- | ------------- |
| [创建对话](/api-reference/platform-api/conversations/create-conversation)   | 创建对话，可选包含初始消息 |
| [查询对话](/api-reference/platform-api/conversations/retrieve-conversation) | 根据 ID 查询对话    |
| [更新对话](/api-reference/platform-api/conversations/update-conversation)   | 更新对话的元数据      |
| [删除对话](/api-reference/platform-api/conversations/delete-conversation)   | 删除对话          |
| [添加消息](/api-reference/platform-api/conversations/create-items)          | 向对话中添加消息      |
| [查询消息列表](/api-reference/platform-api/conversations/list-items)          | 列出对话中的消息      |
| [查询消息](/api-reference/platform-api/conversations/retrieve-item)         | 根据 ID 查询消息    |
| [删除消息](/api-reference/platform-api/conversations/delete-item)           | 删除消息          |

## 限制

- 创建和添加操作中，`items` 数组最多包含 20 条消息。
- 元数据最多 16 个键值对（键最长 64 字符，值最长 512 字符）。
- 会话信息保留最近 7 天内的最新 100 条，超出时间或数量限制的内容将自动清理。
