# OpenAI Embeddings

:::group

```bash title="cURL"
curl https://tokendance.space/gateway/v1/embeddings \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "input": "The food was delicious"
  }'
```

```python title="Python"
from openai import OpenAI

client = OpenAI(api_key="YOUR_KEY", base_url="https://tokendance.space/gateway/v1")

response = client.embeddings.create(
    model="MODEL_ID",
    input="The food was delicious",
)
print(response.data[0].embedding[:5])
```

```javascript title="Node.js"
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: 'YOUR_KEY',
  baseURL: 'https://tokendance.space/gateway/v1',
});

const response = await client.embeddings.create({
  model: 'MODEL_ID',
  input: 'The food was delicious',
});
console.log(response.data[0].embedding.slice(0, 5));
```

:::

`input` 支持字符串或字符串数组（批量）。响应中每个 `data[].embedding` 是浮点数数组。
