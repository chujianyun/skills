---
name: palantir-ontology-wiki
description: "检索 Palantir Foundry Ontology 中文离线文档，并生成 .ttl（OWL 本体）与 HTML 可视化产物。用于 Palantir 概念解释、建模、配置、排障，或基于其对象、属性、链接建模方法交付领域本体；不用于泛哲学本体论或其他图谱产品的配置与排障。"
---

# Palantir Ontology Wiki

使用随 Skill 打包的 Wiki 文档回答问题。离线文档是第一依据；只有本地材料不足、用户要求核对最新版或问题超出快照范围时，才补查规范来源。

先判断任务：概念、配置与排障走回答工作流；要求“生成、导出、交付本体”或指定 `.ttl` / HTML 时，在检索后走产物工作流。普通问答不强制生成文件。已有 TTL 的校验或可视化可直接走产物工作流，无须检索无关 Wiki。

## 资源

- [文档索引](references/INDEX.md)：浏览完整主题结构或搜索词不确定时读取。
- [来源与范围](references/SOURCE.md)：回答版本、许可证、完整性或时效性问题时读取。
- [抓取与覆盖核对](references/capture-method.md)：确认导航、正文、图片解析方法及已知缺图时读取。
- [抓取报告](references/capture-report.json)：查询有效配图数量和全部失效原地址。
- [更新协议](references/UPDATE.md)：用户要求刷新、同步或自动更新本 Wiki Skill 时读取。
- `references/docs/`：保持 Wiki 导航层级的 Markdown 正文；只读取与问题直接相关的文件。
- `references/wiki-manifest.json`：页面来源、路径和逐文档 SHA-256 清单。
- `scripts/search_docs.py`：零第三方依赖的本地全文检索。
- [本体产物规范](references/ontology-artifacts.md)：生成或转换本体时读取，包含 Palantir → OWL 映射、语义边界、依赖和验证步骤。
- [示例本体](assets/example-ontology.ttl)：生成时可参考的虚构设备维护模型，不代表官方导出格式。
- `scripts/ontology_artifacts.py`：解析与基础校验 TTL，按同一图生成独立离线 HTML；仅此产物脚本需要 RDFLib。
- `assets/ontology-viewer.html`：脚本使用的可视化模板，不作为业务本体的数据来源。

## 范围与检索提示

这是 Palantir Foundry 的 Ontology 中文导航快照，覆盖本体定义、相关应用和底层架构；不是整个 Foundry、完整 OSDK 或独立 API Reference。中文内容为官网机器翻译，配图有已知缺失；不要自行补画缺图或将英文新版本悄悄混入快照。

- 概念与建模：搜索 `Object类型`、`属性`、`链接类型`、`操作类型` 或 `接口`；可加 `--prefix 定义本体`。
- 函数与业务逻辑：同时保留 `TypeScript`、`Python`、`OntologyEditFunction` 等代码术语；可加 `--prefix 定义本体/函数`。
- 权限、索引、Object Storage 与编辑：可加 `--prefix 本体架构`；Ontology Manager 位于 `应用/本体管理器`。
- Object Explorer、Object Views、Vertex、地图等应用位于 `应用/`；只覆盖原 Ontology 导航中的页面。

## 回答工作流

1. 从当前 `SKILL.md` 所在目录确定 Skill 根目录，不假设用户工作目录。
2. 把问题提炼为 2–5 个关键词，保留产品名、类名、命令、包名和错误码。
3. 运行：

   ```bash
   python3 <skill-root>/scripts/search_docs.py "<keywords>"
   ```

   搜索过宽时加 `--prefix <directory>`；没有结果时换同义词或旧/新术语重试一次。
4. 读取排名最高且互相补充的 1–3 篇文档。需要理解主题全貌时再读索引，不一次加载全部语料。
5. 根据已读资料给出直接结论、必要步骤和前置条件。版本、包名、导入路径、配置键和命令不能凭记忆补全。
6. 文档不足或用户要求最新版时，只补查 `references/SOURCE.md` 指定的规范来源，并明确标为在线补充。

## 产物工作流

1. 阅读[本体产物规范](references/ontology-artifacts.md)。复用用户提供的业务材料或已有 TTL；缺少业务范围时才询问。可选信息采用注明的假设：未指定格式时默认同名 `.ttl` + `.html`，也支持仅 TTL 或仅 HTML；未指定命名空间时使用明确标为占位符的 `https://example.org/ontology/<slug>#`。
2. 新建模型时按回答工作流检索相关对象、属性、链接、接口或操作文档，先提炼类、属性、关系、数据类型和必要限制。已有模型不擅自改变命名空间或 IRI。区分用户事实、设计建议、假设及无法等价映射的行为。
3. 将模型写为 UTF-8 Turtle，包含 `owl:Ontology` 和显式 OWL 实体声明。TTL 是两种产物的共同数据来源；仅需 HTML 时在临时目录保留中间 TTL，不额外交付。现有 TTL 允许保留原格式与内容，只校验和渲染。
4. 按规范检查依赖，运行 `scripts/ontology_artifacts.py <model.ttl>`；需 HTML 时追加 `--html <model.html>`。解析或基础检查失败时修复本轮生成的文件并复查，不能把失败稿标为完成；用户既有模型的语义修改先说明影响，未经授权不改。
5. 检查 HTML 可打开、无脚本错误，搜索、实体详情、关系方向和数量与 TTL 一致；匿名限制与未投影到关系图的公理须能在完整三元组中查询。未运行浏览器时明确标为未验证，不把静态检查说成实际运行。
6. 把产物放到用户指定目录；未指定时用当前工作区中新建的 `ontology-output/<slug>/`。写入前检查同名文件；覆盖既有文件、部署 Foundry、公开发布或外部写入需核实具体授权，缺少时确认或改用新路径。`--overwrite` 只能在已获授权后使用。完成后按输出契约交付并停止。

## 更新入口

用户要求更新本 Wiki Skill 时，完整阅读 [更新协议](references/UPDATE.md)。必须重新抓取完整范围到临时目录并先 dry-run；内容与元数据都没变化时保持正文、索引和清单原样。未经授权不得归档上游删页、创建后台任务、提交、推送或公开发布。

## 常见陷阱

- 离线快照不天然代表最新版本；版本敏感问题先看来源边界。
- 搜索无结果不等于功能不存在。更换产品术语、类名、命令或目录前缀后再判断。
- 同一主题可能分散在概览、教程、参考和排障文档；必要时交叉读取。
- 示例中的凭据只能当占位符，不读取、输出或写入用户真实密钥。
- 清单中的来源 URL 只用于溯源，不能据此绕过登录或访问控制。

## 输出契约

问答：给出直接结论或可执行做法，以及 `参考文档` 列表（实际读取的 `references/docs/...` 相对路径）。快照可能过期、资料冲突或使用在线补充时再添加版本说明。证据不足时明确列出已搜索关键词和语料缺口，不编造答案。

产物：交付实际生成文件的可点击链接、命名空间、类/对象属性/数据属性/实例数量、校验结论、假设及映射损失，以及实际使用的参考文档。校验区分 Turtle 解析、基础结构检查、浏览器实测、OWL 推理和 Foundry 导入；后两项未执行就明确未验证。只返回代码块不算完成文件交付；若环境不能写文件，说明限制并提供完整内容及保存方法，标为待落盘。仅处理已有 TTL 时，没有读取 Wiki 就不编造参考路径。
