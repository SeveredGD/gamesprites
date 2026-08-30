from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "final-generated"
OUTPUT = ROOT / "production"
FONT = Path(r"C:\Users\garre\Downloads\Everdeep Font Mockups\fonts\Grenze.ttf")
NAMES = ("combat", "runs", "gear", "skills", "more")
SIZES = (72, 80, 96, 128)


def fit_font(label: str, size: int) -> ImageFont.FreeTypeFont:
    target_width = size * 0.72
    font_size = max(10, round(size * 0.16))
    while font_size > 8:
        font = ImageFont.truetype(str(FONT), font_size)
        box = font.getbbox(label)
        if box[2] - box[0] <= target_width:
            return font
        font_size -= 1
    return ImageFont.truetype(str(FONT), 8)


def label_button(im: Image.Image, name: str, size: int) -> Image.Image:
    label = name.upper()
    draw = ImageDraw.Draw(im)
    font = fit_font(label, size)
    box = draw.textbbox((0, 0), label, font=font, stroke_width=1)
    text_w, text_h = box[2] - box[0], box[3] - box[1]
    # Generated buttons reserve the bottom plaque. Center type at ~82% height.
    x = (size - text_w) // 2
    y = round(size * 0.815 - text_h / 2) - box[1]
    draw.text((x + 1, y + 1), label, font=font, fill=(0, 0, 0, 210), stroke_width=1, stroke_fill=(0, 0, 0, 230))
    draw.text((x, y), label, font=font, fill=(230, 218, 187, 255), stroke_width=1, stroke_fill=(30, 35, 42, 255))
    return im


def active_variant(im: Image.Image, size: int) -> Image.Image:
    active = ImageEnhance.Brightness(im).enhance(1.08)
    draw = ImageDraw.Draw(active)
    w = max(1, round(size / 64))
    inset = max(1, round(size * 0.025))
    draw.rectangle((inset, inset, size - 1 - inset, size - 1 - inset), outline=(236, 213, 164, 255), width=w)
    draw.rectangle((inset + w, inset + w, size - 1 - inset - w, size - 1 - inset - w), outline=(156, 121, 65, 225), width=1)
    return active


def build() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest = {"format": "everdeep-mobile-nav-v2", "labelsEmbedded": True, "buttons": []}
    for size in SIZES:
        size_dir = OUTPUT / f"{size}px"
        size_dir.mkdir(exist_ok=True)
        for name in NAMES:
            src = Image.open(SOURCE / f"{name}.png").convert("RGBA")
            base = src.resize((size, size), Image.Resampling.LANCZOS)
            base = ImageEnhance.Sharpness(base).enhance(1.35)
            base = label_button(base, name, size)
            normal_path = size_dir / f"nav-{name}.png"
            active_path = size_dir / f"nav-{name}-active.png"
            base.save(normal_path, optimize=True)
            active_variant(base.copy(), size).save(active_path, optimize=True)
        manifest["buttons"].append({"size": size, "folder": f"{size}px", "states": ["normal", "active"]})
    manifest["order"] = list(NAMES)
    (OUTPUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    # QA strip at the likely mobile target size.
    tile, gap = 96, 8
    qa = Image.new("RGBA", (gap + len(NAMES) * (tile + gap), tile * 2 + gap * 3), (12, 13, 17, 255))
    for col, name in enumerate(NAMES):
        x = gap + col * (tile + gap)
        qa.alpha_composite(Image.open(OUTPUT / "96px" / f"nav-{name}.png").convert("RGBA"), (x, gap))
        qa.alpha_composite(Image.open(OUTPUT / "96px" / f"nav-{name}-active.png").convert("RGBA"), (x, tile + gap * 2))
    qa.save(OUTPUT / "qa-normal-active-96px.png")
    print(f"Built {len(NAMES)} buttons × {len(SIZES)} sizes × 2 states")


if __name__ == "__main__":
    build()
