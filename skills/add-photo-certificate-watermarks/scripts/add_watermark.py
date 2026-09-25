#!/usr/bin/env python3
"""Add non-destructive text watermarks to images and PDFs."""

from __future__ import annotations

import argparse
import io
import os
import sys
from pathlib import Path
from typing import Iterable, Sequence

try:
    from PIL import Image, ImageColor, ImageDraw, ImageFont, ImageOps
except ImportError as exc:  # pragma: no cover - depends on caller environment
    raise SystemExit(
        "Missing dependency Pillow. Install it with: "
        "python3 -m pip install --upgrade Pillow"
    ) from exc


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
SUPPORTED_EXTENSIONS = IMAGE_EXTENSIONS | {".pdf"}

PRESETS = {
    "photo": {
        "layout": "corner",
        "opacity": 62.0,
        "angle": -26.0,
        "color": "#FFFFFF",
        "font_ratio": 0.042,
    },
    "certificate": {
        "layout": "tile",
        "opacity": 22.0,
        "angle": -28.0,
        "color": "#555555",
        "font_ratio": 0.034,
    },
}

CJK_FONT_CANDIDATES = (
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/Library/Fonts/Arial Unicode.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simhei.ttf",
)


def parse_exclusion(raw: str) -> tuple[float, float, float, float]:
    try:
        values = tuple(float(part.strip()) for part in raw.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"Invalid exclusion {raw!r}; expected left,top,right,bottom"
        ) from exc
    if len(values) != 4:
        raise argparse.ArgumentTypeError(
            f"Invalid exclusion {raw!r}; expected four comma-separated values"
        )
    left, top, right, bottom = values
    if not all(0.0 <= value <= 1.0 for value in values):
        raise argparse.ArgumentTypeError("Exclusion coordinates must be between 0 and 1")
    if left >= right or top >= bottom:
        raise argparse.ArgumentTypeError("Exclusion left/top must be smaller than right/bottom")
    return left, top, right, bottom


def has_non_ascii(text: str) -> bool:
    return any(ord(character) > 127 for character in text)


def resolve_font(font_path: str | None, text: str, size: int) -> ImageFont.FreeTypeFont:
    if font_path:
        path = Path(font_path).expanduser()
        if not path.is_file():
            raise FileNotFoundError(f"Font does not exist: {path}")
        return ImageFont.truetype(str(path), size=size)

    for candidate in CJK_FONT_CANDIDATES:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size=size)

    if has_non_ascii(text):
        raise RuntimeError(
            "No CJK-capable font was found. Pass an installed .ttf/.otf/.ttc with --font."
        )

    try:
        return ImageFont.truetype("DejaVuSans.ttf", size=size)
    except OSError as exc:
        raise RuntimeError("No usable font found; provide one with --font") from exc


def parse_color(value: str) -> tuple[int, int, int]:
    try:
        rgb = ImageColor.getrgb(value)
    except ValueError as exc:
        raise ValueError(f"Invalid color {value!r}; use a name or #RRGGBB") from exc
    if len(rgb) == 4:
        return rgb[:3]
    return rgb


def multiline_bbox(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont):
    return draw.multiline_textbbox((0, 0), text, font=font, spacing=max(2, font.size // 5))


def fit_font(
    text: str,
    font_path: str | None,
    initial_size: int,
    maximum_width: int,
) -> ImageFont.FreeTypeFont:
    """Shrink an automatically selected font until every line fits the target width."""
    size = initial_size
    while True:
        font = resolve_font(font_path, text, size)
        scratch = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
        left, _, right, _ = multiline_bbox(ImageDraw.Draw(scratch), text, font)
        text_width = max(1, right - left)
        if text_width <= maximum_width or size <= 6:
            return font
        size = max(6, min(size - 1, round(size * maximum_width / text_width * 0.96)))


def make_stamp(
    text: str,
    font: ImageFont.FreeTypeFont,
    color: tuple[int, int, int],
    alpha: int,
    angle: float,
    add_stroke: bool,
) -> Image.Image:
    scratch = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
    draw = ImageDraw.Draw(scratch)
    left, top, right, bottom = multiline_bbox(draw, text, font)
    padding = max(8, font.size // 2)
    width = max(1, right - left + padding * 2)
    height = max(1, bottom - top + padding * 2)
    stamp = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    stamp_draw = ImageDraw.Draw(stamp)
    stroke_width = max(1, font.size // 24) if add_stroke else 0
    stroke_alpha = min(210, max(60, alpha + 50))
    stamp_draw.multiline_text(
        (padding - left, padding - top),
        text,
        font=font,
        fill=(*color, alpha),
        spacing=max(2, font.size // 5),
        align="center",
        stroke_width=stroke_width,
        stroke_fill=(0, 0, 0, stroke_alpha) if add_stroke else None,
    )
    if angle:
        stamp = stamp.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    return stamp


def apply_exclusions(
    overlay: Image.Image,
    exclusions: Sequence[tuple[float, float, float, float]],
) -> None:
    if not exclusions:
        return
    alpha = overlay.getchannel("A")
    draw = ImageDraw.Draw(alpha)
    width, height = overlay.size
    for left, top, right, bottom in exclusions:
        draw.rectangle(
            (
                round(left * width),
                round(top * height),
                round(right * width),
                round(bottom * height),
            ),
            fill=0,
        )
    overlay.putalpha(alpha)


def build_overlay(
    size: tuple[int, int],
    text: str,
    preset: str,
    layout: str,
    opacity: float,
    angle: float,
    color_value: str,
    font_path: str | None,
    font_size: int | None,
    exclusions: Sequence[tuple[float, float, float, float]],
) -> Image.Image:
    width, height = size
    if width < 2 or height < 2:
        raise ValueError(f"Invalid canvas dimensions: {width}x{height}")
    ratio = float(PRESETS[preset]["font_ratio"])
    selected_font_size = font_size or max(14, round(min(width, height) * ratio))
    maximum_text_width = round(width * (0.58 if layout == "tile" else 0.78))
    font = resolve_font(font_path, text, selected_font_size)
    if font_size is None:
        font = fit_font(text, font_path, selected_font_size, maximum_text_width)
    color = parse_color(color_value)
    alpha = round(255 * opacity / 100.0)
    overlay = Image.new("RGBA", size, (0, 0, 0, 0))

    if layout == "tile":
        stamp = make_stamp(text, font, color, alpha, angle, add_stroke=False)
        step_x = max(1, round(stamp.width * 1.28))
        step_y = max(1, round(stamp.height * 1.65))
        row = 0
        for y in range(-stamp.height, height + stamp.height, step_y):
            offset = -(step_x // 2) if row % 2 else 0
            for x in range(-stamp.width + offset, width + stamp.width, step_x):
                overlay.alpha_composite(stamp, (x, y))
            row += 1
    elif layout == "center":
        stamp = make_stamp(text, font, color, alpha, angle, add_stroke=preset == "photo")
        overlay.alpha_composite(stamp, ((width - stamp.width) // 2, (height - stamp.height) // 2))
    else:
        stamp = make_stamp(text, font, color, alpha, 0.0, add_stroke=True)
        margin = max(12, round(min(width, height) * 0.025))
        overlay.alpha_composite(stamp, (width - stamp.width - margin, height - stamp.height - margin))

    apply_exclusions(overlay, exclusions)
    return overlay


def collect_inputs(
    raw_paths: Iterable[str],
    recursive: bool,
    excluded_directory: Path | None = None,
) -> list[Path]:
    discovered: list[Path] = []
    for raw in raw_paths:
        path = Path(raw).expanduser()
        if not path.exists():
            raise FileNotFoundError(f"Input does not exist: {path}")
        if path.is_file():
            if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                raise ValueError(f"Unsupported input format: {path}")
            discovered.append(path.resolve())
            continue
        iterator = path.rglob("*") if recursive else path.glob("*")
        discovered.extend(
            child.resolve()
            for child in sorted(iterator)
            if child.is_file()
            and child.suffix.lower() in SUPPORTED_EXTENSIONS
            and not (
                excluded_directory is not None
                and excluded_directory in child.resolve().parents
            )
        )
    unique = list(dict.fromkeys(discovered))
    if not unique:
        raise ValueError("No supported JPEG, PNG, WebP, or PDF inputs were found")
    return unique


def output_path_for(input_path: Path, output_dir: Path, preview: bool) -> Path:
    if preview:
        return output_dir / f"{input_path.stem}_preview.png"
    return output_dir / f"{input_path.stem}_watermarked{input_path.suffix.lower()}"


def ensure_available(path: Path) -> None:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite existing output: {path}")


def save_image(
    image: Image.Image,
    destination: Path,
    input_image: Image.Image | None,
    keep_metadata: bool,
) -> None:
    suffix = destination.suffix.lower()
    save_options: dict[str, object] = {}
    if keep_metadata and input_image is not None:
        exif = input_image.getexif()
        if 274 in exif:
            del exif[274]
        if exif:
            save_options["exif"] = exif.tobytes()
        icc_profile = input_image.info.get("icc_profile")
        if icc_profile:
            save_options["icc_profile"] = icc_profile

    if suffix in {".jpg", ".jpeg"}:
        flattened = Image.new("RGB", image.size, "white")
        flattened.paste(image, mask=image.getchannel("A") if image.mode == "RGBA" else None)
        flattened.save(destination, quality=95, subsampling=0, **save_options)
    elif suffix == ".webp":
        image.save(destination, quality=95, method=6, **save_options)
    else:
        image.save(destination, optimize=True, **save_options)


def process_image(
    input_path: Path,
    destination: Path,
    args: argparse.Namespace,
) -> None:
    ensure_available(destination)
    with Image.open(input_path) as source:
        base = ImageOps.exif_transpose(source).convert("RGBA")
        overlay = build_overlay(
            base.size,
            args.text,
            args.preset,
            args.layout,
            args.opacity,
            args.angle,
            args.color,
            args.font,
            args.font_size,
            args.exclude,
        )
        result = Image.alpha_composite(base, overlay)
        save_image(result, destination, source, args.keep_metadata and not args.preview_only)


def import_fitz():
    try:
        import fitz
    except ImportError as exc:  # pragma: no cover - depends on caller environment
        raise RuntimeError(
            "Missing dependency PyMuPDF. Install it with: "
            "python3 -m pip install --upgrade PyMuPDF"
        ) from exc
    return fitz


def overlay_png_bytes(size: tuple[int, int], args: argparse.Namespace) -> bytes:
    overlay = build_overlay(
        size,
        args.text,
        args.preset,
        args.layout,
        args.opacity,
        args.angle,
        args.color,
        args.font,
        args.font_size,
        args.exclude,
    )
    buffer = io.BytesIO()
    overlay.save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()


def process_pdf_preview(input_path: Path, destination: Path, args: argparse.Namespace) -> None:
    fitz = import_fitz()
    ensure_available(destination)
    with fitz.open(input_path) as document:
        if document.needs_pass:
            raise RuntimeError(f"Encrypted PDF requires a password: {input_path.name}")
        if document.page_count == 0:
            raise RuntimeError(f"PDF has no pages: {input_path.name}")
        page = document[0]
        pixmap = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0), alpha=False)
        base = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples).convert("RGBA")
        overlay = build_overlay(
            base.size,
            args.text,
            args.preset,
            args.layout,
            args.opacity,
            args.angle,
            args.color,
            args.font,
            args.font_size,
            args.exclude,
        )
        Image.alpha_composite(base, overlay).save(destination, optimize=True)


def process_pdf(input_path: Path, destination: Path, args: argparse.Namespace) -> None:
    fitz = import_fitz()
    ensure_available(destination)
    with fitz.open(input_path) as document:
        if document.needs_pass:
            raise RuntimeError(f"Encrypted PDF requires a password: {input_path.name}")
        if document.page_count == 0:
            raise RuntimeError(f"PDF has no pages: {input_path.name}")
        for page in document:
            rect = page.rect
            pixel_size = (max(2, round(rect.width * 2)), max(2, round(rect.height * 2)))
            page.insert_image(
                rect,
                stream=overlay_png_bytes(pixel_size, args),
                overlay=True,
                keep_proportion=False,
            )
        document.save(destination, garbage=3, deflate=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="Input files or directories")
    parser.add_argument("--output-dir", required=True, help="Separate output directory")
    parser.add_argument("--text", required=True, help="Watermark text")
    parser.add_argument("--preset", choices=sorted(PRESETS), required=True)
    parser.add_argument("--layout", choices=("auto", "tile", "corner", "center"), default="auto")
    parser.add_argument("--opacity", type=float, help="Opacity percentage from 1 to 100")
    parser.add_argument("--angle", type=float, help="Rotation angle in degrees")
    parser.add_argument("--color", help="Text color name or #RRGGBB")
    parser.add_argument("--font", help="Path to an installed .ttf/.otf/.ttc font")
    parser.add_argument("--font-size", type=int, help="Font size in output pixels")
    parser.add_argument(
        "--exclude",
        type=parse_exclusion,
        action="append",
        default=[],
        metavar="L,T,R,B",
        help="Normalized exclusion rectangle; repeat as needed",
    )
    parser.add_argument("--preview-only", action="store_true", help="Render only the first input/page to PNG")
    parser.add_argument("--recursive", action="store_true", help="Search input directories recursively")
    parser.add_argument("--keep-metadata", action="store_true", help="Preserve image EXIF/ICC metadata")
    return parser


def normalize_args(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    preset = PRESETS[args.preset]
    args.layout = preset["layout"] if args.layout == "auto" else args.layout
    args.opacity = float(preset["opacity"] if args.opacity is None else args.opacity)
    args.angle = float(preset["angle"] if args.angle is None else args.angle)
    args.color = str(preset["color"] if args.color is None else args.color)
    if not args.text.strip():
        parser.error("--text cannot be empty")
    if not 1.0 <= args.opacity <= 100.0:
        parser.error("--opacity must be between 1 and 100")
    if args.font_size is not None and args.font_size < 6:
        parser.error("--font-size must be at least 6")
    if args.keep_metadata and args.preview_only:
        args.keep_metadata = False


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    normalize_args(args, parser)

    try:
        output_dir = Path(args.output_dir).expanduser().resolve()
        inputs = collect_inputs(args.inputs, args.recursive, excluded_directory=output_dir)
        if args.preview_only:
            inputs = inputs[:1]
        output_dir.mkdir(parents=True, exist_ok=True)

        successes: list[Path] = []
        failures: list[tuple[Path, str]] = []
        for input_path in inputs:
            destination = output_path_for(input_path, output_dir, args.preview_only)
            try:
                if input_path.suffix.lower() == ".pdf":
                    if args.preview_only:
                        process_pdf_preview(input_path, destination, args)
                    else:
                        process_pdf(input_path, destination, args)
                else:
                    process_image(input_path, destination, args)
                successes.append(destination)
                print(f"OK\t{input_path}\t{destination}")
            except Exception as exc:  # continue batch, report exact failed file
                failures.append((input_path, str(exc)))
                print(f"ERROR\t{input_path}\t{exc}", file=sys.stderr)

        print(f"SUMMARY\tsucceeded={len(successes)}\tfailed={len(failures)}")
        return 1 if failures else 0
    except Exception as exc:
        print(f"ERROR\t{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
