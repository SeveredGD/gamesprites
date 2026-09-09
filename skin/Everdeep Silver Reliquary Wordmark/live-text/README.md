# Reusable Silver Reliquary text

Copy `silver-reliquary.css`, `silver-reliquary.js`, and `cinzel.woff2` together. All work locally, without a CDN. The font is copied unchanged from your capsule tool.

```html
<link rel="stylesheet" href="silver-reliquary.css">
<script defer src="silver-reliquary.js"></script>
<h1 class="silver-reliquary" style="--silver-size:72px">LOADOUTS</h1>
```

For text inserted after page load, call `SilverReliquary.enhance(container)`. To update an existing title:

```js
SilverReliquary.setText(document.querySelector('h1'), 'RESEARCH');
```

This is real DOM text with Cinzel, the original silver palette, three proportional outline layers and a metallic gradient. Decorative layers are hidden from screen readers; the face remains real selectable text. You can use arbitrary words, mixed case and line breaks. Size outlines through `--silver-size`; leave room around text for strokes. For small body copy, use a normal font treatment instead.

The bitmap's random scratches and exact raster bevel are not replicated. This reusable styling approximates that finish while remaining editable. It is intended for HTML overlays; a Phaser WebGL Text object cannot directly consume CSS, so use a DOM overlay or separately implement its gradient/stroke rendering.
