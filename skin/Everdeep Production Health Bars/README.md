# Everdeep production health bars

Selected and productionized:

- Hero: Argent Thread
- Enemy: Fang Clasp
- Boss: Ossuary Reliquary

Each bar includes transparent `track`, `fill`, `bezel`, tiled strips, a fill leading edge, 0/25/50/75/100 previews, horizontal bezel slices, and a JSON manifest with exact clipping geometry.

Hero and boss center ornaments are also exported separately. Use `bezel-stretchable.png` plus `slices/center-ornament.png` when changing width, so the ornament is centered without distortion. For the original design width, `bezel.png` is ready to composite directly.

Open `dynamic-health-bars-demo.html` to test real-time fill behavior. The fill percentage is created by clipping `layers/fill.png`; none of the production layers has a baked fixed percentage.
