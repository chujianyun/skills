# 外部知识库 API

> 外部知识服务必须实现的 API 规范，用于与 Dify 集成

> 本文档由 AI 自动翻译。如有任何不准确之处，请参考 [英文原版](https://docs.dify.ai/en/cloud/use-dify/knowledge/external-knowledge-api.md)。

本页定义了外部知识服务必须实现的 API 协议，以便 Dify 从中检索内容。API 准备就绪后，详见 [连接外部知识库](%E8%BF%9E%E6%8E%A5%E5%A4%96%E9%83%A8%E7%9F%A5%E8%AF%86%E5%BA%93.md) 在 Dify 中完成注册。

## 认证

Dify 在每个请求中将你配置的 API Key 作为 Bearer 令牌发送：

```text theme={null}
Authorization: Bearer {API_KEY}
```

认证逻辑由你自行定义。Dify 仅传递密钥，不会对其进行验证。

## 请求

```text theme={null}
POST {your-endpoint}/retrieval
Content-Type: application/json
Authorization: Bearer {API_KEY}
```

Dify 在你配置的端点 URL 后追加 `/retrieval`。如果注册的地址为 `https://your-service.com`，Dify 将请求发送至 `https://your-service.com/retrieval`。

### 请求体

| 属性 | 必填 | 类型 | 说明 |
| :- | :- | :- | :- |
| `knowledge_id` | 是 | string | 外部系统中知识源的标识符，即连接时填写的 **外部知识库 ID** 字段的值，用于将查询路由到正确的知识源。 |
| `query` | 是 | string | 用户的搜索查询。 |
| `retrieval_setting` | 是 | object | 检索参数。详见 [下文](%E5%A4%96%E9%83%A8%E7%9F%A5%E8%AF%86%E5%BA%93%20API.md#retrieval_setting)。 |
| `metadata_condition` | 否 | object | 元数据筛选条件。详见 [下文](%E5%A4%96%E9%83%A8%E7%9F%A5%E8%AF%86%E5%BA%93%20API.md#metadata_condition)。 |

#### `retrieval_setting`

| 属性 | 必填 | 类型 | 说明 |
| :- | :- | :- | :- |
| `top_k` | 是 | int | 返回结果的最大数量。 |
| `score_threshold` | 是 | float | 最低相似度分数（0-1）。在 Dify 中禁用分数阈值时，此值为 `0.0`。 |

#### `metadata_condition`

> [!NOTE]
>
> Dify 将元数据条件传递给你的 API，但目前未提供供用户配置的界面。此参数仅用于程序化调用。

| 属性 | 必填 | 类型 | 说明 |
| :- | :- | :- | :- |
| `logical_operator` | 否 | string | `and` 或 `or`。默认值：`and`。 |
| `conditions` | 是 | array\[object] | 筛选条件列表。 |

`conditions` 中每个对象的结构：

| 属性 | 必填 | 类型 | 说明 |
| :- | :- | :- | :- |
| `name` | 是 | string | 要筛选的元数据字段名称。 |
| `comparison_operator` | 是 | string | 比较运算符。支持的值见下文。 |
| `value` | 否 | string、number 或 array\[string] | 比较值。使用 `empty` 或 `not empty` 时可省略。 |

> [accordion] 支持的比较运算符
>
> | 运算符 | 说明 |
> | :- | :- |
> | `contains` | 包含某个值 |
> | `not contains` | 不包含某个值 |
> | `start with` | 以某个值开头 |
> | `end with` | 以某个值结尾 |
> | `is` | 等于某个值 |
> | `is not` | 不等于某个值 |
> | `in` | 匹配列表中的任意值 |
> | `not in` | 不匹配列表中的任意值 |
> | `empty` | 为空 |
> | `not empty` | 不为空 |
> | `=` | 等于（数值） |
> | `≠` | 不等于（数值） |
> | `>` | 大于 |
> | `<` | 小于 |
> | `≥` | 大于或等于 |
> | `≤` | 小于或等于 |
> | `before` | 在某个日期之前 |
> | `after` | 在某个日期之后 |

### 请求示例

```json theme={null}
{
    "knowledge_id": "your-knowledge-id",
    "query": "Dify 是什么？",
    "retrieval_setting": {
        "top_k": 3,
        "score_threshold": 0.5
    }
}
```

## 响应

返回 HTTP 200，响应体为包含 `records` 数组的 JSON。如果没有匹配结果，返回空数组：`{"records": []}`。

### `records`

| 属性 | 类型 | 说明 |
| :- | :- | :- |
| `content` | string | 检索到的文本分段。Dify 将其作为传递给 LLM 的上下文。 |
| `score` | float | 相似度分数（0-1）。用于分数阈值过滤和结果排序。 |
| `title` | string | 源文档标题。 |
| `metadata` | object | 由 Dify 保留的任意键值对。 |

Dify 不会拒绝缺少字段的记录，但缺少 `content` 或 `score` 将导致结果不完整或无法排序。

> [!WARNING]
>
> 记录中的 `metadata` 必须是对象（`{}`），不能为 `null`。`null` 值将导致 Dify 检索流程出错。

### 响应示例

```json theme={null}
{
    "records": [
        {
            "content": "这是外部知识库的文档。",
            "score": 0.98,
            "title": "knowledge.txt",
            "metadata": {
                "path": "s3://dify/knowledge.txt",
                "description": "dify 知识文档"
            }
        },
        {
            "content": "GenAI 应用的创新引擎",
            "score": 0.66,
            "title": "introduce.txt",
            "metadata": {}
        }
    ]
}
```

## 错误处理

Dify 检查响应的 HTTP 状态码。非 200 状态码将触发错误并展示给用户。

可选择在 JSON 中返回结构化的错误信息：

| 属性 | 类型 | 说明 |
| :- | :- | :- |
| `error_code` | int | 自定义的应用级错误码。 |
| `error_msg` | string | 可读的错误描述。 |

以下是建议的错误码，仅为约定，Dify 不强制要求：

| 错误码 | 建议用途 |
| :- | :- |
| 1001 | 无效的 Authorization 请求头格式 |
| 1002 | 认证失败 |
| 2001 | 知识库不存在 |

### 错误响应示例

```json theme={null}
{
    "error_code": 1002,
    "error_msg": "Authorization failed. Please check your API key."
}
```
