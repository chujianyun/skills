# 更新或卸载 difyctl

> Dify 服务器升级到新版本时更新 difyctl，或从机器上卸载 difyctl

> 本文档由 AI 自动翻译。如有任何不准确之处，请参考 [英文原版](https://docs.dify.ai/en/cli/update-or-uninstall.md)。

## 更新

> [!NOTE]
>
> 服务器从 1.17.x 或更早的版本升级到 1.18.0 或更高版本后，旧的构建版本就无法再与它配合使用。需要重做哪些步骤、哪些命令有变化，详见 [Dify 1.18.0 升级指南](Dify%201.18.0%20%E5%8D%87%E7%BA%A7%E6%8C%87%E5%8D%97.md)。

服务器每次升级到新的 Dify 版本，都要随之更新 `difyctl`：

1. 按对应的服务器版本重新运行 [安装命令](../%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B.md#安装)；如果之前设置过 `DIFYCTL_PREFIX`，也保持相同的值。新的构建版本会原地替换旧版本。
2. 运行 `difyctl version`，确认构建版本与服务器版本一致。
3. 如果有编码 Agent 在使用 `difyctl`，[重新安装](../%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B.md#配置编码-agent) difyctl Skill，否则 Agent 会继续按旧版本的说明操作。

`difyctl` 会自动获取服务器的新命令。如果 `difyctl help` 显示的仍是旧列表，运行 `difyctl refresh cache`。

## 卸载

1. 趁 `difyctl` 还没卸载，先 [退出登录](%E7%AE%A1%E7%90%86%E7%99%BB%E5%BD%95.md#登出)。退出登录会结束你在服务器上的会话，并删除本机保存的令牌，直接删除二进制文件则不会：

   ```bash theme={null}
   difyctl logout
   ```

2. 删除二进制文件：

   ```bash macOS / Linux theme={null}
   rm ~/.local/bin/difyctl
   ```

   ```powershell Windows theme={null}
   Remove-Item -Recurse "$env:LOCALAPPDATA\difyctl"
   ```

   如果安装时设置了 `DIFYCTL_PREFIX`，二进制文件则在 `<prefix>/bin` 中。

3. 如需一并删除设置，删除配置目录：

   ```bash macOS theme={null}
   rm -rf ~/.config/difyctl
   ```

   ```bash Linux theme={null}
   rm -rf "${XDG_CONFIG_HOME:-$HOME/.config}/difyctl"
   ```

   ```powershell Windows theme={null}
   Remove-Item -Recurse "$env:APPDATA\difyctl"
   ```

   如果设置过 `DIFY_CONFIG_DIR`，改为删除它指向的目录。

4. 如果为编码 Agent 安装过 difyctl Skill，从 [该 Agent 的 Skill 目录](../%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B.md#配置编码-agent) 中删除 `difyctl` 文件夹。
