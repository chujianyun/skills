# Flomo 工具（10分钟）

> 在大约十分钟内端到端构建一个连接 Flomo 笔记服务的功能性 Dify 工具插件

> 本文档由 AI 自动翻译。如有任何不准确之处，请参考 [英文原版](https://docs.dify.ai/en/develop-plugin/dev-guides-and-walkthroughs/develop-flomo-plugin.md)。

## 你将构建什么

完成本指南后，你将创建一个 Dify 插件，它能够：

* 连接到 Flomo 笔记 API
* 允许用户将 AI 对话中的笔记直接保存到 Flomo
* 正确处理身份验证和错误状态
* 准备好在 Dify Marketplace 中分发

> [card] 所需时间
>
> 10 分钟

> [card] 前置条件
>
> 基本的 Python 知识和一个 Flomo 账户

## 步骤 1：安装 Dify 插件 CLI 并创建项目

**1. 安装 Dify 插件 CLI**

> [tab] Mac
>
> ```bash theme={null}
> brew tap langgenius/dify
> brew install dify
> ```

> [tab] Linux
>
> 从 [Dify Plugin Daemon releases 页面](https://github.com/langgenius/dify-plugin-daemon/releases) 下载最新的二进制文件。x86\_64 选择 `dify-plugin-linux-amd64`，ARM 选择 `dify-plugin-linux-arm64`。
>
> ```bash theme={null}
> chmod +x dify-plugin-linux-amd64
> sudo mv dify-plugin-linux-amd64 /usr/local/bin/dify
> ```

验证安装：

```bash theme={null}
dify version
```

**2. 初始化插件项目**

使用以下命令创建新的插件项目：

```bash theme={null}
dify plugin init
```

按照提示设置你的插件：

* 将其命名为 `flomo`
* 选择 `tool` 作为插件类型
* 完成其余必填字段

**3. 导航到项目目录**

```bash theme={null}
cd flomo
```

该项目包含你的插件的基本结构，以及所有必要的文件。

## 步骤 2：定义插件清单

> [!NOTE]
>
> `manifest.yaml` 文件定义了插件的元数据、权限和功能。

创建 `manifest.yaml` 文件：

```yaml theme={null}
version: 0.0.4
type: plugin
author: yourname
label:
  en_US: Flomo
  zh_Hans: Flomo 浮墨笔记
created_at: "2023-10-01T00:00:00Z"
icon: icon.png

resource:
  memory: 67108864  # 64MB
  permission:
    storage:
      enabled: false

plugins:
  tools:
    - provider/flomo.yaml

meta:
  version: 0.0.1
  arch:
    - amd64
    - arm64
  runner:
    language: python
    version: 3.12
    entrypoint: main
```

## 步骤 3：创建工具定义

工具插件使用两个 YAML 文件：一个 **provider** 文件用于声明凭证并列出工具，以及每个可调用工具对应一个 **tool** 文件。完整的 schema 请参阅[通用规范](../../%E7%89%B9%E6%80%A7%E4%B8%8E%E8%A7%84%E8%8C%83/%E6%8F%92%E4%BB%B6%E7%B1%BB%E5%9E%8B/%E9%80%9A%E7%94%A8%E8%A7%84%E8%8C%83.md)。

创建 `provider/flomo.yaml`：

```yaml theme={null}
identity:
  author: yourname
  name: flomo
  label:
    en_US: Flomo Note
    zh_Hans: Flomo 浮墨笔记
  description:
    en_US: Add notes to your Flomo account directly from Dify.
    zh_Hans: 直接从 Dify 添加笔记到您的 Flomo 账户。
  icon: icon.png
credentials_for_provider:
  api_url:
    type: secret-input
    required: true
    label:
      en_US: API URL
      zh_Hans: API URL
    placeholder:
      en_US: https://flomoapp.com/iwh/{token}/{secret}/
    help:
      en_US: Flomo API URL from your Flomo account settings.
      zh_Hans: 从您的 Flomo 账户设置中获取的 API URL。
tools:
  - tools/flomo.yaml
extra:
  python:
    source: provider/flomo.py
```

创建 `tools/flomo.yaml`：

```yaml theme={null}
identity:
  name: flomo
  author: yourname
  label:
    en_US: Save to Flomo
    zh_Hans: 保存到 Flomo
description:
  human:
    en_US: Save the conversation content as a Flomo note.
    zh_Hans: 将对话内容保存为 Flomo 笔记。
  llm: >
    Saves content to the user's Flomo account. Use this tool when the user
    asks to save, capture, or remember the current message. Takes a single
    `content` parameter containing the text to save.
parameters:
  - name: content
    type: string
    required: true
    label:
      en_US: Note content
      zh_Hans: 笔记内容
    human_description:
      en_US: Content to save as a note in Flomo.
      zh_Hans: 要保存为 Flomo 笔记的内容。
    llm_description: The text to save as a Flomo note.
    form: llm
extra:
  python:
    source: tools/flomo.py
```

## 步骤 4：实现核心工具函数

在 `utils/flomo_utils.py` 中创建用于 API 交互的工具模块：

```python utils/flomo_utils.py theme={null}
import requests

def send_flomo_note(api_url: str, content: str) -> None:
    """
    Send a note to Flomo via the API URL. Raises requests.RequestException on network errors,
    and ValueError on invalid status codes or input.
    """
    api_url = api_url.strip()
    if not api_url:
        raise ValueError("API URL is required and cannot be empty.")
    if not api_url.startswith('https://flomoapp.com/iwh/'):
        raise ValueError(
            "API URL should be in the format: https://flomoapp.com/iwh/{token}/{secret}/"
        )
    if not content:
        raise ValueError("Content cannot be empty.")

    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_url, json={"content": content}, headers=headers, timeout=10)

    if response.status_code != 200:
        raise ValueError(f"API URL is not valid. Received status code: {response.status_code}")
```

## 步骤 5：实现工具提供者

工具提供者处理凭证验证。创建 `provider/flomo.py`：

```python provider/flomo.py theme={null}
from typing import Any
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
import requests
from utils.flomo_utils import send_flomo_note

class FlomoProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            api_url = credentials.get('api_url', '').strip()
            # Use utility for validation and sending test note
            send_flomo_note(api_url, "Hello, #flomo https://flomoapp.com")
        except ValueError as e:
            raise ToolProviderCredentialValidationError(str(e))
        except requests.RequestException as e:
            raise ToolProviderCredentialValidationError(f"Connection error: {str(e)}")
```

## 步骤 6：实现工具

工具类处理用户调用插件时的实际 API 调用。创建 `tools/flomo.py`：

```python tools/flomo.py theme={null}
from collections.abc import Generator
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
import requests
from utils.flomo_utils import send_flomo_note

class FlomoTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        content = tool_parameters.get("content", "")
        api_url = self.runtime.credentials.get("api_url", "")

        try:
            send_flomo_note(api_url, content)
        except ValueError as e:
            yield self.create_text_message(str(e))
            return
        except requests.RequestException as e:
            yield self.create_text_message(f"Connection error: {str(e)}")
            return

        # Return success message and structured data
        yield self.create_text_message(
            "Note created successfully! Your content has been sent to Flomo."
        )
        yield self.create_json_message({
            "status": "success",
            "content": content,
        })
```

> [!WARNING]
>
> 始终优雅地处理异常并返回用户友好的错误消息。请记住，你的插件代表着你在 Dify 生态系统中的品牌形象。

## 步骤 7：测试你的插件

**1. 设置调试环境**

复制示例环境文件：

```bash theme={null}
cp .env.example .env
```

使用你的 Dify 环境详情编辑 `.env` 文件：

```bash theme={null}
INSTALL_METHOD=remote
REMOTE_INSTALL_URL=debug-plugin.dify.dev:5003
REMOTE_INSTALL_KEY=your_debug_key
```

你可以在 Dify 仪表板中找到你的调试 URL 和密钥：点击右上角的**插件**图标，然后点击调试图标。复制 **API Key** 和 **Host Address**（主机地址已包含端口）。

**2. 安装依赖并运行**

```bash theme={null}
pip install -r requirements.txt
python -m main
```

你的插件将以调试模式连接到你的 Dify 实例。

**3. 测试功能**

在你的 Dify 实例中，打开 **插件** 页面并找到你的插件（标记为 **debugging** ）。添加你的 Flomo API 凭证并测试发送笔记。

## 步骤 8：打包和分发

当你准备好分享你的插件时：

```bash theme={null}
dify plugin package ./
```

这将创建一个 `plugin.difypkg` 文件，你可以将其上传到 Dify Marketplace。

## 常见问题和故障排除

**常见问题和故障排除**

> [accordion] 插件在调试模式下不显示
>
> 确保你的 `.env` 文件配置正确，并且你使用的是正确的调试密钥。

> [accordion] API 身份验证错误
>
> 仔细检查你的 Flomo API URL 格式。它应该是这种形式：`https://flomoapp.com/iwh/{token}/{secret}/`

> [accordion] 打包失败
>
> 确保所有必需的文件都存在，并且 `manifest.yaml` 结构有效。

## 总结

你已经构建了一个连接外部 API 服务的功能性 Dify 插件。这种相同的模式适用于与数千种服务的集成，从数据库、搜索引擎到生产力工具和自定义 API。

> [card] 文档
>
> 用英文（en\_US）编写你的 `README.md`，描述功能、设置和使用示例

> [card] 本地化
>
> 为其他语言创建额外的 README 文件，如 `readme/README_zh_Hans.md`

如果发布你的插件，请添加隐私政策（PRIVACY.md）

在文档中包含全面的示例

使用各种文档大小和格式进行全面测试
