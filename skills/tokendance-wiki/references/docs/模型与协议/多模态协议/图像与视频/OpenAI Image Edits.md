# OpenAI Image Edits

```bash title="cURL"
curl -sS https://tokendance.space/gateway/v1/images/edits \
  -H "Authorization: Bearer YOUR_KEY" \
  -F "model=MODEL_ID" \
  -F "image[]=@input.png" \
  -F 'prompt=把图片背景替换为柔和的浅蓝色'
```

请求使用 `multipart/form-data`，添加多张参考图时重复传入 `image[]`。当前接口仅支持非流式响应；
编辑结果位于 `data[0].b64_json` 或 `data[0].url`。
