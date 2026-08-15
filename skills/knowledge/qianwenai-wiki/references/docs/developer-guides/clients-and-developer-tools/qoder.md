> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Qoder

> 在 Qoder 中使用千问AI平台模型

Qoder 是面向软件开发的 Agentic 编码平台，支持桌面 IDE、CLI 和 JetBrains 插件，可以通过 Token Plan 个人版、Token Plan 团队版或按量付费接入千问AI平台。

## Qoder IDE

### 安装

1. 前往 [Qoder 官网](https://qoder.com/)下载并安装 Qoder。
2. 初次启动后完成初始配置并登录 Qoder 账号。

### 配置接入凭证

1. 在界面右上角打开 Qoder 设置，选择**模型**，点击**添加**。

2. 模型配置信息如下：

| 配置项     | 说明                                                                                                                                           |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| 提供商     | 在下拉菜单中选择 **千问AI平台 - 中国**                                                                                                                     |
| 类型      | 根据计费方案选择 **Token Plan**（个人版或团队版）或**按量付费**                                                                                                    |
| 模型      | 在下拉菜单中选择模型                                                                                                                                   |
| API Key | 填写 Token Plan 个人版或团队版专属 [API Key](https://platform.qianwenai.com/home/api-keys) 或千问AI平台 [API Key](/developer-guides/administration/api-keys) |

   <Note>
     仅支持文本生成类模型（如 qwen3.6-plus、glm-5 等）。
   </Note>

3. 点击**添加**，通过校验后即可完成模型配置。

4. 在模型列表中选择对应模型即可开始使用。

## Qoder CLI

### 安装

1. 在终端执行以下命令安装。

```bash
curl -fsSL https://qoder.com/install | bash
```

2. 验证安装是否成功。

```bash
qodercli --version
```

若输出版本号，则安装成功。

### 登录 Qoder

使用前需完成身份验证，有两种方式：

1. **通过 TUI 登录（推荐）**

   1. 执行 `qodercli` 进入交互界面，在对话框中输入 `/login`。
   2. 选择 `login with browser` 或 `login with qoder personal access token` 完成登录。

2. **通过环境变量登录**

   适用于非交互式环境（如 CI/CD 流水线）。将 `your_personal_access_token_here` 替换为实际的 Token，可在[服务集成页面](https://qoder.com/account/integrations)获取。

<Tabs>
  <Tab title="macOS/Linux">
    ```bash
    export QODER_PERSONAL_ACCESS_TOKEN="REDACTED"
    ```
  </Tab>

  <Tab title="Windows">
    ```bash
    set QODER_PERSONAL_ACCESS_TOKEN=your_personal_access_token_here
    ```
  </Tab>
</Tabs>

### 配置接入凭证

1. 在对话框中输入 `/model`，通过 Tab 键切换至 `Custom`。
2. 回车选择 Add custom model，提供商选择 **Alibaba Cloud Model Studio - China**，类型根据计费方案选择 **Token Plan**（个人版或团队版）或**按量付费**。
3. 选择模型后输入对应方案的专属 API Key，确认后等待配置生效。

<Note>
  仅支持文本生成类模型（如 qwen3.6-plus、glm-5 等）。
</Note>

### 使用 Qoder CLI

1. 重启 Qoder CLI。

```bash
qodercli
```

2. 在对话框中输入 `/model`，通过 Tab 键切换至 `Custom`，选择对应模型即可开始使用。

## JetBrains 插件

1. 打开 JetBrains IDE（如 IntelliJ IDEA、PyCharm 等），在扩展市场中搜索 `Qoder` 并安装。

2. 点击右侧导航栏中的 Qoder，在 Qoder 对话面板中完成登录。

3. 点击右上角设置，选择**插件设置**，在弹出界面选择**添加模型**。

4. 配置信息如下：

| 配置项     | 说明                                                                                                                                           |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| 提供商     | 在下拉菜单中选择 **千问AI平台 - 中国**                                                                                                                     |
| 类型      | 根据计费方案选择 **Token Plan**（个人版或团队版）或**按量付费**                                                                                                    |
| 模型      | 在下拉菜单中选择模型                                                                                                                                   |
| API Key | 填写 Token Plan 个人版或团队版专属 [API Key](https://platform.qianwenai.com/home/api-keys) 或千问AI平台 [API Key](/developer-guides/administration/api-keys) |

   <Note>
     仅支持文本生成类模型（如 qwen3.6-plus、glm-5 等）。
   </Note>

   配置完成后，点击**确定**，等待配置生效。

5. 在自定义模型中选择对应模型进行对话。

## 了解更多

如需进一步了解 Qoder 的智能体、MCP、Skills 等扩展能力，请参考 [Qoder 官方文档](https://docs.qoder.com/)。

## 常见问题

### 错误码

配置过程中遇到报错，请参考对应计费方案的常见问题文档：

- 按量付费：[错误码排查](/api-reference/preparation/error-messages)
- Token Plan 个人版：[Token Plan 个人版常见问题](/token-plan/faq)
- Token Plan 团队版：[Token Plan 团队版常见问题](/token-plan/faq)

### 为什么在 Qoder 设置中找不到模型选项？

可能有以下原因：

- **未完成登录**：需要先完成登录，才能进行对话和配置模型。
- **当前版本不支持**：建议更新至最新版本（0.16.0 及以上）。

### 接入 Token Plan 团队版后仍然提示"您已达到配额上限"怎么办？

**原因**：配置完成后未切换到 Token Plan 团队版模型，仍在使用 Qoder 内置模型，触发了 Qoder 的配额限制。

**解决方法**：切换到**自定义模型**，然后选择对应的模型。
