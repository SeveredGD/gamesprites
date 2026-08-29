# Everdeep new item assets

This package contains the final transparent production sheets and their coordinate JSON, plus both versions of the individually spliced ultra-rare concepts.

## Production sheets

Each category folder contains:

- the 64px-per-cell transparent production PNG;
- its coordinate/name JSON;
- the row-major item-name list.

Included sheets: warrior, sorceress, ranger, and rogue weapons; warrior, sorceress, ranger, and rogue armor; rings; amulets; boots; trinket pages 01 and 02; and the corrected T3 unique page.

## Ultra rares

`ultra rares/source sheets` contains both the detailed and simplified concept atlases with their coordinate JSON.

`ultra rares/spliced icons` contains every concept as an individual transparent PNG in both 64px source and 32px display sizes:

- `v1-detailed` — richer original concepts;
- `v2-simplified` — cleaner 32px-first redraws.

Use `ultra-rare-picker.html` to compare the two versions. `ultra-rare-splice-manifest.json` maps filenames to suggested names and source positions. Fill in `ultra-rare-selection-template.json` to record final choices.

Preview renders, raw magenta generations, superseded drafts, and correction backups are intentionally excluded.
