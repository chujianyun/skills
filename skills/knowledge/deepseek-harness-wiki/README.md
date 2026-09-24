# deepseek-harness-wiki

面向 Agent 的 DeepSeek Harness 离线 Wiki Skill，来源为 <https://deepseek-harness.github.io/deepseek-harness/develop/basic>。

文档按原 Wiki 导航层级保存为 Markdown，并配有完整索引、本地全文检索和逐文档 SHA-256 清单。手动或自动同步会先比较内容哈希；没有变化时不会重写正文、索引或清单。

## 使用

调用 `$deepseek-harness-wiki` 后直接询问 DeepSeek Harness 的概念、使用、配置或排障问题。Agent 会先检索少量相关文档，再给出带本地文档路径的回答。

## 更新与边界

- 更新规则见 `references/UPDATE.md`，来源和许可边界见 `references/SOURCE.md`。
- 这是离线快照；版本敏感问题需要核对规范来源。
- 不包含真实凭据，不绕过登录、付费墙或访问控制。


上游文档按 MIT 许可证提供；版权及完整条款见 `UPSTREAM-LICENSE-MIT.txt`。
