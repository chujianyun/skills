# 故障排查

## ModuleNotFoundError: No module named 'requests'

缺少 Python 依赖：

```bash
pip3 install --break-system-packages requests tqdm
```

## Command not found: python

系统使用 `python3` 命令，所有命令中用 `python3` 代替 `python`。

## 下载速度慢

- 脚本未内置代理支持，如需代理可手动设置环境变量 `HTTPS_PROXY`
- 等待下载完成，脚本会自动跳过已下载文件

## 部分照片下载失败

重新运行脚本即可，已下载的照片会自动跳过。

## API 签名失效

脚本中硬编码了 PhotoPlus API 签名盐值（`SALT`），如果 PhotoPlus 更改 API 签名机制，脚本会返回错误。需检查上游仓库是否有更新。
