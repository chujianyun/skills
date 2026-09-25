---
name: photoplus-downloader
description: PhotoPlus相册批量下载原图工具。当用户需要从 photoplus.cn/live/ 相册批量下载原图时使用此技能。适用于 photoplus.cn 相册链接，支持多线程并发、自动跳过已下载文件。
---

# PhotoPlus 相册下载器

从 PhotoPlus 相册（photoplus.cn）批量下载原图。

## 触发条件

用户提供包含 photoplus.cn 的相册链接，例如：
- `https://live.photoplus.cn/live/67458816?accessFrom=live`
- `https://live.photoplus.cn/live/67458816`

## Gotchas

- 不要从 GitHub 克隆脚本，本地 `scripts/download_photos.py` 已可直接使用
- 下载前必须先确认相册信息，不要拿到链接就直接下载
- 依赖 `requests` 和 `tqdm`，首次运行前需安装
- 需要 Python 3

## 工作流程

### 1. 提取相册 ID

从 URL 路径中提取 `/live/` 后面的数字。

示例：`https://live.photoplus.cn/live/67458816?accessFrom=live` → ID 为 `67458816`

### 2. 确认相册信息

运行脚本获取相册信息，确认后再下载：

```bash
cd {skill_dir}/scripts
python3 download_photos.py --id [相册ID] --count 1
```

向用户展示总照片数量，确认是否继续下载。

### 3. 安装依赖（如需）

```bash
pip3 install --break-system-packages requests tqdm
```

### 4. 执行下载

用户确认后，下载全部照片：

```bash
cd {skill_dir}/scripts
python3 download_photos.py --id [相册ID] --count 9999
```

参数：
- `--id`：相册 ID（必需）
- `--count`：下载数量（默认 9999 即全部）

### 5. 验证结果

```bash
ls {skill_dir}/scripts/dist/[相册ID]/ | wc -l
```

向用户报告下载数量和保存路径。默认保存在 `scripts/dist/[相册ID]/`。

### 6. 移动照片（可选）

如用户需要移动到指定目录：

```bash
mv {skill_dir}/scripts/dist/[相册ID]/* ~/Downloads/[目标目录]/
```

## 故障排查

详见 [references/troubleshooting.md](references/troubleshooting.md)
