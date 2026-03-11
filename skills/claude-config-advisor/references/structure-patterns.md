# 推荐结构模式

当用户还没有 Claude 配置，或想重构现有结构时，用这些模式做裁剪式推荐。

## 模式 1：极简个人项目

适用场景：

- 一个人维护
- 目标是让 Claude 快速理解项目
- 还没有明显的专项工作流

推荐结构：

```text
CLAUDE.md
.claude/
  commands/
```

建议内容：

- `CLAUDE.md` 写项目命令、目录入口、代码规范、测试方式
- `.claude/commands/` 只放最高频的 2 到 5 个命令模板

不建议一开始就加：

- agents
- hooks
- output-styles

## 模式 2：有稳定专项任务的项目

适用场景：

- 某些任务会重复出现
- 需要专项知识或固定工作流
- 希望 Claude 在特定场景下更稳定

推荐结构：

```text
CLAUDE.md
.claude/
  skills/
  commands/
```

建议内容：

- `CLAUDE.md` 管全局规则
- `skills/` 管专项知识和流程
- `commands/` 管频繁调用的快捷提示

典型例子：

- PR 审查规范
- 数据库 schema 查询方法
- 发布流程
- 文档生成流程

## 模式 3：团队协作型项目

适用场景：

- 多人协作
- 需要更稳定的角色分工和共享规范
- 项目内已经有多种重复工作流

推荐结构：

```text
CLAUDE.md
.claude/
  skills/
  agents/
  commands/
  settings.json
```

建议内容：

- `CLAUDE.md` 只写团队通用规则
- `skills/` 放知识和流程
- `agents/` 放明确角色，如 reviewer、debugger、architect
- `commands/` 放高频工作流入口
- `settings.json` 放共享设置

## 模式 4：自动化要求较高的项目

适用场景：

- 某些检查或格式化动作必须稳定发生
- 需要在工具调用前后执行脚本

推荐结构：

```text
CLAUDE.md
.claude/
  skills/
  commands/
  hooks/
```

建议内容：

- 只有确定性动作才放进 hooks
- 需要主观判断的流程仍然交给 skills 或 agents

## 设计建议

### 建议 1：从轻到重

优先顺序通常是：

1. `CLAUDE.md`
2. `commands/`
3. `skills/`
4. `agents/`
5. `hooks/`
6. `output-styles/`

### 建议 2：共享与本地分离

- 团队共享规则放到 Git 管理的文件
- 个人偏好放到 `CLAUDE.local.md` 或 `settings.local.json`

### 建议 3：一类问题交给一种机制

不要出现这种混乱情况：

- 同一套规范既写在 `CLAUDE.md`，又写进 command，还塞进 skill

更好的做法：

- `CLAUDE.md` 负责总规则和入口
- 具体长流程拆到对应机制

## 推荐输出格式

向用户给方案时，尽量同时提供：

- 推荐目录树
- 每个文件/目录的职责
- 为什么不建议额外增加某些目录

这样用户更容易判断是否接受这套设计。
