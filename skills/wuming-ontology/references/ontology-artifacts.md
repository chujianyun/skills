# 本体产物规范

本规范是 Skill 的生成扩展，不属于抓取的 Palantir 官方文档。生成的是基于业务材料和 Palantir 建模方法设计的 OWL 本体，不声称是 Foundry 原生导出、部署配置或可直接导入的格式。保留现有 Wiki 快照及其清单。

## 模型与映射

先确定业务问题、范围、主要对象与关系；不强制用户填写固定表格。缺少业务领域且上下文不能推断时询问，不凭空生成业务事实。示例实例必须注明为虚构，不把用户业务数据写入 Skill 或公开仓库。

| Palantir / 业务概念 | OWL 表达 | 注意事项 |
| --- | --- | --- |
| Object type | `owl:Class` | 英文稳定 IRI + 中文 `rdfs:label` 和 `rdfs:comment` |
| Object | `owl:NamedIndividual` + 业务类的 `rdf:type` | 仅按用户需要添加实例；与类层区分 |
| 标量属性 | `owl:DatatypeProperty` | 指定 `rdfs:domain` 和 XSD `rdfs:range` |
| Link type | `owl:ObjectProperty` | 明确方向、domain、range；双向链接按需要声明 `owl:inverseOf` |
| 继承 | `rdfs:subClassOf` | 仅表示真实的“是一种”，不把所有关联都当继承 |
| 接口 | 按语义采用类层次或注释 | OWL 类不是 Foundry 运行时接口，能力与实现细节另作说明 |
| 操作、函数、权限、索引、数据源和工作流 | 注释或单独的业务说明 | 不虚构对应的可执行 OWL 语义；可将业务事件建模为类，但不声称实现操作 |
| 必填、唯一、主键、数组、关联数量 | 逐项审查后建模 | 不机械映射数据库约束；OWL 不是表单或记录完整性校验器 |

- Turtle 是序列化语法，`.ttl` 内必须实际使用 OWL 词汇；不能把普通 RDF、JSON 或图表改后缀当作 OWL。
- 使用标准 `rdf:`、`rdfs:`、`owl:`、`xsd:` 前缀及领域前缀；给本体声明 `a owl:Ontology`、名称、说明。引用外部词汇时保留 IRI；未知外部实体类型不擅自补定义。
- 新模型用绝对、稳定 IRI；未指定时采用 `https://example.org/ontology/<slug>#` 占位命名空间并说明可替换。禁止使用本机文件路径作为命名空间；已有模型保留原 IRI。
- 字符串用 `xsd:string`，布尔用 `xsd:boolean`，整数用 `xsd:integer`，小数用 `xsd:decimal`，日期用 `xsd:date`，带时区日期时间用 `xsd:dateTime`（例如 `2026-01-01T08:00:00Z`）。保留更精细的原数据类型及其范围。附件、向量、地理等类型没有通用无损映射，记录选择和损失；数组的重复属性值不保留顺序和重复次数，需保序时显式建模有序条目。
- 同一属性多个 `rdfs:domain` / `rdfs:range` 表示交集。共享属性若表示“属于任意一种类”，按需求用 `owl:unionOf` 或共同父类，不能简单重复 domain。没有业务依据时不添加不相交、等价、传递、逆函数或基数公理。
- OWL 使用开放世界语义，没有值不自动代表违规；最大基数还可能推出个体相等。`owl:hasKey` 与唯一性校验不同；`owl:FunctionalProperty` 不表示属性必填。业务完整性校验可另行建议 SHACL，未要求时不擅自增加第三种交付物。

## 文件与依赖

默认交付 `model.ttl` 和 `model.html`；用户指定的名字优先。HTML 是 TTL 的浏览视图，不是单独维护的另一份模型。仅 HTML 请求使用临时 TTL；只需 TTL 则不生成 HTML。

检索仍只依赖 Python 3 标准库。产物脚本需要 Python 3.10+ 和 RDFLib 7.x。使用已有满足条件的解释器，或在获得安装授权后创建独立环境：

```bash
python3 -m venv <venv-dir>
<venv-dir>/bin/python -m pip install 'rdflib>=7,<8'
<venv-dir>/bin/python -c "import rdflib; print(rdflib.__version__)"
```

检查当前解释器的 `import rdflib` 是否成功且主版本为 7；失败时也可检查已有的专用环境 `~/.local/share/skill-venvs/wuming-ontology/bin/python`，存在且满足版本时复用。否则在获得安装授权后按上面的命令创建环境。缺少 RDFLib 时，脚本非零退出并说明安装方法，不自动安装。Agent 可以先写 TTL 草稿，但必须标为未解析验证；HTML 生成暂缓，不用正则模拟 Turtle 解析器。浏览器仅用于最终交互验证，HTML 打开无需 Python、服务端、网络或 CDN。

从 Skill 根目录运行（实际执行时将相对路径换成确定的 Skill 根目录路径）：

```bash
# 仅解析、基础检查和数量报告，不改写输入
<python> scripts/ontology_artifacts.py <model.ttl>
# 校验通过后按同一图生成 HTML
<python> scripts/ontology_artifacts.py <model.ttl> --html <model.html>
# 可运行的虚构业务示例
<python> scripts/ontology_artifacts.py assets/example-ontology.ttl --html <new-output-dir>/example.html
# 产物脚本的回归测试
<python> -m unittest discover -s scripts/tests -v
```

目标已存在时默认拒绝；确认覆盖对象后才加 `--overwrite`，不得覆盖输入 TTL（包含链接指向同一文件的情况）。本脚本只读取本地 Turtle，不解析其他格式、不跟随 `owl:imports`、不抓取 IRI 内容、不调用 Foundry。导入公理只会作为原始三元组保留；依赖的外部定义需另行授权获取或由用户提供。

## 验证与 HTML 交付

脚本检查 Turtle 可解析、非空、存在命名的 `owl:Ontology`、存在显式声明的 OWL 类或属性，并报告标签缺失、缺少属性 domain/range、未展开 imports、未解析的外部引用及本机文件 IRI。这是本 Skill 的交付基线，不代表所有合法 OWL 都必须有这些声明。外部引用或结构警告不直接判定本体非法；结合用户模型解释，不盲目改写。

HTML 自包含 CSS、JavaScript 和数据，采用系统字体；显示名称、数量、关系图、图例、可搜索实体列表、完整 IRI、属性和公理详情、分页的完整三元组。类关系图投影直接的类继承及对象属性 domain → range；多个 domain/range 的投影线只是展示，并列声明仍为交集。匿名类、限制、公理、未指定 domain/range 的关系和实例不强行摊平为普通类边，通过详情及三元组完整保留。页面显示投影范围，不能把视图当作全部推理结果。

浏览器验证至少检查：离线打开无脚本错误；搜索与点击实体能定位详情；缩放、重置和三元组分页可用；继承、链接方向和实体数量与 TTL 对得上。窄屏可操作，长 IRI 可换行，标签和注释作为文本呈现。不能运行浏览器时如实报告未验证。

解析失败或结构检查失败时脚本非零退出，不输出成功报告或创建 HTML。不要把“可解析”写成“OWL 2 DL 合规”“推理一致”“满足全部业务约束”或“Foundry 可导入”。如用户要求这些结论，另行选择合适的 OWL profile 检查器、推理器、SHACL 校验器或产品环境；缺少工具时明确停止在已完成的验证层级。

## 规范来源

以下是生成扩展使用的规范来源，与离线 Wiki 快照分开；不据此改写快照：

- [W3C OWL 2 Primer](https://www.w3.org/TR/owl2-primer/)：类、属性、实例、domain/range、基数和开放世界语义。
- [W3C RDF 1.1 Turtle](https://www.w3.org/TR/turtle/)：序列化语法与 IRI。
- [RDFLib 文档](https://rdflib.readthedocs.io/en/stable/intro_to_parsing/)：本地 Turtle 的解析与序列化。

Palantir 概念按实际需求检索 `references/docs/定义本体/对象链接类型/类型参考.md`、属性、链接、接口和操作文档；引用实际读过的页面，不把本规范或示例说成 Palantir 官方文档。
