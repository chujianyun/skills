---
name: local-audio-transcriber
description: 本地录音转文字工具。当用户发送已有录音、音频或视频文件，并希望把语音转成 Markdown 文稿和 SRT 字幕时使用。Apple Silicon 优先用 MLX/Apple GPU 和 whisper-large-v3-turbo-q4，本地转写，不生成 txt/json/vtt，不用于现场临时录音，也不默认调用云端语音识别服务。
---

# Local Audio Transcriber

把用户提供的本地录音、音频或视频文件转成文字。核心目标是：用户发来音频后，直接返回转写文本；同时在本地保存 Markdown 文稿和 SRT 字幕。

## 适用边界

- 适用：`.m4a`、`.mp3`、`.wav`、`.aac`、`.flac`、`.ogg`、`.opus`、`.mp4`、`.mov`、`.mkv` 等已有文件
- 适用：会议录音、访谈录音、课程音频、播客片段、视频提取文字、字幕生成
- 不适用：现场临时录音、麦克风采集、实时听写，除非用户另行明确要求
- 默认本地处理，不上传音频到云端

## 工作流程

1. 确认用户提供的是可访问的本地音频/视频文件路径或附件。
2. 先判断机器类型和可用引擎：

```bash
python3 - <<'PY'
import platform, sys
print(sys.platform, platform.machine())
try:
    import mlx.core as mx
    print("mlx", mx.default_device())
except Exception as e:
    print(type(e).__name__ + ": " + str(e))
PY
```

3. Apple Silicon（M1/M2/M3/M4）优先安装并使用 MLX，本地调用 Apple GPU/统一内存：

```bash
python3.13 -m venv /tmp/local-audio-transcriber-mlx
/tmp/local-audio-transcriber-mlx/bin/python -m pip install -U pip mlx-whisper
```

4. 非 Apple Silicon、CUDA 机器或 MLX 不可用时，再使用 faster-whisper：

```bash
python3 -m pip install -U faster-whisper
```

5. 运行转写脚本，中文录音优先指定 `--language zh`；不确定语言时省略语言参数：

```bash
/tmp/local-audio-transcriber-mlx/bin/python {skill_dir}/scripts/transcribe.py "input.m4a" --language zh --print-text
```

6. 向用户直接发送转写文本。文本很长时，优先交付本地文件路径，并贴出开头和关键说明。
7. 默认只保存 `.md` 和 `.srt` 文件；不要生成 `txt`、`json` 或 `vtt`。

## 常用命令

```bash
# Apple Silicon 中文长录音：优先使用 MLX + Apple GPU + turbo-q4
/tmp/local-audio-transcriber-mlx/bin/python {skill_dir}/scripts/transcribe.py "recording.m4a" --language zh --print-text

# 明确指定 MLX 和模型
/tmp/local-audio-transcriber-mlx/bin/python {skill_dir}/scripts/transcribe.py "recording.m4a" --engine mlx --model mlx-community/whisper-large-v3-turbo-q4 --language zh --print-text

# 非 Apple Silicon / CUDA / CPU：使用 faster-whisper
python3 {skill_dir}/scripts/transcribe.py "recording.m4a" --engine faster-whisper --model small --language zh --print-text

# 自动识别语言，生成 Markdown 和 SRT
python3 {skill_dir}/scripts/transcribe.py "video.mp4" --print-text

# 多个文件批量转写到指定目录
python3 {skill_dir}/scripts/transcribe.py *.m4a --language zh --output-dir ./transcripts

# faster-whisper 质量更高但更慢
python3 {skill_dir}/scripts/transcribe.py "meeting.m4a" --engine faster-whisper --model medium --language zh --print-text
```

## 参数取舍

- Apple Silicon 默认引擎：`mlx`，默认模型：`mlx-community/whisper-large-v3-turbo-q4`
- 非 Apple Silicon 默认引擎：`faster-whisper`，默认模型：`small`
- 中文长录音、多人直播、专有名词较多：优先 `whisper-large-v3-turbo-q4`
- `whisper-large-v3-turbo-q4` 是量化模型，适合 M1 16GB 这类统一内存机器；首次运行会下载模型，之后走本地缓存
- OpenAI Whisper 的 `--device mps` 在 M1 上可能极慢；本地 Apple GPU 路线优先用 MLX，不优先用 PyTorch MPS
- 长录音默认关闭 `condition_on_previous_text`，避免 Whisper 在中文口语录音里进入重复幻觉循环
- 只有明确需要跨段一致性且没有重复风险时，才加 `--condition-on-previous-text`
- faster-whisper 长会议、嘈杂环境或多人访谈：可用 `--model medium`
- CPU 环境：默认 `int8`，更省内存
- CUDA 环境：脚本会尽量自动使用 `float16`
- 口语录音：默认开启 VAD 静音过滤；如切分异常，使用 `--no-vad-filter`
- 如果 MLX `small` 出现明显错词，优先升级到 `whisper-large-v3-turbo-q4`，不要只靠后处理硬校对
- 初始提示词可以帮助专有名词，但如果配合上下文续写出现重复，立即关闭 `--condition-on-previous-text`

## 输出要求

- 用户明确要“转文字”时，最终回复应包含转写正文，不要只给文件路径。
- 用户要“整理成会议纪要/文章/字幕”时，先完成转写，再按用户目标继续加工。
- 转写文件只保留 Markdown 和 SRT 两种格式，不生成 txt/json/vtt。
- 对隐私敏感录音，只说明本地处理和输出位置，不复述无关敏感信息。

## 故障处理

- `ModuleNotFoundError: faster_whisper`：运行 `python3 -m pip install -U faster-whisper`
- `ModuleNotFoundError: mlx_whisper`：在虚拟环境中运行 `/tmp/local-audio-transcriber-mlx/bin/python -m pip install -U mlx-whisper`
- macOS 系统 Python 提示 `externally-managed-environment`：不要加 `--break-system-packages`，改用 `python3.13 -m venv /tmp/local-audio-transcriber-mlx`
- `mlx` 默认设备不是 `Device(gpu, 0)`：说明 MLX/Metal 没走通，降级到 faster-whisper 或检查系统环境
- 音频无法解码：建议安装或更新 `ffmpeg`，或让用户换成 `.m4a/.mp3/.wav`
- 转写很慢：改用 `--model small` 或 `--model base`
- Apple Silicon 转写很慢：确认不是 OpenAI Whisper `--device mps`，优先使用本脚本 `--engine mlx`
- 中文被识别成其他语言：加 `--language zh`
- 字幕时间轴不准：尝试 `--model medium`，或关闭 VAD：`--no-vad-filter`
- 出现“同一句话无限重复”：重跑并确保没有开启 `--condition-on-previous-text`，必要时换 `whisper-large-v3-turbo-q4`
