# Implementation instructions

## Scope and integration point

Restyle the existing `renderIdleQueue()` output and its `#idle-queue-box`. The inspected game snapshot used `renderIdleQueue` around line 60171; search by function name because live line numbers change. Preserve the existing runner, affordability/unlock checks, persistence, loadout handling, offline simulation, rewards and events.

`index.html` is an executable visual reference, not replacement game code. Its sample wallet/launch checks, start/stop simulation and external-destination stubs must not enter production. `scroll.js` shows DOM grouping and sprite assignment; port those presentation changes into the current renderer, preferably by emitting the classes directly rather than post-processing child indexes. Avoid copying the preview toolbar, fixtures, design-selection functions or accumulated five-layout CSS into the game.

## Required structure

```
idle-queue-box (height-limited flex column, container-type:inline-size)
  body artwork (absolute background, behind all controls)
  q-header (fixed cap + title + existing help/status)
  q-map (existing Expedition Map button and conditional Everdeep entry)
  q-body (flex:1; min-height:0)
    queue heading / Clear all
    q-list (flex:1; min-height:0; overflow-y:auto)
      q-row (grip, existing atlas icon, label, run-controls)
  q-transport (fixed footer roller + Loop / Supplies / cost / Start or Stop)
  q-rewards (collapsible drawer with existing reward handlers)
  Close
```

Only the run list scrolls during queue browsing. A long expanded reward drawer may scroll internally. Use the game's existing scrollbar styling; no generated scrollbar asset. Do not hide clipped controls with overflow:hidden as a layout fix. Maintain scroll position across renderer updates; reset it only when appropriate (the preview resets its fixtures).

The current sample uses a 960px maximum overall width, 84% content width (86% on phones), body inset 4% (2% phones), and a 96% footer width (98% phones). Content widths are deliberately smaller than the artwork. No negative horizontal margins. Rows use a grid with icon/label and a wrapping control group. Preserve space inside the footer endcaps before laying out buttons.

The phone preview has a 900px minimum overall height to keep the independent list usable; this makes the document scroll. In the actual modal, adapt the outer height to the game's safe viewport, allowing outer modal scrolling on short screens or collapsing secondary sections. Preserve all controls and a usable list; do not blindly paste the preview minimum-height into a max-height:92vh modal.

## Assets and slices

All source slice values are native pixels, ordered top/right/bottom/left; CSS border-image converts them to displayed border widths independently.

| File | Native size | Source slices | Treatment |
|---|---|---|---|
| header.png | 1188×152 | none | Uniformly scale complete cap to available width; never stretch its plaque vertically |
| body.png | 1132×391 | 24 / 24 / 24 / 24 | Nine-slice with filled center |
| footer.png | 1177×209 | 45 / 205 / 45 / 205 | Fixed endcaps, expandable center |
| run.png | 1125×114 | 18 / 22 / 18 / 22 | Nine-slice strip; no icon socket |

Body example: `border-image: url(body.png) 24 fill / 18px stretch`. Run example: `border-image: url(run.png) 18 22 fill / 14px stretch`. Footer example: `border-image: url(footer.png) 45 205 fill / 22px 82px stretch` (phone displayed borders 18px/42px). Keep content padding inside these visible edges.

The body is not a seamless repeating tile: its top/bottom are torn. Use nine-slice fill, not repeat-y. The PNG alpha has already been extracted; do not chroma-key the runtime PNGs again. Source master is retained separately.

## Title and suspension alignment

Set `container-type:inline-size` on the queue box; the header occupies its full width. Header background is centered at top with `background-size:100% auto`.

The title safe rectangle is left 30%, right 30%, top 1.3cqw, height 9.2cqw. Center the text with flex alignment in that rectangle. This centers it on the plaque, not on the taller header area that also contains status/help. Use the game's font and responsive font size; text must not reach the violet gems.

Body top = `calc(12cqw - 4px)`, meeting the terminal links. Header layout height = `calc(12.8cqw + 44px)` (54px extra on phones). Tiny attachment rings at left 20% and 80% align to that same body-top position. Keep the cap in front and the body behind. Do not restore the old fixed 65px body-top offset: it pushed vellum up behind the roller.

## Existing atlas mapping

Reuse the game's registry where available. These local atlas copies support the preview:

- `acts.png` 3×3: A1 index 2, A2 0, A3 1, A4 7, A5 3.
- `queue_icons_3.png` 3×2: boss 4, delve 3, bloodpit 2.
- `top_bar_buttons.png` 3×2: bounty 0, brightness .57, matching the map's XM_NODES entry.

All already contain their frames. Do not add a second icon socket. Use the existing Everdeep icon/registry mapping for that mode; the demo's unused generic fallback is not an approved substitute. Do not strip arbitrary leading characters from translated production labels; emit text and icons separately. The sample adapter's regex is only for its English fixture labels.

## Behaviors to preserve

- Map builds runs. Keep the conditional Everdeep configuration entry and legacy full-act rendering.
- Drag reorder and arrow reorder; remove and Clear all.
- Farm pack selection; farm/boss/act/bounty counts; Delve extraction-depth changes and until-death variant; Bloodpit 5/10/20-minute select.
- Loop ON/OFF; supplies eligibility/allocation and stock; estimated lap cost.
- Real Start from the top and Stop semantics, including launch preconditions and refunds. No new pause/resume or goal conditions.
- Blocked-entry labels and existing runner behavior (it can skip currently unlaunchable entries).
- Preserve supplied-state indicator, active-entry highlight and any existing progress/ETA information.
- Preserve all Pending Rewards types, including companion rewards. Drawer collapses by default, shows count and opens without claiming anything. Review/Review All invoke the unchanged game handlers. Preserve drawer-open state through renders; no need to save it as gameplay data.

## Acceptance checks

1. Test empty, one-entry, 20-entry, active, unaffordable and mixed-supplies queues.
2. Test every live run type, including legacy Act, Everdeep and until-death Delve.
3. At desktop, phone and short landscape sizes, all controls stay within the visible vellum/footer interior; no horizontal overflow.
4. Scroll the list to its end: title/footer stay outside that scroll region. Edit/reorder/remove entries and confirm scroll/queue indexes remain correct.
5. Expand rewards with long labels and many entries; verify all reward buttons remain reachable and work. Closing the drawer must not consume rewards.
6. Verify title center and chain attachment at multiple widths. Check PNG edges on dark backgrounds for key-color fringes.
7. Verify game keyboard controls, focus visibility, keyboard scrolling, translated labels and existing touch reorder behavior. Add accessible names to icon-only buttons if missing.
8. Run the repository's required checks and regression-test save/load, start/stop and offline queue behavior. This skin must not change game balance or queue execution.

The packaged preview was visually checked at desktop/390px and its reward drawer and row controls checked for horizontal containment. Production game integration and gameplay tests remain the coding agent's work.
