# 在 CI 和自动化中使用 `difyctl`

> 在 CI 任务中安装 difyctl、配置登录，并让任务在该停下时停下，另附合并时更新应用的示例

> 本文档由 AI 自动翻译。如有任何不准确之处，请参考 [英文原版](https://docs.dify.ai/en/cli/scripts-and-ci.md)。

> [!TIP]
>
> 要交给编码 Agent 来做，先 [为它配置好 `difyctl` Skill](https://docs.dify.ai/zh/cli/get-started#配置编码-agent)，再把这个页面发给它。

## 在任务中安装 `difyctl`

使用 [安装程序](../%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B.md#安装) 安装，并始终把 `DIFY_VERSION` 设为服务器的版本号，这样 Dify 发布新版本后，任务装到的构建版本也不会跟着变。如果安装程序因触及 GitHub 的请求上限而中止，在任务的环境变量中设置 `GITHUB_TOKEN` 或 `GH_TOKEN`。

## 登录

任务无人值守时，由你自己登录，再把令牌交给任务。如果每次都有人能批准验证码，脚本也可自行登录。

### 把令牌交给任务

用 CI 专用的账户获取令牌，或者在一台平时不运行 `difyctl` 的机器上获取。账户需具备编辑及以上角色，才能导入、测试和发布。如果同一账户在那台机器上再次登录，任务的登录就会失效。

登录时加上 `--no-keyring`，这样就能从文件中复制令牌：

```bash theme={null}
difyctl login --server https://dify.example.com --no-keyring
```

从 [配置目录](../%E7%AE%A1%E7%90%86%20difyctl/%E7%AE%A1%E7%90%86%E7%99%BB%E5%BD%95.md#令牌的存储位置) 中的 `tokens.yml` 复制令牌：

```yaml theme={null}
tokens:
  dify.example.com:
    ci@example.com: dfoa_…
```

把令牌存为 CI Secret，并在任务中设置以下 [环境变量](../%E5%8F%82%E8%80%83/%E9%85%8D%E7%BD%AE.md#环境变量)：

* `DIFY_SERVER`：登录时使用的地址。
* `DIFY_TOKEN`：令牌，从 Secret 中读取。
* `DIFY_WORKSPACE_ID`：应用所在工作空间的 `id`，可在 `difyctl get workspace` 的结果中查到。

如果任务无法写入默认的配置目录，把 `DIFY_CONFIG_DIR` 设为一个可写的目录。

然后删除 `tokens.yml`，让令牌只保存在 CI Secret 中。删除后，你登录所用的那台机器会退出登录，任务则照常运行。如果改为运行 `logout`，任务的登录也会一并失效。

#### 续期登录

任务中的命令报 `auth_expired` 错误（退出码 4）时，重新登录，再替换 CI Secret 中的令牌。

以下情况会让登录失效：

* 登录到期：有效期为 14 天；在自部署的服务器上，如果设置了 [`OAUTH_TTL_DAYS`](https://docs.dify.ai/zh/self-host/deploy/configuration/environments#dify-cli-与编程-api)，则以它设定的天数为准。
* 同一账户在那台机器上再次登录，即使换了配置目录也一样。

想赶在任务失败前续期，在任务中运行 `difyctl get account session`，找到 `device_label` 为你登录所用机器的那个会话，查看它的 `expires_at`。

### 在脚本中登录

用 `--no-wait` 发起登录。和其他 `login` 一样，它会先退出当前的会话，然后打印验证码，不等批准就结束运行：

```bash theme={null}
difyctl login --server https://dify.example.com --no-wait
```

```json theme={null}
{"status":"pending","verification_uri":"…","user_code":"…","expires_in":900}
```

把 `verification_uri` 和 `user_code` 发给负责批准的人，对方要在 15 分钟内打开该 URL 并批准验证码。

然后在同一个配置目录中完成登录：

```bash theme={null}
difyctl login --resume
```

* 验证码获批之前，它会打印 `{"status":"pending"}` 并以 0 退出，因此要检查 `status`，而不是退出码。
* 验证码获批后，它改为打印已登录的 `account`，不再带有 `status`。
* 如果验证码被拒绝，或在获批前过期，命令会失败并返回退出码 4。这时用 `login --no-wait` 重新开始。

如果在旧验证码过期前就重新开始，要确保没有人批准它。你用新验证码登录后，一旦有人批准了旧验证码，你的登录就会失效。

批准编码 Agent 的验证码前要检查什么，详见 [登录](../%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B.md#登录)。

## 处理失败

每个步骤都用 bash 运行，并设置 `set -eo pipefail`。

以下命令即使遇到任务该停下的情况，也会以 0 退出。用 `jq -e` 检查它们的输出，条件不成立时 `jq -e` 就会失败：

* `check console_app dsl`（文件无效时）：`jq -e '.valid'`
* `import console_app dsl`（导入停在待确认状态时）：`jq -e '.status | startswith("completed")'`
* `check console_app dependency`（工作空间缺少应用用到的集成时）：`jq -e '.leaked_dependencies | length == 0'`
* `test console_app workflow`（运行 [暂停或被截断](../%E5%8F%82%E8%80%83/%E7%BB%93%E6%9E%9C%E3%80%81%E9%94%99%E8%AF%AF%E4%B8%8E%E9%80%80%E5%87%BA%E7%A0%81.md#判断运行如何结束) 时）：`jq -e '.status == "ended"'`
* `check console_app release`（草稿还不能发布时）：`jq -e '.ready'`

命令返回退出码 7 时，说明触发了 [限流](../%E5%8F%82%E8%80%83/%E7%BB%93%E6%9E%9C%E3%80%81%E9%94%99%E8%AF%AF%E4%B8%8E%E9%80%80%E5%87%BA%E7%A0%81.md#限流)，命令没有执行任何操作。让任务等 1 分钟后重试。

## 示例：合并时更新应用

下面这个 GitHub Actions 工作流会在 Pull Request 改动应用的 DSL 文件 `apps/order-status.yml` 时，对照应用检查该文件；合并到 `main` 后，再更新并发布应用。每一步的作用详见 [更新应用](%E9%80%9A%E8%BF%87%20DSL%20%E6%96%87%E4%BB%B6%E5%88%9B%E5%BB%BA%E5%92%8C%E6%9B%B4%E6%96%B0%E5%BA%94%E7%94%A8.md#更新应用)。

> [!WARNING]
>
> 每次导入都会替换应用的草稿，有人在工作室中做的改动也会一并丢失，所以只通过仓库修改这个应用。导入还会立即应用文件中的名称、描述、图标和 Web 应用设置。如果后续某一步失败，线上的工作流保持不变。

使用前，在仓库的 **Settings** > **Secrets and variables** > **Actions** 中添加 Secret `DIFY_TOKEN` 和变量 `DIFY_WORKSPACE_ID`。然后把示例值换成你自己的：服务器地址、应用的 ID 和名称（两者都可通过 `difyctl get console_app` 查到）、文件路径、Dify 版本号和测试输入。

```yaml .github/workflows/update-order-status.yml theme={null}
name: Update Order Status

on:
  pull_request:
    paths: [apps/order-status.yml]
  push:
    branches: [main]
    paths: [apps/order-status.yml]

defaults:
  run:
    shell: bash  # 与默认设置不同，会以 pipefail 运行各步骤

env:
  DIFY_SERVER: https://dify.example.com
  DIFY_TOKEN: ${{ secrets.DIFY_TOKEN }}
  DIFY_WORKSPACE_ID: ${{ vars.DIFY_WORKSPACE_ID }}
  APP_ID: 9b4d2e7c-1a6f-4c8e-b3d5-7e2a9f1c4b6d
  FILE: apps/order-status.yml

jobs:
  check:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install difyctl
        run: |
          curl -fsSL https://raw.githubusercontent.com/langgenius/dify/main/cli/scripts/install-cli.sh | DIFY_VERSION=1.18.0 sh
          echo "$HOME/.local/bin" >> "$GITHUB_PATH"
      - name: Check the file against the app
        run: difyctl check console_app dsl --app-id "$APP_ID" --yaml-content "$(cat "$FILE")" | jq -e '.valid'

  update:
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install difyctl
        run: |
          curl -fsSL https://raw.githubusercontent.com/langgenius/dify/main/cli/scripts/install-cli.sh | DIFY_VERSION=1.18.0 sh
          echo "$HOME/.local/bin" >> "$GITHUB_PATH"
      - name: Import the file
        run: |
          H=$(difyctl export console_app dsl --app-id "$APP_ID" | jq -r .draft_hash)
          difyctl import console_app dsl --mode yaml-content --yaml-content "$(cat "$FILE")" \
            --app-id "$APP_ID" --draft-hash "$H" --name "Order Status" | jq -e '.status | startswith("completed")'
          difyctl check console_app dependency --app-id "$APP_ID" | jq -e '.leaked_dependencies | length == 0'
      - name: Test and publish
        run: |
          difyctl test console_app workflow --app-id "$APP_ID" --inputs '{"topic": "order 1042"}' | jq -e '.status == "ended"'
          difyctl check console_app release --app-id "$APP_ID" | jq -e '.ready'
          difyctl publish console_app --app-id "$APP_ID" --marked-name "${GITHUB_SHA::7}"
```
