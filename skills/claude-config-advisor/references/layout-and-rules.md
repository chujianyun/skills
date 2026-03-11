# `.claude` 目录职责与创建规范

## 目录一览

`.claude` 用来存放项目级别的 Claude Code 自定义配置，适合与团队共享。

常见结构：

```text
.claude/
  skills/
  agents/
  commands/
  hooks/
  output-styles/
  settings.json
  settings.local.json
```

不是每个项目都需要把这些目录配齐。合理的目标是“刚好够用”，而不是“看起来完整”。

## `.claude/skills/`

### 作用

封装专项知识、固定工作流或领域能力，让 Claude 在遇到相关任务时更稳定地调用。

### 创建规范

- 每个技能都必须有一个 `SKILL.md`
- `SKILL.md` 顶部使用 YAML frontmatter
- 至少包含：
  - `name`
  - `description`
- `name` 最好使用小写字母、数字和连字符
- `description` 要同时说明“做什么”和“何时触发”
- YAML 之后是 Markdown 正文

### 最佳实践

- `SKILL.md` 保持简短，优先写工作流和入口规则
- 细节参考资料拆到同目录的 `references/`、`assets/`、`scripts/`
- 如果技能内容太长，采用渐进式披露，只在需要时再读取子文件

## `.claude/agents/`

### 作用

定义项目级子智能体，用于处理明确分工的任务，比如代码审查、调试、架构评审。

### 创建规范

- 每个子智能体是一个 Markdown 文件
- 顶部使用 YAML frontmatter
- 常见字段：
  - `name`
  - `description`
  - `tools`
  - `model`
  - `permissionMode`
  - `skills`
- YAML 之后写该 agent 的系统提示词

### 适用信号

- 某一类任务反复出现，且需要独立角色边界
- 需要和主对话分开上下文
- 对工具权限或模型选择有不同要求

## `.claude/commands/`

### 作用

存放团队可复用的斜杠命令模板，加速固定工作流。

### 创建规范

- 每个命令是一个 Markdown 文件
- 文件名自动成为命令名
- 文件内容就是发给 Claude 的提示词模板
- 支持 `$ARGUMENTS`、`$1`、`$2` 等占位符

### 适用信号

- 同类提示词经常重复输入
- 团队希望把常用操作标准化
- 需要把复杂提示收敛成短命令

## `.claude/hooks/`

### 作用

在 Claude Code 的特定生命周期事件中自动执行 shell 命令或脚本。

### 创建规范

- 通常通过 hooks 配置文件定义事件、匹配器和命令
- 实际脚本可以放在 `.claude/hooks/` 下
- 常见脚本类型：`.sh`、`.py`

### 适用信号

- 某些动作必须稳定自动执行，比如格式化、校验、日志记录
- 执行动作是确定性的，不依赖模糊判断

## `.claude/output-styles/`

### 作用

定义自定义输出风格，用来补充或调整 Claude Code 的默认输出方式。

### 创建规范

- 每个样式是一个带 YAML frontmatter 的 Markdown 文件
- 常见字段：
  - `name`
  - `description`
  - `keep-coding-instructions`
- 后面追加该风格的指令正文

### 适用信号

- 项目确实需要稳定的特定表达风格
- 默认风格无法满足非软件工程场景

## 根目录常见配置文件

### `settings.json`

- 适合存放项目共享的 Claude 设置
- 通常会提交到 Git

### `settings.local.json`

- 适合个人本地偏好或机器相关配置
- 通常不提交到 Git

## 审查时的判断原则

- 缺少目录不是问题，前提是当前需求根本不需要它
- 目录很多也不代表成熟，可能只是过度设计
- 真正重要的是职责边界清楚、内容可维护、能服务实际工作流
