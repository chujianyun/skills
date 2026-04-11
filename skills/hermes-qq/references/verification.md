安装 `hermes-qq` 后，优先做这几步验证：

1. 语法检查

```bash
python -m py_compile gateway/config.py gateway/platforms/base.py gateway/platforms/qq.py gateway/run.py hermes_cli/tools_config.py toolsets.py
```

2. 定向测试

```bash
source venv/bin/activate
python -m pytest tests/gateway/test_platform_base.py tests/gateway/test_extract_local_files.py tests/gateway/test_send_image_file.py tests/cron/test_scheduler.py tests/gateway/test_background_command.py tests/gateway/test_internal_event_bypass_pairing.py -q -n 0
```

3. QQ smoke test

```bash
source venv/bin/activate
python - <<'PY'
from gateway.platforms.qq import QQAdapter, check_qq_requirements
from gateway.config import Platform, PlatformConfig

print(check_qq_requirements())
print(Platform.QQ.value)
adapter = QQAdapter(PlatformConfig(enabled=True, token="app:secret"))
print(adapter.platform.value, type(adapter).__name__)
PY
```
