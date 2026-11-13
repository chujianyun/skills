# 阿里云 Qwen 文本重排

<!-- model-detail-quickstart:start -->

:::group

```bash title="cURL"
curl https://tokendance.space/gateway/alibaba/text-rerank/v1 \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "input": {
      "query": "什么是文本排序模型？",
      "documents": [
        "文本排序模型根据相关性对候选文本重新排序。",
        "量子计算是计算科学的前沿领域。",
        "重排序可以改善 RAG 的检索结果。"
      ]
    },
    "parameters": {
      "top_n": 2,
      "instruct": "Given a web search query, retrieve relevant passages that answer the query."
    }
  }'
```

```python title="Python"
import requests

response = requests.post(
    "https://tokendance.space/gateway/alibaba/text-rerank/v1",
    headers={"Authorization": "Bearer YOUR_KEY"},
    json={
        "model": "MODEL_ID",
        "input": {
            "query": "什么是文本排序模型？",
            "documents": [
                "文本排序模型根据相关性对候选文本重新排序。",
                "量子计算是计算科学的前沿领域。",
                "重排序可以改善 RAG 的检索结果。",
            ],
        },
        "parameters": {"top_n": 2},
    },
    timeout=60,
)
response.raise_for_status()

result = response.json()
for item in result["output"]["results"]:
    print(item["index"], item["relevance_score"])
```

```javascript title="Node.js"
const response = await fetch(
  'https://tokendance.space/gateway/alibaba/text-rerank/v1',
  {
    method: 'POST',
    headers: {
      Authorization: 'Bearer YOUR_KEY',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'MODEL_ID',
      input: {
        query: '什么是文本排序模型？',
        documents: [
          '文本排序模型根据相关性对候选文本重新排序。',
          '量子计算是计算科学的前沿领域。',
          '重排序可以改善 RAG 的检索结果。',
        ],
      },
      parameters: { top_n: 2 },
    }),
  },
);

if (!response.ok) throw new Error(await response.text());
const result = await response.json();
console.log(result.output.results);
```

:::

响应中的 `output.results[].index` 指向原始 `documents` 下标，`relevance_score` 越大表示在本次请求中越相关。

<!-- model-detail-quickstart:end -->

Qwen 文本重排使用阿里云百炼原生嵌套报文，对查询和候选文档进行相关性排序。它不是 TokenDance 的通用
Rerank 报文；当前可用模型及模型 ID 以 TokenDance [模型列表](https://tokendance.space/models)为准。

### 调用地址

```text
POST https://tokendance.space/gateway/alibaba/text-rerank/v1
```

### 请求参数

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `model` | string | 是 | TokenDance 模型 ID |
| `input.query` | string | 是 | 查询文本，不能为空 |
| `input.documents` | string[] | 是 | 待排序的候选文档，1～500 篇，每项均为非空文本 |
| `parameters.top_n` | integer | 否 | 返回相关性最高的前 N 项；省略时返回全部文档 |
| `parameters.instruct` | string | 否 | 排序任务说明，建议使用英文；省略时按问答检索排序 |

### Token 用量与计费

上游计算请求输入量时，会把 query 对每篇候选文档分别计算：

```text
query_tokens × document_count + sum(document_tokens)
```

`top_n` 只控制返回几条结果，不会减少已经送入模型排序的候选文档。需要降低延迟或费用时，应在请求前减少
`documents` 数量或长度。单篇文档和单次请求的 Token 上限可能随模型变化，请以模型页和官方资料为准。

### 输入限制

> 本协议只支持文本。不要在 `documents` 中传 `{"image": "..."}`，否则会返回参数错误。图文、视频
> 重排属于 `qwen3-vl-rerank`，其请求结构和 Token 用量字段与本协议不同。

### 响应与结果

```json
{
  "output": {
    "results": [
      {"index": 0, "relevance_score": 0.9334521178273196},
      {"index": 2, "relevance_score": 0.34100082626411193}
    ]
  },
  "usage": {
    "prompt_tokens": 79,
    "total_tokens": 79
  },
  "request_id": "85ba5752-1900-47d2-8896-23f99b13f6e1"
}
```

结果按 `relevance_score` 从高到低排列；分数只适合在同一次请求内部比较。文本重排模型没有生成式
输出，所以正常响应中 `prompt_tokens` 与 `total_tokens` 相等。文档数量增加会提高两个数值，但不会改变这
一关系；TokenDance 只按一项输入 Token 计费，不会把两个字段重复相加。

该协议不支持 `return_documents`。需要把结果还原为原文时，请使用 `index` 从本次请求的 `documents` 数组
中读取对应项。

完整字段和最新限制请参阅[阿里云百炼文本排序 API](https://help.aliyun.com/zh/model-studio/text-rerank-api)。
