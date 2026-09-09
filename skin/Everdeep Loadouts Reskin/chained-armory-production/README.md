# Chained Armory — Loadout skin 1

Nine assets in `assets/`, plus 63 individual nine-slice pieces in `slices/`. The frame, two tabs, two buttons and two row states have nine-slices; crest and suspension chain are independent decorations. `preview.html` demonstrates responsive sizing, tabs and an inner scrolling list. Game actions are placeholders.

## Use in the game

Keep `assets/` beside `loadout-skin.css`, or change CSS URLs to the final asset location. Copy the styling and retain the existing loadout event handlers, icons and text. The sample uses Active / Equip labels in build rows.

`skin.json` records exact texture sizes and SOURCE pixel insets. Insets are top/right/bottom/left:

| Asset | Insets |
|---|---|
| Modal frame | 155 / 155 / 180 / 155 |
| Tabs, silver and gold | 60 / 95 / 60 / 95 |
| Buttons, silver and gold | 35 / 35 / 35 / 35 |
| Rows, silver and gold | 22 / 30 / 22 / 30 |

The desktop CSS displays modal corners at 40% of source size; tabs, buttons and rows at 50%. Use fixed corner proportions and repeat middle frame edges to preserve the rail texture. Never stretch the entire frame image. For a custom nine-slice renderer, use the named pieces in the manifest; modal center is transparent. Tabs are best around 72–80px high with width adjusted independently; keep state destinations identical even when source sizes differ slightly.

Keep a charcoal background beneath the frame. Put scrolling/clipping only on the inner list, leaving crest and suspension chains outside that scroll container. Crest and chains must retain their aspect ratios. The suspension chain's top is intentionally open so it can continue beyond the panel. Use runtime text and existing game icons. Retain your existing scrollbar.

This is a blank asset adaptation of approved concept 1, not an exact pixel extraction of every original ornament. The built-in image-generation tool produced the blank frame/control sheet; `source/generation-prompt.txt` records its prompt. `source/approved-concept.png` is the visual reference and source of the row borders and chain. Row content was cleared; magenta was keyed from the generated sheet. Center rail medallions were removed to avoid stretching them. Original assets and the earlier production kit remain intact.

Validation: desktop and 390px mobile previews, tab switching, image loads and horizontal overflow checks. Screenshots are in `qa/`. Source masters are not meant to be uploaded as runtime textures.
