# Dify 插件 CLI

> 安装 Dify 插件 CLI、搭建新插件项目，并在本地开发时将其连接到 Dify 实例运行

> 本文档由 AI 自动翻译。如有任何不准确之处，请参考 [英文原版](https://docs.dify.ai/en/develop-plugin/getting-started/cli.md)。

Dify 插件 CLI 负责管理插件开发的整个流程，从项目初始化到打包。本指南介绍如何安装 CLI、搭建插件项目，并将其连接到 Dify 实例运行。

> [!NOTE]
>
> 这是用于插件开发的 Dify 插件 CLI（`dify` 命令）。它与在命令行中运行、管理 Dify 应用的 Dify CLI（[difyctl](../../CLI/%E6%A6%82%E8%BF%B0.md)）不是同一个工具。

## 前提条件

开始之前，请确保具备：

* Python 3.12
* Homebrew（仅 macOS，用于安装 CLI）

## 安装 CLI

> [tab] Mac
>
> ```bash theme={null}
> brew tap langgenius/dify
> brew install dify
> ```

> [tab] Linux
>
> 从 [Dify Plugin Daemon 发布页面](https://github.com/langgenius/dify-plugin-daemon/releases) 下载最新的二进制文件。x86\_64 主机选择 `dify-plugin-linux-amd64`，ARM 主机选择 `dify-plugin-linux-arm64`。
>
> ```bash theme={null}
> chmod +x dify-plugin-linux-amd64
> sudo mv dify-plugin-linux-amd64 /usr/local/bin/dify
> ```

> [tab] Windows
>
> 从 [Dify Plugin Daemon 发布页面](https://github.com/langgenius/dify-plugin-daemon/releases) 下载 `dify-plugin-windows-amd64.exe`（或 `dify-plugin-windows-arm64.exe`），将其重命名为 `dify.exe`，并把所在文件夹加入 `PATH`。

验证安装：

```bash theme={null}
dify version
```

## 创建插件项目

使用以下命令创建新的插件项目：

```bash theme={null}
dify plugin init
```

根据提示填写必填字段：

```bash theme={null}
Edit profile of the plugin
Plugin name (press Enter to next step): hello-world
Author (press Enter to next step): langgenius
Description (press Enter to next step): hello world example
Repository URL (Optional) (press Enter to next step): Repository URL (Optional)
  Enable multilingual README: [✔] English is required by default

Languages to generate:
    English: [✔] (required)
  → 简体中文 (Simplified Chinese): [✔]
    日本語 (Japanese): [✘]
    Português (Portuguese - Brazil): [✘]

Controls:
  ↑/↓ Navigate • Space/Tab Toggle selection • Enter Next step
```

选择 `python` 并按 Enter 使用 Python 插件模板，然后选择要构建的插件类型：

```bash theme={null}
Select the type of plugin you want to create, and press `Enter` to continue
Before starting, here's some basic knowledge about Plugin types in Dify:

- Tool: Tool Providers like Google Search, Stable Diffusion, etc. Used to perform specific tasks.
- Model: Model Providers like OpenAI, Anthropic, etc. Use their models to enhance AI capabilities.
- Endpoint: Similar to Service API in Dify and Ingress in Kubernetes. Extend HTTP services as endpoints with custom logic.
- Trigger: Webhook-based providers that turn third-party platform events into workflow start signals.
- Agent Strategy: Implement your own agent strategies like Function Calling, ReAct, ToT, CoT, etc.

Based on the ability you want to extend, Plugins are divided into six types: Tool, Model, Extension, Agent Strategy, Datasource, and Trigger.

- Tool: A tool provider that can also implement endpoints. For example, building a Discord Bot requires both sending and receiving messages.
- Model: Strictly for model providers, no other extensions allowed.
- Extension: For simple HTTP services that extend functionality.
- Agent Strategy: Implement custom agent logic with a focused approach.
- Datasource: Provide datasource for Dify Knowledge Pipeline.
- Trigger: Build webhook integrations that emit events to kick off workflows.

We've provided templates to help you get started. Choose one of the options below:
-> tool
  agent-strategy
  llm
  text-embedding
  rerank
  tts
  speech2text
  moderation
  extension
  datasource
  trigger
```

提示输入最低 Dify 版本时，留空即可使用最新版本：

```bash theme={null}
Edit minimal Dify version requirement, leave it blank by default
Minimal Dify version (press Enter to next step):
```

CLI 会创建一个以插件名命名的新目录，并搭建基本项目结构。进入该目录：

```bash theme={null}
cd hello-world
```

## 运行插件

在 `hello-world` 目录下，复制示例环境文件：

```bash theme={null}
cp .env.example .env
```

编辑 `.env` 文件，设置插件的环境变量，例如 API 密钥或其他配置。要获取调试凭据，请登录 Dify 环境，点击右上角的 **插件**，再点击调试图标。在弹出窗口中，复制 **API Key** 和 **Host Address**。

```bash theme={null}
INSTALL_METHOD=remote
REMOTE_INSTALL_URL=debug-plugin.dify.dev:5003
REMOTE_INSTALL_KEY=********-****-****-****-************
```

> [!NOTE]
>
> `REMOTE_INSTALL_URL` 以 `host:port` 形式合并主机和端口。主机和端口一同显示在插件页面的 **API Key** 卡片中。

安装依赖并运行插件：

```bash theme={null}
pip install -r requirements.txt
python -m main
```
