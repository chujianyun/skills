# Markdown 导出器

> 学习如何创建一个将对话导出为不同文档格式的插件

> 本文档由 AI 自动翻译。如有任何不准确之处，请参考 [英文原版](https://docs.dify.ai/en/develop-plugin/dev-guides-and-walkthroughs/develop-md-exporter.md)。

## 你将构建什么

你将构建一个实用的 Dify 插件，将对话导出为流行的文档格式。完成后，你的插件将能够：

* 将 markdown 文本转换为 Word 文档 (.docx)
* 将对话导出为 PDF 文件
* 处理文件创建并保持正确的格式
* 为文档导出提供简洁的用户体验

> [card] 所需时间
>
> 15 分钟

> [card] 前提条件
>
> 基本的 Python 知识和熟悉文档处理库

## 步骤 1：设置你的环境

**1. 安装 Dify 插件 CLI**

> [tab] Mac
>
> ```bash theme={null}
> brew tap langgenius/dify
> brew install dify
> ```

> [tab] Linux
>
> 从 [Dify GitHub releases 页面](https://github.com/langgenius/dify-plugin-daemon/releases) 获取最新的 Dify 插件 CLI。
>
> ```bash theme={null}
> # Download appropriate version
> chmod +x dify-plugin-linux-amd64
> mv dify-plugin-linux-amd64 dify
> sudo mv dify /usr/local/bin/
> ```

验证安装：

```bash theme={null}
dify version
```

**2. 创建插件项目**

初始化一个新的插件项目：

```bash theme={null}
dify plugin init
```

按照提示操作：

* **名称**：`md_exporter`
* **类型**：`tool`
* 按提示完成其余详细信息。

## 步骤 2：定义插件清单

创建 `manifest.yaml` 文件来定义你的插件元数据：

```yaml theme={null}
version: 0.0.4
type: plugin
author: your_username
label:
  en_US: Markdown Exporter
  zh_Hans: Markdown导出工具
created_at: "2025-09-30T00:00:00Z"
icon: icon.png

resource:
  memory: 134217728  # 128MB
  permission:
    storage:
      enabled: true  # We need storage for temp files

plugins:
  tools:
    - word_export.yaml
    - pdf_export.yaml

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

## 步骤 3：定义 Word 导出工具

创建一个 `word_export.yaml` 文件来定义 Word 文档导出工具：

```yaml theme={null}
identity:
  author: your_username
  name: word_export
  label:
    en_US: Export to Word
    zh_Hans: 导出为Word文档
description:
  human:
    en_US: Export conversation content to a Word document (.docx)
    zh_Hans: 将对话内容导出为Word文档(.docx)
  llm: >
    A tool that converts markdown text to a Word document (.docx) format.
    Use this tool when the user wants to save or export the conversation
    content as a Word document. The input text should be in markdown format.
credential_schema: {}  # No credentials needed
tool_schema:
  markdown_content:
    type: string
    required: true
    label:
      en_US: Markdown Content
      zh_Hans: Markdown内容
    human_description:
      en_US: The markdown content to convert to Word format
      zh_Hans: 要转换为Word格式的Markdown内容
  document_name:
    type: string
    required: false
    label:
      en_US: Document Name
      zh_Hans: 文档名称
    human_description:
      en_US: Name for the exported document (without extension)
      zh_Hans: 导出文档的名称（无需扩展名）
```

## 步骤 4：定义 PDF 导出工具

为 PDF 导出创建一个 `pdf_export.yaml` 文件：

```yaml theme={null}
identity:
  author: your_username
  name: pdf_export
  label:
    en_US: Export to PDF
    zh_Hans: 导出为PDF文档
description:
  human:
    en_US: Export conversation content to a PDF document
    zh_Hans: 将对话内容导出为PDF文档
  llm: >
    A tool that converts markdown text to a PDF document.
    Use this tool when the user wants to save or export the conversation
    content as a PDF file. The input text should be in markdown format.
credential_schema: {}  # No credentials needed
tool_schema:
  markdown_content:
    type: string
    required: true
    label:
      en_US: Markdown Content
      zh_Hans: Markdown内容
    human_description:
      en_US: The markdown content to convert to PDF format
      zh_Hans: 要转换为PDF格式的Markdown内容
  document_name:
    type: string
    required: false
    label:
      en_US: Document Name
      zh_Hans: 文档名称
    human_description:
      en_US: Name for the exported document (without extension)
      zh_Hans: 导出文档的名称（无需扩展名）
```

## 步骤 5：安装所需依赖

创建或更新 `requirements.txt` 并添加必要的库：

```text theme={null}
python-docx>=0.8.11
markdown>=3.4.1
weasyprint>=59.0
beautifulsoup4>=4.12.2
```

## 步骤 6：实现 Word 导出功能

在 `utils/docx_utils.py` 中创建一个实用工具模块：

```python utils/docx_utils.py theme={null}
import os
import tempfile
import uuid
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import markdown
from bs4 import BeautifulSoup

def convert_markdown_to_docx(markdown_text, document_name=None):
    """
    Convert markdown text to a Word document and return the file path
    """
    if not document_name:
        document_name = f"exported_document_{uuid.uuid4().hex[:8]}"

    # Convert markdown to HTML
    html = markdown.markdown(markdown_text)
    soup = BeautifulSoup(html, 'html.parser')

    # Create a new Word document
    doc = Document()

    # Process HTML elements and add to document
    for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'ul', 'ol']):
        if element.name == 'h1':
            heading = doc.add_heading(element.text.strip(), level=1)
            heading.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        elif element.name == 'h2':
            doc.add_heading(element.text.strip(), level=2)
        elif element.name == 'h3':
            doc.add_heading(element.text.strip(), level=3)
        elif element.name == 'h4':
            doc.add_heading(element.text.strip(), level=4)
        elif element.name == 'p':
            paragraph = doc.add_paragraph(element.text.strip())
        elif element.name in ('ul', 'ol'):
            for li in element.find_all('li'):
                doc.add_paragraph(li.text.strip(), style='ListBullet')

    # Create temp directory if it doesn't exist
    temp_dir = tempfile.gettempdir()
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Save the document
    file_path = os.path.join(temp_dir, f"{document_name}.docx")
    doc.save(file_path)

    return file_path
```

## 步骤 7：实现 PDF 导出功能

在 `utils/pdf_utils.py` 中创建一个实用工具模块：

```python utils/pdf_utils.py theme={null}
import os
import tempfile
import uuid
import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

def convert_markdown_to_pdf(markdown_text, document_name=None):
    """
    Convert markdown text to a PDF document and return the file path
    """
    if not document_name:
        document_name = f"exported_document_{uuid.uuid4().hex[:8]}"

    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_text)

    # Add basic styling
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{document_name}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
            h1 {{ text-align: center; color: #333; }}
            h2, h3, h4 {{ color: #444; margin-top: 20px; }}
            p {{ margin-bottom: 15px; }}
            ul, ol {{ margin-left: 20px; }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # Create temp directory if it doesn't exist
    temp_dir = tempfile.gettempdir()
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Output file path
    file_path = os.path.join(temp_dir, f"{document_name}.pdf")

    # Configure fonts
    font_config = FontConfiguration()

    # Render PDF
    HTML(string=styled_html).write_pdf(
        file_path,
        stylesheets=[],
        font_config=font_config
    )

    return file_path
```

## 步骤 8：创建工具实现

首先，在 `tools/word_export.py` 中创建 Word 导出工具：

```python tools/word_export.py theme={null}
import os
import base64
from collections.abc import Generator
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from utils.docx_utils import convert_markdown_to_docx

class WordExportTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # Extract parameters
        markdown_content = tool_parameters.get("markdown_content", "")
        document_name = tool_parameters.get("document_name", "exported_document")

        if not markdown_content:
            yield self.create_text_message("Error: No content provided for export.")
            return

        try:
            # Convert markdown to Word
            file_path = convert_markdown_to_docx(markdown_content, document_name)

            # Read the file as binary
            with open(file_path, 'rb') as file:
                file_content = file.read()

            # Encode as base64
            file_base64 = base64.b64encode(file_content).decode('utf-8')

            # Return success message and file
            yield self.create_text_message(
                f"Document exported successfully as Word (.docx) format."
            )

            yield self.create_file_message(
                file_name=f"{document_name}.docx",
                file_content=file_base64,
                mime_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        except Exception as e:
            yield self.create_text_message(f"Error exporting to Word: {str(e)}")
            return
```

接下来，在 `tools/pdf_export.py` 中创建 PDF 导出工具：

```python tools/pdf_export.py theme={null}
import os
import base64
from collections.abc import Generator
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from utils.pdf_utils import convert_markdown_to_pdf

class PDFExportTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # Extract parameters
        markdown_content = tool_parameters.get("markdown_content", "")
        document_name = tool_parameters.get("document_name", "exported_document")

        if not markdown_content:
            yield self.create_text_message("Error: No content provided for export.")
            return

        try:
            # Convert markdown to PDF
            file_path = convert_markdown_to_pdf(markdown_content, document_name)

            # Read the file as binary
            with open(file_path, 'rb') as file:
                file_content = file.read()

            # Encode as base64
            file_base64 = base64.b64encode(file_content).decode('utf-8')

            # Return success message and file
            yield self.create_text_message(
                f"Document exported successfully as PDF format."
            )

            yield self.create_file_message(
                file_name=f"{document_name}.pdf",
                file_content=file_base64,
                mime_type="application/pdf"
            )

        except Exception as e:
            yield self.create_text_message(f"Error exporting to PDF: {str(e)}")
            return
```

## 步骤 9：创建入口点

在项目根目录创建一个 `main.py` 文件：

```python main.py theme={null}
from dify_plugin import PluginRunner
from tools.word_export import WordExportTool
from tools.pdf_export import PDFExportTool

plugin = PluginRunner(
    tools=[
        WordExportTool(),
        PDFExportTool(),
    ],
    providers=[]  # No credential providers needed
)
```

## 步骤 10：测试你的插件

**1. 设置你的调试环境**

首先，从模板创建你的 `.env` 文件：

```bash theme={null}
cp .env.example .env
```

使用你的 Dify 环境详细信息进行配置：

```dotenv theme={null}
INSTALL_METHOD=remote
REMOTE_INSTALL_URL=debug-plugin.dify.dev:5003
REMOTE_INSTALL_KEY=your_debug_key
```

**2. 安装依赖**

```bash theme={null}
pip install -r requirements.txt
```

**3. 以调试模式启动插件**

```bash theme={null}
python -m main
```

## 步骤 11：打包分发

当你准备好分享你的插件时：

```bash theme={null}
dify plugin package ./
```

这将创建一个 `plugin.difypkg` 文件用于分发。

## 创意用例

> [card] 报告生成
>
> 使用此插件将分析摘要转换为专业报告提供给客户

> [card] 会话文档
>
> 将辅导或咨询会话笔记导出为格式化文档

## 超越基础

以下是一些扩展此插件的有趣方式：

* **自定义模板**：添加公司品牌或个性化样式。
* **多格式支持**：扩展导出为 HTML、Markdown 或其他格式。
* **图像处理**：处理并包含对话中的图像。
* **表格支持**：为数据表格实现正确的格式化。
* **协作编辑**：添加与 Google Docs 或类似平台的集成。

> [accordion] 技术见解
>
> 文档转换的核心挑战是保持格式和结构。此插件先将 markdown 转换为 HTML 作为中间格式，再将该 HTML 处理为目标格式。
>
> 这个两步流程带来了灵活性：只需添加基于 HTML 表示的新输出模块，即可支持更多格式。
>
> PDF 生成使用 WeasyPrint，因为它提供支持 CSS 的高质量 PDF 渲染。Word 文档则由 python-docx 提供对文档结构的精细控制。

## 总结

你已经构建了一个实用的插件，让用户能以专业文档格式导出对话，弥合 AI 对话与传统文档工作流之间的差距。

> [card] 文档
>
> 用英语 (en\_US) 编写你的 README.md，描述功能、设置和使用示例

> [card] 本地化
>
> 为其他语言创建额外的 README 文件，如 `readme/README_zh_Hans.md`

如果发布你的插件，请添加隐私政策 (PRIVACY.md)

在文档中包含全面的示例

使用各种文档大小和格式进行彻底测试
