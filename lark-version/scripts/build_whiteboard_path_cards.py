#!/usr/bin/env python3
import argparse
import csv
import json
import math
from pathlib import Path


COLORS = ["#EAF2FF", "#FFF4E5", "#ECFDF3", "#F5F3FF"]


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


def wrap_text(text, width=18):
    text = (text or "").strip()
    if not text:
        return ""
    lines = []
    current = ""
    for char in text:
        if char == "\n":
            if current:
                lines.append(current)
                current = ""
            continue
        candidate = current + char
        if len(candidate) <= width or not current:
            current = candidate
        else:
            lines.append(current)
            current = char
    if current:
        lines.append(current)
    return "\n".join(lines[:8])


def build_document(items, title, columns):
    card_w = 360
    card_h = 238
    gap_x = 70
    gap_y = 120
    start_x = 40
    start_y = 128

    nodes = [
        {
            "type": "text",
            "id": "title",
            "x": start_x,
            "y": 28,
            "width": columns * card_w + (columns - 1) * gap_x,
            "height": "fit-content",
            "text": title,
            "fontSize": 34,
            "textColor": "#111827",
            "textAlign": "left",
        }
    ]

    for idx, item in enumerate(items):
        row = idx // columns
        col = idx % columns
        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)
        image_name = Path(item["image"]).name
        text = (
            f"{idx + 1:02d} - {wrap_text(item['caption'], 16)}\n\n"
            f"{wrap_text(item['note'], 19)}\n\n"
            f"截图：{image_name}"
        )
        nodes.append(
            {
                "type": "rect",
                "id": f"step_{idx + 1}",
                "x": x,
                "y": y,
                "width": card_w,
                "height": card_h,
                "fillColor": COLORS[row % len(COLORS)],
                "borderColor": "#334155",
                "borderWidth": 2,
                "borderRadius": 12,
                "text": text,
                "fontSize": 16,
                "textColor": "#111827",
                "textAlign": "left",
                "verticalAlign": "top",
            }
        )

    for idx in range(len(items) - 1):
        current_row = idx // columns
        next_row = (idx + 1) // columns
        same_row = current_row == next_row
        nodes.append(
            {
                "type": "connector",
                "id": f"conn_{idx + 1}_{idx + 2}",
                "connector": {
                    "from": f"step_{idx + 1}",
                    "to": f"step_{idx + 2}",
                    "fromAnchor": "right" if same_row else "bottom",
                    "toAnchor": "left" if same_row else "top",
                    "lineShape": "straight" if same_row else "rightAngle",
                    "lineColor": "#64748B",
                    "lineWidth": 2,
                    "endArrow": "arrow",
                },
            }
        )

    return {"version": 2, "nodes": nodes}


def main():
    parser = argparse.ArgumentParser(description="Build a Lark whiteboard card graph from storyboard TSV.")
    parser.add_argument("--items", required=True, help="TSV file: image path, caption, note")
    parser.add_argument("--output", required=True, help="Output whiteboard DSL JSON path")
    parser.add_argument("--title", default="用户完整路径图", help="Whiteboard title")
    parser.add_argument("--columns", type=int, default=6, help="Cards per row")
    args = parser.parse_args()

    items_path = Path(args.items).resolve()
    items = read_items(items_path)
    if args.columns < 2:
        raise ValueError("--columns must be at least 2")

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    document = build_document(items, args.title, args.columns)
    output.write_text(json.dumps(document, ensure_ascii=False, indent=2), encoding="utf-8")
    rows = math.ceil(len(items) / args.columns)
    print(f"{output} ({len(items)} steps, {rows} rows)")


if __name__ == "__main__":
    main()
