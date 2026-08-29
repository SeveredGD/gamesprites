# Everdeep Ornate Silver skin bundle

This folder is the portable merge boundary for the Ornate Silver work developed
in `Everdeep_Floating_Layout_v4.html`. Move this entire `ornate-silver` folder
into the primary codebase without separating its assets from `integration/`.

## Contents

- `assets/` — every local frame, plaque, button, classic control, surface, and
  composite used or retained by v4. The original internal directory layout is
  preserved so no generated artwork is lost.
- `integration/ornate-silver-v4.css` — the extracted authoritative v4 sizing,
  overflow, icon-only, mobile, and frame behavior.
- `integration/ornate-silver-v4.js` — the extracted authoritative runtime skin
  registry, selector contracts, frame registry, observers, and audit API.
- `integration/everdeep-v4-skin-config.json` — portable selector-to-skin export.
- `integration/everdeep-reskin-map-v4-baseline.json` — full studio baseline.
- `integration/asset-manifest.json` — file sizes and SHA-256 hashes.

## Merge contract

1. Preserve the bundle at `skins/ornate-silver/` relative to the primary HTML,
   or rewrite the asset URLs in the JavaScript and JSON together.
2. Load `integration/ornate-silver-v4.css` after the primary layout styles.
3. Load `integration/ornate-silver-v4.js` after the game has created its initial
   DOM. It also observes controls added later.
4. Do not initialize both the extracted JavaScript and an embedded copy of the
   same v4 runtime. The floating-layout HTML retains its embedded copy for
   standalone testing; the extracted files are the merge source.
5. Keep icon controls marked by the exported `iconOnlySelector` unframed.
6. Run `EverdeepV4Buttons.audit()` after merge. It returns every remaining
   button whose text still exceeds its box.

The asset URLs used by the standalone v4 page are already rewritten to this
bundle, so moving or renaming it later requires a coordinated path update.
