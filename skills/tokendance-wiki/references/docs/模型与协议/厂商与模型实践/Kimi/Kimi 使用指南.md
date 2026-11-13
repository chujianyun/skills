# Kimi 使用指南

本页集中说明 Kimi 模型接入时高频出现的思考参数、采样参数、工具调用和多轮消息问题。模型能力与上下文长度请以 TokenDance 模型页和 Kimi 官方资料为准。

## 接入地址

以下示例使用 OpenAI Chat Completions：

| 项 | 值 |
|---|---|
| 完整接口 | `POST https://tokendance.space/gateway/v1/chat/completions` |
| 鉴权 | `Authorization: Bearer YOUR_KEY` |
| 协议 | `openai:chat-completions` |

## 最短调用

```bash title="cURL"
curl https://tokendance.space/gateway/v1/chat/completions \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "kimi-k3",
    "messages": [{"role": "user", "content": "证明根号 2 是无理数。"}],
    "reasoning_effort": "high",
    "stream": true
  }'
```

## 高频参数问题

### `reasoning_effort` 和 `thinking` 不要混用

| 模型 | 思考参数 |
|---|---|
| `kimi-k3` | 使用顶层 `reasoning_effort`；不要传 `thinking` |
| `kimi-k2.7-code` | 始终思考；通常不传 `thinking`，显式传入时仅使用支持的 enabled/keep 组合 |
| `kimi-k2.6` | 使用 `thinking` 开启、关闭或保留历史思考 |
| `kimi-k2.5` | 可使用 `thinking` 开关思考，但不支持保留历史思考 |

K3 的 `reasoning_effort` 使用厂商支持的档位。切换模型时不要只改 `model`，还应删除另一模型家族的思考参数。

```python title="按模型过滤思考参数"
def normalize_thinking(model: str, payload: dict) -> dict:
    body = dict(payload)
    if model == "kimi-k3":
        body.pop("thinking", None)
    else:
        body.pop("reasoning_effort", None)
    return body
```

### OpenAI SDK 如何传 `thinking`

OpenAI SDK 没有原生 `thinking` 参数，使用 `extra_body`：

```python title="关闭 K2.6 思考"
response = client.chat.completions.create(
    model="kimi-k2.6",
    messages=[{"role": "user", "content": "用一句话总结这段文本。"}],
    extra_body={"thinking": {"type": "disabled"}},
)
```

需要保留历史思考时，使用目标模型支持的 `keep` 配置，并把上一轮完整 assistant message 放回 `messages`。

### 固定采样参数导致 400

部分 Kimi 思考模型对 `temperature`、`top_p`、`n` 和惩罚项有固定要求。很多 OpenAI 项目会全局附带 `temperature=0.2`，切换 Kimi 后可能直接报错。

最稳妥的处理是：只发送任务真正需要的字段，并在 Kimi 适配层删除全局采样参数，而不是猜测一套通用值。

```python title="过滤常见采样字段"
for field in (
    "temperature",
    "top_p",
    "n",
    "presence_penalty",
    "frequency_penalty",
):
    payload.pop(field, None)
```

### `tool_choice: required` 并非都支持

不同 Kimi 模型对 `tool_choice` 的支持范围不同。模型不接受 `required` 时：

1. 改用 `auto`。
2. 缩小当前轮暴露的工具集合。
3. 在提示词中明确必须调用的工具。
4. 在应用层检查返回是否包含 `tool_calls`。

不要把 `required` 作为所有模型的统一默认值。

### 如何读取 `reasoning_content`

思考过程和最终回答是两个字段：

```python
message = response.choices[0].message
reasoning = getattr(message, "reasoning_content", None)
answer = message.content
```

流式响应中分别累计 `delta.reasoning_content` 和 `delta.content`，不要把两者拼成同一个字符串。

### 多轮对话必须回传什么

启用保留式思考或工具调用时，应保存并回传完整 assistant message，包括：

- `content`
- `reasoning_content`
- `tool_calls`

只保留最终文本会丢失模型继续推理和关联工具调用所需的信息。工具执行结果应使用正确的 `tool_call_id` 回传。

## 常见错误

| 现象 | 优先检查 |
|---|---|
| `thinking` 参数不支持 | 是否把 K2.x 参数传给了 K3，或使用了不支持的 `keep` |
| `reasoning_effort` 无效 | 目标模型是否支持该参数和档位 |
| 采样参数报错 | SDK 是否自动附带了非默认 `temperature`、`top_p` 或惩罚项 |
| `tool_choice` 报错 | 当前模型是否支持 `required` |
| 多轮质量突然下降 | 是否完整回传了 assistant message 和工具调用信息 |
| 看不到思考内容 | 是否读取了 `reasoning_content`；流式时是否累计对应 delta |

## 官方资料

- [Kimi 思考模型使用说明](https://platform.kimi.com/docs/guide/use-thinking-models)
- [Kimi 模型参数](https://platform.kimi.com/docs/api/models-overview)
- [Kimi 推理强度](https://platform.kimi.com/docs/guide/use-reasoning-effort)
