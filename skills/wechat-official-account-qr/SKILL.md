---
name: wechat-official-account-qr
description: 微信公众号关注二维码生成助手。当用户要根据公众号 ID、微信号、原始 ID 或 `gh_...` 生成公众号二维码、下载成本地图片并在 Agent/Codex 聊天里显示，或不知道如何在微信里找到公众号 ID、需要操作引导图时使用此技能。只适用于微信公众号二维码，不用于小程序码、个人微信二维码或企业微信二维码。
---

# 微信公众号二维码

## Overview

根据微信公众号 ID 生成关注二维码链接，并在用户没有提供 ID 时，用内置引导图帮助用户在微信中找到公众号 ID。

二维码规则：

```text
https://open.weixin.qq.com/qr/code?username={公众号ID}
```

## Workflow

1. If the user provides a公众号 ID, normalize it and generate the QR code URL directly.
2. If the user provides a full QR URL, extract the `username` value and regenerate the canonical URL.
3. If the user does not provide an ID, show the three guide images from `assets/` and ask them to follow the steps to copy the ID.
4. In Agent/Codex chat surfaces, download the QR image to a local file and embed it with an absolute local path. Do not rely on the remote WeChat image URL for Markdown preview.
5. Return the公众号 ID, the canonical URL, and the local image preview.

## Generate QR Code

Use the helper script for deterministic output. Prefer downloading to `~/Downloads/wechat-qrcodes/` so Agent surfaces can render the image from a local absolute path:

```bash
python3 <skill_dir>/scripts/generate_qr.py gh_11eec77a7c51 \
  --download \
  --output ~/Downloads/wechat-qrcodes/gh_11eec77a7c51.jpg
```

Example output:

```markdown
公众号ID：gh_11eec77a7c51
二维码链接：https://open.weixin.qq.com/qr/code?username=gh_11eec77a7c51
本地图片：/Users/example/Downloads/wechat-qrcodes/gh_11eec77a7c51.jpg

![微信公众号二维码](/Users/example/Downloads/wechat-qrcodes/gh_11eec77a7c51.jpg)
```

If the user only wants the URL and does not need an image preview, omit `--download`:

```bash
python3 <skill_dir>/scripts/generate_qr.py gh_11eec77a7c51
```

## Help User Find The ID

When the user does not know the公众号 ID, provide these steps and include the matching images:

1. Open the chat with the公众号, tap the profile icon in the upper-right corner.
   - Image: `assets/step-1-open-profile.jpg`
2. Tap the公众号 name on the profile page.
   - Image: `assets/step-2-tap-name.jpg`
3. In the basic information panel, copy the value shown next to `微信号`; this is the公众号 ID.
   - Image: `assets/step-3-copy-account-id.jpg`

If the user is in a Markdown-capable interface, embed the images with relative paths or absolute copied paths as appropriate for that interface.

## Gotchas

- Do not invent or guess a公众号 ID from the display name. Ask the user to copy it from the guide if it is missing.
- Keep the exact ID casing and characters unless trimming whitespace or extracting from a URL.
- Remote Markdown image previews from `open.weixin.qq.com` can fail in Agent chat surfaces. Download locally before embedding images.
- If local download fails because of network issues, still provide the URL and say the image could not be downloaded.
- This endpoint is for公众号 follow QR codes. Do not use it for mini programs, personal accounts, group chats, or enterprise accounts.
