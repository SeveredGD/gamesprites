# Everdeep Pro-UI skin — assets

The ornate metal-and-gold interface skin for Everdeep Idle. This folder holds the
**10 image pieces** the skin references; the CSS + toggle logic live inline in the game
HTML (in a block between `<!-- PRO-UI-SKIN:START -->` and `<!-- PRO-UI-SKIN:END -->`).

## What's here
| file | role |
|------|------|
| `btn_gold.png` | gold button border (9-slice) |
| `panel_gold/red/purple/blue.png` | popup frame variants (default / danger / arcane / info) |
| `divider_gold.png` | thin frame for icon/favorite skill pills |
| `reaper_barframe.png` | bronze bar frame (HP / rage / XP / mana troughs) |
| `reaper_fill_red/orange/blue.png` | vivid bar fills |

~412 KB total. Only the pieces actually used are included (the unused `fill_red` and
`reaper_fill_gold` were dropped). PNGs are already max-compressed — lossless re-encode
yields 0 bytes, so shrinking further would mean quality loss.

## How it's wired
- This folder must sit **next to the game HTML** — the skin loads pieces by the relative
  path `skin/NAME.png`, so `Everdeep_Idle_1_10_0.html` and `skin/` live side by side (and a
  mirror copy lives at `ei/www/skin/` for the Capacitor build).
- The skin is **on by default** and can be turned off from **Settings → Display → Interface
  skin** or the **character-select screen**. Off disables the injected `<style>`, reverting
  to the original flat UI. The choice persists in `localStorage.proUiSkin`.

## Regenerating
The inline block + these copies are produced from the source pieces in `rpg_gui/pieces/` by
`merge_skin.js` (which imports the shared template from `build_profork.js`). Re-running it
replaces the marked block in place in both HTML files and refreshes both `skin/` folders.
