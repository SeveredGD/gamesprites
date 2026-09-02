# Production integration instructions — Gloves

Integrate by symbol and behavior, not by old line number. Production has changed substantially since the reference copy used to prepare this package.

## 1. Import the assets

Copy both production pages and their JSON files to:

```text
icons/new items/production sheets/gloves/
```

Register two atlases using the standard 64px cell contract:

```js
gloves_p1: _newSheet('gloves/gloves-page-01.png'),
gloves_p2: _newSheet('gloves/gloves-page-02.png'),
```

Return `gloves_p1` from `_iconAtlasKey('gloves', classKey)`.

For an unnamed generated glove with no saved icon, roll uniformly across all 72 frames. Frames 30–35 remain valid generic fallback art even though selected frames are also used canonically by uniques.

```js
if (item.slot === 'gloves' && item.iconFrame == null) {
  var roll = ri(0, ITEM_ICON_ATLAS.gloves_p1.frames + ITEM_ICON_ATLAS.gloves_p2.frames - 1);
  if (roll >= ITEM_ICON_ATLAS.gloves_p1.frames) {
    item.iconAtlas = 'gloves_p2';
    item.iconFrame = roll - ITEM_ICON_ATLAS.gloves_p1.frames;
  } else {
    item.iconAtlas = 'gloves_p1';
    item.iconFrame = roll;
  }
  return;
}
```

Add every mapping from `data/unique-gloves.json` to `NAMED_ITEM_ICON`. The JSON mapping is canonical and should also repair old copies at render time if test saves already contain these names.

## 2. Register the new slot everywhere

The slot key is exactly `gloves` and the label is `Gloves`.

Add it to:

- `SLOTS`
- `EQUIP_SLOTS`
- `SLOT_LABELS`
- `SLOT_STAT_POOLS`
- `MAGIC_BASES` for every class
- Normal item-name/base-name generation
- Hero `equipped` defaults
- Vault collections
- Every loadout and loadout-lock structure
- Item filters and sorting
- Drag/drop and equip validation
- Crafting, enchanting, infusion, reforging, tinkering, awakening, salvage, scoring, and comparisons
- Drop previews and offline drop simulation
- Debug gear builders
- Artifact/unique/set scans that still contain hard-coded slot arrays
- Save, import, export, cloud sync, and reset/default constructors
- Equipment completeness checks and Journey objectives

Do not rely only on `EQUIP_SLOTS`: the reference copy contains several separate hard-coded arrays such as `['weapon', 'armor', 'ring', 'ring2', 'amulet', 'trinket', 'boots']`. Search for every one and either add `gloves` or replace it with the authoritative slot collection.

Suggested base terms:

```js
MAGIC_BASES.sorceress.gloves = 'Runegloves';
MAGIC_BASES.warrior.gloves = 'Gauntlets';
MAGIC_BASES.rogue.gloves = 'Handwraps';
MAGIC_BASES.ranger.gloves = 'Grips';
```

Gloves are available from the start. Do not hide or disable the slot behind Desolation unless production design later says otherwise.

Existing five-piece sets remain five-piece sets. Merely adding `gloves` to the equipment registry must not make old sets require a sixth item.

## 3. Save migration

Loading an old save must add missing containers without touching existing equipment:

```js
if (!Object.prototype.hasOwnProperty.call(hero.equipped, 'gloves')) hero.equipped.gloves = null;
if (!hero.vault.gloves) hero.vault.gloves = [];
```

Apply equivalent defaults to every saved loadout, lock map, item-priority map, vault expansion map, and offline snapshot that is keyed by equipment slot.

Missing new stat keys always equal zero. Do not rewrite or reroll old items.

## 4. Paper-doll change

Add the missing DOM slot:

```html
<div class="gear-row drop-target" id="pd-slot-gloves" data-slot="gloves"></div>
```

The requested layout moves Armor from the old left-side armor position to the center of the hero. Gloves take Armor's former position.

Use this named-area layout:

```css
#gear-list[data-vd="doll"] {
  grid-template-areas:
    "acc     acc    acc   acc"
    "weapon  .      .     amulet"
    "gloves  armor  armor ring"
    "boots   relics trink ring2";
}

#gear-list[data-vd="doll"] #pd-slot-gloves {
  grid-area: gloves;
}

#gear-list[data-vd="doll"] #pd-slot-armor {
  grid-area: armor;
  justify-self: center;
}
```

Keep Armor and Gloves as separate 58×58 wells using the current Thorned Reliquary slot frame. Armor should sit over the torso, centered between the two middle columns. Gloves occupy the exact left-side cell Armor previously used.

Update any JavaScript that derives paper-doll slot positions or validates named grid areas. Check all four hero silhouettes at desktop and mobile widths. Armor may overlap the silhouette visually by design, but labels and wells must not overlap neighboring slots.

In list/compact equipment modes, keep a normal readable order such as Weapon, Armor, Gloves, Rings, Amulet, Trinket, Boots. The doll's visual placement should not force the list order.

## 5. Add the tiered glove pool

Use `data/glove-affixes.json` as the source of truth.

Do not put the glove ranges directly into the old global rarity tables and then let every difficulty multiply every value. Glove affix tier is a separate roll:

1. Choose the affix using glove weights.
2. Roll T1, T2, or T3 using the content odds.
3. Resolve the range for that tier.
4. Apply existing location scaling only when `locationScaled` is true.
5. Store the resolved roll range and tier on the item.

Suggested item metadata:

```js
item.affixTiers = item.affixTiers || {};
item.affixTiers[stat] = tier;
item._rollRanges = item._rollRanges || {};
item._rollRanges[stat] = [resolvedMin, resolvedMax];
```

T1 is the lowest tier and T3 is the highest. Tooltips must show the tier independently on each stat.

## 6. Enforce the recovery exclusion

`lifeOnHitBps` and `shieldOnHitHalfPct` share `onHitRecovery`.

Once one is selected on an ordinary glove, remove both from the remaining pool. Enforce this during initial generation and every mutation path. Checking only during random drop generation is insufficient because crafting could otherwise create illegal gloves.

Only authored uniques with `bypassExclusiveGroups: ['onHitRecovery']` may carry both.

## 7. Aggregate the new stats

Add these derived hero fields during the normal equipment recalculation:

```js
hero._lifeOnHitBps
hero._shieldOnHitHalfPct
hero._crushingBlow
hero._openWounds
hero._cullingStrike
hero._staggerOnHit
```

Add the keys to every parser/serializer stat list. If production still uses a CSV header for authored uniques, append the keys without shifting existing columns incorrectly. Prefer converting authored unique definitions to named objects if practical.

## 8. Resolve glove effects once per attack execution

Create or reuse an attack sequence ID. All fragments from the same attack—including projectiles, chains, AoE targets, and secondary hits—share that ID. Glove effects resolve only once after the first direct hit that deals damage.

Do not trigger glove effects from:

- DoTs
- Companions
- Thorns or reflection
- Environmental damage
- Automatic echoes or repeats
- Hits against invulnerable targets

Resolve in this order:

1. Crushing Blow before direct damage.
2. Direct damage.
3. Life or Energy Shield recovery.
4. Open Wounds.
5. Stagger.
6. Culling Strike.
7. The existing single death/reward path.

Use the constants and detailed behavior in `docs/GLOVE_AFFIX_DESIGN.md`. Keep balance constants in one `GLOVE_AFFIX_BALANCE` object.

## 9. Add the approved uniques

Import exactly the thirteen entries in `data/unique-gloves.json`.

Approved:

- T1: The Barber's Red Gloves, Pitfighter's Knuckles, Iron Argument, The Last Touch.
- T2: Surgeon's Ledger, Wardweaver's Hands, The Hammer's Memory, Mercy's End, The Twin Reservoir.
- T3: Hands of the Red Saint, Gauntlets of the Falling Gate, Empty Hands of Ordran, Grasp of the Unmoved.

Do not add `The Final Courtesy`.

Implement unique behavior by stable `effectId`, not by repeating item-name comparisons throughout combat code. A compatibility `_hasUnique(name)` check may remain at the boundary, but each mechanic should route through one effect hook.

## 10. Update the Journal

Use `docs/JOURNAL_UPDATE.md`. Also update Reforge help, advanced tooltip help, slot counts, and Journey equipment objectives. Add a Journey discovery objective that opens Equipment and focuses the glove slot.

## 11. Verification checklist

- Both atlases load in DOM and Phaser/canvas renderers.
- Random gloves use frames from both pages.
- All thirteen uniques resolve to their canonical frame.
- The excluded unique is absent.
- Old saves load with an empty glove slot and empty glove vault.
- Gloves drop, equip, unequip, lock, salvage, reforge, enchant, infuse, awaken, compare, and survive save/load.
- Auto-equip and gear score do not produce `NaN`.
- Every glove affix can roll T1, T2, and T3.
- Ordinary gloves never contain both recovery affixes.
- The two approved dual-recovery uniques contain both.
- Multishot, AoE, chains, and echoes resolve glove effects only once per attack execution.
- Energy Shield on Hit displays half-percent rolls correctly.
- Armor is centered on the paper doll and Gloves occupy the old Armor cell on every class and screen size.
- The Journal and Journey are updated in the same release.

