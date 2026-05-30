#!/usr/bin/env python3
import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageSequence


def parse_box(value):
    try:
        parts = [int(float(item.strip())) for item in value.split(",")]
    except ValueError as exc:
        raise ValueError("--highlight must be x,y,w,h") from exc
    if len(parts) != 4:
        raise ValueError("--highlight must be x,y,w,h")
    x, y, w, h = parts
    if w <= 0 or h <= 0:
        raise ValueError("--highlight width and height must be positive")
    return x, y, w, h


def sample_indices(total, count):
    if count <= 0:
        raise ValueError("--frames must be positive")
    if total <= 0:
        return []
    if count == 1:
        return [total // 2]
    return sorted(set(round((total - 1) * i / (count - 1)) for i in range(count)))


def draw_highlight(image, box, color, width):
    if not box:
        return image
    x, y, w, h = box
    out = image.copy()
    draw = ImageDraw.Draw(out)
    for offset in range(width):
        draw.rectangle((x - offset, y - offset, x + w + offset, y + h + offset), outline=color)
    return out


def make_strip(frames, labels, output, columns, margin, padding, label_height):
    columns = columns or min(len(frames), 4)
    rows = math.ceil(len(frames) / columns)
    cell_w, cell_h = frames[0].size
    strip = Image.new(
        "RGB",
        (
            columns * cell_w + (columns + 1) * padding,
            rows * (cell_h + label_height) + (rows + 1) * padding,
        ),
        "white",
    )
    draw = ImageDraw.Draw(strip)
    for index, frame in enumerate(frames):
        row, col = divmod(index, columns)
        x = padding + col * (cell_w + padding)
        y = padding + row * (cell_h + label_height + padding)
        draw.text((x, y), labels[index], fill="#111111")
        strip.paste(frame.convert("RGB"), (x, y + label_height))
    canvas = Image.new("RGB", (strip.width + margin * 2, strip.height + margin * 2), "#f6f7fb")
    canvas.paste(strip, (margin, margin))
    canvas.save(output)


def main():
    parser = argparse.ArgumentParser(description="Export sampled PNG keyframes and a contact sheet from a GIF interaction.")
    parser.add_argument("gif", help="Source GIF path")
    parser.add_argument("--output-dir", required=True, help="Directory for generated PNG files")
    parser.add_argument("--name", default="gif-interaction", help="Output file prefix")
    parser.add_argument("--frames", type=int, default=9, help="Number of sampled frames")
    parser.add_argument("--width", type=int, default=720, help="Output width after scaling; 0 keeps original width")
    parser.add_argument("--highlight", help="Optional highlight box: x,y,w,h")
    parser.add_argument("--highlight-color", default="#ff2b24", help="Highlight rectangle color")
    parser.add_argument("--highlight-thickness", type=int, default=6, help="Highlight rectangle thickness")
    parser.add_argument("--make-strip", action="store_true", help="Also create a contact sheet PNG")
    parser.add_argument("--strip-columns", type=int, default=0, help="Columns for contact sheet; default min(frames, 4)")
    args = parser.parse_args()

    source = Path(args.gif).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    if not source.exists():
        raise FileNotFoundError(source)
    if args.width < 0:
        raise ValueError("--width cannot be negative")

    output_dir.mkdir(parents=True, exist_ok=True)
    box = parse_box(args.highlight) if args.highlight else None

    image = Image.open(source)
    raw_frames = []
    durations = []
    for frame in ImageSequence.Iterator(image):
        raw_frames.append(frame.convert("RGBA"))
        durations.append(frame.info.get("duration", 0))
    indices = sample_indices(len(raw_frames), args.frames)

    saved = []
    strip_frames = []
    labels = []
    for index in indices:
        frame = raw_frames[index]
        if args.width:
            height = round(frame.height * args.width / frame.width)
            frame = frame.resize((args.width, height), Image.Resampling.LANCZOS)
            scale = args.width / raw_frames[index].width
            scaled_box = tuple(round(value * scale) for value in box) if box else None
        else:
            scaled_box = box
        frame = draw_highlight(frame, scaled_box, args.highlight_color, args.highlight_thickness)
        output = output_dir / f"{args.name}-{index:03d}.png"
        frame.save(output)
        saved.append(str(output))
        strip_frames.append(frame)
        labels.append(f"frame {index}  t={sum(durations[:index]) / 1000:.2f}s")

    strip = None
    if args.make_strip and strip_frames:
        strip = output_dir / f"{args.name}-strip.png"
        make_strip(strip_frames, labels, strip, args.strip_columns, margin=0, padding=18, label_height=34)

    print(json.dumps({
        "gif": str(source),
        "width": image.width,
        "height": image.height,
        "frame_count": len(raw_frames),
        "duration_ms_total": sum(durations),
        "duration_ms_min": min(durations) if durations else None,
        "duration_ms_max": max(durations) if durations else None,
        "sample_indices": indices,
        "frames": saved,
        "strip": str(strip) if strip else None,
        "highlight": args.highlight,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
