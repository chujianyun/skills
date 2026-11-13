# OpenAI Chat Completions

:::group

```bash title="cURL"
curl https://tokendance.space/gateway/v1/chat/completions \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

```python title="Python"
from openai import OpenAI

client = OpenAI(api_key="YOUR_KEY", base_url="https://tokendance.space/gateway/v1")

response = client.chat.completions.create(
    model="MODEL_ID",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

```javascript title="Node.js"
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: 'YOUR_KEY',
  baseURL: 'https://tokendance.space/gateway/v1',
});

const response = await client.chat.completions.create({
  model: 'MODEL_ID',
  messages: [{ role: 'user', content: 'Hello!' }],
});
console.log(response.choices[0].message.content);
```

:::

设置 `stream: true` 即可启用 SSE 流式响应。

:::group

```python title="Python"
stream = client.chat.completions.create(
    model="MODEL_ID",
    messages=[{"role": "user", "content": "Hello!"}],
    stream=True
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

```javascript title="Node.js"
const stream = await client.chat.completions.create({
  model: 'MODEL_ID',
  messages: [{ role: 'user', content: 'Hello!' }],
  stream: true,
});
for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content || '');
}
```

:::
