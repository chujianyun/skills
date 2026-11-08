# palantir-ontology-wiki

面向 Agent 的 Palantir Ontology 离线 Wiki Skill，来源为 <https://www.palantir.com/docs/zh/foundry/ontology/overview>。

文档按原 Wiki 导航层级保存为 Markdown，并配有完整索引、本地全文检索和逐文档 SHA-256 清单。手动或自动同步会先比较内容哈希；没有变化时不会重写正文、索引或清单。

## 使用

调用 `$palantir-ontology-wiki` 后直接询问 Palantir Ontology 的概念、使用、配置或排障问题。Agent 会先检索少量相关文档，再给出带本地文档路径的回答。

## 更新与边界

- 更新规则见 `references/UPDATE.md`，来源和许可边界见 `references/SOURCE.md`。
- 这是离线快照；版本敏感问题需要核对规范来源。
- 不包含真实凭据，不绕过登录、付费墙或访问控制。

## 当前快照

316 篇官方中文正文，944 张有效配图；65 个官方失效图片地址已逐处标注（正文完整、配图不完整，用户已接受）。附零依赖抓取器、本地检索、导航索引、逐文件哈希和增量同步工具。完整边界与上游许可见 [来源说明](references/SOURCE.md)。
