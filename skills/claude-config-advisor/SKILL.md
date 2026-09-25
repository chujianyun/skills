---
name: claude-config-advisor
description: 审查或设计 Claude Code 项目配置。用于用户提到 `.claude`、`CLAUDE.md`、Claude 配置文件、项目级 Claude 自定义配置、配置结构是否合理、该创建哪些配置文件，或希望从零规划 Claude 配置时使用。默认先审查或诊断，再给方案；只有用户明确要求时，才进一步输出推荐结构或样例文件。
---

# Claude Config Advisor

帮助用户评估现有 Claude Code 项目配置，或从零设计一套合适的 `.claude` 与 `CLAUDE.md` 结构。

## 设计模式

本 skill 主要采用：
- **Reviewer**：先判断现有配置是否合理，再给评价
- **Inversion**：信息不足时先追问最小必要问题，不一上来就堆完整方案
- **Generator（轻度）**：只有在用户明确需要落地建议时，才生成推荐目录树或样例

## Gotchas

- 不要一上来就默认用户需要全套 `.claude/agents + hooks + commands + skills`
- 不要把“审查现状”和“直接帮他重构一整套配置”混成一步
- 不要为了显得专业就过度设计；简单项目往往只需要 `CLAUDE.md`
- 不要在没读关键文件前就断言结构合理或不合理
- 如果信息不足，先问一个最短问题，不要一次扔很多开放问题

## 工作模式

先判断当前属于哪一类：

1. **审查模式**
   用户已经有 `.claude/`、`CLAUDE.md`、`CLAUDE.local.md` 或相关配置文件。
2. **设计模式**
   用户还没有配置，或明确表示想先规划再创建。

## 使用流程

复制此清单并跟踪进度：

```text
处理进度：
- [ ] 步骤 1：识别场景（审查 / 设计）
- [ ] 步骤 2：读取最小必要文件
- [ ] 步骤 3：判断结构合理性
- [ ] 步骤 4：给出评价与建议
- [ ] 步骤 5：如用户需要，再输出推荐结构或样例
```

### Step 1: 识别场景

优先看用户是否已经提到这些内容：

- 项目根目录下的 `CLAUDE.md` 或 `CLAUDE.local.md`
- `.claude/skills/`
- `.claude/agents/`
- `.claude/commands/`
- `.claude/hooks/`
- `.claude/output-styles/`
- `.claude/settings.json` 或 `.claude/settings.local.json`

判断规则：

- 如果这些文件或目录已存在，进入“审查模式”
- 如果不存在，或用户只是在规划，进入“设计模式”

### Step 2: 读取最小必要文件

#### 审查模式

只读取与判断有关的文件，不要整仓库乱扫。

优先读取：

1. `CLAUDE.md` / `CLAUDE.local.md`
2. `.claude/` 目录的一级结构
3. `.claude/skills/` 下被用户点名或最关键的 `SKILL.md`
4. `.claude/agents/` 下与当前诉求相关的 agent 定义
5. `.claude/commands/` 中具有代表性的命令模板
6. `.claude/hooks/` 的配置文件和关键脚本

需要判断目录职责或创建规范时，读取 [references/layout-and-rules.md](references/layout-and-rules.md)。

需要判断 `CLAUDE.md` 是否写得合理时，读取 [references/claude-md-guide.md](references/claude-md-guide.md)。

需要给出现状评分和优化优先级时，读取 [references/review-rubric.md](references/review-rubric.md)。

#### 设计模式

先了解用户想法，再给建议，不要上来就堆一整套复杂结构。

优先确认这些信息：

- 这是个人项目还是团队项目
- 想解决什么问题：规范协作、复用命令、封装技能、子智能体分工、自动执行 hooks
- 是否需要提交到 Git 与团队共享
- 是否更偏“极简”还是“体系化”

需要推荐合适的目录组合时，读取 [references/structure-patterns.md](references/structure-patterns.md)。

### Step 3: 判断结构合理性

#### 审查模式下的核心判断

从这几个角度判断“是否合理”：

1. **职责是否清晰**
   - `CLAUDE.md` 是否承担全局规范与上下文说明
   - `.claude/skills/` 是否承载可复用的专项能力
   - `.claude/agents/` 是否承载明确分工的子智能体
   - `.claude/commands/` 是否承载可重复执行的提示词模板
   - `.claude/hooks/` 是否承载确定性的自动脚本

2. **结构是否匹配需求**
   - 只是一个简单项目，却堆了大量 agents / hooks / output styles，通常是过度设计
   - 团队协作很复杂，却只有一个臃肿的 `CLAUDE.md`，通常是职责混杂

3. **内容是否易维护**
   - `CLAUDE.md` 是否简洁、可读、偏规则而不是长篇背景故事
   - skill 是否有 frontmatter，description 是否能准确触发
   - 是否把可共享配置与个人本地偏好混在一起

4. **是否有明显缺口**
   - 有团队规范但没有 `CLAUDE.md`
   - 有复杂重复工作流但没有 commands
   - 有高频且确定性的检查动作却没有 hooks
   - 有稳定的专项任务却没有 skills 或 agents

#### 设计模式下的核心判断

重点判断用户真正需要的是哪一层配置，而不是默认全加：

- 只需要项目约束：先上 `CLAUDE.md`
- 需要复用提示：加 `.claude/commands/`
- 需要封装专项知识：加 `.claude/skills/`
- 需要明确角色分工：加 `.claude/agents/`
- 需要自动执行脚本：加 `.claude/hooks/`

### Step 4: 输出方式

#### 审查模式输出模板

必须包含以下四部分：

```markdown
# 配置评价

结论：合理 / 基本合理但有改进空间 / 不太合理

## 做得好的地方
- ...

## 主要问题
- ...

## 优化建议
1. ...
2. ...
3. ...
```

补充规则：

- “是否合理”必须明确表态，不要只说“可以优化”
- 评价要结合用户当前规模和目标，避免脱离场景
- 建议按优先级排序，先讲结构性问题，再讲润色项
- 如果用户要求，可以继续给出推荐目录树和示例文件

#### 设计模式输出模板

必须包含以下三部分：

```markdown
# 推荐方案

## 我对需求的理解
- ...

## 建议创建的文件与目录
- ...

## 为什么这样设计
- ...
```

如果信息不足，先用最短问题让用户补充想法，例如：

- “你更想要极简方案，还是团队协作型方案？”
- “你目前最想让 Claude 帮你稳定执行的是规范、命令、还是专项技能？”

不要一次问很多开放问题。

### Step 5: 提供推荐结构或样例

当用户明确需要落地建议时，再给结构树、样例骨架或文件职责说明。

推荐优先使用 [references/structure-patterns.md](references/structure-patterns.md) 中的方案做裁剪，而不是每次从头发明结构。

## 审查原则

- 先判断是否过度设计，再判断是否缺少关键配置
- 先看职责分层，再看命名和写法细节
- 共享规范放到可提交文件；个人偏好放到本地文件
- `CLAUDE.md` 应尽量短，强调规则、命令入口和例外事项
- 只有当某类需求真实存在时，才建议引入对应目录

## 何时读取额外参考

- 需要解释各目录含义时：读 [references/layout-and-rules.md](references/layout-and-rules.md)
- 需要专门评估 `CLAUDE.md` 时：读 [references/claude-md-guide.md](references/claude-md-guide.md)
- 需要做结构化打分或分级建议时：读 [references/review-rubric.md](references/review-rubric.md)
- 需要给出从零搭建方案时：读 [references/structure-patterns.md](references/structure-patterns.md)
