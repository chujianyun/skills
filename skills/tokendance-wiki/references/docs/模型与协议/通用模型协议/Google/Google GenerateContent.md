# Google GenerateContent

::: tip
通用 `Authorization: Bearer YOUR_KEY` 与 Gemini 原生 `x-goog-api-key: YOUR_KEY` 都支持。SDK 会用原生方式自动设置请求头。
:::

:::group

```bash title="cURL"
curl "https://tokendance.space/gateway/v1beta/models/MODEL_ID:generateContent" \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "Hello!"}]}]
  }'
```

```python title="Python"
from google import genai
from google.genai import types

client = genai.Client(
    api_key="YOUR_KEY",
    http_options=types.HttpOptions(base_url="https://tokendance.space/gateway"),
)

response = client.models.generate_content(
    model="MODEL_ID",
    contents="Hello!",
)
print(response.text)
```

```javascript title="Node.js"
import { GoogleGenAI } from '@google/genai';

const ai = new GoogleGenAI({
  apiKey: 'YOUR_KEY',
  httpOptions: { baseUrl: 'https://tokendance.space/gateway' },
});

const response = await ai.models.generateContent({
  model: 'MODEL_ID',
  contents: 'Hello!',
});
console.log(response.text);
```

:::

## Nano Banana 图片生成与编辑

支持 Gemini 原生协议的 Nano Banana 模型沿用 `gemini:generate-content`，通过 `contents[].parts` 传入提示词和参考图。模型是否支持指定尺寸、比例和响应类型，由所选模型与上游决定。

```bash title="图片生成"
curl "https://tokendance.space/gateway/v1beta/models/MODEL_ID:generateContent" \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"role": "user", "parts": [{"text": "一只戴着草帽的橘猫，水彩风格"}]}],
    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
  }'
```

编辑仍使用同一接口，将参考图作为 `inlineData` 放入 parts。`data` 填写图片的纯 Base64 内容，`mimeType` 与图片格式一致。

```bash title="参考图编辑"
curl "https://tokendance.space/gateway/v1beta/models/MODEL_ID:generateContent" \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"role": "user", "parts": [
      {"text": "保留主体，将背景改为海边日落"},
      {"inlineData": {"mimeType": "image/png", "data": "REPLACE_WITH_IMAGE_BASE64"}}
    ]}],
    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
  }'
```

从响应的 `candidates[].content.parts[].inlineData` 读取图片。`thought: true` 的思考过程图片仍会透传，但不计入最终成图张数。多轮编辑请保留模型返回的完整 content，包括 `thoughtSignature`，再追加下一轮用户内容。

流式请求使用 `/v1beta/models/MODEL_ID:streamGenerateContent?alt=sse`。若选择的是 Grsai 异步协议，请使用 [Grsai 图片生成与编辑](../../%E5%A4%9A%E6%A8%A1%E6%80%81%E5%8D%8F%E8%AE%AE/%E5%9B%BE%E5%83%8F%E4%B8%8E%E8%A7%86%E9%A2%91/Grsai%20%E5%9B%BE%E7%89%87%E7%94%9F%E6%88%90%E4%B8%8E%E7%BC%96%E8%BE%91.md) 的提交与查询接口。
