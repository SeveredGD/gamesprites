# Implementation notes

## Fixed current stage

Use `runeforge-strongbox-master-1284x540.png` as a transparent overlay at the exact equipment/vault usable-area bounds. Its geometry matches the Ossuary production master.

The two content rectangles in the 1935×813 coordinate system are:

```text
equipment: x 132, y 132, width 763, height 549
vault:     x 1040, y 132, width 763, height 549
```

When the complete master is scaled, use the normalized rectangles from `slice-manifest.json` to position the two content containers.

## Variable-size assembly

Build the perimeter from four fixed corners and four stretchable rails. Build the divider independently:

```text
divider-top                    fixed
divider-upper-rail             stretch vertically
divider-center-ornament        fixed and centered
divider-lower-rail             stretch vertically
divider-bottom                 fixed
```

Do not stretch the central medallion, corner blocks, or divider caps. Do not use one conventional nine-slice across the entire dual frame; the center divider must remain independent.

## Layer order

1. panel background
2. equipment and vault contents
3. outer frame slices
4. divider rails
5. fixed divider top, center ornament, and bottom
6. drag/drop highlights and tooltips
