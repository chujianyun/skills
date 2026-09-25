# 因素 II：用 Git 追踪一切

**法则：如果不在 Git 里，就等于没发生过。**

不只是代码——issues、learnings、会话产物、决策、失败分析、Agent 交接，全部要追踪。

## Git 提供什么

- **历史**：每个决策有提交哈希，可以追溯
- **可比较性**：`git diff` 精确展示知识库的变化
- **协作**：多个 Agent 可以同时处理，Git 的合并语义处理冲突
- **可审计性**：`git log` 就是审计日志，无需导出
- **无供应商锁定**：Markdown 文件，工具无关，人类可读
- **离线优先**：不需要 API 调用，不需要数据库连接
- **免费备份**：每个克隆都是完整副本

## 推荐的 Git 目录结构

```
.beads/                     # issues 追踪
├── bd-001.json
├── bd-002.json
└── graph.json              # 依赖关系图

docs/learnings/             # 经验教训
├── patterns/
│   ├── error-handling.md
│   └── testing-strategies.md
├── failures/
│   └── 2026-01-why-X-failed.md
└── decisions/
    └── adr-001-use-git-for-issues.md

.agents/                    # 会话产物
├── session-2026-04-09.log
└── test-results.json
```

## 典型的外部数据库陷阱

你现在用 Jira 追踪 issues，Notion 存经验，S3 存会话日志。
6 个月后：
- Notion 被重新整理，关键架构决策消失了
- 向量数据库 schema 变了，一半记忆成了孤儿
- 新 Agent 加入需要 5 个系统的凭证才能知道有什么工作

Git 方案：`git clone`，就看到全部历史，不需要任何凭证，不需要任何 API。

## 多 Agent 场景的价值

Agent B 全新启动，克隆仓库，立刻看到：
- 问题历史（尝试了什么，什么有效）
- 经验教训（出现的模式）
- 代码变更（实现细节）
- 会话产物（调试日志）

仓库本身就是交接。不需要口头说明，不需要设置凭证。

## 快速检查

- [ ] issues 是不是存在 Git 里（而不是 Jira/飞书）？
- [ ] 经验教训是不是版本控制的 Markdown（而不是 Notion/Confluence）？
- [ ] 会话产物（测试结果、调试日志）有没有提交或引用？
- [ ] 交接说明有没有写进 Git（而不是口头沟通）？
