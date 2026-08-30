# Production integration

The reservoir is assembled from three module roles: `left`, repeatable `center`, and `right`. Every chamber stores two sips and has three states:

- `0`: empty
- `1`: half-full / one sip
- `2`: full / two sips

## Recommended size

Use `20px` when replacing the existing compact pip row. Use `24px` when there is enough vertical room. The 16px exports remain functional but lose much of the silver ornament detail.

## HTML

```html
<link rel="stylesheet" href="modular-reservoir.css">

<div
  id="relic-sips"
  class="relic-reservoir"
  data-chambers="4"
  data-sips="5"
  data-size="20"
  data-asset-root="assets"
></div>

<script src="modular-reservoir.js"></script>
```

## Updating state

```js
const reservoir = document.querySelector('#relic-sips');

EverdeepRelicReservoir.set(reservoir, {
  chambers: relic.maxSips / 2,
  sips: relic.currentSips,
  size: 20
});
```

The renderer clamps the sip count and chooses the closest exported size. It fills chambers left-to-right using `2`, then `1`, then `0` states.

## Existing pip replacement

Replace the current generated `.pip-on` / `.pip-off` span row with one `.relic-reservoir` element. Do not stretch one complete bar image: capacities must be assembled from the exported modules.

The code intentionally uses zero gaps, margins, and overlaps. Each seam is owned by exactly one module.

## Available exported heights

`16`, `20`, `24`, `28`, `32`, `40`, and `48` pixels. Each folder contains nine transparent PNGs:

```text
left-0.png   left-1.png   left-2.png
center-0.png center-1.png center-2.png
right-0.png  right-1.png  right-2.png
```
