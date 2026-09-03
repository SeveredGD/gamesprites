# Everdeep Hero Focus Character Select

## Production goal

Replace the current character-manager-first selection screen with the approved **Hero Focus** layout in `index.html`.

The screen should answer these questions in this order:

1. Which class am I viewing?
2. Which saved character is selected?
3. What is that character's current progression?
4. How do I continue?
5. How do I create or manage another character?

Do not copy the sample names or values from the mockup. The mockup is visual only. Populate it through the existing save and class-select functions in the production HTML.

## Approved desktop structure

Keep the existing full-screen `#class-select-overlay` and outer ornate-silver `.cs-panel` frame. Replace the contents of `#cs-cards` with this hierarchy:

```text
EVERDEEP IDLE
Choose a hero to continue

[ Sorceress ] [ Ranger ] [ Warrior ] [ Rogue ]

+--------------------------+  +---------------------------------------+
| Selected hero silhouette |  | Selected class's saved characters    |
| on class platform        |  |                                       |
|                          |  | [selected character row]              |
| Class name               |  | [other character row]                 |
| HP / play style          |  | [empty slot / New run]                |
| Short class description  |  |                                       |
| 3 save slots             |  | [ Continue as CHARACTER ]             |
|                          |  | Rename · Reorder · Delete              |
+--------------------------+  +---------------------------------------+

Cloud status · Settings · globe/language selector
```

Desktop proportions from the approved mockup:

- Main content width: use the existing `.cs-panel` cap; the mockup is approximately 1180px wide.
- Class strip: four equal columns with a 10px gap.
- Focus area: two columns with an 18px gap.
- Left identity panel: approximately 35–38% of the focus area.
- Right roster panel: approximately 62–65%.
- Both panels use the normalized ornate-silver subtle frame and black interior.

## Existing production data and functions

Reuse these existing definitions from the game. Do not create a second save or class model.

### Classes

- `CLASS_SELECT`
- `CLASS_SELECT_ICON_URL`
- `_cmTab`
- `_cmSetTab(classKey)`

Use `CLASS_SELECT` for:

- class key
- class name
- class color
- metadata / HP / role
- class description
- crest position in `new_class_select_icons_2.png`

### Saves and ordering

- `_slotSummary(classKey, slot)`
- `_cmOrder(classKey)`
- `_cmSaveOrder(classKey, order)`
- `_cmMove(index, direction)`
- `_cmWireDrag()` if desktop drag reordering is retained
- `SAVE_SLOT_COUNT`

### Character actions

- `selectClass(classKey, slot)` to load the selected save
- `_promptCharName(classKey, slot)` to create a character in an empty slot
- `_cmAskRename(classKey, slot)`
- `_cmAskDelete(classKey, slot)`

Keep the current rename and type-name-to-delete confirmation overlays. Only move the launch controls; do not weaken deletion confirmation.

### Cloud and language

- `_cloudCfg.on` and `_cloudCfg.id`
- `_csRenderCloud()` and existing cloud link/pull functions
- `_i18nSetLang(lang)`
- `_syncLangSelect()`

Language options currently exposed by production:

```html
<option value="en">English</option>
<option value="es">Español</option>
<option value="ru">Русский</option>
<option value="zh">中文</option>
```

Use the visible globe icon `🌐` beside the language `<select>`. The control must retain `aria-label="Language"`.

## Selection state

Add one small piece of UI-only state for the selected character row.

Suggested shape:

```js
var _cmSelectedSlotByClass = Object.create(null);
```

Selection rules:

1. When a class tab opens, read that class's saved order from `_cmOrder(classKey)`.
2. If the stored selected slot still contains a valid save, keep it selected.
3. Otherwise select the first filled slot in display order.
4. If no filled slots exist, there is no selected character and no Continue button.
5. Clicking a filled row changes the selected slot; it must not immediately launch the game.
6. The large Continue button calls `selectClass(_cmTab, selectedSlot)`.
7. After deleting the selected character, rerun the fallback selection rule.
8. After changing class, update the silhouette, platform, description, roster, selected row and Continue label in the same render.

This selection is presentation state. It does not need to be written into the character save. Storing the last selection in `localStorage` is optional.

## Class tabs

Keep the four current class crests as the compact selection strip. Do not use the large hero silhouette in these tabs.

Each tab contains:

- class crest
- class name
- short role / HP line on desktop
- `filled / SAVE_SLOT_COUNT`
- active state using the class color and full brightness

Use the existing `new_class_select_icons_2.png` sheet and its current 2x2 frame positions. Do not create four duplicate crest files.

Inactive tabs should be dimmed, not hidden. Class colors are accents; the underlying frames remain chain-silver/black.

## Hero identity panel

### Silhouette

Reuse the existing production sprite map:

```js
HERO_SPRITES = {
  sorceress: _REPO + 'sorc-class-f.png',
  warrior: _REPO + 'warrior-class.png',
  rogue: _REPO + 'rogue-class.png',
  ranger: _REPO + 'Hero_Ranger.png'
};
```

Use the same treatment as `#pd-doll-hero`:

```css
filter:
  brightness(0)
  opacity(.90)
  drop-shadow(0 0 1px #d0b971aa)
  drop-shadow(0 0 13px #a8883f38);
background-repeat: no-repeat;
```

The approved desktop silhouette height and fit are based on the existing `PD_HERO_FIT` corrections:

- Sorceress: approximately 225px in the mockup focus panel.
- Warrior: approximately 202px.
- Rogue: approximately 213px.
- Ranger: approximately 530px background height because its source has a very wide transparent canvas; shift X approximately 33px left.

All silhouettes were raised 9px after the first platform pass. Preserve this lift so the feet sit on the platform's top plane rather than on its front rim.

Do not replace these silhouettes with the class crest. Do not recolor the full hero art.

### Platforms

Use the following production asset names from their primary asset folders:

| Class | File | Preview dimensions | Approx. file size |
|---|---|---:|---:|
| Sorceress | `assets/platform-sorceress-transparent.png` | 640x153 | 179 KB |
| Ranger | `assets/platform-ranger-transparent.png` | 640x142 | 158 KB |
| Warrior | `assets/platform-warrior-transparent.png` | 640x153 | 173 KB |
| Rogue | `assets/platform-rogue-transparent.png` | 640x135 | 138 KB |

Do not take another copy of these assets from this mockup folder. Resolve these filenames through the game's primary asset location. The dimensions and sizes in the table only describe the versions used to validate the layout.

Recommended desktop platform box:

```css
width: 330px;
height: 94px;
background-size: contain;
background-position: center;
background-repeat: no-repeat;
```

Place the platform behind the silhouette with the silhouette at the higher `z-index`. In the approved mockup the platform begins approximately 184px from the top of the identity panel.

The front rim may overlap the visual footprint, but it must not cover the character's ankles. Validate every class separately; Ranger's companion also needs to remain fully on the top plane.

### Text

Below the hero/platform composite show:

- class name in its class accent color
- `CLASS_SELECT.meta`
- `CLASS_SELECT.blurb`
- one neutral `3 save slots` badge
- green `Cloud ready` badge only when cloud sync is enabled

Do not add promotional or flowery copy. Use the current production class descriptions.

## Character roster

Render filled saves first in `_cmOrder()` order, followed by empty slots.

A filled row contains:

- player-entered character name, safely escaped with `_cmEsc()`
- level and class
- Epoch and SSF badges where applicable
- gear score
- furthest progression
- selected state

Use the current `_slotSummary()` calculations for gear score and furthest progression. Do not recalculate them in a second component.

Selected-row treatment:

- brighter silver border
- narrow class-color line on the left
- no large glow across the entire row
- keyboard focus must remain visible independently of selected state

The small `Select` control in the mockup is optional. The whole row should be clickable/tappable, so production can omit that small button if it feels redundant.

### Empty slot

Each empty slot contains:

- `Create a new CLASS`
- `Start a fresh run`
- one `New run` button

`New run` calls `_promptCharName(_cmTab, emptySlot)`.

There must not be a second New Character button below the roster. It conflicted with the empty-slot action and was removed from the approved layout.

## Continue and management actions

The primary action is one full-width chain-silver button:

```text
Continue as CHARACTER_NAME
```

It loads the currently selected filled row. If there is no filled character, hide or disable it and make the first empty slot's New run action the obvious path.

Below Continue, keep these actions visually quiet:

- Rename
- Reorder
- Delete

They operate on the selected row. Delete stays red-tinted and opens the existing typed-name confirmation. Rename opens the existing rename overlay.

For reordering:

- desktop may retain drag-to-reorder
- phone should retain explicit move-up/move-down controls in a Manage state
- do not display permanent arrows beside the primary Continue action

## Footer states

### Cloud enabled

Show:

```text
Cloud sync enabled · Settings · 🌐 [language]
```

The identity panel also shows the green `Cloud ready` badge.

### Cloud not enabled

Show:

```text
Cloud sync is not linked · Link cloud sync · Settings · 🌐 [language]
```

Do not show `Cloud ready` in the identity panel. `Link cloud sync` should open the existing sync-code UI. Keep this status in the footer; do not insert the full sync-code form into the roster until the player asks to link.

The old `Change skin` link must not appear. Skin selection is no longer an option.

## Phone layout

At mobile width, keep the same information order but rearrange it:

1. Header
2. Four compact class crest tabs
3. Compact hero silhouette/platform identity block
4. Character rows
5. Full-width Continue button
6. Footer controls

Approved phone behavior:

- stage target: approximately 390px wide
- class tabs: four compact crest buttons across when space permits
- remove the desktop HP/role line inside each tab; the identity block already contains it
- identity block uses silhouette/platform on the left and class text on the right
- hide roster gear/furthest columns only when they genuinely cannot fit; do not shrink them into unreadable text
- Continue remains full width
- silhouette lift: 4px on phone
- platform display box: approximately 130x48px
- class management may wrap onto a second line or open a Manage overlay

At very narrow widths, switch class tabs to a 2x2 grid rather than reducing crests below readable size.

## Asset references

The layout requires these asset names:

```text
platform-sorceress-transparent.png
platform-ranger-transparent.png
platform-warrior-transparent.png
platform-rogue-transparent.png
```

Reference the files from their existing primary folders. Do not copy any platform, hero, crest, button or frame asset into the implementation package a second time. The existing hero PNGs, crest sheet and normalized button/frame files also remain referenced from their current locations.

## Accessibility and input

- Class tabs are real buttons with `aria-pressed` or tab semantics.
- Character rows are keyboard selectable.
- Enter/Space selects a row; the Continue button performs the launch.
- The language selector has `aria-label="Language"` even though the visible label is only `🌐`.
- Do not communicate selection only with class color; retain border/brightness changes.
- Preserve `_cmEsc()` for all imported, cloud-synced and player-entered names.
- Maintain a visible focus ring without relying on the browser's default blue outline over ornate frames.

## Acceptance checklist

- [ ] All four class tabs switch the entire identity and roster state.
- [ ] Each class uses the correct hero silhouette and platform.
- [ ] Warrior and Rogue use the revised platform art.
- [ ] Silhouette feet sit inside the platform top plane for every class.
- [ ] Ranger and companion both fit without cropping.
- [ ] Filled rows respect `_cmOrder()`.
- [ ] Clicking a row selects it without immediately loading the save.
- [ ] Continue loads the selected class and slot.
- [ ] Empty slots have one New run action.
- [ ] No second New Character button appears below the roster.
- [ ] Rename, reorder and delete target the selected save.
- [ ] Delete still requires the existing typed-name confirmation.
- [ ] Cloud-enabled and cloud-disabled states render correctly.
- [ ] Cloud-disabled state does not claim `Cloud ready`.
- [ ] The globe selector lists English, Español, Русский and 中文.
- [ ] No `Change skin` control remains.
- [ ] Desktop and phone layouts work without horizontal overflow.
- [ ] Names and progression text do not overlap controls at increased UI text size.
- [ ] Platform assets resolve from the primary asset folder with no duplicate copies.

## Visual reference

Open `index.html` in this folder and choose:

```text
1 Hero Focus
```

Use the Desktop/Phone and Cloud On/Cloud Off controls to inspect every approved state. The preview's sample characters are intentionally fake and are not implementation data. The preview folder is a visual reference, not an asset upload bundle.
