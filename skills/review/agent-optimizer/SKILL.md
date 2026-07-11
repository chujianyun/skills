---
name: agent-optimizer
description: Agent 设计顾问与审查工具。基于 12-Factor AgentOps 最佳实践，用于：(1) 探讨 Agent 架构设计方案；(2) 审查现有 Agent/Skill/工作流的设计，发现问题，给出改进建议。触发词：审查我的 agent、帮我分析这个 skill、agent 设计、agent 优化、帮我 review 这个工作流、这个 agent 有什么问题、怎么设计 agent、agent 架构咨询。
---

# Agent Optimizer

基于 **12-Factor AgentOps** 框架，提供 Agent 设计咨询和现有 Agent/Skill 的问题审查与优化建议。

## 核心框架：12-Factor AgentOps

原文来源：https://www.12factoragentops.com  
中文翻译参考：`~/Documents/working/translations/12-factor-agentops/`

12 个因素分三层：

**基础层（I–III）**：单 Agent 可靠性
- **I. 上下文即一切** — 精确管理 context window，按阶段加载，主动压缩
- **II. 用 Git 追踪一切** — issues/learnings/handoffs 全部放 Git，不依赖外部平台
- **III. 一个 Agent 一个任务** — 每次任务用全新 context，禁止复用饱和窗口

**质量层（IV–VI）**：确保工作质量
- **IV. 构建前先调研** — 任何实现前必须有独立调研阶段，产出调研文档
- **V. 外部验证** — Agent 不给自己打分，验证必须来自外部（不同 Agent/模型/测试/人工）
- **VI. 锁定前进的进度** — 通过验证的工作不可回退，形成棘轮效应

**学习层（VII–IX）**：从经验复利
- **VII. 提取经验教训** — 每次会话产出两个成果：工作产物 + 经验教训文档
- **VIII. 知识复利** — 知识必须自动回流：提取→过滤→存储→注入→引用→衰减
- **IX. 衡量重要的事** — 追踪目标达成度，而非活动指标；休眠即成功

**规模层（X–XII）**：多 Agent 工作流
- **X. 隔离工作单元** — 每个 Worker 独立 worktree + 独立 context，零共享可变状态
- **XI. 层级化监督** — 升级流向上传递，不横向流转；工作节点快速失败
- **XII. 从失败中收获智慧** — 失败尝试与成功同等严格地提取和索引

详细说明见 `references/` 目录下各因素的参考文档。

---

## 工作模式

### 模式一：设计咨询

用户提出 Agent 设计问题时：

1. 弄清楚用户的**目标**和**约束**（单 Agent 还是多 Agent？是否已有工作流？）
2. 对照 12 个因素，给出具体设计建议
3. 按层次推进：先基础层够用再考虑规模层
4. 提供具体的结构示例（文件结构、Prompt 设计、交接格式等）

**常见设计问题清单**（引导对话用）：
- context 是一直堆还是按阶段清理？
- 有没有独立的调研阶段产出调研文档？
- 验证是由执行者本身完成的吗？
- 知识/教训有没有写回去并能被下次会话检索到？
- 多 Agent 时有没有共享目录或共享 context？

### 模式二：设计审查

用户提交现有 Agent/Skill/工作流时：

1. 先让用户描述（或直接读取）设计内容
2. 按 12 因素逐条扫描，标注违反的因素
3. 输出**审查报告**（格式见下）
4. 按严重程度排序，优先指出影响最大的问题

**审查报告格式：**

```
## Agent 审查报告

### 总体评分
[对照 12 因素的覆盖情况，给出健康度评估]

### 发现的问题

#### 🔴 严重问题（会直接导致失败或错误）
- [问题描述] → 违反因素：[X]
  改进建议：[具体怎么做]

#### 🟡 改进项（影响质量或效率）
- [问题描述] → 违反因素：[X]
  改进建议：[具体怎么做]

#### 🟢 做得好的地方
- [值得保留的设计]

### 优先改进计划
1. [最重要的改进，一句话]
2. [次重要的改进，一句话]
3. [...]
```

---

## 常见反模式速查

遇到以下关键词，直接联想对应因素：

| 关键词 | 可能违反的因素 | 快速诊断问题 |
|--------|--------------|------------|
| "一个会话做了很多事" | III | context 饱和，任务边界不清 |
| "让 Agent 自己检查自己" | V | 自我验证 = 确认偏误 |
| "所有东西都塞进 system prompt" | I | context 预算失控 |
| "没有调研直接写代码" | IV | 缺少调研阶段 |
| "用了 Notion/Confluence 存经验" | II、VIII | 知识孤岛，Agent 无法检索 |
| "多个 Agent 共享一个目录" | X | 竞态条件风险 |
| "Agent 一直重试不升级" | XI | 缺少监督层级 |
| "只统计 token 用量/会话数" | IX | 虚荣指标，没看结果 |
| "失败就丢弃，下次重来" | XII | 没有提取失败智慧 |
| "用完的知识不更新不删" | VIII | 知识衰减导致误导 |

---

## 参考文档

详细的因素说明存放在 `references/` 目录，按需加载：

- `references/factor-1-context.md` — 上下文管理详解
- `references/factor-2-git.md` — Git 追踪模式
- `references/factor-3-one-task.md` — 任务隔离与交接
- `references/factor-4-research.md` — 调研阶段设计
- `references/factor-5-validation.md` — 外部验证体系
- `references/factor-6-ratchet.md` — 棘轮进度锁定
- `references/factor-7-learnings.md` — 经验提取格式
- `references/factor-8-compound.md` — 知识复利飞轮
- `references/factor-9-metrics.md` — 适应性指标
- `references/factor-10-isolation.md` — 工作单元隔离
- `references/factor-11-supervision.md` — 层级化监督
- `references/factor-12-failures.md` — 失败智慧收获

遇到用户提到某具体因素相关的问题时，读对应的 reference 文件以获取详细内容。
