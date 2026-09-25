---
name: qianwenai-wiki
description: 千问AI平台（Qianwen AI Platform / DashScope）官方文档离线知识库，用于检索并回答模型选择、API Key、OpenAI 兼容接口、DashScope SDK、文本与多模态生成、图像/视频/语音、Realtime API、Embedding、Reranking、Function Calling、MCP、批量调用、计费、Token Plan、API/SDK/CLI 参考和模型更新等问题，也可基于官方文档生成示例代码与排障建议。当用户提到千问AI平台、Qianwen AI Platform、DashScope、通义千问 API、百炼 API、DASHSCOPE_API_KEY 或具体千问/万相模型接入时使用；千问聊天产品的一般使用、模型原理论文解读或无关的阿里云产品问题不使用。
---

# 千问AI平台 Wiki

使用随 Skill 打包的千问AI平台官方文档回答问题。先查离线快照，只有离线资料不足、用户要求核对最新版或问题明显涉及快照后的变更时才联网查官方站点。

## 资源

- [文档索引](references/INDEX.md)：官方 `llms.txt` 目录快照，按栏目列出全部页面。需要浏览主题结构、确认覆盖范围或检索不稳定时读取。
- [来源与快照说明](references/SOURCE.md)：记录官方入口、快照范围、完整性校验与版权边界。回答时效性或来源问题时读取。
- `references/SNAPSHOT.json`：机器可读的文件清单、原始 URL、大小与 SHA-256。需要核对精确来源或快照完整性时查询。
- `references/docs/`：离线 Markdown 与 OpenAPI JSON 正文。只读取与问题直接相关的文件。
- `scripts/search_docs.py`：零第三方依赖的全文检索工具。
- `scripts/sync_docs.py`：从官方 `llms.txt` 重新同步全部文档；覆盖现有快照必须显式传入 `--replace`。

## 工作流

1. 从当前 `SKILL.md` 所在目录确定 Skill 根目录，不要假设用户工作目录。
2. 将问题提炼为 2–6 个中英文关键词，保留模型名、接口名、参数名、错误码和 SDK 类名。
3. 先运行全文检索：

   ```bash
   python3 <skill-root>/scripts/search_docs.py "qwen3.5 function calling tools" --prefix developer-guides
   ```

   API 结构问题可用 `--prefix api-reference`，计费问题可用 `--prefix resources` 或 `--prefix token-plan`。没有结果时换用中文术语、英文术语、模型名或参数名重试一次。
4. 读取排名最高且互相补充的 1–3 篇资料。概念与使用流程优先读 `developer-guides/`；精确字段、请求和响应优先读 `api-reference/` 或根目录 `openapi-*.json`；价格与限额优先读 `resources/` 和 `token-plan/`；版本变化读 `changelog/`。
5. 对照文档给出直接结论、前置条件、代码与排障步骤。版本、模型名、端点、参数和环境变量必须来自实际读取的资料，不凭记忆补全。
6. 同一能力同时提供 OpenAI 兼容接口与 DashScope 原生接口时，明确用户正在使用哪一种；用户未指定时，说明两者差异并给出文档中更通用的方案。
7. 离线文档不足或用户要求最新版时，只补查千问AI平台、阿里云百炼或 DashScope 官方资料，并把新信息标为“联网补充”。不要用第三方博客覆盖官方结论。
8. 用用户的语言回答，并列出实际采用的离线文档相对路径；需要引用原始页面时，从 `SNAPSHOT.json` 或文档中的 Documentation Index 获取官方 URL。

## 常见陷阱

- 这是离线快照，不代表实时价格、免费额度、模型上下线状态或限流规则。此类问题必须说明快照日期，并在可联网时核对官方页面。
- 千问AI平台文档会同时出现千问AI平台、DashScope、阿里云百炼等名称。不要仅凭名称判断接口兼容性；以文档给出的端点和 SDK 为准。
- OpenAI 兼容接口、DashScope HTTP API、DashScope SDK、Anthropic 兼容接口和 Realtime 协议并不等价。不要混用请求字段、Base URL 或鉴权方式。
- 文档可能同时保留新旧模型和多代万相接口。优先使用用户指定模型对应页面；未指定时先查模型选择与更新日志，不擅自推荐已下线型号。
- 根目录 `openapi-*.json` 适合核对精确 Schema，说明性流程以对应 Markdown 为主。两者冲突时说明冲突，并联网核对官方当前页面。
- 示例中的 API Key 只能当占位符。不要读取、输出或写入用户真实凭据；实际调用可能产生费用，未经用户明确要求和确认不要替用户发起付费 API 请求。
- 搜索无结果不等于能力不存在。先换用模型名、产品旧称、中文/英文同义词和目录过滤；仍无依据时明确说未找到，不编造 API。

## 刷新快照

只有用户明确要求更新离线文档时才执行联网刷新。先运行不带 `--replace` 的命令检查目标状态；已有快照时，说明将覆盖 `references/docs/`、`INDEX.md` 和 `SNAPSHOT.json`，取得确认后再加 `--replace`：

```bash
python3 <skill-root>/scripts/sync_docs.py --replace
python3 <skill-root>/scripts/search_docs.py "DASHSCOPE_API_KEY first API call"
```

同步脚本先在临时目录完成下载和校验，任一页面失败时停止且保留旧快照。不要把 Cookie、Token 或 API Key 写入同步脚本、文档或日志。

## 输出契约

回答至少包含：

1. 直接结论或可执行做法。
2. 必要的接口类型、前置条件、代码、配置或排障步骤。
3. `参考文档`：列出实际读取的 `references/docs/...` 相对路径。
4. `版本说明`：仅在价格/模型状态等时效性信息、文档冲突、快照可能过期或使用联网补充时添加。

若证据不足，明确说“当前离线文档未找到可靠依据”，列出已搜索的关键词，不猜测参数或端点。
