# 字节 Ark Image Generations

同步协议，支持返回图片 URL 或 Base64。

### 文生图

```bash title="cURL"
curl https://tokendance.space/gateway/ark/v3/images/generations \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "prompt": "一张商业摄影感的厨房台面静物，透明玻璃杯里装着柠檬气泡水，清晨侧光，浅景深，干净白色背景。",
    "size": "2K",
    "output_format": "jpeg",
    "response_format": "url",
    "watermark": false
  }'
```

### 图文生图

```bash title="cURL"
curl https://tokendance.space/gateway/ark/v3/images/generations \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "prompt": "保留原图人物轮廓和站姿，将背景改成清晨的海边栈道，服装改为浅色风衣，整体色调柔和自然。",
    "image": "https://example.com/input.png",
    "size": "2K",
    "output_format": "jpeg",
    "response_format": "url",
    "watermark": false
  }'
```

### 多参考图生图

```bash title="cURL"
curl https://tokendance.space/gateway/ark/v3/images/generations \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "prompt": "以图 1 的人物为主体，参考图 2 的配色和夹克款式，生成一张城市街拍风半身照。",
    "image": [
      "https://example.com/person.png",
      "https://example.com/outfit.png"
    ],
    "size": "2K",
    "output_format": "jpeg",
    "response_format": "url",
    "watermark": false
  }'
```

组图、联网搜索、流式输出和完整参数说明见 [Seedream 系列](../../%E5%8E%82%E5%95%86%E4%B8%8E%E6%A8%A1%E5%9E%8B%E5%AE%9E%E8%B7%B5/%E5%AD%97%E8%8A%82/Seedream%20%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97.md)。
