# Palantir Ontology 文档索引

本文件由 `scripts/sync_wiki_docs.py` 生成。日常问答优先运行 `scripts/search_docs.py`，需要浏览主题结构时再读取本索引。

- 来源：<https://www.palantir.com/docs/zh/foundry/ontology/overview>
- 文档数：316

## 顶层目录

- `(root)`：5 篇
- `定义本体`：133 篇
- `应用`：159 篇
- `本体架构`：19 篇

## 目录树

```text
docs/
├── 定义本体
│   ├── 函数
│   │   ├── Functions called through the API gateway
│   │   │   └── 查询.md
│   │   ├── Functions on objects
│   │   │   ├── API- Object和链接.md
│   │   │   ├── API- 附件.md
│   │   │   ├── API：媒体.md
│   │   │   ├── API：对象集.md
│   │   │   ├── Object标识符.md
│   │   │   ├── 入门.md
│   │   │   ├── 创建自定义聚合.md
│   │   │   ├── 导入Object和链接类型.md
│   │   │   └── 概述.md
│   │   ├── Models and graphs
│   │   │   └── 创建模型函数.md
│   │   ├── Ontology edits
│   │   │   ├── API- Ontology编辑.md
│   │   │   ├── 为新Objects生成唯一ID.md
│   │   │   ├── 抛出用户界面错误.md
│   │   │   └── 概述.md
│   │   ├── Performance and limits
│   │   │   ├── 优化性能.md
│   │   │   └── 强制限制.md
│   │   ├── Python functions
│   │   │   ├── Ontology 更改.md
│   │   │   ├── 从Python函数进行API调用.md
│   │   │   ├── 在Pipeline Builder中使用Python函数.md
│   │   │   ├── 在Workshop中使用Python函数.md
│   │   │   ├── 对象上的函数.md
│   │   │   ├── 类型参考.md
│   │   │   ├── 起始步骤.md
│   │   │   └── 高级用法.md
│   │   ├── Semantic search
│   │   │   ├── PDF处理.md
│   │   │   ├── 使用Palantir提供的模型创建语义搜索工作流.md
│   │   │   ├── 使用自定义模型创建语义搜索工作流.md
│   │   │   ├── 分块.md
│   │   │   └── 概述.md
│   │   ├── TypeScript basics
│   │   │   ├── 处理未定义值.md
│   │   │   ├── 添加 npm 依赖项.md
│   │   │   ├── 装饰器.md
│   │   │   ├── 调试函数.md
│   │   │   └── 输入和输出类型.md
│   │   ├── Unit testing
│   │   │   ├── 入门指南.md
│   │   │   ├── 创建存根对象.md
│   │   │   ├── 存根对象搜索和聚合.md
│   │   │   ├── 模拟日期、时间戳和UUID.md
│   │   │   ├── 模拟用户和组.md
│   │   │   ├── 调试.md
│   │   │   └── 验证Ontology编辑.md
│   │   ├── 入门.md
│   │   ├── 函数中的外部来源.md
│   │   ├── 函数中的语言模型.md
│   │   ├── 在平台中使用函数.md
│   │   ├── 将函数添加到 Marketplace 产品.md
│   │   ├── 将资源导入代码库.md
│   │   ├── 权限.md
│   │   ├── 概述.md
│   │   ├── 模型上的函数.md
│   │   └── 配置通知.md
│   ├── 动作类型
│   │   ├── Function-backed actions
│   │   │   ├── 入门.md
│   │   │   └── 概述.md
│   │   ├── Parameters
│   │   │   ├── 对象下拉菜单安全注意事项.md
│   │   │   ├── 概述.md
│   │   │   ├── 筛选参数下拉菜单的结果.md
│   │   │   ├── 覆盖.md
│   │   │   └── 设置参数默认值.md
│   │   ├── Side effects
│   │   │   ├── Webhooks.md
│   │   │   ├── 概述.md
│   │   │   ├── 设置 Webhook.md
│   │   │   ├── 设置通知.md
│   │   │   └── 通知.md
│   │   ├── 上传附件.md
│   │   ├── 入门.md
│   │   ├── 在平台中使用操作.md
│   │   ├── 将操作类型添加到Marketplace产品.md
│   │   ├── 提交标准.md
│   │   ├── 撤销或取消操作.md
│   │   ├── 操作指标 [测试版].md
│   │   ├── 操作日志.md
│   │   ├── 权限.md
│   │   ├── 概述.md
│   │   ├── 行内编辑.md
│   │   ├── 规则.md
│   │   ├── 规模和属性限制.md
│   │   └── 配置部分.md
│   ├── 对象链接类型
│   │   ├── Link types
│   │   │   ├── 元数据参考.md
│   │   │   ├── 创建链接类型.md
│   │   │   ├── 概述.md
│   │   │   └── 编辑链接类型.md
│   │   ├── Metadata
│   │   │   ├── 渲染提示.md
│   │   │   ├── 状态.md
│   │   │   └── 类型类.md
│   │   ├── Object types
│   │   │   ├── 元数据参考.md
│   │   │   ├── 创建 Object 类型.md
│   │   │   ├── 概览.md
│   │   │   ├── 编辑Object类型.md
│   │   │   └── 通过类型映射启用 Gotham 集成.md
│   │   ├── Properties
│   │   │   ├── 仅编辑属性.md
│   │   │   ├── 元数据参考.md
│   │   │   ├── 必填属性.md
│   │   │   ├── 支持的值格式化.md
│   │   │   ├── 概览.md
│   │   │   ├── 添加条件格式化.md
│   │   │   └── 编辑Object类型属性.md
│   │   ├── Shared properties
│   │   │   ├── 元数据参考.md
│   │   │   ├── 创建共享属性.md
│   │   │   ├── 在对象类型上使用共享属性.md
│   │   │   ├── 概述.md
│   │   │   └── 编辑共享属性.md
│   │   ├── Struct types
│   │   │   ├── 创建结构属性类型.md
│   │   │   ├── 概述.md
│   │   │   ├── 结构属性和共享属性类型.md
│   │   │   ├── 编辑结构属性类型.md
│   │   │   └── 自动映射结构属性.md
│   │   ├── Value types
│   │   │   ├── 使用值类型.md
│   │   │   ├── 值类型权限.md
│   │   │   ├── 值类型版本.md
│   │   │   ├── 值类型约束.md
│   │   │   ├── 创建值类型.md
│   │   │   └── 概述.md
│   │   ├── Object 类型组.md
│   │   ├── 允许用户编辑Objects和链接.md
│   │   ├── 将Object和链接类型添加到Marketplace产品.md
│   │   └── 类型参考.md
│   ├── 接口
│   │   ├── 元数据参考.md
│   │   ├── 创建界面.md
│   │   ├── 实现接口.md
│   │   ├── 扩展接口.md
│   │   ├── 接口链接类型.md
│   │   ├── 概述.md
│   │   ├── 编辑接口定义.md
│   │   └── 编辑接口实现.md
│   └── 本体
│       ├── Usage
│       │   ├── Ontology 占用量.md
│       │   ├── 使用Ontology查询计算使用情况.md
│       │   └── 计算使用：Ontology 索引.md
│       ├── Ontology 提案.md
│       ├── 共享Ontology.md
│       ├── 在Ontologies之间迁移本体资源.md
│       ├── 权限.md
│       └── 概述.md
├── 应用
│   ├── Foundry规则
│   │   ├── Core concepts
│   │   │   ├── Foundry Rules 工作流配置.md
│   │   │   ├── Object模型.md
│   │   │   ├── Workshop 应用.md
│   │   │   ├── 概述.md
│   │   │   └── 规则逻辑.md
│   │   ├── Deploy
│   │   │   ├── 编写并运行规则.md
│   │   │   ├── 部署 Foundry Rules.md
│   │   │   ├── 部署工作流.md
│   │   │   └── 配置工作流.md
│   │   ├── Legacy Foundry Rules Setup (Taurus)
│   │   │   ├── 升级以使用规则操作.md
│   │   │   ├── 旧版 Foundry 规则设置 (Taurus).md
│   │   │   ├── 迁移到 Foundry Rules.md
│   │   │   ├── 配置 Workshop 应用程序.md
│   │   │   ├── 配置变换管道.md
│   │   │   ├── 配置时间序列.md
│   │   │   └── 配置规则操作.md
│   │   ├── Settings & customization
│   │   │   ├── 允许和默认输出值.md
│   │   │   ├── 启用非必填功能.md
│   │   │   ├── 定制 Foundry Rules.md
│   │   │   ├── 添加自定义属性.md
│   │   │   ├── 编辑规则的权限.md
│   │   │   └── 自定义您的 Foundry Rules 流水线.md
│   │   ├── Time series
│   │   │   ├── 时间序列规则.md
│   │   │   └── 部署时间序列 Foundry 规则.md
│   │   ├── Foundry Rules.md
│   │   ├── 将 Foundry Rules 添加到 Marketplace 产品.md
│   │   └── 故障排除参考.md
│   ├── 动态调度
│   │   ├── Scheduling Calendar widget
│   │   │   ├── 微件配置.md
│   │   │   └── 日程安排日历微件.md
│   │   ├── Ontology 原语和数据模型配置.md
│   │   ├── 建议函数.md
│   │   ├── 搜索函数.md
│   │   ├── 核心概念.md
│   │   ├── 概述.md
│   │   ├── 调度甘特图微件.md
│   │   ├── 起始.md
│   │   └── 验证规则.md
│   ├── 地图
│   │   ├── Configuration
│   │   │   ├── 控制面板.md
│   │   │   └── 设置.md
│   │   ├── Integrate data for the map
│   │   │   ├── Ontology Object.md
│   │   │   ├── Ontology 操作.md
│   │   │   ├── 地图图层编辑器.md
│   │   │   └── 地图搜索周围函数.md
│   │   ├── Interact with maps
│   │   │   ├── 创建、保存和导出地图.md
│   │   │   ├── 图层管理.md
│   │   │   ├── 地图界面概述.md
│   │   │   ├── 导航.md
│   │   │   ├── 将数据添加到地图.md
│   │   │   ├── 形状.md
│   │   │   ├── 操作.md
│   │   │   ├── 注释.md
│   │   │   ├── 直方图.md
│   │   │   └── 选择.md
│   │   ├── Templates & Workshop widget
│   │   │   ├── 在 Workshop 模块中嵌入地图模板.md
│   │   │   └── 地图模板.md
│   │   ├── Time
│   │   │   ├── 事件.md
│   │   │   ├── 地图中的时间和时间数据.md
│   │   │   ├── 时间序列.md
│   │   │   ├── 时间轴.md
│   │   │   └── 时间选择.md
│   │   ├── Visualize Ontology data
│   │   │   ├── 多边形和线几何图形.md
│   │   │   ├── 显示高规模对象数据.md
│   │   │   ├── 概述.md
│   │   │   ├── 点几何图形.md
│   │   │   └── 轨迹几何.md
│   │   ├── 入门指南.md
│   │   ├── 将地图模板添加到Marketplace产品.md
│   │   ├── 核心概念.md
│   │   └── 概览.md
│   ├── 对象浏览器
│   │   ├── Analyze and compare
│   │   │   ├── 使用图表进行探索.md
│   │   │   ├── 保存列表.md
│   │   │   ├── 保存探索.md
│   │   │   ├── 应用操作.md
│   │   │   ├── 查看结果.md
│   │   │   ├── 比较对象集.md
│   │   │   ├── 筛选结果.md
│   │   │   └── 通过旋转探索关联对象.md
│   │   ├── Search and explore objects
│   │   │   ├── 搜索Objects.md
│   │   │   └── 搜索语法.md
│   │   ├── 入门.md
│   │   ├── 概述.md
│   │   ├── 生成 Object Explorer 链接.md
│   │   └── 配置Object Explorer.md
│   ├── 对象监视器
│   │   ├── Core concepts
│   │   │   ├── 操作.md
│   │   │   ├── 条件.md
│   │   │   ├── 活动.md
│   │   │   ├── 监控.md
│   │   │   ├── 评估.md
│   │   │   ├── 输入.md
│   │   │   └── 通知.md
│   │   ├── Object Monitors.md
│   │   ├── 创建一个新Object监视器.md
│   │   ├── 错误参考.md
│   │   └── 限制.md
│   ├── 对象视图
│   │   ├── Configuration
│   │   │   ├── 概述.md
│   │   │   ├── 管理Object视图版本.md
│   │   │   ├── 配置 Workshop 标签页.md
│   │   │   ├── 配置应用程序侧边栏.md
│   │   │   ├── 配置微件（旧版）.md
│   │   │   ├── 配置标签页.md
│   │   │   └── 配置配置文件.md
│   │   ├── Widgets
│   │   │   ├── 可视化.md
│   │   │   ├── 属性和链接.md
│   │   │   ├── 应用程序和文件.md
│   │   │   ├── 筛选.md
│   │   │   └── 设计.md
│   │   ├── 在平台中使用Object View.md
│   │   ├── 对Object发表评论.md
│   │   ├── 概览.md
│   │   ├── 添加Object视图到Marketplace产品.md
│   │   └── 生成Object视图URL.md
│   ├── 本体管理器
│   │   ├── Change management
│   │   │   ├── 保存对Ontology的更改.md
│   │   │   └── 审查和恢复更改.md
│   │   ├── Ontology 清理.md
│   │   ├── Ontology 角色迁移.md
│   │   ├── Ontology指标.md
│   │   ├── 导出、编辑和导入Ontology.md
│   │   ├── 导航.md
│   │   └── 概述.md
│   ├── 流程挖掘
│   │   ├── 创建机械流程.md
│   │   ├── 将流程挖掘操作化.md
│   │   ├── 核心概念.md
│   │   └── 概述.md
│   ├── 逻辑
│   │   ├── AIP Logic Evaluations
│   │   │   ├── 入门.md
│   │   │   ├── 创建评估套件.md
│   │   │   ├── 评估.md
│   │   │   └── 评估指标仪表盘.md
│   │   ├── AIP Logic 常见问题解答.md
│   │   ├── AIP Logic与自动化的集成.md
│   │   ├── 使用 AIP Logic 计算资源消耗.md
│   │   ├── 入门指南.md
│   │   ├── 核心概念.md
│   │   └── 概述.md
│   └── 顶点
│       ├── Configuration
│       │   ├── 在控制面板中配置Vertex设置.md
│       │   └── 配置链接合并.md
│       ├── Events and time series
│       │   ├── 使用时间选择.md
│       │   ├── 探索相关事件.md
│       │   ├── 探索相关时间序列.md
│       │   ├── 查看和筛选时间轴上的事件.md
│       │   ├── 概述.md
│       │   ├── 配置事件.md
│       │   └── 配置阈值.md
│       ├── Graphs
│       │   ├── Object和边显示选项.md
│       │   ├── 从其他应用生成图表.md
│       │   ├── 使用函数派生属性.md
│       │   ├── 使用函数生成图表.md
│       │   ├── 保存、共享和协作.md
│       │   ├── 创建图模板.md
│       │   ├── 只读模式.md
│       │   ├── 在Workshop模块中嵌入图形.md
│       │   ├── 探索Object关系.md
│       │   └── 探索现有图表.md
│       ├── Scenarios
│       │   ├── 入门指南.md
│       │   ├── 场景选项.md
│       │   ├── 概览.md
│       │   └── 配置链式模型.md
│       ├── 将 Vertex 图模板添加到 Marketplace 产品.md
│       ├── 概览.md
│       └── 示例应用案例.md
├── 本体架构
│   ├── 对象后端
│   │   ├── Object Storage v1与Object Storage v2之间的重大变更.md
│   │   ├── 从对象存储 v1 (Phonograph) 迁移到对象存储 v2.md
│   │   ├── 概述.md
│   │   └── 聚合注意事项.md
│   ├── 对象数据库
│   │   └── [遗留] Object Storage v1 (Phonograph).md
│   ├── 对象权限管理
│   │   ├── 多数据源Object类型（MDOs）.md
│   │   ├── 概述.md
│   │   ├── 管理Object类型和Object实例安全性.md
│   │   └── 配置受限视图支持的对象类型.md
│   ├── 对象索引
│   │   ├── Funnel批处理管道.md
│   │   ├── Funnel流式管道.md
│   │   ├── 常见问题解答.md
│   │   └── 概述.md
│   └── 对象编辑
│       ├── Object编辑和物化.md
│       ├── 启用用户编辑历史.md
│       ├── 应用操作时的权限检查.md
│       ├── 物化.md
│       ├── 用户编辑的应用方式.md
│       └── 管理模式更改.md
├── Ontology中的模型.md
├── Ontology搭建.md
├── 为什么创建Ontology？.md
├── 基于Ontology的应用程序.md
└── 核心概念.md
```

## 全部文档

| 路径 | 标题 | 摘要 / 关键词 | 来源 |
|---|---|---|---|
| `Ontology中的模型.md` | Ontology中的模型 | 端到端工作流程；优势；models, ontology | [原文](<https://www.palantir.com/docs/zh/foundry/ontology/models/>) |
| `Ontology搭建.md` | Ontology搭建 | Object和链接类型；操作类型和函数；接口；支持决策制定；ontology, overview | [原文](<https://www.palantir.com/docs/zh/foundry/ontology/overview/>) |
| `为什么创建Ontology？.md` | 为什么创建Ontology？ | 规模化连接；可解释性；规模经济；决策捕获；ontology, why-ontology | [原文](<https://www.palantir.com/docs/zh/foundry/ontology/why-ontology/>) |
| `基于Ontology的应用程序.md` | 基于Ontology的应用程序 | 应用程序参考；Object Views；Object Explorer；Quiver；applications, ontology | [原文](<https://www.palantir.com/docs/zh/foundry/ontology/applications/>) |
| `定义本体/函数/Functions called through the API gateway/查询.md` | 查询 | 查询装饰器；示例：简单查询；示例: API命名查询；API 名称验证；Functions called through the API gateway, functions, query-functions, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/query-functions/>) |
| `定义本体/函数/Functions on objects/API- Object和链接.md` | API: Object和链接 | 属性；数组属性；链接类型；Ontology 元数据；Functions on objects, api-objects-links, functions, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/api-objects-links/>) |
| `定义本体/函数/Functions on objects/API- 附件.md` | API: 附件 | 函数中的附件；读取附件数据；创建附件；Functions on objects, api-attachments, functions, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/api-attachments/>) |
| `定义本体/函数/Functions on objects/API：媒体.md` | API：媒体 | 通用操作；读取原始媒体数据；获取媒体元数据；类型守卫；Functions on objects, api-media, functions, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/api-media/>) |
| `定义本体/函数/Functions on objects/API：对象集.md` | API：对象集 | 对象搜索；筛选；组合筛选；以模糊搜索筛选字符串属性；Functions on objects, api-object-sets, functions, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/api-object-sets/>) |
| `定义本体/函数/Functions on objects/Object标识符.md` | Object标识符 | 标识符类型；Object RIDs；主键；对代码的影响；Functions on objects, functions, object-identifiers, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/object-identifiers/>) |
| `定义本体/函数/Functions on objects/入门.md` | 入门 | 导入Ontology类型；添加一个基于Object的函数；在实时预览中测试；发布新的函数；Functions on objects, foo-getting-started, functions, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/foo-getting-started/>) |
| `定义本体/函数/Functions on objects/创建自定义聚合.md` | 创建自定义聚合 | 加载聚合；操作聚合结果；返回聚合结果；Functions on objects, create-custom-aggregation, functions, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/create-custom-aggregation/>) |
| `定义本体/函数/Functions on objects/导入Object和链接类型.md` | 导入Object和链接类型 | Functions on objects, functions, ontology-imports, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/ontology-imports/>) |
| `定义本体/函数/Functions on objects/概述.md` | 概述 | Functions on objects, functions, functions-on-objects, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/functions-on-objects/>) |
| `定义本体/函数/Models and graphs/创建模型函数.md` | 创建模型函数 | 术语；模型函数的使用；如何编写模型函数；模型函数支持的输入；Models and graphs, functions, model-functions, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/model-functions/>) |
| `定义本体/函数/Ontology edits/API- Ontology编辑.md` | API: Ontology编辑 | 声明编辑函数；更新属性；更新链接；创建对象；Ontology edits, api-ontology-edits, functions, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/api-ontology-edits/>) |
| `定义本体/函数/Ontology edits/为新Objects生成唯一ID.md` | 为新Objects生成唯一ID | 导入包；在代码中使用包；Ontology edits, edits-generate-id, functions, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/edits-generate-id/>) |
| `定义本体/函数/Ontology edits/抛出用户界面错误.md` | 抛出用户界面错误 | Ontology edits, functions, user-facing-error, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/user-facing-error/>) |
| `定义本体/函数/Ontology edits/概述.md` | 概述 | 编辑何时应用；编辑如何被捕获；检索编辑后的值；注意事项：编辑和Object搜索；Ontology edits, edits-overview, functions, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/edits-overview/>) |
| `定义本体/函数/Performance and limits/优化性能.md` | 优化性能 | 使用性能选项卡提升函数性能；尽量使用Objects API；优化链接遍历；优化派生列生成；Performance and limits, functions, optimize-performance, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/optimize-performance/>) |
| `定义本体/函数/Performance and limits/强制限制.md` | 强制限制 | 时间限制；内存限制；单线程；对象集加载限制；Performance and limits, enforced-limits, functions, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/enforced-limits/>) |
| `定义本体/函数/Python functions/Ontology 更改.md` | Ontology 更改 | 定义编辑函数；构建 Ontology 编辑容器；更新属性；更新链接；Python functions, functions, python-ontology-edits, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/python-ontology-edits/>) |
| `定义本体/函数/Python functions/从Python函数进行API调用.md` | 从Python函数进行API调用 | 配置对外部API的访问；在函数中使用外部来源；Python functions, functions, python-functions-api-calls, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/python-functions-api-calls/>) |
| `定义本体/函数/Python functions/在Pipeline Builder中使用Python函数.md` | 在Pipeline Builder中使用Python函数 | 前提条件；架构；在Pipeline Builder管道中使用您的函数；在Pipeline Builder中进行外部API调用；Python functions, functions, python-functions-builder, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/python-functions-builder/>) |
| `定义本体/函数/Python functions/在Workshop中使用Python函数.md` | 在Workshop中使用Python函数 | 先决条件；架构；部署Python函数；在Workshop中使用Python函数；Python functions, functions, python-functions-workshop, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/python-functions-workshop/>) |
| `定义本体/函数/Python functions/对象上的函数.md` | 对象上的函数 | 生成Python Ontology SDK；示例；Python functions, functions, python-functions-on-objects, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/python-functions-on-objects/>) |
| `定义本体/函数/Python functions/类型参考.md` | 类型参考 | 自定义类型和结构体；使用`dataclasses.dataclass`的自定义类型示例；使用API类型的自定义类型示例（不使用`dataclass.dataclass`）；下一步；Python functions, functions, python-function-types, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/python-function-types/>) |
| `定义本体/函数/Python functions/起始步骤.md` | 起始步骤 | 创建 Python 函数库；探索库；在实时预览中测试；提交并发布您的函数；Python functions, functions, python-getting-started, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/python-getting-started/>) |
| `定义本体/函数/Python functions/高级用法.md` | 高级用法 | 发布查询函数；调用查询函数；Python functions, functions, python-functions-advanced-usage, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/python-functions-advanced-usage/>) |
| `定义本体/函数/Semantic search/PDF处理.md` | PDF处理 | 设置语义搜索以在PDF中进行搜索；Semantic search, functions, pdf-handling, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/pdf-handling/>) |
| `定义本体/函数/Semantic search/使用Palantir提供的模型创建语义搜索工作流.md` | 使用Palantir提供的模型创建语义搜索工作流 | 说明；生成嵌入并创建对象类型；在Workshop中使用KNN对象集（无代码）创建简单的语义搜索工作流；使用AIP Agent（无代码）；Semantic search, functions, using-palantir-provided-models-to-create-a-semantic-search-workflow, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/using-palantir-provided-models-to-create-a-semantic-search-workflow/>) |
| `定义本体/函数/Semantic search/使用自定义模型创建语义搜索工作流.md` | 使用自定义模型创建语义搜索工作流 | 1. 使用Foundry中的模型创建嵌入；2. 创建对象类型；3. 创建实时建模部署；4. 在模型上使用函数创建嵌入；Semantic search, functions, using-custom-models-to-create-a-semantic-search-workflow, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/using-custom-models-to-create-a-semantic-search-workflow/>) |
| `定义本体/函数/Semantic search/分块.md` | 分块 | 分块示例；Semantic search, chunking, functions, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/chunking/>) |
| `定义本体/函数/Semantic search/概述.md` | 概述 | Semantic search, functions, overview-semantic-search, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/overview-semantic-search/>) |
| `定义本体/函数/TypeScript basics/处理未定义值.md` | 处理未定义值 | 显式检查；非空断言操作符；TypeScript basics, functions, undefined-values, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/undefined-values/>) |
| `定义本体/函数/TypeScript basics/添加 npm 依赖项.md` | 添加 npm 依赖项 | 启用从公共 npm 注册表获取依赖项；在代码存储库中添加依赖项；手动添加依赖项；TypeScript basics, add-dependencies, functions, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/add-dependencies/>) |
| `定义本体/函数/TypeScript basics/装饰器.md` | 装饰器 | TypeScript basics, decorators, functions, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/decorators/>) |
| `定义本体/函数/TypeScript basics/调试函数.md` | 调试函数 | 控制台日志记录；TypeScript basics, debug, functions, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/debug/>) |
| `定义本体/函数/TypeScript basics/输入和输出类型.md` | 输入和输出类型 | 标量类型；非必填类型；集合；聚合；TypeScript basics, functions, input-output-types, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/input-output-types/>) |
| `定义本体/函数/Unit testing/入门指南.md` | 入门指南 | 示例；运行测试；下一步；Unit testing, functions, unit-test-getting-started, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/unit-test-getting-started/>) |
| `定义本体/函数/Unit testing/创建存根对象.md` | 创建存根对象 | Unit testing, functions, unit-test-stub-objects, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/unit-test-stub-objects/>) |
| `定义本体/函数/Unit testing/存根对象搜索和聚合.md` | 存根对象搜索和聚合 | 测试对象集上的筛选；使用存根测试对象属性上的聚合；使用存根测试对象；使用存根测试不同的对象集；Unit testing, functions, unit-test-object-searches, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/unit-test-object-searches/>) |
| `定义本体/函数/Unit testing/模拟日期、时间戳和UUID.md` | 模拟日期、时间戳和UUID | UUID函数；高级UUID函数；Timestamp.now() 函数；LocalDate.now() 函数；Unit testing, functions, unit-test-dates-timestamps, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/unit-test-dates-timestamps/>) |
| `定义本体/函数/Unit testing/模拟用户和组.md` | 模拟用户和组 | 用户模拟；分组模拟；Unit testing, functions, unit-test-users-groups, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/unit-test-users-groups/>) |
| `定义本体/函数/Unit testing/调试.md` | 调试 | 设置断点；运行调试器；检查变量；桢；Unit testing, functions, unit-test-debugging, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/unit-test-debugging/>) |
| `定义本体/函数/Unit testing/验证Ontology编辑.md` | 验证Ontology编辑 | 单数与复数验证方法；验证Object创建；验证新创建对象上的编辑；验证Object属性编辑；Unit testing, functions, unit-test-ontology-edits, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/unit-test-ontology-edits/>) |
| `定义本体/函数/入门.md` | 入门 | 创建 TypeScript 函数代码库；浏览代码库；添加另一个函数；在实时预览中测试；functions, getting-started, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/getting-started/>) |
| `定义本体/函数/函数中的外部来源.md` | 函数中的外部来源 | 将来源导入到函数库中；在函数中使用 webhooks；示例：从一个函数进行多次调用；错误处理；external-sources, functions, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/external-sources/>) |
| `定义本体/函数/函数中的语言模型.md` | 函数中的语言模型 | 导入语言模型；编写使用语言模型的函数；嵌入；性能注意事项；functions, language-models, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/language-models/>) |
| `定义本体/函数/在平台中使用函数.md` | 在平台中使用函数 | Workshop；变量；对象表：派生属性；图表：派生聚合；functions, use-functions, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/use-functions/>) |
| `定义本体/函数/将函数添加到 Marketplace 产品.md` | 将函数添加到 Marketplace 产品 | 支持的功能；将函数添加到产品中；安装时的函数覆盖；functions, marketplace-functions, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/marketplace-functions/>) |
| `定义本体/函数/将资源导入代码库.md` | 将资源导入代码库 | 选择一个 Ontology；导入资源；管理导入的资源；导入没有 API 名称的资源；functions, resource-imports-sidebar, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/resource-imports-sidebar/>) |
| `定义本体/函数/权限.md` | 权限 | 函数编写；Ontology实体权限；Object加载权限；已发布函数执行；functions, permissions, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/permissions/>) |
| `定义本体/函数/概述.md` | 概述 | 函数功能支持的语言；无服务器函数超时；部署函数超时；functions, overview, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/overview/>) |
| `定义本体/函数/模型上的函数.md` | 模型上的函数 | 导入实时部署；编写一个模型支持的函数；由模型数据集支持的函数；性能考量；functions, functions-on-models, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/functions-on-models/>) |
| `定义本体/函数/配置通知.md` | 配置通知 | 定义自定义通知；检索用户和组；返回接收者；configure-notifications, functions, 函数, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/functions/configure-notifications/>) |
| `定义本体/动作类型/Function-backed actions/入门.md` | 入门 | 先决条件；创建一个基于函数的操作；更改函数逻辑；Function-backed actions, action-types, function-actions-getting-started, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/function-actions-getting-started/>) |
| `定义本体/动作类型/Function-backed actions/概述.md` | 概述 | Function-backed actions, action-types, function-actions-overview, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/function-actions-overview/>) |
| `定义本体/动作类型/Parameters/对象下拉菜单安全注意事项.md` | 对象下拉菜单安全注意事项 | 示例：数据隐私问题；技术细节；Parameters, action-types, dropdown-security, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/dropdown-security/>) |
| `定义本体/动作类型/Parameters/概述.md` | 概述 | Parameters, action-types, parameter-overview, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/parameter-overview/>) |
| `定义本体/动作类型/Parameters/筛选参数下拉菜单的结果.md` | 筛选参数下拉菜单的结果 | 多选参数下拉菜单；对象下拉菜单；数据隐私影响；支持的操作；Parameters, action-types, parameters-filter, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/parameters-filter/>) |
| `定义本体/动作类型/Parameters/覆盖.md` | 覆盖 | 添加和编辑覆盖；覆盖块；"If"和条件；"Then"和覆盖；Parameters, action-types, parameters-override, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/parameters-override/>) |
| `定义本体/动作类型/Parameters/设置参数默认值.md` | 设置参数默认值 | 默认值与局部变量的交互；配置默认值；静态默认值；Object属性默认值；Parameters, action-types, parameters-default-value, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/parameters-default-value/>) |
| `定义本体/动作类型/Side effects/Webhooks.md` | Webhooks | Webhooks: 数据输出与副作用；数据输出 Webhooks；副作用 Webhooks；输入参数；Side effects, action-types, webhooks, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/webhooks/>) |
| `定义本体/动作类型/Side effects/概述.md` | 概述 | Side effects, action-types, side-effects-overview, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/side-effects-overview/>) |
| `定义本体/动作类型/Side effects/设置 Webhook.md` | 设置 Webhook | 前提条件；步骤；下一步；Side effects, action-types, set-up-webhook, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/set-up-webhook/>) |
| `定义本体/动作类型/Side effects/设置通知.md` | 设置通知 | 前提条件；完成入门教程；向您的对象类型添加指派人属性；添加通知；Side effects, action-types, set-up-notification, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/set-up-notification/>) |
| `定义本体/动作类型/Side effects/通知.md` | 通知 | 收件人；内容；内容组件；示例配置；Side effects, action-types, notifications, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/notifications/>) |
| `定义本体/动作类型/上传附件.md` | 上传附件 | 配置操作类型；配置Object类型；架构和限制；action-types, upload-attachments, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/upload-attachments/>) |
| `定义本体/动作类型/入门.md` | 入门 | 先决条件；创建新的操作类型；编辑参数；添加提交条件；action-types, getting-started, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/getting-started/>) |
| `定义本体/动作类型/在平台中使用操作.md` | 在平台中使用操作 | 对象视图；Object Explorer；Workshop；action-types, use-actions, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/use-actions/>) |
| `定义本体/动作类型/将操作类型添加到Marketplace产品.md` | 将操作类型添加到Marketplace产品 | 支持的功能；将操作类型添加到产品；action-types, marketplace-action-types, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/marketplace-action-types/>) |
| `定义本体/动作类型/提交标准.md` | 提交标准 | 条件；当前用户；参数；选择一个值；action-types, submission-criteria, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/submission-criteria/>) |
| `定义本体/动作类型/撤销或取消操作.md` | 撤销或取消操作 | 配置可撤销的操作；撤销操作；注意事项；在没有撤销操作提示的情况下撤销删除操作；action-reverts, action-types, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/action-reverts/>) |
| `定义本体/动作类型/操作指标 [测试版].md` | 操作指标 [测试版] | action-metrics, action-types, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/action-metrics/>) |
| `定义本体/动作类型/操作日志.md` | 操作日志 | 背景；操作日志Ontology；操作日志架构；基于函数的操作类型的操作日志；action-log, action-types, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/action-log/>) |
| `定义本体/动作类型/权限.md` | 权限 | 应用操作；提交标准；Object编辑权限；副作用权限；action-types, permissions, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/permissions/>) |
| `定义本体/动作类型/概述.md` | 概述 | action-types, overview, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/overview/>) |
| `定义本体/动作类型/行内编辑.md` | 行内编辑 | Object Explorer 行内编辑；配置；行内编辑的操作类型要求；Workshop 行内编辑；action-types, inline-edits, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/inline-edits/>) |
| `定义本体/动作类型/规则.md` | 规则 | Ontology规则；值和参数；创建对象和多对多链接；无效组合；action-types, rules, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/rules/>) |
| `定义本体/动作类型/规模和属性限制.md` | 规模和属性限制 | 编辑限制；支持的属性类型；支持的属性；其他限制；action-types, scale-property-limits, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/scale-property-limits/>) |
| `定义本体/动作类型/配置部分.md` | 配置部分 | 向操作表单添加部分；向部分添加参数；action-types, configure-sections, 动作类型, 定义本体 | [原文](<https://www.palantir.com/docs/zh/foundry/action-types/configure-sections/>) |
| `定义本体/对象链接类型/Link types/元数据参考.md` | 元数据参考 | Link types, link-type-metadata, object-link-types, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/link-type-metadata/>) |
| `定义本体/对象链接类型/Link types/创建链接类型.md` | 创建链接类型 | 配置新链接类型；故障排除；出错: `Phonograph2:DatasetAndBranchAlreadyRegistered`；Link types, create-link-type, object-link-types, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/create-link-type/>) |
| `定义本体/对象链接类型/Link types/概述.md` | 概述 | Link types, link-types-overview, object-link-types, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/link-types-overview/>) |
| `定义本体/对象链接类型/Link types/编辑链接类型.md` | 编辑链接类型 | 潜在破坏性更改；无数据输出的链接类型；启用了数据输出的链接类型；编辑现有链接类型；Link types, edit-link-types, object-link-types, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/edit-link-types/>) |
| `定义本体/对象链接类型/Metadata/渲染提示.md` | 渲染提示 | Metadata, metadata-render-hints, object-link-types, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/metadata-render-hints/>) |
| `定义本体/对象链接类型/Metadata/状态.md` | 状态 | 不允许的操作；编辑状态；批量编辑状态；属性；Metadata, metadata-statuses, object-link-types, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/metadata-statuses/>) |
| `定义本体/对象链接类型/Metadata/类型类.md` | 类型类 | Metadata, metadata-typeclasses, object-link-types, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/metadata-typeclasses/>) |
| `定义本体/对象链接类型/Object types/元数据参考.md` | 元数据参考 | Object types, object-link-types, object-type-metadata, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/object-type-metadata/>) |
| `定义本体/对象链接类型/Object types/创建 Object 类型.md` | 创建 Object 类型 | 使用助手创建新 Object 类型；创建新 Object 类型并添加支持数据源；选择支持数据源；Object 类型元数据；Object types, create-object-type, object-link-types, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/create-object-type/>) |
| `定义本体/对象链接类型/Object types/概览.md` | 概览 | Object types, object-link-types, object-types-overview, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/object-types-overview/>) |
| `定义本体/对象链接类型/Object types/编辑Object类型.md` | 编辑Object类型 | 潜在破坏性更改；无数据输出的Object类型；具有数据输出的Object类型；编辑现有的Object类型；Object types, edit-object-type, object-link-types, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/edit-object-type/>) |
| `定义本体/对象链接类型/Object types/通过类型映射启用 Gotham 集成.md` | 通过类型映射启用 Gotham 集成 | 在 Foundry 的 Ontology Manager 中开启类型映射；配置 Object 类型的父类别和 Gotham 属性类型；Object types, enable-gotham-integration, object-link-types, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/enable-gotham-integration/>) |
| `定义本体/对象链接类型/Object 类型组.md` | Object 类型组 | 组配置；组搜索与发现；组权限；传统组迁移；object-link-types, type-groups, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/type-groups/>) |
| `定义本体/对象链接类型/Properties/仅编辑属性.md` | 仅编辑属性 | 仅编辑属性概述；创建仅编辑属性；将仅编辑属性映射到数据集列；Properties, edit-only-properties, object-link-types, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/edit-only-properties/>) |
| `定义本体/对象链接类型/Properties/元数据参考.md` | 元数据参考 | 支持有限的属性基本类型；Properties, object-link-types, property-metadata, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/property-metadata/>) |
| `定义本体/对象链接类型/Properties/必填属性.md` | 必填属性 | 必填属性摘要；创建必填属性；多个支持数据源的对象类型的必填属性；Properties, object-link-types, required-properties, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/required-properties/>) |
| `定义本体/对象链接类型/Properties/支持的值格式化.md` | 支持的值格式化 | 支持的值格式化；添加值格式化；数字格式化选项；日期和时间格式化选项；Properties, object-link-types, value-formatting, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/value-formatting/>) |
| `定义本体/对象链接类型/Properties/概览.md` | 概览 | 支持的属性类型；Properties, object-link-types, properties-overview, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/properties-overview/>) |
| `定义本体/对象链接类型/Properties/添加条件格式化.md` | 添加条件格式化 | 添加条件格式化；使用规则编辑器编辑规则；复制规则；常见问题；Properties, conditional-formatting, object-link-types, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/conditional-formatting/>) |
| `定义本体/对象链接类型/Properties/编辑Object类型属性.md` | 编辑Object类型属性 | 删除属性；更改属性对应的列；编辑属性类型的元数据；批量编辑多个属性；Properties, edit-properties, object-link-types, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/edit-properties/>) |
| `定义本体/对象链接类型/Shared properties/元数据参考.md` | 元数据参考 | Shared properties, object-link-types, shared-property-metadata, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/shared-property-metadata/>) |
| `定义本体/对象链接类型/Shared properties/创建共享属性.md` | 创建共享属性 | Shared properties, create-shared-property, object-link-types, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/create-shared-property/>) |
| `定义本体/对象链接类型/Shared properties/在对象类型上使用共享属性.md` | 在对象类型上使用共享属性 | 从对象中分离共享属性；Shared properties, object-link-types, use-shared-property, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/use-shared-property/>) |
| `定义本体/对象链接类型/Shared properties/概述.md` | 概述 | Shared properties, object-link-types, shared-property-overview, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/shared-property-overview/>) |
| `定义本体/对象链接类型/Shared properties/编辑共享属性.md` | 编辑共享属性 | 编辑共享属性元数据；删除共享属性；Shared properties, edit-shared-property, object-link-types, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/edit-shared-property/>) |
| `定义本体/对象链接类型/Struct types/创建结构属性类型.md` | 创建结构属性类型 | Struct types, create-struct-type, object-link-types, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/create-struct-type/>) |
| `定义本体/对象链接类型/Struct types/概述.md` | 概述 | Struct 配置；当前支持水平；Struct types, object-link-types, structs-overview, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/structs-overview/>) |
| `定义本体/对象链接类型/Struct types/结构属性和共享属性类型.md` | 结构属性和共享属性类型 | 创建一个结构类型的共享属性；附加一个结构类型的共享属性；将结构属性类型转换为共享属性；Struct types, object-link-types, struct-shared-properties, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/struct-shared-properties/>) |
| `定义本体/对象链接类型/Struct types/编辑结构属性类型.md` | 编辑结构属性类型 | Struct types, edit-struct-type, object-link-types, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/edit-struct-type/>) |
| `定义本体/对象链接类型/Struct types/自动映射结构属性.md` | 自动映射结构属性 | 在Ontology Manager中自动映射结构类型；在Pipeline Builder中自动映射结构类型；Struct types, object-link-types, struct-automapping, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/struct-automapping/>) |
| `定义本体/对象链接类型/Value types/使用值类型.md` | 使用值类型 | Value types, object-link-types, use-value-type, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/use-value-type/>) |
| `定义本体/对象链接类型/Value types/值类型权限.md` | 值类型权限 | Value types, object-link-types, value-types-permissions, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/value-types-permissions/>) |
| `定义本体/对象链接类型/Value types/值类型版本.md` | 值类型版本 | Value types, object-link-types, value-types-versions, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/value-types-versions/>) |
| `定义本体/对象链接类型/Value types/值类型约束.md` | 值类型约束 | Value types, object-link-types, value-type-constraints, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/value-type-constraints/>) |
| `定义本体/对象链接类型/Value types/创建值类型.md` | 创建值类型 | Value types, create-value-type, object-link-types, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/create-value-type/>) |
| `定义本体/对象链接类型/Value types/概述.md` | 概述 | Value types, object-link-types, value-types-overview, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/value-types-overview/>) |
| `定义本体/对象链接类型/允许用户编辑Objects和链接.md` | 允许用户编辑Objects和链接 | 从Foundry Object应用程序编辑数据；从外部应用程序编辑数据；设置先决条件；allow-editing, object-link-types, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/allow-editing/>) |
| `定义本体/对象链接类型/将Object和链接类型添加到Marketplace产品.md` | 将Object和链接类型添加到Marketplace产品 | 支持的功能；将Object类型添加到产品中；将链接类型添加到产品中；将共享属性添加到产品中；marketplace-ontology-types, object-link-types, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/marketplace-ontology-types/>) |
| `定义本体/对象链接类型/类型参考.md` | 类型参考 | Ontology类型；Object类型；属性；共享属性；object-link-types, type-reference, 定义本体, 对象链接类型 | [原文](<https://www.palantir.com/docs/zh/foundry/object-link-types/type-reference/>) |
| `定义本体/接口/元数据参考.md` | 元数据参考 | interface-metadata, interfaces, 定义本体, 接口 | [原文](<https://www.palantir.com/docs/zh/foundry/interfaces/interface-metadata/>) |
| `定义本体/接口/创建界面.md` | 创建界面 | 创建界面链接类型（非必填）；create-interface, interfaces, 定义本体, 接口 | [原文](<https://www.palantir.com/docs/zh/foundry/interfaces/create-interface/>) |
| `定义本体/接口/实现接口.md` | 实现接口 | 如何在Ontology Manager中实现接口；1. 选择您的接口和对象类型；2. 映射本地属性；3. 映射链接类型约束；implement-interface, interfaces, 定义本体, 接口 | [原文](<https://www.palantir.com/docs/zh/foundry/interfaces/implement-interface/>) |
| `定义本体/接口/扩展接口.md` | 扩展接口 | extend-interface, interfaces, 定义本体, 接口 | [原文](<https://www.palantir.com/docs/zh/foundry/interfaces/extend-interface/>) |
| `定义本体/接口/接口链接类型.md` | 接口链接类型 | 链接类型约束；接口链接目标；对象类型链接目标；接口链接类型基数；interface-link-types-overview, interfaces, 定义本体, 接口 | [原文](<https://www.palantir.com/docs/zh/foundry/interfaces/interface-link-types-overview/>) |
| `定义本体/接口/概述.md` | 概述 | 接口和对象类型之间的区别；接口类型；功能接口；抽象对象接口；interface-overview, interfaces, 定义本体, 接口 | [原文](<https://www.palantir.com/docs/zh/foundry/interfaces/interface-overview/>) |
| `定义本体/接口/编辑接口定义.md` | 编辑接口定义 | 添加共享属性；添加链接类型约束；移除共享属性；移除或编辑链接类型约束；edit-interface-definition, interfaces, 定义本体, 接口 | [原文](<https://www.palantir.com/docs/zh/foundry/interfaces/edit-interface-definition/>) |
| `定义本体/接口/编辑接口实现.md` | 编辑接口实现 | 1. 删除接口实现；更新实现映射；edit-interface-implementation, interfaces, 定义本体, 接口 | [原文](<https://www.palantir.com/docs/zh/foundry/interfaces/edit-interface-implementation/>) |
| `定义本体/本体/Ontology 提案.md` | Ontology 提案 | 定义；提案工作流程；提案导航；提案视图；ontologies, ontologies-proposals, 定义本体, 本体 | [原文](<https://www.palantir.com/docs/zh/foundry/ontologies/ontologies-proposals/>) |
| `定义本体/本体/Usage/Ontology 占用量.md` | Ontology 占用量 | 测量 Ontology 占用量；调查 Ontology 占用量使用情况；影响 Ontology 占用量的因素；管理 Ontology 占用量；Usage, ontologies, volume-usage, 定义本体, 本体 | [原文](<https://www.palantir.com/docs/zh/foundry/ontologies/volume-usage/>) |
| `定义本体/本体/Usage/使用Ontology查询计算使用情况.md` | 使用Ontology查询计算使用情况 | 核心概念：Object类型和对象集；核心概念：查询类型；使用Ontology对象查询测量Foundry计算；使用Object Storage v1测量计算；Usage, ontologies, query-compute-usage, 定义本体, 本体 | [原文](<https://www.palantir.com/docs/zh/foundry/ontologies/query-compute-usage/>) |
| `定义本体/本体/Usage/计算使用：Ontology 索引.md` | 计算使用：Ontology 索引 | 衡量 Ontology 索引的计算使用；调查 Ontology 索引的使用情况；Ontology 索引使用的驱动因素；管理 Ontology 索引计算；Usage, compute-usage, ontologies, 定义本体, 本体 | [原文](<https://www.palantir.com/docs/zh/foundry/ontologies/compute-usage/>) |
| `定义本体/本体/共享Ontology.md` | 共享Ontology | ontologies, shared-ontologies, 定义本体, 本体 | [原文](<https://www.palantir.com/docs/zh/foundry/ontologies/shared-ontologies/>) |
| `定义本体/本体/在Ontologies之间迁移本体资源.md` | 在Ontologies之间迁移本体资源 | ontologies, ontology-migration, 定义本体, 本体 | [原文](<https://www.palantir.com/docs/zh/foundry/ontologies/ontology-migration/>) |
| `定义本体/本体/权限.md` | 权限 | Ontology角色；概述；使用Ontology角色创建新资源；使用Ontology角色的特定类型编辑权限；ontologies, ontology-permissions, 定义本体, 本体 | [原文](<https://www.palantir.com/docs/zh/foundry/ontologies/ontology-permissions/>) |
| `定义本体/本体/概述.md` | 概述 | 与空间的关系；ontologies, ontologies-overview, 定义本体, 本体 | [原文](<https://www.palantir.com/docs/zh/foundry/ontologies/ontologies-overview/>) |
| `应用/Foundry规则/Core concepts/Foundry Rules 工作流配置.md` | Foundry Rules 工作流配置 | 工作流输入；工作流输出；变换配置；规则执行；Core concepts, Foundry规则, foundry-rules, foundry-rules-workflow-configuration, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/foundry-rules-workflow-configuration/>) |
| `应用/Foundry规则/Core concepts/Object模型.md` | Object模型 | 规则；提案；Core concepts, Foundry规则, foundry-rules, object-model, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/object-model/>) |
| `应用/Foundry规则/Core concepts/Workshop 应用.md` | Workshop 应用 | 规则编辑器；提案审核；Core concepts, Foundry规则, foundry-rules, workshop-application, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/workshop-application/>) |
| `应用/Foundry规则/Core concepts/概述.md` | 概述 | Core concepts, Foundry规则, core-concepts, foundry-rules, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/core-concepts/>) |
| `应用/Foundry规则/Core concepts/规则逻辑.md` | 规则逻辑 | 输入；逻辑块；规则输出；Core concepts, Foundry规则, foundry-rules, rule-logic, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/rule-logic/>) |
| `应用/Foundry规则/Deploy/编写并运行规则.md` | 编写并运行规则 | Deploy, Foundry规则, author-and-run-a-rule, foundry-rules, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/author-and-run-a-rule/>) |
| `应用/Foundry规则/Deploy/部署 Foundry Rules.md` | 部署 Foundry Rules | Deploy, Foundry规则, deploy-foundry-rules, foundry-rules, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/deploy-foundry-rules/>) |
| `应用/Foundry规则/Deploy/部署工作流.md` | 部署工作流 | 常见问题；如何更改操作类型上的提交标准？；Deploy, Foundry规则, deploy-workflow, foundry-rules, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/deploy-workflow/>) |
| `应用/Foundry规则/Deploy/配置工作流.md` | 配置工作流 | 高级配置；备用支持数据集；Deploy, Foundry规则, configure-workflow, foundry-rules, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/configure-workflow/>) |
| `应用/Foundry规则/Foundry Rules.md` | Foundry Rules | 应用案例示例；Foundry规则, foundry-rules, overview, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/overview/>) |
| `应用/Foundry规则/Legacy Foundry Rules Setup (Taurus)/升级以使用规则操作.md` | 升级以使用规则操作 | Foundry规则, Legacy Foundry Rules Setup (Taurus), foundry-rules, upgrade-to-use-rule-actions, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/upgrade-to-use-rule-actions/>) |
| `应用/Foundry规则/Legacy Foundry Rules Setup (Taurus)/旧版 Foundry 规则设置 (Taurus).md` | 旧版 Foundry 规则设置 (Taurus) | 变换管道；Workshop 应用程序；规则操作；Foundry规则, Legacy Foundry Rules Setup (Taurus), foundry-rules, legacy-foundry-rules-setup-taurus, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/legacy-foundry-rules-setup-taurus/>) |
| `应用/Foundry规则/Legacy Foundry Rules Setup (Taurus)/迁移到 Foundry Rules.md` | 迁移到 Foundry Rules | 迁移注意事项；将Taurus工作流迁移到Foundry Rules工作流；验证迁移；常见问题；Foundry规则, Legacy Foundry Rules Setup (Taurus), foundry-rules, migrate-to-foundry-rules, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/migrate-to-foundry-rules/>) |
| `应用/Foundry规则/Legacy Foundry Rules Setup (Taurus)/配置 Workshop 应用程序.md` | 配置 Workshop 应用程序 | Foundry规则, Legacy Foundry Rules Setup (Taurus), configure-workshop-app, foundry-rules, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/configure-workshop-app/>) |
| `应用/Foundry规则/Legacy Foundry Rules Setup (Taurus)/配置变换管道.md` | 配置变换管道 | 示例变换；使用`@AdditionalInputs`添加Ontology输入；输入和输出数据集；Foundry规则运行器；Foundry规则, Legacy Foundry Rules Setup (Taurus), configure-transforms-pipeline, foundry-rules, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/configure-transforms-pipeline/>) |
| `应用/Foundry规则/Legacy Foundry Rules Setup (Taurus)/配置时间序列.md` | 配置时间序列 | Workshop应用程序；变换管道；额外输入；示例；Foundry规则, Legacy Foundry Rules Setup (Taurus), configure-timeseries-foundry-rules, foundry-rules, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/configure-timeseries-foundry-rules/>) |
| `应用/Foundry规则/Legacy Foundry Rules Setup (Taurus)/配置规则操作.md` | 配置规则操作 | Foundry规则, Legacy Foundry Rules Setup (Taurus), configure-rule-actions, foundry-rules, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/configure-rule-actions/>) |
| `应用/Foundry规则/Settings & customization/允许和默认输出值.md` | 允许和默认输出值 | 行为和应用案例；配置选项；列值；静态值；Foundry规则, Settings & customization, foundry-rules, permitted-and-default-output-values, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/permitted-and-default-output-values/>) |
| `应用/Foundry规则/Settings & customization/启用非必填功能.md` | 启用非必填功能 | Foundry规则, Settings & customization, enable-optional-features, foundry-rules, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/enable-optional-features/>) |
| `应用/Foundry规则/Settings & customization/定制 Foundry Rules.md` | 定制 Foundry Rules | Foundry规则, Settings & customization, customization, foundry-rules, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/customization/>) |
| `应用/Foundry规则/Settings & customization/添加自定义属性.md` | 添加自定义属性 | Foundry规则, Settings & customization, add-a-custom-property, foundry-rules, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/add-a-custom-property/>) |
| `应用/Foundry规则/Settings & customization/编辑规则的权限.md` | 编辑规则的权限 | Foundry规则, Settings & customization, foundry-rules, rule-permissions, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/rule-permissions/>) |
| `应用/Foundry规则/Settings & customization/自定义您的 Foundry Rules 流水线.md` | 自定义您的 Foundry Rules 流水线 | 应用案例；指南；Foundry规则, Settings & customization, customize-foundry-rules-pipeline, foundry-rules, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/customize-foundry-rules-pipeline/>) |
| `应用/Foundry规则/Time series/时间序列规则.md` | 时间序列规则 | 概述；时间序列面板；添加时间序列面板；时间序列搜索面板；Foundry规则, Time series, foundry-rules, timeseries-concepts, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/timeseries-concepts/>) |
| `应用/Foundry规则/Time series/部署时间序列 Foundry 规则.md` | 部署时间序列 Foundry 规则 | Foundry规则, Time series, deploy-timeseries-foundry-rules, foundry-rules, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/deploy-timeseries-foundry-rules/>) |
| `应用/Foundry规则/将 Foundry Rules 添加到 Marketplace 产品.md` | 将 Foundry Rules 添加到 Marketplace 产品 | 支持的功能；将 Foundry Rules 工作流添加到产品中；Foundry规则, foundry-rules, marketplace, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/marketplace/>) |
| `应用/Foundry规则/故障排除参考.md` | 故障排除参考 | 错误信息；ReadonlyObjectError；400: Actions:InvalidParametersForApply；自定义属性的提案差异未正确显示；Foundry规则, common-issues, foundry-rules, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/foundry-rules/common-issues/>) |
| `应用/动态调度/Ontology 原语和数据模型配置.md` | Ontology 原语和数据模型配置 | 示例：飞机维护计划；简单配置；高级配置；Ontology 要求；dynamic-scheduling, scheduling-ontology-primitives, 动态调度, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/dynamic-scheduling/scheduling-ontology-primitives/>) |
| `应用/动态调度/Scheduling Calendar widget/微件配置.md` | 微件配置 | 微件模式；输入数据（pucks）；显示配置；Scheduling Calendar widget, dynamic-scheduling, scheduling-calendar-widget, 动态调度, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/dynamic-scheduling/scheduling-calendar-widget/>) |
| `应用/动态调度/Scheduling Calendar widget/日程安排日历微件.md` | 日程安排日历微件 | Scheduling Calendar widget, dynamic-scheduling, scheduling-calendar-overview, 动态调度, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/dynamic-scheduling/scheduling-calendar-overview/>) |
| `应用/动态调度/建议函数.md` | 建议函数 | 函数接口；dynamic-scheduling, scheduling-suggestion-functions, 动态调度, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/dynamic-scheduling/scheduling-suggestion-functions/>) |
| `应用/动态调度/搜索函数.md` | 搜索函数 | 函数界面；dynamic-scheduling, scheduling-search-functions, 动态调度, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/dynamic-scheduling/scheduling-search-functions/>) |
| `应用/动态调度/核心概念.md` | 核心概念 | Schedule object；Resource object；调度甘特图；Scenarios；dynamic-scheduling, scheduling-concepts, 动态调度, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/dynamic-scheduling/scheduling-concepts/>) |
| `应用/动态调度/概述.md` | 概述 | dynamic-scheduling, scheduling-overview, 动态调度, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/dynamic-scheduling/scheduling-overview/>) |
| `应用/动态调度/调度甘特图微件.md` | 调度甘特图微件 | 微件设计；微件设置；时间轴；输入数据（行）；dynamic-scheduling, scheduling-gantt-chart-widget, 动态调度, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/dynamic-scheduling/scheduling-gantt-chart-widget/>) |
| `应用/动态调度/起始.md` | 起始 | 1. 创建核心Ontology对象；2. （非必填）定义验证规则；3. 在Ontology Manager中启用功能；4. 在Workshop中使用动态调度；dynamic-scheduling, scheduling-getting-started, 动态调度, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/dynamic-scheduling/scheduling-getting-started/>) |
| `应用/动态调度/验证规则.md` | 验证规则 | 编排；实现验证规则；函数界面；示例函数；dynamic-scheduling, scheduling-validation-rules, 动态调度, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/dynamic-scheduling/scheduling-validation-rules/>) |
| `应用/地图/Configuration/控制面板.md` | 控制面板 | 地图默认设置；配置数据加载；API 密钥；Mapbox：在地图上启用查找位置；Configuration, control-panel, map, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/control-panel/>) |
| `应用/地图/Configuration/设置.md` | 设置 | 单位；启用GeoJSON面板；轮询间隔；时区；Configuration, map, settings, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/settings/>) |
| `应用/地图/Integrate data for the map/Ontology Object.md` | Ontology Object | 配置地理空间对象；点；圆形；多边形和线条；Integrate data for the map, integrate-objects, map, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/integrate-objects/>) |
| `应用/地图/Integrate data for the map/Ontology 操作.md` | Ontology 操作 | 点操作；形状操作；使用操作编辑对象`geoshape`属性；Integrate data for the map, integrate-actions, map, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/integrate-actions/>) |
| `应用/地图/Integrate data for the map/地图图层编辑器.md` | 地图图层编辑器 | 创建新地图图层；矢量图层；栅格图层；对象图层；Integrate data for the map, layer-editor, map, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/layer-editor/>) |
| `应用/地图/Integrate data for the map/地图搜索周围函数.md` | 地图搜索周围函数 | 实现地图搜索周围函数；返回类型；参数；提示和故障排除；Integrate data for the map, integrate-searcharound-functions, map, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/integrate-searcharound-functions/>) |
| `应用/地图/Interact with maps/创建、保存和导出地图.md` | 创建、保存和导出地图 | 创建新地图；保存地图；导出地图；Interact with maps, create-save-maps, map, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/create-save-maps/>) |
| `应用/地图/Interact with maps/图层管理.md` | 图层管理 | 切换图层可见性；重命名图层；重新排序图层；移动对象到新的或现有的图层；Interact with maps, layer-management, map, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/layer-management/>) |
| `应用/地图/Interact with maps/地图界面概述.md` | 地图界面概述 | 面板；工具栏；Interact with maps, map, map-overview, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/map-overview/>) |
| `应用/地图/Interact with maps/导航.md` | 导航 | 基本地图控件；将地图居中于项目；使用查找面板；在地图上查找Objects；Interact with maps, map, navigation, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/navigation/>) |
| `应用/地图/Interact with maps/将数据添加到地图.md` | 将数据添加到地图 | 添加 Ontology 对象；筛选对象；选择并添加结果；地理空间搜索对象；Interact with maps, add-to-map, map, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/add-to-map/>) |
| `应用/地图/Interact with maps/形状.md` | 形状 | 创建形状；绘制形状；从选择中创建；修改形状；Interact with maps, map, shapes, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/shapes/>) |
| `应用/地图/Interact with maps/操作.md` | 操作 | 对形状和点的操作；对Ontology Objects的操作；Interact with maps, actions, map, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/actions/>) |
| `应用/地图/Interact with maps/注释.md` | 注释 | 创建注释；编辑注释；注释样式；Interact with maps, annotations, map, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/annotations/>) |
| `应用/地图/Interact with maps/直方图.md` | 直方图 | 使用直方图；选择；筛选；Interact with maps, histogram, map, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/histogram/>) |
| `应用/地图/Interact with maps/选择.md` | 选择 | 在地图上选择项目；使用直方图选择项目；在地图上锁定Object；选择面板；Interact with maps, map, selection, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/selection/>) |
| `应用/地图/Templates & Workshop widget/在 Workshop 模块中嵌入地图模板.md` | 在 Workshop 模块中嵌入地图模板 | 在 Workshop 中添加地图应用模板微件；选择资源；配置微件；Templates & Workshop widget, map, widget, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/widget/>) |
| `应用/地图/Templates & Workshop widget/地图模板.md` | 地图模板 | 创建地图模板；配置地图模板；参数；Search Arounds；Templates & Workshop widget, map, templates, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/templates/>) |
| `应用/地图/Time/事件.md` | 事件 | 使用事件进行样式设计；与Object相关联的事件；在系列面板上显示；在标签中显示计数；Time, events, map, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/events/>) |
| `应用/地图/Time/地图中的时间和时间数据.md` | 地图中的时间和时间数据 | 时间序列；事件；轨迹；Time, map, time-overview, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/time-overview/>) |
| `应用/地图/Time/时间序列.md` | 时间序列 | 探索相关时间序列；使用时间序列进行样式设置；Time, map, time-series, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/time-series/>) |
| `应用/地图/Time/时间轴.md` | 时间轴 | 查看时间事件；筛选时间事件；更改光标位置；展开时间轴；Time, map, timeline, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/timeline/>) |
| `应用/地图/Time/时间选择.md` | 时间选择 | 更改选择的时间；查看最新数据；更改时间窗口；Time, map, time-selection, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/time-selection/>) |
| `应用/地图/Visualize Ontology data/多边形和线几何图形.md` | 多边形和线几何图形 | 笔触宽度；笔触样式；填充多边形；Visualize Ontology data, map, visualize-polygons-lines, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/visualize-polygons-lines/>) |
| `应用/地图/Visualize Ontology data/显示高规模对象数据.md` | 显示高规模对象数据 | 启用高规模渲染；添加具有高规模渲染的对象；高规模渲染功能兼容性；样式选项；Visualize Ontology data, map, objects-high-scale, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/objects-high-scale/>) |
| `应用/地图/Visualize Ontology data/概述.md` | 概述 | 编辑图层样式；图层样式；标签和工具提示；对象图层的标签内容；Visualize Ontology data, map, visualize-objects, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/visualize-objects/>) |
| `应用/地图/Visualize Ontology data/点几何图形.md` | 点几何图形 | 图标配置；图标；旋转；标记形状；Visualize Ontology data, map, visualize-points, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/visualize-points/>) |
| `应用/地图/Visualize Ontology data/轨迹几何.md` | 轨迹几何 | 移动几何插值；轨迹线；轨迹面包屑；Visualize Ontology data, map, visualize-tracks, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/visualize-tracks/>) |
| `应用/地图/入门指南.md` | 入门指南 | 创建新地图；Map应用程序界面概览；向地图添加Object；周边搜索关联Object；getting-started, map, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/getting-started/>) |
| `应用/地图/将地图模板添加到Marketplace产品.md` | 将地图模板添加到Marketplace产品 | 支持的功能；将地图模板添加到产品中；map, marketplace-map-templates, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/marketplace-map-templates/>) |
| `应用/地图/核心概念.md` | 核心概念 | 图层；Object样式；时间选择；core-concepts, map, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/core-concepts/>) |
| `应用/地图/概览.md` | 概览 | 地图上的地理空间数据；map, overview, 地图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/map/overview/>) |
| `应用/对象浏览器/Analyze and compare/使用图表进行探索.md` | 使用图表进行探索 | 图表；添加、移除和排序图表；链接对象上的图表；图表类型；Analyze and compare, explore-charts, object-explorer, 对象浏览器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-explorer/explore-charts/>) |
| `应用/对象浏览器/Analyze and compare/保存列表.md` | 保存列表 | 保存列表；访问保存的列表；Analyze and compare, object-explorer, save-lists, 对象浏览器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-explorer/save-lists/>) |
| `应用/对象浏览器/Analyze and compare/保存探索.md` | 保存探索 | 保存探索；访问已保存的探索；Analyze and compare, object-explorer, save-explorations, 对象浏览器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-explorer/save-explorations/>) |
| `应用/对象浏览器/Analyze and compare/应用操作.md` | 应用操作 | 操作；在其他应用中打开；导出；Analyze and compare, apply-actions, object-explorer, 对象浏览器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-explorer/apply-actions/>) |
| `应用/对象浏览器/Analyze and compare/查看结果.md` | 查看结果 | 按列排序表格；配置列；更改列顺序；调整列大小；Analyze and compare, object-explorer, view-results, 对象浏览器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-explorer/view-results/>) |
| `应用/对象浏览器/Analyze and compare/比较对象集.md` | 比较对象集 | 进入比较模式；筛选；协作；保存比较视图；Analyze and compare, compare-object-sets, object-explorer, 对象浏览器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-explorer/compare-object-sets/>) |
| `应用/对象浏览器/Analyze and compare/筛选结果.md` | 筛选结果 | 搜索栏；以属性（主要对象类型）筛选；以关键词筛选；添加术语修饰符；Analyze and compare, filter-results, object-explorer, 对象浏览器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-explorer/filter-results/>) |
| `应用/对象浏览器/Analyze and compare/通过旋转探索关联对象.md` | 通过旋转探索关联对象 | Analyze and compare, object-explorer, pivot-linked, 对象浏览器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-explorer/pivot-linked/>) |
| `应用/对象浏览器/Search and explore objects/搜索Objects.md` | 搜索Objects | 使用侧边栏导航；结果类型；排序结果；探索链接到特定结果的Objects；Search and explore objects, object-explorer, search-objects, 对象浏览器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-explorer/search-objects/>) |
| `应用/对象浏览器/Search and explore objects/搜索语法.md` | 搜索语法 | 引号；逻辑运算符 (AND/OR)；通配符；模糊搜索；Search and explore objects, object-explorer, search-syntax, 对象浏览器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-explorer/search-syntax/>) |
| `应用/对象浏览器/入门.md` | 入门 | 全局搜索栏 (A)；分组探索 (B, C, D)；使用对象类型分组进行搜索 (B)；在图上探索对象类型组 (D)；getting-started, object-explorer, 对象浏览器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-explorer/getting-started/>) |
| `应用/对象浏览器/概述.md` | 概述 | object-explorer, overview, 对象浏览器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-explorer/overview/>) |
| `应用/对象浏览器/生成 Object Explorer 链接.md` | 生成 Object Explorer 链接 | 生成仅关键字搜索；链接到探索；\[高级] 生成复杂搜索；generate-urls, object-explorer, 对象浏览器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-explorer/generate-urls/>) |
| `应用/对象浏览器/配置Object Explorer.md` | 配置Object Explorer | 首页可自定义Object类型分组；从操作成功提示链接到Object视图；在Object Explorer中隐藏操作；动态对象集上的操作；configure, object-explorer, 对象浏览器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-explorer/configure/>) |
| `应用/对象监视器/Core concepts/操作.md` | 操作 | 配置操作；受影响的对象；操作可见性设置；权限；Core concepts, actions, object-monitors, 对象监视器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-monitors/actions/>) |
| `应用/对象监视器/Core concepts/条件.md` | 条件 | 事件；阈值；函数支持；Core concepts, condition, object-monitors, 对象监视器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-monitors/condition/>) |
| `应用/对象监视器/Core concepts/活动.md` | 活动 | 活动事件类型；`监视器触发`；`监视器恢复`；`条件编辑`；Core concepts, activity, object-monitors, 对象监视器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-monitors/activity/>) |
| `应用/对象监视器/Core concepts/监控.md` | 监控 | 存储；保留；过期；Core concepts, monitor, object-monitors, 对象监视器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-monitors/monitor/>) |
| `应用/对象监视器/Core concepts/评估.md` | 评估 | 实时评估；调度监控器；非实时评估；手动评估；Core concepts, evaluation, object-monitors, 对象监视器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-monitors/evaluation/>) |
| `应用/对象监视器/Core concepts/输入.md` | 输入 | Core concepts, input, object-monitors, 对象监视器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-monitors/input/>) |
| `应用/对象监视器/Core concepts/通知.md` | 通知 | 自定义通知内容；模板化渲染；函数支持渲染；Core concepts, notifications, object-monitors, 对象监视器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-monitors/notifications/>) |
| `应用/对象监视器/Object Monitors.md` | Object Monitors | 访问 Object Monitors；object-monitors, overview, 对象监视器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-monitors/overview/>) |
| `应用/对象监视器/创建一个新Object监视器.md` | 创建一个新Object监视器 | 从Object Explorer创建；创建一个Object监视器；保存后；从Object监视器应用程序创建；create_new_object_monitor, object-monitors, 对象监视器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-monitors/create_new_object_monitor/>) |
| `应用/对象监视器/错误参考.md` | 错误参考 | 评估错误；监控器不同步；通知效果错误；操作效果错误；errors, object-monitors, 对象监视器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-monitors/errors/>) |
| `应用/对象监视器/限制.md` | 限制 | 规模限制；limits, object-monitors, 对象监视器, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-monitors/limits/>) |
| `应用/对象视图/Configuration/概述.md` | 概述 | 默认配置；编辑Object视图；使用Object视图编辑器；Configuration, config-overview, object-views, 对象视图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-views/config-overview/>) |
| `应用/对象视图/Configuration/管理Object视图版本.md` | 管理Object视图版本 | 使用说明；保存新版本；浏览历史记录；发布新版本；Configuration, manage-versions, object-views, 对象视图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-views/manage-versions/>) |
| `应用/对象视图/Configuration/配置 Workshop 标签页.md` | 配置 Workshop 标签页 | 创建新的 Workshop 标签页；编辑 Workshop 标签页；配置参数；权限；Configuration, config-workshop-tabs, object-views, 对象视图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-views/config-workshop-tabs/>) |
| `应用/对象视图/Configuration/配置应用程序侧边栏.md` | 配置应用程序侧边栏 | 设置应用程序侧边栏；编辑应用程序侧边栏；在侧边栏中添加/更改应用程序；Configuration, config-app-sidebar, object-views, 对象视图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-views/config-app-sidebar/>) |
| `应用/对象视图/Configuration/配置微件（旧版）.md` | 配置微件（旧版） | 微件配置；微件特定设置；微件格式设置；重用微件配置；Configuration, config-widgets, object-views, 对象视图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-views/config-widgets/>) |
| `应用/对象视图/Configuration/配置标签页.md` | 配置标签页 | 管理标签页；添加新标签页；删除标签页；移动标签页；Configuration, config-tabs, object-views, 对象视图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-views/config-tabs/>) |
| `应用/对象视图/Configuration/配置配置文件.md` | 配置配置文件 | 配置配置文件；指派配置文件给对象视图；作为用户切换配置文件；作为编辑器切换配置文件；Configuration, config-profiles, object-views, 对象视图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-views/config-profiles/>) |
| `应用/对象视图/Widgets/可视化.md` | 可视化 | 链接Object视图；配置；设置选项卡；时间轴；Widgets, object-views, widgets-visualization, 对象视图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-views/widgets-visualization/>) |
| `应用/对象视图/Widgets/属性和链接.md` | 属性和链接 | 属性微件；属性微件配置；Ontology Manager中的属性定义；属性微件本身的配置；Widgets, object-views, widgets-properties-links, 对象视图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-views/widgets-properties-links/>) |
| `应用/对象视图/Widgets/应用程序和文件.md` | 应用程序和文件 | Quiver Object 画布；Slate 应用程序；配置；在 Slate 中使用参数；Widgets, object-views, widgets-apps-files, 对象视图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-views/widgets-apps-files/>) |
| `应用/对象视图/Widgets/筛选.md` | 筛选 | 多选筛选；配置；下拉筛选；配置；Widgets, object-views, widgets-filtering, 对象视图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-views/widgets-filtering/>) |
| `应用/对象视图/Widgets/设计.md` | 设计 | 水平分布；配置；垂直堆叠容器；配置；Widgets, object-views, widgets-layout, 对象视图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-views/widgets-layout/>) |
| `应用/对象视图/在平台中使用Object View.md` | 在平台中使用Object View | 配置Object View；使用Object View；Workshop；Object Explorer；object-views, use-object-views-in-platform, 对象视图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-views/use-object-views-in-platform/>) |
| `应用/对象视图/对Object发表评论.md` | 对Object发表评论 | comment-on-objects, object-views, 对象视图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-views/comment-on-objects/>) |
| `应用/对象视图/概览.md` | 概览 | object-views, overview, 对象视图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-views/overview/>) |
| `应用/对象视图/添加Object视图到Marketplace产品.md` | 添加Object视图到Marketplace产品 | 支持的功能；将Object视图添加到产品中；marketplace-object-views, object-views, 对象视图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-views/marketplace-object-views/>) |
| `应用/对象视图/生成Object视图URL.md` | 生成Object视图URL | 生成Object链接；generate-urls, object-views, 对象视图, 应用 | [原文](<https://www.palantir.com/docs/zh/foundry/object-views/generate-urls/>) |
| `应用/本体管理器/Change management/保存对Ontology的更改.md` | 保存对Ontology的更改 | 保存您的更改；处理错误和警告；处理更新和合并冲突；放弃您的更改；Change management, ontology-manager, save-changes, 应用, 本体管理器 | [原文](<https://www.palantir.com/docs/zh/foundry/ontology-manager/save-changes/>) |
| `应用/本体管理器/Change management/审查和恢复更改.md` | 审查和恢复更改 | 审查对全局Ontology的更改；筛选对全局Ontology的更改；审查对单个Ontology资源的更改；恢复对单个object类型的更改；Change management, ontology-manager, restore-changes, 应用, 本体管理器 | [原文](<https://www.palantir.com/docs/zh/foundry/ontology-manager/restore-changes/>) |
| `应用/本体管理器/Ontology 清理.md` | Ontology 清理 | 访问 Ontology 清理工具；清理您的 Ontology；配置 Ontology 清理；Ontology 清理标记；cleanup, ontology-manager, 应用, 本体管理器 | [原文](<https://www.palantir.com/docs/zh/foundry/ontology-manager/cleanup/>) |
| `应用/本体管理器/Ontology 角色迁移.md` | Ontology 角色迁移 | 什么是 Ontology 角色？；定义；示例；迁移到 Ontology 角色；ontology-manager, ontology-roles-migration, 应用, 本体管理器 | [原文](<https://www.palantir.com/docs/zh/foundry/ontology-manager/ontology-roles-migration/>) |
| `应用/本体管理器/Ontology指标.md` | Ontology指标 | 关键术语；查看使用情况；启用Ontology使用情况；共享Ontology使用情况；ontology-manager, view-usage, 应用, 本体管理器 | [原文](<https://www.palantir.com/docs/zh/foundry/ontology-manager/view-usage/>) |
| `应用/本体管理器/导出、编辑和导入Ontology.md` | 导出、编辑和导入Ontology | 导出；导入；疑难解答；出错: `OntologyMetadata:UnreferencedRuleSets`；export-import, ontology-manager, 应用, 本体管理器 | [原文](<https://www.palantir.com/docs/zh/foundry/ontology-manager/export-import/>) |
| `应用/本体管理器/导航.md` | 导航 | 头部搜索栏；主页筛选；从选择中导航返回；navigation, ontology-manager, 应用, 本体管理器 | [原文](<https://www.palantir.com/docs/zh/foundry/ontology-manager/navigation/>) |
| `应用/本体管理器/概述.md` | 概述 | 访问应用程序；用户界面；Ontology Manager导航；发现；ontology-manager, overview, 应用, 本体管理器 | [原文](<https://www.palantir.com/docs/zh/foundry/ontology-manager/overview/>) |
| `应用/流程挖掘/创建机械流程.md` | 创建机械流程 | 要求；流程对象类型；变更日志数据集；流程日志对象类型；process-mining, process-mining-setup, 应用, 流程挖掘 | [原文](<https://www.palantir.com/docs/zh/foundry/process-mining/process-mining-setup/>) |
| `应用/流程挖掘/将流程挖掘操作化.md` | 将流程挖掘操作化 | 机械流程概览微件；输入数据；节点指标；节点和边样式；process-mining, process-mining-operationalize, 应用, 流程挖掘 | [原文](<https://www.palantir.com/docs/zh/foundry/process-mining/process-mining-operationalize/>) |
| `应用/流程挖掘/核心概念.md` | 核心概念 | 过程；状态；转换；操作；core-concepts, process-mining, 应用, 流程挖掘 | [原文](<https://www.palantir.com/docs/zh/foundry/process-mining/core-concepts/>) |
| `应用/流程挖掘/概述.md` | 概述 | 应用案例；overview, process-mining, 应用, 流程挖掘 | [原文](<https://www.palantir.com/docs/zh/foundry/process-mining/overview/>) |
| `应用/逻辑/AIP Logic Evaluations/入门.md` | 入门 | AIP Logic Evaluations, evaluations-getting-started, logic, 应用, 逻辑 | [原文](<https://www.palantir.com/docs/zh/foundry/logic/evaluations-getting-started/>) |
| `应用/逻辑/AIP Logic Evaluations/创建评估套件.md` | 创建评估套件 | 添加测试用例；评估函数；内置评估函数；市场部署函数；AIP Logic Evaluations, evaluations-create-suite, logic, 应用, 逻辑 | [原文](<https://www.palantir.com/docs/zh/foundry/logic/evaluations-create-suite/>) |
| `应用/逻辑/AIP Logic Evaluations/评估.md` | 评估 | 核心概念；AIP Logic Evaluations, evaluations-overview, logic, 应用, 逻辑 | [原文](<https://www.palantir.com/docs/zh/foundry/logic/evaluations-overview/>) |
| `应用/逻辑/AIP Logic Evaluations/评估指标仪表盘.md` | 评估指标仪表盘 | AIP Logic Evaluations, evaluations-metrics-dashboard, logic, 应用, 逻辑 | [原文](<https://www.palantir.com/docs/zh/foundry/logic/evaluations-metrics-dashboard/>) |
| `应用/逻辑/AIP Logic 常见问题解答.md` | AIP Logic 常见问题解答 | 我如何将 AIP Logic 与平台的其他部分一起使用？；我如何减少我的词元计数？；什么时候我应该将我的 Logic 函数保留在一个块中，而不是拆分成多个块？；我如何提高 AIP Logic 块的性能？；faq, logic, 应用, 逻辑 | [原文](<https://www.palantir.com/docs/zh/foundry/logic/faq/>) |
| `应用/逻辑/AIP Logic与自动化的集成.md` | AIP Logic与自动化的集成 | 从AIP Logic文件创建新的自动化；常见问题；为什么我看不到任何提案？；为什么**创建自动化**按钮不可用？；aip-logic-integration-automate, logic, 应用, 逻辑 | [原文](<https://www.palantir.com/docs/zh/foundry/logic/aip-logic-integration-automate/>) |
| `应用/逻辑/使用 AIP Logic 计算资源消耗.md` | 使用 AIP Logic 计算资源消耗 | 核心概念：资源、块和工具；使用 AIP Logic 测量 Foundry 计算；AIP LLM 词元；LLM 块执行；compute-usage, logic, 应用, 逻辑 | [原文](<https://www.palantir.com/docs/zh/foundry/logic/compute-usage/>) |
| `应用/逻辑/入门指南.md` | 入门指南 | 访问 AIP Logic；应用界面；工作流概述；输入、块和输出配置；getting-started, logic, 应用, 逻辑 | [原文](<https://www.palantir.com/docs/zh/foundry/logic/getting-started/>) |
| `应用/逻辑/核心概念.md` | 核心概念 | Logic函数；块；提示；工具；concepts, logic, 应用, 逻辑 | [原文](<https://www.palantir.com/docs/zh/foundry/logic/concepts/>) |
| `应用/逻辑/概述.md` | 概述 | logic, overview, 应用, 逻辑 | [原文](<https://www.palantir.com/docs/zh/foundry/logic/overview/>) |
| `应用/顶点/Configuration/在控制面板中配置Vertex设置.md` | 在控制面板中配置Vertex设置 | 图形默认设置；数据加载；模型配置；Configuration, vertex, vertex-settings-control-panel, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/vertex-settings-control-panel/>) |
| `应用/顶点/Configuration/配置链接合并.md` | 配置链接合并 | Configuration, link-merging, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/link-merging/>) |
| `应用/顶点/Events and time series/使用时间选择.md` | 使用时间选择 | Events and time series, use-time-selection, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/use-time-selection/>) |
| `应用/顶点/Events and time series/探索相关事件.md` | 探索相关事件 | 查看事件；事件徽章；事件Object；系列面板中的事件；Events and time series, explore-related-events, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/explore-related-events/>) |
| `应用/顶点/Events and time series/探索相关时间序列.md` | 探索相关时间序列 | Events and time series, explore-time-series, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/explore-time-series/>) |
| `应用/顶点/Events and time series/查看和筛选时间轴上的事件.md` | 查看和筛选时间轴上的事件 | 查看时间事件；筛选时间事件；更改光标位置；展开时间轴；Events and time series, timeline, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/timeline/>) |
| `应用/顶点/Events and time series/概述.md` | 概述 | Events and time series, events-overview, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/events-overview/>) |
| `应用/顶点/Events and time series/配置事件.md` | 配置事件 | 事件配置；Events and time series, configure-events, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/configure-events/>) |
| `应用/顶点/Events and time series/配置阈值.md` | 配置阈值 | Events and time series, configure-thresholds, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/configure-thresholds/>) |
| `应用/顶点/Graphs/Object和边显示选项.md` | Object和边显示选项 | 图设计；自动设计选项；层次结构（从左到右/从上到下）；网格；Graphs, graphs-display-options, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/graphs-display-options/>) |
| `应用/顶点/Graphs/从其他应用生成图表.md` | 从其他应用生成图表 | 使用URL参数生成图表；从其他应用生成Vertex图表；Graphs, generate-graph-apps, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/generate-graph-apps/>) |
| `应用/顶点/Graphs/使用函数派生属性.md` | 使用函数派生属性 | Graphs, derive-property-functions, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/derive-property-functions/>) |
| `应用/顶点/Graphs/使用函数生成图表.md` | 使用函数生成图表 | 搜索周边函数；提示与故障排除；参考示例：；Graphs, generate-graph-functions, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/generate-graph-functions/>) |
| `应用/顶点/Graphs/保存、共享和协作.md` | 保存、共享和协作 | 保存草稿；复制现有图表；版本控制；Graphs, save-share, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/save-share/>) |
| `应用/顶点/Graphs/创建图模板.md` | 创建图模板 | 使用图模板；Graphs, graphs-template, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/graphs-template/>) |
| `应用/顶点/Graphs/只读模式.md` | 只读模式 | 何时以只读模式打开 Vertex 图形？；Graphs, read-only-mode, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/read-only-mode/>) |
| `应用/顶点/Graphs/在Workshop模块中嵌入图形.md` | 在Workshop模块中嵌入图形 | 在Workshop中添加Vertex图形微件；选择资源；配置微件；Graphs, embed-graph-workshop, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/embed-graph-workshop/>) |
| `应用/顶点/Graphs/探索Object关系.md` | 探索Object关系 | 开始新的探索；Object选择面板；探索相关Objects；搜索周边；Graphs, explore-object-relationships, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/explore-object-relationships/>) |
| `应用/顶点/Graphs/探索现有图表.md` | 探索现有图表 | Object探索；关联事件；了解当前状态和随时间变化；筛选和探索Object属性；Graphs, graphs-explore, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/graphs-explore/>) |
| `应用/顶点/Scenarios/入门指南.md` | 入门指南 | 添加操作；选择操作；选择模型；新模型选择；Scenarios, scenarios-getting-started, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/scenarios-getting-started/>) |
| `应用/顶点/Scenarios/场景选项.md` | 场景选项 | 时间窗口选择；高级选项；范围；运行基线场景；Scenarios, scenarios-options, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/scenarios-options/>) |
| `应用/顶点/Scenarios/概览.md` | 概览 | Foundry中的业务逻辑和模型；场景的时间序列；Scenarios, scenarios-overview, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/scenarios-overview/>) |
| `应用/顶点/Scenarios/配置链式模型.md` | 配置链式模型 | Scenarios, chained-models, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/chained-models/>) |
| `应用/顶点/将 Vertex 图模板添加到 Marketplace 产品.md` | 将 Vertex 图模板添加到 Marketplace 产品 | 支持的功能；将 Vertex 图模板添加到产品中；marketplace-vertex, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/marketplace-vertex/>) |
| `应用/顶点/概览.md` | 概览 | overview, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/overview/>) |
| `应用/顶点/示例应用案例.md` | 示例应用案例 | 点选式流程图绘制；仿真、动态分析和决策优化；example-use-cases, vertex, 应用, 顶点 | [原文](<https://www.palantir.com/docs/zh/foundry/vertex/example-use-cases/>) |
| `本体架构/对象后端/Object Storage v1与Object Storage v2之间的重大变更.md` | Object Storage v1与Object Storage v2之间的重大变更 | 永久性重大变更；临时性重大变更；object-backend, object-storage-v2-breaking-changes, 对象后端, 本体架构 | [原文](<https://www.palantir.com/docs/zh/foundry/object-backend/object-storage-v2-breaking-changes/>) |
| `本体架构/对象后端/从对象存储 v1 (Phonograph) 迁移到对象存储 v2.md` | 从对象存储 v1 (Phonograph) 迁移到对象存储 v2 | 运行迁移前的考虑事项；迁移行为；不兼容的使用；非阻塞不兼容使用；object-backend, osv1-osv2-migration, 对象后端, 本体架构 | [原文](<https://www.palantir.com/docs/zh/foundry/object-backend/osv1-osv2-migration/>) |
| `本体架构/对象后端/概述.md` | 概述 | 功能组件和架构；Ontology 元数据服务 (OMS)；对象数据库；对象集服务 (OSS)；object-backend, overview, 对象后端, 本体架构 | [原文](<https://www.palantir.com/docs/zh/foundry/object-backend/overview/>) |
| `本体架构/对象后端/聚合注意事项.md` | 聚合注意事项 | Object Explorer 和 Workshop；Quiver 透视表和 Workshop 透视表；Ontology SDK (OSDK)；函数；aggregation-considerations, object-backend, 对象后端, 本体架构 | [原文](<https://www.palantir.com/docs/zh/foundry/object-backend/aggregation-considerations/>) |
| `本体架构/对象数据库/[遗留] Object Storage v1 (Phonograph).md` | [遗留] Object Storage v1 (Phonograph) | 目的；注册；索引状态；增量和批量重新索引；object-databases, object-storage-v1, 对象数据库, 本体架构 | [原文](<https://www.palantir.com/docs/zh/foundry/object-databases/object-storage-v1/>) |
| `本体架构/对象权限管理/多数据源Object类型（MDOs）.md` | 多数据源Object类型（MDOs） | 多数据源Object类型（MDOs）的类型；配置多数据源Object类型；常见问题解答；多数据源Object类型是否可用于索引到Object Storage v1（Phonograph）的Object类型？；multi-datasource-objects, object-permissioning, 对象权限管理, 本体架构 | [原文](<https://www.palantir.com/docs/zh/foundry/object-permissioning/multi-datasource-objects/>) |
| `本体架构/对象权限管理/概述.md` | 概述 | Ontology元数据；Ontology数据；object-permissioning, overview, 对象权限管理, 本体架构 | [原文](<https://www.palantir.com/docs/zh/foundry/object-permissioning/overview/>) |
| `本体架构/对象权限管理/管理Object类型和Object实例安全性.md` | 管理Object类型和Object实例安全性 | Object输入数据源；Foundry Ontology中的细粒度访问控制；Foundry受限视图（RVs）；多数据源Object类型（MDOs）；managing-object-security, object-permissioning, 对象权限管理, 本体架构 | [原文](<https://www.palantir.com/docs/zh/foundry/object-permissioning/managing-object-security/>) |
| `本体架构/对象权限管理/配置受限视图支持的对象类型.md` | 配置受限视图支持的对象类型 | 使用受限视图支持对象类型；安全配置；configuring-rv-access-controls, object-permissioning, 对象权限管理, 本体架构 | [原文](<https://www.palantir.com/docs/zh/foundry/object-permissioning/configuring-rv-access-controls/>) |
| `本体架构/对象索引/Funnel批处理管道.md` | Funnel批处理管道 | Funnel批处理管道的组成部分；更改记录；合并更改；索引；funnel-batch-pipelines, object-indexing, 对象索引, 本体架构 | [原文](<https://www.palantir.com/docs/zh/foundry/object-indexing/funnel-batch-pipelines/>) |
| `本体架构/对象索引/Funnel流式管道.md` | Funnel流式管道 | 流式Object类型的当前产品限制；配置流式Object类型；调试流式管道；funnel-streaming-pipelines, object-indexing, 对象索引, 本体架构 | [原文](<https://www.palantir.com/docs/zh/foundry/object-indexing/funnel-streaming-pipelines/>) |
| `本体架构/对象索引/常见问题解答.md` | 常见问题解答 | 如何知道一个对象类型何时已被索引到 OSv2 中？；为什么即使之前成功注册到 Object Storage v1（Phonograph），索引任务仍可能失败？；其中一个任务失败了，但如果我重试可能会成功。我该如何触发重建？；索引的数据大小是否有限制？；faq, object-indexing, 对象索引, 本体架构 | [原文](<https://www.palantir.com/docs/zh/foundry/object-indexing/faq/>) |
| `本体架构/对象索引/概述.md` | 概述 | object-indexing, overview, 对象索引, 本体架构 | [原文](<https://www.palantir.com/docs/zh/foundry/object-indexing/overview/>) |
| `本体架构/对象编辑/Object编辑和物化.md` | Object编辑和物化 | object-edits, overview, 对象编辑, 本体架构 | [原文](<https://www.palantir.com/docs/zh/foundry/object-edits/overview/>) |
| `本体架构/对象编辑/启用用户编辑历史.md` | 启用用户编辑历史 | 常见问题和注意事项；禁用编辑历史；object-edits, user-edit-history, 对象编辑, 本体架构 | [原文](<https://www.palantir.com/docs/zh/foundry/object-edits/user-edit-history/>) |
| `本体架构/对象编辑/应用操作时的权限检查.md` | 应用操作时的权限检查 | 单数据源Object的编辑；多数据源Object的编辑；创建Object；编辑或修改Object；object-edits, permission-checks, 对象编辑, 本体架构 | [原文](<https://www.palantir.com/docs/zh/foundry/object-edits/permission-checks/>) |
| `本体架构/对象编辑/物化.md` | 物化 | 物化的应用案例；创建物化数据集；数据输出数据集与物化数据集的比较；数据输出和物化数据集中的搭建计划；materializations, object-edits, 对象编辑, 本体架构 | [原文](<https://www.palantir.com/docs/zh/foundry/object-edits/materializations/>) |
| `本体架构/对象编辑/用户编辑的应用方式.md` | 用户编辑的应用方式 | 通过操作编辑对象；实时数据上的用户编辑；如何丢弃/清除/删除现有用户编辑；Ontology实体版本控制；how-edits-applied, object-edits, 对象编辑, 本体架构 | [原文](<https://www.palantir.com/docs/zh/foundry/object-edits/how-edits-applied/>) |
| `本体架构/对象编辑/管理模式更改.md` | 管理模式更改 | 更改对象类型模式；示例工作流；重大模式更改列表；非重大模式更改列表；object-edits, schema-migrations, 对象编辑, 本体架构 | [原文](<https://www.palantir.com/docs/zh/foundry/object-edits/schema-migrations/>) |
| `核心概念.md` | 核心概念 | Ontology；Object类型；属性；共享属性；core-concepts, ontology | [原文](<https://www.palantir.com/docs/zh/foundry/ontology/core-concepts/>) |
