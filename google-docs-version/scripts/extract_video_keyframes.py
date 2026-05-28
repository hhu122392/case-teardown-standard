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


def fmt_time(seconds):
    seconds = max(0.0, float(seconds))
    whole = int(seconds)
    ms = int(round((seconds - whole) * 1000))
    h = whole // 3600
    m = (whole % 3600) // 60
    s = whole % 60
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"
    return f"{m:02d}:{s:02d}.{ms:03d}"


def duration(video):
    output = run([
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "json",
        str(video),
    ])
    data = json.loads(output)
    return float(data["format"]["duration"])


def build_times(video_duration, explicit_times, every, max_frames):
    if explicit_times:
        return [parse_time(item) for item in explicit_times.split(",")]

    if every <= 0:
        raise ValueError("--every must be greater than 0")

    start = min(3.0, max(0.0, video_duration / 10))
    times = []
    current = start
    while current < video_duration:
        times.append(current)
        current += every

    if max_frames and len(times) > max_frames:
        if max_frames == 1:
            return [video_duration / 2]
        step = (video_duration - start) / (max_frames - 1)
        times = [start + step * i for i in range(max_frames)]

    return [min(t, max(0.0, video_duration - 0.2)) for t in times]


def extract_frame(video, timestamp, output):
    run([
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
        "-y",
        str(output),
    ])


def main():
    parser = argparse.ArgumentParser(description="Extract key screenshots from a video for case teardown work.")
    parser.add_argument("video", help="Path to the video file")
    parser.add_argument("--out-dir", required=True, help="Directory for PNG screenshots and manifest.md")
    parser.add_argument("--times", help="Comma-separated timestamps, e.g. 00:00:03,00:00:18,72.5")
    parser.add_argument("--every", type=float, default=12.0, help="Sampling interval in seconds when --times is not set")
    parser.add_argument("--max-frames", type=int, default=18, help="Maximum frames when --times is not set")
    parser.add_argument("--prefix", default="frame", help="Screenshot file prefix")
    args = parser.parse_args()

    video = Path(args.video).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()

    if not video.exists():
        raise FileNotFoundError(video)
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise RuntimeError("ffmpeg and ffprobe must be available in PATH")

    out_dir.mkdir(parents=True, exist_ok=True)
    video_duration = duration(video)
    timestamps = build_times(video_duration, args.times, args.every, args.max_frames)

    records = []
    for index, timestamp in enumerate(timestamps, start=1):
        safe_time = fmt_time(timestamp).replace(":", "-").replace(".", "-")
        image = out_dir / f"{args.prefix}_{index:02d}_{safe_time}.png"
        extract_frame(video, timestamp, image)
        records.append({
            "index": index,
            "timestamp": fmt_time(timestamp),
            "seconds": round(timestamp, 3),
            "path": str(image),
        })

    manifest = out_dir / "manifest.md"
    lines = [
        "# Video Keyframes",
        "",
        f"- Video: `{video}`",
        f"- Duration: `{fmt_time(video_duration)}`",
        "",
        "| # | Timestamp | Image | Notes |",
        "|---|---:|---|---|",
    ]
    for record in records:
        path = record["path"].replace("\\", "/")
        lines.append(f"| {record['index']} | {record['timestamp']} | `{path}` |  |")
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "video": str(video),
        "duration": video_duration,
        "out_dir": str(out_dir),
        "manifest": str(manifest),
        "frames": records,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
