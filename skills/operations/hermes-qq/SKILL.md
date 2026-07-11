---
name: hermes-qq
description: 当用户想在 Hermes Agent 正式版 main 分支上补充 QQ platform 支持，或明确提到“给 hermes main 增加 QQ 渠道”“把 QQ support 作为 skill 安装到 Hermes”“让正式版 Hermes 支持 QQ 和文件发送”时使用。这个技能会把当前仓库补成支持 QQ Bot、QQ 文件发送、QQ 平台配置和工具集接线的版本。
author: 悟鸣
updated_at: 2026-04-10
source: public
visibility: public
---

# Hermes QQ Installer

这个技能用于把 **Hermes Agent 的 `main` 正式代码** 补成支持 QQ platform 的版本。

适用场景：

- 当前仓库是 `hermes-agent`
- 用户希望在正式 `main` 代码上增加 QQ 渠道
- 需要同时支持 QQ 文本、图片、音频、视频、普通文件发送

不适用场景：

- 当前仓库不是 `hermes-agent`
- 用户只是想分析 QQ adapter 原理，不想改代码
- 仓库已经是自带 QQ 支持的分支，且不需要再次打补丁

## 工作流程

1. 先确认目标仓库是 `hermes-agent`，并且工作树里没有会冲突的本地改动。
2. 运行 `scripts/install_hermes_qq.py`，默认对当前工作目录打补丁。
3. 如仓库有 `venv`，优先执行：
   `source venv/bin/activate && python -m pytest tests/gateway/test_platform_base.py tests/gateway/test_extract_local_files.py tests/gateway/test_send_image_file.py tests/cron/test_scheduler.py tests/gateway/test_background_command.py tests/gateway/test_internal_event_bypass_pairing.py -q -n 0`
4. 如果没有现成环境，再按仓库约定补测试环境后执行同一组定向测试。

## 运行方式

当前目录就是目标 `hermes-agent` 仓库时：

```bash
python /Users/liuwangyang/Documents/coding/our/skills-wuming/skills/hermes-qq/scripts/install_hermes_qq.py
```

指定目标仓库时：

```bash
python /Users/liuwangyang/Documents/coding/our/skills-wuming/skills/hermes-qq/scripts/install_hermes_qq.py /path/to/hermes-agent
```

## 资源

- `assets/qq.py`
  QQ adapter 完整实现，会被复制到 `gateway/platforms/qq.py`
- `references/verification.md`
  安装后建议执行的验证命令

如果脚本提示某个补丁锚点不存在，说明目标仓库已经偏离官方 `main` 太多。这种情况下不要盲写，先读 [references/verification.md](references/verification.md)，再手动审查差异后补丁。
