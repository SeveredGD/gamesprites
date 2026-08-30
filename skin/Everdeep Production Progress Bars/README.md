# Everdeep production progress bars — corrected cut

This folder replaces the earlier production cut. The old folder and ZIP were removed to the Recycle Bin.

Included bars:

- Compact Ossuary Hairline — 384×12
- Compact Frost Needle — 384×12
- Ossuary Rivet — 384×24
- Frost Reliquary — 384×24

Each bar contains:

- `layers/bezel.png` — transparent silver frame overlay
- `layers/track.png` — empty track constrained to the interior rectangle
- `layers/fill.png` — seamless full-width fill constrained to the interior rectangle
- repeatable track/fill tiles and optional leading edge
- empty and full composites
- left, one-pixel center, and right bezel slices
- `manifest.json` with dimensions, interior clipping rectangle, and 9-slice margins
- 0%, 25%, 50%, 75%, and 100% validation previews

The corrected large-bar interior is rows 5–18. This removes the colored antialias/highlight pixels that leaked above and below the previous rows 7–16 mask and falsely made the final quarter of the frame appear incomplete.

The Frost bezels additionally rebuild their stretchable upper and lower center rails from a clean empty-track column and remove low-opacity neutral checker artifacts. Their original endcaps remain unchanged.

Open `dynamic-bars-demo.html` for live sliders. Runtime order is track, clipped fill, then bezel. Use `round(interior.width * clamp(value, 0, 1))` for the fill width.
