---
name: alltuu-downloader
description: 喔图(alltuu.com)云摄影相册批量下载工具。当用户需要从 alltuu.com / m.alltuu.com 相册批量下载原图时使用此技能。支持下载原图（6720x4480 级别），自动处理签名URL，并发下载。适用于 alltuu.com/album/ 相册链接。
---

# 喔图相册下载器

从喔图云摄影（alltuu.com）相册批量下载原图。

## 使用场景

当用户提供以下类型的链接时使用此技能：
- `https://m.alltuu.com/album/XXXXXXXX/?menu=live`
- `https://www.alltuu.com/album/XXXXXXXX/`
- 任何包含 alltuu.com 的相册链接

## 前置条件

1. **Chrome Canary** 需要运行并开启远程调试端口（默认 9222）
2. **Node.js** 已安装
3. **ws** npm 包已安装（脚本会提示安装方式）

### 启动 Chrome Canary

```bash
/Applications/Google\ Chrome\ Canary.app/Contents/MacOS/Google\ Chrome\ Canary \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-canary-debug-profile \
  --proxy-server="http://127.0.0.1:7890" &
```

### 安装 ws 依赖

```bash
cd /tmp && npm init -y && npm install ws
```

## 工作流程

### 1. 提取相册 ID

从 URL 中提取相册 ID（通常是 10 位数字或短码）。

**示例：**
- URL: `https://m.alltuu.com/album/1644727243/?menu=live`
- 相册 ID: `1644727243`

### 2. 创建下载目录

在用户指定位置创建目录（默认 `~/Downloads/alltuu`），也可自定义，如 `~/Downloads/樱花`。

### 3. 执行下载

```bash
cd /tmp && node <skill_dir>/scripts/download.js \
  --album <albumId> \
  --output <download_dir> \
  --concurrency 5
```

**参数说明：**

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--album` | 相册 ID（必需） | 无 |
| `--output` | 下载保存目录 | `~/Downloads/alltuu` |
| `--concurrency` | 并发下载数 | 5 |
| `--cdp-port` | Chrome CDP 端口 | 9222 |

### 4. 下载结果

脚本会显示每张照片的下载状态：
```
✅ photo_001.jpg (6720x4480) 11.6MB
✅ photo_002.jpg (6720x4480) 7.5MB
⏭️  photo_003.jpg (already exists, 4.4MB)
❌ Failed: HTTP 403

🎉 Done! Success: 60, Failed: 0
📁 Saved to: /Users/.../Downloads/樱花
```

## 技术原理

alltuu.com 是纯 SPA 应用，照片数据通过前端 JS 动态加载，图片存储在阿里云 OSS，需要签名 URL 才能访问。

脚本通过 Chrome CDP 协议：
1. 打开相册页面，等待 JS 渲染
2. 拦截 `v4c.alltuu.com` 的 `fpl`（fetch photo list）API 响应
3. 从响应 JSON 中提取各尺寸签名 URL
4. 优先下载 `ol`（original，原图），回退到 `url1920` → `bl` → `sl`

### URL 类型说明

| 字段 | 域名 | 说明 |
|------|------|------|
| `ol` | uio.alltuu.com | 原图（最大尺寸） |
| `url1920` | uip.alltuu.com | 1920px 版本 |
| `bl` | uib.alltuu.com | 大图 |
| `sl` | uis.alltuu.com | 缩略图 |
| `ssl` | uis.alltuu.com | 小方图（200x200） |

## 故障排查

### Chrome 未运行
```
Error: Cannot connect to Chrome on port 9222
```
**解决**：启动 Chrome Canary（见前置条件）。

### 相册加载失败
```
Failed to capture photo list API response
```
**可能原因**：
- 相册需要密码或登录
- 相册 ID 不正确
- 网络问题

**解决**：在 Chrome Canary 中手动打开相册链接确认能正常访问。

### 下载 403
**原因**：签名 URL 过期（有效期约 30 天）。
**解决**：重新运行脚本获取新的签名 URL。

### 缺少 ws 模块
```
Missing dependency: ws
```
**解决**：`cd /tmp && npm init -y && npm install ws`

## 注意事项

1. **需要 Chrome Canary**：脚本依赖浏览器渲染获取签名 URL，纯 HTTP 请求无法绕过
2. **签名有时效**：OSS 签名 URL 有过期时间，下载时效内使用即可
3. **相册权限**：仅支持公开相册，需要密码的相册需先在浏览器中解锁
4. **断点续传**：已下载的文件会自动跳过，可安全重复运行
