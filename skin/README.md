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
| `coin_gold.png` | gold coin icon — replaces the `⬡` glyph wherever gold is shown |

~413 KB total (11 files). Only the pieces actually used are included (the unused `fill_red`
and `reaper_fill_gold` were dropped). PNGs are already max-compressed — lossless re-encode
yields 0 bytes, so shrinking further would mean quality loss.

**Frame colours** are normally auto-picked from each popup's border colour, but three menus are
pinned explicitly in the skin: Skill Levels → `panel_blue`, Ascendancy → `panel_purple`,
Crafting → `panel_gold`.

## ClassicRPGUI_2 pieces — "Crimson Command" reskin (added 2026-07-30)

The **20 files** below come from the ClassicRPGUI_2 pack and belong to the **Crimson Command**
reskin (`Everdeep_Idle_Crimson_Command.html`), not to the Citadel skin above. Names do not
collide with any Citadel/Reaper piece. They are routed through the fork's `SKIN THEME REGISTRY`
CSS-variable block — to restyle, edit that block, not these filenames.

Audited 2026-07-30: these are exactly the files the fork references, all present and decoding.

| file | role (registry var) |
|------|---------------------|
| `BarBasic_Standart.png` | panel frame — combat zone, header, panes, dialogs (`--sk-frame`) |
| `BarBasic_Paper.png` | parchment fill — hero stat pane only, desktop (`--sk-parchment`) |
| `ButtonMediumDark/Red/DarkPressed.png` | button normal / hover / **pressed** (`--sk-btn-n/h/p`) |
| `ButtonMini_Gray.png` / `ButtonMini_Red.png` | neutral buttons + tab chips (`--sk-std-*`, `--sk-tab`) |
| `InventoryItemSlot_1.png` | inputs + Panel-card icon well (`--sk-slot`, `--sk-slotwell`) |
| `InventoryItemSlot_2.png` | Medium "forge tile" well (`--sk-tilewell`) |
| `SkillSlot_frame.png` | item-row steel ring, rarity hue-tinted (`--sk-item`) |
| `InventoryCostMiniBar2.png` | Panel vault-row frame (`--sk-rowframe`) |
| `TradeBar_Info.png` | Large "trade info" composed card (`--sk-cardlarge`) |
| `BarLittle_Description.png` | **Inked Panel** thin frame — replaced the pure-CSS walnut ridge (`--sk-thin`) |
| `Icon_Exit_t.png` | the ✕ close/discard icon (`--sk-xicon`, applied by `dressCloseIcons`) |
| `HealthMobBar_Frame.png` | mob + rage/XP bar frame, 9-sliced `4 5 5 5` (`--sk-barframe`) |
| `HealthMobBar_Frame2.png` | **hero** HP bar frame, 9-sliced `21 24 19 26` (`--sk-barframe-hero`) |
| `HealthMobBar_Frame3.png` | boss frame — **declared but UNUSED**, see the note below (`--sk-barframe-boss`) |
| `HealthMobBar_Health/Stamina/Mana.png` | HP / rage / XP fills (`--sk-fill-red/orange/blue`) |

**Bar frames are 9-sliced, not stretched backgrounds.** The slice numbers above are the art's
measured border thickness (sampled from each PNG's alpha). A stretched background scales its
border art unevenly (a 345x32 frame at 905x22 scales 2.6x wide but 0.7x tall), which is why the
fill used to sit short of the rails and run under the sides. Do not revert them to backgrounds.

⚠ `HealthMobBar_Frame3.png` (skull) is kept but **not applied**: its art is ~6:1 while the boss
bar renders ~27:1, so it smears ~4x, and it cannot be 9-sliced because the crest overhangs the
rails and lands in the stretching top-middle slice. Bosses use the plain mob frame. To revive
it, crop the skull into its own asset and draw it as a centred ornament at natural aspect; the
`.boss` class (set in `_syncEnemyHpBar`) is already there as the hook.

⚠ **Size:** ~7.5 MB total, but **6.6 MB of it is two files** — `BarBasic_Paper.png` (5.2 MB) and
`BarBasic_Standart.png` (1.5 MB), both 2048x2048 yet rendered at 10-22px border widths.
Downscale both to ~512px before any build; at render size the result is visually identical and
cuts them to roughly a tenth. Full 173-file pack stays in `CC/classicrpg2_skin/` (mockups read
from there); only the pieces actually used are mirrored here.

⚠ **Two-file rule:** these are staged in `CC/skin/` ONLY. Before an exe/APK build they must also
land in `ei/www/skin/` (and on GitHub `gamesprites/skin/` for web), or the reskin works on web
and silently breaks on exe/APK.

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
