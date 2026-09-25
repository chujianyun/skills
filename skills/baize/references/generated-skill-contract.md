# 生成 Wiki Skill 契约

## 固定结构

```text
<product-wiki>/
├── SKILL.md
├── README.md
├── agents/openai.yaml
├── references/
│   ├── INDEX.md
│   ├── SOURCE.md
│   ├── UPDATE.md
│   ├── wiki-manifest.json
│   ├── docs/<wiki navigation tree>/*.md
│   └── assets/<downloaded assets>
└── scripts/
    ├── search_docs.py
    └── sync_wiki_docs.py
```

- `SKILL.md` 是 Agent 的检索与回答入口，不复制整个目录索引。
- `INDEX.md` 列出目录概览、全部页面、路径和来源，供浏览定位。
- `SOURCE.md` 记录来源根、范围、语言、许可证和快照边界。
- `UPDATE.md` 记录独立更新协议；生成后的 Skill 不依赖白泽仍可同步。
- `wiki-manifest.json` 是更新状态的唯一事实来源。
- `references/docs/` 保持 Wiki 的文档目录树，`references/assets/` 保存必要的本地资源。

## 清单语义

清单使用 `schema_version: 1`，`documents` 以本地 Markdown 相对路径为 key。每个文档至少记录：

```json
{
  "title": "快速开始",
  "source_url": "https://docs.example.com/zh/getting-started",
  "source_path": "/zh/getting-started",
  "local_path": "快速入门/快速开始.md",
  "content_hash": "sha256:<64 hex characters>",
  "updated_at": "2026-08-31T10:00:00Z"
}
```

`content_hash` 基于实际写入文件的规范化 UTF-8 Markdown：统一 LF、Unicode NFC、去掉行尾空白并保证单个末尾换行。图片等二进制资产按原始 bytes 计算 SHA-256。

同一次同步中：

- 内容哈希、标题、来源和路径都相同：文档、索引、清单全部不写。
- 只有部分页面变化：只写变化页面；未变页面保留原 mtime 和 `updated_at`。
- 标题、来源或路径变化：属于元数据变化，更新清单和索引。
- 上游删页或改路径：默认停止；`--prune` 后移出活动文档树并归档到 `references/.baize-trash/`。
- 抓取不完整：默认整次拒绝，不把部分结果覆盖到旧快照。

不要单独维护“最后检查时间”。没有内容或元数据变化时修改时间戳会破坏 no-op 语义；一次无变化检查只写到命令输出或调度运行记录。

## 索引语义

`INDEX.md` 由同步脚本生成，至少包含：

- 来源根和文档总数
- 顶层目录及文档数量
- 可复制的目录树
- 每篇文档的相对路径、标题、简短摘要、关键词和来源 URL

Agent 日常问答优先运行 `scripts/search_docs.py`；只有要浏览主题结构或搜索词不确定时才读取完整索引。索引是导航，不是正文摘要合集。

## 生成 Skill 的回答契约

回答 Wiki 问题时：

1. 先搜索，再读取最相关且互补的 1–3 篇本地文档。
2. 只根据已读取资料给出版本、命令、配置和 API，不凭记忆补全。
3. 列出实际使用的 `references/docs/...` 路径；需要在线补充时明确标注。
4. 证据不足时说明缺口和搜索词，不把未覆盖内容说成不存在。
