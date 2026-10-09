# 纯文本上传包

部分 Skill 上传器禁止二进制文件。白泽的本地图标是 PNG，Python 运行后也可能生成 `.pyc` 缓存，直接压缩已安装目录会把这些文件一并带入。

在仓库根目录运行：

```bash
python3 skills/baize/scripts/package_upload.py --output .skill-publish/baize-upload.zip
```

在其他目录运行时，将脚本路径替换为白泽实际安装路径，输出路径放在 Skill 目录之外。仅上传生成的 ZIP；打包不会上传到外部平台。

脚本保留 `baize/` 顶层目录及全部业务脚本、说明和参考文档，排除：

- 本地图标 `assets/icon.png`。
- 本地界面配置 `agents/openai.yaml`，避免图标路径悬空；上传版依然通过 `SKILL.md` 定义名称、描述与行为。
- `__pycache__`、`.pyc`、`.pyo`、`.DS_Store`、`__MACOSX`、`._*`、Git 元数据及回收目录。

其余文件必须能解码为 UTF-8 且没有二进制控制字符。发现其他二进制文件或软链接就停止，不静默丢弃业务材料。已有同名 ZIP 不会被覆盖；重新打包时使用新的输出文件名。

源目录与本地安装仍保留 PNG 和界面配置。该上传包不携带图标；如平台提供独立图标入口，可按平台要求单独设置。
