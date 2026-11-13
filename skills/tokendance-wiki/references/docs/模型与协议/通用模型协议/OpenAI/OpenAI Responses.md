# OpenAI Responses

:::group

```bash title="cURL"
curl https://tokendance.space/gateway/v1/responses \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "input": "Hello!"
  }'
```

```python title="Python"
from openai import OpenAI

client = OpenAI(api_key="YOUR_KEY", base_url="https://tokendance.space/gateway/v1")

response = client.responses.create(
    model="MODEL_ID",
    input="Hello!"
)
print(response.output_text)
```

```javascript title="Node.js"
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: 'YOUR_KEY',
  baseURL: 'https://tokendance.space/gateway/v1',
});

const response = await client.responses.create({
  model: 'MODEL_ID',
  input: 'Hello!',
});
console.log(response.output_text);
```

:::

## 多轮对话

只传本轮输入，上文由上游按 `previous_response_id` 续接，请求体和往返数据量都更小。

:::group

```bash title="cURL"
curl https://tokendance.space/gateway/v1/responses \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "input": "我刚才让你记的数字是多少？",
    "previous_response_id": "上一轮响应的 id"
  }'
```

```python title="Python"
first = client.responses.create(model="MODEL_ID", input="记住数字 42")

second = client.responses.create(
    model="MODEL_ID",
    input="我刚才让你记的数字是多少？",
    previous_response_id=first.id,
)
print(second.output_text)
```

```javascript title="Node.js"
const first = await client.responses.create({
  model: 'MODEL_ID',
  input: '记住数字 42',
});

const second = await client.responses.create({
  model: 'MODEL_ID',
  input: '我刚才让你记的数字是多少？',
  previous_response_id: first.id,
});
console.log(second.output_text);
```

:::

## 流式

```python title="Python"
stream = client.responses.create(
    model="MODEL_ID",
    input="数到 5",
    stream=True,
)
for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
```
