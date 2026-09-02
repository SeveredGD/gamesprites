# Everdeep Gloves Production Package

This package adds the first `gloves` equipment slot. It contains two validated production atlases, the complete T1–T3 affix data, thirteen approved unique-glove definitions, paper-doll placement instructions, combat rules, migration requirements, Journal copy, and a QA viewer.

## Approved scope

- All four proposed T1 uniques.
- All five proposed T2 uniques.
- Four T3 uniques: Hands of the Red Saint, Gauntlets of the Falling Gate, Empty Hands of Ordran, and Grasp of the Unmoved.
- `The Final Courtesy` is explicitly excluded.
- Life on Hit and Energy Shield on Hit share the `onHitRecovery` affix group on ordinary items.
- Energy Shield on Hit uses the reduced values: 4–6%, 6.5–9.5%, and 10–14% maximum Energy Shield.
- Gloves are available from the beginning; this package does not define a later unlock.
- Existing sets do not gain glove requirements in this pass.

## Production art

Copy the contents of `production sheets/gloves/` to:

```text
icons/new items/production sheets/gloves/
```

Both pages are 6×6 sheets with 64×64 source cells, designed for 32×32 display.

| Sheet | Frames | Validation |
|---|---:|---|
| `gloves-page-01.png` | 36 | RGBA, clean alpha, 43.3% transparent |
| `gloves-page-02.png` | 36 | RGBA, clean alpha, 54.9% transparent |

The raw generations, prompts, cleanup scripts, and checkerboard concepts are intentionally excluded.

## Files

- `production sheets/gloves/`: final PNGs, metadata, and row-major names.
- `data/glove-affixes.json`: machine-readable affix ranges, odds, exclusions, weights, and balance constants.
- `data/unique-gloves.json`: approved uniques and canonical icon mappings.
- `docs/GLOVE_AFFIX_DESIGN.md`: full mechanical design and test plan.
- `docs/PRODUCTION_AGENT_INSTRUCTIONS.md`: integration sequence for the current production game.
- `docs/JOURNAL_UPDATE.md`: required player-facing documentation.
- `qa/index.html`: art and canonical-frame viewer.

Open `qa/index.html` before import and compare every canonical unique assignment at both 64px and 32px.

