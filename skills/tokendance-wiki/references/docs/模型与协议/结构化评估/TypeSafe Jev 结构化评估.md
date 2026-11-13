# TypeSafe Jev 结构化评估

:::group

```bash title="cURL"
curl https://tokendance.space/gateway/typesafe/v1/systemone \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "state": "Help! My payment failed.",
    "questions": {"is_urgent": {"type": "noul", "instructions": "Is this urgent?"}}
  }'
```

```python title="Python"
import requests

response = requests.post(
    "https://tokendance.space/gateway/typesafe/v1/systemone",
    headers={"Authorization": "Bearer YOUR_KEY"},
    json={"model": "MODEL_ID", "state": "Help! My payment failed.",
          "questions": {"is_urgent": {"type": "noul", "instructions": "Is this urgent?"}}},
)
print(response.json())
```

```javascript title="Node.js"
const response = await fetch('https://tokendance.space/gateway/typesafe/v1/systemone', {
  method: 'POST',
  headers: { Authorization: 'Bearer YOUR_KEY', 'Content-Type': 'application/json' },
  body: JSON.stringify({
    model: 'MODEL_ID',
    state: 'Help! My payment failed.',
    questions: { is_urgent: { type: 'noul', instructions: 'Is this urgent?' } },
  }),
});
console.log(await response.json());
```

:::
