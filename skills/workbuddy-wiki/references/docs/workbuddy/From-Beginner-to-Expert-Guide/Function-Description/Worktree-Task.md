# Git 集成和并行开发

这是 WorkBuddy **开发者体验**能力的一部分。当工作空间内包含 Git 仓库时，原本需要切到终端或 IDE 才能完成的 Git 操作，现在可以直接在 WorkBuddy 内完成，连续作业不再被打断：

- **分支从隐式变显式** ：创建任务时即可查看当前检出的分支，并安全切换到目标分支，不必离开 WorkBuddy。
- **多任务并行且互不干扰** ：让多个任务在相互隔离的工作目录中并行运行，文件系统层面完全隔离，避免多个 Agent 的改动互相污染。

两项能力都建立在 **Git 原生语义**之上——不引入额外概念，熟悉 Git 的你能够直接推断系统的真实行为。

![并行任务](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/worktree-1.CGByyFvu.png)

## 一、Git 分支显示与切换

### 创建任务时选择分支

当工作空间内包含 Git 仓库时，新建任务页面会显示当前分支，并支持直接切换：

- **显示当前分支** ：默认展示当前检出的本地分支名。
- **切换分支** ：点击分支选择器，可切换至其他本地分支或远程分支，支持搜索。
- **切换确认** ：切换分支后点击发送初始任务指令时，会弹出确认对话框；未切换分支则无需确认，直接开始任务。

#### 分支选择器的显示状态

| 工作空间类型 | 分支选择器状态 |
| --- | --- |
| 普通文件夹（非 Git 仓库） | 不可操作（置灰） |
| 正常 Git 仓库 | 可操作 |

![创建任务时选择分支](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/worktree-2.Cd-yjlrs.png)

### 切换分支时的变更处理

切换分支时，如果当前工作区存在未提交的改动，确认弹窗中会提供三种处理方式：

| 处理方式 | 说明 |
| --- | --- |
| **Commit 到当前分支**（默认） | 弹出轻量提交面板，勾选变更文件并填写提交信息，提交完成后再切换到目标分支 |
| **Stash 变更** | 自动将当前改动（含未跟踪文件）暂存起来，再切换到目标分支 |
| **丢弃变更** | 放弃所有未提交的改动后切换，需二次确认，请谨慎使用 |

> **Tip: 提示**
>
> - 默认选中 **Commit** （最安全的方式）。
> - 若切换失败，工作区会完整回滚到操作前的状态，不会残留中间态。
> - 选择远程分支时，系统会自动创建同名本地分支并跟踪该远程分支，再切换到该本地分支；若本地已存在同名分支，会提示你手动命名。

### 任务执行中的分支显示

在已有任务的对话界面中，工作区状态栏会实时显示当前检出的分支名，分支发生变化后自动刷新。

![任务执行中的分支显示](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/worktree-6.BlaZZH6c.png)

## 二、Worktree 并行任务

### 什么是 Worktree Task

**Worktree Task** 利用 Git worktree 的原生能力，为每个并行任务提供完全隔离的工作目录，同时与主仓库共享分支和 Git 对象。

当你需要同时推进多个独立任务（新特性开发、bug 修复、实验性方案等），又不希望它们与你当前的工作目录互相干扰时，可以为每个任务分别开启 Worktree。

### 创建 Worktree Task

1. 在新建任务页面输入任务指令（Prompt）；
2. 当工作空间包含 `.git` 目录时，输入框下方会展示 **Worktree** 开关（默认关闭）；
3. 开启后展开 **Base Branch（基础分支）** 选择器，默认选中本地主分支（如 main），可切换为其他本地或远程分支，支持搜索与 fetch 刷新；
4. 发送任务指令，系统开始创建 Worktree Task，界面会实时展示创建进度（大型项目可能需要数十秒到一分钟）；
5. 创建完成后，Agent 自动启动并执行任务指令。

![创建 Worktree Task](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/worktree-3.CtWRq8NY.png)

创建时系统会自动完成以下动作：

- 在 `~/WorkBuddy/Worktrees` 目录下创建独立的 worktree 工作目录；
- 基于所选 Base Branch 的 HEAD commit 自动新建任务分支，命名格式为 `workbuddy/{基础分支}-{8位随机哈希}` （如 `workbuddy/main-a3f8c2b1` ），前缀 `workbuddy/` 用于与你手动创建的分支区分；
- 创建失败时自动回滚已创建的 worktree 与分支，不遗留半成品资源。

> **Note: 说明**
>
> - 非 Git 项目（无 `.git` 目录）不展示 **Worktree** 开关，只能创建普通任务。
> - Base Branch 在任务创建后锁定，不可修改；任务分支在任务生命周期内也不提供切换入口。
> - 创建任务时源工作区存在未提交改动不影响创建，新任务基于所选 Base Branch 的 HEAD commit 开始，不包含未提交改动。

### 任务标识与分支展示

Worktree Task 在任务列表和详情页中有明确标识：

- **类型标识** ：任务列表标题前展示独特的 fork 类型图标，与普通任务明确区分；任务在列表中仍按原项目分组。

![类型标识 fork 图标](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/worktree-7.Bv3Sacix.png)

- **分支标识** ：任务卡片与任务标题旁展示当前分支 Badge（如 `workbuddy/main-a3f8c2b1` ），为只读展示，hover 可查看详情，点击可复制分支名。

![Worktree 任务标识](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/worktree-4.D8OLge1o.png)

### 自动清理机制

为避免 Worktree Task 持续累积占用磁盘空间，系统提供自动清理策略（仅针对 Worktree Task，创建普通任务不受任何限制）：

- **达到 25 个** ：在首页创建新 Worktree Task 时展示数量较多的提示，建议清理；
- **达到 50 个** ：勾选 Worktree 后弹出「任务工作区已达上限」清理确认弹窗，需选择清理范围（清理超过 7 / 15 / 30 天前的任务工作区分支和文件），确认清理后才能继续创建；取消则阻塞创建。

![自动清理](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/worktree-5.UusY3L3Z.png)

## 三、使用建议与注意事项

> **Tip: 使用建议**
>
> - 轻量改动、单点查询使用 **普通任务** 即可；需要并行推进多个任务或隔离试验性方案时，再开启 **Worktree** 。

当前版本（V1）暂不支持以下能力：

- 在云端 WorkBuddy 与 CodeBuddy 中使用 Worktree Task；
- 非 Git 项目、跨多个仓库的 Worktree Task；
- 从已有 Worktree Task fork 新任务，以及在任务内切换分支。
