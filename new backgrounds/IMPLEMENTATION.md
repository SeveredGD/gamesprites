# Bloodpit Amphitheater Production Package

Use `bloodpit_amphitheater-animated-atlas.webp` with
`bloodpit_amphitheater-animated-atlas.json` through the same Phaser loader used
by `ACT_BG_ANIMATED` and the animated Delve backgrounds.

The atlas contains twelve complete 455 x 256 frames in a 4 x 3 grid. The
background geometry is identical in every frame. Only the rain, torch flames,
smoke, embers and localized glow move.

Suggested configuration:

```js
var BLOODPIT_BG_ANIMATED = {
  png: _REPO + 'new%20backgrounds/bloodpit/bloodpit_amphitheater-animated-atlas.webp',
  json: _REPO + 'new%20backgrounds/bloodpit/bloodpit_amphitheater-animated-atlas.json',
  key: 'bg-bloodpit-anim1',
  anim: 'bg-bloodpit-anim1-play'
};
```

When Bloodpit combat begins, pass this configuration to
`scene.setBackgroundAnimated(BLOODPIT_BG_ANIMATED)`. Restore the normal act
background when Bloodpit combat ends.

`defaultAnimation.speed` is intentionally `24.24`. The current game loader
multiplies that field by `0.375`, producing approximately 9.09 displayed FPS,
or 110 ms per frame.

The package also includes:

- `bloodpit_amphitheater.png`: 1376 x 768 fixed source/base image.
- `bloodpit_amphitheater-effects-overlay-atlas.webp`: optional transparent
  4 x 3 effects-only atlas if the production agent later separates the static
  background and animation layer. The existing background loader does not need
  this file.

Do not animate or reposition the full background sprite. Keep the same origin,
scale and camera placement used for the act backgrounds; all motion is baked
inside the atlas frames.
