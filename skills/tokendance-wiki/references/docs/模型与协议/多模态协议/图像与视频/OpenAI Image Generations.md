# OpenAI Image Generations

:::group

```bash title="cURL"
curl https://tokendance.space/gateway/v1/images/generations \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "prompt": "A cute cat playing with a ball of yarn",
    "n": 1,
    "size": "1024x1024"
  }'
```

```python title="Python"
from openai import OpenAI

client = OpenAI(api_key="YOUR_KEY", base_url="https://tokendance.space/gateway/v1")

response = client.images.generate(
    model="MODEL_ID",
    prompt="A cute cat playing with a ball of yarn",
    n=1,
    size="1024x1024",
)
print(response.data[0].url)
```

```javascript title="Node.js"
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: 'YOUR_KEY',
  baseURL: 'https://tokendance.space/gateway/v1',
});

const response = await client.images.generate({
  model: 'MODEL_ID',
  prompt: 'A cute cat playing with a ball of yarn',
  n: 1,
  size: '1024x1024',
});
console.log(response.data[0].url);
```

:::
