# Clockwork Tinker — usable nine-slice kit

## Included

- Six RGBA nine-slice PNGs: shop frame, improvement frame, normal/pressed buttons, normal/active tabs.
- Nine individual PNG regions per texture (54 cuts), for renderers that prefer separate sprites.
- Detached top clockwork crest and winding key. These must remain separate, fixed-size decorations.
- Seam-matched interior texture and a divider built from a repeated axle plus fixed gears.
- `tinker-clockwork.css`: ready-to-use DOM/CSS classes, matching Everdeep's HTML menu approach.
- `nine-slice.json`: exact source dimensions, source-pixel slice insets, display borders, minimum sizes.
- `preview.html`: offline-capable browser demonstration with width and height controls.
- `resize-check.jpg`: minimum-size and wide-frame inspection image.
- `tools/build.py`: reproducible extraction and slicing (Python, Pillow, NumPy). Requires the source atlas in the parent directory.

## Drop-in HTML example

Copy this directory's `assets/` and CSS into the game's asset directory, preserving relative paths. Do not replace global game skin variables: apply these classes to the Tinker only.

```html
<link rel="stylesheet" href="tinker-clockwork.css">
<section class="tinker-clockwork-panel">
  <span class="tinker-clockwork-crest" aria-hidden="true"></span>
  <h2>The Traveling Tinker</h2>
  <!-- Existing shop content and existing event handlers go here. -->
  <button class="tinker-clockwork-tab" aria-selected="true">Shop</button>
  <button class="tinker-clockwork-tab" aria-selected="false">Improve</button>
  <div class="tinker-clockwork-divider" aria-hidden="true"><span></span></div>
  <button class="tinker-clockwork-button">Buy supplies</button>
</section>
<section class="tinker-clockwork-panel tinker-clockwork-panel--improvement">
  <span class="tinker-clockwork-key" aria-hidden="true"></span>
  <!-- Existing item preview and tinker action. -->
</section>
```

Keep `position:relative` and `isolation:isolate` on the panel. Its pseudo-elements render the inset background and nine-slice border behind content. Supply no `fill` on panel border images: the center is transparent and a separately tiled surface provides the interior. Buttons/tabs use `fill` intentionally.

Existing global button skin rules may need Tinker-scoped overrides if they use `!important`; this package has not been inserted into the live game. Existing element IDs and gameplay handlers should be preserved by the implementation agent.

## Sizing contract

| Texture | Source slice top/right/bottom/left | Display border top/right/bottom/left | Minimum outer size |
|---|---|---|---|
| shop-frame | 145 / 156 / 155 / 155 | 72.5 / 78 / 77.5 / 77.5 px | 360 × 320 px |
| improvement-frame | 112 / 110 / 112 / 110 | 56 / 55 / 56 / 55 px | 260 × 260 px |
| button-normal / pressed | 35 / 110 / 35 / 110 | 17.5 / 55 / 17.5 / 55 px | 160 × **65** px |
| tab-normal / active | 35 / 110 / 35 / 110 | 17.5 / 55 / 17.5 / 55 px | 160 × **67** px |

All source slices use the unscaled PNG coordinates. Insets are not percentages. Do not change source slices when changing display scale.

- Panels support changing width and height independently. Corners remain fixed at the chosen artwork scale.
- Controls support changing width. Keep the supplied heights; arbitrary height stretching would elongate gear endcaps in the vertical middle slice. For smaller controls, uniformly scale the height AND all four display border widths.
- At viewport widths below 400px the supplied CSS reduces the main panel's whole border system and crest to 75% of desktop display size, allowing a 280px minimum main panel. Content still determines actual height.
- The improvement panel key extends 25px beyond the right edge. Reserve this space or omit the overlay on narrow layouts, as the preview does.
- Minimum dimensions are artwork constraints, not guarantees that every text label fits. Allow content-driven height and stack controls when needed.
- Keep crest centered at the top. Never stretch it with the top rail.

## Validation performed

All six textures verified RGBA with transparent pixels, positive center regions, and valid slice coordinates. Inspected raster reconstructions at narrow and wide sizes and the actual CSS browser preview. The preview loads local assets without remote dependencies. Buttons and tabs have equal-sized state canvases, preserving their layout when pressed or selected.

Exterior light backgrounds were removed; panel interiors were separated from borders to avoid stretching texture. Some source shading was reduced during extraction. All original generated artwork remains untouched in the parent folder.

These are ready for integration; no gameplay files, Steam assets, or GitHub files were modified.

## Revision 2 — control alpha cleanup
Removed enclosed white pipe-loop backgrounds and neutral exterior fringes from all four control states. Rebuilt their 36 individual slices. Panel artwork and slice coordinates remain unchanged. See control-alpha-check.png for dark-background inspection.


## Revision 3 — Brass & Iron layout
Open brass-iron-preview.html for the approved Brass & Iron layout with the cleaned clockwork skin. brass-iron-clockwork.css applies the skin to its existing tk-* classes. Shop, improvements, equipment/vault selection, and sample actions remain interactive. This is a standalone design integration using demonstration data, not a modification of gameplay or saves. Use this page as the layout reference when binding existing Tinker game handlers.


## Revision 4 — Pets tab
Added Clockwork Menagerie as a third tab. Uses the live catalogue: Clicks, Buckle, Scraps, Kettle, Clicker, Socket and Coil, with existing prices, effects and unlock requirements. Progress and purchases are local preview state. pets-preview.js and pets-layout.css are required alongside the layout. Verified tab rendering and sample purchase ownership/gold update.

