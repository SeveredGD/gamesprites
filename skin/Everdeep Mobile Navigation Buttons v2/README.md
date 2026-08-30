# Everdeep mobile navigation buttons v2

Five square navigation buttons with the label embedded directly into each bitmap: Combat, Runs, Gear, Skills, and More.

## Art direction

- Warm neutral silver and charcoal coloring from the chain-button family
- No literal chain links, moons, crescents, notification badges, or separate CSS labels
- Shared faceted frame, top/bottom diamond, dark inset, and integrated name plaque
- Gear uses separate bag, helmet, and sword silhouettes

## Production files

`production/` contains 72, 80, 96, and 128 pixel versions. Every size has:

- `nav-{name}.png` — normal state
- `nav-{name}-active.png` — selected state with a warm ivory/gold keyline

The 128px files are suitable as high-density browser sources and can be displayed around 64–80 CSS pixels. The 72px files fit five buttons across a 360px viewport without requiring separate text beneath them.

## Suggested markup

Use five equal grid columns. The label is already part of the PNG, so the button only needs an accessible `aria-label`. Swap to the `-active.png` sibling for the selected tab. Do not add another visible text label or notification circle over the art.

`index.html` is a responsive click-through preview.
