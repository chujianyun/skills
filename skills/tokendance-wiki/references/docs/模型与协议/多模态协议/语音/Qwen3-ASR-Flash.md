# Qwen3-ASR-Flash

通过 Chat Completions 提交一段可访问的短音频，获得转写文本。

### cURL

将 `YOUR_KEY` 换成词元跳动 API Key，将音频 URL 换成自己的 WAV 文件。

```bash
curl https://tokendance.space/gateway/v1/chat/completions \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "messages": [{
      "role": "user",
      "content": [{"type": "input_audio", "input_audio": {"data": "https://example.com/audio.wav"}}]
    }]
  }'
```

识别文本在 `choices[0].message.content`；响应的 `usage.seconds` 是音频秒数。
