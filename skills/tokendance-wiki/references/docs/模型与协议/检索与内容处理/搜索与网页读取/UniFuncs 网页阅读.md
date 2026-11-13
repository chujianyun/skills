# UniFuncs 网页阅读

抓取目标 URL 的正文内容，支持网页 / PDF / Word / Excel，返回 Markdown 或纯文本。按次计费，缓存命中享 2 折。

:::group

```bash title="cURL"
curl https://tokendance.space/gateway/unifuncs/web-reader \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://mp.weixin.qq.com/s/wmoNh44A4ofkawPNVx_g6A",
    "format": "md",
    "liteMode": true
  }'
```

```python title="Python"
import requests

resp = requests.post(
    "https://tokendance.space/gateway/unifuncs/web-reader",
    headers={"Authorization": "Bearer YOUR_KEY"},
    json={
        "url": "https://mp.weixin.qq.com/s/wmoNh44A4ofkawPNVx_g6A",
        "format": "md",
        "liteMode": True,
    },
)
print(resp.text)
```

```javascript title="Node.js"
const resp = await fetch("https://tokendance.space/gateway/unifuncs/web-reader", {
  method: "POST",
  headers: {
    "Authorization": "Bearer YOUR_KEY",
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    url: "https://mp.weixin.qq.com/s/wmoNh44A4ofkawPNVx_g6A",
    format: "md",
    liteMode: true,
  }),
});
console.log(await resp.text());
```

:::

### 常用参数

- `url`（必填）：目标 URL
- `format`：`md` / `markdown`（默认）/ `text` / `txt`
- `liteMode`：是否启用可读性修剪，默认 `false`
- `includeImages`：是否包含图片，默认 `true`
- `onlyCSSSelectors` / `waitForCSSSelectors` / `excludeCSSSelectors`：CSS 选择器粒度的抓取控制
- `maxWords`：最大字符数（0–5,000,000，默认 500 万）
- `linkSummary`：是否在尾部追加所有链接，默认 `false`
- `ignoreCache`：忽略缓存，默认 `false`（缓存命中享 2 折）
- `setCookie`：自定义 Cookie，用于需要登录的页面
- `readTimeout` / `extractTimeout`：抓取与提取超时（ms），默认 120000

### 响应

响应体直接是 Markdown / 纯文本字符串。当返回 `format=md` 时，内容形如：

```
Title: <页面标题>
URL Source: <源 URL>

Markdown Content:

<正文>
```
