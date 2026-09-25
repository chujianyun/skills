# MCP 常见问题

本指南帮助你在安装和运行 Model Context Protocol（MCP）服务时诊断并解决常见问题。

## 无法添加或安装 MCP 服务

### 问题：缺少 NPX 运行环境

**错误消息：**
```
failed to start command: exec: "npx": executable file not found in $PATH
```

**原因：** `npx` 命令行工具未安装，或未在系统的 `PATH` 中可用。

**解决方案：** 安装 Node.js V18 或更高版本（内含 NPM V8 及以上）。

### 问题：缺少 UVX 环境

**错误消息：**
```
failed to start command: exec: "uvx": executable file not found in $PATH
```

**原因：** `uvx` 命令尚未安装。

**解决方案：** 安装 `uv`：
- Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### 问题：无法初始化 MCP 客户端

**错误信息：**
```
failed to initialize MCP client: context deadline exceeded
```

**可能原因：**
- MCP 服务参数配置不正确
- 网络问题导致资源无法下载
- 企业网络安全策略阻止初始化

**解决方案：**
1. 在 UI 中点击 **复制完整命令**
2. 在终端运行该命令以获取更详细的错误输出
3. 根据具体错误进行分析与处理

## 工具使用相关问题

### 问题：工具执行失败

**原因：** 某些 MCP 服务器（如 MasterGo、Figma）在设置时需要在参数中手动配置 `API_KEY` 或 `TOKEN`。

**解决方案：**
1. 进入 Qoder 设置 > MCP
2. 找到相关服务器并点击 **Edit**
3. 检查 **Arguments** 中的参数并替换为正确的值

### 问题：LLM 无法调用 MCP 工具

**原因 1：** 未处于 Agent mode

**解决方案：** 打开项目目录并切换到 Agent mode

**原因 2：** MCP 服务器未连接

**解决方案：** 在界面中点击 Retry 图标

> **最佳实践：** 避免为 MCP 服务器及其工具使用过于相似的名称，以避免调用时产生歧义。

### 问题：MCP 服务器列表无法加载

**症状：** 服务器列表一直处于加载状态

**解决方案：** 重启 Qoder IDE 后再试
