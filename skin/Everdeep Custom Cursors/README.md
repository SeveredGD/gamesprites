# Everdeep custom cursors

Six designs: arrow, gauntlet pointer, attack sword, magnifying glass, blocked action and hourglass. Each has transparent 32px, 48px and 64px PNGs. No ZIP; this folder is the complete package.

Start with `USING-CURSORS.md` for game integration instructions.

Open `preview.html` and hover the tiles to test. Choose a size and click to assess each hotspot. `cursor-size-check.png` shows actual-size renders against dark gray.

## Integration

Load `cursors.css` and apply `ed-cursors-48` to the game root (or `ed-cursors-32` / `ed-cursors-64`). Buttons and links use the pointing hand, disabled buttons the blocked cursor. Set `data-cursor="attack"`, `inspect`, `wait`, `pointer`, or `blocked` on specific interaction surfaces as appropriate. Native text cursors are retained on input fields. Do not show an attack cursor over automatic combat unless that surface has a real attack action.

`hotspots.json` provides source-relative CSS hotspot coordinates and native fallback types. Hotspots are initial placements; use the preview to judge feel before integrating. Hourglass is static. Assets and CSS are not wired into game code yet.

Built-in image generation created the source art; deterministic extraction, resizing and hotspot export used Python/Pillow/NumPy. Source and reproducible build tool are included. PNG dimensions and actual-size appearance were checked.

## Revision 2

Redrew default, attack and blocked cursors on the same conventional 45-degree northwest-to-southeast cursor axis. Recentered the blocked badge and its slash. Pointer, inspect and wait are unchanged. The original atlas is preserved; revised sources are `source/default-v2.png`, `source/attack-v2.png` and `source/blocked-v2.png`.

## Generation prompt

+Create a production source atlas of SIX custom mouse cursor graphics for Everdeep Idle, a dark fantasy ARPG. 1536x1024 canvas, strict 3 columns by 2 rows, each cell exactly 512x512. Exactly one cursor centered in each cell, each subject fits inside a 280x280 bounding square centered in its cell, generous uniform whitespace between all subjects. Row1 left: classic sharp mouse arrow pointing northwest with solid dark iron body and bright ivory silver bevel, restrained bronze inset. Row1 middle: armored gauntlet hand pointing UP with one extended index finger, other fingers curled, readable hand silhouette. Row1 right: short stout sword diagonally pointing northwest, silver blade with dark outline and simple bronze guard. Row2 left: magnifying glass, circular silver rim, dark lens with clear pale glass highlight, short handle extending southeast. Row2 middle: classic mouse arrow pointing northwest with a small red barred-circle badge attached to lower right, clear unavailable action. Row2 right: upright compact bronze hourglass, pale sand, clearly readable silhouette. Style: chunky crisply rendered game UI sprites, bold dark external outline plus selective pale silver highlights, dark charcoal iron and tarnished silver with small aged brass accents. Match the reference frame materials but prioritize recognition at 32 pixels. NO tiny filigree, no gears, no glow, no soft shadow, no text or labels, no surrounding boxes or UI frames. Flat front-facing cursor artwork. Transparent background genuinely alpha, no checkerboard or background texture. All six independent complete symbols, unclipped, no duplicate symbols.
