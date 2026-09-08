# Area selector artwork handoff

Approved artwork for the area-selector visual changes. No live game code has been modified.

- mode-icons/: first-column gateway/ruin/abyss icons for Normal, Desolation, The Everdeep. IDs mode-normal, mode-desolation, mode-everdeep.
- difficulty-icons/: first-column skulls for Normal, Nightmare, Hell. Atlas IDs normal, nightmare, hell. Keep this atlas separate from mode-icons.
- banners/: five selected act banners and preview.html. Selection: Act1 panel1, Act2 panel2, Act3 panel3, Act4 panel1, Act5 snow panel1.

Icons include transparent PNGs at 32/48/64/128px and 64px Phaser JSON hash atlases. Use 64px assets for 32px CSS display. Review PNGs and source crops are QA/reference files, not required runtime downloads.

Wire mode emblems into existing modeRow() entries and difficulty skulls into baseDetail() difficulty buttons. Preserve the existing mode/difficulty unlock rules, callbacks and active badges. Use separate image and text elements so translations and selected/disabled states remain functional. Do not bake text into new art.

Use the five banners as act-row backgrounds with cover and right-center positioning; keep runtime names over the dark left side. All five production banners are standardized to 1200 × 200 (6:1) using proportional scaling and right-center cropping. Original crops are preserved in banners/originals/. Keep proportional cover behavior when the UI row has another aspect ratio. Preserve _zpAct() behavior (travel then close) and independent act-drop information controls, including for locked acts.

banners/preview.html is the earlier interactive visual prototype. It demonstrates banner rows and placeholder mode/difficulty buttons; it has not yet been updated to display these new icons. It is not a drop-in game replacement. Mobile bottom-sheet behavior was discussed but remains unimplemented in that prototype.

The generated act frame is still an unsliced review concept and is intentionally not labeled production-ready here.

