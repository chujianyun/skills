# CLI 快速上手

来源: https://docs.qoder.com/zh/cli/quick-start

## 安装方式

- `curl -fsSL https://qoder.com/install | bash`
- `brew install qoderai/qoder/qodercli --cask`
- `npm install -g @qoder-ai/qodercli`

## 支持平台

- macOS
- Linux
- Windows（Windows Terminal）
- CPU 架构：`arm64`、`amd64`

## 登录方式

- 交互式登录：运行 `qodercli` 后使用 `/login`
- 环境变量登录：设置 `QODER_PERSONAL_ACCESS_TOKEN`

## 常用命令

- `qodercli --version`
- `qodercli update`
- `/login`
- `/logout`

## 额外说明

- 默认开启自动升级
- 可在 `~/.qoder.json` 中将 `autoUpdates` 设为 `false`

