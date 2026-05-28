#!/usr/bin/env python3
import argparse
import json
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
    stages = [f"fps={args.fps}"]

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

    base = ",".join(stages)
    return (
        f"{base},split[s0][s1];"
        "[s0]palettegen=max_colors=160[p];"
        "[s1][p]paletteuse=dither=bayer:bayer_scale=3"
    )


def main():
    parser = argparse.ArgumentParser(description="Build a short GIF for a key UI interaction from a screen recording.")
    parser.add_argument("video", help="Source video path")
    parser.add_argument("--start", required=True, help="Start time, e.g. 75.2 or 00:01:15.200")
    parser.add_argument("--end", help="End time. Use this or --duration")
    parser.add_argument("--duration", type=float, help="Duration in seconds. Use this or --end")
    parser.add_argument("--output", required=True, help="Output GIF path")
    parser.add_argument("--fps", type=int, default=8, help="GIF frame rate")
    parser.add_argument("--width", type=int, default=720, help="Output width after scaling; 0 keeps original size")
    parser.add_argument("--crop", help="Optional crop box after reading source video: x,y,w,h")
    parser.add_argument("--highlight", help="Optional highlight box after crop: x,y,w,h")
    parser.add_argument("--highlight-color", default="red@0.85", help="ffmpeg drawbox color")
    parser.add_argument("--highlight-thickness", type=int, default=8, help="Highlight box line thickness")
    parser.add_argument("--loop", type=int, default=0, help="GIF loop count, 0 means forever")
    args = parser.parse_args()

    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg must be available in PATH")

    video = Path(args.video).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    if not video.exists():
        raise FileNotFoundError(video)
    if args.fps <= 0:
        raise ValueError("--fps must be positive")
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

    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-ss",
        f"{start:.3f}",
        "-t",
        f"{duration:.3f}",
        "-i",
        str(video),
        "-vf",
        build_filter(args),
        "-loop",
        str(args.loop),
        "-y",
        str(output),
    ]
    run(command)

    print(json.dumps({
        "video": str(video),
        "output": str(output),
        "start": start,
        "duration": duration,
        "fps": args.fps,
        "width": args.width,
        "crop": args.crop,
        "highlight": args.highlight,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
