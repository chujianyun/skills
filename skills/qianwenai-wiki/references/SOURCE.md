# 来源与快照说明

## 官方来源

- 文档入口：<https://platform.qianwenai.com/docs/developer-guides/getting-started/introduction>
- 完整目录：<https://platform.qianwenai.com/docs/llms.txt>
- 聚合全文：<https://platform.qianwenai.com/docs/llms-full.txt>

千问AI平台页面通过 HTTP `Link` 与 `X-LLMS-TXT` 响应头公开上述机器可读入口。本 Skill 以 `llms.txt` 的全部链接作为完整性基线，逐页下载原始 Markdown 与 OpenAPI JSON。

## 快照范围

快照覆盖 `llms.txt` 当次列出的全部页面，包括：

- Token Plan
- 开发者指南
- API / SDK / CLI 参考
- 资源与计费资料
- 更新日志
- OpenAPI JSON Schema

精确抓取时间、页面数、原始 URL、文件大小和 SHA-256 见 [SNAPSHOT.json](SNAPSHOT.json)。目录导航见 [INDEX.md](INDEX.md)。

## 完整性与更新

`scripts/sync_docs.py` 只接受 `https://platform.qianwenai.com/docs/` 下由官方目录列出的 `.md` 与 `.json` 文件。它先下载到临时目录，校验页面数量、非空内容和哈希后再写入快照；任一页面失败时不会替换旧快照。

为避免上游示例或误提交内容被打包成真实凭据，同步脚本会把符合密钥形态的 `sk-...` 字符串及长 API Key / Token / Secret 赋值统一替换为 `REDACTED`，并把 Tab 统一为四个空格以满足仓库文本规范。`SNAPSHOT.json` 同时记录上游原文哈希、本地处理后哈希、脱敏次数和 Tab 规范化次数，因此本地文件可能不与上游逐字节相同，但技术正文与代码结构保持不变。

离线快照可能落后于官网。价格、额度、模型可用性、区域、限流和版本状态等时效性问题应联网复核。

## 版权与敏感信息

离线文档来源及版权归千问AI平台及相应权利人所有，本仓库不主张上游文档版权。文档中的密钥示例应视为占位符，不得将真实 API Key、Cookie、Token 或账号信息写入 Skill。
