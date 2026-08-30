# Instructions for the production coding agent

Import the loading-screen package without replacing the current game's asset-preload logic.

1. Copy `assets/`, `styles.css`, and `loading-screens.js` into the production project. Preserve the relative paths or rewrite them consistently.
2. Copy the contents of `<main id="everdeep-loader">` from `index.html` into the production document. Do not copy `.ed-devtools`.
3. Load `styles.css` after the main skin CSS. Load `loading-screens.js` after the loader markup exists.
4. Choose a screen with `EverdeepLoadingScreens.show('gate', options)` or `EverdeepLoadingScreens.show('reliquary', options)`.
5. In the existing `_lsWarm` callback, replace the old fill-width assignment with `EverdeepLoadingScreens.setProgress(frac * 100)`. Keep the existing manifest settlement, minimum duration, maximum timeout, skip behavior, and fade-out logic unchanged.
6. Pass the live identity with `EverdeepLoadingScreens.setCharacter(who)` and the phase with `EverdeepLoadingScreens.setPhase('Descending')`.
7. Call `EverdeepLoadingScreens.hide()` from the existing `_hideLoadScreen` path. Do not add a second loading timer.
8. Keep the existing `body.ed-loading` behavior that hides Pause/Swap controls.

The background plates are opaque 16:9 images and use `background-size: cover`. Verify ultrawide and portrait crops. The responsive rules already increase loader width and resize the reliquary arc on narrow screens.

Public API:

```js
EverdeepLoadingScreens.show('gate', {
  character: who,
  phase: 'Descending',
  lore: 'The deeper you go, the more the Deep remembers.',
  progress: 0
});
EverdeepLoadingScreens.setProgress(frac * 100);
EverdeepLoadingScreens.hide();
```
