---
name: qoder-wiki
description: Qoder 官方文档知识库，包含产品介绍、用户指南、功能配置、扩展能力、账户定价和故障排查。当用户询问 Qoder 相关问题（如安装、使用、功能、定价、快捷键、MCP、Skills、Quest Mode、Repo Wiki 等）时使用此 skill。
---

# Qoder Wiki

Qoder 官方文档知识库，提供产品使用指南和技术参考。已于 2026-04-12 按 `https://docs.qoder.com/zh` 左侧导航补齐缺失文档。

## 使用方式

1. 首先查阅 [INDEX.md](INDEX.md) 获取文档索引和内容概览
2. 根据用户问题定位相关文档
3. 使用 Read 工具读取对应的 docs/ 目录下的文档
4. 如文档信息不足，再考虑联网搜索补充

## 文档结构

```
docs/
├── 快速入门/          # 产品概述、安装登录、快速开始
├── 用户指南/          # 模型、Ask/Agent/Experts、工具、Quest、NEXT、Repo Wiki
├── 上下文/            # 代码库索引、@ Mention、规则、记忆
├── 拓展能力/          # Skills、Commands、自定义智能体、MCP、Hooks、Deeplinks
├── 配置/              # 快捷键、网络代理
├── 账户/              # 定价、Credits、账单、Teams
├── 事件/              # 推荐计划、推荐条款、模型活动、限时优惠
├── 支持/              # FAQ、故障排查、MCP常见问题
└── 其他产品/          # JetBrains 插件、CLI、QoderWork 概览
```

## 常见问题分类

| 问题类型 | 参考文档 |
|---------|---------|
| 什么是 Qoder | docs/快速入门/产品概述.md |
| 如何安装使用 | docs/快速入门/快速开始.md |
| 智能会话/Agent模式 | docs/用户指南/智能会话概述.md |
| Ask / Agent / Experts | docs/用户指南/Ask模式.md, docs/用户指南/Agent模式.md, docs/用户指南/Experts模式.md |
| 模型选择/自定义模型 | docs/用户指南/模型选择器.md, docs/用户指南/自定义模型.md |
| Quest Mode | docs/用户指南/Quest Mode.md |
| 代码补全 NEXT | docs/用户指南/行间建议预测NEXT.md |
| 行间会话 / Diff / 工具 | docs/用户指南/行间会话.md, docs/用户指南/Diff视图.md, docs/用户指南/工具.md |
| MCP 配置 | docs/拓展能力/MCP.md |
| Skills 使用 | docs/拓展能力/Skills.md |
| Hooks 配置 | docs/拓展能力/Hooks.md |
| 自定义规则 | docs/上下文/规则.md |
| 快捷键 | docs/配置/快捷键.md |
| 定价方案 | docs/账户/定价.md, docs/账户/价格.md (两个文件都要看！)|
| Teams 组织版 | docs/账户/Teams价格.md, docs/账户/开始使用Teams.md, docs/账户/成员和角色.md |
| CLI / JetBrains / QoderWork | docs/其他产品/CLI快速上手.md, docs/其他产品/JetBrains插件概览.md, docs/其他产品/QoderWork概览.md |
| 故障排查 | docs/支持/FAQ.md, docs/支持/故障排查指南.md |
