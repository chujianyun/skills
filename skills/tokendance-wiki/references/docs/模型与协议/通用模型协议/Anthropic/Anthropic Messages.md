# Anthropic Messages

::: tip
通用 `Authorization: Bearer YOUR_KEY` 与 Anthropic 原生 `x-api-key: YOUR_KEY` 都支持。下方示例用 SDK 默认形式。
:::

:::group

```bash title="cURL"
curl https://tokendance.space/gateway/v1/messages \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "MODEL_ID",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

```python title="Python"
import anthropic

client = anthropic.Anthropic(
    api_key="YOUR_KEY",
    base_url="https://tokendance.space/gateway",
)

message = client.messages.create(
    model="MODEL_ID",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}],
)
print(message.content[0].text)
```

```javascript title="Node.js"
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: 'YOUR_KEY',
  baseURL: 'https://tokendance.space/gateway',
});

const message = await client.messages.create({
  model: 'MODEL_ID',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Hello!' }],
});
console.log(message.content[0].text);
```

:::

### Claude Code 集成

把环境变量 `ANTHROPIC_BASE_URL` 指向词元跳动后，Claude Code 会直接以本协议通信。详见 [Claude Code 集成文档](../../../%E9%9B%86%E6%88%90%E6%8C%87%E5%8D%97/%E7%BC%96%E7%A8%8B%E4%B8%8E%20Agent%20%E5%B7%A5%E5%85%B7/Claude%20Code.md)。
