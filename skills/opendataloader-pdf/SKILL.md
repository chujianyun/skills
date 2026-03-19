---
name: opendataloader-pdf
description: PDF 数据提取工具。当用户提到"PDF 提取"、"PDF 转 Markdown"、"PDF 解析"、"提取 PDF 内容"、"PDF 转 JSON"、"RAG PDF"时使用。OpenDataLoader PDF 是目前基准测试第一的 PDF 解析器，支持本地模式（快速、确定）和混合 AI 模式（复杂表格、扫描件、公式），输出 Markdown、JSON（带边界框）、HTML。适用于需要从 PDF 提取结构化数据用于 RAG/LLM pipeline，或需要批量处理 PDF 文档的场景。
updated_at: 2026-03-19
---

# OpenDataLoader PDF

**PDF 解析器 · 基准测试第一 · RAG/LLM 数据提取利器**

## 功能定位

- **核心能力**：从任意 PDF 提取结构化数据（Markdown、JSON、HTML），带边界框坐标
- **技术亮点**：XY-Cut++ 读取顺序、Bounding Box 定位、AI 混合模式处理复杂页面
- **基准成绩**：综合 0.90（第一），表格 0.93，读取顺序 0.94（对标 Docling、Marker、MinerU 等）
- **许可证**：Apache 2.0（核心功能免费）

## 适用场景

- 批量提取 PDF 为 Markdown / JSON / HTML 用于 RAG 或 LLM 训练
- 需要边界框坐标做源码溯源（哪个段落来自 PDF 第几页哪个位置）
- 复杂表格、扫描件、含公式的学术 PDF
- PDF 无障碍化（Tagged PDF 生成，Q2 2026 免费开放）

## 安装

### 前提

- Java 11+
- Python 3.10+

```bash
pip install -U opendataloader-pdf
```

混合 AI 模式（复杂表格 / OCR / 公式）：

```bash
pip install "opendataloader-pdf[hybrid]"
```

## 快速使用

### CLI（适合单文件或批量）

```bash
# 快速模式：输出 Markdown + JSON
opendataloader-pdf input.pdf output_dir/

# 指定格式
opendataloader-pdf input.pdf output_dir/ --format markdown,json,html

# 混合 AI 模式（复杂表格 / 扫描件）
opendataloader-pdf --hybrid docling-fast input.pdf output_dir/

# 混合模式 + OCR（扫描件）
opendataloader-pdf --hybrid docling-fast --force-ocr input.pdf output_dir/

# 混合模式 + 公式识别
opendataloader-pdf --hybrid docling-fast --hybrid-mode full input.pdf output_dir/
```

### Python API

```python
import opendataloader_pdf

# 批量处理（一次调用会启动 JVM，建议批量一次性传入）
opendataloader_pdf.convert(
    input_path=["file1.pdf", "file2.pdf", "folder/"],
    output_dir="output/",
    format="markdown,json"
)
```

## 模式选择指南

| 文档类型 | 模式 | 命令 |
|---------|------|------|
| 标准数字 PDF | 快速（默认） | `opendataloader-pdf file.pdf out/` |
| 复杂/无线框表格 | 混合 | `opendataloader-pdf --hybrid docling-fast file.pdf out/` |
| 扫描件 | 混合 + OCR | 同上 + `--force-ocr` |
| 非英语扫描件 | 混合 + OCR | `--force-ocr --ocr-lang "ko,en"` |
| 含数学公式 | 混合 + 公式 | `--hybrid docling-fast --hybrid-mode full` |
| 图表需要描述 | 混合 + 图片描述 | `--enrich-picture-description --hybrid-mode full` |

## 输出格式说明

### Markdown
保留标题层级、表格结构、列表嵌套，适合直接用于 chunking。

### JSON（带边界框）
```json
{
  "pages": [{
    "page_number": 1,
    "elements": [{
      "type": "heading",
      "text": "...",
      "bbox": [x0, y0, x1, y1],
      "level": 1
    }, {
      "type": "table",
      "bbox": [x0, y0, x1, y1],
      "html": "..."
    }]
  }]
}
```

每个元素都有 `bbox` 坐标，方便做源码溯源。

### HTML
保留布局结构，适合渲染或进一步处理。

## Gotchas

- **每次 `convert()` 调用会启动一个新的 JVM 进程**，所以批量文件建议一次传入，而不是循环多次调用
- 混合模式需要在后台启动服务器：`opendataloader-pdf-hybrid --port 5002`，然后客户端加 `--hybrid docling-fast`
- `--enrich-formula` 或 `--enrich-picture-description` 必须在混合服务器和客户端都加 `--hybrid-mode full`，否则强化功能静默跳过
- Java 选项修改后必须运行 `npm run sync`，它会重新生成 `options.json` 和所有 Python/Node.js 绑定

## 与其他工具的对比

| 引擎 | 综合分 | 表格 | 速度（秒/页） |
|------|--------|------|--------------|
| **opendataloader（混合）** | **0.90** | **0.93** | 0.43 |
| docling | 0.86 | 0.89 | 0.73 |
| marker | 0.83 | 0.81 | 53.93 |
| mineru | 0.82 | 0.87 | 5.96 |
| pymupdf4llm | 0.57 | 0.40 | 0.09 |

## 引用信息

- PyPI：`pip install opendataloader-pdf`
- npm：`npm install @opendataloader/pdf`
- Maven：`org.opendataloader:opendataloader-pdf-core`
- GitHub：https://github.com/opendataloader-project/opendataloader-pdf
- 基准测试：https://github.com/opendataloader-project/opendataloader-bench
