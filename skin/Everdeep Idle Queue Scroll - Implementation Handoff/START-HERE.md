# Idle Queue scroll skin — coding agent handoff

Implement the approved scroll presentation in the existing Idle Queue. This is a visual/layout change, not a new queue system. Open `index.html` to inspect the packaged mockup; its assets are local. Read `IMPLEMENTATION.md` before copying code.

Approved design: charcoal vellum with silver header/footer rollers, violet accents, existing framed expedition icons, independently scrolling run list, existing scrollbar, and collapsible Pending Rewards drawer. The vellum hangs from the chain ends. The title is centered both ways within the plaque. Controls must stay inside their artwork at narrow widths.

Folders:

- `queue-scroll-skin`: final transparent PNGs, slice metadata, reference CSS and presentation adapter.
- `queue-skin-assets`: existing button/frame artwork and reward chest used by the demo.
- `queue-art-concepts/references`: existing game icon atlases, copied without alterations.
- `source`: generated master, exact generation prompt/provenance and repeatable extraction script. Not runtime assets.

The demo intentionally uses sample queue data and stubbed combat/destination handlers. Never replace production functions with those stubs. Use the real game's latest source as the behavioral authority.

No ZIP is required. Keep the folder structure to open the preview.
