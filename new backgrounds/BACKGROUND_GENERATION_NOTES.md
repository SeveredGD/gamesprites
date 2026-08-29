# Everdeep Combat Background Notes

## Combat-stage composition

- Treat only the bottom 20% as the side-view character-footing strip, not the entire lower third.
- Keep that foreground strip level across the width with a shared character baseline and only mild depth cues.
- Do not place rocks, raised slabs, ice spikes, rubble, loot, or other raised props in the bottom 20%.
- The bottom 20% should still have rich visual noise: varied tile values, chipped corners, hairline cracks, stains, frost veins, thin snow traces, worn flat runes, and embedded grit.
- Distinguish visual texture from collision-like obstruction: painted, inset, cracked, or embedded detail is welcome across the footing strip; raised props are not.
- Tiny low-profile debris may sit at the extreme bottom corners, outside normal character positions.
- Restore environmental detail immediately behind it: the 55–80% height band may contain broken paving, snowbanks, rubble, rocks, and ice formations.
- Decorative masses may occupy the middle ground as well as the outer edges, provided they do not project into the foreground footing strip.
- Preserve a quiet central lane so fighters and effects remain readable.

## Successful ambient-mist animation

- Keep the base background and entire playable ground completely static.
- Build mist as irregular, full-frame alpha clouds rather than horizontal strips.
- Feather mist vertically to zero with a soft cosine falloff so no rectangular band edges appear.
- Duplicate fog shapes across both horizontal boundaries before blurring; wrapped horizontal motion then remains seamless.
- Use multiple low-opacity layers moving at different speeds and directions.
- Avoid shifted water rectangles or per-row masks; they read as hard moving stripes.
- Keep particles sparse, tiny, dim, and outside the central combat lane.
- Current successful timing: 72 frames at 12 FPS for a six-second loop.

## Act-specific ambient animation

- Act 2: use multiple low-opacity, feathered ochre sand clouds plus sparse horizontal grains. Move layers at different speeds and keep the scenery fixed.
- Act 3: combine the proven feathered mist with slow violet glow pulses and sparse motes. Avoid moving rectangular water regions.
- Act 4: detect existing cyan/green luminous pixels, divide them into spatial groups, and pulse those groups independently so the runes blink rather than the whole scene flashing.
- Act 5: sweep small snow streaks diagonally across the full frame with wrapped particle motion. Add only a very faint full-frame snow veil; never translate or warp the ground art.
- All loops currently use 72 atlas frames at 12 FPS for six seconds.

## Output conventions

- Static production size: 1376×768.
- Runtime animation frame size: 455×256.
- Runtime animation format: WebP frame atlas plus matching JSON metadata.
- Keep new candidates versioned until approved; do not overwrite live game backgrounds automatically.
