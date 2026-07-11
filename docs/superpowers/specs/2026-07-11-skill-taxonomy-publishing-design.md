# Skill 分类与发布流水线设计

## 目标

把当前平铺的 Skill 仓库改造成按领域分类、可自动检查、可接入企业内部市场、并在发布成功后推送 Git 远端的团队仓库。

本次改造必须满足：

1. 新 Skill 创建前先匹配分类，并放入对应分类目录。
2. 新 Skill 发布前必须经过 `skill-optimizer` 语义审查和确定性质量检查。
3. 质量门禁通过后，通过统一指令上传企业内部 Skills 市场。
4. 市场上传成功后，才允许提交并推送 Git 远端。

## 目录模型

Skill 统一放在 `skills/<category>/<skill-name>/`，一级分类固定为：

- `knowledge`：产品文档、知识库、领域资料封装。
- `review`：Prompt、Agent、配置和 Skill 的审查与优化。
- `career`：职级能力评估、晋升和职业建议。
- `content`：文章、论文、源码解读和文本加工。
- `visual`：图示、可视化和二维码等视觉输出。
- `media`：音频、PDF、图片下载与媒体处理。
- `operations`：服务运维、故障排查、会话清理和平台接入。
- `distribution`：安装、同步、分发和技能市场相关能力。

分类定义保存为机器可读清单，供创建、校验和发布脚本共同使用。分类名必须来自清单，禁止临时创建近义目录。

## 迁移原则

- 完整移动每个 Skill 文件夹，不拆散其中的 `SKILL.md`、`references/`、`scripts/`、`assets/` 和 `agents/`。
- 同步更新 `README.md` 和 `.claude-plugin/marketplace.json` 中的路径。
- 校验命令从固定两层目录改为递归发现。
- 不修改与分类迁移无关的 Skill 内容。
- 保留用户现有未跟踪文件，不把它意外加入设计提交。

## 团队规范

根 `AGENTS.md` 作为仓库级执行规范，保持简短并明确以下门禁：

1. **Classify**：先从分类清单中选择唯一分类。
2. **Create**：创建 `skills/<category>/<skill-name>/`，frontmatter 只允许 `name` 和 `description`。
3. **Optimize**：使用 `skill-optimizer` 审查触发语义、工作流、确认门槛、异常处理、安全边界和资源拆分；新 Skill 的创建任务视为已授权实施安全、范围内的优化。
4. **Validate**：运行结构、路径、引用、敏感信息和 marketplace 一致性检查。
5. **Publish**：调用企业内部市场适配器，失败时立即停止。
6. **Push**：仅在市场明确返回成功后提交并推送当前分支。

更新现有 Skill 时仍遵循范围控制；发布命令不得借机重写无关 Skill。

## 发布入口

团队统一使用：

```text
/publish-skill <skill-name>
```

其底层入口为：

```bash
python3 scripts/publish_skill.py <skill-name>
```

发布脚本负责可确定执行的步骤；Agent 命令负责调用 `skill-optimizer` 完成语义判断。脚本不能伪造 LLM 审查结果。

## 内部市场适配器

企业市场尚无固定 CLI 或 API，因此本仓库只定义稳定协议，不写死内部地址与凭据。

环境变量 `SKILLS_MARKET_PUBLISHER` 指向一个可执行程序。发布器接收：

```text
<publisher> --skill-dir <absolute-path> --name <skill-name> --category <category>
```

约定：

- 退出码 `0` 表示市场已确认上传成功。
- 非零退出码、程序缺失、变量未配置或超时均视为失败。
- 凭据由发布器自身或环境管理，不写入仓库，也不打印敏感值。
- 失败后不得执行 Git commit 或 push。

## 质量门禁

确定性检查至少覆盖：

- Skill 位于合法分类目录，目录名与 frontmatter `name` 一致。
- frontmatter 只包含 `name` 和 `description`。
- `description` 非空，并同时表达能力和触发场景。
- `SKILL.md` 引用的本地文件存在。
- 不包含常见密钥、Token、私钥和明文凭据模式。
- marketplace 中存在唯一条目，路径指向当前 Skill。
- marketplace JSON 可解析，README 链接不存在旧路径。
- 官方 `quick_validate.py` 校验通过。

语义审查至少覆盖：触发边界、工作流顺序、失败策略、确认门槛、输出契约、渐进式披露、外部依赖和高副作用操作。

## Git 行为

- 发布脚本只处理目标 Skill，以及为该 Skill 必须更新的分类清单、README 和 marketplace 条目。
- 工作区存在无关改动时停止，避免混入提交。
- 市场上传成功后生成明确提交信息，再推送当前非 `main` 分支。
- 禁止从 `main`、detached HEAD 或无上游安全条件下自动发布。
- 本次实现只创建功能分支和本地提交，不自动推送功能分支；自动推送能力由发布流水线提供。

## 失败处理

- 分类不唯一或找不到 Skill：停止并给出候选路径。
- 优化未通过：停止，输出问题，不上传。
- 确定性校验失败：停止并列出失败项。
- 市场适配器未配置：停止并输出配置方式。
- 市场上传失败：保留本地修改，不提交、不推送。
- Git 提交或推送失败：报告失败并保留可恢复状态，不回滚用户文件。

## 验证标准

- 所有现有 Skill 均位于合法分类目录。
- README 和 marketplace 不再引用旧的平铺路径。
- 每个 Skill 通过官方快速校验。
- marketplace JSON 通过解析校验。
- 发布脚本的成功路径和主要失败路径有自动化测试。
- 未配置市场发布器时，发布命令可预测地停止，且 Git 历史不变化。
- 模拟市场成功时，流水线按顺序执行，且只有成功后进入 Git 阶段。

## 非目标

- 本次不建设企业 Skills 市场服务端。
- 不定义企业鉴权体系或保存企业凭据。
- 不批量改写现有 Skill 的业务内容。
- 不拆分多个仓库，也不为每个分类创建独立 marketplace。
