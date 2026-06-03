#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import platform
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Literal


AUDIO_EXTENSIONS = {
    ".aac",
    ".aiff",
    ".flac",
    ".m4a",
    ".mkv",
    ".mov",
    ".mp3",
    ".mp4",
    ".ogg",
    ".opus",
    ".wav",
    ".webm",
    ".wma",
}


@dataclass
class TranscriptSegment:
    start: float
    end: float
    text: str


@dataclass
class TranscriptInfo:
    language: str | None = None
    language_probability: float | None = None
    duration: float | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transcribe existing local audio/video files locally."
    )
    parser.add_argument("inputs", nargs="+", help="Audio/video files to transcribe.")
    parser.add_argument(
        "--engine",
        choices=["auto", "mlx", "faster-whisper"],
        default="auto",
        help=(
            "Inference engine. auto uses MLX on Apple Silicon when available, "
            "otherwise faster-whisper. Default: auto."
        ),
    )
    parser.add_argument(
        "--model",
        default=None,
        help=(
            "Whisper model size, local model path, or Hugging Face repo. "
            "Default: MLX uses mlx-community/whisper-large-v3-turbo-q4; "
            "faster-whisper uses small."
        ),
    )
    parser.add_argument(
        "--language",
        default=None,
        help="Source language code, e.g. zh, en, ja. Omit for auto detection.",
    )
    parser.add_argument(
        "--task",
        choices=["transcribe", "translate"],
        default="transcribe",
        help="Use translate to translate speech into English.",
    )
    parser.add_argument(
        "--formats",
        default="txt,md",
        help="Comma-separated output formats: txt, md, srt, vtt, json. Default: txt,md.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory for transcript files. Default: next to each input file.",
    )
    parser.add_argument(
        "--device",
        default="auto",
        choices=["auto", "cpu", "cuda"],
        help="Inference device. Default: auto.",
    )
    parser.add_argument(
        "--compute-type",
        default="auto",
        help="CTranslate2 compute type. Default: auto.",
    )
    parser.add_argument("--beam-size", type=int, default=5, help="Beam size.")
    parser.add_argument(
        "--initial-prompt",
        default=None,
        help="Optional prompt with names, jargon, or domain terms.",
    )
    parser.add_argument(
        "--condition-on-previous-text",
        dest="condition_on_previous_text",
        action="store_true",
        default=False,
        help=(
            "Prompt each window with previous text. Disabled by default because "
            "long Chinese recordings can fall into repetition loops."
        ),
    )
    parser.add_argument(
        "--vad-filter",
        dest="vad_filter",
        action="store_true",
        default=True,
        help="Enable VAD silence filtering. Enabled by default.",
    )
    parser.add_argument(
        "--no-vad-filter",
        dest="vad_filter",
        action="store_false",
        help="Disable VAD silence filtering.",
    )
    parser.add_argument(
        "--print-text",
        action="store_true",
        help="Print the full transcript text to stdout.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing transcript files.",
    )
    return parser.parse_args()


def is_apple_silicon() -> bool:
    return sys.platform == "darwin" and platform.machine() == "arm64"


def import_mlx_whisper():
    try:
        import mlx_whisper
    except ModuleNotFoundError:
        print(
            "Missing dependency: mlx-whisper\n"
            "Install it in a virtual environment with:\n"
            "  python3.13 -m venv /tmp/local-audio-transcriber-mlx\n"
            "  /tmp/local-audio-transcriber-mlx/bin/python -m pip install -U mlx-whisper",
            file=sys.stderr,
        )
        raise SystemExit(2)
    return mlx_whisper


def import_faster_whisper():
    try:
        from faster_whisper import WhisperModel
    except ModuleNotFoundError:
        print(
            "Missing dependency: faster-whisper\n"
            "Install it with:\n"
            "  python3 -m pip install -U faster-whisper",
            file=sys.stderr,
        )
        raise SystemExit(2)
    return WhisperModel


def choose_engine(engine: str) -> Literal["mlx", "faster-whisper"]:
    if engine == "mlx":
        return "mlx"
    if engine == "faster-whisper":
        return "faster-whisper"

    if is_apple_silicon():
        try:
            import mlx.core as mx
            import mlx_whisper  # noqa: F401

            if str(mx.default_device()).startswith("Device(gpu"):
                return "mlx"
        except Exception:
            pass

    return "faster-whisper"


def choose_model(engine: str, model: str | None) -> str:
    if model:
        return model
    if engine == "mlx":
        return "mlx-community/whisper-large-v3-turbo-q4"
    return "small"


def choose_device_and_compute_type(device: str, compute_type: str) -> tuple[str, str]:
    if device == "auto":
        device = "cpu"
        try:
            import ctranslate2

            if ctranslate2.get_cuda_device_count() > 0:
                device = "cuda"
        except Exception:
            device = "cpu"

    if compute_type == "auto":
        compute_type = "float16" if device == "cuda" else "int8"

    return device, compute_type


def parse_formats(raw: str) -> list[str]:
    formats = [item.strip().lower() for item in raw.split(",") if item.strip()]
    allowed = {"txt", "md", "srt", "vtt", "json"}
    unknown = sorted(set(formats) - allowed)
    if unknown:
        raise SystemExit(f"Unsupported output format(s): {', '.join(unknown)}")
    return formats or ["txt", "md"]


def resolve_inputs(inputs: Iterable[str]) -> list[Path]:
    paths: list[Path] = []
    for raw in inputs:
        path = Path(raw).expanduser().resolve()
        if not path.exists():
            raise SystemExit(f"Input not found: {path}")
        if path.is_dir():
            for child in sorted(path.iterdir()):
                if child.suffix.lower() in AUDIO_EXTENSIONS:
                    paths.append(child.resolve())
        else:
            paths.append(path)

    if not paths:
        raise SystemExit("No supported audio/video files found.")
    return paths


def safe_output_path(input_path: Path, output_dir: Path | None, suffix: str) -> Path:
    target_dir = output_dir or input_path.parent
    return target_dir / f"{input_path.stem}.transcript.{suffix}"


def timestamp(seconds: float, separator: str = ",") -> str:
    milliseconds = int(round(seconds * 1000))
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    secs, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02}{separator}{milliseconds:03}"


def plain_text(segments: list[TranscriptSegment]) -> str:
    return "\n".join(segment.text.strip() for segment in segments if segment.text.strip())


def render_srt(segments: list[TranscriptSegment]) -> str:
    blocks = []
    for index, segment in enumerate(segments, start=1):
        blocks.append(
            "\n".join(
                [
                    str(index),
                    f"{timestamp(segment.start)} --> {timestamp(segment.end)}",
                    segment.text.strip(),
                ]
            )
        )
    return "\n\n".join(blocks) + "\n"


def render_vtt(segments: list[TranscriptSegment]) -> str:
    blocks = ["WEBVTT\n"]
    for segment in segments:
        blocks.append(
            "\n".join(
                [
                    f"{timestamp(segment.start, '.')} --> {timestamp(segment.end, '.')}",
                    segment.text.strip(),
                ]
            )
        )
    return "\n\n".join(blocks) + "\n"


def render_md(
    input_path: Path,
    model_name: str,
    language: str | None,
    language_probability: float | None,
    duration: float | None,
    segments: list[TranscriptSegment],
) -> str:
    detected = language or "unknown"
    probability = (
        f"{language_probability:.2%}" if language_probability is not None else "unknown"
    )
    duration_text = f"{duration:.1f}s" if duration is not None else "unknown"
    body = plain_text(segments)
    return "\n".join(
        [
            f"# {input_path.name}",
            "",
            f"- Model: `{model_name}`",
            f"- Language: `{detected}`",
            f"- Language probability: `{probability}`",
            f"- Duration: `{duration_text}`",
            "",
            "## Transcript",
            "",
            body,
            "",
        ]
    )


def write_outputs(
    input_path: Path,
    formats: list[str],
    output_dir: Path | None,
    overwrite: bool,
    model_name: str,
    info,
    segments: list[TranscriptSegment],
) -> list[Path]:
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    text = plain_text(segments)
    language = getattr(info, "language", None)
    language_probability = getattr(info, "language_probability", None)
    duration = getattr(info, "duration", None)

    payloads = {
        "txt": text + "\n",
        "md": render_md(
            input_path,
            model_name,
            language,
            language_probability,
            duration,
            segments,
        ),
        "srt": render_srt(segments),
        "vtt": render_vtt(segments),
        "json": json.dumps(
            {
                "input": str(input_path),
                "model": model_name,
                "language": language,
                "language_probability": language_probability,
                "duration": duration,
                "text": text,
                "segments": [asdict(segment) for segment in segments],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
    }

    for output_format in formats:
        path = safe_output_path(input_path, output_dir, output_format)
        if path.exists() and not overwrite:
            raise SystemExit(f"Output exists, use --overwrite to replace: {path}")
        path.write_text(payloads[output_format], encoding="utf-8")
        written.append(path)
    return written


def transcribe_one(model, input_path: Path, args: argparse.Namespace):
    segments_iter, info = model.transcribe(
        str(input_path),
        language=args.language,
        task=args.task,
        beam_size=args.beam_size,
        vad_filter=args.vad_filter,
        initial_prompt=args.initial_prompt,
        condition_on_previous_text=args.condition_on_previous_text,
    )
    segments = [
        TranscriptSegment(start=item.start, end=item.end, text=item.text)
        for item in segments_iter
    ]
    return info, segments


def transcribe_one_mlx(model_name: str, input_path: Path, args: argparse.Namespace):
    mlx_whisper = import_mlx_whisper()
    result = mlx_whisper.transcribe(
        str(input_path),
        path_or_hf_repo=model_name,
        language=args.language,
        task=args.task,
        initial_prompt=args.initial_prompt,
        condition_on_previous_text=args.condition_on_previous_text,
        verbose=False,
    )
    raw_segments = result.get("segments", [])
    segments = [
        TranscriptSegment(
            start=float(item["start"]),
            end=float(item["end"]),
            text=str(item["text"]),
        )
        for item in raw_segments
    ]
    duration = segments[-1].end if segments else None
    info = TranscriptInfo(
        language=result.get("language") or args.language,
        language_probability=None,
        duration=duration,
    )
    return info, segments


def main() -> int:
    args = parse_args()
    formats = parse_formats(args.formats)
    inputs = resolve_inputs(args.inputs)
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else None
    engine = choose_engine(args.engine)
    model_name = choose_model(engine, args.model)

    model = None
    if engine == "mlx":
        print(f"Using MLX on Apple GPU with model {model_name!r}...", file=sys.stderr)
    else:
        device, compute_type = choose_device_and_compute_type(
            args.device, args.compute_type
        )
        WhisperModel = import_faster_whisper()
        print(
            f"Loading model {model_name!r} on {device} ({compute_type})...",
            file=sys.stderr,
        )
        model = WhisperModel(model_name, device=device, compute_type=compute_type)

    for index, input_path in enumerate(inputs, start=1):
        print(f"[{index}/{len(inputs)}] Transcribing {input_path}", file=sys.stderr)
        if engine == "mlx":
            info, segments = transcribe_one_mlx(model_name, input_path, args)
        else:
            info, segments = transcribe_one(model, input_path, args)
        written = write_outputs(
            input_path=input_path,
            formats=formats,
            output_dir=output_dir,
            overwrite=args.overwrite,
            model_name=f"{engine}:{model_name}",
            info=info,
            segments=segments,
        )
        print("Written:", file=sys.stderr)
        for path in written:
            print(f"  {path}", file=sys.stderr)

        if args.print_text:
            if len(inputs) > 1:
                print(f"\n===== {input_path.name} =====")
            print(plain_text(segments))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
