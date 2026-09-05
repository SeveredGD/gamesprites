# Traveling Tinker implementation handoff

Approved direction: Brass & Iron layout, clockwork nine-slice skin, cleaned button transparency, and three service tabs: Shop & inventions, Tinker improvements, Pets.

## Review

Open `brass-iron-preview.html` in a browser. It works locally without a server. This is the latest complete interactive layout, including the seven-pet catalogue. `preview.html` is a separate frame-resizing demonstration.

## Integration files

- `assets/`: transparent framing textures, button/tab states, nine individual regions per texture, decorative overlays and background tile.
- `brass-iron-clockwork.css`: approved layout skin overrides.
- `pets-layout.css`: Pets tab layout.
- `tinker-clockwork.css`: reusable standalone skin classes.
- `nine-slice.json`: exact slice coordinates and sizing rules.
- `pets-preview.js`: catalogue and demonstration purchase logic; replace demonstration state with the game's real pet systems.
- `README.md`: detailed geometry and integration notes.

## Required implementation behavior

Bind this design to the game's existing Tinker functions and save state. Preserve equipped/vault selection, item eligibility, stat preview, prices, daily hero/account limits, supplies stock, Fortune Mill states, Catalyst Chamber states, pet ownership and unlock gates. Preserve Talk later and Send away behavior.

The preview uses sample gold, inventory, mastery progress, ownership and purchases. Do not ship those values or the preview purchase handlers as gameplay logic. Pet catalogue values came from the inspected live build; use the game's current definitions as the runtime source of truth. Gear emblems in the preview are placeholders for existing item/pet art.

The Pets tab lists Clicks, Buckle, Scraps, Kettle, Clicker, Socket and Coil. Locked, insufficient-gold and owned appearances are included. Do not add Ratchet as a purchasable Tinker pet; the inspected game awards it through the Mill milestone.

Panels scale in both dimensions above their minimum dimensions. Button and tab heights must remain fixed at their selected artwork scale; widths can change. Keep top crest and winding key separate from stretched rails. The corrected v2 button alpha is included.

## Rebuilding and validation

Original source artwork and layout are included in `source/`. Rebuild tools use package-relative paths and require Python with Pillow and NumPy for asset extraction. They are optional; the finished assets and preview are already built.

Inspected narrow/wide frame reconstruction, the skinned shop/improvement layouts, control transparency on dark backgrounds, Pets tab rendering and local purchase state updates. Live-game integration has not been performed.

No ZIP is needed: give this entire folder to the implementation agent.
