# Codex

::: tip
目前 TokenDance 支持通过 Responses API 在 Codex 中使用 `deepseek-v4-flash-0731`。本文提供 AI 辅助和手动两种配置方式，任选其一。
:::

Codex CLI、Codex Desktop App 与 Codex IDE Extension 共用 `~/.codex/config.toml`，配置一次即可在各客户端使用。

以下两种配置方式任选其一：可以让具备本地文件权限的 AI 协助配置，也可以手动配置，无需重复执行。

## 方式一：AI 辅助配置 {#ai-assisted}

先[下载 models.json](https://au-tokendance.tos-cn-shanghai.volces.com/public/models.json)，然后将本教程和下载的文件一起交给具备本地文件读写权限的 AI，并发送以下指令：

::: warning
请根据这份文档配置 Codex 直连 TokenDance。执行要求：

1. 先读取 `~/.codex/config.toml`，不要立即覆盖。
2. 修改前备份该文件；如果 `~/.codex/config.toml.backup-before-tokendance` 已存在，请创建带时间戳的新备份，不要覆盖旧备份。
3. 保留原有 `desktop`、`plugins`、MCP、`projects`、`features` 和 `notify` 配置。
4. 使用我随文提供的 `models.json` 创建 `~/.codex/models.json`。如果无法读取该文件，请停止并让我重新上传，不要自行编造模型目录内容。
5. 将六个顶层模型字段放在第一个 TOML 配置段之前。
6. 将 `[model_providers.tokendance]` 放在文件末尾；如果原文件已有该区块，请修改原区块，不要重复添加。
7. 不得产生重复字段或重复 Provider 区块。
8. API Key 保留占位符，由我稍后手动填写。
9. 不要修改 `auth.json` 和 `models_cache.json`。
10. 修改完成后校验 TOML 与 JSON，但不要退出或重启 Codex。
11. 最后告诉我：修改了哪些文件、备份文件路径，以及仍需手动填写 API Key 的位置。
:::

AI 完成后，请打开 `~/.codex/config.toml`，将 `experimental_bearer_token` 的占位符替换为你的 TokenDance API Key，然后完全退出并重新启动 Codex。

## 方式二：手动配置 {#manual}

### 1. 将 TokenDance 配置为模型提供方 {#configure-provider}

开始前，请确保已经运行过一次 Codex，并在 TokenDance [API 密钥](https://tokendance.space/keys)页面获取 API Key。建议使用最新版 Codex；Codex CLI 至少需要 `0.144.0`，Codex Desktop App 和 Codex IDE Extension 请升级到当前最新版。

建议先备份 `~/.codex/config.toml`。

#### 创建模型目录文件 {#model-catalog}

[下载 models.json](https://au-tokendance.tos-cn-shanghai.volces.com/public/models.json)，保存到：

```text
~/.codex/models.json
```

#### 编辑 Codex 配置文件 {#edit-config}

编辑 `~/.codex/config.toml`（不存在则新建），并将 API Key 占位符替换为你的 TokenDance API Key：

```toml title="~/.codex/config.toml"
model = "deepseek-v4-flash-0731"
model_provider = "tokendance"
preferred_auth_method = "apikey"
forced_login_method = "api"
model_reasoning_effort = "high"
model_catalog_json = "~/.codex/models.json"

[model_providers.tokendance]
name = "TokenDance"
base_url = "https://tokendance.space/gateway/v1"
wire_api = "responses"
experimental_bearer_token = "<你的 TokenDance API Key>"
```

##### 没有 `config.toml` 时怎么放置 {#new-config}

直接把上述代码复制到 `config.toml` 中。

##### 已有 `config.toml` 时怎么放置 {#existing-config}

找到文件中第一行以 `[` 开头的配置段，例如 `[desktop]`。将上述代码的前六个顶层字段放在它之前；如果已经存在 `model`、`model_provider` 等同名字段，直接修改原字段，不要重复添加。

例如，原文件是：

```toml
notify = ["某个通知程序", "turn-ended"]

[desktop]
followUpQueueMode = "queue"
```

修改后应为：

```toml
model = "deepseek-v4-flash-0731"
model_provider = "tokendance"
preferred_auth_method = "apikey"
forced_login_method = "api"
model_reasoning_effort = "high"
model_catalog_json = "~/.codex/models.json"

notify = ["某个通知程序", "turn-ended"]

[desktop]
followUpQueueMode = "queue"
```

如果文件中不存在 `[model_providers.tokendance]`，将以下 Provider 区块追加到整个文件末尾；如果已经存在，请直接修改原区块，不要重复添加：

```toml
[model_providers.tokendance]
name = "TokenDance"
base_url = "https://tokendance.space/gateway/v1"
wire_api = "responses"
experimental_bearer_token = "<你的 TokenDance API Key>"
```

::: warning
`base_url` 只填写到 `/gateway/v1`，不要追加 `/responses`。Codex 会自动请求 `https://tokendance.space/gateway/v1/responses`。
:::

#### 字段说明 {#fields}

| 字段 | 作用 |
|---|---|
| `model` | 默认模型 ID |
| `model_provider` | 模型提供方，对应 `[model_providers.tokendance]` |
| `preferred_auth_method`、`forced_login_method` | 使用 API Key 认证 |
| `model_reasoning_effort` | 默认推理强度 |
| `model_catalog_json` | 本地模型目录文件路径 |
| `name` | Provider 在 Codex 中的显示名称 |
| `base_url` | TokenDance API Base URL |
| `wire_api` | 使用 Responses API |
| `experimental_bearer_token` | TokenDance API Key |

### 2. 开始使用 {#start}

保存配置后，完全退出并重新启动 Codex：

- **Codex CLI**：启动信息中显示 `model: deepseek-v4-flash-0731`，即表示配置已读取。
- **Codex Desktop App**：模型选择器可能显示“自定义”。
- **Codex IDE Extension**：与 CLI 共用同一份配置，无需再次设置。

Codex 正常回复，且 TokenDance 后台出现对应模型的请求和扣费记录，即可确认调用成功。

::: tip
**桌面端显示说明：** 部分 Codex Desktop App 版本暂未在模型选择器中展示第三方本地模型名称，因此可能回退显示为“自定义”。实际请求仍按照 `config.toml` 中的 `model` 和 `model_provider` 发送，请以 TokenDance 后台调用记录为准。
:::

::: note
切换到 TokenDance 后，ChatGPT 官方认证下的历史任务可能暂时不显示，但通常没有被删除。恢复原来的 `config.toml` 并重启 Codex 后即可重新查看。
:::

::: warning
`experimental_bearer_token` 会将 API Key 明文保存在本机配置文件中。请勿分享 `config.toml` 或 `auth.json`，也不要修改 `models_cache.json`。
:::

## 相关文档 {#related}

- [API 密钥](../../%E5%BC%80%E5%A7%8B%E4%BD%BF%E7%94%A8/%E8%AE%BF%E9%97%AE%E4%B8%8E%E8%AE%A4%E8%AF%81/API%20%E5%AF%86%E9%92%A5.md) — 创建和管理 TokenDance API Key
- [CC-Switch](CC-Switch.md) — 管理其他编程工具的供应商配置
- [多协议支持](../../%E6%A8%A1%E5%9E%8B%E4%B8%8E%E5%8D%8F%E8%AE%AE/%E9%80%89%E6%8B%A9%E6%A8%A1%E5%9E%8B%E4%B8%8E%E5%8D%8F%E8%AE%AE/%E5%8D%8F%E8%AE%AE%E6%80%BB%E8%A7%88.md) — 查看 TokenDance 支持的 API 协议
