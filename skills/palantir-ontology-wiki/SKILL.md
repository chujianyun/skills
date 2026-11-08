---
name: palantir-ontology-wiki
description: "Palantir Foundry Ontology 官方中文离线文档，覆盖本体、对象与链接类型、操作、函数、接口、Ontology Manager、权限、索引及相关应用。用于 Palantir 本体概念解释、建模、配置和排障；不用于泛哲学本体论或其他图谱产品。"
---

# Palantir Ontology Wiki

使用随 Skill 打包的 Wiki 文档回答问题。离线文档是第一依据；只有本地材料不足、用户要求核对最新版或问题超出快照范围时，才补查规范来源。

## 资源

- [文档索引](references/INDEX.md)：浏览完整主题结构或搜索词不确定时读取。
- [来源与范围](references/SOURCE.md)：回答版本、许可证、完整性或时效性问题时读取。
- [抓取与覆盖核对](references/capture-method.md)：确认导航、正文、图片解析方法及已知缺图时读取。
- [抓取报告](references/capture-report.json)：查询有效配图数量和全部失效原地址。
- [更新协议](references/UPDATE.md)：用户要求刷新、同步或自动更新本 Wiki Skill 时读取。
- `references/docs/`：保持 Wiki 导航层级的 Markdown 正文；只读取与问题直接相关的文件。
- `references/wiki-manifest.json`：页面来源、路径和逐文档 SHA-256 清单。
- `scripts/search_docs.py`：零第三方依赖的本地全文检索。

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

## 更新入口

用户要求更新本 Wiki Skill 时，完整阅读 [更新协议](references/UPDATE.md)。必须重新抓取完整范围到临时目录并先 dry-run；内容与元数据都没变化时保持正文、索引和清单原样。未经授权不得归档上游删页、创建后台任务、提交、推送或公开发布。

## 常见陷阱

- 离线快照不天然代表最新版本；版本敏感问题先看来源边界。
- 搜索无结果不等于功能不存在。更换产品术语、类名、命令或目录前缀后再判断。
- 同一主题可能分散在概览、教程、参考和排障文档；必要时交叉读取。
- 示例中的凭据只能当占位符，不读取、输出或写入用户真实密钥。
- 清单中的来源 URL 只用于溯源，不能据此绕过登录或访问控制。

## 输出契约

回答至少包含：直接结论或可执行做法，以及 `参考文档` 列表（实际读取的 `references/docs/...` 相对路径）。快照可能过期、资料冲突或使用在线补充时再添加版本说明。证据不足时明确列出已搜索关键词和语料缺口，不编造答案。
