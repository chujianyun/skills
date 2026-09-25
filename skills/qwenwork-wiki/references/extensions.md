# 技能、连接器与专家套件

资料核对：2026-09-16。桌面路径不适用于网页端。

## Skill 技能

桌面技能是包含 `SKILL.md` 的目录，默认放在 `~/.qwenworkcn/skills/`。可从技能广场、社区来源或本地文件安装。调用方式包括自动匹配、输入 `/` 选择或直接点名；`@` 用于添加文件等上下文，不能当作技能调用符。

制作可复用技能时把实际工作流程和输出要求写清；查询安装方法不代表授权执行陌生脚本。此 Wiki 默认安装于调用它的 Agent 技能目录，不自动复制到千问办公目录。

来源：[技能](https://qwenwork.cn/docs/features/skills)。

## 连接器 / MCP

连接器为工具和外部数据提供入口，安装后可能还需授权。桌面支持浏览器、macOS 应用、Microsoft 365、钉钉以及自定义 MCP。自定义服务可导入 `mcpServers` JSON 或填写表单；远程类型有 Streamable HTTP / SSE，本地 STDIO 需要相应运行时。

新增或切换连接器后，专页要求新建对话使工具生效。排障先检查配置格式、网络、认证和服务状态，不直接删掉重装。服务地址、协议和启动命令应由提供方给出，不从示例 URL 猜测。真实 Token 只进入安全配置。

来源：[连接器](https://qwenwork.cn/docs/features/connectors)。

## 专家套件 / Expert Kit

技能封装单项方法，套件组合技能、数据连接、命令与输出标准，适合团队分发。可让千问办公创建或上传 ZIP。文档接受 `.qwen-plugin/plugin.json` 或 `.claude-plugin/plugin.json`，其中需有 `name`。安装后可在新任务中用 `/` 选择；连接器授权仍需单独完成。

来源：[专家套件](https://qwenwork.cn/docs/desktop/expert-kits)。

## 网页端扩展入口

网页侧栏“扩展”可查找技能、套件和连接器；安装后按需从任务的资源入口选择。套件更新可能覆盖个人定制，更新前先保存需保留的内容。不要把安装成功等同于每条对话都会启用。

来源：[扩展说明](https://qwenwork.cn/docs/features/extensions)、[基础教程](https://qwenwork.cn/docs/getting-started/basic-workflow)。
