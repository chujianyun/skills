# palantir-ontology-wiki

面向 Agent 的 Palantir Ontology 离线 Wiki Skill，来源为 <https://www.palantir.com/docs/zh/foundry/ontology/overview>。

文档按原 Wiki 导航层级保存为 Markdown，并配有完整索引、本地全文检索和逐文档 SHA-256 清单。手动或自动同步会先比较内容哈希；没有变化时不会重写正文、索引或清单。

## 使用

调用 `$palantir-ontology-wiki` 后直接询问 Palantir Ontology 的概念、使用、配置或排障问题。Agent 会先检索少量相关文档，再给出带本地文档路径的回答。

也可以要求生成本体文件，例如：

> 用设备、场地和维护工单建立本体，交付 OWL Turtle（.ttl）和 HTML 可视化。

默认交付同一模型的 `.ttl` 和 `.html`，也可指定一种格式。HTML 可离线打开，支持实体搜索、关系图缩放、属性与公理详情、完整三元组查询。已有 TTL 也能直接校验和可视化。

产物脚本需要 Python 3.10+ 和 RDFLib 7.x；检索仍为零第三方依赖。安装、命令及语义边界见[本体产物规范](references/ontology-artifacts.md)。可使用 [虚构设备维护示例](assets/example-ontology.ttl) 试运行：

```bash
python scripts/ontology_artifacts.py assets/example-ontology.ttl --html /tmp/maintenance-example.html
```

这是基于 Palantir 建模方法设计的 OWL 本体，不代表 Foundry 原生导出或直接可导入格式；Turtle 解析和基础检查通过不代表推理一致或业务约束验证通过。

## 更新与边界

- 更新规则见 `references/UPDATE.md`，来源和许可边界见 `references/SOURCE.md`。
- 这是离线快照；版本敏感问题需要核对规范来源。
- 不包含真实凭据，不绕过登录、付费墙或访问控制。

## 当前快照

316 篇官方中文正文，944 张有效配图；65 个官方失效图片地址已逐处标注（正文完整、配图不完整，用户已接受）。附零依赖抓取器、本地检索、导航索引、逐文件哈希和增量同步工具。完整边界与上游许可见 [来源说明](references/SOURCE.md)。
