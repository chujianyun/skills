> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code

> 在 Claude Code 中使用千问AI平台模型

## 安装 Claude Code

<Tabs>
  <Tab title="macOS/Linux">
    1. 安装或更新 [Node.js](https://nodejs.org/en/download/)（v18.0 或更高版本）。

    2. 在终端中执行下列命令，安装 Claude Code。

    ```bash
    npm install -g @anthropic-ai/claude-code
    ```

    3. 运行以下命令验证安装。若有版本号输出，则表示安装成功。

    ```bash
    claude --version
    ```
  </Tab>

  <Tab title="Windows">
    在 Windows 上使用 Claude Code，需要安装 WSL 或 [Git for Windows](https://git-scm.com/install/windows)，然后在 WSL 或 Git Bash 中执行以下命令。

    ```bash
    npm install -g @anthropic-ai/claude-code
    ```

    <Note>
      详情可参考 Claude Code 官方文档的 [Windows 安装教程](https://docs.anthropic.com/en/docs/claude-code/setup#windows-setup)。
    </Note>
  </Tab>
</Tabs>

## 配置 Token Plan 个人版

在 Claude Code 中接入 Token Plan 个人版，需要配置以下信息：

- `ANTHROPIC_BASE_URL`：设置为 `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`。
- `ANTHROPIC_AUTH_TOKEN`：设置为 Token Plan 个人版专属 API Key。
- `ANTHROPIC_MODEL`：设置为 Token Plan 个人版支持的模型。

<Tabs>
  <Tab title="macOS/Linux">
    1. 创建并打开配置文件 `~/.claude/settings.json`。

    <Note>
      `~` 代表当前系统账户的主目录。如果 `.claude` 目录不存在，需要先行创建。可在终端执行 `mkdir -p ~/.claude` 来创建。
    </Note>

    ```bash
    nano ~/.claude/settings.json
    ```

    2. 编辑配置文件。将 `YOUR_API_KEY` 替换为 Token Plan 个人版专属 [API Key](https://platform.qianwenai.com/home/api-keys)。可用模型：qwen3.8-max、qwen3.7-max、qwen3.7-plus、qwen3.6-flash、glm-5.2、deepseek-v4-pro、deepseek-v4-flash-0731。完整说明参见 Token Plan 个人版[支持的模型](/token-plan/personal/token-plan-personal-overview#支持的模型)。

    ```json
    {
        "env": {
            "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
            "ANTHROPIC_BASE_URL": "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic",
            "ANTHROPIC_MODEL": "qwen3.8-max",
            "ANTHROPIC_DEFAULT_HAIKU_MODEL": "qwen3.6-flash",
            "ANTHROPIC_DEFAULT_SONNET_MODEL": "qwen3.8-max",
            "ANTHROPIC_DEFAULT_OPUS_MODEL": "qwen3.8-max",
            "CLAUDE_CODE_SUBAGENT_MODEL": "qwen3.7-max",
            "CLAUDE_CODE_MAX_CONTEXT_TOKENS": "983616"
        }
    }
    ```

    <Note>
      **qwen3.8-max 思考模式说明**：

      - **thinking**：支持开启和关闭（混合思考模式）。
      - **temperature**：思考模式下默认值为 0.6；传入值小于 0.6 时自动调整为 0.6。
      - **reasoning\_effort**：控制推理深度，可选 xhigh、medium、low，默认 xhigh。
    </Note>

    保存配置文件，重新打开一个终端即可生效。

    3. 编辑或新增 `~/.claude.json` 文件，将 `hasCompletedOnboarding` 字段的值设置为 `true` 并保存文件。

    ```json
    {
      "hasCompletedOnboarding": true
    }
    ```

    <Warning>
      `hasCompletedOnboarding` 作为顶层字段，请勿嵌套于其他字段。该步骤可避免启动 Claude Code 时报错：`Unable to connect to Anthropic services`。
    </Warning>
  </Tab>

  <Tab title="Windows">
    1. 创建并打开配置文件 `C:\Users\<用户名>\.claude\settings.json`。

    <Tabs>
      <Tab title="CMD">
        1) 创建目录

        ```powershell
        if not exist "%USERPROFILE%\.claude" mkdir "%USERPROFILE%\.claude"
        ```

        2. 创建并打开文件

        ```powershell
        notepad "%USERPROFILE%\.claude\settings.json"
        ```
      </Tab>

      <Tab title="PowerShell">
        1. 创建目录

        ```powershell
        mkdir -Force $HOME\.claude
        ```

        2. 创建并打开文件

        ```powershell
        notepad $HOME\.claude\settings.json
        ```
      </Tab>
    </Tabs>

    2. 编辑配置文件。将 `YOUR_API_KEY` 替换为 Token Plan 个人版专属 [API Key](https://platform.qianwenai.com/home/api-keys)。可用模型：qwen3.8-max、qwen3.7-max、qwen3.7-plus、qwen3.6-flash、glm-5.2、deepseek-v4-pro、deepseek-v4-flash-0731。完整说明参见 Token Plan 个人版[支持的模型](/token-plan/personal/token-plan-personal-overview#支持的模型)。

    ```json
    {
        "env": {
            "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
            "ANTHROPIC_BASE_URL": "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic",
            "ANTHROPIC_MODEL": "qwen3.8-max",
            "ANTHROPIC_DEFAULT_HAIKU_MODEL": "qwen3.6-flash",
            "ANTHROPIC_DEFAULT_SONNET_MODEL": "qwen3.8-max",
            "ANTHROPIC_DEFAULT_OPUS_MODEL": "qwen3.8-max",
            "CLAUDE_CODE_SUBAGENT_MODEL": "qwen3.7-max",
            "CLAUDE_CODE_MAX_CONTEXT_TOKENS": "983616"
        }
    }
    ```

    <Note>
      **qwen3.8-max 思考模式说明**：

      - **thinking**：支持开启和关闭（混合思考模式）。
      - **temperature**：思考模式下默认值为 0.6；传入值小于 0.6 时自动调整为 0.6。
      - **reasoning\_effort**：控制推理深度，可选 xhigh、medium、low，默认 xhigh。
    </Note>

    保存配置文件，重新打开一个终端即可生效。

    3. 编辑或新增 `C:\Users\<用户名>\.claude.json` 文件，将 `hasCompletedOnboarding` 字段的值设置为 `true`，并保存文件。

    ```json
    {
      "hasCompletedOnboarding": true
    }
    ```
  </Tab>
</Tabs>

## 配置 Token Plan 团队版

在 Claude Code 中接入 Token Plan 团队版，需要配置以下信息：

- `ANTHROPIC_BASE_URL`：设置为 `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`。
- `ANTHROPIC_AUTH_TOKEN`：设置为 Token Plan 团队版专属 API Key。
- `ANTHROPIC_MODEL`：设置为 Token Plan 团队版支持的模型。

<Tabs>
  <Tab title="macOS/Linux">
    1. 创建并打开配置文件 `~/.claude/settings.json`。

    <Note>
      `~` 代表当前系统账户的主目录。如果 `.claude` 目录不存在，需要先行创建。可在终端执行 `mkdir -p ~/.claude` 来创建。
    </Note>

    ```bash
    nano ~/.claude/settings.json
    ```

    2. 编辑配置文件。将 `YOUR_API_KEY` 替换为 Token Plan 团队版专属 API Key。

    ```json
    {
        "env": {
            "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
            "ANTHROPIC_BASE_URL": "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic",
            "ANTHROPIC_MODEL": "qwen3.8-max",
            "ANTHROPIC_DEFAULT_HAIKU_MODEL": "qwen3.6-flash",
            "ANTHROPIC_DEFAULT_SONNET_MODEL": "qwen3.8-max",
            "ANTHROPIC_DEFAULT_OPUS_MODEL": "qwen3.8-max",
            "CLAUDE_CODE_SUBAGENT_MODEL": "qwen3.7-max",
            "CLAUDE_CODE_MAX_CONTEXT_TOKENS": "983616"
        }
    }
    ```

    <Note>
      **qwen3.8-max 思考模式说明**：

      - **thinking**：支持开启和关闭（混合思考模式）。
      - **temperature**：思考模式下默认值为 0.6；传入值小于 0.6 时自动调整为 0.6。
      - **reasoning\_effort**：控制推理深度，可选 xhigh、medium、low，默认 xhigh。
    </Note>

    保存配置文件，重新打开一个终端即可生效。

    3. 编辑或新增 `~/.claude.json` 文件，将 `hasCompletedOnboarding` 字段的值设置为 `true` 并保存文件。

    ```json
    {
      "hasCompletedOnboarding": true
    }
    ```

    <Warning>
      `hasCompletedOnboarding` 作为顶层字段，请勿嵌套于其他字段。该步骤可避免启动 Claude Code 时报错：`Unable to connect to Anthropic services`。
    </Warning>
  </Tab>

  <Tab title="Windows">
    1. 创建并打开配置文件 `C:\Users\<用户名>\.claude\settings.json`。

    <Tabs>
      <Tab title="CMD">
        1) 创建目录

        ```powershell
        if not exist "%USERPROFILE%\.claude" mkdir "%USERPROFILE%\.claude"
        ```

        2. 创建并打开文件

        ```powershell
        notepad "%USERPROFILE%\.claude\settings.json"
        ```
      </Tab>

      <Tab title="PowerShell">
        1. 创建目录

        ```powershell
        mkdir -Force $HOME\.claude
        ```

        2. 创建并打开文件

        ```powershell
        notepad $HOME\.claude\settings.json
        ```
      </Tab>
    </Tabs>

    2. 编辑配置文件。将 `YOUR_API_KEY` 替换为 Token Plan 团队版专属 API Key。

    ```json
    {
        "env": {
            "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
            "ANTHROPIC_BASE_URL": "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic",
            "ANTHROPIC_MODEL": "qwen3.8-max",
            "ANTHROPIC_DEFAULT_HAIKU_MODEL": "qwen3.6-flash",
            "ANTHROPIC_DEFAULT_SONNET_MODEL": "qwen3.8-max",
            "ANTHROPIC_DEFAULT_OPUS_MODEL": "qwen3.8-max",
            "CLAUDE_CODE_SUBAGENT_MODEL": "qwen3.7-max",
            "CLAUDE_CODE_MAX_CONTEXT_TOKENS": "983616"
        }
    }
    ```

    <Note>
      **qwen3.8-max 思考模式说明**：

      - **thinking**：支持开启和关闭（混合思考模式）。
      - **temperature**：思考模式下默认值为 0.6；传入值小于 0.6 时自动调整为 0.6。
      - **reasoning\_effort**：控制推理深度，可选 xhigh、medium、low，默认 xhigh。
    </Note>

    保存配置文件，重新打开一个终端即可生效。

    3. 编辑或新增 `C:\Users\<用户名>\.claude.json` 文件，将 `hasCompletedOnboarding` 字段的值设置为 `true`，并保存文件。

    ```json
    {
      "hasCompletedOnboarding": true
    }
    ```
  </Tab>
</Tabs>

## 配置按量计费

将 `YOUR_API_KEY` 替换为千问AI平台 [API Key](/developer-guides/administration/api-keys)。可用模型请参考[支持的模型](/developer-guides/getting-started/text-generation-models)。

| 配置项          | 说明                                                                             |
| ------------ | ------------------------------------------------------------------------------ |
| **Base URL** | `https://dashscope.aliyuncs.com/apps/anthropic`                                |
| **API Key**  | 千问AI平台 [API Key](/developer-guides/administration/api-keys)（格式为 `sk-ws-xxxxx`） |
| **可用模型**     | [支持的模型](/developer-guides/getting-started/text-generation-models)              |

创建或编辑 `~/.claude/settings.json`（Windows 路径：`C:\Users\<用户名>\.claude\settings.json`），写入以下配置：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
    "ANTHROPIC_BASE_URL": "https://dashscope.aliyuncs.com/apps/anthropic",
    "ANTHROPIC_MODEL": "qwen3.7-max",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "qwen3.6-flash",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "qwen3.7-max",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "qwen3.7-max",
    "CLAUDE_CODE_SUBAGENT_MODEL": "qwen3.7-max"
  }
}
```

配置保存后，新开一个终端窗口执行 `claude "你好"`。若模型正常返回响应，配置成功。如需进一步确认，在 Claude Code 中执行 `/status`，检查 `ANTHROPIC_BASE_URL` 和 `ANTHROPIC_AUTH_TOKEN` 是否正确指向千问AI平台地址。

### 配置上下文窗口大小

Claude Code 默认使用 200K 上下文窗口。如果需要处理大型代码仓库或长对话，可以将上下文窗口扩展到 1M（1,000,000 tokens），前提是所用模型支持该上下文长度。有两种配置方式：

**方式一：通过环境变量设置**

在 `~/.claude/settings.json` 的 `env` 字段中添加 `CLAUDE_CODE_MAX_CONTEXT_TOKENS`：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
    "ANTHROPIC_BASE_URL": "https://dashscope.aliyuncs.com/apps/anthropic",
    "ANTHROPIC_MODEL": "qwen3.7-plus",
    "CLAUDE_CODE_MAX_CONTEXT_TOKENS": "1000000"
  }
}
```

**方式二：通过模型名称后缀**

在模型名称后添加 `[1m]` 后缀，适用于千问AI平台支持 1M 上下文的模型：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
    "ANTHROPIC_BASE_URL": "https://dashscope.aliyuncs.com/apps/anthropic",
    "ANTHROPIC_MODEL": "qwen3.7-plus[1m]",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "qwen3.7-plus[1m]",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "qwen3.7-plus[1m]",
    "CLAUDE_CODE_SUBAGENT_MODEL": "qwen3.7-plus[1m]"
  }
}
```

修改配置后，需新开终端窗口重新启动 Claude Code 使配置生效。更多环境变量说明参见 [Claude Code 官方环境变量文档](https://code.claude.com/docs/zh-CN/env-vars)。

## 使用 CC Switch

[CC Switch](https://github.com/farion1231/cc-switch) 是社区开源的桌面 GUI，可在多个 API Key 或计费方案之间一键切换，免去手动改 `settings.json`。

### 安装

- macOS：`brew tap farion1231/ccswitch && brew install --cask cc-switch`，或从 [Releases](https://github.com/farion1231/cc-switch/releases) 下载 `.dmg`。
- Windows：从 [Releases](https://github.com/farion1231/cc-switch/releases) 下载 `.msi` 安装包或便携版 `.zip`。
- Linux：Arch 用 `paru -S cc-switch-bin`；其他发行版从 [Releases](https://github.com/farion1231/cc-switch/releases) 下载 `.deb` / `.rpm` / `.AppImage`。

### 添加供应商

1. 在 CC Switch 主界面顶部图标栏选中 Claude Code 橙色星形图标，点击右上角 **+** 进入**添加新供应商**，按下表填入配置后点击**添加**。

| 计费方案           | 配置信息                                                                                                                                                                      |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Token Plan 个人版 | 供应商名称：千问AI平台-Token Plan 个人版<br />API Key：[控制台获取](https://platform.qianwenai.com/home/api-keys)<br />请求地址：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| Token Plan 团队版 | 供应商名称：千问AI平台-Token Plan 团队版<br />API Key：[控制台获取](https://platform.qianwenai.com/home/api-keys)<br />请求地址：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| 按量计费           | 供应商名称：千问AI平台-按量计费<br />API Key：[控制台获取](https://platform.qianwenai.com/home/api-keys)<br />请求地址：`https://dashscope.aliyuncs.com/apps/anthropic`                            |

2. 展开**高级选项**配置模型映射，将主模型与 Haiku、Sonnet、Opus 默认模型填为对应方案[支持的模型](/token-plan/overview)。具体映射关系按需选择，例如：

   - 主模型：`qwen3.7-max`
   - Haiku 默认模型：`qwen3.6-flash`
   - Sonnet 默认模型：`qwen3.7-max`
   - Opus 默认模型：`qwen3.7-max`

3. 回到主界面，点击该供应商右侧**启用**按钮，然后新开一个 Claude Code 会话使配置生效。

### 接入 Claude Code 桌面版

Claude Code 桌面版（Claude Desktop）与 Claude Code CLI 是两个独立入口，在 CC Switch 中分别对应 **Claude Code** 与 **Claude Desktop** 面板。桌面版通过 CC Switch 本地网关访问千问AI平台：网关地址与鉴权令牌均由 CC Switch 自动写入桌面版配置，**无需在桌面版中手动填写千问AI平台 API Key**——千问AI平台 API Key 只在 CC Switch 供应商配置中填写，由本地路由转发时自动注入。

<Warning>
  请勿在桌面版的第三方推理配置中手动填写千问AI平台 API Key。桌面版对 CC Switch 本地网关（地址 `http://127.0.0.1:15721/claude-desktop`）的鉴权令牌由 CC Switch 自动生成并写入，手动填入千问AI平台 API Key 会因令牌不匹配导致鉴权失败。桌面版第三方配置写入目前仅支持 macOS、Windows。
</Warning>

1. 从 [Claude 下载页](https://claude.ai/download)安装 Claude Code 桌面版。

2. 在 CC Switch 左侧应用切换器切换到 **Claude Desktop** 面板。若未显示该入口，前往**设置 → 通用 → 应用可见性**确认 Claude Desktop 未被隐藏。

3. 添加千问AI平台供应商：若已在 **Claude Code** 面板配置过千问AI平台供应商，可点击**将 Claude Code 中已有的供应商导入**一键复用；也可点击右上角 **+** 新增。由于千问AI平台模型 ID（如 `qwen3.7-max`）不是 Claude Desktop 识别的 `claude-sonnet-* / claude-opus-* / claude-haiku-*` 三档角色 ID，需开启**需要模型映射**，为 Sonnet、Opus、Haiku 三档分别填写实际请求的千问AI平台模型（如 Sonnet → qwen3.7-max）。

4. 开启本地路由：前往**设置 → 路由 → 本地路由**，打开**在主页面显示本地路由开关**；回到 Claude Desktop 面板，打开 **Claude Desktop 本地路由**开关，监听地址默认 `127.0.0.1:15721`。

5. 在供应商卡片点击**启用**，CC Switch 会自动将第三方推理配置写入 Claude Code 桌面版。

6. 保持 CC Switch 运行，**完全退出并重启** Claude Code 桌面版后生效，在模型菜单中选择已配置的模型即可使用。

## 使用 Claude Code

1. 打开终端，并进入项目所在的目录。运行以下命令启动 Claude Code：

```bash
cd path/to/your_project
claude
```

2. 启动后，需要授权 Claude Code 执行文件。

3. 输入 `/status` 确认模型、Base URL、API Key 是否配置正确。

4. 在 Claude Code 中对话。

## 切换模型

- **启动 Claude Code 时切换**：在终端执行 `claude --model <模型名称>` 指定模型并启动 Claude Code，例如 `claude --model qwen3.7-max`。
- **会话期间**：在对话框输入 `/model <模型名称>` 命令切换模型，例如 `/model qwen3.7-max`。

## 接入图像生成模型

通过 Claude Code 的斜杠命令（Slash Command），可以调用 Token Plan 团队版的图像生成模型（qwen-image-2.0、wan2.7-image 等）。

### 步骤一：创建斜杠命令

在项目根目录创建 `.claude/commands/text-to-image.md`，写入以下内容：

````
调用 Token Plan 文生图 API，根据描述生成图像。

用户需求：$ARGUMENTS

## 执行步骤

1. 从用户需求中提取 prompt（图像描述）、model（默认 qwen-image-2.0）、size（默认 1024*1024）。

2. 调用 API 生成图像（使用 Bash 工具执行 curl）：

```
curl -s -X POST "https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "<模型>",
    "input": {
      "messages": [{"role":"user","content":[{"text":"<prompt>"}]}]
    },
    "parameters": {"size":"<尺寸>"}
  }'
```

3. 从返回 JSON 的 output.choices[*].message.content[*].image 提取图像 URL。

4. 用 curl -s -o "generated_$(date +%Y%m%d_%H%M%S).png" "<URL>" 下载到当前目录。

5. 向用户展示生成的图片文件路径。

## 可用模型

- qwen-image-2.0（默认）— 通用，擅长中文文本渲染
- qwen-image-2.0-pro — 质量更高
- wan2.7-image — 多风格，默认出 4 张
- wan2.7-image-pro — 支持 4K

## 可用尺寸

1024*1024、720*1280、1280*720。wan2.7-image-pro 额外支持 2048*2048。
````

### 步骤二：使用

在 Claude Code 中输入 `/text-to-image 画一只猫` 即可生成图片。

## 常见命令

| 命令              | 说明                                   | 示例                   |
| --------------- | ------------------------------------ | -------------------- |
| `/init`         | 在项目根目录生成 CLAUDE.md 文件，用于定义项目级指令和上下文。 | `/init`              |
| `/status`       | 查看当前模型、API Key、Base URL 等配置状态。       | `/status`            |
| `/model <模型名称>` | 切换模型。                                | `/model qwen3.7-max` |
| `/clear`        | 清除对话历史，开始全新对话。                       | `/clear`             |
| `/plan`         | 进入规划模式，仅分析和讨论方案，不修改代码。               | `/plan`              |
| `/compact`      | 压缩对话历史，释放上下文窗口空间。                    | `/compact`           |
| `/config`       | 打开配置菜单，可设置语言、主题等。                    | `/config`            |

更多命令与用法详情，请参考 [Claude Code 官方文档](https://code.claude.com/docs/en/overview)。

## 使用 IDE 插件

Claude Code IDE 插件支持在 VS Code、VS Code 系列 IDE（如 Cursor、Trae 等）、JetBrains 系列 IDE（如 IntelliJ IDEA、PyCharm 等）中使用。

<Tabs>
  <Tab title="VS Code">
    1. 请先完成[配置 Token Plan 团队版](#配置-token-plan-团队版)，Windows 还需要安装 WSL 或 [Git for Windows](https://git-scm.com/install/windows)。

    2. 打开 VS Code，在扩展市场中搜索 `Claude Code for VS Code` 并安装。

    3. 安装完成后，重启 VS Code。点击右上角图标进入 Claude Code 开始对话。

       若在对话时弹出 Anthropic 登录界面，说明尚未完成[配置 Token Plan 团队版](#配置-token-plan-团队版)，请先完成配置。

    4. 切换模型：参考[切换模型](#切换模型)完成配置后，在 IDE 插件中新建对话即可生效。
  </Tab>

  <Tab title="JetBrains">
    1. 请先完成[安装 Claude Code](#安装-claude-code) 和[配置 Token Plan 团队版](#配置-token-plan-团队版)。

    2. 打开 JetBrains（如 IntelliJ IDEA、PyCharm 等），在扩展市场中搜索 `Claude Code` 并安装。

    3. 安装后重启 IDE，点击右上角图标即可使用，可通过 `/model <模型名称>` 命令切换模型。

       若在对话时出现 `Not logged in. Please run /login` 报错，说明尚未完成[配置 Token Plan 团队版](#配置-token-plan-团队版)，请先完成配置。
  </Tab>
</Tabs>

## 常见问题

配置过程中遇到报错，参考对应套餐的常见问题文档：

- Token Plan 个人版：[Token Plan 常见问题](/token-plan/personal/token-plan-personal-faq)
- Token Plan 团队版：[Token Plan 团队版常见问题](/token-plan/faq)

### 报错 API Error: Unable to connect to API (ECONNRESET)

该错误由 Claude Code 客户端的网络连接问题引起，与配置无关，通常会自行恢复。建议：

1. 等待几分钟后重试。
2. 检查网络连接是否正常。
3. 如果使用了代理或 VPN，请关闭后重试。
4. 将 Claude Code 升级到最新版本：`npm install -g @anthropic-ai/claude-code@latest`。

### 报错 Unable to connect to Anthropic services. Failed to connect to api.anthropic.com: ERR\_BAD\_REQUEST

该错误表示 Claude Code 尝试连接 Anthropic 官方服务而非 Token Plan 团队版服务端，通常是因为环境变量未正确配置或未生效。请按以下步骤排查：

1. **检查配置文件**：确认 `~/.claude/settings.json` 中已正确配置 `ANTHROPIC_BASE_URL` 和 `ANTHROPIC_AUTH_TOKEN`。

```bash
# 查看当前配置
cat ~/.claude/settings.json
```

确认配置内容如下（请替换为实际 API Key）：

```json
{
    "env": {
        "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
        "ANTHROPIC_BASE_URL": "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic",
        "ANTHROPIC_MODEL": "qwen3.7-max",
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "qwen3.6-flash",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "qwen3.7-max",
        "ANTHROPIC_DEFAULT_OPUS_MODEL": "qwen3.7-max",
        "CLAUDE_CODE_SUBAGENT_MODEL": "qwen3.7-max"
    }
}
```

2. **检查环境变量是否冲突**：如果同时通过环境变量和配置文件设置了 `ANTHROPIC_BASE_URL`，请确保两者指向相同的 Token Plan 团队版地址，避免冲突。执行以下命令检查：

```bash
echo $ANTHROPIC_BASE_URL
```

如果输出为空或指向非 Token Plan 团队版地址，请清除该环境变量或将其设置为正确的 Token Plan 团队版 Base URL。

3. **确认 hasCompletedOnboarding**：检查 `~/.claude.json` 文件中 `hasCompletedOnboarding` 是否设置为 `true`，否则 Claude Code 启动时会尝试连接 Anthropic 官方服务进行登录验证。

4. **重新打开终端**：修改配置文件后，需要打开一个新的终端窗口，再执行 `claude` 命令以使配置生效。

5. **更新 Claude Code**：若以上步骤均无效，可能是 Claude Code 版本过旧导致。执行 `npm install -g @anthropic-ai/claude-code@latest` 更新到最新版本后重试。

### 使用旧版接口，切换模型不生效

如果之前使用旧版代理地址 `https://dashscope.aliyuncs.com/api/v2/apps/claude-code-proxy` 接入，该地址仅支持 `qwen3-coder-plus`，修改 `ANTHROPIC_MODEL` 不会切换模型。请迁移到新版配置（Token Plan 团队版或按量计费），使用本文档中的 Base URL 和配置方式。

### 使用 CC Switch 添加供应商时提示"未找到可用的模型列表端点"

该提示来自 CC Switch 保存供应商时的连通性检查——它会向配置的请求地址探测模型列表端点（如 `/v1/models`）。千问AI平台的 Anthropic 兼容接入端点（以 `/apps/anthropic` 结尾）仅提供对话端点 `/v1/messages`，不提供模型列表端点，该探测因此返回 404，CC Switch 据此提示"未找到可用的模型列表端点"。

**该提示不影响 Claude Code 正常使用，可忽略。** Claude Code 通过 `/v1/messages` 发起对话，所用模型由 CC Switch **高级选项**中的模型映射直接指定，不依赖模型列表端点的自动发现。请求地址与 API Key 配置正确时，直接点击**启用**并新开一个 Claude Code 会话即可正常对话。

若确实无法对话，请确认：请求地址以 `/apps/anthropic` 结尾、勿额外添加 `/v1`，并已在[高级选项的模型映射](#添加供应商)中填入对应套餐支持的模型。

## 最佳实践

### 1. 上下文管理

- **及时清理**：使用 `/clear` 定期重置对话，防止旧的上下文干扰新任务并节省 Token。
- **主动压缩**：使用 `/compact` 命令让 Claude 总结关键决策和修改的文件，保留核心记忆。
- **明确指定文件**：提问时使用 `@` 引用文件（如 `write a test for @auth.py`），避免模型无效扫描整个项目。
- **善用子代理（Sub-agents）**：对于大规模任务，让 Claude 启动子代理执行。子代理完成任务后返回精炼结论，保护主对话的上下文空间。

### 2. 先计划，再执行

- **启用 Plan 模式**：复杂任务前，先分析方案，不实际修改文件。提示词明确要求"先输出详细实施计划，经我确认后再修改文件"。
- **降低试错成本**：确保逻辑闭环后再进行代码变更。

### 3. 沉淀项目核心知识：编写 CLAUDE.md

- **包含关键信息**：每次会话启动时自动加载 CLAUDE.md，建议填入构建命令、代码规范及工作流等通用规则。
- **动态维护**：内容应简短易读，仅记录广泛适用的全局约定，并随项目演进持续补充新规则。

### 4. 扩展能力：MCP 与 Skills

- [**MCP**](https://code.claude.com/docs/en/mcp)：安装成熟的 MCP Server，连接外部服务。
- [**Skills**](https://code.claude.com/docs/en/skills)：编写详细的 Skill 描述文案。Claude 决定是否调用该工具，取决于对该工具用途的定义。
- **Skills vs MCP**：Skills 教会 Claude "怎么做"（工作流知识），MCP 给 Claude "做的工具"（外部接口）。两者互补，Skills 也可集成外部接口。

### 5. 自动化守护：Hooks

- [**使用 Hooks**](https://code.claude.com/docs/en/hooks)：Hooks 是确定性规则。它在 Claude 工作流的特定生命周期节点（如 PreToolUse 工具执行前校验等）自动运行本地脚本，确保关键校验或操作 100% 执行。
- **配置方式**：
  1. 运行 `/hooks` 进行交互式配置。
  2. 直接编辑 `.claude/settings.json`。
  3. 让 Claude 帮你编写，如："编写一个在每次文件编辑后运行 eslint 的 hook"。

### 6. 建立自检闭环

- **强制验证**：要求 Claude 修改代码后，必须运行相关的测试用例（如 `pytest` 或 `npm test`）。
- **定义成功标准**："修改完成后，请确保编译通过，并且运行 `curl` 命令验证 API 返回值为 200"。
- **视觉反馈**：前端修改时，要求 Claude 截取浏览器截图来确认 UI 效果。
