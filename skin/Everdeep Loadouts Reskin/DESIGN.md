# Loadouts: armory ledger proposal

Source inspected: C:/Users/garre/Downloads/Everdeep Skill Panel Concepts/game-reference.html, renderLoadoutPanel() around line 82382 and openLoadoutMenu() around 82649. This is the previously fetched game build, not a verified newer version. Live browser entry failed with a network error during this review.

## Problem

The existing 440px overlay combines active-build switching, three context assignments, skill choices, independent trees and gear, renames and multi-loadout item priorities. Everything competes visually as a button. Active now and assigned for later need clearer separation.

## Proposed organization

Persistent top strip: current gear build and current tree, separately named. Never imply they must match after a context switch.

Builds tab: compact list of unlocked builds with current marker and Switch now action. Switching calls switchLoadout(), preserving its existing gear/tree behavior. Renaming gear and trees stays separate; don't assume they share names. Support up to six without huge cards. Show other-build priority summary as informational only.

Auto-switch tab: Farm / Bosses / Special context navigation. Show current assignments as Gear, Skill tree and Attack skill rows. Clicking Change opens the choices for that row only. Provide an explicit Keep current option mapped to the existing null value. Configuration changes do not masquerade as an immediate switch. Use existing setCtxLoadout, setCtxTree, setCtxSkill handlers with their toggle semantics accounted for.

Farm = normal mobs. Bosses = act and loop bosses. Special = Delve, Bloodpit and Bounties. Ranger also exposes Pet stance (Aggressive / Defensive / Utility / Keep current). Warrior exposes Technique. Retain class filtering and Tier2 locks. The concept image shows Sorceress only.

Loot priorities tab: existing Auto-gear my other loadouts checkbox at top with concise explanation. One expandable row per build, selected priorities summarized and count /5. Expanded row contains existing allowed stat choices, cap/near-cap markers and Fill empty slots from vault. No new priority ordering or weights. Builds with no priorities remain skipped. This does not change active-build pickup rules.

## Behavior that must survive

- Active build switching is immediate; context assignments are configuration.
- Tree and gear assignments are independent. Point pool remains shared; spent/free indicators appear in tree chooser.
- Selected choices can be cleared to null. Audit actual fallback application before changing 'Loadout default' wording: current source label and helper copy are inconsistent.
- No extra Save step unless code semantics are deliberately changed. Avoid a misleading dirty state.
- Retain one-loadout explanation and existing purchase/unlock flow; don't invent free create buttons.
- Auto-gearing sends passed-over drops to other builds based on priorities; no-priority builds are skipped; claimed items bypass vault.
- Fill action fills EMPTY slots only and does not replace equipped items.

## Skin

Smooth charcoal interior, narrow worn silver edges and restrained gold headings. One shared modal frame; shallow rows and subtle separators, with stronger framing only for primary tabs and selected actions. Sword/shield emblem in header. Reuse actual current skill/menu icons when implemented. Generate text-free frame pieces after the appearance is approved; mockup text is not a runtime texture.

Desktop: approximately 780–900px modal with context navigation left and focused editor right. Mobile: full-height sheet, fixed title/status/tab strip, context tabs across, one scrolling content region. 44px touch targets; no hover-only details. Handle long custom names without clipping.

Status: design and generated visual concepts only. No game implementation or production slices.
