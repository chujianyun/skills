# UniFuncs 实时搜索

一次调用即可拿到联网搜索结果，按次计费。请求体仅需提供 `query`，可选 `count`（每页 1-50，默认 10）、`page`、`freshness`（`Day`/`Week`/`Month`/`Year`）、`includeImages`、`format`（`json` 默认 / `markdown` / `text`）。

:::group

```bash title="cURL"
curl https://tokendance.space/gateway/unifuncs/web-search \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "UniFuncs",
    "count": 5
  }'
```

```python title="Python"
import requests

resp = requests.post(
    "https://tokendance.space/gateway/unifuncs/web-search",
    headers={"Authorization": "Bearer YOUR_KEY"},
    json={"query": "UniFuncs", "count": 5},
)
data = resp.json()
for item in data["data"]["webPages"]:
    print(item["name"], item["url"])
```

```javascript title="Node.js"
const resp = await fetch("https://tokendance.space/gateway/unifuncs/web-search", {
  method: "POST",
  headers: {
    "Authorization": "Bearer YOUR_KEY",
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ query: "UniFuncs", count: 5 }),
});
const data = await resp.json();
for (const item of data.data.webPages) {
  console.log(item.name, item.url);
}
```

:::

### 响应字段

- `data.webPages[]`：网页搜索结果，每项含 `name` / `url` / `displayUrl` / `snippet` / `summary` / `siteName` / `siteIcon` / `datePublished`
- `data.images[]`：当 `includeImages=true` 时返回的图片结果
- `requestId`：用于排查的请求 ID
