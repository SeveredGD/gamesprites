from __future__ import annotations

import json
from pathlib import Path
from shutil import copy2

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"C:\Users\garre\Downloads\Everdeep Production Progress Bars")
GENERATED = Path(r"C:\Users\garre\.codex\generated_images\01a04e1b-9896-7dc3-97ba-87796fb3110d")

BARS = [
    {
        "id": "compact-ossuary-hairline",
        "name": "Compact Ossuary Hairline",
        "source": Path(r"C:\Users\garre\Downloads\Everdeep Compact Mastery Bars\transparent-working-384x12\01-ossuary-hairline.png"),
        "ai_empty": GENERATED / "exec-76c55409-1024-4bf2-ba8e-d9235380b9a3.png",
        "inner": (9, 3, 375, 9),
        "fill_sample": (40, 3, 120, 9),
        "track_sample": (310, 3, 360, 9),
        "source_fill_end": 286,
        "leading_width": 2,
    },
    {
        "id": "compact-frost-needle",
        "name": "Compact Frost Needle",
        "source": Path(r"C:\Users\garre\Downloads\Everdeep Compact Mastery Bars\transparent-working-384x12\02-frost-needle.png"),
        "ai_empty": GENERATED / "exec-55278472-ed47-4d3d-a297-33834c48ec5f.png",
        "inner": (14, 3, 370, 9),
        "fill_sample": (42, 3, 180, 9),
        "track_sample": (280, 3, 340, 9),
        "source_fill_end": 232,
        "leading_width": 2,
        "clean_rail_sample_x": 300,
    },
    {
        "id": "ossuary-rivet",
        "name": "Ossuary Rivet",
        "source": Path(r"C:\Users\garre\Downloads\Everdeep Thin Bezel Bars\transparent-working-384x24\05-ossuary-rivet.png"),
        "ai_empty": GENERATED / "exec-83788061-e86c-466c-ac83-0e4728ad2c3b.png",
        "inner": (30, 5, 354, 19),
        "fill_sample": (54, 5, 220, 19),
        "track_sample": (312, 5, 344, 19),
        "source_fill_end": 290,
        "leading_width": 2,
    },
    {
        "id": "frost-reliquary",
        "name": "Frost Reliquary",
        "source": Path(r"C:\Users\garre\Downloads\Everdeep Thin Bezel Bars\transparent-working-384x24\06-frost-reliquary.png"),
        "ai_empty": GENERATED / "exec-5a61d536-31aa-4d2f-9db7-6bd4c1e0b904.png",
        "inner": (27, 5, 358, 19),
        "fill_sample": (50, 5, 175, 19),
        "track_sample": (260, 5, 330, 19),
        "source_fill_end": 211,
        "leading_width": 2,
        "clean_rail_sample_x": 300,
    },
]


def repeat_mirrored(sample: Image.Image, width: int) -> Image.Image:
    sample = sample.convert("RGBA")
    pair = Image.new("RGBA", (sample.width * 2, sample.height))
    pair.alpha_composite(sample, (0, 0))
    pair.alpha_composite(sample.transpose(Image.Transpose.FLIP_LEFT_RIGHT), (sample.width, 0))
    output = Image.new("RGBA", (width, sample.height))
    for x in range(0, width, pair.width):
        output.alpha_composite(pair, (x, 0))
    return output.crop((0, 0, width, sample.height))


def remove_checker_halo(image: Image.Image) -> Image.Image:
    """Remove low-alpha neutral whites left by the generated checker background."""
    cleaned = []
    for red, green, blue, alpha in image.convert("RGBA").getdata():
        light = max(red, green, blue)
        chroma = light - min(red, green, blue)
        if alpha < 16 or (alpha < 140 and light > 215 and chroma < 12):
            alpha = 0
        cleaned.append((red, green, blue, alpha))
    output = Image.new("RGBA", image.size)
    output.putdata(cleaned)
    return output


def normalize_reference(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    rgba = image.convert("RGBA")
    if image.mode != "RGBA" or rgba.getchannel("A").getextrema()[0] != 0:
        cleaned = []
        for red, green, blue, _ in rgba.getdata():
            # Generated empty references use black exterior; remove only connected-looking near-black.
            light = max(red, green, blue)
            alpha = 0 if light < 5 else min(255, max(0, (light - 3) * 32))
            cleaned.append((red, green, blue, alpha))
        rgba.putdata(cleaned)
    box = rgba.getchannel("A").point(lambda value: 255 if value > 32 else 0).getbbox()
    if box:
        rgba = rgba.crop(box)
    return rgba.resize(size, Image.Resampling.LANCZOS)


def make_layers(config: dict) -> dict:
    bar_dir = ROOT / config["id"]
    layers_dir = bar_dir / "layers"
    slices_dir = bar_dir / "slices"
    previews_dir = bar_dir / "previews"
    for directory in (layers_dir, slices_dir, previews_dir):
        directory.mkdir(parents=True, exist_ok=True)

    source = Image.open(config["source"]).convert("RGBA")
    width, height = source.size
    x0, y0, x1, y1 = config["inner"]
    inner_width, inner_height = x1 - x0, y1 - y0

    bezel = source.copy()
    bezel.paste((0, 0, 0, 0), (x0, y0, x1, y1))
    if "clean_rail_sample_x" in config:
        # Frost sources retained uneven pale/checkerboard edge pixels. Replace only
        # the stretchable center rail with one clean empty-track column; preserve
        # both original endcaps, then reopen the exact transparent interior.
        sample_x = config["clean_rail_sample_x"]
        clean_column = source.crop((sample_x, 0, sample_x + 1, height))
        for rail_x in range(x0, x1):
            bezel.paste(clean_column, (rail_x, 0))
        bezel.paste((0, 0, 0, 0), (x0, y0, x1, y1))
        bezel = remove_checker_halo(bezel)

    fill_sample = source.crop(config["fill_sample"])
    track_sample = source.crop(config["track_sample"])
    fill_strip = repeat_mirrored(fill_sample, inner_width)
    track_strip = repeat_mirrored(track_sample, inner_width)

    track = Image.new("RGBA", source.size)
    fill = Image.new("RGBA", source.size)
    track.alpha_composite(track_strip, (x0, y0))
    fill.alpha_composite(fill_strip, (x0, y0))

    empty = Image.alpha_composite(track, bezel)
    full = Image.alpha_composite(track, fill)
    full = Image.alpha_composite(full, bezel)

    leading_width = config["leading_width"]
    boundary = config["source_fill_end"]
    leading = source.crop((boundary - leading_width, y0, boundary, y1))

    source.save(bar_dir / "selected-source.png", optimize=True)
    bezel.save(layers_dir / "bezel.png", optimize=True)
    track.save(layers_dir / "track.png", optimize=True)
    fill.save(layers_dir / "fill.png", optimize=True)
    track_strip.crop((0, 0, min(32, inner_width), inner_height)).save(layers_dir / "track-tile.png", optimize=True)
    fill_strip.crop((0, 0, min(32, inner_width), inner_height)).save(layers_dir / "fill-tile.png", optimize=True)
    leading.save(layers_dir / "fill-leading-edge.png", optimize=True)
    empty.save(layers_dir / "empty-composite.png", optimize=True)
    full.save(layers_dir / "full-composite.png", optimize=True)

    left_margin = x0
    right_margin = width - x1
    center_x = max(left_margin, min(width - right_margin - 1, width // 2))
    bezel.crop((0, 0, left_margin, height)).save(slices_dir / "bezel-left.png", optimize=True)
    bezel.crop((center_x, 0, center_x + 1, height)).save(slices_dir / "bezel-center-1px.png", optimize=True)
    bezel.crop((width - right_margin, 0, width, height)).save(slices_dir / "bezel-right.png", optimize=True)

    for percent in (0, 25, 50, 75, 100):
        composed = track.copy()
        fill_width = round(inner_width * percent / 100)
        if fill_width:
            clipped = fill.crop((x0, y0, x0 + fill_width, y1))
            composed.alpha_composite(clipped, (x0, y0))
            if 0 < percent < 100:
                edge_x = min(x1 - leading_width, x0 + fill_width - leading_width)
                composed.alpha_composite(leading, (edge_x, y0))
        composed = Image.alpha_composite(composed, bezel)
        composed.save(previews_dir / f"{percent:03d}.png", optimize=True)

    ai_empty = normalize_reference(Image.open(config["ai_empty"]), source.size)
    ai_empty.save(bar_dir / "ai-empty-style-reference.png", optimize=True)

    manifest = {
        "id": config["id"],
        "name": config["name"],
        "version": 1,
        "size": {"width": width, "height": height},
        "interior": {"x": x0, "y": y0, "width": inner_width, "height": inner_height},
        "nineSlice": {
            "left": left_margin,
            "right": right_margin,
            "top": y0,
            "bottom": height - y1,
        },
        "layers": {
            "bezel": "layers/bezel.png",
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
        "dynamicFill": {
            "clipOriginX": x0,
            "clipOriginY": y0,
            "clipWidthAt100": inner_width,
            "clipHeight": inner_height,
            "formula": "round(interior.width * clamp(value, 0, 1))",
        },
    }
    (bar_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return {"config": config, "manifest": manifest}


def build_contact(results: list[dict]):
    try:
        title_font = ImageFont.truetype(r"C:\Windows\Fonts\georgiab.ttf", 22)
        label_font = ImageFont.truetype(r"C:\Windows\Fonts\georgia.ttf", 15)
    except OSError:
        title_font = label_font = ImageFont.load_default()
    sheet = Image.new("RGB", (1000, 445), (8, 10, 13))
    draw = ImageDraw.Draw(sheet)
    draw.text((24, 17), "EVERDEEP — PRODUCTION DYNAMIC BARS", fill=(219, 209, 184), font=title_font)
    draw.text((24, 49), "0 / 25 / 50 / 75 / 100 percent — shown at 2×", fill=(125, 133, 143), font=label_font)
    y = 84
    for result in results:
        config, manifest = result["config"], result["manifest"]
        draw.text((24, y + 10), config["name"], fill=(199, 201, 204), font=label_font)
        x = 200
        for percent in (0, 25, 50, 75, 100):
            preview = Image.open(ROOT / config["id"] / "previews" / f"{percent:03d}.png").convert("RGBA")
            scale = 2
            rendered = preview.resize((preview.width * scale, preview.height * scale), Image.Resampling.NEAREST)
            thumb_width = 145
            rendered.thumbnail((thumb_width, rendered.height), Image.Resampling.LANCZOS)
            sheet.paste(rendered, (x, y), rendered)
            x += 155
        y += 86
    sheet.save(ROOT / "00-production-bars-percentage-preview.jpg", quality=95, subsampling=0)


def build_demo(results: list[dict]):
    cards = []
    for index, result in enumerate(results):
        config, manifest = result["config"], result["manifest"]
        interior = manifest["interior"]
        cards.append(f'''<section class="card" data-value="{35 + index * 15}">
  <h2>{config["name"]}</h2>
  <div class="bar" style="--w:{manifest['size']['width']}px;--h:{manifest['size']['height']}px;--ix:{interior['x']}px;--iy:{interior['y']}px;--iw:{interior['width']}px;--ih:{interior['height']}px">
    <img class="track" src="{config['id']}/layers/track.png" alt="">
    <div class="fill-clip"><img class="fill" src="{config['id']}/layers/fill.png" alt=""></div>
    <img class="bezel" src="{config['id']}/layers/bezel.png" alt="">
  </div>
  <label><input type="range" min="0" max="100" value="{35 + index * 15}"> <output>{35 + index * 15}%</output></label>
</section>''')
    html = '''<!doctype html><meta charset="utf-8"><title>Everdeep dynamic progress bars</title>
<style>
body{margin:0;background:#090a0d;color:#d6c9aa;font:16px Georgia,serif;padding:32px}main{max-width:700px;margin:auto}.card{background:#0e0d0c;border:1px solid #605a50;padding:20px;margin:16px 0}h2{font-size:18px;margin:0 0 14px}.bar{position:relative;width:var(--w);height:var(--h);image-rendering:pixelated}.bar>img{position:absolute;inset:0;width:100%;height:100%}.fill-clip{position:absolute;left:var(--ix);top:var(--iy);height:var(--ih);overflow:hidden}.fill{position:absolute;left:calc(-1 * var(--ix));top:calc(-1 * var(--iy));width:var(--w);height:var(--h);max-width:none}.bezel{pointer-events:none}label{display:flex;gap:12px;align-items:center;margin-top:14px}input{width:384px}output{min-width:48px}
</style><main><h1>Everdeep Dynamic Bar Test</h1>''' + "\n".join(cards) + '''</main><script>
document.querySelectorAll('.card').forEach(card=>{const input=card.querySelector('input'),clip=card.querySelector('.fill-clip'),out=card.querySelector('output'),bar=card.querySelector('.bar');function update(){const iw=parseFloat(getComputedStyle(bar).getPropertyValue('--iw'));clip.style.width=Math.round(iw*input.value/100)+'px';out.value=input.value+'%'}input.addEventListener('input',update);update()})
</script>'''
    (ROOT / "dynamic-bars-demo.html").write_text(html, encoding="utf-8")


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    reference_dir = ROOT / "ai-empty-references-original"
    reference_dir.mkdir(exist_ok=True)
    for config in BARS:
        copy2(config["ai_empty"], reference_dir / f"{config['id']}.png")
    results = [make_layers(config) for config in BARS]
    build_contact(results)
    build_demo(results)


if __name__ == "__main__":
    main()
