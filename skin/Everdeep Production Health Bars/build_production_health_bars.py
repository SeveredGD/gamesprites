from __future__ import annotations

import json
from pathlib import Path
from shutil import copy2

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SOURCE_ROOT = Path(r"C:\Users\garre\Downloads\Everdeep Health Bar Frame Mockups\revisions")

BARS = [
    {
        "id": "hero-argent-thread",
        "role": "hero",
        "name": "Argent Thread",
        "source": SOURCE_ROOT / "hero" / "03-argent-thread.png",
        "inner": (26, 28, 489, 42),
        "fill_sample": (60, 28, 200, 42),
        "track_sample": (390, 28, 470, 42),
        "source_fill_end": 350,
        "leading_width": 2,
        "rail_sample_x": 320,
        "center_ornament": (241, 10, 272, 31),
    },
    {
        "id": "enemy-fang-clasp",
        "role": "enemy",
        "name": "Fang Clasp",
        "source": SOURCE_ROOT / "enemy-selected" / "02-fang-clasp.png",
        "inner": (24, 11, 361, 28),
        "fill_sample": (52, 11, 180, 28),
        "track_sample": (300, 11, 350, 28),
        "source_fill_end": 253,
        "leading_width": 2,
        "rail_sample_x": 300,
    },
    {
        "id": "boss-ossuary-reliquary",
        "role": "boss",
        "name": "Ossuary Reliquary",
        "source": SOURCE_ROOT / "boss" / "01-ossuary-reliquary.png",
        "inner": (154, 49, 744, 90),
        "fill_sample": (200, 52, 390, 87),
        "track_sample": (707, 52, 739, 87),
        "source_fill_end": 699,
        "leading_width": 3,
        "rail_sample_x": 600,
        "center_ornament": (413, 18, 484, 106),
        "cleanup": "boss",
    },
]


def repeat_mirrored(sample: Image.Image, width: int, height: int) -> Image.Image:
    sample = sample.convert("RGBA").resize((sample.width, height), Image.Resampling.LANCZOS)
    pair = Image.new("RGBA", (sample.width * 2, height))
    pair.alpha_composite(sample)
    pair.alpha_composite(sample.transpose(Image.Transpose.FLIP_LEFT_RIGHT), (sample.width, 0))
    output = Image.new("RGBA", (width, height))
    for x in range(0, width, pair.width):
        output.alpha_composite(pair, (x, 0))
    return output.crop((0, 0, width, height))


def clean_source(source: Image.Image, kind: str | None) -> Image.Image:
    source = source.convert("RGBA")
    if kind != "boss":
        return source
    # Remove the generated matte/noise while retaining the connected bar,
    # center crest, and ornate end caps.
    keep = Image.new("L", source.size, 0)
    draw = ImageDraw.Draw(keep)
    # Tight silhouettes avoid retaining the checker/matte rectangles around
    # the irregular caps and central crest.
    draw.rectangle((145, 34, 750, 107), fill=255)
    draw.polygon(((67, 70), (92, 42), (115, 27), (168, 34), (168, 106), (115, 114), (92, 96)), fill=255)
    draw.polygon(((828, 70), (803, 42), (780, 27), (727, 34), (727, 106), (780, 114), (803, 96)), fill=255)
    draw.polygon(((412, 58), (426, 32), (448, 18), (471, 32), (484, 58), (484, 101), (412, 101)), fill=255)
    alpha = source.getchannel("A")
    source.putalpha(Image.composite(alpha, Image.new("L", source.size, 0), keep))
    cleaned = []
    for red, green, blue, alpha_value in source.getdata():
        if min(red, green, blue) > 242 and max(red, green, blue) - min(red, green, blue) < 12:
            alpha_value = 0
        cleaned.append((red, green, blue, alpha_value))
    source.putdata(cleaned)
    return source


def make_layers(config: dict) -> dict:
    output = ROOT / config["id"]
    layers = output / "layers"
    slices = output / "slices"
    previews = output / "previews"
    for folder in (layers, slices, previews):
        folder.mkdir(parents=True, exist_ok=True)

    source = clean_source(Image.open(config["source"]), config.get("cleanup"))
    width, height = source.size
    x0, y0, x1, y1 = config["inner"]
    inner_width, inner_height = x1 - x0, y1 - y0

    bezel = source.copy()
    bezel.paste((0, 0, 0, 0), (x0, y0, x1, y1))

    stretchable_bezel = bezel.copy()
    center_info = None
    if "center_ornament" in config:
        ox0, oy0, ox1, oy1 = config["center_ornament"]
        center = bezel.crop((ox0, oy0, ox1, oy1))
        center.save(slices / "center-ornament.png", optimize=True)
        rail_column = bezel.crop((config["rail_sample_x"], 0, config["rail_sample_x"] + 1, height))
        for x in range(ox0, ox1):
            stretchable_bezel.paste(rail_column, (x, 0))
        stretchable_bezel.paste((0, 0, 0, 0), (x0, y0, x1, y1))
        center_info = {
            "file": "slices/center-ornament.png",
            "width": ox1 - ox0,
            "height": oy1 - oy0,
            "anchor": "top-center",
            "sourceOffsetY": oy0,
        }

    fill_strip = repeat_mirrored(source.crop(config["fill_sample"]), inner_width, inner_height)
    track_strip = repeat_mirrored(source.crop(config["track_sample"]), inner_width, inner_height)
    fill = Image.new("RGBA", source.size)
    track = Image.new("RGBA", source.size)
    fill.alpha_composite(fill_strip, (x0, y0))
    track.alpha_composite(track_strip, (x0, y0))
    empty = Image.alpha_composite(track, bezel)
    full = Image.alpha_composite(Image.alpha_composite(track, fill), bezel)

    leading_width = config["leading_width"]
    leading = source.crop((config["source_fill_end"] - leading_width, y0, config["source_fill_end"], y1))

    source.save(output / "selected-source.png", optimize=True)
    bezel.save(layers / "bezel.png", optimize=True)
    stretchable_bezel.save(layers / "bezel-stretchable.png", optimize=True)
    track.save(layers / "track.png", optimize=True)
    fill.save(layers / "fill.png", optimize=True)
    track_strip.crop((0, 0, min(32, inner_width), inner_height)).save(layers / "track-tile.png", optimize=True)
    fill_strip.crop((0, 0, min(32, inner_width), inner_height)).save(layers / "fill-tile.png", optimize=True)
    leading.save(layers / "fill-leading-edge.png", optimize=True)
    empty.save(layers / "empty-composite.png", optimize=True)
    full.save(layers / "full-composite.png", optimize=True)

    left_margin, right_margin = x0, width - x1
    clean_x = config["rail_sample_x"]
    stretchable_bezel.crop((0, 0, left_margin, height)).save(slices / "bezel-left.png", optimize=True)
    stretchable_bezel.crop((clean_x, 0, clean_x + 1, height)).save(slices / "bezel-center-1px.png", optimize=True)
    stretchable_bezel.crop((width - right_margin, 0, width, height)).save(slices / "bezel-right.png", optimize=True)

    for percent in (0, 25, 50, 75, 100):
        composed = track.copy()
        fill_width = round(inner_width * percent / 100)
        if fill_width:
            composed.alpha_composite(fill.crop((x0, y0, x0 + fill_width, y1)), (x0, y0))
            if percent < 100:
                edge_x = max(x0, min(x1 - leading_width, x0 + fill_width - leading_width))
                composed.alpha_composite(leading, (edge_x, y0))
        Image.alpha_composite(composed, bezel).save(previews / f"{percent:03d}.png", optimize=True)

    manifest = {
        "id": config["id"],
        "role": config["role"],
        "name": config["name"],
        "version": 1,
        "size": {"width": width, "height": height},
        "interior": {"x": x0, "y": y0, "width": inner_width, "height": inner_height},
        "nineSlice": {"left": left_margin, "right": right_margin, "top": y0, "bottom": height - y1},
        "layers": {
            "bezel": "layers/bezel.png",
            "stretchableBezel": "layers/bezel-stretchable.png",
            "track": "layers/track.png",
            "fill": "layers/fill.png",
            "trackTile": "layers/track-tile.png",
            "fillTile": "layers/fill-tile.png",
            "fillLeadingEdge": "layers/fill-leading-edge.png",
            "emptyComposite": "layers/empty-composite.png",
            "fullComposite": "layers/full-composite.png",
        },
        "slices": {
            "left": "slices/bezel-left.png",
            "center": "slices/bezel-center-1px.png",
            "right": "slices/bezel-right.png",
        },
        "centerOrnament": center_info,
        "dynamicFill": {
            "clipOriginX": x0,
            "clipOriginY": y0,
            "clipWidthAt100": inner_width,
            "clipHeight": inner_height,
            "formula": "round(interior.width * clamp(value, 0, 1))",
        },
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def build_contact(manifests: list[dict]) -> None:
    title = ImageFont.truetype(r"C:\Windows\Fonts\georgiab.ttf", 22)
    body = ImageFont.truetype(r"C:\Windows\Fonts\georgia.ttf", 15)
    sheet = Image.new("RGB", (1280, 620), (8, 10, 13))
    draw = ImageDraw.Draw(sheet)
    draw.text((24, 18), "EVERDEEP — PRODUCTION HEALTH BARS", fill=(219, 209, 184), font=title)
    draw.text((24, 50), "0 / 25 / 50 / 75 / 100 percent — true dynamic-layer previews", fill=(125, 133, 143), font=body)
    y = 88
    for manifest in manifests:
        draw.text((24, y + 14), f"{manifest['role'].upper()} — {manifest['name']}", fill=(199, 201, 204), font=body)
        x = 235
        for percent in (0, 25, 50, 75, 100):
            image = Image.open(ROOT / manifest["id"] / "previews" / f"{percent:03d}.png").convert("RGBA")
            image.thumbnail((195, 128), Image.Resampling.LANCZOS)
            sheet.paste(image, (x, y), image)
            x += 202
        y += max(120, manifest["size"]["height"] + 34)
    sheet.save(ROOT / "00-production-health-bars-preview.jpg", quality=95, subsampling=0)


def build_demo(manifests: list[dict]) -> None:
    cards = []
    for manifest in manifests:
        interior = manifest["interior"]
        cards.append(f'''<section><h2>{manifest["role"].title()} — {manifest["name"]}</h2>
<div class="bar" style="--w:{manifest['size']['width']}px;--h:{manifest['size']['height']}px;--ix:{interior['x']}px;--iy:{interior['y']}px;--iw:{interior['width']}px;--ih:{interior['height']}px">
<img src="{manifest['id']}/layers/track.png"><div class="clip"><img src="{manifest['id']}/layers/fill.png"></div><img src="{manifest['id']}/layers/bezel.png"></div>
<label><input type="range" min="0" max="100" value="65"><output>65%</output></label></section>''')
    html = '''<!doctype html><meta charset="utf-8"><title>Everdeep health bar test</title><style>
body{margin:0;padding:28px;background:#080a0d;color:#d8cbaa;font:16px Georgia,serif}main{max-width:1000px;margin:auto}section{padding:18px;margin:16px 0;border:1px solid #554f46;background:#0e0d0c;overflow:auto}h2{font-size:18px}.bar{position:relative;width:var(--w);height:var(--h)}.bar>img{position:absolute;inset:0}.clip{position:absolute;left:var(--ix);top:var(--iy);height:var(--ih);overflow:hidden}.clip img{position:absolute;left:calc(-1 * var(--ix));top:calc(-1 * var(--iy));max-width:none}.bar img{image-rendering:pixelated}label{display:flex;gap:12px;margin-top:12px}input{width:420px}</style><main><h1>Everdeep Dynamic Health Bars</h1>''' + "\n".join(cards) + '''</main><script>document.querySelectorAll('section').forEach(s=>{const i=s.querySelector('input'),o=s.querySelector('output'),c=s.querySelector('.clip'),b=s.querySelector('.bar');function u(){c.style.width=Math.round(parseFloat(getComputedStyle(b).getPropertyValue('--iw'))*i.value/100)+'px';o.value=i.value+'%'}i.oninput=u;u()})</script>'''
    (ROOT / "dynamic-health-bars-demo.html").write_text(html, encoding="utf-8")


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    sources = ROOT / "selected-sources"
    sources.mkdir(exist_ok=True)
    for config in BARS:
        copy2(config["source"], sources / f"{config['id']}.png")
    manifests = [make_layers(config) for config in BARS]
    build_contact(manifests)
    build_demo(manifests)
    (ROOT / "health-bars-manifest.json").write_text(json.dumps({"version": 1, "bars": manifests}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
