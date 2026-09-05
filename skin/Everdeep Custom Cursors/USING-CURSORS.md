# Using the Everdeep cursor set

Use the 48px set by default. It remains readable against Everdeep's dark panels without covering as much UI as the 64px set. The 32px set is available for players who prefer a smaller cursor, and 64px works as an accessibility option.

## 1. Copy the files

Copy these into the game while preserving the folder relationship:

```text
index.html
cursors.css
assets/
  default-48.png
  pointer-48.png
  attack-48.png
  inspect-48.png
  blocked-48.png
  wait-48.png
  ...the 32px and 64px versions
```

If the assets live somewhere else, change each URL in `cursors.css`. The URLs are relative to the stylesheet, not to `index.html`.

For the web build, upload the PNGs and stylesheet with the rest of the game. For the executable build, include them beside the local game files. Do not leave production URLs pointed at this Downloads folder or the local preview server.

## 2. Load the stylesheet after the existing game styles

Add this after the game's current style block or other skin styles:

```html
<link rel="stylesheet" href="cursors.css?v=2">
```

Loading it last matters because the current Everdeep build already defines `--cursor-gold` and applies that cursor to clickable elements with `!important`. The packaged stylesheet has `ed-cursors-*` scoped overrides for those rules.

## 3. Enable one size on desktop

Add one class to `body`:

```html
<body class="ed-cursors-48">
```

If body classes are assembled by JavaScript, enable the cursor after startup instead:

```js
if (window.matchMedia('(pointer: fine)').matches) {
  document.body.classList.add('ed-cursors-48');
}
```

Only apply one `ed-cursors-*` class at a time. Touch devices ignore mouse cursors, but the pointer check avoids adding unnecessary styling there.

To support a setting, remove all three size classes before adding the selected one:

```js
function setCursorSize(size) {
  document.body.classList.remove('ed-cursors-32', 'ed-cursors-48', 'ed-cursors-64');
  if (size) document.body.classList.add('ed-cursors-' + size);
}

setCursorSize(48);
```

Store `32`, `48`, `64`, or an empty value for native cursors in the game's existing settings/save system. Call `setCursorSize` after loading that setting.

## 4. Cursor mapping

The stylesheet automatically applies the hand to normal buttons, links, selects, summaries, labeled controls, `[onclick]` elements, and inline `cursor:pointer` elements. Disabled buttons automatically use the blocked cursor. Text fields retain the native text cursor.

Use `data-cursor` for special surfaces:

```html
<div class="item-card" data-cursor="inspect">...</div>
<div class="trial-target" data-cursor="attack">...</div>
<div class="locked-action" data-cursor="blocked">...</div>
<div class="loading-surface" data-cursor="wait">...</div>
```

Recommended roles:

| Cursor | Use it for | Avoid using it for |
|---|---|---|
| Default arrow | Empty panels, combat scene and general movement | Buttons and links |
| Pointing hand | Buttons, item selection, tabs, shop purchases | Static labels |
| Sword | A real click-to-attack or combat-target action | Everdeep's automatic combat canvas when clicking does nothing |
| Magnifier | Item details, previews, collection entries and inspect actions | Ordinary selection |
| Blocked arrow | Disabled or unavailable actions | Hidden requirements that are still clickable |
| Hourglass | A temporarily busy surface during a real operation | Long idle gameplay; it implies input is temporarily unavailable |

The sword cursor should only appear on Phaser content if clicking that canvas performs an attack or target action. If the whole combat canvas becomes interactive, this is enough:

```js
const combatCanvas = document.querySelector('#phaser-container canvas');
if (combatCanvas) combatCanvas.dataset.cursor = 'attack';
```

Remove the attribute when the interaction ends:

```js
delete combatCanvas.dataset.cursor;
```

## 5. Temporary wait state

Set the wait cursor only around an operation that temporarily blocks input:

```js
async function withWaitCursor(element, work) {
  const previous = element.dataset.cursor;
  element.dataset.cursor = 'wait';
  try {
    return await work();
  } finally {
    if (previous) element.dataset.cursor = previous;
    else delete element.dataset.cursor;
  }
}
```

Do not use the hourglass as an animated loading indicator; it is a static cursor image.

## 6. Hotspots and fallbacks

`hotspots.json` contains the exact coordinates used by the CSS. Do not assume every cursor uses `(0, 0)`: the sword uses its blade tip, the hand uses its fingertip, the magnifier uses the lens center, and the hourglass uses its center.

Every CSS declaration ends with a native fallback such as `pointer`, `not-allowed`, or `wait`. If a browser rejects a custom image, the interface remains usable.

## 7. Verification checklist

Test the web build and packaged executable separately:

- Confirm the default arrow appears over empty UI and the hand appears over buttons.
- Confirm the click lands under the visible tip for the arrow, hand, and sword.
- Confirm disabled buttons show the blocked cursor and remain unclickable.
- Confirm text fields still show a text caret cursor.
- Confirm resize, drag, and grab interactions keep their specialized native cursors unless deliberately assigned a custom cursor.
- Check dark panels, pale overlays, 100% UI scale, and the largest supported UI scale.
- Check 32px, 48px, 64px, and native/off settings.
- Check the HTML web build and the local executable asset paths.

Open `preview.html` before integration to compare all three sizes and test the hotspots interactively.
