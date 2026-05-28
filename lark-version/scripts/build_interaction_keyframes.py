#!/usr/bin/env python3
import argparse
import json
import math
import shutil
import subprocess
from pathlib import Path


def run(command):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout


def parse_time(value):
    value = value.strip()
    if not value:
        raise ValueError("empty timestamp")
    parts = value.split(":")
    if len(parts) == 1:
        return float(parts[0])
    if len(parts) == 2:
        return int(parts[0]) * 60 + float(parts[1])
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    raise ValueError(f"bad timestamp: {value}")


def parse_box(value, name):
    try:
        parts = [int(float(item.strip())) for item in value.split(",")]
    except ValueError as exc:
        raise ValueError(f"{name} must be x,y,w,h") from exc
    if len(parts) != 4:
        raise ValueError(f"{name} must be x,y,w,h")
    x, y, w, h = parts
    if w <= 0 or h <= 0:
        raise ValueError(f"{name} width and height must be positive")
    return x, y, w, h


def build_filter(args):
    stages = []
    if args.crop:
        x, y, w, h = parse_box(args.crop, "--crop")
        stages.append(f"crop={w}:{h}:{x}:{y}")
    if args.highlight:
        x, y, w, h = parse_box(args.highlight, "--highlight")
        stages.append(
            "drawbox="
            f"x={x}:y={y}:w={w}:h={h}:"
            f"color={args.highlight_color}:t={args.highlight_thickness}"
        )
    if args.width:
        stages.append(f"scale={args.width}:-1:flags=lanczos")
    return ",".join(stages) if stages else "null"


def sample_times(start, duration, frames):
    if frames == 1:
        return [start + duration / 2]
    end = start + max(duration - 0.04, 0.01)
    return [start + (end - start) * i / (frames - 1) for i in range(frames)]


def build_strip(output_dir, name, frames, columns, margin, padding):
    columns = columns or min(frames, 4)
    rows = math.ceil(frames / columns)
    strip = output_dir / f"{name}-strip.png"
    pattern = output_dir / f"{name}-%02d.png"
    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-framerate",
        "1",
        "-start_number",
        "1",
        "-i",
        str(pattern),
        "-frames:v",
        "1",
        "-vf",
        f"tile={columns}x{rows}:margin={margin}:padding={padding}:color=white",
        "-y",
        str(strip),
    ]
    run(command)
    return strip


def main():
    parser = argparse.ArgumentParser(
        description="Export static PNG keyframes for a key UI interaction from a screen recording."
    )
    parser.add_argument("video", help="Source video path")
    parser.add_argument("--start", required=True, help="Start time, e.g. 75.2 or 00:01:15.200")
    parser.add_argument("--end", help="End time. Use this or --duration")
    parser.add_argument("--duration", type=float, help="Duration in seconds. Use this or --end")
    parser.add_argument("--output-dir", required=True, help="Directory for generated PNG files")
    parser.add_argument("--name", default="interaction", help="Output file prefix")
    parser.add_argument("--frames", type=int, default=4, help="Number of keyframes to export")
    parser.add_argument("--width", type=int, default=720, help="Output width after scaling; 0 keeps original size")
    parser.add_argument("--crop", help="Optional crop box after reading source video: x,y,w,h")
    parser.add_argument("--highlight", help="Optional highlight box after crop: x,y,w,h")
    parser.add_argument("--highlight-color", default="red@0.85", help="ffmpeg drawbox color")
    parser.add_argument("--highlight-thickness", type=int, default=8, help="Highlight box line thickness")
    parser.add_argument("--make-strip", action="store_true", help="Also create a tiled PNG strip")
    parser.add_argument("--strip-columns", type=int, default=0, help="Columns for the tiled strip; default min(frames, 4)")
    parser.add_argument("--strip-margin", type=int, default=24, help="Tiled strip outer margin")
    parser.add_argument("--strip-padding", type=int, default=16, help="Tiled strip gap between frames")
    args = parser.parse_args()

    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg must be available in PATH")

    video = Path(args.video).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    if not video.exists():
        raise FileNotFoundError(video)
    if args.frames <= 0:
        raise ValueError("--frames must be positive")
    if args.width < 0:
        raise ValueError("--width cannot be negative")

    start = parse_time(args.start)
    if args.end:
        duration = parse_time(args.end) - start
    elif args.duration:
        duration = args.duration
    else:
        raise ValueError("use --end or --duration")
    if duration <= 0:
        raise ValueError("duration must be positive")

    output_dir.mkdir(parents=True, exist_ok=True)
    vf = build_filter(args)
    files = []
    for index, timestamp in enumerate(sample_times(start, duration, args.frames), 1):
        output = output_dir / f"{args.name}-{index:02d}.png"
        command = [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            f"{timestamp:.3f}",
            "-i",
            str(video),
            "-frames:v",
            "1",
            "-vf",
            vf,
            "-y",
            str(output),
        ]
        run(command)
        files.append(str(output))

    strip = None
    if args.make_strip:
        strip = str(build_strip(output_dir, args.name, args.frames, args.strip_columns, args.strip_margin, args.strip_padding))

    print(json.dumps({
        "video": str(video),
        "output_dir": str(output_dir),
        "frames": files,
        "strip": strip,
        "start": start,
        "duration": duration,
        "width": args.width,
        "crop": args.crop,
        "highlight": args.highlight,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
