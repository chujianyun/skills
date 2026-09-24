# DeepSeek Harness 文档索引

本文件由 `scripts/sync_wiki_docs.py` 生成。日常问答优先运行 `scripts/search_docs.py`，需要浏览主题结构时再读取本索引。

- 来源：<https://deepseek-harness.github.io/deepseek-harness/develop/basic>
- 文档数：18

## 顶层目录

- `Cordis教程`：8 篇
- `基础`：4 篇
- `实战`：3 篇
- `框架能力`：3 篇

## 目录树

```text
docs/
├── Cordis教程
│   ├── 01-第一个插件.md
│   ├── 02-生命周期与副作用.md
│   ├── 03-服务.md
│   ├── 04-事件.md
│   ├── 05-配置.md
│   ├── 06-组合与热重载.md
│   ├── 07-进入Harness.md
│   └── index.md
├── 基础
│   ├── index.md
│   ├── 开发一个工具.md
│   ├── 打包与安装插件.md
│   └── 插件配置.md
├── 实战
│   ├── index.md
│   ├── LLM适配器.md
│   └── 运行时Cordis工具.md
└── 框架能力
    ├── index.md
    ├── 事件系统.md
    └── 服务与依赖.md
```

## 全部文档

| 路径 | 标题 | 摘要 / 关键词 | 来源 |
|---|---|---|---|
| `Cordis教程/01-第一个插件.md` | 1. 编写第一个插件 | 在本教程使用的 loader 配置中，Cordis 插件模块通过命名导出提供 apply 函数。Cordis 加载模块时，会用一个 上下文 调用 apply；该上下文就是 ctx 对象，插件通过它注册自己贡献的所有内容。；编写第一个插件 | [原文](<https://deepseek-harness.github.io/deepseek-harness/develop/cordis-tutorial/01-first-plugin>) |
| `Cordis教程/02-生命周期与副作用.md` | 2. 生命周期与 effect | Cordis 插件可能因修改配置、热重载、显式资源释放或所需服务消失而卸载。通过 Cordis API 建立的注册属于 effect，会在所属插件卸载时撤销；在这些 API 之外管理的资源必须包装在 ctx.effect() 中。；effect, 生命周期与 | [原文](<https://deepseek-harness.github.io/deepseek-harness/develop/cordis-tutorial/02-lifecycle-and-effects>) |
| `Cordis教程/03-服务.md` | 3. 服务 | 服务是一个插件提供、其他插件通过 ctx 消费的具名能力。在 harness 中，ctx.tools、ctx.llm 和 ctx.agents 都是服务。消费方只指定 'tools' 之类的能力，而不导入其提供方，因此配置可以选择提供方，无需修改消费方。；服务 | [原文](<https://deepseek-harness.github.io/deepseek-harness/develop/cordis-tutorial/03-services>) |
| `Cordis教程/04-事件.md` | 4. 事件 | 服务支持直接调用；事件让插件无需知道有哪些插件正在监听，就能发出通知。harness 使用事件处理工具结果、模型请求和审批决定等交互。；事件 | [原文](<https://deepseek-harness.github.io/deepseek-harness/develop/cordis-tutorial/04-events>) |
| `Cordis教程/05-配置.md` | 5. 配置 | cordis.yml 中的每个 Cordis 配置项都可以携带 config 块，插件则声明一个 schema，在运行 apply 前验证该块。错误配置会导致加载失败，并给出准确的错误：插件绝不会在配置不完整时启动。；配置 | [原文](<https://deepseek-harness.github.io/deepseek-harness/develop/cordis-tutorial/05-config>) |
| `Cordis教程/06-组合与热重载.md` | 6. 组合与 HMR（热模块替换） | 到目前为止构建的每项能力都是插件，cordis.yml 则选择应用的插件树。本章会改变这种组合、热重载一个插件，并诊断始终无法加载的插件。；HMR, 热模块替换, 组合与 | [原文](<https://deepseek-harness.github.io/deepseek-harness/develop/cordis-tutorial/06-composition-and-hmr>) |
| `Cordis教程/07-进入Harness.md` | 7. 进入 harness | 本章会向 harness 的 tools 服务注册一个可由模型调用的工具，通过 harness 工具流水线执行它，并观察结果事件。整个示例无需密钥，也不会调用模型。；harness, 进入 | [原文](<https://deepseek-harness.github.io/deepseek-harness/develop/cordis-tutorial/07-into-the-harness>) |
| `Cordis教程/index.md` | Cordis 教程 | Cordis 是 DeepSeek Harness 底层的插件框架：它是一个小型运行时，其中的每项能力，包括工具、LLM（大语言模型）适配器、文件访问乃至 agent loop（智能体循环）本身，都是挂载到共享上下文中的插件。本教程通过动手实践讲解 Cordis：每一章都是一个可以运行的示例，你将在本仓库内的临时目录中逐步构建它，最后把一个插件接入真实的 h；Cordis, 教程 | [原文](<https://deepseek-harness.github.io/deepseek-harness/develop/cordis-tutorial/>) |
| `基础/index.md` | 第一个插件 | 本教程会创建一个最小的 Harness 插件，并将其加载到 Web UI 中。请从已完成[从源码运行路径](https://github.com/deepseek-ai/deepseek-harness/blob/master/README.zh.md#run-from-source)的仓库检出开始。；第一个插件 | [原文](<https://deepseek-harness.github.io/deepseek-harness/develop/basic/>) |
| `基础/开发一个工具.md` | 开发一个工具 | 本教程会在 Web UI 中添加一个 greet 工具。请先完成[第一个插件](index.md)，并保留其中的 scratch-plugin 目录。；开发一个工具 | [原文](<https://deepseek-harness.github.io/deepseek-harness/develop/basic/tool>) |
| `基础/打包与安装插件.md` | 打包与安装插件 | 前几篇教程通过 --patch overlay 加载本地插件。本教程把它打包成可安装的组合包（bundle），用 dsh plugin add 安装进一个 profile，并解释决定组合后配置的层顺序。本文假设 dsh CLI 已安装。请先完成[插件配置](插件配置.md)。；打包与安装插件 | [原文](<https://deepseek-harness.github.io/deepseek-harness/develop/basic/publish>) |
| `基础/插件配置.md` | 插件配置 | 让你的插件接受用户在 cordis.yml 中传入的配置。；插件配置 | [原文](<https://deepseek-harness.github.io/deepseek-harness/develop/basic/config>) |
| `实战/LLM适配器.md` | LLM 适配器 | LLM 适配器是一个继承 LlmAdapter 并实现 stream() 方法的类，它会将 Harness 的提供方无关请求转换为具体提供方的 API 调用，并将响应转换回 Harness 分片。；LLM, 适配器 | [原文](<https://deepseek-harness.github.io/deepseek-harness/develop/practice/llm-adapter>) |
| `实战/index.md` | 能力的三种角色设计 | 本文分为两部分：先参考三种角色能力模式的概念，再通过高级教程构建一项能力。请先完成[基础插件路径](../基础/index.md)和[服务教程](../框架能力/服务与依赖.md)。；能力的三种角色设计 | [原文](<https://deepseek-harness.github.io/deepseek-harness/develop/practice/>) |
| `实战/运行时Cordis工具.md` | 用 Cordis 工具扩展运行中的智能体 | 本实战指南启用 [@deepseek-ai/dsh-tool-cordis](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/extensions/tool-cordis/README.zh.md)。智能体可以检查当前 Cordis 进程，并在内存中挂载或卸载模型编写的；Cordis, 工具扩展运行中的智能体 | [原文](<https://deepseek-harness.github.io/deepseek-harness/develop/practice/dynamic-cordis>) |
| `框架能力/index.md` | 插件与生命周期 | 每个被加载的插件都拥有一个 Fiber 作用域，其状态如下：；插件与生命周期 | [原文](<https://deepseek-harness.github.io/deepseek-harness/develop/framework/>) |
| `框架能力/事件系统.md` | 事件系统 | 事件是 Cordis 插件间通信的核心机制。Harness 大量使用事件来实现松耦合的扩展点。；事件系统 | [原文](<https://deepseek-harness.github.io/deepseek-harness/develop/framework/events>) |
| `框架能力/服务与依赖.md` | 服务与依赖 | 服务是一个插件向其他插件公开的能力。inject 声明插件需要哪些服务。；服务与依赖 | [原文](<https://deepseek-harness.github.io/deepseek-harness/develop/framework/service>) |
