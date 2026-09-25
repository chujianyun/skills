---
name: baize
description: 将公开或用户有权访问的 Wiki 完整转换为面向 Agent 的离线知识 Skill，并按原 Wiki 层级保存 Markdown、生成检索索引和逐文档哈希清单，支持无变化不落盘的手动或自动增量更新。当用户要求把 Wiki、文档站或帮助中心做成 Skill、同步已有 Wiki Skill、保持文档目录树或设置 Wiki Skill 自动更新时使用；不用于只摘要单篇网页或绕过登录、付费墙和访问控制。
---

# 白泽

把面向人浏览的 Wiki 编译成 Agent 能渐进检索、带来源边界且可持续同步的知识 Skill。创建和更新都必须先完成全量导航盘点，再写入目标目录；不能用搜索结果数量代替完整性验证。

## 依赖

确定性脚本只依赖 Python 3.10+ 标准库，先用 `python3 --version` 验证，不需要安装第三方包。缺少兼容 Python 时停止并报告；不要手工替代哈希、原子写入或目录逃逸校验。网页抓取使用当前环境已有的 HTTP、浏览器或官方导出能力，没有固定的付费服务依赖。

## 工作流

复制并持续更新这份清单：

```text
白泽进度：
- [ ] 1. Scope：确认来源、访问权限、语言与完整范围
- [ ] 2. Map：盘点 Wiki 导航树和预期页面数
- [ ] 3. Capture：逐页转换到临时目录并生成 inventory.json
- [ ] 4. Build/Sync：预演哈希差异，再创建或增量更新 Skill
- [ ] 5. Verify：核对覆盖率、目录树、索引、清单和本地检索
- [ ] 6. Install：安装到当前 Agent；需要时配置自动更新
```

### 1. 确定模式、名称与落点

1. 新建时根据 Wiki 的产品名或知识域起一个简短、贴切的 lowercase-hyphen 名称，默认以 `-wiki` 结尾，例如 `qoder-wiki`。不要直接使用完整域名、`docs`、`help-center` 等泛名。
2. 更新时先定位已有 Skill，读取 `references/wiki-manifest.json`，沿用名称、来源范围和路径映射；不要把更新做成第二份 Skill。
3. 按 [位置与安装规则](references/location-and-installation.md) 选择目标：显式路径优先，其次是当前选中的 Skills 仓库或工作目录；没有选中目录时才直接写入当前 Agent 的 Skills 目录。
4. 若同名目录已存在但没有白泽清单，停止并请用户决定新名称或是否接管，不能覆盖。

### 2. 盘点并抓取 Wiki

完整阅读 [抓取与转换协议](references/capture-protocol.md)，先得到导航树、范围边界和预期页面数，再抓正文。优先使用官方导出、官方源码、`llms.txt`/站点地图与 Wiki 自身导航；动态页面再使用可渲染的浏览器工具。

所有材料先写到用 `mktemp -d` 创建的临时目录：

```text
<staging>/
├── inventory.json
├── docs/       # 与 Wiki 导航层级对应的 Markdown
└── assets/     # 可选；承载信息的图片等本地资源
```

若有页面失败、覆盖数不一致、访问范围不明或正文为空，先重试并修正；仍失败就停止，不得声称“完整转换”，也不得用不完整快照覆盖已有 Skill。

### 3. 创建或更新

新建 Skill：

```bash
python3 <baize-root>/scripts/build_wiki_skill.py \
  --staging-dir <staging> \
  --target-parent <target-parent> \
  --name <product-wiki> \
  --title "<Wiki title>" \
  --source-url "<canonical wiki root>" \
  --description "<包含知识范围和真实触发词的 description>"
```

更新已有 Skill 时先预演：

```bash
python3 <skill-root>/scripts/sync_wiki_docs.py \
  --skill-root <skill-root> \
  --staging-dir <staging> \
  --dry-run
```

预演无异常后去掉 `--dry-run`。脚本以规范化 Markdown 的 SHA-256 为准：内容和元数据均未变化时不重写文档、索引或 JSON 清单。发现上游删页或改路径时，默认停止；只有用户明确同意同步删除，或自动更新已获得持续授权，才加 `--prune`，旧文件会移入 `references/.baize-trash/` 而非直接删除。

清单、索引和生成结果的固定结构见 [生成 Skill 契约](references/generated-skill-contract.md)。不得手工伪造哈希或只更新时间戳。

### 4. 验证并安装

至少验证：

1. `inventory.json` 的发现数、成功数、失败列表与实际文件一致。
2. `references/docs/` 的每一级目录都能对应到 Wiki 导航节点，内部链接能落到本地 Markdown。
3. `references/INDEX.md` 能按目录定位全部页面，`scripts/search_docs.py` 能命中 2–3 个代表性问题。
4. `references/wiki-manifest.json` 为每篇文档记录来源 URL、相对路径和 `sha256:` 哈希。
5. `SKILL.md` 只保留检索流程，详细知识位于 `references/docs/`；运行环境自带的 Skill 校验器存在时必须通过。
6. 若目标位于受治理的 Skills 仓库，按仓库规则完成分类注册与校验，不替用户跳过其确认和发布边界。

创建完成后安装到当前 Agent；Skill 已直接创建在当前 Agent 的 Skills 目录时不重复安装。普通环境可先预演再执行：

```bash
python3 <baize-root>/scripts/install_skill.py <skill-root> --dry-run
python3 <baize-root>/scripts/install_skill.py <skill-root>
```

已安装同名 Skill 但内容不同时，脚本要求 `--replace`；只有确认它是同一来源的更新，或用户明确同意覆盖，才使用该参数。

### 5. 手动或自动更新

用户要求更新时重新抓取完整范围到新的临时目录，再运行同步脚本，不在旧正文上做局部猜改。用户明确要求定期自动更新时，完整阅读 [自动更新规则](references/automatic-updates.md)，使用当前 Agent 提供的调度能力创建任务；未明确提出自动更新时不创建后台任务。

## 常见陷阱

- 左侧导航、移动端导航、站点地图和搜索索引可能覆盖不同；先合并去重，再确定完整范围。
- 折叠块、标签页、代码示例和表格属于正文，不能只抓首屏可见文本。
- 抓取时间、构建 ID、随机锚点等易变数据不能写进正文，否则每次都会产生假更新。
- 内部文档链接要改成相对 Markdown 路径；外部链接保留绝对 URL，带凭据或签名参数的 URL 禁止写入 Skill。
- 公开可访问不等于允许公开再分发。许可证不清楚时只生成本地私有 Skill；提交公开仓库、推送或发布前先取得用户确认并保留上游许可说明。
- 自动更新的“无变化”是成功结果。不要为了留下运行痕迹而修改清单时间戳。

## 输出契约

完成后向用户报告：Skill 名称与路径、来源和页面数、覆盖率、创建/变更/未变数量、索引与清单路径、安装位置、验证结果，以及未解决的抓取或许可证风险。若没有变化，明确报告 `UNCHANGED`，并说明没有文件被重写。
