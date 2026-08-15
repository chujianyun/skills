# Skills

这是悟鸣公开维护的一组 Agent Skills，偏实战、偏工作流，主要服务于 AI 工具使用、文档解读、项目配置、运维排障与技能分发。

和“技能清单”相比，这个仓库更适合被理解成一张**能力地图**：每个 skill 不只是一个说明文件，而是围绕某一类任务组织起来的可复用能力单元。

---

## Skill 地图

仓库采用 `skills/<category>/<skill-name>/` 三级目录。物理分类由 [`config/skill-categories.json`](config/skill-categories.json) 统一管理：

| 分类 | 主要职责 |
|---|---|
| `knowledge` | 产品文档、知识库、领域资料 |
| `review` | Prompt、Agent、配置和 Skill 审查优化 |
| `career` | 职级评估、晋升与职业建议 |
| `content` | 文章、论文、源码解读与文本加工 |
| `visual` | 图示、视觉资产与二维码 |
| `media` | 音频、PDF、图片下载与媒体处理 |
| `operations` | 服务运维、故障排查与平台接入 |
| `distribution` | 安装、同步、发布与分发 |

README 的能力地图可以按使用场景细分展示，但新 Skill 的物理目录只能选择上述八类之一。

### 1. 文档 / 知识库类（Tool Wrapper）

这类 skill 的核心价值，是把某个产品、系统或知识域的资料包装成可按需触发的上下文。

| Skill | 模式 | 适用场景 |
|---|---|---|
| [llama-index-wiki](skills/knowledge/llama-index-wiki/SKILL.md) | Tool Wrapper | 检索 LlamaIndex Python 用户文档，回答 RAG、索引、检索、Agent、Workflow、集成、评估、部署与 LlamaParse 问题 |
| [qianwenai-wiki](skills/knowledge/qianwenai-wiki/SKILL.md) | Tool Wrapper | 检索千问AI平台官方文档，回答模型接入、OpenAI 兼容与 DashScope API、文本/多模态生成、Realtime、计费和排障问题 |
| [qoder-wiki](skills/knowledge/qoder-wiki/SKILL.md) | Tool Wrapper | 用户询问 Qoder 的安装、使用、功能、定价、MCP、快捷键、Quest Mode、Repo Wiki 等 |

---

### 2. 配置审查 / 结构优化类（Reviewer / Inversion）

这类 skill 的重点不是“直接干活”，而是**先判断、先诊断、再给方案**。

| Skill | 模式 | 适用场景 |
|---|---|---|
| [prompt-optimizer](skills/review/prompt-optimizer/SKILL.md) | Reviewer / Generator | 优化 Prompt、改进 AI 指令、为特定任务挑选提示词框架 |
| [agent-md-advisor](skills/review/agent-md-advisor/SKILL.md) | Advisor / Reviewer / Generator | 回答 AGENTS.md / CLAUDE.md 最佳实践，诊断并优化 AI agent 指令文件 |
| [claude-config-advisor](skills/review/claude-config-advisor/SKILL.md) | Reviewer / Inversion | 审查或设计 `.claude`、`CLAUDE.md`、Claude Code 项目配置 |
| [skill-optimizer](skills/review/skill-optimizer/SKILL.md) | Reviewer / Inversion | 审查并优化已有 skill 的触发语义、工作流、确认门槛和资源组织 |
| [agent-optimizer](skills/review/agent-optimizer/SKILL.md) | Reviewer / Consultant | 基于 12-Factor AgentOps 框架，提供 Agent 设计咨询、审查现有 Agent/Skill/工作流设计，发现问题并给出改进建议 |

---

### 3. 职业能力 / 成长与思维提升类（Advisor / Reviewer）

这类 skill 适合把抽象的岗位能力与思维框架，转成具体的评估、判断、建议和成长路径。

| Skill | 模式 | 适用场景 |
|---|---|---|
| [five-perspective-analysis](skills/career/five-perspective-analysis/SKILL.md) | Advisor / Reviewer | 从用户、业务、一线执行、技术和公司经营五种角色交叉分析产品、技术、项目、业务与职业问题，形成有取舍的综合判断 |
| [p7-advisor](skills/career/p7-advisor/SKILL.md) | Advisor / Reviewer | 按一线大厂 P7“团队级专家”能力模型，评估晋升准备度、项目证据、简历表达、面试准备和成长短板 |
| [p8-advisor](skills/career/p8-advisor/SKILL.md) | Advisor / Reviewer | 按一线大厂 P8“领域级负责人”能力模型，评估领域战略、跨团队影响、机制建设、梯队培养和 P7 到 P8 的差距 |
| [p9-advisor](skills/career/p9-advisor/SKILL.md) | Advisor / Reviewer | 按一线大厂 P9“业务/组织级负责人”能力模型，评估战略判断、资源整合、组织建设、高层影响力和 P8 到 P9 的差距 |

---

### 4. 图示 / 可视化类（Generator）

这类 skill 的核心是：**把抽象结构、流程和关系，稳定转成可直接渲染的图**。

| Skill | 模式 | 适用场景 |
|---|---|---|
| [mermaid](skills/visual/mermaid/SKILL.md) | Generator / Reviewer | 用户要求绘制 Mermaid 流程图、架构图、时序图、状态图、甘特图、ER 图、类图、旅程图等 |

---

### 5. 写作 / 表达优化类（Pipeline / Generator）

这类 skill 的核心是：**保留作者原意，把已有文本改成更自然、更可发布的表达**。

| Skill | 模式 | 适用场景 |
|---|---|---|
| [remove-ai-flavor](skills/content/remove-ai-flavor/SKILL.md) | Pipeline / Generator / Reviewer | 识别并改写文章、公众号稿、自媒体稿、口播稿、演讲稿、课程稿、产品文案中的 AI 痕迹、模板腔、资料味、翻译腔和内容空心问题 |

---

### 6. 解读 / 报告生成类（Pipeline / Generator）

这类 skill 的核心是：**把原始资料落到本地，再生成结构化文档交付**。

| Skill | 模式 | 适用场景 |
|---|---|---|
| [article-interpreter](skills/content/article-interpreter/SKILL.md) | Pipeline / Generator | 用户提供文章 URL、Markdown、PDF 或粘贴文本，希望生成包含总览、关键要点、个人启发、批判性思考和延伸思考的结构化解读报告 |
| [github-code-interpreter](skills/content/github-code-interpreter/SKILL.md) | Pipeline / Generator | 用户提供 GitHub 仓库链接，希望解读源码、分析架构、生成学习报告或快速上手文档 |
| [paper-interpreter](skills/content/paper-interpreter/SKILL.md) | Pipeline / Generator | 用户提供 arXiv 链接，希望下载论文、解读论文、生成读书笔记或详细报告 |
| [opendataloader-pdf](skills/media/opendataloader-pdf/SKILL.md) | Tool Wrapper / Pipeline | PDF 提取、PDF 转 Markdown/JSON/HTML、RAG 数据准备、批量 PDF 处理 |

**这类 skill 的共同特点：**
- 默认以本地文件为主交付
- 默认先交付初稿
- **不自动复查，是否复查需要用户明确同意**

---

### 7. 音频 / 转写工具类（Tool Wrapper / Pipeline）

这类 skill 适合把本地音频、录音或视频中的语音转成可继续处理的文本。

| Skill | 模式 | 适用场景 |
|---|---|---|
| [local-audio-transcriber](skills/media/local-audio-transcriber/SKILL.md) | Tool Wrapper / Pipeline | 用户发送已有录音、音频或视频文件，希望本地转写成 Markdown 文稿和 SRT 字幕 |

---

### 8. 图片 / 证件处理工具类（Tool Wrapper / Pipeline）

这类 skill 在本地处理含版权或个人信息的图片与 PDF，重点是保护原件、预览复核和隐私边界。

| Skill | 模式 | 适用场景 |
|---|---|---|
| [add-photo-certificate-watermarks](skills/media/add-photo-certificate-watermarks/SKILL.md) | Tool Wrapper / Pipeline | 给照片添加版权水印，或给身份证、护照、学历证书、资质文件和 PDF 添加限定用途水印 |

---

### 9. 下载 / 采集工具类（Tool Wrapper / Pipeline）

这类 skill 适合把特定网站的资源下载流程固化成可重复执行的脚本化工作流。

| Skill | 模式 | 适用场景 |
|---|---|---|
| [alltuu-downloader](skills/media/alltuu-downloader/SKILL.md) | Tool Wrapper / Pipeline | 用户提供 alltuu.com / m.alltuu.com 喔图云摄影相册链接，希望批量下载原图 |
| [photoplus-downloader](skills/media/photoplus-downloader/SKILL.md) | Tool Wrapper / Pipeline | 用户提供 photoplus.cn/live/ PhotoPlus 相册链接，希望批量下载原图 |

---

### 10. 微信工具类（Tool Wrapper / Generator）

这类 skill 适合把微信生态里的固定规则、入口和操作路径固化成可复用流程。

| Skill | 模式 | 适用场景 |
|---|---|---|
| [wechat-official-account-qr](skills/visual/wechat-official-account-qr/SKILL.md) | Tool Wrapper / Generator | 根据公众号 ID / `gh_...` 生成关注二维码，并提供微信内获取公众号 ID 的引导图 |

---

### 11. 运维 / 排障类（Runbook / Tool Wrapper）

这类 skill 适合处理“系统坏了、服务挂了、渠道断了、命令不会用”的场景。

| Skill | 模式 | 适用场景 |
|---|---|---|
| [openclaw-ops](skills/operations/openclaw-ops/SKILL.md) | Tool Wrapper / Runbook | OpenClaw 状态检查、日志排查、Gateway/渠道/Agent 故障处理 |
| [openclaw-session-cleaner](skills/operations/openclaw-session-cleaner/SKILL.md) | Tool Wrapper / Runbook | 清理 OpenClaw 膨胀的 session 文件、删除旧 cron session、重建 `sessions.json` 引用 |
| [will-codex-quota-reset](skills/operations/will-codex-quota-reset/SKILL.md) | Tool Wrapper | 查询 Codex 配额重置预测概率、最近重置时间和距上次重置时长 |
| [copaw-ops](skills/operations/copaw-ops/SKILL.md) | Tool Wrapper / Runbook | CoPaw 服务状态检查、配置排障、模型问题、cron 异常、渠道故障 |
| [hermes-ops](skills/operations/hermes-ops/SKILL.md) | Tool Wrapper / Runbook | Hermes Agent 运维、故障排查、gateway 异常、平台掉线、cron 不执行、profile 配置问题 |
| [hermes-qq](skills/operations/hermes-qq/SKILL.md) | Pipeline | 为 Hermes Agent 正式版 main 分支补充 QQ 平台支持、QQ Bot 接入、QQ 文件发送 |

**这类 skill 的共同原则：**
- 先做状态检查，再决定是否修复
- 高影响动作（重启、repair、更新、配置修改）应先说明再执行

---

### 12. 安装类（Pipeline）

这类 skill 偏工具链管理，负责把能力装上去。

| Skill | 模式 | 适用场景 |
|---|---|---|
| [claudian-installer](skills/distribution/claudian-installer/SKILL.md) | Pipeline | 安装 Claudian Obsidian 插件，把 Claude Code 接进 Obsidian |

---

## 使用建议

### 什么时候优先选哪类 skill？

- **问产品文档 / 官方资料** → 先看 wiki 类 skill
- **想优化 Prompt / 配置 / skill 本身** → 先看审查优化类 skill
- **想评估 P7/P8/P9 能力、晋升准备度或简历项目表达** → 用职业能力 / 成长评估类 skill
- **想把流程、结构、时序整理成图** → 用 `mermaid` skill
- **想让已有文章更自然、更像终稿** → 用 `remove-ai-flavor` skill
- **想把文章 / 论文 / 仓库整理成报告** → 用解读生成类 skill
- **想把录音、音频或视频转成文字** → 用 `local-audio-transcriber` skill
- **想给照片、身份证、学历证书或资质文件添加版权 / 限定用途水印** → 用 `add-photo-certificate-watermarks` skill
- **想批量下载摄影相册原图** → 用下载 / 采集工具类 skill
- **想根据公众号 ID 生成关注二维码** → 用 `wechat-official-account-qr` skill
- **服务出问题、命令不会用、要排障** → 用运维类 skill
- **要把能力装到工具里、同步到多个目录** → 用安装同步类 skill

---

## 仓库设计原则

这批公有 skill 默认遵循这些原则：

1. **description 是给模型看的触发规则，不只是简介**
2. **SKILL.md 负责调度，细节尽量拆到 references / scripts / assets**
3. **默认先交付初稿，不自动做超出用户预期的后续动作**
4. **需要高影响操作时，先说明再执行**
5. **能脚本化的重复动作，尽量不要只写成文字说明**
6. **持续沉淀 Gotchas，降低误触发和翻车概率**

### 新增 Skill

团队统一执行这条流水线：

1. 在 `config/skill-categories.json` 选择唯一分类，创建 `skills/<category>/<skill-name>/`，并同步注册 taxonomy、README 和 marketplace。
2. 使用 `skill-optimizer` 自动审查并修复新 Skill 的触发、流程、异常、安全和资源组织问题，然后运行 `python3 scripts/validate_skill.py <skill-name>` 直到通过。
3. 只提交新 Skill 及其索引变更，推送当前非主分支到远端。

不需要上传企业 Skills 市场，也不需要 optimizer attestation 或 `/publish-skill` 门禁。完整团队规范见 [`AGENTS.md`](AGENTS.md)。

---

## 安装

### Method 1: Claude Code plugin marketplace

在 Claude Code 中先添加这个仓库作为 plugin marketplace：

```bash
/plugin marketplace add chujianyun/skills
```

然后通过 `/plugin` 交互界面浏览并安装需要的 plugin，或直接安装某个 plugin：

```bash
/plugin install mermaid@wuming-skills
```

这里安装的是 Claude Code plugin。每个 plugin 会携带对应的 skill；Claude Code 目前按 plugin 逐个安装，不是通过自然语言“安装某个 skill”。

### Method 2: Ask a skill installer agent

如果你使用的 Agent 内置了 skill 安装器，可以直接发送类似指令：

- 安装全部：`安装 https://github.com/chujianyun/skills 所有 skills`
- 安装某个：`安装 https://github.com/chujianyun/skills 中的 mermaid skill`

### Method 3: Using [openskills](https://github.com/numman-ali/openskills)

```bash
openskills install chujianyun/skills --global
```

---

## Contact

![联系方式二维码](https://mingmingruyue-hz.oss-cn-hangzhou.aliyuncs.com/2025/codex-clipboard-cb9bcaae-e6b9-410f-b50c-088af145c41b.png)

---

## License

All Skill files in this project are licensed under [CC BY-NC-SA 4.0](LICENSE-CC-BY-NC-SA) (Attribution-NonCommercial-ShareAlike).

For commercial use, please contact the author for authorization.
