from collections import deque
from pathlib import Path
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "runeforge-strongbox-generated.png"
SOURCE_MASTER = ROOT / "runeforge-strongbox-source-master-1672x941.png"
MASTER = ROOT / "runeforge-strongbox-master-1935x813.png"
STAGE = ROOT / "runeforge-strongbox-master-1284x540.png"
SLICES = ROOT / "slices"
TARGET_SIZE = (1935, 813)

CONTENT_WELLS_SOURCE = {
    "equipment": (133, 130, 778, 807),
    "vault": (895, 130, 1540, 807),
}

SLICE_BOXES = {
    "outer-top-left": (0, 0, 150, 150),
    "outer-top-edge": (190, 20, 650, 130),
    "outer-top-right": (1522, 0, 1672, 150),
    "outer-left-edge": (0, 190, 150, 520),
    "outer-right-edge": (1522, 190, 1672, 520),
    "outer-bottom-left": (0, 791, 150, 941),
    "outer-bottom-edge": (190, 811, 650, 921),
    "outer-bottom-right": (1522, 791, 1672, 941),
    "divider-top": (760, 0, 912, 170),
    "divider-upper-rail": (775, 170, 897, 350),
    "divider-center-ornament": (740, 350, 932, 590),
    "divider-lower-rail": (775, 590, 897, 770),
    "divider-bottom": (760, 770, 912, 941),
}

CONTENT_WELLS_TARGET = {
    "equipment": (132, 132, 895, 681),
    "vault": (1040, 132, 1803, 681),
}


def pale(rgb):
    r, g, b = rgb
    return min(r, g, b) > 190 and max(r, g, b) - min(r, g, b) < 25


def transparent_source():
    source = Image.open(SOURCE).convert("RGB")
    w, h = source.size
    px = source.load()
    seen = bytearray(w * h)
    q = deque()
    for x in range(w):
        if pale(px[x, 0]): q.append((x, 0))
        if pale(px[x, h - 1]): q.append((x, h - 1))
    for y in range(h):
        if pale(px[0, y]): q.append((0, y))
        if pale(px[w - 1, y]): q.append((w - 1, y))
    while q:
        x, y = q.popleft()
        i = y * w + x
        if seen[i] or not pale(px[x, y]):
            continue
        seen[i] = 1
        if x: q.append((x - 1, y))
        if x + 1 < w: q.append((x + 1, y))
        if y: q.append((x, y - 1))
        if y + 1 < h: q.append((x, y + 1))

    rgba = source.convert("RGBA")
    alpha = Image.new("L", (w, h), 255)
    ap = alpha.load()
    for y in range(h):
        for x in range(w):
            if seen[y * w + x]: ap[x, y] = 0
    for box in CONTENT_WELLS_SOURCE.values():
        ImageDraw.Draw(alpha).rectangle(box, fill=0)
    rgba.putalpha(alpha)
    rgba.save(SOURCE_MASTER)
    return rgba


def export_slices(source_master):
    SLICES.mkdir(exist_ok=True)
    pieces = {}
    for name, box in SLICE_BOXES.items():
        piece = source_master.crop(box)
        piece.save(SLICES / f"{name}.png")
        pieces[name] = piece
    return pieces


def resize(piece, size):
    return piece.resize(size, Image.Resampling.LANCZOS)


def build_target(p):
    W, H = TARGET_SIZE
    out = Image.new("RGBA", TARGET_SIZE, (0, 0, 0, 0))

    # Fixed outer corners.
    out.alpha_composite(p["outer-top-left"], (0, 0))
    out.alpha_composite(p["outer-top-right"], (W - p["outer-top-right"].width, 0))
    out.alpha_composite(p["outer-bottom-left"], (0, H - p["outer-bottom-left"].height))
    out.alpha_composite(p["outer-bottom-right"], (W - p["outer-bottom-right"].width, H - p["outer-bottom-right"].height))

    # Stretch only the intentionally quiet perimeter rails.
    top_h = p["outer-top-edge"].height
    bottom_h = p["outer-bottom-edge"].height
    out.alpha_composite(resize(p["outer-top-edge"], (W - 300, top_h)), (150, 20))
    out.alpha_composite(resize(p["outer-bottom-edge"], (W - 300, bottom_h)), (150, H - 130))
    side_h = H - 300
    out.alpha_composite(resize(p["outer-left-edge"], (150, side_h)), (0, 150))
    out.alpha_composite(resize(p["outer-right-edge"], (150, side_h)), (W - 150, 150))

    # Five-piece divider: the large runic medallion is fixed and never stretched.
    top = p["divider-top"]
    bottom = p["divider-bottom"]
    center = p["divider-center-ornament"]
    rail_w = p["divider-upper-rail"].width
    divider_x = (W - top.width) // 2
    center_x = (W - center.width) // 2
    center_y = (H - center.height) // 2
    out.alpha_composite(top, (divider_x, 0))
    out.alpha_composite(bottom, (divider_x, H - bottom.height))
    out.alpha_composite(center, (center_x, center_y))

    upper_y = top.height
    upper_h = max(1, center_y - upper_y)
    lower_y = center_y + center.height
    lower_h = max(1, H - bottom.height - lower_y)
    rail_x = (W - rail_w) // 2
    out.alpha_composite(resize(p["divider-upper-rail"], (rail_w, upper_h)), (rail_x, upper_y))
    out.alpha_composite(resize(p["divider-lower-rail"], (rail_w, lower_h)), (rail_x, lower_y))

    out.save(MASTER)
    out.resize((1284, 540), Image.Resampling.LANCZOS).save(STAGE)
    return out


def build_guide(master):
    guide = master.copy()
    d = ImageDraw.Draw(guide)
    W, H = TARGET_SIZE
    regions = {
        "outer-top-left": (0, 0, 150, 150),
        "outer-top-edge": (150, 20, W - 150, 130),
        "outer-top-right": (W - 150, 0, W, 150),
        "outer-left-edge": (0, 150, 150, H - 150),
        "outer-right-edge": (W - 150, 150, W, H - 150),
        "outer-bottom-left": (0, H - 150, 150, H),
        "outer-bottom-edge": (150, H - 130, W - 150, H - 20),
        "outer-bottom-right": (W - 150, H - 150, W, H),
        "divider-fixed-zone": ((W - 192)//2, 0, (W + 192)//2, H),
    }
    colors = [(255, 92, 72, 255), (78, 205, 255, 255), (255, 210, 73, 255)]
    for i, (name, box) in enumerate(regions.items()):
        color = colors[i % len(colors)]
        d.rectangle(box, outline=color, width=3)
        d.text((box[0] + 6, box[1] + 6), name, fill=color)
    for name, box in CONTENT_WELLS_TARGET.items():
        d.rectangle(box, outline=(93, 255, 137, 255), width=3)
        d.text((box[0] + 8, box[1] + 8), f"content: {name}", fill=(93, 255, 137, 255))
    guide.save(ROOT / "runeforge-strongbox-slice-guide.png")


def build_preview(master):
    bg = Image.new("RGBA", master.size, (12, 13, 17, 255))
    d = ImageDraw.Draw(bg)
    for y in range(0, master.height, 32):
        for x in range(0, master.width, 32):
            shade = 27 if ((x // 32) + (y // 32)) % 2 else 20
            d.rectangle((x, y, x + 31, y + 31), fill=(shade, shade + 1, shade + 3, 255))
    bg.alpha_composite(master)
    bg.resize((1284, 540), Image.Resampling.LANCZOS).convert("RGB").save(
        ROOT / "runeforge-strongbox-alpha-preview.jpg", quality=94
    )


if __name__ == "__main__":
    source_master = transparent_source()
    pieces = export_slices(source_master)
    master = build_target(pieces)
    build_guide(master)
    build_preview(master)
    print(f"Built Runeforge package: {len(SLICE_BOXES)} slices, two masters, guide, and alpha preview")
