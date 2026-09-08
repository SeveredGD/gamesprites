# Mode icons

Approved first column: A1 Normal, B1 Desolation, C1 Everdeep from mode-icons-9-v2-magenta.png.

Transparent RGBA icons: 32, 48, 64 and 128 pixels. Source-resolution crops retained. Use 64px image at 32 CSS pixels for high-density screens. Padding is approximately 12.5% on each edge; proportions preserved. Intentional dark doorway and abyss interiors remain opaque.

mode-icons-atlas-64.png and mode-icons.json form a Phaser JSON hash atlas. Frame IDs: mode-normal, mode-desolation, mode-everdeep. These are mode icons, separate from the Normal/Nightmare/Hell difficulty skulls.

Validated nonempty alpha, padding and light/dark previews at 32/64/128px. Extraction uses existing build_sheet.py smooth chroma-removal helper. Reproducible script: ../prepare_modes.py. Original review master unchanged.
