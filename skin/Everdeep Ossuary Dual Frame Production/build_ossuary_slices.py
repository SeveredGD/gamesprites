from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw
import numpy as np


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "ossuary-dual-frame-generated.png"
MASTER = ROOT / "ossuary-dual-frame-master-1935x813.png"
STAGE = ROOT / "ossuary-dual-frame-master-1284x540.png"
SLICES = ROOT / "slices"

# These are the two uninterrupted content wells in the generated 1935x813 master.
# They intentionally stop just inside the inner silver rails.
CONTENT_WELLS = {
    "equipment": (132, 88, 895, 719),
    "vault": (1038, 88, 1800, 719),
}

# Outer frame is an eight-piece stretch system; the divider is independently
# three-sliced so none of its fixed ossuary ornaments are ever stretched.
SLICE_BOXES = {
    "outer-top-left": (0, 0, 300, 180),
    "outer-top-edge": (350, 0, 650, 110),
    "outer-top-right": (1635, 0, 1935, 180),
    "outer-left-edge": (0, 230, 150, 530),
    "outer-right-edge": (1785, 230, 1935, 530),
    "outer-bottom-left": (0, 633, 300, 813),
    "outer-bottom-edge": (350, 703, 650, 813),
    "outer-bottom-right": (1635, 633, 1935, 813),
    "divider-top": (890, 0, 1045, 220),
    "divider-middle": (890, 250, 1045, 550),
    "divider-bottom": (890, 593, 1045, 813),
}


def remove_connected_black_background(rgb: np.ndarray, alpha: np.ndarray) -> None:
    """Remove only near-black neutral pixels connected to the canvas boundary."""
    high = rgb.max(axis=2)
    low = rgb.min(axis=2)
    candidate = (high <= 12) & ((high - low) <= 4)
    height, width = candidate.shape
    visited = np.zeros_like(candidate, dtype=bool)
    queue: deque[tuple[int, int]] = deque()

    for x in range(width):
        if candidate[0, x]:
            queue.append((x, 0))
        if candidate[height - 1, x]:
            queue.append((x, height - 1))
    for y in range(height):
        if candidate[y, 0]:
            queue.append((0, y))
        if candidate[y, width - 1]:
            queue.append((width - 1, y))

    while queue:
        x, y = queue.popleft()
        if visited[y, x] or not candidate[y, x]:
            continue
        visited[y, x] = True
        if x:
            queue.append((x - 1, y))
        if x + 1 < width:
            queue.append((x + 1, y))
        if y:
            queue.append((x, y - 1))
        if y + 1 < height:
            queue.append((x, y + 1))

    alpha[visited] = 0


def build_master() -> Image.Image:
    source = Image.open(SOURCE).convert("RGB")
    rgb = np.array(source)
    alpha = np.full(rgb.shape[:2], 255, dtype=np.uint8)
    remove_connected_black_background(rgb, alpha)

    for left, top, right, bottom in CONTENT_WELLS.values():
        alpha[top:bottom, left:right] = 0

    rgba = np.dstack((rgb, alpha))
    master = Image.fromarray(rgba, "RGBA")
    master.save(MASTER)
    master.resize((1284, 540), Image.Resampling.LANCZOS).save(STAGE)
    return master


def build_slices(master: Image.Image) -> None:
    SLICES.mkdir(exist_ok=True)
    for name, box in SLICE_BOXES.items():
        master.crop(box).save(SLICES / f"{name}.png")


def build_guide(master: Image.Image) -> None:
    guide = master.copy()
    draw = ImageDraw.Draw(guide)
    colors = [(255, 92, 72, 255), (78, 205, 255, 255), (255, 210, 73, 255)]
    for index, (name, box) in enumerate(SLICE_BOXES.items()):
        draw.rectangle(box, outline=colors[index % len(colors)], width=3)
        draw.text((box[0] + 7, box[1] + 7), name, fill=colors[index % len(colors)])
    for name, box in CONTENT_WELLS.items():
        draw.rectangle(box, outline=(93, 255, 137, 255), width=3)
        draw.text((box[0] + 8, box[1] + 8), f"content: {name}", fill=(93, 255, 137, 255))
    guide.save(ROOT / "ossuary-dual-frame-slice-guide.png")


def build_preview(master: Image.Image) -> None:
    preview = Image.new("RGBA", master.size, (12, 13, 17, 255))
    draw = ImageDraw.Draw(preview)
    tile = 32
    for y in range(0, master.height, tile):
        for x in range(0, master.width, tile):
            shade = 27 if ((x // tile) + (y // tile)) % 2 else 20
            draw.rectangle((x, y, x + tile, y + tile), fill=(shade, shade + 1, shade + 3, 255))
    preview.alpha_composite(master)
    preview.resize((1284, 540), Image.Resampling.LANCZOS).convert("RGB").save(
        ROOT / "ossuary-dual-frame-alpha-preview.jpg", quality=94
    )


if __name__ == "__main__":
    final_master = build_master()
    build_slices(final_master)
    build_guide(final_master)
    build_preview(final_master)
    print(f"Built {MASTER.name}, {STAGE.name}, {len(SLICE_BOXES)} slices, guide, and preview")
