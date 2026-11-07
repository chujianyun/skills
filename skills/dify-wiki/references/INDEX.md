# Dify 文档索引

本文件由 `scripts/sync_wiki_docs.py` 生成。日常问答优先运行 `scripts/search_docs.py`，需要浏览主题结构时再读取本索引。

- 来源：<https://docs.dify.ai/zh/cloud>
- 文档数：332

## 顶层目录

- `使用`：108 篇
- `学习`：17 篇
- `开发者资源`：207 篇

## 目录树

```text
docs/
├── 使用
│   ├── 发布
│   │   ├── Web App
│   │   │   ├── Web App 设置.md
│   │   │   ├── Workflow Web 应用.md
│   │   │   ├── 嵌入 Web 应用.md
│   │   │   └── 聊天 Web App.md
│   │   ├── IP 访问控制.md
│   │   ├── MCP 服务器.md
│   │   ├── 分享你的 AI 应用.md
│   │   └── 发布应用到 Marketplace.md
│   ├── 工作空间
│   │   ├── 个人设置.md
│   │   ├── 导出和导入应用.md
│   │   ├── 工作空间.md
│   │   ├── 管理成员.md
│   │   └── 计费.md
│   ├── 监控
│   │   ├── 集成
│   │   │   ├── 集成 Arize.md
│   │   │   ├── 集成 Langfuse.md
│   │   │   ├── 集成 LangSmith.md
│   │   │   ├── 集成 Opik.md
│   │   │   ├── 集成 Phoenix.md
│   │   │   ├── 集成 W&B Weave.md
│   │   │   └── 集成阿里云云监控.md
│   │   ├── 仪表盘.md
│   │   ├── 日志.md
│   │   └── 标注系统.md
│   ├── 知识库
│   │   ├── Agent 知识库
│   │   │   ├── Agent 知识库.md
│   │   │   ├── 从经典知识库升级到 Agent 知识库.md
│   │   │   ├── 创建 Agent 知识库.md
│   │   │   ├── 多模态检索.md
│   │   │   ├── 接入应用、Agent 和代码.md
│   │   │   ├── 检查已索引的文档.md
│   │   │   ├── 检索设置.md
│   │   │   ├── 测试并调优检索.md
│   │   │   └── 维护 Agent 知识库.md
│   │   ├── 经典知识库
│   │   │   ├── 创建即用型知识库
│   │   │   │   ├── 创建即用型知识库.md
│   │   │   │   ├── 指定分段设置.md
│   │   │   │   └── 指定索引方式与检索设置.md
│   │   │   ├── 导入数据
│   │   │   │   ├── 上传本地文件.md
│   │   │   │   ├── 从 Notion 导入数据.md
│   │   │   │   └── 从网页导入数据.md
│   │   │   ├── 构建自定义知识库
│   │   │   │   ├── 数据源授权.md
│   │   │   │   ├── 构建自定义知识库.md
│   │   │   │   ├── 步骤一：创建知识流水线.md
│   │   │   │   ├── 步骤三：发布知识流水线.md
│   │   │   │   ├── 步骤二：编排知识流水线.md
│   │   │   │   ├── 步骤五：管理和使用知识库.md
│   │   │   │   └── 步骤四：上传文件.md
│   │   │   ├── 管理
│   │   │   │   ├── 管理文档元数据.md
│   │   │   │   ├── 维护知识库内容.md
│   │   │   │   └── 调整知识库设置.md
│   │   │   ├── 连接外部知识库
│   │   │   │   ├── 外部知识库 API.md
│   │   │   │   └── 连接外部知识库.md
│   │   │   ├── 在应用内集成知识库.md
│   │   │   ├── 测试检索.md
│   │   │   └── 经典知识库.md
│   │   ├── 知识库.md
│   │   ├── 知识库存储与文档配额.md
│   │   └── 知识库请求频率限制.md
│   ├── 编排
│   │   ├── Agent
│   │   │   ├── Agent.md
│   │   │   └── 构建 Agent.md
│   │   ├── Workflow 与 Chatflow
│   │   │   ├── 人工介入
│   │   │   │   └── 人工介入.md
│   │   │   ├── 开始
│   │   │   │   ├── 开始节点.md
│   │   │   │   └── 用户输入.md
│   │   │   ├── 节点
│   │   │   │   ├── Agent 知识检索.md
│   │   │   │   ├── Agent.md
│   │   │   │   ├── HTTP 请求.md
│   │   │   │   ├── If-Else.md
│   │   │   │   ├── 代码.md
│   │   │   │   ├── 列表操作符.md
│   │   │   │   ├── 参数提取器.md
│   │   │   │   ├── 变量聚合器.md
│   │   │   │   ├── 变量赋值器.md
│   │   │   │   ├── 大语言模型.md
│   │   │   │   ├── 工具节点.md
│   │   │   │   ├── 循环.md
│   │   │   │   ├── 文档提取器.md
│   │   │   │   ├── 模板转换.md
│   │   │   │   ├── 直接回复.md
│   │   │   │   ├── 经典知识检索.md
│   │   │   │   ├── 输出.md
│   │   │   │   ├── 迭代.md
│   │   │   │   └── 问题分类器.md
│   │   │   ├── 触发器
│   │   │   │   ├── Webhook 触发器.md
│   │   │   │   ├── 定时触发器.md
│   │   │   │   ├── 触发器.md
│   │   │   │   └── 集成触发器.md
│   │   │   ├── 调试
│   │   │   │   ├── 单节点.md
│   │   │   │   ├── 变量检查器.md
│   │   │   │   ├── 处理错误.md
│   │   │   │   ├── 运行历史.md
│   │   │   │   └── 错误类型.md
│   │   │   ├── Snippets.md
│   │   │   ├── Workflow 与 Chatflow.md
│   │   │   ├── 快捷键.md
│   │   │   ├── 版本控制.md
│   │   │   └── 编排逻辑.md
│   │   ├── 基础应用
│   │   │   ├── Agent.md
│   │   │   ├── 文本生成应用.md
│   │   │   └── 聊天助手.md
│   │   ├── 全局搜索.md
│   │   └── 应用工具箱.md
│   ├── 集成
│   │   ├── 自定义端点
│   │   │   ├── 使用 Cloudflare Workers 部署自定义端点.md
│   │   │   ├── 外部数据工具.md
│   │   │   ├── 敏感内容审查.md
│   │   │   └── 自定义端点.md
│   │   ├── Dify 工具.md
│   │   ├── 模型供应商.md
│   │   └── 集成.md
│   ├── Dify 文档.md
│   └── 使用 Dify.md
├── 学习
│   ├── 教程
│   │   ├── 工作流 101
│   │   │   ├── 第 1 课：什么是工作流.md
│   │   │   ├── 第 10 课：发布和监控你的 AI 应用.md
│   │   │   ├── 第 2 课：流程的头和尾（开始与输出节点）.md
│   │   │   ├── 第 3 课：工作流的大脑（LLM 节点）.md
│   │   │   ├── 第 4 课：小抄（知识检索）.md
│   │   │   ├── 第 5 课：工作流的岔路口（分类与执行）.md
│   │   │   ├── 第 6 课：处理多个任务（参数提取 & 迭代）.md
│   │   │   ├── 第 7 课：增强工作流（工具）.md
│   │   │   ├── 第 8 课：Agent 节点.md
│   │   │   └── 第 9 课：排版设计师（模板）.md
│   │   ├── 30 分钟快速入门.md
│   │   ├── ChatFlow 实战：搭建 Twitter 账号分析助手.md
│   │   ├── 使用文件上传搭建文章理解助手.md
│   │   ├── 使用知识库搭建智能客服机器人.md
│   │   ├── 如何搭建 AI 图片生成应用.md
│   │   └── 简单聊天机器人.md
│   └── 核心概念.md
└── 开发者资源
    ├── API
    │   ├── 应用 API
    │   │   ├── 人工介入
    │   │   │   ├── 提交人工介入表单.md
    │   │   │   └── 获取人工介入表单.md
    │   │   ├── 会话管理
    │   │   │   ├── 删除会话.md
    │   │   │   ├── 更新会话变量.md
    │   │   │   ├── 获取会话列表.md
    │   │   │   ├── 获取会话历史消息.md
    │   │   │   ├── 获取会话变量.md
    │   │   │   └── 重命名会话.md
    │   │   ├── 对话消息
    │   │   │   ├── 停止响应.md
    │   │   │   ├── 发送对话消息.md
    │   │   │   └── 获取下一轮建议问题列表.md
    │   │   ├── 工作流运行
    │   │   │   ├── 停止工作流任务.md
    │   │   │   ├── 执行工作流.md
    │   │   │   ├── 按 ID 执行工作流.md
    │   │   │   ├── 流式获取工作流事件.md
    │   │   │   ├── 获取工作流执行情况.md
    │   │   │   └── 获取工作流日志.md
    │   │   ├── 应用配置
    │   │   │   ├── 获取应用 WebApp 设置.md
    │   │   │   ├── 获取应用元数据.md
    │   │   │   ├── 获取应用参数.md
    │   │   │   └── 获取应用基本信息.md
    │   │   ├── 文件操作
    │   │   │   ├── 上传文件.md
    │   │   │   └── 下载文件.md
    │   │   ├── 文本生成消息
    │   │   │   ├── 停止响应.md
    │   │   │   └── 发送消息.md
    │   │   ├── 标注管理
    │   │   │   ├── 创建标注.md
    │   │   │   ├── 删除标注.md
    │   │   │   ├── 更新标注.md
    │   │   │   ├── 查询标注回复配置任务状态.md
    │   │   │   ├── 获取标注列表.md
    │   │   │   └── 配置标注回复.md
    │   │   ├── 消息反馈
    │   │   │   ├── 提交消息反馈.md
    │   │   │   └── 获取应用的消息反馈.md
    │   │   ├── 终端用户
    │   │   │   └── 获取终端用户信息.md
    │   │   └── 语音与文字转换
    │   │       ├── 文字转语音.md
    │   │       └── 语音转文字.md
    │   ├── 指南
    │   │   ├── API 概览
    │   │   │   ├── 知识库
    │   │   │   │   ├── Agent 知识库 API.md
    │   │   │   │   ├── 知识库 API.md
    │   │   │   │   └── 经典知识库 API.md
    │   │   │   ├── Agent API.md
    │   │   │   ├── Chatflow 应用 API.md
    │   │   │   ├── Workflow 应用 API.md
    │   │   │   ├── 对话型应用 API.md
    │   │   │   └── 文本生成应用 API.md
    │   │   ├── Dify API 快速开始.md
    │   │   ├── 人工介入 API 集成流程.md
    │   │   ├── 处理流式响应.md
    │   │   ├── 处理错误与速率限制.md
    │   │   └── 终端用户身份.md
    │   └── 知识库 API
    │       ├── Agent 知识库
    │       │   ├── 删除作业
    │       │   │   ├── 获取删除作业.md
    │       │   │   └── 获取删除批次.md
    │       │   ├── 数据源
    │       │   │   ├── 创建数据源.md
    │       │   │   ├── 删除数据源.md
    │       │   │   ├── 更新同步策略.md
    │       │   │   ├── 更新数据源.md
    │       │   │   ├── 测试数据源凭据.md
    │       │   │   ├── 获取同步策略.md
    │       │   │   ├── 获取数据源.md
    │       │   │   ├── 获取数据源列表.md
    │       │   │   ├── 获取数据源文件列表.md
    │       │   │   ├── 获取数据源连接列表.md
    │       │   │   └── 获取数据源页面列表.md
    │       │   ├── 数据源同步与导入
    │       │   │   ├── 取消数据源运行.md
    │       │   │   ├── 同步数据源.md
    │       │   │   ├── 导入所选页面.md
    │       │   │   ├── 导入数据源条目.md
    │       │   │   ├── 导入网站页面.md
    │       │   │   ├── 获取抓取预览页面列表.md
    │       │   │   ├── 获取数据源运行.md
    │       │   │   ├── 获取数据源运行列表.md
    │       │   │   ├── 重试数据源运行.md
    │       │   │   └── 预览网站抓取.md
    │       │   ├── 文档与分段
    │       │   │   ├── 删除文档.md
    │       │   │   ├── 删除文档文件.md
    │       │   │   ├── 批量删除文档文件.md
    │       │   │   ├── 按文件获取文档.md
    │       │   │   ├── 更新文档元数据.md
    │       │   │   ├── 获取分段.md
    │       │   │   ├── 获取分段列表.md
    │       │   │   ├── 获取文档.md
    │       │   │   ├── 获取文档修订版本列表.md
    │       │   │   ├── 获取文档列表.md
    │       │   │   ├── 获取文档大纲.md
    │       │   │   ├── 获取文档文件.md
    │       │   │   ├── 获取文档文件列表.md
    │       │   │   └── 重新索引文档.md
    │       │   ├── 查询
    │       │   │   ├── 创建查询令牌.md
    │       │   │   └── 运行查询.md
    │       │   ├── 查询记录
    │       │   │   ├── 获取查询冲突列表.md
    │       │   │   ├── 获取查询分段列表.md
    │       │   │   ├── 获取查询记录.md
    │       │   │   ├── 获取查询记录列表.md
    │       │   │   └── 获取缺失分段列表.md
    │       │   ├── 研究任务
    │       │   │   ├── 创建研究任务.md
    │       │   │   ├── 取消研究任务.md
    │       │   │   ├── 获取研究任务.md
    │       │   │   ├── 获取研究任务列表.md
    │       │   │   ├── 获取研究任务结果列表.md
    │       │   │   └── 规划研究任务.md
    │       │   ├── 索引任务
    │       │   │   ├── 取消索引任务.md
    │       │   │   ├── 获取后台任务列表.md
    │       │   │   ├── 获取批量任务.md
    │       │   │   ├── 获取文档的索引任务.md
    │       │   │   ├── 获取文档的索引任务列表.md
    │       │   │   ├── 获取索引任务.md
    │       │   │   └── 重试索引任务.md
    │       │   └── 设置
    │       │       ├── 更新知识库设置.md
    │       │       ├── 获取知识库设置.md
    │       │       └── 获取设置迁移.md
    │       └── 经典知识库
    │           ├── 元数据
    │           │   ├── 创建元数据字段.md
    │           │   ├── 删除元数据字段.md
    │           │   ├── 批量更新文档元数据.md
    │           │   ├── 更新元数据字段.md
    │           │   ├── 更新内置元数据字段.md
    │           │   ├── 获取元数据字段列表.md
    │           │   └── 获取内置元数据字段.md
    │           ├── 分段
    │           │   ├── 从文档获取分段.md
    │           │   ├── 创建子分段.md
    │           │   ├── 删除子分段.md
    │           │   ├── 删除文档中的分段.md
    │           │   ├── 向文档添加分段.md
    │           │   ├── 更新子分段.md
    │           │   ├── 更新文档中的分段.md
    │           │   ├── 获取子分段.md
    │           │   └── 获取文档中的分段详情.md
    │           ├── 文档
    │           │   ├── 下载文档.md
    │           │   ├── 从文件创建文档.md
    │           │   ├── 从文本创建文档.md
    │           │   ├── 删除文档.md
    │           │   ├── 批量下载文档（ZIP）.md
    │           │   ├── 批量更新文档状态.md
    │           │   ├── 更新文档.md
    │           │   ├── 用文件更新文档.md
    │           │   ├── 用文本更新文档.md
    │           │   ├── 获取文档嵌入状态（进度）.md
    │           │   ├── 获取文档详情.md
    │           │   └── 获取知识库的文档列表.md
    │           ├── 标签
    │           │   ├── 修改知识库标签.md
    │           │   ├── 创建知识库标签.md
    │           │   ├── 删除知识库标签.md
    │           │   ├── 绑定标签到知识库.md
    │           │   ├── 获取知识库标签列表.md
    │           │   ├── 获取知识库绑定的标签.md
    │           │   └── 解除标签与知识库的绑定.md
    │           ├── 模型
    │           │   └── 获取可用模型.md
    │           ├── 知识库
    │           │   ├── 从知识库检索分段 测试检索.md
    │           │   ├── 创建空知识库.md
    │           │   ├── 删除知识库.md
    │           │   ├── 更新知识库.md
    │           │   ├── 获取知识库列表.md
    │           │   └── 获取知识库详情.md
    │           └── 知识流水线
    │               ├── 上传流水线文件.md
    │               ├── 执行数据源节点.md
    │               ├── 获取数据源插件列表.md
    │               └── 运行流水线.md
    ├── CLI
    │   ├── 参考
    │   │   ├── 命令索引.md
    │   │   ├── 结果、错误与退出码.md
    │   │   └── 配置.md
    │   ├── 应用操作
    │   │   ├── 在 CI 和自动化中使用 `difyctl`.md
    │   │   ├── 构建应用.md
    │   │   ├── 运行应用.md
    │   │   └── 通过 DSL 文件创建和更新应用.md
    │   ├── 管理 difyctl
    │   │   ├── Dify 1.18.0 升级指南.md
    │   │   ├── 更新或卸载 difyctl.md
    │   │   └── 管理登录.md
    │   ├── 快速开始.md
    │   ├── 查找并运行命令.md
    │   └── 概述.md
    └── 插件开发
        ├── 发布
        │   ├── GitHub 仓库
        │   │   └── 发布到个人 GitHub 仓库.md
        │   ├── 本地文件
        │   │   ├── 为第三方签名验证签署插件.md
        │   │   └── 打包为本地文件并分享.md
        │   ├── 标准
        │   │   ├── 插件开发指南.md
        │   │   └── 隐私政策指南.md
        │   ├── 发布插件.md
        │   ├── 发布插件到 Marketplace.md
        │   └── 常见问题.md
        ├── 开发指南与示例
        │   ├── 完整示例
        │   │   ├── Flomo 工具（10分钟）.md
        │   │   ├── Markdown 导出器.md
        │   │   ├── Slack Bot.md
        │   │   └── 多模态工具.md
        │   ├── 按插件类型
        │   │   ├── Agent 策略插件.md
        │   │   ├── Endpoint 插件.md
        │   │   ├── Tool OAuth.md
        │   │   ├── 工具插件.md
        │   │   ├── 数据源插件.md
        │   │   ├── 模型供应商插件.md
        │   │   └── 触发器插件.md
        │   └── 速查表.md
        ├── 快速开始
        │   ├── Dify 插件 CLI.md
        │   ├── Dify 插件.md
        │   └── 选择插件类型.md
        └── 特性与规范
            ├── 插件类型
            │   ├── Manifest.md
            │   ├── 多语言 README.md
            │   ├── 工具返回.md
            │   ├── 持久化存储.md
            │   ├── 插件调试.md
            │   ├── 模型 API 接口.md
            │   ├── 模型规范.md
            │   ├── 输出插件日志.md
            │   └── 通用规范.md
            └── 高级开发
                └── 反向调用
                    ├── Bundle 插件包.md
                    ├── Dify 服务的反向调用.md
                    ├── 反向调用模型.md
                    ├── 工具.md
                    ├── 应用.md
                    ├── 节点.md
                    └── 集成自定义模型.md
```

## 全部文档

| 路径 | 标题 | 摘要 / 关键词 | 来源 |
|---|---|---|---|
| `使用/Dify 文档.md` | Dify 文档 | 官方导航中的补充入口；使用 | [原文](<https://docs.dify.ai/zh/home>) |
| `使用/使用 Dify.md` | 使用 Dify | 在工作空间中构建、发布并监控 AI 应用；introduction, 使用 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/getting-started/introduction>) |
| `使用/发布/IP 访问控制.md` | IP 访问控制 | 使用可复用的 IP 策略，将应用访问范围限制为可信网络；ip-access-control, 使用, 发布 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/publish/ip-access-control>) |
| `使用/发布/MCP 服务器.md` | MCP 服务器 | publish-mcp, 使用, 发布 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/publish/publish-mcp>) |
| `使用/发布/Web App/Web App 设置.md` | Web App 设置 | Web App, web-app-settings, 使用, 发布 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/publish/webapp/web-app-settings>) |
| `使用/发布/Web App/Workflow Web 应用.md` | Workflow Web 应用 | 通过批处理、结果管理和流畅的使用体验，将工作流转变为强大的 Web 应用；Web App, workflow-webapp, 使用, 发布 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/publish/webapp/workflow-webapp>) |
| `使用/发布/Web App/嵌入 Web 应用.md` | 嵌入 Web 应用 | 通过 iframe、聊天气泡组件或自定义集成，将已发布的 Web 应用部署到任何网站；Web App, embedding-in-websites, 使用, 发布 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/publish/webapp/embedding-in-websites>) |
| `使用/发布/Web App/聊天 Web App.md` | 聊天 Web App | 将 Chatflow 转变为具备持久化历史记录和交互功能的完整对话界面；Web App, chatflow-webapp, 使用, 发布 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/publish/webapp/chatflow-webapp>) |
| `使用/发布/分享你的 AI 应用.md` | 分享你的 AI 应用 | README, 使用, 发布 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/publish/README>) |
| `使用/发布/发布应用到 Marketplace.md` | 发布应用到 Marketplace | 将你的应用发布到 Dify Marketplace，与全世界分享；publish-to-marketplace, 使用, 发布 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/publish/publish-to-marketplace>) |
| `使用/工作空间/个人设置.md` | 个人设置 | 管理你在所有工作空间中的个人资料和偏好设置；personal-account-management, 使用, 工作空间 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/workspace/personal-account-management>) |
| `使用/工作空间/导出和导入应用.md` | 导出和导入应用 | 导出应用以备份、分享或迁移，导入应用包以创建新应用或更新已有应用；export-import-apps, 使用, 工作空间 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/workspace/export-import-apps>) |
| `使用/工作空间/工作空间.md` | 工作空间 | 工作空间是 Dify 中的基础组织单位，你的团队所构建、配置和管理的一切都存在于工作空间中；readme, 使用, 工作空间 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/workspace/readme>) |
| `使用/工作空间/管理成员.md` | 管理成员 | 添加团队成员，并通过角色管理他们的访问权限；team-members-management, 使用, 工作空间 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/workspace/team-members-management>) |
| `使用/工作空间/计费.md` | 计费 | 管理工作空间订阅、计划变更以及 Dify 教育版优惠；subscription-management, 使用, 工作空间 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/workspace/subscription-management>) |
| `使用/监控/仪表盘.md` | 仪表盘 | 通过 Dify 内置的分析仪表盘监控性能、成本和用户参与度；analysis, 使用, 监控 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/monitor/analysis>) |
| `使用/监控/日志.md` | 日志 | 浏览与查看应用的对话和运行日志，了解日志保留规则，并管理已归档的工作流日志；logs, 使用, 监控 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/monitor/logs>) |
| `使用/监控/标注系统.md` | 标注系统 | annotation-reply, 使用, 监控 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/monitor/annotation-reply>) |
| `使用/监控/集成/集成 Arize.md` | 集成 Arize | integrate-arize, 使用, 监控, 集成 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/monitor/integrations/integrate-arize>) |
| `使用/监控/集成/集成 LangSmith.md` | 集成 LangSmith | integrate-langsmith, 使用, 监控, 集成 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/monitor/integrations/integrate-langsmith>) |
| `使用/监控/集成/集成 Langfuse.md` | 集成 Langfuse | integrate-langfuse, 使用, 监控, 集成 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/monitor/integrations/integrate-langfuse>) |
| `使用/监控/集成/集成 Opik.md` | 集成 Opik | integrate-opik, 使用, 监控, 集成 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/monitor/integrations/integrate-opik>) |
| `使用/监控/集成/集成 Phoenix.md` | 集成 Phoenix | integrate-phoenix, 使用, 监控, 集成 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/monitor/integrations/integrate-phoenix>) |
| `使用/监控/集成/集成 W&B Weave.md` | 集成 W&B Weave | 通过 W&B Weave 实现 Dify 应用的 LLM 可观测性，将追踪数据发送至 W&B Weave；integrate-weave, 使用, 监控, 集成 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/monitor/integrations/integrate-weave>) |
| `使用/监控/集成/集成阿里云云监控.md` | 集成阿里云云监控 | integrate-aliyun, 使用, 监控, 集成 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/monitor/integrations/integrate-aliyun>) |
| `使用/知识库/Agent 知识库/Agent 知识库.md` | Agent 知识库 | 由知识库替你阅读、整理和索引内容，你只需决定放入哪些内容，并检查检索结果；Agent 知识库, overview, 使用, 知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge-base/overview>) |
| `使用/知识库/Agent 知识库/从经典知识库升级到 Agent 知识库.md` | 从经典知识库升级到 Agent 知识库 | 将经典知识库迁移为 Agent 知识库；Agent 知识库, upgrade-from-classic, 使用, 知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge-base/upgrade-from-classic>) |
| `使用/知识库/Agent 知识库/创建 Agent 知识库.md` | 创建 Agent 知识库 | 创建 Agent 知识库，从数据源导入或上传文件来添加内容，为测试做好准备；Agent 知识库, create-knowledge-base, 使用, 知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge-base/create-knowledge-base>) |
| `使用/知识库/Agent 知识库/多模态检索.md` | 多模态检索 | 所选模型如何影响知识库中图片的索引与检索；Agent 知识库, multimodal-retrieval, 使用, 知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge-base/multimodal-retrieval>) |
| `使用/知识库/Agent 知识库/接入应用、Agent 和代码.md` | 接入应用、Agent 和代码 | Agent 知识库可在哪些地方使用，以及如何分别关闭各类访问；Agent 知识库, use-knowledge-in-apps, 使用, 知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge-base/use-knowledge-in-apps>) |
| `使用/知识库/Agent 知识库/检查已索引的文档.md` | 检查已索引的文档 | 查看文档是如何拆分、如何生成摘要的，并修正处理得不理想的内容；Agent 知识库, review-indexed-documents, 使用, 知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge-base/review-indexed-documents>) |
| `使用/知识库/Agent 知识库/检索设置.md` | 检索设置 | 控制知识库在检索时如何查找分段、如何为分段排序；Agent 知识库, retrieval-settings, 使用, 知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge-base/retrieval-settings>) |
| `使用/知识库/Agent 知识库/测试并调优检索.md` | 测试并调优检索 | 用真实问题测试知识库，用参考问题衡量检索效果，并在结果不理想时调优检索；Agent 知识库, test-and-tune, 使用, 知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge-base/test-and-tune>) |
| `使用/知识库/Agent 知识库/维护 Agent 知识库.md` | 维护 Agent 知识库 | 知识库上线后，处理概览页面提示的问题，保持数据源同步，并及时更新文档；Agent 知识库, maintain-knowledge-base, 使用, 知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge-base/maintain-knowledge-base>) |
| `使用/知识库/知识库.md` | 知识库 | 让应用依据你自己的内容作答，并选定要使用哪一类知识库；overview, 使用, 知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge/overview>) |
| `使用/知识库/知识库存储与文档配额.md` | 知识库存储与文档配额 | 工作空间的知识库最多能容纳多少文档、存储多少索引数据，哪些内容计入各项配额，以及达到上限后如何处理；knowledge-storage-limit, 使用, 知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge/knowledge-storage-limit>) |
| `使用/知识库/知识库请求频率限制.md` | 知识库请求频率限制 | 工作空间每分钟可发起多少次知识库请求、两类知识库各有哪些操作计入，以及达到上限后如何处理；knowledge-request-rate-limit, 使用, 知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge/knowledge-request-rate-limit>) |
| `使用/知识库/经典知识库/创建即用型知识库/创建即用型知识库.md` | 创建即用型知识库 | introduction, 使用, 创建即用型知识库, 知识库, 经典知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge/create-knowledge/introduction>) |
| `使用/知识库/经典知识库/创建即用型知识库/指定分段设置.md` | 指定分段设置 | chunking-and-cleaning-text, 使用, 创建即用型知识库, 知识库, 经典知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge/create-knowledge/chunking-and-cleaning-text>) |
| `使用/知识库/经典知识库/创建即用型知识库/指定索引方式与检索设置.md` | 指定索引方式与检索设置 | setting-indexing-methods, 使用, 创建即用型知识库, 知识库, 经典知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge/create-knowledge/setting-indexing-methods>) |
| `使用/知识库/经典知识库/在应用内集成知识库.md` | 在应用内集成知识库 | integrate-knowledge-within-application, 使用, 知识库, 经典知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge/integrate-knowledge-within-application>) |
| `使用/知识库/经典知识库/导入数据/上传本地文件.md` | 上传本地文件 | readme, 使用, 导入数据, 知识库, 经典知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge/create-knowledge/import-text-data/readme>) |
| `使用/知识库/经典知识库/导入数据/从 Notion 导入数据.md` | 从 Notion 导入数据 | sync-from-notion, 使用, 导入数据, 知识库, 经典知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge/create-knowledge/import-text-data/sync-from-notion>) |
| `使用/知识库/经典知识库/导入数据/从网页导入数据.md` | 从网页导入数据 | sync-from-website, 使用, 导入数据, 知识库, 经典知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge/create-knowledge/import-text-data/sync-from-website>) |
| `使用/知识库/经典知识库/构建自定义知识库/数据源授权.md` | 数据源授权 | authorize-data-source, 使用, 构建自定义知识库, 知识库, 经典知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge/knowledge-pipeline/authorize-data-source>) |
| `使用/知识库/经典知识库/构建自定义知识库/构建自定义知识库.md` | 构建自定义知识库 | readme, 使用, 构建自定义知识库, 知识库, 经典知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge/knowledge-pipeline/readme>) |
| `使用/知识库/经典知识库/构建自定义知识库/步骤一：创建知识流水线.md` | 步骤一：创建知识流水线 | create-knowledge-pipeline, 使用, 构建自定义知识库, 知识库, 经典知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge/knowledge-pipeline/create-knowledge-pipeline>) |
| `使用/知识库/经典知识库/构建自定义知识库/步骤三：发布知识流水线.md` | 步骤三：发布知识流水线 | publish-knowledge-pipeline, 使用, 构建自定义知识库, 知识库, 经典知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge/knowledge-pipeline/publish-knowledge-pipeline>) |
| `使用/知识库/经典知识库/构建自定义知识库/步骤二：编排知识流水线.md` | 步骤二：编排知识流水线 | knowledge-pipeline-orchestration, 使用, 构建自定义知识库, 知识库, 经典知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge/knowledge-pipeline/knowledge-pipeline-orchestration>) |
| `使用/知识库/经典知识库/构建自定义知识库/步骤五：管理和使用知识库.md` | 步骤五：管理和使用知识库 | manage-knowledge-base, 使用, 构建自定义知识库, 知识库, 经典知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge/knowledge-pipeline/manage-knowledge-base>) |
| `使用/知识库/经典知识库/构建自定义知识库/步骤四：上传文件.md` | 步骤四：上传文件 | upload-files, 使用, 构建自定义知识库, 知识库, 经典知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge/knowledge-pipeline/upload-files>) |
| `使用/知识库/经典知识库/测试检索.md` | 测试检索 | test-retrieval, 使用, 知识库, 经典知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge/test-retrieval>) |
| `使用/知识库/经典知识库/管理/管理文档元数据.md` | 管理文档元数据 | metadata, 使用, 知识库, 管理, 经典知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge/metadata>) |
| `使用/知识库/经典知识库/管理/维护知识库内容.md` | 维护知识库内容 | maintain-knowledge-documents, 使用, 知识库, 管理, 经典知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge/manage-knowledge/maintain-knowledge-documents>) |
| `使用/知识库/经典知识库/管理/调整知识库设置.md` | 调整知识库设置 | introduction, 使用, 知识库, 管理, 经典知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge/manage-knowledge/introduction>) |
| `使用/知识库/经典知识库/经典知识库.md` | 经典知识库 | 自己设置分段、索引和检索方式，设计专属的处理流程，或接入你已在运行的外部知识库；readme, 使用, 知识库, 经典知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge/readme>) |
| `使用/知识库/经典知识库/连接外部知识库/外部知识库 API.md` | 外部知识库 API | 外部知识服务必须实现的 API 规范，用于与 Dify 集成；external-knowledge-api, 使用, 知识库, 经典知识库, 连接外部知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge/external-knowledge-api>) |
| `使用/知识库/经典知识库/连接外部知识库/连接外部知识库.md` | 连接外部知识库 | 通过 API 连接将外部知识源集成到 Dify 应用中，以使用自定义 RAG 系统或第三方知识服务；connect-external-knowledge-base, 使用, 知识库, 经典知识库, 连接外部知识库 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/knowledge/connect-external-knowledge-base>) |
| `使用/编排/Agent/Agent.md` | Agent | 构建一次 Agent，既可作为独立应用使用，也可嵌入工作流；Agent, overview, 使用, 编排 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/build/new-agent/overview>) |
| `使用/编排/Agent/构建 Agent.md` | 构建 Agent | 创建 Agent 并塑造它的能力，可逐项手动配置，也可通过描述需求来构建；Agent, build, 使用, 编排 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/build/new-agent/build>) |
| `使用/编排/Workflow 与 Chatflow/Snippets.md` | Snippets | 在多个工作流中复用和共享节点组合；Workflow 与 Chatflow, snippet, 使用, 编排 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/build/snippet>) |
| `使用/编排/Workflow 与 Chatflow/Workflow 与 Chatflow.md` | Workflow 与 Chatflow | 构建将 AI 模型、工具和逻辑组合为可靠、可重复流程的 Agentic 工作流；Workflow 与 Chatflow, workflow-chatflow, 使用, 编排 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/build/workflow-chatflow>) |
| `使用/编排/Workflow 与 Chatflow/人工介入/人工介入.md` | 人工介入 | 暂停工作流以请求人工输入；Workflow 与 Chatflow, human-input, 人工介入, 使用, 编排 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/human-input>) |
| `使用/编排/Workflow 与 Chatflow/开始/开始节点.md` | 开始节点 | 选择工作流的启动方式：按需启动或自动运行；Workflow 与 Chatflow, start, 使用, 开始, 编排 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/start>) |
| `使用/编排/Workflow 与 Chatflow/开始/用户输入.md` | 用户输入 | 收集用户输入以启动 Workflow 和 Chatflow 应用；Workflow 与 Chatflow, user-input, 使用, 开始, 编排 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/user-input>) |
| `使用/编排/Workflow 与 Chatflow/快捷键.md` | 快捷键 | 使用键盘快捷键更快地构建 Dify 工作流；Workflow 与 Chatflow, shortcut-key, 使用, 编排 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/build/shortcut-key>) |
| `使用/编排/Workflow 与 Chatflow/版本控制.md` | 版本控制 | Workflow 与 Chatflow, version-control, 使用, 编排 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/build/version-control>) |
| `使用/编排/Workflow 与 Chatflow/编排逻辑.md` | 编排逻辑 | 构建 Workflow 或 Chatflow 时，如何排列、嵌套与复用节点；Workflow 与 Chatflow, orchestrate-node, 使用, 编排 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/build/orchestrate-node>) |
| `使用/编排/Workflow 与 Chatflow/节点/Agent 知识检索.md` | Agent 知识检索 | 检索 Agent 知识库，并将相关内容传给后续节点；Workflow 与 Chatflow, knowledge-retrieval-v2, 使用, 编排, 节点 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/knowledge-retrieval-v2>) |
| `使用/编排/Workflow 与 Chatflow/节点/Agent.md` | Agent | 将 Agent 作为工作流中的一步运行，通过推理和调用工具完成任务；Workflow 与 Chatflow, agent, 使用, 编排, 节点 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/agent>) |
| `使用/编排/Workflow 与 Chatflow/节点/HTTP 请求.md` | HTTP 请求 | Workflow 与 Chatflow, http-request, 使用, 编排, 节点 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/http-request>) |
| `使用/编排/Workflow 与 Chatflow/节点/If-Else.md` | If-Else | 为工作流添加条件逻辑和分支；Workflow 与 Chatflow, ifelse, 使用, 编排, 节点 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/ifelse>) |
| `使用/编排/Workflow 与 Chatflow/节点/代码.md` | 代码 | Workflow 与 Chatflow, code, 使用, 编排, 节点 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/code>) |
| `使用/编排/Workflow 与 Chatflow/节点/列表操作符.md` | 列表操作符 | 筛选、排序和选择数组中的元素；Workflow 与 Chatflow, list-operator, 使用, 编排, 节点 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/list-operator>) |
| `使用/编排/Workflow 与 Chatflow/节点/参数提取器.md` | 参数提取器 | Workflow 与 Chatflow, parameter-extractor, 使用, 编排, 节点 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/parameter-extractor>) |
| `使用/编排/Workflow 与 Chatflow/节点/变量聚合器.md` | 变量聚合器 | 将互斥工作流分支汇聚为单一输出；Workflow 与 Chatflow, variable-aggregator, 使用, 编排, 节点 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/variable-aggregator>) |
| `使用/编排/Workflow 与 Chatflow/节点/变量赋值器.md` | 变量赋值器 | 在 Chatflow 应用中管理持久化会话变量；Workflow 与 Chatflow, variable-assigner, 使用, 编排, 节点 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/variable-assigner>) |
| `使用/编排/Workflow 与 Chatflow/节点/大语言模型.md` | 大语言模型 | 调用语言模型进行文本生成和分析；Workflow 与 Chatflow, llm, 使用, 编排, 节点 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/llm>) |
| `使用/编排/Workflow 与 Chatflow/节点/工具节点.md` | 工具节点 | 连接外部服务和 API；Workflow 与 Chatflow, tools, 使用, 编排, 节点 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/tools>) |
| `使用/编排/Workflow 与 Chatflow/节点/循环.md` | 循环 | Workflow 与 Chatflow, loop, 使用, 编排, 节点 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/loop>) |
| `使用/编排/Workflow 与 Chatflow/节点/文档提取器.md` | 文档提取器 | Workflow 与 Chatflow, doc-extractor, 使用, 编排, 节点 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/doc-extractor>) |
| `使用/编排/Workflow 与 Chatflow/节点/模板转换.md` | 模板转换 | 使用 Jinja2 模板转换和格式化数据；Workflow 与 Chatflow, template, 使用, 编排, 节点 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/template>) |
| `使用/编排/Workflow 与 Chatflow/节点/直接回复.md` | 直接回复 | Workflow 与 Chatflow, answer, 使用, 编排, 节点 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/answer>) |
| `使用/编排/Workflow 与 Chatflow/节点/经典知识检索.md` | 经典知识检索 | 从经典知识库中检索相关内容，作为下游节点的上下文；Workflow 与 Chatflow, knowledge-retrieval, 使用, 编排, 节点 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/knowledge-retrieval>) |
| `使用/编排/Workflow 与 Chatflow/节点/输出.md` | 输出 | 将工作流结果返回给终端用户或 API 调用者；Workflow 与 Chatflow, output, 使用, 编排, 节点 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/output>) |
| `使用/编排/Workflow 与 Chatflow/节点/迭代.md` | 迭代 | Workflow 与 Chatflow, iteration, 使用, 编排, 节点 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/iteration>) |
| `使用/编排/Workflow 与 Chatflow/节点/问题分类器.md` | 问题分类器 | Workflow 与 Chatflow, question-classifier, 使用, 编排, 节点 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/question-classifier>) |
| `使用/编排/Workflow 与 Chatflow/触发器/Webhook 触发器.md` | Webhook 触发器 | Workflow 与 Chatflow, webhook-trigger, 使用, 编排, 触发器 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/trigger/webhook-trigger>) |
| `使用/编排/Workflow 与 Chatflow/触发器/定时触发器.md` | 定时触发器 | Workflow 与 Chatflow, schedule-trigger, 使用, 编排, 触发器 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/trigger/schedule-trigger>) |
| `使用/编排/Workflow 与 Chatflow/触发器/触发器.md` | 触发器 | Workflow 与 Chatflow, overview, 使用, 编排, 触发器 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/trigger/overview>) |
| `使用/编排/Workflow 与 Chatflow/触发器/集成触发器.md` | 集成触发器 | Workflow 与 Chatflow, plugin-trigger, 使用, 编排, 触发器 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/nodes/trigger/plugin-trigger>) |
| `使用/编排/Workflow 与 Chatflow/调试/单节点.md` | 单节点 | Workflow 与 Chatflow, step-run, 使用, 编排, 调试 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/debug/step-run>) |
| `使用/编排/Workflow 与 Chatflow/调试/变量检查器.md` | 变量检查器 | Workflow 与 Chatflow, variable-inspect, 使用, 编排, 调试 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/debug/variable-inspect>) |
| `使用/编排/Workflow 与 Chatflow/调试/处理错误.md` | 处理错误 | Workflow 与 Chatflow, predefined-error-handling-logic, 使用, 编排, 调试 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/build/predefined-error-handling-logic>) |
| `使用/编排/Workflow 与 Chatflow/调试/运行历史.md` | 运行历史 | Workflow 与 Chatflow, history-and-logs, 使用, 编排, 调试 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/debug/history-and-logs>) |
| `使用/编排/Workflow 与 Chatflow/调试/错误类型.md` | 错误类型 | Workflow 与 Chatflow, error-type, 使用, 编排, 调试 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/debug/error-type>) |
| `使用/编排/全局搜索.md` | 全局搜索 | 通过快捷键快速搜索并跳转到应用、Agent、集成、知识库和工作流节点；goto-anything, 使用, 编排 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/build/goto-anything>) |
| `使用/编排/基础应用/Agent.md` | Agent | 模型能够自主推理、决策并使用工具的对话式应用；agent, 使用, 基础应用, 编排 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/build/agent>) |
| `使用/编排/基础应用/文本生成应用.md` | 文本生成应用 | 通过提示词和用户输入生成文本的简单单轮应用；text-generator, 使用, 基础应用, 编排 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/build/text-generator>) |
| `使用/编排/基础应用/聊天助手.md` | 聊天助手 | 通过模型和提示词构建对话式应用的最简单方式；chatbot, 使用, 基础应用, 编排 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/build/chatbot>) |
| `使用/编排/应用工具箱.md` | 应用工具箱 | 让 Dify 应用更实用的可选功能；additional-features, 使用, 编排 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/build/additional-features>) |
| `使用/集成/Dify 工具.md` | Dify 工具 | 管理使 LLM 能够与外部服务和 API 交互的工具；tools, 使用, 集成 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/workspace/tools>) |
| `使用/集成/模型供应商.md` | 模型供应商 | 使用你的 AI 消息额度调用模型，或连接你自己的供应商账户和密钥；model-providers, 使用, 集成 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/workspace/model-providers>) |
| `使用/集成/自定义端点/使用 Cloudflare Workers 部署自定义端点.md` | 使用 Cloudflare Workers 部署自定义端点 | cloudflare-worker, 使用, 自定义端点, 集成 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/workspace/api-extension/cloudflare-worker>) |
| `使用/集成/自定义端点/外部数据工具.md` | 外部数据工具 | external-data-tool-api-extension, 使用, 自定义端点, 集成 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/workspace/api-extension/external-data-tool-api-extension>) |
| `使用/集成/自定义端点/敏感内容审查.md` | 敏感内容审查 | moderation-api-extension, 使用, 自定义端点, 集成 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/workspace/api-extension/moderation-api-extension>) |
| `使用/集成/自定义端点/自定义端点.md` | 自定义端点 | api-extension, 使用, 自定义端点, 集成 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/workspace/api-extension/api-extension>) |
| `使用/集成/集成.md` | 集成 | 连接 Dify 与模型供应商、工具、数据来源和外部服务；plugins, 使用, 集成 | [原文](<https://docs.dify.ai/zh/cloud/use-dify/workspace/plugins>) |
| `学习/教程/30 分钟快速入门.md` | 30 分钟快速入门 | 通过示例应用深入了解 Dify；quick-start, 学习, 教程 | [原文](<https://docs.dify.ai/zh/quick-start>) |
| `学习/教程/ChatFlow 实战：搭建 Twitter 账号分析助手.md` | ChatFlow 实战：搭建 Twitter 账号分析助手 | twitter-chatflow, 学习, 教程 | [原文](<https://docs.dify.ai/zh/learn/tutorials/twitter-chatflow>) |
| `学习/教程/使用文件上传搭建文章理解助手.md` | 使用文件上传搭建文章理解助手 | article-reader, 学习, 教程 | [原文](<https://docs.dify.ai/zh/learn/tutorials/article-reader>) |
| `学习/教程/使用知识库搭建智能客服机器人.md` | 使用知识库搭建智能客服机器人 | customer-service-bot, 学习, 教程 | [原文](<https://docs.dify.ai/zh/learn/tutorials/customer-service-bot>) |
| `学习/教程/如何搭建 AI 图片生成应用.md` | 如何搭建 AI 图片生成应用 | build-ai-image-generation-app, 学习, 教程 | [原文](<https://docs.dify.ai/zh/learn/tutorials/build-ai-image-generation-app>) |
| `学习/教程/工作流 101/第 1 课：什么是工作流.md` | 第 1 课：什么是工作流 | lesson-01, 学习, 工作流 101, 教程 | [原文](<https://docs.dify.ai/zh/learn/tutorials/workflow-101/lesson-01>) |
| `学习/教程/工作流 101/第 10 课：发布和监控你的 AI 应用.md` | 第 10 课：发布和监控你的 AI 应用 | lesson-10, 学习, 工作流 101, 教程 | [原文](<https://docs.dify.ai/zh/learn/tutorials/workflow-101/lesson-10>) |
| `学习/教程/工作流 101/第 2 课：流程的头和尾（开始与输出节点）.md` | 第 2 课：流程的头和尾（开始与输出节点） | lesson-02, 学习, 工作流 101, 教程 | [原文](<https://docs.dify.ai/zh/learn/tutorials/workflow-101/lesson-02>) |
| `学习/教程/工作流 101/第 3 课：工作流的大脑（LLM 节点）.md` | 第 3 课：工作流的大脑（LLM 节点） | lesson-03, 学习, 工作流 101, 教程 | [原文](<https://docs.dify.ai/zh/learn/tutorials/workflow-101/lesson-03>) |
| `学习/教程/工作流 101/第 4 课：小抄（知识检索）.md` | 第 4 课：小抄（知识检索） | lesson-04, 学习, 工作流 101, 教程 | [原文](<https://docs.dify.ai/zh/learn/tutorials/workflow-101/lesson-04>) |
| `学习/教程/工作流 101/第 5 课：工作流的岔路口（分类与执行）.md` | 第 5 课：工作流的岔路口（分类与执行） | lesson-05, 学习, 工作流 101, 教程 | [原文](<https://docs.dify.ai/zh/learn/tutorials/workflow-101/lesson-05>) |
| `学习/教程/工作流 101/第 6 课：处理多个任务（参数提取 & 迭代）.md` | 第 6 课：处理多个任务（参数提取 & 迭代） | lesson-06, 学习, 工作流 101, 教程 | [原文](<https://docs.dify.ai/zh/learn/tutorials/workflow-101/lesson-06>) |
| `学习/教程/工作流 101/第 7 课：增强工作流（工具）.md` | 第 7 课：增强工作流（工具） | lesson-07, 学习, 工作流 101, 教程 | [原文](<https://docs.dify.ai/zh/learn/tutorials/workflow-101/lesson-07>) |
| `学习/教程/工作流 101/第 8 课：Agent 节点.md` | 第 8 课：Agent 节点 | lesson-08, 学习, 工作流 101, 教程 | [原文](<https://docs.dify.ai/zh/learn/tutorials/workflow-101/lesson-08>) |
| `学习/教程/工作流 101/第 9 课：排版设计师（模板）.md` | 第 9 课：排版设计师（模板） | lesson-09, 学习, 工作流 101, 教程 | [原文](<https://docs.dify.ai/zh/learn/tutorials/workflow-101/lesson-09>) |
| `学习/教程/简单聊天机器人.md` | 简单聊天机器人 | Hello World；simple-chatbot, 学习, 教程 | [原文](<https://docs.dify.ai/zh/learn/tutorials/simple-chatbot>) |
| `学习/核心概念.md` | 核心概念 | Dify 核心概念快速概览；key-concepts, 学习 | [原文](<https://docs.dify.ai/zh/learn/key-concepts>) |
| `开发者资源/API/应用 API/人工介入/提交人工介入表单.md` | 提交人工介入表单 | **适用于**：Chatflow、Workflow。；API, submit-human-input-form, 人工介入, 应用 API, 开发者资源 | [原文](<https://docs.dify.ai/zh/api-reference/human-input/submit-human-input-form>) |
| `开发者资源/API/应用 API/人工介入/获取人工介入表单.md` | 获取人工介入表单 | **适用于**：Chatflow、Workflow。；API, get-human-input-form, 人工介入, 应用 API, 开发者资源 | [原文](<https://docs.dify.ai/zh/api-reference/human-input/get-human-input-form>) |
| `开发者资源/API/应用 API/会话管理/删除会话.md` | 删除会话 | **适用于**：Chatflow、Agent、聊天助手、旧版 Agent。；API, delete-conversation, 会话管理, 应用 API, 开发者资源 | [原文](<https://docs.dify.ai/zh/api-reference/conversations/delete-conversation>) |
| `开发者资源/API/应用 API/会话管理/更新会话变量.md` | 更新会话变量 | **适用于**：Chatflow、聊天助手、旧版 Agent。；API, update-conversation-variable, 会话管理, 应用 API, 开发者资源 | [原文](<https://docs.dify.ai/zh/api-reference/conversations/update-conversation-variable>) |
| `开发者资源/API/应用 API/会话管理/获取会话列表.md` | 获取会话列表 | **适用于**：Chatflow、Agent、聊天助手、旧版 Agent。；API, list-conversations, 会话管理, 应用 API, 开发者资源 | [原文](<https://docs.dify.ai/zh/api-reference/conversations/list-conversations>) |
| `开发者资源/API/应用 API/会话管理/获取会话历史消息.md` | 获取会话历史消息 | **适用于**：Chatflow、Agent、聊天助手、旧版 Agent。；API, list-conversation-messages, 会话管理, 应用 API, 开发者资源 | [原文](<https://docs.dify.ai/zh/api-reference/conversations/list-conversation-messages>) |
| `开发者资源/API/应用 API/会话管理/获取会话变量.md` | 获取会话变量 | **适用于**：Chatflow、聊天助手、旧版 Agent。；API, list-conversation-variables, 会话管理, 应用 API, 开发者资源 | [原文](<https://docs.dify.ai/zh/api-reference/conversations/list-conversation-variables>) |
| `开发者资源/API/应用 API/会话管理/重命名会话.md` | 重命名会话 | **适用于**：Chatflow、Agent、聊天助手、旧版 Agent。；API, rename-conversation, 会话管理, 应用 API, 开发者资源 | [原文](<https://docs.dify.ai/zh/api-reference/conversations/rename-conversation>) |
| `开发者资源/API/应用 API/对话消息/停止响应.md` | 停止响应 | **适用于**：Chatflow、Agent、聊天助手、旧版 Agent。；API, stop-chat-message-generation, 对话消息, 应用 API, 开发者资源 | [原文](<https://docs.dify.ai/zh/api-reference/chat-messages/stop-chat-message-generation>) |
| `开发者资源/API/应用 API/对话消息/发送对话消息.md` | 发送对话消息 | **适用于**：Chatflow、Agent、聊天助手、旧版 Agent。；API, send-chat-message, 对话消息, 应用 API, 开发者资源 | [原文](<https://docs.dify.ai/zh/api-reference/chat-messages/send-chat-message>) |
| `开发者资源/API/应用 API/对话消息/获取下一轮建议问题列表.md` | 获取下一轮建议问题列表 | **适用于**：Chatflow、Agent、聊天助手、旧版 Agent。；API, get-next-suggested-questions, 对话消息, 应用 API, 开发者资源 | [原文](<https://docs.dify.ai/zh/api-reference/chat-messages/get-next-suggested-questions>) |
| `开发者资源/API/应用 API/工作流运行/停止工作流任务.md` | 停止工作流任务 | **适用于**：Workflow。；API, stop-workflow-task, 工作流运行, 应用 API, 开发者资源 | [原文](<https://docs.dify.ai/zh/api-reference/workflow-runs/stop-workflow-task>) |
| `开发者资源/API/应用 API/工作流运行/执行工作流.md` | 执行工作流 | **适用于**：Workflow。；API, run-workflow, 工作流运行, 应用 API, 开发者资源 | [原文](<https://docs.dify.ai/zh/api-reference/workflow-runs/run-workflow>) |
| `开发者资源/API/应用 API/工作流运行/按 ID 执行工作流.md` | 按 ID 执行工作流 | **适用于**：Workflow。；API, run-workflow-by-id, 工作流运行, 应用 API, 开发者资源 | [原文](<https://docs.dify.ai/zh/api-reference/workflow-runs/run-workflow-by-id>) |
| `开发者资源/API/应用 API/工作流运行/流式获取工作流事件.md` | 流式获取工作流事件 | **适用于**：Chatflow、Workflow。；API, stream-workflow-events, 工作流运行, 应用 API, 开发者资源 | [原文](<https://docs.dify.ai/zh/api-reference/workflow-runs/stream-workflow-events>) |
| `开发者资源/API/应用 API/工作流运行/获取工作流执行情况.md` | 获取工作流执行情况 | **适用于**：Chatflow、Workflow。；API, get-workflow-run-detail, 工作流运行, 应用 API, 开发者资源 | [原文](<https://docs.dify.ai/zh/api-reference/workflow-runs/get-workflow-run-detail>) |
| `开发者资源/API/应用 API/工作流运行/获取工作流日志.md` | 获取工作流日志 | **适用于**：Chatflow、Workflow。；API, list-workflow-logs, 工作流运行, 应用 API, 开发者资源 | [原文](<https://docs.dify.ai/zh/api-reference/workflow-runs/list-workflow-logs>) |
| `开发者资源/API/应用 API/应用配置/获取应用 WebApp 设置.md` | 获取应用 WebApp 设置 | **适用于**：Chatflow、Workflow、Agent、聊天助手、旧版 Agent、文本生成应用。；API, get-app-webapp-settings, 应用 API, 应用配置, 开发者资源 | [原文](<https://docs.dify.ai/zh/api-reference/applications/get-app-webapp-settings>) |
| `开发者资源/API/应用 API/应用配置/获取应用元数据.md` | 获取应用元数据 | **适用于**：Chatflow、Workflow、Agent、聊天助手、旧版 Agent、文本生成应用。；API, get-app-meta, 应用 API, 应用配置, 开发者资源 | [原文](<https://docs.dify.ai/zh/api-reference/applications/get-app-meta>) |
| `开发者资源/API/应用 API/应用配置/获取应用参数.md` | 获取应用参数 | **适用于**：Chatflow、Workflow、Agent、聊天助手、旧版 Agent、文本生成应用。；API, get-app-parameters, 应用 API, 应用配置, 开发者资源 | [原文](<https://docs.dify.ai/zh/api-reference/applications/get-app-parameters>) |
| `开发者资源/API/应用 API/应用配置/获取应用基本信息.md` | 获取应用基本信息 | **适用于**：Chatflow、Workflow、Agent、聊天助手、旧版 Agent、文本生成应用。；API, get-app-info, 应用 API, 应用配置, 开发者资源 | [原文](<https://docs.dify.ai/zh/api-reference/applications/get-app-info>) |
| `开发者资源/API/应用 API/文件操作/上传文件.md` | 上传文件 | **适用于**：Chatflow、Workflow、Agent、聊天助手、旧版 Agent、文本生成应用。；API, upload-file, 应用 API, 开发者资源, 文件操作 | [原文](<https://docs.dify.ai/zh/api-reference/files/upload-file>) |
| `开发者资源/API/应用 API/文件操作/下载文件.md` | 下载文件 | **适用于**：Chatflow、聊天助手、旧版 Agent、文本生成应用。；API, download-file, 应用 API, 开发者资源, 文件操作 | [原文](<https://docs.dify.ai/zh/api-reference/files/download-file>) |
| `开发者资源/API/应用 API/文本生成消息/停止响应.md` | 停止响应 | **适用于**：文本生成应用。；API, stop-completion-message-generation, 应用 API, 开发者资源, 文本生成消息 | [原文](<https://docs.dify.ai/zh/api-reference/completion-messages/stop-completion-message-generation>) |
| `开发者资源/API/应用 API/文本生成消息/发送消息.md` | 发送消息 | **适用于**：文本生成应用。；API, send-completion-message, 应用 API, 开发者资源, 文本生成消息 | [原文](<https://docs.dify.ai/zh/api-reference/completion-messages/send-completion-message>) |
| `开发者资源/API/应用 API/标注管理/创建标注.md` | 创建标注 | **适用于**：Chatflow、聊天助手、旧版 Agent。；API, create-annotation, 应用 API, 开发者资源, 标注管理 | [原文](<https://docs.dify.ai/zh/api-reference/annotations/create-annotation>) |
| `开发者资源/API/应用 API/标注管理/删除标注.md` | 删除标注 | **适用于**：Chatflow、聊天助手、旧版 Agent。；API, delete-annotation, 应用 API, 开发者资源, 标注管理 | [原文](<https://docs.dify.ai/zh/api-reference/annotations/delete-annotation>) |
| `开发者资源/API/应用 API/标注管理/更新标注.md` | 更新标注 | **适用于**：Chatflow、聊天助手、旧版 Agent。；API, update-annotation, 应用 API, 开发者资源, 标注管理 | [原文](<https://docs.dify.ai/zh/api-reference/annotations/update-annotation>) |
| `开发者资源/API/应用 API/标注管理/查询标注回复配置任务状态.md` | 查询标注回复配置任务状态 | **适用于**：Chatflow、聊天助手、旧版 Agent。；API, get-annotation-reply-job-status, 应用 API, 开发者资源, 标注管理 | [原文](<https://docs.dify.ai/zh/api-reference/annotations/get-annotation-reply-job-status>) |
| `开发者资源/API/应用 API/标注管理/获取标注列表.md` | 获取标注列表 | **适用于**：Chatflow、聊天助手、旧版 Agent。；API, list-annotations, 应用 API, 开发者资源, 标注管理 | [原文](<https://docs.dify.ai/zh/api-reference/annotations/list-annotations>) |
| `开发者资源/API/应用 API/标注管理/配置标注回复.md` | 配置标注回复 | **适用于**：Chatflow、聊天助手、旧版 Agent。；API, configure-annotation-reply, 应用 API, 开发者资源, 标注管理 | [原文](<https://docs.dify.ai/zh/api-reference/annotations/configure-annotation-reply>) |
| `开发者资源/API/应用 API/消息反馈/提交消息反馈.md` | 提交消息反馈 | **适用于**：Chatflow、聊天助手、旧版 Agent、文本生成应用。；API, submit-message-feedback, 应用 API, 开发者资源, 消息反馈 | [原文](<https://docs.dify.ai/zh/api-reference/feedback/submit-message-feedback>) |
| `开发者资源/API/应用 API/消息反馈/获取应用的消息反馈.md` | 获取应用的消息反馈 | **适用于**：Chatflow、聊天助手、旧版 Agent、文本生成应用。；API, list-app-feedbacks, 应用 API, 开发者资源, 消息反馈 | [原文](<https://docs.dify.ai/zh/api-reference/feedback/list-app-feedbacks>) |
| `开发者资源/API/应用 API/终端用户/获取终端用户信息.md` | 获取终端用户信息 | **适用于**：Chatflow、Workflow、Agent、聊天助手、旧版 Agent、文本生成应用。；API, get-end-user-info, 应用 API, 开发者资源, 终端用户 | [原文](<https://docs.dify.ai/zh/api-reference/end-users/get-end-user-info>) |
| `开发者资源/API/应用 API/语音与文字转换/文字转语音.md` | 文字转语音 | **适用于**：Chatflow、Workflow、Agent、聊天助手、旧版 Agent、文本生成应用。；API, convert-text-to-audio, 应用 API, 开发者资源, 语音与文字转换 | [原文](<https://docs.dify.ai/zh/api-reference/audio/convert-text-to-audio>) |
| `开发者资源/API/应用 API/语音与文字转换/语音转文字.md` | 语音转文字 | **适用于**：Chatflow、Workflow、Agent、聊天助手、旧版 Agent、文本生成应用。；API, convert-audio-to-text, 应用 API, 开发者资源, 语音与文字转换 | [原文](<https://docs.dify.ai/zh/api-reference/audio/convert-audio-to-text>) |
| `开发者资源/API/指南/API 概览/Agent API.md` | Agent API | 面向 Agent 应用的 API，涵盖流式对话消息、会话管理、文件上传及应用配置；API, API 概览, agent, 开发者资源, 指南 | [原文](<https://docs.dify.ai/zh/api-reference/guides/agent>) |
| `开发者资源/API/指南/API 概览/Chatflow 应用 API.md` | Chatflow 应用 API | Chatflow 应用 API，涵盖对话消息、工作流级别流式事件、会话管理、人工介入暂停；API, API 概览, chatflow, 开发者资源, 指南 | [原文](<https://docs.dify.ai/zh/api-reference/guides/chatflow>) |
| `开发者资源/API/指南/API 概览/Workflow 应用 API.md` | Workflow 应用 API | Workflow 应用 API，涵盖工作流执行、运行控制与流式传输、人工介入暂停、运行历史查询；API, API 概览, workflow, 开发者资源, 指南 | [原文](<https://docs.dify.ai/zh/api-reference/guides/workflow>) |
| `开发者资源/API/指南/API 概览/对话型应用 API.md` | 对话型应用 API | 面向聊天助手和旧版 Agent 应用的 API，涵盖对话消息、会话管理、文件上传、语音转换及标注管理；API, API 概览, chat, 开发者资源, 指南 | [原文](<https://docs.dify.ai/zh/api-reference/guides/chat>) |
| `开发者资源/API/指南/API 概览/文本生成应用 API.md` | 文本生成应用 API | 面向文本生成应用的 API，涵盖文本生成消息、文件上传、语音转换及反馈收集；API, API 概览, completion, 开发者资源, 指南 | [原文](<https://docs.dify.ai/zh/api-reference/guides/completion>) |
| `开发者资源/API/指南/API 概览/知识库/Agent 知识库 API.md` | Agent 知识库 API | 在自己的代码中查询 Agent 知识库，回查某次运行检索到的内容，并维护知识库的文档、数据源和设置；API, API 概览, knowledge-base, 开发者资源, 指南, 知识库 | [原文](<https://docs.dify.ai/zh/api-reference/guides/knowledge-base>) |
| `开发者资源/API/指南/API 概览/知识库/知识库 API.md` | 知识库 API | 创建两种知识库 API 通用的 API 密钥并设置访问范围，安全地替换密钥，以及查明调用被拒绝的原因；API, API 概览, knowledge-base-api, 开发者资源, 指南, 知识库 | [原文](<https://docs.dify.ai/zh/api-reference/guides/knowledge-base-api>) |
| `开发者资源/API/指南/API 概览/知识库/经典知识库 API.md` | 经典知识库 API | 用于管理经典知识库、文档、分段、元数据、标签和知识流水线的 API；API, API 概览, knowledge, 开发者资源, 指南, 知识库 | [原文](<https://docs.dify.ai/zh/api-reference/guides/knowledge>) |
| `开发者资源/API/指南/Dify API 快速开始.md` | Dify API 快速开始 | 获取 API 密钥、发起第一个请求，并找到你的应用类型对应的接口；API, get-started, 开发者资源, 指南 | [原文](<https://docs.dify.ai/zh/api-reference/guides/get-started>) |
| `开发者资源/API/指南/人工介入 API 集成流程.md` | 人工介入 API 集成流程 | 通过 API 处理暂停中的人工介入表单的端到端流程；API, human-input-flow, 开发者资源, 指南 | [原文](<https://docs.dify.ai/zh/api-reference/guides/human-input-flow>) |
| `开发者资源/API/指南/处理流式响应.md` | 处理流式响应 | 选择响应模式、解析 SSE 流、按事件类型分发处理，并在连接断开后恢复；API, streaming, 开发者资源, 指南 | [原文](<https://docs.dify.ai/zh/api-reference/guides/streaming>) |
| `开发者资源/API/指南/处理错误与速率限制.md` | 处理错误与速率限制 | 错误响应的统一结构、各状态码类别的含义，以及哪些失败值得重试；API, errors, 开发者资源, 指南 | [原文](<https://docs.dify.ai/zh/api-reference/guides/errors>) |
| `开发者资源/API/指南/终端用户身份.md` | 终端用户身份 | user 字段标识什么、限定哪些数据，以及为何要在各次调用间保持一致；API, end-user-identity, 开发者资源, 指南 | [原文](<https://docs.dify.ai/zh/api-reference/guides/end-user-identity>) |
| `开发者资源/API/知识库 API/Agent 知识库/删除作业/获取删除作业.md` | 获取删除作业 | 返回通过 [删除文档](/zh/api-reference/documents-and-chunks/delete-document)、[删除文档文件](/zh/api-reference/documents-and-chunks/delete-document-file) 或 [删除数据源](/zh/api-reference/sources/delete-source) 发起的删除进度，或 [批量删除文档文件](/zh/api-reference/documents-and-chunks/delete-document-files-in-batch) 中单个文件的删除进度。轮询直到 `ru…；API, Agent 知识库, get-deletion-job, 删除作业, 开发者资源, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/deletion-jobs/get-deletion-job>) |
| `开发者资源/API/知识库 API/Agent 知识库/删除作业/获取删除批次.md` | 获取删除批次 | 返回一次 [批量删除文档文件](/zh/api-reference/documents-and-chunks/delete-document-files-in-batch) 请求，包括每个文件的处理结果，以及每个已受理文件的删除作业当前状态。只有发送该批次的 API 密钥能读取它。；API, Agent 知识库, get-deletion-batch, 删除作业, 开发者资源, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/deletion-jobs/get-deletion-batch>) |
| `开发者资源/API/知识库 API/Agent 知识库/数据源/创建数据源.md` | 创建数据源 | 添加一个通过现有连接读取内容的数据源，连接可通过 [获取数据源连接列表](/zh/api-reference/sources/list-source-connections) 查找。此操作不会抓取或导入任何内容。；API, Agent 知识库, create-source, 开发者资源, 数据源, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/sources/create-source>) |
| `开发者资源/API/知识库 API/Agent 知识库/数据源/删除数据源.md` | 删除数据源 | 请求删除数据源，并返回删除作业。；API, Agent 知识库, delete-source, 开发者资源, 数据源, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/sources/delete-source>) |
| `开发者资源/API/知识库 API/Agent 知识库/数据源/更新同步策略.md` | 更新同步策略 | 设置数据源的定时同步，替换原有设置，并返回新设置。；API, Agent 知识库, update-sync-policy, 开发者资源, 数据源, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/sources/update-sync-policy>) |
| `开发者资源/API/知识库 API/Agent 知识库/数据源/更新数据源.md` | 更新数据源 | 更新数据源的名称、状态、URI、元数据或提供商参数；配置有变化时，可同时启动一次同步。；API, Agent 知识库, update-source, 开发者资源, 数据源, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/sources/update-source>) |
| `开发者资源/API/知识库 API/Agent 知识库/数据源/测试数据源凭据.md` | 测试数据源凭据 | 由数据源提供商验证该数据源的凭据，并返回结果。不会对数据源做任何更改。；API, Agent 知识库, test-source-credentials, 开发者资源, 数据源, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/sources/test-source-credentials>) |
| `开发者资源/API/知识库 API/Agent 知识库/数据源/获取同步策略.md` | 获取同步策略 | 返回数据源的定时同步设置，以及 [更新同步策略](/zh/api-reference/sources/update-sync-policy) 所需的 `revision`。；API, Agent 知识库, get-sync-policy, 开发者资源, 数据源, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/sources/get-sync-policy>) |
| `开发者资源/API/知识库 API/Agent 知识库/数据源/获取数据源.md` | 获取数据源 | 返回一个数据源的存储内容。；API, Agent 知识库, get-source, 开发者资源, 数据源, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/sources/get-source>) |
| `开发者资源/API/知识库 API/Agent 知识库/数据源/获取数据源列表.md` | 获取数据源列表 | 按数据源 ID 升序列出知识库的数据源。每个数据源附带其定时同步设置、最近一次完成的同步或导入，以及当前运行；没有正在进行的运行时，改为附带最近一次同步。；API, Agent 知识库, list-sources, 开发者资源, 数据源, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/sources/list-sources>) |
| `开发者资源/API/知识库 API/Agent 知识库/数据源/获取数据源文件列表.md` | 获取数据源文件列表 | 列出在线云盘数据源在其提供商处可见的存储桶和文件。；API, Agent 知识库, list-source-files, 开发者资源, 数据源, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/sources/list-source-files>) |
| `开发者资源/API/知识库 API/Agent 知识库/数据源/获取数据源连接列表.md` | 获取数据源连接列表 | 列出该知识库的连接，最早的在前。将某个连接的 `id` 作为 `connectionId` 传给 [创建数据源](/zh/api-reference/sources/create-source)，即可添加通过该连接读取内容的数据源。；API, Agent 知识库, list-source-connections, 开发者资源, 数据源, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/sources/list-source-connections>) |
| `开发者资源/API/知识库 API/Agent 知识库/数据源/获取数据源页面列表.md` | 获取数据源页面列表 | 列出在线文档数据源在其提供商处可见的页面，按提供商工作空间分组。；API, Agent 知识库, list-source-pages, 开发者资源, 数据源, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/sources/list-source-pages>) |
| `开发者资源/API/知识库 API/Agent 知识库/数据源同步与导入/取消数据源运行.md` | 取消数据源运行 | 取消尚未结束的数据源运行，并返回该运行。；API, Agent 知识库, cancel-source-run, 开发者资源, 数据源同步与导入, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/source-syncs-and-imports/cancel-source-run>) |
| `开发者资源/API/知识库 API/Agent 知识库/数据源同步与导入/同步数据源.md` | 同步数据源 | 立即启动数据源同步，并返回运行。用其 `id` 轮询 [获取数据源运行](/zh/api-reference/source-syncs-and-imports/get-source-run)，直到 `state` 为 `completed`、`failed` 或 `canceled`。；API, Agent 知识库, sync-source, 开发者资源, 数据源同步与导入, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/source-syncs-and-imports/sync-source>) |
| `开发者资源/API/知识库 API/Agent 知识库/数据源同步与导入/导入所选页面.md` | 导入所选页面 | 将抓取预览中的页面导入为文档，并返回同一个运行，此时它已排队等待导入。用相同的 `id` 轮询 [获取数据源运行](/zh/api-reference/source-syncs-and-imports/get-source-run)，直到 `state` 为 `completed`、`failed` 或 `canceled`。；API, Agent 知识库, import-selected-pages, 开发者资源, 数据源同步与导入, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/source-syncs-and-imports/import-selected-pages>) |
| `开发者资源/API/知识库 API/Agent 知识库/数据源同步与导入/导入数据源条目.md` | 导入数据源条目 | 将在线文档页面或在线云盘文件导入连接器数据源，并返回运行。用其 `id` 轮询 [获取数据源运行](/zh/api-reference/source-syncs-and-imports/get-source-run)，直到 `state` 为 `completed`、`failed` 或 `canceled`。；API, Agent 知识库, import-source-items, 开发者资源, 数据源同步与导入, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/source-syncs-and-imports/import-source-items>) |
| `开发者资源/API/知识库 API/Agent 知识库/数据源同步与导入/导入网站页面.md` | 导入网站页面 | 将已知 URL 导入网站数据源，并返回运行。用其 `id` 轮询 [获取数据源运行](/zh/api-reference/source-syncs-and-imports/get-source-run)，直到 `state` 为 `completed`、`failed` 或 `canceled`。；API, Agent 知识库, import-website-pages, 开发者资源, 数据源同步与导入, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/source-syncs-and-imports/import-website-pages>) |
| `开发者资源/API/知识库 API/Agent 知识库/数据源同步与导入/获取抓取预览页面列表.md` | 获取抓取预览页面列表 | 列出抓取预览发现的页面，以及传给 [导入所选页面](/zh/api-reference/source-syncs-and-imports/import-selected-pages) 所需的 `page_id`。不返回页面内容。；API, Agent 知识库, list-crawl-preview-pages, 开发者资源, 数据源同步与导入, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/source-syncs-and-imports/list-crawl-preview-pages>) |
| `开发者资源/API/知识库 API/Agent 知识库/数据源同步与导入/获取数据源运行.md` | 获取数据源运行 | 返回一个数据源运行。可按 ID 跟踪任意运行，包括 [获取数据源列表](/zh/api-reference/sources/list-sources) 不显示的抓取预览，以及从预览发起的导入。；API, Agent 知识库, get-source-run, 开发者资源, 数据源同步与导入, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/source-syncs-and-imports/get-source-run>) |
| `开发者资源/API/知识库 API/Agent 知识库/数据源同步与导入/获取数据源运行列表.md` | 获取数据源运行列表 | 列出知识库的数据源运行（同步、抓取预览和导入），包括由定时同步或在 Dify 中启动的运行。只列出该密钥可读取的数据源的运行。；API, Agent 知识库, list-source-runs, 开发者资源, 数据源同步与导入, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/source-syncs-and-imports/list-source-runs>) |
| `开发者资源/API/知识库 API/Agent 知识库/数据源同步与导入/重试数据源运行.md` | 重试数据源运行 | 以相同的运行 ID，从头重新执行状态为 `failed` 或 `canceled` 的数据源运行，并返回已排队的运行。进度会重置，导入会重新获取每个条目，同步会从头开始。已选定页面的抓取预览会直接重新导入这些页面，不再抓取。；API, Agent 知识库, retry-source-run, 开发者资源, 数据源同步与导入, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/source-syncs-and-imports/retry-source-run>) |
| `开发者资源/API/知识库 API/Agent 知识库/数据源同步与导入/预览网站抓取.md` | 预览网站抓取 | 抓取网站数据源，并暂存找到的页面供你挑选，不导入任何内容。返回运行。用其 `id` 轮询 [获取数据源运行](/zh/api-reference/source-syncs-and-imports/get-source-run)，直到 `state` 为 `preview_ready`、`zero_results`、`failed` 或 `canceled`。；API, Agent 知识库, preview-website-crawl, 开发者资源, 数据源同步与导入, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/source-syncs-and-imports/preview-website-crawl>) |
| `开发者资源/API/知识库 API/Agent 知识库/文档与分段/删除文档.md` | 删除文档 | 请求删除一个文档，并返回删除作业。该操作会移除文档本身、其所有修订版本，以及仅由该文档使用的文档文件。作业完成后，该文档不再占用文档配额。；API, Agent 知识库, delete-document, 开发者资源, 文档与分段, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/documents-and-chunks/delete-document>) |
| `开发者资源/API/知识库 API/Agent 知识库/文档与分段/删除文档文件.md` | 删除文档文件 | 请求删除一个文档文件，并返回删除作业。基于该文件构建的所有修订版本都不再通过 [获取分段列表](/zh/api-reference/documents-and-chunks/list-chunks) 返回分段。；API, Agent 知识库, delete-document-file, 开发者资源, 文档与分段, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/documents-and-chunks/delete-document-file>) |
| `开发者资源/API/知识库 API/Agent 知识库/文档与分段/批量删除文档文件.md` | 批量删除文档文件 | 一次调用请求删除最多 100 个文档文件，并返回每个文件的处理结果。与 [删除文档文件](/zh/api-reference/documents-and-chunks/delete-document-file) 一样，不要删除生效修订版本的文件。；API, Agent 知识库, delete-document-files-in-batch, 开发者资源, 文档与分段, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/documents-and-chunks/delete-document-files-in-batch>) |
| `开发者资源/API/知识库 API/Agent 知识库/文档与分段/按文件获取文档.md` | 按文件获取文档 | 返回文档 ID，以及由文档文件某个版本构建的修订版本。可用它从引用找到对应的文档：查询记录和研究任务结果通过 `documentAssetId` 和 `documentVersion` 引用文档文件。；API, Agent 知识库, get-document-by-file, 开发者资源, 文档与分段, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/documents-and-chunks/get-document-by-file>) |
| `开发者资源/API/知识库 API/Agent 知识库/文档与分段/更新文档元数据.md` | 更新文档元数据 | 将键合并到文档的 `user_metadata` 中，并返回更新后的文档。与此路径上的其他操作不同，它接收的是文档 ID，而不是文档文件 ID。；API, Agent 知识库, update-document-metadata, 开发者资源, 文档与分段, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/documents-and-chunks/update-document-metadata>) |
| `开发者资源/API/知识库 API/Agent 知识库/文档与分段/获取分段.md` | 获取分段 | 返回文档某个修订版本中的一个分段。接收 [获取文档列表](/zh/api-reference/documents-and-chunks/list-documents) 返回的文档 ID（而不是文档文件 ID），以及修订版本号和分段 ID。；API, Agent 知识库, get-chunk, 开发者资源, 文档与分段, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/documents-and-chunks/get-chunk>) |
| `开发者资源/API/知识库 API/Agent 知识库/文档与分段/获取分段列表.md` | 获取分段列表 | 列出文档某个修订版本的分段，按分段 ID 排序，而非按在文档中的位置排序。接收 [获取文档列表](/zh/api-reference/documents-and-chunks/list-documents) 返回的文档 ID（而不是文档文件 ID），以及修订版本号。；API, Agent 知识库, list-chunks, 开发者资源, 文档与分段, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/documents-and-chunks/list-chunks>) |
| `开发者资源/API/知识库 API/Agent 知识库/文档与分段/获取文档.md` | 获取文档 | 返回一个文档，包括其状态、自定义元数据、`row_version`、生效的修订版本和最近一次索引任务。；API, Agent 知识库, get-document, 开发者资源, 文档与分段, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/documents-and-chunks/get-document>) |
| `开发者资源/API/知识库 API/Agent 知识库/文档与分段/获取文档修订版本列表.md` | 获取文档修订版本列表 | 列出文档的修订版本，最新的在前。接收的是 [获取文档列表](/zh/api-reference/documents-and-chunks/list-documents) 返回的文档 ID，而不是文档文件 ID。；API, Agent 知识库, list-document-revisions, 开发者资源, 文档与分段, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/documents-and-chunks/list-document-revisions>) |
| `开发者资源/API/知识库 API/Agent 知识库/文档与分段/获取文档列表.md` | 获取文档列表 | 列出知识库中的文档，最早的在前，包括每个文档的状态、自定义元数据、生效的修订版本和最近一次索引任务。；API, Agent 知识库, list-documents, 开发者资源, 文档与分段, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/documents-and-chunks/list-documents>) |
| `开发者资源/API/知识库 API/Agent 知识库/文档与分段/获取文档大纲.md` | 获取文档大纲 | 返回为文档文件当前版本构建的标题树。；API, Agent 知识库, get-document-outline, 开发者资源, 文档与分段, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/documents-and-chunks/get-document-outline>) |
| `开发者资源/API/知识库 API/Agent 知识库/文档与分段/获取文档文件.md` | 获取文档文件 | 返回一个文档文件，即文档背后存储的文件，包括其 `version` 和 `parser_status`。；API, Agent 知识库, get-document-file, 开发者资源, 文档与分段, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/documents-and-chunks/get-document-file>) |
| `开发者资源/API/知识库 API/Agent 知识库/文档与分段/获取文档文件列表.md` | 获取文档文件列表 | 列出知识库中存储的文档文件。返回的是文档文件 ID，而非文档 ID。如需列出文档，使用 [获取文档列表](/zh/api-reference/documents-and-chunks/list-documents)。；API, Agent 知识库, list-document-files, 开发者资源, 文档与分段, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/documents-and-chunks/list-document-files>) |
| `开发者资源/API/知识库 API/Agent 知识库/文档与分段/重新索引文档.md` | 重新索引文档 | 为每个选中的文档排入一个索引任务，根据其当前文件重建索引。返回一个批量任务 ID，用于统一跟踪这些任务。；API, Agent 知识库, re-index-documents, 开发者资源, 文档与分段, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/documents-and-chunks/re-index-documents>) |
| `开发者资源/API/知识库 API/Agent 知识库/查询/创建查询令牌.md` | 创建查询令牌 | 为 [运行查询](/zh/api-reference/queries/run-query) 签发查询令牌，并返回需随令牌一起发送的请求体。详见 [查询知识库](/zh/api-reference/guides/knowledge-base#query-the-knowledge-base)。；API, Agent 知识库, create-query-token, 开发者资源, 查询, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/queries/create-query-token>) |
| `开发者资源/API/知识库 API/Agent 知识库/查询/运行查询.md` | 运行查询 | 运行已通过 [创建查询令牌](/zh/api-reference/queries/create-query-token) 获取令牌的查询，并以 Server-Sent Events 流式返回回答。此接口以查询令牌作为凭据，不使用知识库 API 密钥。服务端在受理请求时校验令牌。；API, Agent 知识库, run-query, 开发者资源, 查询, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/queries/run-query>) |
| `开发者资源/API/知识库 API/Agent 知识库/查询记录/获取查询冲突列表.md` | 获取查询冲突列表 | 列出一次查询运行所检索分段上记录的全部冲突，每个冲突一条。；API, Agent 知识库, list-query-conflicts, 开发者资源, 查询记录, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/query-records/list-query-conflicts>) |
| `开发者资源/API/知识库 API/Agent 知识库/查询记录/获取查询分段列表.md` | 获取查询分段列表 | 列出一次查询运行检索到的分段，每个分段一条，包含其主引用、分数、时效性和文本。；API, Agent 知识库, list-query-chunks, 开发者资源, 查询记录, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/query-records/list-query-chunks>) |
| `开发者资源/API/知识库 API/Agent 知识库/查询记录/获取查询记录.md` | 获取查询记录 | 返回一条完整的查询记录：查询内容、检索深度、调用方，以及按执行顺序排列的流水线步骤及其元数据。`query.generate` 步骤的元数据内嵌了所有检索分段，因此响应可能较大（最大 2 MiB）。；API, Agent 知识库, get-query-record, 开发者资源, 查询记录, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/query-records/get-query-record>) |
| `开发者资源/API/知识库 API/Agent 知识库/查询记录/获取查询记录列表.md` | 获取查询记录列表 | 列出知识库的查询记录，最新的在前。每次调用 [运行查询](/zh/api-reference/queries/run-query)，流一建立就会保存一条记录，之后失败的运行也不例外；但客户端断开连接，或运行以 `RETRIEVAL_EXECUTION_LEASE_LOST` 失败时，不保存记录。；API, Agent 知识库, list-query-records, 开发者资源, 查询记录, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/query-records/list-query-records>) |
| `开发者资源/API/知识库 API/Agent 知识库/查询记录/获取缺失分段列表.md` | 获取缺失分段列表 | 列出一次查询运行预期使用但未能使用的分段，每个分段一条。`data` 为空且 `truncated: false` 表示本次运行没有记录此类分段。；API, Agent 知识库, list-missing-chunks, 开发者资源, 查询记录, 知识库 API | [原文](<https://docs.dify.ai/zh/api-reference/query-records/list-missing-chunks>) |
| `开发者资源/API/知识库 API/Agent 知识库/研究任务/创建研究任务.md` | 创建研究任务 | 为一个问题创建研究任务，返回的任务 `stage` 为 `queued`，随后在后台运行。规划、创建、轮询和读取结果的完整流程，详见 [运行研究任务](/zh/api-reference/guides/knowledge-base#run-a-research-task)。；API, Agent 知识库, create-research-task, 开发者资源, 知识库 API, 研究任务 | [原文](<https://docs.dify.ai/zh/api-reference/research-tasks/create-research-task>) |
| `开发者资源/API/知识库 API/Agent 知识库/研究任务/取消研究任务.md` | 取消研究任务 | 取消尚未结束的研究任务，返回的任务 `stage` 为 `canceled`。；API, Agent 知识库, cancel-research-task, 开发者资源, 知识库 API, 研究任务 | [原文](<https://docs.dify.ai/zh/api-reference/research-tasks/cancel-research-task>) |
| `开发者资源/API/知识库 API/Agent 知识库/研究任务/获取研究任务.md` | 获取研究任务 | 返回研究任务的当前状态：`stage`、目前为止的花费、限制、时间戳，以及失败时的错误详情。；API, Agent 知识库, get-research-task, 开发者资源, 知识库 API, 研究任务 | [原文](<https://docs.dify.ai/zh/api-reference/research-tasks/get-research-task>) |
| `开发者资源/API/知识库 API/Agent 知识库/研究任务/获取研究任务列表.md` | 获取研究任务列表 | 列出知识库中归属于当前 API 密钥的研究任务，最新的在前。；API, Agent 知识库, list-research-tasks, 开发者资源, 知识库 API, 研究任务 | [原文](<https://docs.dify.ai/zh/api-reference/research-tasks/list-research-tasks>) |
| `开发者资源/API/知识库 API/Agent 知识库/研究任务/获取研究任务结果列表.md` | 获取研究任务结果列表 | 列出研究任务目前已写入的结果，按 `sequence` 升序排列。；API, Agent 知识库, list-research-task-results, 开发者资源, 知识库 API, 研究任务 | [原文](<https://docs.dify.ai/zh/api-reference/research-tasks/list-research-task-results>) |
| `开发者资源/API/知识库 API/Agent 知识库/研究任务/规划研究任务.md` | 规划研究任务 | 估算研究任务，但不创建任务。返回实际采用的检索深度，以及成本、延迟和工作量的估算，包括是否在拟定的预算之内。；API, Agent 知识库, plan-research-task, 开发者资源, 知识库 API, 研究任务 | [原文](<https://docs.dify.ai/zh/api-reference/research-tasks/plan-research-task>) |
| `开发者资源/API/知识库 API/Agent 知识库/索引任务/取消索引任务.md` | 取消索引任务 | 请求取消一个索引任务，并返回更新后的任务。；API, Agent 知识库, cancel-indexing-task, 开发者资源, 知识库 API, 索引任务 | [原文](<https://docs.dify.ai/zh/api-reference/indexing-tasks/cancel-indexing-task>) |
| `开发者资源/API/知识库 API/Agent 知识库/索引任务/获取后台任务列表.md` | 获取后台任务列表 | 在同一个列表中汇总知识库的后台工作，或按 ID 查找指定任务：；API, Agent 知识库, list-background-tasks, 开发者资源, 知识库 API, 索引任务 | [原文](<https://docs.dify.ai/zh/api-reference/indexing-tasks/list-background-tasks>) |
| `开发者资源/API/知识库 API/Agent 知识库/索引任务/获取批量任务.md` | 获取批量任务 | 返回批量任务中各索引任务的进度。在此 API 中，批量任务来自 [重新索引文档](/zh/api-reference/documents-and-chunks/re-index-documents)，并且只有启动它的 API 密钥才能读取。；API, Agent 知识库, get-bulk-task, 开发者资源, 知识库 API, 索引任务 | [原文](<https://docs.dify.ai/zh/api-reference/indexing-tasks/get-bulk-task>) |
| `开发者资源/API/知识库 API/Agent 知识库/索引任务/获取文档的索引任务.md` | 获取文档的索引任务 | 返回文档的一个索引任务及其进度。轮询直到 `state` 为 `succeeded`、`failed`、`canceled` 或 `superseded`。；API, Agent 知识库, get-document-indexing-task, 开发者资源, 知识库 API, 索引任务 | [原文](<https://docs.dify.ai/zh/api-reference/indexing-tasks/get-document-indexing-task>) |
| `开发者资源/API/知识库 API/Agent 知识库/索引任务/获取文档的索引任务列表.md` | 获取文档的索引任务列表 | 列出文档因上传和同步产生的索引任务，最早的在前，每个任务都带有其结果。失败和已取消的任务也包括在内。；API, Agent 知识库, list-document-indexing-tasks, 开发者资源, 知识库 API, 索引任务 | [原文](<https://docs.dify.ai/zh/api-reference/indexing-tasks/list-document-indexing-tasks>) |
| `开发者资源/API/知识库 API/Agent 知识库/索引任务/获取索引任务.md` | 获取索引任务 | 返回一个索引任务的状态。索引任务负责把文档文件的某个版本变成生效的修订版本。；API, Agent 知识库, get-indexing-task, 开发者资源, 知识库 API, 索引任务 | [原文](<https://docs.dify.ai/zh/api-reference/indexing-tasks/get-indexing-task>) |
| `开发者资源/API/知识库 API/Agent 知识库/索引任务/重试索引任务.md` | 重试索引任务 | 以同一个任务 ID 重新启动 `run_state` 为 `failed` 或 `canceled` 的索引任务，并返回更新后的任务。之后用同一个 ID 轮询 [获取索引任务](/zh/api-reference/indexing-tasks/get-indexing-task)。；API, Agent 知识库, retry-indexing-task, 开发者资源, 知识库 API, 索引任务 | [原文](<https://docs.dify.ai/zh/api-reference/indexing-tasks/retry-indexing-task>) |
| `开发者资源/API/知识库 API/Agent 知识库/设置/更新知识库设置.md` | 更新知识库设置 | 更改知识库的嵌入模型或检索设置。在内容索引前后如何设置模型，详见 [更换模型或检索设置](/zh/api-reference/guides/knowledge-base#change-models-or-retrieval-settings)。；API, Agent 知识库, update-knowledge-base-settings, 开发者资源, 知识库 API, 设置 | [原文](<https://docs.dify.ai/zh/api-reference/settings/update-knowledge-base-settings>) |
| `开发者资源/API/知识库 API/Agent 知识库/设置/获取知识库设置.md` | 获取知识库设置 | 返回知识库的嵌入模型、检索设置、就绪状态，以及调用 [更新知识库设置](/zh/api-reference/settings/update-knowledge-base-settings) 时需要发送的 `revision`。；API, Agent 知识库, get-knowledge-base-settings, 开发者资源, 知识库 API, 设置 | [原文](<https://docs.dify.ai/zh/api-reference/settings/get-knowledge-base-settings>) |
| `开发者资源/API/知识库 API/Agent 知识库/设置/获取设置迁移.md` | 获取设置迁移 | 返回迁移的进度。该迁移由 [更新知识库设置](/zh/api-reference/settings/update-knowledge-base-settings) 在返回 `202` 时启动。轮询直到 `run_state` 为 `succeeded`、`failed` 或 `canceled`。；API, Agent 知识库, get-settings-migration, 开发者资源, 知识库 API, 设置 | [原文](<https://docs.dify.ai/zh/api-reference/settings/get-settings-migration>) |
| `开发者资源/API/知识库 API/经典知识库/元数据/创建元数据字段.md` | 创建元数据字段 | 为知识库创建自定义元数据字段，用于给文档标注结构化信息。；API, create-metadata-field, 元数据, 开发者资源, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/metadata/create-metadata-field>) |
| `开发者资源/API/知识库 API/经典知识库/元数据/删除元数据字段.md` | 删除元数据字段 | 永久删除自定义元数据字段。使用过该字段的文档将丢失其对应的值。；API, delete-metadata-field, 元数据, 开发者资源, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/metadata/delete-metadata-field>) |
| `开发者资源/API/知识库 API/经典知识库/元数据/批量更新文档元数据.md` | 批量更新文档元数据 | 在一次请求中批量更新多个文档的元数据值。；API, update-document-metadata-in-batch, 元数据, 开发者资源, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/metadata/update-document-metadata-in-batch>) |
| `开发者资源/API/知识库 API/经典知识库/元数据/更新元数据字段.md` | 更新元数据字段 | 重命名自定义元数据字段。；API, update-metadata-field, 元数据, 开发者资源, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/metadata/update-metadata-field>) |
| `开发者资源/API/知识库 API/经典知识库/元数据/更新内置元数据字段.md` | 更新内置元数据字段 | 启用或禁用知识库的内置元数据字段。；API, update-built-in-metadata-field, 元数据, 开发者资源, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/metadata/update-built-in-metadata-field>) |
| `开发者资源/API/知识库 API/经典知识库/元数据/获取元数据字段列表.md` | 获取元数据字段列表 | 返回知识库的所有元数据字段（包括自定义和内置字段），以及使用每个字段的文档数量。；API, list-metadata-fields, 元数据, 开发者资源, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/metadata/list-metadata-fields>) |
| `开发者资源/API/知识库 API/经典知识库/元数据/获取内置元数据字段.md` | 获取内置元数据字段 | 返回系统提供的内置元数据字段。；API, get-built-in-metadata-fields, 元数据, 开发者资源, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/metadata/get-built-in-metadata-fields>) |
| `开发者资源/API/知识库 API/经典知识库/分段/从文档获取分段.md` | 从文档获取分段 | 返回文档内分段的分页列表，可按关键词或索引状态筛选。；API, list-chunks, 分段, 开发者资源, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/chunks/list-chunks>) |
| `开发者资源/API/知识库 API/经典知识库/分段/创建子分段.md` | 创建子分段 | 在父分段下创建子分段。适用于使用父子（`hierarchical_model`）分块模式的文档。；API, create-child-chunk, 分段, 开发者资源, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/chunks/create-child-chunk>) |
| `开发者资源/API/知识库 API/经典知识库/分段/删除子分段.md` | 删除子分段 | 从父分段中永久删除一个子分段。；API, delete-child-chunk, 分段, 开发者资源, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/chunks/delete-child-chunk>) |
| `开发者资源/API/知识库 API/经典知识库/分段/删除文档中的分段.md` | 删除文档中的分段 | 从文档中永久删除一个分段。；API, delete-chunk, 分段, 开发者资源, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/chunks/delete-chunk>) |
| `开发者资源/API/知识库 API/经典知识库/分段/向文档添加分段.md` | 向文档添加分段 | 在文档中创建一个或多个分段。；API, create-chunks, 分段, 开发者资源, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/chunks/create-chunks>) |
| `开发者资源/API/知识库 API/经典知识库/分段/更新子分段.md` | 更新子分段 | 更新现有子分段的内容。；API, update-child-chunk, 分段, 开发者资源, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/chunks/update-child-chunk>) |
| `开发者资源/API/知识库 API/经典知识库/分段/更新文档中的分段.md` | 更新文档中的分段 | 更新分段的字段。更新会为该分段重新触发索引。；API, update-chunk, 分段, 开发者资源, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/chunks/update-chunk>) |
| `开发者资源/API/知识库 API/经典知识库/分段/获取子分段.md` | 获取子分段 | 返回特定父分段下子分段的分页列表。；API, list-child-chunks, 分段, 开发者资源, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/chunks/list-child-chunks>) |
| `开发者资源/API/知识库 API/经典知识库/分段/获取文档中的分段详情.md` | 获取文档中的分段详情 | 获取单个分段的完整详情。；API, get-chunk, 分段, 开发者资源, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/chunks/get-chunk>) |
| `开发者资源/API/知识库 API/经典知识库/文档/下载文档.md` | 下载文档 | 返回用于下载文档原始上传文件的签名 URL。；API, download-document, 开发者资源, 文档, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/documents/download-document>) |
| `开发者资源/API/知识库 API/经典知识库/文档/从文件创建文档.md` | 从文件创建文档 | 在知识库中通过上传文件创建文档。支持 PDF、TXT、DOCX 等常见格式。索引异步进行；使用返回的 `batch` ID 通过 [获取文档嵌入状态（进度）](/zh/api-reference/documents/get-document-indexing-status) 跟踪。；API, create-document-by-file, 开发者资源, 文档, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/documents/create-document-by-file>) |
| `开发者资源/API/知识库 API/经典知识库/文档/从文本创建文档.md` | 从文本创建文档 | 在知识库中通过纯文本创建文档。索引异步进行；使用返回的 `batch` ID 通过 [获取文档嵌入状态（进度）](/zh/api-reference/documents/get-document-indexing-status) 跟踪。；API, create-document-by-text, 开发者资源, 文档, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/documents/create-document-by-text>) |
| `开发者资源/API/知识库 API/经典知识库/文档/删除文档.md` | 删除文档 | 从知识库中永久删除文档及其所有分段。；API, delete-document, 开发者资源, 文档, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/documents/delete-document>) |
| `开发者资源/API/知识库 API/经典知识库/文档/批量下载文档（ZIP）.md` | 批量下载文档（ZIP） | 将一个或多个文档下载为单个 ZIP 压缩包。仅可包含以文件形式上传的文档。；API, download-documents-as-zip, 开发者资源, 文档, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/documents/download-documents-as-zip>) |
| `开发者资源/API/知识库 API/经典知识库/文档/批量更新文档状态.md` | 批量更新文档状态 | 在一次请求中批量启用、禁用、归档或取消归档多个文档。；API, update-document-status-in-batch, 开发者资源, 文档, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/documents/update-document-status-in-batch>) |
| `开发者资源/API/知识库 API/经典知识库/文档/更新文档.md` | 更新文档 | 通过上传新文件更新文档，然后重新索引。这是基于文件更新文档的规范端点。使用返回的 `batch` ID 通过 [获取文档嵌入状态（进度）](/zh/api-reference/documents/get-document-indexing-status) 跟踪进度。；API, update-document, 开发者资源, 文档, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/documents/update-document>) |
| `开发者资源/API/知识库 API/经典知识库/文档/用文件更新文档.md` | 用文件更新文档 | 已弃用。改用 [更新文档](/zh/api-reference/documents/update-document)。通过上传新文件更新文档，然后重新索引。；API, update-document-by-file, 开发者资源, 文档, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/documents/update-document-by-file>) |
| `开发者资源/API/知识库 API/经典知识库/文档/用文本更新文档.md` | 用文本更新文档 | 更新文档的文本内容、名称或处理配置。文本变更时会重新索引文档。；API, update-document-by-text, 开发者资源, 文档, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/documents/update-document-by-text>) |
| `开发者资源/API/知识库 API/经典知识库/文档/获取文档嵌入状态（进度）.md` | 获取文档嵌入状态（进度） | 返回批次中每个文档的索引进度：当前阶段和分段完成计数。轮询直到每个 `indexing_status` 变为 `completed` 或 `error`。状态按 `waiting` → `parsing` → `cleaning` → `splitting` → `indexing` → `completed` 推进。；API, get-document-indexing-status, 开发者资源, 文档, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/documents/get-document-indexing-status>) |
| `开发者资源/API/知识库 API/经典知识库/文档/获取文档详情.md` | 获取文档详情 | 返回单个文档的详细信息。；API, get-document, 开发者资源, 文档, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/documents/get-document>) |
| `开发者资源/API/知识库 API/经典知识库/文档/获取知识库的文档列表.md` | 获取知识库的文档列表 | 返回知识库中文档的分页列表。；API, list-documents, 开发者资源, 文档, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/documents/list-documents>) |
| `开发者资源/API/知识库 API/经典知识库/标签/修改知识库标签.md` | 修改知识库标签 | 重命名知识库标签。；API, update-knowledge-tag, 开发者资源, 标签, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/tags/update-knowledge-tag>) |
| `开发者资源/API/知识库 API/经典知识库/标签/创建知识库标签.md` | 创建知识库标签 | 创建用于组织知识库的标签。；API, create-knowledge-tag, 开发者资源, 标签, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/tags/create-knowledge-tag>) |
| `开发者资源/API/知识库 API/经典知识库/标签/删除知识库标签.md` | 删除知识库标签 | 永久删除知识库标签。不会删除已被标记的知识库。；API, delete-knowledge-tag, 开发者资源, 标签, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/tags/delete-knowledge-tag>) |
| `开发者资源/API/知识库 API/经典知识库/标签/绑定标签到知识库.md` | 绑定标签到知识库 | 将一个或多个标签绑定到知识库。一个知识库可以有多个标签。；API, create-tag-binding, 开发者资源, 标签, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/tags/create-tag-binding>) |
| `开发者资源/API/知识库 API/经典知识库/标签/获取知识库标签列表.md` | 获取知识库标签列表 | 返回工作空间中所有的知识库标签。；API, list-knowledge-tags, 开发者资源, 标签, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/tags/list-knowledge-tags>) |
| `开发者资源/API/知识库 API/经典知识库/标签/获取知识库绑定的标签.md` | 获取知识库绑定的标签 | 返回绑定到知识库的标签。；API, get-knowledge-base-tags, 开发者资源, 标签, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/tags/get-knowledge-base-tags>) |
| `开发者资源/API/知识库 API/经典知识库/标签/解除标签与知识库的绑定.md` | 解除标签与知识库的绑定 | 从知识库中移除一个或多个标签。；API, delete-tag-binding, 开发者资源, 标签, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/tags/delete-tag-binding>) |
| `开发者资源/API/知识库 API/经典知识库/模型/获取可用模型.md` | 获取可用模型 | 返回指定类型的可用模型。用它查找可配置到知识库的 `text-embedding` 和 `rerank` 模型。；API, get-available-models, 开发者资源, 模型, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/models/get-available-models>) |
| `开发者资源/API/知识库 API/经典知识库/知识库/从知识库检索分段 测试检索.md` | 从知识库检索分段 / 测试检索 | 搜索知识库，返回与查询最相关的分段，可用于生产环境检索和测试检索。；API, retrieve-chunks-from-a-knowledge-base-test-retrieval, 开发者资源, 知识库, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/knowledge-bases/retrieve-chunks-from-a-knowledge-base-test-retrieval>) |
| `开发者资源/API/知识库 API/经典知识库/知识库/创建空知识库.md` | 创建空知识库 | 创建一个空知识库。之后用 [从文本创建文档](/zh/api-reference/documents/create-document-by-text) 或 [从文件创建文档](/zh/api-reference/documents/create-document-by-file) 向其中添加文档。；API, create-an-empty-knowledge-base, 开发者资源, 知识库, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/knowledge-bases/create-an-empty-knowledge-base>) |
| `开发者资源/API/知识库 API/经典知识库/知识库/删除知识库.md` | 删除知识库 | 永久删除知识库、其中的所有文档，以及只绑定了该知识库的 API 密钥。同时绑定了其他知识库的密钥仍可继续访问那些知识库。；API, delete-knowledge-base, 开发者资源, 知识库, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/knowledge-bases/delete-knowledge-base>) |
| `开发者资源/API/知识库 API/经典知识库/知识库/更新知识库.md` | 更新知识库 | 更新知识库。仅更改请求体中包含的字段。；API, update-knowledge-base, 开发者资源, 知识库, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/knowledge-bases/update-knowledge-base>) |
| `开发者资源/API/知识库 API/经典知识库/知识库/获取知识库列表.md` | 获取知识库列表 | 返回工作空间中知识库的分页列表，不按知识库的权限设置过滤，可按关键词或标签筛选。；API, list-knowledge-bases, 开发者资源, 知识库, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/knowledge-bases/list-knowledge-bases>) |
| `开发者资源/API/知识库 API/经典知识库/知识库/获取知识库详情.md` | 获取知识库详情 | 返回知识库的详细信息，包括嵌入模型、检索配置和文档统计信息。；API, get-knowledge-base, 开发者资源, 知识库, 知识库 API, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/knowledge-bases/get-knowledge-base>) |
| `开发者资源/API/知识库 API/经典知识库/知识流水线/上传流水线文件.md` | 上传流水线文件 | 上传文件以在知识流水线中使用。将返回的 `id` 用作 [运行流水线](/zh/api-reference/knowledge-pipeline/run-pipeline) 中 `local_file` 项的 `reference`。；API, upload-pipeline-file, 开发者资源, 知识库 API, 知识流水线, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/knowledge-pipeline/upload-pipeline-file>) |
| `开发者资源/API/知识库 API/经典知识库/知识流水线/执行数据源节点.md` | 执行数据源节点 | 运行知识流水线中的单个数据源节点，并流式返回其执行事件。；API, run-datasource-node, 开发者资源, 知识库 API, 知识流水线, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/knowledge-pipeline/run-datasource-node>) |
| `开发者资源/API/知识库 API/经典知识库/知识流水线/获取数据源插件列表.md` | 获取数据源插件列表 | 返回知识流水线中已配置的数据源节点，每个节点包含其使用的插件，以及运行该节点所需的元数据。；API, list-datasource-plugins, 开发者资源, 知识库 API, 知识流水线, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/knowledge-pipeline/list-datasource-plugins>) |
| `开发者资源/API/知识库 API/经典知识库/知识流水线/运行流水线.md` | 运行流水线 | 对一个或多个数据源运行完整的知识流水线。`response_mode` 选择流式或阻塞响应。；API, run-pipeline, 开发者资源, 知识库 API, 知识流水线, 经典知识库 | [原文](<https://docs.dify.ai/zh/api-reference/knowledge-pipeline/run-pipeline>) |
| `开发者资源/CLI/参考/命令索引.md` | 命令索引 | 按用途分组列出 difyctl 命令，说明每条命令的作用和使用条件；CLI, command-index, 参考, 开发者资源 | [原文](<https://docs.dify.ai/zh/cli/reference/command-index>) |
| `开发者资源/CLI/参考/结果、错误与退出码.md` | 结果、错误与退出码 | 看懂 difyctl 命令输出的内容，判断一次运行是怎样结束的，并处理错误、退出码、重试与限流；CLI, results-errors-and-exit-codes, 参考, 开发者资源 | [原文](<https://docs.dify.ai/zh/cli/reference/results-errors-and-exit-codes>) |
| `开发者资源/CLI/参考/配置.md` | 配置 | 调整 difyctl 的安装方式，设置它读取的环境变量，修改超时时长，并查看它保存的文件；CLI, configuration, 参考, 开发者资源 | [原文](<https://docs.dify.ai/zh/cli/reference/configuration>) |
| `开发者资源/CLI/应用操作/在 CI 和自动化中使用 \`difyctl\`.md` | 在 CI 和自动化中使用 `difyctl` | 在 CI 任务中安装 difyctl、配置登录，并让任务在该停下时停下，另附合并时更新应用的示例；CLI, scripts-and-ci, 应用操作, 开发者资源 | [原文](<https://docs.dify.ai/zh/cli/scripts-and-ci>) |
| `开发者资源/CLI/应用操作/构建应用.md` | 构建应用 | 让编码 Agent 构建、修改、测试并发布你的 Workflow 和 Chatflow 应用；CLI, build-apps, 应用操作, 开发者资源 | [原文](<https://docs.dify.ai/zh/cli/build-apps>) |
| `开发者资源/CLI/应用操作/运行应用.md` | 运行应用 | 用 difyctl 运行 Dify 应用，传入变量和文件，流式查看或停止耗时较长的运行，填写人工介入表单，并排查运行失败的原因；CLI, run-apps, 应用操作, 开发者资源 | [原文](<https://docs.dify.ai/zh/cli/run-apps>) |
| `开发者资源/CLI/应用操作/通过 DSL 文件创建和更新应用.md` | 通过 DSL 文件创建和更新应用 | 用 difyctl 通过 DSL 文件更新 Dify 应用，再发布或回滚，从文件或应用包创建应用，并修改 Web 应用设置；CLI, create-and-update-apps-from-dsl-files, 应用操作, 开发者资源 | [原文](<https://docs.dify.ai/zh/cli/create-and-update-apps-from-dsl-files>) |
| `开发者资源/CLI/快速开始.md` | 快速开始 | 安装 difyctl 并登录，用 difyctl Skill 配置编码 Agent，再查找你自己要运行的命令；CLI, get-started, 开发者资源 | [原文](<https://docs.dify.ai/zh/cli/get-started>) |
| `开发者资源/CLI/查找并运行命令.md` | 查找并运行命令 | 找到完成某项任务的 difyctl 命令，用标志或 JSON 传值，再按结果中的建议运行后续步骤；CLI, find-and-run-commands, 开发者资源 | [原文](<https://docs.dify.ai/zh/cli/find-and-run-commands>) |
| `开发者资源/CLI/概述.md` | 概述 | 你和编码 Agent 都能用 difyctl 在终端中操作 Dify 应用；CLI, overview, 开发者资源 | [原文](<https://docs.dify.ai/zh/cli/overview>) |
| `开发者资源/CLI/管理 difyctl/Dify 1.18.0 升级指南.md` | Dify 1.18.0 升级指南 | Dify 服务器从 1.17.x 或更早版本升级到 1.18.0 或更高版本时，重新登录、清理旧版残留，并逐一更新命令、脚本和编码 Agent；CLI, upgrade-across-1-18, 开发者资源, 管理 difyctl | [原文](<https://docs.dify.ai/zh/cli/upgrade-across-1-18>) |
| `开发者资源/CLI/管理 difyctl/更新或卸载 difyctl.md` | 更新或卸载 difyctl | Dify 服务器升级到新版本时更新 difyctl，或从机器上卸载 difyctl；CLI, update-or-uninstall, 开发者资源, 管理 difyctl | [原文](<https://docs.dify.ai/zh/cli/update-or-uninstall>) |
| `开发者资源/CLI/管理 difyctl/管理登录.md` | 管理登录 | 续期过期的登录，使用多个服务器或账户，切换工作空间，查看令牌的存储位置，并结束不再使用的会话；CLI, manage-sign-in, 开发者资源, 管理 difyctl | [原文](<https://docs.dify.ai/zh/cli/manage-sign-in>) |
| `开发者资源/插件开发/发布/GitHub 仓库/发布到个人 GitHub 仓库.md` | 发布到个人 GitHub 仓库 | 从自己的 GitHub 仓库分发 Dify 插件，用户通过仓库 URL 直接安装，无需 Marketplace 审核；GitHub 仓库, release-to-individual-github-repo, 发布, 开发者资源, 插件开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/publishing/marketplace-listing/release-to-individual-github-repo>) |
| `开发者资源/插件开发/发布/发布插件.md` | 发布插件 | 分发 Dify 插件的三种方式（Marketplace、GitHub 仓库或本地文件）以及如何选择合适的方式；release-overview, 发布, 开发者资源, 插件开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/publishing/marketplace-listing/release-overview>) |
| `开发者资源/插件开发/发布/发布插件到 Marketplace.md` | 发布插件到 Marketplace | 准备并验证 .difypkg，提交 Marketplace 审核，处理 Pull Request，并在创作者中心查看已发布插件的表现和反馈；submit-plugin-to-marketplace, 发布, 开发者资源, 插件开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/publishing/marketplace-listing/submit-plugin-to-marketplace>) |
| `开发者资源/插件开发/发布/常见问题.md` | 常见问题 | 构建、打包、调试和安装 Dify 插件时的常见问题与解决方法；faq, 发布, 开发者资源, 插件开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/publishing/faq/faq>) |
| `开发者资源/插件开发/发布/本地文件/为第三方签名验证签署插件.md` | 为第三方签名验证签署插件 | 在 Dify Community Edition 中启用已签名的 `.difypkg` 安装，无需完全禁用签名验证（生成密钥、签署软件包、分发公钥）；third-party-signature-verification, 发布, 开发者资源, 插件开发, 本地文件 | [原文](<https://docs.dify.ai/zh/develop-plugin/publishing/standards/third-party-signature-verification>) |
| `开发者资源/插件开发/发布/本地文件/打包为本地文件并分享.md` | 打包为本地文件并分享 | 将 Dify 插件打包为 `.difypkg` 文件，可直接安装或分发给他人，无需发布到 Marketplace 或 GitHub；release-by-file, 发布, 开发者资源, 插件开发, 本地文件 | [原文](<https://docs.dify.ai/zh/develop-plugin/publishing/marketplace-listing/release-by-file>) |
| `开发者资源/插件开发/发布/标准/插件开发指南.md` | 插件开发指南 | 为了确保 Dify Marketplace 中所有插件的质量，并为 Dify Marketplace 用户提供一致的高质量体验，您在提交插件进行审核时必须遵守这些插件开发指南中列出的所有要求。提交插件即表示**您确认已阅读、理解并同意遵守以下所有条款**。遵循这些指南将帮助您的插件更快通过审核。；contributor-covenant-code-of-conduct, 发布, 开发者资源, 插件开发, 标准 | [原文](<https://docs.dify.ai/zh/develop-plugin/publishing/standards/contributor-covenant-code-of-conduct>) |
| `开发者资源/插件开发/发布/标准/隐私政策指南.md` | 隐私政策指南 | 如何声明数据收集行为，并为提交到 Dify Marketplace 的每个插件编写所需的隐私政策；privacy-protection-guidelines, 发布, 开发者资源, 插件开发, 标准 | [原文](<https://docs.dify.ai/zh/develop-plugin/publishing/standards/privacy-protection-guidelines>) |
| `开发者资源/插件开发/开发指南与示例/完整示例/Flomo 工具（10分钟）.md` | Flomo 工具（10分钟） | 在大约十分钟内端到端构建一个连接 Flomo 笔记服务的功能性 Dify 工具插件；develop-flomo-plugin, 完整示例, 开发指南与示例, 开发者资源, 插件开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/dev-guides-and-walkthroughs/develop-flomo-plugin>) |
| `开发者资源/插件开发/开发指南与示例/完整示例/Markdown 导出器.md` | Markdown 导出器 | 学习如何创建一个将对话导出为不同文档格式的插件；develop-md-exporter, 完整示例, 开发指南与示例, 开发者资源, 插件开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/dev-guides-and-walkthroughs/develop-md-exporter>) |
| `开发者资源/插件开发/开发指南与示例/完整示例/Slack Bot.md` | Slack Bot | 构建一个将 Dify 应用连接到 Slack 的 Slack Bot 插件，涵盖从项目初始化到调试和打包的完整流程；develop-a-slack-bot-plugin, 完整示例, 开发指南与示例, 开发者资源, 插件开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/dev-guides-and-walkthroughs/develop-a-slack-bot-plugin>) |
| `开发者资源/插件开发/开发指南与示例/完整示例/多模态工具.md` | 多模态工具 | 配置工具插件以输出图片、音频或视频，使知识库节点能够将多模态输出与文本一同向量化；develop-multimodal-data-processing-tool, 完整示例, 开发指南与示例, 开发者资源, 插件开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/dev-guides-and-walkthroughs/develop-multimodal-data-processing-tool>) |
| `开发者资源/插件开发/开发指南与示例/按插件类型/Agent 策略插件.md` | Agent 策略插件 | 从零开始构建一个 Function Calling Agent 策略，通过实战示例展示如何为 LLM 提供工具并让其自主获取当前时间；agent-strategy-plugin, 开发指南与示例, 开发者资源, 按插件类型, 插件开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/dev-guides-and-walkthroughs/agent-strategy-plugin>) |
| `开发者资源/插件开发/开发指南与示例/按插件类型/Endpoint 插件.md` | Endpoint 插件 | 以 Neko Cat 项目为例，定义、配置并实现 Dify 插件中的 HTTP Endpoint；endpoint, 开发指南与示例, 开发者资源, 按插件类型, 插件开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/dev-guides-and-walkthroughs/endpoint>) |
| `开发者资源/插件开发/开发指南与示例/按插件类型/Tool OAuth.md` | Tool OAuth | 用 OAuth 授权流程替代手动输入 API 密钥，让用户一键授权访问第三方服务；tool-oauth, 开发指南与示例, 开发者资源, 按插件类型, 插件开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/dev-guides-and-walkthroughs/tool-oauth>) |
| `开发者资源/插件开发/开发指南与示例/按插件类型/工具插件.md` | 工具插件 | 从初始化到打包，以 Google Search 为示例完整开发一个 Dify 工具插件；tool-plugin, 开发指南与示例, 开发者资源, 按插件类型, 插件开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/dev-guides-and-walkthroughs/tool-plugin>) |
| `开发者资源/插件开发/开发指南与示例/按插件类型/数据源插件.md` | 数据源插件 | 构建 Dify 1.9.0+ 数据源插件，将文档输入知识库管道；datasource-plugin, 开发指南与示例, 开发者资源, 按插件类型, 插件开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/dev-guides-and-walkthroughs/datasource-plugin>) |
| `开发者资源/插件开发/开发指南与示例/按插件类型/模型供应商插件.md` | 模型供应商插件 | 构建模型供应商插件，从项目搭建、供应商配置到模型实现、调试与发布。；creating-new-model-provider, 开发指南与示例, 开发者资源, 按插件类型, 插件开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/dev-guides-and-walkthroughs/creating-new-model-provider>) |
| `开发者资源/插件开发/开发指南与示例/按插件类型/触发器插件.md` | 触发器插件 | 构建 Dify 1.10.0+ 触发器插件，将第三方 webhook 事件转换为工作流启动信号；trigger-plugin, 开发指南与示例, 开发者资源, 按插件类型, 插件开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/dev-guides-and-walkthroughs/trigger-plugin>) |
| `开发者资源/插件开发/开发指南与示例/速查表.md` | 速查表 | Dify 插件开发的快速参考，涵盖环境配置、安装、开发流程和插件类型；cheatsheet, 开发指南与示例, 开发者资源, 插件开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/dev-guides-and-walkthroughs/cheatsheet>) |
| `开发者资源/插件开发/快速开始/Dify 插件 CLI.md` | Dify 插件 CLI | 安装 Dify 插件 CLI、搭建新插件项目，并在本地开发时将其连接到 Dify 实例运行；cli, 开发者资源, 快速开始, 插件开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/getting-started/cli>) |
| `开发者资源/插件开发/快速开始/Dify 插件.md` | Dify 插件 | 模块化组件，通过外部服务、自定义逻辑和专业工具扩展 Dify AI 应用；getting-started-dify-plugin, 开发者资源, 快速开始, 插件开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/getting-started/getting-started-dify-plugin>) |
| `开发者资源/插件开发/快速开始/选择插件类型.md` | 选择插件类型 | 一份简明的决策指南，帮助你在工具、模型、Agent 策略、扩展、数据源和触发器插件之间做出选择；choose-plugin-type, 开发者资源, 快速开始, 插件开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/getting-started/choose-plugin-type>) |
| `开发者资源/插件开发/特性与规范/插件类型/Manifest.md` | Manifest | 插件 manifest 的 YAML schema，用于声明名称、作者、运行时、资源、权限，以及插件附带的工具、模型和端点；plugin-info-by-manifest, 开发者资源, 插件开发, 插件类型, 特性与规范 | [原文](<https://docs.dify.ai/zh/develop-plugin/features-and-specs/plugin-types/plugin-info-by-manifest>) |
| `开发者资源/插件开发/特性与规范/插件类型/多语言 README.md` | 多语言 README | 添加各语言的 README 文件，让 Dify Marketplace 以用户的首选语言展示插件文档；multilingual-readme, 开发者资源, 插件开发, 插件类型, 特性与规范 | [原文](<https://docs.dify.ai/zh/develop-plugin/features-and-specs/plugin-types/multilingual-readme>) |
| `开发者资源/插件开发/特性与规范/插件类型/工具返回.md` | 工具返回 | 工具插件如何返回消息（文本、链接、图片、文件、JSON）、创建标准变量和流式变量，以及定义输出模式以供工作流引用；tool, 开发者资源, 插件开发, 插件类型, 特性与规范 | [原文](<https://docs.dify.ai/zh/develop-plugin/features-and-specs/plugin-types/tool>) |
| `开发者资源/插件开发/特性与规范/插件类型/持久化存储.md` | 持久化存储 | 使用内置的键值存储在插件的多次交互间保存数据；persistent-storage-kv, 开发者资源, 插件开发, 插件类型, 特性与规范 | [原文](<https://docs.dify.ai/zh/develop-plugin/features-and-specs/plugin-types/persistent-storage-kv>) |
| `开发者资源/插件开发/特性与规范/插件类型/插件调试.md` | 插件调试 | 在本地运行开发中的插件，并将其挂载到在线 Dify 工作空间进行端到端测试，无需打包；remote-debug-a-plugin, 开发者资源, 插件开发, 插件类型, 特性与规范 | [原文](<https://docs.dify.ai/zh/develop-plugin/features-and-specs/plugin-types/remote-debug-a-plugin>) |
| `开发者资源/插件开发/特性与规范/插件类型/模型 API 接口.md` | 模型 API 接口 | 实现 Dify 模型插件所需的接口和数据结构，涵盖 LLM、TextEmbedding、Rerank、Speech2Text、Text2Speech 和 Moderation 模型；model-schema, 开发者资源, 插件开发, 插件类型, 特性与规范 | [原文](<https://docs.dify.ai/zh/develop-plugin/features-and-specs/plugin-types/model-schema>) |
| `开发者资源/插件开发/特性与规范/插件类型/模型规范.md` | 模型规范 | Dify 模型插件相关实体的参考，包括 Provider、AIModelEntity、模型类型、配置方法、参数规则和凭据模式；model-designing-rules, 开发者资源, 插件开发, 插件类型, 特性与规范 | [原文](<https://docs.dify.ai/zh/develop-plugin/features-and-specs/plugin-types/model-designing-rules>) |
| `开发者资源/插件开发/特性与规范/插件类型/输出插件日志.md` | 输出插件日志 | 通过 SDK 的 plugin_logger_handler 输出插件日志，可在远程调试时查看，也会写入守护进程容器日志；plugin-logging, 开发者资源, 插件开发, 插件类型, 特性与规范 | [原文](<https://docs.dify.ai/zh/develop-plugin/features-and-specs/plugin-types/plugin-logging>) |
| `开发者资源/插件开发/特性与规范/插件类型/通用规范.md` | 通用规范 | 各类插件共享的通用数据结构，包括 I18nObject、ProviderConfig、ModelConfig、NodeResponse 和 ToolSelector；general-specifications, 开发者资源, 插件开发, 插件类型, 特性与规范 | [原文](<https://docs.dify.ai/zh/develop-plugin/features-and-specs/plugin-types/general-specifications>) |
| `开发者资源/插件开发/特性与规范/高级开发/反向调用/Bundle 插件包.md` | Bundle 插件包 | 将多个插件打包进一个 Bundle，支持 Marketplace、GitHub 和 Package 三种依赖类型；bundle, 反向调用, 开发者资源, 插件开发, 特性与规范, 高级开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/features-and-specs/advanced-development/bundle>) |
| `开发者资源/插件开发/特性与规范/高级开发/反向调用/Dify 服务的反向调用.md` | Dify 服务的反向调用 | 在插件中调用 Dify 平台的 App、Model、Tool 和 Node 服务；reverse-invocation, 反向调用, 开发者资源, 插件开发, 特性与规范, 高级开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/features-and-specs/advanced-development/reverse-invocation>) |
| `开发者资源/插件开发/特性与规范/高级开发/反向调用/反向调用模型.md` | 反向调用模型 | 在插件中调用 LLM、嵌入、重排序、TTS、语音转文字和内容审核模型；reverse-invocation-model, 反向调用, 开发者资源, 插件开发, 特性与规范, 高级开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/features-and-specs/advanced-development/reverse-invocation-model>) |
| `开发者资源/插件开发/特性与规范/高级开发/反向调用/工具.md` | 工具 | 从插件中调用已安装工具、Workflow as Tool 和自定义工具；reverse-invocation-tool, 反向调用, 开发者资源, 插件开发, 特性与规范, 高级开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/features-and-specs/advanced-development/reverse-invocation-tool>) |
| `开发者资源/插件开发/特性与规范/高级开发/反向调用/应用.md` | 应用 | 在插件中调用 Dify 应用的 Chat、Workflow 和 Completion 接口；reverse-invocation-app, 反向调用, 开发者资源, 插件开发, 特性与规范, 高级开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/features-and-specs/advanced-development/reverse-invocation-app>) |
| `开发者资源/插件开发/特性与规范/高级开发/反向调用/节点.md` | 节点 | 从插件中调用参数提取器和问题分类器节点；reverse-invocation-node, 反向调用, 开发者资源, 插件开发, 特性与规范, 高级开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/features-and-specs/advanced-development/reverse-invocation-node>) |
| `开发者资源/插件开发/特性与规范/高级开发/反向调用/集成自定义模型.md` | 集成自定义模型 | 以 Xinference 为例，将自定义模型集成到 Dify；customizable-model, 反向调用, 开发者资源, 插件开发, 特性与规范, 高级开发 | [原文](<https://docs.dify.ai/zh/develop-plugin/features-and-specs/advanced-development/customizable-model>) |
