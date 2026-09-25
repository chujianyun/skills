# Wiki 抓取与转换协议

本协议用于建立可验证的完整语料。目标不是“抓到很多页面”，而是证明 Wiki 范围内的每个导航文档都有唯一来源、唯一落盘路径和可读取的 Markdown。

## 1. 划定范围

先记录：

- Wiki 的规范根 URL、产品或知识域名称、目标语言
- 用户明确包含或排除的子站、版本、语言、API Reference、博客、更新日志
- 访问方式和许可证；需要登录时只使用用户已有的授权会话，不导出 Cookie、Token 或签名 URL

多语言或多版本站点默认只抓用户提供链接所在的语言和版本。不要把不同版本混进同一目录；用户要求多版本时，在顶层按版本分目录。

## 2. 建立导航地图

按以下优先级发现页面，结果合并后用 canonical URL 去重：

1. 官方导出、官方文档源码仓库或官方提供的完整 Markdown / `llms-full.txt`
2. Wiki 自身的桌面端导航树、目录页和面包屑
3. `sitemap.xml`、`llms.txt`、站内搜索索引或公开 API
4. 动态站点的可渲染浏览器

搜索引擎结果只能用于发现遗漏，不能作为完整性依据。先形成完整导航树并计算范围内 `discovered` 数量，再逐页抓取。

目录对应导航分组，文档对应 Markdown 文件：

- 使用 Wiki 展示标题起可读文件名，保留中文和稳定产品术语，不直接使用 URL 编码串。
- 默认把分组落成文件夹；分组自身有正文时用该目录下的 `index.md` 保存。
- 去掉文件系统不安全字符，避免尾随空格和点；同级重名时添加最短的语义限定词。
- 同一页面被多个导航入口引用时只保存一份，其他入口通过本地相对链接指向它。
- `local_path` 始终使用 `/`，相对于 staging 的 `docs/`，并以 `.md` 结尾。

## 3. 转换正文

每页 Markdown 至少保留：

- 页面标题和原有标题层级
- 正文段落、列表、表格、代码块、公式、引用、告警和步骤
- 折叠区、标签页和分页代码示例；用二级或三级标题展开，避免隐藏内容丢失
- 对理解内容必要的图片、图表和附件

移除站点导航、页眉页脚、Cookie 横幅、推荐卡片、广告、点赞按钮和重复目录。不要写入抓取时间、构建 ID、随机 DOM ID 等易变信息。

内部文档链接要根据完整 URL→`local_path` 映射改写为相对 Markdown 链接；锚点尽量保留。外部链接保留绝对 URL。承载信息的图片下载到 staging 的 `assets/` 并改写为相对路径；装饰图可忽略。代码块必须保留语言标记。

文档正文不需要重复写来源 URL；来源、路径和哈希统一记录在清单中。若保留页面元数据，只能保留稳定字段。

## 4. 临时目录与 inventory

使用 `mktemp -d` 创建临时目录，不要把中间抓取物留在用户工作区。结构：

```text
<staging>/
├── inventory.json
├── docs/
│   └── <wiki navigation tree>/*.md
└── assets/
    └── <stable relative paths>
```

`inventory.json` 示例：

```json
{
  "schema_version": 1,
  "source_root": "https://docs.example.com/zh",
  "coverage": {
    "discovered": 2,
    "captured": 2,
    "failed": [],
    "excluded": [
      {
        "url": "https://docs.example.com/en",
        "reason": "different language"
      }
    ]
  },
  "pages": [
    {
      "title": "快速开始",
      "source_url": "https://docs.example.com/zh/getting-started",
      "source_path": "/zh/getting-started",
      "local_path": "快速入门/快速开始.md",
      "summary": "安装并完成第一次运行",
      "keywords": ["安装", "quickstart"]
    },
    {
      "title": "配置",
      "source_url": "https://docs.example.com/zh/configuration",
      "source_path": "/zh/configuration",
      "local_path": "配置/index.md"
    }
  ],
  "assets": [
    {
      "source_url": "https://docs.example.com/assets/architecture.png",
      "local_path": "架构/architecture.png"
    }
  ]
}
```

`captured` 必须等于 `pages` 数量，`discovered` 必须等于成功页数加失败页数。`failed` 中记录 URL、错误类型和最后一次尝试结果；`excluded` 只记录明确在范围外的页面及理由。资产不计入页面覆盖数。

## 5. 完整性门槛

在构建或更新前检查：

1. `failed` 为空，`discovered == captured == len(pages)`。
2. 每个页面文件存在、非空、标题与来源对应。
3. URL 和 `local_path` 各自唯一，没有 `../`、绝对路径或目录逃逸。
4. 随机抽查首页、最深层页面、代码页、表格页和含图片页面。
5. 用导航树、站点地图或官方源文件总数进行第二次交叉核对。

同一页面最多重试两次；若大量页面遇到相同限流或鉴权错误，停止批量重试并报告阻塞。只有用户明确接受部分快照时才可使用同步脚本的 `--allow-partial`，且生成 Skill 必须在 `SOURCE.md` 和最终报告中标为不完整。
