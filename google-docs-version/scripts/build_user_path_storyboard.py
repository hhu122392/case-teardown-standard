#!/usr/bin/env python3
import argparse
import csv
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def load_font(size):
    candidates = [
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simsun.ttc"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def wrap_text(draw, text, font, max_width):
    if not text:
        return []
    lines = []
    current = ""
    for char in text:
        test = current + char
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width or not current:
            current = test
        else:
            lines.append(current)
            current = char
    if current:
        lines.append(current)
    return lines


def read_items(path):
    items = []
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        for row in reader:
            if not row or not "".join(row).strip() or row[0].strip().startswith("#"):
                continue
            image = row[0].strip()
            caption = row[1].strip() if len(row) > 1 else ""
            note = row[2].strip() if len(row) > 2 else ""
            items.append({"image": image, "caption": caption, "note": note})
    if not items:
        raise ValueError("items file is empty")
    return items


def fit_image(image, max_w, max_h):
    image = image.convert("RGB")
    ratio = min(max_w / image.width, max_h / image.height)
    size = (max(1, int(image.width * ratio)), max(1, int(image.height * ratio)))
    return image.resize(size, Image.Resampling.LANCZOS)


def draw_arrow(draw, x1, y, x2):
    draw.line((x1, y, x2, y), fill=(70, 70, 70), width=3)
    draw.polygon([(x2, y), (x2 - 12, y - 7), (x2 - 12, y + 7)], fill=(70, 70, 70))


def build_storyboard(items, output, columns, thumb_w, thumb_h):
    title_font = load_font(34)
    note_font = load_font(26)
    small_font = load_font(16)

    margin_x = 72
    margin_y = 72
    gap_x = 48
    gap_y = 72
    caption_h = 128
    note_h = 112
    index_h = 28
    card_w = thumb_w
    card_h = index_h + thumb_h + caption_h + note_h

    rows = math.ceil(len(items) / columns)
    width = margin_x * 2 + columns * card_w + (columns - 1) * gap_x
    height = margin_y * 2 + rows * card_h + (rows - 1) * gap_y

    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)

    for idx, item in enumerate(items):
        row = idx // columns
        col = idx % columns
        x = margin_x + col * (card_w + gap_x)
        y = margin_y + row * (card_h + gap_y)

        img = Image.open(item["image"])
        fitted = fit_image(img, thumb_w, thumb_h)
        img_x = x + (thumb_w - fitted.width) // 2
        img_y = y + index_h

        draw.rounded_rectangle((img_x - 8, img_y - 8, img_x + fitted.width + 8, img_y + fitted.height + 8), radius=6, outline=(28, 28, 28), width=2)
        canvas.paste(fitted, (img_x, img_y))

        step_text = f"{idx + 1:02d}"
        draw.text((x, y), step_text, font=small_font, fill=(120, 120, 120))

        caption_lines = wrap_text(draw, item["caption"], title_font, card_w)
        caption_y = y + index_h + thumb_h + 22
        for line in caption_lines[:2]:
            bbox = draw.textbbox((0, 0), line, font=title_font)
            draw.text((x + (card_w - (bbox[2] - bbox[0])) / 2, caption_y), line, font=title_font, fill=(20, 20, 20))
            caption_y += 42

        note_lines = wrap_text(draw, item["note"], note_font, card_w)
        note_y = y + index_h + thumb_h + caption_h
        for line in note_lines[:3]:
            bbox = draw.textbbox((0, 0), line, font=note_font)
            draw.text((x + (card_w - (bbox[2] - bbox[0])) / 2, note_y), line, font=note_font, fill=(85, 85, 85))
            note_y += 34

        next_same_row = idx + 1 < len(items) and (idx + 1) // columns == row
        if next_same_row:
            arrow_y = y + index_h + thumb_h // 2
            draw_arrow(draw, x + card_w + 8, arrow_y, x + card_w + gap_x - 8)

    canvas.save(output)


def chunk_items(items, chunk_size):
    for start in range(0, len(items), chunk_size):
        yield start, items[start:start + chunk_size]


def chunk_output_path(output, start, chunk):
    if len(chunk) == 1:
        suffix = f"{start + 1:02d}"
    else:
        suffix = f"{start + 1:02d}-{start + len(chunk):02d}"
    return output.with_name(f"{output.stem}-{suffix}{output.suffix}")


def main():
    parser = argparse.ArgumentParser(description="Build a screenshot-based user path storyboard image.")
    parser.add_argument("--items", required=True, help="TSV file: image path, caption, note")
    parser.add_argument("--output", required=True, help="Output image path")
    parser.add_argument("--columns", type=int, default=2, help="Cards per row")
    parser.add_argument("--thumb-width", type=int, default=720, help="Max screenshot width")
    parser.add_argument("--thumb-height", type=int, default=1558, help="Max screenshot height")
    parser.add_argument("--chunk-size", type=int, default=2, help="Also create numbered segment images with this many steps each; use 0 to disable")
    args = parser.parse_args()

    items_path = Path(args.items).resolve()
    items = read_items(items_path)
    base = items_path.parent
    for item in items:
        path = Path(item["image"])
        if not path.is_absolute():
            path = base / path
        item["image"] = str(path.resolve())
        if not Path(item["image"]).exists():
            raise FileNotFoundError(item["image"])

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    if args.columns < 1:
        raise ValueError("--columns must be a positive integer")
    build_storyboard(items, output, args.columns, args.thumb_width, args.thumb_height)
    print(str(output))

    if args.chunk_size:
        if args.chunk_size < 1:
            raise ValueError("--chunk-size must be a positive integer")
        for start, chunk in chunk_items(items, args.chunk_size):
            chunk_output = chunk_output_path(output, start, chunk)
            build_storyboard(chunk, chunk_output, min(args.columns, len(chunk)), args.thumb_width, args.thumb_height)
            print(str(chunk_output))


if __name__ == "__main__":
    main()
