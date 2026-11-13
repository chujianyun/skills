# DeepSeek 网页搜索

:::group

```bash title="cURL"
curl https://tokendance.space/gateway/deepseek/v1/tools/search \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"DeepSeek site:deepseek.com","count":3,"need_content":true}'
```

```python title="Python"
import requests

response = requests.post(
    "https://tokendance.space/gateway/deepseek/v1/tools/search",
    headers={"Authorization": "Bearer YOUR_KEY"},
    json={"query": "DeepSeek site:deepseek.com", "count": 3, "need_content": True},
)
response.raise_for_status()
for result in response.json()["results"]:
    print(result["title"], result["url"], result["summary"])
```

```javascript title="Node.js"
const response = await fetch('https://tokendance.space/gateway/deepseek/v1/tools/search', {
  method: 'POST',
  headers: { Authorization: 'Bearer YOUR_KEY', 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: 'DeepSeek site:deepseek.com', count: 3, need_content: true }),
});
if (!response.ok) throw new Error(await response.text());
const data = await response.json();
console.log(data.results);
```

:::

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `query` | string | 是 | 搜索词，1～128 个 Unicode 字符，不能全为空白；支持 `site:`、`-site:`、引号精确匹配等搜索语法 |
| `count` | integer | 否 | 返回条数，1～50，默认 `10` |
| `ori_question` | string / null | 否 | 触发搜索的原始问题，1～128 个字符；`null` 表示未提供 |
| `localization` | string | 否 | 用于优先返回本地结果的 IP 地址，默认 `""` |
| `need_content` | boolean | 否 | 是否返回网页正文，默认 `false` |

### 返回示例

以下仅展示主要字段：

```json
{
  "results": [
    {
      "title": "DeepSeek API 文档",
      "url": "https://api-docs.deepseek.com/",
      "snippet": "DeepSeek API 使用指南。",
      "summary": "介绍 API 调用方式、请求参数和返回格式。",
      "content": "# DeepSeek API\n\n文档正文……"
    }
  ]
}
```

`results` 为搜索结果数组；`snippet` 是短摘要，`summary` 是长摘要，`content` 是正文。
`need_content=false` 或正文缺失时，`content` 为 `""`；无匹配结果时返回 `{"results":[]}`。
每条结果还包含排序分数 `rerank_score`、站点名称 `site_name`、图标 `site_icon`、发布时间 `date` 和权威性 `authority`。
