from pathlib import Path
import json

from PIL import Image


root = Path(__file__).resolve().parent
manifest = json.loads((root / "package-manifest.json").read_text(encoding="utf-8"))
errors = []

for entry in manifest["productionSheets"]:
    for key in ("image", "json", "names"):
        if not (root / entry[key]).is_file():
            errors.append(f"missing {entry[key]}")
    image_path = root / entry["image"]
    json_path = root / entry["json"]
    if image_path.is_file() and json_path.is_file():
        metadata = json.loads(json_path.read_text(encoding="utf-8"))
        image = Image.open(image_path)
        expected = (metadata["sheet"]["imageWidth"], metadata["sheet"]["imageHeight"])
        if image.size != expected:
            errors.append(f"size {entry['image']} {image.size} != {expected}")
        if image.mode != "RGBA":
            errors.append(f"mode {entry['image']} {image.mode}")

spliced = root / "ultra rares" / "spliced icons"
spliced_counts = {
    name: len(list((spliced / name).rglob("*.png")))
    for name in ("v1-detailed", "v2-simplified")
}
ultra_manifest = json.loads(
    (spliced / "ultra-rare-splice-manifest.json").read_text(encoding="utf-8")
)
preview_paths = list((root / "production sheets").rglob("*-32px-preview.png"))
if preview_paths:
    errors.extend(f"shipping preview {path.relative_to(root)}" for path in preview_paths)
file_count = sum(1 for path in root.rglob("*") if path.is_file())
byte_count = sum(path.stat().st_size for path in root.rglob("*") if path.is_file())

print(f"production_sheets={len(manifest['productionSheets'])}")
print(f"production_previews={len(preview_paths)}")
print(f"spliced_png={spliced_counts} total={sum(spliced_counts.values())}")
print(f"ultra_manifest_items={len(ultra_manifest['items'])}")
print(f"package_files={file_count}")
print(f"package_bytes={byte_count}")
print(f"errors={len(errors)}")
for error in errors:
    print(error)

raise SystemExit(1 if errors else 0)
