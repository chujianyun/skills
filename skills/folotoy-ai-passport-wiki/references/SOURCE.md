# 来源与范围

- 产品：FoloToy AI Passport。
- 规范来源：<https://ai-passport.folotoy.cn/guides/>。
- 语言与版本：简体中文，教程区当前线上版本；教程没有独立版本号。
- 范围：教程目录页和 8 篇教程，共 9 个页面，完整覆盖所选中文 `/guides/` 范围。该覆盖率不代表整个官网或开发项目都已收录。
- 导航层级：教程中心 → 8 篇同级教程；目录正文保存为 `docs/教程中心/index.md`。
- 交叉核对：教程首页的 8 张导航卡片与 <https://ai-passport.folotoy.cn/sitemap.xml> 中的中文教程条目完全一致。`llms.txt` 与 `llms-full.txt` 在抓取时返回 404，实际使用公开 HTML 正文转换。
- 转换保留：标题、正文、步骤、列表、提示、5 份开发提示词、输入框占位符、步骤锚点和 28 张去重图片；教程区内链接改为本地 Markdown，范围外链接保持官方地址。
- 排除：英文版、社区玩法详情、在线刷机工具、账号与法律页面、官方动态，以及外链开发仓库正文。排除清单见 `wiki-manifest.json`。
- 精确覆盖、来源、逐页与逐资源 SHA-256、最近一次内容变化时间见 `wiki-manifest.json`。

## 可补查的官方来源

- 设备操作与玩法流程：<https://ai-passport.folotoy.cn/guides/>。
- 开发项目：<https://github.com/folotoy/ai-passport>；官网提示词也给出 <https://gitee.com/FoloToy/ai-passport>。
- 需要具体硬件、API 或构建命令时，先阅读开发项目的 `AGENTS.md`、`docs/README.md` 及对应接口和示例。这些材料不在当前离线快照中，引用时标记在线补充。

## 许可与分发

官网页脚标注 `Copyright © 2026 FoloToy. All rights reserved.`。检查了官网用户协议 <https://ai-passport.folotoy.cn/legal/terms/>，未找到本站教程与图片的公开再分发许可。

开发项目的 MIT 许可证属于该项目，不能据此把教程站的材料认定为 MIT。

发布者已明确确认获得本快照教程与图片的再分发授权，并授权将本 Skill 加入公开 Skills 仓库及推送。此项授权确认不等于网站存在通用开放许可证；仓库许可证不会改变上游材料的权利归属。后续扩展来源范围或另行分发时，核对相应授权，并继续保留上游版权与来源说明。
