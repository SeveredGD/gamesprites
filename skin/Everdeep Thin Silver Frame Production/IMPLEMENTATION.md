# Thin silver frame implementation

The selected winners are production-cut and ready for CSS `border-image` use at a true 2 px or 3 px visible width.

## Recommended use

Load `thin-silver-frames.css`, then add the base class and one variant:

```html
<section class="ed-thin-frame ed-thin-frame--runic ed-thin-frame--3px">
  ...content...
</section>
```

Available variants:

- `ed-thin-frame--runic`
- `ed-thin-frame--thornwire`
- `ed-thin-frame--moonsteel`

Available width presets:

- `ed-thin-frame--2px`
- `ed-thin-frame--3px`

The 3 px preset is recommended. At 2 px, the silver silhouette remains visible but most internal engraving necessarily collapses.

## Direct CSS values

```css
/* Runic Hairline */
border: 3px solid transparent;
border-image: url("02-runic-hairline/master.png") 57 67 55 67 / 3px stretch;

/* Thornwire */
border: 3px solid transparent;
border-image: url("03-thornwire/master.png") 61 61 63 59 / 3px stretch;

/* Moonsteel Stitch */
border: 3px solid transparent;
border-image: url("05-moonsteel-stitch/master.png") 61 61 62 63 / 3px stretch;
```

## Non-CSS consumers

Every variant also includes nine named PNGs under `slices/`. Compose them as corners, horizontal edges, vertical edges, and a guaranteed transparent 1×1 center. The source-space slice measurements are recorded in `manifest.json`.

Use nearest-neighbor sampling for explicitly pixel-scaled canvas or engine rendering. In normal CSS, allow `border-image` to perform the final fit.

## Suggested roles

- Runic Hairline: default compact cards, mastery rows, tooltips, and list entries.
- Thornwire: dangerous, enemy, curse, Bloodpit, or Delve surfaces.
- Moonsteel Stitch: skills, magic, vault, and arcane information panels.
