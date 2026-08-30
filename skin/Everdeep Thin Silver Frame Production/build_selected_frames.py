from pathlib import Path
from PIL import Image, ImageDraw
import shutil

SOURCE = Path(r"C:\Users\garre\Downloads\Everdeep Thin Silver Frame Mockups\cropped-masters")
OUT = Path(r"C:\Users\garre\Downloads\Everdeep Thin Silver Frame Production")

FRAMES = {
    "02-runic-hairline": ("02-runic-hairline.png", (57, 67, 55, 67)),
    "03-thornwire": ("03-thornwire.png", (61, 61, 63, 59)),
    "05-moonsteel-stitch": ("05-moonsteel-stitch.png", (61, 61, 62, 63)),
}


def resize(piece, size):
    return piece.resize(size, Image.Resampling.NEAREST)


def slice_frame(image, slices, target):
    top, right, bottom, left = slices
    width, height = image.size
    boxes = {
        "top-left": (0, 0, left, top),
        "top-edge": (left, 0, width - right, top),
        "top-right": (width - right, 0, width, top),
        "left-edge": (0, top, left, height - bottom),
        "center": (left, top, width - right, height - bottom),
        "right-edge": (width - right, top, width, height - bottom),
        "bottom-left": (0, height - bottom, left, height),
        "bottom-edge": (left, height - bottom, width - right, height),
        "bottom-right": (width - right, height - bottom, width, height),
    }
    slices_dir = target / "slices"
    slices_dir.mkdir(parents=True, exist_ok=True)
    for name, box in boxes.items():
        if name == "center":
            piece = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
        else:
            piece = image.crop(box)
        piece.save(slices_dir / f"{name}.png", optimize=True)


def render_preview(image, slices, rail, size=(720, 180)):
    top, right, bottom, left = slices
    width, height = image.size
    source = {
        "tl": image.crop((0, 0, left, top)),
        "t": image.crop((left, 0, width - right, top)),
        "tr": image.crop((width - right, 0, width, top)),
        "l": image.crop((0, top, left, height - bottom)),
        "r": image.crop((width - right, top, width, height - bottom)),
        "bl": image.crop((0, height - bottom, left, height)),
        "b": image.crop((left, height - bottom, width - right, height)),
        "br": image.crop((width - right, height - bottom, width, height)),
    }
    w, h = size
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    out.alpha_composite(resize(source["tl"], (rail, rail)), (0, 0))
    out.alpha_composite(resize(source["t"], (w - rail * 2, rail)), (rail, 0))
    out.alpha_composite(resize(source["tr"], (rail, rail)), (w - rail, 0))
    out.alpha_composite(resize(source["l"], (rail, h - rail * 2)), (0, rail))
    out.alpha_composite(resize(source["r"], (rail, h - rail * 2)), (w - rail, rail))
    out.alpha_composite(resize(source["bl"], (rail, rail)), (0, h - rail))
    out.alpha_composite(resize(source["b"], (w - rail * 2, rail)), (rail, h - rail))
    out.alpha_composite(resize(source["br"], (rail, rail)), (w - rail, h - rail))
    return out


def on_dark(frame):
    preview = Image.new("RGBA", frame.size, (9, 10, 13, 255))
    draw = ImageDraw.Draw(preview)
    draw.rectangle((8, 8, frame.width - 9, frame.height - 9), fill=(15, 17, 22, 255))
    preview.alpha_composite(frame)
    return preview


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, (filename, slices) in FRAMES.items():
        target = OUT / slug
        target.mkdir(parents=True, exist_ok=True)
        image = Image.open(SOURCE / filename).convert("RGBA")
        image.save(target / "master.png", optimize=True)
        slice_frame(image, slices, target)
        for rail in (2, 3):
            frame = render_preview(image, slices, rail)
            frame.save(target / f"preview-{rail}px-transparent.png", optimize=True)
            on_dark(frame).convert("RGB").save(target / f"preview-{rail}px-on-dark.jpg", quality=92)
    print(f"Built {len(FRAMES)} selected frames in {OUT}")


if __name__ == "__main__":
    main()
