#!/usr/bin/env python3
"""Atomically build an indexed Wiki Skill from a validated staging directory."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

from sync_wiki_docs import SyncError, load_staged_corpus, print_summary, sync_skill, utc_now


def normalized_name(raw: str) -> str:
    value = raw.strip().casefold().replace("_", "-").replace(" ", "-")
    value = re.sub(r"-+", "-", value).strip("-")
    if not value.endswith("-wiki"):
        value += "-wiki"
    if not re.fullmatch(r"[a-z0-9-]+", value):
        raise SyncError(
            "Skill name must use lowercase ASCII letters, digits, and hyphens"
        )
    if len(value) > 63:
        raise SyncError("Skill name must be 63 characters or fewer")
    return value


def quoted(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def triggering_description(raw: str, title: str) -> str:
    value = " ".join(raw.strip().split())
    if not value:
        raise SyncError("--description must not be empty")
    if not re.search(r"(?i)\buse when\b|用于|适用|当用户|触发", value):
        value += f" 当用户询问 {title} 的使用、配置、API 或故障排查问题时使用。"
    return value


def short_description(title: str) -> str:
    suffix = "离线 Wiki 检索与有依据问答"
    maximum_title_length = max(1, 64 - len(suffix) - 1)
    compact_title = title if len(title) <= maximum_title_length else title[: maximum_title_length - 1] + "…"
    value = f"{compact_title} {suffix}"
    if len(value) < 25:
        value += "，支持本地文档索引"
    return value[:64]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def generated_skill_md(name: str, title: str, description: str) -> str:
    return f"""---
name: {name}
description: {quoted(description)}
---

# {title} Wiki

使用随 Skill 打包的 Wiki 文档回答问题。离线文档是第一依据；只有本地材料不足、用户要求核对最新版或问题超出快照范围时，才补查规范来源。

## 资源

- [文档索引](references/INDEX.md)：浏览完整主题结构或搜索词不确定时读取。
- [来源与范围](references/SOURCE.md)：回答版本、许可证、完整性或时效性问题时读取。
- [更新协议](references/UPDATE.md)：用户要求刷新、同步或自动更新本 Wiki Skill 时读取。
- `references/docs/`：保持 Wiki 导航层级的 Markdown 正文；只读取与问题直接相关的文件。
- `references/wiki-manifest.json`：页面来源、路径和逐文档 SHA-256 清单。
- `scripts/search_docs.py`：零第三方依赖的本地全文检索。

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
"""


def generated_readme(name: str, title: str, source_url: str) -> str:
    return f"""# {name}

面向 Agent 的 {title} 离线 Wiki Skill，来源为 <{source_url}>。

文档按原 Wiki 导航层级保存为 Markdown，并配有完整索引、本地全文检索和逐文档 SHA-256 清单。手动或自动同步会先比较内容哈希；没有变化时不会重写正文、索引或清单。

## 使用

调用 `${name}` 后直接询问 {title} 的概念、使用、配置或排障问题。Agent 会先检索少量相关文档，再给出带本地文档路径的回答。

## 更新与边界

- 更新规则见 `references/UPDATE.md`，来源和许可边界见 `references/SOURCE.md`。
- 这是离线快照；版本敏感问题需要核对规范来源。
- 不包含真实凭据，不绕过登录、付费墙或访问控制。
"""


def generated_source_md(
    title: str,
    source_url: str,
    language: str,
    scope: str,
    license_text: str,
    complete: bool,
) -> str:
    status = "完整" if complete else "部分（用户已明确接受）"
    return f"""# 来源与范围

- Wiki：{title}
- 规范来源：<{source_url}>
- 语言 / 版本：{language}
- 抓取范围：{scope}
- 当前快照：{status}；精确覆盖数与最近一次有变化的同步时间见 `wiki-manifest.json`
- 上游许可：{license_text}

离线快照可能落后于上游。许可证不明或不允许再分发时，本 Skill 仅限用户授权的本地使用，不应提交到公开仓库或发布到市场。
"""


def generated_update_md(source_url: str) -> str:
    return f"""# 更新协议

规范来源：<{source_url}>

1. 重新盘点来源范围内的完整导航，不沿用旧页面数量猜测新范围。
2. 使用 `mktemp -d` 创建 staging，写入 `docs/`、可选 `assets/` 和 `inventory.json`。
3. `inventory.json` 使用 `schema_version: 1`，包含 `source_root`、`coverage`、`pages` 和可选 `assets`。每个 page 记录 `title`、`source_url`、`source_path`、`local_path`，可选 `summary` 与 `keywords`。
4. `coverage.discovered` 必须等于成功页数加失败页数，`coverage.captured` 必须等于 pages 数量。失败列表非空时默认停止。
5. 先预演：

   ```bash
   python3 <skill-root>/scripts/sync_wiki_docs.py \\
     --skill-root <skill-root> \\
     --staging-dir <staging> \\
     --dry-run
   ```

6. 预演完整且没有未授权删页后去掉 `--dry-run`。上游删页或改路径时，只有获得授权才加 `--prune`；旧文件会移到 `references/.baize-trash/`。
7. `UNCHANGED` 表示成功且零文件写入。`CHANGED` 后重新验证本地搜索和安装副本。

若当前 Agent 安装了 `$baize`，优先用它完成抓取、覆盖率核对、位置判断和自动化配置。没有可用调度器时不要私自修改系统 cron。
"""


def scaffold(
    root: Path,
    *,
    name: str,
    title: str,
    description: str,
    source_url: str,
    language: str,
    scope: str,
    license_text: str,
    complete: bool,
) -> None:
    for relative in ("agents", "references/docs", "references/assets", "scripts"):
        (root / relative).mkdir(parents=True, exist_ok=True)

    write_text(root / "SKILL.md", generated_skill_md(name, title, description))
    write_text(root / "README.md", generated_readme(name, title, source_url))
    write_text(
        root / "agents" / "openai.yaml",
        "\n".join(
            [
                "interface:",
                f"  display_name: {quoted(title + ' Wiki')}",
                f"  short_description: {quoted(short_description(title))}",
                f"  default_prompt: {quoted(f'Use ${name} to answer my question with documentation-backed guidance.')}",
                "",
            ]
        ),
    )
    write_text(
        root / "references" / "SOURCE.md",
        generated_source_md(
            title, source_url, language, scope, license_text, complete
        ),
    )
    write_text(root / "references" / "UPDATE.md", generated_update_md(source_url))
    write_text(root / "references" / "INDEX.md", "# 文档索引\n")
    manifest = {
        "schema_version": 1,
        "wiki": {
            "skill_name": name,
            "title": title,
            "source_root": source_url,
            "language": language,
            "scope": scope,
            "license": license_text,
        },
        "coverage": {
            "discovered": 0,
            "captured": 0,
            "failed": [],
            "excluded": [],
            "complete": False,
        },
        "documents": {},
        "assets": {},
        "created_at": utc_now(),
    }
    write_text(
        root / "references" / "wiki-manifest.json",
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )

    source_scripts = Path(__file__).resolve().parent
    for filename in ("search_docs.py", "sync_wiki_docs.py"):
        destination = root / "scripts" / filename
        shutil.copy2(source_scripts / filename, destination)
        destination.chmod(destination.stat().st_mode | 0o111)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--staging-dir", required=True, type=Path)
    parser.add_argument("--target-parent", required=True, type=Path)
    parser.add_argument("--name", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--language", default="与来源链接一致")
    parser.add_argument("--scope", default="inventory.json 中盘点的 Wiki 导航范围")
    parser.add_argument(
        "--license",
        default="未确认；仅限本地使用，公开分发前必须核对",
    )
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="Build an explicitly accepted incomplete snapshot",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        name = normalized_name(args.name)
        title = args.title.strip()
        if not title:
            raise SyncError("--title must not be empty")
        description = triggering_description(args.description, title)
        corpus = load_staged_corpus(
            args.staging_dir, allow_partial=args.allow_partial
        )
        source_url = args.source_url.strip().rstrip("/")
        if corpus.source_root.rstrip("/") != source_url:
            raise SyncError("--source-url must match inventory.source_root")

        target_parent = args.target_parent.expanduser().resolve()
        target_parent.mkdir(parents=True, exist_ok=True)
        target = target_parent / name
        if target.exists() or target.is_symlink():
            raise SyncError(f"target already exists: {target}")

        temporary = Path(
            tempfile.mkdtemp(prefix=f".baize-{name}-", dir=target_parent)
        )
        try:
            scaffold(
                temporary,
                name=name,
                title=title,
                description=description,
                source_url=source_url,
                language=args.language.strip(),
                scope=args.scope.strip(),
                license_text=args.license.strip(),
                complete=bool(corpus.coverage["complete"]),
            )
            summary = sync_skill(
                temporary,
                args.staging_dir,
                allow_partial=args.allow_partial,
            )
            os.replace(temporary, target)
        except Exception:
            if temporary.exists():
                shutil.rmtree(temporary)
            raise
    except SyncError as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 2

    print(f"CREATED: {target}")
    print_summary(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
