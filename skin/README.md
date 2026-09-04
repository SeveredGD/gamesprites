# Everdeep pets and Warden's Menagerie production package

This folder contains the implementation-ready Warden's Menagerie mockup and all 67 current pet sprite PNGs. It intentionally excludes monster sprites, combat-preview assets, generated source boards, QA previews, cutting guides, old slices, and build scripts.

## Package layout

- `index.html`, `app.js`, `styles.css`: desktop and compact-phone Menagerie implementation mockup.
- `pets.json`: current Menagerie data snapshot.
- `pets-data.js`: browser-loadable copy of the current data snapshot.
- `import-reviewed-pets.js`: rebuilds both data files from a review-tool instructions export.
- `assets/pets/`: all pet sprite PNGs. Put `everdeep-pet-frame-instructions.json` here after exporting it from the review tool.
- `assets/pets/tinker/`: the five Tinker companions.
- `assets/wardens-menagerie-gate-master-1284x540.png`: complete approved gate overlay.
- `assets/wardens-menagerie-gate-left-642x540.png` and `assets/wardens-menagerie-gate-right-642x540.png`: matched gate halves used by the mockup.
- `assets/ui/`: the three UI images referenced by the Menagerie styles.

## Refresh the Menagerie data

After placing the exported pet-only instructions JSON in `assets/pets/`, run this from the package root:

```powershell
node import-reviewed-pets.js "assets/pets/everdeep-pet-frame-instructions.json"
```

The importer includes only entries whose `type` is `pet`, preserves frame order/exclusions and pixel settings, checks that every referenced sprite exists, then rewrites `pets.json` and `pets-data.js`.

Open `index.html` to review the desktop and compact-phone layouts.
