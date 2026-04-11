#!/usr/bin/env python3
from __future__ import annotations

import shutil
import sys
from pathlib import Path


def replace_once_or_skip(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f"patch anchor not found for {label}")
    return text.replace(old, new, 1)


def insert_after_once(text: str, anchor: str, block: str, label: str) -> str:
    if block in text:
        return text
    if anchor not in text:
        raise RuntimeError(f"insert anchor not found for {label}")
    return text.replace(anchor, anchor + block, 1)


def patch_config_py(path: Path) -> None:
    text = path.read_text(encoding="utf-8")

    text = replace_once_or_skip(
        text,
        '    DINGTALK = "dingtalk"\n    API_SERVER = "api_server"\n',
        '    DINGTALK = "dingtalk"\n    QQ = "qq"\n    API_SERVER = "api_server"\n',
        "config platform enum",
    )

    text = replace_once_or_skip(
        text,
        '            # WeCom uses extra dict for bot credentials\n'
        '            elif platform == Platform.WECOM and config.extra.get("bot_id"):\n'
        '                connected.append(platform)\n'
        '            # BlueBubbles uses extra dict for local server config\n',
        '            # WeCom uses extra dict for bot credentials\n'
        '            elif platform == Platform.WECOM and config.extra.get("bot_id"):\n'
        '                connected.append(platform)\n'
        '            # QQ bot uses app_id/app_secret, stored in token as "app_id:app_secret"\n'
        '            elif platform == Platform.QQ and config.token:\n'
        '                connected.append(platform)\n'
        '            # BlueBubbles uses extra dict for local server config\n',
        "config connected platforms",
    )

    text = replace_once_or_skip(
        text,
        '        Platform.SLACK: "SLACK_BOT_TOKEN",\n'
        '        Platform.MATTERMOST: "MATTERMOST_TOKEN",\n'
        '        Platform.MATRIX: "MATRIX_ACCESS_TOKEN",\n',
        '        Platform.SLACK: "SLACK_BOT_TOKEN",\n'
        '        Platform.MATTERMOST: "MATTERMOST_TOKEN",\n'
        '        Platform.MATRIX: "MATRIX_ACCESS_TOKEN",\n'
        '        Platform.QQ: "QQ_APP_ID",\n',
        "config token env map",
    )

    text = replace_once_or_skip(
        text,
        '    # BlueBubbles (iMessage)\n',
        '    # QQ Bot\n'
        '    qq_app_id = os.getenv("QQ_APP_ID")\n'
        '    qq_app_secret = os.getenv("QQ_APP_SECRET")\n'
        '    if qq_app_id and qq_app_secret:\n'
        '        if Platform.QQ not in config.platforms:\n'
        '            config.platforms[Platform.QQ] = PlatformConfig()\n'
        '        config.platforms[Platform.QQ].enabled = True\n'
        '        config.platforms[Platform.QQ].token = f"{qq_app_id}:{qq_app_secret}"\n'
        '\n'
        '        qq_extra = config.platforms[Platform.QQ].extra\n'
        '        qq_allowed_users = os.getenv("QQ_ALLOWED_USERS", "")\n'
        '        qq_allowed_groups = os.getenv("QQ_ALLOWED_GROUPS", "")\n'
        '        if qq_allowed_users:\n'
        '            qq_extra["allowed_users"] = qq_allowed_users\n'
        '        if qq_allowed_groups:\n'
        '            qq_extra["allowed_groups"] = qq_allowed_groups\n'
        '        if os.getenv("QQ_AT_REQUIRED"):\n'
        '            qq_extra["at_required"] = os.getenv("QQ_AT_REQUIRED", "true").lower() in ("true", "1", "yes")\n'
        '        if os.getenv("QQ_AUTO_QUOTE"):\n'
        '            qq_extra["auto_quote"] = os.getenv("QQ_AUTO_QUOTE", "false").lower() in ("true", "1", "yes")\n'
        '        if os.getenv("QQ_MARKDOWN_SUPPORT"):\n'
        '            qq_extra["markdown_support"] = os.getenv("QQ_MARKDOWN_SUPPORT", "false").lower() in ("true", "1", "yes")\n'
        '\n'
        '        qq_home = os.getenv("QQ_HOME_CHANNEL")\n'
        '        if qq_home:\n'
        '            config.platforms[Platform.QQ].home_channel = HomeChannel(\n'
        '                platform=Platform.QQ,\n'
        '                chat_id=qq_home,\n'
        '                name=os.getenv("QQ_HOME_CHANNEL_NAME", "Home"),\n'
        '            )\n'
        '\n'
        '    # BlueBubbles (iMessage)\n',
        "config qq env overrides",
    )

    path.write_text(text, encoding="utf-8")


def patch_base_py(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_once_or_skip(
        text,
        """            r'''[`"']?MEDIA:\\s*(?P<path>`[^`\\n]+`|"[^"\\n]+"|'[^'\\n]+'|(?:~/|/)\\S+(?:[^\\S\\n]+\\S+)*?\\.(?:png|jpe?g|gif|webp|mp4|mov|avi|mkv|webm|ogg|opus|mp3|wav|m4a)(?=[\\s`"',;:)\\]}]|$)|\\S+)[`"']?'''""",
        """            r'''[`"']?MEDIA:\\s*(?P<path>`[^`\\n]+`|"[^"\\n]+"|'[^'\\n]+'|(?:~/|/)\\S+(?:[^\\S\\n]+\\S+)*?\\.(?:png|jpe?g|gif|webp|mp4|mov|avi|mkv|webm|ogg|opus|mp3|wav|m4a|md|pdf|txt|docx?|xlsx?|pptx?|csv|json|zip)(?=[\\s`"',;:)\\]}]|$)|\\S+)[`"']?'''""",
        "base media regex",
    )
    text = replace_once_or_skip(
        text,
        "        _LOCAL_MEDIA_EXTS = (\n"
        "            '.png', '.jpg', '.jpeg', '.gif', '.webp',\n"
        "            '.mp4', '.mov', '.avi', '.mkv', '.webm',\n"
        "        )\n"
        "        ext_part = '|'.join(e.lstrip('.') for e in _LOCAL_MEDIA_EXTS)\n",
        "        _LOCAL_FILE_EXTS = (\n"
        "            '.png', '.jpg', '.jpeg', '.gif', '.webp',\n"
        "            '.mp4', '.mov', '.avi', '.mkv', '.webm',\n"
        "            '.md', '.pdf', '.txt', '.doc', '.docx', '.xlsx', '.pptx',\n"
        "            '.csv', '.json', '.zip',\n"
        "        )\n"
        "        ext_part = '|'.join(e.lstrip('.') for e in _LOCAL_FILE_EXTS)\n",
        "base local file extensions",
    )
    path.write_text(text, encoding="utf-8")


def patch_run_py(path: Path) -> None:
    text = path.read_text(encoding="utf-8")

    text = replace_once_or_skip(
        text,
        "        elif platform == Platform.API_SERVER:\n"
        "            from gateway.platforms.api_server import APIServerAdapter, check_api_server_requirements\n"
        "            if not check_api_server_requirements():\n"
        "                logger.warning(\"API Server: aiohttp not installed\")\n"
        "                return None\n"
        "            return APIServerAdapter(config)\n"
        "\n"
        "        elif platform == Platform.WEBHOOK:\n",
        "        elif platform == Platform.API_SERVER:\n"
        "            from gateway.platforms.api_server import APIServerAdapter, check_api_server_requirements\n"
        "            if not check_api_server_requirements():\n"
        "                logger.warning(\"API Server: aiohttp not installed\")\n"
        "                return None\n"
        "            return APIServerAdapter(config)\n"
        "\n"
        "        elif platform == Platform.QQ:\n"
        "            from gateway.platforms.qq import QQAdapter, check_qq_requirements\n"
        "            if not check_qq_requirements():\n"
        "                logger.warning(\"QQ: aiohttp not installed. Run: pip install aiohttp\")\n"
        "                return None\n"
        "            return QQAdapter(config)\n"
        "\n"
        "        elif platform == Platform.WEBHOOK:\n",
        "run create_adapter qq",
    )

    text = replace_once_or_skip(
        text,
        '            Platform.DINGTALK: "DINGTALK_ALLOWED_USERS",\n'
        '            Platform.FEISHU: "FEISHU_ALLOWED_USERS",\n'
        '            Platform.WECOM: "WECOM_ALLOWED_USERS",\n'
        '            Platform.BLUEBUBBLES: "BLUEBUBBLES_ALLOWED_USERS",\n',
        '            Platform.DINGTALK: "DINGTALK_ALLOWED_USERS",\n'
        '            Platform.FEISHU: "FEISHU_ALLOWED_USERS",\n'
        '            Platform.WECOM: "WECOM_ALLOWED_USERS",\n'
        '            Platform.QQ: "QQ_ALLOWED_USERS",\n'
        '            Platform.BLUEBUBBLES: "BLUEBUBBLES_ALLOWED_USERS",\n',
        "run allowlist map",
    )

    text = replace_once_or_skip(
        text,
        '            Platform.DINGTALK: "DINGTALK_ALLOW_ALL_USERS",\n'
        '            Platform.FEISHU: "FEISHU_ALLOW_ALL_USERS",\n'
        '            Platform.WECOM: "WECOM_ALLOW_ALL_USERS",\n'
        '            Platform.BLUEBUBBLES: "BLUEBUBBLES_ALLOW_ALL_USERS",\n',
        '            Platform.DINGTALK: "DINGTALK_ALLOW_ALL_USERS",\n'
        '            Platform.FEISHU: "FEISHU_ALLOW_ALL_USERS",\n'
        '            Platform.WECOM: "WECOM_ALLOW_ALL_USERS",\n'
        '            Platform.QQ: "QQ_ALLOW_ALL_USERS",\n'
        '            Platform.BLUEBUBBLES: "BLUEBUBBLES_ALLOW_ALL_USERS",\n',
        "run allow-all map",
    )

    old_deliver = """        from pathlib import Path\n\n        try:\n            media_files, _ = adapter.extract_media(response)\n            _, cleaned = adapter.extract_images(response)\n            local_files, _ = adapter.extract_local_files(cleaned)\n\n            _thread_meta = {\"thread_id\": event.source.thread_id} if event.source.thread_id else None\n\n            _AUDIO_EXTS = {'.ogg', '.opus', '.mp3', '.wav', '.m4a'}\n            _VIDEO_EXTS = {'.mp4', '.mov', '.avi', '.mkv', '.webm', '.3gp'}\n            _IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}\n\n            for media_path, is_voice in media_files:\n                try:\n                    ext = Path(media_path).suffix.lower()\n                    if ext in _AUDIO_EXTS:\n                        await adapter.send_voice(\n                            chat_id=event.source.chat_id,\n                            audio_path=media_path,\n                            metadata=_thread_meta,\n                        )\n                    elif ext in _VIDEO_EXTS:\n                        await adapter.send_video(\n                            chat_id=event.source.chat_id,\n                            video_path=media_path,\n                            metadata=_thread_meta,\n                        )\n                    elif ext in _IMAGE_EXTS:\n                        await adapter.send_image_file(\n                            chat_id=event.source.chat_id,\n                            image_path=media_path,\n                            metadata=_thread_meta,\n                        )\n                    else:\n                        await adapter.send_document(\n                            chat_id=event.source.chat_id,\n                            file_path=media_path,\n                            metadata=_thread_meta,\n                        )\n                except Exception as e:\n                    logger.warning(\"[%s] Post-stream media delivery failed: %s\", adapter.name, e)\n\n            for file_path in local_files:\n                try:\n                    ext = Path(file_path).suffix.lower()\n                    if ext in _IMAGE_EXTS:\n                        await adapter.send_image_file(\n                            chat_id=event.source.chat_id,\n                            image_path=file_path,\n                            metadata=_thread_meta,\n                        )\n                    else:\n                        await adapter.send_document(\n                            chat_id=event.source.chat_id,\n                            file_path=file_path,\n                            metadata=_thread_meta,\n                        )\n                except Exception as e:\n                    logger.warning(\"[%s] Post-stream file delivery failed: %s\", adapter.name, e)\n\n        except Exception as e:\n            logger.warning(\"Post-stream media extraction failed: %s\", e)\n"""

    new_deliver = """        from pathlib import Path\n\n        async def _send_and_check(send_coro, *, kind: str) -> None:\n            result = await send_coro\n            if isinstance(result, SendResult) and not result.success:\n                raise RuntimeError(result.error or f\"unknown {kind} delivery failure\")\n\n        try:\n            media_files, cleaned = adapter.extract_media(response)\n            local_files, _ = adapter.extract_local_files(cleaned)\n\n            _thread_meta = {\"thread_id\": event.source.thread_id} if event.source.thread_id else None\n\n            _AUDIO_EXTS = {'.ogg', '.opus', '.mp3', '.wav', '.m4a'}\n            _VIDEO_EXTS = {'.mp4', '.mov', '.avi', '.mkv', '.webm', '.3gp'}\n            _IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}\n\n            for media_path, _is_voice in media_files:\n                try:\n                    ext = Path(media_path).suffix.lower()\n                    if ext in _AUDIO_EXTS:\n                        await _send_and_check(\n                            adapter.send_voice(\n                                chat_id=event.source.chat_id,\n                                audio_path=media_path,\n                                metadata=_thread_meta,\n                            ),\n                            kind=\"media\",\n                        )\n                    elif ext in _VIDEO_EXTS:\n                        await _send_and_check(\n                            adapter.send_video(\n                                chat_id=event.source.chat_id,\n                                video_path=media_path,\n                                metadata=_thread_meta,\n                            ),\n                            kind=\"media\",\n                        )\n                    elif ext in _IMAGE_EXTS:\n                        await _send_and_check(\n                            adapter.send_image_file(\n                                chat_id=event.source.chat_id,\n                                image_path=media_path,\n                                metadata=_thread_meta,\n                            ),\n                            kind=\"media\",\n                        )\n                    else:\n                        await _send_and_check(\n                            adapter.send_document(\n                                chat_id=event.source.chat_id,\n                                file_path=media_path,\n                                metadata=_thread_meta,\n                            ),\n                            kind=\"media\",\n                        )\n                except Exception as e:\n                    logger.warning(\"[%s] Post-stream media delivery failed for %s: %s\", adapter.name, media_path, e)\n                    try:\n                        await adapter.send(\n                            chat_id=event.source.chat_id,\n                            content=f\"⚠️ 文件发送失败：{Path(media_path).name}\\n原因：{e}\",\n                            metadata=_thread_meta,\n                        )\n                    except Exception:\n                        logger.debug(\"[%s] Failed to send post-stream media failure notice\", adapter.name, exc_info=True)\n\n            for file_path in local_files:\n                try:\n                    ext = Path(file_path).suffix.lower()\n                    if ext in _IMAGE_EXTS:\n                        await _send_and_check(\n                            adapter.send_image_file(\n                                chat_id=event.source.chat_id,\n                                image_path=file_path,\n                                metadata=_thread_meta,\n                            ),\n                            kind=\"file\",\n                        )\n                    else:\n                        await _send_and_check(\n                            adapter.send_document(\n                                chat_id=event.source.chat_id,\n                                file_path=file_path,\n                                metadata=_thread_meta,\n                            ),\n                            kind=\"file\",\n                        )\n                except Exception as e:\n                    logger.warning(\"[%s] Post-stream file delivery failed for %s: %s\", adapter.name, file_path, e)\n                    try:\n                        await adapter.send(\n                            chat_id=event.source.chat_id,\n                            content=f\"⚠️ 文件发送失败：{Path(file_path).name}\\n原因：{e}\",\n                            metadata=_thread_meta,\n                        )\n                    except Exception:\n                        logger.debug(\"[%s] Failed to send post-stream file failure notice\", adapter.name, exc_info=True)\n\n        except Exception as e:\n            logger.warning(\"Post-stream media extraction failed: %s\", e)\n"""
    text = replace_once_or_skip(text, old_deliver, new_deliver, "run post-stream delivery")

    old_bg = """                # Send media files\n                for media_path in (media_files or []):\n                    try:\n                        await adapter.send_document(\n                            chat_id=source.chat_id,\n                            file_path=media_path,\n                        )\n                    except Exception:\n                        pass\n"""
    new_bg = """                # Send media files\n                for media_path in (media_files or []):\n                    try:\n                        result = await adapter.send_document(\n                            chat_id=source.chat_id,\n                            file_path=media_path,\n                        )\n                        if isinstance(result, SendResult) and not result.success:\n                            raise RuntimeError(result.error or \"unknown background media delivery failure\")\n                    except Exception as exc:\n                        logger.warning(\"[%s] Background media delivery failed for %s: %s\", adapter.name, media_path, exc)\n                        try:\n                            await adapter.send(\n                                chat_id=source.chat_id,\n                                content=f\"⚠️ 后台任务文件发送失败：{Path(media_path).name}\\n原因：{exc}\",\n                                metadata=_thread_metadata,\n                            )\n                        except Exception:\n                            logger.debug(\"[%s] Failed to send background media failure notice\", adapter.name, exc_info=True)\n"""
    text = replace_once_or_skip(text, old_bg, new_bg, "run background media delivery")

    path.write_text(text, encoding="utf-8")


def patch_tools_config_py(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_once_or_skip(
        text,
        '    "mattermost": {"label": "💬 Mattermost", "default_toolset": "hermes-mattermost"},\n'
        '    "webhook": {"label": "🔗 Webhook", "default_toolset": "hermes-webhook"},\n'
        '}\n',
        '    "mattermost": {"label": "💬 Mattermost", "default_toolset": "hermes-mattermost"},\n'
        '    "webhook": {"label": "🔗 Webhook", "default_toolset": "hermes-webhook"},\n'
        '    "qq":       {"label": "🐧 QQ",         "default_toolset": "hermes-qq"},\n'
        '}\n',
        "tools config qq platform",
    )
    path.write_text(text, encoding="utf-8")


def patch_toolsets_py(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_once_or_skip(
        text,
        '    "hermes-webhook": {\n'
        '        "description": "Webhook toolset - receive and process external webhook events",\n'
        '        "tools": _HERMES_CORE_TOOLS,\n'
        '        "includes": []\n'
        '    },\n'
        '\n'
        '    "hermes-gateway": {\n',
        '    "hermes-webhook": {\n'
        '        "description": "Webhook toolset - receive and process external webhook events",\n'
        '        "tools": _HERMES_CORE_TOOLS,\n'
        '        "includes": []\n'
        '    },\n'
        '\n'
        '    "hermes-qq": {\n'
        '        "description": "QQ bot toolset - Tencent QQ messaging platform (full access)",\n'
        '        "tools": _HERMES_CORE_TOOLS,\n'
        '        "includes": []\n'
        '    },\n'
        '\n'
        '    "hermes-gateway": {\n',
        "toolsets hermes-qq block",
    )
    text = replace_once_or_skip(
        text,
        '"includes": ["hermes-telegram", "hermes-discord", "hermes-whatsapp", "hermes-slack", "hermes-signal", "hermes-bluebubbles", "hermes-homeassistant", "hermes-email", "hermes-sms", "hermes-mattermost", "hermes-matrix", "hermes-dingtalk", "hermes-feishu", "hermes-wecom", "hermes-webhook"]',
        '"includes": ["hermes-telegram", "hermes-discord", "hermes-whatsapp", "hermes-slack", "hermes-signal", "hermes-bluebubbles", "hermes-homeassistant", "hermes-email", "hermes-sms", "hermes-mattermost", "hermes-matrix", "hermes-dingtalk", "hermes-feishu", "hermes-wecom", "hermes-webhook", "hermes-qq"]',
        "toolsets gateway includes",
    )
    path.write_text(text, encoding="utf-8")


def patch_tests(root: Path) -> None:
    extract_path = root / "tests/gateway/test_extract_local_files.py"
    if extract_path.exists():
        text = extract_path.read_text(encoding="utf-8")
        text = replace_once_or_skip(
            text,
            '    def test_no_media_extensions(self):\n'
            '        """Non-media extensions should not be matched."""\n'
            '        paths, _ = _extract("See /tmp/data.csv and /tmp/script.py and /tmp/notes.txt")\n'
            '        assert paths == []\n',
            '    def test_no_media_extensions(self):\n'
            '        """Unsupported extensions should not be matched, supported docs should."""\n'
            '        paths, _ = _extract("See /tmp/data.csv and /tmp/script.py and /tmp/notes.txt")\n'
            '        assert "/tmp/script.py" not in paths\n'
            '        assert "/tmp/data.csv" in paths\n'
            '        assert "/tmp/notes.txt" in paths\n',
            "test extract local files edge case",
        )
        extract_path.write_text(text, encoding="utf-8")

    platform_base_path = root / "tests/gateway/test_platform_base.py"
    if platform_base_path.exists():
        text = platform_base_path.read_text(encoding="utf-8")
        marker = (
            '    def test_media_tag_supports_quoted_paths_with_spaces(self):\n'
            '        content = "Here\\nMEDIA: \'/tmp/my image.png\'\\nAfter"\n'
            '        media, cleaned = BasePlatformAdapter.extract_media(content)\n'
            '        assert media == [("/tmp/my image.png", False)]\n'
            '        assert "Here" in cleaned\n'
            '        assert "After" in cleaned\n'
        )
        block = (
            '\n'
            '    def test_media_tag_extracts_document_paths(self):\n'
            '        content = "Report ready\\nMEDIA:\'/tmp/quarterly report.pdf\'"\n'
            '        media, cleaned = BasePlatformAdapter.extract_media(content)\n'
            '        assert media == [("/tmp/quarterly report.pdf", False)]\n'
            '        assert "Report ready" in cleaned\n'
            '        assert "MEDIA:" not in cleaned\n'
        )
        text = insert_after_once(text, marker, block, "test platform base document media")
        platform_base_path.write_text(text, encoding="utf-8")


def copy_asset(skill_dir: Path, repo_root: Path) -> None:
    src = skill_dir / "assets/qq.py"
    dst = repo_root / "gateway/platforms/qq.py"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def validate_repo(repo_root: Path) -> None:
    required = [
        repo_root / "gateway/config.py",
        repo_root / "gateway/platforms/base.py",
        repo_root / "gateway/run.py",
        repo_root / "hermes_cli/tools_config.py",
        repo_root / "toolsets.py",
    ]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise RuntimeError("not a hermes-agent repo or files missing: " + ", ".join(missing))


def main() -> int:
    skill_dir = Path(__file__).resolve().parents[1]
    repo_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    validate_repo(repo_root)

    copy_asset(skill_dir, repo_root)
    patch_config_py(repo_root / "gateway/config.py")
    patch_base_py(repo_root / "gateway/platforms/base.py")
    patch_run_py(repo_root / "gateway/run.py")
    patch_tools_config_py(repo_root / "hermes_cli/tools_config.py")
    patch_toolsets_py(repo_root / "toolsets.py")
    patch_tests(repo_root)

    print(f"hermes-qq installed into {repo_root}")
    print("Next steps:")
    print("1. source venv/bin/activate")
    print("2. python -m py_compile gateway/config.py gateway/platforms/base.py gateway/platforms/qq.py gateway/run.py hermes_cli/tools_config.py toolsets.py")
    print("3. python -m pytest tests/gateway/test_platform_base.py tests/gateway/test_extract_local_files.py tests/gateway/test_send_image_file.py tests/cron/test_scheduler.py tests/gateway/test_background_command.py tests/gateway/test_internal_event_bypass_pairing.py -q -n 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
