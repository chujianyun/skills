# Skills

这是悟鸣公开维护的一组 Agent Skills，偏实战、偏工作流，主要服务于 AI 工具使用、文档解读、项目配置、运维排障与技能分发。

和“技能清单”相比，这个仓库更适合被理解成一张**能力地图**：每个 skill 不只是一个说明文件，而是围绕某一类任务组织起来的可复用能力单元。

---

## Skill 地图

### 1. 文档 / 知识库类（Tool Wrapper）

这类 skill 的核心价值，是把某个产品、系统或知识域的资料包装成可按需触发的上下文。

| Skill | 模式 | 适用场景 |
|---|---|---|
| [qoder-wiki](skills/qoder-wiki/SKILL.md) | Tool Wrapper | 用户询问 Qoder 的安装、使用、功能、定价、MCP、快捷键、Quest Mode、Repo Wiki 等 |
| [openclaw-wiki](skills/openclaw-wiki/SKILL.md) | Tool Wrapper | 用户询问 OpenClaw 的安装、Gateway、渠道连接、Sessions、Tools、Skills、故障排查等 |

---

### 2. 配置审查 / 结构优化类（Reviewer / Inversion）

这类 skill 的重点不是“直接干活”，而是**先判断、先诊断、再给方案**。

| Skill | 模式 | 适用场景 |
|---|---|---|
| [prompt-optimizer](skills/prompt-optimizer/SKILL.md) | Reviewer / Generator | 优化 Prompt、改进 AI 指令、为特定任务挑选提示词框架 |
| [claude-config-advisor](skills/claude-config-advisor/SKILL.md) | Reviewer / Inversion | 审查或设计 `.claude`、`CLAUDE.md`、Claude Code 项目配置 |
| [skill-optimizer](skills/skill-optimizer/SKILL.md) | Reviewer | 审查并优化已有 skill 的 description、工作流、确认门槛、目录结构 |

---

### 3. 解读 / 报告生成类（Pipeline / Generator）

这类 skill 的核心是：**把原始资料落到本地，再生成结构化文档交付**。

| Skill | 模式 | 适用场景 |
|---|---|---|
| [github-code-interpreter](skills/github-code-interpreter/SKILL.md) | Pipeline / Generator | 用户提供 GitHub 仓库链接，希望解读源码、分析架构、生成学习报告或快速上手文档 |
| [paper-interpreter](skills/paper-interpreter/SKILL.md) | Pipeline / Generator | 用户提供 arXiv 链接，希望下载论文、解读论文、生成读书笔记或详细报告 |
| [opendataloader-pdf](skills/opendataloader-pdf/SKILL.md) | Tool Wrapper / Pipeline | PDF 提取、PDF 转 Markdown/JSON/HTML、RAG 数据准备、批量 PDF 处理 |

**这类 skill 的共同特点：**
- 默认以本地文件为主交付
- 默认先交付初稿
- **不自动复查，是否复查需要用户明确同意**

---

### 4. 运维 / 排障类（Runbook / Tool Wrapper）

这类 skill 适合处理“系统坏了、服务挂了、渠道断了、命令不会用”的场景。

| Skill | 模式 | 适用场景 |
|---|---|---|
| [openclaw-ops](skills/openclaw-ops/SKILL.md) | Tool Wrapper / Runbook | OpenClaw 状态检查、日志排查、Gateway/渠道/Agent 故障处理 |
| [copaw-ops](skills/copaw-ops/SKILL.md) | Tool Wrapper / Runbook | CoPaw 服务状态检查、配置排障、模型问题、cron 异常、渠道故障 |

**这类 skill 的共同原则：**
- 先做状态检查，再决定是否修复
- 高影响动作（重启、repair、更新、配置修改）应先说明再执行

---

### 5. 安装 / 同步 / 分发类（Pipeline）

这类 skill 偏工具链管理，负责把能力装上去、同步出去。

| Skill | 模式 | 适用场景 |
|---|---|---|
| [sync-skills](skills/sync-skills/SKILL.md) | Pipeline | 将 skills 从本地、GitHub 或 skillsmp.com 同步到多个 AI 工具目录 |
| [claudian-installer](skills/claudian-installer/SKILL.md) | Pipeline | 安装 Claudian Obsidian 插件，把 Claude Code 接进 Obsidian |

---

## 使用建议

### 什么时候优先选哪类 skill？

- **问产品文档 / 官方资料** → 先看 wiki 类 skill
- **想优化 Prompt / 配置 / skill 本身** → 先看审查优化类 skill
- **想把论文 / 仓库整理成报告** → 用解读生成类 skill
- **服务出问题、命令不会用、要排障** → 用运维类 skill
- **要把能力装到工具里、同步到多个目录** → 用安装同步类 skill

---

## 仓库设计原则

这批公有 skill 默认遵循这些原则：

1. **description 是给模型看的触发规则，不只是简介**
2. **SKILL.md 负责调度，细节尽量拆到 references / scripts / assets**
3. **默认先交付初稿，不自动做超出用户预期的后续动作**
4. **需要高影响操作时，先说明再执行**
5. **能脚本化的重复动作，尽量不要只写成文字说明**
6. **持续沉淀 Gotchas，降低误触发和翻车概率**

### 新增 skill 时建议遵循的规范

如果后面继续往这个仓库加新 skill，建议统一按这套来：

- **frontmatter 只保留 `name` 和 `description`**
- `description` 要同时写清：
  - 做什么
  - 什么时候触发
  - 必要时写一句不适用场景
- `SKILL.md` 优先写：
  - 适用边界
  - 设计模式（如 Tool Wrapper / Generator / Reviewer / Inversion / Pipeline）
  - Gotchas
  - 工作流
  - 输出要求
- 如果 skill 逻辑较长，优先拆到：
  - `references/`：规范、模板、清单、补充文档
  - `scripts/`：可执行脚本
  - `assets/`：固定模板、示例资源
- 如果 skill 涉及高影响动作、自动复查、定时任务、外部写操作，要明确写出**确认门槛**
- 如果 skill 只是审查或规划类，默认遵循：**先审查 / 诊断，再出计划，确认后再修改**

---

## 安装

### Method 1: Install directly in Claude Code

1. Add plugin marketplace
```bash
/plugin marketplace add chujianyun/skills
```

2. Install skills

Install `prompt-optimizer`
```bash
/plugin install prompt-engineering-skills@chujianyun/skills
```

Install `qoder-wiki`
```bash
/plugin install qoder-wiki@chujianyun/skills
```

Install `openclaw-wiki`
```bash
/plugin install openclaw-wiki@chujianyun/skills
```

Install `sync-skills`
```bash
/plugin install sync-skills@chujianyun/skills
```

Install `claudian-installer`
```bash
/plugin install claudian-installer@chujianyun/skills
```

Install `openclaw-ops`
```bash
/plugin install openclaw-ops@chujianyun/skills
```

Install `copaw-ops`
```bash
/plugin install copaw-ops@chujianyun/skills
```

Install `skill-optimizer`
```bash
/plugin install skill-optimizer@chujianyun/skills
```

Install `claude-config-advisor`
```bash
/plugin install claude-config-advisor@chujianyun/skills
```

Install `github-code-interpreter`
```bash
/plugin install github-code-interpreter@chujianyun/skills
```

Install `paper-interpreter`
```bash
/plugin install paper-interpreter@chujianyun/skills
```

Install `opendataloader-pdf`
```bash
/plugin install opendataloader-pdf@chujianyun/skills
```

### Method 2: Using [openskills](https://github.com/numman-ali/openskills)

```bash
openskills install chujianyun/skills --global
```

---

## Contact

![](https://mingmingruyue-hz.oss-cn-hangzhou.aliyuncs.com/2025/20260121123942301.png)

---

## License

All Skill files in this project are licensed under [CC BY-NC-SA 4.0](LICENSE-CC-BY-NC-SA) (Attribution-NonCommercial-ShareAlike).

For commercial use, please contact the author for authorization.
