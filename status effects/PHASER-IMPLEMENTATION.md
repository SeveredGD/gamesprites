# Everdeep status VFX and projectile implementation

Use only the contents of `production/` in the game build. `source-generated/`, `work/`, and `tools/` are retained only for regeneration and should not ship in the APK.

`production/manifest.json` is the canonical asset list. Every status sheet is a horizontal strip of four `128 × 128` frames. All projectile images are transparent `128 × 128` canvases and face right.

The approved animation duration is `800 ms` for a complete four-frame pass (`200 ms` per frame). Approved preview placement is Head X `0`, Head Y `106`, Arc Spread `30`, and Arc Drop `20`; the local mob-container equivalent used below is an overhead Y offset of approximately `-36` from the sprite head.

## Phaser preload

```js
import vfxManifest from './vfx/manifest.json';

for (const [id, fx] of Object.entries(vfxManifest.statusEffects)) {
  this.load.spritesheet(`status-${id}`, `assets/vfx/${fx.file}`, {
    frameWidth: fx.frameWidth,
    frameHeight: fx.frameHeight,
  });
}

for (const [id, projectile] of Object.entries(vfxManifest.projectiles)) {
  this.load.image(`projectile-${id}`, `assets/vfx/${projectile.file}`);
}
```

## Register status animations once

```js
for (const [id, fx] of Object.entries(vfxManifest.statusEffects)) {
  const key = `status-${id}-loop`;
  if (!this.anims.exists(key)) {
    this.anims.create({
      key,
      frames: this.anims.generateFrameNumbers(`status-${id}`, { start: 0, end: 3 }),
      duration: fx.durationMs,
      repeat: fx.repeat,
    });
  }
}
```

## Mob placement contract

Do not place every status directly over the enemy. `manifest.json` supplies `placement`, stack scaling, and a stable `displayPriority` for each status.

| Placement | Status effects |
| --- | --- |
| Feet | `burn`, `frozen` |
| Body / center mass | `marked`, `bleed`, `shock`, `plague`, `corrosion`, `sunder`, `open-wounds` |
| Overhead | `chill`, `poison`, `stagger`, `artifice-trapped`, `arcane-vulnerability`, `hex`, `neurotoxin` |

Feet effects may coexist and remain layered around the same ground anchor. Body effects use a tight random scatter around center mass and progressively reduce in scale. Generate the random offsets once per enemy and retain them; never reroll during a layout update. Overhead effects fan out above the head and become progressively smaller as more overhead slots are occupied. Always sort by `displayPriority` so effects do not reshuffle whenever one expires.

Keep one sprite per active effect. Reuse it while the status remains active and destroy it when the status ends; do not create a sprite every combat tick.

```js
function attachMobStatus(scene, mobContainer, statusId) {
  const sprite = scene.add.sprite(0, 0, `status-${statusId}`)
    .setOrigin(0.5)
    .play(`status-${statusId}-loop`);
  sprite.statusId = statusId;
  mobContainer.add(sprite);
  return sprite;
}

const clamp = (value, min, max) => Math.max(min, Math.min(max, value));

function seededUnit(seed, label) {
  let hash = (2166136261 ^ seed) >>> 0;
  for (let i = 0; i < label.length; i++) {
    hash ^= label.charCodeAt(i);
    hash = Math.imul(hash, 16777619);
  }
  hash ^= hash >>> 16;
  hash = Math.imul(hash, 2246822507);
  hash ^= hash >>> 13;
  return (hash >>> 0) / 4294967295;
}

function layoutMobStatuses(mobSprite, statusSprites) {
  // These coordinates are local to a mob container whose origin is at its feet.
  const mobHeight = mobSprite.displayHeight;
  const mobWidth = mobSprite.displayWidth;
  const feetY = 0;
  const bodyY = -mobHeight * 0.46;
  const headY = -mobHeight;
  const mobScale = clamp(mobHeight / 128, 0.65, 1.25);
  // Tune these four values in the preview tool, then copy the chosen values here.
  const overheadLayout = {
    offsetX: 0,
    offsetY: -36,
    arcSpread: 30,
    arcDrop: 20,
  };

  const groups = { feet: [], body: [], overhead: [] };
  for (const sprite of statusSprites) {
    const spec = vfxManifest.statusEffects[sprite.statusId];
    groups[spec.placement].push({ sprite, spec });
  }
  for (const group of Object.values(groups)) {
    group.sort((a, b) => a.spec.displayPriority - b.spec.displayPriority);
  }

  groups.feet.forEach(({ sprite, spec }, index) => {
    const scale = Math.max(spec.stack.minScale,
      spec.stack.baseScale * Math.pow(spec.stack.scaleDecay, index)) * mobScale;
    sprite.setPosition(0, feetY - index * 3)
      .setScale(scale)
      .setDepth(4 + index);
  });

  // Create mobSprite.statusScatterSeed once when this enemy spawns.
  // seededUnit must return a stable 0..1 value for the same seed and string.
  mobSprite.statusScatterSeed ??= Phaser.Math.RND.integer();
  groups.body.forEach(({ sprite, spec }, index) => {
    const scale = Math.max(spec.stack.minScale,
      spec.stack.baseScale * Math.pow(spec.stack.scaleDecay, index)) * mobScale;
    const angle = seededUnit(mobSprite.statusScatterSeed, `${sprite.statusId}:angle`) * Math.PI * 2;
    const radius = Math.sqrt(seededUnit(mobSprite.statusScatterSeed, `${sprite.statusId}:radius`));
    sprite.setPosition(
      Math.cos(angle) * mobWidth * 0.12 * radius,
      bodyY + Math.sin(angle) * mobHeight * 0.14 * radius
    )
      .setScale(scale)
      .setAlpha(0.88)
      .setDepth(12 + index);
  });

  const count = groups.overhead.length;
  groups.overhead.forEach(({ sprite, spec }, index) => {
    const scale = Math.max(spec.stack.minScale,
      spec.stack.baseScale * Math.pow(spec.stack.scaleDecay, index)) * mobScale;
    // Fill the arch center-out: 0, left 1, right 1, left 2, right 2...
    const arcSlot = index === 0 ? 0
      : (index % 2 ? -Math.ceil(index / 2) : Math.ceil(index / 2));
    sprite.setPosition(
      overheadLayout.offsetX + arcSlot * overheadLayout.arcSpread,
      headY + overheadLayout.offsetY
        + overheadLayout.arcDrop * Math.pow(Math.abs(arcSlot), 1.25)
    ).setScale(scale).setDepth(24 + index);
  });
}
```

Call `layoutMobStatuses` whenever a status is added or removed, or when the mob sprite/scale changes. The manifest defaults are:

- Feet: scale `0.98`, decay `0.92`, minimum `0.78`.
- Body: scale `1.07`, decay `0.90`, minimum `0.65`.
- Overhead: scale `0.75`, decay `0.82`, minimum `0.36`. Overheads form an arch: the center is highest and later/smaller effects extend down both sides.

Adjust the four overhead layout values per enemy only if its sprite has unusual transparent padding. Do not compensate by changing individual status textures.

## Chill buildup and fade

Chill is intentionally not a looping effect. Its manifest entry uses `repeat: 0` and `holdLastFrame: true`. Play it once when chill first becomes active; Phaser will remain on frame 3, representing maximum visual buildup, until the status expires. Do not restart the animation on every chill stack.

When chill expires, fade the held sprite before destroying it:

```js
function removeMobStatus(scene, sprite) {
  if (!sprite) return;
  scene.tweens.add({
    targets: sprite,
    alpha: 0,
    duration: 220,
    ease: 'Sine.easeOut',
    onComplete: () => sprite.destroy(),
  });
}
```

## Move a projectile

These are static images; Phaser supplies motion. Rotate only if the shot direction is not horizontal.

```js
function fireProjectile(scene, id, x, y, targetX, targetY, speed = 650) {
  const shot = scene.physics.add.image(x, y, `projectile-${id}`)
    .setOrigin(0.5)
    .setDepth(10);
  const angle = Phaser.Math.Angle.Between(x, y, targetX, targetY);
  shot.setRotation(angle);
  scene.physics.velocityFromRotation(angle, speed, shot.body.velocity);
  scene.time.delayedCall(2500, () => shot.destroy());
  return shot;
}
```

For arrows, knives, javelins, and shards, scale the 128px canvas down to the desired combat size; the transparent padding keeps every asset on a common origin. Flasks and the trap disc should generally remain upright rather than rotating toward the target. A thrown flask can follow a tweened arc and rotate independently.

## Suggested semantic mapping

- `frozen`: full freeze or immobilize.
- `chill`: movement/attack slow.
- `shock`: lightning ailment or increased damage taken.
- `stagger`: knockback-on-hit stagger or short stun.
- `marked`: Ranger marked target.
- `plague`: Plaguebringer transferable plague stacks.
- `artifice-trapped`: Artifice pre-placed trap/immobilize.
- `arcane-vulnerability`: Ranger vulnerability stacks.
- `hex`: persistent curse/ascendancy hex.
- `corrosion`: Toxicologist corrosion stacks.
- `neurotoxin`: Toxicologist neurotoxin.
- `sunder`: armor/physical defense break.
- `open-wounds`: healing prevention plus wound DoT.

Do not use `open-wounds` as the normal physical bleed; it has its own sheet.
