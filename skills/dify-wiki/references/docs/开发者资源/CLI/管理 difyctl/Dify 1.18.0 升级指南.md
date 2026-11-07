# Dify 1.18.0 升级指南

> Dify 服务器从 1.17.x 或更早版本升级到 1.18.0 或更高版本时，重新登录、清理旧版残留，并逐一更新命令、脚本和编码 Agent

> 本文档由 AI 自动翻译。如有任何不准确之处，请参考 [英文原版](https://docs.dify.ai/en/cli/upgrade-across-1-18.md)。

> [!NOTE]
>
> 如果旧的 `difyctl` 开始报 `catalog_stale` 错误（「The request was built from a catalog that is not this server's current catalog」），说明 Dify 服务器已经升级到 1.18.0 或更高版本。

## 换用新版

**1. 安装新版**

[安装](../%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B.md#安装) 与服务器匹配的 `difyctl`。

其他地方如果还有旧版（例如 CI 镜像中），一并删除。用新版登录后，再运行旧版的 `auth logout`，可能会删掉新版保存的令牌，你就得重新登录。

如果仍有服务器停留在 1.17.x 或更早版本，需要继续使用旧版（例如预发环境先升级，生产环境暂缓），就用 `DIFYCTL_PREFIX` 把它装到单独的目录，运行时也给它单独的配置目录。这个配置目录起初是空的，所以要用旧版在其中重新登录：

```bash theme={null}
curl -fsSL https://raw.githubusercontent.com/langgenius/dify/main/cli/scripts/install-cli.sh | DIFY_VERSION=1.17.1 DIFYCTL_PREFIX=$HOME/difyctl-1.17 sh
DIFY_CONFIG_DIR=$HOME/.config/difyctl-1.17 $HOME/difyctl-1.17/bin/difyctl auth login --host https://dify-prod.example.com
DIFY_CONFIG_DIR=$HOME/.config/difyctl-1.17 $HOME/difyctl-1.17/bin/difyctl get app
```

**2. 重新登录**

```bash theme={null}
difyctl login --server https://dify.example.com
```

运行 `difyctl describe account`，确认登录成功。

登录选项以及新版把令牌存在哪里，详见 [管理登录](%E7%AE%A1%E7%90%86%E7%99%BB%E5%BD%95.md)。要在 CI 任务中登录，详见 [在 CI 和自动化中使用 `difyctl`](https://docs.dify.ai/zh/cli/scripts-and-ci)。

**3. 结束旧会话**

用新版登录，并不会结束旧版在服务器上的会话，旧会话默认最长有效 14 天。如果别人可能拿到旧令牌（例如机器是多人共用的，或配置目录被复制过），现在就结束它。否则等它自然过期即可。

要结束旧会话，先列出你的所有会话，再删除标签为 `difyctl on <your-machine-name>` 的那一个。新会话的标签只有机器名。删除时不会要求确认，运行前先核对 ID。

```bash theme={null}
difyctl get account session
difyctl delete account session --session-id <session-id>
```

**4. 重新安装 difyctl Skill**

如果 Claude Code、Codex 等编码 Agent 通过 difyctl Skill 使用 `difyctl`，即使一切看似正常，也要重新安装这个 Skill。

旧版的 `skills install --yes` 会为检测到的每个编码 Agent 都安装 difyctl Skill。检查本机有以下哪些目录：

```bash theme={null}
ls -d ~/.claude/skills/difyctl \
  ~/.agents/skills/difyctl \
  ~/.config/opencode/skills/difyctl \
  ~/.cursor/skills/difyctl \
  ~/.pi/agent/skills/difyctl 2>/dev/null
```

`install skills` 只会替换你传入的那个 Skill 目录中的 difyctl Skill。对仍在使用的每个编码 Agent 分别运行一次，其余 Agent 的 `difyctl` 文件夹直接删除：

```bash theme={null}
difyctl install skills ~/.claude/skills   # Claude Code
difyctl install skills ~/.agents/skills   # Codex
```

旧版的 `skills install <dir>` 会把 `SKILL.md` 直接写入 `<dir>`。如果当时指定的是某个编码 Agent 的 Skill 目录，删除它留在那里的文件，例如 `~/.claude/skills/SKILL.md`。

编码 Agent 使用 `difyctl` 还需要哪些配置，详见 [配置编码 Agent](../%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B.md#配置编码-agent)。

## 替换旧命令

大多数命令现在通过具名标志（例如 `--app-id`）接收 ID 等参数值，不再按位置传入。

要查看某条命令支持的全部标志，运行 `difyctl help <command>`。

全局标志只剩下 `--verbose`、`--json` 和 `--help`。`-v`、`-y`、`-w` 等短标志均已移除。`--verbose` 现在只会在错误中附上服务器的原始响应。所有命令都不再要求确认，`--yes` 可以删掉。

### 登录与会话

| 旧版 | 新版 | 备注 |
| :- | :- | :- |
| `auth login --host <url>` | `login --server <url>` | `--server` 为必填。`--no-browser` 和 `--insecure` 仍可使用。 |
| `auth whoami` | `describe account` | |
| `auth logout` | `logout` | |
| `auth devices list` | `get account session` | |
| `auth devices revoke <id>` | `delete account session --session-id <id>` | 不再支持 `--all`。要结束多个会话，需逐个运行。 |
| `auth list`、`use host`、`use account` | 无 | 每个配置目录只保存一份登录信息。要连接多台服务器，用 `DIFY_CONFIG_DIR` 为每台服务器分配单独的目录。要切换账户，重新登录即可。 |

### 应用

| 旧版 | 新版 | 备注 |
| :- | :- | :- |
| `get app` | `get console_app` | `--mode`、`--name`、`--page` 和 `--limit` 仍可使用。 |
| `describe app <id>`、`get app <id>` | `describe console_app --app-id <id>` | |
| `run app <id> "<message>"`（聊天助手或旧版 Agent 应用） | `run console_app chat --app-id <id> --query "<message>"` | |
| `run app`（Chatflow 应用） | `run console_app advanced_chat --app-id <id> --query "<message>"` | |
| `run app`（文本生成应用） | `run console_app completion --app-id <id>` | |
| `run app`（Workflow 应用） | `run console_app workflow --app-id <id> --inputs '{…}'` | |
| `--inputs-file <file>` | `--inputs @<file>` | |
| `--file <key>=@<path>` | `--files '{"<key>":"<path>"}'` | 网络上的文件改为通过 `--inputs` 传入。 |
| `--conversation <id>` | `--conversation-id <id>` | |
| `--stream` | `--stream` | 改为输出原始 JSON 事件，可用 `--only <event>` 过滤。 |
| `--think`、`--retry-on-limit` | 无 | |

不确定应用类型时，可用 `describe console_app` 查看。

运行聊天助手应用，以及从文件读取输入运行 Workflow 应用，新旧写法对比如下：

```bash theme={null}
# 旧版
difyctl run app 0a1b2c3d-4e5f-6789-abcd-ef0123456789 "你们的营业时间是几点？"
difyctl run app 7f3e9a2b-1c4d-4e8f-9a0b-2d5c8e1f4a7b --inputs-file inputs.json

# 新版
difyctl run console_app chat --app-id 0a1b2c3d-4e5f-6789-abcd-ef0123456789 --query "你们的营业时间是几点？"
difyctl run console_app workflow --app-id 7f3e9a2b-1c4d-4e8f-9a0b-2d5c8e1f4a7b --inputs @inputs.json
```

### 人工介入

运行遇到人工介入而暂停时，现在返回 `"status": "suspended"`，原先是 `"paused"`。检查 `paused` 的脚本要相应更新。运行挂起时，返回结果的 `hints` 会列出每个操作对应的 `submit run form` 命令，表单令牌已经填好。

如需自行提交表单，原来的 `resume app` 改为 `submit run form`：

```bash theme={null}
# 旧版
difyctl resume app 7f3e9a2b-1c4d-4e8f-9a0b-2d5c8e1f4a7b <form-token> --workflow-run-id <workflow-run-id> --action approve --inputs '{"comment":"没问题"}'

# 新版
difyctl submit run form --app-id 7f3e9a2b-1c4d-4e8f-9a0b-2d5c8e1f4a7b --form-token <form-token> --action approve --inputs '{"comment":"没问题"}'
```

`submit run form` 不会像 `resume app` 那样接着跟踪运行。要获取运行的后续内容，执行它返回的提示命令 `get run event`。

### DSL 导出与导入

| 旧版 | 新版 | 备注 |
| :- | :- | :- |
| `export studio-app <id>` | `export console_app dsl --app-id <id>` | 输出的 YAML 包在 JSON 中，不再是纯 YAML。 |
| `import studio-app --from-file <file>` | `import console_app dsl --mode yaml-content --yaml-content "$(cat <file>)"` | |
| `import studio-app --from-url <url>` | `import console_app dsl --mode yaml-url --yaml-url <url>` | |

要把导出内容保存为文件，提取其中的 `.data`：

```bash theme={null}
difyctl export console_app dsl --app-id 7f3e9a2b-1c4d-4e8f-9a0b-2d5c8e1f4a7b | jq -r '.data' > app.yml
```

旧版会自动确认待确认的导入，新版不会。文件的 DSL 版本比服务器的新，或主版本比服务器的旧时，导入会处于待确认状态。确认文件可信后，运行 `confirm console_app dsl_import --import-id <import-id>` 完成导入。

旧版还会在导入后列出缺少的集成，现在要改为运行 `check console_app dependency`。

### 工作空间与成员

| 旧版 | 新版 | 备注 |
| :- | :- | :- |
| `get workspace` Cloud | `get workspace` | 不再标出当前工作空间。要查看 `difyctl` 当前所在的工作空间，运行 `describe workspace`。 |
| `use workspace [<id>]` Cloud | `use workspace <id>` | 必须提供 ID。切换不再改变浏览器中的工作空间。[重新登录或设置 `DIFY_WORKSPACE_ID`](https://docs.dify.ai/zh/cli/manage-sign-in#switch-your-workspace) 会让切换失效。 |
| `--workspace <id>`、`-w <id>` Cloud | `--workspace-id <id>` | 只用于在工作空间中操作的命令，例如 `get console_app`。 |
| `get app -A`、`get app --all-workspaces` Cloud | 无 | 先运行 `get workspace`，再对每个工作空间运行 `get console_app --workspace-id <id>`。 |
| `get member` | `get workspace member` | |
| `create member` | `invite workspace member` | |
| `set member` | `set workspace member_role` | |
| `delete member` | `delete workspace member` | |

### 配置、difyctl Skill、帮助与版本

| 旧版 | 新版 | 备注 |
| :- | :- | :- |
| `config get`、`config view`、`config path` | `get config [<key>]` | 同时显示配置路径。 |
| `config set` | `set config` | 只剩 `http.timeout` 这一项设置。 |
| `config unset` | `unset config` | |
| `env list` | 无 | `difyctl` 读取哪些环境变量，详见 [环境变量](../%E5%8F%82%E8%80%83/%E9%85%8D%E7%BD%AE.md#环境变量)。 |
| `skills install` | `install skills <skills-root>` | 如何为每个编码 Agent 重新安装，详见 [换用新版](Dify%201.18.0%20%E5%8D%87%E7%BA%A7%E6%8C%87%E5%8D%97.md#换用新版) 的第 4 步。 |
| 带 `--short`、`--client`、`--check-compat` 或 `-o` 的 `version` | `version` | 不接受任何标志。 |
| `help -o json --compact`、`help <command> -o json` | `help`、`help <command>` | 通过管道输出时（例如在脚本中）打印 JSON。 |

## 更新脚本中的其他部分

### 以 JSON 读取结果

结果现在一律为 JSON，`-o` 会被当作未知标志而报错，因此要从脚本中删除 `-o json`。

如果脚本原先要求其他格式（如 `-o name` 或 `-o yaml`），需要自行用 `jq` 等工具转换 JSON。以下命令只把聊天助手的回复保留为纯文本：

```bash theme={null}
difyctl run console_app chat --app-id 0a1b2c3d-4e5f-6789-abcd-ef0123456789 --query "你们的营业时间是几点？" | jq -r '.text.answer'
```

在脚本中设置 `DIFY_OUTPUT=json`，或传入 `--json`，这样无论脚本在哪里运行，错误都以 JSON 输出。不设置的话，stderr 上的错误在管道中是 JSON，在终端中则是文本。

### 处理新的退出码和错误码

退出码的编号基本不变，但有两处变化：

* 6 原先表示版本不匹配，现在表示 `difyctl` 在服务器上找不到对应的命令：要么无法获取服务器的命令列表，要么列表里没有与输入匹配的命令。
* 64 已随 `version --check-compat` 一同移除。

如果脚本根据错误码走不同分支：

* 将 `server_4xx_other` 和 `server_5xx` 替换为 `server_error`，并检查随错误一起返回的 HTTP 状态码。
* 将 `token_expired` 和 `expired_token` 替换为 `auth_expired`，它的退出码为 4。
* 删除 `version_skew`、`unsupported_endpoint`、`client_error`、`illegal_argument` 和 `config_schema_unsupported` 的分支。

`input_invalid`、`catalog_unavailable` 等新错误码的含义，详见 [结果、错误与退出码](../%E5%8F%82%E8%80%83/%E7%BB%93%E6%9E%9C%E3%80%81%E9%94%99%E8%AF%AF%E4%B8%8E%E9%80%80%E5%87%BA%E7%A0%81.md)。

### 在脚本中自行重试

新版不会重试失败的请求，`--http-retry` 也已移除。如果脚本依赖重试，需要自己实现。哪些命令可以放心重试，详见 [重试失败的命令](../%E5%8F%82%E8%80%83/%E7%BB%93%E6%9E%9C%E3%80%81%E9%94%99%E8%AF%AF%E4%B8%8E%E9%80%80%E5%87%BA%E7%A0%81.md#重试失败的命令)。

### 更新环境变量

从脚本和 CI 配置中删除以下变量：

* `DIFY_LIMIT`：改为传入 `--limit`。
* `DIFYCTL_HTTP_RETRY`：没有替代项。
* `DIFYCTL_NO_COLOR`：改用 `NO_COLOR`。
* `DIFY_CACHE_DIR`：缓存现在存放在配置目录中，由 `DIFY_CONFIG_DIR` 一并决定。

`DIFY_CONFIG_DIR` 和 `DIFY_WORKSPACE_ID` 照常可用。

新版读取的全部环境变量，详见 [环境变量](../%E5%8F%82%E8%80%83/%E9%85%8D%E7%BD%AE.md#环境变量)。
