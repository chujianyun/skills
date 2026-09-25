> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 生成临时 API Key

> 短期有效的临时访问令牌

当应用需要在浏览器或移动端等不可信环境中调用模型服务时，通过安全的后端服务生成临时 API Key，避免暴露永久 API Key。

<Warning>
  临时 API Key 会继承创建它的 API Key 的权限，例如模型访问限制。
</Warning>

## 前提条件

在 [API Key](https://platform.qianwenai.com/home/api-keys) 页面创建永久 API Key，并设置 `DASHSCOPE_API_KEY` 环境变量。详见[配置 API Key](/api-reference/preparation/export-api-key-env)。

## 请求示例

临时 API Key 默认 60 秒后过期，可通过 `expire_in_seconds` 设置 1 到 1,800 秒的有效期。

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## 响应示例

### 成功响应

```json
{
  "token": "st-****",
  "expires_at": 1744080369
}
```

### 成功响应参数

| 参数          | 类型     | 说明                | 示例          |
| ----------- | ------ | ----------------- | ----------- |
| token       | String | 临时 API Key。       | st-\*\*\*\* |
| expires\_at | Number | 过期时间，UNIX 时间戳（秒）。 | 1744080369  |

### 错误响应

```json
{
  "code": "InvalidApiKey",
  "message": "Invalid API-key provided.",
  "request_id": "902fee3b-f7f0-9a8c-96a1-6b4ea25af114"
}
```

### 错误响应参数

| 参数          | 类型     | 说明                                                         | 示例                                   |
| ----------- | ------ | ---------------------------------------------------------- | ------------------------------------ |
| code        | String | 错误码，详见[错误信息说明](/api-reference/preparation/error-messages)。 | InvalidApiKey                        |
| message     | String | 错误信息。                                                      | Invalid API-key provided.            |
| request\_id | String | 请求 ID。                                                     | 902fee3b-f7f0-9a8c-96a1-6b4ea25af114 |

## FAQ

### 能否手动删除临时 API Key？

不能。临时 API Key 到期后自动失效，无法手动删除。
