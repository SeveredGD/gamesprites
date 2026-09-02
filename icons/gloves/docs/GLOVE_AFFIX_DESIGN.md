# Everdeep Glove Affixes — Design and Implementation Notes

Status: design locked for later implementation  
Reference inspected: `Everdeep_Idle_1_10_0 (2).html`  
Important: production has drifted from this reference. Locate equivalent systems in the current production file instead of applying line-based patches.

## Goals

- Give gloves a distinct offensive-sustain and on-hit identity.
- Add three affix tiers to every glove stat. T1 is lowest and T3 is highest.
- Allow any non-unique glove to roll any of the three affix tiers, with later content improving the odds.
- Add Life on Hit, Energy Shield on Hit, Crushing Blow, Open Wounds, Culling Strike, and Stagger on Hit.
- Prevent multihit, projectile, AoE, echo, and attack-speed combinations from multiplying on-hit recovery beyond the intended value.
- Keep class skills, uniques, and divine effects stronger than ordinary glove affixes where their mechanics overlap.

## Glove affix pool

Flat numerical stats continue through the game's existing location/item scaling. Percentage recovery, proc chances, thresholds, and other bounded values must not be multiplied by location scaling.

| Key | Display name | T1 | T2 | T3 | Scaling |
|---|---|---:|---:|---:|---|
| `mainDmg` | Damage | 2–5 | 6–10 | 11–16 | Existing item scaling |
| `mainSpd` | Attack Speed | 1–3 | 4–6 | 7–10 | Existing item scaling |
| `hp` | Maximum Health | 5–15 | 16–30 | 31–50 | Existing item scaling |
| `hpRegen` | Health Regeneration | 1–2 | 3–4 | 5–7 | Existing item scaling |
| `critChance` | Critical Chance | 1–2% | 3–4% | 5–6% | Fixed |
| `spellShield` | Maximum Energy Shield | 2–5 | 6–11 | 12–18 | Existing item scaling |
| `statusEffect` | Status Effectiveness | 3–6% | 7–11% | 12–16% | Fixed |
| `ailmentDmg` | Ailment Damage | 4–8% | 9–15% | 16–24% | Fixed |
| `lifeOnHitBps` | Life on Hit | 0.15–0.25% max HP | 0.30–0.45% | 0.50–0.75% | Fixed basis points |
| `shieldOnHitHalfPct` | Energy Shield on Hit | 4–6% max ES | 6.5–9.5% | 10–14% | Fixed half-percent units |
| `crushingBlow` | Crushing Blow | 3–5% chance | 6–8% | 9–12% | Fixed |
| `openWounds` | Open Wounds | 6–10% chance | 11–16% | 17–24% | Fixed |
| `cullingStrike` | Culling Strike | 3% threshold | 4–5% | 6–8% | Fixed |
| `staggerOnHit` | Stagger on Hit | 5–8% chance | 9–14% | 15–22% | Fixed |

Energy Shield on Hit has been reduced by exactly 50% from the first proposal.

### Storage units

Avoid floating-point ambiguity in saved items:

- Store Life on Hit as basis points of maximum health. `15` means `0.15%`.
- Store Energy Shield on Hit as half-percent units. `13` means `6.5%`.
- Store all proc chances and Culling Strike thresholds as whole percentage points.
- Store the rolled affix tier alongside the resolved range so advanced tooltips can display and grade it correctly.

Example:

```js
item.stats.lifeOnHitBps = 42; // 0.42% maximum HP
item.affixTiers.lifeOnHitBps = 2;

item.stats.shieldOnHitHalfPct = 17; // 8.5% maximum Energy Shield
item.affixTiers.shieldOnHitHalfPct = 2;
```

## Affix tiers

Roll an affix's tier independently after choosing the affix. Item rarity determines affix count, not tier eligibility.

| Content | T1 | T2 | T3 |
|---|---:|---:|---:|
| Normal difficulty | 75% | 23% | 2% |
| Nightmare | 45% | 48% | 7% |
| Hell | 20% | 60% | 20% |
| Desolation / Epoch | 10% | 50% | 40% |

Deep Delve may improve these odds later, but should not enlarge fixed percentage ranges.

Suggested helper:

```js
function rollGloveAffixTier(context) {
  var odds = context.isDesolation || context.isEpoch
    ? [0.10, 0.50, 0.40]
    : context.difficulty === 'hell'
      ? [0.20, 0.60, 0.20]
      : context.difficulty === 'nightmare'
        ? [0.45, 0.48, 0.07]
        : [0.75, 0.23, 0.02];

  var r = Math.random();
  return r < odds[0] ? 1 : r < odds[0] + odds[1] ? 2 : 3;
}
```

## Shared recovery-affix slot

Life on Hit and Energy Shield on Hit belong to the exclusive group `onHitRecovery`.

On ordinary items, selecting either member removes both from the remaining pool. They consume one normal affix slot and can never coexist on the same non-unique glove.

This restriction must be enforced in every path that can create or alter affixes:

- Item generation
- Reforging
- Enchanting
- Infusion
- Add-affix crafting
- Item cloning or reconstruction from recipes

Uniques and explicitly authored set effects may bypass the restriction.

```js
var AFFIX_GROUPS = {
  lifeOnHitBps: 'onHitRecovery',
  shieldOnHitHalfPct: 'onHitRecovery'
};

function removeConflictingAffixes(available, selectedStat) {
  var group = AFFIX_GROUPS[selectedStat];
  if (!group) return available;
  return available.filter(function(key) {
    return AFFIX_GROUPS[key] !== group;
  });
}
```

## Eligible direct hit

All six new on-hit mechanics use one shared eligibility decision. Calculate it once per attack execution and pass that context to the individual effects.

An eligible hit:

- Comes from the hero's selected attack or skill.
- Successfully deals at least one point of direct damage.
- Can trigger no more than once per attack execution.

It does not come from:

- Individual targets of the same AoE attack
- Additional projectiles from the same attack
- Secondary explosions
- Damage over time
- Thorns or reflected damage
- Companions
- Environmental damage
- Automatic echoes or repeats, unless a unique explicitly overrides this rule
- Damage against an invulnerable target

Create an attack sequence ID when an attack begins. Every damage fragment from that activation carries the same ID. Track whether glove on-hit effects have already been resolved for that sequence.

```js
var hitContext = {
  sequenceId: ++hero._attackSequence,
  directDamage: damageActuallyDealt,
  target: enemy,
  gloveEffectsResolved: false
};
```

This is safer than trying to identify multihit skills separately inside every affix.

## Life on Hit

Restore the rolled basis-point percentage of maximum health after an eligible direct hit.

```js
var gain = Math.max(1, Math.round(hero.maxHp * hero._lifeOnHitBps / 10000));
hero.hp = Math.min(hero.maxHp, hero.hp + allowedByRecoveryBudget(gain));
```

Rules:

- One trigger per eligible attack execution.
- Cannot overheal.
- Critical damage does not increase it.
- Maximum Life-on-Hit recovery is 3% of maximum HP in a rolling one-second window.
- Lifesteal is separate and does not consume this recovery budget.
- A unique may explicitly allow echoes, projectiles, or companion attacks to trigger it.

The cap is a safety rail for extreme attack speed, not the expected normal balance point.

## Energy Shield on Hit

Restore the rolled half-percent amount of maximum Energy Shield after an eligible direct hit.

```js
var pct = hero._shieldOnHitHalfPct * 0.5;
var gain = Math.max(1, Math.round(hero._spellShield * pct / 100));
hero._shieldCurrent = Math.min(
  hero._spellShield,
  hero._shieldCurrent + allowedByShieldRecoveryBudget(gain)
);
```

Rules:

- Requires `hero._spellShield > 0`; otherwise it has no effect.
- Does not create maximum Energy Shield.
- Cannot exceed `hero._spellShield`.
- One trigger per eligible attack execution.
- Maximum recovery is 25% of maximum Energy Shield in a rolling one-second window.
- It restores the existing shield pool; it does not create an overshield.

The per-second cap was also reduced from the initial 50% proposal to match the 50% magnitude reduction.

## Crushing Blow

The affix value is its proc chance. Roll once per eligible attack execution and apply it immediately before normal direct-hit damage.

| Target | Bonus damage |
|---|---:|
| Normal enemy | 8% current HP |
| Rare, elite, or guardian | 2% current HP |
| Boss | 0.5% current HP |

Rules:

- Cannot crit.
- Ignores ordinary damage multipliers and resistance.
- Does not trigger Life on Hit, Energy Shield on Hit, lifesteal, ailments, or another Crushing Blow.
- Cannot reduce the target below one HP. The accompanying direct hit can kill it.
- Uses current HP, causing natural diminishing returns during the fight.
- Track its damage separately in combat recap data.

## Open Wounds

The affix value is its application chance. On application:

- Prevent all enemy regeneration and direct healing for four seconds.
- Deal 30% of the triggering direct hit's actual damage over four seconds.
- Tick once per second for four ticks.
- Count as a physical ailment.
- Scale with Ailment Damage.
- Do not crit.

Open Wounds does not stack. Reapplication refreshes the duration and retains whichever wound has the higher tick damage.

```js
var total = directDamage * 0.30 * (1 + (hero._ailmentDmg || 0) / 100);
var tick = Math.max(1, Math.round(total / 4));
var oldTick = enemy._openWound ? enemy._openWound.tickDmg : 0;

enemy._openWound = {
  tickDmg: Math.max(oldTick, tick),
  ticksLeft: 4,
  nextTick: now + 1000,
  expiresAt: now + 4000
};
enemy._healingPreventedUntil = Math.max(enemy._healingPreventedUntil || 0, now + 4000);
```

Every enemy-healing and regeneration path should use a common check such as `canEnemyHeal(enemy, now)`.

## Culling Strike

The affix value is the execution threshold.

After an eligible direct hit:

- Normal enemies and rares at or below the threshold are killed immediately.
- Guardians use half the displayed threshold.
- Bosses cannot be instantly killed.
- Bosses instead take 25% increased direct-hit damage while below the displayed threshold.
- Damage over time, thorns, reflection, and environmental damage cannot trigger the execution.

Resolve Culling Strike after direct damage and Crushing Blow. It should occur before ordinary death handling so there is only one kill-reward path.

The maximum ordinary threshold is intentionally 8%. This keeps generic gloves below Ranger Execute Shot, the Warrior Execute technique, and the existing Executioner divine effect.

## Stagger on Hit

The affix value is its proc chance. Stagger represents knockback without positional displacement.

| Target | Delay added to next attack |
|---|---:|
| Normal enemy | 150ms |
| Rare or guardian | 100ms |
| Boss | 60ms |

Rules:

- Roll once per eligible attack execution.
- Each target has a 750ms Stagger cooldown.
- Push `enemyNextAtk` forward rather than applying freeze.
- Do not delay scripted boss transitions or invulnerability phases.
- Stagger does not share freeze or stun diminishing returns.

```js
if (now >= (enemy._staggerCooldownUntil || 0)) {
  var delay = enemy.isBoss ? 60 : enemy.isRarePack || enemy.isGuardian ? 100 : 150;
  enemyNextAtk += delay;
  enemy._staggerCooldownUntil = now + 750;
}
```

## Recommended affix weights

The recovery alternatives together should have roughly the weight of one ordinary affix, not two.

| Affix or family | Relative weight |
|---|---:|
| Ordinary glove stat | 1.00 |
| Life on Hit | 0.50 |
| Energy Shield on Hit | 0.50 |
| Crushing Blow | 0.65 |
| Open Wounds | 0.80 |
| Culling Strike | 0.45 |
| Stagger on Hit | 0.80 |

Act-specific affix themes may multiply these weights later. Do not duplicate a recovery-family member to create a false 2x family weight.

## Aggregating equipped stats

Add the new keys to all item-stat ingestion paths, save serialization, score calculation, tooltips, comparisons, reforging, enchanting, debug item generation, and offline-combat snapshots.

Recommended derived hero fields:

```js
hero._lifeOnHitBps
hero._shieldOnHitHalfPct
hero._crushingBlow
hero._openWounds
hero._cullingStrike
hero._staggerOnHit
```

Values from ordinary equipment add together. Since there is initially only one glove slot, stacking primarily matters for sets, uniques, temporary effects, or future equipment changes.

Clamp the final ordinary values defensively:

```js
hero._crushingBlow = Math.min(hero._crushingBlow, 25);
hero._openWounds = Math.min(hero._openWounds, 50);
hero._cullingStrike = Math.min(hero._cullingStrike, 15);
hero._staggerOnHit = Math.min(hero._staggerOnHit, 40);
```

Authored uniques may bypass these caps only when their implementation explicitly says so.

## Resolution order

For the first eligible direct hit in an attack sequence:

1. Verify the target is valid and not invulnerable.
2. Roll and apply Crushing Blow before normal direct damage.
3. Resolve the direct hit and determine actual damage dealt.
4. If actual damage is greater than zero, restore Life or Energy Shield on Hit.
5. Roll Open Wounds using the actual direct damage as its base.
6. Roll Stagger.
7. Check Culling Strike.
8. Enter the game's single normal death and reward path.

Do not call the ordinary kill-reward function from more than one affix branch.

## Tooltip copy

Examples:

```text
[T3] Restore 0.68% maximum Life on Hit
[T2] Restore 8.5% maximum Energy Shield on Hit
[T3] 11% chance to inflict Crushing Blow
[T2] 15% chance to inflict Open Wounds
[T1] Cull non-boss enemies below 3% Life
[T3] 20% chance to Stagger on Hit
```

Expanded tooltip definitions:

- **Life on Hit:** Restores Life once per direct attack, regardless of projectiles or enemies struck.
- **Energy Shield on Hit:** Restores existing Energy Shield once per direct attack. Requires maximum Energy Shield.
- **Crushing Blow:** Removes part of the target's current Life before the attack. Reduced against elites and bosses.
- **Open Wounds:** Prevents healing and deals physical damage over four seconds.
- **Culling Strike:** Kills non-boss enemies below the listed threshold. Deals increased damage to low-Life bosses.
- **Stagger:** Delays the target's next attack. Reduced against elites and bosses.

## Item scoring

Initial score weights are provisional and should be pressure-tested against existing auto-equip decisions:

```js
SCORE_WEIGHTS.lifeOnHitBps = 0.9;
SCORE_WEIGHTS.shieldOnHitHalfPct = 0.7;
SCORE_WEIGHTS.crushingBlow = 4.0;
SCORE_WEIGHTS.openWounds = 2.2;
SCORE_WEIGHTS.cullingStrike = 5.0;
SCORE_WEIGHTS.staggerOnHit = 1.8;
```

Do not let auto-equip scoring treat Culling Strike's threshold as ordinary additive damage. The provisional weight only gives the comparison system a usable first approximation.

## Save compatibility

- Missing new keys must behave as zero.
- Do not rewrite old items during load.
- Old gloves without `affixTiers` remain valid.
- If the UI requires a tier for an old or authored stat, display no tier rather than inventing one.
- Preserve rolled tier and resolved roll range on newly generated gloves so later balance changes do not rewrite existing item tooltips.

## Required tests

### Generation

- Each glove stat can roll T1, T2, and T3.
- Tier odds approximately match each content band over a large simulation.
- Life on Hit and Energy Shield on Hit never coexist on non-unique gloves.
- Reforge, enchant, and infusion cannot bypass the recovery-family exclusion.
- An authored unique can deliberately contain both recovery stats.

### Combat

- One AoE attack hitting multiple enemies triggers recovery once.
- A multishot attack triggers recovery once.
- Echoes and secondary explosions do not trigger recovery.
- DoTs, thorns, companions, and reflected damage do not trigger glove effects.
- Life-on-Hit and shield-recovery budgets cap correctly at extreme attack speed.
- Energy Shield on Hit does nothing at zero maximum Energy Shield.
- Crushing Blow uses current HP and receives the correct target-class reduction.
- Crushing Blow cannot independently kill the target.
- Open Wounds prevents every enemy-healing path and retains the stronger reapplication.
- Culling Strike never executes bosses and uses half threshold on guardians.
- Stagger cannot delay scripted transitions or bypass its cooldown.
- Every affix-generated death passes through the normal reward path exactly once.

### UI and offline combat

- Compact and expanded tooltips display the correct unit and tier.
- Decimal Energy Shield rolls display in 0.5% increments.
- Item comparison and auto-equip do not produce `NaN` for new stats.
- Offline simulation uses the same one-trigger-per-attack rule or an equivalent expected-value model.
- Combat recap separates Crushing Blow and Open Wounds damage from ordinary direct damage.

## Balance knobs to revisit after playtesting

These values are intentional starting points, not promises that should be hard-coded in multiple places:

- Life-on-Hit cap: 3% maximum HP per second.
- Energy-Shield-on-Hit cap: 25% maximum ES per second.
- Crushing Blow target fractions: 8% / 2% / 0.5% current HP.
- Open Wounds: 30% of the triggering hit over four seconds.
- Boss low-life Culling bonus: 25% increased direct-hit damage.
- Stagger delays: 150ms / 100ms / 60ms and 750ms target cooldown.

Put these in one balance object so later tuning does not require searching through combat code.

```js
var GLOVE_AFFIX_BALANCE = {
  lifeOnHitMaxHpPerSecond: 0.03,
  shieldOnHitMaxEsPerSecond: 0.25,
  crushingBlowCurrentHp: { normal: 0.08, elite: 0.02, boss: 0.005 },
  openWoundsHitFraction: 0.30,
  openWoundsDurationMs: 4000,
  cullBossDamageMultiplier: 1.25,
  staggerDelayMs: { normal: 150, elite: 100, boss: 60 },
  staggerCooldownMs: 750
};
```

