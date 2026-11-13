# DeepSeek 网页抓取

:::group

```bash title="cURL"
curl https://tokendance.space/gateway/deepseek/v1/tools/fetch \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://api-docs.deepseek.com/zh-cn/guides/search/"}'
```

```python title="Python"
import requests

response = requests.post(
    "https://tokendance.space/gateway/deepseek/v1/tools/fetch",
    headers={"Authorization": "Bearer YOUR_KEY"},
    json={"url": "https://api-docs.deepseek.com/zh-cn/guides/search/"},
)
response.raise_for_status()
page = response.json()
print(page["title"])
print(page["content"])
```

```javascript title="Node.js"
const response = await fetch('https://tokendance.space/gateway/deepseek/v1/tools/fetch', {
  method: 'POST',
  headers: { Authorization: 'Bearer YOUR_KEY', 'Content-Type': 'application/json' },
  body: JSON.stringify({ url: 'https://api-docs.deepseek.com/zh-cn/guides/search/' }),
});
if (!response.ok) throw new Error(await response.text());
const page = await response.json();
console.log(page.title, page.content);
```

:::

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `url` | string | 是 | 目标网页地址，最长 8192 个字符；必须是包含主机名的 HTTP/HTTPS URL，且不能携带用户名或密码 |

### 返回示例

```json
{
  "title": "网页搜索与抓取",
  "content": "# 网页搜索与抓取\n\nSearch 搜索网页，Fetch 提取网页正文。"
}
```

`title` 是页面标题，缺失时为 `""`；`content` 是抓取后的 Markdown 正文。
